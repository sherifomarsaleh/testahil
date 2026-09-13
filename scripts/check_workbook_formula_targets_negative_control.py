#!/usr/bin/env python3
"""A check nobody has seen fail is not evidence.

Each condition is injected into a SANDBOX COPY and the gate must go red on it, or stay
green where the condition is legitimate. Every mutation is asserted to have LANDED before
the gate runs: a control whose edit silently missed proves only that the file was
untouched.

THE CASE THAT MATTERS IS 1 — the TMGH defect verbatim: a formula whose single-cell
reference lands on a blank, discounting at zero in a file a reader opens while the study's
own recalculation reported 85 of 85 clean. Case 2 is its twin and must stay GREEN: an
empty cell inside a SUM range is ordinary and deliberate, and a gate that cannot tell the
two apart would be untrue on almost every workbook in the book.
"""
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

from openpyxl import Workbook, load_workbook

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join('scripts', 'check_workbook_formula_targets.py')
RAT = os.path.join('engine', 'build_depth_audit',
                   'workbook_formula_targets_outstanding.json')


def book(path, *, dangling=False, in_range=False, cross_sheet_blank=False):
    """A minimal two-sheet workbook: three cash flows, a rate, a discounted sum."""
    wb = Workbook()
    s = wb.active
    s.title = 'Summary'
    s['A1'] = 'Cost of capital'
    s['B1'] = 0.12                       # the rate lives at B1
    d = wb.create_sheet('DCF')
    d['A1'] = 'Cash flow'
    for i, v in enumerate((100.0, 110.0, 121.0)):
        d.cell(row=1, column=2 + i, value=v)
    d['A2'] = 'Discount factor'
    row = 9 if dangling else 1           # B9 on Summary is blank; B1 holds the rate
    for i in range(3):
        d.cell(row=2, column=2 + i,
               value="=1/(1+'Summary'!$B$%d)^%d" % (row, i + 1))
    d['A3'] = 'Present value'
    for i in range(3):
        col = chr(ord('B') + i)
        d.cell(row=3, column=2 + i, value='=%s1*%s2' % (col, col))
    if in_range:
        # a deliberately empty fourth column inside the summed range
        d['A4'] = 'Sum of the explicit years'
        d['B4'] = '=SUM(B3:E3)'
    if cross_sheet_blank:
        d['A5'] = 'Equity value'
        d['B5'] = "='Summary'!B7"        # B7 was never written
    wb.save(path)


def sandbox(**kw):
    t = tempfile.mkdtemp(prefix='wbft_nc_')
    os.makedirs(os.path.join(t, 'scripts'))
    os.makedirs(os.path.join(t, 'engine', 'build_depth_audit'))
    os.makedirs(os.path.join(t, 'engine', 'alpha_study'))
    os.makedirs(os.path.join(t, 'files'))
    shutil.copy(os.path.join(ROOT, GATE), os.path.join(t, GATE))
    json.dump({'dangling': {}, 'note': 'sandbox'}, open(os.path.join(t, RAT), 'w'))
    book(os.path.join(t, 'engine', 'alpha_study',
                      'ALPHA_Valuation_Model_01012026.xlsx'), **kw)
    return t


def run(t):
    r = subprocess.run([sys.executable, GATE], cwd=t, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True, timeout=300)
    return r.returncode, r.stdout


def landed(t, want, sheet='DCF', cell='B2'):
    """Assert the mutation actually reached the file before the gate is asked about it."""
    p = os.path.join(t, 'engine', 'alpha_study', 'ALPHA_Valuation_Model_01012026.xlsx')
    v = load_workbook(p)[sheet][cell].value
    assert want in str(v), 'the injected formula did not land: %r' % (v,)


CASES = []


def case(name, expect_red, build, verify=None):
    CASES.append((name, expect_red, build, verify))


case('1. a single-cell reference onto a blank — TMGH verbatim', True,
     lambda: sandbox(dangling=True),
     lambda t: landed(t, "$B$9"))
case('2. an empty cell INSIDE a summed range — ordinary, must stay green', False,
     lambda: sandbox(in_range=True),
     lambda t: landed(t, 'SUM(B3:E3)', cell='B4'))
case('3. a cross-sheet reference onto a blank', True,
     lambda: sandbox(cross_sheet_blank=True),
     lambda t: landed(t, "'Summary'!B7", cell='B5'))
case('4. a clean workbook', False, lambda: sandbox(), None)


def strip_studies(t):
    shutil.rmtree(os.path.join(t, 'engine', 'alpha_study'))
    return t


def blank_workbook(t):
    """A workbook with no formulas at all — an empty result is not a clean one."""
    p = os.path.join(t, 'engine', 'alpha_study', 'ALPHA_Valuation_Model_01012026.xlsx')
    wb = Workbook()
    wb.active['A1'] = 'nothing here'
    wb.save(p)
    return t


case('5. no study directories at all', True, lambda: strip_studies(sandbox()), None)
case('6. a workbook holding not one formula', True,
     lambda: blank_workbook(sandbox()), None)


def ratchet_excuses(t):
    json.dump({'dangling': {'alpha': {'workbook': 'ALPHA_Valuation_Model_01012026.xlsx',
                                      'count': 3, 'note': 'recorded'}}},
              open(os.path.join(t, RAT), 'w'))
    return t


def ratchet_grew(t):
    json.dump({'dangling': {'alpha': {'workbook': 'ALPHA_Valuation_Model_01012026.xlsx',
                                      'count': 1, 'note': 'recorded when it was one'}}},
              open(os.path.join(t, RAT), 'w'))
    return t


def ratchet_stale(t):
    json.dump({'dangling': {'alpha': {'workbook': 'ALPHA_Valuation_Model_01012026.xlsx',
                                      'count': 3, 'note': 'fixed, never removed'}}},
              open(os.path.join(t, RAT), 'w'))
    return t


case('7. a recorded failure at its recorded size — excused', False,
     lambda: ratchet_excuses(sandbox(dangling=True)), None)
case('8. a recorded failure that GREW — red despite the ratchet', True,
     lambda: ratchet_grew(sandbox(dangling=True)), None)
case('9. a clean study still on the ratchet — the list must shorten', True,
     lambda: ratchet_stale(sandbox()), None)


def main():
    bad = []
    for name, expect_red, build, verify in CASES:
        t = build()
        try:
            if verify:
                verify(t)
            rc, out = run(t)
            red = rc != 0
            ok = red == expect_red
            print('%-58s %-5s %s' % (name, 'RED' if red else 'green',
                                     'ok' if ok else '*** NOT AS REQUIRED'))
            if not ok:
                bad.append((name, out))
        finally:
            shutil.rmtree(t, ignore_errors=True)
    if bad:
        print('\n%d condition(s) did not behave as required:' % len(bad))
        for n, o in bad:
            print('\n--- %s\n%s' % (n, o))
        return 1
    print('\nall %d conditions behave as required' % len(CASES))
    return 0


if __name__ == '__main__':
    sys.exit(main())
