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
| BA-2Motifs | GINE | GNNExplainer | random | 200 | 0.574 | -0.078 | 0.951 | 0.042 | -0.008 | -0.021 | 0.800 | 0.006 | — |
| BA-2Motifs | GINE | GNNExplainer | scaffold | 200 | 0.526 | 0.009 | 0.969 | 0.042 | -0.001 | -0.005 | 0.800 | 0.000 | — |
| BA-2Motifs | GINE | GuidedBackprop | random | 200 | 0.948 | -0.323 | 0.745 | 0.133 | -0.013 | -0.014 | 0.797 | 0.012 | — |
| BA-2Motifs | GINE | GuidedBackprop | scaffold | 200 | 0.909 | -0.667 | 0.807 | 0.118 | -0.002 | -0.004 | 0.800 | 0.000 | — |
| BA-2Motifs | GINE | InputXGradient | random | 200 | 0.928 | -0.260 | 0.796 | 0.127 | -0.012 | -0.016 | 0.790 | 0.012 | — |
| BA-2Motifs | GINE | InputXGradient | scaffold | 200 | 0.927 | -0.671 | 0.663 | 0.117 | -0.002 | -0.004 | 0.799 | 0.000 | — |
| BA-2Motifs | GINE | IntegratedGradients | random | 200 | 0.994 | -0.276 | 0.645 | 0.132 | -0.013 | -0.014 | 0.800 | 0.012 | — |
| BA-2Motifs | GINE | IntegratedGradients | scaffold | 200 | 0.856 | -0.635 | 0.715 | 0.112 | -0.002 | -0.004 | 0.799 | 0.000 | — |
| BA-2Motifs | GINE | PGExplainer | random | 200 | 0.104 | 0.155 | 0.305 | 0.378 | -0.003 | -0.023 | 0.777 | 0.004 | — |
| BA-2Motifs | GINE | PGExplainer | scaffold | 200 | 0.729 | 0.116 | 0.092 | 0.352 | -0.001 | -0.005 | 0.771 | 0.000 | — |
| BA-2Motifs | GINE | Saliency | random | 200 | 0.928 | -0.260 | 0.796 | 0.127 | -0.012 | -0.016 | 0.790 | 0.012 | — |
| BA-2Motifs | GINE | Saliency | scaffold | 200 | 0.927 | -0.671 | 0.663 | 0.117 | -0.002 | -0.004 | 0.799 | 0.000 | — |
| BACE | GCN | IntegratedGradients | random | 200 | — | 0.532 | 0.849 | 0.756 | 0.576 | 0.596 | 0.785 | 0.291 | 0.594 |
| BACE | GCN | IntegratedGradients | scaffold | 200 | — | 0.518 | 0.865 | 0.822 | 0.543 | 0.544 | 0.783 | 0.227 | 0.668 |
| BACE | GINE | IntegratedGradients | random | 200 | — | -0.203 | 0.691 | 0.751 | 0.103 | 0.115 | 0.787 | 0.126 | 0.323 |
| BACE | GINE | IntegratedGradients | scaffold | 200 | — | 0.057 | 0.564 | 0.876 | 0.385 | 0.358 | 0.783 | 0.415 | 0.174 |
| BBBP | AttentiveFP | IntegratedGradients | random | 200 | — | 0.230 | 0.853 | 0.732 | 0.068 | 0.069 | 0.759 | 0.200 | 0.104 |
| BBBP | AttentiveFP | IntegratedGradients | scaffold | 200 | — | 0.389 | 0.847 | 0.768 | 0.232 | 0.166 | 0.778 | 0.327 | 0.070 |
| BBBP | GAT | IntegratedGradients | random | 200 | — | 0.029 | 0.876 | 0.748 | 0.158 | 0.159 | 0.767 | 0.193 | 0.291 |
| BBBP | GAT | IntegratedGradients | scaffold | 200 | — | 0.134 | 0.941 | 0.781 | 0.351 | 0.351 | 0.778 | 0.158 | 0.444 |
| BBBP | GCN | IntegratedGradients | random | 200 | — | -0.376 | 0.842 | 0.794 | 0.008 | 0.003 | 0.765 | 0.092 | 0.195 |
| BBBP | GCN | IntegratedGradients | scaffold | 200 | — | 0.118 | 0.893 | 0.822 | 0.407 | 0.409 | 0.768 | 0.080 | 0.506 |
| BBBP | GINE | GNNExplainer | random | 200 | — | 0.179 | 0.955 | 0.789 | 0.218 | 0.234 | 0.779 | 0.241 | 0.164 |
| BBBP | GINE | GNNExplainer | scaffold | 200 | — | 0.435 | 0.934 | 0.807 | 0.286 | 0.315 | 0.783 | 0.327 | 0.400 |
| BBBP | GINE | IntegratedGradients | random | 200 | — | 0.226 | 0.890 | 0.764 | 0.191 | 0.246 | 0.772 | 0.206 | 0.314 |
| BBBP | GINE | IntegratedGradients | scaffold | 200 | — | 0.591 | 0.855 | 0.777 | 0.230 | 0.334 | 0.777 | 0.277 | 0.471 |
| BBBP | GINE | PGExplainer | random | 200 | — | -0.085 | 0.370 | 0.879 | 0.114 | 0.229 | 0.690 | 0.159 | — |
| BBBP | GINE | PGExplainer | scaffold | 200 | — | 0.145 | 0.438 | 0.828 | 0.144 | 0.248 | 0.639 | 0.223 | — |
| BBBP | MPNN | IntegratedGradients | random | 200 | — | -0.125 | 0.860 | 0.774 | 0.089 | 0.147 | 0.769 | 0.113 | 0.142 |
| BBBP | MPNN | IntegratedGradients | scaffold | 200 | — | 0.048 | 0.882 | 0.823 | 0.256 | 0.395 | 0.777 | 0.080 | 0.307 |
| Benzene | GINE | GNNExplainer | random | 200 | 0.531 | -0.007 | 0.733 | 0.058 | 0.004 | 0.032 | 0.780 | 0.069 | 0.091 |
| Benzene | GINE | GNNExplainer | scaffold | 200 | 0.425 | 0.301 | 0.986 | 0.774 | 0.120 | 0.336 | 0.784 | 0.075 | 0.356 |
| Benzene | GINE | GuidedBackprop | random | 200 | 0.743 | 0.261 | 0.560 | 0.095 | 0.050 | 0.022 | 0.777 | 0.097 | 0.087 |
| Benzene | GINE | GuidedBackprop | scaffold | 200 | 0.997 | 0.400 | 0.804 | 0.893 | 0.307 | 0.252 | 0.778 | 0.198 | 0.358 |
| Benzene | GINE | InputXGradient | random | 200 | 1.000 | -0.027 | 0.566 | 0.143 | 0.012 | 0.059 | 0.774 | 0.091 | 0.086 |
| Benzene | GINE | InputXGradient | scaffold | 200 | 0.987 | 0.244 | 0.865 | 0.915 | 0.304 | 0.286 | 0.778 | 0.174 | 0.339 |
| Benzene | GINE | IntegratedGradients | random | 200 | 1.000 | 0.150 | 0.525 | 0.120 | 0.010 | 0.048 | 0.772 | 0.091 | 0.086 |
| Benzene | GINE | IntegratedGradients | scaffold | 200 | 0.999 | 0.367 | 0.841 | 0.889 | 0.303 | 0.271 | 0.777 | 0.189 | 0.351 |
| Benzene | GINE | PGExplainer | random | 200 | 0.113 | -0.398 | 0.539 | 0.448 | 0.029 | 0.459 | 0.753 | 0.036 | — |
| Benzene | GINE | PGExplainer | scaffold | 200 | 0.241 | -0.064 | 0.366 | 0.904 | 0.056 | 0.288 | 0.633 | 0.083 | — |
| Benzene | GINE | Saliency | random | 200 | 1.000 | -0.091 | 0.629 | 0.118 | 0.010 | 0.061 | 0.774 | 0.087 | 0.089 |
| Benzene | GINE | Saliency | scaffold | 200 | 0.985 | 0.266 | 0.905 | 0.895 | 0.284 | 0.295 | 0.779 | 0.168 | 0.343 |
| Benzene | GINE | SubgraphX | random | 200 | 0.457 | 0.231 | — | 0.165 | 0.061 | 0.010 | 0.579 | 0.109 | — |
| Benzene | GINE | SubgraphX | scaffold | 200 | 0.770 | 0.283 | — | 0.897 | 0.233 | 0.079 | 0.614 | 0.278 | — |
| ClinTox | GINE | GNNExplainer | random | 200 | — | -0.018 | 0.975 | 0.612 | 0.194 | 0.152 | 0.831 | 0.129 | 0.340 |
| ClinTox | GINE | GNNExplainer | scaffold | 200 | — | 0.093 | 0.988 | 0.511 | 0.239 | 0.199 | 0.861 | 0.129 | 0.319 |
| ClinTox | GINE | IntegratedGradients | random | 200 | — | -0.224 | 0.911 | 0.794 | 0.152 | 0.152 | 0.775 | 0.129 | 0.205 |
| ClinTox | GINE | IntegratedGradients | scaffold | 200 | — | -0.264 | 0.971 | 0.760 | 0.199 | 0.199 | 0.779 | 0.129 | 0.221 |
| DILI | GINE | IntegratedGradients | random | 142 | — | 0.105 | 0.813 | 0.774 | 0.149 | 0.164 | 0.775 | 0.220 | 0.287 |
| DILI | GINE | IntegratedGradients | scaffold | 142 | — | 0.505 | 0.921 | 0.857 | 0.205 | 0.111 | 0.779 | 0.282 | 0.527 |
| ESOL | GAT | IntegratedGradients | random | 200 | — | 0.841 | 0.947 | 0.842 | 3.505 | 7.619 | 0.734 | — | — |
| ESOL | GAT | IntegratedGradients | scaffold | 200 | — | 0.879 | 0.955 | 0.862 | 8.272 | 36.696 | 0.716 | — | — |
| ESOL | GCN | IntegratedGradients | random | 200 | — | 0.251 | 0.965 | 0.859 | -0.716 | -0.758 | 0.731 | — | — |
| ESOL | GCN | IntegratedGradients | scaffold | 200 | — | 0.355 | 0.867 | 0.889 | -0.458 | -0.235 | 0.718 | — | — |
| ESOL | GINE | GNNExplainer | random | 200 | — | 0.373 | 0.958 | 0.862 | -1.316 | -1.758 | 0.757 | — | — |
| ESOL | GINE | GNNExplainer | scaffold | 200 | — | 0.086 | 0.890 | 0.880 | -0.347 | 0.129 | 0.751 | — | — |
| ESOL | GINE | IntegratedGradients | random | 200 | — | 0.432 | 0.932 | 0.870 | -1.490 | -1.686 | 0.739 | — | — |
| ESOL | GINE | IntegratedGradients | scaffold | 200 | — | 0.142 | 0.909 | 0.895 | -0.448 | 0.110 | 0.730 | — | — |
| FluorideCarbonyl | GINE | GNNExplainer | random | 200 | 0.671 | 0.125 | 0.460 | 0.072 | 0.162 | 0.202 | 0.784 | 0.171 | 0.106 |
| FluorideCarbonyl | GINE | GNNExplainer | scaffold | 200 | 0.614 | 0.093 | 0.911 | 0.766 | 0.124 | 0.091 | 0.785 | 0.153 | 0.078 |
| FluorideCarbonyl | GINE | GuidedBackprop | random | 200 | 0.881 | 0.304 | 0.289 | 0.214 | 0.159 | 0.160 | 0.783 | 0.186 | 0.579 |
| FluorideCarbonyl | GINE | GuidedBackprop | scaffold | 200 | 0.937 | 0.427 | 0.660 | 0.757 | 0.243 | 0.045 | 0.784 | 0.269 | 0.490 |
| FluorideCarbonyl | GINE | InputXGradient | random | 200 | 0.843 | 0.083 | 0.344 | 0.183 | 0.181 | 0.167 | 0.782 | 0.197 | 0.553 |
| FluorideCarbonyl | GINE | InputXGradient | scaffold | 200 | 0.791 | 0.290 | 0.595 | 0.775 | 0.166 | 0.064 | 0.784 | 0.191 | 0.553 |
| FluorideCarbonyl | GINE | IntegratedGradients | random | 200 | 0.765 | 0.152 | 0.410 | 0.152 | 0.206 | 0.211 | 0.782 | 0.192 | 0.598 |
| FluorideCarbonyl | GINE | IntegratedGradients | scaffold | 200 | 0.833 | 0.278 | 0.395 | 0.762 | 0.290 | 0.115 | 0.783 | 0.323 | 0.616 |
| FluorideCarbonyl | GINE | PGExplainer | random | 200 | 0.122 | -0.243 | -0.101 | 0.428 | 0.026 | 0.356 | 0.781 | 0.035 | — |
| FluorideCarbonyl | GINE | PGExplainer | scaffold | 200 | 0.498 | 0.098 | 0.356 | 0.945 | 0.049 | 0.142 | 0.731 | 0.060 | — |
| FluorideCarbonyl | GINE | Saliency | random | 200 | 0.872 | 0.160 | 0.450 | 0.143 | 0.192 | 0.140 | 0.782 | 0.202 | 0.583 |
| FluorideCarbonyl | GINE | Saliency | scaffold | 200 | 0.821 | 0.273 | 0.706 | 0.742 | 0.134 | 0.082 | 0.781 | 0.155 | 0.501 |
| FluorideCarbonyl | GINE | SubgraphX | random | 200 | 0.538 | 0.108 | — | 0.210 | 0.281 | 0.242 | 0.505 | 0.250 | — |
| FluorideCarbonyl | GINE | SubgraphX | scaffold | 200 | 0.433 | 0.179 | — | 0.946 | 0.111 | 0.063 | 0.428 | 0.146 | — |
| FreeSolv | GINE | IntegratedGradients | random | 193 | — | 0.276 | 0.862 | 0.857 | -0.715 | -0.788 | 0.717 | — | — |
| FreeSolv | GINE | IntegratedGradients | scaffold | 193 | — | 0.453 | 0.703 | 0.860 | -0.874 | -1.434 | 0.705 | — | — |
| Lipophilicity | GINE | IntegratedGradients | random | 200 | — | 0.546 | 0.749 | 0.790 | -0.636 | -1.248 | 0.781 | — | — |
| Lipophilicity | GINE | IntegratedGradients | scaffold | 200 | — | 0.600 | 0.762 | 0.818 | 0.839 | 1.956 | 0.779 | — | — |
| MUTAG | AttentiveFP | IntegratedGradients | random | 58 | 0.039 | -0.871 | 0.822 | 0.958 | -0.007 | -0.022 | 0.772 | 0.000 | 0.000 |
| MUTAG | AttentiveFP | IntegratedGradients | scaffold | 53 | 0.049 | -0.781 | 0.907 | 0.994 | -0.007 | -0.021 | 0.773 | 0.000 | 0.000 |
| MUTAG | GAT | IntegratedGradients | random | 58 | 0.461 | 0.698 | 0.951 | 0.925 | 0.281 | 0.511 | 0.775 | 0.289 | 0.169 |
| MUTAG | GAT | IntegratedGradients | scaffold | 53 | 0.733 | 0.652 | 1.000 | 0.981 | 0.136 | 0.461 | 0.775 | 0.207 | 0.019 |
| MUTAG | GCN | IntegratedGradients | random | 58 | 0.551 | 0.610 | 0.911 | 0.932 | 0.435 | 0.518 | 0.764 | 0.320 | 0.290 |
| MUTAG | GCN | IntegratedGradients | scaffold | 53 | 0.083 | 0.876 | 0.941 | 0.989 | 0.002 | 0.004 | 0.772 | 0.005 | 0.000 |
| MUTAG | GINE | GNNExplainer | random | 58 | 0.858 | -0.170 | 0.848 | 0.929 | 0.310 | 0.175 | 0.777 | 0.338 | 0.703 |
| MUTAG | GINE | GNNExplainer | scaffold | 53 | 0.826 | 0.379 | 0.904 | 0.984 | 0.154 | 0.200 | 0.775 | 0.209 | 0.695 |
| MUTAG | GINE | GuidedBackprop | random | 58 | 0.037 | -0.089 | 0.882 | 0.962 | 0.540 | 0.615 | 0.773 | 0.178 | 0.628 |
| MUTAG | GINE | GuidedBackprop | scaffold | 53 | 0.013 | 0.616 | 0.930 | 0.998 | 0.256 | 0.106 | 0.773 | 0.323 | 0.662 |
| MUTAG | GINE | InputXGradient | random | 58 | 0.013 | -0.200 | 0.770 | 0.984 | 0.491 | 0.605 | 0.772 | 0.160 | 0.501 |
| MUTAG | GINE | InputXGradient | scaffold | 53 | 0.079 | 0.499 | 0.826 | 0.995 | 0.167 | 0.227 | 0.773 | 0.206 | 0.373 |
| MUTAG | GINE | IntegratedGradients | random | 58 | 0.496 | -0.196 | 0.724 | 0.915 | 0.551 | 0.433 | 0.772 | 0.347 | 0.706 |
| MUTAG | GINE | IntegratedGradients | scaffold | 53 | 0.302 | 0.310 | 0.808 | 0.986 | 0.030 | 0.249 | 0.772 | 0.077 | 0.692 |
| MUTAG | GINE | PGExplainer | random | 58 | 0.251 | -0.351 | 0.713 | 0.983 | 0.379 | 0.430 | 0.647 | 0.225 | — |
| MUTAG | GINE | PGExplainer | scaffold | 53 | 0.360 | 0.281 | 0.606 | 1.000 | 0.066 | 0.309 | 0.764 | 0.114 | — |
| MUTAG | GINE | Saliency | random | 58 | 0.002 | -0.195 | 0.767 | 0.975 | 0.494 | 0.610 | 0.772 | 0.163 | 0.516 |
| MUTAG | GINE | Saliency | scaffold | 53 | 0.002 | 0.404 | 0.854 | 0.998 | 0.157 | 0.188 | 0.773 | 0.202 | 0.426 |
| MUTAG | GINE | SubgraphX | random | 58 | 0.348 | -0.154 | — | 0.996 | 0.342 | -0.000 | 0.160 | 0.450 | — |
| MUTAG | GINE | SubgraphX | scaffold | 53 | 0.330 | 0.379 | — | 1.000 | 0.304 | 0.049 | 0.247 | 0.426 | — |
| MUTAG | MPNN | IntegratedGradients | random | 58 | 0.127 | 0.532 | 0.890 | 0.959 | 0.623 | 0.635 | 0.771 | 0.188 | 0.419 |
| MUTAG | MPNN | IntegratedGradients | scaffold | 53 | 0.301 | -0.706 | 0.829 | 0.991 | 0.002 | 0.007 | 0.770 | 0.008 | 0.000 |
| MolMotif | AttentiveFP | IntegratedGradients | random | 200 | 0.986 | 0.486 | 0.912 | 0.792 | 0.522 | 0.017 | 0.770 | 0.520 | 0.339 |
| MolMotif | AttentiveFP | IntegratedGradients | scaffold | 200 | 0.810 | 0.539 | 0.929 | 0.803 | 0.455 | 0.038 | 0.773 | 0.448 | 0.487 |
| MolMotif | GAT | IntegratedGradients | random | 200 | 0.733 | 0.040 | 0.901 | 0.716 | 0.491 | 0.240 | 0.772 | 0.515 | 0.220 |
| MolMotif | GAT | IntegratedGradients | scaffold | 200 | 0.706 | 0.358 | 0.945 | 0.768 | 0.476 | 0.320 | 0.778 | 0.457 | 0.005 |
| MolMotif | GCN | IntegratedGradients | random | 200 | 0.850 | -0.013 | 1.000 | 0.811 | 0.414 | 0.420 | 0.768 | 0.037 | 0.375 |
| MolMotif | GCN | IntegratedGradients | scaffold | 200 | 0.973 | 0.441 | 0.933 | 0.824 | 0.381 | 0.101 | 0.769 | 0.450 | 0.155 |
| MolMotif | GINE | GNNExplainer | random | 200 | 0.630 | 0.030 | 0.973 | 0.835 | -0.018 | 0.387 | 0.778 | 0.025 | 0.089 |
| MolMotif | GINE | GNNExplainer | scaffold | 200 | 0.636 | 0.170 | 0.982 | 0.850 | 0.149 | 0.369 | 0.780 | 0.141 | 0.107 |
| MolMotif | GINE | GuidedBackprop | random | 200 | 0.998 | -0.144 | 0.884 | 0.823 | 0.330 | 0.318 | 0.770 | 0.153 | 0.489 |
| MolMotif | GINE | GuidedBackprop | scaffold | 200 | 0.970 | 0.067 | 0.843 | 0.799 | 0.263 | 0.344 | 0.771 | 0.209 | 0.205 |
| MolMotif | GINE | InputXGradient | random | 200 | 0.999 | -0.112 | 0.848 | 0.810 | 0.312 | 0.322 | 0.768 | 0.144 | 0.490 |
| MolMotif | GINE | InputXGradient | scaffold | 200 | 0.998 | 0.059 | 0.869 | 0.785 | 0.251 | 0.339 | 0.773 | 0.222 | 0.274 |
| MolMotif | GINE | IntegratedGradients | random | 200 | 0.972 | 0.007 | 0.970 | 0.860 | 0.311 | 0.319 | 0.768 | 0.153 | 0.476 |
| MolMotif | GINE | IntegratedGradients | scaffold | 200 | 0.939 | 0.182 | 0.880 | 0.851 | 0.359 | 0.309 | 0.773 | 0.290 | 0.082 |
| MolMotif | GINE | PGExplainer | random | 200 | 0.584 | 0.001 | 0.639 | 0.897 | 0.143 | 0.381 | 0.702 | 0.091 | — |
| MolMotif | GINE | PGExplainer | scaffold | 200 | 0.523 | 0.016 | 0.707 | 0.940 | 0.115 | 0.384 | 0.768 | 0.123 | — |
| MolMotif | GINE | Saliency | random | 200 | 0.994 | -0.117 | 0.837 | 0.802 | 0.318 | 0.317 | 0.772 | 0.150 | 0.506 |
| MolMotif | GINE | Saliency | scaffold | 200 | 0.992 | 0.048 | 0.866 | 0.764 | 0.229 | 0.355 | 0.776 | 0.221 | 0.363 |
| MolMotif | GINE | SubgraphX | random | 200 | 0.556 | -0.013 | — | 0.977 | 0.159 | 0.320 | 0.390 | 0.165 | — |
| MolMotif | GINE | SubgraphX | scaffold | 200 | 0.476 | 0.065 | — | 0.947 | 0.311 | 0.308 | 0.353 | 0.248 | — |
| MolMotif | MPNN | IntegratedGradients | random | 200 | 0.962 | -0.057 | 0.946 | 0.860 | 0.451 | 0.457 | 0.772 | 0.030 | 0.121 |
| MolMotif | MPNN | IntegratedGradients | scaffold | 200 | 0.976 | 0.095 | 0.922 | 0.899 | 0.407 | 0.330 | 0.775 | 0.103 | 0.024 |
| MolMotifHard | AttentiveFP | IntegratedGradients | random | 200 | 0.801 | 0.486 | 0.932 | 0.675 | 0.466 | 0.103 | 0.764 | 0.511 | 0.094 |
| MolMotifHard | AttentiveFP | IntegratedGradients | scaffold | 200 | 0.874 | 0.199 | 0.893 | 0.741 | 0.385 | 0.116 | 0.764 | 0.446 | 0.080 |
| MolMotifHard | GAT | IntegratedGradients | random | 200 | 0.788 | 0.021 | 0.966 | 0.673 | 0.506 | 0.506 | 0.760 | 0.033 | 0.414 |
| MolMotifHard | GAT | IntegratedGradients | scaffold | 200 | 0.782 | -0.034 | 0.921 | 0.743 | 0.405 | 0.405 | 0.765 | 0.052 | 0.430 |
| MolMotifHard | GCN | IntegratedGradients | random | 200 | 0.908 | 0.110 | 0.700 | 0.684 | 0.436 | 0.481 | 0.764 | 0.086 | 0.481 |
| MolMotifHard | GCN | IntegratedGradients | scaffold | 200 | 0.972 | -0.377 | 0.637 | 0.732 | 0.120 | 0.120 | 0.762 | 0.070 | 0.230 |
| MolMotifHard | GINE | GNNExplainer | random | 200 | 0.571 | 0.086 | 0.942 | 0.737 | 0.196 | 0.266 | 0.771 | 0.154 | 0.063 |
| MolMotifHard | GINE | GNNExplainer | scaffold | 200 | 0.303 | -0.289 | 0.960 | 0.810 | 0.139 | 0.154 | 0.775 | 0.098 | 0.231 |
| MolMotifHard | GINE | GuidedBackprop | random | 200 | 0.923 | -0.181 | 0.884 | 0.790 | 0.164 | 0.250 | 0.758 | 0.107 | 0.084 |
| MolMotifHard | GINE | GuidedBackprop | scaffold | 200 | 0.824 | -0.350 | 0.794 | 0.812 | 0.235 | 0.138 | 0.767 | 0.185 | 0.179 |
| MolMotifHard | GINE | InputXGradient | random | 200 | 0.988 | -0.081 | 0.925 | 0.802 | 0.216 | 0.225 | 0.762 | 0.138 | 0.211 |
| MolMotifHard | GINE | InputXGradient | scaffold | 200 | 1.000 | -0.383 | 0.873 | 0.788 | 0.213 | 0.159 | 0.764 | 0.183 | 0.416 |
| MolMotifHard | GINE | IntegratedGradients | random | 200 | 0.982 | -0.064 | 0.914 | 0.722 | 0.168 | 0.290 | 0.764 | 0.099 | 0.174 |
| MolMotifHard | GINE | IntegratedGradients | scaffold | 200 | 1.000 | -0.448 | 0.909 | 0.773 | 0.279 | 0.169 | 0.763 | 0.238 | 0.206 |
| MolMotifHard | GINE | PGExplainer | random | 200 | 0.493 | -0.118 | 0.830 | 0.827 | 0.146 | 0.210 | 0.719 | 0.113 | — |
| MolMotifHard | GINE | PGExplainer | scaffold | 200 | 0.565 | -0.228 | 0.717 | 0.764 | 0.067 | 0.154 | 0.584 | 0.094 | — |
| MolMotifHard | GINE | Saliency | random | 200 | 0.994 | -0.077 | 0.911 | 0.794 | 0.200 | 0.208 | 0.765 | 0.127 | 0.398 |
| MolMotifHard | GINE | Saliency | scaffold | 200 | 1.000 | -0.408 | 0.847 | 0.791 | 0.249 | 0.157 | 0.765 | 0.202 | 0.300 |
| MolMotifHard | GINE | SubgraphX | random | 200 | 0.421 | 0.171 | — | 0.919 | 0.222 | 0.117 | 0.307 | 0.256 | — |
| MolMotifHard | GINE | SubgraphX | scaffold | 200 | 0.443 | -0.300 | — | 0.937 | 0.127 | 0.183 | 0.347 | 0.141 | — |
| MolMotifHard | MPNN | IntegratedGradients | random | 200 | 0.969 | 0.392 | 0.933 | 0.753 | 0.158 | 0.301 | 0.766 | 0.191 | 0.278 |
| MolMotifHard | MPNN | IntegratedGradients | scaffold | 200 | 0.982 | 0.633 | 0.886 | 0.839 | 0.553 | 0.064 | 0.765 | 0.532 | 0.235 |
| SIDER | GCN | IntegratedGradients | random | 200 | — | -0.110 | 0.750 | 0.746 | 0.084 | 0.022 | 0.751 | 0.154 | 0.054 |
| SIDER | GCN | IntegratedGradients | scaffold | 200 | — | 0.231 | 0.879 | 0.754 | 0.121 | 0.248 | 0.762 | 0.179 | 0.033 |
| SIDER | GINE | IntegratedGradients | random | 200 | — | 0.427 | 0.869 | 0.764 | 0.333 | 0.389 | 0.754 | 0.243 | 0.449 |
| SIDER | GINE | IntegratedGradients | scaffold | 200 | — | 0.503 | 0.866 | 0.743 | 0.235 | 0.318 | 0.763 | 0.293 | 0.511 |
| ShapeGGen | GINE | GNNExplainer | random | 50 | 0.483 | 0.154 | 0.563 | 0.069 | 0.003 | 0.008 | 0.776 | 0.007 | 0.001 |
| ShapeGGen | GINE | GNNExplainer | scaffold | 50 | 0.496 | 0.085 | 0.417 | 0.076 | 0.001 | 0.003 | 0.771 | 0.004 | 0.000 |
| ShapeGGen | GINE | GuidedBackprop | random | 50 | 0.791 | 0.465 | 0.796 | 0.160 | 0.008 | 0.003 | 0.776 | 0.016 | 0.001 |
| ShapeGGen | GINE | GuidedBackprop | scaffold | 50 | 0.773 | 0.186 | 0.593 | 0.164 | 0.004 | -0.001 | 0.771 | 0.010 | 0.000 |
| ShapeGGen | GINE | InputXGradient | random | 50 | 0.732 | 0.473 | 0.744 | 0.174 | 0.008 | 0.003 | 0.776 | 0.016 | 0.001 |
| ShapeGGen | GINE | InputXGradient | scaffold | 50 | 0.676 | 0.337 | 0.494 | 0.182 | 0.005 | -0.002 | 0.771 | 0.011 | 0.000 |
| ShapeGGen | GINE | IntegratedGradients | random | 50 | 0.751 | 0.497 | 0.763 | 0.172 | 0.008 | 0.003 | 0.776 | 0.016 | 0.001 |
| ShapeGGen | GINE | IntegratedGradients | scaffold | 50 | 0.708 | 0.303 | 0.505 | 0.183 | 0.005 | -0.002 | 0.771 | 0.011 | 0.000 |
| ShapeGGen | GINE | PGExplainer | random | 50 | 0.489 | -0.167 | 0.676 | 0.429 | 0.002 | 0.009 | 0.698 | 0.005 | — |
| ShapeGGen | GINE | PGExplainer | scaffold | 50 | 0.615 | -0.177 | 0.653 | 0.458 | -0.000 | 0.004 | 0.764 | 0.001 | — |
| ShapeGGen | GINE | Saliency | random | 50 | 0.769 | 0.425 | 0.730 | 0.159 | 0.007 | 0.003 | 0.776 | 0.015 | 0.001 |
| ShapeGGen | GINE | Saliency | scaffold | 50 | 0.742 | 0.297 | 0.445 | 0.164 | 0.005 | -0.002 | 0.771 | 0.011 | 0.000 |
| ShapeGGen | GINE | SubgraphX | random | 50 | 0.620 | 0.471 | 0.233 | 0.180 | 0.011 | -0.000 | 0.567 | 0.021 | — |
| ShapeGGen | GINE | SubgraphX | scaffold | 50 | 0.548 | 0.413 | 0.217 | 0.231 | 0.007 | -0.004 | 0.514 | 0.014 | — |
| SynthMotifs | AttentiveFP | IntegratedGradients | random | 200 | 0.898 | 0.104 | 0.726 | 0.146 | 0.369 | 0.204 | 0.796 | 0.289 | 0.446 |
| SynthMotifs | AttentiveFP | IntegratedGradients | scaffold | 200 | 0.909 | 0.159 | 0.741 | 0.147 | 0.421 | 0.139 | 0.795 | 0.407 | 0.486 |
| SynthMotifs | GAT | IntegratedGradients | random | 200 | 0.642 | 0.230 | 0.384 | 0.119 | 0.315 | 0.319 | 0.792 | 0.093 | 0.434 |
| SynthMotifs | GAT | IntegratedGradients | scaffold | 200 | 0.920 | 0.336 | 1.000 | 0.120 | 0.455 | 0.364 | 0.797 | 0.515 | 0.469 |
| SynthMotifs | GCN | IntegratedGradients | random | 200 | 0.990 | 0.433 | 0.694 | 0.169 | 0.443 | 0.062 | 0.798 | 0.590 | 0.488 |
| SynthMotifs | GCN | IntegratedGradients | scaffold | 200 | 0.981 | 0.344 | 0.625 | 0.169 | 0.313 | 0.117 | 0.798 | 0.431 | 0.292 |
| SynthMotifs | GINE | GNNExplainer | random | 200 | 0.698 | 0.199 | 0.698 | 0.048 | 0.217 | 0.251 | 0.800 | 0.310 | 0.155 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 200 | 0.575 | 0.075 | 0.637 | 0.046 | 0.448 | 0.377 | 0.800 | 0.461 | 0.476 |
| SynthMotifs | GINE | GuidedBackprop | random | 200 | 0.996 | 0.613 | 0.795 | 0.164 | 0.261 | 0.059 | 0.800 | 0.393 | 0.210 |
| SynthMotifs | GINE | GuidedBackprop | scaffold | 200 | 0.970 | 0.636 | 0.732 | 0.126 | 0.461 | 0.081 | 0.796 | 0.577 | 0.534 |
| SynthMotifs | GINE | InputXGradient | random | 200 | 0.959 | 0.498 | 0.656 | 0.238 | 0.261 | 0.132 | 0.795 | 0.379 | 0.203 |
| SynthMotifs | GINE | InputXGradient | scaffold | 200 | 0.961 | 0.434 | 0.705 | 0.204 | 0.433 | 0.187 | 0.797 | 0.500 | 0.489 |
| SynthMotifs | GINE | IntegratedGradients | random | 200 | 0.977 | 0.479 | 0.849 | 0.162 | 0.256 | 0.129 | 0.799 | 0.379 | 0.200 |
| SynthMotifs | GINE | IntegratedGradients | scaffold | 200 | 0.966 | 0.480 | 0.741 | 0.158 | 0.474 | 0.106 | 0.798 | 0.593 | 0.537 |
| SynthMotifs | GINE | PGExplainer | random | 200 | 0.314 | -0.149 | 0.427 | 0.385 | 0.010 | 0.263 | 0.786 | 0.035 | — |
| SynthMotifs | GINE | PGExplainer | scaffold | 200 | 0.331 | -0.101 | 0.585 | 0.393 | 0.084 | 0.385 | 0.734 | 0.117 | — |
| SynthMotifs | GINE | Saliency | random | 200 | 0.960 | 0.513 | 0.560 | 0.176 | 0.262 | 0.141 | 0.796 | 0.380 | 0.208 |
| SynthMotifs | GINE | Saliency | scaffold | 200 | 0.969 | 0.420 | 0.601 | 0.148 | 0.430 | 0.140 | 0.797 | 0.508 | 0.530 |
| SynthMotifs | GINE | SubgraphX | random | 200 | 0.845 | 0.551 | 0.744 | 0.159 | 0.234 | 0.044 | 0.659 | 0.359 | — |
| SynthMotifs | GINE | SubgraphX | scaffold | 200 | 0.777 | 0.430 | 0.562 | 0.183 | 0.436 | 0.094 | 0.517 | 0.556 | — |
| SynthMotifs | MPNN | IntegratedGradients | random | 200 | 0.903 | 0.399 | 0.590 | 0.090 | 0.468 | 0.485 | 0.796 | 0.244 | 0.453 |
| SynthMotifs | MPNN | IntegratedGradients | scaffold | 200 | 0.860 | 0.241 | 0.550 | 0.139 | 0.322 | 0.244 | 0.795 | 0.411 | 0.752 |
| Tox21 | GINE | IntegratedGradients | random | 200 | — | -0.063 | 0.710 | 0.725 | -0.096 | -0.060 | 0.753 | 0.037 | 0.309 |
| Tox21 | GINE | IntegratedGradients | scaffold | 200 | — | -0.592 | 0.927 | 0.781 | -0.156 | -0.159 | 0.736 | 0.042 | 0.149 |
| hERG | GINE | IntegratedGradients | random | 197 | — | 0.776 | 0.953 | 0.773 | 0.765 | 0.765 | 0.779 | 0.188 | 0.809 |
| hERG | GINE | IntegratedGradients | scaffold | 197 | — | 0.863 | 0.943 | 0.794 | 0.854 | 0.854 | 0.777 | 0.074 | 0.642 |

## Paired attributor comparisons (Wilcoxon, shared molecules)

**BA-2Motifs · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 200 | 0.454 | 0.000 |
| GNNExplainer | InputXGradient | 200 | 0.453 | 0.000 |
| GNNExplainer | IntegratedGradients | 200 | 0.502 | 0.000 |
| GNNExplainer | PGExplainer | 200 | -0.391 | 0.000 |
| GNNExplainer | Saliency | 200 | 0.453 | 0.000 |
| GuidedBackprop | InputXGradient | 200 | -0.046 | 0.000 |
| GuidedBackprop | IntegratedGradients | 200 | 0.012 | 0.086 |
| GuidedBackprop | PGExplainer | 200 | -0.996 | 0.000 |
| GuidedBackprop | Saliency | 200 | -0.046 | 0.000 |
| InputXGradient | IntegratedGradients | 200 | 0.010 | 0.110 |
| InputXGradient | PGExplainer | 200 | -1.036 | 0.000 |
| InputXGradient | Saliency | 200 | 0.000 | 0.655 |
| IntegratedGradients | PGExplainer | 200 | -1.111 | 0.000 |
| IntegratedGradients | Saliency | 200 | -0.010 | 0.110 |
| PGExplainer | Saliency | 200 | 1.036 | 0.000 |

**BA-2Motifs · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 200 | 0.703 | 0.000 |
| GNNExplainer | InputXGradient | 200 | 0.701 | 0.000 |
| GNNExplainer | IntegratedGradients | 200 | 0.662 | 0.000 |
| GNNExplainer | PGExplainer | 200 | -0.117 | 0.000 |
| GNNExplainer | Saliency | 200 | 0.701 | 0.000 |
| GuidedBackprop | InputXGradient | 200 | -0.005 | 0.498 |
| GuidedBackprop | IntegratedGradients | 200 | -0.037 | 0.000 |
| GuidedBackprop | PGExplainer | 200 | -0.802 | 0.000 |
| GuidedBackprop | Saliency | 200 | -0.005 | 0.500 |
| InputXGradient | IntegratedGradients | 200 | -0.026 | 0.000 |
| InputXGradient | PGExplainer | 200 | -0.791 | 0.000 |
| InputXGradient | Saliency | 200 | 0.000 | 0.180 |
| IntegratedGradients | PGExplainer | 200 | -0.753 | 0.000 |
| IntegratedGradients | Saliency | 200 | 0.026 | 0.000 |
| PGExplainer | Saliency | 200 | 0.791 | 0.000 |

**BBBP · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 189 | 0.000 | 0.450 |
| GNNExplainer | PGExplainer | 178 | 0.135 | 0.000 |
| IntegratedGradients | PGExplainer | 178 | 0.122 | 0.000 |

**BBBP · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 196 | -0.089 | 0.000 |
| GNNExplainer | PGExplainer | 179 | 0.270 | 0.000 |
| IntegratedGradients | PGExplainer | 179 | 0.435 | 0.000 |

**Benzene · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 200 | -0.253 | 0.000 |
| GNNExplainer | InputXGradient | 200 | 0.132 | 0.650 |
| GNNExplainer | IntegratedGradients | 200 | -0.145 | 0.001 |
| GNNExplainer | PGExplainer | 55 | 0.429 | 0.000 |
| GNNExplainer | Saliency | 200 | 0.159 | 0.051 |
| GNNExplainer | SubgraphX | 200 | -0.239 | 0.000 |
| GuidedBackprop | InputXGradient | 200 | 0.218 | 0.000 |
| GuidedBackprop | IntegratedGradients | 200 | 0.046 | 0.001 |
| GuidedBackprop | PGExplainer | 55 | 0.558 | 0.000 |
| GuidedBackprop | Saliency | 200 | 0.248 | 0.000 |
| GuidedBackprop | SubgraphX | 200 | 0.036 | 0.404 |
| InputXGradient | IntegratedGradients | 200 | -0.117 | 0.000 |
| InputXGradient | PGExplainer | 55 | 0.113 | 0.011 |
| InputXGradient | Saliency | 200 | 0.033 | 0.000 |
| InputXGradient | SubgraphX | 200 | -0.296 | 0.000 |
| IntegratedGradients | PGExplainer | 55 | 0.390 | 0.000 |
| IntegratedGradients | Saliency | 200 | 0.179 | 0.000 |
| IntegratedGradients | SubgraphX | 200 | -0.011 | 0.123 |
| PGExplainer | Saliency | 55 | -0.057 | 0.123 |
| PGExplainer | SubgraphX | 55 | -0.663 | 0.000 |
| Saliency | SubgraphX | 200 | -0.362 | 0.000 |

**Benzene · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 198 | -0.072 | 0.000 |
| GNNExplainer | InputXGradient | 198 | 0.000 | 0.077 |
| GNNExplainer | IntegratedGradients | 198 | -0.036 | 0.001 |
| GNNExplainer | PGExplainer | 189 | 0.443 | 0.000 |
| GNNExplainer | Saliency | 198 | 0.000 | 0.389 |
| GNNExplainer | SubgraphX | 197 | -0.022 | 0.992 |
| GuidedBackprop | InputXGradient | 198 | 0.036 | 0.000 |
| GuidedBackprop | IntegratedGradients | 198 | 0.000 | 0.022 |
| GuidedBackprop | PGExplainer | 189 | 0.568 | 0.000 |
| GuidedBackprop | Saliency | 198 | 0.036 | 0.000 |
| GuidedBackprop | SubgraphX | 197 | 0.031 | 0.005 |
| InputXGradient | IntegratedGradients | 198 | 0.000 | 0.000 |
| InputXGradient | PGExplainer | 189 | 0.358 | 0.000 |
| InputXGradient | Saliency | 198 | 0.000 | 0.033 |
| InputXGradient | SubgraphX | 197 | -0.005 | 0.359 |
| IntegratedGradients | PGExplainer | 189 | 0.529 | 0.000 |
| IntegratedGradients | Saliency | 198 | 0.000 | 0.000 |
| IntegratedGradients | SubgraphX | 197 | 0.030 | 0.111 |
| PGExplainer | Saliency | 189 | -0.431 | 0.000 |
| PGExplainer | SubgraphX | 188 | -0.443 | 0.000 |
| Saliency | SubgraphX | 197 | 0.003 | 0.686 |

**ClinTox · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 139 | 0.000 | 0.205 |

**ClinTox · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 122 | 0.000 | 0.305 |

**ESOL · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 156 | 0.000 | 0.001 |

**ESOL · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 109 | 0.000 | 0.089 |

**FluorideCarbonyl · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 200 | -0.157 | 0.000 |
| GNNExplainer | InputXGradient | 200 | 0.036 | 0.142 |
| GNNExplainer | IntegratedGradients | 200 | -0.046 | 0.067 |
| GNNExplainer | PGExplainer | 200 | 0.427 | 0.000 |
| GNNExplainer | Saliency | 200 | -0.045 | 0.138 |
| GNNExplainer | SubgraphX | 55 | -0.099 | 0.541 |
| GuidedBackprop | InputXGradient | 200 | 0.180 | 0.000 |
| GuidedBackprop | IntegratedGradients | 200 | 0.175 | 0.000 |
| GuidedBackprop | PGExplainer | 200 | 0.604 | 0.000 |
| GuidedBackprop | Saliency | 200 | 0.118 | 0.000 |
| GuidedBackprop | SubgraphX | 55 | 0.265 | 0.000 |
| InputXGradient | IntegratedGradients | 200 | -0.061 | 0.022 |
| InputXGradient | PGExplainer | 200 | 0.321 | 0.000 |
| InputXGradient | Saliency | 200 | -0.070 | 0.000 |
| InputXGradient | SubgraphX | 55 | 0.079 | 0.763 |
| IntegratedGradients | PGExplainer | 200 | 0.402 | 0.000 |
| IntegratedGradients | Saliency | 200 | 0.003 | 0.607 |
| IntegratedGradients | SubgraphX | 55 | 0.000 | 0.738 |
| PGExplainer | Saliency | 200 | -0.431 | 0.000 |
| PGExplainer | SubgraphX | 55 | -0.295 | 0.000 |
| Saliency | SubgraphX | 55 | 0.134 | 0.083 |

**FluorideCarbonyl · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 198 | -0.260 | 0.000 |
| GNNExplainer | InputXGradient | 198 | -0.196 | 0.000 |
| GNNExplainer | IntegratedGradients | 198 | -0.140 | 0.000 |
| GNNExplainer | PGExplainer | 195 | 0.000 | 0.644 |
| GNNExplainer | Saliency | 198 | -0.139 | 0.000 |
| GNNExplainer | SubgraphX | 198 | -0.034 | 0.005 |
| GuidedBackprop | InputXGradient | 198 | 0.058 | 0.000 |
| GuidedBackprop | IntegratedGradients | 198 | 0.135 | 0.000 |
| GuidedBackprop | PGExplainer | 195 | 0.357 | 0.000 |
| GuidedBackprop | Saliency | 198 | 0.075 | 0.000 |
| GuidedBackprop | SubgraphX | 198 | 0.213 | 0.000 |
| InputXGradient | IntegratedGradients | 198 | 0.000 | 0.836 |
| InputXGradient | PGExplainer | 195 | 0.136 | 0.000 |
| InputXGradient | Saliency | 198 | 0.000 | 0.062 |
| InputXGradient | SubgraphX | 198 | 0.091 | 0.001 |
| IntegratedGradients | PGExplainer | 195 | 0.222 | 0.000 |
| IntegratedGradients | Saliency | 198 | 0.000 | 0.804 |
| IntegratedGradients | SubgraphX | 198 | 0.014 | 0.081 |
| PGExplainer | Saliency | 195 | -0.137 | 0.000 |
| PGExplainer | SubgraphX | 195 | -0.083 | 0.018 |
| Saliency | SubgraphX | 198 | 0.049 | 0.005 |

**MUTAG · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 58 | -0.046 | 0.148 |
| GNNExplainer | InputXGradient | 58 | 0.000 | 0.608 |
| GNNExplainer | IntegratedGradients | 58 | 0.000 | 0.704 |
| GNNExplainer | PGExplainer | 57 | 0.070 | 0.007 |
| GNNExplainer | Saliency | 58 | 0.000 | 0.597 |
| GNNExplainer | SubgraphX | 57 | 0.000 | 0.774 |
| GuidedBackprop | InputXGradient | 58 | 0.000 | 0.005 |
| GuidedBackprop | IntegratedGradients | 58 | 0.000 | 0.046 |
| GuidedBackprop | PGExplainer | 57 | 0.316 | 0.000 |
| GuidedBackprop | Saliency | 58 | 0.000 | 0.005 |
| GuidedBackprop | SubgraphX | 57 | 0.028 | 0.154 |
| InputXGradient | IntegratedGradients | 58 | 0.000 | 0.862 |
| InputXGradient | PGExplainer | 57 | 0.213 | 0.000 |
| InputXGradient | Saliency | 58 | 0.000 | 0.779 |
| InputXGradient | SubgraphX | 57 | -0.015 | 0.711 |
| IntegratedGradients | PGExplainer | 57 | 0.149 | 0.006 |
| IntegratedGradients | Saliency | 58 | 0.000 | 0.885 |
| IntegratedGradients | SubgraphX | 57 | 0.000 | 0.692 |
| PGExplainer | Saliency | 57 | -0.193 | 0.000 |
| PGExplainer | SubgraphX | 56 | -0.167 | 0.000 |
| Saliency | SubgraphX | 57 | 0.000 | 0.689 |

**MUTAG · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 53 | -0.200 | 0.000 |
| GNNExplainer | InputXGradient | 53 | -0.017 | 0.019 |
| GNNExplainer | IntegratedGradients | 53 | 0.000 | 0.276 |
| GNNExplainer | PGExplainer | 52 | 0.081 | 0.082 |
| GNNExplainer | Saliency | 53 | 0.000 | 0.722 |
| GNNExplainer | SubgraphX | 53 | 0.000 | 0.746 |
| GuidedBackprop | InputXGradient | 53 | 0.058 | 0.000 |
| GuidedBackprop | IntegratedGradients | 53 | 0.357 | 0.000 |
| GuidedBackprop | PGExplainer | 52 | 0.300 | 0.000 |
| GuidedBackprop | Saliency | 53 | 0.107 | 0.000 |
| GuidedBackprop | SubgraphX | 53 | 0.200 | 0.000 |
| InputXGradient | IntegratedGradients | 53 | 0.200 | 0.002 |
| InputXGradient | PGExplainer | 52 | 0.207 | 0.000 |
| InputXGradient | Saliency | 53 | 0.000 | 0.029 |
| InputXGradient | SubgraphX | 53 | 0.023 | 0.137 |
| IntegratedGradients | PGExplainer | 52 | 0.000 | 0.525 |
| IntegratedGradients | Saliency | 53 | 0.000 | 0.098 |
| IntegratedGradients | SubgraphX | 53 | 0.000 | 0.355 |
| PGExplainer | Saliency | 52 | -0.081 | 0.044 |
| PGExplainer | SubgraphX | 52 | 0.000 | 0.281 |
| Saliency | SubgraphX | 53 | 0.033 | 0.660 |

**MolMotif · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 194 | 0.057 | 0.000 |
| GNNExplainer | InputXGradient | 194 | 0.057 | 0.000 |
| GNNExplainer | IntegratedGradients | 194 | 0.023 | 0.035 |
| GNNExplainer | PGExplainer | 191 | 0.000 | 0.271 |
| GNNExplainer | Saliency | 194 | 0.068 | 0.000 |
| GNNExplainer | SubgraphX | 193 | 0.077 | 0.028 |
| GuidedBackprop | InputXGradient | 194 | 0.000 | 0.032 |
| GuidedBackprop | IntegratedGradients | 194 | 0.000 | 0.000 |
| GuidedBackprop | PGExplainer | 191 | -0.105 | 0.000 |
| GuidedBackprop | Saliency | 194 | 0.000 | 0.082 |
| GuidedBackprop | SubgraphX | 193 | -0.003 | 0.046 |
| InputXGradient | IntegratedGradients | 194 | 0.000 | 0.002 |
| InputXGradient | PGExplainer | 191 | -0.066 | 0.000 |
| InputXGradient | Saliency | 194 | 0.000 | 0.176 |
| InputXGradient | SubgraphX | 193 | -0.002 | 0.187 |
| IntegratedGradients | PGExplainer | 191 | -0.029 | 0.980 |
| IntegratedGradients | Saliency | 194 | 0.000 | 0.000 |
| IntegratedGradients | SubgraphX | 193 | 0.013 | 0.323 |
| PGExplainer | Saliency | 191 | 0.091 | 0.000 |
| PGExplainer | SubgraphX | 190 | 0.068 | 0.137 |
| Saliency | SubgraphX | 193 | -0.012 | 0.091 |

**MolMotif · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 197 | 0.007 | 0.000 |
| GNNExplainer | InputXGradient | 197 | 0.046 | 0.000 |
| GNNExplainer | IntegratedGradients | 197 | 0.000 | 0.742 |
| GNNExplainer | PGExplainer | 194 | 0.082 | 0.002 |
| GNNExplainer | Saliency | 197 | 0.024 | 0.000 |
| GNNExplainer | SubgraphX | 195 | 0.084 | 0.000 |
| GuidedBackprop | InputXGradient | 197 | 0.000 | 0.667 |
| GuidedBackprop | IntegratedGradients | 197 | 0.000 | 0.000 |
| GuidedBackprop | PGExplainer | 194 | 0.000 | 0.423 |
| GuidedBackprop | Saliency | 197 | 0.000 | 0.088 |
| GuidedBackprop | SubgraphX | 195 | 0.028 | 0.401 |
| InputXGradient | IntegratedGradients | 197 | -0.006 | 0.000 |
| InputXGradient | PGExplainer | 194 | 0.018 | 0.283 |
| InputXGradient | Saliency | 197 | 0.000 | 0.036 |
| InputXGradient | SubgraphX | 195 | 0.006 | 0.871 |
| IntegratedGradients | PGExplainer | 194 | 0.039 | 0.003 |
| IntegratedGradients | Saliency | 197 | 0.000 | 0.000 |
| IntegratedGradients | SubgraphX | 195 | 0.077 | 0.000 |
| PGExplainer | Saliency | 194 | 0.000 | 0.537 |
| PGExplainer | SubgraphX | 192 | 0.000 | 0.455 |
| Saliency | SubgraphX | 195 | 0.000 | 0.819 |

**MolMotifHard · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 172 | 0.000 | 0.000 |
| GNNExplainer | InputXGradient | 172 | 0.000 | 0.006 |
| GNNExplainer | IntegratedGradients | 172 | 0.000 | 0.020 |
| GNNExplainer | PGExplainer | 162 | 0.033 | 0.006 |
| GNNExplainer | Saliency | 172 | 0.000 | 0.013 |
| GNNExplainer | SubgraphX | 170 | -0.032 | 0.014 |
| GuidedBackprop | InputXGradient | 172 | 0.000 | 0.016 |
| GuidedBackprop | IntegratedGradients | 172 | 0.000 | 0.016 |
| GuidedBackprop | PGExplainer | 162 | 0.000 | 0.942 |
| GuidedBackprop | Saliency | 172 | 0.000 | 0.009 |
| GuidedBackprop | SubgraphX | 170 | -0.188 | 0.000 |
| InputXGradient | IntegratedGradients | 172 | 0.000 | 0.587 |
| InputXGradient | PGExplainer | 162 | 0.000 | 0.117 |
| InputXGradient | Saliency | 172 | 0.000 | 0.255 |
| InputXGradient | SubgraphX | 170 | -0.097 | 0.001 |
| IntegratedGradients | PGExplainer | 162 | 0.000 | 0.051 |
| IntegratedGradients | Saliency | 172 | 0.000 | 0.893 |
| IntegratedGradients | SubgraphX | 170 | -0.016 | 0.002 |
| PGExplainer | Saliency | 162 | 0.000 | 0.089 |
| PGExplainer | SubgraphX | 162 | -0.155 | 0.000 |
| Saliency | SubgraphX | 170 | -0.078 | 0.001 |

**MolMotifHard · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 161 | 0.000 | 0.029 |
| GNNExplainer | InputXGradient | 161 | 0.071 | 0.006 |
| GNNExplainer | IntegratedGradients | 161 | 0.100 | 0.000 |
| GNNExplainer | PGExplainer | 132 | 0.000 | 0.281 |
| GNNExplainer | Saliency | 161 | 0.095 | 0.001 |
| GNNExplainer | SubgraphX | 158 | 0.015 | 0.411 |
| GuidedBackprop | InputXGradient | 161 | 0.000 | 0.384 |
| GuidedBackprop | IntegratedGradients | 161 | 0.000 | 0.002 |
| GuidedBackprop | PGExplainer | 132 | -0.022 | 0.083 |
| GuidedBackprop | Saliency | 161 | 0.000 | 0.099 |
| GuidedBackprop | SubgraphX | 158 | -0.044 | 0.114 |
| InputXGradient | IntegratedGradients | 161 | 0.000 | 0.008 |
| InputXGradient | PGExplainer | 132 | -0.100 | 0.005 |
| InputXGradient | Saliency | 161 | 0.000 | 0.178 |
| InputXGradient | SubgraphX | 158 | -0.097 | 0.022 |
| IntegratedGradients | PGExplainer | 132 | -0.111 | 0.000 |
| IntegratedGradients | Saliency | 161 | 0.000 | 0.041 |
| IntegratedGradients | SubgraphX | 158 | -0.120 | 0.000 |
| PGExplainer | Saliency | 132 | 0.079 | 0.001 |
| PGExplainer | SubgraphX | 130 | 0.027 | 0.069 |
| Saliency | SubgraphX | 158 | -0.097 | 0.005 |

**ShapeGGen · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 50 | -0.341 | 0.000 |
| GNNExplainer | InputXGradient | 50 | -0.379 | 0.000 |
| GNNExplainer | IntegratedGradients | 50 | -0.360 | 0.000 |
| GNNExplainer | PGExplainer | 47 | 0.372 | 0.000 |
| GNNExplainer | Saliency | 50 | -0.311 | 0.000 |
| GNNExplainer | SubgraphX | 50 | -0.381 | 0.000 |
| GuidedBackprop | InputXGradient | 50 | 0.005 | 0.980 |
| GuidedBackprop | IntegratedGradients | 50 | -0.001 | 0.328 |
| GuidedBackprop | PGExplainer | 47 | 0.682 | 0.000 |
| GuidedBackprop | Saliency | 50 | 0.032 | 0.041 |
| GuidedBackprop | SubgraphX | 50 | -0.028 | 0.527 |
| InputXGradient | IntegratedGradients | 50 | -0.025 | 0.073 |
| InputXGradient | PGExplainer | 47 | 0.688 | 0.000 |
| InputXGradient | Saliency | 50 | 0.024 | 0.005 |
| InputXGradient | SubgraphX | 50 | -0.002 | 0.789 |
| IntegratedGradients | PGExplainer | 47 | 0.696 | 0.000 |
| IntegratedGradients | Saliency | 50 | 0.055 | 0.002 |
| IntegratedGradients | SubgraphX | 50 | -0.001 | 0.789 |
| PGExplainer | Saliency | 47 | -0.663 | 0.000 |
| PGExplainer | SubgraphX | 47 | -0.687 | 0.000 |
| Saliency | SubgraphX | 50 | -0.059 | 0.081 |

**ShapeGGen · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 50 | -0.067 | 0.135 |
| GNNExplainer | InputXGradient | 50 | -0.253 | 0.000 |
| GNNExplainer | IntegratedGradients | 50 | -0.174 | 0.000 |
| GNNExplainer | PGExplainer | 50 | 0.333 | 0.000 |
| GNNExplainer | Saliency | 50 | -0.207 | 0.000 |
| GNNExplainer | SubgraphX | 50 | -0.320 | 0.000 |
| GuidedBackprop | InputXGradient | 50 | -0.152 | 0.000 |
| GuidedBackprop | IntegratedGradients | 50 | -0.101 | 0.000 |
| GuidedBackprop | PGExplainer | 50 | 0.320 | 0.000 |
| GuidedBackprop | Saliency | 50 | -0.057 | 0.000 |
| GuidedBackprop | SubgraphX | 50 | -0.256 | 0.000 |
| InputXGradient | IntegratedGradients | 50 | 0.016 | 0.062 |
| InputXGradient | PGExplainer | 50 | 0.512 | 0.000 |
| InputXGradient | Saliency | 50 | 0.016 | 0.287 |
| InputXGradient | SubgraphX | 50 | -0.087 | 0.123 |
| IntegratedGradients | PGExplainer | 50 | 0.432 | 0.000 |
| IntegratedGradients | Saliency | 50 | 0.000 | 0.975 |
| IntegratedGradients | SubgraphX | 50 | -0.140 | 0.019 |
| PGExplainer | Saliency | 50 | -0.414 | 0.000 |
| PGExplainer | SubgraphX | 50 | -0.589 | 0.000 |
| Saliency | SubgraphX | 50 | -0.140 | 0.009 |

**SynthMotifs · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 200 | -0.371 | 0.000 |
| GNNExplainer | InputXGradient | 200 | -0.275 | 0.000 |
| GNNExplainer | IntegratedGradients | 200 | -0.250 | 0.000 |
| GNNExplainer | PGExplainer | 200 | 0.366 | 0.000 |
| GNNExplainer | Saliency | 200 | -0.295 | 0.000 |
| GNNExplainer | SubgraphX | 200 | -0.369 | 0.000 |
| GuidedBackprop | InputXGradient | 200 | 0.092 | 0.000 |
| GuidedBackprop | IntegratedGradients | 200 | 0.110 | 0.000 |
| GuidedBackprop | PGExplainer | 200 | 0.811 | 0.000 |
| GuidedBackprop | Saliency | 200 | 0.094 | 0.000 |
| GuidedBackprop | SubgraphX | 200 | 0.053 | 0.190 |
| InputXGradient | IntegratedGradients | 200 | 0.021 | 0.019 |
| InputXGradient | PGExplainer | 200 | 0.682 | 0.000 |
| InputXGradient | Saliency | 200 | -0.013 | 0.001 |
| InputXGradient | SubgraphX | 200 | 0.011 | 0.063 |
| IntegratedGradients | PGExplainer | 200 | 0.672 | 0.000 |
| IntegratedGradients | Saliency | 200 | -0.035 | 0.003 |
| IntegratedGradients | SubgraphX | 200 | -0.016 | 0.009 |
| PGExplainer | Saliency | 200 | -0.695 | 0.000 |
| PGExplainer | SubgraphX | 200 | -0.802 | 0.000 |
| Saliency | SubgraphX | 200 | -0.000 | 0.092 |

**SynthMotifs · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | GuidedBackprop | 200 | -0.557 | 0.000 |
| GNNExplainer | InputXGradient | 200 | -0.372 | 0.000 |
| GNNExplainer | IntegratedGradients | 200 | -0.414 | 0.000 |
| GNNExplainer | PGExplainer | 199 | 0.231 | 0.000 |
| GNNExplainer | Saliency | 200 | -0.366 | 0.000 |
| GNNExplainer | SubgraphX | 200 | -0.370 | 0.000 |
| GuidedBackprop | InputXGradient | 200 | 0.163 | 0.000 |
| GuidedBackprop | IntegratedGradients | 200 | 0.187 | 0.000 |
| GuidedBackprop | PGExplainer | 199 | 0.822 | 0.000 |
| GuidedBackprop | Saliency | 200 | 0.152 | 0.000 |
| GuidedBackprop | SubgraphX | 200 | 0.204 | 0.000 |
| InputXGradient | IntegratedGradients | 200 | 0.090 | 0.196 |
| InputXGradient | PGExplainer | 199 | 0.625 | 0.000 |
| InputXGradient | Saliency | 200 | 0.018 | 0.001 |
| InputXGradient | SubgraphX | 200 | 0.075 | 0.524 |
| IntegratedGradients | PGExplainer | 199 | 0.613 | 0.000 |
| IntegratedGradients | Saliency | 200 | -0.070 | 0.089 |
| IntegratedGradients | SubgraphX | 200 | -0.012 | 0.321 |
| PGExplainer | Saliency | 199 | -0.591 | 0.000 |
| PGExplainer | SubgraphX | 199 | -0.572 | 0.000 |
| Saliency | SubgraphX | 200 | 0.082 | 0.612 |

