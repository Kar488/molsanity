"""Generate every manuscript figure from the committed results.

    python paper/figs/make_figures.py

Reads RESULTS.md / BENCHMARK.md / BENCHMARK_GT.json through ``msdata`` — no
number is typed in here. Re-run after more grid cells land and every figure
refreshes. Output: vector PDF in paper/figs/.
"""
from __future__ import annotations

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

BENCH = D.load_benchmark()
GTBENCH = D.load_benchmark_gt()

DATASET_ORDER = ["SynthMotifs", "SynthMotifsXL", "MUTAG", "BBBP", "BACE",
                 "ClinTox", "SIDER", "Tox21", "DILI", "hERG",
                 "ESOL", "FreeSolv", "Lipophilicity"]
ATTR_ORDER = ["IntegratedGradients", "Saliency", "InputXGradient",
              "GuidedBackprop", "GNNExplainer", "PGExplainer"]


def primary_split(dataset: str) -> str:
    splits = {r["split"] for r in BENCH if r["dataset"] == dataset}
    return "scaffold" if "scaffold" in splits else sorted(splits)[0]


def gt_kind(dataset: str) -> str:
    return "exact" if dataset in D.GT_EXACT else "proxy"


# ---------------------------------------------------------------- figure 1
def fig_faithfulness_correctness(out: Path):
    with_gt = [r for r in BENCH if r["gt_auroc"] is not None
               and r["occ_spearman"] is not None]
    no_gt = [r for r in BENCH if r["gt_auroc"] is None
             and r["occ_spearman"] is not None]

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 3.05),
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
        ax.scatter(r["occ_spearman"], r["gt_auroc"],
                   marker=ATTRIBUTOR_MARKER.get(r["attributor"], "o"),
                   s=42, linewidths=0.7,
                   facecolor=GT_COLOR[gt_kind(r["dataset"])],
                   edgecolor="white", alpha=0.92, zorder=3)

    # Label the two cells the headline turns on (values come from the data).
    def find(ds, bb, at, sp):
        for r in with_gt:
            if (r["dataset"], r["backbone"], r["attributor"], r["split"]) == (ds, bb, at, sp):
                return r
        return None

    ann = [(find("MUTAG", "GINE", "Saliency", "scaffold"), "MUTAG·Saliency", (24, 14)),
           (find("MUTAG", "GINE", "IntegratedGradients", "scaffold"), "MUTAG·IG", (16, 18)),
           (find("SynthMotifs", "GINE", "Saliency", "scaffold"), "Synth·Saliency", (26, -16))]
    for r, label, off in ann:
        if r is None:
            continue
        ax.annotate(label, (r["occ_spearman"], r["gt_auroc"]),
                    textcoords="offset points", xytext=off, fontsize=6.4,
                    color=INK,
                    arrowprops=dict(arrowstyle="-", lw=0.5, color=MUTED,
                                    shrinkA=0, shrinkB=2))

    ax.set_xlabel("occlusion faithfulness  (Spearman $\\rho$, higher = more faithful)")
    ax.set_ylabel("ground-truth localisation (AUROC)")
    ax.set_ylim(-0.03, 1.06)
    ax.grid(axis="both", lw=0.4, alpha=0.6)
    ax.set_axisbelow(True)
    despine(ax)
    panel_label(ax, "a")

    h_gt = [plt.Line2D([], [], ls="", marker="o", ms=5, mfc=GT_COLOR["exact"],
                       mec="white", label="exact node GT (synthetic)"),
            plt.Line2D([], [], ls="", marker="o", ms=5, mfc=GT_COLOR["proxy"],
                       mec="white", label="motif-proxy GT (MUTAG)")]
    h_at = [plt.Line2D([], [], ls="", marker=ATTRIBUTOR_MARKER[a], ms=4.5,
                       mfc="0.45", mec="white", label=SHORT[a])
            for a in ATTR_ORDER if any(r["attributor"] == a for r in with_gt)]
    leg1 = ax.legend(handles=h_gt, loc="lower left", bbox_to_anchor=(0.0, 0.0),
                     handletextpad=0.3, borderpad=0.2, labelspacing=0.25)
    ax.add_artist(leg1)
    ax.legend(handles=h_at, loc="upper left", ncol=2, handletextpad=0.3,
              columnspacing=0.9, borderpad=0.2, labelspacing=0.25)

    # (b) cells where the correctness axis does not exist.
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
def fig_heatmaps(out: Path):
    rows = [r for r in BENCH if r["backbone"] == "GINE"
            and r["split"] == primary_split(r["dataset"])]
    datasets = [d for d in DATASET_ORDER if any(r["dataset"] == d for r in rows)]
    attrs = [a for a in ATTR_ORDER if any(r["attributor"] == a for r in rows)]

    audited = {(r["attributor"], r["dataset"]) for r in rows}

    def grid(metric):
        M = np.full((len(attrs), len(datasets)), np.nan)
        for r in rows:
            if r["dataset"] in datasets and r["attributor"] in attrs:
                v = r[metric]
                if v is not None:
                    M[attrs.index(r["attributor"]), datasets.index(r["dataset"])] = v
        return M

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.55))
    specs = [("occ_spearman", "occlusion faithfulness (Spearman $\\rho$)",
              "RdBu_r", -1.0, 1.0, 0.0),
             ("gt_auroc", "ground-truth localisation (AUROC)",
              "RdBu_r", 0.0, 1.0, 0.5)]
    for ax, (metric, title, cmap, lo, hi, mid) in zip(axes, specs):
        M = grid(metric)
        norm = plt.matplotlib.colors.TwoSlopeNorm(vmin=lo, vcenter=mid, vmax=hi)
        ax.set_facecolor("#eceef1")
        im = ax.imshow(M, cmap=cmap, norm=norm, aspect="auto")
        for i in range(len(attrs)):
            for j in range(len(datasets)):
                v = M[i, j]
                if np.isnan(v):
                    # distinguish "cell not audited" from "audited, metric undefined"
                    seen = (attrs[i], datasets[j]) in audited
                    ax.text(j, i, "—" if seen else "·", ha="center", va="center",
                            fontsize=6.5 if seen else 7.5, color="#8b93a0")
                else:
                    shade = abs(norm(v) - 0.5) * 2
                    ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                            fontsize=5.9,
                            color="white" if shade > 0.62 else INK)
        ax.set_xticks(range(len(datasets)))
        ax.set_xticklabels(datasets, rotation=42, ha="right", fontsize=6.4)
        ax.set_yticks(range(len(attrs)))
        ax.set_yticklabels([SHORT[a] for a in attrs], fontsize=6.6)
        ax.set_title(title, fontsize=7.4, pad=5)
        ax.tick_params(length=0)
        for s in ax.spines.values():
            s.set_visible(False)
        cb = fig.colorbar(im, ax=ax, fraction=0.033, pad=0.02)
        cb.ax.tick_params(labelsize=6, length=2)
        cb.outline.set_visible(False)
    panel_label(axes[0], "a", dx=-0.13, dy=1.16)
    panel_label(axes[1], "b", dx=-0.13, dy=1.16)
    fig.subplots_adjust(wspace=0.42)
    save(fig, out)


# ---------------------------------------------------------------- figure 3
def fig_backbone(out: Path):
    panels = [("SynthMotifs", "scaffold", "exact node ground truth"),
              ("MUTAG", "scaffold", "motif-proxy ground truth")]
    fig, axes = plt.subplots(2, 1, figsize=(3.3, 3.5))
    for ax, (ds, sp, sub) in zip(axes, panels):
        rows = [r for r in BENCH if r["dataset"] == ds and r["split"] == sp
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
        ax.set_xlim(0, 1.08)
        ax.set_title(f"{ds} · Integrated Gradients · {sub}", fontsize=7.2, pad=4)
        ax.grid(axis="x", lw=0.4, alpha=0.6)
        ax.set_axisbelow(True)
        despine(ax)
        ax.tick_params(axis="y", length=0)
    axes[1].set_xlabel("ground-truth localisation (AUROC)")
    panel_label(axes[0], "a", dx=-0.30, dy=1.22)
    panel_label(axes[1], "b", dx=-0.30, dy=1.22)
    fig.subplots_adjust(hspace=0.55)
    save(fig, out)


# ---------------------------------------------------------------- figure 4
def fig_dissociation(out: Path):
    titles = {"SynthMotifsXL": "in-distribution (random split, exact GT)",
              "MUTAG": "scaffold shift (motif-proxy GT)"}
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.8))
    for ax, blk in zip(axes, GTBENCH):
        pa = blk["per_attributor"]
        attrs = sorted(pa, key=lambda a: pa[a]["gt_auroc_mean"], reverse=True)
        y = np.arange(len(attrs))
        vals = [pa[a]["gt_auroc_mean"] for a in attrs]
        lo = [v - pa[a]["gt_auroc_ci"][0] for v, a in zip(vals, attrs)]
        hi = [pa[a]["gt_auroc_ci"][1] - v for v, a in zip(vals, attrs)]
        ax.barh(y, vals, height=0.6, xerr=[lo, hi], zorder=3,
                color=[ATTRIBUTOR_COLOR[a] for a in attrs], alpha=0.9,
                error_kw=dict(lw=0.8, ecolor="#3f4653", capsize=1.8))
        ax.axvline(0.5, color=MUTED, lw=0.8, ls="--", zorder=4)
        for i, a in enumerate(attrs):
            v = pa[a]["gt_auroc_mean"]
            if v > 0.18:
                ax.text(v - 0.02, i, f"{v:.2f}", va="center", ha="right",
                        fontsize=6.3, color="white", zorder=5)
            else:
                ax.text(v + 0.06, i, f"{v:.2f}", va="center", ha="left",
                        fontsize=6.3, color=INK, zorder=5)
        ax.set_yticks(y)
        ax.set_yticklabels([SHORT[a] for a in attrs], fontsize=6.8)
        ax.invert_yaxis()
        ax.set_xlim(0, 1.95)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.set_xlabel("ground-truth localisation (AUROC)")
        ax.set_title(f"{blk['dataset']} · {blk['backbone']} — {titles.get(blk['dataset'], '')}",
                     fontsize=7.2, pad=9)
        ax.grid(axis="x", lw=0.4, alpha=0.6)
        ax.set_axisbelow(True)
        despine(ax)
        ax.tick_params(axis="y", length=0)

        # Mark what each faithfulness-only ranking would have selected.
        marks = {"occ_spearman": "occlusion $\\rho$", "fidelity_plus": "Fidelity+",
                 "characterization": "charact."}
        picks: dict[str, list[str]] = {}
        for sel in blk["selections"]:
            picks.setdefault(sel["faithfulness_pick"], []).append(
                marks[sel["faithfulness_metric"]]
                + ("*" if sel["mismatch"] else ""))
        for a, labels in picks.items():
            i = attrs.index(a)
            mism = any(l.endswith("*") for l in labels)
            body = (", ".join(labels[:2]) + ",\n" + ", ".join(labels[2:])
                    if len(labels) > 2 else ", ".join(labels))
            ax.annotate("← ranked 1st by\n" + body, (1.10, i), fontsize=5.8,
                        color="#8B1A1A" if mism else MUTED, va="center",
                        linespacing=1.3)
        rc = blk["rank_correlation"]
        txt = " · ".join(f"{marks[k]} {v['rho']:+.2f}" for k, v in rc.items())
        ax.text(0.0, -0.32, "faithfulness↔truth rank correlation\n" + txt,
                transform=ax.transAxes, fontsize=6.0, color=INK, va="top",
                linespacing=1.4)
    axes[1].text(0.0, -0.56, "*  ranking disagrees with the ground truth "
                 "(paired Wilcoxon $p<0.001$)", transform=axes[1].transAxes,
                 ha="left", fontsize=6.0, color="#8B1A1A")
    panel_label(axes[0], "a", dx=-0.26, dy=1.19)
    panel_label(axes[1], "b", dx=-0.26, dy=1.19)
    fig.subplots_adjust(wspace=0.60, bottom=0.30, top=0.88)
    save(fig, out)


# ---------------------------------------------------------------- figure 5
def fig_distributions(out: Path):
    fig, axes = plt.subplots(1, 3, figsize=(7.1, 2.35))
    rng = np.random.default_rng(1)

    # (a) faithfulness by regime
    ax = axes[0]
    regimes = ["synthetic", "classification", "regression"]
    for i, reg in enumerate(regimes):
        vals = [r["occ_spearman"] for r in BENCH
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

    # (b) field-standard Fidelity+ vs MolSanity occlusion faithfulness
    ax = axes[1]
    for reg in regimes:
        pts = [(r["occ_spearman"], r["fidelity_plus"]) for r in BENCH
               if r["regime"] == reg and r["occ_spearman"] is not None
               and r["fidelity_plus"] is not None]
        if pts:
            ax.scatter(*zip(*pts), s=13, alpha=0.75, color=REGIME_COLOR[reg],
                       edgecolor="white", linewidths=0.4, label=reg, zorder=3)
    ax.axhline(0, color=MUTED, lw=0.7, ls=":")
    ax.axvline(0, color=MUTED, lw=0.7, ls=":")
    ax.set_xlabel("occlusion faithfulness ($\\rho$)")
    ax.set_ylabel("Fidelity+")
    ax.legend(loc="lower right", handletextpad=0.2, labelspacing=0.2,
              borderpad=0.2, fontsize=6.2)
    ax.grid(lw=0.4, alpha=0.6)
    ax.set_axisbelow(True)
    despine(ax)
    panel_label(ax, "b", dx=-0.26)

    # (c) cross-checkpoint stability by attributor
    ax = axes[2]
    attrs = [a for a in ATTR_ORDER
             if any(r["attributor"] == a and r["stability"] is not None for r in BENCH)]
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
    ax.set_ylim(0.2, 1.05)
    ax.grid(axis="y", lw=0.4, alpha=0.6)
    ax.set_axisbelow(True)
    despine(ax)
    panel_label(ax, "c", dx=-0.26)

    fig.subplots_adjust(wspace=0.42)
    save(fig, out)


# ---------------------------------------------------------------- coverage
def fig_coverage(out: Path):
    cov = D.coverage()
    done = {(r["dataset"], r["backbone"], r["attributor"], r["split"]) for r in BENCH}
    planned = {(c["dataset"], c["backbone"], c["attributor"], c["split"])
               for c in D.planned_cells()}
    datasets = [d for d in DATASET_ORDER if any(k[0] == d for k in planned | done)]
    datasets += sorted({k[0] for k in planned | done} - set(datasets))
    splits = ["scaffold", "random"]

    fig, ax = plt.subplots(figsize=(3.3, 3.15))
    cmap = plt.get_cmap("Blues")
    for i, ds in enumerate(datasets):
        for j, sp in enumerate(splits):
            p_ = {k for k in planned if k[0] == ds and k[3] == sp}
            d_ = {k for k in done if k[0] == ds and k[3] == sp}
            n_done, n_plan = len(d_), len(p_ | d_)
            if n_plan == 0:
                ax.add_patch(plt.Rectangle((j - 0.45, i - 0.42), 0.9, 0.84,
                                           facecolor="#f2f3f5", edgecolor="white",
                                           lw=1.0))
                continue
            frac = n_done / n_plan
            ax.add_patch(plt.Rectangle((j - 0.45, i - 0.42), 0.9, 0.84,
                                       facecolor=cmap(0.12 + 0.78 * frac),
                                       edgecolor="white", lw=1.0))
            ax.text(j, i, f"{n_done}/{n_plan}", ha="center", va="center",
                    fontsize=6.6, color="white" if frac > 0.55 else INK)
    ax.set_ylim(len(datasets) - 0.45, -0.55)
    ax.set_xlim(-0.62, len(splits) - 0.38)
    ax.set_yticks(range(len(datasets)))
    ax.set_yticklabels(datasets, fontsize=6.8)
    ax.set_xticks(range(len(splits)))
    ax.set_xticklabels(["scaffold\n(shift)", "random\n(in-distribution)"],
                       fontsize=6.8)
    ax.xaxis.set_ticks_position("top")
    ax.tick_params(length=0)
    for s_ in ax.spines.values():
        s_.set_visible(False)
    ax.set_xlabel(f"{cov['n_done_total']} audited cells committed; "
                  f"{cov['n_done_in_plan']}/{cov['n_planned']} of the\n"
                  f"planned grid complete (grey = no cell planned)",
                  fontsize=6.6, labelpad=6)
    save(fig, out)


if __name__ == "__main__":
    print("Generating figures from committed results…")
    fig_faithfulness_correctness(HERE / "fig_faith_correct.pdf")
    fig_heatmaps(HERE / "fig_heatmaps.pdf")
    fig_backbone(HERE / "fig_backbone.pdf")
    fig_dissociation(HERE / "fig_dissociation.pdf")
    fig_distributions(HERE / "fig_distributions.pdf")
    fig_coverage(HERE / "fig_coverage.pdf")
    print("done.")
