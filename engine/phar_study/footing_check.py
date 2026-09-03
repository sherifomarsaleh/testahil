#!/usr/bin/env python3
"""PHAR — every total a reader sees, reproduced from the rows printed above it.

The mechanism is engine/table_footing.py, shared with every other study; what is declared
here is only what is genuinely this study's own.

WHAT IS DECLARED HERE. The cost-of-capital rows this study prints are a LADDER, not a
column that sums: the risk-free rate, the beta and the premium above a cost of equity are
its inputs rather than its parts, and a premium built from a base and a country component
is blended across a dimension the column does not carry. A transposed table compounds it —
its rows are line items and its columns are scenarios, so its weights are a ROW.

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


DOCS = [d for d in (_latest('EIPICO_Valuation_Study_*.docx'), _latest('EIPICO_Bibliography_*.docx')) if d]

DECLARED = [
    (_latest('EIPICO_Valuation_Study_*.docx'), 12, "TOTAL equity risk premium",
     "A LADDER ROW: the mature-market premium and the country premium above it are its two "
     "parts on one basis and not on the other, and the row is published on both bases side "
     "by side, which is not a construction a single column can sum."),
    (_latest('EIPICO_Valuation_Study_*.docx'), 12, "Blended cost of debt, after tax",
     "The pre-tax cost of debt times one less the tax rate — a row computed FROM two rows "
     "above it by multiplication, not by addition."),
]

if __name__ == '__main__':
    examined, problems = TF.check(DOCS, DECLARED)
    assert examined, 'no tables examined — an empty result is not a clean result'
    sys.exit(TF.report(examined, problems, 'PHAR'))
