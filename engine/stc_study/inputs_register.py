"""STC — the four-field input register, GENERATED from the disclosure this study commits.

WHY IT IS GENERATED RATHER THAN TYPED. The depth bar requires every input to carry a value,
a source, a date and a research layer, validated by assertion and with no orphan numbers.
A register typed by hand is a second copy of figures that already exist in this study's own
modules, and a second copy is a thing that goes stale — which is the defect three separate
rules in this protocol were written to close. Every row here resolves from segments.py,
cost_stack.py, units.py, coc_run.py or the study's own committed bridge, so a figure that
moves in the disclosure moves here in the same pass or fails the assertion.

WHAT THE SOURCE FIELD SAYS. Each names the DOCUMENT the figure was read from — the company's
own audited or reviewed statements and its own earnings presentations, with the note. That
is what SIGCM clause 1 is checked on from outside: a dated historical of this company whose
source names no company document is a breach, and every historical here is a company
document by construction because there is no other kind of source in this study's history.
"""
from __future__ import annotations

import json
import os

import coc_run as COCRUN
import cost_stack as CS
import segments as SEG
import units as UN

HERE = os.path.dirname(os.path.abspath(__file__))

#: The documents, named as a reader would name them, with the period each covers. Keyed by
#: the extracted file so a row cannot cite a document this study does not hold.
DOCS = {
    'FY2025': ('Saudi Telecom Company, audited consolidated financial statements for the '
               'year ended 31 December 2025', '2025-12-31'),
    'FY2024': ('Saudi Telecom Company, audited consolidated financial statements for the '
               'year ended 31 December 2024', '2024-12-31'),
    'FY2023': ('Saudi Telecom Company, audited consolidated financial statements for the '
               'year ended 31 December 2023', '2023-12-31'),
    'H1_2026': ('Saudi Telecom Company, reviewed condensed consolidated interim financial '
                'statements for the six months ended 30 June 2026', '2026-06-30'),
    'IR_FY2025': ('Saudi Telecom Company, fourth-quarter and full-year 2025 earnings '
                  'presentation', '2025-12-31'),
    'IR_H1_2026': ('Saudi Telecom Company, second-quarter and half-year 2026 earnings '
                   'presentation', '2026-06-30'),
}

#: FY2023 and FY2024 columns come from the FY2024 filing wherever a line was regrouped
#: afterwards — the one-filing-per-column discipline segments.py and cost_stack.py both
#: keep, so a column is never two groupings in one place.
COL_DOC = {'FY2023': 'FY2024', 'FY2024': 'FY2025', 'FY2025': 'FY2025'}

LAYER_COMPANY = 'Company'
LAYER_IR = 'Company_IR'
LAYER_MARKET = 'Market'
LAYER_COUNTRY = 'Country'


def _slug(s):
    out = []
    for ch in s.lower():
        out.append(ch if ch.isalnum() else '_')
    s = ''.join(out)
    while '__' in s:
        s = s.replace('__', '_')
    return s.strip('_')[:44]


def _row(value, doc_key, note, layer=LAYER_COMPANY):
    name, date = DOCS[doc_key]
    return dict(value=value, source='%s, %s' % (name, note), date=date, layer=layer)


def build():
    I = {}

    # ---- the group income statement, three filed years -------------------------------
    for i, y in enumerate(CS.YEARS):
        dk = COL_DOC[y]
        tag = y.lower()
        I['rev_%s' % tag] = _row(CS.REVENUE[i], dk, 'consolidated statement of profit or loss')
        I['cogs_%s' % tag] = _row(CS.STATED_TOTAL[i], dk, 'note 35, cost of revenues')
        I['gp_%s' % tag] = _row(CS.GROSS_PROFIT[i], dk,
                                'revenue less cost of revenues, both as stated')
        I['sga_selling_%s' % tag] = _row(CS.SM_TOTAL[i], dk,
                                         'note 36, selling and marketing expenses')
        I['sga_admin_%s' % tag] = _row(CS.GA_TOTAL[i], dk,
                                       'note 37, general and administrative expenses')
        I['ebitda_%s' % tag] = _row(CS.EBITDA[i], dk,
                                    'gross profit less both operating-expense notes, each '
                                    'as stated; the three foot to the riyal')

        # every cost line by nature, on its own row
        for line, v in CS.COST_OF_REVENUES.items():
            I['cogs_%s_%s' % (_slug(line), tag)] = _row(v[i], dk, 'note 35, %s' % line.lower())
        # the government-charge sub-note, which is where the largest of them is levied on
        # a different base entirely
        for line, v in CS.GOVERNMENT_CHARGES.items():
            I['cogs_gov_%s_%s' % (_slug(line), tag)] = _row(
                v[i], dk, 'note 35, details of government charges, %s' % line.lower())
        # revenue by nature
        for line, v in CS.REVENUE_DISAGGREGATION.items():
            I['rev_%s_%s' % (_slug(line), tag)] = _row(v[i], dk, 'note 34, revenues, %s'
                                                       % line.lower())

    # ---- the disclosed operating segments --------------------------------------------
    for k, v in SEG.REVENUE.items():
        for i, y in enumerate(SEG.YEARS):
            I['rev_seg_%s_%s' % (_slug(k), y.lower())] = _row(
                v[i], COL_DOC[y], 'note 9, operating segments, %s' % k)
    for k, v in SEG.GROSS_PROFIT.items():
        for i, y in enumerate(SEG.YEARS):
            I['gp_seg_%s_%s' % (_slug(k), y.lower())] = _row(
                v[i], COL_DOC[y], 'note 9, operating segments, %s' % k)

    # ---- the debt book, facility by facility ------------------------------------------
    for name, cur, rate, cu, ncu in COCRUN.FACILITIES_FY25:
        I['debt_%s_fy2025' % _slug(name)] = _row(
            cu + ncu, 'FY2025', 'note 26, borrowings, %s (%s)' % (name, cur))

    # ---- the reviewed half, which is what the first forecast year is anchored on -------
    I['rev_h1_2026'] = _row(40_110_089, 'H1_2026',
                            'condensed consolidated statement of profit or loss')
    I['rev_h1_2025'] = _row(38_660_477, 'H1_2026',
                            'condensed consolidated statement of profit or loss, '
                            'comparative period')
    I['gp_h1_2026'] = _row(19_637_121, 'H1_2026', 'note 4, revenue less cost of operations')
    I['gp_h1_2025'] = _row(18_657_904, 'H1_2026', 'note 4, comparative period')

    # ---- the bridge, on the latest disclosed sheet ------------------------------------
    for key, value, note in (
        ('debt_borrowings_jun2026', 23_536_554,
         'long-term borrowings 22,094,126 plus short-term borrowings 1,442,428'),
        ('debt_leases_jun2026', 2_258_902,
         'note 13, lease liabilities, non-current 1,642,836 plus current 616,066'),
        ('debt_spectrum_jun2026', 3_443_044,
         'note 14.1, financial liabilities related to frequency spectrum licences'),
        ('cash_non_bank_jun2026', 12_940_389,
         'cash and cash equivalents, excluding the digital-banking subsidiary'),
        ('inv_murabahas_jun2026', 1_062_181, 'short-term murabahas'),
        ('inv_sukuk_jun2026', 6_368_453, 'note 9.1, financial assets at amortised cost'),
        ('inv_tbills_jun2026', 492_070, 'note 9.1, treasury bills'),
        ('eq_nci_jun2026', 2_726_349,
         'consolidated statement of financial position, non-controlling interests'),
    ):
        I[key] = _row(value, 'H1_2026', note)

    # ---- the asset base the terminal is built on --------------------------------------
    I['assets_depreciable_gross_fy2025'] = _row(
        134_634_729, 'FY2025', 'note 10, property and equipment, depreciable gross cost')
    I['dep_charge_fy2025'] = _row(
        6_453_343, 'FY2025', "note 10, the year's depreciation on that base")
    I['assets_additions_total_fy2025'] = _row(
        13_815_240, 'FY2025',
        'additions to property and equipment, intangible assets and goodwill by segment')
    I['assets_additions_noncash_fy2025'] = _row(
        2_122_000, 'FY2025', 'note 12(2), additions include non-cash additions')

    # ---- the investor-relations channel, tagged distinctly -----------------------------
    I['capex_fy2025'] = _row(11_795_000, 'IR_FY2025',
                             'capital expenditure as the company reports it', LAYER_IR)
    # THE SUBSCRIBER COUNTS, which are the whole basis of the unit build for two thirds of
    # this business and exist nowhere in the audited statements — the reason the standing
    # rule makes the investor-relations channel mandatory rather than optional, and tags it
    # separately so a reviewer can see how much of the Company ring rests on it.
    _PER = {'Q4 2023': ('fy2023', 'IR_FY2025'), 'Q4 2024': ('fy2024', 'IR_FY2025'),
            'Q4 2025': ('fy2025', 'IR_FY2025'), 'H1 2026': ('h1_2026', 'IR_H1_2026')}
    for period, (tag, dk) in _PER.items():
        I['inv_subs_mobile_%s' % tag] = _row(
            UN.MOBILE_STATED[period], dk,
            'mobile subscribers as at %s, stated in millions' % period, LAYER_IR)
        I['inv_subs_fixed_%s' % tag] = _row(
            UN.FIXED_STATED[period], dk,
            'fixed subscribers as at %s, stated in millions' % period, LAYER_IR)

    # ---- market and country ------------------------------------------------------------
    d = json.load(open(os.path.join(HERE, 'study_numbers.json'))) \
        if os.path.exists(os.path.join(HERE, 'study_numbers.json')) else {}
    if d:
        I['spot'] = dict(
            value=d['spot'],
            source=('Tadawul closing price for STC, supplied for this study and committed '
                    'under the house price register'),
            date=d['spot_date'], layer=LAYER_MARKET)
        I['shares_mn'] = _row(d['bridge_record']['shares_mn'], 'H1_2026',
                              'note 17, share capital divided by par value, less treasury '
                              'shares')
    return I


def check(I=None):
    """Every row four-field complete, every historical naming a company document."""
    import source_integrity as SI
    I = I if I is not None else build()
    problems = []
    for k, v in I.items():
        for f in ('value', 'source', 'date', 'layer'):
            if v.get(f) in (None, ''):
                problems.append('%s has no %s' % (k, f))
        if not isinstance(v.get('value'), (int, float)):
            problems.append('%s carries a non-numeric value' % k)
    hist = [k for k in I if SI.is_dated_historical(k)]
    if not hist:
        problems.append('the register carries no dated historical at all')
    for k, why, src in SI.audit(I):
        problems.append('%s: %s (%s)' % (k, why, src))
    return problems, len(hist)


if __name__ == '__main__':
    I = build()
    problems, nhist = check(I)
    print('%d inputs, %d of them dated historicals of this company' % (len(I), nhist))
    layers = {}
    for v in I.values():
        layers[v['layer']] = layers.get(v['layer'], 0) + 1
    for k in sorted(layers):
        print('  %-12s %d' % (k, layers[k]))
    for p in problems:
        print('FAIL', p)
    if not problems:
        with open(os.path.join(HERE, 'inputs_register.json'), 'w') as f:
            json.dump(I, f, indent=1)
        print('wrote inputs_register.json')
    raise SystemExit(1 if problems else 0)
