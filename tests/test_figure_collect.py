"""Figure collection: mirrors artifacts/figures into the tracked figures/ tree."""
from pathlib import Path

from molsanity.viz.collect import collect_figures


def _touch(p: Path, data=b"%PDF-1.4 fake"):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)


def test_collect_mirrors_and_indexes(tmp_path):
    src = tmp_path / "artifacts" / "figures"
    dest = tmp_path / "figures"
    _touch(src / "_summary" / "heatmap_gt.pdf")
    _touch(src / "_summary" / "dissociation.pdf")
    _touch(src / "MUTAG__GINE__IntegratedGradients__scaffold" / "gt_validation.pdf")
    _touch(src / "MUTAG__GINE__IntegratedGradients__scaffold" / "case_molecule.svg")

    info = collect_figures(src_root=src, dest_root=dest)

    assert info["scanned"] == 4
    assert info["n_cells"] == 1
    # Summary figures land in summary/, per-cell under cells/<cell>/.
    assert (dest / "summary" / "heatmap_gt.pdf").exists()
    assert (dest / "cells" / "MUTAG__GINE__IntegratedGradients__scaffold"
            / "gt_validation.pdf").exists()
    # Headline figures are promoted into key/.
    assert (dest / "key" / "dissociation.pdf").exists()
    assert (dest / "key" / "heatmap_gt.pdf").exists()

    index = (dest / "INDEX.md").read_text()
    assert "dissociation" in index and "MUTAG__GINE" in index


def test_collect_is_idempotent(tmp_path):
    """Re-running must not rewrite unchanged files (keeps the git diff clean)."""
    src, dest = tmp_path / "src", tmp_path / "dst"
    _touch(src / "_summary" / "heatmap_gt.pdf")
    first = collect_figures(src_root=src, dest_root=dest)
    second = collect_figures(src_root=src, dest_root=dest)
    assert first["copied"] > 0
    assert second["copied"] == 0


def test_collect_handles_missing_source(tmp_path):
    info = collect_figures(src_root=tmp_path / "nope", dest_root=tmp_path / "out")
    assert info["scanned"] == 0
    assert (tmp_path / "out" / "INDEX.md").exists()
