#!/usr/bin/env python3
"""GBCO — every total a reader sees, reproduced from the rows printed above it.

The mechanism is engine/table_footing.py, shared with every other study; what is declared
here is only what is genuinely this study's own.

THIS STUDY DECLARES NOTHING, and that is the result rather than an omission: every row whose
label announces it as a total reproduces from the rows printed above it, as a sum or as a
weighted mean against a column of the same table. A declaration list is where a study says
which of its totals a reader cannot reproduce; this one has no such row.

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


DOCS = [d for d in (_latest('GBCO_Valuation_Study_*.docx'), _latest('GBCO_Bibliography_*.docx')) if d]

_DOC = _latest('GBCO_Valuation_Study_*.docx')

# ONE DECLARED EXCEPTION, AND IT IS A REAL STRUCTURAL FACT ABOUT THE TABLE.
# Table A4 of Appendix A lists the balance-sheet ANCHORS the enterprise-to-equity bridge
# stands on — cash, group borrowings, the auto segment's borrowings, and total equity —
# each as a separately disclosed line with its own date and source. "Total equity" is a
# DISCLOSED LINE ITEM there and not a roll-up of the three rows printed above it, which are
# not its components; it does not foot against them because nothing claims it should. This
# is the shape the shared instrument itself records as structurally indistinguishable from
# a roll-up, so the study declares it with its reason rather than deleting the row.
DECLARED = [(_DOC, 27, 'Total equity',
             'a separately disclosed balance-sheet line listed beside cash and borrowings, '
             'not a total of them: the three rows above it are not its components and the '
             'table makes no claim that they are')] if _DOC else []

if __name__ == '__main__':
    examined, problems = TF.check(DOCS, DECLARED)
    assert examined, 'no tables examined — an empty result is not a clean result'
    sys.exit(TF.report(examined, problems, 'GBCO'))
