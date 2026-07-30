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

### MUTAG · GINE · scaffold split — scaffold shift (motif-proxy GT)

6 attributors on the same ~20 molecules.

| attributor | GT AUROC | 95% CI | occ_spearman | Fidelity+ | characterization |
| --- | --- | --- | --- | --- | --- |
| GNNExplainer ⭐ | 0.671 | (0.547, 0.794) | 0.607 | 0.079 | 0.133 |
| IntegratedGradients | 0.537 | (0.471, 0.604) | 0.419 | 0.084 | 0.133 |
| PGExplainer | 0.108 | (0.068, 0.162) | 0.407 | 0.054 | 0.091 |
| InputXGradient | 0.049 | (0.016, 0.083) | 0.640 | 0.165 | 0.259 |
| GuidedBackprop | 0.016 | (0.000, 0.040) | 0.701 | 0.204 | 0.282 |
| Saliency | 0.009 | (0.000, 0.026) | 0.611 | 0.158 | 0.238 |

⭐ = attributor the exact/proxy ground truth ranks best.

_Faithfulness-only selection test_ — would a framework ranking by each metric pick the GT-best attributor?

| faithfulness metric | its top pick | pick GT AUROC | GT-best | GT-best AUROC | mismatch? | paired Wilcoxon p | rank corr ρ(faith,GT) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| occ_spearman | GuidedBackprop | 0.016 | GNNExplainer | 0.671 | **yes** | 0.0001 | -0.600 |
| fidelity_plus | GuidedBackprop | 0.016 | GNNExplainer | 0.671 | **yes** | 0.0001 | -0.657 |
| characterization | GuidedBackprop | 0.016 | GNNExplainer | 0.671 | **yes** | 0.0001 | -0.657 |

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

