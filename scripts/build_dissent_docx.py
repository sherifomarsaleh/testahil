#!/usr/bin/env python3
"""Render a study's MARKET_DISSENT markdown to the delivered .docx, then to PDF.

WHY THIS EXISTS. [R-GAP-02] makes a study past the publication limit write its case
before it may publish, and the case is the reader's, not the file system's. SWDY
published on 14-09-2026 with MARKET_DISSENT_14-09-2026.md filed, gating the publish
exactly as the rule intends — and with NOTHING on the ticker page pointing at it.
A reader on the site saw a fair value 35.4% below the market and no argument for it.
The document existed, was public in the repository, and was unreachable from the one
page a reader actually opens.

The dissent is written in markdown because it is written while the argument is being
made. The site surfaces PDFs. This closes that gap and nothing else: no content is
rewritten, no heading renamed, and the five headings [R-GAP-02] requires are carried
through exactly as filed.

    python3 scripts/build_dissent_docx.py SWDY
"""
from __future__ import annotations

import glob
import os
import re
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
import make_pdf  # noqa: E402  — the repo's own renderer, never a second copy


def _runs(par, text: str) -> None:
    """Write text into a paragraph, honouring **bold** and `code`."""
    for chunk in re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", text):
        if not chunk:
            continue
        if chunk.startswith("**") and chunk.endswith("**"):
            par.add_run(chunk[2:-2]).bold = True
        elif chunk.startswith("`") and chunk.endswith("`"):
            r = par.add_run(chunk[1:-1])
            r.font.name = "Consolas"
            r.font.size = Pt(9)
        else:
            par.add_run(chunk)


def build(ticker: str) -> str:
    tk = ticker.upper()
    sdir = os.path.join(ROOT, "engine", f"{tk.lower()}_study")
    hits = sorted(glob.glob(os.path.join(sdir, "MARKET_DISSENT_*.md")))
    if not hits:
        sys.exit(f"FAIL: {tk} has no MARKET_DISSENT_*.md in {sdir}")
    src = hits[-1]
    stamp = re.search(r"MARKET_DISSENT_(\d{2}-\d{2}-\d{4})\.md$", os.path.basename(src))
    if not stamp:
        sys.exit(f"FAIL: {os.path.basename(src)} carries no DD-MM-YYYY stamp")

    doc = Document()
    doc.styles["Normal"].font.name = "Calibri"
    doc.styles["Normal"].font.size = Pt(10.5)

    rows: list[list[str]] = []

    def flush_table() -> None:
        """Emit a collected markdown table, dropping its |---| separator row."""
        if not rows:
            return
        body = [r for r in rows if not re.match(r"^[\s|:-]+$", "|".join(r))]
        if body:
            t = doc.add_table(rows=len(body), cols=max(len(r) for r in body))
            t.style = "Table Grid"
            for i, row in enumerate(body):
                for j, cell in enumerate(row):
                    cell_par = t.rows[i].cells[j].paragraphs[0]
                    _runs(cell_par, cell.strip())
                    if i == 0:
                        for run in cell_par.runs:
                            run.bold = True
        rows.clear()

    for raw in open(src, encoding="utf-8").read().splitlines():
        line = raw.rstrip()
        if line.startswith("|"):
            rows.append(line.strip("|").split("|"))
            continue
        flush_table()
        if not line.strip() or line.strip() == "---":
            continue
        if line.startswith("### "):
            doc.add_heading(line[4:].strip(), level=3)
        elif line.startswith("## "):
            doc.add_heading(line[3:].strip(), level=2)
        elif line.startswith("# "):
            h = doc.add_heading(line[2:].strip(), level=1)
            h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif re.match(r"^[-*] ", line):
            _runs(doc.add_paragraph(style="List Bullet"), line[2:].strip())
        elif re.match(r"^\d+\. ", line):
            _runs(doc.add_paragraph(style="List Number"),
                  re.sub(r"^\d+\.\s*", "", line))
        else:
            _runs(doc.add_paragraph(), line.strip())
    flush_table()

    out = os.path.join(ROOT, "files", f"{tk}_Market_Dissent_{stamp.group(1)}.docx")
    doc.save(out)
    pdf = make_pdf.convert(out, os.path.join(ROOT, "files"))
    print(f"  built {os.path.relpath(out, ROOT)}")
    print(f"  built {os.path.relpath(pdf, ROOT)}")
    return pdf


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    build(sys.argv[1])
