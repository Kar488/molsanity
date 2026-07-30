"""Generate every LaTeX table and every inline number used in the manuscript.

    python paper/figs/make_tables.py

Writes into paper/generated/:
  macros.tex        \\newcommand for every number quoted in the prose
  tab_*.tex         booktabs tables

Nothing is hand-typed: all values come from RESULTS.md / BENCHMARK.md /
BENCHMARK_GT.json via ``msdata``. Re-run after new grid cells land.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import msdata as D  # noqa: E402

OUT = HERE.parent / "generated"
OUT.mkdir(exist_ok=True)

CLS, REG = D.load_results()
BENCH = D.load_benchmark()
GTB = D.load_benchmark_gt()
PAIRED = D.load_paired()
COV = D.coverage()

SHORT = {"IntegratedGradients": "IG", "Saliency": "Saliency",
         "InputXGradient": "Input$\\times$Grad", "GuidedBackprop": "GuidedBP",
         "GNNExplainer": "GNNExpl.", "PGExplainer": "PGExpl."}
ESC = {"&": "\\&", "%": "\\%", "_": "\\_", "#": "\\#"}


def tex(s: str) -> str:
    for k, v in ESC.items():
        s = s.replace(k, v)
    return s


def n(v, nd=3, dash="---"):
    if v is None:
        return dash
    s = f"{v:.{nd}f}"
    return "$-$" + s[1:] if s.startswith("-") else s


def bold(s, on=True):
    return f"\\textbf{{{s}}}" if on else s


def key(r):
    return (r["dataset"], r["backbone"], r["attributor"], r["split"])


BIDX = {key(r): r for r in BENCH}


def bench_of(r):
    return BIDX.get(key(r), {})


def write(name, body):
    (OUT / name).write_text(body)
    print(f"  wrote {OUT / name}")


# ------------------------------------------------------------------ macros
def macros():
    m = []

    def n(v, nd=3, dash="---"):
        """Macro-safe number: negatives are wrapped so they typeset as a real
        minus sign whether the macro is used in text or in math mode."""
        if v is None:
            return dash
        s = f"{v:.{nd}f}"
        return "\\ensuremath{" + s + "}" if s.startswith("-") else s

    def add(cmd, val):
        m.append(f"\\newcommand{{\\{cmd}}}{{{val}}}")

    add("nCellsDone", COV["n_done_total"])
    add("nCellsPlanned", COV["n_planned"])
    add("nCellsPlanDone", COV["n_done_in_plan"])
    add("nCellsExtra", COV["n_extra"])
    add("nCellsPending", COV["n_planned"] - COV["n_done_in_plan"])
    add("nDatasetsDone", len(COV["datasets_done"]))
    add("nBackbonesDone", len(COV["backbones_done"]))
    add("nAttributorsDone", len(COV["attributors_done"]))
    add("nClsRows", len(CLS))
    add("nRegRows", len(REG))
    add("nGtCells", sum(1 for r in BENCH if r["gt_auroc"] is not None))
    add("nNoGtCells", sum(1 for r in BENCH if r["gt_auroc"] is None))
    pending_random = sum(1 for p in COV["pending"] if p[3] == "random")
    add("nPendingRandom", pending_random)
    add("nPendingScaffold", len(COV["pending"]) - pending_random)

    # --- MUTAG x GINE x scaffold: the faithful-but-wrong quartet -----------
    def cell(ds, bb, at, sp):
        return BIDX[(ds, bb, at, sp)]

    for at, tag in [("Saliency", "Sal"), ("InputXGradient", "IxG"),
                    ("IntegratedGradients", "IG"), ("GNNExplainer", "GNNE"),
                    ("GuidedBackprop", "GBP"), ("PGExplainer", "PGE")]:
        try:
            c = cell("MUTAG", "GINE", at, "scaffold")
        except KeyError:
            continue
        add(f"mutag{tag}Gt", n(c["gt_auroc"]))
        add(f"mutag{tag}Occ", n(c["occ_spearman"]))
        add(f"mutag{tag}Fid", n(c["fidelity_plus"]))
        add(f"mutag{tag}Char", n(c["characterization"]))
    for at, tag in [("Saliency", "Sal"), ("IntegratedGradients", "IG"),
                    ("GNNExplainer", "GNNE"), ("GuidedBackprop", "GBP"),
                    ("InputXGradient", "IxG"), ("PGExplainer", "PGE")]:
        try:
            c = cell("SynthMotifs", "GINE", at, "scaffold")
        except KeyError:
            continue
        add(f"synth{tag}Gt", n(c["gt_auroc"]))
        add(f"synth{tag}Occ", n(c["occ_spearman"]))

    # --- backbone sweeps at IG -------------------------------------------
    for ds, pre in [("SynthMotifs", "synth"), ("MUTAG", "mutag")]:
        rows = [r for r in BENCH if r["dataset"] == ds and r["split"] == "scaffold"
                and r["attributor"] == "IntegratedGradients"
                and r["gt_auroc"] is not None]
        for r in rows:
            add(f"{pre}{r['backbone']}IgGt", n(r["gt_auroc"]))
            add(f"{pre}{r['backbone']}IgOcc", n(r["occ_spearman"]))
        if rows:
            best = max(rows, key=lambda r: r["gt_auroc"])
            worst = min(rows, key=lambda r: r["gt_auroc"])
            add(f"{pre}IgBestBackbone", best["backbone"])
            add(f"{pre}IgWorstBackbone", worst["backbone"])
            add(f"{pre}IgSpread", n(best["gt_auroc"] - worst["gt_auroc"]))

    # --- selection experiment --------------------------------------------
    for blk in GTB:
        pre = "xl" if blk["dataset"] == "SynthMotifsXL" else "shift"
        add(f"{pre}Dataset", blk["dataset"])
        add(f"{pre}Split", blk["split"])
        add(f"{pre}GtBest", SHORT.get(blk["gt_best"], blk["gt_best"]))
        add(f"{pre}NMol", list(blk["per_attributor"].values())[0]["n_mol"])
        for k, v in blk["rank_correlation"].items():
            add(f"{pre}Rho{k.replace('_','').capitalize()}", n(v["rho"]))
        for sel in blk["selections"]:
            t = sel["faithfulness_metric"].replace("_", "").capitalize()
            add(f"{pre}Pick{t}", SHORT.get(sel["faithfulness_pick"],
                                           sel["faithfulness_pick"]))
            add(f"{pre}PickGt{t}", n(sel["faithfulness_pick_gt_auroc"]))
            if sel["paired_gt_pvalue"] is not None:
                add(f"{pre}P{t}", f"{sel['paired_gt_pvalue']:.4f}")
                add(f"{pre}Gap{t}", n(sel["paired_gt_gap_median"]))
        add(f"{pre}NMismatch", sum(1 for s in blk["selections"] if s["mismatch"]))

    # --- regime-level aggregates -----------------------------------------
    import statistics as st  # noqa: E402
    for reg in ("synthetic", "classification", "regression"):
        vals = [r["occ_spearman"] for r in BENCH
                if r["regime"] == reg and r["occ_spearman"] is not None]
        add(f"med{reg.capitalize()}Occ", n(st.median(vals)))
        add(f"n{reg.capitalize()}Cells", len(vals))
        neg = sum(1 for v in vals if v < 0)
        add(f"nNeg{reg.capitalize()}", neg)
    stab = [r["stability"] for r in BENCH if r["stability"] is not None]
    add("medStability", n(st.median(stab)))
    add("minStability", n(min(stab)))
    add("nStabilityCells", len(stab))

    # --- faithful-but-wrong tally (the headline phenomenon, counted) -------
    gt_cells = [r for r in BENCH if r["gt_auroc"] is not None
                and r["occ_spearman"] is not None]
    add("nGtOccCells", len(gt_cells))
    fbw = [r for r in gt_cells if r["occ_spearman"] > 0 and r["gt_auroc"] < 0.5]
    add("nFaithfulButWrong", len(fbw))
    add("nAntiAligned", sum(1 for r in gt_cells if r["gt_auroc"] < 0.5))

    # --- does the attributor ranking survive a change of dataset? ----------
    def spearman(a, b):
        def rank(v):
            order = sorted(range(len(v)), key=lambda i: v[i])
            r = [0.0] * len(v)
            i = 0
            while i < len(order):
                j = i
                while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                    j += 1
                avg = (i + j) / 2 + 1
                for k in range(i, j + 1):
                    r[order[k]] = avg
                i = j + 1
            return r
        ra, rb = rank(a), rank(b)
        ma, mb = sum(ra) / len(ra), sum(rb) / len(rb)
        num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
        da = sum((x - ma) ** 2 for x in ra) ** 0.5
        db = sum((y - mb) ** 2 for y in rb) ** 0.5
        return num / (da * db) if da and db else float("nan")

    def gt_by(dataset, split, keyfield, fixed):
        out = {}
        for r in BENCH:
            if (r["dataset"] == dataset and r["split"] == split
                    and r["gt_auroc"] is not None
                    and all(r[k] == v for k, v in fixed.items())):
                out[r[keyfield]] = r["gt_auroc"]
        return out

    pairs = [("attrRankRho", gt_by("SynthMotifs", "scaffold", "attributor",
                                   {"backbone": "GINE"}),
              gt_by("MUTAG", "scaffold", "attributor", {"backbone": "GINE"})),
             ("attrRankRhoXL", gt_by("SynthMotifsXL", "random", "attributor",
                                     {"backbone": "GINE"}),
              gt_by("MUTAG", "scaffold", "attributor", {"backbone": "GINE"})),
             ("backboneRankRho", gt_by("SynthMotifs", "scaffold", "backbone",
                                       {"attributor": "IntegratedGradients"}),
              gt_by("MUTAG", "scaffold", "backbone",
                    {"attributor": "IntegratedGradients"}))]
    for cmd, A, B in pairs:
        shared = sorted(set(A) & set(B))
        add(cmd, n(spearman([A[k] for k in shared], [B[k] for k in shared])))
        add(cmd + "N", len(shared))

    # --- per-attributor median stability ----------------------------------
    for at, tag in [("IntegratedGradients", "IG"), ("Saliency", "Sal"),
                    ("InputXGradient", "IxG"), ("GuidedBackprop", "GBP"),
                    ("GNNExplainer", "GNNE"), ("PGExplainer", "PGE")]:
        vals = [r["stability"] for r in BENCH
                if r["attributor"] == at and r["stability"] is not None]
        if vals:
            add(f"stab{tag}", n(st.median(vals)))
            add(f"nStab{tag}", len(vals))

    # --- the anti-predictive-but-faithful cell -----------------------------
    worst = min((r for r in CLS if r["auc"] is not None), key=lambda r: r["auc"])
    add("worstAucDataset", tex(worst["dataset"]))
    add("worstAucBackbone", worst["backbone"])
    add("worstAuc", n(worst["auc"]))
    add("worstAucAcc", n(worst["acc"]))
    add("worstAucOcc", n(worst["occ_spearman"]))
    add("worstAucChar", n(bench_of(worst).get("characterization")))

    # --- gradient-family faithfulness spread on the MUTAG shift cell -------
    grad = [BIDX[("MUTAG", "GINE", a, "scaffold")]["occ_spearman"]
            for a in ("Saliency", "InputXGradient", "IntegratedGradients")
            if ("MUTAG", "GINE", a, "scaffold") in BIDX]
    if len(grad) > 1:
        add("mutagGradOccSpread", n(max(grad) - min(grad)))

    # --- coherence band + ESOL fit, quoted in the prose --------------------
    mol_cls = [r for r in CLS if r["gt_auroc"] is None and r["motif_top1"] is not None]
    mol_all = mol_cls + [r for r in REG if r["motif_top1"] is not None]
    vals = [r["motif_top1"] for r in mol_all]
    add("motifTopMin", n(min(vals)))
    add("motifTopMax", n(max(vals)))
    add("nMolecularCells", len(vals))
    add("nMotifInBand", sum(1 for v in vals if 0.6 <= v <= 0.9))
    esol = [r for r in REG if r["dataset"] == "ESOL" and r["r2"] is not None]
    if esol:
        add("esolRtwoMin", n(min(r["r2"] for r in esol)))
        add("esolRtwoMax", n(max(r["r2"] for r in esol)))
        add("nEsolBackbones", len({r["backbone"] for r in esol}))

    # --- paired contrasts quoted in the prose ------------------------------
    block = PAIRED.get("MUTAG · GINE · scaffold split", [])
    for r in block:
        pair = {r["A"], r["B"]}
        if pair == {"IntegratedGradients", "Saliency"}:
            add("mutagIGvsSalP", f"{r['p']:.3f}")
            add("mutagIGvsSalN", str(int(r["n"])))
        if pair == {"IntegratedGradients", "InputXGradient"}:
            add("mutagIGvsIxGP", f"{r['p']:.3f}")

    # accuracy / calibration extremes actually present in the matrix
    accs = [(r["acc"], r["auc"], r["dataset"], r["backbone"]) for r in CLS
            if r["acc"] is not None and r["auc"] is not None]
    degenerate = [a for a in accs if a[0] >= 0.99 and a[1] < 0.9]
    add("nDegenerateRows", len(degenerate))
    eces = [r["ece"] for r in CLS if r["ece"] is not None]
    add("maxEce", n(max(eces)))
    add("medEce", n(st.median(eces)))

    write("macros.tex", "\n".join(m) + "\n")


# ------------------------------------------------------------- tier-1 table
def tab_tier1():
    rows = [r for r in CLS if r["gt_auroc"] is not None]
    rows.sort(key=lambda r: (r["dataset"], r["split"], r["backbone"], r["attributor"]))
    # best GT AUROC / best occlusion rho within each dataset x split block
    blocks: dict[tuple, list] = {}
    for r in rows:
        blocks.setdefault((r["dataset"], r["split"]), []).append(r)
    best_gt = {id(max(v, key=lambda r: r["gt_auroc"]))
               for v in blocks.values() if len(v) > 1}
    best_occ = {id(max(v, key=lambda r: (r["occ_spearman"] is not None,
                                         r["occ_spearman"])))
                for v in blocks.values() if len(v) > 1}

    L = ["\\begin{table*}[t]", "\\centering",
         "\\caption{\\textbf{Tier-1 cells: the only cells where attribution "
         "\\emph{correctness} is measurable.} All committed cells that carry a "
         "node-level ground truth --- exact for the synthetic sets, a "
         "chemically motivated nitro-motif proxy for MUTAG. GT AUROC $=0.5$ is "
         "chance; below $0.5$ the attribution is anti-aligned with the true "
         "motif. Occlusion $\\rho$ is the attribution--occlusion rank agreement "
         "(higher $=$ more faithful to the model). Bold marks the best GT AUROC "
         "and the best occlusion $\\rho$ within each dataset$\\times$split block "
         "(emphasis only; values are unaltered).}",
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
            tex(r["dataset"]), r["backbone"], SHORT.get(r["attributor"], r["attributor"]),
            r["split"], f"{int(r['n_mol'])}", n(r["acc"]), n(r["auc"]),
            bold(n(r["gt_auroc"]), id(r) in best_gt),
            n(r["gt_auprc"]),
            bold(n(r["occ_spearman"]), id(r) in best_occ),
            n(r["fid+"]), n(r["fid-"]), n(b.get("stability")),
        ]) + " \\\\")
    L += ["\\bottomrule", "\\end{tabular}}", "\\end{table*}"]
    write("tab_tier1.tex", "\n".join(L) + "\n")


# --------------------------------------------------- molecular classification
def tab_molecular():
    """Split across two rotated tables so each fits the page at the same
    \\resizebox{0.95\\textheight} scaling (35 rows do not fit in one)."""
    rows = [r for r in CLS if r["gt_auroc"] is None]
    rows.sort(key=lambda r: (r["dataset"], r["backbone"], r["attributor"]))
    datasets = sorted({r["dataset"] for r in rows})
    half = len(rows) / 2
    cut, seen = len(datasets), 0
    for i, ds in enumerate(datasets):
        seen += sum(1 for r in rows if r["dataset"] == ds)
        if seen >= half:
            cut = i + 1
            break
    parts = [datasets[:cut], datasets[cut:]]

    blocks: dict[str, list] = {}
    for r in rows:
        blocks.setdefault(r["dataset"], []).append(r)
    best_occ = {id(max(v, key=lambda r: (r["occ_spearman"] is not None,
                                         r["occ_spearman"])))
                for v in blocks.values() if len(v) > 1}

    caption_head = ("\\textbf{Molecular classification cells (no node-level "
                    "ground truth available)")
    caption_tail = (".} Every committed classification cell on a real molecular "
                    "dataset. The ground-truth localisation column does not "
                    "exist for these datasets --- no per-atom labels are "
                    "published --- so only model-side reliability can be "
                    "measured, which is precisely the gap the Tier-1 cells are "
                    "needed to close. \\emph{charact.} is the GraphFramEx "
                    "characterisation score and \\emph{unfaith.} the PyG/DIG "
                    "unfaithfulness metric, computed on the same molecules. "
                    "Bold marks the best occlusion $\\rho$ per dataset "
                    "(emphasis only).}")

    for pi, part in enumerate(parts):
        sub = [r for r in rows if r["dataset"] in part]
        L = ["\\begin{sidewaystable*}[p]", "\\centering",
             "\\captionsetup{width=0.95\\textheight}",
             "\\caption{" + caption_head
             + f", {pi + 1} of {len(parts)}" + caption_tail,
             "\\label{tab:molecular" + ("" if pi == 0 else chr(97 + pi)) + "}",
             "\\renewcommand{\\arraystretch}{1.3}",
             "\\resizebox{0.95\\textheight}{!}{%",
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
                tex(r["dataset"]), r["backbone"],
                SHORT.get(r["attributor"], r["attributor"]),
                r["split"], f"{int(r['n_mol'])}", n(r["acc"]), n(r["auc"]),
                n(r["ece"]), n(r["motif_top1"]),
                bold(n(r["occ_spearman"]), id(r) in best_occ),
                n(r["occ_top1"]), n(r["fid+"]), n(r["fid-"]),
                n(b.get("stability")), n(b.get("characterization")),
                n(b.get("unfaithfulness")),
            ]) + " \\\\")
        L += ["\\bottomrule", "\\end{tabular}}", "\\end{sidewaystable*}"]
        write(f"tab_molecular_{pi + 1}.tex", "\n".join(L) + "\n")


# -------------------------------------------------------------- regression
def tab_regression():
    rows = sorted(REG, key=lambda r: (r["dataset"], r["backbone"], r["attributor"]))
    neg = [r for r in REG if r["occ_spearman"] is not None and r["occ_spearman"] < 0]
    pos = [r for r in REG if r["occ_spearman"] is not None and r["occ_spearman"] >= 0]
    NEG_REG = len(neg)
    POS_REG = (", ".join(f"{tex(r['dataset'])} under {r['backbone']}" for r in pos)
               if pos else "none")
    L = ["\\begin{table*}[t]", "\\centering",
         "\\caption{\\textbf{Molecular regression cells.} Occlusion "
         "faithfulness is computed in output space (predicted-value shift) "
         "rather than probability space. In " + str(NEG_REG) + " of the "
         + str(len(REG)) + " committed regression cells the "
         "attribution--occlusion agreement is \\emph{negative} --- the atoms an "
         "attributor ranks highest are not the atoms whose removal moves the "
         "prediction most --- the sole exception being " + POS_REG + ". Bold "
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
         "\\textbf{occ.\\ top-1} & \\textbf{sparsity} & \\textbf{stab.} \\\\",
         "\\midrule"]
    blocks: dict[str, list] = {}
    for r in rows:
        blocks.setdefault(r["dataset"], []).append(r)
    best = {id(max(v, key=lambda r: r["occ_spearman"])) for v in blocks.values()}
    prev = None
    for r in rows:
        b = bench_of(r)
        if prev is not None and r["dataset"] != prev:
            L.append("\\addlinespace[2pt]")
        prev = r["dataset"]
        L.append(" & ".join([
            tex(r["dataset"]), r["backbone"], SHORT.get(r["attributor"], r["attributor"]),
            r["split"], f"{int(r['n_mol'])}", n(r["rmse"]), n(r["mae"]), n(r["r2"]),
            n(r["motif_top1"]), bold(n(r["occ_spearman"]), id(r) in best),
            n(r["occ_top1"]), n(r["sparsity"]), n(b.get("stability")),
        ]) + " \\\\")
    L += ["\\bottomrule", "\\end{tabular}}", "\\end{table*}"]
    write("tab_regression.tex", "\n".join(L) + "\n")


# ------------------------------------------------------- selection experiment
def tab_selection():
    L = ["\\begin{table*}[t]", "\\centering",
         "\\caption{\\textbf{Does a faithfulness-only ranking pick the "
         "ground-truth-best attributor?} Each row ranks the six attributors on "
         "the same molecules by one faithfulness/fidelity metric and asks "
         "whether its top choice is the attributor the ground truth ranks best. "
         "In distribution the answer is yes for every metric; under scaffold "
         "shift the two field-standard metrics choose an attributor that is "
         "anti-aligned with the ground truth, and the rank correlation between "
         "faithfulness and correctness collapses. $p$ is a paired Wilcoxon test "
         "on per-molecule GT AUROC between the selected and the "
         "ground-truth-best attributor.}",
         "\\label{tab:selection}",
         "\\small",
         "\\renewcommand{\\arraystretch}{1.3}",
         "\\resizebox{\\textwidth}{!}{%",
         "\\begin{tabular}{llllrlrcrr}",
         "\\toprule",
         "\\textbf{regime} & \\textbf{cell} & \\textbf{ranking metric} & "
         "\\textbf{its top pick} & \\textbf{pick GT} & \\textbf{GT-best} & "
         "\\textbf{GT-best} & \\textbf{mismatch} & \\textbf{Wilcoxon $p$} & "
         "\\textbf{$\\rho$(faith,GT)} \\\\",
         "\\midrule"]
    names = {"occ_spearman": "occlusion $\\rho$", "fidelity_plus": "Fidelity+",
             "characterization": "characterisation"}
    regimes = {"SynthMotifsXL": "in-distribution", "MUTAG": "scaffold shift"}
    for bi, blk in enumerate(GTB):
        if bi:
            L.append("\\addlinespace[2pt]")
        nmol = list(blk["per_attributor"].values())[0]["n_mol"]
        cell = (tex(blk["dataset"]) + "$\\cdot$" + blk["backbone"]
                + ", $n$=" + str(nmol))
        for si, sel in enumerate(blk["selections"]):
            rho = blk["rank_correlation"][sel["faithfulness_metric"]]["rho"]
            p = sel["paired_gt_pvalue"]
            L.append(" & ".join([
                regimes.get(blk["dataset"], "") if si == 0 else "",
                cell if si == 0 else "",
                names[sel["faithfulness_metric"]],
                SHORT.get(sel["faithfulness_pick"], sel["faithfulness_pick"]),
                n(sel["faithfulness_pick_gt_auroc"]),
                SHORT.get(sel["gt_best"], sel["gt_best"]),
                n(sel["gt_best_gt_auroc"]),
                "\\textbf{yes}" if sel["mismatch"] else "no",
                "---" if p is None else f"{p:.4f}",
                n(rho),
            ]) + " \\\\")
    L += ["\\bottomrule", "\\end{tabular}}", "\\end{table*}"]
    write("tab_selection.tex", "\n".join(L) + "\n")


# ------------------------------------------------------------ paired stats
def tab_paired():
    wanted = [k for k in PAIRED
              if k.startswith("SynthMotifsXL") or k.startswith("MUTAG · GINE · scaffold")]
    L = ["\\begin{table}[t]", "\\centering",
         "\\caption{\\textbf{Paired attributor comparisons on shared "
         "molecules} (Wilcoxon signed-rank on per-molecule occlusion "
         "faithfulness). The powered in-distribution cell separates the "
         "attributor families decisively; the small shift cell mostly cannot, "
         "which is itself a reason not to rank attributors on faithfulness "
         "alone. $p$ values are unadjusted for multiplicity and are printed at "
         "the precision of the committed artifact, in which $0.000$ denotes "
         "$p<0.0005$.}",
         "\\label{tab:paired}",
         "\\footnotesize",
         "\\renewcommand{\\arraystretch}{1.2}",
         "\\begin{tabular}{lrrr}",
         "\\toprule",
         "\\textbf{A vs.\\ B} & \\textbf{$n$} & "
         "\\textbf{median $\\Delta$} & \\textbf{$p$} \\\\",
         "\\midrule"]
    for bi, blockname in enumerate(wanted):
        if bi:
            L.append("\\addlinespace[3pt]")
        rows = PAIRED[blockname]
        label = tex(blockname.replace(" · ", ", "))
        L.append("\\multicolumn{4}{l}{\\itshape " + label + "} \\\\")
        L.append("\\addlinespace[1pt]")
        for r in rows:
            L.append(" & ".join([
                f"{SHORT.get(r['A'], r['A'])} vs.\\ {SHORT.get(r['B'], r['B'])}",
                f"{int(r['n'])}", n(r["median_delta"]),
                "---" if r["p"] is None else f"{r['p']:.3f}",
            ]) + " \\\\")
    L += ["\\bottomrule", "\\end{tabular}", "\\end{table}"]
    write("tab_paired.tex", "\n".join(L) + "\n")


# ------------------------------------------------------------- related work
def tab_related():
    """Render the committed related-work matrix (paper/RELATED_WORK.md)."""
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
        c = c.replace("~", "$\\sim$")
        return tex(c)

    L = ["\\begin{table*}[t]", "\\centering",
         "\\caption{\\textbf{Where the audit sits relative to existing "
         "evaluation frameworks.} \\ding{51}~$=$ core capability, "
         "$\\sim$~$=$ partial or possible but not central, \\ding{55}~$=$ not a "
         "focus. The contribution is the combination, not any single row: "
         "ground-truth validation and faithfulness both exist elsewhere, but "
         "not jointly with cross-checkpoint stability, calibration linkage and "
         "scaffold-shift stratification over a motif-native decomposition.}",
         "\\label{tab:related}",
         "\\small",
         "\\renewcommand{\\arraystretch}{1.3}",
         "\\resizebox{\\textwidth}{!}{%",
         "\\begin{tabular}{l" + "c" * (len(header) - 1) + "}",
         "\\toprule",
         " & ".join(f"\\textbf{{{tex(h.replace('**',''))}}}" for h in header) + " \\\\",
         "\\midrule"]
    for r in rows:
        if len(r) != len(header):
            continue
        L.append(" & ".join([tex(r[0].replace("**", ""))] +
                            [mark(c) for c in r[1:]]) + " \\\\")
    L += ["\\bottomrule", "\\end{tabular}}", "\\end{table*}"]
    write("tab_related.tex", "\n".join(L) + "\n")


# --------------------------------------------------------------- coverage
def tab_coverage():
    pend = COV["pending"]
    by_ds: dict[str, list] = {}
    for ds, bb, at, sp in pend:
        by_ds.setdefault(ds, []).append((bb, at, sp))
    L = ["\\begin{table}[t]", "\\centering",
         "\\caption{\\textbf{What is still running.} The planned grid is "
         "\\texttt{configs/full.yaml}; this draft reports the cells committed "
         "so far. Pending cells are left blank everywhere in this paper --- "
         "never imputed. The overwhelming majority of what is outstanding is "
         "the in-distribution (random-split) reference arm; the two synthetic "
         "sets whose download is blocked in this environment are listed as "
         "blocked, not pending.}",
         "\\label{tab:coverage}",
         "\\footnotesize",
         "\\renewcommand{\\arraystretch}{1.25}",
         "\\begin{tabular}{lcc}",
         "\\toprule",
         "\\textbf{dataset} & \\textbf{cells committed} & "
         "\\textbf{cells pending} \\\\",
         "\\midrule"]
    done_by_ds: dict[str, int] = {}
    for r in BENCH:
        done_by_ds[r["dataset"]] = done_by_ds.get(r["dataset"], 0) + 1
    all_ds = sorted(set(done_by_ds) | set(by_ds))
    for ds in all_ds:
        note = ""
        if ds in {"BA-2Motifs", "ShapeGGen"}:
            note = "~\\textsuperscript{$\\dagger$}"
        L.append(f"{tex(ds)}{note} & {done_by_ds.get(ds, 0)} & "
                 f"{len(by_ds.get(ds, []))} \\\\")
    L += ["\\midrule",
          f"\\textbf{{total}} & \\textbf{{{COV['n_done_total']}}} & "
          f"\\textbf{{{len(pend)}}} \\\\",
          "\\bottomrule", "\\end{tabular}",
          "\\\\[3pt]\\raggedright\\footnotesize $\\dagger$ blocked in this "
          "environment (dependency/download unavailable), not merely unfinished.",
          "\\end{table}"]
    write("tab_coverage.tex", "\n".join(L) + "\n")


if __name__ == "__main__":
    print("Generating LaTeX tables and macros from committed results…")
    macros()
    tab_related()
    tab_tier1()
    tab_selection()
    tab_molecular()
    tab_regression()
    tab_paired()
    tab_coverage()
    print("done.")
