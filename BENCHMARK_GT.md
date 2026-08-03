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

### MUTAG · GINE · random split — in-distribution (motif-proxy GT)

7 attributors on the same ~58 molecules.

| attributor | GT AUROC | 95% CI | occ_spearman | Fidelity+ | characterization |
| --- | --- | --- | --- | --- | --- |
| GNNExplainer ⭐ | 0.858 | (0.791, 0.921) | -0.170 | 0.310 | 0.338 |
| IntegratedGradients | 0.496 | (0.469, 0.523) | -0.196 | 0.551 | 0.347 |
| SubgraphX | 0.348 | (0.316, 0.378) | -0.154 | 0.342 | 0.450 |
| PGExplainer | 0.251 | (0.223, 0.278) | -0.351 | 0.379 | 0.225 |
| GuidedBackprop | 0.037 | (0.018, 0.066) | -0.089 | 0.540 | 0.178 |
| InputXGradient | 0.013 | (0.005, 0.023) | -0.200 | 0.491 | 0.160 |
| Saliency | 0.002 | (0.000, 0.005) | -0.195 | 0.494 | 0.163 |

⭐ = attributor the exact/proxy ground truth ranks best.

_Faithfulness-only selection test_ — would a framework ranking by each metric pick the GT-best attributor?

| faithfulness metric | its top pick | pick GT AUROC | GT-best | GT-best AUROC | mismatch? | paired Wilcoxon p | rank corr ρ(faith,GT) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| occ_spearman | GuidedBackprop | 0.037 | GNNExplainer | 0.858 | **yes** | 0.0000 | 0.143 |
| fidelity_plus | IntegratedGradients | 0.496 | GNNExplainer | 0.858 | **yes** | 0.0000 | -0.357 |
| characterization | SubgraphX | 0.348 | GNNExplainer | 0.858 | **yes** | 0.0000 | 0.821 |

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

- **MUTAG · GINE · random split**: ranking by faithfulness picks the wrong attributor on 3 of 3 metrics (ρ ranges -0.36 to +0.82).
- **MUTAG · GINE · scaffold split**: ranking by faithfulness picks the wrong attributor on 3 of 3 metrics (ρ ranges -0.64 to +0.04).

Mean rank correlation falls from +0.20 in-distribution to -0.24 under scaffold shift (-0.44). Faithfulness and correctness dissociate under shift, so a faithfulness-only benchmark can recommend the wrong method in exactly the regime that matters for drug discovery.

_Single-seed figures. Read `SEED_VARIANCE.md` before treating any attributor ranking above as an effect._

