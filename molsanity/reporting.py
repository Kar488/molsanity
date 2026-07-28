"""Writers for RESULTS.md / PROGRESS.md — validated numbers and rolling status.

All numbers come from computed audit aggregates; nothing here invents values.
Rows are keyed by (dataset, backbone, attributor, split) so re-runs replace the
matching row in place rather than duplicating.
"""
from __future__ import annotations

import re
from pathlib import Path

RESULTS_HEADER = [
    "dataset", "backbone", "attributor", "split", "n_mol", "acc",
    "gt_auroc", "gt_auprc", "motif_top1", "occ_spearman", "occ_top1",
    "fid+", "fid-", "sparsity", "ece",
]


_INT_COLS = {"n_mol"}


def _fmt(v, col: str | None = None):
    if v is None:
        return "—"
    try:
        f = float(v)
        if f != f:  # NaN
            return "—"
        if col in _INT_COLS:
            return str(int(round(f)))
        return f"{f:.3f}"
    except (TypeError, ValueError):
        return str(v)


def results_row(cell: dict, agg: dict, train_res: dict, split_kind: str) -> dict:
    def m(name):
        return agg.get(name, {}).get("mean") if isinstance(agg.get(name), dict) else None

    return {
        "dataset": cell["dataset"],
        "backbone": cell["backbone"],
        "attributor": cell["attributor"],
        "split": split_kind,
        "n_mol": agg.get("n_molecules"),
        "acc": agg.get("accuracy"),
        "gt_auroc": m("gt_auroc"),
        "gt_auprc": m("gt_auprc"),
        "motif_top1": m("motif_top1_share"),
        "occ_spearman": m("occ_spearman"),
        "occ_top1": m("occ_top1_agreement"),
        "fid+": m("fidelity_plus"),
        "fid-": m("fidelity_minus"),
        "sparsity": m("sparsity"),
        "ece": train_res.get("test_ece"),
    }


def _row_key(row: dict) -> tuple:
    return (row["dataset"], row["backbone"], row["attributor"], row["split"])


def update_results_md(rows: list[dict], path: str | Path = "RESULTS.md", notes: str = "") -> None:
    path = Path(path)
    existing = _parse_existing_rows(path)
    for r in rows:
        existing[_row_key(r)] = r

    header = "| " + " | ".join(RESULTS_HEADER) + " |"
    sep = "| " + " | ".join(["---"] * len(RESULTS_HEADER)) + " |"
    lines = [
        "# RESULTS.md — validated numbers only",
        "",
        "> Every number here is computed by code in this run and traceable to a",
        "> logged artifact under `artifacts/`. No placeholders. See `LIMITATIONS.md`",
        "> for caveats (notably: MUTAG ground truth is a chemically motivated",
        "> nitro-motif *proxy*, not annotator labels).",
        "",
        "## Audit matrix (dataset × backbone × attributor)",
        "",
        header, sep,
    ]
    for key in sorted(existing):
        r = existing[key]
        lines.append("| " + " | ".join(_fmt(r.get(c), c) for c in RESULTS_HEADER) + " |")
    lines.append("")
    lines.append("### Metric legend")
    lines.append(
        "- **gt_auroc/gt_auprc**: attribution vs ground-truth motif mask "
        "(Tier-1 only; chance AUROC = 0.5). Below 0.5 means the attribution is "
        "*anti-aligned* with the known motif."
    )
    lines.append(
        "- **motif_top1**: fraction of attribution mass in the single top RDKit "
        "motif. **occ_spearman/occ_top1**: occlusion-vs-attribution faithfulness."
    )
    lines.append(
        "- **fid+/fid-**: Fidelity+ (prob drop removing salient atoms; higher is "
        "better) / Fidelity- (removing non-salient; lower is better). "
        "**ece**: test-set expected calibration error after temperature scaling."
    )
    if notes:
        lines += ["", "### Run notes", notes]
    lines.append("")
    path.write_text("\n".join(lines))


def _parse_existing_rows(path: Path) -> dict:
    rows: dict[tuple, dict] = {}
    if not path.exists():
        return rows
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != len(RESULTS_HEADER):
            continue
        if cells[0] in ("dataset", "---"):
            continue
        row = dict(zip(RESULTS_HEADER, cells))
        rows[_row_key(row)] = row
    return rows


def update_progress_md(
    ledger, config_name: str, timestamp: str, blockers: list[str], path: str | Path = "PROGRESS.md"
) -> None:
    path = Path(path)
    counts = ledger.counts()
    lines = [
        "# PROGRESS.md — MolSanity rolling progress",
        "",
        f"_Last run: `{config_name}` @ {timestamp}._",
        "",
        "## Cell tally",
        "",
        f"- done: **{counts['done']}**  · failed: **{counts['failed']}**  "
        f"· skipped/blocked: **{counts['skipped']}**",
        "",
        "## Cells (dataset × backbone × attributor)",
        "",
        "| dataset | backbone | attributor | status | detail |",
        "| --- | --- | --- | --- | --- |",
    ]
    for e in ledger.cells:
        lines.append(
            f"| {e.get('dataset','')} | {e.get('backbone','')} | "
            f"{e.get('attributor','')} | {e['status']} | {e.get('detail','')} |"
        )
    lines += ["", "## Blockers", ""]
    lines += [f"- {b}" for b in blockers] or ["_None._"]
    lines.append("")
    path.write_text("\n".join(lines))
