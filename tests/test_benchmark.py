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


def test_faithfulness_vs_truth_flags_mismatch(tmp_path):
    """A synthetic cell where a faithfulness metric is anti-aligned with GT must
    be flagged as a mismatch (the core BENCHMARK_GT claim), on shared molecules."""
    import json

    from molsanity.benchmark.faithfulness_vs_truth import analyse

    root = tmp_path / "audit"
    # Attributor A: high faithfulness, LOW ground truth (faithful-but-wrong).
    # Attributor B: low faithfulness, HIGH ground truth (the GT-best).
    def recs(occ, gt):
        return [{"graph_id": i, "occ_spearman": occ, "fidelity_plus": occ,
                 "characterization": occ, "gt_auroc": gt} for i in range(8)]

    # Three attributors so the Spearman rank correlation is defined (needs >=3).
    for name, occ, gt in [("A", 0.9, 0.10), ("B", 0.1, 0.90), ("C", 0.5, 0.50)]:
        d = root / f"DS__GINE__{name}__scaffold"
        d.mkdir(parents=True)
        (d / "records.json").write_text(json.dumps(recs(occ, gt)))

    res = analyse("DS", "GINE", "scaffold", root=root)
    assert res["gt_best"] == "B"
    fp = next(s for s in res["selections"] if s["faithfulness_metric"] == "fidelity_plus")
    assert fp["faithfulness_pick"] == "A"          # faithfulness picks the wrong one
    assert fp["mismatch"] is True
    assert res["rank_correlation"]["fidelity_plus"]["rho"] < 0  # anti-aligned


def test_conclusions_are_computed_not_asserted():
    """The 'What this shows' section used to be a fixed paragraph claiming
    in-distribution 'ρ near 1, no mismatch' and shift mismatch at 'p < 0.001'.
    Neither was read back from the run. On 3 August the report had no
    in-distribution panel at all and the paragraph still described the contrast;
    the run's own in-distribution ρ was +0.20 with mismatches on every metric.
    CLAUDE.md hard rule 1 forbids a report asserting a number it did not compute.
    """
    from molsanity.benchmark.faithfulness_vs_truth import _conclusions

    def res(split, rhos, mismatches):
        return {
            "dataset": "MUTAG", "backbone": "GINE", "split": split,
            "selections": [
                {"faithfulness_metric": m, "mismatch": mm}
                for m, mm in zip(("occ_spearman", "fidelity_plus"), mismatches)
            ],
            "rank_correlation": {
                m: {"rho": r} for m, r in zip(("occ_spearman", "fidelity_plus"), rhos)
            },
        }

    # Dissociating run: correlation drops from in-distribution to shift.
    text = "\n".join(_conclusions([res("random", [0.9, 0.8], [False, False]),
                                   res("scaffold", [-0.6, -0.7], [True, True])]))
    assert "+0.85" in text and "-0.65" in text, text
    assert "dissociate" in text

    # Non-dissociating run: the report must NOT claim the finding anyway.
    text = "\n".join(_conclusions([res("random", [-0.6, -0.7], [True, True]),
                                   res("scaffold", [0.9, 0.8], [False, False])]))
    assert "does not support the dissociation claim" in text, text

    # Single regime: no contrast may be claimed.
    text = "\n".join(_conclusions([res("scaffold", [-0.6, -0.7], [True, True])]))
    assert "no" in text and "contrast is claimed" in text, text
    assert "dissociate" not in text

    # Nothing computed: nothing claimed.
    text = "\n".join(_conclusions([]))
    assert "nothing is claimed" in text.lower()


def test_default_regime_pair_is_one_dataset_across_both_splits():
    """The contrast must isolate scaffold shift, not confound it with a change
    of dataset, and it must not be satisfiable by a partial match: accepting one
    of two preferred cells produced a single-regime report under two-regime prose."""
    from molsanity.benchmark.faithfulness_vs_truth import DEFAULT_CELLS

    assert len({(d, b) for d, b, _, _ in DEFAULT_CELLS}) == 1
    assert {sp for _, _, sp, _ in DEFAULT_CELLS} == {"random", "scaffold"}
