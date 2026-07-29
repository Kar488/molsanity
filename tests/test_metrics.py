"""Unit tests for audit metrics (no heavy torch/rdkit needed)."""
import numpy as np

from molsanity.audit.coherence import gini, salient_cc_fraction, top_k_mass
from molsanity.audit.groundtruth import attribution_gt_scores
from molsanity.audit.stats import bootstrap_ci, fraction_positive, paired_wilcoxon


def test_gini_bounds():
    assert gini(np.ones(10)) == 0.0  # perfectly equal -> 0
    concentrated = np.zeros(10); concentrated[0] = 1.0
    assert gini(concentrated) > 0.8  # highly concentrated -> near 1
    assert gini(np.zeros(5)) == 0.0  # all-zero guarded


def test_top_k_mass():
    x = np.array([10.0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    assert top_k_mass(x, 0.2) == 1.0  # all mass in top atom
    assert abs(top_k_mass(np.ones(10), 0.2) - 0.2) < 1e-9


def test_salient_cc_fraction_connected():
    # 4-node path 0-1-2-3, attribution high on 0,1 (connected)
    attr = np.array([1.0, 1.0, 0.0, 0.0])
    ei = np.array([[0, 1, 1, 2, 2, 3], [1, 0, 2, 1, 3, 2]])
    frac = salient_cc_fraction(attr, ei, quantile=0.5)
    assert frac == 1.0  # the two salient nodes are connected


def test_gt_scores_perfect_and_degenerate():
    gt = np.array([1, 1, 0, 0])
    perfect = np.array([0.9, 0.8, 0.1, 0.0])
    s = attribution_gt_scores(perfect, gt)
    assert s["auroc"] == 1.0
    # degenerate mask -> NaN with a reason, never a fabricated number
    s2 = attribution_gt_scores(perfect, np.zeros(4))
    assert np.isnan(s2["auroc"]) and s2["reason"]


def test_gt_scores_antialigned():
    gt = np.array([1, 1, 0, 0])
    anti = np.array([0.0, 0.1, 0.8, 0.9])
    s = attribution_gt_scores(anti, gt)
    assert s["auroc"] == 0.0  # anti-aligned attribution scores 0, honestly


def test_bootstrap_ci_deterministic():
    x = np.random.default_rng(0).normal(size=50)
    a = bootstrap_ci(x, seed=123)
    b = bootstrap_ci(x, seed=123)
    assert a == b  # seeded -> reproducible
    assert a["lo"] <= a["mean"] <= a["hi"]


def test_fraction_positive_and_paired():
    assert fraction_positive(np.array([1.0, -1.0, 2.0])) == 2 / 3
    res = paired_wilcoxon(np.array([2.0, 3, 4, 5, 6]), np.array([1.0, 1, 1, 1, 1]))
    assert res["n"] == 5


def test_characterization_score():
    from molsanity.audit.occlusion import characterization_score
    import numpy as np
    # perfect: fid+ = 1 (removing salient collapses prob), fid- = 0 (non-salient irrelevant)
    assert abs(characterization_score(1.0, 0.0) - 1.0) < 1e-9
    # worst: fid+ = 0, fid- = 1
    assert characterization_score(0.0, 1.0) != characterization_score(0.0, 1.0) or \
           characterization_score(0.0, 1.0) == 0.0  # NaN or 0 (degenerate)
    # monotonic-ish: higher fid+ (lower fid-) → higher score
    assert characterization_score(0.8, 0.1) > characterization_score(0.3, 0.4)
    # clips out-of-range inputs
    s = characterization_score(1.5, -0.5)
    assert 0.0 <= s <= 1.0
