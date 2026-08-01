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


def test_every_generator_dig_draws_from_is_seeded_per_molecule():
    """The reproducibility defect that hid behind torch.manual_seed.

    ``dig/xgraph/method/shapley.py`` estimates the Shapley value with
    ``np.random.permutation`` -- the *global* NumPy generator, which
    ``torch.manual_seed`` does not reset. A molecule's attribution therefore
    depended on how many molecules had been attributed before it, so a resumed
    run, or one that skipped a cached cell, could return a different subgraph
    for the same input. That is a defect in the serial path, not merely an
    obstacle to parallelising it.
    """
    import numpy as np
    import random as _random

    g, attr = _fixture()
    g.graph_id = 7

    # Disturb every global generator between the two calls. A correctly seeded
    # attributor is indifferent to all of it.
    first = attr.attribute(g).node_attr.copy()
    np.random.seed(12345)
    np.random.permutation(50)
    _random.seed(999)
    _random.random()
    torch.manual_seed(4242)
    torch.rand(10)
    second = attr.attribute(g).node_attr.copy()

    np.testing.assert_array_equal(first, second)


def test_the_seed_follows_the_molecule_not_the_call_order():
    """Two different molecules must not collide, and the same molecule must
    give the same answer wherever it appears in the sequence."""
    import numpy as np

    from molsanity.data.synthetic import generate_synth_motifs

    g, attr = _fixture()
    others = generate_synth_motifs(num_graphs=4, num_nodes=12, seed=0)
    a = others[0]; a.graph_id = 0
    b = others[1]; b.graph_id = 1

    alone = attr.attribute(a).node_attr.copy()
    attr.attribute(b)                      # a different molecule in between
    after = attr.attribute(a).node_attr.copy()
    np.testing.assert_array_equal(alone, after)
