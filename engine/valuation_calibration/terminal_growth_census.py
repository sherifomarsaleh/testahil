#!/usr/bin/env python3
"""EVERY STUDY'S TERMINAL GROWTH, RE-EXPRESSED AS THE REAL RATE IT ACTUALLY ASSUMES.

    python3 engine/valuation_calibration/terminal_growth_census.py

WHY THIS EXISTS. Terminal growth is typed as a NOMINAL rate in almost every study in this
book, and a nominal rate hides its own content: 4% is real growth of two points in a pegged
market and a real DECLINE of three in a high-inflation one, and nothing on the page says
which. [R-MACRO-01] already requires growth to be stored as (real, inflation path) and
recomputed to its nominal — and that rule's own amendment records why a declaration is not
enough: a check that reads what a process DECLARES is not checking what the process DOES.

WHAT PROVOKED IT. Two cable manufacturers, reviewed on the same day, carrying the same
defect with OPPOSITE SIGNS and neither writing it down:

    SWDY         5.0% nominal against Egypt's  7.0% terminal inflation  ->  -1.87% real
    RIYADHCABLE  4.0% nominal against Saudi's  2.0% terminal inflation  ->  +1.96% real

The first starves a going concern in perpetuity; the second grants it permanent real
expansion in a pegged economy. Both were defensible-looking numbers, both were typed, and
in neither study did any sentence state the real rate.

WHAT THIS DOES AND DOES NOT CLAIM. It reports; it does not judge. Real growth away from
zero is PERMITTED — [R-MACRO-01] requires only that it be STATED and that the incremental
capital it needs be charged. So a non-zero real rate here is a question to answer, not a
finding on its own. What it flags is the pair a reader should never have to compute: a real
rate the study does not state.

THE POPULATION is the study directories on disk [R-ENF-04]. A run that reads zero
terminals, or that resolves zero house paths, FAILS rather than reporting clean.
"""
import glob
import json
import re
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, ENGINE)

import macro_path as MP                                                # noqa: E402

# The market a study's own meta records, mapped to the house path's key. A study naming a
# market this cannot resolve is REPORTED as unresolved rather than skipped.
MARKET = {'EGX': 'EG', 'EG': 'EG', 'TADAWUL': 'SA', 'SA': 'SA', 'ADX': 'AE', 'DFM': 'AE',
          'AE': 'AE', 'QSE': 'QA', 'QA': 'QA', 'NSE': 'IN', 'IN': 'IN', 'KRX': 'KR',
          'KR': 'KR', 'NASDAQ': 'US', 'US': 'US'}


def terminal_inflation(mkt):
    p = MP.load(mkt)
    t = (p.raw.get('inflation') or {}).get('terminal') or {}
    return t.get('value'), p.raw.get('regime')


# THREE STATES, NOT TWO, AND THE FIRST DRAFT HAD TWO [R-COC-01].
# It asked only whether a REAL-GROWTH INPUT KEY exists, and printed "not stated" for
# every study without one -- which was FALSE of AIRARABIA, whose g_term justification
# says "about 0.5pp real" in as many words. A check that reads a KEY is not checking
# what the study SAYS, which is [R-MACRO-01 AMENDED]'s own lesson from the other side.
# The remedy differs by state, so the label has to: a SILENT study owes a disclosure,
# a PROSE-ONLY study owes the arithmetic moved into its register, and [R-MACRO-01]
# wants the STORED form because a typed nominal rate is unfalsifiable -- nobody can
# tell whether "about 0.5pp" was computed or asserted.
REAL_KEYS = ('g_term_real', 'real_growth_term', 'g_real')
_REAL_IN_PROSE = re.compile(r'(\d+(?:\.\d+)?)\s*(?:pp|%|percentage points?|points?)?\s*'
                            r'(?:in\s+)?real\b', re.I)


def _how_stated(D, real):
    """'stored' | 'prose' | 'silent' — and prose only counts if the figure AGREES."""
    I = D.get('inputs') or {}
    if any(k in I for k in REAL_KEYS):
        return 'stored'
    just = str(((I.get('g_term') or {}).get('source')) or '')
    for m in _REAL_IN_PROSE.finditer(just):
        try:
            said = float(m.group(1)) / 100.0
        except ValueError:                                           # noqa: PERF203
            continue
        # "about 0.5pp real" against a computed 0.49% agrees; a figure a point away
        # does not, and a WRONG statement is worse than none.
        if abs(abs(said) - abs(real)) <= 0.002:
            return 'prose'
    return 'silent'


def main():
    dirs = sorted(glob.glob(os.path.join(ENGINE, '*_study')))
    if not dirs:
        print('FAIL - no study directories found [R-ENF-04].')
        return 1

    rows, unread, unresolved = [], [], []
    for d in dirs:
        tk = os.path.basename(d)[:-6].upper()
        f = os.path.join(d, 'study_numbers.json')
        if not os.path.exists(f):
            unread.append((tk, 'no committed numbers file'))
            continue
        try:
            D = json.load(open(f, encoding='utf-8'))
        except Exception as e:
            unread.append((tk, 'numbers file will not parse: %s' % e))
            continue
        g = (D.get('dcf') or {}).get('g')
        if g is None:
            I = D.get('inputs') or {}
            rec = I.get('g_term') or {}
            g = rec.get('value') if isinstance(rec, dict) else None
        if not isinstance(g, (int, float)):
            unread.append((tk, 'exposes no terminal growth rate'))
            continue
        mkt_raw = (D.get('meta') or {}).get('market')
        mkt = MARKET.get(str(mkt_raw).upper())
        if not mkt:
            unresolved.append((tk, 'market %r does not resolve to a house path' % mkt_raw))
            continue
        try:
            pi, regime = terminal_inflation(mkt)
        except Exception as e:
            unresolved.append((tk, 'house path for %s: %s' % (mkt, e)))
            continue
        if not isinstance(pi, (int, float)):
            unresolved.append((tk, 'house path for %s states no terminal inflation' % mkt))
            continue
        real = (1.0 + g) / (1.0 + pi) - 1.0
        rows.append((tk, mkt, regime, g, pi, real, _how_stated(D, real)))

    if not rows:
        print('FAIL - %d study directories and not one terminal growth rate was read '
              '[R-ENF-04].' % len(dirs))
        return 1

    print('TERMINAL GROWTH, RE-EXPRESSED AS THE REAL RATE IT ASSUMES')
    print('   %d study directories · %d readable · %d not · %d unresolved market'
          % (len(dirs), len(rows), len(unread), len(unresolved)))
    print()
    print('  %-13s %-4s %-11s %8s %10s %9s   %s'
          % ('ticker', 'mkt', 'regime', 'nominal', 'inflation', 'REAL', 'states it?'))
    print('  ' + '-' * 74)
    for tk, mkt, regime, g, pi, real, stated in sorted(rows, key=lambda r: r[5]):
        flag = {'stored': '', 'prose': '   <- in prose only, not stored as a real rate',
                'silent': '   <- SILENT'}[stated]
        print('  %-13s %-4s %-11s %7.2f%% %9.2f%% %8.2f%%   %-6s%s'
              % (tk, mkt, (regime or '')[:11], 100 * g, 100 * pi, 100 * real,
                 stated, flag))
    print()
    away = [r for r in rows if abs(r[5]) > 0.005]
    silent = [r for r in away if r[6] == 'silent']
    print('  %d of %d assume a real terminal rate more than half a point from zero, and %d '
          'of those state it nowhere.' % (len(away), len(rows), len(silent)))
    if silent:
        print('  A real rate away from zero is PERMITTED and must be STATED, with the '
              'incremental')
        print('  capital it needs charged for. These are the ones a reader would have to '
              'compute:')
        for tk, mkt, regime, g, pi, real, _ in sorted(silent, key=lambda r: r[5]):
            print('     %-13s %+.2f%% real (%s, %s)' % (tk, 100 * real, mkt, regime))
    if unread:
        print('\n  NOT READABLE (%d) - an absent answer is not a clean one:' % len(unread))
        for tk, why in unread:
            print('     %-13s %s' % (tk, why))
    if unresolved:
        print('\n  MARKET UNRESOLVED (%d):' % len(unresolved))
        for tk, why in unresolved:
            print('     %-13s %s' % (tk, why))
    return 0


if __name__ == '__main__':
    sys.exit(main())
