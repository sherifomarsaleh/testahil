#!/usr/bin/env python3
"""ARCC — build every artefact in dependency order, in one command.

WHY THIS EXISTS. Measured 13-09-2026: 23 of 25 studies had no single build entry point, so
reissuing one was a remembered sequence and whatever step was forgotten shipped stale with
every other gate green. This study's audit of the same day found four figures rendered against a central of 66.53 beside a summary table reading
77.18, and a workbook PDF printing 77.49 against the spreadsheet's 77.18.

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
    ('strike_arcc.py', 'strike_result.json', 'the price strike', True),
    ('step0.py', 'step0_result.json', 'Step 0.0, mandatory before any fit or study', True),
    ('beta_reg.py', 'beta_result.json', 'the sanctioned regression', True),
    ('sweep.py', 'sweep_register.json', 'the Step 2A information sweep, read by the model'),
    ('compute.py', 'study_numbers.json', 'the model — REBUILDS the numbers file'),
    ('efg_bridge.py', 'efg_bridge.json', 'the external-estimate bridge the document prints'),
    ('scenario_margin.py', 'scenario_margin.json', 'the margin scenarios'),
    ('diagnostics_arcc.py', 'diagnostics.json', 'the reverse read; follows compute'),
    ('figures.py', '*.png', 'every figure, from the committed numbers'),
    ('fig_efg_bridge.py', 'fig_efg_bridge.png', 'the bridge figure; follows efg_bridge.py'),
    ('docx_arcc.py', 'the study', 'the delivered document'),
    ('docx_biblio.py', 'the bibliography', 'the standalone source register'),
    ('build_xlsx_arcc.py', 'the workbook', 'the delivered model'),
    ('recalc.py', None, 'an independent recalculation of that workbook'),
    ('driver_test.py', None, 'every live driver moves the answer'),
    ('prose_check.py', None, 'every figure in prose reconciled against the model'),
    ('footing_check.py', None, 'every total reproducible from its rows'),
]

if __name__ == '__main__':
    raise SystemExit(run(HERE, STEPS))
