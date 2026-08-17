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
IN('beta', 1.085, "Weekly regression of the stock's own returns on the FTSE ADX General "
   "Index — the published index of the exchange the share is listed on — over the full "
   "listed history to the index's last available session", '2026-07-24', 'Market')
IN('beta_se', 0.199, "Standard error of the same regression", '2026-07-24', 'Market')
IN('beta_r2', 0.158, "R-squared of the same regression", '2026-07-24', 'Market')
IN('beta_dimson', 1.164, "Lead-lag sum beta from the same series, one lead and two lags — "
   "the correction for co-movement a share books late because it does not trade every "
   "session", '2026-07-24', 'Market')
IN('beta_composite', 0.705, "The same regression run against an equal-weight composite of "
   "the exchange's own listed names instead of the published index. Reported because the "
   "gap between the two is large and is a property of index construction, not of the "
   "company: the published index is weighted by size and is dominated by the same "
   "large-capitalisation group the subject belongs to", '2026-08-07', 'Market')
IN('beta_ci_lo', 0.758, "Lower bound of the 90% confidence interval on the regressed beta",
   '2026-07-24', 'Market')
IN('beta_ci_hi', 1.412, "Upper bound of the 90% confidence interval on the regressed beta",
   '2026-07-24', 'Market')
IN('g_terminal', 0.02, FS25 + " — the company's own value-in-use test projects cash flows "
   "beyond its plan at a growth rate equal to an estimated 2% inflation rate; adopted here "
   "as the terminal growth rate", '2025-12-31', 'Company')
IN('rf_terminal', 0.0325, "Long-run nominal anchor for a dollar-pegged economy: a 2% "
   "inflation objective plus a 1.25% long-run real policy rate, the same construction the "
   "terminal growth rate rests on", '2026-08-07', 'Global')

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
# --- tankers: vessel by vessel, at the rate each one actually earns -------------
# The fleet splits in two. Forty-five vessels trade at spot rates and carry the whole of
# the rate risk; eight sit on charters out at rates already fixed and disclosed. They are
# modelled separately, because averaging them would hide exactly the exposure that matters.
CLASSES = ['hs', 'mr', 'lr1', 'lr2', 'vlcc']
FLEET = {c: V[f'tnk_{c}_n'] for c in CLASSES}
SPOT_N = {c: V[f'tnk_{c}_spot'] for c in CLASSES}
FIXED_N = {c: FLEET[c] - SPOT_N[c] for c in CLASSES}
TC_OUT = {'hs': 0.0, 'mr': 0.0, 'lr1': V['tc_out_lr1'], 'lr2': V['tc_out_lr2'],
          'vlcc': V['tc_out_vlcc']}
TCE25 = {c: sum(TCE_FY25[c]) / 4 for c in TCE_FY25}
TCE24 = {c: sum(TCE_FY24[c]) / 4 for c in TCE_FY24}
TCE24['mr'] = TCE25['mr']          # 2024 quarterly rates for this class are not disclosed
TCE25['hs'] = TCE25['mr']          # the smallest tankers are not broken out; the medium-
TCE24['hs'] = TCE24['mr']          # range rate is used for them and the gap is flagged
TCE_EXIT = {c: TCE_FY25[c][3] for c in TCE_FY25}
TCE_EXIT['hs'] = TCE_EXIT['mr']
TCE_MID = {c: (TCE24[c] + TCE25[c]) / 2 for c in CLASSES}       # mid-cycle anchor
Q1_26 = {c: V[f'tce_{c}_q1_26'] for c in ('mr', 'lr1', 'lr2', 'vlcc')}
Q2_26 = {c: V[f'tce_{c}_q2_26'] for c in ('mr', 'lr1', 'lr2', 'vlcc')}
Q1_26['hs'] = Q1_26['mr']; Q2_26['hs'] = Q2_26['mr']

vessel_days_25 = sum(FLEET.values()) * 365
tce_rev_25 = sum(FLEET[c] * TCE25[c] for c in FLEET) * 365 / 1000.0
opex_day_25 = (tce_rev_25 - V['seg_ebitda_tankers_fy25']) * 1000.0 / vessel_days_25
IN('tnk_opex_day', round(opex_day_25, 0), "Implied all-in running cost per vessel per day, "
   "solved so that the owned-fleet time-charter equivalent less running cost reproduces the "
   "reported Tankers earnings before interest, tax, depreciation and amortisation for 2025",
   '2025-12-31', 'Company')
gross_up_25 = V['seg_rev_tankers_fy25'] / tce_rev_25
IN('tnk_grossup_25', round(gross_up_25, 3), "Ratio of reported Tankers revenue to "
   "owned-fleet time-charter-equivalent revenue in 2025 — the voyage-cost and low-margin "
   "relet and third-party trading content of gross revenue", '2025-12-31', 'Company')
gross_up_26 = 1.60
IN('tnk_grossup_26', gross_up_26, "The same ratio for 2026 onward. Reported first-quarter "
   "revenue was flat year on year while the rate earned per vessel more than doubled, "
   "because low-margin relet and third-party trading fell away; the ratio is set well below "
   "the 2025 level to reflect that and is a presentational driver only — it moves revenue, "
   "never earnings", '2026-03-31', 'Company')

OPEX_ESC = IN('opex_escalation', 0.02, "Running-cost escalation applied to crew, technical "
              "management, insurance and repairs — a domestic services and wage escalator, "
              "not a commodity index, because these are the physical drivers of the line",
              '2026-08-09', 'Industry')
H2_26_REVERSION = IN('h2_2026_reversion', 0.50, "Weight placed on the 2025 average rate, "
                     "against the rate achieved in the first quarter of 2026, in setting "
                     "the second half of 2026. A half-and-half blend is a deliberate step "
                     "down from a first half running far above it", '2026-08-09', 'Industry')


def spot_path(mode):
    """Spot time-charter equivalent per class, FY2026-FY2030.

    2026 is built from what the fleet actually earned in the first quarter, the level the
    second quarter was crossing at, and a second half stepped back toward the 2025 average.
    From 2027 the path glides to a mid-cycle anchor — the average of the 2024 and 2025
    outcomes — which is where the whole valuation question sits.
    """
    out = {}
    for c in CLASSES:
        h2 = Q1_26[c] * (1 - H2_26_REVERSION) + TCE25[c] * H2_26_REVERSION
        y26 = (Q1_26[c] + Q2_26[c] + 2 * h2) / 4.0
        end = TCE_MID[c] * (1.0 if mode == 'reversion' else 1.30)
        out[c] = [y26] + [y26 + (end - y26) * i / 4.0 for i in range(1, 5)]
    return out


def tanker_leg(mode):
    tce = spot_path(mode)
    rev, ebitda = [], []
    for i in range(5):
        spot_rev = sum(SPOT_N[c] * tce[c][i] for c in CLASSES) * 365 / 1000.0
        # charters out roll off during 2027; from 2028 the whole fleet is at spot
        roll = [1.0, 0.5, 0.0, 0.0, 0.0][i]
        fixed_rev = sum(FIXED_N[c] * (TC_OUT[c] * roll + tce[c][i] * (1 - roll))
                        for c in CLASSES) * 365 / 1000.0
        tce_rev = spot_rev + fixed_rev
        opex = vessel_days_25 * opex_day_25 * (1 + OPEX_ESC) ** (i + 1) / 1000.0
        rev.append(tce_rev * gross_up_26)
        ebitda.append(tce_rev - opex)
    return rev, ebitda, tce


# --- gas carriers: contracted vessel-years x implied day rate ------------------
GAS_VY = [10.75, 13.0, 21.25, 25.0, 25.0]
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
    gas_rev = [GAS_VY[i] * 365 * gas_rate_25 * (1 + OPEX_ESC) ** (i + 1) / 1000.0
               for i in range(5)]
    gas_ebitda = [r * GAS_MARGIN for r in gas_rev]
    seg = {'Tankers': dict(rev=tnk_rev, ebitda=tnk_ebitda),
           'Gas Carriers': dict(rev=gas_rev, ebitda=gas_ebitda)}
    for s_, d in DRV.items():
        seg[s_] = dict(rev=list(d['rev']),
                       ebitda=[r * m for r, m in zip(d['rev'], d['mar'])])
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
OTHER_DNA25 = IN('other_dna_run_rate',
                 (V['q1_26_dep_rou'] + V['q1_26_dep_ip'] + V['q1_26_amort']) * 4,
                 Q126 + " — depreciation on right-of-use assets and investment properties "
                 "plus amortisation of intangibles in the first quarter, annualised",
                 '2026-03-31', 'Company')
opcost_25 = V['rev_fy25'] - ebitda_op[2]
DSO = ccc['dso'][2]
DIO_OP = V['inv_fy25'] / opcost_25 * 365
DPO_OP = (V['pay_fy25'] + V['dtr_c_fy25']) / opcost_25 * 365
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
    ppe_open, ppe, dep_ppe, dna = V['ppe_fy25'], [], [], []
    for i in range(5):
        d = DEP_RATE * (ppe_open + (ppe_open + CAPEX[i]) ) / 2.0
        # solve the roll consistently: depreciation on the average of opening and closing
        d = DEP_RATE * (ppe_open + max(ppe_open + CAPEX[i] - d, 0)) / 2.0
        close = ppe_open + CAPEX[i] - d
        dep_ppe.append(d); ppe.append(close)
        dna.append(d + OTHER_DNA25 * (1 + OPEX_ESC) ** (i + 1))
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
ke_dimson = rf_star + V['beta_dimson'] * V['erp_total']
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
kd = (kd_m1 + kd_m2 + kd_m3) / 3
we = mktcap / (mktcap + debt_now)
wd = 1 - we
tax_stat = V['tax_stat']
wacc = we * ke + wd * kd * (1 - tax_stat)
# terminal: the same construction on a long-run risk-free anchor
ke_term = V['rf_terminal'] + V['beta'] * V['erp_total']
kd_term = V['rf_terminal'] + (kd - rf_star)
wacc_term = we * ke_term + wd * kd_term * (1 - tax_stat)
wacc_glide = [wacc + (wacc_term - wacc) * (i + 1) / 5.0 for i in range(5)]

wacc_blk = dict(
    rf_observed=V['rf_observed'], sov_spread=V['sov_spread'], rf_star=rf_star,
    beta=V['beta'], beta_se=V['beta_se'], beta_r2=V['beta_r2'], beta_dimson=V['beta_dimson'],
    erp=V['erp_total'], crp=V['crp'], erp_mature=V['erp_mature'],
    ke=ke, ke_dimson=ke_dimson, ke_beta1=ke_beta1,
    kd_method1=kd_m1, kd_method2=kd_m2, kd_method3=kd_m3, kd=kd,
    kd_bank_mid=kd_bank_mid, kd_other_mid=kd_other_mid, kd_thirdparty=kd_thirdparty,
    kd_lease=kd_lease, kd_after_tax=kd * (1 - tax_stat),
    tax_stat=tax_stat, we=we, wd=wd, wacc=wacc,
    rf_terminal=V['rf_terminal'], ke_term=ke_term, kd_term=kd_term, wacc_term=wacc_term,
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
NETDEBT = NETDEBT_CO + DEFERRED
HYBRID = V['q1_26_hybrid']
NCI_BV = V['q1_26_nci']
JV_BV = 493120
IN('jv_bv_q126', JV_BV, Q126 + " — investment in joint ventures and associates",
   '2026-03-31', 'Company')
STUB = 0.75      # the valuation date is 31 March 2026; three quarters of 2026 remain
Q1_FCF = IN('q1_26_fcf', 130000, MDAQ126 + " — free cash flow of USD 130 million in the "
            "first quarter of 2026, already reflected in net debt at the valuation date",
            '2026-03-31', 'Company')


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
    pv_tv = tv * df[4]
    ev_ops = pv_expl + pv_tv
    ev = ev_ops + JV_BV
    nd = NETDEBT + (HYBRID if hybrid_as_debt else 0.0)
    eq = ev - nd - NCI_BV
    fv_usd = eq / shares_mn / 1000.0      # equity is USD thousand, shares are millions
    return dict(wacc=w, wacc_term=wt, g=g, glide=glide, df=df, fcff=fcff, pv=pv,
                pv_explicit=pv_expl, roic_terminal=roic_t, reinvest=reinv,
                nopat_t1=nopat_t1, tv=tv, pv_tv=pv_tv, tv_share=pv_tv / ev_ops,
                ev_ops=ev_ops, jv=JV_BV, ev=ev, net_debt=nd, deferred=DEFERRED,
                hybrid=HYBRID if hybrid_as_debt else 0.0, nci=NCI_BV,
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
    eps = [n / shares_mn / 1000.0 for n in npa]
    return dict(net_debt=nd, gross_debt=gross, interest=interest, fin_income=fin_inc,
                pbt=pbt, tax=tax, pat=pat, nci=nci, npa=npa, eps=eps, dps=DPS_USD,
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

BASE = project('reversion')
GUID = project('sustained')
FINB = finance_roll(BASE)
FING = finance_roll(GUID)
BSB = forecast_bs(BASE, FINB)


def equity_from_ev(ev, hybrid_as_debt=True):
    return ev + JV_BV - NETDEBT - (HYBRID if hybrid_as_debt else 0.0) - NCI_BV


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
pb_fair = (roe_sust - g_b) / (ke - g_b)
bvps_now = (V['q1_26_eqp']) / shares_mn / 1000.0
book = dict(roe_sustainable=roe_sust, ke=ke, g=g_b, pb_fair=pb_fair,
            vessel_sale_price=V['vessel_sale_price'], vessel_sale_book=V['vessel_sale_book'],
            vessel_value_to_book=V['vessel_sale_price'] / V['vessel_sale_book'],
            bvps_usd=bvps_now, bvps_aed=bvps_now * peg,
            base=pb_fair * bvps_now * peg,
            ke_bear=ke_ci_hi, ke_bull=ke_ci_lo,
            bear=((roe_sust * 0.85) - g_b) / (ke_ci_hi - g_b) * bvps_now * peg,
            bull=((roe_sust * 1.15) - g_b) / (ke_ci_lo - g_b) * bvps_now * peg)

# --- discounted cash flow, with scenarios --------------------------------------
BASE_MID = dict(TCE_MID)


def dcf_scenario(beta_s, anchor_mult, capex_mult=1.0, hybrid_as_debt=False):
    global TCE_MID, CAPEX
    old_mid, old_capex = dict(TCE_MID), list(CAPEX)
    TCE_MID.update({c: BASE_MID[c] * anchor_mult for c in BASE_MID})
    CAPEX[:] = [c * capex_mult for c in old_capex]
    kes = rf_star + beta_s * V['erp_total']
    ket = V['rf_terminal'] + beta_s * V['erp_total']
    w = we * kes + wd * kd * (1 - tax_stat)
    wt = we * ket + wd * kd_term * (1 - tax_stat)
    p = project('reversion')
    d = dcf(p, hybrid_as_debt=hybrid_as_debt, wacc_ov=w, term_wacc_ov=wt)
    TCE_MID.update(old_mid); CAPEX[:] = old_capex
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

LENS_W = {'dcf': 0.40, 'relative': 0.25, 'normalized': 0.20, 'book': 0.15}
for _k, _w in LENS_W.items():
    IN(f'lens_weight_{_k}', _w, "Study judgement on how much weight each lens carries — "
       "see the judgements table", '2026-08-09', 'Industry')

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
for _lab, _dcfkey in (('central', 'dcf'), ('central_beta_alt', 'dcf_beta_alt')):
    lenses[_lab] = dict(
        bear=sum(LENS_W[k] * lenses[_dcfkey if k == 'dcf' else k]['bear'] for k in LENS_W),
        base=sum(LENS_W[k] * lenses[_dcfkey if k == 'dcf' else k]['base'] for k in LENS_W),
        bull=sum(LENS_W[k] * lenses[_dcfkey if k == 'dcf' else k]['bull'] for k in LENS_W))
central = lenses['central']['base']
central_alt = lenses['central_beta_alt']['base']

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
BETAS = [0.705, 0.90, 1.085, 1.25, 1.412]   # composite · mid · adopted · mid · CI top
GS = [0.010, 0.015, 0.020, 0.025]
sens_beta_g = [[dcf_scenario(b, 1.0, 1.0, True)['fv_aed'] if g == V['g_terminal'] else None
                for g in GS] for b in BETAS]
sens = dict(betas=BETAS, gs=GS)
grid = []
for b in BETAS:
    row = []
    kes = rf_star + b * V['erp_total']; ket = V['rf_terminal'] + b * V['erp_total']
    w = we * kes + wd * kd * (1 - tax_stat); wt = we * ket + wd * kd_term * (1 - tax_stat)
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
A('the terminal value share is computed, not asserted',
  0.0 < dcf_own_beta['tv_share'] < 1.0)
A('the calibration evidence is the committed market fit',
  step0['nu'] == bt5['fit']['nu'] and step0['width_cal'] == bt5['fit']['width_cal'])
A('the five-year scoring beats the benchmark', bt5['five_year']['skill_norm'] > 0)
A('the price map was struck on the same close as the study',
  abs(strike['spot'] - spot_aed) < 1e-9)
A('the technical read was computed on the same close', abs(tech['close'] - spot_aed) < 1e-9)
A('the beta used is the one the regression produced',
  abs(V['beta'] - round(beta_res['adopted']['beta_used'], 3)) < 1e-9)
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
              shares_mn=shares_mn, shares_wavg_mn=shares_wavg_mn,
              mktcap_usd000=mktcap, ev_usd000=mktcap + NETDEBT,
              klass='asset-heavy marine logistics and shipping operating company',
              sector='Marine transportation and energy logistics'),
    inputs=INPUTS,
    hist_is=hist_is, hist_bs=hist_bs, hist_cf=hist_cf, ccc=ccc,
    seg_hist=seg_hist, grp_hist=grp_hist, segs=SEGS, seg_group=SEG_GROUP,
    groups=GROUPS,
    product_lines=PRODUCT_LINES, cost_lines=COST_LINES,
    fleet=dict(owned=FLEET, spot=SPOT_N, fixed=FIXED_N, tc_out=TC_OUT,
               tce_fy24=TCE24, tce_fy25=TCE25, tce_exit=TCE_EXIT, tce_mid=BASE_MID,
               q1_26=Q1_26, q2_26=Q2_26, opex_day=opex_day_25,
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
    lenses=lenses, lens_weights=LENS_W, central=central, central_beta_alt=central_alt,
    beta_framing=dict(
        primary=dict(beta=V['beta'], label='the published index of its own exchange',
                     ke=ke, wacc=wacc_blk['wacc'], fv=dcf_own_beta['fv_aed'],
                     central=central),
        alternative=dict(beta=V['beta_composite'],
                         label="an equal-weight composite of the same exchange's names",
                         ke=ke_beta1, fv=dcf_beta_alt['fv_aed'], central=central_alt),
        ci90=[V['beta_ci_lo'], V['beta_ci_hi']],
        dimson=V['beta_dimson'],
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
    assert_log=assert_log,
)
if __name__ == '__main__':
    with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
        json.dump(OUT, f, indent=1, default=float)
    print(f"{len(INPUTS)} inputs · {len(assert_log)} assertions passed")
    print(f"central AED {central:.2f} (cost-of-equity alternative {central_alt:.2f}) "
          f"vs spot {spot_aed:.2f}")
    print(f"lenses: " + " · ".join(f"{k} {v['base']:.2f}" for k, v in lenses.items()))
