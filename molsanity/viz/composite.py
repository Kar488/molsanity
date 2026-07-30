"""Assembled multi-panel results figure (Nature-style composite).

Combines the audit's headline panels into one publication figure with bold panel
letters and the shared house style: ground-truth localisation per attributor
(exact vs proxy GT), model-agnostic localisation per backbone, faithfulness and
stability ECDFs, and regime-stratified reliability. Vector PDF + SVG.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from ..utils import get_logger
from .style import (
    GREY,
    METRIC_COLORS,
    MUTED_INK,
    apply_style,
    attributor_color,
    backbone_color,
    panel_label,
    save_vector,
    short,
)
from .summary import _col, _ecdf, _parse_cell_id

log = get_logger()


def _gt_bar(ax, cells, dataset, split="scaffold"):
    from ..audit.stats import bootstrap_ci

    rows = []
    for cid, recs in cells.items():
        m = _parse_cell_id(cid)
        if m["dataset"] == dataset and m["backbone"] == "GINE" and m["split"] == split:
            ci = bootstrap_ci(_col(recs, "gt_auroc"))
            if np.isfinite(ci["mean"]):
                rows.append((m["attributor"], ci))
    rows.sort(key=lambda r: r[1]["mean"])
    if not rows:
        ax.set_axis_off()
        return
    y = np.arange(len(rows))
    means = [r[1]["mean"] for r in rows]
    lo = [max(0, r[1]["mean"] - r[1]["lo"]) for r in rows]
    hi = [max(0, r[1]["hi"] - r[1]["mean"]) for r in rows]
    ax.barh(y, means, xerr=[lo, hi], color=[attributor_color(r[0]) for r in rows],
            height=0.6, capsize=2.2, edgecolor="white", linewidth=0.7,
            error_kw={"lw": 0.8, "ecolor": MUTED_INK}, zorder=3)
    ax.axvline(0.5, color=GREY, ls=(0, (4, 3)), lw=0.9, zorder=1)
    for yi, mv, h in zip(y, means, hi):
        ax.text(mv + h + 0.03, yi, f"{mv:.2f}", va="center", fontsize=7, color=MUTED_INK)
    ax.tick_params(axis="y", length=0)
    ax.set_yticks(y); ax.set_yticklabels([short(r[0]) for r in rows], fontsize=7.5)
    ax.set_xlim(0, 1.18); ax.set_xlabel("GT AUROC", fontsize=8)
    ax.set_title(f"{dataset}", fontsize=9)
    ax.grid(axis="y", visible=False)


def _backbone_bar(ax, cells, dataset="MUTAG", attributor="IntegratedGradients", split="scaffold"):
    from ..audit.stats import bootstrap_ci

    rows = []
    for cid, recs in cells.items():
        m = _parse_cell_id(cid)
        if m["dataset"] == dataset and m["attributor"] == attributor and m["split"] == split:
            ci = bootstrap_ci(_col(recs, "gt_auroc"))
            if np.isfinite(ci["mean"]):
                rows.append((m["backbone"], ci))
    rows.sort(key=lambda r: r[1]["mean"])
    if not rows:
        ax.set_axis_off()
        return
    y = np.arange(len(rows))
    means = [r[1]["mean"] for r in rows]
    lo = [max(0, r[1]["mean"] - r[1]["lo"]) for r in rows]
    hi = [max(0, r[1]["hi"] - r[1]["mean"]) for r in rows]
    ax.barh(y, means, xerr=[lo, hi], color=[backbone_color(r[0]) for r in rows],
            height=0.6, capsize=2.2, edgecolor="white", linewidth=0.7,
            error_kw={"lw": 0.8, "ecolor": MUTED_INK}, zorder=3)
    ax.axvline(0.5, color=GREY, ls=(0, (4, 3)), lw=0.9, zorder=1)
    for yi, mv, h in zip(y, means, hi):
        ax.text(mv + h + 0.03, yi, f"{mv:.2f}", va="center", fontsize=7, color=MUTED_INK)
    ax.tick_params(axis="y", length=0)
    ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=7.5)
    ax.set_xlim(0, 1.18); ax.set_xlabel("GT AUROC", fontsize=8)
    ax.set_title(f"{dataset} · {short(attributor)} · by backbone", fontsize=9)
    ax.grid(axis="y", visible=False)


def _ecdf_panel(ax, cells, metric, dataset="MUTAG", split="scaffold", xlabel=""):
    series = {}
    for cid, recs in cells.items():
        m = _parse_cell_id(cid)
        if m["dataset"] == dataset and m["backbone"] == "GINE" and m["split"] == split:
            series[m["attributor"]] = recs
    for name, recs in sorted(series.items()):
        x, y = _ecdf(_col(recs, metric))
        if x.size:
            ax.step(x, y, where="post", color=attributor_color(name), lw=1.8, label=short(name))
    ax.axvline(0, color=GREY, ls="--", lw=1)
    ax.set_xlabel(xlabel, fontsize=8); ax.set_ylabel("cum. frac.", fontsize=8)
    ax.legend(fontsize=6.5, loc="upper left")


def _regime_panel(ax, cells, split="scaffold"):
    """Compact dumbbell: GT AUROC vs occlusion faithfulness per populated regime."""
    from matplotlib.lines import Line2D

    regimes = ["confident_correct", "borderline", "confident_error"]
    labels = {"confident_correct": "confident\ncorrect",
              "borderline": "borderline", "confident_error": "confident\nerror"}
    pooled = {r: {"gt": [], "occ": []} for r in regimes}
    for cid, recs in cells.items():
        if _parse_cell_id(cid)["split"] != split:
            continue
        for rec in recs:
            r = rec.get("regime")
            if r in pooled:
                pooled[r]["gt"].append(rec.get("gt_auroc", np.nan))
                pooled[r]["occ"].append(rec.get("occ_spearman", np.nan))

    def mean(v):
        v = [z for z in v if np.isfinite(z)]
        return float(np.mean(v)) if v else np.nan
    counts = {r: len([z for z in pooled[r]["occ"] if np.isfinite(z)]) for r in regimes}
    order = [r for r in regimes if counts[r] > 0]
    y = np.arange(len(order))[::-1]

    ax.axvline(0.0, color="#d7d7d1", lw=1.0, zorder=1)
    ax.axvline(0.5, color=GREY, ls=(0, (4, 3)), lw=1.0, zorder=1)
    for yi, r in zip(y, order):
        g, o = mean(pooled[r]["gt"]), mean(pooled[r]["occ"])
        ax.plot([g, o], [yi, yi], color="#cfcfc8", lw=2.2, zorder=2, solid_capstyle="round")
        ax.scatter([g], [yi], s=90, color=METRIC_COLORS["gt"], zorder=4, edgecolor="white", linewidth=1.0)
        ax.scatter([o], [yi], s=90, color=METRIC_COLORS["occ"], zorder=4, edgecolor="white", linewidth=1.0)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{labels[r].replace(chr(10),' ')}\n(n={counts[r]})" for r in order], fontsize=7.5)
    ax.set_ylim(-0.6, len(order) - 0.2)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("mean reliability", fontsize=8)
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)
    handles = [Line2D([0], [0], marker="o", color="none", markerfacecolor=METRIC_COLORS["gt"], markersize=7, label="GT AUROC"),
               Line2D([0], [0], marker="o", color="none", markerfacecolor=METRIC_COLORS["occ"], markersize=7, label="Occl. ρ")]
    ax.legend(handles=handles, fontsize=6.5, loc="lower right", frameon=False, handletextpad=0.2)


def results_composite(out_path="artifacts/figures/_summary/results_composite") -> dict | None:
    from ..benchmark.tables import discover_cells

    apply_style()
    import matplotlib.pyplot as plt

    cells = discover_cells()
    if not cells:
        return None
    fig, axes = plt.subplots(2, 3, figsize=(11.5, 6.4))
    _gt_bar(axes[0, 0], cells, "MUTAG")
    axes[0, 0].set_title("MUTAG (proxy GT) · by attributor", fontsize=9)
    _gt_bar(axes[0, 1], cells, "SynthMotifs")
    axes[0, 1].set_title("SynthMotifs (exact GT) · by attributor", fontsize=9)
    _backbone_bar(axes[0, 2], cells, "MUTAG", "IntegratedGradients")
    _ecdf_panel(axes[1, 0], cells, "occ_spearman", xlabel="occlusion faithfulness (ρ)")
    axes[1, 0].set_title("MUTAG · faithfulness", fontsize=9)
    _ecdf_panel(axes[1, 1], cells, "stability", xlabel="cross-checkpoint stability (ρ)")
    axes[1, 1].set_title("MUTAG · stability", fontsize=9)
    _regime_panel(axes[1, 2], cells)
    axes[1, 2].set_title("reliability by regime (pooled)", fontsize=9)

    for ax, letter in zip(axes.ravel(), "abcdef"):
        panel_label(ax, letter, dx=-0.18, dy=1.12)
    fig.suptitle("MolSanity reliability audit — attribution vs ground truth, faithfulness, "
                 "stability, and regime stratification under scaffold shift",
                 fontsize=11, fontweight="bold", y=1.02)
    fig.tight_layout(rect=(0, 0, 1, 0.98))
    return save_vector(fig, Path(out_path))
