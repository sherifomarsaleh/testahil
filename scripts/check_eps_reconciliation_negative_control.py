#!/usr/bin/env python3
"""Negative control for check_eps_reconciliation.py.

Every case injects a condition into a sandbox copy and asserts the gate goes RED, or is a
legitimate construction and asserts it stays GREEN. EVERY MUTATION IS ASSERTED TO HAVE
LANDED before the gate runs — a fixture that silently fails to inject its condition
produces a green run proving only that nothing changed [R-ENF-04].
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
    d = tempfile.mkdtemp(prefix='eps_nc_')
    for sub in ('scripts', 'engine'):
        shutil.copytree(os.path.join(ROOT, sub), os.path.join(d, sub),
                        ignore=shutil.ignore_patterns('*.xlsx', '*.docx', '*.pdf', '*.png',
                                                      'raw_ohlc', 'raw_indices', '__pycache__'))
    return d


def run(d):
    r = subprocess.run([sys.executable, os.path.join(d, 'scripts',
                                                     'check_eps_reconciliation.py')],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def nf(d, tk):
    return os.path.join(d, 'engine', '%s_study' % tk.lower(), 'study_numbers.json')


def put(d, tk, **kv):
    p = nf(d, tk)
    D = json.load(open(p))
    for k, v in kv.items():
        if v is None:
            D.pop(k, None)
        elif k == 'inputs':
            D['inputs'].update(v)
        else:
            D[k] = v
    json.dump(D, open(p, 'w'), indent=1, default=float)


CASES = []


def case(name, mutate, want_red, landed):
    CASES.append((name, mutate, want_red, landed))


I = lambda v, s: {'value': v, 'source': s, 'date': '2026-02-01', 'ring': 'Company'}


# --- 1: SWDY's defect exactly as it stands, made visible -------------------------
# 17,330.245 / 2,140.778 = 8.095 against a reported 7.13. The employees' statutory
# share, 12.0% of attributable profit, standing between profit and shareholders.
def c1(d):
    put(d, 'swdy', inputs={'eps_fy25': I(7.13, 'audited FY2025 statements, note 39')})
case("SWDY's own figures: 8.095 computed against a reported 7.13",
     c1, True, lambda d: 'eps_fy25' in json.load(open(nf(d, 'swdy')))['inputs'])


# --- 2: the same gap, NAMED — must pass ------------------------------------------
def c2(d):
    put(d, 'swdy', inputs={'eps_fy25': I(7.13, 'audited FY2025 statements, note 39')},
        eps_reconciliation={'what': "employees' statutory share of distributable profits",
                            'difference': 2073.104844,
                            'charged_in_the_valuation': True})
case('the same gap with an eps_reconciliation record naming it',
     c2, False, lambda d: (json.load(open(nf(d, 'swdy'))).get('eps_reconciliation') or {})
                          .get('difference') is not None)


# --- 3: a record that declares the gap and NAMES NOTHING must still fail ----------
def c3(d):
    put(d, 'swdy', inputs={'eps_fy25': I(7.13, 'audited FY2025 statements, note 39')},
        eps_reconciliation={'difference': 2073.104844})
case('a record carrying a number and no explanation — declaration without content',
     c3, True, lambda d: 'what' not in (json.load(open(nf(d, 'swdy'))).get('eps_reconciliation') or {}))


# --- 4: a unit mismatch is UNREADABLE, not a reconciliation gap -------------------
# Reported in local thousands against an EPS in another currency. The first run fired
# at +102,936% on exactly this and the gate was re-pointed rather than widened.
def c4(d):
    put(d, 'fertiglobe', inputs={'npa_fy25': I(838541.0, 'thousands'),
                                 'eps_fy25': I(0.11, 'dollars per share')})
case('profit in thousands against an EPS in another currency — a unit mismatch',
     c4, False, lambda d: json.load(open(nf(d, 'fertiglobe')))['inputs']['eps_fy25']['value'] == 0.11)


# --- 5: a study already on the ratchet must stay green ----------------------------
def c5(d):
    pass
case('ADNOCDIST, knowingly on the ratchet, unchanged',
     c5, False, lambda d: 'ADNOCDIST' in json.load(open(os.path.join(
         d, 'engine', 'build_depth_audit', 'eps_outstanding.json')))['outstanding'])


# --- 6: a ratcheted study going FURTHER wrong is still only ratcheted -------------
#      (the ratchet excuses the CONDITION; this documents that and is a clean case)
def c6(d):
    put(d, 'adnocdist', inputs={'eps_fy25': I(0.100, 'materially different')})
case('a ratcheted study whose gap widens — still excused, and recorded as such',
     c6, False, lambda d: json.load(open(nf(d, 'adnocdist')))['inputs']['eps_fy25']['value'] == 0.100)


# --- 7: a genuinely reconciling study must NOT fire -------------------------------
def c7(d):
    D = json.load(open(nf(d, 'arcc')))
    sh = D['meta']['shares_mn']
    D['inputs']['npa_fy25'] = I(sh * 4.0, 'attributable profit')
    D['inputs']['eps_fy25'] = I(4.0, 'reported basic earnings per share')
    json.dump(D, open(nf(d, 'arcc'), 'w'), indent=1, default=float)
case('a study whose profit and share count reproduce its reported EPS exactly',
     c7, False, lambda d: json.load(open(nf(d, 'arcc')))['inputs']['eps_fy25']['value'] == 4.0)


# --- 8: an emptied population must FAIL ------------------------------------------
def c8(d):
    for n in os.listdir(os.path.join(d, 'engine')):
        if n.endswith('_study'):
            shutil.rmtree(os.path.join(d, 'engine', n))
case('no study directories at all',
     c8, True, lambda d: not [n for n in os.listdir(os.path.join(d, 'engine'))
                              if n.endswith('_study')])


# --- 9: studies present, every numbers file gone ---------------------------------
def c9(d):
    for n in os.listdir(os.path.join(d, 'engine')):
        p = os.path.join(d, 'engine', n, 'study_numbers.json')
        if os.path.exists(p):
            os.remove(p)
case('study directories present, not one committed numbers file',
     c9, True, lambda d: not any(os.path.exists(os.path.join(d, 'engine', n,
                                                             'study_numbers.json'))
                                 for n in os.listdir(os.path.join(d, 'engine'))))


# --- 10: a gap INSIDE the printed rounding must not fire -------------------------
def c10(d):
    D = json.load(open(nf(d, 'arcc')))
    sh = D['meta']['shares_mn']
    D['inputs']['npa_fy25'] = I(sh * 4.0002, 'attributable profit')
    D['inputs']['eps_fy25'] = I(4.00, 'reported to two decimals')
    json.dump(D, open(nf(d, 'arcc'), 'w'), indent=1, default=float)
case('a gap smaller than the EPS is printed to — rounding, not a claim',
     c10, False, lambda d: abs(json.load(open(nf(d, 'arcc')))['inputs']['npa_fy25']['value']
                               / json.load(open(nf(d, 'arcc')))['meta']['shares_mn'] - 4.0002) < 1e-6)


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
        print('  [%s] %-62s expected %s, got %s'
              % ('OK ' if ok else 'BAD', name[:62],
                 'RED' if want_red else 'GREEN', 'RED' if got_red else 'GREEN'))
        if not ok:
            fails.append(name)
            print('        ' + out.strip().replace('\n', '\n        ')[-1200:])
        shutil.rmtree(d)

    if fails:
        print('\nFAIL - %d case(s): %s' % (len(fails), '; '.join(fails)))
        return 1
    print('\nOK - %d conditions, every mutation asserted to have landed.' % len(CASES))
    return 0


if __name__ == '__main__':
    sys.exit(main())
