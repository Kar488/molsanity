"""How much of a reported effect is seed noise?

Every cell in a single-seed run is one deterministic split at one
initialisation, so a difference between two cells could be a real difference or
could be the spread you would get by re-running the same cell. This module
answers that directly: given a matrix run under several seeds, it reports, per
(dataset, backbone, attributor, split) cell, the across-seed mean and standard
deviation of each audit metric.

The number that matters is the comparison between the two spreads. If the
across-seed standard deviation of ground-truth localisation is comparable to the
gap the paper reports between two attributors, that gap is not evidence. If it
is much smaller, the gap is.

Writes ``SEED_VARIANCE.md``. Does nothing (and says so) on a single-seed run,
rather than reporting a standard deviation of zero as if it meant something.
"""
from __future__ import annotations

import math
import statistics as st
from pathlib import Path

from ..utils import get_logger

log = get_logger()

METRICS = ("gt_auroc", "occ_spearman", "fid+", "acc", "auc")
_LABEL = {"gt_auroc": "GT AUROC", "occ_spearman": "occlusion rho",
          "fid+": "Fidelity+", "acc": "accuracy", "auc": "ROC-AUC"}


def _key(row: dict) -> tuple:
    return (row.get("dataset"), row.get("backbone"), row.get("attributor"),
            row.get("split"))


def summarise_seeds(rows) -> dict:
    """Group rows by cell and compute across-seed statistics per metric."""
    by_cell: dict[tuple, list[dict]] = {}
    for r in rows:
        by_cell.setdefault(_key(r), []).append(r)

    cells = []
    for key, group in sorted(by_cell.items(), key=lambda kv: tuple(map(str, kv[0]))):
        seeds = sorted({r.get("seed") for r in group if r.get("seed") is not None})
        if len(seeds) < 2:
            continue
        entry = {"dataset": key[0], "backbone": key[1], "attributor": key[2],
                 "split": key[3], "seeds": seeds, "n_seeds": len(seeds),
                 "metrics": {}}
        for m in METRICS:
            vals = [r.get(m) for r in group]
            vals = [float(v) for v in vals
                    if v is not None and not (isinstance(v, float) and math.isnan(v))]
            if len(vals) < 2:
                continue
            entry["metrics"][m] = {
                "mean": st.mean(vals),
                "sd": st.stdev(vals),
                "min": min(vals),
                "max": max(vals),
                "n": len(vals),
            }
        if entry["metrics"]:
            cells.append(entry)
    return {"cells": cells, "n_cells": len(cells)}


def write_seed_variance_md(rows, out_path: str | Path = "SEED_VARIANCE.md") -> dict:
    summary = summarise_seeds(rows)
    out = Path(out_path)
    L = ["# SEED_VARIANCE.md — how much of each effect is seed noise?", ""]

    if not summary["cells"]:
        L += ["_This run used a single seed, so no across-seed spread can be "
              "computed. Set `seeds: [0, 1, 2]` in the config to populate this "
              "file. A single-seed run is reported as such rather than as a "
              "standard deviation of zero._", ""]
        out.write_text("\n".join(L))
        return summary

    n_seeds = max(c["n_seeds"] for c in summary["cells"])
    L += [f"Across-seed mean and standard deviation over {n_seeds} seeds, per "
          f"cell, for {summary['n_cells']} cells run under more than one seed. "
          "Read the standard deviation against the effect sizes quoted in "
          "RESULTS.md: an effect smaller than the spread here is not evidence.",
          ""]

    for m in METRICS:
        entries = [c for c in summary["cells"] if m in c["metrics"]]
        if not entries:
            continue
        L += [f"## {_LABEL[m]}", "",
              "| dataset | backbone | attributor | split | mean | sd | min | max |",
              "| --- | --- | --- | --- | ---: | ---: | ---: | ---: |"]
        for c in entries:
            s = c["metrics"][m]
            L.append(f"| {c['dataset']} | {c['backbone']} | {c['attributor']} "
                     f"| {c['split']} | {s['mean']:.3f} | {s['sd']:.3f} "
                     f"| {s['min']:.3f} | {s['max']:.3f} |")
        sds = [c["metrics"][m]["sd"] for c in entries]
        L += ["", f"Median across-seed sd: **{st.median(sds):.3f}**  ·  "
                  f"worst cell: **{max(sds):.3f}**", ""]

    out.write_text("\n".join(L) + "\n")
    log.info("Wrote %s (%d cells with >1 seed)", out, summary["n_cells"])
    return summary


__all__ = ["summarise_seeds", "write_seed_variance_md", "METRICS"]
