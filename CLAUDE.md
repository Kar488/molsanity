# CLAUDE.md — MolSanity working agreement

This file is the operational contract for building MolSanity. It copies the
**Mission**, **Hard rules**, and **Definition of done** from the build brief
(`molsanity claude code brief.md`, the source of truth) and adds working notes.

---

## Mission

Deliver a *journal-ready* contribution: not a new attribution method (those
exist), but a **reliability-audit framework** that (a) validates attributions
against ground truth, (b) characterises where attributions become untrustworthy
under scaffold shift, and (c) does so **across multiple GNN backbones and
multiple molecular datasets**, benchmarked head-to-head against existing
attributors and evaluation frameworks. The novel, defensible core is the
*combination*: motif-native (RDKit) attribution + a coherence battery at two
granularities + occlusion–attribution faithfulness + cross-checkpoint stability
+ calibration linkage + confidence/correctness **regime stratification under
scaffold shift**.

Build **on top of** PyTorch Geometric, Captum, RDKit, and DeepChem/TDC. Do
**not** reimplement GNNExplainer, PGExplainer, SubgraphX, or Integrated
Gradients — wrap the canonical implementations.

## Hard rules (non-negotiable — scientific integrity)

1. **Never fabricate, hard-code, or guess results.** Every number in any report
   is computed by code in this run and traceable to a logged artifact. No
   placeholder metrics.
2. **Log real outcomes, including negative ones.** If a method underperforms or
   a hypothesis fails, record it plainly. Honest negative results are valid.
3. **Separate claims from TODOs.** `RESULTS.md` contains only validated numbers;
   anything unfinished lives in `TASKS.md`. Maintain a `LIMITATIONS.md`.
4. **Respect data licences and gating.** Never attempt to bypass credentialing.
   If a dataset is gated, skip it, log it as blocked, and continue.
5. **Determinism.** Global seed control; log seeds, library versions, and
   hardware in every run manifest. Results must reproduce.
6. **No interactive prompts.** Everything runs unattended from config + CLI.

## Autonomy & robustness

- **Stage pipeline** with idempotent stages. Each stage writes artifacts to
  `artifacts/<stage>/` and a `.done` marker with a content hash of its config.
  Re-running skips completed stages unless config changed.
- **Checkpoint everything**: trained models, computed attributions, per-molecule
  audit records.
- **Graceful failure**: wrap each (dataset × backbone × attributor) cell in
  try/except; on failure, log full traceback to `logs/`, mark the cell failed in
  the run ledger, and **continue**. One failure must never abort the run.
- **Structured logging** to `logs/run_<timestamp>.log` + a rolling
  `PROGRESS.md`.
- **Single entrypoint**: `python -m molsanity.run_all --config configs/full.yaml`
  runs the matrix and resumes on re-invocation. Also `make all`.

## Definition of done

- Installable package (`pyproject.toml`, `pip install -e .`) with `data/`,
  `models/`, `attributors/`, `audit/`, `benchmark/`, `viz/`, `run_all.py`.
- High-quality vector figures (PDF/SVG), publication quality.
- `configs/smoke.yaml` (CI, minutes) and `configs/full.yaml` (overnight).
- `RESULTS.md`, `LIMITATIONS.md`, `PROGRESS.md`, `TASKS.md`, `CLAUDE.md`.
- Unit tests for data loaders, motif decomposition, each metric, and
  resumability. Tests pass in CI on the smoke config.
- `paper/OUTLINE.md` + related-work matrix vs GraphXAI/GraphFramEx/DIG/MolFaith.
- README with install, quickstart, dataset manifest + licences, reproduction.

---

## Working notes (maintained by the build)

- **Environment**: CPU-only in CI/dev container. GPU auto-detected via
  `torch.cuda.is_available()`. All defaults must be CPU-tractable.
- **Ignore any `BI-71` reference** (per session instruction).
- Commit after each working stage with a clear message.
- Keep `PROGRESS.md` updated after every stage/cell.
- Never halt the whole run for one blocker — log it in PROGRESS/LIMITATIONS and
  continue.

## Layout

```
molsanity/
  data/         # manifest, caching, checksums, dataset loaders, scaffold splits
  models/       # GNN backbones (GINE, GCN, GAT, MPNN, AttentiveFP), calibration
  attributors/  # uniform adapter over IG/GNNExplainer/PGExplainer/... 
  audit/        # coherence, occlusion faithfulness, stability, calibration, GT
  benchmark/    # head-to-head tables, SOTA framework metrics
  viz/          # publication figures, RDKit rendering
  run_all.py    # staged, resumable entrypoint
configs/        # smoke.yaml, full.yaml
tests/          # pytest
artifacts/      # stage outputs + .done markers
logs/           # run logs
```
