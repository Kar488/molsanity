"""Shared utilities: determinism, hashing, logging, device, run manifests."""
from __future__ import annotations

import hashlib
import json
import logging
import os
import platform
import random
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

LOGGER_NAME = "molsanity"


# --------------------------------------------------------------------------- #
# Determinism
# --------------------------------------------------------------------------- #
def set_global_seed(seed: int) -> None:
    """Seed python / numpy / torch (if present) for reproducibility."""
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch

        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.use_deterministic_algorithms(True, warn_only=True)
    except Exception:  # pragma: no cover - torch optional at import time
        pass


def get_device(prefer: str | None = None):
    """Return a torch device; GPU if available, else CPU."""
    import torch

    if prefer:
        return torch.device(prefer)
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# --------------------------------------------------------------------------- #
# Hashing (for idempotent stages + checksums)
# --------------------------------------------------------------------------- #
def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hash_file(path: str | Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def hash_config(obj: Any) -> str:
    """Stable content hash of a JSON-serialisable config object."""
    payload = json.dumps(obj, sort_keys=True, default=str).encode()
    return hash_bytes(payload)[:16]


# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
def setup_logging(log_dir: str | Path = "logs", timestamp: str | None = None) -> logging.Logger:
    """Configure structured logging to console + rolling file.

    ``timestamp`` is passed in explicitly (never generated with a wall clock in
    hot code paths) so runs are reproducible / resumable.
    """
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    fmt = logging.Formatter("%(asctime)s | %(levelname)-7s | %(name)s | %(message)s")

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    if timestamp:
        fh = logging.FileHandler(log_dir / f"run_{timestamp}.log")
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    logger.propagate = False
    return logger


def get_logger() -> logging.Logger:
    return logging.getLogger(LOGGER_NAME)


# --------------------------------------------------------------------------- #
# Run manifest (environment provenance)
# --------------------------------------------------------------------------- #
def _pkg_version(name: str) -> str | None:
    try:
        mod = __import__(name)
        return getattr(mod, "__version__", None)
    except Exception:
        return None


def _git_rev() -> str | None:
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
    except Exception:
        return None


@dataclass
class RunManifest:
    """Captured environment for reproducibility. Written into every run dir."""

    seed: int
    config_hash: str
    timestamp: str
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        import_versions = {
            n: _pkg_version(n)
            for n in ["numpy", "scipy", "sklearn", "torch", "torch_geometric", "rdkit", "captum"]
        }
        cuda = None
        try:
            import torch

            cuda = {
                "available": torch.cuda.is_available(),
                "device_count": torch.cuda.device_count(),
            }
        except Exception:
            pass
        return {
            "seed": self.seed,
            "config_hash": self.config_hash,
            "timestamp": self.timestamp,
            "python": sys.version,
            "platform": platform.platform(),
            "processor": platform.processor(),
            "git_rev": _git_rev(),
            "versions": import_versions,
            "cuda": cuda,
            **self.extra,
        }

    def write(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2))


# --------------------------------------------------------------------------- #
# Small IO helpers
# --------------------------------------------------------------------------- #
def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text())


def write_json(path: str | Path, obj: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, default=str))
