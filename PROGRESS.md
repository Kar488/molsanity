# PROGRESS.md — MolSanity rolling progress

_Last run: `matrix.yaml` @ 20260728_143130._

## Cell tally

- done: **9**  · failed: **0**  · skipped/blocked: **0**

## Cells (dataset × backbone × attributor)

| dataset | backbone | attributor | status | detail |
| --- | --- | --- | --- | --- |
| MUTAG | GINE | IntegratedGradients | done | acc=0.80 gt_auroc=0.539863023686553 n=20 (capped) |
| MUTAG | GCN | IntegratedGradients | done | acc=0.75 gt_auroc=0.20333152686093864 n=20 (capped) |
| MUTAG | GAT | IntegratedGradients | done | acc=0.75 gt_auroc=0.13012396100631396 n=20 (capped) |
| MUTAG | MPNN | IntegratedGradients | done | acc=0.75 gt_auroc=0.35568985480750187 n=20 (capped) |
| MUTAG | AttentiveFP | IntegratedGradients | done | acc=0.65 gt_auroc=0.1315679418620595 n=20 (capped) |
| MUTAG | GINE | Saliency | done | acc=0.80 gt_auroc=0.02649591149591149 n=20 (capped) |
| MUTAG | GINE | InputXGradient | done | acc=0.80 gt_auroc=0.04156961774608832 n=20 (capped) |
| MUTAG | GINE | GNNExplainer | done | acc=0.80 gt_auroc=0.4913560404736875 n=20 (capped) |
| BBBP | GINE | IntegratedGradients | done | acc=1.00 gt_auroc=nan n=20 (capped) |

## Blockers

_None._
