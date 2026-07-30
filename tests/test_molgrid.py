"""Molecule/graph attribution-grid rendering tests (no training)."""
import numpy as np
import pytest

pytest.importorskip("matplotlib")
pytest.importorskip("rdkit")
pytest.importorskip("PIL")

from molsanity.viz.molgrid import attribution_grid


def test_molecule_grid_renders(tmp_path):
    from rdkit import Chem

    mol = Chem.MolFromSmiles("O=[N+]([O-])c1ccccc1")  # nitrobenzene
    n = mol.GetNumAtoms()
    rng = np.random.default_rng(0)
    methods = ["IntegratedGradients", "Saliency"]
    attrs = {m: [rng.random(n)] for m in methods}
    gt = [np.array([1, 1, 1] + [0] * (n - 3), dtype=float)]  # nitro group atoms
    info = attribution_grid([mol], attrs, gt, methods, ["mol 0"], tmp_path / "grid",
                            title="test")
    assert info and (tmp_path / "grid.pdf").exists() and (tmp_path / "grid.svg").exists()


def test_graph_grid_renders(tmp_path):
    import torch
    from torch_geometric.data import Data

    ei = torch.tensor([[0, 1, 1, 2, 2, 3, 3, 4], [1, 0, 2, 1, 3, 2, 4, 3]])
    g = Data(x=torch.ones(5, 2), edge_index=ei)
    g.num_nodes = 5
    methods = ["IntegratedGradients", "GNNExplainer"]
    attrs = {m: [np.array([0.1, 0.2, 0.9, 0.8, 0.1])] for m in methods}
    gt = [np.array([0, 0, 1, 1, 0], dtype=float)]
    info = attribution_grid([None], attrs, gt, methods, ["graph 0"], tmp_path / "ggrid",
                            graphs=[g], title="graph test")
    assert info and (tmp_path / "ggrid.svg").exists()
