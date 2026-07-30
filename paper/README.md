# paper/ — the MolSanity preprint

Two-column XeLaTeX preprint built **entirely from the committed `results/`
folder**. No number in the manuscript is hand-entered: figures, tables and every
inline value are generated at build time from

```
results/RESULTS.md                classification + regression audit matrices
results/BENCHMARK.md              head-to-head matrix (stability, GraphFramEx
                                  characterisation, PyG/DIG unfaithfulness)
results/PROGRESS.md               the run ledger: done / failed / skipped
results/artifacts/audit/<cell>/   per-molecule records + per-cell aggregate
results/artifacts/run_manifest.json  seed, library versions, hardware
configs/full.yaml                 the planned grid (coverage accounting)
```

```bash
cd paper && make          # figures + tables + main.pdf   (needs xelatex, matplotlib, scipy)
```

Re-run it after a new run lands and the whole paper updates — the ledger,
coverage counts, tables, figures, and the numbers quoted in the prose.

## Provenance handling (the part that matters)

`RESULTS.md` is keyed by cell and the last successful writer wins, so it retains
rows from **earlier runs** for cells that failed in the latest one. The build
therefore classifies every row:

- **current** — the cell has per-molecule records under
  `results/artifacts/audit/`, i.e. this run produced it;
- **carried** — the row survives from an earlier, reduced-budget CPU run.

Carried rows are marked `ᶜ` in every table, drawn with open markers / italic
values in every figure, and **excluded from every aggregate computed over
per-molecule records**. The headline analysis uses current-run cells only.

## Statistics recomputed from the records

`results/BENCHMARK_GT.md` is empty for the current run (both of its target cells
failed), so `figs/msdata.py` recomputes that analysis directly from the
committed per-molecule records: the faithfulness-only selection test, its paired
Wilcoxon tests, bootstrap CIs, the paired attributor comparisons, regime
stratification and calibration linkage. That is also what makes the
within-dataset shift contrast (same dataset, same backbone, same attributors,
only the split changes) possible.

## Layout

| path | what it is |
|---|---|
| `main.tex` | preamble, title block, running header, unicode fallbacks |
| `abstract.tex` | abstract (uses generated macros) |
| `body.tex` | all sections + the bibliography |
| `figs/msdata.py` | the only parser + all statistics |
| `figs/make_figures.py` | writes `figs/fig_*.pdf` (vector) |
| `figs/make_tables.py` | writes `generated/tab_*.tex` and `generated/macros.tex` |
| `figs/style.py` | shared figure style (CVD-safe palette, Pagella-matched serif) |
| `generated/` | build products: LaTeX tables + one `\newcommand` per quoted number |
| `OUTLINE.md`, `RELATED_WORK.md` | planning notes; the capability matrix in `RELATED_WORK.md` is parsed into Table 1 |

## Honesty rules the build enforces

- A cell that was not audited renders as `—`/`·`, never imputed.
- Failed cell-runs are reported with their error, not omitted.
- Coverage is computed by diffing the committed results against
  `configs/full.yaml` and the run ledger, so it cannot drift from reality.
- Bold in tables marks the better value **computed from the data**; values are
  never altered, only emphasised.
- Aggregates quoted in the prose (rank correlations, counts of
  faithful-but-wrong cells, medians per regime) are derived by
  `make_tables.py`, so prose, tables and figures cannot disagree.

## Releasing the artifacts (checkpoints + DOI)

The trained weights are archived under `results/artifacts/checkpoints/` by the
notebook's publish step, so a clone already answers "can you share your
checkpoints?". For a citable, permanent record — what a journal will ask for —
tag a release and let Zenodo archive it:

1. Sign in at <https://zenodo.org> with GitHub, then flip the switch for
   `Kar488/molsanity` under *GitHub* in your Zenodo account. One-time.
2. Tag and publish a GitHub release (e.g. `v1.0.0`). Zenodo archives the
   tarball automatically and mints a DOI.
3. Paste that DOI into the *Data and code availability* section of the paper
   (it currently reads *[DOI to be inserted on deposition]*).

`CITATION.cff` and `.zenodo.json` in the repository root supply the title,
author, ORCID, licence and keywords, so the deposit is populated correctly
rather than from the repo description.

## Requirements

`xelatex` with TeX Gyre Pagella (+ Pagella Math; falls back to Latin Modern
Math), plus `matplotlib`, `numpy` and `scipy`.
