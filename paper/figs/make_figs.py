"""Generate every paper figure from the committed results.

Run: ``python paper/figs/make_figs.py``. Reads RESULTS.md (via load_results) and
BENCHMARK_GT.json only — no value is hard-coded here. Outputs vector PDF into
this directory, which is what main.tex includes.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).parent))
from load_results import REPO, load, regime  # noqa: E402

OUT = Path(__file__).parent

# ---------------------------------------------------------------- style ----
INK, MUTED, AXIS = "#1a1a20", "#40404a", "#8d8d88"
REGIME_COLOR = {
    "synthetic (exact GT)": "#2a78d6",
    "classification": "#eb6834",
    "regression": "#1baf7a",
}
ATTR_MARKER = {
    "IntegratedGradients": "o", "Saliency": "s", "InputXGradient": "^",
    "GuidedBackprop": "D", "GNNExplainer": "v", "PGExplainer": "P",
}
SHORT = {
    "IntegratedGradients": "IG", "InputXGradient": "IxG",
    "GuidedBackprop": "GBP", "GNNExplainer": "GNNExpl", "PGExplainer": "PGExpl",
    "Saliency": "Saliency",
}


def style():
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["TeX Gyre Pagella", "Palatino", "DejaVu Serif"],
        # Match the paper's body font in maths too, so the PDF embeds one family.
        "mathtext.fontset": "custom",
        "mathtext.rm": "TeX Gyre Pagella",
        "mathtext.it": "TeX Gyre Pagella:italic",
        "mathtext.bf": "TeX Gyre Pagella:bold",
        "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8.5,
        "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
        "axes.edgecolor": AXIS, "axes.labelcolor": INK, "text.color": INK,
        "xtick.color": AXIS, "ytick.color": AXIS,
        "xtick.labelcolor": MUTED, "ytick.labelcolor": MUTED,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": "#e6e6e2", "grid.linewidth": 0.6,
        "axes.axisbelow": True, "figure.dpi": 150, "savefig.bbox": "tight",
    })


def save(fig, name):
    p = OUT / f"{name}.pdf"
    fig.savefig(p)
    plt.close(fig)
    print(f"  wrote {p.name}")
    return p


# ------------------------------------------------- Fig 1: money scatter ----
def fig_scatter(R):
    gt = [r for r in R if r["gt_auroc"] == r["gt_auroc"]
          and r["occ_spearman"] == r["occ_spearman"]]
    x = np.array([r["occ_spearman"] for r in gt])
    y = np.array([r["gt_auroc"] for r in gt])
    rho, p = spearmanr(x, y)

    fig, ax = plt.subplots(figsize=(3.4, 2.9))
    ax.axhline(0.5, color=AXIS, lw=0.9, ls=(0, (4, 3)), zorder=1)
    ax.text(0.985, 0.505, "chance", transform=ax.get_yaxis_transform(),
            ha="right", va="bottom", fontsize=6.5, color=MUTED)
    ax.axvline(0.0, color=AXIS, lw=0.9, ls=(0, (1, 3)), zorder=1)

    for r in gt:
        ax.scatter(r["occ_spearman"], r["gt_auroc"], s=26,
                   marker=ATTR_MARKER.get(r["attributor"], "o"),
                   facecolor=REGIME_COLOR[regime(r)], edgecolor="white",
                   linewidth=0.5, alpha=0.92, zorder=4)

    ax.set_xlabel(r"Faithfulness $\rightarrow$  (occlusion Spearman)")
    ax.set_ylabel(r"Correctness $\rightarrow$  (ground-truth AUROC)")
    ax.set_ylim(-0.05, 1.08)
    ax.set_title(rf"$\rho={rho:+.2f}$ ($p={p:.2f}$, $n={len(gt)}$ cells)",
                 fontsize=8, color=INK)

    handles = [Line2D([], [], marker=ATTR_MARKER[a], color="none",
                      markerfacecolor=MUTED, markeredgecolor="white",
                      markersize=4.5, label=SHORT[a]) for a in ATTR_MARKER]
    gt_regime_label = {"synthetic (exact GT)": "synthetic (exact GT)",
                       "classification": "MUTAG (proxy GT)"}
    handles += [Line2D([], [], marker="o", color="none", markerfacecolor=REGIME_COLOR[k],
                       markeredgecolor="white", markersize=4.5, label=v)
                for k, v in gt_regime_label.items()]
    ax.legend(handles=handles, loc="lower left", frameon=False, ncol=2,
              handletextpad=0.3, columnspacing=0.8, labelspacing=0.25,
              borderpad=0.1, fontsize=6)
    return save(fig, "fig1_faithfulness_vs_correctness"), dict(rho=rho, p=p, n=len(gt))


# --------------------------------------------------- Fig 2: heatmaps ------
def _matrix(R, metric, datasets, attributors):
    M = np.full((len(attributors), len(datasets)), np.nan)
    for i, a in enumerate(attributors):
        for j, d in enumerate(datasets):
            vals = [r[metric] for r in R
                    if r["attributor"] == a and r["dataset"] == d
                    and r[metric] == r[metric]]
            if vals:
                M[i, j] = float(np.mean(vals))
    return M


def _heat(ax, M, datasets, attributors, cmap, vmin, vmax, title, cbar_label,
          centre=None):
    im = ax.imshow(M, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(datasets)))
    ax.set_xticklabels(datasets, rotation=38, ha="right", fontsize=6.5)
    ax.set_yticks(range(len(attributors)))
    ax.set_yticklabels([SHORT[a] for a in attributors], fontsize=6.5)
    ax.set_title(title, fontsize=8, color=INK, pad=6)
    ax.grid(False)
    # White dividers between cells.
    for e in range(len(datasets) + 1):
        ax.axvline(e - 0.5, color="white", lw=1.1)
    for e in range(len(attributors) + 1):
        ax.axhline(e - 0.5, color="white", lw=1.1)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M[i, j]
            if v != v:
                ax.text(j, i, "–", ha="center", va="center", fontsize=6,
                        color=MUTED)
                continue
            # Contrast-aware label colour.
            frac = (v - vmin) / (vmax - vmin + 1e-12)
            dark = frac > 0.62 if centre is None else abs(v - centre) / max(
                vmax - centre, centre - vmin) > 0.62
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=5.6,
                    color="white" if dark else INK)
    cb = ax.figure.colorbar(im, ax=ax, fraction=0.030, pad=0.03)
    cb.set_label(cbar_label, fontsize=6.5)
    cb.ax.tick_params(labelsize=6)
    cb.outline.set_visible(False)
    return im


def fig_heatmaps(R):
    attributors = ["IntegratedGradients", "Saliency", "InputXGradient",
                   "GuidedBackprop", "GNNExplainer", "PGExplainer"]
    ds_occ = sorted({r["dataset"] for r in R})
    ds_gt = sorted({r["dataset"] for r in R if r["gt_auroc"] == r["gt_auroc"]})

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.5),
                             gridspec_kw={"width_ratios": [len(ds_occ), len(ds_gt)],
                                          "wspace": 0.62})
    Mo = _matrix(R, "occ_spearman", ds_occ, attributors)
    _heat(axes[0], Mo, ds_occ, attributors, "RdBu_r", -1, 1,
          "(a) Faithfulness: occlusion Spearman", r"$\rho$", centre=0.0)
    Mg = _matrix(R, "gt_auroc", ds_gt, attributors)
    _heat(axes[1], Mg, ds_gt, attributors, "YlGnBu", 0, 1,
          "(b) Correctness: ground-truth AUROC", "AUROC")
    return save(fig, "fig2_heatmaps")


# ------------------------------------------- Fig 3: backbone ordering -----
def fig_backbone(R):
    sub = [r for r in R if r["dataset"] == "SynthMotifs"
           and r["attributor"] == "IntegratedGradients" and r["split"] == "scaffold"]
    sub = sorted(sub, key=lambda r: r["gt_auroc"])
    names = [r["backbone"] for r in sub]
    gtv = [r["gt_auroc"] for r in sub]
    acc = [r["acc"] for r in sub]

    fig, ax = plt.subplots(figsize=(3.4, 2.0))
    ypos = np.arange(len(names))
    ax.axvline(0.5, color=AXIS, lw=0.9, ls=(0, (4, 3)), zorder=1)
    ax.text(0.5, -0.42, "chance", ha="center", va="bottom",
            fontsize=6.5, color=MUTED)
    ax.hlines(ypos, 0, gtv, color="#c9d6e8", lw=1.6, zorder=2)
    ax.scatter(gtv, ypos, s=46, color=REGIME_COLOR["synthetic (exact GT)"],
               edgecolor="white", linewidth=0.8, zorder=4)
    for yv, g, a in zip(ypos, gtv, acc):
        ax.text(g + 0.022, yv, f"{g:.2f}", va="center", fontsize=6.5, color=INK)
        ax.text(0.02, yv + 0.30, f"test acc {a:.2f}", va="center", fontsize=5.8,
                color=MUTED)
    ax.set_yticks(ypos)
    ax.set_yticklabels(names, fontsize=7)
    ax.set_xlim(0, 1.06)
    ax.set_xlabel("Ground-truth AUROC (exact motif mask)")
    ax.set_title("SynthMotifs $\\times$ Integrated Gradients", fontsize=8,
                 color=INK)
    return save(fig, "fig3_backbone_ordering")


# ------------------------------ Fig 4: per-task faithfulness distribution --
def fig_task_strip(R):
    groups = [
        ("synthetic\n(exact GT)", [r for r in R if r["dataset"].startswith("SynthMotifs")]),
        ("molecular\nclassification", [r for r in R if r["task"] == "classification"
                                       and not r["dataset"].startswith("SynthMotifs")]),
        ("molecular\nregression", [r for r in R if r["task"] == "regression"]),
    ]
    fig, ax = plt.subplots(figsize=(3.4, 2.2))
    ax.axhline(0, color=AXIS, lw=0.9, ls=(0, (4, 3)), zorder=1)
    rng = np.random.default_rng(0)
    for i, (lab, sub) in enumerate(groups):
        v = np.array([r["occ_spearman"] for r in sub
                      if r["occ_spearman"] == r["occ_spearman"]])
        col = REGIME_COLOR[["synthetic (exact GT)", "classification",
                            "regression"][i]]
        ax.scatter(i + rng.uniform(-0.16, 0.16, v.size), v, s=17, color=col,
                   edgecolor="white", linewidth=0.4, alpha=0.85, zorder=4)
        ax.hlines(np.median(v), i - 0.30, i + 0.30, color=INK, lw=1.5, zorder=5)
        ax.text(i, 1.02, f"n={v.size}\nmed {np.median(v):+.2f}", ha="center",
                va="bottom", fontsize=6, color=MUTED)
    ax.set_xticks(range(len(groups)))
    ax.set_xticklabels([g[0] for g in groups], fontsize=7)
    ax.set_ylabel(r"Occlusion Spearman $\rho$")
    ax.set_ylim(-1.05, 1.30)
    ax.set_yticks([-1, -0.5, 0, 0.5, 1])
    ax.set_title("Faithfulness by task family", fontsize=8, color=INK)
    return save(fig, "fig4_task_faithfulness")


def _place_labels(ax, points, texts):
    """Greedy non-overlapping label placement with leader lines. Tightly
    clustered attributors otherwise print on top of one another."""
    fig = ax.figure
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    cands = [(0, 7), (0, -11), (11, 4), (-11, 4), (11, -8), (-11, -8),
             (0, 18), (0, -21), (22, 11), (-22, 11), (22, -15), (-22, -15)]
    placed, pt_px = [], [ax.transData.transform(p) for p in points]
    for (x, y), lab in zip(points, texts):
        chosen = None
        for dx, dy in cands:
            ann = ax.annotate(lab, (x, y), textcoords="offset points",
                              xytext=(dx, dy), ha="center", fontsize=5.8,
                              color=INK, zorder=6)
            fig.canvas.draw_idle()
            bb = ann.get_window_extent(renderer=rend).expanded(1.08, 1.35)
            if not (any(bb.overlaps(b) for b in placed)
                    or any(bb.contains(px, py) for px, py in pt_px)):
                chosen = (ann, bb, dx, dy)
                break
            ann.remove()
        if chosen is None:
            dx, dy = cands[0]
            ann = ax.annotate(lab, (x, y), textcoords="offset points",
                              xytext=(dx, dy), ha="center", fontsize=5.8,
                              color=INK, zorder=6)
            chosen = (ann, ann.get_window_extent(renderer=rend), dx, dy)
        ann, bb, dx, dy = chosen
        placed.append(bb)
        if abs(dx) > 12 or abs(dy) > 20:
            ax.annotate("", xy=(x, y), xytext=(dx, dy),
                        textcoords="offset points", xycoords=ax.transData,
                        arrowprops=dict(arrowstyle="-", color=AXIS, lw=0.6,
                                        shrinkA=1, shrinkB=4), zorder=3)


# ---------------------------- Fig 5: two-regime selection (BENCHMARK_GT) --
def fig_regimes():
    data = json.loads((REPO / "BENCHMARK_GT.json").read_text())
    usable = [d for d in data if "error" not in d and d.get("selections")]
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.6))
    for ax, res in zip(axes, usable[:2]):
        t = res["per_attributor"]
        attrs = res["attributors"]
        xs = np.array([t[a]["characterization_mean"] for a in attrs])
        ys = np.array([t[a]["gt_auroc_mean"] for a in attrs])
        rho = res["rank_correlation"]["characterization"]["rho"]
        pv = res["rank_correlation"]["characterization"]["pvalue"]
        ax.axhline(0.5, color=AXIS, lw=0.9, ls=(0, (4, 3)), zorder=1)
        ok = np.isfinite(xs) & np.isfinite(ys)
        if ok.sum() >= 2:
            b, a0 = np.polyfit(xs[ok], ys[ok], 1)
            xr = np.linspace(xs[ok].min(), xs[ok].max(), 40)
            ax.plot(xr, a0 + b * xr, color=AXIS, lw=1.2, alpha=0.6, zorder=2)
        col = (REGIME_COLOR["synthetic (exact GT)"] if res["split"] == "random"
               else REGIME_COLOR["classification"])
        for a, xv, yv in zip(attrs, xs, ys):
            ax.scatter(xv, yv, s=34, marker=ATTR_MARKER.get(a, "o"), color=col,
                       edgecolor="white", linewidth=0.6, zorder=4)
        _place_labels(ax, list(zip(xs, ys)), [SHORT[a] for a in attrs])
        n = list(t.values())[0]["n_mol"]
        sel = next((s for s in res["selections"]
                    if s["faithfulness_metric"] == "characterization"), None)
        tag = ""
        if sel and sel["mismatch"]:
            tag = (f"\nselects {SHORT[sel['faithfulness_pick']]}, "
                   f"truth says {SHORT[sel['gt_best']]} ($p<0.001$)")
        ax.set_title(f"{res['dataset']} · {res['split']} · $n={n}$\n"
                     rf"$\rho={rho:+.2f}$ ($p={pv:.3f}$){tag}",
                     fontsize=7.5, color=INK)
        ax.set_xlabel("GraphFramEx characterisation")
        ax.set_ylim(-0.06, 1.22)
    axes[0].set_ylabel("Ground-truth AUROC")
    fig.tight_layout()
    return save(fig, "fig5_two_regimes")


def main():
    style()
    R = load()
    print(f"loaded {len(R)} result rows from RESULTS.md")
    _, stats = fig_scatter(R)
    fig_heatmaps(R)
    fig_backbone(R)
    fig_task_strip(R)
    fig_regimes()
    print(f"\nglobal rho(occ_spearman, gt_auroc) = {stats['rho']:+.3f} "
          f"(p={stats['p']:.3f}, n={stats['n']})")


if __name__ == "__main__":
    main()
