#!/usr/bin/env python3
"""Negative control for [R-ENF-01]'s sign-convention gate.

A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE. Every condition is reinjected and the
instrument must flag it; every clean case must NOT fire. The clean cases carry as much
weight as the defects here, because the first draft flagged a row reading
"less: complexity / conglomerate discount | 10% | (4,629)" — the RATE bare and the AMOUNT
in parentheses, both perfectly clear — and per [R-COC-01] a check firing on work that is
right is re-pointed rather than widened. That case is kept below as a clean one.
"""
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import table_residual as TR                                            # noqa: E402


def hits(rows):
    return bool(TR.sign_conventions(rows)) or bool(TR.sign_conventions_across(rows))


CASES = [
    ('1  brackets throughout and one bare positive the model adds, exactly as shipped', [
        ['AED million', '2026E'],
        ['Revenue', '43,836'],
        ['Less cash operating expenses', '(2,650)'],
        ['Less impairment and credit losses', '(360)'],
        ['EBITDA', '5,410'],
        ['Less depreciation and amortisation', '(792)'],
        ['Less capital expenditure', '(1,012)'],
        ['Less increase in working capital', '440'],
        ['Free cash flow to the firm', '4,368'],
    ], True),
    ('2  bare magnitudes throughout and one signed negative, exactly as shipped', [
        ['AED mn', 'FY27E'],
        ['EBITDA', '2,286'],
        ['less depreciation & amortisation', '810'],
        ['less owned capex', '1,900'],
        ['less change in working capital', '-373'],
        ['Free cash flow to the firm', '187'],
    ], True),
    ('3  one row switching convention between adjacent years, exactly as shipped', [
        ['EGP million', '2026', '2027'],
        ['Operating profit after tax', '14,637', '17,352'],
        ['less capital spend', '-2,319', '-2,793'],
        ['less increase in homes built ahead of handover', '855', '-4,550'],
        ['Free cash flow to the firm', '24,855', '37,016'],
    ], True),
    ('4  signed negatives throughout — one convention, must NOT fire', [
        ['EGP million', 'FY2026/27'],
        ['NOPAT', '3,039'],
        ['Less capital expenditure', '-2,729'],
        ['Less change in working capital', '-220'],
        ['FREE CASH FLOW TO THE FIRM', '90'],
    ], False),
    ('5  brackets throughout — one convention, must NOT fire', [
        ['USD mn', '2026E'],
        ['Revenue', '5,003'],
        ['Less operating costs', '(2,917)'],
        ['Less depreciation and amortisation', '(575)'],
        ['EBIT', '1,511'],
    ], False),
    ('6  bare magnitudes throughout — one convention, must NOT fire', [
        ['USD million', '2026'],
        ['Revenue', '5,932'],
        ['Less: feedstock', '1,264'],
        ['Less: other production costs', '1,684'],
        ['EBITDA', '2,984'],
    ], False),
    ('7  a RATE bare beside its AMOUNT in parentheses — must NOT fire', [
        ['Leg', 'Basis', 'Value (EGP mn)'],
        ['Sum of the parts', '', '46,291'],
        ['less: complexity / conglomerate discount', '10%', '(4,629)'],
        ['SOTP equity value', '', '41,662'],
    ], False),
    ('8  a note column carrying "26.3% of equity value" is not a convention', [
        ['Line', 'Value', 'Note'],
        ['Enterprise value', '(3,525)', 'the net debt figure'],
        ['less net debt', '(3,525)', '26.3% of equity value'],
        ['Equity value', '20,869', ''],
    ], False),
    ('9  a dash and a nil are not-applicable, not a convention', [
        ['USD mn', '2026E', '2027E'],
        ['Free cash flow', '215', '1,060'],
        ['Less the first quarter already elapsed', '(130)', '—'],
        ['Free cash flow from the valuation date', '85', '1,060'],
    ], False),
    ('10 a table with no deduction row at all is silent', [
        ['Lens', 'Value'],
        ['Cash flow', '43.81'],
        ['Relative multiples', '55.88'],
    ], False),
]


def gate_cases():
    """The gate's own population anchoring, in a sandbox."""
    def sandbox():
        d = tempfile.mkdtemp(prefix='sc-nc-')
        dst = os.path.join(d, 'repo')
        os.makedirs(dst)
        for item in ('scripts', 'engine'):
            shutil.copytree(os.path.join(ROOT, item), os.path.join(dst, item),
                            ignore=shutil.ignore_patterns('*.pdf', '*.png', '*.xlsx',
                                                          '__pycache__', 'raw_ohlc',
                                                          'raw_indices', 'lab'))
        return d, dst

    def run(cwd):
        p = subprocess.run([sys.executable, 'scripts/check_sign_convention.py'],
                           cwd=cwd, capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr

    out = []
    # 11 — an emptied population must FAIL, not report clean
    d, dst = sandbox()
    try:
        n = 0
        for root, _, files in os.walk(os.path.join(dst, 'engine')):
            for f in files:
                if f.endswith('.docx'):
                    os.remove(os.path.join(root, f))
                    n += 1
        assert n, 'fixture never injected: no documents were removed'
        rc, txt = run(dst)
        out.append(('11 an emptied population must FAIL, not report clean',
                    rc != 0 and 'zero' in txt.lower()))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    # 12 — a ratchet naming a study not on disk must FAIL
    d, dst = sandbox()
    try:
        import json
        p = os.path.join(dst, 'engine', 'build_depth_audit', 'signconv_outstanding.json')
        j = json.load(open(p))
        j['outstanding'].append('NOSUCHCO')
        json.dump(j, open(p, 'w'), indent=1)
        assert 'NOSUCHCO' in json.load(open(p))['outstanding']
        rc, txt = run(dst)
        out.append(('12 a ratchet naming a study not on disk must FAIL',
                    rc != 0 and 'NOSUCHCO' in txt))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    # 13 — the repository as it stands must stay GREEN
    d, dst = sandbox()
    try:
        rc, txt = run(dst)
        out.append(('13 the repository as it stands must stay GREEN', rc == 0))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return out


def main():
    fails = []
    for name, rows, must in CASES:
        got = hits(rows)
        ok = (got == must)
        print('  %-4s %s' % ('ok' if ok else 'FAIL', name))
        if not ok:
            fails.append(name)
    for name, ok in gate_cases():
        print('  %-4s %s' % ('ok' if ok else 'FAIL', name))
        if not ok:
            fails.append(name)
    total = len(CASES) + 3
    print('\n%d/%d conditions behaved as required' % (total - len(fails), total))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
