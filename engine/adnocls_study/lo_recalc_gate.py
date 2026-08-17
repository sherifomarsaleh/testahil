"""Gate — does the delivered workbook OPEN IN A COMPUTABLE STATE?

recalc.py evaluates the workbook with an independent reimplementation of the arithmetic.
That is a strong check on whether the formulas say what the model says, but it is not a
check on whether a real spreadsheet application can compute them at all. Those are
different questions, and the difference is not academic: the first edition of this workbook
reconciled cell-for-cell under recalc.py while raising #VALUE! in 689 cells across twelve
sheets the moment it was opened. The text '-' sat in two Assumptions cells that a Segments
formula multiplied, and the error cascaded through the cash-flow waterfall, the Summary and
nine other sheets.

So this gate hands the file to LibreOffice, which recalculates on load, converts it back,
and counts every error value of every kind — #VALUE!, #REF!, #DIV/0!, #NAME?, #N/A, #NULL!
and #NUM!. ONE is a failure. It runs before delivery, and it is the only thing in this
study that can prove the reader will not open a sheet of errors.

Usage:  python3 lo_recalc_gate.py [path/to/workbook.xlsx]
"""
import collections
import os
import re
import shutil
import subprocess
import sys
import tempfile

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = os.path.join(HERE, 'ADNOCLS_Valuation_Model_09082026_public.xlsx')
# every error value a spreadsheet can put in a cell; localisation aside, they all begin '#'
ERRORS = ('#VALUE!', '#REF!', '#DIV/0!', '#NAME?', '#N/A', '#NULL!', '#NUM!')
ERR_RE = re.compile(r'^#[A-Z/0-9]+[!?]?$')


def soffice():
    for name in ('soffice', 'libreoffice'):
        p = shutil.which(name)
        if p:
            return p
    sys.exit('FAIL — LibreOffice is not installed, so the workbook cannot be proved '
             'computable. This gate does not pass by default when it cannot run.')


def recalculate(path, workdir):
    """Round-trip the workbook through LibreOffice, which recalculates it on load."""
    env = dict(os.environ, HOME=workdir)
    r = subprocess.run(
        [soffice(), '--headless', '--norestore', '-env:UserInstallation=file://'
         + os.path.join(workdir, 'profile'), '--convert-to', 'xlsx', '--outdir', workdir,
         path],
        capture_output=True, text=True, timeout=900, env=env)
    out = os.path.join(workdir, os.path.basename(path))
    if not os.path.exists(out):
        sys.exit(f'FAIL — LibreOffice did not produce a recalculated file.\n'
                 f'{r.stdout}\n{r.stderr}')
    return out


def scan(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    per_sheet = collections.OrderedDict((ws.title, []) for ws in wb.worksheets)
    kinds = collections.Counter()
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, str) and ERR_RE.match(v.strip()):
                    per_sheet[ws.title].append((c.coordinate, v.strip()))
                    kinds[v.strip()] += 1
    return per_sheet, kinds


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    src = os.path.abspath(src)
    if not os.path.exists(src):
        sys.exit(f'FAIL — no such workbook: {src}')
    with tempfile.TemporaryDirectory() as workdir:
        out = recalculate(src, workdir)
        per_sheet, kinds = scan(out)

    total = sum(len(v) for v in per_sheet.values())
    width = max(len(s) for s in per_sheet) + 2
    print(f'LIBREOFFICE RECALCULATION GATE — {os.path.basename(src)}\n')
    print(f"  {'Sheet':{width}s} {'Errors':>7s}   First cells")
    print(f"  {'-' * width} {'-' * 7}   {'-' * 40}")
    for sheet, errs in per_sheet.items():
        sample = ', '.join(f'{c}={v}' for c, v in errs[:4]) if errs else ''
        print(f'  {sheet:{width}s} {len(errs):>7d}   {sample}')
    print(f"  {'-' * width} {'-' * 7}")
    print(f"  {'TOTAL':{width}s} {total:>7d}")
    if kinds:
        print('\n  by kind: ' + ', '.join(f'{k} {n}' for k, n in kinds.most_common()))
    print()
    if total:
        sys.exit(f'LIBREOFFICE RECALCULATION GATE FAILED — {total} error cells across '
                 f'{sum(1 for v in per_sheet.values() if v)} sheets. The workbook does not '
                 f'compute in the application the reader opens it in.')
    print(f'LIBREOFFICE RECALCULATION GATE OK — {len(per_sheet)} sheets recalculated, 0 '
          f'error cells of any kind ({", ".join(ERRORS)})')


if __name__ == '__main__':
    main()
