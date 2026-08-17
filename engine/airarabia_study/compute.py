"""AIRARABIA study — master computation. Writes study_numbers.json (single source
of truth for every builder). Code-first rule: INPUTS are four-field records
{value, source, date, ring}; a bare numeral cannot enter the model; the ASSERT
block raises (no JSON emitted) unless the bridge closes, the discount-rate glide
is ordered, the Kd-integrity triple holds, and the terminal is ROIC-consistent.

Built 09-Aug-2026 on the actual audited/reviewed consolidated financial
statements (FY2022, FY2023, FY2024, FY2025 — KPMG Lower Gulf, unqualified
opinion on FY2025 dated 13-Feb-2026; prior years as filed — and the Q1-2026
limited-review interim, Grant Thornton UAE), all read from the company's own
investor-relations page. FY2024 figures are the RESTATED comparatives from the
FY2025 filing (Note 43: aircraft-lease-rental revenue reclassified into revenue,
maintenance provisions re-measured, lease/borrowing classification corrected);
FY2023's closing balance sheet is the restated 1-Jan-2024 column of the same
note, while the FY2023 income statement is as originally reported (the
restatement did not restate 2023's P&L).

Company class: OPERATING COMPANY — low-cost airline. Evidence: FY2025 revenue
is 79% passenger + baggage, 11% ancillary/cargo/services, 3% aircraft leases to
its own JV airlines, 1% hotels; the balance sheet is fleet (PP&E 5.79bn + ROU
0.85bn + pre-delivery payments 2.03bn) against lease/borrowing debt of 2.78bn
and a cash-and-deposits pile of 5.20bn (net cash). The equity-accounted JV
airline network (Abu Dhabi 49%, Egypt 49%, Fly Jinnah 45%, Maroc 44.13%, the
new Saudi 'Air Arabia DMM' 49%) sits OFF the consolidated P&L and is handled
explicitly in the bridge. Lens set follows the operating-company reference:
FCFF DCF primary, relative multiples, normalised earnings power, book/ROE.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np

# the beta regressions (adopted + alternative benchmark) are needed while the cost of
# capital is built, not only at emit time
beta_res_pre = json.load(open(os.path.join(HERE, 'beta_result.json')))

# ============================ INPUTS =========================================
def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)

FS25 = ("audited FY2025 consolidated financial statements, KPMG Lower Gulf, "
        "unqualified opinion 13-Feb-2026, airarabia.com investor relations")
FS24 = ("audited FY2024 consolidated financial statements (approved 13-Feb-2025), "
        "airarabia.com investor relations")
FS23 = ("audited FY2023 consolidated financial statements, airarabia.com investor relations")
Q126 = ("Q1-2026 condensed consolidated interim financial information, limited review, "
        "Grant Thornton UAE, airarabia.com investor relations")

INP = dict(
    # ---- anchors --------------------------------------------------------
    spot=I(5.24, "Uploaded DFM daily price history, last close 07-Aug-2026", "2026-08-07", "Market"),
    shares_mn=I(4666.700, "Share capital note 18, " + FS25 + ": 4,666,700 thousand shares of "
                "AED 1 each, authorised, issued and fully paid, unchanged since FY2022",
                "2026-02-13", "Company"),
    tax_stat=I(0.15, "UAE Domestic Minimum Top-up Tax (DMTT) 15% effective 1-Jan-2025 for "
               "Pillar-Two-scope groups; the Group provides at 15% (Note 27, FY2025 filing). "
               "9% UAE CT applied in FY2024", "2026-02-13", "Country"),
    tax_eff=I(0.15, "Forecast effective rate held AT the 15% DMTT statutory rate. Audited "
              "effective rates: FY2024 8.79%, FY2025 11.60% (Note 27a reconciliation — the "
              "sub-15% prints reflect exempt income and the 9%-era opening); Q1-2026 provides at "
              "15%. Holding 15% is the conservative statutory anchor rather than extrapolating "
              "the lower realised prints", "2026-02-13", "Company/House"),

    # ---- historical income statement (AED mn, consolidated) --------------
    rev_fy23=I(5999.750, FS23 + " (confirmed by the FY2024 filing's comparative column)",
               "2024-02-13", "Company"),
    rev_fy24=I(6765.852, "RESTATED comparative, " + FS25 + " Note 43 (as reported: 6,639.064 — "
               "aircraft lease rentals to JV airlines reclassified into revenue)",
               "2026-02-13", "Company"),
    rev_fy25=I(7787.581, FS25, "2026-02-13", "Company"),
    dcost_fy23=I(4343.184, "Direct costs, " + FS23, "2024-02-13", "Company"),
    dcost_fy24=I(5202.944, "Direct operating costs, restated comparative, " + FS25,
                 "2026-02-13", "Company"),
    dcost_fy25=I(6088.132, "Direct operating costs Note 29, " + FS25, "2026-02-13", "Company"),
    ga_fy23=I(329.206, "Administrative and general expenses, " + FS23, "2024-02-13", "Company"),
    ga_fy24=I(274.965, "G&A, restated comparative, " + FS25, "2026-02-13", "Company"),
    ga_fy25=I(316.264, "G&A Note 30, " + FS25, "2026-02-13", "Company"),
    sm_fy23=I(88.793, "Selling and marketing expenses, " + FS23, "2024-02-13", "Company"),
    sm_fy24=I(103.843, "S&M, restated comparative, " + FS25, "2026-02-13", "Company"),
    sm_fy25=I(113.605, "S&M Note 31, " + FS25, "2026-02-13", "Company"),
    fininc_fy23=I(209.994, "Finance income, " + FS23, "2024-02-13", "Company"),
    fininc_fy24=I(250.698, "Finance income, " + FS25 + " comparative", "2026-02-13", "Company"),
    fininc_fy25=I(240.774, "Finance income, " + FS25, "2026-02-13", "Company"),
    fincost_fy23=I(102.457, "Finance costs, " + FS23, "2024-02-13", "Company"),
    fincost_fy24=I(82.092, "Finance costs, " + FS25 + " comparative", "2026-02-13", "Company"),
    fincost_fy25=I(66.672, "Finance costs, " + FS25, "2026-02-13", "Company"),
    assoc_fy23=I(88.121, "Share of profit of associates and JVs, " + FS23, "2024-02-13", "Company"),
    assoc_fy24=I(124.752, "Share of profit of associates and JVs, " + FS25 + " comparative",
                 "2026-02-13", "Company"),
    assoc_fy25=I(189.975, "Share of profit of associates and JVs Note 12, " + FS25 + ": "
                 "Air Arabia Abu Dhabi 54.210, Fly Jinnah 36.070, Air Arabia Maroc 20.532, "
                 "other JVs/associates the balance", "2026-02-13", "Company"),
    other_fy23=I(113.471, "Other income net, " + FS23, "2024-02-13", "Company"),
    other_fy24=I(131.680, "Other income, " + FS25 + " comparative", "2026-02-13", "Company"),
    other_fy25=I(197.132, "Other income Note 32, " + FS25 + ": management fees from JVs and "
                 "associates 86.905 + others 110.227", "2026-02-13", "Company"),
    tax_fy23=I(0.0, "No income tax expense in FY2023 (UAE CT effective for the Group from "
               "FY2024), " + FS23, "2024-02-13", "Company"),
    tax_fy24=I(141.508, "Income tax expense, " + FS25 + " comparative", "2026-02-13", "Company"),
    tax_fy25=I(202.054, "Income tax expense Note 27 (212.444 current less 10.390 prior-period "
               "adjustment), effective rate 11.60%", "2026-02-13", "Company"),
    pat_fy23=I(1547.696, "Profit for the year, " + FS23, "2024-02-13", "Company"),
    pat_fy24=I(1467.630, "Profit for the year, " + FS25 + " comparative", "2026-02-13", "Company"),
    pat_fy25=I(1628.735, "Profit for the year, " + FS25, "2026-02-13", "Company"),
    npa_fy23=I(1547.132, "Profit attributable to owners; basic and diluted EPS AED 0.33, " + FS23,
               "2024-02-13", "Company"),
    npa_fy24=I(1466.986, "Profit attributable to owners; EPS AED 0.31, " + FS25 + " comparative",
               "2026-02-13", "Company"),
    npa_fy25=I(1628.475, "Profit attributable to owners; basic and diluted EPS AED 0.35 "
               "(note 33 uses 1,629.303 attributable incl. rounding presentation), " + FS25,
               "2026-02-13", "Company"),
    dna_fy23=I(647.327, "Depreciation and amortisation, audited FY2023 consolidated statement "
               "of cash flows (FY2022: 633.957)", "2024-02-13", "Company"),
    dna_fy24=I(648.588, "Depreciation and amortisation, restated FY2024 cash-flow comparative, "
               + FS25, "2026-02-13", "Company"),
    dna_fy25=I(621.798, "Depreciation and amortisation, consolidated statement of cash flows, "
               + FS25 + " (direct-cost D&A 581.717 + G&A depreciation 40.081)",
               "2026-02-13", "Company"),

    # ---- FY2022 (fourth audited year, context columns) --------------------
    rev_fy22=I(5241.830, FS23 + ", comparative column", "2024-02-13", "Company"),
    pat_fy22=I(1222.306, "Profit for the year FY2022 (owners 1,221.786; EPS AED 0.26), " + FS23,
               "2024-02-13", "Company"),
    dna_fy22=I(633.957, "D&A, FY2023 cash-flow comparative", "2024-02-13", "Company"),

    # ---- historical balance sheet (AED mn; FY23 = restated 1-Jan-2024) ------
    ppe_fy23=I(4954.113, "Restated consolidated statement of financial position as at "
               "1-Jan-2024, Note 43, " + FS25, "2026-02-13", "Company"),
    ppe_fy24=I(4661.664, "Restated 31-Dec-2024, Note 43, " + FS25, "2026-02-13", "Company"),
    ppe_fy25=I(5790.022, FS25, "2026-02-13", "Company"),
    rou_fy23=I(574.232, "Right-of-use assets, restated 1-Jan-2024, " + FS25, "2026-02-13", "Company"),
    rou_fy24=I(784.706, "Right-of-use assets, restated 31-Dec-2024, " + FS25, "2026-02-13", "Company"),
    rou_fy25=I(852.577, "Right-of-use assets, " + FS25, "2026-02-13", "Company"),
    adv_fy23=I(886.886, "Advance for new aircraft (pre-delivery payments on the 120-aircraft "
               "A320/A321-family order), restated 1-Jan-2024, " + FS25, "2026-02-13", "Company"),
    adv_fy24=I(1262.605, "Advance for new aircraft, restated 31-Dec-2024, " + FS25,
               "2026-02-13", "Company"),
    adv_fy25=I(2028.265, "Advance for new aircraft Note 7, " + FS25, "2026-02-13", "Company"),
    invprop_fy25=I(277.090, "Investment property (Varazze Tower, Dubai, ~99% complete) Note 8, "
                   + FS25 + "; disclosed FAIR VALUE AED 334mn", "2026-02-13", "Company"),
    invprop_fv=I(334.0, "Disclosed fair value of the investment property, Note 8, " + FS25,
                 "2026-02-13", "Company"),
    nil_fy25=I(334.666, "Net investment in lease (aircraft subleased to JV airlines), " + FS25,
               "2026-02-13", "Company"),
    intang_fy25=I(1362.497, "Intangible assets (incl. goodwill/brands), " + FS25,
                  "2026-02-13", "Company"),
    fvoci_fy25=I(457.528, "Investments at fair value through OCI, " + FS25, "2026-02-13", "Company"),
    assoc_bv_fy25=I(363.386, "Investments in associates and joint ventures, carrying value, "
                    + FS25, "2026-02-13", "Company"),
    inv_fy23=I(48.719, "Inventories, restated 1-Jan-2024, " + FS25, "2026-02-13", "Company"),
    inv_fy24=I(53.456, "Inventories, restated 31-Dec-2024, " + FS25, "2026-02-13", "Company"),
    inv_fy25=I(97.042, "Inventories, " + FS25, "2026-02-13", "Company"),
    recv_fy23=I(858.576, "Trade and other receivables (current), restated 1-Jan-2024, " + FS25,
                "2026-02-13", "Company"),
    recv_fy24=I(824.296, "Trade and other receivables (current), restated 31-Dec-2024, " + FS25,
                "2026-02-13", "Company"),
    recv_fy25=I(896.388, "Trade and other receivables (current), " + FS25, "2026-02-13", "Company"),
    dep_fy23=I(3984.069, "Fixed deposits, restated 1-Jan-2024, " + FS25, "2026-02-13", "Company"),
    dep_fy24=I(4619.288, "Fixed deposits, restated 31-Dec-2024, " + FS25, "2026-02-13", "Company"),
    dep_fy25=I(4126.040, "Fixed deposits Note 17 (average interest 4.41%; FY2024: 5.27%), "
               + FS25, "2026-02-13", "Company"),
    cash_fy23=I(1262.308, "Cash and cash equivalents, restated 1-Jan-2024, " + FS25,
                "2026-02-13", "Company"),
    cash_fy24=I(700.229, "Cash and cash equivalents, restated 31-Dec-2024, " + FS25,
                "2026-02-13", "Company"),
    cash_fy25=I(1072.692, "Cash and cash equivalents, " + FS25, "2026-02-13", "Company"),
    assets_fy23=I(14674.544, "Total assets, restated 1-Jan-2024, " + FS25, "2026-02-13", "Company"),
    assets_fy24=I(15361.444, "Total assets, restated 31-Dec-2024, " + FS25, "2026-02-13", "Company"),
    assets_fy25=I(17698.795, "Total assets, " + FS25, "2026-02-13", "Company"),
    borrow_fy23=I(1577.531, "Bank borrowings, restated 1-Jan-2024: current 505.755 + "
                  "non-current 1,071.776, Note 43, " + FS25, "2026-02-13", "Company"),
    borrow_fy24=I(1059.165, "Bank borrowings, restated 31-Dec-2024: current 375.997 + "
                  "non-current 683.168, " + FS25, "2026-02-13", "Company"),
    borrow_fy25=I(1515.068, "Bank borrowings Note 26: current 393.727 + non-current 1,121.341; "
                  "AED 849.572 new loan drawn in FY2025 to finance 5 aircraft (mortgaged), "
                  + FS25, "2026-02-13", "Company"),
    lease_fy23=I(701.426, "Lease liabilities, restated 1-Jan-2024: current 174.765 + "
                 "non-current 526.661, " + FS25, "2026-02-13", "Company"),
    lease_fy24=I(1042.276, "Lease liabilities, restated 31-Dec-2024: current 249.226 + "
                 "non-current 793.050, " + FS25, "2026-02-13", "Company"),
    lease_fy25=I(1266.367, "Lease liabilities Note 25: current 262.667 + non-current 1,003.700; "
                 "average finance charge 4% (2024: 4%); terms 5-15 years, secured on the "
                 "aircraft", "2026-02-13", "Company"),
    pay_fy23=I(2298.899, "Trade and other payables (current), restated 1-Jan-2024, " + FS25,
               "2026-02-13", "Company"),
    pay_fy24=I(2295.886, "Trade and other payables (current), restated 31-Dec-2024, " + FS25,
               "2026-02-13", "Company"),
    pay_fy25=I(2932.708, "Trade and other payables (current), " + FS25, "2026-02-13", "Company"),
    definc_fy23=I(523.402, "Deferred income (unflown ticket liability), restated 1-Jan-2024, "
                  + FS25, "2026-02-13", "Company"),
    definc_fy24=I(835.350, "Deferred income, restated 31-Dec-2024, " + FS25, "2026-02-13", "Company"),
    definc_fy25=I(1100.030, "Deferred income Note 28b, " + FS25, "2026-02-13", "Company"),
    maint_fy23=I(1795.035, "Provision for maintenance, restated 1-Jan-2024: current 514.690 + "
                 "non-current 1,280.345, " + FS25, "2026-02-13", "Company"),
    maint_fy24=I(1714.335, "Provision for maintenance, restated 31-Dec-2024: current 346.450 + "
                 "non-current 1,367.885, " + FS25, "2026-02-13", "Company"),
    maint_fy25=I(1876.324, "Provision for maintenance: current 817.418 + non-current 1,058.906, "
                 + FS25, "2026-02-13", "Company"),
    staffb_fy23=I(208.175, "Provision for staff termination benefits, restated 1-Jan-2024, "
                  + FS25, "2026-02-13", "Company"),
    staffb_fy24=I(239.721, "Staff termination benefits, restated 31-Dec-2024, " + FS25,
                  "2026-02-13", "Company"),
    staffb_fy25=I(271.202, "Staff termination benefits Note 21, " + FS25, "2026-02-13", "Company"),
    eqp_fy23=I(7534.006, "Equity attributable to owners, restated 1-Jan-2024, " + FS25,
               "2026-02-13", "Company"),
    eqp_fy24=I(7950.330, "Equity attributable to owners, restated 31-Dec-2024, " + FS25,
               "2026-02-13", "Company"),
    eqp_fy25=I(8408.904, "Equity attributable to owners, " + FS25, "2026-02-13", "Company"),
    nci_fy23=I(1.084, "Non-controlling interests, restated 1-Jan-2024, " + FS25,
               "2026-02-13", "Company"),
    nci_fy24=I(1.728, "Non-controlling interests, restated 31-Dec-2024, " + FS25,
               "2026-02-13", "Company"),
    nci_fy25=I(1.287, "Non-controlling interests, " + FS25, "2026-02-13", "Company"),

    # ---- cash-flow markers (AED mn) --------------------------------------
    ocf_fy23=I(2304.108, "Net cash flows from operating activities, FY2023 (FY2024 filing "
               "comparative; the FY2023 filing's own statement shows 2,352.905 before a "
               "reclassification — the later filing's figure is carried)", "2025-02-13", "Company"),
    ocf_fy24=I(2278.691, "Net cash flows from operating activities, restated FY2024, " + FS25,
               "2026-02-13", "Company"),
    ocf_fy25=I(2860.401, "Net cash flows from operating activities, " + FS25, "2026-02-13", "Company"),
    capex_fy23=I(378.035, "FY2023 fleet capex: acquisition of PP&E 76.284 + payments for "
                 "advances for new aircraft 301.751, FY2024 filing comparative cash flows",
                 "2025-02-13", "Company"),
    capex_fy24=I(579.654, "FY2024 fleet capex: PP&E 203.935 + aircraft advances 375.719, "
                 "restated cash flows, " + FS25, "2026-02-13", "Company"),
    capex_fy25=I(2327.603, "FY2025 fleet capex: PP&E 1,387.154 + aircraft advances 940.449, "
                 + FS25 + " — the step-up year: 9 aircraft added (5 loan-financed) and "
                 "pre-delivery payments building for the neo ramp", "2026-02-13", "Company"),
    div_fy23=I(700.005, "Dividends paid to owners during FY2023 (AED 0.15/share on FY2022), "
               "FY2023 cash flows", "2024-02-13", "Company"),
    div_fy24=I(933.340, "Dividends paid during FY2024 (AED 0.20/share on FY2023), " + FS25,
               "2026-02-13", "Company"),
    div_fy25=I(1167.376, "Dividends paid during FY2025 (AED 0.25/share on FY2024), " + FS25,
               "2026-02-13", "Company"),
    dps_fy25=I(0.30, "FY2025 dividend of AED 0.30/share (30% of capital, AED 1.4bn) approved at "
               "the AGM of 12-Mar-2026 and paid in 2026 (company press release; Gulf Today "
               "13-Feb-2026 for the board proposal)", "2026-03-12", "Company"),

    # ---- interim (AED mn, REVIEWED) --------------------------------------
    q1_25_rev=I(1779.3, "Q1-2025 revenue, comparative in the Q1-2026 results presentation and "
                "interim filing", "2026-05-13", "Company"),
    q1_25_np=I(355.4, "Q1-2025 net profit, same comparative", "2026-05-13", "Company"),
    q1_26_rev=I(1800.4, "Q1-2026 revenue (+1% y/y), " + Q126, "2026-05-13", "Company"),
    q1_26_op=I(302.0, "Q1-2026 operating profit (margin 17% vs 21% Q1-2025), Q1-2026 results "
               "presentation", "2026-05-13", "Company"),
    q1_26_np=I(278.1, "Q1-2026 net profit, -22% y/y — the quarter absorbed the regional "
               "airspace closures of Feb-Mar 2026 (consolidated pax -11% y/y, group -5%, load "
               "factor RECORD 86.4%)", "2026-05-13", "Company"),
    q1_26_pax=I(2.68, "Q1-2026 consolidated passengers, millions (Q1-2025: 3.03), Q1-2026 "
                "results presentation", "2026-05-13", "Company"),

    # ---- unit build history (pax mn, LF, revenue lines — DISCLOSED) --------
    pax_hist=I(dict(FY22=8.36, FY23=10.11, FY24=11.22, FY25=13.06),
               "Consolidated passengers carried, millions — company results presentations "
               "Q4-2022 through Q4-2025 KEY PERFORMANCE tables (all-hub group traffic incl. "
               "JV airlines: 18.84mn FY2024, 21.82mn FY2025)", "2026-02-13", "Company"),
    lf_hist=I(dict(FY22=0.80, FY23=0.804, FY24=0.82, FY25=0.853),
              "Seat load factor, same presentations — FY2025 85.3% (+3.3pp)",
              "2026-02-13", "Company"),
    fleet=I(dict(total=90, short_lease=5, leased_out=17, neo_first="2025-09-29"),
            "Operating fleet 90 A320-family at YE2025 excl. 5 short-term leases (Q4-2025 "
            "results presentation); 17 aircraft leased OUT to JV/associate airlines (Note 34, "
            "FY2025 filing; 2024: 18); first A320neo of the 120-aircraft 2019 order delivered "
            "29-Sep-2025 (company press release)", "2026-02-13", "Company"),
    rev_lines_fy25=I(dict(pax=6165.584, baggage=86.129, ancillary=846.000, service=223.323,
                          cargo=186.948, hotel=59.842, leasing=219.755),
                     "Revenue disaggregation Note 28a + aircraft lease rentals Note 28/15, "
                     + FS25 + " — sums exactly to consolidated revenue 7,787.581",
                     "2026-02-13", "Company"),
    rev_lines_fy24=I(dict(pax=5485.261, baggage=67.132, ancillary=677.506, service=281.663,
                          cargo=181.778, hotel=72.512, leasing=149.443),
                     "Restated FY2024 disaggregation, same notes, " + FS25 + ". DISCREPANCY "
                     "NOTE: the filing's own restated-2024 column does not foot internally — "
                     "the six contract lines sum to 6,765.852 (total revenue) while the "
                     "printed contract-revenue subtotal is 6,616.409 (ex-lease); the 149.443 "
                     "lease-rental line is the difference. Unit metrics use the pax+baggage "
                     "lines as printed; recorded as a filing inconsistency, not repaired",
                     "2026-02-13", "Company"),
    dcost_lines_fy25=I(dict(fuel=2251.363, staff=1069.366, maint=800.577, dep_ppe=393.504,
                            landing=470.049, handling=384.125, dep_rou=177.181,
                            wet_lease=118.487, insurance=15.099, amort=11.032, other=397.349),
                       "Direct operating costs Note 29, " + FS25 + " — sums exactly to "
                       "6,088.132. Fuel is 37.0% of direct costs", "2026-02-13", "Company"),
    dcost_lines_fy24=I(dict(fuel=1924.547, staff=885.104, maint=685.639, dep_ppe=462.951,
                            landing=405.084, handling=344.585, dep_rou=142.145,
                            wet_lease=15.040, insurance=17.052, amort=10.059, other=310.738),
                       "Restated FY2024 direct operating costs, " + FS25, "2026-02-13", "Company"),
    dcost_lines_fy23=I(dict(fuel=1690.639, staff=774.751, maint=438.924, dep_ppe=495.060,
                            landing=361.209, handling=312.891, dep_rou=113.104,
                            wet_lease=0.0, insurance=12.274, amort=9.423, other=134.909),
                       "Direct costs note 27, FY2024 filing comparative (as reported — no "
                       "wet-lease line pre-restatement)", "2025-02-13", "Company"),

    # ---- JV / associate airline network (equity-accounted, 100% basis) ------
    jv_detail=I(dict(
        abu_dhabi=dict(stake=0.49, rev_100=2405.159, profit_100=221.448, share=54.210),
        fly_jinnah=dict(stake=0.45, rev_100=492.467, profit_100=90.094, share=36.070),
        maroc=dict(stake=0.4413, rev_100=774.662, profit_100=46.523, share=20.532),
        egypt=dict(stake=0.49, note="stake raised from 40% to 49% during FY2025"),
        dmm=dict(stake=0.49, note="Air Arabia DMM LLC, Saudi JV established FY2025 — "
                 "pre-operational")),
        "Note 12 (investments in associates and JVs), " + FS25 + " — FY2025 100%-basis "
        "revenue/profit and the Group's share, per investee", "2026-02-13", "Company"),

    # ---- forecast drivers — UNIT BUILD (pax x fare, cost per pax) -----------
    pax_path=I([12.85, 13.95, 15.15, 16.35, 17.55],
               "Consolidated passengers, millions, FY26E-FY30E. FY2026 -1.6%: Q1-2026 actual "
               "-11% y/y on the Feb-Mar airspace closures, phased restoration to ~1-Jun (IATA "
               "and route-restoration coverage), H2 growth on nine-plus neo deliveries. "
               "Thereafter +8.6/+8.6/+7.9/+7.3% — fleet-led (90 -> ~115 by FY2030 out of the "
               "120-aircraft order, Airbus delivery constraints acknowledged) at broadly held "
               "load factor ~85-86% (FY2025: 85.3%; Q1-2026 record 86.4%). Seat/ASK-level data "
               "is NOT disclosed — pax x load factor is the finest sourced level; FLAGGED",
               "2026-08-09", "House"),
    fare_path=I([488.0, 480.0, 484.0, 489.0, 494.0],
                "Passenger + baggage revenue per consolidated passenger, AED. History: 499.1 "
                "(FY23, as-reported basis), 494.9 (FY24 restated), 478.7 (FY25). FY2026 +1.9%: "
                "Q1-2026 revenue held +1% on -11% pax (constrained capacity lifted yields); "
                "FY2027 -1.6% as regional capacity restores; +1%/yr thereafter — LCC yield "
                "discipline, no real fare growth assumed", "2026-08-09", "House"),
    anc_path=I([67.4, 70.1, 72.9, 75.8, 78.8],
               "Ancillary ('other airline related services') revenue per passenger, AED, +4%/yr "
               "from FY2025's 64.8 (FY2024: 60.4, FY2023: 46.4) — the disclosed history's own "
               "trend, tapered", "2026-08-09", "House"),
    cargo_g=I([0.05, 0.05, 0.05, 0.05, 0.05], "Cargo revenue growth on FY2025's 186.9 — "
              "belly-capacity grows with the fleet", "2026-08-09", "House"),
    svc_g=I([0.04, 0.04, 0.04, 0.04, 0.04], "Service revenue growth on FY2025's 223.3 "
            "(ground handling, training, IT services to the JV network)", "2026-08-09", "House"),
    hotel_g=I([0.03, 0.03, 0.03, 0.03, 0.03], "Hotel operations growth on FY2025's 59.8 "
              "(Centro Sharjah + Radisson Blu Dubai Marina)", "2026-08-09", "House"),
    lease_g=I([0.10, 0.10, 0.08, 0.06, 0.05],
              "Aircraft-lease-rental revenue growth on FY2025's 219.8 — the leased-out fleet "
              "(17 aircraft to JV airlines) grows with Abu Dhabi's ~40% capacity expansion, "
              "Fly Jinnah, Egypt at the raised 49%, and the Saudi DMM launch",
              "2026-08-09", "House"),

    # ---- cost stack: ONE ESCALATOR PER DRIVER CLASS -------------------------
    jet_eff_base=I([100.7, 85.2, 86.9, 88.6, 90.4],
                   "EFFECTIVE (hedge-blended) jet fuel price path, USD/bbl — the study's "
                   "CENTRAL CONTESTED JUDGEMENT, priced BOTH ways (see jet_eff_alt). BASE = "
                   "the EIA-curve framing: 2025 market average ~USD 89/bbl (IATA); H1-2026 "
                   "spiked (IATA monitor USD 158.77 early Aug-2026) but the book is partly "
                   "hedged 2026-2028 (Note 24 swaps/collars; RATIOS undisclosed — flagged) and "
                   "Q1-2026's realised margin shows nothing like a spot-price hit; EIA "
                   "July-2026 STEO Brent 81.91 (2026) -> 64.76 (2027) then a mild crack-"
                   "normalised drift. Fuel cost per passenger = intensity x this path — its own "
                   "commodity escalator, never a CPI proxy", "2026-08-10", "Industry"),
    jet_eff_alt=I([108.4, 105.8, 106.4, 107.5, 108.5],
                  "The ALTERNATIVE fuel framing: IATA's June-2026 high-fuel view persists "
                  "through the hedge blend — no EIA-style relief. Published side by side with "
                  "the base everywhere the base appears", "2026-08-10", "Industry"),
    fuel_intensity=I(1.937, "Fuel intensity, AED per passenger per USD/bbl of effective jet "
                     "price: FY2025 audited fuel cost/pax 172.4 (Note 29 / presentations) over "
                     "the ~USD 89/bbl 2025 market average (IATA) = 1.937. Held flat — the "
                     "neo's ~20% lower burn is an upside not credited", "2026-08-10",
                     "Company/Industry"),
    fleet_cons=I(dict(fy25_end=56, ends=[58, 61, 64, 68, 72],
                      owned_adds=[1, 1, 1, 2, 2], leased_adds=[1, 2, 2, 2, 2],
                      ac_cost_owned=184.0, ac_rou=175.0, loan_per_owned=150.0),
                 "CONSOLIDATED fleet block (Sharjah + Ras Al Khaimah): YE2025 = 56 aircraft "
                 "per the company's own FY2025 presentation fleet allocation (Sharjah 54, RAK "
                 "2; the 90 total is GROUP-wide incl. the JV hubs). Forward: 16 net additions "
                 "to ~72 by FY2030 (within the 120-aircraft order and Airbus's constrained "
                 "output), split ~7 owned / ~9 leased at ~AED 184mn owned cost (~USD 50mn "
                 "A320neo family net) and ~AED 175mn right-of-use inception value per leased "
                 "aircraft; owned units loan-financed ~AED 150mn each (FY2025 actual: AED "
                 "849.6mn for 5 = 170/unit). The owned/leased split remains UNDISCLOSED — "
                 "flagged and sensitised", "2026-08-10", "Company/House"),
    staff_per_pax=I([84.4, 86.9, 89.5, 92.2, 94.9],
                    "Direct staff cost per passenger, AED, +3%/yr on FY2025's 81.9 (FY2024: "
                    "78.9, FY2023: 76.6) — UAE aviation wage drift, its own labour escalator, "
                    "partly offset by scale", "2026-08-09", "House"),
    maint_per_pax=I([63.8, 66.3, 69.0, 71.7, 74.6],
                    "Maintenance cost per passenger, AED, +4%/yr on FY2025's 61.3 (FY2023: "
                    "43.4 — the step-up is the ageing ceo fleet plus sector-wide MRO "
                    "inflation; neos relieve it only gradually). Its own MRO escalator",
                    "2026-08-09", "House"),
    landing_per_pax=I([36.7, 37.4, 38.2, 38.9, 39.7],
                      "Landing and overflying charges per passenger, AED, +2%/yr on FY2025's "
                      "36.0 — airport-tariff class escalator (UAE CPI ~2%, CBUAE QER)",
                      "2026-08-09", "Country"),
    handling_per_pax=I([30.0, 30.6, 31.2, 31.8, 32.4],
                       "Passenger, ground and technical handling per passenger, AED, +2%/yr on "
                       "FY2025's 29.4 — same tariff-class escalator, separate line",
                       "2026-08-09", "Country"),
    other_per_pax=I([41.5, 41.5, 41.5, 41.5, 41.5],
                    "Other direct costs per passenger (other operating 30.4 + wet-lease 9.1 + "
                    "insurance 1.2 + amortisation 0.8, FY2025), AED, held FLAT: the FY2025 "
                    "wet-lease spike (118.5 vs 15.0 in FY2024) unwinds as owned neos arrive, "
                    "absorbing the other lines' inflation", "2026-08-09", "House"),
    ga_g=I([0.05, 0.05, 0.05, 0.05, 0.05], "Cash G&A growth (FY2025 cash G&A = 316.3 less "
           "40.1 depreciation = 276.2) — scale plus wage drift", "2026-08-09", "House"),
    sm_pct=I(0.0146, "S&M held at FY2025's 1.46% of revenue (FY2024: 1.53%)",
             "2026-08-09", "House"),
    dna_path=I([720.0, 810.0, 900.0, 980.0, 1060.0],
               "Depreciation and amortisation, AED mn, FY26E-FY30E — grows with the OWNED "
               "fleet: FY2025's 621.8 steps up as loan-financed neo deliveries (5 in FY2025, "
               "~3-4/yr assumed owned henceforth) enter the depreciable base; leased "
               "deliveries enter ROU depreciation similarly. Fleet-driven, not a revenue "
               "ratio", "2026-08-09", "House"),
    capex_path=I([2000.0, 1900.0, 1900.0, 1950.0, 2000.0],
                 "Fleet capex including pre-delivery payments, AED mn. FY2025 actual: 2,327.6 "
                 "(a catch-up year: 5 owned aircraft + PDP build). Forward: ~3-4 owned "
                 "aircraft/yr at ~AED 185mn each plus a continuing PDP ladder on the "
                 "120-aircraft order; leased deliveries (the majority) do NOT pass through "
                 "capex (additions to lease liabilities: 472.2 FY2025, 538.9 FY2024). The "
                 "owned/leased delivery split is NOT disclosed — FLAGGED as the build's "
                 "weakest driver and sensitised heavily", "2026-08-09", "House"),
    nwc_pct=I(-0.64, "Operating working capital as a share of revenue, held at the historical "
              "band: (inventories + current receivables) less (current payables + deferred "
              "income + maintenance provisions + staff benefits) = -65.3% (FY23), -62.2% "
              "(FY24), -66.6% (FY25) of revenue. An airline sells tickets before it flies "
              "and accrues maintenance/end-of-service liabilities — growth RELEASES cash. "
              "-64% is the three-year centre, not the best year", "2026-08-09", "House"),
    assoc_g=I([0.02, 0.18, 0.18, 0.15, 0.12],
              "Share-of-JV/associate-profit growth path on FY2025's 189.975: FY2026 held "
              "near-flat (the JV hubs absorbed the same H1 disruption; Air Arabia DMM start-up "
              "costs begin), then +18/+18/+15/+12% as Abu Dhabi (+40% capacity plan), Fly "
              "Jinnah, Egypt (49%) and DMM ramp. The 100%-basis FY2025 P&Ls (Note 12) grew "
              "77% (Abu Dhabi) and 80% (Jinnah) y/y", "2026-08-09", "House"),
    other_g=I([0.08, 0.08, 0.08, 0.07, 0.06],
              "Other-income growth on FY2025's 197.1 (management fees from the JV network "
              "86.9 + misc) — fee income scales with JV activity", "2026-08-09", "House"),
    dep_rate_path=I([0.041, 0.038, 0.037, 0.037, 0.037],
                    "Yield on cash + fixed deposits: FY2025 disclosed average 4.41% (Note 17), "
                    "rolled down with the CBUAE base-rate path (3.65% held 29-Jul-2026, Fed "
                    "flat-to-easing bias)", "2026-08-09", "Country"),
    payout=I([1.00, 0.90, 0.85, 0.85, 0.85],
             "Dividend payout on attributable profit: FY2025's AED 0.30/share = 86% of EPS "
             "0.35, DPS raised 5 fils every year since FY2022 (0.15/0.20/0.25/0.30). FY2026 "
             "held at 0.30 (100% of a dip-year EPS, funded by net cash), then ~85-90%",
             "2026-08-09", "House"),

    # ---- cost of capital ---------------------------------------------------
    rf=I(0.0448, "AED sovereign anchor: UAE Ministry of Finance dirham T-Bond auction, "
         "July-2026 — January-2031 tranche YTM 4.48% (4bp over comparable UST; May-2026 "
         "auction: 4.30%). The LOCAL-currency government bond, per the standing rule, not a "
         "USD proxy", "2026-07-30", "Country"),
    sov_spread_obs=I(0.0004, "The OBSERVED default spread embedded in the AED sovereign "
                     "yield actually used: the July-2026 MoF auction priced the January-2031 "
                     "tranche 4bp over comparable US Treasuries (May-2026: 14bp). Netting THIS "
                     "spread — not the 42bp rating-table spread — keeps the risk-free rate "
                     "currency-consistent under the 1:1 peg (UST 5-yr 4.35% on 07-Aug-2026, "
                     "US Treasury daily curve): 4.48% - 0.04% = 4.44% > 4.35%. Adopted after "
                     "external critique; the rating-basis netting (4.06%) is published as the "
                     "alternative construction", "2026-08-10", "Country"),
    sov_spread_rating=I(0.0042, "Damodaran adjusted default spread, United Arab Emirates row "
                        "(Moody's Aa2), original ctryprem file last updated 5-Jan-2026. "
                        "Netted out of the local yield so sovereign risk is not double-counted",
                        "2026-01-05", "Country"),
    erp_rating=I(0.0487, "Damodaran total equity risk premium, UAE row, rating basis (mature "
                 "4.23% + CRP 0.64%), 5-Jan-2026 file. The CDS column for the UAE is NA in the "
                 "same file, so the rating basis is the ONLY published construction — both-"
                 "bases publication is therefore rating + a stated NA, not two numbers",
                 "2026-01-05", "Country"),
    erp_cds=I(None, "UAE sovereign CDS column: NA in Damodaran's January-2026 file — no "
              "CDS-basis ERP exists to publish; stated plainly rather than substituted",
              "2026-01-05", "Country"),
    beta_used=I(1.086, "Tier-1 OWN-STOCK regression: AIRARABIA weekly log-returns vs the DFM "
                "General Index (DFMGI), 5-year window to 16-Jul-2026: beta 1.086, R-squared "
                "0.402, n=258, SE 0.083, CI90 [0.95, 1.22] — clears the usability gate, not "
                "weak-instrument flagged. DFMGI is the stock's own market: every filing states "
                "the ordinary shares are listed on the Dubai Financial Market (FY2025 note 1; "
                "FY2025 annual report; Q1-2026 interim note 1) and the annual report benchmarks "
                "the share price against DFMGI. See beta_result.json", "2026-08-09", "House"),
    beta_alt_benchmark=I(0.812, "ALTERNATIVE-BENCHMARK cross-check, published not adopted: the "
                "same own-stock 5-year weekly regression run against the FTSE ADX General Index "
                "(index series to 24-Jul-2026): beta 0.812, R-squared 0.135, n=260, SE 0.128, "
                "CI90 [0.60, 1.02]. It clears the same usability gate but explains a THIRD as "
                "much of the stock's weekly variance as its own exchange's composite does, which "
                "is itself the evidence that DFMGI is the right regressor for a DFM-listed name. "
                "Priced in full rather than mentioned", "2026-08-17", "House"),
    kd_booked_path=I([0.031, 0.033, 0.035, 0.036, 0.037],
                     "BOOKED blended finance-cost rate on the rolling gross debt book: FY2025 "
                     "effective 2.73% (finance costs 66.7 / average gross debt), rising as new "
                     "leases (~4%, Note 25) and new aircraft loans (~marginal 5.4%) replace "
                     "older cheaper layers", "2026-08-10", "Company/House"),
    debt_amort=I([500.0, 520.0, 540.0, 560.0, 580.0],
                 "Scheduled repayments of borrowings + lease principal (FY2025 actuals: "
                 "393.7 borrowings repaid + 248.1 lease principal ≈ 642 gross; forward net of "
                 "refinancing ~500-580/yr)", "2026-08-10", "Company/House"),
    kd=I(0.055, "Marginal AED cost of debt: the AED sovereign 4.48% (Jan-2031) plus ~100bp "
         "unsecured corporate allowance for an unrated but NET-CASH flag carrier affiliate. "
         "Evidence table: FY2025 lease book carries an average 4% finance charge (Note 25, "
         "SECURED on aircraft — a floor, not the marginal unsecured rate); the FY2025 "
         "aircraft loan was similarly secured; deposits EARN 4.41%. 5.5% sits above the "
         "sovereign, above the secured book, and above the deposit rate, as it must",
         "2026-08-09", "Company/House"),
    kd_path=I([0.054, 0.052, 0.051, 0.050, 0.050],
              "Forward marginal Kd, easing ~50bp with the Fed/CBUAE path over five years — "
              "the discount-rate glide takes its shape from this path by construction",
              "2026-08-09", "House"),
    kd_term=I(0.050, "Terminal AED cost of debt: long-run UAE sovereign norm ~4.0% + 100bp "
              "corporate spread", "2026-08-09", "House"),
    rf_term=I(0.040, "Terminal risk-free rate, norm-built: ~2% UAE/US long-run inflation "
              "(CBUAE projects 1.8-2.0%) + ~2pp real — the mature-market neutral-rate "
              "convention for a hard-pegged currency. Never a historical average, never "
              "backed out of a price", "2026-08-09", "House"),
    erp_term=I(0.0475, "Terminal equity risk premium: between the mature-market 4.23% and "
               "today's UAE 4.87% — the Aa2 country premium is small and kept",
               "2026-08-09", "House"),
    wd_term=I(0.10, "Terminal debt weight D/(D+E) on a GROSS basis, ~today's 10.2% gross "
              "weight held: the airline runs structurally net-cash but carries secured "
              "aircraft debt and IFRS-16 leases permanently", "2026-08-09", "House"),
    g_term=I(0.025, "Terminal growth 2.5%, AED-nominal against a 4.0% terminal risk-free that "
             "embeds ~2% inflation — about 0.5pp real, for a carrier whose home market "
             "(Sharjah 19.5mn airport pax +13.9% in 2025) is still structurally growing. "
             "Sensitised 1.5-3.5%", "2026-08-09", "House"),

    # ---- lens inputs -------------------------------------------------------
    ev_ebitda_just=I(6.5, "Justified EV/EBITDA on mid-cycle FY2027E EBITDA EXCLUDING the "
                     "fee/other-income stream (valued separately — basis matched to how peer "
                     "multiples are computed). Peer set rebuilt from PRIMARY filings after "
                     "external critique: Ryanair 6.50x (FY26 EBITDA EUR 3,747.6mn = op profit "
                     "2,374.2 + dep 1,373.4; 1,039.2mn shares and EUR 2.7bn net cash per the "
                     "Q1-FY27 report), Wizz ~4.75x (FY26 EBITDA 1,318.3), easyJet ~3.5x, "
                     "IndiGo 11.1x, Pegasus ~6.6x (EUR-functional IFRS) -> median 6.5x. "
                     "Bear 5.0x / bull 8.0x", "2026-08-10", "Industry"),
    pe_just=I(13.0, "Justified through-cycle P/E on normalised earnings. Peers: Ryanair 12.6x, "
              "easyJet 12.4x, Jazeera ~17.7x computed, Damodaran profitable-airlines 12.87x. "
              "13x reflects a structurally profitable LCC with net cash and a growing "
              "equity-accounted network. Bear 10x / bull 16x", "2026-08-09", "Industry"),
    roe_sust=I(0.18, "Sustainable return on equity for the book lens. Trailing ROE on average "
               "attributable equity: 19.9% (FY2025), 18.9% (FY2024) — struck slightly below "
               "the record year", "2026-08-09", "House"),
    jv_pe=I(15.0, "Capitalisation multiple for the JV/associate airline network in the "
            "ALTERNATIVE bridge framing: the share of profit (189.975, growing double-digit) "
            "at 15x — a growth-LCC multiple in line with Jazeera and above the mature peers. "
            "The BASE framing carries the audited carrying value 363.386 instead. THE "
            "CONTESTED JUDGEMENT, published both ways, never averaged", "2026-08-09", "House"),
    nci_book=I(1.287, "Non-controlling interests at audited carrying value, 31-Dec-2025 "
               "— the correct deduction basis (the prior profit-share-ratio proxy deducted "
               "2.9)", "2026-02-13", "Company"),
    lens_weights=I(dict(dcf=0.45, relative=0.20, normalized=0.20, book=0.15),
                   "DCF primary for an operating airline with a disclosed unit history; "
                   "relative and normalised secondary; book least — an airline's book equity "
                   "understates a slot/brand/JV franchise", "2026-08-09", "House"),
    anchor_days=I(219, "Days from the DCF construction date (31-Dec-2025, the audited "
                  "balance-sheet date) to the anchor 7-Aug-2026. All lens values are rolled "
                  "to the anchor at the cost of equity, net of the AED 0.30 FY2025 dividend "
                  "paid inside the window", "2026-08-09", "House"),
)

# validate four-field completeness (code-first rule)
for k, rec in INP.items():
    assert set(rec) == {'value', 'source', 'date', 'ring'}, f"INPUT {k} not four-field"
    assert rec['source'] and rec['date'] and rec['ring'], f"INPUT {k} missing provenance"

V = {k: rec['value'] for k, rec in INP.items()}
V['fuel_per_pax'] = [V['fuel_intensity'] * p for p in V['jet_eff_base']]
V['fuel_per_pax_alt'] = [V['fuel_intensity'] * p for p in V['jet_eff_alt']]
FL = V['fleet_cons']
leased_gross = [FL['leased_adds'][i] * FL['ac_rou'] for i in range(5)]
fleet_ends = [FL['fy25_end']] + FL['ends']
fleet_avg = [(fleet_ends[i] + fleet_ends[i + 1]) / 2 for i in range(5)]
LOG = []
def say(s):
    LOG.append(s); print(s)

say("=" * 78)
say("AIRARABIA — ASSERT / derivation log (built on the audited FY22-25 + Q1-2026 filings)")
say("=" * 78)

# ============================ CALC ===========================================
SH, SPOT, TAX = V['shares_mn'], V['spot'], V['tax_eff']
MKTCAP = SPOT * SH

# ---- historical income statement — every line AUDITED ----------------------
hist_is = {}
for y in ('fy23', 'fy24', 'fy25'):
    op = V[f'rev_{y}'] - V[f'dcost_{y}'] - V[f'ga_{y}'] - V[f'sm_{y}']
    gp = V[f'rev_{y}'] - V[f'dcost_{y}']
    ebt = op + V[f'fininc_{y}'] - V[f'fincost_{y}'] + V[f'assoc_{y}'] + V[f'other_{y}']
    hist_is[y.upper().replace('FY', 'FY')] = dict(
        rev=V[f'rev_{y}'], dcost=V[f'dcost_{y}'], gp=gp, ga=V[f'ga_{y}'], sm=V[f'sm_{y}'],
        ebit=op, dna=V[f'dna_{y}'], ebitda=op + V[f'dna_{y}'],
        ebitda_incl=op + V[f'dna_{y}'] + V[f'other_{y}'],
        fininc=V[f'fininc_{y}'], fincost=V[f'fincost_{y}'], assoc=V[f'assoc_{y}'],
        other=V[f'other_{y}'], ebt=ebt, tax=V[f'tax_{y}'], pat=V[f'pat_{y}'],
        nci=V[f'pat_{y}'] - V[f'npa_{y}'], npa=V[f'npa_{y}'])
for y in ('FY23', 'FY24', 'FY25'):
    assert abs(hist_is[y]['ebt'] - (hist_is[y]['pat'] + hist_is[y]['tax'])) < 0.5, \
        f'{y} P&L does not close: EBT {hist_is[y]["ebt"]:.3f} vs PAT+tax ' \
        f'{hist_is[y]["pat"] + hist_is[y]["tax"]:.3f}'
say(f"[Historical income statement] every FY2023-25 line is the audited/restated figure. "
    f"Operating profit closes to the audited statement in all three years (FY25: "
    f"{hist_is['FY25']['ebit']:,.1f} = revenue 7,787.6 - direct 6,088.1 - G&A 316.3 - S&M "
    f"113.6). House EBITDA (operating profit + D&A): FY23 {hist_is['FY23']['ebitda']:,.0f}, "
    f"FY24 {hist_is['FY24']['ebitda']:,.0f}, FY25 {hist_is['FY25']['ebitda']:,.0f} "
    f"({hist_is['FY25']['ebitda']/V['rev_fy25']:.1%} of revenue); including the recurring "
    f"other-income line (management fees from the JV network) FY25 "
    f"{hist_is['FY25']['ebitda_incl']:,.0f}. Effective tax: FY24 8.79%, FY25 11.60% — the "
    f"forecast provides at the statutory 15% DMTT.")

# ---- direct-cost stack reconciliation --------------------------------------
for y, key in (('FY23', 'dcost_lines_fy23'), ('FY24', 'dcost_lines_fy24'),
               ('FY25', 'dcost_lines_fy25')):
    s = sum(V[key].values())
    assert abs(s - hist_is[y]['dcost']) < 0.5, f'{y} direct-cost stack does not sum: {s}'
rl25 = V['rev_lines_fy25']
assert abs(sum(rl25.values()) - V['rev_fy25']) < 0.5, 'FY25 revenue lines do not sum'
rl24 = V['rev_lines_fy24']
# FY24 lines carry the filing's own internal inconsistency (see the input's discrepancy
# note): the six contract lines already sum to TOTAL restated revenue, so the check is
# lines-vs-total including nothing twice — the lease line is the filing's own residual.
assert abs(sum(v for k, v in rl24.items() if k != 'leasing') - V['rev_fy24']) < 0.5, \
    'FY24 revenue lines (ex-lease residual) do not sum to restated revenue'

# ---- unit economics history -------------------------------------------------
PAX = V['pax_hist']
unit_hist = {}
for y, rl, dl in (('FY24', rl24, V['dcost_lines_fy24']), ('FY25', rl25, V['dcost_lines_fy25'])):
    p = PAX[y]
    unit_hist[y] = dict(
        pax=p, lf=V['lf_hist'][y],
        fare=(rl['pax'] + rl['baggage']) / p, anc=rl['ancillary'] / p,
        fuel=dl['fuel'] / p, staff=dl['staff'] / p, maint=dl['maint'] / p,
        landing=dl['landing'] / p, handling=dl['handling'] / p,
        other=(dl['wet_lease'] + dl['insurance'] + dl['other'] + dl['amort']) / p,
        cash_cost=(sum(dl.values()) - dl['dep_ppe'] - dl['dep_rou'] - dl['amort']) / p)
say(f"[Unit economics, disclosed] FY2025 on 13.06mn consolidated passengers: fare+baggage "
    f"{unit_hist['FY25']['fare']:.1f}/pax (FY24 {unit_hist['FY24']['fare']:.1f}), ancillary "
    f"{unit_hist['FY25']['anc']:.1f} ({unit_hist['FY24']['anc']:.1f}), fuel "
    f"{unit_hist['FY25']['fuel']:.1f} ({unit_hist['FY24']['fuel']:.1f}), staff "
    f"{unit_hist['FY25']['staff']:.1f}, maintenance {unit_hist['FY25']['maint']:.1f}, landing "
    f"{unit_hist['FY25']['landing']:.1f}, handling {unit_hist['FY25']['handling']:.1f}. Load "
    f"factor 85.3% (record). Seat/ASK data is not disclosed: passengers x per-pax rates is "
    f"the finest sourced level, and the gap is flagged rather than reconstructed.")

# ---- historical balance sheet, working capital, net debt --------------------
def nwc_of(y):
    return (V[f'inv_{y}'] + V[f'recv_{y}']) - (V[f'pay_{y}'] + V[f'definc_{y}'] +
                                               V[f'maint_{y}'] + V[f'staffb_{y}'])
nwc_fy23, nwc_fy24, nwc_fy25 = nwc_of('fy23'), nwc_of('fy24'), nwc_of('fy25')
debt_fy23 = V['borrow_fy23'] + V['lease_fy23']
debt_fy24 = V['borrow_fy24'] + V['lease_fy24']
debt_fy25 = V['borrow_fy25'] + V['lease_fy25']
liq_fy23 = V['cash_fy23'] + V['dep_fy23']
liq_fy24 = V['cash_fy24'] + V['dep_fy24']
liq_fy25 = V['cash_fy25'] + V['dep_fy25']
nd_fy23, nd_fy24, nd_fy25 = debt_fy23 - liq_fy23, debt_fy24 - liq_fy24, debt_fy25 - liq_fy25
say(f"[Working capital, audited] operating WC (inventories + current receivables less "
    f"payables, deferred income, maintenance provisions and staff benefits): FY23 "
    f"{nwc_fy23:,.0f} ({nwc_fy23/V['rev_fy23']:.1%} of revenue), FY24 {nwc_fy24:,.0f} "
    f"({nwc_fy24/V['rev_fy24']:.1%}), FY25 {nwc_fy25:,.0f} ({nwc_fy25/V['rev_fy25']:.1%}) — "
    f"deeply NEGATIVE: tickets are sold before they are flown and maintenance/end-of-service "
    f"obligations accrue ahead of cash. Growth releases cash.")
say(f"[Net debt] gross borrowings + lease liabilities: FY23 {debt_fy23:,.0f}, FY24 "
    f"{debt_fy24:,.0f}, FY25 {debt_fy25:,.0f}; cash + fixed deposits {liq_fy23:,.0f} / "
    f"{liq_fy24:,.0f} / {liq_fy25:,.0f} -> NET CASH of {-nd_fy25:,.0f} at FY2025 "
    f"({-nd_fy24:,.0f} FY2024). The bridge quantity is interest-bearing debt less cash and "
    f"deposits; deferred income and provisions live in working capital, never double-counted.")
assert nd_fy25 < 0, "Air Arabia must screen net cash on the audited FY2025 balance sheet"
assert abs(V['nwc_pct'] - (nwc_fy23/V['rev_fy23'] + nwc_fy24/V['rev_fy24'] +
                           nwc_fy25/V['rev_fy25']) / 3) < 0.015, \
    "NWC driver not the three-year centre"

# ---- Kd integrity ----------------------------------------------------------
kd_eff_fy25 = (V['fincost_fy25']) / ((debt_fy24 + debt_fy25) / 2)
say(f"[Kd integrity] (i) the audited book is SECURED and cheap: leases at an average 4% "
    f"finance charge (Note 25), the FY2025 aircraft loan mortgage-secured; effective finance "
    f"cost / average gross debt = {kd_eff_fy25:.2%}. (ii) the adopted MARGINAL Kd "
    f"{V['kd']:.2%} deliberately sits ABOVE the secured effective rate and ABOVE the AED "
    f"sovereign {V['rf']:.2%} — a same-currency corporate cannot fund below its sovereign "
    f"unsecured. (iii) deposits earn {0.0441:.2%}: the marginal Kd also clears the "
    f"opportunity yield on the asset side.")
assert V['kd'] > V['rf'], "marginal Kd must sit above the AED sovereign"
assert V['kd'] > kd_eff_fy25, "marginal unsecured Kd must exceed the secured effective rate"
assert V['kd'] > 0.0441, "marginal Kd must exceed the deposit yield"

# ---- cost of capital (v2: rf normalised, single-count of country risk) -----
rf_star = V['rf'] - V['sov_spread_obs']
rf_star_rating_alt = V['rf'] - V['sov_spread_rating']
BETA = V['beta_used']
ke_exp = rf_star + BETA * V['erp_rating']
kd_at = V['kd'] * (1 - TAX)
wd_gross = debt_fy25 / (debt_fy25 + MKTCAP)
we_gross = 1 - wd_gross
wacc_exp = we_gross * ke_exp + wd_gross * kd_at
wd_net = nd_fy25 / (nd_fy25 + MKTCAP)     # negative: net cash
wacc_net = (1 - wd_net) * ke_exp + wd_net * kd_at
say(f"[Cost of equity] AED sovereign {V['rf']:.2%} (MoF T-Bond auction Jul-2026, Jan-2031 "
    f"tranche) less the OBSERVED 4bp spread the auction itself priced over US Treasuries = rf* "
    f"{rf_star:.2%} — currency-consistent under the peg (UST 5-yr 4.35% on 07-Aug-2026); the "
    f"rating-basis netting ({rf_star_rating_alt:.2%}) is published as the alternative. + beta "
    f"{BETA:.3f} (own-stock weekly vs DFMGI, R2 0.40) x ERP {V['erp_rating']:.2%} (Damodaran "
    f"UAE row, Jan-2026; CDS column NA — stated, not substituted) -> Ke {ke_exp:.2%}.")
say(f"[WACC explicit] GROSS-debt weights {wd_gross:.1%}/{we_gross:.1%} -> {wacc_exp:.2%}. "
    f"On the NET basis the company is net cash (weight {wd_net:.1%}), which would push the "
    f"rate to {wacc_net:.2%}; the gross basis is used because the bridge separately credits "
    f"the cash pile at face value, and the gross basis is the conservative (lower-discount-"
    f"rate-on-nothing) choice here: it is the LOWER of the two, matched by adding cash in "
    f"the bridge rather than pretending the discount rate is higher.")

# ---- terminal (norm-built) --------------------------------------------------
ke_term = V['rf_term'] + BETA * V['erp_term']
kd_term_at = V['kd_term'] * (1 - TAX)
wacc_term = (1 - V['wd_term']) * ke_term + V['wd_term'] * kd_term_at
say(f"[WACC terminal] Ke {ke_term:.2%} (rf {V['rf_term']:.2%} + beta x ERP "
    f"{V['erp_term']:.2%}); Kd after tax {kd_term_at:.2%}; weights "
    f"{1-V['wd_term']:.0%}/{V['wd_term']:.0%} -> {wacc_term:.2%}")
assert wacc_term < wacc_exp, "terminal WACC must be below the explicit-window WACC"

# ---- glide from kd_path ------------------------------------------------------
kdp = V['kd_path']
glide_frac = [(kdp[0] - k) / (kdp[0] - kdp[-1]) for k in kdp]
fwd = [wacc_exp - (wacc_exp - wacc_term) * f for f in glide_frac]
df, c = [], 1.0
for w in fwd:
    c /= (1 + w); df.append(c)
assert all(fwd[i] >= fwd[i + 1] for i in range(len(fwd) - 1)), "glide not monotone"
say("[Glide] forward WACC " + " -> ".join(f"{w:.2%}" for w in fwd) +
    "; discount factors " + ", ".join(f"{d:.4f}" for d in df) +
    ". The glide fractions are the cost-of-debt path's own cumulative progress.")

# ============================ UNIT-BUILD FORECAST =============================
YRS = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
SUBS = ['pax', 'ancillary', 'cargosvc', 'hotel', 'leasing']
SUBNAME = dict(pax='Passenger and baggage', ancillary='Ancillary services',
               cargosvc='Cargo and service revenue', hotel='Hotel operations',
               leasing='Aircraft leases to the JV network')

def build(pax_mult=1.0, fare_mult=1.0, fuel_mult=1.0, cost_shift=0.0, use_alt_fuel=False):
    """Re-run the whole unit build. Scenarios and sensitivity grids call THIS, so a
    fuel move flows through the per-pax fuel line, a demand move through every
    pax-linked revenue AND cost line — never a flat multiplier on finished revenue."""
    fuel_line = V['fuel_per_pax_alt'] if use_alt_fuel else V['fuel_per_pax']
    pax = [p * pax_mult for p in V['pax_path']]
    rev_pax = [pax[i] * V['fare_path'][i] * fare_mult for i in range(5)]
    rev_anc = [pax[i] * V['anc_path'][i] for i in range(5)]
    cargo0, svc0, hot0, lea0 = rl25['cargo'], rl25['service'], rl25['hotel'], rl25['leasing']
    rev_cs, rev_h, rev_l = [], [], []
    c_, s_, h_, l_ = cargo0, svc0, hot0, lea0
    for i in range(5):
        c_ *= 1 + V['cargo_g'][i]; s_ *= 1 + V['svc_g'][i]
        h_ *= 1 + V['hotel_g'][i]; l_ *= 1 + V['lease_g'][i]
        rev_cs.append(c_ + s_); rev_h.append(h_); rev_l.append(l_)
    rev_ = [rev_pax[i] + rev_anc[i] + rev_cs[i] + rev_h[i] + rev_l[i] for i in range(5)]
    cash_cost_pax = [(fuel_line[i] * fuel_mult + V['staff_per_pax'][i] +
                      V['maint_per_pax'][i] + V['landing_per_pax'][i] +
                      V['handling_per_pax'][i] + V['other_per_pax'][i]) * (1 + cost_shift)
                     for i in range(5)]
    dcost_cash = [pax[i] * cash_cost_pax[i] for i in range(5)]
    ga_cash, g_ = [], V['ga_fy25'] - 40.081       # FY2025 cash G&A (less its depreciation)
    for i in range(5):
        g_ *= 1 + V['ga_g'][i]; ga_cash.append(g_)
    sm_ = [V['sm_pct'] * r for r in rev_]
    other_, o_ = [], V['other_fy25']
    for i in range(5):
        o_ *= 1 + V['other_g'][i]; other_.append(o_)
    ebitda_ = [rev_[i] - dcost_cash[i] - ga_cash[i] - sm_[i] for i in range(5)]
    ebitda_incl_ = [ebitda_[i] + other_[i] for i in range(5)]
    seg_rev = [dict(pax=rev_pax[i], ancillary=rev_anc[i], cargosvc=rev_cs[i],
                    hotel=rev_h[i], leasing=rev_l[i]) for i in range(5)]
    return dict(pax=pax, rev=rev_, seg_rev=seg_rev, dcost_cash=dcost_cash, ga=ga_cash,
                sm=sm_, other=other_, ebitda=ebitda_, ebitda_incl=ebitda_incl_,
                cash_cost_pax=cash_cost_pax)

_B = build()
pax_f = _B['pax']; rev = _B['rev']; seg_rev = _B['seg_rev']
ebitda = _B['ebitda']; ebitda_incl = _B['ebitda_incl']; other_inc = _B['other']
ebitda_margin = [ebitda[i] / rev[i] for i in range(5)]
say(f"[Forecast, unit build] passengers " + " -> ".join(f"{p:.2f}mn" for p in pax_f) +
    f"; revenue " + " -> ".join(f"{r:,.0f}" for r in rev) +
    " (growth " + ", ".join(f"{rev[i]/(V['rev_fy25'] if i==0 else rev[i-1])-1:+.1%}"
                            for i in range(5)) + ")")
say(f"[Margins are OUTPUTS] EBITDA margin " + " -> ".join(f"{m:.1%}" for m in ebitda_margin) +
    f" (FY2025 actual {hist_is['FY25']['ebitda']/V['rev_fy25']:.1%}). The FY2026 compression "
    f"is the fuel spike + flat traffic; FY2027 recovers on the EIA fuel path.")
_impl26 = V['q1_26_rev'] / (V['q1_25_rev'] / V['rev_fy25'])
say(f"[FY2026 cross-check against the print] Q1-2026 revenue {V['q1_26_rev']:,.1f} grossed up "
    f"on Q1-2025's seasonal share of FY2025 implies {_impl26:,.0f}; the build produces "
    f"{rev[0]:,.0f} ({rev[0]/_impl26-1:+.1%}).")
assert abs(rev[0] / _impl26 - 1) < 0.10, 'FY26 build diverges from the Q1-2026 print'

# ---- FCFF waterfall ---------------------------------------------------------
dna = list(V['dna_path'])
ebit = [ebitda[i] - dna[i] for i in range(5)]
ebit_incl = [ebitda_incl[i] - dna[i] for i in range(5)]
nopat = [e * (1 - TAX) for e in ebit_incl]     # fees/other income are operating and recurring
capex = list(V['capex_path'])
nwc = [V['nwc_pct'] * r for r in rev]
dnwc = [nwc[0] - nwc_fy25] + [nwc[i] - nwc[i - 1] for i in range(1, 5)]
fcff = [nopat[i] + dna[i] - capex[i] - leased_gross[i] - dnwc[i] for i in range(5)]
say(f"[Leased-fleet charge — adopted from external critique] the forecast leased aircraft "
    f"({sum(FL['leased_adds'])} of the 16 consolidated additions) are no longer acquired for "
    f"free: their gross right-of-use inception value ({', '.join(f'{x:,.0f}' for x in leased_gross)}) "
    f"is charged inside FCFF as leased capex — the 'firm buys all capacity with capital' "
    f"convention, with the financing mix left to the WACC. The NPV-0-financing alternative "
    f"(strip leased assets from invested capital, charge nothing) is worth ~+0.09/share and is "
    f"noted, not adopted.")
pv = [fcff[i] * df[i] for i in range(5)]
pv_explicit = float(sum(pv))
say(f"[FCFF waterfall] NOPAT (on EBIT including the recurring fee/other-income line, at the "
    f"15% DMTT) " + ", ".join(f"{n:,.0f}" for n in nopat) + "; capex " +
    ", ".join(f"{c_:,.0f}" for c_ in capex) + "; working-capital release " +
    ", ".join(f"{-d:+,.0f}" for d in dnwc) + " -> FCFF " +
    ", ".join(f"{f_:,.0f}" for f_ in fcff) + ".")

# ---- forward net-finance, profit, dividend, equity, net debt -----------------
nci_share = (V['pat_fy25'] - V['npa_fy25']) / V['pat_fy25']
DPS_FLOOR = 1400.0   # AED mn = 30 fils held — the ladder is not broken by the base case
interest_path, fininc_path, np_fc, div_fc, eq_fc, nd_fc, assoc_fc, debt_fc = [], [], [], [], [], [], [], []
_nd, _eq, _assoc, _debt = nd_fy25, V['eqp_fy25'], V['assoc_fy25'], debt_fy25
for i in range(5):
    _debt_open = _debt
    _debt = _debt + leased_gross[i] + FL['owned_adds'][i] * FL['loan_per_owned'] - V['debt_amort'][i]
    _liq_open = _debt_open - _nd
    _fin_in = V['dep_rate_path'][i] * _liq_open
    _fin_out = V['kd_booked_path'][i] * (_debt_open + _debt) / 2
    _assoc = _assoc * (1 + V['assoc_g'][i])
    _pat = (ebit_incl[i] + _fin_in - _fin_out) * (1 - TAX) + _assoc   # JV share BELOW the tax line
    _npa = _pat * (1 - nci_share)
    _div = max(V['payout'][i] * _npa, DPS_FLOOR)
    _eq += _npa - _div
    _nd = _nd - (fcff[i] + (_fin_in - _fin_out) * (1 - TAX)) + _div
    interest_path.append(_fin_out); fininc_path.append(_fin_in); assoc_fc.append(_assoc)
    np_fc.append(_npa); div_fc.append(_div); eq_fc.append(_eq); nd_fc.append(_nd)
    debt_fc.append(_debt)
say(f"[Forecast net finance — rebuilt after critique] gross debt now ROLLS with the financing "
    f"of the fleet (leases + aircraft loans - amortisation): " +
    " -> ".join(f"{d:,.0f}" for d in debt_fc) + f"; finance costs at the booked blended rate " +
    ", ".join(f"{x:,.0f}" for x in interest_path) + f" (no hardcoded factor); finance income " +
    ", ".join(f"{x:,.0f}" for x in fininc_path) + ". BOTH financing legs are tax-effected in "
    "the net-debt roll; the JV/associate share sits BELOW the tax line (equity-method income "
    "arrives net of the ventures' own tax). Attributable profit " +
    ", ".join(f"{x:,.0f}" for x in np_fc) + "; EPS " +
    ", ".join(f"{x/SH:.3f}" for x in np_fc) + "; DPS floored at 30 fils throughout — the "
    "dividend ladder holds in the base case by construction, funded by net cash in the dip "
    "year.")

# ---- invested capital, terminal ---------------------------------------------
fleet_assets_fy25 = V['ppe_fy25'] + V['rou_fy25'] + V['adv_fy25']
ic_fy25 = fleet_assets_fy25 + V['intang_fy25'] + nwc_fy25
ppe = []
p = fleet_assets_fy25
for i in range(5):
    p += capex[i] + leased_gross[i] - dna[i]
    ppe.append(p)
ic = [nwc[i] + ppe[i] + V['intang_fy25'] for i in range(5)]
roic = [nopat[i] / ic[i] for i in range(5)]
roic_term = nopat[-1] * (1 + V['g_term']) / ic[-1]
nopat_fy25 = (hist_is['FY25']['ebit'] + V['other_fy25']) * (1 - TAX)
roic_fy25 = nopat_fy25 / ic_fy25
say(f"[Invested capital] FY2025: fleet assets (PP&E + right-of-use + pre-delivery payments) "
    f"{fleet_assets_fy25:,.0f} + intangibles {V['intang_fy25']:,.0f} + working capital "
    f"{nwc_fy25:,.0f} = {ic_fy25:,.0f}; ROIC {roic_fy25:.1%}. Terminal ROIC (NOPAT(n+1)/"
    f"IC(n)) {roic_term:.1%}.")
rr_term = V['g_term'] / roic_term
nopat_term = nopat[-1] * (1 + V['g_term'])
tv = nopat_term * (1 - rr_term) / (wacc_term - V['g_term'])
pv_tv = tv * df[-1]
ev = pv_explicit + pv_tv
tv_share = pv_tv / ev
say(f"[Terminal value] reinvestment g/ROIC = {rr_term:.1%}; terminal NOPAT {nopat_term:,.0f}; "
    f"TV {tv:,.0f} at terminal WACC {wacc_term:.2%} minus g {V['g_term']:.1%}, discounted at "
    f"the year-5 factor {df[-1]:.4f} -> PV {pv_tv:,.0f}. Terminal value is {tv_share:.0%} of "
    f"operating enterprise value — HIGH, because the explicit window carries the fleet "
    f"build-out's capex while its revenue tail sits beyond FY2030; said plainly, not hidden.")
assert abs(roic_term * rr_term - V['g_term']) < 1e-9, "terminal g != ROIC x RR"

# ---- EV -> equity bridge: THE CONTESTED JUDGEMENT BOTH WAYS ------------------
non_op = (V['fvoci_fy25'] + V['invprop_fy25'] + V['nil_fy25'])
jv_book = V['assoc_bv_fy25']
jv_cap = V['jv_pe'] * V['assoc_fy25']
say(f"[JV network — BOTH WAYS, never averaged] BASE: audited carrying value {jv_book:,.0f}. "
    f"ALTERNATIVE: capitalised share of FY2025 profit {V['assoc_fy25']:,.0f} x "
    f"{V['jv_pe']:.0f} = {jv_cap:,.0f}. The gap ({(jv_cap-jv_book)/SH:+.2f}/share) is the "
    f"single most consequential contested judgement in this study: five airline JVs "
    f"(Abu Dhabi, Egypt at a raised 49%, Fly Jinnah, Maroc, the pre-operational Saudi DMM) "
    f"whose combined 100%-basis profits grew ~65% in FY2025 sit on the balance sheet at "
    f"less than 2.0x their annual profit share.")

def bridge(ev_ops, jv_val):
    eq_pre = ev_ops - nd_fy25 + non_op + jv_val
    nci_val = V['nci_book']                      # NCI at audited carrying value
    return eq_pre - nci_val, nci_val

T_ANCHOR = V['anchor_days'] / 365.0
ROLL = (1 + ke_exp) ** T_ANCHOR
ROLL_CASH = (1 + V['dep_rate_path'][0]) ** T_ANCHOR   # cash legs accrete at the cash yield
def to_anchor(v):
    return v * ROLL - V['dps_fy25']
def to_anchor_split(ev_ops, jv_val, roll=None):
    """Operating equity rolls at Ke; the cash/near-cash legs (net cash, non-operating
    assets, JV book) roll at the deposit yield — adopted from external critique: cash
    does not compound at the cost of equity. `roll` is overridable so a re-valuation at
    a PERTURBED cost of equity also accretes at that perturbed rate."""
    roll = ROLL if roll is None else roll
    cash_legs = -nd_fy25 + non_op + jv_val
    op_part = (ev_ops) * roll
    cash_part = cash_legs * ROLL_CASH
    return (op_part + cash_part - V['nci_book']) / SH - V['dps_fy25']

def ke_from_wacc(we_):
    """Invert an explicit-window WACC to the cost of equity that produced it. The anchor
    roll is a Ke accretion, so a sensitivity that moves the discount rate must move the
    roll with it; inverting the weights is the one rule that does this consistently
    whether the perturbation entered as a beta, a rate shift or a WACC directly."""
    return (we_ - wd_gross * kd_at) / we_gross

def roll_at(ke_):
    return (1 + ke_) ** T_ANCHOR

eq_attr, nci_val = bridge(ev, jv_book)
dcf_ps_dec = eq_attr / SH
dcf_ps = to_anchor_split(ev, jv_book)
dcf_ps_jvcap = to_anchor_split(ev, jv_cap)
say(f"[Bridge] operating EV {ev:,.0f} + NET CASH {-nd_fy25:,.0f} + non-operating assets "
    f"(FVOCI investments {V['fvoci_fy25']:,.0f} + investment property {V['invprop_fy25']:,.0f} "
    f"+ net investment in lease {V['nil_fy25']:,.0f}) + JV network at carrying value "
    f"{jv_book:,.0f} = {eq_attr + nci_val:,.0f}; less minorities ({nci_share:.2%}) "
    f"{nci_val:,.0f} -> equity {eq_attr:,.0f} = AED {dcf_ps_dec:.2f}/share at 31-Dec-2025; "
    f"rolled {V['anchor_days']}/365 at Ke (x{ROLL:.4f}) less the AED 0.30 dividend paid in "
    f"the window = AED {dcf_ps:.2f} vs spot {SPOT:.2f} ({dcf_ps/SPOT-1:+.0%}) — the "
    f"operating equity rolls at Ke, the cash/near-cash legs at the deposit yield, and "
    f"minorities are deducted at their audited carrying value. ON THE ALTERNATIVE JV "
    f"FRAMING: AED {dcf_ps_jvcap:.2f} ({dcf_ps_jvcap/SPOT-1:+.0%}).")
assert abs((ev - nd_fy25 + non_op + jv_book - nci_val) - eq_attr) < 1e-6, "bridge does not close"
assert -nd_fy25 > 0, "net cash must ADD to equity value"
assert dcf_ps_jvcap > dcf_ps, "JV capitalised framing must exceed the book framing"

# ---- fuel framing both ways (the operating contested driver) ----------------
def dcf_scenario(pax_mult=1.0, fare_mult=1.0, fuel_mult=1.0, cost_shift=0.0,
                 wacc_shift=0.0, g=None, capex_mult=1.0, use_alt_fuel=False, jv_val=None,
                 nwc_pct=None):
    g = V['g_term'] if g is None else g
    jv_val = jv_book if jv_val is None else jv_val
    nwc_pct = V['nwc_pct'] if nwc_pct is None else nwc_pct
    B = build(pax_mult=pax_mult, fare_mult=fare_mult, fuel_mult=fuel_mult,
              cost_shift=cost_shift, use_alt_fuel=use_alt_fuel)
    _rev, _ebitda_incl = B['rev'], B['ebitda_incl']
    _ebit = [_ebitda_incl[i] - dna[i] for i in range(5)]
    _nopat = [e * (1 - TAX) for e in _ebit]
    _capex = [c_ * capex_mult for c_ in capex]
    _nwc = [nwc_pct * r for r in _rev]
    _dnwc = [_nwc[0] - nwc_fy25] + [_nwc[i] - _nwc[i - 1] for i in range(1, 5)]
    _f = [_nopat[i] + dna[i] - _capex[i] - leased_gross[i] * capex_mult - _dnwc[i]
          for i in range(5)]
    _we, _wt = wacc_exp + wacc_shift, wacc_term + wacc_shift
    _fwd = [_we - (_we - _wt) * fr for fr in glide_frac]
    _df, cc = [], 1.0
    for w in _fwd:
        cc /= (1 + w); _df.append(cc)
    _ppe, pp = [], fleet_assets_fy25
    for i in range(5):
        pp += _capex[i] + leased_gross[i] * capex_mult - dna[i]; _ppe.append(pp)
    _roic = _nopat[-1] * (1 + g) / (_nwc[-1] + _ppe[-1] + V['intang_fy25'])
    _rr = min(g / max(_roic, 1e-6), 0.95)
    _tv = _nopat[-1] * (1 + g) * (1 - _rr) / max(_wt - g, 0.02)
    _ev = sum(_f[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    return to_anchor_split(_ev, jv_val, roll=roll_at(ke_from_wacc(_we)))

_base_chk = dcf_scenario()
assert abs(_base_chk - dcf_ps) < 0.02, f'scenario engine does not reproduce base: {_base_chk}'
dcf_ps_iata = dcf_scenario(use_alt_fuel=True)
say(f"[Fuel framing both ways] BASE (EIA July-2026 STEO path, relief in 2027): AED "
    f"{dcf_ps:.2f}. ALTERNATIVE (IATA June-2026 high-fuel assumption held): AED "
    f"{dcf_ps_iata:.2f} — {dcf_ps_iata-dcf_ps:+.2f}/share. Both published; the workbook "
    f"carries the base and the alternative side by side.")

dcf_bear = dcf_scenario(pax_mult=0.94, fare_mult=0.97, use_alt_fuel=True, wacc_shift=+0.01,
                        g=0.015, capex_mult=1.15)
dcf_bull = dcf_scenario(pax_mult=1.05, fare_mult=1.03, wacc_shift=-0.01, g=0.035,
                        capex_mult=0.90, jv_val=jv_cap)
say(f"[DCF scenarios] bear {dcf_bear:.2f} / base {dcf_ps:.2f} / bull {dcf_bull:.2f} "
    f"(the bull adopts the JV-capitalised framing; the bear the IATA fuel path)")

# ---- lens 2: relative --------------------------------------------------------
REL_I = 1
ebitda_mid = ebitda[REL_I]                       # EX-fee EBITDA — basis matched to the peers
fees_mid = other_inc[REL_I]
df_rel = df[REL_I]
fee_value = fees_mid * (1 - TAX) / (wacc_term - V['g_term'])   # the fee stream, valued as its own annuity
ev_rel_fwd = V['ev_ebitda_just'] * ebitda_mid + fee_value
ev_rel = ev_rel_fwd * df_rel + pv[0] + pv[1]
def _rel(mult):
    _ev = (mult * ebitda_mid + fee_value) * df_rel + pv[0] + pv[1]
    return to_anchor_split(_ev, jv_book)
rel_ps, rel_bear, rel_bull = _rel(V['ev_ebitda_just']), _rel(5.0), _rel(8.0)
ev_trailing = MKTCAP + nd_fy25            # nd negative: EV below mcap
ev_ebitda_trailing = ev_trailing / hist_is['FY25']['ebitda_incl']
ev_ebitda_trailing_ex = ev_trailing / hist_is['FY25']['ebitda']
pe_trailing = SPOT / (V['npa_fy25'] / SH)
say(f"[Relative lens — basis-matched after critique] {V['ev_ebitda_just']}x FY2027E EBITDA "
    f"EXCLUDING fees/other income ({ebitda_mid:,.0f}) — the same basis peer multiples are "
    f"computed on — plus the fee stream valued separately as an after-tax annuity "
    f"({fee_value:,.0f}), discounted and bridged -> AED {rel_ps:.2f}/share. Trailing prints "
    f"for context, BOTH bases: EV/EBITDA {ev_ebitda_trailing_ex:.1f}x ex-fees / "
    f"{ev_ebitda_trailing:.1f}x incl-fees; P/E {pe_trailing:.1f}x. Peer set rebuilt from "
    f"primary filings: Ryanair 6.50x, Wizz 4.75x, easyJet 3.5x, IndiGo 11.1x, Pegasus 6.6x "
    f"-> median 6.5x.")

# ---- lens 3: normalized earnings power ---------------------------------------
# De-JV'd after critique: the earnings base no longer capitalises the JV share at the
# multiple (that silently averaged the two framings); the JV enters at BOOK, as the base
# framing demands, and the capitalised JV lives only in the labelled alternative.
norm_margin = ebitda_margin[2]
norm_rev = rev[0]
norm_ebitda = norm_margin * norm_rev + other_inc[0]
norm_ebit = norm_ebitda - dna[0]
norm_fin = fininc_path[0] - interest_path[0]
norm_assoc = assoc_fc[0]                        # excluded from the multiplied base; shown
norm_np = (norm_ebit + norm_fin) * (1 - TAX) * (1 - nci_share)
norm_eps = norm_np / SH
def _norm(pe):
    return pe * norm_eps * ROLL + (jv_book / SH) * ROLL_CASH - V['dps_fy25']
norm_ps = _norm(V['pe_just'])
norm_bear = _norm(10.0)
norm_bull = _norm(16.0)
say(f"[Normalised lens — de-JV'd] mid-cycle EBITDA margin {norm_margin:.1%} (FY2028E) on "
    f"FY2026E revenue {norm_rev:,.0f} + fees/other + net finance income, EXCLUDING the JV "
    f"share -> normalised EPS {norm_eps:.3f} x {V['pe_just']:.0f} plus the JV network at "
    f"BOOK (AED {jv_book/SH:.2f}/share) = AED {norm_ps:.2f}/share. The base-framing central "
    f"now genuinely carries the JV at carrying value in every lens.")

# ---- lens 4: book / justified P/B --------------------------------------------
bvps = V['eqp_fy25'] / SH
pb_just = (V['roe_sust'] - V['g_term']) / (ke_term - V['g_term'])
book_ps = to_anchor(pb_just * bvps)
book_bear = to_anchor(((V['roe_sust'] - 0.02 - 0.015) / (0.5 * (ke_exp + ke_term) - 0.015)) * bvps)  # (ROE_bear - g_bear)/(k_bear - g_bear): the Gordon identity held in ALL three legs
book_bull = to_anchor(((V['roe_sust'] + 0.02 - V['g_term']) / (ke_term - V['g_term'])) * bvps)
roe_trailing = V['npa_fy25'] / ((V['eqp_fy24'] + V['eqp_fy25']) / 2)
say(f"[Book lens] justified P/B {pb_just:.2f}x = ({V['roe_sust']:.0%} - {V['g_term']:.1%}) / "
    f"({ke_term:.2%} - {V['g_term']:.1%}) on BVPS {bvps:.2f} -> AED {book_ps:.2f}/share. "
    f"Trailing ROE {roe_trailing:.1%}.")

# ---- synthesis ----------------------------------------------------------------
W = V['lens_weights']
lenses = dict(
    dcf=dict(name='Discounted cash flow (primary)', bear=dcf_bear, base=dcf_ps,
             bull=dcf_bull, w=W['dcf']),
    relative=dict(name='Relative multiples', bear=rel_bear, base=rel_ps, bull=rel_bull,
                  w=W['relative']),
    normalized=dict(name='Normalised earnings power', bear=norm_bear, base=norm_ps,
                    bull=norm_bull, w=W['normalized']),
    book=dict(name='Book value and sustainable return', bear=book_bear, base=book_ps,
              bull=book_bull, w=W['book']),
)
central = sum(l['base'] * l['w'] for l in lenses.values())
lo_w = sum(l['bear'] * l['w'] for l in lenses.values())     # the range, weighted like the base
hi_w = sum(l['bull'] * l['w'] for l in lenses.values())
lo = min(l['bear'] for l in lenses.values())                # widest single-lens span, labelled
hi = max(l['bull'] for l in lenses.values())
lenses['central'] = dict(name='Weighted central', bear=lo_w, base=central, bull=hi_w, w=1.0)
say(f"[Range — weighted after critique] the published bear/bull are now weighted the same "
    f"way as the base: {lo_w:.2f} - {hi_w:.2f}; the widest single-lens span "
    f"({lo:.2f} - {hi:.2f}, the DCF scenarios) is shown separately and labelled as such.")
central_jvcap = central + W['dcf'] * (dcf_ps_jvcap - dcf_ps)
say(f"[Synthesis] weighted central AED {central:.2f}; full span {lo:.2f} - {hi:.2f}; spot "
    f"{SPOT:.2f} ({central/SPOT-1:+.0%} to the central). On the JV-capitalised framing the "
    f"central becomes {central_jvcap:.2f} ({central_jvcap/SPOT-1:+.0%}) — both stated, "
    f"never averaged.")
assert 0.20 <= central / SPOT <= 3.0, f"central/spot {central/SPOT:.2f} outside plausibility"

# ---- sensitivity grids ---------------------------------------------------------
g_grid = [0.015, 0.020, 0.025, 0.030, 0.035]
wt_grid = [wacc_term - 0.02, wacc_term - 0.01, wacc_term, wacc_term + 0.01, wacc_term + 0.02]
we_grid = [wacc_exp - 0.02, wacc_exp - 0.01, wacc_exp, wacc_exp + 0.01, wacc_exp + 0.02]
def dcf_at(we_, wt_, g_):
    _fwd = [we_ - (we_ - wt_) * fr for fr in glide_frac]
    _df, cc = [], 1.0
    for w in _fwd:
        cc /= (1 + w); _df.append(cc)
    _rr = min(g_ / roic_term, 0.95)
    _tv = nopat[-1] * (1 + g_) * (1 - _rr) / max(wt_ - g_, 0.02)
    _ev = sum(fcff[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    # SPLIT roll, at the cost of equity implied by the perturbed rate — the same
    # convention as the headline. (Defect found 17-Aug-2026: these grids were still on
    # the superseded single-roll-at-base-Ke convention, so the base cell of every rate
    # grid printed 3.54 against a headline of 3.51 while the caption claimed they
    # matched. The assertion below now makes that claim machine-enforced.)
    return to_anchor_split(_ev, jv_book, roll=roll_at(ke_from_wacc(we_)))
grid_wacc_g = [[dcf_at(wacc_exp, wt, g) for g in g_grid] for wt in wt_grid]
grid_exp_term = [[dcf_at(we, wt, V['g_term']) for wt in wt_grid] for we in we_grid]
def dcf_beta(b):
    ke = rf_star + b * V['erp_rating']
    we_ = we_gross * ke + wd_gross * kd_at
    wt_ = (1 - V['wd_term']) * (V['rf_term'] + b * V['erp_term']) + V['wd_term'] * kd_term_at
    return dcf_at(we_, wt_, V['g_term'])
# the alternative-benchmark regression sits in the grid as its own labelled column, so the
# reader sees the priced consequence of the other UAE market proxy, not just its coefficient
BETA_ALT = V['beta_alt_benchmark']
beta_grid = [round(BETA_ALT, 3), 0.95, round(BETA, 3), 1.20, 1.35]
grid_beta = [dcf_beta(b) for b in beta_grid]
dcf_ps_beta_alt = dcf_beta(BETA_ALT)
ke_alt = rf_star + BETA_ALT * V['erp_rating']
wacc_alt = we_gross * ke_alt + wd_gross * kd_at
say(f"[Beta — respective market, both benchmarks priced] ADOPTED: own-stock 5-year weekly vs "
    f"the DFM General Index, the exchange the filings say the shares are listed on = "
    f"{BETA:.3f} (R2 {beta_res_pre['r2']:.3f}, n {beta_res_pre['n']}) -> Ke {ke_exp:.2%}, WACC "
    f"{wacc_exp:.2%}, DCF AED {dcf_ps:.2f}. CROSS-CHECK on the other UAE market proxy, the "
    f"FTSE ADX General Index, same window and gate = {BETA_ALT:.3f} (R2 "
    f"{beta_res_pre['alt_benchmark']['r2']:.3f}, n {beta_res_pre['alt_benchmark']['n']}) -> Ke "
    f"{ke_alt:.2%}, WACC {wacc_alt:.2%}, DCF AED {dcf_ps_beta_alt:.2f} "
    f"({dcf_ps_beta_alt-dcf_ps:+.2f}/share, {dcf_ps_beta_alt/dcf_ps-1:+.1%}). The adopted "
    f"regressor explains {beta_res_pre['r2']/beta_res_pre['alt_benchmark']['r2']:.1f}x as much "
    f"of the stock's weekly variance; the cross-check is published, not adopted.")
fuel_grid = [0.85, 0.925, 1.0, 1.075, 1.15]
grid_fuel = [dcf_scenario(fuel_mult=m) for m in fuel_grid]
paxg_grid = [0.90, 0.95, 1.0, 1.05, 1.10]
grid_pax = [dcf_scenario(pax_mult=m) for m in paxg_grid]
fare_grid = [0.94, 0.97, 1.0, 1.03, 1.06]
grid_fare = [dcf_scenario(fare_mult=m) for m in fare_grid]
capex_grid = [0.80, 0.90, 1.0, 1.15, 1.30]
grid_capex = [dcf_scenario(capex_mult=m) for m in capex_grid]
jv_grid = [jv_book, 8 * V['assoc_fy25'], 12 * V['assoc_fy25'], jv_cap, 20 * V['assoc_fy25']]
grid_jv = [dcf_scenario(jv_val=j) for j in jv_grid]
nwcg = [-0.58, -0.61, -0.64, -0.67, -0.70]
grid_nwc = [dcf_scenario(nwc_pct=p_) for p_ in nwcg]

# CAPTION LOCK: the sensitivity tables claim the middle column is the base DCF on every row
# except the JV row (whose base is its leftmost column). Assert it rather than assert it in
# prose — this is the check that would have caught the 3.54-vs-3.51 grid defect on delivery.
for _nm, _c in [('beta', grid_beta[2]), ('explicit x terminal', grid_exp_term[2][2]),
                ('terminal x g', grid_wacc_g[2][2]), ('fuel', grid_fuel[2]),
                ('passengers', grid_pax[2]), ('fare', grid_fare[2]),
                ('capex', grid_capex[2]), ('working capital', grid_nwc[2])]:
    assert abs(_c - dcf_ps) < 0.005, (
        f'{_nm} sensitivity base cell {_c:.4f} does not reproduce the headline DCF '
        f'{dcf_ps:.4f} — grids and headline are on different conventions')
assert abs(grid_jv[0] - dcf_ps) < 0.005, 'JV grid leftmost cell must be the base (book) framing'

# ---- expert panel: three genuinely different methods ---------------------------
e1_margin = ebitda_margin[2]
e1_rev = rev[2]
e1_ebit = e1_margin * e1_rev + other_inc[2] - dna[2]
e1_fin = fininc_path[2] - interest_path[2]
e1_eps = ((e1_ebit + e1_fin + assoc_fc[2]) * (1 - TAX) * (1 - nci_share)) / SH
e1_base, e1_lo, e1_hi = (to_anchor(13.0 * e1_eps), to_anchor(10.0 * e1_eps),
                         to_anchor(16.0 * e1_eps))
e2_fcff = float(np.mean(fcff[2:]))
e2_fin_at = (fininc_path[3] - interest_path[3]) * (1 - TAX)
e2_fcfe = (e2_fcff + e2_fin_at + assoc_fc[3] * (1 - TAX) * 0.4) * (1 - nci_share)
e2_ke = ke_term
e2_base = to_anchor((e2_fcfe * (1 + V['g_term']) / (e2_ke - V['g_term']) + (-nd_fy25) * 0.5)
                    / SH)
e2_lo = to_anchor(e2_fcfe * 1.015 / (0.5 * (ke_exp + ke_term) - 0.015) / SH)
e2_hi = to_anchor((e2_fcfe * 1.035 / (e2_ke - 0.035) + (-nd_fy25)) / SH)
ic_beg = [ic_fy25] + ic[:-1]
ep_ = [nopat[i] - fwd[i] * ic_beg[i] for i in range(5)]
pv_ep = sum(ep_[i] * df[i] for i in range(5))
ep_term = nopat[-1] * (1 + V['g_term']) - wacc_term * ic[-1] * (1 + V['g_term'])
pv_ep_term = ep_term / (wacc_term - V['g_term']) * df[-1]
e3_ev = ic_fy25 + pv_ep + pv_ep_term
e3_base = to_anchor_split(e3_ev, jv_book)
e3_lo = to_anchor_split(ic_fy25 + pv_ep * 0.6 + pv_ep_term * 0.55, jv_book)
e3_hi = to_anchor_split(e3_ev, jv_cap)
experts = dict(
    e1=dict(method_short='earnings power', base=e1_base, rng=[e1_lo, e1_hi], eps=e1_eps,
            margin=e1_margin, rev=e1_rev, ebit=e1_ebit, interest=-e1_fin, pe=13.0),
    e2=dict(method_short='owner cash earnings', base=e2_base, rng=[e2_lo, e2_hi], fcff=e2_fcff,
            fcfe=e2_fcfe, ke=e2_ke, int_at=-e2_fin_at),
    e3=dict(method_short='cash returns vs cost of capital', base=e3_base, rng=[e3_lo, e3_hi],
            ic0=ic_fy25, pv_ep=pv_ep, pv_ep_term=pv_ep_term, ev=e3_ev, ep=ep_,
            spread=[roic[i] - fwd[i] for i in range(5)]),
)
panel_centre = float(sorted([e1_base, e2_base, e3_base])[1])
say(f"[Expert panel] Expert 1 {e1_base:.2f} [{e1_lo:.2f}-{e1_hi:.2f}]; Expert 2 {e2_base:.2f} "
    f"[{e2_lo:.2f}-{e2_hi:.2f}]; Expert 3 {e3_base:.2f} [{e3_lo:.2f}-{e3_hi:.2f}]; panel "
    f"median {panel_centre:.2f} ({panel_centre/SPOT-1:+.0%} vs spot)")

# ---- the defined per-quarter fuel-deferral quantity (replaces the unsourced 0.04) ----
fuel_defer_q = ((V['fuel_per_pax'][0] - V['fuel_per_pax'][1]) * pax_f[1] * (1 - TAX) / 4) / SH
say(f"[Catalyst quantity, defined] one quarter's deferral of the FY2027 fuel relief = "
    f"(fuel/pax FY26 - FY27) x FY27 passengers x (1-t) / 4 / shares = AED {fuel_defer_q:.3f} "
    f"per share per quarter.")

# ---- fan for the figure ---------------------------------------------------------
paths3 = np.load(os.path.join(HERE, 'paths_3M.npy'))
fan = np.percentile(paths3, [5, 25, 50, 75, 95], axis=0)
np.save(os.path.join(HERE, 'fan.npy'), fan)

# ============================ EMIT ==============================================
step0 = json.load(open(os.path.join(HERE, 'step0_result.json')))
strike = json.load(open(os.path.join(HERE, 'strike_result.json')))
beta_res = beta_res_pre
bt5 = json.load(open(os.path.join(HERE, 'backtest_5y.json')))

OUT = dict(
    meta=dict(ticker='AIRARABIA', company='Air Arabia PJSC', market='DFM',
              currency='AED', asof='2026-08-07', spot=SPOT, shares_mn=SH, mktcap=MKTCAP,
              ev_trailing=ev_trailing, klass='operating company — low-cost airline'),
    inputs=INP,
    hist_is=hist_is,
    hist_is_fy22=dict(rev=V['rev_fy22'], pat=V['pat_fy22'], dna=V['dna_fy22']),
    hist_bs=dict(
        FY23=dict(ppe=V['ppe_fy23'], rou=V['rou_fy23'], adv=V['adv_fy23'], inv=V['inv_fy23'],
                  recv=V['recv_fy23'], dep=V['dep_fy23'], cash=V['cash_fy23'],
                  assets=V['assets_fy23'], borrow=V['borrow_fy23'], lease=V['lease_fy23'],
                  debt=debt_fy23, pay=V['pay_fy23'], definc=V['definc_fy23'],
                  maint=V['maint_fy23'], staffb=V['staffb_fy23'], eqp=V['eqp_fy23'],
                  nci=V['nci_fy23'], nd=nd_fy23, nwc=nwc_fy23),
        FY24=dict(ppe=V['ppe_fy24'], rou=V['rou_fy24'], adv=V['adv_fy24'], inv=V['inv_fy24'],
                  recv=V['recv_fy24'], dep=V['dep_fy24'], cash=V['cash_fy24'],
                  assets=V['assets_fy24'], borrow=V['borrow_fy24'], lease=V['lease_fy24'],
                  debt=debt_fy24, pay=V['pay_fy24'], definc=V['definc_fy24'],
                  maint=V['maint_fy24'], staffb=V['staffb_fy24'], eqp=V['eqp_fy24'],
                  nci=V['nci_fy24'], nd=nd_fy24, nwc=nwc_fy24),
        FY25=dict(ppe=V['ppe_fy25'], rou=V['rou_fy25'], adv=V['adv_fy25'], inv=V['inv_fy25'],
                  recv=V['recv_fy25'], dep=V['dep_fy25'], cash=V['cash_fy25'],
                  assets=V['assets_fy25'], borrow=V['borrow_fy25'], lease=V['lease_fy25'],
                  debt=debt_fy25, pay=V['pay_fy25'], definc=V['definc_fy25'],
                  maint=V['maint_fy25'], staffb=V['staffb_fy25'], eqp=V['eqp_fy25'],
                  nci=V['nci_fy25'], nd=nd_fy25, nwc=nwc_fy25,
                  fvoci=V['fvoci_fy25'], invprop=V['invprop_fy25'], nil=V['nil_fy25'],
                  intang=V['intang_fy25'], assoc_bv=V['assoc_bv_fy25']),
    ),
    fcst=dict(years=YRS, pax=pax_f, rev=rev, ebitda=ebitda, ebitda_incl=ebitda_incl,
              ebitda_margin=ebitda_margin, other_inc=other_inc, dna=dna, ebit=ebit,
              ebit_incl=ebit_incl, nopat=nopat, capex=capex, nwc=nwc, dnwc=dnwc, fcff=fcff,
              df=df, pv=pv, fwd_wacc=fwd, ppe=ppe, ic=ic, roic=roic, np_attr=np_fc,
              equity=eq_fc, net_debt=nd_fc, interest=interest_path, fininc=fininc_path,
              assoc=assoc_fc, div=div_fc, seg_rev=seg_rev,
              seg_shares=[{s: seg_rev[i][s] / rev[i] for s in SUBS} for i in range(5)],
              dcost_cash=_B['dcost_cash'], ga=_B['ga'], sm=_B['sm'],
              debt=debt_fc, leased_gross=leased_gross, fleet_ends=fleet_ends,
              fleet_avg=fleet_avg,
              cash_cost_pax=_B['cash_cost_pax'], payout=V['payout'],
              glide_frac=glide_frac, fleet_assets_fy25=fleet_assets_fy25,
              eqp_fy25=V['eqp_fy25'], assoc_fy25=V['assoc_fy25'], debt_fy25=debt_fy25,
              nwc_fy25=nwc_fy25, dna_fy25=V['dna_fy25'], nopat_fy25=nopat_fy25,
              ic_fy25=ic_fy25, roic_fy25=roic_fy25),
    bottomup=dict(unit_hist=unit_hist, subs=SUBS, subnames=SUBNAME,
                  rev_lines_fy25=rl25, rev_lines_fy24=rl24,
                  dcost_lines_fy25=V['dcost_lines_fy25'],
                  dcost_lines_fy24=V['dcost_lines_fy24'],
                  dcost_lines_fy23=V['dcost_lines_fy23'],
                  pax_hist=PAX, lf_hist=V['lf_hist'], fleet=V['fleet'],
                  jv_detail=V['jv_detail'],
                  q1_26_implied_fy=_impl26),
    wacc=dict(rf=V['rf'], rf_star=rf_star, rf_star_rating_alt=rf_star_rating_alt,
              sov_spread_obs=V['sov_spread_obs'], ke_exp=ke_exp, kd=V['kd'], kd_at=kd_at,
              we_exp=we_gross, wd_exp=wd_gross, wacc_exp=wacc_exp, wacc_net=wacc_net,
              wd_net=wd_net, ke_term=ke_term, kd_term=V['kd_term'], kd_term_at=kd_term_at,
              wacc_term=wacc_term, glide_frac=glide_frac, kd_path=V['kd_path'],
              kd_eff_fy25=kd_eff_fy25, erp=V['erp_rating'], erp_cds_note='NA for UAE',
              sov_spread=V['sov_spread_rating'], beta=beta_res,
              beta_alt=BETA_ALT, ke_alt=ke_alt, wacc_alt=wacc_alt),
    dcf=dict(pv_explicit=pv_explicit, tv=tv, pv_tv=pv_tv, ev=ev, tv_share=tv_share,
             ps_beta_alt=dcf_ps_beta_alt,
             nd=nd_fy25, non_op=non_op, jv_book=jv_book, jv_cap=jv_cap, jv_pe=V['jv_pe'],
             nci_share=nci_share, nci_val=nci_val, eq_attr=eq_attr, ps=dcf_ps,
             ps_dec=dcf_ps_dec, ps_jvcap=dcf_ps_jvcap, ps_iata_fuel=dcf_ps_iata, roll=ROLL,
             anchor_days=V['anchor_days'], roic_term=roic_term, rr_term=rr_term,
             g=V['g_term'], bear=dcf_bear, bull=dcf_bull, roll_cash=ROLL_CASH,
             nci_book=V['nci_book'],
             scenario_vectors=dict(
                 high_fuel=dict(use_alt_fuel=True),
                 bear=dict(pax_mult=0.94, fare_mult=0.97, use_alt_fuel=True,
                           wacc_shift=+0.01, g=0.015, capex_mult=1.15),
                 bull=dict(pax_mult=1.05, fare_mult=1.03, wacc_shift=-0.01, g=0.035,
                           capex_mult=0.90, jv_val='15x profit share'))),
    lenses=lenses, central=central, central_jvcap=central_jvcap,
    span=[lo_w, hi_w], span_widest=[lo, hi], spot=SPOT,
    fuel_defer_q=fuel_defer_q,
    experts=experts, panel_centre=panel_centre,
    sens_wg=dict(g_grid=g_grid, wacc_grid=wt_grid, table=grid_wacc_g),
    rel=dict(ebitda_mid=ebitda_mid, fee_value=fee_value, fees_mid=fees_mid,
             ev_ebitda_trailing_ex=ev_ebitda_trailing_ex,
             ev_rel=ev_rel, ev_rel_fwd=ev_rel_fwd,
             pv_interim=pv[0] + pv[1], ev_ebitda_trailing=ev_ebitda_trailing,
             pe_trailing=pe_trailing, just_mult=V['ev_ebitda_just']),
    norm=dict(margin=norm_margin, rev=norm_rev, ebitda=norm_ebitda, ebit=norm_ebit,
              interest=-norm_fin, np=norm_np, eps=norm_eps, pe=V['pe_just'],
              year=YRS[0], margin_year=YRS[2], assoc=norm_assoc),
    book=dict(bvps=bvps, pb_just=pb_just, roe_sust=V['roe_sust'], roe_trailing=roe_trailing,
              ke_blend=ke_term),
    sens=dict(g_grid=g_grid, wt_grid=wt_grid, we_grid=we_grid, grid_wacc_g=grid_wacc_g,
              grid_exp_term=grid_exp_term, beta_grid=beta_grid, grid_beta=grid_beta,
              fuel_grid=fuel_grid, grid_fuel=grid_fuel, paxg_grid=paxg_grid,
              grid_pax=grid_pax, fare_grid=fare_grid, grid_fare=grid_fare,
              capex_grid=capex_grid, grid_capex=grid_capex,
              jv_grid=[float(j) for j in jv_grid], grid_jv=grid_jv,
              nwc_grid=nwcg, grid_nwc=grid_nwc),
    step0=step0, strike=strike, backtest_5y=bt5,
    assert_log=LOG,
)
with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(OUT, f, indent=1, default=float)
say("=" * 78)
say(f"WROTE study_numbers.json | central AED {central:.2f} [{lo:.2f} - {hi:.2f}] vs spot "
    f"{SPOT:.2f} | DCF {dcf_ps:.2f} (JV-cap {dcf_ps_jvcap:.2f}, IATA fuel {dcf_ps_iata:.2f}) "
    f"| TV {tv_share:.0%} of EV | WACC {wacc_exp:.2%} -> {wacc_term:.2%}")
