"""Resumability + reporting tests (no heavy deps)."""
import pytest

from molsanity.pipeline import RunLedger, stage
from molsanity.reporting import _parse_existing_rows, results_row, update_results_md


def test_stage_is_idempotent(tmp_path):
    calls = {"n": 0}

    def fn(out_dir):
        calls["n"] += 1
        (out_dir / "artifact.txt").write_text("hi")
        return {"value": 42}

    cfg = {"a": 1}
    r1 = stage("mystage", cfg, fn, root=tmp_path)
    assert r1.cached is False and r1.payload["value"] == 42 and calls["n"] == 1

    # Re-run same config -> cache hit, fn NOT called again.
    r2 = stage("mystage", cfg, fn, root=tmp_path)
    assert r2.cached is True and r2.payload["value"] == 42 and calls["n"] == 1

    # Changed config -> re-run.
    r3 = stage("mystage", {"a": 2}, fn, root=tmp_path)
    assert r3.cached is False and calls["n"] == 2


def test_results_md_roundtrip_and_dedup(tmp_path):
    path = tmp_path / "RESULTS.md"
    cell = {"dataset": "MUTAG", "backbone": "GINE", "attributor": "IntegratedGradients"}
    agg = {"n_molecules": 20, "accuracy": 0.6,
           "gt_auroc": {"mean": 0.22}, "gt_auprc": {"mean": 0.16},
           "motif_top1_share": {"mean": 0.98}, "occ_spearman": {"mean": 0.57},
           "occ_top1_agreement": {"mean": 0.8}, "fidelity_plus": {"mean": 0.27},
           "fidelity_minus": {"mean": 0.27}, "sparsity": {"mean": 0.77}}
    row = results_row(cell, agg, {"test_ece": 0.32}, "scaffold")
    update_results_md([row], path=path)
    rows = _parse_existing_rows(path)
    assert len(rows) == 1
    # The key includes the seed, so ask the module for it rather than pinning a
    # literal; a multi-seed run must not collapse three results into one row.
    from molsanity.reporting import _row_key

    assert _row_key(row) in rows

    # Writing the same key again replaces in place (no duplicate row).
    update_results_md([row], path=path)
    assert len(_parse_existing_rows(path)) == 1


def test_ledger_counts():
    led = RunLedger()
    led.record({"dataset": "MUTAG"}, "done")
    led.record({"dataset": "BBBP"}, "skipped", "blocked")
    assert led.counts()["done"] == 1
    assert led.counts()["skipped"] == 1


def test_scaffold_split_version_invalidates_only_the_scaffold_arm():
    """Correcting the scaffold split must re-run scaffold cells and *only* those.

    The stage hash covers config, not code. Without an explicit version the
    2026-08-03 split fix would have silently reused every cell computed under
    the broken partition; bumping it indiscriminately would have thrown away the
    204 valid random-split cell-runs alongside them.
    """
    from molsanity.run_all import SCAFFOLD_SPLIT_VERSION, stage_config
    from molsanity.utils import hash_config

    cell = {"dataset": "BBBP", "backbone": "GINE", "attributor": "IntegratedGradients"}
    cfg = {"model": {"hidden": 64}, "train": {"epochs": 5}, "budget": {"ig_steps": 50}}

    scaffold = stage_config(cell, "scaffold", cfg, seed=0)
    random_ = stage_config(cell, "random", cfg, seed=0)
    assert scaffold["split_version"] == SCAFFOLD_SPLIT_VERSION
    assert "split_version" not in random_, "a random split has no scaffold version"

    # A version bump changes the scaffold hash and leaves the random one alone.
    bumped = dict(scaffold, split_version=SCAFFOLD_SPLIT_VERSION + 1)
    assert hash_config(bumped) != hash_config(scaffold)
    assert hash_config(stage_config(cell, "random", cfg, seed=0)) == hash_config(random_)


def test_stage_config_is_the_only_definition_of_the_stage_hash():
    """The Colab preflight rebuilt this rule by hand and drifted from it twice.
    It now imports ``stage_config``; nothing else may reconstruct the dict."""
    import json
    from pathlib import Path

    nb = Path("notebooks/molsanity_full_run_colab.ipynb")
    if not nb.exists():
        pytest.skip("notebook not present")
    sources = [
        "".join(c["source"]) for c in json.loads(nb.read_text())["cells"]
        if c["cell_type"] == "code"
    ]
    preflight = [s for s in sources if "hash_config" in s and ".done" in s]
    assert preflight, "no resume-preflight cell found in the notebook"
    for src in preflight:
        assert "stage_config" in src, "preflight must import run_all.stage_config"
        assert "'model': cfg['model']" not in src, (
            "preflight is rebuilding the stage hash by hand again")
