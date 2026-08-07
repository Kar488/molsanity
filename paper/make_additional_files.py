#!/usr/bin/env python3
"""Build the submission package in the form BMC/Journal of Cheminformatics asks for.

Two things the previous bundle got wrong.

First, the manuscript. The submission form takes an *editable* file: a Word
document, or LaTeX with figures compressed into a .zip which the publisher
compiles. A PDF is not a manuscript upload, so ``latex_sources`` emits the
sources and figures the compile service needs.

Second, the supplementary. Five raw ``.md`` files is not a BMC additional-file
set: they must be numbered ``Additional file N``, listed in the manuscript with
name/format/title/description, and cited in order in the text. BMC also asks
for datasets in a machine-readable format -- spreadsheets rather than PDFs --
so the split here is narrative to PDF, tables to CSV:

    Additional file 1  .pdf   supplementary notes and the small summary tables
    Additional file 2  .csv   per-cell audit matrix (the ground-truth rows)
    Additional file 3  .csv   across-seed mean/sd per cell
    Additional file 4  .csv   head-to-head benchmark incl. framework metrics

Everything is derived from results/, so the package cannot describe a different
run from the manuscript.

    python3 make_additional_files.py
"""
from __future__ import annotations

import csv
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
RESULTS = REPO / "results"
OUT = HERE / "submission"

# (number, extension, title, description, source report)
# Order is the order they are cited in the manuscript.
FILES = [
    (1, "pdf", "Supplementary notes and summary tables",
     "Ground-truth benchmark summary per dataset and split; the rationale-use "
     "partition testing the Faber objection; and the abstention "
     "coverage--reliability analysis, including the operating point that the "
     "10% below-chance target is not reachable at any coverage.",
     None),
    (2, "csv", "Per-cell audit matrix",
     "One row per (dataset, backbone, attributor, split, seed) combination: "
     "ground-truth localisation and AUPRC where node labels exist, occlusion "
     "faithfulness, motif coherence, Fidelity+/-, sparsity, calibration error "
     "and the predictive metrics. This is the table every figure and every "
     "quoted statistic in the manuscript is computed from.", "RESULTS.md"),
    (3, "csv", "Across-seed variance per cell",
     "Mean, standard deviation, minimum and maximum over the three seeds for "
     "every cell run under more than one seed. The spread here is the check on "
     "the single-seed selection tests of Table 5.", "SEED_VARIANCE.md"),
    (4, "csv", "Head-to-head benchmark including framework metrics",
     "Every audited cell scored on MolSanity's axes alongside the "
     "field-standard Fidelity+/-, sparsity, the GraphFramEx characterisation "
     "score and the PyG/DIG unfaithfulness metric, computed on the same "
     "molecules.", "BENCHMARK.md"),
]


def md_tables(text: str):
    """Every pipe table in a markdown report, as (heading, header, rows).

    Reports interleave prose, headings and tables, and a table's meaning comes
    from the heading above it -- SEED_VARIANCE has one table per metric under
    "## GT AUROC", "## occlusion rho" and so on. Dropping the heading would
    merge them into an unlabelled block.
    """
    tables, heading, header, rows = [], "", None, []

    def flush():
        nonlocal header, rows
        if header and rows:
            tables.append((heading, header, rows))
        header, rows = None, []

    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#"):
            flush()
            heading = s.lstrip("#").strip()
            continue
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in s[1:-1].split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                continue                      # the |---| alignment row
            if header is None:
                header = cells
            else:
                rows.append(cells)
            continue
        if not s:
            continue
        flush()
    flush()
    return tables


def write_csv(path: Path, report: str) -> int:
    """One CSV per report. A `section` column carries the table headings."""
    tables = md_tables((RESULTS / report).read_text())
    if not tables:
        raise SystemExit(f"no tables found in {report}")
    widest = max(tables, key=lambda t: len(t[1]))[1]
    n = 0
    with path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["section"] + widest)
        for heading, header, rows in tables:
            # Map each table's columns onto the widest header so one file can
            # hold the several tables a report emits without losing alignment.
            idx = {c: i for i, c in enumerate(header)}
            for r in rows:
                w.writerow([heading] + [
                    r[idx[c]] if c in idx and idx[c] < len(r) else ""
                    for c in widest])
                n += 1
    return n


UNICODE_TEX = {
    # Characters the report generators emit that a text serif has no glyph for.
    # The star marking the ground-truth-best attributor rendered as an empty
    # box in the first build of this file, which is the kind of defect nobody
    # notices until a reviewer opens the PDF.
    "\u2b50": r"$\star$", "\u2605": r"$\star$", "\u2606": r"$\star$",
    "\u2713": r"$\checkmark$", "\u2717": r"$\times$",
    "\u03c1": r"$\rho$", "\u03c3": r"$\sigma$", "\u0394": r"$\Delta$",
    "\u2248": r"$\approx$", "\u2264": r"$\leq$", "\u2265": r"$\geq$",
    "\u2192": r"$\rightarrow$", "\u2190": r"$\leftarrow$",
    "\u00b1": r"$\pm$", "\u00d7": r"$\times$", "\u2212": "-",
    "\u00b7": r"$\cdot$", "\u2014": "---", "\u2013": "--",
    "\u2018": "`", "\u2019": "'", "\u201c": "``", "\u201d": "''",
}


def tex_escape(s: str) -> str:
    """Markdown inline -> LaTeX, escaping first so markup cannot be eaten."""
    for a, b in (("\\", "\x00"), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"),
                 ("#", r"\#"), ("_", "\x01"), ("{", r"\{"), ("}", r"\}"),
                 ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}")):
        s = s.replace(a, b)
    # Emphasis is restored from the placeholders, so a literal underscore in a
    # column name survives while _italics_ still become italics. The first
    # build printed the markers verbatim: "_Faithfulness-only selection test_".
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    # Single-asterisk emphasis after double, or the greedy bold rule would eat
    # it. The reports use both: "the *ground truth* says is best" printed its
    # asterisks in the first build.
    s = re.sub(r"(?<!\*)\*(?!\s)([^*]+?)(?<!\s)\*(?!\*)", r"\\emph{\1}", s)
    s = re.sub(r"(?<![A-Za-z0-9])\x01(\S(?:.*?\S)?)\x01(?![A-Za-z0-9])",
               r"\\emph{\1}", s)
    s = re.sub(r"`(.+?)`", lambda m: r"\texttt{" + m.group(1) + "}", s)
    s = s.replace("\x01", r"\_").replace("\x00", r"\textbackslash{}")
    for ch, tex in UNICODE_TEX.items():
        s = s.replace(ch, tex)
    return s


def md_to_tex(text: str, drop_title: bool = True) -> list[str]:
    """One report's markdown as LaTeX, preserving the order of prose and tables."""
    out, buf, lines, i = [], [], text.splitlines(), 0

    def flush():
        if buf:
            out.append(tex_escape(" ".join(buf)))
            out.append("")
            buf.clear()

    while i < len(lines):
        s = lines[i].strip()
        if s.startswith("#"):
            flush()
            level, title = len(s) - len(s.lstrip("#")), s.lstrip("#").strip()
            if not (drop_title and level == 1):
                out.append(rf"\subsection*{{{tex_escape(title)}}}")
            i += 1
            continue
        if s.startswith("|") and s.endswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip()[1:-1].split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                out += tex_table(rows)
            continue
        if s.startswith("- ") or s.startswith("* "):
            flush()
            out.append(r"\begin{itemize}\itemsep2pt\parskip0pt")
            while i < len(lines) and lines[i].strip()[:2] in ("- ", "* "):
                out.append(r"\item " + tex_escape(lines[i].strip()[2:]))
                i += 1
            out.append(r"\end{itemize}")
            continue
        if s.startswith(">"):
            flush()
            # Consecutive quote lines are one paragraph. Emitting a quote
            # environment per line set each at its own \parskip, which read as
            # a double-spaced list rather than a block quotation.
            quoted = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quoted.append(lines[i].strip().lstrip("> ").strip())
                i += 1
            out.append(r"\begin{quote}\small " +
                       tex_escape(" ".join(q for q in quoted if q)) +
                       r"\end{quote}")
            continue
        if set(s) == {"-"} and len(s) >= 3:
            flush()
            out.append(r"\medskip\hrule\medskip")
            i += 1
            continue
        if not s:
            flush()
            i += 1
            continue
        buf.append(s)
        i += 1
    flush()
    return out


def tex_table(rows: list[list[str]]) -> list[str]:
    """A markdown table as LaTeX that stays inside the text block.

    Wide tables ran off the page in the first build -- the selection table lost
    its last two columns entirely. \\fitbox shrinks a box only when it is wider
    than the line, so narrow tables keep the body font and wide ones are scaled
    just enough to fit rather than uniformly squashed.
    """
    ncol = max(len(r) for r in rows)
    rows = [(r + [""] * ncol)[:ncol] for r in rows]
    # First column is a label, the rest are numbers.
    spec = "l" + "r" * (ncol - 1)
    body = [r"\fitbox{%", r"\footnotesize\setlength{\tabcolsep}{5pt}",
            rf"\begin{{tabular}}{{{spec}}}", r"\toprule",
            " & ".join(rf"\textbf{{{tex_escape(c)}}}" for c in rows[0]) +
            r" \\ \midrule"]
    for r in rows[1:]:
        body.append(" & ".join(tex_escape(c) for c in r) + r" \\")
    body += [r"\bottomrule", r"\end{tabular}}", r"\medskip", ""]
    return body


def si_pdf(path: Path) -> None:
    """Additional file 1: the narrative reports, typeset."""
    parts = [
        r"\documentclass[10pt,a4paper]{article}",
        r"\usepackage{fontspec}\setmainfont{TeX Gyre Pagella}",
        r"\usepackage{amssymb,amsmath}",
        r"\usepackage[margin=2.2cm]{geometry}",
        r"\usepackage{booktabs,array,graphicx,xcolor,hyperref}",
        r"\hypersetup{colorlinks=true,linkcolor=black,urlcolor=[HTML]{264E78}}",
        r"\setlength{\parskip}{5pt}\setlength{\parindent}{0pt}",
        r"\renewcommand{\arraystretch}{1.12}",
        r"\newsavebox{\fitb}",
        r"\newcommand{\fitbox}[1]{\sbox{\fitb}{#1}%",
        r"  \ifdim\wd\fitb>\linewidth",
        r"    \noindent\resizebox{\linewidth}{!}{\usebox{\fitb}}%",
        r"  \else\noindent\usebox{\fitb}\fi}",
        r"\title{\vspace{-1.8cm}\bfseries Additional file 1:\\"
        r"Supplementary notes and summary tables}",
        r"\author{\normalsize MolSanity: A Reliability Audit for Feature "
        r"Attributions on Molecular Graph Neural Networks}",
        r"\date{}",
        r"\begin{document}\maketitle\thispagestyle{empty}",
        r"\noindent Every table in this file is generated from the committed "
        r"artifacts of the single run reported in the manuscript, by "
        r"\texttt{paper/make\_additional\_files.py}. Additional files 2--4 "
        r"carry the full per-cell data in machine-readable form.",
        r"\tableofcontents\clearpage",
    ]
    sections = [("BENCHMARK_GT.md", "Ground-truth benchmark by dataset and split"),
                ("RATIONALE_USE.md", "Does the model read the ground truth?"),
                ("ABSTENTION.md", "When not to trust an attribution")]
    for i, (report, label) in enumerate(sections, start=1):
        parts.append(rf"\section*{{S{i}\quad {tex_escape(label)}}}")
        parts.append(rf"\addcontentsline{{toc}}{{section}}"
                     rf"{{S{i}\quad {tex_escape(label)}}}")
        parts += md_to_tex((RESULTS / report).read_text())
        # No forced page break between sections: two of the three are under a
        # page, and clearing after each left most of a sheet blank.

    n = len(sections) + 1
    parts.append(rf"\section*{{S{n}\quad Machine-readable additional files}}")
    parts.append(rf"\addcontentsline{{toc}}{{section}}"
                 rf"{{S{n}\quad Machine-readable additional files}}")
    parts.append(r"\begin{itemize}\itemsep3pt")
    for num, ext, title, desc, _src in FILES:
        if ext != "csv":
            continue
        parts.append(rf"\item \textbf{{Additional file {num}}} "
                     rf"(\texttt{{Additional\_file\_{num}.csv}}) --- "
                     rf"{tex_escape(title)} {tex_escape(desc)}")
    parts.append(r"\end{itemize}")
    parts.append(r"\end{document}")

    tex = OUT / f"{path.stem}.tex"
    tex.write_text("\n".join(parts) + "\n")
    r = None
    for _ in range(3):                     # three passes: the ToC needs two
        r = subprocess.run(["xelatex", "-interaction=nonstopmode",
                            "-halt-on-error", tex.name],
                           cwd=OUT, capture_output=True, text=True)
    if not (OUT / f"{path.stem}.pdf").exists():
        sys.stdout.write(r.stdout[-3000:])
        raise SystemExit("Additional file 1 did not compile")
    log = (OUT / f"{path.stem}.log").read_text(errors="ignore")
    bad = re.findall(r"Missing character: There is no (\S+)", log)
    if bad:
        raise SystemExit(
            "Additional file 1 has characters the font cannot set: "
            + ", ".join(sorted(set(bad))) + " -- add them to UNICODE_TEX")
    over = len(re.findall(r"Overfull \\hbox \((\d{3,})", log))
    if over:
        print(f"    note: {over} overfull boxes in the SI (>=100pt)")
    for junk in OUT.glob(f"{path.stem}.*"):
        if junk.suffix not in (".pdf", ".tex"):
            junk.unlink()


def latex_sources(zip_path: Path) -> int:
    """The editable manuscript upload: every source file, flat, zipped.

    Flat on purpose. Publisher compile services extract into a single working
    directory and are not reliable about nested paths, so the staged copies
    have their ``figs/`` and ``generated/`` prefixes stripped from every
    \\input and \\includegraphics. The repository keeps its subdirectories;
    only the archive is flattened, and the rewrite is verified by compiling
    the extracted archive rather than trusted.

    Only figures the manuscript actually includes are shipped: the repository
    builds one (fig_coverage) that no float references, and an unused file in
    a submission archive is a question a reviewer should not have to ask.
    """
    stage = OUT / "_latex"
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)

    src = {name: (HERE / name).read_text()
           for name in ("main.tex", "body.tex", "abstract.tex")}
    used_figs, used_inputs = set(), set()
    for text in src.values():
        used_figs |= {Path(m).name for m in re.findall(
            r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", text)}
        used_inputs |= {Path(m).name for m in re.findall(
            r"\\(?:input|include)\{([^}]+)\}", text)}

    def flatten(text: str) -> str:
        text = re.sub(r"(\\(?:input|include)\{)[^}]*/([^}]+\})", r"\1\2", text)
        return re.sub(r"(\\includegraphics(?:\[[^\]]*\])?\{)[^}]*/([^}]+\})",
                      r"\1\2", text)

    for name, text in src.items():
        (stage / name).write_text(flatten(text))
    for f in sorted((HERE / "generated").glob("*.tex")):
        if f.stem in used_inputs or f.name in used_inputs:
            shutil.copy2(f, stage / f.name)
    shipped = 0
    for f in sorted((HERE / "figs").glob("*.pdf")):
        if f.name in used_figs or f.stem in used_figs:
            shutil.copy2(f, stage / f.name)
            shipped += 1
    missing = {Path(x).name for x in used_figs} - {
        p.name for p in stage.iterdir()} - {
        p.stem for p in stage.iterdir()}
    if missing:
        raise SystemExit(f"figures referenced but not built: {sorted(missing)}")

    (stage / "README.txt").write_text(
        "MolSanity -- LaTeX sources for peer review.\n\n"
        "Compile with XeLaTeX (twice, for cross-references):\n"
        "    xelatex main.tex && xelatex main.tex\n\n"
        "XeLaTeX is required: main.tex uses fontspec to set TeX Gyre Pagella,\n"
        "so the document will NOT build under pdfLaTeX. TeX Gyre Pagella ships\n"
        "with TeX Live; if it is unavailable, delete the \\setmainfont line in\n"
        "main.tex and the document falls back to the default serif.\n\n"
        "All files are in one directory, with no subfolders to resolve.\n"
        "tab_*.tex and macros.tex hold every number and table quoted in the\n"
        "manuscript; they are generated from the committed results by\n"
        "paper/figs/make_tables.py and are included here so the sources build\n"
        "standalone. The bibliography is inline (thebibliography), so there is\n"
        "no .bib file and no BibTeX pass.\n")

    # Compile the staged tree exactly as the publisher will: a flat directory,
    # nothing else on the path. A rewrite that broke a path would otherwise
    # only surface after submission.
    for _ in range(2):
        r = subprocess.run(["xelatex", "-interaction=nonstopmode", "main.tex"],
                           cwd=stage, capture_output=True, text=True)
    log = (stage / "main.log").read_text(errors="ignore")
    for pattern, what in ((r"^! ", "errors"),
                          (r"Undefined control sequence", "undefined macros"),
                          (r"LaTeX Warning: Citation .* undefined", "undefined citations"),
                          (r"LaTeX Warning: Reference .* undefined", "undefined references"),
                          (r"File .* not found|Cannot find image", "missing files")):
        if re.search(pattern, log, re.M):
            sys.stdout.write(r.stdout[-2500:])
            raise SystemExit(f"the flattened source archive has {what}")
    pages = re.search(r"Output written on main\.pdf \((\d+) pages?\)", log)
    for junk in list(stage.glob("main.*")):
        if junk.suffix != ".tex":
            junk.unlink()

    if zip_path.exists():
        zip_path.unlink()          # zip appends; a stale archive would merge
    shutil.make_archive(str(zip_path.with_suffix("")), "zip", stage)
    shutil.rmtree(stage)
    return int(pages.group(1)) if pages else 0


def main() -> int:
    if not RESULTS.exists():
        raise SystemExit("results/ not found")
    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("Additional_file_*"):
        f.unlink()
    for n, ext, _title, _desc, src in FILES:
        target = OUT / f"Additional_file_{n}.{ext}"
        if ext == "csv":
            rows = write_csv(target, src)
            print(f"  {target.name}: {rows} rows from {src}")
        else:
            si_pdf(target)
            print(f"  {target.name}: {target.stat().st_size // 1024} KB")
    pages = latex_sources(OUT / "molsanity_latex_sources.zip")
    print(f"  molsanity_latex_sources.zip: manuscript upload, "
          f"compiles flat to {pages} pages (XeLaTeX)")
    over = [f.name for f in OUT.iterdir()
            if f.is_file() and f.stat().st_size > 20 * 1024 * 1024]
    if over:
        raise SystemExit(f"over BMC's 20 MB per-file limit: {over}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
