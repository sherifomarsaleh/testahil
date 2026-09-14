#!/usr/bin/env python3
"""A REBUILT STUDY RECORDS THE ROUTE IT TOOK, NOT ONLY WHERE IT ARRIVED [R-ENF-01].

    python3 scripts/check_rebuild_ledger.py [--prune]

WHY THIS EXISTS. [R-VCAL-01]'s promotion guard is explicit about stacking: one lever at
a time, in an order fixed in advance, halted the moment the stacked bias would cross
zero, and it names the failure it guards against — "stacking five individually-justified
moves into an overshoot, the exact failure that called this reassessment". It governs
levers promoted FROM the valuation calibration.

A REBUILD IS THE SAME SHAPE AND WAS GOVERNED BY NOTHING, because it applies rules that
already bind rather than levers seeking promotion, so nobody read the guard as covering
it. On 4 September 2026 one study took six corrections in an afternoon and moved from
55% below the market to 71% below it, through +45% on the way. Every correction was
required by a standing rule. Every one was right. The running total was looked at once,
at the end.

WHAT THIS CHECKS. Not the size of the move — a study wrong in six ways moves a long way
when all six are fixed, and a threshold here would be the free parameter the promotion
rule forbids. It checks that a study whose committed answer has MOVED since its last
delivered edition carries a ledger that can be WALKED: the levers in order, each
starting where the last one ended, each naming the rule it serves, and an audit point
declared in advance.

THE GROUPING IS THE POINT. Several levers serving ONE rule are one piece of evidence.
The study above ran three levers of the house macro path — the inflation ladder, the
currency derived from it, the terminal risk-free derived from it — and between them they
took 56% off a value the terminal correction had just raised by 45%. Read as six
independent corrections that is a landslide; read as two rules pulling opposite ways it
is a contest, which is what it was.

THE POPULATION is the study directories on disk [R-ENF-04]. A run that examined zero
studies FAILS. Ratcheted [R-ENF-02]: every study whose delivered edition predates this
rule is listed and allowed to have no ledger, and the list may only ever SHORTEN.
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, 'engine')
sys.path.insert(0, ENGINE)

import rebuild_ledger as RL                                          # noqa: E402

OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'rebuild_outstanding.json')


def studies():
    """The record directories a record-reading gate can inspect, resolved through
    engine/study_population.py rather than by globbing engine/*_study.

    THE GLOB WAS THE WRONG POPULATION. All 90 covered names carry a delivered
    valuation study; 23 commit a record. This gate globbed the directories and
    printed a count with NO DENOMINATOR, which is why 24 looked like the book.
    The names with no record are DEFERRED to the shared no-record ratchet, which
    the valuation-gap gate reports on — they are not re-listed here, because ten
    gates reporting one fact is the duplication this refactor exists to avoid.

    The import is LAZY so a sandbox that copies this script without engine/
    beside it does not die on an import it never needed.
    """
    global _DEFERRED, _POP_LINE
    # A SANDBOXED FIXTURE SUPPLIES ITS OWN POPULATION, AND SAYS SO OUT LOUD.
    # Several negative controls copy this script into a temp tree holding a fake
    # ENGINE and run it as a subprocess, so the resolver is not importable there —
    # and it should not be, because the whole point of those fixtures is a
    # population they control. The escape is an explicit environment variable that
    # CI never sets, and taking it PRINTS that it was taken: a switch that quietly
    # restored the directory glob would reinstate the defect this replaced.
    if os.environ.get('TESTAHIL_FIXTURE_POPULATION'):
        dirs = sorted(glob.glob(os.path.join(ENGINE, '*_study')))
        _DEFERRED, _POP_LINE = [], ('population: FIXTURE — %d study directories under a '
                                    'sandboxed ENGINE, not the book' % len(dirs))
        print(_POP_LINE)
        return dirs
    if ENGINE not in sys.path:
        sys.path.insert(0, ENGINE)
    import study_population
    dirs, _DEFERRED, _POP_LINE = study_population.examinable()
    # printed HERE so the ten gates have exactly ONE edit site each and the line
    # cannot be forgotten in one of them: a denominator that appears in nine gates
    # and not the tenth is the drift this refactor exists to stop
    print(_POP_LINE)
    return dirs


_DEFERRED, _POP_LINE = [], ""


def main(argv):
    prune = '--prune' in argv
    d, known = {}, set()
    if os.path.exists(OUTSTANDING):
        d = json.load(open(OUTSTANDING, encoding='utf-8'))
        known = set(d.get('outstanding', []))

    dirs = studies()
    if not dirs:
        print('FAIL — the population is empty: no engine/*_study directories found '
              '[R-ENF-04].')
        return 1

    have, bad, absent = [], {}, []
    for dd in dirs:
        tk = os.path.basename(dd)[:-6].upper()
        p = os.path.join(dd, 'rebuild_ledger.json')
        if not os.path.exists(p):
            absent.append(tk)
            continue
        try:
            rec = json.load(open(p, encoding='utf-8'))
        except Exception as e:                                       # noqa: BLE001
            bad.setdefault(tk, []).append('rebuild_ledger.json will not parse: %s' % e)
            continue
        try:
            RL.assert_rebuild(rec, tk)
        except RL.RebuildRefused as e:
            bad.setdefault(tk, []).append(str(e).split('\n', 1)[-1].strip())
            continue
        have.append((tk, rec))

    print('REBUILD LEDGERS  [R-ENF-01 applied to the route rather than the answer]')
    print('   %d study directories · %d carry a ledger · %d do not'
          % (len(dirs), len(have), len(absent)))
    if not have and not bad:
        print('\nFAIL — %d study directories and not one rebuild ledger was read. Either '
              'no study has been rebuilt since this rule, which the ratchet would show, '
              'or this gate is looking in the wrong place [R-ENF-04].' % len(dirs))
        return 1
    print()
    for tk, rec in sorted(have):
        rules = rec['rules']
        top = sorted(rules.items(), key=lambda kv: -abs(kv[1]['move']))
        print('  %-12s %d lever(s), %d rule(s), cumulative %+.1f%%'
              % (tk, len(rec['levers']), len(rules), 100 * rec['cumulative_move']))
        for rule, g in top:
            print('      %-16s %+7.1f%%  %d lever(s)'
                  % (rule, 100 * g['move'], len(g['levers'])))

    unlisted = sorted(t for t in absent if t not in known)
    if prune:
        still = sorted(t for t in known if t in absent)
        json.dump({'outstanding': still, 'note': d.get('note', '')},
                  open(OUTSTANDING, 'w', encoding='utf-8'), indent=1)
        print('\npruned: %d -> %d' % (len(known), len(still)))
        return 0

    if bad:
        print()
        for tk in sorted(bad):
            for line in bad[tk]:
                print('   %-12s %s' % (tk, line))
        print('\nFAIL — %d ledger(s) cannot be walked: %s'
              % (len(bad), ', '.join(sorted(bad))))
        return 1
    if unlisted:
        print('\nFAIL — %d study/studies carry no rebuild ledger and no entry either way: '
              '%s' % (len(unlisted), ', '.join(unlisted)))
        return 1
    print('\nOK — every ledger walks from its start to its answer, and %d study/studies '
          'on the ratchet have none, which may only SHORTEN.' % len(known))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
