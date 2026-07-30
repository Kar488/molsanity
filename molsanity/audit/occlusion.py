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


def _batched_masked_logits(model, data, masks: np.ndarray,
                           baseline=None) -> np.ndarray:
    """Run the model once per mask, batched. masks: [M, num_nodes] in {0,1} kept.

    ``baseline`` selects the counterfactual used for a removed node. ``None``
    zeroes its features, which is the field convention and what the multiplier
    ``node_mask`` implements. A tensor of shape [F] instead *replaces* a removed
    node's features with that vector, which keeps the graph closer to the data
    manifold: the node still looks like a plausible atom, just an uninformative
    one. Comparing the two answers how much of a faithfulness score is an
    artefact of evaluating the model off-distribution.

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
        if baseline is None:
            out = model(X, EI, EA, B, node_mask=node_mask)
        else:
            # Impute rather than zero: x <- keep * x + (1 - keep) * baseline.
            bl = baseline.to(device=X.device, dtype=X.dtype).view(1, -1)
            X_imp = node_mask * X + (1.0 - node_mask) * bl
            out = model(X_imp, EI, EA, B)
    return out.detach().cpu().numpy()


def occlusion_faithfulness(
    model,
    data,
    node_attr: np.ndarray,
    decomp: MotifDecomposition,
    target: int,
    salient_quantile: float = 0.8,
    task: str = "graph-classification",
    baseline=None,
) -> dict:
    """``baseline``: optional [F] feature vector used in place of zeroing when a
    node is removed. Supplying the training-set feature mean gives a
    counterfactual that stays nearer the data manifold; the caller can then
    compare the two and see how much of the score is an off-manifold artefact.
    """
    from scipy.stats import spearmanr

    n = data.num_nodes
    motifs = decomp.motifs
    if not motifs:
        return {"spearman": float("nan"), "top1_agreement": float("nan"),
                "fidelity_plus": float("nan"), "fidelity_minus": float("nan"),
                "fidelity_ratio": float("nan"), "sparsity": float("nan"),
                "characterization": float("nan"), "n_motifs": 0}

    # Baseline (all kept) + one mask per motif (that motif's atoms removed).
    base_mask = np.ones((1, n), dtype=np.float32)
    motif_masks = np.ones((len(motifs), n), dtype=np.float32)
    for i, atoms in enumerate(motifs):
        motif_masks[i, atoms] = 0.0

    is_reg = task == "graph-regression"

    # Which atoms count as "important" according to the attributor.
    #
    # Classification: the attribution is taken w.r.t. the predicted class, so a
    # positive value means "pushes towards this class" and the positive part is
    # the quantity of interest. Clipping at zero is the field convention.
    #
    # Regression: the output is a signed, unbounded scalar. An atom that drives
    # the prediction strongly *down* is exactly as causally important as one
    # that drives it up, but clipping at zero scores it as unimportant, so the
    # attribution ranking and the occlusion ranking are then compared on
    # different quantities. Rank by magnitude instead.
    a = np.abs(node_attr) if is_reg else np.clip(node_attr, 0, None)
    thr = np.quantile(a, salient_quantile) if a.max() > 0 else np.inf
    salient = a >= thr if a.max() > 0 else np.zeros(n, dtype=bool)
    rm_salient = np.ones((1, n), dtype=np.float32); rm_salient[0, salient] = 0.0
    rm_nonsalient = np.ones((1, n), dtype=np.float32); rm_nonsalient[0, ~salient] = 0.0

    all_masks = np.concatenate([base_mask, motif_masks, rm_salient, rm_nonsalient], axis=0)
    logits = _batched_masked_logits(model, data, all_masks, baseline=baseline)

    from ..models.calibration import softmax_1d

    if is_reg:
        # Regression: work directly in output space; a softmax over a single
        # scalar is meaningless. The head is trained on targets standardised on
        # the train split, so this raw output is in units of the training
        # target's standard deviation, and a "fidelity" here is a shift in
        # sigma, not a probability.
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

    occ_delta = base_logit - motif_logits  # target shift when the motif is removed
    ig_motif = motif_scores(a, decomp, reduce="sum")

    # Match the occlusion side to the attribution side. Under classification a
    # signed drop in the target-class logit is the effect of interest. Under
    # regression the prediction can move either way and the attribution is
    # ranked by magnitude, so the occlusion effect is a magnitude too.
    occ_effect = np.abs(occ_delta) if is_reg else occ_delta

    if len(motifs) >= 2 and np.std(occ_effect) > 0 and np.std(ig_motif) > 0:
        rho = float(spearmanr(ig_motif, occ_effect).correlation)
    else:
        rho = float("nan")

    top1_ig = int(np.argmax(ig_motif))
    top1_occ = int(np.argmax(occ_effect))
    top1_agree = float(top1_ig == top1_occ)

    # Field-standard fidelity in probability space (Yuan et al. 2022):
    #   Fidelity+ : prob drop when SALIENT atoms are removed (higher = faithful)
    #   Fidelity- : prob drop when NON-salient atoms are removed (lower = faithful)
    fid_plus = float(p_base - p_rm_salient)
    fid_minus = float(p_base - p_rm_nonsalient)
    sparsity = float(1.0 - salient.mean())

    # A bounded, scale-free companion that is defined for both tasks: of the
    # total movement the two complementary occlusions produce, what share comes
    # from removing the salient atoms? 0.5 means the attributor's atoms are no
    # more causally influential than the rest; 1 means they carry all of it.
    # This is what makes the regression cells comparable to each other and to
    # the classification ones, since the raw regression shift is in sigma and
    # unbounded.
    d_sal, d_non = abs(fid_plus), abs(fid_minus)
    fid_ratio = float(d_sal / (d_sal + d_non)) if (d_sal + d_non) > 0 else float("nan")

    # The GraphFramEx characterisation score is defined on probability-space
    # fidelities in [0,1]. Clipping a sigma-space shift into that range would
    # manufacture a number that looks comparable and is not, so regression
    # reports it as undefined.
    char = float("nan") if is_reg else characterization_score(fid_plus, fid_minus)

    return {
        "spearman": rho,
        "top1_agreement": top1_agree,
        "fidelity_plus": fid_plus,
        "fidelity_minus": fid_minus,
        "fidelity_ratio": fid_ratio,
        "sparsity": sparsity,
        "characterization": char,
        "n_motifs": len(motifs),
    }


def dataset_feature_mean(dataset, indices=None, max_graphs: int = 500):
    """Mean node-feature vector over the training graphs, as an occlusion
    baseline that keeps a removed node looking like a plausible node.

    Computed on the training split only, so the counterfactual carries no
    information from the molecules being audited.
    """
    idx = list(indices) if indices is not None else list(range(len(dataset)))
    idx = idx[:max_graphs]
    total, count = None, 0
    for i in idx:
        x = dataset[i].x
        if x is None:
            continue
        x = x.float()
        total = x.sum(0) if total is None else total + x.sum(0)
        count += int(x.size(0))
    if total is None or count == 0:
        return None
    return total / count


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
