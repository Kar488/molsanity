# paper/ — MolSanity preprint

Two-column XeLaTeX preprint built **entirely** from the committed results.

```bash
python figs/make_figs.py      # regenerate all figures (vector PDF)
python figs/make_tables.py    # regenerate all tables + \num* macros
xelatex main.tex && xelatex main.tex   # -> main.pdf
```

## No hand-typed numbers

`figs/load_results.py` parses `RESULTS.md` into tidy records; `make_tables.py`
emits every table as a `.tex` fragment plus `figs/numbers.tex`, a set of
`\num...` macros for the scalars quoted in prose. `body.tex` `\input`s both, so
a value can only change by re-running the pipeline.

| file | role |
|---|---|
| `main.tex` | preamble, title block, `\twocolumn` layout |
| `abstract.tex` | abstract |
| `body.tex` | all sections + bibliography |
| `figs/load_results.py` | parser: `RESULTS.md` -> records |
| `figs/make_figs.py` | figures 1–5 |
| `figs/make_tables.py` | tables 1–5 + `numbers.tex` |

## Figures

1. `fig1_faithfulness_vs_correctness` — occlusion Spearman vs GT AUROC, one point
   per ground-truth-bearing cell (the headline).
2. `fig2_heatmaps` — attributor × dataset for faithfulness and correctness.
3. `fig3_backbone_ordering` — backbone ordering on exact ground truth.
4. `fig4_task_faithfulness` — faithfulness by task family.
5. `fig5_two_regimes` — the in-distribution vs scaffold-shift selection test.

## Sign conventions (checked against the code, not assumed)

- **Occlusion Spearman**: correlation between motif attribution mass and the
  drop in the explained-class logit when that motif is occluded. **Higher =
  more faithful**; negative = ranks motifs opposite to their causal effect.
- **GT AUROC**: attribution vs the per-atom ground-truth mask. Chance = 0.5;
  **below 0.5 = anti-aligned**.
