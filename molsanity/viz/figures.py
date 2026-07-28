"""Publication-quality figures (vector PDF/SVG).

- ``ground_truth_validation_figure``: the credibility figure — per-molecule
  distribution of attribution-vs-ground-truth AUROC with the chance line, and
  faithfulness (occlusion) alongside, so one can see correctness vs faithfulness.
- ``molecule_attribution_svg``: high-resolution RDKit rendering of a molecule
  with atoms coloured by attribution and the ground-truth motif outlined.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from ..utils import get_logger

log = get_logger()


def _use_agg():
    import matplotlib

    matplotlib.use("Agg")


def _ecdf(x):
    x = np.sort(np.asarray(x, dtype=np.float64))
    x = x[np.isfinite(x)]
    y = np.arange(1, x.size + 1) / x.size
    return x, y


def ground_truth_validation_figure(records, out_path, title: str = "") -> dict:
    """Render the GT-validation figure. Returns the plotted summary values."""
    _use_agg()
    import matplotlib.pyplot as plt

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    gt = np.array([r.gt_auroc for r in records], dtype=np.float64)
    gt = gt[np.isfinite(gt)]
    occ = np.array([r.occ_spearman for r in records], dtype=np.float64)
    occ = occ[np.isfinite(occ)]

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))

    # Panel A: ECDF of GT AUROC with chance line.
    ax = axes[0]
    if gt.size:
        x, y = _ecdf(gt)
        ax.step(x, y, where="post", color="#2166ac", lw=2, label="IG vs GT AUROC")
        ax.axvline(0.5, color="grey", ls="--", lw=1, label="chance (0.5)")
        ax.axvline(gt.mean(), color="#b2182b", ls=":", lw=1.5,
                   label=f"mean={gt.mean():.2f}")
    ax.set_xlim(0, 1)
    ax.set_xlabel("Attribution–ground-truth AUROC")
    ax.set_ylabel("Cumulative fraction of molecules")
    ax.set_title("A. Ground-truth localisation")
    ax.legend(fontsize=7, loc="upper left")

    # Panel B: correctness (GT AUROC) vs faithfulness (occlusion Spearman).
    ax = axes[1]
    data = [d for d in [gt, occ] if d.size]
    labels = [lab for lab, d in zip(["GT AUROC", "Occl. Spearman"], [gt, occ]) if d.size]
    if data:
        parts = ax.violinplot(data, showmeans=True, showextrema=False)
        for pc in parts["bodies"]:
            pc.set_facecolor("#92c5de")
            pc.set_alpha(0.7)
        ax.set_xticks(range(1, len(labels) + 1))
        ax.set_xticklabels(labels, fontsize=8)
    ax.axhline(0.5, color="grey", ls="--", lw=1)
    ax.set_ylabel("Score")
    ax.set_title("B. Correctness vs faithfulness")

    if title:
        fig.suptitle(title, fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.95) if title else None)

    pdf = out_path.with_suffix(".pdf")
    svg = out_path.with_suffix(".svg")
    fig.savefig(pdf, bbox_inches="tight")
    fig.savefig(svg, bbox_inches="tight")
    plt.close(fig)
    log.info("Wrote GT-validation figure: %s (+ .svg)", pdf)

    return {
        "gt_auroc_mean": float(gt.mean()) if gt.size else float("nan"),
        "gt_auroc_n": int(gt.size),
        "occ_spearman_mean": float(occ.mean()) if occ.size else float("nan"),
        "pdf": str(pdf), "svg": str(svg),
    }


def molecule_attribution_svg(
    data, node_attr, out_path, gt_mask=None, size=(500, 500)
) -> str | None:
    """High-res RDKit SVG: atoms coloured by attribution, GT motif circled."""
    from rdkit.Chem.Draw import rdMolDraw2D

    from ..data.chem import graph_to_mol

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    mol, _ = graph_to_mol(data)
    a = np.abs(np.asarray(node_attr, dtype=np.float64))
    rng = a.max() - a.min()
    norm = (a - a.min()) / rng if rng > 0 else np.zeros_like(a)

    highlight_atoms = list(range(mol.GetNumAtoms()))
    atom_colors = {}
    for i in range(mol.GetNumAtoms()):
        v = float(norm[i]) if i < norm.size else 0.0
        # White -> red ramp for importance.
        atom_colors[i] = (1.0, 1.0 - 0.85 * v, 1.0 - 0.85 * v)

    gt_atoms = []
    if gt_mask is not None:
        gt_atoms = [i for i in range(min(len(gt_mask), mol.GetNumAtoms())) if gt_mask[i] > 0]

    drawer = rdMolDraw2D.MolDraw2DSVG(size[0], size[1])
    opts = drawer.drawOptions()
    opts.addAtomIndices = False
    opts.bondLineWidth = 2
    try:
        rdMolDraw2D.PrepareAndDrawMolecule(
            drawer, mol,
            highlightAtoms=highlight_atoms,
            highlightAtomColors=atom_colors,
            highlightBonds=[],
        )
    except Exception as exc:
        log.warning("RDKit draw failed: %s", exc)
        return None
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()
    out_path.write_text(svg)
    log.info("Wrote molecule attribution SVG: %s (GT atoms: %s)", out_path, gt_atoms)
    return str(out_path)
