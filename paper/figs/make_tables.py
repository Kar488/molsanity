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
         "GNNExplainer": "GNNExpl.", "PGExplainer": "PGExpl.",
         "SubgraphX": "SubgraphX"}
ESC = {"&": "\\&", "%": "\\%", "_": "\\_", "#": "\\#"}
ATTR_ORDER = ["IntegratedGradients", "Saliency", "InputXGradient",
              "GuidedBackprop", "GNNExplainer", "PGExplainer", "SubgraphX"]
# Cell families with a node-level ground truth, the full attributor set, and
# BOTH splits — within-dataset in-distribution vs. scaffold-shift contrasts,
# where only the split changes.
#
# MUTAG leads and is the ONLY arm that can carry a shift claim: it is the only
# ground-truth family that is both molecular and unsaturated. SynthMotifs was
# the second arm until 2026-08-03; it is not molecular, so it has no
# Bemis-Murcko scaffold and its "scaffold" split comes back
# frac_grouped = 0.000, degenerate = True — an arbitrary deterministic
# partition, not a chemical shift. Same for BA-2Motifs and ShapeGGen.
# MolMotif is the molecular exactly-labelled arm, but it saturates at
# GT AUROC ~0.99, where ranking attributors is noise around a ceiling; it is
# reported as a probe that the audit works, not as a second shift contrast.
ARMS = [("MUTAG", "GINE", "mut"), ("MolMotifHard", "GINE", "hard"),
        ("MolMotif", "GINE", "mol"), ("Benzene", "GINE", "benz"),
        ("FluorideCarbonyl", "GINE", "fluor")]

# The arms the pooled faithfulness-correctness estimate is computed over: the
# molecular ground-truth datasets, the only ones whose "scaffold" split is a
# chemical shift rather than an arbitrary deterministic partition. Kept at
# module scope, and kept a superset of ARMS, so a test can assert that an arm
# the selection table argues from is also an arm the pool is computed over.
MOLECULAR_GT = ("MUTAG", "MolMotif", "MolMotifHard",
                "Benzene", "FluorideCarbonyl")
# The subset available to an earlier version of this analysis, recomputed on
# the same run so the prose can compare the two without quoting either.
PRIOR_GT = ("MUTAG", "MolMotif", "MolMotifHard")
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

    def add_flag(name: str, on: bool):
        """A LaTeX conditional the prose can branch on.

        Some findings exist in one run and not the next. A macro that is only
        emitted when the finding exists breaks the build the moment it stops
        existing, and -- worse -- prose written around it would silently become
        a false claim if the macro were merely given a default. Emitting a
        boolean instead lets the manuscript drop the whole passage.
        """
        m.append(f"\\newif\\if{name}")
        m.append(f"\\{name}{'true' if on else 'false'}")

    # --- run provenance ----------------------------------------------------
    add("runConfig", tex(MAN["config_name"]))
    add("runStamp", MAN["timestamp"].replace("_", "-"))
    add("runSeed", MAN["seed"])
    add("runTorch", MAN["versions"]["torch"])
    add("runPyG", MAN["versions"]["torch_geometric"])
    add("runRDKit", MAN["versions"]["rdkit"])
    add("runCaptum", MAN["versions"]["captum"])
    add("runGitRev", MAN["git_rev"][:7])
    add("runPython", MAN["python"].split()[0])
    add("runNumpy", MAN["versions"]["numpy"])
    add("runScipy", MAN["versions"]["scipy"])
    add("runSklearn", MAN["versions"]["sklearn"])
    # The manifest records CUDA availability and device count, not the GPU
    # model, so the paper says only what was actually logged.
    add("runCuda", "yes" if MAN.get("cuda", {}).get("available") else "no")
    add("runDevices", MAN.get("cuda", {}).get("device_count", 0))
    _ns = max([r.get("n_seeds", 1) or 1 for r in list(CLS) + list(REG)] or [1])
    add("nRunSeeds", _ns)
    add("runSeedList", ", ".join(str(i) for i in range(_ns)))

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

    # --- the Faber partition: does the model actually read the rationale? ----
    # Faber et al. object that a low GT AUROC may be a fact about the model, not
    # the attribution, when the model does not use the labelled substructure.
    # That is testable per molecule: occlude the ground truth and see whether
    # the prediction collapses. Same rule as molsanity.audit.rationale, applied
    # to the committed records so the paper and the report cannot drift.
    uses, ignores = [], []
    for recs in RECS.values():
        for r in recs:
            rel, gt = r.get("rationale_reliance"), r.get("gt_auroc")
            if rel is None or gt is None:
                continue
            try:
                rel, gt = float(rel), float(gt)
            except (TypeError, ValueError):
                continue
            if rel != rel or gt != gt:
                continue
            (uses if rel > 0.5 else ignores).append(gt)
    add_flag("HasFaberPartition", bool(uses) and bool(ignores))
    if uses and ignores:
        anti = [g for g in uses if g < 0.5]
        add("nFaberUses", f"{len(uses):,}")
        add("nFaberIgnores", f"{len(ignores):,}")
        add("faberGtUses", num(st.mean(uses)))
        add("faberGtIgnores", num(st.mean(ignores)))
        add("nFaberAntiDespiteUse", f"{len(anti):,}")
        add("faberFracAntiDespiteUse", num(len(anti) / len(uses)))

    # --- abstention: what a practitioner can do with no ground truth ---------
    # Reuses the package implementation rather than reimplementing the curves,
    # so the paper and ABSTENTION.md cannot disagree. Every signal ranked here
    # is computable at inference time, without any rationale labels.
    ranked = []
    try:
        import sys
        root = str(Path(__file__).resolve().parents[2])
        if root not in sys.path:
            sys.path.insert(0, root)
        from molsanity.audit.abstention import rank_signals, risk_operating_point

        ranked = rank_signals([r for recs in RECS.values() for r in recs])
    except Exception as exc:  # noqa: BLE001
        print(f"  abstention macros unavailable ({type(exc).__name__}: {exc})")
    add_flag("HasAbstention", bool(ranked))
    if ranked:
        best, worst = ranked[0], ranked[-1]
        SIGNAL_LABEL = {"confidence": "predicted confidence",
                        "rationale_reliance": "rationale reliance",
                        "occ_spearman": "occlusion faithfulness",
                        "stability": "cross-checkpoint stability",
                        "motif_top1_share": "motif top-1 share"}
        add("nAbstainSignals", len(ranked))
        add("abstainBest", SIGNAL_LABEL.get(best["signal"], best["signal"]))
        add("abstainBestLift", num(best["lift"]))
        add("abstainWorst", SIGNAL_LABEL.get(worst["signal"], worst["signal"]))
        add("abstainWorstLift", num(worst["lift"]))
        add("nAbstainNeg", sum(1 for r in ranked if r["lift"] <= 0))
        add("abstainFullBelow", num(best["frac_below_chance_full"]))
        add("nAbstainRecords", f"{best['n']:,}")
        op = risk_operating_point(best["curve"], max_below_chance=0.10)
        add_flag("HasAbstainOp", op is not None)
        if op is not None:
            add("abstainCoverage", f"{100 * op['coverage']:.0f}\\%")
            add("abstainBelow", num(op["frac_below_chance"]))
            add("abstainKeptGt", num(op["mean_target"]))
            add("nAbstainKept", f"{op['n_kept']:,}")

    # --- the within-dataset shift contrasts (only the split changes) --------
    tags = {"IntegratedGradients": "IG", "Saliency": "Sal",
            "InputXGradient": "IxG", "GuidedBackprop": "GBP",
            "GNNExplainer": "GNNE", "PGExplainer": "PGE",
            "SubgraphX": "SGX"}
    add("nArms", len(ARMS))

    # --- the pooled molecular result -----------------------------------------
    # Per arm the 7-point rank correlation is a weak instrument; pooled over
    # every molecular ground-truth cell it is the paper's central claim. Only
    # datasets with a real Bemis-Murcko scaffold: the non-molecular arms have a
    # degenerate scaffold split and cannot enter a shift contrast.
    #
    # Built from CLS, whose rows load_results() has already collapsed to the
    # across-seed mean per cell. Computing it instead from the per-molecule
    # records under artifacts/audit -- which carry a single seed per cell --
    # silently reports rho = -0.255 (p = 0.152) in place of the seed-averaged
    # -0.353 (p = 0.044). With the median across-seed sd on occlusion rho at
    # 0.146, one seed is not the quantity to correlate, and the two answers sit
    # on opposite sides of every conventional threshold.
    # Benzene and FluorideCarbonyl sat out one reported sweep. In the
    # 2026-08-05 run their loader dropped the archive's SMILES, so Bemis-Murcko
    # had nothing to work with and all six of their scaffold splits came back
    # DEGENERATE at 0.0% grouped; pooling them then would have put a
    # deterministic partition into the shift contrast. SCAFFOLD_SPLIT_VERSION 3
    # carries the SMILES and the 2026-08-06 run gives them real partitions, so
    # they are in. They are in whatever they do to the pooled estimate: the
    # exclusion was justified by the degenerate split and by nothing else, and
    # leaving them out once that reason expired would be selecting arms on
    # their result.
    def _paired_cells(arms):
        """(dataset, backbone, attributor) -> {split: (gt, occ)} over `arms`."""
        by = {}
        for r in CLS:
            if r["dataset"] not in arms:
                continue
            g, o = r.get("gt_auroc"), r.get("occ_spearman")
            if g is None or o is None:
                continue
            by.setdefault((r["dataset"], r["backbone"], r["attributor"],
                           r["split"]), []).append((g, o))
        out = {}
        for (ds, bb, at, sp), vals in by.items():
            out.setdefault((ds, bb, at), {})[sp] = (
                st.mean(v[0] for v in vals), st.mean(v[1] for v in vals))
        return {k: v for k, v in out.items() if {"random", "scaffold"} <= set(v)}

    per_cell = _paired_cells(MOLECULAR_GT)
    seeds = [r.get("n_seeds", 1) for r in CLS
             if r["dataset"] in MOLECULAR_GT and r.get("gt_auroc") is not None]
    add("nPooledSeeds", min(seeds) if seeds else 1)

    # The same pooled statistic restricted to the three arms this work reported
    # before Benzene and FluorideCarbonyl were loadable. Recomputed here, from
    # this run's artefacts, rather than quoted from the earlier preprint: the
    # prose compares the two and neither number should be typed by hand.
    _prior = _paired_cells(PRIOR_GT)
    add_flag("HasPriorPool", len(_prior) >= 8 and len(_prior) < len(per_cell))
    if _prior:
        _pk = sorted(_prior)
        add("nPooledPriorCells", len(_pk))
        add("nPooledPriorArms", len({k[0] for k in _pk}))
        for sp, tag in (("random", "Ind"), ("scaffold", "Shift")):
            r, pv = D.spearman([_prior[k][sp][1] for k in _pk],
                               [_prior[k][sp][0] for k in _pk])
            add(f"pooledPrior{tag}Rho", num(r))
            add(f"pooledPrior{tag}P",
                "\\ensuremath{<}0.001" if pv < 0.001 else f"{pv:.3f}")

    # --- compute cost, parsed from the run log, never typed --------------------
    # JCIM asks for reproduction cost. Timings are derived from the committed
    # log's timestamps so they cannot drift from the run they describe.
    import datetime as _dt
    import glob as _glob
    import re as _re
    logs = sorted(_glob.glob(str(D.REPO / "results" / "logs" / "run_*.log")))
    add_flag("HasCompute", bool(logs))
    if logs:
        lines = Path(logs[-1]).read_text().splitlines()
        stamp = lambda l: _dt.datetime.strptime(l[:19], "%Y-%m-%d %H:%M:%S")
        add("computeWall", f"{(stamp(lines[-1]) - stamp(lines[0])).total_seconds() / 60:.0f}")
        n_done = sum(1 for l in lines if "] DONE" in l)
        n_cached = sum(1 for l in lines if "[cached]" in l)
        add("nComputeCached", n_cached)
        add("nComputeFresh", n_done - n_cached)
        # NB: never bind `m` here -- add() closes over the accumulator list of
        # that name, and a loop variable called `m` silently replaces it with a
        # regex match, so every later add() raises on a NoneType.
        durs, last = [], None
        for l in lines:
            hit = _re.search(r"\[cell (\S+?)\] DONE", l)
            if not hit:
                continue
            ts = stamp(l)
            if last and "[cached]" not in l:
                durs.append((hit.group(1).split("__")[2], (ts - last).total_seconds()))
            last = ts
        by = {}
        for a, d in durs:
            by.setdefault(a, []).append(d)
        for attr, tag in (("SubgraphX", "Sgx"), ("IntegratedGradients", "Ig")):
            v = sorted(by.get(attr, []))
            if v:
                add(f"cell{tag}Min", f"{v[len(v) // 2] / 60:.0f}")
                add(f"nCell{tag}", len(v))
        # A resumed sweep's final invocation may re-execute only a handful of
        # cells, so the log it leaves behind need not contain both attributors
        # or any training at all. The cost comparison then cannot be made and
        # the prose that quotes it has to disappear rather than default.
        add_flag("HasCostRatio",
                 bool(by.get("SubgraphX") and by.get("IntegratedGradients")))
        if by.get("SubgraphX") and by.get("IntegratedGradients"):
            a = sorted(by["SubgraphX"])[len(by["SubgraphX"]) // 2]
            b = sorted(by["IntegratedGradients"])[len(by["IntegratedGradients"]) // 2]
            add("cellCostRatio", f"{a / b:.0f}")
        trains, last = [], None
        for l in lines:
            dated = _re.match(r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d", l)
            if dated and _re.search(r"\[(cell|stage cell_)", l):
                last = stamp(l)
            if "Saved checkpoint" in l and "_early" not in l and dated and last:
                trains.append((stamp(l) - last).total_seconds())
        add_flag("HasTrainMedian", bool(trains))
        if trains:
            trains.sort()
            add("trainMedian", f"{trains[len(trains) // 2]:.0f}")
    paired = per_cell          # _paired_cells already keeps only paired cells
    add_flag("HasPooledMolecular", len(paired) >= 8)
    if len(paired) >= 8:
        ks = sorted(paired)
        add("nPooledCells", len(ks))
        add("nPooledArms", len({k[0] for k in ks}))
        for sp, tag in (("random", "Ind"), ("scaffold", "Shift")):
            rho, pv = D.spearman([paired[k][sp][1] for k in ks],
                                 [paired[k][sp][0] for k in ks])
            add(f"pooled{tag}Rho", num(rho))
            add(f"pooled{tag}P", "\\ensuremath{<}0.001" if pv < 0.001 else f"{pv:.3f}")
            add(f"pooled{tag}Faith", num(st.mean(paired[k][sp][1] for k in ks)))
            add(f"pooled{tag}Gt", num(st.mean(paired[k][sp][0] for k in ks)))
        # Does faithfulness itself move, and does correctness?
        for metric, idx, tag in (("faith", 1, "Faith"), ("gt", 0, "Gt")):
            a = [paired[k]["random"][idx] for k in ks]
            b = [paired[k]["scaffold"][idx] for k in ks]
            pv = D.paired_wilcoxon(a, b)["p"]
            add(f"pooledShift{tag}P", "\\ensuremath{<}0.001" if pv < 0.001 else f"{pv:.3f}")
        # Per-arm direction, so a contradicting arm cannot hide in the pool.
        # With five arms the spread of the per-arm shift correlation is the
        # result, not noise around a pooled mean, so the endpoints and the arms
        # holding them are emitted for the prose to quote.
        agree, per_arm_shift = 0, {}
        for ds in sorted({k[0] for k in ks}):
            sub = [k for k in ks if k[0] == ds]
            if len(sub) < 4:
                continue
            r0, _ = D.spearman([paired[k]["random"][1] for k in sub],
                               [paired[k]["random"][0] for k in sub])
            r1, _ = D.spearman([paired[k]["scaffold"][1] for k in sub],
                               [paired[k]["scaffold"][0] for k in sub])
            per_arm_shift[ds] = r1
            if r1 < r0:
                agree += 1
        add("nArmsAgree", agree)
        add("nArmsTotal", len({k[0] for k in ks}))
        if per_arm_shift:
            lo = min(per_arm_shift, key=per_arm_shift.get)
            hi = max(per_arm_shift, key=per_arm_shift.get)
            add("armShiftRhoMin", num(per_arm_shift[lo]))
            add("armShiftRhoMax", num(per_arm_shift[hi]))
            add("armShiftRhoMinDataset", lo)
            add("armShiftRhoMaxDataset", hi)
            add("nArmsShiftNeg", sum(1 for v in per_arm_shift.values() if v < 0))

        # Leave-one-arm-out. The pooled p is the number a reader will quote, so
        # the paper must say how much of it any single arm carries -- the first
        # check a sceptical reviewer runs, and running it ourselves is cheaper
        # than being told. On the 2026-08-04 run it is unflattering: drop MUTAG
        # and the effect is gone (rho -0.027, p 0.907). The pooled result is
        # MUTAG plus corroboration, not three arms independently agreeing.
        loo = {}
        for drop in sorted({k[0] for k in ks}):
            keep = [k for k in ks if k[0] != drop]
            if len(keep) < 8:
                continue
            r, pv = D.spearman([paired[k]["scaffold"][1] for k in keep],
                               [paired[k]["scaffold"][0] for k in keep])
            loo[drop] = (r, pv, len(keep))
        add_flag("HasLeaveOneOut", bool(loo))
        for ds, (r, pv, n) in loo.items():
            tag = {"MUTAG": "Mut", "MolMotif": "Mol", "MolMotifHard": "Hard"}.get(ds, ds)
            add(f"loo{tag}Rho", num(r))
            add(f"loo{tag}P", "\\ensuremath{<}0.001" if pv < 0.001 else f"{pv:.3f}")
            add(f"nLoo{tag}", n)
        add("nLooSurvive", sum(1 for _, pv, _ in loo.values() if pv < 0.05))
        add("nLooTotal", len(loo))
        # Cells contributed by a single arm -- the n a per-arm correlation
        # would actually be computed on, quoted when we say no arm is
        # significant on its own.
        per_arm = sorted({sum(1 for k in ks if k[0] == d)
                          for d in {k[0] for k in ks}})
        add("nArmCells", per_arm[0] if len(per_arm) == 1
            else f"{per_arm[0]}--{per_arm[-1]}")

    # Benjamini-Hochberg over the whole family of selection tests, so the prose
    # can quote an FDR-controlled value rather than a raw one. Built here in the
    # same order tab_selection walks so the macro and the table agree.
    _sel_cache, _pvals = {}, []
    for ds, bb, arm in ARMS:
        for sp, half in (("random", "Ind"), ("scaffold", "Shift")):
            sel = D.selection_test(ds, bb, sp)
            _sel_cache[(ds, bb, sp)] = sel
            if sel is not None:
                _pvals += [x["paired_gt_pvalue"] for x in sel["selections"]]
    _qvals = iter(D.benjamini_hochberg(_pvals))
    _qmap = {}
    for ds, bb, arm in ARMS:
        for sp, half in (("random", "Ind"), ("scaffold", "Shift")):
            sel = _sel_cache[(ds, bb, sp)]
            if sel is None:
                continue
            for x in sel["selections"]:
                _qmap[(ds, bb, sp, x["faithfulness_metric"])] = next(_qvals)
    add("nSelectionTests", len(_pvals))

    # --- how often the selection is wrong, and how much it costs ---------------
    # Counted over the same tests the table prints, per regime, because the
    # regime asymmetry is the claim. The cost of a wrong pick is the gap in
    # ground-truth localisation between the ground-truth-best attributor and
    # the one the faithfulness metric chose: a mismatch that gives up 0.002
    # AUROC and one that gives up 0.821 are the same row in the "mismatch"
    # column and are not the same result, so the gap is reported alongside.
    _sel_rows = []
    for ds, bb, arm in ARMS:
        for sp in ("random", "scaffold"):
            sel = _sel_cache[(ds, bb, sp)]
            if sel is None:
                continue
            for x in sel["selections"]:
                _sel_rows.append((ds, sp, x["faithfulness_metric"], x["mismatch"],
                                  x["gt_best_gt_auroc"] - x["faithfulness_pick_gt_auroc"],
                                  x["faithfulness_pick_gt_auroc"], x["gt_best_gt_auroc"]))
    if _sel_rows:
        add("nSelMismatch", sum(1 for r in _sel_rows if r[3]))
        add("nSelMatch", sum(1 for r in _sel_rows if not r[3]))
        # What uniform-random selection among the audited attributors would
        # have produced, so the handful of agreements is read against a
        # baseline rather than as a success.
        _n_attr = {len(_sel_cache[(ds, bb, sp)]["attributors"])
                   for ds, bb, _ in ARMS for sp in ("random", "scaffold")
                   if _sel_cache[(ds, bb, sp)] is not None}
        add_flag("HasSelChance", len(_n_attr) == 1)
        if len(_n_attr) == 1:
            add("selMatchChance", f"{len(_sel_rows) / _n_attr.pop():.1f}")
        for sp, tag in (("random", "Ind"), ("scaffold", "Shift")):
            sub = [r for r in _sel_rows if r[1] == sp]
            add(f"nSelMismatch{tag}", sum(1 for r in sub if r[3]))
            add(f"nSelTests{tag}", len(sub))
            add(f"selGapMean{tag}", num(st.mean(r[4] for r in sub)))
            # Which side of the gap moves between regimes: the attributor the
            # metric picks, or the one the ground truth ranks best.
            add(f"selPickGtMean{tag}", num(st.mean(r[5] for r in sub)))
            add(f"selBestGtMean{tag}", num(st.mean(r[6] for r in sub)))
        gaps = sorted(r[4] for r in _sel_rows if r[3])
        if gaps:
            add("selGapMin", num(gaps[0]))
            add("selGapMed", num(gaps[len(gaps) // 2]))
            add("selGapMax", num(gaps[-1]))
        # Paired by (arm, metric) so the two regimes are compared on the same
        # 15 selections rather than as two independent samples.
        _ind = {(r[0], r[2]): r[4] for r in _sel_rows if r[1] == "random"}
        _sh = {(r[0], r[2]): r[4] for r in _sel_rows if r[1] == "scaffold"}
        _k = sorted(set(_ind) & set(_sh))
        add_flag("HasSelGapTest", len(_k) >= 6)
        if len(_k) >= 6:
            _p = D.paired_wilcoxon([_ind[k] for k in _k], [_sh[k] for k in _k])["p"]
            add("selGapP", "\\ensuremath{<}0.001" if _p < 0.001 else f"{_p:.3f}")
            add("nSelGapPaired", len(_k))

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
                # A selection with too few paired molecules carries no p-value,
                # so the passage quoting one has to be able to disappear.
                add_flag(f"Has{pre}P{t}", x["paired_gt_pvalue"] is not None)
                if x["paired_gt_pvalue"] is not None:
                    pv = x["paired_gt_pvalue"]
                    add(f"{pre}P{t}",
                        "\\ensuremath{<}0.001" if pv < 0.001 else f"{pv:.3f}")
                    qv = _qmap.get((ds, bb, sp, x["faithfulness_metric"]))
                    if qv is not None and qv == qv:
                        add(f"{pre}Q{t}",
                            "\\ensuremath{<}0.001" if qv < 0.001 else f"{qv:.3f}")
                    add(f"{pre}Gap{t}", num(x["paired_gt_gap_median"]))
                    add(f"{pre}NPaired{t}", x["n_paired"])
            for k, v in sel["rank_correlation"].items():
                add(f"{pre}Rho{k.replace('_', '').capitalize()}", num(v["rho"]))
            # The bunching argument: an arm whose attributors are spread over
            # the AUROC range gives Spearman something to rank; one where most
            # of them sit within a few hundredths of 1.0 does not. Both the
            # range and the count above 0.9 used to be typed into the prose.
            gts = sorted(v["gt_auroc_mean"] for v in pa.values())
            add(f"{pre}GtSpan", f"{num(gts[0])}--{num(gts[-1])}")
            add(f"{pre}NAboveNine", sum(1 for g in gts if g > 0.9))
            # The selection test is computed from ONE seed's per-molecule
            # records -- it has to be, since the split is a function of the
            # seed and a paired test needs the same molecules on both sides.
            # The point estimate it reports is therefore not the across-seed
            # mean that every table row is, so the across-seed mean and sd of
            # the same cell are published next to it. For MUTAG-GINE-GNNExpl.
            # under shift the difference is 0.826 single-seed against
            # 0.774 +/- 0.086 across three: the same ordering, a materially
            # different number, and a reviewer will find it in SEED_VARIANCE.md.
            for r in CLS:
                if (r["dataset"], r["backbone"], r["attributor"], r["split"]) \
                        == (ds, bb, sel["gt_best"], sp):
                    if r.get("gt_auroc") is not None:
                        add(f"{pre}GtBestSeedMean", num(r["gt_auroc"]))
                    if r.get("gt_auroc_sd") is not None:
                        add(f"{pre}GtBestSeedSd", num(r["gt_auroc_sd"]))
                    break
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
    # Degenerate cells were present in the first single-seed run and absent
    # afterwards. The macros below must therefore always be defined, and the
    # prose that quotes them must disappear when there are none, rather than
    # describing a cell that no longer exists.
    add_flag("HasDegenerateCells", bool(degen))
    if degen:
        (k, v, nmol) = degen[0]
        add("degenCell", tex(k[0]) + "$\\cdot$" + k[1] + "$\\cdot$"
            + SHORT.get(k[2], k[2]) + ", " + k[3])
        add("degenVal", num(v))
        add("degenN", nmol)
    else:
        add("degenCell", "---")
        add("degenVal", "---")
        add("degenN", "0")

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
    bb_sweep_ok = True
    for sp, pre in (("scaffold", "bbShift"), ("random", "bbInd")):
        rows = [r for r in CLS if r["dataset"] == bb_ds and r["split"] == sp
                and r["attributor"] == "IntegratedGradients"
                and r["gt_auroc"] is not None]
        for r in rows:
            add(f"{pre}{r['backbone']}", num(r["gt_auroc"]))
        bb_sweep_ok = bb_sweep_ok and bool(rows)
        if rows:
            best = max(rows, key=lambda r: r["gt_auroc"])
            worst = min(rows, key=lambda r: r["gt_auroc"])
            add(f"{pre}Best", best["backbone"])
            add(f"{pre}BestVal", num(best["gt_auroc"]))
            add(f"{pre}Worst", worst["backbone"])
            add(f"{pre}WorstVal", num(worst["gt_auroc"]))
            add(f"{pre}Spread", num(best["gt_auroc"] - worst["gt_auroc"]))
            add(f"{pre}N", len(rows))
    # The backbone sweep is read at Integrated Gradients on both splits, so it
    # empties completely whenever IG fails -- which is exactly what a Captum
    # downgrade does. The passage quoting it must drop out rather than quote
    # macros that were never written.
    add_flag("HasBackboneSweep", bb_sweep_ok)
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
    add_flag("HasTox", bool(tox))
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
    """Every ground-truth cell, split across floats rather than shrunk to fit.

    This was one ``table*`` wrapped in ``adjustbox{max width=\\textwidth,
    max totalheight=0.80\\textheight}``. At 100 rows the HEIGHT constraint is
    the binding one, and adjustbox scales uniformly -- so clamping the height
    also shrank the width, producing a half-column-wide block of ~5pt type with
    empty margins either side. A reference table nobody can read is not a
    reference table.

    Now split on dataset boundaries into floats that each fit a page at
    \\footnotesize, using the same approach as ``tab_molecular``. Width still
    fills the text block; height is never scaled.
    """
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

    # Pack whole datasets into parts of at most MAX_ROWS; a dataset is never
    # split across floats, so no block of comparable rows is separated.
    MAX_ROWS = 46
    datasets = sorted({r["dataset"] for r in rows})
    parts, cur, cur_n = [], [], 0
    for ds in datasets:
        k = sum(1 for r in rows if r["dataset"] == ds)
        if cur and cur_n + k > MAX_ROWS:
            parts.append(cur)
            cur, cur_n = [], 0
        cur.append(ds)
        cur_n += k
    if cur:
        parts.append(cur)

    n_carried = sum(1 for r in rows if r.get("provenance") == "carried")
    carried_note = (
        " Rows marked \\textsuperscript{c} are \\emph{carried}: they survive in "
        "the results matrix from an earlier reduced-budget run because the "
        "corresponding cell failed in the latest one (Table~\\ref{tab:ledger}); "
        "every other row was produced by the run in Table~\\ref{tab:ledger}."
        if n_carried else
        " Every row was produced by the single run in Table~\\ref{tab:ledger}; "
        "none are carried over from an earlier one.")

    head = ("\\textbf{Every committed cell in which attribution "
            "\\emph{correctness} is measurable.} Ground truth is exact for the "
            "synthetic sets and for \\molDataset{}/\\hardDataset{} (the label "
            "\\emph{is} the substructure), and a chemically motivated "
            "nitro-motif proxy for MUTAG. GT AUROC $=0.5$ is chance; below "
            "$0.5$ the attribution is anti-aligned with the true motif. "
            "Occlusion $\\rho$ is the attribution--occlusion rank agreement "
            "(higher $=$ more faithful to the model)." + carried_note +
            " Bold marks the best GT AUROC and the best occlusion $\\rho$ "
            "within each dataset$\\times$split block (emphasis only; values "
            "are unaltered).")

    for pi, part in enumerate(parts):
        sub = [r for r in rows if r["dataset"] in part]
        cap = head if pi == 0 else (
            f"\\textbf{{Ground-truth cells, continued ({pi + 1} of "
            f"{len(parts)}).}} Columns and conventions as in "
            "Table~\\ref{tab:tier1}.")
        L = ["\\begin{table*}[t]", "\\centering",
             "\\caption{" + cap + "}"]
        if pi == 0:
            L.append("\\label{tab:tier1}")
        else:
            L.append(f"\\label{{tab:tier1part{pi + 1}}}")
        L += ["\\footnotesize",
              "\\renewcommand{\\arraystretch}{1.15}",
              # Width only. Never clamp height here: see the docstring.
              "\\adjustbox{max width=\\textwidth}{%",
              "\\begin{tabular}{lllcrrrrrrrrr}",
              "\\toprule",
              "\\textbf{dataset} & \\textbf{backbone} & \\textbf{attributor} & "
              "\\textbf{split} & \\textbf{$n$} & \\textbf{acc} & \\textbf{AUC} & "
              "\\textbf{GT AUROC} & \\textbf{GT AUPRC} & \\textbf{occ.\\ $\\rho$} & "
              "\\textbf{Fid+} & \\textbf{Fid--} & \\textbf{stab.} \\\\",
              "\\midrule"]
        prev = None
        for r in sub:
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
        name = "tab_tier1.tex" if len(parts) == 1 else f"tab_tier1_{pi + 1}.tex"
        write(name, "\n".join(L) + "\n")
    return len(parts)


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

    carried_note = (
        " \\emph{carried} counts cells whose row still appears in the results "
        "matrix from an earlier reduced-budget CPU run because this run's "
        "attempt failed. Those rows are marked \\textsuperscript{c} throughout "
        "this paper and are never mixed into a this-run aggregate."
        if COV["n_carried"] else
        " The \\emph{carried} column counts rows surviving from an earlier "
        "reduced-budget run because this run's attempt failed; it is zero, so "
        "every row in this paper is from the sweep reported here.")
    L = ["\\begin{table}[t]", "\\centering",
         "\\caption{\\textbf{The run ledger.} Outcome of every cell the "
         "\\texttt{" + tex(MAN["config_name"]) + "} sweep attempted, as recorded "
         "in \\texttt{results/PROGRESS.md}." + carried_note + "}",
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
    # A clean sweep leaves no reasons to list; emitting the heading anyway
    # printed a bare "Failure reasons. ." under the table.
    if reasons:
        L.append("\\\\[4pt]\\raggedright\\footnotesize "
                 "\\textbf{Failure reasons.} ")
        L.append("; ".join(f"{len(v)}~$\\times$ ``{tex(k[:66])}\\dots''"
                           for k, v in reasons) + ".")
    else:
        L.append("\\\\[4pt]\\raggedright\\footnotesize "
                 "No cell failed and none was skipped.")
    L.append("\\end{table}")
    write("tab_ledger.tex", "\n".join(L) + "\n")


# ------------------------------------------------------- selection experiment
def tab_selection():
    L = ["\\begin{table*}[t]", "\\centering",
         "\\caption{\\textbf{Does a faithfulness-only ranking pick the "
         "ground-truth-best attributor?} " + str(len(ARMS)) + " molecular cell "
         "families, each audited on both splits with the same backbone and the "
         "same " + str(len(ATTR_ORDER)) + " attributors, so within "
         "a family only the split changes and the contrast isolates distribution "
         "shift rather than confounding it with a change of dataset. Each row "
         "ranks the attributors by one faithfulness/fidelity metric and asks "
         "whether its top choice is the one the ground truth ranks best. $p$ is a "
         "paired Wilcoxon test on per-molecule GT AUROC between the selected and "
         "the ground-truth-best attributor, over the molecules both audited, and "
         "$q$ its Benjamini--Hochberg adjustment over all "
         + str(len(ARMS) * 2 * 3) + " selection tests in this table. Because a "
         "paired per-molecule test needs the same molecules on both sides and "
         "the split is a function of the seed, this table is computed within a "
         "single seed rather than across the three; the across-seed spread for "
         "the same cells is supplementary material.}",
         "\\label{tab:selection}",
         "\\small",
         "\\renewcommand{\\arraystretch}{1.3}",
         "\\resizebox{\\textwidth}{!}{%",
         "\\begin{tabular}{llllrlrcrrr}",
         "\\toprule",
         "\\textbf{cell} & \\textbf{regime} & \\textbf{ranking metric} & "
         "\\textbf{its top pick} & \\textbf{pick GT} & \\textbf{GT-best} & "
         "\\textbf{GT-best} & \\textbf{mismatch} & \\textbf{Wilcoxon $p$} & "
         "\\textbf{$q$} & \\textbf{$\\rho$(faith,GT)} \\\\",
         "\\midrule"]
    names = {"occ_spearman": "occlusion $\\rho$", "fidelity_plus": "Fidelity+",
             "characterization": "characterisation"}

    # Collect every selection test first so the false discovery rate is
    # controlled over the whole family (each cell x split x ranking metric),
    # which is the set a reader draws conclusions from.
    blocks = []
    for ds, bb, _arm in ARMS:
        for sp, label in (("random", "in-distribution"), ("scaffold", "scaffold shift")):
            sel = D.selection_test(ds, bb, sp)
            if sel is not None:
                blocks.append((ds, bb, sp, label, sel))
    qs = D.benjamini_hochberg([x["paired_gt_pvalue"]
                               for _, _, _, _, sel in blocks
                               for x in sel["selections"]])
    qi = iter(qs)

    first = True
    for ds, bb, sp, label, sel in blocks:
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
                pfmt(x["paired_gt_pvalue"]), pfmt(next(qi)), n(rho),
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
         "Table~\\ref{tab:selection}. $p$ is the raw two-sided Wilcoxon value "
         "and $q$ its Benjamini--Hochberg adjustment, controlling the false "
         "discovery rate over the contrasts within each cell block, which is "
         "the family a reader compares across.}",
         "\\label{tab:paired}",
         "\\footnotesize",
         "\\renewcommand{\\arraystretch}{1.2}",
         "\\begin{tabular}{lrrrr}",
         "\\toprule",
         "\\textbf{A vs.\\ B} & \\textbf{$n$} & \\textbf{median $\\Delta$} & "
         "\\textbf{$p$} & \\textbf{$q$} \\\\",
         "\\midrule"]
    for bi, sp in enumerate(("random", "scaffold")):
        cells = D.attributor_cells(ds, bb, sp)
        attrs = [a for a in ATTR_ORDER if a in cells]
        if len(attrs) < 2:
            continue
        if bi:
            L.append("\\addlinespace[3pt]")
        L.append("\\multicolumn{5}{l}{\\itshape " + tex(ds) + ", " + bb + ", "
                 + sp + " split} \\\\")
        L.append("\\addlinespace[1pt]")
        pairs = []
        for i, a in enumerate(attrs):
            for b in attrs[i + 1:]:
                A, B = D.by_graph(cells[a]), D.by_graph(cells[b])
                shared = sorted(set(A) & set(B))
                w = D.paired_wilcoxon([A[g]["occ_spearman"] for g in shared],
                                      [B[g]["occ_spearman"] for g in shared])
                pairs.append((a, b, w))
        # Control the false discovery rate over the contrasts within this
        # cell, which is the family a reader compares across.
        qs = D.benjamini_hochberg([w["p"] for _, _, w in pairs])
        for (a, b, w), q in zip(pairs, qs):
            L.append(" & ".join([
                f"{SHORT.get(a, a)} vs.\\ {SHORT.get(b, b)}",
                str(w["n"]), n(w["median_delta"]), pfmt(w["p"]), pfmt(q),
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
         "only a minority of molecules. In particular the confident-error "
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
    # 56 rows do not fit one rotated page at a legible size; split on a
    # dataset boundary near the halfway row so each part is readable.
    parts = [datasets[:cut], datasets[cut:]]
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
            "these datasets, since no per-atom labels are published, so only "
            "model-side reliability can be measured, which is the gap the "
            "Tier-1 cells are needed to close. \\emph{charact.} is the "
            "GraphFramEx characterisation score and \\emph{unfaith.} the "
            "PyG/DIG unfaithfulness metric, computed on the same molecules"
            + ("; both are blank for carried rows (\\textsuperscript{c}), whose "
               "per-molecule records this run did not regenerate"
               if any(r.get("provenance") == "carried" for r in rows) else "")
            + ". Bold marks the "
            "highest occlusion $\\rho$ per dataset (emphasis only).}")
    for pi, part in enumerate(parts):
        sub = [r for r in rows if r["dataset"] in part]
        suffix = "" if len(parts) == 1 else f", {pi + 1} of {len(parts)}"
        L = ["\\begin{sidewaystable*}[p]", "\\centering",
             "\\captionsetup{width=\\rotmaxw}",
             "\\caption{" + head + suffix + tail,
             "\\label{tab:molecular" + ("" if pi == 0 else chr(97 + pi)) + "}",
             "\\renewcommand{\\arraystretch}{1.15}",
             # Constrain BOTH dimensions. A rotated float has at most
             # \\textheight of width and \\textwidth of height; a width-only
             # \\resizebox scales a tall table *up* and runs it off the page.
             "\\adjustbox{max width=\\rotmaxw,max totalheight=\\rotmaxh}{%",
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
         "attribution--occlusion agreement is \\emph{negative}: the atoms an "
         "attributor ranks highest are not the atoms whose removal moves the "
         "prediction most. " + ", ".join(pos) + " run positive. Note "
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
