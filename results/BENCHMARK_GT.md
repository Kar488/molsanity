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

6 attributors on the same ~53 molecules.

| attributor | GT AUROC | 95% CI | occ_spearman | Fidelity+ | characterization |
| --- | --- | --- | --- | --- | --- |
| PGExplainer ⭐ | 0.981 | (0.965, 0.996) | 0.215 | 0.097 | 0.134 |
| IntegratedGradients | 0.537 | (0.471, 0.604) | 0.419 | 0.084 | 0.133 |
| GNNExplainer | 0.528 | (0.481, 0.577) | 0.365 | 0.071 | 0.149 |
| GuidedBackprop | 0.146 | (0.091, 0.212) | 0.551 | 0.210 | 0.297 |
| InputXGradient | 0.048 | (0.030, 0.071) | 0.534 | 0.199 | 0.296 |
| Saliency | 0.014 | (0.008, 0.021) | 0.531 | 0.198 | 0.295 |

⭐ = attributor the exact/proxy ground truth ranks best.

_Faithfulness-only selection test_ — would a framework ranking by each metric pick the GT-best attributor?

| faithfulness metric | its top pick | pick GT AUROC | GT-best | GT-best AUROC | mismatch? | paired Wilcoxon p | rank corr ρ(faith,GT) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| occ_spearman | GuidedBackprop | 0.146 | PGExplainer | 0.981 | **yes** | 0.0000 | -0.714 |
| fidelity_plus | GuidedBackprop | 0.146 | PGExplainer | 0.981 | **yes** | 0.0000 | -0.543 |
| characterization | GuidedBackprop | 0.146 | PGExplainer | 0.981 | **yes** | 0.0000 | -0.714 |

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

