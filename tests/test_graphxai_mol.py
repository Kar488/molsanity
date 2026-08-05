"""The GraphXAI real-molecule loader, exercised against a stand-in package.

GraphXAI cannot be imported in the CI container (its published wheel omits the
subpackages), so these tests inject a fake ``graphxai.datasets`` module shaped
like the real one -- ``.graphs`` of PyG Data, ``.explanations`` of objects
carrying ``node_imp`` -- and assert the adapter's behaviour. The shape comes
from GraphXAI's own extract_google_datasets.py.

What is actually being pinned: the union over multiple explanations, and the
all-zero mask on negatives. Getting either wrong produces a plausible dataset
that scores a correct attribution as wrong, which is the failure mode this
whole project exists to catch.
"""
from __future__ import annotations

import sys
import types

import pytest

torch = pytest.importorskip("torch")
from torch_geometric.data import Data  # noqa: E402

from molsanity.data.datasets import DatasetBlocked, _load_graphxai_mol  # noqa: E402
from molsanity.data.manifest import DatasetSpec  # noqa: E402


class _Expl:
    def __init__(self, imp):
        self.node_imp = torch.tensor(imp, dtype=torch.float32)


def _mol(n, label):
    ei = torch.tensor([[i for i in range(n - 1)], [i + 1 for i in range(n - 1)]],
                      dtype=torch.long)
    return Data(x=torch.eye(n), edge_index=ei,
                edge_attr=torch.ones(ei.size(1), 3),
                y=torch.tensor([label], dtype=torch.long), num_nodes=n)


def _install_fake(graphs, expls, monkeypatch, tmp_path=None, break_class=True):
    """Stand in for GraphXAI, shaped like the real package.

    ``break_class=True`` is the default because that is the real world: the
    dataset class raises on numpy 2 while ``load_graphs`` is fine, so the
    adapter must never depend on the class succeeding.
    """
    import pathlib

    mod = types.ModuleType("graphxai")
    dsmod = types.ModuleType("graphxai.datasets")
    exmod = types.ModuleType(
        "graphxai.datasets.real_world.extract_google_datasets")
    bzmod = types.ModuleType("graphxai.datasets.real_world.benzene.benzene")

    home = pathlib.Path(tmp_path or ".") / "gx"
    home.mkdir(parents=True, exist_ok=True)
    (home / "benzene.npz").write_bytes(b"")
    bzmod.__file__ = str(home / "benzene.py")
    bzmod.benzene_datapath = str(home / "benzene.npz")

    exmod.load_graphs = lambda path: (graphs, expls, None)

    class Fake:
        def __init__(self, seed=None):
            if break_class:
                raise TypeError(
                    "'numpy.float32' object cannot be interpreted as an integer")
            self.graphs, self.explanations = graphs, expls

    dsmod.Benzene = Fake
    mod.datasets = dsmod
    for name, m in [
            ("graphxai", mod), ("graphxai.datasets", dsmod),
            ("graphxai.datasets.real_world.extract_google_datasets", exmod),
            ("graphxai.datasets.real_world.benzene.benzene", bzmod)]:
        monkeypatch.setitem(sys.modules, name, m)


def _spec(**extra):
    e = {"graphxai_class": "Benzene", "max_graphs": 100, "seed": 0,
         "balance": True}
    e.update(extra)
    return DatasetSpec(name="Benzene", tier=1, task="graph-classification",
                       source="test", licence="MIT", loader="graphxai_mol",
                       has_ground_truth=True, extras=e)


def test_multiple_explanations_are_unioned(monkeypatch, tmp_path):
    """Two benzene rings means two published rationales; both are ground truth.

    Taking only the first would label the second ring's atoms as negatives, so
    an attribution that found it would be scored as wrong.
    """
    monkeypatch.chdir(tmp_path)
    g = _mol(6, 1)
    expls = [[_Expl([1, 1, 0, 0, 0, 0]), _Expl([0, 0, 0, 0, 1, 1])]]
    _install_fake([g, _mol(6, 0)], expls + [[]], monkeypatch, tmp_path)
    out = _load_graphxai_mol(_spec())
    pos = [d for d in out.dataset if int(d.y) == 1][0]
    assert pos.node_gt.tolist() == [1, 1, 0, 0, 1, 1]


def test_negatives_keep_an_all_zero_mask(monkeypatch, tmp_path):
    """Negatives train the classifier and contribute nothing to GT AUROC."""
    monkeypatch.chdir(tmp_path)
    _install_fake([_mol(5, 1), _mol(5, 0)],
                  [[_Expl([1, 1, 0, 0, 0])], []], monkeypatch, tmp_path)
    out = _load_graphxai_mol(_spec())
    neg = [d for d in out.dataset if int(d.y) == 0][0]
    assert float(neg.node_gt.sum()) == 0.0


def test_a_positive_whose_mask_covers_everything_is_dropped(monkeypatch, tmp_path):
    """An all-ones mask has one class, so its AUROC is undefined, not 1.0."""
    monkeypatch.chdir(tmp_path)
    _install_fake([_mol(4, 1), _mol(4, 1), _mol(4, 0), _mol(4, 0)],
                  [[_Expl([1, 1, 1, 1])], [_Expl([1, 0, 0, 0])], [], []],
                  monkeypatch, tmp_path)
    out = _load_graphxai_mol(_spec())
    for d in out.dataset:
        if int(d.y) == 1:
            assert 0 < float(d.node_gt.sum()) < d.num_nodes


def test_the_task_is_balanced(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    graphs = [_mol(5, 1) for _ in range(8)] + [_mol(5, 0) for _ in range(30)]
    expls = [[_Expl([1, 1, 0, 0, 0])] for _ in range(8)] + [[] for _ in range(30)]
    _install_fake(graphs, expls, monkeypatch, tmp_path)
    out = _load_graphxai_mol(_spec())
    labels = [int(d.y) for d in out.dataset]
    assert labels.count(1) == labels.count(0) == 8


def test_a_missing_graphxai_is_blocked_not_fatal(monkeypatch, tmp_path):
    """Hard Rule 4: an unavailable dependency skips the cell, never aborts."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setitem(sys.modules, "graphxai", None)
    with pytest.raises(DatasetBlocked):
        _load_graphxai_mol(_spec())


def test_an_explanation_of_the_wrong_shape_is_ignored(monkeypatch, tmp_path):
    """Never pad or truncate a rationale to fit: that invents ground truth."""
    monkeypatch.chdir(tmp_path)
    _install_fake([_mol(5, 1), _mol(5, 0)],
                  [[_Expl([1, 1, 0]), _Expl([0, 0, 1, 1, 0])], []],
                  monkeypatch, tmp_path)
    out = _load_graphxai_mol(_spec())
    pos = [d for d in out.dataset if int(d.y) == 1][0]
    assert pos.node_gt.tolist() == [0, 0, 1, 1, 0]


def test_a_broken_dataset_class_does_not_lose_the_arm(monkeypatch, tmp_path):
    """The regression that cost 84 cell-runs.

    GraphXAI's Benzene.__init__ reads the .npz and then calls
    GraphDataset.__init__, which builds train/val/test indices with sklearn.
    On numpy 2 that raises "'numpy.float32' object cannot be interpreted as an
    integer" and takes the whole dataset down. Every one of the 84 new
    cell-runs in the 2026-08-05 sweep was skipped by it.

    MolSanity never uses GraphXAI's splits, so the adapter must reach the data
    without constructing the class. _install_fake breaks the class by default;
    that these tests pass at all is the assertion.
    """
    monkeypatch.chdir(tmp_path)
    _install_fake([_mol(5, 1), _mol(5, 0)],
                  [[_Expl([1, 1, 0, 0, 0])], []], monkeypatch, tmp_path,
                  break_class=True)
    out = _load_graphxai_mol(_spec())
    assert len(out.dataset) == 2


def test_the_class_is_still_a_fallback(monkeypatch, tmp_path):
    """If load_graphs ever moves, the class path must still work."""
    monkeypatch.chdir(tmp_path)
    _install_fake([_mol(5, 1), _mol(5, 0)],
                  [[_Expl([1, 1, 0, 0, 0])], []], monkeypatch, tmp_path,
                  break_class=False)
    import sys as _s
    _s.modules["graphxai.datasets.real_world.extract_google_datasets"].load_graphs = (
        lambda path: (_ for _ in ()).throw(RuntimeError("moved")))
    out = _load_graphxai_mol(_spec())
    assert len(out.dataset) == 2


def _write_npz(path, graphs, imps, labels, smi=None):
    """A .npz in the Sanchez-Lengeling layout GraphXAI ships.

    keys: attr, X, y, smiles. X[0] is the graph list; attr[i][0]['nodes'] is a
    (num_nodes, num_rationales) importance matrix.
    """
    import numpy as np

    X = np.empty(1, dtype=object)
    X[0] = np.array(graphs, dtype=object)
    attr = np.empty(len(imps), dtype=object)
    for i, m in enumerate(imps):
        attr[i] = np.array([{"nodes": np.asarray(m, dtype=np.float32),
                             "n_edge": graphs[i]["n_edge"]}], dtype=object)
    smi = smi or ["c1ccccc1"] * len(graphs)
    np.savez(path, attr=attr, X=X,
             y=np.asarray([[float(v)] for v in labels], dtype=np.float32),
             smiles=np.array([[s, i] for i, s in enumerate(smi)], dtype=object))


def _chain(n):
    import numpy as np
    return {"nodes": np.eye(n, dtype=np.float32),
            "edges": np.ones((n - 1, 3), dtype=np.float32),
            "receivers": np.arange(n - 1, dtype=np.float32),
            "senders": np.arange(1, n, dtype=np.float32),
            "n_edge": n - 1}


def test_the_npz_is_read_without_graphxai_at_all(tmp_path):
    """The path that finally works, verified against a real archive.

    GraphXAI's load_graphs reads this same file correctly and then builds
    Explanation objects; that machinery raises "'numpy.float32' object cannot
    be interpreted as an integer" on numpy 2 and cost two sweeps their 84
    cell-runs. Note that receivers/senders here are float32 -- exactly as the
    shipped archives store them, and the reason a loader that indexes with them
    breaks.
    """
    from molsanity.data.datasets import _graphs_from_npz

    p = tmp_path / "fc.npz"
    _write_npz(p, [_chain(4), _chain(3)],
               [[[1, 0], [1, 0], [0, 1], [0, 1]], [[0], [0], [0]]], [1, 0])
    graphs, expls = _graphs_from_npz(str(p))

    assert len(graphs) == len(expls) == 2
    assert graphs[0].edge_index.dtype == torch.long, "float indices would break PyG"
    assert graphs[0].edge_index.shape == (2, 3)
    assert int(graphs[0].y) == 1 and int(graphs[1].y) == 0
    # Two columns -> two published rationales for the first molecule.
    assert len(expls[0]) == 2
    assert expls[0][0].node_imp.tolist() == [1, 1, 0, 0]
    assert expls[0][1].node_imp.tolist() == [0, 0, 1, 1]


def test_the_npz_rationales_union_into_one_mask(tmp_path, monkeypatch):
    """End to end: several rationale columns become one ground-truth mask."""
    import sys
    import types

    from molsanity.data.datasets import _graphs_from_npz

    # 6 atoms, two rationales of two atoms each: the union is 4 of 6, so the
    # molecule stays scoreable. A union covering every atom is dropped, which
    # is deliberate -- AUROC over a single-class mask is undefined, not 1.0.
    p = tmp_path / "fc.npz"
    _write_npz(p, [_chain(6), _chain(6)],
               [[[1, 0], [1, 0], [0, 1], [0, 1], [0, 0], [0, 0]],
                [[0], [0], [0], [0], [0], [0]]], [1, 0])
    graphs, expls = _graphs_from_npz(str(p))

    mod = types.ModuleType("graphxai")
    dsmod = types.ModuleType("graphxai.datasets")
    exmod = types.ModuleType(
        "graphxai.datasets.real_world.extract_google_datasets")
    bzmod = types.ModuleType("graphxai.datasets.real_world.benzene.benzene")
    bzmod.__file__ = str(tmp_path / "benzene.py")
    bzmod.benzene_datapath = str(p)
    exmod.load_graphs = lambda _p: (_ for _ in ()).throw(
        TypeError("'numpy.float32' object cannot be interpreted as an integer"))
    mod.datasets = dsmod
    for nm, m in [("graphxai", mod), ("graphxai.datasets", dsmod),
                  ("graphxai.datasets.real_world.extract_google_datasets", exmod),
                  ("graphxai.datasets.real_world.benzene.benzene", bzmod)]:
        monkeypatch.setitem(sys.modules, nm, m)

    monkeypatch.chdir(tmp_path)
    out = _load_graphxai_mol(_spec())
    pos = [d for d in out.dataset if int(d.y) == 1][0]
    assert pos.node_gt.tolist() == [1, 1, 1, 1, 0, 0], (
        "both published rationales must survive into one mask")
    neg = [d for d in out.dataset if int(d.y) == 0][0]
    assert float(neg.node_gt.sum()) == 0.0


def test_smiles_are_carried_so_the_scaffold_split_is_real(tmp_path):
    """The defect that made the first run of these arms uninterpretable.

    _graphs_from_npz originally built Data(x, edge_index, edge_attr, y) and
    dropped the archive's SMILES. Bemis-Murcko then had no molecule to work
    with, every graph landed in its own scaffold bucket, and scaffold_split
    logged DEGENERATE for all six splits -- 0.0% of molecules sharing a
    scaffold. The arms ran, produced plausible numbers, and those numbers were
    not about scaffold shift at all.

    A dataset whose whole purpose is to carry a shift contrast must not be able
    to lose it silently.
    """
    from molsanity.data.datasets import _graphs_from_npz

    smi = ["c1ccccc1CC", "c1ccccc1CCC"]
    p = tmp_path / "fc.npz"
    _write_npz(p, [_chain(6), _chain(6)],
               [[[1], [1], [0], [0], [0], [0]], [[0]] * 6], [1, 0], smi=smi)
    graphs, _ = _graphs_from_npz(str(p))
    assert [g.smiles for g in graphs] == smi, (
        "no SMILES on the graph means no Bemis-Murcko scaffold means no shift")


def test_a_missing_smiles_table_is_survivable(tmp_path):
    """Absent SMILES must not crash the loader -- only cost the shift regime."""
    import numpy as np

    from molsanity.data.datasets import _graphs_from_npz

    p = tmp_path / "fc.npz"
    _write_npz(p, [_chain(5), _chain(5)],
               [[[1], [1], [0], [0], [0]], [[0]] * 5], [1, 0])
    raw = dict(np.load(p, allow_pickle=True))
    raw.pop("smiles")
    np.savez(p, **raw)
    graphs, _ = _graphs_from_npz(str(p))
    assert len(graphs) == 2
    assert not hasattr(graphs[0], "smiles") or graphs[0].smiles is None
