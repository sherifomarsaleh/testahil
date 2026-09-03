#!/usr/bin/env python3
"""AMR — every total a reader sees, reproduced from the rows printed above it.

The mechanism is engine/table_footing.py, shared with every other study; what is declared
here is only what is genuinely this study's own.

WHAT THIS FOUND AND FIXED. The asset lines this table breaks out came out short of the
disclosed total in every audited year. This study holds the total and those lines and NO
OTHERS, so the remainder cannot be NAMED here without the underlying statements — naming it
would be an invention rather than a disclosure, which SIGCM clause 1 forbids. It is printed
as what it is: a labelled RESIDUAL, so a reader can see there are assets outside the lines
broken out and cannot mistake a missing line for a wrong total. That is the honest fix
available without new data, and it is strictly better than a column that does not add.

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


DOCS = [d for d in (_latest('AMR_Valuation_Study_*_public.docx'), _latest('AMR_Bibliography_*.docx')) if d]

DECLARED = [
    (_latest('AMR_Valuation_Study_*_public.docx'), 14, "Blended equity risk premium",
     "A COMPONENT OF A COST-OF-CAPITAL LADDER, not a roll-up of the rows above it: the "
     "risk-free rate and the beta printed above are the other inputs to the cost of equity "
     "BELOW it, not parts of the premium. The premium is itself blended across the "
     "geographies the company earns in, which this table does not carry."),
]

if __name__ == '__main__':
    examined, problems = TF.check(DOCS, DECLARED)
    assert examined, 'no tables examined — an empty result is not a clean result'
    sys.exit(TF.report(examined, problems, 'AMR'))
