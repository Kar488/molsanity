"""Parse the committed RESULTS.md into tidy records. Single source of truth for
every number in the paper — no value is retyped by hand anywhere else."""
from __future__ import annotations
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

def _rows(md_text, header_key):
    """Return list of dicts for the markdown table whose header contains header_key."""
    lines = md_text.splitlines()
    out, hdr = [], None
    for ln in lines:
        if not ln.startswith("|"):
            hdr = None
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if set("".join(cells)) <= set("- "):      # separator row
            continue
        if hdr is None:
            if header_key in cells:
                hdr = cells
            continue
        if len(cells) != len(hdr):
            continue
        out.append(dict(zip(hdr, cells)))
    return out

def _num(v):
    if v in {"—", "-", "", "nan", "NaN"}:
        return float("nan")
    try:
        return float(v)
    except ValueError:
        return float("nan")

def load(results_md: Path | None = None):
    p = results_md or (REPO / "RESULTS.md")
    txt = p.read_text()
    cls_txt, reg_txt = txt.split("## Regression audit matrix")
    cls = _rows(cls_txt, "gt_auroc")
    reg = _rows(reg_txt, "rmse")
    recs = []
    for r in cls:
        recs.append(dict(
            dataset=r["dataset"], backbone=r["backbone"], attributor=r["attributor"],
            split=r["split"], task="classification", n_mol=int(_num(r["n_mol"])),
            acc=_num(r["acc"]), auc=_num(r["auc"]),
            gt_auroc=_num(r["gt_auroc"]), gt_auprc=_num(r["gt_auprc"]),
            motif_top1=_num(r["motif_top1"]), occ_spearman=_num(r["occ_spearman"]),
            occ_top1=_num(r["occ_top1"]), fid_plus=_num(r["fid+"]),
            fid_minus=_num(r["fid-"]), sparsity=_num(r["sparsity"]), ece=_num(r["ece"]),
            rmse=float("nan"), mae=float("nan"), r2=float("nan"),
        ))
    for r in reg:
        recs.append(dict(
            dataset=r["dataset"], backbone=r["backbone"], attributor=r["attributor"],
            split=r["split"], task="regression", n_mol=int(_num(r["n_mol"])),
            acc=float("nan"), auc=float("nan"),
            gt_auroc=float("nan"), gt_auprc=float("nan"),
            motif_top1=_num(r["motif_top1"]), occ_spearman=_num(r["occ_spearman"]),
            occ_top1=_num(r["occ_top1"]), fid_plus=_num(r["fid+"]),
            fid_minus=_num(r["fid-"]), sparsity=_num(r["sparsity"]), ece=float("nan"),
            rmse=_num(r["rmse"]), mae=_num(r["mae"]), r2=_num(r["r2"]),
        ))
    return recs

# Regime grouping used for colour in the scatter.
EXACT_GT = {"SynthMotifs", "SynthMotifsXL"}
PROXY_GT = {"MUTAG"}

def regime(rec):
    if rec["dataset"] in EXACT_GT:
        return "synthetic (exact GT)"
    if rec["task"] == "regression":
        return "regression"
    return "classification"

if __name__ == "__main__":
    import collections
    R = load()
    print(f"total rows: {len(R)}")
    print(f"  classification: {sum(1 for r in R if r['task']=='classification')}")
    print(f"  regression:     {sum(1 for r in R if r['task']=='regression')}")
    ds = sorted({r['dataset'] for r in R}); bb = sorted({r['backbone'] for r in R})
    at = sorted({r['attributor'] for r in R}); sp = sorted({r['split'] for r in R})
    print(f"datasets ({len(ds)}): {ds}")
    print(f"backbones ({len(bb)}): {bb}")
    print(f"attributors ({len(at)}): {at}")
    print(f"splits ({len(sp)}): {sp}")
    print(f"unique cells: {len({(r['dataset'],r['backbone'],r['attributor'],r['split']) for r in R})}")
    print(f"rows with ground truth (gt_auroc defined): {sum(1 for r in R if r['gt_auroc']==r['gt_auroc'])}")
    print("\nGT datasets:", sorted({r['dataset'] for r in R if r['gt_auroc']==r['gt_auroc']}))
