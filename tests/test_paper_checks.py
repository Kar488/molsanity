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


def _macros() -> dict[str, str]:
    import re

    path = Path(__file__).resolve().parents[1] / "paper" / "generated" / "macros.tex"
    if not path.exists():
        pytest.skip("paper macros not generated")
    return dict(re.findall(r"\\newcommand\{\\(\w+)\}\{(.*)\}", path.read_text()))


def _num(s: str) -> float:
    """Parse a macro value back to a number, undoing the LaTeX it carries."""
    s = s.replace("\\ensuremath{-}", "-").replace("\\ensuremath{", "")
    return float(s.rstrip("}").replace(",", "").replace("\\%", ""))


def test_paper_numbers_match_the_committed_artifacts():
    """A reviewer who clones the repo must find the paper's numbers in it.

    Every figure the manuscript quotes comes from a macro generated out of
    results/, so this cannot drift by hand-editing -- but it *can* drift if the
    generator and the published reports fall out of step, which is exactly what
    happened once already when BENCHMARK_GT.md kept a hard-coded conclusion
    while the data moved underneath it. This pins the headline numbers to the
    committed artifacts directly, not to the generator that produced them.
    """
    import glob
    import json

    root = Path(__file__).resolve().parents[1]
    M = _macros()

    gt_path = root / "results" / "BENCHMARK_GT.json"
    if not gt_path.exists():
        pytest.skip("no committed BENCHMARK_GT.json")
    by = {(r["dataset"], r["split"]): r for r in json.loads(gt_path.read_text())
          if "error" not in r}
    if ("MUTAG", "scaffold") not in by or ("MUTAG", "random") not in by:
        pytest.skip("committed run has no MUTAG regime pair")
    shift, ind = by[("MUTAG", "scaffold")], by[("MUTAG", "random")]

    assert _num(M["mutShiftRhoOccspearman"]) == pytest.approx(
        shift["rank_correlation"]["occ_spearman"]["rho"], abs=5e-4)
    assert _num(M["mutIndRhoOccspearman"]) == pytest.approx(
        ind["rank_correlation"]["occ_spearman"]["rho"], abs=5e-4)
    assert _num(M["mutShiftGtBestVal"]) == pytest.approx(
        shift["per_attributor"][shift["gt_best"]]["gt_auroc_mean"], abs=5e-4)
    assert M["mutShiftGtBest"].startswith(shift["gt_best"][:6])

    # The record count the abstract quotes must be the number of records on disk.
    n_disk = sum(len(json.loads(Path(f).read_text()))
                 for f in glob.glob(str(root / "results/artifacts/audit/*/records.json")))
    if n_disk:
        assert int(_num(M["nRecords"])) == n_disk, (
            f"abstract quotes {M['nRecords']} records, {n_disk} are committed")


def test_no_claim_survives_without_the_data_that_supports_it():
    """Data-conditional passages must be guarded by a flag, not by luck.

    Every \\ifHas... used in the body must be emitted by the generator. A
    passage guarded by a flag that no longer exists silently becomes
    unconditional prose describing a finding that may not be there.
    """
    import re

    root = Path(__file__).resolve().parents[1] / "paper"
    body = (root / "body.tex").read_text() + (root / "abstract.tex").read_text()
    used = set(re.findall(r"\\if(Has\w+)", body))
    if not used:
        pytest.skip("no conditional passages in the manuscript")
    macros_path = root / "generated" / "macros.tex"
    if not macros_path.exists():
        pytest.skip("paper macros not generated")
    declared = set(re.findall(r"\\newif\\if(Has\w+)", macros_path.read_text()))
    missing = sorted(used - declared)
    assert not missing, f"body uses undeclared conditionals: {missing}"


def test_prose_does_not_contradict_the_data():
    """Prose goes stale silently; the macro checker cannot see it.

    Every number in the manuscript is a generated macro, so a number can never
    drift. Sentences *about* those numbers can, and did: across three review
    rounds the paper still said it withdrew the regression cells (the operator
    was corrected and 0 of 12 are now negative), that SubgraphX "will populate
    the matrix on the next sweep" (it had), that BA-2Motifs was unscored (it is
    scored), and that each cell is a "single split, single seed" (three seeds,
    with a variance report). Each claim was true of an earlier run and false of
    the committed one.

    So: for a claim the data can settle, assert the data and the prose agree.
    """
    import re

    root = Path(__file__).resolve().parents[1] / "paper"
    body = (root / "body.tex").read_text() + (root / "abstract.tex").read_text()
    mac = root / "generated" / "macros.tex"
    if not mac.exists():
        pytest.skip("paper macros not generated")
    M = dict(re.findall(r"\\newcommand\{\\(\w+)\}\{(.*)\}", mac.read_text()))

    def val(name, default="0"):
        return _num(M.get(name, default))

    forbidden = []
    # (condition that makes the phrase false, phrase, what the data says)
    rules = [
        (val("nRegNeg") == 0, "withdraw its numbers",
         "nRegNeg = 0: the regression operator is corrected and no cell is negative"),
        (val("nRegNeg") == 0, "excluded from every\nfaithfulness claim",
         "nRegNeg = 0: the regression cells are no longer excluded"),
        (val("nPooledSeeds", "1") > 1, "Single split, single seed",
         f"nPooledSeeds = {M.get('nPooledSeeds')}"),
        (val("nPooledSeeds", "1") > 1, "one deterministic split at\none seed",
         f"nPooledSeeds = {M.get('nPooledSeeds')}"),
        (True, "will populate the matrix on the next sweep",
         "the sweep that populates it is the one being reported"),
        (True, "postdates this\nsweep", "the fix is in the committed sweep"),
        (True, "predate that\nfix", "the fix is in the committed sweep"),
    ]
    for stale, phrase, why in rules:
        if stale and phrase in body:
            forbidden.append(f"{phrase!r} -- but {why}")
    assert not forbidden, "prose contradicts the committed data:\n  " + "\n  ".join(forbidden)


def test_no_hand_typed_statistics_in_the_prose():
    """A statistic typed as a literal cannot go stale loudly -- only silently.

    Three review rounds after the sweep changed, the selection section still
    read "MUTAG strongly (+0.36 to -0.75)" while the macros, the table and the
    figure all said +0.143 to -0.643. Nothing caught it: the macro checker only
    sees macros that fail to expand, and a literal always expands.

    So the rule the paper already claims to follow is now enforced. Decimal
    literals are allowed only where they are a *definition* the code shares --
    a threshold, a percentile, a resample count -- and each such literal is
    listed here with the code that defines it. Anything else must be a macro.
    """
    import re

    root = Path(__file__).resolve().parents[1] / "paper"
    body = (root / "body.tex").read_text() + (root / "abstract.tex").read_text()

    # value -> where the same number is defined in code, so a reviewer can check
    ALLOWED = {
        "0.5": "chance AUROC; also the TwoSlopeNorm centre in make_figures.py",
        "0.05": "alpha, stats.bootstrap_ci / significance threshold",
        "0.9": "make_tables.py NAboveNine bunching threshold",
        "0.6": "make_tables.py nMotifInBand lower edge",
        "0.8": "audit threshold tau_c",
        "0.003": "GPU-vs-CPU GNNExplainer drift, measured and recorded in TASKS.md",
        "0.012": "GPU-vs-CPU GNNExplainer drift, measured and recorded in TASKS.md",
        "0.495": "figure width fraction, not a statistic",
    }
    # The bibliography is DOIs, arXiv ids and lengths, none of them results.
    text = body.split("\\begin{thebibliography}")[0]
    # Strip comments, \includegraphics options and URLs before looking.
    text = re.sub(r"(?<!\\)%.*", "", text)
    text = re.sub(r"\\includegraphics\[[^]]*\]", "", text)
    text = re.sub(r"\\(url|href)\{[^}]*\}", "", text)

    bad = []
    for lit in re.findall(r"(?<![0-9A-Za-z.=])[0-9]+\.[0-9]+", text):
        if lit not in ALLOWED:
            bad.append(lit)
    assert not bad, (
        "decimal literals in the manuscript that are not generated macros: "
        + ", ".join(sorted(set(bad)))
        + "\nEvery statistic must come from paper/generated/macros.tex. If one "
          "of these is a definition rather than a result, add it to ALLOWED "
          "with the code that defines it.")


def test_split_tables_lose_no_rows():
    """Splitting a table across floats is where rows go missing quietly.

    The ground-truth matrix was one oversized landscape float until it was
    split into three, and the molecular matrix into two. A reviewer reading
    the PDF reported the last table looked truncated -- it was not, but the
    only way to be sure is to count. Every row in the data must appear in
    exactly one float.
    """
    import re

    gen = Path(__file__).resolve().parents[1] / "paper" / "generated"
    if not (gen / "macros.tex").exists():
        pytest.skip("paper tables not generated")
    sys.path.insert(0, str(FIGS))
    D = pytest.importorskip("msdata")
    cls, reg = D.load_results()
    rows = list(cls) + list(reg)

    def emitted(pattern):
        n = 0
        for f in sorted(gen.glob(pattern)):
            t = f.read_text()
            if "\\midrule" not in t:
                continue
            body = t.split("\\midrule", 1)[1].split("\\bottomrule")[0]
            n += sum(1 for l in body.splitlines()
                     if "&" in l and l.strip().endswith("\\\\"))
        return n

    n_gt = sum(1 for r in rows if r.get("gt_auroc") is not None)
    assert emitted("tab_tier1_*.tex") == n_gt, (
        "ground-truth floats emit a different number of rows than the data has")


def test_no_selection_verdict_is_asserted_by_hand():
    """A verdict about a selection test must come from the record, not prose.

    This is the error that survived eight regenerations of the macro set. The
    manuscript said, of MUTAG on the random split, that occlusion rho and
    Fidelity+ "both select GuidedBP, which is also the ground-truth-best" --
    while the very table on the facing page, built from the same JSON, recorded
    all three metrics as mismatches, the occlusion pick at GT AUROC 0.037
    against GNNExplainer's 0.858, median paired gap 0.978, p < 0.001. Every
    *number* in the sentence was a generated macro and every number was right.
    The word that made it a claim -- "also" -- was typed, so nothing checked it,
    and the paper's headline ("in distribution it mostly does not") was built on
    top of it.

    A verdict phrase is only safe if it is derived. So: forbid the phrasings
    that assert agreement between a faithfulness pick and the ground truth, and
    require any such claim to be spelled with the mismatch-count macros, which
    are recomputed from the records on every build.
    """
    import re

    root = Path(__file__).resolve().parents[1] / "paper"
    body = " ".join((root / "body.tex").read_text().split())
    body += " " + " ".join((root / "abstract.tex").read_text().split())
    banned = [
        r"which is also the ground-?truth-?best",
        r"correctly (?:selects|picks|identifies) the ground-?truth-?best",
        r"(?:selects|picks) the ground-?truth-?best attributor",
        r"agrees with the ground truth on (?:all|every)",
        r"harmless in distribution",
        r"in distribution it mostly does not",
    ]
    hits = [p for p in banned if re.search(p, body, re.I)]
    assert not hits, (
        "the prose asserts a selection verdict instead of deriving it: "
        + "; ".join(hits)
        + "\nUse \\nSelMismatch/\\nSelMismatchInd/\\nSelMismatchShift, which are "
          "recomputed from the selection records on every build.")


def test_every_arm_the_prose_names_is_in_the_pooled_arm_set():
    """An arm excluded from the pool must not be argued from in the pool.

    Benzene and FluorideCarbonyl were audited for one reported sweep while
    sitting outside MOLECULAR_GT, because a loader bug made their scaffold
    splits degenerate. That exclusion was correct then and wrong the moment the
    loader was fixed -- an exclusion criterion that outlives its justification
    is a criterion applied to the result. This asserts the two lists agree: any
    dataset the selection table treats as a molecular ground-truth arm is also
    an arm the pooled estimate is computed over.
    """
    import importlib.util

    root = Path(__file__).resolve().parents[1] / "paper"
    if not (root / "generated" / "macros.tex").exists():
        pytest.skip("paper tables not generated")
    sys.path.insert(0, str(FIGS))
    pytest.importorskip("msdata")
    spec = importlib.util.spec_from_file_location(
        "make_tables", root / "figs" / "make_tables.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    arms = {ds for ds, _, _ in mod.ARMS}
    pooled = set(mod.MOLECULAR_GT) if hasattr(mod, "MOLECULAR_GT") else None
    if pooled is None:
        pytest.skip("MOLECULAR_GT is local to build(); checked via macros instead")
    assert arms <= pooled, (
        f"arms in the selection table but not the pooled estimate: {sorted(arms - pooled)}")


def test_the_pasted_abstract_matches_the_manuscript():
    """The abstract a reader sees first is the one nothing was checking.

    SUBMISSION.md carried a hand-pasted plain-text abstract for preprint
    servers and submission forms. It went stale silently -- still quoting a
    pooled correlation of -0.353 at p = 0.044 over 33 cells after the five-arm
    run had replaced those numbers -- and unlike the PDF nothing regenerated
    it. It is now generated from abstract.tex with the committed macros
    expanded; this asserts the copy on disk is what the generator produces.
    """
    import importlib.util
    import subprocess

    root = Path(__file__).resolve().parents[1] / "paper"
    gen = root / "make_submission_abstract.py"
    if not (root / "generated" / "macros.tex").exists():
        pytest.skip("paper macros not generated")
    r = subprocess.run([sys.executable, str(gen), "--check"],
                       capture_output=True, text=True, cwd=root)
    assert r.returncode == 0, r.stdout + r.stderr


def test_the_pasted_abstract_carries_no_latex():
    """A plain-text abstract with a stray \\macro in it is pasted as-is.

    Preprint forms take the text verbatim, so an unexpanded command or a
    leftover brace ships to readers. Cheap to assert, and the detex pass is
    regex-based, so it is worth asserting.
    """
    root = Path(__file__).resolve().parents[1] / "paper"
    md = (root / "SUBMISSION.md").read_text()
    head = "## Abstract (plain text)"
    if head not in md:
        pytest.skip("no plain-text abstract section")
    body = md.split(head, 1)[1].split("\n## ", 1)[0]
    bad = [tok for tok in ("\\", "{", "}", "$", "~") if tok in body]
    assert not bad, f"LaTeX leaked into the pasted abstract: {bad}"
