"""MolMotif — real molecules, exact ground truth, by construction.

The audit's ground-truth arms each fail one half of what a reviewer wants.
MUTAG is molecular but its mask is a chemically motivated SMARTS *proxy*: the
trained model may be using a different, equally valid rationale, so a low
GT AUROC does not by itself prove the attribution wrong (Faber et al., KDD
2021). SynthMotifs and BA-2Motifs have exact labels but are Barabasi-Albert
graphs, not chemistry.

MolMotif is both. Real drug-like molecules are taken from a MoleculeNet source
and relabelled: the class is the *presence of a specific chemical
substructure*, and the ground-truth mask is exactly the atoms that substructure
matches. The label is therefore determined by that substructure by
construction, not by assumption, which is the design Sanchez-Lengeling et
al. (NeurIPS 2020) introduced for exactly this problem.

What this does and does not buy:

* It removes the proxy objection. On these molecules the causal substructure is
  known with certainty, because it defines the label.
* It does not remove the *shortcut* objection. A model can still reach the right
  answer via a correlate of the motif rather than the motif itself. That is
  what ``rationale_use`` in ``audit/rationale.py`` measures, per molecule, so
  the two objections are separated rather than conflated.
* The task is easy by design. It is a probe of the audit, not a hard chemistry
  benchmark, and is labelled as such wherever it is reported.
"""
from __future__ import annotations

from ..utils import get_logger

log = get_logger()

# Chemically meaningful, unambiguous, and common enough in drug-like sets to
# give a balanced task. The nitroaromatic pattern is the same family MUTAG's
# proxy targets, which makes the two arms directly comparable: same chemistry,
# proxy label on one and exact label on the other.
MOTIF_SMARTS = {
    "nitroaromatic": "[$([NX3](=O)=O),$([NX3+](=O)[O-])][c]",
    "nitro": "[$([NX3](=O)=O),$([NX3+](=O)[O-])]",
    "sulfonamide": "[SX4](=[OX1])(=[OX1])[NX3]",
    "carboxylic_acid": "[CX3](=O)[OX2H1]",
    "halogen_aromatic": "[F,Cl,Br,I][c]",
}


def _match_atoms(mol, patt) -> set[int]:
    """Every atom index covered by any match of ``patt``."""
    atoms: set[int] = set()
    for match in mol.GetSubstructMatches(patt):
        atoms.update(int(a) for a in match)
    return atoms


def generate_mol_motif(source_dataset, motif: str = "halogen_aromatic",
                       max_graphs: int = 1000, balance: bool = True,
                       seed: int = 0, radius: int = 1):
    """Relabel real molecules by presence of ``motif``; mask = its atoms.

    ``source_dataset`` is any PyG dataset whose graphs carry a ``smiles``
    attribute (MoleculeNet does). Positives are molecules containing the
    substructure; the ground-truth mask is the matched atoms, optionally grown
    by ``radius`` bonds so the mask covers the local environment a
    message-passing model actually reads rather than the bare match.

    Negatives carry an all-zero mask, so they contribute to training but are
    excluded from ground-truth scoring, which is undefined without positives.
    """
    import random

    import torch
    from rdkit import Chem

    from .chem import _silence_rdkit

    _silence_rdkit()
    if motif not in MOTIF_SMARTS:
        raise KeyError(f"unknown motif {motif!r}; known: {sorted(MOTIF_SMARTS)}")
    patt = Chem.MolFromSmarts(MOTIF_SMARTS[motif])
    if patt is None:
        raise ValueError(f"RDKit rejected the SMARTS for {motif!r}")

    pos, neg = [], []
    for i in range(len(source_dataset)):
        g = source_dataset[i]
        smi = getattr(g, "smiles", None)
        if not smi or g.x is None or g.edge_index is None:
            continue
        mol = Chem.MolFromSmiles(smi)
        if mol is None or mol.GetNumAtoms() != int(g.num_nodes):
            # The featuriser and RDKit must agree on atom indexing, or the mask
            # would point at the wrong atoms. Skip rather than risk it.
            continue
        atoms = _match_atoms(mol, patt)
        if atoms and radius > 0:
            grown = set(atoms)
            for _ in range(radius):
                for a in list(grown):
                    for nb in mol.GetAtomWithIdx(int(a)).GetNeighbors():
                        grown.add(int(nb.GetIdx()))
            atoms = grown
        label = 1 if atoms else 0
        mask = torch.zeros(int(g.num_nodes), dtype=torch.float32)
        if atoms:
            mask[list(atoms)] = 1.0
        if label == 1 and (mask.sum() == 0 or mask.sum() == mask.numel()):
            continue  # a mask covering everything cannot be scored
        (pos if label else neg).append((i, mask, label))

    rng = random.Random(seed)
    if balance:
        k = min(len(pos), len(neg), max_graphs // 2)
        if k == 0:
            raise ValueError(
                f"MolMotif({motif}): {len(pos)} positive and {len(neg)} negative "
                "molecules; cannot build a balanced task")
        pos = rng.sample(pos, k)
        neg = rng.sample(neg, k)
    picked = pos + neg
    rng.shuffle(picked)
    picked = picked[:max_graphs]

    graphs = []
    for idx, mask, label in picked:
        src = source_dataset[idx]
        g = src.clone() if hasattr(src, "clone") else src
        g.y = torch.tensor([label], dtype=torch.long)
        g.node_gt = mask
        graphs.append(g)

    n_pos = sum(1 for _, _, y in picked if y == 1)
    log.info("MolMotif(%s): %d molecules (%d positive), mask = matched atoms "
             "grown by %d bond(s)", motif, len(graphs), n_pos, radius)
    return graphs


__all__ = ["generate_mol_motif", "MOTIF_SMARTS"]
