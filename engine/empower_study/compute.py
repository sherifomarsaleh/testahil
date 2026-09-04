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
FS25 = ("Audited consolidated financial statements for the year ended 31 December 2025, "
        "signed 9 February 2026, obtained from the company's own investor-relations page")

INP = dict(
    # ---- anchors ---------------------------------------------------------
    spot=I(1.57, "DFM close for EMPOWER, 3 September 2026, from the price file the "
           "principal supplied that day and committed to the repository. THE STUDY IS "
           "RE-STRUCK ON IT because no study is delivered against a stale price: the "
           "prior edition stood on the 7-August close of 1.50, and the stock has since "
           "risen 4.7%", "2026-09-03", "Market"),
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
    ga_fy25=I(256.383, "General & administrative expenses, FY2025 audited FS statement "
              "face (OCR, verified against the operating-profit identity to the dirham; "
              "CORRECTED 17-Aug-2026 — a first-pass extraction carried 246.577, which also "
              "closed the identity because 9.806 had been shifted between G&A and other "
              "income)", "2026-02-09", "Company"),
    ecl_fy24=I(17.482, "Reversal of expected credit losses, FY2024 audited FS",
               "2025-02-14", "Company"),
    ecl_fy25=I(16.137, "Reversal of expected credit losses, FY2025 audited FS",
               "2026-02-09", "Company"),
    oi_fy23=I(7.120, "Other income, FY2023 audited FS", "2024-02-14", "Company"),
    oi_fy24=I(7.938, "Other income, FY2024 audited FS", "2025-02-14", "Company"),
    oi_fy25=I(24.430, "Other income, FY2025 audited FS statement face; note 29 "
              "composition: rental income 18.094 + government grant 2.780 + scrap 1.482 + "
              "others 2.074 (CORRECTED 17-Aug-2026 from a first-pass 14.624)",
              "2026-02-09", "Company"),
    rental_fy25=I(18.094, "Rental income inside other income, FY2025 note 29 — the return "
                  "on the investment properties the bridge adds at book, so it is EXCLUDED "
                  "from operating EBITDA (double-count fix, critique CCU6 confirmed against "
                  "the note)", "2026-02-09", "Company"),
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
    nci_book_jun26=I(190.745, "Non-controlling interests (15% of DXB CoolCo et al. — "
                     "the H1-2026 subsidiary note shows Dxb CoolCo FZCO at 85%/85%), "
                     "30-Jun-2026 reviewed BS", "2026-08-05", "Company"),
    recv_jun26=I(1294.442, "Financial assets at amortised cost, 30-Jun-2026 reviewed BS: "
                 "non-current 1,273.130 + current 21.312. Note 8 composition: AED 1,005.030 "
                 "from Dubai Aviation City Corporation (DXB CoolCo acquisition, 2023) + AED "
                 "289.412 from Nakheel PJSC (Empower Snow acquisition, 2021) — related-party "
                 "acquisition receivables under common control, NOT an operating concession "
                 "asset. Clean financial-asset treatment adopted per critique (17-Aug-2026): "
                 "interest income excluded from operating EBITDA/FCFF, asset added at book "
                 "in the EV-to-equity bridge, and excluded from terminal invested capital",
                 "2026-08-05", "Company"),
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
    beta=I(0.863, "Own-stock weekly regression vs the FTSE ADX General Index — the "
           "UAE base market index PER EXPLICIT INSTRUCTION 10-Aug-2026, replacing the "
           "listing exchange's own DFM General Index (that regression, beta 0.652, is "
           "retained in beta_result_dfmgi.json as a comparison). User-supplied FADGI "
           "history 2011-2026; regression window 25-Nov-2022..24-Jul-2026 (3.66y, "
           "clipped at the index file's endpoint two weeks before the anchor): beta "
           "0.863, R2 0.103, n 189, SE 0.186, CI90 [0.56, 1.17] — passes the "
           "usability gate (beta_result.json)", "2026-08-10", "Company"),
    kd_marg=I(0.0492, "Marginal cost of debt = the company's OWN FY2025 borrowing-cost "
              "capitalisation rate (note 30), struck on the 2025 full refinance of both "
              "AED 2.75bn RCFs at EIBOR + a REDUCED margin; sits above the 4.48% AED "
              "sovereign as a same-currency corporate must (2024 comparison: 5.993%; "
              "spot 3M EIBOR 3.66% + implied margin ~0.9-1.3%)", "2026-02-09",
              "Company"),
    g1_real=I(0.0049019607843137254,
              "Stage-one REAL growth, and it is the RESIDUE of a volume assumption rather "
              "than a rate anybody set: this company's tariff is REGULATED AND NOT "
              "INDEXED, so nominal revenue growth IS volume growth. The previous edition "
              "typed 2.5% nominal as the Dubai build-out rate (connected 1.7m of ~2.0m RT "
              "contracted), and on the house terminal inflation of 2.0% that is +0.49% "
              "real. STORING IT THIS WAY MOVES NO NUMBER HERE, which is the point worth "
              "recording: on a frozen-tariff business a typed nominal rate carries a "
              "meaning it does not carry elsewhere, and the storage rule makes that "
              "visible instead of leaving a reader to compute it",
              "2026-08-09", "House"),
    g2_real=I(-0.004901960784313725,
              "Stage-two REAL growth, and it is NEGATIVE — written down as the real number "
              "it is rather than left inside a nominal 1.5%. The previous edition set "
              "stage two at 1.5% nominal for 'long-run densification with about zero real "
              "tariff growth', and against 2.0% inflation that is a real DECLINE of 0.49% "
              "a year for ever. Under a tariff the regulator does not index, a business "
              "whose volume grows more slowly than prices shrinks in real terms by "
              "construction, and this rate says so",
              "2026-08-09", "House"),
    asset_life_years=I((10929327.0 - 432364.0 - 495858.0 + 22649.0 + 12157.0 * 30.0)
                       / (352199.0 + 5361.0 + 12157.0),
                       FS25 + ", notes 5, 6 and 7, DERIVED BY IDENTITY from those notes' "
                       "own cost and charge columns and LABELLED as derived, and READ BY "
                       "OCR OFF THE RENDERED PIXELS because the filing carries no usable "
                       "text layer (85 bytes across 85 pages) and its property note is "
                       "printed landscape, so the page was rotated before it could be "
                       "read. ARITHMETIC IS THE ARBITER AND THE EXTRACTION FOOTS FOUR "
                       "WAYS: the cost columns sum to the printed total of 10,929,327; the "
                       "accumulated-depreciation columns to 3,734,337; cost less "
                       "accumulated reproduces the balance sheet's 7,194,990; and the "
                       "year's charge of 352,199 splits to the 341,696 in cost of sales "
                       "and 10,503 in general and administrative expenses the notes state "
                       "separately. Property, plant and equipment 10,001,105 (total less "
                       "land, which is never depreciated, and less capital work in "
                       "progress, whose accumulated column is impairment rather than "
                       "depreciation) over 352,199 gives 28.40 years; right-of-use 22,649 "
                       "over 5,361 gives 4.22; intangibles are DISCLOSED at 30 years "
                       "outright and their gross cost follows from the flat charge. "
                       "Blended, 28.10 years, cross-checked at 27.88 on FY2024's own "
                       "columns. The right-of-use figure does NOT match the 15-year "
                       "equipment lease the note names, and the note explains why rather "
                       "than contradicting it: the book is 19,997 of buildings against "
                       "2,652 of equipment, and the buildings are a head office and "
                       "labour accommodation on ONE-YEAR terms",
                       "2026-02-09", "Company"),
    accum_dep_fy25=I((3734337.0 - 18013.0 + 20771.0) / 1000.0,
                     FS25 + ", notes 5 and 6: accumulated depreciation at 31-Dec-2025 "
                     "across the depreciable classes, less the capital-work-in-progress "
                     "column which is impairment rather than depreciation. AED mn",
                     "2026-02-09", "Company"),
    dep_charge_fy25=I((352199.0 + 5361.0 + 12157.0) / 1000.0,
                      FS25 + ", notes 5, 6 and 7: the year's own depreciation and "
                      "amortisation charge on those classes. AED mn",
                      "2026-02-09", "Company"),
)

V = {k: v['value'] for k, v in INP.items()}

# ---- the house macro path supplies the inflation; this study may not carry one --
import macro_path as MP                                                    # noqa: E402
# aliased TERMVAL, not TV: 'tv' here is the terminal VALUE
import terminal_value as TERMVAL                                           # noqa: E402
_AE = MP.load('AE')
PI_TERM = (_AE.raw['inflation']['terminal'] or {})['value']
V['g_term'] = (1.0 + PI_TERM) * (1.0 + V['g1_real']) - 1.0
V['g_term2'] = (1.0 + PI_TERM) * (1.0 + V['g2_real']) - 1.0
INP['g_term_derived'] = I(V['g_term'], "DERIVED, never typed: (1 + terminal inflation "
                          "%.4f from the house UAE macro path) x (1 + stage-one real "
                          "growth %.4f) - 1. It reproduces the previous edition's typed "
                          "2.50%% to the basis point, because under a tariff the regulator "
                          "does not index a nominal rate IS a volume assumption."
                          % (PI_TERM, V['g1_real']), _AE.as_of, "House")
INP['g_term2_derived'] = I(V['g_term2'], "DERIVED: the same identity on the stage-two real "
                           "rate, reproducing the previous edition's typed 1.50%%. A real "
                           "DECLINE, stated as one.", _AE.as_of, "House")

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
ga_cash25 = V['ga_fy25'] - dep_ga25                            # 245.880
OI_OP = V['oi_fy25'] - V['rental_fy25']                        # 6.336 grant+scrap+others
WAGE_ESC = 0.025

def ebitda_build(rev, cons):
    # OPERATING EBITDA — concession/receivable interest EXCLUDED (clean
    # financial-asset treatment, adopted 17-Aug-2026 per critique): the interest
    # belongs to the related-party acquisition receivables, which are valued at
    # book in the bridge instead.
    ew = {y: EW_RATIO * cons[y] for y in YRS_F}
    oc = {y: other_cos25 * (1 + WAGE_ESC) ** (i + 1) for i, y in enumerate(YRS_F)}
    ga = {y: ga_cash25 * (1 + WAGE_ESC) ** (i + 1) for i, y in enumerate(YRS_F)}
    intco = {y: V['intco_fy25'] * (1 - 0.03) ** (i + 1) for i, y in enumerate(YRS_F)}
    oi = {y: OI_OP for y in YRS_F}
    ebitda = {y: rev[y] - ew[y] - oc[y] - ga[y] + oi[y] for y in YRS_F}
    return ebitda, ew, oc, ga, intco, oi

# FY2025 reconciliation against the AUDITED print: the audited op+D&A includes
# the receivable interest inside gross profit; the OPERATING build excludes it,
# so the identity is build_ex + interest == audited:
ebitda25_ex = (V['rev_fy25'] - V['ew_cost_fy25'] - other_cos25
               - ga_cash25 + OI_OP + V['ecl_fy25'])
ebitda25_build = ebitda25_ex + V['intco_fy25'] + V['rental_fy25']
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

def wacc_of(tax_shield, ke):
    return we * ke + wd * V['kd_marg'] * (1 - tax_shield)

# The Pillar-Two top-up is a minimum-ETR charge on profits, not a higher
# statutory rate on the taxable base — it does not enlarge the value of
# interest deductibility. The 15% framing therefore keeps the 9% debt shield
# (critique finding, accepted 17-Aug-2026): both framings discount at the
# same WACC and differ only in NOPAT.
WACC = dict(
    rating_ct=wacc_of(V['tax_ct'], ke_rating),
    cds_ct=wacc_of(V['tax_ct'], ke_cds),
    rating_dmtt=wacc_of(V['tax_ct'], ke_rating),
    cds_dmtt=wacc_of(V['tax_ct'], ke_cds))

# THREE WACC CONSTRUCTIONS, all priced (adopted 17-Aug-2026 — the construction
# was previously a single unpriced choice):
#   base    — target-structure NET debt weights (company policy ~2x EBITDA,
#             payout ~= FCFE so surplus cash is transient), Kd = facility rate;
#   gross   — gross-debt weights, cash at par in the bridge (the standard
#             textbook frame);
#   carry   — net weights with the cost of NET debt blended for the negative
#             carry on the cash pile (gross Kd on borrowings less the deposit
#             yield on cash).
gross_debt = V['borrow_jun26'] + V['lease_jun26']
wd_gross = gross_debt / (gross_debt + mktcap)
WACC_GROSS = (1 - wd_gross) * ke_rating + wd_gross * V['kd_marg'] * (1 - V['tax_ct'])
cash_all = V['cash_jun26'] + V['deposits_jun26']
kd_net_carry = (gross_debt * V['kd_marg'] * (1 - V['tax_ct'])
                - cash_all * 0.035 * (1 - V['tax_ct'])) / net_debt
WACC_CARRY = we * ke_rating + wd * kd_net_carry
ke_dfm = rf_star_rating + 0.652 * V['erp_rating']
WACC_DFM_BETA = we * ke_dfm + wd * V['kd_marg'] * (1 - V['tax_ct'])
# No Kd glide: the AED curve is flat-to-mildly-hawkish (Fed dots), both RCFs are
# floating, and the 2025 refinance already reset the margin — a glide would be
# invented, not sourced. Explicit-window WACC == terminal WACC, stated openly.

# ============================== DCF (FCFF) ===================================
def dcf(rev, eb, dna, capex, dnwc, tax, wacc, label, ppe_d=None, nwc_d=None):
    # VALUATION CLOCK (fixed 17-Aug-2026 per critique): the bridge is struck on
    # the 30-Jun-2026 reviewed balance sheet, so the cash-flow clock starts
    # there too — FY2026 contributes its SECOND HALF only (half-year stub at
    # t=0.5) and later year-ends sit at 1.5..4.5 years. The previous full-year-
    # at-t=1 convention double-counted H1-2026 cash already inside the June net
    # debt.
    ebit = {y: eb[y] - dna[y] for y in YRS_F}
    nopat = {y: ebit[y] * (1 - tax) for y in YRS_F}
    fcff = {y: nopat[y] + dna[y] - capex[y] - dnwc[y] for y in YRS_F}
    flow = dict(fcff); flow['FY26'] = fcff['FY26'] * 0.5
    df_, pv = {}, {}
    for i, y in enumerate(YRS_F):
        t = i + 0.5
        df_[y] = 1 / (1 + wacc) ** t
        pv[y] = flow[y] * df_[y]
    pv_explicit = sum(pv.values())
    # terminal: ROIC-consistent reinvestment. Invested capital = plant + net
    # working capital ONLY — the related-party receivables are valued at book
    # in the bridge and their interest is outside operating NOPAT, so they no
    # longer sit in operating capital.
    ppe_d = ppe_d if ppe_d is not None else ppe_b
    nwc_d = nwc_d if nwc_d is not None else nwc_b
    ic_term = ppe_d['FY30'] + nwc_d['FY30']
    roic_term = nopat['FY30'] / ic_term
    # TWO-STAGE TERMINAL (adopted 17-Aug-2026 per critique: a fade, not a flat
    # perpetuity): stage 1, FY31-FY40, grows at g1 = 2.5%/yr — the Dubai 2040
    # build-out window, volume-only under the RD10 no-indexation tariff regime;
    # stage 2 perpetuity at g2 = 1.5% (long-run densification with ~zero real
    # tariff growth). Reinvestment is ROIC-consistent in each stage.
    g1, g2 = V['g_term'], V['g_term2']
    rr1, rr2 = g1 / roic_term, g2 / roic_term
    rr_term = rr1
    # THE RETIRED FORM, kept on a few lines so the change is legible and priced
    # [R-TERM-01]. Both stages charged reinvestment as g / return on capital, which is
    # arithmetically the same as rebuilding the entire capital base every 1/g years —
    # fifty in stage one and sixty-seven in stage two, both facts about the dirham's peg
    # to the dollar rather than about a chilled-water plant this company's own notes turn
    # over in 28.1 years.
    tv_retired = 0.0
    nop_k = nopat['FY30']
    for k in range(1, 11):
        nop_k = nop_k * (1 + g1)
        tv_retired += nop_k * (1 - rr1) / (1 + wacc) ** k
    tv_retired += (nop_k * (1 + g2) * (1 - rr2) / (wacc - g2)) / (1 + wacc) ** 10

    # THE CAPITAL ONE UNIT OF REAL GROWTH NEEDS, AND THE OBVIOUS DERIVATION IS REJECTED
    # WITH ITS NUMBER. The marginal reading used on the other names in this programme —
    # the change in invested capital over the change in revenue across the explicit
    # window, at terminal revenue — comes out NEGATIVE here, because over these five years
    # the existing plant is written down faster than capex replaces it and the working
    # capital is negative and growing more so. A negative capital requirement would CREDIT
    # this company for growing, which is not something a chilled-water network can do:
    # another unit of demand needs another plant. So the requirement is the intensity the
    # business already runs at — one per cent of real growth costs one per cent of the
    # invested capital it operates on — which is derivable from the model's own terminal
    # figures rather than invented.
    inc_cap_marginal = (((ic_term - (ppe_d['FY26'] + nwc_d['FY26']))
                         / (rev['FY30'] - rev['FY26'])) * rev['FY30'])
    inc_cap = ic_term

    def _stage(nopat0, dna0, wc0, g_nom, real, inc):
        return TERMVAL.build(TERMVAL.TerminalInputs(
            nopat=nopat0 * (1 + g_nom), wacc=wacc, inflation=PI_TERM, real_growth=real,
            dna_book=dna0 * (1 + g_nom),
            useful_life_years=V['asset_life_years'],
            useful_life_source=INP['asset_life_years']['source'],
            maintenance_basis='book_dna_escalated',
            working_capital=wc0 * (1 + g_nom),
            incremental_capital_per_unit_growth=inc))

    # STAGE ONE, FY31-FY40: ten more years of ORDINARY cash flow rather than a terminal.
    # The module builds the first of them on the sanctioned definition — profit after tax,
    # add back the book charge, deduct what replacing the plant costs at today's prices,
    # deduct the capital real growth consumes, deduct inflation on the working capital —
    # and the remaining nine grow with it, so every year of the fade rests on the same
    # construction as the perpetuity that follows it.
    t1 = _stage(nopat['FY30'], dna['FY30'], nwc_d['FY30'], g1, V['g1_real'], inc_cap)
    stage1_pv = sum(t1.fcff * (1 + g1) ** (k - 1) / (1 + wacc) ** k for k in range(1, 11))
    # STAGE TWO, the perpetuity from FY41, on a real rate that is NEGATIVE. Real growth is
    # charged NO capital release here and the reason is stated rather than assumed: a
    # district-cooling network shrinking half a point a year in real terms does not sell
    # off half a point of plant, it earns less on the plant it has, so crediting it for
    # capital it never recovers would pay this company for its own decline.
    grow10 = (1 + g1) ** 10
    t2 = _stage(nopat['FY30'] * grow10, dna['FY30'] * grow10, nwc_d['FY30'] * grow10,
                g2, V['g2_real'], 0.0)
    tv = stage1_pv + t2.tv / (1 + wacc) ** 10
    pv_tv = tv * df_['FY30']
    ev = pv_explicit + pv_tv
    # EV -> equity bridge (30-Jun-2026 reviewed BS), receivables at book:
    eq = (ev - net_debt + V['recv_jun26'] + V['invprop_jun26'] + V['fvtpl_jun26']
          + V['fvoci_jun26'])
    nci_frac = V['nci_pat_fy25'] / V['pat_fy25']       # 1.06% of profits
    nci_val = eq * nci_frac
    eq_attr = eq - nci_val
    ps = eq_attr / V['shares_mn']
    return dict(label=label, ebit=ebit, nopat=nopat, fcff=fcff, df=df_, pv=pv,
                pv_explicit=pv_explicit, roic_term=roic_term, rr_term=rr_term,
                tv_retired=tv_retired, stage1_pv=stage1_pv, inc_cap=inc_cap,
                inc_cap_marginal=inc_cap_marginal,
                terminal_stage1=t1.record, terminal_stage2=t2.record,
                tv=tv, pv_tv=pv_tv, tv_share=pv_tv / ev, ev=ev,
                nci_val=nci_val, eq_attr=eq_attr, ps=ps)

D_base_ct = dcf(rev_b, eb_b, dna_b, capex_b, dnwc_b, V['tax_ct'],
                WACC['rating_ct'], 'base / 9% CT / rating-basis ERP')
D_base_dmtt = dcf(rev_b, eb_b, dna_b, capex_b, dnwc_b, V['tax_dmtt'],
                  WACC['rating_dmtt'], 'base / 15% DMTT / rating-basis ERP')
D_pers_ct = dcf(rev_p, eb_p, dna_p, capex_p, dnwc_p, V['tax_ct'],
                WACC['rating_ct'], 'consumption-persists / 9% CT',
                ppe_d=ppe_p, nwc_d=nwc_p)
D_pers_dmtt = dcf(rev_p, eb_p, dna_p, capex_p, dnwc_p, V['tax_dmtt'],
                  WACC['rating_dmtt'], 'consumption-persists / 15% DMTT',
                  ppe_d=ppe_p, nwc_d=nwc_p)
D_base_cds = dcf(rev_b, eb_b, dna_b, capex_b, dnwc_b, V['tax_ct'],
                 WACC['cds_ct'], 'base / 9% CT / CDS-basis ERP')
D_base_dfm = dcf(rev_b, eb_b, dna_b, capex_b, dnwc_b, V['tax_ct'],
                 WACC_DFM_BETA, 'base / 9% CT / DFM-index beta 0.652')
D_base_gross = dcf(rev_b, eb_b, dna_b, capex_b, dnwc_b, V['tax_ct'],
                   WACC_GROSS, 'base / 9% CT / gross-debt WACC weights')
D_base_carry = dcf(rev_b, eb_b, dna_b, capex_b, dnwc_b, V['tax_ct'],
                   WACC_CARRY, 'base / 9% CT / negative-carry net-debt cost')

# ====================== OTHER LENSES =========================================
# Relative multiples (peer set: Tabreed primary, DEWA secondary — cross-check
# sources only). Tabreed FY2025: EBITDA 1.27bn, net debt ~4.6x EBITDA, so the
# comparison runs at the EV line:
# Peer multiples restruck like-for-like (critique, accepted 17-Aug-2026):
# TRAILING peer multiple x TRAILING Empower operating EBITDA (ex receivable
# interest), and the bridge carries the receivables at book like the DCF's.
# The 22-Jun-2026 peer marks are retained pending an anchor-date remark and
# the staleness is disclosed with a sensitivity (Tabreed traded lower by the
# anchor; each 0.5x of multiple = AED 0.078/share on this lens).
# Peer marks RESTRUCK AT THE SUBJECT'S ANCHOR DATE (critique, accepted; fact-
# check 17-Aug-2026): Tabreed closed AED 2.46 on 6-and-7-Aug-2026 (2.72 on
# 22-Jun, -9.6%). EV = 2,835m sh x 2.46 = 6,974 + net debt 5,846 = 12,820 /
# FY2025 EBITDA 1,268 = 10.1x; P/E = 6,974 / 465 = 15.0x.
TABREED_EV_EBITDA = 10.1
DEWA_PE = 16.8
TABREED_PE = 15.0
ebitda_trail = EBITDA25 - V['intco_fy25']          # FY2025A operating EBITDA ex interest
ev_rel = TABREED_EV_EBITDA * ebitda_trail
eq_rel = (ev_rel - net_debt + V['recv_jun26'] + V['invprop_jun26']
          + V['fvtpl_jun26'] + V['fvoci_jun26'])
ps_rel = eq_rel * (1 - V['nci_pat_fy25'] / V['pat_fy25']) / V['shares_mn']
# peer P/E on FY2026E attributable profit (base, 9%) — profit INCLUDES the
# receivable interest (it is real income; only the operating EBITDA excludes it):
fin_net26 = -(V['kd_marg'] * V['borrow_jun26'] - 0.035 * V['cash_jun26'])
intco26 = intco_b['FY26']
np26 = (eb_b['FY26'] + intco26 + V['rental_fy25'] - dna_b['FY26']
        + fin_net26) * (1 - V['tax_ct'])
npa26 = np26 * (1 - V['nci_pat_fy25'] / V['pat_fy25'])
ps_pe = TABREED_PE * npa26 / V['shares_mn']

# Normalized earnings power: FY2026E with consumption at the UNSHOCKED per-RT
# level and the 9%/15% average burden shown separately; normalized EPS x a
# justified multiple from Ke and sustainable payout:
rev_norm26 = cons_per_rt25 * rt_avg['FY26'] + cap_b['FY26'] + V['pipes_rev_fy25']
eb_norm26 = (rev_norm26 + intco26 + V['rental_fy25']
             - EW_RATIO * cons_per_rt25 * rt_avg['FY26']
             - oc_b['FY26'] - ga_b['FY26'] + OI_OP)
np_norm26 = (eb_norm26 - dna_b['FY26'] + fin_net26) * (1 - V['tax_ct'])
npa_norm26 = np_norm26 * (1 - V['nci_pat_fy25'] / V['pat_fy25'])
eps_norm = npa_norm26 / V['shares_mn']
roe_sust = V['npa_fy25'] / ((V['eq_attr_fy25'] + 3197.590) / 2)   # avg FY24-25 equity
rr_eq = V['g_term'] / roe_sust
# FORWARD justified P/E on a FORWARD EPS (critique: the (1+g) factor converts
# leading to trailing and double-counts growth on a forward base — removed):
pe_just = (1 - rr_eq) / (ke_rating - V['g_term'])
ps_norm = eps_norm * pe_just
# the same lens under the 15% framing, tax flowed through EARNINGS AND ROE:
roe_15 = roe_sust * (1 - V['tax_dmtt']) / (1 - V['tax_ct'])
pe_just_15 = (1 - V['g_term'] / roe_15) / (ke_rating - V['g_term'])
ps_norm_15 = eps_norm * (1 - V['tax_dmtt']) / (1 - V['tax_ct']) * pe_just_15

# Book value & sustainable return — BOTH tax framings (critique: the 15%
# column previously left this lens untouched):
bvps = V['eq_attr_jun26'] / V['shares_mn']
pb_just = (roe_sust - V['g_term']) / (ke_rating - V['g_term'])
ps_book = bvps * pb_just
pb_just_15 = (roe_15 - V['g_term']) / (ke_rating - V['g_term'])
ps_book_15 = bvps * pb_just_15

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
    normalized=dict(ps=ps_norm, ps_dmtt=ps_norm_15, weight=0.15),
    book=dict(ps=ps_book, ps_dmtt=ps_book_15, weight=0.15))
central_ct = (0.50 * D_base_ct['ps'] + 0.20 * ps_rel + 0.15 * ps_norm
              + 0.15 * ps_book)
central_dmtt = (0.50 * D_base_dmtt['ps'] + 0.20 * ps_rel + 0.15 * ps_norm_15
                + 0.15 * ps_book_15)

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
wacc_bear = we * ke_bear + wd * V['kd_marg'] * (1 - V['tax_ct'])   # shield stays 9%
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
# The base rung is the DERIVED terminal growth rather than a typed 0.025 that happened to
# equal it: the two agree to fifteen decimal places today and would silently separate the
# moment the real rate or the house inflation moved, leaving a grid whose own base cell is
# not the base [L-306].
g_grid = [0.0, 0.010, 0.020, V['g_term'], 0.030]
wacc_grid = [WACC['rating_ct'] - 0.01, WACC['rating_ct'] - 0.005, WACC['rating_ct'],
             WACC['rating_ct'] + 0.005, WACC['rating_ct'] + 0.01]
sens_wg = []
for w_ in wacc_grid:
    row = []
    for g_ in g_grid:
        nopat30 = D_base_ct['nopat']['FY30']
        ic30 = ppe_b['FY30'] + nwc_b['FY30']
        roic_ = nopat30 / ic30
        g2_ = min(0.015, g_)
        rr1_, rr2_ = g_ / roic_, g2_ / roic_
        tv_ = 0.0; nk = nopat30
        for k in range(1, 11):
            nk = nk * (1 + g_)
            tv_ += nk * (1 - rr1_) / (1 + w_) ** k
        tv_ += (nk * (1 + g2_) * (1 - rr2_) / (w_ - g2_)) / (1 + w_) ** 10
        flows = dict(D_base_ct['fcff']); flows['FY26'] *= 0.5
        pv_e = sum(flows[y] / (1 + w_) ** (i + 0.5)
                   for i, y in enumerate(YRS_F))
        ev_ = pv_e + tv_ / (1 + w_) ** 4.5
        eq_ = (ev_ - net_debt + V['recv_jun26'] + V['invprop_jun26']
               + V['fvtpl_jun26'] + V['fvoci_jun26']) * (1 - V['nci_pat_fy25'] / V['pat_fy25'])
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
             WACC['rating_ct'], f'crux {lvl:.0%}', nwc_d=nwc_a)
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
              currency='AED', asof=INP['spot']['date'], spot=V['spot'],
              shares_mn=V['shares_mn'], mktcap=mktcap,
              klass='operating company — regulated district-cooling utility',
              ownership='DEWA 80% (since Feb-2026), free float ~20%'),
    inputs=INP,
    hist_is=hist_is,
    unit_physical=dict(
        rate_aed_per_rth=0.49 * V['rev_h1_26'] / 1174.0,
        rate_source="H1-2026 consumption revenue (deck mix 49% x 1,519.415) / "
                    "1,174m RTh (deck p4) = 0.634 AED/RTh — 1.4% BELOW the RD10 "
                    "v1.3 regulated cap of 0.643 AED/TRh incl. fuel surcharge: "
                    "Empower already prices at the cap, so there is no tariff "
                    "headroom (supports the flat-tariff base and caps upside)",
        rth_fy25_mn=V['cons_rev']['2025'] / (0.49 * V['rev_h1_26'] / 1174.0),
        eflh_fy25_hrs=(V['cons_rev']['2025'] / (0.49 * V['rev_h1_26'] / 1174.0))
                      * 1000.0 / rt_avg25,
        eflh_h1_2026_hrs=698.0,
        note="Consumption leg decomposed to physical units: revenue = connected "
             "RT x EFLH hours x AED/RTh rate. The crux in these units: the "
             "shock year runs ~6% fewer EFLH hours; recovery restores the "
             "FY2025 ~1,880-hour year."),
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
              kd_at_dmtt=V['kd_marg'] * (1 - V['tax_ct']),
              we=we, wd=wd, mktcap=mktcap, net_debt=net_debt,
              constructions=dict(
                  base_net_target=WACC['rating_ct'], gross=WACC_GROSS,
                  carry=WACC_CARRY, dfm_beta=WACC_DFM_BETA,
                  gross_debt=gross_debt, kd_net_carry=kd_net_carry,
                  ke_dfm=ke_dfm),
              **WACC),
    dcf=dict(base_ct=D_base_ct, base_dmtt=D_base_dmtt, pers_ct=D_pers_ct,
             pers_dmtt=D_pers_dmtt, base_cds=D_base_cds, bear=D_bear,
             bull=D_bull, base_dfm_beta=D_base_dfm, base_gross_wacc=D_base_gross,
             base_carry_wacc=D_base_carry),
    scenarios=dict(bear=dict(rt_path=rt_path_bear, rev=rev_bear,
                             ebitda=eb_bear, wacc=wacc_bear, ke=ke_bear,
                             tax=V['tax_dmtt']),
                   bull=dict(rt_path=rt_path_bull, rev=rev_bull,
                             ebitda=eb_bull, wacc=WACC['rating_ct'],
                             tax=V['tax_ct'])),
    lenses=lenses,
    rel=dict(tabreed_ev_ebitda=TABREED_EV_EBITDA, tabreed_pe=TABREED_PE,
             dewa_pe=DEWA_PE, ev_rel=ev_rel, ps_rel=ps_rel, ps_pe=ps_pe,
             np26=np26, npa26=npa26, ebitda_trail=ebitda_trail,
             mult_date='2026-08-07 anchor (restruck: Tabreed 2.46 on 6/7-Aug; '
                       '0.5x of multiple = AED 0.078/share on this lens)'),
    norm=dict(rev=rev_norm26, ebitda=eb_norm26, npa=npa_norm26, eps=eps_norm,
              pe_just=pe_just, ps=ps_norm, pe_just_15=pe_just_15,
              ps_15=ps_norm_15, roe_15=roe_15),
    book=dict(bvps=bvps, roe_sust=roe_sust, pb_just=pb_just, ps=ps_book,
              pb_just_15=pb_just_15, ps_15=ps_book_15),
    ddm=dict(dps=dps, ps=ps_ddm, policy_mn=V['div_policy']),
    dewa_buyin=dict(price=DEWA_BUYIN, date='2026-02-11',
                    note='related-party CONTROL price for Dubai Holding\'s 24% — '
                         'a disclosed reference point, never fair value'),
    central=dict(ct=central_ct, dmtt=central_dmtt,
                 continuation_ct=central_ct - 0.5 * (D_base_ct['ps'] - D_pers_ct['ps']),
                 continuation_dmtt=central_dmtt - 0.5 * (D_base_dmtt['ps'] - D_pers_dmtt['ps']),
                 labels="recovery (de-escalation) / continuation — published side "
                        "by side like the tax framings; neither is privileged as "
                        "'base' after the 17-Aug macro fact-check",
                 bear=bear, bull=bull, spot=V['spot']),
    # THE ANSWER IS TWO-SIDED AND IT NOW SAYS SO IN THE FORM A READER OUTSIDE THIS STUDY
    # CAN PARSE. It always published four named branches and no single central, which is
    # the honest shape for a study whose answer turns on two undecided questions — but it
    # published them under keys only this study knows, so every instrument that reads a
    # central found none and recorded EMPOWER as UNREADABLE. An unreadable answer is not a
    # clean answer: this study escaped the check on how far a fair value sits from the
    # market price entirely, which is the one instrument that looks at the ANSWER rather
    # than at how it was built.
    central_two_sided=dict(
        branches=[
            dict(label='Consumption recovers, taxed at the 9% corporate rate',
                 value=central_ct,
                 condition='Dubai chilled-water consumption de-escalates toward its '
                           'pre-2024 pattern AND the group stays outside the top-up tax'),
            dict(label='Consumption recovers, taxed at the 15% top-up rate',
                 value=central_dmtt,
                 condition='the same consumption path, with the domestic minimum top-up '
                           'tax applying'),
            dict(label='Consumption continues at its current pace, 9% corporate rate',
                 value=central_ct - 0.5 * (D_base_ct['ps'] - D_pers_ct['ps']),
                 condition='the elevated consumption of the last two summers persists '
                           'AND the group stays outside the top-up tax'),
            dict(label='Consumption continues at its current pace, 15% top-up rate',
                 value=central_dmtt - 0.5 * (D_base_dmtt['ps'] - D_pers_dmtt['ps']),
                 condition='the same consumption path, with the top-up tax applying')],
        question='Two questions, neither settled: does Dubai consumption de-escalate or '
                 'persist, and does the group fall inside the domestic minimum top-up tax?',
        decides='The tax question is worth about six per cent of the answer and the '
                'consumption question about two; together they span the published range. '
                'Neither is ours to settle — one is a regulatory determination not yet '
                'made about this group, and the other is two summers of weather.',
        why_not_averaged='averaging a tax rate that will turn out to be either 9% or 15% '
                         'describes a company that pays 12%, which no rule provides for; '
                         'and the consumption question is a fact about the world that '
                         'will resolve one way, not a distribution to be integrated over.'),
    # FIGURES THE DELIVERED DOCUMENTS COMPUTE FROM COMMITTED SOURCE QUOTES, committed here
    # so the shared prose instrument can reconcile them. Each is real, sourced and derived
    # by the builder from a quote this study already holds — a sovereign auction print
    # pulled out of the curve evidence, the two operating margins the shock paragraph
    # compares, and the interim quarterly margins the bibliography cites from the deck.
    # They were reported unmatched because they existed only inside a builder's regex, and
    # the fix for a real figure the instrument cannot see is to make it visible, never to
    # delete the sentence.
    document_figures=dict(
        sukuk_feb33_yield=0.0413,
        op_margin_fy25=(hist_is['FY25']['ebitda'] - V['intco_fy25'] - V['rental_fy25']
                        - V['ecl_fy25']) / V['rev_fy25'],
        op_margin_fy26e=eb_b['FY26'] / rev_b['FY26'],
        op_margin_fy27e=eb_b['FY27'] / rev_b['FY27'],
        h1_26_q1_ebitda_margin=0.568,
        h1_26_q2_ebitda_margin=0.467,
        # the peer table's own margins, computed from the two disclosed lines beside them
        # rather than left as a ratio only the builder can see
        peer_tabreed_ebitda_margin=(
            json.load(open(os.path.join(HERE, 'sweep_external.json')))
            ['peers_relative_multiples']['TABREED']['fy2025']['ebitda_aed_m'] / 2456.0),
        own_ebitda_margin_fy25=hist_is['FY25']['ebitda'] / hist_is['FY25']['rev']),
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
print(f"constructions: DFM-beta {D_base_dfm['ps']:.3f} | gross-WACC "
      f"{D_base_gross['ps']:.3f} | carry-WACC {D_base_carry['ps']:.3f} "
      f"(WACCs {WACC_DFM_BETA:.4f}/{WACC_GROSS:.4f}/{WACC_CARRY:.4f})")
print(f"TV share of EV: {D_base_ct['tv_share']:.1%}")
print(f"lenses: rel(EV/EBITDA) {ps_rel:.3f} | rel(P/E) {ps_pe:.3f} | norm "
      f"{ps_norm:.3f} | book {ps_book:.3f} | ddm {ps_ddm:.3f}")
print(f"central: 9% {central_ct:.3f} | 15% {central_dmtt:.3f} | bear {bear:.3f} "
      f"| bull {bull:.3f} | spot {V['spot']}")
print(f"\nFY26E rev base {rev_b['FY26']:.1f} (seasonality check {fy26_check:.1f}) "
      f"| EBITDA {eb_b['FY26']:.1f}")
print("\n".join(LOG))
