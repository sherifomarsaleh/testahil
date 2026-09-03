#!/usr/bin/env python3
"""EMPOWER — every total a reader sees, reproduced from the rows printed above it.

The mechanism is engine/table_footing.py, shared with every other study; what is declared
here is only what is genuinely this study's own.

WHAT THIS FOUND AND FIXED, AND IT WAS NOT A MODELLING ERROR. Eleven asset and liability
lines sat in the filings and in this study's own extraction and were mapped into no printed
row, so the balance sheet came out about 1% short on the asset side and AED 517mn short on
the liability side in every period. Both residuals are now printed as named rows, and the
builder ASSERTS on FY2023 that each residual IS the sum of the specific lines it names —
94,729 thousand of right-of-use, deferred tax, other financial assets and due-from-related-
parties, and 517,383 thousand of retentions, the deferred government grant, end-of-service
benefits and due-to-related-parties. A residual row that is merely a plug would foot by
construction and prove nothing; this one is held to its own components.

THIS STUDY NOW DECLARES NOTHING. Every row whose label announces it as a total reproduces
from the rows printed above it. A declaration list is where a study names the totals a
reader cannot reproduce; this one has no such row.

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


DOCS = [d for d in (_latest('EMPOWER_Valuation_Study_*.docx'), _latest('EMPOWER_Bibliography_*.docx')) if d]

DECLARED = []

if __name__ == '__main__':
    examined, problems = TF.check(DOCS, DECLARED)
    assert examined, 'no tables examined — an empty result is not a clean result'
    sys.exit(TF.report(examined, problems, 'EMPOWER'))
