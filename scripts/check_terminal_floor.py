#!/usr/bin/env python3
"""[R-TERM-01] enforced from outside the study — the terminal floor.

A company can always decline to invest beyond maintenance and pay the rest out. So a
terminal value can never honestly be worth less than a no-growth perpetuity on the same
profit:

    TV  >=  NOPAT_last / W_terminal

That is a DOMINANCE argument, not a judgement. It has no parameters, so there is nothing in
it to tune, and it needs no view on the return on capital, the capital basis, asset lives or
growth. A terminal below it is dominated by a policy the company can choose unilaterally,
and a study publishing it has chosen the worse of two worlds.

WHY A GATE AND NOT A NOTE. The construction that produces the breach is invisible to every
other check in this repository, because nothing in it is arithmetically wrong. The
reinvestment identity rr = g/ROIC collapses to TV = [NOPAT - g.IC]/(W-g), so it charges
g x IC for ever; read as a maintenance programme that implies replacing the whole asset base
every 1/g years. THE IMPLIED ASSET LIFE IS THE RECIPROCAL OF THE INFLATION RATE, which is
not a fact about the asset — and the workbook still recalculates to the cell, the provenance
is still four-field complete, the external-reader scrub is still clean. It is a
SPECIFICATION error, and [R-FCAL-01] already says of that class that no correction factor
may hide it.

RATCHETED per [R-ENF-02]: studies already breaching are listed in
engine/build_depth_audit/terminal_outstanding.json and allowed to fail; the build breaks on
a NEW breach or a study directory that becomes readable and breaches with no entry. The list
may only ever SHORTEN (--prune).

THE TWO RATCHET GROUPS EXCUSE TWO DIFFERENT CONDITIONS AND ARE NOT INTERCHANGEABLE. An
allowance under `breaching` says "this study publishes a terminal below its floor and we
know"; one under `unreadable` says "this study exposes no terminal to test and we know".
A study filed under the wrong one is NOT excused, and that is deliberate: an entry that
travels between groups would let a name escape a real breach by being re-filed as merely
unreadable, which is the cheapest route past any gate [R-ENF-04]. This control's own case 10
originally asserted the opposite and the gate refused it — the fixture was wrong, not the
gate, and the case was replaced with the boundary test instead.

POPULATION-ANCHORED per [R-ENF-04]: a run that examined zero studies FAILS; a run that
read zero terminals FAILS; every listed ticker must resolve on disk. An unreadable terminal
is TRACKED, not skipped — an unreadable answer is not a clean answer, and nine of
twenty-four study directories were in that state when this gate was written.

READ THE POPULATION LIVE — python3 scripts/check_terminal_floor.py — never from a document.
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, REPO)

from engine.valuation_calibration.terminal_census import census, _fv_at   # noqa: E402

RATCHET = os.path.join(REPO, 'engine', 'build_depth_audit', 'terminal_outstanding.json')


def load_ratchet():
    if not os.path.exists(RATCHET):
        return {'breaching': {}, 'unreadable': {}}
    d = json.load(open(RATCHET))
    d.setdefault('breaching', {})
    d.setdefault('unreadable', {})
    return d


def main(argv):
    prune = '--prune' in argv
    rat = load_ratchet()
    rows = census()
    read = [r for r in rows if 'unreadable' not in r]
    dark = [r for r in rows if 'unreadable' in r]
    scored = [r for r in read if 'floor' in r]

    print('TERMINAL FLOOR GATE  [R-TERM-01]')
    print('   a terminal can never be worth less than not investing at all: TV >= NOPAT/W')
    print('   %d study directories · %d readable · %d with a scoreable terminal'
          % (len(rows), len(read), len(scored)))

    fail = []

    # ---- population anchoring, both ways [R-ENF-04] -----------------------------------
    if not rows:
        print('\nFAIL — the gate examined ZERO study directories. An empty result is not a '
              'clean result.')
        return 1
    if not scored:
        print('\nFAIL — the gate read ZERO terminals across %d study directories. That is '
              'an absent answer wearing the costume of a clean one.' % len(rows))
        return 1
    on_disk = {r['ticker'] for r in rows}
    for group in ('breaching', 'unreadable'):
        for tk in sorted(rat[group]):
            if tk not in on_disk:
                fail.append('ratchet lists %s under %s and no such study directory exists '
                            '— the list is anchored on nothing' % (tk, group))

    # ---- the floor --------------------------------------------------------------------
    breach = [r for r in scored if r.get('below_floor')]
    ok = [r for r in scored if not r.get('below_floor')]
    print('\n  BELOW THE FLOOR: %d of %d' % (len(breach), len(scored)))
    for r in sorted(breach, key=lambda r: r['tv_vs_floor']):
        tk = r['ticker']
        known = tk in rat['breaching']
        fv0, fv1 = r.get('fv'), _fv_at(r, r['floor'])
        px = ('   %.2f -> %.2f at the floor' % (fv0, fv1)) if (fv0 and fv1) else ''
        print('    %-12s%+8.1f%%%s%s' % (tk, 100 * r['tv_vs_floor'], px,
                                         '' if known else '   *** NEW ***'))
        if not known:
            fail.append('%s publishes a terminal %.1f%% below its own floor and is not on '
                        'the ratchet. A company can always decline to invest and pay out '
                        'instead, so this terminal is dominated by a policy it can choose '
                        'unilaterally.' % (tk, 100 * r['tv_vs_floor']))

    # ---- the 1/g signature, reported whether or not it breaches -----------------------
    sig = [r for r in scored
           if r.get('implied_cycle_years') and r.get('one_over_g')
           and abs(r['implied_cycle_years'] / r['one_over_g'] - 1.0) < 0.02]
    if sig:
        print('\n  THE 1/g SIGNATURE — the implied replacement cycle equals the reciprocal of')
        print('  the growth rate, which is the fingerprint of a g x IC charge:')
        for r in sig:
            print('    %-12s%6.1f years against 1/g of %5.1f'
                  % (r['ticker'], r['implied_cycle_years'], r['one_over_g']))

    # ---- unreadable is tracked, never skipped ----------------------------------------
    print('\n  TERMINAL NOT READABLE: %d' % len(dark))
    for r in dark:
        tk = r['ticker']
        if tk not in rat['unreadable']:
            fail.append('%s exposes no readable terminal (%s) and is not on the ratchet. '
                        'An unreadable answer is not a clean answer [R-ENF-04].'
                        % (tk, r['unreadable']))
            print('    %-12s%s   *** NEW ***' % (tk, r['unreadable']))
        else:
            print('    %-12s%s' % (tk, r['unreadable']))

    # ---- the ratchet may only SHORTEN ------------------------------------------------
    now_breach = {r['ticker'] for r in breach}
    now_dark = {r['ticker'] for r in dark}
    cleared = (set(rat['breaching']) - now_breach) | (set(rat['unreadable']) - now_dark)
    if cleared:
        print('\n  CLEARED since the list was written: %s' % ', '.join(sorted(cleared)))
        if prune:
            for tk in cleared:
                rat['breaching'].pop(tk, None)
                rat['unreadable'].pop(tk, None)
            json.dump(rat, open(RATCHET, 'w'), indent=1, sort_keys=True)
            print('  --prune: the list has been SHORTENED. It may never grow.')
        else:
            print('  run with --prune to shorten the list. It may never grow.')

    if fail:
        print('\nFAIL — %d new violation(s):' % len(fail))
        for m in fail:
            print('   * %s' % m)
        return 1
    print('\nOK — no new terminal sits below its own floor, no newly unreadable terminal, '
          'and the list has not grown.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
