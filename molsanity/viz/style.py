"""Shared publication figure style: validated palette + entity colours + rcParams.

One house style for every figure. Colours come from a colourblind-safe
categorical palette (validated with the dataviz palette checker); each attributor
and backbone is bound to a *fixed* hue so identity is consistent across panels
(colour follows the entity, never its rank). Figures are vector (PDF + SVG).
"""
from __future__ import annotations

from pathlib import Path

# Validated categorical palette (light surface). Order is fixed.
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#4a3aa7"]
GREY = "#8a8a86"
GT_GREEN = "#008300"

# Fixed entity -> colour. New entities append; never reorder (identity is stable).
ATTRIBUTOR_COLORS = {
    "IntegratedGradients": PALETTE[0],
    "GNNExplainer": PALETTE[1],
    "Saliency": PALETTE[2],
    "InputXGradient": PALETTE[3],
    "GuidedBackprop": PALETTE[4],
    "Deconvolution": PALETTE[5],
}
BACKBONE_COLORS = {
    "GINE": PALETTE[0],
    "GCN": PALETTE[1],
    "GAT": PALETTE[2],
    "MPNN": PALETTE[3],
    "AttentiveFP": PALETTE[4],
}

# Short display labels to keep legends compact.
SHORT = {
    "IntegratedGradients": "IG",
    "GNNExplainer": "GNNExpl",
    "InputXGradient": "InputXGrad",
    "GuidedBackprop": "GuidedBP",
    "Deconvolution": "Deconv",
    "Saliency": "Saliency",
}


def attributor_color(name: str) -> str:
    return ATTRIBUTOR_COLORS.get(name, GREY)


def backbone_color(name: str) -> str:
    return BACKBONE_COLORS.get(name, GREY)


def short(name: str) -> str:
    return SHORT.get(name, name)


def apply_style():
    """Set global matplotlib rcParams for a clean, publication-grade look."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib as mpl

    mpl.rcParams.update({
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "axes.titleweight": "bold",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.8,
        "axes.edgecolor": "#3a3a38",
        "axes.labelcolor": "#1a1a19",
        "axes.grid": True,
        "grid.color": "#e6e6e2",
        "grid.linewidth": 0.6,
        "xtick.color": "#3a3a38",
        "ytick.color": "#3a3a38",
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "legend.fontsize": 7.5,
        "legend.frameon": False,
        "lines.linewidth": 2.0,
        "lines.solid_capstyle": "round",
        "text.color": "#1a1a19",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "svg.fonttype": "none",
    })


def panel_label(ax, letter: str, dx: float = -0.14, dy: float = 1.06):
    """Bold panel letter (a, b, …) in the top-left, Nature-style."""
    ax.text(dx, dy, letter, transform=ax.transAxes, fontsize=12,
            fontweight="bold", va="top", ha="left")


def save_vector(fig, out_path) -> dict:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pdf, svg = out_path.with_suffix(".pdf"), out_path.with_suffix(".svg")
    fig.savefig(pdf, bbox_inches="tight")
    fig.savefig(svg, bbox_inches="tight")
    import matplotlib.pyplot as plt

    plt.close(fig)
    return {"pdf": str(pdf), "svg": str(svg)}
