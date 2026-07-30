"""Resumability + reporting tests (no heavy deps)."""
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
