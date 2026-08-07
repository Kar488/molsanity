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

.PHONY: all figures tables supplementary submission submission-files zip pdf fontcheck macrocheck clean

all: pdf

figures:
	$(PY) figs/make_figures.py

tables:
	$(PY) figs/make_tables.py

supplementary:
	$(PY) make_supplementary.py

# The plain-text abstract pasted into preprint servers and submission
# forms. Generated from abstract.tex so it cannot drift from the PDF.
submission: tables
	$(PY) make_submission_abstract.py

# The upload artefact. `zip` APPENDS to an existing archive, so a rebuilt
# bundle zipped over an old file ships both copies -- which it did: a
# submission zip went out carrying the current reports at the root and a
# stale supplementary/ folder from a previous run beside them. Remove first.
# The journal package: an editable LaTeX source archive for the manuscript
# upload (the form does not accept a PDF), plus numbered BMC additional
# files -- narrative to PDF, data to CSV, as BMC asks.
submission-files: tables figures
	$(PY) make_additional_files.py

zip: supplementary
	rm -f molsanity_supplementary.zip
	cd supplementary && zip -q -X -r ../molsanity_supplementary.zip . -x '.*'
	@$(PY) -c "import zipfile;n=zipfile.ZipFile('molsanity_supplementary.zip').namelist();\
assert not any('/' in x for x in n), 'nested paths in the bundle: %s' % n;\
print('  molsanity_supplementary.zip: %d files, flat' % len(n))"

pdf: figures tables supplementary submission
	$(XELATEX) -interaction=nonstopmode main.tex
	$(XELATEX) -interaction=nonstopmode main.tex
	$(PY) figs/check_macros.py main.log
	$(PY) figs/check_fonts.py main.pdf

# Which macros the prose quotes that the current results do not support.
# Runs against main.log, so build first.
macrocheck:
	$(PY) figs/check_macros.py main.log

# arXiv rejects Type 3 and non-embedded fonts; run this before uploading.
fontcheck:
	$(PY) figs/check_fonts.py main.pdf

clean:
	rm -f main.aux main.log main.out main.toc main.pdf
