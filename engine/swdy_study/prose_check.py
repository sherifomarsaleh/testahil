#!/usr/bin/env python3
"""SWDY — every percentage and multiple in the delivered documents, reconciled.

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

# NAMED RATIOS, NOT A CROSS PRODUCT. The first attempt at this widened the set with every
# pairwise ratio among the committed inputs and reported zero unmatched — and it was
# VACUOUS: 3,613,198 values, matching 400 of 400 RANDOM two-decimal percentages between
# 0.5 and 99.5. A rendering set that matches everything is a green tick on a red result,
# which is the offence [R-ENF-01 EXTENDED] names in terms, so it was reverted rather than
# kept. What is added instead is the SPECIFIC arithmetic this study's bibliography quotes
# in its own justification text — each one a named ratio of two figures the study commits
# with four fields, of which none is a model OUTPUT, so the output-only set could never
# have matched them.
_I = SN.get('inputs', {})
_H = SN.get('hist_is', {})


def _iv(k):
    v = _I.get(k)
    if isinstance(v, dict):
        v = v.get('value')
    return v if isinstance(v, (int, float)) else None


def _hv(y, k):
    v = (_H.get(y) or {}).get(k)
    return v if isinstance(v, (int, float)) else None


# The bibliography's justification text quotes the arithmetic behind each figure - an
# effective tax rate is income tax over profit before tax, an employees' share is the
# note-39 figure over attributable profit, a minority share is its own line over profit
# after tax. Each pair is NAMED. The denominators are that year's own filed aggregates,
# never every committed number, so the set stays small enough to mean something.
_named = []
for _y, _t in (('FY23', 'tax_fy23'), ('FY24', 'tax_fy24'), ('FY25', 'tax_fy25')):
    for _dk in ('ebt', 'rev', 'pat'):
        _a, _b = _iv(_t), _hv(_y, _dk)
        if _a and _b:
            _named.append(abs(_a / _b))
for _n, _d in (('emp_share_fy24', 'npa_fy24'), ('emp_share_fy25', 'npa_fy25'),
               ('emp_share_h1_26', 'h1_26_npa'),
               ('nci_fy23', 'pat_fy23'), ('nci_fy24', 'pat_fy24'), ('nci_fy25', 'pat_fy25'),
               ('h1_26_nci', 'h1_26_pat'), ('h1_26_tax', 'h1_26_ebt'),
               ('h1_26_nci_eq', 'h1_26_eq_parent'), ('q1_26_tax', 'q1_26_ebt')):
    _a, _b = _iv(_n), _iv(_d)
    if _a and _b:
        _named.append(abs(_a / _b))
vals += _named

RENDER = PF.rendering_set(vals)

if __name__ == '__main__':
    checked, problems = PF.check(DOCS, RENDER)
    sys.exit(PF.report(checked, problems, 'SWDY'))
