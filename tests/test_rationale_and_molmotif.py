"""The two answers to the strongest reviewer objection about ground truth.

The objection (Faber et al., KDD 2021) is that a low GT AUROC may mean the
model solved the task via a different, equally valid rationale, so calling the
attribution "wrong" conflates a property of the model with a property of the
explanation. Two things answer it:

1. ``MolMotif`` removes the proxy entirely. Real molecules are relabelled by
   presence of a chemical substructure, so that substructure *defines* the
   label. It is the only arm that is simultaneously molecular and exactly
   labelled.
2. ``rationale_use`` makes the objection testable per molecule. Occlude the
   ground-truth substructure: if the prediction collapses, the model is using
   it, and an attribution pointing elsewhere is wrong by the model's own
   behaviour rather than by disagreement with a chemical prior.
"""
from __future__ import annotations

import numpy as np
import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("torch_geometric")

from molsanity.audit.rationale import faber_partition, rationale_use  # noqa: E402


class _SubsetModel(torch.nn.Module):
    """Reads only the atoms in ``uses``; everything else is inert.

    Gives an analytically known answer: reliance must be +1 when ``uses`` is
    the ground truth and -1 when it is disjoint from it.
    """

    def __init__(self, n, uses):
        super().__init__()
        self.w = torch.zeros(n)
        self.w[list(uses)] = 4.0
        self._p = torch.nn.Parameter(torch.zeros(1))

    def forward(self, x, edge_index, edge_attr, batch, node_mask=None):
        keep = torch.ones_like(x[:, :1]) if node_mask is None else node_mask
        n_graphs = int(batch.max().item()) + 1
        vals = []
        for g in range(n_graphs):
            sel = batch == g
            vals.append((self.w * keep[sel].view(-1)).sum())
        out = torch.stack(vals)
        return torch.stack([-out, out], dim=1)


def _graph(n):
    from torch_geometric.data import Data

    ei = torch.tensor([[i, (i + 1) % n] for i in range(n)]).t().contiguous()
    ei = torch.cat([ei, ei.flip(0)], dim=1)
    return Data(x=torch.ones(n, 3), edge_index=ei,
                edge_attr=torch.ones(ei.size(1), 1),
                y=torch.tensor([1]), num_nodes=n)


# ------------------------------------------------------- rationale-use test --
def test_model_that_reads_the_rationale_is_detected():
    n = 8
    gt = np.zeros(n, dtype=np.float32)
    gt[:3] = 1.0
    out = rationale_use(_SubsetModel(n, [0, 1, 2]), _graph(n), gt, target=1)
    assert out["uses_rationale"] is True
    assert out["reliance"] > 0.5
    assert out["delta_gt"] > abs(out["delta_complement"])
    assert out["n_gt_atoms"] == 3


def test_model_that_ignores_the_rationale_is_detected():
    """This is the case where the Faber objection genuinely applies."""
    n = 8
    gt = np.zeros(n, dtype=np.float32)
    gt[:3] = 1.0
    out = rationale_use(_SubsetModel(n, [5, 6, 7]), _graph(n), gt, target=1)
    assert out["uses_rationale"] is False
    assert out["reliance"] < 0.5


def test_degenerate_masks_are_undefined_not_guessed():
    n = 6
    for gt in (np.zeros(n, dtype=np.float32), np.ones(n, dtype=np.float32)):
        out = rationale_use(_SubsetModel(n, [0]), _graph(n), gt, target=1)
        assert out["uses_rationale"] is None
        assert np.isnan(out["reliance"])


def test_mask_of_the_wrong_length_is_rejected():
    out = rationale_use(_SubsetModel(6, [0]), _graph(6),
                        np.array([1.0, 0.0], dtype=np.float32), target=1)
    assert out["uses_rationale"] is None


# ------------------------------------------------------------- the partition --
def test_partition_isolates_failures_faber_cannot_explain():
    records = [
        # Model uses the rationale, attribution anti-aligned: a real failure.
        {"rationale_reliance": 0.9, "gt_auroc": 0.10},
        {"rationale_reliance": 0.8, "gt_auroc": 0.20},
        # Model uses it, attribution finds it: fine.
        {"rationale_reliance": 0.7, "gt_auroc": 0.95},
        # Model ignores it: Faber applies, excluded from the headline.
        {"rationale_reliance": 0.1, "gt_auroc": 0.05},
        {"rationale_reliance": 0.2, "gt_auroc": 0.30},
        # Unusable records are dropped, not defaulted.
        {"rationale_reliance": float("nan"), "gt_auroc": 0.5},
        {"gt_auroc": 0.5},
    ]
    out = faber_partition(records)
    assert out["n_uses_rationale"] == 3
    assert out["n_ignores_rationale"] == 2
    assert out["n_anti_aligned_despite_model_using_it"] == 2
    assert out["frac_anti_aligned_despite_model_using_it"] == pytest.approx(2 / 3)
    assert out["mean_gt_auroc_when_used"] == pytest.approx((0.10 + 0.20 + 0.95) / 3)


def test_partition_on_no_usable_records():
    out = faber_partition([{"gt_auroc": 0.5}])
    assert out["n_uses_rationale"] == 0
    assert np.isnan(out["frac_anti_aligned_despite_model_using_it"])


# ------------------------------------------------------------------ MolMotif --
def test_molmotif_mask_is_exactly_the_labelling_substructure():
    """The label IS the substructure, so the mask cannot be a proxy."""
    pytest.importorskip("rdkit")
    from rdkit import Chem

    from molsanity.data.molmotif import MOTIF_SMARTS

    ds = pytest.importorskip("molsanity.data")
    try:
        loaded = ds.load_dataset("MolMotif")
    except Exception as exc:  # dataset download unavailable
        pytest.skip(f"MolMotif source unavailable: {exc}")

    graphs = loaded.dataset
    assert len(graphs) > 100
    labels = [int(g.y) for g in graphs]
    assert set(labels) == {0, 1}
    # Balanced by construction, so accuracy is not a majority-class artefact.
    assert abs(sum(labels) / len(labels) - 0.5) < 0.05

    patt = Chem.MolFromSmarts(MOTIF_SMARTS["halogen_aromatic"])
    checked = 0
    for g in graphs:
        has_match = bool(Chem.MolFromSmiles(g.smiles).GetSubstructMatches(patt))
        assert has_match == bool(int(g.y)), "label must equal substructure presence"
        if int(g.y) == 1:
            assert 0 < float(g.node_gt.sum()) < int(g.num_nodes)
        else:
            assert float(g.node_gt.sum()) == 0.0
        checked += 1
        if checked >= 60:
            break


def test_molmotif_is_registered_as_exact_ground_truth():
    from molsanity.data.groundtruth import has_ground_truth
    from molsanity.data.manifest import MANIFEST

    assert has_ground_truth("MolMotif")
    assert MANIFEST["MolMotif"].tier == 1
    assert MANIFEST["MolMotif"].has_ground_truth


def test_molmotif_variants_all_carry_ground_truth():
    """A MolMotif variant that is not registered for ground truth trains and
    audits normally but scores zero molecules, which reads as 'no signal'
    rather than 'not wired up'. MolMotifHard cost one experiment that way.
    """
    from molsanity.data.groundtruth import has_ground_truth
    from molsanity.data.manifest import MANIFEST

    variants = [n for n in MANIFEST if n.startswith("MolMotif")]
    assert len(variants) >= 2, variants
    for name in variants:
        assert has_ground_truth(name), f"{name} is in the manifest but has no GT"
        assert MANIFEST[name].has_ground_truth, f"{name} spec disagrees with the registry"


def test_molmotif_hard_is_configured_to_avoid_the_ceiling():
    """MolMotifHard exists only to remove MolMotif's saturation. If its motif
    or source drifts back to something a rare-element shortcut solves, the arm
    silently stops being able to adjudicate the shift contrast."""
    from molsanity.data.manifest import MANIFEST

    extras = MANIFEST["MolMotifHard"].extras
    assert extras["motif"] == "carboxylic_acid", extras
    # Carbon and oxygen only: no single rare element identifies the motif.
    from molsanity.data.molmotif import MOTIF_SMARTS

    smarts = MOTIF_SMARTS[extras["motif"]]
    assert not any(e in smarts for e in ("F", "Cl", "Br", "I", "S", "N")), smarts
    # BBBP yields only 410 balanced molecules for this motif; Tox21 yields 1000.
    assert extras["source_dataset"] == "Tox21", extras
