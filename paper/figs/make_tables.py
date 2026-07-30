"""Emit the paper's LaTeX tables directly from the committed results.

Run: ``python paper/figs/make_tables.py``. Writes .tex fragments that body.tex
\\input{}s, so no number in the paper is ever transcribed by hand.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from load_results import REPO, load  # noqa: E402

OUT = Path(__file__).parent
SHORT = {
    "IntegratedGradients": "Integrated Grad.", "InputXGradient": "Input$\\times$Grad.",
    "GuidedBackprop": "Guided BP", "GNNExplainer": "GNNExplainer",
    "PGExplainer": "PGExplainer", "Saliency": "Saliency",
}
# Single-column tables must fit 3.4in: tighten inter-column padding.
TIGHT = r"\setlength{\tabcolsep}{3.6pt}"


def f(v, nd=3):
    if v is None or v != v:
        return "--"
    return f"{v:.{nd}f}"


def write(name, lines):
    p = OUT / f"{name}.tex"
    p.write_text("\n".join(lines) + "\n")
    print(f"  wrote {p.name}")


# ---------------------------------------------------------------- Table 1 --
def table_headline(R):
    """MUTAG x GINE x scaffold: the faithful-but-wrong case, all six attributors."""
    rows = sorted([r for r in R if r["dataset"] == "MUTAG" and r["backbone"] == "GINE"
                   and r["split"] == "scaffold"], key=lambda r: -r["gt_auroc"])
    L = [TIGHT, r"\begin{tabular}{lrrrrr}", r"\toprule",
         r"Attributor & GT AUROC & Occ.\ $\rho$ & Fid$+$ & Fid$-$ & Motif top1 \\",
         r"\midrule"]
    for r in rows:
        L.append(f"{SHORT[r['attributor']]} & {f(r['gt_auroc'])} & {f(r['occ_spearman'])} & "
                 f"{f(r['fid_plus'])} & {f(r['fid_minus'])} & {f(r['motif_top1'])} \\\\")
    L += [r"\bottomrule", r"\end{tabular}"]
    write("tab_headline", L)
    return rows


# ---------------------------------------------------------------- Table 2 --
def table_exact_gt(R):
    """SynthMotifsXL x GINE x random: the well-powered exact-GT control."""
    rows = sorted([r for r in R if r["dataset"] == "SynthMotifsXL"],
                  key=lambda r: -r["gt_auroc"])
    L = [TIGHT, r"\begin{tabular}{lrrrr}", r"\toprule",
         r"Attributor & GT AUROC & GT AUPRC & Occ.\ $\rho$ & Fid$+$ \\",
         r"\midrule"]
    for r in rows:
        L.append(f"{SHORT[r['attributor']]} & {f(r['gt_auroc'])} & {f(r['gt_auprc'])} & "
                 f"{f(r['occ_spearman'])} & {f(r['fid_plus'])} \\\\")
    L += [r"\bottomrule", r"\end{tabular}"]
    write("tab_exact_gt", L)


# ---------------------------------------------------------------- Table 3 --
def table_backbones(R):
    """Backbone ordering on exact GT, with task performance alongside."""
    rows = sorted([r for r in R if r["dataset"] == "SynthMotifs"
                   and r["attributor"] == "IntegratedGradients"
                   and r["split"] == "scaffold"], key=lambda r: -r["gt_auroc"])
    L = [TIGHT, r"\begin{tabular}{lrrrr}", r"\toprule",
         r"Backbone & GT AUROC & Occ.\ $\rho$ & Test acc.\ & Test AUC \\",
         r"\midrule"]
    for r in rows:
        L.append(f"{r['backbone']} & {f(r['gt_auroc'])} & {f(r['occ_spearman'])} & "
                 f"{f(r['acc'], 2)} & {f(r['auc'], 2)} \\\\")
    L += [r"\bottomrule", r"\end{tabular}"]
    write("tab_backbones", L)


# ---------------------------------------------------------------- Table 4 --
def table_grid(R):
    """Dataset inventory: what was audited, with the honest GT status."""
    GT = {"SynthMotifs": "exact", "SynthMotifsXL": "exact", "MUTAG": "proxy"}
    TASK = {}
    for r in R:
        TASK[r["dataset"]] = "reg." if r["task"] == "regression" else "clf."
    order = ["SynthMotifs", "SynthMotifsXL", "MUTAG", "BBBP", "BACE", "ClinTox",
             "SIDER", "Tox21", "DILI", "hERG", "ESOL", "FreeSolv", "Lipophilicity"]
    L = [TIGHT, r"\begin{tabular}{llrrl}", r"\toprule",
         r"Dataset & Task & Cells & $n_{\mathrm{mol}}$ & Node ground truth \\",
         r"\midrule"]
    for d in order:
        sub = [r for r in R if r["dataset"] == d]
        if not sub:
            continue
        nmol = sorted({r["n_mol"] for r in sub})
        L.append(f"{d} & {TASK[d]} & {len(sub)} & "
                 f"{'/'.join(str(n) for n in nmol)} & {GT.get(d, 'none')} \\\\")
    L += [r"\midrule",
          f"\\textbf{{Total}} & & \\textbf{{{len(R)}}} & & \\\\",
          r"\bottomrule", r"\end{tabular}"]
    write("tab_grid", L)


# ---------------------------------------------------------------- Table 5 --
def table_selection():
    """The two-regime selection test straight out of BENCHMARK_GT.json."""
    data = json.loads((REPO / "BENCHMARK_GT.json").read_text())
    NICE = {"occ_spearman": r"Occlusion $\rho$ (ours)",
            "fidelity_plus": r"Fidelity$+$",
            "characterization": r"Characterisation"}
    ABBR = {"IntegratedGradients": "IG", "Saliency": "Saliency",
            "InputXGradient": "Input$\\times$Grad", "GuidedBackprop": "GuidedBP",
            "GNNExplainer": "GNNExpl", "PGExplainer": "PGExpl"}
    L = [r"\begin{tabular}{llrrll}", r"\toprule",
         r"Regime & Selector & $\rho_{\mathrm{rank}}$ & $p$ & Top pick (GT AUROC) & "
         r"Mis-selection \\", r"\midrule"]
    for res in data:
        if "error" in res:
            continue
        n = list(res["per_attributor"].values())[0]["n_mol"]
        lab = ("in-distribution" if res["split"] == "random" else "scaffold shift")
        first = True
        for s in res["selections"]:
            m = s["faithfulness_metric"]
            rc = res["rank_correlation"][m]
            head = (f"{lab} ({res['dataset']}, $n=${n})" if first else "")
            first = False
            pick = f"{ABBR[s['faithfulness_pick']]} ({s['faithfulness_pick_gt_auroc']:.3f})"
            if s["mismatch"]:
                pv = s["paired_gt_pvalue"]
                mis = ("\\textbf{yes}, $p<0.001$" if pv is not None and pv < 1e-3
                       else f"yes, $p={pv:.3f}$")
            else:
                mis = "no"
            L.append(f"{head} & {NICE[m]} & {rc['rho']:+.2f} & {rc['pvalue']:.3f} & "
                     f"{pick} & {mis} \\\\")
        L.append(r"\addlinespace")
    L = L[:-1] + [r"\bottomrule", r"\end{tabular}"]
    write("tab_selection", L)


# --------------------------------------------------------------- numbers ---
def key_numbers(R):
    """Every scalar quoted in the prose, computed here and \\input as macros."""
    from scipy.stats import spearmanr

    gt = [r for r in R if r["gt_auroc"] == r["gt_auroc"]
          and r["occ_spearman"] == r["occ_spearman"]]
    rho, p = spearmanr([r["occ_spearman"] for r in gt], [r["gt_auroc"] for r in gt])
    mut = [r for r in R if r["dataset"] == "MUTAG" and r["backbone"] == "GINE"
           and r["split"] == "scaffold"]
    grad = [r for r in mut if r["attributor"] in
            {"Saliency", "InputXGradient", "GuidedBackprop", "IntegratedGradients"}]
    go = [r["occ_spearman"] for r in grad]
    gg = [r["gt_auroc"] for r in grad]
    reg = [r["occ_spearman"] for r in R if r["task"] == "regression"
           and r["occ_spearman"] == r["occ_spearman"]]
    clf = [r["occ_spearman"] for r in R if r["task"] == "classification"
           and not r["dataset"].startswith("SynthMotifs")
           and r["occ_spearman"] == r["occ_spearman"]]
    m = {
        "NCells": len(R),
        "NCls": sum(1 for r in R if r["task"] == "classification"),
        "NReg": sum(1 for r in R if r["task"] == "regression"),
        "NData": len({r["dataset"] for r in R}),
        "NBack": len({r["backbone"] for r in R}),
        "NAttr": len({r["attributor"] for r in R}),
        "NGtCells": len(gt),
        "GlobalRho": f"{rho:+.2f}", "GlobalP": f"{p:.2f}",
        "GradOccLo": f"{min(go):.3f}", "GradOccHi": f"{max(go):.3f}",
        "GradOccSpread": f"{max(go) - min(go):.3f}",
        "GradGtLo": f"{min(gg):.3f}", "GradGtHi": f"{max(gg):.3f}",
        "GradGtSpread": f"{max(gg) - min(gg):.3f}",
        "RegNeg": sum(1 for v in reg if v < 0), "RegN": len(reg),
        "RegMean": f"{np.mean(reg):+.2f}",
        "ClfNeg": sum(1 for v in clf if v < 0), "ClfN": len(clf),
        "ClfMean": f"{np.mean(clf):+.2f}",
        # Distinct trained models (exclude the *_early intermediates).
        "NCkpt": len([q for q in (REPO / "artifacts" / "checkpoints").rglob("*.pt")
                      if not q.stem.endswith("_early")]),
    }
    L = [f"\\newcommand{{\\num{k}}}{{{v}}}" for k, v in m.items()]
    write("numbers", L)
    for k, v in m.items():
        print(f"    {k} = {v}")


def main():
    R = load()
    print(f"loaded {len(R)} rows")
    table_headline(R)
    table_exact_gt(R)
    table_backbones(R)
    table_grid(R)
    table_selection()
    key_numbers(R)


if __name__ == "__main__":
    main()
