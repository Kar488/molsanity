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
scores every (dataset × backbone × attributor × split) cell on six axes:
motif-native coherence, occlusion-attribution faithfulness, ground-truth
localisation where node labels exist, cross-checkpoint stability, calibration
linkage, and confidence/correctness regime stratification. Our central finding
is that faithfulness is not correctness, and that the two carry no dependable
relationship in either regime. Across 30 selection tests - 5 molecular ground-
truth arms × two splits × 3 ranking metrics, with dataset, backbone and
attributor set held fixed within an arm - a faithfulness-only ranking picks an
attributor other than the ground-truth-best one in 26, and this is no less
true in distribution (14 of 15) than under scaffold shift (12 of 15). The
sharpest case is MUTAG under a Bemis-Murcko scaffold split, where all 3
metrics miss. The occlusion measure selects GuidedBP, whose agreement with the
mutagenic nitro motif is GT AUROC 0.013 - near-perfectly anti-aligned, and
sixth of the 7 attributors audited - while the ground truth ranks GNNExpl.
best at 0.826 in the audited seed, 0.774+/-0.086 across 3 (median paired gap
0.967 AUROC, Wilcoxon p<0.001, Benjamini-Hochberg q<0.001 over the 30
selection tests). Pooled over all 47 cells of the 5 molecular ground-truth
arms (each an across-seed mean of 3 seeds), the faithfulness-correctness rank
correlation is +0.222 in distribution (p=0.134) and -0.124 under shift
(p=0.405) - neither distinguishable from zero. Per arm under shift it runs
from -0.564 on MUTAG to +0.786 on FluorideCarbonyl, so reliability is a
property of the (dataset, backbone, attributor, split) cell rather than of the
attributor, and no pooled coefficient describes any of the arms. We report
against our own prior result: restricted to the 3 arms of an earlier version
of this analysis the same computation gives -0.356 at p=0.042, and adding two
externally authored molecular rationale benchmarks removes the effect.
Faithfulness itself does not fall under shift - across the same 47 cells it
rises, from 0.049 to 0.132 (p=0.005), while ground-truth localisation does not
move (0.660 to 0.658, p=0.539). The metric therefore moves in the reassuring
direction across a shift that leaves correctness unchanged, and gives no
warning either way. Using 31785 committed per-molecule records we further find
that on confidently-wrong predictions ground-truth localisation degrades
(0.769 to 0.681, n=275) while their measured faithfulness improves (0.142 to
0.325) and their stability is no worse - both proxies point away from the
failure - and that the calibration-reliability link attenuates from a per-cell
median of 0.144 to 0.074 when cells are pooled, a Simpson's-paradox trap for
anyone reporting a single aggregate number. Results are the committed
full.yaml run: 558 of 558 cell-runs completed. Every number, figure and table
regenerates from the committed artifacts.

## Acknowledgements (paste-ready)

> This work was carried out at La Trobe University. It builds directly on
> open-source software and released benchmarks: PyTorch Geometric, Captum,
> RDKit, DIG and GraphXAI, and the MUTAG, MoleculeNet and Therapeutics Data
> Commons collections. MolSanity wraps the canonical implementations of the
> attribution methods it audits rather than reimplementing them, and would not
> be possible without the authors of those packages releasing them openly.
> Compute for the reported sweep was provided by Google Colab.
>
> **Generative AI disclosure.** An AI coding assistant was used during
> software development and manuscript preparation. It was not used to
> generate, select or interpret results: all experimental results were
> produced by the released code, and every reported number, figure and table
> is generated from the committed artifacts rather than written by hand. The
> authors designed the study, verified the analyses and take full
> responsibility for the content.

Three things to check before pasting:

1. **Funding.** The draft claims none. If any grant, scholarship or internal
   support applies, name it — an undeclared funder is a correction later.
2. **Compute.** It says Google Colab; amend if any of the sweep ran elsewhere.
3. **The AI disclosure is the one real decision.** Springer Nature and ChemRxiv
   both require disclosure of generative-AI assistance in preparing a
   manuscript, and neither permits AI authorship. Given how this project was
   built, the honest choice is to declare it, and declaring it costs nothing —
   the reproducibility argument in §9 is stronger for it, not weaker, because
   every number regenerates from code rather than resting on anyone's typing.
   Delete the paragraph only if you are certain your reading of the policy
   differs.

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
