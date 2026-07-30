"""molsanity.attributors — uniform adapter over canonical attribution methods."""
from .base import Attribution, minmax_normalise
from .captum_methods import CaptumAttributor
from .gnn_explainer import GNNExplainerAttributor
from .integrated_gradients import IntegratedGradientsAttributor
from .pg_explainer import PGExplainerAttributor
from .subgraphx import SubgraphXAttributor, SubgraphXUnavailable

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
    if name == "PGExplainer":
        task = kwargs.pop("task", "graph-classification")
        kwargs.pop("ig_steps", None)
        return PGExplainerAttributor(
            model, task=task,
            train_graphs=kwargs.pop("train_graphs", None),
            epochs=kwargs.pop("pg_epochs", 30),
            seed=kwargs.pop("seed", 0),
        )
    if name == "SubgraphX":
        # Raises SubgraphXUnavailable at first use if DIG's compiled
        # dependencies are missing; run_all catches it and skips the cell.
        task = kwargs.pop("task", "graph-classification")
        kwargs.pop("ig_steps", None)
        return SubgraphXAttributor(
            model, task=task,
            max_nodes=kwargs.pop("sgx_max_nodes", 8),
            rollouts=kwargs.pop("sgx_rollouts", 20),
            seed=kwargs.pop("seed", 0),
        )
    raise KeyError(f"Unknown attributor '{name}'. Known: {ATTRIBUTORS}.")


ATTRIBUTORS = sorted(_CAPTUM_METHODS | {"GNNExplainer", "PGExplainer",
                                        "SubgraphX"})

__all__ = [
    "Attribution", "minmax_normalise", "CaptumAttributor",
    "IntegratedGradientsAttributor", "GNNExplainerAttributor",
    "PGExplainerAttributor", "SubgraphXAttributor", "SubgraphXUnavailable",
    "build_attributor", "ATTRIBUTORS",
]
