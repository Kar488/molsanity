"""When should a chemist decline to trust an attribution?

The audit's uncomfortable result is that no faithfulness metric tells you which
attributor to pick when no ground truth exists. That is a negative, and a
reviewer is right to ask what a practitioner does with it. This module answers a
different and answerable question: not *which explanation to choose*, but *when
to trust any of them*.

That is selective prediction applied to explanations. Rank molecules by a signal
available at inference time, abstain on the worst, and measure what the retained
set buys you. The output is a coverage-reliability curve: at each coverage level,
the mean ground-truth localisation of the molecules you kept. A signal is useful
exactly when reliability rises as coverage falls, and the curve says by how much,
in units a chemist can act on ("keep the top 60% by confidence and localisation
goes from 0.55 to 0.71").

Several signals are scored side by side because the useful one is not obvious a
priori, and because a signal that does *not* work is worth reporting: it means
the corresponding intuition ("trust the confident predictions", "trust the
faithful explanations") is unsupported on this data.

Nothing here can be evaluated without ground truth, so it runs on the Tier-1
arms and is then a *recommendation* transferred to the cells where correctness
cannot be measured. That transfer is the assumption, and it is stated rather
than hidden.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from ..utils import get_logger

log = get_logger()

# Signals available without ground truth, i.e. things a practitioner actually
# has at inference time. ``higher_is_better`` says which end to keep.
SIGNALS = {
    "confidence": True,        # calibrated max-class probability
    "occ_spearman": True,      # the audit's own faithfulness measure
    "stability": True,         # agreement across checkpoints
    "motif_top1_share": True,  # attribution concentration
    "rationale_reliance": True,  # does the model read the GT substructure
}

_TARGET = "gt_auroc"


def _finite(records, field):
    out = []
    for r in records:
        v = r.get(field)
        try:
            v = float(v)
        except (TypeError, ValueError):
            continue
        if not math.isnan(v):
            out.append((r, v))
    return out


def coverage_reliability_curve(records, signal: str, target: str = _TARGET,
                               steps: int = 11) -> list[dict]:
    """Reliability of the retained set as coverage falls from 1 to ~0.1.

    At each coverage level the molecules with the *worst* signal are abstained
    on, and the mean ``target`` over what remains is reported.
    """
    higher_better = SIGNALS.get(signal, True)
    pairs = [(r, v) for r, v in _finite(records, signal)
             if isinstance(r.get(target), (int, float))
             and not math.isnan(float(r[target]))]
    if len(pairs) < 10:
        return []
    pairs.sort(key=lambda t: t[1], reverse=higher_better)
    targets = np.array([float(r[target]) for r, _ in pairs])

    curve = []
    n = len(pairs)
    for i in range(steps):
        cov = 1.0 - i * (0.9 / max(1, steps - 1))
        k = max(5, int(round(cov * n)))
        if k > n:
            continue
        kept = targets[:k]
        curve.append({
            "coverage": k / n,
            "n_kept": int(k),
            "mean_target": float(kept.mean()),
            "frac_below_chance": float((kept < 0.5).mean()),
            "threshold": float(pairs[k - 1][1]),
        })
    return curve


def operating_point(curve, min_reliability: float = 0.7) -> dict | None:
    """The highest coverage at which mean reliability clears the bar."""
    ok = [p for p in curve if p["mean_target"] >= min_reliability]
    return max(ok, key=lambda p: p["coverage"]) if ok else None


def rank_signals(records, target: str = _TARGET) -> list[dict]:
    """Which abstention signal actually buys reliability, and how much?

    ``lift`` is the gain in mean target between full coverage and 50% coverage.
    A signal with lift <= 0 is not merely weak, it is useless for abstention on
    this data, and saying so is the point.
    """
    out = []
    for signal in SIGNALS:
        curve = coverage_reliability_curve(records, signal, target)
        if not curve:
            continue
        full = curve[0]["mean_target"]
        half = min(curve, key=lambda p: abs(p["coverage"] - 0.5))
        out.append({
            "signal": signal,
            "n": curve[0]["n_kept"],
            "mean_at_full_coverage": full,
            "mean_at_half_coverage": half["mean_target"],
            "lift": half["mean_target"] - full,
            "frac_below_chance_full": curve[0]["frac_below_chance"],
            "frac_below_chance_half": half["frac_below_chance"],
            "curve": curve,
        })
    out.sort(key=lambda d: d["lift"], reverse=True)
    return out


def write_abstention_md(records, out_path: str | Path = "ABSTENTION.md",
                        min_reliability: float = 0.7) -> dict:
    ranked = rank_signals(records)
    out = Path(out_path)
    L = ["# ABSTENTION.md — when not to trust an attribution", ""]

    if not ranked:
        L += ["_No molecule carries both a ground-truth score and an abstention "
              "signal, so no curve can be computed. This needs Tier-1 cells with "
              "per-molecule records._", ""]
        out.write_text("\n".join(L) + "\n")
        return {"signals": [], "n_signals": 0}

    L += ["The audit cannot tell a practitioner which attributor to pick without "
          "ground truth. It can tell them when to decline to trust one. Each "
          "signal below is available at inference time; molecules with the worst "
          "values are abstained on, and the table reports the ground-truth "
          "localisation of what remains.",
          "",
          "`lift` is the gain in mean GT AUROC between keeping everything and "
          "keeping the best half. **A signal with lift <= 0 is useless for "
          "abstention on this data**, which is itself worth knowing: it means the "
          "corresponding intuition is unsupported.",
          "",
          "| signal | n | GT AUROC @100% | @50% | lift | below chance @100% | @50% |",
          "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for d in ranked:
        L.append(f"| {d['signal']} | {d['n']} | {d['mean_at_full_coverage']:.3f} "
                 f"| {d['mean_at_half_coverage']:.3f} | {d['lift']:+.3f} "
                 f"| {d['frac_below_chance_full']:.3f} "
                 f"| {d['frac_below_chance_half']:.3f} |")
    L.append("")

    best = ranked[0]
    if best["lift"] > 0:
        op = operating_point(best["curve"], min_reliability)
        L += [f"## Recommended rule", "",
              f"Rank molecules by **{best['signal']}** and abstain on the tail."]
        if op:
            L.append(f"Keeping the top **{op['coverage']:.0%}** gives mean GT "
                     f"AUROC **{op['mean_target']:.3f}** (n={op['n_kept']}), with "
                     f"{op['frac_below_chance']:.1%} of retained molecules still "
                     f"below chance. Threshold: {best['signal']} >= "
                     f"{op['threshold']:.3f}.")
        else:
            L.append(f"No coverage level reaches mean GT AUROC "
                     f"{min_reliability:.2f}, so on this data there is no "
                     f"operating point that would make an attribution "
                     f"trustworthy by that standard. That is a negative result "
                     f"and is reported as one.")
    else:
        L += ["## No usable rule", "",
              "No signal available at inference time buys reliability on this "
              "data: the best lift is "
              f"{best['lift']:+.3f} ({best['signal']}). Abstaining on any of "
              "these signals retains molecules no better localised than the "
              "ones it discards."]
    L += ["", "---", "",
          "**The transfer assumption.** These curves are computed where ground "
          "truth exists. Applying the rule to a real molecular dataset assumes "
          "the signal-reliability relationship carries over to cells where "
          "correctness cannot be measured. This paper's central finding is that "
          "such transfer fails across splits, so the assumption is stated here "
          "rather than relied on silently.", ""]

    out.write_text("\n".join(L) + "\n")
    log.info("Wrote %s (%d signals ranked)", out, len(ranked))
    return {"signals": [{k: v for k, v in d.items() if k != "curve"}
                        for d in ranked], "n_signals": len(ranked)}


def load_all_records(root: str | Path = "artifacts/audit") -> list[dict]:
    """Every per-molecule record the run has written so far, tagged by cell.

    Abstention is a question about molecules, not cells, so the curves are
    computed over the pooled Tier-1 records. The cell identity is kept on each
    record so a caller can re-split if needed.
    """
    import json

    out: list[dict] = []
    base = Path(root)
    if not base.is_dir():
        return out
    for rec_file in sorted(base.glob("*/records.json")):
        try:
            recs = json.loads(rec_file.read_text())
        except Exception:  # noqa: BLE001 - a partial write must not kill the run
            continue
        cell = rec_file.parent.name
        for r in recs:
            if isinstance(r, dict):
                out.append({**r, "cell": cell})
    return out


__all__ = ["coverage_reliability_curve", "operating_point", "rank_signals",
           "write_abstention_md", "load_all_records", "SIGNALS"]
