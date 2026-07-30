"""Registry + regime/split tests. Require the torch/rdkit stack (skip if absent)."""
import numpy as np
import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("torch_geometric")
pytest.importorskip("rdkit")

from molsanity import data
from molsanity.attributors import ATTRIBUTORS, build_attributor
from molsanity.audit.regime import assign_regime, confidence_from_logits
from molsanity.models import build_backbone


@pytest.fixture(scope="module")
def mutag():
    return data.load_dataset("MUTAG")


@pytest.mark.parametrize("backbone", ["GINE", "GCN", "GAT", "MPNN", "AttentiveFP"])
def test_backbone_forward_shapes(mutag, backbone):
    g = mutag.dataset[0]
    model = build_backbone(backbone, g, {"hidden_channels": 16, "num_layers": 2, "out_channels": 2})
    model.eval()
    batch = torch.zeros(g.num_nodes, dtype=torch.long)
    out = model(g.x, g.edge_index, g.edge_attr, batch)
    assert out.shape == (1, 2)
    # node_mask path (used by IG/occlusion) must also work
    nm = torch.ones(g.num_nodes, 1)
    out2 = model(g.x, g.edge_index, g.edge_attr, batch, node_mask=nm)
    assert out2.shape == (1, 2)


@pytest.mark.parametrize("method", ["IntegratedGradients", "Saliency", "GNNExplainer"])
def test_attributor_runs(mutag, method):
    g = mutag.dataset[0]
    model = build_backbone("GINE", g, {"hidden_channels": 16, "num_layers": 2, "out_channels": 2})
    model.eval()
    attr = build_attributor(method, model, ig_steps=5, epochs=10)
    a = attr.attribute(g)
    assert a.node_attr.shape == (g.num_nodes,)
    assert np.all(np.isfinite(a.node_attr))


def test_attributor_registry_and_unknown(mutag):
    assert "IntegratedGradients" in ATTRIBUTORS and "GNNExplainer" in ATTRIBUTORS
    g = mutag.dataset[0]
    model = build_backbone("GINE", g, {"hidden_channels": 8, "num_layers": 1, "out_channels": 2})
    with pytest.raises(KeyError):
        build_attributor("NoSuchMethod", model)


def test_regime_assignment():
    assert assign_regime(0.95, 1, tau=0.8) == "confident_correct"
    assert assign_regime(0.95, 0, tau=0.8) == "confident_error"
    assert assign_regime(0.6, 1, tau=0.8) == "borderline"
    pred, conf = confidence_from_logits(np.array([2.0, 0.0]), temperature=1.0)
    assert pred == 0 and 0.5 < conf < 1.0


def test_scaffold_split_no_empty_partition(mutag):
    s = data.make_split(mutag.dataset, kind="scaffold")
    assert len(s.train) > 0 and len(s.val) > 0 and len(s.test) > 0
