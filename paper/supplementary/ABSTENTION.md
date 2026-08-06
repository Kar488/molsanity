# ABSTENTION.md — when not to trust an attribution

The audit cannot tell a practitioner which attributor to pick without ground truth. It can tell them when to decline to trust one. Each signal below is available at inference time; molecules with the worst values are abstained on, and the table reports the ground-truth localisation of what remains.

`lift` is the gain in mean GT AUROC between keeping everything and keeping the best half. **A signal with lift <= 0 is useless for abstention on this data**, which is itself worth knowing: it means the corresponding intuition is unsupported.

| signal | n | GT AUROC @100% | @50% | lift | below chance @100% | @50% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| occ_spearman | 15201 | 0.748 | 0.804 | +0.056 | 0.216 | 0.151 |
| confidence | 15609 | 0.749 | 0.793 | +0.044 | 0.214 | 0.168 |
| rationale_reliance | 15609 | 0.749 | 0.782 | +0.032 | 0.214 | 0.184 |
| stability | 14316 | 0.764 | 0.784 | +0.021 | 0.191 | 0.166 |
| motif_top1_share | 15609 | 0.749 | 0.667 | -0.082 | 0.214 | 0.323 |

## Recommended rule

Rank molecules by **occ_spearman** and abstain on the tail.
No coverage level gets the below-chance share under 10%. The best achievable is **14.5%** at 37% coverage. Abstention narrows the problem here but does not solve it, and that is the honest reading.
Mean GT AUROC already exceeds 0.70 at full coverage (0.748), so a rule stated against the mean would be vacuous. The pooled mean hides the tail; the below-chance share does not.

---

**The transfer assumption.** These curves are computed where ground truth exists. Applying the rule to a real molecular dataset assumes the signal-reliability relationship carries over to cells where correctness cannot be measured. This paper's central finding is that such transfer fails across splits, so the assumption is stated here rather than relied on silently.

