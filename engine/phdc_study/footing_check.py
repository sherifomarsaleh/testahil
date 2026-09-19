#!/usr/bin/env python3
"""PHDC — every total a reader sees, reproduced from the rows printed above it.

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


DOCS = [d for d in (_latest('PHDC_Valuation_Study_*.docx'), _latest('PHDC_Bibliography_*.docx')) if d]

DECLARED = [
    (_latest('PHDC_Bibliography_*.docx'), 1, "total assets",
     "AN INPUT-REGISTER ROW, NOT A ROLL-UP. This table lists the study's "
     "committed inputs by KEY with their values, so a key NAMED for a total "
     "sits among unrelated keys rather than beneath its own components. The "
     "register carries no arithmetic down its value column at all."
     ),
    (_latest('PHDC_Bibliography_*.docx'), 1, "total current assets",
     "AN INPUT-REGISTER ROW, NOT A ROLL-UP. This table lists the study's "
     "committed inputs by KEY with their values, so a key NAMED for a total "
     "sits among unrelated keys rather than beneath its own components. The "
     "register carries no arithmetic down its value column at all."
     ),
    (_latest('PHDC_Bibliography_*.docx'), 1, "total equity",
     "AN INPUT-REGISTER ROW, NOT A ROLL-UP. This table lists the study's "
     "committed inputs by KEY with their values, so a key NAMED for a total "
     "sits among unrelated keys rather than beneath its own components. The "
     "register carries no arithmetic down its value column at all."
     ),
    (_latest('PHDC_Bibliography_*.docx'), 1, "total liabilities",
     "AN INPUT-REGISTER ROW, NOT A ROLL-UP. This table lists the study's "
     "committed inputs by KEY with their values, so a key NAMED for a total "
     "sits among unrelated keys rather than beneath its own components. The "
     "register carries no arithmetic down its value column at all."
     ),
    (_latest('PHDC_Bibliography_*.docx'), 1, "total noncurrent assets",
     "AN INPUT-REGISTER ROW, NOT A ROLL-UP. This table lists the study's "
     "committed inputs by KEY with their values, so a key NAMED for a total "
     "sits among unrelated keys rather than beneath its own components. The "
     "register carries no arithmetic down its value column at all."
     ),
    (_latest('PHDC_Bibliography_*.docx'), 2, "total assets 1q26",
     "An input-register row keyed by name, as above \u2014 the first-quarter "
     "balance-sheet inputs, listed as keys rather than summed as a statement."
     ),
    (_latest('PHDC_Bibliography_*.docx'), 2, "total current assets 1q26",
     "An input-register row keyed by name, as above \u2014 the first-quarter "
     "balance-sheet inputs, listed as keys rather than summed as a statement."
     ),
    (_latest('PHDC_Bibliography_*.docx'), 2, "total current liabs 1q26",
     "An input-register row keyed by name, as above \u2014 the first-quarter "
     "balance-sheet inputs, listed as keys rather than summed as a statement."
     ),
    (_latest('PHDC_Bibliography_*.docx'), 2, "total equity 1q26",
     "An input-register row keyed by name, as above \u2014 the first-quarter "
     "balance-sheet inputs, listed as keys rather than summed as a statement."
     ),
    (_latest('PHDC_Bibliography_*.docx'), 2, "total liabilities 1q26",
     "An input-register row keyed by name, as above \u2014 the first-quarter "
     "balance-sheet inputs, listed as keys rather than summed as a statement."
     ),
    (_latest('PHDC_Bibliography_*.docx'), 2, "total noncurrent assets 1q26",
     "An input-register row keyed by name, as above \u2014 the first-quarter "
     "balance-sheet inputs, listed as keys rather than summed as a statement."
     ),
    (_latest('PHDC_Bibliography_*.docx'), 2, "total noncurrent liabs 1q26",
     "An input-register row keyed by name, as above \u2014 the first-quarter "
     "balance-sheet inputs, listed as keys rather than summed as a statement."
     ),
    (_latest('PHDC_Valuation_Study_*.docx'), 1, "Total assets (EGP mn)",
     "A DISCLOSED LINE ITEM heading a summary balance sheet, printed beside "
     "cash, debt and equity, none of which are its components. The full "
     "statement, where it does foot over non-current and current assets, is in "
     "the appendix."
     ),
    (_latest('PHDC_Valuation_Study_*.docx'), 12, "Weighted average cost of capital",
     "The cost of equity and the after-tax cost of debt weighted by the equity "
     "and debt weights, which this table prints as a ROW: it is transposed, "
     "its rows being line items and its columns the explicit-window and "
     "terminal anchors. Reproducible by a reader, not by a column-wise "
     "instrument."
     ),
]

if __name__ == '__main__':
    examined, problems = TF.check(DOCS, DECLARED)
    assert examined, 'no tables examined — an empty result is not a clean result'
    for d in DECLARED:
        assert str(d[-1]).strip(), 'declared exception with no reason: %s' % (d[:3],)
    sys.exit(TF.report(examined, problems, 'PHDC'))
