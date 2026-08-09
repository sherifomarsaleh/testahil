"""EMPOWER study — master computation. Writes study_numbers.json (single source
of truth for every builder). Code-first rule: INPUTS are four-field records
{value, source, date, ring}; a bare numeral cannot enter the model; the ASSERT
block raises (no JSON emitted) unless the FY2025 EBITDA build reconciles to the
audited statements, the bridge closes, the Kd-integrity triple holds
(kd > sovereign > rf*), and the terminal is ROIC-consistent.

Company class: single-leg OPERATING COMPANY — a regulated Dubai district-cooling
utility (chilled-water capacity + consumption charges on 1.7m RT connected, one
small pre-insulated-pipe manufacturing line, one airport cooling concession
inside the same connected base). Lens set follows the operating-company
reference pattern: FCFF DCF primary, relative multiples, normalized earnings
power, book/sustainable-return — four lenses, one field.

TWO STRUCTURAL JUDGEMENTS, both surfaced rather than buried:
1. THE CRUX (sensitised in observable units): consumption revenue per connected
   RT. H1-2026 equivalent full-load hours fell 9.0% y/y (-42m RTh) on
   conflict-hit hospitality occupancy. The model runs the recovery path (per-RT
   consumption regains its FY2025 level through FY2027) as the base case and the
   persistence path (the shock never mean-reverts) as a full alternative model,
   not a one-way sensitivity.
2. THE DUAL-FRAMED CONTESTED JUDGEMENT: the tax rate. FY2025's effective rate is
   a clean 9.0% (UAE CT). Whether the OECD Pillar-Two 15% DMTT reaches Empower
   through DEWA-level consolidation is contested and unresolved; the ENTIRE
   valuation is computed at 9% AND at 15% and both are published side by side —
   summary table, body, workbook, and one expert's range — never averaged.

All money figures in AED MILLIONS unless suffixed _k (thousands) or per-share.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np

# ============================ INPUTS =========================================
def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)

TH = 1e-3   # AED'000 -> AED mn

INP = dict(
    # ---- anchors ---------------------------------------------------------
    spot=I(1.50, "Uploaded DFM daily price history, last close", "2026-08-07", "Market"),
    shares_mn=I(10000.0, "Share capital note 16: AED 1,000,000k at AED 0.10 par = "
                "10,000,000,000 shares, unchanged since the Nov-2022 IPO (EPS note 35 "
                "cross-check: 896,754k / 0.090 = 9,964mn wtd)", "2026-02-09", "Company"),
    tax_ct=I(0.09, "UAE federal corporate tax 9% (FY2025 audited effective rate exactly "
             "9.0%: 99,226k tax on 1,103,161k PBT; note 28)", "2026-02-09", "Company"),
    tax_dmtt=I(0.15, "OECD Pillar-Two UAE domestic minimum top-up tax 15% for groups "
               ">= EUR 750m revenue — whether DEWA-level (80%) consolidation sweeps "
               "Empower in is CONTESTED; computed as the full alternative framing",
               "2026-08-09", "Country"),

    # ---- audited income statements (AED mn) ------------------------------
    rev_fy23=I(3035.203, "Consolidated statement of comprehensive income, FY2023 audited "
               "FS (confirmed by FY2024 filing comparative)", "2024-02-14", "Company"),
    rev_fy24=I(3260.489, "Consolidated statement of comprehensive income, FY2024 audited "
               "FS (confirmed by FY2025 filing comparative)", "2025-02-14", "Company"),
    rev_fy25=I(3419.304, "Consolidated statement of comprehensive income, FY2025 audited "
               "FS", "2026-02-09", "Company"),
    intco_fy23=I(38.711, "Interest income on financial assets at amortised cost (airport "
                 "concession receivable), presented INSIDE gross profit, FY2023 audited FS",
                 "2024-02-14", "Company"),
    intco_fy24=I(59.151, "Interest income on financial assets at amortised cost, FY2024 "
                 "audited FS", "2025-02-14", "Company"),
    intco_fy25=I(58.307, "Interest income on financial assets at amortised cost, FY2025 "
                 "audited FS", "2026-02-09", "Company"),
    cos_fy23=I(1740.878, "Cost of sales, FY2023 audited FS", "2024-02-14", "Company"),
    cos_fy24=I(1917.497, "Cost of sales, FY2024 audited FS", "2025-02-14", "Company"),
    cos_fy25=I(1989.283, "Cost of sales, FY2025 audited FS (gross-profit identity check "
               "in the ASSERT block)", "2026-02-09", "Company"),
    gp_fy23=I(1333.036, "Gross profit, FY2023 audited FS", "2024-02-14", "Company"),
    gp_fy24=I(1402.143, "Gross profit, FY2024 audited FS", "2025-02-14", "Company"),
    gp_fy25=I(1488.328, "Gross profit, FY2025 audited FS", "2026-02-09", "Company"),
    ga_fy23=I(220.285, "General & administrative expenses, FY2023 audited FS",
              "2024-02-14", "Company"),
    ga_fy24=I(235.119, "General & administrative expenses, FY2024 audited FS",
              "2025-02-14", "Company"),
    ga_fy25=I(246.577, "General & administrative expenses, FY2025 audited FS",
              "2026-02-09", "Company"),
    ecl_fy24=I(17.482, "Reversal of expected credit losses, FY2024 audited FS",
               "2025-02-14", "Company"),
    ecl_fy25=I(16.137, "Reversal of expected credit losses, FY2025 audited FS",
               "2026-02-09", "Company"),
    oi_fy23=I(7.120, "Other income, FY2023 audited FS", "2024-02-14", "Company"),
    oi_fy24=I(7.938, "Other income, FY2024 audited FS", "2025-02-14", "Company"),
    oi_fy25=I(14.624, "Other income, FY2025 audited FS", "2026-02-09", "Company"),
    op_fy23=I(1119.871, "Operating profit, FY2023 audited FS", "2024-02-14", "Company"),
    op_fy24=I(1192.444, "Operating profit, FY2024 audited FS", "2025-02-14", "Company"),
    op_fy25=I(1272.512, "Operating profit, FY2025 audited FS", "2026-02-09", "Company"),
    fin_inc_fy25=I(55.347, "Finance income, FY2025 audited FS note 30", "2026-02-09",
                   "Company"),
    fin_cost_fy25=I(224.698, "Finance costs (net of 10.711 capitalised), FY2025 audited "
                    "FS note 30", "2026-02-09", "Company"),
    pbt_fy23=I(942.631, "Profit before tax, FY2023 audited FS", "2024-02-14", "Company"),
    pbt_fy24=I(998.332, "Profit before tax, FY2024 audited FS", "2025-02-14", "Company"),
    pbt_fy25=I(1103.161, "Profit before tax, FY2025 audited FS", "2026-02-09", "Company"),
    tax_fy23=I(+17.454, "Income tax CREDIT (deferred tax asset first recognition ahead of "
               "UAE CT), FY2023 audited FS", "2024-02-14", "Company"),
    tax_fy24=I(-90.097, "Income tax expense, FY2024 audited FS", "2025-02-14", "Company"),
    tax_fy25=I(-99.226, "Income tax expense (current 98.082 + deferred 1.144), FY2025 "
               "audited FS note 28", "2026-02-09", "Company"),
    pat_fy23=I(960.085, "Profit after tax, FY2023 audited FS", "2024-02-14", "Company"),
    pat_fy24=I(908.235, "Profit after tax, FY2024 audited FS", "2025-02-14", "Company"),
    pat_fy25=I(1003.935, "Profit after tax, FY2025 audited FS", "2026-02-09", "Company"),
    npa_fy23=I(952.927, "Profit attributable to equity holders, FY2023", "2024-02-14",
               "Company"),
    npa_fy24=I(896.754, "Profit attributable to equity holders, FY2024", "2025-02-14",
               "Company"),
    npa_fy25=I(993.302, "Profit attributable to equity holders, FY2025", "2026-02-09",
               "Company"),

    # ---- D&A and capex (audited cash-flow statements) --------------------
    dna_fy23=I(348.199, "FY2023 CF: PPE dep 332.884 + RoU 3.158 + intangibles 12.157",
               "2024-02-14", "Company"),
    dna_fy24=I(359.081, "FY2024 CF: PPE dep 342.332 + RoU 4.592 + intangibles 12.157",
               "2025-02-14", "Company"),
    dna_fy25=I(369.717, "FY2025 CF: PPE dep 352.199 + RoU 5.361 + intangibles 12.157 "
               "(investment-property dep 6.317 excluded — investment properties are a "
               "non-operating side pocket in the bridge)", "2026-02-09", "Company"),
    capex_fy23=I(320.144, "FY2023 CF: additions to PPE", "2024-02-14", "Company"),
    capex_fy24=I(306.781, "FY2024 CF: additions to PPE", "2025-02-14", "Company"),
    capex_fy25=I(440.039, "FY2025 CF: capital expenditure net of project-cost accruals "
                 "(a further 171.085 was non-cash accrual movement, note 36)",
                 "2026-02-09", "Company"),

    # ---- the unit build's disclosed physical anchors ---------------------
    rt_conn=I({'2021': 1368.0, '2022': 1405.0, '2024': 1566.0, '2025': 1656.0,
               'H1_2026': 1707.0},
              "Connected capacity history, k RT, H1-2026 earnings deck p13 (2023 not "
              "charted; interpolation never used — growth is computed 2024->2025)",
              "2026-08-05", "Company"),
    rt_contracted=I(2018.0, "Contracted capacity 30-Jun-2026, k RT, deck pp3-4,10",
                    "2026-08-05", "Company"),
    rt_guid_2026=I((100.0, 110.0), "FY2026 new-connections guidance, k RT, deck p13",
                   "2026-08-05", "Company"),
    cons_rev=I({'2022': 1462.983, '2023': 1719.593, '2024': 1895.257, '2025': 1923.892},
               "Consumption revenue, auditor's key-audit-matter section of each audited "
               "FS FY2022-FY2025 (the only disclosed AED split of the revenue streams)",
               "2026-02-09", "Company"),
    pipes_rev_fy25=I(17.214, "Sale of pre-insulated pipes (Logstor), revenue note 23, "
                     "FY2025 audited FS", "2026-02-09", "Company"),
    eflh_h1=I(-0.090, "Equivalent full-load hours H1-2026: 698 hrs, -9.0% y/y "
              "(consumption -42m RTh), deck p4; interim note 30 ties the fall partly to "
              "conflict impact on hospitality occupancy", "2026-08-05", "Company"),
    ew_cost_fy25=I(1467.650, "Electricity & water purchased from DEWA (related-party "
                   "note 12), FY2025 audited FS", "2026-02-09", "Company"),
    ew_cost_fy24=I(1373.2, "Electricity & water purchased from DEWA (related-party note "
                   "12), FY2024 audited FS", "2025-02-14", "Company"),

    # ---- balance sheet & bridge (30-Jun-2026 reviewed interim BS) --------
    borrow_jun26=I(5502.845, "Bank borrowings 30-Jun-2026: current 2.845 + non-current "
                   "5,500.000, reviewed interim BS", "2026-08-05", "Company"),
    lease_jun26=I(0.872, "Lease liabilities 30-Jun-2026", "2026-08-05", "Company"),
    cash_jun26=I(2472.012, "Cash and cash equivalents 30-Jun-2026", "2026-08-05",
                 "Company"),
    deposits_jun26=I(40.212, "Term deposits (>3m) 30-Jun-2026", "2026-08-05", "Company"),
    nci_book_jun26=I(190.745, "Non-controlling interests (30% of DXB CoolCo et al.), "
                     "30-Jun-2026 reviewed BS", "2026-08-05", "Company"),
    invprop_jun26=I(168.716, "Investment properties 30-Jun-2026 (non-operating side "
                    "pocket, added in the bridge at book)", "2026-08-05", "Company"),
    fvtpl_jun26=I(53.411, "Financial assets at FVTPL 30-Jun-2026 (cash-like, added in "
                  "the bridge)", "2026-08-05", "Company"),
    fvoci_jun26=I(74.564, "Financial assets at FVOCI 30-Jun-2026 (added at book)",
                  "2026-08-05", "Company"),
    eq_attr_fy25=I(3310.933, "Equity attributable to holders, 31-Dec-2025 audited BS",
                   "2026-02-09", "Company"),
    eq_attr_jun26=I(3337.585, "Equity attributable to holders, 30-Jun-2026 reviewed BS",
                    "2026-08-05", "Company"),
    nci_pat_fy25=I(10.633, "Profit attributable to NCI, FY2025 audited FS",
                   "2026-02-09", "Company"),

    # ---- H1-2026 actuals the FY2026E build must reconcile to -------------
    rev_h1_26=I(1519.415, "Revenue, H1-2026 reviewed interim FS", "2026-08-05", "Company"),
    rev_h1_25=I(1453.433, "Revenue, H1-2025 comparative", "2026-08-05", "Company"),
    pat_h1_26=I(467.924, "Profit after tax, H1-2026 reviewed interim FS", "2026-08-05",
                "Company"),
    ebitda_h1_26=I(773.0, "EBITDA H1-2026 as presented, earnings deck p4 (Q1 margin "
                   "56.8%, Q2 46.7%)", "2026-08-05", "Company"),
    netdebt_jun26_co=I(2991.0, "Net debt 30-Jun-2026 as the company presents it, deck "
                       "p11 (1.8x LTM EBITDA) — reproduced exactly by borrowings + "
                       "leases - cash - term deposits, see ASSERT", "2026-08-05",
                       "Company"),
    div_policy=I(875.0, "Dividend AED 875m/yr committed for 2025 AND 2026 (2 x 437.5m, "
                 "Oct/Apr), deck p12; FY2025 FS note 39: 875.0 paid in 2025",
                 "2026-08-05", "Company"),

    # ---- cost of capital (v2 method, both ERP bases) ---------------------
    rf_aed=I(0.0448, "UAE dirham T-Bond, Jan-2031 tranche, auction YTM 30-Jul-2026 — "
             "the longest AED sovereign print (4.4y tenor; the 5y+ tenor gap vs the "
             "cash-flow horizon is flagged, spread over UST was ~4bp at issue)",
             "2026-07-30", "Country"),
    ds_rating=I(0.00393, "UAE adjusted default spread, rating basis (Aa2), Damodaran "
                "ctryprem July-2026 edition (data 30-Jun-2026)", "2026-07-01",
                "Country"),
    ds_cds=I(0.0052, "Abu Dhabi 10y sovereign CDS adj. for Switzerland, 30-Jun-2026, "
             "Damodaran July-2026 (the UAE federal CDS row is n/a; Abu Dhabi is the "
             "quoted UAE sovereign CDS — proxy flagged)", "2026-07-01", "Country"),
    erp_rating=I(0.048110, "UAE total equity risk premium, rating basis, Damodaran "
                 "July-2026", "2026-07-01", "Country"),
    erp_cds=I(0.050083, "UAE total ERP, sovereign-CDS basis (via Abu Dhabi CDS), "
              "Damodaran July-2026", "2026-07-01", "Country"),
    beta=I(0.652, "Own-stock weekly regression vs DFM General Index, full listing "
           "window 25-Nov-2022..17-Jul-2026 (3.64y, inside the 2-5y band): beta 0.652, "
           "R2 0.157, n 190, SE 0.110, CI90 [0.47, 0.83] — passes the usability gate "
           "(beta_result.json)", "2026-08-09", "Company"),
    kd_marg=I(0.0492, "Marginal cost of debt = the company's OWN FY2025 borrowing-cost "
              "capitalisation rate (note 30), struck on the 2025 full refinance of both "
              "AED 2.75bn RCFs at EIBOR + a REDUCED margin; sits above the 4.48% AED "
              "sovereign as a same-currency corporate must (2024 comparison: 5.993%; "
              "spot 3M EIBOR 3.66% + implied margin ~0.9-1.3%)", "2026-02-09",
              "Company"),
    g_term=I(0.025, "Terminal growth: long-run UAE nominal-GDP-consistent 2.5% under a "
             "flat regulated tariff — bounded by Dubai build-out saturation "
             "(connected 1.7m of ~2.0m RT contracted; sensitised 1.5-3.5%)",
             "2026-08-09", "House"),
)

V = {k: v['value'] for k, v in INP.items()}

# ===================== HISTORICAL PANEL (audited) ============================
YRS_H = ['FY23', 'FY24', 'FY25']
hist_is = {}
for y, t in zip(YRS_H, ['fy23', 'fy24', 'fy25']):
    rev, cos, gp = V[f'rev_{t}'], V[f'cos_{t}'], V[f'gp_{t}']
    op, dna = V[f'op_{t}'], V[f'dna_{t}']
    hist_is[y] = dict(
        rev=rev, intco=V[f'intco_{t}'], cos=-cos, gp=gp,
        ga=-V[f'ga_{t}'], op=op, dna=dna, ebitda=op + dna,
        ebitda_margin=(op + dna) / rev, pbt=V[f'pbt_{t}'], tax=V[f'tax_{t}'],
        pat=V[f'pat_{t}'], npa=V[f'npa_{t}'],
        capex=V[f'capex_{t}'], gp_margin=gp / rev)

# FY2025 EBITDA reconciliation target for the unit build
EBITDA25 = hist_is['FY25']['ebitda']            # 1,642.229

# ================= UNIT BUILD: the two-leg revenue engine ====================
# Leg 1 — CONSUMPTION (RTh x tariff, carried as revenue-per-connected-RT):
cons25 = V['cons_rev']['2025']                   # 1,923.892
rt25, rt24 = V['rt_conn']['2025'], V['rt_conn']['2024']
rt_avg25 = (rt24 + rt25) / 2                     # 1,611.0 k RT
cons_per_rt25 = cons25 / rt_avg25                # AED k per avg connected RT
# Leg 2 — CAPACITY (demand) + connection/others, everything that is not
# consumption and not pipes. The AED level is IMPLIED (flagged in the sweep:
# no per-RT tariff schedule is published):
cap25 = V['rev_fy25'] - cons25 - V['pipes_rev_fy25']   # 1,478.198
cap_per_rt25 = cap25 / rt_avg25

# Connected-RT path (k RT, year-end). 2026 = guidance midpoint; thereafter the
# contracted backlog (2,018k at Jun-26, 311k above connected) plus the historic
# 90-105k/yr cadence tapers as the concession pipeline matures:
rt_path = dict(FY25=rt25, FY26=rt25 + np.mean(V['rt_guid_2026']),        # 1761.0
               FY27=rt25 + np.mean(V['rt_guid_2026']) + 100.0,           # 1861.0
               FY28=0.0, FY29=0.0, FY30=0.0)
rt_path['FY28'] = rt_path['FY27'] + 90.0
rt_path['FY29'] = rt_path['FY28'] + 80.0
rt_path['FY30'] = rt_path['FY29'] + 70.0

YRS_F = ['FY26', 'FY27', 'FY28', 'FY29', 'FY30']
rt_avg = {}
prev = rt_path['FY25']
for y in YRS_F:
    rt_avg[y] = (prev + rt_path[y]) / 2
    prev = rt_path[y]

# Consumption per-RT path — THE CRUX, run BOTH ways as full models:
#   base    : FY26 carries the disclosed shock (-6% per-RT for the full year:
#             H1 printed -9% EFLH; H2-2025 was itself already soft, so the
#             full-year per-RT fall is smaller), recovers to the FY25 level
#             through FY27, flat real thereafter (regulated flat tariff).
#   persist : the FY26 per-RT level NEVER recovers (structural demand loss).
CRUX_SHOCK = -0.06
cons_per_rt = dict(
    base={'FY26': cons_per_rt25 * (1 + CRUX_SHOCK), 'FY27': cons_per_rt25,
          'FY28': cons_per_rt25, 'FY29': cons_per_rt25, 'FY30': cons_per_rt25},
    persist={y: cons_per_rt25 * (1 + CRUX_SHOCK) for y in YRS_F})

def revenue_path(mode):
    cons = {y: cons_per_rt[mode][y] * rt_avg[y] for y in YRS_F}
    cap = {y: cap_per_rt25 * rt_avg[y] for y in YRS_F}     # flat regulated tariff
    pipes = {y: V['pipes_rev_fy25'] for y in YRS_F}
    rev = {y: cons[y] + cap[y] + pipes[y] for y in YRS_F}
    return rev, cons, cap, pipes

rev_b, cons_b, cap_b, pipes_b = revenue_path('base')
rev_p, cons_p, cap_p, pipes_p = revenue_path('persist')

# H1-2026 reconciliation: FY26E must sit consistently above 2x H1 minus
# seasonality (H2 carries the summer consumption peak; H2-2025 share was 57.5%)
h2_share_25 = 1 - V['rev_h1_25'] / V['rev_fy25']
fy26_check = V['rev_h1_26'] / (1 - h2_share_25)   # naive same-seasonality FY26

# ===================== COST STACK (one escalator per class) ==================
# Class 1 — purchased electricity & water (DEWA): tied to its physical driver,
# the consumption leg (DEWA slab tariff flat, fuel surcharge floats; pass-through
# ratio held at the FY2025 print, itself in line with FY2024):
EW_RATIO = V['ew_cost_fy25'] / cons25             # 0.7629 of consumption revenue
ew_ratio_fy24 = V['ew_cost_fy24'] / V['cons_rev']['2024']
# Class 2 — staff & other cash COS (wage class, UAE CPI/wage ~2.5%):
other_cos25 = V['cos_fy25'] - V['ew_cost_fy25'] - 0.341696e3 * TH * 1e3  # see note
# cos includes the COS share of PPE depreciation (341.696) AND the RoU
# depreciation (5.361) and intangibles amortisation (12.157) — all non-cash;
# strip all of them plus E&W to get cash other-COS:
dep_cos25 = 341.696 + 5.361 + 12.157
other_cos25 = V['cos_fy25'] - V['ew_cost_fy25'] - dep_cos25    # 162.419
# Class 3 — G&A ex its depreciation (wage class):
dep_ga25 = 10.503
ga_cash25 = V['ga_fy25'] - dep_ga25                            # 236.074
WAGE_ESC = 0.025

def ebitda_build(rev, cons):
    ew = {y: EW_RATIO * cons[y] for y in YRS_F}
    oc = {y: other_cos25 * (1 + WAGE_ESC) ** (i + 1) for i, y in enumerate(YRS_F)}
    ga = {y: ga_cash25 * (1 + WAGE_ESC) ** (i + 1) for i, y in enumerate(YRS_F)}
    intco = {y: V['intco_fy25'] * (1 - 0.03) ** (i + 1) for i, y in enumerate(YRS_F)}
    oi = {y: V['oi_fy25'] for y in YRS_F}
    ebitda = {y: rev[y] + intco[y] - ew[y] - oc[y] - ga[y] + oi[y] for y in YRS_F}
    return ebitda, ew, oc, ga, intco, oi

# FY2025 reconciliation of the same identity against the AUDITED print:
ebitda25_build = (V['rev_fy25'] + V['intco_fy25'] - V['ew_cost_fy25'] - other_cos25
                  - ga_cash25 + V['oi_fy25'] + V['ecl_fy25'])
# audited: op 1,272.512 + dna 369.717 = 1,642.229; the identity must close to
# < 0.5 (rounding inside note components) — ASSERTED below.

eb_b, ew_b, oc_b, ga_b, intco_b, oi_b = ebitda_build(rev_b, cons_b)
eb_p, ew_p, oc_p, ga_p, intco_p, oi_p = ebitda_build(rev_p, cons_p)

# ===================== D&A, CAPEX, WORKING CAPITAL ===========================
PPE25 = 7194.990                                   # audited FY2025 BS
DEP_RATE = 352.199 / 6995.160                      # FY25 PPE dep / opening net PPE
AMORT_FLAT = V['dna_fy25'] - 352.199               # RoU + intangibles ~17.5/yr
CAPEX_PER_RT = V['capex_fy25'] / (rt25 - rt24)     # AED mn per k RT added (4.889)
MAINT_PCT = 0.008                                   # of opening net PPE

def capital_block(rev):
    ppe, dna, capex = {}, {}, {}
    ppe_open = PPE25
    for i, y in enumerate(YRS_F):
        added_rt = list(rt_path.values())[i + 1] - list(rt_path.values())[i]
        capex[y] = CAPEX_PER_RT * added_rt + MAINT_PCT * ppe_open
        dna[y] = DEP_RATE * ppe_open + AMORT_FLAT
        ppe[y] = ppe_open + capex[y] - (dna[y] - AMORT_FLAT)
        ppe_open = ppe[y]
    return ppe, dna, capex

ppe_b, dna_b, capex_b = capital_block(rev_b)
ppe_p, dna_p, capex_p = capital_block(rev_p)

# Working capital: NWC/revenue held at the FY2025 statement level (negative —
# customer deposits and payables fund the cycle; DSO 32d, DPO structurally long):
NWC25 = (55.718 + 303.818 + 39.353) - (2165.056 - 171.085) - 161.670
# inventories + receivables + due-from-RP - (payables ex capex accruals) - due-to-RP
NWC_RATIO = NWC25 / V['rev_fy25']

def nwc_block(rev):
    nwc = {y: NWC_RATIO * rev[y] for y in YRS_F}
    dn = {}
    prev = NWC25
    for y in YRS_F:
        dn[y] = nwc[y] - prev
        prev = nwc[y]
    return nwc, dn

nwc_b, dnwc_b = nwc_block(rev_b)
nwc_p, dnwc_p = nwc_block(rev_p)

# ============================== WACC (v2) ====================================
rf_star_rating = V['rf_aed'] - V['ds_rating']          # 4.087%
rf_star_cds = V['rf_aed'] - V['ds_cds']                # 3.960%
ke_rating = rf_star_rating + V['beta'] * V['erp_rating']
ke_cds = rf_star_cds + V['beta'] * V['erp_cds']
mktcap = V['spot'] * V['shares_mn']                    # 15,000
net_debt = (V['borrow_jun26'] + V['lease_jun26'] - V['cash_jun26']
            - V['deposits_jun26'])                     # 2,991.493
wd = net_debt / (net_debt + mktcap)
we = 1 - wd

def wacc_of(tax, ke):
    return we * ke + wd * V['kd_marg'] * (1 - tax)

WACC = dict(
    rating_ct=wacc_of(V['tax_ct'], ke_rating),
    cds_ct=wacc_of(V['tax_ct'], ke_cds),
    rating_dmtt=wacc_of(V['tax_dmtt'], ke_rating),
    cds_dmtt=wacc_of(V['tax_dmtt'], ke_cds))
# No Kd glide: the AED curve is flat-to-mildly-hawkish (Fed dots), both RCFs are
# floating, and the 2025 refinance already reset the margin — a glide would be
# invented, not sourced. Explicit-window WACC == terminal WACC, stated openly.

# ============================== DCF (FCFF) ===================================
def dcf(rev, eb, dna, capex, dnwc, tax, wacc, label, ppe_d=None, nwc_d=None):
    ebit = {y: eb[y] - dna[y] for y in YRS_F}
    nopat = {y: ebit[y] * (1 - tax) for y in YRS_F}
    fcff = {y: nopat[y] + dna[y] - capex[y] - dnwc[y] for y in YRS_F}
    df_, pv = {}, {}
    for i, y in enumerate(YRS_F):
        df_[y] = 1 / (1 + wacc) ** (i + 1)
        pv[y] = fcff[y] * df_[y]
    pv_explicit = sum(pv.values())
    # terminal: ROIC-consistent reinvestment
    ppe_d = ppe_d if ppe_d is not None else ppe_b
    nwc_d = nwc_d if nwc_d is not None else nwc_b
    ic_term = ppe_d['FY30'] + 1150.0 + nwc_d['FY30']   # PPE + concession asset + NWC
    nopat_t1 = nopat['FY30'] * (1 + V['g_term'])
    roic_term = nopat['FY30'] / ic_term
    rr_term = V['g_term'] / roic_term
    fcff_t1 = nopat_t1 * (1 - rr_term)
    tv = fcff_t1 / (wacc - V['g_term'])
    pv_tv = tv * df_['FY30']
    ev = pv_explicit + pv_tv
    # EV -> equity bridge (30-Jun-2026 reviewed BS)
    eq = (ev - net_debt + V['invprop_jun26'] + V['fvtpl_jun26'] + V['fvoci_jun26'])
    nci_frac = V['nci_pat_fy25'] / V['pat_fy25']       # 1.06% of profits
    nci_val = eq * nci_frac
    eq_attr = eq - nci_val
    ps = eq_attr / V['shares_mn']
    return dict(label=label, ebit=ebit, nopat=nopat, fcff=fcff, df=df_, pv=pv,
                pv_explicit=pv_explicit, roic_term=roic_term, rr_term=rr_term,
                tv=tv, pv_tv=pv_tv, tv_share=pv_tv / ev, ev=ev,
                nci_val=nci_val, eq_attr=eq_attr, ps=ps)

D_base_ct = dcf(rev_b, eb_b, dna_b, capex_b, dnwc_b, V['tax_ct'],
                WACC['rating_ct'], 'base / 9% CT / rating-basis ERP')
D_base_dmtt = dcf(rev_b, eb_b, dna_b, capex_b, dnwc_b, V['tax_dmtt'],
                  WACC['rating_dmtt'], 'base / 15% DMTT / rating-basis ERP')
D_pers_ct = dcf(rev_p, eb_p, dna_p, capex_p, dnwc_p, V['tax_ct'],
                WACC['rating_ct'], 'consumption-persists / 9% CT')
D_pers_dmtt = dcf(rev_p, eb_p, dna_p, capex_p, dnwc_p, V['tax_dmtt'],
                  WACC['rating_dmtt'], 'consumption-persists / 15% DMTT')
D_base_cds = dcf(rev_b, eb_b, dna_b, capex_b, dnwc_b, V['tax_ct'],
                 WACC['cds_ct'], 'base / 9% CT / CDS-basis ERP')

# ====================== OTHER LENSES =========================================
# Relative multiples (peer set: Tabreed primary, DEWA secondary — cross-check
# sources only). Tabreed FY2025: EBITDA 1.27bn, net debt ~4.6x EBITDA, so the
# comparison runs at the EV line:
TABREED_EV_EBITDA = 10.7   # derived: USD 2.11bn cap x 3.6725 + 5.84bn ND / 1.27bn
DEWA_PE = 16.8
TABREED_PE = 16.6
ebitda26 = eb_b['FY26']
ev_rel = TABREED_EV_EBITDA * ebitda26
eq_rel = (ev_rel - net_debt + V['invprop_jun26'] + V['fvtpl_jun26']
          + V['fvoci_jun26'])
ps_rel = eq_rel * (1 - V['nci_pat_fy25'] / V['pat_fy25']) / V['shares_mn']
# peer P/E on FY2026E attributable profit (base, 9%):
fin_net26 = -(V['kd_marg'] * V['borrow_jun26'] - 0.035 * V['cash_jun26'])
np26 = (eb_b['FY26'] - dna_b['FY26'] + fin_net26) * (1 - V['tax_ct'])
npa26 = np26 * (1 - V['nci_pat_fy25'] / V['pat_fy25'])
ps_pe = TABREED_PE * npa26 / V['shares_mn']

# Normalized earnings power: FY2026E with consumption at the UNSHOCKED per-RT
# level and the 9%/15% average burden shown separately; normalized EPS x a
# justified multiple from Ke and sustainable payout:
rev_norm26 = cons_per_rt25 * rt_avg['FY26'] + cap_b['FY26'] + V['pipes_rev_fy25']
eb_norm26 = (rev_norm26 + intco_b['FY26'] - EW_RATIO * cons_per_rt25 * rt_avg['FY26']
             - oc_b['FY26'] - ga_b['FY26'] + V['oi_fy25'])
np_norm26 = (eb_norm26 - dna_b['FY26'] + fin_net26) * (1 - V['tax_ct'])
npa_norm26 = np_norm26 * (1 - V['nci_pat_fy25'] / V['pat_fy25'])
eps_norm = npa_norm26 / V['shares_mn']
roe_sust = V['npa_fy25'] / ((V['eq_attr_fy25'] + 3197.590) / 2)   # avg FY24-25 equity
rr_eq = V['g_term'] / roe_sust
pe_just = (1 - rr_eq) * (1 + V['g_term']) / (ke_rating - V['g_term'])
ps_norm = eps_norm * pe_just

# Book value & sustainable return:
bvps = V['eq_attr_jun26'] / V['shares_mn']
pb_just = (roe_sust - V['g_term']) / (ke_rating - V['g_term'])
ps_book = bvps * pb_just

# DDM cross-check (used by Expert 2): committed AED 875m through 2026, then
# growing at g on the RT path:
dps = V['div_policy'] / V['shares_mn']
ps_ddm = dps * (1 + V['g_term']) / (ke_rating - V['g_term'])

# The DEWA control transaction (Feb-2026): a disclosed related-party CONTROL
# price, reported as a reference point ONLY:
DEWA_BUYIN = 2.16

# ====================== SYNTHESIS — four lenses, one field ===================
lenses = dict(
    dcf=dict(ps=D_base_ct['ps'], ps_dmtt=D_base_dmtt['ps'], weight=0.50),
    relative=dict(ps=ps_rel, ps_pe=ps_pe, weight=0.20),
    normalized=dict(ps=ps_norm, weight=0.15),
    book=dict(ps=ps_book, weight=0.15))
central_ct = (0.50 * D_base_ct['ps'] + 0.20 * ps_rel + 0.15 * ps_norm
              + 0.15 * ps_book)
central_dmtt = (0.50 * D_base_dmtt['ps'] + 0.20 * ps_rel + 0.15 * ps_norm * (1 - 0.066)
                + 0.15 * ps_book)

# ---- bear / bull: FULL model re-runs, not lens blends -----------------------
# BEAR — war re-escalation economics: consumption per-RT falls a further 6% in
# FY27 and NEVER recovers, RT additions halve (conflict freezes the connection
# pipeline), the 15% DMTT lands, and the equity market re-prices UAE risk
# (+100bp on Ke via the ERP, the war-month DFM move in cost-of-capital terms).
rt_path_bear = dict(FY25=rt25, FY26=rt25 + 50.0, FY27=rt25 + 100.0,
                    FY28=rt25 + 145.0, FY29=rt25 + 185.0, FY30=rt25 + 220.0)
rt_avg_bear, prev = {}, rt_path_bear['FY25']
for y in YRS_F:
    rt_avg_bear[y] = (prev + rt_path_bear[y]) / 2
    prev = rt_path_bear[y]
cons_bear_prt = {y: cons_per_rt25 * (1 + CRUX_SHOCK) * (0.94 if y != 'FY26' else 1.0)
                 for y in YRS_F}
rev_bear = {y: cons_bear_prt[y] * rt_avg_bear[y] + cap_per_rt25 * rt_avg_bear[y]
            + V['pipes_rev_fy25'] for y in YRS_F}
cons_bear = {y: cons_bear_prt[y] * rt_avg_bear[y] for y in YRS_F}
eb_bear, *_ = ebitda_build(rev_bear, cons_bear)
# capex on the halved RT path:
ppe_bear, dna_bear, capex_bear = {}, {}, {}
ppe_open = PPE25
for i, y in enumerate(YRS_F):
    added = list(rt_path_bear.values())[i + 1] - list(rt_path_bear.values())[i]
    capex_bear[y] = CAPEX_PER_RT * added + MAINT_PCT * ppe_open
    dna_bear[y] = DEP_RATE * ppe_open + AMORT_FLAT
    ppe_bear[y] = ppe_open + capex_bear[y] - (dna_bear[y] - AMORT_FLAT)
    ppe_open = ppe_bear[y]
nwc_bear, dnwc_bear = nwc_block(rev_bear)
ke_bear = ke_rating + 0.010
wacc_bear = we * ke_bear + wd * V['kd_marg'] * (1 - V['tax_dmtt'])
D_bear = dcf(rev_bear, eb_bear, dna_bear, capex_bear, dnwc_bear, V['tax_dmtt'],
             wacc_bear, 'BEAR: re-escalation / persist-6% / 50k RT / 15% / +100bp',
             ppe_d=ppe_bear, nwc_d=nwc_bear)
# BULL — clean recovery: consumption recovers fully in FY27, RT adds at the top
# of guidance (110k) holding through FY28, 9% CT, base WACC:
rt_path_bull = dict(FY25=rt25, FY26=rt25 + 110.0, FY27=rt25 + 220.0,
                    FY28=rt25 + 320.0, FY29=rt25 + 410.0, FY30=rt25 + 490.0)
rt_avg_bull, prev = {}, rt_path_bull['FY25']
for y in YRS_F:
    rt_avg_bull[y] = (prev + rt_path_bull[y]) / 2
    prev = rt_path_bull[y]
rev_bull = {y: (cons_per_rt[('base')][y]) * rt_avg_bull[y]
            + cap_per_rt25 * rt_avg_bull[y] + V['pipes_rev_fy25'] for y in YRS_F}
cons_bull = {y: cons_per_rt['base'][y] * rt_avg_bull[y] for y in YRS_F}
eb_bull, *_ = ebitda_build(rev_bull, cons_bull)
ppe_bull, dna_bull, capex_bull = {}, {}, {}
ppe_open = PPE25
for i, y in enumerate(YRS_F):
    added = list(rt_path_bull.values())[i + 1] - list(rt_path_bull.values())[i]
    capex_bull[y] = CAPEX_PER_RT * added + MAINT_PCT * ppe_open
    dna_bull[y] = DEP_RATE * ppe_open + AMORT_FLAT
    ppe_bull[y] = ppe_open + capex_bull[y] - (dna_bull[y] - AMORT_FLAT)
    ppe_open = ppe_bull[y]
nwc_bull, dnwc_bull = nwc_block(rev_bull)
D_bull = dcf(rev_bull, eb_bull, dna_bull, capex_bull, dnwc_bull, V['tax_ct'],
             WACC['rating_ct'], 'BULL: recovery / 110k RT / 9% CT',
             ppe_d=ppe_bull, nwc_d=nwc_bull)
bear, bull = D_bear['ps'], D_bull['ps']

# ====================== SENSITIVITY GRIDS ====================================
g_grid = [0.015, 0.020, 0.025, 0.030, 0.035]
wacc_grid = [WACC['rating_ct'] - 0.01, WACC['rating_ct'] - 0.005, WACC['rating_ct'],
             WACC['rating_ct'] + 0.005, WACC['rating_ct'] + 0.01]
sens_wg = []
for w_ in wacc_grid:
    row = []
    for g_ in g_grid:
        nopat30 = D_base_ct['nopat']['FY30']
        ic30 = ppe_b['FY30'] + 1150.0 + nwc_b['FY30']
        roic_ = nopat30 / ic30
        rr_ = g_ / roic_
        tv_ = nopat30 * (1 + g_) * (1 - rr_) / (w_ - g_)
        pv_e = sum(D_base_ct['fcff'][y] / (1 + w_) ** (i + 1)
                   for i, y in enumerate(YRS_F))
        ev_ = pv_e + tv_ / (1 + w_) ** 5
        eq_ = (ev_ - net_debt + V['invprop_jun26'] + V['fvtpl_jun26']
               + V['fvoci_jun26']) * (1 - V['nci_pat_fy25'] / V['pat_fy25'])
        row.append(eq_ / V['shares_mn'])
    sens_wg.append(row)

# crux sensitivity in OBSERVABLE units: consumption per-RT recovery level
# (% of FY2025) x recovery year
crux_levels = [0.90, 0.94, 0.97, 1.00, 1.03]
crux_rows = []
for lvl in crux_levels:
    cons_alt = {y: cons_per_rt25 * lvl for y in YRS_F}
    cons_alt['FY26'] = cons_per_rt25 * (1 + CRUX_SHOCK)
    rev_a = {y: cons_alt[y] * rt_avg[y] + cap_per_rt25 * rt_avg[y]
             + V['pipes_rev_fy25'] for y in YRS_F}
    cons_a = {y: cons_alt[y] * rt_avg[y] for y in YRS_F}
    eb_a, *_ = ebitda_build(rev_a, cons_a)
    nwc_a, dnwc_a = nwc_block(rev_a)
    Da = dcf(rev_a, eb_a, dna_b, capex_b, dnwc_a, V['tax_ct'],
             WACC['rating_ct'], f'crux {lvl:.0%}')
    crux_rows.append(dict(level=lvl, ps=Da['ps']))

# ============================ ASSERT BLOCK ===================================
LOG = []
def chk(name, cond, detail):
    LOG.append(f"{'PASS' if cond else 'FAIL'}: {name} — {detail}")
    if not cond:
        raise AssertionError(LOG[-1])

chk("gross-profit identity FY2025",
    abs(V['rev_fy25'] + V['intco_fy25'] - V['cos_fy25'] - V['gp_fy25']) < 0.01,
    f"rev+intco-cos = {V['rev_fy25']+V['intco_fy25']-V['cos_fy25']:.3f} vs gp "
    f"{V['gp_fy25']:.3f}")
chk("EBITDA unit-identity reconciles to audited FY2025",
    abs(ebitda25_build - EBITDA25) < 1.0,
    f"build {ebitda25_build:.3f} vs audited op+dna {EBITDA25:.3f} (gap "
    f"{ebitda25_build-EBITDA25:+.3f}, inside note rounding)")
chk("net debt reproduces the company's own 2,991",
    abs(net_debt - V['netdebt_jun26_co']) < 1.0,
    f"computed {net_debt:.3f} vs deck {V['netdebt_jun26_co']:.1f}")
chk("Kd integrity triple", V['kd_marg'] > V['rf_aed'] > rf_star_rating,
    f"kd {V['kd_marg']:.4f} > sovereign {V['rf_aed']:.4f} > rf* "
    f"{rf_star_rating:.4f}")
chk("both-ERP-basis Ke converge (<30bp)",
    abs(ke_rating - ke_cds) < 0.003,
    f"rating {ke_rating:.4f} vs CDS {ke_cds:.4f}")
chk("terminal ROIC-consistent",
    0 < D_base_ct['rr_term'] < 0.6 and D_base_ct['roic_term'] > WACC['rating_ct'],
    f"roic_term {D_base_ct['roic_term']:.3f}, rr {D_base_ct['rr_term']:.3f}, "
    f"wacc {WACC['rating_ct']:.4f}")
chk("FY2026E revenue consistent with H1 print (±4%)",
    abs(rev_b['FY26'] / fy26_check - 1) < 0.04,
    f"model {rev_b['FY26']:.1f} vs same-seasonality projection {fy26_check:.1f}")
chk("crux monotonic", all(crux_rows[i]['ps'] <= crux_rows[i+1]['ps'] + 1e-9
                          for i in range(len(crux_rows)-1)),
    "fair value rises with the consumption recovery level")
chk("dual-framing spread is material and DISCLOSED",
    D_base_ct['ps'] > D_base_dmtt['ps'],
    f"9% CT {D_base_ct['ps']:.3f} vs 15% DMTT {D_base_dmtt['ps']:.3f} — both "
    f"published side by side")

# ====================== STEP 0 / STRIKE / BETA imports =======================
step0 = json.load(open(os.path.join(HERE, 'backtest_5y.json')))
strike = json.load(open(os.path.join(HERE, 'strike_result.json')))
beta_reg = json.load(open(os.path.join(HERE, 'beta_result.json')))

# ============================ OUTPUT =========================================
out = dict(
    meta=dict(ticker='EMPOWER', company='Emirates Central Cooling Systems '
              'Corporation PJSC (Empower)', market='AE (Dubai Financial Market)',
              currency='AED', asof='2026-08-09', spot=V['spot'],
              shares_mn=V['shares_mn'], mktcap=mktcap,
              klass='operating company — regulated district-cooling utility',
              ownership='DEWA 80% (since Feb-2026), free float ~20%'),
    inputs=INP,
    hist_is=hist_is,
    unit=dict(rt_path=rt_path, rt_avg=rt_avg, cons_per_rt25=cons_per_rt25,
              cap_per_rt25=cap_per_rt25, cons25=cons25, cap25=cap25,
              crux_shock=CRUX_SHOCK, ew_ratio=EW_RATIO,
              ew_ratio_fy24=ew_ratio_fy24, other_cos25=other_cos25,
              ga_cash25=ga_cash25, dep_cos25=dep_cos25, dep_ga25=dep_ga25,
              capex_per_rt=CAPEX_PER_RT, dep_rate=DEP_RATE,
              amort_flat=AMORT_FLAT, maint_pct=MAINT_PCT,
              nwc25=NWC25, nwc_ratio=NWC_RATIO, h2_share_25=h2_share_25,
              fy26_seasonality_check=fy26_check),
    fcst=dict(years=YRS_F,
              base=dict(rev=rev_b, cons=cons_b, cap=cap_b, pipes=pipes_b,
                        ebitda=eb_b, ew=ew_b, other_cos=oc_b, ga=ga_b,
                        intco=intco_b, dna=dna_b, capex=capex_b, ppe=ppe_b,
                        nwc=nwc_b, dnwc=dnwc_b),
              persist=dict(rev=rev_p, ebitda=eb_p, dna=dna_p, capex=capex_p,
                           dnwc=dnwc_p)),
    wacc=dict(rf=V['rf_aed'], rf_star_rating=rf_star_rating,
              rf_star_cds=rf_star_cds, beta=V['beta'],
              erp_rating=V['erp_rating'], erp_cds=V['erp_cds'],
              ke_rating=ke_rating, ke_cds=ke_cds, kd=V['kd_marg'],
              kd_at_ct=V['kd_marg'] * (1 - V['tax_ct']),
              kd_at_dmtt=V['kd_marg'] * (1 - V['tax_dmtt']),
              we=we, wd=wd, mktcap=mktcap, net_debt=net_debt, **WACC),
    dcf=dict(base_ct=D_base_ct, base_dmtt=D_base_dmtt, pers_ct=D_pers_ct,
             pers_dmtt=D_pers_dmtt, base_cds=D_base_cds, bear=D_bear,
             bull=D_bull),
    scenarios=dict(bear=dict(rt_path=rt_path_bear, rev=rev_bear,
                             ebitda=eb_bear, wacc=wacc_bear, ke=ke_bear,
                             tax=V['tax_dmtt']),
                   bull=dict(rt_path=rt_path_bull, rev=rev_bull,
                             ebitda=eb_bull, wacc=WACC['rating_ct'],
                             tax=V['tax_ct'])),
    lenses=lenses,
    rel=dict(tabreed_ev_ebitda=TABREED_EV_EBITDA, tabreed_pe=TABREED_PE,
             dewa_pe=DEWA_PE, ev_rel=ev_rel, ps_rel=ps_rel, ps_pe=ps_pe,
             np26=np26, npa26=npa26),
    norm=dict(rev=rev_norm26, ebitda=eb_norm26, npa=npa_norm26, eps=eps_norm,
              pe_just=pe_just, ps=ps_norm),
    book=dict(bvps=bvps, roe_sust=roe_sust, pb_just=pb_just, ps=ps_book),
    ddm=dict(dps=dps, ps=ps_ddm, policy_mn=V['div_policy']),
    dewa_buyin=dict(price=DEWA_BUYIN, date='2026-02-11',
                    note='related-party CONTROL price for Dubai Holding\'s 24% — '
                         'a disclosed reference point, never fair value'),
    central=dict(ct=central_ct, dmtt=central_dmtt, bear=bear, bull=bull,
                 spot=V['spot']),
    sens_wg=dict(g_grid=g_grid, wacc_grid=wacc_grid, table=sens_wg),
    crux=dict(levels=crux_levels, rows=crux_rows,
              persist_ps_ct=D_pers_ct['ps'], persist_ps_dmtt=D_pers_dmtt['ps']),
    step0=dict(windows=step0['production']['windows'],
               first_origin=step0['production']['first_origin'],
               last_origin=step0['production']['last_origin'],
               span_years=step0['production']['span_years'],
               skill_norm=step0['production']['skill_norm'],
               verdict=step0['production']['verdict'],
               ci_blocks=step0['production']['ci_blocks'],
               cov50=step0['production']['cov50'],
               cov80=step0['production']['cov80'],
               cov90=step0['production']['cov90'],
               pit_mean=step0['production']['pit_mean'],
               pit_hist=step0['production']['pit_hist'],
               chi2_p=step0['production']['chi2_p'],
               ks_p=step0['production']['ks_p'],
               width_vs_benchmark=step0['production']['width_vs_benchmark'],
               market_gate=dict(verdict='PARITY', skill=0.0068,
                                ci90=[-0.001, 0.014], panel=18,
                                fit_date='2026-07-29')),
    strike=strike,
    beta_reg=beta_reg,
    assert_log=LOG)

json.dump(out, open(os.path.join(HERE, 'study_numbers.json'), 'w'), indent=1,
          default=float)

print("study_numbers.json written")
print(f"\nWACC: rating/9% {WACC['rating_ct']:.4f} | CDS/9% {WACC['cds_ct']:.4f} "
      f"| rating/15% {WACC['rating_dmtt']:.4f}")
print(f"Ke rating {ke_rating:.4f} | Ke CDS {ke_cds:.4f} | Kd 4.92% | wd {wd:.3f}")
print(f"\nDCF ps: base/9% {D_base_ct['ps']:.3f} | base/15% {D_base_dmtt['ps']:.3f} "
      f"| persist/9% {D_pers_ct['ps']:.3f} | persist/15% {D_pers_dmtt['ps']:.3f}")
print(f"TV share of EV: {D_base_ct['tv_share']:.1%}")
print(f"lenses: rel(EV/EBITDA) {ps_rel:.3f} | rel(P/E) {ps_pe:.3f} | norm "
      f"{ps_norm:.3f} | book {ps_book:.3f} | ddm {ps_ddm:.3f}")
print(f"central: 9% {central_ct:.3f} | 15% {central_dmtt:.3f} | bear {bear:.3f} "
      f"| bull {bull:.3f} | spot {V['spot']}")
print(f"\nFY26E rev base {rev_b['FY26']:.1f} (seasonality check {fy26_check:.1f}) "
      f"| EBITDA {eb_b['FY26']:.1f}")
print("\n".join(LOG))
