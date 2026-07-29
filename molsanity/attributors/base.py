"""Uniform attribution schema + shared explainer plumbing.

Every attributor returns node/edge attributions in this common form so the audit
and benchmark layers are attributor-agnostic. Motif-level attributions are
derived downstream from node attributions + an RDKit motif decomposition.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import torch


def minmax_normalise(node_attr: np.ndarray) -> np.ndarray:
    """Min-max normalise |attribution| into [0, 1]; all-equal maps to zeros.

    The single canonical normaliser used for GT AUROC, rendering, and the
    Attribution helper below, so the same convention is applied everywhere.
    """
    a = np.abs(np.asarray(node_attr, dtype=np.float64))
    rng = a.max() - a.min() if a.size else 0.0
    if rng <= 0:
        return np.zeros_like(a)
    return (a - a.min()) / rng


@dataclass
class Attribution:
    """Per-molecule attribution in a common schema."""

    graph_id: int
    node_attr: np.ndarray  # shape [num_nodes], non-negative importance
    edge_attr: np.ndarray | None = None  # shape [num_edges]
    method: str = ""
    target: int | None = None  # class explained
    meta: dict = field(default_factory=dict)

    def normalised_node_attr(self) -> np.ndarray:
        """Min-max normalised node attribution in [0, 1] (for GT AUROC etc.)."""
        return minmax_normalise(self.node_attr)


class _ExplainerWrapper(torch.nn.Module):
    """Adapt backbone.forward(x, edge_index, edge_attr, batch) to the
    (x, edge_index, **kwargs) signature PyG's Explainer expects."""

    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, x, edge_index, edge_attr=None, batch=None, **kwargs):
        if batch is None:
            batch = torch.zeros(x.size(0), dtype=torch.long, device=x.device)
        return self.model(x, edge_index, edge_attr, batch)


def _unpack_masks(explanation, num_nodes: int):
    """Repackage a PyG Explanation's node/edge masks into numpy arrays."""
    node_mask = explanation.get("node_mask")
    if node_mask is not None:
        node_attr = node_mask.detach().abs().cpu().numpy()
        if node_attr.ndim > 1:
            node_attr = node_attr.sum(axis=1)
    else:
        node_attr = np.zeros(num_nodes)
    edge_mask = explanation.get("edge_mask")
    edge_attr = edge_mask.detach().abs().cpu().numpy() if edge_mask is not None else None
    return node_attr.astype(np.float64), (
        edge_attr.astype(np.float64) if edge_attr is not None else None
    )


class BaseExplainerAttributor:
    """Shared attribution flow over a PyG ``Explainer``.

    Subclasses supply ``_build_explainer()`` and (optionally) ``_extra_meta()``;
    the eval/device/pred/target logic and schema packaging live here once.
    """

    method: str = ""

    def __init__(self, model, task: str = "graph-classification"):
        self.model = model
        self.task = task
        self._explainer = self._build_explainer()

    def _build_explainer(self):  # pragma: no cover - overridden
        raise NotImplementedError

    def _extra_meta(self) -> dict:
        return {}

    # Base seed for per-molecule attribution reproducibility. Stochastic
    # explainers (e.g. GNNExplainer's random mask init) must not depend on the
    # ambient RNG state — otherwise a fresh-train run and a checkpoint-reload run
    # would give different explanations. We reseed per molecule so an explanation
    # depends only on (molecule, method). Deterministic methods are unaffected.
    attribution_seed: int = 10_000

    def attribute(self, data, target: int | None = None) -> Attribution:
        self.model.eval()
        device = next(self.model.parameters()).device
        data = data.to(device)
        batch = torch.zeros(data.num_nodes, dtype=torch.long, device=device)
        with torch.no_grad():
            out = self.model(data.x, data.edge_index, data.edge_attr, batch)
        pred = int(out.argmax(dim=1)) if self.task == "graph-classification" else 0
        tgt = target if target is not None else pred

        gid = int(getattr(data, "graph_id", 0))
        torch.manual_seed(self.attribution_seed + (gid if gid >= 0 else 0))
        explanation = self._explainer(
            x=data.x, edge_index=data.edge_index,
            target=torch.tensor([tgt], device=device),
            edge_attr=data.edge_attr, batch=batch,
        )
        node_attr, edge_attr = _unpack_masks(explanation, data.num_nodes)
        meta = {"pred": pred, **self._extra_meta()}
        # PyG-native unfaithfulness (KL between full vs top-k masked prediction) —
        # a DIG/GraphFramEx-comparable faithfulness metric, captured inline.
        try:
            from torch_geometric.explain.metric import unfaithfulness

            meta["unfaithfulness"] = float(unfaithfulness(self._explainer, explanation))
        except Exception:
            pass
        return Attribution(
            graph_id=int(getattr(data, "graph_id", -1)),
            node_attr=node_attr, edge_attr=edge_attr,
            method=self.method, target=tgt, meta=meta,
        )
