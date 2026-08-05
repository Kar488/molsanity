"""Dataset loaders with idempotent caching, checksum verification, provenance.

Each loader returns a :class:`LoadedDataset` bundling the PyG dataset object,
its :class:`DatasetSpec`, and a provenance record (source, licence, checksum,
per-graph count). Downloads are delegated to PyG's own cached downloaders; we
add a content checksum over the processed tensors and write a provenance JSON.
"""
from __future__ import annotations

import hashlib
import random as _random
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


def _load_molmotif(spec: DatasetSpec) -> LoadedDataset:
    """Real molecules relabelled so the ground truth is exact by construction."""
    from .molmotif import generate_mol_motif

    extras = spec.extras or {}
    src = load_dataset(extras.get("source_dataset", "BBBP"))
    graphs = generate_mol_motif(
        src.dataset,
        motif=extras.get("motif", "halogen_aromatic"),
        max_graphs=int(extras.get("max_graphs", 1000)),
        seed=int(extras.get("seed", 0)),
        radius=int(extras.get("radius", 1)),
    )
    cache_dir = DATA_ROOT / spec.name
    checksum = _verify_or_record_checksum(spec, graphs, cache_dir)
    prov = _write_provenance(spec, graphs, cache_dir, checksum)
    log.info("Loaded MolMotif: %d molecules with exact node ground truth",
             len(graphs))
    return LoadedDataset(spec, graphs, prov)


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


# Where each GraphXAI real-world dataset lives. Its ``.npz`` sits beside the
# module, so the module file locates the data without hard-coding a path.
_GRAPHXAI_MODULES = {
    "Benzene": "graphxai.datasets.real_world.benzene.benzene",
    "FluorideCarbonyl":
        "graphxai.datasets.real_world.fluoride_carbonyl.fluoride_carbonyl",
    "AlkaneCarbonyl":
        "graphxai.datasets.real_world.alkane_carbonyl.alkane_carbonyl",
}


def _graphxai_load_graphs(name: str, class_name: str):
    """Graphs and explanations from a GraphXAI real-world dataset.

    Deliberately bypasses the dataset *class* and calls ``load_graphs`` on the
    packaged ``.npz`` directly. ``Benzene.__init__`` reads the file and then
    calls ``GraphDataset.__init__``, which builds train/val/test indices with
    sklearn; on numpy 2 that raises

        'numpy.float32' object cannot be interpreted as an integer

    and takes the whole dataset down with it. The first sweep to schedule these
    arms lost all 84 cell-runs to it. We never use GraphXAI's splits --
    MolSanity does its own Bemis-Murcko and random splitting -- so the split
    code is pure liability here, and skipping it is a fix rather than a
    workaround.

    The class is still tried as a fallback, in case a future version moves the
    loading out of ``load_graphs``.
    """
    import importlib
    import os

    mod_path = _GRAPHXAI_MODULES.get(class_name)
    if mod_path is None:
        raise DatasetBlocked(
            f"{name}: no GraphXAI module registered for '{class_name}'.")
    try:
        from graphxai.datasets.real_world.extract_google_datasets import (
            load_graphs)
        mod = importlib.import_module(mod_path)
    except Exception as exc:  # blocked-tolerant, Hard Rule 4
        raise DatasetBlocked(
            f"{name} requires GraphXAI's {class_name}, which is not importable "
            f"({exc}). GraphXAI's published wheel omits its subpackages; "
            "install from a source checkout. Skipping and logging."
        ) from exc

    # The module names its data file in a *_datapath constant; fall back to the
    # only .npz sitting next to it rather than hard-coding either.
    datapath = next((v for k, v in vars(mod).items()
                     if k.endswith("datapath") and isinstance(v, str)), None)
    if datapath is None or not os.path.exists(datapath):
        here = os.path.dirname(getattr(mod, "__file__", "") or "")
        cands = sorted(f for f in os.listdir(here or ".") if f.endswith(".npz")) \
            if here else []
        if not cands:
            raise DatasetBlocked(
                f"{name}: no .npz data file beside {mod_path}. GraphXAI ships "
                "it in the source checkout; a wheel install has the class but "
                "not the data.")
        datapath = os.path.join(here, cands[0])

    try:
        out = load_graphs(datapath)
    except Exception as exc:
        log.warning("%s: load_graphs(%s) failed (%s); trying the dataset class",
                    name, os.path.basename(datapath), exc)
        try:
            import graphxai.datasets as gxd
            src = getattr(gxd, class_name)()
            return getattr(src, "graphs", None), getattr(src, "explanations", None)
        except Exception as exc2:
            raise DatasetBlocked(
                f"{name}: GraphXAI's {class_name} failed both directly "
                f"({exc}) and via its class ({exc2}). Skipping per Hard Rule 4."
            ) from exc2
    # load_graphs returns (graphs, explanations) or (graphs, explanations, ids).
    return out[0], out[1]


def _load_graphxai_mol(spec: DatasetSpec) -> LoadedDataset:
    """A real-molecule attribution benchmark from GraphXAI's ``real_world`` set.

    These are the Sanchez-Lengeling et al. (NeurIPS 2020) tasks as repackaged
    by GraphXAI: real molecules (ZINC-derived) with per-atom ground-truth
    rationales, published by a third party. That last property is the point.
    Every other exactly-labelled molecular arm in this study is one we built
    (MolMotif, MolMotifHard), and a benchmark constructed by the authors of the
    audit is worth less as corroboration than one that already existed.

    A graph may carry *several* explanations, because a molecule can contain
    several instances of the rationale substructure (two benzene rings, say).
    Any of them is a valid rationale, so the mask is their union: an atom
    belonging to any published pathway counts as ground truth. Taking only the
    first would mark real rationale atoms as negatives and score a correct
    attribution as wrong.

    Negatives keep an all-zero mask, as in MolMotif: they are needed to train
    the classifier, and ``attribution_gt_scores`` already returns NaN where a
    mask has one class, so they contribute to accuracy and not to GT AUROC.
    """
    import torch

    class_name = spec.extras.get("graphxai_class")
    seed = int(spec.extras.get("seed", 0))
    max_graphs = int(spec.extras.get("max_graphs", 1000))
    balance = bool(spec.extras.get("balance", True))

    graphs_in, expl_in = _graphxai_load_graphs(spec.name, class_name)
    if not graphs_in or expl_in is None or len(expl_in) != len(graphs_in):
        raise DatasetBlocked(
            f"{spec.name}: {class_name} exposed {len(graphs_in or [])} graphs "
            f"and {len(expl_in or [])} explanation sets; cannot align them.")

    def _union_mask(expls, n_nodes: int) -> "torch.Tensor":
        mask = torch.zeros(n_nodes, dtype=torch.float32)
        for e in (expls if isinstance(expls, (list, tuple)) else [expls]):
            imp = getattr(e, "node_imp", None)
            if imp is None:
                continue
            v = imp.detach().cpu().reshape(-1).float()
            if v.numel() != n_nodes:
                continue          # shape mismatch: skip rather than pad
            mask = torch.maximum(mask, (v > 0).float())
        return mask

    pos, neg, dropped = [], [], 0
    for g, expls in zip(graphs_in, expl_in):
        n = int(g.num_nodes)
        mask = _union_mask(expls, n)
        label = int(g.y.reshape(-1)[0])
        if label == 1:
            if mask.sum() == 0 or mask.sum() == n:
                dropped += 1     # a mask covering none or all cannot be scored
                continue
        else:
            mask = torch.zeros(n, dtype=torch.float32)
        (pos if label == 1 else neg).append((g, mask, label))

    rng = _random.Random(seed)
    if balance:
        k = min(len(pos), len(neg), max(max_graphs // 2, 1))
        if k == 0:
            raise DatasetBlocked(
                f"{spec.name}: {len(pos)} positive and {len(neg)} negative "
                "molecules with a scoreable mask; cannot build a balanced task.")
        pos, neg = rng.sample(pos, k), rng.sample(neg, k)
    picked = pos + neg
    rng.shuffle(picked)
    picked = picked[:max_graphs]

    graphs = []
    for g, mask, label in picked:
        d = g.clone() if hasattr(g, "clone") else g
        d.x = d.x.float()
        if d.edge_attr is not None:
            d.edge_attr = d.edge_attr.float()
        d.y = torch.tensor([label], dtype=torch.long)
        d.node_gt = mask
        graphs.append(d)

    n_pos = sum(1 for _, _, y in picked if y == 1)
    cache_dir = DATA_ROOT / spec.name
    checksum = _verify_or_record_checksum(spec, graphs, cache_dir)
    prov = _write_provenance(spec, graphs, cache_dir, checksum)
    log.info("Loaded %s (GraphXAI %s): %d molecules (%d positive), %d dropped "
             "for an unscoreable mask, checksum %s",
             spec.name, class_name, len(graphs), n_pos, dropped, checksum[:12])
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
    "molmotif": _load_molmotif,
    "tdc": _load_tdc,
    "graphxai_mol": _load_graphxai_mol,
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
