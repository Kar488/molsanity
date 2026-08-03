"""Does a faithfulness-only evaluation pick the attributor the ground truth does?

This is the head-to-head that separates MolSanity from faithfulness-centric
frameworks (GraphFramEx / MolFaith / DIG's fidelity metrics). On a dataset with
*exact* node ground truth, we rank attributors two ways on the SAME molecules:

  1. by a **faithfulness** metric a SOTA framework would use (occlusion Spearman,
     Fidelity+, or GraphFramEx's characterisation score), and
  2. by **correctness** (GT AUROC against the exact motif mask).

If the faithfulness-selected best attributor is *not* the correctness-selected
best, a faithfulness-only benchmark would recommend the wrong method — and we
test that gap for significance with a paired Wilcoxon on per-molecule GT AUROC.
Every number is computed from the per-molecule audit records; nothing is fixed.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from ..audit.stats import paired_wilcoxon, summarise
from .tables import AUDIT_ROOT, _parse_cell_id, discover_cells

# Faithfulness-family selectors a SOTA evaluation framework would rank by.
# (higher = "more faithful" for all three, so argmax is the framework's pick.)
FAITHFULNESS_METRICS = ("occ_spearman", "fidelity_plus", "characterization")
CORRECTNESS_METRIC = "gt_auroc"


def _by_attributor(cells: dict[str, list[dict]], dataset: str, backbone: str,
                   split: str) -> dict[str, list[dict]]:
    out = {}
    for cell_id, recs in cells.items():
        m = _parse_cell_id(cell_id)
        if m["dataset"] == dataset and m["backbone"] == backbone and m["split"] == split:
            out[m["attributor"]] = recs
    return out


def _mean(recs: list[dict], metric: str) -> float:
    vals = np.array([r.get(metric, np.nan) for r in recs], dtype=np.float64)
    vals = vals[np.isfinite(vals)]
    return float(vals.mean()) if vals.size else float("nan")


def _paired_gt(a_recs: list[dict], b_recs: list[dict]) -> dict:
    """Paired GT-AUROC difference between two attributors on shared molecules."""
    a_by = {r["graph_id"]: r.get(CORRECTNESS_METRIC, np.nan) for r in a_recs}
    b_by = {r["graph_id"]: r.get(CORRECTNESS_METRIC, np.nan) for r in b_recs}
    shared = sorted(set(a_by) & set(b_by))
    a = np.array([a_by[g] for g in shared], dtype=np.float64)
    b = np.array([b_by[g] for g in shared], dtype=np.float64)
    return paired_wilcoxon(a, b)


def _rank_correlation(table: dict, attributors: list[str], fm: str) -> dict:
    """Spearman rank correlation between a faithfulness metric and GT AUROC,
    across attributors. Near 0 or negative => faithfulness does not track
    correctness (a faithfulness-only ranking is uninformative about truth)."""
    from scipy.stats import spearmanr

    gt = np.array([table[a]["gt_auroc_mean"] for a in attributors], dtype=np.float64)
    fa = np.array([table[a][f"{fm}_mean"] for a in attributors], dtype=np.float64)
    mask = np.isfinite(gt) & np.isfinite(fa)
    if mask.sum() < 3:
        return {"rho": float("nan"), "pvalue": float("nan")}
    r = spearmanr(fa[mask], gt[mask])
    return {"rho": float(r.correlation), "pvalue": float(r.pvalue)}


def analyse(dataset: str, backbone: str = "GINE", split: str = "random",
            root: Path = AUDIT_ROOT, seed: int = 0) -> dict:
    """Run the faithfulness-vs-correctness selection test for one GT cell group."""
    cells = discover_cells(root)
    by_attr = _by_attributor(cells, dataset, backbone, split)
    attributors = sorted(by_attr)
    if len(attributors) < 2:
        return {"dataset": dataset, "backbone": backbone, "split": split,
                "error": "need >=2 attributors with records", "attributors": attributors}

    # Per-attributor means (with bootstrap CI on the correctness metric).
    table = {}
    for a in attributors:
        recs = by_attr[a]
        gt = np.array([r.get(CORRECTNESS_METRIC, np.nan) for r in recs], dtype=np.float64)
        s = summarise(gt, name=CORRECTNESS_METRIC, seed=seed)
        table[a] = {
            "n_mol": len(recs),
            "gt_auroc_mean": s["mean"],
            "gt_auroc_ci": (s["ci95_lo"], s["ci95_hi"]),
            **{f"{m}_mean": _mean(recs, m) for m in FAITHFULNESS_METRICS},
        }

    # Correctness-selected best (the attributor the exact GT says is best).
    gt_best = max(attributors, key=lambda a: (table[a]["gt_auroc_mean"]
                                              if table[a]["gt_auroc_mean"] == table[a]["gt_auroc_mean"]
                                              else -np.inf))

    # For each faithfulness metric: which attributor would a SOTA framework pick,
    # and is it significantly worse on exact GT than the correctness-best?
    selections = []
    for fm in FAITHFULNESS_METRICS:
        vals = {a: table[a][f"{fm}_mean"] for a in attributors}
        if all(v != v for v in vals.values()):  # all NaN
            continue
        faith_best = max(attributors, key=lambda a: (vals[a] if vals[a] == vals[a] else -np.inf))
        test = _paired_gt(by_attr[gt_best], by_attr[faith_best]) if faith_best != gt_best else None
        selections.append({
            "faithfulness_metric": fm,
            "faithfulness_pick": faith_best,
            "faithfulness_pick_gt_auroc": table[faith_best]["gt_auroc_mean"],
            "gt_best": gt_best,
            "gt_best_gt_auroc": table[gt_best]["gt_auroc_mean"],
            "mismatch": faith_best != gt_best,
            "paired_gt_gap_median": (test or {}).get("median_diff"),
            "paired_gt_pvalue": (test or {}).get("pvalue"),
            "n_paired": (test or {}).get("n"),
        })

    rank_corr = {fm: _rank_correlation(table, attributors, fm)
                 for fm in FAITHFULNESS_METRICS}
    return {"dataset": dataset, "backbone": backbone, "split": split,
            "attributors": attributors, "gt_best": gt_best,
            "per_attributor": table, "selections": selections,
            "rank_correlation": rank_corr}


def _fmt(v, nd=3):
    if v is None:
        return "—"
    try:
        f = float(v)
        return "—" if f != f else f"{f:.{nd}f}"
    except (TypeError, ValueError):
        return str(v)


# Preferred cells to contrast, when a run produced them: an in-distribution
# control and a distribution-shift case. Each is (dataset, backbone, split,
# regime-label). These are *preferences*, not requirements — see
# ``eligible_cells``, which falls back to whatever the run actually audited so
# the report is never silently empty.
# Both splits of the *same* dataset and backbone, so the contrast isolates
# scaffold shift rather than confounding it with a change of dataset. MUTAG is
# the flagship because it is the only ground-truth arm that is both molecular
# (so a Bemis-Murcko split is a real chemical shift -- BA-2Motifs, SynthMotifs
# and ShapeGGen are not molecules and their scaffold split is degenerate) and
# unsaturated (MolMotif sits at GT AUROC ~0.99, where ranking attributors is
# noise around a ceiling).
DEFAULT_CELLS = [
    ("MUTAG", "GINE", "random", "in-distribution (motif-proxy GT)"),
    ("MUTAG", "GINE", "scaffold", "scaffold shift (motif-proxy GT)"),
]

_REGIME_LABEL = {"random": "in-distribution", "scaffold": "scaffold shift"}


def eligible_cells(root: Path = AUDIT_ROOT, min_attributors: int = 2) -> list[tuple]:
    """Cell families this run can actually run the selection test on.

    A family is (dataset, backbone, split) with at least ``min_attributors``
    audited attributors whose records carry ground truth. Families that also
    exist on the *other* split come first: comparing two splits of the same
    dataset isolates distribution shift instead of confounding it with a change
    of dataset. This is what keeps the report meaningful when the preferred
    cells of ``DEFAULT_CELLS`` failed or were not part of the sweep.
    """
    cells = discover_cells(root)
    families: dict[tuple, set] = {}
    for cell_id, recs in cells.items():
        m = _parse_cell_id(cell_id)
        has_gt = any(np.isfinite(r.get(CORRECTNESS_METRIC, np.nan)) for r in recs)
        if has_gt:
            key = (m["dataset"], m["backbone"], m["split"])
            families.setdefault(key, set()).add(m["attributor"])
    keys = [k for k, attrs in families.items() if len(attrs) >= min_attributors]
    paired = {(d, b) for d, b, _ in keys
              if sum(1 for k in keys if k[0] == d and k[1] == b) > 1}
    keys.sort(key=lambda k: (0 if (k[0], k[1]) in paired else 1,
                             k[0], k[1], k[2] != "random"))
    return [(d, b, sp, _REGIME_LABEL.get(sp, sp)) for d, b, sp in keys]


def resolve_cells(cells=None, root: Path = AUDIT_ROOT) -> list[tuple]:
    """Preferred cells that this run produced, else whatever it did produce.

    The preferred set is taken only when it survives *whole*. Accepting a
    partial match used to yield a single-regime report while the surrounding
    prose contrasted two: the 3 August run had no ``SynthMotifsXL``, so the
    in-distribution panel silently vanished and the conclusions described a
    comparison that had not been computed.
    """
    available = {(d, b, sp) for d, b, sp, _ in eligible_cells(root)}
    preferred = list(cells or DEFAULT_CELLS)
    if preferred and all((c[0], c[1], c[2]) in available for c in preferred):
        return preferred
    return eligible_cells(root)


def _section(res: dict, regime: str) -> list[str]:
    if "error" in res:
        return [f"### {res['dataset']} · {res['split']} — _{res['error']}_", ""]
    t = res["per_attributor"]
    n = next(iter(t.values()))["n_mol"]
    lines = [
        f"### {res['dataset']} · {res['backbone']} · {res['split']} split "
        f"— {regime}",
        "",
        f"{len(res['attributors'])} attributors on the same ~{n} molecules.",
        "",
        "| attributor | GT AUROC | 95% CI | occ_spearman | Fidelity+ | characterization |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for a in sorted(res["attributors"], key=lambda a: -t[a]["gt_auroc_mean"]):
        r = t[a]
        star = " ⭐" if a == res["gt_best"] else ""
        lines.append(
            f"| {a}{star} | {_fmt(r['gt_auroc_mean'])} | "
            f"({_fmt(r['gt_auroc_ci'][0])}, {_fmt(r['gt_auroc_ci'][1])}) | "
            f"{_fmt(r['occ_spearman_mean'])} | {_fmt(r['fidelity_plus_mean'])} | "
            f"{_fmt(r['characterization_mean'])} |"
        )
    lines += ["", "⭐ = attributor the exact/proxy ground truth ranks best.", "",
              "_Faithfulness-only selection test_ — would a framework ranking by each "
              "metric pick the GT-best attributor?", "",
              "| faithfulness metric | its top pick | pick GT AUROC | GT-best | GT-best AUROC | "
              "mismatch? | paired Wilcoxon p | rank corr ρ(faith,GT) |",
              "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    rc = res.get("rank_correlation", {})
    for s in res["selections"]:
        rho = rc.get(s["faithfulness_metric"], {}).get("rho")
        lines.append(
            f"| {s['faithfulness_metric']} | {s['faithfulness_pick']} | "
            f"{_fmt(s['faithfulness_pick_gt_auroc'])} | {s['gt_best']} | "
            f"{_fmt(s['gt_best_gt_auroc'])} | {'**yes**' if s['mismatch'] else 'no'} | "
            f"{_fmt(s['paired_gt_pvalue'], 4)} | {_fmt(rho)} |"
        )
    lines.append("")
    return lines


def _conclusions(results: list[dict]) -> list[str]:
    """Write 'What this shows' from what was actually computed.

    This section used to be a fixed paragraph asserting that in-distribution
    'ρ near 1, no mismatch' and that shift mismatches at 'p < 0.001'. Those
    numbers were never read back from the run. On 3 August the report carried
    no in-distribution panel at all and the paragraph still described the
    contrast; the run's own in-distribution ρ was +0.36 with mismatches on two
    of three seeds. A generated report may not assert a number it did not
    compute (CLAUDE.md hard rule 1), so every claim below is derived here.
    """
    usable = [r for r in results if "error" not in r and r.get("selections")]
    lines = ["## What this shows", ""]
    if not usable:
        return lines + ["_No regime in this run yielded a selection test; "
                        "nothing is claimed._", ""]

    def summarise_one(res: dict) -> str:
        sels = res["selections"]
        rc = res.get("rank_correlation", {})
        rhos = [rc.get(s["faithfulness_metric"], {}).get("rho") for s in sels]
        rhos = [x for x in rhos if x is not None and x == x]
        n_mis = sum(1 for s in sels if s["mismatch"])
        rho_txt = (f"ρ ranges {min(rhos):+.2f} to {max(rhos):+.2f}"
                   if len(rhos) > 1 else
                   (f"ρ = {rhos[0]:+.2f}" if rhos else "ρ undefined"))
        agree = ("selects the ground-truth-best attributor on every metric"
                 if n_mis == 0 else
                 f"picks the wrong attributor on {n_mis} of {len(sels)} metrics")
        return (f"- **{res['dataset']} · {res['backbone']} · {res['split']} split**: "
                f"ranking by faithfulness {agree} ({rho_txt}).")

    for res in usable:
        lines.append(summarise_one(res))
    lines.append("")

    by_split = {r["split"]: r for r in usable}
    if {"random", "scaffold"} <= set(by_split):
        def mean_rho(res):
            rc = res.get("rank_correlation", {})
            xs = [rc.get(s["faithfulness_metric"], {}).get("rho")
                  for s in res["selections"]]
            xs = [x for x in xs if x is not None and x == x]
            return sum(xs) / len(xs) if xs else float("nan")
        r_in, r_sh = mean_rho(by_split["random"]), mean_rho(by_split["scaffold"])
        if r_in == r_in and r_sh == r_sh:
            lines += [
                f"Mean rank correlation falls from {r_in:+.2f} in-distribution to "
                f"{r_sh:+.2f} under scaffold shift ({r_sh - r_in:+.2f}). "
                + ("Faithfulness and correctness dissociate under shift, so a "
                   "faithfulness-only benchmark can recommend the wrong method in "
                   "exactly the regime that matters for drug discovery."
                   if r_sh < r_in else
                   "The two regimes do not separate in the expected direction here; "
                   "this run does not support the dissociation claim."),
                "",
            ]
    else:
        missing = {"random", "scaffold"} - set(by_split)
        lines += [
            f"Only the **{'/'.join(sorted(by_split))}** regime was analysed "
            f"(no {'/'.join(sorted(missing))} panel in this run), so no "
            "in-distribution-versus-shift contrast is claimed here.",
            "",
        ]
    lines += [
        "_Single-seed figures. Read `SEED_VARIANCE.md` before treating any "
        "attributor ranking above as an effect._",
        "",
    ]
    return lines


def write_report(cells=None, path: str | Path = "BENCHMARK_GT.md",
                 seed: int = 0, root: Path = AUDIT_ROOT) -> dict:
    cells = resolve_cells(cells, root=root)
    results = []
    lines = [
        "# BENCHMARK_GT.md — faithfulness-only evaluation vs ground truth",
        "",
        "> Computed from per-molecule audit records under `artifacts/audit/`; every",
        "> number is computed, none fixed. **Question:** does ranking attributors by a",
        "> faithfulness / fidelity metric — what SOTA evaluation frameworks",
        "> (GraphFramEx, MolFaith, DIG) emit — recover the attributor the *ground",
        "> truth* says is best? We contrast two regimes: in-distribution vs shift.",
        "",
        "`occ_spearman` = MolSanity occlusion faithfulness · `Fidelity+` and",
        "`characterization` = field-standard / GraphFramEx · `rank corr ρ` = Spearman",
        "correlation between the faithfulness metric and GT AUROC across attributors",
        "(≈1 → faithfulness tracks correctness; ≤0 → it does not).",
        "",
    ]
    if not cells:
        lines.append("_No cell in this run has >=2 attributors with "
                     "ground-truth records; the selection test is not "
                     "computable here. See PROGRESS.md for what failed._")
        lines.append("")
    for ds, bb, sp, regime in cells:
        res = analyse(ds, bb, sp, root=root, seed=seed)
        results.append(res)
        lines += _section(res, regime)

    lines += _conclusions(results)
    Path(path).write_text("\n".join(lines) + "\n")
    Path(path).with_suffix(".json").write_text(
        json.dumps(results, indent=2, default=float) + "\n")
    return {"results": results}


def main() -> None:
    out = write_report()
    print("Wrote BENCHMARK_GT.md")
    for res in out["results"]:
        if "error" in res:
            print(f"  {res['dataset']} {res['split']}: {res['error']}")
            continue
        for s in res["selections"]:
            tag = "MISMATCH" if s["mismatch"] else "match"
            print(f"  [{tag}] {res['dataset']}/{res['split']} {s['faithfulness_metric']}: "
                  f"picks {s['faithfulness_pick']} (GT {s['faithfulness_pick_gt_auroc']:.3f}) "
                  f"vs {s['gt_best']} ({s['gt_best_gt_auroc']:.3f}), p={s['paired_gt_pvalue']}")


if __name__ == "__main__":
    main()
