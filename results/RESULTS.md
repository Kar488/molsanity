# RESULTS.md — validated numbers only

> Every number here is computed by code in this run and traceable to a
> logged artifact under `artifacts/`. No placeholders. See `LIMITATIONS.md`
> for caveats (notably: MUTAG ground truth is a chemically motivated
> nitro-motif *proxy*, not annotator labels).

## Classification audit matrix (dataset × backbone × attributor)

| dataset | backbone | attributor | split | n_mol | acc | auc | gt_auroc | gt_auprc | motif_top1 | occ_spearman | occ_top1 | fid+ | fid- | sparsity | ece |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BACE | GCN | IntegratedGradients | random | 100 | 0.640 | 0.839 | — | — | 0.792 | 0.034 | 0.530 | 0.181 | 0.218 | 0.785 | 0.082 |
| BACE | GCN | IntegratedGradients | scaffold | 100 | 0.850 | 0.507 | — | — | 0.800 | -0.668 | 0.140 | -0.125 | -0.125 | 0.785 | 0.069 |
| BACE | GINE | GNNExplainer | scaffold | 30 | 0.433 | 0.434 | — | — | 0.835 | -0.128 | 0.167 | 0.064 | 0.214 | 0.786 | 0.189 |
| BACE | GINE | InputXGradient | scaffold | 30 | 0.433 | 0.434 | — | — | 0.841 | -0.159 | 0.167 | 0.079 | 0.171 | 0.783 | 0.189 |
| BACE | GINE | IntegratedGradients | random | 100 | 0.730 | 0.846 | — | — | 0.844 | 0.307 | 0.640 | 0.347 | 0.278 | 0.786 | 0.055 |
| BACE | GINE | IntegratedGradients | scaffold | 100 | 0.340 | 0.651 | — | — | 0.843 | 0.389 | 0.810 | 0.104 | 0.092 | 0.783 | 0.179 |
| BACE | GINE | Saliency | scaffold | 30 | 0.433 | 0.434 | — | — | 0.873 | -0.174 | 0.167 | 0.097 | 0.173 | 0.785 | 0.189 |
| BBBP | AttentiveFP | IntegratedGradients | random | 100 | 0.770 | 0.855 | — | — | 0.750 | 0.339 | 0.470 | 0.164 | 0.167 | 0.774 | 0.050 |
| BBBP | AttentiveFP | IntegratedGradients | scaffold | 100 | 0.950 | 0.961 | — | — | 0.841 | 0.284 | 0.250 | 0.036 | 0.015 | 0.776 | 0.033 |
| BBBP | GAT | IntegratedGradients | random | 100 | 0.780 | 0.885 | — | — | 0.770 | 0.043 | 0.510 | 0.328 | 0.328 | 0.780 | 0.051 |
| BBBP | GAT | IntegratedGradients | scaffold | 100 | 0.980 | 0.805 | — | — | 0.831 | -0.712 | 0.000 | -0.021 | -0.050 | 0.772 | 0.010 |
| BBBP | GCN | IntegratedGradients | random | 100 | 0.790 | 0.873 | — | — | 0.768 | 0.023 | 0.510 | 0.311 | 0.318 | 0.774 | 0.074 |
| BBBP | GCN | IntegratedGradients | scaffold | 100 | 0.980 | 0.966 | — | — | 0.814 | -0.812 | 0.030 | -0.010 | -0.145 | 0.772 | 0.013 |
| BBBP | GINE | GNNExplainer | random | 100 | 0.820 | 0.886 | — | — | 0.779 | -0.061 | 0.440 | 0.287 | 0.333 | 0.781 | 0.053 |
| BBBP | GINE | GNNExplainer | scaffold | 100 | 0.950 | 0.932 | — | — | 0.848 | -0.368 | 0.060 | 0.018 | -0.064 | 0.779 | 0.029 |
| BBBP | GINE | GuidedBackprop | scaffold | 30 | 0.967 | 0.805 | — | — | 0.876 | -0.530 | 0.000 | -0.016 | -0.037 | 0.775 | 0.059 |
| BBBP | GINE | InputXGradient | scaffold | 30 | 0.967 | 0.805 | — | — | 0.839 | -0.620 | 0.000 | -0.016 | -0.047 | 0.769 | 0.059 |
| BBBP | GINE | IntegratedGradients | random | 100 | 0.820 | 0.886 | — | — | 0.724 | 0.016 | 0.470 | 0.332 | 0.334 | 0.776 | 0.053 |
| BBBP | GINE | IntegratedGradients | scaffold | 100 | 0.950 | 0.932 | — | — | 0.841 | -0.741 | 0.040 | -0.031 | -0.057 | 0.774 | 0.029 |
| BBBP | GINE | PGExplainer | scaffold | 30 | 0.967 | 0.805 | — | — | 0.422 | -0.185 | 0.367 | -0.055 | -0.059 | 0.635 | 0.059 |
| BBBP | GINE | Saliency | scaffold | 30 | 0.967 | 0.805 | — | — | 0.826 | -0.627 | 0.000 | -0.029 | -0.033 | 0.773 | 0.059 |
| BBBP | MPNN | IntegratedGradients | random | 100 | 0.840 | 0.914 | — | — | 0.792 | 0.154 | 0.420 | 0.210 | 0.267 | 0.774 | 0.053 |
| BBBP | MPNN | IntegratedGradients | scaffold | 100 | 0.950 | 0.922 | — | — | 0.824 | -0.431 | 0.040 | 0.052 | -0.043 | 0.775 | 0.033 |
| ClinTox | GINE | GNNExplainer | random | 100 | 0.710 | 0.910 | — | — | 0.504 | 0.059 | 0.430 | 0.258 | 0.230 | 0.855 | 0.157 |
| ClinTox | GINE | GNNExplainer | scaffold | 100 | 0.800 | 0.845 | — | — | 0.728 | -0.242 | 0.390 | 0.139 | 0.135 | 0.785 | 0.062 |
| ClinTox | GINE | InputXGradient | scaffold | 30 | 0.567 | 0.820 | — | — | 0.793 | 0.139 | 0.567 | 0.356 | 0.356 | 0.749 | 0.207 |
| ClinTox | GINE | IntegratedGradients | random | 100 | 0.710 | 0.910 | — | — | 0.754 | -0.223 | 0.410 | 0.230 | 0.230 | 0.778 | 0.157 |
| ClinTox | GINE | IntegratedGradients | scaffold | 100 | 0.800 | 0.845 | — | — | 0.745 | -0.329 | 0.380 | 0.135 | 0.135 | 0.772 | 0.062 |
| ClinTox | GINE | Saliency | scaffold | 30 | 0.567 | 0.820 | — | — | 0.790 | 0.145 | 0.567 | 0.356 | 0.356 | 0.749 | 0.207 |
| DILI | GINE | GNNExplainer | scaffold | 30 | 0.800 | 0.824 | — | — | 0.826 | -0.044 | 0.433 | 0.080 | 0.154 | 0.782 | 0.141 |
| DILI | GINE | InputXGradient | scaffold | 30 | 0.800 | 0.824 | — | — | 0.858 | -0.126 | 0.433 | 0.075 | 0.122 | 0.780 | 0.141 |
| DILI | GINE | IntegratedGradients | random | 48 | 0.688 | 0.719 | — | — | 0.760 | 0.298 | 0.500 | 0.354 | 0.360 | 0.778 | 0.135 |
| DILI | GINE | IntegratedGradients | scaffold | 48 | 0.688 | 0.824 | — | — | 0.852 | 0.346 | 0.521 | 0.194 | 0.229 | 0.774 | 0.120 |
| DILI | GINE | Saliency | scaffold | 30 | 0.800 | 0.824 | — | — | 0.851 | -0.128 | 0.433 | 0.056 | 0.134 | 0.782 | 0.141 |
| MUTAG | AttentiveFP | IntegratedGradients | scaffold | 20 | 0.650 | 0.967 | 0.132 | 0.150 | 0.993 | -0.880 | 0.000 | 0.002 | 0.012 | 0.771 | 0.235 |
| MUTAG | GAT | IntegratedGradients | scaffold | 20 | 0.750 | 0.890 | 0.130 | 0.151 | 0.992 | 0.268 | 0.600 | 0.189 | 0.247 | 0.771 | 0.155 |
| MUTAG | GCN | IntegratedGradients | scaffold | 20 | 0.750 | 0.912 | 0.203 | 0.222 | 0.989 | 0.175 | 0.600 | 0.123 | 0.228 | 0.767 | 0.138 |
| MUTAG | GINE | GNNExplainer | scaffold | 20 | 0.800 | 0.857 | 0.491 | 0.347 | 0.987 | 0.279 | 0.350 | 0.113 | 0.278 | 0.771 | 0.117 |
| MUTAG | GINE | GuidedBackprop | scaffold | 20 | 0.800 | 0.857 | 0.112 | 0.144 | 0.990 | 0.341 | 0.350 | 0.272 | 0.229 | 0.771 | 0.117 |
| MUTAG | GINE | InputXGradient | scaffold | 20 | 0.800 | 0.857 | 0.042 | 0.134 | 0.998 | 0.398 | 0.350 | 0.251 | 0.225 | 0.771 | 0.117 |
| MUTAG | GINE | IntegratedGradients | random | 20 | 0.700 | 0.781 | 0.075 | 0.183 | 0.967 | 0.587 | 0.800 | 0.211 | 0.200 | 0.776 | 0.271 |
| MUTAG | GINE | IntegratedGradients | scaffold | 20 | 0.800 | 0.857 | 0.540 | 0.405 | 0.979 | 0.414 | 0.350 | 0.252 | 0.245 | 0.771 | 0.117 |
| MUTAG | GINE | PGExplainer | scaffold | 20 | 0.800 | 0.857 | 0.401 | 0.211 | 1.000 | 0.118 | 0.350 | 0.026 | 0.294 | 0.755 | 0.117 |
| MUTAG | GINE | Saliency | random | 20 | 0.700 | 0.781 | 0.022 | 0.176 | 0.983 | 0.541 | 0.800 | 0.209 | 0.203 | 0.770 | 0.271 |
| MUTAG | GINE | Saliency | scaffold | 20 | 0.800 | 0.857 | 0.026 | 0.131 | 0.997 | 0.376 | 0.350 | 0.267 | 0.230 | 0.771 | 0.117 |
| MUTAG | MPNN | IntegratedGradients | scaffold | 20 | 0.750 | 0.868 | 0.356 | 0.274 | 0.985 | 0.191 | 0.600 | 0.263 | 0.312 | 0.768 | 0.129 |
| SIDER | GCN | IntegratedGradients | random | 100 | 0.640 | 0.677 | — | — | 0.722 | 0.479 | 0.720 | 0.141 | 0.249 | 0.762 | 0.050 |
| SIDER | GCN | IntegratedGradients | scaffold | 100 | 0.650 | 0.663 | — | — | 0.746 | 0.067 | 0.620 | 0.060 | 0.118 | 0.673 | 0.054 |
| SIDER | GINE | GNNExplainer | scaffold | 30 | 0.633 | 0.661 | — | — | 0.816 | 0.490 | 0.833 | 0.038 | 0.196 | 0.732 | 0.110 |
| SIDER | GINE | InputXGradient | scaffold | 30 | 0.633 | 0.661 | — | — | 0.878 | 0.576 | 0.867 | 0.088 | 0.196 | 0.716 | 0.110 |
| SIDER | GINE | IntegratedGradients | random | 100 | 0.710 | 0.682 | — | — | 0.761 | 0.516 | 0.660 | 0.157 | 0.315 | 0.762 | 0.049 |
| SIDER | GINE | IntegratedGradients | scaffold | 100 | 0.570 | 0.650 | — | — | 0.836 | 0.816 | 0.860 | 0.065 | 0.082 | 0.679 | 0.072 |
| SIDER | GINE | Saliency | scaffold | 30 | 0.633 | 0.661 | — | — | 0.887 | 0.571 | 0.867 | 0.093 | 0.201 | 0.720 | 0.110 |
| SynthMotifs | AttentiveFP | IntegratedGradients | random | 20 | 1.000 | 1.000 | 0.716 | 0.550 | 0.215 | -0.162 | 0.300 | 0.335 | 0.296 | 0.788 | 0.013 |
| SynthMotifs | AttentiveFP | IntegratedGradients | scaffold | 20 | 0.850 | 0.970 | 0.886 | 0.624 | 0.132 | -0.121 | 0.100 | 0.276 | 0.247 | 0.790 | 0.124 |
| SynthMotifs | GAT | IntegratedGradients | random | 20 | 1.000 | 1.000 | 0.874 | 0.672 | 0.122 | 0.362 | 0.200 | 0.243 | 0.215 | 0.790 | 0.023 |
| SynthMotifs | GAT | IntegratedGradients | scaffold | 20 | 0.950 | 0.990 | 0.592 | 0.433 | 0.216 | 0.155 | 0.100 | 0.071 | 0.066 | 0.783 | 0.281 |
| SynthMotifs | GCN | IntegratedGradients | random | 20 | 0.600 | 1.000 | 0.480 | 0.339 | 0.100 | 0.376 | 0.100 | 0.119 | 0.142 | 0.797 | 0.242 |
| SynthMotifs | GCN | IntegratedGradients | scaffold | 20 | 0.700 | 1.000 | 0.987 | 0.932 | 0.152 | 0.325 | 0.250 | 0.269 | 0.164 | 0.798 | 0.165 |
| SynthMotifs | GINE | GNNExplainer | random | 20 | 1.000 | 1.000 | 0.474 | 0.250 | 0.038 | 0.022 | 0.050 | 0.171 | 0.222 | 0.800 | 0.000 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 20 | 0.950 | 1.000 | 0.668 | 0.360 | 0.052 | 0.063 | 0.000 | 0.201 | 0.168 | 0.800 | 0.029 |
| SynthMotifs | GINE | GuidedBackprop | random | 20 | 1.000 | 1.000 | 1.000 | 1.000 | 0.172 | 0.640 | 0.500 | 0.212 | 0.070 | 0.800 | 0.000 |
| SynthMotifs | GINE | GuidedBackprop | scaffold | 20 | 0.950 | 1.000 | 0.928 | 0.728 | 0.114 | 0.194 | 0.450 | 0.209 | 0.095 | 0.793 | 0.029 |
| SynthMotifs | GINE | InputXGradient | random | 20 | 1.000 | 1.000 | 0.992 | 0.968 | 0.184 | 0.568 | 0.300 | 0.212 | 0.084 | 0.797 | 0.000 |
| SynthMotifs | GINE | InputXGradient | scaffold | 20 | 0.950 | 1.000 | 0.968 | 0.881 | 0.194 | 0.207 | 0.100 | 0.242 | 0.109 | 0.792 | 0.029 |
| SynthMotifs | GINE | IntegratedGradients | random | 20 | 1.000 | 1.000 | 0.998 | 0.993 | 0.182 | 0.614 | 0.400 | 0.216 | 0.092 | 0.798 | 0.000 |
| SynthMotifs | GINE | IntegratedGradients | scaffold | 20 | 0.950 | 1.000 | 0.901 | 0.655 | 0.126 | 0.292 | 0.450 | 0.281 | 0.060 | 0.793 | 0.029 |
| SynthMotifs | GINE | PGExplainer | scaffold | 20 | 1.000 | 1.000 | 0.360 | 0.220 | 0.393 | 0.106 | 0.000 | 0.064 | 0.126 | 0.787 | 0.000 |
| SynthMotifs | GINE | Saliency | random | 20 | 1.000 | 1.000 | 0.999 | 0.997 | 0.167 | 0.584 | 0.350 | 0.234 | 0.068 | 0.798 | 0.000 |
| SynthMotifs | GINE | Saliency | scaffold | 20 | 0.950 | 1.000 | 0.975 | 0.915 | 0.139 | 0.194 | 0.000 | 0.256 | 0.099 | 0.792 | 0.029 |
| SynthMotifs | MPNN | IntegratedGradients | random | 20 | 1.000 | 1.000 | 0.839 | 0.668 | 0.119 | 0.382 | 0.450 | 0.410 | 0.459 | 0.798 | 0.025 |
| SynthMotifs | MPNN | IntegratedGradients | scaffold | 20 | 0.650 | 0.980 | 0.712 | 0.391 | 0.304 | 0.525 | 0.400 | 0.423 | 0.209 | 0.797 | 0.196 |
| SynthMotifsXL | GINE | GNNExplainer | random | 120 | 1.000 | 1.000 | 0.501 | 0.259 | 0.041 | 0.033 | 0.167 | 0.364 | 0.472 | 0.800 | 0.000 |
| SynthMotifsXL | GINE | GuidedBackprop | random | 120 | 1.000 | 1.000 | 1.000 | 0.998 | 0.164 | 0.529 | 0.517 | 0.495 | 0.006 | 0.800 | 0.000 |
| SynthMotifsXL | GINE | InputXGradient | random | 120 | 1.000 | 1.000 | 0.989 | 0.958 | 0.239 | 0.393 | 0.150 | 0.493 | 0.089 | 0.798 | 0.000 |
| SynthMotifsXL | GINE | IntegratedGradients | random | 120 | 1.000 | 1.000 | 0.987 | 0.945 | 0.257 | 0.403 | 0.375 | 0.493 | 0.021 | 0.797 | 0.000 |
| SynthMotifsXL | GINE | PGExplainer | random | 120 | 1.000 | 1.000 | 0.269 | 0.165 | 0.389 | -0.227 | 0.000 | 0.050 | 0.487 | 0.773 | 0.000 |
| SynthMotifsXL | GINE | Saliency | random | 120 | 1.000 | 1.000 | 0.990 | 0.962 | 0.214 | 0.424 | 0.150 | 0.492 | 0.127 | 0.798 | 0.000 |
| Tox21 | GINE | GNNExplainer | scaffold | 30 | 1.000 | 0.827 | — | — | 0.719 | 0.010 | 0.367 | -0.066 | -0.061 | 0.786 | 0.054 |
| Tox21 | GINE | InputXGradient | scaffold | 30 | 1.000 | 0.827 | — | — | 0.704 | -0.409 | 0.167 | -0.075 | -0.060 | 0.780 | 0.054 |
| Tox21 | GINE | IntegratedGradients | random | 100 | 0.970 | 0.849 | — | — | 0.752 | -0.739 | 0.150 | -0.058 | -0.080 | 0.765 | 0.099 |
| Tox21 | GINE | IntegratedGradients | scaffold | 100 | 0.960 | 0.822 | — | — | 0.739 | -0.367 | 0.250 | -0.011 | -0.009 | 0.766 | 0.028 |
| Tox21 | GINE | Saliency | scaffold | 30 | 1.000 | 0.827 | — | — | 0.697 | -0.391 | 0.167 | -0.073 | -0.063 | 0.780 | 0.054 |
| hERG | GCN | IntegratedGradients | scaffold | 30 | 0.900 | 0.802 | — | — | 0.665 | 0.711 | 0.867 | 0.589 | 0.590 | 0.776 | 0.098 |
| hERG | GINE | GNNExplainer | scaffold | 30 | 0.733 | 0.784 | — | — | 0.725 | 0.066 | 0.633 | 0.094 | 0.408 | 0.786 | 0.070 |
| hERG | GINE | InputXGradient | scaffold | 30 | 0.733 | 0.784 | — | — | 0.633 | 0.342 | 0.600 | 0.410 | 0.408 | 0.779 | 0.070 |
| hERG | GINE | IntegratedGradients | random | 66 | 0.803 | 0.824 | — | — | 0.776 | 0.661 | 0.833 | 0.560 | 0.560 | 0.779 | 0.093 |
| hERG | GINE | IntegratedGradients | scaffold | 66 | 0.727 | 0.805 | — | — | 0.689 | 0.245 | 0.606 | 0.337 | 0.337 | 0.774 | 0.070 |
| hERG | GINE | Saliency | scaffold | 30 | 0.733 | 0.784 | — | — | 0.626 | 0.343 | 0.533 | 0.409 | 0.408 | 0.784 | 0.070 |

## Regression audit matrix

| dataset | backbone | attributor | split | n_mol | rmse | mae | r2 | motif_top1 | occ_spearman | occ_top1 | fid+ | fid- | sparsity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ESOL | GAT | IntegratedGradients | random | 100 | 0.730 | 0.549 | 0.888 | 0.850 | 0.845 | 0.970 | 3.524 | 6.515 | 0.715 |
| ESOL | GAT | IntegratedGradients | scaffold | 100 | 0.793 | 0.627 | 0.838 | 0.838 | 0.862 | 0.960 | 5.007 | 9.467 | 0.726 |
| ESOL | GCN | IntegratedGradients | random | 100 | 0.951 | 0.746 | 0.809 | 0.870 | -0.534 | 0.330 | -0.827 | -0.916 | 0.710 |
| ESOL | GCN | IntegratedGradients | scaffold | 100 | 1.017 | 0.793 | 0.734 | 0.870 | -0.509 | 0.350 | -0.882 | -1.277 | 0.724 |
| ESOL | GINE | GNNExplainer | random | 100 | 0.788 | 0.599 | 0.869 | 0.868 | -0.873 | 0.230 | -1.346 | -2.714 | 0.753 |
| ESOL | GINE | GNNExplainer | scaffold | 100 | 0.929 | 0.724 | 0.778 | 0.853 | -0.739 | 0.280 | -0.913 | -2.167 | 0.763 |
| ESOL | GINE | GuidedBackprop | scaffold | 20 | 1.132 | 0.918 | 0.671 | 0.659 | -0.741 | 0.150 | -0.582 | -1.326 | 0.789 |
| ESOL | GINE | InputXGradient | scaffold | 20 | 1.132 | 0.918 | 0.671 | 0.881 | -0.793 | 0.100 | -1.016 | -1.219 | 0.722 |
| ESOL | GINE | IntegratedGradients | random | 100 | 0.788 | 0.599 | 0.869 | 0.878 | -0.944 | 0.230 | -1.733 | -2.430 | 0.719 |
| ESOL | GINE | IntegratedGradients | scaffold | 100 | 0.929 | 0.724 | 0.778 | 0.878 | -0.778 | 0.290 | -1.391 | -1.986 | 0.720 |
| ESOL | GINE | Saliency | scaffold | 20 | 1.132 | 0.918 | 0.671 | 0.878 | -0.798 | 0.100 | -0.996 | -1.234 | 0.727 |
| FreeSolv | GCN | IntegratedGradients | scaffold | 20 | 2.567 | 2.048 | 0.538 | 0.782 | -0.434 | 0.400 | -0.046 | -0.935 | 0.745 |
| FreeSolv | GINE | GNNExplainer | scaffold | 20 | 2.347 | 1.733 | 0.614 | 0.766 | -0.600 | 0.350 | -0.424 | -0.985 | 0.755 |
| FreeSolv | GINE | InputXGradient | scaffold | 20 | 2.347 | 1.733 | 0.614 | 0.805 | -0.370 | 0.450 | -0.364 | -0.943 | 0.714 |
| FreeSolv | GINE | IntegratedGradients | random | 65 | 1.486 | 1.081 | 0.803 | 0.864 | -0.418 | 0.523 | -0.661 | -1.021 | 0.710 |
| FreeSolv | GINE | IntegratedGradients | scaffold | 20 | 2.347 | 1.733 | 0.614 | 0.782 | -0.582 | 0.400 | -0.543 | -0.922 | 0.738 |
| FreeSolv | GINE | Saliency | scaffold | 20 | 2.347 | 1.733 | 0.614 | 0.789 | -0.425 | 0.450 | -0.371 | -0.939 | 0.736 |
| Lipophilicity | GAT | IntegratedGradients | scaffold | 20 | 0.940 | 0.746 | 0.391 | 0.762 | 0.458 | 0.900 | -0.144 | 0.482 | 0.785 |
| Lipophilicity | GINE | GNNExplainer | scaffold | 20 | 0.932 | 0.740 | 0.402 | 0.845 | -0.499 | 0.000 | -0.251 | -0.500 | 0.788 |
| Lipophilicity | GINE | InputXGradient | scaffold | 20 | 0.932 | 0.740 | 0.402 | 0.699 | -0.439 | 0.000 | -0.281 | -0.510 | 0.787 |
| Lipophilicity | GINE | IntegratedGradients | random | 100 | 0.737 | 0.571 | 0.617 | 0.775 | 0.464 | 0.720 | 0.516 | 0.509 | 0.778 |
| Lipophilicity | GINE | IntegratedGradients | scaffold | 100 | 0.749 | 0.584 | 0.614 | 0.760 | 0.575 | 0.860 | 1.033 | 1.954 | 0.781 |
| Lipophilicity | GINE | Saliency | scaffold | 20 | 0.932 | 0.740 | 0.402 | 0.705 | -0.469 | 0.000 | -0.299 | -0.468 | 0.788 |

### Metric legend
- **acc/auc**: classification test accuracy / ROC-AUC (AUC is the honest signal on imbalanced sets, where accuracy tracks the majority class). **gt_auroc/gt_auprc**: attribution vs ground-truth motif mask (Tier-1 only; chance AUROC = 0.5; below 0.5 = *anti-aligned* with the motif).
- **rmse/mae/r2**: regression test-set error metrics (original units).
- **motif_top1**: fraction of attribution mass in the single top RDKit motif. **occ_spearman/occ_top1**: occlusion-vs-attribution faithfulness.
- **fid+/fid-**: Fidelity+ (predicted prob/value drop removing salient atoms; higher is better) / Fidelity- (removing non-salient; lower is better). **ece**: test-set expected calibration error (temperature-scaled).
