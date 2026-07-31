"""Abstention: when should an attribution not be trusted?

The audit's headline is a negative — no faithfulness metric tells you which
attributor to pick without ground truth. A reviewer is right to ask what a
practitioner does with that. Reframing from *which explanation to choose* to
*when to trust any of them* is answerable, and these tests pin that the
machinery reports a real relationship when one exists and reports its absence
when one does not, rather than manufacturing a recommendation either way.
"""
from __future__ import annotations

import numpy as np
import pytest

from molsanity.audit.abstention import (
    coverage_reliability_curve,
    load_all_records,
    operating_point,
    rank_signals,
    risk_operating_point,
    write_abstention_md,
)


def _records(pairs, signal="confidence", **extra):
    """One record per (signal value, gt_auroc) pair."""
    return [{signal: s, "gt_auroc": g, **extra} for s, g in pairs]


def _informative(n=60):
    """A signal that genuinely predicts localisation: gt tracks the signal."""
    rng = np.random.default_rng(0)
    conf = rng.uniform(0.5, 1.0, n)
    gt = np.clip(conf + rng.normal(0, 0.03, n), 0, 1)
    return _records(list(zip(conf, gt)))


def _uninformative(n=60):
    """A signal unrelated to localisation."""
    rng = np.random.default_rng(1)
    return _records(list(zip(rng.uniform(0.5, 1.0, n), rng.uniform(0, 1, n))))


# ------------------------------------------------------------------ curve ---
def test_reliability_rises_as_coverage_falls_for_an_informative_signal():
    curve = coverage_reliability_curve(_informative(), "confidence")
    assert len(curve) > 3
    assert curve[0]["coverage"] == pytest.approx(1.0, abs=0.02)
    # Monotone-ish: keeping the best half must beat keeping everything.
    half = min(curve, key=lambda p: abs(p["coverage"] - 0.5))
    assert half["mean_target"] > curve[0]["mean_target"]
    assert half["frac_below_chance"] <= curve[0]["frac_below_chance"]


def test_uninformative_signal_produces_no_meaningful_lift():
    ranked = rank_signals(_uninformative())
    assert ranked, "a curve should still be computed"
    assert abs(ranked[0]["lift"]) < 0.2, (
        "an unrelated signal must not appear to buy reliability")


def test_curve_needs_enough_molecules():
    """Better to report nothing than a curve over five points."""
    assert coverage_reliability_curve(_records([(0.9, 0.8)] * 4), "confidence") == []


def test_records_missing_either_field_are_dropped_not_defaulted():
    recs = _informative(40) + [{"confidence": 0.99}, {"gt_auroc": 0.99},
                               {"confidence": float("nan"), "gt_auroc": 0.5}]
    curve = coverage_reliability_curve(recs, "confidence")
    assert curve[0]["n_kept"] == 40


# --------------------------------------------------------- operating point ---
def test_operating_point_is_the_widest_coverage_that_clears_the_bar():
    curve = coverage_reliability_curve(_informative(), "confidence")
    op = operating_point(curve, min_reliability=0.8)
    assert op is not None
    assert op["mean_target"] >= 0.8
    wider = [p for p in curve if p["coverage"] > op["coverage"]]
    assert all(p["mean_target"] < 0.8 for p in wider)


def test_no_operating_point_when_the_bar_is_unreachable():
    curve = coverage_reliability_curve(_informative(), "confidence")
    assert operating_point(curve, min_reliability=1.5) is None


# ----------------------------------------------------------------- report ---
def test_rule_is_never_stated_as_keep_everything(tmp_path):
    """The first real run produced "keep the top 100%, threshold >= -1.000".

    That is not a rule. It happened because the criterion was the *mean*, which
    already cleared the bar at full coverage. The criterion is now the share of
    retained explanations that are below chance, which full coverage cannot
    trivially satisfy when that share is large.
    """
    rng = np.random.default_rng(7)
    n = 200
    conf = rng.uniform(0.5, 1.0, n)
    # Mean localisation is high (0.72) but a quarter are below chance, exactly
    # the shape of the real data.
    gt = np.where(rng.random(n) < 0.25, rng.uniform(0.0, 0.5, n),
                  rng.uniform(0.8, 1.0, n))
    gt = np.clip(gt + (conf - 0.75) * 0.5, 0, 1)
    out = tmp_path / "ABSTENTION.md"
    write_abstention_md(_records(list(zip(conf, gt))), out,
                        min_reliability=0.7, max_below_chance=0.10)
    text = out.read_text()
    assert "top 100%" not in text, "the rule degenerated to keeping everything"
    assert "below chance" in text
    # It should also flag that a mean-based rule would have been vacuous.
    assert "vacuous" in text or "does not solve it" in text or "not needed" in text


def test_risk_operating_point_targets_the_tail_not_the_mean():
    curve = [
        {"coverage": 1.00, "n_kept": 100, "mean_target": 0.72,
         "frac_below_chance": 0.25, "threshold": -1.0},
        {"coverage": 0.70, "n_kept": 70, "mean_target": 0.80,
         "frac_below_chance": 0.12, "threshold": 0.4},
        {"coverage": 0.50, "n_kept": 50, "mean_target": 0.86,
         "frac_below_chance": 0.06, "threshold": 0.6},
        {"coverage": 0.30, "n_kept": 30, "mean_target": 0.91,
         "frac_below_chance": 0.02, "threshold": 0.8},
    ]
    got = risk_operating_point(curve, max_below_chance=0.10)
    assert got["coverage"] == 0.50, "must take the WIDEST coverage that qualifies"
    assert risk_operating_point(curve, max_below_chance=0.30)["coverage"] == 1.00
    assert risk_operating_point(curve, max_below_chance=0.001) is None


def test_report_recommends_a_rule_when_one_exists(tmp_path):
    out = tmp_path / "ABSTENTION.md"
    res = write_abstention_md(_informative(), out, min_reliability=0.8)
    text = out.read_text()
    assert res["n_signals"] >= 1
    assert "Recommended rule" in text
    assert "confidence" in text
    assert "transfer assumption" in text.lower()
    assert "top 100%" not in text


def test_report_says_so_plainly_when_no_signal_works(tmp_path):
    """A null result must be reported as one, not dressed up as a rule."""
    rng = np.random.default_rng(2)
    n = 60
    # gt_auroc falls as confidence rises: every signal has negative lift.
    conf = rng.uniform(0.5, 1.0, n)
    recs = _records(list(zip(conf, 1.0 - conf)))
    out = tmp_path / "ABSTENTION.md"
    write_abstention_md(recs, out)
    text = out.read_text()
    assert "No usable rule" in text
    assert "Recommended rule" not in text


def test_report_handles_having_nothing_to_report(tmp_path):
    out = tmp_path / "ABSTENTION.md"
    res = write_abstention_md([], out)
    assert res["n_signals"] == 0
    assert "no curve can be computed" in out.read_text().lower()


def test_signals_are_ranked_by_lift():
    """The useful signal must come first, so the report recommends the right one."""
    rng = np.random.default_rng(3)
    n = 60
    good = rng.uniform(0.5, 1.0, n)
    gt = np.clip(good + rng.normal(0, 0.02, n), 0, 1)
    noise = rng.uniform(0, 1, n)
    recs = [{"confidence": float(c), "stability": float(s), "gt_auroc": float(g)}
            for c, s, g in zip(good, noise, gt)]
    ranked = rank_signals(recs)
    assert ranked[0]["signal"] == "confidence"
    assert ranked[0]["lift"] > ranked[-1]["lift"]


# ------------------------------------------------------------------ loader ---
def test_load_all_records_tags_each_with_its_cell(tmp_path):
    import json

    root = tmp_path / "audit"
    for cell in ("MUTAG__GINE__IG__scaffold", "SynthMotifs__GINE__IG__random"):
        d = root / cell
        d.mkdir(parents=True)
        (d / "records.json").write_text(json.dumps([{"graph_id": 1, "gt_auroc": 0.5}]))
    # A partially written file must not take the whole run down.
    bad = root / "broken__cell"
    bad.mkdir(parents=True)
    (bad / "records.json").write_text("{not json")

    recs = load_all_records(root)
    assert len(recs) == 2
    assert {r["cell"] for r in recs} == {"MUTAG__GINE__IG__scaffold",
                                         "SynthMotifs__GINE__IG__random"}


def test_load_all_records_on_a_missing_directory():
    assert load_all_records("/nonexistent/path/audit") == []
