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
sys.path.insert(0, HERE)
import edition as _ed        # the edition date, written once
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
# POINTED AT THE EDITION MODULE. It named the 03-09 files, and a check that opens a
# SUPERSEDED file reports that file's defects as current [L-066/L-067].
DOCS = [d for d in (_ed.STUDY_DOCX,
                    _ed.BIBLIO_DOCX,
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
# THE TWO-CLOCK ERROR, COMMITTED BY THE LINE UNDER THE WARNING AGAINST IT
# [corrected 13-09-2026]. technicals.json nests its read under a 'state' key --
# docx_arcc.py:56 reads it as ['state'] -- so _tech.get('close') was ALWAYS None and
# this fell through to the study's spot. Every level distance was then checked
# against EGP 77.00 while the document measures it against the read's own EGP 59.00
# close of 2026-08-06, which is precisely the mistake the paragraph above describes.
# It went unnoticed because three of the six distances happened to match some other
# committed value anyway; only support 3 at -18.5% (48.10/59.00-1, checked as
# 48.10/77.00-1 = -37.5%) had no coincidence to hide behind.
#
# A FALLBACK THAT CANNOT BE REACHED HONESTLY IS WORSE THAN NO FALLBACK: it makes the
# wrong denominator the silent default. The read's close is required now, and its
# absence is an error rather than a substitution.
_tstate = _tech.get('state') if isinstance(_tech.get('state'), dict) else _tech
_tclose = _tstate.get('close') if isinstance(_tstate, dict) else None
assert _tclose, ('technicals.json carries no close, so no level distance can be '
                 'checked against the clock the document actually uses')
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
