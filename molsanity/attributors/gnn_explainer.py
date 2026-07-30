"""GNNExplainer attributor, wrapping PyG's canonical GNNExplainer algorithm.

Perturbation-based (learns soft node/edge masks maximising mutual information
with the prediction). Not reimplemented — driven via ``torch_geometric.explain``.
The shared attribution flow lives in :class:`BaseExplainerAttributor`.
"""
from __future__ import annotations

from .base import BaseExplainerAttributor, _ExplainerWrapper


class GNNExplainerAttributor(BaseExplainerAttributor):
    method = "GNNExplainer"

    def __init__(self, model, task: str = "graph-classification", epochs: int = 100):
        self.epochs = epochs
        super().__init__(model, task=task)

    def _build_explainer(self):
        from torch_geometric.explain import Explainer, GNNExplainer

        mode = "multiclass_classification" if self.task == "graph-classification" else "regression"
        return Explainer(
            model=_ExplainerWrapper(self.model),
            algorithm=GNNExplainer(epochs=self.epochs),
            explanation_type="model",
            node_mask_type="attributes",
            edge_mask_type="object",
            model_config=dict(mode=mode, task_level="graph", return_type="raw"),
        )

    def _extra_meta(self) -> dict:
        return {"epochs": self.epochs}
