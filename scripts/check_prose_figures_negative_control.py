#!/usr/bin/env python3
"""Negative control for scripts/check_prose_figures.py.

Reinjects each condition the gate claims to catch — including the shape that matters most,
a study that CARRIES the instrument while its own check is RED, which a gate testing only
for the file's existence would have reported clean.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join('scripts', 'check_prose_figures.py')

PASSING = ("import sys\n"
           "print('prose figures checked: 10; unmatched: 0')\n"
           "print('reads X.docx via Document()')\n"
           "sys.exit(0)\n")
FAILING = ("import sys\n"
           "print('prose figures checked: 10; unmatched: 3')\n"
           "print('reads X.docx via Document()')\n"
           "sys.exit(1)\n")
NOT_A_CHECK = ("print('a report about figures, reading nothing')\n")
CRASHES = ("import sys\n"
           "raise SystemExit('reads X.docx via Document() then dies: no numbers file')\n")


def build(tmp, studies, ratchet=None):
    eng = os.path.join(tmp, 'engine')
    os.makedirs(os.path.join(eng, 'build_depth_audit'), exist_ok=True)
    os.makedirs(os.path.join(tmp, 'scripts'), exist_ok=True)
    shutil.copy(os.path.join(ROOT, GATE), os.path.join(tmp, GATE))
    for tk, script in studies.items():
        sd = os.path.join(eng, '%s_study' % tk.lower())
        os.makedirs(sd, exist_ok=True)
        if script is not None:
            open(os.path.join(sd, 'prose_check.py'), 'w').write(script)
    json.dump({'entries': ratchet or {}},
              open(os.path.join(eng, 'build_depth_audit',
                                'prose_outstanding.json'), 'w'))
    return tmp


def run(tmp):
    r = subprocess.run([sys.executable, GATE], cwd=tmp, capture_output=True, text=True)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


CASES = [
    ('1. no prose check at all', True, {'X': None}, None, 'no script reconciles'),
    ('2. THE ONE THAT MATTERS — carries the instrument and its own check is RED',
     True, {'X': FAILING}, None, 'unmatched: 3'),
    ('3. a file that mentions figures but reads no document', True,
     {'X': NOT_A_CHECK}, None, 'no script reconciles'),
    ('4. a check that crashes', True, {'X': CRASHES}, None, 'X'),
    ('5. a listed study no longer on disk [R-ENF-04]', True, {'X': PASSING},
     {'GONE': 'had none'}, 'no longer resolve on disk'),
    ('6. no study directories at all [R-ENF-04]', True, {}, None,
     'examined zero study directories'),
    ('7. CLEAN — carries it and passes', False, {'X': PASSING}, None, None),
    ('8. CLEAN — a study with no check that is on the ratchet', False, {'X': None},
     {'X': 'no prose check'}, None),
    ('9. CLEAN — a study whose check is RED but is on the ratchet: knowingly '
     'outstanding, allowed to fail', False, {'X': FAILING}, {'X': 'unmatched: 3'}, None),
]


def main():
    bad = 0
    for name, must_fail, studies, ratchet, expect in CASES:
        tmp = tempfile.mkdtemp(prefix='ncprose')
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
