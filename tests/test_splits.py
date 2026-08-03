"""Scaffold-split correctness.

The scaffold split *is* the shift regime — every claim MolSanity makes about
attributions "under scaffold shift" is only as good as this partition. These
tests pin the two ways it can silently stop being a scaffold split:

1. Decoding a dataset's atom features with the wrong vocabulary. Until
   2026-08-03 ``_murcko_scaffold_smiles`` always went through ``graph_to_mol``,
   which assumes MUTAG's 7-way atom one-hot. Applied to MoleculeNet's 9-dim
   feature vectors (whose first entry is the *atomic number*) it produced
   all-carbon skeletons, whose Murcko scaffolds are nearly unique — so every
   molecule got its own bucket and the "scaffold split" became an arbitrary
   index partition with 30-56%% true-scaffold leakage into the test set.

2. A dataset with no chemistry at all (BA-2Motifs, SynthMotifs, ShapeGGen).
   The partition is still deterministic, but it is not a shift regime and must
   be flagged so results are not reported as scaffold shift.

Both tests are network-free: graphs are built from SMILES in-memory with the
same ``from_smiles`` encoding MoleculeNet uses.
"""
from __future__ import annotations

import pytest

pytest.importorskip("rdkit")

from molsanity import data
from molsanity.data.splits import _murcko_scaffold_smiles, scaffold_split


@pytest.fixture(scope="module")
def mutag():
    return data.load_dataset("MUTAG")

# Six benzodiazepine-ish / steroid-ish pairs plus singletons: chosen so several
# molecules genuinely share a Bemis-Murcko scaffold (side chains differ, core
# does not), which is exactly the structure a scaffold split must exploit.
SMILES = [
    "c1ccccc1C",              # toluene            -> c1ccccc1
    "c1ccccc1CC",             # ethylbenzene       -> c1ccccc1
    "c1ccccc1CCC",            # propylbenzene      -> c1ccccc1
    "c1ccccc1O",              # phenol             -> c1ccccc1
    "c1ccc2ccccc2c1",         # naphthalene        -> c1ccc2ccccc2c1
    "Cc1ccc2ccccc2c1",        # methylnaphthalene  -> c1ccc2ccccc2c1
    "OCc1ccc2ccccc2c1",       # naphthalenemethanol-> c1ccc2ccccc2c1
    "c1ccc(-c2ccccc2)cc1",    # biphenyl           -> c1ccc(-c2ccccc2)cc1
    "Cc1ccc(-c2ccccc2)cc1",   # methylbiphenyl     -> c1ccc(-c2ccccc2)cc1
    "C1CCNCC1",               # piperidine         -> C1CCNCC1
    "CC1CCNCC1",              # methylpiperidine   -> C1CCNCC1
    "CCO",                    # ethanol            -> "" (acyclic)
]


def _graphs():
    """MoleculeNet-encoded graphs carrying their own SMILES."""
    from torch_geometric.utils import from_smiles

    gs = []
    for smi in SMILES:
        g = from_smiles(smi)
        g.smiles = smi
        gs.append(g)
    return gs


def _true_scaffolds():
    from rdkit import Chem
    from rdkit.Chem.Scaffolds import MurckoScaffold

    out = []
    for smi in SMILES:
        mol = Chem.MolFromSmiles(smi)
        out.append(MurckoScaffold.MurckoScaffoldSmiles(mol=mol, includeChirality=False))
    return out


def test_scaffold_of_a_moleculenet_graph_matches_rdkit_on_its_own_smiles():
    """Regression: the scaffold must come from the molecule, not from a
    MUTAG-vocabulary reconstruction of its feature matrix."""
    graphs, expected = _graphs(), _true_scaffolds()
    got = [_murcko_scaffold_smiles(g) for g in graphs]
    assert got == expected, (
        "scaffold SMILES disagree with RDKit on the graph's own SMILES; "
        "the split is being computed on a mis-decoded molecule"
    )


def test_scaffold_split_groups_molecules_that_share_a_scaffold():
    """Nine of the twelve molecules share a scaffold with another. If the
    decoder is wrong they all land in singleton buckets."""
    split = scaffold_split(_graphs())
    # 12 molecules -> 4 real scaffold groups (benzene x4, naphthalene x3,
    # biphenyl x2, piperidine x2) + 1 acyclic singleton bucket for ethanol.
    assert split.n_scaffolds == 5, split.n_scaffolds
    assert split.n_scaffoldless == 1
    assert split.frac_grouped == pytest.approx(11 / 12)
    assert split.degenerate is False


def test_scaffold_split_leaks_no_scaffold_from_train_into_test():
    """The defining property of a scaffold split: test scaffolds are unseen in
    training. Under the mis-decoded split this leaked 30-56%% on MoleculeNet."""
    # Fractions chosen so the test fold holds whole scaffold groups rather than
    # only the single acyclic molecule — otherwise the assertion is vacuous.
    split = scaffold_split(_graphs(), frac_train=0.4, frac_val=0.2)
    true = _true_scaffolds()
    scaffolded_test = [i for i in split.test if true[i]]
    assert len(scaffolded_test) >= 3, "test fold has too few real scaffolds to check"
    train_scaffolds = {true[i] for i in split.train if true[i]}
    leaked = [i for i in scaffolded_test if true[i] in train_scaffolds]
    assert leaked == [], (
        f"{len(leaked)}/{len(scaffolded_test)} test molecules share a Bemis-Murcko "
        "scaffold with a training molecule"
    )


def test_scaffold_split_flags_a_dataset_with_no_chemistry_as_degenerate():
    """BA-2Motifs / SynthMotifs / ShapeGGen have no molecular scaffold. The
    partition is still deterministic, but must not be reported as shift."""
    from molsanity.data.synthetic import generate_synth_motifs

    split = scaffold_split(generate_synth_motifs(num_graphs=40, num_nodes=20, seed=0))
    assert split.degenerate is True
    assert split.frac_grouped == 0.0
    assert split.n_scaffolds == 40  # every graph in its own bucket


def test_mutag_scaffold_split_still_groups(mutag):
    """MUTAG has no SMILES, so it takes the one-hot reconstruction path. That
    path was always correct for MUTAG and must stay correct."""
    split = scaffold_split(mutag.dataset)
    assert split.degenerate is False
    assert split.frac_grouped > 0.5
    assert split.n_scaffolds < len(mutag.dataset) / 2


def test_checkpoint_identity_tracks_the_partition_not_the_split_name():
    """A checkpoint keyed on ``split.kind`` alone is reloaded unchanged when the
    partition it was trained on is corrected — the model keeps the old training
    molecules and is then scored on the new test set. Silent contamination, and
    exactly what the 2026-08-03 scaffold fix would have caused on re-run.
    """
    from molsanity.data.splits import Split, split_digest

    old = Split(train=[0, 1, 2, 3], val=[4], test=[5, 6], kind="scaffold")
    new = Split(train=[0, 1, 5, 6], val=[4], test=[2, 3], kind="scaffold")
    same = Split(train=[0, 1, 2, 3], val=[4], test=[5, 6], kind="scaffold")

    assert split_digest(old) != split_digest(new), (
        "two different partitions share a checkpoint identity")
    assert split_digest(old) == split_digest(same), (
        "an identical partition must stay cached")

    # And the digest is what train_model actually keys on.
    import inspect

    from molsanity.models import train as train_mod

    src = inspect.getsource(train_mod.train_model)
    assert "split_digest(split)" in src, (
        "train_model must key its checkpoint on the partition, not just its name")
