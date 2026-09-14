#!/usr/bin/env python3
"""Prove check_workbook_structure.py actually goes red.  [R-ENF-02]

A check nobody has seen fail is not evidence. This one reinjects, into a throwaway copy of
the tree, each condition the gate exists to catch — including the exact one that shipped:
a seven-sheet workbook whose study attests structure_matches_model=True — and asserts the
gate refuses. It also runs three CLEAN cases that must stay green, because a gate that
fires where no rule exists is the permanently-red check [R-ENF-02] forbids.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import research_protocol as RP                                          # noqa: E402
WANT = list(RP.MODEL_STUDY['excel_sheets'])


def workbook(path, sheets):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for n in sheets:
        wb.create_sheet(n)['A1'] = 'x'
    wb.save(path)


def run(tree):
    env = dict(os.environ)
    # THIS FIXTURE SUPPLIES ITS OWN POPULATION [06-09-2026]. The gate now resolves
    # the book through engine/study_population.py; this control runs it against a
    # sandboxed ENGINE holding studies it planted, which is the point of the
    # control and not a shortcoming of it. The escape is explicit and the gate
    # prints that it took it, so a fixture population can never be mistaken for
    # the real one.
    env['TESTAHIL_FIXTURE_POPULATION'] = '1'
    p = subprocess.run([sys.executable, os.path.join(tree, 'scripts',
                                                     'check_workbook_structure.py')],
                       capture_output=True, text=True, env=env)
    return p.returncode, p.stdout + p.stderr


def sandbox():
    tree = tempfile.mkdtemp(prefix='wbstruct-')
    os.makedirs(os.path.join(tree, 'scripts'))
    os.makedirs(os.path.join(tree, 'engine', 'build_depth_audit'))
    shutil.copy(os.path.join(ROOT, 'scripts', 'check_workbook_structure.py'),
                os.path.join(tree, 'scripts'))
    shutil.copy(os.path.join(ROOT, 'engine', 'research_protocol.py'),
                os.path.join(tree, 'engine'))
    # one clean study, so the population is never empty by accident
    d = os.path.join(tree, 'engine', 'clean_study')
    os.makedirs(d)
    workbook(os.path.join(d, 'CLEAN_Valuation_Model_01092026_public.xlsx'), WANT)
    json.dump({'entries': {}}, open(os.path.join(
        tree, 'engine', 'build_depth_audit', 'workbook_outstanding.json'), 'w'))
    return tree


CASES = []


def case(name, build, want_red):
    CASES.append((name, build, want_red))


def _seven(tree):
    d = os.path.join(tree, 'engine', 'seven_study'); os.makedirs(d)
    workbook(os.path.join(d, 'SEVEN_Valuation_Model_01092026_public.xlsx'),
             ['READ FIRST', 'Assumptions', 'Base Year', 'Product and Cost', 'Forecast',
              'Sensitivity', 'Lenses'])


def _renamed(tree):
    d = os.path.join(tree, 'engine', 'renamed_study'); os.makedirs(d)
    s = list(WANT); s[s.index('SOTP Bridge')] = 'EV Bridge'
    workbook(os.path.join(d, 'RENAMED_Valuation_Model_01092026_public.xlsx'), s)


def _misordered(tree):
    d = os.path.join(tree, 'engine', 'misordered_study'); os.makedirs(d)
    s = list(WANT); s[1], s[2] = s[2], s[1]
    workbook(os.path.join(d, 'MISORDERED_Valuation_Model_01092026_public.xlsx'), s)


def _noworkbook(tree):
    os.makedirs(os.path.join(tree, 'engine', 'empty_study'))


def _corrupt(tree):
    d = os.path.join(tree, 'engine', 'corrupt_study'); os.makedirs(d)
    open(os.path.join(d, 'CORRUPT_Valuation_Model_01092026_public.xlsx'), 'w').write('nope')


def _stranded(tree):
    p = os.path.join(tree, 'engine', 'build_depth_audit', 'workbook_outstanding.json')
    json.dump({'entries': {'GHOST': 'listed but not on disk'}}, open(p, 'w'))


def _emptypop(tree):
    shutil.rmtree(os.path.join(tree, 'engine', 'clean_study'))


def _superseded_is_ignored(tree):
    """A study whose OLD workbook is off the standard but whose LATEST one is not."""
    d = os.path.join(tree, 'engine', 'rebuilt_study'); os.makedirs(d)
    workbook(os.path.join(d, 'REBUILT_Valuation_Model_06082026_public.xlsx'),
             ['READ FIRST', 'Assumptions'])
    workbook(os.path.join(d, 'REBUILT_Valuation_Model_01092026_public.xlsx'), WANT)


def _listed_breach_is_tolerated(tree):
    d = os.path.join(tree, 'engine', 'known_study'); os.makedirs(d)
    workbook(os.path.join(d, 'KNOWN_Valuation_Model_01092026_public.xlsx'),
             ['READ FIRST', 'Assumptions'])
    p = os.path.join(tree, 'engine', 'build_depth_audit', 'workbook_outstanding.json')
    json.dump({'entries': {'KNOWN': 'known breach, on the ratchet'}}, open(p, 'w'))


def _second_clean(tree):
    d = os.path.join(tree, 'engine', 'alsoclean_study'); os.makedirs(d)
    workbook(os.path.join(d, 'ALSOCLEAN_Valuation_Model_31082026_public.xlsx'), WANT)


case('the shipped defect — a seven-sheet workbook', _seven, True)
case('sixteen sheets, one renamed', _renamed, True)
case('sixteen sheets, right names, wrong order', _misordered, True)
case('a study directory with no workbook at all', _noworkbook, True)
case('a workbook that will not open', _corrupt, True)
case('a listed study that no longer resolves on disk', _stranded, True)
case('emptied population — zero studies is not zero problems', _emptypop, True)
case('CLEAN — an old off-standard edition beside a current good one, must PASS',
     _superseded_is_ignored, False)
case('CLEAN — a known breach already on the ratchet, must PASS',
     _listed_breach_is_tolerated, False)
case('CLEAN — a second conforming study, must PASS', _second_clean, False)


def main():
    bad = 0
    for name, build, want_red in CASES:
        tree = sandbox()
        try:
            build(tree)
            rc, out = run(tree)
            red = rc != 0
            ok = (red == want_red)
            bad += 0 if ok else 1
            print('  [%s] %-62s %s' % ('ok' if ok else 'XX', name,
                                       'went red' if red else 'reported clean'))
            if not ok:
                print('\n'.join('        ' + ln for ln in out.strip().splitlines()[-8:]))
        finally:
            shutil.rmtree(tree, ignore_errors=True)
    print()
    if bad:
        print('NEGATIVE CONTROL FAILED — %d case(s) did not behave as required' % bad)
        return 1
    print('negative control OK — the gate goes red on every injected defect and stays '
          'green on all three clean cases')
    return 0


if __name__ == '__main__':
    sys.exit(main())
