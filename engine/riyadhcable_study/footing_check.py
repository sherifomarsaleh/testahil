#!/usr/bin/env python3
"""RIYADHCABLE — every total a reader sees, reproduced from the rows printed above it.

The mechanism is engine/table_footing.py, shared with every other study; what is declared
here is only what is genuinely this study's own.

WHAT THIS FOUND AND FIXED. The asset lines this table breaks out came out short of the
disclosed total in every audited year. This study holds the total and those lines and NO
OTHERS, so the remainder cannot be NAMED here without the underlying statements — naming it
would be an invention rather than a disclosure, which SIGCM clause 1 forbids. It is printed
as what it is: a labelled RESIDUAL, so a reader can see there are assets outside the lines
broken out and cannot mistake a missing line for a wrong total. That is the honest fix
available without new data, and it is strictly better than a column that does not add.

THE RESIDUAL IS ALSO A FINDING AND THE CAPTION SAYS SO: it runs SAR 146mn, 147mn and 430mn,
so something outside the four broken-out lines grew by SAR 283mn in a single year. This
table cannot explain that and the next edition should.

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


DOCS = [d for d in (_latest('RIYADHCABLE_Valuation_Study_*_public.docx'), _latest('RIYADHCABLE_Bibliography_*.docx')) if d]

DECLARED = []

if __name__ == '__main__':
    examined, problems = TF.check(DOCS, DECLARED)
    assert examined, 'no tables examined — an empty result is not a clean result'
    sys.exit(TF.report(examined, problems, 'RIYADHCABLE'))
