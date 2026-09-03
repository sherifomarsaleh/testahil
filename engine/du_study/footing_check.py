#!/usr/bin/env python3
"""DU — every total a reader sees, reproduced from the rows printed above it.

The mechanism is engine/table_footing.py, shared with every other study; what is declared
here is only what is genuinely this study's own.

WHAT IS DECLARED HERE. Two of the three are DRIVER NAMES in a sensitivity grid, where every
row carries the fair value at five settings of that driver and nothing is a roll-up of
anything — the word "blended" is in its ordinary sense, ARPU blended across the mobile and
fixed legs. The third is a disclosed line item in a markers table. None is a total that a
reader should be able to reproduce from the rows above it.

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


DOCS = [d for d in (_latest('DU_Valuation_Study_*_public.docx'), _latest('DU_Bibliography_*.docx')) if d]

DECLARED = [
    (_latest('DU_Valuation_Study_*_public.docx'), 17, "Total equity",
     "A DISCLOSED LINE ITEM in a markers table, printed after asset and liability lines "
     "that are not its components — the same shape as TMGH's marker block."),
    (_latest('DU_Valuation_Study_*_public.docx'), 12, "Blended ARPU (\u00d7)  "
     "(0.92 / 0.96 / 1.00 / 1.04 / 1.08)", "A DRIVER NAME IN A SENSITIVITY GRID. The row "
     "carries the fair value at five settings of that driver; nothing in this table is a "
     "roll-up of anything, and the word 'blended' is in its ordinary sense — ARPU blended "
     "across the mobile and fixed legs."),
    (_latest('DU_Valuation_Study_*_public.docx'), 12, "Blended ARPU drift (%/yr)  "
     "(-2.5% / -1.5% / +0.0% / +0.5% / +1.0%)", "A driver name in the same sensitivity "
     "grid, as above."),
]

if __name__ == '__main__':
    examined, problems = TF.check(DOCS, DECLARED)
    assert examined, 'no tables examined — an empty result is not a clean result'
    sys.exit(TF.report(examined, problems, 'DU'))
