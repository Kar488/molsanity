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
| BA-2Motifs | GINE | GNNExplainer | scaffold | 0 | 200 | 0.390 | 0.953 | 0.506 | 0.301 | 0.042 | -0.042 | 0.065 | -0.001 | -0.002 | 0.800 | 0.148 |
| BA-2Motifs | GINE | GNNExplainer | scaffold | 1 | 200 | 0.430 | 0.997 | 0.656 | 0.386 | 0.048 | -0.091 | 0.050 | -0.003 | -0.015 | 0.800 | 0.069 |
| BA-2Motifs | GINE | GNNExplainer | scaffold | 2 | 200 | 0.990 | 0.983 | 0.526 | 0.317 | 0.042 | 0.009 | 0.045 | -0.001 | -0.005 | 0.800 | 0.432 |
| BA-2Motifs | GINE | GuidedBackprop | random | 0 | 200 | 0.780 | 1.000 | 0.923 | 0.859 | 0.180 | -0.159 | 0.140 | 0.141 | -0.004 | 0.790 | 0.076 |
| BA-2Motifs | GINE | GuidedBackprop | random | 1 | 200 | 0.645 | 1.000 | 0.963 | 0.943 | 0.180 | -0.262 | 0.000 | -0.012 | -0.001 | 0.781 | 0.080 |
| BA-2Motifs | GINE | GuidedBackprop | random | 2 | 200 | 0.875 | 1.000 | 0.948 | 0.900 | 0.133 | -0.323 | 0.005 | -0.013 | -0.014 | 0.797 | 0.034 |
| BA-2Motifs | GINE | GuidedBackprop | scaffold | 0 | 200 | 0.390 | 0.953 | 0.681 | 0.399 | 0.105 | 0.111 | 0.090 | -0.000 | -0.003 | 0.783 | 0.148 |
| BA-2Motifs | GINE | GuidedBackprop | scaffold | 1 | 200 | 0.430 | 0.997 | 0.938 | 0.793 | 0.122 | -0.204 | 0.015 | 0.003 | -0.005 | 0.800 | 0.069 |
| BA-2Motifs | GINE | GuidedBackprop | scaffold | 2 | 200 | 0.990 | 0.983 | 0.909 | 0.662 | 0.118 | -0.667 | 0.065 | -0.002 | -0.004 | 0.800 | 0.432 |
| BA-2Motifs | GINE | InputXGradient | random | 0 | 200 | 0.780 | 1.000 | 1.000 | 0.998 | 0.213 | -0.148 | 0.155 | 0.111 | 0.020 | 0.800 | 0.076 |
| BA-2Motifs | GINE | InputXGradient | random | 1 | 200 | 0.645 | 1.000 | 0.996 | 0.987 | 0.199 | -0.164 | 0.280 | -0.010 | -0.002 | 0.800 | 0.080 |
| BA-2Motifs | GINE | InputXGradient | random | 2 | 200 | 0.875 | 1.000 | 0.928 | 0.740 | 0.127 | -0.260 | 0.005 | -0.012 | -0.016 | 0.790 | 0.034 |
| BA-2Motifs | GINE | InputXGradient | scaffold | 0 | 200 | 0.390 | 0.953 | 0.901 | 0.706 | 0.098 | -0.136 | 0.195 | -0.003 | 0.000 | 0.798 | 0.148 |
| BA-2Motifs | GINE | InputXGradient | scaffold | 1 | 200 | 0.430 | 0.997 | 0.982 | 0.938 | 0.131 | -0.050 | 0.075 | 0.002 | -0.011 | 0.800 | 0.069 |
| BA-2Motifs | GINE | InputXGradient | scaffold | 2 | 200 | 0.990 | 0.983 | 0.927 | 0.723 | 0.117 | -0.671 | 0.045 | -0.002 | -0.004 | 0.799 | 0.432 |
| BA-2Motifs | GINE | IntegratedGradients | random | 0 | 200 | 0.780 | 1.000 | 0.996 | 0.987 | 0.210 | -0.177 | 0.160 | 0.112 | 0.020 | 0.800 | 0.076 |
| BA-2Motifs | GINE | IntegratedGradients | random | 1 | 200 | 0.645 | 1.000 | 1.000 | 1.000 | 0.172 | -0.159 | 0.200 | -0.009 | -0.004 | 0.800 | 0.080 |
| BA-2Motifs | GINE | IntegratedGradients | random | 2 | 200 | 0.875 | 1.000 | 0.994 | 0.978 | 0.132 | -0.276 | 0.040 | -0.013 | -0.014 | 0.800 | 0.034 |
| BA-2Motifs | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.390 | 0.953 | 0.885 | 0.612 | 0.098 | -0.202 | 0.145 | -0.004 | 0.000 | 0.800 | 0.148 |
| BA-2Motifs | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.430 | 0.997 | 0.827 | 0.485 | 0.099 | -0.094 | 0.030 | -0.004 | -0.009 | 0.800 | 0.069 |
| BA-2Motifs | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.990 | 0.983 | 0.856 | 0.533 | 0.112 | -0.635 | 0.070 | -0.002 | -0.004 | 0.799 | 0.432 |
| BA-2Motifs | GINE | PGExplainer | random | 0 | 200 | 0.780 | 1.000 | 0.485 | 0.273 | 0.362 | -0.114 | 0.000 | 0.021 | 0.108 | 0.743 | 0.076 |
| BA-2Motifs | GINE | PGExplainer | random | 1 | 200 | 0.645 | 1.000 | 0.604 | 0.450 | 0.410 | 0.003 | 0.005 | 0.001 | -0.004 | 0.756 | 0.080 |
| BA-2Motifs | GINE | PGExplainer | random | 2 | 200 | 0.875 | 1.000 | 0.104 | 0.190 | 0.378 | 0.155 | 0.000 | -0.003 | -0.023 | 0.777 | 0.034 |
| BA-2Motifs | GINE | PGExplainer | scaffold | 0 | 200 | 0.390 | 0.953 | 0.978 | 0.959 | 0.479 | -0.145 | 0.065 | -0.003 | 0.000 | 0.727 | 0.148 |
| BA-2Motifs | GINE | PGExplainer | scaffold | 1 | 200 | 0.430 | 0.997 | 0.948 | 0.895 | 0.497 | 0.122 | 0.315 | -0.003 | -0.011 | 0.641 | 0.069 |
| BA-2Motifs | GINE | PGExplainer | scaffold | 2 | 200 | 0.990 | 0.983 | 0.731 | 0.450 | 0.353 | 0.114 | 0.025 | -0.001 | -0.005 | 0.769 | 0.432 |
| BA-2Motifs | GINE | Saliency | random | 0 | 200 | 0.780 | 1.000 | 1.000 | 0.998 | 0.213 | -0.148 | 0.155 | 0.111 | 0.020 | 0.800 | 0.076 |
| BA-2Motifs | GINE | Saliency | random | 1 | 200 | 0.645 | 1.000 | 0.996 | 0.987 | 0.199 | -0.164 | 0.280 | -0.010 | -0.002 | 0.800 | 0.080 |
| BA-2Motifs | GINE | Saliency | random | 2 | 200 | 0.875 | 1.000 | 0.928 | 0.740 | 0.127 | -0.260 | 0.005 | -0.012 | -0.016 | 0.790 | 0.034 |
| BA-2Motifs | GINE | Saliency | scaffold | 0 | 200 | 0.390 | 0.953 | 0.901 | 0.706 | 0.098 | -0.136 | 0.195 | -0.003 | 0.000 | 0.798 | 0.148 |
| BA-2Motifs | GINE | Saliency | scaffold | 1 | 200 | 0.430 | 0.997 | 0.982 | 0.938 | 0.131 | -0.050 | 0.075 | 0.002 | -0.011 | 0.800 | 0.069 |
| BA-2Motifs | GINE | Saliency | scaffold | 2 | 200 | 0.990 | 0.983 | 0.927 | 0.723 | 0.117 | -0.671 | 0.045 | -0.002 | -0.004 | 0.799 | 0.432 |
| BACE | GCN | IntegratedGradients | random | 0 | 200 | 0.725 | 0.839 | — | — | 0.782 | 0.170 | 0.610 | 0.266 | 0.311 | 0.786 | 0.082 |
| BACE | GCN | IntegratedGradients | random | 1 | 200 | 0.585 | 0.797 | — | — | 0.775 | 0.002 | 0.460 | 0.189 | 0.191 | 0.786 | 0.039 |
| BACE | GCN | IntegratedGradients | random | 2 | 200 | 0.850 | 0.820 | — | — | 0.756 | 0.532 | 0.830 | 0.576 | 0.596 | 0.785 | 0.036 |
| BACE | GCN | IntegratedGradients | scaffold | 0 | 200 | 0.745 | 0.721 | — | — | 0.812 | 0.623 | 0.830 | 0.567 | 0.567 | 0.785 | 0.125 |
| BACE | GCN | IntegratedGradients | scaffold | 1 | 200 | 0.365 | 0.691 | — | — | 0.786 | -0.726 | 0.090 | -0.054 | -0.056 | 0.784 | 0.116 |
| BACE | GCN | IntegratedGradients | scaffold | 2 | 200 | 0.775 | 0.683 | — | — | 0.822 | 0.518 | 0.780 | 0.543 | 0.544 | 0.783 | 0.108 |
| BACE | GINE | IntegratedGradients | random | 0 | 200 | 0.810 | 0.846 | — | — | 0.824 | 0.359 | 0.675 | 0.390 | 0.347 | 0.787 | 0.055 |
| BACE | GINE | IntegratedGradients | random | 1 | 200 | 0.695 | 0.797 | — | — | 0.790 | 0.193 | 0.610 | 0.330 | 0.343 | 0.786 | 0.057 |
| BACE | GINE | IntegratedGradients | random | 2 | 200 | 0.685 | 0.820 | — | — | 0.751 | -0.203 | 0.385 | 0.103 | 0.115 | 0.787 | 0.075 |
| BACE | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.605 | 0.724 | — | — | 0.850 | 0.116 | 0.390 | 0.205 | 0.269 | 0.785 | 0.047 |
| BACE | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.590 | 0.727 | — | — | 0.864 | 0.105 | 0.470 | 0.127 | 0.185 | 0.785 | 0.060 |
| BACE | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.440 | 0.698 | — | — | 0.876 | 0.057 | 0.030 | 0.385 | 0.358 | 0.783 | 0.077 |
| BBBP | AttentiveFP | IntegratedGradients | random | 0 | 200 | 0.785 | 0.855 | — | — | 0.756 | 0.253 | 0.425 | 0.086 | 0.165 | 0.771 | 0.050 |
| BBBP | AttentiveFP | IntegratedGradients | random | 1 | 200 | 0.745 | 0.913 | — | — | 0.760 | 0.220 | 0.415 | 0.123 | 0.046 | 0.762 | 0.024 |
| BBBP | AttentiveFP | IntegratedGradients | random | 2 | 200 | 0.740 | 0.885 | — | — | 0.732 | 0.230 | 0.415 | 0.068 | 0.069 | 0.759 | 0.040 |
| BBBP | AttentiveFP | IntegratedGradients | scaffold | 0 | 200 | 0.875 | 0.948 | — | — | 0.758 | 0.353 | 0.545 | 0.288 | 0.181 | 0.780 | 0.142 |
| BBBP | AttentiveFP | IntegratedGradients | scaffold | 1 | 200 | 0.860 | 0.960 | — | — | 0.725 | 0.486 | 0.545 | 0.232 | 0.161 | 0.776 | 0.135 |
| BBBP | AttentiveFP | IntegratedGradients | scaffold | 2 | 200 | 0.830 | 0.954 | — | — | 0.768 | 0.389 | 0.595 | 0.232 | 0.166 | 0.778 | 0.103 |
| BBBP | GAT | IntegratedGradients | random | 0 | 200 | 0.735 | 0.885 | — | — | 0.760 | 0.044 | 0.505 | 0.268 | 0.267 | 0.775 | 0.051 |
| BBBP | GAT | IntegratedGradients | random | 1 | 200 | 0.740 | 0.906 | — | — | 0.802 | -0.067 | 0.505 | 0.230 | 0.230 | 0.767 | 0.039 |
| BBBP | GAT | IntegratedGradients | random | 2 | 200 | 0.730 | 0.909 | — | — | 0.748 | 0.029 | 0.330 | 0.158 | 0.159 | 0.767 | 0.007 |
| BBBP | GAT | IntegratedGradients | scaffold | 0 | 200 | 0.835 | 0.913 | — | — | 0.772 | -0.022 | 0.415 | 0.145 | 0.256 | 0.779 | 0.146 |
| BBBP | GAT | IntegratedGradients | scaffold | 1 | 200 | 0.810 | 0.924 | — | — | 0.812 | 0.258 | 0.585 | 0.291 | 0.359 | 0.781 | 0.101 |
| BBBP | GAT | IntegratedGradients | scaffold | 2 | 200 | 0.790 | 0.906 | — | — | 0.781 | 0.134 | 0.565 | 0.351 | 0.351 | 0.778 | 0.121 |
| BBBP | GCN | IntegratedGradients | random | 0 | 200 | 0.735 | 0.873 | — | — | 0.769 | -0.040 | 0.475 | 0.222 | 0.224 | 0.770 | 0.074 |
| BBBP | GCN | IntegratedGradients | random | 1 | 200 | 0.710 | 0.893 | — | — | 0.824 | -0.012 | 0.505 | 0.236 | 0.243 | 0.761 | 0.025 |
| BBBP | GCN | IntegratedGradients | random | 2 | 200 | 0.775 | 0.902 | — | — | 0.794 | -0.376 | 0.295 | 0.008 | 0.003 | 0.765 | 0.031 |
| BBBP | GCN | IntegratedGradients | scaffold | 0 | 200 | 0.835 | 0.905 | — | — | 0.798 | 0.041 | 0.460 | 0.269 | 0.284 | 0.777 | 0.167 |
| BBBP | GCN | IntegratedGradients | scaffold | 1 | 200 | 0.800 | 0.910 | — | — | 0.782 | 0.407 | 0.570 | 0.230 | 0.377 | 0.778 | 0.081 |
| BBBP | GCN | IntegratedGradients | scaffold | 2 | 200 | 0.835 | 0.931 | — | — | 0.822 | 0.118 | 0.555 | 0.407 | 0.409 | 0.768 | 0.097 |
| BBBP | GINE | GNNExplainer | random | 0 | 200 | 0.745 | 0.886 | — | — | 0.780 | -0.200 | 0.300 | 0.159 | 0.200 | 0.779 | 0.053 |
| BBBP | GINE | GNNExplainer | random | 1 | 200 | 0.760 | 0.899 | — | — | 0.828 | -0.034 | 0.455 | 0.171 | 0.214 | 0.777 | 0.016 |
| BBBP | GINE | GNNExplainer | random | 2 | 200 | 0.685 | 0.891 | — | — | 0.789 | 0.179 | 0.435 | 0.218 | 0.234 | 0.779 | 0.031 |
| BBBP | GINE | GNNExplainer | scaffold | 0 | 200 | 0.875 | 0.910 | — | — | 0.800 | 0.338 | 0.405 | 0.340 | 0.336 | 0.783 | 0.173 |
| BBBP | GINE | GNNExplainer | scaffold | 1 | 200 | 0.795 | 0.925 | — | — | 0.806 | 0.274 | 0.470 | 0.363 | 0.415 | 0.783 | 0.102 |
| BBBP | GINE | GNNExplainer | scaffold | 2 | 200 | 0.810 | 0.939 | — | — | 0.807 | 0.435 | 0.585 | 0.286 | 0.315 | 0.783 | 0.070 |
| BBBP | GINE | IntegratedGradients | random | 0 | 200 | 0.745 | 0.886 | — | — | 0.719 | -0.175 | 0.370 | 0.201 | 0.201 | 0.772 | 0.053 |
| BBBP | GINE | IntegratedGradients | random | 1 | 200 | 0.760 | 0.899 | — | — | 0.826 | 0.082 | 0.460 | 0.266 | 0.213 | 0.766 | 0.016 |
| BBBP | GINE | IntegratedGradients | random | 2 | 200 | 0.685 | 0.891 | — | — | 0.764 | 0.226 | 0.450 | 0.191 | 0.246 | 0.772 | 0.031 |
| BBBP | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.875 | 0.910 | — | — | 0.751 | 0.516 | 0.440 | 0.282 | 0.332 | 0.775 | 0.173 |
| BBBP | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.795 | 0.925 | — | — | 0.762 | 0.420 | 0.465 | 0.334 | 0.423 | 0.776 | 0.102 |
| BBBP | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.810 | 0.939 | — | — | 0.777 | 0.591 | 0.595 | 0.230 | 0.334 | 0.777 | 0.070 |
| BBBP | GINE | PGExplainer | random | 0 | 200 | 0.745 | 0.886 | — | — | 0.886 | -0.160 | 0.250 | 0.091 | 0.200 | 0.773 | 0.053 |
| BBBP | GINE | PGExplainer | random | 1 | 200 | 0.760 | 0.899 | — | — | 0.933 | -0.149 | 0.305 | 0.173 | 0.178 | 0.703 | 0.016 |
| BBBP | GINE | PGExplainer | random | 2 | 200 | 0.685 | 0.891 | — | — | 0.879 | -0.085 | 0.300 | 0.114 | 0.229 | 0.690 | 0.031 |
| BBBP | GINE | PGExplainer | scaffold | 0 | 200 | 0.875 | 0.910 | — | — | 0.908 | 0.224 | 0.295 | 0.147 | 0.341 | 0.760 | 0.173 |
| BBBP | GINE | PGExplainer | scaffold | 1 | 200 | 0.795 | 0.925 | — | — | 0.909 | 0.268 | 0.210 | 0.278 | 0.405 | 0.757 | 0.102 |
| BBBP | GINE | PGExplainer | scaffold | 2 | 200 | 0.810 | 0.939 | — | — | 0.828 | 0.144 | 0.265 | 0.143 | 0.248 | 0.639 | 0.070 |
| BBBP | MPNN | IntegratedGradients | random | 0 | 200 | 0.740 | 0.914 | — | — | 0.792 | 0.018 | 0.345 | 0.119 | 0.150 | 0.771 | 0.053 |
| BBBP | MPNN | IntegratedGradients | random | 1 | 200 | 0.775 | 0.904 | — | — | 0.810 | 0.247 | 0.455 | 0.119 | 0.209 | 0.763 | 0.023 |
| BBBP | MPNN | IntegratedGradients | random | 2 | 200 | 0.755 | 0.899 | — | — | 0.774 | -0.125 | 0.320 | 0.089 | 0.147 | 0.769 | 0.043 |
| BBBP | MPNN | IntegratedGradients | scaffold | 0 | 200 | 0.810 | 0.917 | — | — | 0.811 | 0.091 | 0.520 | 0.162 | 0.359 | 0.779 | 0.139 |
| BBBP | MPNN | IntegratedGradients | scaffold | 1 | 200 | 0.825 | 0.927 | — | — | 0.823 | 0.341 | 0.465 | 0.107 | 0.216 | 0.776 | 0.118 |
| BBBP | MPNN | IntegratedGradients | scaffold | 2 | 200 | 0.820 | 0.925 | — | — | 0.823 | 0.048 | 0.520 | 0.256 | 0.395 | 0.777 | 0.088 |
| ClinTox | GINE | GNNExplainer | random | 0 | 200 | 0.725 | 0.910 | — | — | 0.566 | 0.065 | 0.435 | 0.245 | 0.226 | 0.840 | 0.157 |
| ClinTox | GINE | GNNExplainer | random | 1 | 200 | 0.760 | 0.870 | — | — | 0.250 | 0.779 | 0.440 | 0.207 | 0.145 | 0.930 | 0.063 |
| ClinTox | GINE | GNNExplainer | random | 2 | 200 | 0.705 | 0.861 | — | — | 0.612 | -0.018 | 0.425 | 0.194 | 0.152 | 0.831 | 0.083 |
| ClinTox | GINE | GNNExplainer | scaffold | 0 | 200 | 0.585 | 0.821 | — | — | 0.746 | 0.026 | 0.520 | 0.280 | 0.277 | 0.786 | 0.193 |
| ClinTox | GINE | GNNExplainer | scaffold | 1 | 200 | 0.710 | 0.844 | — | — | 0.752 | -0.200 | 0.390 | 0.191 | 0.189 | 0.787 | 0.127 |
| ClinTox | GINE | GNNExplainer | scaffold | 2 | 200 | 0.725 | 0.866 | — | — | 0.511 | 0.093 | 0.400 | 0.239 | 0.199 | 0.861 | 0.111 |
| ClinTox | GINE | IntegratedGradients | random | 0 | 200 | 0.725 | 0.910 | — | — | 0.788 | -0.221 | 0.410 | 0.230 | 0.226 | 0.774 | 0.157 |
| ClinTox | GINE | IntegratedGradients | random | 1 | 200 | 0.760 | 0.870 | — | — | 0.815 | -0.417 | 0.335 | 0.148 | 0.145 | 0.769 | 0.063 |
| ClinTox | GINE | IntegratedGradients | random | 2 | 200 | 0.705 | 0.861 | — | — | 0.794 | -0.224 | 0.425 | 0.152 | 0.152 | 0.775 | 0.083 |
| ClinTox | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.585 | 0.821 | — | — | 0.755 | 0.010 | 0.505 | 0.277 | 0.277 | 0.778 | 0.193 |
| ClinTox | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.710 | 0.844 | — | — | 0.754 | -0.256 | 0.375 | 0.189 | 0.189 | 0.778 | 0.127 |
| ClinTox | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.725 | 0.866 | — | — | 0.760 | -0.264 | 0.370 | 0.199 | 0.199 | 0.779 | 0.111 |
| DILI | GINE | IntegratedGradients | random | 0 | 142 | 0.824 | 0.719 | — | — | 0.738 | 0.491 | 0.556 | 0.347 | 0.356 | 0.773 | 0.135 |
| DILI | GINE | IntegratedGradients | random | 1 | 142 | 0.613 | 0.790 | — | — | 0.715 | 0.300 | 0.479 | 0.079 | 0.106 | 0.772 | 0.084 |
| DILI | GINE | IntegratedGradients | random | 2 | 142 | 0.704 | 0.775 | — | — | 0.774 | 0.105 | 0.380 | 0.149 | 0.164 | 0.775 | 0.131 |
| DILI | GINE | IntegratedGradients | scaffold | 0 | 142 | 0.732 | 0.788 | — | — | 0.819 | 0.445 | 0.662 | 0.349 | 0.470 | 0.774 | 0.047 |
| DILI | GINE | IntegratedGradients | scaffold | 1 | 142 | 0.697 | 0.786 | — | — | 0.801 | 0.058 | 0.444 | 0.158 | 0.201 | 0.779 | 0.134 |
| DILI | GINE | IntegratedGradients | scaffold | 2 | 142 | 0.782 | 0.830 | — | — | 0.857 | 0.505 | 0.641 | 0.205 | 0.111 | 0.779 | 0.075 |
| MUTAG | AttentiveFP | IntegratedGradients | random | 0 | 58 | 0.724 | 0.958 | 0.047 | 0.174 | 0.949 | 0.929 | 1.000 | 0.010 | 0.021 | 0.773 | 0.372 |
| MUTAG | AttentiveFP | IntegratedGradients | random | 1 | 58 | 0.810 | 0.875 | 0.034 | 0.173 | 0.977 | 0.411 | 0.672 | 0.193 | 0.374 | 0.769 | 0.068 |
| MUTAG | AttentiveFP | IntegratedGradients | random | 2 | 58 | 0.672 | 0.911 | 0.039 | 0.165 | 0.958 | -0.871 | 0.000 | -0.007 | -0.022 | 0.772 | 0.106 |
| MUTAG | AttentiveFP | IntegratedGradients | scaffold | 0 | 53 | 0.774 | 0.888 | 0.023 | 0.133 | 0.991 | 0.803 | 1.000 | 0.006 | 0.016 | 0.770 | 0.262 |
| MUTAG | AttentiveFP | IntegratedGradients | scaffold | 1 | 53 | 0.774 | 0.894 | 0.016 | 0.132 | 0.995 | 0.953 | 0.830 | 0.026 | 0.057 | 0.773 | 0.132 |
| MUTAG | AttentiveFP | IntegratedGradients | scaffold | 2 | 53 | 0.774 | 0.876 | 0.049 | 0.136 | 0.994 | -0.780 | 0.000 | -0.007 | -0.021 | 0.773 | 0.262 |
| MUTAG | GAT | IntegratedGradients | random | 0 | 58 | 0.741 | 0.583 | 0.689 | 0.612 | 0.935 | 0.313 | 0.638 | 0.350 | 0.385 | 0.772 | 0.247 |
| MUTAG | GAT | IntegratedGradients | random | 1 | 58 | 0.362 | 0.687 | 0.050 | 0.169 | 0.947 | -0.558 | 0.052 | -0.004 | -0.007 | 0.769 | 0.148 |
| MUTAG | GAT | IntegratedGradients | random | 2 | 58 | 0.759 | 0.746 | 0.461 | 0.356 | 0.925 | 0.698 | 0.810 | 0.281 | 0.511 | 0.775 | 0.089 |
| MUTAG | GAT | IntegratedGradients | scaffold | 0 | 53 | 0.774 | 0.854 | 0.848 | 0.693 | 0.981 | 0.686 | 0.132 | 0.001 | 0.002 | 0.772 | 0.193 |
| MUTAG | GAT | IntegratedGradients | scaffold | 1 | 53 | 0.868 | 0.945 | 0.018 | 0.130 | 0.995 | 0.482 | 0.245 | 0.026 | 0.050 | 0.772 | 0.345 |
| MUTAG | GAT | IntegratedGradients | scaffold | 2 | 53 | 0.830 | 0.941 | 0.733 | 0.694 | 0.981 | 0.652 | 0.906 | 0.136 | 0.461 | 0.775 | 0.198 |
| MUTAG | GCN | IntegratedGradients | random | 0 | 58 | 0.776 | 0.604 | 0.170 | 0.238 | 0.950 | 0.299 | 0.603 | 0.276 | 0.387 | 0.772 | 0.308 |
| MUTAG | GCN | IntegratedGradients | random | 1 | 58 | 0.362 | 0.727 | 0.379 | 0.315 | 0.934 | 0.579 | 0.828 | -0.001 | -0.000 | 0.758 | 0.147 |
| MUTAG | GCN | IntegratedGradients | random | 2 | 58 | 0.776 | 0.768 | 0.551 | 0.552 | 0.932 | 0.610 | 0.759 | 0.435 | 0.518 | 0.764 | 0.119 |
| MUTAG | GCN | IntegratedGradients | scaffold | 0 | 53 | 0.792 | 0.799 | 0.101 | 0.162 | 0.990 | 0.696 | 0.925 | 0.316 | 0.584 | 0.771 | 0.266 |
| MUTAG | GCN | IntegratedGradients | scaffold | 1 | 53 | 0.830 | 0.943 | 0.066 | 0.163 | 0.989 | 0.719 | 0.868 | 0.158 | 0.431 | 0.769 | 0.122 |
| MUTAG | GCN | IntegratedGradients | scaffold | 2 | 53 | 0.774 | 0.939 | 0.083 | 0.168 | 0.989 | 0.876 | 1.000 | 0.002 | 0.004 | 0.772 | 0.235 |
| MUTAG | GINE | GNNExplainer | random | 0 | 58 | 0.534 | 0.823 | 0.448 | 0.327 | 0.937 | -0.299 | 0.310 | -0.003 | -0.007 | 0.776 | 0.048 |
| MUTAG | GINE | GNNExplainer | random | 1 | 58 | 0.810 | 0.928 | 0.728 | 0.636 | 0.936 | 0.105 | 0.466 | 0.259 | 0.448 | 0.772 | 0.154 |
| MUTAG | GINE | GNNExplainer | random | 2 | 58 | 0.897 | 0.985 | 0.858 | 0.807 | 0.929 | -0.170 | 0.207 | 0.310 | 0.175 | 0.777 | 0.065 |
| MUTAG | GINE | GNNExplainer | scaffold | 0 | 53 | 0.509 | 0.618 | 0.675 | 0.556 | 0.984 | 0.325 | 0.189 | 0.130 | 0.208 | 0.775 | 0.291 |
| MUTAG | GINE | GNNExplainer | scaffold | 1 | 53 | 0.906 | 0.941 | 0.822 | 0.771 | 0.984 | -0.333 | 0.075 | 0.064 | 0.026 | 0.775 | 0.070 |
| MUTAG | GINE | GNNExplainer | scaffold | 2 | 53 | 0.792 | 0.864 | 0.826 | 0.758 | 0.984 | 0.380 | 0.472 | 0.154 | 0.200 | 0.775 | 0.085 |
| MUTAG | GINE | GuidedBackprop | random | 0 | 58 | 0.534 | 0.823 | 0.225 | 0.246 | 0.941 | -0.323 | 0.310 | -0.003 | -0.006 | 0.773 | 0.048 |
| MUTAG | GINE | GuidedBackprop | random | 1 | 58 | 0.810 | 0.928 | 0.030 | 0.175 | 0.962 | 0.020 | 0.448 | 0.454 | 0.444 | 0.769 | 0.154 |
| MUTAG | GINE | GuidedBackprop | random | 2 | 58 | 0.897 | 0.985 | 0.037 | 0.169 | 0.962 | -0.089 | 0.207 | 0.540 | 0.615 | 0.773 | 0.065 |
| MUTAG | GINE | GuidedBackprop | scaffold | 0 | 53 | 0.509 | 0.618 | 0.067 | 0.156 | 0.996 | 0.529 | 0.189 | 0.221 | 0.155 | 0.772 | 0.291 |
| MUTAG | GINE | GuidedBackprop | scaffold | 1 | 53 | 0.906 | 0.941 | 0.061 | 0.143 | 0.989 | -0.135 | 0.075 | 0.326 | 0.123 | 0.773 | 0.070 |
| MUTAG | GINE | GuidedBackprop | scaffold | 2 | 53 | 0.792 | 0.864 | 0.013 | 0.131 | 0.998 | 0.616 | 0.472 | 0.250 | 0.109 | 0.775 | 0.085 |
| MUTAG | GINE | InputXGradient | random | 0 | 58 | 0.534 | 0.823 | 0.066 | 0.181 | 0.987 | -0.339 | 0.310 | -0.004 | -0.005 | 0.772 | 0.048 |
| MUTAG | GINE | InputXGradient | random | 1 | 58 | 0.810 | 0.928 | 0.025 | 0.166 | 0.976 | 0.022 | 0.448 | 0.398 | 0.463 | 0.770 | 0.154 |
| MUTAG | GINE | InputXGradient | random | 2 | 58 | 0.897 | 0.985 | 0.013 | 0.161 | 0.984 | -0.200 | 0.190 | 0.491 | 0.605 | 0.772 | 0.065 |
| MUTAG | GINE | InputXGradient | scaffold | 0 | 53 | 0.509 | 0.618 | 0.210 | 0.182 | 0.989 | 0.423 | 0.189 | 0.173 | 0.240 | 0.774 | 0.291 |
| MUTAG | GINE | InputXGradient | scaffold | 1 | 53 | 0.906 | 0.941 | 0.060 | 0.143 | 0.992 | -0.180 | 0.075 | 0.347 | 0.119 | 0.771 | 0.070 |
| MUTAG | GINE | InputXGradient | scaffold | 2 | 53 | 0.792 | 0.864 | 0.079 | 0.138 | 0.995 | 0.499 | 0.472 | 0.167 | 0.227 | 0.773 | 0.085 |
| MUTAG | GINE | IntegratedGradients | random | 0 | 58 | 0.534 | 0.823 | 0.052 | 0.175 | 0.984 | -0.351 | 0.310 | -0.004 | -0.005 | 0.771 | 0.048 |
| MUTAG | GINE | IntegratedGradients | random | 1 | 58 | 0.810 | 0.928 | 0.612 | 0.433 | 0.937 | 0.015 | 0.466 | 0.442 | 0.510 | 0.767 | 0.154 |
| MUTAG | GINE | IntegratedGradients | random | 2 | 58 | 0.897 | 0.985 | 0.496 | 0.460 | 0.915 | -0.196 | 0.155 | 0.551 | 0.433 | 0.772 | 0.065 |
| MUTAG | GINE | IntegratedGradients | scaffold | 0 | 53 | 0.509 | 0.618 | 0.686 | 0.709 | 0.973 | 0.414 | 0.170 | 0.109 | 0.322 | 0.773 | 0.291 |
| MUTAG | GINE | IntegratedGradients | scaffold | 1 | 53 | 0.906 | 0.941 | 0.715 | 0.408 | 0.978 | -0.234 | 0.057 | 0.342 | 0.111 | 0.773 | 0.070 |
| MUTAG | GINE | IntegratedGradients | scaffold | 2 | 53 | 0.792 | 0.864 | 0.302 | 0.230 | 0.986 | 0.311 | 0.472 | 0.030 | 0.249 | 0.772 | 0.085 |
| MUTAG | GINE | PGExplainer | random | 0 | 58 | 0.534 | 0.823 | 0.996 | 0.993 | 0.953 | -0.279 | 0.310 | -0.001 | -0.006 | 0.767 | 0.048 |
| MUTAG | GINE | PGExplainer | random | 1 | 58 | 0.810 | 0.928 | 0.743 | 0.572 | 0.999 | 0.152 | 0.448 | 0.361 | 0.453 | 0.730 | 0.154 |
| MUTAG | GINE | PGExplainer | random | 2 | 58 | 0.897 | 0.985 | 0.251 | 0.234 | 0.983 | -0.351 | 0.241 | 0.379 | 0.430 | 0.647 | 0.065 |
| MUTAG | GINE | PGExplainer | scaffold | 0 | 53 | 0.509 | 0.618 | 0.231 | 0.187 | 0.849 | 0.187 | 0.528 | 0.033 | 0.242 | 0.769 | 0.291 |
| MUTAG | GINE | PGExplainer | scaffold | 1 | 53 | 0.906 | 0.941 | 0.367 | 0.187 | 0.717 | -0.299 | 0.208 | 0.016 | 0.056 | 0.551 | 0.070 |
| MUTAG | GINE | PGExplainer | scaffold | 2 | 53 | 0.792 | 0.864 | 0.360 | 0.239 | 1.000 | 0.291 | 0.509 | 0.066 | 0.312 | 0.767 | 0.085 |
| MUTAG | GINE | Saliency | random | 0 | 58 | 0.534 | 0.823 | 0.029 | 0.171 | 0.979 | -0.293 | 0.310 | -0.004 | -0.006 | 0.773 | 0.048 |
| MUTAG | GINE | Saliency | random | 1 | 58 | 0.810 | 0.928 | 0.006 | 0.163 | 0.971 | 0.035 | 0.448 | 0.391 | 0.463 | 0.769 | 0.154 |
| MUTAG | GINE | Saliency | random | 2 | 58 | 0.897 | 0.985 | 0.002 | 0.160 | 0.975 | -0.195 | 0.190 | 0.494 | 0.610 | 0.772 | 0.065 |
| MUTAG | GINE | Saliency | scaffold | 0 | 53 | 0.509 | 0.618 | 0.124 | 0.164 | 0.992 | 0.437 | 0.189 | 0.210 | 0.198 | 0.775 | 0.291 |
| MUTAG | GINE | Saliency | scaffold | 1 | 53 | 0.906 | 0.941 | 0.027 | 0.134 | 0.993 | -0.190 | 0.075 | 0.316 | 0.138 | 0.773 | 0.070 |
| MUTAG | GINE | Saliency | scaffold | 2 | 53 | 0.792 | 0.864 | 0.002 | 0.130 | 0.998 | 0.406 | 0.472 | 0.153 | 0.187 | 0.773 | 0.085 |
| MUTAG | GINE | SubgraphX | random | 0 | 58 | 0.534 | 0.823 | 0.342 | 0.256 | 1.000 | -0.078 | 0.379 | -0.006 | 0.002 | 0.465 | 0.048 |
| MUTAG | GINE | SubgraphX | random | 1 | 58 | 0.810 | 0.928 | 0.489 | 0.433 | 1.000 | 0.127 | 0.483 | 0.492 | 0.084 | 0.314 | 0.154 |
| MUTAG | GINE | SubgraphX | random | 2 | 58 | 0.897 | 0.985 | 0.348 | 0.234 | 0.996 | -0.154 | 0.293 | 0.342 | -0.000 | 0.160 | 0.065 |
| MUTAG | GINE | SubgraphX | scaffold | 0 | 53 | 0.509 | 0.618 | 0.515 | 0.462 | 1.000 | 0.488 | 0.623 | 0.231 | 0.007 | 0.415 | 0.291 |
| MUTAG | GINE | SubgraphX | scaffold | 1 | 53 | 0.906 | 0.941 | 0.332 | 0.187 | 1.000 | -0.270 | 0.377 | 0.185 | 0.014 | 0.240 | 0.070 |
| MUTAG | GINE | SubgraphX | scaffold | 2 | 53 | 0.792 | 0.864 | 0.330 | 0.187 | 1.000 | 0.378 | 0.358 | 0.304 | 0.049 | 0.247 | 0.085 |
| MUTAG | MPNN | IntegratedGradients | random | 0 | 58 | 0.862 | 0.677 | 0.144 | 0.191 | 0.964 | -0.043 | 0.259 | 0.191 | 0.204 | 0.772 | 0.227 |
| MUTAG | MPNN | IntegratedGradients | random | 1 | 58 | 0.724 | 0.708 | 0.038 | 0.167 | 0.971 | 0.586 | 0.293 | 0.704 | 0.710 | 0.769 | 0.154 |
| MUTAG | MPNN | IntegratedGradients | random | 2 | 58 | 0.776 | 0.780 | 0.127 | 0.186 | 0.959 | 0.532 | 0.690 | 0.623 | 0.635 | 0.771 | 0.081 |
| MUTAG | MPNN | IntegratedGradients | scaffold | 0 | 53 | 0.906 | 0.882 | 0.110 | 0.159 | 0.992 | 0.568 | 0.792 | 0.298 | 0.403 | 0.773 | 0.355 |
| MUTAG | MPNN | IntegratedGradients | scaffold | 1 | 53 | 0.849 | 0.939 | 0.079 | 0.145 | 0.996 | 0.757 | 0.830 | 0.198 | 0.348 | 0.775 | 0.221 |
| MUTAG | MPNN | IntegratedGradients | scaffold | 2 | 53 | 0.755 | 0.917 | 0.301 | 0.250 | 0.991 | -0.706 | 0.000 | 0.002 | 0.007 | 0.770 | 0.250 |
| MolMotif | AttentiveFP | IntegratedGradients | random | 0 | 200 | 0.985 | 0.999 | 0.987 | 0.964 | 0.807 | 0.666 | 0.780 | 0.525 | 0.026 | 0.772 | 0.007 |
| MolMotif | AttentiveFP | IntegratedGradients | random | 1 | 200 | 0.910 | 0.991 | 0.928 | 0.838 | 0.738 | 0.335 | 0.555 | 0.360 | 0.031 | 0.768 | 0.055 |
| MolMotif | AttentiveFP | IntegratedGradients | random | 2 | 200 | 0.970 | 0.999 | 0.986 | 0.967 | 0.792 | 0.486 | 0.595 | 0.522 | 0.017 | 0.770 | 0.017 |
| MolMotif | AttentiveFP | IntegratedGradients | scaffold | 0 | 200 | 0.985 | 1.000 | 0.981 | 0.952 | 0.795 | 0.672 | 0.880 | 0.453 | 0.011 | 0.776 | 0.016 |
| MolMotif | AttentiveFP | IntegratedGradients | scaffold | 1 | 200 | 0.995 | 1.000 | 0.978 | 0.943 | 0.792 | 0.806 | 0.940 | 0.434 | 0.023 | 0.772 | 0.004 |
| MolMotif | AttentiveFP | IntegratedGradients | scaffold | 2 | 200 | 0.975 | 1.000 | 0.810 | 0.714 | 0.803 | 0.539 | 0.535 | 0.455 | 0.038 | 0.773 | 0.013 |
| MolMotif | GAT | IntegratedGradients | random | 0 | 200 | 1.000 | 1.000 | 0.796 | 0.709 | 0.707 | 0.246 | 0.480 | 0.401 | 0.417 | 0.772 | 0.008 |
| MolMotif | GAT | IntegratedGradients | random | 1 | 200 | 1.000 | 1.000 | 0.996 | 0.989 | 0.762 | 0.728 | 0.800 | 0.429 | 0.019 | 0.772 | 0.006 |
| MolMotif | GAT | IntegratedGradients | random | 2 | 200 | 1.000 | 1.000 | 0.733 | 0.631 | 0.716 | 0.040 | 0.375 | 0.491 | 0.240 | 0.772 | 0.004 |
| MolMotif | GAT | IntegratedGradients | scaffold | 0 | 200 | 0.990 | 1.000 | 0.767 | 0.678 | 0.743 | 0.261 | 0.600 | 0.511 | 0.525 | 0.776 | 0.016 |
| MolMotif | GAT | IntegratedGradients | scaffold | 1 | 200 | 0.995 | 1.000 | 0.922 | 0.836 | 0.761 | 0.377 | 0.670 | 0.359 | 0.517 | 0.774 | 0.009 |
| MolMotif | GAT | IntegratedGradients | scaffold | 2 | 200 | 1.000 | 1.000 | 0.706 | 0.656 | 0.768 | 0.358 | 0.645 | 0.476 | 0.320 | 0.778 | 0.006 |
| MolMotif | GCN | IntegratedGradients | random | 0 | 200 | 0.970 | 1.000 | 0.998 | 0.994 | 0.777 | 0.042 | 0.375 | 0.447 | 0.447 | 0.768 | 0.020 |
| MolMotif | GCN | IntegratedGradients | random | 1 | 200 | 0.680 | 0.999 | 0.982 | 0.957 | 0.811 | 0.473 | 0.675 | 0.110 | 0.623 | 0.770 | 0.236 |
| MolMotif | GCN | IntegratedGradients | random | 2 | 200 | 0.965 | 0.988 | 0.850 | 0.735 | 0.811 | -0.013 | 0.465 | 0.414 | 0.420 | 0.768 | 0.039 |
| MolMotif | GCN | IntegratedGradients | scaffold | 0 | 200 | 0.995 | 1.000 | 1.000 | 0.999 | 0.809 | 0.083 | 0.355 | 0.428 | 0.390 | 0.768 | 0.015 |
| MolMotif | GCN | IntegratedGradients | scaffold | 1 | 200 | 0.965 | 1.000 | 0.992 | 0.985 | 0.826 | 0.648 | 0.555 | 0.387 | 0.039 | 0.770 | 0.027 |
| MolMotif | GCN | IntegratedGradients | scaffold | 2 | 200 | 0.950 | 1.000 | 0.973 | 0.941 | 0.824 | 0.441 | 0.385 | 0.381 | 0.101 | 0.769 | 0.041 |
| MolMotif | GINE | GNNExplainer | random | 0 | 200 | 0.975 | 0.999 | 0.683 | 0.473 | 0.824 | -0.183 | 0.200 | 0.186 | 0.224 | 0.779 | 0.020 |
| MolMotif | GINE | GNNExplainer | random | 1 | 200 | 0.810 | 1.000 | 0.610 | 0.390 | 0.821 | 0.101 | 0.440 | 0.383 | 0.276 | 0.779 | 0.106 |
| MolMotif | GINE | GNNExplainer | random | 2 | 200 | 1.000 | 1.000 | 0.630 | 0.448 | 0.835 | 0.030 | 0.380 | -0.018 | 0.387 | 0.778 | 0.003 |
| MolMotif | GINE | GNNExplainer | scaffold | 0 | 200 | 0.985 | 1.000 | 0.622 | 0.409 | 0.855 | 0.027 | 0.435 | 0.370 | 0.319 | 0.780 | 0.012 |
| MolMotif | GINE | GNNExplainer | scaffold | 1 | 200 | 0.975 | 1.000 | 0.591 | 0.404 | 0.855 | -0.034 | 0.345 | 0.383 | 0.344 | 0.780 | 0.011 |
| MolMotif | GINE | GNNExplainer | scaffold | 2 | 200 | 0.960 | 0.999 | 0.636 | 0.462 | 0.850 | 0.170 | 0.470 | 0.149 | 0.369 | 0.780 | 0.017 |
| MolMotif | GINE | GuidedBackprop | random | 0 | 200 | 0.975 | 0.999 | 0.981 | 0.956 | 0.854 | -0.202 | 0.270 | 0.169 | 0.132 | 0.772 | 0.020 |
| MolMotif | GINE | GuidedBackprop | random | 1 | 200 | 0.810 | 1.000 | 0.935 | 0.835 | 0.826 | 0.007 | 0.405 | 0.116 | 0.429 | 0.772 | 0.106 |
| MolMotif | GINE | GuidedBackprop | random | 2 | 200 | 1.000 | 1.000 | 0.998 | 0.993 | 0.823 | -0.144 | 0.345 | 0.330 | 0.318 | 0.770 | 0.003 |
| MolMotif | GINE | GuidedBackprop | scaffold | 0 | 200 | 0.985 | 1.000 | 0.996 | 0.989 | 0.841 | -0.004 | 0.440 | 0.217 | 0.365 | 0.774 | 0.012 |
| MolMotif | GINE | GuidedBackprop | scaffold | 1 | 200 | 0.975 | 1.000 | 1.000 | 0.999 | 0.885 | 0.035 | 0.365 | 0.372 | 0.329 | 0.773 | 0.011 |
| MolMotif | GINE | GuidedBackprop | scaffold | 2 | 200 | 0.960 | 0.999 | 0.970 | 0.943 | 0.799 | 0.067 | 0.520 | 0.263 | 0.344 | 0.771 | 0.017 |
| MolMotif | GINE | InputXGradient | random | 0 | 200 | 0.975 | 0.999 | 0.986 | 0.971 | 0.822 | -0.285 | 0.245 | 0.040 | 0.164 | 0.773 | 0.020 |
| MolMotif | GINE | InputXGradient | random | 1 | 200 | 0.810 | 1.000 | 1.000 | 0.998 | 0.773 | -0.140 | 0.315 | 0.087 | 0.414 | 0.772 | 0.106 |
| MolMotif | GINE | InputXGradient | random | 2 | 200 | 1.000 | 1.000 | 0.999 | 0.997 | 0.810 | -0.112 | 0.445 | 0.312 | 0.322 | 0.768 | 0.003 |
| MolMotif | GINE | InputXGradient | scaffold | 0 | 200 | 0.985 | 1.000 | 0.999 | 0.998 | 0.823 | -0.082 | 0.420 | 0.144 | 0.359 | 0.775 | 0.012 |
| MolMotif | GINE | InputXGradient | scaffold | 1 | 200 | 0.975 | 1.000 | 1.000 | 0.999 | 0.824 | -0.234 | 0.315 | 0.072 | 0.382 | 0.773 | 0.011 |
| MolMotif | GINE | InputXGradient | scaffold | 2 | 200 | 0.960 | 0.999 | 0.998 | 0.993 | 0.785 | 0.059 | 0.505 | 0.251 | 0.339 | 0.773 | 0.017 |
| MolMotif | GINE | IntegratedGradients | random | 0 | 200 | 0.975 | 0.999 | 0.919 | 0.813 | 0.876 | -0.166 | 0.225 | 0.250 | 0.077 | 0.770 | 0.020 |
| MolMotif | GINE | IntegratedGradients | random | 1 | 200 | 0.810 | 1.000 | 0.963 | 0.903 | 0.870 | 0.146 | 0.440 | 0.463 | 0.257 | 0.771 | 0.106 |
| MolMotif | GINE | IntegratedGradients | random | 2 | 200 | 1.000 | 1.000 | 0.972 | 0.910 | 0.860 | 0.007 | 0.405 | 0.311 | 0.319 | 0.768 | 0.003 |
| MolMotif | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.985 | 1.000 | 0.887 | 0.690 | 0.899 | 0.026 | 0.435 | 0.386 | 0.319 | 0.773 | 0.012 |
| MolMotif | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.975 | 1.000 | 0.865 | 0.736 | 0.916 | -0.035 | 0.375 | 0.383 | 0.312 | 0.773 | 0.011 |
| MolMotif | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.960 | 0.999 | 0.939 | 0.820 | 0.851 | 0.182 | 0.485 | 0.359 | 0.309 | 0.773 | 0.017 |
| MolMotif | GINE | PGExplainer | random | 0 | 200 | 0.975 | 0.999 | 0.649 | 0.443 | 0.709 | -0.079 | 0.235 | 0.164 | 0.097 | 0.410 | 0.020 |
| MolMotif | GINE | PGExplainer | random | 1 | 200 | 0.810 | 1.000 | 0.273 | 0.218 | 0.909 | -0.215 | 0.240 | 0.090 | 0.428 | 0.768 | 0.106 |
| MolMotif | GINE | PGExplainer | random | 2 | 200 | 1.000 | 1.000 | 0.584 | 0.343 | 0.897 | 0.001 | 0.310 | 0.143 | 0.381 | 0.702 | 0.003 |
| MolMotif | GINE | PGExplainer | scaffold | 0 | 200 | 0.985 | 1.000 | 0.290 | 0.207 | 0.894 | 0.021 | 0.260 | 0.108 | 0.299 | 0.699 | 0.012 |
| MolMotif | GINE | PGExplainer | scaffold | 1 | 200 | 0.975 | 1.000 | 0.725 | 0.596 | 0.747 | -0.369 | 0.120 | 0.165 | 0.213 | 0.414 | 0.011 |
| MolMotif | GINE | PGExplainer | scaffold | 2 | 200 | 0.960 | 0.999 | 0.523 | 0.281 | 0.940 | 0.016 | 0.365 | 0.115 | 0.384 | 0.768 | 0.017 |
| MolMotif | GINE | Saliency | random | 0 | 200 | 0.975 | 0.999 | 0.990 | 0.981 | 0.826 | -0.253 | 0.260 | 0.065 | 0.167 | 0.771 | 0.020 |
| MolMotif | GINE | Saliency | random | 1 | 200 | 0.810 | 1.000 | 0.999 | 0.996 | 0.772 | -0.123 | 0.305 | 0.099 | 0.415 | 0.772 | 0.106 |
| MolMotif | GINE | Saliency | random | 2 | 200 | 1.000 | 1.000 | 0.994 | 0.985 | 0.802 | -0.117 | 0.425 | 0.318 | 0.317 | 0.772 | 0.003 |
| MolMotif | GINE | Saliency | scaffold | 0 | 200 | 0.985 | 1.000 | 0.999 | 0.997 | 0.816 | -0.097 | 0.405 | 0.130 | 0.360 | 0.775 | 0.012 |
| MolMotif | GINE | Saliency | scaffold | 1 | 200 | 0.975 | 1.000 | 1.000 | 1.000 | 0.825 | -0.221 | 0.325 | 0.058 | 0.386 | 0.774 | 0.011 |
| MolMotif | GINE | Saliency | scaffold | 2 | 200 | 0.960 | 0.999 | 0.992 | 0.977 | 0.764 | 0.048 | 0.510 | 0.229 | 0.355 | 0.776 | 0.017 |
| MolMotif | GINE | SubgraphX | random | 0 | 200 | 0.975 | 0.999 | 0.573 | 0.354 | 0.977 | -0.086 | 0.265 | 0.129 | 0.160 | 0.356 | 0.020 |
| MolMotif | GINE | SubgraphX | random | 1 | 200 | 0.810 | 1.000 | 0.535 | 0.303 | 0.983 | -0.008 | 0.205 | 0.358 | 0.166 | 0.308 | 0.106 |
| MolMotif | GINE | SubgraphX | random | 2 | 200 | 1.000 | 1.000 | 0.556 | 0.323 | 0.977 | -0.013 | 0.320 | 0.159 | 0.320 | 0.390 | 0.003 |
| MolMotif | GINE | SubgraphX | scaffold | 0 | 200 | 0.985 | 1.000 | 0.387 | 0.252 | 0.957 | -0.012 | 0.140 | 0.371 | 0.019 | 0.353 | 0.012 |
| MolMotif | GINE | SubgraphX | scaffold | 1 | 200 | 0.975 | 1.000 | 0.543 | 0.303 | 0.979 | -0.073 | 0.130 | 0.404 | 0.061 | 0.309 | 0.011 |
| MolMotif | GINE | SubgraphX | scaffold | 2 | 200 | 0.960 | 0.999 | 0.476 | 0.240 | 0.947 | 0.065 | 0.335 | 0.311 | 0.308 | 0.353 | 0.017 |
| MolMotif | MPNN | IntegratedGradients | random | 0 | 200 | 1.000 | 1.000 | 0.783 | 0.569 | 0.915 | -0.256 | 0.315 | 0.293 | 0.277 | 0.770 | 0.004 |
| MolMotif | MPNN | IntegratedGradients | random | 1 | 200 | 1.000 | 1.000 | 0.874 | 0.755 | 0.926 | -0.060 | 0.395 | 0.388 | 0.308 | 0.770 | 0.007 |
| MolMotif | MPNN | IntegratedGradients | random | 2 | 200 | 1.000 | 1.000 | 0.962 | 0.863 | 0.860 | -0.057 | 0.460 | 0.451 | 0.457 | 0.772 | 0.002 |
| MolMotif | MPNN | IntegratedGradients | scaffold | 0 | 200 | 1.000 | 1.000 | 0.846 | 0.683 | 0.918 | -0.012 | 0.410 | 0.393 | 0.349 | 0.773 | 0.008 |
| MolMotif | MPNN | IntegratedGradients | scaffold | 1 | 200 | 0.995 | 0.999 | 0.791 | 0.574 | 0.931 | 0.082 | 0.470 | 0.398 | 0.364 | 0.772 | 0.009 |
| MolMotif | MPNN | IntegratedGradients | scaffold | 2 | 200 | 1.000 | 1.000 | 0.976 | 0.925 | 0.899 | 0.095 | 0.420 | 0.407 | 0.330 | 0.775 | 0.007 |
| MolMotifHard | AttentiveFP | IntegratedGradients | random | 0 | 200 | 0.960 | 0.989 | 0.955 | 0.913 | 0.738 | 0.457 | 0.660 | 0.379 | 0.085 | 0.762 | 0.031 |
| MolMotifHard | AttentiveFP | IntegratedGradients | random | 1 | 200 | 0.980 | 0.968 | 0.878 | 0.839 | 0.694 | 0.484 | 0.705 | 0.388 | 0.072 | 0.766 | 0.022 |
| MolMotifHard | AttentiveFP | IntegratedGradients | random | 2 | 200 | 0.975 | 0.985 | 0.801 | 0.718 | 0.675 | 0.486 | 0.550 | 0.466 | 0.103 | 0.764 | 0.018 |
| MolMotifHard | AttentiveFP | IntegratedGradients | scaffold | 0 | 200 | 0.990 | 0.995 | 0.909 | 0.847 | 0.736 | 0.198 | 0.635 | 0.381 | 0.061 | 0.768 | 0.013 |
| MolMotifHard | AttentiveFP | IntegratedGradients | scaffold | 1 | 200 | 0.980 | 0.998 | 0.917 | 0.847 | 0.726 | 0.551 | 0.660 | 0.399 | 0.047 | 0.762 | 0.013 |
| MolMotifHard | AttentiveFP | IntegratedGradients | scaffold | 2 | 200 | 0.955 | 0.991 | 0.874 | 0.782 | 0.741 | 0.199 | 0.535 | 0.385 | 0.116 | 0.764 | 0.027 |
| MolMotifHard | GAT | IntegratedGradients | random | 0 | 200 | 0.980 | 0.994 | 0.929 | 0.881 | 0.705 | 0.070 | 0.485 | 0.453 | 0.268 | 0.761 | 0.018 |
| MolMotifHard | GAT | IntegratedGradients | random | 1 | 200 | 0.915 | 0.982 | 0.663 | 0.645 | 0.719 | 0.033 | 0.545 | 0.439 | 0.439 | 0.762 | 0.036 |
| MolMotifHard | GAT | IntegratedGradients | random | 2 | 200 | 0.990 | 1.000 | 0.788 | 0.784 | 0.673 | 0.021 | 0.420 | 0.506 | 0.506 | 0.760 | 0.005 |
| MolMotifHard | GAT | IntegratedGradients | scaffold | 0 | 200 | 0.965 | 1.000 | 0.908 | 0.816 | 0.748 | 0.027 | 0.485 | 0.369 | 0.291 | 0.769 | 0.021 |
| MolMotifHard | GAT | IntegratedGradients | scaffold | 1 | 200 | 0.950 | 0.992 | 0.732 | 0.642 | 0.771 | -0.127 | 0.520 | 0.371 | 0.371 | 0.761 | 0.037 |
| MolMotifHard | GAT | IntegratedGradients | scaffold | 2 | 200 | 0.960 | 0.998 | 0.782 | 0.754 | 0.743 | -0.034 | 0.555 | 0.405 | 0.405 | 0.765 | 0.023 |
| MolMotifHard | GCN | IntegratedGradients | random | 0 | 200 | 0.910 | 0.999 | 0.850 | 0.821 | 0.718 | 0.305 | 0.670 | 0.469 | 0.509 | 0.760 | 0.022 |
| MolMotifHard | GCN | IntegratedGradients | random | 1 | 200 | 0.770 | 0.976 | 0.946 | 0.904 | 0.700 | -0.296 | 0.255 | 0.173 | 0.075 | 0.762 | 0.117 |
| MolMotifHard | GCN | IntegratedGradients | random | 2 | 200 | 0.975 | 0.988 | 0.908 | 0.839 | 0.684 | 0.110 | 0.535 | 0.436 | 0.481 | 0.764 | 0.026 |
| MolMotifHard | GCN | IntegratedGradients | scaffold | 0 | 200 | 0.890 | 0.999 | 0.910 | 0.796 | 0.765 | 0.186 | 0.645 | 0.226 | 0.533 | 0.766 | 0.031 |
| MolMotifHard | GCN | IntegratedGradients | scaffold | 1 | 200 | 0.870 | 0.990 | 0.716 | 0.574 | 0.773 | 0.269 | 0.690 | 0.436 | 0.550 | 0.765 | 0.048 |
| MolMotifHard | GCN | IntegratedGradients | scaffold | 2 | 200 | 0.775 | 0.995 | 0.972 | 0.913 | 0.732 | -0.377 | 0.335 | 0.120 | 0.120 | 0.762 | 0.118 |
| MolMotifHard | GINE | GNNExplainer | random | 0 | 200 | 0.885 | 0.996 | 0.288 | 0.310 | 0.774 | -0.276 | 0.300 | 0.080 | 0.283 | 0.769 | 0.040 |
| MolMotifHard | GINE | GNNExplainer | random | 1 | 200 | 0.970 | 1.000 | 0.380 | 0.366 | 0.752 | -0.035 | 0.355 | 0.148 | 0.205 | 0.774 | 0.016 |
| MolMotifHard | GINE | GNNExplainer | random | 2 | 200 | 0.950 | 0.998 | 0.571 | 0.480 | 0.737 | 0.086 | 0.465 | 0.196 | 0.266 | 0.771 | 0.024 |
| MolMotifHard | GINE | GNNExplainer | scaffold | 0 | 200 | 0.970 | 0.997 | 0.349 | 0.305 | 0.814 | -0.131 | 0.425 | 0.144 | 0.394 | 0.775 | 0.012 |
| MolMotifHard | GINE | GNNExplainer | scaffold | 1 | 200 | 0.885 | 0.995 | 0.608 | 0.460 | 0.798 | -0.082 | 0.440 | 0.256 | 0.127 | 0.775 | 0.057 |
| MolMotifHard | GINE | GNNExplainer | scaffold | 2 | 200 | 0.820 | 1.000 | 0.303 | 0.281 | 0.810 | -0.289 | 0.340 | 0.139 | 0.154 | 0.775 | 0.064 |
| MolMotifHard | GINE | GuidedBackprop | random | 0 | 200 | 0.885 | 0.996 | 0.856 | 0.794 | 0.805 | 0.006 | 0.370 | 0.313 | 0.275 | 0.755 | 0.040 |
| MolMotifHard | GINE | GuidedBackprop | random | 1 | 200 | 0.970 | 1.000 | 0.978 | 0.954 | 0.795 | 0.025 | 0.385 | 0.134 | 0.205 | 0.763 | 0.016 |
| MolMotifHard | GINE | GuidedBackprop | random | 2 | 200 | 0.950 | 0.998 | 0.923 | 0.921 | 0.790 | -0.181 | 0.350 | 0.164 | 0.250 | 0.758 | 0.024 |
| MolMotifHard | GINE | GuidedBackprop | scaffold | 0 | 200 | 0.970 | 0.997 | 0.956 | 0.948 | 0.816 | -0.047 | 0.385 | 0.385 | 0.310 | 0.766 | 0.012 |
| MolMotifHard | GINE | GuidedBackprop | scaffold | 1 | 200 | 0.885 | 0.995 | 0.846 | 0.796 | 0.840 | -0.010 | 0.485 | 0.234 | 0.111 | 0.765 | 0.057 |
| MolMotifHard | GINE | GuidedBackprop | scaffold | 2 | 200 | 0.820 | 1.000 | 0.824 | 0.710 | 0.812 | -0.350 | 0.325 | 0.235 | 0.138 | 0.767 | 0.064 |
| MolMotifHard | GINE | InputXGradient | random | 0 | 200 | 0.885 | 0.996 | 1.000 | 0.999 | 0.803 | -0.116 | 0.370 | 0.284 | 0.275 | 0.759 | 0.040 |
| MolMotifHard | GINE | InputXGradient | random | 1 | 200 | 0.970 | 1.000 | 1.000 | 1.000 | 0.790 | -0.008 | 0.415 | 0.183 | 0.163 | 0.767 | 0.016 |
| MolMotifHard | GINE | InputXGradient | random | 2 | 200 | 0.950 | 0.998 | 0.988 | 0.984 | 0.802 | -0.081 | 0.405 | 0.216 | 0.225 | 0.762 | 0.024 |
| MolMotifHard | GINE | InputXGradient | scaffold | 0 | 200 | 0.970 | 0.997 | 0.986 | 0.985 | 0.811 | -0.079 | 0.385 | 0.392 | 0.314 | 0.764 | 0.012 |
| MolMotifHard | GINE | InputXGradient | scaffold | 1 | 200 | 0.885 | 0.995 | 0.998 | 0.989 | 0.803 | -0.056 | 0.485 | 0.215 | 0.124 | 0.765 | 0.057 |
| MolMotifHard | GINE | InputXGradient | scaffold | 2 | 200 | 0.820 | 1.000 | 1.000 | 0.996 | 0.788 | -0.383 | 0.335 | 0.213 | 0.159 | 0.764 | 0.064 |
| MolMotifHard | GINE | IntegratedGradients | random | 0 | 200 | 0.885 | 0.996 | 0.983 | 0.978 | 0.726 | -0.205 | 0.380 | 0.284 | 0.275 | 0.761 | 0.040 |
| MolMotifHard | GINE | IntegratedGradients | random | 1 | 200 | 0.970 | 1.000 | 0.989 | 0.980 | 0.773 | 0.048 | 0.425 | 0.202 | 0.129 | 0.767 | 0.016 |
| MolMotifHard | GINE | IntegratedGradients | random | 2 | 200 | 0.950 | 0.998 | 0.982 | 0.960 | 0.722 | -0.064 | 0.405 | 0.168 | 0.290 | 0.764 | 0.024 |
| MolMotifHard | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.970 | 0.997 | 0.988 | 0.988 | 0.790 | -0.137 | 0.390 | 0.403 | 0.304 | 0.763 | 0.012 |
| MolMotifHard | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.885 | 0.995 | 0.993 | 0.969 | 0.775 | -0.019 | 0.505 | 0.243 | 0.092 | 0.766 | 0.057 |
| MolMotifHard | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.820 | 1.000 | 1.000 | 1.000 | 0.773 | -0.448 | 0.315 | 0.279 | 0.169 | 0.763 | 0.064 |
| MolMotifHard | GINE | PGExplainer | random | 0 | 200 | 0.885 | 0.996 | 0.582 | 0.503 | 0.840 | -0.112 | 0.430 | 0.207 | 0.252 | 0.711 | 0.040 |
| MolMotifHard | GINE | PGExplainer | random | 1 | 200 | 0.970 | 1.000 | 0.462 | 0.350 | 0.803 | 0.078 | 0.380 | 0.134 | 0.162 | 0.687 | 0.016 |
| MolMotifHard | GINE | PGExplainer | random | 2 | 200 | 0.950 | 0.998 | 0.493 | 0.403 | 0.827 | -0.118 | 0.410 | 0.146 | 0.210 | 0.719 | 0.024 |
| MolMotifHard | GINE | PGExplainer | scaffold | 0 | 200 | 0.970 | 0.997 | 0.256 | 0.244 | 0.855 | -0.065 | 0.460 | 0.119 | 0.350 | 0.702 | 0.012 |
| MolMotifHard | GINE | PGExplainer | scaffold | 1 | 200 | 0.885 | 0.995 | 0.308 | 0.260 | 0.882 | 0.035 | 0.425 | 0.075 | 0.201 | 0.696 | 0.057 |
| MolMotifHard | GINE | PGExplainer | scaffold | 2 | 200 | 0.820 | 1.000 | 0.565 | 0.396 | 0.764 | -0.230 | 0.340 | 0.067 | 0.154 | 0.584 | 0.064 |
| MolMotifHard | GINE | Saliency | random | 0 | 200 | 0.885 | 0.996 | 1.000 | 1.000 | 0.807 | -0.107 | 0.365 | 0.293 | 0.275 | 0.757 | 0.040 |
| MolMotifHard | GINE | Saliency | random | 1 | 200 | 0.970 | 1.000 | 0.999 | 0.998 | 0.796 | -0.007 | 0.410 | 0.157 | 0.169 | 0.767 | 0.016 |
| MolMotifHard | GINE | Saliency | random | 2 | 200 | 0.950 | 0.998 | 0.994 | 0.991 | 0.794 | -0.077 | 0.405 | 0.200 | 0.208 | 0.765 | 0.024 |
| MolMotifHard | GINE | Saliency | scaffold | 0 | 200 | 0.970 | 0.997 | 0.999 | 0.995 | 0.817 | -0.045 | 0.390 | 0.378 | 0.312 | 0.762 | 0.012 |
| MolMotifHard | GINE | Saliency | scaffold | 1 | 200 | 0.885 | 0.995 | 0.999 | 0.993 | 0.811 | -0.041 | 0.485 | 0.206 | 0.165 | 0.764 | 0.057 |
| MolMotifHard | GINE | Saliency | scaffold | 2 | 200 | 0.820 | 1.000 | 1.000 | 0.996 | 0.791 | -0.408 | 0.330 | 0.249 | 0.157 | 0.765 | 0.064 |
| MolMotifHard | GINE | SubgraphX | random | 0 | 200 | 0.885 | 0.996 | 0.362 | 0.333 | 0.929 | -0.280 | 0.315 | 0.218 | 0.275 | 0.406 | 0.040 |
| MolMotifHard | GINE | SubgraphX | random | 1 | 200 | 0.970 | 1.000 | 0.442 | 0.330 | 0.913 | -0.012 | 0.295 | 0.163 | 0.057 | 0.344 | 0.016 |
| MolMotifHard | GINE | SubgraphX | random | 2 | 200 | 0.950 | 0.998 | 0.421 | 0.298 | 0.919 | 0.171 | 0.400 | 0.222 | 0.117 | 0.307 | 0.024 |
| MolMotifHard | GINE | SubgraphX | scaffold | 0 | 200 | 0.970 | 0.997 | 0.436 | 0.255 | 0.932 | 0.033 | 0.530 | 0.330 | 0.304 | 0.327 | 0.012 |
| MolMotifHard | GINE | SubgraphX | scaffold | 1 | 200 | 0.885 | 0.995 | 0.537 | 0.342 | 0.926 | -0.123 | 0.360 | 0.258 | 0.037 | 0.376 | 0.057 |
| MolMotifHard | GINE | SubgraphX | scaffold | 2 | 200 | 0.820 | 1.000 | 0.443 | 0.333 | 0.937 | -0.300 | 0.345 | 0.127 | 0.183 | 0.347 | 0.064 |
| MolMotifHard | MPNN | IntegratedGradients | random | 0 | 200 | 0.975 | 0.998 | 0.923 | 0.880 | 0.765 | 0.038 | 0.475 | 0.305 | 0.285 | 0.760 | 0.015 |
| MolMotifHard | MPNN | IntegratedGradients | random | 1 | 200 | 0.980 | 0.999 | 0.968 | 0.943 | 0.776 | 0.500 | 0.780 | 0.405 | 0.081 | 0.764 | 0.014 |
| MolMotifHard | MPNN | IntegratedGradients | random | 2 | 200 | 0.770 | 0.991 | 0.969 | 0.936 | 0.753 | 0.392 | 0.575 | 0.158 | 0.301 | 0.766 | 0.075 |
| MolMotifHard | MPNN | IntegratedGradients | scaffold | 0 | 200 | 0.980 | 0.995 | 0.976 | 0.942 | 0.806 | 0.536 | 0.755 | 0.457 | 0.075 | 0.763 | 0.007 |
| MolMotifHard | MPNN | IntegratedGradients | scaffold | 1 | 200 | 0.985 | 0.999 | 0.938 | 0.864 | 0.764 | 0.566 | 0.755 | 0.431 | 0.140 | 0.766 | 0.005 |
| MolMotifHard | MPNN | IntegratedGradients | scaffold | 2 | 200 | 0.995 | 1.000 | 0.982 | 0.966 | 0.839 | 0.633 | 0.815 | 0.553 | 0.064 | 0.765 | 0.013 |
| SIDER | GCN | IntegratedGradients | random | 0 | 200 | 0.675 | 0.677 | — | — | 0.748 | 0.514 | 0.720 | 0.145 | 0.252 | 0.751 | 0.050 |
| SIDER | GCN | IntegratedGradients | random | 1 | 200 | 0.625 | 0.636 | — | — | 0.737 | 0.074 | 0.555 | 0.070 | 0.085 | 0.759 | 0.085 |
| SIDER | GCN | IntegratedGradients | random | 2 | 200 | 0.630 | 0.668 | — | — | 0.746 | -0.110 | 0.430 | 0.084 | 0.022 | 0.751 | 0.048 |
| SIDER | GCN | IntegratedGradients | scaffold | 0 | 200 | 0.570 | 0.668 | — | — | 0.750 | 0.468 | 0.765 | 0.211 | 0.323 | 0.764 | 0.028 |
| SIDER | GCN | IntegratedGradients | scaffold | 1 | 200 | 0.560 | 0.660 | — | — | 0.740 | 0.397 | 0.740 | 0.211 | 0.364 | 0.765 | 0.013 |
| SIDER | GCN | IntegratedGradients | scaffold | 2 | 200 | 0.595 | 0.675 | — | — | 0.754 | 0.231 | 0.660 | 0.121 | 0.248 | 0.762 | 0.044 |
| SIDER | GINE | IntegratedGradients | random | 0 | 200 | 0.665 | 0.682 | — | — | 0.782 | 0.526 | 0.675 | 0.159 | 0.304 | 0.752 | 0.049 |
| SIDER | GINE | IntegratedGradients | random | 1 | 200 | 0.615 | 0.628 | — | — | 0.746 | -0.122 | 0.445 | 0.030 | 0.030 | 0.761 | 0.085 |
| SIDER | GINE | IntegratedGradients | random | 2 | 200 | 0.645 | 0.703 | — | — | 0.764 | 0.427 | 0.720 | 0.333 | 0.389 | 0.754 | 0.077 |
| SIDER | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.550 | 0.647 | — | — | 0.750 | 0.249 | 0.390 | 0.073 | 0.117 | 0.764 | 0.039 |
| SIDER | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.555 | 0.617 | — | — | 0.767 | 0.555 | 0.800 | 0.391 | 0.426 | 0.763 | 0.043 |
| SIDER | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.560 | 0.618 | — | — | 0.743 | 0.503 | 0.775 | 0.235 | 0.318 | 0.763 | 0.017 |
| ShapeGGen | GINE | GNNExplainer | random | 0 | 50 | 0.740 | 0.667 | 0.555 | 0.613 | 0.092 | 0.470 | 0.280 | 0.410 | 0.251 | 0.770 | 0.143 |
| ShapeGGen | GINE | GNNExplainer | random | 1 | 50 | 0.820 | 0.455 | 0.610 | 0.646 | 0.083 | 0.544 | 0.260 | 0.305 | 0.207 | 0.772 | 0.202 |
| ShapeGGen | GINE | GNNExplainer | random | 2 | 50 | 0.780 | 0.613 | 0.483 | 0.514 | 0.069 | 0.154 | 0.100 | 0.003 | 0.008 | 0.776 | 0.233 |
| ShapeGGen | GINE | GNNExplainer | scaffold | 0 | 50 | 0.700 | 0.448 | 0.728 | 0.753 | 0.092 | 0.442 | 0.480 | 0.086 | 0.063 | 0.771 | 0.055 |
| ShapeGGen | GINE | GNNExplainer | scaffold | 1 | 50 | 0.260 | 0.583 | 0.499 | 0.566 | 0.076 | -0.098 | 0.020 | -0.002 | -0.005 | 0.771 | 0.241 |
| ShapeGGen | GINE | GNNExplainer | scaffold | 2 | 50 | 0.780 | 0.625 | 0.496 | 0.565 | 0.076 | 0.085 | 0.060 | 0.001 | 0.003 | 0.771 | 0.254 |
| ShapeGGen | GINE | GuidedBackprop | random | 0 | 50 | 0.740 | 0.667 | 0.754 | 0.825 | 0.186 | 0.424 | 0.420 | 0.359 | 0.294 | 0.770 | 0.143 |
| ShapeGGen | GINE | GuidedBackprop | random | 1 | 50 | 0.820 | 0.455 | 0.775 | 0.797 | 0.175 | 0.555 | 0.540 | 0.349 | 0.187 | 0.772 | 0.202 |
| ShapeGGen | GINE | GuidedBackprop | random | 2 | 50 | 0.780 | 0.613 | 0.791 | 0.810 | 0.160 | 0.465 | 0.460 | 0.008 | 0.003 | 0.776 | 0.233 |
| ShapeGGen | GINE | GuidedBackprop | scaffold | 0 | 50 | 0.700 | 0.448 | 0.803 | 0.838 | 0.163 | 0.475 | 0.400 | 0.079 | 0.053 | 0.771 | 0.055 |
| ShapeGGen | GINE | GuidedBackprop | scaffold | 1 | 50 | 0.260 | 0.583 | 0.833 | 0.844 | 0.162 | 0.020 | 0.080 | -0.001 | -0.007 | 0.771 | 0.241 |
| ShapeGGen | GINE | GuidedBackprop | scaffold | 2 | 50 | 0.780 | 0.625 | 0.773 | 0.797 | 0.164 | 0.186 | 0.360 | 0.004 | -0.001 | 0.771 | 0.254 |
| ShapeGGen | GINE | InputXGradient | random | 0 | 50 | 0.740 | 0.667 | 0.724 | 0.791 | 0.201 | 0.378 | 0.400 | 0.407 | 0.270 | 0.770 | 0.143 |
| ShapeGGen | GINE | InputXGradient | random | 1 | 50 | 0.820 | 0.455 | 0.718 | 0.753 | 0.188 | 0.453 | 0.580 | 0.334 | 0.239 | 0.772 | 0.202 |
| ShapeGGen | GINE | InputXGradient | random | 2 | 50 | 0.780 | 0.613 | 0.732 | 0.747 | 0.174 | 0.473 | 0.540 | 0.008 | 0.003 | 0.776 | 0.233 |
| ShapeGGen | GINE | InputXGradient | scaffold | 0 | 50 | 0.700 | 0.448 | 0.733 | 0.766 | 0.179 | 0.325 | 0.440 | 0.061 | 0.072 | 0.771 | 0.055 |
| ShapeGGen | GINE | InputXGradient | scaffold | 1 | 50 | 0.260 | 0.583 | 0.716 | 0.739 | 0.172 | -0.233 | 0.100 | -0.003 | -0.004 | 0.771 | 0.241 |
| ShapeGGen | GINE | InputXGradient | scaffold | 2 | 50 | 0.780 | 0.625 | 0.676 | 0.701 | 0.182 | 0.337 | 0.460 | 0.005 | -0.002 | 0.771 | 0.254 |
| ShapeGGen | GINE | IntegratedGradients | random | 0 | 50 | 0.740 | 0.667 | 0.732 | 0.787 | 0.194 | 0.375 | 0.420 | 0.412 | 0.259 | 0.770 | 0.143 |
| ShapeGGen | GINE | IntegratedGradients | random | 1 | 50 | 0.820 | 0.455 | 0.716 | 0.755 | 0.180 | 0.469 | 0.600 | 0.378 | 0.199 | 0.772 | 0.202 |
| ShapeGGen | GINE | IntegratedGradients | random | 2 | 50 | 0.780 | 0.613 | 0.751 | 0.770 | 0.172 | 0.497 | 0.580 | 0.008 | 0.003 | 0.776 | 0.233 |
| ShapeGGen | GINE | IntegratedGradients | scaffold | 0 | 50 | 0.700 | 0.448 | 0.769 | 0.788 | 0.162 | 0.304 | 0.340 | 0.074 | 0.062 | 0.771 | 0.055 |
| ShapeGGen | GINE | IntegratedGradients | scaffold | 1 | 50 | 0.260 | 0.583 | 0.704 | 0.728 | 0.170 | -0.273 | 0.060 | -0.004 | -0.003 | 0.771 | 0.241 |
| ShapeGGen | GINE | IntegratedGradients | scaffold | 2 | 50 | 0.780 | 0.625 | 0.708 | 0.732 | 0.183 | 0.303 | 0.460 | 0.005 | -0.002 | 0.771 | 0.254 |
| ShapeGGen | GINE | PGExplainer | random | 0 | 50 | 0.740 | 0.667 | 0.503 | 0.541 | 0.349 | -0.098 | 0.020 | 0.236 | 0.316 | 0.589 | 0.143 |
| ShapeGGen | GINE | PGExplainer | random | 1 | 50 | 0.820 | 0.455 | 0.506 | 0.509 | 0.222 | -0.223 | 0.020 | 0.142 | 0.572 | 0.749 | 0.202 |
| ShapeGGen | GINE | PGExplainer | random | 2 | 50 | 0.780 | 0.613 | 0.489 | 0.520 | 0.429 | -0.167 | 0.000 | 0.002 | 0.009 | 0.698 | 0.233 |
| ShapeGGen | GINE | PGExplainer | scaffold | 0 | 50 | 0.700 | 0.448 | 0.491 | 0.525 | 0.303 | -0.127 | 0.020 | 0.064 | 0.103 | 0.608 | 0.055 |
| ShapeGGen | GINE | PGExplainer | scaffold | 1 | 50 | 0.260 | 0.583 | 0.595 | 0.640 | 0.477 | 0.118 | 0.080 | -0.001 | -0.005 | 0.766 | 0.241 |
| ShapeGGen | GINE | PGExplainer | scaffold | 2 | 50 | 0.780 | 0.625 | 0.615 | 0.667 | 0.458 | -0.177 | 0.000 | -0.000 | 0.004 | 0.764 | 0.254 |
| ShapeGGen | GINE | Saliency | random | 0 | 50 | 0.740 | 0.667 | 0.762 | 0.825 | 0.186 | 0.336 | 0.400 | 0.349 | 0.313 | 0.770 | 0.143 |
| ShapeGGen | GINE | Saliency | random | 1 | 50 | 0.820 | 0.455 | 0.776 | 0.803 | 0.173 | 0.439 | 0.520 | 0.329 | 0.256 | 0.772 | 0.202 |
| ShapeGGen | GINE | Saliency | random | 2 | 50 | 0.780 | 0.613 | 0.769 | 0.795 | 0.159 | 0.425 | 0.400 | 0.007 | 0.003 | 0.776 | 0.233 |
| ShapeGGen | GINE | Saliency | scaffold | 0 | 50 | 0.700 | 0.448 | 0.799 | 0.822 | 0.162 | 0.330 | 0.320 | 0.057 | 0.083 | 0.771 | 0.055 |
| ShapeGGen | GINE | Saliency | scaffold | 1 | 50 | 0.260 | 0.583 | 0.787 | 0.818 | 0.159 | -0.136 | 0.140 | -0.002 | -0.005 | 0.771 | 0.241 |
| ShapeGGen | GINE | Saliency | scaffold | 2 | 50 | 0.780 | 0.625 | 0.742 | 0.764 | 0.164 | 0.297 | 0.460 | 0.005 | -0.002 | 0.771 | 0.254 |
| ShapeGGen | GINE | SubgraphX | random | 0 | 50 | 0.740 | 0.667 | 0.676 | 0.637 | 0.198 | 0.552 | 0.080 | 0.527 | -0.002 | 0.461 | 0.143 |
| ShapeGGen | GINE | SubgraphX | random | 1 | 50 | 0.820 | 0.455 | 0.637 | 0.571 | 0.151 | 0.607 | 0.040 | 0.671 | -0.028 | 0.522 | 0.202 |
| ShapeGGen | GINE | SubgraphX | random | 2 | 50 | 0.780 | 0.613 | 0.620 | 0.568 | 0.180 | 0.471 | 0.180 | 0.011 | -0.000 | 0.567 | 0.233 |
| ShapeGGen | GINE | SubgraphX | scaffold | 0 | 50 | 0.700 | 0.448 | 0.666 | 0.608 | 0.162 | 0.578 | 0.220 | 0.170 | -0.007 | 0.452 | 0.055 |
| ShapeGGen | GINE | SubgraphX | scaffold | 1 | 50 | 0.260 | 0.583 | 0.581 | 0.576 | 0.287 | 0.230 | 0.200 | -0.000 | -0.006 | 0.520 | 0.241 |
| ShapeGGen | GINE | SubgraphX | scaffold | 2 | 50 | 0.780 | 0.625 | 0.548 | 0.556 | 0.231 | 0.413 | 0.240 | 0.007 | -0.004 | 0.514 | 0.254 |
| SynthMotifs | AttentiveFP | IntegratedGradients | random | 0 | 200 | 0.975 | 1.000 | 0.776 | 0.601 | 0.205 | 0.004 | 0.305 | 0.489 | 0.394 | 0.795 | 0.013 |
| SynthMotifs | AttentiveFP | IntegratedGradients | random | 1 | 200 | 0.985 | 0.997 | 0.940 | 0.828 | 0.223 | 0.448 | 0.535 | 0.464 | 0.092 | 0.797 | 0.009 |
| SynthMotifs | AttentiveFP | IntegratedGradients | random | 2 | 200 | 0.980 | 1.000 | 0.898 | 0.733 | 0.146 | 0.104 | 0.120 | 0.369 | 0.204 | 0.796 | 0.020 |
| SynthMotifs | AttentiveFP | IntegratedGradients | scaffold | 0 | 200 | 0.930 | 0.999 | 0.823 | 0.657 | 0.162 | 0.311 | 0.355 | 0.318 | 0.104 | 0.794 | 0.020 |
| SynthMotifs | AttentiveFP | IntegratedGradients | scaffold | 1 | 200 | 0.980 | 1.000 | 0.879 | 0.648 | 0.179 | 0.339 | 0.360 | 0.385 | 0.368 | 0.794 | 0.018 |
| SynthMotifs | AttentiveFP | IntegratedGradients | scaffold | 2 | 200 | 0.980 | 1.000 | 0.909 | 0.760 | 0.147 | 0.159 | 0.060 | 0.421 | 0.139 | 0.795 | 0.011 |
| SynthMotifs | GAT | IntegratedGradients | random | 0 | 200 | 0.995 | 1.000 | 0.920 | 0.753 | 0.123 | 0.367 | 0.255 | 0.322 | 0.168 | 0.795 | 0.023 |
| SynthMotifs | GAT | IntegratedGradients | random | 1 | 200 | 0.980 | 1.000 | 0.816 | 0.675 | 0.175 | 0.129 | 0.075 | 0.216 | 0.139 | 0.795 | 0.009 |
| SynthMotifs | GAT | IntegratedGradients | random | 2 | 200 | 0.995 | 1.000 | 0.642 | 0.553 | 0.119 | 0.230 | 0.025 | 0.315 | 0.319 | 0.792 | 0.013 |
| SynthMotifs | GAT | IntegratedGradients | scaffold | 0 | 200 | 0.995 | 1.000 | 0.832 | 0.642 | 0.097 | 0.326 | 0.145 | 0.425 | 0.364 | 0.795 | 0.009 |
| SynthMotifs | GAT | IntegratedGradients | scaffold | 1 | 200 | 0.625 | 0.999 | 0.985 | 0.940 | 0.106 | 0.630 | 0.340 | 0.607 | 0.078 | 0.797 | 0.201 |
| SynthMotifs | GAT | IntegratedGradients | scaffold | 2 | 200 | 0.995 | 1.000 | 0.920 | 0.879 | 0.120 | 0.335 | 0.235 | 0.455 | 0.364 | 0.797 | 0.003 |
| SynthMotifs | GCN | IntegratedGradients | random | 0 | 200 | 0.695 | 1.000 | 0.583 | 0.407 | 0.103 | 0.421 | 0.200 | 0.146 | 0.167 | 0.795 | 0.242 |
| SynthMotifs | GCN | IntegratedGradients | random | 1 | 200 | 0.980 | 1.000 | 0.983 | 0.931 | 0.152 | 0.390 | 0.675 | 0.379 | 0.147 | 0.796 | 0.011 |
| SynthMotifs | GCN | IntegratedGradients | random | 2 | 200 | 0.990 | 1.000 | 0.990 | 0.962 | 0.169 | 0.433 | 0.705 | 0.443 | 0.062 | 0.798 | 0.009 |
| SynthMotifs | GCN | IntegratedGradients | scaffold | 0 | 200 | 0.630 | 0.993 | 0.945 | 0.784 | 0.118 | 0.413 | 0.455 | 0.138 | 0.137 | 0.793 | 0.177 |
| SynthMotifs | GCN | IntegratedGradients | scaffold | 1 | 200 | 0.975 | 0.998 | 0.934 | 0.774 | 0.141 | 0.299 | 0.615 | 0.288 | 0.179 | 0.795 | 0.014 |
| SynthMotifs | GCN | IntegratedGradients | scaffold | 2 | 200 | 0.975 | 0.997 | 0.981 | 0.919 | 0.169 | 0.344 | 0.765 | 0.313 | 0.117 | 0.798 | 0.016 |
| SynthMotifs | GINE | GNNExplainer | random | 0 | 200 | 0.985 | 1.000 | 0.564 | 0.293 | 0.037 | 0.068 | 0.055 | 0.197 | 0.221 | 0.800 | 0.000 |
| SynthMotifs | GINE | GNNExplainer | random | 1 | 200 | 0.985 | 1.000 | 0.635 | 0.397 | 0.046 | 0.103 | 0.095 | 0.283 | 0.282 | 0.800 | 0.009 |
| SynthMotifs | GINE | GNNExplainer | random | 2 | 200 | 0.945 | 1.000 | 0.698 | 0.474 | 0.048 | 0.199 | 0.045 | 0.217 | 0.251 | 0.800 | 0.020 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 0 | 200 | 0.910 | 1.000 | 0.474 | 0.235 | 0.039 | -0.035 | 0.020 | 0.137 | 0.388 | 0.800 | 0.027 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 1 | 200 | 0.960 | 1.000 | 0.878 | 0.663 | 0.046 | 0.236 | 0.160 | 0.395 | 0.258 | 0.800 | 0.011 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 2 | 200 | 0.970 | 1.000 | 0.575 | 0.293 | 0.046 | 0.076 | 0.075 | 0.448 | 0.377 | 0.800 | 0.006 |
| SynthMotifs | GINE | GuidedBackprop | random | 0 | 200 | 0.985 | 1.000 | 0.999 | 0.996 | 0.178 | 0.645 | 0.475 | 0.235 | 0.081 | 0.800 | 0.000 |
| SynthMotifs | GINE | GuidedBackprop | random | 1 | 200 | 0.985 | 1.000 | 0.989 | 0.969 | 0.157 | 0.662 | 0.255 | 0.321 | 0.043 | 0.799 | 0.009 |
| SynthMotifs | GINE | GuidedBackprop | random | 2 | 200 | 0.945 | 1.000 | 0.996 | 0.983 | 0.164 | 0.613 | 0.350 | 0.261 | 0.059 | 0.800 | 0.020 |
| SynthMotifs | GINE | GuidedBackprop | scaffold | 0 | 200 | 0.910 | 1.000 | 0.981 | 0.947 | 0.153 | 0.539 | 0.500 | 0.403 | -0.021 | 0.798 | 0.027 |
| SynthMotifs | GINE | GuidedBackprop | scaffold | 1 | 200 | 0.960 | 1.000 | 0.972 | 0.934 | 0.133 | 0.694 | 0.345 | 0.409 | 0.074 | 0.798 | 0.011 |
| SynthMotifs | GINE | GuidedBackprop | scaffold | 2 | 200 | 0.970 | 1.000 | 0.970 | 0.902 | 0.126 | 0.635 | 0.280 | 0.461 | 0.081 | 0.796 | 0.006 |
| SynthMotifs | GINE | InputXGradient | random | 0 | 200 | 0.985 | 1.000 | 0.987 | 0.956 | 0.194 | 0.488 | 0.220 | 0.244 | 0.109 | 0.798 | 0.000 |
| SynthMotifs | GINE | InputXGradient | random | 1 | 200 | 0.985 | 1.000 | 0.963 | 0.872 | 0.229 | 0.439 | 0.170 | 0.314 | 0.092 | 0.793 | 0.009 |
| SynthMotifs | GINE | InputXGradient | random | 2 | 200 | 0.945 | 1.000 | 0.959 | 0.870 | 0.238 | 0.498 | 0.150 | 0.261 | 0.132 | 0.795 | 0.020 |
| SynthMotifs | GINE | InputXGradient | scaffold | 0 | 200 | 0.910 | 1.000 | 0.992 | 0.962 | 0.159 | 0.418 | 0.175 | 0.388 | 0.040 | 0.799 | 0.027 |
| SynthMotifs | GINE | InputXGradient | scaffold | 1 | 200 | 0.960 | 1.000 | 0.911 | 0.778 | 0.209 | 0.412 | 0.215 | 0.389 | 0.171 | 0.795 | 0.011 |
| SynthMotifs | GINE | InputXGradient | scaffold | 2 | 200 | 0.970 | 1.000 | 0.961 | 0.856 | 0.204 | 0.433 | 0.195 | 0.433 | 0.187 | 0.797 | 0.006 |
| SynthMotifs | GINE | IntegratedGradients | random | 0 | 200 | 0.985 | 1.000 | 0.997 | 0.987 | 0.194 | 0.490 | 0.425 | 0.233 | 0.090 | 0.800 | 0.000 |
| SynthMotifs | GINE | IntegratedGradients | random | 1 | 200 | 0.985 | 1.000 | 0.996 | 0.980 | 0.198 | 0.448 | 0.490 | 0.307 | 0.066 | 0.799 | 0.009 |
| SynthMotifs | GINE | IntegratedGradients | random | 2 | 200 | 0.945 | 1.000 | 0.977 | 0.912 | 0.162 | 0.479 | 0.510 | 0.256 | 0.129 | 0.799 | 0.020 |
| SynthMotifs | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.910 | 1.000 | 0.977 | 0.914 | 0.218 | 0.433 | 0.365 | 0.387 | 0.001 | 0.797 | 0.027 |
| SynthMotifs | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.960 | 1.000 | 0.976 | 0.911 | 0.199 | 0.464 | 0.675 | 0.375 | 0.087 | 0.797 | 0.011 |
| SynthMotifs | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.970 | 1.000 | 0.966 | 0.878 | 0.158 | 0.480 | 0.340 | 0.474 | 0.106 | 0.798 | 0.006 |
| SynthMotifs | GINE | PGExplainer | random | 0 | 200 | 0.985 | 1.000 | 0.460 | 0.192 | 0.303 | -0.078 | 0.015 | 0.138 | 0.114 | 0.434 | 0.000 |
| SynthMotifs | GINE | PGExplainer | random | 1 | 200 | 0.985 | 1.000 | 0.471 | 0.261 | 0.379 | -0.025 | 0.000 | 0.125 | 0.302 | 0.785 | 0.009 |
| SynthMotifs | GINE | PGExplainer | random | 2 | 200 | 0.945 | 1.000 | 0.314 | 0.174 | 0.385 | -0.149 | 0.000 | 0.010 | 0.263 | 0.786 | 0.020 |
| SynthMotifs | GINE | PGExplainer | scaffold | 0 | 200 | 0.910 | 1.000 | 0.442 | 0.206 | 0.419 | 0.059 | 0.010 | 0.217 | 0.284 | 0.573 | 0.027 |
| SynthMotifs | GINE | PGExplainer | scaffold | 1 | 200 | 0.960 | 1.000 | 0.290 | 0.166 | 0.364 | -0.178 | 0.000 | 0.014 | 0.348 | 0.752 | 0.011 |
| SynthMotifs | GINE | PGExplainer | scaffold | 2 | 200 | 0.970 | 1.000 | 0.331 | 0.170 | 0.393 | -0.101 | 0.000 | 0.084 | 0.385 | 0.734 | 0.006 |
| SynthMotifs | GINE | Saliency | random | 0 | 200 | 0.985 | 1.000 | 0.993 | 0.976 | 0.172 | 0.493 | 0.315 | 0.248 | 0.095 | 0.798 | 0.000 |
| SynthMotifs | GINE | Saliency | random | 1 | 200 | 0.985 | 1.000 | 0.983 | 0.934 | 0.197 | 0.460 | 0.150 | 0.311 | 0.080 | 0.797 | 0.009 |
| SynthMotifs | GINE | Saliency | random | 2 | 200 | 0.945 | 1.000 | 0.960 | 0.870 | 0.176 | 0.513 | 0.140 | 0.262 | 0.141 | 0.796 | 0.020 |
| SynthMotifs | GINE | Saliency | scaffold | 0 | 200 | 0.910 | 1.000 | 0.986 | 0.942 | 0.146 | 0.395 | 0.015 | 0.389 | 0.111 | 0.795 | 0.027 |
| SynthMotifs | GINE | Saliency | scaffold | 1 | 200 | 0.960 | 1.000 | 0.916 | 0.822 | 0.164 | 0.388 | 0.220 | 0.362 | 0.199 | 0.791 | 0.011 |
| SynthMotifs | GINE | Saliency | scaffold | 2 | 200 | 0.970 | 1.000 | 0.969 | 0.893 | 0.148 | 0.420 | 0.195 | 0.430 | 0.144 | 0.797 | 0.006 |
| SynthMotifs | GINE | SubgraphX | random | 0 | 200 | 0.985 | 1.000 | 0.642 | 0.430 | 0.175 | 0.308 | 0.030 | 0.181 | 0.088 | 0.578 | 0.000 |
| SynthMotifs | GINE | SubgraphX | random | 1 | 200 | 0.985 | 1.000 | 0.824 | 0.594 | 0.165 | 0.519 | 0.085 | 0.320 | 0.036 | 0.545 | 0.009 |
| SynthMotifs | GINE | SubgraphX | random | 2 | 200 | 0.945 | 1.000 | 0.845 | 0.575 | 0.159 | 0.551 | 0.020 | 0.234 | 0.044 | 0.659 | 0.020 |
| SynthMotifs | GINE | SubgraphX | scaffold | 0 | 200 | 0.910 | 1.000 | 0.631 | 0.349 | 0.277 | 0.046 | 0.000 | 0.325 | 0.012 | 0.350 | 0.027 |
| SynthMotifs | GINE | SubgraphX | scaffold | 1 | 200 | 0.960 | 1.000 | 0.844 | 0.569 | 0.172 | 0.373 | 0.020 | 0.371 | 0.029 | 0.659 | 0.011 |
| SynthMotifs | GINE | SubgraphX | scaffold | 2 | 200 | 0.970 | 1.000 | 0.779 | 0.581 | 0.179 | 0.431 | 0.105 | 0.436 | 0.094 | 0.518 | 0.006 |
| SynthMotifs | MPNN | IntegratedGradients | random | 0 | 200 | 0.985 | 1.000 | 0.812 | 0.651 | 0.115 | 0.300 | 0.410 | 0.411 | 0.412 | 0.795 | 0.025 |
| SynthMotifs | MPNN | IntegratedGradients | random | 1 | 200 | 0.995 | 1.000 | 0.900 | 0.745 | 0.137 | 0.313 | 0.380 | 0.391 | 0.355 | 0.795 | 0.010 |
| SynthMotifs | MPNN | IntegratedGradients | random | 2 | 200 | 1.000 | 1.000 | 0.903 | 0.685 | 0.090 | 0.399 | 0.310 | 0.468 | 0.485 | 0.796 | 0.005 |
| SynthMotifs | MPNN | IntegratedGradients | scaffold | 0 | 200 | 0.980 | 1.000 | 0.829 | 0.613 | 0.102 | 0.237 | 0.350 | 0.418 | 0.437 | 0.791 | 0.015 |
| SynthMotifs | MPNN | IntegratedGradients | scaffold | 1 | 200 | 0.820 | 0.999 | 0.847 | 0.731 | 0.154 | 0.196 | 0.480 | 0.212 | 0.182 | 0.793 | 0.020 |
| SynthMotifs | MPNN | IntegratedGradients | scaffold | 2 | 200 | 0.715 | 0.998 | 0.860 | 0.608 | 0.139 | 0.241 | 0.360 | 0.322 | 0.245 | 0.795 | 0.111 |
| Tox21 | GINE | IntegratedGradients | random | 0 | 200 | 0.940 | 0.849 | — | — | 0.734 | -0.617 | 0.215 | -0.037 | -0.053 | 0.757 | 0.099 |
| Tox21 | GINE | IntegratedGradients | random | 1 | 200 | 0.955 | 0.792 | — | — | 0.788 | -0.127 | 0.420 | -0.012 | -0.012 | 0.757 | 0.148 |
| Tox21 | GINE | IntegratedGradients | random | 2 | 200 | 0.925 | 0.820 | — | — | 0.725 | -0.063 | 0.365 | -0.096 | -0.060 | 0.753 | 0.093 |
| Tox21 | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.945 | 0.742 | — | — | 0.801 | -0.122 | 0.450 | 0.021 | 0.023 | 0.745 | 0.053 |
| Tox21 | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.960 | 0.739 | — | — | 0.799 | -0.525 | 0.360 | -0.076 | -0.069 | 0.745 | 0.023 |
| Tox21 | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.920 | 0.755 | — | — | 0.781 | -0.592 | 0.395 | -0.156 | -0.159 | 0.736 | 0.045 |
| hERG | GINE | IntegratedGradients | random | 0 | 197 | 0.792 | 0.824 | — | — | 0.783 | 0.636 | 0.822 | 0.576 | 0.576 | 0.779 | 0.093 |
| hERG | GINE | IntegratedGradients | random | 1 | 197 | 0.431 | 0.823 | — | — | 0.726 | -0.691 | 0.142 | -0.188 | -0.188 | 0.777 | 0.167 |
| hERG | GINE | IntegratedGradients | random | 2 | 197 | 0.741 | 0.815 | — | — | 0.773 | 0.776 | 0.909 | 0.765 | 0.765 | 0.779 | 0.067 |
| hERG | GINE | IntegratedGradients | scaffold | 0 | 197 | 0.533 | 0.693 | — | — | 0.795 | 0.639 | 0.838 | 0.676 | 0.676 | 0.776 | 0.404 |
| hERG | GINE | IntegratedGradients | scaffold | 1 | 197 | 0.462 | 0.639 | — | — | 0.784 | 0.727 | 0.858 | 0.661 | 0.661 | 0.777 | 0.477 |
| hERG | GINE | IntegratedGradients | scaffold | 2 | 197 | 0.421 | 0.628 | — | — | 0.794 | 0.863 | 0.934 | 0.854 | 0.854 | 0.777 | 0.523 |

## Regression audit matrix

| dataset | backbone | attributor | split | seed | n_mol | rmse | mae | r2 | motif_top1 | occ_spearman | occ_top1 | fid+ | fid- | sparsity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ESOL | GAT | IntegratedGradients | random | 0 | 200 | 0.730 | 0.549 | 0.888 | 0.828 | 0.805 | 0.945 | 3.257 | 6.809 | 0.734 |
| ESOL | GAT | IntegratedGradients | random | 1 | 200 | 0.810 | 0.608 | 0.834 | 0.823 | 0.762 | 0.915 | 2.572 | 3.999 | 0.736 |
| ESOL | GAT | IntegratedGradients | random | 2 | 200 | 0.751 | 0.548 | 0.878 | 0.842 | 0.841 | 0.940 | 3.505 | 7.619 | 0.734 |
| ESOL | GAT | IntegratedGradients | scaffold | 0 | 200 | 1.255 | 0.842 | 0.653 | 0.862 | 0.848 | 0.975 | 9.119 | 35.850 | 0.718 |
| ESOL | GAT | IntegratedGradients | scaffold | 1 | 200 | 0.995 | 0.806 | 0.782 | 0.869 | 0.839 | 0.960 | 5.117 | 9.872 | 0.719 |
| ESOL | GAT | IntegratedGradients | scaffold | 2 | 200 | 0.991 | 0.770 | 0.784 | 0.862 | 0.879 | 0.980 | 8.272 | 36.696 | 0.716 |
| ESOL | GCN | IntegratedGradients | random | 0 | 200 | 0.951 | 0.746 | 0.809 | 0.855 | 0.512 | 0.695 | -0.859 | -0.928 | 0.733 |
| ESOL | GCN | IntegratedGradients | random | 1 | 200 | 0.929 | 0.723 | 0.782 | 0.849 | 0.506 | 0.745 | -0.937 | -1.014 | 0.736 |
| ESOL | GCN | IntegratedGradients | random | 2 | 200 | 0.961 | 0.742 | 0.800 | 0.859 | 0.251 | 0.510 | -0.716 | -0.758 | 0.731 |
| ESOL | GCN | IntegratedGradients | scaffold | 0 | 200 | 1.038 | 0.837 | 0.763 | 0.884 | 0.439 | 0.790 | -0.916 | -0.933 | 0.719 |
| ESOL | GCN | IntegratedGradients | scaffold | 1 | 200 | 1.142 | 0.915 | 0.713 | 0.887 | 0.516 | 0.785 | -0.934 | -0.864 | 0.719 |
| ESOL | GCN | IntegratedGradients | scaffold | 2 | 200 | 1.034 | 0.848 | 0.765 | 0.889 | 0.355 | 0.725 | -0.458 | -0.235 | 0.718 |
| ESOL | GINE | GNNExplainer | random | 0 | 200 | 0.788 | 0.599 | 0.869 | 0.844 | 0.856 | 0.975 | -1.277 | -2.708 | 0.760 |
| ESOL | GINE | GNNExplainer | random | 1 | 200 | 0.832 | 0.648 | 0.825 | 0.840 | 0.674 | 0.880 | -0.986 | -1.731 | 0.757 |
| ESOL | GINE | GNNExplainer | random | 2 | 200 | 0.879 | 0.639 | 0.833 | 0.862 | 0.373 | 0.640 | -1.316 | -1.758 | 0.757 |
| ESOL | GINE | GNNExplainer | scaffold | 0 | 200 | 0.982 | 0.746 | 0.788 | 0.879 | 0.131 | 0.665 | -0.169 | 0.223 | 0.751 |
| ESOL | GINE | GNNExplainer | scaffold | 1 | 200 | 1.023 | 0.782 | 0.770 | 0.879 | 0.706 | 0.930 | -0.698 | -2.211 | 0.751 |
| ESOL | GINE | GNNExplainer | scaffold | 2 | 200 | 1.010 | 0.775 | 0.775 | 0.878 | 0.554 | 0.855 | -0.691 | -1.119 | 0.751 |
| ESOL | GINE | IntegratedGradients | random | 0 | 200 | 0.788 | 0.599 | 0.869 | 0.868 | 0.904 | 0.970 | -1.668 | -2.456 | 0.740 |
| ESOL | GINE | IntegratedGradients | random | 1 | 200 | 0.832 | 0.648 | 0.825 | 0.858 | 0.714 | 0.880 | -1.213 | -1.644 | 0.746 |
| ESOL | GINE | IntegratedGradients | random | 2 | 200 | 0.879 | 0.639 | 0.833 | 0.870 | 0.432 | 0.640 | -1.490 | -1.686 | 0.739 |
| ESOL | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.982 | 0.746 | 0.788 | 0.896 | 0.284 | 0.675 | -0.294 | 0.210 | 0.730 |
| ESOL | GINE | IntegratedGradients | scaffold | 1 | 200 | 1.023 | 0.782 | 0.770 | 0.900 | 0.801 | 0.940 | -1.207 | -1.735 | 0.729 |
| ESOL | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.958 | 0.700 | 0.798 | 0.895 | 0.142 | 0.645 | -0.448 | 0.110 | 0.730 |
| FreeSolv | GINE | IntegratedGradients | random | 0 | 193 | 1.486 | 1.081 | 0.803 | 0.876 | 0.442 | 0.819 | -0.735 | -1.070 | 0.713 |
| FreeSolv | GINE | IntegratedGradients | random | 1 | 193 | 1.346 | 1.003 | 0.857 | 0.861 | 0.461 | 0.798 | -0.606 | -1.000 | 0.707 |
| FreeSolv | GINE | IntegratedGradients | random | 2 | 193 | 1.618 | 1.112 | 0.830 | 0.857 | 0.276 | 0.699 | -0.715 | -0.788 | 0.717 |
| FreeSolv | GINE | IntegratedGradients | scaffold | 0 | 193 | 1.416 | 1.046 | 0.789 | 0.865 | 0.311 | 0.881 | -0.515 | -0.738 | 0.699 |
| FreeSolv | GINE | IntegratedGradients | scaffold | 1 | 193 | 1.193 | 0.897 | 0.850 | 0.870 | 0.499 | 0.907 | -0.447 | -0.542 | 0.697 |
| FreeSolv | GINE | IntegratedGradients | scaffold | 2 | 193 | 1.398 | 1.053 | 0.795 | 0.860 | 0.453 | 0.907 | -0.874 | -1.434 | 0.705 |
| Lipophilicity | GINE | IntegratedGradients | random | 0 | 200 | 0.737 | 0.571 | 0.617 | 0.787 | 0.470 | 0.680 | 0.535 | 0.521 | 0.778 |
| Lipophilicity | GINE | IntegratedGradients | random | 1 | 200 | 0.798 | 0.604 | 0.527 | 0.781 | 0.652 | 0.830 | 1.052 | 1.365 | 0.780 |
| Lipophilicity | GINE | IntegratedGradients | random | 2 | 200 | 0.783 | 0.597 | 0.563 | 0.790 | 0.546 | 0.700 | -0.636 | -1.248 | 0.781 |
| Lipophilicity | GINE | IntegratedGradients | scaffold | 0 | 200 | 0.915 | 0.696 | 0.429 | 0.808 | 0.485 | 0.620 | 0.450 | 0.703 | 0.780 |
| Lipophilicity | GINE | IntegratedGradients | scaffold | 1 | 200 | 0.920 | 0.707 | 0.424 | 0.852 | 0.396 | 0.605 | 0.239 | 0.391 | 0.778 |
| Lipophilicity | GINE | IntegratedGradients | scaffold | 2 | 200 | 0.924 | 0.713 | 0.419 | 0.818 | 0.600 | 0.910 | 0.839 | 1.956 | 0.779 |

### Metric legend
- **acc/auc**: classification test accuracy / ROC-AUC (AUC is the honest signal on imbalanced sets, where accuracy tracks the majority class). **gt_auroc/gt_auprc**: attribution vs ground-truth motif mask (Tier-1 only; chance AUROC = 0.5; below 0.5 = *anti-aligned* with the motif).
- **rmse/mae/r2**: regression test-set error metrics (original units).
- **motif_top1**: fraction of attribution mass in the single top RDKit motif. **occ_spearman/occ_top1**: occlusion-vs-attribution faithfulness.
- **fid+/fid-**: Fidelity+ (predicted prob/value drop removing salient atoms; higher is better) / Fidelity- (removing non-salient; lower is better). **ece**: test-set expected calibration error (temperature-scaled).
