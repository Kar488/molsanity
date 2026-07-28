"""Captum-based attributors wrapped via PyG's CaptumExplainer.

A single adapter parameterised by the Captum method name. We do NOT reimplement
any attribution method — Captum provides them; PyG's ``CaptumExplainer`` bridges
them to graphs; the shared flow + schema packaging live in :class:`BaseExplainerAttributor`.

Supported (gradient-family, cheap, backbone-agnostic):
  IntegratedGradients, Saliency, InputXGradient, GuidedBackprop, Deconvolution.
"""
from __future__ import annotations

from .base import BaseExplainerAttributor, _ExplainerWrapper  # noqa: F401 (re-export)

# Methods that accept n_steps (integration path) vs those that do not.
_STEP_METHODS = {"IntegratedGradients"}


class CaptumAttributor(BaseExplainerAttributor):
    def __init__(self, model, method: str = "IntegratedGradients",
                 task: str = "graph-classification", ig_steps: int = 25):
        self.method = method
        self.ig_steps = ig_steps
        super().__init__(model, task=task)

    def _build_explainer(self):
        from torch_geometric.explain import CaptumExplainer, Explainer

        mode = "multiclass_classification" if self.task == "graph-classification" else "regression"
        kwargs = {"n_steps": self.ig_steps} if self.method in _STEP_METHODS else {}
        return Explainer(
            model=_ExplainerWrapper(self.model),
            algorithm=CaptumExplainer(self.method, **kwargs),
            explanation_type="model",
            node_mask_type="attributes",
            edge_mask_type="object",
            model_config=dict(mode=mode, task_level="graph", return_type="raw"),
        )
