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
- [!] Attributor SubgraphX: DIG installs but **cannot import** here — it needs the
      pre-2.5 PyG `torch_sparse` compiled extension, which has no wheel for torch
      2.13 and won't build. Adapter slot stays blocked-tolerant (KeyError note).
- [x] Datasets Tier-2: BBBP, BACE (classification) + ESOL/FreeSolv/Lipophilicity
      (regression) wired, audited on non-degenerate models (BBBP AUC 0.81/0.89).
- [x] Datasets Tier-3: ClinTox (AUC 0.82), SIDER, Tox21 rehomed to MoleculeNet as
      single-task views. **DILI/hERG now wired via PyTDC** (`_load_tdc`,
      `from_smiles` featurisation): DILI GINE acc 0.80/AUC 0.82 (balanced),
      hERG GCN acc 0.90/AUC 0.80 (and notably faithful, occ_spearman 0.71).
- [x] Cross-checkpoint stability, calibration linkage, regime stratification
- [x] Paired statistics (Wilcoxon, bootstrap CIs, fraction-positive)

## Milestone 5 — SOTA benchmarking & deliverables
- [x] Field-standard metrics (Fidelity± / sparsity) + **GraphFramEx characterization
      score** computed alongside MolSanity metrics on the same molecules
- [ ] Reproduce full GraphXAI / DIG / MolFaith metric suites in-repo (PyG
      `unfaithfulness` available; wiring it per-cell is the remaining piece)
- [x] Head-to-head table (`BENCHMARK.md`) + paired attributor comparisons
- [x] `paper/OUTLINE.md` + related-work matrix (`paper/RELATED_WORK.md`)
- [x] README, LIMITATIONS.md kept current with validated numbers

## Milestone 6 — Remaining for journal-ready
- [x] Regression datasets (ESOL/FreeSolv/Lipophilicity) + regression audit path
      (RMSE/MAE/R2 head, output-space occlusion; ESOL R2≈0.67–0.69 across
      GINE/GCN/GAT, FreeSolv≈0.61, Lipophilicity≈0.40)
- [x] Class-aware scaffold split: guarantees every fold has every class (moves
      whole scaffold groups, no leakage) — fixes degenerate imbalanced Tier-2
- [x] Multi-task datasets (Tox21, SIDER): single-task views (task 0), NaN-filtered,
      SMILES-retained; loadable via MoleculeNet (no TDC needed)
- [x] PGExplainer (parametric) wired; SubgraphX still needs DIG (blocked)
- [x] Class-weighted loss + AUC model-selection (opt-in) for imbalanced Tier-2/3
- [x] Random-split (in-distribution) references alongside scaffold shift
- [x] `configs/full.yaml` = complete overnight sweep (44 cells × 2 splits)
- [x] DILI/hERG (Therapeutics Data Commons) wired via PyTDC — see Milestone 4.
- [x] **Scaled-out matrix (CPU): 75 audit rows.** Full gradient battery
      (Saliency/InputXGradient/GuidedBackprop) + GNNExplainer/PGExplainer on the
      real molecular Tier-2/3 sets (BBBP/BACE/SIDER/ClinTox/DILI/hERG), the
      **regression** sets (ESOL/FreeSolv/Lipophilicity — where occlusion
      faithfulness is consistently *negative* across attributors, ≈ −0.15 to
      −0.80), and SynthMotifs exact-GT across GCN/GAT/MPNN/AttentiveFP. Attributor-
      adds reuse the committed backbone checkpoints (no retraining).
- [x] **Tox21 (single-task NR-AR): audited on CPU** — 7.3k molecules, ~4%
      positive; class-weighted GINE reaches test AUC 0.83. Gradient attributors
      are anti-faithful here too (occ ≈ −0.34 to −0.41), GNNExplainer ≈ chance.
- [x] **Fix:** gradient attributors on integer-featured data (MoleculeNet/TDC)
      failed ("differentiated Tensor does not require grad") — the model casts
      x→float *inside* forward, so Captum's leaf tensor was int. Now the explainer
      is fed float inputs (identity for already-float MUTAG/SynthMotifs, so those
      results are unchanged). Unblocks the battery on all molecular datasets.
- [x] **Head-to-head with statistical significance (the SOTA-comparison claim).**
      `BENCHMARK_GT.md` + `benchmark/faithfulness_vs_truth.py`: on exact/proxy
      ground truth, test whether a faithfulness-only ranking (GraphFramEx
      Fidelity+/characterisation) selects the GT-best attributor. Result:
      *in-distribution* it does (SynthMotifsXL n≈120, rank corr ρ≈0.77–0.94, no
      mismatch); *under scaffold shift* it does NOT — characterisation picks
      Saliency (GT 0.03), Fidelity+ picks GuidedBackprop (0.11) vs GT-best IG
      (0.54), paired Wilcoxon p<0.001, ρ collapses to ≈−0.4. Added SynthMotifsXL
      (600-graph exact-GT twin) for the powered in-distribution arm.
- [ ] Overnight `full.yaml` run on GPU for publication scale (higher epochs /
      IG steps / eval-molecule caps; Tox21 already audited on CPU above). Would
      also power the *shift* arm of BENCHMARK_GT beyond MUTAG's n≈20.
- [!] ShapeGGen (GraphXAI) synthetic exact-GT — GraphXAI's PyPI/GitHub install is
      broken here (wheel omits subpackages) and depends on the same pre-2.5 PyG
      stack as DIG. Its exact-GT role is already filled by SynthMotifs, so this is
      redundant, not a gap.
- [x] Publication figures: house style (validated CVD-safe palette, fixed entity
      colours, panel letters, inline labels); GT-by-attributor bars, faithfulness/
      stability ECDFs, regime stratification, and the signature attributor ×
      molecule/graph grid (RDKit skeletal + node-link, GT motif outlined)
- [ ] Full overnight `configs/full.yaml` run on GPU

## Blockers / notes
- **BA-2Motifs**: PyG download source returns HTTP 403 in this environment.
  Loader + ground-truth extractor are implemented; blocked on data fetch only.
- **SubgraphX (DIG) / ShapeGGen (GraphXAI)**: both need the pre-2.5 PyG
  `torch_sparse`/`torch_scatter` compiled extensions; no wheel exists for the
  torch 2.13 here and source builds hang/fail. DIG installs but can't import;
  GraphXAI's wheel is broken. Kept blocked-tolerant; ShapeGGen's exact-GT role is
  covered by SynthMotifs.
- **TDC (PyTDC)**: installed and wired (DILI, hERG). Install needs a minimal
  footprint (`pip install --no-deps PyTDC` + `huggingface_hub`/`httpx`) because
  the full dependency set conflicts with the pinned numpy/rdkit here.
- MUTAG ground truth is a nitro-motif *proxy* (documented in LIMITATIONS.md),
  not annotator labels; exact GT comes from synthetic Tier-1 sets.
