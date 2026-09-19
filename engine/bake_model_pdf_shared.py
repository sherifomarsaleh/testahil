"""Render a delivered xlsx model to PDF with its VALUES visible. SHARED.

WHY IT EXISTS. The delivered workbook is formula-driven and openpyxl stores no cached
results, so a headless LibreOffice conversion — which does not recalculate on load —
renders every formula cell BLANK: the published model PDF shows only the pasted inputs.
Found in SWDY's own re-audit; no external reviewer caught it.

WHAT IT DOES. Evaluates every formula with the same independent evaluator that carries the
recalc gate, writes the results into a values-only copy, converts THAT to PDF under the
delivered file's name, and deletes the copy. The delivered .xlsx keeps its formulas.

WHY IT IS SHARED [10-09-2026]. It lived in swdy_study and was COPIED into egch_study,
whose model PDF did not exist for its current edition. Two copies of one builder is the
defect this repository keeps finding under other names, and it was created here by the fix
for another one. The study-specific parts are exactly two — the directory and the edition
module — so both are parameters and there is one builder.

    python3 -c "import sys; sys.path.insert(0,'..'); import bake_model_pdf as b; b.main()"

or, from a study directory, the four-line shim each one carries.
"""
import os
import shutil
import subprocess
import sys
import tempfile

import openpyxl


def bake(study_dir, edition_module, xlcalc_module):
    """Bake one study's delivered workbook to a values-visible PDF beside it."""
    src = os.path.join(study_dir, edition_module.MODEL_XLSX)
    if not os.path.exists(src):
        sys.exit('FAIL: %s does not exist. Build the workbook before baking it.' % src)
    wb = openpyxl.load_workbook(src)
    bk = xlcalc_module.Book(wb)
    cells = list(bk.formula_cells())
    for sh, coord in cells:
        wb[sh][coord].value = bk.cell_value(sh, coord)
    print('baked %d formula results into a values copy' % len(cells))

    with tempfile.TemporaryDirectory() as tmp:
        baked = os.path.join(tmp, edition_module.MODEL_XLSX)
        wb.save(baked)
        env = dict(os.environ, HOME=tmp)
        r = subprocess.run(['soffice', '--headless',
                            '-env:UserInstallation=file://%s/profile' % tmp,
                            '--convert-to', 'pdf', '--outdir', study_dir, baked],
                           capture_output=True, text=True, timeout=600, env=env)
        out = os.path.join(study_dir, edition_module.MODEL_XLSX[:-5] + '.pdf')
        if not os.path.exists(out) or os.path.getsize(out) == 0:
            sys.exit('FAIL: no PDF produced\n%s\n%s' % (r.stdout, r.stderr))
        print('wrote %s (%s KB) with values visible'
              % (out, format(os.path.getsize(out) / 1024, ',.0f')))
    return out
