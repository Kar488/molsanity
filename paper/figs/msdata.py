"""Single source of truth for every number that reaches the manuscript.

Parses the *committed* result artifacts of the repository — nothing is
hard-coded, interpolated or hand-entered:

  RESULTS.md        classification + regression audit matrices
  BENCHMARK.md      head-to-head matrix (adds stability / GraphFramEx
                    characterization / PyG-DIG unfaithfulness) + paired Wilcoxon
  BENCHMARK_GT.json faithfulness-only-selection experiment (two regimes)
  configs/full.yaml the *planned* grid, used to report coverage honestly

Every consumer (figure scripts, LaTeX table generator) imports from here, so
re-running the paper pipeline after more cells land refreshes everything.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# --- dataset regimes -------------------------------------------------------
# Grouping used for colour/marker encoding in the figures. Derived from the
# task each dataset carries in the repo (RESULTS.md has separate classification
# and regression matrices; the synthetic Tier-1 sets carry exact node GT).
SYNTHETIC = {"SynthMotifs", "SynthMotifsXL"}
REGRESSION = {"ESOL", "FreeSolv", "Lipophilicity"}


def regime_of(dataset: str) -> str:
    if dataset in SYNTHETIC:
        return "synthetic"
    if dataset in REGRESSION:
        return "regression"
    return "classification"


# Ground-truth availability, as the repo defines it.
GT_EXACT = {"SynthMotifs", "SynthMotifsXL"}   # exact node-level ground truth
GT_PROXY = {"MUTAG"}                          # chemically motivated nitro proxy


def _f(tok: str):
    """Parse one markdown table cell into a float, or None for '—'."""
    tok = tok.strip().replace("**", "")
    if tok in {"", "—", "-", "–", "n/a", "NA"}:
        return None
    try:
        v = float(tok)
    except ValueError:
        return None
    return None if math.isnan(v) else v


def _md_tables(text: str):
    """Yield (header:list[str], rows:list[list[str]]) for every markdown table."""
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


def _table_with(text: str, must_have: set[str]):
    for header, rows in _md_tables(text):
        if must_have.issubset(set(header)):
            return header, rows
    raise KeyError(f"no markdown table with columns {must_have}")


def _records(path: Path, must_have: set[str]) -> list[dict]:
    header, rows = _table_with(path.read_text(), must_have)
    out = []
    for r in rows:
        if len(r) != len(header):
            continue
        rec = {}
        for k, v in zip(header, r):
            rec[k] = v.strip() if k in KEY_COLS else _f(v)
        out.append(rec)
    return out


KEY_COLS = {"dataset", "backbone", "attributor", "split", "method A", "method B"}


# --- public loaders --------------------------------------------------------

def load_results() -> tuple[list[dict], list[dict]]:
    """(classification rows, regression rows) from RESULTS.md."""
    txt = (REPO / "RESULTS.md").read_text()
    cls = reg = None
    for header, rows in _md_tables(txt):
        hs = set(header)
        if {"dataset", "backbone", "attributor", "gt_auroc"} <= hs:
            cls = (header, rows)
        elif {"dataset", "backbone", "attributor", "rmse"} <= hs:
            reg = (header, rows)
    if cls is None or reg is None:
        raise KeyError("RESULTS.md: expected a classification and a regression matrix")

    def to_recs(header, rows):
        out = []
        for r in rows:
            if len(r) != len(header):
                continue
            out.append({k: (v.strip() if k in KEY_COLS else _f(v))
                        for k, v in zip(header, r)})
        return out

    return to_recs(*cls), to_recs(*reg)


def load_benchmark() -> list[dict]:
    """The head-to-head matrix from BENCHMARK.md (one row per audited cell)."""
    recs = _records(REPO / "BENCHMARK.md",
                    {"dataset", "backbone", "attributor", "gt_auroc",
                     "occ_spearman", "stability"})
    for r in recs:
        r["regime"] = regime_of(r["dataset"])
    return recs


def load_paired() -> dict[str, list[dict]]:
    """Paired Wilcoxon blocks from BENCHMARK.md, keyed by their bold heading."""
    txt = (REPO / "BENCHMARK.md").read_text()
    blocks: dict[str, list[dict]] = {}
    cur = None
    lines = txt.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^\*\*(.+?)\*\*\s*\(metric:\s*(\w+)\)", line.strip())
        if m:
            cur = m.group(1)
            blocks[cur] = []
            continue
        if cur and line.strip().startswith("|") and not re.match(
            r"^\|[\s:|-]+\|$", line.strip()
        ):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) == 5 and cells[0] != "method A":
                blocks[cur].append({
                    "A": cells[0], "B": cells[1], "n": _f(cells[2]),
                    "median_delta": _f(cells[3]), "p": _f(cells[4]),
                })
    return {k: v for k, v in blocks.items() if v}


def load_benchmark_gt() -> list[dict]:
    """The faithfulness-only-selection experiment (BENCHMARK_GT.json)."""
    return json.loads((REPO / "BENCHMARK_GT.json").read_text())


# --- coverage --------------------------------------------------------------

def planned_cells() -> list[dict]:
    """Parse the planned grid out of configs/full.yaml without a YAML dep."""
    txt = (REPO / "configs" / "full.yaml").read_text()
    cells = []
    for m in re.finditer(
        r"-\s*\{dataset:\s*([\w\-]+),\s*backbone:\s*(\w+),\s*attributor:\s*(\w+)\}", txt
    ):
        cells.append({"dataset": m.group(1), "backbone": m.group(2),
                      "attributor": m.group(3)})
    splits = ["scaffold"]
    m = re.search(r"^extra_splits:\s*\[([^\]]*)\]", txt, re.M)
    if m:
        splits += [s.strip() for s in m.group(1).split(",") if s.strip()]
    out = []
    for c in cells:
        for s in splits:
            out.append({**c, "split": s})
    return out


def coverage() -> dict:
    """Honest accounting of planned vs. completed cells."""
    done = load_benchmark()
    done_keys = {(r["dataset"], r["backbone"], r["attributor"], r["split"])
                 for r in done}
    planned = planned_cells()
    planned_keys = {(c["dataset"], c["backbone"], c["attributor"], c["split"])
                    for c in planned}
    return {
        "n_planned": len(planned_keys),
        "n_done_in_plan": len(planned_keys & done_keys),
        "n_done_total": len(done_keys),
        "n_extra": len(done_keys - planned_keys),
        "pending": sorted(planned_keys - done_keys),
        "extra": sorted(done_keys - planned_keys),
        "datasets_done": sorted({k[0] for k in done_keys}),
        "backbones_done": sorted({k[1] for k in done_keys}),
        "attributors_done": sorted({k[2] for k in done_keys}),
        "datasets_planned": sorted({k[0] for k in planned_keys}),
        "backbones_planned": sorted({k[1] for k in planned_keys}),
        "attributors_planned": sorted({k[2] for k in planned_keys}),
    }


def fmt(v, nd=3, dash="—"):
    """Format a value exactly as it appears in the source table (no re-rounding
    beyond the committed precision)."""
    if v is None:
        return dash
    return f"{v:.{nd}f}"


if __name__ == "__main__":
    cls, reg = load_results()
    bench = load_benchmark()
    cov = coverage()
    print(f"RESULTS.md   : {len(cls)} classification rows, {len(reg)} regression rows")
    print(f"BENCHMARK.md : {len(bench)} audited cells")
    print(f"paired blocks: {len(load_paired())}")
    print(f"coverage     : {cov['n_done_in_plan']}/{cov['n_planned']} planned "
          f"cell-runs complete; {cov['n_extra']} audited cells outside the plan "
          f"({cov['n_done_total']} committed total)")
    print("pending:")
    for p in cov["pending"]:
        print("   ", " × ".join(p))
