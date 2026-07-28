"""Calibration linkage + confidence/correctness regime stratification.

Under scaffold shift, we care *where* attributions become untrustworthy. Each
molecule is placed in a regime from its calibrated confidence and correctness:

  - ``confident_correct`` : confidence >= tau and prediction correct (conf-TP/TN)
  - ``confident_error``   : confidence >= tau and prediction wrong (dangerous)
  - ``borderline``        : confidence <  tau

We then report attribution reliability (GT AUROC, occlusion Spearman, stability)
*stratified by regime*, and the calibration linkage: correlation between
per-molecule confidence-calibration error and attribution reliability.
"""
from __future__ import annotations

import numpy as np


def assign_regime(confidence: float, correct: int, tau: float = 0.8) -> str:
    if confidence >= tau:
        return "confident_correct" if correct else "confident_error"
    return "borderline"


def confidence_from_logits(logits: np.ndarray, temperature: float = 1.0) -> tuple[int, float]:
    """Return (pred, max calibrated prob) for a single logit vector."""
    z = np.asarray(logits, dtype=np.float64) / max(temperature, 1e-6)
    z = z - z.max()
    e = np.exp(z)
    p = e / e.sum()
    return int(p.argmax()), float(p.max())


def stratify_by_regime(records, metric: str, tau: float = 0.8) -> dict:
    """Aggregate a metric per regime. ``records`` must carry .regime + metric."""
    out: dict[str, dict] = {}
    for regime in ("confident_correct", "confident_error", "borderline"):
        vals = np.array(
            [getattr(r, metric) for r in records if getattr(r, "regime", None) == regime],
            dtype=np.float64,
        )
        vals = vals[np.isfinite(vals)]
        out[regime] = {
            "n": int(vals.size),
            "mean": float(vals.mean()) if vals.size else float("nan"),
        }
    return out


def calibration_linkage(records, reliability_metric: str = "occ_spearman") -> dict:
    """Correlate per-molecule calibration error with attribution reliability.

    Calibration error per molecule = |confidence - correct|. A positive
    correlation between (1 - calib_error) and reliability supports the claim
    that better-calibrated predictions carry more trustworthy attributions.
    """
    from scipy.stats import spearmanr

    conf = np.array([getattr(r, "confidence", np.nan) for r in records], dtype=np.float64)
    correct = np.array([getattr(r, "correct", np.nan) for r in records], dtype=np.float64)
    rel = np.array([getattr(r, reliability_metric, np.nan) for r in records], dtype=np.float64)

    calib_err = np.abs(conf - correct)  # 0 = perfectly calibrated on this molecule
    mask = np.isfinite(calib_err) & np.isfinite(rel)
    if mask.sum() < 5 or np.std(calib_err[mask]) == 0 or np.std(rel[mask]) == 0:
        return {"spearman": float("nan"), "n": int(mask.sum()),
                "reliability_metric": reliability_metric}
    rho = spearmanr(1.0 - calib_err[mask], rel[mask]).correlation
    return {"spearman": float(rho), "n": int(mask.sum()),
            "reliability_metric": reliability_metric}
