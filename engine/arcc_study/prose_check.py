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



def latest_ddmmyyyy(pat):
    """The workbook names its edition DDMMYYYY with no separators, so the date is PARSED
    rather than the filenames sorted as text — 03092026 sorts below 09082026 as a string and
    would pick a superseded edition (the trap ADNOCLS's resolver records). On this study a
    text sort picks ARCC_Valuation_Model_06082026 over 03092026 — the 6 August file."""
    import re
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
DOCS = [d for d in ('ARCC_Valuation_Study_03-09-2026_public.docx',
                    'ARCC_Bibliography_03-09-2026.docx',
                    latest_ddmmyyyy(r'ARCC_Valuation_Model_\d{8}_public\.xlsx$')) if d]

SN = json.load(open('study_numbers.json'))
vals = PF.numbers_from(HERE)
# every lens, expert and scenario is quoted as a DISTANCE from the price
vals += PF.ratios_against(PF.numbers_from(HERE, files=['study_numbers.json']),
                          (SN['meta'].get('spot'),))
# THE TECHNICAL READ IS MEASURED AGAINST ITS OWN CLOSE AND NOT AGAINST SPOT, and the
# difference is not academic here. This widening once admitted BOTH, which is what let the
# levels table publish every resistance and support — and the 52-WEEK HIGH — as a large
# negative distance from a spot struck four weeks and 30.5% later, with prose_figures
# reporting zero unmatched because the wrong-clock figure was in the rendering set. A
# WIDENING MADE TO CLEAR A FALSE POSITIVE CAN HIDE A TRUE ONE, and the discipline that says
# a false positive is fixed by widening the set does not license widening it across two
# clocks: the levels belong to the read's date, full stop.
_tech = json.load(open('technicals.json')) if os.path.exists('technicals.json') else {}
_tclose = (_tech.get('close') if isinstance(_tech, dict) else None) or SN['meta'].get('spot')
vals += PF.relative_to(PF.numbers_from(HERE, files=['technicals.json']), (_tclose,))
# the ONE figure that legitimately spans both clocks is the gap between them, stated in the
# levels caption precisely so a reader is told the read predates the price
vals += PF.relative_to([SN['meta']['spot']], (_tclose,))

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
