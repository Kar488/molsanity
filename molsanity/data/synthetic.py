"""Synthetic Tier-1 dataset with EXACT ground-truth motif masks.

BA-2Motifs' canonical download is unreachable in some environments (HTTP 403),
so we generate an equivalent offline via PyG's ``ExplainerDataset``: a
Barabasi-Albert base graph with one injected motif (a 5-node *house* or *cycle*).
The graph-level label is the motif type; the exact node ground-truth mask is the
set of injected-motif nodes. This validates the audit itself against real
ground truth (unlike MUTAG's chemically-motivated *proxy*).

Node features are structural (degree + constant) so a GNN must use topology.
Fully deterministic given the seed.
"""
from __future__ import annotations

import torch

from ..utils import get_logger

log = get_logger()


def _motif_dataset(motif, num_graphs, num_nodes, seed):
    from torch_geometric.datasets import ExplainerDataset
    from torch_geometric.datasets.graph_generator import BAGraph

    from ..utils import set_global_seed

    # BA generation uses numpy/python/torch RNG; seed all for reproducibility.
    set_global_seed(seed)
    return ExplainerDataset(
        graph_generator=BAGraph(num_nodes=num_nodes, num_edges=1),
        motif_generator=motif,
        num_motifs=1,
        num_graphs=num_graphs,
    )


def _to_classification_graph(expl, label: int):
    """Convert an ExplainerDataset Explanation (per-node motif labels) into a
    graph-classification Data with structural features + exact node GT mask."""
    from torch_geometric.data import Data
    from torch_geometric.utils import degree

    n = int(expl.num_nodes)
    deg = degree(expl.edge_index[0], num_nodes=n).float()
    x = torch.stack([deg, torch.ones(n)], dim=1)  # [degree, 1]
    edge_attr = torch.ones(expl.edge_index.size(1), 1)
    node_gt = (expl.node_mask.view(-1) > 0).float() if expl.node_mask is not None else torch.zeros(n)

    g = Data(x=x, edge_index=expl.edge_index, edge_attr=edge_attr,
             y=torch.tensor([label], dtype=torch.long))
    g.node_gt = node_gt
    return g


def generate_synth_motifs(num_graphs: int = 200, num_nodes: int = 25, seed: int = 0):
    """Balanced 2-class dataset: house (label 0) vs cycle (label 1) motif."""
    from torch_geometric.datasets.motif_generator import CycleMotif, HouseMotif

    half = num_graphs // 2
    house = _motif_dataset(HouseMotif(), half, num_nodes, seed)
    cycle = _motif_dataset(CycleMotif(5), num_graphs - half, num_nodes, seed + 1)

    graphs = []
    for expl in house:
        graphs.append(_to_classification_graph(expl, label=0))
    for expl in cycle:
        graphs.append(_to_classification_graph(expl, label=1))

    # Deterministic interleave so splits see both classes.
    ordered = []
    for i in range(max(len(house), len(cycle))):
        if i < half:
            ordered.append(graphs[i])
        if i < num_graphs - half:
            ordered.append(graphs[half + i])
    log.info("Generated SynthMotifs: %d graphs (house/cycle), exact node GT", len(ordered))
    return ordered
