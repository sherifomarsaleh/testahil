#!/usr/bin/env python3
"""TMGH — every total a reader sees, reproduced from the rows printed above it.

The mechanism is engine/table_footing.py, shared with every other study; what is declared
here is only what is genuinely this study's own — the rows whose label reads like a total
and which are NOT a roll-up of the table they sit in.

A FALSE POSITIVE IS FIXED BY DECLARING THE EXCEPTION WITH ITS REASON, NEVER BY DELETING THE
TOTAL. A total a reader cannot reproduce is indistinguishable from one that is wrong, so the
reason is the whole point of the declaration.

WHAT THIS FOUND AND WHAT IT COST TO FIX. Table 19, the as-reported balance sheet, did not
foot for a reader in either block: the five printed non-current lines came out EGP 748mn
short of the stated total and the seven printed current lines EGP 24mn short. The study was
NOT wrong — it held every missing figure as a registered input and simply did not print
them. The non-current gap is intangibles 84.6 plus right-of-use 481.4 plus the deferred tax
asset 182.0, which is 748.0 to the last hundred thousand; the current gap is work in
progress at 23.6. Both blocks now print those lines and both foot.

That is the whole argument for this gate. The balance sheet closed perfectly at the TOP —
non-current plus current is total assets to the pound, and equity plus liabilities is the
same figure — so every check that reconciles a model to itself passed it, and a reader
adding a column had no way to tell a missing line from a wrong total.
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


DOCS = [d for d in (_latest('TMGH_Valuation_Study_*.docx'), _latest('TMGH_Sources_*.docx')) if d]

DECLARED = [
    (_latest('TMGH_Valuation_Study_*.docx'), 20, "Total assets",
     "BALANCE-SHEET MARKERS AT THE FOOT OF A CASH-FLOW TABLE, not roll-ups of the operating cash flow and dividends printed above them. They do relate to each other \u2014 total assets IS total liabilities plus total equity \u2014 but downward, and the instrument reads upward."
     ),
    (_latest('TMGH_Valuation_Study_*.docx'), 20, "Total liabilities",
     "BALANCE-SHEET MARKERS AT THE FOOT OF A CASH-FLOW TABLE, not roll-ups of the operating cash flow and dividends printed above them. They do relate to each other \u2014 total assets IS total liabilities plus total equity \u2014 but downward, and the instrument reads upward."
     ),
    (_latest('TMGH_Valuation_Study_*.docx'), 20, "Total equity",
     "BALANCE-SHEET MARKERS AT THE FOOT OF A CASH-FLOW TABLE, not roll-ups of the operating cash flow and dividends printed above them. They do relate to each other \u2014 total assets IS total liabilities plus total equity \u2014 but downward, and the instrument reads upward."
     ),
    (_latest('TMGH_Valuation_Study_*.docx'), 27, "Total liabilities",
     "A bridge line, not a roll-up of the rows above it; the figure is negative because it is deducted in the bridge this table sets out."
     ),
    (_latest('TMGH_Sources_*.docx'), 3, "total assets fy25",
     "AN INPUT-REGISTER ROW, NOT A ROLL-UP. This table lists the study's "
     "committed inputs by KEY with their values, so a key NAMED for a total "
     "sits among unrelated keys rather than beneath its own components. The "
     "register carries no arithmetic down its value column at all."
     ),
]

if __name__ == '__main__':
    examined, problems = TF.check(DOCS, DECLARED)
    assert examined, 'no tables examined — an empty result is not a clean result'
    for d in DECLARED:
        assert str(d[-1]).strip(), 'declared exception with no reason: %s' % (d[:3],)
    sys.exit(TF.report(examined, problems, 'TMGH'))
