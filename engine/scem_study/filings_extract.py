#!/usr/bin/env python3
"""SCEM — every figure this study needs, taken from the company's OWN audited statements.

WHY THIS FILE EXISTS. The first edition of this study sourced its revenue, profit and
balance-sheet figures from Global Cement, cemnet, Daily News Egypt, Arab Finance and an
aggregator's carry of S&P Global Market Intelligence. SIGCM clause 1 forbids exactly that
and has since July 2026. The audited statements were on the company's own website the whole
time — sinaicement.com carries them as direct PDF links from its homepage, no
authentication and no portal to navigate:

    SCC-AFS-E-1225.pdf   audited, year ended 31 December 2025 (FY2024 comparatives)
    SCC-AFS-E-1224.pdf   audited, year ended 31 December 2024 (FY2023 comparatives)
    SCC-AFS-E-0326.pdf   reviewed, three months ended 31 March 2026

THE ROUTE IS OCR OFF THE RENDERED PIXELS, and it is recorded because [R-FCAL-01] requires
it: these filings carry a 37-byte text layer across 37 pages, so no text extraction is
possible and the figures are read from the page images. ARITHMETIC IS THE ARBITER, NOT THE
EXTRACTOR'S CONFIDENCE — every assertion below is a footing the filing itself performs, and
a misread digit breaks one of them. They all pass.

WHAT THE FILINGS SAY THAT THE FIRST EDITION DID NOT KNOW, all of it understating the
company:

    shareholders' equity, 31-Dec-2025    6,020.3   against   5,240.0 used   (-13.0%)
    cash and bank, 31-Dec-2025           4,762.3   against   3,850.0 used   (-19.2%)
    depreciation and amortisation FY2025   122.6   against     418.1 used   (+241%)
    operating profit FY2025              3,304.1   against an EBIT of 2,640 (-20.1%)

and a reviewed 31 March 2026 balance sheet carrying EGP 5,802.0mn of cash, EGP 152.7mn of
lease liabilities and no bank debt at all, under a single quarter's profit of EGP 1,114.5mn
against a full prior year of 2,284.5mn.

Figures are EGP unless a key says otherwise. Every one carries its statement, its printed
page and its route.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

SOURCE = {
    'FY2025': {'file': 'filings/SCC-AFS-E-1225.pdf', 'kind': 'audited',
               'period_end': '2025-12-31', 'auditor': 'Medhat Ghaly / Albert Edward',
               'route': 'OCR off the rendered pixels; the filing carries a 37-byte text '
                        'layer across 37 pages'},
    'FY2024': {'file': 'filings/SCC-AFS-E-1224.pdf', 'kind': 'audited',
               'period_end': '2024-12-31', 'auditor': 'Medhat Ghaly / Albert Edward',
               'route': 'OCR off the rendered pixels'},
    'Q1_2026': {'file': 'filings/SCC-AFS-E-0326.pdf', 'kind': 'reviewed',
                'period_end': '2026-03-31', 'auditor': 'Medhat Ghaly, report dated '
                                                       '11 May 2026',
                'route': 'OCR off the rendered pixels'},
}

# ---------------------------------------------------------------------------
# INCOME STATEMENT — audited FY2025 (page 3), FY2024 (page 3 of its own filing),
# FY2023 as the comparative column of the FY2024 filing, and the reviewed quarter.
# ---------------------------------------------------------------------------
IS = {
    'FY2023': dict(sales=4285470153, cogs=3364587755, gross=920882398,
                   selling=556987405, ga=162657891, finance=275591963,
                   provisions=4910710, total_expenses=1000147969,
                   operating=-79265571, pbt=-110108976, pat=-117581612, eps=-0.88,
                   page='FY2024 filing, page 3, comparative column'),
    'FY2024': dict(sales=6428011851, cogs=3775018888, gross=2652992963,
                   selling=765354606, ga=355437994, finance=194386055,
                   provisions=37487827, total_expenses=1352666482,
                   operating=1300326481, pbt=3150036485, pat=3072361811, eps=23.09,
                   page='FY2024 filing, page 3'),
    'FY2025': dict(sales=9089149688, cogs=4632038855, gross=4457110833,
                   selling=791121463, ga=361535405, finance=28517057,
                   provisions=-28192283, total_expenses=1152981642,
                   operating=3304129191, pbt=3358865272, pat=2284539004, eps=10.29,
                   page='FY2025 filing, page 3'),
    'Q1_2026': dict(sales=2135463626, cogs=969246686, gross=1166216940,
                    selling=184954169, ga=99574502, finance=3075771,
                    provisions=35224391, total_expenses=322828833,
                    operating=843388107, pbt=1531029452, pat=1114478954, eps=4.27,
                    page='Q1-2026 filing, page 3'),
    'Q1_2025': dict(sales=2016196812, cogs=1115434502, gross=900762310,
                    selling=189852789, ga=62054388, finance=11806633,
                    provisions=32487104, total_expenses=296200914,
                    operating=604561396, pbt=639671508, pat=194252006, eps=1.46,
                    page='Q1-2026 filing, page 3, comparative column'),
}

# ---------------------------------------------------------------------------
# DEPRECIATION AND AMORTISATION — from the cash-flow statement, cross-checked
# against note 4 (fixed assets) and note 5 (right-of-use).
# ---------------------------------------------------------------------------
DNA = {
    'FY2023': dict(depreciation=87210904, amortisation=19023,
                   page='FY2024 filing, page 6, comparative column'),
    'FY2024': dict(depreciation=88786811, amortisation=1963206,
                   page='FY2024 filing, page 6'),
    'FY2025': dict(depreciation=99209674, amortisation=23349222,
                   page='FY2025 filing, page 6; depreciation agrees with note 4 and '
                        'amortisation with note 5'),
}

CAPEX = {
    'FY2023': dict(fixed_assets=43041892, cwip=77785335,
                   page='FY2024 filing, page 6, comparative column'),
    'FY2024': dict(fixed_assets=320960258, cwip=205447467,
                   page='FY2024 filing, page 6'),
    'FY2025': dict(fixed_assets=339330933, cwip=-76933449,
                   page='FY2025 filing, page 6; the construction line is a RELEASE in '
                        'FY2025, CWIP falling from 344.6mn to 267.7mn'),
}

# ---------------------------------------------------------------------------
# BALANCE SHEET
# ---------------------------------------------------------------------------
BS = {
    'FY2024': dict(fixed_assets=1026166835, intangibles=162269152, cwip=344607261,
                   fin_inv_affiliates=25039500, fvoci=65010, deferred_tax_asset=145689339,
                   total_non_current=1703837098,
                   inventories=1049449935, debtors=223320195, due_from_affiliates=4170523,
                   sundry_debtors=77574168, other_debit=599285115, cash=1890505077,
                   cash_blocked=147466100, total_current=3991771113,
                   total_assets=5695608211,
                   capital=1330658670, paid_under_increase=1277466100,
                   legal_reserve=227163603, general_reserve=29359411,
                   retained=-2201209864, profit_for_year=3072361812, equity=3735799732,
                   deferred_tax_liability=0, lease_lt=141240526, total_lt=141240526,
                   due_to_affiliates=0, lease_st=8717155, provisions=121722580,
                   st_loans_affiliates=427905191, suppliers=599922969,
                   other_credit=660300058, total_current_liab=1818567953,
                   total_liabilities=1959808479,
                   page='FY2025 filing, page 2, comparative column'),
    'FY2025': dict(fixed_assets=1265871591, intangibles=138919931, cwip=267673812,
                   fin_inv_affiliates=25039500, fvoci=65010, deferred_tax_asset=0,
                   total_non_current=1697569844,
                   inventories=876191093, debtors=243390012, due_from_affiliates=7806,
                   sundry_debtors=137574616, other_debit=577635635, cash=4762348666,
                   cash_blocked=0, total_current=6597147828,
                   total_assets=8294717672,
                   capital=2608124770, paid_under_increase=0,
                   legal_reserve=227163603, general_reserve=29359411,
                   retained=871151948, profit_for_year=2284539004, equity=6020338736,
                   deferred_tax_liability=126684552, lease_lt=111742265,
                   total_lt=238426817,
                   due_to_affiliates=20772778, lease_st=25823623, provisions=102403549,
                   st_loans_affiliates=0, suppliers=652572902,
                   other_credit=1234379267, total_current_liab=2035952119,
                   total_liabilities=2274378936,
                   page='FY2025 filing, page 2'),
    'Q1_2026': dict(fixed_assets=1238709175, intangibles=133082625, cwip=517594972,
                    fin_inv_affiliates=25039500, fvoci=65010, deferred_tax_asset=0,
                    total_non_current=1914491282,
                    inventories=1010545613, debtors=86358603, due_from_affiliates=7806,
                    sundry_debtors=373407065, other_debit=463766965, cash=5801981716,
                    cash_blocked=0, total_current=7736067768,
                    total_assets=9650559050,
                    capital=2608124770, paid_under_increase=0,
                    legal_reserve=227163603, general_reserve=29359411,
                    retained=3155690951, profit_for_year=1114478954, equity=7134817689,
                    deferred_tax_liability=295514623, lease_lt=137620919,
                    total_lt=433135542,
                    due_to_affiliates=27953288, lease_st=15089045, provisions=102559424,
                    st_loans_affiliates=0, suppliers=458406613,
                    other_credit=1478597449, total_current_liab=2082605819,
                    total_liabilities=2515741361,
                    page='Q1-2026 filing, page 2'),
}

# ---------------------------------------------------------------------------
# NOTE 4 — FIXED ASSETS BY CLASS, and NOTE 3/2 — THE DISCLOSED DEPRECIATION RATES.
# The rates are what [R-TERM-01] needs and what a house guess may not replace.
# ---------------------------------------------------------------------------
FIXED_ASSETS_FY2025 = {
    'buildings_utilities': dict(cost=834757411, acc_dep=298821711, dep_year=19398364,
                                rate_low=0.02, rate_high=0.025),
    'machinery_equipment': dict(cost=2182615926, acc_dep=1492350013, dep_year=73240388,
                                rate_low=0.05, rate_high=0.05),
    'motor_vehicles': dict(cost=37425653, acc_dep=23542358, dep_year=1023883,
                           rate_low=0.20, rate_high=0.20),
    'tools': dict(cost=42816197, acc_dep=34819519, dep_year=1138979,
                  rate_low=0.20, rate_high=0.20),
    'furniture_office': dict(cost=43239967, acc_dep=25449962, dep_year=4408060,
                             rate_low=0.10, rate_high=0.25),
}
FIXED_ASSETS_TOTALS = dict(cost=3140855154, acc_dep=1874983563, dep_year=99209674,
                           nbv=1265871591, fully_depreciated_in_use=379375977)

DISCLOSED_LIVES_NOTE = (
    "Note 3/2, Fixed assets and depreciation, audited statements for the year ended "
    "31 December 2025, printed page 8: 'Depreciation is calculated on the basis of the "
    "straight-line method ... based on the estimated useful life of fixed assets and "
    "consistent with preceeding year, at the following rates: Buildings & Utilities "
    "2% - 2.5%; Machinery 5%; Motor Vehicles 20%; Tools 20%; Furniture & Office equipment "
    "10%-25%.' The FY2024 filing carries the identical table at printed page 9, which is "
    "the cross-check [R-TERM-01] requires."
)

CORPORATE = dict(
    term_note="Note 1, Activities: 'The company's term is twenty-five years, ending on "
              "4/9/2032'. A disclosed finite term on a company valued as a perpetuity, "
              "recorded because it is disclosed; Egyptian company terms are routinely "
              "extended and no non-renewal is disclosed.",
    par_value=10.0,
    shares_from_capital=None,   # filled by the assertions below
)


# ---------------------------------------------------------------------------
# NOTES 24, 25 AND 26 — THE COST STACK AT THE FINEST SOURCED LEVEL. This is what
# SIGCM clause 2 asks for and what the first edition built from assumption instead:
# its per-tonne stack over-charged FY2025 by EGP 357mn against these lines, and the
# check that should have caught it compared the stack to a figure SOLVED FROM THE
# SAME PRESS FIGURES, so two wrong numbers agreed to 1.36%.
# ---------------------------------------------------------------------------
COGS_NOTE24 = {
    'FY2025': dict(raw_fuel_power_packing=3592466202, wages=98744488,
                   clay_resource_fees=115806935, various_supplies=21792821,
                   stationery=1340705, maintenance=306304604, public_relations=145217,
                   travel=551000, government_fees=1376421, insurance=31689328,
                   consultancy=2860565, transfer_loading=5614378,
                   cleaning_security_customs=13764899, accommodation_services=52947253,
                   subcontractor=151945693, rents=101566242, donations=367136,
                   industrial_depreciation=94083975, intangible_amortisation=19023,
                   total=4593386885, change_in_inventory=38651970, net=4632038855,
                   page='FY2025 filing, note 24, printed page 23'),
    'FY2024': dict(raw_fuel_power_packing=3031229986, wages=69084467,        # the footing assertion located this digit: read as 457, filed as 467
                   clay_resource_fees=98752335, various_supplies=18797577,
                   stationery=713271, maintenance=217728745, public_relations=148360,
                   travel=352579, government_fees=4617943, insurance=22996332,
                   consultancy=1434534, transfer_loading=5090262,
                   cleaning_security_customs=10983180, accommodation_services=40327893,
                   subcontractor=104578702, rents=53786444, donations=0,
                   industrial_depreciation=84045872, intangible_amortisation=19023,
                   total=3764687505, change_in_inventory=10331383, net=3775018888,
                   page='FY2025 filing, note 24, comparative column'),
}

SELLING_NOTE25 = {
    'FY2025': dict(wages=19262013, transport_and_loading=579219496, stationery=29838,
                   maintenance=57943, public_relations=1994646, travel=634830,
                   government_fees=656171, cleaning_gratuities=106665,
                   export_and_quality_mark=185690219, rents=1552790, donations=219930,
                   electricity_fuel=291448, accommodation=5750, consultancy=1399724,
                   total=791121463, page='FY2025 filing, note 25, printed page 24'),
    'FY2024': dict(wages=12841119, transport_and_loading=499269967, stationery=763,
                   maintenance=318351, public_relations=12391825, travel=513589,
                   government_fees=404890, cleaning_gratuities=479735,
                   export_and_quality_mark=232605937, rents=5450013, donations=55201,
                   electricity_fuel=108477, accommodation=60500, consultancy=854239,
                   total=765354606, page='FY2025 filing, note 25, comparative column'),
}

GA_NOTE26 = {
    'FY2025': dict(wages=112952031, board=10993242, electricity_gas_fuel=1503465,
                   stationery=1392363, maintenance=6011356, advertising=3535923,
                   travel=4452930, government_fees=20275125, insurance=10306977,
                   consultancy=17187504, cleaning=9528110, accommodation=1424293,
                   technical_assistance=92559282, rents=7939110, donations=706866,
                   solidarity=23196592, real_estate_tax=0, security=612062,
                   tax_inspection_variance=8502276, non_industrial_depreciation=5125699,
                   intangible_depreciation=23330199, total=361535405,
                   page='FY2025 filing, note 26, printed page 25'),
    'FY2024': dict(wages=92587705, board=10797648, electricity_gas_fuel=964580,
                   stationery=465628, maintenance=2982589, advertising=2790290,
                   travel=3796290, government_fees=14149601, insurance=12785968,
                   consultancy=46073960, cleaning=10327484, accommodation=10332755,
                   technical_assistance=87296694, rents=27085244, donations=1168562,
                   solidarity=20728288, real_estate_tax=7110, security=0,
                   tax_inspection_variance=4412476, non_industrial_depreciation=4740939,
                   intangible_depreciation=1944183, total=355437994,
                   page='FY2025 filing, note 26, comparative column'),
}

# NOTE 27 — the EPS working, which STATES the weighted-average count and the dates.
EPS_NOTE27 = dict(
    pre_increase_shares=133065867, post_increase_shares=260812477,
    increase_shares=127746610, par_value=10.0,
    registered='2025-04-22, in the commercial registry',
    first_period_days=111, second_period_days=254, days_in_year=365,
    first_period_profit=327695435, second_period_profit=1956843569,
    page='FY2025 filing, note 27, printed page 25',
    text='"The company increased its number of issued shares from 133,065,867 shares to '
         '260,812,477 shares, representing an increase of 127,746,610 shares, with a par '
         'value of EGP 10 per share, as a result of a public offering to existing '
         'shareholders."')


def _foots(name, parts, total, tol=1.0):
    got = sum(parts)
    assert abs(got - total) <= tol, (
        '%s does not foot: the printed rows give %.0f against a printed %.0f — a misread '
        'digit, since the filing foots' % (name, got, total))


def verify():
    """Every footing the filings themselves perform. A misread digit breaks one."""
    for y, d in IS.items():
        _foots('%s gross profit' % y, [d['sales'], -d['cogs']], d['gross'])
        _foots('%s total expenses' % y,
               [d['selling'], d['ga'], d['finance'], d['provisions']], d['total_expenses'])
        _foots('%s operating profit' % y, [d['gross'], -d['total_expenses']], d['operating'])
    for y, d in BS.items():
        _foots('%s total assets' % y, [d['total_non_current'], d['total_current']],
               d['total_assets'])
        _foots('%s equity' % y, [d['capital'], d['paid_under_increase'], d['legal_reserve'],
                                 d['general_reserve'], d['retained'], d['profit_for_year']],
               d['equity'], tol=2.0)
        _foots('%s total liabilities' % y, [d['total_lt'], d['total_current_liab']],
               d['total_liabilities'])
        _foots('%s balance sheet' % y, [d['total_liabilities'], d['equity']],
               d['total_assets'], tol=2.0)
    _foots('note 4 gross cost',
           [v['cost'] for v in FIXED_ASSETS_FY2025.values()], FIXED_ASSETS_TOTALS['cost'])
    _foots('note 4 accumulated depreciation',
           [v['acc_dep'] for v in FIXED_ASSETS_FY2025.values()],
           FIXED_ASSETS_TOTALS['acc_dep'])
    _foots('note 4 charge for the year',
           [v['dep_year'] for v in FIXED_ASSETS_FY2025.values()],
           FIXED_ASSETS_TOTALS['dep_year'])
    _foots('note 4 net book value',
           [FIXED_ASSETS_TOTALS['cost'], -FIXED_ASSETS_TOTALS['acc_dep']],
           FIXED_ASSETS_TOTALS['nbv'])
    # THE COST NOTES FOOT TO THEIR OWN TOTALS AND THOSE TOTALS ARE THE FACE OF THE P&L
    for y in COGS_NOTE24:
        d = dict(COGS_NOTE24[y])
        tot, chg, net = d.pop('total'), d.pop('change_in_inventory'), d.pop('net')
        d.pop('page')
        _foots('%s note 24' % y, list(d.values()), tot, tol=2.0)
        _foots('%s note 24 net' % y, [tot, chg], net)
        assert net == IS[y]['cogs'], 'note 24 does not agree with the face of the P&L'
    for y in SELLING_NOTE25:
        d = dict(SELLING_NOTE25[y]); tot = d.pop('total'); d.pop('page')
        _foots('%s note 25' % y, list(d.values()), tot, tol=2.0)
        assert tot == IS[y]['selling'], 'note 25 does not agree with the face of the P&L'
    for y in GA_NOTE26:
        d = dict(GA_NOTE26[y]); tot = d.pop('total'); d.pop('page')
        _foots('%s note 26' % y, list(d.values()), tot, tol=2.0)
        assert tot == IS[y]['ga'], 'note 26 does not agree with the face of the P&L'
    # AND THE THREE ROUTES TO DEPRECIATION AGREE, which is the strongest check available:
    # the cash-flow statement, note 4 plus note 5, and the cost notes' own charges.
    via_notes = (COGS_NOTE24['FY2025']['industrial_depreciation']
                 + COGS_NOTE24['FY2025']['intangible_amortisation']
                 + GA_NOTE26['FY2025']['non_industrial_depreciation']
                 + GA_NOTE26['FY2025']['intangible_depreciation'])
    via_cf = DNA['FY2025']['depreciation'] + DNA['FY2025']['amortisation']
    assert via_notes == via_cf, (
        'the cost notes charge %d of depreciation and the cash-flow statement adds back '
        '%d' % (via_notes, via_cf))
    # THE FILING STATES ITS OWN WEIGHTED-AVERAGE EPS WORKING, so it is reproduced
    e = EPS_NOTE27
    wavg = (e['pre_increase_shares'] * e['first_period_days'] / e['days_in_year']
            + e['post_increase_shares'] * e['second_period_days'] / e['days_in_year'])
    assert abs(IS['FY2025']['pat'] / wavg - IS['FY2025']['eps']) < 0.01, \
        "note 27's own EPS working does not reproduce"
    _foots('note 27 profit split',
           [e['first_period_profit'], e['second_period_profit']], IS['FY2025']['pat'],
           tol=2.0)
    assert (e['post_increase_shares'] - e['pre_increase_shares']
            == e['increase_shares']), 'note 27 share increase does not foot'
    # the cash-flow charge IS note 4's charge, which ties two statements together
    assert DNA['FY2025']['depreciation'] == FIXED_ASSETS_TOTALS['dep_year'], (
        'the cash-flow depreciation and note 4 disagree')
    # THE SHARE COUNT IS FOOTED OR IT IS NOT RECORDED [R-FCAL-01]: issued capital over par
    n = BS['FY2025']['capital'] / CORPORATE['par_value']
    assert abs(n - 260812477.0) < 1.0, 'the share count does not foot against issued capital'
    CORPORATE['shares_from_capital'] = n / 1e6
    # THE CLOSING COUNT REPRODUCES THE QUARTER'S EPS AND NOT THE YEAR'S, AND THAT IS THE
    # CAPITAL INCREASE RATHER THAN A MISREAD. This assertion fired on its first run and it
    # was right to: FY2025 profit over the closing count gives 8.76 against a printed
    # 10.29, because EPS is struck on the WEIGHTED-AVERAGE count and 2025 is the year the
    # EGP 1,277,466,100 paid under capital increase converted into capital. FY2024's EPS
    # reproduces exactly on the PRE-INCREASE count of 133.07mn, and Q1-2026's on the
    # closing count, which is what makes the reading unambiguous. This is [R-FCAL-01]'s
    # own warning arriving in practice: a count changes on a capital increase and today's
    # count is never carried back.
    assert abs(IS['Q1_2026']['pat'] / n - IS['Q1_2026']['eps']) < 0.02, \
        'Q1-2026 EPS does not reproduce from the footed closing share count'
    pre = BS['FY2024']['capital'] / CORPORATE['par_value']
    assert abs(IS['FY2024']['pat'] / pre - IS['FY2024']['eps']) < 0.02, \
        'FY2024 EPS does not reproduce from the pre-increase share count'
    CORPORATE['shares_pre_increase'] = pre / 1e6
    CORPORATE['shares_wavg_fy2025'] = (IS['FY2025']['pat'] / IS['FY2025']['eps']) / 1e6
    CORPORATE['shares_note'] = (
        'Issued capital of EGP 2,608,124,770 over a par of EGP 10 gives 260,812,477 shares '
        'at 31-Dec-2025 and at 31-Mar-2026, and that count reproduces the reviewed '
        "quarter's printed EPS of 4.27. FY2025's printed EPS of 10.29 is struck on a "
        'weighted-average count of about 222.0mn, because the EGP 1,277,466,100 paid under '
        'capital increase converted during the year; FY2024 EPS of 23.09 reproduces '
        'exactly on the pre-increase 133,065,867. The count used for value per share is '
        'the CLOSING one.')
    return True


def derived():
    """What the filings imply, computed rather than typed."""
    out = {}
    for y in ('FY2023', 'FY2024', 'FY2025'):
        d, dn = IS[y], DNA[y]
        dna = dn['depreciation'] + dn['amortisation']
        out[y] = dict(
            dna=dna / 1e6,
            # finance expense sits INSIDE this filing's operating line, so EBIT adds it back
            ebit=(d['operating'] + d['finance']) / 1e6,
            ebitda=(d['operating'] + d['finance'] + dna) / 1e6,
            gross_margin=d['gross'] / d['sales'],
            ebitda_margin=(d['operating'] + d['finance'] + dna) / d['sales'],
            capex=(CAPEX[y]['fixed_assets'] + CAPEX[y]['cwip']) / 1e6,
        )
    for y in ('Q1_2025', 'Q1_2026'):
        d = IS[y]
        out[y] = dict(gross_margin=d['gross'] / d['sales'],
                      ebit=(d['operating'] + d['finance']) / 1e6)
    q = BS['Q1_2026']
    out['latest_sheet'] = dict(
        date='2026-03-31', kind='reviewed',
        cash=q['cash'] / 1e6,
        interest_bearing_debt=(q['lease_lt'] + q['lease_st']) / 1e6,
        net_cash=(q['cash'] - q['lease_lt'] - q['lease_st']) / 1e6,
        equity=q['equity'] / 1e6,
        note='the company carries NO bank borrowings at either date; the whole of its '
             'interest-bearing debt is lease liabilities under EAS 49')
    # the weighted disclosed life, on the company's own gross-cost mix
    lives, cost = 0.0, 0.0
    for k, v in FIXED_ASSETS_FY2025.items():
        rate = (v['rate_low'] + v['rate_high']) / 2.0
        lives += v['cost'] * (1.0 / rate)
        cost += v['cost']
    out['weighted_disclosed_life_years'] = lives / cost
    out['machinery_life_years'] = 1.0 / FIXED_ASSETS_FY2025['machinery_equipment']['rate_low']
    out['capex_to_book_dna_fy25'] = out['FY2025']['capex'] / out['FY2025']['dna']
    return out


if __name__ == '__main__':
    verify()
    d = derived()
    json.dump({'source': SOURCE, 'income_statement': IS, 'dna': DNA, 'capex': CAPEX,
               'balance_sheet': BS, 'fixed_assets_fy2025': FIXED_ASSETS_FY2025,
               'fixed_assets_totals': FIXED_ASSETS_TOTALS,
               'disclosed_lives_note': DISCLOSED_LIVES_NOTE, 'corporate': CORPORATE,
               'derived': d},
              open(os.path.join(HERE, 'filings_extract.json'), 'w'), indent=1)
    print('every footing the filings perform: PASSED')
    for y in ('FY2023', 'FY2024', 'FY2025'):
        print('  %s  revenue %9.1f  EBITDA %8.1f (%5.1f%%)  D&A %6.1f  capex %6.1f  '
              'PAT %8.1f' % (y, IS[y]['sales'] / 1e6, d[y]['ebitda'],
                             d[y]['ebitda_margin'] * 100, d[y]['dna'], d[y]['capex'],
                             IS[y]['pat'] / 1e6))
    print('  Q1-2026 gross margin %.2f%% against FY2025 %.2f%% and Q1-2025 %.2f%%'
          % (d['Q1_2026']['gross_margin'] * 100, d['FY2025']['gross_margin'] * 100,
             d['Q1_2025']['gross_margin'] * 100))
    print('  latest reviewed sheet 31-Mar-2026: cash %.1f, lease debt %.1f, net cash %.1f, '
          'equity %.1f' % (d['latest_sheet']['cash'],
                           d['latest_sheet']['interest_bearing_debt'],
                           d['latest_sheet']['net_cash'], d['latest_sheet']['equity']))
    print('  disclosed lives: machinery %.0f years; weighted on the gross-cost mix %.1f'
          % (d['machinery_life_years'], d['weighted_disclosed_life_years']))
    print('  FY2025 capex is %.2fx book depreciation' % d['capex_to_book_dna_fy25'])
