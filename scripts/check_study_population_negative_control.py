#!/usr/bin/env python3
"""Negative control for engine/study_population.py.

A resolver nobody has seen REFUSE is not evidence.  This one exists because
the population it replaces was wrong for a month while 77 gates reported
themselves population-anchored against it, so the ways it can be wrong are
the ways that actually happened rather than the ways that are easy to test.

EVERY MUTATION ASSERTS THAT IT LANDED before the resolver runs.  Three
negative controls in this repository have been caught passing a fixture
that never injected its condition; a control that proves the code is
unchanged proves nothing.

CASE 8 IS THE ONE THAT MATTERS: the defect that produced the wrong answer
was a CASE-SENSITIVE stem match, which silently dropped `Aramco_`,
`Samsung_`, `Aldar_` and `Kakao_` and reported sixteen names as having no
study.  It must stay resolvable, and a mutation that makes the matcher
case-sensitive again must be CAUGHT rather than merely return fewer names.
"""

import importlib.util
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECLARED_CASES = 13


def _load():
    p = os.path.join(ROOT, 'engine', 'study_population.py')
    spec = importlib.util.spec_from_file_location('_sp_nc', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _refuses(fn):
    """True iff the resolver REFUSES rather than returning a short list."""
    try:
        fn()
    except SystemExit:
        return True
    except AssertionError:
        return True
    return False


def main():
    results = []

    def case(n, name, expect_red, fn, landed):
        assert landed(), ('case %d (%s): THE MUTATION DID NOT LAND. A control that '
                          'never injected its condition proves only that the code is '
                          'unchanged.' % (n, name))
        red = _refuses(fn)
        ok = (red == expect_red)
        results.append((n, name, 'RED' if red else 'green',
                        'RED' if expect_red else 'green', ok))

    m = _load()
    base = m.population()
    assert len(base) == 90, 'the clean population is not 90 -- fixture is stale'

    # 1. an alias removed: a covered name stops resolving to its delivered study
    m1 = _load()
    m1.FILE_ALIAS = {k: v for k, v in m1.FILE_ALIAS.items() if k != 'AL_RAJHI'}
    case(1, 'alias table short: ALRAJHI resolves to no delivered study', True,
         m1.population, lambda: 'AL_RAJHI' not in m1.FILE_ALIAS)

    # 2. a delivered stem resolving to no covered ticker
    m2 = _load()
    m2.NOT_AN_EQUITY = {}
    case(2, 'a metals stem declared nowhere', True,
         m2.population, lambda: m2.NOT_AN_EQUITY == {})

    # 3. files/ emptied -- the delivered studies ARE the anchor
    d3 = tempfile.mkdtemp()
    m3 = _load()
    m3.FILES = d3
    case(3, 'files/ empty: no delivered study to anchor on', True,
         m3.population, lambda: os.path.isdir(d3) and not os.listdir(d3))

    # 4. data.js exposing no TICKERS
    d4 = tempfile.mkdtemp()
    p4 = os.path.join(d4, 'data.js')
    open(p4, 'w').write('const TICKERS = {};\n')
    m4 = _load()
    m4.DATA_JS = p4
    case(4, 'data.js exposes no TICKERS: an empty result is not a clean one', True,
         m4.population, lambda: open(p4).read().strip().endswith('{};'))

    # 5. no study directories at all
    d5 = tempfile.mkdtemp()
    m5 = _load()
    m5.ENGINE = d5
    case(5, 'no engine/*_study directories', True,
         m5.population, lambda: os.path.isdir(d5) and not os.listdir(d5))

    # 6. a record directory for a name the site does not carry, undeclared
    d6 = tempfile.mkdtemp()
    for d in os.listdir(os.path.join(ROOT, 'engine')):
        if d.endswith('_study'):
            os.makedirs(os.path.join(d6, d), exist_ok=True)
    os.makedirs(os.path.join(d6, 'zznotcovered_study'), exist_ok=True)
    m6 = _load()
    m6.ENGINE = d6
    case(6, 'a study record for a name the site does not carry', True,
         m6.population, lambda: os.path.isdir(os.path.join(d6, 'zznotcovered_study')))

    # 7. CLEAN: the repository as it stands must resolve, all 90
    m7 = _load()
    case(7, 'the book as it stands: 90 covered, 90 delivered', False,
         m7.population, lambda: True)

    # 8. CLEAN, AND THE ONE THAT MATTERS: the mixed-case stems that started
    #    this must resolve. Asserted on the NAMES, not on the count, because
    #    a count can be right for the wrong reason.
    m8 = _load()
    pop8 = m8.population()
    mixed = ('ARAMCO', 'SAMSUNG', 'ALDAR', 'KAKAO', 'MAADEN', 'EMAAR')
    for tk in mixed:
        assert tk in pop8, 'case 8: %s did not resolve -- the case-sensitivity ' \
                           'defect is back' % tk
        assert pop8[tk]['delivered'], 'case 8: %s resolved with no delivered file' % tk
    case(8, 'mixed-case delivered stems (Aramco, Samsung, Aldar, Kakao) resolve',
         False, m8.population, lambda: all(t in pop8 for t in mixed))

    # ---- THE SHARED NO-RECORD RATCHET [added 06-09-2026 with the refactor that
    # moved it out of gap_outstanding.json before ten gates could each copy it].
    # Its three problem classes are the whole of its job, and the fourth case is
    # the one a first draft got wrong: an EMPTY ratchet is the GOAL STATE of a list
    # that may only shorten, so refusing it would make the target unreachable.
    import json as _j, tempfile as _t

    def _ratchet(mod, names):
        f = os.path.join(tempfile.mkdtemp(), 'nr.json')
        _j.dump({'no_record': sorted(names)}, open(f, 'w'))
        mod.NO_RECORD_RATCHET = f
        return f

    _base = _load()
    _pop = _base.population()
    _actual = sorted(k for k, v in _pop.items() if not v['readable'])
    assert len(_actual) > 2, 'fixture stale: the book has almost no unrecorded names'

    def _problems(names):
        m = _load(); _ratchet(m, names)
        return m.no_record_ratchet(m.population())[1]

    def case2(n, name, expect_problem, names, landed):
        assert landed(), 'case %d (%s): THE MUTATION DID NOT LAND.' % (n, name)
        probs = _problems(names)
        got = bool(probs)
        results.append((n, name, 'PROBLEM' if got else 'clean',
                        'PROBLEM' if expect_problem else 'clean', got == expect_problem))

    case2(9, 'a name on the ratchet that is not a covered name at all', True,
          _actual + ['ZZNOTABOOKNAME'], lambda: 'ZZNOTABOOKNAME' not in _pop)
    _withrec = sorted(k for k, v in _pop.items() if v['readable'])
    case2(10, 'a name excused on the ratchet that DOES commit a record', True,
          _actual + [_withrec[0]], lambda: _pop[_withrec[0]]['readable'])
    case2(11, 'a name with no record left OFF the ratchet — the new breach', True,
          _actual[1:], lambda: len(_actual[1:]) == len(_actual) - 1)
    case2(12, 'the book as it stands must be clean', False,
          _actual, lambda: True)
    case2(13, 'an EMPTY ratchet is the goal state, not a refusal — it reports every '
              'unlisted name instead', True, [], lambda: True)
    _base.NO_RECORD_RATCHET = _base.NO_RECORD_RATCHET

    assert len(results) == DECLARED_CASES, (
        'declared %d cases, ran %d. A control that quietly loses a case reports '
        'clean for the wrong reason.' % (DECLARED_CASES, len(results)))

    print('NEGATIVE CONTROL — engine/study_population.py')
    print('%d cases: %d must go red, %d must come back clean\n'
          % (len(results), sum(1 for r in results if r[3] == 'RED'),
             sum(1 for r in results if r[3] == 'green')))
    bad = 0
    for n, name, got, want, ok in results:
        print('  %s  %d. %-62s got %-5s want %s'
              % ('ok ' if ok else 'FAIL', n, name[:62], got, want))
        bad += (not ok)
    for d in (d3, d4, d5, d6):
        shutil.rmtree(d, ignore_errors=True)
    print()
    if bad:
        print('%d case(s) did not behave as declared.' % bad)
        return 1
    print('All %d behaved as declared.' % len(results))
    return 0


if __name__ == '__main__':
    sys.exit(main())
