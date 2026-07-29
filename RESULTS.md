# RESULTS.md — validated numbers only

> Every number here is computed by code in this run and traceable to a
> logged artifact under `artifacts/`. No placeholders. See `LIMITATIONS.md`
> for caveats (notably: MUTAG ground truth is a chemically motivated
> nitro-motif *proxy*, not annotator labels).

## Classification audit matrix (dataset × backbone × attributor)

| dataset | backbone | attributor | split | n_mol | acc | auc | gt_auroc | gt_auprc | motif_top1 | occ_spearman | occ_top1 | fid+ | fid- | sparsity | ece |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BACE | GCN | IntegratedGradients | scaffold | 30 | 0.133 | 0.224 | — | — | 0.776 | 0.766 | 0.900 | 0.597 | 0.597 | 0.785 | 0.398 |
| BACE | GINE | GNNExplainer | scaffold | 30 | 0.433 | 0.434 | — | — | 0.835 | -0.128 | 0.167 | 0.064 | 0.214 | 0.786 | 0.189 |
| BACE | GINE | InputXGradient | scaffold | 30 | 0.433 | 0.434 | — | — | 0.841 | -0.159 | 0.167 | 0.079 | 0.171 | 0.783 | 0.189 |
| BACE | GINE | IntegratedGradients | scaffold | 30 | 0.433 | 0.434 | — | — | 0.884 | -0.252 | 0.167 | 0.074 | 0.202 | 0.780 | 0.189 |
| BACE | GINE | Saliency | scaffold | 30 | 0.433 | 0.434 | — | — | 0.873 | -0.174 | 0.167 | 0.097 | 0.173 | 0.785 | 0.189 |
| BBBP | GAT | IntegratedGradients | scaffold | 30 | 0.967 | 0.888 | — | — | 0.810 | -0.808 | 0.000 | -0.069 | -0.069 | 0.778 | 0.024 |
| BBBP | GCN | IntegratedGradients | scaffold | 30 | 0.833 | 0.888 | — | — | 0.781 | -0.316 | 0.233 | 0.005 | -0.096 | 0.773 | 0.016 |
| BBBP | GINE | GNNExplainer | scaffold | 30 | 0.967 | 0.805 | — | — | 0.823 | -0.367 | 0.067 | 0.021 | -0.077 | 0.778 | 0.059 |
| BBBP | GINE | GuidedBackprop | scaffold | 30 | 0.967 | 0.805 | — | — | 0.876 | -0.530 | 0.000 | -0.016 | -0.037 | 0.775 | 0.059 |
| BBBP | GINE | InputXGradient | scaffold | 30 | 0.967 | 0.805 | — | — | 0.839 | -0.620 | 0.000 | -0.016 | -0.047 | 0.769 | 0.059 |
| BBBP | GINE | IntegratedGradients | scaffold | 30 | 0.967 | 0.805 | — | — | 0.773 | -0.430 | 0.000 | 0.006 | -0.054 | 0.775 | 0.059 |
| BBBP | GINE | PGExplainer | scaffold | 30 | 0.967 | 0.805 | — | — | 0.422 | -0.185 | 0.367 | -0.055 | -0.059 | 0.635 | 0.059 |
| BBBP | GINE | Saliency | scaffold | 30 | 0.967 | 0.805 | — | — | 0.826 | -0.627 | 0.000 | -0.029 | -0.033 | 0.773 | 0.059 |
| ClinTox | GINE | GNNExplainer | scaffold | 30 | 0.567 | 0.820 | — | — | 0.483 | 0.927 | 0.700 | 0.375 | 0.356 | 0.848 | 0.207 |
| ClinTox | GINE | InputXGradient | scaffold | 30 | 0.567 | 0.820 | — | — | 0.793 | 0.139 | 0.567 | 0.356 | 0.356 | 0.749 | 0.207 |
| ClinTox | GINE | IntegratedGradients | scaffold | 30 | 0.567 | 0.820 | — | — | 0.724 | 0.085 | 0.633 | 0.356 | 0.356 | 0.755 | 0.207 |
| ClinTox | GINE | Saliency | scaffold | 30 | 0.567 | 0.820 | — | — | 0.790 | 0.145 | 0.567 | 0.356 | 0.356 | 0.749 | 0.207 |
| DILI | GINE | GNNExplainer | scaffold | 30 | 0.800 | 0.824 | — | — | 0.826 | -0.044 | 0.433 | 0.080 | 0.154 | 0.782 | 0.141 |
| DILI | GINE | InputXGradient | scaffold | 30 | 0.800 | 0.824 | — | — | 0.858 | -0.126 | 0.433 | 0.075 | 0.122 | 0.780 | 0.141 |
| DILI | GINE | IntegratedGradients | scaffold | 30 | 0.800 | 0.824 | — | — | 0.847 | -0.101 | 0.433 | 0.073 | 0.128 | 0.781 | 0.141 |
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
| SIDER | GCN | IntegratedGradients | scaffold | 30 | 0.500 | 0.668 | — | — | 0.843 | -0.512 | 0.333 | 0.014 | -0.059 | 0.716 | 0.073 |
| SIDER | GINE | GNNExplainer | scaffold | 30 | 0.633 | 0.661 | — | — | 0.816 | 0.490 | 0.833 | 0.038 | 0.196 | 0.732 | 0.110 |
| SIDER | GINE | InputXGradient | scaffold | 30 | 0.633 | 0.661 | — | — | 0.878 | 0.576 | 0.867 | 0.088 | 0.196 | 0.716 | 0.110 |
| SIDER | GINE | IntegratedGradients | scaffold | 30 | 0.633 | 0.661 | — | — | 0.836 | 0.493 | 0.800 | 0.068 | 0.196 | 0.715 | 0.110 |
| SIDER | GINE | Saliency | scaffold | 30 | 0.633 | 0.661 | — | — | 0.887 | 0.571 | 0.867 | 0.093 | 0.201 | 0.720 | 0.110 |
| SynthMotifs | AttentiveFP | IntegratedGradients | scaffold | 20 | 0.600 | 0.510 | 0.821 | 0.453 | 0.141 | 0.643 | 0.300 | 0.014 | 0.072 | 0.793 | 0.091 |
| SynthMotifs | GAT | IntegratedGradients | scaffold | 20 | 0.900 | 0.990 | 0.718 | 0.549 | 0.177 | 0.527 | 0.500 | 0.102 | 0.047 | 0.790 | 0.241 |
| SynthMotifs | GCN | IntegratedGradients | scaffold | 20 | 0.900 | 1.000 | 0.920 | 0.687 | 0.168 | 0.096 | 0.300 | 0.055 | 0.040 | 0.793 | 0.271 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 20 | 1.000 | 1.000 | 0.498 | 0.246 | 0.043 | -0.017 | 0.050 | 0.101 | 0.099 | 0.800 | 0.000 |
| SynthMotifs | GINE | GuidedBackprop | scaffold | 20 | 1.000 | 1.000 | 0.966 | 0.845 | 0.152 | 0.059 | 0.050 | 0.118 | 0.086 | 0.797 | 0.000 |
| SynthMotifs | GINE | InputXGradient | scaffold | 20 | 1.000 | 1.000 | 0.964 | 0.866 | 0.220 | 0.014 | 0.100 | 0.114 | 0.102 | 0.795 | 0.000 |
| SynthMotifs | GINE | IntegratedGradients | random | 20 | 1.000 | 1.000 | 0.590 | 0.489 | 0.194 | -0.026 | 0.050 | 0.102 | 0.211 | 0.785 | 0.001 |
| SynthMotifs | GINE | IntegratedGradients | scaffold | 20 | 1.000 | 1.000 | 0.742 | 0.633 | 0.225 | 0.073 | 0.050 | 0.109 | 0.100 | 0.792 | 0.000 |
| SynthMotifs | GINE | PGExplainer | scaffold | 20 | 1.000 | 1.000 | 0.360 | 0.220 | 0.393 | 0.106 | 0.000 | 0.064 | 0.126 | 0.787 | 0.000 |
| SynthMotifs | GINE | Saliency | scaffold | 20 | 1.000 | 1.000 | 0.983 | 0.935 | 0.199 | 0.022 | 0.050 | 0.123 | 0.074 | 0.778 | 0.000 |
| SynthMotifs | MPNN | IntegratedGradients | scaffold | 20 | 0.850 | 0.910 | 0.807 | 0.400 | 0.224 | -0.104 | 0.300 | 0.041 | 0.030 | 0.798 | 0.267 |
| hERG | GCN | IntegratedGradients | scaffold | 30 | 0.900 | 0.802 | — | — | 0.665 | 0.711 | 0.867 | 0.589 | 0.590 | 0.776 | 0.098 |
| hERG | GINE | GNNExplainer | scaffold | 30 | 0.733 | 0.784 | — | — | 0.725 | 0.066 | 0.633 | 0.094 | 0.408 | 0.786 | 0.070 |
| hERG | GINE | InputXGradient | scaffold | 30 | 0.733 | 0.784 | — | — | 0.633 | 0.342 | 0.600 | 0.410 | 0.408 | 0.779 | 0.070 |
| hERG | GINE | IntegratedGradients | scaffold | 30 | 0.733 | 0.784 | — | — | 0.673 | 0.431 | 0.700 | 0.411 | 0.408 | 0.784 | 0.070 |
| hERG | GINE | Saliency | scaffold | 30 | 0.733 | 0.784 | — | — | 0.626 | 0.343 | 0.533 | 0.409 | 0.408 | 0.784 | 0.070 |

## Regression audit matrix

| dataset | backbone | attributor | split | n_mol | rmse | mae | r2 | motif_top1 | occ_spearman | occ_top1 | fid+ | fid- | sparsity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ESOL | GAT | IntegratedGradients | scaffold | 20 | 1.092 | 0.880 | 0.694 | 0.799 | -0.481 | 0.150 | -0.115 | -0.995 | 0.730 |
| ESOL | GCN | IntegratedGradients | scaffold | 20 | 1.142 | 0.868 | 0.665 | 0.821 | -0.820 | 0.100 | -1.321 | -1.996 | 0.720 |
| ESOL | GINE | GNNExplainer | scaffold | 20 | 1.132 | 0.918 | 0.671 | 0.828 | -0.770 | 0.100 | -0.798 | -1.288 | 0.772 |
| ESOL | GINE | IntegratedGradients | scaffold | 20 | 1.132 | 0.918 | 0.671 | 0.834 | -0.798 | 0.100 | -1.044 | -1.235 | 0.731 |
| FreeSolv | GINE | IntegratedGradients | scaffold | 20 | 2.347 | 1.733 | 0.614 | 0.782 | -0.582 | 0.400 | -0.543 | -0.922 | 0.738 |
| Lipophilicity | GINE | IntegratedGradients | scaffold | 20 | 0.932 | 0.740 | 0.402 | 0.758 | -0.149 | 0.000 | -0.203 | -0.524 | 0.785 |

### Metric legend
- **acc/auc**: classification test accuracy / ROC-AUC (AUC is the honest signal on imbalanced sets, where accuracy tracks the majority class). **gt_auroc/gt_auprc**: attribution vs ground-truth motif mask (Tier-1 only; chance AUROC = 0.5; below 0.5 = *anti-aligned* with the motif).
- **rmse/mae/r2**: regression test-set error metrics (original units).
- **motif_top1**: fraction of attribution mass in the single top RDKit motif. **occ_spearman/occ_top1**: occlusion-vs-attribution faithfulness.
- **fid+/fid-**: Fidelity+ (predicted prob/value drop removing salient atoms; higher is better) / Fidelity- (removing non-salient; lower is better). **ece**: test-set expected calibration error (temperature-scaled).
