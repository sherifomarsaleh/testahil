"""Riyadh Cables Group Company (Tadawul 4142) — master computation.
Writes study_numbers.json, the single source of truth every builder reads.

Code-first rule: INPUTS are four-field records {value, source, date, ring}; a bare
numeral cannot enter the model; the ASSERT block raises (no JSON emitted) unless
the bridge closes, the discount-rate glide is ordered, the Kd sits above the
sovereign, and the terminal is ROIC-consistent.

Built on the company's OWN audited consolidated financial statements (KPMG,
unmodified opinions) for FY2022, FY2023, FY2024 and FY2025, plus the official
Tadawul-filed reviewed interim results for the six months to 30 June 2026. Every
historical income-statement, balance-sheet, cash-flow, segment and cost-stack
line is the audited/reviewed figure, transcribed into source_financials.json and
foot-checked (balance sheet balances every year; segments, COGS breakdown,
inventory and EPS all tie). No aggregator, broker or press figure is a build
source.

Company class: operating company — an industrial manufacturer of electrical
cables and wire. Revenue is product sales; the balance sheet is working-capital
heavy (copper/aluminium inventory and trade receivables); there is no captive
lender and no investment-holding structure. Lens set follows the operating-company
reference: an FCFF DCF primary, relative multiples, normalised earnings power and
a book/return lens.

Ground-up construction: a cable maker's cost is dominated by metal. Materials are
94.9% of cost of revenue and the company hedges copper, aluminium and lead. The
build therefore treats the physical unit as an index of cable tonnage and prices
it as METAL CONTENT (on its own commodity path) plus a CONVERSION SPREAD; the
conversion cost stack escalates on Saudi domestic inflation, the materials leg on
the metal path — one escalator per driver class. Gross margin is an OUTPUT of that
stack, never an input. The single most consequential contested judgement — the
conversion spread, i.e. the gross margin the business sustains once the metal
tailwind of FY2024-25 has passed — is computed BOTH ways and published side by
side, anchored on the most recent reviewed actual (H1-2026, 15.26%) rather than
the stale FY2025 full-year print (16.24%).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np

SRC = json.load(open(os.path.join(HERE, 'source_financials.json')))
IS, BS, CF = SRC['income_statement'], SRC['balance_sheet'], SRC['cash_flow']
CB, INV = SRC['cost_of_revenue_breakdown'], SRC['inventory_composition_2025']
SEG25, SEG24 = SRC['segments_2025'], SRC['segments_2024']
GEO, H1 = SRC['geography'], SRC['interims_2026']

MN = 1e6  # statements are in full SAR; the model works in SAR millions for readability


def m(x):
    return x / MN


# ============================ INPUTS =========================================
def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)


AUD = "Audited consolidated financial statements, Riyadh Cables Group Company (KPMG, unmodified opinion)"
INP = dict(
    # ---- anchors --------------------------------------------------------
    spot=I(104.80, "Tadawul daily close, symbol 4142, uploaded price history", "2026-08-18", "Market"),
    shares_out=I(149.7175, "150,000,000 ordinary shares issued (SAR 10 par, paid capital SAR 1,500mn) "
                 "less 282,500 treasury shares; the weighted-average basic/diluted share count in EPS "
                 "Note 41 of the FY2025 audited statements is 149,717,500", "2026-03-26", "Company"),
    tax_eff=I(0.095, "Blended zakat-and-income-tax rate for the forecast. Audited effective charge "
              "(zakat + income tax + deferred) / profit before zakat: FY2023 7.0%, FY2024 7.3%, "
              "FY2025 9.0%. Saudi zakat is ~2.5% of the zakat base; income tax (20%) applies to any "
              "non-GCC-owned share of profits and to foreign operations. 9.5% sits just above the "
              "FY2025 print, allowing for the rising trend and the growing foreign (UAE and export) "
              "profit share rather than extrapolating one year", "2026-03-26", "Company/House"),

    # ---- historical income statement (SAR mn, consolidated, AUDITED) -----
    rev_fy23=I(m(IS['revenue']['2023']), AUD + ", FY2023 (confirmed by the FY2024 comparative column)",
               "2024-03", "Company"),
    rev_fy24=I(m(IS['revenue']['2024']), AUD + ", FY2024 (confirmed by the FY2025 comparative column)",
               "2025-03", "Company"),
    rev_fy25=I(m(IS['revenue']['2025']), AUD + ", FY2025", "2026-03-26", "Company"),
    cogs_fy23=I(m(IS['cost_of_revenue']['2023']), AUD + ", FY2023", "2024-03", "Company"),
    cogs_fy24=I(m(IS['cost_of_revenue']['2024']), AUD + ", FY2024", "2025-03", "Company"),
    cogs_fy25=I(m(IS['cost_of_revenue']['2025']), AUD + ", FY2025", "2026-03-26", "Company"),
    gp_fy23=I(m(IS['gross_profit']['2023']), AUD + ", FY2023", "2024-03", "Company"),
    gp_fy24=I(m(IS['gross_profit']['2024']), AUD + ", FY2024", "2025-03", "Company"),
    gp_fy25=I(m(IS['gross_profit']['2025']), AUD + ", FY2025", "2026-03-26", "Company"),
    op_fy23=I(m(IS['operating_profit']['2023']), AUD + ", FY2023 (restated operating-profit geography "
              "per the FY2024 comparative; net profit identical to the FY2023-as-filed 661.9mn "
              "operating profit — the difference is a reclassification between gross and operating "
              "lines, not an earnings change)", "2025-03", "Company"),
    op_fy24=I(m(IS['operating_profit']['2024']), AUD + ", FY2024", "2025-03", "Company"),
    op_fy25=I(m(IS['operating_profit']['2025']), AUD + ", FY2025", "2026-03-26", "Company"),
    netfin_fy23=I(m(IS['net_finance_costs']['2023']), AUD + ", FY2023 net finance cost (finance costs "
                  "89.62mn less finance income 0.61mn)", "2024-03", "Company"),
    netfin_fy24=I(m(IS['net_finance_costs']['2024']), AUD + ", FY2024 net finance cost (finance costs "
                  "89.98mn less finance income 2.32mn)", "2025-03", "Company"),
    netfin_fy25=I(m(IS['net_finance_costs']['2025']), AUD + ", FY2025 net finance cost (finance costs "
                  "75.35mn less finance income 1.20mn)", "2026-03-26", "Company"),
    zakat_fy23=I(m(IS['zakat_income_tax']['2023']), AUD + ", FY2023 zakat and income tax", "2024-03", "Company"),
    zakat_fy24=I(m(IS['zakat_income_tax']['2024'] + IS['deferred_tax']['2024']),
                 AUD + ", FY2024 total tax charge: zakat and income tax (71.88mn charge) plus the "
                 "deferred-tax credit (8.0mn) = 63.89mn net", "2025-03", "Company"),
    zakat_fy25=I(m(IS['zakat_income_tax']['2025'] + IS['deferred_tax']['2025']),
                 AUD + ", FY2025 zakat and income tax (104.53mn) plus deferred-tax charge (3.15mn)",
                 "2026-03-26", "Company"),
    pat_fy23=I(m(IS['profit_for_year']['2023']), AUD + ", FY2023 profit for the year", "2024-03", "Company"),
    pat_fy24=I(m(IS['profit_for_year']['2024']), AUD + ", FY2024 profit for the year", "2025-03", "Company"),
    pat_fy25=I(m(IS['profit_for_year']['2025']), AUD + ", FY2025 profit for the year", "2026-03-26", "Company"),
    npa_fy24=I(m(IS['profit_to_shareholders']['2024']), AUD + ", FY2024 profit attributable to "
               "shareholders. Basic and diluted EPS 5.45", "2025-03", "Company"),
    npa_fy25=I(m(IS['profit_to_shareholders']['2025']), AUD + ", FY2025 profit attributable to "
               "shareholders. Basic and diluted EPS 7.22", "2026-03-26", "Company"),
    dna_fy23=I(m(CF['total_da']['2023']), AUD + ", FY2023 cash-flow statement: PP&E depreciation "
               "59.53mn + intangibles amortisation 5.57mn + right-of-use depreciation 1.33mn = 66.43mn "
               "(corrected from the first edition, which carried the FY2024 figure in the FY2023 row)",
               "2024-03", "Company"),
    dna_fy24=I(m(CF['total_da']['2024']), AUD + ", FY2024 cash-flow statement: PP&E depreciation "
               "61.96mn + intangibles amortisation 5.60mn + right-of-use depreciation 1.08mn",
               "2025-03", "Company"),
    dna_fy25=I(m(CF['total_da']['2025']), AUD + ", FY2025 cash-flow statement: PP&E depreciation "
               "76.62mn + intangibles amortisation 5.60mn + right-of-use depreciation 3.18mn",
               "2026-03-26", "Company"),

    # ---- historical balance sheet (SAR mn, consolidated, AUDITED) --------
    ppe_fy23=I(m(BS['ppe_net']['2023']), AUD + ", 31 Dec 2023", "2024-03", "Company"),
    ppe_fy24=I(m(BS['ppe_net']['2024']), AUD + ", 31 Dec 2024", "2025-03", "Company"),
    ppe_fy25=I(m(BS['ppe_net']['2025']), AUD + ", 31 Dec 2025", "2026-03-26", "Company"),
    inv_fy23=I(m(BS['inventory_net']['2023']), AUD + ", inventories net of NRV allowance, 31 Dec 2023",
               "2024-03", "Company"),
    inv_fy24=I(m(BS['inventory_net']['2024']), AUD + ", inventories net, 31 Dec 2024", "2025-03", "Company"),
    inv_fy25=I(m(BS['inventory_net']['2025']), AUD + ", inventories net, 31 Dec 2025", "2026-03-26", "Company"),
    recv_fy23=I(m(BS['trade_receivables']['2023'] + BS['contract_assets']['2023'] + BS['advances_other_ca']['2023']),
                AUD + ", 31 Dec 2023: trade receivables 1,305.1mn + contract assets 25.2mn + advances "
                "and other current assets 88.6mn", "2024-03", "Company"),
    recv_fy24=I(m(BS['trade_receivables']['2024'] + BS['contract_assets']['2024'] + BS['advances_other_ca']['2024']),
                AUD + ", 31 Dec 2024: trade receivables 2,022.9mn + contract assets 15.2mn + advances 74.0mn",
                "2025-03", "Company"),
    recv_fy25=I(m(BS['trade_receivables']['2025'] + BS['contract_assets']['2025'] + BS['advances_other_ca']['2025']),
                AUD + ", 31 Dec 2025: trade receivables 2,485.3mn + contract assets 51.9mn + advances 175.4mn",
                "2026-03-26", "Company"),
    pay_fy23=I(m(BS['trade_payables']['2023'] + BS['contract_liab']['2023'] + BS['accrued_other_liab']['2023']),
               AUD + ", 31 Dec 2023: trade and other payables 1,195.4mn + accrued expenses and other "
               "liabilities 266.5mn + contract liabilities 25.0mn. The accrued line was omitted from the "
               "first edition's FY2023 payables, understating FY2023 working-capital funding relative to "
               "FY2024-25 (both of which included it); corrected here so the net-working-capital series is "
               "built on a consistent basis across all three years", "2024-03", "Company"),
    pay_fy24=I(m(BS['trade_payables']['2024'] + BS['contract_liab']['2024'] + BS['accrued_other_liab']['2024']),
               AUD + ", 31 Dec 2024: trade and other payables 1,598.4mn + accrued expenses and other "
               "liabilities 381.1mn + contract liabilities 61.2mn", "2025-03", "Company"),
    pay_fy25=I(m(BS['trade_payables']['2025'] + BS['contract_liab']['2025'] + BS['accrued_other_liab']['2025']),
               AUD + ", 31 Dec 2025: trade and other payables 1,584.2mn + accrued expenses and other "
               "liabilities 537.7mn + contract liabilities 68.7mn. Includes the reverse-factoring "
               "(supplier-finance) balance the company runs within trade payables", "2026-03-26", "Company"),
    cash_fy23=I(m(BS['cash']['2023']), AUD + ", cash and cash equivalents 31 Dec 2023", "2024-03", "Company"),
    cash_fy24=I(m(BS['cash']['2024']), AUD + ", cash 31 Dec 2024", "2025-03", "Company"),
    cash_fy25=I(m(BS['cash']['2025']), AUD + ", cash 31 Dec 2025", "2026-03-26", "Company"),
    assets_fy23=I(m(BS['total_assets']['2023']), AUD + ", total assets 31 Dec 2023", "2024-03", "Company"),
    assets_fy24=I(m(BS['total_assets']['2024']), AUD + ", total assets 31 Dec 2024", "2025-03", "Company"),
    assets_fy25=I(m(BS['total_assets']['2025']), AUD + ", total assets 31 Dec 2025", "2026-03-26", "Company"),
    debt_fy23=I(m(BS['islamic_finance_current']['2023'] + BS['borrowings_noncurrent']['2023']
                  + BS['lease_liab_current']['2023'] + BS['lease_liab_noncurrent']['2023']),
                AUD + ", 31 Dec 2023: Islamic finance facilities and borrowings 722.1mn + lease "
                "liabilities (current 1.1mn + non-current 7.4mn)", "2024-03", "Company"),
    debt_fy24=I(m(BS['islamic_finance_current']['2024'] + BS['borrowings_noncurrent']['2024']
                  + BS['lease_liab_current']['2024'] + BS['lease_liab_noncurrent']['2024']),
                AUD + ", 31 Dec 2024: Islamic finance facilities 433.1mn + lease liabilities 7.4mn",
                "2025-03", "Company"),
    debt_fy25=I(m(BS['islamic_finance_current']['2025'] + BS['borrowings_noncurrent']['2025']
                  + BS['lease_liab_current']['2025'] + BS['lease_liab_noncurrent']['2025']),
                AUD + ", 31 Dec 2025: Islamic finance facilities and borrowings (current 585.2mn + "
                "non-current 24.6mn) + lease liabilities (current 2.0mn + non-current 9.4mn). The "
                "SAR ~1.1bn supplier-finance/reverse-factoring facility is classified within trade "
                "payables, not here, consistent with the audited presentation", "2026-03-26", "Company"),
    eqp_fy23=I(m(BS['total_equity']['2023'] - BS['nci']['2023']), AUD + ", equity attributable to "
               "shareholders 31 Dec 2023 (total equity 2,246.2mn less NCI of -0.5mn)", "2024-03", "Company"),
    eqp_fy24=I(m(BS['equity_to_shareholders']['2024']), AUD + ", equity attributable to shareholders "
               "31 Dec 2024", "2025-03", "Company"),
    eqp_fy25=I(m(BS['equity_to_shareholders']['2025']), AUD + ", equity attributable to shareholders "
               "31 Dec 2025", "2026-03-26", "Company"),
    nci_fy25=I(m(BS['nci']['2025']), AUD + ", non-controlling interests 31 Dec 2025 — rose from "
               "-0.48mn to 62.7mn on the FY2025 acquisition of a subsidiary with NCI", "2026-03-26", "Company"),
    assoc_fy25=I(m(BS['equity_investees']['2025']), AUD + ", equity-accounted investees carrying "
                 "value 31 Dec 2025", "2026-03-26", "Company"),
    nonop_fy25=I(m(BS['fvoci_investments']['2025'] + BS['investment_property_land']['2025']),
                 AUD + ", non-operating assets 31 Dec 2025: investments at FVOCI 10.37mn + investment "
                 "property (land) 10.03mn", "2026-03-26", "Company"),
    total_equity_fy25=I(m(BS['total_equity']['2025']), AUD + ", total equity 31 Dec 2025", "2026-03-26", "Company"),

    # ---- cash-flow markers (SAR mn, AUDITED) -----------------------------
    capex_fy24=I(m(CF['capex_ppe']['2024']), AUD + ", FY2024 cash-flow statement, purchase of "
                 "property, plant and equipment", "2025-03", "Company"),
    capex_fy25=I(m(CF['capex_ppe']['2025']), AUD + ", FY2025 cash-flow statement, purchase of "
                 "property, plant and equipment (of which assets under construction 107.9mn)",
                 "2026-03-26", "Company"),
    ocf_fy25=I(m(CF['net_cfo']['2025']), AUD + ", FY2025 net cash from operating activities",
               "2026-03-26", "Company"),
    div_paid_fy25=I(m(CF['dividends_paid']['2025']), AUD + ", FY2025 dividends paid (SAR 1.9/share "
                    "final for FY2024 + SAR 1.9/share interim = SAR 3.8/share)", "2026-03-26", "Company"),

    # ---- cost stack (SAR mn, Note 34, AUDITED) — the ground-up base -------
    materials_fy24=I(m(CB['materials']['2024']), AUD + ", Note 34 cost of revenue, FY2024: materials "
                     "(copper/aluminium/lead-dominated)", "2025-03", "Company"),
    materials_fy25=I(m(CB['materials']['2025']), AUD + ", Note 34 cost of revenue, FY2025: materials — "
                     "94.9% of cost of revenue and 79.5% of sales; this is the metal-content leg",
                     "2026-03-26", "Company"),
    conv_fy24=I(m(CB['total']['2024'] - CB['materials']['2024']), AUD + ", Note 34, FY2024 conversion "
               "cost (salaries 228.7mn + depreciation 59.6mn + repairs 42.8mn + utilities 57.4mn + "
               "other 21.9mn)", "2025-03", "Company"),
    conv_fy25=I(m(CB['total']['2025'] - CB['materials']['2025']), AUD + ", Note 34, FY2025 conversion "
               "cost (salaries 244.6mn + depreciation 76.4mn + repairs 44.8mn + utilities 68.2mn + "
               "other 19.4mn) — the non-metal leg that escalates on domestic inflation, not metal",
               "2026-03-26", "Company"),

    # ---- segments (SAR mn, Note 40, AUDITED) -----------------------------
    seg_rev_fy25=I(dict(cables=m(SEG25['cables_wires']['revenue']), hv=m(SEG25['hv_turnkey']['revenue']),
                        other=m(SEG25['other']['revenue'])),
                   AUD + ", Note 40 reporting segments, FY2025 revenue: Cables and wires, High-voltage "
                   "cables (turnkey projects), Other (telephone cables and services). Sums exactly to "
                   "consolidated revenue", "2026-03-26", "Company"),
    seg_rev_fy24=I(dict(cables=m(SEG24['cables_wires']['revenue']), hv=m(SEG24['hv_turnkey']['revenue']),
                        other=m(SEG24['other']['revenue'])),
                   AUD + ", Note 40, FY2024 segment revenue", "2025-03", "Company"),
    seg_cost_fy25=I(dict(cables=m(-SEG25['cables_wires']['cost']), hv=m(-SEG25['hv_turnkey']['cost']),
                         other=m(-SEG25['other']['cost'])),
                    AUD + ", Note 40, FY2025 segment cost of revenue", "2026-03-26", "Company"),
    geo_ksa_fy25=I(m(GEO['inside_ksa']['2025']), AUD + ", Note 40 geographic split, FY2025 revenue "
                   "inside Saudi Arabia (73.2% of sales)", "2026-03-26", "Company"),
    geo_exp_fy25=I(m(GEO['outside_ksa']['2025']), AUD + ", Note 40, FY2025 revenue outside Saudi "
                   "Arabia (26.8%), predominantly the UAE at ~SAR 2.2bn", "2026-03-26", "Company"),

    # ---- interim anchor (SAR mn, REVIEWED, Tadawul-filed) ----------------
    h1_26_rev=I(H1['H1_2026_thousands']['revenue'] / 1000.0, "Tadawul-filed reviewed interim results, "
                "six months to 30 Jun 2026 (announcement 29-Jul-2026): revenue", "2026-07-29", "Company"),
    h1_26_gp=I(H1['H1_2026_thousands']['gross_profit'] / 1000.0, "Tadawul-filed reviewed H1-2026 "
               "results: gross profit — FLAT year on year (-0.06%) on +9.5% revenue, so gross margin "
               "15.26% vs H1-2025's 16.72% and FY2025's 16.24%", "2026-07-29", "Company"),
    h1_26_op=I(H1['H1_2026_thousands']['operating_profit'] / 1000.0, "Tadawul-filed reviewed H1-2026 "
               "results: operating profit", "2026-07-29", "Company"),
    h1_26_np=I(H1['H1_2026_thousands']['net_profit_shareholders'] / 1000.0, "Tadawul-filed reviewed "
               "H1-2026 results: net profit to shareholders (+9.96% y/y)", "2026-07-29", "Company"),

    # ---- forecast drivers — cable tonnage index, metal path, spread ------
    vol_growth=I([0.10, 0.075, 0.065, 0.055, 0.050],
                 "Real cable-volume (tonnage-index) growth FY2026E-FY2030E, tapering from ~10% toward "
                 "5%. Anchored on the reviewed H1-2026 disclosure that revenue rose 9.5% 'due to the "
                 "increase in the volume of quantities sold' with metal prices roughly flat, and on the "
                 "Saudi grid-expansion and construction demand behind Vision-2030 (Saudi Electricity "
                 "capex, NEOM/giga-project cabling, housing); tapered because a mid-teens pace is not a "
                 "perpetuity. The company does not disclose tonnage, so this is an index, not an absolute "
                 "volume", "2026-08-18", "Industry/House"),
    metal_growth=I([-0.01, 0.00, 0.01, 0.01, 0.01],
                   "Metal-content price growth FY2026E-FY2030E for the copper/aluminium/lead blend that "
                   "is 94.9% of cost of revenue. Held broadly flat with a slight near-term easing: LME "
                   "copper ~USD 9,500-10,000/t and aluminium ~USD 2,500/t in mid-2026, and H1-2026 gross "
                   "profit was flat, consistent with metals not repeating the FY2024-25 tailwind. A "
                   "directional metals view would dominate the valuation, so the base holds them near "
                   "current and the sensitivity carries +/-15% metal moves. SAR is pegged to the US "
                   "dollar, so LME dollar prices pass through with no separate currency leg",
                   "2026-08-18", "Industry/House"),
    conv_infl=I([0.03, 0.03, 0.03, 0.03, 0.03],
                "Domestic-inflation escalator on the conversion cost stack (salaries, utilities, "
                "repairs, depreciation) — Saudi CPI has run ~2% and Saudi wage/utility inflation ~3%; "
                "applied ONLY to the non-metal leg, per the one-escalator-per-driver-class rule. The "
                "metal leg escalates on the metal path above, never on this", "2026-08-18", "Country/House"),
    spread_anchor=I(0.1526, "Gross margin the business sustains once the FY2024-25 metal tailwind has "
                    "passed — the study's central contested judgement, anchored on the MOST RECENT "
                    "REVIEWED ACTUAL: the H1-2026 gross margin of 15.26% (gross profit flat on +9.5% "
                    "revenue), BELOW the FY2025 full-year 16.24% and H1-2025's 16.72%. Carried as the "
                    "conversion-spread the model prices; the FY2025 peak is the bull framing, published "
                    "beside it, never averaged in", "2026-07-29", "Company/House"),
    spread_bull=I(0.160, "Bull framing of the sustained gross margin: the FY2025 full-year print holds "
                  "(premium high-voltage and export mix, pricing power in a tight Gulf market). Published "
                  "beside the H1-2026-anchored base, per the dual-framing rule", "2026-08-18", "House"),
    spread_bear=I(0.145, "Bear framing of the sustained gross margin: the conversion spread competes "
                  "down further as Gulf capacity normalises and the metal tailwind fully unwinds",
                  "2026-08-18", "House"),
    margin_glide=I([0.0, 0.001, 0.001, 0.0015, 0.0015],
                   "Small annual drift ADDED to the spread anchor as scale and mix (rising high-voltage "
                   "and export share) modestly lift the sustained margin off the H1-2026 trough; "
                   "cumulative +0.5pp by FY2030E, deliberately modest", "2026-08-18", "House"),
    hv_growth=I([0.10, 0.10, 0.09, 0.08, 0.08],
                "High-voltage turnkey-projects segment revenue growth. The segment is lumpy (FY2025 "
                "SAR 231mn, down from FY2024's 339mn as projects completed); a moderate recovery is "
                "assumed off the low base, well below the cables segment's contribution either way "
                "(2.2% of FY2025 revenue)", "2026-08-18", "House"),
    other_growth=I([0.08, 0.08, 0.07, 0.06, 0.06],
                   "Other segment (telephone cables and services) revenue growth — 0.3% of revenue, "
                   "immaterial to the valuation", "2026-08-18", "House"),
    opex_pct=I([0.043, 0.043, 0.0425, 0.042, 0.042],
               "Operating expenses below gross profit (selling and distribution + general and "
               "administrative + normalised receivables impairment) as a share of revenue. History: "
               "FY2023 4.0%, FY2024 3.4%, FY2025 4.3% (the FY2025 rise is a 150.8mn receivables "
               "impairment charge, up from 23.4mn). Held near the FY2025 level with a slight decline as "
               "the impairment normalises toward the through-cycle rate", "2026-08-18", "House"),
    dna_pct=I(0.0085, "Depreciation and amortisation as a share of revenue, near the FY2025 level "
              "(85.4mn / 10,673.6mn = 0.80%), lifted slightly for the larger capitalised base from the "
              "FY2024-25 capex", "2026-08-18", "House"),
    capex_pct=I([0.019, 0.018, 0.017, 0.016, 0.016],
                "Capital expenditure as a share of revenue, easing from the FY2025 level (188.9mn / "
                "10,673.6mn = 1.77%) held broadly flat — a maintenance-plus-modest-capacity level for a "
                "plant already largely built out (FY2025 assets under construction were 107.9mn of the "
                "188.9mn spend)", "2026-08-18", "House"),
    nwc_pct=I(0.28, "Net working capital as a share of revenue, held near the FY2025 level. History on a "
              "consistent basis (accrued expenses included in payables in every year): FY2023 23.5%, "
              "FY2024 24.4%, FY2025 27.5% — a structurally working-capital-heavy cable maker "
              "(copper/aluminium inventory + trade receivables, partly offset by trade payables and a "
              "reverse-factoring facility) whose intensity has RISEN as the receivables book grew. Held at "
              "the FY2025 level rather than assuming a reversion the disclosures do not evidence", "2026-08-18", "House"),

    # ---- cost of capital (WACC v2) ---------------------------------------
    rf=I(0.0550, "Saudi 10-year local-currency (SAR) government sukuk yield ~5.50%. RE-DERIVED from "
         "primary index observations after external audit (the prior 4.85% policy-rate-plus-term-premium "
         "estimate sat below the entire published SAR government sukuk curve): FTSE Saudi Government Bond "
         "Index 7-10-year yield-to-maturity 5.52% (31-Jul-2026 factsheet); iBoxx Tadawul SAR Government "
         "Sukuk Index broad yield 5.44% at 6.07-year modified duration (S&P DJI, Q1-2026 commentary) on an "
         "UPWARD-sloping curve, so the 10-year point is at or above 5.5%; the 1-year Sah retail sukuk was "
         "4.60% (Jun-2026), consistent with a steep curve. SAR sovereign yields carry a notable pickup "
         "over the USD-pegged curve. Sensitised 5.44-5.75%", "2026-07-31", "Country"),
    sov_spread=I(0.0048, "Saudi Arabia adjusted sovereign default spread 0.48% (Moody's Aa3), Damodaran "
                 "country-risk-premium file, JULY-2026 update (posted ~10-Jul-2026, superseding the "
                 "January vintage of 0.51% used in the first edition). Netted out of the local-currency "
                 "risk-free rate so sovereign default risk is not charged twice", "2026-07-10", "Country"),
    erp=I(0.0494, "Saudi Arabia total equity risk premium 4.94%, Damodaran country-risk-premium file, "
          "JULY-2026 update: the ~4.20% mature-market premium plus a 0.74% country risk premium (0.48% "
          "default spread scaled by relative equity volatility ~1.55). Updated from the January vintage "
          "(5.01%) after external audit noted a newer vintage existed five weeks before the report date; "
          "the July update pulled premia down modestly across the board", "2026-07-10", "Country"),
    erp_cds=I(0.0490, "Saudi Arabia equity risk premium on the CDS basis ~4.90% (July-2026 vintage). "
              "Published beside the rating basis; the two converge for a high-grade sovereign", "2026-07-10", "Country"),
    beta=I(1.129, "Own-stock tier-1 regression: RIYADHCABLE weekly log-returns against the published "
           "Tadawul All Share Index (TASI), Dimson sum-beta over the full 3.6-year listed history "
           "(185 weekly observations to 13-Aug-2026). R-squared 0.145, standard error 0.309, 90% "
           "confidence interval [0.62, 1.64]. Clears the usability gate (n>=24, R-squared>=5%, "
           "SE<|beta|) and is not weak-instrument flagged. The regressor is the exchange's own index, "
           "not a constituent composite — attested by the beta-provenance gate. Plain-OLS cross-check "
           "0.928; Blume-adjusted 1.086", "2026-08-18", "House"),
    kd=I(0.059, "Marginal cost of debt, pre-tax, in SAR. The company's Islamic Murabaha working-capital "
         "facilities price at SAIBOR plus a variable margin; 3-month SAIBOR ~5.2% (SAMA repo 4.25% plus "
         "the ~95bp SAIBOR-repo spread) plus a ~0.70% corporate margin. Sits above the 5.50% ten-year "
         "sovereign sukuk yield, as a same-currency corporate must, and well above the short-tenor sovereign "
         "that matches these working-capital facilities. The one disclosed long-term tranche (5-year USD "
         "swap + 5.25%) is a specific project facility, not the marginal working-capital rate", "2026-08-18",
         "Company/House"),

    # ---- terminal (norm-built) -------------------------------------------
    rf_term=I(0.0502, "Terminal risk-free rate = the normalised SAR risk-free (rf 5.50% less the 0.48% "
              "sovereign default spread = 5.02%) HELD FLAT: Saudi rates are already at a long-run level, so "
              "no crisis-premium normalisation is applied and the terminal risk-free is NOT marked below its "
              "current normalised level — the terminal cost of equity falls only through beta reverting to "
              "1.0 and a modest country-premium compression, never by cutting the risk-free to lift value",
              "2026-08-18", "House"),
    erp_term=I(0.0470, "Terminal equity risk premium 4.70%, a mild compression of the current 4.94% "
               "(July-2026 Damodaran) as the country risk premium narrows with Vision-2030 diversification; "
               "never held at a crisis level, never below the ~4.2% mature-market base", "2026-08-18", "House"),
    beta_term=I(1.0, "Terminal beta 1.0 — mean reversion toward the market (Blume), from the 1.129 "
                "own-stock estimate; the Blume-adjusted current beta is already 1.086", "2026-08-18", "House"),
    kd_term=I(0.055, "Terminal cost of debt 5.5%, a modest easing from the 5.9% marginal rate as SAMA "
              "tracks the Fed toward a neutral setting", "2026-08-18", "House"),
    wd_term=I(0.05, "Terminal net-debt weight 5%, normalised modestly above today's ~2.4% to acknowledge "
              "the structural working-capital leverage a cable maker carries, while staying far below a "
              "geared capital structure this equity-funded company has never run", "2026-08-18", "House"),
    kd_path=I([0.059, 0.058, 0.057, 0.056, 0.055], "Forward cost-of-debt path FY2026E-FY2030E, easing "
              "gently from the 5.9% marginal rate to the 5.5% terminal as policy normalises. The discount-"
              "rate glide takes its shape from this path by construction", "2026-08-18", "House"),
    g_term=I(0.04, "Terminal growth 4.0% in nominal SAR: ~2% long-run Saudi real growth plus ~2% "
             "inflation. Struck below the terminal risk-free-plus-spread and below a blended nominal "
             "GDP ceiling; sensitised 2-6%. Saudi electrification and construction (grid capex, "
             "giga-projects, housing) support a durable but not perpetual mid-single-digit nominal pace",
             "2026-08-18", "House"),
    anchor_days=I(230, "Days from the DCF construction date (31 Dec 2025, the audited balance-sheet date "
                  "the bridge is built on) to the 18 Aug 2026 anchor. Every lens value is rolled to the "
                  "anchor at the cost of equity, net of the SAR 2.25/share FY2025 final dividend paid "
                  "inside the window, so one date and one price of time govern the comparison to spot",
                  "2026-08-18", "House"),
    div_window=I(2.25, "SAR 2.25/share FY2025 final cash dividend (SAR 336,864,375 total on 149,717,500 "
                 "shares) paid inside the 31-Dec-2025-to-anchor window, netted from the rolled-forward "
                 "value. It is the ONLY dividend paid in the window: the company distributes semi-annually "
                 "(a final declared with the March results and paid ~April, an interim paid ~September), so "
                 "the next FY2026 interim falls AFTER the 18-Aug-2026 anchor. The FY2025 final steps up from "
                 "the SAR 1.9 finals of the prior two years on the higher FY2025 earnings; corrected from "
                 "the 1.90 first-edition figure after external audit", "2026-08-18", "Company/House"),

    # ---- lens inputs -----------------------------------------------------
    ev_ebitda_just=I(9.5, "Justified EV/EBITDA on mid-cycle FY2027E EBITDA. Riyadh Cables trades ~11.9x "
                     "trailing EV/EBITDA and ~14.5x trailing earnings. The wire-and-cable peer set splits in "
                     "two, and the first edition mischaracterised it as a single 7-11x band: developed-market "
                     "majors (Prysmian, Nexans) trade ~7-9x forward EV/EBITDA, while the Indian high-growth "
                     "names (Polycab, KEI) carry ~22-26x on far faster volume growth. 9.5x sits with the "
                     "developed majors — a deliberate discount to Riyadh Cables' OWN trailing multiple for "
                     "its single-country concentration and the unwinding metal tailwind, lifted modestly off "
                     "a bare developed-major level for its higher ROIC (~25%) and durable mid-single-digit "
                     "growth. Bear 7.5x / bull 11.0x", "2026-08-18", "House"),
    pe_just=I(13.0, "Justified through-cycle P/E on normalised earnings. 13.0x for a high-return, "
              "low-leverage regional champion with a ~10% cost of equity and mid-single-digit durable "
              "growth. Bear 10.0x / bull 16.0x", "2026-08-18", "House"),
    roe_sust=I(0.28, "Sustainable return on equity for the book lens. Trailing ROE on average equity is "
               "~36% (FY2025 net profit 1,084.8mn / average equity ~2,966mn); struck below it because the "
               "FY2024-25 prints were lifted by the metal tailwind and a large receivables book, and "
               "because retained-earnings growth dilutes the return as equity compounds", "2026-08-18", "House"),
    lens_weights=I(dict(dcf=0.45, relative=0.20, normalized=0.20, book=0.15),
                   "DCF primary for an operating manufacturer whose cash flows are directly modelled; the "
                   "relative and normalised-earnings lenses carry equal secondary weight and the book lens "
                   "least, because book value understates a business earning a ~30%+ return on it",
                   "2026-08-18", "House"),
    ownership=I(dict(founder_family=0.55, free_float=0.45),
                "Ownership is concentrated in the founding shareholder group with a substantial free "
                "float (the company listed 30% in the December 2022 IPO; a further 9mn-share transfer "
                "among major shareholders was disclosed in May 2026). Indicative split pending the FY2025 "
                "annual-report ownership table; not used as a valuation input", "2026-05-20", "Company/House"),
)

# validate four-field completeness
for k, rec in INP.items():
    assert set(rec) == {'value', 'source', 'date', 'ring'}, f"INPUT {k} not four-field"
    assert rec['source'] and rec['date'] and rec['ring'], f"INPUT {k} missing provenance"

V = {k: rec['value'] for k, rec in INP.items()}
LOG = []


def say(s):
    LOG.append(s); print(s)


say("=" * 78)
say("RIYADH CABLES (Tadawul 4142) — ASSERT / derivation log")
say("built on the audited FY2022-FY2025 statements + the reviewed H1-2026 interim")
say("=" * 78)

# ============================ CALC ===========================================
SH, SPOT, TAX = V['shares_out'], V['spot'], V['tax_eff']
MKTCAP = SPOT * SH

# ---- historical income statement — every line audited ----------------------
ebitda_fy24 = V['op_fy24'] + V['dna_fy24']
ebitda_fy25 = V['op_fy25'] + V['dna_fy25']
nci_fy25 = V['pat_fy25'] - V['npa_fy25']
say(f"[Historical income statement] every FY2023-25 line is the audited figure. Revenue "
    f"{V['rev_fy23']:,.0f} -> {V['rev_fy24']:,.0f} -> {V['rev_fy25']:,.0f} SAR mn "
    f"(+{V['rev_fy24']/V['rev_fy23']-1:.1%}, +{V['rev_fy25']/V['rev_fy24']-1:.1%}); gross margin "
    f"{V['gp_fy23']/V['rev_fy23']:.2%} -> {V['gp_fy24']/V['rev_fy24']:.2%} -> "
    f"{V['gp_fy25']/V['rev_fy25']:.2%}; net profit {V['pat_fy23']:,.0f} -> {V['pat_fy24']:,.0f} -> "
    f"{V['pat_fy25']:,.0f}. House EBITDA (operating profit + D&A) FY24 {ebitda_fy24:,.0f}, FY25 "
    f"{ebitda_fy25:,.0f} ({ebitda_fy25/V['rev_fy25']:.2%} of revenue). Effective zakat/tax rate FY25 "
    f"{V['zakat_fy25']/(V['op_fy25']+V['netfin_fy25']):.1%}.")

hist_is = {}
for y in ('23', '24', '25'):
    rev, gp, op = V[f'rev_fy{y}'], V[f'gp_fy{y}'], V[f'op_fy{y}']
    fin, zk, pat = V[f'netfin_fy{y}'], V[f'zakat_fy{y}'], V[f'pat_fy{y}']
    dna = V.get(f'dna_fy{y}', V['dna_fy25'] if y == '25' else V['dna_fy24'])
    ebt = op + fin
    hist_is[f'FY{y}'] = dict(rev=rev, cogs=V[f'cogs_fy{y}'], gp=gp, ebitda=op + dna, dna=dna, ebit=op,
                             fin=fin, ebt=ebt, zakat=zk, pat=pat)
    assert abs(ebt - (pat - zk)) < 1.0, f"FY{y} P&L does not close: EBT {ebt:.1f} vs PAT-zakat {pat-zk:.1f}"
say("[P&L closure] operating profit + net finance = profit before zakat = profit for the year + "
    "zakat, to the SAR mn, in all three years.")

# ---- historical net working capital (audited balance sheets) ---------------
nwc = {}
for y in ('23', '24', '25'):
    nwc[y] = (V[f'inv_fy{y}'] + V[f'recv_fy{y}']) - V[f'pay_fy{y}']
say(f"[Working capital, audited] inventory + receivables (incl. contract assets and advances) less "
    f"payables (incl. accruals and contract liabilities): FY23 {nwc['23']:,.0f} "
    f"({nwc['23']/V['rev_fy23']:.1%} of revenue), FY24 {nwc['24']:,.0f} ({nwc['24']/V['rev_fy24']:.1%}), "
    f"FY25 {nwc['25']:,.0f} ({nwc['25']/V['rev_fy25']:.1%}) — structurally heavy, a copper/aluminium "
    f"inventory and receivables book part-funded by payables and reverse factoring.")
nwc_fy25 = nwc['25']
assert abs(nwc_fy25 / V['rev_fy25'] - V['nwc_pct']) < 0.015, "NWC driver inconsistent with FY25 actual"

# ---- net financial debt (bridge quantity) ----------------------------------
nd_fy25 = V['debt_fy25'] - V['cash_fy25']
say(f"[Net financial debt] FY2025 gross borrowings incl. leases {V['debt_fy25']:,.0f} less cash "
    f"{V['cash_fy25']:,.0f} = {nd_fy25:,.0f} SAR mn — {nd_fy25/ebitda_fy25:.2f}x EBITDA, a lightly "
    f"geared balance sheet. The reverse-factoring facility (~SAR 1.1bn) sits in working capital, not "
    f"here, so it is captured through the net-working-capital driver rather than double-counted as debt.")

# ---- cost of capital: WACC v2 (sovereign double-count removed) --------------
rf_star = V['rf'] - V['sov_spread']
ke = rf_star + V['beta'] * V['erp']
ke_cds = rf_star + V['beta'] * V['erp_cds']
kd_at = V['kd'] * (1 - TAX)
wd = nd_fy25 / (nd_fy25 + MKTCAP)
we = 1 - wd
wacc = we * ke + wd * kd_at
say(f"[Cost of equity] rf {V['rf']:.2%} less Saudi sovereign default spread {V['sov_spread']:.2%} = "
    f"rf* {rf_star:.2%}; + beta {V['beta']:.3f} x ERP {V['erp']:.2%} -> Ke {ke:.2%} (rating basis). "
    f"CDS basis {ke_cds:.2%} — the two converge for a high-grade sovereign. Country risk enters once, "
    f"via the country premium inside the ERP; the raw local yield is NOT combined with a country-loaded "
    f"ERP, which would double-count.")
say(f"[WACC] weights on net financial debt {wd:.1%} / equity {we:.1%}; Kd after tax "
    f"{V['kd']:.2%} x (1-{TAX:.3f}) = {kd_at:.2%}; WACC {wacc:.2%}. The balance sheet is almost "
    f"entirely equity-funded, so WACC sits close to the cost of equity.")

# ---- terminal WACC (norm-built) --------------------------------------------
ke_term = V['rf_term'] + V['beta_term'] * V['erp_term']
kd_term_at = V['kd_term'] * (1 - TAX)
wacc_term = (1 - V['wd_term']) * ke_term + V['wd_term'] * kd_term_at
say(f"[WACC terminal] Ke {ke_term:.2%} (rf* {V['rf_term']:.2%} + beta_term {V['beta_term']:.2f} x ERP "
    f"{V['erp_term']:.2%}); Kd after tax {kd_term_at:.2%}; weights {1-V['wd_term']:.0%}/{V['wd_term']:.0%} "
    f"-> {wacc_term:.2%}.")
assert wacc_term < wacc, "terminal WACC must be below the explicit-window WACC"
assert V['kd'] > V['rf'], "marginal Kd must sit above the sovereign yield"

# ---- glide: fractions from kd_path -----------------------------------------
kdp = V['kd_path']
glide_frac = [(kdp[0] - k) / (kdp[0] - kdp[-1]) for k in kdp]
fwd = [wacc - (wacc - wacc_term) * f for f in glide_frac]
df_, c = [], 1.0
for w in fwd:
    c /= (1 + w); df_.append(c)
assert all(fwd[i] >= fwd[i + 1] for i in range(len(fwd) - 1)), "glide not monotone"
say("[Glide] forward WACC " + " -> ".join(f"{w:.2%}" for w in fwd) +
    "; discount factors " + ", ".join(f"{d:.4f}" for d in df_) +
    ". The glide fractions are the cost-of-debt path's own cumulative progress, inherited not invented.")

# ============================ GROUND-UP COST-STACK BUILD ======================
# Physical unit = cable tonnage index (FY2025 = 100). Selling price per unit =
# metal content per unit + conversion spread per unit; materials cost per unit =
# metal content per unit; conversion cost per unit escalates on domestic inflation.
# Gross margin is the OUTPUT. This is the disclosed cost structure: materials
# (94.9% of COGS) on the metal path, conversion (5.1%) on domestic inflation.
YRS = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
mat25, conv25, rev25, gp25 = V['materials_fy25'], V['conv_fy25'], V['rev_fy25'], V['gp_fy25']
# FY2025 per-unit economics on a volume index of 100
VOL0 = 100.0
mat_pu0 = mat25 / VOL0                       # metal content per unit
conv_pu0 = conv25 / VOL0                     # conversion cost per unit
rev_pu0 = rev25 / VOL0                       # selling price per unit
gp_pu0 = gp25 / VOL0                         # gross profit per unit
say(f"[Ground-up unit economics, FY2025] on a cable-tonnage index of {VOL0:.0f}: metal content per "
    f"unit {mat_pu0:.2f}, conversion cost per unit {conv_pu0:.2f}, selling price per unit {rev_pu0:.2f} "
    f"SAR mn/index-point; gross profit per unit {gp_pu0:.2f} (gross margin {gp_pu0/rev_pu0:.2%}). "
    f"Materials are {mat25/(-V['cogs_fy25']*-1)*0+mat25/(mat25+conv25):.1%} of cost of revenue.")


def build(gm_anchor=None, metal_mult=1.0, vol_mult=1.0, conv_mult=1.0):
    """Re-run the whole ground-up build. The physical unit is a cable-tonnage index;
    the company earns a CONVERSION SPREAD per unit, not a fixed % of metal cost. So:
    revenue = metal content (on the metal path) + conversion cost (on domestic inflation)
    + conversion spread (calibrated to the FY2026 anchor margin, then escalated on domestic
    inflation). Gross margin is the OUTPUT — it FALLS when metal prices rise (the spread is
    fixed per tonne, so a bigger metal denominator dilutes the %), exactly the H1-2026
    mechanism where gross profit was flat while revenue rose. mat25/conv25 are the whole
    GROUP's cost base (cables & wires is 97.6% of revenue), so this builds the whole group."""
    gm_anchor = V['spread_anchor'] if gm_anchor is None else gm_anchor
    # base-case gross-margin PATH (the driver): anchored on H1-2026, a gentle mix/scale glide,
    # staying below the FY2024-25 metal-tailwind peak of 16.24%.
    gm_target = [gm_anchor + V['margin_glide'][i] for i in range(5)]
    vol = [VOL0]; mat_pu_base = [mat_pu0]; mat_pu = [mat_pu0]; conv_pu = [conv_pu0]
    for i in range(5):
        vol.append(vol[-1] * (1 + V['vol_growth'][i]) * (vol_mult ** 0.2))
        mat_pu_base.append(mat_pu_base[-1] * (1 + V['metal_growth'][i]))          # base metal path
        mat_pu.append(mat_pu[-1] * (1 + V['metal_growth'][i]) * metal_mult ** (1 / 5))  # shocked
        conv_pu.append(conv_pu[-1] * (1 + V['conv_infl'][i]) * conv_mult ** (1 / 5))
    vol, mat_pu_base, mat_pu, conv_pu = vol[1:], mat_pu_base[1:], mat_pu[1:], conv_pu[1:]
    # Conversion spread per unit is CALIBRATED at the BASE metal path to hit the target margin;
    # a metal shock then moves cogs but NOT the spread, so gross margin (the output) is DILUTED
    # by higher metal — the correct economics of a metal converter, and the H1-2026 mechanism.
    gp_pu = [gm_target[i] / (1 - gm_target[i]) * (mat_pu_base[i] + conv_pu[i]) for i in range(5)]
    rev_, gp_, mat_cab, conv_cab = [], [], [], []
    for i in range(5):
        materials = vol[i] * mat_pu[i]
        conversion = vol[i] * conv_pu[i]
        gp = vol[i] * gp_pu[i]
        revenue = materials + conversion + gp
        rev_.append(revenue); gp_.append(gp); mat_cab.append(materials); conv_cab.append(conversion)
    opex_ = [V['opex_pct'][i] * rev_[i] for i in range(5)]
    dna_ = [V['dna_pct'] * rev_[i] for i in range(5)]
    ebit_ = [gp_[i] - opex_[i] for i in range(5)]
    ebitda_ = [ebit_[i] + dna_[i] for i in range(5)]
    tot25 = sum(V['seg_rev_fy25'].values())
    mix = {k: V['seg_rev_fy25'][k] / tot25 for k in V['seg_rev_fy25']}
    return dict(rev=rev_, gp=gp_, opex=opex_, dna=dna_, ebit=ebit_, ebitda=ebitda_,
                gm=[gp_[i] / rev_[i] for i in range(5)], vol_index=vol[-1],
                gp_pu=gp_pu, mat_pu=mat_pu, conv_pu=conv_pu, vol=vol,
                rev_cab=rev_, mat_cab=mat_cab, conv_cab=conv_cab,
                seg_rev=[{k: rev_[i] * mix[k] for k in mix} for i in range(5)])


_B = build()
rev, gp, opex, dna, ebit, ebitda = (_B['rev'], _B['gp'], _B['opex'], _B['dna'], _B['ebit'], _B['ebitda'])
gm = _B['gm']
ebitda_margin = [ebitda[i] / rev[i] for i in range(5)]
say(f"[Forecast, ground-up] revenue " + " -> ".join(f"{r:,.0f}" for r in rev) +
    " (growth " + ", ".join(f"{rev[i]/(rev25 if i == 0 else rev[i-1])-1:+.1%}" for i in range(5)) + ")")
say(f"[Forecast margins are OUTPUTS] gross margin " + " -> ".join(f"{x:.2%}" for x in gm) +
    f"; EBITDA margin " + " -> ".join(f"{x:.2%}" for x in ebitda_margin) +
    f". The gross margin is anchored on the H1-2026 reviewed actual ({V['spread_anchor']:.2%}) and "
    f"lifts only modestly on the mix/scale glide — it does NOT return to the FY2024-25 metal-tailwind "
    f"peak.")

# FY2026 cross-check against the reviewed H1-2026 print
h1_gm = V['h1_26_gp'] / V['h1_26_rev']
fy26_rev_implied = V['h1_26_rev'] * 2 * 1.02   # H1 x2 with a light seasonal uplift
say(f"[FY2026 cross-check against the reviewed print] H1-2026 revenue {V['h1_26_rev']:,.0f} at a "
    f"{h1_gm:.2%} gross margin. Doubling H1 with a light seasonal uplift implies a full year near "
    f"{fy26_rev_implied:,.0f}; the build produces {rev[0]:,.0f} ({rev[0]/fy26_rev_implied-1:+.1%}). The "
    f"model's FY2026E gross margin {gm[0]:.2%} sits right on the reviewed H1 actual.")
assert abs(rev[0] / fy26_rev_implied - 1) < 0.08, "FY26 build diverges from the H1-2026 print"
assert abs(gm[0] - h1_gm) < 0.01, "FY26 gross margin not anchored on the H1-2026 actual"

# ---- FCFF waterfall ---------------------------------------------------------
nopat = [ebit[i] * (1 - TAX) for i in range(5)]
capex = [V['capex_pct'][i] * rev[i] for i in range(5)]
nwc_f = [V['nwc_pct'] * r for r in rev]
dnwc = [nwc_f[0] - nwc_fy25] + [nwc_f[i] - nwc_f[i - 1] for i in range(1, 5)]
fcff = [nopat[i] + dna[i] - capex[i] - dnwc[i] for i in range(5)]
pv = [fcff[i] * df_[i] for i in range(5)]
pv_explicit = float(sum(pv))
say(f"[FCFF waterfall] EBIT " + " -> ".join(f"{e:,.0f}" for e in ebit) + "; NOPAT " +
    " -> ".join(f"{n:,.0f}" for n in nopat) + "; less capex " + ", ".join(f"{c:,.0f}" for c in capex) +
    " and working-capital investment " + ", ".join(f"{d:+,.0f}" for d in dnwc) +
    "; FCFF " + " -> ".join(f"{f:,.0f}" for f in fcff) + f"; PV of explicit FCFF {pv_explicit:,.0f}.")

# ---- invested capital, terminal ROIC ---------------------------------------
ic_fy25 = nwc_fy25 + V['ppe_fy25']
ppe = []
p = V['ppe_fy25']
for i in range(5):
    p += capex[i] - dna[i]; ppe.append(p)
ic = [nwc_f[i] + ppe[i] for i in range(5)]
roic = [nopat[i] / ic[i] for i in range(5)]
roic_term = nopat[-1] * (1 + V['g_term']) / ic[-1]
nopat_fy25 = V['op_fy25'] * (1 - V['zakat_fy25'] / (V['op_fy25'] + V['netfin_fy25']))
hist_roic25 = nopat_fy25 / ic_fy25
say(f"[Return on capital] FY2025 NOPAT {nopat_fy25:,.0f} / invested capital {ic_fy25:,.0f} = "
    f"{hist_roic25:.1%}; forecast ROIC {roic[0]:.1%} -> {roic[-1]:.1%}; terminal ROIC (next-year NOPAT "
    f"over closing capital) {roic_term:.1%}. A high-return, capital-light-relative-to-earnings model.")

# terminal value: reinvestment forced to satisfy g = ROIC x RR
rr_term = V['g_term'] / roic_term
nopat_term = nopat[-1] * (1 + V['g_term'])
tv = nopat_term * (1 - rr_term) / (wacc_term - V['g_term'])
pv_tv = tv * df_[-1]
ev = pv_explicit + pv_tv
tv_share = pv_tv / ev
say(f"[Terminal value] terminal ROIC {roic_term:.1%}; required reinvestment g/ROIC {rr_term:.1%}; "
    f"terminal NOPAT {nopat_term:,.0f}; TV {tv:,.0f} discounted at the year-5 factor {df_[-1]:.4f} -> PV "
    f"{pv_tv:,.0f}. Terminal value is {tv_share:.0%} of enterprise value.")
assert abs(roic_term * rr_term - V['g_term']) < 1e-9, "terminal g != ROIC x RR"

# terminal-growth ceiling (blended nominal)
SAUDI_NOM = 0.05    # long-run Saudi nominal GDP growth ~5%
exp_share = V['geo_exp_fy25'] / V['rev_fy25']
blend_ceiling = (1 - exp_share) * SAUDI_NOM + exp_share * 0.045
say(f"[Terminal ceiling] {1-exp_share:.0%} of revenue is domestic (Saudi nominal ~{SAUDI_NOM:.0%}), "
    f"{exp_share:.0%} export (~4.5% world nominal); blended ceiling {blend_ceiling:.1%}. Adopted g "
    f"{V['g_term']:.1%} sits below it.")
assert V['g_term'] < blend_ceiling, "terminal g exceeds the blended nominal ceiling"

# ---- forward profit / equity / net-debt paths ------------------------------
nci_share = nci_fy25 / V['pat_fy25']
PAYOUT = 0.55   # FY2025 paid SAR 3.8/share on EPS 7.22 = 52.6%; semi-annual policy, ~55% forward
interest_path, np_fc, div_fc, eq_fc, nd_fc = [], [], [], [], []
_nd, _eq = nd_fy25, V['eqp_fy25']
for i in range(5):
    _cash = V['debt_fy25'] - _nd
    _int = V['kd_path'][i] * V['debt_fy25'] - 0.04 * max(_cash, 0.0)   # surplus cash yields ~4% (SAR deposit)
    _pbt = ebit[i] - _int
    _npa = _pbt * (1 - TAX) * (1 - nci_share)
    _div = PAYOUT * _npa
    _eq += _npa - _div
    _nd = _nd - (fcff[i] - _int * (1 - TAX)) + _div
    interest_path.append(_int); np_fc.append(_npa); div_fc.append(_div); eq_fc.append(_eq); nd_fc.append(_nd)
say(f"[Forecast profit & distribution] attributable profit " + ", ".join(f"{x:,.0f}" for x in np_fc) +
    f"; payout {PAYOUT:.0%} (the FY2025 actual was 52.6%: SAR 3.8/share on EPS 7.22); net debt path " +
    ", ".join(f"{x:,.0f}" for x in nd_fc) + " — the company de-gears further as free cash flow accrues.")

# ---- EV -> equity bridge ----------------------------------------------------
assoc_val = V['assoc_fy25']
nonop_val = V['nonop_fy25']
eq_pre_nci = ev - nd_fy25 + assoc_val + nonop_val
nci_val = V['nci_fy25']   # deduct NCI at audited carrying value
eq_attr = eq_pre_nci - nci_val
dcf_ps_dec = eq_attr / SH
say(f"[Bridge] EV {ev:,.0f} - net debt {nd_fy25:,.0f} + associates {assoc_val:,.0f} + non-operating "
    f"assets {nonop_val:,.0f} = {eq_pre_nci:,.0f}; less NCI at carrying value {nci_val:,.0f} = equity "
    f"attributable {eq_attr:,.0f} = SAR {dcf_ps_dec:.2f}/share at 31-Dec-2025.")
assert abs((ev - nd_fy25 + assoc_val + nonop_val - nci_val) - eq_attr) < 1e-6, "bridge does not close"
assert nd_fy25 > 0 and nci_val > 0, "net debt and NCI must reduce equity value"

# ---- one date, one price of time: roll every lens to the anchor -------------
T_ANCHOR = V['anchor_days'] / 365.0
ROLL = (1 + ke) ** T_ANCHOR


def to_anchor(v):
    return v * ROLL - V['div_window']


dcf_ps = to_anchor(dcf_ps_dec)
say(f"[Anchor roll] SAR {dcf_ps_dec:.2f}/share at 31-Dec-2025 rolled {V['anchor_days']}/365 of a year "
    f"at the {ke:.1%} cost of equity (x{ROLL:.4f}) less the SAR {V['div_window']:.2f} dividend paid in "
    f"the window = SAR {dcf_ps:.2f}/share at the 18-Aug-2026 anchor, against a spot of {SPOT:.2f} "
    f"({dcf_ps/SPOT-1:+.0%}).")

# ---- contested judgement BOTH WAYS: the sustained gross margin --------------
def dcf_at_spread(spread):
    B = build(gm_anchor=spread)
    _ebit = B['ebit']
    _nopat = [e * (1 - TAX) for e in _ebit]
    _rev = B['rev']
    _capex = [V['capex_pct'][i] * _rev[i] for i in range(5)]
    _dna = B['dna']
    _nwc = [V['nwc_pct'] * r for r in _rev]
    _dnwc = [_nwc[0] - nwc_fy25] + [_nwc[i] - _nwc[i - 1] for i in range(1, 5)]
    _f = [_nopat[i] + _dna[i] - _capex[i] - _dnwc[i] for i in range(5)]
    _ppe, pp = [], V['ppe_fy25']
    for i in range(5):
        pp += _capex[i] - _dna[i]; _ppe.append(pp)
    _ic = _nwc[-1] + _ppe[-1]
    _roic = _nopat[-1] * (1 + V['g_term']) / _ic
    _rr = V['g_term'] / _roic
    _tv = _nopat[-1] * (1 + V['g_term']) * (1 - _rr) / (wacc_term - V['g_term'])
    _ev = sum(_f[i] * df_[i] for i in range(5)) + _tv * df_[-1]
    return to_anchor(((_ev - nd_fy25 + assoc_val + nonop_val - nci_val)) / SH)


dcf_spread_base = dcf_at_spread(V['spread_anchor'])
dcf_spread_bull = dcf_at_spread(V['spread_bull'])
dcf_spread_bear = dcf_at_spread(V['spread_bear'])
assert abs(dcf_spread_base - dcf_ps) < 0.05, "spread helper does not reproduce base"
say(f"[CONTESTED JUDGEMENT — sustained gross margin, computed BOTH ways] the central question is the "
    f"gross margin the business holds once the FY2024-25 metal tailwind has passed. Anchored on the "
    f"H1-2026 reviewed actual of {V['spread_anchor']:.2%}: SAR {dcf_spread_base:.2f}/share. On the "
    f"FY2025-peak framing ({V['spread_bull']:.1%}): SAR {dcf_spread_bull:.2f}. On the further-"
    f"compression framing ({V['spread_bear']:.1%}): SAR {dcf_spread_bear:.2f}. Published side by side, "
    f"never averaged into one number.")

# ---- scenarios on the DCF ---------------------------------------------------
def dcf_scenario(spread=None, metal_mult=1.0, vol_mult=1.0, wacc_shift=0.0, g=None, nwc=None):
    g = V['g_term'] if g is None else g
    nwc = V['nwc_pct'] if nwc is None else nwc
    B = build(gm_anchor=spread, metal_mult=metal_mult, vol_mult=vol_mult)
    _rev, _ebitda, _dna = B['rev'], B['ebitda'], B['dna']
    _ebit = [_ebitda[i] - _dna[i] for i in range(5)]
    _nopat = [e * (1 - TAX) for e in _ebit]
    _capex = [V['capex_pct'][i] * r for i, r in enumerate(_rev)]
    _nwc = [nwc * r for r in _rev]
    _dnwc = [_nwc[0] - nwc_fy25] + [_nwc[i] - _nwc[i - 1] for i in range(1, 5)]
    _f = [_nopat[i] + _dna[i] - _capex[i] - _dnwc[i] for i in range(5)]
    _we, _wt = wacc + wacc_shift, wacc_term + wacc_shift
    _fwd = [_we - (_we - _wt) * f for f in glide_frac]
    _df, cc = [], 1.0
    for w in _fwd:
        cc /= (1 + w); _df.append(cc)
    _ppe, pp = [], V['ppe_fy25']
    for i in range(5):
        pp += _capex[i] - _dna[i]; _ppe.append(pp)
    _roic = _nopat[-1] * (1 + g) / (_nwc[-1] + _ppe[-1])
    _rr = min(g / _roic, 0.95)
    _tv = _nopat[-1] * (1 + g) * (1 - _rr) / max(_wt - g, 0.02)
    _ev = sum(_f[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    return to_anchor(((_ev - nd_fy25 + assoc_val + nonop_val - nci_val)) / SH)


assert abs(dcf_scenario() - dcf_ps) < 0.05, "scenario engine does not reproduce base"
dcf_bear = dcf_scenario(spread=V['spread_bear'], vol_mult=0.92, wacc_shift=+0.012, g=0.03)
dcf_bull = dcf_scenario(spread=V['spread_bull'], vol_mult=1.05, wacc_shift=-0.010, g=0.045)
say(f"[DCF scenarios] bear {dcf_bear:.2f} / base {dcf_ps:.2f} / bull {dcf_bull:.2f} SAR per share.")

# ---- lens 2: relative -------------------------------------------------------
REL_I = 1
ebitda_mid = ebitda[REL_I]
df_rel = df_[REL_I]
ev_rel_fwd = V['ev_ebitda_just'] * ebitda_mid


def _rel(mult):
    return to_anchor((((mult * ebitda_mid) * df_rel + pv[0] + pv[1]
                       - nd_fy25 + assoc_val + nonop_val - nci_val)) / SH)


rel_ps, rel_bear, rel_bull = _rel(V['ev_ebitda_just']), _rel(7.5), _rel(11.0)
ev_trailing = MKTCAP + nd_fy25
ev_ebitda_trailing = ev_trailing / ebitda_fy25
pe_trailing = SPOT / (V['npa_fy25'] / SH)
say(f"[Relative lens] {V['ev_ebitda_just']}x on FY2027E EBITDA {ebitda_mid:,.0f} discounted at the "
    f"year-2 factor plus interim free cash flow -> SAR {rel_ps:.2f}/share. Trailing EV/EBITDA "
    f"{ev_ebitda_trailing:.1f}x, trailing P/E {pe_trailing:.1f}x.")

# ---- lens 3: normalized earnings power --------------------------------------
norm_margin = ebitda_margin[2]
norm_rev = rev[0]
norm_ebitda = norm_margin * norm_rev
norm_ebit = norm_ebitda - V['dna_pct'] * norm_rev
norm_interest = interest_path[0]
norm_np = (norm_ebit - norm_interest) * (1 - TAX) * (1 - nci_share)
norm_eps = norm_np / SH
norm_ps = to_anchor(V['pe_just'] * norm_eps)
norm_bear = to_anchor(10.0 * norm_eps)
norm_bull = to_anchor(16.0 * norm_eps)
say(f"[Normalised lens] mid-cycle EBITDA margin {norm_margin:.2%} (FY2028E) on FY2026E revenue "
    f"{norm_rev:,.0f} -> normalised EPS {norm_eps:.2f} x {V['pe_just']:.1f} = SAR {norm_ps:.2f}/share.")

# ---- lens 4: book / justified P/B -------------------------------------------
bvps = V['eqp_fy25'] / SH
pb_just = (V['roe_sust'] - V['g_term']) / (ke_term - V['g_term'])
book_ps = to_anchor(pb_just * bvps)
# bear: a lower sustainable return discounted at the HIGHER explicit cost of equity;
# bull: a higher sustainable return at the lower terminal cost of equity.
book_bear = to_anchor(((V['roe_sust'] - 0.05 - V['g_term']) / (ke - V['g_term'])) * bvps)
book_bull = to_anchor(((V['roe_sust'] + 0.03 - V['g_term']) / (ke_term - V['g_term'])) * bvps)
roe_trailing = V['npa_fy25'] / ((V['eqp_fy24'] + V['eqp_fy25']) / 2)
say(f"[Book lens] book value per share SAR {bvps:.2f}; justified P/B {pb_just:.2f}x = (sustainable ROE "
    f"{V['roe_sust']:.0%} - g {V['g_term']:.0%})/(terminal Ke {ke_term:.2%} - g) -> SAR {book_ps:.2f}. "
    f"Trailing ROE {roe_trailing:.1%}.")

# ---- synthesis --------------------------------------------------------------
W = V['lens_weights']
lenses = dict(
    dcf=dict(name='Discounted cash flow (primary)', bear=dcf_bear, base=dcf_ps, bull=dcf_bull, w=W['dcf']),
    relative=dict(name='Relative multiples', bear=rel_bear, base=rel_ps, bull=rel_bull, w=W['relative']),
    normalized=dict(name='Normalised earnings power', bear=norm_bear, base=norm_ps, bull=norm_bull,
                    w=W['normalized']),
    book=dict(name='Book value and sustainable return', bear=book_bear, base=book_ps, bull=book_bull,
              w=W['book']),
)
central = sum(l['base'] * l['w'] for l in lenses.values())
lo = min(l['bear'] for l in lenses.values())
hi = max(l['bull'] for l in lenses.values())
lenses['central'] = dict(name='Weighted central', bear=lo, base=central, bull=hi, w=1.0)
say(f"[Synthesis] weighted central SAR {central:.2f}; full span {lo:.2f} - {hi:.2f}; spot {SPOT:.2f} "
    f"({central/SPOT-1:+.0%} to the central).")
assert 0.30 <= central / SPOT <= 3.0, f"central/spot {central/SPOT:.2f} outside plausibility band"

# ---- sensitivity grids ------------------------------------------------------
g_grid = [0.02, 0.03, 0.04, 0.05, 0.06]
wt_grid = [wacc_term - 0.02, wacc_term - 0.01, wacc_term, wacc_term + 0.01, wacc_term + 0.02]
we_grid = [wacc - 0.02, wacc - 0.01, wacc, wacc + 0.01, wacc + 0.02]


def dcf_at(we_, wt_, g_):
    # A terminal denominator (wt_ - g_) below ~1.5% is a near-singular perpetuity: the implied exit
    # multiple explodes and the cell is not economically meaningful. Report it as n.m. (None) rather
    # than clamp it to an arbitrary floor, which printed a non-monotone number (value FALLING as g
    # rose, purely because the floor stopped the denominator shrinking while the reinvestment drag
    # kept rising). The retained cells now use the true denominator and are monotone by construction.
    if wt_ - g_ < 0.015:
        return None
    _fwd = [we_ - (we_ - wt_) * f for f in glide_frac]
    _df, cc = [], 1.0
    for w in _fwd:
        cc /= (1 + w); _df.append(cc)
    _rr = min(g_ / roic_term, 0.95)
    _tv = nopat[-1] * (1 + g_) * (1 - _rr) / (wt_ - g_)
    _ev = sum(fcff[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    return to_anchor(((_ev - nd_fy25 + assoc_val + nonop_val - nci_val)) / SH)


assert abs(dcf_at(wacc, wacc_term, V['g_term']) - dcf_ps) < 0.05, "dcf_at does not reproduce the base DCF"
grid_wacc_g = [[dcf_at(wacc, wt, g) for g in g_grid] for wt in wt_grid]
beta_grid = [0.70, 0.90, round(V['beta'], 3), 1.30, 1.50]


def dcf_beta(b):
    # Vary the EXPLICIT-window beta only; the terminal beta stays mean-reverted at beta_term (1.0),
    # which is the base-case terminal assumption. So the base-beta column reproduces the base DCF
    # exactly, and the grid isolates the effect of five-year systematic risk on the near-term
    # discounting (and hence on the discount factor carried through to the terminal value).
    ke_b = rf_star + b * V['erp']
    we_ = we * ke_b + wd * kd_at
    return dcf_at(we_, wacc_term, V['g_term'])


grid_beta = [dcf_beta(b) for b in beta_grid]
metal_grid = [0.85, 0.925, 1.0, 1.075, 1.15]
grid_metal = [dcf_scenario(metal_mult=mm) for mm in metal_grid]
spread_grid = [0.140, 0.145, 0.1526, 0.155, 0.160]
grid_spread = [dcf_at_spread(s) for s in spread_grid]
vol_grid = [0.90, 0.95, 1.0, 1.05, 1.10]
grid_vol = [dcf_scenario(vol_mult=vm) for vm in vol_grid]
nwc_grid = [0.24, 0.26, 0.28, 0.30, 0.32]
grid_nwc = [dcf_scenario(nwc=p) for p in nwc_grid]

# ---- expert panel: three genuinely different methods ------------------------
# E1 — earnings power (through-cycle P/E on mid-cycle EPS)
e1_margin = ebitda_margin[2]
e1_rev = rev[2]
e1_ebit = e1_margin * e1_rev - V['dna_pct'] * e1_rev
e1_int = interest_path[2]   # the model's OWN mid-cycle (FY2028E) net interest, consistent with the DCF and
#                             income statement — not a static re-derivation on end-2025 cash, which ignored
#                             the surplus cash the company accumulates as it de-gears
e1_eps = ((e1_ebit - e1_int) * (1 - TAX) * (1 - nci_share)) / SH
e1_base, e1_lo, e1_hi = to_anchor(13.0 * e1_eps), to_anchor(10.0 * e1_eps), to_anchor(16.0 * e1_eps)
# E2 — owner cash earnings (FCFE perpetuity)
e2_fcff = float(np.mean(fcff[2:]))
e2_int_at = interest_path[3] * (1 - TAX)   # model's own FY2029E net interest, after tax (consistent basis)
e2_fcfe = (e2_fcff - e2_int_at) * (1 - nci_share)
e2_base = to_anchor(e2_fcfe * (1 + V['g_term']) / (ke_term - V['g_term']) / SH)
e2_lo = to_anchor(e2_fcfe * 1.02 / (0.5 * (ke + ke_term) - 0.02) / SH)
e2_hi = to_anchor(e2_fcfe * 1.05 / (ke_term - 0.05) / SH)
# E3 — economic profit (cash returns vs cost of capital)
ic_beg = [ic_fy25] + ic[:-1]
ep_ = [nopat[i] - fwd[i] * ic_beg[i] for i in range(5)]
pv_ep = sum(ep_[i] * df_[i] for i in range(5))
ep_term = nopat[-1] * (1 + V['g_term']) - wacc_term * ic[-1] * (1 + V['g_term'])
pv_ep_term = ep_term / (wacc_term - V['g_term']) * df_[-1]
e3_ev = ic_fy25 + pv_ep + pv_ep_term
e3_base = to_anchor(((e3_ev - nd_fy25 + assoc_val + nonop_val - nci_val)) / SH)
e3_lo = to_anchor(((ic_fy25 + pv_ep * 0.7 + pv_ep_term * 0.65 - nd_fy25 + assoc_val + nonop_val - nci_val)) / SH)
e3_hi = to_anchor(((ic_fy25 + pv_ep * 1.15 + pv_ep_term * 1.2 - nd_fy25 + assoc_val + nonop_val - nci_val)) / SH)
experts = dict(
    e1=dict(method_short='earnings power', base=e1_base, rng=[e1_lo, e1_hi], eps=e1_eps,
            margin=e1_margin, rev=e1_rev, ebit=e1_ebit, interest=e1_int, pe=13.0),
    e2=dict(method_short='owner cash earnings', base=e2_base, rng=[e2_lo, e2_hi], fcff=e2_fcff,
            fcfe=e2_fcfe, ke=ke_term, int_at=e2_int_at),
    e3=dict(method_short='cash returns vs cost of capital', base=e3_base, rng=[e3_lo, e3_hi],
            ic0=ic_fy25, pv_ep=pv_ep, pv_ep_term=pv_ep_term, ev=e3_ev, ep=ep_,
            spread=[roic[i] - fwd[i] for i in range(5)]),
)
panel_centre = float(sorted([e1_base, e2_base, e3_base])[1])
say(f"[Expert panel] Expert 1 {e1_base:.2f} [{e1_lo:.2f}-{e1_hi:.2f}]; Expert 2 {e2_base:.2f} "
    f"[{e2_lo:.2f}-{e2_hi:.2f}]; Expert 3 {e3_base:.2f} [{e3_lo:.2f}-{e3_hi:.2f}]; panel median "
    f"{panel_centre:.2f} ({panel_centre/SPOT-1:+.0%} vs spot).")

# ---- fan for the figure -----------------------------------------------------
paths3 = np.load(os.path.join(HERE, 'paths_3M.npy'))
fan = np.percentile(paths3, [5, 25, 50, 75, 95], axis=0)
np.save(os.path.join(HERE, 'fan.npy'), fan)

# ============================ EMIT ==========================================
step0 = json.load(open(os.path.join(HERE, 'step0_result.json')))
strike = json.load(open(os.path.join(HERE, 'strike_result.json')))
beta_res = json.load(open(os.path.join(HERE, 'beta_result.json')))
backtest = json.load(open(os.path.join(HERE, 'backtest_5y.json')))

OUT = dict(
    meta=dict(ticker='RIYADHCABLE', tadawul_code='4142',
              company='Riyadh Cables Group Company', market='TADAWUL', currency='SAR',
              asof='2026-08-18', spot=SPOT, shares_mn=SH, mktcap=MKTCAP,
              ev_trailing=ev_trailing, klass='operating company — electrical cable & wire manufacturer',
              sector='Capital Goods — Electrical Equipment (wire & cable)'),
    inputs=INP,
    hist_is=hist_is,
    hist_bs=dict(
        FY23=dict(ppe=V['ppe_fy23'], inv=V['inv_fy23'], recv=V['recv_fy23'], cash=V['cash_fy23'],
                  assets=V['assets_fy23'], debt=V['debt_fy23'], pay=V['pay_fy23'], nwc=nwc['23'],
                  eqp=V['eqp_fy23'], nd=V['debt_fy23'] - V['cash_fy23']),
        FY24=dict(ppe=V['ppe_fy24'], inv=V['inv_fy24'], recv=V['recv_fy24'], cash=V['cash_fy24'],
                  assets=V['assets_fy24'], debt=V['debt_fy24'], pay=V['pay_fy24'], eqp=V['eqp_fy24'],
                  nwc=nwc['24'], nd=V['debt_fy24'] - V['cash_fy24']),
        FY25=dict(ppe=V['ppe_fy25'], inv=V['inv_fy25'], recv=V['recv_fy25'], cash=V['cash_fy25'],
                  assets=V['assets_fy25'], debt=V['debt_fy25'], pay=V['pay_fy25'], eqp=V['eqp_fy25'],
                  nci=V['nci_fy25'], nd=nd_fy25, nwc=nwc_fy25, assoc=assoc_val, nonop=nonop_val,
                  total_equity=V['total_equity_fy25']),
    ),
    unit_econ=dict(vol0=VOL0, mat_pu0=mat_pu0, conv_pu0=conv_pu0, rev_pu0=rev_pu0, gp_pu0=gp_pu0,
                   materials_share_cogs=mat25 / (mat25 + conv25)),
    fcst=dict(years=YRS, rev=rev, seg_rev=_B['seg_rev'], rev_cab=_B['rev_cab'], mat_cab=_B['mat_cab'],
              conv_cab=_B['conv_cab'], gp=gp, gm=gm, opex=opex, dna=dna, ebit=ebit, ebitda=ebitda,
              ebitda_margin=ebitda_margin, nopat=nopat, capex=capex, nwc=nwc_f, dnwc=dnwc, fcff=fcff,
              df=df_, pv=pv, fwd_wacc=fwd, ppe=ppe, ic=ic, roic=roic, np_attr=np_fc, equity=eq_fc,
              net_debt=nd_fc, interest=interest_path, div=div_fc, payout=PAYOUT, glide_frac=glide_frac,
              ppe_fy25=V['ppe_fy25'], eqp_fy25=V['eqp_fy25'], nwc_fy25=nwc_fy25, nd_fy25=nd_fy25,
              debt_fy25=V['debt_fy25'], nopat_fy25=nopat_fy25, ic_fy25=ic_fy25, dna_fy25=V['dna_fy25']),
    seg_fy25=dict(rev=V['seg_rev_fy25'], cost=V['seg_cost_fy25'],
                  gp={k: V['seg_rev_fy25'][k] + V['seg_cost_fy25'][k] * -1 * 0 - (-V['seg_cost_fy25'][k])
                      for k in V['seg_rev_fy25']},
                  names=dict(cables='Cables and wires', hv='High-voltage cables (turnkey projects)',
                             other='Other (telephone cables & services)'),
                  geo=dict(ksa=V['geo_ksa_fy25'], export=V['geo_exp_fy25'])),
    bottomup=dict(materials_fy25=mat25, conv_fy25=conv25, cost_stack_fy25=SRC['cost_of_revenue_breakdown'],
                  inventory_fy25=INV, h1_26_gm=h1_gm, fy26_implied=fy26_rev_implied),
    wacc=dict(rf=V['rf'], rf_star=rf_star, sov_spread=V['sov_spread'], ke=ke, ke_cds=ke_cds,
              erp=V['erp'], erp_cds=V['erp_cds'], beta=V['beta'], kd=V['kd'], kd_at=kd_at,
              we=we, wd=wd, wacc=wacc, ke_term=ke_term, kd_term=V['kd_term'], kd_term_at=kd_term_at,
              wacc_term=wacc_term, glide_frac=glide_frac, kd_path=V['kd_path'], beta_res=beta_res,
              beta_term=V['beta_term'], rf_term=V['rf_term'], erp_term=V['erp_term'], wd_term=V['wd_term']),
    dcf=dict(pv_explicit=pv_explicit, tv=tv, pv_tv=pv_tv, ev=ev, tv_share=tv_share, nd=nd_fy25,
             assoc=assoc_val, nonop=nonop_val, nci=nci_val, nci_share=nci_share, eq_attr=eq_attr,
             ps=dcf_ps, ps_dec=dcf_ps_dec, roll=ROLL, anchor_days=V['anchor_days'], roic_term=roic_term,
             rr_term=rr_term, g=V['g_term'], bear=dcf_bear, bull=dcf_bull,
             spread_base=dcf_spread_base, spread_bull=dcf_spread_bull, spread_bear=dcf_spread_bear,
             spread_anchor=V['spread_anchor'], spread_bull_v=V['spread_bull'], spread_bear_v=V['spread_bear']),
    terminal_recon=dict(roic_term=roic_term, rr_term=rr_term, ceiling=blend_ceiling,
                        hist_roic25=hist_roic25, nopat_fy25=nopat_fy25),
    lenses=lenses, central=central, span=[lo, hi], spot=SPOT,
    experts=experts, panel_centre=panel_centre,
    rel=dict(ebitda_mid=ebitda_mid, ev_rel_fwd=ev_rel_fwd, pv_interim=pv[0] + pv[1],
             ev_ebitda_trailing=ev_ebitda_trailing, pe_trailing=pe_trailing, just_mult=V['ev_ebitda_just']),
    norm=dict(margin=norm_margin, rev=norm_rev, ebitda=norm_ebitda, ebit=norm_ebit,
              interest=norm_interest, np=norm_np, eps=norm_eps, pe=V['pe_just'], year=YRS[0],
              margin_year=YRS[2]),
    book=dict(bvps=bvps, pb_just=pb_just, roe_sust=V['roe_sust'], roe_trailing=roe_trailing, ke_term=ke_term),
    sens=dict(g_grid=g_grid, wt_grid=wt_grid, we_grid=we_grid, grid_wacc_g=grid_wacc_g,
              beta_grid=beta_grid, grid_beta=grid_beta, metal_grid=metal_grid, grid_metal=grid_metal,
              spread_grid=spread_grid, grid_spread=grid_spread, vol_grid=vol_grid, grid_vol=grid_vol,
              nwc_grid=nwc_grid, grid_nwc=grid_nwc),
    step0=step0, strike=strike, backtest=backtest,
    assert_log=LOG,
)
with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(OUT, f, indent=1, default=float)
say("=" * 78)
say(f"WROTE study_numbers.json | central SAR {central:.2f} [{lo:.2f} - {hi:.2f}] vs spot {SPOT:.2f} "
    f"| DCF {dcf_ps:.2f} | TV {tv_share:.0%} of EV | WACC {wacc:.2%} -> {wacc_term:.2%} | "
    f"margin both-ways {dcf_spread_bear:.0f}/{dcf_spread_base:.0f}/{dcf_spread_bull:.0f}")
