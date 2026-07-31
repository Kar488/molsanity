"""The paper build's two gates: no undefined macros, no arXiv-hostile fonts.

Both exist because of failures that actually happened. The manuscript quotes
results only through macros generated from the committed data, which means a
passage can lose its macros the run after a finding stops reproducing -- and a
figure written by the audit run can carry Type 3 fonts that arXiv rejects while
every other figure in the same run is fine.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

FIGS = Path(__file__).resolve().parents[1] / "paper" / "figs"
sys.path.insert(0, str(FIGS))

check_macros = pytest.importorskip("check_macros")


LOG_WITH_UNDEFINED = r"""
This is XeTeX, Version 3.141592653
(./main.tex
[14] [15]
! Undefined control sequence.
l.881 ...ry audited molecule, including \degenCell
                                                  {}
! Undefined control sequence.
<recently read> \degenVal
l.882 ($\degenVal
                 {}$, $n=\degenN{}$). Zero between-molecule variance means the
[16]
Output written on main.pdf (18 pages).
"""

CLEAN_LOG = """
This is XeTeX, Version 3.141592653
(./main.tex
[1] [2] (./main.aux)
Output written on main.pdf (18 pages).
"""


def test_undefined_control_sequences_are_extracted_from_the_log():
    got = check_macros.undefined_control_sequences(LOG_WITH_UNDEFINED)
    assert got == ["degenCell", "degenVal"], got


def test_a_clean_log_reports_nothing():
    assert check_macros.undefined_control_sequences(CLEAN_LOG) == []


def test_each_name_is_reported_once():
    doubled = LOG_WITH_UNDEFINED + LOG_WITH_UNDEFINED
    assert check_macros.undefined_control_sequences(doubled) == [
        "degenCell", "degenVal"]


def test_fstring_built_macro_names_are_recognised():
    """``add(f"{pre}Best", ...)`` must make ``\\bbIndBest`` a known macro.

    Without this, the fifteen backbone-sweep macros that vanished when
    Integrated Gradients failed were reported as typos rather than as
    data-conditional, which points the reader at the wrong fix.
    """
    literal, patterns = check_macros.emittable_macro_names()
    assert "degenCell" in literal
    assert any(p.match("bbIndBest") for p in patterns), (
        "the f-string add() calls were not turned into patterns")
    assert any(p.match("bbShiftWorstVal") for p in patterns)
    # It must not match everything.
    assert not any(p.match("thisIsNotAMacroWeEmit") for p in patterns)


def test_newif_flags_count_as_defined():
    """A flag defines three control sequences, not one."""
    names = check_macros.defined_macro_names(
        "\\newif\\ifHasTox\n\\HasToxfalse\n\\newcommand{\\foo}{1}")
    assert {"ifHasTox", "HasToxtrue", "HasToxfalse", "foo"} <= names


def test_the_committed_manuscript_has_no_undefined_macros():
    """The real gate. Skipped where the paper has not been built."""
    log = FIGS.parent / "main.log"
    if not log.exists():
        pytest.skip("paper/main.log absent; run 'make -C paper' first")
    undefined = check_macros.undefined_control_sequences(
        log.read_text(errors="ignore"))
    assert undefined == [], (
        f"the manuscript quotes undefined macros: {undefined}. Guard the "
        "passage with a flag from add_flag() rather than defaulting them.")


def test_generated_macros_define_the_flags_the_prose_branches_on():
    """Every ``\\ifFoo`` in the prose must have a matching ``\\newif``."""
    import re

    paper = FIGS.parent
    macros = paper / "generated" / "macros.tex"
    if not macros.exists():
        pytest.skip("paper/generated/macros.tex absent; run 'make -C paper tables'")
    defined = check_macros.defined_macro_names(macros.read_text())
    body = (paper / "body.tex").read_text()
    used = set(re.findall(r"\\(ifHas[A-Za-z]+)", body))
    missing = sorted(f for f in used if f not in defined)
    assert not missing, f"prose branches on undefined flags: {missing}"
