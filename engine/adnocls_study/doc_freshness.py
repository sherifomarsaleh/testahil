"""Do the delivered documents actually carry the delivered numbers?

recalc.py ties the workbook to study_numbers.json cell by cell. Nothing tied the Word
documents to it at all, so a study rebuilt from a stale numbers file would pass the
vocabulary scrub, the table-width check, the figure check and the label gate while
quoting a fair value the model no longer produces. That is exactly the failure the
beta rebuild could have shipped.

Three assertions, and the distinction between the second and third is the whole point.
Every headline figure the model currently produces must appear in the rendered text —
that proves the rebuild ran. Every figure of the ALTERNATIVE construction must also
appear — the study publishes both legs and dropping one would be a silent retreat from
the dual framing. Only the FRAMING the rebuild replaced is banned, never a number: the
alternative leg's cost of capital and terminal share look exactly like the superseded
edition's, because on that leg they still are its numbers.
"""
import os, re, sys, json, subprocess

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

# The alternative construction is PUBLISHED, not superseded, so its figures must be
# present. Only the framing the rebuild replaced is banned. Getting this distinction
# wrong is how a freshness check starts failing correct documents: 7.31% and an 84%
# terminal share are not stale numbers, they are the alternative leg's own numbers and
# the study is required to carry them.
ALTERNATIVE = [
    ('the alternative beta', f"{D['inputs']['beta_composite']['value']:.3f}"),
    ('the alternative cost of capital',
     f"{D['dcf_beta_alt']['wacc'] * 100:.2f}%"),
    ('the alternative terminal share',
     f"{D['dcf_beta_alt']['tv_share'] * 100:.0f}% of enterprise value"),
]
# Framing the rebuild replaced. A sentence carrying one of these has not been reached,
# however clean everything else looks.
# Regexes, not substrings, and the reason is a bug this check produced on itself:
# 'beta of 1.0' matches the PREFIX of 'beta of 1.085', so a plain substring test failed
# the document for containing the very figure it is supposed to contain. Every pattern
# here ends on a boundary.
SUPERSEDED = [
    ('asset-risk beta wording', r'asset-risk beta'),
    ('asset beta wording', r'asset beta'),
    ('beta-of-one wording', r'beta of one\b'),
    ('beta-of-1.0 wording', r'beta of 1\.0(?!\d)'),
    ('beta-of-1 wording', r'beta of 1(?![\d.])'),
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
print('the alternative construction is carried, not dropped')
for label, needle in ALTERNATIVE:
    hit = needle in t
    print(f'  {"OK  " if hit else "MISS"}  {label:<32} {needle}')
    if not hit:
        fails.append(f'{label} ({needle}) missing — the alternative leg must be published')

print('=' * 74)
print('no superseded framing survives in the text')
for label, needle in SUPERSEDED:
    n = len(re.findall(needle, t))
    print(f'  {"OK  " if n == 0 else "FAIL"}  {label:<32} {needle!r} appears {n}x')
    if n:
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
      f'{len(ALTERNATIVE)} alternative-construction figures carried, '
      f'{len(SUPERSEDED)} superseded phrasings absent')
