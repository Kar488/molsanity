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
        e = self.edge_encoder(edge_attr) if edge_attr is not None else None
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
        e = self.edge_encoder(edge_attr) if edge_attr is not None else None
        for conv, bn in zip(self.convs, self.bns):
            h = F.relu(bn(conv(h, edge_index, e)))
        return self.pool(h, batch)
