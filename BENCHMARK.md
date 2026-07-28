# BENCHMARK.md — head-to-head audit matrix

> Computed from per-molecule audit records under `artifacts/audit/`.
> MolSanity metrics sit alongside the field-standard Fidelity±/sparsity
> on the **same molecules**. GT AUROC is defined only where ground truth
> exists (Tier-1). `—` = undefined/not-applicable, never a fabricated 0.

## Attribution provenance

- **gt_auroc** — MolSanity/GT
- **occ_spearman** — MolSanity/faithfulness
- **stability** — MolSanity/stability
- **motif_top1_share** — MolSanity/coherence
- **fidelity_plus** — field-standard
- **fidelity_minus** — field-standard
- **sparsity** — field-standard

## Matrix

| dataset | backbone | attributor | split | n_mol | gt_auroc | occ_spearman | stability | motif_top1_share | fidelity_plus | fidelity_minus | sparsity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BBBP | GINE | IntegratedGradients | scaffold | 20 | — | -0.613 | 0.887 | 0.862 | -0.095 | -0.175 | 0.773 |
| ESOL | GINE | GNNExplainer | scaffold | 20 | — | -0.770 | 0.968 | 0.828 | -0.798 | -1.288 | 0.772 |
| ESOL | GINE | IntegratedGradients | scaffold | 20 | — | -0.798 | 0.804 | 0.834 | -1.044 | -1.235 | 0.731 |
| FreeSolv | GINE | IntegratedGradients | scaffold | 20 | — | -0.582 | 0.943 | 0.782 | -0.543 | -0.922 | 0.738 |
| MUTAG | AttentiveFP | IntegratedGradients | scaffold | 20 | 0.132 | -0.880 | 0.716 | 0.993 | 0.002 | 0.012 | 0.771 |
| MUTAG | GAT | IntegratedGradients | scaffold | 20 | 0.130 | 0.268 | 0.929 | 0.992 | 0.189 | 0.247 | 0.771 |
| MUTAG | GCN | IntegratedGradients | scaffold | 20 | 0.203 | 0.175 | 0.745 | 0.989 | 0.123 | 0.228 | 0.767 |
| MUTAG | GINE | GNNExplainer | scaffold | 20 | 0.491 | 0.279 | 0.986 | 0.987 | 0.113 | 0.278 | 0.771 |
| MUTAG | GINE | InputXGradient | scaffold | 20 | 0.042 | 0.398 | 0.816 | 0.998 | 0.251 | 0.225 | 0.771 |
| MUTAG | GINE | IntegratedGradients | scaffold | 20 | 0.540 | 0.414 | 0.728 | 0.979 | 0.252 | 0.245 | 0.771 |
| MUTAG | GINE | PGExplainer | scaffold | 20 | 0.401 | 0.118 | 0.839 | 1.000 | 0.026 | 0.294 | 0.755 |
| MUTAG | GINE | Saliency | scaffold | 20 | 0.026 | 0.376 | 0.931 | 0.997 | 0.267 | 0.230 | 0.771 |
| MUTAG | MPNN | IntegratedGradients | scaffold | 20 | 0.356 | 0.191 | 0.885 | 0.985 | 0.263 | 0.312 | 0.768 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 20 | 0.498 | -0.017 | 0.934 | 0.043 | 0.101 | 0.099 | 0.800 |
| SynthMotifs | GINE | InputXGradient | scaffold | 20 | 0.964 | 0.014 | 0.692 | 0.220 | 0.114 | 0.102 | 0.795 |
| SynthMotifs | GINE | IntegratedGradients | scaffold | 20 | 0.742 | 0.073 | 0.656 | 0.225 | 0.109 | 0.100 | 0.792 |
| SynthMotifs | GINE | PGExplainer | scaffold | 20 | 0.360 | 0.106 | 0.701 | 0.393 | 0.064 | 0.126 | 0.787 |
| SynthMotifs | GINE | Saliency | scaffold | 20 | 0.983 | 0.022 | 0.509 | 0.199 | 0.123 | 0.074 | 0.778 |

## Paired attributor comparisons (Wilcoxon, shared molecules)

**ESOL · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 19 | 0.000 | 0.139 |

**MUTAG · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | InputXGradient | 20 | -0.036 | 0.198 |
| GNNExplainer | IntegratedGradients | 20 | -0.018 | 0.152 |
| GNNExplainer | PGExplainer | 20 | 0.200 | 0.020 |
| GNNExplainer | Saliency | 20 | -0.036 | 0.233 |
| InputXGradient | IntegratedGradients | 20 | 0.000 | 1.000 |
| InputXGradient | PGExplainer | 20 | 0.468 | 0.052 |
| InputXGradient | Saliency | 20 | 0.000 | 0.102 |
| IntegratedGradients | PGExplainer | 20 | 0.468 | 0.047 |
| IntegratedGradients | Saliency | 20 | 0.000 | 0.206 |
| PGExplainer | Saliency | 20 | -0.468 | 0.063 |

**SynthMotifs · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | InputXGradient | 20 | 0.206 | 0.648 |
| GNNExplainer | IntegratedGradients | 20 | 0.124 | 0.368 |
| GNNExplainer | PGExplainer | 20 | -0.147 | 0.097 |
| GNNExplainer | Saliency | 20 | 0.001 | 0.648 |
| InputXGradient | IntegratedGradients | 20 | -0.024 | 0.198 |
| InputXGradient | PGExplainer | 20 | -0.055 | 0.430 |
| InputXGradient | Saliency | 20 | 0.013 | 0.927 |
| IntegratedGradients | PGExplainer | 20 | -0.102 | 0.784 |
| IntegratedGradients | Saliency | 20 | 0.094 | 0.123 |
| PGExplainer | Saliency | 20 | -0.026 | 0.546 |

