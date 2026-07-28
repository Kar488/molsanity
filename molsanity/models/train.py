"""Training loop + checkpointing for graph classification (the slice target).

Deterministic, resumable: if a checkpoint with a matching config hash exists we
load it instead of retraining. Records train/val metrics and the calibration
temperature into the checkpoint payload.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from torch_geometric.loader import DataLoader

from ..utils import get_device, get_logger, hash_config
from .calibration import TemperatureScaler, expected_calibration_error, softmax_np
from .gine import build_model

log = get_logger()


@dataclass
class TrainResult:
    ckpt_path: str
    val_acc: float
    val_auc: float
    test_acc: float
    test_auc: float
    temperature: float
    val_ece: float
    test_ece: float
    epochs_run: int
    config_hash: str
    history: list = field(default_factory=list)


def _subset(dataset, idx):
    return [dataset[i] for i in idx]


@torch.no_grad()
def _collect_logits(model, loader, device):
    model.eval()
    logits_all, labels_all = [], []
    for batch in loader:
        batch = batch.to(device)
        out = model(batch.x, batch.edge_index, batch.edge_attr, batch.batch)
        logits_all.append(out.cpu())
        labels_all.append(batch.y.view(-1).cpu())
    return torch.cat(logits_all), torch.cat(labels_all)


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


def train_gine(
    dataset,
    split,
    model_cfg: dict,
    train_cfg: dict,
    ckpt_dir: str | Path,
    seed: int = 0,
) -> tuple[torch.nn.Module, TrainResult]:
    """Train (or load) a GINE on the given split. Idempotent by config hash."""
    from ..utils import set_global_seed

    set_global_seed(seed)
    device = get_device(train_cfg.get("device"))
    ckpt_dir = Path(ckpt_dir)
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    cfg_hash = hash_config({"model": model_cfg, "train": train_cfg, "split": split.kind, "seed": seed})
    ckpt_path = ckpt_dir / f"gine_{cfg_hash}.pt"

    sample = dataset[0]
    model = build_model(sample, model_cfg).to(device)

    if ckpt_path.exists():
        payload = torch.load(ckpt_path, map_location=device, weights_only=False)
        model.load_state_dict(payload["state_dict"])
        model.eval()
        log.info("Loaded existing checkpoint %s (val_acc=%.3f)", ckpt_path.name, payload["val_acc"])
        res = TrainResult(**{k: payload[k] for k in TrainResult.__dataclass_fields__ if k in payload})
        return model, res

    train_loader = DataLoader(_subset(dataset, split.train), batch_size=train_cfg.get("batch_size", 32), shuffle=True)
    val_loader = DataLoader(_subset(dataset, split.val), batch_size=64)
    test_loader = DataLoader(_subset(dataset, split.test), batch_size=64)

    opt = torch.optim.Adam(
        model.parameters(),
        lr=train_cfg.get("lr", 1e-3),
        weight_decay=train_cfg.get("weight_decay", 5e-4),
    )
    epochs = int(train_cfg.get("epochs", 100))
    best_val, best_state, best_epoch = -1.0, None, 0
    history = []

    for epoch in range(1, epochs + 1):
        model.train()
        total = 0.0
        for batch in train_loader:
            batch = batch.to(device)
            opt.zero_grad()
            out = model(batch.x, batch.edge_index, batch.edge_attr, batch.batch)
            loss = F.cross_entropy(out, batch.y.view(-1).long())
            loss.backward()
            opt.step()
            total += float(loss) * batch.num_graphs
        train_loss = total / max(1, len(split.train))

        vl, vy = _collect_logits(model, val_loader, device)
        val_acc, val_auc = _binary_metrics(vl, vy)
        history.append({"epoch": epoch, "train_loss": train_loss, "val_acc": val_acc, "val_auc": val_auc})
        if val_acc > best_val:
            best_val, best_epoch = val_acc, epoch
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}

    if best_state is not None:
        model.load_state_dict(best_state)
    model.eval()  # deterministic downstream attribution/audit
    log.info("Training done: best val_acc=%.3f @epoch %d", best_val, best_epoch)

    # Calibrate on validation logits.
    vl, vy = _collect_logits(model, val_loader, device)
    scaler = TemperatureScaler().to("cpu")
    if len(vy) > 0:
        scaler.fit(vl, vy)
    temperature = scaler.temperature

    val_acc, val_auc = _binary_metrics(vl, vy)
    tl, ty = _collect_logits(model, test_loader, device)
    test_acc, test_auc = _binary_metrics(tl, ty)

    val_ece = expected_calibration_error(softmax_np((vl / temperature).numpy()), vy.numpy().astype(int))["ece"]
    test_ece = expected_calibration_error(softmax_np((tl / temperature).numpy()), ty.numpy().astype(int))["ece"]

    res = TrainResult(
        ckpt_path=str(ckpt_path),
        val_acc=val_acc, val_auc=val_auc,
        test_acc=test_acc, test_auc=test_auc,
        temperature=temperature,
        val_ece=val_ece, test_ece=test_ece,
        epochs_run=epochs, config_hash=cfg_hash, history=history,
    )

    payload = {"state_dict": model.state_dict(), **res.__dict__}
    torch.save(payload, ckpt_path)
    log.info("Saved checkpoint %s | test_acc=%.3f test_auc=%.3f T=%.3f", ckpt_path.name, test_acc, test_auc, temperature)
    return model, res
