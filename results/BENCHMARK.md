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
| BA-2Motifs | GINE | GNNExplainer | scaffold | 200 | 0.503 | 0.007 | 0.985 | 0.042 | 0.003 | 0.011 | 0.800 | 0.007 | — |
| BA-2Motifs | GINE | GuidedBackprop | random | 200 | 0.948 | -0.323 | 0.745 | 0.133 | -0.013 | -0.014 | 0.797 | 0.012 | — |
| BA-2Motifs | GINE | GuidedBackprop | scaffold | 200 | 0.908 | 0.506 | 0.845 | 0.136 | 0.007 | 0.006 | 0.792 | 0.018 | — |
| BA-2Motifs | GINE | InputXGradient | random | 200 | 0.928 | -0.260 | 0.796 | 0.127 | -0.012 | -0.016 | 0.790 | 0.012 | — |
| BA-2Motifs | GINE | InputXGradient | scaffold | 200 | 0.963 | 0.516 | 0.754 | 0.127 | 0.007 | 0.007 | 0.800 | 0.016 | — |
| BA-2Motifs | GINE | IntegratedGradients | random | 200 | 0.994 | -0.276 | 0.645 | 0.132 | -0.013 | -0.014 | 0.800 | 0.012 | — |
| BA-2Motifs | GINE | IntegratedGradients | scaffold | 200 | 0.947 | 0.519 | 0.820 | 0.128 | 0.009 | 0.005 | 0.800 | 0.020 | — |
| BA-2Motifs | GINE | PGExplainer | random | 200 | 0.104 | 0.155 | 0.305 | 0.378 | -0.003 | -0.023 | 0.777 | 0.004 | — |
| BA-2Motifs | GINE | PGExplainer | scaffold | 200 | 0.881 | 0.095 | -0.471 | 0.424 | 0.003 | 0.011 | 0.763 | 0.007 | — |
| BA-2Motifs | GINE | Saliency | random | 200 | 0.928 | -0.260 | 0.796 | 0.127 | -0.012 | -0.016 | 0.790 | 0.012 | — |
| BA-2Motifs | GINE | Saliency | scaffold | 200 | 0.963 | 0.516 | 0.754 | 0.127 | 0.007 | 0.007 | 0.800 | 0.016 | — |
| BACE | GCN | IntegratedGradients | random | 200 | — | 0.532 | 0.849 | 0.756 | 0.576 | 0.596 | 0.785 | 0.291 | 0.594 |
| BACE | GCN | IntegratedGradients | scaffold | 200 | — | -0.683 | 0.904 | 0.778 | -0.114 | -0.114 | 0.783 | 0.069 | 0.263 |
| BACE | GINE | IntegratedGradients | random | 200 | — | -0.203 | 0.691 | 0.751 | 0.103 | 0.115 | 0.787 | 0.126 | 0.323 |
| BACE | GINE | IntegratedGradients | scaffold | 200 | — | 0.502 | 0.894 | 0.818 | 0.005 | 0.011 | 0.786 | 0.010 | 0.000 |
| BBBP | AttentiveFP | IntegratedGradients | random | 200 | — | 0.230 | 0.853 | 0.732 | 0.068 | 0.069 | 0.759 | 0.200 | 0.104 |
| BBBP | AttentiveFP | IntegratedGradients | scaffold | 200 | — | -0.031 | 0.854 | 0.721 | -0.020 | 0.021 | 0.772 | 0.070 | 0.085 |
| BBBP | GAT | IntegratedGradients | random | 200 | — | 0.029 | 0.876 | 0.748 | 0.158 | 0.159 | 0.767 | 0.193 | 0.291 |
| BBBP | GAT | IntegratedGradients | scaffold | 200 | — | -0.826 | 0.907 | 0.728 | -0.095 | -0.105 | 0.773 | 0.011 | 0.061 |
| BBBP | GCN | IntegratedGradients | random | 200 | — | -0.376 | 0.842 | 0.794 | 0.008 | 0.003 | 0.765 | 0.092 | 0.195 |
| BBBP | GCN | IntegratedGradients | scaffold | 200 | — | -0.731 | 0.840 | 0.751 | -0.113 | -0.211 | 0.775 | 0.013 | 0.200 |
| BBBP | GINE | GNNExplainer | random | 200 | — | 0.179 | 0.955 | 0.789 | 0.218 | 0.234 | 0.779 | 0.241 | 0.164 |
| BBBP | GINE | GNNExplainer | scaffold | 200 | — | -0.355 | 0.978 | 0.802 | 0.004 | -0.060 | 0.781 | 0.064 | 0.175 |
| BBBP | GINE | IntegratedGradients | random | 200 | — | 0.226 | 0.890 | 0.764 | 0.191 | 0.246 | 0.772 | 0.206 | 0.314 |
| BBBP | GINE | IntegratedGradients | scaffold | 200 | — | -0.562 | 0.935 | 0.755 | -0.039 | -0.058 | 0.776 | 0.074 | 0.110 |
| BBBP | GINE | PGExplainer | random | 200 | — | -0.085 | 0.370 | 0.879 | 0.114 | 0.229 | 0.690 | 0.159 | — |
| BBBP | GINE | PGExplainer | scaffold | 200 | — | -0.298 | 0.682 | 0.821 | -0.042 | -0.051 | 0.593 | 0.080 | — |
| BBBP | MPNN | IntegratedGradients | random | 200 | — | -0.125 | 0.860 | 0.774 | 0.089 | 0.147 | 0.769 | 0.113 | 0.142 |
| BBBP | MPNN | IntegratedGradients | scaffold | 200 | — | -0.543 | 0.714 | 0.809 | -0.038 | -0.055 | 0.778 | 0.021 | 0.084 |
| ClinTox | GINE | GNNExplainer | random | 200 | — | -0.018 | 0.975 | 0.612 | 0.194 | 0.152 | 0.831 | 0.129 | 0.340 |
| ClinTox | GINE | GNNExplainer | scaffold | 200 | — | -0.228 | 0.988 | 0.686 | 0.205 | 0.205 | 0.783 | 0.151 | 0.294 |
| ClinTox | GINE | IntegratedGradients | random | 200 | — | -0.224 | 0.911 | 0.794 | 0.152 | 0.152 | 0.775 | 0.129 | 0.205 |
| ClinTox | GINE | IntegratedGradients | scaffold | 200 | — | -0.251 | 0.980 | 0.686 | 0.205 | 0.205 | 0.780 | 0.151 | 0.144 |
| DILI | GINE | IntegratedGradients | random | 142 | — | 0.105 | 0.813 | 0.774 | 0.149 | 0.164 | 0.775 | 0.220 | 0.287 |
| DILI | GINE | IntegratedGradients | scaffold | 142 | — | -0.039 | 0.885 | 0.779 | 0.243 | 0.257 | 0.777 | 0.138 | 0.342 |
| ESOL | GAT | IntegratedGradients | random | 200 | — | 0.841 | 0.947 | 0.842 | 3.505 | 7.619 | 0.734 | — | — |
| ESOL | GAT | IntegratedGradients | scaffold | 200 | — | 0.902 | 0.965 | 0.798 | 4.788 | 14.204 | 0.730 | — | — |
| ESOL | GCN | IntegratedGradients | random | 200 | — | 0.251 | 0.965 | 0.859 | -0.716 | -0.758 | 0.731 | — | — |
| ESOL | GCN | IntegratedGradients | scaffold | 200 | — | 0.640 | 0.967 | 0.829 | -1.051 | -1.432 | 0.730 | — | — |
| ESOL | GINE | GNNExplainer | random | 200 | — | 0.373 | 0.958 | 0.862 | -1.316 | -1.758 | 0.757 | — | — |
| ESOL | GINE | GNNExplainer | scaffold | 200 | — | 0.525 | 0.927 | 0.825 | -1.054 | -1.408 | 0.758 | — | — |
| ESOL | GINE | IntegratedGradients | random | 200 | — | 0.432 | 0.932 | 0.870 | -1.490 | -1.686 | 0.739 | — | — |
| ESOL | GINE | IntegratedGradients | scaffold | 200 | — | 0.571 | 0.757 | 0.827 | -1.218 | -1.265 | 0.742 | — | — |
| FreeSolv | GINE | IntegratedGradients | random | 193 | — | 0.276 | 0.862 | 0.857 | -0.715 | -0.788 | 0.717 | — | — |
| FreeSolv | GINE | IntegratedGradients | scaffold | 193 | — | 0.779 | 0.632 | 0.847 | -1.020 | -1.561 | 0.731 | — | — |
| Lipophilicity | GINE | IntegratedGradients | random | 200 | — | 0.546 | 0.749 | 0.790 | -0.636 | -1.248 | 0.781 | — | — |
| Lipophilicity | GINE | IntegratedGradients | scaffold | 200 | — | 0.542 | 0.772 | 0.769 | -0.716 | -1.411 | 0.781 | — | — |
| MUTAG | AttentiveFP | IntegratedGradients | random | 58 | 0.039 | -0.871 | 0.822 | 0.958 | -0.007 | -0.022 | 0.772 | 0.000 | 0.000 |
| MUTAG | AttentiveFP | IntegratedGradients | scaffold | 53 | 0.044 | -0.778 | 0.950 | 0.993 | -0.011 | -0.023 | 0.771 | 0.000 | 0.002 |
| MUTAG | GAT | IntegratedGradients | random | 58 | 0.461 | 0.698 | 0.951 | 0.925 | 0.281 | 0.511 | 0.775 | 0.289 | 0.169 |
| MUTAG | GAT | IntegratedGradients | scaffold | 53 | 0.222 | 0.867 | 0.953 | 0.987 | 0.019 | 0.076 | 0.772 | 0.041 | 0.000 |
| MUTAG | GCN | IntegratedGradients | random | 58 | 0.551 | 0.610 | 0.911 | 0.932 | 0.435 | 0.518 | 0.764 | 0.320 | 0.290 |
| MUTAG | GCN | IntegratedGradients | scaffold | 53 | 0.174 | 0.911 | 0.863 | 0.987 | 0.002 | 0.004 | 0.771 | 0.005 | 0.000 |
| MUTAG | GINE | GNNExplainer | random | 58 | 0.858 | -0.170 | 0.848 | 0.929 | 0.310 | 0.175 | 0.777 | 0.338 | 0.703 |
| MUTAG | GINE | GNNExplainer | scaffold | 53 | 0.534 | 0.369 | 0.907 | 0.984 | 0.068 | 0.305 | 0.774 | 0.148 | 0.496 |
| MUTAG | GINE | GuidedBackprop | random | 58 | 0.037 | -0.089 | 0.882 | 0.962 | 0.540 | 0.615 | 0.773 | 0.178 | 0.628 |
| MUTAG | GINE | GuidedBackprop | scaffold | 53 | 0.146 | 0.551 | 0.973 | 0.985 | 0.210 | 0.242 | 0.772 | 0.297 | 0.494 |
| MUTAG | GINE | InputXGradient | random | 58 | 0.013 | -0.200 | 0.770 | 0.984 | 0.491 | 0.605 | 0.772 | 0.160 | 0.501 |
| MUTAG | GINE | InputXGradient | scaffold | 53 | 0.048 | 0.534 | 0.969 | 0.995 | 0.199 | 0.246 | 0.772 | 0.296 | 0.487 |
| MUTAG | GINE | IntegratedGradients | random | 58 | 0.496 | -0.196 | 0.724 | 0.915 | 0.551 | 0.433 | 0.772 | 0.347 | 0.706 |
| MUTAG | GINE | IntegratedGradients | scaffold | 53 | 0.528 | 0.562 | 0.912 | 0.975 | 0.215 | 0.253 | 0.772 | 0.290 | 0.482 |
| MUTAG | GINE | PGExplainer | random | 58 | 0.251 | -0.351 | 0.713 | 0.983 | 0.379 | 0.430 | 0.647 | 0.225 | — |
| MUTAG | GINE | PGExplainer | scaffold | 53 | 0.981 | 0.214 | 0.940 | 0.986 | 0.097 | 0.238 | 0.641 | 0.133 | — |
| MUTAG | GINE | Saliency | random | 58 | 0.002 | -0.195 | 0.767 | 0.975 | 0.494 | 0.610 | 0.772 | 0.163 | 0.516 |
| MUTAG | GINE | Saliency | scaffold | 53 | 0.014 | 0.532 | 0.932 | 0.996 | 0.198 | 0.246 | 0.772 | 0.296 | 0.498 |
| MUTAG | GINE | SubgraphX | random | 58 | 0.348 | -0.154 | — | 0.996 | 0.342 | -0.000 | 0.160 | 0.450 | — |
| MUTAG | GINE | SubgraphX | scaffold | 53 | 0.452 | 0.540 | — | 1.000 | 0.216 | 0.193 | 0.592 | 0.316 | — |
| MUTAG | MPNN | IntegratedGradients | random | 58 | 0.127 | 0.532 | 0.890 | 0.959 | 0.623 | 0.635 | 0.771 | 0.188 | 0.419 |
| MUTAG | MPNN | IntegratedGradients | scaffold | 53 | 0.124 | 0.327 | 0.895 | 0.991 | 0.005 | 0.010 | 0.770 | 0.013 | 0.001 |
| MolMotif | AttentiveFP | IntegratedGradients | random | 200 | 0.986 | 0.486 | 0.912 | 0.792 | 0.522 | 0.017 | 0.770 | 0.520 | 0.339 |
| MolMotif | AttentiveFP | IntegratedGradients | scaffold | 200 | 0.995 | 0.521 | 0.958 | 0.797 | 0.503 | 0.019 | 0.775 | 0.504 | 0.425 |
| MolMotif | GAT | IntegratedGradients | random | 200 | 0.733 | 0.040 | 0.901 | 0.716 | 0.491 | 0.240 | 0.772 | 0.515 | 0.220 |
| MolMotif | GAT | IntegratedGradients | scaffold | 200 | 0.873 | 0.156 | 0.956 | 0.722 | 0.653 | 0.406 | 0.775 | 0.521 | 0.080 |
| MolMotif | GCN | IntegratedGradients | random | 200 | 0.850 | -0.013 | 1.000 | 0.811 | 0.414 | 0.420 | 0.768 | 0.037 | 0.375 |
| MolMotif | GCN | IntegratedGradients | scaffold | 200 | 0.893 | 0.178 | 0.962 | 0.837 | 0.300 | 0.446 | 0.772 | 0.031 | 0.429 |
| MolMotif | GINE | GNNExplainer | random | 200 | 0.630 | 0.030 | 0.973 | 0.835 | -0.018 | 0.387 | 0.778 | 0.025 | 0.089 |
| MolMotif | GINE | GNNExplainer | scaffold | 200 | 0.610 | -0.049 | 0.958 | 0.814 | -0.021 | 0.259 | 0.780 | 0.068 | 0.138 |
| MolMotif | GINE | GuidedBackprop | random | 200 | 0.998 | -0.144 | 0.884 | 0.823 | 0.330 | 0.318 | 0.770 | 0.153 | 0.489 |
| MolMotif | GINE | GuidedBackprop | scaffold | 200 | 0.882 | -0.270 | 0.837 | 0.814 | 0.214 | 0.191 | 0.774 | 0.255 | 0.339 |
| MolMotif | GINE | InputXGradient | random | 200 | 0.999 | -0.112 | 0.848 | 0.810 | 0.312 | 0.322 | 0.768 | 0.144 | 0.490 |
| MolMotif | GINE | InputXGradient | scaffold | 200 | 0.999 | -0.255 | 0.859 | 0.758 | 0.205 | 0.170 | 0.774 | 0.234 | 0.399 |
| MolMotif | GINE | IntegratedGradients | random | 200 | 0.972 | 0.007 | 0.970 | 0.860 | 0.311 | 0.319 | 0.768 | 0.153 | 0.476 |
| MolMotif | GINE | IntegratedGradients | scaffold | 200 | 0.984 | -0.091 | 0.898 | 0.815 | 0.270 | 0.099 | 0.773 | 0.304 | 0.269 |
| MolMotif | GINE | PGExplainer | random | 200 | 0.584 | 0.001 | 0.639 | 0.897 | 0.143 | 0.381 | 0.702 | 0.091 | — |
| MolMotif | GINE | PGExplainer | scaffold | 200 | 0.240 | -0.031 | 0.464 | 0.911 | 0.125 | 0.236 | 0.774 | 0.153 | — |
| MolMotif | GINE | Saliency | random | 200 | 0.994 | -0.117 | 0.837 | 0.802 | 0.318 | 0.317 | 0.772 | 0.150 | 0.506 |
| MolMotif | GINE | Saliency | scaffold | 200 | 0.998 | -0.269 | 0.845 | 0.751 | 0.220 | 0.179 | 0.775 | 0.250 | 0.400 |
| MolMotif | GINE | SubgraphX | random | 200 | 0.556 | -0.013 | — | 0.977 | 0.159 | 0.320 | 0.390 | 0.165 | — |
| MolMotif | GINE | SubgraphX | scaffold | 200 | 0.513 | -0.084 | — | 0.969 | 0.147 | 0.182 | 0.406 | 0.217 | — |
| MolMotif | MPNN | IntegratedGradients | random | 200 | 0.962 | -0.057 | 0.946 | 0.860 | 0.451 | 0.457 | 0.772 | 0.030 | 0.121 |
| MolMotif | MPNN | IntegratedGradients | scaffold | 200 | 0.940 | -0.019 | 0.952 | 0.865 | 0.341 | 0.423 | 0.777 | 0.043 | 0.084 |
| SIDER | GCN | IntegratedGradients | random | 200 | — | -0.110 | 0.750 | 0.746 | 0.084 | 0.022 | 0.751 | 0.154 | 0.054 |
| SIDER | GCN | IntegratedGradients | scaffold | 200 | — | -0.137 | 0.745 | 0.704 | 0.003 | 0.021 | 0.770 | 0.109 | 0.018 |
| SIDER | GINE | IntegratedGradients | random | 200 | — | 0.427 | 0.869 | 0.764 | 0.333 | 0.389 | 0.754 | 0.243 | 0.449 |
| SIDER | GINE | IntegratedGradients | scaffold | 200 | — | -0.032 | 0.638 | 0.707 | 0.084 | 0.098 | 0.772 | 0.188 | 0.455 |
| ShapeGGen | GINE | GNNExplainer | random | 50 | 0.483 | 0.154 | 0.563 | 0.069 | 0.003 | 0.008 | 0.776 | 0.007 | 0.001 |
| ShapeGGen | GINE | GuidedBackprop | random | 50 | 0.791 | 0.465 | 0.796 | 0.160 | 0.008 | 0.003 | 0.776 | 0.016 | 0.001 |
| ShapeGGen | GINE | InputXGradient | random | 50 | 0.732 | 0.473 | 0.744 | 0.174 | 0.008 | 0.003 | 0.776 | 0.016 | 0.001 |
| ShapeGGen | GINE | IntegratedGradients | random | 50 | 0.751 | 0.497 | 0.763 | 0.172 | 0.008 | 0.003 | 0.776 | 0.016 | 0.001 |
| ShapeGGen | GINE | PGExplainer | random | 50 | 0.489 | -0.167 | 0.676 | 0.429 | 0.002 | 0.009 | 0.698 | 0.005 | — |
| ShapeGGen | GINE | Saliency | random | 50 | 0.769 | 0.425 | 0.730 | 0.159 | 0.007 | 0.003 | 0.776 | 0.015 | 0.001 |
| ShapeGGen | GINE | SubgraphX | random | 50 | 0.620 | 0.471 | 0.233 | 0.180 | 0.011 | -0.000 | 0.567 | 0.021 | — |
| SynthMotifs | AttentiveFP | IntegratedGradients | random | 200 | 0.898 | 0.104 | 0.726 | 0.146 | 0.369 | 0.204 | 0.796 | 0.289 | 0.446 |
| SynthMotifs | AttentiveFP | IntegratedGradients | scaffold | 200 | 0.957 | 0.312 | 0.743 | 0.146 | 0.487 | 0.082 | 0.795 | 0.542 | 0.565 |
| SynthMotifs | GAT | IntegratedGradients | random | 200 | 0.642 | 0.230 | 0.384 | 0.119 | 0.315 | 0.319 | 0.792 | 0.093 | 0.434 |
| SynthMotifs | GAT | IntegratedGradients | scaffold | 200 | 0.910 | 0.368 | 0.901 | 0.107 | 0.497 | 0.248 | 0.793 | 0.580 | 0.477 |
| SynthMotifs | GCN | IntegratedGradients | random | 200 | 0.990 | 0.433 | 0.694 | 0.169 | 0.443 | 0.062 | 0.798 | 0.590 | 0.488 |
| SynthMotifs | GCN | IntegratedGradients | scaffold | 200 | 0.936 | 0.366 | 0.706 | 0.141 | 0.240 | 0.166 | 0.796 | 0.322 | 0.247 |
| SynthMotifs | GINE | GNNExplainer | random | 200 | 0.698 | 0.199 | 0.698 | 0.048 | 0.217 | 0.251 | 0.800 | 0.310 | 0.155 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 200 | 0.796 | 0.206 | 0.593 | 0.051 | 0.331 | 0.322 | 0.800 | 0.388 | 0.426 |
| SynthMotifs | GINE | GuidedBackprop | random | 200 | 0.996 | 0.613 | 0.795 | 0.164 | 0.261 | 0.059 | 0.800 | 0.393 | 0.210 |
| SynthMotifs | GINE | GuidedBackprop | scaffold | 200 | 0.982 | 0.628 | 0.775 | 0.143 | 0.345 | 0.033 | 0.800 | 0.473 | 0.449 |
| SynthMotifs | GINE | InputXGradient | random | 200 | 0.959 | 0.498 | 0.656 | 0.238 | 0.261 | 0.132 | 0.795 | 0.379 | 0.203 |
| SynthMotifs | GINE | InputXGradient | scaffold | 200 | 0.982 | 0.456 | 0.723 | 0.180 | 0.338 | 0.122 | 0.797 | 0.437 | 0.462 |
| SynthMotifs | GINE | IntegratedGradients | random | 200 | 0.977 | 0.479 | 0.849 | 0.162 | 0.256 | 0.129 | 0.799 | 0.379 | 0.200 |
| SynthMotifs | GINE | IntegratedGradients | scaffold | 200 | 0.978 | 0.517 | 0.651 | 0.163 | 0.353 | 0.051 | 0.798 | 0.485 | 0.450 |
| SynthMotifs | GINE | PGExplainer | random | 200 | 0.314 | -0.149 | 0.427 | 0.385 | 0.010 | 0.263 | 0.786 | 0.035 | — |
| SynthMotifs | GINE | PGExplainer | scaffold | 200 | 0.323 | -0.158 | 0.563 | 0.377 | 0.058 | 0.280 | 0.656 | 0.103 | — |
| SynthMotifs | GINE | Saliency | random | 200 | 0.960 | 0.513 | 0.560 | 0.176 | 0.262 | 0.141 | 0.796 | 0.380 | 0.208 |
| SynthMotifs | GINE | Saliency | scaffold | 200 | 0.983 | 0.432 | 0.605 | 0.150 | 0.332 | 0.096 | 0.794 | 0.437 | 0.445 |
| SynthMotifs | GINE | SubgraphX | random | 200 | 0.845 | 0.551 | 0.744 | 0.159 | 0.234 | 0.044 | 0.659 | 0.359 | — |
| SynthMotifs | GINE | SubgraphX | scaffold | 200 | 0.841 | 0.500 | 0.383 | 0.182 | 0.353 | 0.056 | 0.436 | 0.490 | — |
| SynthMotifs | MPNN | IntegratedGradients | random | 200 | 0.903 | 0.399 | 0.590 | 0.090 | 0.468 | 0.485 | 0.796 | 0.244 | 0.453 |
| SynthMotifs | MPNN | IntegratedGradients | scaffold | 200 | 0.913 | 0.267 | 0.663 | 0.137 | 0.421 | 0.266 | 0.793 | 0.491 | 0.587 |
| Tox21 | GINE | IntegratedGradients | random | 200 | — | -0.063 | 0.710 | 0.725 | -0.096 | -0.060 | 0.753 | 0.037 | 0.309 |
| Tox21 | GINE | IntegratedGradients | scaffold | 200 | — | -0.088 | 0.950 | 0.750 | 0.118 | 0.137 | 0.761 | 0.138 | 0.449 |
| hERG | GINE | IntegratedGradients | random | 197 | — | 0.776 | 0.953 | 0.773 | 0.765 | 0.765 | 0.779 | 0.188 | 0.809 |
| hERG | GINE | IntegratedGradients | scaffold | 197 | — | -0.130 | 0.679 | 0.730 | -0.000 | 0.000 | 0.776 | 0.000 | 0.000 |

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
| GNNExplainer | GuidedBackprop | 200 | -0.595 | 0.000 |
| GNNExplainer | InputXGradient | 200 | -0.604 | 0.000 |
| GNNExplainer | IntegratedGradients | 200 | -0.625 | 0.000 |
| GNNExplainer | PGExplainer | 200 | -0.088 | 0.000 |
| GNNExplainer | Saliency | 200 | -0.604 | 0.000 |
| GuidedBackprop | InputXGradient | 200 | -0.008 | 0.162 |
| GuidedBackprop | IntegratedGradients | 200 | -0.019 | 0.000 |
| GuidedBackprop | PGExplainer | 200 | 0.518 | 0.000 |
| GuidedBackprop | Saliency | 200 | -0.008 | 0.162 |
| InputXGradient | IntegratedGradients | 200 | -0.008 | 0.398 |
| InputXGradient | PGExplainer | 200 | 0.525 | 0.000 |
| InputXGradient | Saliency | 200 | 0.000 | 0.655 |
| IntegratedGradients | PGExplainer | 200 | 0.545 | 0.000 |
| IntegratedGradients | Saliency | 200 | 0.008 | 0.398 |
| PGExplainer | Saliency | 200 | -0.525 | 0.000 |

**BBBP · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 189 | 0.000 | 0.450 |
| GNNExplainer | PGExplainer | 178 | 0.135 | 0.000 |
| IntegratedGradients | PGExplainer | 178 | 0.122 | 0.000 |

**BBBP · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 197 | 0.171 | 0.000 |
| GNNExplainer | PGExplainer | 175 | -0.031 | 0.183 |
| IntegratedGradients | PGExplainer | 175 | -0.250 | 0.000 |

**ClinTox · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 139 | 0.000 | 0.205 |

**ClinTox · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 197 | 0.000 | 0.029 |

**ESOL · GINE · random split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 156 | 0.000 | 0.001 |

**ESOL · GINE · scaffold split** (metric: occ_spearman)

| method A | method B | n | median Δ(A−B) | p-value |
| --- | --- | --- | --- | --- |
| GNNExplainer | IntegratedGradients | 157 | 0.000 | 0.010 |

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
| GNNExplainer | GuidedBackprop | 53 | -0.171 | 0.000 |
| GNNExplainer | InputXGradient | 53 | -0.171 | 0.000 |
| GNNExplainer | IntegratedGradients | 53 | -0.200 | 0.000 |
| GNNExplainer | PGExplainer | 53 | 0.149 | 0.000 |
| GNNExplainer | Saliency | 53 | -0.171 | 0.000 |
| GNNExplainer | SubgraphX | 53 | -0.154 | 0.000 |
| GuidedBackprop | InputXGradient | 53 | 0.000 | 0.060 |
| GuidedBackprop | IntegratedGradients | 53 | 0.000 | 0.087 |
| GuidedBackprop | PGExplainer | 53 | 0.352 | 0.000 |
| GuidedBackprop | Saliency | 53 | 0.000 | 0.024 |
| GuidedBackprop | SubgraphX | 53 | 0.014 | 0.933 |
| InputXGradient | IntegratedGradients | 53 | 0.000 | 0.003 |
| InputXGradient | PGExplainer | 53 | 0.375 | 0.000 |
| InputXGradient | Saliency | 53 | 0.000 | 0.465 |
| InputXGradient | SubgraphX | 53 | 0.000 | 0.670 |
| IntegratedGradients | PGExplainer | 53 | 0.388 | 0.000 |
| IntegratedGradients | Saliency | 53 | 0.000 | 0.001 |
| IntegratedGradients | SubgraphX | 53 | 0.014 | 0.531 |
| PGExplainer | Saliency | 53 | -0.345 | 0.000 |
| PGExplainer | SubgraphX | 53 | -0.300 | 0.000 |
| Saliency | SubgraphX | 53 | 0.000 | 0.547 |

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
| GNNExplainer | GuidedBackprop | 199 | 0.159 | 0.000 |
| GNNExplainer | InputXGradient | 199 | 0.107 | 0.000 |
| GNNExplainer | IntegratedGradients | 199 | 0.000 | 0.011 |
| GNNExplainer | PGExplainer | 197 | -0.057 | 0.442 |
| GNNExplainer | Saliency | 199 | 0.119 | 0.000 |
| GNNExplainer | SubgraphX | 196 | 0.035 | 0.185 |
| GuidedBackprop | InputXGradient | 199 | 0.000 | 0.380 |
| GuidedBackprop | IntegratedGradients | 199 | -0.034 | 0.000 |
| GuidedBackprop | PGExplainer | 197 | -0.286 | 0.000 |
| GuidedBackprop | Saliency | 199 | 0.000 | 0.498 |
| GuidedBackprop | SubgraphX | 196 | -0.094 | 0.000 |
| InputXGradient | IntegratedGradients | 199 | 0.000 | 0.000 |
| InputXGradient | PGExplainer | 197 | -0.200 | 0.000 |
| InputXGradient | Saliency | 199 | 0.000 | 0.253 |
| InputXGradient | SubgraphX | 196 | -0.035 | 0.001 |
| IntegratedGradients | PGExplainer | 197 | -0.176 | 0.162 |
| IntegratedGradients | Saliency | 199 | 0.000 | 0.000 |
| IntegratedGradients | SubgraphX | 196 | 0.004 | 0.972 |
| PGExplainer | Saliency | 197 | 0.200 | 0.000 |
| PGExplainer | SubgraphX | 195 | 0.096 | 0.109 |
| Saliency | SubgraphX | 196 | -0.059 | 0.001 |

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
| GNNExplainer | GuidedBackprop | 200 | -0.421 | 0.000 |
| GNNExplainer | InputXGradient | 200 | -0.236 | 0.000 |
| GNNExplainer | IntegratedGradients | 200 | -0.330 | 0.000 |
| GNNExplainer | PGExplainer | 198 | 0.426 | 0.000 |
| GNNExplainer | Saliency | 200 | -0.215 | 0.000 |
| GNNExplainer | SubgraphX | 200 | -0.342 | 0.000 |
| GuidedBackprop | InputXGradient | 200 | 0.131 | 0.000 |
| GuidedBackprop | IntegratedGradients | 200 | 0.122 | 0.000 |
| GuidedBackprop | PGExplainer | 198 | 0.901 | 0.000 |
| GuidedBackprop | Saliency | 200 | 0.164 | 0.000 |
| GuidedBackprop | SubgraphX | 200 | 0.180 | 0.000 |
| InputXGradient | IntegratedGradients | 200 | 0.060 | 0.024 |
| InputXGradient | PGExplainer | 198 | 0.769 | 0.000 |
| InputXGradient | Saliency | 200 | 0.019 | 0.000 |
| InputXGradient | SubgraphX | 200 | 0.076 | 0.241 |
| IntegratedGradients | PGExplainer | 198 | 0.683 | 0.000 |
| IntegratedGradients | Saliency | 200 | 0.030 | 0.002 |
| IntegratedGradients | SubgraphX | 200 | -0.019 | 0.791 |
| PGExplainer | Saliency | 198 | -0.767 | 0.000 |
| PGExplainer | SubgraphX | 198 | -0.704 | 0.000 |
| Saliency | SubgraphX | 200 | 0.030 | 0.064 |

