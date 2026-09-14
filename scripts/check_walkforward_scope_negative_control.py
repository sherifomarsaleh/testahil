#!/usr/bin/env python3
"""A check nobody has seen fail is not evidence.

Every condition is injected into a SANDBOX COPY and the gate must go RED — and on the clean
cases must stay GREEN. Every mutation is ASSERTED to have landed before the gate runs,
because a control whose edit silently missed proves only that the file was untouched.

The cases that matter most are 4, 5 and 11. Case 4 is a decision that CONTRADICTS THE DISK,
which is the declared-versus-done failure [R-MACRO-01] names and the only one here that is
false rather than merely absent. Case 5 is that same falsehood sitting on the ratchet: the
allowance spares a study that has not WRITTEN a decision, never one that has written a
wrong one, and a ratchet that excused it would make the gate unable to see the thing it
exists for. Case 11 is a study on the ratchet that legitimately has no decision and must
stay GREEN, because a gate red where no rule is broken is the permanently-red check
[R-ENF-02] forbids.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join('scripts', 'check_walkforward_scope.py')
RAT = os.path.join('engine', 'build_depth_audit', 'walkforward_scope_outstanding.json')

GOOD = {'rule': 'R-FCAL-01', 'scope': 'FULL', 'sourceable_fiscal_years': 16,
        'earliest_sourceable': 'FY2010', 'basis': "the company's own archive",
        'status': 'pending', 'note': 'the run has not happened; nothing rests on it'}


def sandbox():
    d = tempfile.mkdtemp(prefix='wfscope_nc_')
    os.makedirs(os.path.join(d, 'scripts'), exist_ok=True)
    os.makedirs(os.path.join(d, 'engine', 'build_depth_audit'), exist_ok=True)
    shutil.copy(os.path.join(ROOT, GATE), os.path.join(d, GATE))
    for tk, rec in (('alpha', dict(GOOD)), ('beta', dict(GOOD)), ('gamma', dict(GOOD))):
        sd = os.path.join(d, 'engine', '%s_study' % tk)
        os.makedirs(sd, exist_ok=True)
        json.dump({'central': 10.0, 'walkforward_scope': rec},
                  open(os.path.join(sd, 'study_numbers.json'), 'w'), indent=1)
    json.dump({'entries': {}, 'note': 'sandbox'}, open(os.path.join(d, RAT), 'w'), indent=1)
    return d


def put(d, tk, rec):
    p = os.path.join(d, 'engine', '%s_study' % tk, 'study_numbers.json')
    nums = json.load(open(p))
    if rec is None:
        nums.pop('walkforward_scope', None)
    else:
        nums['walkforward_scope'] = rec
    json.dump(nums, open(p, 'w'), indent=1)
    return p


def ratchet(d, obj):
    json.dump(obj, open(os.path.join(d, RAT), 'w'), indent=1)


def run(d):
    r = subprocess.run([sys.executable, GATE], cwd=d, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
    return r.returncode, r.stdout.decode('utf-8', 'replace')


CASES = []


def case(name, red, build, why):
    CASES.append((name, red, build, why))


def _1(d):
    p = put(d, 'beta', None)
    assert 'walkforward_scope' not in json.load(open(p))


case('1 a study with no scope decision and no ratchet entry', True, _1,
     'the ordinary case: the rule has stood since 31-Aug-2026 and bound nothing')


def _2(d):
    r = dict(GOOD, scope='FULL', sourceable_fiscal_years=3)
    p = put(d, 'beta', r)
    assert json.load(open(p))['walkforward_scope']['sourceable_fiscal_years'] == 3


case('2 FULL declared on three sourceable years', True, _2,
     'a study claiming a test its history cannot support')


def _3(d):
    r = dict(GOOD, scope='SKIP', sourceable_fiscal_years=2,
             note='we did not get round to it')
    p = put(d, 'beta', r)
    assert 'round to it' in json.load(open(p))['walkforward_scope']['note']


case('3 a SKIP not recorded in the rule\'s own words', True, _3,
     'the rule specifies the words because a skip phrased freely is a skip nobody can find')


def _4(d):
    os.makedirs(os.path.join(d, 'engine', 'beta_walkforward'), exist_ok=True)
    p = put(d, 'beta', dict(GOOD, status='pending'))
    assert os.path.isdir(os.path.join(d, 'engine', 'beta_walkforward'))
    assert json.load(open(p))['walkforward_scope']['status'] == 'pending'


case('4 a run EXISTS on disk and the record says pending', True, _4,
     'THE DECLARED-VERSUS-DONE CASE [R-MACRO-01]: the only falsehood here rather than an '
     'absence, and it runs in the direction that tells a reader the method is untested '
     'when it has been tested')


def _5(d):
    os.makedirs(os.path.join(d, 'engine', 'beta_walkforward'), exist_ok=True)
    put(d, 'beta', dict(GOOD, status='not_run'))
    ratchet(d, {'entries': {'BETA': 'excused'}, 'note': 'sandbox'})
    assert 'BETA' in json.load(open(os.path.join(d, RAT)))['entries']


case('5 that same falsehood sitting on the ratchet', True, _5,
     'THE ALLOWANCE SPARES A STUDY THAT HAS NOT WRITTEN A DECISION, NEVER ONE THAT HAS '
     'WRITTEN A FALSE ONE — a ratchet that excused this would blind the gate to the thing '
     'it exists for')


def _6(d):
    r = dict(GOOD)
    del r['basis']
    p = put(d, 'beta', r)
    assert 'basis' not in json.load(open(p))['walkforward_scope']


case('6 a decision missing the basis for its own count', True, _6,
     'a count nobody can check is not a count')


def _7(d):
    p = put(d, 'beta', dict(GOOD, scope='THOROUGH'))
    assert json.load(open(p))['walkforward_scope']['scope'] == 'THOROUGH'


case('7 a scope outside the three the rule allows', True, _7,
     'an open vocabulary lets a study opt out by inventing a scope')


def _8(d):
    ratchet(d, {'entries': {'NOSUCHNAME': 'listed and not on disk'}, 'note': 'sandbox'})
    assert 'NOSUCHNAME' in open(os.path.join(d, RAT)).read()


case('8 a ratchet entry naming a study not on disk', True, _8,
     'the population is anchored elsewhere and every listed name must resolve [R-ENF-04]')


def _9(d):
    for tk in ('alpha', 'beta', 'gamma'):
        shutil.rmtree(os.path.join(d, 'engine', '%s_study' % tk))
    assert not os.path.exists(os.path.join(d, 'engine', 'alpha_study'))


case('9 an EMPTIED population', True, _9,
     'zero directories means the resolver broke, not that the book is clean')


def _10(d):
    for tk in ('alpha', 'beta', 'gamma'):
        os.remove(os.path.join(d, 'engine', '%s_study' % tk, 'study_numbers.json'))
    ratchet(d, {'entries': {'ALPHA': 'x', 'BETA': 'x', 'GAMMA': 'x'}, 'note': 'sandbox'})
    assert not os.path.exists(os.path.join(d, 'engine', 'alpha_study', 'study_numbers.json'))


case('10 every study present and ZERO numbers files READ', True, _10,
     'THE SECOND HALF OF THE ANCHORING: a run that examined directories and read nothing '
     'would otherwise report clean')


def _11(d):
    put(d, 'beta', None)
    ratchet(d, {'entries': {'BETA': 'predates the gate'}, 'note': 'sandbox'})
    assert 'BETA' in json.load(open(os.path.join(d, RAT)))['entries']


case('11 an absent decision correctly on the ratchet', False, _11,
     'the allowance doing its job — a gate red where no rule is broken is the '
     'permanently-red check [R-ENF-02] forbids')


def _12(d):
    p = put(d, 'beta', dict(GOOD, scope='LIGHT', sourceable_fiscal_years=6,
                            status='run'))
    os.makedirs(os.path.join(d, 'engine', 'beta_walkforward'), exist_ok=True)
    assert json.load(open(p))['walkforward_scope']['scope'] == 'LIGHT'


case('12 LIGHT on six years, run, with the run on disk', False, _12,
     'the fully conforming shape, and the bands must not fire on their own middle')


def _13(d):
    p = put(d, 'beta', dict(GOOD, scope='SKIP', sourceable_fiscal_years=3,
                            note='walk-forward not run - insufficient sourceable history '
                                 '(3 years)', status='not_run'))
    assert 'insufficient' in json.load(open(p))['walkforward_scope']['note']


case('13 a legitimate SKIP in the rule\'s own words', False, _13,
     'a short history is a real answer and must not be punished for being one')


def _14(d):
    assert os.path.exists(os.path.join(d, 'engine', 'alpha_study', 'study_numbers.json'))


case('14 the untouched sandbox', False, _14,
     'three conforming studies and an empty ratchet must be green')


def main():
    bad = []
    for name, red, build, why in CASES:
        d = sandbox()
        try:
            build(d)
            rc, out = run(d)
            got = rc != 0
            ok = got == red
            print('%-4s %-56s expected %-5s got %-5s'
                  % ('OK' if ok else 'MISS', name, 'RED' if red else 'green',
                     'RED' if got else 'green'))
            if not ok:
                bad.append((name, why, out[-900:]))
        finally:
            shutil.rmtree(d, ignore_errors=True)
    print()
    if bad:
        for name, why, out in bad:
            print('MISS: %s\n  why it matters: %s\n%s\n' % (name, why, out))
        print('FAIL — %d of %d conditions did not behave as required.' % (len(bad), len(CASES)))
        return 1
    print('OK — all %d conditions behaved as required (%d red, %d green).'
          % (len(CASES), sum(1 for c in CASES if c[1]), sum(1 for c in CASES if not c[1])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
