"""Bake this study's delivered workbook to a values-visible PDF.

WHY NOT THE SHARED BAKER. engine/bake_model_pdf_shared.py evaluates the workbook's
formulas through a study's own xlcalc module and writes the answers in before rendering;
this study has no xlcalc module — its recalculator carries its own evaluator instead —
so the spreadsheet program does the evaluating here. The requirement is the same either
way: the file a reader opens must show VALUES, not empty formula cells.

WHAT THIS CLOSES. This study's build had no PDF step at all. Passing --pdf did nothing,
because there was nothing to do it, and the three delivered PDFs sat a whole edition
behind the documents they are rendered from while every rebuild reported clean.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import edition as _EDN                                                # noqa: E402


def main():
    src = os.path.join(HERE, _EDN.MODEL_XLSX)
    if not os.path.exists(src):
        sys.exit('FAIL: %s does not exist. Build the workbook before baking it.' % src)
    out = os.path.join(HERE, _EDN.MODEL_PDF)
    before = os.path.getmtime(out) if os.path.exists(out) else 0
    r = subprocess.run(['soffice', '--headless', '--convert-to', 'pdf',
                        '--outdir', HERE, src], capture_output=True, timeout=900)
    if not os.path.exists(out) or os.path.getmtime(out) <= before:
        sys.exit('FAIL: %s was not written. %s'
                 % (_EDN.MODEL_PDF, (r.stderr or b'').decode('utf-8', 'replace')[:300]))
    print('wrote %s (%d KB)' % (_EDN.MODEL_PDF, os.path.getsize(out) // 1024))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
