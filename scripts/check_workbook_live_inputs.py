#!/usr/bin/env python3
"""An input sheet may not publish a number no formula in the workbook reads.

WHY THIS EXISTS. Every delivered workbook in this book heads its Assumptions sheet with
some form of "blue cells are inputs — change one and the model recomputes". Audited from
outside on 13-09-2026, that sentence was false on study after study:

    SWDY     TWELVE of fifty-six numeric driver rows were referenced by no formula at
             all — copper, the currency path, all three segment growth rates and all
             three segment margins — while the study's own driver test exempted every
             one of them BY NAME and then printed "none — every remaining driver
             reprices the model".
    PHDC     the gross margin published 38.32% against a model running 35.48%; the
             terminal growth published 12% against 7%, and 12% is the alternative the
             study's own contested record marks REJECTED; and a bare "Cost of capital"
             published the rating basis while the model discounts on the swap basis.
    ADNOCLS  the equity risk premium TOTAL sat above the two legs the cost of equity is
             built from and was read by nothing, so the model report's own driver test
             reported that a higher equity risk premium moves fair value by 0.0.

NONE of these is an arithmetic error and every one reaches a reader. A number on a sheet
that says it is an input is a claim about what the model does with it, and where nothing
reads it the claim is false — worse, it usually holds a SUPERSEDED value, because the
thing that keeps a live figure current is the formula that consumes it.

WHAT IS CHECKED. Every cell on an inputs sheet holding a bare number, against every cell
reference appearing in any formula anywhere in the workbook, ranges included. A cell that
nothing references is reported with its label.

WHAT IS DELIBERATELY NOT CHECKED. Whether the input is RIGHT — that is the recalculator's
job — and whether a formula that reads it reaches the answer, which is the driver test's.
This is the cheap structural half: it needs no evaluation engine and cannot be satisfied
by moving a number.

DISPLAY ROWS ARE A REAL CATEGORY AND THEY ARE DECLARED, NOT INFERRED. A sheet may
legitimately print a figure for context — a prior edition's rate, a reference basis the
model does not adopt. Label it so a reader knows: a row whose label carries "reference",
"not used", "for comparison", "alternative", "memo" or "superseded" is exempt, because
the page then tells the reader what this gate would otherwise have to guess.

THE RATCHET [R-ENF-02]. engine/build_depth_audit/live_inputs_outstanding.json holds what
was already breaching when this gate was written, per workbook, and may only SHORTEN.

    python3 scripts/check_workbook_live_inputs.py
    python3 scripts/check_workbook_live_inputs.py --seed
"""
import glob
import json
import os
import re
import sys
import warnings

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

warnings.filterwarnings('ignore')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'live_inputs_outstanding.json')

HOUSE = '*_Valuation_Model_*.xlsx'
# The sheets that tell a reader their cells are inputs.
INPUT_SHEETS = ('assumptions', 'inputs', 'drivers')

# A BARE SHEET NAME MAY NOT START MID-EXPRESSION, AND THE HYPHEN IS WHY.
# The unquoted sheet-name class carried '-', so in "=B11-Assumptions!$B$26*E5" the
# pattern matched "B11-Assumptions" as ONE sheet name -- which resolves to no sheet, so
# the reference was dropped AND B11 was lost with it. SWDY's corporate cost load was
# reported as read by nothing while five formulas read it. The lookbehind requires a real
# boundary before an unquoted name, and a sheet whose name genuinely contains a hyphen is
# written quoted, which the first alternative still accepts.
RANGE = re.compile(r'(?:(?:\'([^\']+)\'|(?<![\w$.])([A-Za-z][\w .&]*))!)?'
                   r'\$?([A-Z]{1,3})\$?(\d+)\s*:\s*\$?([A-Z]{1,3})\$?(\d+)')
REF = re.compile(r'(?:(?:\'([^\']+)\'|(?<![\w$.])([A-Za-z][\w .&]*))!)?\$?([A-Z]{1,3})\$?(\d+)\b')
STRLIT = re.compile(r'"[^"]*"')

# A label that tells the reader this figure is not a driver.
DECLARED_DISPLAY = re.compile(
    r'reference|not used|for comparison|alternative|memo|superseded|retired|'
    r'previous edition|prior edition|published unused|context only|not adopted|'
    r'cross-check|diagnostic', re.I)


def delivered(sdir):
    """The workbook a reader opens."""
    ed = os.path.join(sdir, 'edition.py')
    if os.path.exists(ed):
        ns = {}
        try:
            exec(compile(open(ed, encoding='utf-8').read(), ed, 'exec'), ns)
            name = ns.get('MODEL_XLSX')
        except Exception:                                               # noqa: BLE001
            name = None
        if name and os.path.exists(os.path.join(sdir, name)):
            return os.path.join(sdir, name)
    cands = sorted(glob.glob(os.path.join(sdir, HOUSE)))
    if not cands:
        tk = os.path.basename(sdir)[:-len('_study')].lower()
        cands = sorted(p for p in glob.glob(os.path.join(ROOT, 'files', HOUSE))
                       if os.path.basename(p).lower().startswith(tk))
    if not cands:
        return None

    def key(p):
        m = re.search(r'_(\d{2})(\d{2})(\d{4})', os.path.basename(p))
        return (m.group(3), m.group(2), m.group(1)) if m else ('0000', '00', '00')

    return max(cands, key=key)


def referenced(wb):
    """Every (sheet, coordinate) any formula in the workbook reads."""
    seen = set()
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if not (isinstance(v, str) and v.startswith('=')):
                    continue
                body = STRLIT.sub(' ', v)
                for m in RANGE.finditer(body):
                    sheet = m.group(1) or m.group(2) or ws.title
                    c1, r1, c2, r2 = m.group(3), int(m.group(4)), m.group(5), int(m.group(6))
                    try:
                        from openpyxl.utils import column_index_from_string as ci
                        for col in range(ci(c1), ci(c2) + 1):
                            for rr in range(r1, r2 + 1):
                                seen.add((sheet, '%s%d' % (get_column_letter(col), rr)))
                    except Exception:                                   # noqa: BLE001
                        pass
                for m in REF.finditer(RANGE.sub(' ', body)):
                    sheet = m.group(1) or m.group(2) or ws.title
                    seen.add((sheet, '%s%d' % (m.group(3), int(m.group(4)))))
    return seen


def dead_inputs(path):
    wb = load_workbook(path, data_only=False)
    used = referenced(wb)
    dead, examined = [], 0
    for ws in wb.worksheets:
        if not any(k in ws.title.strip().lower() for k in INPUT_SHEETS):
            continue
        for row in ws.iter_rows():
            label = None
            for c in row:
                if c.column == 1 and isinstance(c.value, str):
                    label = c.value.strip()
                if c.column == 1 or not isinstance(c.value, (int, float)):
                    continue
                if isinstance(c.value, bool):
                    continue
                examined += 1
                if (ws.title, c.coordinate) in used:
                    continue
                if label and DECLARED_DISPLAY.search(label):
                    continue
                dead.append((ws.title, c.coordinate, (label or '(no label)')[:62]))
    return dead, examined


def main():
    seed = '--seed' in sys.argv
    held = {}
    if os.path.exists(OUTSTANDING):
        held = json.load(open(OUTSTANDING, encoding='utf-8')).get('dead', {})

    sdirs = sorted(glob.glob(os.path.join(ENGINE, '*_study')))
    if not sdirs:
        print('FAIL — zero study directories examined [R-ENF-04]')
        return 1

    found, examined, cells, unknown = {}, 0, 0, []
    for sdir in sdirs:
        tk = os.path.basename(sdir)[:-len('_study')].upper()
        p = delivered(sdir)
        if p is None:
            unknown.append((tk, 'no delivered workbook'))
            continue
        try:
            dead, n = dead_inputs(p)
        except Exception as e:                                          # noqa: BLE001
            unknown.append((tk, 'unreadable: %s' % e))
            continue
        examined += 1
        cells += n
        if dead:
            found[tk] = dead

    if seed:
        os.makedirs(os.path.dirname(OUTSTANDING), exist_ok=True)
        json.dump({'_': 'Seeded once, at this gate\'s creation, with every input cell no '
                        'formula reads. The list may only ever SHORTEN: an entry leaves '
                        'when the cell is wired or declared a display row on the page.',
                   'seeded': '2026-09-13',
                   'dead': {k: sorted('%s!%s' % (d[0], d[1]) for d in v)
                            for k, v in found.items()}},
                  open(OUTSTANDING, 'w'), indent=1)
        print('seeded %s with %d workbook(s)' % (OUTSTANDING, len(found)))
        return 0

    print('INPUT CELLS NO FORMULA READS — a sheet that says "change one and the model '
          'recomputes"')
    print('  delivered workbooks examined : %d' % examined)
    print('  input cells inspected        : %d' % cells)
    if examined == 0 or cells == 0:
        print('\nFAIL — an empty result is not a clean result [R-ENF-04]')
        return 1

    hard = {}
    for tk, dead in sorted(found.items()):
        allowed = set(held.get(tk, []))
        live = [d for d in dead if '%s!%s' % (d[0], d[1]) not in allowed]
        print('\n%s — %d input cell(s) no formula reads:' % (tk, len(dead)))
        for sheet, coord, label in dead[:14]:
            tag = '   [ratcheted]' if '%s!%s' % (sheet, coord) in allowed else ''
            print('   %-26s %-6s %s%s' % (sheet, coord, label, tag))
        if len(dead) > 14:
            print('   ... and %d more' % (len(dead) - 14))
        if live:
            hard[tk] = live

    if unknown:
        print('\nUNKNOWN, and unknown is not clean [R-ENF-04] (%d):' % len(unknown))
        for tk, why in unknown:
            print('   %-12s %s' % (tk, why))

    if hard or unknown:
        print('\nFAIL — wire the cell to the formula that should read it, or label it on '
              'the page as the reference it is. Do not delete it quietly: a figure a '
              'reader has seen is a figure somebody may be using.')
        return 1
    print('\nOK — every input cell on every delivered input sheet is read by a formula, '
          'or is labelled on the page as a reference.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
