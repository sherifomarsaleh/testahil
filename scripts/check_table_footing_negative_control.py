#!/usr/bin/env python3
"""The footing gate must go RED on the defects that provoked it, and GREEN on legitimate
constructions that resemble them. A check nobody has seen fail is not evidence.

Every failing case is one of the three ARCC tables EXACTLY AS IT SHIPPED on the morning of
03-Sep-2026, plus the shapes the gate must not be fooled by. Every clean case is a real
construction from the book that must NOT fire — including two that fired against this
instrument's own first draft and were what taught it how tables actually roll up.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import table_footing as TF                                              # noqa: E402

FAIL_CASES = [
    ('ARCC Table 3 as shipped — provisions deducted in the model, absent from the page',
     [['EGP per tonne of cement', 'FY2025A'],
      ['Materials and fuel', '5,698'],
      ['Transportation', '764'],
      ['Overheads and administration', '1,021'],
      ['Total cash cost', '1,542'],
      ['Blended realised price', '2,565'],
      ['EBITDA (EGP mn)', '4,886']]),
    ('ARCC Table 5 as shipped — four contractual rates under an adopted blend',
     [['Facility', 'Balance (EGP mn)', 'Contractual rate'],
      ['CIB credit facilities', '100', '20.60%'],
      ['National Bank of Egypt / KfW', '146', '5.49%'],
      ['European Bank for Reconstruction and Development', '888', '6.84%'],
      ['Lease liabilities', '1.2', '—'],
      ['Blended cost of debt, adopted', '1,135', '13.36%']]),
    ('ARCC Table 2 as shipped — export cement tonnage printed nowhere',
     [['Physical', 'FY2025'],
      ['Cement sold', '3.553Mt'],
      ['Cement exported  (DRIVER)', '17.7%'],
      ['Local cement', '2.923Mt'],
      ['TOTAL DESPATCHES', '4.854Mt']]),
    ('a total that is simply wrong',
     [['EGP mn', 'FY2025'], ['Revenue', '100'], ['Other income', '20'],
      ['Total income', '130']]),
    ('a weighted average reproducible from no column of its own table',
     [['Facility', 'Balance', 'Rate'], ['A', '100', '5.0%'], ['B', '900', '5.0%'],
      ['Weighted average', '1,000', '9.0%']]),
    ('a subtotal roll-up that does not roll up',
     [['EGP mn', 'FY2025'], ['Current assets', '400'], ['Total current assets', '400'],
      ['Non-current assets', '600'], ['Total non-current assets', '600'],
      ['Total assets', '1,400']]),
]

CLEAN_CASES = [
    ('ARCC Table 3 CORRECTED — the provisions line printed, the stack foots',
     [['The cost stack and the margin it produces', 'FY2025A'],
      ['Materials and fuel (EGP mn)', '5,698'],
      ['Transportation (EGP mn)', '764'],
      ['Overheads and administration (EGP mn)', '1,021'],
      ['Provisions and credit losses (EGP mn)', '78'],
      ['Total cash cost (EGP per tonne of cement)', '1,542'],
      ['Blended realised price (EGP per tonne of cement)', '2,565'],
      ['EBITDA (EGP mn)', '4,886']],
     ['Total cash cost (EGP per tonne of cement)',
      'Blended realised price (EGP per tonne of cement)']),
    ('ARCC Table 5 CORRECTED — both columns weight to the figures shown',
     [['Facility', 'Balance (EGP mn)', 'Contractual rate', 'Pound-equivalent cost'],
      ['CIB credit facilities', '100', '20.60%', '20.60%'],
      ['National Bank of Egypt / KfW', '146', '5.49%', '11.49%'],
      ['European Bank for Reconstruction and Development', '888', '6.84%', '12.84%'],
      ['Lease liabilities', '1.2', '20.60%', '20.60%'],
      ['Weighted average', '1,135', '7.89%', '13.36%']], []),
    ('a balance sheet footing over its SUBTOTALS — the shape that flagged 67 tables '
     'against the first draft, and was this instrument being wrong rather than the book',
     [['EGP mn', 'FY2025'], ['Property, plant and equipment', '600'],
      ['Intangibles', '100'], ['Total non-current assets', '700'],
      ['Inventories', '200'], ['Cash', '100'], ['Total current assets', '300'],
      ['Total assets', '1,000']], []),
    ('a balance sheet footing over its LEAF rows, skipping the intermediate subtotal',
     [['EGP mn', 'FY2025'], ['Property, plant and equipment', '600'],
      ['Total non-current assets', '600'], ['Inventories', '200'], ['Cash', '200'],
      ['Total assets', '1,000']], []),
    ('"Total assets" as the FIRST data row of a summary balance sheet — a DISCLOSED LINE '
     'ITEM among cash, debt and equity, none of which are its components; 34 of these '
     'fired against the first draft',
     [['EGP mn', 'FY2025'], ['Total assets', '8,784'], ['Cash and bank balances', '3,459'],
      ['Interest-bearing debt', '1,135'], ['Equity attributable to owners', '4,643']], []),
    ('a sensitivity grid whose ROW LABEL happens to carry the word "blended"',
     [['Driver (grid)', 'low', 'base', 'high'],
      ['Beta', '22.40', '18.89', '13.89'],
      ['Blended ARPU (x)', '16.00', '18.89', '21.78'],
      ['Subscribers', '17.95', '18.89', '19.83']],
     ['Blended ARPU (x)']),
    ('a rounded stack that foots only inside its own rounding band',
     [['EGP mn', 'FY2025'], ['A', '333.3'], ['B', '333.3'], ['C', '333.3'],
      ['Total', '1,000.0']], []),
]


def run():
    bad = []
    for name, rows in FAIL_CASES:
        n = len(TF.check_table(rows))
        print(f'  [{"RED " if n else "MISS"}] {name}: {n} unreconciled')
        if not n:
            bad.append(f'FAIL CASE DID NOT FIRE: {name}')
    print()
    for name, rows, declared in CLEAN_CASES:
        probs = [p for p in TF.check_table(rows) if p[2] not in declared]
        print(f'  [{"ok  " if not probs else "FIRE"}] {name}: {len(probs)} unreconciled')
        if probs:
            bad.append(f'CLEAN CASE FIRED: {name} -> {[p[2] for p in probs]}')

    # the gate's own refusals
    import subprocess
    g = os.path.join(ROOT, 'scripts', 'check_table_footing.py')
    r = subprocess.run([sys.executable, g, '--measure'], capture_output=True, text=True)
    ok_adv = 'never a bar' in r.stdout.lower()
    print(f'\n  [{"ok  " if ok_adv else "FIRE"}] the advisory names itself as never a bar')
    if not ok_adv:
        bad.append('the advisory does not disclaim itself')

    print()
    for b in bad:
        print('  ' + b)
    total = len(FAIL_CASES) + len(CLEAN_CASES) + 1
    print(f'\nNEGATIVE CONTROL {"OK" if not bad else "FAILED"} — '
          f'{total - len(bad)}/{total} conditions')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(run())
