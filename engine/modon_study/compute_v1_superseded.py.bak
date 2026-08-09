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
# FORECAST — FY2026E..FY2030E, segment build (finest sourced level = IFRS 8
# segment, with unit-level anchors on development; full per-project volume x
# price is NOT disclosed — flagged per the ground-up mandate)
# =============================================================================
years = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
NY = 5

# development: backlog roll-forward. dev revenue_t = conv_t x opening backlog
# + point-in-time land sales; backlog_t = backlog_{t-1} + new dev sales - dev rev
conv_path = inp('conv_path', [0.24, 0.27, 0.29, 0.31, 0.33],
                'Backlog conversion rate on opening development backlog. FY2026E '
                'anchored on H1-2026 actuals (RED development revenue ex-land 4,237 '
                'in H1 = ~20% annualised pace on the opening 42,600, with an '
                'H2-weighted construction ramp), stepping up as the AED 32bn of '
                'construction contracts procured in 2025 mobilise', '2026-08-09',
                'House')
new_sales = inp('new_sales', [26000.0, 24000.0, 22000.0, 20500.0, 19000.0],
                'New development sales, BASE path: normalising from the 2025 record '
                '(33.8bn dev component of 36.3bn) toward a mid-cycle ~19-26bn as '
                'the ADREC-reported +67% residential market cools; Modon share of '
                'Abu Dhabi residential held roughly flat', '2026-08-09', 'House')
land_rev = inp('land_rev', [1800.0, 1600.0, 1400.0, 1200.0, 1000.0],
               'Point-in-time land and plot sales, tapering from the FY2025 2,513 '
               '(related-party-heavy; 67% gross margin) toward 1,000', '2026-08-09',
               'House')
red_margin = inp('red_margin', [0.41, 0.40, 0.39, 0.385, 0.38],
                 'RED gross margin: FY2025 actual 43.7%, H1-2026 41.3%; glides to '
                 '38% as the related-party land mix fades and the tender-price '
                 'escalator (~4%) runs ahead of realised-price escalation (~2%)',
                 '2026-08-09', 'House')
aim_growth = inp('aim_growth', [0.10, 0.085, 0.085, 0.08, 0.08],
                 'AIM revenue growth: 97% occupancy, contracted GLA additions, '
                 '2 Finsbury Avenue and Harborside step-ins', '2026-08-09', 'House')
aim_margin = inp('aim_margin', [0.64, 0.64, 0.64, 0.64, 0.64],
                 'AIM gross margin held at the FY2025 actual 64.3%', '2026-08-09',
                 'House')
hosp_growth = inp('hosp_growth', [0.06, 0.07, 0.07, 0.06, 0.06],
                  'Hospitality: 7,137 keys at 71% occupancy recovering toward 75% '
                  'plus Olympia Resort ramp', '2026-08-09', 'House')
hosp_margin = inp('hosp_margin', [0.27, 0.28, 0.29, 0.30, 0.30],
                  'Hospitality gross margin: FY2025 26.6% (post-2024 impairment '
                  'reset), H1-2026 27.2%, recovering to 30%', '2026-08-09', 'House')
ect_growth = inp('ect_growth', [0.118, 0.045, 0.043, 0.041, 0.039],
                 'ECT: FY2026E anchored on H1 actual 2,775 with the H2-weighted '
                 'events season (896 events, 6.3mn visitors 2025; Arena Group '
                 'full-year effect), then ~4%/yr events-industry growth',
                 '2026-08-09', 'House')
ect_margin = inp('ect_margin', [0.265, 0.27, 0.275, 0.28, 0.28],
                 'ECT gross margin: FY2025 26.5%, temporary-infrastructure mix '
                 'maturing', '2026-08-09', 'House')
oth_rev_f = inp('oth_rev_f', -30.0, 'Others/eliminations revenue, held at FY2025',
                '2026-08-09', 'House')
oth_gp_f = inp('oth_gp_f', -120.0, 'Others gross loss: FY2025 -164.6 included '
               'one-off items; H1-2026 run-rate -115', '2026-08-09', 'House')
ga_pct = inp('ga_pct', [0.088, 0.088, 0.087, 0.086, 0.085],
             'G&A as a share of revenue: FY2025 11.2%, H1-2026 actual 7.5% '
             '(operating leverage); forecast holds a conservative 8.5-8.8%',
             '2026-08-09', 'House')
sm_pct = inp('sm_pct', [0.018, 0.018, 0.017, 0.017, 0.016],
             'Selling and marketing as a share of revenue: FY2025 1.9%, H1-2026 '
             '1.6%', '2026-08-09', 'House')
invinc_f = inp('invinc_f', [160.0, 165.0, 170.0, 175.0, 180.0],
               'Investment and other income, recurring component only: FY2025 338 '
               'included 94 of one-off unwinding/disposal items; H1-2026 71',
               '2026-08-09', 'House')
assoc_g = inp('assoc_g', 0.08, 'Growth in the share of associates/JV profit off a '
              'post-disposal FY2026E base of 200', '2026-08-09', 'House')
assoc_base = inp('assoc_base', 200.0, 'FY2026E associate income base: H1-2026 actual '
                 '88.3 plus H2, after the Q2-2026 JV disposal', '2026-08-09', 'House')
dna_pct = inp('dna_pct', 0.042, 'Depreciation and amortisation as a share of revenue: '
              'FY2025 4.4%, H1-2026 3.6%; held near 4.2% as venues and resorts '
              'commission', '2026-08-09', 'House')
capex_f = inp('capex_f', [1400.0, 1500.0, 1550.0, 1600.0, 1650.0],
              'Capital expenditure: FY2025 actual 1,260.6 (PP&E + intangibles + IP); '
              'rising with Olympia Resort and venue pipeline', '2026-08-09', 'House')
nwc_release = inp('nwc_release', [-1500.0, 800.0, 1200.0, 1400.0, 1400.0],
                  'Annual net working-capital release (negative = absorption) as '
                  'the AED 26.6bn land bank and WIP convert to recognised revenue. '
                  'FY2026E ABSORBS cash: the H1-2026 interim shows AED 5.4bn of '
                  'receivable/related-party build-up and negative operating cash '
                  'flow, only partly collected in H2; releases start FY2027E as '
                  'escrows and Department-of-Finance receivables collect',
                  '2026-08-09', 'House')
tax_f = inp('tax_f', 0.155, 'Forecast effective tax rate: DMTT 15% floor on UAE '
            'profits plus the UK/Spain uplift; H1-2026 actual 15.4%', '2026-08-09',
            'House')
nci_pct = inp('nci_pct', 0.02, 'NCI share of profit: FY2025 was a small NCI loss, '
              'H1-2026 +1.8% of PAT as hospitality JVs recover', '2026-08-09', 'House')

# --- build the segment paths -------------------------------------------------
red_rev, aim_rev, hosp_rev, ect_rev = [], [], [], []
bl_open, bl_close, dev_rev_l = [], [], []
bl = dev_backlog
a_prev, h_prev, e_prev = seg_rev25['aim'], seg_rev25['hosp'], seg_rev25['ect']
for t in range(NY):
    dev_rev = conv_path[t] * bl
    rr = dev_rev + land_rev[t]
    bl_open.append(bl)
    bl = bl + new_sales[t] - dev_rev
    bl_close.append(bl)
    dev_rev_l.append(dev_rev)
    red_rev.append(rr)
    a_prev *= (1 + aim_growth[t]); aim_rev.append(a_prev)
    h_prev *= (1 + hosp_growth[t]); hosp_rev.append(h_prev)
    e_prev *= (1 + ect_growth[t]); ect_rev.append(e_prev)

rev_f = [red_rev[t] + aim_rev[t] + hosp_rev[t] + ect_rev[t] + oth_rev_f
         for t in range(NY)]
gp_f = [red_rev[t] * red_margin[t] + aim_rev[t] * aim_margin[t]
        + hosp_rev[t] * hosp_margin[t] + ect_rev[t] * ect_margin[t] + oth_gp_f
        for t in range(NY)]
ga_f = [ga_pct[t] * rev_f[t] for t in range(NY)]
sm_f = [sm_pct[t] * rev_f[t] for t in range(NY)]
ebit_f = [gp_f[t] - ga_f[t] - sm_f[t] + invinc_f[t] for t in range(NY)]
dna_f = [dna_pct * rev_f[t] for t in range(NY)]
ebitda_f = [ebit_f[t] + dna_f[t] for t in range(NY)]
assoc_f = [assoc_base * (1 + assoc_g) ** t for t in range(NY)]
nopat_f = [ebit_f[t] * (1 - tax_f) for t in range(NY)]
dnwc_f = [-nwc_release[t] for t in range(NY)]
fcff_f = [nopat_f[t] + dna_f[t] - capex_f[t] - dnwc_f[t] for t in range(NY)]

# =============================================================================
# COST OF CAPITAL — v2 (per-sovereign, bottom-up, both ERP bases where published)
# =============================================================================
rf_gross = inp('rf', 0.0448, 'AED sovereign anchor: UAE dirham T-Bond maturing '
               'Jan-2031 auctioned at 4.48% YTM (July-2026 auction, ~4bp over '
               'comparable UST), UAE MoF/CBUAE via WAM, longest liquid AED tranche',
               '2026-07-30', 'Country')
sov_spread = inp('sov_spread_rating', 0.0042, 'Damodaran adjusted default spread, '
                 'UAE row, rating basis (Aa2), January 2026 update of ctryprem',
                 '2026-01-05', 'Country')
erp_rating = inp('erp_rating', 0.0487, 'Damodaran total equity risk premium, UAE row, '
                 'rating basis, January 2026 ctryprem (mature-market base 4.23% + '
                 'CRP 0.64%)', '2026-01-05', 'Country')
inp('erp_cds_na', 'NA', 'Damodaran ctryprem UAE row: sovereign CDS and CDS-based ERP '
    'published as NA — the CDS-basis WACC cannot be built for the UAE; the '
    'consistency rule (strip the same basis you add back) is satisfied on the '
    'rating basis alone', '2026-01-05', 'Country')
beta = inp('beta', 1.0, 'Tier-3 fallback, FLAGGED INTERIM: the own-stock regression '
           'is unavailable because no FTSE ADX General Index history could be '
           'retrieved (seven sources attempted and logged); same-country peer betas '
           'need the same index. House precedent: EAND, TWOPOINTZERO. Sensitised '
           '0.8-1.2', '2026-08-09', 'House')
rf_star = rf_gross - sov_spread
ke = rf_star + beta * erp_rating
eibor6 = inp('eibor6m', 0.0371, 'EIBOR 6-month fixing 3.71% at 31-Mar-2026 (CBUAE '
             'published set via secondary mirrors; CBUAE page returned 403 at this '
             'session\'s proxy, logged)', '2026-03-31', 'Country')
kd_margin = inp('kd_margin', 0.0165, 'Blended forward margin over 6M EIBOR: the '
                'newest large AED tranche (Term Loan 15, 1,415mn, Jan-2027) priced '
                'at 6M EIBOR+0.60%; construction tranches at 3M EIBOR+0.85-2.5%; '
                'GBP venue debt at SONIA+0.95-2.05%. Blend ~+165bp', '2026-02-18',
                'Company/House')
kd = eibor6 + kd_margin
A(kd > rf_gross, f'marginal Kd {kd:.3%} sits above the AED sovereign {rf_gross:.3%} '
  '(a same-currency corporate cannot borrow below its sovereign)')
kd_at = kd * (1 - tax_f)
we = mktcap / (mktcap + debt25)
wd = debt25 / (mktcap + debt25)
wacc = we * ke + wd * kd_at
wd_term = inp('wd_term', 0.15, 'Terminal debt weight D/(D+E), normalised: current '
              'book gearing 12.8% on market values, construction-phase drawdowns '
              'push it up before land-bank cash releases pull it back',
              '2026-08-09', 'House')
g_term = inp('g_term', 0.025, 'Terminal growth 2.5%: long-run AED/USD-peg nominal '
             'growth; Abu Dhabi population and tourism growth support the real '
             'component', '2026-08-09', 'House')
ke_term = ke
kd_term = kd
wacc_term = (1 - wd_term) * ke_term + wd_term * kd_term * (1 - tax_f)
roic_term = inp('roic_term', 0.085, 'Terminal return on invested capital: FY2025 '
                'clean ROIC 6.6% rising as the at-cost land bank converts to '
                'recognised profit; capped near the terminal WACC + a thin spread',
                '2026-08-09', 'House')
rr_term = g_term / roic_term
D['wacc'] = dict(rf=rf_gross, rf_star=rf_star, sov_spread=sov_spread,
                 erp=erp_rating, beta=beta, ke_exp=ke, kd=kd, kd_at=kd_at,
                 we_exp=we, wd_exp=wd, wacc_exp=wacc,
                 ke_term=ke_term, kd_term=kd_term, kd_term_at=kd_term * (1 - tax_f),
                 wd_term=wd_term, wacc_term=wacc_term,
                 eibor6=eibor6, kd_margin=kd_margin,
                 kd_eff_fy25=(390.389 - 30.916) / ((debt24 + debt25) / 2),
                 cds_basis='NA — Damodaran publishes no UAE sovereign CDS row',
                 war_adder=0.0,
                 war_adder_note='the 1.0pt conflict adder used by the Jul-2026 AE '
                                'bank studies is retired here on auction evidence: '
                                'the July-2026 AED sovereign printed 4bp over UST; '
                                'a +1pt Ke stress is carried in sensitivity instead')

# ---- DCF --------------------------------------------------------------------
df_l = [(1 + wacc) ** -(t + 1) for t in range(NY)]
pv_l = [fcff_f[t] * df_l[t] for t in range(NY)]
pv_explicit = sum(pv_l)
nopat_term = nopat_f[-1] * (1 + g_term)
tv = nopat_term * (1 - rr_term) / (wacc_term - g_term)
pv_tv = tv * df_l[-1]
ev = pv_explicit + pv_tv
tv_share = pv_tv / ev

# EV -> equity bridge (31-Dec-2025 basis)
nci_val = nci25            # book value; alt framing below
eq_attr = ev + cash25 - debt25 - lease25 + assocbv25 + finass25 - nci_val
ps_dec = eq_attr / shares_mn
anchor_days = inp('anchor_days', 219, 'Days from the 31-Dec-2025 valuation date (the '
                  'audited balance-sheet anchor) to the 7-Aug-2026 price anchor',
                  '2026-08-09', 'House')
roll = (1 + ke) ** (anchor_days / 365.0)
ps = ps_dec * roll
eq_attr_anchor = eq_attr * roll

# NCI alternative framing: capitalise NCI at its share of group profit
nci_alt = max(nci25, 0.02 * eq_attr)
ps_nci_alt = (ev + cash25 - debt25 - lease25 + assocbv25 + finass25 - nci_alt) \
    / shares_mn * roll

# ---- CONTESTED JUDGEMENT, BOTH WAYS: backlog run-off alternative ------------
new_sales_runoff = inp('new_sales_runoff', [15000.0, 12000.0, 10000.0, 9000.0, 8000.0],
                       'ALTERNATIVE (run-off) path: new development sales halve from '
                       'the record and keep fading — the mean-reversion reading of '
                       'an ADREC market that grew 67% in a year', '2026-08-09',
                       'House')
red_margin_runoff = inp('red_margin_runoff', [0.40, 0.385, 0.37, 0.36, 0.35],
                        'Run-off RED margin: pricing power fades with volume',
                        '2026-08-09', 'House')


def dcf_variant(ns, rm, conv=conv_path):
    bl_v = dev_backlog
    fcffs, revs, ebits = [], [], []
    a2, h2, e2 = seg_rev25['aim'], seg_rev25['hosp'], seg_rev25['ect']
    for t in range(NY):
        dr = conv[t] * bl_v
        bl_v = bl_v + ns[t] - dr
        rr = dr + land_rev[t]
        a2 *= (1 + aim_growth[t]); h2 *= (1 + hosp_growth[t]); e2 *= (1 + ect_growth[t])
        rv = rr + a2 + h2 + e2 + oth_rev_f
        gpv = rr * rm[t] + a2 * aim_margin[t] + h2 * hosp_margin[t] \
            + e2 * ect_margin[t] + oth_gp_f
        eb = gpv - ga_pct[t] * rv - sm_pct[t] * rv + invinc_f[t]
        fc = eb * (1 - tax_f) + dna_pct * rv - capex_f[t] + nwc_release[t]
        revs.append(rv); ebits.append(eb); fcffs.append(fc)
    pvx = sum(f * d for f, d in zip(fcffs, df_l))
    tvv = ebits[-1] * (1 - tax_f) * (1 + g_term) * (1 - rr_term) / (wacc_term - g_term)
    evv = pvx + tvv * df_l[-1]
    eq = (evv + cash25 - debt25 - lease25 + assocbv25 + finass25 - nci_val) \
        / shares_mn * roll
    return dict(ev=evv, ps=eq, rev=revs, fcff=fcffs, ebit=ebits)


runoff = dcf_variant(new_sales_runoff, red_margin_runoff)
bull_var = dcf_variant([30000.0] * 5, [0.42, 0.42, 0.41, 0.41, 0.40])
D['contested'] = dict(
    name='development sales trajectory (sustained-normalising vs backlog run-off)',
    base_ps=ps, runoff_ps=runoff['ps'], bull_ps=bull_var['ps'],
    runoff_ev=runoff['ev'], base_ev=ev * 1.0,
    runoff_rev=runoff['rev'], runoff_fcff=runoff['fcff'],
    note='published side by side (summary table, section 1.7, workbook, Expert 2), '
         'never averaged')

# ---- Egypt stress (Ras El Hekma leg priced at Egypt risk) -------------------
egy_crp = inp('egy_crp', 0.0971, 'Damodaran country risk premium, Egypt row (Caa1), '
              'January 2026 ctryprem — applied as a stress to the ~18% of revenue '
              'earned outside the UAE', '2026-01-05', 'Country')
fgn_share = inp('fgn_share', 2361.935 / 13828.869, 'Revenue outside UAE, FY2025 '
                'geographic split, note 5, ' + FS25, '2026-02-18', 'Company')
ke_stress = rf_star + beta * (erp_rating + fgn_share * (egy_crp - 0.0064))
wacc_stress = we * ke_stress + wd * kd_at
df_s = [(1 + wacc_stress) ** -(t + 1) for t in range(NY)]
wacc_term_s = (1 - wd_term) * ke_stress + wd_term * kd_term * (1 - tax_f)
tv_s = nopat_term * (1 - rr_term) / (wacc_term_s - g_term)
ev_s = sum(f * d for f, d in zip(fcff_f, df_s)) + tv_s * df_s[-1]
ps_egystress = (ev_s + cash25 - debt25 - lease25 + assocbv25 + finass25 - nci_val) \
    / shares_mn * (1 + ke_stress) ** (anchor_days / 365.0)
D['egy_stress'] = dict(ke=ke_stress, wacc=wacc_stress, ps=ps_egystress,
                       fgn_share=fgn_share)

# ---- balance-sheet / statement roll-forward ---------------------------------
np_f, npa_f, eq_f, nd_f, int_f, cash_f, debt_f = [], [], [], [], [], [], []
eq = eqp25 + nci25
nd = nd25
debt_path = inp('debt_path', [9700.0, 9900.0, 9200.0, 8300.0, 7400.0],
                'Gross debt path (loans + related-party loan): H1-2026 actual '
                'already 9,542 as construction mobilises; amortising from FY2028 '
                'as land-bank cash releases fund the build', '2026-08-09', 'House')
cash_yield = inp('cash_yield', 0.035, 'Yield on cash balances ~ CBUAE base rate',
                 '2026-06-17', 'Country')
for t in range(NY):
    d_open = debt25 if t == 0 else debt_path[t - 1]
    c_open = cash25 if t == 0 else cash_f[t - 1]
    fin_cost_t = kd * (d_open + debt_path[t]) / 2 + 35.0
    fin_inc_t = cash_yield * c_open
    ebt_t = ebit_f[t] + assoc_f[t] + fin_inc_t - fin_cost_t
    np_t = ebt_t * (1 - tax_f)
    npa_t = np_t * (1 - nci_pct)
    np_f.append(np_t); npa_f.append(npa_t); int_f.append(fin_cost_t)
    eq = eq + np_t
    eq_f.append(eq)
    cash_t = c_open + fcff_f[t] - fin_cost_t + fin_inc_t \
        - (ebt_t * tax_f - ebit_f[t] * tax_f) + (debt_path[t] - d_open)
    cash_f.append(cash_t)
    debt_f.append(debt_path[t])
    nd_f.append(debt_path[t] - cash_t)

ic25 = eqp25 + nci25 + debt25 - cash25
nopat25_clean = ebit25_clean * (1 - tax_f)
ic_f = [ic25 + sum(capex_f[:t + 1]) - sum(dna_f[:t + 1])
        + sum(dnwc_f[:t + 1]) for t in range(NY)]
roic_f = [nopat_f[t] / ((ic_f[t] + (ic25 if t == 0 else ic_f[t - 1])) / 2)
          for t in range(NY)]

D['fcst'] = dict(years=years, rev=rev_f, gp=gp_f, ga=ga_f, sm=sm_f,
                 invinc=invinc_f, ebitda=ebitda_f,
                 ebitda_margin=[ebitda_f[t] / rev_f[t] for t in range(NY)],
                 dna=dna_f, ebit=ebit_f, nopat=nopat_f, capex=capex_f,
                 dnwc=dnwc_f, nwc_release=nwc_release, fcff=fcff_f, df=df_l, pv=pv_l,
                 red_rev=red_rev, aim_rev=aim_rev, hosp_rev=hosp_rev,
                 ect_rev=ect_rev, dev_rev=dev_rev_l, land_rev=land_rev,
                 bl_open=bl_open, bl_close=bl_close, new_sales=new_sales,
                 assoc=assoc_f, np=np_f, np_attr=npa_f, equity=eq_f,
                 net_debt=nd_f, cash=cash_f, debt=debt_f, interest=int_f,
                 ic=ic_f, roic=roic_f,
                 nwc=[nwc25 + sum(dnwc_f[:t + 1]) for t in range(NY)],
                 ic_fy25=ic25, nopat_fy25=nopat25_clean, nwc_fy25=nwc25,
                 dna_fy25=dna25, eqp_fy25=eqp25, debt_fy25=debt25)

D['dcf'] = dict(pv_explicit=pv_explicit, tv=tv, pv_tv=pv_tv, ev=ev,
                tv_share=tv_share, cash=cash25, debt=debt25, lease=lease25,
                assoc=assocbv25, finass=finass25, nci_val=nci_val,
                eq_attr=eq_attr, ps_dec=ps_dec, roll=roll, ps=ps,
                anchor_days=anchor_days, roic_term=roic_term, rr_term=rr_term,
                g=g_term, nopat_term=nopat_term,
                ps_nci_alt=ps_nci_alt, nci_alt=nci_alt,
                bear=runoff['ps'], bull=bull_var['ps'],
                ps_egystress=ps_egystress)

# ---- relative multiples lens ------------------------------------------------
peers = dict(
    ALDAR=dict(name='Aldar Properties (ADX)', pe=7.54, spot=7.78, mcap=61170.0,
               np=8800.0, rev=33800.0, ebitda=11200.0, backlog=66500.0),
    EMAAR=dict(name='Emaar Properties (DFM)', pe=5.30, spot=11.50, mcap=101650.0,
               np=None, rev=49600.0, ebitda=None, backlog=155000.0),
    EMAARDEV=dict(name='Emaar Development (DFM)', pe=4.08, spot=13.38, mcap=53520.0,
                  np=11320.0, rev=27490.0, ebitda=None, backlog=134300.0),
)
inp('peers', peers, 'Peer FY2025 fundamentals from each company\'s own results '
    'release (aldar.com 09-Feb-2026; emaar.com Feb-2026); trailing P/E and market '
    'caps cross-checked on stockanalysis.com, 07-Aug-2026 — CROSS-CHECK ONLY, '
    'labelled as such; no peer figure enters the subject\'s historicals',
    '2026-08-07', 'Industry')
pe_just = inp('pe_just', 8.0, 'Justified P/E on FY2026E attributable profit: peer '
              'trailing set 4.1-7.5x (EmaarDev/Emaar/Aldar); premium to Aldar for '
              'the recurring-income mix and backlog growth, discounted for the '
              '~15% free float and related-party revenue concentration',
              '2026-08-09', 'House')
ev_ebitda_just = inp('ev_ebitda_just', 7.0, 'Justified EV/EBITDA on FY2026E: Aldar '
                     'trailing ~5.6x (EV on net-debt-adjusted 61.2bn mcap vs 11.2bn '
                     'EBITDA); premium for growth, discount for asset heaviness',
                     '2026-08-09', 'House')
rel_pe_ps = pe_just * npa_f[0] / shares_mn
rel_ev = ev_ebitda_just * ebitda_f[0]
rel_ev_ps = (rel_ev + cash25 - debt25 - lease25 + assocbv25 + finass25 - nci_val) \
    / shares_mn
rel_base = (rel_pe_ps + rel_ev_ps) / 2
D['rel'] = dict(pe_just=pe_just, ev_ebitda_just=ev_ebitda_just,
                pe_ps=rel_pe_ps, ev_ps=rel_ev_ps, base=rel_base,
                pe_trailing=mktcap / pat25,
                ev_ebitda_trailing=(mktcap + nd25) / ebitda25,
                peers=peers)

# ---- normalised earnings power lens -----------------------------------------
norm_sales = inp('norm_sales', 18000.0, 'Through-cycle development sales: midpoint '
                 'of the base terminal-year 19,000 and the run-off tail 8,000, '
                 'weighted toward the ADREC structural-demand reading',
                 '2026-08-09', 'House')
norm_margin = inp('norm_margin', 0.115, 'Through-cycle group net margin on revenue: '
                  'FY2025 clean 10.8% (ex-fair-value/one-off), H1-2026 headline '
                  '24.0% flattered by land mix; mid-cycle 11.5%', '2026-08-09',
                  'House')
norm_rev = norm_sales * 0.85 + (seg_rev25['aim'] + seg_rev25['hosp']
                                + seg_rev25['ect']) * 1.15
norm_np = norm_rev * norm_margin
norm_eps = norm_np / shares_mn
norm_pe = inp('norm_pe', 8.5, 'Through-cycle P/E on normalised earnings, midway '
              'between Aldar trailing 7.5x and the justified 8.0x with a growth '
              'nudge', '2026-08-09', 'House')
norm_ps = norm_eps * norm_pe
D['norm'] = dict(rev=norm_rev, margin=norm_margin, np=norm_np, eps=norm_eps,
                 pe=norm_pe, base=norm_ps,
                 clean_margin_fy25=(pat25 - oneoff25 * (1 - tax_f)) / rev25)

# ---- book value & sustainable return lens -----------------------------------
bvps = eqp25 / shares_mn
roe_sust = inp('roe_sust', 0.075, 'Sustainable ROE: FY2025 attributable 4,020 on '
               'average attributable equity 51,789 = 7.8% reported; clean-basis '
               '~7.0%; forward forecast 7.3-7.6%', '2026-08-09', 'House')
pb_just = (roe_sust - g_term) / (ke - g_term)
book_ps = bvps * pb_just
D['book'] = dict(bvps=bvps, roe_sust=roe_sust, pb_just=pb_just, base=book_ps,
                 roe_fy25=npa25 / ((eqp24 + eqp25) / 2),
                 pb_trailing=mktcap / eqp25)

# ---- SOTP by segment (DCF EV decomposed on segment EBIT contribution) -------
seg_ebit_w = {k: (seg_gp25[k] - (ga25 + sm25) * seg_rev25[k] / rev25
                  * 1.0) for k in SEG}
tot_w = sum(max(v, 0.0) for v in seg_ebit_w.values())
sotp = {k: ev * max(seg_ebit_w[k], 0.0) / tot_w for k in SEG}
D['sotp'] = dict(ev_split=sotp, weights=seg_ebit_w,
                 note='group EV allocated on FY2025 segment gross profit less a '
                      'revenue-proportional share of the corporate load; the four '
                      'legs share one discount rate, with the Egypt stress case '
                      'pricing the cross-border leg separately')

# ---- lenses & weighted central ----------------------------------------------
w = inp('lens_weights', dict(dcf=0.40, relative=0.20, normalized=0.20, book=0.20),
        'DCF primary: the backlog gives unusual forward revenue visibility for a '
        'developer. Relative/normalised/book each 0.20: the peer set is cheap and '
        'liquid where MODON is tightly held, so the market lens is real evidence '
        'against the DCF, not decoration', '2026-08-09', 'House')
lens = dict(
    dcf=dict(name='Discounted cash flow (primary)', bear=runoff['ps'], base=ps,
             bull=bull_var['ps'], w=w['dcf']),
    relative=dict(name='Relative multiples', bear=rel_base * (4.08 / pe_just),
                  base=rel_base, bull=rel_base * (9.5 / pe_just), w=w['relative']),
    normalized=dict(name='Normalised earnings power',
                    bear=norm_eps * 6.0, base=norm_ps, bull=norm_eps * 10.5,
                    w=w['normalized']),
    book=dict(name='Book value and sustainable return',
              bear=bvps * (0.055 - g_term) / (ke - g_term) if True else 0,
              base=book_ps,
              bull=bvps * (0.095 - g_term) / (ke - g_term), w=w['book']),
)
central = sum(lens[k]['base'] * lens[k]['w'] for k in lens)
lo = min(lens[k]['bear'] for k in lens)
hi = max(lens[k]['bull'] for k in lens)
lens['central'] = dict(name='Weighted central', bear=lo, base=central, bull=hi, w=1.0)
D['lenses'] = lens
D['central'] = central
D['span'] = [lo, hi]
D['spot'] = spot

# panel centre for the expert appendix (median of the three expert bases, below)

# ---- sensitivity grids ------------------------------------------------------
def dcf_ps_for(wacc_x=None, g_x=None, beta_x=None, margin_shift=0.0,
               conv_shift=0.0, nwc_add=0.0, sales_mult=1.0, ke_add=0.0):
    b = beta if beta_x is None else beta_x
    ke_x = rf_star + b * erp_rating + ke_add
    wx = we * ke_x + wd * kd_at if wacc_x is None else wacc_x
    gx = g_term if g_x is None else g_x
    wtx = (1 - wd_term) * ke_x + wd_term * kd_term * (1 - tax_f) \
        if wacc_x is None else wacc_x
    dfx = [(1 + wx) ** -(t + 1) for t in range(NY)]
    bl_v = dev_backlog
    fcffs, ebits = [], []
    a2, h2, e2 = seg_rev25['aim'], seg_rev25['hosp'], seg_rev25['ect']
    for t in range(NY):
        cv = min(max(conv_path[t] + conv_shift, 0.05), 0.6)
        dr = cv * bl_v
        bl_v = bl_v + new_sales[t] * sales_mult - dr
        rr = dr + land_rev[t]
        a2 *= (1 + aim_growth[t]); h2 *= (1 + hosp_growth[t]); e2 *= (1 + ect_growth[t])
        rv = rr + a2 + h2 + e2 + oth_rev_f
        gpv = rr * (red_margin[t] + margin_shift) + a2 * aim_margin[t] \
            + h2 * hosp_margin[t] + e2 * ect_margin[t] + oth_gp_f
        eb = gpv - ga_pct[t] * rv - sm_pct[t] * rv + invinc_f[t]
        fcffs.append(eb * (1 - tax_f) + dna_pct * rv - capex_f[t]
                     + nwc_release[t] + nwc_add)
        ebits.append(eb)
    rrx = gx / roic_term
    tvx = ebits[-1] * (1 - tax_f) * (1 + gx) * (1 - rrx) / max(wtx - gx, 0.005)
    evx = sum(f * d for f, d in zip(fcffs, dfx)) + tvx * dfx[-1]
    return (evx + cash25 - debt25 - lease25 + assocbv25 + finass25 - nci_val) \
        / shares_mn * (1 + ke_x) ** (anchor_days / 365.0)


g_grid = [0.015, 0.02, 0.025, 0.03, 0.035]
wacc_grid = [wacc - 0.01, wacc - 0.005, wacc, wacc + 0.005, wacc + 0.01]
sens_wg = [[dcf_ps_for(wacc_x=wx, g_x=gx) for gx in g_grid] for wx in wacc_grid]
beta_grid = [0.8, 0.9, 1.0, 1.1, 1.2]
grid_beta = [dcf_ps_for(beta_x=b) for b in beta_grid]
mg_grid = [-0.04, -0.02, 0.0, 0.02, 0.04]
grid_margin = [dcf_ps_for(margin_shift=m) for m in mg_grid]
conv_grid = [-0.06, -0.03, 0.0, 0.03, 0.06]
grid_conv = [dcf_ps_for(conv_shift=c) for c in conv_grid]
sales_grid = [0.5, 0.75, 1.0, 1.25, 1.5]
grid_sales = [dcf_ps_for(sales_mult=s) for s in sales_grid]
nwc_grid = [-1000.0, -500.0, 0.0, 500.0, 1000.0]
grid_nwc = [dcf_ps_for(nwc_add=n) for n in nwc_grid]
ke_grid = [0.0, 0.005, 0.01, 0.015, 0.02]
grid_ke = [dcf_ps_for(ke_add=k) for k in ke_grid]
D['sens'] = dict(g_grid=g_grid, wacc_grid=wacc_grid, table=sens_wg,
                 beta_grid=beta_grid, grid_beta=grid_beta,
                 mg_grid=mg_grid, grid_margin=grid_margin,
                 conv_grid=conv_grid, grid_conv=grid_conv,
                 sales_grid=sales_grid, grid_sales=grid_sales,
                 nwc_grid=nwc_grid, grid_nwc=grid_nwc,
                 ke_grid=ke_grid, grid_ke=grid_ke)
A(abs(dcf_ps_for() - ps) < 0.02, 'sensitivity engine reproduces the base DCF at '
  'the unshifted point')

# ---- experts ----------------------------------------------------------------
# Expert 1 — asset/NAV: land bank + investment portfolio at appraisal logic
land_uplift = inp('e1_land_uplift', 0.35, 'Expert 1 marks the at-cost land bank '
                  '(26,611 land plots) up 35%: 2025 realised land sales carried a '
                  '67% gross margin on related-party pricing; an arms-length '
                  'haircut halves that', '2026-08-09', 'House')
land_bv = inp('land_bv', 26610.771, 'Land plots at cost inside inventories, note 19, '
              + FS25, '2026-02-18', 'Company')
e1_nav = eqp25 + land_bv * land_uplift + dwip25 * 0.15
e1_ps = e1_nav / shares_mn
e1 = dict(method_short='asset value (RNAV)', base=e1_ps,
          rng=[e1_nav * 0.85 / shares_mn, e1_nav * 1.12 / shares_mn],
          nav=e1_nav, land_bv=land_bv, uplift=land_uplift,
          dwip_uplift=0.15, eqp=eqp25)
# Expert 2 — cash-quality skeptic: run-off DCF + related-party receivable haircut
e2_hair = inp('e2_rp_haircut', 0.25, 'Expert 2 haircuts the AED 7.9bn net '
              'related-party receivable book 25% for timing/collection on '
              'non-arms-length land sales (H1-2026: 5.4bn further build-up, '
              'negative operating cash flow)', '2026-08-09', 'House')
e2_ps = runoff['ps'] - e2_hair * duefr25 / shares_mn
e2 = dict(method_short='owner cash flow, run-off basis', base=e2_ps,
          rng=[e2_ps * 0.8, ps * 0.95],
          runoff_ps=runoff['ps'], haircut=e2_hair, rp_book=duefr25)
# Expert 3 — market pricer: peer multiple convergence
e3_pe = inp('e3_pe', 6.5, 'Expert 3 prices MODON at the peer-set centre (Aldar 7.5x, '
            'Emaar 5.3x, EmaarDev 4.1x): a government developer earns the sector '
            'multiple, not a premium, once the growth premium is competed away',
            '2026-08-09', 'House')
e3_ps = e3_pe * npa_f[0] / shares_mn
e3 = dict(method_short='peer-multiple convergence', base=e3_ps,
          rng=[4.08 * npa_f[0] / shares_mn, 8.5 * npa_f[0] / shares_mn],
          pe=e3_pe, npa26=npa_f[0])
D['experts'] = dict(e1=e1, e2=e2, e3=e3)
panel_centre = sorted([e1_ps, e2_ps, e3_ps])[1]
D['panel_centre'] = panel_centre

# ---- what the spot implies: solve the Ke adder that prices MODON at 2.83 ----
lo_k, hi_k = 0.0, 0.20
for _ in range(60):
    mid = (lo_k + hi_k) / 2
    if dcf_ps_for(ke_add=mid) > spot:
        lo_k = mid
    else:
        hi_k = mid
implied_ke_add = (lo_k + hi_k) / 2
D['market_implied'] = dict(
    ke_add=implied_ke_add, ke=ke + implied_ke_add,
    note='the cost-of-equity adder that reconciles the base-path DCF to the market '
         'price — one honest reading of the spot is the base cash flows at a deep '
         'related-party/execution risk premium')

# ---- terminal reconciliation ------------------------------------------------
D['terminal_recon'] = dict(
    roic_fy25=nopat25_clean / ic25,
    roic_path=roic_f, roic_term=roic_term, rr_term=rr_term,
    implied_reinvest=[(capex_f[t] - dna_f[t] + dnwc_f[t]) / nopat_f[t]
                      for t in range(NY)],
    note='FY2025 clean ROIC on invested capital (equity + NCI + debt - cash) is '
         f'{nopat25_clean / ic25:.1%}; the terminal 8.5% sits above it because the '
         'at-cost land bank inside invested capital converts to recognised profit '
         'across the explicit window')

# ---- external results: step0 / strike / technicals --------------------------
with open(os.path.join(HERE, 'step0_result.json')) as f:
    D['step0'] = json.load(f)
with open(os.path.join(HERE, 'strike_result.json')) as f:
    D['strike'] = json.load(f)
with open(os.path.join(HERE, 'tech_read.json')) as f:
    D['tech'] = json.load(f)
A(D['step0']['verdict'] == 'PASS', 'Step 0 calibration verdict PASS carried into '
  'the study')
A(abs(D['strike']['spot'] - spot) < 1e-9, 'strike anchor equals the study spot')
A(D['strike']['q_annual'] == 0.0, 'q=0 sourced (no dividend paid or proposed)')

# ---- inputs validation: four-field completeness ------------------------------
for k, v in INP.items():
    assert set(v.keys()) == {'value', 'source', 'date', 'ring'}, k
    assert v['source'] and v['date'] and v['ring'], f'orphan field on {k}'
D['inputs'] = INP
A(len(INP) >= 100, f'input register carries {len(INP)} four-field inputs')

D['assert_log'] = assert_log
with open(OUT, 'w') as f:
    json.dump(D, f, indent=1)

print(f"inputs: {len(INP)} | asserts passed: {len(assert_log)}")
print(f"WACC {wacc:.3%} (Ke {ke:.3%}, Kd {kd:.3%}, wd {wd:.1%}) | term {wacc_term:.3%}")
print(f"rev path: {[round(r) for r in rev_f]}")
print(f"EBITDA path: {[round(e) for e in ebitda_f]}")
print(f"FCFF path: {[round(x) for x in fcff_f]}")
print(f"EV {ev:,.0f} | TV share {tv_share:.1%} | eq_attr {eq_attr:,.0f}")
print(f"DCF ps {ps:.2f} (dec {ps_dec:.2f}, roll {roll:.4f}) | run-off {runoff['ps']:.2f} "
      f"| bull {bull_var['ps']:.2f} | Egypt-stress {ps_egystress:.2f}")
print(f"lenses: rel {rel_base:.2f} | norm {norm_ps:.2f} | book {book_ps:.2f}")
print(f"CENTRAL {central:.2f} vs spot {spot} ({central / spot - 1:+.1%}) | "
      f"span [{lo:.2f}, {hi:.2f}] | experts {e1_ps:.2f}/{e2_ps:.2f}/{e3_ps:.2f}")
