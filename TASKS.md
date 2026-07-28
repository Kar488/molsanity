# TASKS.md — MolSanity task tracker

Status legend: `[ ]` todo · `[~]` in progress · `[x]` done · `[!]` blocked

> `RESULTS.md` holds only validated numbers. This file holds everything
> unfinished. Update continuously.

## Milestone 0 — Scaffold & environment
- [x] Create package layout (`molsanity/{data,models,attributors,audit,benchmark,viz}`)
- [x] `pyproject.toml`, `CLAUDE.md`, `TASKS.md`, `PROGRESS.md`
- [x] CI smoke workflow (`.github/workflows/pipeline.yml`)
- [x] Install CPU torch + torch-geometric + rdkit + captum stack

## Milestone 1 — Data (`molsanity.data`)
- [x] Manifest schema (loader, source, licence, cache path, checksum)
- [x] Idempotent caching + checksum verification + provenance logging
- [x] Wire Tier-1 MUTAG (PyG TUDataset) and verify a load
- [!] Wire BA-2Motifs — loader written + GT extractor ready, but the PyG source
      returns **HTTP 403** in this environment (network policy). Handled
      gracefully (skip+log); retry where the source is reachable.
- [x] Exact-GT synthetic Tier-1: **SynthMotifs** (BA base + house/cycle motif,
      generated offline via PyG ExplainerDataset). Replaces the 403-blocked
      BA-2Motifs for validating the audit against real ground truth.
- [ ] Wire ShapeGGen via GraphXAI (blocked-tolerant: skip+log if unavailable)
- [x] Bemis–Murcko scaffold split (deterministic) + random split reference

## Milestone 2 — First vertical slice (MUTAG)
- [x] GINE backbone (PyG) + training loop + checkpointing
- [x] Temperature-scaling calibration on validation
- [x] Integrated Gradients via Captum (`CaptumExplainer`) adapter
- [x] Uniform attribution schema (node/edge/motif)
- [x] RDKit motif decomposition (SSSR rings + Bemis–Murcko + fragments)
- [x] Audit metrics: GT accuracy (AUROC/AUPRC), coherence battery
- [x] Occlusion–attribution faithfulness (per-motif Δlogit, Spearman)
- [x] First real `RESULTS.md` row (MUTAG × GINE × IG)
- [x] Ground-truth validation figure (vector)

## Milestone 3 — Resumable pipeline
- [x] Staged runner with `.done` markers + config-hash idempotency
- [x] `configs/smoke.yaml` + `configs/full.yaml`
- [x] Run ledger + graceful per-cell failure
- [x] `python -m molsanity.run_all` entrypoint + `make all`

## Milestone 4 — Broaden matrix (after slice verified)
- [x] Backbones: GCN, GAT, MPNN, AttentiveFP (registry, shared forward)
- [x] Attributors: GNNExplainer + gradient family (Saliency, InputXGradient,
      GuidedBackprop, Deconvolution) via Captum adapter
- [x] Attributor PGExplainer: parametric explainer wrapped (trains a mask MLP on
      the training graphs; edge→node aggregation; BN-frozen model copy so training
      can't corrupt predictions; reproducible). Distinct profile: most faithful
      (occ≈0.93) yet near-chance GT on MUTAG, and does not flip on SynthMotifs.
- [!] Attributor SubgraphX: needs DIG, which is **not installed** here (blocked).
- [x] Datasets Tier-2: BBBP, BACE wired + verified (MoleculeNet). ESOL/FreeSolv/
      Lipophilicity are regression — need a regression head/metrics (future).
- [!] Datasets Tier-3 (TDC): ClinTox/SIDER/DILI/hERG — PyTDC not installed;
      loaders raise DatasetBlocked (skip+log). Tox21/SIDER are multi-task (future).
- [x] Cross-checkpoint stability, calibration linkage, regime stratification
- [x] Paired statistics (Wilcoxon, bootstrap CIs, fraction-positive)

## Milestone 5 — SOTA benchmarking & deliverables
- [x] Field-standard metrics (Fidelity± / sparsity) computed alongside MolSanity
      metrics on the same molecules (comparability)
- [ ] Reproduce full GraphXAI / GraphFramEx / DIG / MolFaith metric suites in-repo
- [x] Head-to-head table (`BENCHMARK.md`) + paired attributor comparisons
- [x] `paper/OUTLINE.md` + related-work matrix (`paper/RELATED_WORK.md`)
- [x] README, LIMITATIONS.md kept current with validated numbers

## Milestone 6 — Remaining for journal-ready
- [x] Regression datasets (ESOL/FreeSolv/Lipophilicity) + regression audit path
      (RMSE/MAE/R2 head, output-space occlusion; ESOL R2≈0.67, FreeSolv≈0.61)
- [ ] Multi-task datasets (Tox21, SIDER) label handling
- [ ] PGExplainer (parametric) + SubgraphX (needs DIG)
- [ ] ShapeGGen (GraphXAI) synthetic exact-GT
- [x] Publication figures: house style (validated CVD-safe palette, fixed entity
      colours, panel letters, inline labels); GT-by-attributor bars, faithfulness/
      stability ECDFs, regime stratification, and the signature attributor ×
      molecule/graph grid (RDKit skeletal + node-link, GT motif outlined)
- [ ] Full overnight `configs/full.yaml` run on GPU

## Blockers / notes
- **BA-2Motifs**: PyG download source returns HTTP 403 in this environment.
  Loader + ground-truth extractor are implemented; blocked on data fetch only.
- ShapeGGen (GraphXAI) install may be heavy; treat as blocked-tolerant.
- TDC (PyTDC) not yet installed; wire in Milestone 4.
- MUTAG ground truth is a nitro-motif *proxy* (documented in LIMITATIONS.md),
  not annotator labels; exact GT comes from synthetic Tier-1 sets.
