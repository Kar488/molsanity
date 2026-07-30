"""GINE backbone for graph classification/regression (PyG).

GINE (Hu et al. 2020) extends GIN with edge features. We keep a single head and
a configurable width/depth so the same module serves every dataset. The forward
signature accepts a continuous ``node_mask`` multiplier on the input node
features so Integrated Gradients (Captum) can attribute w.r.t. node inputs.
"""
from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import nn
from torch_geometric.nn import GINEConv, global_add_pool, global_mean_pool


def cast_inputs(x, edge_attr):
    """Coerce node/edge features to float once at each forward entry.

    Datasets ship features as int (MoleculeNet one-hot codes) or float (MUTAG);
    the linear encoders need float. Shared by every backbone's forward so a new
    backbone cannot forget the cast.
    """
    x = x.float()
    if edge_attr is not None:
        edge_attr = edge_attr.float()
    return x, edge_attr


def ensure_edge_attr(x, edge_index, edge_attr, edge_dim: int):
    """Materialise a zero edge-feature tensor when the dataset has none.

    Some graph datasets (BA-2Motifs, and synthetic generators in general) carry
    no edge features, but the edge-conditioned convolutions used here require a
    tensor. Passing ``None`` through reaches ``Linear(None)`` and raises. Shared
    by every backbone's forward so a new backbone cannot forget it.
    """
    if edge_attr is not None:
        return edge_attr
    return torch.zeros(edge_index.size(1), edge_dim,
                       device=x.device, dtype=x.dtype)


class GINE(nn.Module):
    def __init__(
        self,
        in_channels: int,
        edge_dim: int,
        hidden_channels: int = 64,
        num_layers: int = 3,
        out_channels: int = 2,
        dropout: float = 0.5,
        pool: str = "mean",
        task: str = "graph-classification",
    ):
        super().__init__()
        self.task = task
        self.dropout = dropout
        self.pool = global_mean_pool if pool == "mean" else global_add_pool

        self.edge_dim = edge_dim
        self.node_encoder = nn.Linear(in_channels, hidden_channels)
        self.edge_encoder = nn.Linear(edge_dim, hidden_channels)

        self.convs = nn.ModuleList()
        self.bns = nn.ModuleList()
        for _ in range(num_layers):
            mlp = nn.Sequential(
                nn.Linear(hidden_channels, hidden_channels),
                nn.ReLU(),
                nn.Linear(hidden_channels, hidden_channels),
            )
            self.convs.append(GINEConv(mlp, edge_dim=hidden_channels, train_eps=True))
            self.bns.append(nn.BatchNorm1d(hidden_channels))

        self.head = nn.Sequential(
            nn.Linear(hidden_channels, hidden_channels),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_channels, out_channels),
        )

    def forward(self, x, edge_index, edge_attr, batch, node_mask=None):
        x, edge_attr = cast_inputs(x, edge_attr)
        if node_mask is not None:
            # Broadcast a per-node scalar (or per-feature) multiplier onto inputs.
            x = x * node_mask
        h = self.node_encoder(x)
        e = self.edge_encoder(ensure_edge_attr(x, edge_index, edge_attr,
                                               self.edge_dim))
        for conv, bn in zip(self.convs, self.bns):
            h = conv(h, edge_index, e)
            h = bn(h)
            h = F.relu(h)
            h = F.dropout(h, p=self.dropout, training=self.training)
        hg = self.pool(h, batch)
        return self.head(hg)

    @torch.no_grad()
    def embed(self, x, edge_index, edge_attr, batch):
        x, edge_attr = cast_inputs(x, edge_attr)
        h = self.node_encoder(x)
        e = self.edge_encoder(ensure_edge_attr(x, edge_index, edge_attr,
                                               self.edge_dim))
        for conv, bn in zip(self.convs, self.bns):
            h = F.relu(bn(conv(h, edge_index, e)))
        return self.pool(h, batch)
