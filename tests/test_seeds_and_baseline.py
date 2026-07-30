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


def test_results_rows_are_keyed_by_seed(tmp_path):
    """Three seeds must produce three rows, not overwrite one another.

    Without the seed in the key a multi-seed run writes each cell's three
    results to the same slot and keeps the last, discarding two thirds of the
    matrix while the file still looks complete.
    """
    from molsanity.reporting import update_results_md

    out = tmp_path / "RESULTS.md"
    rows = [{"task": "graph-classification", "dataset": "MUTAG",
             "backbone": "GINE", "attributor": "IG", "split": "scaffold",
             "seed": s, "n_mol": 56, "acc": 0.7, "auc": 0.9,
             "gt_auroc": g, "gt_auprc": 0.3, "motif_top1": 0.8,
             "occ_spearman": 0.4, "occ_top1": 0.5, "fid+": 0.1, "fid-": 0.0,
             "sparsity": 0.8, "ece": 0.1}
            for s, g in ((0, 0.53), (1, 0.61), (2, 0.48))]
    update_results_md(rows, out)

    body = out.read_text()
    for val in ("0.530", "0.610", "0.480"):
        assert val in body, f"seed row {val} was overwritten"
    data = [ln for ln in body.splitlines()
            if ln.startswith("| MUTAG ")]
    assert len(data) == 3, f"expected 3 rows, got {len(data)}"


def test_rows_still_overwrite_within_a_seed(tmp_path):
    """Re-running the same cell at the same seed must replace, not duplicate."""
    from molsanity.reporting import update_results_md

    out = tmp_path / "RESULTS.md"
    base = {"task": "graph-classification", "dataset": "MUTAG",
            "backbone": "GINE", "attributor": "IG", "split": "scaffold",
            "seed": 0, "n_mol": 56, "acc": 0.7, "auc": 0.9, "gt_auroc": 0.10,
            "gt_auprc": 0.3, "motif_top1": 0.8, "occ_spearman": 0.4,
            "occ_top1": 0.5, "fid+": 0.1, "fid-": 0.0, "sparsity": 0.8,
            "ece": 0.1}
    update_results_md([base], out)
    update_results_md([{**base, "gt_auroc": 0.99}], out)
    from molsanity.reporting import RESULTS_HEADER

    rows_out = [ln for ln in out.read_text().splitlines()
                if ln.startswith("| MUTAG ")]
    assert len(rows_out) == 1, "same cell at the same seed must not duplicate"
    cells = [c.strip() for c in rows_out[0].strip("|").split("|")]
    gt = cells[RESULTS_HEADER.index("gt_auroc")]
    assert gt == "0.990", f"gt_auroc column is {gt}, expected the newer value"


def test_paper_build_collapses_seed_rows_to_one_per_cell():
    """Otherwise a three-seed run triplicates every row of every table."""
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "paper" / "figs"))
    import msdata as D

    recs = [{"dataset": "MUTAG", "backbone": "GINE", "attributor": "IG",
             "split": "scaffold", "seed": s, "gt_auroc": g, "occ_spearman": 0.4}
            for s, g in ((0, 0.50), (1, 0.60), (2, 0.40))]
    out = D._collapse_seeds([dict(r) for r in recs])

    assert len(out) == 1, "three seeds must collapse to one row per cell"
    row = out[0]
    assert row["n_seeds"] == 3 and row["seeds"] == [0, 1, 2]
    assert "seed" not in row
    assert row["gt_auroc"] == pytest.approx(0.50)
    import statistics as st
    assert row["gt_auroc_sd"] == pytest.approx(st.stdev([0.50, 0.60, 0.40]))
    # A field identical across seeds still gets an sd, of zero.
    assert row["occ_spearman_sd"] == pytest.approx(0.0)


def test_single_seed_results_pass_through_unchanged():
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "paper" / "figs"))
    import msdata as D

    recs = [{"dataset": "MUTAG", "backbone": "GINE", "attributor": "IG",
             "split": "scaffold", "gt_auroc": 0.5},
            {"dataset": "MUTAG", "backbone": "GINE", "attributor": "Saliency",
             "split": "scaffold", "gt_auroc": 0.1}]
    out = D._collapse_seeds([dict(r) for r in recs])
    assert len(out) == 2
    assert all(r["n_seeds"] == 1 for r in out)
    assert all("gt_auroc_sd" not in r for r in out)


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
