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
from .chem import mol_from_data

log = get_logger()


@dataclass
class Split:
    train: list[int]
    val: list[int]
    test: list[int]
    kind: str
    # Scaffold-split diagnostics (zero/None for other split kinds). ``degenerate``
    # means almost every molecule sits in its own scaffold bucket, so the split is
    # deterministic but is NOT a chemical shift regime.
    n_scaffolds: int = 0
    n_scaffoldless: int = 0
    frac_grouped: float = 0.0
    degenerate: bool = False

    def as_dict(self) -> dict:
        return {
            "kind": self.kind, "train": self.train, "val": self.val, "test": self.test,
            "n_scaffolds": self.n_scaffolds, "n_scaffoldless": self.n_scaffoldless,
            "frac_grouped": self.frac_grouped, "degenerate": self.degenerate,
        }


def _murcko_scaffold_smiles(data) -> str:
    """Bemis-Murcko scaffold SMILES for one graph.

    Uses ``mol_from_data``, which parses the graph's own SMILES when it carries
    one and only falls back to MUTAG-style one-hot reconstruction otherwise.
    Going through ``graph_to_mol`` unconditionally (as this did until 2026-08-03)
    decodes every dataset with MUTAG's atom vocabulary, which turns MoleculeNet
    molecules into all-carbon skeletons and makes their scaffolds nearly unique —
    i.e. no grouping, so no scaffold shift. See ``test_splits.py``.

    Empty string is a valid bucket (acyclic / scaffold-less molecules group
    together deterministically).
    """
    from rdkit.Chem.Scaffolds import MurckoScaffold

    mol, source = mol_from_data(data)
    if mol is None or source == "none":
        return ""
    try:
        scaf = MurckoScaffold.MurckoScaffoldSmiles(mol=mol, includeChirality=False)
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
    n_scaffoldless = 0
    for i in range(len(dataset)):
        scaf = _murcko_scaffold_smiles(dataset[i])
        # Molecules with no Murcko scaffold (acyclic) get unique buckets so they
        # distribute across splits instead of collapsing into one giant group
        # that would starve the test set.
        if not scaf:
            n_scaffoldless += 1
        key = scaf if scaf else f"__acyclic_{i}"
        scaffold_to_idx[key].append(i)

    # Deterministic ordering: by group size desc, then scaffold string.
    groups = sorted(scaffold_to_idx.values(), key=lambda g: (-len(g), min(g)))

    # Honesty check. A split over buckets that are almost all singletons is an
    # arbitrary deterministic partition, not a chemical shift regime; anything
    # measured "under scaffold shift" on such a dataset must not be reported as
    # such. Recorded on the Split so callers/artifacts can carry the caveat.
    n_mols = len(dataset)
    grouped = sum(len(g) for g in groups if len(g) > 1)
    degenerate = n_mols > 0 and (grouped / n_mols) < 0.10

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
        "Scaffold split: %d scaffolds over %d molecules (%d scaffold-less, "
        "%.1f%% of molecules in multi-member groups) -> train %d / val %d / test %d",
        len(groups), n_mols, n_scaffoldless, 100.0 * grouped / max(1, n_mols),
        len(train), len(val), len(test),
    )
    if degenerate:
        log.warning(
            "Scaffold split is DEGENERATE: only %.1f%% of molecules share a "
            "scaffold with another molecule, so this partition is deterministic "
            "but not a chemical shift regime. Do not report it as scaffold shift.",
            100.0 * grouped / max(1, n_mols),
        )
    return Split(
        sorted(train), sorted(val), sorted(test), kind="scaffold",
        n_scaffolds=len(groups), n_scaffoldless=n_scaffoldless,
        frac_grouped=grouped / max(1, n_mols), degenerate=degenerate,
    )


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
