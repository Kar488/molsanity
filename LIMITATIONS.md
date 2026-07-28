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

## Methods

- The first slice audits a single attributor (Integrated Gradients). Additional
  attributors and backbones broaden the matrix in later milestones; absence of a
  cell in RESULTS.md means it has not been validated, not that it failed.
