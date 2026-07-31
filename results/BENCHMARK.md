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
| BA-2Motifs | GINE | GNNExplainer | random | 200 | 0.572 | -0.044 | 0.004 | 0.042 | -0.007 | -0.021 | 0.800 | 0.007 | — |
| BA-2Motifs | GINE | GNNExplainer | scaffold | 200 | 0.502 | 0.030 | 0.012 | 0.042 | 0.003 | 0.011 | 0.800 | 0.008 | — |
| BA-2Motifs | GINE | GuidedBackprop | random | 200 | 0.948 | -0.323 | 0.746 | 0.133 | -0.013 | -0.014 | 0.797 | 0.012 | — |
| BA-2Motifs | GINE | GuidedBackprop | scaffold | 200 | 0.908 | 0.506 | 0.845 | 0.136 | 0.007 | 0.006 | 0.792 | 0.018 | — |
| BA-2Motifs | GINE | InputXGradient | random | 200 | 0.928 | -0.260 | 0.796 | 0.127 | -0.012 | -0.016 | 0.790 | 0.012 | — |
| BA-2Motifs | GINE | InputXGradient | scaffold | 200 | 0.963 | 0.516 | 0.754 | 0.127 | 0.007 | 0.007 | 0.800 | 0.016 | — |
| BA-2Motifs | GINE | IntegratedGradients | random | 100 | — | -0.393 | 0.745 | 0.209 | 0.037 | 0.001 | 0.800 | 0.132 | — |
| BA-2Motifs | GINE | IntegratedGradients | scaffold | 100 | — | 0.636 | 0.740 | 0.119 | 0.022 | 0.029 | 0.799 | 0.044 | — |
| BA-2Motifs | GINE | PGExplainer | random | 200 | 0.102 | 0.161 | 0.009 | 0.382 | -0.003 | -0.024 | 0.784 | 0.004 | — |
| BA-2Motifs | GINE | PGExplainer | scaffold | 200 | 0.863 | 0.079 | -0.395 | 0.417 | 0.003 | 0.011 | 0.762 | 0.007 | — |
| BA-2Motifs | GINE | Saliency | random | 200 | 0.928 | -0.260 | 0.796 | 0.127 | -0.012 | -0.016 | 0.790 | 0.012 | — |
| BA-2Motifs | GINE | Saliency | scaffold | 200 | 0.963 | 0.516 | 0.754 | 0.127 | 0.007 | 0.007 | 0.800 | 0.016 | — |
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
| BBBP | GINE | GNNExplainer | random | 200 | — | 0.186 | 0.945 | 0.790 | 0.224 | 0.232 | 0.779 | 0.249 | 0.163 |
| BBBP | GINE | GNNExplainer | scaffold | 200 | — | -0.357 | 0.964 | 0.802 | -0.003 | -0.060 | 0.781 | 0.062 | 0.176 |
| BBBP | GINE | IntegratedGradients | random | 100 | — | 0.016 | 0.827 | 0.724 | 0.332 | 0.334 | 0.776 | 0.098 | 0.394 |
| BBBP | GINE | IntegratedGradients | scaffold | 100 | — | -0.741 | 0.857 | 0.841 | -0.031 | -0.057 | 0.774 | 0.028 | 0.090 |
| BBBP | GINE | PGExplainer | random | 200 | — | -0.086 | 0.371 | 0.879 | 0.115 | 0.229 | 0.689 | 0.160 | — |
| BBBP | GINE | PGExplainer | scaffold | 200 | — | -0.297 | 0.683 | 0.821 | -0.042 | -0.051 | 0.593 | 0.080 | — |
| BBBP | MPNN | IntegratedGradients | random | 100 | — | 0.154 | 0.765 | 0.792 | 0.210 | 0.267 | 0.774 | 0.121 | 0.104 |
| BBBP | MPNN | IntegratedGradients | scaffold | 100 | — | -0.431 | 0.832 | 0.824 | 0.052 | -0.043 | 0.775 | 0.117 | 0.096 |
| ClinTox | GINE | GNNExplainer | random | 200 | — | -0.039 | 0.956 | 0.619 | 0.191 | 0.152 | 0.827 | 0.129 | 0.340 |
| ClinTox | GINE | GNNExplainer | scaffold | 200 | — | -0.219 | 0.969 | 0.686 | 0.205 | 0.205 | 0.783 | 0.151 | 0.294 |
| ClinTox | GINE | IntegratedGradients | random | 100 | — | -0.223 | 0.983 | 0.754 | 0.230 | 0.230 | 0.778 | 0.108 | 0.119 |
| ClinTox | GINE | IntegratedGradients | scaffold | 100 | — | -0.329 | 0.991 | 0.745 | 0.135 | 0.135 | 0.772 | 0.128 | 0.254 |
| DILI | GINE | IntegratedGradients | random | 48 | — | 0.298 | 0.780 | 0.760 | 0.354 | 0.360 | 0.778 | 0.383 | 0.393 |
| DILI | GINE | IntegratedGradients | scaffold | 48 | — | 0.346 | 0.941 | 0.852 | 0.194 | 0.229 | 0.774 | 0.276 | 0.428 |
| ESOL | GAT | IntegratedGradients | random | 100 | — | 0.845 | 0.908 | 0.850 | 3.524 | 6.515 | 0.715 | 0.020 | — |
| ESOL | GAT | IntegratedGradients | scaffold | 100 | — | 0.862 | 0.935 | 0.838 | 5.007 | 9.467 | 0.726 | 0.000 | — |
| ESOL | GCN | IntegratedGradients | random | 100 | — | -0.534 | 0.936 | 0.870 | -0.827 | -0.916 | 0.710 | 0.009 | — |
| ESOL | GCN | IntegratedGradients | scaffold | 100 | — | -0.509 | 0.965 | 0.870 | -0.882 | -1.277 | 0.724 | 0.024 | — |
| ESOL | GINE | GNNExplainer | random | 200 | — | 0.374 | 0.954 | 0.862 | -1.310 | -1.756 | 0.757 | — | — |
| ESOL | GINE | GNNExplainer | scaffold | 200 | — | 0.554 | 0.902 | 0.824 | -1.064 | -1.405 | 0.758 | — | — |
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
| MUTAG | GINE | GNNExplainer | random | 58 | 0.838 | -0.155 | 0.801 | 0.930 | 0.313 | 0.185 | 0.777 | 0.324 | 0.704 |
| MUTAG | GINE | GNNExplainer | scaffold | 53 | 0.528 | 0.365 | 0.781 | 0.984 | 0.071 | 0.310 | 0.774 | 0.149 | 0.496 |
| MUTAG | GINE | GuidedBackprop | random | 58 | 0.037 | -0.089 | 0.884 | 0.962 | 0.540 | 0.615 | 0.773 | 0.178 | 0.628 |
| MUTAG | GINE | GuidedBackprop | scaffold | 53 | 0.146 | 0.551 | 0.975 | 0.985 | 0.210 | 0.242 | 0.772 | 0.297 | 0.494 |
| MUTAG | GINE | InputXGradient | random | 58 | 0.013 | -0.198 | 0.770 | 0.984 | 0.487 | 0.605 | 0.771 | 0.159 | 0.501 |
| MUTAG | GINE | InputXGradient | scaffold | 53 | 0.048 | 0.534 | 0.969 | 0.995 | 0.199 | 0.246 | 0.772 | 0.296 | 0.487 |
| MUTAG | GINE | IntegratedGradients | random | 20 | 0.048 | -0.561 | 0.861 | 0.984 | -0.009 | -0.013 | 0.774 | 0.009 | 0.001 |
| MUTAG | GINE | IntegratedGradients | scaffold | 20 | 0.537 | 0.419 | 0.863 | 0.991 | 0.084 | 0.361 | 0.763 | 0.133 | 0.572 |
| MUTAG | GINE | PGExplainer | random | 58 | 0.251 | -0.346 | 0.710 | 0.983 | 0.380 | 0.429 | 0.648 | 0.225 | — |
| MUTAG | GINE | PGExplainer | scaffold | 53 | 0.981 | 0.215 | 0.942 | 0.986 | 0.097 | 0.238 | 0.637 | 0.134 | — |
| MUTAG | GINE | Saliency | random | 58 | 0.002 | -0.196 | 0.767 | 0.975 | 0.497 | 0.610 | 0.772 | 0.165 | 0.516 |
| MUTAG | GINE | Saliency | scaffold | 53 | 0.014 | 0.531 | 0.933 | 0.996 | 0.198 | 0.248 | 0.772 | 0.295 | 0.498 |
| MUTAG | MPNN | IntegratedGradients | random | 20 | 0.164 | 0.034 | 0.794 | 0.958 | 0.193 | 0.252 | 0.770 | 0.176 | 0.122 |
| MUTAG | MPNN | IntegratedGradients | scaffold | 20 | 0.672 | 0.734 | 0.909 | 0.989 | 0.229 | 0.258 | 0.771 | 0.334 | 0.323 |
| MolMotif | GINE | GNNExplainer | random | 200 | 0.630 | 0.031 | 0.963 | 0.836 | -0.020 | 0.387 | 0.778 | 0.027 | 0.090 |
| MolMotif | GINE | GNNExplainer | scaffold | 200 | 0.604 | -0.054 | 0.949 | 0.814 | -0.014 | 0.265 | 0.780 | 0.073 | 0.138 |
| MolMotif | GINE | GuidedBackprop | random | 200 | 0.998 | -0.145 | 0.884 | 0.823 | 0.330 | 0.318 | 0.770 | 0.153 | 0.489 |
| MolMotif | GINE | GuidedBackprop | scaffold | 200 | 0.882 | -0.269 | 0.837 | 0.814 | 0.214 | 0.191 | 0.774 | 0.255 | 0.339 |
| MolMotif | GINE | InputXGradient | random | 200 | 0.999 | -0.112 | 0.848 | 0.810 | 0.312 | 0.322 | 0.768 | 0.144 | 0.490 |
| MolMotif | GINE | InputXGradient | scaffold | 200 | 0.999 | -0.257 | 0.859 | 0.758 | 0.205 | 0.170 | 0.774 | 0.234 | 0.399 |
| MolMotif | GINE | PGExplainer | random | 200 | 0.584 | 0.001 | 0.639 | 0.897 | 0.143 | 0.381 | 0.702 | 0.091 | — |
| MolMotif | GINE | PGExplainer | scaffold | 200 | 0.240 | -0.031 | 0.464 | 0.911 | 0.125 | 0.237 | 0.774 | 0.153 | — |
| MolMotif | GINE | Saliency | random | 200 | 0.994 | -0.117 | 0.836 | 0.802 | 0.318 | 0.317 | 0.772 | 0.150 | 0.506 |
| MolMotif | GINE | Saliency | scaffold | 200 | 0.998 | -0.270 | 0.844 | 0.751 | 0.220 | 0.179 | 0.775 | 0.250 | 0.400 |
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
| SynthMotifs | GINE | GNNExplainer | random | 200 | 0.689 | 0.191 | 0.352 | 0.048 | 0.213 | 0.250 | 0.800 | 0.306 | 0.150 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 200 | 0.796 | 0.217 | 0.222 | 0.051 | 0.336 | 0.321 | 0.800 | 0.391 | 0.426 |
| SynthMotifs | GINE | GuidedBackprop | random | 200 | 0.996 | 0.614 | 0.795 | 0.164 | 0.261 | 0.059 | 0.800 | 0.393 | 0.210 |
| SynthMotifs | GINE | GuidedBackprop | scaffold | 200 | 0.982 | 0.628 | 0.775 | 0.143 | 0.345 | 0.033 | 0.800 | 0.473 | 0.449 |
| SynthMotifs | GINE | InputXGradient | random | 200 | 0.959 | 0.499 | 0.656 | 0.238 | 0.261 | 0.132 | 0.795 | 0.379 | 0.203 |
| SynthMotifs | GINE | InputXGradient | scaffold | 200 | 0.982 | 0.456 | 0.723 | 0.180 | 0.338 | 0.122 | 0.797 | 0.437 | 0.462 |
| SynthMotifs | GINE | IntegratedGradients | random | 20 | 0.998 | 0.614 | 0.476 | 0.182 | 0.216 | 0.092 | 0.798 | 0.340 | 0.129 |
| SynthMotifs | GINE | IntegratedGradients | scaffold | 20 | 0.901 | 0.292 | 0.657 | 0.126 | 0.281 | 0.060 | 0.793 | 0.390 | 0.143 |
| SynthMotifs | GINE | PGExplainer | random | 200 | 0.314 | -0.149 | 0.427 | 0.385 | 0.010 | 0.262 | 0.785 | 0.035 | — |
| SynthMotifs | GINE | PGExplainer | scaffold | 200 | 0.323 | -0.158 | 0.563 | 0.377 | 0.058 | 0.280 | 0.656 | 0.103 | — |
| SynthMotifs | GINE | Saliency | random | 200 | 0.960 | 0.514 | 0.560 | 0.176 | 0.262 | 0.141 | 0.796 | 0.380 | 0.208 |
| SynthMotifs | GINE | Saliency | scaffold | 200 | 0.983 | 0.432 | 0.605 | 0.150 | 0.332 | 0.099 | 0.794 | 0.436 | 0.445 |
| SynthMotifs | MPNN | IntegratedGradients | random | 20 | 0.839 | 0.382 | 0.473 | 0.119 | 0.410 | 0.459 | 0.798 | 0.450 | 0.346 |
| SynthMotifs | MPNN | IntegratedGradients | scaffold | 20 | 0.712 | 0.525 | 0.716 | 0.304 | 0.423 | 0.209 | 0.797 | 0.509 | 0.230 |
| Tox21 | GINE | IntegratedGradients | random | 100 | — | -0.739 | 0.639 | 0.752 | -0.058 | -0.080 | 0.765 | 0.017 | 0.205 |
| Tox21 | GINE | IntegratedGradients | scaffold | 100 | — | -0.367 | 0.381 | 0.739 | -0.011 | -0.009 | 0.766 | 0.031 | 0.188 |
| hERG | GINE | IntegratedGradients | random | 66 | — | 0.661 | 0.992 | 0.776 | 0.560 | 0.560 | 0.779 | 0.279 | 0.659 |
| hERG | GINE | IntegratedGradients | scaffold | 66 | — | 0.245 | 0.924 | 0.689 | 0.337 | 0.337 | 0.774 | 0.283 | 0.527 |

## Paired attributor comparisons (Wilcoxon, shared molecules)

**BA-2Motifs · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 200 | 0.495 | 0.000 |
| GNNExplainer | InputXGradient | 200 | 0.472 | 0.000 |
| GNNExplainer | IntegratedGradients | 18 | 0.231 | 0.081 |
| GNNExplainer | PGExplainer | 200 | -0.340 | 0.000 |
| GNNExplainer | Saliency | 200 | 0.472 | 0.000 |
| GuidedBackprop | InputXGradient | 200 | -0.046 | 0.000 |
| GuidedBackprop | IntegratedGradients | 18 | -0.423 | 0.865 |
| GuidedBackprop | PGExplainer | 200 | -0.997 | 0.000 |
| GuidedBackprop | Saliency | 200 | -0.046 | 0.000 |
| InputXGradient | IntegratedGradients | 18 | -0.283 | 0.734 |
| InputXGradient | PGExplainer | 200 | -1.029 | 0.000 |
| InputXGradient | Saliency | 200 | 0.000 | 0.180 |
| IntegratedGradients | PGExplainer | 18 | -0.441 | 0.002 |
| IntegratedGradients | Saliency | 18 | 0.283 | 0.734 |
| PGExplainer | Saliency | 200 | 1.023 | 0.000 |

**BA-2Motifs · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 200 | -0.579 | 0.000 |
| GNNExplainer | InputXGradient | 200 | -0.585 | 0.000 |
| GNNExplainer | IntegratedGradients | 1 | -0.244 | — |
| GNNExplainer | PGExplainer | 200 | -0.056 | 0.026 |
| GNNExplainer | Saliency | 200 | -0.585 | 0.000 |
| GuidedBackprop | InputXGradient | 200 | -0.008 | 0.163 |
| GuidedBackprop | IntegratedGradients | 1 | -1.068 | — |
| GuidedBackprop | PGExplainer | 200 | 0.544 | 0.000 |
| GuidedBackprop | Saliency | 200 | -0.008 | 0.163 |
| InputXGradient | IntegratedGradients | 1 | -0.649 | — |
| InputXGradient | PGExplainer | 200 | 0.559 | 0.000 |
| InputXGradient | Saliency | 200 | 0.000 | 0.180 |
| IntegratedGradients | PGExplainer | 1 | 0.171 | — |
| IntegratedGradients | Saliency | 1 | 0.649 | — |
| PGExplainer | Saliency | 200 | -0.559 | 0.000 |

**BBBP · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 19 | 0.336 | 0.029 |
| GNNExplainer | PGExplainer | 178 | 0.134 | 0.000 |
| IntegratedGradients | PGExplainer | 18 | -0.511 | 0.015 |

**BBBP · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 1 | 0.939 | — |
| GNNExplainer | PGExplainer | 175 | -0.031 | 0.174 |
| IntegratedGradients | PGExplainer | 1 | -0.673 | — |

**ClinTox · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 12 | -0.032 | 0.203 |

**ClinTox · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 0 | — | — |

**ESOL · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 17 | 1.600 | 0.001 |

**ESOL · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 0 | — | — |

**MUTAG · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 58 | 0.000 | 0.278 |
| GNNExplainer | InputXGradient | 58 | 0.000 | 0.428 |
| GNNExplainer | IntegratedGradients | 6 | -0.100 | 1.000 |
| GNNExplainer | PGExplainer | 57 | 0.133 | 0.003 |
| GNNExplainer | Saliency | 58 | 0.000 | 0.422 |
| GuidedBackprop | InputXGradient | 58 | 0.000 | 0.006 |
| GuidedBackprop | IntegratedGradients | 6 | -0.300 | 1.000 |
| GuidedBackprop | PGExplainer | 57 | 0.316 | 0.000 |
| GuidedBackprop | Saliency | 58 | 0.000 | 0.004 |
| InputXGradient | IntegratedGradients | 6 | -0.300 | 1.000 |
| InputXGradient | PGExplainer | 57 | 0.213 | 0.000 |
| InputXGradient | Saliency | 58 | 0.000 | 0.866 |
| IntegratedGradients | PGExplainer | 6 | 0.574 | 0.688 |
| IntegratedGradients | Saliency | 6 | 0.300 | 1.000 |
| PGExplainer | Saliency | 57 | -0.193 | 0.000 |

**MUTAG · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 53 | -0.100 | 0.000 |
| GNNExplainer | InputXGradient | 53 | -0.100 | 0.000 |
| GNNExplainer | IntegratedGradients | 20 | 0.018 | 0.913 |
| GNNExplainer | PGExplainer | 53 | 0.149 | 0.001 |
| GNNExplainer | Saliency | 53 | -0.100 | 0.000 |
| GuidedBackprop | InputXGradient | 53 | 0.000 | 0.050 |
| GuidedBackprop | IntegratedGradients | 20 | 0.418 | 0.197 |
| GuidedBackprop | PGExplainer | 53 | 0.352 | 0.000 |
| GuidedBackprop | Saliency | 53 | 0.000 | 0.017 |
| InputXGradient | IntegratedGradients | 20 | 0.486 | 0.217 |
| InputXGradient | PGExplainer | 53 | 0.345 | 0.000 |
| InputXGradient | Saliency | 53 | 0.000 | 0.180 |
| IntegratedGradients | PGExplainer | 20 | 0.018 | 0.397 |
| IntegratedGradients | Saliency | 20 | -0.436 | 0.217 |
| PGExplainer | Saliency | 53 | -0.345 | 0.000 |

**MolMotif · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 194 | 0.071 | 0.000 |
| GNNExplainer | InputXGradient | 194 | 0.077 | 0.000 |
| GNNExplainer | PGExplainer | 191 | 0.000 | 0.296 |
| GNNExplainer | Saliency | 194 | 0.072 | 0.000 |
| GuidedBackprop | InputXGradient | 194 | 0.000 | 0.033 |
| GuidedBackprop | PGExplainer | 191 | -0.105 | 0.000 |
| GuidedBackprop | Saliency | 194 | 0.000 | 0.084 |
| InputXGradient | PGExplainer | 191 | -0.066 | 0.000 |
| InputXGradient | Saliency | 194 | 0.000 | 0.171 |
| PGExplainer | Saliency | 191 | 0.091 | 0.000 |

**MolMotif · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 199 | 0.150 | 0.000 |
| GNNExplainer | InputXGradient | 199 | 0.114 | 0.000 |
| GNNExplainer | PGExplainer | 197 | -0.057 | 0.377 |
| GNNExplainer | Saliency | 199 | 0.119 | 0.000 |
| GuidedBackprop | InputXGradient | 199 | 0.000 | 0.399 |
| GuidedBackprop | PGExplainer | 197 | -0.286 | 0.000 |
| GuidedBackprop | Saliency | 199 | 0.000 | 0.561 |
| InputXGradient | PGExplainer | 197 | -0.200 | 0.000 |
| InputXGradient | Saliency | 199 | 0.000 | 0.190 |
| PGExplainer | Saliency | 197 | 0.200 | 0.000 |

**SynthMotifs · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 200 | -0.398 | 0.000 |
| GNNExplainer | InputXGradient | 200 | -0.280 | 0.000 |
| GNNExplainer | IntegratedGradients | 6 | -0.596 | 0.031 |
| GNNExplainer | PGExplainer | 200 | 0.361 | 0.000 |
| GNNExplainer | Saliency | 200 | -0.309 | 0.000 |
| GuidedBackprop | InputXGradient | 200 | 0.092 | 0.000 |
| GuidedBackprop | IntegratedGradients | 6 | -0.028 | 0.562 |
| GuidedBackprop | PGExplainer | 200 | 0.811 | 0.000 |
| GuidedBackprop | Saliency | 200 | 0.094 | 0.000 |
| InputXGradient | IntegratedGradients | 6 | -0.055 | 0.094 |
| InputXGradient | PGExplainer | 200 | 0.682 | 0.000 |
| InputXGradient | Saliency | 200 | -0.013 | 0.001 |
| IntegratedGradients | PGExplainer | 6 | 0.896 | 0.031 |
| IntegratedGradients | Saliency | 6 | 0.095 | 0.094 |
| PGExplainer | Saliency | 200 | -0.696 | 0.000 |

**SynthMotifs · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 200 | -0.441 | 0.000 |
| GNNExplainer | InputXGradient | 200 | -0.257 | 0.000 |
| GNNExplainer | IntegratedGradients | 0 | — | — |
| GNNExplainer | PGExplainer | 198 | 0.448 | 0.000 |
| GNNExplainer | Saliency | 200 | -0.252 | 0.000 |
| GuidedBackprop | InputXGradient | 200 | 0.131 | 0.000 |
| GuidedBackprop | IntegratedGradients | 0 | — | — |
| GuidedBackprop | PGExplainer | 198 | 0.901 | 0.000 |
| GuidedBackprop | Saliency | 200 | 0.164 | 0.000 |
| InputXGradient | IntegratedGradients | 0 | — | — |
| InputXGradient | PGExplainer | 198 | 0.768 | 0.000 |
| InputXGradient | Saliency | 200 | 0.019 | 0.000 |
| IntegratedGradients | PGExplainer | 0 | — | — |
| IntegratedGradients | Saliency | 0 | — | — |
| PGExplainer | Saliency | 198 | -0.767 | 0.000 |

