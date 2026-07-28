# MolSanity — Claude Code build brief

You are building **MolSanity**, an open-source Python library and reproducible research
pipeline for **auditing the reliability of feature attributions on molecular graph neural
networks (GNNs) under distribution (scaffold) shift**. This brief is your source of truth.
On first run, copy the "Mission", "Hard rules", and "Definition of done" sections into a
`CLAUDE.md` at the repo root and maintain a `TASKS.md` task tracker you update continuously.

---

## Mission

Deliver a *journal-ready* contribution: not a new attribution method (those exist), but a
**reliability-audit framework** that (a) validates attributions against ground truth,
(b) characterises where attributions become untrustworthy under scaffold shift, and
(c) does so **across multiple GNN backbones and multiple molecular datasets**, benchmarked
head-to-head against existing attributors and evaluation frameworks. The novel, defensible
core is the *combination*: motif-native (RDKit) attribution + a coherence battery at two
granularities + occlusion–attribution faithfulness + cross-checkpoint stability +
calibration linkage + confidence/correctness **regime stratification under scaffold shift**.

Build **on top of** PyTorch Geometric, Captum, RDKit, and DeepChem/TDC. Do **not** reimplement
GNNExplainer, PGExplainer, SubgraphX, or Integrated Gradients — wrap the canonical
implementations. The optional M-JEPA encoder (public repo: https://github.com/Kar488/M-JEPA)
may be included as **one** pretrained-backbone case study, not as the base.

---

## Hard rules (non-negotiable — scientific integrity)

1. **Never fabricate, hard-code, or guess results.** Every number in any report is computed
   by code in this run and traceable to a logged artifact. No placeholder metrics.
2. **Log real outcomes, including negative ones.** If a method underperforms or a hypothesis
   fails, record it plainly. Honest negative results are valid output.
3. **Separate claims from TODOs.** `RESULTS.md` contains only validated numbers; anything
   unfinished lives in `TASKS.md`. Maintain a `LIMITATIONS.md`.
4. **Respect data licences and gating.** Never attempt to bypass credentialing (e.g. MIMIC).
   If a dataset is gated, skip it, log it as blocked, and continue.
5. **Determinism.** Global seed control; log seeds, library versions, and hardware in every
   run manifest. Results must reproduce.
6. **No interactive prompts.** Everything runs unattended from config + CLI.

---

## Autonomy & robustness (must run unattended overnight and resume)

- **Stage pipeline** with idempotent stages. Each stage writes artifacts to `artifacts/<stage>/`
  and a `.done` completion marker with a content hash of its config. Re-running skips completed
  stages unless config changed. Never redo finished work.
- **Checkpoint everything**: trained models, computed attributions, per-molecule audit records.
- **Graceful failure**: wrap each (dataset × backbone × attributor) cell in try/except; on
  failure, log full traceback to `logs/`, mark the cell failed in a run ledger, and **continue**
  to the next independent cell. One failure must never abort the run.
- **Structured logging** to `logs/run_<timestamp>.log` + a rolling `PROGRESS.md` summarising
  cells done / running / failed, updated after every cell.
- **Single entrypoint**: `python -m molsanity.run_all --config configs/full.yaml` runs the
  entire matrix end to end; re-invoking resumes. Also provide `make all`.
- **CI / git-runner**: a `.github/workflows/pipeline.yml` that runs a **smoke config** (tiny
  subset) on push, and can run the full pipeline on a self-hosted runner / manual dispatch.
- Assume it may be launched, left overnight, and relaunched to resume. Design for that.

---

## Performance requirements

- Batched, vectorised attribution computation; GPU when `torch.cuda.is_available()`, else CPU.
- Cache intermediate attributions and motif decompositions to disk keyed by (model_ckpt, graph_id).
- Parallelise the occlusion sweeps (per-motif masking) with multiprocessing / batched forward passes.
- Optional mixed precision for training. Profile the hot paths; the occlusion + IG loops are the
  bottleneck — make them fast (no Python per-atom loops in the inner path).
- The full matrix must be tractable on a single modern GPU overnight; expose a `--budget` knob
  (epochs, IG steps, molecules/assay) so a reduced-but-honest run is possible, clearly labelled.

---

## Datasets — pull from canonical sources, cache locally, verify

Implement a `molsanity.data` module with a **manifest** mapping each dataset to its loader,
source, licence, and a local cache path (`data/<name>/`), with checksum verification and
idempotent download. Log provenance for every dataset.

**Tier 1 — ground-truth (validates the audit itself; the credibility tier):**
- `BA-2Motifs`, `BA-Shapes` — synthetic, exact motif/node ground truth.
- `ShapeGGen` (via **GraphXAI**, https://github.com/mims-harvard/GraphXAI) — synthetic generator
  with ground-truth explanations robust to known pitfalls.
- `MUTAG` (PyG `TUDataset`) — NO₂ / aromatic motifs as quasi-ground-truth mutagenicity signals.
- Sanchez-Lengeling et al. attribution benchmark tasks (benzene/logic) if loadable.

**Tier 2 — real molecular property prediction (generalisation), via PyG / DeepChem / TDC:**
- Regression: `ESOL`, `FreeSolv`, `Lipophilicity`.
- Classification: `BBBP`, `BACE`, `Tox21`.
- Splits: **Bemis–Murcko scaffold splits** (deterministic) as the primary regime; random split
  as an in-distribution reference.

**Tier 3 — chemistry-meets-medicine (clinical-outcome molecular tasks), via Therapeutics Data
Commons (`pip install PyTDC`):**
- `ClinTox` (clinical-trial toxicity / FDA approval), `SIDER` (side effects by organ system),
  `DILI` (drug-induced liver injury), `hERG` (cardiotoxicity).
- These are molecular graphs with direct clinical meaning — the coherent medical angle.
- **Do NOT** attempt ICU / EHR time-series data (MIMIC, eICU, HiRID, AmsterdamUMCdb): different
  modality, credential-gated, out of scope for this tool. If referenced in config, skip + log.

---

## Backbones (demonstrate model-agnosticism)

Implement/train, via PyG, at minimum: **GIN/GINE, GCN, GAT, MPNN, AttentiveFP**. Optionally add
one pretrained SSL backbone (MolCLR or the public M-JEPA encoder) as a case study. Same head,
same splits, same calibration (temperature scaling on validation) across backbones.

---

## Attribution methods to audit (reuse canonical implementations)

Wrap and run: **Integrated Gradients** (Captum via PyG `CaptumExplainer`), **GNNExplainer**,
**PGExplainer**, **Grad-CAM** for graphs, **SubgraphX** (DIG). Provide a uniform adapter so each
returns node/edge/motif attributions in a common schema.

---

## The MolSanity audit (the contribution) — implement as `molsanity.audit`

For every (dataset × backbone × attributor) cell, compute and store per-molecule:

1. **Ground-truth accuracy** (Tier 1 only): attribution-vs-GT mask AUROC/AUPRC.
2. **Coherence battery**: atom-Gini, atom top-20% mass, salient largest-connected-component
   fraction, **motif top-1 share** (RDKit motifs: SSSR rings + Bemis–Murcko + fragments).
3. **Occlusion–attribution faithfulness**: per-motif masking Δlogit; per-molecule Spearman(IG rank,
   occlusion Δ) and top-1 agreement. Also compute the field-standard **Fidelity+ / Fidelity− /
   sparsity** and PyG `unfaithfulness` + GraphFramEx characterization score for comparability.
4. **Cross-checkpoint stability**: Spearman of motif attributions between pretrained/early and
   fine-tuned/late checkpoints.
5. **Calibration linkage**: relate attribution reliability to per-molecule calibration (ECE bins).
6. **Regime stratification**: confident-TP/TN, confident-error, borderline — under scaffold shift;
   blind, scaffold-diverse selection.

Then aggregate with proper **paired statistics** (Wilcoxon, bootstrap 95% CIs, effect sizes,
fraction-positive), per-assay and pooled, exactly-paired across methods/backbones where possible.

---

## SOTA-aware benchmarking (address the "novelty over SOTA" feedback)

- Reproduce, in-repo, the relevant metrics from **GraphXAI**, **GraphFramEx**, **DIG**, and
  **MolFaith** (https://github.com/molML/MolFaith) and run MolSanity's audit alongside them on
  shared datasets, so results are directly comparable to published evaluation frameworks.
- Produce a **head-to-head table**: attributors × datasets × {GT accuracy, Fidelity±, sparsity,
  MolSanity coherence/occlusion/stability}. Show, quantitatively, what the scaffold-shift regime
  audit + stability + calibration linkage surfaces that the existing frameworks do not.
- Explicitly cite and differentiate from MolFaith (molecular attribution *faithfulness* benchmark)
  and GraphXAI/GraphFramEx (general GNN explanation evaluation). The delta is: distribution-shift
  reliability + calibration + molecular-motif-native audit, across backbones.

---

## Deliverables (definition of done)

- Installable package (`pyproject.toml`, `pip install -e .`), `molsanity/` with `data/`, `models/`,
  `attributors/`, `audit/`, `benchmark/`, `viz/`, `run_all.py`.
- **High-quality figures** (vector PDF/SVG): ground-truth validation curves, coherence deltas,
  occlusion faithfulness, stability ECDFs, regime case studies with proper RDKit molecule
  rendering (high-res SVG, publication quality — not low-res raster composites).
- `configs/` with `smoke.yaml` (CI, minutes) and `full.yaml` (overnight matrix).
- `RESULTS.md` (validated numbers + tables), `LIMITATIONS.md`, `PROGRESS.md`, `TASKS.md`, `CLAUDE.md`.
- Unit tests (`pytest`) for data loaders, motif decomposition, each metric, and resumability
  (a stage re-run is a no-op). Tests must pass in CI on the smoke config.
- A `paper/` draft outline (`OUTLINE.md`) mapping each results table/figure to a manuscript
  section, and a related-work matrix vs GraphXAI/GraphFramEx/DIG/MolFaith with the explicit gap.
- README with install, quickstart, the dataset manifest + licences, and reproduction instructions.

---

## Start here (first session)

1. Scaffold the repo, `pyproject.toml`, `CLAUDE.md`, `TASKS.md`, `PROGRESS.md`, CI smoke workflow.
2. Implement `molsanity.data` with the manifest + caching + checksums; wire Tier-1 (BA-2Motifs,
   MUTAG, ShapeGGen) first and verify a load.
3. Implement one backbone (GINE) + one attributor (IG via Captum) + the audit metrics end to end
   on MUTAG, producing the first real `RESULTS.md` row and a ground-truth validation figure.
4. Only then broaden the matrix (more backbones, attributors, datasets). Keep it always-runnable
   and always-resumable; commit after each working stage with a clear message.
5. Continuously update `PROGRESS.md`. When blocked (gated data, missing dep), log it and move on —
   never stop the whole run for one blocker.
