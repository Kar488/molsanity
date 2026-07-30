"""Training loop + checkpointing for graph classification and regression.

Deterministic, resumable: if a checkpoint with a matching config hash exists we
load it instead of retraining. Classification records the calibration temperature
and ECE; regression records RMSE/MAE/R2 (targets standardised on the train split
for stable optimisation, metrics reported in original units).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from torch_geometric.loader import DataLoader

from ..utils import get_device, get_logger, hash_config
from .backbones import build_backbone
from .calibration import TemperatureScaler, expected_calibration_error, softmax_np

log = get_logger()


@dataclass
class TrainResult:
    ckpt_path: str
    config_hash: str
    epochs_run: int
    task: str = "graph-classification"
    backbone: str = "GINE"
    # classification metrics
    val_acc: float = float("nan")
    val_auc: float = float("nan")
    test_acc: float = float("nan")
    test_auc: float = float("nan")
    temperature: float = 1.0
    val_ece: float = float("nan")
    test_ece: float = float("nan")
    # regression metrics
    val_rmse: float = float("nan")
    test_rmse: float = float("nan")
    test_mae: float = float("nan")
    test_r2: float = float("nan")
    y_mean: float = 0.0
    y_std: float = 1.0
    early_ckpt_path: str | None = None
    history: list = field(default_factory=list)


def _subset(dataset, idx):
    return [dataset[i] for i in idx]


@torch.no_grad()
def _collect_outputs(model, loader, device):
    model.eval()
    out_all, y_all = [], []
    for batch in loader:
        batch = batch.to(device)
        out = model(batch.x, batch.edge_index, batch.edge_attr, batch.batch)
        out_all.append(out.cpu())
        y_all.append(batch.y.view(-1).cpu())
    if not out_all:
        return torch.empty(0), torch.empty(0)
    return torch.cat(out_all), torch.cat(y_all)


def _binary_metrics(logits: torch.Tensor, labels: torch.Tensor) -> tuple[float, float]:
    from sklearn.metrics import roc_auc_score

    probs = softmax_np(logits.numpy())
    pred = probs.argmax(axis=1)
    y = labels.numpy().astype(int)
    acc = float((pred == y).mean())
    try:
        auc = float(roc_auc_score(y, probs[:, 1]))
    except Exception:
        auc = float("nan")
    return acc, auc


def _regression_metrics(pred: torch.Tensor, y: torch.Tensor) -> dict:
    from sklearn.metrics import mean_absolute_error, r2_score

    p = pred.view(-1).numpy().astype(np.float64)
    t = y.view(-1).numpy().astype(np.float64)
    rmse = float(np.sqrt(np.mean((p - t) ** 2))) if p.size else float("nan")
    mae = float(mean_absolute_error(t, p)) if p.size else float("nan")
    try:
        r2 = float(r2_score(t, p)) if p.size > 1 else float("nan")
    except Exception:
        r2 = float("nan")
    return {"rmse": rmse, "mae": mae, "r2": r2}


def _train_epochs(model, opt, train_loader, val_loader, epochs, split, device,
                  loss_fn, eval_fn, better, save_intermediate_epoch, early_ckpt_path):
    """Shared training loop. ``loss_fn(out, batch)`` returns the batch loss;
    ``eval_fn()`` returns (monitor_scalar, history_dict); ``better(a, b)`` is the
    model-selection comparison. Identical control flow for both tasks."""
    best_monitor, best_state, best_epoch = None, None, 0
    history = []
    for epoch in range(1, epochs + 1):
        model.train()
        total = 0.0
        for batch in train_loader:
            batch = batch.to(device)
            opt.zero_grad()
            out = model(batch.x, batch.edge_index, batch.edge_attr, batch.batch)
            loss = loss_fn(out, batch)
            loss.backward()
            opt.step()
            total += float(loss) * batch.num_graphs
        train_loss = total / max(1, len(split.train))

        monitor, hist = eval_fn()
        history.append({"epoch": epoch, "train_loss": train_loss, **hist})
        if best_monitor is None or better(monitor, best_monitor):
            best_monitor, best_epoch = monitor, epoch
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
        if save_intermediate_epoch is not None and epoch == save_intermediate_epoch:
            torch.save(
                {"state_dict": {k: v.detach().cpu().clone() for k, v in model.state_dict().items()},
                 "epoch": epoch},
                early_ckpt_path,
            )
            log.info("Saved early checkpoint @epoch %d -> %s", epoch, early_ckpt_path.name)
    return best_state, best_monitor, best_epoch, history


def train_model(
    dataset,
    split,
    model_cfg: dict,
    train_cfg: dict,
    ckpt_dir: str | Path,
    seed: int = 0,
    backbone: str = "GINE",
    save_intermediate_epoch: int | None = None,
) -> tuple[torch.nn.Module, TrainResult]:
    """Train (or load) a backbone on the given split. Idempotent by config hash.

    ``save_intermediate_epoch`` additionally snapshots the model at that epoch
    (an *early* checkpoint) so the audit can measure cross-checkpoint stability.
    """
    from ..utils import set_global_seed

    set_global_seed(seed)
    device = get_device(train_cfg.get("device"))
    ckpt_dir = Path(ckpt_dir)
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    task = model_cfg.get("task", "graph-classification")
    is_reg = task == "graph-regression"

    cfg_hash = hash_config(
        {"model": model_cfg, "train": train_cfg, "split": split.kind,
         "seed": seed, "backbone": backbone}
    )
    ckpt_path = ckpt_dir / f"{backbone.lower()}_{cfg_hash}.pt"
    early_ckpt_path = ckpt_dir / f"{backbone.lower()}_{cfg_hash}_early.pt"

    sample = dataset[0]
    model = build_backbone(backbone, sample, model_cfg).to(device)

    if ckpt_path.exists():
        payload = torch.load(ckpt_path, map_location=device, weights_only=False)
        model.load_state_dict(payload["state_dict"])
        model.eval()
        log.info("Loaded existing checkpoint %s", ckpt_path.name)
        res = TrainResult(**{k: payload[k] for k in TrainResult.__dataclass_fields__ if k in payload})
        return model, res

    train_subset = _subset(dataset, split.train)
    batch_size = train_cfg.get("batch_size", 32)
    # A trailing batch of size 1 makes BatchNorm raise in train mode ("expected
    # more than 1 value per channel"), which killed whole cells whenever
    # len(train) % batch_size == 1. Drop that single graph for the epoch instead.
    drop_last = len(train_subset) % batch_size == 1 and len(train_subset) > batch_size
    train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True,
                              drop_last=drop_last)
    val_loader = DataLoader(_subset(dataset, split.val), batch_size=64)
    test_loader = DataLoader(_subset(dataset, split.test), batch_size=64)

    opt = torch.optim.Adam(
        model.parameters(),
        lr=train_cfg.get("lr", 1e-3),
        weight_decay=train_cfg.get("weight_decay", 5e-4),
    )
    epochs = int(train_cfg.get("epochs", 100))

    if is_reg:
        # Standardise targets on the train split for stable optimisation.
        train_y = torch.cat([dataset[i].y.view(-1) for i in split.train]).float()
        y_mean, y_std = float(train_y.mean()), float(train_y.std().clamp_min(1e-6))

        def loss_fn(out, batch):
            target = (batch.y.view(-1).float() - y_mean) / y_std
            return F.smooth_l1_loss(out.view(-1), target)

        def eval_fn():
            out, y = _collect_outputs(model, val_loader, device)
            pred = out.view(-1) * y_std + y_mean
            m = _regression_metrics(pred, y)
            return m["rmse"], {"val_rmse": m["rmse"]}

        better = lambda a, b: a < b  # lower RMSE is better
    else:
        y_mean, y_std = 0.0, 1.0

        # Optional inverse-frequency class weighting for imbalanced datasets
        # (opt-in via train.class_weight so balanced sets are numerically
        # unchanged). Without it, imbalanced sets collapse to majority-class.
        class_weight = None
        if train_cfg.get("class_weight"):
            import numpy as _np

            train_y = _np.array([int(dataset[i].y.view(-1)[0]) for i in split.train])
            n_out = int(model_cfg.get("out_channels", 2))
            counts = _np.array([max(1, int((train_y == c).sum())) for c in range(n_out)])
            w = counts.sum() / (n_out * counts)
            class_weight = torch.tensor(w, dtype=torch.float, device=device)

        def loss_fn(out, batch):
            return F.cross_entropy(out, batch.y.view(-1).long(), weight=class_weight)

        select_by_auc = bool(train_cfg.get("class_weight"))

        def eval_fn():
            vl, vy = _collect_outputs(model, val_loader, device)
            acc, auc = _binary_metrics(vl, vy)
            # For imbalanced (weighted) training, select by AUC (robust); for
            # balanced sets keep accuracy selection so validated numbers are
            # unchanged.
            monitor = (auc if auc == auc else acc) if select_by_auc else acc
            return monitor, {"val_acc": acc, "val_auc": auc}

        better = lambda a, b: a > b  # higher is better

    best_state, best_monitor, best_epoch, history = _train_epochs(
        model, opt, train_loader, val_loader, epochs, split, device,
        loss_fn, eval_fn, better, save_intermediate_epoch, early_ckpt_path,
    )

    if best_state is not None:
        model.load_state_dict(best_state)
    model.eval()  # deterministic downstream attribution/audit

    common = dict(
        ckpt_path=str(ckpt_path), config_hash=cfg_hash, epochs_run=epochs,
        task=task, backbone=backbone,
        early_ckpt_path=str(early_ckpt_path) if early_ckpt_path.exists() else None,
        history=history, y_mean=y_mean, y_std=y_std,
    )

    if is_reg:
        vout, vy = _collect_outputs(model, val_loader, device)
        tout, ty = _collect_outputs(model, test_loader, device)
        vm = _regression_metrics(vout.view(-1) * y_std + y_mean, vy)
        tm = _regression_metrics(tout.view(-1) * y_std + y_mean, ty)
        res = TrainResult(val_rmse=vm["rmse"], test_rmse=tm["rmse"],
                          test_mae=tm["mae"], test_r2=tm["r2"], **common)
        log.info("Training done (regression): best val_rmse=%.3f @epoch %d | "
                 "test_rmse=%.3f test_r2=%.3f", best_monitor, best_epoch,
                 tm["rmse"], tm["r2"])
    else:
        vl, vy = _collect_outputs(model, val_loader, device)
        scaler = TemperatureScaler().to("cpu")
        if len(vy) > 0:
            scaler.fit(vl, vy)
        temperature = scaler.temperature
        val_acc, val_auc = _binary_metrics(vl, vy)
        tl, ty = _collect_outputs(model, test_loader, device)
        test_acc, test_auc = _binary_metrics(tl, ty)
        val_ece = expected_calibration_error(softmax_np((vl / temperature).numpy()), vy.numpy().astype(int))["ece"]
        test_ece = expected_calibration_error(softmax_np((tl / temperature).numpy()), ty.numpy().astype(int))["ece"]
        res = TrainResult(val_acc=val_acc, val_auc=val_auc, test_acc=test_acc,
                          test_auc=test_auc, temperature=temperature,
                          val_ece=val_ece, test_ece=test_ece, **common)
        log.info("Training done: best val_acc=%.3f @epoch %d | test_acc=%.3f "
                 "test_auc=%.3f T=%.3f", best_monitor, best_epoch, test_acc, test_auc, temperature)

    payload = {"state_dict": model.state_dict(), **res.__dict__}
    torch.save(payload, ckpt_path)
    log.info("Saved checkpoint %s", ckpt_path.name)
    return model, res


def train_gine(dataset, split, model_cfg, train_cfg, ckpt_dir, seed=0, **kw):
    """Back-compat alias: train the GINE backbone."""
    return train_model(dataset, split, model_cfg, train_cfg, ckpt_dir, seed=seed,
                       backbone="GINE", **kw)
