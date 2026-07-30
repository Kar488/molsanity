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

### SynthMotifsXL · GINE · random split — in-distribution (exact GT, n≈120)

6 attributors on the same ~120 molecules.

| attributor | GT AUROC | 95% CI | occ_spearman | Fidelity+ | characterization |
| --- | --- | --- | --- | --- | --- |
| GuidedBackprop ⭐ | 1.000 | (0.999, 1.000) | 0.529 | 0.495 | 0.599 |
| Saliency | 0.990 | (0.986, 0.993) | 0.424 | 0.492 | 0.496 |
| InputXGradient | 0.989 | (0.986, 0.992) | 0.393 | 0.493 | 0.529 |
| IntegratedGradients | 0.987 | (0.983, 0.991) | 0.403 | 0.493 | 0.595 |
| GNNExplainer | 0.501 | (0.478, 0.525) | 0.033 | 0.364 | 0.209 |
| PGExplainer | 0.269 | (0.248, 0.290) | -0.227 | 0.050 | 0.037 |

⭐ = attributor the exact/proxy ground truth ranks best.

_Faithfulness-only selection test_ — would a framework ranking by each metric pick the GT-best attributor?

| faithfulness metric | its top pick | pick GT AUROC | GT-best | GT-best AUROC | mismatch? | paired Wilcoxon p | rank corr ρ(faith,GT) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| occ_spearman | GuidedBackprop | 1.000 | GuidedBackprop | 1.000 | no | — | 0.943 |
| fidelity_plus | GuidedBackprop | 1.000 | GuidedBackprop | 1.000 | no | — | 0.829 |
| characterization | GuidedBackprop | 1.000 | GuidedBackprop | 1.000 | no | — | 0.771 |

### MUTAG · GINE · scaffold split — scaffold shift (motif-proxy GT)

6 attributors on the same ~20 molecules.

| attributor | GT AUROC | 95% CI | occ_spearman | Fidelity+ | characterization |
| --- | --- | --- | --- | --- | --- |
| IntegratedGradients ⭐ | 0.540 | (0.471, 0.604) | 0.414 | 0.252 | 0.282 |
| GNNExplainer | 0.491 | (0.411, 0.570) | 0.279 | 0.113 | 0.163 |
| PGExplainer | 0.401 | (0.302, 0.497) | 0.118 | 0.026 | 0.059 |
| GuidedBackprop | 0.112 | (0.067, 0.159) | 0.341 | 0.272 | 0.284 |
| InputXGradient | 0.042 | (0.018, 0.066) | 0.398 | 0.251 | 0.277 |
| Saliency | 0.026 | (0.011, 0.045) | 0.376 | 0.267 | 0.285 |

⭐ = attributor the exact/proxy ground truth ranks best.

_Faithfulness-only selection test_ — would a framework ranking by each metric pick the GT-best attributor?

| faithfulness metric | its top pick | pick GT AUROC | GT-best | GT-best AUROC | mismatch? | paired Wilcoxon p | rank corr ρ(faith,GT) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| occ_spearman | IntegratedGradients | 0.540 | IntegratedGradients | 0.540 | no | — | -0.029 |
| fidelity_plus | GuidedBackprop | 0.112 | IntegratedGradients | 0.540 | **yes** | 0.0001 | -0.371 |
| characterization | Saliency | 0.026 | IntegratedGradients | 0.540 | **yes** | 0.0001 | -0.486 |

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

