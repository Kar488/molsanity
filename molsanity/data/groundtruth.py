"""Ground-truth attribution masks for Tier-1 datasets.

MUTAG has no per-atom explanation labels. We derive a chemically motivated
**quasi-ground-truth** node mask: the nitro group (an N bonded to >= 2 O), the
canonical mutagenicity motif for the nitroaromatic MUTAG compounds
(Debnath et al. 1991). This is a motif-level proxy, clearly labelled as such
(see LIMITATIONS.md), not annotator ground truth.

BA-2Motifs carries exact node ground truth (the injected motif nodes); when
present in the PyG object it is read directly.
"""
from __future__ import annotations

import numpy as np

from .chem import MUTAG_ATOMS

_C, _N, _O = 0, 1, 2  # MUTAG atom-type indices


def mutag_nitro_mask(data) -> np.ndarray:
    """Return a float node mask in {0,1}: 1 for atoms in a nitro (NO2) group.

    Detected structurally on the graph (an N with >= 2 O neighbours, plus those
    O atoms), which is robust to bond-order ambiguity in the reconstructed mol.
    """
    x = data.x.argmax(dim=1).numpy()
    n = x.shape[0]
    ei = data.edge_index.numpy()

    neighbors: list[list[int]] = [[] for _ in range(n)]
    for k in range(ei.shape[1]):
        a, b = int(ei[0, k]), int(ei[1, k])
        neighbors[a].append(b)

    mask = np.zeros(n, dtype=np.float32)
    for i in range(n):
        if x[i] == _N:
            oxy = [j for j in neighbors[i] if x[j] == _O]
            if len(set(oxy)) >= 2:
                mask[i] = 1.0
                for j in set(oxy):
                    mask[j] = 1.0
    return mask


def ba2motifs_node_mask(data) -> np.ndarray | None:
    """Read exact node ground truth from a BA-2Motifs graph if available."""
    for key in ("node_mask", "node_label", "y_node"):
        if hasattr(data, key) and getattr(data, key) is not None:
            val = getattr(data, key)
            arr = val.detach().cpu().numpy().astype(np.float32).reshape(-1)
            if arr.shape[0] == data.num_nodes:
                return (arr > 0).astype(np.float32)
    return None


def ground_truth_mask(dataset_name: str, data) -> np.ndarray | None:
    """Dispatch to the right GT extractor. Returns None when no GT is defined."""
    if dataset_name == "MUTAG":
        return mutag_nitro_mask(data)
    if dataset_name == "BA-2Motifs":
        return ba2motifs_node_mask(data)
    return None


def has_ground_truth(dataset_name: str) -> bool:
    return dataset_name in {"MUTAG", "BA-2Motifs"}


__all__ = [
    "mutag_nitro_mask",
    "ba2motifs_node_mask",
    "ground_truth_mask",
    "has_ground_truth",
    "MUTAG_ATOMS",
]
