#!/usr/bin/env python3
"""PHAR — build every artefact in dependency order, in one command.

WHY THIS EXISTS. Measured 13-09-2026: 23 of 25 studies had no single build entry point, so
reissuing one was a remembered sequence and whatever step was forgotten shipped stale with
every other gate green. This study's audit of the same day found its bibliography's judgements table contradicting the study of the same edition on
6 of 12 rows, from a hard-coded Python literal.

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

    ('strike_phar.py', 'strike_result.json', 'the price strike', True),
    ('step0.py', 'step0_result.json', 'Step 0.0, mandatory before any fit or study', True),
    ('beta_reg.py', 'beta_result.json', 'the sanctioned regression, now asserting on its own record', True),
    ('compute.py', 'study_numbers.json', 'the model — REBUILDS the numbers file'),
    ('far_year_ranges.py', 'far_year_ranges.json', 'the far-year ranges the document prints'),
    ('figures.py', '*.png', 'every figure, from the committed numbers'),
    ('docx_phar.py', 'the study', 'the delivered document'),
    ('docx_biblio.py', 'the bibliography', 'the standalone source register'),
    ('bake_docs_pdf.py', 'the study and bibliography PDFs', 'rendered FROM those documents, so it follows them — the PDF is the file a reader opens, and a rebuild that leaves it stale has not rebuilt the study'),
    ('build_xlsx_phar.py', 'the workbook', 'the delivered model'),
    ('recalc.py', None, 'an independent recalculation of that workbook'),
    ('driver_test.py', None, 'every live driver moves the answer'),
    ('prose_check.py', None, 'every figure in prose reconciled against the model'),
    ('footing_check.py', None, 'every total reproducible from its rows'),
    ('qc_checks.py', None, "the study's own delivered-document checks"),
    ('bridge_record.py', 'study_numbers.json (bridge_record)', 'APPENDS — after compute'),
]

if __name__ == '__main__':
    raise SystemExit(run(HERE, STEPS))
