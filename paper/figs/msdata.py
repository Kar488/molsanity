"""Single source of truth for every number that reaches the manuscript.

Reads the **committed `results/` folder** — the output of the `full.yaml` run —
and nothing else. Nothing is hard-coded, interpolated or hand-entered:

  results/RESULTS.md                classification + regression audit matrices
  results/BENCHMARK.md              head-to-head matrix (stability / GraphFramEx
                                    characterisation / PyG-DIG unfaithfulness)
  results/PROGRESS.md               per-cell run ledger: done / failed / skipped
  results/artifacts/audit/<cell>/   per-molecule records + per-cell aggregate
  results/artifacts/run_manifest.json  seed, versions, hardware
  configs/full.yaml                 the planned grid, used to report coverage

Provenance note (important, and enforced in code): ``RESULTS.md`` is keyed by
cell and the last writer wins, so it still contains rows from *earlier*
reduced-budget runs for cells that failed in the latest run. A row is treated as
belonging to the current run only if that cell has per-molecule records under
``results/artifacts/audit/``; everything else is labelled ``carried``.
"""
from __future__ import annotations

import json
import math
import re
from functools import lru_cache
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RES = REPO / "results"
AUDIT = RES / "artifacts" / "audit"

# --- dataset regimes -------------------------------------------------------
SYNTHETIC = {"SynthMotifs", "SynthMotifsXL", "BA-2Motifs"}
REGRESSION = {"ESOL", "FreeSolv", "Lipophilicity"}


def regime_of(dataset: str) -> str:
    if dataset in SYNTHETIC:
        return "synthetic"
    if dataset in REGRESSION:
        return "regression"
    return "classification"


GT_EXACT = {"SynthMotifs", "SynthMotifsXL", "BA-2Motifs"}  # exact node GT by design
GT_PROXY = {"MUTAG"}                          # chemically motivated nitro proxy

KEY_COLS = {"dataset", "backbone", "attributor", "split", "method A", "method B"}


def _f(tok: str):
    tok = tok.strip().replace("**", "")
    if tok in {"", "—", "-", "–", "n/a", "NA"}:
        return None
    try:
        v = float(tok)
    except ValueError:
        return None
    return None if math.isnan(v) else v


def _md_tables(text: str):
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|") and i + 1 < len(lines) and re.match(
            r"^\|[\s:|-]+\|$", lines[i + 1].strip()
        ):
            header = [c.strip() for c in line.strip("|").split("|")]
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")])
                j += 1
            yield header, rows
            i = j
        else:
            i += 1


def _to_recs(header, rows) -> list[dict]:
    out = []
    for r in rows:
        if len(r) != len(header):
            continue
        out.append({k: (v.strip() if k in KEY_COLS else _f(v))
                    for k, v in zip(header, r)})
    return out


def cell_key(r) -> tuple:
    return (r["dataset"], r["backbone"], r["attributor"], r["split"])


def cell_dir(key) -> Path:
    return AUDIT / "__".join(key)


@lru_cache(maxsize=1)
def current_cells() -> frozenset:
    """Cells with per-molecule records from the latest committed run."""
    if not AUDIT.exists():
        return frozenset()
    return frozenset(tuple(p.name.split("__")) for p in AUDIT.iterdir()
                     if p.is_dir() and len(p.name.split("__")) == 4)


# --- public loaders --------------------------------------------------------

@lru_cache(maxsize=1)
def load_results() -> tuple[tuple[dict, ...], tuple[dict, ...]]:
    """(classification rows, regression rows) from results/RESULTS.md.

    Each row gains ``provenance`` = "current" (this run produced per-molecule
    records for it) or "carried" (row survives from an earlier run).
    """
    txt = (RES / "RESULTS.md").read_text()
    cls = reg = None
    for header, rows in _md_tables(txt):
        hs = set(header)
        if {"dataset", "backbone", "attributor", "gt_auroc"} <= hs:
            cls = (header, rows)
        elif {"dataset", "backbone", "attributor", "rmse"} <= hs:
            reg = (header, rows)
    if cls is None or reg is None:
        raise KeyError("results/RESULTS.md: expected classification + regression matrices")
    cur = current_cells()
    out = []
    for pack in (cls, reg):
        recs = _to_recs(*pack)
        for r in recs:
            r["regime"] = regime_of(r["dataset"])
            r["provenance"] = "current" if cell_key(r) in cur else "carried"
        out.append(tuple(recs))
    return out[0], out[1]


@lru_cache(maxsize=1)
def load_benchmark() -> tuple[dict, ...]:
    """Head-to-head matrix from results/BENCHMARK.md (this run's cells only)."""
    txt = (RES / "BENCHMARK.md").read_text()
    for header, rows in _md_tables(txt):
        if {"dataset", "backbone", "attributor", "occ_spearman",
            "stability"} <= set(header):
            recs = _to_recs(header, rows)
            cur = current_cells()
            for r in recs:
                r["regime"] = regime_of(r["dataset"])
                r["provenance"] = "current" if cell_key(r) in cur else "carried"
            return tuple(recs)
    raise KeyError("no head-to-head matrix in results/BENCHMARK.md")


@lru_cache(maxsize=1)
def load_records() -> dict:
    """{cell_key: [per-molecule record, ...]} from results/artifacts/audit/."""
    out = {}
    for key in sorted(current_cells()):
        p = cell_dir(key) / "records.json"
        if p.exists():
            out[key] = json.loads(p.read_text())
    return out


@lru_cache(maxsize=1)
def load_manifest() -> dict:
    return json.loads((RES / "artifacts" / "run_manifest.json").read_text())


@lru_cache(maxsize=1)
def load_ledger() -> tuple[dict, ...]:
    """The run ledger from results/PROGRESS.md: one entry per attempted cell."""
    txt = (RES / "PROGRESS.md").read_text()
    for header, rows in _md_tables(txt):
        if {"dataset", "backbone", "attributor", "status"} <= set(header):
            out = []
            for r in rows:
                if len(r) != len(header):
                    continue
                d = dict(zip(header, r))
                out.append({"dataset": d["dataset"].strip(),
                            "backbone": d["backbone"].strip(),
                            "attributor": d["attributor"].strip(),
                            "status": d["status"].strip(),
                            "detail": d.get("detail", "").strip()})
            return tuple(out)
    raise KeyError("no cell ledger in results/PROGRESS.md")


def ledger_tally() -> dict:
    led = load_ledger()
    t = {"done": 0, "failed": 0, "skipped": 0, "other": 0}
    for e in led:
        t[e["status"] if e["status"] in t else "other"] += 1
    return t


# --- statistics computed from the committed per-molecule records -----------

def _finite_pairs(a, b):
    out = [(x, y) for x, y in zip(a, b)
           if x is not None and y is not None
           and not math.isnan(x) and not math.isnan(y)]
    return [x for x, _ in out], [y for _, y in out]


def spearman(a, b):
    from scipy.stats import spearmanr
    a, b = _finite_pairs(a, b)
    if len(a) < 3:
        return float("nan"), float("nan")
    r = spearmanr(a, b)
    return float(r.correlation), float(r.pvalue)


def paired_wilcoxon(a, b):
    """Paired Wilcoxon signed-rank over molecules present in both lists."""
    from scipy.stats import wilcoxon
    import numpy as np
    a, b = _finite_pairs(a, b)
    if len(a) < 5:
        return {"n": len(a), "median_delta": float("nan"), "p": float("nan")}
    d = np.asarray(a) - np.asarray(b)
    med = float(np.median(d))
    if not d.any():
        return {"n": len(a), "median_delta": med, "p": float("nan")}
    try:
        p = float(wilcoxon(a, b).pvalue)
    except Exception:
        p = float("nan")
    return {"n": len(a), "median_delta": med, "p": p}


def benjamini_hochberg(pvalues) -> list[float]:
    """Benjamini-Hochberg adjusted p-values (q-values) for a family of tests.

    Every paired test in this paper belongs to a family: the attributor-vs-
    attributor contrasts within a cell, and the selection tests across cells.
    Reporting raw p-values across dozens of such tests inflates the false
    discovery rate, which is why the tables previously carried a note saying
    they should be read as descriptive. Controlling the FDR at the family level
    lets the surviving contrasts be read as findings instead.

    Returns adjusted values in the input order. NaN inputs stay NaN and are
    excluded from the family size, since a test that could not be computed is
    not a test that was performed.
    """
    import math

    idx = [i for i, p in enumerate(pvalues)
           if p is not None and not (isinstance(p, float) and math.isnan(p))]
    m = len(idx)
    out = [float("nan")] * len(pvalues)
    if m == 0:
        return out
    order = sorted(idx, key=lambda i: pvalues[i])
    # Step up from the largest p, enforcing monotonicity.
    prev = 1.0
    for rank in range(m, 0, -1):
        i = order[rank - 1]
        q = min(prev, float(pvalues[i]) * m / rank)
        out[i] = q
        prev = q
    return out


def by_graph(records) -> dict:
    return {r["graph_id"]: r for r in records}


def attributor_cells(dataset: str, backbone: str, split: str) -> dict:
    """{attributor: records} for every audited attributor of one cell family."""
    out = {}
    for key, recs in load_records().items():
        if key[0] == dataset and key[1] == backbone and key[3] == split:
            out[key[2]] = recs
    return out


def cell_mean(records, field) -> float:
    vals = [r.get(field) for r in records]
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    return sum(vals) / len(vals) if vals else float("nan")


def bootstrap_ci(records, field, n_boot: int = 2000, seed: int = 0):
    import numpy as np
    vals = np.array([r.get(field) for r in records if r.get(field) is not None],
                    dtype=float)
    vals = vals[np.isfinite(vals)]
    if vals.size < 2:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    means = vals[rng.integers(0, vals.size, (n_boot, vals.size))].mean(axis=1)
    return (float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5)))


FAITH_METRICS = ["occ_spearman", "fidelity_plus", "characterization"]


def selection_test(dataset: str, backbone: str, split: str) -> dict | None:
    """Would ranking attributors by a faithfulness metric pick the attributor
    the ground truth ranks best?  Recomputed here from the committed
    per-molecule records, because results/BENCHMARK_GT.md is empty for this run
    (its two target cells produced no records — see results/PROGRESS.md)."""
    cells = attributor_cells(dataset, backbone, split)
    cells = {a: r for a, r in cells.items()
             if not math.isnan(cell_mean(r, "gt_auroc"))}
    if len(cells) < 2:
        return None
    attrs = sorted(cells)
    gt = {a: cell_mean(cells[a], "gt_auroc") for a in attrs}
    gt_best = max(attrs, key=lambda a: gt[a])

    per_attr = {a: {"n_mol": len(cells[a]), "gt_auroc_mean": gt[a],
                    "gt_auroc_ci": bootstrap_ci(cells[a], "gt_auroc"),
                    **{m: cell_mean(cells[a], m) for m in FAITH_METRICS}}
                for a in attrs}

    selections, rank_corr = [], {}
    for m in FAITH_METRICS:
        vals = {a: cell_mean(cells[a], m) for a in attrs}
        if all(math.isnan(v) for v in vals.values()):
            continue
        pick = max(attrs, key=lambda a: (not math.isnan(vals[a]), vals[a]))
        rho, p_rho = spearman([vals[a] for a in attrs], [gt[a] for a in attrs])
        rank_corr[m] = {"rho": rho, "pvalue": p_rho}
        row = {"faithfulness_metric": m, "faithfulness_pick": pick,
               "faithfulness_pick_gt_auroc": gt[pick], "gt_best": gt_best,
               "gt_best_gt_auroc": gt[gt_best], "mismatch": pick != gt_best,
               "paired_gt_gap_median": None, "paired_gt_pvalue": None,
               "n_paired": None}
        if pick != gt_best:
            A, B = by_graph(cells[gt_best]), by_graph(cells[pick])
            shared = sorted(set(A) & set(B))
            w = paired_wilcoxon([A[g]["gt_auroc"] for g in shared],
                                [B[g]["gt_auroc"] for g in shared])
            row.update(paired_gt_gap_median=w["median_delta"],
                       paired_gt_pvalue=w["p"], n_paired=w["n"])
        selections.append(row)
    return {"dataset": dataset, "backbone": backbone, "split": split,
            "attributors": attrs, "gt_best": gt_best, "per_attributor": per_attr,
            "selections": selections, "rank_correlation": rank_corr}


def regime_table(records, fields=("gt_auroc", "occ_spearman", "stability")) -> dict:
    """Confidence/correctness regime stratification from per-molecule records."""
    out = {}
    for reg in ("confident_correct", "confident_error", "borderline"):
        sub = [r for r in records if r.get("regime") == reg]
        out[reg] = {"n": len(sub),
                    **{f: cell_mean(sub, f) if sub else float("nan")
                       for f in fields}}
    return out


def calibration_linkage(records, metric="occ_spearman") -> dict:
    """Spearman(1 - |confidence - correct|, reliability) over molecules."""
    conf = [r.get("confidence") for r in records]
    corr = [r.get("correct") for r in records]
    rel = [r.get(metric) for r in records]
    x = [1.0 - abs(c - k) if c is not None and k is not None else None
         for c, k in zip(conf, corr)]
    rho, p = spearman(x, rel)
    n = len(_finite_pairs(x, rel)[0])
    return {"spearman": rho, "pvalue": p, "n": n, "metric": metric}


# --- coverage --------------------------------------------------------------

def planned_cells() -> list[dict]:
    txt = (REPO / "configs" / "full.yaml").read_text()
    cells = [{"dataset": m.group(1), "backbone": m.group(2),
              "attributor": m.group(3)}
             for m in re.finditer(
                 r"-\s*\{dataset:\s*([\w\-]+),\s*backbone:\s*(\w+),"
                 r"\s*attributor:\s*(\w+)\}", txt)]
    splits = ["scaffold"]
    m = re.search(r"^extra_splits:\s*\[([^\]]*)\]", txt, re.M)
    if m:
        splits += [s.strip() for s in m.group(1).split(",") if s.strip()]
    return [{**c, "split": s} for c in cells for s in splits]


def coverage() -> dict:
    cur = current_cells()
    cls, reg = load_results()
    rows = list(cls) + list(reg)
    carried = {cell_key(r) for r in rows if r["provenance"] == "carried"}
    planned = {(c["dataset"], c["backbone"], c["attributor"], c["split"])
               for c in planned_cells()}
    tally = ledger_tally()
    return {
        "n_planned": len(planned),
        "n_current": len(cur),
        "n_current_in_plan": len(planned & set(cur)),
        "n_carried": len(carried),
        "n_rows": len(rows),
        "pending": sorted(planned - set(cur)),
        "extra": sorted(set(cur) - planned),
        "ledger": tally,
        "datasets_current": sorted({k[0] for k in cur}),
        "backbones_current": sorted({k[1] for k in cur}),
        "attributors_current": sorted({k[2] for k in cur}),
        "carried_cells": sorted(carried),
    }


def failure_reasons() -> dict:
    """Group failed ledger entries by the (truncated) error they reported."""
    out: dict[str, list] = {}
    for e in load_ledger():
        if e["status"] != "failed":
            continue
        msg = e["detail"].split("(see ")[0].strip()
        out.setdefault(msg, []).append(e)
    return out


def fmt(v, nd=3, dash="—"):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return dash
    return f"{v:.{nd}f}"


if __name__ == "__main__":
    cls, reg = load_results()
    bench = load_benchmark()
    cov = coverage()
    recs = load_records()
    man = load_manifest()
    print(f"run          : {man['config_name']} @ {man['timestamp']} "
          f"(cuda={man['cuda']['available']}, seed={man['seed']})")
    print(f"ledger       : {cov['ledger']}")
    print(f"RESULTS.md   : {len(cls)} classification rows, {len(reg)} regression rows")
    print(f"  provenance : {sum(1 for r in list(cls)+list(reg) if r['provenance']=='current')}"
          f" current / {cov['n_carried']} carried from earlier runs")
    print(f"BENCHMARK.md : {len(bench)} cells")
    print(f"audit records: {len(recs)} cells, "
          f"{sum(len(v) for v in recs.values())} molecule records")
    print(f"coverage     : {cov['n_current_in_plan']}/{cov['n_planned']} planned "
          f"cell-runs produced records this run")
    print("\nfailures by reason:")
    for msg, cells in failure_reasons().items():
        print(f"  {len(cells):2d} × {msg[:80]}")
    print("\ncarried-over cells (row present, no records this run):")
    for k in cov["carried_cells"]:
        print("   ", " × ".join(k))
