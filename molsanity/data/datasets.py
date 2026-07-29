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
    try:
        import graphxai  # noqa: F401
    except Exception as exc:  # blocked-tolerant
        raise DatasetBlocked(
            f"ShapeGGen requires GraphXAI which is not installed ({exc}). "
            "Skipping and logging per Hard Rule 4."
        ) from exc
    raise DatasetBlocked("ShapeGGen loader not yet wired (Milestone 4).")


def _load_tdc(spec: DatasetSpec) -> LoadedDataset:
    try:
        import tdc  # noqa: F401
    except Exception as exc:  # blocked-tolerant
        raise DatasetBlocked(
            f"{spec.name} requires PyTDC which is not installed ({exc}). "
            "Skipping and logging per Hard Rule 4."
        ) from exc
    raise DatasetBlocked(f"{spec.name} TDC loader not yet wired (Milestone 4).")


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
