"""molsanity.audit — the reliability audit: coherence, faithfulness, GT, stats."""
from .coherence import coherence_battery, gini, salient_cc_fraction, top_k_mass
from .groundtruth import attribution_gt_scores
from .motifs import MotifDecomposition, decompose, motif_scores, primary_motif_share
from .occlusion import occlusion_faithfulness
from .regime import (
    assign_regime,
    calibration_linkage,
    confidence_from_logits,
    stratify_by_regime,
)
from .run import MoleculeAuditRecord, aggregate_records, audit_molecule
from .stability import cross_checkpoint_stability
from .stats import bootstrap_ci, paired_wilcoxon, summarise, wilcoxon_vs_zero

__all__ = [
    "coherence_battery", "gini", "top_k_mass", "salient_cc_fraction",
    "attribution_gt_scores",
    "MotifDecomposition", "decompose", "motif_scores", "primary_motif_share",
    "occlusion_faithfulness",
    "assign_regime", "confidence_from_logits", "stratify_by_regime",
    "calibration_linkage",
    "cross_checkpoint_stability",
    "MoleculeAuditRecord", "audit_molecule", "aggregate_records",
    "bootstrap_ci", "paired_wilcoxon", "summarise", "wilcoxon_vs_zero",
]
