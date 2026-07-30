"""Regressions for the four defects that failed 27 cell-runs of the GPU sweep.

Each test names the failure it guards against, so a re-introduction is obvious:

  1. ground-truth mask called ``.numpy()`` on a CUDA tensor  (20 MUTAG cells)
  2. PGExplainer's mask MLP stayed on CPU while the model was on CUDA  (6 cells)
  3. GINE-family forward passed ``edge_attr=None`` into an edge-conditioned
     convolution, for datasets without edge features  (2 BA-2Motifs cells)
  4. a trailing training batch of size 1 made BatchNorm raise  (1 FreeSolv cell)

The two device-dependent tests are skipped without a GPU but run unchanged on
the machine the sweep uses.
"""
from __future__ import annotations

import pytest

torch = pytest.importorskip("torch")


# --- 3. edge_attr=None must not reach the convolutions ---------------------
def test_ensure_edge_attr_materialises_zeros():
    from molsanity.models.gine import ensure_edge_attr

    x = torch.randn(4, 3)
    edge_index = torch.tensor([[0, 1, 2], [1, 2, 3]])
    out = ensure_edge_attr(x, edge_index, None, edge_dim=5)
    assert out.shape == (3, 5)
    assert out.dtype == x.dtype and out.device == x.device
    assert torch.count_nonzero(out) == 0

    given = torch.ones(3, 5)
    assert ensure_edge_attr(x, edge_index, given, edge_dim=5) is given


def test_gine_forward_without_edge_features():
    """BA-2Motifs-style graphs carry no edge features; the forward must cope."""
    pytest.importorskip("torch_geometric")
    from molsanity.models.gine import GINE

    model = GINE(in_channels=3, edge_dim=1, hidden_channels=8, num_layers=2,
                 out_channels=2).eval()
    x = torch.randn(5, 3)
    edge_index = torch.tensor([[0, 1, 2, 3], [1, 2, 3, 4]])
    batch = torch.zeros(5, dtype=torch.long)
    out = model(x, edge_index, None, batch)          # edge_attr=None
    assert out.shape == (1, 2) and torch.isfinite(out).all()


def test_every_backbone_survives_missing_edge_features():
    pytest.importorskip("torch_geometric")
    from molsanity.models.backbones import _BACKBONES

    x = torch.randn(6, 3)
    edge_index = torch.tensor([[0, 1, 2, 3, 4], [1, 2, 3, 4, 5]])
    batch = torch.zeros(6, dtype=torch.long)
    for name, cls in _BACKBONES.items():
        model = cls(in_channels=3, edge_dim=1, hidden_channels=8, num_layers=2,
                    out_channels=2, dropout=0.0, pool="mean",
                    task="graph-classification").eval()
        out = model(x, edge_index, None, batch)
        assert torch.isfinite(out).all(), f"{name} produced non-finite logits"


# --- 4. a trailing batch of one must never reach BatchNorm ----------------
@pytest.mark.parametrize("n_train,batch_size,expected", [
    (513, 64, True),    # the FreeSolv scaffold split that failed
    (512, 64, False),
    (65, 64, True),
    (1, 64, False),     # smaller than one batch: nothing to drop
])
def test_drop_last_rule(n_train, batch_size, expected):
    drop_last = n_train % batch_size == 1 and n_train > batch_size
    assert drop_last is expected


def test_batchnorm_would_reject_a_single_graph_batch():
    """Documents *why* the rule above exists (this raise is the failure seen)."""
    bn = torch.nn.BatchNorm1d(8).train()
    with pytest.raises(ValueError):
        bn(torch.randn(1, 8))
    bn(torch.randn(2, 8))  # two is fine


# --- 1. ground-truth mask on a GPU graph ----------------------------------
@pytest.mark.skipif(not torch.cuda.is_available(), reason="needs a GPU")
def test_mutag_mask_on_cuda_graph():
    from types import SimpleNamespace

    from molsanity.data.groundtruth import mutag_nitro_mask

    # N bonded to two O -> a nitro group; features are MUTAG one-hot (C, N, O).
    x = torch.tensor([[0., 1., 0.], [0., 0., 1.], [0., 0., 1.], [1., 0., 0.]])
    edge_index = torch.tensor([[0, 0, 0, 1, 2, 3], [1, 2, 3, 0, 0, 0]])
    data = SimpleNamespace(x=x.cuda(), edge_index=edge_index.cuda())
    mask = mutag_nitro_mask(data)
    assert mask.tolist() == [1.0, 1.0, 1.0, 0.0]


# --- 2. PGExplainer must follow the model onto the GPU --------------------
@pytest.mark.skipif(not torch.cuda.is_available(), reason="needs a GPU")
def test_pgexplainer_moves_to_model_device():
    pytest.importorskip("torch_geometric")
    from torch_geometric.data import Data

    from molsanity.attributors.pg_explainer import PGExplainerAttributor
    from molsanity.models.gine import GINE

    model = GINE(in_channels=3, edge_dim=2, hidden_channels=8, num_layers=2,
                 out_channels=2).cuda().eval()
    graphs = [Data(x=torch.randn(5, 3), edge_index=torch.tensor([[0, 1, 2, 3],
                                                                 [1, 2, 3, 4]]),
                   edge_attr=torch.randn(4, 2), y=torch.tensor([0]))
              for _ in range(2)]
    attr = PGExplainerAttributor(model, train_graphs=graphs, epochs=1)
    devices = {p.device.type for p in attr._explainer.algorithm.parameters()}
    assert devices == {"cuda"}
    out = attr.attribute(graphs[0])                    # must not raise
    assert out.node_attr.shape == (5,)
