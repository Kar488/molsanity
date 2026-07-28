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
        x = x.float()
        if edge_attr is not None:
            edge_attr = edge_attr.float()
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
        x = x.float()
        if edge_attr is not None:
            edge_attr = edge_attr.float()
        h = self.node_encoder(x)
        e = self.edge_encoder(edge_attr) if edge_attr is not None else None
        for conv, bn in zip(self.convs, self.bns):
            h = F.relu(bn(conv(h, edge_index, e)))
        return self.pool(h, batch)


def build_model(sample_graph, cfg: dict) -> GINE:
    """Construct a GINE from a sample graph and a model config dict."""
    in_channels = sample_graph.x.size(1)
    edge_dim = sample_graph.edge_attr.size(1) if sample_graph.edge_attr is not None else 1
    task = cfg.get("task", "graph-classification")
    out_channels = cfg.get("out_channels", 2 if task == "graph-classification" else 1)
    return GINE(
        in_channels=in_channels,
        edge_dim=edge_dim,
        hidden_channels=cfg.get("hidden_channels", 64),
        num_layers=cfg.get("num_layers", 3),
        out_channels=out_channels,
        dropout=cfg.get("dropout", 0.5),
        pool=cfg.get("pool", "mean"),
        task=task,
    )
