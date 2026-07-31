"""The dependency interaction that cost a full run its Integrated Gradients.

The first complete sweep produced 204 failed cells, every one of them
Integrated Gradients, every one raising ``IndexError: index 1 is out of bounds
for dimension 0 with size 1`` inside PyG's ``set_masks``. The cause was not in
this repository: installing ``dive-into-graphs`` for SubgraphX honours DIG's
``captum==0.2.0`` pin and downgrades Captum. PyG's ``CaptumExplainer`` forces
``internal_batch_size=1``, and Captum 0.2 slices the additional forward
arguments along dimension 0 after expanding them, so ``edge_index`` reaches
``set_masks`` with shape (1, E) rather than (2, E).

Integrated Gradients is the only method in the sweep that takes
``internal_batch_size``, which is exactly why Saliency, InputXGradient and
GuidedBackprop survived and it did not. Nothing in the audit could detect this:
the cell failed, was logged, and the run continued as designed.

These tests make the interaction visible before a run rather than after one.
"""
from __future__ import annotations

import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("torch_geometric")
captum = pytest.importorskip("captum")


def _captum_version() -> tuple[int, int]:
    parts = captum.__version__.split(".")
    return int(parts[0]), int(parts[1])


def test_captum_is_new_enough_for_pygs_explainer():
    """A version this test rejects would fail every IG molecule at runtime."""
    assert _captum_version() >= (0, 7), (
        f"captum {captum.__version__} is incompatible with PyG's "
        "CaptumExplainer and will fail every Integrated Gradients cell. "
        "Something installed DIG's captum==0.2.0 pin; reinstall with "
        "'pip install -U captum>=0.7' and install DIG with --no-deps."
    )


def _fixture():
    from molsanity.attributors import build_attributor
    from molsanity.data.synthetic import generate_synth_motifs
    from molsanity.models import build_backbone

    g = generate_synth_motifs(num_graphs=2, num_nodes=12, seed=0)[0]
    model = build_backbone("GINE", g, {"hidden_channels": 16, "num_layers": 2,
                                       "task": "graph-classification",
                                       "out_channels": 2})
    model.eval()
    return g, model


@pytest.mark.parametrize("method", ["IntegratedGradients", "Saliency",
                                    "InputXGradient"])
def test_gradient_attributors_produce_a_score_per_atom(method):
    """The end-to-end check the failed run needed and did not have.

    Integrated Gradients is parametrised alongside two methods that were never
    affected, so a failure here localises to the batching path rather than to
    the wrapper.
    """
    from molsanity.attributors import build_attributor

    g, model = _fixture()
    attr = build_attributor(method, model, task="graph-classification",
                            ig_steps=5)
    attr.edge_dim = g.edge_attr.size(1)
    out = attr.attribute(g)

    assert out.node_attr.shape == (int(g.num_nodes),)
    assert out.method == method
    assert bool((out.node_attr != 0).any()), (
        "an all-zero attribution is what a silently broken adapter returns")


def test_subgraphx_import_does_not_need_digs_package_init():
    """SubgraphX must load without DeepLIFT, GradCAM, or torch_sparse.

    DIG's ``__init__`` imports every explainer it ships, two of which reach
    into Captum internals that were removed after 0.2. Importing through it is
    what forced the downgrade in the first place.
    """
    pytest.importorskip("dig", reason="DIG (dive-into-graphs) not installed")
    from molsanity.attributors.subgraphx import _import_subgraphx

    SubgraphX = _import_subgraphx()
    assert SubgraphX.__module__ == "dig.xgraph.method.subgraphx"
    assert _captum_version() >= (0, 7), (
        "importing SubgraphX must not require an old Captum")


def test_preflight_refuses_to_start_a_run_quietly_on_a_broken_stack(monkeypatch,
                                                                   caplog):
    """Six hours is too long to wait to find out Captum was downgraded."""
    import logging

    from molsanity.run_all import preflight

    monkeypatch.setattr(captum, "__version__", "0.2.0")
    log = logging.getLogger("molsanity.test.preflight")
    with caplog.at_level(logging.WARNING):
        warnings = preflight({"cells": [{"attributor": "IntegratedGradients"}]},
                             log)

    assert warnings, "a downgraded captum must be reported before the run"
    assert "captum 0.2.0" in warnings[0]
    assert "IntegratedGradients" in warnings[0]
    assert "--no-deps" in warnings[0], "the message must say how to fix it"
    assert any("PREFLIGHT" in r.getMessage() for r in caplog.records)


def test_preflight_is_quiet_when_the_stack_is_good():
    import logging

    from molsanity.run_all import preflight

    assert preflight({"cells": [{"attributor": "IntegratedGradients"}]},
                     logging.getLogger("molsanity.test.preflight")) == []


def test_preflight_ignores_dependencies_the_config_does_not_use(monkeypatch):
    """A config with no gradient cells must not be warned about Captum."""
    import logging

    from molsanity.run_all import preflight

    monkeypatch.setattr(captum, "__version__", "0.2.0")
    assert preflight({"cells": [{"attributor": "GNNExplainer"}]},
                     logging.getLogger("molsanity.test.preflight")) == []


def test_digs_shapley_loader_does_not_pin_device_tensors():
    """The bug that failed all 18 SubgraphX cells on the GPU run.

    DIG's Shapley value function iterates a PyG ``DataLoader`` over subgraphs
    that already live on the compute device. Where the installed Torch pins by
    default, the first rollout raises ``cannot pin 'torch.cuda.FloatTensor'``.
    """
    pytest.importorskip("dig", reason="DIG (dive-into-graphs) not installed")
    from molsanity.attributors.subgraphx import _import_subgraphx

    _import_subgraphx()
    from dig.xgraph.method import shapley

    loader = shapley.DataLoader([], batch_size=2, pin_memory=True)
    assert loader.pin_memory is False, (
        "pin_memory must be forced off; DIG passes device-resident tensors")
