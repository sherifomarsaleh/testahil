#!/usr/bin/env python3
"""STC — every percentage and multiple in the delivered documents, reconciled.

The mechanism is engine/prose_figures.py, shared with every other study; what is declared
here is only what is genuinely this study's own.

WHAT THIS WOULD HAVE CAUGHT, and what was instead found by reading twenty-six rendered
pages one at a time: a cost-of-capital table typed end to end whose every cell had stopped
matching the model (5.50% against 5.52%, a beta of 0.48 against 0.71, 7.59% against 8.13%,
terminal growth 2.50% against 2.00%); an expert's worked table still discounting at the
retired 7.59%; his colleague's sensitivity quoting 13.5x his own earnings as SAR 36.8 when
the arithmetic gives 35.8; a divergence paragraph asserting a spread of "about 23% of the
low" against an actual 7.9% and placing two of three experts at or above a price all three
sit below; and three typed figures inside a chart's own axis labels, where no check that
reads text can reach them at all.

TWO CLOCKS, AND THIS STUDY RUNS ON BOTH. The valuation is struck against the latest known
close; the technical read and the price cone are computed on the last session in the
persistent price library, which is an earlier date. A distance quoted in §2 or §3 is
measured against the cone anchor, and one quoted in §1 against the market price. The
widening below admits BOTH denominators and that is deliberate — but it is the widening
most likely to hide a true positive, so the two are declared separately and named.

A FALSE POSITIVE IS FIXED BY WIDENING THE RENDERING SET, NEVER BY DELETING THE FIGURE. If
a figure is real and the model cannot produce it, the model is what is missing.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
os.chdir(HERE)
import prose_figures as PF                                             # noqa: E402

# THE WORKBOOK IS A DELIVERED DOCUMENT AND WAS IN NO STUDY'S POPULATION IN THE BOOK. This
# study's own audit found six typed figures inside it — a spot, a share count, a market
# capitalisation, an equity weight, a superseded balance-sheet date and a caption promising
# a retired four-lens blend — every one of them beside a cell computing the right answer
# from the numbers file. prose_figures.texts_of() reads a workbook's STRING cells only: a
# numeric cell is a model output the recalculation gate already reconciles, and a numeral
# inside a label is prose that happens to live in a spreadsheet.
DOCS = ['STC_Valuation_Study_05-09-2026_public.docx',
        'STC_Bibliography_05-09-2026.docx',
        'STC_Valuation_Model_05092026_public.xlsx']

SN = json.load(open('study_numbers.json'))
SPOT = SN['spot']
ANCHOR = SN['cone_anchor']

vals = PF.numbers_from(HERE)

# Every lens, expert and scenario is quoted as a distance from the price it is measured
# against — the commonest shape on the page and not itself a committed number.
vals += PF.ratios_against(PF.numbers_from(HERE, files=['study_numbers.json']), (SPOT,))

# THE PRICE CONE AND THE TECHNICAL READ ARE ON THE LIBRARY'S CLOCK, NOT THE VALUATION'S.
# Section 3 quotes every percentile as a move on the cone anchor and section 2 quotes the
# moving-average stack the same way; measuring either against the valuation price would be
# checking a document this study did not write. The first draft of section 2 made exactly
# that mistake in the other direction — it computed the stack distance on the valuation
# price and printed the stock 0.1% BELOW an average it sits above.
_cone = PF.numbers_from(HERE, files=['study_numbers.json'])
vals += PF.ratios_against(_cone, (ANCHOR,))
vals += PF.relative_to(_cone, (ANCHOR,))
# the one figure that legitimately spans both clocks is the gap between the two prices
vals += PF.relative_to([SPOT], (ANCHOR,))

# A SPREAD BETWEEN TWO COMMITTED VALUES IS NOT ITSELF COMMITTED. Appendix C quotes the
# panel's spread as a percentage of its own low, section 4 quotes the multiple lens as a
# distance from the cash-flow lens, and section 1.5 quotes the envelope the same way. Every
# pairwise ratio among the lens values and the expert centrals is declared rather than the
# sentences being deleted or the figures typed.
_E = SN['experts']
_L = SN['lenses']
_PANEL = [_E['e1']['base'], _E['e2']['base'], _E['e3']['base'],
          _E['e1']['rng'][0], _E['e1']['rng'][1], _E['e2']['rng'][0], _E['e2']['rng'][1],
          SN['central'], SN['central_range']['low'], SN['central_range']['high'],
          _L['book_value']]
for k in ('dcf', 'ddm', 'relative', 'normalized'):
    _PANEL += [_L[k]['bear'], _L[k]['base'], _L[k]['bull']]
vals += PF.ratios_against(_PANEL, _PANEL)

# A MULTIPLE IS A VALUE OVER AN EARNINGS FIGURE, and this study quotes several: the
# through-cycle price-to-earnings each expert will defend, the multiple the market itself
# is paying, and the multiple on economic profit that Expert 1's fade implies. None is a
# committed number; all three are two committed numbers divided.
_PER_SHARE = [SN['rel_basis']['norm_eps'], SN['rel_basis']['eps26']]
vals += PF.ratios_against(_PANEL + [SPOT, ANCHOR], _PER_SHARE)

# THE BAND RECORD IS A COUNT AND A SHARE OF IT. "51 of 58" is not in the numbers file as a
# ratio, and neither is the shortfall against the 90% the band aims at.
_B = SN['band_record']
vals += [_B['hits'] / _B['n'], _B['cov90'] - 0.90, _B['n'] - _B['hits']]

# THE SWEEP REGISTER'S FINDINGS CARRY THEIR NUMBERS IN PROSE, NOT IN NUMERIC FIELDS. The
# bibliography quotes those findings VERBATIM — that is what a research trail is — so a
# figure inside one is a QUOTATION of a committed artefact rather than a figure typed into
# a builder. numbers_from() reads numeric JSON values and cannot see them.
#
# This widening is deliberately narrow: it takes numerals only from this one file's own
# text, so it admits the research facts the trail reports and nothing else. The alternative
# — dropping the figures out of the quoted findings — would make the trail less useful and
# would be the "delete the figure" move this method forbids.
import re as _re

_sweep_text = []


def _walk(o):
    if isinstance(o, dict):
        for v in o.values():
            _walk(v)
    elif isinstance(o, list):
        for v in o:
            _walk(v)
    elif isinstance(o, str):
        _sweep_text.append(o)


_walk(json.load(open('sweep_register.json')))
for _t in _sweep_text:
    for _m in _re.finditer(r'(?<![\w.])(\d[\d,]*\.?\d*)', _t):
        try:
            _v = float(_m.group(1).replace(',', ''))
        except ValueError:
            continue
        vals.append(_v)
        vals.append(_v / 100.0)

RENDER = PF.rendering_set(vals)

if __name__ == '__main__':
    checked, problems = PF.check([d for d in DOCS if os.path.exists(d)], RENDER)
    sys.exit(PF.report(checked, problems, 'STC'))
