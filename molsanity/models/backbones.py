"""GNN backbones behind a common interface (model-agnosticism).

Every backbone exposes the same forward signature so the attributor and
occlusion audit are backbone-agnostic::

    forward(x, edge_index, edge_attr, batch, node_mask=None) -> logits

``node_mask`` is a per-node scalar multiplier on the input features, used by
Integrated Gradients (Captum) and the occlusion sweeps. Backbones: GINE, GCN,
GAT, MPNN, AttentiveFP. Same head, same pooling, same calibration downstream.
"""
from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import nn
from torch_geometric.nn import (
    AttentiveFP,
    GATConv,
    GCNConv,
    NNConv,
    global_add_pool,
    global_mean_pool,
)

from .gine import GINE, cast_inputs  # canonical GINE + shared input cast


def _pool_fn(pool: str):
    return global_mean_pool if pool == "mean" else global_add_pool


class _BaseGNN(nn.Module):
    """Shared plumbing: node/edge encoders, node_mask, pooling, MLP head."""

    def __init__(self, in_channels, edge_dim, hidden_channels, num_layers,
                 out_channels, dropout, pool, task):
        super().__init__()
        self.task = task
        self.dropout = dropout
        self.pool = _pool_fn(pool)
        self.node_encoder = nn.Linear(in_channels, hidden_channels)
        self.edge_encoder = nn.Linear(edge_dim, hidden_channels)
        self.convs = nn.ModuleList()
        self.bns = nn.ModuleList()
        self._build_convs(hidden_channels, num_layers)
        self.head = nn.Sequential(
            nn.Linear(hidden_channels, hidden_channels), nn.ReLU(),
            nn.Dropout(dropout), nn.Linear(hidden_channels, out_channels),
        )

    def _build_convs(self, hidden, num_layers):  # pragma: no cover - overridden
        raise NotImplementedError

    def _conv_forward(self, conv, h, edge_index, e):  # pragma: no cover
        raise NotImplementedError

    def forward(self, x, edge_index, edge_attr, batch, node_mask=None):
        x, edge_attr = cast_inputs(x, edge_attr)
        if node_mask is not None:
            x = x * node_mask
        h = self.node_encoder(x)
        e = self.edge_encoder(edge_attr) if edge_attr is not None else None
        for conv, bn in zip(self.convs, self.bns):
            h = self._conv_forward(conv, h, edge_index, e)
            h = F.relu(bn(h))
            h = F.dropout(h, p=self.dropout, training=self.training)
        return self.head(self.pool(h, batch))


class GCN(_BaseGNN):
    """GCN — ignores edge features (uses graph structure only)."""

    def _build_convs(self, hidden, num_layers):
        for _ in range(num_layers):
            self.convs.append(GCNConv(hidden, hidden, add_self_loops=True))
            self.bns.append(nn.BatchNorm1d(hidden))

    def _conv_forward(self, conv, h, edge_index, e):
        return conv(h, edge_index)


class GAT(_BaseGNN):
    """GAT with edge features (multi-head, concatenated then projected)."""

    def __init__(self, *args, heads: int = 4, **kwargs):
        self._heads = heads
        super().__init__(*args, **kwargs)

    def _build_convs(self, hidden, num_layers):
        self._edge_dim = hidden
        for _ in range(num_layers):
            self.convs.append(
                GATConv(hidden, hidden // self._heads, heads=self._heads,
                        edge_dim=hidden, add_self_loops=True)
            )
            self.bns.append(nn.BatchNorm1d(hidden))

    def _conv_forward(self, conv, h, edge_index, e):
        return conv(h, edge_index, edge_attr=e)


class MPNN(_BaseGNN):
    """MPNN via edge-conditioned NNConv (Gilmer et al. 2017 style)."""

    def _build_convs(self, hidden, num_layers):
        for _ in range(num_layers):
            edge_nn = nn.Sequential(
                nn.Linear(hidden, hidden), nn.ReLU(), nn.Linear(hidden, hidden * hidden)
            )
            self.convs.append(NNConv(hidden, hidden, edge_nn, aggr="mean"))
            self.bns.append(nn.BatchNorm1d(hidden))

    def _conv_forward(self, conv, h, edge_index, e):
        if e is None:
            e = torch.zeros(edge_index.size(1), self.node_encoder.out_features, device=h.device)
        return conv(h, edge_index, e)


class AttentiveFPBackbone(nn.Module):
    """Wrap PyG's canonical AttentiveFP into the common forward signature."""

    def __init__(self, in_channels, edge_dim, hidden_channels, num_layers,
                 out_channels, dropout, pool, task):
        super().__init__()
        self.task = task
        self.dropout = dropout
        self.edge_dim = edge_dim
        self.model = AttentiveFP(
            in_channels=in_channels, hidden_channels=hidden_channels,
            out_channels=out_channels, edge_dim=edge_dim,
            num_layers=num_layers, num_timesteps=2, dropout=dropout,
        )

    def forward(self, x, edge_index, edge_attr, batch, node_mask=None):
        x, edge_attr = cast_inputs(x, edge_attr)
        if node_mask is not None:
            x = x * node_mask
        if edge_attr is None:
            edge_attr = torch.zeros(edge_index.size(1), self.edge_dim, device=x.device)
        return self.model(x, edge_index, edge_attr, batch)


_BACKBONES = {
    "GINE": GINE,
    "GCN": GCN,
    "GAT": GAT,
    "MPNN": MPNN,
    "AttentiveFP": AttentiveFPBackbone,
}


def build_backbone(name: str, sample_graph, cfg: dict):
    if name not in _BACKBONES:
        raise KeyError(f"Unknown backbone '{name}'. Known: {sorted(_BACKBONES)}")
    in_channels = sample_graph.x.size(1)
    edge_dim = sample_graph.edge_attr.size(1) if sample_graph.edge_attr is not None else 1
    task = cfg.get("task", "graph-classification")
    out_channels = cfg.get("out_channels", 2 if task == "graph-classification" else 1)
    common = dict(
        in_channels=in_channels, edge_dim=edge_dim,
        hidden_channels=cfg.get("hidden_channels", 64),
        num_layers=cfg.get("num_layers", 3), out_channels=out_channels,
        dropout=cfg.get("dropout", 0.5), pool=cfg.get("pool", "mean"), task=task,
    )
    return _BACKBONES[name](**common)
