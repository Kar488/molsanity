"""SubgraphX attributor, wrapping DIG's canonical implementation.

SubgraphX (Yuan et al., ICML 2021) searches *connected subgraphs* with
Monte-Carlo tree search under a Shapley-value objective, so unlike the
gradient family and unlike the soft-mask explainers it returns a discrete
subgraph rather than a per-atom score. That is the reason to include it: the
audit's perturbation-family conclusions otherwise rest on GNNExplainer alone.

We do not reimplement it. ``dig.xgraph.method.SubgraphX`` is driven directly
and its selected subgraph is converted into the per-node score vector the rest
of the audit consumes: atoms inside the chosen subgraph get 1, the rest 0. That
conversion is lossy in one direction only (a hard mask carries no ranking
within the subgraph), which the audit's rank statistics tolerate because they
handle ties, and which is stated where SubgraphX results are reported.

Two compatibility problems stand between the published DIG package and a
working cell, and both are handled in :func:`_import_subgraphx` rather than by
forking DIG.

The first is that ``dig.xgraph.method.__init__`` imports every explainer in the
package, including DeepLIFT and GradCAM, which reach into private Captum
internals (``captum.attr._utils.typing.Literal``, ``_verify_select_column``)
that were removed after Captum 0.2, and into ``torch_sparse``. DIG pins
``captum==0.2.0`` for exactly that reason. Honouring that pin is not an option
here: Captum 0.2's ``internal_batch_size`` path is itself incompatible with the
PyG ``CaptumExplainer`` this project uses for Integrated Gradients, so
installing DIG the obvious way silently breaks a different attributor. The
first real run lost all 204 Integrated Gradients cells to precisely that
downgrade. ``subgraphx.py`` and the ``shapley.py`` it depends on need neither
Captum nor ``torch_sparse``, so the package ``__init__`` is bypassed and the
submodule imported directly, leaving Captum modern.

The second is that DIG's Shapley value function iterates a
``torch_geometric.loader.DataLoader`` over subgraphs that are already on the
compute device. Where the installed Torch pins by default, that raises
``cannot pin 'torch.cuda.FloatTensor'`` on the first rollout and takes every
SubgraphX cell with it. Pinned memory is a host-to-device staging optimisation
and is meaningless for tensors already resident on the device, so the loader
DIG constructs is forced to ``pin_memory=False``.

Where DIG is genuinely absent the import fails, and the audit skips and logs
the cell rather than aborting the run.
"""
from __future__ import annotations

import importlib.util
import sys
import types

import numpy as np
import torch

from .base import Attribution

_DIG_METHOD_PKG = "dig.xgraph.method"


def _shim_dataloader(shapley_module) -> None:
    """Stop DIG's Shapley loader from pinning device-resident tensors."""
    loader_cls = getattr(shapley_module, "DataLoader", None)
    if loader_cls is None or getattr(loader_cls, "_molsanity_no_pin", False):
        return

    class _UnpinnedDataLoader(loader_cls):
        _molsanity_no_pin = True

        def __init__(self, *args, **kwargs):
            kwargs["pin_memory"] = False
            super().__init__(*args, **kwargs)

    shapley_module.DataLoader = _UnpinnedDataLoader


def _import_subgraphx():
    """DIG's ``SubgraphX`` without executing the package ``__init__``.

    A synthetic module object carrying the real package's ``__path__`` is
    installed in ``sys.modules`` first, so Python resolves the submodule
    against it and never runs the ``__init__`` that would drag in Captum 0.2
    and ``torch_sparse``. If the real package is already imported, that import
    is reused untouched.
    """
    if _DIG_METHOD_PKG not in sys.modules:
        spec = importlib.util.find_spec(_DIG_METHOD_PKG)
        if spec is None:
            raise ImportError(f"{_DIG_METHOD_PKG} not found")
        stub = types.ModuleType(_DIG_METHOD_PKG)
        stub.__path__ = list(spec.submodule_search_locations or [])
        stub.__package__ = _DIG_METHOD_PKG
        stub.__spec__ = spec
        sys.modules[_DIG_METHOD_PKG] = stub

    from dig.xgraph.method import shapley as _shapley
    from dig.xgraph.method.subgraphx import SubgraphX

    _shim_dataloader(_shapley)
    return SubgraphX


class _TwoArgWrapper(torch.nn.Module):
    """Adapt ``backbone.forward(x, edge_index, edge_attr, batch)`` to the
    ``model(x, edge_index)`` signature DIG's SubgraphX calls.

    SubgraphX rebuilds the graph on every Monte-Carlo rollout and passes only
    the two tensors it perturbs, so the edge features and the batch vector have
    to be supplied here. Edge features are re-derived per call because the
    rollout's edge set is a subset of the original one and the stored
    ``edge_attr`` no longer lines up with it.
    """

    def __init__(self, model, edge_dim: int):
        super().__init__()
        self.model = model
        self.edge_dim = edge_dim

    def forward(self, x=None, edge_index=None, edge_attr=None, batch=None,
                data=None, **kwargs):
        from ..models.gine import ensure_edge_attr

        # DIG calls this two ways: positionally as ``model(x, edge_index)`` from
        # the search loop, and as ``model(data=batch)`` from the Shapley value
        # function, which passes a whole PyG Batch. Accept both.
        if data is not None:
            x = data.x
            edge_index = data.edge_index
            edge_attr = getattr(data, "edge_attr", None)
            batch = getattr(data, "batch", None)
        if batch is None:
            batch = torch.zeros(x.size(0), dtype=torch.long, device=x.device)
        if edge_attr is None or edge_attr.size(0) != edge_index.size(1):
            edge_attr = ensure_edge_attr(x, edge_index, None, self.edge_dim)
        return self.model(x, edge_index, edge_attr, batch)


class SubgraphXUnavailable(RuntimeError):
    """DIG (or its compiled dependencies) could not be imported."""


class SubgraphXAttributor:
    method = "SubgraphX"

    def __init__(self, model, task: str = "graph-classification",
                 max_nodes: int = 8, rollouts: int = 20, seed: int = 0,
                 edge_dim: int = 1):
        self.model = model
        self.edge_dim = edge_dim
        self.task = task
        self.max_nodes = max_nodes
        self.rollouts = rollouts
        self.seed = seed
        self._explainer = None

    def _build(self, num_classes: int):
        try:
            SubgraphX = _import_subgraphx()
        except Exception as exc:  # noqa: BLE001
            raise SubgraphXUnavailable(
                f"SubgraphX needs DIG (dive-into-graphs): {exc}"
            ) from exc
        device = next(self.model.parameters()).device
        return SubgraphX(
            _TwoArgWrapper(self.model, self.edge_dim).to(device),
            num_classes=num_classes, device=device,
            explain_graph=True, rollout=self.rollouts,
            min_atoms=min(4, self.max_nodes), expand_atoms=8,
            reward_method="mc_l_shapley", subgraph_building_method="zero_filling",
        )

    def attribute(self, data, target: int | None = None) -> Attribution:
        self.model.eval()
        device = next(self.model.parameters()).device
        data = data.to(device)
        batch = torch.zeros(data.num_nodes, dtype=torch.long, device=device)
        with torch.no_grad():
            out = self.model(data.x, data.edge_index, data.edge_attr, batch)
        n_classes = int(out.shape[1])
        pred = int(out.argmax(dim=1)) if self.task == "graph-classification" else 0
        tgt = pred if target is None else target

        if self._explainer is None:
            self._explainer = self._build(n_classes)

        torch.manual_seed(self.seed + int(getattr(data, "graph_id", 0) or 0))
        _, explanation, _related = self._explainer(
            data.x, data.edge_index, max_nodes=self.max_nodes
        )
        nodes = _selected_nodes(explanation, tgt, self.max_nodes)

        node_attr = np.zeros(int(data.num_nodes), dtype=np.float32)
        if nodes:
            node_attr[list(nodes)] = 1.0
        return Attribution(
            graph_id=int(getattr(data, "graph_id", 0) or 0),
            node_attr=node_attr,
            edge_attr=None,
            method=self.method,
            target=tgt,
            meta={"pred": pred, "max_nodes": self.max_nodes,
                  "rollouts": self.rollouts,
                  "n_selected": int(node_attr.sum()),
                  # An empty selection means the search returned nothing we
                  # recognised; the audit must not read that as "no atoms
                  # matter", so it is surfaced rather than swallowed.
                  "empty_selection": not nodes,
                  # SubgraphX returns a discrete subgraph, so the per-atom
                  # scores are 0/1 with no ranking inside the selection.
                  "hard_mask": True},
        )


def _coalition_of(node):
    """A search node's atom set, whether it is a dict or an object."""
    if isinstance(node, dict):
        return node.get("coalition")
    return getattr(node, "coalition", None)


def _score_of(node) -> float:
    """A search node's reward (``P`` in DIG's MCTS bookkeeping)."""
    p = node.get("P") if isinstance(node, dict) else getattr(node, "P", None)
    try:
        return float(p)
    except (TypeError, ValueError):
        return float("-inf")


def _selected_nodes(explanation, target: int, max_nodes: int) -> list[int]:
    """Pick the explaining subgraph out of DIG's Monte-Carlo search results.

    ``explanation`` is a list indexed by class, each entry a list of search
    nodes. The selection rule is DIG's own ``find_closest_node_result``: among
    the nodes whose coalition fits in ``max_nodes``, take the highest reward,
    defaulting to the smallest coalition if none fits. Reproducing their rule
    rather than inventing one keeps this a wrapper.

    Returns an empty list if the structure is not what we expect, so the caller
    can flag the molecule instead of scoring against a fabricated subgraph.
    """
    if not isinstance(explanation, (list, tuple)) or not explanation:
        return []
    results = explanation[target] if target < len(explanation) else explanation[0]
    if not isinstance(results, (list, tuple)) or not results:
        return []
    nodes = [r for r in results if _coalition_of(r) is not None]
    if not nodes:
        return []
    nodes = sorted(nodes, key=lambda r: len(_coalition_of(r)))
    best = nodes[0]
    for r in nodes:
        if len(_coalition_of(r)) <= max_nodes and _score_of(r) > _score_of(best):
            best = r
    return [int(v) for v in _coalition_of(best)]


__all__ = ["SubgraphXAttributor", "SubgraphXUnavailable"]
