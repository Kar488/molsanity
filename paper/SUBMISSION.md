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

Correspondence: 22557016@students.latrobe.edu.au (institutional);
karthik.iyer@hotmail.com. Give the institutional address as the primary
contact — several publishers verify affiliation against the domain, and a
free-mail-only corresponding address can hold up desk processing.

## Files to upload

The submission form takes an **editable** manuscript file — a Word document, or
LaTeX with figures zipped, which the publisher compiles. **A PDF is not
accepted as the manuscript file.** Build everything with
`make -C paper submission-files`; it writes to `paper/submission/`.

| Form field | File | Notes |
| --- | --- | --- |
| Manuscript file | `molsanity_latex_sources.zip` | LaTeX sources + figures. **Requires XeLaTeX** (fontspec/TeX Gyre Pagella); it will not build under pdfLaTeX. The archive's README.txt says so, but flag it in the cover note too — if their compile service is pdfLaTeX-only, ask the editorial office how to proceed rather than silently sending something that fails technical check. |
| Supplementary material | `Additional_file_1.pdf` | Supplementary notes and summary tables. |
| Supplementary material | `Additional_file_2.csv` | Per-cell audit matrix (558 rows). |
| Supplementary material | `Additional_file_3.csv` | Across-seed variance (886 rows). |
| Supplementary material | `Additional_file_4.csv` | Head-to-head benchmark (520 rows). |

Each is under BMC's 20 MB per-file limit. The manuscript declares all four in
an "Additional files" list and cites them in order in the text, which is what
BMC's technical check looks for. Do **not** upload the `.md` files in
`paper/supplementary/` — that bundle is the repository's own copy of the
generated reports, not a journal additional-file set.

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
reliability: existing frameworks ask whether an explanation is faithful to the
model, not whether it identifies the chemistry that determines the property,
nor where it stops being trustworthy under scaffold shift. MolSanity is a
reliability-audit framework that wraps canonical implementations (Captum,
PyTorch Geometric, RDKit) rather than proposing a new attributor, scoring
every (dataset × backbone × attributor × split) cell on six axes: motif-native
coherence, occlusion-attribution faithfulness, ground-truth localisation where
node labels exist, cross-checkpoint stability, calibration linkage, and
confidence/correctness regime stratification. Our central finding is that
faithfulness is not correctness, and that the two carry no dependable
relationship in either regime. Across 30 selection tests - 5 molecular ground-
truth arms × two splits × 3 ranking metrics - a faithfulness-only ranking
picks an attributor other than the ground-truth-best one in 26, and this is no
less true in distribution (14 of 15) than under scaffold shift (12 of 15); on
MUTAG under shift it prefers an attributor anti-aligned with the nitro motif
(GT AUROC 0.013) over one at 0.826. Pooled over 47 cells the faithfulness-
correctness rank correlation is +0.222 in distribution (p=0.134) and -0.124
under shift (p=0.405), neither distinguishable from zero, while per arm under
shift it runs from -0.564 to +0.786: reliability is a property of the
individual (dataset, backbone, attributor, split) cell rather than of the
attributor. Restricted to the 3 arms of an earlier analysis it gives -0.356
(p=0.042); two externally authored rationale benchmarks remove the effect, and
we report the 5-arm result. Faithfulness itself does not fall under shift - it
rises, from 0.049 to 0.132, while ground-truth localisation does not move - so
the metric gives no warning either way. Over 31785 per-molecule records,
localisation degrades on confidently-wrong predictions (0.769 to 0.681) while
their measured faithfulness improves, and the calibration-reliability link
attenuates from a per-cell median of 0.144 to 0.074 when cells are pooled.
Every number, figure and table regenerates from the committed artifacts.

## Collection

**AI and XAI in Drug Discovery.** The paper is an explainability-evaluation
study on molecular property models, which is squarely the collection's scope;
"Diversifying cheminformatics" is a community/EDI collection and does not fit.

## Cover letter (paste-ready)

> Dear Editors,
>
> Please consider our manuscript, "MolSanity: A Reliability Audit for Feature
> Attributions on Molecular Graph Neural Networks", for publication in the
> Journal of Cheminformatics, as part of the AI and XAI in Drug Discovery
> collection.
>
> Feature attributions are routinely shown to chemists as evidence for a
> model's prediction, and the frameworks used to evaluate them ask whether an
> explanation is faithful to the model rather than whether it identifies the
> chemistry that determines the property. Those are different questions, and
> our results indicate they do not answer one another. MolSanity audits every
> (dataset, backbone, attributor, split) cell on six axes and benchmarks
> against the field-standard metrics computed on the same molecules, wrapping
> the canonical implementations (Captum, PyTorch Geometric, RDKit, DIG,
> GraphXAI) rather than proposing another attribution method.
>
> Across 30 selection tests spanning five molecular ground-truth arms, a
> faithfulness-only ranking picks an attributor other than the ground-truth-best
> one in 26 -- and no less often in distribution than under scaffold shift.
> Pooled over 47 cells the faithfulness-correctness rank correlation is not
> distinguishable from zero in either regime, while per arm under shift it
> ranges from -0.564 to +0.786 under an identical protocol. The practical
> conclusion is that attribution reliability is a property of the specific
> cell rather than of the attribution method, which is not how the field
> currently reports it.
>
> We would draw the editors' attention to one aspect of the study. An earlier
> version of this analysis, restricted to three arms, found a significant
> collapse in that correlation under scaffold shift (-0.356, p = 0.042). Adding
> two externally authored rationale benchmarks removed the effect. We report
> the five-arm result, state the superseded one alongside it, and treat the
> disagreement as a finding about how narrowly such claims generalise. The
> manuscript reports negative and null results at the same length as positive
> ones throughout.
>
> Every number, figure and table in the manuscript is generated from committed
> artifacts by released code; none is transcribed by hand. The repository
> (https://github.com/Kar488/molsanity, MIT licence) contains the pipeline,
> configurations, trained checkpoints, per-molecule audit records and the run
> manifest, and a single command regenerates the manuscript from them.
>
> The manuscript is submitted as LaTeX source. It requires XeLaTeX rather than
> pdfLaTeX, as it uses fontspec to set TeX Gyre Pagella; a note to this effect
> is included in the archive. Please let us know if your production system
> requires a pdfLaTeX-compatible version and we will supply one.
>
> A preprint of an earlier version is available on ChemRxiv. The work is not
> under consideration elsewhere, all authors have approved the submission, and
> we declare no competing interests.
>
> Yours sincerely,
> Karthik Iyer and Nasser Sabar
> Department of Computer Science and Information Technology, La Trobe
> University, Melbourne, Australia
> 22557016@students.latrobe.edu.au

Before sending, check three things in the letter: the ChemRxiv DOI (add it
once issued), the funding statement, and whether any of the sweep ran outside
Google Colab.

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
