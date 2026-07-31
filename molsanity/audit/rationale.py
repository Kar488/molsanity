"""Does the model actually use the ground-truth rationale on this molecule?

The standard objection to scoring attributions against a known rationale is
Faber et al. (KDD 2021): if the trained model solved the task some other way,
an attribution that points elsewhere is describing the model correctly, and
calling it "wrong" conflates a property of the model with a property of the
explanation. Every anti-aligned result in a ground-truth benchmark is open to
that reading.

The objection is testable, not merely arguable. Occlude the ground-truth
substructure and watch the prediction:

* If removing it collapses the prediction, the model *is* using it. An
  attribution that ranks those atoms low is then wrong by the model's own
  behaviour, not by disagreement with a chemical prior. Faber does not apply.
* If removing it barely moves the prediction, the model is not using it, and a
  low GT AUROC says something about the model, not the attribution. Faber
  applies, and the molecule should be excluded from correctness claims.

So each molecule is labelled with which case it is in, and the audit can report
its central finding on the subset where the objection provably does not hold.
That converts the reviewer's strongest criticism from an unanswerable framing
argument into a reported statistic.
"""
from __future__ import annotations

import numpy as np
import torch

from .occlusion import _batched_masked_logits


def rationale_use(model, data, gt_mask: np.ndarray, target: int,
                  task: str = "graph-classification",
                  baseline=None) -> dict:
    """Measure the model's reliance on the ground-truth substructure.

    Returns
    -------
    delta_gt
        Drop in the target-class probability (or in the standardised predicted
        value, for regression) when the ground-truth atoms are removed.
    delta_complement
        The same for removing everything *except* the ground-truth atoms. A
        model reading the motif alone moves little here.
    reliance
        ``delta_gt / (|delta_gt| + |delta_complement|)`` in [-1, 1]. Above zero
        the ground-truth substructure carries more of the prediction than the
        rest of the molecule does.
    uses_rationale
        True when removing the ground truth moves the prediction more than
        removing everything else, i.e. reliance > 0.5 of the total movement.
    """
    n = int(data.num_nodes)
    gt = np.asarray(gt_mask, dtype=np.float32).reshape(-1)
    if gt.shape[0] != n or gt.sum() == 0 or gt.sum() == n:
        return {"delta_gt": float("nan"), "delta_complement": float("nan"),
                "reliance": float("nan"), "uses_rationale": None,
                "n_gt_atoms": int(gt.sum())}

    keep_all = np.ones((1, n), dtype=np.float32)
    drop_gt = np.ones((1, n), dtype=np.float32)
    drop_gt[0, gt > 0] = 0.0
    drop_rest = np.ones((1, n), dtype=np.float32)
    drop_rest[0, gt == 0] = 0.0

    logits = _batched_masked_logits(
        model, data, np.concatenate([keep_all, drop_gt, drop_rest], axis=0),
        baseline=baseline)

    if task == "graph-regression":
        def score(row):
            return float(row[target])
    else:
        from ..models.calibration import softmax_1d

        def score(row):
            return float(softmax_1d(row)[target])

    base = score(logits[0])
    d_gt = base - score(logits[1])
    d_rest = base - score(logits[2])
    total = abs(d_gt) + abs(d_rest)
    reliance = float(d_gt / total) if total > 0 else float("nan")

    return {
        "delta_gt": float(d_gt),
        "delta_complement": float(d_rest),
        "reliance": reliance,
        "uses_rationale": bool(reliance > 0.5) if total > 0 else None,
        "n_gt_atoms": int(gt.sum()),
    }


def faber_partition(records) -> dict:
    """Split audited molecules by whether the Faber objection can apply.

    ``records`` are per-molecule audit records carrying ``rationale_reliance``
    and ``gt_auroc``. Returns the counts and the mean GT AUROC in each group,
    plus the headline number: among molecules the model demonstrably *does*
    read the ground-truth substructure from, how many still get an anti-aligned
    attribution? Those are attribution failures that no appeal to an
    alternative rationale can explain away.
    """
    uses, ignores = [], []
    for r in records:
        rel = r.get("rationale_reliance")
        gt = r.get("gt_auroc")
        if rel is None or gt is None:
            continue
        try:
            rel, gt = float(rel), float(gt)
        except (TypeError, ValueError):
            continue
        if rel != rel or gt != gt:  # NaN
            continue
        (uses if rel > 0.5 else ignores).append(gt)

    def _mean(xs):
        return float(np.mean(xs)) if xs else float("nan")

    anti_despite_use = [g for g in uses if g < 0.5]
    return {
        "n_uses_rationale": len(uses),
        "n_ignores_rationale": len(ignores),
        "mean_gt_auroc_when_used": _mean(uses),
        "mean_gt_auroc_when_ignored": _mean(ignores),
        # The number that answers Faber directly.
        "n_anti_aligned_despite_model_using_it": len(anti_despite_use),
        "frac_anti_aligned_despite_model_using_it":
            (len(anti_despite_use) / len(uses)) if uses else float("nan"),
    }


__all__ = ["rationale_use", "faber_partition"]
