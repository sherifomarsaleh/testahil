#!/usr/bin/env python3
"""AIRARABIA — every percentage and multiple in the delivered documents, reconciled.

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



def latest_ddmmyyyy(pat):
    """The workbook names its edition DDMMYYYY with no separators, so the date is PARSED
    rather than the filenames sorted as text — 03092026 sorts below 09082026 as a string and
    would pick the wrong file, the mistake the document resolver above records having made."""
    c = []
    for f in os.listdir('.'):
        if re.match(pat, f) and not f.startswith('~$'):
            m = re.findall(r'_(\d{2})(\d{2})(\d{4})_', f)
            c.append(((m[-1][2] + m[-1][1] + m[-1][0]) if m else '', f))
    return sorted(c)[-1][1] if c else None


# THE WORKBOOK IS A DELIVERED DOCUMENT AND WAS IN NO STUDY'S POPULATION IN THE BOOK [L-350].
# A reader receives three files and this list named two, so the third was read by nothing.
# prose_figures.texts_of() reads a workbook's STRING cells only: a numeric cell is a model
# output the recalculation gate already reconciles, and a numeral inside a label is prose
# that happens to live in a spreadsheet.
DOCS = [d for d in (latest(r'.*Valuation_Study_.*\.docx$'),
                    latest(r'.*(?:Bibliograph|Source).*\.docx$'),
                    latest_ddmmyyyy(r'.*Valuation_Model_\d{8}.*\.xlsx$')) if d]

SN = json.load(open('study_numbers.json'))
_spot = SN['spot']
vals = PF.numbers_from(HERE)
# every lens, expert and scenario is quoted as a DISTANCE from the price, and a ratio of
# two committed numbers is not itself committed
vals += PF.ratios_against(PF.numbers_from(HERE, files=['study_numbers.json']), (_spot,))
# and the reads are quoted against each other
_PANEL = [v for v in PF.numbers_from(HERE, files=['study_numbers.json']) if _spot and 0 < v < _spot * 5]
vals += PF.ratios_against([_spot] if _spot else [], _PANEL)
# INTRA-STATEMENT RATIOS. A study quotes an effective tax rate, a margin and a
# working-capital intensity constantly, and every one is a ratio of two committed
# figures IN THE SAME PERIOD — never a number the model stores on its own. The first
# runs of this check flagged the FY2024 audited effective rate of 8.79% (tax over
# profit before tax) and working capital at -66.6% of FY2025 revenue, both of which the
# model computes to the decimal. WIDENED RATHER THAN DELETED, which is the standing
# discipline for a false positive here: if a figure is real and the model can produce
# it, the rendering set is what was missing.
for _blk in ('hist_is', 'hist_bs'):
    for _yr, _row in (SN.get(_blk) or {}).items():
        if not isinstance(_row, dict):
            continue
        _dens = [_row.get(k) for k in ('rev', 'ebt', 'ebitda', 'assets', 'eqp')]
        _dens = [d for d in _dens if isinstance(d, (int, float)) and d]
        _nums = [v for v in _row.values() if isinstance(v, (int, float))]
        # revenue is the natural denominator for a balance-sheet intensity too
        _rev = ((SN.get('hist_is') or {}).get(_yr) or {}).get('rev')
        if isinstance(_rev, (int, float)) and _rev:
            _dens.append(_rev)
        vals += PF.ratios_against(_nums, tuple(_dens))

RENDER = PF.rendering_set(vals)

if __name__ == '__main__':
    checked, problems = PF.check(DOCS, RENDER)
    sys.exit(PF.report(checked, problems, 'AIRARABIA'))
