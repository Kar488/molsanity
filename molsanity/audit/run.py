"""Per-cell audit: compute per-molecule audit records for one
(dataset x backbone x attributor) cell, then aggregate.

A "cell" here is fixed dataset + trained model + attributor. For each molecule
in the evaluation set we compute the ground-truth, coherence, and occlusion
metrics and store one record. Aggregation applies paired statistics.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

import numpy as np

from ..data.chem import mol_from_data
from ..data.groundtruth import ground_truth_mask, has_ground_truth
from ..utils import get_logger
from .coherence import coherence_battery
from .groundtruth import attribution_gt_scores
from .motifs import decompose
from .occlusion import occlusion_faithfulness
from .stats import summarise

log = get_logger()


@dataclass
class MoleculeAuditRecord:
    graph_id: int
    label: int
    pred: int
    correct: int
    target: int
    gt_auroc: float = float("nan")
    gt_auprc: float = float("nan")
    atom_gini: float = float("nan")
    top20_mass: float = float("nan")
    salient_cc_frac: float = float("nan")
    motif_top1_share: float = float("nan")
    occ_spearman: float = float("nan")
    occ_top1_agreement: float = float("nan")
    fidelity_plus: float = float("nan")
    fidelity_minus: float = float("nan")
    sparsity: float = float("nan")
    n_motifs: int = 0
    n_atoms: int = 0
    confidence: float = float("nan")
    regime: str = "unknown"
    stability: float = float("nan")


def audit_molecule(model, data, attribution, dataset_name: str,
                   temperature: float = 1.0, tau: float = 0.8) -> MoleculeAuditRecord:
    import torch

    from .regime import assign_regime, confidence_from_logits

    node_attr = attribution.node_attr
    target = attribution.target
    pred = attribution.meta.get("pred", target)
    label = int(data.y.view(-1)[0]) if hasattr(data, "y") else -1

    mol, _ = mol_from_data(data)
    decomp = decompose(data, mol=mol)
    edge_index = data.edge_index.cpu().numpy()

    # Calibrated confidence + regime.
    device = next(model.parameters()).device
    model.eval()
    with torch.no_grad():
        batch = torch.zeros(data.num_nodes, dtype=torch.long, device=device)
        logits = model(data.x.to(device), data.edge_index.to(device),
                       data.edge_attr.to(device) if data.edge_attr is not None else None,
                       batch).cpu().numpy()[0]
    _, confidence = confidence_from_logits(logits, temperature)

    rec = MoleculeAuditRecord(
        graph_id=attribution.graph_id,
        label=label,
        pred=int(pred),
        correct=int(pred == label),
        target=int(target),
        n_atoms=int(data.num_nodes),
        confidence=confidence,
        regime=assign_regime(confidence, int(pred == label), tau=tau),
    )

    coh = coherence_battery(node_attr, edge_index, decomp)
    rec.atom_gini = coh["atom_gini"]
    rec.top20_mass = coh["top20_mass"]
    rec.salient_cc_frac = coh["salient_cc_frac"]
    rec.motif_top1_share = coh["motif_top1_share"]

    occ = occlusion_faithfulness(model, data, node_attr, decomp, target=int(target))
    rec.occ_spearman = occ["spearman"]
    rec.occ_top1_agreement = occ["top1_agreement"]
    rec.fidelity_plus = occ["fidelity_plus"]
    rec.fidelity_minus = occ["fidelity_minus"]
    rec.sparsity = occ["sparsity"]
    rec.n_motifs = occ["n_motifs"]

    if has_ground_truth(dataset_name):
        gt = ground_truth_mask(dataset_name, data)
        if gt is not None:
            gs = attribution_gt_scores(node_attr, gt)
            rec.gt_auroc = gs["auroc"]
            rec.gt_auprc = gs["auprc"]

    return rec


def aggregate_records(records: list[MoleculeAuditRecord], seed: int = 0) -> dict:
    """Aggregate per-molecule records with paired/bootstrap statistics."""
    def col(name):
        return np.array([getattr(r, name) for r in records], dtype=np.float64)

    from .regime import calibration_linkage, stratify_by_regime

    metrics = [
        "gt_auroc", "gt_auprc", "atom_gini", "top20_mass", "salient_cc_frac",
        "motif_top1_share", "occ_spearman", "occ_top1_agreement",
        "fidelity_plus", "fidelity_minus", "sparsity", "stability", "confidence",
    ]
    agg = {m: summarise(col(m), name=m, seed=seed) for m in metrics}
    agg["n_molecules"] = len(records)
    agg["accuracy"] = float(np.mean([r.correct for r in records])) if records else float("nan")

    # Regime stratification of the key reliability metrics.
    agg["regime_counts"] = {
        r: sum(1 for rec in records if rec.regime == r)
        for r in ("confident_correct", "confident_error", "borderline")
    }
    agg["regime_stratified"] = {
        m: stratify_by_regime(records, m)
        for m in ("gt_auroc", "occ_spearman", "stability")
    }
    # Calibration linkage (confidence-calibration vs attribution reliability).
    agg["calibration_linkage"] = {
        m: calibration_linkage(records, reliability_metric=m)
        for m in ("occ_spearman", "gt_auroc")
    }
    return agg
