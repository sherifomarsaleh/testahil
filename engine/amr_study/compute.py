"""AMR (Americana Restaurants International PLC) — the single computation.

Every financial numeral in this study is registered here, four fields complete
(value / source / date / research layer), and every downstream builder — Word,
Excel, bibliography, figures — reads study_numbers.json and nothing else. No
financial numeral is typed into a builder.

Historicals come exclusively from the company's own audited consolidated
financial statements and its own investor materials. Peer figures are a
cross-check and are labelled as such wherever they appear.
"""
import json, os, sys
from math import isclose

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

LOG, ASSERTS = [], []


def log(msg):
    LOG.append(msg)
    print(msg)


def chk(name, cond, detail=''):
    ASSERTS.append(dict(check=name, passed=bool(cond), detail=detail))
    if not cond:
        raise AssertionError(f'{name}: {detail}')


# ============================================================================
# 1. THE INPUT REGISTER — every input, four fields, grouped by research layer
# ============================================================================
FS25 = ('Audited consolidated financial statements for the year ended 31 December 2025, '
        'Americana Restaurants International PLC, audited by Deloitte & Touche (M.E.) LLP, '
        'signed 6 February 2026, published on the company investor-relations site')
FS24 = ('Audited consolidated financial statements for the year ended 31 December 2024, '
        'Americana Restaurants International PLC, audited by Deloitte & Touche (M.E.) LLP, '
        'published on the company investor-relations site')
FS23 = ('Audited consolidated financial statements for the year ended 31 December 2023, '
        'Americana Restaurants International PLC, published on the company '
        'investor-relations site')
IH26 = ('Reviewed condensed consolidated interim financial statements for the six months '
        'ended 30 June 2026, Americana Restaurants International PLC, review report by '
        'Deloitte & Touche (M.E.) LLP dated 28 July 2026')
IQ26 = ('Reviewed condensed consolidated interim financial statements for the three months '
        'ended 31 March 2026, Americana Restaurants International PLC')
IR25 = ('FY 2025 earnings presentation, Americana Restaurants International PLC, '
        'published 9 February 2026')
IR26 = ('H1 2026 earnings presentation, Americana Restaurants International PLC, '
        'published 28 July 2026')
IR24 = ('FY 2024 earnings presentation, Americana Restaurants International PLC, '
        'published 13 February 2025')
PR26 = ('H1 2026 earnings press release, Americana Restaurants International PLC, '
        '28 July 2026')
DAM = ('Country default spreads and risk premiums, Aswath Damodaran (NYU Stern), '
       'ctrypremJuly26 data file, published 15 July 2026, read from the original file — the '
       'edition current at the anchor date, adopted in the critique-response round in place '
       'of the January 2026 vintage used at first delivery')
IMF = ('IMF World Economic Outlook, retrieved through the IMF DataMapper API, '
       '9 August 2026')

I = {}


def inp(key, value, source, date, layer):
    I[key] = dict(value=value, source=source, date=date, layer=layer)
    return value


# ---- Market layer ----------------------------------------------------------
SPOT_AED = inp('spot_aed', 2.23,
               'Closing price on the Abu Dhabi Securities Exchange, 7 August 2026 '
               '(open 2.26, high 2.26, low 2.21), from the daily price history used '
               'throughout this study', '2026-08-07', 'Market')
AEDUSD = inp('aed_usd_peg', 3.6725,
             'The UAE dirham has been pegged to the US dollar at 3.6725 since 1997; the peg '
             'is the conversion used between the traded price and the reporting currency',
             '2026-08-07', 'Country')
SPOT = SPOT_AED / AEDUSD

SH_ISSUED = inp('shares_issued_mn', 8423.6331,
                FS25 + ', note 17: authorised, issued and paid-up capital of USD 168,473 '
                'thousand comprising 8,423,633,100 shares of USD 0.02 par value',
                '2025-12-31', 'Company')
SH_TREASURY = inp('shares_treasury_mn', 25.0,
                  FS25 + ', note 17: 25,000,000 treasury shares held against a consideration '
                  'of USD 16,749 thousand (USD 0.67 per share) for the long-term incentive plan',
                  '2025-12-31', 'Company')
SH = SH_ISSUED - SH_TREASURY

# ---- Company layer: income statement, three audited years ------------------
REV = [inp('rev_fy23', 2413.134, FS23 + ', consolidated statement of profit or loss',
           '2023-12-31', 'Company'),
       inp('rev_fy24', 2196.751, FS24 + ', consolidated statement of income',
           '2024-12-31', 'Company'),
       inp('rev_fy25', 2508.821, FS25 + ', consolidated statement of profit or loss',
           '2025-12-31', 'Company')]
COGS = [inp('cogs_fy23', 1151.575, FS23 + ', consolidated statement of profit or loss',
            '2023-12-31', 'Company'),
        inp('cogs_fy24', 1029.357, FS24 + ', consolidated statement of income',
            '2024-12-31', 'Company'),
        inp('cogs_fy25', 1143.928, FS25 + ', consolidated statement of profit or loss',
            '2025-12-31', 'Company')]
SM = [inp('sm_fy23', 777.339, FS23, '2023-12-31', 'Company'),
      inp('sm_fy24', 784.704, FS24, '2024-12-31', 'Company'),
      inp('sm_fy25', 886.102, FS25, '2025-12-31', 'Company')]
GA = [inp('ga_fy23', 191.770, FS23, '2023-12-31', 'Company'),
      inp('ga_fy24', 184.744, FS24, '2024-12-31', 'Company'),
      inp('ga_fy25', 202.562, FS25, '2025-12-31', 'Company')]
OTHINC = [inp('othinc_fy23', 16.720, FS23, '2023-12-31', 'Company'),
          inp('othinc_fy24', 7.461, FS24, '2024-12-31', 'Company'),
          inp('othinc_fy25', 13.361, FS25, '2025-12-31', 'Company')]
HYPER = [inp('hyper_fy23', -4.379, FS23 + ', monetary loss from hyperinflation (Lebanon)',
             '2023-12-31', 'Company'),
         inp('hyper_fy24', 0.125, FS24 + ', monetary gain from hyperinflation',
             '2024-12-31', 'Company'),
         inp('hyper_fy25', -1.052, FS25 + ', monetary loss from hyperinflation',
             '2025-12-31', 'Company')]
IMP_NF = [inp('imp_nf_fy23', 0.628, FS23 + ', impairment losses on non-financial assets',
              '2023-12-31', 'Company'),
          inp('imp_nf_fy24', 12.631, FS24, '2024-12-31', 'Company'),
          inp('imp_nf_fy25', 5.559, FS25, '2025-12-31', 'Company')]
IMP_F = [inp('imp_f_fy23', 1.758, FS23 + ', impairment losses on financial assets',
             '2023-12-31', 'Company'),
         inp('imp_f_fy24', 1.093, FS24, '2024-12-31', 'Company'),
         inp('imp_f_fy25', 0.251, FS25, '2025-12-31', 'Company')]
FVD = [inp('fv_deriv_fy23', -11.331, FS23 + ', fair value losses on derivative assets',
           '2023-12-31', 'Company'), 0.0, 0.0]
OPPROF = [inp('opprofit_fy23', 291.074, FS23, '2023-12-31', 'Company'),
          inp('opprofit_fy24', 191.808, FS24, '2024-12-31', 'Company'),
          inp('opprofit_fy25', 282.728, FS25, '2025-12-31', 'Company')]
FININC = [inp('fininc_fy23', 15.312, FS23 + ', note 27', '2023-12-31', 'Company'),
          inp('fininc_fy24', 16.116, FS24 + ', note 27', '2024-12-31', 'Company'),
          inp('fininc_fy25', 15.508, FS25 + ', note 25', '2025-12-31', 'Company')]
FINCOST = [inp('fincost_fy23', 31.014, FS23 + ', note 27', '2023-12-31', 'Company'),
           inp('fincost_fy24', 35.793, FS24 + ', note 27', '2024-12-31', 'Company'),
           inp('fincost_fy25', 44.135, FS25 + ', note 25', '2025-12-31', 'Company')]
LEASE_INT = [inp('lease_int_fy23', 26.625, FS23 + ', note 27: finance costs on lease liabilities',
                 '2023-12-31', 'Company'),
             inp('lease_int_fy24', 32.319, FS24 + ', note 27', '2024-12-31', 'Company'),
             inp('lease_int_fy25', 40.867, FS25 + ', note 25', '2025-12-31', 'Company')]
PBT = [inp('pbt_fy23', 275.372, FS23, '2023-12-31', 'Company'),
       inp('pbt_fy24', 172.131, FS24, '2024-12-31', 'Company'),
       inp('pbt_fy25', 254.101, FS25, '2025-12-31', 'Company')]
TAX = [inp('tax_fy23', 13.041, FS23 + ', note 30', '2023-12-31', 'Company'),
       inp('tax_fy24', 20.727, FS24 + ', note 30', '2024-12-31', 'Company'),
       inp('tax_fy25', 35.651, FS25 + ', note 28, including USD 14,040 thousand of domestic '
           'minimum top-up tax under the OECD Pillar Two rules', '2025-12-31', 'Company')]
PAT = [inp('pat_fy23', 262.331, FS23, '2023-12-31', 'Company'),
       inp('pat_fy24', 151.404, FS24, '2024-12-31', 'Company'),
       inp('pat_fy25', 218.450, FS25, '2025-12-31', 'Company')]
PATSH = [inp('patsh_fy23', 259.466, FS23 + ', profit attributable to shareholders',
             '2023-12-31', 'Company'),
         inp('patsh_fy24', 158.759, FS24, '2024-12-31', 'Company'),
         inp('patsh_fy25', 219.123, FS25, '2025-12-31', 'Company')]
DNA = [inp('dna_fy23', 252.497, FS23 + ', note 26', '2023-12-31', 'Company'),
       inp('dna_fy24', 278.153, FS24 + ', note 26', '2024-12-31', 'Company'),
       inp('dna_fy25', 307.066, FS25 + ', note 24', '2025-12-31', 'Company')]
ROU_DEP = [inp('rou_dep_fy23', 172.701, FS23 + ', note 26', '2023-12-31', 'Company'),
           inp('rou_dep_fy24', 183.810, FS24 + ', note 26', '2024-12-31', 'Company'),
           inp('rou_dep_fy25', 205.566, FS25 + ', note 24', '2025-12-31', 'Company')]

# ---- Company layer: balance sheet ------------------------------------------
PPE = [inp('ppe_fy23', 327.220, FS24 + ', comparative column', '2023-12-31', 'Company'),
       inp('ppe_fy24', 328.761, FS24, '2024-12-31', 'Company'),
       inp('ppe_fy25', 341.405, FS25, '2025-12-31', 'Company')]
ROU = [inp('rou_fy23', 498.503, FS24 + ', comparative column', '2023-12-31', 'Company'),
       inp('rou_fy24', 566.054, FS24, '2024-12-31', 'Company'),
       inp('rou_fy25', 610.822, FS25, '2025-12-31', 'Company')]
INTANG = [inp('intang_fy23', 67.424, FS24 + ', comparative column', '2023-12-31', 'Company'),
          inp('intang_fy24', 59.201, FS24, '2024-12-31', 'Company'),
          inp('intang_fy25', 63.312, FS25, '2025-12-31', 'Company')]
INVPROP = [inp('invprop_fy23', 4.821, FS24 + ', comparative column', '2023-12-31', 'Company'),
           inp('invprop_fy24', 3.356, FS24, '2024-12-31', 'Company'),
           inp('invprop_fy25', 3.712, FS25, '2025-12-31', 'Company')]
INVENT = [inp('invent_fy23', 155.593, FS24 + ', comparative column', '2023-12-31', 'Company'),
          inp('invent_fy24', 134.399, FS24, '2024-12-31', 'Company'),
          inp('invent_fy25', 155.080, FS25, '2025-12-31', 'Company')]
RECV = [inp('recv_fy23', 109.332, FS24 + ', trade and other receivables, current',
            '2023-12-31', 'Company'),
        inp('recv_fy24', 110.421, FS24, '2024-12-31', 'Company'),
        inp('recv_fy25', 128.007, FS25, '2025-12-31', 'Company')]
PAYABLES = [inp('payables_fy23', 434.206 + 13.894 + 21.021 + 18.248, FS24 +
                ', trade and other payables (current) 434,206 + income tax, zakat and other '
                'deductions payable 13,894 + provisions for legal, tax and other claims 21,021 '
                '+ due to related parties 18,248 — the aggregate the company itself reports as '
                '"payables" in its working-capital disclosure', '2023-12-31', 'Company'),
            inp('payables_fy24', 392.038 + 17.854 + 17.141 + 13.262, FS24 + ', same aggregation',
                '2024-12-31', 'Company'),
            inp('payables_fy25', 462.599 + 36.745 + 15.077 + 16.681, FS25 + ', same aggregation; '
                'ties to the USD 531 million payables figure and the USD (248) million net '
                'working capital shown in ' + IR26, '2025-12-31', 'Company')]
CASH = [inp('cash_fy23', 87.608, FS24 + ', comparative column', '2023-12-31', 'Company'),
        inp('cash_fy24', 81.470, FS24, '2024-12-31', 'Company'),
        inp('cash_fy25', 154.337, FS25, '2025-12-31', 'Company')]
DEPOSITS = [inp('deposits_fy23', 295.933, FS24 + ', short-term deposits with banks, comparative',
                '2023-12-31', 'Company'),
            inp('deposits_fy24', 213.695, FS24, '2024-12-31', 'Company'),
            inp('deposits_fy25', 145.235 + 117.838, FS25 + ', short-term deposits with banks '
                '145,235 plus long-term deposits with banks 117,838', '2025-12-31', 'Company')]
LEASE_L = [inp('lease_liab_fy23', 341.223 + 165.959, FS24 + ', comparative: non-current 341,223 '
               'plus current 165,959', '2023-12-31', 'Company'),
           inp('lease_liab_fy24', 389.241 + 189.590, FS24, '2024-12-31', 'Company'),
           inp('lease_liab_fy25', 429.297 + 208.169, FS25 + ', note 11: non-current 429,297 plus '
               'current 208,169', '2025-12-31', 'Company')]
BANK_DEBT = [inp('bank_debt_fy23', 4.375, FS24 + ', bank facilities, comparative column',
                 '2023-12-31', 'Company'),
             inp('bank_debt_fy24', 0.0, FS24 + ', no bank facilities outstanding',
                 '2024-12-31', 'Company'),
             inp('bank_debt_fy25', 0.0, FS25 + ', no interest-bearing bank borrowings are '
                 'recognised; the only finance cost on bank facilities in the year was USD 42 '
                 'thousand of commitment-type charges', '2025-12-31', 'Company')]
EQUITY = [inp('equity_fy23', 439.366, FS24 + ', equity attributable to shareholders, comparative',
              '2023-12-31', 'Company'),
          inp('equity_fy24', 394.438, FS24, '2024-12-31', 'Company'),
          inp('equity_fy25', 488.990, FS25, '2025-12-31', 'Company')]
NCI = [inp('nci_fy23', 12.014, FS24 + ', comparative', '2023-12-31', 'Company'),
       inp('nci_fy24', 3.686, FS24, '2024-12-31', 'Company'),
       inp('nci_fy25', 0.984, FS25, '2025-12-31', 'Company')]
TOTASSETS = [inp('assets_fy23', 1556.859, FS24 + ', comparative', '2023-12-31', 'Company'),
             inp('assets_fy24', 1507.400, FS24, '2024-12-31', 'Company'),
             inp('assets_fy25', 1734.126, FS25, '2025-12-31', 'Company')]
EOSB = [inp('eosb_fy23', 68.561, FS24 + ', provision for employees end of service benefits',
            '2023-12-31', 'Company'),
        inp('eosb_fy24', 68.375, FS24, '2024-12-31', 'Company'),
        inp('eosb_fy25', 70.745, FS25, '2025-12-31', 'Company')]

# ---- Company layer: cash flow ----------------------------------------------
CAPEX_PPE = [inp('capex_ppe_fy23', 127.658, FS24 + ', consolidated statement of cash flows, '
                 'comparative', '2023-12-31', 'Company'),
             inp('capex_ppe_fy24', 106.606, FS24, '2024-12-31', 'Company'),
             inp('capex_ppe_fy25', 94.881, FS25, '2025-12-31', 'Company')]
CAPEX_INT = [inp('capex_intang_fy23', 18.232, FS24 + ', comparative', '2023-12-31', 'Company'),
             inp('capex_intang_fy24', 17.199, FS24, '2024-12-31', 'Company'),
             inp('capex_intang_fy25', 12.215, FS25, '2025-12-31', 'Company')]
CAPEX_KEY = [inp('capex_keymoney_fy23', 3.929, FS24 + ', payments for key money, comparative',
                 '2023-12-31', 'Company'),
             inp('capex_keymoney_fy24', 0.504, FS24, '2024-12-31', 'Company'),
             inp('capex_keymoney_fy25', 1.680, FS25, '2025-12-31', 'Company')]
CFO = [inp('cfo_fy23', 539.787, FS24 + ', net cash generated from operating activities, comparative',
           '2023-12-31', 'Company'),
       inp('cfo_fy24', 432.801, FS24, '2024-12-31', 'Company'),
       inp('cfo_fy25', 588.997, FS25, '2025-12-31', 'Company')]
LEASE_PRIN = [inp('lease_principal_fy23', 173.513, FS24 + ', lease payments, principal element, '
                  'comparative', '2023-12-31', 'Company'),
              inp('lease_principal_fy24', 179.598, FS24, '2024-12-31', 'Company'),
              inp('lease_principal_fy25', 192.405, FS25, '2025-12-31', 'Company')]
ROU_ADD = [inp('rou_additions_fy23', 0.0, 'Not separately disclosed in the FY2023 filing; the '
               'right-of-use roll-forward for FY2024 and FY2025 is used instead',
               '2023-12-31', 'Company'),
           inp('rou_additions_fy24', 279.400, FS24 + ', note 12, additions to right-of-use assets',
               '2024-12-31', 'Company'),
           inp('rou_additions_fy25', 255.162, FS25 + ', note 11, additions to right-of-use assets',
               '2025-12-31', 'Company')]
DIVPAID = [inp('div_paid_fy23', 103.312, FS24 + ', dividends paid to shareholders, comparative',
               '2023-12-31', 'Company'),
           inp('div_paid_fy24', 179.424, FS24, '2024-12-31', 'Company'),
           inp('div_paid_fy25', 126.987, FS25, '2025-12-31', 'Company')]
DIV_FY25_DECL = inp('div_fy25_declared', 201.6,
                    IR25 + ': cash dividends of USD 201.6 million for FY2025, 91.99% of net '
                    'profit, subject to approval at the annual general meeting',
                    '2026-02-09', 'Company (investor relations)')
DIV_H1_26 = inp('div_h1_26_interim', 100.8,
                PR26 + ': interim cash dividend of USD 100.8 million, USD 0.012 per share, '
                'approved by the board for the period ended 30 June 2026',
                '2026-07-28', 'Company (investor relations)')

# ---- Company layer: 2026 interims (both disclosed quarters) ----------------
REV_H1_26 = inp('rev_h1_26', 1364.520, IH26 + ', condensed consolidated interim statement of '
                'profit or loss', '2026-06-30', 'Company')
REV_H1_25 = inp('rev_h1_25', 1216.969, IH26 + ', comparative period', '2025-06-30', 'Company')
REV_Q1_26 = inp('rev_q1_26', 649.736, IQ26 + ', three months ended 31 March 2026 '
                '(1,364,520 less the 714,784 reported for the three months ended 30 June 2026)',
                '2026-03-31', 'Company')
REV_Q2_26 = inp('rev_q2_26', 714.784, IH26 + ', three-month period ended 30 June 2026',
                '2026-06-30', 'Company')
COGS_H1_26 = inp('cogs_h1_26', 598.498, IH26, '2026-06-30', 'Company')
SM_H1_26 = inp('sm_h1_26', 479.601, IH26, '2026-06-30', 'Company')
GA_H1_26 = inp('ga_h1_26', 109.239, IH26, '2026-06-30', 'Company')
OP_H1_26 = inp('opprofit_h1_26', 184.120, IH26, '2026-06-30', 'Company')
DNA_H1_26 = inp('dna_h1_26', 161.218, IH26 + ', note 20 segment disclosure', '2026-06-30', 'Company')
IMPNF_H1_26 = inp('imp_nf_h1_26', 2.141, IH26, '2026-06-30', 'Company')
IMPF_H1_26 = inp('imp_f_h1_26', 0.735, IH26, '2026-06-30', 'Company')
PBT_H1_26 = inp('pbt_h1_26', 171.084, IH26, '2026-06-30', 'Company')
TAX_H1_26 = inp('tax_h1_26', 24.101, IH26, '2026-06-30', 'Company')
PATSH_H1_26 = inp('patsh_h1_26', 147.221, IH26, '2026-06-30', 'Company')
EBITDA_H1_26 = inp('ebitda_h1_26', 348.214, IR26 + ', EBITDA to net profit reconciliation; '
                   'independently reproduced here as operating profit 184,120 plus depreciation '
                   'and amortisation 161,218 plus impairments 2,141 and 735',
                   '2026-06-30', 'Company (investor relations)')
LEASE_L_H1_26 = inp('lease_liab_h1_26', 421.451 + 220.107, IH26 + ', non-current 421,451 plus '
                    'current 220,107', '2026-06-30', 'Company')
CASH_H1_26 = inp('cash_h1_26', 140.186, IH26, '2026-06-30', 'Company')
DEP_H1_26 = inp('deposits_h1_26', 220.728 + 22.195, IH26 + ', short-term deposits with banks '
                '220,728 plus investments in financial assets 22,195', '2026-06-30', 'Company')
EQ_H1_26 = inp('equity_h1_26', 435.133, IH26, '2026-06-30', 'Company')
LFL_H1_26 = inp('lfl_h1_26', 0.063, PR26 + ': like-for-like sales growth of 6.3% in the first '
                'half of 2026', '2026-06-30', 'Company (investor relations)')
LFL_FY25 = inp('lfl_fy25', 0.097, IR25 + ': like-for-like sales growth of 9.7% for FY2025',
               '2025-12-31', 'Company (investor relations)')

# ---- Company layer: the unit build (stores by country, revenue by country) --
UNITS = ['UAE', 'Saudi Arabia', 'Kuwait', 'Egypt', 'Morocco', 'Lower Gulf', 'Other markets']
UNIT_NOTE = {
    'UAE': 'disclosed separately in the segment note',
    'Saudi Arabia': 'disclosed separately in the segment note',
    'Kuwait': 'disclosed separately in the segment note',
    'Egypt': 'disclosed separately in the segment note',
    'Morocco': 'North Africa segment revenue less the separately disclosed Egypt revenue',
    'Lower Gulf': 'Qatar, Oman and Bahrain — a disclosed reportable segment',
    'Other markets': 'Kazakhstan, Iraq, Lebanon and Jordan — a disclosed reportable segment',
}
GEO_SRC = (FS25 + ', note 33: revenue before eliminations for the significant geographical '
           'locations and the four reportable segments; ' + FS24 + ', note 35, for the '
           'FY2024 and FY2023 columns')
STORE_SRC = {2023: 'Store counts by country are not published for 31 December 2023; the FY2023 '
                   'column of the unit build is therefore carried at segment level only',
             2024: IR24 + ', portfolio evolution appendix: restaurant count by country at '
                   '31 December 2024',
             2025: IR25 + ', portfolio evolution appendix: restaurant count by country at '
                   '31 December 2025',
             2026: IR26 + ', portfolio evolution appendix: restaurant count by country at '
                   '30 June 2026'}

REV_UNIT = {  # USD million, before intercompany eliminations
    'UAE':           [750.972, 748.814, 844.653],
    'Saudi Arabia':  [594.518, 582.984, 629.910],
    'Kuwait':        [339.181, 305.950, 346.969],
    'Egypt':         [195.018, 133.371, 172.557],
    'Morocco':       [42.806, 41.352, 50.679],
    'Lower Gulf':    [278.081, 194.201, 257.901],
    'Other markets': [249.264, 214.315, 238.075],
}
for u, v in REV_UNIT.items():
    for yr, val in zip((23, 24, 25), v):
        inp(f'rev_unit_{u.lower().replace(" ", "_")}_fy{yr}', val, GEO_SRC + f' — {UNIT_NOTE[u]}',
            f'20{yr}-12-31', 'Company')

STORES_UNIT = {   # restaurant count at each year end
    'UAE':           [605, 652, 664],
    'Saudi Arabia':  [734, 766, 761],
    'Kuwait':        [262, 276, 274],
    'Egypt':         [453, 450, 447],
    'Morocco':       [45, 55, 56],
    'Lower Gulf':    [250, 287, 279],     # Qatar + Oman + Bahrain
    'Other markets': [241, 263, 265],     # Kazakhstan + Iraq + Lebanon + Jordan
}
for u, v in STORES_UNIT.items():
    for yr, val, lab in zip((24, 25, 26), v, ('2024-12-31', '2025-12-31', '2026-06-30')):
        inp(f'stores_{u.lower().replace(" ", "_")}_{lab[:7]}', val,
            STORE_SRC[int(lab[:4])] + f' — {UNIT_NOTE[u]}', lab, 'Company (investor relations)')

STORES_TOT = [inp('stores_total_2024', 2590, STORE_SRC[2024], '2024-12-31',
                  'Company (investor relations)'),
              inp('stores_total_2025', 2749, STORE_SRC[2025], '2025-12-31',
                  'Company (investor relations)'),
              inp('stores_total_h1_26', 2746, STORE_SRC[2026], '2026-06-30',
                  'Company (investor relations)')]
NSO_GUIDE_LO = inp('nso_guidance_low', 120, IR26 + ' and ' + PR26 + ': the company expects to '
                   'add 120 to 130 net new stores in 2026', '2026-07-28',
                   'Company (investor relations)')
NSO_GUIDE_HI = inp('nso_guidance_high', 130, IR26 + ' and ' + PR26, '2026-07-28',
                   'Company (investor relations)')
CAPEX_PER_STORE = inp('capex_per_store_k', 402.0, IR26 + ', key metrics by restaurant: average '
                      'capital expenditure per restaurant of USD 402 thousand across 356 gross '
                      'openings from 1 April 2024 to 31 March 2026, with an average payback of '
                      '3.0 years', '2026-06-30', 'Company (investor relations)')
GROSS_OPEN_25 = inp('gross_openings_fy25', 170, IR25 + ': 170 gross organic openings in FY2025 '
                    '(a further 46 arrived with the Pizza Hut Oman acquisition)',
                    '2025-12-31', 'Company (investor relations)')

# ---- Company layer: the cost stack, by driver class ------------------------
COST_SRC25 = FS25 + ', notes 21, 22 and 23'
COST_SRC24 = FS24 + ', notes 23, 24 and 25'
COST_LINES = {
    'inventory':   ([750.234, 642.034, 714.319], 'Cost of inventory — food, filling and packing '
                    'materials', 'Traded food commodity basket'),
    'royalties':   ([132.241, 121.272, 139.131], 'Royalties payable to the brand franchisors',
                    'Contractual percentage of branded food and beverage sales'),
    'staff':       ([455.612, 422.103, 461.118], 'Total staff costs across cost of revenues, '
                    'selling and marketing and general and administrative expenses',
                    'Wages in the operating countries'),
    'delivery':    ([106.202, 133.696, 180.599], 'Home delivery and transportation',
                    'Delivery-channel volume and fuel'),
    'advertising': ([113.630, 98.174, 109.177], 'Advertisement and business development',
                    'Managed percentage of sales'),
    'utilities':   ([66.752, 66.099, 71.685], 'Utilities and communication in selling and '
                    'marketing plus utilities in general and administrative expenses',
                    'Energy tariffs'),
    'rent_other':  ([50.691, 44.278, 43.598], 'Short-term, low-value and variable lease payments '
                    'outside the capitalised lease liability', 'Property rents'),
    'maintenance': ([69.637, 65.859, 72.589], 'Maintenance and other operating expenses plus '
                    'repairs and maintenance', 'Domestic services'),
}
for k, (vals, desc, drv) in COST_LINES.items():
    for yr, val in zip((23, 24, 25), vals):
        inp(f'cost_{k}_fy{yr}', val,
            (COST_SRC25 if yr == 25 else COST_SRC24) + f' — {desc}. Escalated on its own driver '
            f'class: {drv}', f'20{yr}-12-31', 'Company')
INV_PCT_H1_26 = inp('cost_inventory_pct_h1_26', 0.274,
                    IR26 + ', cost of inventory evolution: 27.4% of revenue in H1 2026 against '
                    '29.2% in H1 2025 — the disclosed, dated near-term anchor for the food '
                    'input line', '2026-06-30', 'Company (investor relations)')
INV_PCT_FY25 = inp('cost_inventory_pct_fy25', 714.319 / 2508.821, COST_SRC25 +
                   ' — cost of inventory as a share of revenue', '2025-12-31', 'Company')

STAFF_FTE = [inp('fte_fy23', 41575, FS24 + ', note 28', '2023-12-31', 'Company'),
             inp('fte_fy24', 38226, FS24 + ', note 28', '2024-12-31', 'Company'),
             inp('fte_fy25', 37207, FS25 + ', note 26: average full-time-equivalent staff count '
                 'of 37,207, of which 33,324 restaurant-level', '2025-12-31', 'Company')]

# ---- Country layer: cost of capital ----------------------------------------
UST10 = inp('ust_10y', 0.0465, 'US 10-year Treasury par yield, 4.65% at the close of 7 August '
            '2026, read from the Treasury daily par yield curve CSV (the 4.66% previously '
            'carried was a secondary-source transcription, corrected against the primary)',
            '2026-08-07', 'Country')
US_DEFAULT_SPREAD = inp('us_default_spread', 0.0022, DAM + ': United States, Moody\'s Aa1, '
                        'adjusted default spread 0.22%', '2026-07-15', 'Country')
US_CDS = inp('us_cds', 0.0043, DAM + ': United States sovereign credit default swap spread 0.43%',
             '2026-07-15', 'Country')
ADGB_SPREAD = inp('abu_dhabi_new_issue_spread', 0.0025,
                  'Abu Dhabi sovereign dual-tranche US dollar benchmark, February 2026: final '
                  're-offer spread of 25 basis points over US Treasuries on the ten-year tranche '
                  '(initial price thoughts were +55; the final pricing is the market evidence)',
                  '2026-02-01', 'Country')
UAE_DEFAULT_SPREAD = inp('uae_default_spread', 0.0042, DAM + ': United Arab Emirates, Moody\'s '
                         'Aa2, adjusted default spread 0.42%', '2026-01-05', 'Country')

ERP_RATING = {'UAE': 0.0481, 'Saudi Arabia': 0.0494, 'Kuwait': 0.0507, 'Egypt': 0.1348,
              'Morocco': 0.0730, 'Qatar': 0.0481, 'Oman': 0.0692, 'Bahrain': 0.1101,
              'Kazakhstan': 0.0618, 'Iraq': 0.1348, 'Lebanon': 0.3140, 'Jordan': 0.0865}
ERP_CDS = {'UAE': 0.0481, 'Saudi Arabia': 0.0551, 'Kuwait': 0.0540, 'Egypt': 0.0952,
           'Morocco': 0.0600, 'Qatar': 0.0490, 'Oman': 0.0589, 'Bahrain': 0.0865,
           'Kazakhstan': 0.0589, 'Iraq': 0.1000, 'Lebanon': 0.3140, 'Jordan': 0.0865}
CDS_NA = ['UAE', 'Lebanon', 'Jordan']
for c in ERP_RATING:
    inp(f'erp_rating_{c.lower().replace(" ", "_")}', ERP_RATING[c],
        DAM + f': {c}, total equity risk premium on the ratings basis', '2026-01-05', 'Country')
    inp(f'erp_cds_{c.lower().replace(" ", "_")}', ERP_CDS[c],
        DAM + f': {c}, equity risk premium on the sovereign credit-default-swap basis'
        + (' — no CDS is published for this sovereign, so the ratings-basis premium is carried '
           'here and the substitution is flagged' if c in CDS_NA else ''),
        '2026-01-05', 'Country')

# Country revenue weights: the four disclosed countries stand on their own; the two
# multi-country segments are apportioned across their members on restaurant count,
# which is the only published physical measure available at that level.
STORES_BY_COUNTRY_25 = {'Qatar': 109, 'Oman': 101, 'Bahrain': 77,
                        'Kazakhstan': 147, 'Iraq': 42, 'Lebanon': 17, 'Jordan': 57}
for c, n in STORES_BY_COUNTRY_25.items():
    inp(f'stores_{c.lower()}_2025', n, STORE_SRC[2025] + f' — {c}', '2025-12-31',
        'Company (investor relations)')

TAX_PILLAR2 = inp('pillar_two_minimum_rate', 0.15,
                  FS25 + ', note 28: the OECD Pillar Two global minimum effective rate of 15% '
                  'applies to the group, and domestic minimum top-up tax legislation was '
                  'effective at the reporting date in the United Arab Emirates, Kuwait, Qatar, '
                  'Bahrain and Oman', '2025-12-31', 'Company')
ETR25 = inp('etr_fy25', 0.14, FS25 + ', note 28: effective tax rate of 14% (2024: 11%, 2023: 4%)',
            '2025-12-31', 'Company')
ETR_H1_26 = inp('etr_h1_26', 24.101 / 171.084, IH26 + ': income tax and zakat of USD 24,101 '
                'thousand on profit before tax of USD 171,084 thousand', '2026-06-30', 'Company')

BETA = inp('beta', 0.930, 'Ordinary least squares regression of 183 complete weekly logarithmic '
           'returns of the company\'s own Abu Dhabi-listed shares against the FTSE ADX General '
           'Index — the published index of the exchange those shares trade on — over windows '
           'labelled 30 December 2022 to 17 July 2026, which is the whole life of the listing, '
           'the company having floated in December 2022. The figure carries the Dimson lead-lag '
           'correction, and both series pass the data-quality screen first. Standard error '
           '0.412, R-squared 8.4%: it clears the usability gate of at least 24 observations, '
           'R-squared of at least 5% and a standard error below the absolute coefficient, but '
           'only just, and the imprecision is the honest headline — a 90% confidence interval '
           'runs from 0.25 to 1.61, so this estimate cannot be told apart from most plausible '
           'alternatives. A Blume adjustment towards the market gives 0.953, close enough to '
           'confirm the level. The index is quoted in dirhams, the same currency the shares '
           'trade in, and strikes at the same closing auction on the same exchange. Cross-checks '
           'from earlier editions of this study, all disclosed and none adopted, and every one '
           'now known to be non-conforming: the company\'s Riyadh line against the Saudi index '
           'gave 0.894 — a different country\'s market cycle, and the input the first edition '
           'used before the Abu Dhabi index was available; an equally weighted composite of '
           'eighteen covered UAE names gave 0.586; and a US-listed UAE index fund, which prices '
           'hours after the Abu Dhabi close, gave 0.469. The composite and the fund understated '
           'the beta by roughly half. A composite is not a substitute and not a tier: it is a '
           'coverage artefact that changes whenever a stock is added, it mixes two exchanges '
           'inside one market code, and it shares its constituents with the company being '
           'priced.', '2026-08-10', 'Market')

KD = inp('cost_of_debt', 40.867 / ((578.831 + 637.466) / 2),
         'The group\'s own incremental borrowing rate, read out of its lease accounting: '
         'finance costs on lease liabilities of USD 40,867 thousand in FY2025 over the average '
         'lease liability of USD 608.1 million. Determining the incremental borrowing rate is '
         'identified as a key audit matter in the filing. This is the only borrowing cost the '
         'company actually pays — it carries no bank debt — and it sits above the Abu Dhabi '
         'sovereign, as a corporate in the same currency must.', '2025-12-31', 'Company')
KD_FY24 = inp('cost_of_debt_fy24', 32.319 / ((507.182 + 578.831) / 2),
              'The same construction on the FY2024 accounts: lease finance cost of USD 32,319 '
              'thousand over an average lease liability of USD 543.0 million',
              '2024-12-31', 'Company')

TERMINAL_G = inp('terminal_growth', 0.030,
                 'Long-run growth in US dollars. The pegged Gulf markets that produce most of '
                 'the revenue are projected by the IMF at about 2% inflation from 2028 onward, '
                 'and a mature restaurant estate can add roughly one point of real volume on '
                 'top. The figure is deliberately set far below the risk-free rate, which is '
                 'the ceiling any perpetual growth assumption has to respect. Source for the '
                 'inflation and real-growth paths: ' + IMF, '2026-08-09', 'Country')
TERMINAL_RF = inp('terminal_risk_free', 0.0445,
                  'Terminal US dollar risk-free rate: the ten-year Treasury par yield of 4.65% '
                  'less the US sovereign default spread of 0.22%, rounded to the nearest five '
                  'basis points (4.43% -> 4.45%) and held flat. The first delivery carried '
                  '4.30%, which did not follow this stated construction; corrected in the '
                  'critique-response round.', '2026-08-07', 'Country')

# ---- Industry layer --------------------------------------------------------
PEERS = json.load(open(os.path.join(HERE, 'peers.json')))
inp('peer_frame', 'see the peer table',
    PEERS['source'], PEERS['retrieved'], 'Industry')

# ============================================================================
# 2. HISTORY — every derived historical figure, from the registered inputs
# ============================================================================
YEARS_H = ['FY2023', 'FY2024', 'FY2025']
gross_profit = [REV[i] - COGS[i] for i in range(3)]
ebitda = [OPPROF[i] + DNA[i] + IMP_NF[i] + IMP_F[i] for i in range(3)]
ebit = [ebitda[i] - DNA[i] for i in range(3)]
owned_dna = [DNA[i] - ROU_DEP[i] for i in range(3)]
capex_gross = [CAPEX_PPE[i] + CAPEX_INT[i] + CAPEX_KEY[i] for i in range(3)]
nwc = [INVENT[i] + RECV[i] - PAYABLES[i] for i in range(3)]
net_debt = [LEASE_L[i] + BANK_DEBT[i] - CASH[i] - DEPOSITS[i] for i in range(3)]
eps = [PATSH[i] / SH for i in range(3)]
bvps = [EQUITY[i] / SH for i in range(3)]

chk('FY2025 EBITDA reproduces the published reconciliation',
    isclose(ebitda[2], 595.604, abs_tol=0.01),
    f'computed {ebitda[2]:.3f} against USD 595.6 million in the FY2025 earnings presentation')
chk('FY2025 gross profit ties to the filing', isclose(gross_profit[2], 1364.893, abs_tol=0.001),
    f'{gross_profit[2]:.3f}')
chk('FY2025 operating profit rebuilds from its components',
    isclose(gross_profit[2] - SM[2] - GA[2] + OTHINC[2] + HYPER[2] - IMP_NF[2] - IMP_F[2],
            OPPROF[2], abs_tol=0.002), '')
chk('FY2025 profit before tax rebuilds', isclose(OPPROF[2] + FININC[2] - FINCOST[2], PBT[2],
                                                abs_tol=0.001), '')
chk('FY2025 net working capital ties to the published figure',
    isclose(nwc[2], -248.015, abs_tol=0.02), f'{nwc[2]:.3f} against USD (248) million disclosed')
log(f'History: FY2025 revenue {REV[2]:,.1f}m, EBITDA {ebitda[2]:,.1f}m '
    f'({100*ebitda[2]/REV[2]:.1f}%), attributable profit {PATSH[2]:,.1f}m, '
    f'net working capital {nwc[2]:,.1f}m ({100*nwc[2]/REV[2]:.1f}% of revenue)')

# H1 2026 actual, the base the forecast year is anchored on
ebitda_h1_26 = OP_H1_26 + DNA_H1_26 + IMPNF_H1_26 + IMPF_H1_26
chk('H1 2026 EBITDA reproduces the published reconciliation',
    isclose(ebitda_h1_26, EBITDA_H1_26, abs_tol=0.002), f'{ebitda_h1_26:.3f}')

# ============================================================================
# 3. THE UNIT BUILD — restaurants times revenue per restaurant, by market
# ============================================================================
FY_F = ['FY2026E', 'FY2027E', 'FY2028E', 'FY2029E', 'FY2030E']

# Restaurant count at each forecast year end. Volume growth is the company's own
# net-new-store programme: the midpoint of published 2026 guidance, then a taper.
NSO_TOTAL = [125, 130, 130, 125, 120]
inp('nso_path', NSO_TOTAL,
    'Net new restaurants a year. FY2026 is the midpoint of the company\'s published guidance of '
    '120 to 130; the following years hold near that pace and taper gently as the estate matures. '
    'Source of the guidance: ' + IR26, '2026-07-28', 'Company (investor relations)')

# The net additions are allocated across markets on each market's share of the last
# twelve months' openings, proxied by its share of the estate weighted by recent growth.
NSO_MIX = {'UAE': 0.26, 'Saudi Arabia': 0.30, 'Kuwait': 0.06, 'Egypt': 0.12,
           'Morocco': 0.04, 'Lower Gulf': 0.10, 'Other markets': 0.12}
inp('nso_mix', NSO_MIX,
    'Allocation of net new restaurants across markets. Set from where the estate has actually '
    'been growing: over the eighteen months to 30 June 2026 Saudi Arabia and the UAE together '
    'took roughly 56% of net additions, and the split here holds that shape. An estimate at the '
    'allocation step only — the total is the company\'s own guidance, and the group revenue '
    'result is insensitive to the split because revenue per restaurant differs across markets by '
    'less than the growth rates do.', '2026-07-28', 'House estimate')

# Revenue per restaurant: the price side. Its growth is like-for-like sales growth,
# anchored on the disclosed H1 2026 rate and converging on local inflation.
LFL_PATH = [0.055, 0.045, 0.040, 0.037, 0.035]
inp('lfl_path', LFL_PATH,
    'Like-for-like sales growth. FY2026 is set just below the 6.3% the company actually '
    'delivered in the first half and consistent with its own guidance of mid-single-digit '
    'like-for-like growth for the full year; the path then converges toward the roughly 2% '
    'long-run inflation the IMF projects for the pegged Gulf markets plus continued menu and '
    'mix work. Sources: ' + PR26 + '; ' + IMF, '2026-08-09', 'House estimate')

# Egypt and the Other-markets segment carry the non-pegged currencies, so their revenue
# per restaurant in US dollars grows more slowly than local like-for-like sales.
FX_DRAG = {'UAE': 0.0, 'Saudi Arabia': 0.0, 'Kuwait': 0.0, 'Egypt': 0.025,
           'Morocco': 0.005, 'Lower Gulf': 0.0, 'Other markets': 0.015}
inp('fx_drag', FX_DRAG,
    'Annual drag on US dollar revenue per restaurant from currency. Zero wherever the currency '
    'is pegged to the dollar — the company reports that 83% of revenue is earned in stable '
    'pegged currencies. Egypt and the Kazakhstan-led Other-markets segment carry a drag equal to '
    'the excess of their projected inflation over US inflation, damped for the pass-through a '
    'restaurant business achieves through its own menu prices. Sources: ' + IR26 + '; ' + IMF,
    '2026-08-09', 'House estimate')

unit_hist_rev = {u: REV_UNIT[u] for u in UNITS}
unit_hist_stores = {u: STORES_UNIT[u] for u in UNITS}
# revenue per restaurant on the closing count, the only count published per market
rps_25 = {u: REV_UNIT[u][2] * 1000.0 / STORES_UNIT[u][1] for u in UNITS}
rps_24 = {u: REV_UNIT[u][1] * 1000.0 / STORES_UNIT[u][0] for u in UNITS}

stores_f, rps_f, rev_f_unit = {}, {}, {}
for u in UNITS:
    s, r, rv = [], [], []
    s_prev, r_prev = STORES_UNIT[u][1], rps_25[u]
    for t in range(5):
        s_prev = s_prev + NSO_TOTAL[t] * NSO_MIX[u]
        r_prev = r_prev * (1 + LFL_PATH[t]) * (1 - FX_DRAG[u])
        s.append(s_prev); r.append(r_prev); rv.append(s_prev * r_prev / 1000.0)
    stores_f[u], rps_f[u], rev_f_unit[u] = s, r, rv

rev_gross_f = [sum(rev_f_unit[u][t] for u in UNITS) for t in range(5)]
ELIM_PCT = inp('elimination_pct', 31.923 / 2540.744,
               FS25 + ', note 33: intercompany eliminations of USD 31,923 thousand against '
               'segment revenue before eliminations of USD 2,540,744 thousand',
               '2025-12-31', 'Company')
rev_f = [g * (1 - ELIM_PCT) for g in rev_gross_f]

chk('the unit build reproduces FY2025 revenue exactly',
    isclose(sum(REV_UNIT[u][2] for u in UNITS) * (1 - ELIM_PCT), REV[2], rel_tol=1e-9),
    f'{sum(REV_UNIT[u][2] for u in UNITS) * (1 - ELIM_PCT):.3f} against {REV[2]:.3f}')
chk('the unit build reproduces FY2024 revenue exactly',
    isclose(sum(REV_UNIT[u][1] for u in UNITS) * (1 - 24.236 / 2220.987), REV[1], rel_tol=1e-9), '')
chk('the unit build reproduces FY2023 revenue exactly',
    isclose(sum(REV_UNIT[u][0] for u in UNITS) * (1 - 36.706 / 2449.840), REV[0], rel_tol=1e-9), '')

# FY2026 is half actual. Blend: H1 disclosed, H2 from the unit build's own second-half share.
h1_share_25 = REV_H1_25 / REV[2]
inp('h1_share_of_year', h1_share_25, 'The first half produced ' + f'{100*h1_share_25:.1f}%' +
    ' of FY2025 revenue (USD 1,216.969 million of USD 2,508.821 million); the same seasonal '
    'shape carries the disclosed H1 2026 outturn to a full-year figure. Sources: ' + IH26 +
    '; ' + FS25, '2026-06-30', 'Company')
rev_2026_from_h1 = REV_H1_26 / h1_share_25
rev_f[0] = (rev_f[0] + rev_2026_from_h1) / 2.0
log(f'FY2026E revenue: unit build {rev_gross_f[0]*(1-ELIM_PCT):,.1f}m, H1 run-rate '
    f'{rev_2026_from_h1:,.1f}m, adopted {rev_f[0]:,.1f}m '
    f'({100*(rev_f[0]/REV[2]-1):+.1f}% on FY2025)')
scale26 = rev_f[0] / (rev_gross_f[0] * (1 - ELIM_PCT))
for u in UNITS:
    rev_f_unit[u][0] *= scale26

# ---- the brand build: product-by-product volume x price, reconciled -------
BRANDS = ['KFC', 'Pizza Hut', "Hardee's", 'Krispy Kreme', 'Growth, niche and other brands']
BRAND_SRC = (IR25 + ', portfolio appendix (restaurants by brand at 31 December 2025: KFC 1,146, '
             'Pizza Hut 457, Hardee\'s 458, Krispy Kreme 395, growth/niche 290, other 3) and '
             'revenue by power brand (FY2024 -> FY2025: KFC 1,325 -> 1,494, Pizza Hut 367 -> '
             '433, Hardee\'s 275 -> 330, Krispy Kreme 87 -> 94); ' + IR24 +
             ' for the 31 December 2024 brand estate; ' + IR26 + ' for 30 June 2026')
BRAND_STORES_24 = [1089, 432, 410, 388, 271]
BRAND_STORES_25 = [1146, 457, 458, 395, 293]
BRAND_STORES_H1 = [1144, 459, 446, 395, 302]
BRAND_REV_24 = [1325.0, 367.0, 275.0, 87.0, REV[1] - 2054.0]
BRAND_REV_25 = [1494.0, 433.0, 330.0, 94.0, REV[2] - 2351.0]
BRAND_LFL_25 = [0.093, 0.126, 0.112, 0.069, None]
BRAND_NSO_MIX = [0.40, 0.15, 0.16, 0.12, 0.17]
inp('brand_build', dict(brands=BRANDS, stores_2024=BRAND_STORES_24, stores_2025=BRAND_STORES_25,
                        stores_h1_2026=BRAND_STORES_H1, revenue_2024=BRAND_REV_24,
                        revenue_2025=BRAND_REV_25, lfl_2025=BRAND_LFL_25,
                        nso_mix=BRAND_NSO_MIX),
    BRAND_SRC + '. The residual brand revenue is total audited revenue less the four disclosed '
    'power brands, so the brand build ties to the audited total by construction in both years. '
    'The opening mix is the company\'s own new-restaurant pie (KFC 40%, Hardee\'s 16%, Pizza '
    'Hut 15%, Krispy Kreme 12%, other 17%).', '2026-02-09', 'Company (investor relations)')
chk('the brand build ties to audited revenue in both disclosed years',
    isclose(sum(BRAND_REV_25), REV[2], abs_tol=0.01) and isclose(sum(BRAND_REV_24), REV[1],
                                                                 abs_tol=0.01), '')
brand_rps_25 = [BRAND_REV_25[b] * 1000.0 / BRAND_STORES_25[b] for b in range(5)]
WAVG_DRAG = sum(FX_DRAG[u] * REV_UNIT[u][2] for u in UNITS) / sum(REV_UNIT[u][2] for u in UNITS)
brand_stores_f, brand_rps_f, brand_rev_f = [], [], []
sb = list(BRAND_STORES_25)
rb = list(brand_rps_25)
for t in range(5):
    sb = [sb[b] + NSO_TOTAL[t] * BRAND_NSO_MIX[b] for b in range(5)]
    rb = [rb[b] * (1 + LFL_PATH[t]) * (1 - WAVG_DRAG) for b in range(5)]
    brand_stores_f.append(list(sb)); brand_rps_f.append(list(rb))
    brand_rev_f.append([sb[b] * rb[b] / 1000.0 for b in range(5)])
brand_total_f = [sum(brand_rev_f[t]) * (1 - ELIM_PCT) for t in range(5)]
brand_total_f[0] = (brand_total_f[0] + rev_2026_from_h1) / 2.0
brand_vs_geo = [brand_total_f[t] / rev_f[t] - 1 for t in range(5)]
chk('the brand build and the geographic build reconcile within 2% in every year',
    max(abs(x) for x in brand_vs_geo) < 0.02,
    f'max gap {100 * max(abs(x) for x in brand_vs_geo):.2f}%')
# The residual gap is a genuine mix effect, not an error: the company's brand-level opening
# mix is KFC-heavy (40% of openings at ~USD 1.3m per restaurant) while the geographic mix
# spreads additions across markets averaging ~USD 0.9m, so the brand build runs ~2% ahead
# by FY2030. The geographic build is adopted (it ties the audited history exactly at unit
# level); the brand build is the volume-x-price cross-check and its gap is published.
log(f'Brand build: FY2030E {brand_total_f[4]:,.0f}m vs geographic {rev_f[4]:,.0f}m '
    f'({100 * brand_vs_geo[4]:+.2f}%); KFC revenue per restaurant USD '
    f'{brand_rps_25[0]:,.0f}k, Krispy Kreme {brand_rps_25[3]:,.0f}k')

# ============================================================================
# 4. THE COST STACK — one escalator per driver class
# ============================================================================
# Each cost class is driven by its own physical or contractual driver. No single
# blended inflation index is applied across physically distinct lines.
COST_DRIVERS = {
    'inventory':   ('share of revenue', [0.2740, 0.2725, 0.2715, 0.2710, 0.2705],
                    'Food, filling and packing materials. Held at the 27.4% of revenue the '
                    'company actually recorded in the first half of 2026 — down from 29.2% a '
                    'year earlier on procurement and menu work — and then flat to marginally '
                    'better as those programmes mature. This line is escalated on a traded food '
                    'basket, never on a domestic price index.'),
    'royalties':   ('share of revenue', [0.0555] * 5,
                    'Royalties to the brand franchisors. A contractual percentage of branded '
                    'sales, not an inflating cost: 5.55% of revenue in FY2025 and 5.52% in '
                    'FY2024. Held flat.'),
    'advertising': ('share of revenue', [0.0425] * 5,
                    'Advertisement and business development. A managed percentage of sales set '
                    'with the franchisors. 4.35% of revenue in FY2025.'),
    'utilities':   ('share of revenue', [0.0283, 0.0282, 0.0281, 0.0280, 0.0279],
                    'Utilities and communication. Driven by energy tariffs in the operating '
                    'countries. 2.86% of revenue in FY2025.'),
    'rent_other':  ('share of revenue', [0.0170, 0.0169, 0.0168, 0.0167, 0.0166],
                    'Short-term, low-value and variable lease payments that sit outside the '
                    'capitalised lease liability. Driven by property rents. 1.74% of revenue '
                    'in FY2025.'),
    'maintenance': ('share of revenue', [0.0288, 0.0287, 0.0286, 0.0285, 0.0284],
                    'Maintenance, repairs and other restaurant operating costs. Driven by '
                    'domestic services. 2.89% of revenue in FY2025.'),
}
for k, (_, path, why) in COST_DRIVERS.items():
    inp(f'cost_path_{k}', path, why + ' Base year from ' + COST_SRC25 + '.',
        '2026-08-09', 'House estimate')

# Staff: headcount per restaurant x wage per head — a unit build, not a share.
FTE_STORE_PATH = inp('fte_per_store_path', [12.05, 11.85, 11.65, 11.45, 11.25],
    'Restaurant-level full-time equivalents per restaurant. Disclosed trend: 15.4 in FY2023, '
    '13.3 in FY2024, 12.12 in FY2025 (note 26 of each filing over the year-end estate) — '
    'kiosks, the ordering application and delivery mix keep pulling it down; the path slows '
    'the decline to about 1.7% a year.', '2026-08-09', 'House estimate')
WAGE_FTE_25 = inp('wage_per_fte', STAFF_FTE and 461.118 / 37.207,
    'Average staff cost per full-time equivalent: USD 12,394 in FY2025 (staff costs USD '
    '461.118m over 37,207 average FTEs, note 26). Implied growth from FY2023 (USD 10,959) is '
    '6.3% a year.', '2025-12-31', 'Company')
WAGE_G = inp('wage_growth', 0.06,
    'Wage cost per full-time equivalent grows 6% a year, the rate the audited notes imply for '
    'FY2023 to FY2025 — deliberately above Gulf CPI, because the mix shifts toward '
    'delivery-capable and above-restaurant staff.', '2026-08-09', 'House estimate')
ABOVE_FTE = inp('above_restaurant_fte', 3.883,
    'Above-restaurant staff: 3,883 average FTEs in FY2025 (note 26), held flat — scale '
    'leverage in headcount, cost growth through the wage line only.', '2025-12-31', 'Company')
_stores_prev = STORES_TOT[1]
staff_f, _st = [], _stores_prev
for t in range(5):
    _open = _st
    _st = _st + NSO_TOTAL[t]
    avg_stores = (_open + _st) / 2.0
    wage = WAGE_FTE_25 * (1 + WAGE_G) ** (t + 1)
    staff_f.append((avg_stores * FTE_STORE_PATH[t] / 1000.0 + ABOVE_FTE) * wage)
# Delivery: channel share x cost per unit of delivered revenue — volume x price, not a share.
DEL_SHARE_PATH = inp('delivery_share_path', [0.52, 0.535, 0.55, 0.56, 0.565],
    'Home delivery share of revenue: 44% in FY2024, 48% in FY2025, 52% in H1 2026 (channel-mix '
    'slides). The path continues the shift and flattens near 56%.', '2026-06-30',
    'Company (investor relations)')
DEL_RATIO_PATH = inp('delivery_cost_ratio_path', [0.1425, 0.1420, 0.1415, 0.1410, 0.1405],
    'Delivery and transportation cost per dollar of delivered revenue: 13.8% in FY2024 '
    '(133.7/966.6), 15.0% in FY2025 (180.6/1,204.2). FY2026 is calibrated at 14.25% so the '
    'line reproduces the disclosed H1 2026 margin at the disclosed 52% share — consistent with '
    'the company\'s claim of improving unit economics in the channel — then improves only '
    'five basis points a year. The channel mix keeps rising, so the LINE as a share of group '
    'revenue rises from 7.4% to 7.9%: the unit build caps the margin expansion in a way the '
    'flat-share treatment at first delivery did not.', '2026-06-30', 'House estimate')
delivery_f = None  # filled after rev_f is final (below)

OTHER_COST_25 = (COGS[2] + SM[2] + GA[2] - DNA[2]
                 - sum(COST_LINES[k][0][2] for k in COST_LINES))
OTHER_COST_PCT = OTHER_COST_25 / REV[2]
inp('cost_residual_pct', OTHER_COST_PCT,
    'Everything in the three expense notes not separately named above — the residual "others" '
    'lines, professional fees, travel, office administration and provisions for legal and tax '
    'claims. Carried at its FY2025 share of revenue. Source: ' + COST_SRC25,
    '2025-12-31', 'Company')

delivery_f = [DEL_SHARE_PATH[t] * DEL_RATIO_PATH[t] * rev_f[t] for t in range(5)]
cash_cost_f = []
for t in range(5):
    c = sum(COST_DRIVERS[k][1][t] for k in COST_DRIVERS) + OTHER_COST_PCT
    cash_cost_f.append(c * rev_f[t] + staff_f[t] + delivery_f[t])
ebitda_f = [rev_f[t] - cash_cost_f[t] + OTHINC[2] / REV[2] * rev_f[t] for t in range(5)]
ebitda_margin_f = [ebitda_f[t] / rev_f[t] for t in range(5)]

MARGIN_HIST_AVG = sum(ebitda[i] / REV[i] for i in range(3)) / 3.0
inp('margin_history_average', MARGIN_HIST_AVG,
    'Average EBITDA margin across the three audited years — 22.6% in FY2023, 22.0% in FY2024 '
    'and 23.7% in FY2025. This is the level the cyclical reading reverts to. Source: ' + FS25 +
    ' and ' + FS24, '2025-12-31', 'Company')
margin_revert = [ebitda_margin_f[0]]
for t in range(1, 5):
    margin_revert.append(margin_revert[0] + (MARGIN_HIST_AVG - margin_revert[0]) * (t / 4.0))
inp('margin_path_cyclical', margin_revert,
    'The cyclical reading of the margin: the first half of 2026 is banked, and the margin then '
    'reverts in a straight line to the three-year audited average by FY2030. Constructed from '
    'the audited history; no forecast is taken from any outside party.',
    '2026-08-09', 'House estimate')

cost_pct_25 = ((COGS[2] + SM[2] + GA[2] - DNA[2]) / REV[2])
chk('the FY2025 cost stack closes on the audited EBITDA',
    isclose(REV[2] * (1 - cost_pct_25) + OTHINC[2] + HYPER[2], ebitda[2], abs_tol=0.01),
    f'{REV[2] * (1 - cost_pct_25) + OTHINC[2] + HYPER[2]:.3f} against {ebitda[2]:.3f}')
log(f'Cost stack: FY2025 cash costs {100*cost_pct_25:.2f}% of revenue -> FY2026E '
    f'{100*(cash_cost_f[0]/rev_f[0]):.2f}%; EBITDA margin {100*ebitda[2]/REV[2]:.1f}% -> '
    f'{100*ebitda_margin_f[0]:.1f}% -> {100*ebitda_margin_f[4]:.1f}%')
chk('the FY2026E EBITDA margin is consistent with the disclosed first half',
    ebitda_margin_f[0] >= ebitda_h1_26 / REV_H1_26 - 0.015,
    f'{100*ebitda_margin_f[0]:.2f}% against {100*ebitda_h1_26/REV_H1_26:.2f}% actually '
    f'delivered in H1 2026')

# ============================================================================
# 5. ASSET, LEASE AND WORKING-CAPITAL ROLL-FORWARDS
# ============================================================================
IMP_RATE = inp('impairment_rate_recurring',
               (sum(IMP_NF) + sum(IMP_F)) / sum(REV),
               'Recurring impairment charge on the estate, as a share of revenue: the three-year '
               'audited total of impairments on non-financial and financial assets (USD 2.4m, '
               '13.7m, 5.8m) over three-year revenue = 0.31%. A 2,700-restaurant estate always '
               'carries some underperforming brand-country units, so the forecast charges this '
               'as a recurring operating line rather than caveating it — adopted from the '
               'critique round; the first delivery excluded it and said so in §7.',
               '2025-12-31', 'Company')
OWNED_DEP_RATE = inp('owned_depreciation_rate',
                     owned_dna[2] / (PPE[1] + INTANG[1] + INVPROP[1]),
                     'Depreciation and amortisation of owned assets over the opening owned asset '
                     'base: USD 101.5 million in FY2025 over USD 391.3 million of property, '
                     'equipment, intangibles and investment property at the start of the year. '
                     'Source: ' + FS25 + ', note 24 and the statement of financial position',
                     '2025-12-31', 'Company')
ROU_DEP_RATE = inp('rou_depreciation_rate', ROU_DEP[2] / ROU[1],
                   'Depreciation of right-of-use assets over the opening right-of-use balance: '
                   'USD 205.6 million in FY2025 over USD 566.1 million. Source: ' + FS25 +
                   ', note 11', '2025-12-31', 'Company')
ROU_ADD_PCT = inp('rou_additions_pct', 0.085,
                  'Additions to right-of-use assets as a share of revenue. The company added '
                  '10.2% of revenue in FY2025 and 12.7% in FY2024, but only 7.7% in the first '
                  'half of 2026 as the opening programme normalised; 8.5% is set between the '
                  'first-half run rate and the FY2025 figure. Sources: ' + FS25 + ', note 11; '
                  + IH26 + ', note 10', '2026-06-30', 'House estimate')
LEASE_PAY_PCT = inp('lease_payments_pct', 0.089,
                    'Total lease payments — principal and interest — as a share of revenue. '
                    'USD 233.3 million on USD 2,508.8 million of revenue in FY2025, or 9.3%, '
                    'against USD 120 million on USD 1,364.5 million in the first half of 2026, '
                    'or 8.8%. Sources: ' + FS25 + ', statement of cash flows; ' + IR26,
                    '2026-06-30', 'House estimate')
NWC_PCT = inp('nwc_pct_revenue', nwc[2] / REV[2],
              'Net working capital as a share of revenue. Negative, because a restaurant '
              'business collects at the till and pays its suppliers on terms: USD (248) million '
              'on USD 2,508.8 million in FY2025, and USD (266) million on the twelve months to '
              '30 June 2026. Held at the FY2025 ratio. Sources: ' + FS25 + '; ' + IR26,
              '2025-12-31', 'Company')
MAINT_CAPEX_PCT = inp('maintenance_capex_pct',
                      (capex_gross[2] - GROSS_OPEN_25 * CAPEX_PER_STORE / 1000.0) / REV[2],
                      'Maintenance capital expenditure as a share of revenue, derived rather '
                      'than assumed: FY2025 gross capital expenditure of USD 108.8 million less '
                      'the 170 gross organic openings at the company\'s own average of USD 402 '
                      'thousand each leaves USD 40.4 million, or 1.61% of revenue, spent on the '
                      'existing estate. Sources: ' + FS25 + ', statement of cash flows; ' + IR26,
                      '2025-12-31', 'Company')
CLOSURE_RATE = inp('closure_rate', 57.0 / 2749.0,
                   'Restaurant closures as a share of the estate: 57 closures in FY2025 against '
                   '2,749 restaurants, or 2.1%. Gross openings are therefore net additions plus '
                   'closures, and capital expenditure is charged on gross openings. Source: '
                   + IR25, '2025-12-31', 'Company (investor relations)')
ETR_PATH = [0.145, 0.150, 0.155, 0.160, 0.160]
inp('etr_path', ETR_PATH,
    'Effective tax rate. The group paid 4% in FY2023, 11% in FY2024 and 14% in FY2025 as the '
    'UAE introduced corporate tax and the first domestic minimum top-up taxes landed; the first '
    'half of 2026 ran at 14.1%. The path converges on the 15% Pillar Two minimum plus a modest '
    'drag for withholding taxes and non-deductible items, which is where a group of this '
    'footprint settles once every jurisdiction has adopted the rules. Sources: ' + FS25 +
    ', note 28; ' + IH26 + '; ' + IR24 + ', changes in corporate income tax',
    '2026-08-09', 'House estimate')
PAYOUT = inp('payout_ratio', 0.85,
             'Dividend payout ratio. The board declared USD 201.6 million against FY2025, which '
             'the company states is 91.99% of net profit, and has already declared USD 100.8 '
             'million as an interim against 2026. The forecast holds 85%, a little below the '
             'FY2025 rate, because the estate is still growing. Sources: ' + IR25 + '; ' + PR26,
             '2026-07-28', 'House estimate')
DEPOSIT_YIELD = inp('deposit_yield', FININC[2] / ((CASH[1] + DEPOSITS[1] + CASH[2] + DEPOSITS[2]) / 2),
                    'Yield earned on cash and bank deposits: finance income of USD 15.5 million '
                    'in FY2025 over average cash and deposits of USD 297.5 million. Source: '
                    + FS25 + ', note 25', '2025-12-31', 'Company')

stores_tot_f, gross_open_f = [], []
s = STORES_TOT[1]
for t in range(5):
    s = s + NSO_TOTAL[t]
    stores_tot_f.append(s)
    gross_open_f.append(NSO_TOTAL[t] + s * CLOSURE_RATE)

capex_f = [gross_open_f[t] * CAPEX_PER_STORE / 1000.0 + MAINT_CAPEX_PCT * rev_f[t]
           for t in range(5)]
nwc_f = [NWC_PCT * rev_f[t] for t in range(5)]
dnwc_f = [(nwc_f[0] - nwc[2])] + [nwc_f[t] - nwc_f[t - 1] for t in range(1, 5)]

rou_f, rou_dep_f, lease_l_f, lease_int_f, lease_add_f = [], [], [], [], []
rou_prev, ll_prev = ROU[2], LEASE_L[2]
for t in range(5):
    add = ROU_ADD_PCT * rev_f[t]
    dep = ROU_DEP_RATE * rou_prev
    rou_prev = rou_prev + add - dep
    interest = KD * ll_prev
    pay = LEASE_PAY_PCT * rev_f[t]
    ll_prev = ll_prev + add + interest - pay
    rou_f.append(rou_prev); rou_dep_f.append(dep); lease_l_f.append(ll_prev)
    lease_int_f.append(interest); lease_add_f.append(add)

ppe_f, owned_dep_f = [], []
own_prev = PPE[2] + INTANG[2] + INVPROP[2]
for t in range(5):
    dep = OWNED_DEP_RATE * own_prev
    own_prev = own_prev + capex_f[t] - dep
    ppe_f.append(own_prev); owned_dep_f.append(dep)

dna_f = [owned_dep_f[t] + rou_dep_f[t] for t in range(5)]
imp_line_f = [IMP_RATE * rev_f[t] for t in range(5)]
ebit_f = [ebitda_f[t] - dna_f[t] - imp_line_f[t] for t in range(5)]
nopat_f = [ebit_f[t] * (1 - ETR_PATH[t]) for t in range(5)]
# On the capitalised-lease reading, taking a new restaurant lease IS an investment: the
# right-of-use asset is capital the firm puts to work and the matching lease liability is
# money it borrows to do so. Adding back right-of-use depreciation while charging nothing
# for right-of-use additions would count the depreciation shield without ever paying for
# the asset, and would overstate free cash flow by roughly the whole rent bill.
capex_total_f = [capex_f[t] + lease_add_f[t] for t in range(5)]
fcff_f = [nopat_f[t] + dna_f[t] - capex_total_f[t] - dnwc_f[t] for t in range(5)]
chk('capitalised-lease free cash flow reconciles to the published free-cash-flow measure',
    abs((ebitda_f[0] - ETR_PATH[0] * ebit_f[0] - capex_f[0] - dnwc_f[0]
         - LEASE_PAY_PCT * rev_f[0]) - fcff_f[0]) < 0.09 * fcff_f[0],
    'the company defines free cash flow after the whole rent bill and before tax shields; '
    'the two constructions differ only by the lease interest shield and the gap between '
    'additions and payments')

log(f'Forecast: revenue {rev_f[0]:,.0f} -> {rev_f[4]:,.0f}m; EBITDA {ebitda_f[0]:,.0f} -> '
    f'{ebitda_f[4]:,.0f}m; FCFF {fcff_f[0]:,.0f} -> {fcff_f[4]:,.0f}m')

# ---- the forecast statements: income statement, balance sheet, cash flow ----
OTHER_FIN_PCT = inp('other_finance_cost_pct',
                    (FINCOST[2] - LEASE_INT[2]) / REV[2],
                    'Finance costs other than lease interest — the unwinding of the employees\' '
                    'end-of-service provision and USD 42 thousand of bank commitment charges — '
                    'as a share of revenue. Source: ' + FS25 + ', note 25',
                    '2025-12-31', 'Company')
lease_pay_f = [LEASE_PAY_PCT * rev_f[t] for t in range(5)]
cash_open = CASH[2] + DEPOSITS[2]
fin_inc_f, other_fin_f, fincost_f, pbt_f, tax_f, pat_f, eps_f = [], [], [], [], [], [], []
cash_f, equity_f, div_f, netdebt_f, ic_f = [], [], [], [], []
eq_prev, cash_prev = EQUITY[2], cash_open
for t in range(5):
    fi = DEPOSIT_YIELD * cash_prev
    ofc = OTHER_FIN_PCT * rev_f[t]
    fc = lease_int_f[t] + ofc
    pbt = ebit_f[t] + fi - fc
    tx = pbt * ETR_PATH[t]
    pat = pbt - tx
    div = PAYOUT * pat
    cash_prev = (cash_prev + ebitda_f[t] + fi - ofc - tx - dnwc_f[t]
                 - capex_f[t] - lease_pay_f[t] - div)
    eq_prev = eq_prev + pat - div
    fin_inc_f.append(fi); other_fin_f.append(ofc); fincost_f.append(fc)
    pbt_f.append(pbt); tax_f.append(tx); pat_f.append(pat); eps_f.append(pat / SH)
    div_f.append(div); cash_f.append(cash_prev); equity_f.append(eq_prev)
    netdebt_f.append(lease_l_f[t] - cash_prev)
    ic_f.append(ppe_f[t] + rou_f[t] + nwc_f[t])
roic_f = [nopat_f[t] / ic_f[t] for t in range(5)]
chk('the forecast balance sheet keeps cash positive', min(cash_f) > 0,
    f'minimum forecast cash and deposits {min(cash_f):.1f}m')
chk('the terminal invested capital used in the DCF is the balance sheet’s own',
    isclose(ic_f[4], ppe_f[4] + rou_f[4] + nwc_f[4], rel_tol=1e-12))
log(f'Statements: FY2030E profit after tax {pat_f[4]:,.0f}m, equity {equity_f[4]:,.0f}m, '
    f'cash and deposits {cash_f[4]:,.0f}m, return on invested capital '
    f'{100*roic_f[0]:.1f}% -> {100*roic_f[4]:.1f}%')

# ============================================================================
# 6. COST OF CAPITAL — built, not assumed; both premium bases published
# ============================================================================
rev_by_country = {
    'UAE': REV_UNIT['UAE'][2], 'Saudi Arabia': REV_UNIT['Saudi Arabia'][2],
    'Kuwait': REV_UNIT['Kuwait'][2], 'Egypt': REV_UNIT['Egypt'][2],
    'Morocco': REV_UNIT['Morocco'][2],
}
lg_stores = sum(STORES_BY_COUNTRY_25[c] for c in ('Qatar', 'Oman', 'Bahrain'))
for c in ('Qatar', 'Oman', 'Bahrain'):
    rev_by_country[c] = REV_UNIT['Lower Gulf'][2] * STORES_BY_COUNTRY_25[c] / lg_stores
om_stores = sum(STORES_BY_COUNTRY_25[c] for c in ('Kazakhstan', 'Iraq', 'Lebanon', 'Jordan'))
for c in ('Kazakhstan', 'Iraq', 'Lebanon', 'Jordan'):
    rev_by_country[c] = REV_UNIT['Other markets'][2] * STORES_BY_COUNTRY_25[c] / om_stores
tot_rev_c = sum(rev_by_country.values())
chk('the country revenue map sums to segment revenue before eliminations',
    isclose(tot_rev_c, 2540.744, abs_tol=0.01), f'{tot_rev_c:.3f}')
country_weights = {c: v / tot_rev_c for c, v in rev_by_country.items()}

ERP_BLEND_RATING = sum(country_weights[c] * ERP_RATING[c] for c in country_weights)
ERP_BLEND_CDS = sum(country_weights[c] * ERP_CDS[c] for c in country_weights)

RF_RATING = UST10 - US_DEFAULT_SPREAD
RF_CDS = UST10 - US_CDS
KE_RATING = RF_RATING + BETA * ERP_BLEND_RATING
KE_CDS = RF_CDS + BETA * ERP_BLEND_CDS

MKTCAP = SPOT * SH   # net of treasury — treasury shares carry no market value
DEBT_MV = LEASE_L[2]
WD = DEBT_MV / (DEBT_MV + MKTCAP)
WE = 1 - WD
KD_AT = KD * (1 - ETR_PATH[0])
WACC_RATING = WE * KE_RATING + WD * KD_AT
WACC_CDS = WE * KE_CDS + WD * KD_AT

KE_TERM = TERMINAL_RF + BETA * ERP_BLEND_RATING
WACC_TERM = WE * KE_TERM + WD * KD * (1 - ETR_PATH[4])

# The explicit-window discount rate glides from the current rate to the terminal rate on
# the effective-tax-rate path — the only forward path in the model with its own schedule.
glide = [(ETR_PATH[t] - ETR_PATH[0]) / (ETR_PATH[4] - ETR_PATH[0]) for t in range(5)]
wacc_path = [WACC_RATING - (WACC_RATING - WACC_TERM) * glide[t] for t in range(5)]
df = []
acc = 1.0
for t in range(5):
    acc = acc / (1 + wacc_path[t])
    df.append(acc)

log(f'Cost of capital: risk-free {100*RF_RATING:.2f}% (ratings basis) / {100*RF_CDS:.2f}% (CDS '
    f'basis); blended equity premium {100*ERP_BLEND_RATING:.2f}% / {100*ERP_BLEND_CDS:.2f}%; '
    f'beta {BETA}; cost of equity {100*KE_RATING:.2f}% / {100*KE_CDS:.2f}%; cost of debt '
    f'{100*KD:.2f}% ({100*KD_AT:.2f}% after tax); debt weight {100*WD:.1f}%; '
    f'weighted cost {100*WACC_RATING:.2f}% / {100*WACC_CDS:.2f}%, terminal {100*WACC_TERM:.2f}%')
DAYS_ANCHOR = inp('days_to_anchor', 219,
    'Calendar days from the 31 December 2025 valuation date — the audited balance sheet the '
    'bridge deducts net debt at, and the date the year-1 discount factor runs from — to the '
    '7 August 2026 price anchor. Every published per-share value is rolled forward across '
    'this window at the cost of equity, net of the dividend paid inside it, so the valuation '
    'and the market price are compared on the same date. The first delivery omitted this '
    'roll (the model-study convention) entirely — the largest single correction of the '
    'critique-response round, found by self-audit.', '2026-08-07', 'Market')
DIV_WINDOW = inp('dividend_paid_in_window', DIV_FY25_DECL / SH,
    'The FY2025 dividend of USD 201.6 million (USD 0.024 a share), approved at the annual '
    'general meeting and paid in June 2026 — inside the roll window. The USD 100.8 million '
    'interim declared 28 July 2026 had not been paid by the anchor date and is excluded.',
    '2026-06-30', 'Company (investor relations)')
ROLL = (1 + KE_RATING) ** (DAYS_ANCHOR / 365.0)


def rollv(v):
    """Roll a 31-Dec-2025 per-share USD value to the 7-Aug-2026 anchor."""
    return v * ROLL - DIV_WINDOW


chk('the marginal cost of debt sits above the sovereign', KD > UST10 + ADGB_SPREAD,
    f'{100*KD:.2f}% against an Abu Dhabi ten-year of about '
    f'{100*(UST10 + ADGB_SPREAD):.2f}%')
chk('terminal growth is below the terminal risk-free rate', TERMINAL_G < TERMINAL_RF,
    f'{100*TERMINAL_G:.1f}% against {100*TERMINAL_RF:.2f}%')

# ============================================================================
# 7. THE DISCOUNTED CASH FLOW, AND THE CONTESTED JUDGEMENT COMPUTED BOTH WAYS
# ============================================================================
TERMINAL_ROIC = inp('terminal_roic', 0.30,
    'Terminal return on incremental invested capital, faded to 30% from the model-implied '
    'average of ~55%. Anchored on the company\'s own store-economics disclosure: USD 402 '
    'thousand average capital cost and a 3.0-year average payback imply roughly a 33% pre-tax '
    'cash-on-cash return on the AVERAGE new store, and the same table shows the MARGINAL brands '
    '(Pizza Hut, Krispy Kreme, growth brands) beyond five years — materially below the average. '
    'Continuing the average net-book return into perpetuity was the largest judgement defect '
    'raised in the critique round, conceded in the study\'s own expert cross-examination; the '
    'fade prices it. The 55% continuation is published as the bull reading in the sensitivity.',
    '2026-06-30', 'Company (investor relations)')


def run_dcf(fcff, nopat_last, invested_capital, wacc_t, g, disc, wacc_term,
            net_debt_bridge, nci_deduct, roic_target=None):
    pv = [fcff[t] * disc[t] for t in range(5)]
    nopat_next = nopat_last * (1 + g)
    roic_implied_avg = nopat_last / invested_capital   # matched-year, off-by-one fixed
    roic_term = roic_target if roic_target is not None else roic_implied_avg
    rr = g / roic_term
    tv = nopat_next * (1 - rr) / (wacc_term - g)
    pv_tv = tv * disc[4]
    ev = sum(pv) + pv_tv
    equity = ev - net_debt_bridge - nci_deduct
    return dict(pv=pv, sum_pv=sum(pv), tv=tv, pv_tv=pv_tv, ev=ev,
                tv_share=pv_tv / ev, roic_term=roic_term, rr_term=rr,
                roic_implied_avg=roic_implied_avg,
                nopat_next=nopat_next, equity=equity, fv=equity / SH,
                net_debt=net_debt_bridge, invested_capital=invested_capital)


NET_CASH_25 = CASH[2] + DEPOSITS[2] - BANK_DEBT[2]
IC_TERM = ppe_f[4] + rou_f[4] + nwc_f[4]
NET_DEBT_A = LEASE_L[2] - NET_CASH_25
A = run_dcf(fcff_f, nopat_f[4], IC_TERM, wacc_path, TERMINAL_G, df, WACC_TERM,
            NET_DEBT_A, NCI[2], roic_target=TERMINAL_ROIC)

# --- Framing B: leases as an operating cost, not as debt ---------------------
# EBITDA is struck after the cash rent the company actually pays, depreciation excludes
# the right-of-use charge, and the lease liability is not subtracted in the bridge. The
# cost of capital is rebuilt at zero debt weight, because on this reading the company
# has none.
ebitda_B = [ebitda_f[t] - LEASE_PAY_PCT * rev_f[t] for t in range(5)]
dna_B = owned_dep_f
ebit_B = [ebitda_B[t] - dna_B[t] for t in range(5)]
nopat_B = [ebit_B[t] * (1 - ETR_PATH[t]) for t in range(5)]
fcff_B = [nopat_B[t] + dna_B[t] - capex_f[t] - dnwc_f[t] for t in range(5)]
WACC_B = KE_RATING
WACC_TERM_B = KE_TERM
wacc_path_B = [WACC_B - (WACC_B - WACC_TERM_B) * glide[t] for t in range(5)]
df_B, acc = [], 1.0
for t in range(5):
    acc = acc / (1 + wacc_path_B[t])
    df_B.append(acc)
IC_TERM_B = ppe_f[4] + nwc_f[4]
B = run_dcf(fcff_B, nopat_B[4], IC_TERM_B, wacc_path_B, TERMINAL_G, df_B, WACC_TERM_B,
            -NET_CASH_25, NCI[2], roic_target=TERMINAL_ROIC)

A['fv_unrolled'], A['fv'] = A['fv'], rollv(A['fv'])
B['fv_unrolled'], B['fv'] = B['fv'], rollv(B['fv'])
log(f'Lease treatment, both ways: capitalised USD {A["fv"]:.3f}/share '
    f'(AED {A["fv"]*AEDUSD:.2f}); as an operating cost USD {B["fv"]:.3f}/share '
    f'(AED {B["fv"]*AEDUSD:.2f}); gap {100*(B["fv"]/A["fv"]-1):+.1f}%')

# ============================================================================
# 8. THE OTHER THREE LENSES
# ============================================================================
peer_ev_ebitda = sorted(p['ev_ebitda'] for p in PEERS['peers'].values()
                        if p.get('ev_ebitda') and 4 < p['ev_ebitda'] < 40)
peer_pe = sorted(p['pe_trailing'] for p in PEERS['peers'].values()
                 if p.get('pe_trailing') and 5 < p['pe_trailing'] < 45)
med = lambda xs: (xs[len(xs) // 2] if len(xs) % 2 else (xs[len(xs) // 2 - 1] + xs[len(xs) // 2]) / 2)
PEER_EV_EBITDA_MED = med(peer_ev_ebitda)
PEER_PE_MED = med(peer_pe)

MULT_EV_EBITDA = inp('justified_ev_ebitda', 8.5,
                     'Justified enterprise value to EBITDA. The peer median on a post-lease '
                     f'basis is {PEER_EV_EBITDA_MED:.1f} times across the usable comparators, '
                     'but every one of them is either a franchisor keeping a royalty margin '
                     'rather than an operator, or a listed franchisee on a different growth and '
                     'currency profile. 8.5 times is set below the peer median to reflect that '
                     'Americana is the operator, not the brand owner, and carries the whole '
                     'lease estate on its balance sheet. Source of the peer figures, as a '
                     'cross-check only: ' + PEERS['source'], '2026-08-09', 'Industry')
MULT_PE = inp('justified_pe', 17.0,
              'Justified price to earnings. The usable peer median is '
              f'{PEER_PE_MED:.1f} times; 17 times sits just below it, which is where a '
              'high-return, cash-generative operator with a mid-single-digit like-for-like '
              'growth rate and a heavy dividend belongs. Source of the peer figures, as a '
              'cross-check only: ' + PEERS['source'], '2026-08-09', 'Industry')
SUSTAINABLE_ROE = inp('sustainable_roe', 0.42,
                      'Sustainable return on equity. The company earned 49.6% in FY2025 on '
                      'average equity, and 41.9% in FY2024, on a book that is small because the '
                      'estate is leased rather than owned and most of the earnings are paid out. '
                      '42% is set below the FY2025 outturn. Source: ' + FS25,
                      '2025-12-31', 'Company')

# relative lens: FY2027E EBITDA on the justified multiple, discounted back
rel_ev_27 = ebitda_f[1] * MULT_EV_EBITDA
# EV struck at the END of FY2027 is discounted two years, so BOTH intervening years'
# free cash flows belong to today's holder — the first delivery dropped FY2027's
# (the one defect all four external critiques agreed on).
rel_ev_now = rel_ev_27 * df[1] + A['pv'][0] + A['pv'][1]
rel_equity = rel_ev_now - NET_DEBT_A - NCI[2]
rel_fv = rollv(rel_equity / SH)
rel_bear = rollv(((ebitda_f[1] * 7.0) * df[1] + A['pv'][0] + A['pv'][1] - NET_DEBT_A - NCI[2]) / SH)
rel_bull = rollv(((ebitda_f[1] * 10.5) * df[1] + A['pv'][0] + A['pv'][1] - NET_DEBT_A - NCI[2]) / SH)

# normalised earnings power: mid-cycle margin at current scale
# Mid-cycle means neither the structural peak nor the trough: the midpoint of the two
# FY2028 margin readings the study itself dual-frames. The first delivery used the
# structural FY2028 margin alone — above every audited year — under a mid-cycle label,
# the second-largest judgement defect raised in the critique round.
norm_margin = (ebitda_margin_f[2] + margin_revert[2]) / 2.0
norm_ebitda = rev_f[0] * norm_margin
norm_ebit = norm_ebitda - dna_f[0] - imp_line_f[0]
norm_net_fin = fin_inc_f[0] - KD * LEASE_L[2] - OTHER_FIN_PCT * rev_f[0]
norm_earnings = (norm_ebit + norm_net_fin) * (1 - ETR_PATH[1])
norm_eps = norm_earnings / SH
norm_fv = rollv(norm_eps * MULT_PE)
norm_bear = rollv(norm_eps * 13.0)
norm_bull = rollv(norm_eps * 21.0)

# book value and sustainable return
bvps_now = EQ_H1_26 / SH
justified_pb = (SUSTAINABLE_ROE - TERMINAL_G) / (KE_TERM - TERMINAL_G)
# The book lens is struck on 30-Jun-2026 equity, already inside the window: roll the
# remaining 38 days only, with no dividend (the interim was unpaid at the anchor).
BOOK_ROLL = (1 + KE_RATING) ** (38 / 365.0)
book_fv = bvps_now * justified_pb * BOOK_ROLL
book_bear = bvps_now * ((0.34 - TERMINAL_G) / (KE_TERM + 0.02 - TERMINAL_G)) * BOOK_ROLL
book_bull = bvps_now * ((0.48 - TERMINAL_G) / (KE_TERM - 0.01 - TERMINAL_G)) * BOOK_ROLL

# DCF bear/bull: whole-model re-runs
def rerun(margin_shift, wacc_shift, g, lfl_shift, margin_path=None):
    lfl = [x + lfl_shift for x in LFL_PATH]
    st, rp, rv = [], [], []
    s_p = {u: STORES_UNIT[u][1] for u in UNITS}
    r_p = dict(rps_25)
    revs = []
    for t in range(5):
        tot = 0.0
        for u in UNITS:
            s_p[u] = s_p[u] + NSO_TOTAL[t] * NSO_MIX[u]
            r_p[u] = r_p[u] * (1 + lfl[t]) * (1 - FX_DRAG[u])
            tot += s_p[u] * r_p[u] / 1000.0
        revs.append(tot * (1 - ELIM_PCT))
    revs[0] = (revs[0] + rev_2026_from_h1) / 2.0
    mp = margin_path if margin_path is not None else ebitda_margin_f
    eb = [revs[t] * (mp[t] + margin_shift) for t in range(5)]
    cx = [gross_open_f[t] * CAPEX_PER_STORE / 1000.0 + MAINT_CAPEX_PCT * revs[t] for t in range(5)]
    nw = [NWC_PCT * revs[t] for t in range(5)]
    dnw = [nw[0] - nwc[2]] + [nw[t] - nw[t - 1] for t in range(1, 5)]
    rr, rd, op, od = ROU[2], [], PPE[2] + INTANG[2] + INVPROP[2], []
    for t in range(5):
        d = ROU_DEP_RATE * rr
        rr = rr + ROU_ADD_PCT * revs[t] - d
        rd.append(d)
        d2 = OWNED_DEP_RATE * op
        op = op + cx[t] - d2
        od.append(d2)
    dn = [rd[t] + od[t] for t in range(5)]
    eb_it = [eb[t] - dn[t] - IMP_RATE * revs[t] for t in range(5)]
    npt = [eb_it[t] * (1 - ETR_PATH[t]) for t in range(5)]
    fc = [npt[t] + dn[t] - cx[t] - ROU_ADD_PCT * revs[t] - dnw[t] for t in range(5)]
    w0, wt = WACC_RATING + wacc_shift, WACC_TERM + wacc_shift
    wp = [w0 - (w0 - wt) * glide[t] for t in range(5)]
    d_, a_ = [], 1.0
    for t in range(5):
        a_ = a_ / (1 + wp[t]); d_.append(a_)
    return rollv(run_dcf(fc, npt[4], op + rr + nw[4], wp, g, d_, wt, NET_DEBT_A, NCI[2],
                         roic_target=TERMINAL_ROIC)['fv'])


dcf_bear = rerun(-0.015, +0.015, 0.020, -0.010)
dcf_bull = rerun(+0.015, -0.015, 0.040, +0.010)

contested_b_fv = rerun(0.0, 0.0, TERMINAL_G, 0.0, margin_path=margin_revert)
log(f'Contested judgement — margin: structural USD {A["fv"]:.3f}/share '
    f'(AED {A["fv"]*AEDUSD:.2f}); cyclical USD {contested_b_fv:.3f}/share '
    f'(AED {contested_b_fv*AEDUSD:.2f}); gap {100*(contested_b_fv/A["fv"]-1):+.1f}%')

W_DCF = inp('weight_dcf', 0.50, 'Weight on the cash-flow lens. It carries the most because the '
            'business is cash-generative, the estate is knowable restaurant by restaurant, and '
            'the company publishes the store-level economics the model is built on.',
            '2026-08-09', 'House estimate')
W_REL = inp('weight_relative', 0.20, 'Weight on relative multiples. Held down because no clean '
            'comparable exists: the global names are franchisors, not operators.',
            '2026-08-09', 'House estimate')
W_NORM = inp('weight_normalised', 0.20, 'Weight on normalised earnings power.',
             '2026-08-09', 'House estimate')
W_BOOK = inp('weight_book', 0.10, 'Weight on book value and sustainable return. The lowest, '
             'because an operator that leases its estate carries very little book equity and '
             'the lens is correspondingly unstable here.', '2026-08-09', 'House estimate')
chk('the lens weights sum to one', isclose(W_DCF + W_REL + W_NORM + W_BOOK, 1.0, abs_tol=1e-12))

lens_values = {'Discounted cash flow': A['fv'], 'Relative multiples': rel_fv,
               'Normalised earnings power': norm_fv, 'Book value and sustainable return': book_fv}
lens_weights = {'Discounted cash flow': W_DCF, 'Relative multiples': W_REL,
                'Normalised earnings power': W_NORM, 'Book value and sustainable return': W_BOOK}
central = sum(lens_values[k] * lens_weights[k] for k in lens_values)
lens_ranges = {'Discounted cash flow': (dcf_bear, A['fv'], dcf_bull),
               'Relative multiples': (rel_bear, rel_fv, rel_bull),
               'Normalised earnings power': (norm_bear, norm_fv, norm_bull),
               'Book value and sustainable return': (book_bear, book_fv, book_bull)}
low = min(v[0] for v in lens_ranges.values())
high = max(v[2] for v in lens_ranges.values())
log(f'Lenses (USD/share): cash flow {A["fv"]:.3f}, relative {rel_fv:.3f}, normalised '
    f'{norm_fv:.3f}, book {book_fv:.3f}; weighted central {central:.3f} '
    f'(AED {central*AEDUSD:.2f}) against a spot of AED {SPOT_AED:.2f}')

# ============================================================================
# 9. SENSITIVITY — whole-model re-runs
# ============================================================================
g_grid = [0.020, 0.025, 0.030, 0.035, 0.040]
w_grid = [-0.015, -0.0075, 0.0, 0.0075, 0.015]
grid_g_w = [[rerun(0.0, dw, g, 0.0) for g in g_grid] for dw in w_grid]
m_grid = [-0.02, -0.01, 0.0, 0.01, 0.02]
grid_m_w = [[rerun(dm, dw, TERMINAL_G, 0.0) for dm in m_grid] for dw in w_grid]
single = {
    'Like-for-like sales growth (−1.0pp / −0.5pp / base / +0.5pp / +1.0pp)':
        [rerun(0.0, 0.0, TERMINAL_G, d) for d in (-0.010, -0.005, 0.0, 0.005, 0.010)],
    'EBITDA margin (−2.0pp / −1.0pp / base / +1.0pp / +2.0pp)':
        [rerun(d, 0.0, TERMINAL_G, 0.0) for d in m_grid],
    'Cost of capital (−1.5pp / −0.75pp / base / +0.75pp / +1.5pp)':
        [rerun(0.0, d, TERMINAL_G, 0.0) for d in w_grid],
    'Terminal growth (2.0% / 2.5% / 3.0% / 3.5% / 4.0%)':
        [rerun(0.0, 0.0, g, 0.0) for g in g_grid],
}

# ============================================================================
# 10. EXPERT PANEL — three methods, worked
# ============================================================================
# Expert 1 — restaurant-level unit economics: value the estate as a portfolio of
# restaurants earning a four-wall return on the capital each one costs to build.
e1_stores = STORES_TOT[1]
e1_fw_ebitda = 433.0 * 2.0 / 2  # four-wall EBITDA, H1 2026 annualised
inp('four_wall_ebitda_h1_26', 433.0, IR26 + ': four-wall EBITDA of USD 433 million in the first '
    'half of 2026, a margin of 31.7% of revenue', '2026-06-30', 'Company (investor relations)')
e1_fw_annual = 433.0 * 2
e1_per_store = e1_fw_annual / e1_stores * 1000.0
e1_capex_store = CAPEX_PER_STORE
e1_cash_return = e1_per_store / e1_capex_store
e1_corporate = (GA[2] - GA[2] * 0.14)   # G&A less its depreciation share, the corporate drag
e1_maint = MAINT_CAPEX_PCT * rev_f[0]
e1_lease = LEASE_PAY_PCT * rev_f[0]
e1_owner_cash = (e1_fw_annual - e1_corporate - e1_maint - e1_lease) * (1 - ETR_PATH[1])
# No growth credit without the capital that funds it (critique finding): the owner
# cash earnings charge no growth capital, so they are capitalised at the FULL
# terminal cost of equity rather than a growth-adjusted rate.
e1_cap_rate = KE_TERM
e1_value = e1_owner_cash / e1_cap_rate
e1_equity = e1_value + NET_CASH_25 - NCI[2]
e1_fv = rollv(e1_equity / SH)
e1_low = rollv((e1_owner_cash / (e1_cap_rate + 0.015) + NET_CASH_25 - NCI[2]) / SH)
e1_high = rollv((e1_owner_cash / (e1_cap_rate - 0.010) + NET_CASH_25 - NCI[2]) / SH)

# Expert 2 — franchise-annuity view: capitalise the dividend the company actually pays.
e2_dps_25 = DIV_FY25_DECL / SH
e2_g = TERMINAL_G
e2_ke = KE_TERM
e2_fv = rollv(e2_dps_25 * (1 + e2_g) / (e2_ke - e2_g))
e2_low = rollv(e2_dps_25 * (1 + 0.02) / (e2_ke + 0.01 - 0.02))
e2_high = rollv(e2_dps_25 * (1 + 0.04) / (e2_ke - 0.005 - 0.04))

# Expert 3 — return on invested capital against the cost of capital.
e3_ic = ppe_f[0] + rou_f[0] + nwc_f[0]
e3_roic = nopat_f[0] / e3_ic
e3_spread = e3_roic - WACC_RATING
e3_ev = nopat_f[0] / WACC_TERM + (nopat_f[0] * (e3_roic - WACC_TERM) / e3_roic) * \
    (TERMINAL_G / (WACC_TERM * (WACC_TERM - TERMINAL_G)))
e3_equity = e3_ev - NET_DEBT_A - NCI[2]
e3_fv = rollv(e3_equity / SH)
e3_low = rollv((nopat_f[0] / (WACC_TERM + 0.01) - NET_DEBT_A - NCI[2]) / SH)
e3_high = rollv((e3_ev * 1.18 - NET_DEBT_A - NCI[2]) / SH)

experts = [
    dict(label='Expert 1', method='Restaurant-level unit economics',
         base=e1_fv, low=e1_low, high=e1_high,
         worldview='A restaurant chain is a portfolio of individual cash machines. Value it by '
                   'what one restaurant earns against what one restaurant costs to build, then '
                   'count the restaurants and take off what head office and the landlords cost.',
         works='When the operator publishes store-level economics, as this one does, and when '
               'the estate is homogeneous enough for an average to mean something.',
         fails='When new restaurants are systematically worse than the ones already open, so '
               'the portfolio average flatters the marginal decision — and when a large part of '
               'the estate sits in markets where the currency, not the restaurant, drives the '
               'result.',
         falsifier='Average capital expenditure per restaurant rising above roughly USD 500 '
                   'thousand while payback lengthens beyond four years would break the '
                   'arithmetic this lens rests on.'),
    dict(label='Expert 2', method='Distributable cash as a perpetuity',
         base=e2_fv, low=e2_low, high=e2_high,
         worldview='The only thing an outside shareholder in a controlled company receives is '
                   'the dividend. Capitalise what is actually paid, at the return the risk '
                   'demands, and grow it at what the business can sustain.',
         works='When the payout is high, established and covered by cash rather than by '
               'accounting profit — as here, at roughly 92% of FY2025 earnings and with an '
               'interim already declared against 2026.',
         fails='When the payout is discretionary and the controlling shareholder has a reason '
               'to change it, or when the dividend is funded from a balance sheet that is '
               'quietly running down.',
         falsifier='A cut in the declared dividend, or free cash flow falling below the '
                   'distribution for two consecutive years, would end this reading.'),
    dict(label='Expert 3', method='Return on capital against the cost of capital',
         base=e3_fv, low=e3_low, high=e3_high,
         worldview='Value is the capitalised current profit plus whatever the business earns '
                   'above its cost of capital on the capital it goes on to invest. If the '
                   'spread is positive, growth is worth paying for; if it is not, growth '
                   'destroys value.',
         works='When invested capital is measurable and the spread is wide and stable, so the '
               'growth term is not doing all the work.',
         fails='When most of the invested capital is a right-of-use asset whose measurement '
               'depends on lease-term judgements — which is exactly the key audit matter in '
               'this filing.',
         falsifier='The return on invested capital falling to the cost of capital would '
                   'collapse the growth term to zero and take roughly a fifth off this value.'),
]
expert_median = sorted(e['base'] for e in experts)[1]

# ============================================================================
# 11. ASSEMBLE
# ============================================================================
OUT = dict(
    # THE ANSWER, WHERE THE SHARED READER LOOKS FOR IT. [R-GAP-01]'s gate reads a
    # study's own numbers for a central and the spot it was struck at; this study
    # carried both — under meta.spot and lenses.central — and the gate could see
    # neither, so it could say nothing about this name at all and the study sat on
    # the unreadable list. AN UNREADABLE STUDY IS NOT A CLEAN STUDY [R-ENF-04].
    # The figures below are the ones the delivered document publishes today, in the
    # study's own currency: they are NOT a new answer and NOTHING here endorses the
    # weighted blend that produces the central — [R-LENS-03] retires it and this name
    # stays on the lens ratchet until it is rebuilt. What the gate audits is the
    # answer a reader actually receives, and this is that answer.
    # IN THE LISTING CURRENCY, WHICH IS NOT THIS STUDY'S REPORTING CURRENCY. The
    # gate substitutes the LATEST KNOWN price for the struck spot, and that price
    # comes from the supplied close register and the OHLC library, both of which
    # carry an ADX name in DIRHAMS. Committing the dollar figures the model works
    # in put a USD 0.58 central against an AED 2.39 close and the gate reported this
    # study 75.6% below the market — a currency error wearing the appearance of a
    # valuation finding, and the more dangerous kind because the arithmetic is
    # perfect. Both figures below are therefore converted at the peg, and both are
    # what the delivered document states in its own headline.
    central=central * AEDUSD,
    spot=SPOT_AED,
    meta=dict(ticker='AMR', company='Americana Restaurants International PLC',
              market='UAE (ADX/DFM)', market_code='AE', exchange='Abu Dhabi Securities Exchange',
              dual_listing='Saudi Exchange (Tadawul), symbol 6015',
              currency='USD', currency_note='The company reports in US dollars; the shares '
              'trade in dirhams on the Abu Dhabi Securities Exchange and in riyals in Riyadh. '
              'The valuation runs in US dollars, the reporting and functional currency of the '
              'group, and is converted to dirhams at the 3.6725 peg.',
              listing_currency='AED', fx=AEDUSD,
              asof='2026-08-07', spot=SPOT, spot_aed=SPOT_AED,
              shares_mn=SH, shares_issued_mn=SH_ISSUED, mktcap=MKTCAP,
              klass='Operating company — multi-country restaurant operator and master franchisee',
              sector='Consumer discretionary — restaurants and quick-service food',
              basis='Post-IFRS-16 free cash flow to the firm, US dollars million',
              revision=1),
    inputs=I,
    history=dict(years=YEARS_H, revenue=REV, gross_profit=gross_profit, cogs=COGS,
                 selling=SM, admin=GA, other_income=OTHINC, hyperinflation=HYPER,
                 impair_nonfin=IMP_NF, impair_fin=IMP_F, operating_profit=OPPROF,
                 ebitda=ebitda, ebitda_margin=[ebitda[i] / REV[i] for i in range(3)],
                 dna=DNA, rou_dep=ROU_DEP, owned_dna=owned_dna, ebit=ebit,
                 finance_income=FININC, finance_cost=FINCOST, lease_interest=LEASE_INT,
                 pbt=PBT, tax=TAX, pat=PAT, pat_shareholders=PATSH, eps=eps,
                 ppe=PPE, rou=ROU, intangibles=INTANG, investment_property=INVPROP,
                 inventories=INVENT, receivables=RECV, payables=PAYABLES,
                 cash=CASH, deposits=DEPOSITS, lease_liabilities=LEASE_L,
                 bank_debt=BANK_DEBT, equity=EQUITY, nci=NCI, total_assets=TOTASSETS,
                 eosb=EOSB, nwc=nwc, net_debt=net_debt, bvps=bvps,
                 capex=capex_gross, cfo=CFO, lease_principal=LEASE_PRIN,
                 dividends_paid=DIVPAID, fte=STAFF_FTE,
                 h1_2026=dict(revenue=REV_H1_26, ebitda=ebitda_h1_26, pbt=PBT_H1_26,
                              tax=TAX_H1_26, pat_shareholders=PATSH_H1_26,
                              dna=DNA_H1_26, equity=EQ_H1_26,
                              lease_liabilities=LEASE_L_H1_26,
                              cash_and_deposits=CASH_H1_26 + DEP_H1_26,
                              margin=ebitda_h1_26 / REV_H1_26),
                 q1_2026_revenue=REV_Q1_26, q2_2026_revenue=REV_Q2_26),
    unit_build=dict(units=UNITS, unit_note=UNIT_NOTE,
                    revenue_hist={u: REV_UNIT[u] for u in UNITS},
                    stores_hist={u: STORES_UNIT[u] for u in UNITS},
                    rps_2024={u: rps_24[u] for u in UNITS},
                    rps_2025={u: rps_25[u] for u in UNITS},
                    stores_f=stores_f, rps_f=rps_f, revenue_f=rev_f_unit,
                    stores_total_f=stores_tot_f, gross_openings_f=gross_open_f,
                    nso=NSO_TOTAL, nso_mix=NSO_MIX, lfl=LFL_PATH, fx_drag=FX_DRAG,
                    elimination_pct=ELIM_PCT,
                    revenue_2026_from_h1=rev_2026_from_h1),
    cost_stack=dict(lines={k: dict(hist=COST_LINES[k][0], description=COST_LINES[k][1],
                                   driver_class=COST_LINES[k][2],
                                   pct_hist=[COST_LINES[k][0][i] / REV[i] for i in range(3)],
                                   path=(COST_DRIVERS[k][1] if k in COST_DRIVERS else
                                         [(staff_f if k == 'staff' else delivery_f)[t] / rev_f[t]
                                          for t in range(5)]))
                           for k in COST_LINES},
                    residual_pct=OTHER_COST_PCT,
                    staff_f=staff_f, delivery_f=delivery_f,
                    fte_per_store=FTE_STORE_PATH, wage_per_fte=WAGE_FTE_25, wage_growth=WAGE_G,
                    above_restaurant_fte=ABOVE_FTE, delivery_share=DEL_SHARE_PATH,
                    delivery_cost_ratio=DEL_RATIO_PATH,
                    cash_cost_f=cash_cost_f,
                    cost_pct_2025=cost_pct_25),
    brand_build=dict(brands=BRANDS, stores_2024=BRAND_STORES_24, stores_2025=BRAND_STORES_25,
                     stores_h1_2026=BRAND_STORES_H1, revenue_2024=BRAND_REV_24,
                     revenue_2025=BRAND_REV_25, rps_2025=brand_rps_25, lfl_2025=BRAND_LFL_25,
                     nso_mix=BRAND_NSO_MIX, wavg_drag=WAVG_DRAG,
                     stores_f=brand_stores_f, rps_f=brand_rps_f, revenue_f=brand_rev_f,
                     total_f=brand_total_f, vs_geographic=brand_vs_geo),
    forecast=dict(years=FY_F, revenue=rev_f, ebitda=ebitda_f, ebitda_margin=ebitda_margin_f,
                  dna=dna_f, owned_dep=owned_dep_f, rou_dep=rou_dep_f, ebit=ebit_f,
                  nopat=nopat_f, capex=capex_f, capex_total=capex_total_f,
                  nwc=nwc_f, dnwc=dnwc_f, fcff=fcff_f,
                  lease_liabilities=lease_l_f, lease_interest=lease_int_f,
                  lease_additions=lease_add_f, lease_payments=lease_pay_f,
                  rou=rou_f, owned_assets=ppe_f,
                  impairment=imp_line_f,
                  etr=ETR_PATH, wacc_path=wacc_path, discount_factor=df, glide=glide,
                  stores=stores_tot_f, gross_openings=gross_open_f,
                  finance_income=fin_inc_f, other_finance_cost=other_fin_f,
                  finance_cost=fincost_f, pbt=pbt_f, tax=tax_f, pat=pat_f, eps=eps_f,
                  dividends=div_f, cash=cash_f, equity=equity_f, net_debt=netdebt_f,
                  invested_capital=ic_f, roic=roic_f),
    wacc=dict(rf_ust=UST10, us_default_spread=US_DEFAULT_SPREAD, us_cds=US_CDS,
              rf_rating=RF_RATING, rf_cds=RF_CDS,
              erp_rating=ERP_BLEND_RATING, erp_cds=ERP_BLEND_CDS,
              beta_provenance=json.load(open(os.path.join(HERE, 'beta_result.json'))),
              beta=BETA, ke_rating=KE_RATING, ke_cds=KE_CDS, ke_terminal=KE_TERM,
              kd=KD, kd_fy24=KD_FY24, kd_after_tax=KD_AT,
              debt_weight=WD, equity_weight=WE,
              wacc_rating=WACC_RATING, wacc_cds=WACC_CDS, wacc_terminal=WACC_TERM,
              terminal_rf=TERMINAL_RF, terminal_g=TERMINAL_G, terminal_roic=TERMINAL_ROIC,
              roll_factor=ROLL, days_to_anchor=DAYS_ANCHOR, div_in_window=DIV_WINDOW,
              country_weights=country_weights, erp_by_country_rating=ERP_RATING,
              erp_by_country_cds=ERP_CDS, cds_not_published=CDS_NA,
              abu_dhabi_spread=ADGB_SPREAD, uae_default_spread=UAE_DEFAULT_SPREAD),
    dcf=dict(A, framing='Leases capitalised (IFRS 16): the lease liability is debt, '
             'right-of-use depreciation is in depreciation and amortisation, and lease '
             'payments are not an operating cost'),
    dcf_alt=dict(B, framing='Leases as an operating cost: EBITDA is struck after the cash rent '
                 'actually paid, right-of-use depreciation is excluded, and the lease liability '
                 'is not deducted in the bridge',
                 ebitda=ebitda_B, ebit=ebit_B, nopat=nopat_B, fcff=fcff_B,
                 wacc=WACC_B, wacc_terminal=WACC_TERM_B, discount_factor=df_B),
    contested=dict(
        title='Is the margin step-change structural or cyclical?',
        why='Between the first half of 2025 and the first half of 2026 the EBITDA margin went '
            'from 22.6% to 25.5%, and the cost of food and packaging fell from 29.2% of revenue '
            'to 27.4%. Almost the entire increase in value over the last year rests on that '
            'move. The company attributes it to procurement work, menu engineering and the '
            'improving unit economics of home delivery — all of which are structural if they '
            'hold. The same numbers are equally consistent with a favourable turn in globally '
            'traded food prices and a period of restrained promotional intensity, both of which '
            'revert. Nothing in the filings settles it, and the two readings are worth '
            'materially different amounts, so both are computed and published.',
        way_a=dict(name='Structural — the gains hold and improve slowly',
                   detail='The base case. Food and packaging stays near the 27.4% of revenue '
                          'the company actually recorded in the first half of 2026, and the '
                          f'EBITDA margin runs from {100*ebitda_margin_f[0]:.1f}% to a peak of '
                          f'{100*max(ebitda_margin_f):.1f}% before the growing delivery channel '
                          f'eases it to {100*ebitda_margin_f[4]:.1f}%.',
                   value_usd=A['fv'], value_aed=A['fv'] * AEDUSD, ev=A['ev'],
                   margin_path=ebitda_margin_f, wacc=WACC_RATING, tv_share=A['tv_share']),
        way_b=dict(name='Cyclical — the gains are competed away',
                   detail='The first half of 2026 is banked, and the EBITDA margin then reverts '
                          'in a straight line to the three-year audited average of '
                          f'{100*MARGIN_HIST_AVG:.1f}% by FY2030.',
                   value_usd=contested_b_fv, value_aed=contested_b_fv * AEDUSD,
                   margin_path=margin_revert),
        gap_pct=contested_b_fv / A['fv'] - 1,
        margin_history_average=MARGIN_HIST_AVG,
        resolution='Both are published side by side, in the summary table, in the body and in '
                   'the workbook, and an expert range is struck on each. Neither is averaged '
                   'into the other.'),
    dual_framing_leases=dict(
        title='How the lease estate is treated',
        why='Americana leases essentially every restaurant it operates. At 31 December 2025 the '
            'capitalised lease liability was USD 637.5 million and the right-of-use asset USD '
            '610.8 million — 35% of total assets, and larger than the entire owned property and '
            'equipment base. Determining the discount rate inside those leases is one of the two '
            'key audit matters in the filing. Whether that estate is treated as borrowed money '
            'or as next year\'s rent is a live question, so it is answered twice.',
        way_a=dict(name='Leases capitalised, as the accounts present them',
                   value_usd=A['fv'], value_aed=A['fv'] * AEDUSD, ev=A['ev'],
                   net_debt=NET_DEBT_A, wacc=WACC_RATING, tv_share=A['tv_share']),
        way_b=dict(name='Leases as an operating cost',
                   value_usd=B['fv'], value_aed=B['fv'] * AEDUSD, ev=B['ev'],
                   net_debt=-NET_CASH_25, wacc=WACC_B, tv_share=B['tv_share']),
        gap_pct=B['fv'] / A['fv'] - 1,
        finding='The two readings differ by under two percent once each is built consistently — '
                'charging the right-of-use additions as investment on the capitalised reading, '
                'and charging the whole rent bill as a cost on the other. That is a result '
                'worth stating: the accounting choice that dominates the balance sheet turns '
                'out not to be the thing that decides the value.'),
    lenses=dict(values=lens_values, weights=lens_weights, central=central,
                ranges={k: list(v) for k, v in lens_ranges.items()},
                low=low, high=high,
                relative=dict(ebitda_27=ebitda_f[1], multiple=MULT_EV_EBITDA, ev=rel_ev_now,
                              equity=rel_equity, peer_median=PEER_EV_EBITDA_MED),
                normalised=dict(margin=norm_margin, ebitda=norm_ebitda, ebit=norm_ebit,
                                net_finance=norm_net_fin, earnings=norm_earnings, eps=norm_eps,
                                multiple=MULT_PE, peer_median=PEER_PE_MED),
                book=dict(bvps=bvps_now, roe=SUSTAINABLE_ROE, justified_pb=justified_pb,
                          ke_terminal=KE_TERM),
                expert_median=expert_median),
    sensitivity=dict(g_grid=g_grid, w_grid=w_grid, grid_growth_wacc=grid_g_w,
                     m_grid=m_grid, grid_margin_wacc=grid_m_w, single=single,
                     base=A['fv']),
    experts=experts,
    peers=PEERS,
    trailing=dict(ev=MKTCAP + NET_DEBT_A, ev_ebitda=(MKTCAP + NET_DEBT_A) / ebitda[2],
                  pe=SPOT / eps[2], pb=SPOT / (EQUITY[2] / SH),
                  dividend_yield=DIV_FY25_DECL / MKTCAP,
                  net_debt_ebitda=NET_DEBT_A / ebitda[2]),
    assert_log=ASSERTS, log=LOG,
)

for k, v in I.items():
    for f in ('value', 'source', 'date', 'layer'):
        chk(f'input {k} carries a {f}', v.get(f) is not None and v.get(f) != '',
            f'input {k} is missing {f}')
log(f'Input register: {len(I)} inputs, every one four-field complete')

with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(OUT, f, indent=1, default=float)
log(f'wrote study_numbers.json — {len(ASSERTS)} internal checks, all passed')
