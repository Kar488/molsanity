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

| Tier | Datasets | Source | Ground truth |
|------|----------|--------|--------------|
| 1 | MUTAG, SynthMotifs, BA-2Motifs, ShapeGGen | PyG / generated / GraphXAI | yes (SynthMotifs exact, MUTAG proxy) |
| 2 | ESOL, FreeSolv, Lipophilicity, BBBP, BACE, Tox21 | MoleculeNet (PyG) | no |
| 3 | ClinTox, SIDER, DILI, hERG | Therapeutics Data Commons | no |

Credential-gated ICU/EHR modalities (MIMIC, eICU, HiRID, AmsterdamUMCdb) are
**out of scope**: referencing them is a no-op (skipped + logged), never a
bypass attempt (Hard Rule 4).

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

## Scientific integrity

No number in any report is hand-entered; every value is computed by code in the
run and traceable to an artifact. Negative results are reported plainly.
`RESULTS.md` holds only validated numbers; open work lives in `TASKS.md`;
caveats in `LIMITATIONS.md`.
