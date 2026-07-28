"""Integrated Gradients attributor (Captum via PyG's CaptumExplainer).

Thin specialisation of :class:`CaptumAttributor`; the generic Captum bridge and
schema packaging live in ``captum_methods.py``.
"""
from __future__ import annotations

from .captum_methods import CaptumAttributor


class IntegratedGradientsAttributor(CaptumAttributor):
    method = "IntegratedGradients"

    def __init__(self, model, task: str = "graph-classification", ig_steps: int = 25):
        super().__init__(model, method="IntegratedGradients", task=task, ig_steps=ig_steps)
