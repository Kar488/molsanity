# MolSanity

**A reliability-audit framework for feature attributions on molecular graph
neural networks (GNNs) under scaffold shift.**

MolSanity does not propose a new attribution method. It audits *existing* ones —
Integrated Gradients, GNNExplainer, PGExplainer, Grad-CAM, SubgraphX — by asking
a different question: **when, and where, do molecular GNN attributions stop being
trustworthy under distribution (scaffold) shift?** It combines motif-native
(RDKit) attribution, a coherence battery, occlusion–attribution faithfulness,
cross-checkpoint stability, calibration linkage, and confidence/correctness
regime stratification, benchmarked head-to-head against GraphXAI, GraphFramEx,
DIG, and MolFaith.

Built **on top of** PyTorch Geometric, Captum, and RDKit — canonical
implementations are wrapped, never reimplemented.

> Status: **audit matrix live** — 5 backbones (GINE/GCN/GAT/MPNN/AttentiveFP) ×
> 6 attributors (IG/Saliency/InputXGradient/GuidedBackprop/GNNExplainer/PGExplainer)
> × Tier-1 exact-GT (SynthMotifs) + quasi-GT (MUTAG) + Tier-2 classification &
> **regression** (BBBP/ESOL/FreeSolv/Lipophilicity), with validated numbers in
> [`RESULTS.md`](RESULTS.md), a head-to-head [`BENCHMARK.md`](BENCHMARK.md), and
> publication figures in [`results_figures/`](results_figures/). See
> [`TASKS.md`](TASKS.md) for what remains.

## Install

```bash
# CPU stack (CI / laptop)
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -e ".[dev]"
pip install torch-geometric captum rdkit
# or:  make install-graph
```

GPU is auto-detected via `torch.cuda.is_available()`; all defaults are
CPU-tractable.

## Quickstart

```bash
# Tiny, honest end-to-end slice (minutes). Resumable: re-run to continue.
python -m molsanity.run_all --config configs/smoke.yaml
#   → RESULTS.md row + artifacts/figures/.../gt_validation.pdf

# Overnight matrix (broadens as backbones/datasets are wired in).
python -m molsanity.run_all --config configs/full.yaml   # or: make all

pytest -q          # unit tests (loaders, motifs, metrics, resumability)
```

Every run writes a manifest (`artifacts/run_manifest.json`) with seed, library
versions, git rev, and hardware for reproducibility. Stages are idempotent: each
writes a `.done` marker with a config hash, so finished work is never redone.

## Headline result — **faithfulness is not correctness**

MolSanity's central distinction is that an attribution can faithfully track the
model yet fail to recover the true motif. On MUTAG under a **scaffold split**
(numbers below are from `configs/matrix.yaml`, a reduced-budget run — all in
[`RESULTS.md`](RESULTS.md) / [`BENCHMARK.md`](BENCHMARK.md)):

- **Attributor choice changes ground-truth localisation by >0.5 AUROC at
  near-equal faithfulness.** On GINE, Saliency and InputXGradient are *faithful*
  (occlusion Spearman ≈ 0.38 / 0.40) yet strongly **anti-aligned with the nitro
  ground truth** (GT AUROC ≈ **0.03 / 0.04**, chance = 0.5) — faithful-but-wrong.
  Integrated Gradients (0.54) and GNNExplainer (0.49) recover the motif far
  better at similar faithfulness. A faithfulness-only benchmark would rate all
  four as fine; MolSanity's ground-truth view separates them.
- **Backbone matters too.** With IG, ground-truth localisation ranges from GINE
  0.54 → MPNN 0.36 → GCN 0.20 → GAT/AttentiveFP ≈ 0.13 (anti-aligned); AttentiveFP
  is even *anti-faithful* (occlusion ≈ −0.88). Reliability is model-dependent.
  On **SynthMotifs** (with *exact* node ground truth) the same backbone spread is
  confirmed at IG: GCN **0.92** > AttentiveFP 0.82 ≈ MPNN 0.81 > GAT 0.72 > GINE —
  i.e. the "best" backbone for attribution reliability is itself dataset-dependent,
  now shown against exact truth, not a proxy.
- **The attributor ranking flips with the regime.** On **SynthMotifs** (a
  synthetic Tier-1 task with *exact* node ground truth, where GINE hits 100 %
  test accuracy and provably uses the motif), Saliency localises the motif almost
  perfectly (GT AUROC **0.98**), IG 0.74, GNNExplainer 0.50 (chance) — the
  *opposite* order to MUTAG under scaffold shift, where Saliency was worst (0.03).
  No single attributor is "best"; reliability is regime-dependent, which is
  exactly what the audit is built to surface.

See the ground-truth validation figure under `results_figures/` and
`artifacts/figures/`. (MUTAG's motif "ground truth" is a chemically motivated
nitro-group *proxy*, clearly labelled as such — see
[`LIMITATIONS.md`](LIMITATIONS.md). Exact ground truth comes from the synthetic
Tier-1 sets.)

## Dataset manifest & licences

`molsanity.data` holds the manifest (loader, source, licence, cache path,
checksum). Provenance is logged per dataset to `data/<name>/provenance.json`.

| Tier | Datasets | Source | Status |
|------|----------|--------|--------|
| 1 | **SynthMotifs** (exact GT), **MUTAG** (proxy GT) | generated offline / PyG | ✅ audited |
| 1 | BA-2Motifs, ShapeGGen | PyG download / GraphXAI | ⚠ skip+log (unreachable here) |
| 2 | **BBBP, BACE** (classification); **ESOL, FreeSolv, Lipophilicity** (regression) | MoleculeNet (PyG) | ✅ audited |
| 2 | Tox21 | MoleculeNet (PyG) | ✅ loadable (single-task); deferred to overnight (5.8k) |
| 3 | **ClinTox** (clinical-trial toxicity), **SIDER** (side effects) | MoleculeNet single-task views | ✅ audited |
| 3 | **DILI** (drug-induced liver injury), **hERG** (cardiotoxicity) | Therapeutics Data Commons (PyTDC) | ✅ audited |

Multi-task panels (Tox21 12-task, SIDER 27-task, ClinTox 2-task) are audited as
single-task binary views. Imbalanced classification uses a **class-aware scaffold
split** + inverse-frequency weighting so folds aren't single-class. TDC sets are
featurised with the same PyG `from_smiles` encoding as MoleculeNet (x: 9-dim,
edge_attr: 3-dim), so the backbones are drop-in; install with `pip install -e
'.[tdc]'`. Credential-gated ICU/EHR modalities (MIMIC, eICU, HiRID,
AmsterdamUMCdb) are **out of scope**: referencing them is a no-op (skipped +
logged), never a bypass attempt (Hard Rule 4).

Two synthetic/attributor extensions stay **honestly blocked** in this
environment (logged in [`LIMITATIONS.md`](LIMITATIONS.md), not silently dropped):
**SubgraphX** (DIG) and **ShapeGGen** (GraphXAI) both depend on the pre-2.5 PyG
ecosystem (`torch_sparse`/`torch_scatter` compiled extensions), which has no wheel
for the torch 2.13 here; DIG installs but cannot import, and GraphXAI's exact-GT
role is already covered by the offline **SynthMotifs** generator.

## Layout

```
molsanity/
  data/         manifest, caching, checksums, MUTAG/BA-2Motifs loaders,
                RDKit reconstruction, scaffold splits, ground-truth masks
  models/       GINE backbone, training + checkpointing, temperature scaling
  attributors/  uniform Attribution schema; Integrated Gradients (Captum/PyG)
  audit/        coherence battery, occlusion faithfulness, GT scoring, stats
  viz/          publication figures + RDKit molecule rendering
  run_all.py    staged, resumable entrypoint
configs/        smoke.yaml (CI) · full.yaml (overnight)
```

## Reproduction

Results are deterministic given the seed in the config. To reproduce the slice:
`python -m molsanity.run_all --config configs/smoke.yaml`. The CI workflow
(`.github/workflows/pipeline.yml`) runs the smoke config + tests on every push.

### Pretrained checkpoints (resume / rerun without retraining)

The trained GNN backbones behind every featured `RESULTS.md` row are committed
under [`artifacts/checkpoints/`](artifacts/checkpoints/) — 22 models (classification
+ regression) plus their `_early` intermediates (used by the cross-checkpoint
stability metric). They are the only part of `artifacts/` kept in git; everything
else there regenerates cheaply. An index with each model's real held-out metrics
is in [`artifacts/checkpoints/MANIFEST.md`](artifacts/checkpoints/MANIFEST.md),
regenerated by:

```bash
python -m molsanity.models.checkpoint_manifest
```

**How resume works.** Each checkpoint is named `<backbone>_<config_hash>.pt`,
where `config_hash` is a content hash of `{model, train, split, seed, backbone}`.
When you re-run `run_all`, it recomputes that hash per cell; if the matching
checkpoint exists it is **loaded instead of retrained** (see
`molsanity/models/train.py`). So on a fresh clone, the committed `RESULTS.md`
regenerates from the committed weights with **no training** — only the cheap,
deterministic attribution + audit stages re-run:

```bash
# 1) Tier-1 (MUTAG/SynthMotifs) + regression + a first pass at the imbalanced sets.
python -m molsanity.run_all --config configs/matrix.yaml
# 2) Class-weighted 60-epoch models for the imbalanced Tier-2/3 sets. Run this
#    SECOND: it owns the BBBP/BACE/SIDER/ClinTox rows (same cell keys as matrix,
#    but the class-aware split + inverse-frequency weighting is the honest model —
#    matrix's unweighted 30-epoch pass collapses to the majority class on these).
python -m molsanity.run_all --config configs/tier2.yaml
```

Both configs' checkpoints are committed, so both passes are 0-retrain. The
ordering matters only because `RESULTS.md` keys rows by
`dataset × backbone × attributor × split`, and the last writer wins; the two
committed checkpoints for those cells (e.g. BBBP GINE: unweighted 30-epoch vs
class-weighted 60-epoch) are both present so either can be inspected. Delete a
checkpoint (or change any of model/train/split/seed) and that cell retrains from
scratch, deterministically. Each checkpoint also stores its full training
`history`, so an examiner can inspect the learning curve directly:
`torch.load(path, weights_only=False)["history"]`.

## Scientific integrity

No number in any report is hand-entered; every value is computed by code in the
run and traceable to an artifact. Negative results are reported plainly.
`RESULTS.md` holds only validated numbers; open work lives in `TASKS.md`;
caveats in `LIMITATIONS.md`.
