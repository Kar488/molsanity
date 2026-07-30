# Rebuild the preprint from the committed results.
#
#   make            # figures + tables + PDF
#   make figures    # vector PDF figures only
#   make tables     # LaTeX tables + inline-number macros only
#   make clean      # remove build products (not the sources)
#
# Every number, table and figure is derived from RESULTS.md, BENCHMARK.md,
# BENCHMARK_GT.json and configs/full.yaml by the scripts in figs/. Re-running
# this after more grid cells land refreshes the whole manuscript.

PY ?= python3
XELATEX ?= xelatex

.PHONY: all figures tables pdf fontcheck clean

all: pdf

figures:
	$(PY) figs/make_figures.py

tables:
	$(PY) figs/make_tables.py

pdf: figures tables
	$(XELATEX) -interaction=nonstopmode main.tex
	$(XELATEX) -interaction=nonstopmode main.tex
	$(PY) figs/check_fonts.py main.pdf

# arXiv rejects Type 3 and non-embedded fonts; run this before uploading.
fontcheck:
	$(PY) figs/check_fonts.py main.pdf

clean:
	rm -f main.aux main.log main.out main.toc main.pdf
