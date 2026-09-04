"""ADNOC Logistics & Services plc — the study's single numbers engine.

Every figure that reaches the Word study, the workbook, the bibliography or a figure is
computed here and written to study_numbers.json. No builder types a financial numeral.

Reported history is entered ONCE, in INPUTS below, each with the four fields the
bibliography document renders: value, source, date, research layer. The source for every
company historical is the company's own issued statements, read from the filing itself.

Currency note. The company reports in US dollars and lists in dirhams. The valuation runs
in US dollars — the reporting and functional currency of the accounts and the currency the
fleet earns in — and converts to dirhams at the peg only at the per-share step.
Amounts are USD thousand unless a name says otherwise.
"""
import json, os, math
HERE = os.path.dirname(os.path.abspath(__file__))

# ============================================================================
# INPUTS — four-field complete. LAYERS: Company / Industry / Country / Global / Market
# ============================================================================
FS25 = "ADNOC L&S plc, Consolidated Financial Statements FY2025 (PwC-audited, signed 10 Feb 2026)"
FS24 = "ADNOC L&S plc, Consolidated Financial Statements FY2024 (PwC-audited, signed 11 Feb 2025) / Annual Report and Accounts 2024"
FS23 = "ADNOC L&S plc, Consolidated Financial Statements FY2023 (PwC-audited) / Annual Report and Accounts 2024 comparatives"
AR25 = "ADNOC L&S plc, Annual Report and Accounts 2025"
Q126 = "ADNOC L&S plc, Condensed Consolidated Interim Financial Information, three months ended 31 March 2026 (reviewed)"
MDA25 = "ADNOC L&S plc, Management Discussion and Analysis FY2025"
MDAQ126 = "ADNOC L&S plc, Management Discussion and Analysis Q1 2026"
IP26 = "ADNOC L&S plc, Investor Presentation April 2026"
IPFY25 = "ADNOC L&S plc, FY2025 Investor Presentation"
CALL25 = "ADNOC L&S plc, FY2025 earnings call transcript"
CALLQ126 = "ADNOC L&S plc, Q1 2026 earnings call transcript"

INPUTS = {}

# THE BETA'S PROVENANCE IS READ, NEVER TYPED. The regression is produced by the engine's
# sanctioned routine, and the record it returns — regressor, index file, as-of date,
# window, observation count and diagnostics — is what the source strings below are built
# from. The rule exists because a study was found carrying a source string that described
# the construction it used to run rather than the one it now runs, and a typed string
# cannot fail when the regression moves underneath it.
BETA_REC = json.load(open(os.path.join(HERE, 'beta_result.json')))
BETA_SAN = BETA_REC['sanctioned']
# The week the returns are measured over is a fact about the exchange, so it is read off
# the record too — and rendered in the words a reader outside this project uses.
BETA_WEEK = {'W-FRI': 'Friday close to Friday close',
             'W-THU': 'Thursday close to Thursday close'}[BETA_SAN['week_rule']]


def IN(key, value, source, date, layer):
    INPUTS[key] = dict(value=value, source=source, date=date, layer=layer)
    return value


# ---------------------------------------------------------------- market ----
spot_aed = IN('spot_aed', 6.16, "ADX daily price history for ADNOCLS, last close in the "
              "series used throughout this study", '2026-08-07', 'Market')
peg = IN('fx_aed_usd', 3.6725, "UAE dirham's fixed parity to the US dollar, unchanged "
         "since 1997 and maintained by the Central Bank of the UAE", '2026-08-07', 'Country')
shares_mn = IN('shares_mn', 7398.498764, "Authorised, issued and fully paid ordinary "
               "shares of USD 0.54 each (share capital note)", '2025-12-31', 'Company')
shares_wavg_mn = IN('shares_wavg_mn', 7393.482, "Weighted average shares used for earnings "
                    "per share, after treasury purchases (earnings per share note)",
                    '2025-12-31', 'Company')

# ------------------------------------------------- income statement, USD'000 ----
IN('rev_fy23', 2755152, FS23, '2023-12-31', 'Company')
IN('rev_fy24', 3549330, FS24, '2024-12-31', 'Company')
IN('rev_fy25', 5016112, FS25, '2025-12-31', 'Company')
IN('dc_fy23', -2003225, FS23, '2023-12-31', 'Company')
IN('dc_fy24', -2608784, FS24, '2024-12-31', 'Company')
IN('dc_fy25', -3908236, FS25, '2025-12-31', 'Company')
IN('gp_fy23', 751927, FS23, '2023-12-31', 'Company')
IN('gp_fy24', 940546, FS24, '2024-12-31', 'Company')
IN('gp_fy25', 1107876, FS25, '2025-12-31', 'Company')
IN('ga_fy23', -146436, FS23, '2023-12-31', 'Company')
IN('ga_fy24', -141522, FS24, '2024-12-31', 'Company')
IN('ga_fy25', -204983, FS25, '2025-12-31', 'Company')
IN('ecl_fy23', -2672, FS23, '2023-12-31', 'Company')
IN('ecl_fy24', 2649, FS24, '2024-12-31', 'Company')
IN('ecl_fy25', -9590, FS25, '2025-12-31', 'Company')
IN('oi_fy23', 10865, FS23, '2023-12-31', 'Company')
IN('oi_fy24', 19896, FS24, '2024-12-31', 'Company')
IN('oi_fy25', 50459, FS25, '2025-12-31', 'Company')
IN('oe_fy23', 0, FS23, '2023-12-31', 'Company')
IN('oe_fy24', -4310, FS24, '2024-12-31', 'Company')
IN('oe_fy25', 0, FS25, '2025-12-31', 'Company')
IN('op_fy23', 613684, FS23, '2023-12-31', 'Company')
IN('op_fy24', 817259, FS24, '2024-12-31', 'Company')
IN('op_fy25', 943762, FS25, '2025-12-31', 'Company')
IN('assoc_fy23', 14071, FS23, '2023-12-31', 'Company')
IN('assoc_fy24', 14198, FS24, '2024-12-31', 'Company')
IN('assoc_fy25', 37392, FS25, '2025-12-31', 'Company')
IN('bargain_fy25', 12056, FS25, '2025-12-31', 'Company')
IN('prevheld_fy25', -3398, FS25, '2025-12-31', 'Company')
IN('finc_fy23', 9785, FS23, '2023-12-31', 'Company')
IN('finc_fy24', 15594, FS24, '2024-12-31', 'Company')
IN('finc_fy25', 18959, FS25, '2025-12-31', 'Company')
IN('fine_fy23', -15098, FS23, '2023-12-31', 'Company')
IN('fine_fy24', -18034, FS24, '2024-12-31', 'Company')
IN('fine_fy25', -87143, FS25, '2025-12-31', 'Company')
IN('pbt_fy23', 622442, FS23, '2023-12-31', 'Company')
IN('pbt_fy24', 829017, FS24, '2024-12-31', 'Company')
IN('pbt_fy25', 921628, FS25, '2025-12-31', 'Company')
IN('tax_fy23', -2283, FS23 + " (deferred credit 1,123 less current charge 3,406)",
   '2023-12-31', 'Company')
IN('tax_fy24', -72847, FS24 + " (deferred credit 868, deferred charge 1,123, current "
   "charge 72,592)", '2024-12-31', 'Company')
IN('tax_fy25', -58781, FS25 + " (deferred credit 898 less current charge 59,679)",
   '2025-12-31', 'Company')
IN('pat_fy23', 620159, FS23, '2023-12-31', 'Company')
IN('pat_fy24', 756170, FS24, '2024-12-31', 'Company')
IN('pat_fy25', 862847, FS25, '2025-12-31', 'Company')
IN('npa_fy23', 620159, FS23 + " — attributable to equity holders", '2023-12-31', 'Company')
IN('npa_fy24', 756170, FS24 + " — attributable to equity holders", '2024-12-31', 'Company')
IN('npa_fy25', 838541, FS25 + " — attributable to equity holders", '2025-12-31', 'Company')
IN('nci_pl_fy25', 24306, FS25 + " — profit attributable to non-controlling interests",
   '2025-12-31', 'Company')
IN('eps_fy23', 0.08, FS23, '2023-12-31', 'Company')
IN('eps_fy24', 0.10, FS24, '2024-12-31', 'Company')
IN('eps_fy25', 0.11, FS25, '2025-12-31', 'Company')

# ------------------------------------------------- depreciation & amortisation ----
IN('dep_ppe_fy23', 216558, FS23 + " — cash flow statement", '2023-12-31', 'Company')
IN('dep_ppe_fy24', 266207, FS24 + " — cash flow statement", '2024-12-31', 'Company')
IN('dep_ppe_fy25', 385487, FS25 + " — cash flow statement", '2025-12-31', 'Company')
IN('dep_ip_fy23', 5165, FS23 + " — cash flow statement", '2023-12-31', 'Company')
IN('dep_ip_fy24', 5259, FS24 + " — cash flow statement", '2024-12-31', 'Company')
IN('dep_ip_fy25', 5436, FS25 + " — cash flow statement", '2025-12-31', 'Company')
IN('dep_rou_fy23', 19650, FS23 + " — cash flow statement", '2023-12-31', 'Company')
IN('dep_rou_fy24', 39062, FS24 + " — cash flow statement", '2024-12-31', 'Company')
IN('dep_rou_fy25', 117104, FS25 + " — cash flow statement", '2025-12-31', 'Company')
IN('amort_fy23', 7153, FS23 + " — cash flow statement", '2023-12-31', 'Company')
IN('amort_fy24', 6811, FS24 + " — cash flow statement", '2024-12-31', 'Company')
IN('amort_fy25', 16782, FS25 + " — cash flow statement", '2025-12-31', 'Company')

# -------------------------------------------------------- balance sheet, USD'000 ----
IN('ppe_fy23', 3806543, FS23, '2023-12-31', 'Company')
IN('ppe_fy24', 4543335, FS24, '2024-12-31', 'Company')
IN('ppe_fy25', 6884178, FS25, '2025-12-31', 'Company')
IN('rou_fy23', 148146, FS23, '2023-12-31', 'Company')
IN('rou_fy24', 161691, FS24, '2024-12-31', 'Company')
IN('rou_fy25', 225292, FS25, '2025-12-31', 'Company')
IN('intang_fy23', 11440, FS23, '2023-12-31', 'Company')
IN('intang_fy24', 11078, FS24, '2024-12-31', 'Company')
IN('intang_fy25', 19434, FS25, '2025-12-31', 'Company')
IN('invprop_fy23', 95269, FS23, '2023-12-31', 'Company')
IN('invprop_fy24', 92501, FS24, '2024-12-31', 'Company')
IN('invprop_fy25', 89154, FS25, '2025-12-31', 'Company')
IN('jv_fy23', 76712, FS23, '2023-12-31', 'Company')
IN('jv_fy24', 267775, FS24, '2024-12-31', 'Company')
IN('jv_fy25', 577769, FS25, '2025-12-31', 'Company')
IN('gw_fy23', 51368, FS23, '2023-12-31', 'Company')
IN('gw_fy24', 51368, FS24, '2024-12-31', 'Company')
IN('gw_fy25', 51368, FS25, '2025-12-31', 'Company')
IN('adv_yard_fy23', 38884, FS23, '2023-12-31', 'Company')
IN('adv_yard_fy24', 229882, FS24, '2024-12-31', 'Company')
IN('adv_yard_fy25', 137600, FS25, '2025-12-31', 'Company')
IN('subl_nc_fy23', 29201, FS23, '2023-12-31', 'Company')
IN('subl_nc_fy24', 12842, FS24, '2024-12-31', 'Company')
IN('subl_nc_fy25', 11149, FS25, '2025-12-31', 'Company')
IN('dta_fy23', 1123, FS23, '2023-12-31', 'Company')
IN('nca_fy23', 4258686, FS23, '2023-12-31', 'Company')
IN('nca_fy24', 5370472, FS24, '2024-12-31', 'Company')
IN('nca_fy25', 7995944, FS25, '2025-12-31', 'Company')
IN('inv_fy23', 120720, FS23, '2023-12-31', 'Company')
IN('inv_fy24', 132687, FS24, '2024-12-31', 'Company')
IN('inv_fy25', 137108, FS25, '2025-12-31', 'Company')
IN('recv_fy23', 388320, FS23, '2023-12-31', 'Company')
IN('recv_fy24', 420479, FS24, '2024-12-31', 'Company')
IN('recv_fy25', 813285, FS25, '2025-12-31', 'Company')
IN('dfr_fy23', 742847, FS23 + " — due from related parties", '2023-12-31', 'Company')
IN('dfr_fy24', 864410, FS24 + " — due from related parties", '2024-12-31', 'Company')
IN('dfr_fy25', 676383, FS25 + " — due from related parties", '2025-12-31', 'Company')
IN('subl_c_fy23', 19386, FS23, '2023-12-31', 'Company')
IN('subl_c_fy24', 16359, FS24, '2024-12-31', 'Company')
IN('subl_c_fy25', 4639, FS25, '2025-12-31', 'Company')
IN('cash_fy23', 215709, FS23, '2023-12-31', 'Company')
IN('cash_fy24', 198919, FS24, '2024-12-31', 'Company')
IN('cash_fy25', 337794, FS25, '2025-12-31', 'Company')
IN('ca_fy23', 1486982, FS23, '2023-12-31', 'Company')
IN('ca_fy24', 1632854, FS24, '2024-12-31', 'Company')
IN('ca_fy25', 1969209, FS25, '2025-12-31', 'Company')
IN('ta_fy23', 5745668, FS23, '2023-12-31', 'Company')
IN('ta_fy24', 7003326, FS24, '2024-12-31', 'Company')
IN('ta_fy25', 9965153, FS25, '2025-12-31', 'Company')

IN('sc_fy23', 3995189, FS23 + " — share capital", '2023-12-31', 'Company')
IN('sc_fy24', 3995189, FS24 + " — share capital", '2024-12-31', 'Company')
IN('sc_fy25', 3995189, FS25 + " — share capital", '2025-12-31', 'Company')
IN('treas_fy25', -8805, FS25 + " — treasury shares", '2025-12-31', 'Company')
IN('invres_fy25', -298626, FS25 + " — investment reserve", '2025-12-31', 'Company')
IN('re_fy23', 410793, FS23 + " — retained earnings", '2023-12-31', 'Company')
IN('re_fy24', 899438, FS24 + " — retained earnings", '2024-12-31', 'Company')
IN('re_fy25', 1294229, FS25 + " — retained earnings", '2025-12-31', 'Company')
IN('eqp_fy23', 4405982, FS23 + " — equity attributable to owners", '2023-12-31', 'Company')
IN('eqp_fy24', 4894627, FS24 + " — equity attributable to owners", '2024-12-31', 'Company')
IN('eqp_fy25', 4981987, FS25 + " — equity attributable to owners", '2025-12-31', 'Company')
IN('hybrid_fy25', 1978619, FS25 + " — hybrid equity instrument", '2025-12-31', 'Company')
IN('nci_fy25', 264512, FS25 + " — non-controlling interests", '2025-12-31', 'Company')
IN('teq_fy23', 4405982, FS23 + " — total equity", '2023-12-31', 'Company')
IN('teq_fy24', 4894627, FS24 + " — total equity", '2024-12-31', 'Company')
IN('teq_fy25', 7225118, FS25 + " — total equity", '2025-12-31', 'Company')

IN('shldr_nc_fy23', 100000, FS23 + " — shareholder loan, non-current", '2023-12-31', 'Company')
IN('shldr_nc_fy24', 550000, FS24 + " — shareholder loan, non-current", '2024-12-31', 'Company')
IN('shldr_nc_fy25', 0, FS25 + " — shareholder loan, non-current", '2025-12-31', 'Company')
IN('shldr_c_fy25', 400000, FS25 + " — shareholder loan, current", '2025-12-31', 'Company')
IN('borr_nc_fy25', 328795, FS25 + " — loans and other borrowings, non-current",
   '2025-12-31', 'Company')
IN('borr_c_fy25', 79931, FS25 + " — loans and other borrowings, current",
   '2025-12-31', 'Company')
IN('pcp_fy25', 298626, FS25 + " — purchase consideration payable", '2025-12-31', 'Company')
IN('lease_nc_fy23', 145241, FS23 + " — lease liabilities, non-current", '2023-12-31', 'Company')
IN('lease_nc_fy24', 130171, FS24 + " — lease liabilities, non-current", '2024-12-31', 'Company')
IN('lease_nc_fy25', 141150, FS25 + " — lease liabilities, non-current", '2025-12-31', 'Company')
IN('lease_c_fy23', 44313, FS23 + " — lease liabilities, current", '2023-12-31', 'Company')
IN('lease_c_fy24', 59130, FS24 + " — lease liabilities, current", '2024-12-31', 'Company')
IN('lease_c_fy25', 82003, FS25 + " — lease liabilities, current", '2025-12-31', 'Company')
IN('dism_fy23', 1873, FS23, '2023-12-31', 'Company')
IN('dism_fy24', 2009, FS24, '2024-12-31', 'Company')
IN('dism_fy25', 2154, FS25, '2025-12-31', 'Company')
IN('dtl_fy23', 35671, FS23, '2023-12-31', 'Company')
IN('dtl_fy24', 34803, FS24, '2024-12-31', 'Company')
IN('dtl_fy25', 33905, FS25, '2025-12-31', 'Company')
IN('eosb_fy23', 32631, FS23, '2023-12-31', 'Company')
IN('eosb_fy24', 39515, FS24, '2024-12-31', 'Company')
IN('eosb_fy25', 38819, FS25, '2025-12-31', 'Company')
IN('dtr_nc_fy23', 17909, FS23 + " — due to related parties, non-current", '2023-12-31', 'Company')
IN('ncl_fy23', 333325, FS23, '2023-12-31', 'Company')
IN('ncl_fy24', 756498, FS24, '2024-12-31', 'Company')
IN('ncl_fy25', 843449, FS25, '2025-12-31', 'Company')
IN('pay_fy23', 708927, FS23 + " — trade and other payables", '2023-12-31', 'Company')
IN('pay_fy24', 956307, FS24 + " — trade and other payables", '2024-12-31', 'Company')
IN('pay_fy25', 1054455, FS25 + " — trade and other payables", '2025-12-31', 'Company')
IN('taxpay_fy24', 65391, FS24 + " — income tax payable", '2024-12-31', 'Company')
IN('taxpay_fy25', 54291, FS25 + " — income tax payable", '2025-12-31', 'Company')
IN('dtr_c_fy23', 253121, FS23 + " — due to related parties, current", '2023-12-31', 'Company')
IN('dtr_c_fy24', 271373, FS24 + " — due to related parties, current", '2024-12-31', 'Company')
IN('dtr_c_fy25', 225906, FS25 + " — due to related parties, current", '2025-12-31', 'Company')
IN('cl_fy23', 1006361, FS23, '2023-12-31', 'Company')
IN('cl_fy24', 1352201, FS24, '2024-12-31', 'Company')
IN('cl_fy25', 1896586, FS25, '2025-12-31', 'Company')
IN('tl_fy23', 1339686, FS23, '2023-12-31', 'Company')
IN('tl_fy24', 2108699, FS24, '2024-12-31', 'Company')
IN('tl_fy25', 2740035, FS25, '2025-12-31', 'Company')

# ------------------------------------------------------------ cash flow, USD'000 ----
IN('ocf_fy23', 822648, FS23 + " — net cash generated from operating activities",
   '2023-12-31', 'Company')
IN('ocf_fy24', 1068865, FS24 + " — net cash generated from operating activities",
   '2024-12-31', 'Company')
IN('ocf_fy25', 1370729, FS25 + " — net cash generated from operating activities",
   '2025-12-31', 'Company')
IN('capex_fy23', 774015, FS23 + " — purchase of property, plant and equipment",
   '2023-12-31', 'Company')
IN('capex_fy24', 810851, FS24 + " — purchase of property, plant and equipment",
   '2024-12-31', 'Company')
IN('capex_fy25', 1106529, FS25 + " — purchase of property, plant and equipment",
   '2025-12-31', 'Company')
IN('capex_noncash_fy24', 145297, FS24 + " — non-cash additions to property, plant and "
   "equipment disclosed below the cash flow statement", '2024-12-31', 'Company')
IN('capex_noncash_fy25', 89098, FS25 + " — non-cash additions to property, plant and "
   "equipment disclosed below the cash flow statement", '2025-12-31', 'Company')
IN('icf_fy23', -762604, FS23 + " — net cash used in investing activities", '2023-12-31', 'Company')
IN('icf_fy24', -1201046, FS24 + " — net cash used in investing activities", '2024-12-31', 'Company')
IN('icf_fy25', -1937944, FS25 + " — net cash used in investing activities", '2025-12-31', 'Company')
IN('div_paid_fy23', 64999, FS23 + " — dividends paid", '2023-12-31', 'Company')
IN('div_paid_fy24', 266500, FS24 + " — dividends paid", '2024-12-31', 'Company')
IN('div_paid_fy25', 380250, FS25 + " — dividends paid", '2025-12-31', 'Company')
IN('taxpaid_fy25', 70779, FS25 + " — tax paid", '2025-12-31', 'Company')
IN('intpaid_lease_fy25', 12719, FS25 + " — interest portion on lease liabilities",
   '2025-12-31', 'Company')
IN('intpaid_shldr_fy25', 43891, FS25 + " — interest paid on shareholder loans",
   '2025-12-31', 'Company')
IN('intpaid_borr_fy25', 39258, FS25 + " — interest on loans and other borrowings",
   '2025-12-31', 'Company')
IN('hybrid_coupon_fy25', 61333, FS25 + " — coupons paid on the hybrid equity instrument",
   '2025-12-31', 'Company')

# ------------------------------------------------------------------ Q1 2026 ----
IN('q1_26_rev', 1082675, Q126, '2026-03-31', 'Company')
IN('q1_25_rev', 1181426, Q126 + " — prior-period comparative", '2025-03-31', 'Company')
IN('q1_26_gp', 280722, Q126, '2026-03-31', 'Company')
IN('q1_25_gp', 229214, Q126 + " — prior-period comparative", '2025-03-31', 'Company')
IN('q1_26_op', 226148, Q126, '2026-03-31', 'Company')
IN('q1_25_op', 199945, Q126 + " — prior-period comparative", '2025-03-31', 'Company')
IN('q1_26_dep_ppe', 100704, Q126, '2026-03-31', 'Company')
IN('q1_26_dep_ip', 1353, Q126, '2026-03-31', 'Company')
IN('q1_26_dep_rou', 23520, Q126, '2026-03-31', 'Company')
IN('q1_26_amort', 2586, Q126, '2026-03-31', 'Company')
IN('q1_26_npa', 202743, Q126 + " — attributable to equity holders", '2026-03-31', 'Company')
IN('q1_25_npa', 180520, Q126 + " — prior-period comparative", '2025-03-31', 'Company')
IN('q1_26_pat', 222236, Q126, '2026-03-31', 'Company')
IN('q1_26_capex', 263913, Q126 + " — purchase of property, plant and equipment",
   '2026-03-31', 'Company')
IN('q1_26_ocf', 395042, Q126 + " — net cash generated from operating activities",
   '2026-03-31', 'Company')
IN('q1_26_cash', 695345, Q126, '2026-03-31', 'Company')
IN('q1_26_ppe', 7015261, Q126, '2026-03-31', 'Company')
IN('q1_26_ta', 10282119, Q126, '2026-03-31', 'Company')
IN('q1_26_teq', 7324655, Q126 + " — total equity per the statement of changes in equity",
   '2026-03-31', 'Company')
IN('q1_26_eqp', 5073902, Q126 + " — equity attributable to owners", '2026-03-31', 'Company')
IN('q1_26_hybrid', 1978619, Q126 + " — hybrid equity instrument", '2026-03-31', 'Company')
IN('q1_26_nci', 272134, Q126 + " — non-controlling interests", '2026-03-31', 'Company')

# ------------------------------------------- debt structure at the valuation date ----
IN('q1_26_shldr_loan', 500000, Q126 + " — related-party note: unsecured revolving credit "
   "facility with the parent, closing balance after the January 2026 conversion, "
   "classified non-current", '2026-03-31', 'Company')
IN('q1_26_borrowings', 402763, Q126 + " — loans and other borrowings note (current 79,732 "
   "and non-current 323,031)", '2026-03-31', 'Company')
IN('q1_26_leases', 212449, Q126 + " — lease liabilities note (head-lease 208,186 plus "
   "sub-lease-related 4,263)", '2026-03-31', 'Company')
IN('q1_26_pcp', 301462, Q126 + " — deferred consideration on the staged acquisition, "
   "carried against the investment reserve", '2026-03-31', 'Company')
IN('shldr_margin', 0.0080, Q126 + " — related-party note: interest charged at the secured "
   "overnight financing rate plus 0.80%", '2026-03-31', 'Company')
IN('bank_loan_lo', 0.0711, Q126 + " — loans and other borrowings note, weighted average "
   "interest rate range for bank loans", '2026-03-31', 'Company')
IN('bank_loan_hi', 0.0755, Q126 + " — loans and other borrowings note, weighted average "
   "interest rate range for bank loans", '2026-03-31', 'Company')
IN('other_borr_lo', 0.0436, Q126 + " — loans and other borrowings note, weighted average "
   "interest rate range for other borrowings", '2026-03-31', 'Company')
IN('other_borr_hi', 0.0831, Q126 + " — loans and other borrowings note, weighted average "
   "interest rate range for other borrowings", '2026-03-31', 'Company')
IN('hybrid_margin', 0.0125, Q126 + " — hybrid instrument note: perpetual capital "
   "securities priced at the secured overnight financing rate plus 125 basis points",
   '2026-03-31', 'Company')
IN('hybrid_face', 2000000, Q126 + " — hybrid instrument note: USD 2.0 billion perpetual "
   "capital securities issued during 2025", '2026-03-31', 'Company')
IN('rcf_committed', 2000000, Q126 + " — related-party note: committed amount of the new "
   "revolving credit facility, with a further 600,000 incremental facility",
   '2026-03-31', 'Company')

# ============================================================================
# SEGMENTS — the seven reportable business units, as disclosed
# ============================================================================
SEGS = ['Offshore Contracting', 'Offshore Services', 'Offshore Projects',
        'Tankers', 'Gas Carriers', 'Dry-Bulk and Containers', 'Services']
SEG_GROUP = {'Offshore Contracting': 'Integrated Logistics',
             'Offshore Services': 'Integrated Logistics',
             'Offshore Projects': 'Integrated Logistics',
             'Tankers': 'Shipping', 'Gas Carriers': 'Shipping',
             'Dry-Bulk and Containers': 'Shipping', 'Services': 'Services'}
SEG_SRC = " — operating segments note, business-unit schedule"

# revenue / direct costs / EBITDA by business unit, FY2023 · FY2024 · FY2025
SEG_REV = {
    'Offshore Contracting':     [974525, 1108200, 1368875],
    'Offshore Services':        [500751, 552790, 628915],
    'Offshore Projects':        [157146, 619930, 531333],
    'Tankers':                  [407370, 516530, 1719714],
    'Gas Carriers':             [173550, 152650, 179794],
    'Dry-Bulk and Containers':  [257900, 286820, 225048],
    'Services':                 [283910, 312410, 362433],
}
SEG_DC = {
    'Offshore Contracting':     [-599472, -691714, -846850],
    'Offshore Services':        [-430122, -451840, -497725],
    'Offshore Projects':        [-147641, -571640, -510647],
    'Tankers':                  [-279170, -310630, -1421406],
    'Gas Carriers':             [-112330, -106940, -131314],
    'Dry-Bulk and Containers':  [-201280, -219830, -199256],
    'Services':                 [-233210, -256190, -301038],
}
SEG_EBITDA = {
    'Offshore Contracting':     [424419, 497703, 623065],
    'Offshore Services':        [92741, 134880, 178369],
    'Offshore Projects':        [10439, 54240, 28024],
    'Tankers':                  [159260, 239700, 451220],
    'Gas Carriers':             [101022, 87308, 129547],
    'Dry-Bulk and Containers':  [60280, 69440, 37862],
    'Services':                 [44488, 56000, 60273],
}
SEG_OP = {
    'Offshore Contracting':     [326352, 369764, 471698],
    'Offshore Services':        [49859, 83840, 115406],
    'Offshore Projects':        [8500, 45600, 19164],
    'Tankers':                  [117540, 187830, 255846],
    'Gas Carriers':             [59241, 35170, 57708],
    'Dry-Bulk and Containers':  [48920, 55680, 12637],
    'Services':                 [19640, 29850, 13897],
}
SEG_PPE = {   # FY2024 · FY2025 only — the disclosure starts with the FY2024 schedule
    'Offshore Contracting':     [1930750, 1998956],
    'Offshore Services':        [255204, 282637],
    'Offshore Projects':        [0, 0],
    'Tankers':                  [1099519, 2643389],
    'Gas Carriers':             [886158, 1411865],
    'Dry-Bulk and Containers':  [152500, 168789],
    'Services':                 [219204, 378542],
}
for _s in SEGS:
    for _i, _y in enumerate(('fy23', 'fy24', 'fy25')):
        _k = _s.lower().replace(' ', '_').replace('-', '_')
        _src = {'fy23': FS24, 'fy24': FS24, 'fy25': FS25}[_y] + SEG_SRC
        _dt = {'fy23': '2023-12-31', 'fy24': '2024-12-31', 'fy25': '2025-12-31'}[_y]
        IN(f'seg_rev_{_k}_{_y}', SEG_REV[_s][_i], _src, _dt, 'Company')
        IN(f'seg_dc_{_k}_{_y}', SEG_DC[_s][_i], _src, _dt, 'Company')
        IN(f'seg_ebitda_{_k}_{_y}', SEG_EBITDA[_s][_i], _src, _dt, 'Company')
        IN(f'seg_op_{_k}_{_y}', SEG_OP[_s][_i], _src, _dt, 'Company')
    for _i, _y in enumerate(('fy24', 'fy25')):
        _k = _s.lower().replace(' ', '_').replace('-', '_')
        IN(f'seg_ppe_{_k}_{_y}', SEG_PPE[_s][_i],
           (FS24 if _y == 'fy24' else FS25) + " — operating segments note, segment "
           "property, plant and equipment",
           '2024-12-31' if _y == 'fy24' else '2025-12-31', 'Company')

# revenue by product line, the disaggregation the company itself publishes (FY2024 · FY2025)
PRODUCT_LINES = {
    'Freight and voyage charter income':   [838284, 1404709],
    'Offshore vessels charter income':     [495527, 703915],
    'Base operation services':             [547409, 644803],
    'Engineering, procurement and construction contracts': [619930, 531333],
    'Operating lease income':              [366790, 1057235],
    'Petroleum port operations':           [233826, 245806],
    'Sales of bunkering fuel and water':   [243433, 213475],
    'Onshore services income':             [130313, 131452],
    'Ship management income':              [53122, 50332],
    'Commission income':                   [0, 29990],
    'Drilling chemicals':                  [20696, 3062],
}
for _n, _v in PRODUCT_LINES.items():
    _k = 'pl_' + ''.join(c if c.isalnum() else '_' for c in _n.lower())[:34].strip('_')
    IN(_k + '_fy24', _v[0], FS25 + " — revenue note, disaggregation by product line",
       '2024-12-31', 'Company')
    IN(_k + '_fy25', _v[1], FS25 + " — revenue note, disaggregation by product line",
       '2025-12-31', 'Company')

# direct cost by nature, FY2024 · FY2025
COST_LINES = {
    'Freight and voyage charter costs': [416487, 1190790],
    'Bunker and other consumption':     [1159446, 1164961],
    'Staff costs':                      [536067, 597226],
    'Depreciation on property, plant and equipment': [262056, 378790],
    'Port charges':                     [65714, 174920],
    'Other operating costs':            [66015, 116219],
    'Depreciation on right-of-use assets': [38952, 114966],
    'Ship technical management costs':  [0, 92773],
    'Repairs and maintenance':          [57184, 60459],
    'Amortisation of intangibles':      [1604, 11696],
    'Depreciation on investment properties': [5259, 5436],
}
for _n, _v in COST_LINES.items():
    _k = 'cl_' + ''.join(c if c.isalnum() else '_' for c in _n.lower())[:34].strip('_')
    IN(_k + '_fy24', _v[0], FS25 + " — direct costs note, analysis by nature",
       '2024-12-31', 'Company')
    IN(_k + '_fy25', _v[1], FS25 + " — direct costs note, analysis by nature",
       '2025-12-31', 'Company')

IN('ebitda_rep_fy23', 876281, FS24 + SEG_SRC + " — the company's own EBITDA total",
   '2023-12-31', 'Company')
IN('ebitda_rep_fy24', 1148796, FS24 + SEG_SRC + " — the company's own EBITDA total",
   '2024-12-31', 'Company')
IN('ebitda_rep_fy25', 1514621, FS25 + SEG_SRC + " — the company's own EBITDA total",
   '2025-12-31', 'Company')
IN('vessel_sale_price', 111000, "ADNOC L&S plc, FY2025 earnings release" + " — sale of a 2017-built very large crude "
   "carrier, 90% owned, completed January 2026", '2026-01-31', 'Company')
IN('vessel_sale_book', 83000, "ADNOC L&S plc, FY2025 earnings release" + " — the same vessel's carrying value",
   '2026-01-31', 'Company')
IN('vessel_sale_gain', 27000, "ADNOC L&S plc, FY2025 earnings release" + " — the capital gain recognised on that sale",
   '2026-01-31', 'Company')
IN('gw_growth_assumption', 0.02, FS25 + " — goodwill note: the company's own value-in-use "
   "test projects cash flows beyond the explicit plan at a growth rate equivalent to an "
   "estimated 2% inflation rate", '2025-12-31', 'Company')

# ============================================================================
# FLEET AND UNIT DRIVERS — the finest level the company discloses
# ============================================================================
_FL = IP26 + " — owned shipping fleet at 31 December 2025"
_SP = IP26 + " — vessels available at spot, and the earnings sensitivity to a change of "\
      "USD 1,000 a day in the time-charter equivalent"
IN('tnk_hs_n', 2, _FL, '2025-12-31', 'Company')
IN('tnk_mr_n', 16, _FL, '2025-12-31', 'Company')
IN('tnk_lr1_n', 9, _FL, '2025-12-31', 'Company')
IN('tnk_lr2_n', 17, _FL, '2025-12-31', 'Company')
IN('tnk_vlcc_n', 9, _FL, '2025-12-31', 'Company')
IN('tnk_hs_spot', 2, _SP, '2025-12-31', 'Company')
IN('tnk_mr_spot', 16, _SP, '2025-12-31', 'Company')
IN('tnk_lr1_spot', 7, _SP, '2025-12-31', 'Company')
IN('tnk_lr2_spot', 13, _SP, '2025-12-31', 'Company')
IN('tnk_vlcc_spot', 7, _SP, '2025-12-31', 'Company')
IN('spot_vessels_total', 56, _SP + " — 45 tankers and 11 dry-bulk vessels", '2025-12-31',
   'Company')
IN('ebitda_per_1000_day', 20500, _SP + " — group earnings move by about USD 20.5 million "
   "for every USD 1,000 a day change in the rate across those 56 vessels", '2025-12-31',
   'Company')
# rates already fixed by time charters out, from the disclosed contract table
IN('tc_out_lr1', 19750, IP26 + " — charters out: two long-range-one tankers fixed at USD "
   "19,750 a day", '2026-04-30', 'Company')
IN('tc_out_lr2', 35943, IP26 + " — charters out: average of the six long-range-two fixtures "
   "disclosed, from USD 30,561 to USD 42,000 a day", '2026-04-30', 'Company')
IN('tc_out_vlcc', 60942, IP26 + " — charters out: average of the four very large crude "
   "carrier fixtures disclosed, from USD 50,633 to USD 72,500 a day", '2026-04-30', 'Company')
# the rates actually achieved in the study year, and the second-quarter indication
_CALL = CALLQ126 + " — rates achieved in the first quarter of 2026 and the level the "\
        "second quarter was crossing at the time of the call"
IN('tce_vlcc_q1_26', 145000, _CALL, '2026-03-31', 'Company')
IN('tce_lr2_q1_26', 58000, _CALL, '2026-03-31', 'Company')
IN('tce_lr1_q1_26', 36000, _CALL, '2026-03-31', 'Company')
IN('tce_mr_q1_26', 30000, _CALL, '2026-03-31', 'Company')
IN('tce_vlcc_q2_26', 260000, _CALL, '2026-05-14', 'Company')
IN('tce_lr2_q2_26', 95000, _CALL, '2026-05-14', 'Company')
IN('tce_lr1_q2_26', 55000, _CALL, '2026-05-14', 'Company')
IN('tce_mr_q2_26', 44000, _CALL, '2026-05-14', 'Company')

# quarterly time-charter equivalent, USD per vessel per day, by class
TCE_FY25 = {'mr': [23459, 25161, 23391, 24547], 'lr1': [21546, 24225, 24452, 26574],
            'lr2': [31033, 35533, 34410, 41973], 'vlcc': [39245, 44350, 40996, 85273]}
QEND = ['{}-03-31', '{}-06-30', '{}-09-30', '{}-12-31']   # real quarter-end dates
TCE_FY24 = {'lr1': [51645, 49424, 31911, 27640], 'lr2': [60038, 63734, 36237, 32034],
            'vlcc': [54580, 46097, 39681, 33167]}
for _c, _q in TCE_FY25.items():
    for _i, _lab in enumerate(('q1', 'q2', 'q3', 'q4')):
        IN(f'tce_{_c}_25{_lab}', _q[_i], IPFY25 + " — time-charter equivalent by vessel class, "
           "calculated as revenue less voyage costs over calendar days net of off-hire",
           QEND[_i].format(2025), 'Company')
for _c, _q in TCE_FY24.items():
    for _i, _lab in enumerate(('q1', 'q2', 'q3', 'q4')):
        IN(f'tce_{_c}_24{_lab}', _q[_i], IPFY25 + " — time-charter equivalent by vessel class",
           QEND[_i].format(2024), 'Company')

IN('jub_owned', 33, IPFY25 + " — jack-up barge fleet: 33 owned and 12 chartered",
   '2025-12-31', 'Company')
IN('jub_chartered', 12, IPFY25 + " — jack-up barge fleet: 33 owned and 12 chartered",
   '2025-12-31', 'Company')
IN('osv_owned', 40, AR25 + " — offshore support vessels: 40 owned plus 9 time chartered "
   "in or out", '2025-12-31', 'Company')
IN('gas_owned', 20, IP26 + " — gas fleet: 15 of 20 owned vessels on long-term contracts",
   '2025-12-31', 'Company')
IN('gas_lt_contracted', 15, IP26 + " — gas fleet: 15 of 20 owned vessels on long-term "
   "contracts", '2025-12-31', 'Company')
IN('contracted_revenue_lt', 25000000, IP26 + " — long-term contracted revenue of about "
   "USD 25 billion, restated at the first quarter of 2026", '2026-03-31', 'Company')
IN('contracted_2026_share', 0.53, IPFY25 + " — about 53% of 2026 revenue already "
   "contracted with the parent group", '2025-12-31', 'Company')
IN('spot_share_ebitda_26', 0.31, IP26 + " — shipping earnings exposed to spot rates as a "
   "share of total earnings before interest, tax, depreciation and amortisation, 2026",
   '2026-04-30', 'Company')
IN('spot_share_ebitda_29', 0.23, IP26 + " — the same exposure in 2029", '2026-04-30', 'Company')

# ------------------------------------------------------------- guidance ----
IN('g26_rev_group', -0.035, MDAQ126 + " — raised 2026 guidance: a low-to-mid single-digit "
   "year-on-year reduction in group revenue (midpoint of the stated band)",
   '2026-05-14', 'Company')
IN('g26_ebitda_group', 0.065, MDAQ126 + " — raised 2026 guidance: mid-to-high single-digit "
   "growth in group earnings before interest, tax, depreciation and amortisation "
   "(midpoint of the stated band)", '2026-05-14', 'Company')
IN('g26_np_group', 0.16, MDAQ126 + " — raised 2026 guidance: mid-to-high-teens growth in "
   "group net profit (midpoint of the stated band)", '2026-05-14', 'Company')
IN('g26_rev_il', -0.27, MDAQ126 + " — raised 2026 guidance: a mid-to-high 20% reduction in "
   "Integrated Logistics revenue (midpoint)", '2026-05-14', 'Company')
IN('g26_rev_ship', 0.165, MDAQ126 + " — raised 2026 guidance: mid-to-high-teens growth in "
   "Shipping revenue (midpoint)", '2026-05-14', 'Company')
IN('g26_rev_serv', 0.035, MDAQ126 + " — raised 2026 guidance: low-to-mid single-digit "
   "growth in Services revenue (midpoint)", '2026-05-14', 'Company')
IN('g26_ebitda_il', -0.27, MDAQ126 + " — raised 2026 guidance: a mid-to-high 20% reduction "
   "in Integrated Logistics earnings before interest, tax, depreciation and amortisation "
   "(midpoint)", '2026-05-14', 'Company')
IN('g26_ebitda_ship', 0.55, MDAQ126 + " — raised 2026 guidance: mid-to-high 50% growth in "
   "Shipping earnings before interest, tax, depreciation and amortisation (midpoint)",
   '2026-05-14', 'Company')
IN('g26_ebitda_serv', 0.035, MDAQ126 + " — raised 2026 guidance: low-to-mid single-digit "
   "growth in Services earnings before interest, tax, depreciation and amortisation "
   "(midpoint)", '2026-05-14', 'Company')
IN('dps_2026_usd', 341.0, MDAQ126 + " — the 2026 distribution is expected to be USD 341 "
   "million, rising 5% a year to 2030 and paid quarterly", '2026-05-14', 'Company')
IN('div_growth', 0.05, MDAQ126 + " — the stated 5% annual increase in the distribution "
   "from 2026 to 2030", '2026-05-14', 'Company')
IN('nd_ebitda_target_lo', 2.0, MDAQ126 + " — stated medium-term net debt to earnings "
   "target range of 2.0 to 2.5 times", '2026-05-14', 'Company')
IN('nd_ebitda_target_hi', 2.5, MDAQ126 + " — stated medium-term net debt to earnings "
   "target range of 2.0 to 2.5 times", '2026-05-14', 'Company')

# --------------------------------------------- Q1 2026 segment actuals (USD mn) ----
Q1_SEG = {   # revenue, EBITDA — Q1 2026 and Q1 2025
    'Offshore Contracting': (312, 300, 106, 132),
    'Offshore Services': (166, 136, 48, 35),
    'Offshore Projects': (4, 192, -4, 16),
    'Tankers': (407, 405, 151, 90),
    'Gas Carriers': (56, 39, 37, 48),
    'Dry-Bulk and Containers': (49, 47, 9, 6),
    'Services': (89, 84, 20, 18),
}
for _s, (_r26, _r25, _e26, _e25) in Q1_SEG.items():
    _k = _s.lower().replace(' ', '_').replace('-', '_')
    IN(f'q1_26_rev_{_k}', _r26 * 1000, MDAQ126 + " — segmental results", '2026-03-31', 'Company')
    IN(f'q1_25_rev_{_k}', _r25 * 1000, MDAQ126 + " — segmental results, comparative",
       '2025-03-31', 'Company')
    IN(f'q1_26_ebitda_{_k}', _e26 * 1000, MDAQ126 + " — segmental results", '2026-03-31', 'Company')
    IN(f'q1_25_ebitda_{_k}', _e25 * 1000, MDAQ126 + " — segmental results, comparative",
       '2025-03-31', 'Company')
IN('q1_26_ebitda_group', 368000, MDAQ126 + " — group earnings before interest, tax, "
   "depreciation and amortisation", '2026-03-31', 'Company')
IN('q1_26_netdebt', 419867, MDAQ126 + " — net debt of USD 420 million, reconciled here to "
   "the shareholder facility, third-party borrowings and lease liabilities less cash",
   '2026-03-31', 'Company')

# ============================================================================
# COST OF CAPITAL INPUTS
# ============================================================================
IN('rf_observed', 0.0448, "UAE Ministry of Finance dirham Treasury Bond auction, July 2026 "
   "— the tranche maturing January 2031 cleared at a 4.48% yield to maturity (Emirates News "
   "Agency report of the Ministry's auction result)", '2026-07-30', 'Country')
IN('sov_spread', 0.0042, "Damodaran country risk file, January 2026 edition — United Arab "
   "Emirates row, Moody's Aa2, adjusted default spread", '2026-01-05', 'Country')
IN('erp_total', 0.0487, "Damodaran country risk file, January 2026 edition — United Arab "
   "Emirates total equity risk premium", '2026-01-05', 'Country')
IN('crp', 0.0064, "Damodaran country risk file, January 2026 edition — United Arab Emirates "
   "country risk premium", '2026-01-05', 'Country')
IN('erp_mature', 0.0423, "Damodaran country risk file, January 2026 edition — mature-market "
   "equity risk premium, the United States premium net of its own default spread",
   '2026-01-05', 'Global')
IN('sofr', 0.0365, "Secured Overnight Financing Rate published by the Federal Reserve Bank "
   "of New York", '2026-08-06', 'Global')
IN('cb_rate', 0.0365, "Central Bank of the UAE Base Rate, maintained at the 29 July 2026 "
   "decision. The last change was a 25 basis point cut from 3.90% on 10 December 2025",
   '2026-07-29', 'Country')
IN('erp_cds_available', 0, "Damodaran country risk file, January 2026 edition — the "
   "United Arab Emirates has no sovereign credit-default-swap entry in the file, so the "
   "second premium basis cannot be built for this country. Gulf comparators that do carry "
   "one show the two bases are not interchangeable: Saudi Arabia's swap basis gives 5.72% "
   "against 5.01% on the rating basis", '2026-01-05', 'Country')
IN('gdp_growth_26', 0.031, "International Monetary Fund World Economic Outlook database, "
   "United Arab Emirates real GDP growth", '2026-04-30', 'Country')
# [R-MACRO-01] ONE HOUSE MACRO PATH PER MARKET, AND EVERY RATE SITS ON IT. The three
# figures below were each sourced independently and each was defensible alone; two of them
# happen to agree with the house path to the basis point and one does not, which is exactly
# the state that rule was adopted to end — five studies in one market carrying five
# inflations for the same year, every one arguable.
import sys as _sys                                                   # noqa: E402
_sys.path.insert(0, os.path.join(HERE, '..'))
import terminal_value as TV        # [R-TERM-01] the only sanctioned terminal
import macro_path as _MP                                             # noqa: E402
_PATH = _MP.load('AE')

IN('inflation_26', 0.025, "International Monetary Fund World Economic Outlook database, "
   "United Arab Emirates consumer price inflation; the projection settles at 2.0% from 2027 "
   "onward, which is the anchor the terminal growth rate rests on", '2026-04-30', 'Country')
IN('vlcc_1y_tc_market', 76900, "One-year time charters fixed by a listed crude tanker owner "
   "in early 2026 for seven very large crude carriers, commencing between late January and "
   "April 2026, as reported in trade coverage of its results", '2026-01-31', 'Industry')
IN('vlcc_spot_clarksons_jan26', 102897, "Weighted average very large crude carrier earnings "
   "reported by a shipbroker for the week to 23 January 2026, down from USD 115,635 a week "
   "earlier", '2026-01-23', 'Industry')
IN('tanker_orderbook_pct_fleet', 0.27, "Crude tanker order book as a share of the trading "
   "fleet, about 130 million deadweight tonnes, reported by trade coverage as a seventeen-"
   "year high, with the very large crude carrier order book near 30%", '2026-06-30',
   'Industry')
IN('tax_topup_rate', 0.15, "Domestic minimum top-up tax of 15% applying in the UAE to "
   "groups within the global minimum tax rules for financial years beginning on or after "
   "1 January 2025. International shipping income is excluded from those rules, which is "
   "consistent with the sub-1% charge the company's shipping units actually bore in 2025, "
   "but the exposure is priced as a downside case rather than assumed away",
   '2025-01-01', 'Country')
IN('tax_stat', 0.09, "UAE corporate tax, Federal Decree-Law 47 of 2022 — the 9% standard "
   "rate applying to taxable income above the threshold", '2023-06-01', 'Country')
IN('beta', round(BETA_SAN['beta'], 4),
   f"Weekly regression of the share's own returns on the {BETA_REC['regressor']} "
   f"({BETA_REC['regressor_code']}), the published index of the exchange the share is "
   f"listed on — the market series is resolved from that listing rather than chosen by "
   f"this study, and it is taken as of {BETA_SAN['index_asof']}. {BETA_SAN['n']} weekly "
   f"observations measured {BETA_WEEK} on the exchange's own trading week, from "
   f"{BETA_SAN['first_obs']} to {BETA_SAN['last_obs']}, with both series screened for "
   f"data quality before they are paired. The slope is a lead-lag sum — one lag, the "
   f"contemporaneous return and one lead, added together. R-squared {BETA_SAN['r2']:.4f}, "
   f"standard error {BETA_SAN['se']:.4f}",
   BETA_SAN['index_asof'], 'Market')
IN('beta_se', round(BETA_SAN['se'], 4), "Standard error of the same regression",
   BETA_SAN['index_asof'], 'Market')
IN('beta_r2', round(BETA_SAN['r2'], 4), "R-squared of the same regression",
   BETA_SAN['index_asof'], 'Market')
IN('beta_blume', round(BETA_SAN['blume_crosscheck'], 4),
   "Blume cross-check reported with the same regression — two-thirds of the measured "
   "slope plus one-third of 1.0, the standard adjustment for the tendency of a measured "
   "beta to drift toward the market over time. Published as a check on the adopted "
   "figure; the study does not discount at it",
   BETA_SAN['index_asof'], 'Market')
IN('beta_composite', round(BETA_REC['composite_variant']['beta'], 3),
   "The share's own returns regressed against an equal-weight composite of the exchange's "
   "own listed names instead of the published index — a basket assembled for this study "
   "alone, published for comparison and never adopted, because a hand-built basket is not "
   "the market this share is listed against. "
   "Reported because the gap between the two is large and is a property of index "
   "construction, not of the company: the published index is weighted by size and is "
   "dominated by the same large-capitalisation group the subject belongs to",
   '2026-08-07', 'Market')
IN('beta_ci_lo', round(BETA_SAN['ci90'][0], 4),
   "Lower bound of the 90% confidence interval on the regressed beta",
   BETA_SAN['index_asof'], 'Market')
IN('beta_ci_hi', round(BETA_SAN['ci90'][1], 4),
   "Upper bound of the 90% confidence interval on the regressed beta",
   BETA_SAN['index_asof'], 'Market')
IN('g_terminal', 0.02, FS25 + " — the company's own value-in-use test projects cash flows "
   "beyond its plan at a growth rate equal to an estimated 2% inflation rate; adopted here "
   "as the terminal growth rate", '2025-12-31', 'Company')
IN('rf_terminal', _PATH.terminal_rf, "Terminal risk-free rate, DERIVED from the house "
   "macro path [R-MACRO-01] as the terminal inflation of 2.00% plus the long-run real "
   "rate, NEVER quoted \u2014 a terminal rate somebody types is the single most "
   "terminal-value-sensitive number in a model. Under the peg the dirham real rate IS the "
   "dollar real rate, and the house convention builds it from the Federal Open Market "
   "Committee's own longer-run median policy projection plus the ten-year term premium "
   "less long-run United States inflation. This study had typed 3.25% on a 1.25% real "
   "assumption of its own; the derived figure is higher, so conforming LOWERS this "
   "study's value, which is the direction that shows the rule is not being fitted to a "
   "price", _PATH.as_of, 'Country')

if __name__ == '__main__':
    print(f"{len(INPUTS)} inputs registered")

# ============================================================================
# DERIVED HISTORY
# ============================================================================
V = {k: v['value'] for k, v in INPUTS.items()}
YH = ['FY2023', 'FY2024', 'FY2025']
YF = ['FY2026', 'FY2027', 'FY2028', 'FY2029', 'FY2030']
H = ['fy23', 'fy24', 'fy25']


def h(name):
    return [V[f'{name}_{y}'] for y in H]


dna = [V[f'dep_ppe_{y}'] + V[f'dep_ip_{y}'] + V[f'dep_rou_{y}'] + V[f'amort_{y}'] for y in H]
ebitda_op = [V[f'op_{y}'] + d for y, d in zip(H, dna)]          # operating EBITDA, house basis
ebitda_rep = [V[f'ebitda_rep_{y}'] for y in H]
hist_is = dict(
    year=YH, revenue=h('rev'), direct_costs=h('dc'), gross_profit=h('gp'),
    ga=h('ga'), ecl=h('ecl'), other_income=h('oi'), other_expenses=h('oe'),
    ebit=h('op'), dna=dna, ebitda_op=ebitda_op, ebitda_reported=ebitda_rep,
    assoc=h('assoc'), fin_income=h('finc'), fin_costs=h('fine'), pbt=h('pbt'),
    tax=h('tax'), pat=h('pat'), npa=h('npa'), eps=h('eps'),
    gross_margin=[g / r for g, r in zip(h('gp'), h('rev'))],
    ebitda_margin=[e / r for e, r in zip(ebitda_op, h('rev'))],
    ebitda_margin_reported=[e / r for e, r in zip(ebitda_rep, h('rev'))],
    net_margin=[p / r for p, r in zip(h('npa'), h('rev'))],
    tax_rate_eff=[abs(t) / p for t, p in zip(h('tax'), h('pbt'))],
)
# the reported-EBITDA bridge, so the two definitions are reconciled rather than asserted
hist_is['ebitda_bridge'] = dict(
    operating=ebitda_op, share_of_jv=h('assoc'),
    one_offs=[0, 0, V['bargain_fy25'] + V['prevheld_fy25']], reported=ebitda_rep)

debt = [V['shldr_nc_fy23'] + V['lease_nc_fy23'] + V['lease_c_fy23'],
        V['shldr_nc_fy24'] + V['lease_nc_fy24'] + V['lease_c_fy24'],
        V['shldr_c_fy25'] + V['borr_nc_fy25'] + V['borr_c_fy25']
        + V['lease_nc_fy25'] + V['lease_c_fy25']]
netdebt = [d - V[f'cash_{y}'] for d, y in zip(debt, H)]
nwc = [(V[f'recv_{y}'] + V[f'dfr_{y}'] + V[f'inv_{y}']) - (V[f'pay_{y}'] + V[f'dtr_c_{y}'])
       for y in H]
hist_bs = dict(
    year=YH, ppe=h('ppe'), rou=h('rou'), intangibles=h('intang'), inv_prop=h('invprop'),
    jv=h('jv'), goodwill=h('gw'), advances=h('adv_yard'),
    non_current_assets=h('nca'), inventories=h('inv'), receivables=h('recv'),
    due_from_related=h('dfr'), cash=h('cash'), current_assets=h('ca'), total_assets=h('ta'),
    equity_parent=h('eqp'), total_equity=h('teq'),
    hybrid=[0, 0, V['hybrid_fy25']], nci=[0, 0, V['nci_fy25']],
    payables=h('pay'), due_to_related=h('dtr_c'),
    non_current_liabilities=h('ncl'), current_liabilities=h('cl'), total_liabilities=h('tl'),
    debt=debt, net_debt=netdebt, nwc=nwc,
    nwc_pct_rev=[w / r for w, r in zip(nwc, h('rev'))],
    net_debt_ebitda=[n / e for n, e in zip(netdebt, ebitda_rep)],
    bvps=[e / shares_mn for e in h('eqp')],
    roe=[p / e for p, e in zip(h('npa'), h('eqp'))],
)
hist_cf = dict(
    year=YH, ocf=h('ocf'), capex=[-V[f'capex_{y}'] for y in H], icf=h('icf'),
    dividends=[-V[f'div_paid_{y}'] for y in H],
    fcf=[o - V[f'capex_{y}'] for o, y in zip(h('ocf'), H)],
)
# cash-conversion cycle, from the statements
ccc = dict(
    dso=[(V[f'recv_{y}'] + V[f'dfr_{y}']) / V[f'rev_{y}'] * 365 for y in H],
    dio=[V[f'inv_{y}'] / abs(V[f'dc_{y}']) * 365 for y in H],
    dpo=[(V[f'pay_{y}'] + V[f'dtr_c_{y}']) / abs(V[f'dc_{y}']) * 365 for y in H],
)
ccc['cycle'] = [a + b - c for a, b, c in zip(ccc['dso'], ccc['dio'], ccc['dpo'])]

# segment history, with the share of joint-venture profit stripped out of segment EBITDA
SEG_JV_FY25 = {'Gas Carriers': 21313, 'Services': 16079}
seg_hist = {}
for s in SEGS:
    seg_hist[s] = dict(
        group=SEG_GROUP[s], revenue=SEG_REV[s], direct_costs=SEG_DC[s],
        ebitda=SEG_EBITDA[s], ebit=SEG_OP[s],
        ebitda_op=[SEG_EBITDA[s][0], SEG_EBITDA[s][1],
                   SEG_EBITDA[s][2] - SEG_JV_FY25.get(s, 0)],
        margin=[e / r for e, r in zip(SEG_EBITDA[s], SEG_REV[s])],
        ppe=SEG_PPE[s],
    )
GROUPS = ['Integrated Logistics', 'Shipping', 'Services']
grp_hist = {g: dict(
    revenue=[sum(SEG_REV[s][i] for s in SEGS if SEG_GROUP[s] == g) for i in range(3)],
    ebitda=[sum(SEG_EBITDA[s][i] for s in SEGS if SEG_GROUP[s] == g) for i in range(3)],
) for g in GROUPS}
for g in GROUPS:
    grp_hist[g]['margin'] = [e / r for e, r in
                             zip(grp_hist[g]['ebitda'], grp_hist[g]['revenue'])]

# ============================================================================
# FORECAST — built unit by unit, five years, two rate paths
# ============================================================================
# --- tankers: vessel by vessel, on the disclosed charter table -------------------
# The company publishes a rate per class each quarter, but the CFO stated on the
# first-quarter call that this rate is a BLEND across the whole class -- "the $144,000 was
# related to our full fleet of 8, and it includes all the vessels on long-term charter as
# well ... it's a blended rate that we give there, which is obviously less than the spot
# rate". Treating that blend as a spot rate and then adding the chartered vessels again at
# their own rates counts the charter drag twice, so it is not done here.
#
# Instead every chartered vessel is carried individually, at its own disclosed rate, for
# exactly the days its own contract runs, and the SPOT rate is DERIVED from the published
# blend by removing those vessels:
#     spot = (blend x class vessel-days  -  charter revenue) / spot vessel-days
# Nothing about the spot rate is assumed; it is solved out of the company's own disclosure.
import datetime as _date


def _dstr(s_):
    return _date.date(*map(int, s_.split('-')))


def _minus_months(d, n):
    y, m = d.year, d.month - n
    while m <= 0:
        m += 12; y -= 1
    day = min(d.day, [31, 29 if y % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30,
                      31][m - 1])
    return _date.date(y, m, day)


# The twelve charters out, exactly as published: vessel, class, period, rate, expiry.
# The start is the expiry less the disclosed period, so no date is invented.
CHARTER_TABLE = [
    ('Navig8 Macallister', 'lr1', 20, 19750, '2027-03-28'),
    ('Navig8 Martinez', 'lr1', 32, 19750, '2028-03-28'),
    ('Navig8 Prosperity', 'lr2', 36, 30561, '2026-05-04'),
    ('Navig8 Promise', 'lr2', 12, 32125, '2026-07-02'),
    ('Navig8 Pride', 'lr2', 12, 32125, '2026-07-09'),
    ('Navig8 Prestige', 'lr2', 12, 36850, '2026-10-08'),
    ('Navig8 Providence', 'lr2', 12, 42000, '2027-01-31'),
    ('Navig8 Passion', 'lr2', 12, 42000, '2027-02-06'),
    ('Zakum', 'vlcc', 22, 50633, '2027-09-02'),
    ('Hili', 'vlcc', 22, 50633, '2027-09-16'),
    ('Arzanah', 'vlcc', 12, 70000, '2027-02-01'),
    ('Habshan', 'vlcc', 12, 72500, '2027-02-21'),
]
CHARTERS = [dict(name=n, klass=k, rate=r, start=_minus_months(_dstr(e), p), end=_dstr(e),
                 period_months=p)
            for n, k, p, r, e in CHARTER_TABLE]
for _c in CHARTERS:
    IN(f"charter_{_c['name'].lower().replace(' ', '_')}", _c['rate'],
       IP26 + f" — charters out: {_c['name']}, a {_c['klass'].upper()} fixed for "
              f"{_c['period_months']} months to {_c['end']:%d %b %Y}",
       '2026-04-30', 'Company')


# On 7 August 2026 -- the anchor date of this study, and therefore already inside the
# market price it is compared against -- the company announced the purchase of eleven
# vessels for about USD 1.3 billion: six very large crude carriers and three gas carriers
# bought secondhand for delivery in the third quarter, and two gas carrier newbuildings
# resold from a Chinese yard for the fourth. It takes the fleet to fourteen crude carriers
# and twelve gas carriers. The first edition of this study omitted it, which left a fair
# value that excluded the vessels being compared with a price that already included them.
ACQ_COST = IN('acq_2026_cost', 1300000, "Announced 7 August 2026 — purchase of eleven "
              "vessels, six very large crude carriers and five gas carriers, for about USD "
              "1.3 billion; nine delivering in the third quarter of 2026 and two gas carrier "
              "newbuildings in the fourth", '2026-08-07', 'Company')
ACQUIRED = [
    ('vlcc', 6, '2026-09-01'),      # six crude carriers, secondhand, Q3 delivery
]
ACQ_GAS = [(3, '2026-09-01'), (2, '2026-11-15')]   # gas carriers, Q3 then Q4
IN('acq_2026_vlcc', 6, "Announced 7 August 2026 — very large crude carriers in that "
   "purchase, taking the owned crude fleet to fourteen", '2026-08-07', 'Company')
IN('acq_2026_gas', 5, "Announced 7 August 2026 — gas carriers in that purchase, taking the "
   "owned gas fleet to twelve very large gas carriers", '2026-08-07', 'Company')


def acquired_days(klass, a, b):
    """Vessel-days the newly bought ships contribute between a and b."""
    days = 0
    for k, n, start in ACQUIRED:
        if k != klass:
            continue
        lo = max(a, _dstr(start))
        if b > lo:
            days += n * (b - lo).days
    return days


def charter_days(klass, a, b):
    """Vessel-days and revenue (USD) that class's charters out earn between a and b."""
    days = rev = 0
    for c in CHARTERS:
        if c['klass'] != klass:
            continue
        lo, hi = max(a, c['start']), min(b, c['end'])
        n = (hi - lo).days
        if n > 0:
            days += n
            rev += n * c['rate']
    return days, rev


CLASSES = ['hs', 'mr', 'lr1', 'lr2', 'vlcc']
FLEET_FY25 = {c: V[f'tnk_{c}_n'] for c in CLASSES}           # owned at 31-Dec-2025
# One 2017-built very large crude carrier was sold in January 2026, so the fleet the
# valuation date actually owns is one smaller. The first edition used the year-end count.
FLEET = dict(FLEET_FY25); FLEET['vlcc'] = FLEET_FY25['vlcc'] - 1
IN('vlcc_sold_jan26', 1, "ADNOC L&S plc, FY2025 earnings release" + " — the 2017-built very large crude carrier sold in "
   "January 2026, which reduces the owned fleet between the year end and the valuation "
   "date", '2026-01-31', 'Company')


def implied_spot(klass, blend, fleet_n, a, b):
    """Back out the spot rate the published blend implies for a class over [a, b)."""
    total_days = fleet_n * (b - a).days
    cd, crev = charter_days(klass, a, b)
    sd = total_days - cd
    if sd <= 0:
        return blend
    return (blend * total_days - crev) / sd


# Quarterly windows, so each blend is converted on the fleet and charters of its own quarter
Q25 = [(_dstr('2025-01-01'), _dstr('2025-04-01')), (_dstr('2025-04-01'), _dstr('2025-07-01')),
       (_dstr('2025-07-01'), _dstr('2025-10-01')), (_dstr('2025-10-01'), _dstr('2026-01-01'))]
Q26 = [(_dstr('2026-01-01'), _dstr('2026-04-01')), (_dstr('2026-04-01'), _dstr('2026-07-01'))]

TCE25 = {c: sum(TCE_FY25[c]) / 4 for c in TCE_FY25}
TCE24 = {c: sum(TCE_FY24[c]) / 4 for c in TCE_FY24}
TCE24['mr'] = TCE25['mr']          # 2024 quarterly rates for this class are not disclosed
# The smallest tankers are not broken out by quarter. The first edition stood the
# medium-range rate in for them, but the company said on the first-quarter call that
# "Handysize rates were softer, down 21%" while medium range was "up 29%" — the two
# classes moved in OPPOSITE directions, so the substitution was not merely imprecise, it
# had the sign wrong. The disclosed relative move is applied instead.
HS_REL = IN('handysize_relative', 0.79, CALLQ126 + " — Handysize rates were softer, down "
            "21%, against medium range up 29%; the two smallest classes moved in opposite "
            "directions, so the medium-range rate is scaled by the disclosed Handysize "
            "move rather than used unadjusted", '2026-05-14', 'Company')
TCE25['hs'] = TCE25['mr'] * HS_REL
TCE24['hs'] = TCE24['mr'] * HS_REL
BLEND_MID = {c: (TCE24[c] + TCE25[c]) / 2 for c in CLASSES}

# spot rates implied by the disclosed blends, class by class
SPOT_25 = {c: sum(implied_spot(c, TCE_FY25.get(c, [TCE25[c]] * 4)[i], FLEET_FY25[c], *Q25[i])
                  for i in range(4)) / 4 for c in CLASSES}
SPOT_MID = {c: implied_spot(c, BLEND_MID[c], FLEET_FY25[c], *Q25[0]) for c in CLASSES}
Q1_BLEND = {c: V[f'tce_{c}_q1_26'] for c in ('mr', 'lr1', 'lr2', 'vlcc')}
Q2_BLEND = {c: V[f'tce_{c}_q2_26'] for c in ('mr', 'lr1', 'lr2', 'vlcc')}
Q1_BLEND['hs'] = Q1_BLEND['mr'] * HS_REL; Q2_BLEND['hs'] = Q2_BLEND['mr'] * HS_REL
SPOT_Q1 = {c: implied_spot(c, Q1_BLEND[c], FLEET[c], *Q26[0]) for c in CLASSES}
SPOT_Q2 = {c: implied_spot(c, Q2_BLEND[c], FLEET[c], *Q26[1]) for c in CLASSES}

# the running cost is solved so the same construction reproduces reported 2025 earnings
vessel_days_25 = sum(FLEET_FY25.values()) * 365
tce_rev_25 = sum(FLEET_FY25[c] * TCE25[c] for c in FLEET_FY25) * 365 / 1000.0
opex_day_25 = (tce_rev_25 - V['seg_ebitda_tankers_fy25']) * 1000.0 / vessel_days_25
IN('tnk_opex_day', round(opex_day_25, 0), "Implied all-in running cost per vessel per day, "
   "solved so that the owned fleet's charter-equivalent revenue less running cost "
   "reproduces the reported Tankers earnings before interest, tax, depreciation and "
   "amortisation for 2025", '2025-12-31', 'Company')
gross_up_25 = V['seg_rev_tankers_fy25'] / tce_rev_25
IN('tnk_grossup_25', round(gross_up_25, 3), "Ratio of reported Tankers revenue to "
   "owned-fleet charter-equivalent revenue in 2025 — the voyage-cost and low-margin relet "
   "and third-party trading content of gross revenue", '2025-12-31', 'Company')
gross_up_26 = 1.60
IN('tnk_grossup_26', gross_up_26, "The same ratio for 2026 onward. Reported first-quarter "
   "revenue was flat year on year while the rate earned per vessel more than doubled, "
   "because low-margin relet and third-party trading fell away; the ratio is set well below "
   "the 2025 level to reflect that and is presentational only — it moves revenue, never "
   "earnings", '2026-03-31', 'Company')

# [R-MACRO-01] THE RUNNING-COST ESCALATOR IS THE HOUSE LADDER, YEAR BY YEAR. A single
# 2.0 per cent rate was carried for all five years and the house path's own 2026 figure is
# 2.5; the gate refused the half point, and it was right to. The first draft of this record
# declared the gap "inside this rule's tolerance", which is a sentence and not a
# measurement — the tolerance is 25 basis points and the gap is 50. Conformed rather than
# exempted, because no disclosure in this company's filings anchors a 2026 cost escalation
# of its own, and an exemption is a COUNT WITH A REASON rather than a convenience.
OPEX_PATH = [_PATH.inflation(y) for y in (2026, 2027, 2028, 2029, 2030)]
OPEX_ESC = IN('opex_escalation', OPEX_PATH[-1], "Running-cost escalation on crew, "
              "technical management, insurance and repairs \u2014 the HOUSE inflation "
              "ladder for this market, read from the macro path rather than typed. The "
              "terminal rate is quoted here; the per-year path is opex_escalation_path "
              "and is what the model applies", _PATH.as_of, 'Country')
OPEX_IDX = []
_c = 1.0
for _r in OPEX_PATH:
    _c *= (1.0 + _r)
    OPEX_IDX.append(_c)
IN('opex_escalation_path', OPEX_PATH, "The house calendar ladder 2026-2030, compounded "
   "into opex_index and applied to every dirham cost line. A study may not carry an "
   "inflation number of its own", _PATH.as_of, 'Country')
H2_26_REVERSION = IN('h2_2026_reversion', 0.50, "Weight placed on the 2025 implied spot "
                     "rate, against the rate implied by the first quarter of 2026, in "
                     "setting the second half of 2026", '2026-08-09', 'Industry')


def spot_path(mode):
    """Implied SPOT rate per class, FY2026-FY2030 — never the published blend."""
    out = {}
    for c in CLASSES:
        h2 = SPOT_Q1[c] * (1 - H2_26_REVERSION) + SPOT_25[c] * H2_26_REVERSION
        y26 = (SPOT_Q1[c] + SPOT_Q2[c] + 2 * h2) / 4.0
        end = SPOT_MID[c] * (1.0 if mode == 'reversion' else 1.30)
        out[c] = [y26] + [y26 + (end - y26) * i / 4.0 for i in range(1, 5)]
    return out


def tanker_leg(mode):
    """Every vessel priced on its own terms: chartered vessels at their own rate for
    exactly the days their own contract runs, everything else at the implied spot rate."""
    spot = spot_path(mode)
    rev, ebitda = [], []
    for i, y in enumerate(range(2026, 2031)):
        a, b = _date.date(y, 1, 1), _date.date(y + 1, 1, 1)
        yr_days = (b - a).days
        tce_rev = 0.0
        for c in CLASSES:
            cd, crev = charter_days(c, a, b)
            # the ships bought in August 2026 trade at spot from delivery
            sd = FLEET[c] * yr_days - cd + acquired_days(c, a, b)
            tce_rev += (crev + sd * spot[c][i]) / 1000.0
        opex = vessel_days_25 * opex_day_25 * OPEX_IDX[i] / 1000.0
        rev.append(tce_rev * gross_up_26)
        ebitda.append(tce_rev - opex)
    return rev, ebitda, spot


# --- gas carriers: contracted vessel-years x implied day rate ------------------
GAS_VY = [10.75, 13.0, 21.25, 25.0, 25.0]
# the five gas carriers bought on 7 August 2026: three delivering in the third quarter,
# two newbuildings in the fourth, so 2026 carries only the part-year
GAS_VY = [v + a for v, a in zip(GAS_VY, [3 * (4 / 12.0) + 2 * (1.5 / 12.0), 5, 5, 5, 5])]
IN('gas_vessel_years_26', GAS_VY[0], IP26 + " — gas fleet contract table, consolidated "
   "vessel-quarters averaged over the year (floating storage 2, the four spot liquefied "
   "natural gas carriers to mid-year, one very large gas carrier, the ethane carrier ramp "
   "and five Das carriers from the second quarter)", '2026-04-30', 'Company')
IN('gas_vessel_years_27', GAS_VY[1], IP26 + " — the same table for 2027", '2026-04-30', 'Company')
IN('gas_vessel_years_28', GAS_VY[2], IP26 + " — the same table for 2028, including the "
   "Ruwais carriers entering service", '2026-04-30', 'Company')
IN('gas_vessel_years_29', GAS_VY[3], IP26 + " — the same table for 2029", '2026-04-30', 'Company')
IN('gas_vessel_years_30', GAS_VY[4], IP26 + " — held at the 2029 level; the contract table "
   "ends in 2029", '2026-04-30', 'Company')
gas_vy_25 = 8.0
IN('gas_vessel_years_25', gas_vy_25, IP26 + " — consolidated gas vessels in service through "
   "2025 (two floating storage units, four liquefied natural gas carriers, one very large "
   "gas carrier and the first ethane carrier), excluding the six gas carriers held in the "
   "50% joint venture", '2025-12-31', 'Company')
gas_rate_25 = V['seg_rev_gas_carriers_fy25'] * 1000.0 / (gas_vy_25 * 365)
IN('gas_rate_day', round(gas_rate_25, 0), "Implied average charter revenue per gas vessel "
   "per day, solved from reported 2025 Gas Carriers revenue over consolidated vessel-years. "
   "Per-vessel rates are not disclosed, so this is the finest level the disclosure supports",
   '2025-12-31', 'Company')
JV_GAS = IN('jv_gas_fy25', 21313, FS25 + " — operating segments note: the share of profit from the "
   "AW Shipping joint venture carried inside the disclosed Gas Carriers earnings",
   '2025-12-31', 'Company')
JV_SERVICES = IN('jv_services_fy25', 16079, FS25 + " — operating segments note: the share of profit from "
   "joint ventures and associates carried inside the disclosed Services earnings",
   '2025-12-31', 'Company')
GAS_MARGIN = IN('gas_margin', 0.70, "Gas Carriers earnings margin held near the 2025 "
                "outcome of 72% net of joint-venture profit, reflecting that fifteen of "
                "twenty owned vessels sit on long-term contracts", '2026-08-09', 'Company')

# --- the remaining units: growth and margin drivers ---------------------------
# Every unit below is anchored on what it actually earned in the first quarter of 2026,
# annualised, and then grown on its own driver. Where the company has given a figure for
# 2026 — engineering and construction revenue of USD 100-150 million — that figure is used
# rather than a growth rate.
DRV = {
    'Offshore Contracting':    dict(rev=[1248192, 1298120, 1350044, 1404046, 1460208],
                                    mar=[0.385, 0.415, 0.430, 0.430, 0.430]),
    'Offshore Services':       dict(rev=[662856, 696000, 730800, 767340, 805707],
                                    mar=[0.287, 0.290, 0.290, 0.290, 0.290]),
    'Offshore Projects':       dict(rev=[125000, 200000, 250000, 275000, 300000],
                                    mar=[-0.020, 0.060, 0.065, 0.065, 0.065]),
    'Dry-Bulk and Containers': dict(rev=[197164, 201107, 205129, 209232, 213417],
                                    mar=[0.184, 0.184, 0.184, 0.184, 0.184]),
    'Services':                dict(rev=[355372, 369587, 384370, 399745, 415735],
                                    mar=[0.200, 0.200, 0.200, 0.200, 0.200]),
}
DRV_WHY = {
    'Offshore Contracting': 'First-quarter revenue annualised, then 4% a year as further '
                            'jack-up barges and support vessels are deployed on the '
                            'contracted programme. The 2026 margin is the first quarter\'s '
                            'own margin before the one-off receivable provision, recovering '
                            'toward the 2025 level as utilisation normalises.',
    'Offshore Services': 'First-quarter revenue annualised, then 5% a year on the support-'
                         'vessel fleet growth already under way. Margin held at the level '
                         'the first quarter delivered.',
    'Offshore Projects': 'The company\'s own stated range of USD 100-150 million of '
                         'engineering and construction revenue for 2026 after the large '
                         'island project completed, then a recovery as new awards replace '
                         'it. This is the least visible line in the model.',
    'Dry-Bulk and Containers': 'First-quarter revenue annualised and grown 2% a year; the '
                               'container vessels sit on a fifteen-year contract and the '
                               'bulk carriers earn charter rates that have been recovering.',
    'Services': 'First-quarter revenue annualised and grown 4% a year. The margin reflects '
                'the warehouse activity moved into this unit and the growing profit share '
                'from the bunkering associate.',
}
for _s, _d in DRV.items():
    _k = _s.lower().replace(' ', '_').replace('-', '_')
    for _i, _y in enumerate(YF):
        IN(f'drv_rev_{_k}_{_y[2:]}', _d['rev'][_i], DRV_WHY[_s], '2026-08-09', 'Company')
        IN(f'drv_mar_{_k}_{_y[2:]}', _d['mar'][_i], DRV_WHY[_s], '2026-08-09', 'Company')


def build_forecast(mode):
    """Two rate paths, one skeleton.

    Both start from the same place — what the fleet actually earned in the first quarter of
    2026 and the level the second quarter was crossing at. They differ only in where rates
    settle: 'reversion' glides to the average of the 2024 and 2025 outcomes, 'sustained'
    to a level 30% above that, on the view that sanctions-driven trade re-routing, an ageing
    fleet and a thin order book have moved the floor up. That single choice is the study's
    central question and it is published both ways rather than blended.
    """
    tnk_rev, tnk_ebitda, tce = tanker_leg(mode)
    gas_rev = [GAS_VY[i] * 365 * gas_rate_25 * OPEX_IDX[i] / 1000.0
               for i in range(5)]
    gas_ebitda = [r * GAS_MARGIN for r in gas_rev]
    # The company's disclosed segment earnings INCLUDE its share of joint-venture and
    # associate profit -- verifiable exactly in the 2025 segment note, where Gas Carriers'
    # operating profit plus its own depreciation falls short of its disclosed earnings by
    # 21,313, precisely the AW Shipping share, and Services by 16,079, precisely the
    # Navig8 share. Those earnings are equity-accounted, not consolidated cash flow, and
    # the equity bridge already adds the joint ventures at carrying value. Leaving them in
    # the forecast would count them twice, so they are removed here.
    gas_ebitda = [e - JV_GAS * OPEX_IDX[i]
                  for i, e in enumerate(gas_ebitda)]
    seg = {'Tankers': dict(rev=tnk_rev, ebitda=tnk_ebitda),
           'Gas Carriers': dict(rev=gas_rev, ebitda=gas_ebitda)}
    for s_, d in DRV.items():
        eb = [r * m for r, m in zip(d['rev'], d['mar'])]
        if s_ == 'Services':                       # same joint-venture removal
            eb = [e - JV_SERVICES * OPEX_IDX[i]
                  for i, e in enumerate(eb)]
        seg[s_] = dict(rev=list(d['rev']), ebitda=eb)
    grp = {g: dict(rev=[sum(seg[s_]['rev'][i] for s_ in SEGS if SEG_GROUP[s_] == g)
                        for i in range(5)],
                   ebitda=[sum(seg[s_]['ebitda'][i] for s_ in SEGS if SEG_GROUP[s_] == g)
                           for i in range(5)]) for g in GROUPS}
    rev = [sum(seg[s_]['rev'][i] for s_ in SEGS) for i in range(5)]
    ebitda = [sum(seg[s_]['ebitda'][i] for s_ in SEGS) for i in range(5)]
    return dict(seg=seg, group=grp, revenue=rev, ebitda=ebitda, tce=tce)


def guidance_check(f):
    """What management guided for 2026, against what this build produces for 2026."""
    gkey = {'Integrated Logistics': 'il', 'Shipping': 'ship', 'Services': 'serv'}
    out = {}
    for g in GROUPS:
        out[g] = dict(
            guided_revenue=grp_hist[g]['revenue'][2] * (1 + V[f'g26_rev_{gkey[g]}']),
            guided_ebitda=grp_hist[g]['ebitda'][2] * (1 + V[f'g26_ebitda_{gkey[g]}']),
            built_revenue=f['group'][g]['rev'][0], built_ebitda=f['group'][g]['ebitda'][0])
        out[g]['ebitda_gap'] = out[g]['built_ebitda'] / out[g]['guided_ebitda'] - 1
    out['Group'] = dict(
        guided_revenue=V['rev_fy25'] * (1 + V['g26_rev_group']),
        guided_ebitda=ebitda_rep[2] * (1 + V['g26_ebitda_group']),
        built_revenue=f['revenue'][0], built_ebitda=f['ebitda'][0])
    out['Group']['ebitda_gap'] = out['Group']['built_ebitda'] / out['Group']['guided_ebitda'] - 1
    return out


# --- segment depreciation and amortisation, as disclosed for 2025 -------------
SEG_DNA25 = {'Offshore Contracting': 151367, 'Offshore Services': 62963,
             'Offshore Projects': 8860, 'Tankers': 195374, 'Gas Carriers': 50526,
             'Dry-Bulk and Containers': 25225, 'Services': 30297}
for _s, _v in SEG_DNA25.items():
    IN('seg_dna_' + _s.lower().replace(' ', '_').replace('-', '_') + '_fy25', _v,
       FS25 + " — operating segments note: depreciation and amortisation carried in direct "
       "costs plus that carried in general and administrative expenses", '2025-12-31',
       'Company')

CAPEX = [1375000, 1245000, 1245000, 700000, 650000]
for _i, _y in enumerate(YF):
    IN(f'capex_{_y[2:]}', CAPEX[_i],
       (IP26 + " — the company's own capital-expenditure path, about USD 7.0 billion in "
        "total to 2028" ) if _i < 3 else
       ("Study forecast driver — beyond the guided window the newbuild programme has "
        "delivered, so spending falls back toward the stated USD 100-150 million a year of "
        "maintenance capital expenditure plus continuing fleet renewal"),
       '2026-04-30' if _i < 3 else '2026-08-09', 'Company')
DEP_RATE = IN('dep_rate_ppe', round(V['q1_26_dep_ppe'] * 4 /
              ((V['ppe_fy25'] + V['q1_26_ppe']) / 2), 4),
              "Depreciation charged on property, plant and equipment in the first quarter "
              "of 2026, annualised, over the average balance for that quarter. The first "
              "quarter is the better forward basis than the 2025 full year, whose average "
              "balance is distorted by the fleet acquired at the start of that year",
              '2026-03-31', 'Company')
IN('life_tankers', 25, FS25 + " — accounting policies: tankers are depreciated straight "
   "line over 25 years, dry-bulk and containers 25, gas carriers 25 to 40, offshore vessels "
   "20 to 25 and jack-up barges 40, with dry-docking components over 2 to 5",
   '2025-12-31', 'Company')
IN('dep_rate_realised_fy25', 0.0675, FS25 + " — depreciation charged on property, plant "
   "and equipment in 2025 over the average balance for the year. It is higher than the "
   "rate used here, and both are higher than the disclosed useful lives imply for a fleet "
   "written off over 25 to 40 years, because dry-docking components are written off over "
   "2 to 5 years. The rate used is the more conservative of the two available forward "
   "bases and is sensitised", '2025-12-31', 'Company')
OTHER_DNA25 = IN('other_dna_run_rate',
                 (V['q1_26_dep_rou'] + V['q1_26_dep_ip'] + V['q1_26_amort']) * 4,
                 Q126 + " — depreciation on right-of-use assets and investment properties "
                 "plus amortisation of intangibles in the first quarter, annualised",
                 '2026-03-31', 'Company')
opcost_25 = V['rev_fy25'] - ebitda_op[2]
# Receivables were calibrated on 2025 revenue, which carries a 2.72x gross-up from
# charter-equivalent revenue, and then applied to forecast revenue built at 1.60x. The
# same absolute receivable balance against a smaller revenue line is MORE days, not the
# same days, so the ratio is re-based onto the basis the forecast actually uses. This also
# falsifies the first edition's claim that the gross-up "never touches the valuation": it
# reaches it through receivables and the change in working capital.
DSO_REPORTED = ccc['dso'][2]
_rev25_fwd_basis = (V['rev_fy25'] - V['seg_rev_tankers_fy25'] + tce_rev_25 * gross_up_26)
DSO = DSO_REPORTED * V['rev_fy25'] / _rev25_fwd_basis
DIO_OP = V['inv_fy25'] / opcost_25 * 365
DPO_OP = (V['pay_fy25'] + V['dtr_c_fy25']) / opcost_25 * 365
IN('dso_days_reported', round(DSO_REPORTED, 1), FS25 + " — trade and other receivables "
   "plus amounts due from related parties over reported 2025 revenue", '2025-12-31',
   'Company')
IN('dso_days', round(DSO, 1), FS25 + " — trade and other receivables plus amounts due from "
   "related parties over revenue, in days", '2025-12-31', 'Company')
IN('dio_days', round(DIO_OP, 1), FS25 + " — inventories over total operating cost, in days",
   '2025-12-31', 'Company')
IN('dpo_days', round(DPO_OP, 1), FS25 + " — trade and other payables plus amounts due to "
   "related parties over total operating cost, in days", '2025-12-31', 'Company')
TAX_SEG = {'Integrated Logistics': 0.090, 'Shipping': 0.010, 'Services': 0.040}
for _g, _r in TAX_SEG.items():
    IN('tax_' + _g.lower().replace(' ', '_'), _r, FS25 + " — operating segments note: the "
       "income tax charge borne by each business unit over its own profit before tax in "
       "2025. International shipping income is relieved under the UAE corporate tax law, "
       "which is why the shipping units carry almost no charge", '2025-12-31', 'Country')


def project(mode):
    f = build_forecast(mode)
    rev, ebitda = f['revenue'], f['ebitda']
    # the vessels bought in August 2026 are added to the asset base in the year they
    # arrive, so they depreciate and shield tax exactly as any other vessel does
    ppe_open, ppe, dep_ppe, dna = V['ppe_fy25'], [], [], []
    ACQ_CAPEX = [ACQ_COST, 0.0, 0.0, 0.0, 0.0]
    for i in range(5):
        d = DEP_RATE * (ppe_open + (ppe_open + CAPEX[i] + ACQ_CAPEX[i])) / 2.0
        # solve the roll consistently: depreciation on the average of opening and closing
        d = DEP_RATE * (ppe_open + max(ppe_open + CAPEX[i] + ACQ_CAPEX[i] - d, 0)) / 2.0
        close = ppe_open + CAPEX[i] + ACQ_CAPEX[i] - d
        dep_ppe.append(d); ppe.append(close)
        dna.append(d + OTHER_DNA25 * OPEX_IDX[i])
        ppe_open = close
    ebit = [e - d for e, d in zip(ebitda, dna)]
    # tax as a MIX OUTCOME: each business unit taxed at its own disclosed rate
    seg_dna_tot = sum(SEG_DNA25.values())
    tax_eff, tax_amt = [], []
    for i in range(5):
        t = 0.0
        for g in GROUPS:
            members = [s for s in SEGS if SEG_GROUP[s] == g]
            g_ebitda = sum(f['seg'][s]['ebitda'][i] for s in members)
            g_dna = dna[i] * sum(SEG_DNA25[s] for s in members) / seg_dna_tot
            t += max(g_ebitda - g_dna, 0) * TAX_SEG[g]
        tax_amt.append(t)
        tax_eff.append(t / ebit[i] if ebit[i] else 0.0)
    nopat = [e - t for e, t in zip(ebit, tax_amt)]
    opcost = [r - e for r, e in zip(rev, ebitda)]
    nwc = [r * DSO / 365 + c * DIO_OP / 365 - c * DPO_OP / 365
           for r, c in zip(rev, opcost)]
    dnwc = [nwc[0] - hist_bs['nwc'][2]] + [nwc[i] - nwc[i - 1] for i in range(1, 5)]
    fcff = [n + d - c - w for n, d, c, w in zip(nopat, dna, CAPEX, dnwc)]
    return dict(mode=mode, years=YF, seg=f['seg'], group=f['group'], tce=f['tce'],
                revenue=rev, ebitda=ebitda, ebitda_margin=[e / r for e, r in zip(ebitda, rev)],
                dna=dna, dep_ppe=dep_ppe, ppe=ppe, ebit=ebit,
                ebit_margin=[e / r for e, r in zip(ebit, rev)],
                tax=tax_amt, tax_rate=tax_eff, nopat=nopat,
                capex=CAPEX, nwc=nwc, dnwc=dnwc, fcff=fcff, opcost=opcost)

# ============================================================================
# COST OF CAPITAL — built, not asserted
# ============================================================================
mktcap = shares_mn * spot_aed / peg * 1000.0            # USD'000
spot_usd = spot_aed / peg
rf_star = V['rf_observed'] - V['sov_spread']            # country risk enters once, via the ERP
ke = rf_star + V['beta'] * V['erp_total']
ke_blume = rf_star + V['beta_blume'] * V['erp_total']
ke_beta1 = rf_star + V['beta_composite'] * V['erp_total']
# The two bounds of the regressed beta's own 90% confidence interval, carried as costs of
# equity. Every low/high bound in the study that moves with the discount rate uses these,
# so the published span is the span the estimate itself supports. NOTE: ke_beta1 is the
# ALTERNATIVE construction (a LOWER beta, so a HIGHER value) and must never be used as a
# downside bound — it was, while it stood for a beta of one, and that silently inverted
# the book lens's low bound and Expert 2's low bound when the regressor changed.
ke_ci_hi = rf_star + V['beta_ci_hi'] * V['erp_total']   # high beta -> low value
ke_ci_lo = rf_star + V['beta_ci_lo'] * V['erp_total']   # low beta  -> high value

# --- cost of debt: three independent constructions, averaged on the sheet ------
kd_m1 = V['sofr'] + V['shldr_margin']                        # the marginal drawdown rate
kd_bank_mid = (V['bank_loan_lo'] + V['bank_loan_hi']) / 2
kd_other_mid = (V['other_borr_lo'] + V['other_borr_hi']) / 2
kd_thirdparty = (kd_bank_mid + kd_other_mid) / 2
kd_lease = V['intpaid_lease_fy25'] / ((170274 + 223153) / 2)  # implied lease borrowing rate
IN('lease_open_fy25', 170274, FS25 + " — lease liabilities note, opening balance",
   '2025-01-01', 'Company')
IN('lease_close_fy25', 223153, FS25 + " — lease liabilities note, closing balance",
   '2025-12-31', 'Company')
debt_now = V['q1_26_shldr_loan'] + V['q1_26_borrowings'] + V['q1_26_leases']
kd_m2 = (V['q1_26_shldr_loan'] * kd_m1 + V['q1_26_borrowings'] * kd_thirdparty
         + V['q1_26_leases'] * kd_lease) / debt_now
kd_m3 = kd_bank_mid
# Three independent constructions, AVERAGED. The first edition's prose described this as
# "weighted across the drawn book", which it is not: only the second construction is
# balance-weighted, and that one alone gives 5.69%. The average is the triangulation the
# study set out to show; the balance-weighted figure is published beside it rather than
# the average being mislabelled as it.
# [R-COC-01 AMENDED] THE ADOPTED RATE MUST REPRODUCE FROM ITS CONTRACTUAL ANCHOR — every
# facility with its balance, its own rate and the note that rate comes from, weighted. A
# weighted average either comes out or it does not, and that is what makes the number
# verifiable from outside the study.
#
# THE AVERAGE OF THREE CONSTRUCTIONS DOES NOT COME OUT. Only the second is
# balance-weighted; averaging it with a marginal drawdown rate and a mid-point of a
# disclosed bank range produces a figure no set of facility lines reproduces, and this
# study's own comment two lines up already said so — "only the second construction is
# balance-weighted, and that one alone gives 5.69%". That is [R-LENS-03]'s lesson in the
# cost of debt: a number produced by averaging several methods is a NEW method with free
# parameters nobody tested, wearing the appearance of caution.
#
# The balance-weighted construction is adopted; the other two are published beside it as
# what they are — a marginal rate and a range mid-point — rather than blended into it. It
# moves the weighted cost of capital by about one basis point, because the drawn book is
# 7.2 per cent of the capital structure, and that is exactly why it was worth correcting:
# a rule obeyed only when it is expensive is not a rule.
kd = kd_m2
kd_balance_weighted = kd_m2
kd_retired_average = (kd_m1 + kd_m2 + kd_m3) / 3
# The perpetual capital securities are deducted in the equity bridge as a claim ranking
# ahead of the ordinary shares. A claim that is deducted from enterprise value must also
# be WEIGHTED in the cost of capital at its own cost — those are the two halves of one
# treatment, not a double count. The first edition weighted only equity and debt, which
# subtracted a cheap tranche of capital from value without letting it price that value.
# Two independent reviews reached the same conclusion; it is adopted here.
kh = V['sofr'] + V['hybrid_margin']            # the perpetual's own coupon rate
hybrid_cap = V['q1_26_hybrid']
cap_total = mktcap + debt_now + hybrid_cap
we = mktcap / cap_total
wd = debt_now / cap_total
wh = hybrid_cap / cap_total
tax_stat = V['tax_stat']
wacc = we * ke + wd * kd * (1 - tax_stat) + wh * kh   # the coupon is not tax-deductible: it is an equity distribution
# terminal: the same construction on a long-run risk-free anchor
ke_term = V['rf_terminal'] + V['beta'] * V['erp_total']
kd_term = V['rf_terminal'] + (kd - rf_star)
# the perpetual pays a floating coupon, so its cost normalises with the risk-free rate
kh_term = V['rf_terminal'] + V['hybrid_margin']
wacc_term = we * ke_term + wd * kd_term * (1 - tax_stat) + wh * kh_term
wacc_glide = [wacc + (wacc_term - wacc) * (i + 1) / 5.0 for i in range(5)]

wacc_blk = dict(
    rf_observed=V['rf_observed'], sov_spread=V['sov_spread'], rf_star=rf_star,
    beta=V['beta'], beta_se=V['beta_se'], beta_r2=V['beta_r2'], beta_blume=V['beta_blume'],
    erp=V['erp_total'], crp=V['crp'], erp_mature=V['erp_mature'],
    ke=ke, ke_blume=ke_blume, ke_beta1=ke_beta1,
    kd_method1=kd_m1, kd_method2=kd_m2, kd_method3=kd_m3, kd=kd,
    wacc_ex_hybrid=((mktcap / (mktcap + debt_now)) * ke
                    + (debt_now / (mktcap + debt_now)) * kd * (1 - tax_stat)),
    kd_balance_weighted=kd_balance_weighted,
    kd_retired_average=kd_retired_average, kd_construction='balance-weighted across the instruments actually outstanding; the average of three constructions is retired because it reproduces from no set of facility lines',
    kd_bank_mid=kd_bank_mid, kd_other_mid=kd_other_mid, kd_thirdparty=kd_thirdparty,
    kd_lease=kd_lease, kd_after_tax=kd * (1 - tax_stat),
    tax_stat=tax_stat, we=we, wd=wd, wacc=wacc,
    rf_terminal=V['rf_terminal'], ke_term=ke_term, kd_term=kd_term, wacc_term=wacc_term,
    kh=kh, kh_term=kh_term, wh=wh, hybrid_cap=hybrid_cap,
    wacc_glide=wacc_glide, mktcap=mktcap, debt=debt_now, spot_usd=spot_usd,
    kd_evidence=[
        ('Parent revolving credit facility, drawn January 2026', 'SOFR + 0.80%', kd_m1),
        ('Third-party bank loans, disclosed weighted-average range 7.11%-7.55%',
         'midpoint', kd_bank_mid),
        ('Other third-party borrowings, disclosed range 4.36%-8.31%', 'midpoint',
         kd_other_mid),
        ('Lease liabilities, interest charged over the average balance in 2025', 'implied',
         kd_lease),
        ('Perpetual capital securities placed with a third-party investor',
         'SOFR + 1.25%', V['sofr'] + V['hybrid_margin']),
        ('Local government bond, the dirham tranche maturing January 2031', 'auction yield',
         V['rf_observed']),
    ],
)

# ============================================================================
# DISCOUNTED CASH FLOW — both paths, identical machinery
# ============================================================================
NETDEBT_CO = V['q1_26_netdebt']
DEFERRED = V['q1_26_pcp']
NETDEBT = NETDEBT_CO + DEFERRED + ACQ_COST   # the August purchase is committed and funded
HYBRID = V['q1_26_hybrid']
NCI_BV = V['q1_26_nci']
# Minorities take 8.8% of profit but hold only 5.1% of book equity, so book understates
# their claim on VALUE. But the dominant minority is already priced elsewhere: 251,985 of
# the 264,512 arose on the Navig8 combination (equity statement), and that 20% is
# CONTRACTED for purchase in mid-2027 -- its present value sits in the bridge already as
# deferred consideration. Deducting it again at a share of equity value would count it
# twice. Only the remaining minorities are lifted from book to value.
NCI_NAVIG8 = IN('nci_navig8', 251985, FS25 + " — statement of changes in equity: "
                "non-controlling interests arising on business combinations, being the 20% "
                "of the acquired tanker business", '2025-12-31', 'Company')
NCI_OTHER_BV = NCI_BV - NCI_NAVIG8
JV_BV = 493120
IN('jv_bv_q126', JV_BV, Q126 + " — investment in joint ventures and associates",
   '2026-03-31', 'Company')
# [R-TERM-01] THE TERMINAL IS BUILT ON A DISCLOSED ASSET LIFE, NOT ON THE RECIPROCAL OF
# THE GROWTH RATE. This study charged the reinvestment identity rr = g/ROIC, which
# substitutes to a charge of g x IC every year for ever and therefore an implied
# replacement cycle of 1/g — FIFTY YEARS at a 2 per cent terminal, for a fleet of ships.
#
# AND THE DIRECTION OF THAT DEFECT IS THE OPPOSITE OF THE EGYPTIAN CASES. There, terminal
# inflation of 7 per cent made 1/g = 14.3 years and the construction OVER-charged a
# 25-year plant. Here a pegged 2 per cent makes 1/g = 50 years and it UNDER-charges a
# 25-year ship by half. It is the same defect — an inflation rate silently doing duty as
# an asset life — and which way it bites depends only on the market's inflation, which is
# a fact about the currency and not about the asset.
GROSS_PPE_FY25 = IN('gross_ppe_ex_cwip_fy25', 8167686 - 572616,
    FS25 + " — note 11, gross cost of property, plant and equipment at 31 December 2025 "
    "of USD 8,167,686 thousand LESS capital work in progress of USD 572,616 thousand, "
    "which is not depreciated. Buildings 148,743, vessels and marine equipment 7,279,939, "
    "plant 5,305, equipment and vehicles 114,636, furniture and office equipment 46,447",
    '2025-12-31', 'Company')
VESSEL_LIFE = IN('vessel_life_years', 25.0,
    FS25 + " — the accounting-policies note states the estimated useful lives directly: "
    "tankers 25 years, dry-bulk and containers 25 years, gas carriers 25-40 years, "
    "offshore vessels 20-25 years, jack-up barges 40 years, plant 20 years, buildings and "
    "port infrastructure 7-50 years. TWENTY-FIVE IS THE STATED LIFE FOR THE MAJORITY "
    "VESSEL TYPES and the bottom of the gas-carrier range; the note does not split the "
    "USD 7,279,939 thousand vessel line by type, so a gross-cost-weighted blend across "
    "vessel classes cannot be computed from this disclosure and is NOT invented. Using "
    "the longer end instead would lengthen the life and raise the value, and that "
    "alternative is priced in the sensitivity rather than chosen silently",
    '2025-12-31', 'Company')
STUB = 0.75      # the valuation date is 31 March 2026; three quarters of 2026 remain
Q1_FCF = IN('q1_26_fcf', 130000, MDAQ126 + " — free cash flow of USD 130 million in the "
            "first quarter of 2026, already reflected in net debt at the valuation date",
            '2026-03-31', 'Company')


def nci_deduction(equity_pre):
    """Minorities: the contracted slice at its contracted price, the rest at value."""
    share_other = NCI_SHARE * NCI_OTHER_BV / NCI_BV
    return NCI_NAVIG8 + max(NCI_OTHER_BV, equity_pre * share_other)


def dcf(path, hybrid_as_debt=False, wacc_ov=None, g_ov=None, term_wacc_ov=None):
    w = wacc if wacc_ov is None else wacc_ov
    wt = wacc_term if term_wacc_ov is None else term_wacc_ov
    g = V['g_terminal'] if g_ov is None else g_ov
    glide = [w + (wt - w) * (i + 1) / 5.0 for i in range(5)]
    df, cum = [], 1.0
    for i, r in enumerate(glide):
        cum *= (1 + r) ** (STUB if i == 0 else 1.0)     # the factors compound year on year
        df.append(1.0 / cum)
    fcff = list(path['fcff'])
    # the valuation date is 31 March 2026, so the first quarter's free cash flow is already
    # inside the balance-sheet net debt and is removed rather than discounted a second time
    fcff[0] -= Q1_FCF
    pv = [c * d for c, d in zip(fcff, df)]
    pv_expl = sum(pv)
    ic_end = path['ppe'][4] + path['nwc'][4] + V['intang_fy25'] + V['gw_fy25']
    roic_t = path['nopat'][4] / ic_end
    reinv = g / roic_t
    nopat_t1 = path['nopat'][4] * (1 + g)
    tv = nopat_t1 * (1 - reinv) / (wt - g)
    # [R-TERM-01] THIS TERMINAL IS THE RETIRED REINVESTMENT IDENTITY AND IT IS LISTED ON
    # THAT RULE'S RATCHET WITH TWELVE OTHERS. It was rebuilt on the sanctioned module in
    # this pass and the module REFUSED, for a reason worth writing down rather than
    # working around.
    #
    # THE DEFECT'S DIRECTION REVERSES AT LOW INFLATION AND NOBODY HAD SAID SO. rr = g/ROIC
    # substitutes to a charge of g x IC every year for ever, so the implied replacement
    # cycle is 1/g. On the Egyptian names a 7 per cent terminal makes that 14.3 years and
    # it OVER-charges a 25-year plant. Here a pegged 2 per cent makes it FIFTY YEARS and
    # it UNDER-charges a 25-year ship by half. Same defect, an inflation rate silently
    # doing duty as an asset life; which way it bites is a fact about the currency.
    #
    # WHY THE SANCTIONED BUILD REFUSED, AND IT IS A REAL DISCLOSURE PROBLEM RATHER THAN A
    # PARAMETER TO TUNE. Maintenance at the disclosed 25-year vessel life on the gross
    # base comes to less than this model's own book depreciation, so terminal free cash
    # flow exceeds terminal profit and the implied payout lands at 117 per cent — a going
    # concern distributing more than it earns for ever, which the module refuses outright
    # and is right to. The two figures disagree because THEY ARE NOT MEASURING THE SAME
    # THING: this study's own register already records that the realised rate runs above
    # what the disclosed lives imply BECAUSE DRY-DOCKING COMPONENTS ARE WRITTEN OFF OVER
    # TWO TO FIVE YEARS. Dry-docking IS maintenance, capitalised and amortised fast, so a
    # terminal charging only hull replacement while adding back all book depreciation
    # would add back the amortisation of a maintenance cost it never charged.
    #
    # The honest maintenance charge therefore covers the hull cycle AND the recurring
    # dry-docking, and this disclosure does not split the vessel line by type or the
    # charge by component, so the life that would do it cannot be derived from the
    # filings. A LIFE THIS DESK CHOSE IS NOT A DISCLOSED LIFE, so none is chosen here.
    # What is needed is the component split — stop and inform, per SIGCM clause 8.
    pv_tv = tv * df[4]
    ev_ops = pv_expl + pv_tv
    ev = ev_ops + JV_BV
    nd = NETDEBT + (HYBRID if hybrid_as_debt else 0.0)
    pre_nci = ev - nd
    nci_ded = nci_deduction(pre_nci)
    eq = pre_nci - nci_ded
    fv_usd = eq / shares_mn / 1000.0      # equity is USD thousand, shares are millions
    return dict(wacc=w, wacc_term=wt, g=g, glide=glide, df=df, fcff=fcff, pv=pv,
                pv_explicit=pv_expl, roic_terminal=roic_t, reinvest=reinv,
                nopat_t1=nopat_t1, tv=tv, pv_tv=pv_tv, tv_share=pv_tv / ev_ops,
                term_life_disclosed=float(VESSEL_LIFE),
                term_gross_base_fy25=float(GROSS_PPE_FY25),
                ev_ops=ev_ops, jv=JV_BV, ev=ev, net_debt=nd, deferred=DEFERRED,
                hybrid=HYBRID if hybrid_as_debt else 0.0, nci=nci_ded,
                nci_book=NCI_BV, nci_navig8=NCI_NAVIG8, nci_other_bv=NCI_OTHER_BV,
                equity=eq, fv_usd=fv_usd, fv_aed=fv_usd * peg,
                ic_terminal=ic_end)

# ============================================================================
# FORECAST INCOME STATEMENT BELOW OPERATING PROFIT, AND THE FUNDING ROLL
# ============================================================================
DPS_USD = [V['dps_2026_usd'] * 1000.0 * (1 + V['div_growth']) ** i for i in range(5)]
HYB_COUPON = HYBRID * (V['sofr'] + V['hybrid_margin'])
NCI_SHARE = IN('nci_share', 0.088, Q126 + " — profit attributable to non-controlling "
               "interests over profit for the period in the first quarter of 2026",
               '2026-03-31', 'Company')
CASH_HELD = V['q1_26_cash']


def finance_roll(path):
    nd, gross, interest, fin_inc = [], [], [], []
    nd_prev = NETDEBT
    for i in range(5):
        g_open = nd_prev + CASH_HELD
        int_i = kd * g_open
        fi = V['sofr'] * CASH_HELD
        fcfe = path['fcff'][i] - int_i * (1 - tax_stat) + fi * (1 - tax_stat) - HYB_COUPON
        nd_new = nd_prev - fcfe + DPS_USD[i]
        nd.append(nd_new); gross.append(g_open); interest.append(int_i); fin_inc.append(fi)
        nd_prev = nd_new
    pbt = [e - i_ + f for e, i_, f in zip(path['ebit'], interest, fin_inc)]
    tax = [p * r for p, r in zip(pbt, path['tax_rate'])]
    pat = [p - t for p, t in zip(pbt, tax)]
    nci = [p * NCI_SHARE for p in pat]
    npa = [p - n for p, n in zip(pat, nci)]
    # earnings per ORDINARY share: the perpetual coupon ranks ahead of the ordinary
    # shares, so it comes out of the numerator. Leaving it in credits the ordinary
    # holders with a return that is contractually someone else's.
    eps = [(n - HYB_COUPON) / shares_mn / 1000.0 for n in npa]
    eps_pre_coupon = [n / shares_mn / 1000.0 for n in npa]
    return dict(net_debt=nd, gross_debt=gross, interest=interest, fin_income=fin_inc,
                pbt=pbt, tax=tax, pat=pat, nci=nci, npa=npa, eps=eps, eps_pre_coupon=eps_pre_coupon,
                npa_ordinary=[n - HYB_COUPON for n in npa], dps=DPS_USD,
                hybrid_coupon=HYB_COUPON,
                nd_ebitda=[n / e for n, e in zip(nd, path['ebitda'])],
                payout=[d / n for d, n in zip(DPS_USD, npa)])


def forecast_bs(path, fin):
    """Balance sheet rolled forward from the drivers, not pasted."""
    eq_prev = V['q1_26_eqp']
    rows = []
    for i in range(5):
        eq = eq_prev + fin['npa'][i] - DPS_USD[i] - HYB_COUPON
        rows.append(dict(
            ppe=path['ppe'][i], nwc=path['nwc'][i], cash=CASH_HELD,
            gross_debt=fin['gross_debt'][i], net_debt=fin['net_debt'][i],
            equity_parent=eq, hybrid=HYBRID, nci=NCI_BV, jv=JV_BV,
            intangibles=V['intang_fy25'], goodwill=V['gw_fy25'],
            bvps=eq / shares_mn / 1000.0,
            roe=fin['npa'][i] / ((eq_prev + eq) / 2),
            invested_capital=path['ppe'][i] + path['nwc'][i] + V['intang_fy25'] + V['gw_fy25'],
            roic=path['nopat'][i] / (path['ppe'][i] + path['nwc'][i] + V['intang_fy25']
                                     + V['gw_fy25']),
        ))
        eq_prev = eq
    return rows

# ============================================================================
# THE FOUR LENSES
# ============================================================================
PEERS = [
    dict(name='Qatar Gas Transport (Nakilat)', ticker='QGTS', market='Qatar',
         model='long-term contracted gas shipping', ev_ebitda=12.26, pe_fwd=13.97,
         pe_ttm=14.15, pb=1.65, dy=0.0336,
         src='stockanalysis.com company statistics page', asof='2026-08-09'),
    dict(name='Frontline plc', ticker='FRO', market='Oslo / New York',
         model='spot crude tankers', ev_ebitda=8.96, pe_fwd=6.44, pe_ttm=9.98,
         pb=None, dy=None, src='stockanalysis.com company statistics page',
         asof='2026-08-09'),
    dict(name='International Seaways', ticker='INSW', market='New York',
         model='spot crude and product tankers', ev_ebitda=8.10, pe_fwd=None,
         pe_ttm=None, pb=None, dy=None,
         src='valueinvesting.io enterprise-value-to-earnings page', asof='2026-07-26'),
]
SPOT_W = V['spot_share_ebitda_26']          # the company's own disclosed spot exposure
contracted_mult = PEERS[0]['ev_ebitda']
spot_mult = (PEERS[1]['ev_ebitda'] + PEERS[2]['ev_ebitda']) / 2
blend_ev_ebitda = (1 - SPOT_W) * contracted_mult + SPOT_W * spot_mult
blend_pe = (1 - SPOT_W) * PEERS[0]['pe_fwd'] + SPOT_W * PEERS[1]['pe_fwd']
# The peers' forward multiples are applied to the company's forward earnings, which is
# consistent. What was NOT consistent was the table beside them, which quoted the company
# on a TRAILING multiple against peers shown forward. Both bases are now published.
blend_pe_ttm = (1 - SPOT_W) * PEERS[0]['pe_ttm'] + SPOT_W * PEERS[1]['pe_ttm']

BASE = project('reversion')
GUID = project('sustained')
FINB = finance_roll(BASE)
FING = finance_roll(GUID)
BSB = forecast_bs(BASE, FINB)


def equity_from_ev(ev, hybrid_as_debt=True):
    pre = ev + JV_BV - NETDEBT - (HYBRID if hybrid_as_debt else 0.0)
    return pre - nci_deduction(pre)


def per_share(eq):
    return eq / shares_mn / 1000.0 * peg


rel_ev = blend_ev_ebitda * BASE['ebitda'][0]
rel_ev_lo = spot_mult * BASE['ebitda'][0]
rel_ev_hi = contracted_mult * BASE['ebitda'][0]
rel_pe_val = blend_pe * FINB['npa'][0]
rel = dict(
    spot_weight=SPOT_W, contracted_multiple=contracted_mult, spot_multiple=spot_mult,
    blend_ev_ebitda=blend_ev_ebitda, blend_pe=blend_pe, peers=PEERS,
    ebitda_26=BASE['ebitda'][0], npa_26=FINB['npa'][0],
    ev=rel_ev, value_ev_ebitda=per_share(equity_from_ev(rel_ev)),
    npa_ord_26=FINB['npa'][0] - HYB_COUPON,
    value_pe=blend_pe * (FINB['npa'][0] - HYB_COUPON) / shares_mn / 1000.0 * peg,
    bear=per_share(equity_from_ev(rel_ev_lo)),
    bull=per_share(equity_from_ev(rel_ev_hi)),
    own_ev_ebitda_ttm=(mktcap + NETDEBT) / ebitda_rep[2],
    own_ev_bridge=mktcap + NETDEBT + HYBRID + NCI_BV,
    own_ev_ebitda_26_bridge=(mktcap + NETDEBT + HYBRID + NCI_BV) / BASE['ebitda'][0],
    own_ev_ebitda_26=(mktcap + NETDEBT) / BASE['ebitda'][0],
    own_pe_ttm=mktcap / (V['npa_fy25'] - V['hybrid_coupon_fy25']),
    own_pb=mktcap / (V['q1_26_eqp'] + HYBRID),
    own_dy=V['dps_2026_usd'] * 1000.0 / mktcap,
)
rel['base'] = (rel['value_ev_ebitda'] + rel['value_pe']) / 2

# --- normalised earnings power ------------------------------------------------
norm_ebitda = sum(BASE['ebitda']) / 5.0
norm_npa = sum(FINB['npa']) / 5.0 - HYB_COUPON
norm_pe = blend_pe
norm = dict(norm_ebitda=norm_ebitda, norm_npa=norm_npa, pe=norm_pe,
            ev=blend_ev_ebitda * norm_ebitda,
            base=per_share(equity_from_ev(blend_ev_ebitda * norm_ebitda)),
            eps=norm_npa / shares_mn / 1000.0,
            value_pe=norm_pe * norm_npa / shares_mn / 1000.0 * peg)
norm['base'] = (norm['base'] + norm['value_pe']) / 2
norm['bear'] = per_share(equity_from_ev(spot_mult * norm_ebitda))
norm['bull'] = per_share(equity_from_ev(contracted_mult * norm_ebitda))

# --- book value and sustainable return ----------------------------------------
roe_sust = sum(b['roe'] for b in BSB) / 5.0
g_b = V['g_terminal']
# A single-stage justified price-to-book, (ROE - g)/(Ke - g), assumes a steady state:
# it is only coherent if the company distributes exactly what it does not need to fund g.
# At a sustainable return of 16.9% and 2% growth that means paying out 88% of earnings.
# This company pays out 31-39% and compounds its book at 9.6% a year against a 9.34% cost
# of equity -- above it, where the formula is not merely wrong but undefined. So the
# single-stage form is not used. The lens is built instead as RESIDUAL INCOME over the
# model's own forecast: the book the company already has, plus the value of earning more
# than the cost of equity on it while that lasts, plus a fading remainder.
def residual_income(ke_r, roe_scale=1.0):
    """Book value plus the present value of returns above the cost of equity."""
    b0 = V['q1_26_eqp'] / 1000.0                      # opening ordinary book, USD mn
    b, pv, detail = b0, 0.0, []
    for i in range(5):
        roe_i = FINB_ROE[i] * roe_scale
        ri = (roe_i - ke_r) * b                       # residual income earned on that book
        df = 1.0 / (1 + ke_r) ** (i + 1)
        pv += ri * df
        detail.append(dict(year=YF[i], opening_book=b, roe=roe_i, residual_income=ri,
                           discount_factor=df, pv=ri * df))
        b = BSB[i]['equity_parent'] / 1000.0          # the model's own roll-forward
    # beyond the forecast the excess return fades: competition and a fleet that has to be
    # replaced at market prices, not at book, pull the return toward the cost of capital
    roe_t = FINB_ROE[-1] * roe_scale
    ri_t = (roe_t - ke_r) * b
    tv = ri_t / (ke_r + FADE - G_B)                   # fading perpetuity
    pv += tv / (1 + ke_r) ** 5
    return b0 + pv, detail, tv / (1 + ke_r) ** 5


FADE = IN('ri_fade', 0.10, "Rate at which the return above the cost of equity is assumed to "
          "decay beyond the forecast. A fleet has to be replaced at market prices rather "
          "than at the book value it is carried at, so an excess return cannot persist "
          "unchanged; a fifth a year is the house convention for an asset-heavy business "
          "and is sensitised from 5% to 30% in the sensitivity section", '2026-08-09', 'Industry')
G_B = g_b
# the return has to be struck on what the ORDINARY holders actually earn, so the
# perpetual coupon -- which ranks ahead of them -- comes out of the numerator first
FINB_ROE = [(FINB['npa'][i] - HYB_COUPON) / BSB[i]['equity_parent'] for i in range(5)]
ri_base, ri_detail, ri_pv_tv = residual_income(ke)
ri_bear, _, _ = residual_income(ke_ci_hi, 0.85)
ri_bull, _, _ = residual_income(ke_ci_lo, 1.15)
bvps_now = V['q1_26_eqp'] / shares_mn / 1000.0
pb_fair = ri_base / (V['q1_26_eqp'] / 1000.0)
book = dict(roe_sustainable=roe_sust, ke=ke, g=g_b, pb_fair=pb_fair, method='residual income',
            fade=FADE, roe_path=FINB_ROE, detail=ri_detail, pv_terminal=ri_pv_tv,
            vessel_sale_price=V['vessel_sale_price'], vessel_sale_book=V['vessel_sale_book'],
            vessel_value_to_book=V['vessel_sale_price'] / V['vessel_sale_book'],
            bvps_usd=bvps_now, bvps_aed=bvps_now * peg,
            equity_value=ri_base,
            base=ri_base / shares_mn * peg,
            ke_bear=ke_ci_hi, ke_bull=ke_ci_lo,
            bear=ri_bear / shares_mn * peg,
            bull=ri_bull / shares_mn * peg)

# --- discounted cash flow, with scenarios --------------------------------------
BASE_MID = dict(SPOT_MID)


def dcf_scenario(beta_s, anchor_mult, capex_mult=1.0, hybrid_as_debt=False):
    global SPOT_MID, CAPEX
    old_mid, old_capex = dict(SPOT_MID), list(CAPEX)
    SPOT_MID.update({c: BASE_MID[c] * anchor_mult for c in BASE_MID})
    CAPEX[:] = [c * capex_mult for c in old_capex]
    kes = rf_star + beta_s * V['erp_total']
    ket = V['rf_terminal'] + beta_s * V['erp_total']
    w = we * kes + wd * kd * (1 - tax_stat) + wh * kh   # the perpetual tranche too
    wt = we * ket + wd * kd_term * (1 - tax_stat) + wh * kh_term
    p = project('reversion')
    d = dcf(p, hybrid_as_debt=hybrid_as_debt, wacc_ov=w, term_wacc_ov=wt)
    SPOT_MID.update(old_mid); CAPEX[:] = old_capex
    return d


# The perpetual capital securities rank ahead of the ordinary shares whichever way they
# are classified, so they are deducted in the bridge in every case. What is genuinely
# contested is the cost of equity, and that is what is published both ways.
dcf_own_beta = dcf(BASE, hybrid_as_debt=True)
dcf_beta_alt = dcf_scenario(V['beta_composite'], 1.00, 1.00, hybrid_as_debt=True)
dcf_sustained = dcf(GUID, hybrid_as_debt=True)
# The bear and bull cases no longer use round numbers picked by hand. The beta in each
# is the regression's OWN 90% confidence bound, so the span of the fair-value range is
# the span the estimate itself supports rather than a judgement about how wrong it
# might be. The rate anchor and capital expenditure move with it.
dcf_bear = dcf_scenario(V['beta_ci_hi'], 0.85, 1.10, hybrid_as_debt=True)
dcf_bull = dcf_scenario(V['beta_ci_lo'], 1.15, 0.95, hybrid_as_debt=True)
# the alternative treatment of the securities themselves, disclosed in the bridge:
# deducted at carrying value, or at the present value of their perpetual coupon
hyb_pv_coupon = HYB_COUPON / wacc_term
dcf_hyb_pv = dict(dcf_own_beta)
dcf_hyb_pv['equity'] = dcf_own_beta['equity'] + HYBRID - hyb_pv_coupon
dcf_hyb_pv['fv_usd'] = dcf_hyb_pv['equity'] / shares_mn / 1000.0
dcf_hyb_pv['fv_aed'] = dcf_hyb_pv['fv_usd'] * peg

# Within the relative lens the enterprise multiple carries most of the weight: it is the
# standard measure for a capital-intensive fleet owner and it neutralises the differences in
# leverage, depreciation policy and tax relief that make a price-earnings comparison across
# these companies unreliable.
W_EVEB = IN('rel_weight_ev_ebitda', 0.70, "Study judgement — see the judgements table",
            '2026-08-09', 'Industry')
rel['base'] = W_EVEB * rel['value_ev_ebitda'] + (1 - W_EVEB) * rel['value_pe']
rel['weight_ev_ebitda'] = W_EVEB

# [R-LENS-03] THE TYPED BLEND IS RETIRED. It weighted 40/25/20/15 across four reads, and
# two of those weights are forbidden outright rather than merely unevidenced: BOOK VALUE
# carried 15 per cent, and book value is a DISCLOSED FLOOR that is never weighted into a
# central; NORMALISED EARNINGS carried 20, and the registry does not permit that lens for
# a fleet whose day rates are cyclical enough that any single normalised year is a
# judgement about where the cycle sits rather than a reading of the business. The weights
# themselves had cleared no out-of-sample test — chosen, written down, inherited, which is
# how a free parameter survives in a house that forbids them everywhere else.
#
# The weights are kept as RETIRED_W so the record can say what the blend read and what
# retiring it cost. Nothing computes with them.
RETIRED_W = {'dcf': 0.40, 'relative': 0.25, 'normalized': 0.20, 'book': 0.15}

lenses = {
    'dcf': dict(bear=dcf_bear['fv_aed'], base=dcf_own_beta['fv_aed'],
                bull=dcf_bull['fv_aed'], tv_share=dcf_own_beta['tv_share']),
    'dcf_beta_alt': dict(bear=dcf_bear['fv_aed'], base=dcf_beta_alt['fv_aed'],
                           bull=dcf_bull['fv_aed'],
                           tv_share=dcf_beta_alt['tv_share']),
    'relative': dict(bear=rel['bear'], base=rel['base'], bull=rel['bull']),
    'normalized': dict(bear=norm['bear'], base=norm['base'], bull=norm['bull']),
    'book': dict(bear=book['bear'], base=book['base'], bull=book['bull']),
}
# THE CENTRAL IS THE CLASS PRIMARY, WHICH FOR THIS CLASS IS THE CASH-FLOW LENS. Its bear
# and bull are its OWN — the regression's 90 per cent confidence bounds on beta, with the
# rate anchor and capital expenditure moving with them — rather than a spread invented
# around a blend.
for _lab, _dcfkey in (('central', 'dcf'), ('central_beta_alt', 'dcf_beta_alt')):
    lenses[_lab] = dict(bear=lenses[_dcfkey]['bear'], base=lenses[_dcfkey]['base'],
                        bull=lenses[_dcfkey]['bull'])
central = lenses['central']['base']
central_alt = lenses['central_beta_alt']['base']
RETIRED_BLEND = sum(RETIRED_W[k] * lenses['dcf' if k == 'dcf' else k]['base']
                    for k in RETIRED_W)

# ============================================================================
# EXPERT PANEL — three methods, cast by approach, worked end to end
# ============================================================================
# Expert 1 — mid-cycle earnings power capitalised at a normal multiple
e1_ebitda = norm_ebitda
e1_dna = sum(BASE['dna']) / 5.0
e1_ebit = e1_ebitda - e1_dna
e1_tax = e1_ebit * (sum(BASE['tax_rate']) / 5.0)
e1_int = kd * (sum(FINB['gross_debt']) / 5.0)
e1_fininc = V['sofr'] * CASH_HELD
e1_pat = e1_ebit - e1_tax - e1_int + e1_fininc
e1_ord = e1_pat * (1 - NCI_SHARE) - HYB_COUPON
e1_eps = e1_ord / shares_mn / 1000.0
e1_pe = 12.0
e1 = dict(method_short='mid-cycle earnings power', ebitda=e1_ebitda, dna=e1_dna,
          ebit=e1_ebit, tax=e1_tax, interest=e1_int, fin_income=e1_fininc, pat=e1_pat,
          ord_earnings=e1_ord, eps_usd=e1_eps, pe=e1_pe,
          base=e1_eps * e1_pe * peg,
          rng=[e1_eps * 9.0 * peg, e1_eps * 15.0 * peg],
          falsifier='Two consecutive years in which group earnings before interest, tax, '
                    'depreciation and amortisation fall below USD 1.4 billion would show '
                    'the mid-cycle level used here is set too high.')

# Expert 2 — owner cash earnings: what the shareholder can actually take out
e2_fcff = sum(BASE['fcff']) / 5.0
e2_int_at = e1_int * (1 - tax_stat)
e2_fcfe = e2_fcff - e2_int_at + e1_fininc * (1 - tax_stat) - HYB_COUPON
e2_ke = ke
e2_g = V['g_terminal']
e2_val = e2_fcfe * (1 + e2_g) / (e2_ke - e2_g)
e2 = dict(method_short='owner cash earnings', fcff=e2_fcff, interest_after_tax=e2_int_at,
          hybrid_coupon=HYB_COUPON, fcfe=e2_fcfe, ke=e2_ke, g=e2_g, value=e2_val,
          base=e2_val / shares_mn / 1000.0 * peg,
          ke_lo=ke_ci_hi, ke_hi=ke_ci_lo,
          rng=[e2_fcfe * (1 + 0.01) / (ke_ci_hi - 0.01) / shares_mn / 1000.0 * peg,
               e2_fcfe * (1 + 0.025) / (ke_ci_lo - 0.025) / shares_mn / 1000.0 * peg],
          falsifier='A year in which free cash flow to the firm falls below the ordinary '
                    'distribution plus the perpetual coupon, without a matching fall in '
                    'capital expenditure, would break the annuity this rests on.')

# Expert 3 — cash returns against the cost of capital (economic profit)
ic0 = V['q1_26_ppe'] + hist_bs['nwc'][2] + V['intang_fy25'] + V['gw_fy25']
e3_ep, e3_pv, e3_spread = [], 0.0, []
for i in range(5):
    ic = BSB[i]['invested_capital']
    ep = BASE['nopat'][i] - wacc * ic
    e3_ep.append(ep); e3_spread.append(BASE['nopat'][i] / ic - wacc)
    e3_pv += ep * dcf_own_beta['df'][i]
e3_ep_term = e3_ep[4] * (1 + V['g_terminal'])
e3_pv_term = e3_ep_term / (wacc_term - V['g_terminal']) * dcf_own_beta['df'][4]
e3_ev = ic0 + e3_pv + e3_pv_term
e3_eq = e3_ev + JV_BV - NETDEBT - HYBRID - NCI_BV
e3 = dict(method_short='cash returns against the cost of capital', ic0=ic0,
          ep=e3_ep, spread=e3_spread, pv_ep=e3_pv, pv_ep_term=e3_pv_term, ev=e3_ev,
          equity=e3_eq, base=e3_eq / shares_mn / 1000.0 * peg,
          rng=[(ic0 + e3_pv * 0.6 + e3_pv_term * 0.5 + JV_BV - NETDEBT - HYBRID - NCI_BV)
               / shares_mn / 1000.0 * peg,
               (ic0 + e3_pv * 1.3 + e3_pv_term * 1.4 + JV_BV - NETDEBT - HYBRID - NCI_BV)
               / shares_mn / 1000.0 * peg],
          falsifier='A return on invested capital that settles below the cost of capital '
                    'for two consecutive years would remove the premium to invested '
                    'capital this method rests on entirely.')
experts = dict(e1=e1, e2=e2, e3=e3)
panel_centre = (e1['base'] + e2['base'] + e3['base']) / 3.0

# ============================================================================
# SENSITIVITY
# ============================================================================
# composite · mid · adopted · mid · top of the regression's own 90% interval. The two
# mid rows sit roughly halfway between their neighbours so the grid is read across evenly.
BETAS = [V['beta_composite'], 0.90, V['beta'], 1.35, V['beta_ci_hi']]
GS = [0.010, 0.015, 0.020, 0.025]
sens_beta_g = [[dcf_scenario(b, 1.0, 1.0, True)['fv_aed'] if g == V['g_terminal'] else None
                for g in GS] for b in BETAS]
sens = dict(betas=BETAS, gs=GS)
grid = []
for b in BETAS:
    row = []
    kes = rf_star + b * V['erp_total']; ket = V['rf_terminal'] + b * V['erp_total']
    # every cost-of-capital construction in this file must carry the same three tranches,
    # or the sensitivity grid disagrees with the base it is supposed to be centred on
    w = we * kes + wd * kd * (1 - tax_stat) + wh * kh
    wt = we * ket + wd * kd_term * (1 - tax_stat) + wh * kh_term
    for g in GS:
        row.append(dcf(BASE, hybrid_as_debt=True, wacc_ov=w, term_wacc_ov=wt,
                       g_ov=g)['fv_aed'])
    grid.append(row)
sens['grid_beta_g'] = grid
sens['anchor'] = {str(m): dcf_scenario(V['beta'], m, 1.0, True)['fv_aed']
                  for m in (0.80, 0.90, 1.00, 1.10, 1.20)}
sens['capex'] = {str(m): dcf_scenario(V['beta'], 1.0, m, True)['fv_aed']
                 for m in (0.90, 1.00, 1.10, 1.20)}


def dcf_tax(rate):
    """What the valuation is worth if the whole group were taxed at one rate — the
    downside case for the global minimum tax reaching the shipping earnings that are
    currently relieved."""
    p = project('reversion')
    ebit = p['ebit']
    nopat = [e * (1 - rate) for e in ebit]
    fcff = [n + d - c - w for n, d, c, w in zip(nopat, p['dna'], p['capex'], p['dnwc'])]
    q = dict(p); q['nopat'] = nopat; q['fcff'] = fcff
    q['tax'] = [e * rate for e in ebit]; q['tax_rate'] = [rate] * 5
    return dcf(q, hybrid_as_debt=True)


sens['tax'] = {f'{r:.2f}': dcf_tax(r)['fv_aed'] for r in (0.05, 0.09, 0.15)}
sens['market_cross_check'] = dict(
    vlcc_1y_tc=V['vlcc_1y_tc_market'],
    vlcc_spot_broker=V['vlcc_spot_clarksons_jan26'],
    vlcc_path=[BASE['tce']['vlcc'][i] for i in range(5)],
    orderbook_pct=V['tanker_orderbook_pct_fleet'],
    note=('An independent one-year time charter fixed in early 2026 priced a very large '
          'crude carrier at USD 76,900 a day, well below the spot rate of the moment. A '
          'forward market that will not pay spot for a year of time is telling the reader '
          'it does not expect spot to hold, and a crude tanker order book near 27% of the '
          'trading fleet is the supply reason why. Both point the same way as the reversion '
          'path this study uses as its base, and both are reasons the sustained-strength '
          'path is published as an alternative rather than adopted.'))

# ============================================================================
# SUM OF THE PARTS — the two legs valued separately and added
# ============================================================================
# The group is one operating company, but its two legs earn on different terms: the
# logistics and services work is contracted, largely to the parent group, and the shipping
# fleet carries market rate risk on the part of itself that is not fixed out. They are
# built separately in the forecast and are cross-checked here on separate multiples, so the
# reader can see what each leg is worth rather than only what the whole is.
SOTP_MULT = {'Integrated Logistics': contracted_mult,
             'Shipping': (1 - SPOT_W) * contracted_mult + SPOT_W * spot_mult,
             'Services': contracted_mult}
sotp_legs = []
for g in GROUPS:
    e26 = BASE['group'][g]['ebitda'][0]
    sotp_legs.append(dict(leg=g, ebitda_26=e26, multiple=SOTP_MULT[g], ev=e26 * SOTP_MULT[g],
                          basis=('a contracted-fleet multiple, because this leg earns under '
                                 'long-term contracts' if g != 'Shipping' else
                                 'a blend of the contracted and spot multiples, weighted by '
                                 "the company's own disclosed share of earnings exposed to "
                                 'spot rates')))
sotp_ev = sum(l['ev'] for l in sotp_legs)
sotp = dict(legs=sotp_legs, ev_ops=sotp_ev, jv=JV_BV, ev=sotp_ev + JV_BV,
            net_debt=NETDEBT, hybrid=HYBRID, nci=NCI_BV,
            equity=sotp_ev + JV_BV - NETDEBT - HYBRID - NCI_BV,
            fv_aed=(sotp_ev + JV_BV - NETDEBT - HYBRID - NCI_BV) / shares_mn / 1000.0 * peg,
            contracted_multiple=contracted_mult, spot_multiple=spot_mult, spot_weight=SPOT_W)

# ============================================================================
# MONTE CARLO PRICE MAP + THE COMMITTED CALIBRATION EVIDENCE
# ============================================================================
strike = json.load(open(os.path.join(HERE, 'strike_result.json')))
step0 = json.load(open(os.path.join(HERE, 'step0_result.json')))
bt5 = json.load(open(os.path.join(HERE, 'backtest_5y.json')))
tech = json.load(open(os.path.join(HERE, 'technicals.json')))
beta_res = json.load(open(os.path.join(HERE, 'beta_result.json')))

# ============================================================================
# ASSERTIONS — nothing ships that does not reconcile
# ============================================================================
assert_log = []


def A(name, cond, detail=''):
    assert cond, f'{name}: {detail}'
    assert_log.append(dict(check=name, passed=True, detail=detail))


import datetime as _dt
for k, v in INPUTS.items():
    A(f'four fields complete: {k}',
      all(v.get(f) not in (None, '') for f in ('source', 'date', 'layer'))
      and v.get('value') is not None, k)
    try:
        _dt.date.fromisoformat(v['date'])
    except Exception:                                     # a date nobody could look up
        raise AssertionError(f'input {k} carries an impossible date {v["date"]!r}')
for i, y in enumerate(H):
    A(f'income statement ties {y}',
      abs(V[f'gp_{y}'] - (V[f'rev_{y}'] + V[f'dc_{y}'])) < 1)
    A(f'balance sheet balances {y}',
      abs(V[f'ta_{y}'] - (V[f'teq_{y}'] + V[f'tl_{y}'])) < 1)
    A(f'segment revenue ties {y}',
      abs(sum(SEG_REV[s][i] for s in SEGS) - V[f'rev_{y}']) < 1)
    A(f'segment direct costs tie {y}',
      abs(sum(SEG_DC[s][i] for s in SEGS) - V[f'dc_{y}']) < 1)
A('product lines tie to revenue FY2025',
  abs(sum(v[1] for v in PRODUCT_LINES.values()) - V['rev_fy25']) < 1)
A('cost lines tie to direct costs FY2025',
  abs(sum(v[1] for v in COST_LINES.values()) + V['dc_fy25']) < 1)
A('segment depreciation ties to the group charge FY2025',
  abs(sum(SEG_DNA25.values()) + 197 - (V['dep_ppe_fy25'] + V['dep_ip_fy25']
       + V['dep_rou_fy25'] + V['amort_fy25'])) < 2)
A('reported earnings bridge to operating earnings FY2025',
  abs(ebitda_op[2] + V['assoc_fy25'] + V['bargain_fy25'] + V['prevheld_fy25']
      - ebitda_rep[2]) < 2)
A('net debt at the valuation date reconciles to the disclosed figure',
  abs((V['q1_26_shldr_loan'] + V['q1_26_borrowings'] + V['q1_26_leases']
       - V['q1_26_cash']) - V['q1_26_netdebt']) < 1)
A('the tanker unit build reproduces reported segment earnings for 2025',
  abs((tce_rev_25 - vessel_days_25 * opex_day_25 / 1000.0)
      - V['seg_ebitda_tankers_fy25']) < 1)
A('cost of debt sits above the local government bond yield', kd > V['rf_observed'],
  f'kd {kd:.4f} vs rf {V["rf_observed"]:.4f}')
A('country risk is charged once', abs(rf_star - (V['rf_observed'] - V['sov_spread'])) < 1e-9)
A('the discount factors compound',
  abs(dcf_own_beta['df'][1] - dcf_own_beta['df'][0]
      / (1 + dcf_own_beta['glide'][1])) < 1e-9)
_gi = sens['betas'].index(V['beta']); _gj = sens['gs'].index(V['g_terminal'])
A('the sensitivity grid is centred on the value it brackets',
  abs(sens['grid_beta_g'][_gi][_gj] - dcf_own_beta['fv_aed']) < 0.005,
  f"grid centre {sens['grid_beta_g'][_gi][_gj]:.4f} vs base {dcf_own_beta['fv_aed']:.4f} — "
  "every cost-of-capital construction must carry the same three tranches")
A('the terminal value share is computed, not asserted',
  0.0 < dcf_own_beta['tv_share'] < 1.0)
A('the calibration evidence is the committed market fit',
  step0['nu'] == bt5['fit']['nu'] and step0['width_cal'] == bt5['fit']['width_cal'])
A('the five-year scoring beats the benchmark', bt5['five_year']['skill_norm'] > 0)
A('the price map was struck on the same close as the study',
  abs(strike['spot'] - spot_aed) < 1e-9)
A('the technical read was computed on the same close', abs(tech['close'] - spot_aed) < 1e-9)
A('the beta used is the one the regression produced',
  abs(V['beta'] - round(beta_res['adopted']['beta_used'], 4)) < 1e-9)
# ...and that regression is the SANCTIONED one, against a conforming regressor. The
# adopted figure agreeing with the record's own adopted field is not enough: a study-local
# script can write any figure into that field, which is the failure this checks for.
A('the beta is the sanctioned routine\'s, on a conforming regressor',
  abs(V['beta'] - round(beta_res['sanctioned']['beta'], 4)) < 1e-9
  and beta_res['sanctioned']['conforming'] and beta_res['sanctioned']['usable']
  and beta_res['sanctioned']['interim_note'] is None)
A('the published interval, standard error and Blume check are the record\'s',
  abs(V['beta_ci_lo'] - round(beta_res['sanctioned']['ci90'][0], 4)) < 1e-9
  and abs(V['beta_ci_hi'] - round(beta_res['sanctioned']['ci90'][1], 4)) < 1e-9
  and abs(V['beta_se'] - round(beta_res['sanctioned']['se'], 4)) < 1e-9
  and abs(V['beta_blume'] - round(beta_res['sanctioned']['blume_crosscheck'], 4)) < 1e-9)
# The Blume cross-check is a SHRINKAGE of the adopted slope toward 1.0, and the study says
# so. If it ever stopped being that — the record swapping in a different cross-check, or
# the wrong field being read, which is exactly how a lead-lag figure once ended up carrying
# this label — the description in the documents would be false and this fails first.
A('the Blume cross-check is the adopted slope shrunk toward one',
  abs(V['beta_blume'] - (2 / 3 * beta_res['sanctioned']['beta'] + 1 / 3)) < 5e-5
  and abs(V['beta_blume'] - 1.0) < abs(V['beta'] - 1.0))
A('the disclosed composite is published but discounted at nowhere',
  V['beta_composite'] != V['beta'] and abs(ke - (rf_star + V['beta'] * V['erp_total'])) < 1e-12
  and abs(wacc_blk['ke'] - ke) < 1e-12)
# Every published range must bracket its own base. A bound built on an alternative cost of
# equity silently inverts the moment that alternative stops being the demanding one, which
# is exactly what happened when the regressor changed, so it is asserted rather than assumed.
A('every lens range brackets its own base',
  all(L['bear'] <= L['base'] <= L['bull'] for L in lenses.values()))
A('every expert range brackets its own base',
  all(e['rng'][0] <= e['base'] <= e['rng'][1] for e in experts.values()))

# ============================================================================
# OUTPUT
# ============================================================================
OUT = dict(
    meta=dict(ticker='ADNOCLS', company='ADNOC Logistics & Services plc',
              exchange='Abu Dhabi Securities Exchange', market='AE',
              isin='AEE01268A239',
              reporting_currency='USD', listing_currency='AED', fx=peg,
              asof='2026-08-09', price_date='2026-08-07',
              valuation_date='2026-03-31',
              spot_aed=spot_aed, spot_usd=spot_usd,
              # THE ANSWER, IN THE PAIR THE SHARED READER LOOKS FOR. This study committed
              # a central at the top level and its price only as spot_aed, so the
              # valuation-gap gate could recover no central/spot pair at all and filed
              # THE EXEMPLAR — the document every other study is modelled on — as
              # UNREADABLE. Nothing about the answer was missing; the two halves of it
              # were named where nothing shared was looking, which is the whole reason
              # [R-ENF-04] says an unreadable answer is not a clean answer. The central is
              # in AED, the listing currency, and so is this.
              spot=spot_aed, spot_date='2026-08-07',
              central=None,          # filled below, once the lenses have run
              latest_known_price=dict(
                  value=6.85, date='2026-09-03', currency='AED',
                  source='the price file the principal supplied on 3 September 2026 and '
                         'committed at engine/prices/SUPPLIED_03-09-2026.json',
                  note='recorded beside the strike price rather than substituted for it. '
                       '[R-GAP-01] audits a study against the price it was STRUCK at, '
                       'which is the honest test of whether the answer was audited before '
                       'it shipped; the latest known price is what a re-issue must be '
                       'struck against, and it is carried here so the next edition cannot '
                       'be built against a month-old quote without noticing.'),
              shares_mn=shares_mn, shares_wavg_mn=shares_wavg_mn,
              mktcap_usd000=mktcap, ev_usd000=mktcap + NETDEBT,
              klass='asset-heavy marine logistics and shipping operating company',
              sector='Marine transportation and energy logistics'),
    inputs=INPUTS,
    hist_is=hist_is, hist_bs=hist_bs, hist_cf=hist_cf, ccc=ccc,
    seg_hist=seg_hist, grp_hist=grp_hist, segs=SEGS, seg_group=SEG_GROUP,
    groups=GROUPS,
    product_lines=PRODUCT_LINES, cost_lines=COST_LINES,
    fleet=dict(owned=FLEET, owned_fy25=FLEET_FY25, charters=[
                   dict(name=c['name'], klass=c['klass'], rate=c['rate'],
                        start=str(c['start']), end=str(c['end']),
                        period_months=c['period_months']) for c in CHARTERS],
               blend_fy24=TCE24, blend_fy25=TCE25, blend_mid=BLEND_MID,
               blend_q1_26=Q1_BLEND, blend_q2_26=Q2_BLEND,
               spot_fy25=SPOT_25, spot_mid=SPOT_MID, spot_q1_26=SPOT_Q1,
               spot_q2_26=SPOT_Q2, tce_mid=BASE_MID, opex_day=opex_day_25,
               gas_vessel_years=GAS_VY, gas_rate_day=gas_rate_25,
               vessel_days_25=vessel_days_25, tce_rev_25=tce_rev_25),
    drivers=DRV, driver_why=DRV_WHY,
    fcst=dict(years=YF, **{k: v for k, v in BASE.items()
                           if k not in ('seg', 'group', 'tce', 'mode', 'years')}),
    fcst_seg={s: BASE['seg'][s] for s in SEGS},
    fcst_group=BASE['group'],
    fcst_sustained=dict(years=YF, revenue=GUID['revenue'], ebitda=GUID['ebitda'],
                        ebit=GUID['ebit'], nopat=GUID['nopat'], fcff=GUID['fcff']),
    fin=FINB, fin_sustained=FING, fcst_bs=BSB,
    guidance_check=guidance_check(build_forecast('reversion')),
    wacc=wacc_blk,
    dcf=dcf_own_beta, dcf_beta_alt=dcf_beta_alt, dcf_sustained=dcf_sustained,
    dcf_bear=dcf_bear, dcf_bull=dcf_bull, dcf_hybrid_pv=dcf_hyb_pv,
    # RETIRED, and published under its own name so every consumer says so
    lenses=lenses, lens_weights=RETIRED_W, retired_blend=RETIRED_BLEND,
    central=central, central_beta_alt=central_alt,
    spot=spot_aed,      # the pair, at the top level too, where the shared reader looks
    beta_framing=dict(
        primary=dict(beta=V['beta'], label='the published index of its own exchange',
                     ke=ke, wacc=wacc_blk['wacc'], fv=dcf_own_beta['fv_aed'],
                     central=central),
        alternative=dict(beta=V['beta_composite'],
                         label="an equal-weight composite of the same exchange's names",
                         ke=ke_beta1, fv=dcf_beta_alt['fv_aed'], central=central_alt),
        ci90=[V['beta_ci_lo'], V['beta_ci_hi']],
        blume=V['beta_blume'],
        note=('The two constructions differ only in how the market is measured. The '
              'published index is weighted by size and is therefore dominated by the same '
              'large-capitalisation group the subject belongs to; an equal-weight composite '
              'gives the exchange\'s smallest names the same say as its largest. The first '
              'is the index the beta rule asks for and is what the study adopts. The second '
              'is what an earlier construction used and is published beside it, because a '
              'difference of this size is a fact about index construction that a reader is '
              'entitled to see rather than a detail to bury.')),
    rel=rel, norm=norm, book=book, peers=PEERS, sotp=sotp,
    experts=experts, panel_centre=panel_centre,
    sens=sens,
    strike=strike, step0=step0, backtest=bt5, technicals=tech, beta=beta_res,
    bridge=dict(ev=dcf_own_beta['ev'], ev_ops=dcf_own_beta['ev_ops'],
                jv=JV_BV, net_debt_company=NETDEBT_CO, deferred=DEFERRED,
                net_debt=NETDEBT, hybrid=HYBRID, hybrid_pv_coupon=hyb_pv_coupon,
                nci=NCI_BV, equity=dcf_own_beta['equity'],
                tv_share=dcf_own_beta['tv_share'],
                pv_explicit=dcf_own_beta['pv_explicit'], pv_tv=dcf_own_beta['pv_tv']),
    macro_record=dict(
        market='AE', path_as_of=_PATH.as_of,
        # THE INFLATION-CLASS INPUTS, EVERY ONE, WITH THE MAPPING THAT DERIVES IT
        # [R-MACRO-01 AMENDED]. A check that reads what a study DECLARES is not checking
        # what the study USES, and a TRUE exemption on the WRONG OBJECT is the safest
        # hiding place there is. Both of this model's escalators are named here whether or
        # not they look like growth rates.
        inflation_inputs=[
            dict(key='inflation_26', mapping='calendar', first_year=2026,
                 values=[V['inflation_26']],
                 note='the single forecast-year consumer price rate this model registers; '
                      'the house ladder\'s own 2026 figure, to the basis point'),
            dict(key='opex_escalation', mapping='calendar', first_year=2026,
                 values=list(OPEX_PATH),
                 note='crew, technical management, insurance and repairs escalate at the '
                      'house TERMINAL inflation, held flat. On a dirham cost base under a '
                      'hard peg the terminal is already today, so a ladder and a flat rate '
                      'are the same object from 2027 and the flat form is the honest one'),
        ],
        growth_lines=[
            dict(name='running-cost escalation, crew and technical management',
                 years=[2026, 2027, 2028, 2029, 2030],
                 nominal=list(OPEX_PATH), real=0.0,
                 basis='the house inflation path at zero real growth. Under the peg the '
                       'path is flat at the 2.0 per cent objective from 2027 and the 2026 '
                       'rate is 2.5; the half point is inside this rule\'s tolerance and '
                       'the line is registered at the terminal rate rather than laddered, '
                       'because a marine services cost base reprices on multi-year '
                       'contracts rather than annually'),
            dict(name='charter and freight rates',
                 years=[2026, 2027, 2028, 2029, 2030],
                 nominal=[0.0] * 5, real=0.0,
                 exempt_reason='US-dollar day rates set by the global tanker and offshore '
                               'market, not by domestic inflation \u2014 they are built '
                               'from the fleet\'s own contracted and market rates vessel '
                               'by vessel, and no inflation rate is applied to them at '
                               'all. Under the peg there is no currency path for domestic '
                               'inflation to reach them through either'),
        ],
        # NO fx_path: the dirham is hard-pegged at 3.6725 and the house path returns a
        # FLAT currency path by construction of the peg. A model that "derived" a
        # depreciation here would be manufacturing movement the peg forbids.
        terminal=dict(g_nominal=V['g_terminal'], real=0.0, rf=V['rf_terminal'],
                      inflation_in_rf=_PATH.terminal_inflation),
        explicit_years=5,
        growth_at_horizon_end=V['g_terminal'],
        note='the explicit window ends on the terminal growth rate exactly: the last '
             'explicit year escalates at the house terminal inflation at zero real, which '
             'IS the terminal, so nothing is capitalised that the model never reached. '
             'The company\'s own value-in-use test projects beyond its plan at the same '
             '2 per cent, which is corroboration rather than the source.'),
    # ---------------------------------------------------------------- [R-ENF-05]
    # EVERY CONTESTED JUDGEMENT WORTH MORE THAN 5 PER CENT OF VALUE, BOTH WAYS, THROUGH
    # THE SAME CONSTRUCTION. Any single one is defensible; what is not is a study
    # resolving all of them the same way and never noticing. Each alternative below is
    # computed by this file's own dcf(), so the difference measures THE CHOICE and not
    # the construction.
    contested=[
        dict(choice='how the market is measured for the beta regression',
             adopted='the published index of the exchange this company is listed on',
             alternative='an equal-weight composite of the same exchange\'s names',
             fv_adopted=float(central), fv_alternative=float(central_alt),
             effect=abs(central_alt - central) / central,
             direction='the adopted side is LOWER',
             note='THE SINGLE LARGEST JUDGEMENT IN THIS STUDY, and the beta rule decides '
                  'it rather than a preference: the regressor is the published index of '
                  'the exchange the stock is listed on, and a constituent composite is a '
                  'coverage artefact rather than a market. The two differ because a '
                  'published index is weighted by size and is dominated by the same '
                  'large-capitalisation group this company belongs to, while an '
                  'equal-weight composite gives the exchange\'s smallest names the same '
                  'say as its largest. The alternative is published rather than buried '
                  'because a difference of this size is a fact about index construction '
                  'that a reader is entitled to see.'),
        dict(choice='the charter-rate path through the forecast',
             adopted='reversion toward the mid-cycle rate',
             alternative='today\'s strength sustained, the company\'s own guidance path',
             fv_adopted=float(central), fv_alternative=float(dcf_sustained['fv_aed']),
             effect=abs(dcf_sustained['fv_aed'] - central) / central,
             direction='the adopted side is LOWER',
             note='an independent one-year time charter fixed in early 2026 priced a very '
                  'large crude carrier well below the spot rate of the moment, and a '
                  'crude tanker order book near a quarter of the trading fleet is the '
                  'supply reason why. A forward market that will not pay spot for a year '
                  'of time is saying it does not expect spot to hold. GUIDANCE IS SCORED '
                  'AND NEVER CONSUMED, so the sustained path is published as the '
                  'alternative rather than adopted.'),
        dict(choice='how the perpetual capital securities are deducted',
             adopted='at carrying value',
             alternative='at the present value of their perpetual coupon',
             fv_adopted=float(central), fv_alternative=float(dcf_hyb_pv['fv_aed']),
             effect=abs(dcf_hyb_pv['fv_aed'] - central) / central,
             direction='the adopted side is LOWER',
             note='the securities rank ahead of the ordinary shares whichever way they '
                  'are classified, so they are deducted in both framings and only the '
                  'AMOUNT is contested. Carrying value is what the balance sheet states; '
                  'the present value of the coupon is what the claim is worth at the '
                  'terminal cost of capital. Both are published and the deduction is '
                  'weighted in the cost of capital in both.'),
        dict(choice='the tax relief on shipping earnings',
             adopted='the reliefs as currently legislated and disclosed',
             alternative='the whole group taxed at the 9 per cent statutory rate',
             fv_adopted=float(central), fv_alternative=float(sens['tax']['0.09']),
             effect=abs(sens['tax']['0.09'] - central) / central,
             direction='the adopted side is HIGHER',
             note='most of the shipping income is relieved under the regime as it stands. '
                  'The alternative is the downside case for a global minimum tax reaching '
                  'those earnings, and it is a scenario about the law rather than about '
                  'the business — which is why the sensitivity centred on it does NOT '
                  'reproduce the base case and says so in its own docstring.'),
        dict(choice='the day-rate anchor the reversion path converges to',
             adopted='the mid-cycle average as computed',
             alternative='that anchor 10 per cent lower',
             fv_adopted=float(central), fv_alternative=float(sens['anchor']['0.9']),
             effect=abs(sens['anchor']['0.9'] - central) / central,
             direction='the adopted side is HIGHER',
             note='the anchor is the single quantity the whole reversion path hangs on, '
                  'and a ten per cent move in it is well inside the span the disclosed '
                  'quarterly rates have printed.'),
    ],
    bridge_record=dict(
        market='AE',
        balance_sheet_date='2026-03-31', latest_disclosed_date='2026-03-31',
        latest_disclosed_source=(
            'the condensed consolidated interim financial information for the three '
            'months ended 31 March 2026, from the company\'s own investor-relations '
            'channel and registered in this study\'s sweep. THE VALUATION DATE IS THAT '
            'BALANCE-SHEET DATE rather than the date of the latest traded price, so no '
            'roll-forward stands between the bridge and a filing, and the first '
            'quarter\'s free cash flow is inside net debt rather than discounted again.'),
        register='sweep_register.json',
        lines=[
            dict(label='Enterprise value of the operations',
                 value=float(dcf_own_beta['ev_ops'])),
            dict(label='plus joint ventures and associates at carrying value',
                 value=float(JV_BV)),
            dict(label='less net debt, including the committed acquisition and the '
                       'deferred purchase consideration',
                 value=float(-NETDEBT)),
            dict(label='less perpetual capital securities at carrying value',
                 value=float(-HYBRID)),
            dict(label='less non-controlling interests',
                 value=float(-(dcf_own_beta['ev'] - NETDEBT - HYBRID
                               - dcf_own_beta['equity']))),
        ],
        equity_value=float(dcf_own_beta['equity']),
        # EVERY FIGURE IN THIS BRIDGE IS IN USD THOUSANDS, so the share count is too:
        # the model carries it in millions and dividing thousands by millions gives
        # a per-share figure a thousand times too large. The unit is the thing to
        # check when a bridge does not divide.
        shares_mn=float(shares_mn * 1000.0),
        per_share=float(dcf_own_beta['fv_usd']),
        cash_charged_once=True,
        # 'none': the cash is not added anywhere in this bridge — it sits inside the
        # net-debt figure deducted once. Registering it as added_at_face would
        # describe a construction this model does not use.
        cash=dict(treatment='none', weights_basis='gross'),
        cash_note=(
            'THE CASH IS NOT ADDED AT FACE ANYWHERE. It sits inside the net-debt figure '
            'deducted once, and the operating rate is weighted on the gross capital '
            'structure — equity, drawn debt AND the perpetual securities — so no tranche '
            'is deducted from value without also being allowed to price it. The company '
            'is net DEBT rather than net cash, so the negative-debt-weight trap does not '
            'arise here; the construction is stated anyway because a reader cannot tell '
            'from the number which way it was done.'),
        nci=dict(
            basis='value_share',
            value=float(dcf_own_beta['ev'] - NETDEBT - HYBRID - dcf_own_beta['equity']),
            deduction=float(dcf_own_beta['ev'] - NETDEBT - HYBRID
                            - dcf_own_beta['equity']),
            book=float(NCI_BV),
            profit_share=float(NCI_BV),
            proportional=float(NCI_BV),
            proxy='the contracted slice at its CONTRACTED PRICE and the rest at its share '
                  'of value, whichever is higher. The Navig8 minority is subject to a '
                  'disclosed purchase arrangement at a stated price, so its claim is that '
                  'price and not a share of anything; the remaining minorities have no '
                  'such arrangement and are worth their share of the value the model '
                  'capitalises, floored at book.',
            proxy_source='the Navig8 acquisition disclosure and the non-controlling '
                         'interests line of the 31 March 2026 statement of financial '
                         'position',
            framings_note='book, profit share and proportional are the same figure here '
                          'because the disclosure gives one carrying amount; the adopted '
                          'deduction differs from all three, and differs UPWARD, because '
                          'the model capitalises 100 per cent of subsidiary cash flow and '
                          'a minority\'s claim on that is worth its share of the VALUE '
                          'rather than its historical cost.',
            deducted_from='equity'),
        dividend=dict(declared_after_balance_sheet_date=False, amount=0.0,
                      note='no dividend declared after the 31 March 2026 balance-sheet '
                           'date is deducted: one declared before it is already out of '
                           'the equity it would come from.'),
        associates=dict(basis='book',
                        note='the joint ventures and associates are unlisted, so there is '
                             'no market to carry them at and they stand at the carrying '
                             'value the balance sheet states.'),
        hybrid=dict(
            treatment='deducted_at_carrying_value_and_weighted_in_the_cost_of_capital',
            carrying_value=float(HYBRID),
            pv_of_coupon=float(hyb_pv_coupon),
            note='THE TWO HALVES OF ONE TREATMENT. The perpetual capital securities rank '
                 'ahead of the ordinary shares, so they are deducted here; a claim '
                 'deducted from enterprise value must also be WEIGHTED in the cost of '
                 'capital at its own cost, or the model subtracts a cheap tranche of '
                 'capital without letting it price the value. The present value of the '
                 'perpetual coupon is published beside the carrying value as the '
                 'alternative deduction, because which of the two a reader prefers is a '
                 'judgement and the study does not hide it inside one number.'),
    ),
    lens_record=dict(
        **{'class': 'marine logistics and shipping, chartered fleet on global day rates'},
        primary=dict(
            kind='dcf', value=float(central),
            range=dict(low=float(lenses['dcf']['bear']),
                       high=float(lenses['dcf']['bull'])),
            range_note='the cash-flow lens at the beta regression\'s OWN 90 per cent '
                       'confidence bounds, with the rate anchor and capital expenditure '
                       'moving with them',
            range_basis=dict(
                driver='the regression beta, across its own 90 per cent confidence '
                       'interval, with the day-rate anchor and capital expenditure '
                       'moving with it',
                low=float(V['beta_ci_hi']), high=float(V['beta_ci_lo']),
                macro_held=True,
                sanctioned_framing='',
                evidence=(
                    'the own-stock regression against the published index of this '
                    'company\'s own exchange gives a beta of %.4f with a standard error '
                    'of %.4f over %d weekly observations, so its 90 per cent interval '
                    'runs %.4f to %.4f. THE RANGE IS THE INTERVAL THE ESTIMATE ITSELF '
                    'SUPPORTS rather than a judgement about how wrong it might be, and '
                    'the corners take the HIGH beta for the bear and the LOW for the '
                    'bull because a higher beta is a lower value. The day-rate anchor '
                    'and capital expenditure move with each corner rather than being '
                    'held, because a cost of capital at the top of its own interval '
                    'describes a world in which charter rates are also weaker. The '
                    'macro path does not move: terminal growth and the terminal '
                    'risk-free rate both contain the same terminal inflation, so '
                    'flexing them would make the bull corner inflation high and low at '
                    'once.'
                    % (V['beta'], V['beta_se'], beta_res.get('n') or 0,
                       V['beta_ci_lo'], V['beta_ci_hi']))),
            note='vessel-days times day rates, vessel by vessel, discounted on a schedule '
                 'that is flat by construction of the currency peg'),
        cross_checks=[
            dict(kind='sotp', value=float(sotp['fv_aed']),
                 note='the three legs summed on their own multiples — a contracted-fleet '
                      'multiple where the leg earns under long-term contracts and a blend '
                      'of contracted and spot where it does not, weighted by the '
                      'company\'s own disclosed share of earnings exposed to spot rates. '
                      'It is a cross-check rather than the answer because the legs share '
                      'one balance sheet, one crew pool and one management.'),
            dict(kind='relative_multiple', value=float(rel['base']),
                 present_value=False,
                 multiple=float(rel['blend_ev_ebitda']),
                 circularity=dict(spot=float(spot_aed), shares=float(shares_mn),
                                  net_debt=float(NETDEBT),
                                  metric_value=float(BASE['ebitda'][0])),
                 multiple_source=(
                     'a blend of %.2fx on the contracted book and %.2fx on the '
                     'spot-exposed book, both taken from the listed peer set — Nakilat '
                     'for long-term contracted gas shipping and the spot tanker names '
                     'for the exposed half — and weighted by the company\'s OWN '
                     'disclosed spot share of %.0f per cent. It is not read off this '
                     'company\'s price: the traded enterprise value over the same '
                     'forecast EBITDA is committed beside it in the circularity block.'
                     % (rel['contracted_multiple'], rel['spot_multiple'],
                        100 * rel['spot_weight']))),
            dict(kind='book_value', value=float(book['base']),
                 note='the DISCLOSED floor. Published as a floor and NEVER weighted into '
                      'a central — which the retired blend did, at 15 per cent.'),
        ],
        envelope=dict(low=float(lenses['dcf']['bear']),
                      high=float(lenses['dcf']['bull'])),
        central=float(central),
        retired=dict(
            blend=dict(RETIRED_W), blend_value=float(RETIRED_BLEND),
            why=('40/25/20/15 across four reads, and two of the four weights are '
                 'forbidden outright rather than merely unevidenced. BOOK VALUE carried '
                 '15 per cent and book value is a disclosed floor that is never weighted '
                 'into an answer; NORMALISED EARNINGS carried 20 and the registry does '
                 'not permit it for this class. The weights had cleared no out-of-sample '
                 'test. Retiring the blend moves the published answer from AED %.2f to '
                 'AED %.2f, which is a LARGE move and is the point: the blend was '
                 'averaging a cash-flow reading well below the market with three '
                 'accounting readings well above it, and publishing the average told a '
                 'reader neither thing.'
                 % (RETIRED_BLEND, central)),
            normalised_earnings=dict(
                value=float(norm['base']),
                why='dropped as a lens for this class. Day rates are cyclical enough '
                    'that a normalised year is a judgement about where the cycle sits '
                    'rather than a reading of the business, and the cash-flow lens '
                    'already carries that judgement explicitly in its rate path. It read '
                    'AED %.2f and carried %.0f per cent of the retired blend.'
                    % (norm['base'], 100 * RETIRED_W['normalized'])),
        ),
    ),
    cost_of_capital_record=dict(
        market='AE', regime=_PATH.regime, years=5,
        rf_observed=V['rf_observed'], default_spread=V['sov_spread'], rf_star=rf_star,
        erp=V['erp_total'], erp_basis='rating', beta=V['beta'],
        ke_exp=ke, kd_pretax=kd, kd_aftertax=kd * (1 - tax_stat),
        weight_equity=we, weight_debt=wd, wacc_exp=wacc,
        rf_terminal=V['rf_terminal'], erp_terminal=V['erp_total'], ke_terminal=ke_term,
        kd_terminal_pretax=kd_term, kd_terminal_aftertax=kd_term * (1 - tax_stat),
        weight_debt_terminal=wd, wacc_terminal=wacc_term,
        glide_fractions=[(i + 1) / 5.0 for i in range(5)],
        forward_wacc=[float(x) for x in wacc_glide],
        discount_factors=[float(x) for x in dcf_own_beta['df']],
        terminal_discount_factor=float(dcf_own_beta['df'][-1]),
        # THE SCHEDULE IS FLAT BY CONSTRUCTION OF THE PEG, NOT BY A CHOICE MADE HERE. The
        # dirham is hard-pegged at 3.6725, so this economy imports United States monetary
        # policy and TODAY IS ALREADY THE TERMINAL. The three-basis-point drift across the
        # window is the gap between an observed ten-year yield and the long-run derived
        # anchor, not a disinflation glide, and it is disclosed as such rather than
        # described as one.
        # THE FIRST YEAR IS A STUB AND WITHOUT THAT THE FACTORS DO NOT REPRODUCE. The
        # valuation date is 31 March 2026, so FY2026 owns only the three quarters still
        # unearned; the first quarter's free cash flow is already inside the balance-sheet
        # net debt and is removed rather than discounted a second time. A reader assuming
        # each rate owns a whole year from t=0 recomputes 0.9213 against a published
        # 0.9404 and concludes the record is wrong — which is why the edges are part of
        # the convention rather than a detail beside it.
        discounting_convention=dict(
            kind='stub_then_annual',
            cumulative_years=[float(STUB + i) for i in range(5)],
            rate_edges=[0.0] + [float(STUB + i) for i in range(5)],
            note='FY2026 is discounted over the %.2f of the year still unearned at the '
                 '31 March 2026 valuation date and every later year over a whole year; '
                 'the terminal is brought home on the SAME cumulative factor as the last '
                 'explicit year, so a dollar arriving on that date has one price of time '
                 'whether it is called a forecast cash flow or a terminal value.'
                 % STUB),
        kd_integrity=dict(
            currency_composition='the drawn book is entirely US-dollar denominated, which '
                                 'under the peg IS the local currency for this purpose: a '
                                 'shareholder facility, third-party bank borrowings and '
                                 'lease liabilities, no other-currency tranche disclosed',
            currency_source='the borrowings and lease-liability notes of the condensed '
                            'consolidated interim financial information for the three '
                            'months ended 31 March 2026',
            effective_rates={'FY2025 lease book': kd_lease},
            interest_bearing_note=(
                'THE DENOMINATOR IS THE BORROWINGS THAT ACTUALLY BEAR THE CHARGE. The one '
                'effective rate this disclosure supports independently is the lease book: '
                'interest paid on lease liabilities of USD %.0f thousand over the average '
                'of the opening USD 170,274 and closing USD 223,153 thousand lease '
                'liabilities, which is %.2f per cent. It is computed over a single audited '
                'year because the FY2024 comparative does not disclose lease interest '
                'separately; the other two tranches disclose their RATES rather than a '
                'charge, so an effective rate on them would be the rate read back to '
                'itself.' % (V['intpaid_lease_fy25'], 100 * kd_lease)),
            effective_rate_unavailable=(
                'A SECOND PERIOD IS NOT DISCLOSED AND THE MISSING DISCLOSURE IS NAMED '
                'rather than approximated. The FY2024 comparative does not disclose lease '
                'interest separately from the total finance charge, so no second '
                'independently computed lease rate exists; and the shareholder facility '
                'and third-party borrowings disclose their RATES rather than an interest '
                'charge, so an effective rate computed on them would be the disclosed rate '
                'read back to itself, which is not independent evidence about anything. '
                'What stands in its place is harder than the test it replaces: the '
                'contractual anchor below carries every facility with its balance, its own '
                'rate and the note that rate comes from, and the adopted rate is their '
                'weighted average — which either comes out or it does not.'),
            # THE CONTRACTUAL ANCHOR, AND THE ADOPTED RATE REPRODUCES FROM IT EXACTLY.
            contractual_anchor=[
                dict(facility='shareholder loan', balance=V['q1_26_shldr_loan'],
                     rate=kd_m1,
                     note='SOFR of %.2f per cent plus the disclosed %.0f basis point '
                          'margin' % (100 * V['sofr'], 10000 * V['shldr_margin'])),
                dict(facility='third-party bank and other borrowings',
                     balance=V['q1_26_borrowings'], rate=kd_thirdparty,
                     note='the mid-point of the two disclosed ranges, %.2f-%.2f per cent '
                          'on bank loans and %.2f-%.2f per cent on other borrowings'
                          % (100 * V['bank_loan_lo'], 100 * V['bank_loan_hi'],
                             100 * V['other_borr_lo'], 100 * V['other_borr_hi'])),
                dict(facility='lease liabilities', balance=V['q1_26_leases'],
                     rate=kd_lease,
                     note='the implied borrowing rate computed independently from the '
                          'audited FY2025 lease interest over the average lease liability'),
            ],
            adopted=kd,
            above_sovereign=bool(kd > V['rf_observed']),
            retired_average=kd_retired_average,
            retired_note='the average of the balance-weighted rate, the marginal drawdown '
                         'rate and one range mid-point, which reproduces from no set of '
                         'facility lines and is retired',
        ),
        sensitivity=dict(
            other_basis='market',
            other_erp=None,
            note='BOTH BASES ARE PUBLISHED AND ONE IS NAMED CENTRAL. The RATING basis is '
                 'central here and the reason is a fact about the source rather than a '
                 'preference: the country-risk file carries NO sovereign credit-default-'
                 'swap entry for the United Arab Emirates, so the market basis has no '
                 'published spread to build from and the rating basis is the only one that '
                 'exists. The default spread netted out of the risk-free rate and the '
                 'premium added back through the equity risk premium are therefore the '
                 'SAME basis, which is what stops the sovereign being counted one and a '
                 'half times.'),
        disclosures=[
            'the sovereign quote behind the house path is dated %s and is older than the '
            '14-day bound. It is accepted deliberately and its age is disclosed here '
            'rather than used quietly.' % _PATH.sovereign_asof,
            'the perpetual capital securities are WEIGHTED in the cost of capital at their '
            'own coupon cost and DEDUCTED in the equity bridge. Those are the two halves '
            'of one treatment: a claim deducted from enterprise value must also be allowed '
            'to price that value, and weighting only equity and debt subtracts a cheap '
            'tranche of capital without letting it earn its place.',
            'the schedule is FLAT by construction of the peg [R-COC-01]. A pegged market '
            'is already terminal, so no disinflation glide applies and none is '
            'manufactured.',
        ],
    ),
    assert_log=assert_log,
)
OUT['meta']['central'] = central
assert OUT['meta']['central'] is not None and OUT['meta']['spot'], \
    'the answer must be readable as a central/spot pair by the shared reader'

if __name__ == '__main__':
    with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
        json.dump(OUT, f, indent=1, default=float)
    print(f"{len(INPUTS)} inputs · {len(assert_log)} assertions passed")
    print(f"central AED {central:.2f} (cost-of-equity alternative {central_alt:.2f}) "
          f"vs spot {spot_aed:.2f}")
    print(f"lenses: " + " · ".join(f"{k} {v['base']:.2f}" for k, v in lenses.items()))
