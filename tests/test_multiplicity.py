"""Benjamini-Hochberg adjustment used by the manuscript's tables.

Every paired test in the paper belongs to a family: the selection tests across
cells, and the attributor-vs-attributor contrasts within a cell. Reporting raw
p-values across dozens of these inflates the false discovery rate, which is why
the tables previously carried a note telling the reader to treat them as
descriptive. These tests pin the adjustment against scipy's implementation and
against the properties a reader relies on.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "paper" / "figs"))

import msdata as D  # noqa: E402


def test_matches_scipy_on_the_canonical_example():
    scipy_fdr = pytest.importorskip("scipy.stats").false_discovery_control
    p = [0.001, 0.008, 0.039, 0.041, 0.042, 0.06, 0.074,
         0.205, 0.212, 0.216, 0.222, 0.435, 0.5]
    np.testing.assert_allclose(D.benjamini_hochberg(p),
                               scipy_fdr(np.array(p), method="bh"), atol=1e-12)


def test_matches_scipy_on_random_families():
    scipy_fdr = pytest.importorskip("scipy.stats").false_discovery_control
    rng = np.random.default_rng(0)
    for _ in range(100):
        p = rng.random(int(rng.integers(2, 40)))
        np.testing.assert_allclose(D.benjamini_hochberg(list(p)),
                                   scipy_fdr(p, method="bh"), atol=1e-12)


def test_adjusted_values_never_shrink():
    """An adjustment that made a p-value smaller would be a bug, not a control."""
    rng = np.random.default_rng(1)
    for _ in range(50):
        p = rng.random(int(rng.integers(2, 25)))
        q = np.array(D.benjamini_hochberg(list(p)))
        assert np.all(q >= p - 1e-12)
        assert np.all(q <= 1.0 + 1e-12)


def test_ordering_is_preserved():
    p = [0.5, 0.01, 0.2, 0.001]
    q = D.benjamini_hochberg(p)
    assert [i for i, _ in sorted(enumerate(p), key=lambda t: t[1])] == \
           [i for i, _ in sorted(enumerate(q), key=lambda t: t[1])]


def test_undefined_tests_do_not_count_towards_the_family():
    """A test that could not be computed was not a test that was performed.

    Several selection rows have no p-value because the faithfulness pick and
    the ground-truth pick are the same attributor. Counting those would inflate
    the family size and make the real contrasts look weaker than they are.
    """
    with_nans = [0.01, float("nan"), 0.02, float("nan")]
    without = [0.01, 0.02]
    got = [q for q in D.benjamini_hochberg(with_nans) if q == q]
    np.testing.assert_allclose(got, D.benjamini_hochberg(without), atol=1e-12)
    assert np.isnan(D.benjamini_hochberg(with_nans)[1])


def test_empty_and_single_families():
    assert D.benjamini_hochberg([]) == []
    assert D.benjamini_hochberg([float("nan")])[0] != D.benjamini_hochberg([0.5])[0]
    assert D.benjamini_hochberg([0.42]) == [pytest.approx(0.42)]


def test_headline_contrast_survives_correction():
    """The paper's central claim must hold after FDR control, not just before.

    Recomputed from the committed per-molecule records, so this fails if a
    future run weakens the result rather than silently reporting the old text.
    """
    arms = [("MUTAG", "GINE"), ("SynthMotifs", "GINE")]
    pvals, labels = [], []
    for ds, bb in arms:
        for split in ("random", "scaffold"):
            sel = D.selection_test(ds, bb, split)
            if sel is None:
                pytest.skip(f"no committed records for {ds}/{bb}/{split}")
            for x in sel["selections"]:
                pvals.append(x["paired_gt_pvalue"])
                labels.append((ds, split, x["faithfulness_metric"], x["mismatch"]))

    qs = D.benjamini_hochberg(pvals)
    shift_mismatches = [(lab, q) for lab, q in zip(labels, qs)
                        if lab[0] == "MUTAG" and lab[1] == "scaffold" and lab[3]]
    assert shift_mismatches, "expected mismatches on the MUTAG shift arm"
    for lab, q in shift_mismatches:
        assert q < 0.05, f"{lab} no longer survives FDR control (q={q})"
