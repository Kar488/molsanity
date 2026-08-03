# RESULTS.md — validated numbers only

> Every number here is computed by code in this run and traceable to a
> logged artifact under `artifacts/`. No placeholders. See `LIMITATIONS.md`
> for caveats (notably: MUTAG ground truth is a chemically motivated
> nitro-motif *proxy*, not annotator labels).

## Classification audit matrix (dataset × backbone × attributor)

| dataset | backbone | attributor | split | seed | n_mol | acc | auc | gt_auroc | gt_auprc | motif_top1 | occ_spearman | occ_top1 | fid+ | fid- | sparsity | ece |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BA-2Motifs | GINE | GNNExplainer | random | 0 | 200 | 0.780 | 1.000 | 0.501 | 0.298 | 0.042 | 0.006 | 0.050 | 0.014 | 0.091 | 0.800 | 0.076 |
| BA-2Motifs | GINE | GNNExplainer | random | 1 | 200 | 0.645 | 1.000 | 0.459 | 0.272 | 0.042 | -0.008 | 0.040 | -0.008 | -0.012 | 0.800 | 0.080 |
| BA-2Motifs | GINE | GNNExplainer | random | 2 | 200 | 0.875 | 1.000 | 0.574 | 0.355 | 0.042 | -0.078 | 0.010 | -0.008 | -0.021 | 0.800 | 0.034 |
| BA-2Motifs | GINE | GNNExplainer | scaffold | 0 | 200 | 0.985 | 0.990 | 0.485 | 0.280 | 0.042 | 0.021 | 0.095 | 0.011 | 0.045 | 0.800 | 0.253 |
| BA-2Motifs | GINE | GNNExplainer | scaffold | 1 | 200 | 0.990 | 0.987 | 0.500 | 0.259 | 0.046 | 0.206 | 0.350 | 0.043 | 0.099 | 0.800 | 0.012 |
| BA-2Motifs | GINE | GNNExplainer | scaffold | 2 | 200 | 0.900 | 0.980 | 0.503 | 0.299 | 0.042 | 0.007 | 0.040 | 0.003 | 0.011 | 0.800 | 0.206 |
| BA-2Motifs | GINE | GuidedBackprop | random | 0 | 200 | 0.780 | 1.000 | 0.923 | 0.859 | 0.180 | -0.159 | 0.140 | 0.141 | -0.004 | 0.790 | 0.076 |
| BA-2Motifs | GINE | GuidedBackprop | random | 1 | 200 | 0.645 | 1.000 | 0.963 | 0.943 | 0.180 | -0.262 | 0.000 | -0.012 | -0.001 | 0.781 | 0.080 |
| BA-2Motifs | GINE | GuidedBackprop | random | 2 | 200 | 0.875 | 1.000 | 0.948 | 0.900 | 0.133 | -0.323 | 0.005 | -0.013 | -0.014 | 0.797 | 0.034 |
| BA-2Motifs | GINE | GuidedBackprop | scaffold | 0 | 200 | 0.985 | 0.990 | 0.850 | 0.524 | 0.106 | 0.588 | 0.305 | 0.022 | 0.033 | 0.797 | 0.253 |
| BA-2Motifs | GINE | GuidedBackprop | scaffold | 1 | 200 | 0.990 | 0.987 | 0.934 | 0.745 | 0.115 | 0.758 | 0.635 | 0.070 | 0.072 | 0.800 | 0.012 |
| BA-2Motifs | GINE | GuidedBackprop | scaffold | 2 | 200 | 0.900 | 0.980 | 0.908 | 0.814 | 0.136 | 0.506 | 0.755 | 0.007 | 0.006 | 0.792 | 0.206 |
| BA-2Motifs | GINE | InputXGradient | random | 0 | 200 | 0.780 | 1.000 | 1.000 | 0.998 | 0.213 | -0.148 | 0.155 | 0.111 | 0.020 | 0.800 | 0.076 |
| BA-2Motifs | GINE | InputXGradient | random | 1 | 200 | 0.645 | 1.000 | 0.996 | 0.987 | 0.199 | -0.164 | 0.280 | -0.010 | -0.002 | 0.800 | 0.080 |
| BA-2Motifs | GINE | InputXGradient | random | 2 | 200 | 0.875 | 1.000 | 0.928 | 0.740 | 0.127 | -0.260 | 0.005 | -0.012 | -0.016 | 0.790 | 0.034 |
| BA-2Motifs | GINE | InputXGradient | scaffold | 0 | 200 | 0.985 | 0.990 | 0.895 | 0.661 | 0.105 | 0.916 | 0.745 | 0.025 | 0.030 | 0.799 | 0.253 |
| BA-2Motifs | GINE | InputXGradient | scaffold | 1 | 200 | 0.990 | 0.987 | 0.935 | 0.757 | 0.111 | 0.773 | 0.905 | 0.065 | 0.076 | 0.800 | 0.012 |
| BA-2Motifs | GINE | InputXGradient | scaffold | 2 | 200 | 0.900 | 0.980 | 0.963 | 0.836 | 0.127 | 0.516 | 0.715 | 0.007 | 0.007 | 0.800 | 0.206 |
| BA-2Motifs | GINE | IntegratedGradients | random | 0 | 200 | 0.780 | 1.000 | 0.996 | 0.987 | 0.210 | -0.177 | 0.160 | 0.112 | 0.020 | 0.800 | 0.076 |
| BA-2Motifs | GINE | IntegratedGradients | random | 1 | 200 | 0.645 | 1.000 | 1.000 | 1.000 | 0.172 | -0.159 | 0.200 | -0.009 | -0.004 | 0.800 | 0.080 |
| BA-2Motifs | GINE | IntegratedGradients | random | 2 | 200 | 0.875 | 1.000 | 0.994 | 0.978 | 0.132 | -0.276 | 0.040 | -0.013 | -0.014 | 0.800 | 0.034 |
| BA-2Motifs | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.985 | 0.990 | 0.862 | 0.542 | 0.118 | 0.663 | 0.380 | 0.023 | 0.032 | 0.799 | 0.253 |
| BA-2Motifs | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.990 | 0.987 | 0.892 | 0.675 | 0.117 | 0.704 | 0.855 | 0.069 | 0.076 | 0.800 | 0.012 |
| BA-2Motifs | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.900 | 0.980 | 0.947 | 0.783 | 0.128 | 0.519 | 0.720 | 0.009 | 0.005 | 0.800 | 0.206 |
| BA-2Motifs | GINE | PGExplainer | random | 0 | 200 | 0.780 | 1.000 | 0.485 | 0.273 | 0.362 | -0.114 | 0.000 | 0.021 | 0.108 | 0.743 | 0.076 |
| BA-2Motifs | GINE | PGExplainer | random | 1 | 200 | 0.645 | 1.000 | 0.604 | 0.450 | 0.410 | 0.003 | 0.005 | 0.001 | -0.004 | 0.756 | 0.080 |
| BA-2Motifs | GINE | PGExplainer | random | 2 | 200 | 0.875 | 1.000 | 0.104 | 0.190 | 0.378 | 0.155 | 0.000 | -0.003 | -0.023 | 0.777 | 0.034 |
| BA-2Motifs | GINE | PGExplainer | scaffold | 0 | 200 | 0.985 | 0.990 | 0.954 | 0.911 | 0.497 | 0.474 | 0.055 | 0.022 | 0.034 | 0.782 | 0.253 |
| BA-2Motifs | GINE | PGExplainer | scaffold | 1 | 200 | 0.990 | 0.987 | 0.857 | 0.723 | 0.405 | 0.383 | 0.000 | 0.046 | 0.099 | 0.765 | 0.012 |
| BA-2Motifs | GINE | PGExplainer | scaffold | 2 | 200 | 0.900 | 0.980 | 0.881 | 0.793 | 0.424 | 0.095 | 0.010 | 0.003 | 0.011 | 0.763 | 0.206 |
| BA-2Motifs | GINE | Saliency | random | 0 | 200 | 0.780 | 1.000 | 1.000 | 0.998 | 0.213 | -0.148 | 0.155 | 0.111 | 0.020 | 0.800 | 0.076 |
| BA-2Motifs | GINE | Saliency | random | 1 | 200 | 0.645 | 1.000 | 0.996 | 0.987 | 0.199 | -0.164 | 0.280 | -0.010 | -0.002 | 0.800 | 0.080 |
| BA-2Motifs | GINE | Saliency | random | 2 | 200 | 0.875 | 1.000 | 0.928 | 0.740 | 0.127 | -0.260 | 0.005 | -0.012 | -0.016 | 0.790 | 0.034 |
| BA-2Motifs | GINE | Saliency | scaffold | 0 | 200 | 0.985 | 0.990 | 0.895 | 0.661 | 0.105 | 0.916 | 0.745 | 0.025 | 0.030 | 0.799 | 0.253 |
| BA-2Motifs | GINE | Saliency | scaffold | 1 | 200 | 0.990 | 0.987 | 0.935 | 0.757 | 0.111 | 0.773 | 0.905 | 0.065 | 0.076 | 0.800 | 0.012 |
| BA-2Motifs | GINE | Saliency | scaffold | 2 | 200 | 0.900 | 0.980 | 0.963 | 0.836 | 0.127 | 0.516 | 0.715 | 0.007 | 0.007 | 0.800 | 0.206 |
| BACE | GCN | IntegratedGradients | random | 0 | 200 | 0.725 | 0.839 | — | — | 0.782 | 0.170 | 0.610 | 0.266 | 0.311 | 0.786 | 0.082 |
| BACE | GCN | IntegratedGradients | random | 1 | 200 | 0.585 | 0.797 | — | — | 0.775 | 0.002 | 0.460 | 0.189 | 0.191 | 0.786 | 0.039 |
| BACE | GCN | IntegratedGradients | random | 2 | 200 | 0.850 | 0.820 | — | — | 0.756 | 0.532 | 0.830 | 0.576 | 0.596 | 0.785 | 0.036 |
| BACE | GCN | IntegratedGradients | scaffold | 0 | 200 | 0.830 | 0.507 | — | — | 0.781 | -0.623 | 0.160 | -0.109 | -0.109 | 0.783 | 0.069 |
| BACE | GCN | IntegratedGradients | scaffold | 1 | 200 | 0.585 | 0.233 | — | — | 0.789 | -0.153 | 0.410 | 0.057 | 0.057 | 0.787 | 0.077 |
| BACE | GCN | IntegratedGradients | scaffold | 2 | 200 | 0.855 | 0.160 | — | — | 0.778 | -0.683 | 0.140 | -0.114 | -0.114 | 0.783 | 0.064 |
| BACE | GINE | IntegratedGradients | random | 0 | 200 | 0.810 | 0.846 | — | — | 0.824 | 0.359 | 0.675 | 0.390 | 0.347 | 0.787 | 0.055 |
| BACE | GINE | IntegratedGradients | random | 1 | 200 | 0.695 | 0.797 | — | — | 0.790 | 0.193 | 0.610 | 0.330 | 0.343 | 0.786 | 0.057 |
| BACE | GINE | IntegratedGradients | random | 2 | 200 | 0.685 | 0.820 | — | — | 0.751 | -0.203 | 0.385 | 0.103 | 0.115 | 0.787 | 0.075 |
| BACE | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.470 | 0.651 | — | — | 0.806 | 0.422 | 0.740 | 0.128 | 0.102 | 0.784 | 0.179 |
| BACE | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.770 | 0.332 | — | — | 0.715 | 0.505 | 0.700 | 0.326 | 0.358 | 0.785 | 0.047 |
| BACE | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.005 | 0.105 | — | — | 0.818 | 0.502 | 0.435 | 0.005 | 0.011 | 0.786 | 0.499 |
| BBBP | AttentiveFP | IntegratedGradients | random | 0 | 200 | 0.785 | 0.855 | — | — | 0.756 | 0.253 | 0.425 | 0.086 | 0.165 | 0.771 | 0.050 |
| BBBP | AttentiveFP | IntegratedGradients | random | 1 | 200 | 0.745 | 0.913 | — | — | 0.760 | 0.220 | 0.415 | 0.123 | 0.046 | 0.762 | 0.024 |
| BBBP | AttentiveFP | IntegratedGradients | random | 2 | 200 | 0.740 | 0.885 | — | — | 0.732 | 0.230 | 0.415 | 0.068 | 0.069 | 0.759 | 0.040 |
| BBBP | AttentiveFP | IntegratedGradients | scaffold | 0 | 200 | 0.940 | 0.961 | — | — | 0.792 | 0.220 | 0.295 | 0.018 | 0.014 | 0.773 | 0.033 |
| BBBP | AttentiveFP | IntegratedGradients | scaffold | 1 | 200 | 0.895 | 0.900 | — | — | 0.688 | 0.205 | 0.375 | 0.004 | 0.025 | 0.773 | 0.014 |
| BBBP | AttentiveFP | IntegratedGradients | scaffold | 2 | 200 | 0.935 | 0.959 | — | — | 0.721 | -0.031 | 0.320 | -0.020 | 0.021 | 0.772 | 0.022 |
| BBBP | GAT | IntegratedGradients | random | 0 | 200 | 0.735 | 0.885 | — | — | 0.760 | 0.044 | 0.505 | 0.268 | 0.267 | 0.775 | 0.051 |
| BBBP | GAT | IntegratedGradients | random | 1 | 200 | 0.740 | 0.906 | — | — | 0.802 | -0.067 | 0.505 | 0.230 | 0.230 | 0.767 | 0.039 |
| BBBP | GAT | IntegratedGradients | random | 2 | 200 | 0.730 | 0.909 | — | — | 0.748 | 0.029 | 0.330 | 0.158 | 0.159 | 0.767 | 0.007 |
| BBBP | GAT | IntegratedGradients | scaffold | 0 | 200 | 0.990 | 0.805 | — | — | 0.776 | -0.727 | 0.015 | -0.049 | -0.070 | 0.774 | 0.010 |
| BBBP | GAT | IntegratedGradients | scaffold | 1 | 200 | 0.885 | 0.940 | — | — | 0.754 | -0.545 | 0.140 | -0.014 | -0.015 | 0.777 | 0.018 |
| BBBP | GAT | IntegratedGradients | scaffold | 2 | 200 | 0.970 | 0.798 | — | — | 0.728 | -0.826 | 0.040 | -0.095 | -0.105 | 0.773 | 0.016 |
| BBBP | GCN | IntegratedGradients | random | 0 | 200 | 0.735 | 0.873 | — | — | 0.769 | -0.040 | 0.475 | 0.222 | 0.224 | 0.770 | 0.074 |
| BBBP | GCN | IntegratedGradients | random | 1 | 200 | 0.710 | 0.893 | — | — | 0.824 | -0.012 | 0.505 | 0.236 | 0.243 | 0.761 | 0.025 |
| BBBP | GCN | IntegratedGradients | random | 2 | 200 | 0.775 | 0.902 | — | — | 0.794 | -0.376 | 0.295 | 0.008 | 0.003 | 0.765 | 0.031 |
| BBBP | GCN | IntegratedGradients | scaffold | 0 | 200 | 0.980 | 0.966 | — | — | 0.767 | -0.761 | 0.045 | -0.013 | -0.145 | 0.774 | 0.013 |
| BBBP | GCN | IntegratedGradients | scaffold | 1 | 200 | 0.915 | 0.958 | — | — | 0.775 | -0.273 | 0.100 | 0.006 | -0.080 | 0.774 | 0.041 |
| BBBP | GCN | IntegratedGradients | scaffold | 2 | 200 | 0.975 | 0.894 | — | — | 0.751 | -0.731 | 0.050 | -0.113 | -0.211 | 0.775 | 0.010 |
| BBBP | GINE | GNNExplainer | random | 0 | 200 | 0.745 | 0.886 | — | — | 0.780 | -0.200 | 0.300 | 0.159 | 0.200 | 0.779 | 0.053 |
| BBBP | GINE | GNNExplainer | random | 1 | 200 | 0.760 | 0.899 | — | — | 0.828 | -0.034 | 0.455 | 0.171 | 0.214 | 0.777 | 0.016 |
| BBBP | GINE | GNNExplainer | random | 2 | 200 | 0.685 | 0.891 | — | — | 0.789 | 0.179 | 0.435 | 0.218 | 0.234 | 0.779 | 0.031 |
| BBBP | GINE | GNNExplainer | scaffold | 0 | 200 | 0.915 | 0.932 | — | — | 0.799 | -0.391 | 0.100 | 0.028 | -0.038 | 0.781 | 0.029 |
| BBBP | GINE | GNNExplainer | scaffold | 1 | 200 | 0.720 | 0.918 | — | — | 0.787 | -0.294 | 0.225 | 0.091 | 0.059 | 0.781 | 0.070 |
| BBBP | GINE | GNNExplainer | scaffold | 2 | 200 | 0.840 | 0.941 | — | — | 0.802 | -0.355 | 0.165 | 0.004 | -0.060 | 0.781 | 0.024 |
| BBBP | GINE | IntegratedGradients | random | 0 | 200 | 0.745 | 0.886 | — | — | 0.719 | -0.175 | 0.370 | 0.201 | 0.201 | 0.772 | 0.053 |
| BBBP | GINE | IntegratedGradients | random | 1 | 200 | 0.760 | 0.899 | — | — | 0.826 | 0.082 | 0.460 | 0.266 | 0.213 | 0.766 | 0.016 |
| BBBP | GINE | IntegratedGradients | random | 2 | 200 | 0.685 | 0.891 | — | — | 0.764 | 0.226 | 0.450 | 0.191 | 0.246 | 0.772 | 0.031 |
| BBBP | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.915 | 0.932 | — | — | 0.794 | -0.663 | 0.095 | -0.009 | -0.031 | 0.777 | 0.029 |
| BBBP | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.720 | 0.918 | — | — | 0.736 | -0.341 | 0.260 | 0.099 | 0.051 | 0.771 | 0.070 |
| BBBP | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.840 | 0.941 | — | — | 0.755 | -0.562 | 0.175 | -0.039 | -0.058 | 0.776 | 0.024 |
| BBBP | GINE | PGExplainer | random | 0 | 200 | 0.745 | 0.886 | — | — | 0.886 | -0.160 | 0.250 | 0.091 | 0.200 | 0.773 | 0.053 |
| BBBP | GINE | PGExplainer | random | 1 | 200 | 0.760 | 0.899 | — | — | 0.933 | -0.149 | 0.305 | 0.173 | 0.178 | 0.703 | 0.016 |
| BBBP | GINE | PGExplainer | random | 2 | 200 | 0.685 | 0.891 | — | — | 0.879 | -0.085 | 0.300 | 0.114 | 0.229 | 0.690 | 0.031 |
| BBBP | GINE | PGExplainer | scaffold | 0 | 200 | 0.915 | 0.932 | — | — | 0.937 | -0.481 | 0.095 | -0.009 | -0.034 | 0.778 | 0.029 |
| BBBP | GINE | PGExplainer | scaffold | 1 | 200 | 0.720 | 0.918 | — | — | 0.855 | -0.309 | 0.165 | 0.048 | 0.031 | 0.592 | 0.070 |
| BBBP | GINE | PGExplainer | scaffold | 2 | 200 | 0.840 | 0.941 | — | — | 0.821 | -0.298 | 0.215 | -0.042 | -0.051 | 0.593 | 0.024 |
| BBBP | MPNN | IntegratedGradients | random | 0 | 200 | 0.740 | 0.914 | — | — | 0.792 | 0.018 | 0.345 | 0.119 | 0.150 | 0.771 | 0.053 |
| BBBP | MPNN | IntegratedGradients | random | 1 | 200 | 0.775 | 0.904 | — | — | 0.810 | 0.247 | 0.455 | 0.119 | 0.209 | 0.763 | 0.023 |
| BBBP | MPNN | IntegratedGradients | random | 2 | 200 | 0.755 | 0.899 | — | — | 0.774 | -0.125 | 0.320 | 0.089 | 0.147 | 0.769 | 0.043 |
| BBBP | MPNN | IntegratedGradients | scaffold | 0 | 200 | 0.870 | 0.922 | — | — | 0.787 | -0.379 | 0.115 | 0.069 | 0.026 | 0.777 | 0.033 |
| BBBP | MPNN | IntegratedGradients | scaffold | 1 | 200 | 0.005 | 0.824 | — | — | 0.940 | -0.800 | 0.045 | -0.051 | -0.036 | 0.774 | 0.504 |
| BBBP | MPNN | IntegratedGradients | scaffold | 2 | 200 | 0.950 | 0.863 | — | — | 0.809 | -0.543 | 0.050 | -0.038 | -0.055 | 0.778 | 0.011 |
| ClinTox | GINE | GNNExplainer | random | 0 | 200 | 0.725 | 0.910 | — | — | 0.566 | 0.065 | 0.435 | 0.245 | 0.226 | 0.840 | 0.157 |
| ClinTox | GINE | GNNExplainer | random | 1 | 200 | 0.760 | 0.870 | — | — | 0.250 | 0.779 | 0.440 | 0.207 | 0.145 | 0.930 | 0.063 |
| ClinTox | GINE | GNNExplainer | random | 2 | 200 | 0.705 | 0.861 | — | — | 0.612 | -0.018 | 0.425 | 0.194 | 0.152 | 0.831 | 0.083 |
| ClinTox | GINE | GNNExplainer | scaffold | 0 | 200 | 0.805 | 0.845 | — | — | 0.547 | -0.354 | 0.250 | 0.084 | 0.037 | 0.820 | 0.062 |
| ClinTox | GINE | GNNExplainer | scaffold | 1 | 200 | 0.785 | 0.839 | — | — | 0.652 | -0.438 | 0.220 | 0.050 | 0.038 | 0.791 | 0.096 |
| ClinTox | GINE | GNNExplainer | scaffold | 2 | 200 | 0.660 | 0.873 | — | — | 0.686 | -0.228 | 0.370 | 0.205 | 0.205 | 0.783 | 0.120 |
| ClinTox | GINE | IntegratedGradients | random | 0 | 200 | 0.725 | 0.910 | — | — | 0.788 | -0.221 | 0.410 | 0.230 | 0.226 | 0.774 | 0.157 |
| ClinTox | GINE | IntegratedGradients | random | 1 | 200 | 0.760 | 0.870 | — | — | 0.815 | -0.417 | 0.335 | 0.148 | 0.145 | 0.769 | 0.063 |
| ClinTox | GINE | IntegratedGradients | random | 2 | 200 | 0.705 | 0.861 | — | — | 0.794 | -0.224 | 0.425 | 0.152 | 0.152 | 0.775 | 0.083 |
| ClinTox | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.805 | 0.845 | — | — | 0.684 | -0.521 | 0.240 | 0.037 | 0.037 | 0.781 | 0.062 |
| ClinTox | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.785 | 0.839 | — | — | 0.676 | -0.537 | 0.230 | 0.038 | 0.038 | 0.781 | 0.096 |
| ClinTox | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.660 | 0.873 | — | — | 0.686 | -0.251 | 0.370 | 0.205 | 0.205 | 0.780 | 0.120 |
| DILI | GINE | IntegratedGradients | random | 0 | 142 | 0.824 | 0.719 | — | — | 0.738 | 0.491 | 0.556 | 0.347 | 0.356 | 0.773 | 0.135 |
| DILI | GINE | IntegratedGradients | random | 1 | 142 | 0.613 | 0.790 | — | — | 0.715 | 0.300 | 0.479 | 0.079 | 0.106 | 0.772 | 0.084 |
| DILI | GINE | IntegratedGradients | random | 2 | 142 | 0.704 | 0.775 | — | — | 0.774 | 0.105 | 0.380 | 0.149 | 0.164 | 0.775 | 0.131 |
| DILI | GINE | IntegratedGradients | scaffold | 0 | 142 | 0.768 | 0.824 | — | — | 0.809 | 0.358 | 0.549 | 0.223 | 0.248 | 0.778 | 0.120 |
| DILI | GINE | IntegratedGradients | scaffold | 1 | 142 | 0.782 | 0.848 | — | — | 0.758 | -0.046 | 0.472 | 0.174 | 0.237 | 0.778 | 0.059 |
| DILI | GINE | IntegratedGradients | scaffold | 2 | 142 | 0.711 | 0.796 | — | — | 0.779 | -0.039 | 0.458 | 0.243 | 0.257 | 0.777 | 0.136 |
| MUTAG | AttentiveFP | IntegratedGradients | random | 0 | 58 | 0.724 | 0.958 | 0.047 | 0.174 | 0.949 | 0.929 | 1.000 | 0.010 | 0.021 | 0.773 | 0.372 |
| MUTAG | AttentiveFP | IntegratedGradients | random | 1 | 58 | 0.810 | 0.875 | 0.034 | 0.173 | 0.977 | 0.411 | 0.672 | 0.193 | 0.374 | 0.769 | 0.068 |
| MUTAG | AttentiveFP | IntegratedGradients | random | 2 | 58 | 0.672 | 0.911 | 0.039 | 0.165 | 0.958 | -0.871 | 0.000 | -0.007 | -0.022 | 0.772 | 0.106 |
| MUTAG | AttentiveFP | IntegratedGradients | scaffold | 0 | 53 | 0.717 | 0.912 | 0.044 | 0.142 | 0.999 | 0.496 | 0.566 | 0.091 | 0.270 | 0.771 | 0.192 |
| MUTAG | AttentiveFP | IntegratedGradients | scaffold | 1 | 53 | 0.755 | 0.834 | 0.337 | 0.392 | 0.990 | 0.978 | 1.000 | 0.007 | 0.026 | 0.772 | 0.166 |
| MUTAG | AttentiveFP | IntegratedGradients | scaffold | 2 | 53 | 0.755 | 0.813 | 0.044 | 0.138 | 0.993 | -0.778 | 0.000 | -0.011 | -0.023 | 0.771 | 0.099 |
| MUTAG | GAT | IntegratedGradients | random | 0 | 58 | 0.741 | 0.583 | 0.689 | 0.612 | 0.935 | 0.313 | 0.638 | 0.350 | 0.385 | 0.772 | 0.247 |
| MUTAG | GAT | IntegratedGradients | random | 1 | 58 | 0.362 | 0.687 | 0.050 | 0.169 | 0.947 | -0.558 | 0.052 | -0.004 | -0.007 | 0.769 | 0.148 |
| MUTAG | GAT | IntegratedGradients | random | 2 | 58 | 0.759 | 0.746 | 0.461 | 0.356 | 0.925 | 0.698 | 0.810 | 0.281 | 0.511 | 0.775 | 0.089 |
| MUTAG | GAT | IntegratedGradients | scaffold | 0 | 53 | 0.830 | 0.868 | 0.425 | 0.266 | 0.988 | 0.498 | 0.717 | 0.395 | 0.435 | 0.772 | 0.232 |
| MUTAG | GAT | IntegratedGradients | scaffold | 1 | 53 | 0.830 | 0.912 | 0.392 | 0.251 | 0.986 | 0.617 | 0.736 | 0.179 | 0.269 | 0.771 | 0.000 |
| MUTAG | GAT | IntegratedGradients | scaffold | 2 | 53 | 0.755 | 0.919 | 0.222 | 0.167 | 0.987 | 0.867 | 1.000 | 0.019 | 0.076 | 0.772 | 0.201 |
| MUTAG | GCN | IntegratedGradients | random | 0 | 58 | 0.776 | 0.604 | 0.170 | 0.238 | 0.950 | 0.299 | 0.603 | 0.276 | 0.387 | 0.772 | 0.308 |
| MUTAG | GCN | IntegratedGradients | random | 1 | 58 | 0.362 | 0.727 | 0.379 | 0.315 | 0.934 | 0.579 | 0.828 | -0.001 | -0.000 | 0.758 | 0.147 |
| MUTAG | GCN | IntegratedGradients | random | 2 | 58 | 0.776 | 0.768 | 0.551 | 0.552 | 0.932 | 0.610 | 0.759 | 0.435 | 0.518 | 0.764 | 0.119 |
| MUTAG | GCN | IntegratedGradients | scaffold | 0 | 53 | 0.245 | 0.791 | 0.979 | 0.934 | 0.975 | 0.454 | 0.057 | -0.000 | -0.002 | 0.772 | 0.154 |
| MUTAG | GCN | IntegratedGradients | scaffold | 1 | 53 | 0.245 | 0.913 | 0.034 | 0.162 | 0.996 | 0.265 | 0.528 | -0.012 | -0.015 | 0.771 | 0.256 |
| MUTAG | GCN | IntegratedGradients | scaffold | 2 | 53 | 0.755 | 0.919 | 0.174 | 0.197 | 0.987 | 0.911 | 1.000 | 0.002 | 0.004 | 0.771 | 0.214 |
| MUTAG | GINE | GNNExplainer | random | 0 | 58 | 0.534 | 0.823 | 0.448 | 0.327 | 0.937 | -0.299 | 0.310 | -0.003 | -0.007 | 0.776 | 0.048 |
| MUTAG | GINE | GNNExplainer | random | 1 | 58 | 0.810 | 0.928 | 0.728 | 0.636 | 0.936 | 0.105 | 0.466 | 0.259 | 0.448 | 0.772 | 0.154 |
| MUTAG | GINE | GNNExplainer | random | 2 | 58 | 0.897 | 0.985 | 0.858 | 0.807 | 0.929 | -0.170 | 0.207 | 0.310 | 0.175 | 0.777 | 0.065 |
| MUTAG | GINE | GNNExplainer | scaffold | 0 | 53 | 0.830 | 0.912 | 0.723 | 0.684 | 0.976 | 0.366 | 0.321 | 0.080 | 0.295 | 0.774 | 0.177 |
| MUTAG | GINE | GNNExplainer | scaffold | 1 | 53 | 0.585 | 0.910 | 0.482 | 0.333 | 0.984 | -0.347 | 0.340 | -0.000 | -0.001 | 0.774 | 0.061 |
| MUTAG | GINE | GNNExplainer | scaffold | 2 | 53 | 0.868 | 0.900 | 0.534 | 0.376 | 0.984 | 0.369 | 0.698 | 0.068 | 0.305 | 0.774 | 0.059 |
| MUTAG | GINE | GuidedBackprop | random | 0 | 58 | 0.534 | 0.823 | 0.225 | 0.246 | 0.941 | -0.323 | 0.310 | -0.003 | -0.006 | 0.773 | 0.048 |
| MUTAG | GINE | GuidedBackprop | random | 1 | 58 | 0.810 | 0.928 | 0.030 | 0.175 | 0.962 | 0.020 | 0.448 | 0.454 | 0.444 | 0.769 | 0.154 |
| MUTAG | GINE | GuidedBackprop | random | 2 | 58 | 0.897 | 0.985 | 0.037 | 0.169 | 0.962 | -0.089 | 0.207 | 0.540 | 0.615 | 0.773 | 0.065 |
| MUTAG | GINE | GuidedBackprop | scaffold | 0 | 53 | 0.830 | 0.912 | 0.007 | 0.134 | 0.995 | 0.427 | 0.321 | 0.264 | 0.318 | 0.772 | 0.177 |
| MUTAG | GINE | GuidedBackprop | scaffold | 1 | 53 | 0.585 | 0.910 | 0.014 | 0.135 | 0.994 | -0.289 | 0.340 | 0.000 | -0.001 | 0.772 | 0.061 |
| MUTAG | GINE | GuidedBackprop | scaffold | 2 | 53 | 0.868 | 0.900 | 0.146 | 0.193 | 0.985 | 0.551 | 0.698 | 0.210 | 0.242 | 0.772 | 0.059 |
| MUTAG | GINE | InputXGradient | random | 0 | 58 | 0.534 | 0.823 | 0.066 | 0.181 | 0.987 | -0.339 | 0.310 | -0.004 | -0.005 | 0.772 | 0.048 |
| MUTAG | GINE | InputXGradient | random | 1 | 58 | 0.810 | 0.928 | 0.025 | 0.166 | 0.976 | 0.022 | 0.448 | 0.398 | 0.463 | 0.770 | 0.154 |
| MUTAG | GINE | InputXGradient | random | 2 | 58 | 0.897 | 0.985 | 0.013 | 0.161 | 0.984 | -0.200 | 0.190 | 0.491 | 0.605 | 0.772 | 0.065 |
| MUTAG | GINE | InputXGradient | scaffold | 0 | 53 | 0.830 | 0.912 | 0.032 | 0.138 | 0.999 | 0.394 | 0.321 | 0.262 | 0.330 | 0.773 | 0.177 |
| MUTAG | GINE | InputXGradient | scaffold | 1 | 53 | 0.585 | 0.910 | 0.049 | 0.146 | 0.996 | -0.289 | 0.340 | 0.000 | -0.001 | 0.773 | 0.061 |
| MUTAG | GINE | InputXGradient | scaffold | 2 | 53 | 0.868 | 0.900 | 0.048 | 0.140 | 0.995 | 0.534 | 0.698 | 0.199 | 0.246 | 0.772 | 0.059 |
| MUTAG | GINE | IntegratedGradients | random | 0 | 58 | 0.534 | 0.823 | 0.052 | 0.175 | 0.984 | -0.351 | 0.310 | -0.004 | -0.005 | 0.771 | 0.048 |
| MUTAG | GINE | IntegratedGradients | random | 1 | 58 | 0.810 | 0.928 | 0.612 | 0.433 | 0.937 | 0.015 | 0.466 | 0.442 | 0.510 | 0.767 | 0.154 |
| MUTAG | GINE | IntegratedGradients | random | 2 | 58 | 0.897 | 0.985 | 0.496 | 0.460 | 0.915 | -0.196 | 0.155 | 0.551 | 0.433 | 0.772 | 0.065 |
| MUTAG | GINE | IntegratedGradients | scaffold | 0 | 53 | 0.830 | 0.912 | 0.571 | 0.371 | 0.980 | 0.209 | 0.321 | 0.116 | 0.344 | 0.768 | 0.177 |
| MUTAG | GINE | IntegratedGradients | scaffold | 1 | 53 | 0.585 | 0.910 | 0.016 | 0.135 | 0.996 | -0.315 | 0.340 | -0.000 | -0.001 | 0.772 | 0.061 |
| MUTAG | GINE | IntegratedGradients | scaffold | 2 | 53 | 0.868 | 0.900 | 0.528 | 0.358 | 0.975 | 0.562 | 0.698 | 0.215 | 0.253 | 0.772 | 0.059 |
| MUTAG | GINE | PGExplainer | random | 0 | 58 | 0.534 | 0.823 | 0.996 | 0.993 | 0.953 | -0.279 | 0.310 | -0.001 | -0.006 | 0.767 | 0.048 |
| MUTAG | GINE | PGExplainer | random | 1 | 58 | 0.810 | 0.928 | 0.743 | 0.572 | 0.999 | 0.152 | 0.448 | 0.361 | 0.453 | 0.730 | 0.154 |
| MUTAG | GINE | PGExplainer | random | 2 | 58 | 0.897 | 0.985 | 0.251 | 0.234 | 0.983 | -0.351 | 0.241 | 0.379 | 0.430 | 0.647 | 0.065 |
| MUTAG | GINE | PGExplainer | scaffold | 0 | 53 | 0.830 | 0.912 | 0.039 | 0.191 | 1.000 | 0.204 | 0.264 | 0.142 | 0.375 | 0.763 | 0.177 |
| MUTAG | GINE | PGExplainer | scaffold | 1 | 53 | 0.585 | 0.910 | 0.988 | 0.974 | 0.987 | -0.379 | 0.340 | 0.001 | -0.001 | 0.764 | 0.061 |
| MUTAG | GINE | PGExplainer | scaffold | 2 | 53 | 0.868 | 0.900 | 0.981 | 0.952 | 0.986 | 0.214 | 0.698 | 0.097 | 0.238 | 0.641 | 0.059 |
| MUTAG | GINE | Saliency | random | 0 | 58 | 0.534 | 0.823 | 0.029 | 0.171 | 0.979 | -0.293 | 0.310 | -0.004 | -0.006 | 0.773 | 0.048 |
| MUTAG | GINE | Saliency | random | 1 | 58 | 0.810 | 0.928 | 0.006 | 0.163 | 0.971 | 0.035 | 0.448 | 0.391 | 0.463 | 0.769 | 0.154 |
| MUTAG | GINE | Saliency | random | 2 | 58 | 0.897 | 0.985 | 0.002 | 0.160 | 0.975 | -0.195 | 0.190 | 0.494 | 0.610 | 0.772 | 0.065 |
| MUTAG | GINE | Saliency | scaffold | 0 | 53 | 0.830 | 0.912 | 0.009 | 0.134 | 0.999 | 0.358 | 0.321 | 0.221 | 0.375 | 0.771 | 0.177 |
| MUTAG | GINE | Saliency | scaffold | 1 | 53 | 0.585 | 0.910 | 0.101 | 0.158 | 0.990 | -0.289 | 0.340 | 0.000 | -0.001 | 0.773 | 0.061 |
| MUTAG | GINE | Saliency | scaffold | 2 | 53 | 0.868 | 0.900 | 0.014 | 0.134 | 0.996 | 0.532 | 0.698 | 0.198 | 0.246 | 0.772 | 0.059 |
| MUTAG | GINE | SubgraphX | random | 0 | 58 | 0.534 | 0.823 | 0.342 | 0.256 | 1.000 | -0.078 | 0.379 | -0.006 | 0.002 | 0.465 | 0.048 |
| MUTAG | GINE | SubgraphX | random | 1 | 58 | 0.810 | 0.928 | 0.489 | 0.433 | 1.000 | 0.127 | 0.483 | 0.492 | 0.084 | 0.314 | 0.154 |
| MUTAG | GINE | SubgraphX | random | 2 | 58 | 0.897 | 0.985 | 0.348 | 0.234 | 0.996 | -0.154 | 0.293 | 0.342 | -0.000 | 0.160 | 0.065 |
| MUTAG | GINE | SubgraphX | scaffold | 0 | 53 | 0.830 | 0.912 | 0.350 | 0.221 | 1.000 | 0.242 | 0.245 | 0.329 | 0.068 | 0.219 | 0.177 |
| MUTAG | GINE | SubgraphX | scaffold | 1 | 53 | 0.585 | 0.910 | 0.353 | 0.191 | 1.000 | -0.025 | 0.264 | -0.003 | 0.007 | 0.366 | 0.061 |
| MUTAG | GINE | SubgraphX | scaffold | 2 | 53 | 0.868 | 0.900 | 0.452 | 0.283 | 1.000 | 0.540 | 0.377 | 0.216 | 0.193 | 0.592 | 0.059 |
| MUTAG | MPNN | IntegratedGradients | random | 0 | 58 | 0.862 | 0.677 | 0.144 | 0.191 | 0.964 | -0.043 | 0.259 | 0.191 | 0.204 | 0.772 | 0.227 |
| MUTAG | MPNN | IntegratedGradients | random | 1 | 58 | 0.724 | 0.708 | 0.038 | 0.167 | 0.971 | 0.586 | 0.293 | 0.704 | 0.710 | 0.769 | 0.154 |
| MUTAG | MPNN | IntegratedGradients | random | 2 | 58 | 0.776 | 0.780 | 0.127 | 0.186 | 0.959 | 0.532 | 0.690 | 0.623 | 0.635 | 0.771 | 0.081 |
| MUTAG | MPNN | IntegratedGradients | scaffold | 0 | 53 | 0.830 | 0.879 | 0.706 | 0.490 | 0.981 | 0.715 | 0.585 | 0.301 | 0.367 | 0.770 | 0.222 |
| MUTAG | MPNN | IntegratedGradients | scaffold | 1 | 53 | 0.245 | 0.708 | 0.951 | 0.874 | 0.969 | -0.598 | 0.019 | -0.001 | -0.008 | 0.774 | 0.256 |
| MUTAG | MPNN | IntegratedGradients | scaffold | 2 | 53 | 0.830 | 0.885 | 0.124 | 0.198 | 0.991 | 0.327 | 0.698 | 0.005 | 0.010 | 0.770 | 0.323 |
| MolMotif | AttentiveFP | IntegratedGradients | random | 0 | 200 | 0.985 | 0.999 | 0.987 | 0.964 | 0.807 | 0.666 | 0.780 | 0.525 | 0.026 | 0.772 | 0.007 |
| MolMotif | AttentiveFP | IntegratedGradients | random | 1 | 200 | 0.910 | 0.991 | 0.928 | 0.838 | 0.738 | 0.335 | 0.555 | 0.360 | 0.031 | 0.768 | 0.055 |
| MolMotif | AttentiveFP | IntegratedGradients | random | 2 | 200 | 0.970 | 0.999 | 0.986 | 0.967 | 0.792 | 0.486 | 0.595 | 0.522 | 0.017 | 0.770 | 0.017 |
| MolMotif | AttentiveFP | IntegratedGradients | scaffold | 0 | 200 | 0.995 | 1.000 | 0.980 | 0.949 | 0.782 | 0.735 | 0.840 | 0.496 | 0.034 | 0.773 | 0.004 |
| MolMotif | AttentiveFP | IntegratedGradients | scaffold | 1 | 200 | 0.990 | 1.000 | 0.925 | 0.848 | 0.768 | 0.723 | 0.730 | 0.513 | 0.025 | 0.768 | 0.011 |
| MolMotif | AttentiveFP | IntegratedGradients | scaffold | 2 | 200 | 0.990 | 0.999 | 0.995 | 0.981 | 0.797 | 0.521 | 0.570 | 0.503 | 0.019 | 0.775 | 0.012 |
| MolMotif | GAT | IntegratedGradients | random | 0 | 200 | 1.000 | 1.000 | 0.796 | 0.709 | 0.707 | 0.246 | 0.480 | 0.401 | 0.417 | 0.772 | 0.008 |
| MolMotif | GAT | IntegratedGradients | random | 1 | 200 | 1.000 | 1.000 | 0.996 | 0.989 | 0.762 | 0.728 | 0.800 | 0.429 | 0.019 | 0.772 | 0.006 |
| MolMotif | GAT | IntegratedGradients | random | 2 | 200 | 1.000 | 1.000 | 0.733 | 0.631 | 0.716 | 0.040 | 0.375 | 0.491 | 0.240 | 0.772 | 0.004 |
| MolMotif | GAT | IntegratedGradients | scaffold | 0 | 200 | 0.965 | 0.998 | 0.679 | 0.578 | 0.702 | 0.208 | 0.490 | 0.401 | 0.418 | 0.777 | 0.025 |
| MolMotif | GAT | IntegratedGradients | scaffold | 1 | 200 | 0.975 | 0.999 | 0.946 | 0.859 | 0.767 | 0.573 | 0.655 | 0.445 | 0.354 | 0.773 | 0.016 |
| MolMotif | GAT | IntegratedGradients | scaffold | 2 | 200 | 0.990 | 1.000 | 0.873 | 0.774 | 0.722 | 0.156 | 0.470 | 0.653 | 0.406 | 0.775 | 0.007 |
| MolMotif | GCN | IntegratedGradients | random | 0 | 200 | 0.970 | 1.000 | 0.998 | 0.994 | 0.777 | 0.042 | 0.375 | 0.447 | 0.447 | 0.768 | 0.020 |
| MolMotif | GCN | IntegratedGradients | random | 1 | 200 | 0.680 | 0.999 | 0.982 | 0.957 | 0.811 | 0.473 | 0.675 | 0.110 | 0.623 | 0.770 | 0.236 |
| MolMotif | GCN | IntegratedGradients | random | 2 | 200 | 0.965 | 0.988 | 0.850 | 0.735 | 0.811 | -0.013 | 0.465 | 0.414 | 0.420 | 0.768 | 0.039 |
| MolMotif | GCN | IntegratedGradients | scaffold | 0 | 200 | 0.980 | 0.999 | 0.958 | 0.914 | 0.851 | 0.106 | 0.385 | 0.467 | 0.423 | 0.770 | 0.012 |
| MolMotif | GCN | IntegratedGradients | scaffold | 1 | 200 | 0.965 | 0.999 | 0.965 | 0.901 | 0.819 | 0.146 | 0.470 | 0.407 | 0.459 | 0.773 | 0.037 |
| MolMotif | GCN | IntegratedGradients | scaffold | 2 | 200 | 0.950 | 1.000 | 0.893 | 0.708 | 0.837 | 0.178 | 0.445 | 0.300 | 0.446 | 0.772 | 0.020 |
| MolMotif | GINE | GNNExplainer | random | 0 | 200 | 0.975 | 0.999 | 0.683 | 0.473 | 0.824 | -0.183 | 0.200 | 0.186 | 0.224 | 0.779 | 0.020 |
| MolMotif | GINE | GNNExplainer | random | 1 | 200 | 0.810 | 1.000 | 0.610 | 0.390 | 0.821 | 0.101 | 0.440 | 0.383 | 0.276 | 0.779 | 0.106 |
| MolMotif | GINE | GNNExplainer | random | 2 | 200 | 1.000 | 1.000 | 0.630 | 0.448 | 0.835 | 0.030 | 0.380 | -0.018 | 0.387 | 0.778 | 0.003 |
| MolMotif | GINE | GNNExplainer | scaffold | 0 | 200 | 0.985 | 1.000 | 0.591 | 0.418 | 0.817 | 0.022 | 0.495 | 0.297 | 0.414 | 0.780 | 0.012 |
| MolMotif | GINE | GNNExplainer | scaffold | 1 | 200 | 0.985 | 1.000 | 0.589 | 0.417 | 0.814 | -0.009 | 0.485 | 0.300 | 0.443 | 0.780 | 0.010 |
| MolMotif | GINE | GNNExplainer | scaffold | 2 | 200 | 0.910 | 1.000 | 0.610 | 0.425 | 0.814 | -0.049 | 0.215 | -0.021 | 0.259 | 0.780 | 0.018 |
| MolMotif | GINE | GuidedBackprop | random | 0 | 200 | 0.975 | 0.999 | 0.981 | 0.956 | 0.854 | -0.202 | 0.270 | 0.169 | 0.132 | 0.772 | 0.020 |
| MolMotif | GINE | GuidedBackprop | random | 1 | 200 | 0.810 | 1.000 | 0.935 | 0.835 | 0.826 | 0.007 | 0.405 | 0.116 | 0.429 | 0.772 | 0.106 |
| MolMotif | GINE | GuidedBackprop | random | 2 | 200 | 1.000 | 1.000 | 0.998 | 0.993 | 0.823 | -0.144 | 0.345 | 0.330 | 0.318 | 0.770 | 0.003 |
| MolMotif | GINE | GuidedBackprop | scaffold | 0 | 200 | 0.985 | 1.000 | 0.994 | 0.980 | 0.844 | -0.025 | 0.465 | 0.321 | 0.410 | 0.773 | 0.012 |
| MolMotif | GINE | GuidedBackprop | scaffold | 1 | 200 | 0.985 | 1.000 | 0.995 | 0.979 | 0.821 | -0.078 | 0.450 | 0.251 | 0.433 | 0.773 | 0.010 |
| MolMotif | GINE | GuidedBackprop | scaffold | 2 | 200 | 0.910 | 1.000 | 0.882 | 0.849 | 0.814 | -0.270 | 0.235 | 0.214 | 0.191 | 0.774 | 0.018 |
| MolMotif | GINE | InputXGradient | random | 0 | 200 | 0.975 | 0.999 | 0.986 | 0.971 | 0.822 | -0.285 | 0.245 | 0.040 | 0.164 | 0.773 | 0.020 |
| MolMotif | GINE | InputXGradient | random | 1 | 200 | 0.810 | 1.000 | 1.000 | 0.998 | 0.773 | -0.140 | 0.315 | 0.087 | 0.414 | 0.772 | 0.106 |
| MolMotif | GINE | InputXGradient | random | 2 | 200 | 1.000 | 1.000 | 0.999 | 0.997 | 0.810 | -0.112 | 0.445 | 0.312 | 0.322 | 0.768 | 0.003 |
| MolMotif | GINE | InputXGradient | scaffold | 0 | 200 | 0.985 | 1.000 | 0.999 | 0.998 | 0.830 | -0.045 | 0.460 | 0.246 | 0.415 | 0.774 | 0.012 |
| MolMotif | GINE | InputXGradient | scaffold | 1 | 200 | 0.985 | 1.000 | 0.996 | 0.985 | 0.849 | -0.097 | 0.450 | 0.258 | 0.436 | 0.774 | 0.010 |
| MolMotif | GINE | InputXGradient | scaffold | 2 | 200 | 0.910 | 1.000 | 0.999 | 0.995 | 0.758 | -0.255 | 0.190 | 0.205 | 0.170 | 0.774 | 0.018 |
| MolMotif | GINE | IntegratedGradients | random | 0 | 200 | 0.975 | 0.999 | 0.919 | 0.813 | 0.876 | -0.166 | 0.225 | 0.250 | 0.077 | 0.770 | 0.020 |
| MolMotif | GINE | IntegratedGradients | random | 1 | 200 | 0.810 | 1.000 | 0.963 | 0.903 | 0.870 | 0.146 | 0.440 | 0.463 | 0.257 | 0.771 | 0.106 |
| MolMotif | GINE | IntegratedGradients | random | 2 | 200 | 1.000 | 1.000 | 0.972 | 0.910 | 0.860 | 0.007 | 0.405 | 0.311 | 0.319 | 0.768 | 0.003 |
| MolMotif | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.985 | 1.000 | 0.830 | 0.676 | 0.860 | -0.011 | 0.495 | 0.333 | 0.415 | 0.773 | 0.012 |
| MolMotif | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.985 | 1.000 | 0.806 | 0.613 | 0.868 | -0.022 | 0.485 | 0.309 | 0.435 | 0.773 | 0.010 |
| MolMotif | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.910 | 1.000 | 0.984 | 0.937 | 0.815 | -0.091 | 0.230 | 0.270 | 0.099 | 0.773 | 0.018 |
| MolMotif | GINE | PGExplainer | random | 0 | 200 | 0.975 | 0.999 | 0.649 | 0.443 | 0.709 | -0.079 | 0.235 | 0.164 | 0.097 | 0.410 | 0.020 |
| MolMotif | GINE | PGExplainer | random | 1 | 200 | 0.810 | 1.000 | 0.273 | 0.218 | 0.909 | -0.215 | 0.240 | 0.090 | 0.428 | 0.768 | 0.106 |
| MolMotif | GINE | PGExplainer | random | 2 | 200 | 1.000 | 1.000 | 0.584 | 0.343 | 0.897 | 0.001 | 0.310 | 0.143 | 0.381 | 0.702 | 0.003 |
| MolMotif | GINE | PGExplainer | scaffold | 0 | 200 | 0.985 | 1.000 | 0.716 | 0.560 | 0.448 | -0.714 | 0.040 | -0.027 | 0.445 | 0.551 | 0.012 |
| MolMotif | GINE | PGExplainer | scaffold | 1 | 200 | 0.985 | 1.000 | 0.499 | 0.219 | 0.053 | -0.025 | 0.090 | 0.042 | 0.404 | 0.945 | 0.010 |
| MolMotif | GINE | PGExplainer | scaffold | 2 | 200 | 0.910 | 1.000 | 0.240 | 0.199 | 0.911 | -0.031 | 0.180 | 0.125 | 0.236 | 0.774 | 0.018 |
| MolMotif | GINE | Saliency | random | 0 | 200 | 0.975 | 0.999 | 0.990 | 0.981 | 0.826 | -0.253 | 0.260 | 0.065 | 0.167 | 0.771 | 0.020 |
| MolMotif | GINE | Saliency | random | 1 | 200 | 0.810 | 1.000 | 0.999 | 0.996 | 0.772 | -0.123 | 0.305 | 0.099 | 0.415 | 0.772 | 0.106 |
| MolMotif | GINE | Saliency | random | 2 | 200 | 1.000 | 1.000 | 0.994 | 0.985 | 0.802 | -0.117 | 0.425 | 0.318 | 0.317 | 0.772 | 0.003 |
| MolMotif | GINE | Saliency | scaffold | 0 | 200 | 0.985 | 1.000 | 0.999 | 0.996 | 0.822 | -0.065 | 0.455 | 0.242 | 0.415 | 0.774 | 0.012 |
| MolMotif | GINE | Saliency | scaffold | 1 | 200 | 0.985 | 1.000 | 0.995 | 0.983 | 0.841 | -0.084 | 0.465 | 0.254 | 0.439 | 0.774 | 0.010 |
| MolMotif | GINE | Saliency | scaffold | 2 | 200 | 0.910 | 1.000 | 0.998 | 0.994 | 0.751 | -0.269 | 0.185 | 0.220 | 0.179 | 0.775 | 0.018 |
| MolMotif | GINE | SubgraphX | random | 0 | 200 | 0.975 | 0.999 | 0.573 | 0.354 | 0.977 | -0.086 | 0.265 | 0.129 | 0.160 | 0.356 | 0.020 |
| MolMotif | GINE | SubgraphX | random | 1 | 200 | 0.810 | 1.000 | 0.535 | 0.303 | 0.983 | -0.008 | 0.205 | 0.358 | 0.166 | 0.308 | 0.106 |
| MolMotif | GINE | SubgraphX | random | 2 | 200 | 1.000 | 1.000 | 0.556 | 0.323 | 0.977 | -0.013 | 0.320 | 0.159 | 0.320 | 0.390 | 0.003 |
| MolMotif | GINE | SubgraphX | scaffold | 0 | 200 | 0.985 | 1.000 | 0.475 | 0.261 | 0.918 | 0.018 | 0.365 | 0.418 | 0.390 | 0.306 | 0.012 |
| MolMotif | GINE | SubgraphX | scaffold | 1 | 200 | 0.985 | 1.000 | 0.490 | 0.273 | 0.940 | 0.052 | 0.415 | 0.369 | 0.409 | 0.312 | 0.010 |
| MolMotif | GINE | SubgraphX | scaffold | 2 | 200 | 0.910 | 1.000 | 0.513 | 0.305 | 0.969 | -0.084 | 0.195 | 0.147 | 0.182 | 0.406 | 0.018 |
| MolMotif | MPNN | IntegratedGradients | random | 0 | 200 | 1.000 | 1.000 | 0.783 | 0.569 | 0.915 | -0.256 | 0.315 | 0.293 | 0.277 | 0.770 | 0.004 |
| MolMotif | MPNN | IntegratedGradients | random | 1 | 200 | 1.000 | 1.000 | 0.874 | 0.755 | 0.926 | -0.060 | 0.395 | 0.388 | 0.308 | 0.770 | 0.007 |
| MolMotif | MPNN | IntegratedGradients | random | 2 | 200 | 1.000 | 1.000 | 0.962 | 0.863 | 0.860 | -0.057 | 0.460 | 0.451 | 0.457 | 0.772 | 0.002 |
| MolMotif | MPNN | IntegratedGradients | scaffold | 0 | 200 | 0.970 | 0.994 | 0.772 | 0.516 | 0.908 | -0.203 | 0.325 | 0.294 | 0.262 | 0.774 | 0.021 |
| MolMotif | MPNN | IntegratedGradients | scaffold | 1 | 200 | 0.975 | 0.993 | 0.793 | 0.573 | 0.915 | -0.049 | 0.470 | 0.332 | 0.376 | 0.774 | 0.014 |
| MolMotif | MPNN | IntegratedGradients | scaffold | 2 | 200 | 0.980 | 0.998 | 0.940 | 0.778 | 0.865 | -0.019 | 0.440 | 0.341 | 0.423 | 0.777 | 0.014 |
| SIDER | GCN | IntegratedGradients | random | 0 | 200 | 0.675 | 0.677 | — | — | 0.748 | 0.514 | 0.720 | 0.145 | 0.252 | 0.751 | 0.050 |
| SIDER | GCN | IntegratedGradients | random | 1 | 200 | 0.625 | 0.636 | — | — | 0.737 | 0.074 | 0.555 | 0.070 | 0.085 | 0.759 | 0.085 |
| SIDER | GCN | IntegratedGradients | random | 2 | 200 | 0.630 | 0.668 | — | — | 0.746 | -0.110 | 0.430 | 0.084 | 0.022 | 0.751 | 0.048 |
| SIDER | GCN | IntegratedGradients | scaffold | 0 | 200 | 0.600 | 0.663 | — | — | 0.716 | 0.101 | 0.580 | 0.102 | 0.173 | 0.773 | 0.054 |
| SIDER | GCN | IntegratedGradients | scaffold | 1 | 200 | 0.650 | 0.673 | — | — | 0.746 | 0.294 | 0.655 | 0.094 | 0.215 | 0.771 | 0.035 |
| SIDER | GCN | IntegratedGradients | scaffold | 2 | 200 | 0.570 | 0.645 | — | — | 0.704 | -0.137 | 0.435 | 0.003 | 0.021 | 0.770 | 0.029 |
| SIDER | GINE | IntegratedGradients | random | 0 | 200 | 0.665 | 0.682 | — | — | 0.782 | 0.526 | 0.675 | 0.159 | 0.304 | 0.752 | 0.049 |
| SIDER | GINE | IntegratedGradients | random | 1 | 200 | 0.615 | 0.628 | — | — | 0.746 | -0.122 | 0.445 | 0.030 | 0.030 | 0.761 | 0.085 |
| SIDER | GINE | IntegratedGradients | random | 2 | 200 | 0.645 | 0.703 | — | — | 0.764 | 0.427 | 0.720 | 0.333 | 0.389 | 0.754 | 0.077 |
| SIDER | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.600 | 0.650 | — | — | 0.818 | 0.739 | 0.775 | 0.068 | 0.093 | 0.774 | 0.072 |
| SIDER | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.625 | 0.656 | — | — | 0.720 | 0.290 | 0.450 | 0.080 | 0.168 | 0.774 | 0.059 |
| SIDER | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.585 | 0.668 | — | — | 0.707 | -0.032 | 0.460 | 0.084 | 0.098 | 0.772 | 0.028 |
| ShapeGGen | GINE | GNNExplainer | random | 0 | 50 | 0.740 | 0.667 | 0.555 | 0.613 | 0.092 | 0.470 | 0.280 | 0.410 | 0.251 | 0.770 | 0.143 |
| ShapeGGen | GINE | GNNExplainer | random | 1 | 50 | 0.820 | 0.455 | 0.610 | 0.646 | 0.083 | 0.544 | 0.260 | 0.305 | 0.207 | 0.772 | 0.202 |
| ShapeGGen | GINE | GNNExplainer | random | 2 | 50 | 0.780 | 0.613 | 0.483 | 0.514 | 0.069 | 0.154 | 0.100 | 0.003 | 0.008 | 0.776 | 0.233 |
| ShapeGGen | GINE | GuidedBackprop | random | 0 | 50 | 0.740 | 0.667 | 0.754 | 0.825 | 0.186 | 0.424 | 0.420 | 0.359 | 0.294 | 0.770 | 0.143 |
| ShapeGGen | GINE | GuidedBackprop | random | 1 | 50 | 0.820 | 0.455 | 0.775 | 0.797 | 0.175 | 0.555 | 0.540 | 0.349 | 0.187 | 0.772 | 0.202 |
| ShapeGGen | GINE | GuidedBackprop | random | 2 | 50 | 0.780 | 0.613 | 0.791 | 0.810 | 0.160 | 0.465 | 0.460 | 0.008 | 0.003 | 0.776 | 0.233 |
| ShapeGGen | GINE | InputXGradient | random | 0 | 50 | 0.740 | 0.667 | 0.724 | 0.791 | 0.201 | 0.378 | 0.400 | 0.407 | 0.270 | 0.770 | 0.143 |
| ShapeGGen | GINE | InputXGradient | random | 1 | 50 | 0.820 | 0.455 | 0.718 | 0.753 | 0.188 | 0.453 | 0.580 | 0.334 | 0.239 | 0.772 | 0.202 |
| ShapeGGen | GINE | InputXGradient | random | 2 | 50 | 0.780 | 0.613 | 0.732 | 0.747 | 0.174 | 0.473 | 0.540 | 0.008 | 0.003 | 0.776 | 0.233 |
| ShapeGGen | GINE | IntegratedGradients | random | 0 | 50 | 0.740 | 0.667 | 0.732 | 0.787 | 0.194 | 0.375 | 0.420 | 0.412 | 0.259 | 0.770 | 0.143 |
| ShapeGGen | GINE | IntegratedGradients | random | 1 | 50 | 0.820 | 0.455 | 0.716 | 0.755 | 0.180 | 0.469 | 0.600 | 0.378 | 0.199 | 0.772 | 0.202 |
| ShapeGGen | GINE | IntegratedGradients | random | 2 | 50 | 0.780 | 0.613 | 0.751 | 0.770 | 0.172 | 0.497 | 0.580 | 0.008 | 0.003 | 0.776 | 0.233 |
| ShapeGGen | GINE | PGExplainer | random | 0 | 50 | 0.740 | 0.667 | 0.503 | 0.541 | 0.349 | -0.098 | 0.020 | 0.236 | 0.316 | 0.589 | 0.143 |
| ShapeGGen | GINE | PGExplainer | random | 1 | 50 | 0.820 | 0.455 | 0.506 | 0.509 | 0.222 | -0.223 | 0.020 | 0.142 | 0.572 | 0.749 | 0.202 |
| ShapeGGen | GINE | PGExplainer | random | 2 | 50 | 0.780 | 0.613 | 0.489 | 0.520 | 0.429 | -0.167 | 0.000 | 0.002 | 0.009 | 0.698 | 0.233 |
| ShapeGGen | GINE | Saliency | random | 0 | 50 | 0.740 | 0.667 | 0.762 | 0.825 | 0.186 | 0.336 | 0.400 | 0.349 | 0.313 | 0.770 | 0.143 |
| ShapeGGen | GINE | Saliency | random | 1 | 50 | 0.820 | 0.455 | 0.776 | 0.803 | 0.173 | 0.439 | 0.520 | 0.329 | 0.256 | 0.772 | 0.202 |
| ShapeGGen | GINE | Saliency | random | 2 | 50 | 0.780 | 0.613 | 0.769 | 0.795 | 0.159 | 0.425 | 0.400 | 0.007 | 0.003 | 0.776 | 0.233 |
| ShapeGGen | GINE | SubgraphX | random | 0 | 50 | 0.740 | 0.667 | 0.676 | 0.637 | 0.198 | 0.552 | 0.080 | 0.527 | -0.002 | 0.461 | 0.143 |
| ShapeGGen | GINE | SubgraphX | random | 1 | 50 | 0.820 | 0.455 | 0.637 | 0.571 | 0.151 | 0.607 | 0.040 | 0.671 | -0.028 | 0.522 | 0.202 |
| ShapeGGen | GINE | SubgraphX | random | 2 | 50 | 0.780 | 0.613 | 0.620 | 0.568 | 0.180 | 0.471 | 0.180 | 0.011 | -0.000 | 0.567 | 0.233 |
| SynthMotifs | AttentiveFP | IntegratedGradients | random | 0 | 200 | 0.975 | 1.000 | 0.776 | 0.601 | 0.205 | 0.004 | 0.305 | 0.489 | 0.394 | 0.795 | 0.013 |
| SynthMotifs | AttentiveFP | IntegratedGradients | random | 1 | 200 | 0.985 | 0.997 | 0.940 | 0.828 | 0.223 | 0.448 | 0.535 | 0.464 | 0.092 | 0.797 | 0.009 |
| SynthMotifs | AttentiveFP | IntegratedGradients | random | 2 | 200 | 0.980 | 1.000 | 0.898 | 0.733 | 0.146 | 0.104 | 0.120 | 0.369 | 0.204 | 0.796 | 0.020 |
| SynthMotifs | AttentiveFP | IntegratedGradients | scaffold | 0 | 200 | 0.905 | 0.970 | 0.875 | 0.621 | 0.124 | -0.066 | 0.190 | 0.308 | 0.270 | 0.796 | 0.124 |
| SynthMotifs | AttentiveFP | IntegratedGradients | scaffold | 1 | 200 | 0.890 | 0.999 | 0.820 | 0.607 | 0.173 | 0.345 | 0.480 | 0.362 | 0.275 | 0.795 | 0.049 |
| SynthMotifs | AttentiveFP | IntegratedGradients | scaffold | 2 | 200 | 0.820 | 0.999 | 0.957 | 0.855 | 0.146 | 0.312 | 0.285 | 0.487 | 0.082 | 0.795 | 0.019 |
| SynthMotifs | GAT | IntegratedGradients | random | 0 | 200 | 0.995 | 1.000 | 0.920 | 0.753 | 0.123 | 0.367 | 0.255 | 0.322 | 0.168 | 0.795 | 0.023 |
| SynthMotifs | GAT | IntegratedGradients | random | 1 | 200 | 0.980 | 1.000 | 0.816 | 0.675 | 0.175 | 0.129 | 0.075 | 0.216 | 0.139 | 0.795 | 0.009 |
| SynthMotifs | GAT | IntegratedGradients | random | 2 | 200 | 0.995 | 1.000 | 0.642 | 0.553 | 0.119 | 0.230 | 0.025 | 0.315 | 0.319 | 0.792 | 0.013 |
| SynthMotifs | GAT | IntegratedGradients | scaffold | 0 | 200 | 0.955 | 0.990 | 0.601 | 0.445 | 0.191 | 0.151 | 0.145 | 0.078 | 0.056 | 0.792 | 0.281 |
| SynthMotifs | GAT | IntegratedGradients | scaffold | 1 | 200 | 0.995 | 1.000 | 0.950 | 0.797 | 0.115 | 0.006 | 0.165 | 0.415 | 0.231 | 0.796 | 0.004 |
| SynthMotifs | GAT | IntegratedGradients | scaffold | 2 | 200 | 0.995 | 1.000 | 0.910 | 0.836 | 0.107 | 0.368 | 0.190 | 0.497 | 0.248 | 0.793 | 0.010 |
| SynthMotifs | GCN | IntegratedGradients | random | 0 | 200 | 0.695 | 1.000 | 0.583 | 0.407 | 0.103 | 0.421 | 0.200 | 0.146 | 0.167 | 0.795 | 0.242 |
| SynthMotifs | GCN | IntegratedGradients | random | 1 | 200 | 0.980 | 1.000 | 0.983 | 0.931 | 0.152 | 0.390 | 0.675 | 0.379 | 0.147 | 0.796 | 0.011 |
| SynthMotifs | GCN | IntegratedGradients | random | 2 | 200 | 0.990 | 1.000 | 0.990 | 0.962 | 0.169 | 0.433 | 0.705 | 0.443 | 0.062 | 0.798 | 0.009 |
| SynthMotifs | GCN | IntegratedGradients | scaffold | 0 | 200 | 0.635 | 1.000 | 0.988 | 0.938 | 0.151 | 0.345 | 0.295 | 0.255 | 0.185 | 0.797 | 0.165 |
| SynthMotifs | GCN | IntegratedGradients | scaffold | 1 | 200 | 0.970 | 0.998 | 0.946 | 0.805 | 0.143 | 0.352 | 0.620 | 0.250 | 0.165 | 0.796 | 0.023 |
| SynthMotifs | GCN | IntegratedGradients | scaffold | 2 | 200 | 0.985 | 0.997 | 0.936 | 0.797 | 0.141 | 0.366 | 0.685 | 0.240 | 0.166 | 0.796 | 0.014 |
| SynthMotifs | GINE | GNNExplainer | random | 0 | 200 | 0.985 | 1.000 | 0.564 | 0.293 | 0.037 | 0.068 | 0.055 | 0.197 | 0.221 | 0.800 | 0.000 |
| SynthMotifs | GINE | GNNExplainer | random | 1 | 200 | 0.985 | 1.000 | 0.635 | 0.397 | 0.046 | 0.103 | 0.095 | 0.283 | 0.282 | 0.800 | 0.009 |
| SynthMotifs | GINE | GNNExplainer | random | 2 | 200 | 0.945 | 1.000 | 0.698 | 0.474 | 0.048 | 0.199 | 0.045 | 0.217 | 0.251 | 0.800 | 0.020 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 0 | 200 | 0.900 | 1.000 | 0.672 | 0.350 | 0.053 | 0.003 | 0.025 | 0.180 | 0.194 | 0.800 | 0.029 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 1 | 200 | 1.000 | 1.000 | 0.544 | 0.270 | 0.040 | 0.052 | 0.030 | 0.280 | 0.357 | 0.800 | 0.003 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 2 | 200 | 0.915 | 1.000 | 0.796 | 0.496 | 0.051 | 0.206 | 0.085 | 0.331 | 0.322 | 0.800 | 0.030 |
| SynthMotifs | GINE | GuidedBackprop | random | 0 | 200 | 0.985 | 1.000 | 0.999 | 0.996 | 0.178 | 0.645 | 0.475 | 0.235 | 0.081 | 0.800 | 0.000 |
| SynthMotifs | GINE | GuidedBackprop | random | 1 | 200 | 0.985 | 1.000 | 0.989 | 0.969 | 0.157 | 0.662 | 0.255 | 0.321 | 0.043 | 0.799 | 0.009 |
| SynthMotifs | GINE | GuidedBackprop | random | 2 | 200 | 0.945 | 1.000 | 0.996 | 0.983 | 0.164 | 0.613 | 0.350 | 0.261 | 0.059 | 0.800 | 0.020 |
| SynthMotifs | GINE | GuidedBackprop | scaffold | 0 | 200 | 0.900 | 1.000 | 0.913 | 0.719 | 0.113 | 0.266 | 0.455 | 0.206 | 0.103 | 0.795 | 0.029 |
| SynthMotifs | GINE | GuidedBackprop | scaffold | 1 | 200 | 1.000 | 1.000 | 0.999 | 0.995 | 0.161 | 0.777 | 0.160 | 0.349 | 0.107 | 0.800 | 0.003 |
| SynthMotifs | GINE | GuidedBackprop | scaffold | 2 | 200 | 0.915 | 1.000 | 0.982 | 0.952 | 0.143 | 0.628 | 0.640 | 0.345 | 0.033 | 0.800 | 0.030 |
| SynthMotifs | GINE | InputXGradient | random | 0 | 200 | 0.985 | 1.000 | 0.987 | 0.956 | 0.194 | 0.488 | 0.220 | 0.244 | 0.109 | 0.798 | 0.000 |
| SynthMotifs | GINE | InputXGradient | random | 1 | 200 | 0.985 | 1.000 | 0.963 | 0.872 | 0.229 | 0.439 | 0.170 | 0.314 | 0.092 | 0.793 | 0.009 |
| SynthMotifs | GINE | InputXGradient | random | 2 | 200 | 0.945 | 1.000 | 0.959 | 0.870 | 0.238 | 0.498 | 0.150 | 0.261 | 0.132 | 0.795 | 0.020 |
| SynthMotifs | GINE | InputXGradient | scaffold | 0 | 200 | 0.900 | 1.000 | 0.951 | 0.826 | 0.183 | 0.247 | 0.110 | 0.228 | 0.113 | 0.796 | 0.029 |
| SynthMotifs | GINE | InputXGradient | scaffold | 1 | 200 | 1.000 | 1.000 | 0.977 | 0.921 | 0.199 | 0.624 | 0.125 | 0.352 | 0.142 | 0.798 | 0.003 |
| SynthMotifs | GINE | InputXGradient | scaffold | 2 | 200 | 0.915 | 1.000 | 0.982 | 0.926 | 0.180 | 0.456 | 0.110 | 0.338 | 0.122 | 0.797 | 0.030 |
| SynthMotifs | GINE | IntegratedGradients | random | 0 | 200 | 0.985 | 1.000 | 0.997 | 0.987 | 0.194 | 0.490 | 0.425 | 0.233 | 0.090 | 0.800 | 0.000 |
| SynthMotifs | GINE | IntegratedGradients | random | 1 | 200 | 0.985 | 1.000 | 0.996 | 0.980 | 0.198 | 0.448 | 0.490 | 0.307 | 0.066 | 0.799 | 0.009 |
| SynthMotifs | GINE | IntegratedGradients | random | 2 | 200 | 0.945 | 1.000 | 0.977 | 0.912 | 0.162 | 0.479 | 0.510 | 0.256 | 0.129 | 0.799 | 0.020 |
| SynthMotifs | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.900 | 1.000 | 0.889 | 0.640 | 0.132 | 0.272 | 0.490 | 0.272 | 0.085 | 0.795 | 0.029 |
| SynthMotifs | GINE | IntegratedGradients | scaffold | 1 | 200 | 1.000 | 1.000 | 0.992 | 0.970 | 0.223 | 0.611 | 0.175 | 0.340 | 0.135 | 0.799 | 0.003 |
| SynthMotifs | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.915 | 1.000 | 0.978 | 0.927 | 0.163 | 0.517 | 0.445 | 0.353 | 0.051 | 0.798 | 0.030 |
| SynthMotifs | GINE | PGExplainer | random | 0 | 200 | 0.985 | 1.000 | 0.460 | 0.192 | 0.303 | -0.078 | 0.015 | 0.138 | 0.114 | 0.434 | 0.000 |
| SynthMotifs | GINE | PGExplainer | random | 1 | 200 | 0.985 | 1.000 | 0.471 | 0.261 | 0.379 | -0.025 | 0.000 | 0.125 | 0.302 | 0.785 | 0.009 |
| SynthMotifs | GINE | PGExplainer | random | 2 | 200 | 0.945 | 1.000 | 0.314 | 0.174 | 0.385 | -0.149 | 0.000 | 0.010 | 0.263 | 0.786 | 0.020 |
| SynthMotifs | GINE | PGExplainer | scaffold | 0 | 200 | 0.900 | 1.000 | 0.536 | 0.277 | 0.364 | 0.090 | 0.025 | 0.154 | 0.213 | 0.612 | 0.029 |
| SynthMotifs | GINE | PGExplainer | scaffold | 1 | 200 | 1.000 | 1.000 | 0.308 | 0.167 | 0.377 | -0.203 | 0.000 | 0.032 | 0.324 | 0.732 | 0.003 |
| SynthMotifs | GINE | PGExplainer | scaffold | 2 | 200 | 0.915 | 1.000 | 0.323 | 0.167 | 0.377 | -0.158 | 0.000 | 0.058 | 0.280 | 0.656 | 0.030 |
| SynthMotifs | GINE | Saliency | random | 0 | 200 | 0.985 | 1.000 | 0.993 | 0.976 | 0.172 | 0.493 | 0.315 | 0.248 | 0.095 | 0.798 | 0.000 |
| SynthMotifs | GINE | Saliency | random | 1 | 200 | 0.985 | 1.000 | 0.983 | 0.934 | 0.197 | 0.460 | 0.150 | 0.311 | 0.080 | 0.797 | 0.009 |
| SynthMotifs | GINE | Saliency | random | 2 | 200 | 0.945 | 1.000 | 0.960 | 0.870 | 0.176 | 0.513 | 0.140 | 0.262 | 0.141 | 0.796 | 0.020 |
| SynthMotifs | GINE | Saliency | scaffold | 0 | 200 | 0.900 | 1.000 | 0.965 | 0.873 | 0.131 | 0.237 | 0.090 | 0.216 | 0.114 | 0.794 | 0.029 |
| SynthMotifs | GINE | Saliency | scaffold | 1 | 200 | 1.000 | 1.000 | 0.983 | 0.950 | 0.172 | 0.606 | 0.095 | 0.344 | 0.148 | 0.796 | 0.003 |
| SynthMotifs | GINE | Saliency | scaffold | 2 | 200 | 0.915 | 1.000 | 0.983 | 0.927 | 0.150 | 0.432 | 0.110 | 0.332 | 0.096 | 0.794 | 0.030 |
| SynthMotifs | GINE | SubgraphX | random | 0 | 200 | 0.985 | 1.000 | 0.642 | 0.430 | 0.175 | 0.308 | 0.030 | 0.181 | 0.088 | 0.578 | 0.000 |
| SynthMotifs | GINE | SubgraphX | random | 1 | 200 | 0.985 | 1.000 | 0.824 | 0.594 | 0.165 | 0.519 | 0.085 | 0.320 | 0.036 | 0.545 | 0.009 |
| SynthMotifs | GINE | SubgraphX | random | 2 | 200 | 0.945 | 1.000 | 0.845 | 0.575 | 0.159 | 0.551 | 0.020 | 0.234 | 0.044 | 0.659 | 0.020 |
| SynthMotifs | GINE | SubgraphX | scaffold | 0 | 200 | 0.900 | 1.000 | 0.604 | 0.353 | 0.262 | -0.019 | 0.035 | 0.200 | 0.020 | 0.289 | 0.029 |
| SynthMotifs | GINE | SubgraphX | scaffold | 1 | 200 | 1.000 | 1.000 | 0.871 | 0.596 | 0.157 | 0.587 | 0.020 | 0.352 | 0.049 | 0.690 | 0.003 |
| SynthMotifs | GINE | SubgraphX | scaffold | 2 | 200 | 0.915 | 1.000 | 0.841 | 0.661 | 0.182 | 0.500 | 0.160 | 0.353 | 0.056 | 0.436 | 0.030 |
| SynthMotifs | MPNN | IntegratedGradients | random | 0 | 200 | 0.985 | 1.000 | 0.812 | 0.651 | 0.115 | 0.300 | 0.410 | 0.411 | 0.412 | 0.795 | 0.025 |
| SynthMotifs | MPNN | IntegratedGradients | random | 1 | 200 | 0.995 | 1.000 | 0.900 | 0.745 | 0.137 | 0.313 | 0.380 | 0.391 | 0.355 | 0.795 | 0.010 |
| SynthMotifs | MPNN | IntegratedGradients | random | 2 | 200 | 1.000 | 1.000 | 0.903 | 0.685 | 0.090 | 0.399 | 0.310 | 0.468 | 0.485 | 0.796 | 0.005 |
| SynthMotifs | MPNN | IntegratedGradients | scaffold | 0 | 200 | 0.595 | 0.980 | 0.698 | 0.385 | 0.272 | 0.575 | 0.475 | 0.455 | 0.222 | 0.794 | 0.196 |
| SynthMotifs | MPNN | IntegratedGradients | scaffold | 1 | 200 | 0.865 | 0.999 | 0.922 | 0.798 | 0.139 | 0.262 | 0.480 | 0.246 | 0.228 | 0.795 | 0.037 |
| SynthMotifs | MPNN | IntegratedGradients | scaffold | 2 | 200 | 0.910 | 0.999 | 0.913 | 0.713 | 0.137 | 0.267 | 0.490 | 0.421 | 0.266 | 0.793 | 0.028 |
| Tox21 | GINE | IntegratedGradients | random | 0 | 200 | 0.940 | 0.849 | — | — | 0.734 | -0.617 | 0.215 | -0.037 | -0.053 | 0.757 | 0.099 |
| Tox21 | GINE | IntegratedGradients | random | 1 | 200 | 0.955 | 0.792 | — | — | 0.788 | -0.127 | 0.420 | -0.012 | -0.012 | 0.757 | 0.148 |
| Tox21 | GINE | IntegratedGradients | random | 2 | 200 | 0.925 | 0.820 | — | — | 0.725 | -0.063 | 0.365 | -0.096 | -0.060 | 0.753 | 0.093 |
| Tox21 | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.970 | 0.822 | — | — | 0.765 | -0.358 | 0.275 | 0.009 | 0.004 | 0.760 | 0.028 |
| Tox21 | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.950 | 0.786 | — | — | 0.760 | -0.673 | 0.215 | -0.093 | -0.111 | 0.760 | 0.201 |
| Tox21 | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.635 | 0.729 | — | — | 0.750 | -0.088 | 0.490 | 0.118 | 0.137 | 0.761 | 0.099 |
| hERG | GINE | IntegratedGradients | random | 0 | 197 | 0.792 | 0.824 | — | — | 0.783 | 0.636 | 0.822 | 0.576 | 0.576 | 0.779 | 0.093 |
| hERG | GINE | IntegratedGradients | random | 1 | 197 | 0.431 | 0.823 | — | — | 0.726 | -0.691 | 0.142 | -0.188 | -0.188 | 0.777 | 0.167 |
| hERG | GINE | IntegratedGradients | random | 2 | 197 | 0.741 | 0.815 | — | — | 0.773 | 0.776 | 0.909 | 0.765 | 0.765 | 0.779 | 0.067 |
| hERG | GINE | IntegratedGradients | scaffold | 0 | 197 | 0.685 | 0.805 | — | — | 0.729 | -0.077 | 0.472 | 0.162 | 0.163 | 0.775 | 0.070 |
| hERG | GINE | IntegratedGradients | scaffold | 1 | 197 | 0.198 | 0.629 | — | — | 0.760 | -0.228 | 0.254 | 0.000 | 0.000 | 0.774 | 0.529 |
| hERG | GINE | IntegratedGradients | scaffold | 2 | 197 | 0.198 | 0.542 | — | — | 0.730 | -0.130 | 0.426 | -0.000 | 0.000 | 0.776 | 0.514 |

## Regression audit matrix

| dataset | backbone | attributor | split | seed | n_mol | rmse | mae | r2 | motif_top1 | occ_spearman | occ_top1 | fid+ | fid- | sparsity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ESOL | GAT | IntegratedGradients | random | 0 | 200 | 0.730 | 0.549 | 0.888 | 0.828 | 0.805 | 0.945 | 3.257 | 6.809 | 0.734 |
| ESOL | GAT | IntegratedGradients | random | 1 | 200 | 0.810 | 0.608 | 0.834 | 0.823 | 0.762 | 0.915 | 2.572 | 3.999 | 0.736 |
| ESOL | GAT | IntegratedGradients | random | 2 | 200 | 0.751 | 0.548 | 0.878 | 0.842 | 0.841 | 0.940 | 3.505 | 7.619 | 0.734 |
| ESOL | GAT | IntegratedGradients | scaffold | 0 | 200 | 0.793 | 0.627 | 0.838 | 0.806 | 0.849 | 0.940 | 4.745 | 9.031 | 0.730 |
| ESOL | GAT | IntegratedGradients | scaffold | 1 | 200 | 0.829 | 0.633 | 0.850 | 0.812 | 0.701 | 0.880 | 1.729 | 2.561 | 0.727 |
| ESOL | GAT | IntegratedGradients | scaffold | 2 | 200 | 0.894 | 0.669 | 0.826 | 0.798 | 0.902 | 0.960 | 4.788 | 14.204 | 0.730 |
| ESOL | GCN | IntegratedGradients | random | 0 | 200 | 0.951 | 0.746 | 0.809 | 0.855 | 0.512 | 0.695 | -0.859 | -0.928 | 0.733 |
| ESOL | GCN | IntegratedGradients | random | 1 | 200 | 0.929 | 0.723 | 0.782 | 0.849 | 0.506 | 0.745 | -0.937 | -1.014 | 0.736 |
| ESOL | GCN | IntegratedGradients | random | 2 | 200 | 0.961 | 0.742 | 0.800 | 0.859 | 0.251 | 0.510 | -0.716 | -0.758 | 0.731 |
| ESOL | GCN | IntegratedGradients | scaffold | 0 | 200 | 1.017 | 0.793 | 0.734 | 0.835 | 0.579 | 0.715 | -0.970 | -1.432 | 0.733 |
| ESOL | GCN | IntegratedGradients | scaffold | 1 | 200 | 1.062 | 0.823 | 0.755 | 0.822 | 0.759 | 0.895 | -1.332 | -2.286 | 0.729 |
| ESOL | GCN | IntegratedGradients | scaffold | 2 | 200 | 0.972 | 0.746 | 0.794 | 0.829 | 0.640 | 0.785 | -1.051 | -1.432 | 0.730 |
| ESOL | GINE | GNNExplainer | random | 0 | 200 | 0.788 | 0.599 | 0.869 | 0.844 | 0.856 | 0.975 | -1.277 | -2.708 | 0.760 |
| ESOL | GINE | GNNExplainer | random | 1 | 200 | 0.832 | 0.648 | 0.825 | 0.840 | 0.674 | 0.880 | -0.986 | -1.731 | 0.757 |
| ESOL | GINE | GNNExplainer | random | 2 | 200 | 0.879 | 0.639 | 0.833 | 0.862 | 0.373 | 0.640 | -1.316 | -1.758 | 0.757 |
| ESOL | GINE | GNNExplainer | scaffold | 0 | 200 | 0.929 | 0.724 | 0.778 | 0.824 | 0.765 | 0.910 | -0.982 | -2.256 | 0.758 |
| ESOL | GINE | GNNExplainer | scaffold | 1 | 200 | 0.928 | 0.693 | 0.812 | 0.822 | 0.714 | 0.875 | -0.978 | -2.121 | 0.758 |
| ESOL | GINE | GNNExplainer | scaffold | 2 | 200 | 0.886 | 0.650 | 0.829 | 0.825 | 0.525 | 0.725 | -1.054 | -1.408 | 0.758 |
| ESOL | GINE | IntegratedGradients | random | 0 | 200 | 0.788 | 0.599 | 0.869 | 0.868 | 0.904 | 0.970 | -1.668 | -2.456 | 0.740 |
| ESOL | GINE | IntegratedGradients | random | 1 | 200 | 0.832 | 0.648 | 0.825 | 0.858 | 0.714 | 0.880 | -1.213 | -1.644 | 0.746 |
| ESOL | GINE | IntegratedGradients | random | 2 | 200 | 0.879 | 0.639 | 0.833 | 0.870 | 0.432 | 0.640 | -1.490 | -1.686 | 0.739 |
| ESOL | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.929 | 0.724 | 0.778 | 0.843 | 0.807 | 0.925 | -1.425 | -2.077 | 0.735 |
| ESOL | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.928 | 0.693 | 0.812 | 0.833 | 0.757 | 0.880 | -1.320 | -1.882 | 0.737 |
| ESOL | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.886 | 0.650 | 0.829 | 0.827 | 0.571 | 0.725 | -1.218 | -1.265 | 0.742 |
| FreeSolv | GINE | IntegratedGradients | random | 0 | 193 | 1.486 | 1.081 | 0.803 | 0.876 | 0.442 | 0.819 | -0.735 | -1.070 | 0.713 |
| FreeSolv | GINE | IntegratedGradients | random | 1 | 193 | 1.346 | 1.003 | 0.857 | 0.861 | 0.461 | 0.798 | -0.606 | -1.000 | 0.707 |
| FreeSolv | GINE | IntegratedGradients | random | 2 | 193 | 1.618 | 1.112 | 0.830 | 0.857 | 0.276 | 0.699 | -0.715 | -0.788 | 0.717 |
| FreeSolv | GINE | IntegratedGradients | scaffold | 0 | 193 | 1.304 | 0.965 | 0.881 | 0.871 | 0.567 | 0.839 | -0.549 | -1.092 | 0.720 |
| FreeSolv | GINE | IntegratedGradients | scaffold | 1 | 193 | 1.425 | 1.075 | 0.847 | 0.840 | 0.612 | 0.865 | -0.660 | -0.822 | 0.722 |
| FreeSolv | GINE | IntegratedGradients | scaffold | 2 | 193 | 1.529 | 1.126 | 0.824 | 0.847 | 0.779 | 0.881 | -1.020 | -1.561 | 0.731 |
| Lipophilicity | GINE | IntegratedGradients | random | 0 | 200 | 0.737 | 0.571 | 0.617 | 0.787 | 0.470 | 0.680 | 0.535 | 0.521 | 0.778 |
| Lipophilicity | GINE | IntegratedGradients | random | 1 | 200 | 0.798 | 0.604 | 0.527 | 0.781 | 0.652 | 0.830 | 1.052 | 1.365 | 0.780 |
| Lipophilicity | GINE | IntegratedGradients | random | 2 | 200 | 0.783 | 0.597 | 0.563 | 0.790 | 0.546 | 0.700 | -0.636 | -1.248 | 0.781 |
| Lipophilicity | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.749 | 0.584 | 0.614 | 0.753 | 0.582 | 0.870 | 1.044 | 1.906 | 0.781 |
| Lipophilicity | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.764 | 0.595 | 0.599 | 0.830 | 0.143 | 0.320 | 0.172 | -0.539 | 0.781 |
| Lipophilicity | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.754 | 0.587 | 0.609 | 0.769 | 0.542 | 0.705 | -0.716 | -1.411 | 0.781 |

### Metric legend
- **acc/auc**: classification test accuracy / ROC-AUC (AUC is the honest signal on imbalanced sets, where accuracy tracks the majority class). **gt_auroc/gt_auprc**: attribution vs ground-truth motif mask (Tier-1 only; chance AUROC = 0.5; below 0.5 = *anti-aligned* with the motif).
- **rmse/mae/r2**: regression test-set error metrics (original units).
- **motif_top1**: fraction of attribution mass in the single top RDKit motif. **occ_spearman/occ_top1**: occlusion-vs-attribution faithfulness.
- **fid+/fid-**: Fidelity+ (predicted prob/value drop removing salient atoms; higher is better) / Fidelity- (removing non-salient; lower is better). **ece**: test-set expected calibration error (temperature-scaled).
