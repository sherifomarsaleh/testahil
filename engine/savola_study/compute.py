"""SAVOLA study — master computation. Writes study_numbers.json (single source of
truth for every builder). Code-first rule: INPUTS are four-field records
{value, source, date, ring}; a bare numeral cannot enter the model; the ASSERT
block raises (no JSON emitted) unless the bridge closes, the category builds foot
to the audited segment totals, and the terminal is ROIC-consistent.

BUILT 18-Aug-2026 on the company's own issued statements read from savola.com/
investors (COMPANY_OFFICIAL): FY2023 audited (KPMG-predecessor basis, 14-Mar-2024),
FY2024 audited (KPMG, 10-Mar-2025), FY2025 audited (Deloitte, unmodified,
authorized 05-Mar-2026), Q1-2026 reviewed interim FS (06-May-2026), the company's
own H1-2026 earnings release (06-Aug-2026) and the Q2-2026 / FY2025 investor
presentations (COMPANY_IR).

Company class: diversified consumer-staples OPERATING COMPANY (food processing +
grocery retail + QSR + frozen food; the Almarai-holding era ended with the 2024
capital reduction and in-kind distribution). Lens set follows the operating-
company reference (SWDY pattern inside the model-study skeleton): FCFF DCF
primary, relative multiples, normalized earnings power, and a book/ROE lens.
Leases are treated as DEBT throughout: FCFF charges a steady-state lease
replacement equal to right-of-use depreciation, the lease liability is netted in
the bridge at its audited balance, and lease debt carries its measured effective
rate inside the WACC.

THE CONTESTED JUDGEMENT (computed BOTH WAYS, per the dual-framing rule extended
to the study's central judgement): whether Panda's 20-store-per-year expansion
programme is value-ACCRETIVE or value-DILUTIVE. Framing A (base): sales density
stabilises as the CXR programme and e-commerce mature (sales-per-store decline
fades -6% -> -3% -> -1% -> 0%, and the store-opex ratio gains 10bp/yr of scale
from FY2028). Framing B: the measured H1-2026 density erosion persists
(-3%/yr forever) and the opex ratio never improves. Both fair values are
published side by side; they are never averaged.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np

# ============================ INPUTS =========================================
# All statement figures in SAR mn (audited statements print SAR'000; /1000 is a
# unit conversion, not a derivation). Volumes in thousand metric tonnes (k MT);
# per-tonne figures in SAR/tonne; per-share figures in SAR.
def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)

FS25 = ("Audited consolidated FS FY2025, savola.com/en/investors/financial-statements "
        "(Deloitte & Touche, unmodified opinion, authorized 05-Mar-2026)")
FS24 = ("Audited consolidated FS FY2024, savola.com (KPMG, 10-Mar-2025)")
FS23 = ("Audited consolidated FS FY2023, savola.com (auditor's report 14-Mar-2024)")
Q126 = ("Reviewed interim condensed consolidated FS, three months ended 31-Mar-2026, "
        "savola.com (review report 06-May-2026)")
H1REL = ("Company H1-2026 earnings release, savola.com/en/news-media, 06-Aug-2026 "
         "(COMPANY_OFFICIAL)")
IRQ2 = "Company Q2-2026 investor presentation, savola.com, Aug-2026 (COMPANY_IR)"
IRFY = "Company FY2025 investor presentation, savola.com, Mar-2026 (COMPANY_IR)"
ANNC = "Official Saudi Exchange announcement, saudiexchange.sa"

# ---------------------------------------------------------------------------
# PRE-PASS: every delta quoted in a register justification is computed here from
# the raw disclosed pair, never typed (DU edition-4 standing rule).
# ---------------------------------------------------------------------------
_OILV_H125, _OILV_H126 = 645.0, 749.0            # k MT, IRQ2 volume chart
_SUGV_H125, _SUGV_H126 = 968.0, 1038.0
_PASV_H125, _PASV_H126 = 135.0, 139.0
_OIL_GPT_H126 = 571.0 / 749.0 * 1000             # disclosed GP 571 on 749k MT
_SUG_GPT_H126 = 226.0 / 1038.0 * 1000
_PAS_GPT_H126 = 73.0 / 139.0 * 1000
_D_OILV = _OILV_H126 / _OILV_H125 - 1            # +16.12%
_D_SUGV = _SUGV_H126 / _SUGV_H125 - 1            # +7.23%
_D_PASV = _PASV_H126 / _PASV_H125 - 1            # +2.96%
_PANDA_SPS_H125 = 5852.0 / ((209.0 + 213.0) / 2)   # H1-25 revenue on avg store count
_PANDA_SPS_H126 = 5902.0 / ((227.0 + 231.0) / 2)   # H1-26
_D_PANDA_SPS = _PANDA_SPS_H126 / _PANDA_SPS_H125 - 1   # measured density change

INP = dict(
    # ---- anchors --------------------------------------------------------
    spot=I(25.30, "Uploaded Tadawul daily price history for SAVOLA (2050), last close "
           "18-Aug-2026", "2026-08-18", "Market"),
    shares_issued_mn=I(300.0, FS25 + ", note 16: share capital SAR 3bn = 300mn fully paid "
                       "shares of SAR 10, after the 2024 rights issue (+600mn shares) and the "
                       "capital reduction cancelling 833.98mn shares against the Almarai "
                       "in-kind distribution", "2026-03-05", "Company"),
    shares_wavg_mn=I(298.589, FS25 + ", note 31: weighted-average shares outstanding net of "
                     "1.411mn treasury shares under the employee share plan", "2026-03-05",
                     "Company"),
    anchor_days=I(230.0, "31-Dec-2025 valuation date to the 18-Aug-2026 price anchor",
                  "2026-08-18", "House"),
    div_between=I(1.70, "FY2025 dividend SAR 1.70/share (SAR 510mn, 17% of par), board-"
                  "recommended 05-Mar-2026 (" + ANNC + " anId 93503), EX-DATE 07-May-2026, "
                  "paid during H1-2026 (H1 release: 524 incl. NCI). Its ex-date falls between "
                  "the 31-Dec-2025 valuation date and the 18-Aug-2026 anchor, so every lens "
                  "rolled to the anchor must be ex this dividend", "2026-05-07", "Company"),

    # ---- historical income statement (SAR mn, consolidated, continuing) ----
    # FY2024 figures are the re-presented comparatives in the FY2025 statements
    # (Türkiye moved to discontinued), so FY2024 and FY2025 sit on one perimeter.
    # FY2023 is the re-presented comparative in the FY2024 statements (Iran and
    # Sudan discontinued) and still INCLUDES Türkiye — the one basis break in the
    # three-year table, flagged wherever the row is shown (Türkiye FY2024 revenue
    # was 941.1, note 22.2 of FY2025).
    rev_fy23=I(24149.521, FS24 + ", FY2023 comparative (continuing, incl. Türkiye)",
               "2025-03-10", "Company"),
    rev_fy24=I(23045.574, FS25 + ", FY2024 comparative (continuing, ex-Türkiye)",
               "2026-03-05", "Company"),
    rev_fy25=I(26081.053, FS25, "2026-03-05", "Company"),
    cogs_fy23=I(19103.682, FS24 + ", FY2023 comparative", "2025-03-10", "Company"),
    cogs_fy24=I(18212.904, FS25 + ", FY2024 comparative", "2026-03-05", "Company"),
    cogs_fy25=I(20992.159, FS25, "2026-03-05", "Company"),
    sda_fy23=I(2931.087, FS24 + ", FY2023 comparative, selling & distribution", "2025-03-10",
               "Company"),
    sda_fy24=I(2970.149, FS25 + ", FY2024 comparative", "2026-03-05", "Company"),
    sda_fy25=I(3199.605, FS25 + ", note 36", "2026-03-05", "Company"),
    adm_fy23=I(869.798, FS24 + ", FY2023 comparative, administrative", "2025-03-10", "Company"),
    adm_fy24=I(901.723, FS25 + ", FY2024 comparative", "2026-03-05", "Company"),
    adm_fy25=I(820.208, FS25 + ", note 37", "2026-03-05", "Company"),
    oth_fy23=I(-7.935, FS24 + ", FY2023 comparative, other operating (expense) net",
               "2025-03-10", "Company"),
    oth_fy24=I(1.040, FS25 + ", FY2024 comparative", "2026-03-05", "Company"),
    oth_fy25=I(91.832, FS25 + ", note 38 (incl. a 69.5 reversal of accruals no longer "
               "required — stripped from the recurring base below)", "2026-03-05", "Company"),
    dna_fy23=I(1064.590, FS24 + ", FY2023 segment note: continuing depreciation & "
               "amortisation", "2025-03-10", "Company"),
    dna_fy24=I(1099.866, FS25 + ", FY2024 segment note (continuing)", "2026-03-05", "Company"),
    dna_fy25=I(1190.022, FS25 + ", segment note 33 (continuing); cash-flow total incl. "
               "discontinued 1,198.4", "2026-03-05", "Company"),
    dna_own_fy25=I(608.933, FS25 + ", note 6: depreciation for the year on owned PP&E",
                   "2026-03-05", "Company"),
    dna_int_fy25=I(48.936, FS25 + ", note 8: amortisation of intangibles", "2026-03-05",
                   "Company"),
    assoc_fy25=I(51.775, FS25 + ": share of results of equity-accounted investees (Kinan), "
                 "net of zakat and tax", "2026-03-05", "Company"),
    fin_income_fy25=I(205.247, FS25 + ", note 41 (incl. one-off 49.7 put-settlement gain and "
                      "9.9 settlement discount)", "2026-03-05", "Company"),
    fin_cost_fy25=I(480.772, FS25 + ", note 41: borrowings 231.9 + leases 219.4 + bank "
                    "commission 14.2 + FX 9.5 + site-restoration unwind 5.8", "2026-03-05",
                    "Company"),
    pbt_fy25=I(861.708, FS25, "2026-03-05", "Company"),
    tax_fy25=I(131.049, FS25 + ", note 29: continuing income-tax expense (foreign "
               "subsidiaries)", "2026-03-05", "Company"),
    zakat_rev_fy25=I(-217.425, FS25 + ", note 29: net zakat REVERSAL — ZATCA final "
                     "assessment of 2024 released 247.3 of prior-year accruals", "2026-03-05",
                     "Company"),
    np_att_fy25=I(874.462, FS25 + ": profit attributable to owners", "2026-03-05", "Company"),
    np_att_fy24=I(9974.266, FS25 + ", FY2024 comparative (incl. the 11,554.7 Almarai "
                  "distribution gain)", "2026-03-05", "Company"),
    np_att_fy23=I(899.185, FS23 + " (original basis)", "2024-03-14", "Company"),
    eps_fy25=I(2.93, FS25 + ", note 31 (basic, total)", "2026-03-05", "Company"),
    recurring_np_fy25=I(539.1, IRFY + ": reported-to-recurring bridge (874.4 less zakat/"
                        "accrual reversals 300.0, Türkiye gain 32.3, put gain 40.2, plus "
                        "impairment 11.7 and other 32.7)", "2026-03-09", "Company"),
    recurring_np_fy24=I(295.5, IRFY + ", same bridge for FY2024", "2026-03-09", "Company"),

    # ---- historical balance sheet (SAR mn, audited) -----------------------
    ppe_fy25=I(5486.067, FS25, "2026-03-05", "Company"),
    ppe_fy24=I(5438.447, FS25 + ", comparative", "2026-03-05", "Company"),
    rou_fy25=I(3416.863, FS25, "2026-03-05", "Company"),
    intang_fy25=I(1408.747, FS25 + " (goodwill 956.3 gross in note 8)", "2026-03-05", "Company"),
    invprop_fy25=I(158.234, FS25, "2026-03-05", "Company"),
    kinan_carry=I(435.517, FS25 + ", note 10: Kinan 29.9%, equity method", "2026-03-05",
                  "Company"),
    kinan_share_na=I(600.925, FS25 + ", note 10.2: Group's 29.9% share of Kinan's net assets",
                     "2026-03-05", "Company"),
    kinan_profit_share_h126=I(34.0, H1REL + ": share of results from equity-accounted "
                              "investees H1-2026 (vs 18 in H1-2025), driven by Kinan",
                              "2026-08-06", "Company"),
    inv_nc_fy25=I(676.359, FS25 + ", note 11: MOF sukuk at amortised cost 524.8 (matures "
                  "26-Aug-2027) + FVOCI 151.6 (incl. quoted Almarai residual 131.6)",
                  "2026-03-05", "Company"),
    inv_c_fy25=I(85.802, FS25 + ", note 11: FVTPL 32.3 (Almarai ESOP shares) + T-bills/term "
                 "deposits 53.5", "2026-03-05", "Company"),
    inventories_fy25=I(4680.559, FS25 + ", note 12", "2026-03-05", "Company"),
    inventories_fy24=I(4171.221, FS25 + ", comparative", "2026-03-05", "Company"),
    tr_fy25=I(1856.697, FS25, "2026-03-05", "Company"),
    tr_fy24=I(1956.952, FS25 + ", comparative", "2026-03-05", "Company"),
    prepay_fy25=I(1346.504, FS25, "2026-03-05", "Company"),
    tp_fy25=I(3915.807, FS25, "2026-03-05", "Company"),
    tp_fy24=I(3679.328, FS25 + ", comparative", "2026-03-05", "Company"),
    accrued_fy25=I(2829.405, FS25, "2026-03-05", "Company"),
    contract_fy25=I(151.990, FS25, "2026-03-05", "Company"),
    cash_fy25=I(904.137, FS25 + ", note 15 (incl. <3-month deposits 306.7)", "2026-03-05",
                "Company"),
    loans_fy25=I(1893.924, FS25 + ", note 21: all current — unsecured bank loans 1,823.8 + "
                 "overdrafts 61.4 + accrued finance cost 8.7; zero long-term debt",
                 "2026-03-05", "Company"),
    loans_geo_sa=I(1256.382, FS25 + ", note 21 geographical analysis: Saudi Arabia",
                   "2026-03-05", "Company"),
    loans_geo_eg=I(417.192, FS25 + ", note 21: Egypt", "2026-03-05", "Company"),
    loans_geo_other=I(220.350, FS25 + ", note 21: Algeria 72.2 + UAE 148.2", "2026-03-05",
                      "Company"),
    leases_fy25=I(3952.231, FS25 + ", note 23 (non-current 3,446.1 + current 506.1)",
                  "2026-03-05", "Company"),
    lease_int_fy25=I(220.889, FS25 + ", note 23: interest expense for the year", "2026-03-05",
                     "Company"),
    lease_open_fy25=I(3593.097, FS25 + ", note 23: opening balance", "2026-03-05", "Company"),
    eb_fy25=I(748.401, FS25 + ": employee benefits liabilities (non-current)", "2026-03-05",
              "Company"),
    restor_fy25=I(164.946, FS25 + ": provision against asset restoration", "2026-03-05",
                  "Company"),
    equity_att_fy25=I(5516.027, FS25, "2026-03-05", "Company"),
    other_net_liab=I(332.716, FS25 + ": accrued income tax 134.125 + accrued zakat 112.265 "
                     "+ deferred tax liability 110.893 less deferred tax asset 2.628 less "
                     "other non-current assets 21.939 — the audited lines outside the "
                     "working-capital day build, held flat and deducted in the bridge",
                     "2026-03-05", "Company/derived"),
    nci_book_fy25=I(950.039, FS25 + ", note 20", "2026-03-05", "Company"),
    nci_herfy_book=I(434.618, FS25 + ", note 20: carrying amount of the 51% Herfy NCI",
                     "2026-03-05", "Company"),
    herfy_price=I(15.50, "Herfy Food Services (Tadawul 6002) close 18-Aug-2026, market data "
                  "(stockanalysis.com; cross-check quote — Herfy's own listing)", "2026-08-18",
                  "Market"),
    herfy_shares_mn=I(64.68, "Herfy shares outstanding, market data 18-Aug-2026", "2026-08-18",
                      "Market"),

    # ---- FY2025 category unit data (Food Processing) -----------------------
    oil_vol_fy25=I(1322.0, IRFY + ": oil volume FY2025 (Arabia 612 + other markets 710), "
                   "k MT", "2026-03-09", "Company"),
    oil_rev_fy25=I(7098.0, IRFY + ": oil revenue FY2025", "2026-03-09", "Company"),
    oil_gp_fy25=I(958.0, IRFY + ": oil gross profit FY2025 (GP/ton 724)", "2026-03-09",
                  "Company"),
    oil_ebitda_fy25=I(563.0, IRFY + ": oil EBITDA FY2025", "2026-03-09", "Company"),
    sug_vol_fy25=I(2162.0, IRFY + ": sugar volume FY2025 (KSA 1,186 + Egypt 975; FY2024 "
                   "comparative USCE-adjusted)", "2026-03-09", "Company"),
    sug_rev_fy25=I(4868.0, IRFY + ": sugar revenue FY2025", "2026-03-09", "Company"),
    sug_gp_fy25=I(413.0, IRFY + ": sugar gross profit FY2025 (GP/ton 191)", "2026-03-09",
                  "Company"),
    sug_ebitda_fy25=I(335.0, IRFY + ": sugar EBITDA FY2025", "2026-03-09", "Company"),
    pas_rev_fy25=I(545.0, IRFY + ": pasta revenue FY2025 (+3.2% on 528)", "2026-03-09",
                   "Company"),
    pas_gm_fy25=I(0.215, IRFY + ": pasta gross margin FY2025 21.5%", "2026-03-09", "Company"),
    pas_ebitda_mgn_fy25=I(0.135, IRFY + ": pasta EBITDA margin FY2025 13.5%", "2026-03-09",
                          "Company"),
    fp_segrev_fy25=I(13279.850, FS25 + ", note 33: Food Processing segment revenue (incl. "
                     "inter-segment 336.5)", "2026-03-05", "Company"),
    fp_cogs_fy25=I(11590.617, FS25 + ", note 33: Food Processing cost of revenues",
                   "2026-03-05", "Company"),
    ret_segrev_fy25=I(11327.912, FS25 + ", note 33: Retail segment revenue", "2026-03-05",
                      "Company"),
    ret_cogs_fy25=I(8435.273, FS25 + ", note 33", "2026-03-05", "Company"),
    fsv_segrev_fy25=I(1082.562, FS25 + ", note 33: Food Services (Herfy) segment revenue",
                      "2026-03-05", "Company"),
    frz_segrev_fy25=I(804.997, FS25 + ", note 33: Frozen Food segment revenue", "2026-03-05",
                      "Company"),
    elim_fy25=I(-443.246, FS25 + ", note 33: others / eliminations", "2026-03-05", "Company"),
    invseg_rev_fy25=I(28.978, FS25 + ", note 33: Investments segment revenue", "2026-03-05",
                      "Company"),

    # ---- H1-2026 actuals (the near-term anchors) ---------------------------
    h1_rev=I(13588.0, H1REL, "2026-08-06", "Company"),
    h1_ebitda=I(1316.0, H1REL + " (company basis: operating income before D&A, includes the "
                "34 share of associates)", "2026-08-06", "Company"),
    h1_np_att=I(401.0, H1REL + " (incl. +41 Sudan disposal gain net; recurring 372)",
                "2026-08-06", "Company"),
    h1_capex=I(385.0, H1REL, "2026-08-06", "Company"),
    h1_netdebt=I(851.0, H1REL + ": net debt at 30-Jun-2026 (company definition: loans and "
                 "overdrafts less cash; excludes leases and the 528 government sukuk)",
                 "2026-08-06", "Company"),
    h1_oil_vol=I(_OILV_H126, IRQ2 + f": oil volume H1-2026 749k MT vs 645 "
                 f"(computed {+_D_OILV:+.1%})", "2026-08-06", "Company"),
    h1_oil_rev=I(4172.0, IRQ2, "2026-08-06", "Company"),
    h1_oil_gp=I(571.0, IRQ2 + f" (computed GP/ton {_OIL_GPT_H126:,.0f})", "2026-08-06",
                "Company"),
    h1_sug_vol=I(_SUGV_H126, IRQ2 + f": sugar volume H1-2026 1,038k MT vs 968 "
                 f"(computed {+_D_SUGV:+.1%})", "2026-08-06", "Company"),
    h1_sug_rev=I(2113.0, IRQ2, "2026-08-06", "Company"),
    h1_sug_gp=I(226.0, IRQ2 + f" (computed GP/ton {_SUG_GPT_H126:,.0f})", "2026-08-06",
                "Company"),
    h1_pas_vol=I(_PASV_H126, IRQ2 + f": pasta volume H1-2026 139k MT vs 135 "
                 f"(computed {+_D_PASV:+.1%})", "2026-08-06", "Company"),
    h1_pas_rev=I(292.0, IRQ2, "2026-08-06", "Company"),
    h1_pas_gp=I(73.0, IRQ2 + f" (computed GP/ton {_PAS_GPT_H126:,.0f})", "2026-08-06",
                "Company"),
    h1_nuts_rev=I(337.0, IRQ2 + ": Bayara UAE 278 + KSA 59", "2026-08-06", "Company"),
    h1_panda_rev=I(5902.0, H1REL, "2026-08-06", "Company"),
    h1_panda_ebitda=I(524.0, H1REL, "2026-08-06", "Company"),
    h1_panda_gm=I(0.232, IRQ2 + ": Panda gross margin H1-2026 23.2% (presentation basis)",
                  "2026-08-06", "Company"),
    h1_herfy_rev=I(516.0, H1REL, "2026-08-06", "Company"),
    h1_herfy_ebitda=I(96.0, H1REL + " (18.7% margin)", "2026-08-06", "Company"),
    h1_frz_rev=I(411.0, H1REL, "2026-08-06", "Company"),
    h1_frz_ebitda=I(56.0, H1REL + " (13.7% margin)", "2026-08-06", "Company"),
    h1_unalloc_cash=I(64.0, IRQ2 + ": unallocated costs H1-2026, cash-based (Arabia 74 + "
                      "Egypt 39 gross; 64 net cash per the net-income bridge)", "2026-08-06",
                      "Company"),
    stores_end24=I(209.0, IRFY + ": Panda store network at Dec-2024 (227 at Dec-2025 after "
                   "+20 openings and 2 closures)", "2026-03-09", "Company"),
    stores_end25=I(227.0, IRFY, "2026-03-09", "Company"),
    stores_jun26=I(231.0, IRQ2 + ": 231 stores at Jun-2026 (+6 opened, 2 closed in H1); "
                   "225 KSA + 6 Egypt; 170 super + 61 hyper; NSA 583k m2", "2026-08-06",
                   "Company"),
    h1_panda_rev_h125=I(5852.0, IRQ2 + ": Panda H1-2025 revenue (restated comparative); "
                        f"computed sales-per-average-store change H1-26 vs H1-25 = "
                        f"{_D_PANDA_SPS:+.1%}", "2026-08-06", "Company"),

    # ---- forecast drivers (each with its evidence and its named mechanism) --
    oil_vol_g=I([0.125, 0.04, 0.03, 0.025, 0.02],
                "FY2026E +12.5% = H1 actual +16.1% carried at a moderated +9% H2 (B2B wins "
                "annualise; Algeria record volumes); then fading to market growth. Mechanism: "
                "company-reported share gains and exports, not price", "2026-08-18", "House"),
    oil_rpt_g=I([0.005, 0.015, 0.015, 0.01, 0.01],
                "revenue/ton: H1-2026 5,570 vs H1-2025 5,416 (+2.8% computed); FY26E +0.5% on "
                "the FY25 base then +1-1.5%/yr pass-through of the FAO veg-oil rise (Jul-2026 "
                "index highest since Jun-2022)", "2026-08-18", "House"),
    oil_gpt_path=I([740.0, 745.0, 745.0, 745.0, 745.0],
                   "GP/ton: FY25 724, H1-2026 actual 762; FY26E 740 = H1 762 blended with a "
                   "replacement-cost-squeezed H2 (company's own Q3/Q4 warning + FAO); held "
                   "745 after — the observed improvement is NOT projected further (no "
                   "measured mechanism)", "2026-08-18", "House"),
    sug_vol_g=I([0.055, 0.025, 0.02, 0.02, 0.015],
                "FY2026E +5.5% = H1 actual +7.2% with +4% H2; then 1.5-2.5% (KSA demand + "
                "Egypt supply resilience per company disclosures)", "2026-08-18", "House"),
    sug_rpt_g=I([-0.075, 0.005, 0.005, 0.005, 0.005],
                "revenue/ton: H1-2026 2,036 vs FY25 2,252 computed (-9.6%); FY26E -7.5% on "
                "the FY25 base (soft world sugar, FAO -8% y/y; committed refined-sales book "
                "1,044mn on 544k t = 1,918/t at Dec-25); flat-to-+0.5% after", "2026-08-18",
                "House"),
    sug_gpt_path=I([215.0, 212.0, 212.0, 212.0, 212.0],
                   "GP/ton: FY25 191, H1-2026 actual 218 (KSA margin recovery + Egypt); FY26E "
                   "215, then 212 — holds most of the measured gain without projecting more",
                   "2026-08-18", "House"),
    pas_vol_fy25=I(268.0, "DERIVED (flagged): FY2025 pasta volume = disclosed revenue 545 / "
                   "implied revenue-per-tonne 2,034 (H1-2026 2,101 and H1-2025 2,052 disclosed "
                   "pairs; FY25 midpoint) — the presentation discloses H1 volumes but not the "
                   "FY total", "2026-08-18", "House/derived"),
    pas_vol_g=I([0.03, 0.03, 0.025, 0.02, 0.02],
                "H1-2026 actual +3.0% (computed) carried, wheat-cost tailwind supporting "
                "competitiveness", "2026-08-18", "House"),
    pas_rpt_g=I([0.02, 0.01, 0.01, 0.01, 0.01],
                "revenue/ton +2% FY26E (H1-2026 2,101 vs H1-2025 2,052 = +2.4% computed), "
                "then +1%", "2026-08-18", "House"),
    pas_gpt_path=I([520.0, 520.0, 520.0, 520.0, 520.0],
                   "GP/ton: H1-2026 actual 525 (73/139); FY25 ~437 implied; held at 520 — "
                   "the wheat/packaging tailwind the company names is retained, not amplified",
                   "2026-08-18", "House"),
    nuts_rev_path=I([730.0, 800.0, 848.0, 890.0, 926.0],
                    "FY25 base 769 (residual of the four categories against the audited FP "
                    "segment revenue); H1-2026 337 (-6.9% y/y computed) with the Mehbaj "
                    "bolt-on from Jul-2026 (consideration undisclosed — dated negative "
                    "search; modelled as a modest KSA revenue step +40 in H2-26E, +8.5% "
                    "FY27E, then +5%) — flagged as the least-anchored revenue line",
                    "2026-08-18", "House"),
    nuts_gm_path=I([0.265, 0.27, 0.27, 0.27, 0.27],
                   "FY25 residual category GM 26.1% (segment-note GP less the three "
                   "disclosed categories); H1-2026 blended 29.9% disclosed; forward 26.5-27% "
                   "— direction supported by the measured UAE margin and the Mehbaj/Jeddah "
                   "integration, size capped", "2026-08-18", "House"),
    fp_opex_ratio=I(dict(oil=0.0556, sugar=0.0160, pasta=0.0790, nuts=0.2350),
                    "per-category (GP - EBITDA)/revenue measured FY2025: oil (958-563)/7,098; "
                    "sugar (413-335)/4,868; pasta (21.5%-13.5%); nuts residual (201-20)/769 — "
                    "held flat: opex scales with revenue, margins stay OUTPUTS", "2026-03-09",
                    "Company/derived"),
    stores_path=I([247.0, 267.0, 285.0, 300.0, 312.0],
                  "company guidance 20+ stores/yr (Q2-2026 presentation 2026 target; AR2025); "
                  "tapering to +12 by FY2030", "2026-08-06", "Company/House"),
    sps_g_A=I([-0.06, -0.03, -0.01, 0.0, 0.0],
              "FRAMING A sales-per-average-store path: measured H1-2026 density change "
              f"{_D_PANDA_SPS:+.1%} carried into FY26E, fading as CXR (149 stores done) and "
              "e-commerce (~2.5x) mature", "2026-08-18", "House"),
    sps_g_B=I([-0.06, -0.03, -0.03, -0.03, -0.03],
              "FRAMING B: the measured erosion never fades — competition and small-format "
              "mix keep density falling 3%/yr", "2026-08-18", "House"),
    panda_gm=I(0.232, "Panda gross margin held at the H1-2026 actual 23.2% (presentation "
               "basis) — Q4 seasonality helps but promo intensity offsets; no uplift "
               "projected", "2026-08-06", "Company/House"),
    panda_opex_ratio=I(0.143, "store opex / revenue = measured H1-2026 GM 23.2% less EBITDA "
                       "margin 8.9%; held flat in Framing A until FY2028 then -10bp/yr of "
                       "scale; flat forever in Framing B", "2026-08-06", "Company/derived"),
    herfy_rev_g=I([-0.045, 0.0, 0.02, 0.02, 0.02],
                  "H1-2026 actual -6.8%; FY26E -4.5% (softer H2 comps), stabilising then +2% "
                  "— no turnaround projected beyond the company's own cost actions",
                  "2026-08-18", "House"),
    herfy_ebitda_mgn=I(0.185, "H1-2026 actual 18.7% held at 18.5% (post-IFRS16 margin; the "
                       "cost programme's gain retained, not extended)", "2026-08-06",
                       "Company/House"),
    frz_rev_g=I([0.01, 0.035, 0.035, 0.03, 0.03],
                "H1-2026 -1.4% with a stronger Q2; FY26E +1% (H2 recovery per company), then "
                "3-3.5% B2B/food-service growth", "2026-08-18", "House"),
    frz_ebitda_mgn=I(0.137, "H1-2026 actual 13.7% held", "2026-08-06", "Company/House"),
    elim_ratio=I(-0.0334, "eliminations / FP segment revenue measured FY2025 (-443.2 / "
                 "13,279.9); held proportional", "2026-03-05", "Company/derived"),
    unalloc_path=I([130.0, 133.0, 136.0, 139.0, 142.0],
                   "unallocated corporate costs: 2x the H1-2026 cash-based 64, growing ~2%/yr "
                   "(Saudi CPI)", "2026-08-06", "Company/House"),
    invseg_rev=I(29.0, "Investments segment rental/other revenue held at the FY2025 29.0",
                 "2026-03-05", "Company"),

    # ---- capex / D&A / leases ------------------------------------------------
    capex_path=I([810.0, 900.0, 880.0, 860.0, 850.0],
                 "FY26E 810 = H1 actual 385 + H2 at the FY25 H2 run-rate + Panda openings; "
                 "FY27E 900 (new Jeddah nuts facility + refinery upgrades per AR2025 + 20 "
                 "stores), easing to 850; FY25 actual was 858 (Panda 567, Foods 231) and "
                 "capital commitments 425 stood at Dec-25", "2026-08-18", "House"),
    dep_rate_own=I(0.112, "owned-PP&E depreciation rate on opening NBV, measured FY2025: "
                   "608.9 / 5,438.4 opening", "2026-03-05", "Company/derived"),
    int_amort=I(50.0, "intangibles amortisation ~ FY2025 actual 48.9, held", "2026-03-05",
                "Company/derived"),
    rou_dna_fy25=I(532.153, "right-of-use depreciation FY2025 = segment D&A 1,190.0 less "
                   "owned 608.9 less intangibles 48.9 (all audited components)", "2026-03-05",
                   "Company/derived"),
    rou_growth=I([0.05, 0.045, 0.04, 0.035, 0.03],
                 "right-of-use charge grows with the Panda store network (leases are "
                 "store-driven: Panda holds 2.9bn of the 3.7bn group lease book per the "
                 "Q2-2026 presentation)", "2026-08-06", "Company/House"),
    lease_rate=I(0.0586, "effective lease interest rate = FY2025 interest 220.9 / average "
                 "lease liability (3,593.1 + 3,952.2)/2", "2026-03-05", "Company/derived"),

    # ---- working capital (component days, audited) ---------------------------
    dio_fy25=I(81.4, "days inventory = 4,680.6 / 20,992.2 x 365 (FY2025 audited)",
               "2026-03-05", "Company/derived"),
    dso_fy25=I(26.0, "days sales = 1,856.7 / 26,081.1 x 365", "2026-03-05", "Company/derived"),
    dpo_fy25=I(68.1, "days payable = 3,915.8 / 20,992.2 x 365", "2026-03-05",
               "Company/derived"),
    prepay_ratio=I(0.0516, "prepayments & other receivables / revenue FY2025", "2026-03-05",
                   "Company/derived"),
    accrued_ratio=I(0.1085, "accrued & other liabilities / revenue FY2025", "2026-03-05",
                    "Company/derived"),
    contract_ratio=I(0.0058, "contract liabilities / revenue FY2025", "2026-03-05",
                     "Company/derived"),

    # ---- tax / payout --------------------------------------------------------
    tax_rate=I(0.195, "combined zakat + income tax on profit: FY2023 17.6% (228.5/1,299.0), "
               "FY2025 normalized ~18.7% (tax 131.0 + underlying zakat ~30 on PBT 861.7), "
               "Q1-2026 20.5% (70.0/341.6) -> 19.5% held flat and sensitized", "2026-08-18",
               "House"),
    payout=I(0.55, "stated dividend policy 'approximately 50% to 60% of net profit annually' "
             "(" + ANNC + " anId 93503, 08-Mar-2026); midpoint 55% drives the forecast "
             "dividend and cash walk", "2026-03-08", "Company"),

    # ---- cost of capital (v2 method, both ERP bases) -------------------------
    ust10=I(0.0468, "US 10Y constant maturity 4.68%, FRED DGS10, 14-Aug-2026", "2026-08-14",
            "Global"),
    ust1=I(0.0398, "US 1Y constant maturity 3.98%, FRED DGS1, 14-Aug-2026", "2026-08-14",
           "Global"),
    ksa_usd10_spread=I(0.0085, "Saudi sovereign USD 10Y new-issue spread +85bp over UST "
                       "(USD 11.5bn 4-tranche jumbo, Jan-2026; Emirates NBD Research note "
                       "06-Jan-2026)", "2026-01-06", "Country"),
    sar_1y_obs=I(0.0470, "observed 1Y SAR sovereign rate: NDMC 'Sah' savings sukuk fixed "
                 "annual return 4.70%, Aug-2026 subscription (NDMC announcement via Arab "
                 "News 02-Aug-2026)", "2026-08-02", "Country"),
    rf_observed=I(0.0553, "CONSTRUCTED 10Y SAR proxy (flagged; direct SAR 10Y quote "
                  "inaccessible this session — investing.com/WGB/TradingEconomics/spglobal/"
                  "cbonds all walled, NDMC publishes tranche sizes not yields): UST10Y 4.68% "
                  "(FRED 14-Aug-2026) + 0.85% Saudi Jan-2026 USD 10Y new-issue spread = "
                  "5.53%, cross-checked against the observed 1Y SAR 4.70% = UST1Y + 72bp "
                  "(the peg keeps the SAR curve near the sovereign USD curve); WACC "
                  "sensitivity to +/-50bp is published", "2026-08-14", "Country"),
    sov_spread_rating=I(0.0051, "Damodaran ctryprem.html (original file, 'last updated "
                        "January 5, 2026'): Saudi Arabia Aa3, adjusted default spread 0.51%",
                        "2026-01-05", "Country"),
    erp_rating=I(0.0501, "Damodaran same file: Saudi Arabia total ERP 5.01% (CRP 0.78%)",
                 "2026-01-05", "Country"),
    sov_spread_cds=I(0.0098, "Damodaran same file: Saudi sovereign CDS 0.98%", "2026-01-05",
                     "Country"),
    erp_cds=I(0.0572, "Damodaran same file: ERP on the CDS basis 5.72%", "2026-01-05",
              "Country"),
    beta=I(1.087, "tier-1 own-stock beta: 5y weekly Dimson regression of SAVOLA vs TASI "
           "(engine registry copy of the exchange's published index, as-of 18-Aug-2026): "
           "beta 1.087, R2 0.159, n 254, SE 0.215, CI90 [0.73, 1.44]; produced by the "
           "sanctioned beta_regression.own_stock_beta() and attested by "
           "assert_beta_provenance(); Blume cross-check 1.058", "2026-08-18", "Market"),
    saibor3m=I(0.0474, "3M SAIBOR 4.74% (Jun-2026, TradingEconomics market data — labelled "
               "cross-check level for the SAR marginal cost of debt)", "2026-06-30", "Market"),
    kd_sar=I(0.0574, "marginal SAR cost of debt = 3M SAIBOR 4.74% + ~100bp murabaha spread "
             "on Savola's sharia-compliant facilities (1.3bn of the book, note 21.1); sits "
             "above the 1Y sovereign 4.70% as it must", "2026-08-18", "House"),
    kd_eg_localeq=I(0.065, "EGP tranche (417.2 of 1,893.9) at SAR-equivalent cost: under "
                    "covered interest parity the 25-27% EGP nominal cost converts to the SAR "
                    "rate + Egypt credit/liquidity spread; carried at 6.5% (SAR marginal + "
                    "~75bp) — NOT the raw EGP coupon, which would misstate a SAR-nominal "
                    "WACC", "2026-08-18", "House"),
    kd_other=I(0.055, "AED/DZD minor tranches (220.4) at ~5.5% local-equivalent",
               "2026-08-18", "House"),
    g_term=I(0.025, "terminal growth 2.5% = Saudi CPI 1.8% (GASTAT Jul-2026) + ~0.7% real "
             "staples growth; below nominal GDP", "2026-08-14", "House"),
    roic_term=I(0.105, "terminal ROIC 10.5%: above the 8.5% terminal WACC (brands, shelf "
                "position) but far below the current oil-cycle segment returns; drives "
                "terminal reinvestment = g / ROIC", "2026-08-18", "House"),
    tw_e=I(0.65, "terminal equity weight 65% (explicit-window market weights re-based to "
           "the model's own equity value; leases stay a structural 25-27% of capital for a "
           "leased-store retailer)", "2026-08-18", "House"),
    tw_loans=I(0.08, "terminal loans weight 8%", "2026-08-18", "House"),

    # ---- relative / normalized lens inputs -----------------------------------
    peer_pe=I(dict(ALMARAI=19.7, OTHAIM=19.4, BINDAWOOD=19.8, NADEC=13.0, WILMAR=12.4),
              "TTM P/E, market data 18-Aug-2026 (stockanalysis.com): Almarai 19.7, Al Othaim "
              "19.4, BinDawood 19.8, NADEC 13.0, Wilmar (international analogue) 12.4; "
              "cross-check only, never a build source", "2026-08-18", "Market"),
    pe_mix_w_fp=I(0.55, "EBITDA-mix weight of the processing/frozen leg for the peer-mix "
                  "multiple: FY2025 category EBITDA (oil 563 + sugar 335 + pasta ~74 + nuts "
                  "~20 + Kabeer ~110) over the group total ex-unallocated", "2026-03-09",
                  "Company/derived"),
    pe_discount=I(0.20, "conglomerate / EM-mix discount applied to the peer-mix P/E: ~21% of "
                  "revenue is Egypt (Caa1 sovereign) and the group stacks a holding level "
                  "over four operating legs; 20% base, published undiscounted alongside and "
                  "sensitized 10-30%", "2026-08-18", "House"),
    norm_ebitda_mgn=I(0.092, "normalized mid-cycle operating EBITDA margin 9.2% (ex-"
                      "associates): inside the observed FY2023-FY2025 envelope 8.9%-9.5% "
                      "(computed on the model's own basis) and between FY2025's 9.0% and the "
                      "H1-2026 ~9.4% restated level", "2026-08-18", "House"),
    nci_share=I(0.070, "non-controlling interests' share of group profit, measured FY2025: "
                "66.0 / 940.5 (audited P&L); held flat — Herfy's 51% NCI absorbs its losses, "
                "SFC/GFC minorities take their profit shares", "2026-03-05",
                "Company/derived"),
    kinan_g=I(0.03, "growth on Kinan's contribution off the annualized H1-2026 actual "
              "(34 x 2): ~3%/yr with Saudi real estate; falsified by Kinan's own results",
              "2026-08-18", "House"),
    kinan_div=I(25.116, "cash dividend received from Kinan FY2025 (note 10.1); grows with "
                "kinan_g in the cash walk — the share of profit itself is non-cash",
                "2026-03-05", "Company"),
    panda_scale_step=I(0.001, "Framing A store-opex scale gain: -10bp/yr from FY2028 as CXR "
                       "conversions and e-commerce density mature; ZERO in Framing B",
                       "2026-08-18", "House"),
    rec_g_fy26=I(0.15, "recurring-earnings step FY2025 -> FY2026E for the sustainable-ROE "
                 "lens: H1-2026 recurring +40% y/y moderated to +15% for the full year "
                 "(H2 replacement-cost squeeze); feeds roe_sust only", "2026-08-18", "House"),
)

# ============================ CALC ===========================================
V = {k: r['value'] for k, r in INP.items()}
Y = [2026, 2027, 2028, 2029, 2030]
say = print

# ---- historical operating EBITDA (model basis: ex-associates, ex-impairments) --
def op_ebitda(rev, cogs, sda, adm, oth, dna):
    return rev - cogs - sda - adm + oth + dna

EBITDA_H = dict(
    FY23=op_ebitda(V['rev_fy23'], V['cogs_fy23'], V['sda_fy23'], V['adm_fy23'],
                   V['oth_fy23'], V['dna_fy23']),
    FY24=op_ebitda(V['rev_fy24'], V['cogs_fy24'], V['sda_fy24'], V['adm_fy24'],
                   V['oth_fy24'], V['dna_fy24']),
    FY25=op_ebitda(V['rev_fy25'], V['cogs_fy25'], V['sda_fy25'], V['adm_fy25'],
                   V['oth_fy25'], V['dna_fy25']),
)
GP_H = dict(FY23=V['rev_fy23'] - V['cogs_fy23'], FY24=V['rev_fy24'] - V['cogs_fy24'],
            FY25=V['rev_fy25'] - V['cogs_fy25'])

# FY2025 category cross-foot: the four categories must reproduce the audited FP segment
nuts_rev_fy25 = V['fp_segrev_fy25'] - V['oil_rev_fy25'] - V['sug_rev_fy25'] - V['pas_rev_fy25']
fp_gp_fy25 = V['fp_segrev_fy25'] - V['fp_cogs_fy25']
pas_gp_fy25 = V['pas_rev_fy25'] * V['pas_gm_fy25']
nuts_gp_fy25 = fp_gp_fy25 - V['oil_gp_fy25'] - V['sug_gp_fy25'] - pas_gp_fy25
assert abs(nuts_rev_fy25 - 768.85) < 1.0, nuts_rev_fy25
assert nuts_gp_fy25 > 0, "residual nuts GP must be economically possible"
nuts_gm_fy25 = nuts_gp_fy25 / nuts_rev_fy25

# ============================ SEGMENT BUILD ==================================
def build(oil_gpt_shift=0.0, sug_gpt_shift=0.0, sps_variant='A', panda_opex_flat=False,
          vol_mult=1.0, capex_mult=1.0, gm_panda_shift=0.0):
    """Full five-year segment build. Returns dict of paths (SAR mn)."""
    # --- Food Processing: category volume x price x GP/ton ---
    oil_v, sug_v, pas_v = [], [], []
    oil_rpt, sug_rpt, pas_rpt = [], [], []
    v_o, v_s, v_p = V['oil_vol_fy25'], V['sug_vol_fy25'], V['pas_vol_fy25']
    r_o = V['oil_rev_fy25'] / V['oil_vol_fy25'] * 1000.0     # SAR/t
    r_s = V['sug_rev_fy25'] / V['sug_vol_fy25'] * 1000.0
    r_p = V['pas_rev_fy25'] / V['pas_vol_fy25'] * 1000.0
    for i in range(5):
        v_o *= (1 + V['oil_vol_g'][i] * vol_mult)
        v_s *= (1 + V['sug_vol_g'][i] * vol_mult)
        v_p *= (1 + V['pas_vol_g'][i] * vol_mult)
        r_o *= (1 + V['oil_rpt_g'][i]); r_s *= (1 + V['sug_rpt_g'][i])
        r_p *= (1 + V['pas_rpt_g'][i])
        oil_v.append(v_o); sug_v.append(v_s); pas_v.append(v_p)
        oil_rpt.append(r_o); sug_rpt.append(r_s); pas_rpt.append(r_p)
    oil_rev = [v * r / 1000.0 for v, r in zip(oil_v, oil_rpt)]
    sug_rev = [v * r / 1000.0 for v, r in zip(sug_v, sug_rpt)]
    pas_rev = [v * r / 1000.0 for v, r in zip(pas_v, pas_rpt)]
    nuts_rev = list(V['nuts_rev_path'])
    oil_gp = [v * (g + oil_gpt_shift) / 1000.0 for v, g in zip(oil_v, V['oil_gpt_path'])]
    sug_gp = [v * (g + sug_gpt_shift) / 1000.0 for v, g in zip(sug_v, V['sug_gpt_path'])]
    pas_gp = [v * g / 1000.0 for v, g in zip(pas_v, V['pas_gpt_path'])]
    nuts_gp = [r * g for r, g in zip(nuts_rev, V['nuts_gm_path'])]
    opx = V['fp_opex_ratio']
    oil_eb = [g - r * opx['oil'] for g, r in zip(oil_gp, oil_rev)]
    sug_eb = [g - r * opx['sugar'] for g, r in zip(sug_gp, sug_rev)]
    pas_eb = [g - r * opx['pasta'] for g, r in zip(pas_gp, pas_rev)]
    nuts_eb = [g - r * opx['nuts'] for g, r in zip(nuts_gp, nuts_rev)]
    fp_rev = [a + b + c + d for a, b, c, d in zip(oil_rev, sug_rev, pas_rev, nuts_rev)]
    fp_gp = [a + b + c + d for a, b, c, d in zip(oil_gp, sug_gp, pas_gp, nuts_gp)]
    fp_eb = [a + b + c + d for a, b, c, d in zip(oil_eb, sug_eb, pas_eb, nuts_eb)]

    # --- Retail (Panda): stores x sales/store; margin as OUTPUT ---
    sps_g = V['sps_g_A'] if sps_variant == 'A' else V['sps_g_B']
    sps = V['ret_segrev_fy25'] / ((V['stores_end24'] + V['stores_end25']) / 2.0)
    stores_prev = V['stores_end25']
    pan_rev, pan_eb, pan_gp = [], [], []
    opex_ratio = V['panda_opex_ratio']
    for i in range(5):
        sps *= (1 + sps_g[i])
        avg_stores = (stores_prev + V['stores_path'][i]) / 2.0
        rev = avg_stores * sps
        gm = V['panda_gm'] + gm_panda_shift
        if (not panda_opex_flat) and sps_variant == 'A' and i >= 2:
            opex_ratio = opex_ratio - V['panda_scale_step']
        gp = rev * gm
        pan_rev.append(rev); pan_gp.append(gp); pan_eb.append(gp - rev * opex_ratio)
        stores_prev = V['stores_path'][i]

    # --- Food Services (Herfy) and Frozen (Al Kabeer) ---
    her_rev, frz_rev = [], []
    hr, fr = V['fsv_segrev_fy25'], V['frz_segrev_fy25']
    for i in range(5):
        hr *= (1 + V['herfy_rev_g'][i]); fr *= (1 + V['frz_rev_g'][i])
        her_rev.append(hr); frz_rev.append(fr)
    her_eb = [r * V['herfy_ebitda_mgn'] for r in her_rev]
    frz_eb = [r * V['frz_ebitda_mgn'] for r in frz_rev]

    # --- group ---
    elim = [r * V['elim_ratio'] for r in fp_rev]
    rev = [a + b + c + d + e + V['invseg_rev'] for a, b, c, d, e in
           zip(fp_rev, pan_rev, her_rev, frz_rev, elim)]
    ebitda = [a + b + c + d - u for a, b, c, d, u in
              zip(fp_eb, pan_eb, her_eb, frz_eb, V['unalloc_path'])]
    return dict(oil_v=oil_v, sug_v=sug_v, pas_v=pas_v, oil_rev=oil_rev, sug_rev=sug_rev,
                pas_rev=pas_rev, nuts_rev=nuts_rev, oil_gp=oil_gp, sug_gp=sug_gp,
                pas_gp=pas_gp, nuts_gp=nuts_gp, oil_eb=oil_eb, sug_eb=sug_eb, pas_eb=pas_eb,
                nuts_eb=nuts_eb, fp_rev=fp_rev, fp_gp=fp_gp, fp_eb=fp_eb, pan_rev=pan_rev,
                pan_gp=pan_gp, pan_eb=pan_eb, her_rev=her_rev, her_eb=her_eb,
                frz_rev=frz_rev, frz_eb=frz_eb, elim=elim, rev=rev, ebitda=ebitda,
                capex=[c * capex_mult for c in V['capex_path']])

B = build()

# ---- D&A from asset roll-forwards -------------------------------------------
# Convention (stated in the workbook): intangible capex equals intangible
# amortisation (the book stays flat), so owned-PP&E capex = capex path - amort.
def dna_paths(capex):
    ppe = V['ppe_fy25']
    own, intang, rou, ppe_path = [], [], [], []
    rd = V['rou_dna_fy25']
    for i in range(5):
        d = ppe * V['dep_rate_own']
        own.append(d)
        ppe = ppe + (capex[i] - V['int_amort']) - d
        ppe_path.append(ppe)
        intang.append(V['int_amort'])
        rd = rd * (1 + V['rou_growth'][i])
        rou.append(rd)
    return own, intang, rou, ppe_path

OWN_D, INT_D, ROU_D, PPE_PATH = dna_paths(B['capex'])
DNA = [a + b + c for a, b, c in zip(OWN_D, INT_D, ROU_D)]

# ---- working capital (component days held at FY2025) -------------------------
def wc_path(rev, ebitda):
    cogs_ratio = 1 - (GP_H['FY25'] / V['rev_fy25'])   # COGS/revenue held at FY2025
    nwc, prev = [], None
    nwc0 = (V['inventories_fy25'] + V['tr_fy25'] + V['prepay_fy25'] - V['tp_fy25']
            - V['accrued_fy25'] - V['contract_fy25'])
    prev = nwc0
    dwc = []
    for i in range(5):
        cogs = rev[i] * cogs_ratio
        w = (cogs * V['dio_fy25'] / 365.0 + rev[i] * V['dso_fy25'] / 365.0
             + rev[i] * V['prepay_ratio'] - cogs * V['dpo_fy25'] / 365.0
             - rev[i] * V['accrued_ratio'] - rev[i] * V['contract_ratio'])
        nwc.append(w); dwc.append(w - prev); prev = w
    return nwc0, nwc, dwc

NWC0, NWC, DWC = wc_path(B['rev'], B['ebitda'])

# ---- FCFF waterfall -----------------------------------------------------------
T = V['tax_rate']
EBIT = [e - d for e, d in zip(B['ebitda'], DNA)]
NOPAT = [e * (1 - T) for e in EBIT]
FCFF = [n + d - c - r - w for n, d, c, r, w in
        zip(NOPAT, DNA, B['capex'], ROU_D, DWC)]
# lease replacement = right-of-use depreciation (steady state); owned capex separate

# ---- cost of capital: v2, both ERP bases --------------------------------------
rf_star_rating = V['rf_observed'] - V['sov_spread_rating']
rf_star_cds = V['rf_observed'] - V['sov_spread_cds']
ke_rating = rf_star_rating + V['beta'] * V['erp_rating']
ke_cds = rf_star_cds + V['beta'] * V['erp_cds']
w_sa = V['loans_geo_sa'] / V['loans_fy25']
w_eg = V['loans_geo_eg'] / V['loans_fy25']
w_ot = V['loans_geo_other'] / V['loans_fy25']
kd_loans = w_sa * V['kd_sar'] + w_eg * V['kd_eg_localeq'] + w_ot * V['kd_other']
kd_lease = V['lease_rate']
mktcap = V['spot'] * V['shares_issued_mn']
EV_w = mktcap + V['loans_fy25'] + V['leases_fy25']
we = mktcap / EV_w
wl = V['loans_fy25'] / EV_w
wz = V['leases_fy25'] / EV_w
wacc_exp = we * ke_rating + wl * kd_loans * (1 - T) + wz * kd_lease * (1 - T)
wacc_exp_cds = we * ke_cds + wl * kd_loans * (1 - T) + wz * kd_lease * (1 - T)
tw_lease = 1 - V['tw_e'] - V['tw_loans']
wacc_term = (V['tw_e'] * ke_rating + V['tw_loans'] * kd_loans * (1 - T)
             + tw_lease * kd_lease * (1 - T))
wacc_term_cds = (V['tw_e'] * ke_cds + V['tw_loans'] * kd_loans * (1 - T)
                 + tw_lease * kd_lease * (1 - T))

# ---- DCF and the EV -> equity bridge ------------------------------------------
def dcf(fcff, nopat, wacc_e, wacc_t, g, roic):
    dfs = [(1 + wacc_e) ** -(i + 1) for i in range(5)]
    pv_exp = sum(f * d for f, d in zip(fcff, dfs))
    reinvest = g / roic
    fcff_t = nopat[-1] * (1 + g) * (1 - reinvest)
    tv = fcff_t / (wacc_t - g)
    pv_tv = tv * dfs[-1]
    return pv_exp, tv, pv_tv, dfs, fcff_t

PV_EXP, TV, PV_TV, DFS, FCFF_T = dcf(FCFF, NOPAT, wacc_exp, wacc_term, V['g_term'],
                                     V['roic_term'])
EV_OP = PV_EXP + PV_TV
TV_SHARE = PV_TV / EV_OP

# non-operating assets at the 31-Dec-2025 valuation date
kinan_capitalized = (V['kinan_profit_share_h126'] * 2.0) / ke_rating
NONOP = V['inv_nc_fy25'] + V['inv_c_fy25'] + kinan_capitalized + V['invprop_fy25']
# NCI at value: Herfy 51% at its own market price; other NCI at book
herfy_mktcap = V['herfy_price'] * V['herfy_shares_mn']
nci_herfy_mkt = 0.51 * herfy_mktcap
nci_other_book = V['nci_book_fy25'] - V['nci_herfy_book']
NCI_VAL = nci_herfy_mkt + nci_other_book

def bridge(ev):
    """Enterprise value -> equity attributable, one definition used everywhere."""
    return (ev + NONOP + V['cash_fy25'] - V['loans_fy25'] - V['leases_fy25'] - V['eb_fy25']
            - V['restor_fy25'] - V['other_net_liab'] - NCI_VAL)

EQ = bridge(EV_OP)
PS_DEC = EQ / V['shares_wavg_mn']

def to_anchor(v):
    roll = (1 + ke_rating) ** (V['anchor_days'] / 365.0)
    return (v * roll - V['div_between'], roll)

PS, ROLL = to_anchor(PS_DEC)

# ---- THE CONTESTED JUDGEMENT, COMPUTED BOTH WAYS ------------------------------
def full_value(**kw):
    b = build(**kw)
    own, intd, roud, _ = dna_paths(b['capex'])
    dna = [a + x + c for a, x, c in zip(own, intd, roud)]
    _, _, dwc = wc_path(b['rev'], b['ebitda'])
    ebit = [e - d for e, d in zip(b['ebitda'], dna)]
    nopat = [e * (1 - T) for e in ebit]
    fcff = [n + d - c - r - w for n, d, c, r, w in
            zip(nopat, dna, b['capex'], roud, dwc)]
    pv_e, tv_, pv_t, _, _ = dcf(fcff, nopat, wacc_exp, wacc_term, V['g_term'],
                                V['roic_term'])
    ev = pv_e + pv_t
    eq = bridge(ev)
    ps_dec = eq / V['shares_wavg_mn']
    return to_anchor(ps_dec)[0], b, ev

PS_A = PS                                       # Framing A is the base build
PS_B, B_B, EV_B = full_value(sps_variant='B', panda_opex_flat=True)

# ---- scenarios (bear / bull on the DCF) ---------------------------------------
PS_BEAR, _, _ = full_value(oil_gpt_shift=-40.0, sug_gpt_shift=-15.0, sps_variant='B',
                           panda_opex_flat=True, vol_mult=0.5)
PS_BULL, _, _ = full_value(oil_gpt_shift=+25.0, sug_gpt_shift=+10.0, vol_mult=1.2,
                           gm_panda_shift=0.004)

# ---- forward profit / dividend / balance-sheet walk (Framing A) ---------------
# Closed double-entry system (the balance sheet foots by construction; asserted):
#   NP_total = (EBIT + NF) x (1-T) + KINAN   (associates are already net of tax)
#   NP_att   = (EBIT + NF) x (1-T) x (1-s) + KINAN     s = NCI profit share
#   cash_t   = cash_{t-1} + CFO - capex - lease principal - dividends (att + NCI)
#   leases and the right-of-use book grow together on the store-driven path;
#   lease principal paid = right-of-use depreciation; new leases are non-cash.
NCI_SHARE = V['nci_share']
KINAN = [V['kinan_profit_share_h126'] * 2 * (1 + V['kinan_g']) ** i for i in range(5)]
KINAN_DIV = [V['kinan_div'] * (1 + V['kinan_g']) ** i for i in range(5)]
NF, NP, NP_NCI, DIV, DIV_NCI, NDEBT, LEASEB = [], [], [], [], [], [], []
CASH_P, EQ_ATT_P, NCI_P, KINAN_BV, ROU_P, CFO_P = [], [], [], [], [], []
nd = V['loans_fy25'] - V['cash_fy25'] - V['inv_c_fy25']   # company-style net debt (ex sukuk)
cash = V['cash_fy25']
lease_bal = V['leases_fy25']
rou_bv = V['rou_fy25']
eq_att = V['equity_att_fy25']
nci_bv = V['nci_book_fy25']
kin_bv = V['kinan_carry']
for i in range(5):
    fin_cost = max(nd, 0.0) * kd_loans + lease_bal * kd_lease
    fin_inc = max(-nd, 0.0) * V['sar_1y_obs']
    nf = fin_inc - fin_cost
    core = (EBIT[i] + nf) * (1 - T)
    npatt = core * (1 - NCI_SHARE) + KINAN[i]
    npnci = core * NCI_SHARE
    NF.append(nf); NP.append(npatt); NP_NCI.append(npnci)
    DIV.append(npatt * V['payout']); DIV_NCI.append(npnci * V['payout'])
    cfo = core + DNA[i] - DWC[i] + KINAN_DIV[i]
    CFO_P.append(cfo)
    cash = cash + cfo - B['capex'][i] - ROU_D[i] - DIV[i] - DIV_NCI[i]
    CASH_P.append(cash)
    dlease = lease_bal * V['rou_growth'][i]
    lease_bal += dlease
    rou_bv += dlease
    LEASEB.append(lease_bal); ROU_P.append(rou_bv)
    eq_att = eq_att + npatt - DIV[i]
    nci_bv = nci_bv + npnci - DIV_NCI[i]
    kin_bv = kin_bv + KINAN[i] - KINAN_DIV[i]
    EQ_ATT_P.append(eq_att); NCI_P.append(nci_bv); KINAN_BV.append(kin_bv)
    nd = V['loans_fy25'] - cash - V['inv_c_fy25']
    NDEBT.append(nd)

# balance-sheet foot: assets less liabilities less equity == 0 in every year
for i in range(5):
    assets = (PPE_PATH[i] + ROU_P[i] + V['intang_fy25'] + V['invprop_fy25'] + KINAN_BV[i]
              + V['inv_nc_fy25'] + V['inv_c_fy25'] + NWC[i] + CASH_P[i])
    liabs = (V['loans_fy25'] + LEASEB[i] + V['eb_fy25'] + V['restor_fy25']
             + V['other_net_liab'])
    gap = assets - liabs - EQ_ATT_P[i] - NCI_P[i]
    assert abs(gap) < 1e-6, (i, gap)

# ---- lens 2: relative (peer-mix multiple, computed — never typed) --------------
eps_f = [n / V['shares_wavg_mn'] for n in NP]
_pe = V['peer_pe']
pe_fp_leg = float(np.median([_pe['NADEC'], _pe['WILMAR']]))        # processing analogues
pe_ret_leg = float(np.median([_pe['OTHAIM'], _pe['BINDAWOOD']]))   # Saudi grocery pair
pe_mix = V['pe_mix_w_fp'] * pe_fp_leg + (1 - V['pe_mix_w_fp']) * pe_ret_leg
pe_applied = pe_mix * (1 - V['pe_discount'])
rel_base = pe_applied * eps_f[0]
rel_bear = pe_mix * (1 - 0.30) * eps_f[0]
rel_bull = pe_mix * (1 - 0.10) * eps_f[0]
# DDM-justified P/E from the study's own Ke/payout/growth — the crosswalk that
# §4 uses to reconcile the DCF with the peer-implied value (computed, not typed)
_g_e = (NP[-1] / NP[0]) ** 0.25 - 1
_divs = [V['payout'] * (1 + _g_e) ** t for t in range(1, 6)]
_pe_ddm = (sum(d / (1 + ke_rating) ** t for d, t in zip(_divs, range(1, 6)))
           + (V['payout'] * (1 + _g_e) ** 5 * (1 + V['g_term']) / (ke_rating - V['g_term']))
           / (1 + ke_rating) ** 5)

# ---- lens 3: normalized earnings power -----------------------------------------
rev_mid = B['rev'][1]
np_norm = (((rev_mid * V['norm_ebitda_mgn'] - DNA[1]) + NF[1]) * (1 - T) * (1 - NCI_SHARE)
           + KINAN[1])
eps_norm = np_norm / V['shares_wavg_mn']
norm_base = eps_norm * pe_applied
norm_bear = eps_norm * pe_mix * (1 - 0.30)
norm_bull = eps_norm * pe_mix * (1 - 0.10)

# ---- lens 4: book / justified P/B ----------------------------------------------
bvps = V['equity_att_fy25'] / V['shares_wavg_mn']
roe_sust = (V['recurring_np_fy25'] * (1 + V['rec_g_fy26'])) / V['equity_att_fy25']
pb_just = (roe_sust - V['g_term']) / (ke_rating - V['g_term'])
book_base = bvps * pb_just
book_bear = bvps * max(pb_just - 0.15, 0.5)
book_bull = bvps * (pb_just + 0.15)

# ---- synthesis -----------------------------------------------------------------
W_L = dict(dcf=0.45, relative=0.25, normalized=0.15, book=0.15)
CENTRAL = (W_L['dcf'] * PS_A + W_L['relative'] * rel_base + W_L['normalized'] * norm_base
           + W_L['book'] * book_base)
PANEL = float(np.median([PS_A, rel_base, norm_base, book_base]))

# ---- sensitivity grids ----------------------------------------------------------
def dcf_at(wacc_e_, wacc_t_, g_):
    pv_e, _, pv_t, _, _ = dcf(FCFF, NOPAT, wacc_e_, wacc_t_, g_, V['roic_term'])
    ev = pv_e + pv_t
    eq = bridge(ev)
    ps_dec = eq / V['shares_wavg_mn']
    return ps_dec * ROLL - V['div_between']   # roll at the base Ke: the grid varies WACC/g only

WACC_GRID = [wacc_exp - 0.01, wacc_exp - 0.005, wacc_exp, wacc_exp + 0.005, wacc_exp + 0.01]
G_GRID = [0.015, 0.02, 0.025, 0.03, 0.035]
SENS = [[dcf_at(w, wacc_term + (w - wacc_exp), g) for g in G_GRID] for w in WACC_GRID]

def dcf_beta(b_):
    ke_ = rf_star_rating + b_ * V['erp_rating']
    we_ = we
    wacc_e_ = we_ * ke_ + wl * kd_loans * (1 - T) + wz * kd_lease * (1 - T)
    wacc_t_ = (V['tw_e'] * ke_ + V['tw_loans'] * kd_loans * (1 - T)
               + tw_lease * kd_lease * (1 - T))
    pv_e, _, pv_t, _, _ = dcf(FCFF, NOPAT, wacc_e_, wacc_t_, V['g_term'], V['roic_term'])
    ev = pv_e + pv_t
    eq = bridge(ev)
    roll_ = (1 + ke_) ** (V['anchor_days'] / 365.0)
    return eq / V['shares_wavg_mn'] * roll_ - V['div_between']

BETA_GRID = {round(b_, 3): dcf_beta(b_) for b_ in
             [0.73, 0.90, 1.00, V['beta'], 1.20, 1.44]}

def dcf_rf(rf_):
    rs = rf_ - V['sov_spread_rating']
    ke_ = rs + V['beta'] * V['erp_rating']
    wacc_e_ = we * ke_ + wl * kd_loans * (1 - T) + wz * kd_lease * (1 - T)
    wacc_t_ = (V['tw_e'] * ke_ + V['tw_loans'] * kd_loans * (1 - T)
               + tw_lease * kd_lease * (1 - T))
    pv_e, _, pv_t, _, _ = dcf(FCFF, NOPAT, wacc_e_, wacc_t_, V['g_term'], V['roic_term'])
    ev = pv_e + pv_t
    eq = bridge(ev)
    roll_ = (1 + ke_) ** (V['anchor_days'] / 365.0)
    return eq / V['shares_wavg_mn'] * roll_ - V['div_between']

RF_ALTS = {'5.03%': dcf_rf(0.0503), '5.53% (base)': dcf_rf(0.0553), '6.03%': dcf_rf(0.0603)}

# ---- CDS-basis DCF (published beside the rating basis, never averaged) ---------
pv_e_cds, _, pv_t_cds, _, _ = dcf(FCFF, NOPAT, wacc_exp_cds, wacc_term_cds, V['g_term'],
                                  V['roic_term'])
ev_cds = pv_e_cds + pv_t_cds
eq_cds = bridge(ev_cds)
PS_CDS = eq_cds / V['shares_wavg_mn'] * (1 + ke_cds) ** (V['anchor_days'] / 365.0) - V['div_between']

# ============================ EXPERT PANEL ===================================
# Three genuinely different methods, every intermediate line kept for App C.
# ---- Expert 1: sum-of-the-parts on segment EV/EBITDA multiples ----------------
# Lease-INCLUSIVE EBITDA carries lease-inclusive EV multiples: 6.5x processing
# (Wilmar-area), 7.0x Saudi grocery (BinDawood-area), 7.0x frozen. The frame
# deliberately imports the market's cheaper implied capital — that is its point,
# and its falsifier.
E1_MULT = dict(fp=6.5, retail=7.0, frozen=7.0)
e1_fp_ev = B['fp_eb'][0] * E1_MULT['fp']
e1_ret_ev = B['pan_eb'][0] * E1_MULT['retail']
e1_frz_ev = B['frz_eb'][0] * E1_MULT['frozen']
e1_herfy = 0.49 * herfy_mktcap                    # Savola's 49% of Herfy at ITS OWN market price
e1_unalloc_cap = -V['unalloc_path'][0] * E1_MULT['fp']
e1_ev = e1_fp_ev + e1_ret_ev + e1_frz_ev + e1_unalloc_cap
e1_eq = (e1_ev + e1_herfy + NONOP + V['cash_fy25'] - V['loans_fy25'] - V['leases_fy25']
         - V['eb_fy25'] - V['restor_fy25'] - V['other_net_liab']
         - (NCI_VAL - nci_herfy_mkt))
e1_ps_dec = e1_eq / V['shares_wavg_mn']
e1_base = to_anchor(e1_ps_dec)[0]
e1_lo = to_anchor((e1_eq - (B['fp_eb'][0] + B['pan_eb'][0] + B['frz_eb'][0]) * 0.75)
                  / V['shares_wavg_mn'])[0]        # three-quarters of a turn lower
e1_hi = to_anchor((e1_eq + (B['fp_eb'][0] + B['pan_eb'][0] + B['frz_eb'][0]) * 0.75)
                  / V['shares_wavg_mn'])[0]

# ---- Expert 2: two-stage dividend model on the stated 50-60% policy -----------
e2_dps = [DIV[i] / V['shares_wavg_mn'] for i in range(5)]
e2_pv_divs = sum(d / (1 + ke_rating) ** (t + 1) for t, d in enumerate(e2_dps))
e2_tv = e2_dps[-1] * (1 + V['g_term']) / (ke_rating - V['g_term'])
e2_pv_tv = e2_tv / (1 + ke_rating) ** 5
e2_ps_dec = e2_pv_divs + e2_pv_tv
e2_base = to_anchor(e2_ps_dec)[0]
e2_lo = to_anchor(sum(d * (V['payout'] and 0.50 / V['payout']) / (1 + ke_rating) ** (t + 1)
                      for t, d in enumerate(e2_dps))
                  + e2_tv * (0.50 / V['payout']) / (1 + ke_rating) ** 5)[0]
e2_hi = to_anchor(sum(d * (0.60 / V['payout']) / (1 + ke_rating) ** (t + 1)
                      for t, d in enumerate(e2_dps))
                  + e2_dps[-1] * (0.60 / V['payout']) * (1 + 0.03) / (ke_rating - 0.03)
                  / (1 + ke_rating) ** 5)[0]

# ---- Expert 3: residual income / economic profit ------------------------------
IC0 = (V['equity_att_fy25'] + V['nci_book_fy25'] + V['loans_fy25'] + V['leases_fy25']
       - V['cash_fy25'] - V['inv_c_fy25'] - V['inv_nc_fy25'] - V['kinan_carry'])
IC_PATH, RI_PATH = [], []
ic = IC0
for i in range(5):
    ri = NOPAT[i] - wacc_exp * ic
    RI_PATH.append(ri)
    reinv = B['capex'][i] + ROU_D[i] + DWC[i] - DNA[i]
    ic = ic + reinv
    IC_PATH.append(ic)
# fade the year-5 spread to zero over 5 more years (economic-profit decay)
ri5 = RI_PATH[-1]
e3_pv_ri = sum(r_ / (1 + wacc_exp) ** (t + 1) for t, r_ in enumerate(RI_PATH))
e3_fade = sum(ri5 * (1 - (t + 1) / 5.0) / (1 + wacc_exp) ** (5 + t + 1) for t in range(5))
e3_ev = IC0 + e3_pv_ri + e3_fade
e3_eq = (e3_ev + NONOP + V['kinan_carry'] + V['cash_fy25'] + V['inv_c_fy25'] * 0.0
         - V['loans_fy25'] - V['leases_fy25'] - V['eb_fy25'] - V['restor_fy25'] - V['other_net_liab'] - NCI_VAL)
e3_ps_dec = e3_eq / V['shares_wavg_mn']
e3_base = to_anchor(e3_ps_dec)[0]
e3_lo = to_anchor((IC0 + e3_pv_ri + NONOP + V['kinan_carry'] + V['cash_fy25']
                   - V['loans_fy25'] - V['leases_fy25'] - V['eb_fy25'] - V['restor_fy25']
                   - NCI_VAL) / V['shares_wavg_mn'])[0]     # no fade tail at all
e3_hi = to_anchor((IC0 + e3_pv_ri + e3_fade + ri5 * 0.4 / (wacc_exp)
                   / (1 + wacc_exp) ** 10 + NONOP + V['kinan_carry'] + V['cash_fy25']
                   - V['loans_fy25'] - V['leases_fy25'] - V['eb_fy25'] - V['restor_fy25']
                   - NCI_VAL) / V['shares_wavg_mn'])[0]     # 40% of the spread persists

EXPERTS = dict(
    e1=dict(base=e1_base, rng=[e1_lo, e1_hi], method_short='segment sum-of-the-parts',
            detail=dict(fp_ev=e1_fp_ev, ret_ev=e1_ret_ev, frz_ev=e1_frz_ev,
                        herfy_49=e1_herfy, unalloc=e1_unalloc_cap, ev=e1_ev, eq=e1_eq,
                        ps_dec=e1_ps_dec, mults=E1_MULT)),
    e2=dict(base=e2_base, rng=[e2_lo, e2_hi], method_short='two-stage dividend model',
            detail=dict(dps=e2_dps, pv_divs=e2_pv_divs, tv=e2_tv, pv_tv=e2_pv_tv,
                        ps_dec=e2_ps_dec)),
    e3=dict(base=e3_base, rng=[e3_lo, e3_hi], method_short='residual income / economic profit',
            detail=dict(ic0=IC0, ri=RI_PATH, ic=IC_PATH, pv_ri=e3_pv_ri, fade=e3_fade,
                        ev=e3_ev, eq=e3_eq, ps_dec=e3_ps_dec)),
)
PANEL_MED = float(np.median([e1_base, e2_base, e3_base]))

# ============================ ASSERTS ========================================
# bridge closes
_eq_chk = bridge(EV_OP)
assert abs(_eq_chk - EQ) < 1e-6
# category revenues foot to the audited FP segment revenue in the base year
_fp0 = V['oil_rev_fy25'] + V['sug_rev_fy25'] + V['pas_rev_fy25'] + nuts_rev_fy25
assert abs(_fp0 - V['fp_segrev_fy25']) < 0.5, _fp0
# category GP foots to the audited FP gross profit
_gp0 = V['oil_gp_fy25'] + V['sug_gp_fy25'] + pas_gp_fy25 + nuts_gp_fy25
assert abs(_gp0 - fp_gp_fy25) < 0.5, _gp0
# FY2026E must sit ABOVE the H1-2026 actual for revenue (H2 cannot be negative)
assert B['rev'][0] > V['h1_rev'], (B['rev'][0], V['h1_rev'])
# implied H2-2026E revenue within a sane band of H2-2025 actual (=FY25 - H1-25 13,080)
_h2_26 = B['rev'][0] - V['h1_rev']
_h2_25 = V['rev_fy25'] - 13080.0
assert 0.9 < _h2_26 / _h2_25 < 1.15, (_h2_26, _h2_25)
# terminal must be ROIC-consistent and ordered
assert V['roic_term'] > wacc_term > V['g_term']
assert wacc_term > wacc_exp - 0.02
# EBITDA margin path stays inside the observed historical envelope +/- 150bp
for i in range(5):
    m = B['ebitda'][i] / B['rev'][i]
    assert 0.075 < m < 0.115, (i, m)
# Framing A must exceed Framing B (the accretive framing is the upside by construction)
assert PS_A > PS_B
# lens sanity
assert 0.5 < pb_just < 1.5
# discount factors compound
assert all(DFS[i] > DFS[i + 1] for i in range(4))

# ============================ EMIT ===========================================
OUT = dict(
    meta=dict(
        ticker='SAVOLA', exchange='TADAWUL', code='2050', market='SA', currency='SAR',
        spot=V['spot'], spot_date='2026-08-18', shares_mn=V['shares_issued_mn'],
        shares_wavg_mn=V['shares_wavg_mn'], mktcap=mktcap,
        valuation_date='2025-12-31', anchor_date='2026-08-18',
        anchor_days=V['anchor_days'], div_between=V['div_between'],
        study_date='2026-08-18', build='SAVOLA_Valuation_Study_18-08-2026',
    ),
    hist_is=dict(
        FY23=dict(rev=V['rev_fy23'], cogs=V['cogs_fy23'], gp=GP_H['FY23'],
                  sda=V['sda_fy23'], adm=V['adm_fy23'], oth=V['oth_fy23'],
                  dna=V['dna_fy23'], ebitda=EBITDA_H['FY23'], np_att=V['np_att_fy23'],
                  basis='continuing per FY2024 FS (ex Iran/Sudan, INCL. Turkiye)'),
        FY24=dict(rev=V['rev_fy24'], cogs=V['cogs_fy24'], gp=GP_H['FY24'],
                  sda=V['sda_fy24'], adm=V['adm_fy24'], oth=V['oth_fy24'],
                  dna=V['dna_fy24'], ebitda=EBITDA_H['FY24'], np_att=V['np_att_fy24'],
                  recurring_np=V['recurring_np_fy24'],
                  basis='continuing per FY2025 FS (ex Turkiye)'),
        FY25=dict(rev=V['rev_fy25'], cogs=V['cogs_fy25'], gp=GP_H['FY25'],
                  sda=V['sda_fy25'], adm=V['adm_fy25'], oth=V['oth_fy25'],
                  dna=V['dna_fy25'], ebitda=EBITDA_H['FY25'], np_att=V['np_att_fy25'],
                  recurring_np=V['recurring_np_fy25'], eps=V['eps_fy25'],
                  assoc=V['assoc_fy25'], pbt=V['pbt_fy25'],
                  basis='continuing per FY2025 FS'),
    ),
    hist_bs=dict(
        FY25=dict(ppe=V['ppe_fy25'], rou=V['rou_fy25'], intang=V['intang_fy25'],
                  invprop=V['invprop_fy25'], kinan=V['kinan_carry'],
                  inv_nc=V['inv_nc_fy25'], inv_c=V['inv_c_fy25'],
                  inventories=V['inventories_fy25'], tr=V['tr_fy25'],
                  prepay=V['prepay_fy25'], cash=V['cash_fy25'],
                  loans=V['loans_fy25'], leases=V['leases_fy25'], eb=V['eb_fy25'],
                  restor=V['restor_fy25'], tp=V['tp_fy25'], accrued=V['accrued_fy25'],
                  contract=V['contract_fy25'], equity_att=V['equity_att_fy25'],
                  nci=V['nci_book_fy25'], nwc=NWC0,
                  total_assets=20480.053, total_liab=14013.987),
        FY24=dict(inventories=V['inventories_fy24'], tr=V['tr_fy24'], tp=V['tp_fy24'],
                  ppe=V['ppe_fy24'], loans=3403.577, leases=3593.097, cash=2235.328,
                  equity_att=4620.330, total_assets=21394.242),
        FY23=dict(loans=8644.487, cash=1213.193, term_dep=738.395, equity_att=8397.145,
                  total_assets=29937.138,
                  note='per FY2024 FS comparative; pre-restructuring balance sheet'),
    ),
    segments_fy25=dict(
        fp=dict(rev=V['fp_segrev_fy25'], cogs=V['fp_cogs_fy25'], gp=fp_gp_fy25),
        retail=dict(rev=V['ret_segrev_fy25'], cogs=V['ret_cogs_fy25'],
                    gp=V['ret_segrev_fy25'] - V['ret_cogs_fy25']),
        food_services=dict(rev=V['fsv_segrev_fy25']),
        frozen=dict(rev=V['frz_segrev_fy25']),
        investments=dict(rev=V['invseg_rev_fy25']),
        elim=V['elim_fy25'],
        categories=dict(oil=dict(vol=V['oil_vol_fy25'], rev=V['oil_rev_fy25'],
                                 gp=V['oil_gp_fy25'], ebitda=V['oil_ebitda_fy25']),
                        sugar=dict(vol=V['sug_vol_fy25'], rev=V['sug_rev_fy25'],
                                   gp=V['sug_gp_fy25'], ebitda=V['sug_ebitda_fy25']),
                        pasta=dict(vol=V['pas_vol_fy25'], rev=V['pas_rev_fy25'],
                                   gp=pas_gp_fy25),
                        nuts=dict(rev=nuts_rev_fy25, gp=nuts_gp_fy25, gm=nuts_gm_fy25)),
    ),
    h1_2026=dict(rev=V['h1_rev'], ebitda_company=V['h1_ebitda'], np_att=V['h1_np_att'],
                 recurring_np=372.0, capex=V['h1_capex'], netdebt=V['h1_netdebt'],
                 oil=dict(vol=V['h1_oil_vol'], rev=V['h1_oil_rev'], gp=V['h1_oil_gp'],
                          gpt=_OIL_GPT_H126),
                 sugar=dict(vol=V['h1_sug_vol'], rev=V['h1_sug_rev'], gp=V['h1_sug_gp'],
                            gpt=_SUG_GPT_H126),
                 pasta=dict(vol=V['h1_pas_vol'], rev=V['h1_pas_rev'], gp=V['h1_pas_gp'],
                            gpt=_PAS_GPT_H126),
                 nuts_rev=V['h1_nuts_rev'],
                 panda=dict(rev=V['h1_panda_rev'], ebitda=V['h1_panda_ebitda'],
                            sps_change=_D_PANDA_SPS),
                 herfy=dict(rev=V['h1_herfy_rev'], ebitda=V['h1_herfy_ebitda']),
                 frozen=dict(rev=V['h1_frz_rev'], ebitda=V['h1_frz_ebitda']),
                 stores=V['stores_jun26']),
    fcst=dict(
        years=Y, rev=B['rev'], ebitda=B['ebitda'],
        ebitda_margin=[e / r for e, r in zip(B['ebitda'], B['rev'])],
        dna=DNA, dna_own=OWN_D, dna_int=INT_D, dna_rou=ROU_D,
        ebit=EBIT, nopat=NOPAT, capex=B['capex'], dwc=DWC, nwc=NWC, fcff=FCFF,
        fp_rev=B['fp_rev'], fp_gp=B['fp_gp'], fp_eb=B['fp_eb'],
        oil=dict(vol=B['oil_v'], rev=B['oil_rev'], gp=B['oil_gp'], eb=B['oil_eb'],
                 gpt=V['oil_gpt_path']),
        sugar=dict(vol=B['sug_v'], rev=B['sug_rev'], gp=B['sug_gp'], eb=B['sug_eb'],
                   gpt=V['sug_gpt_path']),
        pasta=dict(vol=B['pas_v'], rev=B['pas_rev'], gp=B['pas_gp'], eb=B['pas_eb'],
                   gpt=V['pas_gpt_path']),
        nuts=dict(rev=B['nuts_rev'], gp=B['nuts_gp'], eb=B['nuts_eb'],
                  gm=V['nuts_gm_path']),
        panda=dict(rev=B['pan_rev'], gp=B['pan_gp'], eb=B['pan_eb'],
                   stores=V['stores_path'],
                   sps=[r / ((a + b) / 2) for r, a, b in
                        zip(B['pan_rev'], [V['stores_end25']] + V['stores_path'][:-1],
                            V['stores_path'])]),
        herfy=dict(rev=B['her_rev'], eb=B['her_eb']),
        frozen=dict(rev=B['frz_rev'], eb=B['frz_eb']),
        elim=B['elim'], unalloc=V['unalloc_path'],
        np=NP, np_nci=NP_NCI, eps=eps_f, div=DIV, div_nci=DIV_NCI,
        netdebt=NDEBT, netfin=NF, kinan=KINAN, kinan_div=KINAN_DIV,
        ppe=PPE_PATH, rou=ROU_P, leases=LEASEB, cash=CASH_P, cfo=CFO_P,
        equity_att=EQ_ATT_P, nci=NCI_P, kinan_bv=KINAN_BV,
    ),
    wacc=dict(
        rf_observed=V['rf_observed'], rf_star_rating=rf_star_rating,
        rf_star_cds=rf_star_cds, erp_rating=V['erp_rating'], erp_cds=V['erp_cds'],
        sov_spread_rating=V['sov_spread_rating'], sov_spread_cds=V['sov_spread_cds'],
        beta=V['beta'], ke_rating=ke_rating, ke_cds=ke_cds,
        kd_sar=V['kd_sar'], kd_eg=V['kd_eg_localeq'], kd_other=V['kd_other'],
        kd_loans=kd_loans, kd_lease=kd_lease, debt_w=dict(sa=w_sa, eg=w_eg, other=w_ot),
        we=we, wl=wl, wlease=wz, wacc_exp=wacc_exp, wacc_exp_cds=wacc_exp_cds,
        tw_e=V['tw_e'], tw_loans=V['tw_loans'], tw_lease=tw_lease,
        wacc_term=wacc_term, wacc_term_cds=wacc_term_cds,
        ust10=V['ust10'], ust1=V['ust1'], sar1y=V['sar_1y_obs'],
        ksa_spread=V['ksa_usd10_spread'], saibor3m=V['saibor3m'], tax=T,
    ),
    dcf=dict(
        pv_explicit=PV_EXP, tv=TV, pv_tv=PV_TV, ev=EV_OP, tv_share=TV_SHARE,
        dfs=DFS, fcff_term=FCFF_T, reinvest_term=V['g_term'] / V['roic_term'],
        g=V['g_term'], roic_term=V['roic_term'],
        nonop=NONOP, kinan_capitalized=kinan_capitalized,
        nci_val=NCI_VAL, nci_herfy_mkt=nci_herfy_mkt, nci_other_book=nci_other_book,
        herfy_mktcap=herfy_mktcap,
        eq_val=EQ, ps_dec=PS_DEC, roll=ROLL, ps=PS,
        ps_cds=PS_CDS, eq_cds=eq_cds, ev_cds=ev_cds,
        framingA=PS_A, framingB=PS_B, framing_gap=PS_A - PS_B,
        bear=PS_BEAR, bull=PS_BULL,
    ),
    lenses=dict(
        dcf=dict(base=PS_A, bear=PS_BEAR, bull=PS_BULL),
        relative=dict(base=rel_base, bear=rel_bear, bull=rel_bull,
                      eps_f=eps_f[0], pe=pe_applied, pe_mix=pe_mix,
                      pe_fp_leg=pe_fp_leg, pe_ret_leg=pe_ret_leg,
                      pe_discount=V['pe_discount'], pe_ddm=_pe_ddm),
        normalized=dict(base=norm_base, bear=norm_bear, bull=norm_bull,
                        eps_norm=eps_norm, pe=pe_applied),
        book=dict(base=book_base, bear=book_bear, bull=book_bull, bvps=bvps,
                  roe=roe_sust, pb=pb_just),
    ),
    weights=W_L, central=CENTRAL, panel_centre=PANEL,
    experts=EXPERTS, panel_median=PANEL_MED,
    sens=dict(wacc_grid=WACC_GRID, g_grid=G_GRID, grid=SENS, beta_grid=BETA_GRID,
              rf_alts=RF_ALTS),
    peers=dict(pe=V['peer_pe'],
               note='cross-check only (market data 18-Aug-2026); the peer-mix multiple is '
                    'computed from these quotes with the discount applied and disclosed'),
    inputs={k: INP[k] for k in INP},
)

# embed the quant-pipeline results so every builder reads ONE file
for fn, key in [('step0_result.json', 'step0'), ('backtest_5y.json', 'backtest'),
                ('strike_result.json', 'strike'), ('beta_result.json', 'beta'),
                ('tech_read.json', 'tech')]:
    with open(os.path.join(HERE, fn)) as fh:
        OUT[key] = json.load(fh)

with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(OUT, f, indent=1, default=float)

say(f"FY26E revenue {B['rev'][0]:,.0f} (H1 actual {V['h1_rev']:,.0f} -> implied H2 "
    f"{B['rev'][0] - V['h1_rev']:,.0f} vs H2-25 {V['rev_fy25'] - 13080.0:,.0f})")
say(f"EBITDA path: " + " ".join(f"{e:,.0f}" for e in B['ebitda'])
    + f" | margins " + " ".join(f"{e / r:.1%}" for e, r in zip(B['ebitda'], B['rev'])))
say(f"FCFF path: " + " ".join(f"{x:,.0f}" for x in FCFF))
say(f"WACC exp {wacc_exp:.2%} (CDS {wacc_exp_cds:.2%}) | term {wacc_term:.2%} | "
    f"Ke {ke_rating:.2%}/{ke_cds:.2%} | Kd loans {kd_loans:.2%} lease {kd_lease:.2%}")
say(f"EV {EV_OP:,.0f} | TV share {TV_SHARE:.1%} | nonop {NONOP:,.0f} | NCI {NCI_VAL:,.0f}")
say(f"equity {EQ:,.0f} -> {PS_DEC:.2f}/sh (Dec-25) -> {PS:.2f} at anchor "
    f"(roll {ROLL:.4f}, div {V['div_between']:.2f})")
say(f"FRAMING A {PS_A:.2f} vs FRAMING B {PS_B:.2f} (gap {PS_A - PS_B:.2f}) | CDS basis {PS_CDS:.2f}")
say(f"lenses: DCF {PS_A:.2f} [{PS_BEAR:.2f},{PS_BULL:.2f}] | rel {rel_base:.2f} | "
    f"norm {norm_base:.2f} | book {book_base:.2f} | CENTRAL {CENTRAL:.2f} vs spot {V['spot']}")
say("study_numbers.json written")
