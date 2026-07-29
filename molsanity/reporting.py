"""Writers for RESULTS.md / PROGRESS.md — validated numbers and rolling status.

All numbers come from computed audit aggregates; nothing here invents values.
Rows are keyed by (dataset, backbone, attributor, split) so re-runs replace the
matching row in place rather than duplicating.
"""
from __future__ import annotations

import re
from pathlib import Path

RESULTS_HEADER = [
    "dataset", "backbone", "attributor", "split", "n_mol", "acc", "auc",
    "gt_auroc", "gt_auprc", "motif_top1", "occ_spearman", "occ_top1",
    "fid+", "fid-", "sparsity", "ece",
]

# Regression table (no class accuracy / GT / ECE; adds RMSE/MAE/R2).
REGRESSION_HEADER = [
    "dataset", "backbone", "attributor", "split", "n_mol", "rmse", "mae", "r2",
    "motif_top1", "occ_spearman", "occ_top1", "fid+", "fid-", "sparsity",
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
        "task": train_res.get("task", "graph-classification"),
        "dataset": cell["dataset"],
        "backbone": cell["backbone"],
        "attributor": cell["attributor"],
        "split": split_kind,
        "n_mol": agg.get("n_molecules"),
        "acc": agg.get("accuracy"),
        "auc": train_res.get("test_auc"),
        "gt_auroc": m("gt_auroc"),
        "gt_auprc": m("gt_auprc"),
        "motif_top1": m("motif_top1_share"),
        "occ_spearman": m("occ_spearman"),
        "occ_top1": m("occ_top1_agreement"),
        "fid+": m("fidelity_plus"),
        "fid-": m("fidelity_minus"),
        "sparsity": m("sparsity"),
        "ece": train_res.get("test_ece"),
        "rmse": train_res.get("test_rmse"),
        "mae": train_res.get("test_mae"),
        "r2": train_res.get("test_r2"),
    }


def _row_key(row: dict) -> tuple:
    return (row["dataset"], row["backbone"], row["attributor"], row["split"])


def _table(rows: list[dict], header: list[str]) -> list[str]:
    lines = ["| " + " | ".join(header) + " |",
             "| " + " | ".join(["---"] * len(header)) + " |"]
    for r in sorted(rows, key=_row_key):
        lines.append("| " + " | ".join(_fmt(r.get(c), c) for c in header) + " |")
    return lines


def update_results_md(rows: list[dict], path: str | Path = "RESULTS.md", notes: str = "") -> None:
    path = Path(path)
    existing = _parse_existing_rows(path)
    for r in rows:
        existing[_row_key(r)] = r

    cls_rows = [r for r in existing.values() if r.get("task") != "graph-regression"]
    reg_rows = [r for r in existing.values() if r.get("task") == "graph-regression"]

    lines = [
        "# RESULTS.md — validated numbers only",
        "",
        "> Every number here is computed by code in this run and traceable to a",
        "> logged artifact under `artifacts/`. No placeholders. See `LIMITATIONS.md`",
        "> for caveats (notably: MUTAG ground truth is a chemically motivated",
        "> nitro-motif *proxy*, not annotator labels).",
        "",
        "## Classification audit matrix (dataset × backbone × attributor)",
        "",
        *_table(cls_rows, RESULTS_HEADER),
        "",
    ]
    if reg_rows:
        lines += [
            "## Regression audit matrix",
            "",
            *_table(reg_rows, REGRESSION_HEADER),
            "",
        ]
    lines += [
        "### Metric legend",
        "- **acc/auc**: classification test accuracy / ROC-AUC (AUC is the honest "
        "signal on imbalanced sets, where accuracy tracks the majority class). "
        "**gt_auroc/gt_auprc**: attribution vs ground-truth motif mask (Tier-1 "
        "only; chance AUROC = 0.5; below 0.5 = *anti-aligned* with the motif).",
        "- **rmse/mae/r2**: regression test-set error metrics (original units).",
        "- **motif_top1**: fraction of attribution mass in the single top RDKit "
        "motif. **occ_spearman/occ_top1**: occlusion-vs-attribution faithfulness.",
        "- **fid+/fid-**: Fidelity+ (predicted prob/value drop removing salient "
        "atoms; higher is better) / Fidelity- (removing non-salient; lower is "
        "better). **ece**: test-set expected calibration error (temperature-scaled).",
    ]
    if notes:
        lines += ["", "### Run notes", notes]
    lines.append("")
    path.write_text("\n".join(lines))


def _parse_existing_rows(path: Path) -> dict:
    """Parse both the classification and regression tables back into row dicts,
    tagging each with its ``task`` by which header's column count it matches."""
    rows: dict[tuple, dict] = {}
    if not path.exists():
        return rows
    headers = {len(RESULTS_HEADER): (RESULTS_HEADER, "graph-classification"),
               len(REGRESSION_HEADER): (REGRESSION_HEADER, "graph-regression")}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        spec = headers.get(len(cells))
        if spec is None or cells[0] in ("dataset", "---"):
            continue
        header, task = spec
        row = dict(zip(header, cells))
        row["task"] = task
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
