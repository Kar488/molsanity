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
| BA-2Motifs | GINE | IntegratedGradients | random | 100 | — | -0.393 | 0.745 | 0.209 | 0.037 | 0.001 | 0.800 | 0.132 | — |
| BA-2Motifs | GINE | IntegratedGradients | scaffold | 100 | — | 0.636 | 0.740 | 0.119 | 0.022 | 0.029 | 0.799 | 0.044 | — |
| BACE | GCN | IntegratedGradients | random | 100 | — | 0.034 | 0.738 | 0.792 | 0.181 | 0.218 | 0.785 | 0.209 | 0.268 |
| BACE | GCN | IntegratedGradients | scaffold | 100 | — | -0.668 | 0.898 | 0.800 | -0.125 | -0.125 | 0.785 | 0.067 | 0.276 |
| BACE | GINE | IntegratedGradients | random | 100 | — | 0.307 | 0.844 | 0.844 | 0.347 | 0.278 | 0.786 | 0.366 | 0.219 |
| BACE | GINE | IntegratedGradients | scaffold | 100 | — | 0.389 | 0.571 | 0.843 | 0.104 | 0.092 | 0.783 | 0.184 | 0.066 |
| BBBP | AttentiveFP | IntegratedGradients | random | 100 | — | 0.339 | 0.844 | 0.750 | 0.164 | 0.167 | 0.774 | 0.234 | 0.203 |
| BBBP | AttentiveFP | IntegratedGradients | scaffold | 100 | — | 0.284 | 0.766 | 0.841 | 0.036 | 0.015 | 0.776 | 0.082 | 0.074 |
| BBBP | GAT | IntegratedGradients | random | 100 | — | 0.043 | 0.944 | 0.770 | 0.328 | 0.328 | 0.780 | 0.105 | 0.243 |
| BBBP | GAT | IntegratedGradients | scaffold | 100 | — | -0.712 | 0.953 | 0.831 | -0.021 | -0.050 | 0.772 | 0.021 | 0.055 |
| BBBP | GCN | IntegratedGradients | random | 100 | — | 0.023 | 0.874 | 0.768 | 0.311 | 0.318 | 0.774 | 0.122 | 0.349 |
| BBBP | GCN | IntegratedGradients | scaffold | 100 | — | -0.812 | 0.884 | 0.814 | -0.010 | -0.145 | 0.772 | 0.065 | 0.271 |
| BBBP | GINE | GNNExplainer | random | 100 | — | -0.061 | 0.951 | 0.779 | 0.287 | 0.333 | 0.781 | 0.097 | 0.315 |
| BBBP | GINE | GNNExplainer | scaffold | 100 | — | -0.368 | 0.791 | 0.848 | 0.018 | -0.064 | 0.779 | 0.044 | 0.073 |
| BBBP | GINE | IntegratedGradients | random | 100 | — | 0.016 | 0.827 | 0.724 | 0.332 | 0.334 | 0.776 | 0.098 | 0.394 |
| BBBP | GINE | IntegratedGradients | scaffold | 100 | — | -0.741 | 0.857 | 0.841 | -0.031 | -0.057 | 0.774 | 0.028 | 0.090 |
| BBBP | GINE | PGExplainer | random | 100 | — | -0.050 | 0.562 | 0.927 | 0.086 | 0.332 | 0.761 | 0.075 | — |
| BBBP | GINE | PGExplainer | scaffold | 100 | — | -0.538 | 0.488 | 0.954 | -0.016 | -0.060 | 0.770 | 0.031 | — |
| BBBP | MPNN | IntegratedGradients | random | 100 | — | 0.154 | 0.765 | 0.792 | 0.210 | 0.267 | 0.774 | 0.121 | 0.104 |
| BBBP | MPNN | IntegratedGradients | scaffold | 100 | — | -0.431 | 0.832 | 0.824 | 0.052 | -0.043 | 0.775 | 0.117 | 0.096 |
| ClinTox | GINE | GNNExplainer | random | 100 | — | 0.059 | 0.984 | 0.504 | 0.258 | 0.230 | 0.855 | 0.108 | 0.323 |
| ClinTox | GINE | GNNExplainer | scaffold | 100 | — | -0.242 | 0.983 | 0.728 | 0.139 | 0.135 | 0.785 | 0.128 | 0.289 |
| ClinTox | GINE | IntegratedGradients | random | 100 | — | -0.223 | 0.983 | 0.754 | 0.230 | 0.230 | 0.778 | 0.108 | 0.119 |
| ClinTox | GINE | IntegratedGradients | scaffold | 100 | — | -0.329 | 0.991 | 0.745 | 0.135 | 0.135 | 0.772 | 0.128 | 0.254 |
| DILI | GINE | IntegratedGradients | random | 48 | — | 0.298 | 0.780 | 0.760 | 0.354 | 0.360 | 0.778 | 0.383 | 0.393 |
| DILI | GINE | IntegratedGradients | scaffold | 48 | — | 0.346 | 0.941 | 0.852 | 0.194 | 0.229 | 0.774 | 0.276 | 0.428 |
| ESOL | GAT | IntegratedGradients | random | 100 | — | 0.845 | 0.908 | 0.850 | 3.524 | 6.515 | 0.715 | 0.020 | — |
| ESOL | GAT | IntegratedGradients | scaffold | 100 | — | 0.862 | 0.935 | 0.838 | 5.007 | 9.467 | 0.726 | 0.000 | — |
| ESOL | GCN | IntegratedGradients | random | 100 | — | -0.534 | 0.936 | 0.870 | -0.827 | -0.916 | 0.710 | 0.009 | — |
| ESOL | GCN | IntegratedGradients | scaffold | 100 | — | -0.509 | 0.965 | 0.870 | -0.882 | -1.277 | 0.724 | 0.024 | — |
| ESOL | GINE | GNNExplainer | random | 100 | — | -0.873 | 0.948 | 0.868 | -1.346 | -2.714 | 0.753 | 0.000 | — |
| ESOL | GINE | GNNExplainer | scaffold | 100 | — | -0.739 | 0.974 | 0.853 | -0.913 | -2.167 | 0.763 | 0.000 | — |
| ESOL | GINE | IntegratedGradients | random | 100 | — | -0.944 | 0.960 | 0.878 | -1.733 | -2.430 | 0.719 | 0.000 | — |
| ESOL | GINE | IntegratedGradients | scaffold | 100 | — | -0.778 | 0.954 | 0.878 | -1.391 | -1.986 | 0.720 | 0.000 | — |
| FreeSolv | GINE | IntegratedGradients | random | 65 | — | -0.418 | 0.847 | 0.864 | -0.661 | -1.021 | 0.710 | 0.047 | — |
| FreeSolv | GINE | IntegratedGradients | scaffold | 65 | — | -0.589 | 0.877 | 0.872 | -0.503 | -1.066 | 0.726 | 0.031 | — |
| Lipophilicity | GINE | IntegratedGradients | random | 100 | — | 0.464 | 0.832 | 0.775 | 0.516 | 0.509 | 0.778 | 0.296 | — |
| Lipophilicity | GINE | IntegratedGradients | scaffold | 100 | — | 0.575 | 0.863 | 0.760 | 1.033 | 1.954 | 0.781 | 0.053 | — |
| MUTAG | AttentiveFP | IntegratedGradients | random | 20 | 0.055 | 0.920 | 0.876 | 0.943 | 0.009 | 0.019 | 0.774 | 0.018 | 0.003 |
| MUTAG | AttentiveFP | IntegratedGradients | scaffold | 20 | 0.033 | 0.388 | 0.937 | 0.999 | 0.042 | 0.203 | 0.771 | 0.116 | 0.377 |
| MUTAG | GAT | IntegratedGradients | random | 20 | 0.709 | 0.281 | 0.966 | 0.935 | 0.307 | 0.338 | 0.774 | 0.253 | 0.071 |
| MUTAG | GAT | IntegratedGradients | scaffold | 20 | 0.420 | 0.280 | 0.947 | 0.989 | 0.260 | 0.265 | 0.771 | 0.276 | 0.261 |
| MUTAG | GCN | IntegratedGradients | random | 20 | 0.169 | 0.285 | 0.985 | 0.946 | 0.260 | 0.336 | 0.771 | 0.248 | 0.148 |
| MUTAG | GCN | IntegratedGradients | scaffold | 20 | 0.950 | 0.242 | 0.628 | 0.983 | 0.000 | -0.002 | 0.771 | 0.001 | 0.000 |
| MUTAG | GINE | GNNExplainer | random | 20 | 0.452 | -0.476 | 0.816 | 0.929 | -0.006 | -0.015 | 0.776 | 0.006 | 0.002 |
| MUTAG | GINE | GNNExplainer | scaffold | 20 | 0.671 | 0.607 | 0.882 | 0.987 | 0.079 | 0.303 | 0.771 | 0.133 | 0.565 |
| MUTAG | GINE | GuidedBackprop | random | 20 | 0.258 | -0.505 | 0.837 | 0.938 | -0.007 | -0.014 | 0.774 | 0.009 | 0.001 |
| MUTAG | GINE | GuidedBackprop | scaffold | 20 | 0.016 | 0.701 | 0.891 | 0.993 | 0.204 | 0.240 | 0.771 | 0.282 | 0.522 |
| MUTAG | GINE | InputXGradient | random | 20 | 0.054 | -0.553 | 0.860 | 0.985 | -0.008 | -0.013 | 0.769 | 0.009 | 0.001 |
| MUTAG | GINE | InputXGradient | scaffold | 20 | 0.049 | 0.640 | 0.901 | 0.998 | 0.165 | 0.294 | 0.771 | 0.259 | 0.571 |
| MUTAG | GINE | IntegratedGradients | random | 20 | 0.048 | -0.561 | 0.861 | 0.984 | -0.009 | -0.013 | 0.774 | 0.009 | 0.001 |
| MUTAG | GINE | IntegratedGradients | scaffold | 20 | 0.537 | 0.419 | 0.863 | 0.991 | 0.084 | 0.361 | 0.763 | 0.133 | 0.572 |
| MUTAG | GINE | PGExplainer | random | 20 | 1.000 | -0.409 | 0.390 | 0.978 | -0.003 | -0.014 | 0.761 | 0.002 | — |
| MUTAG | GINE | PGExplainer | scaffold | 20 | 0.108 | 0.407 | 0.829 | 0.950 | 0.054 | 0.368 | 0.774 | 0.091 | — |
| MUTAG | GINE | Saliency | random | 20 | 0.020 | -0.521 | 0.796 | 0.976 | -0.008 | -0.013 | 0.769 | 0.009 | 0.001 |
| MUTAG | GINE | Saliency | scaffold | 20 | 0.009 | 0.611 | 0.871 | 0.999 | 0.158 | 0.335 | 0.771 | 0.238 | 0.647 |
| MUTAG | MPNN | IntegratedGradients | random | 20 | 0.164 | 0.034 | 0.794 | 0.958 | 0.193 | 0.252 | 0.770 | 0.176 | 0.122 |
| MUTAG | MPNN | IntegratedGradients | scaffold | 20 | 0.672 | 0.734 | 0.909 | 0.989 | 0.229 | 0.258 | 0.771 | 0.334 | 0.323 |
| SIDER | GCN | IntegratedGradients | random | 100 | — | 0.479 | 0.782 | 0.722 | 0.141 | 0.249 | 0.762 | 0.220 | 0.048 |
| SIDER | GCN | IntegratedGradients | scaffold | 100 | — | 0.067 | 0.831 | 0.746 | 0.060 | 0.118 | 0.673 | 0.144 | 0.062 |
| SIDER | GINE | IntegratedGradients | random | 100 | — | 0.516 | 0.785 | 0.761 | 0.157 | 0.315 | 0.762 | 0.221 | 0.452 |
| SIDER | GINE | IntegratedGradients | scaffold | 100 | — | 0.816 | 0.661 | 0.836 | 0.065 | 0.082 | 0.679 | 0.139 | 0.490 |
| SynthMotifs | AttentiveFP | IntegratedGradients | random | 20 | 0.716 | -0.162 | 0.655 | 0.215 | 0.335 | 0.296 | 0.788 | 0.083 | 0.539 |
| SynthMotifs | AttentiveFP | IntegratedGradients | scaffold | 20 | 0.886 | -0.121 | 0.805 | 0.132 | 0.276 | 0.247 | 0.790 | 0.231 | 0.292 |
| SynthMotifs | GAT | IntegratedGradients | random | 20 | 0.874 | 0.362 | 0.881 | 0.122 | 0.243 | 0.215 | 0.790 | 0.315 | 0.226 |
| SynthMotifs | GAT | IntegratedGradients | scaffold | 20 | 0.592 | 0.155 | 0.337 | 0.216 | 0.071 | 0.066 | 0.783 | 0.159 | 0.041 |
| SynthMotifs | GCN | IntegratedGradients | random | 20 | 0.480 | 0.376 | 0.693 | 0.100 | 0.119 | 0.142 | 0.797 | 0.203 | 0.039 |
| SynthMotifs | GCN | IntegratedGradients | scaffold | 20 | 0.987 | 0.325 | 0.787 | 0.152 | 0.269 | 0.164 | 0.798 | 0.370 | 0.151 |
| SynthMotifs | GINE | GNNExplainer | random | 20 | 0.474 | 0.022 | 0.018 | 0.038 | 0.171 | 0.222 | 0.800 | 0.258 | 0.118 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 20 | 0.668 | 0.063 | -0.008 | 0.052 | 0.201 | 0.168 | 0.800 | 0.295 | 0.135 |
| SynthMotifs | GINE | GuidedBackprop | random | 20 | 1.000 | 0.640 | 0.738 | 0.172 | 0.212 | 0.070 | 0.800 | 0.335 | 0.129 |
| SynthMotifs | GINE | GuidedBackprop | scaffold | 20 | 0.928 | 0.194 | 0.833 | 0.114 | 0.209 | 0.095 | 0.793 | 0.331 | 0.146 |
| SynthMotifs | GINE | InputXGradient | random | 20 | 0.992 | 0.568 | 0.633 | 0.184 | 0.212 | 0.084 | 0.797 | 0.334 | 0.123 |
| SynthMotifs | GINE | InputXGradient | scaffold | 20 | 0.968 | 0.207 | 0.716 | 0.194 | 0.242 | 0.109 | 0.792 | 0.339 | 0.161 |
| SynthMotifs | GINE | IntegratedGradients | random | 20 | 0.998 | 0.614 | 0.476 | 0.182 | 0.216 | 0.092 | 0.798 | 0.340 | 0.129 |
| SynthMotifs | GINE | IntegratedGradients | scaffold | 20 | 0.901 | 0.292 | 0.657 | 0.126 | 0.281 | 0.060 | 0.793 | 0.390 | 0.143 |
| SynthMotifs | GINE | PGExplainer | random | 20 | 0.490 | -0.106 | -0.014 | 0.087 | 0.048 | 0.160 | 0.800 | 0.073 | — |
| SynthMotifs | GINE | PGExplainer | scaffold | 20 | 0.565 | 0.116 | 0.268 | 0.404 | 0.184 | 0.164 | 0.627 | 0.273 | — |
| SynthMotifs | GINE | Saliency | random | 20 | 0.999 | 0.584 | 0.485 | 0.167 | 0.234 | 0.068 | 0.798 | 0.368 | 0.134 |
| SynthMotifs | GINE | Saliency | scaffold | 20 | 0.975 | 0.194 | 0.610 | 0.139 | 0.256 | 0.099 | 0.792 | 0.347 | 0.145 |
| SynthMotifs | MPNN | IntegratedGradients | random | 20 | 0.839 | 0.382 | 0.473 | 0.119 | 0.410 | 0.459 | 0.798 | 0.450 | 0.346 |
| SynthMotifs | MPNN | IntegratedGradients | scaffold | 20 | 0.712 | 0.525 | 0.716 | 0.304 | 0.423 | 0.209 | 0.797 | 0.509 | 0.230 |
| Tox21 | GINE | IntegratedGradients | random | 100 | — | -0.739 | 0.639 | 0.752 | -0.058 | -0.080 | 0.765 | 0.017 | 0.205 |
| Tox21 | GINE | IntegratedGradients | scaffold | 100 | — | -0.367 | 0.381 | 0.739 | -0.011 | -0.009 | 0.766 | 0.031 | 0.188 |
| hERG | GINE | IntegratedGradients | random | 66 | — | 0.661 | 0.992 | 0.776 | 0.560 | 0.560 | 0.779 | 0.279 | 0.659 |
| hERG | GINE | IntegratedGradients | scaffold | 66 | — | 0.245 | 0.924 | 0.689 | 0.337 | 0.337 | 0.774 | 0.283 | 0.527 |

## Paired attributor comparisons (Wilcoxon, shared molecules)

**BBBP · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 96 | -0.024 | 0.334 |
| GNNExplainer | PGExplainer | 96 | 0.007 | 0.850 |
| IntegratedGradients | PGExplainer | 96 | -0.040 | 0.309 |

**BBBP · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 100 | 0.280 | 0.000 |
| GNNExplainer | PGExplainer | 100 | 0.138 | 0.000 |
| IntegratedGradients | PGExplainer | 100 | -0.108 | 0.000 |

**ClinTox · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 63 | 0.000 | 0.315 |

**ClinTox · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 88 | 0.000 | 0.225 |

**ESOL · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 77 | 0.000 | 0.000 |

**ESOL · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 76 | 0.000 | 0.015 |

**MUTAG · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 20 | 0.029 | 0.393 |
| GNNExplainer | InputXGradient | 20 | 0.029 | 0.134 |
| GNNExplainer | IntegratedGradients | 20 | 0.029 | 0.088 |
| GNNExplainer | PGExplainer | 20 | 0.000 | 0.363 |
| GNNExplainer | Saliency | 20 | 0.000 | 0.363 |
| GuidedBackprop | InputXGradient | 20 | 0.000 | 0.533 |
| GuidedBackprop | IntegratedGradients | 20 | 0.000 | 0.374 |
| GuidedBackprop | PGExplainer | 20 | -0.114 | 0.245 |
| GuidedBackprop | Saliency | 20 | 0.000 | 0.600 |
| InputXGradient | IntegratedGradients | 20 | 0.000 | 0.180 |
| InputXGradient | PGExplainer | 20 | -0.086 | 0.116 |
| InputXGradient | Saliency | 20 | 0.000 | 0.236 |
| IntegratedGradients | PGExplainer | 20 | -0.086 | 0.108 |
| IntegratedGradients | Saliency | 20 | 0.000 | 0.161 |
| PGExplainer | Saliency | 20 | 0.186 | 0.083 |

**MUTAG · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 20 | -0.050 | 0.276 |
| GNNExplainer | InputXGradient | 20 | 0.000 | 0.571 |
| GNNExplainer | IntegratedGradients | 20 | 0.104 | 0.010 |
| GNNExplainer | PGExplainer | 19 | 0.200 | 0.011 |
| GNNExplainer | Saliency | 20 | 0.029 | 0.962 |
| GuidedBackprop | InputXGradient | 20 | 0.000 | 0.063 |
| GuidedBackprop | IntegratedGradients | 20 | 0.350 | 0.004 |
| GuidedBackprop | PGExplainer | 19 | 0.483 | 0.012 |
| GuidedBackprop | Saliency | 20 | 0.000 | 0.027 |
| InputXGradient | IntegratedGradients | 20 | 0.250 | 0.003 |
| InputXGradient | PGExplainer | 19 | 0.143 | 0.021 |
| InputXGradient | Saliency | 20 | 0.000 | 0.292 |
| IntegratedGradients | PGExplainer | 19 | -0.036 | 0.527 |
| IntegratedGradients | Saliency | 20 | -0.200 | 0.011 |
| PGExplainer | Saliency | 19 | -0.143 | 0.047 |

**SynthMotifs · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 20 | -0.684 | 0.000 |
| GNNExplainer | InputXGradient | 20 | -0.558 | 0.000 |
| GNNExplainer | IntegratedGradients | 20 | -0.635 | 0.000 |
| GNNExplainer | PGExplainer | 4 | -0.086 | — |
| GNNExplainer | Saliency | 20 | -0.588 | 0.000 |
| GuidedBackprop | InputXGradient | 20 | 0.020 | 0.189 |
| GuidedBackprop | IntegratedGradients | 20 | -0.120 | 1.000 |
| GuidedBackprop | PGExplainer | 4 | 0.769 | — |
| GuidedBackprop | Saliency | 20 | -0.022 | 0.622 |
| InputXGradient | IntegratedGradients | 20 | -0.087 | 0.231 |
| InputXGradient | PGExplainer | 4 | 0.619 | — |
| InputXGradient | Saliency | 20 | -0.030 | 0.189 |
| IntegratedGradients | PGExplainer | 4 | 0.589 | — |
| IntegratedGradients | Saliency | 20 | 0.043 | 0.277 |
| PGExplainer | Saliency | 4 | -0.659 | — |

**SynthMotifs · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 20 | -0.243 | 0.189 |
| GNNExplainer | InputXGradient | 20 | -0.097 | 0.123 |
| GNNExplainer | IntegratedGradients | 20 | -0.212 | 0.001 |
| GNNExplainer | PGExplainer | 20 | -0.099 | 0.409 |
| GNNExplainer | Saliency | 20 | -0.109 | 0.114 |
| GuidedBackprop | InputXGradient | 20 | 0.014 | 0.812 |
| GuidedBackprop | IntegratedGradients | 20 | -0.153 | 0.294 |
| GuidedBackprop | PGExplainer | 20 | 0.160 | 0.674 |
| GuidedBackprop | Saliency | 20 | 0.045 | 0.784 |
| InputXGradient | IntegratedGradients | 20 | -0.128 | 0.409 |
| InputXGradient | PGExplainer | 20 | 0.144 | 0.388 |
| InputXGradient | Saliency | 20 | 0.033 | 0.083 |
| IntegratedGradients | PGExplainer | 20 | 0.054 | 0.133 |
| IntegratedGradients | Saliency | 20 | 0.091 | 0.294 |
| PGExplainer | Saliency | 20 | -0.140 | 0.475 |

