"""Signature figure: an attributor × molecule grid of RDKit attribution maps.

Each cell renders a molecule with atoms shaded by attribution intensity
(sequential ramp) and the ground-truth motif outlined in green — so the reader
sees, at a glance, which methods land on the true motif and which do not
(the "faithful-but-wrong" and "ranking-flip" findings). Column titles are the
attributor names in their fixed entity colours.

Rendering: RDKit MolDraw2DCairo → PNG → composed into a matplotlib grid, with a
shared attribution colourbar and a green ground-truth-motif key.
"""
from __future__ import annotations

import io
from pathlib import Path

import numpy as np

from ..utils import get_logger
from .style import GT_GREEN, apply_style, attributor_color, save_vector, short

log = get_logger()


def _render_cell_png(mol, node_attr, gt_mask, size=(260, 220)):
    """RDKit PNG: atom fill = attribution intensity, GT motif bonds = green."""
    from matplotlib import colormaps
    from rdkit.Chem.Draw import rdMolDraw2D

    n = mol.GetNumAtoms()
    a = np.abs(np.asarray(node_attr, dtype=np.float64))[:n]
    rng = a.max() - a.min()
    norm = (a - a.min()) / rng if rng > 0 else np.zeros_like(a)

    ramp = colormaps["YlOrRd"]
    atom_colors = {i: tuple(ramp(0.15 + 0.85 * float(norm[i]))[:3]) for i in range(n)}
    highlight_atoms = list(range(n))

    # Ground-truth motif: outline its internal bonds in green.
    gt_atoms = set(int(i) for i in np.where(np.asarray(gt_mask) > 0)[0]) if gt_mask is not None else set()
    gt_bonds, bond_colors = [], {}
    for b in mol.GetBonds():
        i, j = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
        if i in gt_atoms and j in gt_atoms:
            gt_bonds.append(b.GetIdx())
            bond_colors[b.GetIdx()] = _hex_to_rgb(GT_GREEN)

    drawer = rdMolDraw2D.MolDraw2DCairo(size[0], size[1])
    opts = drawer.drawOptions()
    opts.bondLineWidth = 2
    opts.highlightBondWidthMultiplier = 3
    opts.clearBackground = True
    try:
        rdMolDraw2D.PrepareAndDrawMolecule(
            drawer, mol,
            highlightAtoms=highlight_atoms, highlightAtomColors=atom_colors,
            highlightBonds=gt_bonds, highlightBondColors=bond_colors,
        )
    except Exception as exc:
        log.warning("cell render failed: %s", exc)
        return None
    drawer.FinishDrawing()
    return drawer.GetDrawingText()


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _render_graph_cell(ax, data, node_attr, gt_mask):
    """Node-link rendering for non-molecular graphs: node fill = attribution,
    ground-truth motif nodes ringed in green. Deterministic layout."""
    import networkx as nx
    from matplotlib import colormaps

    n = int(data.num_nodes)
    ei = data.edge_index.cpu().numpy()
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(zip(ei[0].tolist(), ei[1].tolist()))
    pos = nx.spring_layout(G, seed=0, k=0.5)

    a = np.abs(np.asarray(node_attr, dtype=np.float64))[:n]
    rng = a.max() - a.min()
    norm = (a - a.min()) / rng if rng > 0 else np.zeros_like(a)
    ramp = colormaps["YlOrRd"]
    node_colors = [ramp(0.15 + 0.85 * float(norm[i])) for i in range(n)]
    gt = set(int(i) for i in np.where(np.asarray(gt_mask) > 0)[0]) if gt_mask is not None else set()
    edgecolors = [GT_GREEN if i in gt else "#3a3a38" for i in range(n)]
    lw = [2.2 if i in gt else 0.5 for i in range(n)]

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#b8b8b4", width=1.0)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=70,
                           edgecolors=edgecolors, linewidths=lw)
    ax.set_axis_off()


def attribution_grid(
    mols, node_attrs_by_method, gt_masks, method_names, row_labels, out_path,
    title="", dataset="", size=(260, 220), graphs=None,
):
    """Grid: rows = molecules/graphs, columns = attribution methods.

    Molecular rows (``mols[r]`` is an RDKit mol) render as skeletal structures;
    non-molecular rows (``mols[r]`` is None) render as node-link graphs from
    ``graphs[r]``. ``node_attrs_by_method[method][row]`` is the attribution vector.
    """
    apply_style()
    import matplotlib.pyplot as plt
    from matplotlib import colormaps
    from matplotlib.cm import ScalarMappable
    from matplotlib.colors import Normalize
    from matplotlib.lines import Line2D
    from PIL import Image

    n_rows, n_cols = len(mols), len(method_names)
    fig, axes = plt.subplots(
        n_rows, n_cols, figsize=(2.15 * n_cols, 1.95 * n_rows + 0.5),
        squeeze=False,
    )
    for r in range(n_rows):
        for c, method in enumerate(method_names):
            ax = axes[r][c]
            ax.set_axis_off()
            attr_r = node_attrs_by_method[method][r]
            if mols[r] is not None:
                png = _render_cell_png(mols[r], attr_r, gt_masks[r], size=size)
                if png:
                    ax.imshow(Image.open(io.BytesIO(png)))
            elif graphs is not None:
                _render_graph_cell(ax, graphs[r], attr_r, gt_masks[r])
            if r == 0:
                ax.set_title(short(method), color=attributor_color(method),
                             fontsize=11, fontweight="bold", pad=6)
            if c == 0:
                ax.text(-0.06, 0.5, row_labels[r], transform=ax.transAxes,
                        rotation=90, va="center", ha="right", fontsize=9,
                        color="#3a3a38")

    # Shared attribution colourbar + ground-truth key.
    sm = ScalarMappable(norm=Normalize(0, 1), cmap=colormaps["YlOrRd"])
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=axes.ravel().tolist(), fraction=0.02, pad=0.02)
    cbar.set_label("attribution intensity (normalised)", fontsize=8)
    cbar.ax.tick_params(labelsize=7)
    fig.legend(
        handles=[Line2D([0], [0], color=GT_GREEN, lw=3, label="ground-truth motif")],
        loc="lower center", ncol=1, fontsize=8, bbox_to_anchor=(0.5, -0.02),
    )
    if title:
        fig.suptitle(title, fontsize=12, fontweight="bold", y=1.0)
    return save_vector(fig, Path(out_path))


def make_case_study_grid(
    dataset_name, backbone, attributor_names, out_path,
    n_molecules=4, split_kind="scaffold", budget=None, seed=0,
    hidden=32, layers=3, epochs=30,
):
    """Train/load a model, compute attributions for a few molecules, render grid."""
    from .. import data as dataio
    from ..attributors import build_attributor
    from ..data.chem import mol_from_data
    from ..models import train_model

    budget = budget or {}
    loaded = dataio.load_dataset(dataset_name)
    dataset = loaded.dataset
    task = loaded.spec.task
    n_out = 1 if task == "graph-regression" else 2
    split = dataio.make_split(dataset, kind=split_kind, seed=seed)
    model, res = train_model(
        dataset, split,
        {"hidden_channels": hidden, "num_layers": layers, "task": task, "out_channels": n_out},
        {"epochs": epochs}, ckpt_dir=Path("artifacts/checkpoints") / dataset_name,
        seed=seed, backbone=backbone,
    )

    # Pick case-study molecules: prefer ones with a ground-truth motif present.
    idx = []
    for i in list(split.test):
        gt = dataio.ground_truth_mask(dataset_name, dataset[i])
        if gt is not None and 0 < gt.sum() < len(gt):
            idx.append(i)
        if len(idx) >= n_molecules:
            break
    if len(idx) < n_molecules:
        idx = list(split.test)[:n_molecules]

    mols, graphs, gt_masks, row_labels = [], [], [], []
    for i in idx:
        g = dataset[i]
        mol, _ = mol_from_data(g)
        mols.append(mol)
        graphs.append(g)
        gt_masks.append(dataio.ground_truth_mask(dataset_name, g))
        row_labels.append(f"graph {i}" if mol is None else f"mol {i}")

    node_attrs = {m: [] for m in attributor_names}
    for m in attributor_names:
        attr = build_attributor(m, model, task=task, ig_steps=budget.get("ig_steps", 25))
        for i in idx:
            g = dataset[i]
            g.graph_id = i
            node_attrs[m].append(attr.attribute(g).node_attr)

    return attribution_grid(
        mols, node_attrs, gt_masks, attributor_names, row_labels, out_path,
        title=f"{dataset_name} · {backbone}: attribution vs ground-truth motif",
        dataset=dataset_name, graphs=graphs,
    )
