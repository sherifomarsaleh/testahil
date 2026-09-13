#!/usr/bin/env python3
"""EGCH — build every artefact in dependency order, in one command.

WHY THIS EXISTS. Measured 13-09-2026: 23 of 25 studies had no single build entry point, so
reissuing one was a remembered sequence and whatever step was forgotten shipped stale with
every other gate green. This study's audit of the same day found its two branches named everywhere and defined nowhere, and an export levy it
reported repealed on a source that does not verify.

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

    ('strike_egch.py', 'strike_result.json', 'the price strike'),
    ('step0.py', 'step0_result.json', 'Step 0.0, mandatory before any fit or study'),
    ('beta_record.py', 'beta_result.json', 'the sanctioned regression'),
    ('inputs.py', 'input_register.json', 'the four-field input register the model reads'),
    ('compute.py', 'study_numbers.json', 'the model — REBUILDS the numbers file'),
    ('lenses.py', 'lenses.json', 'the lens set; reads the numbers'),
    ('alternatives.py', 'alternatives.json', 'the contested alternatives, priced'),
    ('sensitivity.py', 'sensitivity_grid.json', 'the grids'),
    ('experts.py', 'experts.json', 'the expert panel'),
    ('band_record.py', 'band_record.json', 'the resolved-forecast band record'),
    ('tech.py', 'technicals.json', 'the shipped technical read'),
    ('diagnostics_egch.py', 'diagnostics.json', 'the reverse read; follows compute'),
    ('figures.py', '*.png', 'every figure, from the committed numbers'),
    ('docx_egch.py', 'the study', 'the delivered document'),
    ('docx_biblio.py', 'the bibliography', 'the standalone source register'),
    ('build_xlsx.py', 'the workbook', 'the delivered model'),
    ('bake_model_pdf.py', 'the workbook PDF', 'rendered FROM the workbook'),
    ('recalc.py', None, 'an independent recalculation of that workbook'),
    ('driver_test.py', None, 'every live driver moves the answer'),
    ('prose_check.py', None, 'every figure in prose reconciled against the model'),
    ('footing_check.py', None, 'every total reproducible from its rows'),
    ('attest.py', 'attestation.json', 'the model-study attestation'),
    ('coc_record.py', 'study_numbers.json (cost_of_capital_record)', 'APPENDS — after compute'),
    ('asset_base_record.py', 'study_numbers.json (asset_base_record)', '[R-ASSET-01]; APPENDS, so last'),
]

if __name__ == '__main__':
    raise SystemExit(run(HERE, STEPS))
