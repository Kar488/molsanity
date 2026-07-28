"""Rich statistical figure tests: joint scatter, raincloud, heatmap (synthetic)."""
import numpy as np
import pytest

pytest.importorskip("matplotlib")
pytest.importorskip("scipy")

from molsanity.viz.richforms import (
    faithfulness_correctness_joint,
    raincloud_gt,
    results_heatmap,
)


def _cells():
    rng = np.random.default_rng(0)

    def recs(gt_mean, occ_mean, n=20):
        return [{"graph_id": i,
                 "gt_auroc": float(np.clip(gt_mean + rng.normal(0, 0.12), 0, 1)),
                 "occ_spearman": float(np.clip(occ_mean + rng.normal(0, 0.2), -1, 1))}
                for i in range(n)]

    return {
        "MUTAG__GINE__IntegratedGradients__scaffold": recs(0.55, 0.4),
        "MUTAG__GINE__Saliency__scaffold": recs(0.05, 0.38),
        "MUTAG__GINE__GNNExplainer__scaffold": recs(0.48, 0.28),
        "SynthMotifs__GINE__Saliency__scaffold": recs(0.95, 0.05),
        "SynthMotifs__GINE__IntegratedGradients__scaffold": recs(0.74, 0.1),
    }


def test_joint_scatter_renders(tmp_path):
    info = faithfulness_correctness_joint(_cells(), tmp_path / "joint")
    assert info and (tmp_path / "joint.pdf").exists() and (tmp_path / "joint.svg").exists()


def test_raincloud_renders(tmp_path):
    info = raincloud_gt(_cells(), tmp_path / "rain")
    assert info and (tmp_path / "rain.svg").exists()


def test_heatmap_renders(tmp_path):
    info = results_heatmap(_cells(), tmp_path / "heat")
    assert info and (tmp_path / "heat.pdf").exists()


def test_empty_cells_return_none(tmp_path):
    assert faithfulness_correctness_joint({}, tmp_path / "e") is None
    assert results_heatmap({}, tmp_path / "e2") is None
