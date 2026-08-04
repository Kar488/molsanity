# ABSTENTION.md — when not to trust an attribution

The audit cannot tell a practitioner which attributor to pick without ground truth. It can tell them when to decline to trust one. Each signal below is available at inference time; molecules with the worst values are abstained on, and the table reports the ground-truth localisation of what remains.

`lift` is the gain in mean GT AUROC between keeping everything and keeping the best half. **A signal with lift <= 0 is useless for abstention on this data**, which is itself worth knowing: it means the corresponding intuition is unsupported.

| signal | n | GT AUROC @100% | @50% | lift | below chance @100% | @50% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| confidence | 13033 | 0.758 | 0.817 | +0.058 | 0.203 | 0.139 |
| rationale_reliance | 13033 | 0.758 | 0.813 | +0.055 | 0.203 | 0.150 |
| occ_spearman | 12631 | 0.758 | 0.801 | +0.043 | 0.205 | 0.154 |
| stability | 12109 | 0.770 | 0.782 | +0.012 | 0.183 | 0.164 |
| motif_top1_share | 13033 | 0.758 | 0.669 | -0.090 | 0.203 | 0.318 |

## Recommended rule

Rank molecules by **confidence** and abstain on the tail.
Keeping the top **10%** holds the share of retained molecules whose attribution is *below chance* to **9.8%** (from 20.3% at full coverage), with mean GT AUROC 0.829 over n=1303. Threshold: confidence $\geq$ 1.000.
Mean GT AUROC already exceeds 0.70 at full coverage (0.758), so a rule stated against the mean would be vacuous. The pooled mean hides the tail; the below-chance share does not.

---

**The transfer assumption.** These curves are computed where ground truth exists. Applying the rule to a real molecular dataset assumes the signal-reliability relationship carries over to cells where correctness cannot be measured. This paper's central finding is that such transfer fails across splits, so the assumption is stated here rather than relied on silently.

