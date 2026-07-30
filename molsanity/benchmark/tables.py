"""Head-to-head benchmark tables + paired statistics across the audit matrix.

Reads the per-cell audit records written under ``artifacts/audit/`` and builds:
  - a head-to-head table (attributors × datasets × metrics), and
  - paired Wilcoxon comparisons between attributors on shared molecules,

so MolSanity's audit sits directly alongside the field-standard metrics
(Fidelity± / sparsity) it also computes, on the same molecules.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from ..audit.stats import paired_wilcoxon, summarise

AUDIT_ROOT = Path("artifacts") / "audit"

# Metrics surfaced in the head-to-head table and where each comes from.
HEADLINE_METRICS = [
    ("gt_auroc", "MolSanity/GT"),
    ("occ_spearman", "MolSanity/faithfulness"),
    ("stability", "MolSanity/stability"),
    ("motif_top1_share", "MolSanity/coherence"),
    ("fidelity_plus", "field-standard"),
    ("fidelity_minus", "field-standard"),
    ("sparsity", "field-standard"),
    ("characterization", "GraphFramEx"),
    ("unfaithfulness", "PyG/DIG"),
]


def _load_cell_records(cell_dir: Path) -> list[dict]:
    rec_path = cell_dir / "records.json"
    if not rec_path.exists():
        return []
    return json.loads(rec_path.read_text())


def discover_cells(root: Path = AUDIT_ROOT) -> dict[str, list[dict]]:
    """Map cell_id -> list of per-molecule records for every audited cell."""
    cells = {}
    if not root.exists():
        return cells
    for d in sorted(root.iterdir()):
        if d.is_dir():
            recs = _load_cell_records(d)
            if recs:
                cells[d.name] = recs
    return cells


def _parse_cell_id(cell_id: str) -> dict:
    parts = cell_id.split("__")
    keys = ["dataset", "backbone", "attributor", "split"]
    return dict(zip(keys, parts + [""] * (len(keys) - len(parts))))


def head_to_head_table(cells: dict[str, list[dict]], seed: int = 0) -> list[dict]:
    """One row per cell with summarised headline metrics."""
    rows = []
    for cell_id, recs in cells.items():
        meta = _parse_cell_id(cell_id)
        row = {**meta, "n_mol": len(recs)}
        for metric, _src in HEADLINE_METRICS:
            vals = np.array([r.get(metric, np.nan) for r in recs], dtype=np.float64)
            s = summarise(vals, name=metric, seed=seed)
            row[metric] = s["mean"]
            row[f"{metric}__ci"] = (s["ci95_lo"], s["ci95_hi"])
        rows.append(row)
    return rows


def paired_method_comparison(
    cells: dict[str, list[dict]], dataset: str, backbone: str, split: str,
    metric: str = "occ_spearman",
) -> list[dict]:
    """Paired Wilcoxon between every pair of attributors on shared molecules.

    Molecules are paired by graph_id within the same (dataset, backbone, split).
    """
    subset = {}
    for cell_id, recs in cells.items():
        m = _parse_cell_id(cell_id)
        if m["dataset"] == dataset and m["backbone"] == backbone and m["split"] == split:
            by_id = {r["graph_id"]: r.get(metric, np.nan) for r in recs}
            subset[m["attributor"]] = by_id

    methods = sorted(subset)
    out = []
    for i in range(len(methods)):
        for j in range(i + 1, len(methods)):
            a, b = methods[i], methods[j]
            shared = sorted(set(subset[a]) & set(subset[b]))
            va = np.array([subset[a][g] for g in shared], dtype=np.float64)
            vb = np.array([subset[b][g] for g in shared], dtype=np.float64)
            res = paired_wilcoxon(va, vb)
            out.append({
                "dataset": dataset, "backbone": backbone, "split": split,
                "metric": metric, "method_a": a, "method_b": b,
                "n_paired": res["n"], "median_diff": res["median_diff"],
                "pvalue": res["pvalue"],
            })
    return out
