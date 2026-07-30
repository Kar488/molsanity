"""Ground-truth accuracy: attribution-vs-GT-mask AUROC / AUPRC (Tier-1 only)."""
from __future__ import annotations

import numpy as np


def attribution_gt_scores(node_attr: np.ndarray, gt_mask: np.ndarray) -> dict:
    """AUROC/AUPRC of normalised node attribution against a binary GT node mask.

    Returns NaNs (with a reason) when the mask is degenerate (all-0 / all-1),
    which is honest: AUROC is undefined without both classes present.
    """
    from sklearn.metrics import average_precision_score, roc_auc_score

    from ..attributors.base import minmax_normalise

    a = minmax_normalise(node_attr)
    gt = (np.asarray(gt_mask) > 0).astype(int)
    pos = int(gt.sum())
    if pos == 0 or pos == gt.size:
        return {"auroc": float("nan"), "auprc": float("nan"),
                "n_pos": pos, "n": int(gt.size), "reason": "degenerate GT mask"}
    try:
        auroc = float(roc_auc_score(gt, a))
    except Exception:
        auroc = float("nan")
    try:
        auprc = float(average_precision_score(gt, a))
    except Exception:
        auprc = float("nan")
    # baseline AUPRC = prevalence, for interpretability
    return {"auroc": auroc, "auprc": auprc, "auprc_baseline": pos / gt.size,
            "n_pos": pos, "n": int(gt.size), "reason": ""}
