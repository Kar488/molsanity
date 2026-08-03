# ABSTENTION.md — when not to trust an attribution

The audit cannot tell a practitioner which attributor to pick without ground truth. It can tell them when to decline to trust one. Each signal below is available at inference time; molecules with the worst values are abstained on, and the table reports the ground-truth localisation of what remains.

`lift` is the gain in mean GT AUROC between keeping everything and keeping the best half. **A signal with lift <= 0 is useless for abstention on this data**, which is itself worth knowing: it means the corresponding intuition is unsupported.

| signal | n | GT AUROC @100% | @50% | lift | below chance @100% | @50% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| rationale_reliance | 10626 | 0.766 | 0.839 | +0.073 | 0.213 | 0.138 |
| occ_spearman | 10619 | 0.766 | 0.824 | +0.058 | 0.213 | 0.147 |
| confidence | 10626 | 0.766 | 0.823 | +0.057 | 0.213 | 0.143 |
| stability | 10297 | 0.775 | 0.775 | +0.000 | 0.199 | 0.189 |
| motif_top1_share | 10626 | 0.766 | 0.642 | -0.124 | 0.213 | 0.370 |

## Recommended rule

Rank molecules by **rationale_reliance** and abstain on the tail.
Keeping the top **10%** holds the share of retained molecules whose attribution is *below chance* to **7.4%** (from 21.3% at full coverage), with mean GT AUROC 0.892 over n=1063. Threshold: rationale_reliance $\geq$ 0.948.
Mean GT AUROC already exceeds 0.70 at full coverage (0.766), so a rule stated against the mean would be vacuous. The pooled mean hides the tail; the below-chance share does not.

---

**The transfer assumption.** These curves are computed where ground truth exists. Applying the rule to a real molecular dataset assumes the signal-reliability relationship carries over to cells where correctness cannot be measured. This paper's central finding is that such transfer fails across splits, so the assumption is stated here rather than relied on silently.

