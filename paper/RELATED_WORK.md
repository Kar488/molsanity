# Related-work matrix — where MolSanity differs

MolSanity is not a new attribution method. It is a **reliability audit** that
composes ground-truth validation, coherence, occlusion faithfulness, stability,
calibration linkage, and **scaffold-shift regime stratification**, across
backbones and datasets, benchmarked head-to-head against existing frameworks.

## Capability matrix

Legend: ✓ = core capability · ~ = partial / possible but not central · ✗ = not a focus.

| Capability | GraphXAI | GraphFramEx | DIG | MolFaith | **MolSanity** |
|---|---|---|---|---|---|
| Ground-truth explanation benchmarks | ✓ (synthetic) | ~ | ✓ | ✗ | ✓ (synthetic + motif-proxy) |
| Faithfulness / fidelity metrics | ~ | ✓ | ✓ | ✓ | ✓ (reproduced for comparability) |
| Molecular-motif-native audit (RDKit) | ✗ | ✗ | ~ | ~ | ✓ (SSSR + Murcko + BRICS) |
| Occlusion–attribution agreement | ~ | ✓ | ~ | ✓ | ✓ |
| Cross-checkpoint stability | ✗ | ✗ | ✗ | ✗ | ✓ |
| Calibration linkage | ✗ | ✗ | ✗ | ✗ | ✓ |
| **Scaffold-shift regime stratification** | ✗ | ~ | ✗ | ✗ | ✓ (the core differentiator) |
| Multiple GNN backbones (agnostic) | ~ | ✓ | ✓ | ~ | ✓ (GINE/GCN/GAT/MPNN/AttentiveFP) |
| Paired statistics (Wilcoxon, bootstrap CI) | ~ | ~ | ~ | ~ | ✓ |
| Wraps canonical implementations (no re-impl) | ✓ | ✓ | ✓ | ✓ | ✓ (Captum/PyG/RDKit) |

## The explicit delta

- **vs MolFaith** (Hiltscher, Bianciotto & Grisoni 2026, ChemRxiv,
  doi:10.26434/chemrxiv.10001594/v1, platform at github.com/molML/MolFaith):
  the closest work on the faithfulness axis, and **larger than MolSanity on that
  axis** — 8 attribution methods x 2 molecular representations x 5 architectures
  over ~14,000 molecules. We claim no broader faithfulness coverage. Their
  finding that some methods are inherently more faithful largely independently of
  architecture *converges* with ours that faithfulness does not shift
  systematically across splits (median change -0.001 over 43 paired cells). The
  delta is what that stability does and does not buy: the ordering that fails to
  survive the split is the **ground-truth** one, so a stable faithfulness ranking
  is not evidence of a stable correctness ranking. MolSanity adds correctness
  under shift, cross-checkpoint stability, calibration linkage, and
  confidence/correctness regime stratification (which locates part of the
  per-molecule faithfulness variance they report).
- **vs GraphXAI / GraphFramEx** (general GNN explanation evaluation): MolSanity is
  molecular-motif-native (RDKit) and centres the **scaffold-shift regime**, which
  general-graph frameworks do not target.
- **vs DIG** (methods + metrics library): DIG supplies implementations MolSanity
  *wraps*; MolSanity contributes the shift-stratified reliability audit on top.

## Empirical hook (validated in this repo)

On MUTAG × GINE under a scaffold split, Saliency and InputXGradient are
*faithful* (occlusion Spearman ≈ 0.38/0.40) yet **anti-aligned with the nitro
ground truth** (GT AUROC ≈ 0.03/0.04), while IG (0.54) and GNNExplainer (0.49)
recover it at similar faithfulness — a >0.5 AUROC localisation gap. Crucially,
the ranking **flips** on SynthMotifs (exact node ground truth, GINE at 100 %
accuracy): there Saliency is best (0.98), IG 0.74, GNNExplainer at chance (0.50).
No attributor is universally reliable; a faithfulness-only benchmark would miss
this regime dependence. MolSanity's ground-truth + shift view surfaces it. See
`RESULTS.md` / `BENCHMARK.md` for the computed numbers.

> References: GraphXAI (Agarwal et al., Scientific Data 10:144, 2023);
> GraphFramEx (Amara et al., LoG 2022); DIG (Liu et al., JMLR 22(240), 2021);
> MolFaith (Hiltscher, Bianciotto & Grisoni, ChemRxiv 2026,
> doi:10.26434/chemrxiv.10001594/v1); Sanchez-Lengeling et al. (NeurIPS 2020);
> MUTAG (Debnath et al., J. Med. Chem. 34(2):786-797, 1991).
