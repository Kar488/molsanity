"""The regression occlusion metric compares like with like.

Under classification the attribution is taken w.r.t. the predicted class, so
its positive part is the quantity of interest and a *drop* in the target logit
is the matching occlusion effect. Under regression the output is a signed,
unbounded scalar: an atom that drives the prediction down is as causally
important as one that drives it up. Clipping the attribution at zero while
correlating against a signed shift compares two different quantities, which is
what made the regression faithfulness numbers uninterpretable.

These tests pin the fix and, importantly, pin that classification is unchanged,
since every classification number in the manuscript depends on it.
"""
from __future__ import annotations

import numpy as np
import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("torch_geometric")

from molsanity.audit.motifs import MotifDecomposition  # noqa: E402
from molsanity.audit.occlusion import occlusion_faithfulness  # noqa: E402


class _AdditiveModel(torch.nn.Module):
    """Prediction = sum of per-node weights, so the causal effect of removing a
    node is exactly its weight. Ground truth for the metric is then known."""

    def __init__(self, weights, out_dim=1):
        super().__init__()
        self.w = torch.tensor(weights, dtype=torch.float32)
        self.out_dim = out_dim
        self._p = torch.nn.Parameter(torch.zeros(1))

    def forward(self, x, edge_index, edge_attr, batch, node_mask=None):
        n = self.w.numel()
        keep = torch.ones_like(x[:, :1]) if node_mask is None else node_mask
        per_graph = int(batch.max().item()) + 1
        vals = []
        for g in range(per_graph):
            sel = batch == g
            vals.append((self.w * keep[sel].view(-1)).sum())
        out = torch.stack(vals).view(-1, 1)
        if self.out_dim == 1:
            return out
        return torch.cat([-out, out], dim=1)


def _graph(n):
    from torch_geometric.data import Data

    ei = torch.tensor([[i, (i + 1) % n] for i in range(n)]).t().contiguous()
    ei = torch.cat([ei, ei.flip(0)], dim=1)
    return Data(x=torch.ones(n, 3), edge_index=ei,
                edge_attr=torch.ones(ei.size(1), 1), y=torch.tensor([0.0]),
                num_nodes=n)


def _decomp(groups, n):
    return MotifDecomposition(motifs=[list(g) for g in groups],
                              motif_types=["ring"] * len(groups),
                              num_atoms=n)


def test_regression_recovers_a_negatively_contributing_motif():
    """A motif whose atoms push the prediction *down* is causally important.

    Weights: motif 0 strongly negative, motif 1 near zero, motif 2 positive but
    weaker than motif 0. The true importance order is therefore m0 > m2 > m1,
    with distinct magnitudes so the rank correlation is unambiguous. Under the
    old signed comparison m0 ranked *last* despite being the most influential.
    """
    n = 6
    weights = [-6.0, -6.0, 0.05, 0.05, 3.0, 3.0]
    model = _AdditiveModel(weights)
    data = _graph(n)
    decomp = _decomp([[0, 1], [2, 3], [4, 5]], n)
    # A perfect attributor: magnitude tracks the true causal magnitude, sign
    # tracks the direction of influence.
    node_attr = np.array(weights, dtype=np.float32)

    out = occlusion_faithfulness(model, data, node_attr, decomp, target=0,
                                 task="graph-regression")
    assert out["spearman"] == pytest.approx(1.0), (
        "a magnitude-correct attributor must read as faithful under regression")
    assert out["top1_agreement"] == 1.0

    # An attributor that misses the dominant (negative-influence) motif and
    # points only at the weaker positive one must score strictly worse.
    partial = np.array([0.05, 0.05, 0.05, 0.05, 3.0, 3.0], dtype=np.float32)
    worse = occlusion_faithfulness(model, data, partial, decomp, target=0,
                                   task="graph-regression")
    assert worse["spearman"] < out["spearman"]


def test_regression_fidelity_ratio_is_bounded_and_ordered():
    n = 6
    weights = [-8.0, -8.0, 0.1, 0.1, 0.1, 0.1]
    model = _AdditiveModel(weights)
    data = _graph(n)
    decomp = _decomp([[0, 1], [2, 3], [4, 5]], n)
    good = np.array(weights, dtype=np.float32)
    bad = np.array([0.1, 0.1, 8.0, 8.0, 0.1, 0.1], dtype=np.float32)

    r_good = occlusion_faithfulness(model, data, good, decomp, target=0,
                                    task="graph-regression")["fidelity_ratio"]
    r_bad = occlusion_faithfulness(model, data, bad, decomp, target=0,
                                   task="graph-regression")["fidelity_ratio"]
    for r in (r_good, r_bad):
        assert 0.0 <= r <= 1.0, "fidelity_ratio must stay in [0,1]"
    assert r_good > r_bad, (
        "an attributor pointing at the causally active atoms must score higher")


def test_characterisation_is_undefined_for_regression():
    """Clipping a sigma-space shift into [0,1] would fabricate comparability."""
    n = 4
    model = _AdditiveModel([3.0, 3.0, 0.1, 0.1])
    data = _graph(n)
    decomp = _decomp([[0, 1], [2, 3]], n)
    out = occlusion_faithfulness(model, data, np.array([3.0, 3.0, 0.1, 0.1],
                                 dtype=np.float32), decomp, target=0,
                                 task="graph-regression")
    assert np.isnan(out["characterization"])


def test_classification_path_is_untouched():
    """Every classification number in the manuscript depends on this path."""
    n = 6
    weights = [4.0, 4.0, 0.05, 0.05, -4.0, -4.0]
    model = _AdditiveModel(weights, out_dim=2)
    data = _graph(n)
    decomp = _decomp([[0, 1], [2, 3], [4, 5]], n)
    node_attr = np.array(weights, dtype=np.float32)

    out = occlusion_faithfulness(model, data, node_attr, decomp, target=1,
                                 task="graph-classification")
    # Signed comparison: the positive-attribution motif is the one whose
    # removal drops the target-class probability most.
    assert out["top1_agreement"] == 1.0
    assert not np.isnan(out["characterization"])
    assert 0.0 <= out["sparsity"] <= 1.0
