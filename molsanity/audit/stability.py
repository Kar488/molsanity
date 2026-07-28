"""Cross-checkpoint stability of attributions.

An attribution that flips between an *early* and the *final* checkpoint of the
same training run is less trustworthy. For each molecule we compute the Spearman
correlation between motif-level attributions from the two checkpoints. High
correlation = stable; near-zero/negative = unstable.
"""
from __future__ import annotations

import numpy as np

from .motifs import decompose, motif_scores


def motif_attr_vector(model, attributor, data, dataset_name: str) -> np.ndarray:
    """Motif-level attribution scores for one molecule under a given model."""
    from ..data.chem import mol_from_data

    mol, _ = mol_from_data(data)
    decomp = decompose(data, mol=mol)
    attribution = attributor.attribute(data)
    return motif_scores(np.clip(attribution.node_attr, 0, None), decomp, reduce="sum")


def cross_checkpoint_stability(
    model_early, model_final, attr_early, attr_final, data, dataset_name: str
) -> float:
    """Spearman(motif attributions early, motif attributions final)."""
    from scipy.stats import spearmanr

    v_early = motif_attr_vector(model_early, attr_early, data, dataset_name)
    v_final = motif_attr_vector(model_final, attr_final, data, dataset_name)
    if v_early.size < 2 or np.std(v_early) == 0 or np.std(v_final) == 0:
        return float("nan")
    rho = spearmanr(v_early, v_final).correlation
    return float(rho)
