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

- **vs MolFaith** (molecular attribution *faithfulness* benchmark): MolSanity
  keeps faithfulness but adds *correctness under distribution shift*, *stability*,
  and *calibration linkage* — and stratifies all of them by confidence/correctness
  regime. Faithfulness answers "does the explanation match the model"; MolSanity
  also asks "is the model's explanation trustworthy, and where does it fail".
- **vs GraphXAI / GraphFramEx** (general GNN explanation evaluation): MolSanity is
  molecular-motif-native (RDKit) and centres the **scaffold-shift regime**, which
  general-graph frameworks do not target.
- **vs DIG** (methods + metrics library): DIG supplies implementations MolSanity
  *wraps*; MolSanity contributes the shift-stratified reliability audit on top.

## Empirical hook (validated in this repo)

On MUTAG × GINE under a scaffold split, Saliency and InputXGradient are
*faithful* (occlusion Spearman ≈ 0.38/0.40) yet **anti-aligned with the nitro
ground truth** (GT AUROC ≈ 0.03/0.04), while IG (0.54) and GNNExplainer (0.57)
recover it at similar faithfulness — a >0.5 AUROC localisation gap. A
faithfulness-only benchmark would score all four as fine; MolSanity's
ground-truth + shift view separates them. See `RESULTS.md` / `BENCHMARK.md` for
the computed numbers.

> References (to be completed with full citations in the manuscript):
> GraphXAI (Agarwal et al., 2023); GraphFramEx (Amara et al., 2022);
> DIG (Liu et al., 2021); MolFaith (molML). MUTAG (Debnath et al., 1991).
