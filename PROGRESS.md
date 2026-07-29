# PROGRESS.md — MolSanity rolling progress

_Last run: `benchmark_gt.yaml` @ 20260729_174701._

## Cell tally

- done: **6**  · failed: **0**  · skipped/blocked: **0**

## Cells (dataset × backbone × attributor)

| dataset | backbone | attributor | status | detail |
| --- | --- | --- | --- | --- |
| SynthMotifsXL | GINE | IntegratedGradients | done | acc=1.00 gt_auroc=0.9867333333333334 n=120 (capped) [cached] |
| SynthMotifsXL | GINE | Saliency | done | acc=1.00 gt_auroc=0.9898000000000001 n=120 (capped) [cached] |
| SynthMotifsXL | GINE | InputXGradient | done | acc=1.00 gt_auroc=0.9893333333333333 n=120 (capped) [cached] |
| SynthMotifsXL | GINE | GuidedBackprop | done | acc=1.00 gt_auroc=0.9996000000000002 n=120 (capped) [cached] |
| SynthMotifsXL | GINE | GNNExplainer | done | acc=1.00 gt_auroc=0.5006666666666668 n=120 (capped) |
| SynthMotifsXL | GINE | PGExplainer | done | acc=1.00 gt_auroc=0.26903333333333335 n=120 (capped) |

## Blockers

_None._
