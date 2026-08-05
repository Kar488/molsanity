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
