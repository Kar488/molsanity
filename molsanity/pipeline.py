"""Staged, resumable pipeline primitives.

A *stage* writes artifacts to ``artifacts/<stage>/`` plus a ``.done`` marker
carrying a content hash of its config. Re-running a stage whose config hash
matches an existing marker is a no-op (returns the cached result). This gives
overnight resumability: finished work is never redone.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .utils import get_logger, hash_config

log = get_logger()

ARTIFACT_ROOT = Path("artifacts")


@dataclass
class StageResult:
    name: str
    config_hash: str
    cached: bool
    output_dir: str
    payload: dict


def stage(
    name: str,
    config: dict,
    fn: Callable[[Path], dict],
    root: Path = ARTIFACT_ROOT,
) -> StageResult:
    """Run ``fn(output_dir)`` unless a matching ``.done`` marker exists.

    ``fn`` must write its artifacts under ``output_dir`` and return a JSON-able
    payload dict, which is persisted next to the marker and returned on cache
    hits without re-running.
    """
    cfg_hash = hash_config(config)
    out_dir = root / name
    out_dir.mkdir(parents=True, exist_ok=True)
    done = out_dir / ".done"
    payload_path = out_dir / "payload.json"

    if done.exists():
        prev = done.read_text().strip()
        if prev == cfg_hash and payload_path.exists():
            payload = json.loads(payload_path.read_text())
            log.info("[stage %s] cache hit (%s) — skipping", name, cfg_hash)
            return StageResult(name, cfg_hash, True, str(out_dir), payload)
        log.info("[stage %s] config changed (%s -> %s) — rerunning", name, prev, cfg_hash)

    log.info("[stage %s] running (%s)", name, cfg_hash)
    payload = fn(out_dir)
    payload_path.write_text(json.dumps(payload, indent=2, default=str))
    done.write_text(cfg_hash)
    return StageResult(name, cfg_hash, False, str(out_dir), payload)


class RunLedger:
    """Tracks per-cell status (done / running / failed) for PROGRESS.md."""

    def __init__(self):
        self.cells: list[dict] = []

    def record(self, cell: dict, status: str, detail: str = ""):
        self.cells.append({**cell, "status": status, "detail": detail})

    def counts(self) -> dict:
        c = {"done": 0, "failed": 0, "skipped": 0, "running": 0}
        for e in self.cells:
            c[e["status"]] = c.get(e["status"], 0) + 1
        return c
