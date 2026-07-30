"""Dataset loaders with idempotent caching, checksum verification, provenance.

Each loader returns a :class:`LoadedDataset` bundling the PyG dataset object,
its :class:`DatasetSpec`, and a provenance record (source, licence, checksum,
per-graph count). Downloads are delegated to PyG's own cached downloaders; we
add a content checksum over the processed tensors and write a provenance JSON.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..utils import get_logger, write_json
from .manifest import BLOCKED, DatasetSpec, get_spec

log = get_logger()

DATA_ROOT = Path("data")


class DatasetBlocked(Exception):
    """Raised when a dataset is gated / unavailable. Callers skip + log."""


@dataclass
class LoadedDataset:
    spec: DatasetSpec
    dataset: Any  # a torch_geometric InMemoryDataset (list of Data)
    provenance: dict

    def __len__(self) -> int:
        return len(self.dataset)


# --------------------------------------------------------------------------- #
# Checksum over materialised graphs (order-independent per-graph, then combined)
# --------------------------------------------------------------------------- #
def dataset_checksum(dataset) -> str:
    """Deterministic content hash over a PyG dataset's tensors."""
    import numpy as np

    h = hashlib.sha256()
    for i in range(len(dataset)):
        g = dataset[i]
        for key in sorted(g.keys()):
            val = g[key]
            try:
                arr = np.ascontiguousarray(val.detach().cpu().numpy())
            except Exception:
                continue
            h.update(key.encode())
            h.update(arr.tobytes())
    return h.hexdigest()


def _write_provenance(spec: DatasetSpec, dataset, cache_dir: Path, checksum: str) -> dict:
    prov = {
        "name": spec.name,
        "tier": spec.tier,
        "task": spec.task,
        "source": spec.source,
        "licence": spec.licence,
        "num_graphs": len(dataset),
        "cache_dir": str(cache_dir),
        "checksum_sha256": checksum,
        "notes": spec.notes,
    }
    write_json(cache_dir / "provenance.json", prov)
    return prov


def _verify_or_record_checksum(spec: DatasetSpec, dataset, cache_dir: Path) -> str:
    """Idempotent checksum: record on first load, verify on later loads."""
    checksum = dataset_checksum(dataset)
    stamp = cache_dir / "checksum.sha256"
    if stamp.exists():
        prev = stamp.read_text().strip()
        if prev != checksum:
            log.warning(
                "%s checksum changed (%s -> %s); data cache may have been "
                "regenerated with different library versions.",
                spec.name, prev[:12], checksum[:12],
            )
    else:
        cache_dir.mkdir(parents=True, exist_ok=True)
        stamp.write_text(checksum)
        log.info("%s checksum recorded: %s", spec.name, checksum[:12])
    return checksum


# --------------------------------------------------------------------------- #
# Individual loaders
# --------------------------------------------------------------------------- #
def _load_mutag(spec: DatasetSpec) -> LoadedDataset:
    from torch_geometric.datasets import TUDataset

    cache_dir = DATA_ROOT / spec.name
    ds = TUDataset(root=str(cache_dir / "TUDataset"), name="MUTAG")
    checksum = _verify_or_record_checksum(spec, ds, cache_dir)
    prov = _write_provenance(spec, ds, cache_dir, checksum)
    log.info("Loaded MUTAG: %d graphs, checksum %s", len(ds), checksum[:12])
    return LoadedDataset(spec, ds, prov)


def _load_ba2motifs(spec: DatasetSpec) -> LoadedDataset:
    from torch_geometric.datasets import BA2MotifDataset

    cache_dir = DATA_ROOT / spec.name
    ds = BA2MotifDataset(root=str(cache_dir / "BA2Motif"))
    checksum = _verify_or_record_checksum(spec, ds, cache_dir)
    prov = _write_provenance(spec, ds, cache_dir, checksum)
    log.info("Loaded BA-2Motifs: %d graphs, checksum %s", len(ds), checksum[:12])
    return LoadedDataset(spec, ds, prov)


def _single_task_view(ds, task_index: int):
    """Reduce a multi-task MoleculeNet dataset to one binary task: select the
    task column, drop molecules with a missing (NaN) label for it, and relabel
    each graph's y to that single task. Keeps x/edge/smiles intact."""
    import math

    import torch

    out = []
    for i in range(len(ds)):
        g = ds[i]
        val = float(g.y.view(-1)[task_index])
        if math.isnan(val):
            continue
        g = g.clone()
        g.y = torch.tensor([[int(val)]], dtype=torch.long)
        out.append(g)
    return out


def _load_moleculenet(spec: DatasetSpec) -> LoadedDataset:
    from torch_geometric.datasets import MoleculeNet

    molnet_name = spec.extras["molnet_name"]
    cache_dir = DATA_ROOT / spec.name
    ds = MoleculeNet(root=str(cache_dir / "MoleculeNet"), name=molnet_name)

    task_index = spec.extras.get("task_index")
    if task_index is not None:
        ds = _single_task_view(ds, task_index)
        log.info("%s: reduced to single task #%d (%s), %d labelled molecules",
                 spec.name, task_index, spec.extras.get("task_name", ""), len(ds))

    checksum = _verify_or_record_checksum(spec, ds, cache_dir)
    prov = _write_provenance(spec, ds, cache_dir, checksum)
    log.info("Loaded %s: %d graphs, checksum %s", spec.name, len(ds), checksum[:12])
    return LoadedDataset(spec, ds, prov)


def _load_synthmotifs(spec: DatasetSpec) -> LoadedDataset:
    from .synthetic import generate_synth_motifs

    cache_dir = DATA_ROOT / spec.name
    ds = generate_synth_motifs(
        num_graphs=spec.extras.get("num_graphs", 200),
        num_nodes=spec.extras.get("num_nodes", 25),
        seed=0,
    )
    checksum = _verify_or_record_checksum(spec, ds, cache_dir)
    prov = _write_provenance(spec, ds, cache_dir, checksum)
    log.info("Loaded SynthMotifs: %d graphs, checksum %s", len(ds), checksum[:12])
    return LoadedDataset(spec, ds, prov)


def _load_shapeggen(spec: DatasetSpec) -> LoadedDataset:
    """ShapeGGen as a graph-classification task, via k-hop enclosing subgraphs.

    ShapeGGen is a *node* classification benchmark on one large graph, while
    every MolSanity axis is defined per instance at the graph level. The two are
    reconciled the way the node-explainability literature already does it: a
    node's explanation lives in its computation graph, i.e. its k-hop
    neighbourhood, where k is the number of message-passing layers. So each
    labelled node becomes one instance, its enclosing k-hop subgraph is the
    "molecule", its class is the graph label, and GraphXAI's per-node
    explanation restricted to that subgraph is the exact node ground truth.

    This adds no new attribution or evaluation logic; it is a data adapter, and
    the audit downstream is unchanged. GraphXAI's setup.py packages only the
    top-level module, so a wheel install is importable but unusable; install
    from a source checkout (and note it needs ``ipdb``).
    """
    import torch
    from torch_geometric.data import Data
    from torch_geometric.utils import k_hop_subgraph

    try:
        from graphxai.datasets import ShapeGGen
    except Exception as exc:  # blocked-tolerant
        raise DatasetBlocked(
            f"ShapeGGen requires GraphXAI, which is not importable ({exc}). "
            "Install it from a source checkout (its published wheel omits the "
            "subpackages). Skipping and logging per Hard Rule 4."
        ) from exc

    extras = spec.extras or {}
    hops = int(extras.get("hops", 2))
    seed = int(extras.get("seed", 0))
    max_graphs = int(extras.get("max_graphs", 400))

    from ..utils import set_global_seed

    set_global_seed(seed)
    src = ShapeGGen(
        model_layers=hops,
        num_subgraphs=int(extras.get("num_subgraphs", 100)),
        prob_connection=float(extras.get("prob_connection", 0.4)),
        subgraph_size=int(extras.get("subgraph_size", 8)),
        seed=seed,
        max_tries_verification=int(extras.get("max_tries_verification", 15)),
    )
    big = src.graph
    n_total = int(big.num_nodes)

    def _explained_nodes(expl) -> set[int]:
        """Node indices GraphXAI marks as the rationale for one node."""
        out: set[int] = set()
        for e in (expl if isinstance(expl, (list, tuple)) else [expl]):
            nm = getattr(e, "node_imp", None)
            idx = getattr(e, "node_reference", None)
            if nm is None:
                continue
            imp = nm.detach().cpu().numpy().reshape(-1)
            if idx is not None:                       # local -> global mapping
                keys = list(idx.keys()) if isinstance(idx, dict) else list(idx)
                for local, g in enumerate(keys):
                    if local < imp.shape[0] and imp[local] > 0:
                        out.add(int(g))
            elif imp.shape[0] == n_total:
                out.update(int(v) for v in imp.nonzero()[0])
        return out

    graphs, skipped = [], 0
    for node in range(n_total):
        if len(graphs) >= max_graphs:
            break
        subset, edge_index, mapping, _ = k_hop_subgraph(
            node, hops, big.edge_index, relabel_nodes=True, num_nodes=n_total)
        if int(subset.numel()) < 3 or int(edge_index.numel()) == 0:
            skipped += 1
            continue
        rationale = _explained_nodes(src.explanations[node])
        gt = torch.tensor([1.0 if int(g) in rationale else 0.0 for g in subset],
                          dtype=torch.float32)
        if gt.sum() == 0 or gt.sum() == gt.numel():
            # A degenerate mask cannot be scored; drop rather than score it.
            skipped += 1
            continue
        g = Data(
            x=big.x[subset].float(),
            edge_index=edge_index,
            edge_attr=torch.ones(edge_index.size(1), 1),
            y=torch.tensor([int(big.y[node])], dtype=torch.long),
            num_nodes=int(subset.numel()),
        )
        g.node_gt = gt
        g.seed_node = int(mapping[0])
        graphs.append(g)

    if len(graphs) < 20:
        raise DatasetBlocked(
            f"ShapeGGen produced only {len(graphs)} scoreable subgraphs "
            f"({skipped} skipped as too small or degenerately masked); "
            "not enough to audit."
        )

    cache_dir = DATA_ROOT / spec.name
    checksum = _verify_or_record_checksum(spec, graphs, cache_dir)
    prov = _write_provenance(spec, graphs, cache_dir, checksum)
    log.info("Loaded ShapeGGen: %d %d-hop subgraphs from %d nodes (%d skipped)",
             len(graphs), hops, n_total, skipped)
    return LoadedDataset(spec, graphs, prov)


_TDC_GROUPS = {
    "Tox": "single_pred.Tox",
    "ADME": "single_pred.ADME",
    "HTS": "single_pred.HTS",
}


def _load_tdc(spec: DatasetSpec) -> LoadedDataset:
    """Load a Therapeutics Data Commons single-prediction task.

    TDC serves SMILES + a binary label; we featurise with the *same* PyG
    ``from_smiles`` encoding MoleculeNet uses (x: 9-dim, edge_attr: 3-dim), so
    the backbones are drop-in compatible. Molecules RDKit cannot parse are
    skipped and counted. Blocked-tolerant: a missing PyTDC or an unreachable
    download raises :class:`DatasetBlocked` so the run logs it and continues.
    """
    try:
        from tdc import single_pred  # noqa: F401
        from torch_geometric.utils import from_smiles
    except Exception as exc:  # blocked-tolerant
        raise DatasetBlocked(
            f"{spec.name} requires PyTDC which is not installed ({exc}). "
            "Skipping and logging per Hard Rule 4."
        ) from exc

    import torch

    group = spec.extras["tdc_group"]
    tdc_name = spec.extras["tdc_name"]
    if group not in _TDC_GROUPS:
        raise DatasetBlocked(f"Unsupported TDC group '{group}' for {spec.name}.")

    cache_dir = DATA_ROOT / spec.name
    cache_dir.mkdir(parents=True, exist_ok=True)
    try:
        loader_cls = getattr(single_pred, group)
        df = loader_cls(name=tdc_name, path=str(cache_dir / "tdc")).get_data()
    except Exception as exc:  # network / server / gating — stay blocked-tolerant
        raise DatasetBlocked(
            f"{spec.name}: TDC fetch failed ({exc}). Skipping per Hard Rule 4."
        ) from exc

    graphs = []
    n_skipped = 0
    for idx, row in enumerate(df.itertuples(index=False)):
        smiles = getattr(row, "Drug")
        label = int(getattr(row, "Y"))
        try:
            g = from_smiles(smiles)
        except Exception:
            n_skipped += 1
            continue
        if g.x is None or g.num_nodes == 0 or g.edge_index.numel() == 0:
            n_skipped += 1
            continue
        g.y = torch.tensor([[label]], dtype=torch.long)
        g.smiles = smiles
        graphs.append(g)
    if not graphs:
        raise DatasetBlocked(f"{spec.name}: no parseable molecules from TDC.")
    if n_skipped:
        log.info("%s: skipped %d unparseable molecules", spec.name, n_skipped)

    checksum = _verify_or_record_checksum(spec, graphs, cache_dir)
    prov = _write_provenance(spec, graphs, cache_dir, checksum)
    log.info("Loaded %s (TDC %s/%s): %d graphs, checksum %s",
             spec.name, group, tdc_name, len(graphs), checksum[:12])
    return LoadedDataset(spec, graphs, prov)


_LOADERS = {
    "mutag": _load_mutag,
    "ba2motifs": _load_ba2motifs,
    "synthmotifs": _load_synthmotifs,
    "moleculenet": _load_moleculenet,
    "shapeggen": _load_shapeggen,
    "tdc": _load_tdc,
}


def load_dataset(name: str) -> LoadedDataset:
    """Load a dataset by manifest name. Raises DatasetBlocked for gated data."""
    if name in BLOCKED:
        raise DatasetBlocked(
            f"{name} is a credential-gated modality out of scope for MolSanity "
            "(Hard Rule 4). Skipping."
        )
    spec = get_spec(name)
    loader = _LOADERS.get(spec.loader)
    if loader is None:
        raise DatasetBlocked(f"No loader registered for '{spec.loader}'.")
    return loader(spec)
