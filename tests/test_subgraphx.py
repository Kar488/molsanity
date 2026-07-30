"""SubgraphX, wrapped from DIG, actually finds the planted motif.

SubgraphX is the one perturbation-family attributor in the sweep that searches
connected subgraphs rather than learning a soft mask, so without it every
perturbation-family conclusion rests on GNNExplainer alone. It needs DIG and
its compiled torch_sparse/torch_scatter extensions; where those are missing the
whole module is skipped rather than failing the suite, which mirrors how the
audit treats the cell.

The substantive test uses a synthetic graph whose motif is known exactly, so a
wrapper that returned an empty or arbitrary subgraph would fail rather than
silently produce an all-zero attribution.
"""
from __future__ import annotations

import numpy as np
import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("torch_geometric")
pytest.importorskip("dig", reason="DIG (dive-into-graphs) not installed")

from molsanity.attributors import build_attributor  # noqa: E402
from molsanity.attributors.subgraphx import _selected_nodes  # noqa: E402


def _fixture(num_nodes=12, seed=0):
    from molsanity.data.synthetic import generate_synth_motifs
    from molsanity.models import build_backbone

    g = generate_synth_motifs(num_graphs=4, num_nodes=num_nodes, seed=seed)[0]
    model = build_backbone("GINE", g, {"hidden_channels": 16, "num_layers": 2,
                                       "task": "graph-classification",
                                       "out_channels": 2})
    model.eval()
    attr = build_attributor("SubgraphX", model, task="graph-classification",
                            sgx_max_nodes=5, sgx_rollouts=3, seed=0)
    attr.edge_dim = g.edge_attr.size(1) if g.edge_attr is not None else 1
    return g, attr


def test_subgraphx_is_registered():
    from molsanity.attributors import ATTRIBUTORS

    assert "SubgraphX" in ATTRIBUTORS


def test_subgraphx_recovers_the_planted_motif():
    g, attr = _fixture()
    out = attr.attribute(g)

    assert not out.meta["empty_selection"], "search returned no subgraph"
    assert out.meta["n_selected"] > 0
    chosen = set(np.flatnonzero(out.node_attr).tolist())
    truth = set(np.flatnonzero(g.node_gt.numpy()).tolist())
    assert chosen == truth, f"selected {sorted(chosen)}, motif is {sorted(truth)}"


def test_attribution_shape_and_flags():
    g, attr = _fixture()
    out = attr.attribute(g)
    assert out.node_attr.shape == (int(g.num_nodes),)
    assert set(np.unique(out.node_attr)).issubset({0.0, 1.0}), (
        "SubgraphX returns a discrete subgraph, so scores must be 0/1")
    assert out.meta["hard_mask"] is True
    assert out.method == "SubgraphX"


def test_unrecognised_search_output_yields_no_selection():
    """A shape we do not understand must not become a confident empty mask."""
    assert _selected_nodes(None, 0, 5) == []
    assert _selected_nodes([], 0, 5) == []
    assert _selected_nodes([[]], 0, 5) == []
    assert _selected_nodes([[{"no_coalition": 1}]], 0, 5) == []


def test_selection_follows_digs_own_rule():
    """Highest reward among coalitions that fit; smallest coalition otherwise."""
    results = [
        {"coalition": [0, 1, 2, 3, 4, 5, 6], "P": 9.0},   # too big
        {"coalition": [1, 2], "P": 0.2},
        {"coalition": [3, 4, 5], "P": 0.9},               # best that fits
        {"coalition": [6, 7], "P": 0.4},
    ]
    assert _selected_nodes([results], 0, max_nodes=5) == [3, 4, 5]
