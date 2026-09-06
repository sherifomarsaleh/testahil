#!/usr/bin/env python3
"""Negative control for check_rebuild_ledger.py.

Every case injects a condition into a sandbox copy and asserts the gate goes RED, or is
a legitimate construction and asserts it stays GREEN. EVERY MUTATION IS ASSERTED TO HAVE
LANDED before the gate runs, and the assertion is on the CONDITION rather than on a key
[L-297] — a fixture that reports landed while injecting nothing produces a green run
proving only that nothing changed.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXPECTED_CASES = 9


def sandbox():
    d = tempfile.mkdtemp(prefix='rebuild_nc_')
    for sub in ('scripts', 'engine'):
        shutil.copytree(os.path.join(ROOT, sub), os.path.join(d, sub),
                        ignore=shutil.ignore_patterns('*.xlsx', '*.docx', '*.pdf', '*.png',
                                                      'raw_ohlc', 'raw_indices',
                                                      '__pycache__'))
    return d


# THIS FIXTURE SUPPLIES ITS OWN POPULATION [06-09-2026]. The gate resolves the
# book through engine/study_population.py; this control runs it against a
# sandboxed tree holding studies it planted, which is the point of the control.
# The escape is explicit and the gate PRINTS that it took it, so a fixture
# population can never be mistaken for the real one.
_FIXTURE_ENV = dict(os.environ, TESTAHIL_FIXTURE_POPULATION='1')


def run(d):
    r = subprocess.run([sys.executable,
                        os.path.join(d, 'scripts', 'check_rebuild_ledger.py')],
                       capture_output=True, text=True, env=_FIXTURE_ENV)
    return r.returncode, r.stdout + r.stderr


def led(d, tk):
    return os.path.join(d, 'engine', '%s_study' % tk.lower(), 'rebuild_ledger.json')


def load(d, tk):
    return json.load(open(led(d, tk), encoding='utf-8'))


def save(d, tk, rec):
    json.dump(rec, open(led(d, tk), 'w', encoding='utf-8'), indent=1)


CASES = []


def case(name, mutate, want_red, landed):
    CASES.append((name, mutate, want_red, landed))


# --- 1: THE ONE THAT MATTERS — a broken chain -------------------------------------
# The running total is only a running total if each lever starts where the last ended.
def c1(d):
    r = load(d, 'PHAR')
    r['levers'][2]['before'] = r['levers'][2]['before'] * 1.4
    save(d, 'PHAR', r)
case('a lever that does not start where the one before it ended',
     c1, True,
     lambda d: abs(load(d, 'PHAR')['levers'][2]['before']
                   - load(d, 'PHAR')['levers'][1]['after']) > 1e-6)


# --- 2: a lever naming no rule — the grouping key is what the module is FOR --------
def c2(d):
    r = load(d, 'PHAR')
    r['levers'][0]['rule'] = ''
    save(d, 'PHAR', r)
case('a lever that names no rule, so it silently becomes its own evidence',
     c2, True, lambda d: not load(d, 'PHAR')['levers'][0]['rule'])


# --- 3: a sequence with no declared audit point -----------------------------------
def c3(d):
    r = load(d, 'PHAR')
    r['audit_after'] = '   '
    save(d, 'PHAR', r)
case('a five-lever rebuild that declares no audit point',
     c3, True, lambda d: not str(load(d, 'PHAR')['audit_after']).strip())


# --- 4: the published answer is not where the levers end --------------------------
def c4(d):
    r = load(d, 'PHAR')
    r['value'] = r['value'] * 1.25
    save(d, 'PHAR', r)
case('the ledger publishes an answer the last lever does not reach',
     c4, True,
     lambda d: abs(load(d, 'PHAR')['value']
                   - load(d, 'PHAR')['levers'][-1]['after']) > 1e-6)


# --- 5: a ledger that will not parse ----------------------------------------------
def c5(d):
    open(led(d, 'PHAR'), 'w').write('{not json')
case('a rebuild ledger that will not parse',
     c5, True, lambda d: open(led(d, 'PHAR')).read().startswith('{not json'))


# --- 6: a NEW study with neither a ledger nor a ratchet entry ----------------------
def c6(d):
    n = os.path.join(d, 'engine', 'newco_study')
    os.makedirs(n, exist_ok=True)
    open(os.path.join(n, 'study_numbers.json'), 'w').write('{}')
case('a new study with neither a ledger nor an entry either way',
     c6, True, lambda d: os.path.isdir(os.path.join(d, 'engine', 'newco_study')))


# --- 7: an empty population -------------------------------------------------------
def c7(d):
    for n in os.listdir(os.path.join(d, 'engine')):
        if n.endswith('_study'):
            shutil.rmtree(os.path.join(d, 'engine', n))
case('no study directories at all [R-ENF-04]',
     c7, True, lambda d: not [n for n in os.listdir(os.path.join(d, 'engine'))
                              if n.endswith('_study')])


# --- 8: every ledger removed — the gate must refuse, not report clean --------------
# A run that reads ZERO ledgers is the absent answer wearing the costume of a clean one.
def c8(d):
    n = 0
    for x in os.listdir(os.path.join(d, 'engine')):
        p = os.path.join(d, 'engine', x, 'rebuild_ledger.json')
        if os.path.exists(p):
            os.remove(p); n += 1
    assert n > 0, 'nothing to remove; this case tests nothing'
case('study directories present, not one ledger among them [R-ENF-04]',
     c8, True, lambda d: not any(os.path.exists(os.path.join(d, 'engine', x,
                                                             'rebuild_ledger.json'))
                                 for x in os.listdir(os.path.join(d, 'engine'))))


# --- 9: CLEAN — a LARGE cumulative move with a walkable ledger must PASS -----------
# THE CASE THAT KEEPS THIS GATE HONEST. It records a route; it does not judge a
# destination. A study wrong in six ways moves a long way when all six are fixed, and a
# threshold here would be the free parameter the promotion rule forbids. PHAR's own
# -36.9% is already the largest in the book and passes; this doubles it and it must
# still pass, because what is checked is whether the move can be WALKED.
def c9(d):
    r = load(d, 'PHAR')
    lv = r['levers'][-1]
    lv['after'] = lv['before'] * 0.25
    lv['move'] = lv['after'] / lv['before'] - 1.0
    r['value'] = lv['after']
    r['cumulative_move'] = r['value'] / r['start_value'] - 1.0
    for g in r['rules'].values():
        pass
    r['rules']['R-MACRO-01']['last_after'] = lv['after']
    r['rules']['R-MACRO-01']['move'] = (lv['after']
                                        / r['rules']['R-MACRO-01']['first_before'] - 1.0)
    save(d, 'PHAR', r)
case('CLEAN — a far larger cumulative move whose ledger still walks',
     c9, False, lambda d: load(d, 'PHAR')['cumulative_move'] < -0.6)


def main():
    base = sandbox()
    rc, out = run(base)
    print('baseline: %s' % ('GREEN' if rc == 0 else 'RED'))
    if rc != 0:
        print(out)
        shutil.rmtree(base)
        print('FAIL — the unmutated repository does not pass; nothing below means '
              'anything.')
        return 1
    shutil.rmtree(base)

    assert len(CASES) == EXPECTED_CASES, (
        'this control claims %d cases and carries %d. A case quietly dropped is a '
        'condition quietly untested.' % (EXPECTED_CASES, len(CASES)))

    fails = []
    for name, mutate, want_red, landed in CASES:
        d = sandbox()
        mutate(d)
        if not landed(d):
            fails.append('%s: THE MUTATION DID NOT LAND' % name)
            print('  [BAD] %-62s mutation did not land' % name[:62])
            shutil.rmtree(d)
            continue
        rc, out = run(d)
        got_red = rc != 0
        ok = got_red == want_red
        print('  [%s] %-62s expected %s, got %s'
              % ('OK ' if ok else 'BAD', name[:62],
                 'RED' if want_red else 'GREEN', 'RED' if got_red else 'GREEN'))
        if not ok:
            fails.append(name)
            print('        ' + out.strip().replace('\n', '\n        ')[-900:])
        shutil.rmtree(d)

    if fails:
        print('\nFAIL — %d case(s): %s' % (len(fails), '; '.join(fails)))
        return 1
    print('\nOK — %d conditions, every mutation asserted to have landed.' % len(CASES))
    return 0


if __name__ == '__main__':
    sys.exit(main())
