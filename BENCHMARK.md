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
| BACE | GCN | IntegratedGradients | scaffold | 30 | — | 0.766 | 0.873 | 0.776 | 0.597 | 0.597 | 0.785 | 0.370 | 0.619 |
| BACE | GINE | GNNExplainer | scaffold | 30 | — | -0.128 | 0.932 | 0.835 | 0.064 | 0.214 | 0.786 | 0.223 | 0.036 |
| BACE | GINE | InputXGradient | scaffold | 30 | — | -0.159 | 0.640 | 0.841 | 0.079 | 0.171 | 0.783 | 0.165 | 0.049 |
| BACE | GINE | IntegratedGradients | scaffold | 30 | — | -0.252 | 0.386 | 0.884 | 0.074 | 0.202 | 0.780 | 0.200 | 0.047 |
| BACE | GINE | Saliency | scaffold | 30 | — | -0.174 | 0.579 | 0.873 | 0.097 | 0.173 | 0.785 | 0.196 | 0.045 |
| BBBP | GAT | IntegratedGradients | scaffold | 30 | — | -0.808 | 0.944 | 0.810 | -0.069 | -0.069 | 0.778 | 0.000 | 0.063 |
| BBBP | GCN | IntegratedGradients | scaffold | 30 | — | -0.316 | 0.883 | 0.781 | 0.005 | -0.096 | 0.773 | 0.085 | 0.049 |
| BBBP | GINE | GNNExplainer | scaffold | 30 | — | -0.367 | 0.929 | 0.823 | 0.021 | -0.077 | 0.778 | 0.102 | 0.053 |
| BBBP | GINE | GuidedBackprop | scaffold | 30 | — | -0.530 | 0.890 | 0.876 | -0.016 | -0.037 | 0.775 | 0.061 | 0.084 |
| BBBP | GINE | InputXGradient | scaffold | 30 | — | -0.620 | 0.897 | 0.839 | -0.016 | -0.047 | 0.769 | 0.063 | 0.110 |
| BBBP | GINE | IntegratedGradients | scaffold | 30 | — | -0.430 | 0.699 | 0.773 | 0.006 | -0.054 | 0.775 | 0.085 | 0.151 |
| BBBP | GINE | PGExplainer | scaffold | 30 | — | -0.185 | 0.387 | 0.422 | -0.055 | -0.059 | 0.635 | 0.000 | — |
| BBBP | GINE | Saliency | scaffold | 30 | — | -0.627 | 0.873 | 0.826 | -0.029 | -0.033 | 0.773 | 0.051 | 0.100 |
| ClinTox | GINE | GNNExplainer | scaffold | 30 | — | 0.927 | 0.963 | 0.483 | 0.375 | 0.356 | 0.848 | 0.246 | 0.394 |
| ClinTox | GINE | InputXGradient | scaffold | 30 | — | 0.139 | 0.583 | 0.793 | 0.356 | 0.356 | 0.749 | 0.246 | 0.388 |
| ClinTox | GINE | IntegratedGradients | scaffold | 30 | — | 0.085 | 0.859 | 0.724 | 0.356 | 0.356 | 0.755 | 0.246 | 0.386 |
| ClinTox | GINE | Saliency | scaffold | 30 | — | 0.145 | 0.570 | 0.790 | 0.356 | 0.356 | 0.749 | 0.246 | 0.382 |
| DILI | GINE | GNNExplainer | scaffold | 30 | — | -0.044 | 0.949 | 0.826 | 0.080 | 0.154 | 0.782 | 0.109 | 0.110 |
| DILI | GINE | InputXGradient | scaffold | 30 | — | -0.126 | 0.923 | 0.858 | 0.075 | 0.122 | 0.780 | 0.147 | 0.388 |
| DILI | GINE | IntegratedGradients | scaffold | 30 | — | -0.101 | 0.897 | 0.847 | 0.073 | 0.128 | 0.781 | 0.151 | 0.386 |
| DILI | GINE | Saliency | scaffold | 30 | — | -0.128 | 0.910 | 0.851 | 0.056 | 0.134 | 0.782 | 0.136 | 0.385 |
| ESOL | GAT | IntegratedGradients | scaffold | 20 | — | -0.481 | 0.922 | 0.799 | -0.115 | -0.995 | 0.730 | 0.215 | — |
| ESOL | GCN | IntegratedGradients | scaffold | 20 | — | -0.820 | 0.967 | 0.821 | -1.321 | -1.996 | 0.720 | 0.000 | — |
| ESOL | GINE | GNNExplainer | scaffold | 20 | — | -0.770 | 0.968 | 0.828 | -0.798 | -1.288 | 0.772 | 0.000 | — |
| ESOL | GINE | GuidedBackprop | scaffold | 20 | — | -0.741 | 0.882 | 0.659 | -0.582 | -1.326 | 0.789 | 0.001 | — |
| ESOL | GINE | InputXGradient | scaffold | 20 | — | -0.793 | 0.801 | 0.881 | -1.016 | -1.219 | 0.722 | 0.000 | — |
| ESOL | GINE | IntegratedGradients | scaffold | 20 | — | -0.798 | 0.804 | 0.834 | -1.044 | -1.235 | 0.731 | 0.000 | — |
| ESOL | GINE | Saliency | scaffold | 20 | — | -0.798 | 0.829 | 0.878 | -0.996 | -1.234 | 0.727 | 0.000 | — |
| FreeSolv | GCN | IntegratedGradients | scaffold | 20 | — | -0.434 | 0.857 | 0.782 | -0.046 | -0.935 | 0.745 | 0.077 | — |
| FreeSolv | GINE | GNNExplainer | scaffold | 20 | — | -0.600 | 1.000 | 0.766 | -0.424 | -0.985 | 0.755 | 0.006 | — |
| FreeSolv | GINE | InputXGradient | scaffold | 20 | — | -0.370 | 0.754 | 0.805 | -0.364 | -0.943 | 0.714 | 0.000 | — |
| FreeSolv | GINE | IntegratedGradients | scaffold | 20 | — | -0.582 | 0.943 | 0.782 | -0.543 | -0.922 | 0.738 | 0.004 | — |
| FreeSolv | GINE | Saliency | scaffold | 20 | — | -0.425 | 0.843 | 0.789 | -0.371 | -0.939 | 0.736 | 0.004 | — |
| Lipophilicity | GAT | IntegratedGradients | scaffold | 20 | — | 0.458 | 0.812 | 0.762 | -0.144 | 0.482 | 0.785 | 0.092 | — |
| Lipophilicity | GINE | GNNExplainer | scaffold | 20 | — | -0.499 | 0.867 | 0.845 | -0.251 | -0.500 | 0.788 | 0.003 | — |
| Lipophilicity | GINE | InputXGradient | scaffold | 20 | — | -0.439 | 0.465 | 0.699 | -0.281 | -0.510 | 0.787 | 0.006 | — |
| Lipophilicity | GINE | IntegratedGradients | scaffold | 20 | — | -0.149 | 0.889 | 0.758 | -0.203 | -0.524 | 0.785 | 0.017 | — |
| Lipophilicity | GINE | Saliency | scaffold | 20 | — | -0.469 | 0.536 | 0.705 | -0.299 | -0.468 | 0.788 | 0.002 | — |
| MUTAG | AttentiveFP | IntegratedGradients | scaffold | 20 | 0.132 | -0.880 | 0.716 | 0.993 | 0.002 | 0.012 | 0.771 | 0.005 | 0.003 |
| MUTAG | GAT | IntegratedGradients | scaffold | 20 | 0.130 | 0.268 | 0.929 | 0.992 | 0.189 | 0.247 | 0.771 | 0.250 | 0.097 |
| MUTAG | GCN | IntegratedGradients | scaffold | 20 | 0.203 | 0.175 | 0.745 | 0.989 | 0.123 | 0.228 | 0.767 | 0.214 | 0.110 |
| MUTAG | GINE | GNNExplainer | scaffold | 20 | 0.491 | 0.279 | 0.986 | 0.987 | 0.113 | 0.278 | 0.771 | 0.163 | 0.373 |
| MUTAG | GINE | GuidedBackprop | scaffold | 20 | 0.112 | 0.341 | 0.903 | 0.990 | 0.272 | 0.229 | 0.771 | 0.284 | 0.369 |
| MUTAG | GINE | InputXGradient | scaffold | 20 | 0.042 | 0.398 | 0.816 | 0.998 | 0.251 | 0.225 | 0.771 | 0.277 | 0.368 |
| MUTAG | GINE | IntegratedGradients | random | 20 | 0.075 | 0.587 | 0.847 | 0.967 | 0.211 | 0.200 | 0.776 | 0.302 | 0.151 |
| MUTAG | GINE | IntegratedGradients | scaffold | 20 | 0.540 | 0.414 | 0.728 | 0.979 | 0.252 | 0.245 | 0.771 | 0.282 | 0.361 |
| MUTAG | GINE | PGExplainer | scaffold | 20 | 0.401 | 0.118 | 0.839 | 1.000 | 0.026 | 0.294 | 0.755 | 0.059 | — |
| MUTAG | GINE | Saliency | random | 20 | 0.022 | 0.541 | 0.870 | 0.983 | 0.209 | 0.203 | 0.770 | 0.298 | 0.156 |
| MUTAG | GINE | Saliency | scaffold | 20 | 0.026 | 0.376 | 0.931 | 0.997 | 0.267 | 0.230 | 0.771 | 0.285 | 0.369 |
| MUTAG | MPNN | IntegratedGradients | scaffold | 20 | 0.356 | 0.191 | 0.885 | 0.985 | 0.263 | 0.312 | 0.768 | 0.256 | 0.284 |
| SIDER | GCN | IntegratedGradients | scaffold | 30 | — | -0.512 | 0.893 | 0.843 | 0.014 | -0.059 | 0.716 | 0.073 | 0.023 |
| SIDER | GINE | GNNExplainer | scaffold | 30 | — | 0.490 | 0.845 | 0.816 | 0.038 | 0.196 | 0.732 | 0.111 | 0.252 |
| SIDER | GINE | InputXGradient | scaffold | 30 | — | 0.576 | 0.724 | 0.878 | 0.088 | 0.196 | 0.716 | 0.176 | 0.499 |
| SIDER | GINE | IntegratedGradients | scaffold | 30 | — | 0.493 | 0.875 | 0.836 | 0.068 | 0.196 | 0.715 | 0.160 | 0.499 |
| SIDER | GINE | Saliency | scaffold | 30 | — | 0.571 | 0.753 | 0.887 | 0.093 | 0.201 | 0.720 | 0.180 | 0.498 |
| SynthMotifs | AttentiveFP | IntegratedGradients | scaffold | 20 | 0.821 | 0.643 | 0.659 | 0.141 | 0.014 | 0.072 | 0.793 | 0.065 | 0.015 |
| SynthMotifs | GAT | IntegratedGradients | scaffold | 20 | 0.718 | 0.527 | 0.568 | 0.177 | 0.102 | 0.047 | 0.790 | 0.195 | 0.045 |
| SynthMotifs | GCN | IntegratedGradients | scaffold | 20 | 0.920 | 0.096 | 0.448 | 0.168 | 0.055 | 0.040 | 0.793 | 0.125 | 0.014 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 20 | 0.498 | -0.017 | 0.934 | 0.043 | 0.101 | 0.099 | 0.800 | 0.162 | 0.041 |
| SynthMotifs | GINE | GuidedBackprop | scaffold | 20 | 0.966 | 0.059 | 0.346 | 0.152 | 0.118 | 0.086 | 0.797 | 0.202 | 0.041 |
| SynthMotifs | GINE | InputXGradient | scaffold | 20 | 0.964 | 0.014 | 0.692 | 0.220 | 0.114 | 0.102 | 0.795 | 0.200 | 0.040 |
| SynthMotifs | GINE | IntegratedGradients | random | 20 | 0.590 | -0.026 | 0.753 | 0.194 | 0.102 | 0.211 | 0.785 | 0.219 | 0.122 |
| SynthMotifs | GINE | IntegratedGradients | scaffold | 20 | 0.742 | 0.073 | 0.656 | 0.225 | 0.109 | 0.100 | 0.792 | 0.203 | 0.040 |
| SynthMotifs | GINE | PGExplainer | scaffold | 20 | 0.360 | 0.106 | 0.701 | 0.393 | 0.064 | 0.126 | 0.787 | 0.106 | — |
| SynthMotifs | GINE | Saliency | scaffold | 20 | 0.983 | 0.022 | 0.509 | 0.199 | 0.123 | 0.074 | 0.778 | 0.197 | 0.042 |
| SynthMotifs | MPNN | IntegratedGradients | scaffold | 20 | 0.807 | -0.104 | 0.894 | 0.224 | 0.041 | 0.030 | 0.798 | 0.262 | 0.132 |
| Tox21 | GINE | GNNExplainer | scaffold | 30 | — | 0.010 | 1.000 | 0.719 | -0.066 | -0.061 | 0.786 | 0.002 | 0.171 |
| Tox21 | GINE | InputXGradient | scaffold | 30 | — | -0.409 | 0.809 | 0.704 | -0.075 | -0.060 | 0.780 | 0.001 | 0.211 |
| Tox21 | GINE | IntegratedGradients | scaffold | 30 | — | -0.339 | 0.664 | 0.713 | -0.080 | -0.062 | 0.779 | 0.001 | 0.211 |
| Tox21 | GINE | Saliency | scaffold | 30 | — | -0.391 | 0.760 | 0.697 | -0.073 | -0.063 | 0.780 | 0.002 | 0.208 |
| hERG | GCN | IntegratedGradients | scaffold | 30 | — | 0.711 | 0.910 | 0.665 | 0.589 | 0.590 | 0.776 | 0.368 | 0.641 |
| hERG | GINE | GNNExplainer | scaffold | 30 | — | 0.066 | 0.950 | 0.725 | 0.094 | 0.408 | 0.786 | 0.149 | 0.575 |
| hERG | GINE | InputXGradient | scaffold | 30 | — | 0.342 | 0.671 | 0.633 | 0.410 | 0.408 | 0.779 | 0.310 | 0.582 |
| hERG | GINE | IntegratedGradients | scaffold | 30 | — | 0.431 | 0.956 | 0.673 | 0.411 | 0.408 | 0.784 | 0.311 | 0.582 |
| hERG | GINE | Saliency | scaffold | 30 | — | 0.343 | 0.656 | 0.626 | 0.409 | 0.408 | 0.784 | 0.311 | 0.583 |

## Paired attributor comparisons (Wilcoxon, shared molecules)

**BACE · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | InputXGradient | 30 | -0.039 | 0.918 |
| GNNExplainer | IntegratedGradients | 30 | 0.070 | 0.015 |
| GNNExplainer | Saliency | 30 | -0.108 | 1.000 |
| InputXGradient | IntegratedGradients | 30 | 0.142 | 0.271 |
| InputXGradient | Saliency | 30 | 0.000 | 0.936 |
| IntegratedGradients | Saliency | 30 | -0.140 | 0.179 |

**BBBP · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 30 | 0.036 | 0.092 |
| GNNExplainer | InputXGradient | 30 | 0.103 | 0.001 |
| GNNExplainer | IntegratedGradients | 30 | 0.060 | 0.727 |
| GNNExplainer | PGExplainer | 14 | 0.036 | 0.808 |
| GNNExplainer | Saliency | 30 | 0.086 | 0.006 |
| GuidedBackprop | InputXGradient | 30 | 0.012 | 0.011 |
| GuidedBackprop | IntegratedGradients | 30 | 0.000 | 0.305 |
| GuidedBackprop | PGExplainer | 14 | 0.037 | 0.463 |
| GuidedBackprop | Saliency | 30 | 0.000 | 0.026 |
| InputXGradient | IntegratedGradients | 30 | -0.024 | 0.005 |
| InputXGradient | PGExplainer | 14 | -0.062 | 0.311 |
| InputXGradient | Saliency | 30 | 0.000 | 0.099 |
| IntegratedGradients | PGExplainer | 14 | 0.013 | 0.345 |
| IntegratedGradients | Saliency | 30 | 0.024 | 0.011 |
| PGExplainer | Saliency | 14 | 0.059 | 0.311 |

**ClinTox · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | InputXGradient | 13 | 0.048 | 0.055 |
| GNNExplainer | IntegratedGradients | 13 | 0.000 | 0.047 |
| GNNExplainer | Saliency | 13 | 0.048 | 0.055 |
| InputXGradient | IntegratedGradients | 24 | 0.000 | 0.653 |
| InputXGradient | Saliency | 24 | 0.000 | 0.068 |
| IntegratedGradients | Saliency | 24 | 0.000 | 0.619 |

**DILI · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | InputXGradient | 29 | 0.116 | 0.050 |
| GNNExplainer | IntegratedGradients | 29 | 0.066 | 0.209 |
| GNNExplainer | Saliency | 29 | 0.109 | 0.038 |
| InputXGradient | IntegratedGradients | 29 | 0.000 | 0.233 |
| InputXGradient | Saliency | 29 | 0.000 | 0.441 |
| IntegratedGradients | Saliency | 29 | 0.000 | 0.170 |

**ESOL · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 15 | 0.000 | 0.600 |
| GNNExplainer | InputXGradient | 19 | 0.000 | 0.214 |
| GNNExplainer | IntegratedGradients | 19 | 0.000 | 0.139 |
| GNNExplainer | Saliency | 19 | 0.000 | 0.139 |
| GuidedBackprop | InputXGradient | 15 | 0.000 | 0.465 |
| GuidedBackprop | IntegratedGradients | 15 | 0.000 | 0.223 |
| GuidedBackprop | Saliency | 15 | 0.000 | 0.223 |
| InputXGradient | IntegratedGradients | 19 | 0.000 | 0.317 |
| InputXGradient | Saliency | 19 | 0.000 | 0.317 |
| IntegratedGradients | Saliency | 19 | 0.000 | — |

**FreeSolv · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | InputXGradient | 14 | 0.000 | 0.109 |
| GNNExplainer | IntegratedGradients | 14 | 0.000 | 0.465 |
| GNNExplainer | Saliency | 14 | 0.000 | 0.109 |
| InputXGradient | IntegratedGradients | 14 | 0.000 | 0.109 |
| InputXGradient | Saliency | 14 | 0.000 | 0.317 |
| IntegratedGradients | Saliency | 14 | 0.000 | 0.180 |

**Lipophilicity · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | InputXGradient | 20 | -0.108 | 0.573 |
| GNNExplainer | IntegratedGradients | 20 | -0.444 | 0.003 |
| GNNExplainer | Saliency | 20 | -0.112 | 0.717 |
| InputXGradient | IntegratedGradients | 20 | -0.058 | 0.028 |
| InputXGradient | Saliency | 20 | 0.000 | 0.382 |
| IntegratedGradients | Saliency | 20 | 0.100 | 0.031 |

**MUTAG · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| IntegratedGradients | Saliency | 20 | 0.000 | 0.049 |

**MUTAG · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 20 | -0.107 | 0.512 |
| GNNExplainer | InputXGradient | 20 | -0.036 | 0.198 |
| GNNExplainer | IntegratedGradients | 20 | -0.018 | 0.152 |
| GNNExplainer | PGExplainer | 20 | 0.200 | 0.020 |
| GNNExplainer | Saliency | 20 | -0.036 | 0.233 |
| GuidedBackprop | InputXGradient | 20 | 0.000 | 0.196 |
| GuidedBackprop | IntegratedGradients | 20 | 0.000 | 0.211 |
| GuidedBackprop | PGExplainer | 20 | 0.268 | 0.123 |
| GuidedBackprop | Saliency | 20 | 0.000 | 0.559 |
| InputXGradient | IntegratedGradients | 20 | 0.000 | 1.000 |
| InputXGradient | PGExplainer | 20 | 0.468 | 0.052 |
| InputXGradient | Saliency | 20 | 0.000 | 0.102 |
| IntegratedGradients | PGExplainer | 20 | 0.468 | 0.047 |
| IntegratedGradients | Saliency | 20 | 0.000 | 0.206 |
| PGExplainer | Saliency | 20 | -0.468 | 0.063 |

**SIDER · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | InputXGradient | 25 | -0.100 | 0.095 |
| GNNExplainer | IntegratedGradients | 25 | 0.000 | 0.398 |
| GNNExplainer | Saliency | 25 | -0.102 | 0.136 |
| InputXGradient | IntegratedGradients | 25 | 0.048 | 0.192 |
| InputXGradient | Saliency | 25 | 0.000 | 0.799 |
| IntegratedGradients | Saliency | 25 | -0.048 | 0.192 |

**SynthMotifs · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 20 | 0.202 | 0.388 |
| GNNExplainer | InputXGradient | 20 | 0.206 | 0.648 |
| GNNExplainer | IntegratedGradients | 20 | 0.124 | 0.368 |
| GNNExplainer | PGExplainer | 20 | -0.147 | 0.097 |
| GNNExplainer | Saliency | 20 | 0.001 | 0.648 |
| GuidedBackprop | InputXGradient | 20 | 0.007 | 0.546 |
| GuidedBackprop | IntegratedGradients | 20 | -0.006 | 0.729 |
| GuidedBackprop | PGExplainer | 20 | -0.051 | 0.784 |
| GuidedBackprop | Saliency | 20 | 0.050 | 0.261 |
| InputXGradient | IntegratedGradients | 20 | -0.024 | 0.198 |
| InputXGradient | PGExplainer | 20 | -0.055 | 0.430 |
| InputXGradient | Saliency | 20 | 0.013 | 0.927 |
| IntegratedGradients | PGExplainer | 20 | -0.102 | 0.784 |
| IntegratedGradients | Saliency | 20 | 0.094 | 0.123 |
| PGExplainer | Saliency | 20 | -0.026 | 0.546 |

**Tox21 · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | InputXGradient | 28 | 0.062 | 0.006 |
| GNNExplainer | IntegratedGradients | 28 | 0.029 | 0.016 |
| GNNExplainer | Saliency | 28 | 0.129 | 0.006 |
| InputXGradient | IntegratedGradients | 28 | 0.000 | 0.575 |
| InputXGradient | Saliency | 28 | 0.000 | 0.600 |
| IntegratedGradients | Saliency | 28 | 0.000 | 0.445 |

**hERG · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | InputXGradient | 30 | -0.150 | 0.015 |
| GNNExplainer | IntegratedGradients | 30 | -0.349 | 0.000 |
| GNNExplainer | Saliency | 30 | -0.117 | 0.014 |
| InputXGradient | IntegratedGradients | 30 | -0.036 | 0.110 |
| InputXGradient | Saliency | 30 | 0.000 | 0.814 |
| IntegratedGradients | Saliency | 30 | 0.060 | 0.094 |

