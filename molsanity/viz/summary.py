"""Cross-matrix publication figures built from the per-cell audit records.

House-styled (see ``style.py``): fixed entity colours, bold panel letters, inline
value labels, clean spines. All vector (PDF + SVG). These summarise the whole
audit matrix — GT localisation by attributor, faithfulness/stability ECDFs, and
regime-stratified reliability.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from ..utils import get_logger
from .style import (
    AXIS_GREY,
    GREY,
    INK,
    METRIC_COLORS,
    MUTED_INK,
    apply_style,
    attributor_color,
    panel_label,
    save_vector,
    short,
)

log = get_logger()


def _ecdf(x):
    x = np.sort(np.asarray([v for v in x if np.isfinite(v)], dtype=np.float64))
    if x.size == 0:
        return np.array([]), np.array([])
    return x, np.arange(1, x.size + 1) / x.size


def _col(records, name):
    return np.array([r.get(name, np.nan) for r in records], dtype=np.float64)


def _parse_cell_id(cell_id: str) -> dict:
    parts = cell_id.split("__")
    return dict(zip(["dataset", "backbone", "attributor", "split"], parts + [""] * 4))


def attributor_gt_bar(cells: dict, out_path, dataset="MUTAG", split="scaffold") -> dict | None:
    """Bar of mean GT AUROC per attributor (fixed backbone GINE) with 95% CI."""
    apply_style()
    import matplotlib.pyplot as plt

    from ..audit.stats import bootstrap_ci

    rows = []
    for cid, recs in cells.items():
        m = _parse_cell_id(cid)
        if m["dataset"] == dataset and m["backbone"] == "GINE" and m["split"] == split:
            ci = bootstrap_ci(_col(recs, "gt_auroc"))
            if np.isfinite(ci["mean"]):
                rows.append((m["attributor"], ci))
    if not rows:
        return None
    rows.sort(key=lambda r: r[1]["mean"])
    labels = [short(r[0]) for r in rows]
    colors = [attributor_color(r[0]) for r in rows]
    means = [r[1]["mean"] for r in rows]
    lo = [max(0.0, r[1]["mean"] - r[1]["lo"]) for r in rows]
    hi = [max(0.0, r[1]["hi"] - r[1]["mean"]) for r in rows]

    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    y = np.arange(len(labels))
    ax.barh(y, means, xerr=[lo, hi], color=colors, capsize=2.5,
            edgecolor="white", linewidth=0.8,
            error_kw={"lw": 0.9, "ecolor": MUTED_INK}, height=0.62, zorder=3)
    ax.axvline(0.5, color=GREY, ls=(0, (4, 3)), lw=0.9, zorder=1)
    ax.text(0.5, -0.78, "chance", color=GREY, fontsize=7.5, ha="center", va="top",
            style="italic")
    for yi, mval, h in zip(y, means, hi):
        ax.text(mval + h + 0.03, yi, f"{mval:.2f}", va="center", ha="left",
                fontsize=9.5, color=INK, fontweight="semibold")
    ax.set_yticks(y); ax.set_yticklabels(labels, color=INK)
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(-0.95, len(labels) - 0.3)
    ax.set_xlim(0, 1.15)
    ax.grid(axis="x", visible=True)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Ground-truth AUROC (mean ± 95% CI)")
    ax.set_title(f"{dataset} · GINE · attribution vs ground truth · {split} split",
                 fontsize=9.5, color=INK)
    fig.tight_layout()
    return save_vector(fig, Path(out_path))


def faithfulness_stability_ecdf(cells: dict, out_path, dataset="MUTAG", split="scaffold") -> dict | None:
    """ECDFs of occlusion faithfulness and cross-checkpoint stability per attributor."""
    apply_style()
    import matplotlib.pyplot as plt

    series = {}
    for cid, recs in cells.items():
        m = _parse_cell_id(cid)
        if m["dataset"] == dataset and m["backbone"] == "GINE" and m["split"] == split:
            series[m["attributor"]] = recs
    if not series:
        return None

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    for name, recs in sorted(series.items()):
        c = attributor_color(name)
        x, y = _ecdf(_col(recs, "occ_spearman"))
        if x.size:
            axes[0].step(x, y, where="post", color=c, lw=2, label=short(name))
        xs, ys = _ecdf(_col(recs, "stability"))
        if xs.size:
            axes[1].step(xs, ys, where="post", color=c, lw=2, label=short(name))
    axes[0].axvline(0, color=GREY, ls="--", lw=1)
    axes[0].set_xlabel("Occlusion faithfulness (Spearman)")
    axes[0].set_ylabel("Cumulative fraction of molecules")
    axes[0].set_title("Faithfulness")
    axes[0].legend(loc="upper left")
    panel_label(axes[0], "a")
    axes[1].set_xlabel("Cross-checkpoint stability (Spearman)")
    axes[1].set_title("Stability")
    axes[1].legend(loc="upper left")
    panel_label(axes[1], "b")
    fig.suptitle(f"{dataset} · GINE ({split} split)", fontsize=11, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    return save_vector(fig, Path(out_path))


def regime_stratification_figure(cells: dict, out_path, split="scaffold") -> dict | None:
    """Reliability (GT AUROC, occlusion) stratified by confidence/correctness regime,
    pooled across all classification cells with the given split."""
    apply_style()
    import matplotlib.pyplot as plt

    regimes = ["confident_correct", "confident_error", "borderline"]
    reg_labels = ["confident\ncorrect", "confident\nerror", "borderline"]
    pooled = {r: {"gt_auroc": [], "occ_spearman": []} for r in regimes}
    for cid, recs in cells.items():
        m = _parse_cell_id(cid)
        if m["split"] != split:
            continue
        for rec in recs:
            reg = rec.get("regime")
            if reg in pooled:
                pooled[reg]["gt_auroc"].append(rec.get("gt_auroc", np.nan))
                pooled[reg]["occ_spearman"].append(rec.get("occ_spearman", np.nan))

    counts = {r: len([v for v in pooled[r]["occ_spearman"] if np.isfinite(v)]) for r in regimes}
    if sum(counts.values()) == 0:
        return None

    def _mean(vals):
        vals = [v for v in vals if np.isfinite(v)]
        return float(np.mean(vals)) if vals else np.nan

    gt = [_mean(pooled[r]["gt_auroc"]) for r in regimes]
    occ = [_mean(pooled[r]["occ_spearman"]) for r in regimes]

    # Dumbbell plot: one row per (populated) regime; a dot for GT AUROC and a dot
    # for occlusion faithfulness joined by a thin connector. Reads as a designed
    # comparison, not a chunky grouped bar; empty regimes (n=0) are dropped.
    from matplotlib.lines import Line2D

    order = [r for r in ["confident_correct", "borderline", "confident_error"]
             if counts[r] > 0]
    label_of = dict(zip(regimes, reg_labels))
    dropped = [r for r in regimes if counts[r] == 0]

    fig, ax = plt.subplots(figsize=(8.4, 1.15 * len(order) + 2.2))
    y = np.arange(len(order))[::-1]  # first regime at top

    finite = [v for v in gt + occ if np.isfinite(v)] or [0.0]
    lo_x, hi_x = min(0.0, min(finite)) - 0.16, max(0.5, max(finite)) + 0.16
    ax.set_xlim(lo_x, hi_x)

    # Reference lines behind everything.
    ax.axvline(0.0, color="#c2c2bb", lw=1.1, zorder=1)
    ax.axvline(0.5, color=AXIS_GREY, ls=(0, (4, 3)), lw=1.1, zorder=1)
    ax.text(0.5, len(order) - 0.36, "chance (0.5)", color=MUTED_INK, fontsize=9,
            ha="center", va="bottom")

    for yi, r in zip(y, order):
        g, o = dict(zip(regimes, gt))[r], dict(zip(regimes, occ))[r]
        ax.plot([g, o], [yi, yi], color="#b9b9b1", lw=3.0, zorder=2,
                solid_capstyle="round")
        ax.scatter([g], [yi], s=230, color=METRIC_COLORS["gt"], zorder=4,
                   edgecolor="white", linewidth=1.5)
        ax.scatter([o], [yi], s=230, color=METRIC_COLORS["occ"], zorder=4,
                   edgecolor="white", linewidth=1.5)
        # Value labels on the outer side of each dot, in dark ink (readable;
        # the coloured dot beside them carries the identity).
        lefti, righti = (g, o) if g <= o else (o, g)
        ax.text(lefti - 0.028, yi, f"{lefti:.2f}", ha="right", va="center",
                fontsize=10.5, color=INK, fontweight="semibold")
        ax.text(righti + 0.028, yi, f"{righti:.2f}", ha="left", va="center",
                fontsize=10.5, color=INK, fontweight="semibold")

    ax.set_yticks(y)
    ax.set_yticklabels([f"{label_of[r].replace(chr(10), ' ')}  (n={counts[r]})" for r in order],
                       fontsize=11, color=INK, fontweight="medium")
    ax.set_ylim(-0.7, len(order) - 0.1)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Mean reliability")
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    ax.spines["left"].set_visible(False)

    sub = f"GT localisation vs occlusion faithfulness · {split} split · pooled"
    if dropped:
        sub += " · confident-error empty (n=0)"
    ax.set_title("Attribution reliability by regime",
                 fontsize=13, color=INK, loc="left", pad=26, fontweight="semibold")
    ax.text(0.0, 1.05, sub, transform=ax.transAxes, fontsize=9.5, color=MUTED_INK,
            ha="left", va="bottom")

    handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor=METRIC_COLORS["gt"],
               markersize=11, label="GT AUROC (correctness)"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=METRIC_COLORS["occ"],
               markersize=11, label="Occlusion ρ (faithfulness)"),
    ]
    ax.legend(handles=handles, loc="lower right", bbox_to_anchor=(1.0, -0.04),
              ncol=1, frameon=False, fontsize=9.5, handletextpad=0.4)
    fig.tight_layout()
    return save_vector(fig, Path(out_path))


def make_summary_figures(out_dir="artifacts/figures/_summary") -> dict:
    """Generate all cross-matrix figures from the discovered audit records."""
    from ..benchmark.tables import discover_cells

    cells = discover_cells()
    out_dir = Path(out_dir)
    made = {}
    if not cells:
        log.info("No audit cells found; skipping summary figures.")
        return made
    jobs = [
        ("attributor_gt_bar_MUTAG",
         lambda: attributor_gt_bar(cells, out_dir / "attributor_gt_bar_MUTAG", dataset="MUTAG")),
        ("attributor_gt_bar_SynthMotifs",
         lambda: attributor_gt_bar(cells, out_dir / "attributor_gt_bar_SynthMotifs", dataset="SynthMotifs")),
        ("faithfulness_stability_ecdf",
         lambda: faithfulness_stability_ecdf(cells, out_dir / "faithfulness_stability_ecdf")),
        ("regime_stratification",
         lambda: regime_stratification_figure(cells, out_dir / "regime_stratification")),
    ]
    for name, fn in jobs:
        try:
            info = fn()
            if info:
                made[name] = info
                log.info("Wrote summary figure: %s", info["pdf"])
        except Exception as exc:  # noqa: BLE001
            log.warning("Summary figure %s failed: %s", name, exc)

    # Assembled multi-panel composite (Nature-style Figure 2).
    try:
        from .composite import results_composite

        info = results_composite(out_dir / "results_composite")
        if info:
            made["results_composite"] = info
            log.info("Wrote composite figure: %s", info["pdf"])
    except Exception as exc:  # noqa: BLE001
        log.warning("Composite figure failed: %s", exc)

    # Signature molecule × attributor grids (retrains cheaply from cached ckpts).
    from .molgrid import make_case_study_grid

    grid_methods = ["Saliency", "InputXGradient", "IntegratedGradients", "GNNExplainer"]
    for ds in ("MUTAG", "SynthMotifs"):
        try:
            info = make_case_study_grid(ds, "GINE", grid_methods,
                                        out_dir / f"molgrid_{ds}", n_molecules=3)
            if info:
                made[f"molgrid_{ds}"] = info
                log.info("Wrote molecule grid: %s", info["pdf"])
        except Exception as exc:  # noqa: BLE001
            log.warning("Molecule grid %s failed: %s", ds, exc)
    return made
