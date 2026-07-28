"""Integrated Gradients attributor, wrapping Captum via PyG's CaptumExplainer.

We do NOT reimplement IG. This adapter drives ``torch_geometric.explain.Explainer``
with the ``CaptumExplainer('IntegratedGradients')`` algorithm and repackages the
resulting node/edge masks into MolSanity's common :class:`Attribution` schema.
"""
from __future__ import annotations

import numpy as np
import torch

from ..utils import get_logger
from .base import Attribution

log = get_logger()


class IntegratedGradientsAttributor:
    method = "IntegratedGradients"

    def __init__(self, model, task: str = "graph-classification", ig_steps: int = 25):
        self.model = model
        self.task = task
        self.ig_steps = ig_steps
        self._explainer = self._build_explainer()

    def _build_explainer(self):
        from torch_geometric.explain import CaptumExplainer, Explainer

        mode = "multiclass_classification" if self.task == "graph-classification" else "regression"
        return Explainer(
            model=_ExplainerWrapper(self.model),
            algorithm=CaptumExplainer("IntegratedGradients", n_steps=self.ig_steps),
            explanation_type="model",
            node_mask_type="attributes",
            edge_mask_type="object",
            model_config=dict(mode=mode, task_level="graph", return_type="raw"),
        )

    def attribute(self, data, target: int | None = None) -> Attribution:
        self.model.eval()  # deterministic: no dropout during attribution
        device = next(self.model.parameters()).device
        data = data.to(device)
        model_out = self.model(
            data.x, data.edge_index, data.edge_attr,
            torch.zeros(data.num_nodes, dtype=torch.long, device=device),
        )
        pred = int(model_out.argmax(dim=1)) if self.task == "graph-classification" else 0
        tgt = target if target is not None else pred

        explanation = self._explainer(
            x=data.x,
            edge_index=data.edge_index,
            target=torch.tensor([tgt], device=device),
            edge_attr=data.edge_attr,
            batch=torch.zeros(data.num_nodes, dtype=torch.long, device=device),
        )

        node_mask = explanation.get("node_mask")
        if node_mask is not None:
            node_attr = node_mask.detach().abs().cpu().numpy()
            if node_attr.ndim > 1:
                node_attr = node_attr.sum(axis=1)
        else:
            node_attr = np.zeros(data.num_nodes)

        edge_mask = explanation.get("edge_mask")
        edge_attr = (
            edge_mask.detach().abs().cpu().numpy() if edge_mask is not None else None
        )

        return Attribution(
            graph_id=int(getattr(data, "graph_id", -1)),
            node_attr=node_attr.astype(np.float64),
            edge_attr=edge_attr.astype(np.float64) if edge_attr is not None else None,
            method=self.method,
            target=tgt,
            meta={"pred": pred, "ig_steps": self.ig_steps},
        )


class _ExplainerWrapper(torch.nn.Module):
    """Adapts GINE.forward(x, edge_index, edge_attr, batch) to the (x, edge_index,
    **kwargs) signature PyG's Explainer expects."""

    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, x, edge_index, edge_attr=None, batch=None, **kwargs):
        if batch is None:
            batch = torch.zeros(x.size(0), dtype=torch.long, device=x.device)
        return self.model(x, edge_index, edge_attr, batch)
