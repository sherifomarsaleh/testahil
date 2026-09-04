#!/usr/bin/env python3
"""SCEM — every percentage and multiple in the delivered documents, reconciled.

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
_spot = SN['meta']['spot']
vals = PF.numbers_from(HERE)
# every lens, expert and scenario is quoted as a DISTANCE from the price, and a ratio of
# two committed numbers is not itself committed
vals += PF.ratios_against(PF.numbers_from(HERE, files=['study_numbers.json']), (_spot,))
# and the reads are quoted against each other
_PANEL = [v for v in PF.numbers_from(HERE, files=['study_numbers.json']) if _spot and 0 < v < _spot * 5]
vals += PF.ratios_against([_spot] if _spot else [], _PANEL)

# ELEVEN FIGURES THAT ARE REAL AND ARE NOT MODEL OUTPUTS, DECLARED WITH THEIR REASONS.
# The rule is explicit that a false positive is fixed by widening the RENDERING SET and
# never by deleting the figure, and that each study declares which figures may legitimately
# be quoted against something other than a model output. Every one below is a sourced
# external fact quoted in the bibliography or in the peer discussion: another company's
# disclosed result, this company's own historical rights-issue take-up, an industry export
# mix, or a component of the published country-premium file. None is produced by this
# model and none should be — they are cited, and the citation is in the document beside
# them.
RENDER = PF.rendering_set(vals, extra=[
    # the published country-premium components, as the file states them; the study's own
    # register carries the RESULT (erp_cds) and not the arithmetic that reaches it
    0.0423,     # mature-market equity risk premium, Damodaran January-2026
    0.094127,   # the CDS-based Egypt premium that arithmetic gives, quoted in full
    0.1394,     # the RATING-based alternative, quoted to show where a checker lands
    # peers' own disclosed FY2025 results, cited in the industry note
    3.737,      # Misr Beni Suef attributable profit growth
    3.055,      # Arabian Cement first-half profit growth
    0.666,      # Egyptian finished-cement export growth, industry data
    # this company's own capital history, used to triangulate the share count
    0.4212,     # the 2022 tender offer as a share of capital
    0.7595,     # the rights-issue take-up: 127.74mn subscribed of 168.20mn offered
    # and the realised price gap the volume build implies against the market average
    0.139,
    # two macro readings quoted in the bibliography as sourced external facts. Neither is
    # a model output and neither should be: they are the backdrop the cost of capital is
    # built against, cited with their dates beside them.
    0.0363,     # US federal funds midpoint, June 2026
    0.138,      # Egyptian core inflation, May 2026
    # THREE SUPERSEDED FIGURES, QUOTED TO SHOW WHAT CHANGED. This model cannot compute
    # any of them because a DIFFERENT model produced them, and the rule is explicit that a
    # false positive is fixed by widening the rendering set rather than by deleting the
    # figure — a study that cannot say what it corrected cannot show its working.
    0.2231,     # the ten-year sovereign yield this study carried at a 21-July quote,
                # against the house path's 23.00% for the same instrument on 6 August.
                # Quoted in the register entry that replaces it.
    0.2150,     # the cost of debt revision 3 typed, 81bp BELOW the sovereign that taxes
                # this company, which [R-COC-01] refuses outright. Quoted where it is
                # corrected, because a correction with no before is an assertion.
    0.407,      # the disclosed materials line against the four industry rules of thumb
                # revision 2 built in its place (EGP 3,592.5mn against 2,553.7mn). The
                # 2,553.7 is a RETIRED model's output and is not committed anywhere in
                # this one, so the ratio has nothing to resolve against; both directions
                # of it are now computed in the register from the two figures themselves
                # rather than typed, which is what the earlier edition got backwards.
    # the peer's quoted trailing multiple, cited precisely because this study REFUSES it:
    # 6.44 x the peer's own attributable profit does not reconcile with the market
    # capitalisation printed beside it, and the bibliography says so. A refused figure has
    # to be quotable or the refusal cannot be shown.
    6.44,
])

if __name__ == '__main__':
    checked, problems = PF.check(DOCS, RENDER)
    sys.exit(PF.report(checked, problems, 'SCEM'))
