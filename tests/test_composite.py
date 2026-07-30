"""Composite multi-panel figure test (renders from synthetic cells, monkeypatched)."""
import numpy as np
import pytest

pytest.importorskip("matplotlib")


def test_results_composite_renders(tmp_path, monkeypatch):
    import molsanity.viz.composite as comp

    def rec(i, gt, occ, stab, regime):
        return {"graph_id": i, "gt_auroc": gt, "occ_spearman": occ,
                "stability": stab, "regime": regime}

    cells = {
        "MUTAG__GINE__IntegratedGradients__scaffold":
            [rec(i, 0.54, 0.41, 0.7, "confident_correct") for i in range(10)],
        "MUTAG__GINE__Saliency__scaffold":
            [rec(i, 0.03, 0.38, 0.9, "borderline") for i in range(10)],
        "MUTAG__GCN__IntegratedGradients__scaffold":
            [rec(i, 0.20, 0.18, 0.7, "confident_correct") for i in range(10)],
        "SynthMotifs__GINE__Saliency__scaffold":
            [rec(i, 0.98, 0.02, 0.9, "confident_correct") for i in range(10)],
    }
    monkeypatch.setattr(comp, "discover_cells", lambda: cells, raising=False)
    # discover_cells is imported inside the function; patch the source module too.
    import molsanity.benchmark.tables as tbl
    monkeypatch.setattr(tbl, "discover_cells", lambda: cells)

    info = comp.results_composite(tmp_path / "composite")
    assert info and (tmp_path / "composite.pdf").exists() and (tmp_path / "composite.svg").exists()
