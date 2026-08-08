"""Render the delivered xlsx model to PDF with its VALUES visible.

The delivered workbook is formula-driven and openpyxl stores no cached results, so a
headless LibreOffice conversion — which does not recalculate on load — rendered every
formula cell BLANK: the published model PDF showed only the pasted inputs. (Found in this
study's own re-audit; no external reviewer caught it.)

Fix: evaluate every formula with the same independent evaluator that carries the recalc
gate (xlcalc), write the results into a values-only copy, convert THAT to PDF under the
delivered file's name, and delete the copy. The delivered .xlsx keeps its formulas.
"""
import os, shutil, subprocess, sys, tempfile
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'SWDY_Valuation_Model_05082026_public.xlsx')

wb = openpyxl.load_workbook(SRC)
bk = xlcalc.Book(wb)
cells = list(bk.formula_cells())
for sh, coord in cells:
    v = bk.cell_value(sh, coord)
    wb[sh][coord].value = v
print(f'baked {len(cells)} formula results into a values copy')

with tempfile.TemporaryDirectory() as tmp:
    baked = os.path.join(tmp, 'SWDY_Valuation_Model_05082026_public.xlsx')
    wb.save(baked)
    env = dict(os.environ, HOME=tmp)
    r = subprocess.run(['soffice', '--headless',
                        f'-env:UserInstallation=file://{tmp}/profile',
                        '--convert-to', 'pdf', '--outdir', HERE, baked],
                       capture_output=True, text=True, timeout=600, env=env)
    out = os.path.join(HERE, 'SWDY_Valuation_Model_05082026_public.pdf')
    if not os.path.exists(out) or os.path.getsize(out) == 0:
        sys.exit(f'FAIL: no PDF produced\n{r.stdout}\n{r.stderr}')
    print(f'wrote {out} ({os.path.getsize(out)/1024:,.0f} KB) with values visible')
