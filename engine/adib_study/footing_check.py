#!/usr/bin/env python3
"""ADIB — every total a reader sees, reproduced from the rows printed above it.

The mechanism is engine/table_footing.py, shared with every other study; what is declared
here is only what is genuinely this study's own.

WHY THIS STUDY HAD NONE. It was built on 09-09-2026 and shipped without the instrument
every other study in the book carries, so the one gate that reproduces a delivered total
from its own rows reported ADIB as "no footing check" and passed the study anyway until the
gate learned to refuse that [R-ENF-04]. An absent check is not a clean check.

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


DOCS = [d for d in (_latest('ADIB_Valuation_Study_*.docx'),
                    _latest('ADIB_Bibliography_*.docx')) if d]

DECLARED = [
    (_latest('ADIB_Valuation_Study_*.docx'), 20, "Total liabilities",
     "The balance sheet in A.2 is a SUMMARY of five selected lines, not an additive "
     "schedule: financing to customers and total assets are not liabilities at all, and "
     "customers' deposits are one liability among several. The total is the filed total, "
     "read from the statements, and a reader reproduces it from the balance sheet rather "
     "than from the four rows above it. Declared rather than deleted — a total a reader "
     "cannot reproduce is indistinguishable from one that is wrong, and this one is right."),
]

if __name__ == '__main__':
    examined, problems = TF.check(DOCS, DECLARED)
    assert examined, 'no tables examined — an empty result is not a clean result'
    sys.exit(TF.report(examined, problems, 'ADIB'))
