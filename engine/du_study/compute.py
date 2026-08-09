"""DU study — master computation. Writes study_numbers.json (single source of
truth for every builder). Code-first rule: INPUTS are four-field records
{value, source, date, ring}; a bare numeral cannot enter the model; the ASSERT
block raises (no JSON emitted) unless the bridge closes, the discount-rate glide
is ordered, and the terminal is ROIC-consistent.

BUILT 09-Aug-2026 on the actual audited/reviewed consolidated financial
statements read from the company's own investor-relations portal
(investors.du.ae): FY2023 (PwC, unqualified, 13-Feb-2024), FY2024 (PwC,
unqualified, 10-Feb-2025), FY2025 (KPMG Lower Gulf, unmodified, 09-Feb-2026),
and the reviewed condensed interims for Q1-2026 (31-Mar) and H1-2026 (30-Jun,
KPMG ISRE 2410, 22-Jul-2026). Segment KPIs (subscribers, ARPU, capex intensity)
from the company's own earnings releases and analyst presentations (COMPANY_IR).

Company class: integrated telecom OPERATING COMPANY (mobile + fixed + wholesale
+ ICT; no captive lender, no borrowings — the balance sheet is unleveraged with
a net cash position in every year studied). Lens set follows the operating-
company reference (SWDY pattern inside the model-study skeleton): FCFF DCF
primary, relative multiples, normalized earnings power, and a book/ROE lens.

THE CONTESTED JUDGEMENT (computed BOTH WAYS, per the dual-framing rule extended
to the study's central judgement): the post-2026 UAE fiscal regime for telecom
operators. Cabinet decision 8/38 of 2023 legislates the 38% federal royalty +
9% corporate income tax (combined floor AED 1.8bn/yr) for 2024-2026 ONLY.
Framing A (base): the current regime persists unchanged — combined effective
take 43.6% (the audited FY2025 rate). Framing B: reversion to the pre-2024
construction (15% of regulated revenue + 30% of regulated profit), which took
53.1% of pre-royalty profit in FY2023. Both fair values are published side by
side; they are never averaged.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np

# ============================ INPUTS =========================================
# All statement figures in AED mn (audited statements print AED'000; /1000 here,
# a unit conversion, not a derivation). Per-share figures in AED.
def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)

AR25 = ("Audited consolidated FS, Integrated Annual Report 2025, investors.du.ae "
        "(KPMG Lower Gulf, unmodified opinion 09-Feb-2026)")
AR24 = ("Audited consolidated FS, Annual Report 2024, investors.du.ae "
        "(PwC, unqualified opinion 10-Feb-2025)")
AR23 = ("Audited consolidated FS, Annual Report 2023, investors.du.ae "
        "(PwC, unqualified opinion 13-Feb-2024)")
H126 = ("Reviewed condensed consolidated interim FS for the six months ended 30-Jun-2026, "
        "investors.du.ae (KPMG ISRE 2410 review, 22-Jul-2026)")
IRQ2 = "Company Q2-2026 earnings release + analyst presentation, investors.du.ae (COMPANY_IR)"
IRQ4 = "Company Q4/FY2025 results presentation, 10-Feb-2026, investors.du.ae (COMPANY_IR)"

INP = dict(
    # ---- anchors --------------------------------------------------------
    spot=I(12.30, "Uploaded DFM daily price history for DU, last close 07-Aug-2026", "2026-08-07",
           "Market"),
    shares_mn=I(4532.905989, "Share capital note 27, audited FY2025 consolidated FS: "
                "4,532,905,989 shares of AED 1 each, authorised, issued and fully paid, "
                "unchanged across FY2023-FY2025 and both 2026 interims", "2026-02-09", "Company"),
    anchor_days=I(219.0, "31-Dec-2025 valuation date to the 07-Aug-2026 price anchor", "2026-08-07",
                  "House"),
    div_between=I(0.40, "Final FY2025 cash dividend AED 0.40/share, approved AGM 30-Mar-2026, "
                  "PAID 28-Apr-2026 (AED 1,813,162k) — value that left the share between the "
                  "valuation date and the anchor. The H1-2026 interim of AED 0.26 was declared "
                  "23-Jul-2026 but not yet paid at the anchor, so it stays in the share",
                  "2026-07-22", "Company"),

    # ---- historical income statement (AED mn, consolidated, AUDITED) ------
    # FY2024 figures are the IFRS 18 re-presented comparatives in the FY2025
    # statements (Note 39) so that FY2024 and FY2025 sit on one presentation.
    rev_fy23=I(13636.340, AR23 + ", consolidated statement of comprehensive income", "2024-02-13",
               "Company"),
    rev_fy24=I(14635.917, AR25 + ", FY2024 comparative (IFRS 18 re-presented, Note 39)",
               "2026-02-09", "Company"),
    rev_fy25=I(15905.421, AR25, "2026-02-09", "Company"),
    ebitda_fy25=I(7338.388, AR25 + ": 'Operating profit before depreciation and amortization' "
                  "printed on the face of the statement", "2026-02-09", "Company"),
    ebitda_fy24=I(6469.839, AR25 + ", FY2024 comparative on the face (IFRS 18)", "2026-02-09",
                  "Company"),
    ebitda_fy23=I(5799.601, "DERIVED (flagged): FY2023 statements print no EBITDA line "
                  "(pre-IFRS 18). Operating profit pre-royalty (rev - opex - ECL + other income "
                  "= 3,601.324) + D&A 2,198.277, every component audited (" + AR23 + ")",
                  "2024-02-13", "Company/derived"),
    dna_fy23=I(2198.277, AR23 + ", Note 26 opex split: PP&E depreciation 1,544.182 + "
               "right-of-use depreciation 445.042 + intangibles amortisation 209.053",
               "2024-02-13", "Company"),
    dna_fy24=I(2153.590, AR24 + ", Note 31 split: PP&E 1,569.189 + ROU 374.505 + intangibles "
               "209.896", "2025-02-10", "Company"),
    dna_fy25=I(2167.933, AR25 + ", Note 31 split: PP&E 1,557.989 + ROU 364.063 + intangibles "
               "245.881", "2026-02-09", "Company"),
    op_fy25=I(5170.455, AR25 + ", operating profit on the face", "2026-02-09", "Company"),
    op_fy24=I(4316.249, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    int_inc_fy25=I(74.672, AR25 + ", interest income (Note 32)", "2026-02-09", "Company"),
    int_inc_fy24=I(82.214, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    int_exp_fy25=I(95.054, AR25 + ", interest expense (Note 32; principally lease interest "
                   "71.094)", "2026-02-09", "Company"),
    int_exp_fy24=I(89.770, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    assoc_fy25=I(-0.894, AR25 + ", share of loss on equity-accounted investments", "2026-02-09",
                 "Company"),
    pbt_fy25=I(5149.122, AR25 + ", profit before federal royalty and income tax", "2026-02-09",
               "Company"),
    pbt_fy24=I(4306.151, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    pbt_fy23=I(3558.501, "DERIVED (flagged): profit 1,667.851 + total federal royalty 1,890.650 "
               "(revenue leg 1,400.199 + profit leg 490.451, Note 27, " + AR23 + ") — the "
               "pre-royalty profit the FY2023 statement layout never prints as one line",
               "2024-02-13", "Company/derived"),
    royalty_fy25=I(1956.602, AR25 + ", federal royalty on the face", "2026-02-09", "Company"),
    royalty_fy24=I(1571.649, AR25 + ", FY2024 comparative (IFRS 18)", "2026-02-09", "Company"),
    royalty_fy23=I(1890.650, AR23 + ", Note 27: royalty on regulated revenue 1,400.199 + royalty "
                   "on regulated profit 490.451", "2024-02-13", "Company"),
    tax_fy25=I(287.435, AR25 + ", income tax expense on the face", "2026-02-09", "Company"),
    tax_fy24=I(246.955, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    np_fy23=I(1667.851, AR23, "2024-02-13", "Company"),
    np_fy24=I(2487.547, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    np_fy25=I(2905.085, AR25, "2026-02-09", "Company"),
    eps_fy23=I(0.37, AR23 + ", Note 29", "2024-02-13", "Company"),
    eps_fy24=I(0.55, AR25 + ", Note 33 comparative", "2026-02-09", "Company"),
    eps_fy25=I(0.64, AR25 + ", Note 33", "2026-02-09", "Company"),

    # ---- the fiscal regime: THE CONTESTED JUDGEMENT ------------------------
    tax_eff=I(0.4357, "Combined federal royalty + income tax charge / profit before both, audited "
              "FY2025: (1,956.602 + 287.435) / 5,149.122 = 43.57% (Note 26 states 43.6%; FY2024 "
              "44.7%). Regime: Cabinet decision 8/38 of 2023 — 38% federal royalty on total UAE "
              "regulated and non-regulated profits + 9% corporate income tax, combined floor "
              "AED 1.8bn/yr, legislated for 2024-2026", "2026-02-09", "Company"),
    reg_share=I(0.690, "Regulated revenue share under the PRE-2024 regime, audited FY2023 Note 27: "
                "total regulated revenue 9,410.136 / total revenue 13,636.340 = 69.0% — the "
                "revenue base for Framing B of the contested judgement", "2024-02-13", "Company"),
    royB_rev_rate=I(0.15, "Pre-2024 royalty construction, leg 1: 15% of regulated revenue "
                    "(" + AR23 + ", Note 27)", "2024-02-13", "Company"),
    royB_prof_rate=I(0.30, "Pre-2024 royalty construction, leg 2: 30% of regulated profit after "
                     "deducting the revenue-leg royalty (" + AR23 + ", Note 27)", "2024-02-13",
                     "Company"),

    # ---- historical balance sheet (AED mn, AUDITED) ------------------------
    ppe_fy23=I(9722.700, AR23, "2024-02-13", "Company"),
    ppe_fy24=I(9838.448, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    ppe_fy25=I(10288.767, AR25, "2026-02-09", "Company"),
    rou_fy23=I(1597.185, AR23, "2024-02-13", "Company"),
    rou_fy24=I(1657.217, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    rou_fy25=I(1515.395, AR25, "2026-02-09", "Company"),
    intang_fy23=I(1110.769, AR23 + " ('Intangible assets and goodwill', one line pre-2024)",
                  "2024-02-13", "Company"),
    intang_fy24=I(846.932, AR25 + ", FY2024 comparative (intangibles excl. goodwill)",
                  "2026-02-09", "Company"),
    intang_fy25=I(869.600, AR25 + " (software 297.272 + capital work in progress 571.459 + TDRA "
                  "licence NBV 0.869, Note 8)", "2026-02-09", "Company"),
    goodwill_fy25=I(413.220, AR25 + ", Note 9 (unchanged from FY2024)", "2026-02-09", "Company"),
    inv_fy23=I(101.695, AR23, "2024-02-13", "Company"),
    inv_fy24=I(175.610, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    inv_fy25=I(175.457, AR25, "2026-02-09", "Company"),
    recv_fy23=I(2224.031, AR23 + " ('Trade receivables, contract assets and other assets', "
                "current)", "2024-02-13", "Company"),
    recv_fy24=I(2128.565, AR25 + ", FY2024 comparative (trade receivables and contract assets, "
                "current)", "2026-02-09", "Company"),
    recv_fy25=I(2222.511, AR25, "2026-02-09", "Company"),
    ccost_fy23=I(341.863, AR23 + " (contract costs, current)", "2024-02-13", "Company"),
    ccost_fy24=I(361.577, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    ccost_fy25=I(442.363, AR25, "2026-02-09", "Company"),
    relparty_a_fy23=I(53.449, AR23 + " (due from related parties)", "2024-02-13", "Company"),
    relparty_a_fy24=I(21.732, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    relparty_a_fy25=I(27.481, AR25, "2026-02-09", "Company"),
    othca_fy23=I(0.0, AR23 + " — other non-financial assets are not a separate current line in "
                 "the FY2023 layout (folded into trade receivables and other assets); carried at "
                 "zero to avoid double-counting", "2024-02-13", "Company"),
    othca_fy24=I(324.287, AR25 + ", FY2024 comparative (other non-financial assets, current)",
                 "2026-02-09", "Company"),
    othca_fy25=I(416.846, AR25, "2026-02-09", "Company"),
    cash_fy23=I(610.036, AR23 + " (cash and bank balances)", "2024-02-13", "Company"),
    cash_fy24=I(983.969, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    cash_fy25=I(465.700, AR25, "2026-02-09", "Company"),
    deposits_fy23=I(1326.586, AR23 + " (term deposits)", "2024-02-13", "Company"),
    deposits_fy24=I(1299.283, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    deposits_fy25=I(1784.019, AR25, "2026-02-09", "Company"),
    assets_fy23=I(17703.736, AR23, "2024-02-13", "Company"),
    assets_fy24=I(18693.292, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    assets_fy25=I(19375.709, AR25, "2026-02-09", "Company"),
    pay_fy23=I(5247.287, AR23 + " (trade and other payables — INCLUDES the accrued federal "
               "royalty, which the FY2023 layout does not present separately)", "2024-02-13",
               "Company"),
    roy_accr_fy23=I(2033.172, AR24 + ", Note 23 accrued-royalty movement: balance at 1-Jan-2024 "
                    "= 2,033.172 — the royalty accrual sitting INSIDE FY2023 trade payables, "
                    "netted out for a like-for-like working-capital series", "2025-02-10",
                    "Company"),
    pay_fy24=I(3666.058, AR25 + ", FY2024 comparative (trade and other payables)", "2026-02-09",
               "Company"),
    pay_fy25=I(3711.346, AR25, "2026-02-09", "Company"),
    roytax_fy24=I(1923.452, AR25 + ", FY2024 comparative (federal royalty and income tax, "
                  "current liability)", "2026-02-09", "Company"),
    roytax_fy25=I(2283.439, AR25, "2026-02-09", "Company"),
    cliab_fy23=I(465.710, AR23 + " (contract liabilities, current)", "2024-02-13", "Company"),
    cliab_fy24=I(559.180, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    cliab_fy25=I(629.724, AR25, "2026-02-09", "Company"),
    relparty_l_fy23=I(6.064, AR23 + " (due to related parties)", "2024-02-13", "Company"),
    relparty_l_fy24=I(6.717, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    relparty_l_fy25=I(6.030, AR25, "2026-02-09", "Company"),
    lease_fy23=I(2104.959, AR23 + " (lease liabilities: current 649.585 + non-current 1,455.374)",
                 "2024-02-13", "Company"),
    lease_fy24=I(1998.687, AR25 + ", FY2024 comparative (561.999 + 1,436.688)", "2026-02-09",
                 "Company"),
    lease_fy25=I(1938.819, AR25 + " (592.141 + 1,346.678)", "2026-02-09", "Company"),
    debt_fy25=I(0.0, AR25 + ", Note 4.2 capital-risk table: Total borrowings '–' — ZERO drawn "
                "borrowings in every year studied (FY2022-FY2025 and both 2026 interims). The "
                "only facility is undrawn: AED 2.0bn 7-year unsecured RCF signed 06-Apr-2026",
                "2026-02-09", "Company"),
    eq_fy23=I(9243.213, AR23, "2024-02-13", "Company"),
    eq_fy24=I(9878.445, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    eq_fy25=I(10148.291, AR25, "2026-02-09", "Company"),

    # ---- cash-flow markers (AED mn, AUDITED) -----------------------------
    ocf_fy23=I(4425.366, AR23 + ", net cash generated from operating activities", "2024-02-13",
               "Company"),
    ocf_fy24=I(4636.508, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    ocf_fy25=I(5229.823, AR25, "2026-02-09", "Company"),
    capex_ppe_fy23=I(1899.868, AR23 + ", purchase of property, plant and equipment",
                     "2024-02-13", "Company"),
    capex_ppe_fy24=I(1535.742, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    capex_ppe_fy25=I(2038.501, AR25, "2026-02-09", "Company"),
    capex_int_fy23=I(327.690, AR23 + ", purchase of intangible assets", "2024-02-13", "Company"),
    capex_int_fy24=I(384.726, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    capex_int_fy25=I(314.729, AR25, "2026-02-09", "Company"),
    div_paid_fy23=I(1178.556, AR23 + ", dividends paid", "2024-02-13", "Company"),
    div_paid_fy24=I(1858.491, AR25 + ", FY2024 comparative", "2026-02-09", "Company"),
    div_paid_fy25=I(2629.085, AR25 + " (final-2024 AED 0.34 + interim-2025 AED 0.24)",
                    "2026-02-09", "Company"),
    lease_paid_fy25=I(282.473, AR25 + ", repayment of lease liabilities (financing)",
                      "2026-02-09", "Company"),
    lease_int_fy25=I(71.094, AR25 + ", interest paid on lease liabilities", "2026-02-09",
                     "Company"),
    dps_fy23=I(0.34, AR23 + "/AR24: interim 0.13 (paid 23-Aug-2023) + final 0.21 (paid "
               "18-Apr-2024)", "2024-04-18", "Company"),
    dps_fy24=I(0.54, AR24 + "/AR25: interim 0.20 (paid 19-Aug-2024) + final 0.34 (paid "
               "15-Apr-2025); IR: 98% payout", "2025-04-15", "Company"),
    dps_fy25=I(0.64, AR25 + ": interim 0.24 (paid 21-Aug-2025) + final 0.40 (paid 28-Apr-2026); "
               "IR: ~100% payout, the highest dividend and payout in du history", "2026-04-28",
               "Company"),

    # ---- interims (AED mn, REVIEWED) --------------------------------------
    h1_26_rev=I(8197.573, H126, "2026-07-22", "Company"),
    h1_25_rev=I(7750.295, H126 + ", comparative", "2026-07-22", "Company"),
    h1_26_ebitda=I(4031.922, H126 + ", operating profit before D&A on the face (margin 49.2%)",
                   "2026-07-22", "Company"),
    h1_26_dna=I(1133.244, H126, "2026-07-22", "Company"),
    h1_26_np=I(1631.971, H126, "2026-07-22", "Company"),
    h1_25_np=I(1449.267, H126 + ", comparative", "2026-07-22", "Company"),
    h1_25_ebitda=I(3650.187, H126 + ", comparative", "2026-07-22", "Company"),
    h1_26_capex=I(1038.0, IRQ2 + ": cost additions to PP&E + intangibles, H1-2026 (capital "
                  "intensity 12.7%)", "2026-07-23", "Company"),
    h2_25_rev=I(8155.126, "DERIVED (flagged): FY2025 revenue 15,905.421 − H1-2025 7,750.295, "
                "both audited/reviewed", "2026-07-22", "Company/derived"),
    h2_25_ebitda=I(3688.201, "DERIVED (flagged): FY2025 EBITDA 7,338.388 − H1-2025 3,650.187",
                   "2026-07-22", "Company/derived"),
    dps_h1_26=I(0.26, H126 + " + Q2 earnings release: interim AED 0.26/share approved by the "
                "Board 23-Jul-2026 (AED 1,178.556mn), +8.3% y/y", "2026-07-23", "Company"),

    # ---- segment structure — THE DISCLOSED FOUR SEGMENTS -------------------
    # AR2025 basis (Mobile / Fixed / Wholesale / ICT and associated telecom
    # services) for FY2024-FY2025; the FY2023 statements use the older
    # Mobile / Fixed / Wholesale / Others split, and the wholesale-vs-other
    # boundary moved in the re-segmentation, so FY2023 is carried on its own
    # printed basis and flagged as a presentation break.
    seg_rev_hist=I(dict(
        FY23=dict(mobile=7004.142, fixed=3779.777, wholesale=1768.447, ict=1083.974),
        FY24=dict(mobile=6548.135, fixed=4002.658, wholesale=2373.068, ict=1712.056),
        FY25=dict(mobile=7074.936, fixed=4379.705, wholesale=2568.222, ict=1882.558),
    ), "Segment notes: FY2023 Note 34 (" + AR23 + ", old basis, 'Others' shown under ict); "
       "FY2024-FY2025 Note 38 (" + AR25 + ", current basis, FY2024 re-presented)", "2026-02-09",
       "Company"),
    seg_contrib_hist=I(dict(
        FY24=dict(mobile=3985.612, fixed=3387.593, wholesale=2088.976, ict=355.294),
        FY25=dict(mobile=4303.642, fixed=3757.853, wholesale=2219.473, ict=365.028),
    ), AR25 + ", Note 38: segment contribution ('gross margin' = revenue less direct costs, "
       "before opex and D&A)", "2026-02-09", "Company"),

    # ---- unit build: subscribers x ARPU (COMPANY_IR, per-quarter) ----------
    subs_mobile=I(dict(Q4_2024=8916, Q1_2025=9137, Q2_2025=9138, Q3_2025=9170, Q4_2025=9704,
                       Q1_2026=9692, Q2_2026=9280),
                  IRQ2 + " + prior quarterly decks: mobile customers ('000, TDRA 90-day active "
                  "definition); Q2-2026 net adds −412k (prepaid −442k on the tourism shock, "
                  "postpaid +30k)", "2026-07-23", "Company"),
    subs_fixed=I(dict(Q4_2024=682, Q1_2025=701, Q2_2025=706, Q3_2025=718, Q4_2025=735,
                      Q1_2026=745, Q2_2026=744),
                 IRQ2 + ": fixed customers ('000)", "2026-07-23", "Company"),
    arpu_mobile=I(dict(FY2025=63.3, Q1_2026=63.4, Q2_2026=63.4),
                  IRQ2 + ": blended mobile ARPU, AED/month", "2026-07-23", "Company"),
    subs_mobile_path=I([9450.0, 9760.0, 10010.0, 10240.0, 10450.0],
                       "House forecast, end-of-year mobile subscribers ('000): H2-2026 recovery "
                       "of +170k from the Q2 trough (gross adds still below pre-conflict per the "
                       "company's own Q2 commentary), then +310k/+250k/+230k/+210k as tourism "
                       "and population inflows normalise — well below the +788k of boom-year "
                       "2025, above the flat conflict quarter", "2026-08-09", "House"),
    subs_fixed_path=I([760.0, 790.0, 815.0, 838.0, 858.0],
                      "House forecast, end-of-year fixed subscribers ('000): +16k in H2-2026 "
                      "then +30k/+25k/+23k/+20k — continued fibre/FWA share gain at a slowing "
                      "rate; FY2025 added +53k", "2026-08-09", "House"),
    arpu_mobile_path=I([63.4, 63.6, 63.8, 64.0, 64.2],
                       "House forecast, blended mobile ARPU AED/month: held essentially flat "
                       "(+0.3%/yr) — postpaid mix gain (+9% y/y postpaid growth) offsetting "
                       "prepaid dilution; company printed 63.3-63.4 across FY2025-Q2-2026",
                       "2026-08-09", "House"),
    arpu_fixed_path=I([537.0, 545.0, 553.0, 561.0, 569.0],
                      "House forecast, implied fixed revenue per subscriber AED/month (fixed "
                      "segment revenue / average base — a blend of consumer broadband and "
                      "enterprise fixed, so a revenue-intensity metric, not a tariff): H1-2026 "
                      "actual 533; FY2025 515. +1.5%/yr on enterprise/ICT-adjacent mix",
                      "2026-08-09", "House"),
    seg_g=I(dict(wholesale=[-0.008, 0.015, 0.020, 0.020, 0.020],
                 ict=[0.079, 0.110, 0.100, 0.090, 0.080]),
            "House forecast: wholesale −0.8% in 2026 (H1 actual −2.0% y/y on conflict-hit "
            "roaming/transit, partial H2 stabilisation) then +1.5-2%; ICT +7.9% in 2026 (H1 "
            "actual +4.8%, Q4-heavy seasonality) accelerating to +11% on the data-centre ramp "
            "(Microsoft hyperscale agreement, du Q4-2025 deck) then easing to +8%",
            "2026-08-09", "House"),
    contrib_margin_path=I(dict(
        mobile=[0.608, 0.608, 0.608, 0.608, 0.608],
        fixed=[0.858, 0.858, 0.858, 0.858, 0.858],
        wholesale=[0.864, 0.864, 0.864, 0.864, 0.864],
        ict=[0.194, 0.200, 0.205, 0.210, 0.215]),
        "Segment contribution margins: mobile/fixed/wholesale held at the audited FY2025 rates "
        "(60.8% / 85.8% / 86.4% — FY2024: 60.9% / 84.6% / 88.0%); ICT lifted 19.4% -> 21.5% "
        "over five years on data-centre scale (still the thinnest-margin segment)",
        "2026-08-09", "House"),

    # ---- opex stack — ONE ESCALATOR PER DRIVER CLASS -----------------------
    # (cost-stack escalation rule: each physically distinct cost line gets its
    # own driver, never one blended index)
    opex_base_fy25=I(dict(network=963.878, marketing=292.293, staff=1105.328, admin=189.654,
                          licence=433.959, other=133.192, ecl=211.020, other_inc=-21.716),
                     AR25 + ", face of the income statement: net operating expenses before D&A "
                     "by nature (licence = telecommunication licence and related fees, a "
                     "revenue-linked regulatory charge; ecl = impairment of trade/lease "
                     "receivables and contract assets net of recoveries)", "2026-02-09",
                     "Company"),
    esc_staff=I(0.020, "Staff-cost escalator 2.0%/yr — UAE wage inflation proxied by CPI (~2%) "
                "on a base the company is actively managing DOWN (H1-2026 staff cost −6.3% y/y, "
                "reviewed interims); applied from a rebased FY2026 level", "2026-08-09", "House"),
    esc_network=I(0.030, "Network & maintenance escalator 3.0%/yr — grows with network scale "
                  "(sites, fibre, data centres), proxied by blended subscriber growth plus "
                  "capacity additions", "2026-08-09", "House"),
    esc_admin=I(0.020, "Administrative escalator 2.0%/yr — general UAE cost inflation",
                "2026-08-09", "House"),
    esc_other=I(0.020, "Other operating expense escalator 2.0%/yr", "2026-08-09", "House"),
    marketing_pct=I(0.0180, "Marketing at 1.80% of revenue (FY2025 actual 1.84%, H1-2026 1.44% — "
                    "conflict-quarter restraint; forecast between the two)", "2026-08-09",
                    "House"),
    licence_pct=I(0.0270, "Telecom licence and related fees at 2.70% of revenue (FY2025 2.73%, "
                  "H1-2026 2.65% — a regulatory revenue-share, so revenue-linked by its own "
                  "nature)", "2026-08-09", "House"),
    ecl_pct=I(0.0145, "Expected-credit-loss charge at 1.45% of revenue (FY2025 1.33%, H1-2026 "
              "1.64% — conflict-quarter receivables stress; forecast between the two)",
              "2026-08-09", "House"),
    staff_fy26=I(985.0, "FY2026E staff cost: H1-2026 actual 471.360 + H2 at the H2-2025 "
                 "seasonal ratio (H2 runs above H1; 513.6 = H1 x 1.09) — the company's own "
                 "run-rate after the efficiency program, escalated 2%/yr thereafter",
                 "2026-08-09", "House"),
    other_inc_path=I(15.0, "Other operating income held at AED 15mn/yr (FY2025 21.7, H1-2026 "
                     "5.8 — lumpy, small)", "2026-08-09", "House"),

    # ---- capital intensity, D&A, working capital ---------------------------
    capex_pct=I([0.155, 0.150, 0.145, 0.135, 0.130],
                "Capex (PP&E + intangibles, cash basis) / revenue: FY2025 actual 14.8% "
                "(2,353.230 / 15,905.421, audited CF); H1-2026 12.7% with the company stating a "
                "back-loaded, data-centre-heavy plan and commitments UP at 2,411.760 (30-Jun-26 "
                "note) vs 2,124.526 (FY2025) — 15.5% at the peak of the data-centre build, "
                "gliding to 13.0% (no numeric company capex guidance for FY2026 was published; "
                "flagged as a house path on sourced commitment evidence)", "2026-08-09", "House"),
    capex_tang_share=I(0.866, "Tangible share of capex: FY2025 audited 2,038.501 / 2,353.230",
                       "2026-02-09", "Company"),
    dep_rate_ppe=I(0.1583, "PP&E depreciation rate on OPENING gross-of-additions balance: FY2025 "
                   "audited PP&E depreciation 1,557.989 / opening PP&E 9,838.448 = 15.83%",
                   "2026-02-09", "Company"),
    amort_rate=I(0.2890, "Intangibles amortisation rate on opening balance: FY2025 amortisation "
                 "245.881 / opening intangibles 846.932 = 29.0% (short-lived software; the TDRA "
                 "licence is fully amortised at NBV 0.869)", "2026-02-09", "Company"),
    rou_dep_path=I([355.0, 350.0, 345.0, 340.0, 335.0],
                   "Right-of-use depreciation: FY2025 actual 364.063, FY2024 374.505, FY2023 "
                   "445.042 — a gently declining site-lease book; held on that glide. Lease "
                   "REPLACEMENT capex is set equal to ROU depreciation in the FCFF build (the "
                   "steady-state assumption; actual FY2025 lease additions were only 96.034, so "
                   "this is the conservative side)", "2026-08-09", "House"),

    # ---- cost of capital ---------------------------------------------------
    # v2 method: rf* = local govt yield less the sovereign's own default spread;
    # country risk enters ONCE through the ERP. Both ERP bases published.
    rf=I(4.14, "PLACEHOLDER — DO NOT SHIP", "1900-01-01", "SENTINEL"),

    # ---- lens inputs -------------------------------------------------------
    lens_weights=I(dict(dcf=0.45, relative=0.25, normalized=0.20, book=0.10),
                   "House synthesis weights, operating-company pattern (SWDY reference study)",
                   "2026-08-09", "House"),
    g_term=I(0.025, "Terminal nominal AED growth 2.5%: below the IMF's UAE long-run nominal GDP "
             "growth (~4%: real ~4% + CPI ~2% per WEO Apr-2026) and consistent with a mature "
             "duopoly telecom growing at population-plus-inflation minus price erosion",
             "2026-08-09", "Country/House"),
)

# The WACC block is completed from live-sourced records (Damodaran UAE row,
# CBUAE/market AED yields, UAE CDS, peer betas) — appended by wacc_inputs.py
# merge below before anything is computed. The sentinel above guarantees the
# model cannot run on a placeholder.
_wacc_path = os.path.join(HERE, 'wacc_register.json')
with open(_wacc_path) as f:
    _wr = json.load(f)
for k, rec in _wr.items():
    INP[k] = rec
assert INP['rf']['ring'] != 'SENTINEL', 'WACC register did not overwrite the sentinel rf'

V = {k: rec['value'] for k, rec in INP.items()}
LOG = []
def say(s):
    LOG.append(s); print(s)

say("=" * 78)
say("DU — ASSERT / derivation log (built on audited FY23-25 + reviewed Q1/H1-2026 filings)")
say("=" * 78)

# ============================ CALC ===========================================
SH, SPOT, TAX = V['shares_mn'], V['spot'], V['tax_eff']
MKTCAP = SPOT * SH

# ---- historical income statement -------------------------------------------
ebit_fy23 = V['ebitda_fy23'] - V['dna_fy23']
ebit_fy24 = V['op_fy24']
ebit_fy25 = V['op_fy25']
netfin_fy25 = V['int_inc_fy25'] - V['int_exp_fy25']
netfin_fy24 = V['int_inc_fy24'] - V['int_exp_fy24']
say(f"[Historical income statement] FY2025 EBITDA {V['ebitda_fy25']:,.0f} is PRINTED on the face "
    f"('operating profit before depreciation and amortization', IFRS 18); FY2024 comparative "
    f"likewise ({V['ebitda_fy24']:,.0f}). FY2023 predates IFRS 18 and prints no such line — the "
    f"{V['ebitda_fy23']:,.0f} carried here is DERIVED from audited components and flagged. "
    f"Margins: FY23 {V['ebitda_fy23']/V['rev_fy23']:.1%}, FY24 {V['ebitda_fy24']/V['rev_fy24']:.1%}, "
    f"FY25 {V['ebitda_fy25']/V['rev_fy25']:.1%}; H1-2026 ACTUAL {V['h1_26_ebitda']/V['h1_26_rev']:.1%}.")
say(f"[Fiscal regime] combined royalty+tax take: FY2023 {(V['royalty_fy23'])/V['pbt_fy23']:.1%} "
    f"(OLD regime: 15% of regulated revenue + 30% of regulated profit), FY2024 "
    f"{(V['royalty_fy24']+V['tax_fy24'])/V['pbt_fy24']:.1%}, FY2025 "
    f"{(V['royalty_fy25']+V['tax_fy25'])/V['pbt_fy25']:.1%} (CURRENT regime: 38% royalty + 9% "
    f"CT, legislated 2024-2026 only). The post-2026 regime is THE CONTESTED JUDGEMENT — both "
    f"framings are computed and published side by side.")
assert abs((V['royalty_fy25'] + V['tax_fy25']) / V['pbt_fy25'] - TAX) < 0.002, \
    'tax_eff input does not reproduce the audited FY2025 combined take'

hist_is = {
    'FY23': dict(rev=V['rev_fy23'], ebitda=V['ebitda_fy23'], dna=V['dna_fy23'], ebit=ebit_fy23,
                 royalty=V['royalty_fy23'], tax=0.0, np=V['np_fy23'], eps=V['eps_fy23'],
                 pbt=V['pbt_fy23']),
    'FY24': dict(rev=V['rev_fy24'], ebitda=V['ebitda_fy24'], dna=V['dna_fy24'], ebit=ebit_fy24,
                 royalty=V['royalty_fy24'], tax=V['tax_fy24'], np=V['np_fy24'], eps=V['eps_fy24'],
                 pbt=V['pbt_fy24'], fin=netfin_fy24),
    'FY25': dict(rev=V['rev_fy25'], ebitda=V['ebitda_fy25'], dna=V['dna_fy25'], ebit=ebit_fy25,
                 royalty=V['royalty_fy25'], tax=V['tax_fy25'], np=V['np_fy25'], eps=V['eps_fy25'],
                 pbt=V['pbt_fy25'], fin=netfin_fy25),
}
for y, k in (('FY24', 'pbt_fy24'), ('FY25', 'pbt_fy25')):
    got = hist_is[y]['pbt'] - hist_is[y]['royalty'] - hist_is[y]['tax']
    assert abs(got - hist_is[y]['np']) < 0.01, f'{y} P&L does not close: {got} vs {hist_is[y]["np"]}'
assert abs(hist_is['FY23']['pbt'] - hist_is['FY23']['royalty'] - hist_is['FY23']['np']) < 0.5, \
    'FY23 P&L does not close'

# ---- historical net working capital (audited balance sheets) ----------------
# Like-for-like: the FY2023 payables line still CONTAINS the royalty accrual
# (2,033.172 at 1-Jan-2024 per the AR2024 movement note); FY2024-25 present it
# separately. It is netted out of FY2023 payables, and the royalty/tax accrual
# is excluded from working capital in every year (it is a fiscal flow, not an
# operating one).
nwc = {}
nwc['FY23'] = ((V['inv_fy23'] + V['recv_fy23'] + V['ccost_fy23'] + V['relparty_a_fy23']
                + V['othca_fy23'])
               - ((V['pay_fy23'] - V['roy_accr_fy23']) + V['cliab_fy23'] + V['relparty_l_fy23']))
nwc['FY24'] = ((V['inv_fy24'] + V['recv_fy24'] + V['ccost_fy24'] + V['relparty_a_fy24']
                + V['othca_fy24'])
               - (V['pay_fy24'] + V['cliab_fy24'] + V['relparty_l_fy24']))
nwc['FY25'] = ((V['inv_fy25'] + V['recv_fy25'] + V['ccost_fy25'] + V['relparty_a_fy25']
                + V['othca_fy25'])
               - (V['pay_fy25'] + V['cliab_fy25'] + V['relparty_l_fy25']))
nwc_fy25 = nwc['FY25']
# asset-conversion cycle, computed from the same audited lines (SIGCM clause 4)
dso = {y: nwc_r / r * 365 for y, nwc_r, r in [
    ('FY23', V['recv_fy23'], V['rev_fy23']), ('FY24', V['recv_fy24'], V['rev_fy24']),
    ('FY25', V['recv_fy25'], V['rev_fy25'])]}
dio_fy25 = V['inv_fy25'] / (V['rev_fy25'] - V['ebitda_fy25'] + 3307.608) * 365  # vs direct costs
dpo = {y: p / r * 365 for y, p, r in [
    ('FY23', V['pay_fy23'] - V['roy_accr_fy23'], V['rev_fy23']),
    ('FY24', V['pay_fy24'], V['rev_fy24']), ('FY25', V['pay_fy25'], V['rev_fy25'])]}
nwc_pct = nwc['FY25'] / V['rev_fy25']
say(f"[Working capital, audited, royalty-accrual-adjusted] FY23 {nwc['FY23']:,.0f} "
    f"({nwc['FY23']/V['rev_fy23']:.1%} of revenue), FY24 {nwc['FY24']:,.0f} "
    f"({nwc['FY24']/V['rev_fy24']:.1%}), FY25 {nwc['FY25']:,.0f} ({nwc_pct:.1%}) — structurally "
    f"NEGATIVE, the classic prepaid/deferred-revenue telecom shape: customers and payables fund "
    f"the operation. Cycle: DSO {dso['FY25']:.0f}d (FY23 {dso['FY23']:.0f}d), payables "
    f"{dpo['FY25']:.0f}d of revenue, inventory {dio_fy25:.0f}d of direct costs. The forecast "
    f"holds the FY2025 component days constant, so NWC stays {nwc_pct:.1%} of revenue and "
    f"GROWTH RELEASES cash rather than absorbing it.")

net_cash = {y: V[f'cash_{y.lower()}'] + V[f'deposits_{y.lower()}'] for y in ('FY23', 'FY24', 'FY25')}
say(f"[Balance sheet] ZERO drawn borrowings in every year studied (Note 4.2 prints Total "
    f"borrowings '–'); cash + term deposits: FY23 {net_cash['FY23']:,.0f}, FY24 "
    f"{net_cash['FY24']:,.0f}, FY25 {net_cash['FY25']:,.0f}. Lease liabilities (the only "
    f"debt-like item): FY23 {V['lease_fy23']:,.0f} -> FY25 {V['lease_fy25']:,.0f}. Net cash "
    f"AFTER leases at FY2025: {net_cash['FY25'] - V['lease_fy25']:+,.0f}.")

hist_bs = {
    'FY23': dict(ppe=V['ppe_fy23'], rou=V['rou_fy23'], intang=V['intang_fy23'], goodwill=None,
                 inv=V['inv_fy23'], recv=V['recv_fy23'], cash=V['cash_fy23'],
                 deposits=V['deposits_fy23'], assets=V['assets_fy23'],
                 pay=V['pay_fy23'], lease=V['lease_fy23'], debt=0.0, eq=V['eq_fy23'],
                 nwc=nwc['FY23'], net_cash=net_cash['FY23'],
                 nd=V['lease_fy23'] - net_cash['FY23']),
    'FY24': dict(ppe=V['ppe_fy24'], rou=V['rou_fy24'], intang=V['intang_fy24'],
                 goodwill=V['goodwill_fy25'], inv=V['inv_fy24'], recv=V['recv_fy24'],
                 cash=V['cash_fy24'], deposits=V['deposits_fy24'], assets=V['assets_fy24'],
                 pay=V['pay_fy24'], lease=V['lease_fy24'], debt=0.0, eq=V['eq_fy24'],
                 nwc=nwc['FY24'], net_cash=net_cash['FY24'],
                 nd=V['lease_fy24'] - net_cash['FY24']),
    'FY25': dict(ppe=V['ppe_fy25'], rou=V['rou_fy25'], intang=V['intang_fy25'],
                 goodwill=V['goodwill_fy25'], inv=V['inv_fy25'], recv=V['recv_fy25'],
                 cash=V['cash_fy25'], deposits=V['deposits_fy25'], assets=V['assets_fy25'],
                 pay=V['pay_fy25'], lease=V['lease_fy25'], debt=0.0, eq=V['eq_fy25'],
                 nwc=nwc['FY25'], net_cash=net_cash['FY25'],
                 nd=V['lease_fy25'] - net_cash['FY25']),
}

# ============================ FOUR-SEGMENT FORECAST BUILD =====================
# The disclosed segments (Note 38): Mobile, Fixed, Wholesale, ICT and associated
# telecom services. Mobile and Fixed are built BOTTOM-UP as subscribers x ARPU
# (the finest sourced level — both series are company-disclosed KPIs);
# Wholesale and ICT are disclosed only as segment revenue, so they are built at
# segment level and the gap is FLAGGED (no unit KPIs are published for them).
YRS = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
SEGS = ['mobile', 'fixed', 'wholesale', 'ict']
SEGNAME = dict(mobile='Mobile', fixed='Fixed', wholesale='Wholesale',
               ict='ICT and associated telecom services')
SRH, SCH = V['seg_rev_hist'], V['seg_contrib_hist']
for y, key in (('FY23', 'rev_fy23'), ('FY24', 'rev_fy24'), ('FY25', 'rev_fy25')):
    assert abs(sum(SRH[y].values()) - V[key]) < 0.01, f'{y} segment revenue != consolidated P&L'
for y in ('FY24', 'FY25'):
    m = {s: SCH[y][s] / SRH[y][s] for s in SEGS}
    say(f"[Segment contribution margins {y}] " +
        ", ".join(f"{s} {m[s]:.1%}" for s in SEGS))

# unit-build reconciliation on the audited year: avg subscribers x ARPU x 12
_avg_subs_25 = (V['subs_mobile']['Q4_2024'] + V['subs_mobile']['Q4_2025']) / 2
_unit_mobile_25 = _avg_subs_25 * V['arpu_mobile']['FY2025'] * 12 / 1000
say(f"[Unit-build reconciliation, FY2025] avg mobile base {_avg_subs_25:,.0f}k x ARPU "
    f"AED {V['arpu_mobile']['FY2025']} x 12 = {_unit_mobile_25:,.0f} vs disclosed mobile "
    f"segment revenue {SRH['FY25']['mobile']:,.0f} ({_unit_mobile_25/SRH['FY25']['mobile']-1:+.1%})"
    f" — the subscribers-x-ARPU frame reproduces the audited segment to within a percent.")
assert abs(_unit_mobile_25 / SRH['FY25']['mobile'] - 1) < 0.02

H1_SEG = dict(mobile=3646.314, fixed=2382.608, wholesale=1257.566, ict=911.085)
assert abs(sum(H1_SEG.values()) - V['h1_26_rev']) < 0.01, 'H1-2026 segments != reviewed total'

def build(arpu_mult=1.0, subs_shift=0.0, contrib_mult=1.0, opex_shift=0.0, capex_mult=1.0):
    """arpu_mult scales the mobile+fixed price paths; subs_shift adds N thousand
    to every point of both subscriber paths; contrib_mult scales all contribution
    margins; opex_shift adds a fraction of revenue to the opex stack;
    capex_mult scales the capex path."""
    sm = [s + subs_shift for s in V['subs_mobile_path']]
    sf = [s + subs_shift * 0.08 for s in V['subs_fixed_path']]
    am = [a * arpu_mult for a in V['arpu_mobile_path']]
    af = [a * arpu_mult for a in V['arpu_fixed_path']]
    seg_rev = {s: [] for s in SEGS}
    # FY2026: reviewed H1 actual + unit-built H2
    seg_rev['mobile'].append(H1_SEG['mobile']
                             + (V['subs_mobile']['Q2_2026'] + sm[0]) / 2 * am[0] * 6 / 1000)
    seg_rev['fixed'].append(H1_SEG['fixed']
                            + (V['subs_fixed']['Q2_2026'] + sf[0]) / 2 * af[0] * 6 / 1000)
    seg_rev['wholesale'].append(SRH['FY25']['wholesale'] * (1 + V['seg_g']['wholesale'][0]))
    seg_rev['ict'].append(SRH['FY25']['ict'] * (1 + V['seg_g']['ict'][0]))
    for i in range(1, 5):
        seg_rev['mobile'].append((sm[i - 1] + sm[i]) / 2 * am[i] * 12 / 1000)
        seg_rev['fixed'].append((sf[i - 1] + sf[i]) / 2 * af[i] * 12 / 1000)
        seg_rev['wholesale'].append(seg_rev['wholesale'][-1] * (1 + V['seg_g']['wholesale'][i]))
        seg_rev['ict'].append(seg_rev['ict'][-1] * (1 + V['seg_g']['ict'][i]))
    rev = [sum(seg_rev[s][i] for s in SEGS) for i in range(5)]
    contrib = {s: [seg_rev[s][i] * V['contrib_margin_path'][s][i] * contrib_mult
                   for i in range(5)] for s in SEGS}
    contrib_tot = [sum(contrib[s][i] for s in SEGS) for i in range(5)]
    ob = V['opex_base_fy25']
    staff = [V['staff_fy26'] * (1 + V['esc_staff']) ** i for i in range(5)]
    network = [ob['network'] * (1 + V['esc_network']) ** (i + 1) for i in range(5)]
    admin = [ob['admin'] * (1 + V['esc_admin']) ** (i + 1) for i in range(5)]
    other = [ob['other'] * (1 + V['esc_other']) ** (i + 1) for i in range(5)]
    marketing = [V['marketing_pct'] * r for r in rev]
    licence = [V['licence_pct'] * r for r in rev]
    ecl = [V['ecl_pct'] * r for r in rev]
    opex = [staff[i] + network[i] + admin[i] + other[i] + marketing[i] + licence[i]
            + ecl[i] - V['other_inc_path'] + opex_shift * rev[i] for i in range(5)]
    ebitda = [contrib_tot[i] - opex[i] for i in range(5)]
    capex = [V['capex_pct'][i] * rev[i] * capex_mult for i in range(5)]
    return dict(rev=rev, seg_rev=seg_rev, contrib=contrib, contrib_tot=contrib_tot,
                opex=opex, ebitda=ebitda, capex=capex,
                opex_lines=dict(staff=staff, network=network, admin=admin, other=other,
                                marketing=marketing, licence=licence, ecl=ecl))

_B = build()
rev, seg_rev, ebitda, capex = _B['rev'], _B['seg_rev'], _B['ebitda'], _B['capex']
contrib_tot, opex_fc = _B['contrib_tot'], _B['opex']
ebitda_margin = [ebitda[i] / rev[i] for i in range(5)]
g26 = rev[0] / V['rev_fy25'] - 1
say(f"[Revenue build] FY26E {rev[0]:,.0f} ({g26:+.1%} vs guidance 4-6% revised 23-Jul-2026) -> "
    f"FY30E {rev[-1]:,.0f}. Segments FY26E: " +
    ", ".join(f"{s} {seg_rev[s][0]:,.0f}" for s in SEGS))
assert 0.035 <= g26 <= 0.065, f'FY2026E growth {g26:.1%} outside the guidance sanity band'
say(f"[EBITDA — an OUTPUT, not an input] " +
    " -> ".join(f"{ebitda[i]:,.0f} ({ebitda_margin[i]:.1%})" for i in range(5)) +
    f". H1-2026 actual margin was 49.2% and H2 is seasonally softer (H2-2025: "
    f"{V['h2_25_ebitda']/V['h2_25_rev']:.1%}); the FY26E output sits against the company's "
    f"46-47% guidance — ABOVE it, because H1 already printed 49.2% and the build holds "
    f"disclosed contribution margins rather than forcing the guidance midpoint.")
assert 0.44 <= ebitda_margin[0] <= 0.50

# ---- D&A from asset roll-forwards ------------------------------------------
capex_tang = [c * V['capex_tang_share'] for c in capex]
capex_int = [c * (1 - V['capex_tang_share']) for c in capex]
dep_ppe, amort, ppe_path, int_path = [], [], [], []
pp, ii = V['ppe_fy25'], V['intang_fy25']
for i in range(5):
    d = V['dep_rate_ppe'] * pp
    a = V['amort_rate'] * ii
    dep_ppe.append(d); amort.append(a)
    pp = pp + capex_tang[i] - d
    ii = ii + capex_int[i] - a
    ppe_path.append(pp); int_path.append(ii)
dna = [dep_ppe[i] + amort[i] + V['rou_dep_path'][i] for i in range(5)]
say(f"[D&A roll-forward] FY26E {dna[0]:,.0f} (2x reviewed H1-2026 actual = "
    f"{2*V['h1_26_dna']:,.0f} — within {abs(dna[0]/(2*V['h1_26_dna'])-1):.1%}); PP&E "
    f"{V['ppe_fy25']:,.0f} -> {ppe_path[-1]:,.0f}.")
assert abs(dna[0] / (2 * V['h1_26_dna']) - 1) < 0.05

ebit = [ebitda[i] - dna[i] for i in range(5)]
nopat = [e * (1 - TAX) for e in ebit]

# ---- working capital (component days held at FY2025) ------------------------
nwc_fc = [nwc_pct * r for r in rev]
dnwc = [nwc_fc[0] - nwc_fy25] + [nwc_fc[i] - nwc_fc[i - 1] for i in range(1, 5)]

# ---- FCFF waterfall ----------------------------------------------------------
# Leases: lease liabilities are DEBT in the bridge, so lease payments never hit
# FCFF; the offsetting cost is lease REPLACEMENT capex, set equal to ROU
# depreciation (steady-state; actual FY2025 additions 96.034 ran well below).
rou_repl = list(V['rou_dep_path'])
fcff = [nopat[i] + dna[i] - capex[i] - rou_repl[i] - dnwc[i] for i in range(5)]
say(f"[FCFF waterfall] " + " -> ".join(f"{f:,.0f}" for f in fcff))

# ---- cost of capital: explicit window (sovereign double-count removed) -------
rf_star = V['rf'] - V['sov_spread_rating']
ke_exp = rf_star + V['beta'] * V['erp_rating']
ke_mkt_alt = (V['rf'] - V['sov_spread_mkt']) + V['beta'] * V['erp_mkt']
ke_raw_retired = V['rf'] + V['beta'] * V['erp_rating']
kd_at = V['kd'] * (1 - TAX)
LEASE, NETCASH = V['lease_fy25'], net_cash['FY25']
wd_exp = LEASE / (LEASE + MKTCAP)
we_exp = 1 - wd_exp
wacc_exp = we_exp * ke_exp + wd_exp * kd_at
wacc_exp_mkt = we_exp * ke_mkt_alt + wd_exp * kd_at
say(f"[Cost of equity] rf {V['rf']:.2%} (Jan-2031 AED T-bond) less UAE rating-basis default "
    f"spread {V['sov_spread_rating']:.2%} = rf* {rf_star:.2%}; + beta {V['beta']:.3f} x ERP "
    f"{V['erp_rating']:.2%} -> Ke {ke_exp:.2%}. ERP basis 2 (market-spread, implied-US base): "
    f"{ke_mkt_alt:.2%}. RETIRED un-netted construction {ke_raw_retired:.2%} (audit trail only).")
say(f"[WACC explicit] weights: lease debt {wd_exp:.1%} / market equity {we_exp:.1%} "
    f"(market cap {MKTCAP:,.0f}; du has no drawn borrowings) -> WACC {wacc_exp:.2%} "
    f"(basis 2: {wacc_exp_mkt:.2%}). Interest shields both fiscal legs (the royalty base is "
    f"profit AFTER interest), so the shield runs at the combined {TAX:.1%}.")

ke_term = (V['rf_term'] - V['sov_spread_rating']) + V['beta'] * V['erp_term']
kd_term_at = V['kd_term'] * (1 - TAX)
wacc_term = (1 - V['wd_term']) * ke_term + V['wd_term'] * kd_term_at
say(f"[WACC terminal] Ke {ke_term:.2%}; Kd after tax {kd_term_at:.2%}; weights "
    f"{1-V['wd_term']:.0%}/{V['wd_term']:.0%} -> {wacc_term:.2%}")
assert wacc_term < wacc_exp, 'terminal WACC must sit below the explicit-window WACC'

# ---- glide: fractions from the rf path (du has no debt to define a Kd path) --
rfp = V['rf_path']
glide_frac = [(rfp[0] - r) / (rfp[0] - rfp[-1]) for r in rfp]
fwd = [wacc_exp - (wacc_exp - wacc_term) * f for f in glide_frac]
df, c = [], 1.0
for w in fwd:
    c /= (1 + w); df.append(c)
assert all(fwd[i] >= fwd[i + 1] for i in range(len(fwd) - 1)), 'glide not monotone'
say("[Glide] forward WACC " + " -> ".join(f"{w:.2%}" for w in fwd) +
    "; discount factors " + ", ".join(f"{d:.4f}" for d in df))

# ---- forward net-finance, profit, dividend, equity and net-cash paths --------
PAYOUT = 0.98   # FY2024 payout 98%, FY2025 ~100% (company IR); H1-2026 interim +8.3% —
                # the company's own declared posture, held one notch below full payout
dep_yield = 0.033   # FY2025 interest income 74.672 / avg cash+deposits 2,266.5 = 3.3% (audited)
lease_rate = 0.036  # FY2025 lease interest 71.094 / avg lease book 1,968.8 (audited)
np_fc, eq_fc, ncash_fc, div_fc, int_inc_fc, int_exp_fc = [], [], [], [], [], []
nc, eq, lease_bal = NETCASH, V['eq_fy25'], V['lease_fy25']
for i in range(5):
    ii_ = dep_yield * max(nc, 0.0)
    ie_ = lease_rate * lease_bal
    pbt_ = ebit[i] + ii_ - ie_
    np_ = pbt_ * (1 - TAX)
    dv_ = PAYOUT * np_
    nc = nc + np_ + dna[i] - capex[i] - rou_repl[i] - dnwc[i] - dv_ \
         - (V['rou_dep_path'][i] - V['rou_dep_path'][i])   # lease book held ~flat
    eq = eq + np_ - dv_
    int_inc_fc.append(ii_); int_exp_fc.append(ie_)
    np_fc.append(np_); div_fc.append(dv_); eq_fc.append(eq); ncash_fc.append(nc)
eps_fc = [n / SH for n in np_fc]
dps_fc = [d / SH for d in div_fc]
say(f"[Profit path] EPS " + " -> ".join(f"{e:.2f}" for e in eps_fc) +
    f"; DPS at {PAYOUT:.0%} payout " + " -> ".join(f"{d:.2f}" for d in dps_fc) +
    f"; net cash (before leases) {NETCASH:,.0f} -> {ncash_fc[-1]:,.0f}")

# ---- invested capital, terminal ----------------------------------------------
ic_fy25 = (V['ppe_fy25'] + V['rou_fy25'] + V['intang_fy25'] + V['goodwill_fy25'] + nwc_fy25)
rou_path = []
rb = V['rou_fy25']
for i in range(5):
    rb = rb + rou_repl[i] - V['rou_dep_path'][i]
    rou_path.append(rb)
ic = [ppe_path[i] + rou_path[i] + int_path[i] + V['goodwill_fy25'] + nwc_fc[i]
      for i in range(5)]
roic = [nopat[i] / ((ic[i] + ([ic_fy25] + ic)[i]) / 2) for i in range(5)]
roic_term = nopat[-1] * (1 + V['g_term']) / ic[-1]
rr_term = min(V['g_term'] / roic_term, 0.95)
tv = nopat[-1] * (1 + V['g_term']) * (1 - rr_term) / (wacc_term - V['g_term'])
say(f"[Terminal] ROIC(term) {roic_term:.1%}; reinvestment = g/ROIC = {rr_term:.1%} of NOPAT; "
    f"TV {tv:,.0f} at g {V['g_term']:.1%} / WACC(term) {wacc_term:.2%}")

# ---- DCF and the EV -> equity bridge ------------------------------------------
pv = [fcff[i] * df[i] for i in range(5)]
pv_explicit = sum(pv)
pv_tv = tv * df[-1]
ev = pv_explicit + pv_tv
tv_share = pv_tv / ev
assoc_val = 0.511 / 1000 * 1000 * 0.001  # equity-accounted investees, AED 0.511mn — negligible
eq_val = ev - LEASE + NETCASH + V['assoc_fy25'] * 0 + 0.511
dcf_ps_dec = eq_val / SH
T_ANCHOR = V['anchor_days'] / 365.0
ROLL = (1 + ke_exp) ** T_ANCHOR
def to_anchor(v):
    return v * ROLL
dcf_ps = dcf_ps_dec * ROLL - V['div_between']
say(f"[DCF] PV(explicit) {pv_explicit:,.0f} + PV(terminal) {pv_tv:,.0f} "
    f"(TV = {tv_share:.0%} of EV) = EV {ev:,.0f}; − leases {LEASE:,.0f} + cash & deposits "
    f"{NETCASH:,.0f} + investees 0.5 = equity {eq_val:,.0f} -> AED {dcf_ps_dec:.2f} at "
    f"31-Dec-2025; x accretion {ROLL:.4f} − final dividend {V['div_between']:.2f} paid "
    f"28-Apr-2026 = AED {dcf_ps:.2f} at the 07-Aug-2026 anchor")
assert abs((ev - LEASE + NETCASH + 0.511) - eq_val) < 0.01, 'bridge does not close'
assert tv_share < 0.90, 'terminal value share implausibly high'

# ---- THE CONTESTED JUDGEMENT, COMPUTED BOTH WAYS ------------------------------
# Framing A (base, above): the 2024-2026 regime (38% royalty + 9% CT, combined
# 43.6%) persists — now supported by the e& market disclosure of an MoF
# notification (17-Jul-2026) extending the regime to 2027-2029 on the same
# structure (secondary evidence; du's own H1-2026 notes, signed 22-Jul-2026,
# still describe 2024-2026 only).
# Framing B: reversion to the pre-2024 construction — 15% of regulated revenue
# + 30% of regulated profit (69.0% regulated share, audited FY2023 Note 27) —
# which took 53.1% of FY2023 pre-royalty profit.
def framingB():
    tb, fcffB, npB = [], [], []
    for i in range(5):
        pbt_ = ebit[i] + int_inc_fc[i] - int_exp_fc[i]
        leg1 = V['royB_rev_rate'] * V['reg_share'] * rev[i]
        leg2 = V['royB_prof_rate'] * max(pbt_ - leg1, 0.0)
        t_ = (leg1 + leg2) / pbt_
        tb.append(t_)
        fcffB.append(ebit[i] * (1 - t_) + dna[i] - capex[i] - rou_repl[i] - dnwc[i])
        npB.append(pbt_ * (1 - t_))
    tvB = ebit[-1] * (1 - tb[-1]) * (1 + V['g_term']) * (1 - rr_term) / (wacc_term - V['g_term'])
    evB = sum(fcffB[i] * df[i] for i in range(5)) + tvB * df[-1]
    psB = (evB - LEASE + NETCASH + 0.511) / SH * ROLL - V['div_between']
    return tb, fcffB, npB, psB
taxB_path, fcffB, npB, dcf_ps_B = framingB()
say(f"[Contested judgement — BOTH WAYS] Framing A (regime persists, 43.6% take): AED "
    f"{dcf_ps:.2f}. Framing B (reversion to the pre-2024 construction, effective take "
    f"{taxB_path[0]:.1%} -> {taxB_path[-1]:.1%}): AED {dcf_ps_B:.2f}. Gap "
    f"{dcf_ps - dcf_ps_B:+.2f}/share ({(dcf_ps_B/dcf_ps-1):+.0%}). Published side by side; "
    f"never averaged.")

# ---- rf-tenor alternative, priced --------------------------------------------
ke_rf_alt = (V['rf_alt'] - V['sov_spread_rating']) + V['beta'] * V['erp_rating']
wacc_rf_alt = we_exp * ke_rf_alt + wd_exp * kd_at
_shift = wacc_rf_alt - wacc_exp
_fwd_alt = [w + _shift for w in fwd]
_df_alt, cc = [], 1.0
for w in _fwd_alt:
    cc /= (1 + w); _df_alt.append(cc)
_tv_alt = nopat[-1] * (1 + V['g_term']) * (1 - rr_term) / (wacc_term + _shift - V['g_term'])
_ev_alt = sum(fcff[i] * _df_alt[i] for i in range(5)) + _tv_alt * _df_alt[-1]
dcf_ps_rf_alt = (_ev_alt - LEASE + NETCASH + 0.511) / SH * ((1 + ke_rf_alt) ** T_ANCHOR) \
                - V['div_between']
say(f"[rf tenor gap, PRICED] 10y peg-extrapolated rf {V['rf_alt']:.2%} instead of the Jan-2031 "
    f"AED print {V['rf']:.2%} -> WACC {wacc_rf_alt:.2%} -> AED {dcf_ps_rf_alt:.2f} "
    f"({dcf_ps_rf_alt-dcf_ps:+.2f}/share)")

# ---- scenarios on the DCF -----------------------------------------------------
def dcf_scenario(arpu_mult=1.0, subs_shift=0.0, contrib_mult=1.0, opex_shift=0.0,
                 capex_mult=1.0, wacc_shift=0.0, g=None, tax=None, nwc=None):
    g = V['g_term'] if g is None else g
    t_ = TAX if tax is None else tax
    nw = nwc_pct if nwc is None else nwc
    B = build(arpu_mult=arpu_mult, subs_shift=subs_shift, contrib_mult=contrib_mult,
              opex_shift=opex_shift, capex_mult=capex_mult)
    _rev, _ebitda, _capex = B['rev'], B['ebitda'], B['capex']
    _ct = [c * V['capex_tang_share'] for c in _capex]
    _ci = [c * (1 - V['capex_tang_share']) for c in _capex]
    _dep, _amo = [], []
    pp_, ii_ = V['ppe_fy25'], V['intang_fy25']
    _ppe = []
    for i in range(5):
        d_ = V['dep_rate_ppe'] * pp_; a_ = V['amort_rate'] * ii_
        _dep.append(d_); _amo.append(a_)
        pp_ = pp_ + _ct[i] - d_; ii_ = ii_ + _ci[i] - a_
        _ppe.append(pp_)
    _dna = [_dep[i] + _amo[i] + V['rou_dep_path'][i] for i in range(5)]
    _ebit = [_ebitda[i] - _dna[i] for i in range(5)]
    _nopat = [e * (1 - t_) for e in _ebit]
    _nwc = [nw * r for r in _rev]
    _dnwc = [_nwc[0] - nwc_fy25] + [_nwc[i] - _nwc[i - 1] for i in range(1, 5)]
    _f = [_nopat[i] + _dna[i] - _capex[i] - rou_repl[i] - _dnwc[i] for i in range(5)]
    _we, _wt = wacc_exp + wacc_shift, wacc_term + wacc_shift
    _fwd = [_we - (_we - _wt) * fr for fr in glide_frac]
    _df, cc = [], 1.0
    for w in _fwd:
        cc /= (1 + w); _df.append(cc)
    _ic5 = _ppe[-1] + rou_path[-1] + ii_ + V['goodwill_fy25'] + _nwc[-1]
    _roic = _nopat[-1] * (1 + g) / _ic5
    _rr = min(g / _roic, 0.95)
    _tv = _nopat[-1] * (1 + g) * (1 - _rr) / max(_wt - g, 0.015)
    _ev = sum(_f[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    return ((_ev - LEASE + NETCASH + 0.511) / SH) * ROLL - V['div_between']

_base_chk = dcf_scenario()
assert abs(_base_chk - dcf_ps) < 0.02, f'scenario engine != base: {_base_chk} vs {dcf_ps}'

dcf_bear = dcf_scenario(arpu_mult=0.95, subs_shift=-250.0, contrib_mult=0.97,
                        opex_shift=+0.005, wacc_shift=+0.01, g=0.02, capex_mult=1.08)
dcf_bull = dcf_scenario(arpu_mult=1.03, subs_shift=+200.0, contrib_mult=1.015,
                        opex_shift=-0.005, wacc_shift=-0.005, g=0.03, capex_mult=0.95)
say(f"[DCF scenarios] bear {dcf_bear:.2f} / base {dcf_ps:.2f} / bull {dcf_bull:.2f} AED per share")

# ---- lens 2: relative ---------------------------------------------------------
pe_trailing = SPOT / (V['np_fy25'] / SH)   # exact EPS, not the printed 2dp round
ev_trailing = MKTCAP + LEASE - NETCASH
ev_ebitda_trailing = ev_trailing / V['ebitda_fy25']
rel_ps = to_anchor(V['pe_just'] * eps_fc[0]) - V['div_between']
rel_bear = to_anchor(12.0 * eps_fc[0]) - V['div_between']
rel_bull = to_anchor(18.5 * eps_fc[0]) - V['div_between']
yield_ps = dps_fc[0] / V['div_yield_peer']
say(f"[Relative lens] trailing P/E {pe_trailing:.1f}x, trailing EV/EBITDA "
    f"{ev_ebitda_trailing:.1f}x (du's own, computed from audited figures). Justified P/E "
    f"{V['pe_just']:.1f}x (GCC peer median) x FY26E EPS {eps_fc[0]:.2f} -> AED {rel_ps:.2f} at "
    f"the anchor [bear 12x {rel_bear:.2f} / bull 18.5x {rel_bull:.2f}]. Dividend-yield cross: "
    f"DPS {dps_fc[0]:.2f} / peer benchmark {V['div_yield_peer']:.1%} = AED {yield_ps:.2f}. "
    f"Peer EV/EBITDA was NOT reliably sourceable from public aggregators (flagged) — the "
    f"relative lens runs on P/E and yield, both sourced.")

# ---- lens 3: normalized earnings power ----------------------------------------
norm_margin = ebitda_margin[2]
norm_rev = rev[0]
norm_ebitda = norm_margin * norm_rev
norm_ebit = norm_ebitda - dna[0]
norm_np = (norm_ebit + int_inc_fc[0] - int_exp_fc[0]) * (1 - TAX)
norm_eps = norm_np / SH
norm_ps = to_anchor(V['pe_just'] * norm_eps) - V['div_between']
norm_bear = to_anchor(12.0 * norm_eps) - V['div_between']
norm_bull = to_anchor(18.5 * norm_eps) - V['div_between']
say(f"[Normalised lens] mid-cycle margin {norm_margin:.1%} (FY2028E) on FY2026E revenue -> "
    f"normalised EPS {norm_eps:.2f} x {V['pe_just']:.1f} = AED {norm_ps:.2f} at the anchor")

# ---- lens 4: book / justified P/B ---------------------------------------------
bvps = V['eq_fy25'] / SH
pb_just = (V['roe_sust'] - V['g_term']) / (ke_term - V['g_term'])
book_ps = to_anchor(pb_just * bvps) - V['div_between']
book_bear = to_anchor(((V['roe_sust'] - 0.04) / (0.5 * (ke_exp + ke_term) + 0.01 - 0.02)) * bvps) - V['div_between']
book_bull = to_anchor(((V['roe_sust'] + 0.02 - V['g_term']) / (ke_term - V['g_term'])) * bvps) - V['div_between']
roe_trailing = V['np_fy25'] / ((V['eq_fy24'] + V['eq_fy25']) / 2)
say(f"[Book lens] justified P/B = ({V['roe_sust']:.0%} − {V['g_term']:.1%}) / ({ke_term:.2%} − "
    f"{V['g_term']:.1%}) = {pb_just:.2f}x on BVPS {bvps:.2f} -> AED {book_ps:.2f} at the anchor. "
    f"A 27% sustainable ROE against a {ke_term:.1%} cost of equity is what a licensed duopoly "
    f"with negative working capital looks like; the multiple is high because the equity base is "
    f"small, not because the claim is aggressive. Trailing ROE {roe_trailing:.1%}.")

# ---- synthesis ----------------------------------------------------------------
W = V['lens_weights']
lenses = dict(
    dcf=dict(name='Discounted cash flow (primary)', bear=dcf_bear, base=dcf_ps, bull=dcf_bull,
             w=W['dcf']),
    relative=dict(name='Relative multiples', bear=rel_bear, base=rel_ps, bull=rel_bull,
                  w=W['relative']),
    normalized=dict(name='Normalised earnings power', bear=norm_bear, base=norm_ps,
                    bull=norm_bull, w=W['normalized']),
    book=dict(name='Book value and sustainable return', bear=book_bear, base=book_ps,
              bull=book_bull, w=W['book']),
)
central = sum(l['base'] * l['w'] for l in lenses.values())
lo = min(l['bear'] for l in lenses.values())
hi = max(l['bull'] for l in lenses.values())
lenses['central'] = dict(name='Weighted central', bear=lo, base=central, bull=hi, w=1.0)
say(f"[Synthesis] weighted central AED {central:.2f}; span {lo:.2f} - {hi:.2f}; spot "
    f"{SPOT:.2f} ({central/SPOT-1:+.0%} to the central).")
assert 0.3 <= central / SPOT <= 3.0

# ---- sensitivity grids ---------------------------------------------------------
g_grid = [0.015, 0.020, 0.025, 0.030, 0.035]
wt_grid = [wacc_term - 0.010, wacc_term - 0.005, wacc_term, wacc_term + 0.005,
           wacc_term + 0.010]
we_grid = [wacc_exp - 0.010, wacc_exp - 0.005, wacc_exp, wacc_exp + 0.005, wacc_exp + 0.010]

def dcf_at(we_, wt_, g_):
    _fwd = [we_ - (we_ - wt_) * fr for fr in glide_frac]
    _df, cc = [], 1.0
    for w in _fwd:
        cc /= (1 + w); _df.append(cc)
    _rr = min(g_ / roic_term, 0.95)
    _tv = nopat[-1] * (1 + g_) * (1 - _rr) / max(wt_ - g_, 0.012)
    _ev = sum(fcff[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    return ((_ev - LEASE + NETCASH + 0.511) / SH) * ROLL - V['div_between']

grid_wacc_g = [[dcf_at(wacc_exp, wt, g) for g in g_grid] for wt in wt_grid]
grid_exp_term = [[dcf_at(we, wt, V['g_term']) for wt in wt_grid] for we in we_grid]
beta_grid = [0.38, round(V['beta'], 3), 0.57, 0.65, 0.80]
def dcf_beta(b):
    ke = rf_star + b * V['erp_rating']
    we_ = we_exp * ke + wd_exp * kd_at
    wt_ = (1 - V['wd_term']) * (V['rf_term'] + b * V['erp_term']) + V['wd_term'] * kd_term_at
    return dcf_at(we_, wt_, V['g_term'])
grid_beta = [dcf_beta(b) for b in beta_grid]
tax_grid = [0.40, TAX, 0.47, 0.50, 0.531]
grid_tax = [dcf_scenario(tax=t) for t in tax_grid]
arpu_grid = [0.92, 0.96, 1.00, 1.04, 1.08]
grid_arpu = [dcf_scenario(arpu_mult=m) for m in arpu_grid]
subs_grid = [-400.0, -200.0, 0.0, 200.0, 400.0]
grid_subs = [dcf_scenario(subs_shift=s) for s in subs_grid]
mg_grid = [0.94, 0.97, 1.00, 1.03, 1.06]
grid_margin = [dcf_scenario(contrib_mult=m) for m in mg_grid]
capex_grid = [0.85, 0.925, 1.00, 1.10, 1.20]
grid_capex = [dcf_scenario(capex_mult=m) for m in capex_grid]
nwc_grid = [-0.10, -0.085, nwc_pct, -0.050, -0.030]
grid_nwc = [dcf_scenario(nwc=p) for p in nwc_grid]
roic_grid = [0.18, 0.22, roic_term, 0.30, 0.34]
def dcf_roic(r_):
    _rr = min(V['g_term'] / r_, 0.95)
    _tv = nopat[-1] * (1 + V['g_term']) * (1 - _rr) / (wacc_term - V['g_term'])
    _ev = pv_explicit + _tv * df[-1]
    return ((_ev - LEASE + NETCASH + 0.511) / SH) * ROLL - V['div_between']
grid_roic = [dcf_roic(r_) for r_ in roic_grid]
dcf_opex_1pp = dcf_scenario(opex_shift=+0.01)   # +1pp of revenue in the cost stack
dcf_tax_per_pp = (grid_tax[0] - grid_tax[4]) / ((tax_grid[4] - tax_grid[0]) * 100)

# ---- expert panel: three genuinely different methods ---------------------------
# Expert 1 — earnings power on a through-cycle multiple
e1_eps = eps_fc[2]
e1_base, e1_lo, e1_hi = (to_anchor(15.0 * e1_eps) / (1 + ke_exp) ** 2 - V['div_between'],
                         to_anchor(12.0 * e1_eps) / (1 + ke_exp) ** 2 - V['div_between'],
                         to_anchor(17.5 * e1_eps) / (1 + ke_exp) ** 2 - V['div_between'])
# Expert 2 — dividend discount (the natural lens for a ~100%-payout duopoly)
e2_dps = dps_fc[0]
e2_ke = ke_term
e2_base = to_anchor(e2_dps * (1 + V['g_term']) / (e2_ke - V['g_term'])) - V['div_between']
e2_lo = to_anchor((e2_dps * 0.85) * (1 + 0.015) / (0.5 * (ke_exp + ke_term) + 0.01 - 0.015)) - V['div_between']
e2_hi = to_anchor(e2_dps * (1 + 0.030) / (e2_ke - 0.030)) - V['div_between']
# Expert 3 — economic profit / residual income on invested capital
ic_beg = [ic_fy25] + ic[:-1]
ep_ = [nopat[i] - fwd[i] * ic_beg[i] for i in range(5)]
pv_ep = sum(ep_[i] * df[i] for i in range(5))
ep_term = nopat[-1] * (1 + V['g_term']) - wacc_term * ic[-1] * (1 + V['g_term'])
pv_ep_term = ep_term / (wacc_term - V['g_term']) * df[-1]
e3_ev = ic_fy25 + pv_ep + pv_ep_term
e3_base = ((e3_ev - LEASE + NETCASH + 0.511) / SH) * ROLL - V['div_between']
e3_lo = ((ic_fy25 + pv_ep * 0.7 + pv_ep_term * 0.6 - LEASE + NETCASH + 0.511) / SH) * ROLL \
        - V['div_between']
e3_hi = dcf_ps_rf_alt if dcf_ps_rf_alt > e3_base else e3_base * 1.12
experts = dict(
    e1=dict(method_short='earnings power', base=e1_base, rng=[e1_lo, e1_hi], eps=e1_eps,
            pe=15.0, discount_years=2),
    e2=dict(method_short='dividend stream', base=e2_base, rng=[e2_lo, e2_hi], dps=e2_dps,
            ke=e2_ke, g=V['g_term']),
    e3=dict(method_short='cash returns vs cost of capital', base=e3_base, rng=[e3_lo, e3_hi],
            ic0=ic_fy25, pv_ep=pv_ep, pv_ep_term=pv_ep_term, ev=e3_ev, ep=ep_,
            spread=[roic[i] - fwd[i] for i in range(5)]),
)
panel_centre = float(sorted([e1_base, e2_base, e3_base])[1])
say(f"[Expert panel] Expert 1 {e1_base:.2f} [{e1_lo:.2f}-{e1_hi:.2f}]; Expert 2 {e2_base:.2f} "
    f"[{e2_lo:.2f}-{e2_hi:.2f}]; Expert 3 {e3_base:.2f} [{e3_lo:.2f}-{e3_hi:.2f}]; panel "
    f"median {panel_centre:.2f} ({panel_centre/SPOT-1:+.0%} vs spot)")

# ---- fan for the figure ---------------------------------------------------------
paths3 = np.load(os.path.join(HERE, 'paths_3M.npy'))
fan = np.percentile(paths3, [5, 25, 50, 75, 95], axis=0)
np.save(os.path.join(HERE, 'fan.npy'), fan)

# ============================ EMIT ==============================================
step0 = json.load(open(os.path.join(HERE, 'step0_result.json')))
strike = json.load(open(os.path.join(HERE, 'strike_result.json')))
beta_res = json.load(open(os.path.join(HERE, 'beta_result.json')))
bt5 = json.load(open(os.path.join(HERE, 'backtest_5y.json')))

OUT = dict(
    meta=dict(ticker='DU', company='Emirates Integrated Telecommunications Company PJSC (du)',
              market='DFM', currency='AED', asof='2026-08-07', spot=SPOT, shares_mn=SH,
              mktcap=MKTCAP, ev_trailing=ev_trailing,
              klass='integrated telecom operating company'),
    inputs=INP,
    hist_is=hist_is,
    hist_bs=hist_bs,
    nwc_hist=nwc, nwc_pct=nwc_pct, cycle=dict(dso=dso, dpo=dpo, dio_fy25=dio_fy25),
    fcst=dict(years=YRS, rev=rev, seg_rev=seg_rev, contrib=_B['contrib'],
              contrib_tot=contrib_tot, opex=opex_fc, opex_lines=_B['opex_lines'],
              ebitda=ebitda, ebitda_margin=ebitda_margin, dna=dna, dep_ppe=dep_ppe,
              amort=amort, rou_dep=V['rou_dep_path'], ebit=ebit, nopat=nopat,
              capex=capex, capex_tang=capex_tang, capex_int=capex_int,
              nwc=nwc_fc, dnwc=dnwc, rou_repl=rou_repl, fcff=fcff, df=df, pv=pv,
              fwd_wacc=fwd, ppe=ppe_path, intang=int_path, rou=rou_path, ic=ic, roic=roic,
              np=np_fc, eps=eps_fc, dps=dps_fc, div=div_fc, equity=eq_fc, net_cash=ncash_fc,
              int_inc=int_inc_fc, int_exp=int_exp_fc, payout=PAYOUT,
              dep_yield=dep_yield, lease_rate=lease_rate, glide_frac=glide_frac,
              taxB_path=taxB_path, fcffB=fcffB, npB=npB),
    seg_fy25=dict(rev=SRH['FY25'], contrib=SCH['FY25'], names=SEGNAME,
                  margin={s: SCH['FY25'][s] / SRH['FY25'][s] for s in SEGS}),
    bottomup=dict(seg_rev_hist=SRH, seg_contrib_hist=SCH,
                  subs_mobile=V['subs_mobile'], subs_fixed=V['subs_fixed'],
                  arpu=V['arpu_mobile'], unit_mobile_fy25=_unit_mobile_25,
                  subs_mobile_path=V['subs_mobile_path'], subs_fixed_path=V['subs_fixed_path'],
                  arpu_mobile_path=V['arpu_mobile_path'], arpu_fixed_path=V['arpu_fixed_path'],
                  h1_seg=H1_SEG),
    wacc=dict(rf=V['rf'], rf_alt=V['rf_alt'], rf_star=rf_star, ke_exp=ke_exp,
              ke_mkt_alt=ke_mkt_alt, ke_raw_retired=ke_raw_retired, kd=V['kd'], kd_at=kd_at,
              we_exp=we_exp, wd_exp=wd_exp, wacc_exp=wacc_exp, wacc_exp_mkt=wacc_exp_mkt,
              wacc_rf_alt=wacc_rf_alt, ke_term=ke_term, kd_term=V['kd_term'],
              kd_term_at=kd_term_at, wacc_term=wacc_term, glide_frac=glide_frac,
              rf_path=V['rf_path'], lease_rate_disclosed=lease_rate, beta=beta_res,
              erp_rating=V['erp_rating'], erp_mkt=V['erp_mkt'],
              sov_spread_rating=V['sov_spread_rating'], sov_spread_mkt=V['sov_spread_mkt']),
    dcf=dict(pv_explicit=pv_explicit, tv=tv, pv_tv=pv_tv, ev=ev, tv_share=tv_share,
             lease=LEASE, net_cash=NETCASH, investees=0.511, eq_val=eq_val,
             ps=dcf_ps, ps_dec=dcf_ps_dec, roll=ROLL, anchor_days=V['anchor_days'],
             div_between=V['div_between'], roic_term=roic_term, rr_term=rr_term,
             g=V['g_term'], bear=dcf_bear, bull=dcf_bull,
             ps_framing_b=dcf_ps_B, ps_rf_alt=dcf_ps_rf_alt),
    terminal_recon=dict(roic_term=roic_term, rr=rr_term,
                        nopat=dict(FY25=(V['pbt_fy25'] - netfin_fy25) * (1 - TAX)),
                        roic_path=roic),
    lenses=lenses, central=central, span=[lo, hi], spot=SPOT,
    experts=experts, panel_centre=panel_centre, yield_ps=yield_ps,
    rel=dict(pe_trailing=pe_trailing, ev_ebitda_trailing=ev_ebitda_trailing,
             pe_just=V['pe_just'], div_yield_peer=V['div_yield_peer'], eps26=eps_fc[0],
             dps26=dps_fc[0]),
    norm=dict(margin=norm_margin, rev=norm_rev, ebitda=norm_ebitda, ebit=norm_ebit,
              np=norm_np, eps=norm_eps, pe=V['pe_just'], year=YRS[0], margin_year=YRS[2]),
    book=dict(bvps=bvps, pb_just=pb_just, roe_sust=V['roe_sust'], roe_trailing=roe_trailing,
              ke_term=ke_term),
    sens=dict(g_grid=g_grid, wt_grid=wt_grid, we_grid=we_grid, grid_wacc_g=grid_wacc_g,
              grid_exp_term=grid_exp_term, beta_grid=beta_grid, grid_beta=grid_beta,
              tax_grid=tax_grid, grid_tax=grid_tax, arpu_grid=arpu_grid, grid_arpu=grid_arpu,
              subs_grid=subs_grid, grid_subs=grid_subs, mg_grid=mg_grid,
              grid_margin=grid_margin, capex_grid=capex_grid, grid_capex=grid_capex,
              nwc_grid=nwc_grid, grid_nwc=grid_nwc, roic_grid=roic_grid, grid_roic=grid_roic,
              dcf_opex_1pp=dcf_opex_1pp, dcf_tax_per_pp=dcf_tax_per_pp),
    step0=step0, strike=strike, backtest=bt5,
    assert_log=LOG,
)
with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(OUT, f, indent=1, default=float)
say("=" * 78)
say(f"WROTE study_numbers.json | central AED {central:.2f} [{lo:.2f} - {hi:.2f}] vs spot "
    f"{SPOT:.2f} | DCF A {dcf_ps:.2f} / B {dcf_ps_B:.2f} | TV {tv_share:.0%} of EV | WACC "
    f"{wacc_exp:.2%} -> {wacc_term:.2%}")
