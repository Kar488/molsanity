# ABSTENTION.md — when not to trust an attribution

The audit cannot tell a practitioner which attributor to pick without ground truth. It can tell them when to decline to trust one. Each signal below is available at inference time; molecules with the worst values are abstained on, and the table reports the ground-truth localisation of what remains.

`lift` is the gain in mean GT AUROC between keeping everything and keeping the best half. **A signal with lift <= 0 is useless for abstention on this data**, which is itself worth knowing: it means the corresponding intuition is unsupported.

| signal | n | GT AUROC @100% | @50% | lift | below chance @100% | @50% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| confidence | 10822 | 0.750 | 0.823 | +0.073 | 0.210 | 0.138 |
| rationale_reliance | 10822 | 0.750 | 0.811 | +0.061 | 0.210 | 0.158 |
| occ_spearman | 10814 | 0.750 | 0.800 | +0.049 | 0.210 | 0.155 |
| stability | 10487 | 0.760 | 0.771 | +0.011 | 0.194 | 0.173 |
| motif_top1_share | 10822 | 0.750 | 0.637 | -0.113 | 0.210 | 0.353 |

## Recommended rule

Rank molecules by **confidence** and abstain on the tail.
Keeping the top **10%** holds the share of retained molecules whose attribution is *below chance* to **9.2%** (from 21.0% at full coverage), with mean GT AUROC 0.840 over n=1082. Threshold: confidence $\geq$ 1.000.
Mean GT AUROC already exceeds 0.70 at full coverage (0.750), so a rule stated against the mean would be vacuous. The pooled mean hides the tail; the below-chance share does not.

---

**The transfer assumption.** These curves are computed where ground truth exists. Applying the rule to a real molecular dataset assumes the signal-reliability relationship carries over to cells where correctness cannot be measured. This paper's central finding is that such transfer fails across splits, so the assumption is stated here rather than relied on silently.

