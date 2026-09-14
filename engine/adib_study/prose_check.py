#!/usr/bin/env python3
"""ADIB-Egypt — every percentage and multiple in the delivered documents, reconciled.

The mechanism is engine/prose_figures.py, shared with every other study; what is declared
here is only what is genuinely this study's own: which documents a reader receives, and
which figures may legitimately be quoted against something other than a model output.

WRITTEN 10-09-2026. This study was delivered, re-issued and audited without one, and the
delivered-vocabulary gate reported it as the only study with NO prose check and no entry
either way -- neither carrying the check nor recorded as owing it. That is the worst of
the three states: a study whose typed figures nothing has ever reconciled, and nothing
saying so.

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


DOCS = [d for d in (latest(r'.*Valuation_Study_.*\.docx$'),
                    latest(r'.*Bibliograph.*\.docx$')) if d]

SN = json.load(open('study_numbers.json'))
_spot = SN['meta']['spot']
vals = PF.numbers_from(HERE)

# EVERY LENS IS QUOTED AS A DISTANCE FROM THE PRICE, and a ratio of two committed
# numbers is not itself a committed number. On a bank this matters more than usual:
# the study publishes seven lenses and states each one's gap to the market.
vals += PF.ratios_against(PF.numbers_from(HERE, files=['study_numbers.json']), (_spot,))

# AND THE LENSES ARE QUOTED AGAINST EACH OTHER — the three equity-flow reads are
# compared to one another in the text, which is a ratio of two model outputs.
_PANEL = [v for v in PF.numbers_from(HERE, files=['study_numbers.json'])
          if _spot and 0 < v < _spot * 5]
vals += PF.ratios_against([_spot] if _spot else [], _PANEL)

# THE PER-SHARE AND PER-BOOK MULTIPLES A BANK IS READ ON. Price-to-book and
# price-to-earnings at the central and at the market are ratios of two committed
# figures apiece, and the document states all four.
_PROJ = SN.get('projection') or []
_BOOK = [r['bvps'] for r in _PROJ if isinstance(r, dict) and r.get('bvps')]
_EPS = [r['eps'] for r in _PROJ if isinstance(r, dict) and r.get('eps')]
_CENT = [SN['central'], _spot]
vals += PF.ratios_against(_CENT, tuple(_BOOK) + tuple(_EPS))

# EVERY CROSS-CHECK IS ALSO QUOTED AGAINST THE CENTRAL, NOT ONLY AGAINST THE PRICE.
# The study's own lens table has a column headed "against the central" -- the relative
# lens at +40.2%, residual income at +3.5%, and so on -- and a ratio base built on the
# spot alone cannot reach a single one of them.
vals += PF.ratios_against(PF.numbers_from(HERE, files=['study_numbers.json']),
                          (SN['central'],))

# THE JUSTIFIED PRICE-TO-BOOK IS AN IDENTITY OF THREE COMMITTED RATES, and the document
# states the multiple it produces: (sustainable return - growth) / (cost of equity -
# growth). It is derived here rather than registered, because a multiple registered
# beside the three rates that produce it is a fourth number that can disagree with them.
_CC = SN['cost_of_capital']
_g, _ket = _CC['terminal_growth'], _CC['ke_terminal']
_roe_t = [r['roe'] for r in _PROJ if isinstance(r, dict) and r.get('roe')]
for _r in _roe_t:
    if _ket > _g and _r > _g:
        vals.append((_r - _g) / (_ket - _g))

RENDER = PF.rendering_set(vals)

if __name__ == '__main__':
    checked, problems = PF.check(DOCS, RENDER)
    sys.exit(PF.report(checked, problems, 'ADIB'))
