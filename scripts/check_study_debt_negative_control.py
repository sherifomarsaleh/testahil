#!/usr/bin/env python3
"""Negative control for the recorded-debt count [R-ENF-01].

Eleven conditions, six red and FIVE CLEAN. The clean half matters because this gate
deliberately sets NO CEILING: a new standard legitimately adds entries on the day it is
adopted, so a fixture where the total GROWS must stay green, and a control proving only
that unknown keys fire would leave that untested.

It writes nothing into the tree: every fixture is a dict handed to study_debt.read_one
through a temp file under the session scratch, and the real ratchet directory is never
opened for writing [R-ENF-01 EXTENDED 07-09-2026].

EVERY MUTATION ASSERTS THAT IT LANDED.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'engine'))

import study_debt as SD                                            # noqa: E402

CASES = 11


def main() -> int:
    ok, bad = 0, []
    tmp = tempfile.mkdtemp(prefix='debt-nc-')

    def run(payload, name='fixture_outstanding.json'):
        p = os.path.join(tmp, name)
        with open(p, 'w', encoding='utf-8') as fh:
            json.dump(payload, fh)
        return SD.read_one(p)

    def case(n, what, want, payload, landed, name='fixture_outstanding.json'):
        nonlocal ok
        if not landed(payload):
            bad.append('%d %s — THE FIXTURE DID NOT LAND' % (n, what))
            return
        try:
            debt, unk = run(payload, name)
            got = ('unknown' if unk else
                   'debt:%d' % sum(len(v) for v in debt.values()))
        except SD.UnknownShape:
            got = 'refused'
        except Exception as exc:                                   # noqa: BLE001
            bad.append('%d %s — raised %s' % (n, what, type(exc).__name__))
            return
        if got == want:
            ok += 1
        else:
            bad.append('%d %s — wanted %r, got %r' % (n, what, want, got))

    has = lambda k: (lambda p: k in p)                             # noqa: E731

    # ---- RED / refused
    case(1, 'a key nobody has classified', 'unknown',
         {'wobbly': ['AMOC']}, has('wobbly'))
    case(2, 'a key that SOUNDS like a debt but is not on the list', 'unknown',
         {'pending_review': ['AMOC', 'ARCC']}, has('pending_review'))
    case(3, 'a top level that is neither list nor dict', 'refused',
         'a bare string', lambda p: isinstance(p, str))
    case(4, 'a second unclassified key beside a known one', 'unknown',
         {'outstanding': ['AMOC'], 'halfway': ['ARCC']}, has('halfway'))
    case(5, 'an unclassified key holding a DICT', 'unknown',
         {'sort_of_open': {'AMOC': 'why'}}, has('sort_of_open'))
    case(6, 'an unclassified key with an empty value — still unclassified', 'unknown',
         {'mystery': []}, has('mystery'))

    # ---- CLEAN
    case(7, 'the ordinary shape: an outstanding list', 'debt:2',
         {'outstanding': ['AMOC', 'ARCC'], 'note': 'prose'}, has('outstanding'))
    case(8, 'A GROWING TOTAL — a new standard listing four studies', 'debt:4',
         {'outstanding': ['AMOC', 'ARCC', 'PHDC', 'TMGH']},
         lambda p: len(p['outstanding']) == 4)
    case(9, 'a ratchet keyed BY TICKER at the top level', 'debt:2',
         {'AMOC': {'why': 'x'}, 'ARCC': {'why': 'y'}, 'note': 'prose'}, has('AMOC'))
    case(10, 'a bare top-level list, which one file in the book ships', 'debt:2',
          ['AMOC', 'XPT'], lambda p: isinstance(p, list) and len(p) == 2)
    case(11, 'a TICKER STARTING WITH A DIGIT — 2POINTZERO, which the first draft '
             'silently dropped', 'debt:1',
          {'outstanding': ['2POINTZERO']},
          lambda p: p['outstanding'] == ['2POINTZERO'])

    # the real tree must be untouched by any of it
    real = os.path.join(ROOT, 'engine', 'build_depth_audit')
    before = sorted(os.listdir(real))
    after = sorted(os.listdir(real))
    if before != after:
        bad.append('THE CONTROL MODIFIED THE REAL RATCHET DIRECTORY')

    print('study debt negative control — %s %d/%d'
          % ('PASS' if not bad else 'FAILED', ok, CASES))
    for b in bad:
        print('  - ' + b)
    if ok + len(bad) != CASES:
        print('  - CASE COUNT: %d ran against a declared %d' % (ok + len(bad), CASES))
        return 1
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
