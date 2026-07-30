# PROGRESS.md — MolSanity rolling progress

_Last run: `full.yaml` @ 20260730_184508._

## Cell tally

- done: **86**  · failed: **0**  · skipped/blocked: **2**

## Cells (dataset × backbone × attributor)

| dataset | backbone | attributor | status | detail |
| --- | --- | --- | --- | --- |
| SynthMotifs | GINE | IntegratedGradients | done | acc=0.95 gt_auroc=0.9011999999999999 n=20 (capped) [cached] |
| SynthMotifs | GINE | IntegratedGradients | done | acc=1.00 gt_auroc=0.998 n=20 (capped) [cached] |
| SynthMotifs | GINE | Saliency | done | acc=0.95 gt_auroc=0.9752000000000001 n=20 (capped) [cached] |
| SynthMotifs | GINE | Saliency | done | acc=1.00 gt_auroc=0.9992000000000001 n=20 (capped) [cached] |
| SynthMotifs | GINE | InputXGradient | done | acc=0.95 gt_auroc=0.9683999999999999 n=20 (capped) [cached] |
| SynthMotifs | GINE | InputXGradient | done | acc=1.00 gt_auroc=0.9916 n=20 (capped) [cached] |
| SynthMotifs | GINE | GuidedBackprop | done | acc=0.95 gt_auroc=0.9279999999999999 n=20 (capped) [cached] |
| SynthMotifs | GINE | GuidedBackprop | done | acc=1.00 gt_auroc=1.0 n=20 (capped) [cached] |
| SynthMotifs | GINE | GNNExplainer | done | acc=0.95 gt_auroc=0.6680000000000001 n=20 (capped) [cached] |
| SynthMotifs | GINE | GNNExplainer | done | acc=1.00 gt_auroc=0.4744 n=20 (capped) [cached] |
| SynthMotifs | GINE | PGExplainer | done | acc=0.95 gt_auroc=0.5648000000000001 n=20 (capped) |
| SynthMotifs | GINE | PGExplainer | done | acc=1.00 gt_auroc=0.49000000000000005 n=20 (capped) |
| SynthMotifs | GCN | IntegratedGradients | done | acc=0.70 gt_auroc=0.9867999999999999 n=20 (capped) [cached] |
| SynthMotifs | GCN | IntegratedGradients | done | acc=0.60 gt_auroc=0.4796 n=20 (capped) [cached] |
| SynthMotifs | GAT | IntegratedGradients | done | acc=0.95 gt_auroc=0.5916 n=20 (capped) [cached] |
| SynthMotifs | GAT | IntegratedGradients | done | acc=1.00 gt_auroc=0.8739999999999999 n=20 (capped) [cached] |
| SynthMotifs | MPNN | IntegratedGradients | done | acc=0.65 gt_auroc=0.7116 n=20 (capped) [cached] |
| SynthMotifs | MPNN | IntegratedGradients | done | acc=1.00 gt_auroc=0.8388 n=20 (capped) [cached] |
| SynthMotifs | AttentiveFP | IntegratedGradients | done | acc=0.85 gt_auroc=0.8856000000000002 n=20 (capped) [cached] |
| SynthMotifs | AttentiveFP | IntegratedGradients | done | acc=1.00 gt_auroc=0.7156 n=20 (capped) [cached] |
| MUTAG | GINE | IntegratedGradients | done | acc=0.75 gt_auroc=0.5365513952278658 n=20 (capped) |
| MUTAG | GINE | IntegratedGradients | done | acc=0.55 gt_auroc=0.047792942351765885 n=20 (capped) |
| MUTAG | GINE | Saliency | done | acc=0.75 gt_auroc=0.009368191721132898 n=20 (capped) |
| MUTAG | GINE | Saliency | done | acc=0.55 gt_auroc=0.020338485044367395 n=20 (capped) |
| MUTAG | GINE | InputXGradient | done | acc=0.75 gt_auroc=0.04896514161220043 n=20 (capped) |
| MUTAG | GINE | InputXGradient | done | acc=0.55 gt_auroc=0.05400090105972458 n=20 (capped) |
| MUTAG | GINE | GuidedBackprop | done | acc=0.75 gt_auroc=0.015677361853832443 n=20 (capped) |
| MUTAG | GINE | GuidedBackprop | done | acc=0.55 gt_auroc=0.2583383977133977 n=20 (capped) |
| MUTAG | GINE | GNNExplainer | done | acc=0.75 gt_auroc=0.6711043422808128 n=20 (capped) |
| MUTAG | GINE | GNNExplainer | done | acc=0.55 gt_auroc=0.4516712739874504 n=20 (capped) |
| MUTAG | GINE | PGExplainer | done | acc=0.75 gt_auroc=0.1084493937435114 n=20 (capped) |
| MUTAG | GINE | PGExplainer | done | acc=0.55 gt_auroc=1.0 n=20 (capped) |
| MUTAG | GCN | IntegratedGradients | done | acc=0.35 gt_auroc=0.9504616298733947 n=20 (capped) |
| MUTAG | GCN | IntegratedGradients | done | acc=0.65 gt_auroc=0.16935581439257907 n=20 (capped) |
| MUTAG | GAT | IntegratedGradients | done | acc=0.75 gt_auroc=0.4199902167549226 n=20 (capped) |
| MUTAG | GAT | IntegratedGradients | done | acc=0.55 gt_auroc=0.7085026642747231 n=20 (capped) |
| MUTAG | MPNN | IntegratedGradients | done | acc=0.75 gt_auroc=0.6722368970898384 n=20 (capped) |
| MUTAG | MPNN | IntegratedGradients | done | acc=0.75 gt_auroc=0.16441819482260658 n=20 (capped) |
| MUTAG | AttentiveFP | IntegratedGradients | done | acc=0.80 gt_auroc=0.032861952861952856 n=20 (capped) |
| MUTAG | AttentiveFP | IntegratedGradients | done | acc=0.60 gt_auroc=0.054620281679105195 n=20 (capped) |
| BBBP | GINE | IntegratedGradients | done | acc=0.95 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | GINE | IntegratedGradients | done | acc=0.82 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | GCN | IntegratedGradients | done | acc=0.98 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | GCN | IntegratedGradients | done | acc=0.79 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | GAT | IntegratedGradients | done | acc=0.98 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | GAT | IntegratedGradients | done | acc=0.78 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | MPNN | IntegratedGradients | done | acc=0.95 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | MPNN | IntegratedGradients | done | acc=0.84 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | AttentiveFP | IntegratedGradients | done | acc=0.95 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | AttentiveFP | IntegratedGradients | done | acc=0.77 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | GINE | GNNExplainer | done | acc=0.95 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | GINE | GNNExplainer | done | acc=0.82 gt_auroc=nan n=100 (capped) [cached] |
| BBBP | GINE | PGExplainer | done | acc=0.95 gt_auroc=nan n=100 (capped) |
| BBBP | GINE | PGExplainer | done | acc=0.82 gt_auroc=nan n=100 (capped) |
| BACE | GINE | IntegratedGradients | done | acc=0.34 gt_auroc=nan n=100 (capped) [cached] |
| BACE | GINE | IntegratedGradients | done | acc=0.73 gt_auroc=nan n=100 (capped) [cached] |
| BACE | GCN | IntegratedGradients | done | acc=0.85 gt_auroc=nan n=100 (capped) [cached] |
| BACE | GCN | IntegratedGradients | done | acc=0.64 gt_auroc=nan n=100 (capped) [cached] |
| ESOL | GINE | IntegratedGradients | done | rmse=0.929 r2=0.778 n=100 (capped) [cached] |
| ESOL | GINE | IntegratedGradients | done | rmse=0.788 r2=0.869 n=100 (capped) [cached] |
| ESOL | GCN | IntegratedGradients | done | rmse=1.017 r2=0.734 n=100 (capped) [cached] |
| ESOL | GCN | IntegratedGradients | done | rmse=0.951 r2=0.809 n=100 (capped) [cached] |
| ESOL | GAT | IntegratedGradients | done | rmse=0.793 r2=0.838 n=100 (capped) [cached] |
| ESOL | GAT | IntegratedGradients | done | rmse=0.730 r2=0.888 n=100 (capped) [cached] |
| ESOL | GINE | GNNExplainer | done | rmse=0.929 r2=0.778 n=100 (capped) [cached] |
| ESOL | GINE | GNNExplainer | done | rmse=0.788 r2=0.869 n=100 (capped) [cached] |
| FreeSolv | GINE | IntegratedGradients | done | rmse=1.304 r2=0.881 n=65 (capped) |
| FreeSolv | GINE | IntegratedGradients | done | rmse=1.486 r2=0.803 n=65 (capped) [cached] |
| Lipophilicity | GINE | IntegratedGradients | done | rmse=0.749 r2=0.614 n=100 (capped) [cached] |
| Lipophilicity | GINE | IntegratedGradients | done | rmse=0.737 r2=0.617 n=100 (capped) [cached] |
| ClinTox | GINE | IntegratedGradients | done | acc=0.80 gt_auroc=nan n=100 (capped) [cached] |
| ClinTox | GINE | IntegratedGradients | done | acc=0.71 gt_auroc=nan n=100 (capped) [cached] |
| ClinTox | GINE | GNNExplainer | done | acc=0.80 gt_auroc=nan n=100 (capped) [cached] |
| ClinTox | GINE | GNNExplainer | done | acc=0.71 gt_auroc=nan n=100 (capped) [cached] |
| SIDER | GINE | IntegratedGradients | done | acc=0.57 gt_auroc=nan n=100 (capped) [cached] |
| SIDER | GINE | IntegratedGradients | done | acc=0.71 gt_auroc=nan n=100 (capped) [cached] |
| SIDER | GCN | IntegratedGradients | done | acc=0.65 gt_auroc=nan n=100 (capped) [cached] |
| SIDER | GCN | IntegratedGradients | done | acc=0.64 gt_auroc=nan n=100 (capped) [cached] |
| Tox21 | GINE | IntegratedGradients | done | acc=0.96 gt_auroc=nan n=100 (capped) [cached] |
| Tox21 | GINE | IntegratedGradients | done | acc=0.97 gt_auroc=nan n=100 (capped) [cached] |
| BA-2Motifs | GINE | IntegratedGradients | done | acc=0.99 gt_auroc=nan n=100 (capped) |
| BA-2Motifs | GINE | IntegratedGradients | done | acc=0.82 gt_auroc=nan n=100 (capped) |
| ShapeGGen | GINE | IntegratedGradients | skipped | ShapeGGen requires GraphXAI which is not installed (No module named 'graphxai'). Skipping and logging per Hard Rule 4. |
| ShapeGGen | GINE | IntegratedGradients | skipped | ShapeGGen requires GraphXAI which is not installed (No module named 'graphxai'). Skipping and logging per Hard Rule 4. |
| DILI | GINE | IntegratedGradients | done | acc=0.69 gt_auroc=nan n=48 (capped) [cached] |
| DILI | GINE | IntegratedGradients | done | acc=0.69 gt_auroc=nan n=48 (capped) [cached] |
| hERG | GINE | IntegratedGradients | done | acc=0.73 gt_auroc=nan n=66 (capped) [cached] |
| hERG | GINE | IntegratedGradients | done | acc=0.80 gt_auroc=nan n=66 (capped) [cached] |

## Blockers

- ShapeGGen__GINE__IntegratedGradients__scaffold: ShapeGGen requires GraphXAI which is not installed (No module named 'graphxai'). Skipping and logging per Hard Rule 4.
- ShapeGGen__GINE__IntegratedGradients__random: ShapeGGen requires GraphXAI which is not installed (No module named 'graphxai'). Skipping and logging per Hard Rule 4.
