#!/usr/bin/env python3
"""Negative control for [R-BETA-05] — check_beta_estimator_disclosure.py.

Every case is built in a SANDBOX COPY and nothing is written into the real tree
[R-ENF-01 EXTENDED 07-09-2026]: there is no undo that has to run. Every mutation ASSERTS
THAT IT LANDED before the gate is invoked, because this project has four times caught a
control passing a fixture that never injected its condition; and the case COUNT is asserted
against a declared constant, because a control that quietly loses cases reports clean.

Each case first requires the gate GREEN on the unmutated sandbox, so a red afterwards was
caused by the mutation rather than by something already broken.

RED cases (the gate must FAIL):
  1  a Dimson study quoting the diagnostics and naming no estimator          -- the rule
  2  the SAME, on the nested record shape                                    -- the adapter
  3  an unrecognised record shape                                            -- [L-355]
  4  a ratcheted study that stopped failing and was not pruned               -- [R-ENF-02]
  5  zero study directories                                                  -- [R-ENF-04]
  6  study directories present, zero beta records read                       -- [R-ENF-04]

CLEAN cases (the gate must PASS), and this half is the one that matters:
  7  a study that names the estimator in a TABLE CELL rather than a paragraph -- the exemplar's
     own shape, and the shape a paragraph-only reader misses
  8  a Dimson study quoting NO testable diagnostic                            -- nothing to test
  9  a NON-Dimson record                                                      -- out of scope
 10  a study with a beta record and no delivered document                     -- out of scope
"""
import json, os, re, shutil, subprocess, sys, tempfile

EXPECTED_CASES = 10
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = 'scripts/check_beta_estimator_disclosure.py'


def sandbox():
    d = tempfile.mkdtemp(prefix='betaest_nc_')
    os.makedirs(os.path.join(d, 'scripts'))
    os.makedirs(os.path.join(d, 'engine', 'build_depth_audit'))
    shutil.copy(os.path.join(ROOT, GATE), os.path.join(d, GATE))
    return d


def make_doc(path, text):
    from docx import Document
    doc = Document()
    for para in text.split('\n'):
        doc.add_paragraph(para)
    doc.save(path)


def make_doc_with_table(path, para_text, cells):
    from docx import Document
    doc = Document()
    doc.add_paragraph(para_text)
    t = doc.add_table(rows=1, cols=len(cells))
    for i, c in enumerate(cells):
        t.rows[0].cells[i].text = c
    doc.save(path)


QUOTED = ("Beta 1.4718 - the stock's own weekly returns regressed against the exchange's "
          "published index over 4.85 years, 251 observations, explaining 32.6% of the "
          "variation, standard error 0.185.")
UNQUOTED = "Beta 1.4718, regressed against the exchange's published index over 4.85 years."


def plant(d, tk, numbers, doc_text=None, table_cells=None, doc=True):
    sd = os.path.join(d, 'engine', f'{tk.lower()}_study')
    os.makedirs(sd, exist_ok=True)
    json.dump(numbers, open(os.path.join(sd, 'study_numbers.json'), 'w'))
    if doc:
        p = os.path.join(sd, f'{tk}_Valuation_Study_18-09-2026.docx')
        if table_cells:
            make_doc_with_table(p, doc_text or QUOTED, table_cells)
        else:
            make_doc(p, doc_text or QUOTED)
    return sd


def flat(dimson=True):
    return {'wacc': {'beta_record': {'beta': 1.4718, 'se': 0.185, 'r2': 0.326,
                                     'n': 251, 'dimson': dimson}}}


def nested():
    return {'wacc': {'beta_record': {'beta': 0.3507,
                                     'dimson': {'sum_beta': 0.3507, 'se_sum': 0.178,
                                                'coefficients': {'lead': 0.02},
                                                'note': 'Dimson (1979) sum-beta'}}}}


def run(d, ratchet):
    json.dump({'rule': '[R-BETA-05]', 'outstanding': ratchet},
              open(os.path.join(d, 'engine', 'build_depth_audit',
                                'beta_estimator_outstanding.json'), 'w'))
    r = subprocess.run([sys.executable, GATE], cwd=d, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def case(n, label, build, ratchet, expect_red):
    d = sandbox()
    try:
        # a clean baseline that must be GREEN, so a red afterwards is the mutation's doing
        plant(d, 'BASE', flat(), doc_text=UNQUOTED)
        rc0, out0 = run(d, {})
        if rc0 != 0 and n not in (5, 6):
            print('   SETUP FAIL case %d — sandbox is not green before the mutation' % n)
            return False
        landed = build(d)
        if not landed:
            print('   FIXTURE DID NOT LAND case %d — %s' % (n, label))
            return False
        rc, out = run(d, ratchet)
        red = rc != 0
        good = (red == expect_red)
        print('   %s case %-2d %s' % ('CAUGHT ' if good and expect_red else
                                      'PASSED ' if good else 'MISSED ', n, label))
        if not good:
            print('      ' + out.strip().splitlines()[-1][:160])
        return good
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    results = []

    def c1(d):
        sd = plant(d, 'RED1', flat())
        return os.path.exists(os.path.join(sd, 'study_numbers.json'))
    results.append(case(1, 'Dimson, quotes the diagnostics, names no estimator', c1, {}, True))

    def c2(d):
        sd = plant(d, 'RED2', nested())
        return json.load(open(os.path.join(sd, 'study_numbers.json')))['wacc']['beta_record']['dimson']['note']
    results.append(case(2, 'the NESTED record shape, same breach', c2, {}, True))

    def c3(d):
        sd = plant(d, 'RED3', {'wacc': {'beta_record': {'dimson': 12345}}})
        return json.load(open(os.path.join(sd, 'study_numbers.json')))['wacc']['beta_record']['dimson'] == 12345
    results.append(case(3, 'an unrecognised record shape is RED, never skipped', c3, {}, True))

    def c4(d):
        sd = plant(d, 'RED4', flat(), doc_text=UNQUOTED)   # no longer fails
        return os.path.isdir(sd)
    results.append(case(4, 'a ratcheted study that stopped failing and was not pruned',
                        c4, {'RED4': 'was failing'}, True))

    def c5(d):
        for p in os.listdir(os.path.join(d, 'engine')):
            fp = os.path.join(d, 'engine', p)
            if os.path.isdir(fp) and p.endswith('_study'):
                shutil.rmtree(fp)
        return not [p for p in os.listdir(os.path.join(d, 'engine')) if p.endswith('_study')]
    results.append(case(5, 'zero study directories [R-ENF-04]', c5, {}, True))

    def c6(d):
        for p in os.listdir(os.path.join(d, 'engine')):
            fp = os.path.join(d, 'engine', p)
            if os.path.isdir(fp) and p.endswith('_study'):
                json.dump({'central': 1.0}, open(os.path.join(fp, 'study_numbers.json'), 'w'))
        return all('beta' not in open(os.path.join(d, 'engine', p, 'study_numbers.json')).read()
                   for p in os.listdir(os.path.join(d, 'engine')) if p.endswith('_study'))
    results.append(case(6, 'directories present, zero beta records read [R-ENF-04]', c6, {}, True))

    def c7(d):
        sd = plant(d, 'CLEAN7', flat(), doc_text=QUOTED,
                   table_cells=['How the slope is measured', 'lead-lag sum',
                                'The estimate is a lead-lag sum beta: one lag, the '
                                'contemporaneous return and one lead, summed.'])
        from docx import Document
        doc = Document(os.path.join(sd, 'CLEAN7_Valuation_Study_18-09-2026.docx'))
        return any('lead-lag sum' in c.text for t in doc.tables for r in t.rows for c in r.cells)
    results.append(case(7, 'the estimator named in a TABLE CELL — the exemplar\'s own shape',
                        c7, {}, False))

    def c8(d):
        sd = plant(d, 'CLEAN8', flat(), doc_text=UNQUOTED)
        from docx import Document
        t = "\n".join(p.text for p in Document(
            os.path.join(sd, 'CLEAN8_Valuation_Study_18-09-2026.docx')).paragraphs)
        return 'standard error' not in t.lower()
    results.append(case(8, 'a Dimson study quoting no testable diagnostic', c8, {}, False))

    def c9(d):
        sd = plant(d, 'CLEAN9', flat(dimson=False))
        return json.load(open(os.path.join(sd, 'study_numbers.json')))['wacc']['beta_record']['dimson'] is False
    results.append(case(9, 'a NON-Dimson record is out of scope', c9, {}, False))

    def c10(d):
        sd = plant(d, 'CLEAN10', flat(), doc=False)
        return not [f for f in os.listdir(sd) if f.endswith('.docx')]
    results.append(case(10, 'a beta record with no delivered document', c10, {}, False))

    assert len(results) == EXPECTED_CASES, (
        'the control declares %d cases and ran %d — a control that quietly loses cases '
        'reports clean' % (EXPECTED_CASES, len(results)))
    red, clean = results[:6], results[6:]
    print('\n%d/%d red conditions caught, %d/%d clean cases passed'
          % (sum(red), len(red), sum(clean), len(clean)))
    return 0 if all(results) else 1


if __name__ == '__main__':
    sys.exit(main())
