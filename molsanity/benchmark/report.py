"""Render the head-to-head benchmark to a Markdown table (BENCHMARK.md).

Pure formatting over computed audit records — no numbers are invented here.
"""
from __future__ import annotations

from pathlib import Path

from .tables import (
    HEADLINE_METRICS,
    discover_cells,
    head_to_head_table,
    paired_method_comparison,
)


def _fmt(v):
    if v is None:
        return "—"
    try:
        f = float(v)
        return "—" if f != f else f"{f:.3f}"
    except (TypeError, ValueError):
        return str(v)


def write_benchmark_md(path: str | Path = "BENCHMARK.md", seed: int = 0) -> dict:
    cells = discover_cells()
    if not cells:
        Path(path).write_text(
            "# BENCHMARK.md\n\n_No audited cells found. Run "
            "`python -m molsanity.run_all --config configs/full.yaml` first._\n"
        )
        return {"n_cells": 0}

    rows = head_to_head_table(cells, seed=seed)
    metric_cols = [m for m, _ in HEADLINE_METRICS]
    header = ["dataset", "backbone", "attributor", "split", "n_mol"] + metric_cols

    lines = [
        "# BENCHMARK.md — head-to-head audit matrix",
        "",
        "> Computed from per-molecule audit records under `artifacts/audit/`.",
        "> MolSanity metrics sit alongside the field-standard Fidelity±/sparsity",
        "> on the **same molecules**. GT AUROC is defined only where ground truth",
        "> exists (Tier-1). `—` = undefined/not-applicable, never a fabricated 0.",
        "",
        "## Attribution provenance",
        "",
    ]
    for m, src in HEADLINE_METRICS:
        lines.append(f"- **{m}** — {src}")
    lines += ["", "## Matrix", "", "| " + " | ".join(header) + " |",
              "| " + " | ".join(["---"] * len(header)) + " |"]
    for r in sorted(rows, key=lambda x: (x["dataset"], x["backbone"], x["attributor"], x["split"])):
        cells_out = [r.get("dataset"), r.get("backbone"), r.get("attributor"),
                     r.get("split"), str(r.get("n_mol"))]
        cells_out += [_fmt(r.get(m)) for m in metric_cols]
        lines.append("| " + " | ".join(cells_out) + " |")

    # Paired attributor comparisons where multiple attributors share a cell.
    lines += ["", "## Paired attributor comparisons (Wilcoxon, shared molecules)", ""]
    combos = sorted({(r["dataset"], r["backbone"], r["split"]) for r in rows})
    any_pairs = False
    for ds, bb, sp in combos:
        comps = paired_method_comparison(cells, ds, bb, sp, metric="occ_spearman")
        if not comps:
            continue
        any_pairs = True
        lines.append(f"**{ds} · {bb} · {sp} split** (metric: occ_spearman)")
        lines.append("")
        lines.append("| method A | method B | n | median Δ(A−B) | p-value |")
        lines.append("| --- | --- | --- | --- | --- |")
        for c in comps:
            lines.append(
                f"| {c['method_a']} | {c['method_b']} | {c['n_paired']} | "
                f"{_fmt(c['median_diff'])} | {_fmt(c['pvalue'])} |"
            )
        lines.append("")
    if not any_pairs:
        lines.append("_No cell has ≥2 attributors yet; add attributor rows to compare._")

    lines.append("")
    Path(path).write_text("\n".join(lines))
    return {"n_cells": len(cells), "n_rows": len(rows)}
