#!/usr/bin/env python3
"""GBCO — build every artefact in dependency order, in one command.

WHY THIS EXISTS. Measured 13-09-2026: 23 of 25 studies had no single build entry point, so
reissuing one was a remembered sequence and whatever step was forgotten shipped stale with
every other gate green. This study's audit of the same day found its headline giving GB Auto a value that is not GB Auto's, Figure 2 printing
`nan` five times, and eight numerals typed into the builder while the record held them.

THE ORDER IS DECLARED, NOT DISCOVERED. Anything writing an INPUT precedes the builder that
reads it; anything APPENDING to study_numbers.json follows everything that REBUILDS it, or
the append is silently reverted [R-ENF-04]. The runner is engine/build_all_shared.py.

    python3 build_all.py            every step, in order
    python3 build_all.py --list     the declared order, run nothing
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from build_all_shared import run                                    # noqa: E402

STEPS = [

    ('compute.py', 'study_numbers.json', 'the model — REBUILDS the numbers file, so every append follows it'),
    ('rebuild_levers.py', 'study_numbers.json (rebuild ledger)', 'the lever ledger; it appends'),
    ('diagnostics_gbco.py', 'diagnostics.json', 'the reverse read; follows compute'),
    ('figures.py', '*.png', 'every figure, from the committed numbers'),
    ('build_docx.py', 'the study', 'assembles the delivered document from docx_A/B/C'),
    ('docx_biblio.py', 'the bibliography', 'the standalone source register'),
    ('bake_docs_pdf.py', 'the study and bibliography PDFs', 'rendered FROM those documents, so it follows them — the PDF is the file a reader opens, and a rebuild that leaves it stale has not rebuilt the study'),
    ('build_xlsx.py', 'the workbook, part 1', 'READ FIRST and Assumptions'),
    ('build_xlsx2.py', 'the workbook, part 2', "Segments and DCF — reads part 1's rows"),
    ('build_xlsx3.py', 'the workbook, part 3', 'the statements — reads parts 1-2'),
    ('build_xlsx4.py', 'the workbook, part 4', 'sheets in model-report order — reads parts 1-3'),
    ('bake_model_pdf.py', 'the workbook PDF', 'rendered FROM the workbook, so it follows it — check_artefact_freshness found this PDF a whole edition behind its own spreadsheet'),
    ('recalc.py', None, 'an independent recalculation of that workbook'),
    ('prose_check.py', None, 'every figure in prose reconciled against the model'),
    ('footing_check.py', None, 'every total reproducible from its rows'),
    ('scrub.py', None, 'the external-reader scrub of the delivered files'),
]

if __name__ == '__main__':
    raise SystemExit(run(HERE, STEPS))
