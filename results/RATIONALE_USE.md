# RATIONALE_USE.md — does the model actually read the ground truth?

Faber et al. (KDD 2021) argue that scoring attributions against a known
rationale misleads when the trained model did not use that rationale: a
low GT AUROC would then be a fact about the model, not the explanation.
This is testable. Occlude the ground-truth substructure; if the
prediction collapses, the model *is* using it.

- molecules where the model reads the ground truth: **4266**
- molecules where it does not (Faber applies): **6360**
- mean GT AUROC when the model reads it: **0.838**
- mean GT AUROC when it does not: **0.718**

## The number that answers the objection

**597** molecules (0.140 of those the model
demonstrably reads the ground truth from) still receive an attribution
anti-aligned with it. On those, no appeal to an alternative rationale
explains the result: the attribution misdescribes a model that is
provably using the substructure the attribution ranks lowest.
