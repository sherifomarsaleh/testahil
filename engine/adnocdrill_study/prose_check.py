#!/usr/bin/env python3
"""ADNOCDRILL — every percentage and multiple in the delivered documents, reconciled.

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
            # the workbook's filename carries its date WITHOUT dashes (..._09082026.xlsx)
            m = re.findall(r'(\d{2})-?(\d{2})-?(\d{4})', f)
            c.append(((m[-1][2] + m[-1][1] + m[-1][0]) if m else '', f))
    return sorted(c)[-1][1] if c else None


# THE WORKBOOK IS A DELIVERED DOCUMENT AND WAS IN NO STUDY'S POPULATION IN THE BOOK [L-350]. A
# reader receives three files and this list named two, so the third was scanned by nothing.
# prose_figures.texts_of() reads a workbook's STRING cells only: a numeric cell is a model
# output the recalculation gate already reconciles, and a numeral inside a label is prose
# that happens to live in a spreadsheet.
DOCS = [d for d in (latest(r'.*Valuation_Study_.*\.docx$'), latest(r'.*(?:Bibliograph|Source).*\.docx$'),
                    latest(r'.*Valuation_Model_.*\.xlsx$'),) if d]

SN = json.load(open('study_numbers.json'))
# THE SPOT WAS None AND EVERY DISTANCE-FROM-PRICE FIGURE WENT UNMATCHED [09-09-2026].
# Both helpers below take the spot as their denominator, so with None they produced
# nothing at all: ratios_against((None,)) is empty and the _PANEL guard is False. The
# machinery was present, wired and dead, and 14 of this study's unmatched figures were
# the headline gap and the sensitivity table's "change against the base" — ratios of
# committed numbers that no committed number equals. A checker whose denominator is None
# is not a lenient checker; it is a checker that is not running.
_spot = SN['market']['spot_aed']
assert isinstance(_spot, (int, float)) and _spot > 0, _spot
vals = PF.numbers_from(HERE)
# every lens, expert and scenario is quoted as a DISTANCE from the price, and a ratio of
# two committed numbers is not itself committed
vals += PF.ratios_against(PF.numbers_from(HERE, files=['study_numbers.json']), (_spot,))
# and the reads are quoted against each other
_PANEL = [v for v in PF.numbers_from(HERE, files=['study_numbers.json']) if _spot and 0 < v < _spot * 5]
vals += PF.ratios_against([_spot] if _spot else [], _PANEL)

# AND AGAINST THE FIGURES A TABLE DIVIDES BY. The segment table quotes each segment's
# share of revenue and its EBITDA margin — ratios of committed numbers against a committed
# denominator that is not the price, which the two helpers above do not reach. The
# denominators are named rather than inferred: a checker that models what a document ought
# to divide by is checking a different document.
_DENOMS = [v.get('revenue') for v in (SN.get('history') or {}).values()
           if isinstance(v, dict) and isinstance(v.get('revenue'), (int, float))]
assert _DENOMS, 'no audited revenue found to divide segment shares by'
vals += PF.ratios_against(PF.numbers_from(HERE, files=['study_numbers.json']), _DENOMS)

RENDER = PF.rendering_set(vals)

if __name__ == '__main__':
    checked, problems = PF.check(DOCS, RENDER)
    sys.exit(PF.report(checked, problems, 'ADNOCDRILL'))
