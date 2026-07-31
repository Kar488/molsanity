# RESULTS.md — validated numbers only

> Every number here is computed by code in this run and traceable to a
> logged artifact under `artifacts/`. No placeholders. See `LIMITATIONS.md`
> for caveats (notably: MUTAG ground truth is a chemically motivated
> nitro-motif *proxy*, not annotator labels).

## Classification audit matrix (dataset × backbone × attributor)

| dataset | backbone | attributor | split | seed | n_mol | acc | auc | gt_auroc | gt_auprc | motif_top1 | occ_spearman | occ_top1 | fid+ | fid- | sparsity | ece |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BA-2Motifs | GINE | GNNExplainer | random | 0 | 200 | 0.780 | 1.000 | 0.514 | 0.296 | 0.042 | 0.005 | 0.040 | 0.011 | 0.094 | 0.800 | 0.076 |
| BA-2Motifs | GINE | GNNExplainer | random | 1 | 200 | 0.645 | 1.000 | 0.456 | 0.261 | 0.042 | 0.002 | 0.040 | -0.009 | -0.015 | 0.800 | 0.080 |
| BA-2Motifs | GINE | GNNExplainer | random | 2 | 200 | 0.875 | 1.000 | 0.572 | 0.356 | 0.042 | -0.044 | 0.030 | -0.007 | -0.021 | 0.800 | 0.034 |
| BA-2Motifs | GINE | GNNExplainer | scaffold | 0 | 200 | 0.985 | 0.990 | 0.477 | 0.273 | 0.042 | 0.026 | 0.110 | 0.011 | 0.045 | 0.800 | 0.253 |
| BA-2Motifs | GINE | GNNExplainer | scaffold | 1 | 200 | 0.990 | 0.987 | 0.485 | 0.253 | 0.046 | 0.213 | 0.315 | 0.043 | 0.098 | 0.800 | 0.012 |
| BA-2Motifs | GINE | GNNExplainer | scaffold | 2 | 200 | 0.900 | 0.980 | 0.502 | 0.292 | 0.042 | 0.030 | 0.045 | 0.003 | 0.011 | 0.800 | 0.206 |
| BA-2Motifs | GINE | GuidedBackprop | random | 0 | 200 | 0.780 | 1.000 | 0.923 | 0.859 | 0.180 | -0.159 | 0.140 | 0.141 | -0.004 | 0.790 | 0.076 |
| BA-2Motifs | GINE | GuidedBackprop | random | 1 | 200 | 0.645 | 1.000 | 0.963 | 0.943 | 0.180 | -0.263 | 0.000 | -0.012 | -0.001 | 0.781 | 0.080 |
| BA-2Motifs | GINE | GuidedBackprop | random | 2 | 200 | 0.875 | 1.000 | 0.948 | 0.900 | 0.133 | -0.323 | 0.005 | -0.013 | -0.014 | 0.797 | 0.034 |
| BA-2Motifs | GINE | GuidedBackprop | scaffold | 0 | 200 | 0.985 | 0.990 | 0.850 | 0.524 | 0.106 | 0.588 | 0.305 | 0.022 | 0.033 | 0.797 | 0.253 |
| BA-2Motifs | GINE | GuidedBackprop | scaffold | 1 | 200 | 0.990 | 0.987 | 0.934 | 0.745 | 0.115 | 0.758 | 0.635 | 0.070 | 0.072 | 0.800 | 0.012 |
| BA-2Motifs | GINE | GuidedBackprop | scaffold | 2 | 200 | 0.900 | 0.980 | 0.908 | 0.814 | 0.136 | 0.506 | 0.755 | 0.007 | 0.006 | 0.792 | 0.206 |
| BA-2Motifs | GINE | InputXGradient | random | 0 | 200 | 0.780 | 1.000 | 1.000 | 0.998 | 0.213 | -0.148 | 0.135 | 0.111 | 0.020 | 0.800 | 0.076 |
| BA-2Motifs | GINE | InputXGradient | random | 1 | 200 | 0.645 | 1.000 | 0.996 | 0.987 | 0.199 | -0.164 | 0.285 | -0.010 | -0.002 | 0.800 | 0.080 |
| BA-2Motifs | GINE | InputXGradient | random | 2 | 200 | 0.875 | 1.000 | 0.928 | 0.740 | 0.127 | -0.260 | 0.005 | -0.012 | -0.016 | 0.790 | 0.034 |
| BA-2Motifs | GINE | InputXGradient | scaffold | 0 | 200 | 0.985 | 0.990 | 0.895 | 0.661 | 0.105 | 0.916 | 0.745 | 0.025 | 0.030 | 0.799 | 0.253 |
| BA-2Motifs | GINE | InputXGradient | scaffold | 1 | 200 | 0.990 | 0.987 | 0.935 | 0.757 | 0.111 | 0.774 | 0.905 | 0.065 | 0.076 | 0.800 | 0.012 |
| BA-2Motifs | GINE | InputXGradient | scaffold | 2 | 200 | 0.900 | 0.980 | 0.963 | 0.836 | 0.127 | 0.516 | 0.715 | 0.007 | 0.007 | 0.800 | 0.206 |
| BA-2Motifs | GINE | PGExplainer | random | 0 | 200 | 0.780 | 1.000 | 0.377 | 0.306 | 0.438 | -0.053 | 0.000 | 0.014 | 0.113 | 0.731 | 0.076 |
| BA-2Motifs | GINE | PGExplainer | random | 1 | 200 | 0.645 | 1.000 | 0.591 | 0.393 | 0.389 | -0.033 | 0.015 | -0.009 | -0.003 | 0.617 | 0.080 |
| BA-2Motifs | GINE | PGExplainer | random | 2 | 200 | 0.875 | 1.000 | 0.102 | 0.194 | 0.382 | 0.161 | 0.000 | -0.003 | -0.024 | 0.784 | 0.034 |
| BA-2Motifs | GINE | PGExplainer | scaffold | 0 | 200 | 0.985 | 0.990 | 0.838 | 0.759 | 0.497 | 0.355 | 0.010 | 0.020 | 0.035 | 0.759 | 0.253 |
| BA-2Motifs | GINE | PGExplainer | scaffold | 1 | 200 | 0.990 | 0.987 | 0.858 | 0.724 | 0.407 | 0.385 | 0.000 | 0.046 | 0.099 | 0.765 | 0.012 |
| BA-2Motifs | GINE | PGExplainer | scaffold | 2 | 200 | 0.900 | 0.980 | 0.863 | 0.756 | 0.417 | 0.079 | 0.010 | 0.003 | 0.011 | 0.762 | 0.206 |
| BA-2Motifs | GINE | Saliency | random | 0 | 200 | 0.780 | 1.000 | 1.000 | 0.998 | 0.213 | -0.148 | 0.135 | 0.111 | 0.020 | 0.800 | 0.076 |
| BA-2Motifs | GINE | Saliency | random | 1 | 200 | 0.645 | 1.000 | 0.996 | 0.987 | 0.199 | -0.164 | 0.285 | -0.010 | -0.002 | 0.800 | 0.080 |
| BA-2Motifs | GINE | Saliency | random | 2 | 200 | 0.875 | 1.000 | 0.928 | 0.740 | 0.127 | -0.260 | 0.005 | -0.012 | -0.016 | 0.790 | 0.034 |
| BA-2Motifs | GINE | Saliency | scaffold | 0 | 200 | 0.985 | 0.990 | 0.895 | 0.661 | 0.105 | 0.916 | 0.745 | 0.025 | 0.030 | 0.799 | 0.253 |
| BA-2Motifs | GINE | Saliency | scaffold | 1 | 200 | 0.990 | 0.987 | 0.935 | 0.757 | 0.111 | 0.774 | 0.905 | 0.065 | 0.076 | 0.800 | 0.012 |
| BA-2Motifs | GINE | Saliency | scaffold | 2 | 200 | 0.900 | 0.980 | 0.963 | 0.836 | 0.127 | 0.516 | 0.715 | 0.007 | 0.007 | 0.800 | 0.206 |
| BBBP | GINE | GNNExplainer | random | 0 | 200 | 0.745 | 0.886 | — | — | 0.780 | -0.201 | 0.295 | 0.158 | 0.198 | 0.779 | 0.053 |
| BBBP | GINE | GNNExplainer | random | 1 | 200 | 0.760 | 0.899 | — | — | 0.829 | -0.027 | 0.455 | 0.170 | 0.215 | 0.777 | 0.016 |
| BBBP | GINE | GNNExplainer | random | 2 | 200 | 0.685 | 0.891 | — | — | 0.790 | 0.186 | 0.430 | 0.224 | 0.232 | 0.779 | 0.031 |
| BBBP | GINE | GNNExplainer | scaffold | 0 | 200 | 0.915 | 0.932 | — | — | 0.799 | -0.389 | 0.100 | 0.028 | -0.039 | 0.781 | 0.029 |
| BBBP | GINE | GNNExplainer | scaffold | 1 | 200 | 0.720 | 0.918 | — | — | 0.788 | -0.293 | 0.225 | 0.084 | 0.059 | 0.781 | 0.070 |
| BBBP | GINE | GNNExplainer | scaffold | 2 | 200 | 0.840 | 0.941 | — | — | 0.802 | -0.357 | 0.165 | -0.003 | -0.060 | 0.781 | 0.024 |
| BBBP | GINE | PGExplainer | random | 0 | 200 | 0.745 | 0.886 | — | — | 0.886 | -0.155 | 0.250 | 0.091 | 0.200 | 0.770 | 0.053 |
| BBBP | GINE | PGExplainer | random | 1 | 200 | 0.760 | 0.899 | — | — | 0.933 | -0.148 | 0.305 | 0.174 | 0.178 | 0.702 | 0.016 |
| BBBP | GINE | PGExplainer | random | 2 | 200 | 0.685 | 0.891 | — | — | 0.879 | -0.086 | 0.300 | 0.115 | 0.229 | 0.689 | 0.031 |
| BBBP | GINE | PGExplainer | scaffold | 0 | 200 | 0.915 | 0.932 | — | — | 0.937 | -0.480 | 0.095 | -0.009 | -0.034 | 0.775 | 0.029 |
| BBBP | GINE | PGExplainer | scaffold | 1 | 200 | 0.720 | 0.918 | — | — | 0.855 | -0.309 | 0.160 | 0.048 | 0.031 | 0.590 | 0.070 |
| BBBP | GINE | PGExplainer | scaffold | 2 | 200 | 0.840 | 0.941 | — | — | 0.821 | -0.297 | 0.220 | -0.042 | -0.051 | 0.593 | 0.024 |
| ClinTox | GINE | GNNExplainer | random | 0 | 200 | 0.725 | 0.910 | — | — | 0.575 | 0.058 | 0.450 | 0.245 | 0.226 | 0.835 | 0.157 |
| ClinTox | GINE | GNNExplainer | random | 1 | 200 | 0.760 | 0.870 | — | — | 0.250 | 0.803 | 0.440 | 0.207 | 0.145 | 0.930 | 0.063 |
| ClinTox | GINE | GNNExplainer | random | 2 | 200 | 0.705 | 0.861 | — | — | 0.619 | -0.039 | 0.420 | 0.191 | 0.152 | 0.827 | 0.083 |
| ClinTox | GINE | GNNExplainer | scaffold | 0 | 200 | 0.805 | 0.845 | — | — | 0.554 | -0.339 | 0.255 | 0.086 | 0.040 | 0.818 | 0.062 |
| ClinTox | GINE | GNNExplainer | scaffold | 1 | 200 | 0.785 | 0.839 | — | — | 0.655 | -0.432 | 0.225 | 0.047 | 0.038 | 0.790 | 0.096 |
| ClinTox | GINE | GNNExplainer | scaffold | 2 | 200 | 0.660 | 0.873 | — | — | 0.686 | -0.219 | 0.375 | 0.205 | 0.205 | 0.783 | 0.120 |
| MUTAG | GINE | GNNExplainer | random | 0 | 58 | 0.534 | 0.823 | 0.480 | 0.342 | 0.936 | -0.290 | 0.310 | -0.003 | -0.007 | 0.776 | 0.048 |
| MUTAG | GINE | GNNExplainer | random | 1 | 58 | 0.810 | 0.928 | 0.704 | 0.608 | 0.936 | 0.096 | 0.466 | 0.274 | 0.444 | 0.772 | 0.154 |
| MUTAG | GINE | GNNExplainer | random | 2 | 58 | 0.897 | 0.985 | 0.838 | 0.799 | 0.930 | -0.155 | 0.241 | 0.313 | 0.185 | 0.777 | 0.065 |
| MUTAG | GINE | GNNExplainer | scaffold | 0 | 53 | 0.830 | 0.912 | 0.762 | 0.712 | 0.975 | 0.357 | 0.321 | 0.090 | 0.300 | 0.774 | 0.177 |
| MUTAG | GINE | GNNExplainer | scaffold | 1 | 53 | 0.585 | 0.910 | 0.489 | 0.307 | 0.984 | -0.370 | 0.340 | -0.001 | -0.000 | 0.774 | 0.061 |
| MUTAG | GINE | GNNExplainer | scaffold | 2 | 53 | 0.868 | 0.900 | 0.528 | 0.353 | 0.984 | 0.365 | 0.698 | 0.071 | 0.310 | 0.774 | 0.059 |
| MUTAG | GINE | GuidedBackprop | random | 0 | 58 | 0.534 | 0.823 | 0.225 | 0.246 | 0.941 | -0.328 | 0.310 | -0.003 | -0.006 | 0.773 | 0.048 |
| MUTAG | GINE | GuidedBackprop | random | 1 | 58 | 0.810 | 0.928 | 0.030 | 0.175 | 0.962 | 0.018 | 0.448 | 0.454 | 0.444 | 0.769 | 0.154 |
| MUTAG | GINE | GuidedBackprop | random | 2 | 58 | 0.897 | 0.985 | 0.037 | 0.169 | 0.962 | -0.089 | 0.207 | 0.540 | 0.615 | 0.773 | 0.065 |
| MUTAG | GINE | GuidedBackprop | scaffold | 0 | 53 | 0.830 | 0.912 | 0.007 | 0.134 | 0.995 | 0.427 | 0.321 | 0.264 | 0.318 | 0.772 | 0.177 |
| MUTAG | GINE | GuidedBackprop | scaffold | 1 | 53 | 0.585 | 0.910 | 0.014 | 0.135 | 0.994 | -0.289 | 0.340 | 0.000 | -0.001 | 0.772 | 0.061 |
| MUTAG | GINE | GuidedBackprop | scaffold | 2 | 53 | 0.868 | 0.900 | 0.146 | 0.193 | 0.985 | 0.551 | 0.698 | 0.210 | 0.242 | 0.772 | 0.059 |
| MUTAG | GINE | InputXGradient | random | 0 | 58 | 0.534 | 0.823 | 0.066 | 0.181 | 0.987 | -0.346 | 0.310 | -0.004 | -0.006 | 0.770 | 0.048 |
| MUTAG | GINE | InputXGradient | random | 1 | 58 | 0.810 | 0.928 | 0.025 | 0.166 | 0.976 | 0.022 | 0.448 | 0.398 | 0.463 | 0.770 | 0.154 |
| MUTAG | GINE | InputXGradient | random | 2 | 58 | 0.897 | 0.985 | 0.013 | 0.161 | 0.984 | -0.198 | 0.190 | 0.487 | 0.605 | 0.771 | 0.065 |
| MUTAG | GINE | InputXGradient | scaffold | 0 | 53 | 0.830 | 0.912 | 0.032 | 0.138 | 0.999 | 0.395 | 0.321 | 0.262 | 0.322 | 0.772 | 0.177 |
| MUTAG | GINE | InputXGradient | scaffold | 1 | 53 | 0.585 | 0.910 | 0.049 | 0.146 | 0.996 | -0.292 | 0.340 | 0.000 | -0.001 | 0.773 | 0.061 |
| MUTAG | GINE | InputXGradient | scaffold | 2 | 53 | 0.868 | 0.900 | 0.048 | 0.140 | 0.995 | 0.534 | 0.698 | 0.199 | 0.246 | 0.772 | 0.059 |
| MUTAG | GINE | PGExplainer | random | 0 | 58 | 0.534 | 0.823 | 0.996 | 0.993 | 0.953 | -0.281 | 0.310 | -0.001 | -0.006 | 0.765 | 0.048 |
| MUTAG | GINE | PGExplainer | random | 1 | 58 | 0.810 | 0.928 | 0.743 | 0.573 | 0.999 | 0.154 | 0.448 | 0.361 | 0.453 | 0.728 | 0.154 |
| MUTAG | GINE | PGExplainer | random | 2 | 58 | 0.897 | 0.985 | 0.251 | 0.234 | 0.983 | -0.346 | 0.259 | 0.380 | 0.429 | 0.648 | 0.065 |
| MUTAG | GINE | PGExplainer | scaffold | 0 | 53 | 0.830 | 0.912 | 0.039 | 0.191 | 1.000 | 0.196 | 0.226 | 0.141 | 0.377 | 0.764 | 0.177 |
| MUTAG | GINE | PGExplainer | scaffold | 1 | 53 | 0.585 | 0.910 | 0.988 | 0.974 | 0.987 | -0.381 | 0.340 | 0.001 | -0.001 | 0.763 | 0.061 |
| MUTAG | GINE | PGExplainer | scaffold | 2 | 53 | 0.868 | 0.900 | 0.981 | 0.952 | 0.986 | 0.215 | 0.698 | 0.097 | 0.238 | 0.637 | 0.059 |
| MUTAG | GINE | Saliency | random | 0 | 58 | 0.534 | 0.823 | 0.029 | 0.171 | 0.979 | -0.301 | 0.310 | -0.004 | -0.006 | 0.771 | 0.048 |
| MUTAG | GINE | Saliency | random | 1 | 58 | 0.810 | 0.928 | 0.006 | 0.163 | 0.971 | 0.034 | 0.448 | 0.391 | 0.463 | 0.769 | 0.154 |
| MUTAG | GINE | Saliency | random | 2 | 58 | 0.897 | 0.985 | 0.002 | 0.160 | 0.975 | -0.196 | 0.190 | 0.497 | 0.610 | 0.772 | 0.065 |
| MUTAG | GINE | Saliency | scaffold | 0 | 53 | 0.830 | 0.912 | 0.009 | 0.134 | 0.999 | 0.358 | 0.321 | 0.221 | 0.381 | 0.772 | 0.177 |
| MUTAG | GINE | Saliency | scaffold | 1 | 53 | 0.585 | 0.910 | 0.101 | 0.158 | 0.990 | -0.290 | 0.340 | 0.000 | -0.001 | 0.774 | 0.061 |
| MUTAG | GINE | Saliency | scaffold | 2 | 53 | 0.868 | 0.900 | 0.014 | 0.134 | 0.996 | 0.531 | 0.698 | 0.198 | 0.248 | 0.772 | 0.059 |
| MolMotif | GINE | GNNExplainer | random | 0 | 200 | 0.975 | 0.999 | 0.679 | 0.464 | 0.823 | -0.187 | 0.200 | 0.184 | 0.222 | 0.779 | 0.020 |
| MolMotif | GINE | GNNExplainer | random | 1 | 200 | 0.810 | 1.000 | 0.606 | 0.386 | 0.821 | 0.104 | 0.435 | 0.371 | 0.282 | 0.779 | 0.106 |
| MolMotif | GINE | GNNExplainer | random | 2 | 200 | 1.000 | 1.000 | 0.630 | 0.442 | 0.836 | 0.031 | 0.380 | -0.020 | 0.387 | 0.778 | 0.003 |
| MolMotif | GINE | GNNExplainer | scaffold | 0 | 200 | 0.985 | 1.000 | 0.587 | 0.402 | 0.817 | 0.023 | 0.500 | 0.297 | 0.413 | 0.780 | 0.012 |
| MolMotif | GINE | GNNExplainer | scaffold | 1 | 200 | 0.985 | 1.000 | 0.585 | 0.398 | 0.814 | -0.012 | 0.485 | 0.305 | 0.437 | 0.780 | 0.010 |
| MolMotif | GINE | GNNExplainer | scaffold | 2 | 200 | 0.910 | 1.000 | 0.604 | 0.409 | 0.814 | -0.054 | 0.220 | -0.014 | 0.265 | 0.780 | 0.018 |
| MolMotif | GINE | GuidedBackprop | random | 0 | 200 | 0.975 | 0.999 | 0.981 | 0.956 | 0.854 | -0.202 | 0.270 | 0.170 | 0.132 | 0.771 | 0.020 |
| MolMotif | GINE | GuidedBackprop | random | 1 | 200 | 0.810 | 1.000 | 0.935 | 0.835 | 0.826 | 0.007 | 0.405 | 0.116 | 0.429 | 0.772 | 0.106 |
| MolMotif | GINE | GuidedBackprop | random | 2 | 200 | 1.000 | 1.000 | 0.998 | 0.993 | 0.823 | -0.145 | 0.345 | 0.330 | 0.318 | 0.770 | 0.003 |
| MolMotif | GINE | GuidedBackprop | scaffold | 0 | 200 | 0.985 | 1.000 | 0.994 | 0.980 | 0.844 | -0.025 | 0.465 | 0.321 | 0.410 | 0.773 | 0.012 |
| MolMotif | GINE | GuidedBackprop | scaffold | 1 | 200 | 0.985 | 1.000 | 0.995 | 0.979 | 0.821 | -0.078 | 0.450 | 0.251 | 0.433 | 0.772 | 0.010 |
| MolMotif | GINE | GuidedBackprop | scaffold | 2 | 200 | 0.910 | 1.000 | 0.882 | 0.849 | 0.814 | -0.269 | 0.235 | 0.214 | 0.191 | 0.774 | 0.018 |
| MolMotif | GINE | InputXGradient | random | 0 | 200 | 0.975 | 0.999 | 0.986 | 0.971 | 0.822 | -0.285 | 0.245 | 0.040 | 0.164 | 0.772 | 0.020 |
| MolMotif | GINE | InputXGradient | random | 1 | 200 | 0.810 | 1.000 | 1.000 | 0.998 | 0.773 | -0.138 | 0.315 | 0.087 | 0.414 | 0.772 | 0.106 |
| MolMotif | GINE | InputXGradient | random | 2 | 200 | 1.000 | 1.000 | 0.999 | 0.997 | 0.810 | -0.112 | 0.445 | 0.312 | 0.322 | 0.768 | 0.003 |
| MolMotif | GINE | InputXGradient | scaffold | 0 | 200 | 0.985 | 1.000 | 0.999 | 0.998 | 0.830 | -0.045 | 0.460 | 0.246 | 0.415 | 0.774 | 0.012 |
| MolMotif | GINE | InputXGradient | scaffold | 1 | 200 | 0.985 | 1.000 | 0.996 | 0.985 | 0.849 | -0.097 | 0.450 | 0.258 | 0.436 | 0.774 | 0.010 |
| MolMotif | GINE | InputXGradient | scaffold | 2 | 200 | 0.910 | 1.000 | 0.999 | 0.995 | 0.758 | -0.257 | 0.190 | 0.205 | 0.170 | 0.774 | 0.018 |
| MolMotif | GINE | PGExplainer | random | 0 | 200 | 0.975 | 0.999 | 0.649 | 0.443 | 0.709 | -0.079 | 0.245 | 0.164 | 0.097 | 0.410 | 0.020 |
| MolMotif | GINE | PGExplainer | random | 1 | 200 | 0.810 | 1.000 | 0.273 | 0.218 | 0.909 | -0.216 | 0.250 | 0.090 | 0.428 | 0.768 | 0.106 |
| MolMotif | GINE | PGExplainer | random | 2 | 200 | 1.000 | 1.000 | 0.584 | 0.344 | 0.897 | 0.001 | 0.310 | 0.143 | 0.381 | 0.702 | 0.003 |
| MolMotif | GINE | PGExplainer | scaffold | 0 | 200 | 0.985 | 1.000 | 0.716 | 0.560 | 0.448 | -0.715 | 0.040 | -0.027 | 0.445 | 0.551 | 0.012 |
| MolMotif | GINE | PGExplainer | scaffold | 1 | 200 | 0.985 | 1.000 | 0.499 | 0.219 | 0.053 | -0.025 | 0.090 | 0.042 | 0.404 | 0.945 | 0.010 |
| MolMotif | GINE | PGExplainer | scaffold | 2 | 200 | 0.910 | 1.000 | 0.240 | 0.199 | 0.911 | -0.031 | 0.180 | 0.125 | 0.237 | 0.774 | 0.018 |
| MolMotif | GINE | Saliency | random | 0 | 200 | 0.975 | 0.999 | 0.990 | 0.981 | 0.826 | -0.254 | 0.260 | 0.065 | 0.167 | 0.771 | 0.020 |
| MolMotif | GINE | Saliency | random | 1 | 200 | 0.810 | 1.000 | 0.999 | 0.996 | 0.772 | -0.121 | 0.305 | 0.099 | 0.415 | 0.772 | 0.106 |
| MolMotif | GINE | Saliency | random | 2 | 200 | 1.000 | 1.000 | 0.994 | 0.985 | 0.802 | -0.117 | 0.425 | 0.318 | 0.317 | 0.772 | 0.003 |
| MolMotif | GINE | Saliency | scaffold | 0 | 200 | 0.985 | 1.000 | 0.999 | 0.996 | 0.822 | -0.065 | 0.455 | 0.242 | 0.415 | 0.775 | 0.012 |
| MolMotif | GINE | Saliency | scaffold | 1 | 200 | 0.985 | 1.000 | 0.995 | 0.983 | 0.841 | -0.084 | 0.465 | 0.254 | 0.439 | 0.774 | 0.010 |
| MolMotif | GINE | Saliency | scaffold | 2 | 200 | 0.910 | 1.000 | 0.998 | 0.994 | 0.751 | -0.270 | 0.185 | 0.220 | 0.179 | 0.775 | 0.018 |
| SynthMotifs | GINE | GNNExplainer | random | 0 | 200 | 0.985 | 1.000 | 0.557 | 0.302 | 0.037 | 0.088 | 0.055 | 0.211 | 0.221 | 0.800 | 0.000 |
| SynthMotifs | GINE | GNNExplainer | random | 1 | 200 | 0.985 | 1.000 | 0.623 | 0.380 | 0.046 | 0.109 | 0.070 | 0.291 | 0.286 | 0.800 | 0.009 |
| SynthMotifs | GINE | GNNExplainer | random | 2 | 200 | 0.945 | 1.000 | 0.689 | 0.470 | 0.048 | 0.191 | 0.075 | 0.213 | 0.250 | 0.800 | 0.020 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 0 | 200 | 0.900 | 1.000 | 0.668 | 0.345 | 0.053 | 0.018 | 0.065 | 0.185 | 0.207 | 0.800 | 0.029 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 1 | 200 | 1.000 | 1.000 | 0.538 | 0.268 | 0.040 | 0.034 | 0.020 | 0.255 | 0.358 | 0.800 | 0.003 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 2 | 200 | 0.915 | 1.000 | 0.796 | 0.491 | 0.051 | 0.217 | 0.090 | 0.336 | 0.321 | 0.800 | 0.030 |
| SynthMotifs | GINE | GuidedBackprop | random | 0 | 200 | 0.985 | 1.000 | 0.999 | 0.996 | 0.178 | 0.645 | 0.465 | 0.235 | 0.081 | 0.800 | 0.000 |
| SynthMotifs | GINE | GuidedBackprop | random | 1 | 200 | 0.985 | 1.000 | 0.989 | 0.969 | 0.157 | 0.662 | 0.280 | 0.321 | 0.043 | 0.799 | 0.009 |
| SynthMotifs | GINE | GuidedBackprop | random | 2 | 200 | 0.945 | 1.000 | 0.996 | 0.983 | 0.164 | 0.614 | 0.360 | 0.261 | 0.059 | 0.800 | 0.020 |
| SynthMotifs | GINE | GuidedBackprop | scaffold | 0 | 200 | 0.900 | 1.000 | 0.913 | 0.719 | 0.113 | 0.266 | 0.455 | 0.206 | 0.103 | 0.795 | 0.029 |
| SynthMotifs | GINE | GuidedBackprop | scaffold | 1 | 200 | 1.000 | 1.000 | 0.999 | 0.995 | 0.161 | 0.778 | 0.155 | 0.349 | 0.107 | 0.800 | 0.003 |
| SynthMotifs | GINE | GuidedBackprop | scaffold | 2 | 200 | 0.915 | 1.000 | 0.982 | 0.952 | 0.143 | 0.628 | 0.655 | 0.345 | 0.033 | 0.800 | 0.030 |
| SynthMotifs | GINE | InputXGradient | random | 0 | 200 | 0.985 | 1.000 | 0.987 | 0.956 | 0.194 | 0.488 | 0.200 | 0.244 | 0.109 | 0.798 | 0.000 |
| SynthMotifs | GINE | InputXGradient | random | 1 | 200 | 0.985 | 1.000 | 0.963 | 0.872 | 0.229 | 0.439 | 0.170 | 0.314 | 0.092 | 0.793 | 0.009 |
| SynthMotifs | GINE | InputXGradient | random | 2 | 200 | 0.945 | 1.000 | 0.959 | 0.870 | 0.238 | 0.499 | 0.150 | 0.261 | 0.132 | 0.795 | 0.020 |
| SynthMotifs | GINE | InputXGradient | scaffold | 0 | 200 | 0.900 | 1.000 | 0.951 | 0.826 | 0.183 | 0.247 | 0.120 | 0.228 | 0.113 | 0.796 | 0.029 |
| SynthMotifs | GINE | InputXGradient | scaffold | 1 | 200 | 1.000 | 1.000 | 0.977 | 0.921 | 0.199 | 0.624 | 0.125 | 0.352 | 0.142 | 0.798 | 0.003 |
| SynthMotifs | GINE | InputXGradient | scaffold | 2 | 200 | 0.915 | 1.000 | 0.982 | 0.926 | 0.180 | 0.456 | 0.110 | 0.338 | 0.122 | 0.797 | 0.030 |
| SynthMotifs | GINE | PGExplainer | random | 0 | 200 | 0.985 | 1.000 | 0.460 | 0.192 | 0.303 | -0.078 | 0.015 | 0.138 | 0.114 | 0.434 | 0.000 |
| SynthMotifs | GINE | PGExplainer | random | 1 | 200 | 0.985 | 1.000 | 0.471 | 0.261 | 0.379 | -0.025 | 0.000 | 0.125 | 0.302 | 0.784 | 0.009 |
| SynthMotifs | GINE | PGExplainer | random | 2 | 200 | 0.945 | 1.000 | 0.314 | 0.174 | 0.385 | -0.149 | 0.000 | 0.010 | 0.262 | 0.785 | 0.020 |
| SynthMotifs | GINE | PGExplainer | scaffold | 0 | 200 | 0.900 | 1.000 | 0.536 | 0.277 | 0.364 | 0.090 | 0.025 | 0.154 | 0.213 | 0.612 | 0.029 |
| SynthMotifs | GINE | PGExplainer | scaffold | 1 | 200 | 1.000 | 1.000 | 0.308 | 0.167 | 0.377 | -0.203 | 0.000 | 0.032 | 0.324 | 0.731 | 0.003 |
| SynthMotifs | GINE | PGExplainer | scaffold | 2 | 200 | 0.915 | 1.000 | 0.323 | 0.167 | 0.377 | -0.158 | 0.000 | 0.058 | 0.280 | 0.656 | 0.030 |
| SynthMotifs | GINE | Saliency | random | 0 | 200 | 0.985 | 1.000 | 0.993 | 0.976 | 0.172 | 0.493 | 0.305 | 0.248 | 0.095 | 0.798 | 0.000 |
| SynthMotifs | GINE | Saliency | random | 1 | 200 | 0.985 | 1.000 | 0.983 | 0.934 | 0.197 | 0.461 | 0.150 | 0.311 | 0.080 | 0.797 | 0.009 |
| SynthMotifs | GINE | Saliency | random | 2 | 200 | 0.945 | 1.000 | 0.960 | 0.870 | 0.176 | 0.514 | 0.140 | 0.262 | 0.141 | 0.796 | 0.020 |
| SynthMotifs | GINE | Saliency | scaffold | 0 | 200 | 0.900 | 1.000 | 0.965 | 0.873 | 0.131 | 0.237 | 0.095 | 0.216 | 0.114 | 0.794 | 0.029 |
| SynthMotifs | GINE | Saliency | scaffold | 1 | 200 | 1.000 | 1.000 | 0.983 | 0.950 | 0.172 | 0.606 | 0.095 | 0.344 | 0.148 | 0.796 | 0.003 |
| SynthMotifs | GINE | Saliency | scaffold | 2 | 200 | 0.915 | 1.000 | 0.983 | 0.927 | 0.150 | 0.432 | 0.110 | 0.332 | 0.099 | 0.794 | 0.030 |

## Regression audit matrix

| dataset | backbone | attributor | split | seed | n_mol | rmse | mae | r2 | motif_top1 | occ_spearman | occ_top1 | fid+ | fid- | sparsity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ESOL | GINE | GNNExplainer | random | 0 | 200 | 0.788 | 0.599 | 0.869 | 0.844 | 0.862 | 0.985 | -1.279 | -2.712 | 0.760 |
| ESOL | GINE | GNNExplainer | random | 1 | 200 | 0.832 | 0.648 | 0.825 | 0.840 | 0.685 | 0.880 | -0.998 | -1.732 | 0.757 |
| ESOL | GINE | GNNExplainer | random | 2 | 200 | 0.879 | 0.639 | 0.833 | 0.862 | 0.374 | 0.645 | -1.310 | -1.756 | 0.757 |
| ESOL | GINE | GNNExplainer | scaffold | 0 | 200 | 0.929 | 0.724 | 0.778 | 0.823 | 0.782 | 0.925 | -0.972 | -2.258 | 0.758 |
| ESOL | GINE | GNNExplainer | scaffold | 1 | 200 | 0.928 | 0.693 | 0.812 | 0.822 | 0.718 | 0.885 | -0.964 | -2.129 | 0.758 |
| ESOL | GINE | GNNExplainer | scaffold | 2 | 200 | 0.886 | 0.650 | 0.829 | 0.824 | 0.554 | 0.750 | -1.064 | -1.405 | 0.758 |

### Metric legend
- **acc/auc**: classification test accuracy / ROC-AUC (AUC is the honest signal on imbalanced sets, where accuracy tracks the majority class). **gt_auroc/gt_auprc**: attribution vs ground-truth motif mask (Tier-1 only; chance AUROC = 0.5; below 0.5 = *anti-aligned* with the motif).
- **rmse/mae/r2**: regression test-set error metrics (original units).
- **motif_top1**: fraction of attribution mass in the single top RDKit motif. **occ_spearman/occ_top1**: occlusion-vs-attribution faithfulness.
- **fid+/fid-**: Fidelity+ (predicted prob/value drop removing salient atoms; higher is better) / Fidelity- (removing non-salient; lower is better). **ece**: test-set expected calibration error (temperature-scaled).
