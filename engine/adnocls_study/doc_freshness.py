"""Do the delivered documents actually carry the delivered numbers?

recalc.py ties the workbook to study_numbers.json cell by cell. Nothing tied the Word
documents to it at all, so a study rebuilt from a stale numbers file would pass the
vocabulary scrub, the table-width check, the figure check and the label gate while
quoting a fair value the model no longer produces. That is exactly the failure the
beta rebuild could have shipped.

This asserts that every headline figure the model produces appears somewhere in the
rendered text of the study, and that the figures it SUPERSEDED do not. Both halves
matter: finding the new number proves the rebuild ran, and not finding the old one
proves nothing was left behind in a sentence the rebuild did not reach.
"""
import os, sys, json, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
STUDY = os.path.join(HERE, 'ADNOCLS_Valuation_Study_09-08-2026_public.pdf')
BIB = os.path.join(HERE, 'ADNOCLS_Bibliography_09-08-2026.pdf')


def text(pdf):
    return subprocess.run(['pdftotext', '-layout', pdf, '-'],
                          capture_output=True, text=True).stdout


def money(x):
    return f'{x:,.2f}'


bf = D['beta_framing']
MUST = [
    ('the adopted beta', f"{D['inputs']['beta']['value']:.3f}"),
    ('the alternative beta', f"{D['inputs']['beta_composite']['value']:.3f}"),
    ('the cash-flow lens', money(D['lenses']['dcf']['base'])),
    ('the alternative cash-flow lens', money(D['lenses']['dcf_beta_alt']['base'])),
    ('the weighted central', money(D['central'])),
    ('the alternative central', money(D['central_beta_alt'])),
    ('the relative lens', money(D['lenses']['relative']['base'])),
    ('the normalised lens', money(D['lenses']['normalized']['base'])),
    ('the book lens', money(D['lenses']['book']['base'])),
    ('the market price', money(D['meta']['spot_aed'])),
    ('the cost of equity', f"{bf['primary']['ke'] * 100:.2f}"),
    ('the cost of capital', f"{D['wacc']['wacc'] * 100:.2f}"),
    ('the terminal-value share', f"{D['dcf']['tv_share'] * 100:.0f}%"),
]

# Figures the model no longer produces. A rebuild that leaves one of these in a
# sentence has not finished, however clean everything else looks.
SUPERSEDED = [
    ('the first edition beta', '0.705', 'appears only as the disclosed alternative'),
    ('the first edition cost of capital', '7.31%', None),
    ('the first edition terminal-value share', '84% of enterprise value', None),
    ('asset-risk beta wording', 'asset-risk beta', None),
    ('asset beta wording', 'asset beta', None),
]

fails = []
t = text(STUDY)
print('=' * 74)
print('the study carries the numbers the model currently produces')
for label, needle in MUST:
    hit = needle in t
    print(f'  {"OK  " if hit else "MISS"}  {label:<32} {needle}')
    if not hit:
        fails.append(f'{label} ({needle}) missing from the study')

print('=' * 74)
print('nothing superseded survives in the text')
for label, needle, allowed in SUPERSEDED:
    n = t.count(needle)
    # 0.705 is legitimately present as the published alternative; everything else is not
    ok = (n > 0) if allowed else (n == 0)
    print(f'  {"OK  " if ok else "FAIL"}  {label:<32} {needle!r} appears {n}x')
    if not ok:
        fails.append(f'{label}: {needle!r} appears {n}x and should not')

print('=' * 74)
print('the bibliography agrees with the same file')
tb = text(BIB)
n_inputs = len(D['inputs'])
for label, needle in [('the input count', str(n_inputs)),
                      ('the adopted beta', f"{D['inputs']['beta']['value']:.3f}"),
                      ('the alternative beta', '0.705')]:
    hit = needle in tb
    print(f'  {"OK  " if hit else "MISS"}  {label:<32} {needle}')
    if not hit:
        fails.append(f'{label} ({needle}) missing from the bibliography')

print('=' * 74)
if fails:
    print('DOCUMENT FRESHNESS FAILED:')
    for f in fails:
        print('  -', f)
    sys.exit(1)
print(f'DOCUMENTS ARE CURRENT — {len(MUST)} headline figures found, '
      f'{len(SUPERSEDED) - 1} superseded figures absent')
