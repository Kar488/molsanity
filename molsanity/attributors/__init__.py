"""molsanity.attributors — uniform adapter over canonical attribution methods."""
from .base import Attribution, minmax_normalise
from .captum_methods import CaptumAttributor
from .gnn_explainer import GNNExplainerAttributor
from .integrated_gradients import IntegratedGradientsAttributor

# Gradient-family methods share the Captum adapter (parameterised by name).
_CAPTUM_METHODS = {"IntegratedGradients", "Saliency", "InputXGradient",
                   "GuidedBackprop", "Deconvolution"}


def build_attributor(name, model, **kwargs):
    if name in _CAPTUM_METHODS:
        ig_steps = kwargs.pop("ig_steps", 25)
        task = kwargs.pop("task", "graph-classification")
        return CaptumAttributor(model, method=name, task=task, ig_steps=ig_steps)
    if name == "GNNExplainer":
        task = kwargs.pop("task", "graph-classification")
        epochs = kwargs.pop("epochs", 100)
        kwargs.pop("ig_steps", None)
        return GNNExplainerAttributor(model, task=task, epochs=epochs)
    raise KeyError(
        f"Unknown attributor '{name}'. Known: "
        f"{sorted(_CAPTUM_METHODS | {'GNNExplainer'})}. "
        "PGExplainer/SubgraphX are blocked-tolerant (see TASKS.md)."
    )


ATTRIBUTORS = sorted(_CAPTUM_METHODS | {"GNNExplainer"})

__all__ = [
    "Attribution", "minmax_normalise", "CaptumAttributor",
    "IntegratedGradientsAttributor", "GNNExplainerAttributor",
    "build_attributor", "ATTRIBUTORS",
]
