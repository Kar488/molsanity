"""Parallel attribution must change the wall clock and nothing else.

SubgraphX is 28-38 s per molecule and the work is Python-bound, not compute
bound: 16.9 million calls per molecule, 51.6 s on one thread against 33 s on
four. Threads and GPUs cannot fix that; separate processes can, because each
molecule's attribution is completely independent.

Independence is the claim these tests exist to check. A parallel path that ran
five times faster and produced different numbers would be worse than useless in
a project whose central claim is that its results reproduce. So the substantive
test is equality with the serial path, molecule for molecule, not a speedup.
"""
from __future__ import annotations

import numpy as np
import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("torch_geometric")

from molsanity.audit.parallel import (  # noqa: E402
    parallel_attributions,
    resolve_workers,
)


# ------------------------------------------------------------------ workers ---
def test_worker_count_never_exceeds_the_work_or_the_machine():
    import os

    cores = os.cpu_count() or 1
    assert resolve_workers(64, 3) <= 3, "more workers than molecules is waste"
    assert resolve_workers(64, 1000) <= cores
    assert resolve_workers("auto", 1000) <= cores


def test_parallelism_off_means_serial():
    """The default must not silently change how a run executes."""
    assert resolve_workers(None, 100) == 1
    assert resolve_workers(0, 100) == 1
    assert resolve_workers(1, 100) == 1
    # A single molecule is not worth a pool.
    assert resolve_workers(8, 1) == 1


# ------------------------------------------------------- equality with serial ---
class _CountingAttributor:
    """Deterministic per-graph attribution that depends only on the graph.

    Mirrors the property the real attributors have -- seeded per molecule, not
    per call -- so a correct pool must reproduce the serial result exactly.
    """

    method = "Counting"

    def attribute(self, data):
        from molsanity.attributors.base import Attribution

        gid = int(getattr(data, "graph_id", 0))
        rng = np.random.default_rng(gid)          # seeded by molecule, not order
        n = int(data.num_nodes)
        return Attribution(graph_id=gid, node_attr=rng.random(n).astype(np.float32),
                           edge_attr=None, method="Counting", target=0,
                           meta={"gid": gid})


class _OrderSensitiveAttributor(_CountingAttributor):
    """Deliberately wrong: its output depends on how many calls preceded it.

    This is the failure the equality test must be able to detect. If the test
    passes for this class too, it is not testing anything.
    """

    def __init__(self):
        self.calls = 0

    def attribute(self, data):
        self.calls += 1
        out = super().attribute(data)
        out.node_attr = out.node_attr + self.calls
        return out


def _graphs(n_graphs=12, n_nodes=6):
    from torch_geometric.data import Data

    out = []
    for k in range(n_graphs):
        ei = torch.tensor([[i, (i + 1) % n_nodes] for i in range(n_nodes)]).t()
        out.append(Data(x=torch.randn(n_nodes, 3), edge_index=ei.contiguous(),
                        edge_attr=torch.ones(ei.size(1), 1),
                        y=torch.tensor([k % 2]), num_nodes=n_nodes))
    return out


def test_parallel_matches_serial_molecule_for_molecule():
    """The one that matters."""
    graphs = _graphs()
    idx = list(range(len(graphs)))

    serial = parallel_attributions(_CountingAttributor(), graphs, idx, workers=1)
    par = parallel_attributions(_CountingAttributor(), graphs, idx, workers=4)

    assert len(par) == len(serial) == len(idx)
    for s, p in zip(serial, par):
        assert s.graph_id == p.graph_id
        np.testing.assert_array_equal(s.node_attr, p.node_attr)


def test_results_come_back_in_the_callers_order():
    """Workers finish out of order; the record list must not be reordered,
    or every per-molecule record would be attached to the wrong molecule."""
    graphs = _graphs(16)
    idx = [11, 2, 7, 0, 15, 4]          # deliberately not sorted
    got = parallel_attributions(_CountingAttributor(), graphs, idx, workers=4)
    assert [a.graph_id for a in got] == idx


def test_the_equality_test_can_actually_fail():
    """Guards the guard: an order-dependent attributor must be caught."""
    graphs = _graphs()
    idx = list(range(len(graphs)))
    serial = parallel_attributions(_OrderSensitiveAttributor(), graphs, idx,
                                   workers=1)
    par = parallel_attributions(_OrderSensitiveAttributor(), graphs, idx,
                                workers=4)
    assert any(not np.array_equal(s.node_attr, p.node_attr)
               for s, p in zip(serial, par)), (
        "an order-dependent attributor came back identical, so the equality "
        "test above proves nothing")


def test_a_missing_result_is_an_error_not_a_short_list():
    """A cell with holes in it must not be reported as a complete cell."""
    from molsanity.audit import parallel as P

    graphs = _graphs(6)
    real = P._attribute_one

    def drop_one(index):
        if index == 3:
            raise ValueError("simulated worker failure")
        return real(index)

    P._attribute_one = drop_one
    try:
        with pytest.raises(Exception):
            parallel_attributions(_CountingAttributor(), graphs,
                                  list(range(6)), workers=2)
    finally:
        P._attribute_one = real


def test_module_state_is_cleared_after_the_pool():
    """The context holds a model and a dataset; leaking it would pin them."""
    from molsanity.audit import parallel as P

    graphs = _graphs(8)
    parallel_attributions(_CountingAttributor(), graphs, list(range(8)),
                          workers=2)
    assert P._CTX == {}


# ------------------------------------------------------------ the real thing ---
def test_subgraphx_gives_the_same_subgraph_in_parallel():
    """End to end with the attributor this exists for."""
    pytest.importorskip("dig", reason="DIG (dive-into-graphs) not installed")
    from molsanity.attributors import build_attributor
    from molsanity.data.synthetic import generate_synth_motifs
    from molsanity.models import build_backbone

    graphs = list(generate_synth_motifs(num_graphs=4, num_nodes=10, seed=0))
    model = build_backbone("GINE", graphs[0],
                           {"hidden_channels": 16, "num_layers": 2,
                            "task": "graph-classification", "out_channels": 2})
    model.eval()

    def fresh():
        a = build_attributor("SubgraphX", model, task="graph-classification",
                             sgx_max_nodes=5, sgx_rollouts=3, seed=0)
        a.edge_dim = graphs[0].edge_attr.size(1)
        return a

    idx = list(range(len(graphs)))
    serial = parallel_attributions(fresh(), graphs, idx, workers=1)
    par = parallel_attributions(fresh(), graphs, idx, workers=2)
    for s, p in zip(serial, par):
        np.testing.assert_array_equal(s.node_attr, p.node_attr)
        assert s.meta["n_selected"] == p.meta["n_selected"]


# --------------------------------------------------- the full audit loop ---
def test_parallel_audit_matches_serial_on_every_field_of_every_record():
    """The loop that actually costs the time, compared field by field.

    Parallelising attribution alone optimised the wrong half: measured on a live
    run, an Integrated Gradients cell spends 0.6-0.7 s per molecule of which
    attribution is milliseconds. The rest is occlusion faithfulness (a forward
    pass per motif) and cross-checkpoint stability (a second attribution). A
    record carries 27 fields and all of them have to survive the move into a
    worker, so this compares all of them rather than spot-checking one.
    """
    import math
    from dataclasses import asdict

    from molsanity.attributors import build_attributor
    from molsanity.audit import audit_molecule
    from molsanity.audit.motifs import decompose
    from molsanity.audit.occlusion import dataset_feature_mean
    from molsanity.audit.parallel import parallel_audit
    from molsanity.data.synthetic import generate_synth_motifs
    from molsanity.models import build_backbone

    n = 8
    graphs = list(generate_synth_motifs(num_graphs=n + 4, num_nodes=12, seed=0))
    model = build_backbone("GINE", graphs[0],
                           {"hidden_channels": 16, "num_layers": 2,
                            "task": "graph-classification", "out_channels": 2})
    model.eval()
    baseline = dataset_feature_mean(graphs, list(range(n, n + 4)))
    idx = list(range(n))

    def attributor():
        a = build_attributor("IntegratedGradients", model,
                             task="graph-classification", ig_steps=8)
        a.edge_dim = graphs[0].edge_attr.size(1)
        return a

    serial = []
    attr = attributor()
    for i in idx:
        g = graphs[i]
        g.graph_id = i
        a = attr.attribute(g)
        serial.append(audit_molecule(model, g, a, "SynthMotifs", temperature=1.0,
                                     decomp=decompose(g),
                                     task="graph-classification",
                                     occ_baseline=baseline))

    par, first = parallel_audit(
        attributor=attributor(), dataset=graphs, indices=idx, workers=2,
        model=model, dataset_name="SynthMotifs", temperature=1.0,
        task="graph-classification", occ_baseline=baseline, early_attr=None)

    assert len(par) == len(serial)
    assert first is not None, "the case-study figure needs the first attribution"

    def same(a, b):
        if isinstance(a, float) and isinstance(b, float):
            return (math.isnan(a) and math.isnan(b)) or a == b
        return a == b

    mismatches = []
    for k, (s, p) in enumerate(zip(serial, par)):
        ds, dp = asdict(s), asdict(p)
        assert ds.keys() == dp.keys()
        mismatches += [(k, f) for f in ds if not same(ds[f], dp[f])]
    assert not mismatches, f"parallel audit differs from serial: {mismatches[:5]}"


def test_parallel_audit_refuses_a_single_worker():
    """The caller keeps its own serial loop, so a silent one-worker 'pool'
    would be a second code path pretending to be the first."""
    from molsanity.audit.parallel import parallel_audit

    with pytest.raises(ValueError):
        parallel_audit(attributor=None, dataset=[], indices=[1], workers=1,
                       model=None, dataset_name="x", temperature=1.0,
                       task="graph-classification", occ_baseline=None)


# ------------------------------------------------ everything off the GPU ---
def test_to_cpu_for_fork_finds_modules_the_backbone_does_not_own():
    """The bug that failed every GNNExplainer and PGExplainer cell.

    run_cell moved the backbone to CPU before forking and stopped there. But an
    attributor owns modules of its own -- PGExplainer keeps a mask MLP on
    ``explainer.algorithm`` -- and inside a forked child even ``.to('cpu')`` on
    a CUDA tensor has to initialise CUDA to read the source. One module left on
    the accelerator raises ``CUDA error: initialization error`` on the first
    molecule and takes the whole cell with it.

    Devices cannot be exercised without a GPU, so this checks the reachability
    that the fix turns on: every nested module must be found and touched.
    """
    from molsanity.audit.parallel import to_cpu_for_fork

    class Inner(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.lin = torch.nn.Linear(2, 2)
            self.moved = False

        def to(self, *args, **kwargs):
            self.moved = True
            return super().to(*args, **kwargs)

    class Algorithm(Inner):
        pass

    class FakeExplainer:
        def __init__(self):
            self.algorithm = Algorithm()

    class FakeAttributor:
        def __init__(self):
            self.model = Inner()
            self._explainer = FakeExplainer()
            self.not_a_module = 42

    backbone, attributor = Inner(), FakeAttributor()
    to_cpu_for_fork(backbone, attributor, None)

    assert backbone.moved, "the backbone was missed"
    assert attributor.model.moved, "the attributor's own model was missed"
    assert attributor._explainer.algorithm.moved, (
        "explainer.algorithm was missed -- this is exactly the module that "
        "failed every PGExplainer cell")


def test_to_cpu_for_fork_tolerates_none_and_cycles():
    """It walks arbitrary attributor objects, so it must not hang or raise."""
    from molsanity.audit.parallel import to_cpu_for_fork

    class Node:
        pass

    a, b = Node(), Node()
    a.peer, b.peer = b, a          # cycle
    a.module = torch.nn.Linear(2, 2)
    to_cpu_for_fork(None, a, b)    # must simply return


def _accelerator_probe(_):
    """Module level so the fork pool can pickle the callable."""
    import torch

    from molsanity.audit.parallel import _init_worker

    _init_worker()
    acc = torch.accelerator.current_accelerator(check_available=True)
    return (acc.type if acc is not None else None,
            torch.cuda.is_available(),
            torch.get_num_threads())


def test_worker_init_hides_the_accelerator():
    """The third failure: even a CUDA *query* fails in a forked child.

    torch.optim.Optimizer._accelerator_graph_capture_health_check runs on every
    step() and calls torch.accelerator.current_accelerator(). GNNExplainer fits
    a mask with Adam per molecule, so it died on its first optimiser step even
    with every tensor on the CPU -- moving modules was necessary but not
    sufficient. The child is told there is no accelerator at all.
    """
    import multiprocessing as mp

    with mp.get_context("fork").Pool(1) as pool:
        acc_type, cuda_available, threads = pool.map(_accelerator_probe, [0])[0]

    assert acc_type is None, f"worker still sees accelerator {acc_type!r}"
    assert cuda_available is False, "worker still reports CUDA as available"
    assert threads == 1, "worker should be single-threaded"


def test_the_parent_keeps_its_accelerator():
    """The patch is worker-local. Neutering the parent would move the whole
    run onto the CPU, including training."""
    import torch

    before = torch.cuda.is_available
    from molsanity.audit import parallel as P  # noqa: F401

    assert torch.cuda.is_available is before, (
        "importing the parallel module patched the parent's torch")
