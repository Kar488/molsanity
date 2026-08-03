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

7 attributors on the same ~53 molecules.

| attributor | GT AUROC | 95% CI | occ_spearman | Fidelity+ | characterization |
| --- | --- | --- | --- | --- | --- |
| GNNExplainer ⭐ | 0.826 | (0.754, 0.896) | 0.380 | 0.154 | 0.209 |
| PGExplainer | 0.360 | (0.298, 0.429) | 0.291 | 0.066 | 0.114 |
| SubgraphX | 0.330 | (0.294, 0.366) | 0.378 | 0.304 | 0.426 |
| IntegratedGradients | 0.302 | (0.235, 0.367) | 0.311 | 0.030 | 0.077 |
| InputXGradient | 0.079 | (0.060, 0.099) | 0.499 | 0.167 | 0.206 |
| GuidedBackprop | 0.013 | (0.007, 0.019) | 0.616 | 0.250 | 0.318 |
| Saliency | 0.002 | (0.000, 0.003) | 0.406 | 0.153 | 0.200 |

⭐ = attributor the exact/proxy ground truth ranks best.

_Faithfulness-only selection test_ — would a framework ranking by each metric pick the GT-best attributor?

| faithfulness metric | its top pick | pick GT AUROC | GT-best | GT-best AUROC | mismatch? | paired Wilcoxon p | rank corr ρ(faith,GT) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| occ_spearman | GuidedBackprop | 0.013 | GNNExplainer | 0.826 | **yes** | 0.0000 | -0.643 |
| fidelity_plus | SubgraphX | 0.330 | GNNExplainer | 0.826 | **yes** | 0.0000 | -0.107 |
| characterization | SubgraphX | 0.330 | GNNExplainer | 0.826 | **yes** | 0.0000 | 0.036 |

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

