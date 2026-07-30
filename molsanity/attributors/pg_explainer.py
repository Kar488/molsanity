"""PGExplainer attributor, wrapping PyG's canonical parametric PGExplainer.

Unlike the gradient / GNNExplainer methods, PGExplainer is *parametric*: a small
MLP is trained once over the training graphs to predict edge masks, then reused to
explain any molecule. It produces edge masks only; we aggregate incident-edge
importance to a per-node attribution so it fits MolSanity's common node schema.

Not reimplemented — driven via ``torch_geometric.explain.PGExplainer``.
"""
from __future__ import annotations

import numpy as np
import torch

from ..utils import get_logger
from .base import Attribution, _ExplainerWrapper

log = get_logger()


class PGExplainerAttributor:
    method = "PGExplainer"
    attribution_seed = 10_000

    def __init__(self, model, task: str = "graph-classification",
                 train_graphs=None, epochs: int = 30, lr: float = 0.01,
                 max_train_graphs: int = 200, seed: int = 0):
        if task != "graph-classification":
            raise ValueError("PGExplainer wrapper currently supports classification only.")
        from ..utils import set_global_seed

        # Seed BEFORE constructing the explainer: PGExplainer's mask MLP is
        # randomly initialised at build time, so seeding here (not just before
        # training) makes the whole attributor reproducible regardless of the
        # ambient RNG state (fresh-train vs checkpoint-reload).
        import copy

        set_global_seed(seed)
        self.task = task
        self.epochs = epochs
        # Work on a private copy in eval mode: PGExplainer's training forwards the
        # GNN, which would otherwise update the caller's BatchNorm running stats
        # (corrupting predictions the audit reads from the same model object).
        # Freeze BN running stats (momentum=0) so they stay identical to the
        # trained model even if the algorithm forwards in train mode.
        self.model = copy.deepcopy(model).eval()
        for mod in self.model.modules():
            if isinstance(mod, torch.nn.modules.batchnorm._BatchNorm):
                mod.momentum = 0.0
        self._wrapped = _ExplainerWrapper(self.model)
        self._explainer = self._build_explainer(lr)
        self._train(train_graphs or [], max_train_graphs, seed)

    def _build_explainer(self, lr):
        from torch_geometric.explain import Explainer, PGExplainer

        return Explainer(
            model=self._wrapped,
            algorithm=PGExplainer(epochs=self.epochs, lr=lr),
            explanation_type="phenomenon",
            edge_mask_type="object",
            node_mask_type=None,
            model_config=dict(mode="multiclass_classification",
                              task_level="graph", return_type="raw"),
        )

    def _pred_target(self, g, device):
        batch = torch.zeros(g.num_nodes, dtype=torch.long, device=device)
        with torch.no_grad():
            out = self.model(g.x, g.edge_index, g.edge_attr, batch)
        return out.argmax(dim=1), batch

    def _train(self, train_graphs, max_train_graphs, seed):
        from ..utils import set_global_seed

        set_global_seed(seed)
        device = next(self.model.parameters()).device
        self.model.eval()
        graphs = list(train_graphs)[:max_train_graphs]
        if not graphs:
            log.warning("PGExplainer: no training graphs provided; explanations "
                        "will be from an untrained parametric mask.")
            return
        last = None
        for epoch in range(self.epochs):
            for g in graphs:
                g = g.to(device)
                target, batch = self._pred_target(g, device)
                last = self._explainer.algorithm.train(
                    epoch, self._wrapped, g.x, g.edge_index, target=target,
                    edge_attr=g.edge_attr, batch=batch,
                )
        log.info("PGExplainer trained on %d graphs (%d epochs), final loss %.4f",
                 len(graphs), self.epochs, float(last) if last is not None else float("nan"))

    def attribute(self, data, target: int | None = None) -> Attribution:
        self.model.eval()
        device = next(self.model.parameters()).device
        data = data.to(device)
        pred_t, batch = self._pred_target(data, device)
        pred = int(pred_t)
        tgt = target if target is not None else pred

        gid = int(getattr(data, "graph_id", 0))
        torch.manual_seed(self.attribution_seed + (gid if gid >= 0 else 0))
        explanation = self._explainer(
            data.x, data.edge_index, target=torch.tensor([tgt], device=device),
            edge_attr=data.edge_attr, batch=batch,
        )
        edge_mask = explanation.get("edge_mask")
        n = int(data.num_nodes)
        if edge_mask is not None:
            em = edge_mask.detach().abs().cpu().numpy()
            ei = data.edge_index.cpu().numpy()
            node_attr = np.zeros(n, dtype=np.float64)
            # Aggregate incident-edge importance onto nodes (both endpoints).
            for k in range(ei.shape[1]):
                node_attr[ei[0, k]] += em[k]
                node_attr[ei[1, k]] += em[k]
        else:
            node_attr = np.zeros(n, dtype=np.float64)
            em = None

        return Attribution(
            graph_id=gid, node_attr=node_attr,
            edge_attr=em.astype(np.float64) if em is not None else None,
            method=self.method, target=tgt,
            meta={"pred": pred, "epochs": self.epochs},
        )
