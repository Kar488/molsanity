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
                fontsize=8, color=MUTED_INK)
    ax.set_yticks(y); ax.set_yticklabels(labels)
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

    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    x = np.arange(len(regimes))
    w = 0.32
    b1 = ax.bar(x - w / 2, gt, w, color=METRIC_COLORS["gt"], label="GT AUROC",
                edgecolor="white", linewidth=0.8, zorder=3)
    b2 = ax.bar(x + w / 2, occ, w, color=METRIC_COLORS["occ"], label="Occlusion ρ",
                edgecolor="white", linewidth=0.8, zorder=3)

    finite = [v for v in gt + occ if np.isfinite(v)] or [0.0]
    top = max(0.5, max(finite)) + 0.16
    bottom = min(0.0, min(finite)) - 0.16
    ax.set_ylim(bottom, top)
    ax.axhline(0.5, color=GREY, ls=(0, (4, 3)), lw=0.9, zorder=1)
    ax.text(-0.42, 0.505, "chance", color=GREY, fontsize=7,
            va="bottom", ha="left", style="italic")
    ax.axhline(0, color="#c4c4be", lw=0.9, zorder=1)

    for bars, vals in [(b1, gt), (b2, occ)]:
        for bar, v in zip(bars, vals):
            if not np.isfinite(v):
                continue
            off, va = (0.02, "bottom") if v >= 0 else (-0.02, "top")
            ax.text(bar.get_x() + bar.get_width() / 2, v + off, f"{v:.2f}",
                    ha="center", va=va, fontsize=8, color=MUTED_INK)

    ax.set_xticks(x)
    ax.set_xticklabels([f"{lab}\n(n={counts[r]})" for lab, r in zip(reg_labels, regimes)])
    ax.tick_params(axis="x", length=0)
    ax.set_ylabel("Mean reliability")
    ax.set_title(f"Attribution reliability by confidence/correctness regime "
                 f"· {split} split, pooled", fontsize=9.5, color=INK)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 0.98), ncol=1,
              handlelength=1.1, handleheight=1.1, borderpad=0.6,
              frameon=True, framealpha=0.95, edgecolor="#e2e2dd", fontsize=8)
    ax.margins(x=0.12)
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
