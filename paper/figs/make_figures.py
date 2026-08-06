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
                   GRID, GT_COLOR, INK, MUTED, REGIME_COLOR, SHORT, despine,
                   panel_label, save, use_style)

use_style()

CLS, REG = D.load_results()
ROWS = list(CLS) + list(REG)
BENCH = D.load_benchmark()
RECS = D.load_records()

DATASET_ORDER = ["SynthMotifs", "SynthMotifsXL", "BA-2Motifs", "ShapeGGen",
                 "MUTAG", "MolMotif", "MolMotifHard", "Benzene",
                 "FluorideCarbonyl", "BBBP", "BACE",
                 "ClinTox", "SIDER", "Tox21", "DILI", "hERG",
                 "ESOL", "FreeSolv", "Lipophilicity"]
# Figures filter by this list, so a dataset missing from it is silently absent
# from the heatmap while the ledger still counts it -- which is how Benzene and
# FluorideCarbonyl were audited, tabulated, and invisible in Figure 5. Anything
# in the results but not named above is appended rather than dropped.
DATASET_ORDER += sorted({r["dataset"] for r in ROWS} - set(DATASET_ORDER))
ATTR_ORDER = ["IntegratedGradients", "Saliency", "InputXGradient",
              "GuidedBackprop", "GNNExplainer", "PGExplainer", "SubgraphX"]
# Must mirror ARMS in make_tables.py: the molecular ground-truth arms, the only
# ones whose "scaffold" split is a chemical shift rather than an arbitrary
# deterministic partition. Panelling a non-molecular arm here would show a
# shift contrast the data cannot support.
ARMS = [("MUTAG", "GINE"), ("MolMotifHard", "GINE"), ("MolMotif", "GINE"),
        ("Benzene", "GINE"), ("FluorideCarbonyl", "GINE")]
# The backbone sweep is read off the exact-ground-truth arm; must stay in step
# with ``bb_ds`` in make_tables.py, which defines the \bb* macros quoted in the
# caption and in the prose.
BB_DATASET = "SynthMotifs"
CARRIED_EDGE = "#4b5563"


def gt_kind(dataset: str) -> str:
    """Which of the three kinds of node ground truth a dataset carries.

    The distinction the paper turns on is not exact-vs-proxy but whether an arm
    is exact *and* molecular: only a molecular arm has a Bemis-Murcko scaffold,
    so only a molecular arm can carry a shift contrast.
    """
    if dataset in D.GT_EXACT_MOL:
        return "exact-mol"
    if dataset in D.GT_EXACT_SYNTH:
        return "exact-synth"
    return "proxy"


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
    bandbox = dict(boxstyle="square,pad=0.12", fc="white", ec="none", alpha=0.82)
    ax.text(0.985, 0.507, "chance localisation", transform=ax.get_yaxis_transform(),
            ha="right", va="bottom", fontsize=6.2, color=MUTED, bbox=bandbox,
            zorder=6)
    ax.text(0.985, 0.487, "anti-aligned with ground truth",
            transform=ax.get_yaxis_transform(), ha="right", va="top",
            fontsize=6.2, color=MUTED, bbox=bandbox, zorder=6)

    for r in with_gt:
        carried = r["provenance"] == "carried"
        ax.scatter(r["occ_spearman"], r["gt_auroc"],
                   marker=ATTRIBUTOR_MARKER.get(r["attributor"], "o"),
                   s=26, linewidths=0.9 if carried else 0.5,
                   facecolor="none" if carried else GT_COLOR[gt_kind(r["dataset"])],
                   edgecolor=GT_COLOR[gt_kind(r["dataset"])] if carried else "white",
                   alpha=0.9, zorder=3)

    def find(ds, bb, at, sp):
        for r in with_gt:
            if D.cell_key(r) == (ds, bb, at, sp):
                return r
        return None

    # One exemplar per ground-truth kind, chosen to sit in the corners the
    # reader is asked to look at; the cloud is too dense for more than that.
    for r, label, off in [
        (find("MUTAG", "GINE", "Saliency", "scaffold"), "MUTAG·Saliency", (26, 10)),
        (find("MUTAG", "GINE", "IntegratedGradients", "scaffold"), "MUTAG·IG", (30, 4)),
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

    kinds = {gt_kind(r["dataset"]) for r in with_gt}
    labels = {"exact-mol": "exact node GT (molecular)",
              "exact-synth": "exact node GT (synthetic)",
              "proxy": "motif-proxy GT (MUTAG)"}
    h_gt = [plt.Line2D([], [], ls="", marker="o", ms=5, mfc=GT_COLOR[k],
                       mec="white", label=labels[k])
            for k in ("exact-mol", "exact-synth", "proxy") if k in kinds]
    # Only advertise the carried-row encoding when a carried row is on the plot.
    if any(r["provenance"] == "carried" for r in with_gt):
        h_gt.append(plt.Line2D([], [], ls="", marker="o", ms=5, mfc="none",
                               mec=CARRIED_EDGE, label="carried from earlier run"))
    h_at = [plt.Line2D([], [], ls="", marker=ATTRIBUTOR_MARKER[a], ms=4.5,
                       mfc="0.45", mec="white", label=SHORT[a])
            for a in ATTR_ORDER if any(r["attributor"] == a for r in with_gt)]
    # Both legends live under the figure: with every ground-truth cell on
    # panel (a) there is no in-axes gap left that a legend can occupy without
    # covering points.
    leg1 = fig.legend(handles=h_gt, loc="lower left", ncol=len(h_gt),
                      bbox_to_anchor=(0.055, -0.005), frameon=False,
                      handletextpad=0.3, columnspacing=1.1, fontsize=6.4)
    fig.add_artist(leg1)
    fig.legend(handles=h_at, loc="lower left", ncol=len(h_at),
               bbox_to_anchor=(0.055, -0.075), frameon=False,
               handletextpad=0.3, columnspacing=1.1, fontsize=6.4)

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

    fig.subplots_adjust(wspace=0.22, bottom=0.28)
    save(fig, out)


# ---------------------------------------------------------------- figure 2
def fig_dissociation(out: Path):
    marks = {"occ_spearman": "occlusion $\\rho$", "fidelity_plus": "Fidelity+",
             "characterization": "charact."}
    # One row per arm. Five arms at the natural row height overruns the text
    # block, so rows are compressed to fit a full-page float rather than
    # dropping an arm from the figure the caption enumerates.
    row_h = min(2.35, 8.55 / len(ARMS))
    fig, axes = plt.subplots(len(ARMS), 2, figsize=(7.1, row_h * len(ARMS)))
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
            # Two metrics can pick adjacent attributors, and a two- or
            # three-line callout is taller than one bar row, so anchoring each
            # note at its own row overlaps the note above it. Walk them in row
            # order, push any that would collide downward, and draw a leader
            # line so a displaced note still points at the bar it describes.
            notes = []
            for a, labels in picks.items():
                body = (", ".join(labels[:2]) + ",\n" + ", ".join(labels[2:])
                        if len(labels) > 2 else ", ".join(labels))
                text = "ranked 1st by\n" + body
                notes.append((attrs.index(a), text, text.count("\n") + 1,
                              any(t.endswith("*") for t in labels)))
            y_free = -1e9
            for i, text, n_lines, sig in sorted(notes):
                y = max(i, y_free + 0.55 * n_lines)
                ax.annotate(
                    text, xy=(1.02, i), xytext=(1.14, y), fontsize=5.5,
                    color="#8B1A1A" if sig else MUTED, va="center",
                    linespacing=1.25,
                    arrowprops=dict(arrowstyle="-", lw=0.5, shrinkA=1, shrinkB=1,
                                    color="#8B1A1A" if sig else MUTED,
                                    connectionstyle="arc3,rad=0"))
                y_free = y + 0.55 * n_lines
            rc = sel["rank_correlation"]
            txt = " · ".join(f"{marks[k]} {v['rho']:+.2f}" for k, v in rc.items())
            # The last row carries the x-axis label, so its correlation line
            # has to clear it; the others only clear the tick labels.
            ax.text(0.0, -0.24 if row < len(ARMS) - 1 else -0.62,
                    "faithfulness↔truth rank corr.:  " + txt,
                    transform=ax.transAxes, fontsize=5.7, color=INK, va="top")
    for row in range(len(ARMS)):
        panel_label(axes[row][0], "abcdef"[row], dx=-0.26, dy=1.20)
    axes[-1][1].text(0.0, -0.84,
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

    n_gt, n_no = len(gt_sets), len(datasets) - len(gt_sets)
    note = fig.add_subplot(gs[1, 1]); note.axis("off")
    # Panel b's rotated tick labels hang below its axes into this one, so the
    # note starts well down rather than at the top of its box.
    note.text(0.0, 0.66, f"Panel b stops after {n_gt} rows.",
              transform=note.transAxes, ha="left", va="top", fontsize=7.0,
              color=INK, weight="bold")
    note.text(0.0, 0.53,
              f"Of the {len(datasets)} datasets audited, {n_gt} carry node-level "
              f"labels\nagainst which an attribution can be scored. The other "
              f"{n_no}\nare the real molecular property datasets, for which no\n"
              "such labels are published, so only panel a can be\ncomputed at "
              "all. Faithfulness is auditable everywhere;\ncorrectness only "
              "where a benchmark was built for it.",
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


def fig_abstention(out: Path):
    """Coverage-reliability curves: the selective-prediction view of trust.

    Uses the package implementation of the curves rather than recomputing them,
    so this figure, ABSTENTION.md and the macros cannot disagree.
    """
    sys.path.insert(0, str(HERE.parents[1]))
    from molsanity.audit.abstention import rank_signals

    ranked = rank_signals([r for recs in RECS.values() for r in recs])
    if not ranked:
        print("  SKIP fig_abstention (no records carry a signal and ground truth)")
        return

    LABEL = {"confidence": "confidence", "rationale_reliance": "rationale reliance",
             "occ_spearman": "occlusion faith.", "stability": "stability",
             "motif_top1_share": "motif top-1 share"}
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.9))
    for i, r in enumerate(ranked):
        cov = [pt["coverage"] for pt in r["curve"]]
        # The best signal and any anti-predictive one are the two the text
        # argues from, so they carry the ink; the rest are context.
        neg = r["lift"] <= 0
        best = i == 0
        style = dict(lw=2.0, zorder=4, color=ACCENT) if best else (
            dict(lw=1.8, zorder=4, color="#c0392b", ls="--") if neg else
            dict(lw=1.0, zorder=2, color=MUTED, alpha=0.75))
        lab = LABEL.get(r["signal"], r["signal"])
        axes[0].plot(cov, [pt["mean_target"] for pt in r["curve"]],
                     label=lab, **style)
        axes[1].plot(cov, [pt["frac_below_chance"] for pt in r["curve"]],
                     label=lab, **style)

    axes[0].axhline(0.5, color=INK, lw=0.7, ls=":", zorder=1)
    axes[0].set_ylabel("mean GT AUROC of retained")
    axes[1].set_ylabel("fraction below chance")
    for ax, lbl in zip(axes, "ab"):
        ax.set_xlabel("coverage (fraction of molecules retained)")
        ax.invert_xaxis()  # left-to-right = abstaining more
        despine(ax)
        panel_label(ax, lbl)
    axes[0].legend(frameon=False, fontsize=6.2, loc="lower left", ncol=1)
    fig.tight_layout()
    save(fig, out)


def fig_lead(out: Path):
    """The claim and its scope in one view, before any qualification.

    Form follows the two jobs. Panels (a) and (b) are a RELATIONSHIP question --
    does faithfulness track correctness -- so they are scatters of the two axes
    against each other, one per regime. Panel (c) is a MAGNITUDE question over
    four fits -- how much of the pooled effect survives dropping each arm -- so
    it is a dot plot, not a third scatter.

    Putting (c) beside (a) and (b) is the whole point: a reader meets the effect
    and the fact that one dataset carries it at the same moment, rather than
    finding the second three pages later among the caveats.

    Layout choices come from looking at the first render, not from assuming. The
    correlation sits in each panel TITLE because every in-panel position for it
    collided with data, and the legend is one figure-level row above the
    scatters because both panels are occupied corner to corner.
    """
    MOL, ARM_COLOR, ARM_MARKER = D.MOLECULAR_GT, D.ARM_COLOR, D.ARM_MARKER

    cells = {}
    for r in CLS:
        if r["dataset"] not in MOL:
            continue
        g, o = r.get("gt_auroc"), r.get("occ_spearman")
        if g is None or o is None:
            continue
        cells.setdefault((r["dataset"], r["backbone"], r["attributor"]), {})[r["split"]] = (g, o)
    paired = {k: v for k, v in cells.items() if {"random", "scaffold"} <= set(v)}
    if len(paired) < 8:
        print("  SKIP fig_lead (too few paired molecular cells)")
        return
    ks = sorted(paired)

    fig, axes = plt.subplots(
        1, 3, figsize=(7.1, 2.9), constrained_layout=True,
        gridspec_kw={"width_ratios": [1, 1, 1.35]})

    handles = []
    for ax, split, title in zip(axes[:2], ("random", "scaffold"),
                                ("In distribution", "Under scaffold shift")):
        for ds in MOL:
            sub = [k for k in ks if k[0] == ds]
            if not sub:
                continue
            h, = ax.plot([paired[k][split][1] for k in sub],
                         [paired[k][split][0] for k in sub],
                         ARM_MARKER[ds], ms=4.6, mfc=ARM_COLOR[ds], mec="white",
                         mew=0.6, ls="none", label=ds, zorder=3)
            if split == "random":
                handles.append(h)
        rho, pv = D.spearman([paired[k][split][1] for k in ks],
                             [paired[k][split][0] for k in ks])
        ax.axhline(0.5, color=MUTED, lw=0.7, ls=":", zorder=1)
        ax.axvline(0.0, color=MUTED, lw=0.7, ls=":", zorder=1)
        ax.set_xlim(-0.9, 1.0)
        ax.set_ylim(-0.05, 1.08)
        ax.set_xlabel("occlusion faithfulness  $\\rho$")
        ax.set_title(f"{title}\n$\\rho$ = {rho:+.3f},  $p$ = {pv:.3f}",
                     fontsize=7.8, color=INK, pad=5)
        despine(ax)
    axes[0].set_ylabel("ground-truth localisation\n(GT AUROC)")
    axes[1].set_yticklabels([])

    # (c) leave-one-out: the scope of the claim, beside the claim.
    ax = axes[2]
    present = [ds for ds in MOL if any(k[0] == ds for k in ks)]
    fits = [(f"all {len(present)} arms", ks, INK)]
    for ds in present:
        fits.append((f"without {ds}", [k for k in ks if k[0] != ds], ARM_COLOR[ds]))
    drawn = []
    for y, (label, keys, colour) in enumerate(fits):
        if len(keys) < 8:
            continue
        rho, pv = D.spearman([paired[k]["scaffold"][1] for k in keys],
                             [paired[k]["scaffold"][0] for k in keys])
        sig = pv < 0.05
        ax.plot([rho], [y], "o", ms=7.4 if sig else 6.6,
                mfc=colour if sig else "white", mec=colour, mew=1.5, zorder=3)
        ax.text(rho, y - 0.3, f"{rho:+.2f}" + ("*" if sig else ""),
                va="bottom", ha="center", fontsize=6.9, color=INK)
        drawn.append(rho)
    ax.axvline(0, color=MUTED, lw=0.7, ls=":", zorder=1)
    ax.set_yticks(range(len(fits)))
    ax.set_yticklabels([f[0] for f in fits], fontsize=7.0)
    ax.set_ylim(len(fits) - 0.5, -0.75)
    # Limits follow the fits. Hard-coding them clipped a leave-one-out estimate
    # the moment one turned positive, which is the case a reader most needs to
    # see: dropping the arm that reverses the sign of the pooled coefficient.
    if drawn:
        lo, hi = min(drawn), max(drawn)
        pad = max(0.12, 0.22 * (hi - lo))
        ax.set_xlim(lo - pad, hi + pad)
    ax.set_xlabel("scaffold-split $\\rho$   ($*$ $p<0.05$)")
    ax.set_title("What the pooled estimate rests on", fontsize=7.8, color=INK,
                 pad=5)
    despine(ax)

    fig.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.055, 0.955),
               ncol=3, frameon=False, fontsize=6.8, handletextpad=0.3,
               columnspacing=1.2)
    for ax, lbl in zip(axes, "abc"):
        panel_label(ax, lbl)
    save(fig, out)


# ---------------------------------------------------------------- figure 0
def fig_overview(out: Path):
    """What the audit does, before any notation.

    The manuscript went from related work straight into notation, which asks a
    reader to hold the whole design in their head before being shown its shape.
    This is the shape: one cell is audited on axes that describe the model, and
    -- only where per-atom labels exist -- on one axis that describes the
    chemistry. The asymmetry between those two columns is the paper.

    Drawn from the results rather than annotated by hand: the cell counts, the
    ground-truth coverage and the selection tally are read off the same
    artifacts every other figure uses, so this cannot describe a different run
    from the one reported.
    """
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

    n_cells = len({(r["dataset"], r["backbone"], r["attributor"], r["split"])
                   for r in ROWS})
    n_gt = sum(1 for r in ROWS if r.get("gt_auroc") is not None)
    n_nogt = n_cells - n_gt
    n_ds = len({r["dataset"] for r in ROWS})
    n_bb = len({r["backbone"] for r in ROWS})
    n_at = len({r["attributor"] for r in ROWS})
    sel_total = sel_bad = 0
    for ds, bb in ARMS:
        for sp in ("random", "scaffold"):
            sel = D.selection_test(ds, bb, sp)
            if sel is None:
                continue
            sel_total += len(sel["selections"])
            sel_bad += sum(1 for x in sel["selections"] if x["mismatch"])

    MODEL_C, CHEM_C = "#0072B2", "#CC79A7"
    fig, ax = plt.subplots(figsize=(7.1, 2.62))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 42)
    ax.axis("off")

    def box(x, y, w, h, fc, ec, lw=0.9, r=1.6):
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
            fc=fc, ec=ec, lw=lw, zorder=2))

    def arrow(x0, y0, x1, y1, c=MUTED):
        ax.add_patch(FancyArrowPatch(
            (x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=7,
            lw=0.8, color=c, shrinkA=0, shrinkB=0, zorder=3))

    # --- the sweep, and the unit it produces -------------------------------
    box(0.5, 8, 20, 26, "#f6f7f9", GRID)
    ax.text(10.5, 31.4, "the sweep", ha="center", fontsize=7.4, color=INK,
            style="italic")
    for i, (n, what) in enumerate([(n_ds, "datasets"), (n_bb, "backbones"),
                                   (n_at, "attributors"), (2, "splits")]):
        ax.text(3.0, 26.6 - 4.6 * i, f"{n}", ha="right", fontsize=8.6,
                color=ACCENT, weight="bold")
        ax.text(4.0, 26.6 - 4.6 * i, what, ha="left", fontsize=7.2, color=INK)
    ax.text(10.5, 10.0, "random  ·  scaffold\n(Bemis–Murcko)", ha="center",
            va="center", fontsize=5.9, color=MUTED, linespacing=1.35)

    box(25, 14, 20, 14, "white", ACCENT, lw=1.1)
    ax.text(35, 24.0, "one cell", ha="center", fontsize=7.8, color=ACCENT,
            weight="bold")
    ax.text(35, 20.4, "(dataset, backbone,\nattributor, split)", ha="center",
            va="center", fontsize=6.5, color=INK, linespacing=1.3)
    ax.text(35, 15.4, f"{n_cells} audited", ha="center", fontsize=6.5,
            color=MUTED)
    arrow(20.9, 21, 24.6, 21)

    # --- the two questions, and the fact that only one is always askable ----
    ax.text(74.75, 38.6, "each cell is scored on two kinds of question",
            ha="center", fontsize=7.4, color=INK, style="italic")

    box(50, 20.5, 49.5, 15.5, "#f2f7fb", MODEL_C, lw=1.0)
    ax.text(52.2, 32.8, "Does the attribution describe the MODEL?",
            fontsize=7.2, color=MODEL_C, weight="bold")
    ax.text(52.2, 29.0,
            "occlusion faithfulness  ·  coherence  ·  stability\n"
            "calibration linkage  ·  confidence/correctness regime\n"
            "Fidelity±, sparsity, characterisation score",
            fontsize=6.3, color=INK, linespacing=1.45, va="center")
    ax.text(97.3, 21.9, f"measurable on all {n_cells} cells", ha="right",
            fontsize=6.2, color=MODEL_C)

    box(50, 5.0, 49.5, 12.5, "#fbf3f7", CHEM_C, lw=1.0)
    ax.text(52.2, 14.4, "Does it describe the CHEMISTRY?",
            fontsize=7.2, color=CHEM_C, weight="bold")
    ax.text(52.2, 10.9, "ground-truth localisation against the labelled\n"
                        "substructure (motif-native, RDKit)",
            fontsize=6.3, color=INK, linespacing=1.45, va="center")
    ax.text(97.3, 6.4, f"measurable on {n_gt}  ·  unmeasurable on {n_nogt}",
            ha="right", fontsize=6.2, color=CHEM_C)

    arrow(45.4, 23, 49.6, 28.2, MODEL_C)
    arrow(45.4, 19, 49.6, 11.2, CHEM_C)

    # --- the finding that connects them ------------------------------------
    ax.text(50, 1.4,
            f"The two come apart: ranking attributors by a model-side score "
            f"picks the wrong one in {sel_bad} of {sel_total} tests.",
            ha="center", fontsize=6.9, color=INK)
    ax.plot([2, 98], [3.4, 3.4], lw=0.5, color=GRID, zorder=1)

    save(fig, out)


if __name__ == "__main__":
    print("Generating figures from results/ …")
    fig_overview(HERE / "fig_overview.pdf")
    fig_lead(HERE / "fig_lead.pdf")
    fig_faithfulness_correctness(HERE / "fig_faith_correct.pdf")
    fig_dissociation(HERE / "fig_dissociation.pdf")
    fig_heatmaps(HERE / "fig_heatmaps.pdf")
    fig_backbone(HERE / "fig_backbone.pdf")
    fig_distributions(HERE / "fig_distributions.pdf")
    fig_regime(HERE / "fig_regime.pdf")
    fig_coverage(HERE / "fig_coverage.pdf")
    fig_abstention(HERE / "fig_abstention.pdf")
    copy_pipeline_figures()
    print("done.")
