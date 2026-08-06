# LIMITATIONS.md — MolSanity

Honest, running list of caveats, scope limits, and known weaknesses. Kept
current alongside RESULTS.md.

## Corrections to previously published numbers

- **The scaffold split was not a scaffold split, except on MUTAG (found
  2026-08-03; all shift results before this date are withdrawn).**
  `splits._murcko_scaffold_smiles` reconstructed every graph through
  `graph_to_mol`, which decodes atom features using MUTAG's 7-way atom one-hot.
  MoleculeNet and TDC graphs use a 9-dim vector whose first entry is the atomic
  number, so `argmax` picked index 0 for almost every atom and each molecule was
  rebuilt as an all-carbon skeleton. The Murcko scaffolds of those skeletons are
  near-unique, so every molecule fell into its own bucket and the partition
  became a deterministic index split with no scaffold grouping at all. Measured
  fraction of test molecules sharing a *true* Bemis-Murcko scaffold with a
  training molecule: **ClinTox 50.3%, BBBP 56.1%, BACE 30.3%** — a correct
  scaffold split leaks none, by construction. Consequences:
  - Every "under scaffold shift" number computed before 2026-08-03 on a dataset
    other than MUTAG is invalid and is not reported. 99 cell-runs are being
    recomputed.
  - MUTAG is unaffected in kind (it ships no SMILES, so the one-hot path is the
    correct one for it), though the fix changes its grouping slightly, 52 -> 47.
  - The random-split arm, the motif battery, `motif_top1_share` and the
    ground-truth masks never used this code path and are unaffected.
  - Fixed by routing through `mol_from_data`, which parses the graph's own
    SMILES when it has one. Regression tests in `tests/test_splits.py` fail
    against the old implementation.
  - The lesson worth keeping: the split reported `2038 scaffolds` over ~2039
    BBBP molecules and nothing flagged it, because a near-1:1 ratio reads as
    "diverse chemistry" rather than "no grouping happened". RDKit on BBBP's own
    SMILES gives 1025. `scaffold_split` now records `frac_grouped` and
    `degenerate` on the `Split` and warns when a partition is not a shift regime.

## Scope

- **Three of the ground-truth datasets cannot support a shift contrast at all.**
  BA-2Motifs, SynthMotifs and ShapeGGen are not molecules, so a Bemis-Murcko
  scaffold is undefined for them; post-fix, `scaffold_split` reports
  `frac_grouped = 0.000, degenerate = True` on all three — every graph in its own
  bucket. Their "scaffold" partition is deterministic and reproducible but is not
  a chemical shift, and they are excluded from the shift analysis and reported as
  random-split evidence only. The shift contrast rests on the five molecular
  arms: MUTAG (proxy ground truth), MolMotif and MolMotifHard (exact by our own
  construction), and Benzene and FluorideCarbonyl (per-atom rationales published
  by Sanchez-Lengeling et al., repackaged by GraphXAI — the only two we neither
  designed nor labelled).
- **The pooled shift effect did not survive the two new arms, and that is now
  the reported result.** Restricted to MUTAG/MolMotif/MolMotifHard the pooled
  faithfulness–correctness correlation runs +0.009 (p = 0.962) → −0.356
  (p = 0.042) over 33 cells. Over all five arms and 47 cells it is +0.222
  (p = 0.134) → −0.124 (p = 0.405): no effect in either regime. Both figures are
  recomputed from the same run by restricting the arm set. Per-arm values under
  shift span −0.564 (MUTAG) to +0.786 (FluorideCarbonyl), so no pooled
  coefficient describes any single arm. The paper reports the five-arm result
  and records the supersession explicitly.
- **Benzene and FluorideCarbonyl are single-functional-group detection tasks.**
  They are the only externally labelled molecular arms and are weighted
  accordingly, but a rationale that is one functional group is an easier
  localisation problem than the multi-centre rationales behind most real ADMET
  endpoints. They widen the evidence; they do not make it representative.
- **CPU-only development environment.** All defaults are CPU-tractable. The
  overnight full matrix assumes a single modern GPU; without one, use `--budget`
  to run a reduced-but-honest subset (clearly labelled in reports).
- **The proxy objection is now answered two ways.** Faber et al. (KDD 2021)
  argue that comparing against a known rationale misleads when the trained model
  does not use that rationale, so a low GT AUROC may say something about the
  model rather than the attribution. Two additions address it directly:
  - **MolMotif** (`molsanity/data/molmotif.py`): real drug-like molecules
    relabelled so the class *is* presence of a chemical substructure. The
    ground truth is exact **by construction**, and the arm is molecular. It is
    the only arm that is both. Easy by design, and labelled as a probe of the
    audit rather than a hard benchmark.
  - **The rationale-use test** (`molsanity/audit/rationale.py`): per molecule,
    occlude the ground-truth substructure. If the prediction collapses, the
    model demonstrably uses it, and an anti-aligned attribution is wrong by the
    model's own behaviour, not by disagreement with a chemical prior. If it does
    not, Faber applies and the molecule is reported separately. The headline
    number is `n_anti_aligned_despite_model_using_it`.
- **MUTAG "ground truth" is quasi-ground-truth.** MUTAG has no per-atom
  explanation labels shipped with the PyG `TUDataset`. We derive a chemically
  motivated proxy mask (nitro / aromatic-nitro groups, the canonical
  mutagenicity motifs from Debnath et al. 1991) via RDKit SMARTS. This is a
  motif-level proxy, not annotator ground truth; it is labelled as such wherever
  used. Exact ground truth comes from the offline SynthMotifs generator, and
  (from the next sweep onward) from BA-2Motifs.

## Data

- **SynthMotifs** provides *exact* node ground truth but is a **structural,
  non-molecular** synthetic task (BA base + house/cycle motif); it validates the
  audit machinery, not chemical generalisation. Molecular ground truth remains
  the MUTAG nitro *proxy* until BA-2Motifs/ShapeGGen are reachable.
- **DILI / hERG (Therapeutics Data Commons)** are wired via PyTDC and audited
  (DILI GINE acc 0.80/AUC 0.82; hERG GCN acc 0.90/AUC 0.80). They carry **no node
  ground truth** (gt_auroc is "—"), so they extend the coherence/faithfulness/
  calibration battery to real ADMET-toxicity endpoints but not the GT-localisation
  axis — that axis stays anchored on SynthMotifs (exact) and the MUTAG proxy.
- **SubgraphX (DIG): resolved, but postdates the committed run.** The earlier
  entry here said no wheel exists for `torch_sparse`/`torch_scatter` at torch
  2.13 and that source builds hang. That was wrong: they build from source
  (slowly, ~15 min), DIG then installs and imports, and SubgraphX is now wrapped
  in `attributors/subgraphx.py` with tests in which it recovers a planted
  five-node motif exactly. It is enabled in `configs/full.yaml`. No SubgraphX
  row exists in the committed results, so every perturbation-family statement in
  the current RESULTS.md still rests on GNNExplainer alone.
- **ShapeGGen (GraphXAI): installable, but a task-level mismatch.** It also was
  not blocked by `torch_sparse`. GraphXAI's `setup.py` packages only the
  top-level module, so a wheel install is broken; from a source checkout (plus
  `ipdb`) `ShapeGGen` builds fine. It stays unintegrated for a real reason:
  ShapeGGen is **node** classification on one large graph, while every MolSanity
  axis is defined per molecule at the **graph** level. Integrating it means
  extending the audit to node-level tasks, not fixing a dependency.
- **BA-2Motifs node labels: recovered, but postdates the committed run.** PyG's
  `BA2MotifDataset` exposes no per-node field, so the extractor read nothing and
  both cells landed in the no-GT block. The labels are recoverable from the
  release's node ordering (motif appended after the BA base); that is now
  implemented, structurally verified (induced subgraph must be a house or a
  five-cycle, else refused), and cross-checked against PyG's `ExplainerDataset`.
  The committed numbers predate it.
- **PGExplainer is classification-only.** Its parametric mask-MLP is trained
  against class logits, so the current wrapper does not support graph-regression;
  regression cells use the gradient family + GNNExplainer (the perturbation-based
  attributor that does support regression). Regression PGExplainer is future work.

## Tier-2 classification under reduced-budget scaffold split

- **Degenerate models on imbalanced classification (BBBP, BACE).** Under the
  reduced `matrix.yaml` budget (30 epochs, hidden 32), Bemis–Murcko scaffold
  splits on the class-imbalanced BBBP/BACE produce near-single-class test folds,
  and the model collapses to a majority-class predictor (test accuracy ≈ 1.0 but
  ROC-AUC undefined). The audit still *runs*, but attributions of a constant
  predictor are not scientifically meaningful, so these cells are **not featured**
  (one BBBP·GINE cell is retained as a documented example). Meaningful Tier-2
  classification needs the overnight `full.yaml` budget **and** a class-aware
  scaffold split — tracked in `TASKS.md`. The meaningful Tier-2 results at this
  budget are the **regression** tasks (ESOL/FreeSolv/Lipophilicity), where models
  reach honest R² (e.g. ESOL ≈ 0.67–0.69 across backbones).

## Practical utility

- **The audit does not propose a replacement selection method.** It shows that
  faithfulness metrics fail to pick the ground-truth-best attributor under
  shift, and does not offer a metric that succeeds. That is deliberate: on this
  evidence no available signal does, and inventing one would invite the same
  criticism one level up.
- **What it offers instead is abstention.** `audit/abstention.py` reframes the
  question from *which explanation to choose* to *when to trust any of them*,
  as a coverage-reliability curve over signals available at inference time.
  `ABSTENTION.md` reports a recommended operating point, or states plainly that
  no signal buys reliability. **The transfer assumption is the weak point**: the
  curves are computed where ground truth exists, and applying the rule to a real
  molecular dataset assumes the relationship carries over to cells where
  correctness cannot be measured. This paper's own central finding is that such
  transfer fails across splits, so the assumption is stated rather than relied
  on silently.

## Statistics

- **Multiplicity is now controlled.** Selection tests carry Benjamini-Hochberg
  adjusted q-values over the family of 12 tests; attributor contrasts carry them
  over the family within each cell block. Every headline mismatch on the MUTAG
  and SynthMotifs scaffold-shift arms survives at q < 0.001, so those are
  false-discovery-rate controlled findings rather than descriptive numbers. The
  adjustment is pinned against `scipy.stats.false_discovery_control` in
  `tests/test_multiplicity.py`, including a test that fails if a future run
  weakens the headline contrast.
- **What the adjustment does not fix is power.** At n = 20 molecules per
  ground-truth arm, a contrast that fails to reach significance is weak evidence
  of no difference, not evidence of none. Raising n on the ground-truth arms is
  the outstanding statistical work.

## Methods

- **The regression occlusion metric was mis-specified in the committed run.**
  It clipped the attribution at zero (keeping only atoms that push the
  prediction *up*) while leaving the occlusion effect signed, so a motif that
  drives the prediction strongly down scored as unimportant on one side and
  dominant on the other. That alone is enough to produce the systematic
  negative rho across the regression cells, and it is why the unbounded
  output-space Fidelity+ values run far outside the [-1,1] a probability-space
  fidelity occupies. Corrected in `audit/occlusion.py`: regression ranks by
  magnitude on both sides, the GraphFramEx characterisation score is reported
  as undefined rather than clipping a sigma-space shift into [0,1], and a
  bounded `fidelity_ratio` gives the share of the total occlusion effect
  carried by the salient atoms. The classification path is untouched (pinned by
  a test). **The committed regression faithfulness numbers predate the fix and
  are excluded from every faithfulness claim** until the next sweep.
- **Occlusion is an off-manifold counterfactual — now measured, not just
  stated.** Zeroing node features takes the graph off the data manifold, so a
  motif whose removal barely moves the output may be redundant rather than
  unimportant. Each record now also carries `occ_spearman_imputed`, the same
  statistic with removed nodes set to the training-split mean feature vector
  instead of zero, which keeps a removed node looking like a plausible but
  uninformative one. The two agreeing bounds the artefact; the two disagreeing
  localises it. The baseline is computed on the training split only, so it
  carries no information from the audited molecules.
- The first slice audits a single attributor (Integrated Gradients). Additional
  attributors and backbones broaden the matrix in later milestones; absence of a
  cell in RESULTS.md means it has not been validated, not that it failed.
