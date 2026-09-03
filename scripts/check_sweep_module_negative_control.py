#!/usr/bin/env python3
"""Negative control for scripts/check_sweep_module.py.

Reinjects each condition the gate claims to catch — including ARCC's hand-rolled register
exactly as it stood, and the subtler shape of a study that imports the module for its enums
and never runs its invariants — and asserts the gate goes RED. Then clean cases that must
stay GREEN.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join('scripts', 'check_sweep_module.py')

GOOD_SCRIPT = (
    "import sys, os\n"
    "sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))\n"
    "from research_sweep import SweepRegister, AssetClass\n"
    "R = SweepRegister('X', AssetClass.STOCK, '2026-09-03')\n"
    "ERRORS, WARNINGS = R.validate()\n")

HANDROLLED = (
    "# ARCC's shape: its own F() helper, its own assertions, no shared module\n"
    "FINDINGS = []\n"
    "for f in FINDINGS:\n"
    "    assert f['source_name'] and f['source_date']\n")

IMPORT_ONLY = (
    "import sys, os\n"
    "sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))\n"
    "from research_sweep import Ring, FindingClass, SourceType   # enums only\n"
    "FINDINGS = [dict(ring='GLOBAL')]\n")


def build(tmp, studies, ratchet=None):
    eng = os.path.join(tmp, 'engine')
    os.makedirs(os.path.join(eng, 'build_depth_audit'), exist_ok=True)
    os.makedirs(os.path.join(tmp, 'scripts'), exist_ok=True)
    shutil.copy(os.path.join(ROOT, GATE), os.path.join(tmp, GATE))
    for tk, (script, reg) in studies.items():
        sd = os.path.join(eng, '%s_study' % tk.lower())
        os.makedirs(sd, exist_ok=True)
        if script is not None:
            open(os.path.join(sd, 'sweep.py'), 'w').write(script)
        if reg == '__BROKEN__':
            open(os.path.join(sd, 'sweep_register.json'), 'w').write('{not json,')
        elif reg is not None:
            json.dump(reg, open(os.path.join(sd, 'sweep_register.json'), 'w'))
    json.dump({'entries': ratchet or {}},
              open(os.path.join(eng, 'build_depth_audit',
                                'sweep_outstanding.json'), 'w'))
    return tmp


def run(tmp):
    r = subprocess.run([sys.executable, GATE], cwd=tmp, capture_output=True, text=True)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


CASES = []


def case(name, must_fail, studies, ratchet=None, expect=None):
    CASES.append((name, must_fail, studies, ratchet, expect))


REG_OK = {'ticker': 'X', 'findings': [], 'drivers': []}
REG_ERRS_NAMED = dict(REG_OK, invariant_errors=["COVERAGE: INDUSTRY / 'technology "
                                                "substitution' unclosed"],
                      uncovered={'technology substitution': 'named, with a reason'})
REG_ERRS_UNNAMED = dict(REG_OK, invariant_errors=["COVERAGE: COMPANY / 'IR "
                                                  "communications' unclosed"],
                        uncovered={})

case("1. ARCC's shape — a hand-rolled register with its own assertions",
     True, {'ARCC': (HANDROLLED, REG_OK)}, expect='does not import research_sweep')
case('2. imports the module for its ENUMS and never calls validate()',
     True, {'X': (IMPORT_ONLY, REG_OK)}, expect='never calls validate')
case('3. no sweep script at all', True, {'X': (None, None)},
     expect='no sweep script')
case('4. runs the module but commits no register', True, {'X': (GOOD_SCRIPT, None)},
     expect='commits no sweep_register.json')
# case 5 originally passed reg=None, which is case 4's condition — it never injected a
# malformed register and its green proved only that the no-register case fails twice. The
# fixture takes a raw-bytes marker instead.
case('5. a register that will not parse', True, {'X': (GOOD_SCRIPT, '__BROKEN__')},
     expect='will not parse')
case('6. invariant failures the study does not NAME', True,
     {'X': (GOOD_SCRIPT, REG_ERRS_UNNAMED)}, expect='does not name')
case('7. a listed study no longer on disk [R-ENF-04]', True,
     {'X': (GOOD_SCRIPT, REG_OK)}, ratchet={'GONE': 'had no sweep'},
     expect='no longer resolve on disk')
case('8. no study directories at all [R-ENF-04]', True, {},
     expect='examined zero study directories')

case('9. CLEAN — imports the module and calls validate()', False,
     {'X': (GOOD_SCRIPT, REG_OK)})
case('10. CLEAN — invariant failures the study NAMES, which is a gap written down '
     'rather than a gap hidden', False, {'X': (GOOD_SCRIPT, REG_ERRS_NAMED)})
case('11. CLEAN — a study with no sweep that is on the ratchet', False,
     {'X': (None, None)}, ratchet={'X': 'no sweep script'})


def main():
    bad = 0
    for name, must_fail, studies, ratchet, expect in CASES:
        tmp = tempfile.mkdtemp(prefix='ncsweep')
        try:
            build(tmp, studies, ratchet)
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
