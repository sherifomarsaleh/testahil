#!/usr/bin/env python3
"""AMOC — build every artefact in dependency order, in one command.

WHY THIS EXISTS. Measured 13-09-2026: 23 of 25 studies had no single build entry point, so
reissuing one was a remembered sequence and whatever step was forgotten shipped stale with
every other gate green. This study's audit of the same day found four of five figures publishing EGP 11.40 while every table published 20.05.

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
    ('strike_amoc.py', 'strike_result.json', 'the price strike the cone is anchored on'),
    ('step0.py', 'step0_result.json', 'Step 0.0, mandatory before any fit or study'),
    ('beta_record.py', 'beta_result.json', 'the sanctioned regression against the published index'),
    ('compute.py', 'study_numbers.json', 'the model — and it REBUILDS the numbers file, so every append follows it'),
    ('diagnostics_amoc.py', 'diagnostics.json', 'the reverse read; it READS the numbers and must follow compute'),
    ('figures_v5.py', '*.png', 'every figure of the current edition, from the committed numbers'),
    ('docx_v6.py', 'the study', 'the delivered document'),
    ('docx_register.py', 'the bibliography', 'the standalone source register'),
    ('build_xlsx_v5.py', 'the workbook', 'the delivered model'),
    ('bake_model_pdf.py', 'the workbook PDF', 'rendered FROM the workbook, so it follows it'),
    ('recalc_v5.py', None, 'an independent recalculation of that workbook'),
    ('prose_check.py', None, 'every figure in prose reconciled against the model'),
    ('footing_check.py', None, 'every total reproducible from the rows above it'),
    ('scrub.py', None, 'the external-reader scrub of the delivered files'),
    ('asset_base_record.py', 'study_numbers.json (asset_base_record)', '[R-ASSET-01]; it APPENDS, so it is last'),
]

if __name__ == '__main__':
    raise SystemExit(run(HERE, STEPS))
