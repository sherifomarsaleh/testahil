#!/usr/bin/env python3
"""Negative control for the delivered-bibliography source check [R-ENF-01].

Fourteen conditions, six red and EIGHT CLEAN, and the clean half is the half that
decides this one: the instrument's first draft flagged 34 rows across six studies and
the largest class was PEER MULTIPLES, every one of them the construction SIGCM clause
5 requires. A control proving only that an aggregator citation fires would say nothing
about the 12,639 rows that must stay silent.

It writes nothing: every fixture is a list of cells built in memory and handed to
engine/source_integrity.py directly. The four rows the book actually ships are pulled
from the DELIVERED DOCUMENTS AT RUN TIME rather than transcribed, so a control cannot
drift from what it claims to reproduce.

EVERY MUTATION ASSERTS THAT IT LANDED.
"""
from __future__ import annotations

import glob
import html
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'engine'))
sys.path.insert(0, HERE)

import source_integrity as SI                                        # noqa: E402
import importlib                                                     # noqa: E402
G = importlib.import_module('check_bibliography_sources')             # noqa: E402

CASES = 14


def shipped(ticker, needle):
    """The row the named study actually ships, read out of its delivered document."""
    d = os.path.join(ROOT, 'engine', '%s_study' % ticker.lower())
    for f in G.latest_editions(d):
        try:
            rs = G.rows_of(f)
        except Exception:                                            # noqa: BLE001
            continue
        for cells in rs:
            if needle.lower() in ' | '.join(cells).lower():
                return cells
    return None


def main() -> int:
    ok, bad = 0, []

    def case(n, what, want_red, cells, landed):
        nonlocal ok
        if cells is None:
            bad.append('%d %s — THE FIXTURE IS NOT PRESENT IN THE BOOK' % (n, what))
            return
        if not landed(cells):
            bad.append('%d %s — THE FIXTURE DID NOT LAND' % (n, what))
            return
        why = SI.document_row_violation(cells)
        red = bool(why)
        if red == want_red:
            ok += 1
        else:
            bad.append('%d %s — wanted %s, got %s%s'
                       % (n, what, 'RED' if want_red else 'quiet',
                          'RED' if red else 'quiet', (': ' + why[:60]) if why else ''))

    has = lambda s: (lambda c: s.lower() in ' | '.join(c).lower())    # noqa: E731

    # ---- RED: rows the book ships, exactly as they ship
    case(1, "AMOC's aggregator row exactly as delivered", True,
         shipped('AMOC', 'Company financial summary pages'),
         has('stockanalysis.com'))
    case(2, "ELEC's Simply Wall St balance-sheet row as delivered", True,
         shipped('ELEC', 'Balance-sheet health snapshot'), has('Simply Wall St'))
    case(3, "SCEM's trade-press FY2024 profit row as delivered", True,
         shipped('SCEM', 'FY2024 turnaround'), has('Global Cement'))
    # ---- RED: constructed shapes
    case(4, 'a relayed venue — "EGX filing reported by Bloomberg"', True,
         ['ta_fy2024', '10,000', 'FY2024 total assets as reported by Bloomberg'],
         has('reported by Bloomberg'))
    case(5, 'revenue for a named past year sourced to Refinitiv alone', True,
         ['Revenue', 'FY2023', 'EGP 4.2bn', 'Refinitiv company financials'],
         has('Refinitiv'))
    case(6, 'net profit sourced to a news outlet with no filing named', True,
         ['Net profit FY2025', 'EGP 1.1bn', 'Daily News Egypt'],
         has('Daily News Egypt'))

    # ---- CLEAN: work that is RIGHT and must stay silent
    case(7, 'a PEER multiple off an aggregator — SIGCM clause 5, as ADNOCDIST ships it',
         False, shipped('ADNOCDIST', 'Peer multiple'), has('peer multiple'))
    case(8, 'a forward REVENUE TARGET inside a budget announcement, as AMOC ships it',
         False, shipped('AMOC', 'planning budget'), has('budget'))
    case(9, 'a non-Company sweep ring carrying an industry figure', False,
         ['I-04', 'Industry', 'Supporting', 'Egyptian cement demand 2024', 'Global Cement'],
         has('| Industry |'))
    case(10, 'the same balance-sheet claim WITH the audited statements named', False,
          ['Total assets, total liabilities, cash', 'FY2025',
           'Audited consolidated financial statements FY2025, statement of financial '
           'position; cross-checked against stockanalysis.com'],
          has('Audited consolidated financial statements'))
    case(11, 'an aggregator cited for a MARKET quantity, which is not a statement line',
          False, ['Market capitalisation', 'Aug 2026', 'TradingView'],
          has('TradingView'))
    case(12, 'a statement line with NO period named — not a dated historical', False,
          ['Total assets', 'stockanalysis.com company page'], has('stockanalysis.com'))
    case(13, 'a dated statement line from the filing itself, no vendor anywhere', False,
          ['Revenue FY2025', 'EGP 4.2bn', 'Audited statements, note 4'],
          has('note 4'))
    case(14, 'an empty row', False, [], lambda c: c == [])

    print('bibliography sources negative control — %s %d/%d'
          % ('PASS' if not bad else 'FAILED', ok, CASES))
    for b in bad:
        print('  - ' + b)
    if ok + len(bad) != CASES:
        print('  - CASE COUNT: %d ran against a declared %d' % (ok + len(bad), CASES))
        return 1
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
