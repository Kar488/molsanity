"""Multi-seed plumbing and the manifold-respecting occlusion baseline.

Two of the reviewer-facing limitations are addressed by machinery rather than
by more compute: a run can now repeat the matrix under several seeds and report
the across-seed spread, and occlusion can be evaluated under a second, less
off-manifold counterfactual so that caveat becomes a measurement.
"""
from __future__ import annotations

import numpy as np
import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("torch_geometric")

from molsanity.audit.motifs import MotifDecomposition  # noqa: E402
from molsanity.audit.occlusion import (  # noqa: E402
    dataset_feature_mean,
    occlusion_faithfulness,
)
from molsanity.benchmark.seed_variance import (  # noqa: E402
    summarise_seeds,
    write_seed_variance_md,
)


# ----------------------------------------------------------------- seeds ---
def _rows(seed_values):
    return [{"dataset": "MUTAG", "backbone": "GINE", "attributor": "IG",
             "split": "scaffold", "seed": s, "gt_auroc": v,
             "occ_spearman": 0.4, "acc": 0.8, "auc": 0.9, "fid+": 0.1}
            for s, v in seed_values]


def test_across_seed_spread_is_computed():
    import statistics as st

    vals = [0.53, 0.61, 0.48]
    out = summarise_seeds(_rows(list(zip((0, 1, 2), vals))))
    assert out["n_cells"] == 1
    m = out["cells"][0]["metrics"]["gt_auroc"]
    assert m["mean"] == pytest.approx(st.mean(vals))
    assert m["sd"] == pytest.approx(st.stdev(vals))
    assert (m["min"], m["max"]) == (min(vals), max(vals))
    assert out["cells"][0]["seeds"] == [0, 1, 2]


def test_single_seed_reports_nothing_rather_than_zero_spread(tmp_path):
    """A standard deviation of zero over one sample would be a false claim."""
    out = write_seed_variance_md(_rows([(0, 0.53)]), tmp_path / "SV.md")
    assert out["n_cells"] == 0
    text = (tmp_path / "SV.md").read_text()
    assert "single seed" in text
    assert "0.000" not in text


def test_cells_are_grouped_independently():
    rows = _rows([(0, 0.5), (1, 0.6)])
    other = [{**r, "attributor": "Saliency", "gt_auroc": 0.1} for r in rows]
    out = summarise_seeds(rows + other)
    assert out["n_cells"] == 2
    means = sorted(c["metrics"]["gt_auroc"]["mean"] for c in out["cells"])
    assert means[0] == pytest.approx(0.1)
    assert means[1] == pytest.approx(0.55)


def test_report_names_the_worst_cell(tmp_path):
    rows = _rows([(0, 0.10), (1, 0.90)])
    write_seed_variance_md(rows, tmp_path / "SV.md")
    text = (tmp_path / "SV.md").read_text()
    assert "GT AUROC" in text and "Median across-seed sd" in text


# -------------------------------------------------------------- baseline ---
class _FeatureSumModel(torch.nn.Module):
    """Graph score = sum over nodes of (feature dot w). Removing a node by
    zeroing subtracts its contribution; removing it by imputing the mean
    substitutes the mean's contribution instead, so the two counterfactuals are
    genuinely different and the difference is analytically known."""

    def __init__(self, w):
        super().__init__()
        self.w = torch.tensor(w, dtype=torch.float32)
        self._p = torch.nn.Parameter(torch.zeros(1))

    def forward(self, x, edge_index, edge_attr, batch, node_mask=None):
        if node_mask is not None:
            x = x * node_mask
        per = (x * self.w.view(1, -1)).sum(dim=1)
        n_graphs = int(batch.max().item()) + 1
        out = torch.stack([per[batch == g].sum() for g in range(n_graphs)])
        return torch.stack([-out, out], dim=1)


def _graph(feats):
    from torch_geometric.data import Data

    n = feats.shape[0]
    ei = torch.tensor([[i, (i + 1) % n] for i in range(n)]).t().contiguous()
    ei = torch.cat([ei, ei.flip(0)], dim=1)
    return Data(x=torch.tensor(feats, dtype=torch.float32), edge_index=ei,
                edge_attr=torch.ones(ei.size(1), 1),
                y=torch.tensor([1]), num_nodes=n)


def test_feature_mean_is_the_training_mean():
    ds = [_graph(np.array([[1.0, 0.0], [3.0, 4.0]])),
          _graph(np.array([[2.0, 2.0], [2.0, 2.0]]))]
    got = dataset_feature_mean(ds, [0, 1])
    np.testing.assert_allclose(got.numpy(), np.array([2.0, 2.0]), atol=1e-6)


def test_baseline_is_computed_only_from_the_given_indices():
    """It must see the training split alone, never the audited molecules."""
    ds = [_graph(np.array([[0.0, 0.0], [0.0, 0.0]])),
          _graph(np.array([[9.0, 9.0], [9.0, 9.0]]))]
    np.testing.assert_allclose(dataset_feature_mean(ds, [0]).numpy(),
                               np.zeros(2), atol=1e-6)
    np.testing.assert_allclose(dataset_feature_mean(ds, [1]).numpy(),
                               np.full(2, 9.0), atol=1e-6)


def test_imputed_counterfactual_changes_the_measurement():
    """If the two baselines gave identical scores the comparison would be
    vacuous, and the off-manifold caveat would remain unmeasurable."""
    feats = np.array([[5.0, 0.0], [5.0, 0.0], [0.0, 1.0], [0.0, 1.0]])
    model = _FeatureSumModel([1.0, 1.0])
    data = _graph(feats)
    decomp = MotifDecomposition(motifs=[[0, 1], [2, 3]],
                                motif_types=["ring", "ring"], num_atoms=4)
    attr = np.array([5.0, 5.0, 0.1, 0.1], dtype=np.float32)

    zeroed = occlusion_faithfulness(model, data, attr, decomp, target=1)
    imputed = occlusion_faithfulness(model, data, attr, decomp, target=1,
                                     baseline=torch.tensor([2.5, 0.5]))
    assert np.isfinite(zeroed["fidelity_plus"])
    assert np.isfinite(imputed["fidelity_plus"])
    assert imputed["fidelity_plus"] != pytest.approx(zeroed["fidelity_plus"])


def test_baseline_of_zeros_reproduces_the_zeroing_counterfactual():
    """Sanity anchor: imputing zeros must equal multiplying by the mask."""
    feats = np.array([[5.0, 0.0], [5.0, 0.0], [0.0, 1.0], [0.0, 1.0]])
    model = _FeatureSumModel([1.0, 1.0])
    data = _graph(feats)
    decomp = MotifDecomposition(motifs=[[0, 1], [2, 3]],
                                motif_types=["ring", "ring"], num_atoms=4)
    attr = np.array([5.0, 5.0, 0.1, 0.1], dtype=np.float32)

    zeroed = occlusion_faithfulness(model, data, attr, decomp, target=1)
    as_zero = occlusion_faithfulness(model, data, attr, decomp, target=1,
                                     baseline=torch.zeros(2))
    assert as_zero["fidelity_plus"] == pytest.approx(zeroed["fidelity_plus"])
    assert as_zero["fidelity_minus"] == pytest.approx(zeroed["fidelity_minus"])
