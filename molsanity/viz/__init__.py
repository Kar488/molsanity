"""molsanity.viz — publication figures (house-styled, vector PDF+SVG)."""
from .figures import ground_truth_validation_figure, molecule_attribution_svg
from .composite import results_composite
from .molgrid import attribution_grid, make_case_study_grid
from .summary import (
    attributor_gt_bar,
    faithfulness_stability_ecdf,
    make_summary_figures,
    regime_stratification_figure,
)
from .style import apply_style, attributor_color, backbone_color

__all__ = [
    "ground_truth_validation_figure", "molecule_attribution_svg",
    "attribution_grid", "make_case_study_grid",
    "make_summary_figures", "results_composite", "attributor_gt_bar",
    "faithfulness_stability_ecdf", "regime_stratification_figure",
    "apply_style", "attributor_color", "backbone_color",
]
