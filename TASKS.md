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
- [ ] Backbones: GCN, GAT, MPNN, AttentiveFP
- [ ] Attributors: GNNExplainer, PGExplainer, Grad-CAM, SubgraphX
- [ ] Datasets Tier-2: ESOL, FreeSolv, Lipophilicity, BBBP, BACE, Tox21
- [ ] Datasets Tier-3 (TDC): ClinTox, SIDER, DILI, hERG
- [ ] Cross-checkpoint stability, calibration linkage, regime stratification
- [ ] Paired statistics (Wilcoxon, bootstrap CIs, effect sizes)

## Milestone 5 — SOTA benchmarking & deliverables
- [ ] Reproduce GraphXAI / GraphFramEx / DIG / MolFaith metrics in-repo
- [ ] Head-to-head table
- [ ] `paper/OUTLINE.md` + related-work matrix
- [ ] Full README, LIMITATIONS.md

## Blockers / notes
- **BA-2Motifs**: PyG download source returns HTTP 403 in this environment.
  Loader + ground-truth extractor are implemented; blocked on data fetch only.
- ShapeGGen (GraphXAI) install may be heavy; treat as blocked-tolerant.
- TDC (PyTDC) not yet installed; wire in Milestone 4.
- MUTAG ground truth is a nitro-motif *proxy* (documented in LIMITATIONS.md),
  not annotator labels; exact GT comes from synthetic Tier-1 sets.
