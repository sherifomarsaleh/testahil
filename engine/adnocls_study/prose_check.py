#!/usr/bin/env python3
"""ADNOCLS — every percentage and multiple in the delivered documents, reconciled.

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
_spot = SN['strike']['spot']
vals = PF.numbers_from(HERE)
# every lens, expert and scenario is quoted as a DISTANCE from the price, and a ratio of
# two committed numbers is not itself committed
vals += PF.ratios_against(PF.numbers_from(HERE, files=['study_numbers.json']), (_spot,))
# and the reads are quoted against each other
_PANEL = [v for v in PF.numbers_from(HERE, files=['study_numbers.json']) if _spot and 0 < v < _spot * 5]
vals += PF.ratios_against([_spot] if _spot else [], _PANEL)

# TWO FIGURES THAT ARE REAL AND ARE NOT MODEL OUTPUTS, DECLARED WITH THEIR REASONS. The
# rule is explicit that a false positive is fixed by widening the RENDERING SET and never
# by deleting the figure, and that each study declares which figures may legitimately be
# quoted against something other than a model output. Both below are sourced external
# facts cited in the text beside them; neither is produced by this model and neither
# should be.
RENDER = PF.rendering_set(vals, extra=[
    # the disclosed discount at which a twelve-month time charter was struck against the
    # spot rate in front of it — a market fact quoted from the company's own disclosure to
    # show what a counterparty willing to commit for a year actually paid. It is evidence
    # ABOUT the rate path rather than an output of it.
    -0.253,
    # Saudi Arabia's country risk premium on the agency credit-rating basis, cited beside
    # its swap basis to show that the two bases are not interchangeable. It is another
    # sovereign's figure, quoted from the country-risk file to make a point about basis
    # consistency, and this model has no reason to compute it.
    0.0501,
])

if __name__ == '__main__':
    checked, problems = PF.check(DOCS, RENDER)
    sys.exit(PF.report(checked, problems, 'ADNOCLS'))
