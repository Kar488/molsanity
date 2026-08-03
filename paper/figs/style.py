"""Shared figure style for the manuscript (vector PDF, Pagella-matched serif)."""
from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt

ACCENT = "#264E78"
INK = "#1a1a1a"
MUTED = "#6b7280"
GRID = "#d9dde3"

# Colour-blind-safe categorical palette (Okabe–Ito derived), fixed per entity.
REGIME_COLOR = {
    "synthetic": "#0072B2",       # exact node ground truth
    "classification": "#D55E00",  # molecular classification
    "regression": "#009E73",      # molecular regression
}
GT_COLOR = {
    "exact": "#0072B2",
    "proxy": "#D55E00",
}
ATTRIBUTOR_MARKER = {
    "IntegratedGradients": "o",
    "Saliency": "s",
    "InputXGradient": "^",
    "GuidedBackprop": "D",
    "GNNExplainer": "P",
    "PGExplainer": "X",
    "SubgraphX": "v",
}
ATTRIBUTOR_COLOR = {
    "IntegratedGradients": "#0072B2",
    "Saliency": "#D55E00",
    "InputXGradient": "#009E73",
    "GuidedBackprop": "#CC79A7",
    "GNNExplainer": "#E69F00",
    "PGExplainer": "#56B4E9",
    "SubgraphX": "#000000",
}
BACKBONE_COLOR = {
    "GINE": "#0072B2",
    "GCN": "#D55E00",
    "GAT": "#009E73",
    "MPNN": "#CC79A7",
    "AttentiveFP": "#E69F00",
}
SHORT = {
    "IntegratedGradients": "IG",
    "Saliency": "Saliency",
    "InputXGradient": "Input×Grad",
    "GuidedBackprop": "GuidedBP",
    "GNNExplainer": "GNNExpl",
    "PGExplainer": "PGExpl",
    "SubgraphX": "SubgraphX",
}


def use_style():
    mpl.rcParams.update({
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "font.family": "serif",
        "font.serif": ["TeX Gyre Pagella", "Palatino", "URW Palladio L",
                       "TeX Gyre Termes", "DejaVu Serif"],
        "mathtext.fontset": "dejavuserif",
        "font.size": 8.0,
        "axes.titlesize": 8.5,
        "axes.labelsize": 8.0,
        "xtick.labelsize": 7.2,
        "ytick.labelsize": 7.2,
        "legend.fontsize": 7.0,
        "axes.edgecolor": "#9aa2ad",
        "axes.linewidth": 0.6,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": "#4b5563",
        "ytick.color": "#4b5563",
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
        "grid.color": GRID,
        "grid.linewidth": 0.5,
        "legend.frameon": False,
        "figure.dpi": 200,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
    })


def panel_label(ax, letter, dx=-0.085, dy=1.045):
    ax.text(dx, dy, letter, transform=ax.transAxes, fontsize=9.5,
            fontweight="bold", va="top", ha="left", color=INK)


def despine(ax, keep=("left", "bottom")):
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(side in keep)


def save(fig, path):
    fig.savefig(path, format="pdf")
    plt.close(fig)
    print(f"  wrote {path}")
