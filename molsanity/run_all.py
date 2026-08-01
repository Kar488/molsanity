"""Single entrypoint: staged, resumable audit matrix.

    python -m molsanity.run_all --config configs/smoke.yaml

Runs each (dataset × backbone × attributor) cell through: load → train →
attribute → audit → figure → RESULTS.md row. Each cell is wrapped so one failure
never aborts the run; failures are logged to ``logs/`` and marked in the ledger.
Re-invoking resumes: trained checkpoints and stage ``.done`` markers are reused.
"""
from __future__ import annotations

import argparse
import json
import time
import traceback
from dataclasses import asdict
from pathlib import Path

import yaml

from .pipeline import RunLedger, stage
from .reporting import results_row, update_progress_md, update_results_md
from .utils import RunManifest, get_logger, hash_config, set_global_seed, setup_logging


def _timestamp() -> str:
    # Wall clock is allowed here at the top-level entrypoint (not in hot paths).
    return time.strftime("%Y%m%d_%H%M%S", time.gmtime())


def _load_config(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text())


def _rationale_md(fp: dict) -> str:
    """RATIONALE_USE.md — the number that answers Faber et al. (KDD 2021).

    Their objection is that a low ground-truth AUROC may mean the model solved
    the task another way, so the attribution is describing the model correctly.
    Occluding the ground-truth substructure settles it per molecule.
    """
    def f(x, nd=3):
        try:
            v = float(x)
            return "n/a" if v != v else f"{v:.{nd}f}"
        except (TypeError, ValueError):
            return "n/a"

    return "\n".join([
        "# RATIONALE_USE.md — does the model actually read the ground truth?",
        "",
        "Faber et al. (KDD 2021) argue that scoring attributions against a known",
        "rationale misleads when the trained model did not use that rationale: a",
        "low GT AUROC would then be a fact about the model, not the explanation.",
        "This is testable. Occlude the ground-truth substructure; if the",
        "prediction collapses, the model *is* using it.",
        "",
        f"- molecules where the model reads the ground truth: "
        f"**{fp['n_uses_rationale']}**",
        f"- molecules where it does not (Faber applies): "
        f"**{fp['n_ignores_rationale']}**",
        f"- mean GT AUROC when the model reads it: "
        f"**{f(fp['mean_gt_auroc_when_used'])}**",
        f"- mean GT AUROC when it does not: "
        f"**{f(fp['mean_gt_auroc_when_ignored'])}**",
        "",
        "## The number that answers the objection",
        "",
        f"**{fp['n_anti_aligned_despite_model_using_it']}** molecules "
        f"({f(fp['frac_anti_aligned_despite_model_using_it'])} of those the model",
        "demonstrably reads the ground truth from) still receive an attribution",
        "anti-aligned with it. On those, no appeal to an alternative rationale",
        "explains the result: the attribution misdescribes a model that is",
        "provably using the substructure the attribution ranks lowest.",
        "",
    ])


# Attributors whose per-molecule cost justifies a worker pool. The gradient
# family runs in milliseconds, where process startup would dominate; SubgraphX
# is tens of seconds per molecule, where it is the difference between a four
# hour cell and a twenty hour one.
PARALLEL_ATTRIBUTORS = frozenset({"SubgraphX"})


def effective_budget(budget: dict | None, attributor: str) -> dict:
    """The budget as it applies to one attributor, with overrides resolved.

    Attributors differ by three orders of magnitude in cost: measured on 30-node
    SynthMotifs graphs, Integrated Gradients is milliseconds per molecule and
    SubgraphX is 28-38 seconds. A single ``max_eval_molecules`` is therefore the
    wrong shape -- a cap that is free for one is a twenty-hour job for the other
    -- so ``max_eval_molecules_<Attributor>`` overrides it for that attributor
    alone.

    Resolving the override *here*, rather than inside the cell, is what keeps
    the cache intact. The stage hash is taken over this dict, so a cell sees
    only the cap that applies to it: adding an override for SubgraphX leaves
    every other cell's hash byte-identical and its ``.done`` marker valid.
    """
    budget = dict(budget or {})
    prefix = "max_eval_molecules_"
    override = budget.pop(f"{prefix}{attributor}", None)
    for key in [k for k in budget if k.startswith(prefix)]:
        del budget[key]
    if override is not None:
        budget["max_eval_molecules"] = override
    return budget


def run_cell(cell: dict, cfg: dict, split_kind: str, log, ts: str) -> dict:
    """Run one audit cell end to end. Returns a dict with agg + train + row."""
    import torch

    from . import data as dataio
    from .attributors import build_attributor
    from .audit import aggregate_records, audit_molecule, cross_checkpoint_stability
    from .audit.motifs import decompose
    from .models import build_backbone, train_model
    from .viz import ground_truth_validation_figure, molecule_attribution_svg

    dataset_name = cell["dataset"]
    backbone = cell["backbone"]
    attributor_name = cell["attributor"]
    cell_id = f"{dataset_name}__{backbone}__{attributor_name}__{split_kind}"

    loaded = dataio.load_dataset(dataset_name)  # raises DatasetBlocked -> skipped
    dataset = loaded.dataset
    task = loaded.spec.task
    n_out = 1 if task == "graph-regression" else int(loaded.spec.extras.get("num_classes", 2))

    # For classification, pass labels so the scaffold split guarantees every fold
    # contains every class (imbalanced datasets otherwise yield single-class folds).
    labels = None
    if task == "graph-classification":
        labels = [int(dataset[i].y.view(-1)[0]) for i in range(len(dataset))]
    split = dataio.make_split(
        dataset, kind=split_kind,
        frac_train=cfg["split"]["frac_train"], frac_val=cfg["split"]["frac_val"],
        seed=cfg["seed"], labels=labels,
    )

    budget = cfg.get("budget", {})
    model_cfg = {**cfg["model"], "task": task, "out_channels": n_out}
    train_cfg = {**cfg["train"], "epochs": budget.get("epochs", 100)}
    epochs = train_cfg["epochs"]
    early_epoch = max(1, epochs // 5)  # early checkpoint for stability

    model, train_res = train_model(
        dataset, split, model_cfg, train_cfg,
        ckpt_dir=Path("artifacts/checkpoints") / dataset_name, seed=cfg["seed"],
        backbone=backbone, save_intermediate_epoch=early_epoch,
    )
    temperature = train_res.temperature

    # PGExplainer is parametric and needs the training graphs to fit its mask MLP.
    train_graphs = [dataset[i] for i in split.train] if attributor_name == "PGExplainer" else None
    # Manifold-respecting occlusion baseline, computed on the TRAINING split
    # only so the counterfactual carries no information from the audited
    # molecules. Zeroing a node's features takes the graph off the data
    # manifold; replacing them with the training mean keeps a removed node
    # looking like a plausible but uninformative one. Both are recorded, so the
    # off-manifold caveat is measurable rather than only stated.
    from .audit.occlusion import dataset_feature_mean

    occ_baseline = dataset_feature_mean(dataset, split.train)

    attributor = build_attributor(
        attributor_name, model, task=task, ig_steps=budget.get("ig_steps", 25),
        train_graphs=train_graphs, pg_epochs=budget.get("pg_epochs", 30),
        sgx_max_nodes=budget.get("sgx_max_nodes", 8),
        sgx_rollouts=budget.get("sgx_rollouts", 20),
        seed=cfg["seed"],
    )
    # SubgraphX rebuilds the graph on every rollout, so it needs to know the
    # edge-feature width to regenerate edge_attr for a perturbed edge set.
    if hasattr(attributor, "edge_dim"):
        probe = dataset[0]
        attributor.edge_dim = (probe.edge_attr.size(1)
                               if probe.edge_attr is not None else 1)

    # Early-checkpoint model + attributor for cross-checkpoint stability.
    early_model = None
    early_attr = None
    if train_res.early_ckpt_path and Path(train_res.early_ckpt_path).exists():
        early_model = build_backbone(backbone, dataset[0], model_cfg)
        payload = torch.load(train_res.early_ckpt_path, map_location="cpu", weights_only=False)
        early_model.load_state_dict(payload["state_dict"])
        early_model.eval()
        early_attr = build_attributor(
            attributor_name, early_model, task=task,
            ig_steps=budget.get("ig_steps", 25),
            train_graphs=train_graphs, pg_epochs=budget.get("pg_epochs", 30),
            seed=cfg["seed"],
        )

    eval_idx = list(split.test)
    # The per-attributor cap has already been resolved into this budget by
    # effective_budget(), so that a cell's stage hash reflects only the cap that
    # applies to it and adding an override for one attributor does not
    # invalidate every other cell's cache.
    cap = budget.get("max_eval_molecules")
    if cap:
        eval_idx = eval_idx[:cap]
    log.info("[cell %s] auditing %d molecules%s", cell_id, len(eval_idx),
             f" (capped from {len(split.test)})" if cap and len(split.test) > cap
             else "")

    # Attribution is the expensive half for the search-based attributors and is
    # embarrassingly parallel, so it can be lifted out of the audit loop and run
    # across processes. Only worth it where a molecule costs seconds: below the
    # threshold the pool costs more than it saves, and the serial path is used.
    from .audit.parallel import parallel_attributions, resolve_workers

    n_workers = resolve_workers(
        budget.get("attribution_workers") if attributor_name in PARALLEL_ATTRIBUTORS
        else None,
        len(eval_idx))
    precomputed = None
    if n_workers > 1:
        # CUDA cannot survive fork, and the GPU was not helping these
        # attributors anyway: the cost is Python dispatch, not arithmetic.
        model.to("cpu")
        if hasattr(attributor, "model"):
            attributor.model = model
        attributor._explainer = getattr(attributor, "_explainer", None)
        log.info("[cell %s] attributing on %d worker processes (CPU)",
                 cell_id, n_workers)
        t_par = time.time()
        precomputed = parallel_attributions(attributor, dataset, eval_idx,
                                            n_workers)
        log.info("[cell %s] attribution done in %.1f min (%.1fs per molecule)",
                 cell_id, (time.time() - t_par) / 60,
                 (time.time() - t_par) / max(1, len(eval_idx)))

    records = []
    first_attribution = None
    # A cell that prints nothing for twenty minutes is indistinguishable from a
    # crash, and SubgraphX takes seconds per molecule. The heartbeat is by
    # elapsed time rather than every N molecules so that fast attributors stay
    # quiet and slow ones report often enough to be trusted.
    HEARTBEAT_S = 60.0
    t_cell = time.time()
    t_beat = t_cell
    for n_done, i in enumerate(eval_idx, 1):
        g = dataset[i]
        g.graph_id = i
        attribution = (precomputed[n_done - 1] if precomputed is not None
                       else attributor.attribute(g))
        now = time.time()
        if now - t_beat >= HEARTBEAT_S:
            rate = (now - t_cell) / n_done
            left = rate * (len(eval_idx) - n_done)
            log.info("[cell %s] %d/%d molecules (%.1fs each, ~%.0f min left)",
                     cell_id, n_done, len(eval_idx), rate, left / 60)
            t_beat = now
        if first_attribution is None:
            first_attribution = attribution
        # Motif decomposition depends only on the molecule; compute once and
        # share it between the coherence/occlusion audit and the stability check.
        decomp = decompose(g)
        rec = audit_molecule(model, g, attribution, dataset_name,
                             temperature=temperature, decomp=decomp, task=task,
                             occ_baseline=occ_baseline)
        if early_attr is not None:
            try:
                rec.stability = cross_checkpoint_stability(
                    early_attr, g, decomp, attribution.node_attr
                )
            except Exception:
                pass
        records.append(rec)

    agg = aggregate_records(records, seed=cfg["seed"])

    # --- Figures (GT validation + one case-study molecule) ---
    fig_dir = Path("artifacts") / "figures" / cell_id
    fig_info = ground_truth_validation_figure(
        records, fig_dir / "gt_validation",
        title=f"{dataset_name} · {backbone} · {attributor_name} ({split_kind} split)",
    )
    if eval_idx and first_attribution is not None:
        g0 = dataset[eval_idx[0]]
        g0.graph_id = eval_idx[0]
        gt0 = dataio.ground_truth_mask(dataset_name, g0)  # reuse loop's attribution
        molecule_attribution_svg(
            g0, first_attribution.node_attr, fig_dir / "case_molecule.svg", gt_mask=gt0,
        )

    row = results_row(cell, agg, train_res.__dict__, split_kind)

    # Persist per-cell audit records + aggregate.
    rec_dir = Path("artifacts") / "audit" / cell_id
    rec_dir.mkdir(parents=True, exist_ok=True)
    (rec_dir / "records.json").write_text(
        json.dumps([asdict(r) for r in records], indent=2, default=str)
    )
    (rec_dir / "aggregate.json").write_text(json.dumps(agg, indent=2, default=str))

    return {"agg": agg, "train": train_res.__dict__, "row": row, "fig": fig_info,
            "n_eval": len(eval_idx), "capped": bool(cap)}


def preflight(cfg, log) -> list[str]:
    """Check the installed stack against the attributors the config asks for.

    A dependency can be importable and still be wrong. The first full sweep ran
    for six hours and returned 204 failed Integrated Gradients cells because
    installing DIG for SubgraphX had quietly downgraded Captum to the 0.2.0 it
    pins, and Captum 0.2 is incompatible with the PyG ``CaptumExplainer`` this
    project uses. Nothing detected it: every cell failed, was logged, and the
    run continued exactly as designed.

    Returns a list of warnings, logged loudly at the start of the run. This
    does not abort — a broken optional attributor should still leave the rest
    of the matrix runnable, which is the whole point of the graceful-failure
    policy — but it must not be discovered afterwards.
    """
    wanted = {c.get("attributor") for c in cfg.get("cells", [])}
    warnings: list[str] = []

    if wanted & {"IntegratedGradients", "Saliency", "InputXGradient",
                 "GuidedBackprop", "Deconvolution"}:
        try:
            import captum

            major, minor = (int(v) for v in captum.__version__.split(".")[:2])
            if (major, minor) < (0, 7):
                warnings.append(
                    f"captum {captum.__version__} is too old for PyG's "
                    "CaptumExplainer. Every IntegratedGradients cell will fail "
                    "with 'IndexError: index 1 is out of bounds'. This is what "
                    "'pip install dive-into-graphs' does if run without "
                    "--no-deps. Fix: pip install -U 'captum>=0.7'.")
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"captum unavailable ({exc}); gradient attributors "
                            "will be skipped.")

    if "SubgraphX" in wanted:
        try:
            from .attributors.subgraphx import _import_subgraphx

            _import_subgraphx()
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"SubgraphX unavailable ({type(exc).__name__}: "
                            f"{exc}); its cells will be skipped and logged.")

    for w in warnings:
        log.warning("PREFLIGHT: %s", w)
    if not warnings:
        log.info("Preflight: attributor dependencies OK.")
    return warnings


def main(argv=None):
    parser = argparse.ArgumentParser(description="MolSanity audit matrix runner")
    parser.add_argument("--config", required=True)
    parser.add_argument("--budget", default=None, help="override: epochs,ig_steps")
    args = parser.parse_args(argv)

    ts = _timestamp()
    log = setup_logging(timestamp=ts)
    cfg = _load_config(args.config)
    set_global_seed(cfg.get("seed", 0))

    config_name = Path(args.config).name
    log.info("=== MolSanity run: %s (seed=%d) ===", config_name, cfg.get("seed", 0))

    RunManifest(
        seed=cfg.get("seed", 0), config_hash=hash_config(cfg), timestamp=ts,
        extra={"config_name": config_name},
    ).write(Path("artifacts") / "run_manifest.json")

    split_kinds = [cfg["split"]["kind"]] + list(cfg.get("extra_splits", []))
    ledger = RunLedger()
    blockers: list[str] = list(preflight(cfg, log))
    rows: list[dict] = []

    from .data import DatasetBlocked

    # A run may repeat the whole matrix under several seeds so that split and
    # initialisation variance is measured rather than assumed away.
    seeds = [int(v) for v in (cfg.get("seeds") or [cfg.get("seed", 0)])]
    multi_seed = len(seeds) > 1
    log.info("Seeds: %s", seeds)

    for cell in cfg["cells"]:
        # A cell may pin its own split(s) (e.g. a random-split reference row);
        # otherwise it runs on the config's split list.
        cell_splits = cell.get("splits") or ([cell["split"]] if cell.get("split") else split_kinds)
        for split_kind in cell_splits:
            for seed in seeds:
                cfg_seed = {**cfg, "seed": seed}
                set_global_seed(seed)
                base_id = (f"{cell['dataset']}__{cell['backbone']}"
                           f"__{cell['attributor']}__{split_kind}")
                # Single-seed configs keep the old stage identifier, so cells
                # cached by an earlier run stay cached instead of silently
                # re-running.
                cell_id = f"{base_id}__seed{seed}" if multi_seed else base_id
                eff = effective_budget(cfg.get("budget"), cell["attributor"])
                cfg_seed = {**cfg_seed, "budget": eff}
                stage_cfg = {"cell": cell, "split": split_kind, "budget": eff,
                             "model": cfg["model"], "train": cfg["train"], "seed": seed}
                try:
                    res = stage(
                        f"cell_{cell_id}", stage_cfg,
                        lambda _out, c=cell, s=split_kind, cs=cfg_seed:
                            run_cell(c, cs, s, log, ts),
                    )
                    # Rebuild the row from the stored agg + train payload so newly
                    # added columns (e.g. test AUC) populate for cached cells too.
                    row = results_row(cell, res.payload["agg"],
                                      res.payload["train"], split_kind)
                    row["seed"] = seed
                    rows.append(row)
                    if row.get("task") == "graph-regression":
                        headline = f"rmse={row.get('rmse'):.3f} r2={res.payload['train'].get('test_r2'):.3f}"
                    else:
                        headline = f"acc={row['acc']:.2f} gt_auroc={row.get('gt_auroc')}"
                    detail = (f"{headline} n={res.payload['n_eval']}"
                              + (" (capped)" if res.payload.get("capped") else "")
                              + (" [cached]" if res.cached else ""))
                    ledger.record({**cell, "split": split_kind, "seed": seed}, "done", detail)
                    log.info("[cell %s] DONE — %s", cell_id, detail)
                except (DatasetBlocked, NotImplementedError) as exc:
                    ledger.record({**cell, "split": split_kind, "seed": seed}, "skipped", str(exc))
                    blockers.append(f"{cell_id}: {exc}")
                    log.warning("[cell %s] SKIPPED — %s", cell_id, exc)
                except Exception as exc:  # noqa: BLE001 — graceful per-cell failure
                    tb = traceback.format_exc()
                    err_path = Path("logs") / f"error_{cell_id}_{ts}.log"
                    err_path.parent.mkdir(parents=True, exist_ok=True)
                    err_path.write_text(tb)
                    ledger.record({**cell, "split": split_kind, "seed": seed}, "failed", f"{exc} (see {err_path})")
                    blockers.append(f"{cell_id}: FAILED {exc}")
                    log.error("[cell %s] FAILED — %s (traceback -> %s)", cell_id, exc, err_path)

                # Update reports after EVERY cell (rolling, resumable).
                if rows:
                    update_results_md(rows)
                update_progress_md(ledger, config_name, ts, blockers)

    # Across-seed spread, so a reported effect can be compared against the
    # variance of re-running the same cell.
    try:
        from .benchmark.seed_variance import write_seed_variance_md

        sv = write_seed_variance_md(rows)
        log.info("Wrote SEED_VARIANCE.md (%d multi-seed cells)", sv["n_cells"])
    except Exception as exc:  # noqa: BLE001
        log.warning("Seed-variance report failed: %s", exc)

    # When should an attribution not be trusted? Coverage-reliability curves
    # over the pooled per-molecule records, plus the partition that answers the
    # Faber objection directly.
    try:
        from .audit.abstention import load_all_records, write_abstention_md
        from .audit.rationale import faber_partition

        all_recs = load_all_records()
        ab = write_abstention_md(all_recs)
        log.info("Wrote ABSTENTION.md (%d signals ranked over %d records)",
                 ab["n_signals"], len(all_recs))

        fp = faber_partition(all_recs)
        Path("RATIONALE_USE.md").write_text(_rationale_md(fp))
        log.info("Wrote RATIONALE_USE.md (%d molecules where the model reads "
                 "the ground truth, %d anti-aligned despite that)",
                 fp["n_uses_rationale"],
                 fp["n_anti_aligned_despite_model_using_it"])
    except Exception as exc:  # noqa: BLE001
        log.warning("Abstention/rationale reports failed: %s", exc)

    # Head-to-head benchmark table over everything audited so far.
    try:
        from .benchmark import write_benchmark_md

        info = write_benchmark_md(seed=cfg["seed"])
        log.info("Wrote BENCHMARK.md (%s cells)", info.get("n_cells"))
    except Exception as exc:  # noqa: BLE001
        log.warning("Benchmark table generation failed: %s", exc)

    # Faithfulness-only-vs-ground-truth selection test (in-distribution vs shift).
    # Only writes if the referenced GT cells have been audited; skips quietly.
    try:
        from .benchmark.faithfulness_vs_truth import write_report

        write_report(seed=cfg["seed"])
        log.info("Wrote BENCHMARK_GT.md (faithfulness-vs-ground-truth)")
    except Exception as exc:  # noqa: BLE001
        log.warning("BENCHMARK_GT generation failed: %s", exc)

    # Cross-matrix publication figures (GT bar, faithfulness/stability ECDFs, regimes).
    try:
        from .viz import make_summary_figures

        made = make_summary_figures()
        log.info("Wrote %d summary figure(s)", len(made))
    except Exception as exc:  # noqa: BLE001
        log.warning("Summary figure generation failed: %s", exc)

    # Capstone figure: faithfulness-vs-truth dissociation across the two regimes.
    try:
        from .viz.dissociation import make_dissociation_figure

        make_dissociation_figure("artifacts/figures/_summary/dissociation")
        log.info("Wrote dissociation figure")
    except Exception as exc:  # noqa: BLE001
        log.warning("Dissociation figure generation failed: %s", exc)

    # Mirror every figure into the tracked, browsable figures/ folder + INDEX.md.
    try:
        from .viz.collect import collect_figures

        info = collect_figures()
        log.info("Collected figures -> figures/ (%d files, %d cells)",
                 info["scanned"], info["n_cells"])
    except Exception as exc:  # noqa: BLE001
        log.warning("Figure collection failed: %s", exc)

    counts = ledger.counts()
    log.info("=== Run complete: %s ===", counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
