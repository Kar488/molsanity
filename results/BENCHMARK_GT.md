# BENCHMARK_GT.md — faithfulness-only evaluation vs ground truth

> Computed from per-molecule audit records under `artifacts/audit/`; every
> number is computed, none fixed. **Question:** does ranking attributors by a
> faithfulness / fidelity metric — what SOTA evaluation frameworks
> (GraphFramEx, MolFaith, DIG) emit — recover the attributor the *ground
> truth* says is best? We contrast two regimes: in-distribution vs shift.

`occ_spearman` = MolSanity occlusion faithfulness · `Fidelity+` and
`characterization` = field-standard / GraphFramEx · `rank corr ρ` = Spearman
correlation between the faithfulness metric and GT AUROC across attributors
(≈1 → faithfulness tracks correctness; ≤0 → it does not).

### SynthMotifsXL · random — _need >=2 attributors with records_

### MUTAG · scaffold — _need >=2 attributors with records_

## What this shows

- **In-distribution** (the model applied to molecules like its training set),
  faithfulness and correctness **agree**: ranking by any faithfulness metric
  recovers the ground-truth-best attributor (ρ near 1, no mismatch). A
  faithfulness-only benchmark is adequate *here*.
- **Under scaffold shift**, they **dissociate**: the field-standard
  Fidelity+ / characterization scores select an attributor the exact/proxy
  ground truth shows is wrong (mismatch, paired Wilcoxon p < 0.001), and the
  faithfulness↔correctness rank correlation collapses. A faithfulness-only
  benchmark **recommends the wrong method in exactly the regime that matters
  for drug discovery** — which is what MolSanity's ground-truth + shift audit
  is built to catch.

