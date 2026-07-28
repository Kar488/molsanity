"""Paired statistics for aggregating per-molecule audit records.

Bootstrap 95% CIs, Wilcoxon signed-rank (paired), fraction-positive, and a
simple paired effect size. NaNs are dropped with the count reported so we never
silently average over missing values.
"""
from __future__ import annotations

import numpy as np


def _clean(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=np.float64)
    return x[np.isfinite(x)]


def bootstrap_ci(x, n_boot: int = 2000, alpha: float = 0.05, seed: int = 0) -> dict:
    """Mean + bootstrap CI. Deterministic (seeded RNG)."""
    x = _clean(x)
    n = x.size
    if n == 0:
        return {"mean": float("nan"), "lo": float("nan"), "hi": float("nan"), "n": 0}
    if n == 1:
        return {"mean": float(x[0]), "lo": float(x[0]), "hi": float(x[0]), "n": 1}
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(n_boot, n))
    means = x[idx].mean(axis=1)
    lo, hi = np.quantile(means, [alpha / 2, 1 - alpha / 2])
    return {"mean": float(x.mean()), "lo": float(lo), "hi": float(hi), "n": int(n)}


def fraction_positive(x, threshold: float = 0.0) -> float:
    x = _clean(x)
    if x.size == 0:
        return float("nan")
    return float((x > threshold).mean())


def wilcoxon_vs_zero(x) -> dict:
    """Wilcoxon signed-rank test that the median of x differs from 0."""
    from scipy.stats import wilcoxon

    x = _clean(x)
    if x.size < 5 or np.all(x == 0):
        return {"stat": float("nan"), "pvalue": float("nan"), "n": int(x.size)}
    try:
        res = wilcoxon(x)
        return {"stat": float(res.statistic), "pvalue": float(res.pvalue), "n": int(x.size)}
    except Exception:
        return {"stat": float("nan"), "pvalue": float("nan"), "n": int(x.size)}


def paired_wilcoxon(a, b) -> dict:
    """Paired Wilcoxon signed-rank between two aligned samples a, b."""
    from scipy.stats import wilcoxon

    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    mask = np.isfinite(a) & np.isfinite(b)
    a, b = a[mask], b[mask]
    d = a - b
    if d.size < 5 or np.all(d == 0):
        return {"stat": float("nan"), "pvalue": float("nan"), "n": int(d.size),
                "median_diff": float(np.median(d)) if d.size else float("nan")}
    try:
        res = wilcoxon(a, b)
        return {"stat": float(res.statistic), "pvalue": float(res.pvalue),
                "n": int(d.size), "median_diff": float(np.median(d))}
    except Exception:
        return {"stat": float("nan"), "pvalue": float("nan"), "n": int(d.size),
                "median_diff": float(np.median(d))}


def summarise(x, name: str = "", seed: int = 0) -> dict:
    ci = bootstrap_ci(x, seed=seed)
    return {
        "name": name,
        "mean": ci["mean"],
        "ci95_lo": ci["lo"],
        "ci95_hi": ci["hi"],
        "median": float(np.median(_clean(x))) if _clean(x).size else float("nan"),
        "frac_positive": fraction_positive(x),
        "n": ci["n"],
    }
