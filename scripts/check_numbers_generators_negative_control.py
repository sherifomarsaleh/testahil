#!/usr/bin/env python3
"""Negative control for scripts/check_numbers_generators.py.

That gate is GREEN on adoption with an empty ratchet, because the three studies it
governs were declared the same morning the defect was found. A gate nobody has seen
go red is not evidence, and one that is green from birth needs its falsifier more
than most.

CASE 7 IS THIS AUTHOR'S OWN MISTAKE MADE INTO A TEST. A restore-guard beside one
generator must NOT count as two generators. EMPOWER and FERTIGLOBE were called
false positives of the detector twice before it was understood that their writes
are real writes of the original bytes — the guard, not a second generator. If that
classification ever regresses, this case goes red rather than the book quietly
acquiring two phantom violations.

Every mutation asserts it landed before the gate runs: four negative controls in
this repository have been caught passing a fixture that never injected its
condition, and a control that proves the code is unchanged proves nothing.
"""

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join('scripts', 'check_numbers_generators.py')
DECLARED_CASES = 7

ONE_GEN = '''"""A study with a single generator."""
import os, json
P = os.path.join(os.path.dirname(__file__), 'study_numbers.json')
json.dump({'central': 1.0}, open(P, 'w'))
'''

SECOND_GEN = '''"""Appends a record afterwards."""
import os, json
P = os.path.join(os.path.dirname(__file__), 'study_numbers.json')
d = json.load(open(P)); d['forecast_anchor'] = {}; json.dump(d, open(P, 'w'))
'''

GUARD = '''"""A diagnostic that must not move the file it measures."""
import os
P = os.path.join(os.path.dirname(__file__), 'study_numbers.json')
_BEFORE = open(P, 'rb').read()
import compute
if open(P, 'rb').read() != _BEFORE:
    open(P, 'wb').write(_BEFORE)
'''

DECLARED = '''"""RUN ORDER: compute.py THEN second.py. Running this file alone deletes what
the other appended."""
import os, json
P = os.path.join(os.path.dirname(__file__), 'study_numbers.json')
json.dump({'central': 1.0}, open(P, 'w'))
'''


def sandbox(studies):
    """studies: {ticker: {filename: source}}"""
    tmp = tempfile.mkdtemp(prefix='ngnc')
    os.makedirs(os.path.join(tmp, 'engine', 'build_depth_audit'), exist_ok=True)
    os.makedirs(os.path.join(tmp, 'scripts'), exist_ok=True)
    for f in ('numbers_generators.py',):
        shutil.copy(os.path.join(ROOT, 'engine', f), os.path.join(tmp, 'engine', f))
    shutil.copy(os.path.join(ROOT, GATE), os.path.join(tmp, GATE))
    for tk, files in studies.items():
        d = os.path.join(tmp, 'engine', '%s_study' % tk.lower())
        os.makedirs(d, exist_ok=True)
        for name, src in files.items():
            open(os.path.join(d, name), 'w').write(src)
    json.dump({'outstanding': []},
              open(os.path.join(tmp, 'engine', 'build_depth_audit',
                                'generators_outstanding.json'), 'w'))
    return tmp


def run(tmp):
    p = subprocess.run([sys.executable, os.path.join(tmp, GATE)],
                       capture_output=True, text=True, cwd=tmp)
    return p.returncode, p.stdout + p.stderr


def main():
    results = []

    def case(n, name, expect_red, studies, landed):
        tmp = sandbox(studies)
        try:
            assert landed(tmp), ('case %d (%s): THE MUTATION DID NOT LAND — a control '
                                 'that never injected its condition proves only that the '
                                 'code is unchanged.' % (n, name))
            rc, out = run(tmp)
            red = rc != 0
            results.append((n, name, red, expect_red, red == expect_red, out))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def has(tmp, tk, f):
        return os.path.exists(os.path.join(tmp, 'engine', '%s_study' % tk.lower(), f))

    case(1, 'two generators and no RUN ORDER anywhere', True,
         {'ZZA': {'compute.py': ONE_GEN, 'second.py': SECOND_GEN}},
         lambda t: has(t, 'ZZA', 'second.py'))

    case(2, 'a RUN ORDER that names only one of the two', True,
         {'ZZB': {'compute.py': DECLARED.replace('THEN second.py', 'and nothing else'),
                  'second.py': SECOND_GEN}},
         lambda t: 'and nothing else' in open(
             os.path.join(t, 'engine', 'zzb_study', 'compute.py')).read())

    case(3, 'zero study directories', True, {},
         lambda t: not [d for d in os.listdir(os.path.join(t, 'engine'))
                        if d.endswith('_study')])

    case(4, 'a study whose writer the detector cannot find', True,
         {'ZZC': {'compute.py': '"""writes nothing."""\nx = 1\n'}},
         lambda t: has(t, 'ZZC', 'compute.py'))

    case(5, 'CLEAN — two generators WITH a run order naming both', False,
         {'ZZD': {'compute.py': DECLARED, 'second.py': SECOND_GEN}},
         lambda t: 'RUN ORDER' in open(
             os.path.join(t, 'engine', 'zzd_study', 'compute.py')).read())

    case(6, 'CLEAN — one generator, nothing to declare', False,
         {'ZZE': {'compute.py': ONE_GEN}},
         lambda t: has(t, 'ZZE', 'compute.py'))

    # THE ONE THAT MATTERS: the classification this author got wrong twice.
    case(7, 'CLEAN — a restore-guard beside one generator is not two generators', False,
         {'ZZF': {'compute.py': ONE_GEN, 'diagnostics.py': GUARD}},
         lambda t: '_BEFORE' in open(
             os.path.join(t, 'engine', 'zzf_study', 'diagnostics.py')).read())

    assert len(results) == DECLARED_CASES, (
        'declared %d cases, ran %d — a control that quietly loses a case reports clean '
        'for the wrong reason.' % (DECLARED_CASES, len(results)))

    print('NEGATIVE CONTROL — scripts/check_numbers_generators.py')
    print('%d cases: %d must go RED, %d must stay GREEN\n'
          % (len(results), sum(1 for r in results if r[3]),
             sum(1 for r in results if not r[3])))
    bad = 0
    for n, name, red, want, ok, out in results:
        print('  %s %d. %-58s got %-5s want %s'
              % ('ok ' if ok else 'FAIL', n, name[:58],
                 'RED' if red else 'green', 'RED' if want else 'green'))
        if not ok:
            bad += 1
            for line in out.strip().splitlines()[-6:]:
                print('        %s' % line)
    print()
    if bad:
        print('%d case(s) did not behave as declared.' % bad)
        return 1
    print('All %d behaved as declared.' % len(results))
    return 0


if __name__ == '__main__':
    sys.exit(main())
