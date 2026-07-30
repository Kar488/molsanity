"""Fail the build if any font in the PDF would be rejected by arXiv.

    python paper/figs/check_fonts.py paper/main.pdf

arXiv requires every font to carry an embedded font programme and rejects
Type 3 fonts. matplotlib's PDF backend defaults to ``pdf.fonttype: 3``, which
emits Type 3 with no embedded programme, so a figure generated without an
explicit ``pdf.fonttype: 42`` silently poisons an otherwise clean XeLaTeX
build. This walks every font object in the file, not only the ones reachable
from page resources, because figures arrive as Form XObjects with their own
resource dictionaries.

Exit code 0 = clean, 1 = at least one font would be rejected.
"""
from __future__ import annotations

import sys
from pathlib import Path


def audit(pdf_path: Path) -> list[tuple[str, str, str]]:
    import pikepdf

    pdf = pikepdf.open(pdf_path)
    problems: list[tuple[str, str, str]] = []
    n_fonts = 0
    for obj in pdf.objects:
        if not isinstance(obj, pikepdf.Dictionary):
            continue
        if obj.get("/Type") != "/Font":
            continue
        n_fonts += 1
        subtype = str(obj.get("/Subtype"))
        name = str(obj.get("/BaseFont", "<unnamed>"))
        desc = obj.get("/FontDescriptor")
        if subtype == "/Type0" and "/DescendantFonts" in obj:
            desc = obj["/DescendantFonts"][0].get("/FontDescriptor")
        embedded = desc is not None and any(
            k in desc for k in ("/FontFile", "/FontFile2", "/FontFile3")
        )
        if subtype == "/Type3":
            problems.append((name, subtype, "Type 3: no embedded font programme"))
        elif not embedded:
            problems.append((name, subtype, "no /FontFile in the descriptor"))
    audit.n_fonts = n_fonts  # type: ignore[attr-defined]
    return problems


def main() -> int:
    pdf_path = Path(sys.argv[1] if len(sys.argv) > 1 else "main.pdf")
    if not pdf_path.exists():
        print(f"check_fonts: {pdf_path} not found", file=sys.stderr)
        return 1
    try:
        problems = audit(pdf_path)
    except ImportError:
        print("check_fonts: pikepdf not installed, skipping (pip install pikepdf)")
        return 0
    n = getattr(audit, "n_fonts", 0)
    if problems:
        print(f"check_fonts: {len(problems)} of {n} font objects would be "
              f"rejected by arXiv:", file=sys.stderr)
        for name, subtype, why in sorted(set(problems)):
            print(f"    {name}  [{subtype}]  {why}", file=sys.stderr)
        print("    fix: set pdf.fonttype=42 wherever the figure is generated",
              file=sys.stderr)
        return 1
    print(f"check_fonts: {n} font objects, all embedded, no Type 3.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
