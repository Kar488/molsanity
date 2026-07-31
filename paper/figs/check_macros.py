#!/usr/bin/env python3
"""Turn 'Undefined control sequence' into a diagnosis.

    python paper/figs/check_macros.py [main.log]

The manuscript quotes results only through macros written by
``make_tables.py``, so no number is ever hand-typed. The failure mode that
creates is a macro whose *existence* depends on the data: a passage describing
a finding compiles for as long as the finding exists, and breaks the build the
run after a new sweep stops reproducing it.

That happened. The first single-seed run had two degenerate ground-truth cells
and emitted ``\\degenCell``; the three-seed run had none, emitted nothing, and
three paragraphs lost their macros. LaTeX reports that as ``Undefined control
sequence`` at line 881, which says nothing about the cause. Meanwhile the same
run lost every Integrated Gradients cell, which took ``\\bbIndBest`` and its
siblings with it, and Tox21 never loaded, which took ``\\toxAucMax``.

Worse than a broken build is the version that does not break: had those macros
carried defaults, the paragraphs would have compiled while describing cells
that no longer exist. So the fix is a flag from ``add_flag()`` and a
conditional in the prose, and this script names which macros need one.

It reads LaTeX's own log rather than parsing TeX, so there is no allowlist of
built-in control sequences to maintain and no false positives: if xelatex
accepted it, this script does not care about it.

Exit status is 0 when clean, 1 when the prose quotes macros the data no longer
supports.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
GENERATED = PAPER / "generated" / "macros.tex"
MAKE_TABLES = HERE / "make_tables.py"

# LaTeX prints the offending control sequence on the line after the error,
# as the tail of the partially-read line:
#     ! Undefined control sequence.
#     l.881 ...ry audited molecule, including \degenCell
# or, when the macro was consumed by another one:
#     <recently read> \degenVal
_ERROR_LINE = "! Undefined control sequence."
_TRAILING_CS = re.compile(r"\\([A-Za-z]+)\s*$")


def undefined_control_sequences(log_text: str) -> list[str]:
    """Every control sequence LaTeX reported as undefined, in order.

    Scanned line by line rather than with one regex over the whole log: the
    context lines after one error can contain the next error, and a pattern
    that consumes them swallows every second failure.
    """
    lines = log_text.splitlines()
    names: list[str] = []
    for i, line in enumerate(lines):
        if line.strip() != _ERROR_LINE:
            continue
        for follow in lines[i + 1:i + 4]:
            if follow.strip() == _ERROR_LINE:
                break
            found = _TRAILING_CS.search(follow)
            if found:
                names.append(found.group(1))
                break
    seen = set()
    return [n for n in names if not (n in seen or seen.add(n))]


def emittable_macro_names() -> tuple[set[str], list[re.Pattern]]:
    """What ``make_tables.py`` is capable of emitting.

    Returns the literal names, plus patterns for the names it builds with
    f-strings: ``add(f"{pre}Best", ...)`` becomes ``^[A-Za-z]+Best$``, which is
    how ``\\bbIndBest`` is recognised as a macro the script knows how to write
    rather than as a typo.
    """
    if not MAKE_TABLES.exists():
        return set(), []
    src = MAKE_TABLES.read_text()
    literal = set(re.findall(r"""\badd(?:_flag)?\(\s*["']([A-Za-z]+)["']""",
                             src))
    patterns = []
    for expr in re.findall(r"""\badd(?:_flag)?\(\s*f["']([^"']+)["']""", src):
        if "{" not in expr:
            continue
        # Literal runs stay literal; each {...} becomes one name-ish chunk.
        parts = re.split(r"\{[^{}]*\}", expr)
        if any(not re.fullmatch(r"[A-Za-z]*", p) for p in parts):
            continue  # not a plain macro name; skip rather than guess
        patterns.append(re.compile(
            "^" + "[A-Za-z]+".join(re.escape(p) for p in parts) + "$"))
    return literal, patterns


def defined_macro_names(text: str) -> set[str]:
    names = set(re.findall(r"\\(?:new|renew|provide)command\{?\\([A-Za-z]+)",
                           text))
    for flag in re.findall(r"\\newif\s*\\if([A-Za-z]+)", text):
        names |= {f"if{flag}", f"{flag}true", f"{flag}false"}
    return names


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    log_path = Path(argv[0]) if argv else PAPER / "main.log"
    if not log_path.exists():
        print(f"{log_path} does not exist; run the LaTeX build first.",
              file=sys.stderr)
        return 1

    undefined = undefined_control_sequences(
        log_path.read_text(errors="ignore"))
    if not undefined:
        n = len(defined_macro_names(GENERATED.read_text())) \
            if GENERATED.exists() else 0
        print(f"check_macros: no undefined control sequences "
              f"({n} generated macros available).")
        return 0

    literal, patterns = emittable_macro_names()
    generated = defined_macro_names(GENERATED.read_text()) \
        if GENERATED.exists() else set()

    def emittable(name: str) -> bool:
        return name in literal or any(p.match(name) for p in patterns)

    print(f"check_macros: {len(undefined)} undefined control sequence(s).\n",
          file=sys.stderr)
    data_conditional = []
    for name in undefined:
        if emittable(name):
            data_conditional.append(name)
            print(f"  \\{name}  -- make_tables.py can emit this but did not: "
                  f"the current results do not support it.", file=sys.stderr)
        elif name in generated:
            print(f"  \\{name}  -- defined in macros.tex; a load-order or "
                  f"grouping problem, not a data problem.", file=sys.stderr)
        else:
            print(f"  \\{name}  -- not a generated macro. Typo, or a missing "
                  f"package.", file=sys.stderr)

    if data_conditional:
        print("\nThese macros are conditional on the data. Do not give them "
              "defaults -- that produces prose describing findings that are "
              "not there. Emit a flag with add_flag() and wrap the passage:"
              "\n"
              "\n    \\ifHasThing ... \\else ... \\fi\n", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
