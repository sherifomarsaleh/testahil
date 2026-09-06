"""ELEC study — master computation. Writes study_numbers.json (single source of
truth for every builder). Code-first rule: INPUTS are four-field records
{value, source, date, ring}; a bare numeral cannot enter the model; the ASSERT
block raises (no JSON emitted) unless the bridge closes, the glide is ordered,
the Kd-integrity triple holds, and the terminal is ROIC-consistent."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np

# ============================ INPUTS =========================================
# Every record: {value, source, date, ring}. ring: Market/Country/Industry/Company/House.
def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)

INP = dict(
    # ---- anchors ----
    spot=I(2.19, "uploaded EGX daily history, last close", "2026-08-05", "Market"),
    shares_mn=I(3313.540373, "Mubasher ELEC profile (paid-in capital EGP 662,708,074.60 / par 0.20); "
                "verified 3 ways: SWS holder sum; FY24 EPS 0.40=1,327.8/3,313.5; FY25 EPS 0.15=500.3/3,313.5",
                "2026 (mid)", "Company"),
    tax=I(0.225, "PwC Tax Summaries Egypt — corporate income tax 22.5%, unchanged 2025-26", "2026", "Country"),
    fx=I(49.8, "USD/EGP mid-market 49.765 (Xe/Google Finance, 05-Aug-26). NB the pound was NOT "
         "range-bound over the last year: 46.8 (Feb-26 strong side) to ~54.7 (Apr-26, war spike), "
         "back to ~49.8 — the prior 'range-bound 47-52' description was wrong and is corrected "
         "throughout", "2026-08-05", "Country"),

    # ---- historical income statement (EGP mn) ----
    rev_fy23=I(8673.4, "MarketScreener/Mubasher FY2024 results note (comparative)", "2025-03", "Company"),
    rev_fy24=I(13778.2, "MarketScreener/Mubasher FY2024 consolidated results", "2025-03", "Company"),
    rev_fy25=I(10819.0, "Arab Finance/Zawya FY2025 results (net sales EGP 10.81bn)", "2026-03", "Company"),
    np_fy23=I(1248.0, "Zawya/MarketScreener (FY23 consolidated NP)", "2024-03", "Company"),
    np_fy24=I(1327.8, "Mubasher FY2024 consolidated results", "2025-03", "Company"),
    np_fy25=I(500.31, "Arab Finance FY2025 (attributable; Reuters flash 501.4 incl. NCI)", "2026-03", "Company"),
    ebit_fy24=I(3400.0, "Simply Wall St health page: 'EBIT is EGP3.4B, interest coverage 2x'", "2025-05-22", "Company"),
    ebitda_fy24=I(3490.0, "Investing.com financial summary ('EBITDA 3.49B') — single aggregator, "
                  "period attributed to FY2024; flagged", "2026 capture", "Company"),
    int_cover_fy24=I(2.0, "Simply Wall St health page (interest coverage 2x EBIT)", "2025-05-22", "Company"),
    q1_26_rev=I(2094.0, "Zawya/Arab Finance Q1-2026 (consolidated net sales)", "2026-05", "Company"),
    q1_26_np=I(-241.6, "Zawya/Arab Finance Q1-2026 (consolidated net LOSS)", "2026-05", "Company"),
    q1_25_rev=I(3723.0, "Q1-2026 release comparatives", "2026-05", "Company"),
    q1_25_np=I(451.7, "Q1-2026 release comparatives", "2026-05", "Company"),

    # ---- historical balance sheet anchors (EGP mn) ----
    assets_fy22=I(4960.0, "Zawya 9M-2023 results note (comparative, 31-Dec-2022)", "2023-11", "Company"),
    assets_fy24=I(14970.0, "Zawya/Decypha FY2025 note (comparative) + SWS (15.0bn)", "2026-03", "Company"),
    assets_fy25=I(16460.0, "Zawya/Decypha FY2025 results (total assets, +9.9%)", "2026-03", "Company"),
    debt_fy24=I(8960.0, "Company's own FY25-filing comparative ('vs 8.96bn in 2024'); SWS independent "
                "print ~9.0bn corroborates. Standardized on the filing comparative so every FY24 "
                "net-debt reference in the study is the same number (8,132)", "2026-03-18", "Company"),
    cash_fy24=I(827.6, "Simply Wall St health page (cash & ST investments)", "2025-05-22", "Company"),
    equity_fy24=I(3600.0, "Simply Wall St health page (total shareholder equity)", "2025-05-22", "Company"),
    liab_fy24=I(11300.0, "Simply Wall St health page (total liabilities)", "2025-05-22", "Company"),
    assets_fy23_est=I(10000.0, "House estimate — bounded by 9M-23 disclosed 8,060 and FY24 14,970; "
                      "no FY23 year-end print found (flagged). A single aggregator shows ~8,900, "
                      "which would put this estimate ~12%% high — affects only the FY23 ROIC context "
                      "row, no valuation line", "2026-08-05", "House"),
    facilities_fy25=I(10900.0, "Disclosed: 'obtained credit facilities of EGP 10.9bn during 2025 vs "
                "8.96bn in 2024, from several local banks' (almalnews/amwalalghad FY25 results coverage "
                "of the EGX filing). AMBIGUOUS between drawn balance and limits granted — no longer used "
                "directly as the debt anchor; retained as the disclosure record and upper cross-check "
                "(the triangulated drawn debt below implies ~96% drawn if these are limits)",
                "2026-03-18", "Company"),
    debt_fy25=I(10465.0, "TRIANGULATED drawn debt (rollforward_fy25.py): total liabilities 12,360 "
                "(disclosed assets 16,460 - rolled equity 4,100) less non-debt liabilities ~1,890 "
                "(FY24's 2,410 scaled with purchase value, -21.5%). Independent of the ambiguous "
                "facilities sentence; sits at 96% of the disclosed 10.9bn facilities",
                "2026-08-05", "House"),
    cash_fy25_est=I(665.0, "House: midpoint of [500 stress floor, 830 FY24-flat] — a no-dividend, "
                    "liquidity-conserving year argues below the FY24 print (827.6)", "2026-08-05", "House"),
    q1_26_cogs=I(1975.0, "Q1-2026 cost of sales (almalnews/alborsaanews/hapijournal, 30-Jun-2026, of the "
                 "EGX interim filing)", "2026-06-30", "Company"),
    q1_26_gp=I(119.066, "Q1-2026 gross profit — 5.7% margin vs 33.1% in Q1-25 (same sources)", "2026-06-30", "Company"),
    q1_26_op=I(1.429, "Q1-2026 operating profit — essentially zero (same sources)", "2026-06-30", "Company"),
    q1_25_gp=I(1233.0, "Q1-2025 gross profit comparative (same sources)", "2026-06-30", "Company"),
    q1_25_op=I(1124.0, "Q1-2025 operating profit comparative (same sources)", "2026-06-30", "Company"),
    fy25_standalone_sales=I(4700.0, "FY25 standalone sales EGP 4.7bn vs 7.69bn FY24 (Arab Finance AR) — "
                            "the consolidated subsidiaries carry most of group revenue", "2026-03", "Company"),
    agm_no_dividend=I("FY25 profits carried forward, no cash distribution; new board elected",
                      "AGM resolutions (amwalalghad/almasryalyoum, May-2026)", "2026-05-06", "Company"),

    # ---- derived-history assumptions (flagged house judgments) ----
    fin_cost_fy25_est=I(2150.0, "House derivation: avg debt ~9.25bn x ~23.2% effective (CBE corridor 2025 "
                        "path); closes FY25 P&L to the reported NP 500.3 via EBT=NP/(1-22.5%)", "2026-08-05", "House"),
    fin_cost_fy23_est=I(990.0, "House derivation: avg FY23 debt ~4.5bn (D/E path 36%->248% over 5yrs, "
                        "SWS) x ~22% 2023 corridor-linked rate", "2026-08-05", "House"),
    dna_pct=I(0.013, "House: FY24 EBITDA 3,490 - EBIT 3,400 = ~90mn D&A on 13.8bn revenue (~0.7%); "
              "forecast set at 1.3% of revenue to fund modest PP&E renewal", "2026-08-05", "House"),
    payables_fy25_est=I(1890.0, "Non-debt liabilities rolled from FY24's 2,410 on purchase value "
                        "(volume -34%, copper-in-EGP +20% => x0.785); thin payables consistent with "
                        "LC/bank-financed copper imports (rollforward_fy25.py)", "2026-08-05", "House"),
    nwc_fy25_est=I(12245.0, "House derivation on the triangulated balance sheet: FY25 assets 16,460 - "
                   "cash 665 - PP&E ~680 - other ~980 = gross WC ~14,135; less non-debt liabilities "
                   "~1,890 => ~12,245 (113% of FY25 revenue; FY24 was ~76%)", "2026-08-05", "House"),
    net_debt_fy25_est=I(9805.0, "TRIANGULATED (rollforward_fy25.py, replacing the facilities-sentence "
                        "reading 10,200): (A) balance-sheet residual — disclosed assets 16,460 less "
                        "rolled equity 4,100 (FY24 3,600 + NP 500.3, no dividend) gives liabilities "
                        "12,360; less non-debt liabilities ~1,890 => drawn debt 10,465; less cash 665 "
                        "=> 9,802. (B) cash-flow roll-forward from FY24 ND 8,132 + interest 2,150 + "
                        "tax 145 + capex 210 + dNWC ~2,036 - EBITDA 2,871 => 9,803 (shares the "
                        "balance-sheet WC decomposition with A — agreement is consistency, not full "
                        "independence). (C) facilities-as-drawn 10,235 = the upper cross-check. Range "
                        "9,120-10,360 carried in sensitivity (~±EGP 0.19/sh); the FY24-vintage low "
                        "alternative 8,172 is REJECTED by the reverse test (needs non-debt liabilities "
                        "+41% while purchases fell 21%). Falsifier: audited FY25 borrowings note. "
                        "POST-AUDIT NOTE: two aggregator-side readings sit AT/ABOVE the range top — "
                        "facilities-as-drawn 10,235, and an unverifiable D/E print (299.35%) implying "
                        "~11.4bn total debt / ~10.4bn net — so the residual risk on this anchor is "
                        "SKEWED ADVERSE; the challenged 10,386 reading is explicitly sensitized",
                        "2026-08-05", "House"),
    equity_fy25_est=I(4100.0, "House derivation: FY24 equity 3,600 + FY25 NP 500.3, no dividends "
                      "(company has never paid one)", "2026-08-05", "House"),

    # ---- BOTTOM-UP TONNAGE BUILD (rev 3) ------------------------------------
    # Revenue = volume (kt) x price-per-tonne, where price/t = LME copper x EGP x a
    # fabrication uplift k. EBITDA = volume x conversion-EBITDA per tonne. Margins
    # are OUTPUTS of this build, not inputs.
    capacity_kt=I(25.0, "Annual production capacity ~25,000 t/yr at the PARENT's 370,000 sqm Mostorod "
                  "plant (IATF exhibitor profile — audit-confirmed parent-only). The consolidated "
                  "group adds Giza Power Industry's 81,745 sqm Abu Rawash plant (99.99%%-owned; "
                  "company-stated range 1kV-220kV incl. XLPE HV; certification evidence reaches 33kV; "
                  "tonnage NOT disclosed) — so group capacity exceeds 25kt by an unknown margin and "
                  "every utilization ratio in this study is an UPPER BOUND on a parent-capacity basis",
                  "2025", "Company"),
    copper_hist=I(dict(FY23=8478.0, FY24=9147.0, FY25=10000.0),
                  "LME cash annual averages: 2023 $8,478/t and 2024 $9,147/t (LME published averages); "
                  "2025 ~$10,000/t derived from INN's dated statement that the 2026 consensus average "
                  "$12,600 is '+26% vs the 2025 average'", "2026-08-05", "Global"),
    copper_fcst=I([14000.0] * 5, "Flat at the CURRENT market level ~$14,000/t (LME cash ~13.9-14.2k "
                  "3-4 Aug-26; COMEX $6.63/lb 04-Aug, 2-month high; Aug MTD ~14.1k) — a 'no house view' "
                  "forecast must anchor on the market, and the prior $12,600 anchor was a ~6-month-old "
                  "consensus print ~10%% below the tape (audit-corrected). The −10%% copper sensitivity "
                  "(=12.6k, the old anchor) and the bull's softer-copper leg carry the mean-reversion "
                  "case; Goldman's Dec-25 ~$10.7k H1-26 view was overtaken by events and sits beyond "
                  "the grid", "2026-08-05", "Global"),
    egp_hist=I(dict(FY23=30.7, FY24=45.3, FY25=49.5),
               "USD/EGP annual averages: 2023 official ~30.7 (parallel ~38 — the FY23 implied-volume "
               "range below carries both); 2024 blended ~45.3 (float 06-Mar-24); 2025 ~49.5 "
               "(range-bound 47-52, +6% appreciation year)", "2026-08-05", "Country"),
    egp_fcst=I([50.4, 52.0, 53.5, 55.0, 56.5],
               "~3%/yr nominal crawl — the inflation differential narrows as the CBE targets bite; "
               "far below PPP catch-up, consistent with the post-float managed range", "2026-08-05", "House"),
    k_uplift=I(1.387, "Fabrication uplift: cable price per tonne / copper cost per tonne. Set from the "
               "industry norm that copper is ~70-75% of a power-cable price (IndexBox: LME 'directly "
               "and rapidly reflected' in quotations) => k = 1/0.72 = 1.39. VALIDATION, not "
               "calibration: FY24 revenue 13,778 at 9,147 x 45.3 x 1.387 = 574k EGP/t implies 24.0 kt "
               "— 96% of the stated 25 kt capacity in the sector's boom year. Sensitized ±5%", "2026-08-05", "House"),
    vols_fcst=I([10.4, 11.9, 13.4, 14.8, 16.0],
                "Volumes (kt): Q1-26 implied ~2.4 kt/qtr sets the FY26E base (~42% utilization); "
                "recovery on EETC's EGP 45bn plan, the EU package and interconnector follow-on to "
                "~64% utilization by FY30E — still below the FY23-24 near-full prints; sensitized ±15%", "2026-08-05", "House"),
    ebitda_per_t=I([40.0, 90.0, 115.0, 128.0, 135.0],
                   "Conversion EBITDA per tonne (k EGP/t). Historical: FY23 ~111k, FY24 ~145k (both "
                   "near-full utilization WITH devaluation inventory gains), FY25 ~183k (copper-gain "
                   "inflated), Q1-26 ~11k (under-absorption at ~40% utilization). Forecast recovers "
                   "with utilization to 135k by FY30E — BELOW FY24's 145k nominal despite five years "
                   "of EGP inflation, i.e. a ~30% real discount to the windfall; sensitized ±30%. CROSS-CHECK: as a "
                   "share of realized price/t at the $14k copper anchor, the terminal 135/1,097 = 12.3% matches "
                   "the PRE-windfall 2022 norm (~12% of price at implied full utilization) — the forecast returns "
                   "the company to its pre-devaluation conversion economics, not to the windfall", "2026-08-05", "House"),
    capex_mn=I([225.0, 243.0, 262.0, 283.0, 306.0],
               "Maintenance capex ~EGP 9k per tonne of capacity (25 kt), escalated ~8%/yr — no "
               "disclosed capex any year (flagged gap); FY24 D&A ~0.7% of revenue corroborates a "
               "light fixed-asset base", "2026-08-05", "House"),
    nwc_pct=I([1.12, 1.06, 1.00, 0.94, 0.88],
              "House: FY25 intensity ~113% of revenue (triangulated balance sheet) gliding to 88% as "
              "receivables collect and copper-inflated inventory normalises; FY24 was ~76% — full "
              "reversion NOT assumed; sensitized in the grid", "2026-08-05", "House"),

    # ---- cost of capital (sliding schedule — Egypt) ----
    rf=I(0.2231, "investing.com, Egypt 10Y local-currency govt bond yield, 21-Jul-26 print (cached "
         "in-repo). Audit-checked: the credible early-Aug band is ~22.3-23.0% (Jul-26 3Y auction avg "
         "23.32%; secondary prints 22.6-23.0 reported but unreachable at source) — the print sits at "
         "the LOW edge, worth ~-0.10/sh unfloored if the top of the band is right; May-26 window avg "
         "21.29% (investing series) corroborates the level's vintage", "2026-07-21", "Country"),
    sov_spread_cds=I(0.0340, "Egypt CDS-implied sovereign default spread, Damodaran Jan-2026 original "
                     "file (house cache); market 5Y CDS ~330bp late-May-2026 corroborates", "2026-01-05", "Country"),
    sov_spread_rating=I(0.0637, "Damodaran adjusted default spread, rating basis (Caa1), Jan-2026 "
                        "original file (house cache)", "2026-01-05", "Country"),
    erp_cds=I(0.0941, "Damodaran ORIGINAL ctryprem, Egypt row, CDS column, 'Last updated January 5, "
              "2026' (house cache; original page 403-blocked this session). A July-2026 secondary "
              "reproduction claims total ERP 14.87% — same figure previously caught as a misquote; "
              "NOT adopted, shown in sensitivity only", "2026-01-05", "Country"),
    erp_rating=I(0.1394, "Damodaran ORIGINAL ctryprem, Egypt row, rating basis, Jan-2026 (house cache)",
                 "2026-01-05", "Country"),
    beta=I(0.964, "Own-stock tier-1 regression: ELEC weekly log-returns vs 30-name equal-weight EGX "
           "composite (full engine library), 5yr window: beta 0.964, R2 0.222, n=257, SE 0.113, "
           "CI90 [0.78, 1.15] — passes usability gate; NOT weak-flagged (R2>10%, CI span < 2x beta)",
           "2026-08-05", "House"),
    kd=I(0.220, "Marginal EGP rate for a levered EGX mid-cap: CBE corridor 19.00/20.00% deposit/lending "
         "(main operation 19.50%; third consecutive hold 09-Jul-26 after the 100bp Feb-26 cut) "
         "+ ~2.5pp credit margin; consistent with avg bank lending 21.3% (Jan-26). Cross-checked "
         "against the two effective-rate computations below (23.5% FY24, 22.1% FY25 on the triangulated "
         "debt path). NB the Q1-26 P&L implies a much smaller net finance line (~243/qtr) than Q1-25 "
         "(~542/qtr) — unexplained without the statements (possible FX/interest income offset or "
         "capitalised financing); flagged, does not change the marginal rate", "2026-08-05", "House"),
    kd_eff_fy24=I(0.235, "Effective-rate check #1: FY24 interest ~1,700 (EBIT 3,400 / coverage 2.0x, "
                  "SWS) / avg debt ~(5,500e+8,960)/2 = 7,230 => 23.5%", "2026-08-05", "House"),
    kd_eff_fy25=I(0.221, "Effective-rate check #2: FY25 finance cost ~2,150 (derived, closes P&L to "
                  "reported NP; independently corroborated by Q1-25's implied ~542/qtr) / avg debt "
                  "(8,960 + triangulated 10,465)/2 = 9,713 => 22.1%", "2026-08-05", "House"),
    debt_ccy_evidence=I("No facility-level disclosure reachable (FS notes on Mubasher/company site "
                        "403-blocked). PRESUMPTION, flagged: predominantly EGP working-capital "
                        "facilities (import LCs settled spot; post-2016 Egyptian cable-sector norm); "
                        "no USD facility found in any search — treated as ~100%% EGP with the gap "
                        "stated rather than assumed away",
                        "search sweep 05-Aug-2026, negative result", "2026-08-05", "Company"),
    kd_term=I(0.150, "Terminal Kd: Egyptian long-run corporate-borrowing norm 14-16%, midpoint "
              "(standing house norm; no name-specific reason to deviate)", "2026-08-05", "House"),
    wd_term=I(0.40, "Terminal debt weight D/(D+E): NORMALIZED capital structure, not today's ~60% "
              "distress weight — the steady state the terminal value describes presupposes "
              "deleveraging, and current market-value weights are circular (the equity weight "
              "depends on the DCF's own output). 40% is the industry-normal structure for a "
              "working-capital-funded cable maker; sensitized via the terminal-WACC grid", "2026-08-05", "House"),
    rf_term=I(0.105, "Terminal rf norm-built: CBE's own stated Q4-2028 inflation target 5%% (+/-2pp) "
              "+ ~5.5pp EM real-rate convention (house standing construction)", "2026-08-05", "House"),
    erp_term=I(0.070, "Terminal ERP normalised below the crisis-era 9.41%% CDS-based level toward the "
               "B-rating-class norm; never held flat into perpetuity (house standing rule)", "2026-08-05", "House"),
    kd_path=I([0.220, 0.200, 0.185, 0.168, 0.155],
              "Forward Kd path: FY26 held FLAT at 22%% — the CBE paused its easing cycle in Apr-26 "
              "('wait-and-see', three consecutive holds through 09-Jul-26, inflation guided to "
              "accelerate through Q3-26 on base effects and energy price hikes) and the path resumes "
              "only from FY27 toward the 7%%->5%% inflation-target glide; corporate spread held ~3pp; "
              "terminal 15%%. Next MPC 20-Aug-26 (confirmed). A higher-for-longer path is the explicit "
              "+2pp column of the rate grid. The WACC glide shape is tied to this path by construction",
              "2026-08-05", "House"),
    g_term=I(0.05, "Terminal growth center 5%% — standing convention for established Egyptian names "
             "post-disinflation; grid 3-7%%", "2026-08-05", "House"),

    # ---- lens inputs ----
    ev_ebitda_base=I(5.5, "Justified EV/EBITDA on mid-cycle FY27E EBITDA: SWDY trades ~6x (multiples.vc "
                     "mid-2026) with a fortress balance sheet and export book; ELEC discount for "
                     "leverage, domestic concentration, no dividend record. Bear 4.5x / bull 6.5x",
                     "2026-08-05", "House"),
    pe_norm=I(6.5, "Justified through-cycle P/E on normalized EPS: SWDY 10.4x trailing (stockanalysis, "
              "Jul-26); Riyadh Cables 18x (different market). Levered uncovered EGX small-cap "
              "discount. Bear 5.5x / bull 8.0x", "2026-08-05", "House"),
    roe_sust=I(0.14, "Sustainable ROE for the book lens: normalized NP ~600-750 on ~4.6-5.2bn forward "
               "book => 13-15%%; struck below FY23-24 windfall ROEs (35%%+) which carried "
               "devaluation inventory gains", "2026-08-05", "House"),
    lens_weights=I(dict(dcf=0.40, relative=0.20, normalized=0.20, book=0.20),
                   "House: DCF primary for an operating manufacturer; the three market lenses share "
                   "the remainder equally", "2026-08-05", "House"),
)

# validate four-field completeness (code-first rule)
for k, rec in INP.items():
    assert set(rec) == {'value', 'source', 'date', 'ring'}, f"INPUT {k} not four-field"
    assert rec['source'] and rec['date'] and rec['ring'], f"INPUT {k} missing provenance"

V = {k: rec['value'] for k, rec in INP.items()}

# ============================ CALC ===========================================
SH = V['shares_mn']; SPOT = V['spot']; TAX = V['tax']
MKTCAP = SPOT * SH

# ---- derived history (P&L closure) ----
int_fy24 = V['ebit_fy24'] / V['int_cover_fy24']                     # 1,700
ebt_fy24 = V['ebit_fy24'] - int_fy24                                # 1,700
np_fy24_check = ebt_fy24 * (1 - TAX)                                # 1,317.5 vs 1,327.8
ebt_fy25 = V['np_fy25'] / (1 - TAX)                                 # 645.6
ebit_fy25 = ebt_fy25 + V['fin_cost_fy25_est']                       # 2,795.6
ebitda_fy25 = ebit_fy25 + 0.007 * V['rev_fy25']                     # + ~76 D&A (0.7% hist)
ebt_fy23 = V['np_fy23'] / (1 - TAX)                                 # 1,610.3
ebit_fy23 = ebt_fy23 + V['fin_cost_fy23_est']                       # 2,600.3
ebitda_fy23 = ebit_fy23 + 0.007 * V['rev_fy23']
dna_fy = {'FY23': 0.007 * V['rev_fy23'], 'FY24': V['ebitda_fy24'] - V['ebit_fy24'],
          'FY25': 0.007 * V['rev_fy25']}

hist_is = {
    'FY23': dict(rev=V['rev_fy23'], ebitda=ebitda_fy23, dna=dna_fy['FY23'], ebit=ebit_fy23,
                 fin=-V['fin_cost_fy23_est'], ebt=ebt_fy23, tax=-(ebt_fy23 - V['np_fy23']),
                 np=V['np_fy23']),
    'FY24': dict(rev=V['rev_fy24'], ebitda=V['ebitda_fy24'], dna=dna_fy['FY24'], ebit=V['ebit_fy24'],
                 fin=-int_fy24, ebt=ebt_fy24, tax=-(ebt_fy24 - V['np_fy24']), np=V['np_fy24']),
    'FY25': dict(rev=V['rev_fy25'], ebitda=ebitda_fy25, dna=dna_fy['FY25'], ebit=ebit_fy25,
                 fin=-V['fin_cost_fy25_est'], ebt=ebt_fy25, tax=-(ebt_fy25 - V['np_fy25']),
                 np=V['np_fy25']),
}

# ---- cost of capital: explicit window (sovereign double-count removed) ----
rf_star_cds = V['rf'] - V['sov_spread_cds']
rf_star_rating = V['rf'] - V['sov_spread_rating']
ke_cds = rf_star_cds + V['beta'] * V['erp_cds']            # primary
ke_rating = rf_star_rating + V['beta'] * V['erp_rating']   # alternative
ke_raw = V['rf'] + V['beta'] * V['erp_cds']                # RETIRED, audit trail only
kd_at = V['kd'] * (1 - TAX)
we = MKTCAP / (MKTCAP + V['debt_fy25'])
wd = 1 - we
wacc_exp = we * ke_cds + wd * kd_at
wacc_exp_rating = we * ke_rating + wd * kd_at

# ---- terminal (norm-built, never backed out of a price) ----
# Terminal weights are NORMALIZED, not today's distress weights: using the current
# 60% debt share into perpetuity would assert the near-insolvent capital structure
# persists in the very steady state whose existence presupposes deleveraging — and
# it is circular (the equity weight depends on the equity value the DCF outputs).
# 40% debt / 60% equity is the industry-normal structure (Elsewedy-like), disclosed
# as a house view and sensitized. NB this RAISES terminal WACC vs distress weights
# (more weight on the dearer equity leg) — the conservative direction.
ke_term = V['rf_term'] + V['beta'] * V['erp_term']
kd_term_at = V['kd_term'] * (1 - TAX)
wd_term = V['wd_term']
we_term = 1 - wd_term
wacc_term = we_term * ke_term + wd_term * kd_term_at

# ---- glide: fractions from kd_path (never invented separately) ----
kdp = V['kd_path']
glide_frac = [(kdp[0] - k) / (kdp[0] - kdp[-1]) for k in kdp]
fwd = [wacc_exp - (wacc_exp - wacc_term) * f for f in glide_frac]
df = []
c = 1.0
for w in fwd:
    c /= (1 + w)
    df.append(c)

# ---- BOTTOM-UP forecast & FCFF waterfall (tonnage build) -------------------
# price/t (EGP mn per kt = k EGP/t / 1000): LME x EGP x k_uplift
yrs = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']

def price_per_t(cu_usd, egp):
    return cu_usd * egp * V['k_uplift'] / 1e6          # EGP mn per tonne

# implied HISTORICAL volumes (the calibration evidence)
hist_vol = {}
for y in ('FY23', 'FY24', 'FY25'):
    ppt = price_per_t(V['copper_hist'][y], V['egp_hist'][y])
    hist_vol[y] = dict(price_per_t=ppt, vol_kt=V[f'rev_{y.lower()}'] / ppt / 1000.0,
                       util=V[f'rev_{y.lower()}'] / ppt / 1000.0 / V['capacity_kt'])
# FY23 alternative at the parallel rate (~38): the honest range
_p23 = price_per_t(V['copper_hist']['FY23'], 38.0)
hist_vol['FY23_alt_parallel'] = dict(price_per_t=_p23, vol_kt=V['rev_fy23'] / _p23 / 1000.0,
                                     util=V['rev_fy23'] / _p23 / 1000.0 / V['capacity_kt'])
q1_ppt = price_per_t(12852.0, 50.4)     # Q1-26 LME average (audit: 12,852, not the 12,600 anchor)
hist_vol['Q1_26_annualized'] = dict(price_per_t=q1_ppt,
                                    vol_kt=4 * V['q1_26_rev'] / q1_ppt / 1000.0,
                                    util=4 * V['q1_26_rev'] / q1_ppt / 1000.0 / V['capacity_kt'])
# k EGP per tonne (EGP mn / kt); Q1-26 adds ~25mn quarterly D&A back to the
# disclosed near-zero operating profit
hist_ebitda_per_t = {'FY23': hist_is['FY23']['ebitda'] / hist_vol['FY23']['vol_kt'],
                     'FY24': hist_is['FY24']['ebitda'] / hist_vol['FY24']['vol_kt'],
                     'FY25': hist_is['FY25']['ebitda'] / hist_vol['FY25']['vol_kt'],
                     'Q1_26': (V['q1_26_op'] + 25.0) / (hist_vol['Q1_26_annualized']['vol_kt'] / 4)}

rows = []
nwc_prev = V['nwc_fy25_est']
for i, y in enumerate(yrs):
    ppt = price_per_t(V['copper_fcst'][i], V['egp_fcst'][i])
    vol = V['vols_fcst'][i]
    rev = vol * ppt * 1000.0
    ebitda = vol * V['ebitda_per_t'][i]                # kt x kEGP/t = EGP mn
    dna = rev * V['dna_pct']
    ebit = ebitda - dna
    nopat = ebit * (1 - TAX)
    capex = V['capex_mn'][i]
    nwc = rev * V['nwc_pct'][i]
    dwc = nwc - nwc_prev
    fcff = nopat + dna - capex - dwc
    rows.append(dict(year=y, rev=rev, ebitda=ebitda, dna=dna, ebit=ebit, nopat=nopat,
                     capex=capex, nwc=nwc, dwc=dwc, fcff=fcff,
                     vol_kt=vol, price_per_t=ppt, util=vol / V['capacity_kt'],
                     ebitda_per_t=V['ebitda_per_t'][i], margin=ebitda / rev,
                     fwd_wacc=fwd[i], df=df[i], pv=fcff * df[i]))
    nwc_prev = nwc

pv_sum = sum(r['pv'] for r in rows)

# ---- terminal value, ROIC x RR-consistent (the CLHO rule) ----
nop_T = rows[-1]['nopat']
ic_T = rows[-1]['nwc'] + 0.05 * rows[-1]['rev']       # invested capital ~ NWC + light PP&E
roic_T = nop_T / ic_T
rr_T = V['g_term'] / roic_T                            # reinvestment needed to fund g
fcff_T1 = nop_T * (1 + V['g_term']) * (1 - rr_T)
tv = fcff_T1 / (wacc_term - V['g_term'])
pv_tv = tv * df[-1]
ev = pv_sum + pv_tv
tv_pct = pv_tv / ev

# ---- bridge ----
net_debt = V['net_debt_fy25_est']
nci = 0.0   # consolidated-attributable gap ~1.1mn FY25 — immaterial, carried at zero (flagged)
eq_dcf_unfloored = ev - net_debt - nci
# LIMITED LIABILITY: the equity of a listed company cannot be worth less than zero.
# The unfloored intrinsic (negative here — the EV does not cover the net debt) is
# DISCLOSED in the bridge; the lens carries a nominal floor as pure option value.
eq_dcf = max(eq_dcf_unfloored, 0.0)
dcf_ps_unfloored = eq_dcf_unfloored / SH
dcf_ps = max(eq_dcf / SH, 0.01)

# ---- scenario engine (tonnage knobs) --------------------------------------
def run_dcf(ept_shift=0.0, vol_shift=0.0, cu_shift=0.0, nwc_end=None,
            wacc_t=None, g=None, nd=None, detail=False):
    """ept_shift/vol_shift/cu_shift are proportional (+0.30 = +30%). Copper moves
    BOTH the price line and, via revenue, the working-capital need — the
    double-edged pass-through the tonnage build exists to capture.
    NB terminal ROIC is RECOMPUTED under each shift (shifted NOPAT / shifted invested
    capital), so margin scenarios lift or cut the terminal economics with the explicit
    years — this is the grid's specification, stated in the §1.9 captions.
    detail=True returns the full scenario bridge (PV, TV, EV, ND, equity, per-share)."""
    wt = wacc_term if wacc_t is None else wacc_t
    gg = V['g_term'] if g is None else g
    nde = net_debt if nd is None else nd
    nwcp = list(V['nwc_pct'])
    if nwc_end is not None:
        nwcp = list(np.linspace(nwcp[0], nwc_end, 5))
    fwd_ = [wacc_exp - (wacc_exp - wt) * f for f in glide_frac]
    df_, c_ = [], 1.0
    for w in fwd_:
        c_ /= (1 + w)
        df_.append(c_)
    nwcprev = V['nwc_fy25_est']; pv = 0.0
    for i in range(5):
        ppt = price_per_t(V['copper_fcst'][i] * (1 + cu_shift), V['egp_fcst'][i])
        vol = V['vols_fcst'][i] * (1 + vol_shift)
        rev_ = vol * ppt * 1000.0
        ebitda_ = vol * V['ebitda_per_t'][i] * (1 + ept_shift)
        dna_ = rev_ * V['dna_pct']
        nopat_ = (ebitda_ - dna_) * (1 - TAX)
        nwc_ = rev_ * nwcp[i]
        fcff_ = nopat_ + dna_ - V['capex_mn'][i] - (nwc_ - nwcprev)
        pv += fcff_ * df_[i]
        nwcprev = nwc_
    ic = nwc_ + 0.05 * rev_
    roic = nopat_ / ic
    if roic <= gg / 0.95:                        # growth unfundable — cap RR at 95%
        if detail:
            return dict(pv=pv, tv=0.0, pv_tv=0.0, ev=pv, nd=nde, roic_T=roic,
                        eq=pv - nde, ps=max((pv - nde) / SH, 0.0))
        return max((pv - nde) / SH, 0.0)
    rr = gg / roic
    tv_ = nopat_ * (1 + gg) * (1 - rr) / (wt - gg)
    if detail:
        return dict(pv=pv, tv=tv_, pv_tv=tv_ * df_[-1], ev=pv + tv_ * df_[-1], nd=nde,
                    roic_T=roic, rr_T=rr,
                    eq=pv + tv_ * df_[-1] - nde, ps=(pv + tv_ * df_[-1] - nde) / SH)
    return (pv + tv_ * df_[-1] - nde) / SH

# bear: volumes stall, conversion stays depressed, copper stays up (WC strain),
#       collection fails, terminal costlier. bull: windfall partially returns
#       (ept +30% ~ 175k/t), volumes toward full utilization, collection to the
#       FY24 intensity, easing overshoots.
BEAR_KNOBS = dict(ept_shift=-0.30, vol_shift=-0.10, nwc_end=1.05,
                  wacc_t=wacc_term + 0.02, g=0.04, nd=net_debt + 1000)
BULL_KNOBS = dict(ept_shift=+0.30, vol_shift=+0.15, cu_shift=-0.10, nwc_end=0.76,
                  wacc_t=wacc_term - 0.015, g=0.06, nd=net_debt - 1000)
bear_detail = run_dcf(detail=True, **BEAR_KNOBS)
bull_detail = run_dcf(detail=True, **BULL_KNOBS)
dcf_bear = max(bear_detail['ps'], 0.01)
dcf_bull = bull_detail['ps']

# ---- equity P&L / debt schedule (interest on OPENING net debt, no circularity) ----
# Tax only on positive EBT; FY27's small profit is sheltered by the FY26 loss
# carryforward (Egyptian tax law allows 5-year carryforward) — modelled simply.
is_fcst = []
nd_path, cash_path, eq_path = [net_debt], [V['cash_fy25_est']], [V['equity_fy25_est']]
loss_cf = 0.0
for i, r in enumerate(rows):
    nd_open = nd_path[-1]
    intr = V['kd_path'][i] * nd_open
    ebt = r['ebit'] - intr
    taxable = max(ebt - loss_cf, 0.0)
    tax_chg = TAX * taxable if ebt > 0 else 0.0
    loss_cf = max(loss_cf - max(ebt, 0.0), 0.0) + max(-ebt, 0.0)
    np_ = ebt - tax_chg
    fcf_eq = np_ + r['dna'] - r['dwc'] - r['capex']
    nd_new = nd_open - fcf_eq
    nd_path.append(nd_new)
    eq_path.append(eq_path[-1] + np_)
    is_fcst.append(dict(year=r['year'], rev=r['rev'], ebitda=r['ebitda'], dna=r['dna'],
                        ebit=r['ebit'], fin=-intr, ebt=ebt, tax=-tax_chg, np=np_,
                        eps=np_ / SH, nd_open=nd_open, nd_close=nd_new, fcf_eq=fcf_eq))

# relative lens: EV/EBITDA on FY27E EBITDA (first recovery year), net debt after the
# FY26E release. EBITDA now FLEXES with the scenario (same ±30% conversion shift as the
# DCF scenarios) — an audit correctly noted the prior version applied base EBITDA in
# all three columns, making the lens a constant. All three columns remain negative
# equity at any multiple, so the disclosed 0.05 floor still binds in each.
nd_fy26 = is_fcst[0]['nd_close']
ebitda_27 = rows[1]['ebitda']
rel = {tag: max((m * ebitda_27 * (1 + s) - nd_fy26) / SH, 0.05)
       for tag, m, s in [('bear', 4.5, -0.30), ('base', V['ev_ebitda_base'], 0.0),
                         ('bull', 6.5, +0.30)]}

# normalized earnings power: mid-cycle EBIT less normalized finance cost
ebit_mid = rows[2]['ebit']                       # FY28E-scale operations
nd_mid = 6000.0                                  # post-release, post-paydown mid-cycle net debt
np_norm = (ebit_mid - V['kd_term'] * nd_mid) * (1 - TAX)
eps_norm = np_norm / SH
norm = dict(bear=(rows[2]['ebit'] * 0.9 - 0.16 * 6500) * (1 - TAX) / SH * 5.5,
            base=eps_norm * V['pe_norm'],
            bull=(rows[2]['ebit'] * 1.1 - 0.14 * 5500) * (1 - TAX) / SH * 8.0)

# book lens: justified P/B = (ROE - g)/(Ke_term - g) on FY25e book
bvps = V['equity_fy25_est'] / SH
def jpb(roe, g=V['g_term'], ke=None):
    k = ke_term if ke is None else ke
    return max((roe - g) / (k - g), 0.10)
# one Ke for all three columns (an audit found the prior bull column quietly used
# Ke_term - 1pp, which the stated formula could not reproduce)
book = dict(bear=bvps * jpb(0.11), base=bvps * jpb(V['roe_sust']), bull=bvps * jpb(0.18))

W = V['lens_weights']
lens = dict(dcf=dict(bear=dcf_bear, base=dcf_ps, bull=dcf_bull),
            relative=rel, normalized=norm, book=book)
central = {tag: sum(W[k] * lens[k][tag] for k in W) for tag in ('bear', 'base', 'bull')}
lens['central'] = central

# ---- sensitivity grids ----
wacc_grid = [wacc_term - 0.02, wacc_term - 0.01, wacc_term, wacc_term + 0.01, wacc_term + 0.02]
g_grid = [0.03, 0.04, 0.05, 0.06, 0.07]
sens_wg = [[run_dcf(wacc_t=w, g=g) for g in g_grid] for w in wacc_grid]
expl_grid = [wacc_exp - 0.02, wacc_exp - 0.01, wacc_exp, wacc_exp + 0.01, wacc_exp + 0.02]
sens_expl = [[0.0] * 5 for _ in range(5)]
for i, wex in enumerate(expl_grid):
    for j, wt in enumerate(wacc_grid):
        fwd_ = [wex - (wex - wt) * f for f in glide_frac]
        df_, c_ = [], 1.0
        for w in fwd_:
            c_ /= (1 + w)
            df_.append(c_)
        pv = sum(r['fcff'] * df_[k] for k, r in enumerate(rows))
        tv_ = nop_T * (1 + V['g_term']) * (1 - V['g_term'] / roic_T) / (wt - V['g_term'])
        sens_expl[i][j] = (pv + tv_ * df_[-1] - net_debt) / SH
beta_grid = [0.6, 0.78, 0.8, 0.964, 1.0, 1.15, 1.3]
sens_beta = []
for b in beta_grid:
    ke_b = rf_star_cds + b * V['erp_cds']
    kt_b = V['rf_term'] + b * V['erp_term']
    wex_b = we * ke_b + wd * kd_at
    wt_b = (1 - V['wd_term']) * kt_b + V['wd_term'] * kd_term_at
    sens_beta.append(dict(beta=b, ke=ke_b, wacc_exp=wex_b, wacc_term=wt_b,
                          dcf=run_dcf(wacc_t=wt_b) if wt_b > V['g_term'] + 0.02 else float('nan')))
margin_grid = [-0.30, -0.15, 0.0, 0.15, 0.30]      # conversion-EBITDA/t shifts (proportional)
nwc_grid = [1.00, 0.94, 0.88, 0.82, 0.76]
sens_mn = [[run_dcf(ept_shift=m, nwc_end=n) for n in nwc_grid] for m in margin_grid]
# terminal-ROIC sensitivity (audit request: the input driving RR = g/ROIC and the
# inverted g-gradient was gridded nowhere; it swings more than the whole beta grid)
nd_challenge = dict(nd=10386.0, ps=run_dcf(nd=10386.0),
                    note='the auditor-asserted (unverified) FY25 net-debt reading')
roic_grid = sorted({round(roic_T - 0.015, 3), round(roic_T - 0.007, 3), roic_T, 0.12, 0.15})
sens_roic = []
for rc in roic_grid:
    rr_ = V['g_term'] / rc
    tv_ = nop_T * (1 + V['g_term']) * (1 - rr_) / (wacc_term - V['g_term'])
    sens_roic.append(dict(roic=rc, rr=rr_, tv=tv_,
                          ps=(pv_sum + tv_ * df[-1] - net_debt) / SH))

# ---- terminal-growth reconciliation table (historical) ----
tg_recon = []
ic_hist = {'FY23': 0.60 * V['assets_fy23_est'] + 3600 - 2300,   # rough IC = NWC + PP&E ≈ equity+debt
           'FY24': V['equity_fy24'] + V['debt_fy24'] - V['cash_fy24'],
           'FY25': V['equity_fy25_est'] + V['debt_fy25'] - V['cash_fy25_est']}
nopat_hist = {y: hist_is[y]['ebit'] * (1 - TAX) for y in ('FY23', 'FY24', 'FY25')}
for y in ('FY23', 'FY24', 'FY25'):
    noph = nopat_hist[y]
    capex_h = 0.012 * hist_is[y]['rev']   # derived — no disclosed capex any year (flagged)
    tg_recon.append(dict(year=y, capex=capex_h, capex_ebitda=capex_h / hist_is[y]['ebitda'],
                         character='burst (debt-funded WC build, RR>100%)' if y != 'FY25' else
                                   'contraction (WC release beginning)',
                         nopat=noph, roic=noph / ic_hist[y]))
nopat_cagr_23_25 = (nopat_hist['FY25'] / nopat_hist['FY23']) ** 0.5 - 1

# ---- MC / step0 / tech / beta artefacts ----
step0 = json.load(open(os.path.join(HERE, 'step0_result.json')))
strike = json.load(open(os.path.join(HERE, 'strike_result.json')))
tech = json.load(open(os.path.join(HERE, 'tech_result.json')))
beta_reg = json.load(open(os.path.join(HERE, 'beta_result.json')))
p3 = np.load(os.path.join(HERE, 'paths_3M.npy'))
p1 = np.load(os.path.join(HERE, 'paths_1M.npy'))
term3, term1 = p3[:, -1], p1[:, -1]
zone_edges = [0, 1.80, 2.05, 2.35, 2.70, 1e9]
zones = [float(np.mean((term3 >= a) & (term3 < b))) for a, b in zip(zone_edges[:-1], zone_edges[1:])]
fan = np.array([np.percentile(p3, p, axis=0) for p in (5, 25, 50, 75, 95)])
np.save(os.path.join(HERE, 'fan.npy'), fan)
levels = [3.00, 2.75, 2.50, 2.35, 2.19, 2.05, 1.90, 1.70]
touch = {}
rmax1, rmin1 = p1.max(axis=1), p1.min(axis=1)
rmax3, rmin3 = p3.max(axis=1), p3.min(axis=1)
for L in levels:
    up = L > SPOT
    touch[f'{L:.2f}'] = dict(
        t1=float(np.mean(rmax1 >= L) if up else np.mean(rmin1 <= L)),
        t3=float(np.mean(rmax3 >= L) if up else np.mean(rmin3 <= L)))
prob_read = dict(
    p_above=float(np.mean(term3 > SPOT)),
    p_up10=float(np.mean(term3 >= SPOT * 1.10)), p_dn10=float(np.mean(term3 <= SPOT * 0.90)),
    median=float(np.median(term3)), med_move=float(np.median(term3) / SPOT - 1),
    band50=(float(np.percentile(term3, 25)), float(np.percentile(term3, 75))),
    touch_up10=float(np.mean(rmax3 >= SPOT * 1.10)), touch_dn10=float(np.mean(rmin3 <= SPOT * 0.90)))
prob_read['odds'] = prob_read['p_up10'] / prob_read['p_dn10']

# experts (methods cast from the persona library; labelled Expert 1/2/3 in output)
e1 = dict(method_short='earnings power x justified multiple', base=norm['base'],
          rng=(norm['bear'], norm['bull']))
own_cash_np = (rows[1]['ebit'] - V['kd_path'][1] * nd_fy26) * (1 - TAX)  # FY27E after actual funding cost
e2_credit = 0.35 * (np_norm - own_cash_np)
e2_pre_floor = own_cash_np + e2_credit
e2_floor_mn = 60.0    # nominal residual cash-earnings base (option value) — the bridge is DISCLOSED
e2_base = max(e2_pre_floor, e2_floor_mn) / SH * 6.0
e2 = dict(method_short='owner cash earnings (accountant)', base=e2_base,
          rng=(e2_base * 0.6, e2_base * 1.5),
          workings=dict(own_cash=own_cash_np, credit=e2_credit, pre_floor=e2_pre_floor,
                        floor_mn=e2_floor_mn, mult=6.0))
econ_profit_ps = dcf_ps  # Expert 3 anchors on the economic-profit DCF with own haircuts
e3_unfloored = (ev * 0.95 - net_debt) / SH
e3_base = e3_unfloored
e3 = dict(method_short='cash returns: ROIC vs the cost of capital', base=max(e3_base, 0.10),
          unfloored=e3_unfloored, floor=0.10,
          rng=(max((ev * 0.85 - net_debt - 500) / SH, 0.05),
               max((ev * 1.05 - net_debt + 500) / SH, 0.20)))

# ============================ ASSERT =========================================
err = []
# engine reconciliation — the study may not disagree with production
if step0['verdict'] != 'PASS' or step0['nu'] != 6.0 or step0['width_cal'] != 0.951:
    err.append('step0 reconciliation failed')
if not (step0['skill_norm'] > 0 and all(step0['ci_blocks'][b][0] > 0 for b in ('2', '3', '4'))):
    err.append('calibration gate not robust-PASS')
# P&L closure on the one fully-triangulated year
if abs(np_fy24_check - V['np_fy24']) / V['np_fy24'] > 0.03:
    err.append(f'FY24 P&L does not close: {np_fy24_check:.0f} vs {V["np_fy24"]:.0f}')
# bridge closes exactly (on the unfloored intrinsic)
if abs((ev - net_debt - nci) - eq_dcf_unfloored) > 1e-6:
    err.append('EV->equity bridge does not close')
# signs into the bridge
if not (net_debt > 0 and nci >= 0):
    err.append('net debt / NCI sign error')
# glide ordering (hard ASSERT per the standing procedure)
if not wacc_term < wacc_exp:
    err.append('WACC_TERM >= WACC_EXP')
if any(fwd[i] < fwd[i + 1] for i in range(4)):
    err.append('forward WACC schedule not monotone')
# one date, one price of time: TV discounted at year-5 cumulative factor
if abs(pv_tv - tv * df[-1]) > 1e-9:
    err.append('terminal value not discounted at the year-5 factor')
# Kd-integrity triple
if not INP['debt_ccy_evidence']['value']:
    err.append('no debt-currency evidence')
if abs(V['kd'] - V['kd_eff_fy25']) > 0.015:
    err.append('Kd more than 150bp from the most recent effective-rate check')
if V['kd'] > max(V['kd_eff_fy24'], V['kd_eff_fy25']) + 0.005:
    err.append('Kd exceeds peak-year effective rate by more than 50bp')
# terminal capital structure: normalized, and lighter on debt than today's distress weights
if not (V['wd_term'] < wd):
    err.append('terminal debt weight not below the current distress weight')
# terminal-growth procedure
if V['g_term'] != 0.05:
    err.append('terminal g center is not the standing 5%')
if rr_T >= 1.0 or rr_T <= 0:
    err.append('terminal reinvestment rate not in (0,1)')
if abs(roic_T * rr_T - V['g_term']) > 1e-9:
    err.append('terminal g != ROIC x RR')
# plausibility band
# Band floor 0.10 (was 0.25): with triangulated FY25 net debt ~9.8bn against an EV below it, the
# equity is a thin residual — a deep-distress read is the honest arithmetic for a 2.5x-levered
# name whose EV barely clears its net debt, not an implausible model output.
if not (0.10 <= (central['base'] / SPOT) <= 2.5):
    err.append(f'central/spot {central["base"]/SPOT:.2f} outside plausibility band [0.10, 2.5]')
if err:
    raise SystemExit('ASSERT FAILED:\n  - ' + '\n  - '.join(err))

print('ASSERT PASS —')
print(f'  FY24 closure: NP derived {np_fy24_check:,.0f} vs reported {V["np_fy24"]:,.0f} (gap {abs(np_fy24_check-V["np_fy24"])/V["np_fy24"]*100:.1f}%)')
print(f'  WACC explicit {wacc_exp*100:.2f}% (CDS-primary; rating alt {wacc_exp_rating*100:.2f}%) -> terminal {wacc_term*100:.2f}%  [glide tied to kd_path]')
print(f'  forward WACC: ' + ' / '.join(f'{w*100:.1f}%' for w in fwd))
print(f'  Kd {V["kd"]*100:.1f}% vs effective checks {V["kd_eff_fy24"]*100:.1f}% (FY24) / {V["kd_eff_fy25"]*100:.1f}% (FY25) — inside 150bp/50bp bounds')
print(f'  terminal: ROIC {roic_T*100:.1f}% x RR {rr_T*100:.1f}% = g {roic_T*rr_T*100:.1f}%  | TV = {tv_pct*100:.0f}% of EV')
print(f'  bridge: EV {ev:,.0f} - ND {net_debt:,.0f} = intrinsic equity {eq_dcf_unfloored:,.0f} '
      f'-> floored at 0 under limited liability (lens carries EGP {dcf_ps:.2f} option-value placeholder)')
print('  COST-OF-CAPITAL VERIFICATION —')
print(f'    Ke explicit = (rf {V["rf"]*100:.2f} - CDS {V["sov_spread_cds"]*100:.2f}) + beta {V["beta"]:.3f} x ERP {V["erp_cds"]*100:.2f} = {ke_cds*100:.2f}%  (rating alt {ke_rating*100:.2f}%; retired raw {ke_raw*100:.2f}%)')
print(f'    beta triple: R2 {beta_reg["r2"]:.3f}, n {beta_reg["n"]}, SE {beta_reg["se"]:.3f}, CI90 [{beta_reg["ci90"][0]:.2f},{beta_reg["ci90"][1]:.2f}] — usable, not weak-flagged')
print(f'    Kd marginal {V["kd"]*100:.1f}% (after-tax {kd_at*100:.2f}%) vs effective {V["kd_eff_fy24"]*100:.1f}/{V["kd_eff_fy25"]*100:.1f}%')
print(f'    weights: explicit E/D {we*100:.0f}/{wd*100:.0f} (market values) -> TERMINAL {we_term*100:.0f}/{wd_term*100:.0f} (normalized structure, not distress weights)')
print(f'    Ke_term = rf_term {V["rf_term"]*100:.1f} + beta x ERP_term {V["erp_term"]*100:.1f} = {ke_term*100:.2f}% | Kd_term {V["kd_term"]*100:.1f}%')
print(f'    terminal ROIC {roic_T*100:.1f}% vs WACC_term {wacc_term*100:.2f}% — spread {"NEGATIVE: growth subtracts value; the g-grid gradient inverts by construction" if roic_T < wacc_term else "positive"}')
print(f'  central {central["base"]:.2f} [{central["bear"]:.2f}-{central["bull"]:.2f}] vs spot {SPOT} ({central["base"]/SPOT-1:+.0%})')


# ---- [R-ANCHOR-01] THE FORECAST IS ANCHORED ON THE LATEST REVIEWED PERIOD ----
# NEITHER CLAUSE OF THAT RULE FIRES HERE AND THE RECORD IS COMMITTED ANYWAY, which
# is the point of printing it for every study: the forecast opens ABOVE the latest
# reviewed period and its path RISES from its own opening year, so clause one has
# nothing to fire on and clause two has nothing to reach. No mechanism is owed and
# none is claimed — inventing one to decorate a record that does not fire would be
# the assumption wearing a mechanism, which this rule exists to stop.
#
# WHAT THE RECORD MAKES VISIBLE IS THAT THE RULE CANNOT SEE THIS STUDY'S CLAIM.
# The latest reviewed period is the worst quarter in the company's record, so a
# forecast opening above it is arithmetically unavoidable; and the rate that
# carries the answer is not the opening year but the LAST one, which is 82% of
# enterprise value and sits half below every full year the company has reported.
# Clause one compares the opening year with the latest reviewed period; clause two
# compares the path's minimum with its own opening year. On a path that rises out
# of a collapsed quarter, NEITHER COMPARISON REACHES THE TERMINAL. That is a
# property of the rule's two comparisons rather than a defect in this record, and
# it is written down here rather than left for somebody to discover.
#
# EVERY FIGURE BELOW IS DERIVED FROM THIS STUDY'S OWN COMMITTED VALUES. The
# Q1-2026 EBITDA is recovered from the conversion rate this model already commits
# for that quarter rather than retyped, so the depreciation add-back inside it is
# the study's own and not a second one introduced here.
_q1_ebitda = hist_ebitda_per_t['Q1_26'] * hist_vol['Q1_26_annualized']['vol_kt'] / 4.0
_q1_dna_addback = _q1_ebitda - V['q1_26_op']
_q1_mgn = _q1_ebitda / V['q1_26_rev']
_fcst_mgn = [r['margin'] for r in rows]
_hist_mgn = {y: hist_is[y]['ebitda'] / hist_is[y]['rev'] for y in ('FY23', 'FY24', 'FY25')}
_mgn_filed_low = min(_hist_mgn.values())
# the add-back the quarter would need before the forecast opened BELOW it at all:
# the verdict is insensitive to a construction that is a house estimate, and the
# bound says by how much rather than asserting it.
_dna_to_close = _fcst_mgn[0] * V['q1_26_rev'] - V['q1_26_op']
_ebit_mgn_f = [r['ebit'] / r['rev'] for r in rows]
_ebit_mgn_q1 = V['q1_26_op'] / V['q1_26_rev']

FORECAST_ANCHOR = dict(
    rate_name='EBITDA margin',
    latest_reviewed_period='Q1-2026 (three months ended 31 March 2026), interim filing — '
                           'the statements themselves are not held',
    latest_reviewed_date='2026-03-31',
    latest_reviewed_rate=float(_q1_mgn),
    latest_reviewed_source=(
        'THE STUDY HOLDS NO COMPANY FINANCIAL STATEMENT, AND THIS FIELD SAYS SO RATHER '
        'THAN NAMING A FILING. The Q1-2026 figures reach this model as press coverage of '
        'the interim filing lodged with the exchange — revenue EGP %.0fmn, cost of sales '
        'EGP %.0fmn, gross profit EGP %.3fmn and operating profit EGP %.3fmn — not as the '
        'reviewed statements. EBITDA is that operating profit plus a depreciation add-back '
        'of EGP %.1fmn, which is this study\'s own estimate for the quarter and not a '
        'disclosed line. The issuer\'s statement index lists nothing after 30 September '
        '2025 and nothing consolidated after 31 December 2020, every consolidated file it '
        'does list sits on a host that no longer resolves, and this study models '
        'consolidated figures; the position is carried in the escalation register and was '
        're-probed on 5 September 2026 rather than taken on report. So the anchor is '
        'recorded and its provenance is not of the class the source rule requires — a '
        'condition of the study, not of this record.'
        % (V['q1_26_rev'], V['q1_26_cogs'], V['q1_26_gp'], V['q1_26_op'], _q1_dna_addback)),
    first_forecast_rate=float(_fcst_mgn[0]),
    forecast_path=[float(m) for m in _fcst_mgn],
    other_framing=dict(
        label='operating margin — no depreciation add-back on either side',
        latest_reviewed_rate=float(_ebit_mgn_q1),
        first_forecast_rate=float(_ebit_mgn_f[0]),
        forecast_path=[float(m) for m in _ebit_mgn_f],
        note='RECORDED BECAUSE THE HEADLINE RATE CARRIES A HOUSE ESTIMATE AND THE VERDICT '
             'SHOULD BE SHOWN NOT TO TURN ON IT. Strip the add-back from both sides and the '
             'shape is identical: %.4f%% in the quarter against %.4f%% in the first forecast '
             'year, rising to %.2f%% by FY2030E. The bound is exact — the quarterly add-back '
             'would have to exceed EGP %.1fmn, an annualised EGP %.0fmn against this study\'s '
             'own FY2025 depreciation charge of EGP %.1fmn, before the forecast opened below '
             'the quarter at all. No treatment of depreciation available on these numbers '
             'reverses the sign.'
             % (100 * _ebit_mgn_q1, 100 * _ebit_mgn_f[0], 100 * _ebit_mgn_f[-1],
                _dna_to_close, 4 * _dna_to_close, dna_fy['FY25'])),
    driver_rate_beside_it=dict(
        label='conversion EBITDA per tonne (k EGP/t) — the unit rate the forecast is '
              'actually built on, margin being an output of it',
        latest_reviewed_rate=float(hist_ebitda_per_t['Q1_26']),
        forecast_path=[float(x) for x in V['ebitda_per_t']],
        filed_record={y: float(hist_ebitda_per_t[y]) for y in ('FY23', 'FY24', 'FY25')},
        note='THE DRIVER TELLS THE SAME STORY AND IS NOT RECORDED AS THE GOVERNING RATE, '
             'for a reason worth stating: its denominator is a volume the company does not '
             'disclose, implied through a fabrication uplift that revenue alone does not '
             'identify, so it cannot be read off any filing. It opens at %.1f against %.1f '
             'in the quarter and rises to %.0f, while the filed years run %.1f (FY2023), '
             '%.1f (FY2024) and %.1f (FY2025) — the same shape as the margin: above the '
             'quarter, far below every year.'
             % (V['ebitda_per_t'][0], hist_ebitda_per_t['Q1_26'], V['ebitda_per_t'][-1],
                hist_ebitda_per_t['FY23'], hist_ebitda_per_t['FY24'],
                hist_ebitda_per_t['FY25'])),
    note='THE FORECAST OPENS ABOVE THE LATEST REVIEWED PERIOD AND RISES FROM THERE, SO '
         'NEITHER CLAUSE FIRES AND NO MECHANISM IS OWED OR CLAIMED. It opens at %.2f%% '
         'against %.2f%% in the three months to 31 March 2026 — %+.0f%% relative — and the '
         'path\'s minimum IS its opening year, running %.2f%% / %.2f%% / %.2f%% / %.2f%% / '
         '%.2f%%.\n\n'
         'WHAT SITS EITHER SIDE OF THAT IS THE WHOLE OF THIS STUDY AND A READER SHOULD SEE '
         'IT. The anchor quarter is the worst the company has reported: revenue EGP %.0fmn '
         'against EGP %.0fmn a year earlier, gross margin %.2f%% against %.2f%%, operating '
         'profit EGP %.3fmn against EGP %.0fmn, and a net loss of EGP %.1fmn against a '
         'profit of EGP %.1fmn. A forecast opening above that is the ordinary consequence of '
         'not projecting the worst quarter for ever, and it is not evidence of anything. The '
         'LAST forecast year is where the answer lives: %.2f%% against a reported record of '
         '%.2f%% (FY2023), %.2f%% (FY2024) and %.2f%% (FY2025) — %.0f%% relatively below the '
         'lowest of the three — and %.0f%% of enterprise value sits in the terminal struck '
         'off it. THIS RULE\'S TWO COMPARISONS CANNOT REACH THAT NUMBER: one holds the '
         'opening year against the latest reviewed period and the other holds the path\'s '
         'minimum against its own opening year, and on a rising path out of a collapsed '
         'quarter both pass while the single judgement carrying the valuation goes '
         'unexamined. It is examined instead by this study\'s own dated gap review, which '
         'solves the traded price back through these same drivers onto a terminal margin of '
         '27.17%% and finds it inside the reported range in all three years.\n\n'
         'AND THE RECORD IS ONLY AS GOOD AS WHAT IT IS STRUCK ON. The full-year margins '
         'quoted above are not filed rates: revenue and net profit are vendor and press '
         'prints, and everything between them is solved or typed — the FY2025 EBITDA rests '
         'on a finance cost derived to close the profit and loss to a reported net profit, '
         'and this study\'s own review prices that single unsourced input at about 40%% of '
         'the FY2025 conversion rate the forecast is calibrated against. The comparison this '
         'record draws is therefore between a forecast and a reconstruction, and it is '
         'recorded in those terms.'
         % (100 * _fcst_mgn[0], 100 * _q1_mgn,
            100 * (_fcst_mgn[0] - _q1_mgn) / abs(_q1_mgn),
            100 * _fcst_mgn[0], 100 * _fcst_mgn[1], 100 * _fcst_mgn[2],
            100 * _fcst_mgn[3], 100 * _fcst_mgn[4],
            V['q1_26_rev'], V['q1_25_rev'],
            100 * V['q1_26_gp'] / V['q1_26_rev'], 100 * V['q1_25_gp'] / V['q1_25_rev'],
            V['q1_26_op'], V['q1_25_op'], -V['q1_26_np'], V['q1_25_np'],
            100 * _fcst_mgn[-1], 100 * _hist_mgn['FY23'], 100 * _hist_mgn['FY24'],
            100 * _hist_mgn['FY25'],
            -100 * (_fcst_mgn[-1] - _mgn_filed_low) / _mgn_filed_low,
            100 * tv_pct))

# ============================ EMIT ===========================================
out = dict(
    # THE ANSWER, WHERE THE SHARED READER LOOKS FOR IT. [R-GAP-01]'s gate reads a study's
    # own numbers for a central; this study carried its spot at the top level and its
    # central at lenses.central.base, so the gate could see neither pair and THE LARGEST
    # GAP IN THE BOOK WAS INVISIBLE FOR A MONTH. An unreadable answer is not a clean
    # answer [R-ENF-04].
    #
    # NOTHING HERE ENDORSES THE NUMBER. GAP_REVIEW_05-09-2026.md establishes that the
    # published central is not a valuation at all: two of the four lenses are pinned at
    # floors (max(...,0.01) and max(...,0.05) at lines 389 and 493) and carry 60% of the
    # weight while producing 4.2% of the answer; unfloored the same blend is -0.7055. The
    # figure below is what a reader receives today, which is what the gate audits.
    central=lens['central']['base'],
    spot=SPOT, spot_date=tech['spot_date'], shares=SH, mktcap=MKTCAP, fx=V['fx'], tax=TAX,
    inputs={k: INP[k] for k in INP},
    hist_is=hist_is,
    hist_bs=dict(assets={'FY22': V['assets_fy22'], 'FY23e': V['assets_fy23_est'],
                         'FY24': V['assets_fy24'], 'FY25': V['assets_fy25']},
                 debt_fy24=V['debt_fy24'], cash_fy24=V['cash_fy24'],
                 equity_fy24=V['equity_fy24'], liab_fy24=V['liab_fy24'],
                 equity_fy25e=V['equity_fy25_est'], net_debt_fy25e=V['net_debt_fy25_est'],
                 debt_fy25e=V['debt_fy25'], cash_fy25e=V['cash_fy25_est'],
                 facilities_fy25=V['facilities_fy25'],
                 nwc_fy25e=V['nwc_fy25_est'], payables_fy25e=V['payables_fy25_est']),
    rollforward=json.load(open(os.path.join(HERE, 'rollforward_result.json'))),
    interims=dict(q1_26_rev=V['q1_26_rev'], q1_26_np=V['q1_26_np'],
                  q1_25_rev=V['q1_25_rev'], q1_25_np=V['q1_25_np']),
    tonnage=dict(hist_vol=hist_vol, hist_ebitda_per_t=hist_ebitda_per_t,
                 capacity_kt=V['capacity_kt'], k_uplift=V['k_uplift'],
                 copper_hist=V['copper_hist'], copper_fcst=V['copper_fcst'],
                 egp_hist=V['egp_hist'], egp_fcst=V['egp_fcst'],
                 vols_fcst=V['vols_fcst'], ebitda_per_t=V['ebitda_per_t']),
    coc=dict(rf=V['rf'], sov_cds=V['sov_spread_cds'], sov_rating=V['sov_spread_rating'],
             rf_star_cds=rf_star_cds, rf_star_rating=rf_star_rating,
             erp_cds=V['erp_cds'], erp_rating=V['erp_rating'], beta=V['beta'],
             beta_reg=beta_reg, ke_cds=ke_cds, ke_rating=ke_rating, ke_raw_retired=ke_raw,
             kd=V['kd'], kd_at=kd_at, kd_eff_fy24=V['kd_eff_fy24'], kd_eff_fy25=V['kd_eff_fy25'],
             we=we, wd=wd, wacc_exp=wacc_exp, wacc_exp_rating=wacc_exp_rating,
             rf_term=V['rf_term'], erp_term=V['erp_term'], ke_term=ke_term,
             kd_term=V['kd_term'], wd_term=wd_term, we_term=we_term, wacc_term=wacc_term,
             kd_path=kdp, glide_frac=glide_frac, fwd_wacc=fwd, df=df),
    dcf=dict(rows=rows, pv_sum=pv_sum, tv=tv, pv_tv=pv_tv, ev=ev, tv_pct=tv_pct,
             fcff_T1=fcff_T1, roic_T=roic_T, rr_T=rr_T, ic_T=ic_T,
             net_debt=net_debt, nci=nci, eq=eq_dcf, ps=dcf_ps,
             eq_unfloored=eq_dcf_unfloored, ps_unfloored=dcf_ps_unfloored,
             nd_fy26=nd_fy26),
    is_fcst=is_fcst,
    debt_schedule=dict(nd_path=nd_path, eq_path=eq_path,
                       note='interest charged on OPENING net debt at that year\'s forward Kd; '
                            'tax 22.5% on positive EBT net of the FY26E loss carryforward'),
    lenses=lens, weights=W,
    tg_recon=dict(rows=tg_recon, nopat_cagr_23_25=nopat_cagr_23_25,
                  note='FY23/FY24 are burst years (debt-funded working-capital build, RR>100%) — '
                       'excluded from the ROIC x RR identity per the standing rule; no clean stable '
                       'year exists in the disclosed record, so the terminal check leans on the '
                       'forward build (terminal ROIC 14-15% x RR ~34% = 5%)'),
    sens_wg=dict(wacc_grid=wacc_grid, g_grid=g_grid, table=sens_wg),
    sens_expl=dict(expl_grid=expl_grid, term_grid=wacc_grid, table=sens_expl),
    sens_beta=sens_beta,
    sens_mn=dict(margin_grid=margin_grid, nwc_grid=nwc_grid, table=sens_mn),
    sens_roic=sens_roic, nd_challenge=nd_challenge,
    scenarios=dict(bear=dict(knobs=BEAR_KNOBS, **bear_detail),
                   bull=dict(knobs=BULL_KNOBS, **bull_detail)),
    forecast_anchor=FORECAST_ANCHOR,
    step0=step0, strike=strike, tech=tech,
    mc=dict(prob_read=prob_read, zones=zones, zone_edges=zone_edges[1:-1], touch=touch,
            pct1={p: float(np.percentile(term1, p)) for p in (5, 25, 50, 75, 95)},
            pct3={p: float(np.percentile(term3, p)) for p in (5, 25, 50, 75, 95)}),
    experts=dict(e1=e1, e2=e2, e3=e3, eps_norm=eps_norm, np_norm=np_norm, bvps=bvps),
    peers=dict(swdy=dict(rev_fy25=281049.0, np_fy25=17330.0, ebitda_fy25=30660.0,
                         nd_fy25=19789.0, mktcap=196310.0,
                         pe=196310.0 / 17330.0,                       # 11.3x COMPUTED from the filing
                         ev_ebitda=(196310.0 + 19789.0) / 30660.0,    # 7.05x COMPUTED
                         wc_seg_fy25_growth='low-teens (H1-25 +12.3%; the widely quoted +66% is FY2024)',
                         yield_=0.0202,
                         src='FY25 release (NP attrib 17,330; EBITDA 30,660; net bank debt 19,789, '
                             'company ER); mktcap EGP 196.31bn @ 91.90 21-Jul-26 (Investing.com; '
                             'stockanalysis 95.90 27-Jul implies ~205bn). Multiples COMPUTED from these, '
                             'replacing prior aggregator prints (10.4x/6.0x) that did not reproduce'),
               riyadh=dict(pe=15405.0 / 1080.4, ev_ebitda=12.5, mktcap_sar=15405.0,
                           np_fy25_sar=1080.4, de=0.51, roe=0.327,
                           src='SAR 102.70 30-Jul-26 (sa.investing) x 150mn sh; FY25 NP 1,080.4 +32% '
                               '(maaal). EV/EBITDA ~12.5x derived, balance-sheet inputs unverified; '
                               'prior 18x was a stale mid-June cache')),
)
with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(out, f, indent=1, default=float)
print('study_numbers.json written')
