"""Capstone figure: faithfulness tracks correctness in-distribution, not under shift.

Form choice — the data's job is to show whether a *relationship* holds, and the
claim is that it holds in one regime and collapses in another. That is a
comparison of two bivariate relationships, so the form is a **small-multiple
scatter with shared axes**: the claim becomes geometry (an upward trend vs a
scattered/downward one) rather than a number the reader has to trust.

Every point is one attributor, positioned by its mean faithfulness (x) and its
mean ground-truth localisation (y) over the *same* molecules. All six points are
directly labelled — required relief for the house palette's contrast warning, and
it means identity is never carried by colour alone.

Numbers come from ``benchmark.faithfulness_vs_truth.analyse``; nothing is fixed.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from .style import apply_style, attributor_color, panel_label, save_vector
from .style import AXIS_GREY, INK, MUTED_INK, short

# The faithfulness metric plotted on x. characterization is GraphFramEx's
# headline score, so it is the fairest stand-in for "what a SOTA framework ranks by".
X_METRIC = "characterization"
X_LABEL = "Faithfulness  (GraphFramEx characterisation)"


def _place_labels(ax, points, texts, colors):
    """Greedy non-overlapping label placement with leader lines.

    Attributors cluster tightly (four gradient methods often land on top of one
    another), so fixed offsets collide. We try candidate offsets ring-by-ring and
    keep the first that clears every already-placed label and every data point;
    if the chosen offset is far from its point we draw a thin leader line.
    """
    fig = ax.figure
    fig.canvas.draw()  # need a renderer for text extents
    renderer = fig.canvas.get_renderer()

    # Candidate offsets in points, nearest ring first, prefer up then sideways.
    candidates = [(0, 11), (0, -15), (13, 6), (-13, 6), (13, -9), (-13, -9),
                  (0, 24), (0, -27), (26, 14), (-26, 14), (26, -18), (-26, -18),
                  (0, 37), (0, -39), (38, 22), (-38, 22), (38, -26), (-38, -26)]
    placed = []
    pt_boxes = [ax.transData.transform(p) for p in points]

    for (x, y), label, colour in zip(points, texts, colors):
        best = None
        for dx, dy in candidates:
            ann = ax.annotate(label, (x, y), textcoords="offset points",
                              xytext=(dx, dy), ha="center", fontsize=8,
                              color=INK, zorder=6)
            fig.canvas.draw_idle()
            bb = ann.get_window_extent(renderer=renderer).expanded(1.06, 1.30)
            clash = any(bb.overlaps(b) for b in placed) or any(
                bb.contains(px, py) for px, py in pt_boxes)
            if not clash:
                best = (ann, bb, dx, dy)
                break
            ann.remove()
        if best is None:  # everything collided — fall back to the first offset
            dx, dy = candidates[0]
            ann = ax.annotate(label, (x, y), textcoords="offset points",
                              xytext=(dx, dy), ha="center", fontsize=8,
                              color=INK, zorder=6)
            bb = ann.get_window_extent(renderer=renderer)
            best = (ann, bb, dx, dy)
        ann, bb, dx, dy = best
        placed.append(bb)
        if abs(dx) > 14 or abs(dy) > 26:  # far label -> thin leader line
            ann.set_arrowprops if False else None
            ax.annotate("", xy=(x, y), xytext=(dx, dy),
                        textcoords="offset points",
                        xycoords=ax.transData,
                        arrowprops=dict(arrowstyle="-", color=AXIS_GREY,
                                        lw=0.7, shrinkA=2, shrinkB=6),
                        zorder=3)


def _panel(ax, res: dict, title: str, subtitle: str, show_ylabel: bool):
    t = res["per_attributor"]
    attributors = res["attributors"]
    rho = res.get("rank_correlation", {}).get(X_METRIC, {}).get("rho", float("nan"))

    xs = np.array([t[a][f"{X_METRIC}_mean"] for a in attributors], dtype=float)
    ys = np.array([t[a]["gt_auroc_mean"] for a in attributors], dtype=float)

    # Chance line: below it, an attribution is anti-aligned with the truth.
    # Tag it on the LEFT: the right side is where the faithful methods cluster.
    ax.axhline(0.5, color=AXIS_GREY, lw=1.0, ls=(0, (4, 3)), zorder=1)
    ax.text(0.015, 0.505, "chance", transform=ax.get_yaxis_transform(),
            ha="left", va="bottom", fontsize=7.5, color=MUTED_INK,
            bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none", alpha=0.85))

    # Trend line — the visual answer to "does faithfulness track correctness?".
    ok = np.isfinite(xs) & np.isfinite(ys)
    if ok.sum() >= 2:
        b, a0 = np.polyfit(xs[ok], ys[ok], 1)
        xr = np.linspace(xs[ok].min(), xs[ok].max(), 50)
        ax.plot(xr, a0 + b * xr, color=AXIS_GREY, lw=1.4, alpha=0.55, zorder=2)

    pts, labels_, cols = [], [], []
    for a, x, y in zip(attributors, xs, ys):
        if not (np.isfinite(x) and np.isfinite(y)):
            continue
        ax.scatter([x], [y], s=88, color=attributor_color(a), zorder=4,
                   edgecolor="white", linewidth=1.6)  # surface ring
        pts.append((x, y))
        labels_.append(short(a))
        cols.append(attributor_color(a))

    # Selection error: what a faithfulness-only ranking picks vs what GT says.
    sel = next((s for s in res["selections"]
                if s["faithfulness_metric"] == X_METRIC), None)
    if sel and sel.get("mismatch"):
        pick, best = sel["faithfulness_pick"], sel["gt_best"]
        px, py = t[pick][f"{X_METRIC}_mean"], t[pick]["gt_auroc_mean"]
        bx, by = t[best][f"{X_METRIC}_mean"], t[best]["gt_auroc_mean"]
        ax.annotate("", xy=(bx, by), xytext=(px, py),
                    arrowprops=dict(arrowstyle="->", color=INK, lw=1.3,
                                    connectionstyle="arc3,rad=-0.25",
                                    shrinkA=9, shrinkB=9), zorder=3)
        p = sel.get("paired_gt_pvalue")
        ptxt = "p < 0.001" if (p is not None and p == p and p < 1e-3) else f"p = {p:.3g}"
        # Caption goes at the TOP: the bottom of this panel is where the
        # faithful-but-wrong cluster and its labels live.
        ax.text(0.5, 0.915,
                f"ranks {short(pick)} top — truth says {short(best)}   ({ptxt})",
                transform=ax.transAxes, ha="center", va="top", fontsize=8.5,
                color=INK,
                bbox=dict(boxstyle="round,pad=0.34", fc="white", ec=AXIS_GREY,
                          lw=0.7, alpha=0.95))

    ax.set_title(title, fontsize=10.5, pad=16, loc="left")
    ax.text(0, 1.02, subtitle, transform=ax.transAxes, fontsize=8.5,
            color=MUTED_INK, va="bottom")
    ax.set_xlabel(X_LABEL, fontsize=9)
    if show_ylabel:
        ax.set_ylabel("Correctness  (ground-truth AUROC)", fontsize=9)
    # Headroom above 1.0 so the top cluster's labels have somewhere to go.
    ax.set_ylim(-0.26, 1.34)
    ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.margins(x=0.16)

    # rho is the headline of each panel — state it, don't make the reader infer.
    verdict = "faithfulness tracks truth" if (rho == rho and rho > 0.5) else \
              "faithfulness does NOT track truth"
    ax.text(0.5, 0.995, f"ρ = {rho:+.2f}   {verdict}", transform=ax.transAxes,
            ha="center", va="top", fontsize=9.5, color=INK, fontweight="bold")

    # Labels last: placement needs the final limits/transforms to de-collide.
    _place_labels(ax, pts, labels_, cols)


def dissociation_figure(results: list[dict], out_path="figures/key/dissociation",
                        labels=None) -> dict:
    """Two-panel small multiple: in-distribution vs shift.

    ``results`` is the list returned by ``faithfulness_vs_truth.write_report``.
    """
    import matplotlib.pyplot as plt

    apply_style()
    usable = [r for r in results if "error" not in r and r.get("selections")]
    if len(usable) < 2:
        raise ValueError("need two analysed regimes for the dissociation figure")
    labels = labels or [
        ("In-distribution", "random split · exact ground truth"),
        ("Under scaffold shift", "scaffold split · motif ground truth"),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.5), sharey=True)
    for i, (ax, res) in enumerate(zip(axes, usable[:2])):
        title, sub = labels[i]
        n = next(iter(res["per_attributor"].values()))["n_mol"]
        _panel(ax, res, title, f"{res['dataset']} · n = {n} molecules", i == 0)
        panel_label(ax, "ab"[i], dx=-0.10 if i == 0 else -0.04)

    fig.suptitle(
        "A faithfulness-only benchmark selects the wrong attributor under shift",
        fontsize=12, y=1.04, x=0.5, ha="center", color=INK, fontweight="bold")
    fig.tight_layout()
    return save_vector(fig, Path(out_path))


def make_dissociation_figure(out_path="figures/key/dissociation") -> dict:
    """Recompute the analysis and render the figure. Returns saved paths."""
    from ..benchmark.faithfulness_vs_truth import DEFAULT_CELLS, analyse

    results = [analyse(ds, bb, sp) for ds, bb, sp, _ in DEFAULT_CELLS]
    labels = [(("In-distribution" if sp == "random" else "Under scaffold shift"),
               f"{sp} split") for _, _, sp, _ in DEFAULT_CELLS]
    return dissociation_figure(results, out_path, labels=labels)


if __name__ == "__main__":
    print(make_dissociation_figure())
