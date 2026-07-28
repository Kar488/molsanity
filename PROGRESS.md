# PROGRESS.md — MolSanity rolling progress

_Last run: `matrix.yaml` @ 20260728_213006._

## Cell tally

- done: **16**  · failed: **0**  · skipped/blocked: **0**

## Cells (dataset × backbone × attributor)

| dataset | backbone | attributor | status | detail |
| --- | --- | --- | --- | --- |
| SynthMotifs | GINE | IntegratedGradients | done | acc=1.00 gt_auroc=0.742 n=20 (capped) [cached] |
| SynthMotifs | GINE | Saliency | done | acc=1.00 gt_auroc=0.9828000000000001 n=20 (capped) [cached] |
| SynthMotifs | GINE | InputXGradient | done | acc=1.00 gt_auroc=0.9644 n=20 (capped) |
| SynthMotifs | GINE | GNNExplainer | done | acc=1.00 gt_auroc=0.49800000000000005 n=20 (capped) [cached] |
| MUTAG | GINE | IntegratedGradients | done | acc=0.80 gt_auroc=0.539863023686553 n=20 (capped) [cached] |
| MUTAG | GCN | IntegratedGradients | done | acc=0.75 gt_auroc=0.20333152686093864 n=20 (capped) [cached] |
| MUTAG | GAT | IntegratedGradients | done | acc=0.75 gt_auroc=0.13012396100631396 n=20 (capped) [cached] |
| MUTAG | MPNN | IntegratedGradients | done | acc=0.75 gt_auroc=0.35568985480750187 n=20 (capped) [cached] |
| MUTAG | AttentiveFP | IntegratedGradients | done | acc=0.65 gt_auroc=0.1315679418620595 n=20 (capped) [cached] |
| MUTAG | GINE | Saliency | done | acc=0.80 gt_auroc=0.02649591149591149 n=20 (capped) [cached] |
| MUTAG | GINE | InputXGradient | done | acc=0.80 gt_auroc=0.04156961774608832 n=20 (capped) [cached] |
| MUTAG | GINE | GNNExplainer | done | acc=0.80 gt_auroc=0.4913560404736875 n=20 (capped) [cached] |
| BBBP | GINE | IntegratedGradients | done | acc=1.00 gt_auroc=nan n=20 (capped) [cached] |
| ESOL | GINE | IntegratedGradients | done | rmse=1.132 r2=0.671 n=20 (capped) [cached] |
| ESOL | GINE | GNNExplainer | done | rmse=1.132 r2=0.671 n=20 (capped) [cached] |
| FreeSolv | GINE | IntegratedGradients | done | rmse=2.347 r2=0.614 n=20 (capped) [cached] |

## Blockers

_None._
