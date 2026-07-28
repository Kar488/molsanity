"""Cross-matrix publication figures built from the per-cell audit records.

These summarise the whole audit matrix (not a single cell): a head-to-head bar
of ground-truth localisation by attributor, faithfulness/stability ECDFs, and
regime-stratified reliability. All vector (PDF + SVG).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from ..utils import get_logger

log = get_logger()

_PALETTE = ["#2166ac", "#b2182b", "#1b7837", "#762a83", "#e08214", "#01665e"]


def _use_agg():
    import matplotlib

    matplotlib.use("Agg")


def _save(fig, out_path: Path) -> dict:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pdf, svg = out_path.with_suffix(".pdf"), out_path.with_suffix(".svg")
    fig.savefig(pdf, bbox_inches="tight")
    fig.savefig(svg, bbox_inches="tight")
    import matplotlib.pyplot as plt

    plt.close(fig)
    return {"pdf": str(pdf), "svg": str(svg)}


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
    _use_agg()
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
    labels = [r[0] for r in rows]
    means = [r[1]["mean"] for r in rows]
    lo = [r[1]["mean"] - r[1]["lo"] for r in rows]
    hi = [r[1]["hi"] - r[1]["mean"] for r in rows]

    fig, ax = plt.subplots(figsize=(6, 3.4))
    y = np.arange(len(labels))
    ax.barh(y, means, xerr=[lo, hi], color=_PALETTE[0], alpha=0.85, capsize=3)
    ax.axvline(0.5, color="grey", ls="--", lw=1, label="chance")
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("Ground-truth AUROC (mean ± 95% CI)")
    ax.set_title(f"{dataset} · GINE · attribution vs ground truth ({split} split)")
    ax.legend(fontsize=7)
    fig.tight_layout()
    return _save(fig, Path(out_path))


def faithfulness_stability_ecdf(cells: dict, out_path, dataset="MUTAG", split="scaffold") -> dict | None:
    """ECDFs of occlusion faithfulness and cross-checkpoint stability per attributor."""
    _use_agg()
    import matplotlib.pyplot as plt

    series = {}
    for cid, recs in cells.items():
        m = _parse_cell_id(cid)
        if m["dataset"] == dataset and m["backbone"] == "GINE" and m["split"] == split:
            series[m["attributor"]] = recs
    if not series:
        return None

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    for i, (name, recs) in enumerate(sorted(series.items())):
        c = _PALETTE[i % len(_PALETTE)]
        x, y = _ecdf(_col(recs, "occ_spearman"))
        if x.size:
            axes[0].step(x, y, where="post", color=c, lw=1.8, label=name)
        xs, ys = _ecdf(_col(recs, "stability"))
        if xs.size:
            axes[1].step(xs, ys, where="post", color=c, lw=1.8, label=name)
    axes[0].axvline(0, color="grey", ls="--", lw=1)
    axes[0].set_xlabel("Occlusion faithfulness (Spearman)")
    axes[0].set_ylabel("Cumulative fraction")
    axes[0].set_title("A. Faithfulness ECDF")
    axes[0].legend(fontsize=7)
    axes[1].set_xlabel("Cross-checkpoint stability (Spearman)")
    axes[1].set_title("B. Stability ECDF")
    axes[1].legend(fontsize=7)
    fig.suptitle(f"{dataset} · GINE ({split} split)", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    return _save(fig, Path(out_path))


def regime_stratification_figure(cells: dict, out_path, split="scaffold") -> dict | None:
    """Reliability (GT AUROC, occlusion) stratified by confidence/correctness regime,
    pooled across all classification cells with the given split."""
    _use_agg()
    import matplotlib.pyplot as plt

    regimes = ["confident_correct", "confident_error", "borderline"]
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

    fig, ax = plt.subplots(figsize=(6, 3.6))
    x = np.arange(len(regimes))
    w = 0.38
    ax.bar(x - w / 2, gt, w, color=_PALETTE[0], label="GT AUROC")
    ax.bar(x + w / 2, occ, w, color=_PALETTE[1], label="Occlusion Spearman")
    ax.axhline(0.5, color="grey", ls="--", lw=1)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{r}\n(n={counts[r]})" for r in regimes], fontsize=8)
    ax.set_ylabel("Mean reliability")
    ax.set_title(f"Attribution reliability by regime ({split} split, pooled)")
    ax.legend(fontsize=7)
    fig.tight_layout()
    return _save(fig, Path(out_path))


def make_summary_figures(out_dir="artifacts/figures/_summary") -> dict:
    """Generate all cross-matrix figures from the discovered audit records."""
    from ..benchmark.tables import discover_cells

    cells = discover_cells()
    out_dir = Path(out_dir)
    made = {}
    if not cells:
        log.info("No audit cells found; skipping summary figures.")
        return made
    for name, fn in [
        ("attributor_gt_bar", lambda: attributor_gt_bar(cells, out_dir / "attributor_gt_bar")),
        ("faithfulness_stability_ecdf",
         lambda: faithfulness_stability_ecdf(cells, out_dir / "faithfulness_stability_ecdf")),
        ("regime_stratification",
         lambda: regime_stratification_figure(cells, out_dir / "regime_stratification")),
    ]:
        try:
            info = fn()
            if info:
                made[name] = info
                log.info("Wrote summary figure: %s", info["pdf"])
        except Exception as exc:  # noqa: BLE001
            log.warning("Summary figure %s failed: %s", name, exc)
    return made
