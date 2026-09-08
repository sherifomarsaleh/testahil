#!/usr/bin/env python3
"""DU — every percentage and multiple in the delivered documents, reconciled.

The mechanism is engine/prose_figures.py, shared with every other study; what is declared
here is only what is genuinely this study's own: which documents a reader receives, and
which figures may legitimately be quoted against something other than a model output.

A FALSE POSITIVE IS FIXED BY WIDENING THE RENDERING SET, NEVER BY DELETING THE FIGURE FROM
THE STUDY. If a figure is real and the model cannot produce it, the model is what is
missing.
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
    """The edition a reader receives, by the date in the filename [L-067]."""
    c = []
    for f in os.listdir('.'):
        if re.match(pat, f) and not f.startswith('~$'):
            m = re.findall(r'(\d{2})-(\d{2})-(\d{4})', f)
            c.append(((m[-1][2] + m[-1][1] + m[-1][0]) if m else '', f))
    return sorted(c)[-1][1] if c else None


DOCS = [d for d in (latest(r'.*Valuation_Study_.*\.docx$'), latest(r'.*(?:Bibliograph|Source).*\.docx$'),) if d]

SN = json.load(open('study_numbers.json'))
_spot = SN['spot']
vals = PF.numbers_from(HERE)
# every lens, expert and scenario is quoted as a DISTANCE from the price, and a ratio of
# two committed numbers is not itself committed
vals += PF.ratios_against(PF.numbers_from(HERE, files=['study_numbers.json']), (_spot,))
# and the reads are quoted against each other
_PANEL = [v for v in PF.numbers_from(HERE, files=['study_numbers.json']) if _spot and 0 < v < _spot * 5]
vals += PF.ratios_against([_spot] if _spot else [], _PANEL)

# EFFECTIVE FISCAL RATES ARE RATIOS OF COMMITTED NUMBERS AND ARE NOT THEMSELVES COMMITTED
# [widened 08-09-2026]. The source-discrepancy note quotes the FY2024 combined take on the
# ORIGINAL presentation basis — (royalty + tax) / profit before both — and the model holds
# all three components as four-field inputs but not their quotient. The widening is the fix
# the rule prescribes; deleting the figure from the register would have hidden a real
# discrepancy a checking reader is entitled to see.
_IV = {k: v['value'] for k, v in SN['inputs'].items() if isinstance(v.get('value'), (int, float))}
for _roy in ('royalty_fy23', 'royalty_fy24', 'royalty_fy24_original', 'royalty_fy25'):
    for _tax in ('tax_fy24', 'tax_fy25'):
        for _pbt in ('pbt_fy23', 'pbt_fy24', 'pbt_fy25'):
            if _roy in _IV and _tax in _IV and _pbt in _IV and _IV[_pbt]:
                vals.append((_IV[_roy] + _IV[_tax]) / _IV[_pbt])
                vals.append(_IV[_roy] / _IV[_pbt])

RENDER = PF.rendering_set(vals)

if __name__ == '__main__':
    checked, problems = PF.check(DOCS, RENDER)
    sys.exit(PF.report(checked, problems, 'DU'))
