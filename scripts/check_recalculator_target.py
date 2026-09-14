"""EVERY RECALCULATOR OPENS THE WORKBOOK ITS STUDY ACTUALLY DELIVERS.

WHAT THIS EXISTS TO STOP, found on SWDY 09-09-2026. engine/swdy_study/recalc.py named
SWDY_Valuation_Model_05082026_public.xlsx -- the 5-AUGUST workbook -- and went on naming
it through a 2-September edition and a 9-September one. The workbook is the artefact a
reader recalculates the study in, and recalc.py is the only check that proves it
reproduces the model. So the proof was being taken on a month-old file and reported as
the current edition's, and it PASSED every time, because the old workbook did agree with
the old numbers it was built from.

THAT IS [L-066] IN ITS PUREST FORM: a check that opens a superseded file reports that
file's state as current. It cannot be caught by reading recalc.py, because the name in it
is a real file that really is a workbook of that study; it can only be caught by asking
whether it is the one the study SHIPS.

WHY THIS IS A GATE AND NOT A FIX. Nine studies hardcode a workbook name and eight of them
happen to be right today. They are right by coincidence -- nobody re-issued them -- and
the coincidence expires on the next rebuild. A gate holds them all, including the ones
that do not exist yet.

THE FALSIFIER [R-ENF-07]: scripts/check_recalculator_target_negative_control.py points a
copy of a recalculator at a superseded workbook and requires this to go red.

[R-ENF-01] this runs from outside every study it governs and modifies nothing.
"""
import ast
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')


def _literal_target(src):
    """The workbook filename a recalculator names as a LITERAL, or None if it derives it.

    A derived target (edition.MODEL_XLSX, a newest-on-disk helper) is exactly the shape
    this gate wants and is not examined further -- there is no typed name to go stale.
    """
    for node in ast.walk(ast.parse(src)):
        if not isinstance(node, ast.Assign):
            continue
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if 'XLSX' not in names:
            continue
        for sub in ast.walk(node.value):
            if isinstance(sub, ast.Constant) and isinstance(sub.value, str) \
                    and sub.value.lower().endswith('.xlsx'):
                return sub.value
        return None          # XLSX is assigned, but from something derived
    return None


def _delivered(study_dir):
    """Every workbook this study has on disk, newest first by the DATE IN ITS NAME.

    Modification time is not used and must not be: a rebuild of an old edition, a
    checkout, or a copy would reorder the files without any edition changing. The date a
    study puts in an artefact's own name is the study's own claim about which edition it
    is, which is the claim this gate holds it to.
    """
    out = []
    for p in glob.glob(os.path.join(study_dir, '*[Vv]aluation_[Mm]odel*.xlsx')):
        b = os.path.basename(p)
        m = re.search(r'(\d{2})[-_]?(\d{2})[-_]?(\d{4})', b)
        if not m:
            continue
        d, mo, y = m.groups()
        out.append(((y, mo, d), b))
    return [b for _, b in sorted(out, reverse=True)]


def main():
    rows, red = [], []
    for rc in sorted(glob.glob(os.path.join(ENGINE, '*_study', 'recalc.py'))):
        study = os.path.basename(os.path.dirname(rc))
        named = _literal_target(open(rc, encoding='utf-8').read())
        books = _delivered(os.path.dirname(rc))
        if named is None:
            rows.append((study, 'DERIVED', 'target is derived, not typed — cannot go stale'))
            continue
        if not books:
            # [R-ENF-04] AN ABSENT RESULT IS NOT A CLEAN RESULT. A recalculator naming a
            # workbook where the gate can find none is not "nothing to check": either the
            # name is wrong or the artefact is missing, and both are red.
            red.append((study, named, 'names a workbook but NO dated workbook is on disk'))
            continue
        if named != books[0]:
            red.append((study, named,
                        'names a SUPERSEDED edition; the study delivers ' + books[0]))
            continue
        rows.append((study, 'OK', named))

    print('RECALCULATOR TARGETS — the workbook each recalc.py opens')
    print('  %-24s %-9s %s' % ('study', 'state', 'target'))
    for s, st, t in rows:
        print('  %-24s %-9s %s' % (s, st, t))
    print('\n  %d recalculator(s) examined, %d typed target(s), %d derived'
          % (len(rows) + len(red),
             sum(1 for _, st, _ in rows if st == 'OK') + len(red),
             sum(1 for _, st, _ in rows if st == 'DERIVED')))
    if not rows and not red:
        print('\nRED — no recalculator found at all. An empty population is not a pass '
              '[R-ENF-04]: this gate globs engine/*_study/recalc.py and that glob '
              'returning nothing means the layout moved, not that every study is clean.')
        return 1
    if red:
        print('\nRED — %d recalculator(s) grade a workbook the study does not deliver:' % len(red))
        for s, named, why in red:
            print('   %-22s %s' % (s, why))
            print('   %-22s   it opens %s' % ('', named))
        print('\nThe fix is edition.py, never a retyped name: write the edition once and '
              'derive every artefact filename from it.')
        return 1
    print('\nOK — every recalculator opens the workbook its study delivers.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
