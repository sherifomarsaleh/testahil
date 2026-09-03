#!/usr/bin/env python3
"""ARCC — every percentage and multiple in the delivered documents, reconciled.

The mechanism is engine/prose_figures.py, shared with every other study; what is declared
here is only what is genuinely this study's own.

WHAT THIS WOULD HAVE CAUGHT: a masthead reading "issued 2 September" on a 3 September
edition, a source note quoting the 6 August close beside a 3 September price, an EFG bridge
still ending on "this study's weighted central — four lenses, weighted" after the blend was
retired, and a caption asserting the panel median "sits close to" a central 22% away.

A FALSE POSITIVE IS FIXED BY WIDENING THE RENDERING SET, NEVER BY DELETING THE FIGURE.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
os.chdir(HERE)
import prose_figures as PF                                             # noqa: E402

DOCS = ['ARCC_Valuation_Study_03-09-2026_public.docx',
        'ARCC_Bibliography_03-09-2026.docx']

SN = json.load(open('study_numbers.json'))
vals = PF.numbers_from(HERE)
# every lens, expert and scenario is quoted as a DISTANCE from the price
vals += PF.ratios_against(PF.numbers_from(HERE, files=['study_numbers.json']),
                          (SN['meta'].get('spot'),))
_tech = json.load(open('technicals.json')) if os.path.exists('technicals.json') else {}
_tclose = (_tech.get('close') if isinstance(_tech, dict) else None) or SN['meta'].get('spot')
vals += PF.relative_to(PF.numbers_from(HERE, files=['technicals.json']),
                       (_tclose, SN['meta'].get('spot')))

# A SPREAD BETWEEN TWO COMMITTED VALUES is not itself committed, and section C.5 quotes the
# panel's spread as one — "a spread of 32.1% of the lower number". Every pairwise ratio of
# the expert centrals and the lens values is declared here rather than the sentence being
# deleted or the figure typed.
_PANEL = [e['central'] for e in SN['experts']] + [e['low'] for e in SN['experts']] \
    + [e['high'] for e in SN['experts']] + list(SN['lenses']['values'].values())
vals += PF.ratios_against(_PANEL, _PANEL)

RENDER = PF.rendering_set(vals)

if __name__ == '__main__':
    checked, problems = PF.check([d for d in DOCS if os.path.exists(d)], RENDER)
    sys.exit(PF.report(checked, problems, 'ARCC'))
