"""Coherence battery: does an attribution concentrate mass sensibly?

Metrics (per molecule), all in [0, 1] unless noted:
  - atom_gini:            Gini coefficient of node attribution mass (concentration)
  - top20_mass:           fraction of total mass in the top-20% of atoms
  - salient_cc_frac:      largest-connected-component fraction among salient atoms
  - motif_top1_share:     fraction of mass in the single most-attributed motif

These characterise *coherence* (concentration + connectedness + motif-alignment),
distinct from *faithfulness* (occlusion) and *correctness* (ground truth).
"""
from __future__ import annotations

import numpy as np

from .motifs import MotifDecomposition, primary_motif_share


def gini(x: np.ndarray) -> float:
    a = np.clip(np.asarray(x, dtype=np.float64), 0, None)
    if a.sum() <= 0 or a.size == 0:
        return 0.0
    a = np.sort(a)
    n = a.size
    idx = np.arange(1, n + 1)
    return float((np.sum((2 * idx - n - 1) * a)) / (n * a.sum()))


def top_k_mass(x: np.ndarray, frac: float = 0.2) -> float:
    a = np.clip(np.asarray(x, dtype=np.float64), 0, None)
    total = a.sum()
    if total <= 0:
        return 0.0
    k = max(1, int(np.ceil(frac * a.size)))
    topk = np.sort(a)[::-1][:k]
    return float(topk.sum() / total)


def salient_cc_fraction(
    node_attr: np.ndarray, edge_index: np.ndarray, quantile: float = 0.8
) -> float:
    """Largest connected component among salient (top-quantile) atoms / #salient."""
    a = np.clip(np.asarray(node_attr, dtype=np.float64), 0, None)
    n = a.size
    if n == 0 or a.sum() <= 0:
        return 0.0
    thr = np.quantile(a, quantile)
    salient = set(np.where(a >= thr)[0].tolist())
    if not salient:
        return 0.0

    adj: dict[int, list[int]] = {i: [] for i in salient}
    for k in range(edge_index.shape[1]):
        u, v = int(edge_index[0, k]), int(edge_index[1, k])
        if u in salient and v in salient:
            adj[u].append(v)

    seen: set[int] = set()
    best = 0
    for s in salient:
        if s in seen:
            continue
        stack, comp = [s], 0
        while stack:
            node = stack.pop()
            if node in seen:
                continue
            seen.add(node)
            comp += 1
            stack.extend(adj[node])
        best = max(best, comp)
    return float(best / len(salient))


def coherence_battery(
    node_attr: np.ndarray,
    edge_index: np.ndarray,
    decomp: MotifDecomposition,
) -> dict:
    return {
        "atom_gini": gini(node_attr),
        "top20_mass": top_k_mass(node_attr, 0.2),
        "salient_cc_frac": salient_cc_fraction(node_attr, edge_index, 0.8),
        "motif_top1_share": primary_motif_share(node_attr, decomp),
    }
