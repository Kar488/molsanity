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
- **DILI / hERG (Therapeutics Data Commons)** are wired via PyTDC and audited
  (DILI GINE acc 0.80/AUC 0.82; hERG GCN acc 0.90/AUC 0.80). They carry **no node
  ground truth** (gt_auroc is "—"), so they extend the coherence/faithfulness/
  calibration battery to real ADMET-toxicity endpoints but not the GT-localisation
  axis — that axis stays anchored on SynthMotifs (exact) and the MUTAG proxy.
- **SubgraphX (DIG) and ShapeGGen (GraphXAI)** could not be installed in this
  environment: both depend on the pre-2.5 PyG `torch_sparse`/`torch_scatter`
  compiled extensions, for which no wheel exists at torch 2.13 (source builds
  hang). DIG installs but fails to import; GraphXAI's wheel omits its subpackages.
  Both are kept blocked-tolerant and logged, never faked — and ShapeGGen's
  exact-GT role is already met by the offline SynthMotifs generator.
- **PGExplainer is classification-only.** Its parametric mask-MLP is trained
  against class logits, so the current wrapper does not support graph-regression;
  regression cells use the gradient family + GNNExplainer (the perturbation-based
  attributor that does support regression). Regression PGExplainer is future work.

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
