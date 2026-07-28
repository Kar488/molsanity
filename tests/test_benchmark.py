"""Benchmark table + paired-comparison tests (pure, no heavy deps)."""
import numpy as np

from molsanity.benchmark.tables import (
    head_to_head_table,
    paired_method_comparison,
)


def _cell(dataset, backbone, attributor, split, values):
    """Build a fake cell of per-molecule records for one metric column."""
    return {
        f"{dataset}__{backbone}__{attributor}__{split}": [
            {"graph_id": i, "occ_spearman": v, "gt_auroc": v * 0.5,
             "stability": 0.9, "motif_top1_share": 0.8, "fidelity_plus": 0.2,
             "fidelity_minus": 0.1, "sparsity": 0.7}
            for i, v in enumerate(values)
        ]
    }


def test_head_to_head_summarises_each_cell():
    cells = {}
    cells.update(_cell("MUTAG", "GINE", "IntegratedGradients", "scaffold", [0.5, 0.6, 0.7]))
    cells.update(_cell("MUTAG", "GINE", "GNNExplainer", "scaffold", [0.1, 0.2, 0.3]))
    rows = head_to_head_table(cells, seed=0)
    assert len(rows) == 2
    ig = next(r for r in rows if r["attributor"] == "IntegratedGradients")
    assert abs(ig["occ_spearman"] - 0.6) < 1e-9
    assert ig["n_mol"] == 3


def test_paired_comparison_on_shared_molecules():
    cells = {}
    cells.update(_cell("MUTAG", "GINE", "IntegratedGradients", "scaffold", [0.5, 0.6, 0.7, 0.8, 0.9]))
    cells.update(_cell("MUTAG", "GINE", "GNNExplainer", "scaffold", [0.1, 0.2, 0.3, 0.4, 0.5]))
    comps = paired_method_comparison(cells, "MUTAG", "GINE", "scaffold", metric="occ_spearman")
    assert len(comps) == 1
    c = comps[0]
    assert c["n_paired"] == 5
    # Methods are compared in sorted order; IG is uniformly 0.4 above GNNExplainer,
    # so the sign of median Δ(A−B) follows which method is A.
    if c["method_a"] == "IntegratedGradients":
        assert c["median_diff"] > 0
    else:
        assert c["median_diff"] < 0
