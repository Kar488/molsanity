# TASKS.md — MolSanity task tracker

Status legend: `[ ]` todo · `[~]` in progress · `[x]` done · `[!]` blocked

> `RESULTS.md` holds only validated numbers. This file holds everything
> unfinished. Update continuously.

## PAPER EDITS PENDING — the running list

Everything found during the sweeps that changes what the manuscript may claim.
Read this before `make -C paper`. Ordered by how much damage it does if missed.

### Claims that changed with the corrected split — DONE 2026-08-03

The 3 August re-run inverted or weakened four claims the manuscript made. All
four are now rewritten from the regenerated macros and cross-checked against
`results/BENCHMARK_GT.json` and `results/RATIONALE_USE.md`.

- [x] **"Faithfulness and correctness invert under shift" was too strong.**
      Faithfulness rankings mismatch the ground truth *in-distribution too*
      (3 of 3 metrics). The claim is now a collapse in rank correlation
      (occlusion +0.143 -> -0.643; mean over metrics +0.20 -> -0.24), stated as
      such in the abstract and the contribution list.
- [x] **"The attributor ordering does not survive the split" was backwards.**
      It largely does: rho = 0.821 on MUTAG, 0.964 on MolMotif. The *backbone*
      ordering is what does not survive (rho = 0.100). Rewritten to separate
      what shift breaks from what it leaves alone, and the MolFaith positioning
      now turns on "stability of a proxy is not validity of a proxy".
- [x] **"Ground-truth localisation falls below chance on confidently-wrong
      predictions" was false.** It is 0.612, above chance, down from 0.787 on
      confident-correct. The stronger honest version replaced it: localisation
      degrades exactly there, while occlusion faithfulness *improves*
      (0.170 -> 0.443) and stability does not worsen (0.787 -> 0.825). Both
      cheap proxies point away from the failure.
- [x] **"The calibration link reverses sign when pooled" was false.** It
      attenuates, +0.160 per-cell median to +0.037 pooled. Still a Simpson
      trap, no longer a sign flip.

### Scope corrections — DONE 2026-08-03

- [x] **SynthMotifs, BA-2Motifs and ShapeGGen are out of the shift contrast.**
      Not molecules, so no Bemis-Murcko scaffold; the splitter reports
      `frac_grouped = 0.000, degenerate = True`. `ARMS` in `make_tables.py` no
      longer includes SynthMotifs, and the molgrid caption says explicitly that
      SynthMotifs is a structural illustration only.
- [x] **MolMotif replaces it as the second arm, and cannot adjudicate.**
      Molecular and exactly labelled, but saturated: top attributors at GT AUROC
      0.99-1.00, so ranking among them is noise around a ceiling, and its
      faithfulness-truth correlation is negative in *both* regimes. Reported as
      a probe that the audit works, not as a second shift contrast.
- [x] **The shift contrast rests on MUTAG alone**, n=53 per arm, proxy ground
      truth. Stated in the abstract and Limitations, not buried.
- [x] **SubgraphX was missing from every paper-side attributor map** (SHORT,
      ATTR_ORDER, tags, ATTRIBUTOR_COLOR, ATTRIBUTOR_MARKER), so `make tables`
      crashed once it entered the selection test. Added, with `#000000` (the
      eighth Okabe-Ito colour) and marker `v`.
- [x] **The Faber objection now has a section** (`sec:rationale`) rather than
      only a citation. 6,257 molecules carry a rationale the model does not use
      against 4,565 that it does; of the latter, **722** (0.158) still receive an
      anti-aligned attribution. Macros recompute the partition from the records
      with the same rule as `molsanity/audit/rationale.py`, so the paper and the
      report cannot drift.

### Still open

- [ ] **ShapeGGen's scaffold cells now run rather than crash**, producing a
      degenerate partition flagged as such. The ledger counts them; make sure no
      table implies they contribute to the shift axis.
- [ ] **Re-decide whether the flagship table should be single-seed.**
      `BENCHMARK_GT.md` reports seed 0. The per-seed check holds — occlusion
      rho is negative on 3/3 seeds under shift, +0.36 +/- 0.19 -> -0.66 +/- 0.09
      — and the abstract quotes that spread, but the table itself does not.
      Either add a seed column or state the single-seed scope in the caption.

### Reproducibility statement

- [ ] **Attribution runs on CPU.** The worker pool forks, and CUDA cannot
      survive fork, so the audit loop is CPU-only while training uses the GPU.
- [ ] **GNNExplainer is device-sensitive at the third decimal.** IG, Saliency,
      GuidedBackprop and InputXGradient were bit-identical GPU vs CPU;
      GNNExplainer moved 0.003-0.012 because it fits a mask with Adam over ~100
      steps. A reader reproducing on GPU will not match it beyond two decimals.
- [ ] **Parallel equals serial.** Verified field-by-field over full records, so
      a reader may trade cores for time freely. Worth one sentence: it is the
      kind of claim reviewers assume is untested.
- [ ] **SubgraphX seeding was a real defect, now fixed.** DIG draws from
      `np.random`, which `torch.manual_seed` never reset, so results depended on
      how many molecules preceded them. Seeding per molecule made it
      order-independent and resume-safe.

### Compute paragraph (Experimental setup, not its own section)

- [ ] Reproduction cost: cell-runs, wall clock, hardware (A100, 12 vCPU),
      derivable from the log timestamps rather than hand-typed.
- [ ] **The cost asymmetry is a finding, not filler.** SubgraphX measured at
      23.67 s per molecule on 12 workers (~79 min per 200-molecule cell) against
      0.01-0.07 s for the gradient family — two to three orders of magnitude.
      Compute cost is a hidden selection pressure on which attributors get
      benchmarked at all, and it biases the literature toward cheap ones. Our
      own first instinct was to cap SubgraphX's n, which would have introduced
      exactly the small-n weakness the field criticises.
- [ ] Do **not** write a "future compute directions" roadmap. Anything genuinely
      compute-limited belongs in Limitations, phrased as a limitation.

### Positioning

- [ ] **MolFaith is prior art** (Hiltscher, Bianciotto, Grisoni; chemRxiv,
      27 Jan 2026): 8 methods, 2 representations, 5 architectures, ~14,000
      molecules, faithfulness only. Already cited with its exact scope and the
      concession that it is larger on that axis. Keep the distinction explicit
      in the abstract: their finding is that *faithfulness* ordering is stable
      across **architectures**; ours is that *correctness* ordering is unstable
      across **splits**. Not a contradiction, but a reviewer will land on it.
- [ ] Target venue: Journal of Cheminformatics, "AI and XAI in Drug Discovery"
      collection, deadline 13 January 2027. Check whether an APC waiver or a
      read-and-publish agreement applies before committing.

### Done this session

- [x] `LICENSE` (MIT) added; `THIRD_PARTY_LICENSES.md` records that DIG is
      GPL-3.0, not vendored, and optional.
- [x] n=200 for every attributor, SubgraphX included — the small-n criticism is
      answered rather than traded away.
- [x] Across-seed variance added to the related-work capability matrix; none of
      GraphXAI, GraphFramEx, DIG or MolFaith reports it.

## Cost of the strengthened sweep

`configs/full.yaml` is now **58 cells x 2 splits x 3 seeds = 348 cell-runs**, up
from 88, and SubgraphX runs a Monte-Carlo tree search per molecule. If that
budget is not available, run `configs/groundtruth.yaml` instead: **36 cells,
216 cell-runs**, covering every dataset on which attribution *correctness* can
be measured at all. That is where the selection experiment, the seed variance
and the shift contrast live; the no-ground-truth molecular cells only ever
contributed the faithfulness axis.

## Next sweep — what a re-run must pick up

Four code changes landed after the committed `full.yaml` run
(`20260730-184508`). None of them changed a published number; all of them
change what the *next* run produces. Re-run `python -m molsanity.run_all
--config configs/full.yaml` to collect them.

- [ ] **BA-2Motifs becomes a third exact-ground-truth arm.** Node labels are now
      recovered from the release's node ordering and structurally verified.
      `configs/full.yaml` gives it the full attributor sweep. The selection
      experiment can then be replicated on a second exact-GT dataset, which is
      the single biggest strengthening available to the paper.
- [ ] **SubgraphX populates the perturbation family.** Needs
      `pip install -e ".[subgraphx]"`; `torch_sparse`/`torch_scatter` build from
      source and take roughly 15 minutes. SubgraphX runs a Monte-Carlo tree
      search per molecule and is by far the most expensive attributor in the
      sweep — budget for it (`sgx_rollouts`, `sgx_max_nodes`).
- [ ] **Regression faithfulness gets recomputed under the corrected operator.**
      The current regression numbers are withdrawn from interpretation. After
      the re-run, either restore the regression faithfulness claim or state the
      corrected finding.
- [ ] **MolMotif gives a molecular AND exactly-labelled arm.** 906 balanced
      BBBP molecules whose label is presence of an aromatic halogen, mask = the
      matched atoms grown by one bond. Removes the proxy objection outright on
      one arm.
- [ ] **The rationale-use test runs on every ground-truth molecule.** Reports
      whether the model actually reads the ground-truth substructure, so the
      central finding can be restated on the subset where the Faber objection
      provably does not apply.
- [ ] **ShapeGGen closes the grid.** The 2 skipped cells in the 86/88 tally
      were both ShapeGGen. It is now wired as graph classification by taking
      each labelled node's k-hop enclosing subgraph, which is where a node's
      explanation lives, giving ~164 instances with exact node ground truth.
      Needs GraphXAI from a source checkout plus `ipdb`; its published wheel
      omits the subpackages.
- [ ] **Three seeds instead of one.** `seeds: [0, 1, 2]`. `SEED_VARIANCE.md`
      reports the across-seed mean and sd per cell. Read it against the effect
      sizes in RESULTS.md: an effect smaller than the spread is not evidence.
- [ ] **Bigger ground-truth arms.** The test fold went 0.1 -> 0.3 and
      SynthMotifs 200 -> 1000 graphs, so n per arm goes from 20 to roughly 56
      (MUTAG), 200 (SynthMotifs, capped), 200 (BA-2Motifs) and 49 (ShapeGGen).
      This retrains every model, so every number moves.
- [ ] **Occlusion measured under two counterfactuals.** Each record now also
      carries `occ_spearman_imputed`, computed with removed nodes set to the
      training-set mean feature vector instead of zero. The gap between the two
      bounds how much of a faithfulness score is an off-manifold artefact.
- [ ] **The 38 carried rows become current.** They survive from an earlier
      reduced-budget run because those cells failed in an older sweep; the GPU
      defects behind that are fixed, so a clean re-run should retire the
      `carried` provenance class entirely.

After the sweep: `cd paper && make` regenerates every figure, table and inline
number, then re-read the withdrawn regression paragraph and the two BA-2Motifs
paragraphs in `body.tex`, which are written for the pre-fix state.

## After the sweep — analyses that need its output

- [ ] **Read `ABSTENTION.md` first.** If a signal shows positive lift, the paper
      gains an actionable rule ("keep the top X% by <signal>") and answers the
      "no practical utility" criticism. If no signal works, that is a reportable
      negative and the Discussion should say so plainly rather than hedging.
- [ ] **Read `RATIONALE_USE.md`.** `n_anti_aligned_despite_model_using_it` is
      the number that answers Faber et al. Promote it into the Results if it is
      non-trivial; it converts the strongest reviewer objection from a framing
      argument into a statistic.
- [ ] **Restate the headline on the MolMotif arm.** It is the only arm that is
      both molecular and exactly labelled, so if the inversion replicates there
      it should lead, with MUTAG demoted to a supporting proxy result.

## Known-good, do not regress

- [x] CI has two jobs: the smoke pipeline on the **pinned** stack
      (`requirements-lock.txt`), and a paper rebuild that fails on a LaTeX
      error, a missing glyph or a non-embeddable font. The reproducibility
      claim in the paper is exactly what those jobs test.
- [x] `configs/smoke.yaml` runs two seeds, so CI exercises the multi-seed path.
      A single-seed smoke config could not have caught the row-key bug that
      would have discarded two thirds of a three-seed matrix.
- [x] Fonts: `make` runs `figs/check_fonts.py`, which fails the build on a Type 3
      or non-embedded font. arXiv rejects both. matplotlib's PDF default is
      Type 3, so any new figure code must set `pdf.fonttype: 42`.

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
- [x] **Capstone figure + single figure home.** `figures/` is now the one
      committed, browsable folder for every generated figure (key / summary /
      per-cell + generated `INDEX.md`), mirrored from `artifacts/figures` at the
      end of each run by `viz.collect`; the old partial `results_figures/` is
      retired. Added `viz.dissociation` — the two-regime faithfulness-vs-truth
      capstone (`figures/key/dissociation.pdf`).
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
- **GNNExplainer is device-sensitive at the third decimal, and this belongs in
  the reproducibility statement.** Every other attributor returns bit-identical
  values on GPU and on the CPU worker pool (IG 0.8886, Saliency 0.96492,
  GuidedBackprop 0.91328, InputXGradient 0.95144 all matched exactly across the
  two). GNNExplainer moved by 0.003-0.012 (e.g. 0.66812 -> 0.67156). It is the
  only attributor that fits a mask with Adam over ~100 steps, so floating-point
  differences compound. Not a determinism defect -- the per-molecule seeding in
  `base.py` is correct -- but a reader reproducing on a GPU will not match the
  committed GNNExplainer numbers to more than two decimals, and the paper
  should say so rather than let them discover it.
- **Parallel attribution: on, after fixing a real reproducibility defect.**
  The first attempt produced results that did not match the serial path, and the
  cause turned out to be a bug in the serial path rather than in the pool.
  `dig/xgraph/method/shapley.py` estimates the Shapley value with
  `np.random.permutation` — the *global* NumPy generator, which
  `torch.manual_seed` never touched. A molecule's SubgraphX attribution
  therefore depended on how many molecules preceded it, so a resumed run, or one
  that skipped a cached cell, could return a different subgraph for the same
  input. Seeding NumPy and `random` per molecule alongside torch fixes both:
  pooled results are now bit-identical to serial ones at the realistic
  configuration (20 rollouts, 30-node graphs), and a molecule attributed alone
  matches the same molecule attributed mid-run. Pinned by two tests in
  `tests/test_subgraphx.py`.
  Speed remains unproven on this hardware: 1.22x on a 4-core container that is
  almost certainly CPU-quota-limited. The mechanism scales with real cores, but
  the number to quote is whatever the Colab runtime actually reports.
- **BA-2Motifs**: PyG download source returns HTTP 403 in this environment.
  Loader + ground-truth extractor are implemented; blocked on data fetch only.
- **SubgraphX (DIG)**: no longer blocked, and no longer needs
  `torch_sparse`/`torch_scatter` at all — those come from DIG's package
  `__init__`, which the wrapper now bypasses. Install with
  `pip install --no-deps dive-into-graphs`; `--no-deps` is required because
  DIG pins `captum==0.2.0`, which breaks Integrated Gradients under PyG's
  `CaptumExplainer` (this cost the 31 July run all 204 of its IG cells).
- **ShapeGGen (GraphXAI)**: GraphXAI's PyPI wheel omits its subpackages, so it
  imports but is unusable; install from a source checkout. Its exact-GT role is
  covered by SynthMotifs, so this is redundant rather than a gap.
- **TDC (PyTDC)**: installed and wired (DILI, hERG). Install needs a minimal
  footprint (`pip install --no-deps PyTDC` + `huggingface_hub`/`httpx`) because
  the full dependency set conflicts with the pinned numpy/rdkit here.
- MUTAG ground truth is a nitro-motif *proxy* (documented in LIMITATIONS.md),
  not annotator labels; exact GT comes from synthetic Tier-1 sets.

### Audit records are written without the seed in their path

`run_all.py` builds `cell_id` as `dataset__backbone__attributor__split`, with
no seed, so each seed's run overwrites the previous one's
`artifacts/audit/<cell_id>/records.json`. What survives on disk is whichever
seed ran last, unlabelled.

- [ ] Put the seed in the records path and keep all three.
- The consequence today: the selection tests, which read per-molecule records,
  are single-seed. That is *methodologically* correct — the split is a function
  of the seed, so a paired per-molecule test must stay within one seed — but
  the retained seed is arbitrary rather than chosen, and it happened to be the
  one where MUTAG·GINE·GNNExplainer scores 0.826 against an across-seed mean of
  0.774 ± 0.086. Same ordering, materially different number.
- The paper now states this and quotes both figures (§7, Table 5 caption,
  abstract), and SEED_VARIANCE.md ships as supplementary material. Fixing the
  path lets a future run pick the seed deliberately, or report the paired test
  per seed and pool.
