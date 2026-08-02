"""Attribute molecules in parallel, without changing a single number.

SubgraphX runs a Monte-Carlo tree search per molecule and is three orders of
magnitude slower than the gradient family. Profiling one molecule shows why, and
rules out the obvious fixes: 16.9 million Python calls, 9.7 s across 845 model
forwards at 11 ms each on a 30-node graph, and 6.3 s of pure DataLoader
collation. It is framework-overhead bound, not compute bound, so a GPU buys
almost nothing (the arithmetic is already trivial), and a cluster framework buys
less than nothing (it adds serialisation to a problem that is already
serialisation).

Threads do not help much either, for the same reason: 51.6 s per molecule on one
thread against 33 s on four, a 1.55x return on 4x the cores. The Python
interpreter is the bottleneck and a single process cannot escape it.

Separate processes can. Each molecule's attribution is completely independent --
no shared state, no ordering -- so this is embarrassingly parallel, and four
single-threaded workers beat one four-threaded process by about 2.6x.

**Reproducibility is the whole constraint here.** A parallel path that produced
different numbers would be worthless whatever its speed. Two properties make
this safe, and both are tested rather than assumed:

* Every attributor seeds per molecule (``seed + graph_id``), not per call, so a
  molecule's result does not depend on how many molecules preceded it or on
  which worker took it.
* Results are reassembled in the caller's index order, so the record list is
  identical to the serial one even though workers finish out of order.

``fork`` is used deliberately: the model and the attributor are inherited
copy-on-write rather than pickled, which matters because DIG's explainer object
does not pickle. CUDA and ``fork`` are incompatible, so the caller must hand
over a CPU model -- no loss, since the GPU was not helping.
"""
from __future__ import annotations

import os

from ..utils import get_logger

log = get_logger()

# Set in the parent before the pool is created; inherited by fork.
_CTX: dict = {}


def _init_worker() -> None:
    """One thread per worker.

    With N workers each spawning N torch threads the machine thrashes and the
    parallel version can be slower than the serial one. Single-threaded workers
    cost 51.6 s per molecule against 33 s multi-threaded, but N of them run at
    once, which is the trade that pays.
    """
    import torch

    torch.set_num_threads(1)


def to_cpu_for_fork(*objects) -> None:
    """Move every torch module reachable from ``objects`` onto the CPU.

    This must happen in the *parent*, before the pool is created, and moving the
    backbone alone is not enough. An attributor owns modules the backbone does
    not: PGExplainer keeps a mask MLP on ``explainer.algorithm``, and its
    ``attribute`` re-syncs that module to the model's device on every call.

    Inside a forked child, ``tensor.to('cpu')`` on a CUDA tensor still has to
    initialise CUDA to read the source, so a module left on the GPU raises
    ``CUDA error: initialization error`` on the first molecule -- and takes the
    whole cell with it. Every module has to be off the accelerator before the
    fork, not after.
    """
    import torch

    seen = set()

    def walk(obj, depth=0):
        if obj is None or depth > 3 or id(obj) in seen:
            return
        seen.add(id(obj))
        if isinstance(obj, torch.nn.Module):
            obj.to("cpu")
            return
        for name in vars(obj) if hasattr(obj, "__dict__") else ():
            if name.startswith("__"):
                continue
            walk(getattr(obj, name, None), depth + 1)

    for obj in objects:
        walk(obj)


def _attribute_one(index: int):
    """Attribute one molecule inside a worker. Returns (index, Attribution)."""
    attributor = _CTX["attributor"]
    dataset = _CTX["dataset"]
    graph = dataset[index]
    graph.graph_id = index
    return index, attributor.attribute(graph)


def resolve_workers(requested, n_items: int) -> int:
    """How many workers to actually use.

    Never more than there is work for, never more than the machine has, and
    never so few that the pool costs more than it saves.
    """
    if not requested:
        return 1
    if requested in ("auto", -1):
        requested = os.cpu_count() or 1
    workers = max(1, min(int(requested), n_items, os.cpu_count() or 1))
    return workers if workers > 1 and n_items > 1 else 1


def parallel_attributions(attributor, dataset, indices, workers: int):
    """Attributions for ``indices``, in ``indices`` order, computed in parallel.

    Falls back to the serial path for a single worker, so the caller has one
    code path and the serial behaviour is untouched when parallelism is off.
    """
    indices = list(indices)
    workers = resolve_workers(workers, len(indices))

    if workers == 1:
        out = []
        for i in indices:
            graph = dataset[i]
            graph.graph_id = i
            out.append(attributor.attribute(graph))
        return out

    import multiprocessing as mp

    _CTX.clear()
    _CTX.update({"attributor": attributor, "dataset": dataset})
    try:
        ctx = mp.get_context("fork")
        with ctx.Pool(workers, initializer=_init_worker) as pool:
            done = {}
            for index, attribution in pool.imap_unordered(
                    _attribute_one, indices, chunksize=1):
                done[index] = attribution
    finally:
        _CTX.clear()

    missing = [i for i in indices if i not in done]
    if missing:
        raise RuntimeError(
            f"{len(missing)} molecule(s) returned nothing from the worker pool "
            f"(first: {missing[0]}). Refusing to report a cell with holes in it.")
    # Reassembled in the caller's order: workers finish out of order, the
    # record list must not.
    return [done[i] for i in indices]


def _audit_one(index: int):
    """Attribute *and* audit one molecule inside a worker.

    Parallelising attribution alone was optimising the wrong half. Measured on
    the live run, an Integrated Gradients cell spends 0.6-0.7 s per molecule of
    which attribution is milliseconds: the cost is the audit around it --
    occlusion faithfulness runs a forward pass per motif, and cross-checkpoint
    stability attributes the molecule a second time against the early
    checkpoint. Both are per-molecule and independent, so both belong here.
    """
    from ..audit import audit_molecule, cross_checkpoint_stability
    from ..audit.motifs import decompose

    ctx = _CTX
    graph = ctx["dataset"][index]
    graph.graph_id = index
    attribution = ctx["attributor"].attribute(graph)

    # The decomposition depends only on the molecule, so it is computed once
    # and shared between the coherence/occlusion audit and the stability check.
    decomp = decompose(graph)
    record = audit_molecule(ctx["model"], graph, attribution, ctx["dataset_name"],
                            temperature=ctx["temperature"], decomp=decomp,
                            task=ctx["task"], occ_baseline=ctx["occ_baseline"])
    early = ctx.get("early_attr")
    if early is not None:
        try:
            record.stability = cross_checkpoint_stability(
                early, graph, decomp, attribution.node_attr)
        except Exception:  # noqa: BLE001 - one molecule must not fail a cell
            pass
    return index, record, attribution


def parallel_audit(*, attributor, dataset, indices, workers: int, model,
                   dataset_name: str, temperature, task: str, occ_baseline,
                   early_attr=None):
    """Per-molecule records for ``indices``, in ``indices`` order.

    Returns ``(records, first_attribution)`` so the caller can still draw its
    case-study figure from the first molecule's attribution.
    """
    indices = list(indices)
    workers = resolve_workers(workers, len(indices))
    if workers == 1:
        raise ValueError("caller should use its own serial loop for one worker")

    import multiprocessing as mp

    _CTX.clear()
    _CTX.update({"attributor": attributor, "dataset": dataset, "model": model,
                 "dataset_name": dataset_name, "temperature": temperature,
                 "task": task, "occ_baseline": occ_baseline,
                 "early_attr": early_attr})
    try:
        ctx = mp.get_context("fork")
        with ctx.Pool(workers, initializer=_init_worker) as pool:
            done = {}
            for index, record, attribution in pool.imap_unordered(
                    _audit_one, indices, chunksize=1):
                done[index] = (record, attribution)
    finally:
        _CTX.clear()

    missing = [i for i in indices if i not in done]
    if missing:
        raise RuntimeError(
            f"{len(missing)} molecule(s) returned nothing from the worker pool "
            f"(first: {missing[0]}). Refusing to report a cell with holes in it.")
    records = [done[i][0] for i in indices]
    return records, done[indices[0]][1]


__all__ = ["parallel_attributions", "parallel_audit", "resolve_workers",
           "to_cpu_for_fork"]
