"""Ground-truth attribution masks for Tier-1 datasets.

MUTAG has no per-atom explanation labels. We derive a chemically motivated
**quasi-ground-truth** node mask: the nitro group (an N bonded to >= 2 O), the
canonical mutagenicity motif for the nitroaromatic MUTAG compounds
(Debnath et al. 1991). This is a motif-level proxy, clearly labelled as such
(see LIMITATIONS.md), not annotator ground truth.

BA-2Motifs carries exact node ground truth (the injected motif nodes), but
PyG's loader does not expose it: the released tensors are only ``x``,
``edge_index`` and a graph-level ``y``. We recover it from the dataset's node
ordering (the injected motif is appended after the Barabasi-Albert base) and
*verify* the recovery structurally before using it.
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
    # .cpu() before .numpy(): on a GPU run the graph has already been moved to
    # the device by the attribution step, and a bare .numpy() raises.
    x = data.x.argmax(dim=1).detach().cpu().numpy()
    n = x.shape[0]
    ei = data.edge_index.detach().cpu().numpy()

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


# A BA-2Motifs motif is five nodes: a *house* (a 4-cycle plus a roof node, six
# internal edges) or a five-*cycle* (five internal edges). Sorted degree
# sequences of the induced subgraph, which exclude the edges tying the motif to
# the Barabasi-Albert base:
_MOTIF_DEGREE_SEQUENCES = {
    (2, 2, 2, 3, 3): "house",
    (2, 2, 2, 2, 2): "cycle",
}
_BA2_MOTIF_SIZE = 5


def _induced_degree_sequence(data, nodes) -> tuple[int, ...] | None:
    """Sorted degrees of ``nodes`` in the subgraph they induce, or None."""
    ei = data.edge_index
    if ei is None:
        return None
    src = ei[0].detach().cpu().numpy()
    dst = ei[1].detach().cpu().numpy()
    member = set(int(v) for v in nodes)
    deg: dict[int, set[int]] = {v: set() for v in member}
    for u, v in zip(src, dst):
        u, v = int(u), int(v)
        if u in member and v in member and u != v:
            deg[u].add(v)
            deg[v].add(u)
    return tuple(sorted(len(s) for s in deg.values()))


def ba2motifs_trailing_motif_mask(data, motif_size: int = _BA2_MOTIF_SIZE):
    """Recover the injected-motif mask from BA-2Motifs' node ordering.

    The canonical PGExplainer release, which PyG's ``BA2MotifDataset`` loads
    without reordering, appends the injected motif after the Barabasi-Albert
    base, so the motif is always the final ``motif_size`` node indices. That is
    the convention every published evaluation on this dataset uses, but relying
    on position alone would silently produce a wrong mask if an upstream loader
    ever reordered nodes. So the positional guess is *verified*: the induced
    subgraph on those nodes must have the degree sequence of a house or a
    five-cycle. If it does not, we return ``None`` and the cell degrades to
    having no ground truth rather than being scored against a fabricated one.

    Returns ``(mask, motif_name)`` or ``None``.
    """
    n = int(data.num_nodes)
    if n <= motif_size:
        return None
    nodes = list(range(n - motif_size, n))
    seq = _induced_degree_sequence(data, nodes)
    name = _MOTIF_DEGREE_SEQUENCES.get(seq)
    if name is None:
        return None
    mask = np.zeros(n, dtype=np.float32)
    mask[nodes] = 1.0
    return mask, name


def ba2motifs_node_mask(data) -> np.ndarray | None:
    """Exact node ground truth for a BA-2Motifs graph.

    Prefers an explicit per-node label if the loader supplies one. PyG's
    ``BA2MotifDataset`` does not: it carries only ``x``, ``edge_index`` and a
    graph-level ``y``, which is why this dataset previously contributed no
    ground-truth cells at all. We fall back to the structurally verified
    trailing-motif convention.
    """
    for key in ("node_mask", "node_label", "y_node", "node_gt"):
        if hasattr(data, key) and getattr(data, key) is not None:
            val = getattr(data, key)
            arr = val.detach().cpu().numpy().astype(np.float32).reshape(-1)
            if arr.shape[0] == data.num_nodes:
                return (arr > 0).astype(np.float32)
    found = ba2motifs_trailing_motif_mask(data)
    return None if found is None else found[0]


def synth_motifs_node_mask(data) -> np.ndarray | None:
    """Exact node ground truth for the synthetic motif dataset."""
    if hasattr(data, "node_gt") and data.node_gt is not None:
        return data.node_gt.detach().cpu().numpy().astype(np.float32).reshape(-1)
    return None


def ground_truth_mask(dataset_name: str, data) -> np.ndarray | None:
    """Dispatch to the right GT extractor. Returns None when no GT is defined."""
    if dataset_name == "MUTAG":
        return mutag_nitro_mask(data)
    if dataset_name == "BA-2Motifs":
        return ba2motifs_node_mask(data)
    if dataset_name.startswith("SynthMotifs") or dataset_name == "ShapeGGen":
        # Both carry an exact per-node mask on the graph object as ``node_gt``.
        return synth_motifs_node_mask(data)
    return None


def has_ground_truth(dataset_name: str) -> bool:
    # Any SynthMotifs* variant (e.g. SynthMotifsXL) carries exact node_gt.
    return (dataset_name in {"MUTAG", "BA-2Motifs", "ShapeGGen"}
            or dataset_name.startswith("SynthMotifs"))


__all__ = [
    "mutag_nitro_mask",
    "ba2motifs_node_mask",
    "ba2motifs_trailing_motif_mask",
    "ground_truth_mask",
    "has_ground_truth",
    "MUTAG_ATOMS",
]
