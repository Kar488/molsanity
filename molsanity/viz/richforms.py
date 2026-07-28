"""Richer statistical figure forms (distributions & relationships, not means).

- ``faithfulness_correctness_joint``: per-molecule scatter of occlusion
  faithfulness (x) vs ground-truth correctness (y), coloured by attributor, with
  marginal densities and a shaded "faithful-but-wrong" quadrant — the thesis in
  one figure.
- ``raincloud_gt``: half-violin + box + jittered points showing the full
  per-molecule GT-AUROC distribution per attributor.
- ``results_heatmap``: attributor × (dataset, metric) matrix, annotated.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from ..utils import get_logger
from .style import (
    AXIS_GREY,
    GREY,
    INK,
    MUTED_INK,
    apply_style,
    attributor_color,
    panel_label,
    save_vector,
    short,
)

log = get_logger()


def _parse_cell_id(cell_id: str) -> dict:
    parts = cell_id.split("__")
    return dict(zip(["dataset", "backbone", "attributor", "split"], parts + [""] * 4))


def _pairs(cells, dataset, backbone, split, xk, yk):
    """Return {attributor: (x_array, y_array)} of per-molecule metric pairs."""
    out = {}
    for cid, recs in cells.items():
        m = _parse_cell_id(cid)
        if m["dataset"] == dataset and m["backbone"] == backbone and m["split"] == split:
            x = np.array([r.get(xk, np.nan) for r in recs], dtype=np.float64)
            y = np.array([r.get(yk, np.nan) for r in recs], dtype=np.float64)
            mask = np.isfinite(x) & np.isfinite(y)
            if mask.sum():
                out[m["attributor"]] = (x[mask], y[mask])
    return out


def _kde(vals, grid):
    from scipy.stats import gaussian_kde

    vals = np.asarray(vals, dtype=np.float64)
    vals = vals[np.isfinite(vals)]
    if vals.size < 3 or np.std(vals) < 1e-6:
        return None
    try:
        return gaussian_kde(vals)(grid)
    except Exception:
        return None


def faithfulness_correctness_joint(
    cells, out_path, dataset="MUTAG", backbone="GINE", split="scaffold",
) -> dict | None:
    """Joint scatter of faithfulness (x) vs ground-truth correctness (y)."""
    apply_style()
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec

    data = _pairs(cells, dataset, backbone, split, "occ_spearman", "gt_auroc")
    if not data:
        return None

    fig = plt.figure(figsize=(7.8, 7.8))
    gs = GridSpec(2, 2, width_ratios=[5, 1.15], height_ratios=[1.15, 5],
                  hspace=0.04, wspace=0.04,
                  top=0.86, bottom=0.09, left=0.11, right=0.97)
    ax = fig.add_subplot(gs[1, 0])
    axx = fig.add_subplot(gs[0, 0], sharex=ax)
    axy = fig.add_subplot(gs[1, 1], sharey=ax)

    # "Faithful-but-wrong" quadrant: faithful to the model (x>0) yet below chance
    # ground-truth localisation (y<0.5).
    ax.axhspan(0.0, 0.5, xmin=0.5, xmax=1.0, color="#f4dcc9", alpha=0.45, zorder=0)
    ax.axhline(0.5, color=AXIS_GREY, ls=(0, (4, 3)), lw=1.1, zorder=1)
    ax.axvline(0.0, color="#c2c2bb", lw=1.1, zorder=1)

    xgrid = np.linspace(-1.05, 1.05, 200)
    ygrid = np.linspace(-0.03, 1.03, 200)
    for name in sorted(data):
        xs, ys = data[name]
        c = attributor_color(name)
        ax.scatter(xs, ys, s=46, color=c, alpha=0.72, edgecolor="white",
                   linewidth=0.6, zorder=3, label=short(name))
        kx = _kde(xs, xgrid)
        if kx is not None:
            axx.fill_between(xgrid, kx, color=c, alpha=0.16, zorder=2)
            axx.plot(xgrid, kx, color=c, lw=1.6, zorder=3)
        ky = _kde(ys, ygrid)
        if ky is not None:
            axy.fill_betweenx(ygrid, ky, color=c, alpha=0.16, zorder=2)
            axy.plot(ky, ygrid, color=c, lw=1.6, zorder=3)

    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-0.03, 1.03)
    ax.set_xlabel("Occlusion faithfulness  (Spearman ρ)  →  more faithful")
    ax.set_ylabel("Ground-truth correctness  (AUROC)  →  more correct")
    ax.text(0.97, 0.02, "faithful\nbut wrong", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=10.5, color="#a35a25",
            fontweight="semibold")
    ax.text(-1.0, 0.505, "chance", color=MUTED_INK, fontsize=9, va="bottom")
    ax.legend(loc="upper left", title="attributor", title_fontsize=9,
              frameon=False, fontsize=9)

    for a in (axx, axy):
        a.set_facecolor("white")
        for s in a.spines.values():
            s.set_visible(False)
        a.grid(False)
    axx.tick_params(labelbottom=False, left=False, labelleft=False, bottom=False)
    axy.tick_params(labelleft=False, bottom=False, labelbottom=False, left=False)

    fig.text(0.11, 0.955, f"Faithfulness ≠ correctness — {dataset} · {backbone} "
             f"({split} split)", fontsize=13, fontweight="semibold", ha="left",
             color=INK)
    fig.text(0.11, 0.925, "each point is one molecule · faithful-but-wrong "
             "(shaded) = high faithfulness, below-chance ground truth",
             fontsize=9.5, color=MUTED_INK, ha="left")
    return save_vector(fig, Path(out_path))


def raincloud_gt(cells, out_path, dataset="MUTAG", backbone="GINE", split="scaffold") -> dict | None:
    """Half-violin + box + jittered strip of per-molecule GT AUROC per attributor."""
    apply_style()
    import matplotlib.pyplot as plt
    from scipy.stats import gaussian_kde

    series = {}
    for cid, recs in cells.items():
        m = _parse_cell_id(cid)
        if m["dataset"] == dataset and m["backbone"] == backbone and m["split"] == split:
            v = np.array([r.get("gt_auroc", np.nan) for r in recs], dtype=np.float64)
            v = v[np.isfinite(v)]
            if v.size:
                series[m["attributor"]] = v
    if not series:
        return None
    order = sorted(series, key=lambda k: np.median(series[k]))
    fig, ax = plt.subplots(figsize=(7.6, 1.15 * len(order) + 1.8))
    rng = np.random.default_rng(0)

    for i, name in enumerate(order):
        v = series[name]
        c = attributor_color(name)
        # half violin (KDE) above the row
        if v.size >= 3 and np.std(v) > 1e-6:
            grid = np.linspace(max(-0.05, v.min() - 0.1), min(1.05, v.max() + 0.1), 200)
            dens = gaussian_kde(v)(grid)
            dens = dens / dens.max() * 0.36
            ax.fill_between(grid, i + 0.06, i + 0.06 + dens, color=c, alpha=0.28, zorder=2, lw=0)
            ax.plot(grid, i + 0.06 + dens, color=c, lw=1.4, zorder=3)
        # jittered points below the row
        jitter = i - 0.16 + rng.uniform(-0.07, 0.07, size=v.size)
        ax.scatter(v, jitter, s=26, color=c, alpha=0.6, edgecolor="white",
                   linewidth=0.4, zorder=3)
        # median marker
        med = float(np.median(v))
        ax.plot([med, med], [i - 0.26, i + 0.06], color=INK, lw=1.6, zorder=4)
        ax.text(1.04, i, f"med {med:.2f}", va="center", ha="left", fontsize=9,
                color=INK, fontweight="semibold")

    ax.axvline(0.5, color=AXIS_GREY, ls=(0, (4, 3)), lw=1.1, zorder=1)
    ax.text(0.5, len(order) - 0.35, "chance", color=MUTED_INK, fontsize=9, ha="center")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([short(n) for n in order], fontsize=11, color=INK)
    ax.set_ylim(-0.6, len(order) - 0.2)
    ax.set_xlim(-0.05, 1.18)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Ground-truth AUROC  (per molecule)")
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)
    ax.set_title(f"Per-molecule ground-truth localisation — {dataset} · {backbone}",
                 fontsize=12.5, loc="left", pad=12, fontweight="semibold")
    return save_vector(fig, Path(out_path))


def results_heatmap(cells, out_path, split="scaffold") -> dict | None:
    """Attributor × dataset heatmap of mean GT AUROC (classification, GINE).

    YlGnBu colour scheme (pale = weak, deep navy = strong) with crisp white cell
    dividers and contrast-aware value labels — the chance level (0.5) is marked on
    the colour bar.
    """
    apply_style()
    import matplotlib.pyplot as plt
    from matplotlib import colormaps
    from matplotlib.colors import Normalize

    datasets, attributors, vals = set(), set(), {}
    for cid, recs in cells.items():
        m = _parse_cell_id(cid)
        if m["backbone"] != "GINE" or m["split"] != split:
            continue
        v = np.array([r.get("gt_auroc", np.nan) for r in recs], dtype=np.float64)
        v = v[np.isfinite(v)]
        if v.size:
            datasets.add(m["dataset"]); attributors.add(m["attributor"])
            vals[(m["dataset"], m["attributor"])] = float(np.mean(v))
    if not vals:
        return None
    ds = sorted(datasets)
    at = sorted(attributors, key=lambda a: -np.nanmean([vals.get((d, a), np.nan) for d in ds]))
    M = np.full((len(at), len(ds)), np.nan)
    for i, a in enumerate(at):
        for j, d in enumerate(ds):
            if (d, a) in vals:
                M[i, j] = vals[(d, a)]

    cmap = colormaps["YlGnBu"]
    norm = Normalize(vmin=0.0, vmax=1.0)

    fig, ax = plt.subplots(figsize=(1.7 * len(ds) + 3.0, 0.82 * len(at) + 1.9))
    # Draw each cell as a white-bordered rectangle (crisp dividers), missing cells
    # rendered as a light neutral tile so the matrix stays complete-looking.
    for i in range(len(at)):
        for j in range(len(ds)):
            v = M[i, j]
            if np.isfinite(v):
                rgba = cmap(norm(v))
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=rgba,
                                           edgecolor="white", linewidth=3.5, zorder=2))
                lum = 0.299 * rgba[0] + 0.587 * rgba[1] + 0.114 * rgba[2]
                txt = "white" if lum < 0.55 else INK
                ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=13,
                        color=txt, fontweight="semibold", zorder=3)
            else:
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor="#f0f0ec",
                                           edgecolor="white", linewidth=3.5, zorder=2))
                ax.text(j, i, "–", ha="center", va="center", fontsize=13,
                        color="#b4b4ae", zorder=3)

    ax.set_xlim(-0.5, len(ds) - 0.5); ax.set_ylim(len(at) - 0.5, -0.5)
    ax.set_xticks(range(len(ds))); ax.set_xticklabels(ds, fontsize=11, color=INK)
    ax.set_yticks(range(len(at))); ax.set_yticklabels([short(a) for a in at], fontsize=11, color=INK)
    ax.tick_params(length=0)
    ax.grid(False)
    ax.set_aspect("auto")
    for s in ax.spines.values():
        s.set_visible(False)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm); sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, fraction=0.05, pad=0.04)
    cbar.set_label("mean ground-truth AUROC", fontsize=9.5, labelpad=20)
    cbar.ax.axhline(0.5, color="#c0392b", lw=1.6)
    cbar.set_ticks([0.0, 0.25, 0.5, 0.75, 1.0])
    cbar.set_ticklabels(["0.0", "0.25", "0.5\nchance", "0.75", "1.0"])
    cbar.ax.tick_params(length=0, labelsize=8)
    cbar.outline.set_visible(False)

    ax.set_title("Ground-truth localisation across datasets — GINE",
                 fontsize=12.5, loc="left", pad=12, fontweight="semibold")
    fig.tight_layout()
    return save_vector(fig, Path(out_path))
