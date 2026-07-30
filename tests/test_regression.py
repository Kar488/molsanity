"""Regression path tests: training branch, audit in output space, reporting split."""
import numpy as np
import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("torch_geometric")
pytest.importorskip("rdkit")

from torch_geometric.data import Data

from molsanity.data.splits import Split
from molsanity.models import train_model
from molsanity.reporting import _parse_existing_rows, results_row, update_results_md


def _synth_regression_dataset(n=40, seed=0):
    """Tiny molecule-like graphs (a triangle) with a continuous target.

    SMILES is attached so the audit's motif decomposition has a real molecule;
    the target is a noisy function of a node feature so training can learn."""
    rng = np.random.default_rng(seed)
    graphs = []
    for i in range(n):
        x = torch.tensor(rng.random((3, 4)), dtype=torch.float)
        ei = torch.tensor([[0, 1, 1, 2, 2, 0], [1, 0, 2, 1, 0, 2]], dtype=torch.long)
        ea = torch.ones((6, 2), dtype=torch.float)
        y = torch.tensor([[float(x[:, 0].mean() * 3.0 + rng.normal(0, 0.05))]])
        g = Data(x=x, edge_index=ei, edge_attr=ea, y=y)
        g.smiles = "C1CC1"  # cyclopropane: gives a ring motif
        graphs.append(g)
    return graphs


def test_regression_training_and_audit():
    ds = _synth_regression_dataset(48)
    split = Split(train=list(range(0, 36)), val=list(range(36, 42)),
                  test=list(range(42, 48)), kind="random")
    model, res = train_model(
        ds, split,
        model_cfg={"hidden_channels": 16, "num_layers": 2, "task": "graph-regression",
                   "out_channels": 1},
        train_cfg={"epochs": 40, "lr": 0.01},
        ckpt_dir="artifacts/_test_reg", seed=0, backbone="GINE",
    )
    assert res.task == "graph-regression"
    assert np.isfinite(res.test_rmse) and res.test_rmse >= 0
    assert np.isnan(res.test_acc)  # classification metric not set for regression

    from molsanity.attributors import build_attributor
    from molsanity.audit import audit_molecule
    from molsanity.audit.motifs import decompose

    attr = build_attributor("IntegratedGradients", model, task="graph-regression", ig_steps=5)
    g = ds[split.test[0]]
    g.graph_id = split.test[0]
    rec = audit_molecule(model, g, attr.attribute(g), "SYNTH",
                         decomp=decompose(g), task="graph-regression")
    assert rec.regime == "regression"
    assert np.isnan(rec.gt_auroc)  # no ground truth for regression
    assert np.isfinite(rec.motif_top1_share)


def test_reporting_splits_tasks(tmp_path):
    path = tmp_path / "RESULTS.md"
    agg = {"n_molecules": 10, "accuracy": float("nan"),
           "motif_top1_share": {"mean": 0.8}, "occ_spearman": {"mean": 0.1},
           "occ_top1_agreement": {"mean": 0.5}, "fidelity_plus": {"mean": -1.0},
           "fidelity_minus": {"mean": 0.2}, "sparsity": {"mean": 0.7},
           "gt_auroc": {"mean": float("nan")}, "gt_auprc": {"mean": float("nan")}}
    cls = results_row({"dataset": "BBBP", "backbone": "GINE", "attributor": "IntegratedGradients"},
                      {**agg, "accuracy": 0.8}, {"task": "graph-classification", "test_ece": 0.1}, "scaffold")
    reg = results_row({"dataset": "ESOL", "backbone": "GINE", "attributor": "IntegratedGradients"},
                      agg, {"task": "graph-regression", "test_rmse": 1.2, "test_mae": 0.9, "test_r2": 0.6}, "scaffold")
    update_results_md([cls, reg], path=path)
    text = path.read_text()
    assert "Classification audit matrix" in text and "Regression audit matrix" in text
    assert "1.200" in text  # regression RMSE rendered

    parsed = _parse_existing_rows(path)
    tasks = {k: r["task"] for k, r in parsed.items()}
    assert ("ESOL", "GINE", "IntegratedGradients", "scaffold") in parsed
    assert tasks[("ESOL", "GINE", "IntegratedGradients", "scaffold")] == "graph-regression"
    assert tasks[("BBBP", "GINE", "IntegratedGradients", "scaffold")] == "graph-classification"
