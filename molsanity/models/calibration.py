"""Temperature scaling for calibration + Expected Calibration Error.

Temperature scaling (Guo et al. 2017): fit a single scalar T on validation
logits by minimising NLL, then divide logits by T at inference. Used uniformly
across backbones so the calibration linkage in the audit is comparable.
"""
from __future__ import annotations

import numpy as np
import torch
from torch import nn


class TemperatureScaler(nn.Module):
    def __init__(self):
        super().__init__()
        self.log_t = nn.Parameter(torch.zeros(1))  # T = exp(log_t) >= 0, start at 1
        self.hit_bound = False

    @property
    def temperature(self) -> float:
        return float(self.log_t.exp().item())

    def forward(self, logits: torch.Tensor) -> torch.Tensor:
        return logits / self.log_t.exp()

    def fit(
        self,
        logits: torch.Tensor,
        labels: torch.Tensor,
        max_iter: int = 100,
        t_min: float = 0.1,
        t_max: float = 10.0,
    ):
        """Fit T by NLL, clamped to [t_min, t_max].

        On tiny or perfectly-separated validation sets, unconstrained NLL drives
        T -> 0 (degenerate over-sharpening). We clamp to a sane range so the
        calibration linkage reflects real over/under-confidence, not an optimiser
        artifact. ``hit_bound`` records when the clamp was active.
        """
        logits = logits.detach()
        labels = labels.detach().long()
        opt = torch.optim.LBFGS([self.log_t], lr=0.05, max_iter=max_iter)
        nll = nn.CrossEntropyLoss()

        def closure():
            opt.zero_grad()
            loss = nll(self(logits), labels)
            loss.backward()
            return loss

        opt.step(closure)
        raw_t = float(self.log_t.exp().item())
        clamped = min(max(raw_t, t_min), t_max)
        self.hit_bound = raw_t < t_min or raw_t > t_max
        with torch.no_grad():
            self.log_t.copy_(torch.log(torch.tensor([clamped])))
        return self


def softmax_np(logits: np.ndarray) -> np.ndarray:
    z = logits - logits.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def expected_calibration_error(
    probs: np.ndarray, labels: np.ndarray, n_bins: int = 10
) -> dict:
    """Return ECE + per-bin stats for confidence-vs-accuracy reliability."""
    conf = probs.max(axis=1)
    pred = probs.argmax(axis=1)
    correct = (pred == labels).astype(np.float64)

    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    per_bin = []
    n = len(labels)
    for lo, hi in zip(bins[:-1], bins[1:]):
        in_bin = (conf > lo) & (conf <= hi)
        count = int(in_bin.sum())
        if count == 0:
            per_bin.append({"lo": lo, "hi": hi, "count": 0, "acc": None, "conf": None})
            continue
        acc = float(correct[in_bin].mean())
        avg_conf = float(conf[in_bin].mean())
        ece += (count / n) * abs(acc - avg_conf)
        per_bin.append({"lo": lo, "hi": hi, "count": count, "acc": acc, "conf": avg_conf})
    return {"ece": float(ece), "n_bins": n_bins, "bins": per_bin}
