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

> Status: **first vertical slice complete** — MUTAG × GINE × Integrated
> Gradients, end to end, with validated numbers in [`RESULTS.md`](RESULTS.md).
> The matrix broadens from here (see [`TASKS.md`](TASKS.md)).

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

## First result (MUTAG × GINE × Integrated Gradients, scaffold split)

The slice surfaces MolSanity's central distinction — **faithfulness is not
correctness**:

- IG attributions are **faithful to the model** (occlusion Spearman ≈ 0.58,
  top-1 motif agreement 0.80) …
- … yet they **do not recover the ground-truth nitro motif** — attribution-vs-GT
  AUROC ≈ **0.22**, i.e. *anti-aligned* (chance = 0.5). The model, under scaffold
  shift, leans on the fused-aromatic core rather than the mutagenic NO₂ group,
  and IG faithfully reports that.

See the exact numbers in [`RESULTS.md`](RESULTS.md) and the ground-truth
validation figure under `artifacts/figures/`. (MUTAG's motif "ground truth" is a
chemically motivated nitro-group *proxy*, clearly labelled as such — see
[`LIMITATIONS.md`](LIMITATIONS.md). Exact ground truth comes from the synthetic
Tier-1 sets.)

## Dataset manifest & licences

`molsanity.data` holds the manifest (loader, source, licence, cache path,
checksum). Provenance is logged per dataset to `data/<name>/provenance.json`.

| Tier | Datasets | Source | Ground truth |
|------|----------|--------|--------------|
| 1 | MUTAG, BA-2Motifs, ShapeGGen | PyG / GraphXAI | yes (exact or proxy) |
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
