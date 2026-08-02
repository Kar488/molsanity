# Third-party licences

MolSanity is MIT (see `LICENSE`). It wraps canonical implementations rather
than reimplementing them, which is a deliberate scientific choice — the audit
measures the attributors the field actually uses, not our versions of them —
but it means the licences below govern what you may do with a MolSanity
installation, not just the MIT terms.

## Runtime dependencies

| Package | Licence | Required? |
|---|---|---|
| PyTorch | BSD-3-Clause | yes |
| PyTorch Geometric | MIT | yes |
| RDKit | BSD-3-Clause | yes |
| Captum | BSD-3-Clause | yes |
| NumPy | BSD-3-Clause | yes |
| SciPy | BSD-3-Clause | yes |
| scikit-learn | BSD-3-Clause | yes |
| matplotlib | PSF-based (matplotlib licence) | yes |
| PyYAML | MIT | yes |
| **DIG (`dive-into-graphs`)** | **GPL-3.0** | **no — SubgraphX only** |
| GraphXAI | MIT | no — ShapeGGen only |
| PyTDC | MIT | no — DILI/hERG only |

Every required dependency is permissive (BSD/MIT/PSF), so an MIT licence on
MolSanity's own code is consistent.

## The one that needs care: DIG is GPL-3.0

`SubgraphX` is wrapped from DIG, which is GPL-3.0. Three things follow, and the
project is arranged so that they stay manageable:

1. **No GPL code is vendored here.** `molsanity/attributors/subgraphx.py`
   imports DIG at runtime; it contains none of DIG's source. This repository is
   therefore distributable under MIT.
2. **SubgraphX is optional and the framework degrades cleanly without it.**
   `pip install -e .` does not pull DIG. If DIG is absent, SubgraphX cells are
   skipped and logged and every other cell runs unchanged. A user who never
   installs DIG never comes near GPL terms.
3. **If you install DIG, the combined installation is subject to GPL-3.0**, and
   redistributing that combination means complying with it. That is a
   consequence of DIG's licence, not of anything MolSanity does, and it is the
   same position anyone using SubgraphX is in.

The practical reading: use and modify MolSanity under MIT; if you redistribute
an environment that bundles DIG, the GPL applies to that distribution.

## Datasets

Datasets are **not** redistributed by this repository. They are downloaded at
run time from their sources, and each carries its own terms, recorded in
`molsanity/data/manifest.py` alongside the loader and checksum. MUTAG and
BA-2Motifs come via PyTorch Geometric; the MoleculeNet sets (BBBP, BACE, ESOL,
FreeSolv, Lipophilicity, ClinTox, SIDER, Tox21) are widely redistributed under
permissive terms; DILI and hERG come via PyTDC. SynthMotifs and MolMotif are
generated locally by this codebase and are covered by the MIT licence above.

Where a dataset is gated, the pipeline logs it as blocked and continues rather
than attempting to work around the credentialing.
