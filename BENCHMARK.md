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
- **characterization** — GraphFramEx
- **unfaithfulness** — PyG/DIG

## Matrix

| dataset | backbone | attributor | split | n_mol | gt_auroc | occ_spearman | stability | motif_top1_share | fidelity_plus | fidelity_minus | sparsity | characterization | unfaithfulness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BACE | GINE | IntegratedGradients | scaffold | 30 | — | -0.252 | 0.386 | 0.884 | 0.074 | 0.202 | 0.780 | 0.200 | 0.047 |
| BBBP | GCN | IntegratedGradients | scaffold | 30 | — | -0.316 | 0.883 | 0.781 | 0.005 | -0.096 | 0.773 | 0.085 | 0.049 |
| BBBP | GINE | GNNExplainer | scaffold | 30 | — | -0.367 | 0.929 | 0.823 | 0.021 | -0.077 | 0.778 | 0.102 | 0.053 |
| BBBP | GINE | IntegratedGradients | scaffold | 30 | — | -0.430 | 0.699 | 0.773 | 0.006 | -0.054 | 0.775 | 0.085 | 0.151 |
| ClinTox | GINE | IntegratedGradients | scaffold | 30 | — | 0.085 | 0.859 | 0.724 | 0.356 | 0.356 | 0.755 | 0.246 | 0.386 |
| DILI | GINE | GNNExplainer | scaffold | 30 | — | -0.044 | 0.949 | 0.826 | 0.080 | 0.154 | 0.782 | 0.109 | 0.110 |
| DILI | GINE | IntegratedGradients | scaffold | 30 | — | -0.101 | 0.897 | 0.847 | 0.073 | 0.128 | 0.781 | 0.151 | 0.386 |
| ESOL | GAT | IntegratedGradients | scaffold | 20 | — | -0.481 | 0.922 | 0.799 | -0.115 | -0.995 | 0.730 | 0.215 | — |
| ESOL | GCN | IntegratedGradients | scaffold | 20 | — | -0.820 | 0.967 | 0.821 | -1.321 | -1.996 | 0.720 | 0.000 | — |
| ESOL | GINE | GNNExplainer | scaffold | 20 | — | -0.770 | 0.968 | 0.828 | -0.798 | -1.288 | 0.772 | 0.000 | — |
| ESOL | GINE | IntegratedGradients | scaffold | 20 | — | -0.798 | 0.804 | 0.834 | -1.044 | -1.235 | 0.731 | 0.000 | — |
| FreeSolv | GINE | IntegratedGradients | scaffold | 20 | — | -0.582 | 0.943 | 0.782 | -0.543 | -0.922 | 0.738 | 0.004 | — |
| Lipophilicity | GINE | IntegratedGradients | scaffold | 20 | — | -0.149 | 0.889 | 0.758 | -0.203 | -0.524 | 0.785 | 0.017 | — |
| MUTAG | AttentiveFP | IntegratedGradients | scaffold | 20 | 0.132 | -0.880 | 0.716 | 0.993 | 0.002 | 0.012 | 0.771 | 0.005 | 0.003 |
| MUTAG | GAT | IntegratedGradients | scaffold | 20 | 0.130 | 0.268 | 0.929 | 0.992 | 0.189 | 0.247 | 0.771 | 0.250 | 0.097 |
| MUTAG | GCN | IntegratedGradients | scaffold | 20 | 0.203 | 0.175 | 0.745 | 0.989 | 0.123 | 0.228 | 0.767 | 0.214 | 0.110 |
| MUTAG | GINE | GNNExplainer | scaffold | 20 | 0.491 | 0.279 | 0.986 | 0.987 | 0.113 | 0.278 | 0.771 | 0.163 | 0.373 |
| MUTAG | GINE | InputXGradient | scaffold | 20 | 0.042 | 0.398 | 0.816 | 0.998 | 0.251 | 0.225 | 0.771 | 0.277 | 0.368 |
| MUTAG | GINE | IntegratedGradients | random | 20 | 0.075 | 0.587 | 0.847 | 0.967 | 0.211 | 0.200 | 0.776 | 0.302 | 0.151 |
| MUTAG | GINE | IntegratedGradients | scaffold | 20 | 0.540 | 0.414 | 0.728 | 0.979 | 0.252 | 0.245 | 0.771 | 0.282 | 0.361 |
| MUTAG | GINE | PGExplainer | scaffold | 20 | 0.401 | 0.118 | 0.839 | 1.000 | 0.026 | 0.294 | 0.755 | 0.059 | — |
| MUTAG | GINE | Saliency | random | 20 | 0.022 | 0.541 | 0.870 | 0.983 | 0.209 | 0.203 | 0.770 | 0.298 | 0.156 |
| MUTAG | GINE | Saliency | scaffold | 20 | 0.026 | 0.376 | 0.931 | 0.997 | 0.267 | 0.230 | 0.771 | 0.285 | 0.369 |
| MUTAG | MPNN | IntegratedGradients | scaffold | 20 | 0.356 | 0.191 | 0.885 | 0.985 | 0.263 | 0.312 | 0.768 | 0.256 | 0.284 |
| SIDER | GCN | IntegratedGradients | scaffold | 30 | — | -0.512 | 0.893 | 0.843 | 0.014 | -0.059 | 0.716 | 0.073 | 0.023 |
| SIDER | GINE | GNNExplainer | scaffold | 30 | — | 0.490 | 0.845 | 0.816 | 0.038 | 0.196 | 0.732 | 0.111 | 0.252 |
| SIDER | GINE | IntegratedGradients | scaffold | 30 | — | 0.493 | 0.875 | 0.836 | 0.068 | 0.196 | 0.715 | 0.160 | 0.499 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 20 | 0.498 | -0.017 | 0.934 | 0.043 | 0.101 | 0.099 | 0.800 | 0.162 | 0.041 |
| SynthMotifs | GINE | InputXGradient | scaffold | 20 | 0.964 | 0.014 | 0.692 | 0.220 | 0.114 | 0.102 | 0.795 | 0.200 | 0.040 |
| SynthMotifs | GINE | IntegratedGradients | random | 20 | 0.590 | -0.026 | 0.753 | 0.194 | 0.102 | 0.211 | 0.785 | 0.219 | 0.122 |
| SynthMotifs | GINE | IntegratedGradients | scaffold | 20 | 0.742 | 0.073 | 0.656 | 0.225 | 0.109 | 0.100 | 0.792 | 0.203 | 0.040 |
| SynthMotifs | GINE | PGExplainer | scaffold | 20 | 0.360 | 0.106 | 0.701 | 0.393 | 0.064 | 0.126 | 0.787 | 0.106 | — |
| SynthMotifs | GINE | Saliency | scaffold | 20 | 0.983 | 0.022 | 0.509 | 0.199 | 0.123 | 0.074 | 0.778 | 0.197 | 0.042 |
| hERG | GCN | IntegratedGradients | scaffold | 30 | — | 0.711 | 0.910 | 0.665 | 0.589 | 0.590 | 0.776 | 0.368 | 0.641 |
| hERG | GINE | IntegratedGradients | scaffold | 30 | — | 0.431 | 0.956 | 0.673 | 0.411 | 0.408 | 0.784 | 0.311 | 0.582 |

## Paired attributor comparisons (Wilcoxon, shared molecules)

**BBBP · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 30 | 0.060 | 0.727 |

**DILI · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 29 | 0.066 | 0.209 |

**ESOL · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 19 | 0.000 | 0.139 |

**MUTAG · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| IntegratedGradients | Saliency | 20 | 0.000 | 0.049 |

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

**SIDER · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 25 | 0.000 | 0.398 |

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

