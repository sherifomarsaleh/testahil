"""MODON (Modon Holding PSC, ADX) — study model. Single source of numbers.

Every figure the workbook, study document and bibliography carry is computed here
and written to study_numbers.json with a four-field input register (value, source,
date, ring) validated by assertion. No financial numeral is typed into a builder.

Perimeter note: FY2024 is a base reset (Modon Properties/ADNEC combination via
share issues of AED 27.4bn + bargain-purchase gain of AED 9,192mn). FY2023 and
FY2022 are the Q Holding perimeter. The forecast base is FY2025, the first clean
full year of the combined group. All AED mn unless stated.

The study's single most consequential contested judgement — whether the FY2025-26
development sales surge persists (base: normalising but sustained launches) or
mean-reverts to backlog run-off — is computed BOTH WAYS and published side by
side, never averaged into one number."""
import json, os, math

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'study_numbers.json')

D = {}
assert_log = []


def A(cond, msg):
    assert cond, msg
    assert_log.append(msg)


# =============================================================================
# INPUT REGISTER — every input four-field complete (value, source, date, ring)
# =============================================================================
INP = {}


def inp(key, value, source, date, ring):
    INP[key] = dict(value=value, source=source, date=date, ring=ring)
    return value


FS25 = ("Audited consolidated financial statements FY2025, Modon Holding PSC, "
        "signed 18-Feb-2026, modon.com investor relations")
FS23 = ("Audited consolidated financial statements FY2023, Q Holding PSC, "
        "modon.com investor relations")
H126 = ("Interim condensed consolidated financial statements, 30-Jun-2026 "
        "(reviewed, unaudited), modon.com investor relations")
AR25 = "Modon Annual Report 2025, modon.com investor relations"
PR25 = "Modon FY2025 results announcement, modon.com media centre, 18-Feb-2026"

# ---- market / meta ----------------------------------------------------------
spot = inp('spot', 2.83, 'Uploaded ADX daily price history, last close', '2026-08-07',
           'Market')
shares_mn = inp('shares_mn', 16347.080, 'Share capital note 23: 16,347,080 thousand '
                'shares of AED 1 each, ' + FS25, '2026-02-18', 'Company')
mktcap = spot * shares_mn
D['meta'] = dict(ticker='MODON', company='Modon Holding PSC', market='ADX',
                 currency='AED', asof='2026-08-09', spot=spot, shares_mn=shares_mn,
                 mktcap=mktcap,
                 klass='diversified city-developer group (development + recurring '
                       'income + hospitality + events platform)')

# ---- historical income statement (as-reported house lines, AED mn) ----------
# FY2023 = Q Holding perimeter. FY2024/FY2025 = Modon perimeter (FY2024 from the
# FY2025 filing's audited comparatives).
rev23 = inp('rev_fy23', 994.293, 'Consolidated statement of profit or loss (revenue '
            'from contracts 473.338 + rental 409.058 + dividends 111.897), ' + FS23,
            '2024-02-15', 'Company')
rev24 = inp('rev_fy24', 6511.182, 'Consolidated statement of profit or loss, FY2024 '
            'comparatives, ' + FS25, '2026-02-18', 'Company')
rev25 = inp('rev_fy25', 13828.869, 'Consolidated statement of profit or loss, ' + FS25,
            '2026-02-18', 'Company')
gp24 = inp('gp_fy24', 2316.507, 'Gross profit, FY2024 comparatives, ' + FS25,
           '2026-02-18', 'Company')
gp25 = inp('gp_fy25', 5025.259, 'Gross profit, ' + FS25, '2026-02-18', 'Company')
# FY2023 P&L is by nature, not function — a gross-profit line does not exist.
# House proxy: revenue less contract costs (the only cost line tied to revenue).
gp23 = inp('gp_fy23_house', 994.293 - 394.734, 'House proxy: revenue less contract '
           'costs 394.734 (P&L by nature carries no gross-profit line), ' + FS23,
           '2024-02-15', 'Company/House')

fin_inc25 = inp('fin_inc_fy25', 262.923, 'Finance income note 9, ' + FS25,
                '2026-02-18', 'Company')
fin_cost25 = inp('fin_cost_fy25', 390.389, 'Finance costs note 10, ' + FS25,
                 '2026-02-18', 'Company')
fin_inc24 = inp('fin_inc_fy24', 126.776, 'Finance income, FY2024 comparatives, ' + FS25,
                '2026-02-18', 'Company')
fin_cost24 = inp('fin_cost_fy24', 283.443, 'Finance costs, FY2024 comparatives, ' + FS25,
                 '2026-02-18', 'Company')
assoc25 = inp('assoc_fy25', 263.592, 'Share of profit from associates and joint '
              'ventures note 17, ' + FS25, '2026-02-18', 'Company')
assoc24 = inp('assoc_fy24', 115.114, 'Share of profit from associates and JVs, FY2024 '
              'comparatives, ' + FS25, '2026-02-18', 'Company')
ebt25 = inp('ebt_fy25', 4421.195, 'Profit before tax incl. discontinued 0.182, ' + FS25,
            '2026-02-18', 'Company')
ebt24 = inp('ebt_fy24', 9488.267, 'Profit before tax incl. discontinued, FY2024 '
            'comparatives, ' + FS25, '2026-02-18', 'Company')
ebt23 = inp('ebt_fy23', 653.455, 'Profit before tax incl. discontinued 4.051, ' + FS23,
            '2024-02-15', 'Company')
tax25 = inp('tax_fy25', 495.490, 'Income tax expense note 11 (incl. DMTT 350.356), '
            + FS25, '2026-02-18', 'Company')
tax24 = inp('tax_fy24', 98.815, 'Income tax expense, FY2024 comparatives, ' + FS25,
            '2026-02-18', 'Company')
tax23 = inp('tax_fy23', 79.504, 'Income tax expense, ' + FS23, '2024-02-15', 'Company')
pat25 = inp('pat_fy25', 3925.705, 'Profit for the year, ' + FS25, '2026-02-18',
            'Company')
pat24 = inp('pat_fy24', 9389.452, 'Profit for the year, FY2024 comparatives, ' + FS25,
            '2026-02-18', 'Company')
pat23 = inp('pat_fy23', 573.951, 'Profit for the year after tax, ' + FS23,
            '2024-02-15', 'Company')
npa25 = inp('npa_fy25', 4020.102, 'Profit attributable to owners of the Parent, '
            + FS25, '2026-02-18', 'Company')
npa24 = inp('npa_fy24', 9423.191, 'Profit attributable to owners, FY2024 comparatives, '
            + FS25, '2026-02-18', 'Company')
npa23 = inp('npa_fy23', 461.269, 'Profit attributable to owners of the Parent, ' + FS23,
            '2024-02-15', 'Company')
bargain24 = inp('bargain_fy24', 9192.243, 'Bargain purchase gain on acquisition of '
                'subsidiaries, note 4.2, FY2024 comparatives, ' + FS25, '2026-02-18',
                'Company')
dna25 = inp('dna_fy25', 468.264 + 76.645 + 65.574, 'Depreciation on PP&E 468.264 + '
            'amortisation 76.645 + right-of-use depreciation 65.574, cash flow '
            'statement adjustments, ' + FS25, '2026-02-18', 'Company')
dna24 = inp('dna_fy24', 193.207 + 46.619 + 25.296, 'Same three lines, FY2024 '
            'comparatives, ' + FS25, '2026-02-18', 'Company')
dna23 = inp('dna_fy23', 20.756 + 3.539 + 3.424, 'Depreciation and amortisation lines, '
            'cash flow statement, ' + FS23, '2024-02-15', 'Company')
ga25 = inp('ga_fy25', 1547.476, 'General and administrative expenses note 7, ' + FS25,
           '2026-02-18', 'Company')
sm25 = inp('sm_fy25', 266.211, 'Selling and marketing expenses, ' + FS25, '2026-02-18',
           'Company')
invinc25 = inp('invinc_fy25', 338.260, 'Investment and other income note 8, ' + FS25,
               '2026-02-18', 'Company')
fvip25 = inp('fv_ip_fy25', 343.426, 'Fair value gain on revaluation of investment '
             'properties note 16, ' + FS25, '2026-02-18', 'Company')
fvpl25 = inp('fv_fvtpl_fy25', 221.952, 'Change in fair value of investments at FVTPL '
             'note 18, ' + FS25, '2026-02-18', 'Company')
dispassoc25 = inp('disp_assoc_fy25', 169.677, 'Gain on disposal of an associate note '
                  '17(ii), ' + FS25, '2026-02-18', 'Company')

# house EBIT/EBITDA (reported basis): EBIT = EBT - net finance income + finance
# costs... defined as EBT excluding net finance result and associate income.
fin_net25 = fin_inc25 - fin_cost25
fin_net24 = fin_inc24 - fin_cost24
fin_net23 = inp('fin_net_fy23', 8.518, 'Finance income (costs), net, note 10, ' + FS23,
                '2024-02-15', 'Company')
assoc23 = inp('assoc_fy23', -0.697, 'Share of loss from associates and JVs, ' + FS23,
              '2024-02-15', 'Company')
ebit25 = ebt25 - fin_net25 - assoc25
ebit24 = ebt24 - fin_net24 - assoc24
ebit23 = ebt23 - fin_net23 - assoc23
ebitda25 = ebit25 + dna25
ebitda24 = ebit24 + dna24
ebitda23 = ebit23 + dna23
A(abs(ebitda25 - 4895.370) < 0.5,
  f'FY2025 house EBITDA {ebitda25:.1f} reconciles to the company adjusted EBITDA '
  f'4,900 within rounding (release: 4.9bn, 35.2% margin)')

# one-off strip for the clean/normalised basis (FY2025)
oneoff25 = fvip25 + fvpl25 + dispassoc25
ebit25_clean = ebit25 - oneoff25
ebitda25_clean = ebit25_clean + dna25
imp24 = inp('impair_fy24', 539.922 + 406.663 + 78.141, 'Impairment of PP&E 539.922 + '
            'development WIP 406.663 + goodwill 78.141, FY2024 comparatives, ' + FS25,
            '2026-02-18', 'Company')
ebit24_ex = ebit24 - bargain24 + imp24 + 212.107   # ex-bargain, ex-impair, ex-IP FV loss
D['hist_is'] = dict(
    FY23=dict(rev=rev23, gp=gp23, ebitda=ebitda23, dna=dna23, ebit=ebit23,
              fin=fin_net23, assoc=assoc23, ebt=ebt23, tax=-tax23, pat=pat23,
              nci=pat23 - npa23, npa=npa23),
    FY24=dict(rev=rev24, gp=gp24, ebitda=ebitda24, dna=dna24, ebit=ebit24,
              fin=fin_net24, assoc=assoc24, ebt=ebt24, tax=-tax24, pat=pat24,
              nci=pat24 - npa24, npa=npa24),
    FY25=dict(rev=rev25, gp=gp25, ebitda=ebitda25, dna=dna25, ebit=ebit25,
              fin=fin_net25, assoc=assoc25, ebt=ebt25, tax=-tax25, pat=pat25,
              nci=pat25 - npa25, npa=npa25),
)
D['oneoff'] = dict(fy25=dict(fv_ip=fvip25, fv_pl=fvpl25, disp=dispassoc25,
                             total=oneoff25, ebit_clean=ebit25_clean,
                             ebitda_clean=ebitda25_clean),
                   fy24=dict(bargain=bargain24, impair=imp24,
                             ebit_ex=ebit24_ex,
                             npa_ex=npa24 - bargain24))

# ---- historical balance sheet (AED mn) --------------------------------------
def bs(key, v, label, src, dt):
    return inp(key, v, label + ', ' + src, dt, 'Company')

# FY2025 / FY2024 from the FY2025 filing (liabilities page OCR cross-checked
# against the H1-2026 interim's audited 31-Dec-2025 comparative column).
ppe25 = bs('ppe_fy25', 8812.397, 'Property, plant and equipment', FS25, '2026-02-18')
ip25 = bs('ip_fy25', 9461.777, 'Investment properties', FS25, '2026-02-18')
intang25 = bs('intang_fy25', 952.423, 'Intangible assets and goodwill', FS25, '2026-02-18')
rou25 = bs('rou_fy25', 530.349, 'Right-of-use assets', FS25, '2026-02-18')
assocbv25 = bs('assoc_bv_fy25', 3723.897, 'Investments in associates and JVs', FS25,
               '2026-02-18')
finass25 = bs('finass_fy25', 339.620 + 54.685, 'Investments in financial assets, '
              'non-current 339.620 + current 54.685', FS25, '2026-02-18')
inv25 = bs('inv_fy25', 27297.588, 'Inventories (land plots 26,610.771 + properties '
           '635.198 + spares 51.619)', FS25, '2026-02-18')
dwip25 = bs('dwip_fy25', 6111.794, 'Development work-in-progress', FS25, '2026-02-18')
recv25 = bs('recv_fy25', 395.103 + 8308.491, 'Trade and other receivables, NC + C',
            FS25, '2026-02-18')
duefr25 = bs('duefr_fy25', 1183.975 + 6747.554, 'Amounts due from related parties, '
             'NC + C (incl. Department of Finance 5,998.151)', FS25, '2026-02-18')
cash25 = bs('cash_fy25', 12641.987, 'Cash and bank balances (incl. escrow 3,311.941 + '
            'restricted 735.174)', FS25, '2026-02-18')
dta25 = bs('dta_fy25', 469.345, 'Deferred tax assets', FS25, '2026-02-18')
assets25 = bs('assets_fy25', 87030.985, 'Total assets', FS25, '2026-02-18')
eqp25 = bs('eqp_fy25', 53902.504, 'Equity attributable to owners of the Parent', FS25,
           '2026-02-18')
nci25 = bs('nci_fy25', 847.480, 'Non-controlling interests', FS25, '2026-02-18')
loans25 = bs('loans_fy25', 5136.373, 'Loans and borrowings, NC 2,943.416 + C 2,192.957, '
             'note 29', FS25, '2026-02-18')
rploan25 = bs('rploan_fy25', 1652.713, 'Loan from a related party, note 30', FS25,
              '2026-02-18')
lease25 = bs('lease_fy25', 556.147 + 67.619, 'Lease liabilities, NC + C', FS25,
             '2026-02-18')
pay25 = bs('pay_fy25', 3427.379 + 17980.495, 'Trade and other payables, NC + C', FS25,
           '2026-02-18')
dueto25 = bs('dueto_fy25', 430.404 + 1263.317, 'Amounts due to related parties, NC + C',
             FS25, '2026-02-18')
taxpay25 = bs('taxpay_fy25', 468.089, 'Income tax payable', FS25, '2026-02-18')
dtl25 = bs('dtl_fy25', 1131.012, 'Deferred tax liabilities', FS25, '2026-02-18')
eosb25 = bs('eosb_fy25', 167.453, "Employees' end of service benefits", FS25, '2026-02-18')
liab25 = bs('liab_fy25', 32281.001, 'Total liabilities', FS25, '2026-02-18')
A(abs((eqp25 + nci25 + liab25) - assets25) < 0.5, 'FY2025 balance sheet foots: equity '
  '+ NCI + liabilities = total assets')
A(abs((loans25 + rploan25 + lease25 + pay25 + dueto25 + taxpay25 + dtl25 + eosb25)
      - liab25) < 0.5, 'FY2025 liability components sum to total liabilities')

ppe24 = bs('ppe_fy24', 7593.191, 'PP&E, FY2024 comparatives', FS25, '2026-02-18')
ip24 = bs('ip_fy24', 9336.725, 'Investment properties, FY2024 comparatives', FS25,
          '2026-02-18')
inv24 = bs('inv_fy24', 29586.274, 'Inventories, FY2024 comparatives', FS25, '2026-02-18')
dwip24 = bs('dwip_fy24', 2461.672, 'Development WIP, FY2024 comparatives', FS25,
            '2026-02-18')
recv24 = bs('recv_fy24', 538.515 + 2990.510, 'Trade and other receivables, FY2024',
            FS25, '2026-02-18')
duefr24 = bs('duefr_fy24', 9314.779, 'Amounts due from related parties, FY2024', FS25,
             '2026-02-18')
cash24 = bs('cash_fy24', 7009.670, 'Cash and bank balances, FY2024', FS25, '2026-02-18')
assets24 = bs('assets_fy24', 75925.281, 'Total assets, FY2024', FS25, '2026-02-18')
eqp24 = bs('eqp_fy24', 49676.408, 'Equity attributable to owners, FY2024', FS25,
           '2026-02-18')
nci24 = bs('nci_fy24', 1186.183, 'Non-controlling interests, FY2024', FS25, '2026-02-18')
loans24 = bs('loans_fy24', 3711.397, 'Loans and borrowings, FY2024, note 29', FS25,
             '2026-02-18')
rploan24 = bs('rploan_fy24', 1652.713, 'Loan from a related party, FY2024', FS25,
              '2026-02-18')
lease24 = bs('lease_fy24', 451.040 + 60.937, 'Lease liabilities, FY2024', FS25,
             '2026-02-18')
pay24 = bs('pay_fy24', 1287.211 + 6961.331, 'Trade and other payables, FY2024', FS25,
           '2026-02-18')
dueto24 = bs('dueto_fy24', 1089.965 + 8691.405, 'Amounts due to related parties, FY2024',
             FS25, '2026-02-18')
assocbv24 = bs('assoc_bv_fy24', 2242.891, 'Investments in associates and JVs, FY2024',
               FS25, '2026-02-18')

assets23 = bs('assets_fy23', 21311.081, 'Total assets', FS23, '2024-02-15')
eqp23 = bs('eqp_fy23', 13769.094, 'Equity attributable to owners', FS23, '2024-02-15')
nci23 = bs('nci_fy23', 1149.566, 'Non-controlling interests', FS23, '2024-02-15')
loans23 = bs('loans_fy23', 1758.963 + 217.172, 'Loans and borrowings, NC + C', FS23,
             '2024-02-15')
cash23 = bs('cash_fy23', 2259.902, 'Cash and bank balances', FS23, '2024-02-15')
ip23 = bs('ip_fy23', 7536.858, 'Investment properties', FS23, '2024-02-15')
inv23 = bs('inv_fy23', 2246.917, 'Inventory properties', FS23, '2024-02-15')

debt25 = loans25 + rploan25
debt24 = loans24 + rploan24
nd25 = debt25 - cash25          # strict statement basis: net cash 5,852.901
nd24 = debt24 - cash24
nwc25 = inv25 + dwip25 + recv25 + duefr25 - pay25 - dueto25
nwc24 = inv24 + dwip24 + recv24 + duefr24 - pay24 - dueto24
D['hist_bs'] = dict(
    FY23=dict(ppe=789.463, ip=ip23, inv=inv23, recv=1039.926 + 645.607, cash=cash23,
              assets=assets23, debt=loans23, eqp=eqp23, nci=nci23,
              nd=loans23 - cash23, nwc=float('nan')),
    FY24=dict(ppe=ppe24, ip=ip24, inv=inv24, dwip=dwip24, recv=recv24, duefr=duefr24,
              cash=cash24, assets=assets24, debt=debt24, pay=pay24, dueto=dueto24,
              eqp=eqp24, nci=nci24, nd=nd24, nwc=nwc24),
    FY25=dict(ppe=ppe25, ip=ip25, inv=inv25, dwip=dwip25, recv=recv25, duefr=duefr25,
              cash=cash25, assets=assets25, debt=debt25, pay=pay25, dueto=dueto25,
              eqp=eqp25, nci=nci25, nd=nd25, nwc=nwc25),
)
# net cash, both framings (dual-framing rule)
netcash_strict = -nd25
netcash_company = inp('netcash_company', 1800.0, 'Net cash AED 1.8bn on the company '
                      'definition (available cash incl. qualifying escrow less total '
                      'debt incl. the related-party loan), ' + PR25, '2026-02-18',
                      'Company')
D['netcash'] = dict(strict=netcash_strict, company=netcash_company,
                    note='strict = all cash and bank balances (incl. escrow/restricted) '
                         'less loans+related-party loan; company definition restricts '
                         'to available cash')

# ---- historical cash flow (AED mn) ------------------------------------------
ocf25 = inp('ocf_fy25', 3860.373, 'Net cash generated from operating activities, '
            + FS25, '2026-02-18', 'Company')
ocf24 = inp('ocf_fy24', 3231.447, 'Net cash from operating activities, FY2024 '
            'comparatives, ' + FS25, '2026-02-18', 'Company')
capex25 = inp('capex_fy25', 1072.497 + 25.513 + 162.556, 'Purchases of PP&E 1,072.497 '
              '+ intangibles 25.513 + investment properties 162.556, cash flow '
              'statement, ' + FS25, '2026-02-18', 'Company')
capex24 = inp('capex_fy24', 1112.883 + 5.584 + 128.533, 'Same three lines, FY2024 '
              'comparatives, ' + FS25, '2026-02-18', 'Company')
D['hist_cf'] = dict(FY24=dict(ocf=ocf24, capex=capex24),
                    FY25=dict(ocf=ocf25, capex=capex25))

# ---- H1-2026 actuals (study-year anchor) ------------------------------------
h1_rev = inp('h1_26_rev', 9188.304, 'Revenues, ' + H126, '2026-08-07', 'Company')
h1_gp = inp('h1_26_gp', 3201.275, 'Gross profit, ' + H126, '2026-08-07', 'Company')
h1_pbt = inp('h1_26_pbt', 2601.227, 'Profit before tax, continuing, ' + H126,
             '2026-08-07', 'Company')
h1_pat = inp('h1_26_pat', 2202.138, 'Profit for the period, ' + H126, '2026-08-07',
             'Company')
h1_npa = inp('h1_26_npa', 2162.966, 'Profit attributable to owners, ' + H126,
             '2026-08-07', 'Company')
h1_tax = inp('h1_26_tax', 401.202, 'Income tax expense, ' + H126, '2026-08-07',
             'Company')
h1_ga = inp('h1_26_ga', 685.124, 'General and administrative expenses, ' + H126,
            '2026-08-07', 'Company')
h1_ocf = inp('h1_26_ocf', -3921.027, 'Net cash used in operating activities '
             '(receivables and related-party balances built up AED 5.4bn), ' + H126,
             '2026-08-07', 'Company')
h1_loans = inp('h1_26_loans', 8541.685, 'Loans and borrowings NC 3,821.289 + C '
               '4,720.396, ' + H126, '2026-08-07', 'Company')
h1_rploan = inp('h1_26_rploan', 1000.0, 'Loan from a related party, current, ' + H126,
                '2026-08-07', 'Company')
h1_cash = inp('h1_26_cash', 12303.240, 'Cash and bank balances, ' + H126, '2026-08-07',
              'Company')
h1_eqp = inp('h1_26_eqp', 56396.629, 'Equity attributable to owners, ' + H126,
             '2026-08-07', 'Company')
h1_eff_tax = h1_tax / h1_pbt
D['h1'] = dict(rev=h1_rev, gp=h1_gp, pbt=h1_pbt, pat=h1_pat, npa=h1_npa,
               eff_tax=h1_eff_tax, ga=h1_ga, ocf=h1_ocf,
               debt=h1_loans + h1_rploan, cash=h1_cash, eqp=h1_eqp,
               rev_yoy=h1_rev / 6545.053 - 1)

# ---- segments (IFRS 8, note 33 FY2025 / note 28 H1-2026) --------------------
SEG = ['red', 'aim', 'hosp', 'ect']
segnames = dict(red='Real Estate Development', aim='Asset & Investment Management',
                hosp='Hospitality', ect='Events, Catering & Tourism')
seg_rev25 = dict(red=inp('seg_red_rev25', 7403.313, 'Segment revenues, note 33, ' + FS25,
                         '2026-02-18', 'Company'),
                 aim=inp('seg_aim_rev25', 654.658, 'Segment revenues, note 33, ' + FS25,
                         '2026-02-18', 'Company'),
                 hosp=inp('seg_hosp_rev25', 791.771, 'Segment revenues, note 33, ' + FS25,
                          '2026-02-18', 'Company'),
                 ect=inp('seg_ect_rev25', 5008.749, 'Segment revenues, note 33, ' + FS25,
                         '2026-02-18', 'Company'))
seg_oth_rev25 = inp('seg_oth_rev25', -29.622, 'Others segment (corporate, '
                    'eliminations), note 33, ' + FS25, '2026-02-18', 'Company')
seg_gp25 = dict(red=inp('seg_red_gp25', 3232.891, 'Segment gross profit, note 33, '
                        + FS25, '2026-02-18', 'Company'),
                aim=inp('seg_aim_gp25', 421.083, 'Segment gross profit, note 33, '
                        + FS25, '2026-02-18', 'Company'),
                hosp=inp('seg_hosp_gp25', 210.893, 'Segment gross profit, note 33, '
                         + FS25, '2026-02-18', 'Company'),
                ect=inp('seg_ect_gp25', 1325.029, 'Segment gross profit, note 33, '
                        + FS25, '2026-02-18', 'Company'))
seg_oth_gp25 = inp('seg_oth_gp25', -164.637, 'Others segment gross loss, note 33, '
                   + FS25, '2026-02-18', 'Company')
seg_pbt25 = dict(red=2547.573, aim=685.082, hosp=-69.150, ect=1061.602)
seg_assets25 = dict(red=55738.581, aim=11095.849, hosp=4601.757, ect=14118.268)
inp('seg_pbt25', seg_pbt25, 'Segment profit before tax, note 33, ' + FS25,
    '2026-02-18', 'Company')
inp('seg_assets25', seg_assets25, 'Segment assets, note 33, ' + FS25, '2026-02-18',
    'Company')
A(abs(sum(seg_rev25.values()) + seg_oth_rev25 - rev25) < 0.5,
  'segment revenues + others sum to group revenue FY2025')
A(abs(sum(seg_gp25.values()) + seg_oth_gp25 - gp25) < 0.5,
  'segment gross profit + others sums to group gross profit FY2025')
seg_rev24 = dict(red=2869.294, aim=578.358, hosp=569.870, ect=2493.660)
inp('seg_rev24', seg_rev24, 'Segment revenues FY2024, note 33 comparatives, ' + FS25,
    '2026-02-18', 'Company')
h1_seg_rev = dict(red=5675.275, aim=360.966, hosp=388.398, ect=2775.402)
h1_seg_gp = dict(red=2342.842, aim=258.380, hosp=105.504, ect=552.062)
inp('h1_seg', dict(rev=h1_seg_rev, gp=h1_seg_gp), 'Segment table, note 28, ' + H126,
    '2026-08-07', 'Company')
D['seg_fy25'] = dict(rev=seg_rev25, gp=seg_gp25, pbt=seg_pbt25, assets=seg_assets25,
                     oth_rev=seg_oth_rev25, oth_gp=seg_oth_gp25, names=segnames,
                     gp_margin={k: seg_gp25[k] / seg_rev25[k] for k in SEG},
                     rev24=seg_rev24, h1_rev=h1_seg_rev, h1_gp=h1_seg_gp,
                     h1_gp_margin={k: h1_seg_gp[k] / h1_seg_rev[k] for k in SEG})

# ---- unit-level anchors (development volume x price; AR2025) ----------------
sales25 = inp('sales25_total', 36300.0, 'Total real estate sales AED 36.3bn across '
              '6,358 units, ' + AR25, '2026-03-31', 'Company')
units25 = inp('units25', 6358, 'Units sold across launches, ' + AR25, '2026-03-31',
              'Company')
sales25_uae = inp('sales25_uae', 29800.0, 'UAE sales (incl. JV) AED 29.8bn across '
                  '4,243 units, ' + AR25, '2026-03-31', 'Company')
units25_uae = inp('units25_uae', 4243, 'UAE units, ' + AR25, '2026-03-31', 'Company')
sales25_intl = inp('sales25_intl', 6600.0, 'International sales (Egypt+Spain+JV) '
                   'AED 6.6bn across 2,115 units, ' + AR25, '2026-03-31', 'Company')
units25_intl = inp('units25_intl', 2115, 'International units, ' + AR25, '2026-03-31',
                   'Company')
backlog = inp('backlog', 46000.0, 'Revenue backlog AED 46.0bn, 93% development sales, '
              + PR25, '2026-02-18', 'Company')
dev_backlog = inp('dev_backlog', 42600.0, 'Development backlog (UAE + Egypt) AED '
                  '42.6bn, ' + AR25, '2026-03-31', 'Company')
D['units'] = dict(total=dict(sales=sales25, units=units25, px=sales25 / units25),
                  uae=dict(sales=sales25_uae, units=units25_uae,
                           px=sales25_uae / units25_uae),
                  intl=dict(sales=sales25_intl, units=units25_intl,
                            px=sales25_intl / units25_intl),
                  backlog=backlog, dev_backlog=dev_backlog)

# =============================================================================
# H1-2026 RESULTS RELEASE (29-Jul-2026) — the restrike anchors [ADDED at revision 2,
# 09-Aug-2026: the first edition struck its development drivers on 31-Dec-2025
# disclosures although this release existed; the external audits caught it]
# =============================================================================
H1R = ("Modon H1-2026 results announcement, modon.com media centre, 29-Jul-2026 "
       "(verified via Zawya/WAM syndication of the official release)")
h1_backlog = inp('h1_backlog', 65400.0, 'Group revenue backlog AED 65.4bn, doubling '
                 'y/y, +42% vs FY2025; ' + H1R, '2026-07-29', 'Company')
h1_dev_share = inp('h1_dev_share', 0.95, 'Development projects across the UAE and '
                   'Egypt = 95% of the total backlog; ' + H1R, '2026-07-29', 'Company')
dev_backlog_h1 = h1_backlog * h1_dev_share
h1_sales = inp('h1_sales', 26000.0, 'H1-2026 real estate sales AED 26bn (2.6x H1-2025), '
               'incl. AED 23bn Abu Dhabi; Hudayriyat Golf Estates AED 13bn within days; '
               + H1R, '2026-07-29', 'Company')
h1_netdebt = inp('h1_netdebt', 912.0, 'Net debt AED 912mn (0.02x equity) at 30-Jun-2026, '
                 'company definition; ' + H1R, '2026-07-29', 'Company')
h1_avail_cash = inp('h1_avail_cash', 8600.0, 'AED 8.6bn of unrestricted cash plus AED '
                    '1.5bn undrawn committed facilities; ' + H1R, '2026-07-29', 'Company')
h1_adj_ebitda = inp('h1_adj_ebitda', 2995.0, 'H1-2026 Group Adjusted EBITDA AED 3.0bn, '
                    'margin 32.6% (32.6% x 9,188 = 2,995); ' + H1R, '2026-07-29',
                    'Company')
h1_keys = inp('h1_keys', 3613, 'Hospitality portfolio 3,613 keys across 16 owned, '
              'operated and JV hotels (narrower perimeter than the FY2025 report\'s '
              '7,137 keys across 27 hotels incl. managed); ' + H1R, '2026-07-29',
              'Company')
h1_recurring = inp('h1_recurring', 3500.0, 'Recurring revenues +22% y/y to AED 3.5bn '
                   '= 38% of Group revenues; ' + H1R, '2026-07-29', 'Company')

# 30-Jun-2026 balance-sheet anchors (reviewed interim, already extracted above)
bs30_cash_total = h1_cash                          # 12,303.240
bs30_debt = h1_loans + h1_rploan                   # 9,541.685
bs30_lease = inp('h1_lease', 559.703 + 85.096, 'Lease liabilities NC + C, ' + H126,
                 '2026-08-07', 'Company')
bs30_assoc = inp('h1_assoc_bv', 2826.454, 'Investments in associates and JVs, ' + H126,
                 '2026-08-07', 'Company')
bs30_finass = inp('h1_finass', 338.000 + 54.972, 'Investments in financial assets, '
                  'NC + C, ' + H126, '2026-08-07', 'Company')
bs30_nci = inp('h1_nci', 922.342, 'Non-controlling interests, ' + H126, '2026-08-07',
               'Company')
bs30_eqp = h1_eqp                                  # 56,396.629
bs30_recv = inp('h1_recv_total', 762.616 + 10637.555 + 2436.750 + 8318.759,
                'Trade and other receivables (NC+C) + amounts due from related '
                'parties (NC+C), 30-Jun-2026, ' + H126, '2026-08-07', 'Company')
bs30_invdwip = inp('h1_inv_dwip', 27599.592 + 6487.697, 'Inventories + development '
                   'work-in-progress, 30-Jun-2026, ' + H126, '2026-08-07', 'Company')
bs30_pay = inp('h1_pay_total', 4219.904 + 16903.729 + 717.981 + 447.706,
               'Trade and other payables (NC+C, incl. customer advances/contract '
               'liabilities) + amounts due to related parties, 30-Jun-2026, ' + H126,
               '2026-08-07', 'Company')
nwc30 = bs30_recv + bs30_invdwip - bs30_pay
D['h1_anchors'] = dict(backlog=h1_backlog, dev_backlog=dev_backlog_h1,
                       sales=h1_sales, netdebt=h1_netdebt, avail_cash=h1_avail_cash,
                       cash_total=bs30_cash_total, debt=bs30_debt, lease=bs30_lease,
                       assoc=bs30_assoc, finass=bs30_finass, nci=bs30_nci,
                       eqp=bs30_eqp, recv=bs30_recv, invdwip=bs30_invdwip,
                       pay=bs30_pay, nwc=nwc30, adj_ebitda=h1_adj_ebitda)

# =============================================================================
# FORECAST v2 — valuation date 30-Jun-2026; H2-2026 stub + FY2027E..FY2030E.
# Bottom-up: development off the DISCLOSED 30-Jun backlog with H1-realised
# anchors; working capital from components (receivable days, land-bank
# conversion, payables/advances cover) calibrated to the two audited/reviewed
# balance-sheet dates; D&A off the asset base, not revenue.
# =============================================================================
years = ['H2-26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
NY = 5
YRFRAC = [0.5, 1.0, 1.0, 1.0, 1.0]
T_EXP = [0.5, 1.5, 2.5, 3.5, 4.5]     # end-of-period discounting from 30-Jun-2026

conv_path = inp('conv_path', [0.105, 0.25, 0.28, 0.30, 0.32],
                'Backlog conversion on opening development backlog (H2-2026 is a '
                'half-year rate). Anchor: H1-2026 realised development revenue '
                'ex-land 4,237 = 9.9% of the 42,600 opening — a ~20-23% annualised '
                'pace on a growing base, stepping up as the record construction '
                'book mobilises', '2026-08-09', 'House')
new_sales = inp('new_sales', [12000.0, 30000.0, 26000.0, 23000.0, 21000.0],
                'New development sales, BASE path, POST-H1 (the AED 26bn H1-2026 '
                'actual is already inside the opening backlog): H2-2026 12bn '
                '(no assumed repeat of the 13bn Golf Estates launch), then fading '
                '30->21bn/yr — still below the 52bn annualised H1 run-rate '
                'throughout', '2026-08-09', 'House')
land_rev = inp('land_rev', [700.0, 1400.0, 1300.0, 1200.0, 1100.0],
               'Point-in-time land and plot sales: H1-2026 actual was 1,438; '
               'tapering path', '2026-08-09', 'House')
red_margin = inp('red_margin', [0.41, 0.40, 0.39, 0.385, 0.38],
                 'RED gross margin: FY2025 43.7%, H1-2026 actual 41.3%; glides to '
                 '38% as related-party land mix fades and the ~4% tender-price '
                 'escalator runs ahead of ~2% realised-price escalation',
                 '2026-08-09', 'House')
aim_growth = inp('aim_growth', [None, 0.09, 0.085, 0.08, 0.08],
                 'AIM revenue growth off the FY2026E base; H2-2026E set directly',
                 '2026-08-09', 'House')
aim_h2 = inp('aim_h2', 385.0, 'AIM H2-2026E revenue: H1 actual 361 with contracted '
             'occupancy 96% and GLA additions', '2026-08-09', 'House')
aim_margin = inp('aim_margin', [0.68, 0.66, 0.65, 0.64, 0.64],
                 'AIM gross margin: FY2025 64.3%, H1-2026 actual 71.6%; held near '
                 'the blend', '2026-08-09', 'House')
hosp_growth = inp('hosp_growth', [None, 0.07, 0.07, 0.06, 0.06],
                  'Hospitality growth off FY2026E; H2 set directly', '2026-08-09',
                  'House')
hosp_h2 = inp('hosp_h2', 452.0, 'Hospitality H2-2026E: H1 actual 388 plus the '
              'winter-season weighting (H2-2025 was 52% of the year)', '2026-08-09',
              'House')
hosp_margin = inp('hosp_margin', [0.29, 0.28, 0.29, 0.30, 0.30],
                  'Hospitality gross margin: H1-2026 actual 27.2%, recovering to 30%',
                  '2026-08-09', 'House')
ect_growth = inp('ect_growth', [None, 0.045, 0.043, 0.041, 0.039],
                 'ECT growth off FY2026E; H2 set directly', '2026-08-09', 'House')
ect_h2 = inp('ect_h2', 3000.0, 'ECT H2-2026E: H1 actual 2,775 plus the H2-weighted '
             'events season (ADNEC calendar; Arena full-period)', '2026-08-09',
             'House')
ect_margin = inp('ect_margin', [0.29, 0.27, 0.275, 0.28, 0.28],
                 'ECT gross margin: H1-2026 actual 19.9% (temporary-infrastructure '
                 'mix), recovering toward the FY2025 26.5% as the events season '
                 'carries H2', '2026-08-09', 'House')
oth_rev_f = inp('oth_rev_f', -30.0, 'Others / eliminations, full-year rate',
                '2026-08-09', 'House')
oth_gp_f = inp('oth_gp_f', -120.0, 'Others gross loss, full-year rate (H1-2026 '
               'actual -57.5)', '2026-08-09', 'House')
ga_pct = inp('ga_pct', [0.083, 0.088, 0.087, 0.086, 0.085],
             'G&A / revenue. Anchors stated: FY2025 11.19%; H1-2026 headline 7.46% '
             'flattered by a -77.9 ECL reversal — ex-reversal 8.30%. The path '
             'glides 8.3% -> 8.5-8.8%, i.e. BELOW FY2025 on realised operating '
             'leverage but ABOVE the flattered H1 print. The first edition\'s '
             'conservatism claim is withdrawn: this is a generous assumption '
             'relative to FY2025 and is now labelled as such', '2026-08-09', 'House')
sm_pct = inp('sm_pct', [0.017, 0.018, 0.017, 0.017, 0.016],
             'S&M / revenue: FY2025 1.93%, H1-2026 1.64%', '2026-08-09', 'House')
invinc_f = inp('invinc_f', [80.0, 165.0, 170.0, 175.0, 180.0],
               'Investment and other income, recurring component (H1-2026 actual 71 '
               'incl. one-offs)', '2026-08-09', 'House')
assoc_f_path = inp('assoc_f_path', [95.0, 210.0, 227.0, 245.0, 264.0],
                   'Associate/JV income: H1-2026 actual 88.3 post the Q2 JV '
                   'disposal; ~8%/yr thereafter', '2026-08-09', 'House')
dna_rate = inp('dna_rate', 0.034, 'Depreciation & amortisation as a rate on the '
               'AVERAGE depreciable asset base (PP&E + investment properties + '
               'right-of-use + intangibles): FY2025 charge 610.5 on an average '
               'base of ~17,940 = 3.4%. Respecified off the asset base at '
               'revision 2 — the first edition drove D&A off revenue, a '
               'mis-specified driver both external audits flagged', '2026-08-09',
               'House')
asset_base_30jun = inp('asset_base_30jun', 8702.928 + 9496.084 + 529.636 + 1007.486,
                       'Depreciable base at 30-Jun-2026: PP&E 8,702.928 + investment '
                       'properties 9,496.084 + right-of-use 529.636 + intangibles '
                       '1,007.486, ' + H126, '2026-08-07', 'Company')
capex_f = inp('capex_f', [700.0, 1500.0, 1550.0, 1600.0, 1650.0],
              'Capital expenditure (H2 stub then annual): H1-2026 actual 312.5 '
              '(PP&E 206.9 + intangibles 63.5 + IP 42.0); rising with Olympia and '
              'venue pipeline', '2026-08-09', 'House')
tax_f = inp('tax_f', 0.155, 'Effective tax: DMTT 15% floor + foreign uplift; '
            'H1-2026 actual 15.4%', '2026-08-09', 'House')
nci_pct = inp('nci_pct', 0.02, 'NCI share of profit: H1-2026 actual 1.8%',
              '2026-08-09', 'House')

# ---- working capital from components (SIGCM clause 4), calibrated at
# 31-Dec-2025 and 30-Jun-2026 --------------------------------------------------
dso_path = inp('dso_path', [440.0, 430.0, 410.0, 390.0, 370.0],
               'Receivable days (trade + contract + related-party receivables '
               'over revenue): FY2025 439 days, 30-Jun-2026 440 days — held flat '
               'through 2026 then declining as Department-of-Finance balances '
               'collect. THE collection caveat in one driver', '2026-08-09', 'House')
inv_addition = inp('inv_addition', 0.10, 'New-project WIP added per dirham of new '
                   'development sales (mobilisation, infrastructure)', '2026-08-09',
                   'House')
inv_consumption = inp('inv_consumption', 0.20, 'Share of RED direct costs drawn '
                      'from the existing land bank / WIP (land content of cost of '
                      'sales)', '2026-08-09', 'House')
pay_cover = inp('pay_cover', [1.86, 1.70, 1.55, 1.45, 1.40],
                'Trade payables + customer advances + related-party payables as a '
                'multiple of annual direct costs: FY2025 2.62x (advance-heavy), '
                '30-Jun-2026 1.86x; declining as handovers recognise advances. '
                'This is the presale-funding mechanism: customers, not the '
                'balance sheet, fund construction', '2026-08-09', 'House')

# ---- build the paths ---------------------------------------------------------
red_rev, aim_rev, hosp_rev, ect_rev = [], [], [], []
bl_open, bl_close, dev_rev_l = [], [], []
bl = dev_backlog_h1
for t in range(NY):
    dr = conv_path[t] * bl
    rr = dr + land_rev[t]
    bl_open.append(bl); bl = bl + new_sales[t] - dr; bl_close.append(bl)
    dev_rev_l.append(dr); red_rev.append(rr)
    if t == 0:
        aim_rev.append(aim_h2); hosp_rev.append(hosp_h2); ect_rev.append(ect_h2)
    elif t == 1:
        # FY2027 = the FULL FY2026 (H1 actual + H2 stub) grown at the segment rate
        aim_rev.append((h1_seg_rev['aim'] + aim_h2) * (1 + aim_growth[t]))
        hosp_rev.append((h1_seg_rev['hosp'] + hosp_h2) * (1 + hosp_growth[t]))
        ect_rev.append((h1_seg_rev['ect'] + ect_h2) * (1 + ect_growth[t]))
    else:
        aim_rev.append(aim_rev[-1] * (1 + aim_growth[t]))
        hosp_rev.append(hosp_rev[-1] * (1 + hosp_growth[t]))
        ect_rev.append(ect_rev[-1] * (1 + ect_growth[t]))

rev_f = [red_rev[t] + aim_rev[t] + hosp_rev[t] + ect_rev[t] + oth_rev_f * YRFRAC[t]
         for t in range(NY)]
gp_f = [red_rev[t] * red_margin[t] + aim_rev[t] * aim_margin[t]
        + hosp_rev[t] * hosp_margin[t] + ect_rev[t] * ect_margin[t]
        + oth_gp_f * YRFRAC[t] for t in range(NY)]
ga_f = [ga_pct[t] * rev_f[t] for t in range(NY)]
sm_f = [sm_pct[t] * rev_f[t] for t in range(NY)]
ebit_f = [gp_f[t] - ga_f[t] - sm_f[t] + invinc_f[t] for t in range(NY)]
# D&A off the asset base
dna_f, ab = [], asset_base_30jun
for t in range(NY):
    da = dna_rate * (ab + capex_f[t] / 2) * YRFRAC[t]
    dna_f.append(da); ab = ab + capex_f[t] - da
ebitda_f = [ebit_f[t] + dna_f[t] for t in range(NY)]
assoc_f = assoc_f_path
nopat_f = [ebit_f[t] * (1 - tax_f) for t in range(NY)]

# WC components
fy26_rev_total = h1_rev + rev_f[0]
recv_f, inv_f, pay_f, nwc_f, dnwc_f = [], [], [], [], []
rprev, iprev, pprev, nprev = bs30_recv, bs30_invdwip, bs30_pay, nwc30
for t in range(NY):
    rev_run = fy26_rev_total if t == 0 else rev_f[t]
    dc_run = (fy26_rev_total - (h1_gp + gp_f[0])) if t == 0 else rev_f[t] - gp_f[t]
    red_cost = red_rev[t] * (1 - red_margin[t])
    recv = dso_path[t] / 365.0 * rev_run
    invv = iprev + inv_addition * new_sales[t] - inv_consumption * red_cost
    pay = pay_cover[t] * dc_run
    nwc = recv + invv - pay
    recv_f.append(recv); inv_f.append(invv); pay_f.append(pay)
    nwc_f.append(nwc); dnwc_f.append(nwc - nprev)
    rprev, iprev, pprev, nprev = recv, invv, pay, nwc
fcff_f = [nopat_f[t] + dna_f[t] - capex_f[t] - dnwc_f[t] for t in range(NY)]

# =============================================================================
# COST OF CAPITAL v3 — beta is now TIER 1: the own-stock regression against the
# stock's OWN local index, the official FTSE ADX General. Revision 2 ran a
# flagged PROXY (equal-weight composite) because the official series could not
# be obtained through ten logged sources; it arrived 10-Aug-2026 and replaces
# the proxy. The proxy was not a harmless stand-in: the official index is 1.30x
# LESS volatile than the composite at a similar correlation, and beta is
# corr x (sigma_stock / sigma_market), so the smaller denominator lifts beta
# 1.03 -> 1.278 and takes the central down 3.38 -> 2.98. Numbers below are READ
# from beta_official.json — none is typed here.
# =============================================================================
_BETA = json.load(open(os.path.join(HERE, 'beta_official.json')))
rf_gross = inp('rf', 0.0448, 'AED sovereign anchor: Jan-2031 dirham T-Bond, 4.48% '
               'YTM, July-2026 auction, ~4bp over UST (UAE MoF via WAM) — the '
               'longest liquid AED government tranche; the tenor choice (4.4y vs a '
               'perpetual stream) is stated as a limitation', '2026-07-30', 'Country')
sov_spread = inp('sov_spread_rating', 0.0042, 'Damodaran adjusted default spread, '
                 'UAE (Aa2), rating basis, January-2026 ctryprem (the July-2026 '
                 'refresh carries the same UAE parameters per independent '
                 'verification; vintage stated)', '2026-01-05', 'Country')
erp_rating = inp('erp_rating', 0.0487, 'Damodaran total ERP, UAE row, rating basis',
                 '2026-01-05', 'Country')
inp('erp_cds_na', 'NA', 'No UAE sovereign CDS row is published — the CDS-basis '
    'WACC cannot be built; rating basis stands alone, stated', '2026-01-05',
    'Country')
_BR = _BETA['record']
beta = inp('beta', _BETA['adopted_beta'],
           'TIER 1 — own-stock weekly regression against the PUBLISHED INDEX OF THE '
           'EXCHANGE THE STOCK IS LISTED ON (FTSE ADX General, '
           f'{_BR["index_file"]}, as of {_BR["index_asof"]}), produced by the house '
           'regression module and passed through the beta-provenance gate, not by a '
           'study-local script. Dimson lead-lag corrected, which matters here: 84.75% '
           'of the shares sit with a single holder, and non-synchronous trading biases '
           'a naive beta DOWNWARD — the correction is worth '
           f'{_BETA["adopted_beta"] - _BETA["naive"]["beta"]:+.3f} of beta '
           f'({_BETA["naive"]["beta"]:.3f} naive on the same weeks). Diagnostics: SE '
           f'{_BR["se"]:.3f}, R2 {_BR["r2"]:.3f}, n {_BR["n"]}, 90% CI '
           f'[{_BR["ci90"][0]:.3f}, {_BR["ci90"][1]:.3f}], usability gate PASS. '
           f'Blume cross-check {_BR["blume_crosscheck"]:.3f}. THE CONFIDENCE INTERVAL '
           'IS WIDE — this beta is quoted with its interval everywhere it supports a '
           'conclusion, never as a precise point. SUPERSEDES both earlier regressors: '
           'revision 2 used an equal-weight composite of the house UAE library (1.03 '
           'adopted) and an intermediate revision-3 pass used a study-local naive '
           'regression on the official series (1.278). A constituent composite is not '
           'a substitute and not a tier. The Damodaran EM industry route '
           '(business-weighted unlevered 0.50 -> relevered 0.56-0.59) stays REJECTED '
           'as a primary: the 786-firm Real-Estate-Development row is dominated by '
           'highly-levered Chinese developers (D/E 1.97) unrepresentative of a UAE '
           'state platform; it is retained as a lower-bound cross-check. Sensitised in '
           'steps of one standard error',
           '2026-08-10', 'Company')
inp('beta_record',
    {k: _BR[k] for k in ('beta', 'se', 'r2', 'n', 'ci90', 'usable', 'weak', 'dimson',
                         'index_file', 'index_asof', 'window_years', 'first_obs',
                         'last_obs', 'blume_crosscheck', 'conforming')},
    'Full beta provenance record as returned by the house regression module and '
    'accepted by the beta-provenance gate: regressor, as-of date, diagnostics, '
    'confidence interval and conformance flag',
    '2026-08-10', 'Company')
inp('beta_naive_same_weeks', _BETA['naive'],
    'The same regression WITHOUT the Dimson thin-trading correction, on the same '
    'weeks, so the correction is visible rather than buried in a default argument',
    '2026-08-10', 'Company')
inp('beta_retired_regressors',
    dict(rev2_proxy_composite=1.03, rev3_naive_on_official=1.278),
    'Retired regressors, kept so the swap can be priced: the revision-2 equal-weight '
    'composite of the house UAE library, and the intermediate study-local naive '
    'regression on the official series',
    '2026-08-10', 'House')
inp('beta_rev2_published', 1.03,
    'The beta PUBLISHED at revision 2 (proxy composite). Registered so the correction '
    'can be stated against what readers actually saw',
    '2026-08-09', 'House')
inp('beta_industry_check', dict(unlevered_weighted=0.501, relevered_fy25=0.563,
                                relevered_h1=0.588),
    'Damodaran January-2026 EM industry betas (betaemerg.xls, saved 07-Jan-2026): '
    'RE Development unlevered 0.452 (cash-corrected, 786 firms, D/E 1.97), RE '
    'Operations 0.590, Hotel/Gaming 0.580; gross-profit-weighted and relevered at '
    'Modon\'s structure. Cross-check only', '2026-01-07', 'Industry')
rf_star = rf_gross - sov_spread
ke = rf_star + beta * erp_rating
eibor6 = inp('eibor6m', 0.0371, 'EIBOR 6M 3.71% (31-Mar-2026 published set; the '
             'CBUAE page again refused this session — fixing retained WITH ITS '
             'DATE; a 25bp EIBOR move is ~3bp of WACC)', '2026-03-31', 'Country')
kd_margin = inp('kd_margin', 0.0165, 'Blended forward margin over 6M EIBOR from '
                'the note-29 tranche table (+0.60% newest large AED tranche to '
                '+2.5% construction; SONIA +0.95-2.05% GBP)', '2026-02-18',
                'Company/House')
kd = eibor6 + kd_margin
A(kd > rf_gross, 'marginal Kd above the AED sovereign')
kd_at = kd * (1 - tax_f)
mktcap = spot * shares_mn
we = mktcap / (mktcap + bs30_debt)
wd = bs30_debt / (mktcap + bs30_debt)
wacc = we * ke + wd * kd_at
g_term = inp('g_term', 0.025, 'Terminal growth 2.5%', '2026-08-09', 'House')
roic_term = inp('roic_term', 0.085, 'Terminal ROIC 8.5% — deliberately BELOW the '
                'model\'s own forecast path (which reaches ~15% by FY2030E as '
                'invested capital shrinks while NOPAT grows): a mean-reversion '
                'margin of safety on the block that carries ~70% of EV, and above '
                'the FY2025 clean achieved 6.1% because the at-cost land bank '
                'converts. Both anchors stated; the step-down is a choice, priced '
                'in sensitivity', '2026-08-09', 'House')
rr_term = g_term / roic_term

# forecast balance-sheet roll (needed for the DERIVED terminal weights)
debt_path = inp('debt_path', [10300.0, 10500.0, 9700.0, 8800.0, 7900.0],
                'Gross debt path incl. related-party loan from the 30-Jun-2026 '
                'actual 9,542: construction peak then amortising', '2026-08-09',
                'House')
cash_yield = inp('cash_yield', 0.035, 'Yield on cash', '2026-06-17', 'Country')
lease_int = inp('lease_int', 36.0, 'Annual interest on lease liabilities (H1-2026 '
                'actual ~18 per half), now an explicit input rather than an '
                'embedded numeral', '2026-08-07', 'Company')
np_f, npa_f, eq_f, nd_f, int_f, cash_f, debt_f = [], [], [], [], [], [], []
eq = bs30_eqp + bs30_nci
c_prev, d_prev = bs30_cash_total, bs30_debt
for t in range(NY):
    fin_cost_t = (kd * (d_prev + debt_path[t]) / 2 + lease_int) * YRFRAC[t]
    fin_inc_t = cash_yield * c_prev * YRFRAC[t]
    ebt_t = ebit_f[t] + assoc_f[t] + fin_inc_t - fin_cost_t
    np_t = ebt_t * (1 - tax_f)
    npa_f.append(np_t * (1 - nci_pct)); np_f.append(np_t); int_f.append(fin_cost_t)
    eq = eq + np_t; eq_f.append(eq)
    cash_t = c_prev + fcff_f[t] + fin_inc_t - fin_cost_t \
        - (ebt_t - ebit_f[t]) * tax_f + (debt_path[t] - d_prev)
    cash_f.append(cash_t); debt_f.append(debt_path[t]); nd_f.append(debt_path[t] - cash_t)
    c_prev, d_prev = cash_t, debt_path[t]

# terminal weights DERIVED from the model's own terminal-year structure
# (the first edition assumed 15%; both audits showed the model's own FY2030E
# balance sheet contradicts it)
wd_term = debt_f[-1] / (debt_f[-1] + eq_f[-1])
inp('wd_term_derived', wd_term, 'Terminal debt weight DERIVED from the model\'s own '
    'FY2030E balance sheet: gross debt / (gross debt + book equity). Assumed-15% '
    'retired at revision 2', '2026-08-09', 'House')
ke_term, kd_term = ke, kd
wacc_term = (1 - wd_term) * ke_term + wd_term * kd_term * (1 - tax_f)
D['wacc'] = dict(rf=rf_gross, rf_star=rf_star, sov_spread=sov_spread,
                 erp=erp_rating, beta=beta, ke_exp=ke, kd=kd, kd_at=kd_at,
                 we_exp=we, wd_exp=wd, wacc_exp=wacc,
                 ke_term=ke_term, kd_term=kd_term, kd_term_at=kd_term * (1 - tax_f),
                 wd_term=wd_term, wacc_term=wacc_term,
                 eibor6=eibor6, kd_margin=kd_margin,
                 kd_eff_fy25=(390.389 - 30.916) / ((debt24 + debt25) / 2),
                 cds_basis='NA — no UAE sovereign CDS published',
                 weights_note='market-value equity per the standing method; the '
                              'circularity (using the market\'s weights while '
                              'arguing the market misprices the equity) is '
                              'acknowledged: at the study\'s own equity value the '
                              'WACC would be ~30bp higher and the DCF ~1% lower')

# ---- DCF ---------------------------------------------------------------------
df_l = [(1 + wacc) ** -x for x in T_EXP]
pv_l = [fcff_f[t] * df_l[t] for t in range(NY)]
pv_explicit = sum(pv_l)
nopat_term = nopat_f[-1] * (1 + g_term)
tv = nopat_term * (1 - rr_term) / (wacc_term - g_term)
pv_tv = tv * df_l[-1]
ev = pv_explicit + pv_tv
tv_share = pv_tv / ev

# EV -> equity bridge at 30-Jun-2026, AVAILABLE-cash basis (revision 2: the
# gross-cash basis added ~AED 3.7bn of escrow committed to completing the very
# backlog the DCF values — the escrow's value is already inside the margins)
restricted = bs30_cash_total - h1_avail_cash
eq_attr_book_nci = ev + h1_avail_cash - bs30_debt - bs30_lease + bs30_assoc \
    + bs30_finass - bs30_nci
nci_cap = max(bs30_nci, 0.02 * eq_attr_book_nci)
eq_attr = ev + h1_avail_cash - bs30_debt - bs30_lease + bs30_assoc \
    + bs30_finass - nci_cap
ps_jun = eq_attr / shares_mn
anchor_days = inp('anchor_days', 38, 'Days from the 30-Jun-2026 valuation date '
                  '(reviewed balance sheet) to the 7-Aug-2026 price anchor — the '
                  'first edition\'s 219-day accretion from 31-Dec-2025 is retired '
                  'with the restrike', '2026-08-09', 'House')
roll = (1 + ke) ** (anchor_days / 365.0)
ps = ps_jun * roll
D['netcash'] = dict(strict=-(bs30_debt - bs30_cash_total),
                    company=-h1_netdebt,
                    note='30-Jun-2026: strict all-cash basis net cash 2,762; '
                         'company definition net DEBT 912 (available cash only). '
                         'The bridge uses the available-cash basis; the strict '
                         'basis is the disclosed alternative')

# ---- contested judgement, both ways (post-H1 basis) --------------------------
new_sales_runoff = inp('new_sales_runoff', [8000.0, 15000.0, 11000.0, 9000.0, 8000.0],
                       'RUN-OFF path, post-H1: launches halve from the realised '
                       'pace and fade — now a stress reading, not a live '
                       'alternative: the H1-2026 disclosure (26bn in six months) '
                       'falsified the first edition\'s run-off premise as a '
                       'central scenario', '2026-08-09', 'House')
red_margin_runoff = inp('red_margin_runoff', [0.40, 0.385, 0.37, 0.36, 0.35],
                        'Run-off margins', '2026-08-09', 'House')
new_sales_bull = inp('new_sales_bull', [15000.0, 34000.0, 34000.0, 34000.0, 34000.0],
                     'GROWTH-HOLD path: sales hold near the realised H1-2026 '
                     'annualised pace less the launch effect', '2026-08-09', 'House')
red_margin_bull = inp('red_margin_bull', [0.42, 0.42, 0.41, 0.41, 0.40],
                      'Growth-hold margins (published in full at revision 2 — the '
                      'first edition left this vector undisclosed)', '2026-08-09',
                      'House')


def dcf_variant(ns, rm, conv=conv_path, ke_add=0.0, dso=None, nwc_add=0.0):
    ke_x = rf_star + beta * erp_rating + ke_add
    wacc_x = we * ke_x + wd * kd_at
    dfx = [(1 + wacc_x) ** -x for x in T_EXP]
    bl_v = dev_backlog_h1
    a2 = h2_ = e2 = None
    fcffs, ebits, revs = [], [], []
    rprev2, iprev2, nprev2 = bs30_recv, bs30_invdwip, nwc30
    ab2 = asset_base_30jun
    dso_v = dso or dso_path
    for t in range(NY):
        dr = conv[t] * bl_v
        bl_v = bl_v + ns[t] - dr
        rr = dr + land_rev[t]
        av = aim_rev[t]; hv = hosp_rev[t]; ev_ = ect_rev[t]
        rv = rr + av + hv + ev_ + oth_rev_f * YRFRAC[t]
        gpv = rr * rm[t] + av * aim_margin[t] + hv * hosp_margin[t] \
            + ev_ * ect_margin[t] + oth_gp_f * YRFRAC[t]
        eb = gpv - ga_pct[t] * rv - sm_pct[t] * rv + invinc_f[t]
        da = dna_rate * (ab2 + capex_f[t] / 2) * YRFRAC[t]
        ab2 = ab2 + capex_f[t] - da
        rev_run = (h1_rev + rv) if t == 0 else rv
        dc_run = (h1_rev + rv - (h1_gp + gpv)) if t == 0 else rv - gpv
        recv = dso_v[t] / 365.0 * rev_run
        invv = iprev2 + inv_addition * ns[t] - inv_consumption * rr * (1 - rm[t])
        pay = pay_cover[t] * dc_run
        nwc = recv + invv - pay
        dn = nwc - nprev2
        rprev2, iprev2, nprev2 = recv, invv, nwc
        fcffs.append(eb * (1 - tax_f) + da - capex_f[t] - dn + nwc_add)
        ebits.append(eb); revs.append(rv)
    wt_x = (1 - wd_term) * ke_x + wd_term * kd * (1 - tax_f)
    tvv = ebits[-1] * (1 - tax_f) * (1 + g_term) * (1 - rr_term) / (wt_x - g_term)
    evv = sum(f * d for f, d in zip(fcffs, dfx)) + tvv * dfx[-1]
    eqv = evv + h1_avail_cash - bs30_debt - bs30_lease + bs30_assoc + bs30_finass
    eqv_attr = eqv - max(bs30_nci, 0.02 * (eqv - bs30_nci))
    return dict(ev=evv, ps=eqv_attr / shares_mn * (1 + ke_x) ** (anchor_days / 365.0),
                rev=revs, fcff=fcffs, ebit=ebits)


base_check = dcf_variant(new_sales, red_margin)
A(abs(base_check['ps'] - ps) < 0.02, 'scenario engine reproduces the base DCF')
runoff = dcf_variant(new_sales_runoff, red_margin_runoff)
bull_var = dcf_variant(new_sales_bull, red_margin_bull)
D['contested'] = dict(
    name='development sales trajectory (sustained-normalising vs run-off stress)',
    base_ps=ps, runoff_ps=runoff['ps'], bull_ps=bull_var['ps'],
    runoff_ev=runoff['ev'], base_ev=ev,
    runoff_rev=runoff['rev'], runoff_fcff=runoff['fcff'],
    note='published side by side; the run-off is now labelled a stress: the '
         'H1-2026 disclosure falsified it as a live central path')

# Egypt stress (note 5 geographic revenue split — 17.08% outside UAE)
egy_crp = inp('egy_crp', 0.0971, 'Damodaran CRP, Egypt (Caa1), Jan-2026',
              '2026-01-05', 'Country')
fgn_share = inp('fgn_share', 2361.935 / 13828.869, 'Revenue OUTSIDE the UAE, FY2025 '
                'audited geographic split, note 5 (11,466.934 within / 2,361.935 '
                'outside) — recognised REVENUE, not contracted sales; one external '
                'audit asserted this split is unpublished; it is note 5 of the '
                'audited statements', '2026-02-18', 'Company')
egy = dcf_variant(new_sales, red_margin,
                  ke_add=beta * fgn_share * (egy_crp - 0.0064))
D['egy_stress'] = dict(ke=ke + beta * fgn_share * (egy_crp - 0.0064),
                       ps=egy['ps'], fgn_share=fgn_share)

ic30 = bs30_eqp + bs30_nci + bs30_debt - bs30_cash_total
ic_f = [ic30 + sum(capex_f[:t + 1]) - sum(dna_f[:t + 1]) + sum(dnwc_f[:t + 1])
        for t in range(NY)]
roic_f = [nopat_f[t] / YRFRAC[t] / ((ic_f[t] + (ic30 if t == 0 else ic_f[t - 1])) / 2)
          for t in range(NY)]

D['fcst'] = dict(years=years, yrfrac=YRFRAC, t_exp=T_EXP,
                 rev=rev_f, gp=gp_f, ga=ga_f, sm=sm_f, invinc=invinc_f,
                 ebitda=ebitda_f,
                 ebitda_margin=[ebitda_f[t] / rev_f[t] for t in range(NY)],
                 dna=dna_f, ebit=ebit_f, nopat=nopat_f, capex=capex_f,
                 dnwc=dnwc_f, recv=recv_f, invdwip=inv_f, pay=pay_f, nwc=nwc_f,
                 fcff=fcff_f, df=df_l, pv=pv_l,
                 red_rev=red_rev, aim_rev=aim_rev, hosp_rev=hosp_rev,
                 ect_rev=ect_rev, dev_rev=dev_rev_l, land_rev=land_rev,
                 bl_open=bl_open, bl_close=bl_close, new_sales=new_sales,
                 assoc=assoc_f, np=np_f, np_attr=npa_f, equity=eq_f,
                 net_debt=nd_f, cash=cash_f, debt=debt_f, interest=int_f,
                 ic=ic_f, roic=roic_f,
                 fy26_rev_total=fy26_rev_total,
                 fy26_npa_total=h1_npa + npa_f[0],
                 ic_30jun=ic30, nwc_30jun=nwc30)

D['dcf'] = dict(pv_explicit=pv_explicit, tv=tv, pv_tv=pv_tv, ev=ev,
                tv_share=tv_share, cash_avail=h1_avail_cash,
                cash_total=bs30_cash_total, restricted=restricted,
                debt=bs30_debt, lease=bs30_lease, assoc=bs30_assoc,
                finass=bs30_finass, nci_book=bs30_nci, nci_val=nci_cap,
                eq_attr=eq_attr, ps_jun=ps_jun, roll=roll, ps=ps,
                anchor_days=anchor_days, roic_term=roic_term, rr_term=rr_term,
                g=g_term, nopat_term=nopat_term,
                ps_grosscash=(ev + bs30_cash_total - bs30_debt - bs30_lease
                              + bs30_assoc + bs30_finass - nci_cap) / shares_mn * roll,
                ps_booknci=(eq_attr_book_nci / shares_mn) * roll,
                bear=runoff['ps'], bull=bull_var['ps'], ps_egystress=egy['ps'])

# ---- relative multiples lens (rebuilt: ONE attributable basis, P/E leg only
# in the average; EV/EBITDA shown as an unanchored cross-check) ----------------
peers = dict(
    ALDAR=dict(name='Aldar Properties (ADX)', spot=7.78, shares_mn=7862.6,
               mcap=61171.0, np_attr=7548.0, eps=0.96, pe_attr=8.10,
               rev=33800.0, ebitda=11200.0, backlog=71700.0,
               basis='attributable EPS 0.96 disclosed in the Q4-FY25 release; '
                     'FY2025 development backlog 71.7bn (66.5bn was the 9M-2025 '
                     'vintage, corrected at revision 2)'),
    EMAAR=dict(name='Emaar Properties (DFM)', spot=11.50, shares_mn=8838.0,
               mcap=101650.0, np_attr=17599.0, eps=None, pe_attr=5.78,
               rev=49600.0, ebitda=None, backlog=155000.0,
               basis='attributable 17,599.179 from the audited DFM filing '
                     '(previously marked n/d in error)'),
    EMAARDEV=dict(name='Emaar Development (DFM)', spot=13.38, shares_mn=4000.0,
                  mcap=53520.0, np_attr=11316.0, eps=None, pe_attr=4.73,
                  rev=27490.0, ebitda=None, backlog=125200.0,
                  basis='attributable 11,316.189 audited; backlog 125.2bn '
                        '(134.3bn was Emaar Properties\' UAE figure, corrected)'))
inp('peers', peers, 'Peer table REBUILT at revision 2 on one attributable-earnings '
    'basis from the peers\' own audited filings/releases (figures per the '
    'external audits\' primary-source checks, adopted after verification); market '
    'caps from prices at 07-Aug-2026. Cross-check only', '2026-08-09', 'Industry')
pe_just = inp('pe_just', 7.5, 'Justified P/E on FY2026E attributable profit: peer '
              'attributable trailing set 4.7x / 5.8x / 8.1x (EmaarDev / Emaar / '
              'Aldar). 7.5x = parity-minus with the sector leader: the growth and '
              'recurring-income premium and the 15%-float/related-party discount '
              'are treated as offsetting, stated as a judgement. (The first '
              'edition\'s 8.0x was described as a premium to Aldar off a broken '
              'peer table)', '2026-08-09', 'House')
fy26_npa = h1_npa + npa_f[0]
rel_pe_ps = pe_just * fy26_npa / shares_mn
ev_ebitda_just = inp('ev_ebitda_just', 7.0, 'EV/EBITDA 7.0x — HOUSE JUDGEMENT '
                     'WITHOUT A PEER ANCHOR (no peer EV/EBITDA is computable from '
                     'reachable disclosures: peer net debt not held). Shown as a '
                     'cross-check only; EXCLUDED from the lens average at '
                     'revision 2', '2026-08-09', 'House')
fy26_ebitda = h1_adj_ebitda + ebitda_f[0]
_ev_rel = ev_ebitda_just * fy26_ebitda
_eq_rel_book = _ev_rel + h1_avail_cash - bs30_debt - bs30_lease + bs30_assoc \
    + bs30_finass - bs30_nci
rel_ev_ps = (_ev_rel + h1_avail_cash - bs30_debt - bs30_lease + bs30_assoc
             + bs30_finass - max(bs30_nci, 0.02 * _eq_rel_book)) / shares_mn
rel_base = rel_pe_ps
D['rel'] = dict(pe_just=pe_just, ev_ebitda_just=ev_ebitda_just,
                pe_ps=rel_pe_ps, ev_ps=rel_ev_ps, base=rel_base,
                fy26_npa=fy26_npa, fy26_ebitda=fy26_ebitda,
                pe_trailing_attr=mktcap / npa25,
                pe_trailing_group=mktcap / pat25,
                ev_ebitda_trailing=(mktcap + nd25) / ebitda25,
                peers=peers,
                note='lens = P/E leg only; EV/EBITDA displayed as unanchored '
                     'cross-check (first edition averaged the two legs, which '
                     'disagreed by 43%, without showing either)')

# ---- normalised earnings power ----------------------------------------------
norm_sales = inp('norm_sales', 20000.0, 'Through-cycle development sales raised '
                 '18bn -> 20bn: the realised H1-2026 26bn lifts the cycle '
                 'evidence; still far below the 38bn FY2026E in-year pace',
                 '2026-08-09', 'House')
norm_margin = inp('norm_margin', 0.115, 'Through-cycle net margin', '2026-08-09',
                  'House')
recurring_base = inp('recurring_base', seg_rev25['aim'] + seg_rev25['hosp']
                     + seg_rev25['ect'],
                     'Recurring/operating legs base = FY2025 AIM + Hospitality + '
                     'ECT segment revenue (6,455.178), grown 15% to mid-cycle',
                     '2026-02-18', 'Company')
norm_rev = norm_sales * 0.85 + recurring_base * 1.15
norm_np = norm_rev * norm_margin
norm_eps = norm_np / shares_mn
norm_pe = inp('norm_pe', 8.5, 'Through-cycle P/E', '2026-08-09', 'House')
norm_ps = norm_eps * norm_pe
D['norm'] = dict(rev=norm_rev, margin=norm_margin, np=norm_np, eps=norm_eps,
                 pe=norm_pe, base=norm_ps,
                 clean_np_fy25=pat25 - oneoff25 * (1 - tax_f),
                 clean_margin_fy25=(pat25 - oneoff25 * (1 - tax_f)) / rev25)

# ---- book value & sustainable return (rolled to the anchor like the DCF) -----
bvps = bs30_eqp / shares_mn
roe_sust = inp('roe_sust', 0.075, 'Sustainable ROE 7.5%. Receipts, one cleaning '
               'only: mechanical FY2025 clean ROE (ex the 735.1 of fair-value/'
               'disposal gains, tax-effected) = 6.6%; the model\'s own forward '
               'attributable ROE path runs 7.8% -> 9.8%. 7.5% sits between the '
               'two, below the forward path — a forward-sustainable judgement, '
               'not a historical cleaning (the first edition conflated the two)',
               '2026-08-09', 'House')
pb_just = (roe_sust - g_term) / (ke - g_term)
book_ps = bvps * pb_just * roll
D['book'] = dict(bvps=bvps, roe_sust=roe_sust, pb_just=pb_just, base=book_ps,
                 roe_fy25=npa25 / ((eqp24 + eqp25) / 2),
                 roe_fy25_clean=(npa25 - oneoff25 * (1 - tax_f))
                 / ((eqp24 + eqp25) / 2),
                 pb_trailing=mktcap / bs30_eqp, rolled=True)

# ---- SOTP (weights now DERIVED from the same segment data, no fixed divisor) --
seg_w = {k: seg_gp25[k] - (ga25 + sm25) * seg_rev25[k] / rev25 for k in SEG}
tot_w = sum(max(v, 0.0) for v in seg_w.values())
D['sotp'] = dict(ev_split={k: ev * max(seg_w[k], 0.0) / tot_w for k in SEG},
                 weights=seg_w, tot_w=tot_w,
                 note='group EV allocated on FY2025 segment gross profit less a '
                      'revenue-proportional corporate load; weights and divisor '
                      'are live formulas in the workbook at revision 2')

# ---- lenses & weighted central ----------------------------------------------
w = inp('lens_weights', dict(dcf=0.40, relative=0.20, normalized=0.20, book=0.20),
        'Weights unchanged: DCF primary on backlog visibility; three market lenses '
        'carry 60% jointly — that structure, not an additional holdco discount, is '
        'how float/governance friction is priced (a 30% haircut on top would '
        'double-count it; the reading is still shown in section 4)', '2026-08-09',
        'House')
lens = dict(
    dcf=dict(name='Discounted cash flow (primary)', bear=runoff['ps'], base=ps,
             bull=bull_var['ps'], w=w['dcf']),
    relative=dict(name='Relative multiples', bear=rel_base * (4.73 / pe_just),
                  base=rel_base, bull=rel_base * (8.1 / pe_just), w=w['relative']),
    normalized=dict(name='Normalised earnings power',
                    bear=norm_eps * 6.0, base=norm_ps, bull=norm_eps * 10.5,
                    w=w['normalized']),
    book=dict(name='Book value and sustainable return',
              bear=bvps * (0.055 - g_term) / (ke - g_term) * roll,
              base=book_ps,
              bull=bvps * (0.095 - g_term) / (ke - g_term) * roll, w=w['book']),
)
central = sum(lens[k]['base'] * lens[k]['w'] for k in lens)
lo = min(lens[k]['bear'] for k in lens)
hi = max(lens[k]['bull'] for k in lens)
lens['central'] = dict(name='Weighted central', bear=lo, base=central, bull=hi, w=1.0)
D['lenses'] = lens
D['central'] = central
D['span'] = [lo, hi]
D['spot'] = spot

# ---- sensitivity (rebuilt on the base convention: explicit and terminal
# rates move TOGETHER by the same shift, preserving the terminal-weight step) ---
def dcf_shift(w_add=0.0, g_x=None, beta_x=None, margin_shift=0.0, conv_shift=0.0,
              nwc_add=0.0, sales_mult=1.0, dso_add=0.0):
    b = beta if beta_x is None else beta_x
    ke_x = rf_star + b * erp_rating + w_add
    wacc_x = we * ke_x + wd * kd_at
    wt_x = (1 - wd_term) * ke_x + wd_term * kd * (1 - tax_f)
    gx = g_term if g_x is None else g_x
    dfx = [(1 + wacc_x) ** -x for x in T_EXP]
    bl_v = dev_backlog_h1
    fcffs, ebits = [], []
    iprev2, nprev2 = bs30_invdwip, nwc30
    ab2 = asset_base_30jun
    for t in range(NY):
        cv = min(max(conv_path[t] + conv_shift * (YRFRAC[t]), 0.03), 0.6)
        ns_t = new_sales[t] * sales_mult
        dr = cv * bl_v
        bl_v = bl_v + ns_t - dr
        rr = dr + land_rev[t]
        rv = rr + aim_rev[t] + hosp_rev[t] + ect_rev[t] + oth_rev_f * YRFRAC[t]
        gpv = rr * (red_margin[t] + margin_shift) + aim_rev[t] * aim_margin[t] \
            + hosp_rev[t] * hosp_margin[t] + ect_rev[t] * ect_margin[t] \
            + oth_gp_f * YRFRAC[t]
        eb = gpv - ga_pct[t] * rv - sm_pct[t] * rv + invinc_f[t]
        da = dna_rate * (ab2 + capex_f[t] / 2) * YRFRAC[t]
        ab2 = ab2 + capex_f[t] - da
        rev_run = (h1_rev + rv) if t == 0 else rv
        dc_run = (h1_rev + rv - (h1_gp + gpv)) if t == 0 else rv - gpv
        recv = (dso_path[t] + dso_add) / 365.0 * rev_run
        invv = iprev2 + inv_addition * ns_t - inv_consumption * rr * (1 - red_margin[t] - margin_shift)
        pay = pay_cover[t] * dc_run
        nwc = recv + invv - pay
        dn = nwc - nprev2
        iprev2, nprev2 = invv, nwc
        fcffs.append(eb * (1 - tax_f) + da - capex_f[t] - dn + nwc_add)
        ebits.append(eb)
    rrx = gx / roic_term
    tvx = ebits[-1] * (1 - tax_f) * (1 + gx) * (1 - rrx) / max(wt_x - gx, 0.005)
    evx = sum(f * d for f, d in zip(fcffs, dfx)) + tvx * dfx[-1]
    eqx = evx + h1_avail_cash - bs30_debt - bs30_lease + bs30_assoc + bs30_finass
    eqx_attr = eqx - max(bs30_nci, 0.02 * (eqx - bs30_nci))
    return eqx_attr / shares_mn * (1 + ke_x) ** (anchor_days / 365.0)


A(abs(dcf_shift() - ps) < 0.02, 'sensitivity engine reproduces the base at the '
  'unshifted point (grid convention fixed at revision 2)')
g_grid = [0.015, 0.02, 0.025, 0.03, 0.035]
w_grid = [-0.01, -0.005, 0.0, 0.005, 0.01]
sens_wg = [[dcf_shift(w_add=wx, g_x=gx) for gx in g_grid] for wx in w_grid]
_bse = _BR['se']
beta_grid = [round(beta + k * _bse, 3) for k in (-2, -1, 0, 1, 2)]
grid_beta = [dcf_shift(beta_x=b) for b in beta_grid]
mg_grid = [-0.04, -0.02, 0.0, 0.02, 0.04]
grid_margin = [dcf_shift(margin_shift=m) for m in mg_grid]
conv_grid = [-0.06, -0.03, 0.0, 0.03, 0.06]
grid_conv = [dcf_shift(conv_shift=c) for c in conv_grid]
sales_grid = [0.5, 0.75, 1.0, 1.25, 1.5]
grid_sales = [dcf_shift(sales_mult=s) for s in sales_grid]
nwc_grid = [-1000.0, -500.0, 0.0, 500.0, 1000.0]
grid_nwc = [dcf_shift(nwc_add=n) for n in nwc_grid]
dso_grid = [-60.0, -30.0, 0.0, 30.0, 60.0]
grid_dso = [dcf_shift(dso_add=d_) for d_ in dso_grid]
ke_grid = [0.0, 0.005, 0.01, 0.015, 0.02]
grid_ke = [dcf_shift(w_add=k) for k in ke_grid]
D['sens'] = dict(g_grid=g_grid, wacc_grid=[wacc + x for x in w_grid], table=sens_wg,
                 beta_grid=beta_grid, grid_beta=grid_beta,
                 mg_grid=mg_grid, grid_margin=grid_margin,
                 conv_grid=conv_grid, grid_conv=grid_conv,
                 sales_grid=sales_grid, grid_sales=grid_sales,
                 nwc_grid=nwc_grid, grid_nwc=grid_nwc,
                 dso_grid=dso_grid, grid_dso=grid_dso,
                 ke_grid=ke_grid, grid_ke=grid_ke)

# ---- what the market price implies -------------------------------------------
lo_k, hi_k = 0.0, 0.25
for _ in range(60):
    mid = (lo_k + hi_k) / 2
    if dcf_shift(w_add=mid) > spot:
        lo_k = mid
    else:
        hi_k = mid
implied_ke_add = (lo_k + hi_k) / 2
D['market_implied'] = dict(ke_add=implied_ke_add, ke=ke + implied_ke_add,
                           note='cost-of-equity adder reconciling the base DCF '
                                'to the market price')
disc_solve = 1 - spot / runoff['ps']
D['market_implied']['runoff_discount'] = disc_solve

# ---- experts (post-restrike) -------------------------------------------------
land_bv = inp('land_bv', 26610.771, 'Land plots at cost, note 19, ' + FS25,
              '2026-02-18', 'Company')
land_uplift = inp('e1_land_uplift', 0.337, 'Expert 1 land mark-up = exactly HALF '
                  'the realised 67.4% related-party land-sale gross margin '
                  '(1 - 818.033/2,512.837), as the arms-length haircut — the '
                  'first edition said "half" but used 35%; aligned at revision 2',
                  '2026-08-09', 'House')
dwip_bv_h1 = inp('dwip_bv_h1', 6487.697, 'Development WIP at 30-Jun-2026, ' + H126,
                 '2026-08-07', 'Company')
e1_nav = bs30_eqp + land_bv * land_uplift + dwip_bv_h1 * 0.15
e1_ps = e1_nav / shares_mn
e1 = dict(method_short='asset value (RNAV)', base=e1_ps,
          rng=[e1_nav * 0.85 / shares_mn, e1_nav * 1.12 / shares_mn],
          nav=e1_nav, land_bv=land_bv, uplift=land_uplift,
          dwip_uplift=0.15, eqp=bs30_eqp)
e2_hair = inp('e2_rp_haircut', 0.25, 'Expert 2 haircut on the related-party '
              'receivable book (30-Jun-2026: 10,756 gross due-from)', '2026-08-09',
              'House')
rp_book_h1 = inp('rp_book_h1', 2436.750 + 8318.759, 'Amounts due from related '
                 'parties NC + C, 30-Jun-2026, ' + H126, '2026-08-07', 'Company')
e2_ps = runoff['ps'] - e2_hair * rp_book_h1 / shares_mn
e2 = dict(method_short='owner cash flow, run-off stress basis', base=e2_ps,
          rng=[e2_ps * 0.8, ps * 0.95],
          runoff_ps=runoff['ps'], haircut=e2_hair, rp_book=rp_book_h1,
          note='builds on the study\'s own run-off scenario with an independent '
               'receivable haircut — labelled as derived, not independent')
e3_pe = inp('e3_pe', 6.2, 'Expert 3 multiple = the arithmetic MEAN of the '
            'rebuilt attributable peer set (4.73 + 5.78 + 8.10)/3 = 6.20x — the '
            'first edition claimed "centre of the set" but used 6.5x; the '
            'statistic is now the one named', '2026-08-09', 'House')
e3_ps = e3_pe * fy26_npa / shares_mn
e3 = dict(method_short='peer-multiple convergence', base=e3_ps,
          rng=[4.73 * fy26_npa / shares_mn, 8.10 * fy26_npa / shares_mn],
          pe=e3_pe, npa26=fy26_npa)
D['experts'] = dict(e1=e1, e2=e2, e3=e3)
D['panel_centre'] = sorted([e1_ps, e2_ps, e3_ps])[1]

D['terminal_recon'] = dict(
    roic_fy25_clean=ebit25_clean * (1 - tax_f)
    / (eqp25 + nci25 + debt25 - cash25),
    roic_path=roic_f, roic_term=roic_term, rr_term=rr_term,
    note='terminal 8.5% sits between the FY2025 clean achieved 6.1% and the '
         'model\'s own forward path (peaking ~15% as capital releases); the '
         'step-down from the path is a deliberate mean-reversion margin of '
         'safety, stated and sensitised')

# ---- external results --------------------------------------------------------
with open(os.path.join(HERE, 'step0_result.json')) as f:
    D['step0'] = json.load(f)
with open(os.path.join(HERE, 'strike_result.json')) as f:
    D['strike'] = json.load(f)
with open(os.path.join(HERE, 'tech_read.json')) as f:
    D['tech'] = json.load(f)
A(D['step0']['verdict'] == 'PASS', 'Step 0 PASS carried')
A(abs(D['strike']['spot'] - spot) < 1e-9, 'strike anchor equals study spot')
A(D['strike']['q_annual'] == 0.0, 'q=0 sourced')

for k, v in INP.items():
    assert set(v.keys()) == {'value', 'source', 'date', 'ring'}, k
    assert v['source'] and v['date'] and v['ring'], f'orphan field on {k}'
D['inputs'] = INP
A(len(INP) >= 120, f'input register carries {len(INP)} four-field inputs')
D['assert_log'] = assert_log
D['meta']['revision'] = 2
D['meta']['valuation_date'] = '2026-06-30'
with open(OUT, 'w') as f:
    json.dump(D, f, indent=1)

print(f"inputs: {len(INP)} | asserts: {len(assert_log)}")
print(f"Ke {ke:.3%} (beta {beta}) | WACC {wacc:.3%} | term {wacc_term:.3%} "
      f"(wd_term derived {wd_term:.3%})")
print(f"rev: {[round(r) for r in rev_f]} (FY26 total {fy26_rev_total:,.0f})")
print(f"FCFF: {[round(x) for x in fcff_f]}")
print(f"dNWC: {[round(x) for x in dnwc_f]}")
print(f"EV {ev:,.0f} | TV share {tv_share:.1%} | eq_attr {eq_attr:,.0f}")
print(f"DCF ps {ps:.2f} (30-Jun {ps_jun:.2f}, roll {roll:.4f}) | runoff {runoff['ps']:.2f} "
      f"| bull {bull_var['ps']:.2f} | Egypt {egy['ps']:.2f} | gross-cash alt "
      f"{D['dcf']['ps_grosscash']:.2f}")
print(f"lenses: rel {rel_base:.2f} | norm {norm_ps:.2f} | book {book_ps:.2f}")
print(f"CENTRAL {central:.2f} vs spot {spot} ({central / spot - 1:+.1%}) | span "
      f"[{lo:.2f},{hi:.2f}] | experts {e1_ps:.2f}/{e2_ps:.2f}/{e3_ps:.2f} | "
      f"implied ke_add {implied_ke_add:.2%}")
