#!/usr/bin/env python3
"""AMOC — every percentage and multiple in the delivered documents, reconciled.

The mechanism is engine/prose_figures.py, shared with every other study. What is declared
here is only what is genuinely this study's own: which documents a reader receives, and
which figures may legitimately be quoted against something other than a model output.

WHAT THIS WOULD HAVE CAUGHT, on the day it was written: a 514-basis-point margin range
typed into section 1.12 against five filed periods whose actual spread is 737, and a
terminal share of 36% stated in an earlier edition against a computed 58%. Both reached
readers in a study that passed every other gate, because every other gate examines how a
number was BUILT rather than what the page says.

A FALSE POSITIVE IS FIXED BY WIDENING THE RENDERING SET, NEVER BY DELETING THE FIGURE.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
os.chdir(HERE)
import prose_figures as PF                                             # noqa: E402

DOCS = ['AMOC_Valuation_Study_03-09-2026_public.docx',
        'AMOC_Bibliography_03-09-2026.docx']

SN = json.load(open('study_numbers.json'))
vals = PF.numbers_from(HERE)

# The technical read is computed on the price library's last session and the study is
# struck on the latest known price. Those are two clocks, so a level quoted as a distance
# is measured against BOTH — the close the read itself states, and spot.
_tech = json.load(open('technicals.json')) if os.path.exists('technicals.json') else {}
_tclose = (_tech.get('close') if isinstance(_tech, dict) else None) or SN.get('spot')
vals += PF.relative_to(PF.numbers_from(HERE, files=['technicals.json']),
                       (_tclose, SN.get('spot')))

# Every lens, expert and scenario is quoted as a DISTANCE from the price, and a ratio of
# two committed numbers is not itself a committed number. Eleven of this check's first
# eighteen unmatched figures were exactly that shape and every one was correct.
vals += PF.ratios_against(PF.numbers_from(HERE, files=['study_numbers.json']),
                          (SN.get('spot'),))

RENDER = PF.rendering_set(vals, extra=[
    # the statutory rate and the tax basis a reader sees quoted directly
    SN['inputs']['tax_stat']['value'] if 'tax_stat' in SN['inputs'] else 0.225,
])

if __name__ == '__main__':
    checked, problems = PF.check([d for d in DOCS if os.path.exists(d)], RENDER)
    sys.exit(PF.report(checked, problems, 'AMOC'))
