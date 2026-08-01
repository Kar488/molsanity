"""Per-attributor evaluation caps, without invalidating the cache.

Attributors differ by three orders of magnitude in cost. Measured on 30-node
SynthMotifs graphs, Integrated Gradients is milliseconds per molecule and
SubgraphX is 28-38 seconds, so a single ``max_eval_molecules: 200`` is free for
one and a twenty-hour job for the other -- with every cell queued behind it
waiting.

The override fixes that, but it has a trap: the stage ``.done`` marker is keyed
by a hash that includes the budget, so a naive `budget["max_eval_molecules_X"]`
would change every cell's hash and silently discard a run's worth of completed
work. Resolving the override per attributor keeps each cell's hash dependent
only on the cap that applies to it.
"""
from __future__ import annotations

from molsanity.run_all import effective_budget, hashable_budget
from molsanity.utils import hash_config

BASE = {"epochs": 150, "ig_steps": 50, "max_eval_molecules": 200,
        "sgx_max_nodes": 8}
WITH_OVERRIDE = {**BASE, "max_eval_molecules_SubgraphX": 40}


def _stage_hash(budget, attributor):
    return hash_config({
        "cell": {"dataset": "SynthMotifs", "backbone": "GINE",
                 "attributor": attributor},
        "split": "scaffold", "budget": budget,
        "model": {"hidden_channels": 64}, "train": {"lr": 1e-3}, "seed": 0,
    })


def test_override_applies_to_its_attributor_only():
    assert effective_budget(WITH_OVERRIDE, "SubgraphX")["max_eval_molecules"] == 40
    for other in ("IntegratedGradients", "GNNExplainer", "Saliency"):
        assert effective_budget(WITH_OVERRIDE, other)["max_eval_molecules"] == 200


def test_adding_an_override_does_not_invalidate_other_cells():
    """The whole point. A cheap knob must not cost a run's worth of cache."""
    for other in ("IntegratedGradients", "GNNExplainer", "PGExplainer",
                  "Saliency", "GuidedBackprop"):
        before = _stage_hash(BASE, other)
        after = _stage_hash(effective_budget(WITH_OVERRIDE, other), other)
        assert before == after, (
            f"{other} lost its .done marker because SubgraphX got a cap")


def test_the_overridden_attributor_does_re_run():
    """It must invalidate the cell it applies to -- n changed, so the result
    would no longer match the marker."""
    before = _stage_hash(BASE, "SubgraphX")
    after = _stage_hash(effective_budget(WITH_OVERRIDE, "SubgraphX"), "SubgraphX")
    assert before != after


def test_override_keys_never_leak_into_the_hashed_budget():
    """Otherwise adding an override for a second attributor would invalidate
    the first one's cells."""
    two = {**WITH_OVERRIDE, "max_eval_molecules_GNNExplainer": 100}
    eff = effective_budget(two, "SubgraphX")
    assert not any(k.startswith("max_eval_molecules_") for k in eff)
    assert eff["max_eval_molecules"] == 40
    # Adding the GNNExplainer override must not disturb SubgraphX's hash.
    assert _stage_hash(effective_budget(WITH_OVERRIDE, "SubgraphX"), "SubgraphX") \
        == _stage_hash(eff, "SubgraphX")


def test_no_override_is_a_pass_through():
    assert effective_budget(BASE, "SubgraphX") == BASE
    assert effective_budget(None, "SubgraphX") == {}


def test_the_original_budget_is_not_mutated():
    """run_all calls this once per cell over the same config dict."""
    snapshot = dict(WITH_OVERRIDE)
    effective_budget(WITH_OVERRIDE, "SubgraphX")
    effective_budget(WITH_OVERRIDE, "IntegratedGradients")
    assert WITH_OVERRIDE == snapshot


def test_committed_full_config_keeps_the_full_n_for_every_attributor():
    """SubgraphX must not be made affordable by shrinking n.

    Capping it was the first fix, and it was the wrong one: a small n is
    precisely what the review criticised, so buying speed that way trades the
    problem for the problem. Speed comes from the worker pool instead, and this
    test exists so that a future "just cap it" cannot land quietly.
    """
    from pathlib import Path

    import yaml

    root = Path(__file__).resolve().parents[1]
    budget = yaml.safe_load((root / "configs/full.yaml").read_text())["budget"]

    assert not any(k.startswith("max_eval_molecules_") for k in budget), (
        "a per-attributor cap is back in full.yaml; n must stay uniform")
    for attributor in ("SubgraphX", "IntegratedGradients", "GNNExplainer"):
        assert effective_budget(budget, attributor)["max_eval_molecules"] == 200
    assert budget.get("attribution_workers"), (
        "SubgraphX at n=200 is a ~20 hour job without the worker pool")


# ------------------------------------------------- execution-only settings ---
def test_turning_parallelism_on_does_not_discard_the_cache():
    """attribution_workers lives in `budget`, and the stage hash is taken over
    `budget`, so switching the worker pool on would have rehashed every cell and
    thrown away 150 completed cell-runs. It schedules work; it does not change
    what is computed, and that is verified separately by the parallel-equals-
    serial test. It must not reach the hash."""
    without = dict(BASE)
    with_pool = {**BASE, "attribution_workers": "auto"}
    for attributor in ("IntegratedGradients", "GNNExplainer", "SubgraphX",
                       "Saliency", "PGExplainer"):
        before = _stage_hash(without, attributor)
        after = _stage_hash(hashable_budget(effective_budget(with_pool, attributor)),
                            attributor)
        assert before == after, (
            f"{attributor} lost its .done marker merely because parallelism "
            "was switched on")


def test_the_cell_still_receives_the_setting_it_needs():
    """Stripping it from the hash must not strip it from the run."""
    with_pool = {**BASE, "attribution_workers": 8}
    assert effective_budget(with_pool, "SubgraphX")["attribution_workers"] == 8
    assert "attribution_workers" not in hashable_budget(with_pool)


def test_scientific_parameters_still_reach_the_hash():
    """Guards the guard: only execution settings are exempt."""
    for key, value in (("epochs", 999), ("ig_steps", 7),
                       ("max_eval_molecules", 50), ("sgx_max_nodes", 3)):
        changed = {**BASE, key: value}
        assert _stage_hash(hashable_budget(BASE), "SubgraphX") \
            != _stage_hash(hashable_budget(changed), "SubgraphX"), (
            f"changing {key} did not invalidate the cache, so a re-run would "
            "silently reuse results computed under different settings")
