#!/usr/bin/env python3
"""AMOC — every total a reader sees, reproduced from the rows printed above it.

The mechanism is engine/table_footing.py, shared with every other study; what is declared
here is only what is genuinely this study's own — the rows whose label reads like a total
and which are NOT a roll-up of the table they sit in.

A FALSE POSITIVE IS FIXED BY DECLARING THE EXCEPTION WITH ITS REASON, NEVER BY DELETING THE
TOTAL. A total a reader cannot reproduce is indistinguishable from one that is wrong, so the
reason is the whole point of the declaration.
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


DOCS = [d for d in (_latest('AMOC_Valuation_Study_*_public.docx'), _latest('AMOC_Bibliography_*.docx')) if d]

DECLARED = [
    (_latest('AMOC_Valuation_Study_*_public.docx'), 11, "Blended",
     "A blend ACROSS PRODUCTS weighted by TONNAGE, and this table does not "
     "carry the tonnages \u2014 they are in the volume table beside it. "
     "Reproducible from the two tables together and not from this one alone, "
     "which is why it is declared rather than deleted; its spread column DOES "
     "foot across the row, which a column-wise instrument cannot see."
     ),
    (_latest('AMOC_Valuation_Study_*_public.docx'), 29, "Total assets, as filed",
     "A DISCLOSED LINE ITEM in a summary balance sheet, printed beside cash, "
     "debt and equity, none of which are its components."
     ),
    (_latest('AMOC_Valuation_Study_*_public.docx'), 29, "Total liabilities, as filed",
     "A DISCLOSED LINE ITEM in a summary balance sheet, printed beside cash, "
     "debt and equity, none of which are its components."
     ),
]

if __name__ == '__main__':
    examined, problems = TF.check(DOCS, DECLARED)
    assert examined, 'no tables examined — an empty result is not a clean result'
    for d in DECLARED:
        assert str(d[-1]).strip(), 'declared exception with no reason: %s' % (d[:3],)
    sys.exit(TF.report(examined, problems, 'AMOC'))
