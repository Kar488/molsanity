# LIMITATIONS.md — MolSanity

Honest, running list of caveats, scope limits, and known weaknesses. Kept
current alongside RESULTS.md.

## Scope

- **CPU-only development environment.** All defaults are CPU-tractable. The
  overnight full matrix assumes a single modern GPU; without one, use `--budget`
  to run a reduced-but-honest subset (clearly labelled in reports).
- **MUTAG "ground truth" is quasi-ground-truth.** MUTAG has no per-atom
  explanation labels shipped with the PyG `TUDataset`. We derive a chemically
  motivated proxy mask (nitro / aromatic-nitro groups, the canonical
  mutagenicity motifs from Debnath et al. 1991) via RDKit SMARTS. This is a
  motif-level proxy, not annotator ground truth; it is labelled as such wherever
  used. Exact ground truth is provided by the synthetic Tier-1 sets
  (BA-2Motifs, BA-Shapes, ShapeGGen).

## Data

- **SynthMotifs** provides *exact* node ground truth but is a **structural,
  non-molecular** synthetic task (BA base + house/cycle motif); it validates the
  audit machinery, not chemical generalisation. Molecular ground truth remains
  the MUTAG nitro *proxy* until BA-2Motifs/ShapeGGen are reachable.
- ShapeGGen (GraphXAI) is an optional heavy dependency; if unavailable it is
  skipped and logged, never faked.
- TDC (Tier-3) datasets are wired in a later milestone.

## Tier-2 classification under reduced-budget scaffold split

- **Degenerate models on imbalanced classification (BBBP, BACE).** Under the
  reduced `matrix.yaml` budget (30 epochs, hidden 32), Bemis–Murcko scaffold
  splits on the class-imbalanced BBBP/BACE produce near-single-class test folds,
  and the model collapses to a majority-class predictor (test accuracy ≈ 1.0 but
  ROC-AUC undefined). The audit still *runs*, but attributions of a constant
  predictor are not scientifically meaningful, so these cells are **not featured**
  (one BBBP·GINE cell is retained as a documented example). Meaningful Tier-2
  classification needs the overnight `full.yaml` budget **and** a class-aware
  scaffold split — tracked in `TASKS.md`. The meaningful Tier-2 results at this
  budget are the **regression** tasks (ESOL/FreeSolv/Lipophilicity), where models
  reach honest R² (e.g. ESOL ≈ 0.67–0.69 across backbones).

## Methods

- The first slice audits a single attributor (Integrated Gradients). Additional
  attributors and backbones broaden the matrix in later milestones; absence of a
  cell in RESULTS.md means it has not been validated, not that it failed.
