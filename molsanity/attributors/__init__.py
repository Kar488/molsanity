"""molsanity.attributors — uniform adapter over canonical attribution methods."""
from .base import Attribution
from .integrated_gradients import IntegratedGradientsAttributor

ATTRIBUTORS = {
    "IntegratedGradients": IntegratedGradientsAttributor,
}


def build_attributor(name, model, **kwargs):
    if name not in ATTRIBUTORS:
        raise KeyError(f"Unknown attributor '{name}'. Known: {sorted(ATTRIBUTORS)}")
    return ATTRIBUTORS[name](model, **kwargs)


__all__ = ["Attribution", "IntegratedGradientsAttributor", "build_attributor", "ATTRIBUTORS"]
