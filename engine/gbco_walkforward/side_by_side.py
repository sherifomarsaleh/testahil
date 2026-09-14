#!/usr/bin/env python3
"""GBCO walk-forward — the projected-versus-actual income statement, for EVERY origin.

[R-FCAL-01] requires it side by side at every origin rather than as a pooled statistic,
because a pooled bias hides which years produced it.
"""
from __future__ import annotations
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import score as S                                              # noqa: E402

LINES = [('revenue', 'Revenue'), ('gross_profit', 'Gross profit'), ('sga', 'SG&A'),
         ('operating_profit', 'Operating profit'), ('finance_cost', 'Finance cost, net'),
         ('net_profit', 'Net profit')]


def main():
    P = S.load()
    for t in S.ORIGINS:
        m = S.project(P, t)
        if m is None:
            continue
        print('\n=== ORIGIN FY%d — projected vs actual, EGP mn ===' % t)
        hs = [h for h in S.HOR if t + h <= S.LAST]
        print('%-20s %s' % ('', '  '.join('%17s' % ('FY%d (h=%d)' % (t + h, h)) for h in hs)))
        for key, label in LINES:
            cells = []
            for h in hs:
                a = S.actual(P, t + h)
                av, mv = (a or {}).get(key), m[h].get(key)
                if av is None or mv is None:
                    cells.append('%17s' % '—')
                else:
                    cells.append('%8.0f /%8.0f' % (mv, av))
            print('%-20s %s' % (label, '  '.join(cells)))
        print('%-20s %s' % ('(proj / actual)', ''))


if __name__ == '__main__':
    main()
