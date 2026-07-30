"""RDKit motif decomposition + node->motif attribution aggregation.

Motifs used (per brief):
  - SSSR rings (smallest set of smallest rings)
  - Bemis-Murcko scaffold (as one motif)
  - Fragment decomposition (BRICS bonds -> connected fragments)

A motif is a set of atom indices. We also return a per-atom "primary motif"
assignment for the top-1 motif-share coherence metric.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from ..data.chem import graph_to_mol


@dataclass
class MotifDecomposition:
    motifs: list[list[int]]  # each is a list of atom indices
    motif_types: list[str]   # parallel: "ring" | "scaffold" | "fragment"
    num_atoms: int
    meta: dict = field(default_factory=dict)

    def coverage(self) -> float:
        covered = set()
        for m in self.motifs:
            covered.update(m)
        return len(covered) / max(1, self.num_atoms)


def _sssr_rings(mol) -> list[list[int]]:
    from rdkit import Chem

    rings = []
    try:
        for ring in Chem.GetSymmSSSR(mol):
            rings.append(list(ring))
    except Exception:
        pass
    return rings


def _murcko_atoms(mol) -> list[int]:
    from rdkit.Chem.Scaffolds import MurckoScaffold

    try:
        core = MurckoScaffold.GetScaffoldForMol(mol)
        if core is None or core.GetNumAtoms() == 0:
            return []
        match = mol.GetSubstructMatch(core)
        return list(match)
    except Exception:
        return []


def _brics_fragments(mol) -> list[list[int]]:
    from rdkit import Chem
    from rdkit.Chem import BRICS

    try:
        bonds = list(BRICS.FindBRICSBonds(mol))
        if not bonds:
            return [list(range(mol.GetNumAtoms()))]
        bond_indices = []
        for (a1, a2), _ in bonds:
            b = mol.GetBondBetweenAtoms(a1, a2)
            if b is not None:
                bond_indices.append(b.GetIdx())
        if not bond_indices:
            return [list(range(mol.GetNumAtoms()))]
        frag_mol = Chem.FragmentOnBonds(mol, bond_indices, addDummies=False)
        frags = Chem.GetMolFrags(frag_mol, sanitizeFrags=False)
        return [list(f) for f in frags]
    except Exception:
        return [list(range(mol.GetNumAtoms()))]


def decompose(data, mol=None) -> MotifDecomposition:
    """Full motif decomposition for a molecular graph (dataset-agnostic).

    Uses SMILES when available, else MUTAG-style reconstruction. If no valid
    mol is available or its atom count disagrees with the graph, falls back to
    per-atom singleton motifs over ``data.num_nodes`` so the audit still runs.
    """
    from ..data.chem import mol_from_data

    n_nodes = int(data.num_nodes)
    if mol is None:
        mol, _ = mol_from_data(data)
    if mol is None or mol.GetNumAtoms() != n_nodes:
        return MotifDecomposition(
            motifs=[[i] for i in range(n_nodes)],
            motif_types=["atom"] * n_nodes, num_atoms=n_nodes,
            meta={"fallback": "singleton-atoms"},
        )
    n = mol.GetNumAtoms()

    motifs: list[list[int]] = []
    types: list[str] = []

    for r in _sssr_rings(mol):
        if r:
            motifs.append(r)
            types.append("ring")

    scaf = _murcko_atoms(mol)
    if scaf:
        motifs.append(scaf)
        types.append("scaffold")

    for f in _brics_fragments(mol):
        if len(f) > 1:  # skip singletons; captured as fallback below
            motifs.append(f)
            types.append("fragment")

    if not motifs:
        motifs = [[i] for i in range(n)]
        types = ["atom"] * n

    return MotifDecomposition(motifs=motifs, motif_types=types, num_atoms=n)


def motif_scores(node_attr: np.ndarray, decomp: MotifDecomposition, reduce: str = "sum") -> np.ndarray:
    """Aggregate node attribution to a score per motif."""
    scores = np.zeros(len(decomp.motifs))
    a = np.asarray(node_attr, dtype=np.float64)
    for i, m in enumerate(decomp.motifs):
        if not m:
            continue
        vals = a[m]
        scores[i] = vals.sum() if reduce == "sum" else vals.mean()
    return scores


def primary_motif_share(node_attr: np.ndarray, decomp: MotifDecomposition) -> float:
    """Fraction of total (positive) attribution mass in the single top motif."""
    a = np.clip(np.asarray(node_attr, dtype=np.float64), 0, None)
    total = a.sum()
    if total <= 0 or not decomp.motifs:
        return 0.0
    scores = motif_scores(a, decomp, reduce="sum")
    return float(scores.max() / total)
