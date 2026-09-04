#!/usr/bin/env python3
"""Negative control for check_harness_outputs.py.

Every case reinjects a condition into a sandbox copy of the repository and asserts the
gate goes RED, or is a legitimate construction and asserts it stays GREEN. EVERY MUTATION
IS ASSERTED TO HAVE LANDED before the gate runs -- a fixture that silently fails to inject
its condition produces a green run that proves only that nothing was changed, which is the
defect [R-ENF-04] names and which this control's own first draft committed.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def sandbox():
    d = tempfile.mkdtemp(prefix='harness_nc_')
    for sub in ('scripts', 'engine'):
        shutil.copytree(os.path.join(ROOT, sub), os.path.join(d, sub),
                        ignore=shutil.ignore_patterns('*.xlsx', '*.docx', '*.pdf', '*.png',
                                                      'raw_ohlc', 'raw_indices', '__pycache__'))
    return d


def run(d):
    r = subprocess.run([sys.executable, os.path.join(d, 'scripts', 'check_harness_outputs.py')],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def numbers(d, tk):
    return os.path.join(d, 'engine', '%s_study' % tk.lower(), 'study_numbers.json')


def compute(d, tk):
    return os.path.join(d, 'engine', '%s_study' % tk.lower(), 'compute.py')


CASES = []


def case(name, mutate, want_red, landed):
    CASES.append((name, mutate, want_red, landed))


# --- 1: the defect exactly as it occurred -----------------------------------------
def c1(d):
    p = numbers(d, 'du')
    D = json.load(open(p))
    D['override'] = {'inputs': {'beta': {'was': 0.4879595874282318, 'now': 1.079}},
                     'flags': {}, 'note': 'pricing harness'}
    D['dcf']['ps'] = 11.36
    json.dump(D, open(p, 'w'), indent=1)
case('DU committed file is a harness run, exactly as it occurred',
     c1, True, lambda d: 'override' in json.load(open(numbers(d, 'du'))))


# --- 2: a harness that CAN overwrite the committed file ---------------------------
def c2(d):
    p = compute(d, 'du')
    s = open(p).read()
    s = s.replace("_out_name = 'study_numbers.override.json' if OVERRIDE_RECORD is not None "
                  "else 'study_numbers.json'\n_out_path = os.environ.get('DU_OUT', "
                  "os.path.join(HERE, _out_name))",
                  "_out_path = os.path.join(HERE, 'study_numbers.json')")
    open(p, 'w').write(s)
case('a harness whose output name does not depend on the override',
     c2, True, lambda d: "_out_name = 'study_numbers.override.json'" not in open(compute(d, 'du')).read()
                         and "_out_path = os.path.join(HERE, 'study_numbers.json')" in open(compute(d, 'du')).read())


# --- 3: an unparseable committed numbers file -------------------------------------
def c3(d):
    open(numbers(d, 'du'), 'w').write('{not json')
case('a committed numbers file that will not parse',
     c3, True, lambda d: open(numbers(d, 'du')).read().startswith('{not json'))


# --- 4: an emptied population must FAIL, never report clean -----------------------
def c4(d):
    for n in os.listdir(os.path.join(d, 'engine')):
        if n.endswith('_study'):
            shutil.rmtree(os.path.join(d, 'engine', n))
case('no study directories at all',
     c4, True, lambda d: not [n for n in os.listdir(os.path.join(d, 'engine'))
                              if n.endswith('_study')])


# --- 5: studies present, every numbers file gone ----------------------------------
def c5(d):
    for n in os.listdir(os.path.join(d, 'engine')):
        p = os.path.join(d, 'engine', n, 'study_numbers.json')
        if os.path.exists(p):
            os.remove(p)
case('study directories present, not one committed numbers file',
     c5, True, lambda d: not any(os.path.exists(os.path.join(d, 'engine', n, 'study_numbers.json'))
                                 for n in os.listdir(os.path.join(d, 'engine'))))


# --- 6: every harness removed — the detector has stopped matching -----------------
def c6(d):
    for tk in ('du', 'phar'):
        p = compute(d, tk)
        if os.path.exists(p):
            s = open(p).read().replace('_OVERRIDE', '_PRICING_SWITCH')
            open(p, 'w').write(s)
case('not one pricing harness is detected — the matcher, not the risk, has gone',
     c6, True, lambda d: '_OVERRIDE' not in open(compute(d, 'du')).read())


# --- CLEAN CASES: these must NOT fire ---------------------------------------------
def c7(d):
    # an override file sitting BESIDE the committed one is the correct outcome
    p = numbers(d, 'du')
    D = json.load(open(p))
    D['override'] = {'inputs': {'beta': {'was': 0.488, 'now': 0.9}}, 'flags': {}}
    json.dump(D, open(p.replace('study_numbers.json', 'study_numbers.override.json'), 'w'),
              indent=1)
case('a harness run written BESIDE the committed file (the correct outcome)',
     c7, False, lambda d: os.path.exists(numbers(d, 'du').replace(
         'study_numbers.json', 'study_numbers.override.json')))


def c8(d):
    # a study with no harness at all is not implicated
    p = numbers(d, 'arcc')
    if os.path.exists(p):
        D = json.load(open(p))
        D['_touched'] = True
        json.dump(D, open(p, 'w'), indent=1)
case('a study with no harness, its numbers file rewritten',
     c8, False, lambda d: json.load(open(numbers(d, 'arcc'))).get('_touched') is True)


def main():
    base = sandbox()
    rc, out = run(base)
    print('baseline: %s' % ('GREEN' if rc == 0 else 'RED'))
    if rc != 0:
        print(out)
        shutil.rmtree(base)
        print('FAIL - the unmutated repository does not pass; nothing below means anything.')
        return 1
    shutil.rmtree(base)

    fails = []
    for name, mutate, want_red, landed in CASES:
        d = sandbox()
        mutate(d)
        if not landed(d):
            fails.append('%s: THE MUTATION DID NOT LAND' % name)
            shutil.rmtree(d)
            continue
        rc, out = run(d)
        got_red = rc != 0
        ok = got_red == want_red
        print('  [%s] %-64s expected %s, got %s'
              % ('OK ' if ok else 'BAD', name[:64],
                 'RED' if want_red else 'GREEN', 'RED' if got_red else 'GREEN'))
        if not ok:
            fails.append(name)
            print('        ' + out.strip().replace('\n', '\n        ')[:900])
        shutil.rmtree(d)

    if fails:
        print('\nFAIL - %d case(s): %s' % (len(fails), '; '.join(fails)))
        return 1
    print('\nOK - %d conditions, every mutation asserted to have landed.' % len(CASES))
    return 0


if __name__ == '__main__':
    sys.exit(main())
