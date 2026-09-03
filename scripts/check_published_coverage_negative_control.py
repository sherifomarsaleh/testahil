#!/usr/bin/env python3
"""Negative control for scripts/check_published_coverage.py.

Reinjects each condition the gate claims to catch — and the one that matters is a NEW name
published with no study, because that is the only way this number grows.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join('scripts', 'check_published_coverage.py')

EXPECTED_CASES = 8       # a case lost to an edit is a green that proves nothing


def data_js(names):
    """names: {ticker: has_fair}. Written as a real object literal, loaded by the gate
    through node — which is the point of [R-ENF-03] and the reason this fixture does not
    hand-write JSON."""
    parts = []
    for tk, fair in names.items():
        if fair:
            parts.append('  %s: {code: "EGX:%s", fair: {bear: 1, base: 2, full: 3}}'
                         % (tk, tk))
        else:
            parts.append('  %s: {code: "EGX:%s"}' % (tk, tk))
    return 'const TICKERS = {\n' + ',\n'.join(parts) + '\n};\n'


def build(tmp, names, studies, ratchet=None, raw=None):
    os.makedirs(os.path.join(tmp, 'assets'), exist_ok=True)
    os.makedirs(os.path.join(tmp, 'engine', 'build_depth_audit'), exist_ok=True)
    os.makedirs(os.path.join(tmp, 'scripts'), exist_ok=True)
    shutil.copy(os.path.join(ROOT, GATE), os.path.join(tmp, GATE))
    if raw is not None:
        open(os.path.join(tmp, 'assets', 'data.js'), 'w').write(raw)
    elif names is not None:
        open(os.path.join(tmp, 'assets', 'data.js'), 'w').write(data_js(names))
    for tk in studies:
        os.makedirs(os.path.join(tmp, 'engine', '%s_study' % tk.lower()), exist_ok=True)
    json.dump({'entries': ratchet or {}},
              open(os.path.join(tmp, 'engine', 'build_depth_audit',
                                'coverage_outstanding.json'), 'w'))
    return tmp


def run(tmp):
    r = subprocess.run([sys.executable, GATE], cwd=tmp, capture_output=True, text=True)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


CASES = []


def case(name, must_fail, kw, expect=None):
    CASES.append((name, must_fail, kw, expect))


case('1. THE ONE THAT MATTERS — a NEW name published with no study', True,
     dict(names={'AAA': True, 'BBB': True}, studies=['aaa'], ratchet={}),
     expect='BBB')
case('2. a listed name that stopped being published [R-ENF-04]', True,
     dict(names={'AAA': True}, studies=['aaa'], ratchet={'GONE': 'was unstudied'}),
     expect='no longer carry a published fair value')
case('3. data.js absent — an absent site file is not an empty one', True,
     dict(names=None, studies=['aaa'], ratchet={}), expect='not present')
case('4. data.js parses but will not LOAD [R-ENF-03]', True,
     dict(names=None, studies=['aaa'], ratchet={},
          raw='const TICKERS = {AAA: {fair: {base: 1}}}; throw new Error("boom");'),
     expect='would not LOAD')
case('5. the site publishes no fair value at all [R-ENF-04]', True,
     dict(names={'AAA': False, 'BBB': False}, studies=['aaa'], ratchet={}),
     expect='publishes no fair value')
case('6. no study directories at all [R-ENF-04]', True,
     dict(names={'AAA': True}, studies=[], ratchet={'AAA': 'listed'}),
     expect='no study directories')
case('7. CLEAN — every published name has a study', False,
     dict(names={'AAA': True, 'BBB': True}, studies=['aaa', 'bbb'], ratchet={}))
case('8. CLEAN — an unstudied name that is on the ratchet', False,
     dict(names={'AAA': True, 'BBB': True}, studies=['aaa'],
          ratchet={'BBB': 'published, unstudied, Phase 2'}))


def main():
    assert len(CASES) == EXPECTED_CASES, (
        'this file declares %d cases and %d are registered' % (EXPECTED_CASES, len(CASES)))
    bad = 0
    for name, must_fail, kw, expect in CASES:
        tmp = tempfile.mkdtemp(prefix='nccov')
        try:
            build(tmp, **kw)
            rc, out = run(tmp)
            red = rc != 0
            ok = (red == must_fail) and (expect is None or expect in out)
            print('%-4s %s' % ('PASS' if ok else 'FAIL', name))
            if not ok:
                bad += 1
                print('      rc=%d wanted %s%s' % (
                    rc, 'RED' if must_fail else 'GREEN',
                    (' containing %r' % expect) if expect else ''))
                print('      ' + '\n      '.join(out.strip().splitlines()[-8:]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    print('\n%d/%d cases behaved as specified' % (len(CASES) - bad, len(CASES)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
