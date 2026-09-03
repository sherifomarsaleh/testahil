#!/usr/bin/env python3
"""BOROUGE — every total a reader sees, reproduced from the rows printed above it.

The mechanism is engine/table_footing.py, shared with every other study; what is declared
here is only what is genuinely this study's own.

WHAT IS DECLARED HERE AND WHY IT IS QUANTIFIED. This study's summary balance sheet is a
CONDENSED layout: it prints selected lines against a DISCLOSED total rather than a complete
statement, so the printed rows do not add to that total and are not meant to. That is a
legitimate presentation, and it is declared rather than fixed — but THE SHARE NOT BROKEN OUT
IS STATED IN EACH DECLARATION BELOW, because a declaration that hides the size of the gap is
the rubber stamp this mechanism exists to prevent.

The disposition follows what each study HOLDS. Where the missing lines were registered
inputs they were printed instead (TMGH 748.0 and 23.6, ADNOCDRILL 32, EMPOWER eleven lines).
Where a study held only a total and a selection and the gap was small, a LABELLED RESIDUAL
was printed (AMR 10-14, RIYADHCABLE 146-430). At the sizes below a residual row would be a
way of not investigating rather than a disclosure, so the honest record is the number stated
here and a caption at the next re-issue saying the table is a selection.

A FALSE POSITIVE IS FIXED BY DECLARING THE EXCEPTION WITH ITS REASON, NEVER BY DELETING THE
TOTAL. A total a reader cannot reproduce is indistinguishable from one that is wrong.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
os.chdir(HERE)
import table_footing as TF                                              # noqa: E402

_DATE = re.compile(r'(\d{2})-(\d{2})-(\d{4})')


def _latest(pattern):
    """The LATEST edition by DATE, never by string sort — "08-08-2026" sorts above
    "03-09-2026" and a check that opens a superseded file reports its defects as current."""
    fs = [f for f in glob.glob(pattern) if not os.path.basename(f).startswith('~$')]
    if not fs:
        return None
    return max(fs, key=lambda f: (_DATE.search(f).group(3, 2, 1)
                                  if _DATE.search(f) else ('0', '0', '0')))


DOCS = [d for d in (_latest('BOROUGE_Valuation_Study_*_public.docx'), _latest('BOROUGE_Bibliography_*.docx')) if d]

DECLARED = [
    (_latest('BOROUGE_Valuation_Study_*_public.docx'), 24, "Total assets",
     "A CONDENSED LAYOUT against a disclosed total: between 14.2% and 17.2% of assets are "
     "not broken out in the three rows above."),
]

if __name__ == '__main__':
    examined, problems = TF.check(DOCS, DECLARED)
    assert examined, 'no tables examined — an empty result is not a clean result'
    sys.exit(TF.report(examined, problems, 'BOROUGE'))
