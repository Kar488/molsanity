"""Uniform attribution schema.

Every attributor returns node/edge attributions in this common form so the audit
and benchmark layers are attributor-agnostic. Motif-level attributions are
derived downstream from node attributions + an RDKit motif decomposition.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class Attribution:
    """Per-molecule attribution in a common schema."""

    graph_id: int
    node_attr: np.ndarray  # shape [num_nodes], non-negative importance
    edge_attr: np.ndarray | None = None  # shape [num_edges]
    method: str = ""
    target: int | None = None  # class explained
    meta: dict = field(default_factory=dict)

    def normalised_node_attr(self) -> np.ndarray:
        """Min-max normalised node attribution in [0, 1] (for GT AUROC etc.)."""
        a = np.abs(self.node_attr).astype(np.float64)
        rng = a.max() - a.min()
        if rng <= 0:
            return np.zeros_like(a)
        return (a - a.min()) / rng
