"""THE FALSIFIER FOR check_recalculator_target.py [R-ENF-07].

A gate that has never been seen to go red is a gate nobody has tested. This one plants
the exact defect found on SWDY on 09-09-2026 -- a recalculator naming a superseded
workbook -- into a throwaway tree and requires the gate to CATCH it. It also plants the
two neighbouring shapes: a recalculator naming a workbook that is not on disk at all
[R-ENF-04], and an empty population, which must be red rather than a silent pass.

CASE 4 IS THE ONE THAT MATTERS MOST AND IT IS A PASS CASE: a recalculator that DERIVES
its target must stay green. A gate that went red on the correct construction would push
studies back towards typed names to stay green, which is the opposite of the point.

[R-ENF-01] this builds its own tree in a temporary directory and never touches the repo.
"""
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, 'scripts', 'check_recalculator_target.py')


def _study(tmp, name, recalc_body, workbooks):
    d = os.path.join(tmp, 'engine', name)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'recalc.py'), 'w', encoding='utf-8').write(recalc_body)
    for wb in workbooks:
        open(os.path.join(d, wb), 'w', encoding='utf-8').write('not really a workbook')
    return d


def _run(tmp):
    gate = os.path.join(tmp, 'scripts', 'check_recalculator_target.py')
    os.makedirs(os.path.dirname(gate), exist_ok=True)
    shutil.copy(GATE, gate)
    p = subprocess.run([sys.executable, gate], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def case(label, build, expect_red):
    tmp = tempfile.mkdtemp(prefix='recalc_nc_')
    try:
        build(tmp)
        rc, out = _run(tmp)
        got_red = rc != 0
        ok = got_red == expect_red
        print('  [%s] %s' % ('PASS' if ok else 'FAIL', label))
        if not ok:
            print('      expected %s, got exit %d' % ('RED' if expect_red else 'GREEN', rc))
            print('      ' + out.strip().replace('\n', '\n      '))
        return ok
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


TYPED = ("import os\nHERE = os.path.dirname(__file__)\n"
         "XLSX = os.path.join(HERE, '%s')\n")
DERIVED = ("import os\nimport edition as _ed\nHERE = os.path.dirname(__file__)\n"
           "XLSX = os.path.join(HERE, _ed.MODEL_XLSX)\n")


def main():
    ok = True

    ok &= case('1 the SWDY defect — recalculator names a SUPERSEDED workbook while a '
               'newer edition sits beside it',
               lambda t: _study(t, 'swdy_study', TYPED % 'SWDY_Valuation_Model_05082026_public.xlsx',
                                ['SWDY_Valuation_Model_05082026_public.xlsx',
                                 'SWDY_Valuation_Model_09092026_public.xlsx']),
               expect_red=True)

    ok &= case('2 recalculator names a workbook that is not on disk at all — absent is '
               'not clean [R-ENF-04]',
               lambda t: _study(t, 'ghost_study', TYPED % 'GHOST_Valuation_Model_01012026_public.xlsx',
                                []),
               expect_red=True)

    ok &= case('3 no recalculator anywhere — an empty population is not a pass [R-ENF-04]',
               lambda t: os.makedirs(os.path.join(t, 'engine'), exist_ok=True),
               expect_red=True)

    ok &= case('4 THE CORRECT CONSTRUCTION STAYS GREEN — a derived target is never stale, '
               'even with three editions on disk',
               lambda t: _study(t, 'good_study', DERIVED,
                                ['GOOD_Valuation_Model_05082026_public.xlsx',
                                 'GOOD_Valuation_Model_02092026_public.xlsx',
                                 'GOOD_Valuation_Model_09092026_public.xlsx']),
               expect_red=False)

    ok &= case('5 a typed target that IS the newest edition stays green — the gate holds '
               'the name against the artefacts, not against the style',
               lambda t: _study(t, 'fine_study', TYPED % 'FINE_Valuation_Model_09092026_public.xlsx',
                                ['FINE_Valuation_Model_05082026_public.xlsx',
                                 'FINE_Valuation_Model_09092026_public.xlsx']),
               expect_red=False)

    print('\nNEGATIVE CONTROL %s — check_recalculator_target.py %s'
          % ('OK' if ok else 'FAILED',
             'goes red on the defect it was built for and stays green on the correct '
             'construction' if ok else 'does NOT behave as claimed'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
