#!/usr/bin/env python3
"""Regenerate the plain-text abstract in SUBMISSION.md from abstract.tex.

The submission metadata carried a hand-pasted copy of the abstract. It drifted:
by the time the five-arm run landed it still quoted a pooled correlation of
-0.353 at p = 0.044 over 33 cells, numbers the manuscript no longer reports,
and it is the text that gets pasted into a preprint server -- the one version a
reader sees before the PDF. A copy that has to be kept in step by hand will not
be. So it is generated from abstract.tex with the committed macros expanded,
and a test asserts the file on disk matches what this script produces.

Run:  python3 make_submission_abstract.py        (rewrites SUBMISSION.md)
      python3 make_submission_abstract.py --check (exit 1 if stale)
"""
from __future__ import annotations

import re
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
ABSTRACT = HERE / "abstract.tex"
MACROS = HERE / "generated" / "macros.tex"
SUBMISSION = HERE / "SUBMISSION.md"
HEADING = "## Abstract (plain text)"
WIDTH = 78


def macro_table() -> dict[str, str]:
    """{name: value} for every \\newcommand in the generated macro file."""
    out = {}
    for name, val in re.findall(r"\\newcommand\{\\(\w+)\}\{(.*)\}",
                                MACROS.read_text()):
        out[name] = val
    return out


def _detex(s: str, macros: dict[str, str]) -> str:
    # Expand generated macros first, repeatedly: a macro value may itself be
    # \ensuremath{...}, which the LaTeX-stripping pass below has to see.
    for _ in range(6):
        before = s
        s = re.sub(r"\\(\w+)\{\}", lambda m: macros.get(m.group(1), m.group(0)), s)
        s = re.sub(r"\\(\w+)(?![\w{])",
                   lambda m: macros.get(m.group(1), m.group(0)), s)
        if s == before:
            break
    s = re.sub(r"\\ensuremath\{([^{}]*)\}", r"\1", s)
    # Citations and cross-references carry no meaning in a pasted abstract.
    s = re.sub(r"~?\\cite\{[^}]*\}", "", s)
    s = re.sub(r"\\S~?\\ref\{[^}]*\}", "the paper", s)
    s = re.sub(r"\\ref\{[^}]*\}", "", s)
    # Text-level markup: keep the words, drop the commands.
    for _ in range(6):
        before = s
        s = re.sub(r"\\(?:emph|textbf|textit|texttt|mathrm|text)\{([^{}]*)\}",
                   r"\1", s)
        if s == before:
            break
    replacements = {
        r"\times": "×", r"\pm": "+/-", r"\%": "%", r"\&": "&", r"\_": "_",
        r"\,": " ", r"\ ": " ", r"\small": "", r"\rho": "rho",
        "---": " - ", "--": "-", "``": '"', "''": '"',
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    s = s.replace("$", "")
    s = re.sub(r"\\[a-zA-Z]+", "", s)      # any command that survived
    s = s.replace("{", "").replace("}", "")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([,.;:)])", r"\1", s)
    s = re.sub(r"\(\s+", "(", s)
    return s


def render() -> str:
    body = ABSTRACT.read_text()
    body = body.replace(r"\textbf{Abstract.}", "")
    text = _detex(body, macro_table())
    return "\n".join(textwrap.wrap(text, WIDTH))


def splice(md: str, abstract: str) -> str:
    lines = md.splitlines()
    try:
        start = lines.index(HEADING)
    except ValueError:
        raise SystemExit(f"{SUBMISSION.name} has no {HEADING!r} section")
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[:start + 1] + ["", abstract, ""] + lines[end:]) + "\n"


def main() -> int:
    if not MACROS.exists():
        print("macros not generated; run figs/make_tables.py first")
        return 1
    want = splice(SUBMISSION.read_text(), render())
    if "--check" in sys.argv:
        if SUBMISSION.read_text() != want:
            print("SUBMISSION.md abstract is stale; run make_submission_abstract.py")
            return 1
        print("SUBMISSION.md abstract is current.")
        return 0
    SUBMISSION.write_text(want)
    print(f"  wrote {SUBMISSION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
