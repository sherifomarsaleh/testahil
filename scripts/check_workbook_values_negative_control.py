#!/usr/bin/env python3
"""A check nobody has seen fail is not evidence.

Every condition below is injected into a SANDBOX COPY of the repository and the gate must
go red on it — and, on the clean cases, must stay green. Every mutation is asserted to have
LANDED before the gate runs: a negative control whose edit silently missed proves only that
the file was untouched, which is the defect this repository has already paid for once
(a control searching for a QUOTED object key where the file writes them unquoted).

The two cases that matter most are 2 and 9. Case 2 is a study whose script EXISTS and is
RED: treating the file's existence as conformance would put a green tick on a red result,
and here that is not hypothetical — it is SWDY as delivered. Case 9 is the ratchet's two
groups being non-interchangeable, which is [R-TERM-01]'s own negative-control lesson: an
allowance for an ABSENT check must not excuse a RED one, or a study escapes a real
disagreement by being re-filed as merely unchecked.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join('scripts', 'check_workbook_values.py')
RAT = os.path.join('engine', 'build_depth_audit', 'workbook_values_outstanding.json')

# A tiny study that passes: a recalculation script exiting 0.
PASSING = 'import sys\nprint("RECALC OK - 3 of 3 cells reproduce the model")\nsys.exit(0)\n'
FAILING = ('import sys\nprint("AssertionError: 4 formula cells disagree with the model")\n'
           'sys.exit(1)\n')
CRASHING = 'raise SystemExit("could not open the delivered workbook")\n'


def sandbox():
    d = tempfile.mkdtemp(prefix='wbvals_nc_')
    for p in ('scripts', 'engine/build_depth_audit'):
        os.makedirs(os.path.join(d, p), exist_ok=True)
    shutil.copy(os.path.join(ROOT, GATE), os.path.join(d, GATE))
    shutil.copy(os.path.join(ROOT, RAT), os.path.join(d, RAT))
    # a minimal book: three studies, each with a passing recalculation
    for tk in ('alpha', 'beta', 'gamma'):
        sd = os.path.join(d, 'engine', '%s_study' % tk)
        os.makedirs(sd, exist_ok=True)
        open(os.path.join(sd, 'recalc.py'), 'w').write(PASSING)
    # the ratchet starts EMPTY against this book — every real entry is off-book here
    json.dump({'no_check': {}, 'failing': {}, 'note': 'sandbox'},
              open(os.path.join(d, RAT), 'w'), indent=1)
    return d


def run(d):
    r = subprocess.run([sys.executable, GATE], cwd=d, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
    return r.returncode, r.stdout.decode('utf-8', 'replace')


def put_ratchet(d, obj):
    json.dump(obj, open(os.path.join(d, RAT), 'w'), indent=1)


CASES = []


def case(name, expect_red, build, why):
    CASES.append((name, expect_red, build, why))


# ---------------------------------------------------------------- the failures
def _c1(d):
    sd = os.path.join(d, 'engine', 'delta_study')
    os.makedirs(sd, exist_ok=True)
    open(os.path.join(sd, 'recalc.py'), 'w').write(FAILING)
    assert os.path.exists(os.path.join(sd, 'recalc.py'))


case('1 a NEW study whose recalculation is red', True, _c1,
     'the ordinary case this gate exists for')


def _c2(d):
    p = os.path.join(d, 'engine', 'beta_study', 'recalc.py')
    open(p, 'w').write(FAILING)
    assert 'disagree' in open(p).read(), 'the failing script did not land'


case('2 an EXISTING study whose script exists and is RED', True, _c2,
     'THE CASE THAT MATTERS MOST — counting the file rather than running it puts a green '
     'tick on a red result, which is SWDY exactly as delivered')


def _c3(d):
    sd = os.path.join(d, 'engine', 'epsilon_study')
    os.makedirs(sd, exist_ok=True)
    assert not os.path.exists(os.path.join(sd, 'recalc.py'))


case('3 a NEW study with no recalculation script at all', True, _c3,
     'an absent instrument is not a clean one')


def _c4(d):
    p = os.path.join(d, 'engine', 'gamma_study', 'recalc.py')
    open(p, 'w').write(CRASHING)
    assert 'could not open' in open(p).read()


case('4 a script that CRASHES rather than returning a verdict', True, _c4,
     'a crash is an ABSENT answer, and an absent answer wearing the costume of a clean one '
     'is strictly worse than a failure [R-ENF-04]')


def _c5(d):
    put_ratchet(d, {'no_check': {'NOSUCHNAME': 'listed and not on disk'}, 'failing': {}})
    assert 'NOSUCHNAME' in open(os.path.join(d, RAT)).read()


case('5 a ratchet entry naming a study that is not on disk', True, _c5,
     'the population is anchored elsewhere and every listed name must resolve [R-ENF-04]')


def _c6(d):
    for tk in ('alpha', 'beta', 'gamma'):
        shutil.rmtree(os.path.join(d, 'engine', '%s_study' % tk))
    assert not os.path.exists(os.path.join(d, 'engine', 'alpha_study'))


case('6 an EMPTIED population — no study directories at all', True, _c6,
     'a run examining zero directories means the resolver broke, not that the book is clean')


def _c7(d):
    for tk in ('alpha', 'beta', 'gamma'):
        os.remove(os.path.join(d, 'engine', '%s_study' % tk, 'recalc.py'))
    put_ratchet(d, {'no_check': {'ALPHA': 'x', 'BETA': 'x', 'GAMMA': 'x'}, 'failing': {}})
    assert not os.path.exists(os.path.join(d, 'engine', 'alpha_study', 'recalc.py'))


case('7 every study ratcheted, so ZERO recalculations RUN', True, _c7,
     'THE SECOND HALF OF THE ANCHORING: a book where every check is excused still examined '
     'directories, and would otherwise report clean having run nothing')


def _c8(d):
    p = os.path.join(d, 'engine', 'alpha_study', 'recalc.py')
    open(p, 'w').write('import time\ntime.sleep(9999)\n')
    g = os.path.join(d, GATE)
    s = open(g).read().replace('TIMEOUT = 600', 'TIMEOUT = 2')
    open(g, 'w').write(s)
    assert 'TIMEOUT = 2' in open(g).read(), 'the shortened timeout did not land'


case('8 a script that HANGS past the timeout', True, _c8,
     'a timeout is an absent answer like any other')


def _c9(d):
    p = os.path.join(d, 'engine', 'beta_study', 'recalc.py')
    open(p, 'w').write(FAILING)
    put_ratchet(d, {'no_check': {'BETA': 'excused as having no check'}, 'failing': {}})
    assert 'BETA' in json.load(open(os.path.join(d, RAT)))['no_check']


case('9 a RED script excused by the NO-CHECK list', True, _c9,
     'THE TWO GROUPS ARE NOT INTERCHANGEABLE [R-TERM-01]: an allowance for an absent check '
     'must not excuse a real disagreement, or a study escapes one by being re-filed')


def _c10(d):
    os.remove(os.path.join(d, 'engine', 'gamma_study', 'recalc.py'))
    put_ratchet(d, {'no_check': {}, 'failing': {'GAMMA': 'excused as red'}})
    assert 'GAMMA' in json.load(open(os.path.join(d, RAT)))['failing']


case('10 an ABSENT script excused by the FAILING list', True, _c10,
     'the same clause in the other direction — the instrument going missing is a change')


# ---------------------------------------------------------------- the clean cases
def _c11(d):
    assert os.path.exists(os.path.join(d, 'engine', 'alpha_study', 'recalc.py'))


case('11 the untouched book', False, _c11,
     'a gate red where no rule is broken is the permanently-red check [R-ENF-02] forbids')


def _c12(d):
    p = os.path.join(d, 'engine', 'beta_study', 'recalc.py')
    open(p, 'w').write(FAILING)
    put_ratchet(d, {'no_check': {}, 'failing': {'BETA': 'a known red check, recorded'}})
    assert json.load(open(os.path.join(d, RAT)))['failing']['BETA']


case('12 a RED script correctly on the FAILING list', False, _c12,
     'the ratchet must actually excuse what it names, or it is a permanently red build')


def _c13(d):
    os.remove(os.path.join(d, 'engine', 'gamma_study', 'recalc.py'))
    put_ratchet(d, {'no_check': {'GAMMA': 'no instrument yet, recorded'}, 'failing': {}})
    assert not os.path.exists(os.path.join(d, 'engine', 'gamma_study', 'recalc.py'))


case('13 an ABSENT script correctly on the NO-CHECK list', False, _c13,
     'the other allowance, doing its job')


def _c14(d):
    p = os.path.join(d, 'engine', 'alpha_study', 'lo_recalc_gate.py')
    os.remove(os.path.join(d, 'engine', 'alpha_study', 'recalc.py'))
    open(p, 'w').write(PASSING)
    assert os.path.exists(p)


case('14 a study whose instrument is named lo_recalc_gate.py', False, _c14,
     'the second name a recalculation goes by in this book — a study is not red for '
     'naming its own file differently')


def main():
    bad = []
    for name, expect_red, build, why in CASES:
        d = sandbox()
        try:
            build(d)
            rc, out = run(d)
            got_red = rc != 0
            ok = got_red == expect_red
            print('%-4s %-58s expected %-5s got %-5s' %
                  ('OK' if ok else 'MISS', name, 'RED' if expect_red else 'green',
                   'RED' if got_red else 'green'))
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
