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
    n_classes = int(loaded.spec.extras.get("num_classes", 2))

    split = dataio.make_split(
        dataset, kind=split_kind,
        frac_train=cfg["split"]["frac_train"], frac_val=cfg["split"]["frac_val"],
        seed=cfg["seed"],
    )

    budget = cfg.get("budget", {})
    model_cfg = {**cfg["model"], "task": "graph-classification", "out_channels": n_classes}
    train_cfg = {**cfg["train"], "epochs": budget.get("epochs", 100)}
    epochs = train_cfg["epochs"]
    early_epoch = max(1, epochs // 5)  # early checkpoint for stability

    model, train_res = train_model(
        dataset, split, model_cfg, train_cfg,
        ckpt_dir=Path("artifacts/checkpoints") / dataset_name, seed=cfg["seed"],
        backbone=backbone, save_intermediate_epoch=early_epoch,
    )
    temperature = train_res.temperature

    attributor = build_attributor(
        attributor_name, model, ig_steps=budget.get("ig_steps", 25),
    )

    # Early-checkpoint model + attributor for cross-checkpoint stability.
    early_model = None
    early_attr = None
    if train_res.early_ckpt_path and Path(train_res.early_ckpt_path).exists():
        early_model = build_backbone(backbone, dataset[0], model_cfg)
        payload = torch.load(train_res.early_ckpt_path, map_location="cpu", weights_only=False)
        early_model.load_state_dict(payload["state_dict"])
        early_model.eval()
        early_attr = build_attributor(attributor_name, early_model, ig_steps=budget.get("ig_steps", 25))

    eval_idx = list(split.test)
    cap = budget.get("max_eval_molecules")
    if cap:
        eval_idx = eval_idx[:cap]

    records = []
    first_attribution = None
    for i in eval_idx:
        g = dataset[i]
        g.graph_id = i
        attribution = attributor.attribute(g)
        if first_attribution is None:
            first_attribution = attribution
        # Motif decomposition depends only on the molecule; compute once and
        # share it between the coherence/occlusion audit and the stability check.
        decomp = decompose(g)
        rec = audit_molecule(model, g, attribution, dataset_name,
                             temperature=temperature, decomp=decomp)
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
    blockers: list[str] = []
    rows: list[dict] = []

    from .data import DatasetBlocked

    for cell in cfg["cells"]:
        for split_kind in split_kinds:
            cell_id = f"{cell['dataset']}__{cell['backbone']}__{cell['attributor']}__{split_kind}"
            stage_cfg = {"cell": cell, "split": split_kind, "budget": cfg.get("budget"),
                         "model": cfg["model"], "train": cfg["train"], "seed": cfg["seed"]}
            try:
                res = stage(
                    f"cell_{cell_id}", stage_cfg,
                    lambda _out, c=cell, s=split_kind: run_cell(c, cfg, s, log, ts),
                )
                rows.append(res.payload["row"])
                detail = (f"acc={res.payload['row']['acc']:.2f} "
                          f"gt_auroc={res.payload['row'].get('gt_auroc')} "
                          f"n={res.payload['n_eval']}"
                          + (" (capped)" if res.payload.get("capped") else "")
                          + (" [cached]" if res.cached else ""))
                ledger.record({**cell, "split": split_kind}, "done", detail)
                log.info("[cell %s] DONE — %s", cell_id, detail)
            except (DatasetBlocked, NotImplementedError) as exc:
                ledger.record({**cell, "split": split_kind}, "skipped", str(exc))
                blockers.append(f"{cell_id}: {exc}")
                log.warning("[cell %s] SKIPPED — %s", cell_id, exc)
            except Exception as exc:  # noqa: BLE001 — graceful per-cell failure
                tb = traceback.format_exc()
                err_path = Path("logs") / f"error_{cell_id}_{ts}.log"
                err_path.parent.mkdir(parents=True, exist_ok=True)
                err_path.write_text(tb)
                ledger.record({**cell, "split": split_kind}, "failed", f"{exc} (see {err_path})")
                blockers.append(f"{cell_id}: FAILED {exc}")
                log.error("[cell %s] FAILED — %s (traceback -> %s)", cell_id, exc, err_path)

            # Update reports after EVERY cell (rolling, resumable).
            if rows:
                update_results_md(rows)
            update_progress_md(ledger, config_name, ts, blockers)

    # Head-to-head benchmark table over everything audited so far.
    try:
        from .benchmark import write_benchmark_md

        info = write_benchmark_md(seed=cfg["seed"])
        log.info("Wrote BENCHMARK.md (%s cells)", info.get("n_cells"))
    except Exception as exc:  # noqa: BLE001
        log.warning("Benchmark table generation failed: %s", exc)

    counts = ledger.counts()
    log.info("=== Run complete: %s ===", counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
