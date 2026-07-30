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
    labels=None,
) -> Split:
    """Deterministic Bemis-Murcko scaffold split.

    Largest scaffold groups are placed first (standard MoleculeNet behaviour) so
    the test set is dominated by rarer, unseen scaffolds — the shift regime. When
    ``labels`` are provided (classification), a deterministic post-hoc pass moves
    whole scaffold groups from train so every fold contains every class (no
    scaffold leakage) — otherwise imbalanced datasets yield single-class folds.
    """
    scaffold_to_idx: dict[str, list[int]] = defaultdict(list)
    for i in range(len(dataset)):
        scaf = _murcko_scaffold_smiles(dataset[i])
        # Molecules with no Murcko scaffold (acyclic) get unique buckets so they
        # distribute across splits instead of collapsing into one giant group
        # that would starve the test set.
        key = scaf if scaf else f"__acyclic_{i}"
        scaffold_to_idx[key].append(i)

    # Deterministic ordering: by group size desc, then scaffold string.
    groups = sorted(scaffold_to_idx.values(), key=lambda g: (-len(g), min(g)))

    n = len(dataset)
    n_train, n_val = int(frac_train * n), int(frac_val * n)
    train, val, test = [], [], []
    # Standard MoleculeNet scaffold assignment: fill train, then val, then test
    # by *current count* (not fit-check), so no split is starved of examples.
    for group in groups:
        if len(train) < n_train:
            train.extend(group)
        elif len(val) < n_val:
            val.extend(group)
        else:
            test.extend(group)

    # Safety net: if a split is empty (pathological grouping), rebalance by
    # moving whole groups from the largest split. Keeps the split deterministic.
    if not test or not val:
        pool = sorted(train + val + test)
        n_tr, n_va = int(frac_train * n), int(frac_val * n)
        train, val, test = pool[:n_tr], pool[n_tr:n_tr + n_va], pool[n_tr + n_va:]
        log.warning("Scaffold split had an empty partition; applied index-based rebalance.")

    if labels is not None:
        train, val, test = _ensure_class_coverage(train, val, test, groups, labels)

    log.info(
        "Scaffold split: %d scaffolds -> train %d / val %d / test %d",
        len(groups), len(train), len(val), len(test),
    )
    return Split(sorted(train), sorted(val), sorted(test), kind="scaffold")


def _ensure_class_coverage(train, val, test, groups, labels):
    """Guarantee every fold contains every class, moving *whole* scaffold groups
    from train (no scaffold leakage). Deterministic. For imbalanced classification
    under scaffold split, folds can otherwise be single-class (AUC undefined)."""
    labels = {i: int(labels[i]) for i in range(len(labels))}
    classes = sorted(set(labels.values()))
    if len(classes) < 2:
        return train, val, test

    idx_to_group = {}
    for gi, g in enumerate(groups):
        for i in g:
            idx_to_group[i] = gi

    def classes_in(fold):
        return set(labels[i] for i in fold)

    train_s, val_s, test_s = set(train), set(val), set(test)
    for fold_s, name in ((val_s, "val"), (test_s, "test")):
        for c in classes:
            if c in classes_in(fold_s):
                continue
            # Find the smallest train scaffold group that contains class c.
            candidate_groups = sorted(
                {idx_to_group[i] for i in train_s if labels[i] == c},
                key=lambda gi: (len(groups[gi]), min(groups[gi])),
            )
            if not candidate_groups:
                continue
            gi = candidate_groups[0]
            members = [i for i in groups[gi] if i in train_s]
            for i in members:
                train_s.discard(i)
                fold_s.add(i)
            log.info("class-aware split: moved scaffold group (%d mols, class %s) "
                     "from train to %s for coverage", len(members), c, name)

    return sorted(train_s), sorted(val_s), sorted(test_s)


def random_split(
    dataset,
    frac_train: float = 0.8,
    frac_val: float = 0.1,
    seed: int = 0,
    labels=None,  # accepted for a uniform make_split signature; unused here
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
