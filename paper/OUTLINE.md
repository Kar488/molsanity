# MolSanity — paper outline

Working title: **MolSanity: A Reliability Audit for Molecular GNN Attributions
under Scaffold Shift.**

One-line thesis: existing attribution *faithfulness* benchmarks answer "does the
explanation match the model?"; MolSanity additionally answers "**is the model's
explanation trustworthy, and where does it stop being so under distribution
shift?**" — combining motif-native ground-truth validation, a coherence battery,
occlusion faithfulness, cross-checkpoint stability, calibration linkage, and
confidence/correctness regime stratification, across backbones and datasets.

---

## 1. Introduction
- Attribution methods for molecular GNNs are widely used but rarely audited for
  reliability *under scaffold shift*, the regime that matters for drug discovery.
- Contribution: a reliability-audit framework (not a new attributor). The
  defensible novelty is the *combination* and the *shift-stratified* view.
- Figure 1: the framework schematic (dataset × backbone × attributor → audit).

## 2. Related work and the gap  → `paper/RELATED_WORK.md`
- GraphXAI, GraphFramEx (general GNN explanation evaluation); DIG (methods +
  metrics); MolFaith (molecular attribution *faithfulness*).
- Gap MolSanity fills: distribution-shift reliability + calibration linkage +
  molecular-motif-native audit, **across backbones**, benchmarked head-to-head.
- Table 1: related-work matrix (capabilities × frameworks).

## 3. Method — the MolSanity audit
- 3.1 Motif-native decomposition (RDKit: SSSR rings + Bemis–Murcko + BRICS).
- 3.2 Ground-truth accuracy (Tier-1): attribution-vs-motif AUROC/AUPRC.
- 3.3 Coherence battery (Gini, top-20% mass, salient CC fraction, motif top-1).
- 3.4 Occlusion–attribution faithfulness (per-motif Δlogit; Spearman; Fidelity±;
  sparsity) — field-standard metrics reproduced for comparability.
- 3.5 Cross-checkpoint stability (early vs final motif attributions).
- 3.6 Calibration linkage + regime stratification (confident-correct /
  confident-error / borderline) under scaffold shift.
- 3.7 Aggregation: paired Wilcoxon, bootstrap 95% CIs, fraction-positive.

## 4. Experimental setup
- Datasets: Tier-1 exact-GT **SynthMotifs** (BA + house/cycle motif, generated
  offline) and quasi-GT **MUTAG**; Tier-2 MoleculeNet classification (BBBP, BACE)
  and regression (ESOL, FreeSolv, Lipophilicity); Tier-3 chemistry-meets-medicine
  as single-task views (**ClinTox** CT_TOX, **SIDER**, **Tox21**). ShapeGGen /
  TDC-native / BA-2Motifs download are gracefully skipped where unreachable.
- Backbones: GINE, GCN, GAT, MPNN, AttentiveFP (shared head/calibration/splits).
- Attributors: IG, Saliency, InputXGradient, GuidedBackprop, GNNExplainer,
  **PGExplainer** (SubgraphX needs DIG, unavailable here).
- Splits: **class-aware** Bemis–Murcko scaffold (primary; guarantees every fold
  has every class without scaffold leakage) + random (in-distribution reference).
  Imbalanced classification uses inverse-frequency class weighting + AUC model
  selection.
- Reproducibility: global seed; per-attribution seeding for stochastic explainers
  (GNNExplainer/PGExplainer); versions + hardware in every run manifest.

## 5. Results (maps to artifacts)
- 5.1 Ground-truth localisation — **Fig. `gt_validation`** + RESULTS.md GT AUROC.
  Headline (validated, `configs/matrix.yaml`): faithfulness ≠ correctness. On
  MUTAG/GINE, Saliency and InputXGradient are *faithful* (occlusion Spearman
  ≈ 0.38/0.40) yet **anti-aligned with the nitro ground truth** (GT AUROC
  ≈ 0.03/0.04 ≪ 0.5), while IG (0.54) and GNNExplainer (0.49) recover it — a
  >0.5 AUROC gap at near-equal faithfulness that a faithfulness-only benchmark
  misses.
- 5.2 Head-to-head across attributors — **BENCHMARK.md** + paired Wilcoxon.
  Perturbation (GNNExplainer) vs gradient trade-off between GT localisation and
  faithfulness.
- 5.3 Model-agnosticism — MUTAG × {GINE,GCN,GAT,MPNN,AttentiveFP}.
- 5.4 Stability & calibration linkage — regime-stratified reliability.
- 5.5 Regime stratification under shift — where attributions fail (confident
  errors) — case-study molecule figures.

## 6. Discussion
- Practical guidance: when to trust molecular attributions; what the shift +
  calibration view surfaces that faithfulness-only benchmarks miss.
- Honest negatives are reported (LIMITATIONS.md), including proxy-GT caveats.

## 7. Limitations  → `LIMITATIONS.md`
## 8. Reproducibility  → README + run manifest + CI smoke.

---

### Artifact → manuscript map
| Manuscript element | Produced by | Artifact |
|---|---|---|
| Fig. 1 schematic | (hand-drawn) | — |
| Fig. GT validation | `viz.ground_truth_validation_figure` | `artifacts/figures/<cell>/gt_validation.pdf` |
| Case-study molecule | `viz.molecule_attribution_svg` | `artifacts/figures/<cell>/case_molecule.svg` |
| Fig. GT-by-attributor bar | `viz.attributor_gt_bar` | `figures/summary/attributor_gt_bar_{MUTAG,SynthMotifs}.pdf` |
| Fig. faithfulness/stability ECDF | `viz.faithfulness_stability_ecdf` | `figures/summary/faithfulness_stability_ecdf.pdf` |
| Fig. regime stratification | `viz.regime_stratification_figure` | `figures/summary/regime_stratification.pdf` |
| Fig. attributor × molecule grid (signature) | `viz.make_case_study_grid` | `figures/summary/molgrid_{MUTAG,SynthMotifs}.pdf` |
| Fig. faithfulness–correctness joint scatter | `viz.faithfulness_correctness_joint` | `figures/summary/joint_faithful_correct.pdf` |
| Fig. per-molecule GT raincloud | `viz.raincloud_gt` | `figures/summary/raincloud_gt_MUTAG.pdf` |
| Fig. cross-dataset GT heatmap | `viz.results_heatmap` | `figures/summary/heatmap_gt.pdf` |

All figures use one house style (`viz/style.py`): a colourblind-safe categorical
palette with each attributor/backbone bound to a fixed hue across every panel,
bold panel letters, inline value labels, recessive spines/grid — vector PDF+SVG.
| Table 1 related work | `paper/RELATED_WORK.md` | committed |
| Results matrix | `run_all` → `RESULTS.md` | committed |
| Head-to-head + paired stats | `benchmark.write_benchmark_md` | `BENCHMARK.md` |
| Per-molecule records | `audit.audit_molecule` | `artifacts/audit/<cell>/records.json` |
