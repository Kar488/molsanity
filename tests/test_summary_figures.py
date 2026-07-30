"""Summary-figure tests: render from synthetic cells without heavy training."""
import pytest

pytest.importorskip("matplotlib")

from molsanity.viz.summary import (
    attributor_gt_bar,
    faithfulness_stability_ecdf,
    regime_stratification_figure,
)


def _cells():
    def rec(i, gt, occ, stab, regime):
        return {"graph_id": i, "gt_auroc": gt, "occ_spearman": occ,
                "stability": stab, "regime": regime}
    return {
        "MUTAG__GINE__IntegratedGradients__scaffold": [
            rec(i, 0.5 + 0.01 * i, 0.4, 0.7, "confident_correct") for i in range(10)
        ],
        "MUTAG__GINE__Saliency__scaffold": [
            rec(i, 0.03, 0.38, 0.9, "borderline") for i in range(10)
        ],
    }


def test_gt_bar_renders(tmp_path):
    info = attributor_gt_bar(_cells(), tmp_path / "gt_bar")
    assert info and (tmp_path / "gt_bar.pdf").exists() and (tmp_path / "gt_bar.svg").exists()


def test_ecdf_renders(tmp_path):
    info = faithfulness_stability_ecdf(_cells(), tmp_path / "ecdf")
    assert info and (tmp_path / "ecdf.svg").exists()


def test_regime_figure_renders(tmp_path):
    info = regime_stratification_figure(_cells(), tmp_path / "regime")
    assert info and (tmp_path / "regime.pdf").exists()


def test_no_cells_returns_none(tmp_path):
    assert attributor_gt_bar({}, tmp_path / "empty") is None
