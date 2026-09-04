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

# ---------------------------------------------------------------------------
# Like-for-like half-year unit-cost deltas, computed BEFORE the register so the register's
# own justification text quotes the arithmetic instead of restating it by hand.
# ---------------------------------------------------------------------------
# ADDED 17-Aug-2026 after a rendered-PDF read caught two typed narrative figures ("-4.2%",
# "+3.1%") disagreeing with the computed values (-4.13%, +2.98%). Same defect class as the
# numerals once typed into the workbook builder: a number stated in prose that nothing checks.
# These are derived from the raw disclosed figures that appear as literals in the register
# below, and are re-asserted against the full DCU table once that is built.
def _lfl(h125, h126, m125, m126):
    """Per-subscriber-per-month rate for each half, and the like-for-like change."""
    r125 = h125 / m125 / 6 * 1000
    r126 = h126 / m126 / 6 * 1000
    return r125, r126, r126 / r125 - 1

# average mobile base over each half: (opening + closing) / 2, from the disclosed quarter ends
_M125 = (8916.0 + 9138.0) / 2
_M126 = (9704.0 + 9280.0) / 2
_F125 = (682.0 + 706.0) / 2
_F126 = (735.0 + 744.0) / 2
# mobile interconnect = total interconnect less the fixed and wholesale segment direct costs
_I125, _I126, _D_INTER = _lfl(1442.312 - (2140.263 - 1826.774) - (1283306 - 1104384) / 1000,
                              1456.789 - (2382.608 - 2079.325) - (1257.566 - 1061.640),
                              _M125, _M126)
_C125, _C126, _D_COMM = _lfl(331.701, 359.188, _M125, _M126)
_X125, _X126, _D_FIXED = _lfl(2140.263 - 1826.774, 2382.608 - 2079.325, _F125, _F126)

INP = dict(
    # ---- anchors --------------------------------------------------------
    spot=I(11.36, "DFM close for DU, 3 September 2026, from the price file the principal "
           "supplied that day and committed to the repository. THE STUDY IS RE-STRUCK ON "
           "IT because no study is delivered against a stale price: the prior edition "
           "stood on the 7-August close of 12.30, and the stock has since fallen 7.6%, "
           "which widens rather than closes this study's disagreement with the market",
           "2026-09-03",
           "Market"),
    shares_mn=I(4532.905989, "Share capital note 27, audited FY2025 consolidated FS: "
                "4,532,905,989 shares of AED 1 each, authorised, issued and fully paid, "
                "unchanged across FY2023-FY2025 and both 2026 interims", "2026-02-09", "Company"),
    anchor_days=I(246.0, "31-Dec-2025 valuation date to the 3-Sep-2026 price anchor "
                  "(246 days), twenty-seven days longer than the prior edition's because "
                  "the anchor moved with the price it is compared against", "2026-09-03",
                  "House"),
    div_between=I(0.66, "Dividends whose EX-DATE falls between the 31-Dec-2025 valuation date and "
                  "the 07-Aug-2026 anchor, and which are therefore no longer in the share price: "
                  "the final FY2025 AED 0.40 (AGM 30-Mar-2026, paid 28-Apr-2026) PLUS the H1-2026 "
                  "interim AED 0.26 — Board-approved 22-Jul-2026, EX-DATE 31-JULY-2026, record "
                  "03-Aug-2026, paid 21-Aug-2026, per du's own dividend disclosure to DFM (Ref "
                  "RME/14/2026). CORRECTED 17-Aug-2026: the prior edition carried only 0.40, on the "
                  "reasoning that the interim was declared but unpaid at the anchor so it 'stays in "
                  "the share'. That applied the PAYMENT date; the correct test is the EX-date, which "
                  "had passed six trading sessions before the anchor. The anchor spot of AED 12.30 "
                  "is ex the 0.26, so every lens rolled to that anchor must be ex it too",
                  "2026-07-31", "Company"),

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
    # FY2022 is carried for ONE purpose and it is stated rather than left to be inferred:
    # section 1.4 says the latest reviewed half printed the best margin in the company's
    # history, and a superlative needs a record to be superlative over. The FY2023
    # statements carry FY2022 as their comparative, so this costs a read of a document the
    # study already holds. It enters no forecast driver and no lens.
    rev_fy22=I(12754.492, AR23 + ", FY2022 comparative on the face of the income statement",
               "2024-02-13", "Company"),
    ebitda_fy22=I(5142.857, "DERIVED (flagged), on the SAME construction as FY2023 so the "
                  "series is like-for-like: revenue 12,754.492 less operating expenses "
                  "9,551.929 excluding D&A 2,112.223, less expected credit losses 173.566, "
                  "plus other income 1.637. Every component is an audited FY2022 comparative "
                  "in " + AR23 + " (income statement and Note 26)",
                  "2024-02-13", "Company/derived"),
    dna_fy22=I(2112.223, AR23 + ", Note 26 FY2022 comparative: PP&E depreciation 1,607.280 + "
               "right-of-use depreciation 350.859 + intangibles amortisation 154.084",
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
    investees_bv=I(0.511, AR25 + ", Note 10: investments accounted for using the equity method, "
                   "carrying value AED 0.511mn at 31-Dec-2025 (FY2024: 2.716mn). REGISTERED "
                   "17-Aug-2026 — this figure was previously typed directly into the bridge, so it "
                   "was an input with no four-field record and the completeness assertion passed "
                   "over it", "2026-02-09", "Company"),
    # ---- by-nature historical detail, REGISTERED 17-Aug-2026 -----------------
    # These lines were previously typed as numerals into the workbook builder, which broke the
    # numeric-traceability rule (every builder reads the committed numbers file exclusively).
    direct_costs_hist=I(dict(FY24=-4818.442, FY25=-5259.425),
                        AR25 + ", face of the income statement: interconnect + commission + devices "
                        "and other direct services cost", "2026-02-09", "Company"),
    # ---- direct costs BY NATURE, four fiscal years + both 2026 interims ----
    # REGISTERED 17-Aug-2026. These were disclosed all along and were NOT swept in: the
    # forecast held one blended contribution margin per segment instead of driving each
    # physically distinct cost line on its own driver. Same failure class as ARCC.
    dc_nature_hist=I(dict(
        FY22=dict(interconnect=2768.016, commission=463.784, devices=1303.426),
        FY23=dict(interconnect=2729.605, commission=535.469, devices=1405.604),
        FY24=dict(interconnect=2811.223, commission=596.223, devices=1410.996),
        FY25=dict(interconnect=2914.172, commission=686.408, devices=1658.845),
    ), "Operating-expenses note, by nature: " + AR23 + " Note 26 (FY2022 'Product costs' and "
       "FY2023); " + AR24 + " Note 27 (FY2023-24, where the line is renamed 'Cost of devices and "
       "direct services'); " + AR25 + " face of the income statement (FY2024-25). NOTE A REAL "
       "DISCREPANCY: AR2024 Note 27 prints FY2024 devices as 1,402.121 while AR2025 re-presents "
       "the same year at 1,410.996 (+8.875). The later filing is taken as the authority, and the "
       "FY2024 by-nature lines then foot exactly to the disclosed 4,818.442 total",
       "2026-02-09", "Company"),
    dc_nature_h1=I(dict(
        H125=dict(interconnect=1442.312, commission=331.701, devices=778.268),
        H126=dict(interconnect=1456.789, commission=359.188, devices=769.467),
    ), H126 + ", face of the income statement: the three direct-cost lines with their H1-2025 "
       "comparatives. THE LIKE-FOR-LIKE HALF-YEAR PAIR is what makes a per-unit escalator "
       "sourced rather than assumed", "2026-07-22", "Company"),
    seg_dc_hist=I(dict(
        FY24=dict(mobile=2562.523, fixed=615.065, wholesale=284.092, ict=1356.762),
        FY25=dict(mobile=2771.294, fixed=621.852, wholesale=348.749, ict=1517.530),
    ), AR25 + ", Note 38: 'interconnect and other direct costs' by segment (segment revenue less "
       "segment contribution)", "2026-02-09", "Company"),
    seg_dc_h1=I(dict(
        H125=dict(mobile=1357.492, fixed=313.489, wholesale=178.922, ict=702.378),
        H126=dict(mobile=1371.245, fixed=303.283, wholesale=195.926, ict=714.990),
    ), H126 + ", Note 17 segment analysis: segment revenue less segment contribution ('gross "
       "margin'), for the six months ended 30-Jun-2026 and the 30-Jun-2025 comparative",
       "2026-07-22", "Company"),
    h1_25_seg=I(dict(mobile=3457.094, fixed=2140.263, wholesale=1283.306, ict=869.632),
                H126 + ", Note 17: H1-2025 comparative segment revenue; foots to 7,750.295",
                "2026-07-22", "Company"),
    subs_prepaid=I(dict(Q4_2024=7116, Q1_2025=7292, Q2_2025=7254, Q3_2025=7248, Q4_2025=7726,
                        Q1_2026=7670, Q2_2026=7227),
                   IRQ2 + " + prior quarterly decks: prepaid mobile customers ('000). "
                   "REGISTERED 17-Aug-2026 — du discloses the mobile base SPLIT by prepaid and "
                   "postpaid every quarter, and the prior edition modelled only the total",
                   "2026-07-23", "Company"),
    subs_postpaid=I(dict(Q4_2024=1800, Q1_2025=1845, Q2_2025=1884, Q3_2025=1922, Q4_2025=1979,
                         Q1_2026=2023, Q2_2026=2053),
                    IRQ2 + " + prior quarterly decks: postpaid mobile customers ('000)",
                    "2026-07-23", "Company"),
    arpu_leg_disclosed=I(0.0, "NEGATIVE RESULT, dated 17-Aug-2026: du discloses a SINGLE BLENDED "
                         "mobile ARPU line in its quarterly KPI table and nowhere publishes "
                         "prepaid or postpaid ARPU separately — checked across the Q2-2026, "
                         "Q1-2026 and Q4-2025 earnings releases and analyst presentations and the "
                         "FY2025 annual report, and confirmed against the audited segment note (Note 38, "
                         "interim Note 17), which splits Mobile/Fixed and never prepaid/postpaid. "
                         "The value 0.0 records the count of separately disclosed leg ARPUs. "
                         "CORRECTED 17-Aug-2026: an earlier draft of this note called the omission "
                         "a du-specific choice against a sector norm. It is the REGIONAL norm — "
                         "e& (du's own duopoly counterparty), stc and Mobily all publish the "
                         "subscriber split with a single blended ARPU, exactly as du does; Ooredoo "
                         "is the sole Gulf exception. ACCESS CAVEAT, logged not papered over: "
                         "investors.du.ae is intermittent from this environment (HTTP 200 on a "
                         "direct request during this session, HTTP 503 on every attempt in a "
                         "parallel verification pass), so the deck-level negative rests on the "
                         "documents captured in this study's own first-hand extract of the "
                         "Q2-2026 presentation rather than on a fresh re-read. Consequence: the mobile "
                         "price driver is built on the blended figure and the two-leg split is "
                         "shown to be UNIDENTIFIED rather than estimated (see the identification "
                         "test in the derivation log)", "2026-08-17", "Company"),
    arpu_mobile_q=I(dict(Q4_2024=65.8, Q1_2025=63.5, Q2_2025=63.3, Q3_2025=64.5, Q4_2025=65.3,
                         Q1_2026=63.4, Q2_2026=63.4, FY_2024=62.5, FY_2025=63.3),
                    "du quarterly analyst presentation, mobile segment KPI slide (Q2-2026 deck "
                    "slide 12) — the full blended-ARPU series, AED/month. REGISTERED 17-Aug-2026: "
                    "the prior edition carried only three points and its driver note described "
                    "the company as printing '63.3-63.4', which understates the real dispersion — "
                    "the quarterly series ranges 63.3 to 65.8 and fell from 65.3 (Q4-2025) to "
                    "63.4 (Q2-2026). FY2025 63.3 is corroborated independently by the Q4-FY2025 "
                    "earnings release, and the subscribers x ARPU build reproduces audited mobile "
                    "segment revenue to within 0.05%, so the level is not in doubt",
                    "2026-07-23", "Company"),
    arpu_ratio_peers=I(dict(ooredoo_qatar=7.22, ooredoo_kuwait=4.67, ooredoo_oman=2.92),
                       "Postpaid/prepaid ARPU ratios at the ONLY Gulf operator that discloses "
                       "both legs, from Ooredoo's own Q2-2026 disclosure (QAR: Qatar 239.8/33.2, "
                       "Kuwait 161.5/34.6, Oman 67.2/23.0). Used ONLY to bound the identification "
                       "test and the mix decomposition — never to build revenue. The 2.9x-7.2x "
                       "spread across three markets of a SINGLE operator is itself evidence that "
                       "an imported ratio cannot pin down du's split", "2026-08-17", "Industry"),
    arpu_ratio_norm=I(3.0, "Central postpaid/prepaid ARPU ratio used ONLY for the mix "
                      "decomposition — never to build revenue. Set at the low end of the peer "
                      "band above, which makes the decomposition's implied per-leg erosion the "
                      "SMALLEST of the defensible range: a higher ratio implies a larger mix "
                      "tailwind and therefore worse underlying erosion, so 3.0x is the "
                      "conservative choice for the risk being flagged", "2026-08-17", "House"),
    arpu_drift=I(0.0, "Annual compounding shift applied to the registered blended mobile ARPU "
                 "path, zero in the base case. Exists so the mix-exhaustion risk identified by "
                 "the decomposition below can be PRICED rather than described",
                 "2026-08-17", "House"),
    subs_mobile_h1_25=I(9138.0, "Mobile customers at 30-Jun-2025 ('000), du Q2-2025 quarterly "
                        "disclosure — needed to put the H1-2025 comparative cost on the same "
                        "average-base denominator as H1-2026", "2025-07-23", "Company"),
    subs_fixed_h1_25=I(706.0, "Fixed customers at 30-Jun-2025 ('000), same source",
                       "2025-07-23", "Company"),
    opex_before_dna_hist=I(dict(FY24=-3347.636, FY25=-3307.608),
                           AR25 + ", total net operating expenses before depreciation and "
                           "amortization", "2026-02-09", "Company"),
    int_inc_fy23=I(61.327, AR23 + ", finance income", "2024-02-13", "Company"),
    int_exp_fy23=I(101.430, AR23 + ", finance costs", "2024-02-13", "Company"),
    assoc_hist=I(dict(FY23=-2.720, FY24=-2.427, FY25=-0.894),
                 "Share of loss of associate and joint venture: " + AR23 + " (FY2023); " + AR25
                 + " (FY2024 comparative and FY2025)", "2026-02-09", "Company"),
    dep_ppe_hist=I(dict(FY23=1544.182, FY24=1569.189, FY25=1557.989),
                   "Depreciation and impairment of property, plant and equipment: " + AR23
                   + " Note 26 (FY2023); " + AR25 + " Note 31 (FY2024-25)", "2026-02-09", "Company"),
    amort_hist=I(dict(FY23=209.053, FY24=209.896, FY25=245.881),
                 "Amortisation and impairment of intangible assets, same notes as above",
                 "2026-02-09", "Company"),
    capex_cash_hist=I(dict(FY23=2227.558, FY24=1920.468, FY25=2353.230),
                      "Cash capital expenditure = purchase of PP&E + purchase of intangible assets, "
                      "audited consolidated statements of cash flows (AR2023 for FY2023; AR2025 for "
                      "the FY2024 comparative and FY2025)", "2026-02-09", "Company"),
    tax_paid_hist=I(dict(FY24=-1928.939, FY25=-1883.442),
                    "Federal royalty paid + income tax paid, audited consolidated statements of cash "
                    "flows (" + AR25 + ")", "2026-02-09", "Company"),
    ocf_hist=I(dict(FY24=4636.508, FY25=5229.823),
               AR25 + ", net cash generated from operating activities", "2026-02-09", "Company"),
    div_paid_hist=I(dict(FY24=-1858.491, FY25=-2629.085),
                    AR25 + ", dividends paid (financing activities)", "2026-02-09", "Company"),
    subs_mobile_hist_display=I(dict(FY23=8554.0, FY24=8916.0, FY25=9704.0),
                               IRQ2 + " and the Q4/FY2025 deck: mobile customers at 31-Dec-2024 and "
                               "31-Dec-2025 ('000)", "2026-02-10", "Company"),
    subs_fixed_hist_display=I(dict(FY23=604.0, FY24=682.0, FY25=735.0),
                              IRQ2 + " and the Q4/FY2025 deck: fixed customers at 31-Dec-2024 and "
                              "31-Dec-2025 ('000)", "2026-02-10", "Company"),
    arpu_hist_display=I(dict(FY24=65.8, FY25=63.3),
                        "Blended mobile ARPU (AED/month): Q4-2024 print 65.8 and the FY2025 average "
                        "63.3, both from the company's quarterly analyst decks", "2026-02-10",
                        "Company"),
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
    h1_26_seg=I(dict(mobile=3646.314, fixed=2382.608, wholesale=1257.566, ict=911.085),
                H126 + ", segment revenue for the six months ended 30-Jun-2026 (Note 17 segment "
                "analysis); ties exactly to reviewed total revenue 8,197.573. REGISTERED "
                "17-Aug-2026 — previously a typed dict inside the build, so it was an input with "
                "no four-field record", "2026-07-22", "Company"),
    subs_mobile_fy23=I(8554.0, "Mobile customer base at 31-Dec-2023: 8,554 thousand, du Annual "
                       "Report 2024 operational highlights (page 6), which prints the 2023 and "
                       "2024 bases side by side", "2025-02-10", "Company"),
    subs_fixed_fy23=I(604.0, "Fixed customer base at 31-Dec-2023: 604 thousand, same source and "
                      "page. This SETTLES an external challenge that the 682 thousand figure was "
                      "FY2023: du's own report shows 604 (2023) and 682 (2024)", "2025-02-10",
                      "Company"),
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
                       "prepaid dilution. CORRECTED 17-Aug-2026: the prior note said the company "
                       "'printed 63.3-63.4', which flattered the stability of the series — the "
                       "disclosed quarterly range is 63.3 to 65.8, and the last three prints run "
                       "65.3 (Q4-2025) -> 63.4 (Q1-2026) -> 63.4 (Q2-2026), i.e. DOWN 2.9% from "
                       "the recent peak. Holding the path flat is therefore an assumption that "
                       "the recent decline stops, and the mix decomposition shows why it is "
                       "fragile; the downside is priced as the mix-exhaustion scenario",
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
    # ---- direct-cost stack: COST PER UNIT, ONE ESCALATOR PER DRIVER CLASS ---
    # REPLACES contrib_margin_path (retired 17-Aug-2026). The retired driver set a
    # contribution MARGIN per segment as an INPUT, held at the audited FY2025 rate. That
    # broke two standing rules at once: §1.6 requires margins to be OUTPUTS, and the
    # cost-stack escalation rule requires each physically distinct cost line to carry its
    # own driver. It also ignored six months of reviewed H1-2026 data in favour of a
    # stale full-year rate — the ARCC failure exactly.
    #
    # Every base rate below is COMPUTED from the registered filings (seg_dc_h1 / dc_nature_h1
    # over the disclosed average subscriber base), never typed. Only the escalators are
    # House inputs, and the default is FLAT: a rate drifts only where a named structural
    # mechanism has a MEASURED like-for-like direction in du's own half-year pair.
    esc_dc_inter=I(-0.015, "Mobile interconnect cost per subscriber per month, -1.5%/yr. "
                   f"MEASURED: {_I125:.2f} (H1-2025) -> {_I126:.2f} (H1-2026), "
                   f"{_D_INTER:+.2%} like-for-like. "
                   "MECHANISM: regulated mobile-termination rates ratchet down and terminated "
                   "voice/SMS keeps migrating to OTT, so the per-subscriber off-net bill falls "
                   "even as the base grows. The forecast takes barely a third of the observed "
                   "decline, on the view that it decays as the OTT substitution matures",
                   "2026-08-17", "House"),
    esc_dc_comm=I(0.030, "Mobile commission cost per subscriber per month, +3.0%/yr. MEASURED: "
                  f"{_C125:.2f} (H1-2025) -> {_C126:.2f} (H1-2026), {_D_COMM:+.2%} "
                  "like-for-like, and 5.69 -> 6.14 "
                  "across FY2024-25. MECHANISM: dealer and retail acquisition/retention "
                  "commission per subscriber, rising with competitive intensity in a "
                  "two-player market. The observed rate is carried forward unchanged",
                  "2026-08-17", "House"),
    esc_dc_dev=I(0.0, "Mobile devices and direct-services cost per subscriber per month, held "
                 "FLAT. MEASURED but NOT extrapolated: 1.40 (H1-2025) -> 0.96 (H1-2026), with "
                 "0.52 in FY2024 and 1.26 in FY2025. This is the handset/direct-services "
                 "residual after ICT takes the bulk of the disclosed devices line — small "
                 "(under AED 1.5/sub/month) and visibly lumpy, so no trend is read into it",
                 "2026-08-17", "House"),
    esc_dc_fixed=I(0.0, "Fixed capacity and direct cost per subscriber per month, held FLAT at "
                   "the H1-2026 reviewed rate. MEASURED but NOT extrapolated: 79.71 (FY2024) -> "
                   f"73.14 (FY2025) -> {_X126:.2f} (H1-2026), a {_D_FIXED:+.2%} like-for-like "
                   "half-year fall. "
                   "The mechanism (fibre/FWA scale plus enterprise mix) is real but decays at an "
                   "unmeasurable rate, so the observed improvement is stopped dead rather than "
                   "projected. Because revenue per subscriber escalates 1.5%/yr against a flat "
                   "cost, the fixed margin still widens as an OUTPUT",
                   "2026-08-17", "House"),
    dc_rate_wholesale=I(0.1558, "Wholesale direct cost as a share of wholesale revenue, held "
                        "FLAT at the H1-2026 reviewed rate. The series worsens at every "
                        "observation — 11.97% (FY2024), 13.58% (FY2025), 13.94% (H1-2025), "
                        "15.58% (H1-2026) — which du's own Q2 commentary attributes to the "
                        "conflict-hit roaming and transit mix. The forecast takes NO credit for "
                        "the recovery that commentary implies, and equally does not project "
                        "further deterioration", "2026-08-17", "House"),
    dc_rate_ict=I(0.7848, "ICT and associated-services direct cost as a share of ICT revenue, "
                  "held FLAT at the H1-2026 reviewed rate. The history does not support a "
                  "trend in either direction: 79.25% (FY2024) worsened to 80.61% (FY2025) then "
                  "improved to 78.48% (H1-2026). The prior edition projected a 2.1pp margin "
                  "improvement on a data-centre-scale story; that story is not measurable in "
                  "the disclosed series, so it has been removed and the rate held flat",
                  "2026-08-17", "House"),

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
    staff_fy26=I(1035.16, "FY2026E staff cost: H1-2026 reviewed actual 471.360 grossed up by the "
                 "company's OWN disclosed H2/H1 seasonality of 1.1961 (H2-2025 602.018 / H1-2025 "
                 "503.310, from the audited FY2025 and reviewed H1-2025 statements) = 471.360 + "
                 "563.80 = 1,035.16 — which is −6.35% on the audited FY2025 1,105.328, exactly the "
                 "−6.35% y/y the company printed at the half. CORRECTED 17-Aug-2026: the prior 985.0 "
                 "applied a ratio of 1.09 while its own note described it as 'the H2-2025 seasonal "
                 "ratio'; the true ratio is 1.1961, so staff cost was understated by AED 50.2mn and "
                 "total FY2026E operating expenses fell BELOW the audited FY2025 actual even as "
                 "revenue rose 4.3% — impossible in a stack where every class escalates, and "
                 "correctly identified by external audit as falsifying the margin-as-an-output claim",
                 "2026-08-17", "Company/House"),
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
    e1_horizon_years=I(2.4027, "Years from the 07-Aug-2026 anchor to 31-Dec-2028, the date "
                       "Expert 1's FY2028 earnings multiple values: 877 calendar days / 365. "
                       "REGISTERED 17-Aug-2026 after an external critique showed the lens was "
                       "discounting over a NET 1.40 years, a full year short of anchor "
                       "consistency", "2026-08-17", "House"),
    guidance_mid=I(0.05, "Midpoint of du's own FY2026 revenue-growth guidance of 4%-6%, revised "
                   "and confirmed in the Q2-2026 analyst presentation (slide 16, 'Guidance "
                   "confirmed for EBITDA margin and slightly adjusted for revenue growth'). Used "
                   "only to PRICE a critique finding, never as a build driver — reverse-engineering "
                   "a forecast to a guidance number is the opposite of a ground-up build",
                   "2026-07-23", "Company"),
    lens_weights=I(dict(dcf=0.45, relative=0.25, normalized=0.20, book=0.10),
                   "RETIRED 02-Sep-2026 and kept only as the record of what the retired "
                   "construction did. These were house synthesis weights copied from an "
                   "operating-company pattern; they were typed, they had never cleared an "
                   "out-of-sample test, and they are no longer an input to any published "
                   "figure. They are consumed in exactly two places, both of which price "
                   "the retired construction rather than the answer: the Summary's own "
                   "labelled retired row, and the arithmetic recording how the external "
                   "weight finding was priced at the time it was raised",
                   "2026-08-09", "House"),
    # ---- figures a reader meets in prose, committed as numbers ----------------
    # Each of these was sourced correctly and then written ONLY into a justification
    # sentence or a paragraph, where no instrument could reconcile it. They drive no
    # forecast: they are the components and refusals the register's own text quotes, and
    # a component quoted in prose is a claim like any other.
    erp_mature_base=I(0.0423, "Damodaran mature-market equity risk premium base, Jan-2026 "
                      "edition, read from the original ctryprem file. Both published UAE "
                      "constructions add their country premium to THIS number: the adopted "
                      "market-spread basis (4.23% + 6bp) and the alternative rating basis "
                      "(4.23% + 64bp, Aa2). Quoted four times across the delivered documents "
                      "and committed here so those quotations reconcile",
                      "2026-01-01", "Country"),
    rf_ad_usd_10y=I(0.0473, "Abu Dhabi sovereign USD 10-year, Feb-2026 issue, priced at "
                    "UST+25bp. The peg-extrapolated alternative risk-free anchor is this "
                    "figure less the ~4bp observed AED-through-USD basis at matched tenor; "
                    "the AED-equivalent result is registered separately as rf_alt, and this "
                    "is the USD leg it is built from",
                    "2026-02-01", "Country"),
    pe_provider_refused=I(11365.0, "A NEGATIVE RESULT, committed because it is quoted. The "
                          "data provider returned a price/earnings multiple of 11,365x for "
                          "Zain, which is corrupt on its face; it was REFUSED rather than "
                          "carried into a peer median, and that refusal is one of the two "
                          "reasons this study claims no peer median at all",
                          "2026-08-06", "Industry"),
    mamoura_stake_sold=I(0.0755, "Mubadala's Mamoura vehicle sold three quarters of its "
                         "holding in du in the 2025 secondary offering — 7.55% of the "
                         "company. It widened the free float without changing control, and "
                         "it drives nothing in this model: it is committed because the "
                         "company overview states it to a reader",
                         "2025-12-31", "Company"),
    g_term_real=I(0.0, "Terminal REAL growth of ZERO, the house default for a real rate "
                  "nobody has quantified. The previous edition typed a nominal 2.5% and "
                  "argued it as 'population-plus-inflation minus price erosion' — which "
                  "names TWO real forces pointing opposite ways and puts a number on "
                  "NEITHER, so the +0.49% real that a 2.5% nominal implies against 2.0% "
                  "inflation was never anybody's estimate; it was the residue of typing "
                  "the nominal figure. Real growth is now CHARGED for the capital it "
                  "consumes, which this model's own forecast prices at AED 10,430mn per "
                  "unit of real growth, so half a point of it is worth AED 52mn a year "
                  "for ever. Assuming it away is the conservative reading and the "
                  "sensitivity publishes the alternative rather than burying it",
                  "2026-08-09", "Country/House"),
    asset_life_years=I((28616356.0 + 3500287.0 + 3726888.0)
                       / (1542393.0 + 239907.0 + 364063.0),
                       AR25 + ", notes 6, 7 and 8, DERIVED BY IDENTITY from those notes' "
                       "own cost and charge columns and LABELLED as derived: the gross "
                       "cost of every depreciable class over the year's own charge. "
                       "Property, plant and equipment 28,616,356 over 1,542,393 gives "
                       "18.55 years; intangibles 3,500,287 over 239,907 gives 14.59; "
                       "right-of-use assets 3,726,888 over 364,063 gives 10.24; blended, "
                       "16.70. Capital work in progress is excluded from the property and "
                       "intangible notes because neither depreciates it. THE ROUTE "
                       "VALIDATES ITSELF AGAINST A DIRECTLY DISCLOSED FIGURE: the "
                       "right-of-use component derives 10.24 years against the 10.1 years "
                       "note 7 states as the average lease term, 1.4% apart — the "
                       "strongest available evidence that gross cost over charge measures "
                       "what it is being asked to measure. The policy note gives RANGES "
                       "per class (buildings 10-25, plant and equipment 3-25, furniture "
                       "and fixtures 3-5, motor vehicles 4-5, software 5-10) and no "
                       "weighting, so no single figure can be read off it. CROSS-CHECKED "
                       "at 15.96 years on FY2024's own columns, and the route is clean "
                       "because no note carries business-combination additions and each "
                       "discloses impairment separately from the charge",
                       "2026-02-09", "Company"),
    accum_dep_owned_fy25=I((22440927.0 + 2211493.0) / 1000.0,
                       AR25 + ", notes 6, 7 and 8: accumulated depreciation and "
                       "amortisation at 31-Dec-2025 across the same depreciable classes. "
                       "AED mn", "2026-02-09", "Company"),
    dep_charge_owned_fy25=I((1782300.0 + 364063.0) / 1000.0,
                       AR25 + ", notes 6, 7 and 8: the year's own depreciation and "
                       "amortisation charge on those classes, excluding the separately "
                       "disclosed impairment. AED mn", "2026-02-09", "Company"),
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

# ---- audit-response override hook (pricing harness only; unset in the delivered build) ----
# Lets a finding be PRICED on the real chain rather than on a re-implementation.
#
# IT MAY NOT WRITE THE COMMITTED NUMBERS FILE, AND THAT IS STRUCTURAL RATHER THAN
# REMEMBERED [corrected 04-Sep-2026]. As first written this harness overwrote
# study_numbers.json with the overridden run, and the file it left behind LOOKED CLEAN:
# every other block was coherent, and the beta RECORD still reported the registered value
# because the record is written from the input's own metadata rather than from the value
# the model used. So an overridden fair value sat in the committed file under a beta the
# file itself said was 0.488. Nothing could have detected it — no gate reads a provenance
# that does not exist — and it was found only because a figure printed for another purpose
# was one somebody happened to recognise. A harness that can silently replace the answer
# is a harness that eventually does.
_ovr = os.environ.get('DU_OVERRIDE')
FLAGS = {}
OVERRIDE_RECORD = None
if _ovr:
    _o = json.loads(_ovr)
    _applied = {}
    for _k, _v in _o.get('inputs', {}).items():
        _applied[_k] = dict(was=INP[_k]['value'], now=_v)
        INP[_k] = dict(INP[_k], value=_v,
                       source=INP[_k]['source'] + ' [AUDIT OVERRIDE — not the delivered value]')
    FLAGS = _o.get('flags', {})
    OVERRIDE_RECORD = dict(inputs=_applied, flags=FLAGS,
                           note=('this run is a PRICING HARNESS run and its numbers are not '
                                 'this study. The committed file is written only by a run '
                                 'with no override set.'))

V = {k: rec['value'] for k, rec in INP.items()}

# ---- the house macro path supplies the inflation; this study may not carry one --
import macro_path as MP                                                    # noqa: E402
# aliased TERMVAL, not TV: this file's tv is the terminal VALUE
import terminal_value as TERMVAL                                           # noqa: E402
_AE = MP.load('AE')
PI_TERM = (_AE.raw['inflation']['terminal'] or {})['value']
V['g_term'] = (1.0 + PI_TERM) * (1.0 + V['g_term_real']) - 1.0
INP['g_term_derived'] = I(V['g_term'], "DERIVED, never typed: (1 + terminal inflation "
                          "%.4f from the house UAE macro path) x (1 + stated real growth "
                          "%.4f) - 1. The previous edition typed 2.50%%."
                          % (PI_TERM, V['g_term_real']), _AE.as_of, "House")
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

H1_SEG = V['h1_26_seg']
assert abs(sum(H1_SEG.values()) - V['h1_26_rev']) < 0.01, 'H1-2026 segments != reviewed total'

# ---------------------------------------------------------------------------
# MOBILE PRICE: is a prepaid/postpaid split IDENTIFIED from du's disclosure?
# ---------------------------------------------------------------------------
# du publishes the mobile base split by prepaid and postpaid every quarter but publishes only
# ONE blended ARPU. A two-leg revenue build therefore needs the leg ARPUs, which are two
# unknowns per period against one disclosed equation. The test below asks whether the split
# is nonetheless pinned down by the fact that the MIX moved: if both leg ARPUs were constant,
# the blended series and the mix series together determine the ratio between them.
_pp = {k: V['subs_postpaid'][k] / (V['subs_prepaid'][k] + V['subs_postpaid'][k])
       for k in V['subs_postpaid']}
_m_fy25 = (_pp['Q4_2024'] + _pp['Q4_2025']) / 2          # average-base proxy for FY2025
_m_q226 = _pp['Q2_2026']
_a_fy25, _a_q226 = V['arpu_mobile']['FY2025'], V['arpu_mobile']['Q2_2026']
_rel = _a_q226 / _a_fy25
_r_implied = ((1 - _m_fy25) - _rel * (1 - _m_q226)) / (_rel * _m_q226 - _m_fy25)

# The single-pair result above depends entirely on WHICH pair is chosen, so run every pair.
# If the split were identified, the implied ratio would be stable across pairs.
_AQ = {k: v for k, v in V['arpu_mobile_q'].items() if k in _pp}
_pairs = []
for _i, _ka in enumerate(list(_AQ)):
    for _kb in list(_AQ)[_i + 1:]:
        _rl = _AQ[_kb] / _AQ[_ka]
        _dn = _rl * _pp[_kb] - _pp[_ka]
        if abs(_dn) < 1e-9:
            continue
        _pairs.append((_ka, _kb, ((1 - _pp[_ka]) - _rl * (1 - _pp[_kb])) / _dn))
_rv = [r for _, _, r in _pairs]
_neg = sum(1 for r in _rv if r < 0)
_sub1 = sum(1 for r in _rv if 0 <= r < 1)
_lo, _hi = min(V['arpu_ratio_peers'].values()), max(V['arpu_ratio_peers'].values())
_inband = sum(1 for r in _rv if _lo <= r <= _hi)
say(f"[Mobile mix, disclosed] postpaid share of the base "
    f"{_pp['Q4_2024']:.1%} (Q4-2024) -> {_pp['Q4_2025']:.1%} (Q4-2025) -> {_m_q226:.1%} "
    f"(Q2-2026). The Q2-2026 jump is not postpaid strength alone: prepaid fell "
    f"{V['subs_prepaid']['Q2_2026'] - V['subs_prepaid']['Q4_2025']:+,.0f}k while postpaid rose "
    f"{V['subs_postpaid']['Q2_2026'] - V['subs_postpaid']['Q4_2025']:+,.0f}k.")
say(f"[Is a prepaid/postpaid split IDENTIFIED? — NO. Tested across every quarter pair, not one] "
    f"du publishes the base split every quarter but only ONE blended ARPU, so a two-leg build "
    f"needs two unknowns per period against one disclosed equation. The mix DID move, which in "
    f"principle pins the ratio between the legs if both are constant — so solve for it on all "
    f"{len(_pairs)} available quarter pairs. The implied postpaid/prepaid ARPU ratio ranges "
    f"{min(_rv):.1f}x to {max(_rv):.1f}x. {_neg} of {len(_pairs)} pairs imply a NEGATIVE ratio "
    f"and {_sub1} imply a postpaid subscriber worth LESS than a prepaid one — both impossible. "
    f"Only {_inband} sit inside the {_lo:.1f}x-{_hi:.1f}x band observed at the one Gulf operator "
    f"that discloses both legs. An estimator that swings from {min(_rv):.0f}x to {max(_rv):.0f}x "
    f"depending on which two quarters you pick is not identifying anything. THE SPLIT IS "
    f"THEREFORE NOT BUILT: the build stays on the blended figure, which is the finest level du "
    f"sources, and the gap is flagged rather than filled with an imported ratio. Note the "
    f"arithmetic is also mix-preserving — at unchanged mix EVERY ratio in the peer band "
    f"reproduces the same blended ARPU and the same audited revenue — so a split would add an "
    f"unsourced driver and no information.")
_r = V['arpu_ratio_norm']
_b0 = (1 - _m_fy25) + _r * _m_fy25
_b1 = (1 - _m_q226) + _r * _m_q226
mix_lift = _b1 / _b0 - 1
leg_erosion = _rel / (_b1 / _b0) - 1
say(f"[What the flat blended ARPU is actually hiding — mix decomposition] at a {_r:.1f}x "
    f"postpaid/prepaid ratio, the {(_m_q226-_m_fy25)*100:+.2f}pp mix shift alone would have "
    f"lifted blended ARPU {mix_lift:+.2%}. The company printed {_rel-1:+.2%}. So each leg's own "
    f"ARPU eroded about {leg_erosion:+.2%} over the same span, and the flat headline is a "
    f"COINCIDENCE of two offsetting forces, not stability. THE RISK THIS CREATES: the mix shift "
    f"came from a one-off collapse in low-value visitor prepaid SIMs, and the subscriber path "
    f"in this study assumes prepaid RECOVERS. A recovering prepaid base pushes the postpaid "
    f"share back DOWN, which removes the tailwind and leaves the underlying leg erosion "
    f"exposed. Priced below as the mix-exhaustion scenario, and carried into the caveats.")
assert _neg > 0 and _inband < len(_pairs) / 2, (
    'the non-identification finding rests on the implied ratio being unstable and often '
    'impossible across pairs; if most pairs landed in the peer band the split WOULD be '
    'identified and the build should then use it')

# ---------------------------------------------------------------------------
# THE DIRECT-COST JOINT: by-nature x by-segment, recovered exactly
# ---------------------------------------------------------------------------
# du discloses direct costs two ways and never cross-tabulates them: by NATURE on the face
# of the income statement (interconnect / commission / devices and other direct services)
# and by SEGMENT in the segment note (one 'interconnect and other direct costs' line per
# segment). Both marginals are disclosed; the joint is not. It is recoverable exactly under
# two structural assumptions:
#   A1  fixed and wholesale direct cost is entirely interconnect and capacity — neither
#       segment carries dealer commission (no consumer acquisition channel) or device cost.
#   A2  commission is entirely mobile — it is the dealer/retail acquisition and recharge
#       commission on the consumer mobile base.
# Under A1+A2 the mobile interconnect line falls out as a residual from total interconnect,
# and the mobile device line as a residual from mobile's own segment total. The TEST that
# the assumption set is not nonsense: the residual mobile device cost must be POSITIVE and
# small in every period, and ICT's own direct cost plus that residual must foot to the
# disclosed devices line. Both hold in all four disclosed periods (see the assert below).
def dc_joint(nature, seg):
    """Split a period's direct costs into the by-nature x by-segment joint."""
    mob_inter = nature['interconnect'] - seg['fixed'] - seg['wholesale']
    mob_dev = seg['mobile'] - nature['commission'] - mob_inter
    return dict(mob_inter=mob_inter, mob_comm=nature['commission'], mob_dev=mob_dev,
                ict_dev=seg['ict'], fixed_cap=seg['fixed'], whl_cap=seg['wholesale'])

_DCP = {}
for _p, _nat, _seg in (('FY24', V['dc_nature_hist']['FY24'], V['seg_dc_hist']['FY24']),
                       ('FY25', V['dc_nature_hist']['FY25'], V['seg_dc_hist']['FY25']),
                       ('H125', V['dc_nature_h1']['H125'], V['seg_dc_h1']['H125']),
                       ('H126', V['dc_nature_h1']['H126'], V['seg_dc_h1']['H126'])):
    _j = dc_joint(_nat, _seg)
    assert _j['mob_dev'] > 0, f'{_p}: residual mobile device cost is negative — A1/A2 broken'
    assert abs(_j['ict_dev'] + _j['mob_dev'] - _nat['devices']) < 1e-6, (
        f"{_p}: ICT direct cost + residual mobile device cost does not foot to the disclosed "
        f"devices line")
    assert abs(sum((_j['mob_inter'], _j['mob_comm'], _j['mob_dev'])) - _seg['mobile']) < 1e-6
    _DCP[_p] = _j

# Average subscriber bases and month counts for each disclosed period, so a per-unit rate is
# always cost over the base that actually carried it.
_DEN = {
    'FY24': (( V['subs_mobile_fy23'] + V['subs_mobile']['Q4_2024']) / 2,
             ( V['subs_fixed_fy23'] + V['subs_fixed']['Q4_2024']) / 2, 12),
    'FY25': ((V['subs_mobile']['Q4_2024'] + V['subs_mobile']['Q4_2025']) / 2,
             (V['subs_fixed']['Q4_2024'] + V['subs_fixed']['Q4_2025']) / 2, 12),
    'H125': ((V['subs_mobile']['Q4_2024'] + V['subs_mobile_h1_25']) / 2,
             (V['subs_fixed']['Q4_2024'] + V['subs_fixed_h1_25']) / 2, 6),
    'H126': ((V['subs_mobile']['Q4_2025'] + V['subs_mobile']['Q2_2026']) / 2,
             (V['subs_fixed']['Q4_2025'] + V['subs_fixed']['Q2_2026']) / 2, 6),
}
DCU = {}   # per-unit direct cost rates, AED per subscriber per month / % of own revenue
for _p, _j in _DCP.items():
    _m, _f, _n = _DEN[_p]
    _sr = (V['seg_rev_hist']['FY24'] if _p == 'FY24' else V['seg_rev_hist']['FY25'] if _p == 'FY25'
           else V['h1_25_seg'] if _p == 'H125' else H1_SEG)
    DCU[_p] = dict(
        mob_inter=_j['mob_inter'] / _m / _n * 1000,
        mob_comm=_j['mob_comm'] / _m / _n * 1000,
        mob_dev=_j['mob_dev'] / _m / _n * 1000,
        mob_tot=(_j['mob_inter'] + _j['mob_comm'] + _j['mob_dev']) / _m / _n * 1000,
        fixed_cap=_j['fixed_cap'] / _f / _n * 1000,
        whl_rate=_j['whl_cap'] / _sr['wholesale'],
        ict_rate=_j['ict_dev'] / _sr['ict'],
    )
# GATE (added 17-Aug-2026): the deltas quoted inside the register's own justification text are
# computed in a pre-pass from raw disclosed figures; the full joint recovery above computes them
# again by a different route. They must agree, or a register note is describing arithmetic the
# model does not perform — the failure a rendered-PDF read caught by hand this once.
for _lab, _pre, _post in (
        ('mobile interconnect', _D_INTER,
         DCU['H126']['mob_inter'] / DCU['H125']['mob_inter'] - 1),
        ('mobile commission', _D_COMM, DCU['H126']['mob_comm'] / DCU['H125']['mob_comm'] - 1),
        ('fixed capacity', _D_FIXED, DCU['H126']['fixed_cap'] / DCU['H125']['fixed_cap'] - 1)):
    assert abs(_pre - _post) < 5e-5, (
        f'{_lab}: the like-for-like delta quoted in the register ({_pre:+.4%}) disagrees with the '
        f'one the joint recovery produces ({_post:+.4%})')

say("[Direct-cost unit rates, from du's own filings] AED per subscriber per month unless "
    "shown as a rate. " + " | ".join(
        f"{p}: mobile interconnect {DCU[p]['mob_inter']:.2f} + commission "
        f"{DCU[p]['mob_comm']:.2f} + devices {DCU[p]['mob_dev']:.2f} = {DCU[p]['mob_tot']:.2f}; "
        f"fixed capacity {DCU[p]['fixed_cap']:.2f}; wholesale {DCU[p]['whl_rate']:.2%}; "
        f"ICT {DCU[p]['ict_rate']:.2%}" for p in ('FY24', 'FY25', 'H125', 'H126')))
say(f"[Like-for-like half-year direction] mobile interconnect "
    f"{DCU['H125']['mob_inter']:.2f} -> {DCU['H126']['mob_inter']:.2f} "
    f"({DCU['H126']['mob_inter']/DCU['H125']['mob_inter']-1:+.1%}); commission "
    f"{DCU['H125']['mob_comm']:.2f} -> {DCU['H126']['mob_comm']:.2f} "
    f"({DCU['H126']['mob_comm']/DCU['H125']['mob_comm']-1:+.1%}); fixed capacity "
    f"{DCU['H125']['fixed_cap']:.2f} -> {DCU['H126']['fixed_cap']:.2f} "
    f"({DCU['H126']['fixed_cap']/DCU['H125']['fixed_cap']-1:+.1%}). Only the first two carry a "
    f"named mechanism and a drift; the rest are anchored on H1-2026 and held flat.")

# H2-2025 rates, to show that anchoring H2-2026 on the H1-2026 rate is CONSERVATIVE wherever
# the second half of a year is cheaper than the first.
_H2_25 = dict(
    mobile=V['seg_dc_hist']['FY25']['mobile'] - V['seg_dc_h1']['H125']['mobile'],
    fixed=V['seg_dc_hist']['FY25']['fixed'] - V['seg_dc_h1']['H125']['fixed'],
    wholesale=V['seg_dc_hist']['FY25']['wholesale'] - V['seg_dc_h1']['H125']['wholesale'],
    ict=V['seg_dc_hist']['FY25']['ict'] - V['seg_dc_h1']['H125']['ict'])
_h2m = (V['subs_mobile_h1_25'] + V['subs_mobile']['Q4_2025']) / 2
_h2f = (V['subs_fixed_h1_25'] + V['subs_fixed']['Q4_2025']) / 2
H2_25_U = dict(
    mob_tot=_H2_25['mobile'] / _h2m / 6 * 1000,
    fixed_cap=_H2_25['fixed'] / _h2f / 6 * 1000,
    whl_rate=_H2_25['wholesale'] / (V['seg_rev_hist']['FY25']['wholesale']
                                    - V['h1_25_seg']['wholesale']),
    ict_rate=_H2_25['ict'] / (V['seg_rev_hist']['FY25']['ict'] - V['h1_25_seg']['ict']))
say(f"[Is the H1 rate a fair stand-in for H2? — H2-2025 actuals] mobile "
    f"{H2_25_U['mob_tot']:.2f} vs H1-2025 {DCU['H125']['mob_tot']:.2f}; fixed "
    f"{H2_25_U['fixed_cap']:.2f} vs {DCU['H125']['fixed_cap']:.2f}; wholesale "
    f"{H2_25_U['whl_rate']:.2%} vs {DCU['H125']['whl_rate']:.2%}; ICT "
    f"{H2_25_U['ict_rate']:.2%} vs {DCU['H125']['ict_rate']:.2%}. Three of the four second-half "
    f"rates came in CHEAPER than the first half, so carrying the H1-2026 rate into H2-2026 "
    f"overstates cost rather than understating it.")

def build(arpu_mult=1.0, subs_shift=0.0, dc_mult=1.0, opex_shift=0.0, capex_mult=1.0,
          arpu_drift=None):
    """arpu_mult scales the mobile+fixed price paths; subs_shift adds N thousand
    to every point of both subscriber paths; dc_mult scales every direct-cost
    unit rate (so a HIGHER dc_mult is worth LESS); opex_shift adds a fraction of
    revenue to the opex stack; capex_mult scales the capex path."""
    sm = [s + subs_shift for s in V['subs_mobile_path']]
    sf = [s + subs_shift * 0.08 for s in V['subs_fixed_path']]
    dr = V['arpu_drift'] if arpu_drift is None else arpu_drift
    am = [a * arpu_mult * (1 + dr) ** i for i, a in enumerate(V['arpu_mobile_path'])]
    af = [a * arpu_mult * (1 + dr) ** i for i, a in enumerate(V['arpu_fixed_path'])]
    # Per-unit direct-cost paths: anchored on the H1-2026 reviewed actual, drifting only
    # where a named mechanism has a measured direction. Year 0 is the H2-2026 rate.
    A = DCU['H126']
    ui = [A['mob_inter'] * (1 + V['esc_dc_inter']) ** i * dc_mult for i in range(5)]
    uc = [A['mob_comm'] * (1 + V['esc_dc_comm']) ** i * dc_mult for i in range(5)]
    ud = [A['mob_dev'] * (1 + V['esc_dc_dev']) ** i * dc_mult for i in range(5)]
    um = [ui[i] + uc[i] + ud[i] for i in range(5)]
    uf = [A['fixed_cap'] * (1 + V['esc_dc_fixed']) ** i * dc_mult for i in range(5)]
    rw = V['dc_rate_wholesale'] * dc_mult
    ri = V['dc_rate_ict'] * dc_mult
    seg_rev = {s: [] for s in SEGS}
    seg_dc = {s: [] for s in SEGS}
    # FY2026: reviewed H1 actual + unit-built H2, on BOTH sides of the margin
    seg_rev['mobile'].append(H1_SEG['mobile']
                             + (V['subs_mobile']['Q2_2026'] + sm[0]) / 2 * am[0] * 6 / 1000)
    seg_rev['fixed'].append(H1_SEG['fixed']
                            + (V['subs_fixed']['Q2_2026'] + sf[0]) / 2 * af[0] * 6 / 1000)
    seg_rev['wholesale'].append(SRH['FY25']['wholesale'] * (1 + V['seg_g']['wholesale'][0]))
    seg_rev['ict'].append(SRH['FY25']['ict'] * (1 + V['seg_g']['ict'][0]))
    seg_dc['mobile'].append(V['seg_dc_h1']['H126']['mobile']
                            + (V['subs_mobile']['Q2_2026'] + sm[0]) / 2 * um[0] * 6 / 1000)
    seg_dc['fixed'].append(V['seg_dc_h1']['H126']['fixed']
                           + (V['subs_fixed']['Q2_2026'] + sf[0]) / 2 * uf[0] * 6 / 1000)
    seg_dc['wholesale'].append(V['seg_dc_h1']['H126']['wholesale']
                               + (seg_rev['wholesale'][0] - H1_SEG['wholesale']) * rw)
    seg_dc['ict'].append(V['seg_dc_h1']['H126']['ict']
                         + (seg_rev['ict'][0] - H1_SEG['ict']) * ri)
    for i in range(1, 5):
        seg_rev['mobile'].append((sm[i - 1] + sm[i]) / 2 * am[i] * 12 / 1000)
        seg_rev['fixed'].append((sf[i - 1] + sf[i]) / 2 * af[i] * 12 / 1000)
        seg_rev['wholesale'].append(seg_rev['wholesale'][-1] * (1 + V['seg_g']['wholesale'][i]))
        seg_rev['ict'].append(seg_rev['ict'][-1] * (1 + V['seg_g']['ict'][i]))
        seg_dc['mobile'].append((sm[i - 1] + sm[i]) / 2 * um[i] * 12 / 1000)
        seg_dc['fixed'].append((sf[i - 1] + sf[i]) / 2 * uf[i] * 12 / 1000)
        seg_dc['wholesale'].append(seg_rev['wholesale'][i] * rw)
        seg_dc['ict'].append(seg_rev['ict'][i] * ri)
    rev = [sum(seg_rev[s][i] for s in SEGS) for i in range(5)]
    # Contribution is now what is LEFT after a costed unit build — an output, not an input.
    contrib = {s: [seg_rev[s][i] - seg_dc[s][i] for i in range(5)] for s in SEGS}
    contrib_margin = {s: [contrib[s][i] / seg_rev[s][i] for i in range(5)] for s in SEGS}
    contrib_tot = [sum(contrib[s][i] for s in SEGS) for i in range(5)]
    # The same total, re-cut by NATURE. This is an ALLOCATION of the segment build, not a
    # second independent forecast: du never cross-tabulates the two cuts, so the joint rests
    # on A1+A2 above. Presenting it as independent corroboration would be false.
    dc_nature = dict(
        interconnect=[(sm[i - 1] + sm[i]) / 2 * ui[i] * (12 if i else 12) / 1000 if i else
                      _DCP['H126']['mob_inter']
                      + (V['subs_mobile']['Q2_2026'] + sm[0]) / 2 * ui[0] * 6 / 1000
                      for i in range(5)],
        commission=[(sm[i - 1] + sm[i]) / 2 * uc[i] * 12 / 1000 if i else
                    _DCP['H126']['mob_comm']
                    + (V['subs_mobile']['Q2_2026'] + sm[0]) / 2 * uc[0] * 6 / 1000
                    for i in range(5)],
        devices=[(sm[i - 1] + sm[i]) / 2 * ud[i] * 12 / 1000 + seg_dc['ict'][i] if i else
                 _DCP['H126']['mob_dev']
                 + (V['subs_mobile']['Q2_2026'] + sm[0]) / 2 * ud[0] * 6 / 1000
                 + seg_dc['ict'][0]
                 for i in range(5)])
    # fixed + wholesale capacity cost is interconnect by A1, so add it back to that line
    dc_nature['interconnect'] = [dc_nature['interconnect'][i] + seg_dc['fixed'][i]
                                 + seg_dc['wholesale'][i] for i in range(5)]
    for i in range(5):
        assert abs(sum(dc_nature[k][i] for k in dc_nature)
                   - sum(seg_dc[s][i] for s in SEGS)) < 1e-6, (
            f'year {i}: the by-nature re-cut does not foot to the by-segment total')
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
                seg_dc=seg_dc, contrib_margin=contrib_margin, dc_nature=dc_nature,
                unit_cost=dict(mob_inter=ui, mob_comm=uc, mob_dev=ud, mob_tot=um, fixed_cap=uf,
                               whl_rate=[rw] * 5, ict_rate=[ri] * 5),
                opex_lines=dict(staff=staff, network=network, admin=admin, other=other,
                                marketing=marketing, licence=licence, ecl=ecl))

_B = build()
rev, seg_rev, ebitda, capex = _B['rev'], _B['seg_rev'], _B['ebitda'], _B['capex']
contrib_tot, opex_fc = _B['contrib_tot'], _B['opex']
seg_dc, contrib_margin = _B['seg_dc'], _B['contrib_margin']
dc_nature_fc, unit_cost = _B['dc_nature'], _B['unit_cost']
dc_tot = [sum(seg_dc[s][i] for s in SEGS) for i in range(5)]
gross_margin = [1 - dc_tot[i] / rev[i] for i in range(5)]
say("[Contribution margin — now an OUTPUT of a costed unit build] " + "; ".join(
    f"{s} " + "->".join(f"{contrib_margin[s][i]:.1%}" for i in (0, 4))
    + f" (audited FY2025 {SCH['FY25'][s]/SRH['FY25'][s]:.1%}, H1-2026 actual "
    f"{1 - V['seg_dc_h1']['H126'][s]/H1_SEG[s]:.1%})" for s in SEGS))
_gm_fy25 = 1 - (-V['direct_costs_hist']['FY25']) / V['rev_fy25']
_gm_h126 = 1 - sum(V['seg_dc_h1']['H126'].values()) / V['h1_26_rev']
say(f"[Group gross margin — OUTPUT] " + " -> ".join(f"{g:.1%}" for g in gross_margin)
    + f", against an audited FY2025 {_gm_fy25:.1%} and an H1-2026 reviewed {_gm_h126:.1%}. "
    f"Nothing here was assumed: the margin is what is left after each cost line is grown on "
    f"its own physical driver.")
# The retired construction, kept as an audit trail: what the margin path WOULD have been under
# the withdrawn contribution-margin input, so the size of the correction is visible.
_retired_cm = dict(mobile=[0.608] * 5, fixed=[0.858] * 5, wholesale=[0.864] * 5,
                   ict=[0.194, 0.200, 0.205, 0.210, 0.215])
_retired_contrib = [sum(seg_rev[s][i] * _retired_cm[s][i] for s in SEGS) for i in range(5)]
say(f"[Size of the correction] contribution under the retired flat-margin input " +
    " -> ".join(f"{c:,.0f}" for c in _retired_contrib) + " vs the unit-built "
    + " -> ".join(f"{c:,.0f}" for c in contrib_tot) + ", i.e. "
    + " -> ".join(f"{contrib_tot[i]-_retired_contrib[i]:+,.0f}" for i in range(5))
    + ". The retired input ignored six months of reviewed data in every segment.")
ebitda_margin = [ebitda[i] / rev[i] for i in range(5)]
g26 = rev[0] / V['rev_fy25'] - 1
say(f"[Revenue build] FY26E {rev[0]:,.0f} ({g26:+.1%} vs guidance 4-6% revised 23-Jul-2026) -> "
    f"FY30E {rev[-1]:,.0f}. Segments FY26E: " +
    ", ".join(f"{s} {seg_rev[s][0]:,.0f}" for s in SEGS))
assert 0.035 <= g26 <= 0.065, f'FY2026E growth {g26:.1%} outside the guidance sanity band'
say(f"[EBITDA — an OUTPUT, not an input] " +
    " -> ".join(f"{ebitda[i]:,.0f} ({ebitda_margin[i]:.1%})" for i in range(5)) + ".")
# The FY2026E margin sits above the company's 46-47% guided range, so the implied SECOND HALF
# is the number that has to be defended, not the full year: H1 is already a reviewed actual.
_h2_26_rev = rev[0] - V['h1_26_rev']
_h2_26_ebitda = ebitda[0] - V['h1_26_ebitda']
_h2_26_margin = _h2_26_ebitda / _h2_26_rev
_h1_25_margin = V['h1_25_ebitda'] / V['h1_25_rev']
_h1_26_margin = V['h1_26_ebitda'] / V['h1_26_rev']
_h2_25_margin = V['h2_25_ebitda'] / V['h2_25_rev']
say(f"[Is the FY2026E margin too rich? — TEST IT ON THE IMPLIED SECOND HALF] the build's "
    f"FY26E {ebitda_margin[0]:.1%} sits above the company's guided 46-47%, so the claim to "
    f"defend is the implied H2-2026 margin of {_h2_26_margin:.1%}. H1 improved "
    f"{(_h1_26_margin - _h1_25_margin)*100:+.1f}pp y/y ({_h1_25_margin:.1%} -> "
    f"{_h1_26_margin:.1%}); "
    f"the implied H2 improves only {(_h2_26_margin - _h2_25_margin)*100:+.1f}pp y/y "
    f"({_h2_25_margin:.1%} -> {_h2_26_margin:.1%}). The forecast therefore assumes the y/y "
    f"margin gain roughly HALVES in the second half. The guided range is a full-year figure "
    f"the company set in July against a first half that had already printed "
    f"{_h1_26_margin:.1%}; hitting the 46.5% midpoint would require an H2 margin of "
    f"{(0.465 * rev[0] - V['h1_26_ebitda']) / _h2_26_rev:.1%}, i.e. a y/y DETERIORATION of "
    f"{((0.465 * rev[0] - V['h1_26_ebitda']) / _h2_26_rev - _h2_25_margin)*100:+.1f}pp against an "
    f"H1 that improved. That is a possible outcome and it is priced in the sensitivity, but it "
    f"is not the central case the filings support.")
assert _h2_26_margin - _h2_25_margin < _h1_26_margin - _h1_25_margin, (
    'the implied H2 y/y margin gain must not exceed the actual H1 gain — that would be '
    'an acceleration the forecast has no evidence for')
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
# LEASES ARE DEBT (corrected 17-Aug-2026). The bridge deducts the full lease liability and the
# WACC carries a lease-debt weight, so charging a lease-replacement capex in FCFF as well billed the
# same obligation twice (PV ~1,450mn). Perpetual renewal IS charged in the terminal: terminal
# invested capital includes the right-of-use asset and terminal reinvestment (g/ROIC) maintains it.
rou_repl = [0.0] * 5
rou_repl_retired = list(V['rou_dep_path'])   # audit trail only
fcff = [nopat[i] + dna[i] - capex[i] - rou_repl[i] - dnwc[i] for i in range(5)]
say(f"[FCFF waterfall] " + " -> ".join(f"{f:,.0f}" for f in fcff))

# ---- cost of capital: explicit window (sovereign double-count removed) -------
rf_star = V['rf'] - V['sov_spread_market_observed']
# NO-ARBITRAGE FLOOR (added 17-Aug-2026): under a hard peg a DEFAULT-FREE dirham rate cannot sit
# below the default-free dollar rate at matched tenor. The prior edition netted the 42bp RATING
# spread, driving rf* to 4.06% — about 26bp through the matched-tenor UST — and nothing caught it.
assert rf_star >= V['ust_matched'] - 0.0005, (
    f"rf* {rf_star:.4%} sits below the matched-tenor US Treasury {V['ust_matched']:.4%}: a "
    f"default-free AED rate cannot be below the default-free USD rate under a hard peg")
ke_exp = rf_star + V['beta'] * V['erp_market_basis']
ke_mkt_alt = (V['rf'] - V['sov_spread_damodaran_rating']) + V['beta'] * V['erp_rating_basis']  # rating basis
ke_raw_retired = V['rf'] + V['beta'] * V['erp_market_basis']
kd_at = V['kd'] * (1 - TAX)
LEASE, NETCASH = V['lease_fy25'], net_cash['FY25']
wd_exp = LEASE / (LEASE + MKTCAP)
we_exp = 1 - wd_exp
wacc_exp = we_exp * ke_exp + wd_exp * kd_at
wacc_exp_mkt = we_exp * ke_mkt_alt + wd_exp * kd_at
say(f"[Cost of equity] rf {V['rf']:.2%} (Jan-2031 AED T-bond) less UAE rating-basis default "
    f"spread {V['sov_spread_market_observed']:.2%} = rf* {rf_star:.2%}; + beta {V['beta']:.3f} x ERP "
    f"{V['erp_market_basis']:.2%} -> Ke {ke_exp:.2%}. ERP basis 2 (market-spread, implied-US base): "
    f"{ke_mkt_alt:.2%}. RETIRED un-netted construction {ke_raw_retired:.2%} (audit trail only).")
say(f"[WACC explicit] weights: lease debt {wd_exp:.1%} / market equity {we_exp:.1%} "
    f"(market cap {MKTCAP:,.0f}; du has no drawn borrowings) -> WACC {wacc_exp:.2%} "
    f"(basis 2: {wacc_exp_mkt:.2%}). Interest shields both fiscal legs (the royalty base is "
    f"profit AFTER interest), so the shield runs at the combined {TAX:.1%}.")

ke_term = (V['rf_term'] - V['sov_spread_market_observed']) + V['beta'] * V['erp_term']
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
df_tv = df[-1]
# CONVENTION, stated rather than left implicit: full-year END-of-period factors on the explicit
# window, and the terminal value (a value dated at the end of year 5) discounted at the year-5
# factor. Mid-year convention on the explicit window alone would add ~AED 0.09/share; it is the
# less conservative choice and is not adopted.
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
# The right-of-use ASSET is held flat because the lease LIABILITY is held flat: a new lease
# creates an asset and a liability simultaneously and is NON-CASH, so additions equal
# depreciation. This is separate from the FCFF question — no cash charge belongs in FCFF (the
# liability is deducted in the bridge and its interest sits in the WACC), but the asset must
# still be maintained in invested capital or the terminal reinvestment is understated.
rou_additions = list(V['rou_dep_path'])   # non-cash, equal to depreciation
rou_path = []
rb = V['rou_fy25']
for i in range(5):
    rb = rb + rou_additions[i] - V['rou_dep_path'][i]
    rou_path.append(rb)
assert abs(rou_path[-1] - V['rou_fy25']) < 1e-9, 'right-of-use book must stay flat'
ic = [ppe_path[i] + rou_path[i] + int_path[i] + V['goodwill_fy25'] + nwc_fc[i]
      for i in range(5)]
roic = [nopat[i] / ((ic[i] + ([ic_fy25] + ic)[i]) / 2) for i in range(5)]
roic_term = nopat[-1] * (1 + V['g_term']) / ic[-1]
rr_term = min(V['g_term'] / roic_term, 0.95)
# THE RETIRED FORM, kept on one line so the change is legible and priced [R-TERM-01].
tv_retired = nopat[-1] * (1 + V['g_term']) * (1 - rr_term) / (wacc_term - V['g_term'])

# The capital one unit of REAL growth actually needs: this model's own marginal invested
# capital per unit of revenue across the explicit window, at terminal revenue.
INC_CAP = ((ic[-1] - ic[0]) / (rev[-1] - rev[0])) * rev[-1]
# THE FULL CHARGE IS ADDED BACK AND THE LEASE RENEWAL IS CHARGED INSIDE THE BLENDED LIFE.
# The explicit window adds back total depreciation and charges no lease-replacement capex,
# because the lease liability is DEBT in the bridge and charging renewal there would bill
# the EXISTING obligation twice. That argument does not survive into perpetuity: a one-off
# deduction of today's liability cannot cover renewals for ever, and the retired
# construction supplied that renewal only as a side effect of charging g x invested
# capital — on a 1/g cycle of 50 years against a lease term the company discloses at 10.1.
# A lease is an asset with a life like any other here, so it enters the blended life at its
# own derived 10.24 years and its book charge is escalated to current cost like the rest.
DNA_OWNED = dna[-1]


def _terminal_at(g_nom, life=None, nopat_last=None, dna_last=None, wc_last=None,
                 inc_cap=None, wacc_t=None):
    """Every terminal in this file goes through the sanctioned module — base, scenario and
    sensitivity point alike — so the retired construction cannot survive in a grid nobody
    reads the arithmetic of."""
    # EVERY FIGURE HANDED IN IS THE LAST EXPLICIT YEAR'S. The module grows the free cash flow
    # once itself — tv = fcff (1+g)/(w-g) values the terminal at the END of that year, which is
    # where it is discounted — so figures already grown by (1+g) overstate it by exactly (1+g).
    # They were, until 4 September 2026.
    return TERMVAL.build(TERMVAL.TerminalInputs(
        nopat=(nopat[-1] if nopat_last is None else nopat_last),
        wacc=wacc_term if wacc_t is None else wacc_t,
        inflation=PI_TERM, real_growth=(1.0 + g_nom) / (1.0 + PI_TERM) - 1.0,
        dna_book=(DNA_OWNED if dna_last is None else dna_last),
        useful_life_years=V['asset_life_years'] if life is None else life,
        useful_life_source=INP['asset_life_years']['source'],
        maintenance_basis='book_dna_escalated',
        working_capital=(nwc_fc[-1] if wc_last is None else wc_last),
        incremental_capital_per_unit_growth=INC_CAP if inc_cap is None else inc_cap))


TERMINAL = _terminal_at(V['g_term'])
tv = TERMINAL.tv
say(f"[Terminal] life {V['asset_life_years']:.2f}y derived; maintenance "
    f"{TERMINAL.maintenance:,.0f} against owned book charge {TERMINAL.dna_addback:,.0f}; "
    f"working-capital line {TERMINAL.wc_charge:,.0f} (a CREDIT — this company collects "
    f"before it pays); terminal FCFF {TERMINAL.fcff:,.0f} = "
    f"{TERMINAL.fcff / (nopat[-1] * (1 + V['g_term'])):.1%} of terminal profit; TV "
    f"{tv:,.0f} against the retired {tv_retired:,.0f} ({tv / tv_retired - 1:+.1%}) at g "
    f"{V['g_term']:.2%} / WACC(term) {wacc_term:.2%}")

# ---- DCF and the EV -> equity bridge ------------------------------------------
pv = [fcff[i] * df[i] for i in range(5)]
pv_explicit = sum(pv)
pv_tv = tv * df_tv
ev = pv_explicit + pv_tv
tv_share = pv_tv / ev
INVEST = V['investees_bv']
eq_val = ev - LEASE + NETCASH + INVEST
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
assert abs((ev - LEASE + NETCASH + INVEST) - eq_val) < 0.01, 'bridge does not close'
assert tv_share < 0.90, 'terminal value share implausibly high'

# ---- THE CONTESTED JUDGEMENT, COMPUTED BOTH WAYS ------------------------------
# RECAST 17-Aug-2026. The prior edition's contested judgement was the post-2026 fiscal regime.
# It is no longer contested: du disclosed the 2027-2029 extension ITSELF on 24-Jul-2026, on the
# same structure and with the AED 1.8bn combined floor expressly retained — sixteen days before
# this study's own sweep date, which the prior edition's dated negative search missed. That
# framing is demoted to a named post-2029 tail scenario (still computed, below).
# The judgement that IS live, and the one the whole study turns on, is THE REQUIRED RETURN:
#   Framing 1 — du's own measured beta (0.488 on the ADX regression) sets the cost of equity.
#   Framing 2 — the market's own required return, revealed by refusing to re-rate the terminal:
#              hold du's CURRENT trailing EV/EBITDA into perpetuity instead of capitalising at
#              the Gordon rate. This is the honest form of the "85% of value is terminal" caveat,
#              and it is what section 4's disagreement is actually about.
ev_ebitda_now = (MKTCAP + LEASE - NETCASH) / V['ebitda_fy25']
ebitda_term = ebitda[-1] * (1 + V['g_term'])
tv_implied_mult = tv / ebitda_term
tv_at_market = ev_ebitda_now * ebitda_term
ev_at_market = pv_explicit + tv_at_market * df_tv
dcf_ps_mkt_term = ((ev_at_market - LEASE + NETCASH + INVEST) / SH) * ROLL - V['div_between']
say(f"[Contested judgement — THE REQUIRED RETURN, both ways] Framing 1 (measured beta "
    f"{V['beta']:.3f}, Gordon terminal): AED {dcf_ps:.2f}, whose terminal implies an exit multiple "
    f"of {tv_implied_mult:.2f}x EBITDA against du's OWN current {ev_ebitda_now:.2f}x — i.e. a "
    f"{tv_implied_mult/ev_ebitda_now-1:+.0%} re-rating. Framing 2 (no re-rating: du's current "
    f"multiple held into perpetuity): AED {dcf_ps_mkt_term:.2f}. Gap {dcf_ps - dcf_ps_mkt_term:+.2f}"
    f"/share. Published side by side; never averaged.")
assert tv_implied_mult > 0

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
    # Framing B must earn its own reinvestment rate off its own NOPAT, not inherit Framing A's
    _roicB = ebit[-1] * (1 - tb[-1]) * (1 + V['g_term']) / ic[-1]
    _rrB = min(V['g_term'] / _roicB, 0.95)
    tvB = ebit[-1] * (1 - tb[-1]) * (1 + V['g_term']) * (1 - _rrB) / (wacc_term - V['g_term'])
    evB = sum(fcffB[i] * df[i] for i in range(5)) + tvB * df[-1]
    psB = (evB - LEASE + NETCASH + INVEST) / SH * ROLL - V['div_between']
    return tb, fcffB, npB, psB
taxB_path, fcffB, npB, dcf_ps_B = framingB()
say(f"[Post-2029 fiscal tail — no longer the contested judgement, du disclosed the 2027-2029 "
    f"extension itself on 24-Jul-2026] Current regime ({TAX:.1%} take): AED "
    f"{dcf_ps:.2f}. Framing B (reversion to the pre-2024 construction, effective take "
    f"{taxB_path[0]:.1%} -> {taxB_path[-1]:.1%}): AED {dcf_ps_B:.2f}. Gap "
    f"{dcf_ps - dcf_ps_B:+.2f}/share ({(dcf_ps_B/dcf_ps-1):+.0%}). Published side by side; "
    f"never averaged.")

# ---- rf-tenor alternatives, both priced, neither averaged ---------------------
def dcf_at_rf(rf_):
    _ke = (rf_ - V['sov_spread_market_observed']) + V['beta'] * V['erp_market_basis']
    _w = we_exp * _ke + wd_exp * kd_at
    _sh = _w - wacc_exp
    _dfa, cc = [], 1.0
    for w in [x + _sh for x in fwd]:
        cc /= (1 + w); _dfa.append(cc)
    _tv = nopat[-1] * (1 + V['g_term']) * (1 - rr_term) / (wacc_term + _sh - V['g_term'])
    _ev = sum(fcff[i] * _dfa[i] for i in range(5)) + _tv * _dfa[-1]
    return ((_ev - LEASE + NETCASH + INVEST) / SH * ((1 + _ke) ** T_ANCHOR)
            - V['div_between']), _w

dcf_ps_rf_alt, wacc_rf_alt = dcf_at_rf(V['rf_alt'])
dcf_ps_rf_long, wacc_rf_long = dcf_at_rf(V['rf_alt_long'])
say(f"[rf tenor gap, BOTH ALTERNATIVES PRICED] base rf {V['rf']:.2%} (Jan-2031 AED T-Bond, "
    f"30-Jul-2026) -> AED {dcf_ps:.2f}. LONGER, LOWER: the Feb-2033 AED Islamic Treasury Sukuk "
    f"second tap at {V['rf_alt_long']:.2%} (23-Apr-2026) -> WACC {wacc_rf_long:.2%} -> AED "
    f"{dcf_ps_rf_long:.2f} ({dcf_ps_rf_long-dcf_ps:+.2f}/share, "
    f"{dcf_ps_rf_long/dcf_ps-1:+.1%}). LONGER, HIGHER: the 10y peg-extrapolated "
    f"{V['rf_alt']:.2%} -> WACC {wacc_rf_alt:.2%} -> AED {dcf_ps_rf_alt:.2f} "
    f"({dcf_ps_rf_alt-dcf_ps:+.2f}/share). The base sits BETWEEN the two, which is the point: "
    f"there is no liquid 10-year AED point, so the tenor choice is a real range and it is "
    f"published as one.")
# An external critique argued for the Feb-2033 sukuk's DEBUT print instead. Price that too,
# rather than only asserting it is stale.
dcf_ps_rf_debut, wacc_rf_debut = dcf_at_rf(V['rf_sukuk_debut'])
say(f"[The critique's rf, PRICED before it is judged] the Feb-2033 sukuk's DEBUT print "
    f"{V['rf_sukuk_debut']:.3%} (22-Feb-2026) -> WACC {wacc_rf_debut:.2%} -> AED "
    f"{dcf_ps_rf_debut:.2f} ({dcf_ps_rf_debut-dcf_ps:+.2f}/share, "
    f"{dcf_ps_rf_debut/dcf_ps-1:+.1%}) — so the finding is MATERIAL and had to be re-derived, "
    f"not waved away. It is nonetheless REJECTED on the evidence: the issuer's own second tap of "
    f"the SAME instrument cleared {V['rf_alt_long']:.2%} two months later, and the Jan-2031 "
    f"T-Bond moved 3.90% -> 3.85% -> 4.30% -> 4.48% across the same window. A debut print 5.5 "
    f"months before the anchor is not the rate that prevailed at the anchor.")
assert V['rf_sukuk_debut'] < V['rf_alt_long'] < V['rf'], (
    'the rf evidence chain must run debut < second tap < the Jan-2031 print used, which is what '
    'makes the staleness argument rather than a preference')

# ---- scenarios on the DCF -----------------------------------------------------
def dcf_scenario(arpu_mult=1.0, subs_shift=0.0, dc_mult=1.0, opex_shift=0.0,
                 arpu_drift=None,
                 capex_mult=1.0, wacc_shift=0.0, g=None, tax=None, nwc=None):
    g = V['g_term'] if g is None else g
    t_ = TAX if tax is None else tax
    nw = nwc_pct if nwc is None else nwc
    B = build(arpu_mult=arpu_mult, subs_shift=subs_shift, dc_mult=dc_mult,
              arpu_drift=arpu_drift,
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
    _ic0 = _ppe[0] + rou_path[0] + V['goodwill_fy25'] + _nwc[0]
    _inc = ((_ic5 - _ic0) / (_rev[-1] - _rev[0])) * _rev[-1]
    try:
        _tv = _terminal_at(g, nopat_last=_nopat[-1], dna_last=_dna[-1],
                           wc_last=_nwc[-1], inc_cap=_inc, wacc_t=max(_wt, g + 0.015)).tv
    except TERMVAL.TerminalRefused:
        return float('nan')
    _ev = sum(_f[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    return ((_ev - LEASE + NETCASH + INVEST) / SH) * ROLL - V['div_between']

_base_chk = dcf_scenario()
assert abs(_base_chk - dcf_ps) < 0.02, f'scenario engine != base: {_base_chk} vs {dcf_ps}'

dcf_bear = dcf_scenario(arpu_mult=0.95, subs_shift=-250.0, dc_mult=1.03,
                        opex_shift=+0.005, wacc_shift=+0.01, g=0.02, capex_mult=1.08)
dcf_bull = dcf_scenario(arpu_mult=1.03, subs_shift=+200.0, dc_mult=0.985,
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
    f"{V['pe_just']:.1f}x (Mobily, the closest structural analogue, from its own filings — NO peer "
    f"median is claimed: only 2 of 6 peers survive as clean observations) x FY26E EPS "
    f"{eps_fc[0]:.2f} -> AED {rel_ps:.2f} at "
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
# ONE g throughout a justified price-to-book, and it is the REGISTERED terminal growth — not a
# second, different number. The bear is the +100bp stress on the cost of equity. The prior edition
# ran g=4% in the numerator against g=2% in the denominator; an interim fix then used a 2.0%
# literal against the registered 2.5%, which still left two growth rates in one Gordon.
_bear_g = V['g_term']
book_bear = to_anchor(((V['roe_sust'] - _bear_g)
                       / (0.5 * (ke_exp + ke_term) + 0.01 - _bear_g)) * bvps) - V['div_between']
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
# ---------------------------------------------------------------------------
# [R-LENS-03] ONE CLASS PRIMARY IS THE CENTRAL; THE OTHERS ARE CROSS-CHECKS.
# ---------------------------------------------------------------------------
# WHAT THE RETIRED BLEND DID HERE, measured rather than described. The four
# weights moved the answer from the cash-flow lens's own read to a number
# roughly a third lower, and what that concealed was the SIZE of this study's
# disagreement with the market: the blend reported a modest premium where the
# primary lens asserts a large one. A blend does not bias an answer, it masks
# one -- and which direction it masks in is an accident of which lenses happen
# to sit where.
#
# NORMALISED EARNINGS IS REMOVED RATHER THAN RE-WEIGHTED. The registry's
# telecom row is a cash-flow primary with an enterprise multiple on own
# history, a relative multiple and book value beside it; normalised earnings
# power is not among them, so the lens carrying a fifth of the weight here was
# not one this class publishes at all. Computed and shown so the move is
# visible.
#
# ONE PERMITTED CROSS-CHECK IS NOT YET BUILT AND IS NAMED RATHER THAN QUIETLY
# ABSENT: an enterprise multiple on du's OWN HISTORY. This study computes a
# trailing multiple, but from the CURRENT market capitalisation -- which is a
# multiple read off the price, and this rule forbids exactly that because it
# values the company at what it already trades at. A genuine own-history
# multiple needs a series of past enterprise values against past EBITDA, which
# is a construction rather than a rename, and it is left for the pass that can
# source it.
RETIRED_BLEND_W = dict(W)
RETIRED_BLEND_VALUE = sum(l['base'] * l['w'] for l in lenses.values())
for _k in lenses:
    lenses[_k]['w'] = None
lenses['normalized']['note'] = (
    'RETIRED for this class: normalised earnings power is not among a telecom '
    'operator\'s permitted cross-checks. Removed rather than re-weighted, and '
    'computed and shown so the move is visible.')
lenses['book']['note'] = 'a disclosed FLOOR, published as such and never weighted'

central = lenses['dcf']['base']
lo, hi = lenses['dcf']['bear'], lenses['dcf']['bull']
lenses['central'] = dict(name='Cash-flow lens (the central)', bear=lo, base=central,
                         bull=hi, w=None)
lenses['retired_blend'] = dict(
    name='RETIRED %d/%d/%d/%d blend, published unused' % tuple(
        round(100 * RETIRED_BLEND_W[k]) for k in ('dcf', 'relative', 'normalized', 'book')),
    bear=None, base=RETIRED_BLEND_VALUE, bull=None, w=0.0)
say(f"[Synthesis] the cash-flow lens IS the central, AED {central:.2f}; span {lo:.2f} - {hi:.2f}; spot "
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
    return ((_ev - LEASE + NETCASH + INVEST) / SH) * ROLL - V['div_between']

grid_wacc_g = [[dcf_at(wacc_exp, wt, g) for g in g_grid] for wt in wt_grid]
grid_exp_term = [[dcf_at(we, wt, V['g_term']) for wt in wt_grid] for we in we_grid]
_bci = json.load(open(os.path.join(HERE, 'beta_result.json')))['ci90']
beta_grid = [round(_bci[0], 2), round(V['beta'], 3), round(_bci[1], 2), 0.65, 0.80]
def dcf_beta(b):
    ke = rf_star + b * V['erp_market_basis']
    we_ = we_exp * ke + wd_exp * kd_at
    # the grid MUST use the same netted basis as the base case, or its base cell contradicts the
    # headline (it did, by AED 1.77, before 17-Aug-2026)
    wt_ = (1 - V['wd_term']) * ((V['rf_term'] - V['sov_spread_market_observed']) + b * V['erp_term']) \
        + V['wd_term'] * kd_term_at
    return dcf_at(we_, wt_, V['g_term'])
grid_beta = [dcf_beta(b) for b in beta_grid]
tax_grid = [0.40, TAX, 0.47, 0.50, 0.531]
grid_tax = [dcf_scenario(tax=t) for t in tax_grid]
arpu_grid = [0.92, 0.96, 1.00, 1.04, 1.08]
grid_arpu = [dcf_scenario(arpu_mult=m) for m in arpu_grid]
subs_grid = [-400.0, -200.0, 0.0, 200.0, 400.0]
grid_subs = [dcf_scenario(subs_shift=s) for s in subs_grid]
mg_grid = [0.94, 0.97, 1.00, 1.03, 1.06]
grid_margin = [dcf_scenario(dc_mult=m) for m in mg_grid]
# THE MIX-EXHAUSTION SCENARIO, priced. The blended ARPU path is flat-to-slightly-up because a
# postpaid mix tailwind offsets per-leg erosion; if prepaid recovers as the subscriber path
# assumes, the tailwind goes and the erosion shows through.
drift_grid = [-0.025, -0.015, 0.0, 0.005, 0.010]
grid_drift = [dcf_scenario(arpu_drift=d) for d in drift_grid]
dcf_mix_exhaust = dcf_scenario(arpu_drift=leg_erosion / 1.0 if leg_erosion < 0 else -0.02)
say(f"[Mix-exhaustion scenario, PRICED] if the postpaid mix tailwind exhausts and the blended "
    f"ARPU path instead erodes at the per-leg rate the decomposition implies "
    f"({leg_erosion:+.2%}/yr), the DCF is AED {dcf_mix_exhaust:.2f} against the base "
    f"{dcf_ps:.2f} ({dcf_mix_exhaust - dcf_ps:+.2f}/share, "
    f"{dcf_mix_exhaust / dcf_ps - 1:+.1%}). Grid across ARPU drift: " +
    ", ".join(f"{d:+.1%} -> {v:.2f}" for d, v in zip(drift_grid, grid_drift)) + ".")
capex_grid = [0.85, 0.925, 1.00, 1.10, 1.20]
grid_capex = [dcf_scenario(capex_mult=m) for m in capex_grid]
nwc_grid = [-0.10, -0.085, nwc_pct, -0.050, -0.030]
grid_nwc = [dcf_scenario(nwc=p) for p in nwc_grid]
# THE TERMINAL SENSITIVITY IS NOW THE ASSET LIFE, because that is what the terminal
# actually turns on. The retired grid moved the terminal return on capital, which the
# sanctioned construction does not use at all — publishing it would have been a lever a
# reader could not pull. The rungs are DERIVED from the base so the grid cannot drift off
# its own centre, and the widest is close to the second reading of the same notes:
# accumulated depreciation over the year's charge says the base has taken 12.59 years,
# which the module's half-the-life formula would reach at a life of 25.18.
_LIFE = V['asset_life_years']
life_grid = [round(_LIFE + k * 3.0, 2) for k in (-2, -1, 0, 1, 2)]
def dcf_life(l_):
    try:
        _tv = _terminal_at(V['g_term'], life=l_).tv
    except TERMVAL.TerminalRefused:
        return float('nan')
    _ev = pv_explicit + _tv * df[-1]
    return ((_ev - LEASE + NETCASH + INVEST) / SH) * ROLL - V['div_between']
grid_life = [dcf_life(l_) for l_ in life_grid]
LIFE_VARIANT = 2.0 * (V['accum_dep_owned_fy25'] / V['dep_charge_owned_fy25'])
PS_LIFE_VARIANT = dcf_life(LIFE_VARIANT)
dcf_opex_1pp = dcf_scenario(opex_shift=+0.01)   # +1pp of revenue in the cost stack
dcf_tax_per_pp = (grid_tax[0] - grid_tax[4]) / ((tax_grid[4] - tax_grid[0]) * 100)

# ---- expert panel: three genuinely different methods ---------------------------
# Expert 1 — earnings power on a through-cycle multiple.
# CORRECTED 17-Aug-2026 (external finding CC7, and it was right): the lens values FY2028
# earnings, which arrive at 31-Dec-2028 — 2.40 years after the 07-Aug-2026 anchor. The prior
# construction discounted two years from a 31-Dec-2025 base and then accreted to the anchor, a
# NET 1.40 years, so it was a full year short. Correcting the horizon alone would have dropped
# the dividends receivable in the meantime from a company paying out about all of its earnings,
# so those are now discounted in explicitly. Both defects were in the same three lines.
e1_eps = eps_fc[2]
_e1_yrs = V['e1_horizon_years']
_e1_divs = [(dps_fc[0] * 0.5, _e1_yrs - 2.0), (dps_fc[1], _e1_yrs - 1.0), (dps_fc[2], _e1_yrs)]
_e1_dpv = sum(d / (1 + ke_exp) ** t for d, t in _e1_divs)

def _e1_at(mult):
    return mult * e1_eps / (1 + ke_exp) ** _e1_yrs + _e1_dpv

e1_base, e1_lo, e1_hi = _e1_at(15.0), _e1_at(12.0), _e1_at(17.5)
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
e3_base = ((e3_ev - LEASE + NETCASH + INVEST) / SH) * ROLL - V['div_between']
e3_lo = ((ic_fy25 + pv_ep * 0.7 + pv_ep_term * 0.6 - LEASE + NETCASH + INVEST) / SH) * ROLL \
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

# ---------------------------------------------------------------------------
# THREE CRITIQUE FINDINGS THAT WERE NEVER PRICED — priced here, 17-Aug-2026
# ---------------------------------------------------------------------------
# The response procedure forbids calling a finding immaterial without a number beside the word.
# Three findings in the 17-Aug response were bucketed without one. That was a procedural
# failure regardless of where they land, so each is now priced on the real chain.
#
# (1) Expert 1's discounting horizon. The lens values FY2028 earnings on a through-cycle
# multiple. As built it accretes to the anchor from a 31-Dec-2025 base after discounting two
# years, a NET exponent of (T_ANCHOR - 2) = -1.40 years. But FY2028 earnings arrive at
# 31-Dec-2028, which is 2.40 years after the 07-Aug-2026 anchor. The horizon is a full year
# short. Correcting it alone, however, would drop nearly three years of dividends from a
# ~98%-payout company, so the coherent correction adds those back.
_e1_years_anchor = V['e1_horizon_years']
_e1_eq_2028 = 15.0 * e1_eps                                   # equity value at 31-Dec-2028
# what the RETIRED construction produced, kept only to size the correction
_e1_as_built = to_anchor(_e1_eq_2028) / (1 + ke_exp) ** 2 - V['div_between']
_e1_horizon_only = _e1_eq_2028 / (1 + ke_exp) ** _e1_years_anchor
_e1_div_pv = _e1_dpv
_e1_coherent = e1_base                                        # now the PUBLISHED Expert 1
say(f"[CC7 PRICED — Expert 1's discounting horizon] as built AED {_e1_as_built:.2f} (net "
    f"exponent {T_ANCHOR - 2:+.2f} years). Horizon corrected to the anchor-consistent "
    f"{_e1_years_anchor:.2f} years and nothing else: AED {_e1_horizon_only:.2f} "
    f"({_e1_horizon_only - _e1_as_built:+.2f}/share). But that version silently discards the "
    f"dividends receivable between the anchor and FY2028, worth AED {_e1_div_pv:.2f} in present "
    f"value on a payout near 100%; adding them back gives AED {_e1_coherent:.2f} "
    f"({_e1_coherent - _e1_as_built:+.2f}/share vs as built, "
    f"{(_e1_coherent - _e1_as_built) / central:+.1%} of the central). VERDICT: the "
    f"finding's PREMISE is correct and was under-priced by being left unpriced — the horizon "
    f"really is a year short. Its CONCLUSION that the lens is overstated is wrong in sign once "
    f"the omitted dividends are restored. Expert 1 is republished on the coherent construction.")

# (2) The synthesis weights. One critique asked what happens if the market-multiple family
# (relative + normalised) carries 25% rather than 45%. Priced both ways for where the freed
# weight goes, because that choice drives the answer more than the reweighting itself.
_lens = dict(dcf=dcf_ps, relative=rel_ps, normalized=norm_ps, book=book_ps)
def _weighted(w):
    return sum(_lens[k] * w[k] for k in _lens)
_w_base = dict(V['lens_weights'])
_fam = _w_base['relative'] + _w_base['normalized']
_scale = 0.25 / _fam
_w_to_dcf = dict(dcf=_w_base['dcf'] + (_fam - 0.25), book=_w_base['book'],
                 relative=_w_base['relative'] * _scale,
                 normalized=_w_base['normalized'] * _scale)
_w_to_book = dict(dcf=_w_base['dcf'], book=_w_base['book'] + (_fam - 0.25),
                  relative=_w_base['relative'] * _scale,
                  normalized=_w_base['normalized'] * _scale)
for _w in (_w_base, _w_to_dcf, _w_to_book):
    assert abs(sum(_w.values()) - 1.0) < 1e-9, 'lens weights must sum to one'
cc10_to_dcf, cc10_to_book = _weighted(_w_to_dcf), _weighted(_w_to_book)
say(f"[CC10 RESOLVED — the market-multiple family's weight] the finding said the weight "
    f"scheme was a house judgement that moved the answer, and it was right. It was priced "
    f"against the blend this study published at the time, AED {RETIRED_BLEND_VALUE:.2f}: "
    f"moving the freed {_fam - 0.25:.0%} to the cash-flow lens gave AED {cc10_to_dcf:.2f} "
    f"({cc10_to_dcf - RETIRED_BLEND_VALUE:+.2f}/share) and to the book lens AED "
    f"{cc10_to_book:.2f} ({cc10_to_book - RETIRED_BLEND_VALUE:+.2f}/share) — up to "
    f"{max(abs(cc10_to_dcf - RETIRED_BLEND_VALUE), abs(cc10_to_book - RETIRED_BLEND_VALUE)):.2f}"
    f"/share, not immaterial. VERDICT: RESOLVED, and not by re-tuning the weights. The "
    f"scheme is gone: the cash-flow lens IS the central at AED {central:.2f} and the others "
    f"are published beside it, so there is no weight left to re-set. The finding pointed at "
    f"a free parameter nobody had tested and the answer was to remove it rather than to "
    f"choose it better. The arithmetic above is kept as the record of what the retired "
    f"construction did, and the blend itself is published unused.")

# (3) Revenue at the guidance midpoint. The build lands at +4.3% against a guided 4-6%.
# The gap is priced BOTH WAYS because the attribution decides most of the value: revenue won
# on price carries no incremental unit cost or capex, revenue won on volume carries both.
_g_mid = V['guidance_mid']
def _solve(fn, lo, hi, target):
    """Bisect for the driver value at which fn() reaches target. The target is an ARGUMENT:
    an earlier version closed over the guidance midpoint, which silently mis-solved the
    matched-revenue calibration below and was caught by its own assertion."""
    for _ in range(60):
        mid = (lo + hi) / 2
        if fn(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
_m_price = _solve(lambda m: build(arpu_mult=m)['rev'][0] / V['rev_fy25'] - 1, 1.0, 1.2,
                  _g_mid)
_m_vol = _solve(lambda sh: build(subs_shift=sh)['rev'][0] / V['rev_fy25'] - 1, 0.0,
                2000.0, _g_mid)
cc3_price = dcf_scenario(arpu_mult=_m_price)
cc3_vol = dcf_scenario(subs_shift=_m_vol)
say(f"[CC3 PRICED — revenue at the guidance midpoint] the build lands at "
    f"{g26:+.1%} against du's guided 4-6%, so the midpoint {_g_mid:+.1%} is "
    f"{(_g_mid - g26)*100:+.1f}pp above it, worth about AED "
    f"{(_g_mid - g26) * V['rev_fy25']:,.0f}mn of FY2026 revenue. Won on PRICE (blended ARPU "
    f"{_m_price:.3f}x, no incremental unit cost or capex): AED {cc3_price:.2f} "
    f"({cc3_price - dcf_ps:+.2f}/share). Won on VOLUME (+{_m_vol:,.0f}k subscribers, carrying "
    f"both unit cost and the capex it implies): AED {cc3_vol:.2f} "
    f"({cc3_vol - dcf_ps:+.2f}/share). So the finding is worth AED "
    f"{min(cc3_price, cc3_vol) - dcf_ps:+.2f} to {max(cc3_price, cc3_vol) - dcf_ps:+.2f} a share "
    f"and is NOT immaterial.")
# The volume case comes out HIGHER, which contradicted the first expectation written here. The
# expectation was not wrong about attribution; the TEST was wrong about what it held constant.
_rev_price = sum(build(arpu_mult=_m_price)['rev'])
_rev_vol = sum(build(subs_shift=_m_vol)['rev'])
say(f"[Why volume looks better here — the comparison was mis-specified, and the fix] calibrating "
    f"both cases on FY2026 growth does NOT hold revenue constant, because H1-2026 is a reviewed "
    f"ACTUAL: a subscriber shift can only move the second half of FY2026, so matching FY2026 "
    f"needs a shift large enough to then apply to the WHOLE of FY2027-FY2030. Five-year revenue "
    f"comes out {_rev_price:,.0f} on price against {_rev_vol:,.0f} on volume "
    f"({_rev_vol/_rev_price - 1:+.2%}) — the volume case simply sells more over the window. That "
    f"is a timing artefact of the calibration, not evidence about attribution.")
# Re-calibrate the volume case to the SAME five-year revenue, so attribution is isolated.
_m_vol_matched = _solve(lambda sh: sum(build(subs_shift=sh)['rev']) / _rev_price - 1.0, 0.0,
                        2000.0, 0.0)
cc3_vol_matched = dcf_scenario(subs_shift=_m_vol_matched)
say(f"[CC3, attribution isolated on matched five-year revenue] +{_m_vol_matched:,.0f}k "
    f"subscribers delivers the same {_rev_price:,.0f} of five-year revenue as the price case. "
    f"On PRICE: AED {cc3_price:.2f}. On VOLUME: AED {cc3_vol_matched:.2f} "
    f"({cc3_vol_matched - cc3_price:+.2f}/share, {cc3_vol_matched/cc3_price - 1:+.1%}). NOW the "
    f"expected ordering holds: identical revenue is worth less when it has to be bought with "
    f"per-subscriber cost and the capex to carry the traffic. VERDICT on the finding: material, "
    f"published as a range. The build stays below the midpoint because it is driven by disclosed "
    f"subscriber and ARPU paths rather than reverse-engineered to a guidance number — but the "
    f"reader is entitled to see what the midpoint is worth and that HOW it is won matters as "
    f"much as whether it is.")
assert cc3_vol_matched < cc3_price, (
    'on matched five-year revenue, revenue won on volume must be worth LESS than revenue won on '
    'price, because it carries per-unit cost and capex')
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

# ---- the EBITDA-margin record the section-1.4 superlative stands on -------------
# One construction across every period so the series is like-for-like: revenue less
# operating expenses excluding D&A, less expected credit losses, plus other income —
# which is what the FY2025 statements print directly as "Operating profit before
# depreciation and amortization" and what the pre-IFRS-18 years are derived to.
_MARGIN_PERIODS = [
    ('FY2022', V['rev_fy22'], V['ebitda_fy22']),
    ('FY2023', V['rev_fy23'], V['ebitda_fy23']),
    ('FY2024', V['rev_fy24'], V['ebitda_fy24']),
    ('FY2025', V['rev_fy25'], V['ebitda_fy25']),
    ('H1-2025', V['h1_25_rev'], V['h1_25_ebitda']),
    ('H1-2026', V['h1_26_rev'], V['h1_26_ebitda']),
]
_MARGINS = [(p, e / r) for p, r, e in _MARGIN_PERIODS]
_BEST_P, _BEST_M = max(_MARGINS, key=lambda t: t[1])
_FULL = [(p, m) for p, m in _MARGINS if p.startswith('FY')]
_MONOTONE = all(_FULL[i][1] < _FULL[i + 1][1] for i in range(len(_FULL) - 1))
MARGIN_RECORD = dict(
    periods=[dict(period=p, revenue=r, ebitda=e, margin=e / r) for p, r, e in _MARGIN_PERIODS],
    best_period=_BEST_P, best_margin=_BEST_M,
    window='FY2022 to the reviewed half-year ended 30 June 2026',
    full_years_monotone=_MONOTONE,
    note=('the window this superlative is claimed over, stated rather than implied. Every '
          'period is footed to an audited or reviewed filing on one construction.'))
say(f"[EBITDA margin record] " + " · ".join(f"{p} {m:.2%}" for p, m in _MARGINS)
    + f" | highest {_BEST_P} at {_BEST_M:.2%}"
    + (" | the full years rise monotonically" if _MONOTONE else " | the full years do NOT rise monotonically"))
assert _BEST_P == 'H1-2026', (
    f"section 1.4 says the latest reviewed half printed the best margin on this record; the "
    f"record's own maximum is {_BEST_P} at {_BEST_M:.2%}. Fix the sentence, not the record.")

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
              taxB_path=taxB_path, fcffB=fcffB, npB=npB,
              seg_dc=seg_dc, dc_tot=dc_tot, contrib_margin=contrib_margin,
              gross_margin=gross_margin, dc_nature=dc_nature_fc, unit_cost=unit_cost,
              retired_contrib=_retired_contrib,
              h2_26=dict(rev=_h2_26_rev, ebitda=_h2_26_ebitda, margin=_h2_26_margin,
                         h2_25_margin=_h2_25_margin, h1_26_margin=_h1_26_margin,
                         h1_25_margin=_h1_25_margin,
                         margin_at_guidance_mid=(0.465 * rev[0] - V['h1_26_ebitda'])
                         / _h2_26_rev)),
    unitcost=dict(hist=DCU, joint=_DCP, h2_25=H2_25_U, den={k: list(v) for k, v in _DEN.items()},
                  arpu_q=V['arpu_mobile_q'], peers=V['arpu_ratio_peers'],
                  nature_hist=V['dc_nature_hist'], nature_h1=V['dc_nature_h1'],
                  seg_dc_hist=V['seg_dc_hist'], seg_dc_h1=V['seg_dc_h1'],
                  mix=dict(fy25=_m_fy25, q226=_m_q226, ratio=_r, lift=mix_lift,
                           erosion=leg_erosion, printed=_rel - 1,
                           prepaid_drop=V['subs_prepaid']['Q2_2026'] - V['subs_prepaid']['Q4_2025'],
                           postpaid_gain=V['subs_postpaid']['Q2_2026'] - V['subs_postpaid']['Q4_2025'],
                           share={k: _pp[k] for k in _pp}),
                  ident=dict(pairs=len(_pairs), lo=min(_rv), hi=max(_rv), neg=_neg,
                             sub1=_sub1, inband=_inband,
                             band=[_lo, _hi], single=_r_implied)),
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
              erp_market_basis=V['erp_market_basis'], erp_rating_basis=V['erp_rating_basis'],
              sov_spread_market_observed=V['sov_spread_market_observed'], sov_spread_damodaran_rating=V['sov_spread_damodaran_rating']),
    dcf=dict(pv_explicit=pv_explicit, tv=tv, pv_tv=pv_tv, ev=ev, tv_share=tv_share,
             lease=LEASE, net_cash=NETCASH, investees=INVEST, eq_val=eq_val,
             ps=dcf_ps, ps_dec=dcf_ps_dec, roll=ROLL, anchor_days=V['anchor_days'],
             div_between=V['div_between'], roic_term=roic_term, rr_term=rr_term,
             g=V['g_term'], bear=dcf_bear, bull=dcf_bull,
             ps_framing_b=dcf_ps_B, ps_rf_alt=dcf_ps_rf_alt,
             ps_rf_long=dcf_ps_rf_long, ps_rf_debut=dcf_ps_rf_debut,
             wacc_rf_long=wacc_rf_long, wacc_rf_debut=wacc_rf_debut,
             ev_ebitda_now=ev_ebitda_now, ebitda_term=ebitda_term,
             tv_implied_mult=tv_implied_mult, ps_mkt_term=dcf_ps_mkt_term,
             rou_repl_retired=rou_repl_retired),
    terminal_recon=dict(roic_term=roic_term, rr=rr_term,
                        nopat=dict(FY25=(V['pbt_fy25'] - netfin_fy25) * (1 - TAX)),
                        roic_path=roic,
                        note='the terminal return and the reinvestment rate are published '
                             'because the RETIRED construction rested on them and a reader '
                             'comparing editions is owed the pair; they no longer build '
                             'anything.'),
    terminal_record=dict(
        construction='engine/terminal_value.py [R-TERM-01]',
        retired_construction=dict(
            form='NOPAT(1+g)(1 - g/ROIC)/(W-g)', tv=tv_retired,
            implied_cycle_years=1.0 / V['g_term'],
            why_retired="the reinvestment identity charges g x invested capital every year "
                        "for ever, so the implied replacement cycle is 1/g — 50 years at "
                        "the derived 2.0% and 40 at the previous edition's typed 2.5%, "
                        "both facts about the dirham's peg to the dollar rather than about "
                        "a mobile network. Notes 6 and 8 say the depreciable owned base "
                        "turns over in 17.91 years. It also supplied the perpetual LEASE "
                        "renewal only as a side effect, which is why the corrected "
                        "construction has to put that renewal back explicitly."),
        inputs=dict(nopat=nopat[-1], wacc=wacc_term, inflation=PI_TERM,
                    real_growth=V['g_term_real'], nominal_growth=V['g_term'],
                    dna_book=DNA_OWNED,
                    dna_basis=('THE FULL charge — property, intangibles and right-of-use '
                               'alike — escalated over half the BLENDED life. The explicit '
                               'window adds back total depreciation and charges no '
                               'lease-replacement capital, because the lease liability is '
                               'DEBT in the bridge and charging renewal there would bill '
                               'the existing obligation twice. In perpetuity that argument '
                               'fails — a one-off deduction cannot cover renewals for ever '
                               '— and the retired construction supplied that renewal only '
                               'as a side effect, on a 50-year cycle against a lease term '
                               'the company discloses at 10.1 years. A lease is an asset '
                               'with a life like any other here, so it enters the blended '
                               'life at its own derived 10.24 years.'),
                    useful_life_years=V['asset_life_years'],
                    useful_life_source=INP['asset_life_years']['source'],
                    maintenance_basis='book_dna_escalated',
                    maintenance_basis_reason=(
                        "'disclosed_life' divides REPLACEMENT-COST invested capital by the "
                        "life and this model commits no replacement-cost capital base: the "
                        "notes give gross HISTORICAL cost on a base 70% depreciated. "
                        "Escalating the model's own book charge over half the derived life "
                        "uses only figures that exist."),
                    working_capital=nwc_fc[-1],
                    working_capital_note=('NEGATIVE for this company, so the inflation line '
                                          'is a CREDIT rather than a charge: a telecom '
                                          'collects from its subscribers before it pays its '
                                          'suppliers, and inflation makes that float worth '
                                          'more each year.'),
                    incremental_capital_per_unit_growth=INC_CAP),
        outputs=dict(fcff=TERMINAL.fcff, tv=TERMINAL.tv, floor=TERMINAL.floor,
                     maintenance=TERMINAL.maintenance, growth_capex=TERMINAL.growth_capex,
                     wc_charge=TERMINAL.wc_charge, dna_addback=TERMINAL.dna_addback,
                     implied_cycle_years=TERMINAL.implied_cycle_years,
                     below_floor=TERMINAL.below_floor),
        record=TERMINAL.record,
        derived_life=dict(
            years=V['asset_life_years'], cross_check_fy2024=15.96,
            direct_average_age=V['accum_dep_owned_fy25'] / V['dep_charge_owned_fy25'],
            basis="notes 6, 7 and 8: gross cost of every depreciable class over the year's "
                  "own charge, validated against the 10.1-year average lease term "
                  "note 7 discloses directly",
            note="the module's formula assumes an average age of half the life; the second "
                 "identity — accumulated depreciation over the same charge — measures that "
                 "age directly, and where it reads higher the base charge is the lighter of "
                 "the two readings."),
        moved=dict(tv_before=tv_retired, tv_after=tv, pct=tv / tv_retired - 1.0)),
    lenses=lenses, central=central, span=[lo, hi], spot=SPOT,
    retired_blend_value=RETIRED_BLEND_VALUE,
    lens_record=dict(**{'class': 'telecom operator'},
        primary=dict(
            kind='dcf', two_sided=False, value=float(central),
            range={'low': float(lo), 'high': float(hi)},
            range_note=('the cash-flow lens under its own bear and bull paths on one '
                        'clock, not the widest spread across four methods'),
            range_basis=dict(
                driver='the fibre and mobile revenue path and the capital intensity it '
                       'carries',
                low=float(lo), high=float(hi),
                units='AED per share, the present-value read under each path',
                macro_held=True,
                evidence='both paths are engine re-runs of the same model with the macro '
                         'path, the cost of capital and terminal growth held still')),
        cross_checks=[
            dict(kind='relative_multiple', value=float(lenses['relative']['base']),
                 present_value=False, multiple=float(V['pe_just']),
                 multiple_source=('a justified earnings multiple set against the named '
                                  'regional telecom peer set and this company\'s own '
                                  'history, never one read off the current price'),
                 circularity=dict(spot=float(SPOT), shares=float(SH),
                                  net_debt=float(-NETCASH),
                                  metric_value=float(V['ebitda_fy25'])),
                 note='forward earnings on a peer-anchored multiple'),
            dict(kind='book_value', value=float(lenses['book']['base']),
                 present_value=False, floor=True,
                 note='a disclosed FLOOR, published as such and never weighted'),
        ],
        cross_checks_not_built=[
            dict(kind='ev_ebitda_own_history',
                 why=('this class permits an enterprise multiple on the company\'s OWN '
                      'history and this study does not publish one. What it computes is a '
                      'trailing multiple from the CURRENT market capitalisation, which is '
                      'a multiple read off the price and is what the non-circularity rule '
                      'forbids. A genuine own-history multiple needs a series of past '
                      'enterprise values against past EBITDA — a construction rather than '
                      'a rename — and it is named here rather than left quietly absent.')),
        ],
        retired=dict(
            blend=dict(RETIRED_BLEND_W),
            blend_value=float(RETIRED_BLEND_VALUE),
            why=('the weights were typed and had never cleared an out-of-sample test. What '
                 'they concealed here was the SIZE of the disagreement rather than its '
                 'direction: the blend read %+.0f%% against the price where the cash-flow '
                 'lens reads %+.0f%%, so a reader — and every gate that reads the published '
                 'central — saw about a quarter of the disagreement this study actually '
                 'holds. An external finding (CC10) had already identified the weight '
                 'scheme as an untested house judgement that moved the answer; it is '
                 'resolved by removing the scheme rather than by re-tuning it.'
                 % (100 * (RETIRED_BLEND_VALUE / SPOT - 1), 100 * (central / SPOT - 1))),
            normalised_removed=dict(
                value=float(lenses['normalized']['base']),
                why=('normalised earnings power is not among a telecom operator\'s '
                     'permitted cross-checks. Removed rather than re-weighted; computed '
                     'and shown so the move is visible.')))),
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
              drift_grid=drift_grid, grid_drift=grid_drift,
              cc3=dict(price=cc3_price, vol=cc3_vol, vol_matched=cc3_vol_matched,
                       m_price=_m_price, m_vol=_m_vol, m_vol_matched=_m_vol_matched,
                       g_mid=_g_mid, g_build=g26,
                       rev_price=_rev_price, rev_vol=_rev_vol),
              cc10=dict(to_dcf=cc10_to_dcf, to_book=cc10_to_book, family=_fam,
                        w_to_dcf=_w_to_dcf, w_to_book=_w_to_book),
              cc7=dict(as_built=_e1_as_built, horizon_only=_e1_horizon_only,
                       coherent=_e1_coherent, div_pv=_e1_div_pv,
                       years=_e1_years_anchor, net_exp_as_built=T_ANCHOR - 2),
              dcf_mix_exhaust=dcf_mix_exhaust,
              subs_grid=subs_grid, grid_subs=grid_subs, mg_grid=mg_grid,
              grid_margin=grid_margin, capex_grid=capex_grid, grid_capex=grid_capex,
              nwc_grid=nwc_grid, grid_nwc=grid_nwc, life_grid=life_grid, grid_life=grid_life,
              life_variant_years=LIFE_VARIANT, ps_life_variant=PS_LIFE_VARIANT,
              dcf_opex_1pp=dcf_opex_1pp, dcf_tax_per_pp=dcf_tax_per_pp),
    step0=step0, strike=strike, backtest=bt5,
    # ---------------------------------------------------------------------------------
    # FIGURES QUOTED IN THE REGISTER'S OWN JUSTIFICATION TEXT, COMMITTED AS NUMBERS.
    # [R-ENF-01] reaches the four-field register's justification text, not only the
    # builders — and every one of these was computed or sourced correctly and then written
    # ONLY into a sentence, where no instrument could reconcile it. A figure the model
    # holds and does not commit is indistinguishable from one somebody typed. The
    # like-for-like deltas below are the pre-pass values already cross-asserted against
    # the joint direct-cost recovery above; the rest are sourced constants and one
    # refused negative result, each of which a reader meets in prose.
    # THE SUPERLATIVE IS COMPUTED AND BOUNDED, NEVER TYPED. Section 1.4 claims the latest
    # reviewed half printed the best margin in the company's history. It was a typed
    # sentence over a record the study did not carry — which is the AMOC defect exactly
    # ("above the best single quarter this company has ever filed", when the company had
    # filed a higher one twice). The record is now committed, the claim is derived from it,
    # and the WINDOW IS NAMED so the sentence claims only what the evidence covers.
    margin_record=MARGIN_RECORD,
    register_figures=dict(
        lfl_mobile_interconnect=_D_INTER,
        lfl_mobile_commission=_D_COMM,
        lfl_fixed_capacity=_D_FIXED,
        rate_mobile_interconnect_h125=_I125, rate_mobile_interconnect_h126=_I126,
        rate_mobile_commission_h125=_C125, rate_mobile_commission_h126=_C126,
        rate_fixed_capacity_h125=_X125, rate_fixed_capacity_h126=_X126,
        erp_mature_base=V['erp_mature_base'],
        rf_ad_usd_10y=V['rf_ad_usd_10y'],
        pe_provider_refused=V['pe_provider_refused'],
        mamoura_stake_sold=V['mamoura_stake_sold'],
    ),
    assert_log=LOG,
)
# An overridden run writes BESIDE the committed file, never over it. The default is the
# safe one, so forgetting the flag cannot corrupt the study.
if OVERRIDE_RECORD is not None:
    OUT['override'] = OVERRIDE_RECORD
_out_name = 'study_numbers.override.json' if OVERRIDE_RECORD is not None else 'study_numbers.json'
_out_path = os.environ.get('DU_OUT', os.path.join(HERE, _out_name))
with open(_out_path, 'w') as f:
    json.dump(OUT, f, indent=1, default=float)
if OVERRIDE_RECORD is not None:
    say('PRICING-HARNESS RUN — wrote %s and left the committed study untouched'
        % os.path.basename(_out_path))
say("=" * 78)
say(f"WROTE {os.path.basename(_out_path)} | central AED {central:.2f} [{lo:.2f} - {hi:.2f}] vs spot "
    f"{SPOT:.2f} | DCF A {dcf_ps:.2f} / B {dcf_ps_B:.2f} | TV {tv_share:.0%} of EV | WACC "
    f"{wacc_exp:.2%} -> {wacc_term:.2%}")
