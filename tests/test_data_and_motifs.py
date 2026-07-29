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


def test_class_aware_scaffold_split_covers_all_classes():
    """Every fold must contain every class when labels are provided, without
    changing MUTAG's split (which already has both classes in each fold)."""
    ld = data.load_dataset("MUTAG")
    labels = [int(ld.dataset[i].y.view(-1)[0]) for i in range(len(ld))]
    s = data.make_split(ld.dataset, kind="scaffold", labels=labels)
    for fold in (s.train, s.val, s.test):
        classes = {int(ld.dataset[i].y.view(-1)[0]) for i in fold}
        assert classes == {0, 1}
    # MUTAG folds already had both classes, so labels must not change the split.
    s_nolabel = data.make_split(ld.dataset, kind="scaffold")
    assert s.test == s_nolabel.test


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


def test_synth_motifs_exact_ground_truth():
    ld = data.load_dataset("SynthMotifs")
    assert len(ld) == 200
    g = ld.dataset[0]
    gt = data.ground_truth_mask("SynthMotifs", g)
    assert gt is not None
    assert gt.sum() == 5  # exactly the injected 5-node motif
    assert set(int(ld.dataset[i].y) for i in range(len(ld))) == {0, 1}  # both motifs
    # Deterministic: regenerating gives the same checksum.
    c1 = data.dataset_checksum(ld.dataset)
    ld2 = data.load_dataset("SynthMotifs")
    assert data.dataset_checksum(ld2.dataset) == c1
