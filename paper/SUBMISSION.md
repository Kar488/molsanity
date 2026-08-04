# Preprint / journal submission metadata

Paste-ready fields for the ChemRxiv submission form and, later, the Journal of
Cheminformatics one. The abstract below is the manuscript's abstract with the
LaTeX macros expanded and the PDF's line-break hyphenation removed — it is a
copy of what the PDF says, not a reworded version. If the numbers in the paper
change, regenerate the PDF and re-copy this from it.

---

## Title

MolSanity: A Reliability Audit for Feature Attributions on Molecular Graph
Neural Networks

## Authors

Karthik Iyer (corresponding, ORCID 0009-0004-0593-1602), Nasser Sabar.
Department of Computer Science and Information Technology, La Trobe
University, Melbourne, Victoria 3086, Australia.

## Category

Theoretical and Computational Chemistry — machine learning / cheminformatics.

## Keywords

explainable AI; feature attribution; graph neural networks; molecular property
prediction; scaffold split; distribution shift; model reliability;
faithfulness; benchmark; reproducibility

## Licence

CC BY 4.0 — matches the licence Journal of Cheminformatics publishes under, so
the preprint and the journal version do not end up under different terms.

## Abstract (plain text)

Feature attributions are routinely used to justify molecular graph neural
network (GNN) predictions to chemists, yet they are almost never audited for
reliability: existing evaluation frameworks ask whether an explanation is
faithful to the model, not whether the model's explanation can be trusted, and
not where it stops being trustworthy under the scaffold shift that
characterises real drug-discovery workflows. We present MolSanity, a
reliability-audit framework that wraps canonical attribution implementations
(Captum, PyTorch Geometric, RDKit) rather than proposing a new attributor, and
scores every (dataset x backbone x attributor x split) cell on six axes:
motif-native coherence, occlusion-attribution faithfulness, ground-truth
localisation where node labels exist, cross-checkpoint stability, calibration
linkage, and confidence/correctness regime stratification. Our central finding
is that faithfulness is not correctness, and that the relationship between them
collapses under shift. Holding dataset, backbone and attributor set fixed and
changing only the split, all 3 faithfulness metrics we test (our occlusion
measure, Fidelity+ and the GraphFramEx characterisation score) fail to recover
the ground-truth-best attributor on MUTAG under a Bemis-Murcko scaffold split.
The occlusion measure selects GuidedBP, whose agreement with the mutagenic
nitro motif is GT AUROC 0.013 - near-perfectly anti-aligned, and sixth of the 7
attributors audited - while the ground truth ranks GNNExplainer best at 0.826
(median paired gap 0.967 AUROC, Wilcoxon p < 0.001, Benjamini-Hochberg q <
0.001 over the 18 selection tests). What separates the regimes is the rank
correlation between faithfulness and correctness. Pooled over all 33 cells of
the 3 molecular ground-truth arms (each an across-seed mean of 3 seeds), it
moves from +0.009 in distribution (p = 0.962) to -0.353 under shift (p =
0.044). We state plainly how much of that pooled figure any one arm carries:
dropping MUTAG leaves -0.027 (p = 0.907, n = 22 cells), so the effect is MUTAG
together with corroboration rather than 3 arms independently agreeing. On MUTAG
alone the contrast is +0.143 to -0.643; 2 of 3 arms move in that direction and
one does not, and the paper says why rather than pooling the disagreement out
of sight. We are equally explicit that faithfulness rankings mismatch the
ground truth in-distribution as well (3 of 3 metrics on MUTAG), so the finding
is a collapse in rank correlation rather than agreement followed by
disagreement. Faithfulness itself does not fall under shift - across the same
33 cells it rises, from 0.028 to 0.132 (p = 0.008), while ground-truth
localisation does not move (0.641 to 0.631, p = 0.888). The metric therefore
moves in the reassuring direction in exactly the regime where its relationship
to correctness breaks, and gives no warning. Using 26185 committed per-molecule
records we further find that on confidently-wrong predictions ground-truth
localisation degrades (0.790 to 0.674, n = 257) while their measured
faithfulness improves (0.126 to 0.330) and their stability is no worse - both
proxies point away from the failure - and that the calibration-reliability link
attenuates from a per-cell median of 0.137 to 0.046 when cells are pooled, a
Simpson's-paradox trap for anyone reporting a single aggregate number. Results
are the committed full.yaml run: 474 of 474 cell-runs completed. Every number,
figure and table regenerates from the committed artifacts.

## Declarations

- **Conflict of interest**: none.
- **Funding**: none to declare (amend if La Trobe support applies).
- **Data and code**: https://github.com/Kar488/molsanity, MIT licence.
- **Generative AI**: disclose per the venue's policy if AI assistance was used
  in preparing the manuscript; both ChemRxiv and Springer Nature ask.

## Notes on the form

- The uploader tries to auto-extract title, authors and abstract from the PDF.
  Two-column PDFs extract badly — check every field against this file rather
  than trusting the extraction.
- Every co-author gets a confirmation email and must accept before the preprint
  posts. Make sure the address on file for Nasser Sabar is current.
- The abstract above deliberately spells out "Section 5.2" rather than using a
  section-number cross-reference, and uses "x" for the multiplication sign and
  plain hyphens for dashes, because the abstract box is plain text.
