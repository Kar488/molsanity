# PROGRESS.md — MolSanity rolling progress

_Last run: `smoke.yaml` @ 20260728_075613._

## Cell tally

- done: **1**  · failed: **0**  · skipped/blocked: **0**

## Cells (dataset × backbone × attributor)

| dataset | backbone | attributor | status | detail |
| --- | --- | --- | --- | --- |
| MUTAG | GINE | IntegratedGradients | done | acc=0.60 gt_auroc=0.21770501829325356 n=20 (capped) |

## Key finding (first slice, validated)

MUTAG × GINE × Integrated Gradients under a **scaffold split** demonstrates
MolSanity's core distinction — **faithfulness ≠ correctness**:

- IG is **faithful to the model**: occlusion Spearman ≈ 0.58, top-1 motif
  agreement 0.80, Fidelity+ ≈ 0.27 > Fidelity− (numbers in RESULTS.md).
- IG does **not** recover the ground-truth nitro motif: attribution-vs-GT AUROC
  ≈ **0.22** (chance 0.5) — *anti-aligned*. The case-study figure shows IG
  lighting up the fused-aromatic core, not the NO₂ group.

This is a genuine (and honest) **negative result** for GT localisation that the
audit surfaces exactly as designed. See `results_figures/MUTAG_GINE_IG/`.

## Blockers

_None for the first slice. Broadening blockers (TDC, GraphXAI) tracked in TASKS.md._
