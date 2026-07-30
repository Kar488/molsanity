"""Cross-checkpoint stability of attributions.

An attribution that flips between an *early* and the *final* checkpoint of the
same training run is less trustworthy. For each molecule we compute the Spearman
correlation between motif-level attributions from the two checkpoints. High
correlation = stable; near-zero/negative = unstable.
"""
from __future__ import annotations

import numpy as np

from .motifs import motif_scores


def _motif_vector(node_attr: np.ndarray, decomp) -> np.ndarray:
    return motif_scores(np.clip(node_attr, 0, None), decomp, reduce="sum")


def cross_checkpoint_stability(early_attr, data, decomp, final_node_attr) -> float:
    """Spearman(early motif attributions, final motif attributions).

    The final attribution is already computed in the audit loop and passed in as
    ``final_node_attr``; the shared motif ``decomp`` is reused for both. Only the
    *early* checkpoint's attribution is (re)computed here.
    """
    from scipy.stats import spearmanr

    v_final = _motif_vector(final_node_attr, decomp)
    v_early = _motif_vector(early_attr.attribute(data).node_attr, decomp)
    if v_early.size < 2 or np.std(v_early) == 0 or np.std(v_final) == 0:
        return float("nan")
    return float(spearmanr(v_early, v_final).correlation)
