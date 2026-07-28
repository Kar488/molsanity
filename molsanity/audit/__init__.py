"""molsanity.audit — the reliability audit: coherence, faithfulness, GT, stats."""
from .coherence import coherence_battery, gini, salient_cc_fraction, top_k_mass
from .groundtruth import attribution_gt_scores
from .motifs import MotifDecomposition, decompose, motif_scores, primary_motif_share
from .occlusion import occlusion_faithfulness
from .run import MoleculeAuditRecord, aggregate_records, audit_molecule
from .stats import bootstrap_ci, paired_wilcoxon, summarise, wilcoxon_vs_zero

__all__ = [
    "coherence_battery", "gini", "top_k_mass", "salient_cc_fraction",
    "attribution_gt_scores",
    "MotifDecomposition", "decompose", "motif_scores", "primary_motif_share",
    "occlusion_faithfulness",
    "MoleculeAuditRecord", "audit_molecule", "aggregate_records",
    "bootstrap_ci", "paired_wilcoxon", "summarise", "wilcoxon_vs_zero",
]
