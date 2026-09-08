#!/usr/bin/env python3
"""GBCO — every percentage and multiple in the delivered documents, reconciled.

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


DOCS = [d for d in (latest(r'.*Valuation_Study_.*\.docx$'),) if d]

SN = json.load(open('study_numbers.json'))
_spot = SN['spot']
vals = PF.numbers_from(HERE)
# every lens, expert and scenario is quoted as a DISTANCE from the price, and a ratio of
# two committed numbers is not itself committed
vals += PF.ratios_against(PF.numbers_from(HERE, files=['study_numbers.json']), (_spot,))
# and the reads are quoted against each other
_PANEL = [v for v in PF.numbers_from(HERE, files=['study_numbers.json']) if _spot and 0 < v < _spot * 5]
vals += PF.ratios_against([_spot] if _spot else [], _PANEL)

# A MARGIN IS A RATIO OF TWO COMMITTED FIGURES AND THE RATIO IS NOT ITSELF COMMITTED.
# Every income statement in this study — the three reported years and the five forecast
# years — prints a gross margin and a net margin beside its own revenue, and the
# forecast's cost lines are quoted as a share of revenue in §1.2. Those are exactly the
# ratios_against() shape the shared module documents, so the rendering set is WIDENED here
# rather than the figures being deleted from the page.
_SN = json.load(open('study_numbers.json'))
_IS_ROWS = list(_SN['history']['income_statement'].values()) + _SN['group_forecast']['rows']
for _row in _IS_ROWS:
    _rev = _row.get('revenue')
    if not _rev:
        continue
    vals += [v / _rev for v in _row.values() if isinstance(v, (int, float)) and v]
# and the auto leg's own lines against the auto revenue of the same year
for _row in _SN['dcf']['rows']:
    _r = _row.get('rev')
    if not _r:
        continue
    vals += [v / _r for v in _row.values() if isinstance(v, (int, float)) and v]

# A LEVEL IS QUOTED AS A DISTANCE FROM THE CLOSE THE READ WAS COMPUTED ON, not from the
# price the valuation is struck on: the technical read and the cone sit on the exchange
# library's own last session and the valuation on the latest known price, and they are two
# clocks. relative_to() is the shared module's own name for exactly this shape.
_ANCHOR = _SN['valuation_gap']['mc_anchor']
vals += PF.relative_to([float(k) for k in _SN['mc']['touch']], [_ANCHOR])
vals += PF.relative_to([v for v in PF.numbers_from(HERE, files=['study_numbers.json'])
                        if _ANCHOR and 0 < v < _ANCHOR * 3], [_ANCHOR])

# A MULTIPLE IS A RATIO OF TWO COMMITTED FIGURES AND THE RATIO IS NOT ITSELF COMMITTED.
# The study quotes what each answer, and the traded price, come to as a multiple of the
# earnings and of the book they stand on — the ratios_against() shape the shared module
# documents, widened here rather than the figures being deleted from the page.
_S, _L = _SN['sotp'], _SN['lens_record']
_MARKS = [_L['primary']['range_basis']['low'], _L['primary']['range_basis']['high']]
_ANSWERS = ([b['value'] * _SN['shares'] for b in _SN['central_two_sided']['branches']]
            + [_SN['mktcap'], _S['auto_eq'], _S['cap_val'], _S['auto_eq'] + _S['cap_val']]
            + [m + _S['other_assoc'] for m in _MARKS])
_BASES = [_SN['history']['income_statement'][y]['net_profit']
          for y in _SN['history']['years']]
_BASES += [_SN['group_forecast']['rows'][0]['net_profit'],
           _SN['inputs']['eq_jun2026']['value'],
           _SN['lens_inputs']['capital']['operating_equity']]
vals += PF.ratios_against(_ANSWERS, _BASES)
# and the associate mark quoted as a share of the round, of the carrying value, and of what
# the traded price leaves for the associates
# TWO RESIDUALS, AS THE DOCUMENT COMPUTES THEM: what the price leaves for ALL the
# associates once the two operating legs are taken at this study's marks, and what it
# leaves for MNT-Halan alone with the smaller holdings held at carrying value.
_PRICE_ASSOC = _SN['spot'] * _SN['shares'] - _S['auto_eq'] - _S['cap_val']
_PRICE_MARK = _PRICE_ASSOC - _S['other_assoc']
_ASSOC_LINES = _MARKS + [m + _S['other_assoc'] for m in _MARKS] + [_S['assoc']]
vals += PF.ratios_against(_ASSOC_LINES + [_PRICE_ASSOC, _PRICE_MARK],
                          _ASSOC_LINES + [_PRICE_ASSOC, _PRICE_MARK, _SN['mktcap']])

# TWO FIGURES THE MODEL REGISTERS AND THE NUMBERS FILE DOES NOT CARRY FORWARD. GB Corp's
# reviewed statements give a second ownership pair for the same transaction as its press
# release, and the study prints both rather than deciding silently. They are read from the
# model's own committed constants by the document builder and are read the same way here,
# so the page and the check cannot disagree about what the model registered.
import re as _re                                                       # noqa: E402
_SRC = open('compute.py', encoding='utf-8').read()
for _nm in ('mnt_stake_statements', 'mnt_stake_statements_prior'):
    _m = _re.search(r'^%s\s*=\s*([0-9.]+)' % _nm, _SRC, _re.M)
    assert _m, 'the model no longer registers %s' % _nm
    vals.append(float(_m.group(1)))

RENDER = PF.rendering_set(vals)

if __name__ == '__main__':
    checked, problems = PF.check(DOCS, RENDER)
    sys.exit(PF.report(checked, problems, 'GBCO'))
