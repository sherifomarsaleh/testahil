#!/usr/bin/env python3
"""PHDC — every percentage and multiple in the delivered documents, reconciled.

The mechanism is engine/prose_figures.py, shared with every other study; what is declared
here is only what is genuinely this study's own.

A FALSE POSITIVE IS FIXED BY WIDENING THE RENDERING SET, NEVER BY DELETING THE FIGURE.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
os.chdir(HERE)
import prose_figures as PF                                             # noqa: E402


def latest(pat):
    c = []
    for f in os.listdir('.'):
        if re.match(pat, f) and not f.startswith('~$'):
            m = re.findall(r'(\d{2})-(\d{2})-(\d{4})', f)
            c.append(((m[-1][2] + m[-1][1] + m[-1][0]) if m else '', f))
    return sorted(c)[-1][1] if c else None


DOCS = [d for d in (latest(r'PHDC_Valuation_Study_.*\.docx$'),
                    latest(r'PHDC_Bibliograph.*\.docx$')) if d]

SN = json.load(open('study_numbers.json'))
_spot = SN.get('spot')
vals = PF.numbers_from(HERE)
# every lens and case is quoted as a DISTANCE from the price
vals += PF.ratios_against(PF.numbers_from(HERE, files=['study_numbers.json']), (_spot,))
# and the lenses are quoted against each other
_LENS = [v for v in [SN['lens_record']['primary'].get('value')]
         if isinstance(v, (int, float))]
_LENS += [c.get('value') for c in SN['lens_record'].get('cross_checks', [])
          if isinstance(c.get('value'), (int, float))]
vals += PF.ratios_against(_LENS, _LENS)

RENDER = PF.rendering_set(vals)

if __name__ == '__main__':
    checked, problems = PF.check(DOCS, RENDER)
    sys.exit(PF.report(checked, problems, 'PHDC'))
