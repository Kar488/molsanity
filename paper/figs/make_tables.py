"""Generate every LaTeX table and every inline number used in the manuscript.

    python paper/figs/make_tables.py

Writes into paper/generated/:
  macros.tex        \\newcommand for every number quoted in the prose
  tab_*.tex         booktabs tables

Nothing is hand-typed: values come from the committed ``results/`` folder via
``msdata`` — the audit matrices, the run ledger, and the per-molecule records
under ``results/artifacts/audit/``. Re-run after a new run lands.
"""
from __future__ import annotations

import math
import statistics as st
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import msdata as D  # noqa: E402

OUT = HERE.parent / "generated"
OUT.mkdir(exist_ok=True)

CLS, REG = D.load_results()
BENCH = D.load_benchmark()
RECS = D.load_records()
COV = D.coverage()
MAN = D.load_manifest()

SHORT = {"IntegratedGradients": "IG", "Saliency": "Saliency",
         "InputXGradient": "Input$\\times$Grad", "GuidedBackprop": "GuidedBP",
         "GNNExplainer": "GNNExpl.", "PGExplainer": "PGExpl."}
ESC = {"&": "\\&", "%": "\\%", "_": "\\_", "#": "\\#"}
ATTR_ORDER = ["IntegratedGradients", "Saliency", "InputXGradient",
              "GuidedBackprop", "GNNExplainer", "PGExplainer"]
# Cell families with a node-level ground truth, the full attributor set, and
# BOTH splits — i.e. within-dataset in-distribution vs. scaffold-shift
# contrasts, where only the split changes. MUTAG is the molecular one (proxy
# ground truth) and leads; SynthMotifs carries exact ground truth.
ARMS = [("MUTAG", "GINE", "mut"), ("SynthMotifs", "GINE", "syn")]
ARM = ARMS[0][:2]


def tex(s: str) -> str:
    for k, v in ESC.items():
        s = s.replace(k, v)
    return s


def n(v, nd=3, dash="---"):
    """Table number; negatives get a real minus sign."""
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return dash
    s = f"{v:.{nd}f}"
    return "$-$" + s[1:] if s.startswith("-") else s


def pfmt(p, dash="---"):
    if p is None or (isinstance(p, float) and math.isnan(p)):
        return dash
    return "$<$0.001" if p < 0.001 else f"{p:.3f}"


def bold(s, on=True):
    return f"\\textbf{{{s}}}" if on else s


BIDX = {D.cell_key(r): r for r in BENCH}


def bench_of(r):
    return BIDX.get(D.cell_key(r), {})


def prov_mark(r):
    return "" if r["provenance"] == "current" else "\\,\\textsuperscript{c}"


def write(name, body):
    (OUT / name).write_text(body)
    print(f"  wrote {OUT / name}")


def cell_row(ds, bb, at, sp):
    for r in CLS:
        if D.cell_key(r) == (ds, bb, at, sp):
            return r
    return None


# ------------------------------------------------------------------ macros
def macros():
    m = []

    def num(v, nd=3):
        """Macro-safe number (negatives typeset correctly in text or math)."""
        if v is None or (isinstance(v, float) and math.isnan(v)):
            return "---"
        s = f"{v:.{nd}f}"
        return "\\ensuremath{" + s + "}" if s.startswith("-") else s

    def add(cmd, val):
        m.append(f"\\newcommand{{\\{cmd}}}{{{val}}}")

    # --- run provenance ----------------------------------------------------
    add("runConfig", tex(MAN["config_name"]))
    add("runStamp", MAN["timestamp"].replace("_", "-"))
    add("runSeed", MAN["seed"])
    add("runTorch", MAN["versions"]["torch"])
    add("runPyG", MAN["versions"]["torch_geometric"])
    add("runRDKit", MAN["versions"]["rdkit"])
    add("runCaptum", MAN["versions"]["captum"])
    add("runGitRev", MAN["git_rev"][:7])

    led = COV["ledger"]
    add("nDone", led["done"])
    add("nFailed", led["failed"])
    add("nSkipped", led["skipped"])
    add("nAttempted", sum(led.values()))
    add("nPlanned", COV["n_planned"])
    add("nCurrentInPlan", COV["n_current_in_plan"])
    add("nCarried", COV["n_carried"])
    add("nRecordCells", len(RECS))
    add("nRecords", sum(len(v) for v in RECS.values()))
    add("nClsRows", len(CLS))
    add("nRegRows", len(REG))
    add("nRowsTotal", len(CLS) + len(REG))
    add("nDatasetsCurrent", len(COV["datasets_current"]))
    add("nBackbonesCurrent", len(COV["backbones_current"]))
    add("nAttributorsCurrent", len(COV["attributors_current"]))
    add("nDatasetsAll", len({r["dataset"] for r in list(CLS) + list(REG)}))
    add("nAttributorsAll", len({r["attributor"] for r in list(CLS) + list(REG)}))

    fails = D.failure_reasons()
    for msg, cells in fails.items():
        if "numpy" in msg:
            add("nFailCudaNumpy", len(cells))
        elif "same device" in msg:
            add("nFailDeviceMismatch", len(cells))
        elif "more than 1 value per channel" in msg:
            add("nFailBatchNorm", len(cells))
        elif "NoneType" in msg:
            add("nFailNoneType", len(cells))
    add("nFailReasons", len(fails))
    mutag_failed = sum(1 for e in D.load_ledger()
                       if e["dataset"] == "MUTAG" and e["status"] == "failed")
    add("nMutagFailed", mutag_failed)

    # --- ground-truth cells -------------------------------------------------
    gt_cells = [r for r in CLS if r["gt_auroc"] is not None
                and r["occ_spearman"] is not None]
    add("nGtCells", len(gt_cells))
    add("nGtCurrent", sum(1 for r in gt_cells if r["provenance"] == "current"))
    fbw = [r for r in gt_cells if r["occ_spearman"] > 0 and r["gt_auroc"] < 0.5]
    add("nFaithfulButWrong", len(fbw))
    add("nAntiAligned", sum(1 for r in gt_cells if r["gt_auroc"] < 0.5))
    add("nNoGtCells", sum(1 for r in list(CLS) + list(REG)
                          if r.get("gt_auroc") is None))

    # --- the within-dataset shift contrasts (only the split changes) --------
    tags = {"IntegratedGradients": "IG", "Saliency": "Sal",
            "InputXGradient": "IxG", "GuidedBackprop": "GBP",
            "GNNExplainer": "GNNE", "PGExplainer": "PGE"}
    add("nArms", len(ARMS))
    for ds, bb, arm in ARMS:
        add(f"{arm}Dataset", ds)
        add(f"{arm}Backbone", bb)
        for sp, half in (("random", "Ind"), ("scaffold", "Shift")):
            sel = D.selection_test(ds, bb, sp)
            if sel is None:
                continue
            pre = arm + half
            pa = sel["per_attributor"]
            add(f"{pre}NAttr", len(sel["attributors"]))
            add(f"{pre}NMol", max(v["n_mol"] for v in pa.values()))
            add(f"{pre}GtBest", SHORT.get(sel["gt_best"], sel["gt_best"]))
            add(f"{pre}GtBestVal", num(pa[sel["gt_best"]]["gt_auroc_mean"]))
            add(f"{pre}GtWorstVal", num(min(v["gt_auroc_mean"] for v in pa.values())))
            add(f"{pre}NMismatch", sum(1 for x in sel["selections"] if x["mismatch"]))
            add(f"{pre}NMetrics", len(sel["selections"]))
            for a, v in pa.items():
                add(f"{pre}{tags[a]}Gt", num(v["gt_auroc_mean"]))
                add(f"{pre}{tags[a]}Occ", num(v["occ_spearman"]))
            for x in sel["selections"]:
                t = x["faithfulness_metric"].replace("_", "").capitalize()
                add(f"{pre}Pick{t}", SHORT.get(x["faithfulness_pick"],
                                               x["faithfulness_pick"]))
                add(f"{pre}PickGt{t}", num(x["faithfulness_pick_gt_auroc"]))
                if x["paired_gt_pvalue"] is not None:
                    pv = x["paired_gt_pvalue"]
                    add(f"{pre}P{t}",
                        "\\ensuremath{<}0.001" if pv < 0.001 else f"{pv:.3f}")
                    add(f"{pre}Gap{t}", num(x["paired_gt_gap_median"]))
                    add(f"{pre}NPaired{t}", x["n_paired"])
            for k, v in sel["rank_correlation"].items():
                add(f"{pre}Rho{k.replace('_', '').capitalize()}", num(v["rho"]))
        # does the attributor GT ordering survive the change of split?
        A = {a: D.cell_mean(RECS[(ds, bb, a, "random")], "gt_auroc")
             for a in ATTR_ORDER if (ds, bb, a, "random") in RECS}
        B = {a: D.cell_mean(RECS[(ds, bb, a, "scaffold")], "gt_auroc")
             for a in ATTR_ORDER if (ds, bb, a, "scaffold") in RECS}
        shared = [a for a in sorted(set(A) & set(B))
                  if not math.isnan(A[a]) and not math.isnan(B[a])]
        rho, _ = D.spearman([A[a] for a in shared], [B[a] for a in shared])
        add(f"{arm}AttrRankRho", num(rho))
        add(f"{arm}AttrRankN", len(shared))

    # --- degenerate cells among the ground-truth arms ----------------------
    degen = []
    for (dsx, bbx, atx, spx), recs in RECS.items():
        vals = [r["gt_auroc"] for r in recs
                if r.get("gt_auroc") is not None and not math.isnan(r["gt_auroc"])]
        if len(vals) >= 10 and len(set(round(v, 6) for v in vals)) == 1:
            degen.append(((dsx, bbx, atx, spx), vals[0], len(vals)))
    add("nDegenerateGtCells", len(degen))
    if degen:
        (k, v, nmol) = degen[0]
        add("degenCell", tex(k[0]) + "$\\cdot$" + k[1] + "$\\cdot$"
            + SHORT.get(k[2], k[2]) + ", " + k[3])
        add("degenVal", num(v))
        add("degenN", nmol)

    # attributor GT ordering: does it survive the change of split?
    def gt_by_attr(sp):
        out = {}
        for a in ATTR_ORDER:
            recs = RECS.get((ds, bb, a, sp))
            if recs:
                v = D.cell_mean(recs, "gt_auroc")
                if not math.isnan(v):
                    out[a] = v
        return out
    A, B = gt_by_attr("random"), gt_by_attr("scaffold")
    shared = sorted(set(A) & set(B))
    rho, _ = D.spearman([A[k] for k in shared], [B[k] for k in shared])
    add("armAttrRankRho", num(rho))
    add("armAttrRankN", len(shared))

    # --- MUTAG (carried from the earlier reduced-budget run) ---------------
    for at, tag in [("Saliency", "Sal"), ("InputXGradient", "IxG"),
                    ("IntegratedGradients", "IG"), ("GNNExplainer", "GNNE"),
                    ("GuidedBackprop", "GBP"), ("PGExplainer", "PGE")]:
        r = cell_row("MUTAG", "GINE", at, "scaffold")
        if r:
            add(f"mutag{tag}Gt", num(r["gt_auroc"]))
            add(f"mutag{tag}Occ", num(r["occ_spearman"]))
    grad = [cell_row("MUTAG", "GINE", a, "scaffold")["occ_spearman"]
            for a in ("Saliency", "InputXGradient", "IntegratedGradients")
            if cell_row("MUTAG", "GINE", a, "scaffold")]
    if len(grad) > 1:
        add("mutagGradOccSpread", num(max(grad) - min(grad)))

    # --- backbone sweeps at IG, both splits, on the exact-GT dataset -------
    bb_ds = "SynthMotifs"
    add("bbDataset", bb_ds)
    for sp, pre in (("scaffold", "bbShift"), ("random", "bbInd")):
        rows = [r for r in CLS if r["dataset"] == bb_ds and r["split"] == sp
                and r["attributor"] == "IntegratedGradients"
                and r["gt_auroc"] is not None]
        for r in rows:
            add(f"{pre}{r['backbone']}", num(r["gt_auroc"]))
        if rows:
            best = max(rows, key=lambda r: r["gt_auroc"])
            worst = min(rows, key=lambda r: r["gt_auroc"])
            add(f"{pre}Best", best["backbone"])
            add(f"{pre}BestVal", num(best["gt_auroc"]))
            add(f"{pre}Worst", worst["backbone"])
            add(f"{pre}WorstVal", num(worst["gt_auroc"]))
            add(f"{pre}Spread", num(best["gt_auroc"] - worst["gt_auroc"]))
            add(f"{pre}N", len(rows))
    Ab = {r["backbone"]: r["gt_auroc"] for r in CLS
          if r["dataset"] == bb_ds and r["split"] == "random"
          and r["attributor"] == "IntegratedGradients" and r["gt_auroc"] is not None}
    Bb = {r["backbone"]: r["gt_auroc"] for r in CLS
          if r["dataset"] == bb_ds and r["split"] == "scaffold"
          and r["attributor"] == "IntegratedGradients" and r["gt_auroc"] is not None}
    sh = sorted(set(Ab) & set(Bb))
    rho, _ = D.spearman([Ab[k] for k in sh], [Bb[k] for k in sh])
    add("bbRankRho", num(rho))
    add("bbRankN", len(sh))

    # --- regression --------------------------------------------------------
    rvals = [r for r in REG if r["occ_spearman"] is not None]
    neg = [r for r in rvals if r["occ_spearman"] < 0]
    pos = [r for r in rvals if r["occ_spearman"] >= 0]
    add("nRegCells", len(rvals))
    add("nRegNeg", len(neg))
    add("nRegPos", len(pos))
    add("medRegOcc", num(st.median([r["occ_spearman"] for r in rvals])))
    add("regPosCells", ", ".join(sorted({f"{tex(r['dataset'])}$\\cdot${r['backbone']}"
                                         for r in pos})))
    fidmax = max((r["fid+"] for r in REG if r["fid+"] is not None), default=None)
    add("maxRegFidPlus", num(fidmax, 2))

    # --- regimes (pooled over all cells with records) ----------------------
    pooled: dict[str, list] = {}
    for recs in RECS.values():
        for r in recs:
            pooled.setdefault(r.get("regime", "?"), []).append(r)
    for reg, tag in (("confident_correct", "CC"), ("confident_error", "CE"),
                     ("borderline", "BL")):
        sub = pooled.get(reg, [])
        add(f"nReg{tag}", len(sub))
        for f, ftag in (("occ_spearman", "Occ"), ("gt_auroc", "Gt"),
                        ("stability", "Stab")):
            vals = [r[f] for r in sub
                    if r.get(f) is not None and not math.isnan(r[f])]
            add(f"reg{tag}{ftag}", num(st.mean(vals)) if vals else "---")
            add(f"nReg{tag}{ftag}", len(vals))
    add("nRegimeMol", sum(len(v) for v in pooled.values()))

    # --- calibration linkage, per cell (pooling is a Simpson trap) ---------
    links = []
    for k, recs in RECS.items():
        if D.regime_of(k[0]) == "regression":
            continue
        cl = D.calibration_linkage(recs)
        if not math.isnan(cl["spearman"]):
            links.append(cl)
    add("nCalibCells", len(links))
    add("medCalibRho", num(st.median([c["spearman"] for c in links])))
    add("nCalibSigPos", sum(1 for c in links if c["spearman"] > 0 and c["pvalue"] < 0.05))
    add("nCalibSigNeg", sum(1 for c in links if c["spearman"] < 0 and c["pvalue"] < 0.05))
    add("nCalibPos", sum(1 for c in links if c["spearman"] > 0))
    allrec = [r for k, v in RECS.items() if D.regime_of(k[0]) != "regression"
              for r in v]
    add("pooledCalibRho", num(D.calibration_linkage(allrec)["spearman"]))

    # --- stability ---------------------------------------------------------
    stab = [r["stability"] for r in BENCH if r["stability"] is not None]
    add("medStability", num(st.median(stab)))
    add("minStability", num(min(stab)))
    add("nStabilityCells", len(stab))
    for at, tag in [("IntegratedGradients", "IG"), ("Saliency", "Sal"),
                    ("InputXGradient", "IxG"), ("GuidedBackprop", "GBP"),
                    ("GNNExplainer", "GNNE"), ("PGExplainer", "PGE")]:
        vals = [r["stability"] for r in BENCH
                if r["attributor"] == at and r["stability"] is not None]
        if vals:
            add(f"stab{tag}", num(st.median(vals)))
            add(f"nStab{tag}", len(vals))

    # --- coherence + fit quoted in the prose -------------------------------
    mol = [r for r in list(CLS) + list(REG)
           if r["dataset"] not in D.SYNTHETIC and r["motif_top1"] is not None]
    vals = [r["motif_top1"] for r in mol]
    add("motifTopMin", num(min(vals)))
    add("motifTopMax", num(max(vals)))
    add("nMolecularCells", len(vals))
    add("nMotifInBand", sum(1 for v in vals if 0.6 <= v <= 0.9))
    esol = [r for r in REG if r["dataset"] == "ESOL" and r["r2"] is not None]
    if esol:
        add("esolRtwoMin", num(min(r["r2"] for r in esol)))
        add("esolRtwoMax", num(max(r["r2"] for r in esol)))

    # --- honest negatives: exemplar cells, chosen by the data --------------
    mol_cur = [r for r in CLS if r["provenance"] == "current"
               and r["dataset"] not in D.SYNTHETIC
               and r["auc"] is not None and r["occ_spearman"] is not None]

    def exemplar(pre, r):
        add(pre + "Dataset", tex(r["dataset"]))
        add(pre + "Backbone", r["backbone"])
        add(pre + "Split", r["split"])
        add(pre + "Acc", num(r["acc"]))
        add(pre + "Auc", num(r["auc"]))
        add(pre + "Occ", num(r["occ_spearman"]))
        add(pre + "Ece", num(r["ece"]))

    exemplar("bestAuc", max(mol_cur, key=lambda r: r["auc"]))
    exemplar("mostFaithful", max(mol_cur, key=lambda r: r["occ_spearman"]))
    exemplar("mostAnti", min(mol_cur, key=lambda r: r["occ_spearman"]))
    worst = min(mol_cur, key=lambda r: r["auc"])
    exemplar("worstAuc", worst)
    hi = [r for r in CLS if r["acc"] is not None and r["acc"] >= 0.95
          and r["auc"] is not None]
    add("nHighAccRows", len(hi))
    add("minHighAccAuc", num(min(r["auc"] for r in hi)))
    tox = [r for r in CLS if r["dataset"] == "Tox21" and r["auc"] is not None]
    if tox:
        add("nToxRows", len(tox))
        add("toxAccMin", num(min(r["acc"] for r in tox)))
        add("toxAccMax", num(max(r["acc"] for r in tox)))
        add("toxAucMin", num(min(r["auc"] for r in tox)))
        add("toxAucMax", num(max(r["auc"] for r in tox)))
    eces = [r["ece"] for r in CLS if r["ece"] is not None]
    add("maxEce", num(max(eces)))
    add("medEce", num(st.median(eces)))

    # --- split effect on faithfulness, paired within cell family ----------
    pairs = []
    for (dsx, bbx, atx, spx) in RECS:
        if spx != "scaffold":
            continue
        other = (dsx, bbx, atx, "random")
        if other in RECS:
            a = D.cell_mean(RECS[(dsx, bbx, atx, spx)], "occ_spearman")
            b = D.cell_mean(RECS[other], "occ_spearman")
            if not math.isnan(a) and not math.isnan(b):
                pairs.append((dsx, bbx, atx, a, b))
    add("nSplitPairs", len(pairs))
    add("nSplitOccDrop", sum(1 for p in pairs if p[3] < p[4]))
    add("medSplitOccDelta", num(st.median([p[3] - p[4] for p in pairs])))

    write("macros.tex", "\n".join(m) + "\n")


# ------------------------------------------------------------- tier-1 table
def tab_tier1():
    rows = [r for r in CLS if r["gt_auroc"] is not None]
    rows.sort(key=lambda r: (r["dataset"], r["split"], r["backbone"], r["attributor"]))
    blocks: dict[tuple, list] = {}
    for r in rows:
        blocks.setdefault((r["dataset"], r["split"]), []).append(r)
    best_gt = {id(max(v, key=lambda r: r["gt_auroc"]))
               for v in blocks.values() if len(v) > 1}
    best_occ = {id(max(v, key=lambda r: (r["occ_spearman"] is not None,
                                         r["occ_spearman"])))
                for v in blocks.values() if len(v) > 1}

    L = ["\\begin{table*}[t]", "\\centering",
         "\\caption{\\textbf{Every committed cell in which attribution "
         "\\emph{correctness} is measurable.} Ground truth is exact for the "
         "synthetic sets and a chemically motivated nitro-motif proxy for "
         "MUTAG. GT AUROC $=0.5$ is chance; below $0.5$ the attribution is "
         "anti-aligned with the true motif. Occlusion $\\rho$ is the "
         "attribution--occlusion rank agreement (higher $=$ more faithful to "
         "the model). Rows marked \\textsuperscript{c} are \\emph{carried}: "
         "they survive in the results matrix from an earlier reduced-budget "
         "CPU run because the corresponding cell failed in the latest run "
         "(Table~\\ref{tab:ledger}); every other row was produced by the run "
         "in Table~\\ref{tab:ledger}. Bold marks the best GT AUROC and the best "
         "occlusion $\\rho$ within each dataset$\\times$split block (emphasis "
         "only; values are unaltered).}",
         "\\label{tab:tier1}",
         "\\small",
         "\\renewcommand{\\arraystretch}{1.3}",
         "\\resizebox{\\textwidth}{!}{%",
         "\\begin{tabular}{lllcrrrrrrrrr}",
         "\\toprule",
         "\\textbf{dataset} & \\textbf{backbone} & \\textbf{attributor} & "
         "\\textbf{split} & \\textbf{$n$} & \\textbf{acc} & \\textbf{AUC} & "
         "\\textbf{GT AUROC} & \\textbf{GT AUPRC} & \\textbf{occ.\\ $\\rho$} & "
         "\\textbf{Fid+} & \\textbf{Fid--} & \\textbf{stab.} \\\\",
         "\\midrule"]
    prev = None
    for r in rows:
        b = bench_of(r)
        if prev is not None and (r["dataset"], r["split"]) != prev:
            L.append("\\addlinespace[2pt]")
        prev = (r["dataset"], r["split"])
        L.append(" & ".join([
            tex(r["dataset"]) + prov_mark(r), r["backbone"],
            SHORT.get(r["attributor"], r["attributor"]), r["split"],
            f"{int(r['n_mol'])}", n(r["acc"]), n(r["auc"]),
            bold(n(r["gt_auroc"]), id(r) in best_gt), n(r["gt_auprc"]),
            bold(n(r["occ_spearman"]), id(r) in best_occ),
            n(r["fid+"]), n(r["fid-"]), n(b.get("stability")),
        ]) + " \\\\")
    L += ["\\bottomrule", "\\end{tabular}}", "\\end{table*}"]
    write("tab_tier1.tex", "\n".join(L) + "\n")


# --------------------------------------------------------------- run ledger
def tab_ledger():
    led = D.load_ledger()
    per: dict[str, dict] = {}
    for e in led:
        d = per.setdefault(e["dataset"], {"done": 0, "failed": 0, "skipped": 0})
        d[e["status"]] = d.get(e["status"], 0) + 1
    carried: dict[str, int] = {}
    for k in COV["carried_cells"]:
        carried[k[0]] = carried.get(k[0], 0) + 1

    L = ["\\begin{table}[t]", "\\centering",
         "\\caption{\\textbf{The run ledger.} Outcome of every cell the "
         "\\texttt{" + tex(MAN["config_name"]) + "} sweep attempted, as recorded "
         "in \\texttt{results/PROGRESS.md}. \\emph{carried} counts cells whose "
         "row still appears in the results matrix from an earlier "
         "reduced-budget CPU run because this run's attempt failed --- those "
         "rows are marked \\textsuperscript{c} throughout this paper and are "
         "never mixed into a this-run aggregate.}",
         "\\label{tab:ledger}",
         "\\footnotesize",
         "\\renewcommand{\\arraystretch}{1.25}",
         "\\begin{tabular}{lrrrr}",
         "\\toprule",
         "\\textbf{dataset} & \\textbf{done} & \\textbf{failed} & "
         "\\textbf{skipped} & \\textbf{carried} \\\\",
         "\\midrule"]
    for ds in sorted(per):
        d = per[ds]
        L.append(f"{tex(ds)} & {d.get('done', 0)} & {d.get('failed', 0)} & "
                 f"{d.get('skipped', 0)} & {carried.get(ds, 0)} \\\\")
    t = COV["ledger"]
    L += ["\\midrule",
          f"\\textbf{{total}} & \\textbf{{{t['done']}}} & "
          f"\\textbf{{{t['failed']}}} & \\textbf{{{t['skipped']}}} & "
          f"\\textbf{{{COV['n_carried']}}} \\\\",
          "\\bottomrule", "\\end{tabular}"]
    reasons = sorted(D.failure_reasons().items(), key=lambda kv: -len(kv[1]))
    L.append("\\\\[4pt]\\raggedright\\footnotesize \\textbf{Failure reasons.} ")
    L.append("; ".join(f"{len(v)}~$\\times$ ``{tex(k[:66])}\\dots''"
                       for k, v in reasons) + ".")
    L.append("\\end{table}")
    write("tab_ledger.tex", "\n".join(L) + "\n")


# ------------------------------------------------------- selection experiment
def tab_selection():
    L = ["\\begin{table*}[t]", "\\centering",
         "\\caption{\\textbf{Does a faithfulness-only ranking pick the "
         "ground-truth-best attributor?} Two cell families, each audited on both "
         "splits with the same backbone and the same six attributors, so within "
         "a family only the split changes and the contrast isolates distribution "
         "shift rather than confounding it with a change of dataset. Each row "
         "ranks the attributors by one faithfulness/fidelity metric and asks "
         "whether its top choice is the one the ground truth ranks best. $p$ is a "
         "paired Wilcoxon test on per-molecule GT AUROC between the selected and "
         "the ground-truth-best attributor, over the molecules both audited.}",
         "\\label{tab:selection}",
         "\\small",
         "\\renewcommand{\\arraystretch}{1.3}",
         "\\resizebox{\\textwidth}{!}{%",
         "\\begin{tabular}{llllrlrcrr}",
         "\\toprule",
         "\\textbf{cell} & \\textbf{regime} & \\textbf{ranking metric} & "
         "\\textbf{its top pick} & \\textbf{pick GT} & \\textbf{GT-best} & "
         "\\textbf{GT-best} & \\textbf{mismatch} & \\textbf{Wilcoxon $p$} & "
         "\\textbf{$\\rho$(faith,GT)} \\\\",
         "\\midrule"]
    names = {"occ_spearman": "occlusion $\\rho$", "fidelity_plus": "Fidelity+",
             "characterization": "characterisation"}
    first = True
    for ds, bb, _arm in ARMS:
        for sp, label in (("random", "in-distribution"), ("scaffold", "scaffold shift")):
            sel = D.selection_test(ds, bb, sp)
            if sel is None:
                continue
            if not first:
                L.append("\\addlinespace[2pt]")
            first = False
            nmol = max(v["n_mol"] for v in sel["per_attributor"].values())
            cell = tex(ds) + "$\\cdot$" + bb + ", $n$=" + str(nmol)
            for si, x in enumerate(sel["selections"]):
                rho = sel["rank_correlation"][x["faithfulness_metric"]]["rho"]
                L.append(" & ".join([
                    cell if si == 0 else "", label if si == 0 else "",
                    names[x["faithfulness_metric"]],
                    SHORT.get(x["faithfulness_pick"], x["faithfulness_pick"]),
                    n(x["faithfulness_pick_gt_auroc"]),
                    SHORT.get(x["gt_best"], x["gt_best"]), n(x["gt_best_gt_auroc"]),
                    "\\textbf{yes}" if x["mismatch"] else "no",
                    pfmt(x["paired_gt_pvalue"]), n(rho),
                ]) + " \\\\")
    L += ["\\bottomrule", "\\end{tabular}}", "\\end{table*}"]
    write("tab_selection.tex", "\n".join(L) + "\n")


# ------------------------------------------------------------- paired stats
def tab_paired():
    ds, bb = ARM  # the molecular arm; the exact-GT arm is in the repository
    L = ["\\begin{table}[t]", "\\centering",
         "\\caption{\\textbf{Paired attributor comparisons on shared "
         "molecules}, computed from the committed per-molecule records "
         "(Wilcoxon signed-rank on per-molecule occlusion faithfulness, "
         "$\\Delta = A - B$). Same cell family as "
         "Table~\\ref{tab:selection}. $p$ values are unadjusted for "
         "multiplicity and should be read as descriptive at these sample "
         "sizes.}",
         "\\label{tab:paired}",
         "\\footnotesize",
         "\\renewcommand{\\arraystretch}{1.2}",
         "\\begin{tabular}{lrrr}",
         "\\toprule",
         "\\textbf{A vs.\\ B} & \\textbf{$n$} & \\textbf{median $\\Delta$} & "
         "\\textbf{$p$} \\\\",
         "\\midrule"]
    for bi, sp in enumerate(("random", "scaffold")):
        cells = D.attributor_cells(ds, bb, sp)
        attrs = [a for a in ATTR_ORDER if a in cells]
        if len(attrs) < 2:
            continue
        if bi:
            L.append("\\addlinespace[3pt]")
        L.append("\\multicolumn{4}{l}{\\itshape " + tex(ds) + ", " + bb + ", "
                 + sp + " split} \\\\")
        L.append("\\addlinespace[1pt]")
        for i, a in enumerate(attrs):
            for b in attrs[i + 1:]:
                A, B = D.by_graph(cells[a]), D.by_graph(cells[b])
                shared = sorted(set(A) & set(B))
                w = D.paired_wilcoxon([A[g]["occ_spearman"] for g in shared],
                                      [B[g]["occ_spearman"] for g in shared])
                L.append(" & ".join([
                    f"{SHORT.get(a, a)} vs.\\ {SHORT.get(b, b)}",
                    str(w["n"]), n(w["median_delta"]), pfmt(w["p"]),
                ]) + " \\\\")
    L += ["\\bottomrule", "\\end{tabular}", "\\end{table}"]
    write("tab_paired.tex", "\n".join(L) + "\n")


# ------------------------------------------------------------ regime table
def tab_regime():
    pooled: dict[str, list] = {}
    for recs in RECS.values():
        for r in recs:
            pooled.setdefault(r.get("regime", "?"), []).append(r)
    fields = [("occ_spearman", "occlusion $\\rho$"),
              ("gt_auroc", "GT AUROC"),
              ("stability", "stability")]
    L = ["\\begin{table}[t]", "\\centering",
         "\\caption{\\textbf{Reliability stratified by confidence/correctness "
         "regime}, pooled over the "
         + str(sum(len(v) for v in pooled.values()))
         + " per-molecule records this run committed. A molecule is "
         "\\emph{confident-correct} or \\emph{confident-error} when its "
         "temperature-scaled confidence is at least $0.8$, \\emph{borderline} "
         "otherwise. $n$ is given per metric because ground truth exists for "
         "only a minority of molecules --- in particular the confident-error "
         "GT mean rests on too few molecules to interpret, and is printed "
         "rather than hidden.}",
         "\\label{tab:regime}",
         "\\footnotesize",
         "\\renewcommand{\\arraystretch}{1.25}",
         "\\begin{tabular}{l" + "rr" * len(fields) + "}",
         "\\toprule",
         "\\textbf{regime} & "
         + " & ".join("\\multicolumn{2}{c}{\\textbf{" + lab + "}}"
                      for _, lab in fields) + " \\\\",
         " & " + " & ".join("\\textit{mean} & \\textit{n}" for _ in fields)
         + " \\\\",
         "\\midrule"]
    for reg in ("confident_correct", "confident_error", "borderline"):
        sub = pooled.get(reg, [])
        cells = []
        for f, _ in fields:
            vals = [r[f] for r in sub
                    if r.get(f) is not None and not math.isnan(r[f])]
            cells += [n(st.mean(vals)) if vals else "---", str(len(vals))]
        L.append(reg.replace("_", "-") + " & " + " & ".join(cells) + " \\\\")
    L += ["\\bottomrule", "\\end{tabular}", "\\end{table}"]
    write("tab_regime.tex", "\n".join(L) + "\n")


# --------------------------------------------------- molecular classification
def tab_molecular():
    rows = [r for r in CLS if r["gt_auroc"] is None]
    rows.sort(key=lambda r: (r["dataset"], r["backbone"], r["attributor"],
                             r["split"]))
    datasets = sorted({r["dataset"] for r in rows})
    half = len(rows) / 2
    cut, seen = len(datasets), 0
    for i, dsx in enumerate(datasets):
        seen += sum(1 for r in rows if r["dataset"] == dsx)
        if seen >= half:
            cut = i + 1
            break
    parts = [datasets]   # one reference table; two rotated pages read as a wall
    blocks: dict[str, list] = {}
    for r in rows:
        blocks.setdefault(r["dataset"], []).append(r)
    best_occ = {id(max(v, key=lambda r: (r["occ_spearman"] is not None,
                                         r["occ_spearman"])))
                for v in blocks.values() if len(v) > 1}
    head = ("\\textbf{Molecular classification cells (no node-level ground "
            "truth available)")
    tail = (".} Every committed classification cell on a real molecular "
            "dataset. The ground-truth localisation column does not exist for "
            "these datasets --- no per-atom labels are published --- so only "
            "model-side reliability can be measured, which is precisely the "
            "gap the Tier-1 cells are needed to close. \\emph{charact.} is the "
            "GraphFramEx characterisation score and \\emph{unfaith.} the "
            "PyG/DIG unfaithfulness metric, computed on the same molecules; "
            "both are blank for carried rows (\\textsuperscript{c}), whose "
            "per-molecule records this run did not regenerate. Bold marks the "
            "highest occlusion $\\rho$ per dataset (emphasis only).}")
    for pi, part in enumerate(parts):
        sub = [r for r in rows if r["dataset"] in part]
        suffix = "" if len(parts) == 1 else f", {pi + 1} of {len(parts)}"
        L = ["\\begin{sidewaystable*}[p]", "\\centering",
             "\\captionsetup{width=0.94\\textheight}",
             "\\caption{" + head + suffix + tail,
             "\\label{tab:molecular" + ("" if pi == 0 else chr(97 + pi)) + "}",
             "\\renewcommand{\\arraystretch}{1.3}",
             "\\resizebox{0.94\\textheight}{!}{%",
             "\\begin{tabular}{lllcrrrrrrrrrrrr}",
             "\\toprule",
             "\\textbf{dataset} & \\textbf{backbone} & \\textbf{attributor} & "
             "\\textbf{split} & \\textbf{$n$} & \\textbf{acc} & \\textbf{AUC} & "
             "\\textbf{ECE} & \\textbf{motif top-1} & \\textbf{occ.\\ $\\rho$} & "
             "\\textbf{occ.\\ top-1} & \\textbf{Fid+} & \\textbf{Fid--} & "
             "\\textbf{stab.} & \\textbf{charact.} & \\textbf{unfaith.} \\\\",
             "\\midrule"]
        prev = None
        for r in sub:
            b = bench_of(r)
            if prev is not None and r["dataset"] != prev:
                L.append("\\addlinespace[2pt]")
            prev = r["dataset"]
            L.append(" & ".join([
                tex(r["dataset"]) + prov_mark(r), r["backbone"],
                SHORT.get(r["attributor"], r["attributor"]), r["split"],
                f"{int(r['n_mol'])}", n(r["acc"]), n(r["auc"]), n(r["ece"]),
                n(r["motif_top1"]), bold(n(r["occ_spearman"]), id(r) in best_occ),
                n(r["occ_top1"]), n(r["fid+"]), n(r["fid-"]),
                n(b.get("stability")), n(b.get("characterization")),
                n(b.get("unfaithfulness")),
            ]) + " \\\\")
        L += ["\\bottomrule", "\\end{tabular}}", "\\end{sidewaystable*}"]
        name = "tab_molecular.tex" if len(parts) == 1 else f"tab_molecular_{pi + 1}.tex"
        write(name, "\n".join(L) + "\n")


# -------------------------------------------------------------- regression
def tab_regression():
    rows = sorted(REG, key=lambda r: (r["dataset"], r["backbone"],
                                      r["attributor"], r["split"]))
    vals = [r for r in REG if r["occ_spearman"] is not None]
    neg = [r for r in vals if r["occ_spearman"] < 0]
    pos = sorted({f"{tex(r['dataset'])}$\\cdot${r['backbone']}" for r in vals
                  if r["occ_spearman"] >= 0})
    L = ["\\begin{table*}[t]", "\\centering",
         "\\caption{\\textbf{Molecular regression cells.} Occlusion "
         "faithfulness is computed in output space (predicted-value shift) "
         "rather than probability space. In " + str(len(neg)) + " of the "
         + str(len(vals)) + " committed regression cells the "
         "attribution--occlusion agreement is \\emph{negative} --- the atoms an "
         "attributor ranks highest are not the atoms whose removal moves the "
         "prediction most --- while " + ", ".join(pos) + " run positive. Note "
         "the Fidelity$\\pm$ columns leave the $[-1,1]$ range a probability-space "
         "fidelity would occupy (up to " + n(max(r["fid+"] for r in REG
                                                 if r["fid+"] is not None), 2)
         + "), which is why we report but do not interpret their sign. Bold "
         "marks the highest occlusion $\\rho$ per dataset (emphasis only). "
         "PGExplainer is classification-only and therefore absent by "
         "construction.}",
         "\\label{tab:regression}",
         "\\small",
         "\\renewcommand{\\arraystretch}{1.3}",
         "\\resizebox{\\textwidth}{!}{%",
         "\\begin{tabular}{lllcrrrrrrrrr}",
         "\\toprule",
         "\\textbf{dataset} & \\textbf{backbone} & \\textbf{attributor} & "
         "\\textbf{split} & \\textbf{$n$} & \\textbf{RMSE} & \\textbf{MAE} & "
         "\\textbf{$R^2$} & \\textbf{motif top-1} & \\textbf{occ.\\ $\\rho$} & "
         "\\textbf{occ.\\ top-1} & \\textbf{Fid+} & \\textbf{stab.} \\\\",
         "\\midrule"]
    blocks: dict[str, list] = {}
    for r in rows:
        blocks.setdefault(r["dataset"], []).append(r)
    best = {id(max(v, key=lambda r: r["occ_spearman"]))
            for v in blocks.values() if len(v) > 1}
    prev = None
    for r in rows:
        b = bench_of(r)
        if prev is not None and r["dataset"] != prev:
            L.append("\\addlinespace[2pt]")
        prev = r["dataset"]
        L.append(" & ".join([
            tex(r["dataset"]) + prov_mark(r), r["backbone"],
            SHORT.get(r["attributor"], r["attributor"]), r["split"],
            f"{int(r['n_mol'])}", n(r["rmse"]), n(r["mae"]), n(r["r2"]),
            n(r["motif_top1"]), bold(n(r["occ_spearman"]), id(r) in best),
            n(r["occ_top1"]), n(r["fid+"], 2), n(b.get("stability")),
        ]) + " \\\\")
    L += ["\\bottomrule", "\\end{tabular}}", "\\end{table*}"]
    write("tab_regression.tex", "\n".join(L) + "\n")


# ------------------------------------------------------------- related work
def tab_related():
    txt = (D.REPO / "paper" / "RELATED_WORK.md").read_text()
    header, rows = None, []
    for h, rws in D._md_tables(txt):
        if "Capability" in h[0]:
            header, rows = h, rws
            break
    if header is None:
        raise KeyError("no capability matrix in RELATED_WORK.md")

    def mark(c):
        c = c.strip().replace("**", "")
        c = c.replace("✓", "\\ding{51}").replace("✗", "\\ding{55}")
        return tex(c.replace("~", "$\\sim$"))

    L = ["\\begin{table*}[t]", "\\centering",
         "\\caption{\\textbf{Where the audit sits relative to existing "
         "evaluation frameworks.} \\ding{51}~$=$ core capability, "
         "$\\sim$~$=$ partial or possible but not central, \\ding{55}~$=$ not a "
         "focus. The contribution is the combination, not any single row: "
         "ground-truth validation and faithfulness both exist elsewhere, but "
         "not jointly with cross-checkpoint stability, calibration linkage and "
         "shift stratification over a motif-native decomposition.}",
         "\\label{tab:related}",
         "\\small",
         "\\renewcommand{\\arraystretch}{1.3}",
         "\\resizebox{\\textwidth}{!}{%",
         "\\begin{tabular}{l" + "c" * (len(header) - 1) + "}",
         "\\toprule",
         " & ".join(f"\\textbf{{{tex(h.replace('**', ''))}}}" for h in header)
         + " \\\\", "\\midrule"]
    for r in rows:
        if len(r) != len(header):
            continue
        L.append(" & ".join([tex(r[0].replace("**", ""))]
                            + [mark(c) for c in r[1:]]) + " \\\\")
    L += ["\\bottomrule", "\\end{tabular}}", "\\end{table*}"]
    write("tab_related.tex", "\n".join(L) + "\n")


if __name__ == "__main__":
    print("Generating LaTeX tables and macros from results/ …")
    macros()
    tab_related()
    tab_ledger()
    tab_tier1()
    tab_selection()
    tab_paired()
    tab_regime()
    tab_molecular()
    tab_regression()
    print("done.")
