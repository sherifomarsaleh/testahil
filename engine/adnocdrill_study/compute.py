"""ADNOC Drilling Company P.J.S.C. (ADX: ADNOCDRILL) — master computation.

Writes study_numbers.json, the single source of truth every builder reads. No
financial numeral is typed into a builder; a builder that needs a number reads
it from here.

CODE-FIRST RULE. Every INPUT is a four-field record {value, source, date, ring}.
A bare numeral cannot enter the model. The ASSERT block at the end raises (and
no JSON is emitted) unless the EV-to-equity bridge closes, the discount-rate
glide is ordered, the cost-of-debt integrity triple holds, the terminal block is
return-on-capital consistent, and every historical statement ties to the filing
it was read from.

SOURCE DISCIPLINE. Every historical income-statement, balance-sheet and
cash-flow figure below is read from ADNOC Drilling's own signed consolidated
financial statements, downloaded from the company's investor-relations site:

  FY2023  audited, KPMG Lower Gulf Limited, unqualified — signed 12 Feb 2024
  FY2024  audited, Deloitte & Touche (M.E.), unqualified — signed 11 Feb 2025
  FY2025  audited, Deloitte & Touche (M.E.), unqualified — signed 11 Feb 2026
  Q1-2026 and 1H-2026 condensed interim, reviewed

FY2023 and FY2024 are each cross-confirmed against the following year's filing
comparative column and tie to the dollar. Operating unit data (rig counts, wells
drilled, availability, integrated-drilling-services rig counts, unconventional
revenue) comes from the company's own quarterly management discussion and
analysis and earnings presentations, which are the only published source for
those units — no financial statement carries them.

Company class: operating company. An asset-heavy contract driller (onshore and
offshore rigs) with an integrated oilfield-services arm. Three reported
segments, no inter-segment sales, one customer group. Lens set follows the
operating-company reference: FCFF discounted cash flow primary, plus relative
multiples, normalised earnings power, and a book-value / return-on-capital lens.

Reporting currency is USD (the group's functional and presentation currency per
Note 2 of the audited statements). The shares trade in AED on the Abu Dhabi
Securities Exchange. The valuation runs in USD and converts to AED at the peg.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np

# ============================ INPUT RECORD ===================================
REGISTER = []


def I(value, source, date, ring):
    rec = dict(value=value, source=source, date=date, ring=ring)
    REGISTER.append(rec)
    return rec


FS23 = "FY2023 audited consolidated financial statements (KPMG Lower Gulf Limited, unqualified)"
FS24 = "FY2024 audited consolidated financial statements (Deloitte & Touche (M.E.), unqualified)"
FS25 = "FY2025 audited consolidated financial statements (Deloitte & Touche (M.E.), unqualified)"
IH26 = "1H-2026 condensed consolidated interim financial information (reviewed)"
MDA24 = "FY2024 management discussion and analysis"
MDA25 = "FY2025 management discussion and analysis"
MDA26 = "1H-2026 management discussion and analysis"
PR26 = "1H-2026 earnings press release"

INP = dict(
    # ---------------- market anchors ----------------------------------------
    spot_aed=I(5.94, "Uploaded ADX daily price history for ADNOCDRILL, last close 07-Aug-2026",
               "2026-08-07", "Market"),
    fx_aed_usd=I(3.6725, "AED/USD central-bank peg, unchanged since 1997; the rate at which the "
                 "company itself translates its AED-declared dividends into the USD amounts "
                 "disclosed in Note 24 of the audited statements", "2026-08-07", "Country"),
    shares_issued_k=I(16_000_000.0, "Share capital note 13, FY2025 audited statements: 16,000,000 "
                      "thousand shares of AED 0.10 each, unchanged since listing", "2026-02-11",
                      "Company"),
    treasury_shares_k=I(7_349.0, "Note 14, 1H-2026 interim: the appointed market maker held 7,349 "
                        "thousand shares on the company's behalf at 30 June 2026, classified as "
                        "treasury shares in equity (31 Dec 2025: 9,279 thousand)", "2026-06-30",
                        "Company"),

    # ---------------- historical income statement (USD '000, consolidated) ---
    rev_fy23=I(3_056_865.0, f"Consolidated statement of profit or loss, {FS23} (confirmed to the "
               f"dollar by the FY2024 filing's comparative column)", "2024-02-12", "Company"),
    rev_fy24=I(4_034_222.0, f"Consolidated statement of profit or loss, {FS24} (confirmed to the "
               f"dollar by the FY2025 filing's comparative column)", "2025-02-11", "Company"),
    rev_fy25=I(4_902_886.0, f"Consolidated statement of profit or loss, {FS25}", "2026-02-11",
               "Company"),
    dcost_fy23=I(1_848_729.0, f"Direct cost, {FS23}", "2024-02-12", "Company"),
    dcost_fy24=I(2_337_407.0, f"Direct cost, {FS24}", "2025-02-11", "Company"),
    dcost_fy25=I(3_105_963.0, f"Direct cost, {FS25}", "2026-02-11", "Company"),
    gna_fy23=I(126_334.0, f"General and administrative expenses, {FS23}", "2024-02-12", "Company"),
    gna_fy24=I(155_358.0, f"General and administrative expenses, {FS24}", "2025-02-11", "Company"),
    gna_fy25=I(167_197.0, f"General and administrative expenses, {FS25}", "2026-02-11", "Company"),
    othinc_fy23=I(9_847.0, f"Other income - net, {FS23}", "2024-02-12", "Company"),
    othinc_fy24=I(6_388.0, f"Other income - net, {FS24}", "2025-02-11", "Company"),
    othinc_fy25=I(26_991.0, f"Other income - net, {FS25}", "2026-02-11", "Company"),
    jv_fy23=I(0.0, f"Share of results of joint ventures, {FS23} — the joint ventures did not exist "
              f"in FY2023; the first investment was made in FY2024", "2024-02-12", "Company"),
    jv_fy24=I(8_490.0, f"Share of results of joint ventures, {FS24}", "2025-02-11", "Company"),
    jv_fy25=I(29_000.0, f"Share of results of joint ventures, {FS25}", "2026-02-11", "Company"),
    fincost_fy23=I(74_577.0, f"Finance cost, {FS23} (the FY2023 face presents finance cost net of "
                   f"income; the gross figures are in the cash-flow statement adjustments)",
                   "2024-02-12", "Company"),
    fincost_fy24=I(135_995.0, f"Finance cost, {FS24}", "2025-02-11", "Company"),
    fincost_fy25=I(109_463.0, f"Finance cost note 23, {FS25}: interest on loans 108,839 plus lease "
                   f"interest 624", "2026-02-11", "Company"),
    finincome_fy23=I(15_727.0, f"Finance income, {FS23}", "2024-02-12", "Company"),
    finincome_fy24=I(11_736.0, f"Finance income, {FS24}", "2025-02-11", "Company"),
    finincome_fy25=I(11_626.0, f"Finance income, {FS25}", "2026-02-11", "Company"),
    tax_fy23=I(0.0, f"Income tax, {FS23} — the Abu Dhabi fiscal arrangement took effect 1 January "
               f"2024, so FY2023 carries no corporate income tax charge", "2024-02-12", "Company"),
    tax_fy24=I(128_510.0, f"Income tax note 30, {FS24}", "2025-02-11", "Company"),
    tax_fy25=I(139_099.0, f"Income tax note 30, {FS25}: current 138,930 plus deferred 169",
               "2026-02-11", "Company"),
    pat_fy23=I(1_032_799.0, f"Profit for the year, {FS23}", "2024-02-12", "Company"),
    pat_fy24=I(1_303_566.0, f"Profit after tax, {FS24}", "2025-02-11", "Company"),
    pat_fy25=I(1_448_781.0, f"Profit after tax, {FS25}", "2026-02-11", "Company"),

    # depreciation and amortisation, from the cash-flow statement adjustments
    dna_fy23=I(391_247.0, f"Consolidated statement of cash flows, {FS23}: property and equipment "
               f"368,110 + right-of-use assets 19,589 + intangibles 3,548. Ties to the segment "
               f"note's total depreciation of 391,247", "2024-02-12", "Company"),
    dna_fy24=I(458_452.0, f"Consolidated statement of cash flows, {FS24}: property and equipment "
               f"426,473 + right-of-use assets 28,435 + intangibles 3,544. Ties to the segment "
               f"note's total depreciation and amortisation of 458,452", "2025-02-11", "Company"),
    dna_fy25=I(512_319.0, f"Consolidated statement of cash flows, {FS25}: property and equipment "
               f"497,084 + right-of-use assets 11,042 + intangibles 4,193. Ties to the segment "
               f"note's total depreciation and amortisation of 512,319", "2026-02-11", "Company"),

    # ---------------- segment revenue (USD '000) -----------------------------
    seg_on_fy23=I(1_495_057.0, f"Segment note 26, {FS23} — Onshore", "2024-02-12", "Company"),
    seg_off_fy23=I(1_008_805.0, f"Segment note 26, {FS23} — Offshore Jackup 799,726 plus Offshore "
                   f"Island 209,079. The two were reported separately until FY2024 and combined "
                   f"into a single Offshore segment from 1Q-2025; they are summed here so the "
                   f"three-year series is on one basis", "2024-02-12", "Company"),
    seg_ofs_fy23=I(553_003.0, f"Segment note 26, {FS23} — Oilfield Services", "2024-02-12",
                   "Company"),
    seg_on_fy24=I(1_892_670.0, f"Segment note 28, {FS25} comparative column — Onshore",
                  "2026-02-11", "Company"),
    seg_off_fy24=I(1_328_436.0, f"Segment note 28, {FS25} comparative column — Offshore",
                   "2026-02-11", "Company"),
    seg_ofs_fy24=I(813_116.0, f"Segment note 28, {FS25} comparative column — Oilfield Services",
                   "2026-02-11", "Company"),
    seg_on_fy25=I(2_037_025.0, f"Segment note 28, {FS25} — Onshore", "2026-02-11", "Company"),
    seg_off_fy25=I(1_403_893.0, f"Segment note 28, {FS25} — Offshore", "2026-02-11", "Company"),
    seg_ofs_fy25=I(1_461_968.0, f"Segment note 28, {FS25} — Oilfield Services", "2026-02-11",
                   "Company"),
    seg_ebitda_on_fy25=I(994_477.0, f"Segment note 28, {FS25} — Onshore EBITDA", "2026-02-11",
                         "Company"),
    seg_ebitda_off_fy25=I(952_523.0, f"Segment note 28, {FS25} — Offshore EBITDA", "2026-02-11",
                          "Company"),
    seg_ebitda_ofs_fy25=I(251_036.0, f"Segment note 28, {FS25} — Oilfield Services EBITDA",
                          "2026-02-11", "Company"),

    # ---------------- direct-cost stack, FY2025 (USD '000) -------------------
    dc_repairs_fy25=I(904_937.0, f"Direct cost note 20, {FS25} — repairs and maintenance",
                      "2026-02-11", "Company"),
    dc_staff_fy25=I(802_536.0, f"Direct cost note 20, {FS25} — staff costs", "2026-02-11",
                    "Company"),
    dc_hire_fy25=I(303_652.0, f"Direct cost note 20, {FS25} — hire of equipment", "2026-02-11",
                   "Company"),
    dc_chem_fy25=I(254_535.0, f"Direct cost note 20, {FS25} — chemicals", "2026-02-11", "Company"),
    dc_fuel_fy25=I(170_776.0, f"Direct cost note 20, {FS25} — fuel and lubricants", "2026-02-11",
                   "Company"),
    dc_majmaint_fy25=I(53_151.0, f"Direct cost note 20, {FS25} — major maintenance charges",
                       "2026-02-11", "Company"),
    dc_other_fy25=I(123_312.0, f"Direct cost note 20, {FS25} — other direct cost", "2026-02-11",
                    "Company"),
    dc_dep_fy25=I(493_064.0, f"Direct cost note 20, {FS25} — depreciation of property and "
                  f"equipment charged to direct cost", "2026-02-11", "Company"),
    gna_dep_fy25=I(19_255.0, f"Segment note 28, {FS25} — depreciation and amortisation included "
                   f"in general and administrative expenses. Ties to note 21: property and "
                   f"equipment 4,020 plus right-of-use 11,042 plus intangibles 4,193",
                   "2026-02-11", "Company"),

    # ---------------- historical balance sheet (USD '000) --------------------
    ppe_fy23=I(4_847_540.0, f"Consolidated statement of financial position, {FS23}", "2024-02-12",
               "Company"),
    ppe_fy24=I(5_352_674.0, f"Consolidated statement of financial position, {FS24}", "2025-02-11",
               "Company"),
    ppe_fy25=I(5_477_158.0, f"Consolidated statement of financial position, {FS25}", "2026-02-11",
               "Company"),
    rou_fy23=I(173_911.0, f"Right-of-use assets, {FS23}", "2024-02-12", "Company"),
    rou_fy24=I(23_310.0, f"Right-of-use assets, {FS24}", "2025-02-11", "Company"),
    rou_fy25=I(45_729.0, f"Right-of-use assets, {FS25}", "2026-02-11", "Company"),
    intang_fy23=I(5_432.0, f"Intangible assets, {FS23}", "2024-02-12", "Company"),
    intang_fy24=I(5_301.0, f"Intangible assets, {FS24}", "2025-02-11", "Company"),
    intang_fy25=I(10_769.0, f"Intangible assets, {FS25}", "2026-02-11", "Company"),
    jvinv_fy23=I(0.0, f"Investment in joint ventures, {FS23} — none held", "2024-02-12", "Company"),
    jvinv_fy24=I(275_240.0, f"Investment in joint ventures, {FS24}", "2025-02-11", "Company"),
    jvinv_fy25=I(437_090.0, f"Investment in joint ventures, {FS25}", "2026-02-11", "Company"),
    dta_fy23=I(0.0, f"Deferred tax assets, {FS23} — none recognised", "2024-02-12", "Company"),
    dta_fy24=I(1_397.0, f"Deferred tax assets, {FS24}", "2025-02-11", "Company"),
    dta_fy25=I(1_228.0, f"Deferred tax assets, {FS25}", "2026-02-11", "Company"),
    advnc_fy23=I(1_654.0, f"Advances (non-current), {FS23}", "2024-02-12", "Company"),
    advnc_fy24=I(2_230.0, f"Advances (non-current), {FS24}", "2025-02-11", "Company"),
    advnc_fy25=I(8_292.0, f"Advances (non-current), {FS25}", "2026-02-11", "Company"),
    # Carried as its own line rather than inside advances, because it is not an
    # advance that stays on the balance sheet: it is consideration already paid
    # for SLDC, and in 2026 it converts into the acquired assets. The forecast
    # roll-forward releases exactly this figure, read from here.
    advacq_fy25=I(90_926.0, f"Advance for acquisition of a subsidiary, {FS25}. Nil at 31 December "
                  f"2024 and nil again at 30 June 2026, when the SLDC acquisition completed",
                  "2026-02-11", "Company"),
    advacq_fy23=I(0.0, f"No advance for acquisition of a subsidiary is presented in {FS23}",
                  "2024-02-12", "Company"),
    advacq_fy24=I(0.0, f"No advance for acquisition of a subsidiary is presented in {FS24}",
                  "2025-02-11", "Company"),
    inv_fy23=I(206_107.0, f"Inventories, {FS23}", "2024-02-12", "Company"),
    inv_fy24=I(223_083.0, f"Inventories, {FS24}", "2025-02-11", "Company"),
    inv_fy25=I(279_030.0, f"Inventories, {FS25}", "2026-02-11", "Company"),
    tr_fy23=I(153_946.0, f"Trade and other receivables, {FS23}", "2024-02-12", "Company"),
    tr_fy24=I(185_958.0, f"Trade and other receivables, {FS24}", "2025-02-11", "Company"),
    tr_fy25=I(150_376.0, f"Trade and other receivables, {FS25}", "2026-02-11", "Company"),
    dfrp_fy23=I(986_696.0, f"Due from related parties, {FS23}", "2024-02-12", "Company"),
    dfrp_fy24=I(1_361_282.0, f"Due from related parties, {FS24}", "2025-02-11", "Company"),
    dfrp_fy25=I(1_364_794.0, f"Due from related parties note 18, {FS25} — 228,666 billed plus "
                f"1,164,132 of unbilled contract assets less a 28,004 expected-credit-loss "
                f"allowance", "2026-02-11", "Company"),
    cash_fy23=I(354_122.0, f"Cash and cash equivalents, {FS23}", "2024-02-12", "Company"),
    cash_fy24=I(330_288.0, f"Cash and cash equivalents, {FS24}", "2025-02-11", "Company"),
    cash_fy25=I(236_016.0, f"Cash and cash equivalents, {FS25}", "2026-02-11", "Company"),
    afs_fy23=I(10_717.0, f"Assets held for sale, {FS23}", "2024-02-12", "Company"),
    afs_fy24=I(5_708.0, f"Assets held for sale, {FS24}", "2025-02-11", "Company"),
    afs_fy25=I(0.0, f"Assets held for sale, {FS25} — nil at year end", "2026-02-11", "Company"),
    debt_fy23=I(1_992_264.0, f"Borrowings note 13, {FS23} (non-current 1,992,264, current nil)",
                "2024-02-12", "Company"),
    debt_fy24=I(2_294_750.0, f"Borrowings note 15, {FS24}: non-current 1,495,227 plus current "
                f"799,523", "2025-02-11", "Company"),
    debt_fy25=I(2_269_039.0, f"Borrowings note 15, {FS25}: non-current 1,246,507 plus current "
                f"1,022,532", "2026-02-11", "Company"),
    lease_fy23=I(189_211.0, f"Lease liabilities, {FS23}: non-current 152,378 plus current 36,833",
                 "2024-02-12", "Company"),
    lease_fy24=I(25_157.0, f"Lease liabilities, {FS24}: non-current 12,027 plus current 13,130",
                 "2025-02-11", "Company"),
    lease_fy25=I(47_581.0, f"Lease liabilities, {FS25}: non-current 35,855 plus current 11,726",
                 "2026-02-11", "Company"),
    tp_fy23=I(929_770.0, f"Trade and other payables, {FS23}: non-current 80,936 plus current "
              f"848,834", "2024-02-12", "Company"),
    tp_fy24=I(1_240_598.0, f"Trade and other payables note 17, {FS24}: non-current 64,849 plus "
              f"current 1,175,749", "2025-02-11", "Company"),
    tp_fy25=I(1_114_818.0, f"Trade and other payables note 17, {FS25}: non-current 75,399 plus "
              f"current 1,039,419", "2026-02-11", "Company"),
    dtrp_fy23=I(250_237.0, f"Due to related parties, {FS23}", "2024-02-12", "Company"),
    dtrp_fy24=I(250_850.0, f"Due to related parties, {FS24}", "2025-02-11", "Company"),
    dtrp_fy25=I(416_071.0, f"Due to related parties note 18, {FS25}", "2026-02-11", "Company"),
    eosb_fy23=I(114_422.0, f"Provision for employees' end of service benefits, {FS23}: non-current "
                f"105,328 plus current 9,094", "2024-02-12", "Company"),
    eosb_fy24=I(129_947.0, f"Provision for employees' end of service benefits note 16, {FS24}",
                "2025-02-11", "Company"),
    eosb_fy25=I(143_587.0, f"Provision for employees' end of service benefits note 16, {FS25}",
                "2026-02-11", "Company"),
    taxpay_fy23=I(0.0, f"Income tax payable, {FS23} — nil", "2024-02-12", "Company"),
    taxpay_fy24=I(15_000.0, f"Income tax payable, {FS24}", "2025-02-11", "Company"),
    taxpay_fy25=I(11_000.0, f"Income tax payable, {FS25}", "2026-02-11", "Company"),
    equity_fy23=I(3_264_221.0, f"Total equity, {FS23}", "2024-02-12", "Company"),
    equity_fy24=I(3_810_169.0, f"Total equity, {FS24}", "2025-02-11", "Company"),
    equity_fy25=I(4_099_312.0, f"Total equity, {FS25}", "2026-02-11", "Company"),
    ta_fy23=I(6_740_125.0, f"Total assets, {FS23}", "2024-02-12", "Company"),
    ta_fy24=I(7_766_471.0, f"Total assets, {FS24}", "2025-02-11", "Company"),
    ta_fy25=I(8_101_408.0, f"Total assets, {FS25}", "2026-02-11", "Company"),

    # ---------------- historical cash flow (USD '000) ------------------------
    capex_fy23=I(1_062_274.0, f"Payments for purchase of property and equipment, {FS23}",
                 "2024-02-12", "Company"),
    capex_fy24=I(761_822.0, f"Purchase of property and equipment 758,409 plus intangibles 3,413, "
                 f"{FS24}", "2025-02-11", "Company"),
    capex_fy25=I(814_876.0, f"Purchase of property and equipment 805,215 plus intangibles 9,661, "
                 f"{FS25}", "2026-02-11", "Company"),
    cfo_fy23=I(1_355_056.0, f"Net cash from operating activities, {FS23}", "2024-02-12", "Company"),
    cfo_fy24=I(1_653_666.0, f"Net cash from operating activities, {FS24}", "2025-02-11", "Company"),
    cfo_fy25=I(2_225_843.0, f"Net cash from operating activities, {FS25}", "2026-02-11", "Company"),
    div_fy23=I(699_559.0, f"Dividends paid, {FS23}", "2024-02-12", "Company"),
    div_fy24=I(752_452.0, f"Dividends paid, {FS24}", "2025-02-11", "Company"),
    div_fy25=I(1_143_567.0, f"Dividends paid, {FS25}", "2026-02-11", "Company"),

    # ---------------- 1H-2026 interim (USD '000) -----------------------------
    rev_1h26=I(2_459_813.0, f"Revenue, {IH26}", "2026-07-30", "Company"),
    ebitda_1h26=I(1_084_000.0, f"EBITDA, {MDA26} financial summary. Reconciles to the interim "
                  f"statements: revenue 2,459,813 less direct cost 1,566,479 less general and "
                  f"administrative 90,356 plus joint-venture share 16,479 plus other income 3,807 "
                  f"= 823,264 before adding back the 260,530 of depreciation and amortisation "
                  f"inside cost of sales and overheads", "2026-07-30", "Company"),
    pat_1h26=I(705_545.0, f"Profit after tax, {IH26}", "2026-07-30", "Company"),
    dna_1h26=I(260_530.0, f"Cash-flow statement adjustments, {IH26}: property and equipment "
               f"252,319 plus right-of-use 5,906 plus intangibles 2,305", "2026-07-30", "Company"),
    ppe_1h26=I(5_705_373.0, f"Property and equipment, {IH26}", "2026-06-30", "Company"),
    debt_1h26=I(2_468_779.0, f"Borrowings, {IH26}: non-current 1,247,510 plus current 1,221,269",
                "2026-06-30", "Company"),
    cash_1h26=I(355_423.0, f"Cash and cash equivalents, {IH26}", "2026-06-30", "Company"),
    lease_1h26=I(45_183.0, f"Lease liabilities, {IH26}: non-current 28,206 plus current 16,977",
                 "2026-06-30", "Company"),
    jvinv_1h26=I(461_729.0, f"Investment in joint ventures, {IH26}", "2026-06-30", "Company"),
    nci_1h26=I(53_594.0, f"Non-controlling interests, {IH26} — arising on the SLDC and MBPS "
               f"acquisitions completed in the period", "2026-06-30", "Company"),
    equity_1h26=I(4_287_313.0, f"Total equity, {IH26}", "2026-06-30", "Company"),
    finliab_1h26=I(62_530.0, f"Financial liability, {IH26} note 5 — the put obligation recognised "
                   f"over the non-controlling interests in the acquired regional businesses",
                   "2026-06-30", "Company"),

    # --- the 30-Jun-2026 working-capital lines ------------------------------
    # These carry the forecast working-capital ratio. The 30-Jun-2026 balance
    # sheet is the ONLY one that consolidates the two acquired regional
    # businesses, so it is the only basis on which a ratio can be set for a
    # revenue line that likewise consolidates them.
    ebitda_1h25=I(1_078_000.0, f"{MDA26} financial summary, 1H-2025 comparative column — group "
                  f"EBITDA of $1,078 million", "2026-07-30", "Company/IR"),
    jv_1h26=I(16_479.0, f"Share of results of joint ventures, {IH26} statement of cash flows",
              "2026-06-30", "Company"),
    jv_1h25=I(14_000.0, f"Share of results of joint ventures, {IH26} statement of cash flows, "
              f"1H-2025 comparative column", "2026-06-30", "Company"),
    cfo_1h26=I(843_049.0, f"Net cash generated from operating activities, {IH26}. Stated after "
               f"income tax and end-of-service benefits paid and BEFORE finance cost paid, which "
               f"this company presents inside financing — so the figure is already unlevered",
               "2026-06-30", "Company"),
    capex_1h26=I(189_878.0, f"Payments for purchase of property and equipment, {IH26}",
                 "2026-06-30", "Company"),
    days_jun26_to_anchor=I(38.0, "Calendar days from 30 June 2026, the date the bridge is struck "
                           "on, to the 7 August 2026 price anchor", "2026-08-07", "Market"),
    inv_1h26=I(342_783.0, f"Inventories, {IH26}", "2026-06-30", "Company"),
    recv_1h26=I(233_060.0, f"Trade and other receivables, {IH26}", "2026-06-30", "Company"),
    dfrp_1h26=I(1_418_236.0, f"Due from related parties, {IH26}", "2026-06-30", "Company"),
    tp_1h26=I(1_238_037.0, f"Trade and other payables, {IH26}: non-current 40,533 plus current "
              f"1,197,504", "2026-06-30", "Company"),
    dtrp_1h26=I(312_862.0, f"Due to related parties, {IH26}", "2026-06-30", "Company"),
    # The 1H-2025 comparative movements in the same statement of cash flows are
    # what rule OUT a seasonal reading of the ratio: over 1H-2025 working capital
    # RELEASED cash, so a mid-year balance sheet runs BELOW the year end for this
    # company rather than above it. The 1H-2026 build is therefore real.
    wc_move_1h25=I(154_080.0, f"{IH26} statement of cash flows, 1H-2025 comparative column — "
                   f"inventories (6,132), receivables (3,671), due from related parties (57,523), "
                   f"payables 58,261, due to related parties 163,145; a net RELEASE of working "
                   f"capital of 154,080 over the first half of 2025", "2026-07-30", "Company"),
    wc_move_1h26=I(-172_636.0, f"{IH26} statement of cash flows — inventories (50,645), "
                   f"receivables (2,127), due from related parties (53,442), payables 36,787, "
                   f"due to related parties (103,209); a net ABSORPTION of 172,636 over the first "
                   f"half of 2026, before the working capital that arrived with the acquisitions",
                   "2026-07-30", "Company"),

    # ---------------- operating units (from the company's own MD&A) ----------
    rigs_onshore_fy22=I(74.0, "FY2023 MD&A operational highlights, FY22 comparative column — "
                        "onshore rigs at year end", "2024-02-12", "Company/IR"),
    rigs_onshore_fy23=I(84.0, "FY2023 MD&A operational highlights — onshore rigs at year end "
                        "(includes 4 lease-to-own land rigs)", "2024-02-12", "Company/IR"),
    rigs_onshore_fy24=I(95.0, "FY2024 MD&A operational highlights — onshore rigs at year end",
                        "2025-02-11", "Company/IR"),
    rigs_onshore_fy25=I(92.0, f"{MDA25} operational highlights — Abu Dhabi onshore rigs at year "
                        f"end", "2026-02-11", "Company/IR"),
    rigs_jackup_fy22=I(31.0, "FY2023 MD&A, FY22 comparative — offshore jack-up rigs",
                       "2024-02-12", "Company/IR"),
    rigs_jackup_fy23=I(35.0, "FY2023 MD&A — offshore jack-up rigs at year end", "2024-02-12",
                       "Company/IR"),
    rigs_jackup_fy24=I(37.0, "FY2024 MD&A — offshore jack-up rigs at year end", "2025-02-11",
                       "Company/IR"),
    rigs_jackup_fy25=I(36.0, f"{MDA25} — offshore jack-up rigs at year end", "2026-02-11",
                       "Company/IR"),
    rigs_island_fy22=I(10.0, "FY2023 MD&A, FY22 comparative — offshore island rigs", "2024-02-12",
                       "Company/IR"),
    rigs_island_fy23=I(10.0, "FY2023 MD&A — offshore island rigs at year end", "2024-02-12",
                       "Company/IR"),
    rigs_island_fy24=I(10.0, "FY2024 MD&A — offshore island rigs at year end", "2025-02-11",
                       "Company/IR"),
    rigs_island_fy25=I(12.0, f"{MDA25} — offshore island rigs at year end", "2026-02-11",
                       "Company/IR"),
    ids_fy23=I(48.0, "FY2023 MD&A — integrated-drilling-services rigs at year end (2022: 40)",
               "2024-02-12", "Company/IR"),
    ids_fy24=I(57.0, "FY2024 MD&A — integrated-drilling-services rigs at year end", "2025-02-11",
               "Company/IR"),
    ids_fy25=I(60.0, f"{MDA25} — integrated-drilling-services rigs at year end", "2026-02-11",
               "Company/IR"),
    rigs_island_2q26=I(13.0, f"{MDA26}: 'One additional AI-enabled Island rig entered the domestic "
                       f"fleet during the second quarter, ahead of schedule' — 12 at 31 December "
                       f"2025 plus one", "2026-07-30", "Company/IR"),
    ids_2q26=I(61.0, f"{MDA26} — integrated-drilling-services rigs at 30 June 2026", "2026-07-30",
               "Company/IR"),
    # --- the SECOND oilfield-services volume driver, added 17-Aug-2026 --------
    # The segment serves two distinct books: rigs under a full integrated-drilling
    # contract, and rigs taking at least one discrete service. Only the first was
    # modelled before; the company discloses both, and the second is the larger
    # count in 2025.
    discrete_fy24=I(48.0, "FY2024 MD&A: 'offered at least one discrete service to an additional 48 "
                    "rigs between onshore and offshore'", "2025-02-11", "Company/IR"),
    discrete_fy25=I(58.0, f"{MDA25}: 'The segment offered at least one discrete service to an "
                    f"additional 58 rigs between onshore and offshore in the fourth quarter. All "
                    f"in all, oilfield services are offered to 118 rigs'", "2026-02-11",
                    "Company/IR"),
    discrete_2q26=I(53.0, f"{MDA26}: 'at least one discrete service was delivered across an "
                    f"additional 53 rigs... resulting in OFS coverage across a total of 114 rigs'",
                    "2026-07-30", "Company/IR"),

    # --- the two 2026 business combinations, from Note 5 of the interim ------
    # Every figure below is the sum of the two acquisition tables. Two independent
    # cross-checks tie exactly: goodwill 16,830 equals the goodwill line on the
    # face of the 30-Jun-2026 balance sheet, and the minority interests of 49,931
    # equal the 'Acquisition of non-controlling interest' line in the statement of
    # changes in equity.
    acq_ppe=I(282_531.0, f"Note 5, {IH26} — property and equipment acquired: SLDC 138,622 plus "
              f"MBPS 143,909", "2026-06-30", "Company"),
    acq_rou=I(10_037.0, f"Note 5, {IH26} — right-of-use assets acquired (MBPS)", "2026-06-30",
              "Company"),
    acq_goodwill=I(16_830.0, f"Note 5, {IH26} — provisional goodwill: SLDC 7,029 plus MBPS 9,801. "
                   f"Ties exactly to the goodwill line on the face of the balance sheet",
                   "2026-06-30", "Company"),
    acq_inventories=I(13_590.0, f"Note 5, {IH26} — inventories acquired: 3,348 plus 10,242",
                      "2026-06-30", "Company"),
    acq_receivables=I(80_557.0, f"Note 5, {IH26} — trade and other receivables acquired: 11,531 "
                      f"plus 69,026", "2026-06-30", "Company"),
    acq_payables=I(53_013.0, f"Note 5, {IH26} — trade and other payables assumed: 13,094 plus "
                   f"39,919", "2026-06-30", "Company"),
    acq_cash=I(42_683.0, f"Note 5, {IH26} — cash acquired: 4,086 plus 38,597", "2026-06-30",
               "Company"),
    acq_borrowings=I(172_931.0, f"Note 5, {IH26} — term loans, overdraft and borrowings assumed "
                     f"with MBPS", "2026-06-30", "Company"),
    acq_leases=I(6_717.0, f"Note 5, {IH26} — lease liabilities assumed with MBPS", "2026-06-30",
                 "Company"),
    acq_nci=I(49_931.0, f"Note 5, {IH26} — minority interests recognised on acquisition: 40,559 "
              f"plus 9,372. Ties exactly to the statement of changes in equity", "2026-06-30",
              "Company"),
    acq_consideration_2026=I(47_287.0, f"Note 5, {IH26} — MBPS total purchase consideration, paid "
                             f"in cash in the period per that acquisition's own analysis of "
                             f"cash flows", "2026-06-30", "Company"),
    acq_deferred_tax=I(4_697.0, f"Note 5, {IH26} — deferred tax liability assumed with SLDC. Ties "
                       f"to the new 'deferred tax liability' line on the face of the 30-Jun-2026 "
                       f"balance sheet, which was nil at 31-Dec-2025", "2026-06-30", "Company"),
    acq_income_tax=I(7_293.0, f"Note 5, {IH26} — income tax payable assumed: SLDC 4,600 plus MBPS "
                     f"2,693", "2026-06-30", "Company"),
    acq_eosb=I(2_693.0, f"Note 5, {IH26} — provision for employees' end of service benefits "
               f"assumed with MBPS", "2026-06-30", "Company"),
    acq_contingent=I(20_372.0, f"Note 5, {IH26} — contingent consideration inside SLDC's purchase "
                     f"consideration, at fair value at the acquisition date, payable over three "
                     f"years against EBITDA-based performance targets", "2026-06-30", "Company"),
    acq_cash_returned=I(9_632.0, f"Note 5, {IH26}, SLDC analysis of cash flows — 'consideration "
                        f"received against acquisition paid in the prior year'", "2026-06-30",
                        "Company"),
    div_paid_1h26=I(512_500.0, f"Dividends paid, {IH26} statement of cash flows", "2026-06-30",
                    "Company"),
    days_dec25_to_anchor=I(219.0, "Calendar days from 31 December 2025, the date the discounting "
                           "convention places enterprise value on, to the 7 August 2026 price "
                           "anchor", "2026-08-07", "Market"),
    ids_target_fy26=I(70.0, f"{PR26}: 'ADNOC Drilling targets to deploy approximately 70 IDS rigs "
                      f"by the end of 2026'", "2026-07-30", "Company/IR"),
    rigs_regional_2q26=I(30.0, f"{MDA26}: 30 regional rigs outside the UAE at 30 June 2026 — 8 in "
                         f"Oman and Kuwait from the 70%-owned SLDC joint venture with SLB "
                         f"(completed January 2026) and 22 from the 80% stake in MBPS",
                         "2026-06-30", "Company/IR"),
    wells_fy23=I(613.0, "FY2023 MD&A — wells drilled", "2024-02-12", "Company/IR"),
    wells_fy24=I(676.0, "FY2024 MD&A — wells drilled", "2025-02-11", "Company/IR"),
    wells_fy25=I(836.0, f"{MDA25} — wells drilled", "2026-02-11", "Company/IR"),
    availability_fy25=I(0.98, f"{MDA25} — overall owned fleet availability at year end, excluding "
                        f"the 29 regional rigs", "2026-02-11", "Company/IR"),
    island_rigs_ordered=I(6.0, f"{MDA25}: 'the Company has ordered an additional six new island "
                          f"rigs that are expected to join the fleet gradually between 2026 and "
                          f"2028'", "2026-02-11", "Company/IR"),

    # unconventional programme — a finite, separately disclosed contract
    unconv_fy24=I(117_000.0, "FY2024 MD&A — unconventional business revenue contribution",
                  "2025-02-11", "Company/IR"),
    unconv_fy25=I(692_000.0, f"{MDA25}: unconventional revenue of $692 million in full year 2025, "
                  f"split $534 million in Oilfield Services and $158 million in Onshore land "
                  f"drilling", "2026-02-11", "Company/IR"),
    unconv_ofs_fy25=I(534_000.0, f"{MDA25} Oilfield Services commentary — unconventional "
                      f"contribution rose from $95 million in 2024 to $534 million in 2025",
                      "2026-02-11", "Company/IR"),
    unconv_ofs_fy24=I(95_000.0, f"{MDA25} Oilfield Services commentary, prior-year comparative — "
                      f"the unconventional contribution inside Oilfield Services was $95 million "
                      f"in 2024", "2026-02-11", "Company/IR"),
    ids_fy22=I(40.0, "FY2023 MD&A operational highlights, FY2022 comparative column — "
               "integrated-drilling-services rigs at year end", "2024-02-12", "Company/IR"),
    unconv_remaining_2025=I(860_000.0, f"{MDA25}: 'The remaining $0.86 billion contract value for "
                            f"unconventional ($1.7 billion total contract value less...)'",
                            "2026-02-11", "Company/IR"),
    unconv_1h26=I(206_000.0, f"1Q-2026 MD&A ($131 million) plus {MDA26} ($75 million in 2Q26, "
                  f"split $60 million Oilfield Services and $15 million Onshore)", "2026-07-30",
                  "Company/IR"),
    conv_ebitda_margin_fy25=I(0.51, f"{MDA25} financial summary — conventional EBITDA margin for "
                              f"FY2025, defined by the company as excluding the contribution of "
                              f"the unconventional business", "2026-02-11", "Company/IR"),
    conv_ebitda_margin_fy24=I(0.52, f"{MDA24} financial summary — conventional EBITDA margin for "
                              f"FY2024, on the same definition", "2025-02-11", "Company/IR"),
    seg_island_fy23=I(209_079.0, f"{FS23} segment note — Offshore Island revenue for FY2023, the "
                      f"last year the island and jack-up businesses were reported as separate "
                      f"segments; from 1Q-2025 they are presented as one Offshore segment",
                      "2024-02-12", "Company"),
    seg_jackup_fy23=I(799_726.0, f"{FS23} segment note — Offshore Jack-up revenue for FY2023",
                      "2024-02-12", "Company"),

    # ---------------- FY2026 company guidance --------------------------------
    g26_revenue=I(5_000_000.0, f"{PR26} full-year 2026 guidance — revenue of approximately $5 "
                  f"billion, reaffirmed at the 1H-2026 results", "2026-07-30", "Company/IR"),
    g26_rev_onshore=I(2_000_000.0, f"{PR26} guidance — Onshore revenue of approximately $2 billion",
                      "2026-07-30", "Company/IR"),
    g26_rev_offshore=I(1_500_000.0, f"{PR26} guidance — Offshore revenue of approximately $1.5 "
                       f"billion", "2026-07-30", "Company/IR"),
    g26_rev_ofs=I(1_500_000.0, f"{PR26} guidance — Oilfield Services revenue of approximately $1.5 "
                  f"billion", "2026-07-30", "Company/IR"),
    g26_ebitda_lo=I(2_200_000.0, f"{PR26} guidance — EBITDA of $2.2-2.3 billion", "2026-07-30",
                    "Company/IR"),
    g26_ebitda_hi=I(2_300_000.0, f"{PR26} guidance — EBITDA of $2.2-2.3 billion", "2026-07-30",
                    "Company/IR"),
    g26_capex_lo=I(600_000.0, f"{PR26} guidance — cash capital expenditure excluding mergers and "
                   f"acquisitions of $0.6-0.8 billion", "2026-07-30", "Company/IR"),
    g26_capex_hi=I(800_000.0, f"{PR26} guidance — cash capital expenditure excluding mergers and "
                   f"acquisitions of $0.6-0.8 billion", "2026-07-30", "Company/IR"),
    g26_dividend=I(1_050_000.0, f"{PR26} guidance — dividend floor of $1.05 billion, up 5% "
                   f"year on year", "2026-07-30", "Company/IR"),
    g_maint_capex=I(250_000.0, f"{MDA25}: 'Maintenance CapEx is expected at around $250 million per "
                    f"annum'", "2026-02-11", "Company/IR"),
    g_conv_margin_mt=I(0.50, f"{PR26}: 'management is focused on preserving a healthy EBITDA margin "
                       f"of circa 50% in the domestic conventional drilling business'",
                       "2026-07-30", "Company/IR"),
    g_ofs_margin_mt_lo=I(0.23, f"{PR26} medium-term guidance — conventional Oilfield Services "
                         f"EBITDA margin of 23-26%", "2026-07-30", "Company/IR"),
    g_ofs_margin_mt_hi=I(0.26, f"{PR26} medium-term guidance — conventional Oilfield Services "
                         f"EBITDA margin of 23-26%", "2026-07-30", "Company/IR"),

    # ---------------- cost of capital ----------------------------------------
    ust10=I(0.0469, "US 10-year constant-maturity Treasury yield, Federal Reserve H.15 via the "
            "St. Louis Fed (series DGS10), 06-Aug-2026 close", "2026-08-06", "Global"),
    ust5=I(0.0440, "US 5-year constant-maturity Treasury yield, Federal Reserve H.15 via the "
           "St. Louis Fed (series DGS5), 06-Aug-2026 close", "2026-08-06", "Global"),
    us_default_spread=I(0.0023, "Adjusted default spread for the United States (Moody's Aa1), "
                        "Damodaran country default spreads and risk premiums, original ctryprem "
                        "file, last updated 5 January 2026", "2026-01-05", "Global"),
    ad_rating=I("Aa2", "Moody's rating for the Emirate of Abu Dhabi, Damodaran ctryprem file",
                "2026-01-05", "Country"),
    ad_default_spread=I(0.0042, "Adjusted default spread for the Emirate of Abu Dhabi (Aa2), "
                        "Damodaran ctryprem file, 5 January 2026", "2026-01-05", "Country"),
    ad_crp=I(0.0064, "Country risk premium for the Emirate of Abu Dhabi, Damodaran ctryprem file",
             "2026-01-05", "Country"),
    erp_rating=I(0.0487, "Equity risk premium for the Emirate of Abu Dhabi on the rating basis "
                 "(mature-market premium plus the Abu Dhabi country risk premium), Damodaran "
                 "ctryprem file, 5 January 2026. The United Arab Emirates federal row carries the "
                 "identical Aa2 / 0.42% / 0.64% / 4.87% set", "2026-01-05", "Country"),
    ad_cds=I(0.0046, "Sovereign credit-default-swap spread for the Emirate of Abu Dhabi, "
             "Damodaran ctryprem file", "2026-01-05", "Country"),
    erp_cds=I(0.0493, "Equity risk premium for the Emirate of Abu Dhabi on the credit-default-swap "
              "basis, Damodaran ctryprem file, 5 January 2026", "2026-01-05", "Country"),
    tax_rate=I(0.09, f"Income tax note 30, {FS25}: 'The Group is subject to income tax at 9% on "
               f"its taxable profits in accordance with the fiscal arrangement with Abu Dhabi "
               f"Supreme Council for Financial and Economic Affairs effective 1 January 2024.' The "
               f"same 9% is the UAE statutory corporate rate in the Damodaran country file",
               "2026-02-11", "Company"),
    facility_margin=I(0.0075, f"Borrowings note 15, {FS25} — the Facility E and F term loan and "
                      f"revolving facility signed 16 October 2025, USD 2.0 billion committed, "
                      f"5-year initial maturity, priced at Term SOFR plus 0.75%. This is the "
                      f"company's own latest and longest-dated debt issue and therefore its "
                      f"marginal borrowing margin", "2025-10-16", "Company"),
    sofr_spot=I(0.0365, "Secured Overnight Financing Rate, New York Fed via the St. Louis Fed "
                "(series SOFR), 06-Aug-2026", "2026-08-06", "Global"),
    beta_raw=I(0.795, "Own-stock 5-year weekly regression against the FTSE ADX General Index — "
               "the headline index of the exchange the stock actually trades on, held at "
               "engine/raw_indices/AE/ADXGENERAL.csv (3,884 sessions, 02-Jan-2011 to "
               "24-Jul-2026, screened for blanks, duplicate dates, limit-exceeding single-session "
               "moves and trading-day density before use). n=247 weekly observations, R-squared "
               "0.128, standard error 0.133, 90% interval 0.58 to 1.01. Clears the regression "
               "usability gate (n>=24, R-squared>=5%, standard error below the absolute beta), so "
               "the first tier of the beta hierarchy applies and no peer beta is needed. "
               "SUPERSEDES a prior 0.664 measured against an equal-weight composite of the "
               "18-name UAE price library; that composite under-weights the large-capitalisation "
               "names the published index is concentrated in, and it is retained as a robustness "
               "check rather than as the regressor. The index series ends 24-Jul-2026 against a "
               "07-Aug-2026 price anchor, a 14-day gap that costs the regression two of roughly "
               "250 weekly observations. Source: engine/adnocdrill_study/beta_reg.py",
               "2026-07-24", "Market"),

    # ---------------- cost escalators, one per driver class ------------------
    esc_wages=I(0.020, "Staff-cost escalator. United Arab Emirates consumer price inflation ran "
                "1.63% in 2023, 1.66% in 2024 and 1.25% in 2025 (World Bank via the St. Louis "
                "Fed, series FPCPITOTLZGARE); 2.0% carries a modest real-wage drift above that "
                "for a business competing for skilled rig crews in a tight regional labour "
                "market. Applies ONLY to the domestic labour line", "2026-08-07", "Country"),
    esc_oilfield=I(0.015, "Oilfield-services cost escalator, applied to repairs and maintenance, "
                   "major maintenance and hire of equipment. US producer price index for drilling "
                   "oil and gas wells (series PCU213111213111) stood at 396.978 in June 2026, "
                   "down 1.63% year on year with a three-year compound rate of +0.29%. 1.5% sits "
                   "above the flat recent print and below general inflation, on the view that the "
                   "recent softness reflects the US land downturn rather than the Gulf market "
                   "these costs are actually incurred in — the gap is flagged rather than "
                   "smoothed away", "2026-06-01", "Industry"),
    esc_fuel=I(0.000, "Fuel and lubricants escalator. This is a globally traded input and is "
               "escalated on its own commodity path, NOT on a domestic inflation proxy: Brent "
               "closed at $88.90 on 03-Aug-2026 against a one-year average of $79.69 and a "
               "three-year average of $79.48 (US Energy Information Administration via the St. "
               "Louis Fed, series DCOILBRENTEU). Spot sits roughly 12% above the three-year mean, "
               "so a flat nominal path embeds mean reversion in real terms. The company's onshore "
               "contracts carry an explicit fuel-escalation pass-through — the 1H-2026 MD&A "
               "attributes part of the onshore revenue increase to 'higher fuel escalation' — so "
               "this line is close to margin-neutral either way", "2026-08-03", "Global"),
    esc_general=I(0.015, "Escalator for other direct cost and for general and administrative "
                  "expenses, anchored on United Arab Emirates consumer price inflation (1.25% in "
                  "2025, 1.66% in 2024) rounded to 1.5%", "2026-08-07", "Country"),
    esc_dayrate=I(0.015, "Contract day-rate escalator applied to the conventional revenue-per-rig "
                  "price line. The customer is a single national oil company on multi-year "
                  "contracts, so realised day rates track a negotiated escalation rather than a "
                  "spot market. Realised Abu Dhabi onshore revenue per average deployed rig moved "
                  "from $18.9 million in FY2023 to $20.9 million in FY2024 to $20.1 million in "
                  "FY2025 (this model's own unit arithmetic on disclosed segment revenue and "
                  "disclosed rig counts) — a three-year path that is up but not monotone. 1.5% is "
                  "set at domestic inflation rather than extrapolating the FY2024 step",
                  "2026-08-07", "Industry"),

    # ---------------- forecast judgements ------------------------------------
    unconv_ebitda_margin=I(0.065, "EBITDA margin on unconventional revenue, triangulated three "
                           "ways in the workbook rather than asserted: (i) the FY2025 disclosed "
                           "conventional EBITDA margin of 51% applied to conventional revenue "
                           "implies $50 million of EBITDA on $692 million of unconventional "
                           "revenue, a 7.3% margin; (ii) the same arithmetic on FY2024's "
                           "disclosed 52% implies a negative margin, but on a $117 million "
                           "revenue base a half-point of rounding in the disclosed margin swings "
                           "the answer by more than the answer itself, so it is reported and "
                           "discarded; (iii) the FY2024-to-FY2025 incremental bridge — group "
                           "EBITDA up $183 million on revenue up $869 million, of which $294 "
                           "million of conventional revenue at 51% explains $150 million — leaves "
                           "$33 million on $575 million of incremental unconventional revenue, a "
                           "5.8% margin. The average of the two usable estimates is 6.5%. This is "
                           "the single most consequential fact about the unconventional "
                           "programme: it is a large revenue line that carries almost no profit",
                           "2026-08-07", "House"),
    terminal_growth_A=I(0.025, "Terminal nominal growth under the continued-expansion framing. "
                        "Sits below long-run United States inflation expectations of 2.25% plus "
                        "real regional activity growth, and below the 3.0% ceiling a mature "
                        "contract driller could justify", "2026-08-07", "House"),
    terminal_growth_B=I(0.015, "Terminal nominal growth under the capacity-plateau framing — the "
                        "domestic fleet stops growing once the five-million-barrel-per-day "
                        "capacity target is met, so nominal growth is contract escalation only",
                        "2026-08-07", "House"),
    terminal_roic=I(0.18, "Terminal after-tax return on invested capital. The company earned a "
                    "23% return on capital employed in FY2025 and again in 1H-2026 (both "
                    "disclosed in the MD&A financial summary). 18% fades that toward, but not to, "
                    "a cost-of-capital return: the rig fleet is contracted to a single national "
                    "oil company on terms that have sustained a 23% return through a full "
                    "commodity cycle, so a fade to parity would contradict the observed record, "
                    "while holding 23% in perpetuity would capitalise an incumbency that faces "
                    "renegotiation at every contract roll", "2026-08-07", "House"),
    rev_per_rig_regional=I(8_000.0, "Revenue per regional land rig-year, USD thousands. Derived, "
                           "not assumed: 1H-2026 Onshore revenue of $1,031 million less roughly "
                           "$35 million of unconventional land drilling leaves $996 million; the "
                           "Abu Dhabi conventional fleet at its disclosed FY2025 realised rate "
                           "accounts for approximately $920 million of that, leaving about $76 "
                           "million earned across an average of roughly 19 regional rigs in the "
                           "half (8 SLDC rigs from January, 22 MBPS rigs part-period). That is "
                           "about $8.0 million per rig-year, roughly 40% of the Abu Dhabi rate, "
                           "consistent with smaller land rigs on Oman and Kuwait terms",
                           "2026-07-30", "House"),
)


def V(k):
    return INP[k]['value']


# ============================ DERIVED HISTORY ================================
YRS_H = [2023, 2024, 2025]
H = {}
for y in YRS_H:
    s = f'fy{y - 2000}'
    rev = V(f'rev_{s}')
    dcost = V(f'dcost_{s}')
    gna = V(f'gna_{s}')
    dna = V(f'dna_{s}')
    jv = V(f'jv_{s}')
    oth = V(f'othinc_{s}')
    ebitda = rev - dcost - gna + jv + oth + dna
    H[y] = dict(
        revenue=rev, direct_cost=dcost, gross_profit=rev - dcost, gna=gna, other_income=oth,
        jv_share=jv, ebitda=ebitda, ebitda_ex_jv=ebitda - jv, dna=dna, ebit=ebitda - dna,
        finance_cost=V(f'fincost_{s}'), finance_income=V(f'finincome_{s}'),
        pbt=rev - dcost - gna + oth + jv - V(f'fincost_{s}') + V(f'finincome_{s}'),
        tax=V(f'tax_{s}'), pat=V(f'pat_{s}'),
        seg_onshore=V(f'seg_on_{s}'), seg_offshore=V(f'seg_off_{s}'), seg_ofs=V(f'seg_ofs_{s}'),
        ppe=V(f'ppe_{s}'), rou=V(f'rou_{s}'), intangibles=V(f'intang_{s}'),
        jv_investment=V(f'jvinv_{s}'), deferred_tax_asset=V(f'dta_{s}'),
        advances=V(f'advnc_{s}') + V(f'advacq_{s}'),
        advance_for_acquisition=V(f'advacq_{s}'),
        inventories=V(f'inv_{s}'), receivables=V(f'tr_{s}'), due_from_rp=V(f'dfrp_{s}'),
        cash=V(f'cash_{s}'), assets_held_for_sale=V(f'afs_{s}'),
        debt=V(f'debt_{s}'), leases=V(f'lease_{s}'), payables=V(f'tp_{s}'),
        due_to_rp=V(f'dtrp_{s}'), eosb=V(f'eosb_{s}'), tax_payable=V(f'taxpay_{s}'),
        equity=V(f'equity_{s}'), total_assets=V(f'ta_{s}'),
        capex=V(f'capex_{s}'), cfo=V(f'cfo_{s}'), dividends=V(f'div_{s}'),
    )
    b = H[y]
    b['net_debt'] = b['debt'] + b['leases'] - b['cash']
    b['working_capital'] = (b['inventories'] + b['receivables'] + b['due_from_rp']
                            - b['payables'] - b['due_to_rp'])
    b['capital_employed'] = b['equity'] + b['net_debt']
    b['nopat'] = (b['ebit'] - b['jv_share']) * (1 - V('tax_rate'))
    b['roic'] = b['nopat'] / b['capital_employed']
    b['dso'] = (b['receivables'] + b['due_from_rp']) / b['revenue'] * 365
    b['dio'] = b['inventories'] / b['direct_cost'] * 365
    b['dpo'] = (b['payables'] + b['due_to_rp']) / b['direct_cost'] * 365
    b['ebitda_margin'] = b['ebitda'] / b['revenue']
    b['net_margin'] = b['pat'] / b['revenue']

# tie every reconstructed line to the filing it came from
for y in YRS_H:
    assert abs(H[y]['pat'] - V(f'pat_fy{y-2000}')) < 1.0, (y, H[y]['pbt'], H[y]['tax'])
    assert abs((H[y]['pbt'] - H[y]['tax']) - H[y]['pat']) < 1.0, y
assert abs(H[2025]['total_assets'] - (
    H[2025]['ppe'] + H[2025]['rou'] + H[2025]['intangibles'] + H[2025]['deferred_tax_asset']
    + H[2025]['jv_investment'] + H[2025]['advances'] + H[2025]['inventories']
    + H[2025]['receivables'] + H[2025]['due_from_rp'] + H[2025]['cash'])) < 1.0, "FY25 assets"
assert abs(H[2025]['equity'] - (
    H[2025]['total_assets'] - H[2025]['debt'] - H[2025]['leases'] - H[2025]['payables']
    - H[2025]['due_to_rp'] - H[2025]['eosb'] - H[2025]['tax_payable'])) < 1.0, "FY25 balance"
assert abs(sum(H[2025][k] for k in ('seg_onshore', 'seg_offshore', 'seg_ofs'))
           - H[2025]['revenue']) < 1.0, "FY25 segments do not sum to revenue"

# FY2025 direct-cost stack must sum to the disclosed direct cost
DC_STACK_FY25 = dict(
    repairs=V('dc_repairs_fy25'), staff=V('dc_staff_fy25'), hire=V('dc_hire_fy25'),
    chemicals=V('dc_chem_fy25'), fuel=V('dc_fuel_fy25'), major_maintenance=V('dc_majmaint_fy25'),
    other=V('dc_other_fy25'), depreciation=V('dc_dep_fy25'))
assert abs(sum(DC_STACK_FY25.values()) - H[2025]['direct_cost']) < 1.0, "FY25 cost stack"

# ============================ UNIT ARITHMETIC ================================
def avg(a, b):
    return (a + b) / 2.0


UNITS_H = {
    2023: dict(onshore=avg(V('rigs_onshore_fy22'), V('rigs_onshore_fy23')),
               jackup=avg(V('rigs_jackup_fy22'), V('rigs_jackup_fy23')),
               island=avg(V('rigs_island_fy22'), V('rigs_island_fy23')),
               ids=avg(V('ids_fy22'), V('ids_fy23')), wells=V('wells_fy23'), regional=0.0,
               unconv=0.0, unconv_ofs=0.0),
    2024: dict(onshore=avg(V('rigs_onshore_fy23'), V('rigs_onshore_fy24')),
               jackup=avg(V('rigs_jackup_fy23'), V('rigs_jackup_fy24')),
               island=avg(V('rigs_island_fy23'), V('rigs_island_fy24')),
               ids=avg(V('ids_fy23'), V('ids_fy24')), wells=V('wells_fy24'), regional=0.0,
               unconv=V('unconv_fy24'), unconv_ofs=V('unconv_ofs_fy24')),
    2025: dict(onshore=avg(V('rigs_onshore_fy24'), V('rigs_onshore_fy25')),
               jackup=avg(V('rigs_jackup_fy24'), V('rigs_jackup_fy25')),
               island=avg(V('rigs_island_fy24'), V('rigs_island_fy25')),
               ids=avg(V('ids_fy24'), V('ids_fy25')), wells=V('wells_fy25'), regional=0.0,
               unconv=V('unconv_fy25'), unconv_ofs=V('unconv_ofs_fy25')),
}
# The oilfield-services segment serves TWO books, and the company discloses both
# counts. Modelling only the integrated-services rigs — as the first edition did —
# leaves the larger of the two out of the volume driver entirely.
UNITS_H[2024]['discrete'] = V('discrete_fy24')
UNITS_H[2025]['discrete'] = V('discrete_fy25')
UNITS_H[2023]['discrete'] = float('nan')      # not disclosed for 2023; see below

for y in YRS_H:
    u = UNITS_H[y]
    u['unconv_onshore'] = u['unconv'] - u['unconv_ofs']
    u['offshore'] = u['jackup'] + u['island']
    u['rev_per_onshore_rig'] = (H[y]['seg_onshore'] - u['unconv_onshore']) / u['onshore']
    u['rev_per_offshore_rig'] = H[y]['seg_offshore'] / u['offshore']
    u['rev_per_ids_rig'] = (H[y]['seg_ofs'] - u['unconv_ofs']) / u['ids']
    u['wells_per_rig'] = u['wells'] / (u['onshore'] + u['offshore'])

# --- oilfield services: rigs served, and revenue per rig served --------------
# A two-driver model with CONSTANT rates is falsified by the company's own
# numbers: solving 57a + 48b = 718,116 and 60a + 58b = 928,004 returns a NEGATIVE
# rate for integrated services. Coverage grew 12% while conventional segment
# revenue grew 29%, so the growth is in revenue PER RIG SERVED, not in the count.
# That is what the company says too — "22% overall improvement in IDS drilling
# efficiency", "expanded delivery of discrete services". So the driver is total
# rigs served and the price is an intensity that is measured, not assumed.
OFS_SERVED = {2024: V('ids_fy24') + V('discrete_fy24'),
              2025: V('ids_fy25') + V('discrete_fy25')}
OFS_CONV = {y: H[y]['seg_ofs'] - UNITS_H[y]['unconv_ofs'] for y in (2024, 2025)}
OFS_REV_PER_SERVED = {y: OFS_CONV[y] / OFS_SERVED[y] for y in (2024, 2025)}
OFS_INTENSITY_REALISED = OFS_REV_PER_SERVED[2025] / OFS_REV_PER_SERVED[2024] - 1
_ofs_neg_check = np.linalg.solve(
    np.array([[V('ids_fy24'), V('discrete_fy24')], [V('ids_fy25'), V('discrete_fy25')]]),
    np.array([OFS_CONV[2024], OFS_CONV[2025]]))
assert _ofs_neg_check[0] < 0, ("the constant-rate two-driver solve is expected to be infeasible; "
                               "if it is not, the intensity construction below is unnecessary",
                               _ofs_neg_check)
OFS_SOLVE_INFEASIBLE = dict(implied_ids_rate=float(_ofs_neg_check[0]),
                            implied_discrete_rate=float(_ofs_neg_check[1]))

# The FY2023 offshore split is the only year the two offshore segments were
# reported separately; it fixes the island-to-jackup revenue ratio used to carry
# a split forward after the segments were merged into one from 1Q-2025.
_rev_per_island_23 = V('seg_island_fy23') / V('rigs_island_fy23')
_rev_per_jackup_23 = V('seg_jackup_fy23') / avg(V('rigs_jackup_fy22'),
                                                 V('rigs_jackup_fy23'))
ISLAND_TO_JACKUP = _rev_per_island_23 / _rev_per_jackup_23
REV_PER_JACKUP_25 = H[2025]['seg_offshore'] / (UNITS_H[2025]['jackup']
                                               + ISLAND_TO_JACKUP * UNITS_H[2025]['island'])
REV_PER_ISLAND_25 = REV_PER_JACKUP_25 * ISLAND_TO_JACKUP

# --- unconventional EBITDA margin, triangulated in code, not asserted --------
# Method (i): apply the disclosed FY2025 conventional EBITDA margin to
# conventional revenue; whatever group EBITDA is left over belongs to
# unconventional.
_conv_rev_25 = H[2025]['revenue'] - V('unconv_fy25')
_m1 = (H[2025]['ebitda'] - V('conv_ebitda_margin_fy25') * _conv_rev_25) / V('unconv_fy25')
# Method (ii): the same arithmetic on FY2024's disclosed 52%. Reported and then
# discarded — on a $117m revenue base, half a point of rounding in the disclosed
# margin moves the answer by more than the answer.
_conv_rev_24 = H[2024]['revenue'] - V('unconv_fy24')
_m2 = ((H[2024]['ebitda'] - V('conv_ebitda_margin_fy24') * _conv_rev_24)
       / V('unconv_fy24'))
# Method (iii): the FY2024-to-FY2025 incremental bridge.
_d_ebitda = H[2025]['ebitda'] - H[2024]['ebitda']
_d_conv_rev = _conv_rev_25 - _conv_rev_24
_d_unconv_rev = V('unconv_fy25') - V('unconv_fy24')
_m3 = (_d_ebitda - V('conv_ebitda_margin_fy25') * _d_conv_rev) / _d_unconv_rev
UNCONV_MARGIN_TRIANGULATION = dict(
    m1_disclosed_fy25_margin=_m1, m2_disclosed_fy24_margin=_m2,
    m3_incremental_bridge=_m3, used=[_m1, _m3], average_of_used=float(np.mean([_m1, _m3])),
    adopted=V('unconv_ebitda_margin'))

# ============================ COST OF CAPITAL ================================
# v2 method. The cash flows are USD, so the risk-free is the USD risk-free
# normalised by the United States' own default spread — country risk enters ONCE,
# through the Abu Dhabi country risk premium already inside the equity risk
# premium. Using a local yield that already contains sovereign risk AND adding a
# country-risk-loaded premium would count Abu Dhabi's default risk twice.
rf_star = V('ust10') - V('us_default_spread')
BETA = V('beta_raw')
ke_rating = rf_star + BETA * V('erp_rating')
ke_cds = rf_star + BETA * V('erp_cds')

# Cost of debt, triangulated three ways, with the sovereign floor as the test
kd_m1_term = V('ust5') + V('facility_margin')          # term-matched to the 5y facility
kd_m2_spot = V('sofr_spot') + V('facility_margin')     # today's floating all-in cost
kd_m3_trailing = V('fincost_fy25') and (108_839.0 / ((V('debt_fy24') + V('debt_fy25')) / 2))
sovereign_floor = V('ust5') + V('ad_cds')              # Abu Dhabi 5y USD sovereign
KD_CANDIDATES = dict(term_matched=kd_m1_term, spot_floating=kd_m2_spot,
                     trailing_effective=kd_m3_trailing)
KD_PASS = {k: v for k, v in KD_CANDIDATES.items() if v > sovereign_floor}
kd_pretax = kd_m1_term
kd_after_tax = kd_pretax * (1 - V('tax_rate'))

shares_out_k = V('shares_issued_k') - V('treasury_shares_k')
spot_usd = V('spot_aed') / V('fx_aed_usd')
mkt_cap = shares_out_k * spot_usd                       # USD '000
net_debt_now = V('debt_1h26') + V('lease_1h26') - V('cash_1h26')
# Capital-structure weights are struck on GROSS interest-bearing debt, not net.
# The first edition netted cash off debt before weighting, which is a category
# error: the cost of debt is paid on the gross balance, and cash is bridged
# separately in the EV-to-equity step. Netting it twice understates the debt
# weight — here by 355,423, about 1.3 points of weight and 4 basis points of
# discount rate. The direction of the correction is to LOWER the WACC, because
# after-tax debt is cheaper than equity, and so to RAISE value.
gross_debt_now = V('debt_1h26') + V('lease_1h26')
w_e = mkt_cap / (mkt_cap + gross_debt_now)
w_d = 1 - w_e
wacc_rating = w_e * ke_rating + w_d * kd_after_tax
wacc_cds = w_e * ke_cds + w_d * kd_after_tax
WACC = wacc_rating


# ==================== THE EV-TO-EQUITY BRIDGE, ONCE ==========================
# Every lens bridges through this one function, so a change to the bridge cannot
# reach one lens and miss another. Two corrections are built into it.
#
# (1) THE MINORITY IS DEDUCTED ONCE, NOT TWICE. The first edition deducted BOTH
#     the non-controlling interests of 53,594 AND the 62,530 financial liability
#     recognised over those same minorities. Those are two names for one claim:
#     under the shareholders' arrangements the parent may be required to buy the
#     30% of SLDC and the 20% of MBPS, and the company has recognised the present
#     value of that exercise price as a liability with a matching INVESTMENT
#     RESERVE of (62,530) charged directly to owners' equity — which is why the
#     30-Jun-2026 equity statement shows the reserve as negative. Deducting both
#     charges the parent twice for the same 30% and 20%. The put is the deduction
#     that survives, because it is the cash the parent would actually pay.
# (2) THE VALUATION DATE IS THE SAME ON BOTH SIDES. The first edition discounted
#     FY2026 free cash flow by a full year, which dates enterprise value at
#     31-Dec-2025, and then bridged it across the 30-Jun-2026 balance sheet. That
#     is half a year of mismatch, and it runs against the reader: enterprise value
#     was dated six months before the net debt deducted from it. Enterprise value
#     is now rolled forward to 30-Jun-2026 at the cost of capital, less the free
#     cash flow the business ACTUALLY generated over that half year, and the
#     resulting equity value is accreted the further 38 days to the price anchor
#     at the cost of equity.
FCFF_1H26 = V('cfo_1h26') - V('capex_1h26')
STUB_YEARS = 0.5                     # 31-Dec-2025 to 30-Jun-2026
ANCHOR_YEARS = V('days_jun26_to_anchor') / 365.0


def roll_ev_to_jun26(ev_dec25):
    """Enterprise value dated 31-Dec-2025, carried to 30-Jun-2026.

    The enterprise compounds at the cost of capital and is reduced by the cash it
    actually handed back over the half year. Acquisition consideration is NOT a
    reduction: it buys an asset that sits inside the same enterprise, so it nets
    out of an enterprise-value roll-forward by construction.
    """
    return (ev_dec25 * (1 + WACC) ** STUB_YEARS
            - FCFF_1H26 * (1 + WACC) ** (STUB_YEARS / 2))


def bridge(ev_jun26, detail=False):
    """Enterprise value at 30-Jun-2026 to equity per share at the price anchor."""
    eq_jun26 = (ev_jun26 + V('jvinv_1h26') + V('cash_1h26')
                - V('debt_1h26') - V('lease_1h26') - V('finliab_1h26'))
    eq_anchor = eq_jun26 * (1 + ke_rating) ** ANCHOR_YEARS
    usd = eq_anchor / shares_out_k
    if not detail:
        return usd * V('fx_aed_usd')
    return dict(enterprise_value=ev_jun26, jv_investment=V('jvinv_1h26'), cash=V('cash_1h26'),
                debt=-V('debt_1h26'), leases=-V('lease_1h26'), put_liability=-V('finliab_1h26'),
                equity_30jun26=eq_jun26, accretion_years=ANCHOR_YEARS,
                accretion=eq_anchor - eq_jun26, equity_value=eq_anchor,
                value_per_share_usd=usd, value_per_share_aed=usd * V('fx_aed_usd'))


# ============================ FORECAST =======================================
YRS_F = [2026, 2027, 2028, 2029, 2030]

FLEET = {
    # Framing A — the programme continues. The six ordered island rigs deliver
    # through 2028, integrated-services rigs scale past the stated 70 target,
    # and the regional platform adds rigs organically.
    'A': dict(
        onshore_ad={2026: 92, 2027: 94, 2028: 96, 2029: 98, 2030: 100},
        regional={2026: 30, 2027: 32, 2028: 34, 2029: 36, 2030: 38},
        # NB the regional book OPENS at 30, not at zero — see OPEN_FLEET below
        jackup={2026: 36, 2027: 36, 2028: 36, 2029: 36, 2030: 36},
        island={2026: 14, 2027: 16, 2028: 18, 2029: 18, 2030: 18},
        ids={2026: 70, 2027: 74, 2028: 78, 2029: 80, 2030: 82},
        discrete={2026: 56, 2027: 58, 2028: 60, 2029: 62, 2030: 64},
        unconv={2026: 400_000.0, 2027: 260_000.0, 2028: 200_000.0,
                2029: 200_000.0, 2030: 200_000.0},
    ),
    # Framing B — the capacity target lands and the domestic fleet plateaus.
    # The already-ordered island rigs still arrive (they are paid for), but
    # nothing follows them, integrated services stop at the announced target,
    # and the unconventional contract runs off with no phase two.
    'B': dict(
        onshore_ad={2026: 92, 2027: 92, 2028: 92, 2029: 92, 2030: 92},
        regional={2026: 30, 2027: 30, 2028: 30, 2029: 30, 2030: 30},
        jackup={2026: 36, 2027: 36, 2028: 36, 2029: 36, 2030: 36},
        island={2026: 14, 2027: 16, 2028: 18, 2029: 18, 2030: 18},
        ids={2026: 70, 2027: 72, 2028: 72, 2029: 72, 2030: 72},
        discrete={2026: 56, 2027: 56, 2028: 56, 2029: 56, 2030: 56},
        unconv={2026: 400_000.0, 2027: 200_000.0, 2028: 60_000.0, 2029: 0.0, 2030: 0.0},
    ),
}
CAPEX_PLAN = {
    'A': {2026: 700_000.0, 2027: 600_000.0, 2028: 520_000.0, 2029: 420_000.0, 2030: 380_000.0},
    'B': {2026: 700_000.0, 2027: 520_000.0, 2028: 400_000.0, 2029: 300_000.0, 2030: 280_000.0},
}
TERMINAL_G = {'A': V('terminal_growth_A'), 'B': V('terminal_growth_B')}

# FY2025 conventional cost stack, net of the cost carried by unconventional revenue
unconv_cost_fy25 = V('unconv_fy25') * (1 - V('unconv_ebitda_margin'))
conv_dcost_fy25 = (H[2025]['direct_cost'] - V('dc_dep_fy25')) - unconv_cost_fy25
_stack_ex_dep = {k: v for k, v in DC_STACK_FY25.items() if k != 'depreciation'}
_share = sum(_stack_ex_dep.values())
CONV_STACK_FY25 = {k: v * conv_dcost_fy25 / _share for k, v in _stack_ex_dep.items()}

COST_DRIVER = dict(
    repairs='rig_years', staff='rig_years', hire='conv_revenue', chemicals='wells',
    fuel='rig_years', major_maintenance='offshore_rig_years', other='conv_revenue')
COST_ESCALATOR = dict(
    repairs=V('esc_oilfield'), staff=V('esc_wages'), hire=V('esc_oilfield'),
    chemicals=V('esc_oilfield'), fuel=V('esc_fuel'),
    major_maintenance=V('esc_oilfield'), other=V('esc_general'))

GNA_DA_FY25 = V('gna_dep_fy25')
GNA_EX_DA_FY25 = V('gna_fy25') - GNA_DA_FY25
assert abs((V('dc_dep_fy25') + GNA_DA_FY25) - V('dna_fy25')) < 1.0, \
    "the two depreciation allocations must sum to total depreciation and amortisation"
BASE_UNITS_25 = dict(
    rig_years=UNITS_H[2025]['onshore'] + UNITS_H[2025]['offshore'] + UNITS_H[2025]['ids'],
    offshore_rig_years=UNITS_H[2025]['offshore'],
    wells=UNITS_H[2025]['wells'],
    conv_revenue=H[2025]['revenue'] - V('unconv_fy25'))

DEP_RATE = V('dna_fy25') / (H[2024]['ppe'] + H[2024]['rou'] + H[2024]['intangibles'])

# ---- working capital: the ratio comes off the 30-Jun-2026 balance sheet ------
# The first edition projected the FY2023-25 audited average, 5.91% of revenue.
# That average was constructed entirely from year ends that PRE-DATE the two
# regional acquisitions, and it was applied to a revenue line that consolidates
# them from 2026 — an internal inconsistency, and the one the audit priced.
#
# The 30-Jun-2026 balance sheet is the only one that consolidates the acquired
# book, so it is the only coherent basis. Two questions had to be settled before
# using a mid-year balance sheet for a full-year ratio:
#   (1) is a mid-year balance sheet seasonally inflated for this company? The
#       1H-2025 comparative movements in the same statement of cash flows say
#       the opposite: working capital RELEASED 154,080 over 1H-2025, so a
#       mid-year balance sheet here runs BELOW the year end, not above it. The
#       ratio is therefore, if anything, understated rather than seasonal.
#   (2) how much of the 1H-2026 build is the acquisition rather than the
#       business? The acquired book is separable from note 5 and is taken out
#       below, so both the total ratio and the organic ratio are visible.
WC_ACQUIRED = V('acq_inventories') + V('acq_receivables') - V('acq_payables')
WC_1H26 = (V('inv_1h26') + V('recv_1h26') + V('dfrp_1h26') - V('tp_1h26') - V('dtrp_1h26'))
REV_1H26_ANNUALISED = V('rev_1h26') * 2
WC_PCT_REVENUE = WC_1H26 / REV_1H26_ANNUALISED
WC_PCT_REVENUE_ORGANIC = (WC_1H26 - WC_ACQUIRED) / REV_1H26_ANNUALISED
WC_PCT_REVENUE_HIST = float(np.mean([H[y]['working_capital'] / H[y]['revenue'] for y in YRS_H]))


# FY2025 working-capital composition, used to split the forecast working-capital
# balance back into the individual balance-sheet lines it is made of.
WC_MIX = {k: H[2025][k] / abs(H[2025]['working_capital']) for k in
          ('inventories', 'receivables', 'due_from_rp', 'payables', 'due_to_rp')}


# The regional book OPENS at the count already consolidated, not at zero. Opening
# it at zero averaged 15 rig-years into 2026 when the interim accounts already
# carried roughly 19 in the first half alone — a full-year average cannot sit
# below the first-half average of a growing fleet.
ADVANCE_FOR_ACQUISITION = H[2025]['advance_for_acquisition']

# The 2026 business combinations as one entry, published so a reader can add it up.
# It is asserted to close to zero against owners' equity inside build_case().
ACQ_ENTRY = [
    ('Property, equipment, right-of-use assets and goodwill acquired',
     V('acq_ppe') + V('acq_rou') + V('acq_goodwill')),
    ('Working capital acquired', V('acq_inventories') + V('acq_receivables') - V('acq_payables')),
    ('Cash acquired', V('acq_cash')),
    ('Borrowings and lease liabilities assumed', -(V('acq_borrowings') + V('acq_leases'))),
    ('Deferred tax, income tax and end-of-service benefits assumed',
     -(V('acq_deferred_tax') + V('acq_income_tax') + V('acq_eosb'))),
    ('Contingent consideration outstanding', -V('acq_contingent')),
    ('Minority interests recognised', -V('acq_nci')),
    ('The 2025 advance, released against consideration', -ADVANCE_FOR_ACQUISITION),
    ('Cash consideration paid in 2026, net of the amount received back',
     -(V('acq_consideration_2026') - V('acq_cash_returned'))),
]
OPEN_FLEET = dict(onshore_ad=V('rigs_onshore_fy25'), regional=V('rigs_regional_2q26'),
                  jackup=V('rigs_jackup_fy25'), island=V('rigs_island_fy25'),
                  ids=V('ids_fy25'), discrete=V('discrete_fy25'))


def build_case(case, calib=None):
    fl, cx = FLEET[case], CAPEX_PLAN[case]
    cal = calib or dict(onshore=1.0, offshore=1.0, ofs=1.0)
    prev = dict(OPEN_FLEET)
    # The forecast balance sheet opens on the FY2025 AUDITED balance sheet and the
    # two 2026 business combinations are then added IN 2026, which is when they
    # actually closed. The first edition consolidated the acquired REVENUE from
    # 2026 while leaving the acquired asset base, the assumed borrowings and the
    # minority interests out of the roll-forward entirely.
    ppe_open = H[2025]['ppe'] + H[2025]['rou'] + H[2025]['intangibles']
    other_nc = H[2025]['deferred_tax_asset'] + H[2025]['advances']
    # Debt policy: hold gross interest-bearing debt flat at the audited FY2025
    # level. The company guides to leverage below 2.0x net debt to EBITDA and is
    # running at 1.0x, so there is neither a repayment obligation the cash flow
    # cannot meet nor a stated intention to lever up. Cash is the balancing item.
    debt = H[2025]['debt'] + H[2025]['leases']
    equity_open = H[2025]['equity']
    cash_open = H[2025]['cash']
    jv_book = H[2025]['jv_investment']
    
    eosb_open, taxpay_open = H[2025]['eosb'], H[2025]['tax_payable']
    nci_book = 0.0
    # Liabilities that came with the two acquisitions and that no forecast driver
    # generates: the deferred tax liability, the income tax payable assumed, and
    # the contingent consideration still outstanding. Held flat across the window
    # and disclosed as such — 32,362 on an 8.6bn balance sheet.
    acq_liab = 0.0
    intensity_prev = 1.0
    rows = []
    for n, y in enumerate(YRS_F, start=1):
        esc = (1 + V('esc_dayrate')) ** n
        a_on = avg(prev['onshore_ad'], fl['onshore_ad'][y])
        a_rg = avg(prev['regional'], fl['regional'][y])
        a_ju = avg(prev['jackup'], fl['jackup'][y])
        a_is = avg(prev['island'], fl['island'][y])
        a_ids = avg(prev['ids'], fl['ids'][y])
        a_disc = avg(prev['discrete'], fl['discrete'][y])
        a_served = a_ids + a_disc
        # Oilfield-services intensity: revenue per rig served grew 15.0% from
        # FY2024 to FY2025 on the company's own disclosed counts and segment
        # revenue. That is measured, not assumed. It fades linearly to the
        # contract escalator by the end of the window, because a 15% annual gain
        # in revenue per rig served is an efficiency and mix effect that cannot
        # compound indefinitely.
        fade = (n - 1) / (len(YRS_F) - 1)
        step = OFS_INTENSITY_REALISED * (1 - fade) + V('esc_dayrate') * fade
        intensity = (intensity_prev := intensity_prev * (1 + step))

        r_on_raw = a_on * UNITS_H[2025]['rev_per_onshore_rig'] * esc
        r_rg_raw = a_rg * V('rev_per_rig_regional') * esc
        r_ju_raw = a_ju * REV_PER_JACKUP_25 * esc
        r_is_raw = a_is * REV_PER_ISLAND_25 * esc
        r_ids_raw = a_served * OFS_REV_PER_SERVED[2025] * intensity
        r_on = r_on_raw * cal['onshore']
        r_rg = r_rg_raw * cal['onshore']
        r_ju = r_ju_raw * cal['offshore']
        r_is = r_is_raw * cal['offshore']
        r_ids = r_ids_raw * cal['ofs']
        unconv = fl['unconv'][y]
        unconv_on = unconv * (V('unconv_fy25') and
                              (V('unconv_fy25') - V('unconv_ofs_fy25')) / V('unconv_fy25'))
        unconv_ofs = unconv - unconv_on

        seg_on = r_on + r_rg + unconv_on
        seg_off = r_ju + r_is
        seg_ofs = r_ids + unconv_ofs
        revenue = seg_on + seg_off + seg_ofs
        conv_revenue = revenue - unconv

        if n == 1:
            # The two business combinations closed in 2026 and enter here, in the
            # year they closed, as the single entry note 5 supports line by line.
            # Every figure below is disclosed; nothing is a plug, and the entry is
            # asserted to balance to zero against owners' equity immediately after
            # it is applied — a business combination cannot move the parent's
            # equity, so an entry that does is wrong by construction.
            #
            #   Dr  property, plant, right-of-use and goodwill        309,398
            #   Dr  working capital acquired                           41,134
            #   Dr  cash acquired                                      42,683
            #   Cr  borrowings and lease liabilities assumed          179,648
            #   Cr  deferred tax, income tax and end-of-service        14,683
            #   Cr  contingent consideration outstanding               20,372
            #   Cr  minority interests recognised                      49,931
            #   Cr  the 2025 advance, released against consideration   90,926
            #   Cr  cash consideration paid in 2026, net of the
            #       9,632 received back against the 2025 advance       37,655
            #                                          Dr 393,215  Cr 393,215
            acq_fixed = V('acq_ppe') + V('acq_rou') + V('acq_goodwill')
            acq_debt = V('acq_borrowings') + V('acq_leases')
            acq_liab = V('acq_deferred_tax') + V('acq_income_tax') + V('acq_contingent')
            acq_cash_net = V('acq_cash') - V('acq_consideration_2026') + V('acq_cash_returned')
            ppe_open += acq_fixed
            other_nc -= ADVANCE_FOR_ACQUISITION      # the 2025 advance converts into the above
            debt += acq_debt
            cash_open += acq_cash_net
            eosb_open += V('acq_eosb')
            nci_book = V('acq_nci')
            _entry = (acq_fixed + WC_ACQUIRED + V('acq_cash')
                      - acq_debt - V('acq_deferred_tax') - V('acq_income_tax') - V('acq_eosb')
                      - V('acq_contingent') - V('acq_nci') - ADVANCE_FOR_ACQUISITION
                      - (V('acq_consideration_2026') - V('acq_cash_returned')))
            assert abs(_entry) < 1.0, ('the business-combination entry does not close against '
                                       'owners equity', _entry)

        units = dict(rig_years=a_on + a_rg + a_ju + a_is + a_ids,
                     offshore_rig_years=a_ju + a_is,
                     wells=UNITS_H[2025]['wells'] * (a_on + a_rg + a_ju + a_is)
                     / (UNITS_H[2025]['onshore'] + UNITS_H[2025]['offshore']),
                     conv_revenue=conv_revenue)
        stack = {}
        for k, base in CONV_STACK_FY25.items():
            drv = COST_DRIVER[k]
            stack[k] = base * (units[drv] / BASE_UNITS_25[drv]) * (1 + COST_ESCALATOR[k]) ** n
        conv_cash_cost = sum(stack.values())
        unconv_cash_cost = unconv * (1 - V('unconv_ebitda_margin'))
        gna = GNA_EX_DA_FY25 * (conv_revenue / BASE_UNITS_25['conv_revenue']) \
            * (1 + V('esc_general')) ** n
        other_income = V('othinc_fy25') * (1 + V('esc_general')) ** n
        jv_share = V('jv_fy25') * (1 + V('esc_general')) ** n

        ebitda = revenue - conv_cash_cost - unconv_cash_cost - gna + other_income + jv_share
        ebitda_ex_jv = ebitda - jv_share
        capex = cx[y]
        dna = ppe_open * DEP_RATE
        ebit = ebitda_ex_jv - dna
        nopat = ebit * (1 - V('tax_rate'))
        wc = revenue * WC_PCT_REVENUE
        wc_prev = (H[2025]['working_capital'] if n == 1 else rows[-1]['working_capital'])
        # The working capital that ARRIVED with the acquisitions was bought, not
        # funded out of operations, so it is stripped out of the operating
        # movement. Leaving it in would charge the free cash flow twice for the
        # same 41,134 — once in the consideration and once again here.
        d_wc = wc - wc_prev - (WC_ACQUIRED if n == 1 else 0.0)
        fcff = nopat + dna - capex - d_wc
        df = 1 / (1 + WACC) ** n
        ppe_close = ppe_open + capex - dna

        # --- statements ------------------------------------------------------
        interest = debt * kd_pretax
        finance_income = cash_open * V('sofr_spot')
        pbt = ebit + jv_share - interest + finance_income
        tax = pbt * V('tax_rate')
        pat = pbt - tax
        dividend = V('g26_dividend') * (1.05 ** (n - 1))
        equity_close = equity_open + pat - dividend
        eosb_close = eosb_open * (1 + V('esc_wages'))
        taxpay_close = tax * (H[2025]['tax_payable'] / H[2025]['tax'])
        cfo = pat + dna - d_wc + (eosb_close - eosb_open) + (taxpay_close - taxpay_open)
        cff = -dividend
        cash_close = cash_open + cfo - capex + cff

        # balance sheet, built line by line from the drivers above
        bs = dict(fixed_assets=ppe_close, other_non_current=other_nc, jv_investment=jv_book,
                  inventories=wc * WC_MIX['inventories'],
                  receivables=wc * WC_MIX['receivables'],
                  due_from_rp=wc * WC_MIX['due_from_rp'],
                  cash=cash_close,
                  debt=debt, payables=wc * WC_MIX['payables'],
                  due_to_rp=wc * WC_MIX['due_to_rp'],
                  eosb=eosb_close, tax_payable=taxpay_close,
                  acquisition_liabilities=acq_liab, nci=nci_book)
        bs['total_assets'] = (bs['fixed_assets'] + bs['other_non_current'] + bs['jv_investment']
                              + bs['inventories'] + bs['receivables'] + bs['due_from_rp']
                              + bs['cash'])
        bs['total_liabilities'] = (bs['debt'] + bs['payables'] + bs['due_to_rp'] + bs['eosb']
                                   + bs['tax_payable'] + bs['acquisition_liabilities'])
        # Equity is the residual of a balance sheet whose every other line is
        # driven. The roll-forward equity above is the independent check on it,
        # and the two must agree — asserted after the loop.
        bs['equity_residual'] = bs['total_assets'] - bs['total_liabilities'] - nci_book
        bs['equity_rollforward'] = equity_close
        bs['balance_check'] = bs['equity_residual'] - equity_close

        rows.append(dict(
            year=y, avg_onshore_ad=a_on, avg_regional=a_rg, avg_jackup=a_ju, avg_island=a_is,
            avg_ids=a_ids, avg_discrete=a_disc, avg_served=a_served,
            day_rate_index=esc, ofs_intensity=intensity,
            rev_onshore_ad_raw=r_on_raw, rev_regional_raw=r_rg_raw, rev_jackup_raw=r_ju_raw,
            rev_island_raw=r_is_raw, rev_ids_raw=r_ids_raw,
            calib_onshore=cal['onshore'], calib_offshore=cal['offshore'], calib_ofs=cal['ofs'],
            rev_onshore_ad=r_on, rev_regional=r_rg, rev_jackup=r_ju, rev_island=r_is,
            rev_ids=r_ids, unconventional=unconv, unconv_onshore=unconv_on,
            unconv_ofs=unconv_ofs,
            seg_onshore=seg_on, seg_offshore=seg_off, seg_ofs=seg_ofs,
            revenue=revenue, conv_revenue=conv_revenue,
            cost_stack=stack, conv_cash_cost=conv_cash_cost, unconv_cash_cost=unconv_cash_cost,
            gna=gna, other_income=other_income, jv_share=jv_share,
            ebitda=ebitda, ebitda_ex_jv=ebitda_ex_jv, ebitda_margin=ebitda / revenue,
            dna=dna, ebit=ebit, nopat=nopat, capex=capex,
            working_capital=wc, delta_wc=d_wc, fcff=fcff,
            discount_factor=df, pv_fcff=fcff * df,
            ppe_open=ppe_open, ppe_close=ppe_close,
            interest=interest, finance_income=finance_income, pbt=pbt, tax=tax, pat=pat,
            dividend=dividend, equity_open=equity_open, equity_close=equity_close,
            cfo=cfo, cash_open=cash_open, cash_close=cash_close,
            net_margin=pat / revenue, balance_sheet=bs,
            net_debt=debt - cash_close,
            capital_employed=equity_close + debt - cash_close,
            roic=nopat / (equity_close + debt - cash_close),
            units=units))
        prev = {k: fl[k][y] for k in prev}
        ppe_open, equity_open, cash_open = ppe_close, equity_close, cash_close
        eosb_open, taxpay_open = eosb_close, taxpay_close

    g = TERMINAL_G[case]
    roic_t = V('terminal_roic')
    nopat_t1 = rows[-1]['nopat'] * (1 + g)
    reinvest_rate = g / roic_t
    # THE TERMINAL BLOCK IS CAPITALISED AT THE WEIGHTED COST OF CAPITAL — and this
    # is a REVERSAL of a correction this study's own self-audit accepted and
    # priced at -0.157 a share. It was implemented, and it did not survive
    # implementation. The finding was that by 2030 the model's own balance sheet
    # has the firm holding net cash, so the terminal rate should be the cost of
    # equity rather than a leveraged weighted cost.
    #
    # It fails a coherence test against a correction accepted in the same pass.
    # The capital-structure weights were moved from NET debt onto GROSS debt on
    # the argument that interest is paid on the gross balance and cash is bridged
    # separately — accept that, and a firm holding cash alongside undiminished
    # gross borrowings has not de-levered at all. It still pays interest on the
    # same debt and still earns the same tax shield. Reading the terminal capital
    # structure off NET debt after refusing to read today's off net debt is the
    # same quantity treated two ways in one model.
    #
    # Implementing it also produced a defect neither framing predicted: a rate
    # that switches on the SIGN of terminal net debt is discontinuous, and a
    # driver test caught it — raising the working-capital ratio cut the present
    # value of the explicit five years by 546,000, flipped the 2030 firm into net
    # debt, moved the capitalisation rate DOWN 32 basis points and lifted the
    # answer. A heavier working-capital burden made the company more valuable.
    # That is not a result, it is a kink.
    #
    # Terminal net debt is still computed and still published, because it is worth
    # seeing. It just no longer sets the rate.
    terminal_net_debt = rows[-1]['net_debt']
    terminal_is_net_cash = terminal_net_debt < 0
    terminal_rate = WACC
    tv = nopat_t1 * (1 - reinvest_rate) / (terminal_rate - g)
    pv_tv = tv * rows[-1]['discount_factor']
    pv_explicit = sum(r['pv_fcff'] for r in rows)
    ev_dec25 = pv_explicit + pv_tv
    ev = roll_ev_to_jun26(ev_dec25)
    br = bridge(ev, detail=True)
    return dict(case=case, rows=rows, terminal_growth=g, terminal_roic=roic_t,
                terminal_nopat=nopat_t1, reinvestment_rate=reinvest_rate,
                terminal_net_debt=terminal_net_debt, terminal_is_net_cash=terminal_is_net_cash,
                terminal_rate=terminal_rate,
                terminal_value=tv, pv_terminal=pv_tv, pv_explicit=pv_explicit,
                enterprise_value_dec25=ev_dec25, stub_fcff=FCFF_1H26,
                enterprise_value=ev, tv_pct_of_ev=pv_tv / ev_dec25, bridge=br,
                equity_value=br['equity_value'],
                value_per_share_usd=br['value_per_share_usd'],
                value_per_share_aed=br['value_per_share_aed'])


# ---- segment calibration to the company's own FY2026 guidance ----------------
# The first edition reconciled to guidance at GROUP level (-1.8%) while the
# segment build missed Oilfield Services by -9.6%. The company guides all three
# segments, so the build is reconciled to all three: the ratio of guided to built
# revenue becomes a persistent level correction on that segment's unit rate,
# carried through every forecast year rather than plugged into 2026.
# The factor is solved on the CONVENTIONAL part of each segment, which is the part
# the unit rates build. The unconventional programme is contracted revenue on its
# own schedule and is not scaled by a unit-rate correction; solving the factor over
# the whole segment and then applying it to part of the segment would leave the
# calibrated year short of the guidance it was solved against, which is what the
# first edition did — it missed the group guide by 1.8% AFTER calibrating to it.
_raw = build_case('A')
_r0 = _raw['rows'][0]
CALIB = dict(
    onshore=((V('g26_rev_onshore') - _r0['unconv_onshore'])
             / (_r0['rev_onshore_ad'] + _r0['rev_regional'])),
    offshore=V('g26_rev_offshore') / _r0['seg_offshore'],
    ofs=(V('g26_rev_ofs') - _r0['unconv_ofs']) / _r0['rev_ids'])
CALIB_UNCALIBRATED = dict(onshore=_r0['seg_onshore'], offshore=_r0['seg_offshore'],
                          ofs=_r0['seg_ofs'], total=_r0['revenue'],
                          onshore_conventional=_r0['rev_onshore_ad'] + _r0['rev_regional'],
                          offshore_conventional=_r0['seg_offshore'],
                          ofs_conventional=_r0['rev_ids'])

CASE = {c: build_case(c, CALIB) for c in ('A', 'B')}

# ============================ OTHER LENSES ===================================
with open(os.path.join(HERE, 'peers_raw.json')) as f:
    PEERS_RAW = json.load(f)
SAR_USD = 3.75
peer_rows = []
for p in PEERS_RAW:
    if 'error' in p or not p.get('ltm_ebitda'):
        continue
    fx = SAR_USD if p['currency'] == 'SAR' else 1.0
    mcap = p['price'] * p['shares'] / fx / 1e6
    nd = (p['total_debt'] - (p['cash'] or 0)) / fx / 1e6
    ebitda = p['ltm_ebitda'] / fx / 1e6
    ni = (p['ltm_net_income'] or 0) / fx / 1e6
    ev = mcap + nd
    peer_rows.append(dict(symbol=p['symbol'], name=p['name'], group=p['group'],
                          market_cap_usd_mn=mcap, net_debt_usd_mn=nd, ev_usd_mn=ev,
                          ltm_ebitda_usd_mn=ebitda, ltm_net_income_usd_mn=ni,
                          ev_ebitda=ev / ebitda if ebitda > 0 else None,
                          pe=mcap / ni if ni > 0 else None,
                          latest_period=p['latest_period']))
mena = [r for r in peer_rows if r['group'].startswith('MENA')]
land = [r for r in peer_rows if r['group'].startswith('Global land')]
offs = [r for r in peer_rows if r['group'].startswith('Global offshore')]
ofsg = [r for r in peer_rows if r['group'].startswith('Diversified')]


def med(rows, k):
    v = sorted(r[k] for r in rows if r.get(k))
    if not v:
        return None
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


ebitda_fy26 = (V('g26_ebitda_lo') + V('g26_ebitda_hi')) / 2
# Segment-weighted peer multiple: each segment gets the multiple of the peer
# group that actually does that job, weighted by that segment's share of EBITDA.
seg_w = dict(onshore=V('seg_ebitda_on_fy25'), offshore=V('seg_ebitda_off_fy25'),
             ofs=V('seg_ebitda_ofs_fy25'))
seg_tot = sum(seg_w.values())
mult_mena, mult_land, mult_offs, mult_ofsg = (med(mena, 'ev_ebitda'), med(land, 'ev_ebitda'),
                                              med(offs, 'ev_ebitda'), med(ofsg, 'ev_ebitda'))
blended_multiple = (seg_w['onshore'] / seg_tot * np.mean([mult_mena, mult_land])
                    + seg_w['offshore'] / seg_tot * np.mean([mult_mena, mult_offs])
                    + seg_w['ofs'] / seg_tot * mult_ofsg)

# The multiple and the earnings it multiplies are now on the SAME basis, on two
# counts the first edition got wrong in the same direction.
#   TRAILING ON TRAILING. Every peer multiple in the table is an enterprise value
#   struck today over the LAST TWELVE MONTHS of that peer's EBITDA. The first
#   edition applied those trailing multiples to ADNOC Drilling's GUIDED FY2026
#   EBITDA, which credits the company with a year of growth no peer in the
#   denominator is credited with. The multiple is now applied to the same
#   last-twelve-months EBITDA basis: audited FY2025 plus 1H-2026 less 1H-2025.
#   EX-JOINT-VENTURE ON EX-JOINT-VENTURE. This company's reported EBITDA includes
#   its share of the results of Enersol and Turnwell. The carrying value of those
#   joint ventures is then added back on the bridge. Capitalising the earnings AND
#   adding back the asset that produces them counts the joint ventures twice. The
#   share of results is stripped out of the multiplied earnings; the carrying
#   value stays in the bridge, which is the side of the pair that is observable.
ltm_ebitda = H[2025]['ebitda'] + V('ebitda_1h26') - V('ebitda_1h25')
ltm_jv = V('jv_fy25') + V('jv_1h26') - V('jv_1h25')
ltm_ebitda_ex_jv = ltm_ebitda - ltm_jv
rel_ev = blended_multiple * ltm_ebitda_ex_jv
rel_bridge = bridge(rel_ev, detail=True)
RELATIVE = dict(peers=peer_rows,
                median_mena=mult_mena, median_land=mult_land, median_offshore=mult_offs,
                median_ofs=mult_ofsg, blended_multiple=float(blended_multiple),
                segment_weights={k: v / seg_tot for k, v in seg_w.items()},
                ltm_ebitda=float(ltm_ebitda), ltm_jv_share=float(ltm_jv),
                guided_ebitda_fy26=float(ebitda_fy26),
                applied_ebitda=float(ltm_ebitda_ex_jv), enterprise_value=float(rel_ev),
                bridge=rel_bridge,
                equity_value=float(rel_bridge['equity_value']),
                value_per_share_usd=float(rel_bridge['value_per_share_usd']),
                value_per_share_aed=float(rel_bridge['value_per_share_aed']),
                implied_own_ev_ebitda=float((mkt_cap + gross_debt_now - V('cash_1h26'))
                                            / ltm_ebitda_ex_jv),
                median_pe_mena=med(mena, 'pe'), median_pe_land=med(land, 'pe'),
                median_pe_offshore=med(offs, 'pe'), median_pe_ofs=med(ofsg, 'pe'))

# --- book value and sustainable return ---------------------------------------
# A return-on-equity franchise lens: the justified price-to-book of a business
# earning ROE against a cost of equity, growing at g. P/B = (ROE - g)/(Ke - g).
roe_fy25 = H[2025]['pat'] / avg(H[2024]['equity'], H[2025]['equity'])
roe_historical = np.mean([H[y]['pat'] / avg(H[y - 1]['equity'] if y > 2023 else H[2023]['equity'],
                                            H[y]['equity']) for y in (2024, 2025)])
# The return that goes into a PERPETUAL formula has to be a return the business
# can be held to in perpetuity, and this study already contains a forecast of
# exactly that. The first edition used the FY2024-25 realised average, 36.7%. Its
# own cash-flow model, on its own drivers, has the return falling as the capital
# base grows into the fleet being built. Using the historical return here made the
# book lens richer than the model that sits four sections above it, on nothing
# more than the fact that the past was measured on a smaller balance sheet. The
# 2030 return the model itself forecasts is the number used; the average across
# the forecast window is published beside it so a reader can see the spread.
_bk = CASE['A']['rows']
roe_forecast_2030 = _bk[-1]['pat'] / avg(_bk[-2]['equity_close'], _bk[-1]['equity_close'])
roe_forecast_mean = float(np.mean([r['pat'] / avg(r['equity_open'], r['equity_close'])
                                   for r in _bk]))
roe_sustainable = roe_forecast_2030
g_book = V('terminal_growth_A')
justified_pb = (roe_sustainable - g_book) / (ke_rating - g_book)
book_equity_now = V('equity_1h26') - V('nci_1h26')
_book_eq = (justified_pb * book_equity_now) * (1 + ke_rating) ** ANCHOR_YEARS
BOOK = dict(roe_fy25=roe_fy25, roe_historical=float(roe_historical),
            roe_forecast_2030=float(roe_forecast_2030), roe_forecast_mean=roe_forecast_mean,
            roe_sustainable=float(roe_sustainable), justified_pb=justified_pb,
            cost_of_equity=ke_rating, growth=g_book, book_equity=book_equity_now,
            equity_value=_book_eq,
            value_per_share_usd=_book_eq / shares_out_k,
            value_per_share_aed=_book_eq / shares_out_k * V('fx_aed_usd'),
            current_pb=mkt_cap / book_equity_now)

# --- normalised earnings power ------------------------------------------------
# What the fleet ALREADY INSTALLED earns at the margin the company itself guides
# to, capitalised in perpetuity with no growth credited at all. This lens is the
# floor of the set, and the first edition failed it in three separate places, each
# of which made the floor higher than a floor can be. All three are corrected here.
#
#   (1) IT CAPITALISED AT A GROWTH-ADJUSTED RATE. The first edition divided by
#       (WACC minus the terminal growth rate) while the text beside it said no
#       growth was credited. A denominator of WACC-minus-g IS the growth credit:
#       there is no other reason for the g to be there. A lens that credits no
#       growth divides by the cost of capital, full stop. This is the single
#       largest correction in the whole response and it is conceded in full.
#   (2) IT PRICED A FLEET THAT IS NOT INSTALLED YET. It carried 14 island rigs
#       and the 70 integrated-drilling-services rigs the company TARGETS for the
#       end of 2026. At 30 June 2026 the company disclosed 13 island rigs and 61
#       integrated rigs. A target is growth. The installed count is what an
#       installed-fleet lens may price.
#   (3) IT CHARGED LESS DEPRECIATION THAN THE FLEET IT PRICED CARRIES. It set
#       normalised depreciation halfway between maintenance capital expenditure
#       and the 2030 charge, which is the charge on a fleet larger than the one
#       being valued. The fleet priced here is the fleet at 30 June 2026, so the
#       depreciation is what that fleet carries: the annualised 1H-2026 charge.
norm_units = dict(onshore=V('rigs_onshore_fy25'), regional=V('rigs_regional_2q26'),
                  jackup=V('rigs_jackup_fy25'), island=V('rigs_island_2q26'),
                  ids=V('ids_2q26') + V('discrete_2q26'))
norm_rev = (norm_units['onshore'] * UNITS_H[2025]['rev_per_onshore_rig']
            + norm_units['regional'] * V('rev_per_rig_regional')
            + norm_units['jackup'] * REV_PER_JACKUP_25
            + norm_units['island'] * REV_PER_ISLAND_25
            + norm_units['ids'] * OFS_REV_PER_SERVED[2025])
# The normalised margin is the company's own FY2026 guided group EBITDA margin —
# the midpoint of the $2.2-2.3bn EBITDA range over the ~$5bn revenue guide. That
# is deliberately the GROUP margin, not the "circa 50%" domestic-conventional
# margin management guides to separately: the installed fleet priced here
# includes the low-margin oilfield-services book, so applying the conventional-only
# margin to the whole revenue base would double-count the mix.
norm_margin = (V('g26_ebitda_lo') + V('g26_ebitda_hi')) / 2 / V('g26_revenue')
norm_ebitda = norm_rev * norm_margin
# Depreciation is the charge the fleet being priced actually carries: the 1H-2026
# charge, annualised, which is measured on that fleet and no other. Two reference
# points are carried beside it so the choice is visible rather than asserted —
# maintenance capital expenditure, which is the floor a flat fleet must still
# spend, and the 2030 charge, which belongs to a larger fleet this lens is not
# permitted to price.
norm_dna = V('dna_1h26') * 2
norm_dna_maintenance_floor = V('g_maint_capex')
norm_dna_2030_reference = CASE['A']['rows'][-1]['dna']
norm_ebit = norm_ebitda - norm_dna
norm_nopat = norm_ebit * (1 - V('tax_rate'))
norm_rate = WACC                      # no growth credited means no g in the denominator
norm_ev = norm_nopat / norm_rate
norm_bridge = bridge(norm_ev, detail=True)
NORMALISED = dict(units=norm_units, revenue=norm_rev, ebitda=norm_ebitda,
                  ebitda_margin=norm_ebitda / norm_rev, dna=norm_dna,
                  dna_maintenance_floor=norm_dna_maintenance_floor,
                  dna_2030_reference=norm_dna_2030_reference,
                  ebit=norm_ebit,
                  nopat=norm_nopat, capitalisation_rate=norm_rate,
                  enterprise_value=norm_ev, bridge=norm_bridge,
                  equity_value=norm_bridge['equity_value'],
                  value_per_share_usd=norm_bridge['value_per_share_usd'],
                  value_per_share_aed=norm_bridge['value_per_share_aed'])

# ============================ SENSITIVITY ====================================
def revalue(wacc=None, g=None, margin_shift=0.0, case='A'):
    w = WACC if wacc is None else wacc
    gg = TERMINAL_G[case] if g is None else g
    rows = CASE[case]['rows']
    pv, tot = 0.0, None
    for n, r in enumerate(rows, start=1):
        eb = r['ebitda_ex_jv'] + margin_shift * r['revenue']
        ebit = eb - r['dna']
        nopat = ebit * (1 - V('tax_rate'))
        f = nopat + r['dna'] - r['capex'] - r['delta_wc']
        pv += f / (1 + w) ** n
        tot = nopat
    nopat_t1 = tot * (1 + gg)
    # The terminal rate follows the same rule the base case follows: the terminal
    # capital structure, not today's. A sensitivity that moved the weighted cost
    # of capital but left the terminal rate behind would be measuring something
    # the model does not do.
    t_rate = w
    tv = nopat_t1 * (1 - gg / V('terminal_roic')) / (t_rate - gg)
    ev_dec25 = pv + tv / (1 + w) ** len(rows)
    return bridge(ev_dec25 * (1 + w) ** STUB_YEARS
                  - FCFF_1H26 * (1 + w) ** (STUB_YEARS / 2))


WACC_GRID = [round(WACC + d, 6) for d in (-0.010, -0.005, 0.0, 0.005, 0.010)]
G_GRID = [0.010, 0.015, 0.020, 0.025, 0.030]
SENS = dict(
    wacc_grid=WACC_GRID, g_grid=G_GRID,
    matrix=[[revalue(wacc=w, g=g) for g in G_GRID] for w in WACC_GRID],
    margin_shift=[dict(shift=s, aed=revalue(margin_shift=s))
                  for s in (-0.04, -0.02, 0.0, 0.02, 0.04)],
    beta_grid=[dict(beta=b,
                    aed=revalue(wacc=(mkt_cap / (mkt_cap + gross_debt_now))
                                * (rf_star + b * V('erp_rating'))
                                + (gross_debt_now / (mkt_cap + gross_debt_now)) * kd_after_tax))
               # The grid spans the whole robustness set: the equal-weight-composite
               # beta at the bottom, the adopted index beta in the middle, and the
               # top of its own 90% interval — which reaches 1.01 — at the top.
               for b in (0.50, 0.664, 0.795, 0.90, 1.01)],
)

# ============================ ASSERTS ========================================
assert 0 < WACC < 0.20, WACC
assert wacc_rating < ke_rating and kd_after_tax < wacc_rating, "glide out of order"
assert kd_pretax > sovereign_floor, ("marginal cost of debt must exceed the sovereign",
                                     kd_pretax, sovereign_floor)
assert kd_pretax > rf_star * 0.5, "cost of debt implausibly low"
for c in ('A', 'B'):
    r = CASE[c]
    assert r['terminal_growth'] < r['terminal_rate'], (c, "terminal growth exceeds its rate")
    assert 0 < r['reinvestment_rate'] < 1, (c, r['reinvestment_rate'])
    _b = r['bridge']
    assert abs(_b['equity_30jun26'] - (r['enterprise_value'] + V('jvinv_1h26') + V('cash_1h26')
                                      - V('debt_1h26') - V('lease_1h26')
                                      - V('finliab_1h26'))) < 1.0, (c, "bridge does not close")
    # the minority is deducted exactly once, through the put and not also as NCI
    assert 'nci' not in _b, (c, "the bridge must not carry a separate minority deduction")
    assert 0.3 < r['tv_pct_of_ev'] < 0.95, (c, r['tv_pct_of_ev'])
    dfs = [x['discount_factor'] for x in r['rows']]
    assert all(dfs[i] > dfs[i + 1] for i in range(len(dfs) - 1)), "discount factors not decreasing"
    for x in r['rows']:
        assert abs(x['ebit'] - (x['ebitda_ex_jv'] - x['dna'])) < 1e-6
        assert abs(x['nopat'] - x['ebit'] * (1 - V('tax_rate'))) < 1e-6
        assert abs(x['fcff'] - (x['nopat'] + x['dna'] - x['capex'] - x['delta_wc'])) < 1e-6
        assert abs(x['pv_fcff'] - x['fcff'] * x['discount_factor']) < 1e-6
        # the forecast balance sheet must balance, and the residual equity must
        # agree with the independently rolled-forward equity
        b = x['balance_sheet']
        assert abs(b['balance_check']) < 25.0, (c, x['year'], "balance sheet does not tie",
                                                b['balance_check'])
        assert abs(b['total_assets'] - (b['total_liabilities'] + b['equity_residual']
                                        + b['nci'])) < 1e-6
        assert x['revenue'] > 0 and x['ebitda'] > 0 and x['cash_close'] > 0
# FY2026 build must reconcile to the company's own guidance
g26 = CASE['A']['rows'][0]
assert abs(g26['revenue'] / V('g26_revenue') - 1) < 0.06, ("FY26 revenue vs guidance",
                                                           g26['revenue'])
assert abs(g26['ebitda'] / ebitda_fy26 - 1) < 0.10, ("FY26 EBITDA vs guidance", g26['ebitda'])

# ============================ OUTPUT =========================================
FAIR = {
    'dcf_A': CASE['A']['value_per_share_aed'],
    'dcf_B': CASE['B']['value_per_share_aed'],
    'relative': RELATIVE['value_per_share_aed'],
    'book': BOOK['value_per_share_aed'],
    'normalised': NORMALISED['value_per_share_aed'],
}


def _quartiles(vals):
    v = sorted(x for x in vals if x)
    n = len(v)
    return v[max(0, n // 4 - 1)], v[min(n - 1, (3 * n) // 4)]


def _pb_at(ke):
    return ((roe_sustainable - g_book) / (ke - g_book) * book_equity_now
            * (1 + ke) ** ANCHOR_YEARS) / shares_out_k * V('fx_aed_usd')


_rel_lo_mult, _rel_hi_mult = _quartiles([r['ev_ebitda'] for r in peer_rows])
_norm_lo = norm_rev * (norm_margin - 0.02)
_norm_hi = norm_rev * (norm_margin + 0.02)


def _norm_ps(eb):
    return bridge((eb - norm_dna) * (1 - V('tax_rate')) / norm_rate)


def _rel_ps(mult):
    return bridge(mult * ltm_ebitda_ex_jv)


# Bear and bull for each lens are the SAME lens re-run on a stated stress, not a
# judgement layered on top of the base: the discounted-cash-flow bands move the
# cost of capital 50 basis points either way, the relative band is the peer set's
# own interquartile range of enterprise value to EBITDA, the book band moves the
# cost of equity 50 basis points, and the normalised band moves the margin two
# points.
LENS_RANGE = dict(
    dcf_A=dict(bear=revalue(wacc=WACC + 0.005, case='A'), base=FAIR['dcf_A'],
               bull=revalue(wacc=WACC - 0.005, case='A')),
    dcf_B=dict(bear=revalue(wacc=WACC + 0.005, case='B'), base=FAIR['dcf_B'],
               bull=revalue(wacc=WACC - 0.005, case='B')),
    relative=dict(bear=_rel_ps(_rel_lo_mult), base=FAIR['relative'],
                  bull=_rel_ps(_rel_hi_mult)),
    book=dict(bear=_pb_at(ke_rating + 0.005), base=FAIR['book'],
              bull=_pb_at(ke_rating - 0.005)),
    normalised=dict(bear=_norm_ps(_norm_lo), base=FAIR['normalised'],
                    bull=_norm_ps(_norm_hi)),
)
LENS_WEIGHT = dict(dcf_A=0.25, dcf_B=0.25, relative=0.20, book=0.15, normalised=0.15)
central = sum(FAIR[k] * LENS_WEIGHT[k] for k in FAIR)
lo, hi = min(FAIR.values()), max(FAIR.values())

OUT = dict(
    # THE ANSWER, WHERE THE SHARED READER LOOKS FOR IT. [R-GAP-01]'s gate reads a study's
    # own numbers for a central and the spot it was struck at; this study carried both at
    # fair_value.central and fair_value.spot, where that reader does not look, so the gate
    # could say nothing about this name at all and it sat on the unreadable list. AN
    # UNREADABLE STUDY IS NOT A CLEAN STUDY [R-ENF-04], and here the invisibility and the
    # defect are the same event: nothing was looking at the number, so nothing asked why
    # three lenses that value a franchise at historical cost were carrying half the weight.
    #
    # Both figures are in DIRHAMS, the listing currency, because the gate substitutes the
    # LATEST KNOWN price for the struck spot and that price comes from the supplied close
    # register in the currency the shares trade in — not the dollars this study models in.
    # Nothing here is a new answer and nothing here endorses the five-lens blend that
    # produces the central: [R-LENS-03] retires it and this study stays on the lens
    # ratchet. What the gate audits is the answer a reader actually receives.
    central=central,
    spot=V('spot_aed'),
    meta=dict(ticker='ADNOCDRILL', market='AE', exchange='Abu Dhabi Securities Exchange',
              company='ADNOC Drilling Company P.J.S.C.',
              reporting_currency='USD', listing_currency='AED',
              sector='Energy Equipment & Services — contract drilling and oilfield services',
              company_class='Operating company (asset-heavy contract driller with an integrated '
                            'oilfield-services arm)',
              units='USD thousands unless stated', anchor_date='2026-08-07',
              study_date='2026-08-09'),
    inputs={k: v for k, v in INP.items()},
    history=H, units_history=UNITS_H,
    fleet_plan=FLEET, capex_plan=CAPEX_PLAN, terminal_growth=TERMINAL_G,
    unconv_margin_triangulation=UNCONV_MARGIN_TRIANGULATION,
    unit_economics=dict(rev_per_jackup_fy25=REV_PER_JACKUP_25,
                        rev_per_island_fy25=REV_PER_ISLAND_25,
                        island_to_jackup_ratio=ISLAND_TO_JACKUP,
                        conventional_cost_stack_fy25=CONV_STACK_FY25,
                        cost_driver=COST_DRIVER, cost_escalator=COST_ESCALATOR,
                        base_units_fy25=BASE_UNITS_25,
                        depreciation_rate=DEP_RATE, wc_pct_revenue=float(WC_PCT_REVENUE),
                        wc_pct_revenue_organic=float(WC_PCT_REVENUE_ORGANIC),
                        wc_pct_revenue_historical=WC_PCT_REVENUE_HIST,
                        wc_1h26=float(WC_1H26), wc_acquired=float(WC_ACQUIRED),
                        rev_1h26_annualised=float(REV_1H26_ANNUALISED),
                        ofs_served={str(k): v for k, v in OFS_SERVED.items()},
                        ofs_conventional_revenue={str(k): v for k, v in OFS_CONV.items()},
                        ofs_rev_per_served={str(k): v for k, v in OFS_REV_PER_SERVED.items()},
                        ofs_intensity_realised=float(OFS_INTENSITY_REALISED),
                        segment_calibration=CALIB,
                        segment_uncalibrated=CALIB_UNCALIBRATED,
                        acquisition_entry=ACQ_ENTRY,
                        ofs_solve_infeasible=OFS_SOLVE_INFEASIBLE,
                        gna_ex_da_fy25=GNA_EX_DA_FY25,
                        fcff_1h26=FCFF_1H26, stub_years=STUB_YEARS,
                        anchor_years=ANCHOR_YEARS,
                        unconventional_cost_fy25=unconv_cost_fy25),
    wacc=dict(rf_observed=V('ust10'), us_default_spread=V('us_default_spread'), rf_star=rf_star,
              beta=BETA, erp_rating=V('erp_rating'), erp_cds=V('erp_cds'),
              ke_rating=ke_rating, ke_cds=ke_cds,
              kd_candidates=KD_CANDIDATES, kd_passing_sovereign_floor=list(KD_PASS),
              sovereign_floor=sovereign_floor, kd_pretax=kd_pretax, kd_after_tax=kd_after_tax,
              tax_rate=V('tax_rate'), market_cap=mkt_cap, net_debt=net_debt_now,
              gross_debt=gross_debt_now,
              weight_equity=w_e, weight_debt=w_d,
              wacc_rating=wacc_rating, wacc_cds=wacc_cds, wacc_used=WACC),
    market=dict(spot_aed=V('spot_aed'), spot_usd=spot_usd, fx=V('fx_aed_usd'),
                shares_outstanding_k=shares_out_k, market_cap_usd_k=mkt_cap,
                enterprise_value_usd_k=mkt_cap + net_debt_now,
                net_debt_usd_k=net_debt_now),
    cases=CASE, relative=RELATIVE, book=BOOK, normalised=NORMALISED, sensitivity=SENS,
    fair_value=dict(by_lens=FAIR, weights=LENS_WEIGHT, central=central, low=lo, high=hi,
                    spot=V('spot_aed'), upside_central=central / V('spot_aed') - 1,
                    lens_range=LENS_RANGE,
                    central_range=dict(
                        bear=sum(LENS_RANGE[k]['bear'] * LENS_WEIGHT[k] for k in LENS_RANGE),
                        base=central,
                        bull=sum(LENS_RANGE[k]['bull'] * LENS_WEIGHT[k] for k in LENS_RANGE))),
    register=REGISTER,
)


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return float(o)
    return o


if __name__ == '__main__':
    with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
        json.dump(_clean(OUT), f, indent=1)
    print(f"WACC {WACC:.4%} (rating) / {wacc_cds:.4%} (CDS) | Ke {ke_rating:.4%} | "
          f"Kd pre-tax {kd_pretax:.4%} | beta {BETA:.3f} | We {w_e:.1%}")
    print(f"FY26 build revenue {g26['revenue']/1e6:.3f}bn vs guidance "
          f"{V('g26_revenue')/1e6:.2f}bn | EBITDA {g26['ebitda']/1e6:.3f}bn vs "
          f"{ebitda_fy26/1e6:.3f}bn | margin {g26['ebitda_margin']:.1%}")
    for c in ('A', 'B'):
        r = CASE[c]
        print(f"  Case {c}: EV {r['enterprise_value']/1e6:.2f}bn  TV {r['tv_pct_of_ev']:.1%} of EV"
              f"  equity {r['equity_value']/1e6:.2f}bn  AED {r['value_per_share_aed']:.2f}/sh")
    print(f"  Relative  AED {RELATIVE['value_per_share_aed']:.2f} "
          f"(blended {RELATIVE['blended_multiple']:.2f}x vs own {RELATIVE['implied_own_ev_ebitda']:.2f}x)")
    print(f"  Book      AED {BOOK['value_per_share_aed']:.2f} (justified P/B {BOOK['justified_pb']:.2f}x, "
          f"current {BOOK['current_pb']:.2f}x)")
    print(f"  Normalised AED {NORMALISED['value_per_share_aed']:.2f}")
    print(f"  CENTRAL AED {central:.2f} vs spot {V('spot_aed'):.2f} "
          f"({central/V('spot_aed')-1:+.1%}) | range {lo:.2f}-{hi:.2f}")
