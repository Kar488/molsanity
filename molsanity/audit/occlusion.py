"""Occlusion-attribution faithfulness.

For each motif we mask its atoms (zero the input node features via the model's
``node_mask`` multiplier) and measure the drop in the explained-class logit
(Delta logit). A faithful attribution ranks motifs the same way occlusion does.

Per molecule we report:
  - spearman:        Spearman(IG motif score, occlusion Delta) across motifs
  - top1_agreement:  does the top-IG motif == top-occlusion motif (0/1)
  - fidelity_plus:   drop in predicted-class prob when the *salient* atoms are
                     removed (higher = more faithful)
  - fidelity_minus:  drop when the *non-salient* atoms are removed
                     (lower = more faithful)
  - sparsity:        1 - (fraction of atoms deemed salient)

Occlusion is batched over motifs in a single forward pass (no per-atom Python
loop in the inner path).
"""
from __future__ import annotations

import numpy as np
import torch

from .motifs import MotifDecomposition, motif_scores


def _batched_masked_logits(model, data, masks: np.ndarray) -> np.ndarray:
    """Run the model once per mask, batched. masks: [M, num_nodes] in {0,1} kept.

    Returns the full logit matrix [M, num_classes] for the M masked variants.
    """
    device = next(model.parameters()).device
    n = data.num_nodes
    m = masks.shape[0]

    x = data.x.to(device)
    ei = data.edge_index.to(device)
    ea = data.edge_attr.to(device) if data.edge_attr is not None else None

    # Replicate the graph M times into one big batch.
    xs, eis, eas, batch = [], [], [], []
    for j in range(m):
        xs.append(x)
        eis.append(ei + j * n)
        if ea is not None:
            eas.append(ea)
        batch.append(torch.full((n,), j, dtype=torch.long, device=device))
    X = torch.cat(xs, 0)
    EI = torch.cat(eis, 1)
    EA = torch.cat(eas, 0) if ea is not None else None
    B = torch.cat(batch, 0)
    node_mask = torch.tensor(masks.reshape(-1, 1), dtype=X.dtype, device=device)

    model.eval()
    with torch.no_grad():
        out = model(X, EI, EA, B, node_mask=node_mask)
    return out.detach().cpu().numpy()


def occlusion_faithfulness(
    model,
    data,
    node_attr: np.ndarray,
    decomp: MotifDecomposition,
    target: int,
    salient_quantile: float = 0.8,
    task: str = "graph-classification",
) -> dict:
    from scipy.stats import spearmanr

    n = data.num_nodes
    motifs = decomp.motifs
    if not motifs:
        return {"spearman": float("nan"), "top1_agreement": float("nan"),
                "fidelity_plus": float("nan"), "fidelity_minus": float("nan"),
                "sparsity": float("nan"), "n_motifs": 0}

    # Baseline (all kept) + one mask per motif (that motif's atoms removed).
    base_mask = np.ones((1, n), dtype=np.float32)
    motif_masks = np.ones((len(motifs), n), dtype=np.float32)
    for i, atoms in enumerate(motifs):
        motif_masks[i, atoms] = 0.0

    # Fidelity masks: remove salient / remove non-salient.
    a = np.clip(node_attr, 0, None)
    thr = np.quantile(a, salient_quantile) if a.max() > 0 else np.inf
    salient = a >= thr if a.max() > 0 else np.zeros(n, dtype=bool)
    rm_salient = np.ones((1, n), dtype=np.float32); rm_salient[0, salient] = 0.0
    rm_nonsalient = np.ones((1, n), dtype=np.float32); rm_nonsalient[0, ~salient] = 0.0

    all_masks = np.concatenate([base_mask, motif_masks, rm_salient, rm_nonsalient], axis=0)
    logits = _batched_masked_logits(model, data, all_masks)  # [M, C]

    from ..models.calibration import softmax_1d

    if task == "graph-regression":
        # Regression: work directly in (standardised) output space — softmax over
        # a single scalar output is meaningless. "Fidelity" = predicted-value shift.
        def target_prob(row):
            return float(row[target])
    else:
        def target_prob(row):
            return float(softmax_1d(row)[target])

    base_logit = logits[0, target]
    motif_logits = logits[1 : 1 + len(motifs), target]
    p_base = target_prob(logits[0])
    p_rm_salient = target_prob(logits[1 + len(motifs)])
    p_rm_nonsalient = target_prob(logits[2 + len(motifs)])

    occ_delta = base_logit - motif_logits  # target-logit drop when motif removed
    ig_motif = motif_scores(a, decomp, reduce="sum")

    if len(motifs) >= 2 and np.std(occ_delta) > 0 and np.std(ig_motif) > 0:
        rho = float(spearmanr(ig_motif, occ_delta).correlation)
    else:
        rho = float("nan")

    top1_ig = int(np.argmax(ig_motif))
    top1_occ = int(np.argmax(occ_delta))
    top1_agree = float(top1_ig == top1_occ)

    # Field-standard fidelity in probability space (Yuan et al. 2022):
    #   Fidelity+ : prob drop when SALIENT atoms are removed (higher = faithful)
    #   Fidelity- : prob drop when NON-salient atoms are removed (lower = faithful)
    fid_plus = float(p_base - p_rm_salient)
    fid_minus = float(p_base - p_rm_nonsalient)
    sparsity = float(1.0 - salient.mean())

    return {
        "spearman": rho,
        "top1_agreement": top1_agree,
        "fidelity_plus": fid_plus,
        "fidelity_minus": fid_minus,
        "sparsity": sparsity,
        "characterization": characterization_score(fid_plus, fid_minus),
        "n_motifs": len(motifs),
    }


def characterization_score(fid_plus: float, fid_minus: float,
                           w_plus: float = 0.5, w_minus: float = 0.5) -> float:
    """GraphFramEx characterization score (Amara et al. 2022): the weighted
    harmonic mean of Fidelity+ and (1 - Fidelity-), in [0, 1]. Higher is better.
    Reproduced here so MolSanity's audit is directly comparable to the published
    GraphFramEx framework. Undefined (NaN) outside the valid fidelity range."""
    p = float(np.clip(fid_plus, 0.0, 1.0))
    q = 1.0 - float(np.clip(fid_minus, 0.0, 1.0))
    denom = w_minus * p + w_plus * q
    if denom <= 0:
        return float("nan")
    return float((w_plus + w_minus) * p * q / denom)
