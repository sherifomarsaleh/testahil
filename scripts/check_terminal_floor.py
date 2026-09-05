#!/usr/bin/env python3
"""[R-TERM-01] enforced from outside the study — the 1/g signature.

THE FILENAME SAYS "floor" AND THE TEST IS THE SIGNATURE. The name is kept because CI, the
workflow paths and the ratchet all address this file, and a rename mid-flight is how a gate
stops running while everything still says it does — [L-067], a check that opens a file by
name. What it tests is stated here and in every line it prints.

WHAT THIS GATE TESTS, and it took two tries to point it at the right thing. The
reinvestment identity rr = g/ROIC substitutes to TV = [NOPAT(1+g) - g.IC]/(W-g), so the
construction charges g x IC every year for ever. Read that charge as a capital-maintenance
programme and the implied replacement cycle is

    IC / charge  =  (NOPAT/ROIC) / (NOPAT . g/ROIC)  =  1 / g        EXACTLY

so a terminal built on the identity ALWAYS implies replacing its whole capital base every
1/g years. THE IMPLIED ASSET LIFE IS THE RECIPROCAL OF THE GROWTH RATE — a fact about the
inflation path and not about the asset, and worse the higher inflation goes, which is the
exact opposite of prudence. Because the algebra is exact rather than approximate, this is a
CLEAN DETECTOR: a terminal whose implied cycle equals 1/g is built on the identity, and one
whose cycle does not is built on something else.

WHY THE FLOOR IS NOT THE TEST, recorded because the first version of this gate thought it
was. `TV >= NOPAT/W` looked like a dominance argument — a company can always decline to
invest and pay out. It is not one: NOPAT is net of BOOK depreciation, struck on historical
cost, so distributing NOPAT for ever while owing current-cost replacement is not an
available policy, and "zero NOMINAL growth" is not a choice a board can make. Measured
across the book it also does not separate the class: of the six studies carrying the g x IC
construction, only two sit below that floor and four sit comfortably above it. THE FLOOR
FOUND THE DEFECT ON ONE NAME AND WOULD HAVE MISSED IT ON FOUR. It is still printed, as a
diagnostic, labelled for what it is.

WHY A GATE AND NOT A NOTE. Nothing in the construction is arithmetically wrong, so every
other check in this repository passes it: the workbook recalculates to the cell, provenance
is four-field complete, the external-reader scrub is clean. It is a SPECIFICATION error, and
[R-FCAL-01] already says of that class that no correction factor may hide it.

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
        return {'breaching': {}, 'unreadable': {}, 'unscored': {}}
    d = json.load(open(RATCHET))
    d.setdefault('breaching', {})
    d.setdefault('signature', {})
    d.setdefault('unreadable', {})
    d.setdefault('unscored', {})
    return d


def main(argv):
    prune = '--prune' in argv
    rat = load_ratchet()
    rows = census()
    read = [r for r in rows if 'unreadable' not in r]
    dark = [r for r in rows if 'unreadable' in r]
    scored = [r for r in read if 'floor' in r]
    # THE THIRD BUCKET, AND IT WAS FALLING THROUGH [ADDED 05-Sep-2026]. A study is
    # `dark` when no terminal resolves at all and `scored` when the charge it levies can
    # be derived. Between them sits a state this gate did not name: the terminal
    # RESOLVES — g and the terminal rate both read — and the charge does NOT, because
    # some component of it (terminal NOPAT, invested capital, the terminal value itself)
    # is not exposed. Those studies were counted in `read`, excluded from `scored`, and
    # then mentioned nowhere; the gate printed OK having said nothing about them.
    #
    # ELEC is what found it. engine/elec_study/compute.py builds its terminal as
    #     roic_T = nop_T / ic_T ; rr_T = g / roic_T ; tv = nop_T (1+g)(1-rr_T)/(W-g)
    # which is the retired reinvestment identity in plain sight, and this gate reported
    # "no new terminal carries the 1/g construction" while it sat there — because the
    # census cannot recover its terminal NOPAT and so never scored the charge. A gate
    # blind to the exact construction it exists to find is the [R-ENF-04] failure in its
    # usual costume: an ABSENT answer wearing a clean one's clothes.
    unscored = [r for r in read if 'floor' not in r]

    print('TERMINAL CONSTRUCTION GATE  [R-TERM-01]')
    print('   the implied replacement cycle is 1/g whenever the terminal is built on the')
    print('   reinvestment identity — so the asset life is the reciprocal of the GROWTH RATE')
    print('   %d study directories · %d readable · %d with a scoreable terminal · '
          '%d read but not scoreable'
          % (len(rows), len(read), len(scored), len(unscored)))

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
    for group in ('breaching', 'signature', 'unreadable', 'unscored'):
        for tk in sorted(rat[group]):
            if tk not in on_disk:
                fail.append('ratchet lists %s under %s and no such study directory exists '
                            '— the list is anchored on nothing' % (tk, group))

    # ---- THE 1/g SIGNATURE — the failing test ------------------------------------------
    sig = [r for r in scored
           if r.get('implied_cycle_years') and r.get('one_over_g')
           and abs(r['implied_cycle_years'] / r['one_over_g'] - 1.0) < 0.02]
    clean = [r for r in scored if r not in sig]
    moved = []
    print('\n  CARRYING THE 1/g CONSTRUCTION: %d of %d' % (len(sig), len(scored)))
    for r in sorted(sig, key=lambda r: r['one_over_g']):
        tk = r['ticker']
        # A NAME THAT WAS ON THE UNREADABLE LIST AND HAS BECOME READABLE IS ALREADY
        # RATCHETED, AND THE DIRECTION OF THE MOVE IS THE WHOLE ARGUMENT [ADDED
        # 03-Sep-2026]. The two groups are deliberately NOT interchangeable and this
        # control's own case 10 proves it: re-filing a BREACHING study as UNREADABLE
        # hides a known defect behind an absence, which is the cheapest route past any
        # gate [R-ENF-04]. The reverse move hides nothing. When the census learned to read
        # SCEM and BOROUGE — by deriving g from the reinvestment rate and the return they
        # already publish, and by recognising that a study with ONE rate for every year has
        # no terminal rate to expose — both turned out to carry the 1/g construction they
        # had carried all along. Nothing about either study changed; what changed is that
        # the instrument can now see them, and SCEM's terminal is 34% below its own floor,
        # the worst in the book, which was invisible while it counted as unreadable.
        # Failing that as a NEW violation would punish the census for learning to read and
        # would make widening a reader more expensive than leaving studies dark — the exact
        # incentive [R-ENF-04] exists to remove. So the allowance TRAVELS one way only, and
        # the entry is rewritten into the group that now describes it.
        # `unscored` travels the same way and for the same reason [ADDED 05-Sep-2026]:
        # a study whose charge the census could not derive was never TESTED, so learning
        # to score it and finding the construction is the instrument improving rather
        # than the study getting worse. The move toward `signature` is free; the move
        # away from it stays refused.
        known = (tk in rat['signature'] or tk in rat['unreadable']
                 or tk in rat['unscored'])
        if tk not in rat['signature'] and (tk in rat['unreadable']
                                           or tk in rat['unscored']):
            moved.append(tk)
        print('    %-12s implied cycle %6.1f years against 1/g of %5.1f   '
              'charge %5.1f%% of terminal profit%s'
              % (tk, r['implied_cycle_years'], r['one_over_g'],
                 100 * r['charge_share_of_nopat'], '' if known else '   *** NEW ***'))
        if not known:
            fail.append('%s builds its terminal on the reinvestment identity: its implied '
                        'replacement cycle is %.1f years against 1/g of %.1f, so the asset '
                        'life is the reciprocal of the growth rate rather than a fact about '
                        'the asset. Build it through engine/terminal_value.py on a DISCLOSED '
                        'useful life.' % (tk, r['implied_cycle_years'], r['one_over_g']))
    if clean:
        print('  built on something else (the cycle does not equal 1/g): %s'
              % ', '.join(sorted(r['ticker'] for r in clean)))

    # ---- the floor, a DIAGNOSTIC and not a bar -----------------------------------------
    breach = [r for r in scored if r.get('below_floor')]
    print('\n  DIAGNOSTIC — below a NOPAT perpetuity at book depreciation: %d of %d'
          % (len(breach), len(scored)))
    print('  NOT A BAR. That figure assumes a maintenance charge the company does not face,')
    print('  so it is not an available policy and cannot dominate anything; and it does not')
    print('  separate the class — four of the studies carrying the construction sit ABOVE it.')
    for r in sorted(breach, key=lambda r: r['tv_vs_floor']):
        fv0, fv1 = r.get('fv'), _fv_at(r, r['floor'])
        px = ('   %.2f -> %.2f there' % (fv0, fv1)) if (fv0 and fv1) else ''
        print('    %-12s%+8.1f%%%s' % (r['ticker'], 100 * r['tv_vs_floor'], px))

    # ---- frame mixing is reported, because it manufactured a breach once ---------------
    mixed = [r for r in read if r.get('off_frame')]
    if mixed:
        print('\n  FIELDS READ FROM ANOTHER FRAME — recorded, never silent. Reading a terminal')
        print('  value from one framing and its NOPAT from another produced a PLAUSIBLE and')
        print('  FABRICATED breach on FERTIGLOBE: a floor of 8,174 against its own 5,347.')
        for r in mixed:
            print('    %-12s%s' % (r['ticker'], '; '.join(r['off_frame'][:3])))

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

    # ---- read but not scoreable is tracked, never skipped -----------------------------
    # Same discipline as the line above and for the same reason: a charge that cannot be
    # derived is not a charge that is sound. These studies are NOT excused the 1/g test —
    # they are recorded as untested, which is the honest state and the one a reader can
    # act on.
    print('\n  READ BUT NOT SCOREABLE: %d' % len(unscored))
    for r in sorted(unscored, key=lambda r: r['ticker']):
        tk = r['ticker']
        why = ', '.join('no ' + f for f in ('nopat_term', 'ic', 'tv')
                        if r.get(f) is None) or 'the charge is not derivable'
        if tk not in rat['unscored']:
            fail.append('%s exposes a terminal whose charge cannot be derived (%s) and is '
                        'not on the ratchet. The 1/g test never ran on it, and an untested '
                        'terminal is not a clean terminal [R-ENF-04].' % (tk, why))
            print('    %-12s%s   *** NEW ***' % (tk, why))
        else:
            print('    %-12s%s' % (tk, why))

    # ---- the ratchet may only SHORTEN ------------------------------------------------
    now_sig = {r['ticker'] for r in sig}
    now_dark = {r['ticker'] for r in dark}
    now_unscored = {r['ticker'] for r in unscored}
    if moved:
        print('\n  BECAME READABLE AND WERE ALREADY RATCHETED (%d): %s'
              % (len(moved), ', '.join(sorted(moved))))
        print('    the allowance moves from `unreadable` or `unscored` to `signature` — '
              'the defect was always there and the census could not see it. The reverse '
              'move stays refused: a known breach re-filed behind an absence is the '
              'escape hatch.')
    # A NAME THAT MOVED GROUPS HAS NOT CLEARED, AND SAYING SO IS NOT A DETAIL: it is no
    # longer in `now_dark`, so the plain arithmetic below reads it as cleared, --prune
    # would DROP it, and the very next run would fail it as a NEW violation — a ratchet
    # that empties itself and then goes red is worse than one that never shortened.
    cleared = ((set(rat['signature']) - now_sig - now_unscored)
               | (set(rat['unreadable']) - now_dark - now_sig - now_unscored)
               | (set(rat['unscored']) - now_unscored - now_sig)
               | set(rat['breaching']))
    # A MOVE IS A REWRITE EVEN WHEN NOTHING CLEARED [FIXED 05-Sep-2026]. The rewrite of a
    # travelled entry sat inside `if cleared:`, so a run where an entry moved groups and
    # nothing else cleared printed the move and wrote nothing — and reported the move again
    # on every subsequent run, for ever. ELEC found it: it travelled from `unscored` to
    # `signature`, `cleared` was empty by the very guard that keeps a moved name from
    # reading as cleared, and --prune was a no-op.
    if cleared or moved:
        if cleared:
            print('\n  CLEARED since the list was written: %s' % ', '.join(sorted(cleared)))
        if prune:
            for tk in moved:
                whence = 'unreadable' if tk in rat['unreadable'] else 'unscored'
                rat['signature'][tk] = (
                    'terminal built on the reinvestment identity: implied cycle equals 1/g. '
                    'MOVED FROM `%s` — it was always breaching and the census could not '
                    'score it; the allowance travels this way and never the other. Gets '
                    'engine/terminal_value.py and a DISCLOSED useful life at its next '
                    're-issue.' % whence)
                rat['unreadable'].pop(tk, None)
                rat['unscored'].pop(tk, None)
            for tk in cleared:
                rat['breaching'].pop(tk, None)
                rat['signature'].pop(tk, None)
                rat['unreadable'].pop(tk, None)
                rat['unscored'].pop(tk, None)
            json.dump(rat, open(RATCHET, 'w'), indent=1, sort_keys=True)
            print('  --prune: the list has been SHORTENED. It may never grow.')
        else:
            print('  run with --prune to shorten the list. It may never grow.')

    if fail:
        print('\nFAIL — %d new violation(s):' % len(fail))
        for m in fail:
            print('   * %s' % m)
        return 1
    print('\nOK — no new terminal carries the 1/g construction, no newly unreadable '
          'terminal, no newly unscoreable one, and the list has not grown.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
