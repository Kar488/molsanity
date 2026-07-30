"""Generate every manuscript figure from the committed results/ folder.

    python paper/figs/make_figures.py

Reads results/RESULTS.md, results/BENCHMARK.md, results/PROGRESS.md and the
per-molecule records under results/artifacts/audit/ through ``msdata`` — no
number is typed in here. Output: vector PDF in paper/figs/.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import msdata as D  # noqa: E402
from style import (ACCENT, ATTRIBUTOR_COLOR, ATTRIBUTOR_MARKER, BACKBONE_COLOR,  # noqa: E402
                   GT_COLOR, INK, MUTED, REGIME_COLOR, SHORT, despine,
                   panel_label, save, use_style)

use_style()

CLS, REG = D.load_results()
ROWS = list(CLS) + list(REG)
BENCH = D.load_benchmark()
RECS = D.load_records()

DATASET_ORDER = ["SynthMotifs", "SynthMotifsXL", "MUTAG", "BBBP", "BACE",
                 "ClinTox", "SIDER", "Tox21", "DILI", "hERG",
                 "ESOL", "FreeSolv", "Lipophilicity"]
ATTR_ORDER = ["IntegratedGradients", "Saliency", "InputXGradient",
              "GuidedBackprop", "GNNExplainer", "PGExplainer"]
ARMS = [("MUTAG", "GINE"), ("SynthMotifs", "GINE")]
# The backbone sweep is read off the exact-ground-truth arm; must stay in step
# with ``bb_ds`` in make_tables.py, which defines the \bb* macros quoted in the
# caption and in the prose.
BB_DATASET = "SynthMotifs"
CARRIED_EDGE = "#4b5563"


def gt_kind(dataset: str) -> str:
    return "exact" if dataset in D.GT_EXACT else "proxy"


# ---------------------------------------------------------------- figure 1
def fig_faithfulness_correctness(out: Path):
    with_gt = [r for r in CLS if r["gt_auroc"] is not None
               and r["occ_spearman"] is not None]
    no_gt = [r for r in ROWS if r.get("gt_auroc") is None
             and r["occ_spearman"] is not None]

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 3.15),
                             gridspec_kw={"width_ratios": [1.35, 1.0]})
    ax = axes[0]
    ax.axhspan(0, 0.5, color="#f3f4f6", zorder=0)
    ax.axhline(0.5, color=MUTED, lw=0.7, ls="--", zorder=1)
    ax.axvline(0.0, color=MUTED, lw=0.7, ls=":", zorder=1)
    ax.text(0.015, 0.507, "chance localisation", transform=ax.get_yaxis_transform(),
            ha="left", va="bottom", fontsize=6.2, color=MUTED)
    ax.text(0.015, 0.487, "anti-aligned with ground truth",
            transform=ax.get_yaxis_transform(), ha="left", va="top",
            fontsize=6.2, color=MUTED)

    for r in with_gt:
        carried = r["provenance"] == "carried"
        ax.scatter(r["occ_spearman"], r["gt_auroc"],
                   marker=ATTRIBUTOR_MARKER.get(r["attributor"], "o"),
                   s=40, linewidths=0.9 if carried else 0.7,
                   facecolor="none" if carried else GT_COLOR[gt_kind(r["dataset"])],
                   edgecolor=GT_COLOR[gt_kind(r["dataset"])] if carried else "white",
                   alpha=0.95, zorder=3)

    def find(ds, bb, at, sp):
        for r in with_gt:
            if D.cell_key(r) == (ds, bb, at, sp):
                return r
        return None

    for r, label, off in [
        (find("SynthMotifs", "GINE", "Saliency", "scaffold"), "Synth·Sal (shift)", (20, -14)),
        (find("SynthMotifs", "GINE", "IntegratedGradients", "scaffold"), "Synth·IG (shift)", (24, 8)),
        (find("MUTAG", "GINE", "Saliency", "scaffold"), "MUTAG·Saliency", (24, 12)),
        (find("MUTAG", "GINE", "IntegratedGradients", "scaffold"), "MUTAG·IG", (14, 16)),
    ]:
        if r is None:
            continue
        ax.annotate(label, (r["occ_spearman"], r["gt_auroc"]),
                    textcoords="offset points", xytext=off, fontsize=6.2,
                    color=INK,
                    arrowprops=dict(arrowstyle="-", lw=0.5, color=MUTED,
                                    shrinkA=0, shrinkB=2))

    ax.set_xlabel("occlusion faithfulness  (Spearman $\\rho$, higher = more faithful)")
    ax.set_ylabel("ground-truth localisation (AUROC)")
    ax.set_ylim(-0.03, 1.07)
    ax.grid(lw=0.4, alpha=0.6)
    ax.set_axisbelow(True)
    despine(ax)
    panel_label(ax, "a")

    h_gt = [plt.Line2D([], [], ls="", marker="o", ms=5, mfc=GT_COLOR["exact"],
                       mec="white", label="exact node GT (synthetic)"),
            plt.Line2D([], [], ls="", marker="o", ms=5, mfc=GT_COLOR["proxy"],
                       mec="white", label="motif-proxy GT (MUTAG)"),
            plt.Line2D([], [], ls="", marker="o", ms=5, mfc="none",
                       mec=CARRIED_EDGE, label="carried from earlier run")]
    h_at = [plt.Line2D([], [], ls="", marker=ATTRIBUTOR_MARKER[a], ms=4.5,
                       mfc="0.45", mec="white", label=SHORT[a])
            for a in ATTR_ORDER if any(r["attributor"] == a for r in with_gt)]
    leg1 = ax.legend(handles=h_gt, loc="lower left", handletextpad=0.3,
                     borderpad=0.2, labelspacing=0.25)
    ax.add_artist(leg1)
    ax.legend(handles=h_at, loc="upper left", ncol=2, handletextpad=0.3,
              columnspacing=0.9, borderpad=0.2, labelspacing=0.25)

    ax = axes[1]
    regimes = ["classification", "regression"]
    rng = np.random.default_rng(0)
    for i, reg in enumerate(regimes):
        vals = [r["occ_spearman"] for r in no_gt if r["regime"] == reg]
        y = i + rng.uniform(-0.16, 0.16, size=len(vals))
        ax.scatter(vals, y, s=20, alpha=0.75, linewidths=0.5,
                   color=REGIME_COLOR[reg], edgecolor="white", zorder=3)
        med = float(np.median(vals))
        ax.plot([med, med], [i - 0.24, i + 0.24], color=INK, lw=1.4, zorder=4)
        ax.text(med, i + 0.29, f"median {med:.2f}", ha="center", fontsize=6.3,
                color=INK)
        ax.text(-1.12, i + 0.52, f"{reg}  (n={len(vals)} cells)", fontsize=6.8,
                color=REGIME_COLOR[reg], va="center")
    ax.axvline(0.0, color=MUTED, lw=0.7, ls=":")
    ax.set_yticks([])
    ax.set_ylim(-0.62, 1.85)
    ax.set_xlim(-1.15, 1.12)
    ax.set_xlabel("occlusion faithfulness  (Spearman $\\rho$)")
    ax.set_title("cells with no ground truth", fontsize=7.6, color=INK, pad=6)
    ax.grid(axis="x", lw=0.4, alpha=0.6)
    ax.set_axisbelow(True)
    despine(ax, keep=("bottom",))
    panel_label(ax, "b", dx=-0.03)

    fig.subplots_adjust(wspace=0.22)
    save(fig, out)


# ---------------------------------------------------------------- figure 2
def fig_dissociation(out: Path):
    marks = {"occ_spearman": "occlusion $\\rho$", "fidelity_plus": "Fidelity+",
             "characterization": "charact."}
    fig, axes = plt.subplots(len(ARMS), 2, figsize=(7.1, 2.5 * len(ARMS)))
    for row, (ds, bb) in enumerate(ARMS):
        for col, (sp, title) in enumerate([("random", "in-distribution"),
                                           ("scaffold", "scaffold shift")]):
            ax = axes[row][col]
            sel = D.selection_test(ds, bb, sp)
            if sel is None:
                ax.axis("off")
                continue
            pa = sel["per_attributor"]
            attrs = sorted(pa, key=lambda a: pa[a]["gt_auroc_mean"], reverse=True)
            y = np.arange(len(attrs))
            vals = [pa[a]["gt_auroc_mean"] for a in attrs]
            lo = [v - pa[a]["gt_auroc_ci"][0] for v, a in zip(vals, attrs)]
            hi = [pa[a]["gt_auroc_ci"][1] - v for v, a in zip(vals, attrs)]
            ax.barh(y, vals, height=0.62, xerr=[lo, hi], zorder=3,
                    color=[ATTRIBUTOR_COLOR[a] for a in attrs], alpha=0.9,
                    error_kw=dict(lw=0.7, ecolor="#3f4653", capsize=1.6))
            ax.axvline(0.5, color=MUTED, lw=0.8, ls="--", zorder=4)
            for i, a in enumerate(attrs):
                v = pa[a]["gt_auroc_mean"]
                inside = v > 0.24
                ax.text(v - 0.02 if inside else v + 0.03, i, f"{v:.3f}",
                        va="center", ha="right" if inside else "left",
                        fontsize=5.9, color="white" if inside else INK, zorder=5)
            ax.set_yticks(y)
            ax.set_yticklabels([SHORT[a] for a in attrs], fontsize=6.2)
            ax.invert_yaxis()
            ax.set_xlim(0, 1.85)
            ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
            nmol = max(v["n_mol"] for v in pa.values())
            ax.set_title(f"{ds}·{bb}: {title}, $n$={nmol}", fontsize=7.0, pad=6)
            if row == len(ARMS) - 1:
                ax.set_xlabel("ground-truth localisation (AUROC)")
            ax.grid(axis="x", lw=0.4, alpha=0.6)
            ax.set_axisbelow(True)
            despine(ax)
            ax.tick_params(axis="y", length=0)

            picks: dict[str, list] = {}
            for x in sel["selections"]:
                tag = marks[x["faithfulness_metric"]]
                if x["mismatch"]:
                    pv = x["paired_gt_pvalue"]
                    tag += "*" if (pv is not None and pv < 0.05) else "†"
                picks.setdefault(x["faithfulness_pick"], []).append(tag)
            for a, labels in picks.items():
                i = attrs.index(a)
                sig = any(t.endswith("*") for t in labels)
                body = (", ".join(labels[:2]) + ",\n" + ", ".join(labels[2:])
                        if len(labels) > 2 else ", ".join(labels))
                ax.annotate("← ranked 1st by\n" + body, (1.08, i), fontsize=5.5,
                            color="#8B1A1A" if sig else MUTED, va="center",
                            linespacing=1.25)
            rc = sel["rank_correlation"]
            txt = " · ".join(f"{marks[k]} {v['rho']:+.2f}" for k, v in rc.items())
            ax.text(0.0, -0.22 if row < len(ARMS) - 1 else -0.42,
                    "faithfulness↔truth rank corr.:  " + txt,
                    transform=ax.transAxes, fontsize=5.7, color=INK, va="top")
    for row in range(len(ARMS)):
        panel_label(axes[row][0], "ab"[row] if len(ARMS) == 2 else str(row),
                    dx=-0.26, dy=1.20)
    axes[-1][1].text(0.0, -0.60,
                     "*  selected attributor is significantly worse than the "
                     "ground-truth-best  ·  † mismatch, not significant",
                     transform=axes[-1][1].transAxes, ha="left", fontsize=5.7,
                     color="#8B1A1A")
    fig.subplots_adjust(wspace=0.62, hspace=0.78, bottom=0.19, top=0.92)
    save(fig, out)


# ---------------------------------------------------------------- figure 3
def fig_heatmaps(out: Path):
    """Faithfulness over the whole grid; correctness only where it exists.

    Rendering the correctness panel at full height would be ten rows of dashes.
    The asymmetry between the two panels *is* the finding, so it is drawn once
    and stated, rather than repeated as absent cells.
    """
    rows = [r for r in ROWS if r["backbone"] == "GINE" and r["split"] == "scaffold"]
    datasets = [d for d in DATASET_ORDER if any(r["dataset"] == d for r in rows)]
    attrs = [a for a in ATTR_ORDER if any(r["attributor"] == a for r in rows)]
    idx = {(r["dataset"], r["attributor"]): r for r in rows}
    gt_sets = [d for d in datasets
               if any(idx.get((d, a), {}).get("gt_auroc") is not None for a in attrs)]

    def draw(ax, dsets, metric, lo, hi, mid, title, value_fs):
        M = np.full((len(dsets), len(attrs)), np.nan)
        for i, d in enumerate(dsets):
            for j, a in enumerate(attrs):
                r = idx.get((d, a))
                if r is not None and r.get(metric) is not None:
                    M[i, j] = r[metric]
        norm = plt.matplotlib.colors.TwoSlopeNorm(vmin=lo, vcenter=mid, vmax=hi)
        ax.set_facecolor("#eef0f3")
        im = ax.imshow(M, cmap="RdBu_r", norm=norm, aspect="auto")
        for i, d in enumerate(dsets):
            for j, a in enumerate(attrs):
                v, r = M[i, j], idx.get((d, a))
                if np.isnan(v):
                    ax.text(j, i, "–" if r is not None else "", ha="center",
                            va="center", fontsize=7, color="#a7aeb8")
                    continue
                shade = abs(norm(v) - 0.5) * 2
                ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                        fontsize=value_fs, color="white" if shade > 0.62 else INK)
                if r["provenance"] == "carried":
                    ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False,
                                               lw=0.6, edgecolor="#aeb5bf", zorder=4))
        ax.set_xticks(range(len(attrs)))
        ax.set_xticklabels([SHORT[a] for a in attrs], rotation=38, ha="right",
                           fontsize=7.0)
        ax.set_yticks(range(len(dsets)))
        ax.set_yticklabels(dsets, fontsize=7.0)
        ax.set_title(title, fontsize=8.0, pad=6)
        ax.tick_params(length=0)
        for sp in ax.spines.values():
            sp.set_visible(False)
        return im

    fig = plt.figure(figsize=(7.1, 3.3))
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1],
                          height_ratios=[len(gt_sets), len(datasets) - len(gt_sets)],
                          wspace=0.42, hspace=0.0)
    axA = fig.add_subplot(gs[:, 0])
    axB = fig.add_subplot(gs[0, 1])

    imA = draw(axA, datasets, "occ_spearman", -1.0, 1.0, 0.0,
               "occlusion faithfulness (Spearman $\\rho$)", 6.6)
    imB = draw(axB, gt_sets, "gt_auroc", 0.0, 1.0, 0.5,
               "ground-truth localisation (AUROC)", 7.2)

    for ax, im, asp in ((axA, imA, 44), (axB, imB, 8)):
        cb = fig.colorbar(im, ax=ax, fraction=0.040, pad=0.02, aspect=asp)
        cb.ax.tick_params(labelsize=6.6, length=2)
        cb.outline.set_visible(False)

    note = fig.add_subplot(gs[1, 1]); note.axis("off")
    note.text(0.0, 0.70, "Panel b stops after two rows.",
              transform=note.transAxes, ha="left", va="top", fontsize=7.0,
              color=INK, weight="bold")
    note.text(0.0, 0.58,
              f"Of the {len(datasets)} datasets audited, {len(gt_sets)} carry "
              "node-level labels\nagainst which an attribution can be scored. "
              f"For the other\n{len(datasets) - len(gt_sets)}, every real "
              "molecular property dataset in the sweep,\nno such labels are "
              "published, so only panel a can\nbe computed at all. "
              "Faithfulness is auditable\neverywhere; correctness almost "
              "nowhere.",
              transform=note.transAxes, ha="left", va="top", fontsize=6.6,
              color=INK, linespacing=1.5)
    panel_label(axA, "a", dx=-0.22, dy=1.06)
    panel_label(axB, "b", dx=-0.22, dy=1.30)
    save(fig, out)


# ---------------------------------------------------------------- figure 4
def fig_backbone(out: Path):
    ds = BB_DATASET
    panels = [(ds, "random", "in-distribution (random split)"),
              (ds, "scaffold", "scaffold shift")]
    fig, axes = plt.subplots(2, 1, figsize=(3.3, 3.5))
    for ax, (dset, sp, sub) in zip(axes, panels):
        rows = [r for r in CLS if r["dataset"] == dset and r["split"] == sp
                and r["attributor"] == "IntegratedGradients"
                and r["gt_auroc"] is not None]
        rows.sort(key=lambda r: r["gt_auroc"])
        y = np.arange(len(rows))
        ax.barh(y, [r["gt_auroc"] for r in rows], height=0.62,
                color=[BACKBONE_COLOR.get(r["backbone"], ACCENT) for r in rows],
                alpha=0.9, zorder=3)
        ax.axvline(0.5, color=MUTED, lw=0.8, ls="--", zorder=4)
        for i, r in enumerate(rows):
            ax.text(r["gt_auroc"] + 0.015, i, f"{r['gt_auroc']:.2f}", va="center",
                    fontsize=6.4, color=INK)
        ax.set_yticks(y)
        ax.set_yticklabels([r["backbone"] for r in rows], fontsize=6.8)
        ax.set_xlim(0, 1.12)
        ax.set_title(f"{dset} · Integrated Gradients · {sub}", fontsize=7.2, pad=4)
        ax.grid(axis="x", lw=0.4, alpha=0.6)
        ax.set_axisbelow(True)
        despine(ax)
        ax.tick_params(axis="y", length=0)
    axes[1].set_xlabel("ground-truth localisation (AUROC)")
    panel_label(axes[0], "a", dx=-0.30, dy=1.22)
    panel_label(axes[1], "b", dx=-0.30, dy=1.22)
    fig.subplots_adjust(hspace=0.55)
    save(fig, out)


# ---------------------------------------------------------------- figure 5
def fig_distributions(out: Path):
    fig, axes = plt.subplots(1, 3, figsize=(7.1, 2.35))
    rng = np.random.default_rng(1)

    ax = axes[0]
    regimes = ["synthetic", "classification", "regression"]
    for i, reg in enumerate(regimes):
        vals = [r["occ_spearman"] for r in ROWS
                if r["regime"] == reg and r["occ_spearman"] is not None]
        x = i + rng.uniform(-0.17, 0.17, len(vals))
        ax.scatter(x, vals, s=13, alpha=0.7, color=REGIME_COLOR[reg],
                   edgecolor="white", linewidths=0.4, zorder=3)
        med = float(np.median(vals))
        ax.plot([i - 0.3, i + 0.3], [med, med], color=INK, lw=1.3, zorder=4)
        ax.text(i, 1.12, f"n={len(vals)}", ha="center", fontsize=6.0, color=MUTED)
    ax.axhline(0, color=MUTED, lw=0.7, ls=":")
    ax.set_xticks(range(3))
    ax.set_xticklabels(["synthetic", "classif.", "regression"], fontsize=6.6)
    ax.set_ylim(-1.05, 1.2)
    ax.set_ylabel("occlusion faithfulness ($\\rho$)")
    ax.grid(axis="y", lw=0.4, alpha=0.6)
    ax.set_axisbelow(True)
    despine(ax)
    panel_label(ax, "a", dx=-0.26)

    # (b) what the scaffold split does to faithfulness, paired within cell
    ax = axes[1]
    pairs = []
    for k in RECS:
        if k[3] != "scaffold":
            continue
        other = (k[0], k[1], k[2], "random")
        if other in RECS:
            a = D.cell_mean(RECS[k], "occ_spearman")
            b = D.cell_mean(RECS[other], "occ_spearman")
            if not math.isnan(a) and not math.isnan(b):
                pairs.append((k[0], b, a))
    for ds_, b, a in pairs:
        ax.plot([0, 1], [b, a], color=REGIME_COLOR[D.regime_of(ds_)],
                lw=0.8, alpha=0.55, zorder=2)
        ax.scatter([0, 1], [b, a], s=9, zorder=3, linewidths=0,
                   color=REGIME_COLOR[D.regime_of(ds_)], alpha=0.8)
    if pairs:
        for xi, vals in ((0, [p[1] for p in pairs]), (1, [p[2] for p in pairs])):
            med = float(np.median(vals))
            ax.plot([xi - 0.16, xi + 0.16], [med, med], color=INK, lw=1.6, zorder=5)
            ax.text(xi, med + 0.07, f"{med:+.2f}", ha="center", fontsize=6.2,
                    color=INK, zorder=6)
    ax.axhline(0, color=MUTED, lw=0.7, ls=":")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["random\n(in-dist.)", "scaffold\n(shift)"], fontsize=6.4)
    ax.set_xlim(-0.35, 1.35)
    ax.set_ylabel("occlusion faithfulness ($\\rho$)")
    ax.set_title(f"same cell, both splits ($n$={len(pairs)})", fontsize=7.0, pad=4)
    ax.grid(axis="y", lw=0.4, alpha=0.6)
    ax.set_axisbelow(True)
    despine(ax)
    panel_label(ax, "b", dx=-0.26)

    ax = axes[2]
    attrs = [a for a in ATTR_ORDER
             if any(r["attributor"] == a and r["stability"] is not None
                    for r in BENCH)]
    for i, a in enumerate(attrs):
        vals = [r["stability"] for r in BENCH
                if r["attributor"] == a and r["stability"] is not None]
        x = i + rng.uniform(-0.17, 0.17, len(vals))
        ax.scatter(x, vals, s=13, alpha=0.7, color=ATTRIBUTOR_COLOR[a],
                   edgecolor="white", linewidths=0.4, zorder=3)
        med = float(np.median(vals))
        ax.plot([i - 0.3, i + 0.3], [med, med], color=INK, lw=1.3, zorder=4)
    ax.set_xticks(range(len(attrs)))
    ax.set_xticklabels([SHORT[a] for a in attrs], rotation=38, ha="right",
                       fontsize=6.2)
    ax.set_ylabel("cross-checkpoint stability ($\\rho$)")
    ax.grid(axis="y", lw=0.4, alpha=0.6)
    ax.set_axisbelow(True)
    despine(ax)
    panel_label(ax, "c", dx=-0.26)

    fig.subplots_adjust(wspace=0.42)
    save(fig, out)


# ---------------------------------------------------------------- figure 6
def fig_regime(out: Path):
    """Regime stratification + per-cell calibration linkage (both newly
    computable: this run committed its per-molecule records)."""
    pooled: dict[str, list] = {}
    for recs in RECS.values():
        for r in recs:
            pooled.setdefault(r.get("regime", "?"), []).append(r)
    order = ["confident_correct", "confident_error", "borderline"]
    labels = ["confident\ncorrect", "confident\nerror", "borderline"]
    colors = ["#0072B2", "#D55E00", "#9aa2ad"]

    fig, axes = plt.subplots(1, 3, figsize=(7.1, 2.3))

    for ax, (field, name, chance) in zip(
            axes[:2], [("occ_spearman", "occlusion faithfulness ($\\rho$)", 0.0),
                       ("gt_auroc", "ground-truth localisation (AUROC)", 0.5)]):
        means, ns = [], []
        for reg in order:
            vals = [r[field] for r in pooled.get(reg, [])
                    if r.get(field) is not None and not math.isnan(r[field])]
            means.append(float(np.mean(vals)) if vals else np.nan)
            ns.append(len(vals))
        x = np.arange(len(order))
        ax.bar(x, means, width=0.6, color=colors, alpha=0.9, zorder=3)
        ax.axhline(chance, color=MUTED, lw=0.8, ls="--", zorder=4)
        span = max(abs(np.nanmax(means) - chance), abs(np.nanmin(means) - chance))
        for i, (m, nn) in enumerate(zip(means, ns)):
            if np.isnan(m):
                continue
            up = m >= chance
            ax.text(i, m + (0.06 * span if up else -0.06 * span),
                    f"{m:.2f}\nn={nn}", ha="center",
                    va="bottom" if up else "top",
                    fontsize=6.0, color=INK, linespacing=1.25)
        lo_y = min(np.nanmin(means), chance) - 0.42 * span
        hi_y = max(np.nanmax(means), chance) + 0.42 * span
        ax.set_ylim(lo_y, hi_y)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=6.4)
        ax.set_ylabel(name)
        ax.grid(axis="y", lw=0.4, alpha=0.6)
        ax.set_axisbelow(True)
        despine(ax)
    panel_label(axes[0], "a", dx=-0.28)
    panel_label(axes[1], "b", dx=-0.28)

    ax = axes[2]
    links = []
    for k, recs in RECS.items():
        if D.regime_of(k[0]) == "regression":
            continue
        cl = D.calibration_linkage(recs)
        if not math.isnan(cl["spearman"]):
            links.append((k, cl))
    rng = np.random.default_rng(3)
    for k, cl in links:
        sig = cl["pvalue"] < 0.05
        ax.scatter(rng.uniform(-0.18, 0.18), cl["spearman"], s=16,
                   color=REGIME_COLOR[D.regime_of(k[0])],
                   alpha=0.9 if sig else 0.35,
                   edgecolor="white" if sig else "none", linewidths=0.4, zorder=3)
    vals = [cl["spearman"] for _, cl in links]
    med = float(np.median(vals))
    ax.plot([-0.3, 0.3], [med, med], color=INK, lw=1.5, zorder=5)
    ax.text(0.34, med, f"median {med:+.2f}", fontsize=6.2, va="center", color=INK)
    ax.axhline(0, color=MUTED, lw=0.7, ls=":")
    pooled_rho = D.calibration_linkage(
        [r for k, v in RECS.items() if D.regime_of(k[0]) != "regression"
         for r in v])["spearman"]
    ax.scatter([0], [pooled_rho], marker="*", s=90, color="#8B1A1A", zorder=6)
    ax.text(0.06, pooled_rho, f" pooled {pooled_rho:+.2f}", fontsize=6.2,
            va="center", color="#8B1A1A")
    ax.set_xlim(-0.55, 1.15)
    ax.set_xticks([])
    ax.set_ylabel("calibration linkage $\\rho$")
    ax.set_title(f"per cell ($n$={len(links)}); solid = $p<0.05$",
                 fontsize=6.8, pad=4)
    ax.grid(axis="y", lw=0.4, alpha=0.6)
    ax.set_axisbelow(True)
    despine(ax, keep=("left",))
    panel_label(ax, "c", dx=-0.28)

    fig.subplots_adjust(wspace=0.45)
    save(fig, out)


# ---------------------------------------------------------------- coverage
def fig_coverage(out: Path):
    led = D.load_ledger()
    per: dict[str, dict] = {}
    for e in led:
        d = per.setdefault(e["dataset"], {"done": 0, "failed": 0, "skipped": 0})
        d[e["status"]] = d.get(e["status"], 0) + 1
    carried: dict[str, int] = {}
    for k in D.coverage()["carried_cells"]:
        carried[k[0]] = carried.get(k[0], 0) + 1
    datasets = [d for d in DATASET_ORDER if d in per or d in carried]
    datasets += sorted(set(per) | set(carried) - set(datasets) - set(DATASET_ORDER))
    datasets = list(dict.fromkeys(datasets))

    fig, ax = plt.subplots(figsize=(3.3, 3.0))
    keys = [("done", "#1f5c9e"), ("failed", "#c0392b"), ("skipped", "#9aa2ad")]
    y = np.arange(len(datasets))
    left = np.zeros(len(datasets))
    for status, colour in keys:
        vals = np.array([per.get(d, {}).get(status, 0) for d in datasets],
                        dtype=float)
        ax.barh(y, vals, left=left, height=0.66, color=colour, alpha=0.92,
                label=status, zorder=3)
        for i, v in enumerate(vals):
            if v:
                ax.text(left[i] + v / 2, i, f"{int(v)}", ha="center", va="center",
                        fontsize=5.8, color="white")
        left += vals
    for i, d in enumerate(datasets):
        c = carried.get(d, 0)
        if c:
            ax.text(left[i] + 0.35, i, f"+{c}\\,c", va="center", fontsize=5.8,
                    color=MUTED)
    ax.set_yticks(y)
    ax.set_yticklabels(datasets, fontsize=6.8)
    ax.invert_yaxis()
    ax.set_xlabel("cell-runs attempted in this run")
    ax.legend(loc="lower right", fontsize=6.2, handlelength=1.0,
              handletextpad=0.4, borderpad=0.25)
    ax.grid(axis="x", lw=0.4, alpha=0.6)
    ax.set_axisbelow(True)
    despine(ax)
    ax.tick_params(axis="y", length=0)
    save(fig, out)


def copy_pipeline_figures():
    """Carry the pipeline's own qualitative figures into the manuscript.

    The attribution-overlay grids are rendered by the audit run itself (RDKit
    skeletal structures for molecules, node-link diagrams for the synthetic
    graphs, ground-truth motif outlined). They are copied rather than
    regenerated so the paper shows exactly what the pipeline produced.
    """
    import shutil
    src = D.RES / "figures" / "summary"
    for name in ("molgrid_MUTAG", "molgrid_SynthMotifs"):
        p = src / f"{name}.pdf"
        if p.exists():
            shutil.copy2(p, HERE / f"fig_{name}.pdf")
            print(f"  copied {p.name}")
        else:
            print(f"  MISSING {p} — the qualitative figure will not build")


if __name__ == "__main__":
    print("Generating figures from results/ …")
    fig_faithfulness_correctness(HERE / "fig_faith_correct.pdf")
    fig_dissociation(HERE / "fig_dissociation.pdf")
    fig_heatmaps(HERE / "fig_heatmaps.pdf")
    fig_backbone(HERE / "fig_backbone.pdf")
    fig_distributions(HERE / "fig_distributions.pdf")
    fig_regime(HERE / "fig_regime.pdf")
    fig_coverage(HERE / "fig_coverage.pdf")
    copy_pipeline_figures()
    print("done.")
