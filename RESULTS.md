# RESULTS.md — validated numbers only

> Every number here is computed by code in this run and traceable to a
> logged artifact under `artifacts/`. No placeholders. See `LIMITATIONS.md`
> for caveats (notably: MUTAG ground truth is a chemically motivated
> nitro-motif *proxy*, not annotator labels).

## Classification audit matrix (dataset × backbone × attributor)

| dataset | backbone | attributor | split | n_mol | acc | gt_auroc | gt_auprc | motif_top1 | occ_spearman | occ_top1 | fid+ | fid- | sparsity | ece |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BBBP | GINE | IntegratedGradients | scaffold | 20 | 1.000 | — | — | 0.862 | -0.613 | 0.000 | -0.095 | -0.175 | 0.773 | 0.015 |
| MUTAG | AttentiveFP | IntegratedGradients | scaffold | 20 | 0.650 | 0.132 | 0.150 | 0.993 | -0.880 | 0.000 | 0.002 | 0.012 | 0.771 | 0.235 |
| MUTAG | GAT | IntegratedGradients | scaffold | 20 | 0.750 | 0.130 | 0.151 | 0.992 | 0.268 | 0.600 | 0.189 | 0.247 | 0.771 | 0.155 |
| MUTAG | GCN | IntegratedGradients | scaffold | 20 | 0.750 | 0.203 | 0.222 | 0.989 | 0.175 | 0.600 | 0.123 | 0.228 | 0.767 | 0.138 |
| MUTAG | GINE | GNNExplainer | scaffold | 20 | 0.800 | 0.491 | 0.347 | 0.987 | 0.279 | 0.350 | 0.113 | 0.278 | 0.771 | 0.117 |
| MUTAG | GINE | InputXGradient | scaffold | 20 | 0.800 | 0.042 | 0.134 | 0.998 | 0.398 | 0.350 | 0.251 | 0.225 | 0.771 | 0.117 |
| MUTAG | GINE | IntegratedGradients | scaffold | 20 | 0.800 | 0.540 | 0.405 | 0.979 | 0.414 | 0.350 | 0.252 | 0.245 | 0.771 | 0.117 |
| MUTAG | GINE | Saliency | scaffold | 20 | 0.800 | 0.026 | 0.131 | 0.997 | 0.376 | 0.350 | 0.267 | 0.230 | 0.771 | 0.117 |
| MUTAG | MPNN | IntegratedGradients | scaffold | 20 | 0.750 | 0.356 | 0.274 | 0.985 | 0.191 | 0.600 | 0.263 | 0.312 | 0.768 | 0.129 |
| SynthMotifs | GINE | GNNExplainer | scaffold | 20 | 1.000 | 0.498 | 0.246 | 0.043 | -0.017 | 0.050 | 0.101 | 0.099 | 0.800 | 0.000 |
| SynthMotifs | GINE | InputXGradient | scaffold | 20 | 1.000 | 0.964 | 0.866 | 0.220 | 0.014 | 0.100 | 0.114 | 0.102 | 0.795 | 0.000 |
| SynthMotifs | GINE | IntegratedGradients | scaffold | 20 | 1.000 | 0.742 | 0.633 | 0.225 | 0.073 | 0.050 | 0.109 | 0.100 | 0.792 | 0.000 |
| SynthMotifs | GINE | Saliency | scaffold | 20 | 1.000 | 0.983 | 0.935 | 0.199 | 0.022 | 0.050 | 0.123 | 0.074 | 0.778 | 0.000 |

## Regression audit matrix

| dataset | backbone | attributor | split | n_mol | rmse | mae | r2 | motif_top1 | occ_spearman | occ_top1 | fid+ | fid- | sparsity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ESOL | GINE | GNNExplainer | scaffold | 20 | 1.132 | 0.918 | 0.671 | 0.828 | -0.770 | 0.100 | -0.798 | -1.288 | 0.772 |
| ESOL | GINE | IntegratedGradients | scaffold | 20 | 1.132 | 0.918 | 0.671 | 0.834 | -0.798 | 0.100 | -1.044 | -1.235 | 0.731 |
| FreeSolv | GINE | IntegratedGradients | scaffold | 20 | 2.347 | 1.733 | 0.614 | 0.782 | -0.582 | 0.400 | -0.543 | -0.922 | 0.738 |

### Metric legend
- **acc/gt_auroc/gt_auprc**: classification accuracy; attribution vs ground-truth motif mask (Tier-1 only; chance AUROC = 0.5). Below 0.5 = *anti-aligned* with the known motif.
- **rmse/mae/r2**: regression test-set error metrics (original units).
- **motif_top1**: fraction of attribution mass in the single top RDKit motif. **occ_spearman/occ_top1**: occlusion-vs-attribution faithfulness.
- **fid+/fid-**: Fidelity+ (predicted prob/value drop removing salient atoms; higher is better) / Fidelity- (removing non-salient; lower is better). **ece**: test-set expected calibration error (temperature-scaled).
