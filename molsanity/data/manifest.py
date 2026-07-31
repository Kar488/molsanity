"""Dataset manifest: maps each dataset to loader, source, licence, cache path.

The manifest is the single source of provenance. Every loader records where the
data came from and verifies a checksum of the materialised cache.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    tier: int
    task: str  # "graph-classification" | "graph-regression"
    source: str  # human-readable provenance
    licence: str
    loader: str  # dotted path key resolved in registry
    has_ground_truth: bool
    notes: str = ""
    extras: dict = field(default_factory=dict)


# Canonical manifest. Loaders are resolved lazily (see registry.py) so importing
# this module never triggers a heavy download.
MANIFEST: dict[str, DatasetSpec] = {
    # ---- Tier 1: ground-truth / quasi-ground-truth --------------------------
    "MUTAG": DatasetSpec(
        name="MUTAG",
        tier=1,
        task="graph-classification",
        source="PyG TUDataset (Debnath et al. 1991)",
        licence="Public benchmark (TU Dortmund graph collection)",
        loader="mutag",
        has_ground_truth=True,
        notes=(
            "188 nitroaromatic compounds; quasi-GT motif = nitro (NO2) groups, "
            "the canonical mutagenicity signal. See LIMITATIONS.md."
        ),
    ),
    "BA-2Motifs": DatasetSpec(
        name="BA-2Motifs",
        tier=1,
        task="graph-classification",
        source="Synthetic (Luo et al. 2020, PGExplainer)",
        licence="Synthetic / MIT-style research use",
        loader="ba2motifs",
        has_ground_truth=True,
        notes="Barabasi-Albert base + house/cycle motif; exact node GT.",
    ),
    "SynthMotifs": DatasetSpec(
        name="SynthMotifs",
        tier=1,
        task="graph-classification",
        source="Synthetic (PyG ExplainerDataset: BA base + house/cycle motif)",
        licence="Synthetic / generated offline",
        loader="synthmotifs",
        has_ground_truth=True,
        notes=(
            "Exact node ground truth (injected-motif nodes). Offline BA-2Motifs "
            "equivalent; validates the audit against real GT, not a proxy."
        ),
        extras={"num_graphs": 1000, "num_nodes": 25},  # 1000 matches BA-2Motifs
    ),
    "SynthMotifsXL": DatasetSpec(
        name="SynthMotifsXL",
        tier=1,
        task="graph-classification",
        source="Synthetic (PyG ExplainerDataset: BA base + house/cycle motif)",
        licence="Synthetic / generated offline",
        loader="synthmotifs",
        has_ground_truth=True,
        notes=(
            "Larger exact-GT twin of SynthMotifs (600 graphs) for a statistically "
            "powered head-to-head: with a 20% test fold this yields ~120 molecules "
            "with exact node ground truth per attributor, enough for paired tests."
        ),
        extras={"num_graphs": 600, "num_nodes": 25},
    ),
    "ShapeGGen": DatasetSpec(
        name="ShapeGGen",
        tier=1,
        task="graph-classification",
        source="GraphXAI (Agarwal et al. 2023)",
        licence="MIT (GraphXAI)",
        loader="shapeggen",
        has_ground_truth=True,
        # ShapeGGen's generator verifies each candidate graph and gives up
        # after a few tries; only the smaller settings build reliably, so these
        # are the largest values observed to succeed rather than the largest we
        # would like. ~164 nodes yields ~100+ scoreable k-hop subgraphs, which
        # is already several times the n of the other exact-GT arms.
        extras={"hops": 2, "num_subgraphs": 20, "subgraph_size": 8,
                "prob_connection": 0.4, "max_graphs": 400, "seed": 0,
                "max_tries_verification": 15},
        notes=("Node classification, adapted to graph classification by taking "
               "each labelled node's k-hop enclosing subgraph (k = message "
               "passing depth), which is where its explanation lives. Needs "
               "GraphXAI from a source checkout; skip+log if unavailable."),
    ),
    "MolMotif": DatasetSpec(
        name="MolMotif",
        tier=1,
        task="graph-classification",
        source="MoleculeNet BBBP molecules, relabelled by substructure presence",
        licence="MoleculeNet (open)",
        loader="molmotif",
        has_ground_truth=True,
        extras={"source_dataset": "BBBP", "motif": "halogen_aromatic",
                "max_graphs": 1000, "radius": 1, "seed": 0},
        notes=("Real drug-like molecules with EXACT node ground truth: the "
               "label is presence of a chemical substructure, so that "
               "substructure determines the label by construction rather than "
               "by assumption. Closes the gap where every other ground-truth "
               "arm is either molecular-but-proxy (MUTAG) or "
               "exact-but-non-molecular (SynthMotifs, BA-2Motifs). Easy by "
               "design: a probe of the audit, not a hard benchmark."),
    ),
    # ---- Tier 2: real molecular property prediction -------------------------
    "ESOL": DatasetSpec(
        name="ESOL", tier=2, task="graph-regression",
        source="MoleculeNet via PyG", licence="MoleculeNet (open)",
        loader="moleculenet", has_ground_truth=False,
        extras={"molnet_name": "ESOL"},
    ),
    "FreeSolv": DatasetSpec(
        name="FreeSolv", tier=2, task="graph-regression",
        source="MoleculeNet via PyG", licence="MoleculeNet (open)",
        loader="moleculenet", has_ground_truth=False,
        extras={"molnet_name": "FreeSolv"},
    ),
    "Lipophilicity": DatasetSpec(
        name="Lipophilicity", tier=2, task="graph-regression",
        source="MoleculeNet via PyG", licence="MoleculeNet (open)",
        loader="moleculenet", has_ground_truth=False,
        extras={"molnet_name": "Lipo"},
    ),
    "BBBP": DatasetSpec(
        name="BBBP", tier=2, task="graph-classification",
        source="MoleculeNet via PyG", licence="MoleculeNet (open)",
        loader="moleculenet", has_ground_truth=False,
        extras={"molnet_name": "BBBP"},
    ),
    "BACE": DatasetSpec(
        name="BACE", tier=2, task="graph-classification",
        source="MoleculeNet via PyG", licence="MoleculeNet (open)",
        loader="moleculenet", has_ground_truth=False,
        extras={"molnet_name": "BACE"},
    ),
    "Tox21": DatasetSpec(
        name="Tox21", tier=2, task="graph-classification",
        source="MoleculeNet via PyG (multi-task; single task audited)",
        licence="MoleculeNet (open)",
        loader="moleculenet", has_ground_truth=False,
        notes="12-task nuclear-receptor/stress panel; we audit task 0 (NR-AR).",
        extras={"molnet_name": "Tox21", "task_index": 0, "task_name": "NR-AR",
                "num_classes": 2},
    ),
    # ---- Tier 3: chemistry-meets-medicine (TDC) -----------------------------
    "ClinTox": DatasetSpec(
        name="ClinTox", tier=3, task="graph-classification",
        source="MoleculeNet via PyG (clinical-trial toxicity; single task)",
        licence="MoleculeNet (open)",
        loader="moleculenet", has_ground_truth=False,
        notes="Clinical-trial toxicity (CT_TOX, task 1) — the chemistry-meets-"
              "medicine angle; imbalanced (112 toxic / 1368), class-weighted.",
        extras={"molnet_name": "ClinTox", "task_index": 1, "task_name": "CT_TOX",
                "num_classes": 2},
    ),
    "SIDER": DatasetSpec(
        name="SIDER", tier=3, task="graph-classification",
        source="MoleculeNet via PyG (side-effect panel; single task audited)",
        licence="MoleculeNet (open)",
        loader="moleculenet", has_ground_truth=False,
        notes="27 organ-system side-effect tasks; we audit task 0 (balanced).",
        extras={"molnet_name": "SIDER", "task_index": 0,
                "task_name": "Hepatobiliary disorders", "num_classes": 2},
    ),
    "DILI": DatasetSpec(
        name="DILI", tier=3, task="graph-classification",
        source="Therapeutics Data Commons", licence="TDC",
        loader="tdc", has_ground_truth=False, extras={"tdc_group": "Tox", "tdc_name": "DILI"},
    ),
    "hERG": DatasetSpec(
        name="hERG", tier=3, task="graph-classification",
        source="Therapeutics Data Commons", licence="TDC",
        loader="tdc", has_ground_truth=False, extras={"tdc_group": "Tox", "tdc_name": "hERG"},
    ),
}

# Explicitly out-of-scope, credential-gated modalities. Referencing these in a
# config is a no-op (skipped + logged), never an attempt to bypass gating.
BLOCKED = {"MIMIC", "eICU", "HiRID", "AmsterdamUMCdb"}


def get_spec(name: str) -> DatasetSpec:
    if name not in MANIFEST:
        raise KeyError(f"Unknown dataset '{name}'. Known: {sorted(MANIFEST)}")
    return MANIFEST[name]
