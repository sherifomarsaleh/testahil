#!/usr/bin/env python3
"""SCEM — build every artefact in dependency order, in one command.

WHY THIS EXISTS. Measured 13-09-2026: 23 of 25 studies had no single build entry point, so
reissuing one was a remembered sequence and whatever step was forgotten shipped stale with
every other gate green. This study's audit of the same day found nine figures built when the central was EGP 111.62 against a published 122.67,
and a masthead reading 'issued 7 September' on a 10 September edition.

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
    ('strike_scem.py', 'strike_result.json', 'the price strike', True),
    ('step0.py', 'step0_result.json', 'Step 0.0, mandatory before any fit or study', True),
    ('beta_reg.py', 'beta_result.json', 'the sanctioned regression, now asserting on its own record', True),
    ('filings_extract.py', 'filings_extract.json', 'the audited filings the model reads'),
    ('compute_bu.py', 'bottom_up.json', 'the unit build compute reads'),
    ('compute.py', 'study_numbers.json', 'the model — REBUILDS the numbers file'),
    ('diagnostics_scem.py', 'diagnostics.json', 'the reverse read; follows compute'),
    ('figures.py', '*.png', 'every figure, from the committed numbers'),
    ('docx_scem.py', 'the study', 'the delivered document'),
    ('docx_biblio.py', 'the bibliography', 'the standalone source register'),
    ('build_xlsx_scem.py', 'the workbook', 'the delivered model'),
    ('recalc.py', None, 'an independent recalculation of that workbook'),
    ('driver_test.py', None, 'every live driver moves the answer'),
    ('prose_check.py', None, 'every figure in prose reconciled against the model'),
    ('footing_check.py', None, 'every total reproducible from its rows'),
    ('gap_review_numbers.py', 'study_numbers.json (gap review)', 'APPENDS — after compute'),
]

if __name__ == '__main__':
    raise SystemExit(run(HERE, STEPS))
