"""Data loader + motif + GT tests. Require the torch/rdkit stack (skip if absent)."""
import numpy as np
import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("torch_geometric")
pytest.importorskip("rdkit")

from molsanity import data
from molsanity.audit.motifs import decompose, primary_motif_share


@pytest.fixture(scope="module")
def mutag():
    return data.load_dataset("MUTAG")


def test_mutag_loads_and_checksum_stable(mutag):
    assert len(mutag) == 188
    c1 = data.dataset_checksum(mutag.dataset)
    c2 = data.dataset_checksum(mutag.dataset)
    assert c1 == c2 and len(c1) == 64
    assert mutag.provenance["licence"]


def test_mol_reconstruction_valid(mutag):
    ok = 0
    for i in range(len(mutag)):
        mol, _ = data.graph_to_mol(mutag.dataset[i])
        if data.mol_to_smiles(mol):
            ok += 1
    assert ok == len(mutag)  # all 188 reconstruct to valid SMILES


def test_nitro_ground_truth(mutag):
    # MUTAG compounds are nitroaromatics -> every graph has a nitro motif.
    g = mutag.dataset[0]
    mask = data.mutag_nitro_mask(g)
    assert mask.sum() >= 3  # N + >=2 O
    n_with = sum(int(data.ground_truth_mask("MUTAG", mutag.dataset[i]).sum() > 0)
                 for i in range(len(mutag)))
    assert n_with == len(mutag)


def test_scaffold_split_deterministic_and_partitions(mutag):
    s1 = data.make_split(mutag.dataset, kind="scaffold")
    s2 = data.make_split(mutag.dataset, kind="scaffold")
    assert s1.test == s2.test
    all_idx = sorted(s1.train + s1.val + s1.test)
    assert all_idx == list(range(len(mutag)))  # exact partition, no overlap
    assert set(s1.train).isdisjoint(s1.test)


def test_motif_decomposition_covers_and_top1(mutag):
    g = mutag.dataset[0]
    decomp = decompose(g)
    assert len(decomp.motifs) >= 1
    assert decomp.coverage() > 0.0
    # concentrated attribution on one motif -> top1 share high
    attr = np.zeros(g.num_nodes)
    attr[decomp.motifs[0]] = 1.0
    assert primary_motif_share(attr, decomp) > 0.0


def test_blocked_dataset_raises(mutag):
    with pytest.raises(data.DatasetBlocked):
        data.load_dataset("MIMIC")
