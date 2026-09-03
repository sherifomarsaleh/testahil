#!/usr/bin/env python3
"""ADNOCDRILL — every total a reader sees, reproduced from the rows printed above it.

The mechanism is engine/table_footing.py, shared with every other study; what is declared
here is only what is genuinely this study's own.

WHAT THIS FOUND AND FIXED. The forecast liability block did not foot for a reader: the five
printed lines came out about USD 32mn short of the total above them in every forecast year,
while the audited years footed exactly. The cause is that the audited total is struck as
assets less equity and the forecast total as an explicit sum which includes ACQUISITION
LIABILITIES — a line the model carried and the table did not print. It is printed now, and
both halves foot.

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


DOCS = [d for d in (_latest('ADNOCDRILL_Valuation_Study_*.docx'), _latest('ADNOCDRILL_Bibliography_*.docx')) if d]

DECLARED = [
    (_latest('ADNOCDRILL_Valuation_Study_*.docx'), 28, "Total equity",
     "A DISCLOSED LINE ITEM printed after total liabilities, not a roll-up of them: the "
     "rows above it are liabilities, and equity is not their sum. Assets equals liabilities "
     "plus equity does hold across the three — downward, and this instrument reads upward."),
    (_latest('ADNOCDRILL_Valuation_Study_*.docx'), 17, "Weighted average cost of capital",
     "The cost of equity and the after-tax cost of debt weighted by the equity and debt "
     "weights, which this table prints as a ROW: it is transposed, its rows being line items "
     "and its columns the scenarios. Reproducible by a reader, not by a column-wise "
     "instrument."),
]

if __name__ == '__main__':
    examined, problems = TF.check(DOCS, DECLARED)
    assert examined, 'no tables examined — an empty result is not a clean result'
    sys.exit(TF.report(examined, problems, 'ADNOCDRILL'))
