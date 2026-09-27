"""molsanity.audit — the reliability audit: coherence, faithfulness, GT, stats."""
from .coherence import coherence_battery, gini, salient_cc_fraction, top_k_mass
from .groundtruth import attribution_gt_scores
from .motifs import MotifDecomposition, decompose, motif_scores, primary_motif_share
from .regime import (
    assign_regime,
    calibration_linkage,
    confidence_from_logits,
    stratify_by_regime,
)
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

# The two torch-backed submodules are imported on first use, not at package
# import. paper/figs/make_figures.py imports molsanity.audit.abstention, which
# runs this __init__; while these were eager that pulled in torch. The paper
# rebuild job deliberately installs no deep-learning stack -- the claim it
# checks is that the manuscript regenerates from committed results without
# retraining anything -- so the figure build died on ModuleNotFoundError and
# the job that verifies reproducibility was red. PEP 562 defers the cost to
# the first caller that actually wants one of these names.
_LAZY = {
    "occlusion_faithfulness": ".occlusion",
    "MoleculeAuditRecord": ".run",
    "aggregate_records": ".run",
    "audit_molecule": ".run",
}


def __getattr__(name):
    mod = _LAZY.get(name)
    if mod is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from importlib import import_module
    return getattr(import_module(mod, __name__), name)


def __dir__():
    return sorted(set(globals()) | set(_LAZY))