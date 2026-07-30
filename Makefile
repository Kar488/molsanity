.PHONY: install install-graph test smoke all clean lint paper

PY ?= python

install:
	pip install -e ".[dev]"

install-graph:
	pip install torch --index-url https://download.pytorch.org/whl/cpu
	pip install -e ".[dev]"
	pip install torch-geometric captum rdkit

test:
	pytest -q

smoke:
	$(PY) -m molsanity.run_all --config configs/smoke.yaml

all:
	$(PY) -m molsanity.run_all --config configs/full.yaml

paper:
	$(MAKE) -C paper

lint:
	ruff check molsanity tests || true

clean:
	rm -rf artifacts/* logs/* .pytest_cache
