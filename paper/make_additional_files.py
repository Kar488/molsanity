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


def tex_escape(s: str) -> str:
    for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"),
                 ("}", r"\}"), ("~", r"\textasciitilde{}"),
                 ("^", r"\textasciicircum{}")):
        s = s.replace(a, b)
    # Markdown emphasis survives into the report text; render it rather than
    # printing the asterisks.
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"`(.+?)`", r"\\texttt{\1}", s)
    return s


def si_pdf(path: Path) -> None:
    """Additional file 1: the narrative reports, typeset."""
    parts = [
        r"\documentclass[10pt,a4paper]{article}",
        r"\usepackage{fontspec}\setmainfont{TeX Gyre Pagella}",
        r"\usepackage[margin=2.4cm]{geometry}",
        r"\usepackage{booktabs,longtable,array,xcolor,hyperref}",
        r"\hypersetup{colorlinks=true,linkcolor=black,urlcolor=[HTML]{264E78}}",
        r"\setlength{\parskip}{5pt}\setlength{\parindent}{0pt}",
        r"\renewcommand{\arraystretch}{1.15}",
        r"\title{\vspace{-1.6cm}\bfseries Additional file 1: Supplementary "
        r"notes and summary tables}",
        r"\author{MolSanity: A Reliability Audit for Feature Attributions on "
        r"Molecular Graph Neural Networks}",
        r"\date{}",
        r"\begin{document}\maketitle",
        r"\noindent Every table and figure in this file is generated from the "
        r"committed artifacts of the single run reported in the manuscript, by "
        r"\texttt{paper/make\_additional\_files.py}. Additional files 2--4 "
        r"carry the full per-cell data in machine-readable form.\par\vspace{6pt}",
    ]
    for i, (report, label) in enumerate(
            [("BENCHMARK_GT.md", "Ground-truth benchmark by dataset and split"),
             ("RATIONALE_USE.md", "Does the model read the ground truth?"),
             ("ABSTENTION.md", "When not to trust an attribution")], start=1):
        text = (RESULTS / report).read_text()
        parts.append(rf"\section*{{S{i}\quad {tex_escape(label)}}}")
        for heading, header, rows in [(None, None, None)]:
            pass
        # Walk the report in order so prose and tables keep their sequence.
        buf, tbl = [], []
        def flush_prose():
            if buf:
                parts.append(tex_escape(" ".join(buf)))
                buf.clear()
        lines = text.splitlines()
        j = 0
        while j < len(lines):
            s = lines[j].strip()
            if s.startswith("#"):
                flush_prose()
                sub = s.lstrip("#").strip()
                if not sub.lower().startswith(report.split(".")[0].lower()):
                    parts.append(rf"\subsection*{{{tex_escape(sub)}}}")
                j += 1
                continue
            if s.startswith("|") and s.endswith("|"):
                flush_prose()
                tbl = []
                while j < len(lines) and lines[j].strip().startswith("|"):
                    cells = [c.strip() for c in lines[j].strip()[1:-1].split("|")]
                    if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                        tbl.append(cells)
                    j += 1
                if tbl:
                    ncol = len(tbl[0])
                    spec = "l" + "r" * (ncol - 1)
                    parts.append(rf"\begin{{longtable}}{{{spec}}}\toprule")
                    parts.append(" & ".join(
                        rf"\textbf{{{tex_escape(c)}}}" for c in tbl[0]) + r"\\\midrule\endhead")
                    for r in tbl[1:]:
                        r = (r + [""] * ncol)[:ncol]
                        parts.append(" & ".join(tex_escape(c) for c in r) + r"\\")
                    parts.append(r"\bottomrule\end{longtable}")
                continue
            if s.startswith("---"):
                j += 1
                continue
            if s.startswith("- "):
                flush_prose()
                parts.append(r"\begin{itemize}\itemsep2pt")
                while j < len(lines) and lines[j].strip().startswith("- "):
                    parts.append(r"\item " + tex_escape(lines[j].strip()[2:]))
                    j += 1
                parts.append(r"\end{itemize}")
                continue
            if not s:
                flush_prose()
                j += 1
                continue
            buf.append(s)
            j += 1
        flush_prose()

    parts.append(r"\section*{S4\quad Machine-readable additional files}")
    parts.append(r"\begin{itemize}\itemsep3pt")
    for n, ext, title, desc, _src in FILES:
        if ext != "csv":
            continue
        parts.append(rf"\item \textbf{{Additional file {n}}} "
                     rf"(\texttt{{Additional\_file\_{n}.csv}}) --- "
                     rf"{tex_escape(title)}. {tex_escape(desc)}")
    parts.append(r"\end{itemize}")
    parts.append(r"\end{document}")

    tex = OUT / f"{path.stem}.tex"
    tex.write_text("\n".join(parts) + "\n")
    for _ in range(2):
        r = subprocess.run(["xelatex", "-interaction=nonstopmode",
                            "-halt-on-error", tex.name],
                           cwd=OUT, capture_output=True, text=True)
    if not (OUT / f"{path.stem}.pdf").exists():
        sys.stdout.write(r.stdout[-3000:])
        raise SystemExit("Additional file 1 did not compile")
    for junk in OUT.glob(f"{path.stem}.*"):
        if junk.suffix not in (".pdf", ".tex"):
            junk.unlink()


def latex_sources(zip_path: Path) -> None:
    """The editable manuscript upload: sources plus figures, flat, zipped."""
    stage = OUT / "_latex"
    if stage.exists():
        shutil.rmtree(stage)
    (stage / "figs").mkdir(parents=True)
    (stage / "generated").mkdir()
    for name in ("main.tex", "body.tex", "abstract.tex"):
        shutil.copy2(HERE / name, stage / name)
    for f in sorted((HERE / "generated").glob("*.tex")):
        shutil.copy2(f, stage / "generated" / f.name)
    for f in sorted((HERE / "figs").glob("*.pdf")):
        shutil.copy2(f, stage / "figs" / f.name)
    readme = stage / "README.txt"
    readme.write_text(
        "MolSanity -- LaTeX sources for peer review.\n\n"
        "Compile with XeLaTeX (twice, for cross-references):\n"
        "    xelatex main.tex && xelatex main.tex\n\n"
        "XeLaTeX is required: main.tex uses fontspec to set TeX Gyre Pagella,\n"
        "so the document will NOT build under pdfLaTeX. TeX Gyre Pagella ships\n"
        "with TeX Live; if it is unavailable, delete the \\setmainfont line in\n"
        "main.tex and the document falls back to the default serif.\n\n"
        "generated/*.tex hold every number, table and macro quoted in the\n"
        "manuscript. They are produced from the committed results by\n"
        "paper/figs/make_tables.py and are included here so the sources build\n"
        "standalone, without the results directory.\n")
    if zip_path.exists():
        zip_path.unlink()          # zip appends; a stale archive would merge
    shutil.make_archive(str(zip_path.with_suffix("")), "zip", stage)
    shutil.rmtree(stage)


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
    latex_sources(OUT / "molsanity_latex_sources.zip")
    print(f"  molsanity_latex_sources.zip: manuscript upload (XeLaTeX)")
    over = [f.name for f in OUT.iterdir()
            if f.is_file() and f.stat().st_size > 20 * 1024 * 1024]
    if over:
        raise SystemExit(f"over BMC's 20 MB per-file limit: {over}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
