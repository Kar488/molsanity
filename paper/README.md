# paper/ — the MolSanity preprint

Two-column XeLaTeX preprint built **entirely from the committed results**. No
number in the manuscript is hand-entered: figures, tables and every inline
value are generated from `RESULTS.md`, `BENCHMARK.md`, `BENCHMARK_GT.json` and
`configs/full.yaml` at build time.

```bash
cd paper && make          # figures + tables + main.pdf   (needs xelatex, matplotlib)
```

Re-run it after more grid cells land and the whole paper updates — coverage
counts, tables, figures, and the numbers quoted in the prose.

## Layout

| path | what it is |
|---|---|
| `main.tex` | preamble, title block, running header, unicode fallbacks |
| `abstract.tex` | abstract (uses generated macros) |
| `body.tex` | all sections + the bibliography |
| `figs/msdata.py` | the only parser: reads the committed result files |
| `figs/make_figures.py` | writes `figs/fig_*.pdf` (vector) |
| `figs/make_tables.py` | writes `generated/tab_*.tex` and `generated/macros.tex` |
| `figs/style.py` | shared figure style (CVD-safe palette, Pagella-matched serif) |
| `generated/` | build products: LaTeX tables + one `\newcommand` per quoted number |
| `OUTLINE.md`, `RELATED_WORK.md` | pre-existing planning notes; `RELATED_WORK.md`'s capability matrix is parsed into Table 1 |

## Honesty rules the build enforces

- A cell that has not been audited is rendered `---` or left out entirely —
  never imputed, never interpolated.
- Coverage (`R of N planned cell-runs complete`) is computed by diffing the
  committed results against `configs/full.yaml`, so the reported coverage can
  never drift from reality.
- Bold in tables marks the better value **computed from the data**; values are
  never altered, only emphasised.
- `paper/figs/make_tables.py` also derives the aggregate statistics quoted in
  the text (rank correlations between regimes, counts of faithful-but-wrong
  cells, medians per regime), so prose and tables cannot disagree.

## Requirements

`xelatex` with TeX Gyre Pagella (+ Pagella Math; falls back to Latin Modern
Math), and `matplotlib` for the figures.
