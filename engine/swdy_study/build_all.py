#!/usr/bin/env python3
"""SWDY — build every artefact in dependency order, in one command.

WHY THIS EXISTS. Measured 13-09-2026: 23 of 25 studies had no single build entry point, so
reissuing one was a remembered sequence and whatever step was forgotten shipped stale with
every other gate green. This study's audit of the same day found qc_checks.py and driver_test.py both opening the 05-08-2026 edition, certifying
a document and a workbook no reader receives.

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
    ('strike_swdy.py', 'strike_result.json', 'the price strike', True),
    ('step0.py', 'step0_result.json', 'Step 0.0, mandatory before any fit or study', True),
    ('beta_reg.py', 'beta_result.json', 'the sanctioned regression, now asserting on its own record', True),
    ('compute.py', 'study_numbers.json', 'the model — REBUILDS the numbers file'),
    ('figures.py', '*.png', 'every figure, from the committed numbers'),
    ('docx_swdy.py', 'the study', 'the delivered document'),
    ('docx_register.py', 'the bibliography', 'the standalone source register'),
    ('bake_docs_pdf.py', 'the study and bibliography PDFs', 'rendered FROM those documents, so it follows them — the PDF is the file a reader opens, and a rebuild that leaves it stale has not rebuilt the study'),
    ('build_xlsx_swdy.py', 'the workbook', 'the delivered model'),
    ('bake_model_pdf.py', 'the workbook PDF', 'rendered FROM the workbook'),
    ('recalc.py', None, 'an independent recalculation of that workbook'),
    ('driver_test.py', None, 'every live driver moves the answer'),
    ('prose_check.py', None, 'every figure in prose reconciled against the model'),
    ('footing_check.py', None, 'every total reproducible from its rows'),
    ('coc_record.py', 'study_numbers.json (cost_of_capital_record)', 'APPENDS — after compute'),
    ('bridge_record.py', 'study_numbers.json (bridge_record)', 'APPENDS — after compute'),
    ('forecast_anchor.py', 'study_numbers.json (forecast_anchor)', 'APPENDS — after compute'),
    # THE TWO STANDING HARD GATES, WHICH THIS STUDY CALLED NOWHERE. qc_checks records
    # the evidence attest.py then holds the checklist against, so it runs first; both
    # run LAST, on the delivered artefacts, because that is what a reader receives.
    ('qc_checks.py', 'qc_checks.json', 'the automated document QC, now RECORDING its findings'),
    ('attest.py', 'attestation.json', 'assert_model_study, assert_sigcm, assert_beta_provenance and the ground-up driver record'),
]

if __name__ == '__main__':
    raise SystemExit(run(HERE, STEPS))
