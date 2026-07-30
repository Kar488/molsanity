"""BA-2Motifs node ground truth: recovered, and verified before it is used.

PyG's ``BA2MotifDataset`` exposes no per-node labels, so the motif has to be
recovered from the dataset's node ordering. These tests pin the two properties
that make that safe:

1. On graphs built exactly the way BA-2Motifs is built (a Barabasi-Albert base
   with one house or five-cycle appended), the recovered mask equals the
   generator's own ``node_mask``. PyG's ``ExplainerDataset`` produces that
   ground truth independently, so this is a real cross-check rather than a
   restatement of the implementation.
2. When the trailing nodes are *not* a motif, recovery returns None. The cell
   then reports no ground truth, which is what it did before this change. A
   loader that reorders nodes therefore degrades to the old behaviour instead
   of scoring attributions against a fabricated mask.
"""
from __future__ import annotations

import numpy as np
import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("torch_geometric")

from molsanity.data.groundtruth import (  # noqa: E402
    ba2motifs_node_mask,
    ba2motifs_trailing_motif_mask,
)


def _ba2motifs_like(motif, num_graphs=8, num_nodes=25, seed=0):
    """Graphs built the way the BA-2Motifs release was built."""
    from torch_geometric.datasets import ExplainerDataset
    from torch_geometric.datasets.graph_generator import BAGraph

    torch.manual_seed(seed)
    np.random.seed(seed)
    return ExplainerDataset(
        graph_generator=BAGraph(num_nodes=num_nodes, num_edges=1),
        motif_generator=motif,
        num_motifs=1,
        num_graphs=num_graphs,
    )


def _features(g):
    """ExplainerDataset leaves x unset; BA2MotifDataset ships constant features."""
    n = int(g.num_nodes)
    return g.x if g.x is not None else torch.ones(n, 10)


def _strip_node_mask(g):
    """A BA2MotifDataset graph as PyG actually hands it over: no node labels."""
    from torch_geometric.data import Data

    return Data(x=_features(g), edge_index=g.edge_index,
                y=torch.tensor([0]), num_nodes=int(g.num_nodes))


@pytest.mark.parametrize("motif_name", ["house", "cycle"])
def test_recovered_mask_matches_the_generator(motif_name):
    from torch_geometric.datasets.motif_generator import CycleMotif, HouseMotif

    motif = HouseMotif() if motif_name == "house" else CycleMotif(5)
    ds = _ba2motifs_like(motif)
    for g in ds:
        truth = (g.node_mask.view(-1).numpy() > 0).astype(np.float32)
        got = ba2motifs_node_mask(_strip_node_mask(g))
        assert got is not None, "recovery returned None on a well-formed graph"
        np.testing.assert_array_equal(got, truth)
        assert got.sum() == 5


@pytest.mark.parametrize("motif_name", ["house", "cycle"])
def test_motif_kind_is_identified(motif_name):
    from torch_geometric.datasets.motif_generator import CycleMotif, HouseMotif

    motif = HouseMotif() if motif_name == "house" else CycleMotif(5)
    g = _ba2motifs_like(motif, num_graphs=1)[0]
    found = ba2motifs_trailing_motif_mask(_strip_node_mask(g))
    assert found is not None
    assert found[1] == motif_name


def test_returns_none_when_the_trailing_nodes_are_not_a_motif():
    """A reordered graph must degrade to 'no ground truth', never to a guess."""
    from torch_geometric.data import Data
    from torch_geometric.datasets.motif_generator import HouseMotif

    g = _ba2motifs_like(HouseMotif(), num_graphs=1)[0]
    n = int(g.num_nodes)
    # Reverse the node order: the motif now sits at the *front*, so the
    # positional convention no longer holds and validation must reject it.
    perm = torch.arange(n - 1, -1, -1)
    inv = torch.empty(n, dtype=torch.long)
    inv[perm] = torch.arange(n)
    reordered = Data(x=_features(g)[perm], edge_index=inv[g.edge_index],
                     y=torch.tensor([0]), num_nodes=n)
    assert ba2motifs_node_mask(reordered) is None


def test_explicit_node_labels_take_precedence():
    """If a loader ever does supply labels, they win over the convention."""
    from torch_geometric.datasets.motif_generator import HouseMotif

    g = _ba2motifs_like(HouseMotif(), num_graphs=1)[0]
    truth = (g.node_mask.view(-1).numpy() > 0).astype(np.float32)
    np.testing.assert_array_equal(ba2motifs_node_mask(g), truth)


def test_graph_smaller_than_the_motif_is_rejected():
    from torch_geometric.data import Data

    tiny = Data(x=torch.zeros(4, 3),
                edge_index=torch.tensor([[0, 1, 1, 2], [1, 0, 2, 1]]),
                y=torch.tensor([0]))
    assert ba2motifs_node_mask(tiny) is None
