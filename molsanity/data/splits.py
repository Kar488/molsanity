"""Deterministic dataset splits.

Primary regime: **Bemis-Murcko scaffold split** — groups molecules by their
Murcko scaffold and assigns whole scaffold groups to train/val/test so the test
set contains scaffolds unseen in training (distribution / scaffold shift). This
is the deterministic default. A random split is provided as an in-distribution
reference.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

import numpy as np

from ..utils import get_logger
from .chem import graph_to_mol, mol_to_smiles

log = get_logger()


@dataclass
class Split:
    train: list[int]
    val: list[int]
    test: list[int]
    kind: str

    def as_dict(self) -> dict:
        return {"kind": self.kind, "train": self.train, "val": self.val, "test": self.test}


def _murcko_scaffold_smiles(data) -> str:
    """Bemis-Murcko scaffold SMILES for a reconstructed molecule.

    Empty string is a valid bucket (acyclic / scaffold-less molecules group
    together deterministically).
    """
    from rdkit.Chem.Scaffolds import MurckoScaffold

    mol, _ = graph_to_mol(data)
    smi = mol_to_smiles(mol)
    if not smi:
        return ""
    try:
        scaf = MurckoScaffold.MurckoScaffoldSmiles(smiles=smi, includeChirality=False)
        return scaf or ""
    except Exception:
        return ""


def scaffold_split(
    dataset,
    frac_train: float = 0.8,
    frac_val: float = 0.1,
    seed: int = 0,
) -> Split:
    """Deterministic Bemis-Murcko scaffold split.

    Largest scaffold groups are placed first (standard MoleculeNet behaviour) so
    the test set is dominated by rarer, unseen scaffolds — the shift regime.
    """
    scaffold_to_idx: dict[str, list[int]] = defaultdict(list)
    for i in range(len(dataset)):
        scaf = _murcko_scaffold_smiles(dataset[i])
        scaffold_to_idx[scaf].append(i)

    # Deterministic ordering: by group size desc, then scaffold string.
    groups = sorted(scaffold_to_idx.values(), key=lambda g: (-len(g), min(g)))

    n = len(dataset)
    n_train, n_val = int(frac_train * n), int(frac_val * n)
    train, val, test = [], [], []
    for group in groups:
        if len(train) + len(group) <= n_train:
            train.extend(group)
        elif len(val) + len(group) <= n_val:
            val.extend(group)
        else:
            test.extend(group)

    log.info(
        "Scaffold split: %d scaffolds -> train %d / val %d / test %d",
        len(groups), len(train), len(val), len(test),
    )
    return Split(sorted(train), sorted(val), sorted(test), kind="scaffold")


def random_split(
    dataset,
    frac_train: float = 0.8,
    frac_val: float = 0.1,
    seed: int = 0,
) -> Split:
    """Deterministic random split (in-distribution reference)."""
    n = len(dataset)
    rng = np.random.default_rng(seed)
    perm = rng.permutation(n).tolist()
    n_train, n_val = int(frac_train * n), int(frac_val * n)
    train = perm[:n_train]
    val = perm[n_train : n_train + n_val]
    test = perm[n_train + n_val :]
    return Split(sorted(train), sorted(val), sorted(test), kind="random")


def make_split(dataset, kind: str = "scaffold", **kwargs) -> Split:
    if kind == "scaffold":
        return scaffold_split(dataset, **kwargs)
    if kind == "random":
        return random_split(dataset, **kwargs)
    raise ValueError(f"Unknown split kind: {kind}")
