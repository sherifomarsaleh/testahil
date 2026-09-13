#!/usr/bin/env python3
"""ADIB — build every artefact in dependency order, in one command.

WHY THIS EXISTS. Measured 13-09-2026: 23 of 25 studies had no single build entry point, so
reissuing one was a remembered sequence and whatever step was forgotten shipped stale with
every other gate green. This study's audit of the same day found that it committed none of the standard records, and a masthead stating no edition
date at all.

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

    ('strike_adib.py', 'strike_result.json', 'the price strike'),
    ('beta_sanctioned.py', 'beta_sanctioned.json', 'the sanctioned beta record'),
    ('build_records.py', 'study_numbers.json', "the model's records — REBUILDS the numbers file"),
    ('gap_review.py', 'gap_review_numbers.json', "the [R-GAP-01] review's own arithmetic"),
    ('docx_adib.py', 'the study', 'the delivered document'),
    ('docx_biblio.py', 'the bibliography', 'the standalone source register'),
    ('build_xlsx_adib.py', 'the workbook', 'the delivered model'),
    ('bake_model_pdf.py', 'the workbook PDF', 'rendered FROM the workbook'),
    ('recalc.py', None, 'an independent recalculation of that workbook'),
    ('prose_check.py', None, 'every figure in prose reconciled against the model'),
    ('footing_check.py', None, 'every total reproducible from its rows'),
    ('gates.py', None, 'the four standing assertions'),
]

if __name__ == '__main__':
    raise SystemExit(run(HERE, STEPS))
