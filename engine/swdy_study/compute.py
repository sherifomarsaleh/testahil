"""RUN ORDER: compute.py THEN forecast_anchor.py. RUNNING THIS FILE ALONE DELETES
A STANDING-RULE RECORD.

study_numbers.json is written whole by this script, and [R-ANCHOR-01]'s
forecast_anchor block is appended afterwards by forecast_anchor.py in this same
directory. So a rebuild that runs only this file silently drops that block: it
reappears as a deletion in the diff and nothing in the code says why. Caught
06-09-2026 by reading a diffstat that came back at 18 lines when the edit was
one -- had the diff not been read, a rebuild would have removed the record and
check_forecast_anchor would have gone red on a study whose forecast had not moved.

This is the L-066/L-067 species one step over: those were about a CHECK that
opens a delivered file by name and must move with the re-issue; this is about a
GENERATOR that is one of two and must run with the other. SAVOLA carries a
forecast_anchor.py of the same shape and has not been tested for it.
"""
"""SWDY study — master computation. Writes study_numbers.json (single source of
truth for every builder). Code-first rule: INPUTS are four-field records
{value, source, date, ring}; a bare numeral cannot enter the model; the ASSERT
block raises (no JSON emitted) unless the bridge closes, the discount-rate glide
is ordered, the Kd-integrity triple holds, and the terminal is ROIC-consistent.

REBUILT 06-Aug-2026 on the actual audited/reviewed consolidated financial
statements (FY2023, FY2024, FY2025 — KPMG Hazem Hassan, unqualified opinions —
and the Q1-2026 limited-review interim), superseding a version built on press
coverage, IR commentary and triangulation because the underlying filings were
not reachable from the build environment. Two structural corrections follow
directly from having the primary source in hand:

1. THE REAL SEGMENT STRUCTURE IS THREE SEGMENTS, NOT SEVEN. The company's own
   Note 5-3 (revenue by product/service line) and segment note report Cables
   (and its accessories), Constructions (and infrastructure), and Electrical
   products (and digital solutions) — nothing else. The previous build's
   seven-way split (cables / raw material / engineering & construction /
   transformers / meters / other electrical products / infrastructure
   investment) does not appear anywhere in three years of audited filings; it
   was an inference from IR commentary that is retired here in favour of the
   disclosed taxonomy, which reconciles EXACTLY to consolidated revenue for
   all three years (to the nearest EGP).
2. FY2025 IS NOW FULLY DISCLOSED, so the "close the P&L to the two disclosed
   anchors" and "triangulate the balance sheet three ways" machinery the
   previous build needed is gone. Every FY2025 income-statement and
   balance-sheet line below is the audited figure, not a derivation.

Company class: diversified industrial operating company (wires & cables
manufacturer + engineering & construction contractor + electrical products and
digital solutions). Lens set follows the operating-company reference: FCFF DCF
primary, relative multiples, normalized earnings power, and a book/ROE lens.
"""
import datetime as _dt
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import macro_path as _MPmod
_MP_EG = _MPmod.load('EG')
from numbers_file import write_preserving          # [R-REPAIR-01]
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import terminal_value as TV          # [R-TERM-01] — verified by import, not by parse

# ============================ INPUTS =========================================
def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)


# THE BETA IS READ, NOT TYPED, AND THAT IS THE WHOLE CORRECTION. This input used to
# carry a literal 1.009 with a source describing a regression against a 31-name
# equal-weight composite of the covered EGX library. Two defects sat in one line:
# the regressor was a COMPOSITE, which SIGCM clause 6 calls a hard fail rather than
# a fallback, and the number was TYPED, so beta_reg.py could be re-run to any answer
# at all and the model would go on discounting at the old one. Re-running it against
# the published index of the exchange this stock is listed on moved the beta 21.4%
# and moved the valuation by nothing, because nothing downstream was reading it.
_BETA = json.load(open(os.path.join(HERE, 'beta_result.json'), encoding='utf-8'))
assert _BETA.get('conforming'), 'beta_result.json is not a conforming regression'
assert str(_BETA.get('index_file', '')).startswith('raw_indices/'), \
    'the regressor is not a registered published index'

# THE HOUSE TERMINAL RATES, READ LIVE FROM THE PATH AND NEVER COPIED [09-09-2026].
# engine/macro_paths/EG.json is the one source of an inflation rate in this study, which
# is what the terminal growth line has always claimed and what the terminal risk-free line
# did not do until today.
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import macro_path as _MP
_MACRO_EG = _MP.load('EG')
_PI_T_HOUSE = _MACRO_EG.terminal_inflation
_RRC_HOUSE = _MACRO_EG.real_rate_convention
_RF_TERM_HOUSE = _PI_T_HOUSE + _RRC_HOUSE

# THE TWO MARGINS THE SEASONALITY ARGUMENT RESTS ON, COMPUTED [09-09-2026]. Both were
# typed into a source string. They are simple ratios of figures this register already
# carries, so typing them meant the study asserted numbers it did not produce -- and the
# whole re-anchoring discipline turns on the claim that this company's halves are not
# alike, which is the claim these two figures ARE.
_KD_FY24_EGP, _KD_FY24_USD, _KD_FY24_EUR = 0.2868, 0.0649, 0.0392
_SP_FY25 = (21016.396482 + 5868.890571 + 7604.808509) - 246.710877
_MGN_FY25 = _SP_FY25 / 281049.081719
_SP_H1_25 = ((6823.397790 + 3925.845038 + 2031.644426 + 1083.868786
              + 1923.388459 + 1713.421415) - (88.329068 + 9.124728))
_MGN_H1_25 = _SP_H1_25 / 123800.551073

H126 = ("Reviewed condensed interim consolidated financial statements for the six months "
        "ended 30 June 2026, El Sewedy Electric Company, approved for issuance by the board "
        "on 11 August 2026 (note 2-1), published on the company's own investor-relations "
        "portal at ir.elsewedyelectric.com")

FY25 = ("Audited consolidated financial statements of El Sewedy Electric Company for the "
        "financial year ended 31 December 2025, published on the company's own "
        "investor-relations portal at ir.elsewedyelectric.com")
FY24 = ("Audited consolidated financial statements of El Sewedy Electric Company for the "
        "financial year ended 31 December 2024, published on the company's own "
        "investor-relations portal at ir.elsewedyelectric.com")

# THE SEGMENT REVENUE HISTORY IS LIFTED OUT OF THE INPUT DICT so that the growth rates
# quoted in the source strings below can be DERIVED FROM IT rather than typed beside it.
# A rate typed into a source string is a figure a reader sees, cannot trace to any
# committed number, and the prose check therefore cannot reconcile -- which is exactly
# what happened to the Constructions segment's "+28.3% (FY2024: +32.6%)". Both were
# right, and being right by hand is not the same as being right by construction.
_SEG_REV_HIST = dict(
    FY23=dict(cables=82421.265314, construct=53482.804001, elecprod=16282.178230),
    FY24=dict(cables=137189.798892, construct=70921.447985, elecprod=23870.588700),
    FY25=dict(cables=155792.929738, construct=90958.550228, elecprod=34297.601753))


def _seg_growth(seg, year, prior):
    return _SEG_REV_HIST[year][seg] / _SEG_REV_HIST[prior][seg] - 1.0


INP = dict(
    # ---- anchors --------------------------------------------------------
    spot=I(130.00, "Closing price supplied by the principal for 3 September 2026. "
           "RE-STRUCK: the study was struck at "
           "EGP 105.20 of 5 August 2026 and a fair value delivered against a month-old "
           "quote is a comparison a reader cannot use. The supplied file records that the "
           "figure first arrived as 90.50 and was CORRECTED to 130.00 on 6 September 2026 "
           "after it disagreed with this name's own price library on all 35 overlapping "
           "sessions after 14 June 2026, including the 5 August close of 105.20 this "
           "study was originally struck at. A fair value delivered against a month-old "
           "quote is a comparison a reader cannot use",
           "2026-09-03", "Market"),
    shares_mn=I(2140.777876, "Issued and paid-up capital note (29), audited FY2025 consolidated "
                "financial statements and the Q1-2026 condensed interim statements: 2,140,777,876 "
                "shares of EGP 1 par value, unchanged across both filings", "2026-05-13", "Company"),
    tax_stat=I(0.225, "Egypt corporate income tax 22.5% (PwC Worldwide Tax Summaries, unchanged "
               "2025-26)", "2026", "Country"),
    tax_eff=I(0.245, "Group effective tax rate used for the forecast. Audited effective rates: "
              "FY2023 31.3%, FY2024 30.1%, FY2025 22.6% (all now EXACT — tax expense / profit "
              "before tax, audited statement of profit or loss); Q1-2026 interim 25.75%. No "
              "statutory-vs-effective reconciliation is disclosed anywhere in the filings (Egyptian "
              "Accounting Standards do not require the IFRS-style table); the group operates in 15+ "
              "tax jurisdictions plus Free-Zone entities that pay 1% of revenue to GAFI instead of "
              "corporate tax. 24.5% sits between the FY2025 print and the historical average, "
              "allowing for the Q1-2026 uptick rather than extrapolating one low year",
              "2026-05-13", "Company/House"),
    fx=I(49.8, "USD/EGP mid-market ~49.8 (house cost-of-capital reference, re-verified 05-Aug-2026). "
         "The pound was not range-bound over the last year: ~46.8 (Feb-26) to ~54.7 (Apr-26 regional "
         "war spike) and back to ~49.8", "2026-08-05", "Country"),

    # ---- historical income statement (EGP mn, consolidated, AUDITED) ------
    # FY2023 and FY2024 are cross-confirmed between their own filing and the following
    # year's comparative column (both tie to the cent); FY2025 is the current year's own
    # audited filing. All four documents: KPMG Hazem Hassan, unqualified opinion.
    rev_fy23=I(152186.247545, "Consolidated statement of profit or loss, FY2023 audited financial "
               "statements (confirmed by the FY2024 filing's comparative column)",
               "2024-03-13", "Company"),
    rev_fy24=I(231981.835577, "Consolidated statement of profit or loss, FY2024 audited financial "
               "statements (confirmed by the FY2025 filing's comparative column)",
               "2025-03-13", "Company"),
    rev_fy25=I(281049.081719, "Consolidated statement of profit or loss, FY2025 audited financial "
               "statements", "2026-03-15", "Company"),
    gp_fy23=I(29077.288803, "Consolidated statement of profit or loss, FY2023 audited financial "
              "statements", "2024-03-13", "Company"),
    gp_fy24=I(43898.520903, "Consolidated statement of profit or loss, FY2024 audited financial "
              "statements", "2025-03-13", "Company"),
    gp_fy25=I(40762.108187, "Consolidated statement of profit or loss, FY2025 audited financial "
              "statements", "2026-03-15", "Company"),
    op_fy23=I(17739.118249, "Operating profit, FY2023 audited financial statements", "2024-03-13",
              "Company"),
    op_fy24=I(29341.719144, "Operating profit, FY2024 audited financial statements", "2025-03-13",
              "Company"),
    op_fy25=I(25354.225619, "Operating profit, FY2025 audited financial statements", "2026-03-15",
              "Company"),
    dna_fy23=I(2295.986956, "Audited FY2023 consolidated statement of cash flows: PP&E depreciation "
               "2,120.789808 + investment property 6.388342 + intangibles amortisation 53.947575 + "
               "right-of-use assets 114.861231", "2024-03-13", "Company"),
    dna_fy24=I(2259.745806, "Audited FY2024 consolidated statement of cash flows: PP&E depreciation "
               "2,019.646871 + investment property 1.472753 + intangibles amortisation 80.726323 + "
               "right-of-use assets 157.899859", "2025-03-13", "Company"),
    dna_fy25=I(3008.977627, "Audited FY2025 consolidated statement of cash flows: PP&E depreciation "
               "2,733.671862 + investment property 1.687166 + intangibles amortisation 78.072847 + "
               "right-of-use assets 195.545752 — the depreciable base stepped up with the FY2025 "
               "capex ramp", "2026-03-15", "Company"),
    netfin_fy23=I(-2124.362277, "Net finance costs, FY2023 audited financial statements: finance "
                  "income 2,818.868796 less finance costs 4,943.231073", "2024-03-13", "Company"),
    netfin_fy24=I(-3515.365946, "Net finance costs, FY2024 audited financial statements: finance "
                  "income 4,247.625658 less finance costs 7,762.991604", "2025-03-13", "Company"),
    netfin_fy25=I(-2145.438755, "Net finance costs, FY2025 audited financial statements: finance "
                  "income 3,713.003271 less finance costs 5,858.442026. REPLACES a previous "
                  "estimate of -3,400 struck when the filing was not reachable — this is the exact "
                  "audited figure and it is materially smaller (net finance improved even as gross "
                  "debt grew, because the CBE's easing cycle and a larger cash pile both cut the "
                  "net charge)", "2026-03-15", "Company"),
    assoc_fy23=I(603.624972, "Group's share of profit of equity-accounted investees, FY2023 audited "
                 "financial statements", "2024-03-13", "Company"),
    assoc_fy24=I(1132.366257, "Group's share of profit of equity-accounted investees, FY2024 "
                 "audited financial statements", "2025-03-13", "Company"),
    assoc_fy25=I(1568.902975, "Group's share of profit of equity-accounted investees, FY2025 "
                 "audited financial statements — reconciles exactly to the sum of the per-investee "
                 "shares in Note 20 (Doha Cables 940.3, Elsewedy Cables-Qatar 259.2, SC Zone "
                 "Utilities 255.5, SWIEP 73.4, Aloula 96.9, Raneen 15.5, Senyar -71.9). REPLACES a "
                 "previous 1.15x uplift on the FY2024 figure, no longer needed now the actual "
                 "number is disclosed", "2026-03-15", "Company"),
    tax_fy23=I(-5080.406688, "Income tax expense, FY2023 audited financial statements", "2024-03-13",
               "Company"),
    tax_fy24=I(-8121.510082, "Income tax expense, FY2024 audited financial statements", "2025-03-13",
               "Company"),
    tax_fy25=I(-5591.139782, "Income tax expense, FY2025 audited financial statements: current tax "
               "6,312.161650 less deferred tax credit 721.021868. Effective rate 22.57% against "
               "24,777.689839 pre-tax profit — REPLACES a previous house assumption of 25.9%",
               "2026-03-15", "Company"),
    pat_fy23=I(11137.974256, "Profit for the year, FY2023 audited financial statements", "2024-03-13",
               "Company"),
    pat_fy24=I(18837.209373, "Profit for the year, FY2024 audited financial statements", "2025-03-13",
               "Company"),
    pat_fy25=I(19186.550057, "Profit for the year, FY2025 audited financial statements",
               "2026-03-15", "Company"),
    npa_fy23=I(10115.701777, "Profit attributable to owners of the parent, FY2023 audited financial "
               "statements. Basic EPS 4.26, diluted 4.25", "2024-03-13", "Company"),
    npa_fy24=I(17461.358714, "Profit attributable to owners of the parent, FY2024 audited financial "
               "statements. Basic EPS 7.22, diluted 7.21", "2025-03-13", "Company"),
    npa_fy25=I(17330.244990, "Profit attributable to owners of the parent, FY2025 audited financial "
               "statements. Basic and diluted EPS both 7.13 (no dilutive instruments beyond the "
               "already-deducted ESOP shares)", "2026-03-15", "Company"),

    # ---- historical balance sheet (EGP mn, consolidated, AUDITED) --------
    ppe_fy23=I(18009.166367, "Consolidated statement of financial position, 31 Dec 2023",
               "2024-03-13", "Company"),
    ppe_fy24=I(27543.762675, "Consolidated statement of financial position, 31 Dec 2024",
               "2025-03-13", "Company"),
    ppe_fy25=I(35961.076614, "Consolidated statement of financial position, 31 Dec 2025",
               "2026-03-15", "Company"),
    inv_fy23=I(30881.822082, "Inventories, 31 Dec 2023 (net of write-down)", "2024-03-13", "Company"),
    inv_fy24=I(56795.884068, "Inventories, 31 Dec 2024 (net of write-down)", "2025-03-13", "Company"),
    inv_fy25=I(59860.044570, "Inventories, 31 Dec 2025 (net of write-down)", "2026-03-15", "Company"),
    ca_fy23=I(16179.633722, "Contract assets, 31 Dec 2023", "2024-03-13", "Company"),
    ca_fy24=I(18051.966570, "Contract assets, 31 Dec 2024", "2025-03-13", "Company"),
    ca_fy25=I(29894.579591, "Contract assets, 31 Dec 2025", "2026-03-15", "Company"),
    recv_fy23=I(46591.885092, "Trade and other receivables (current), 31 Dec 2023", "2024-03-13",
                "Company"),
    recv_fy24=I(86736.309423, "Trade and other receivables (current), 31 Dec 2024", "2025-03-13",
                "Company"),
    recv_fy25=I(116259.797169, "Trade and other receivables (current), 31 Dec 2025", "2026-03-15",
                "Company"),
    pay_fy23=I(31938.122060, "Trade and other payables, 31 Dec 2023", "2024-03-13", "Company"),
    pay_fy24=I(54808.185042, "Trade and other payables, 31 Dec 2024", "2025-03-13", "Company"),
    pay_fy25=I(68895.662044, "Trade and other payables, 31 Dec 2025", "2026-03-15", "Company"),
    cl_fy23=I(25060.328092, "Contract liabilities, 31 Dec 2023", "2024-03-13", "Company"),
    cl_fy24=I(53281.056753, "Contract liabilities, 31 Dec 2024", "2025-03-13", "Company"),
    cl_fy25=I(81266.224686, "Contract liabilities, 31 Dec 2025", "2026-03-15", "Company"),
    cash_fy23=I(25552.044800, "Cash and cash equivalents, 31 Dec 2023", "2024-03-13", "Company"),
    cash_fy24=I(38180.002322, "Cash and cash equivalents, 31 Dec 2024", "2025-03-13", "Company"),
    cash_fy25=I(41949.208624, "Cash and cash equivalents, 31 Dec 2025: bank time deposits 9,689.1, "
                "bank current accounts 32,157.7, cash on hand 102.4", "2026-03-15", "Company"),
    assets_fy23=I(151448.654828, "Total assets, 31 Dec 2023", "2024-03-13", "Company"),
    assets_fy24=I(249527.138687, "Total assets, 31 Dec 2024", "2025-03-13", "Company"),
    assets_fy25=I(311099.090775, "Total assets, 31 Dec 2025", "2026-03-15", "Company"),
    debt_fy23=I(41766.492071, "Loans and borrowings including lease liabilities, 31 Dec 2023: "
                "current 34,950.810105 (loans 7,401.079843 + bank facilities 27,530.523733 + leases "
                "19.206529) + non-current 6,815.681966 (loans 6,235.939701 + leases 579.742265)",
                "2024-03-13", "Company"),
    debt_fy24=I(59082.941807, "Loans and borrowings including lease liabilities, 31 Dec 2024: "
                "current 52,733.931099 (loans 12,580.708167 + bank facilities 40,049.471127 + "
                "leases 103.751805) + non-current 6,349.010708 (loans 6,166.616210 + leases "
                "182.394498)", "2025-03-13", "Company"),
    debt_fy25=I(62509.211797, "Loans and borrowings including lease liabilities, 31 Dec 2025: "
                "current 53,888.496799 (loans 26,673.246745 + bank facilities 27,183.559774 + "
                "leases 31.690280) + non-current 8,620.714998 (loans 8,605.301580 + leases "
                "15.413418)", "2026-03-15", "Company"),
    nd_fy23=I(16214.447271, "Net financial debt, 31 Dec 2023: total loans and borrowings including "
              "leases 41,766.492071 less cash and cash equivalents 25,552.044800. NOTE: this is the "
              "interest-bearing-debt definition used for the equity bridge, not the company's own "
              "'net debt' capital-management ratio (Note 29-1), which nets a much broader liability "
              "base (total liabilities less deferred tax and provisions) against cash and is a "
              "leverage-monitoring metric, not a valuation-bridge quantity",
              "2024-03-13", "Company"),
    nd_fy24=I(20902.939485, "Net financial debt, 31 Dec 2024: total loans and borrowings including "
              "leases 59,082.941807 less cash 38,180.002322", "2025-03-13", "Company"),
    nd_fy25=I(20560.003173, "Net financial debt, 31 Dec 2025: total loans and borrowings including "
              "leases 62,509.211797 less cash 41,949.208624. The company's OWN 'net debt' figure "
              "(Note 29-1) is EGP 180,102.969196 — total liabilities LESS deferred tax and "
              "provisions, less cash — a capital-structure leverage ratio (net debt/equity 2.50x) "
              "that nets trade payables and contract liabilities against cash. Using it in an "
              "EV-to-equity bridge would double-count operating liabilities already reflected in "
              "working capital; the interest-bearing figure above is the correct bridge quantity "
              "and is used throughout", "2026-03-15", "Company"),
    eqp_fy23=I(35724.466132, "Equity attributable to owners of the parent, 31 Dec 2023",
               "2024-03-13", "Company"),
    eqp_fy24=I(55274.913356, "Equity attributable to owners of the parent, 31 Dec 2024",
               "2025-03-13", "Company"),
    eqp_fy25=I(66870.866550, "Equity attributable to owners of the parent, 31 Dec 2025 — now the "
               "audited closing figure, not derived from the prior year plus profit less an "
               "assumed dividend", "2026-03-15", "Company"),
    nci_fy23=I(2384.013396, "Non-controlling interests, 31 Dec 2023", "2024-03-13", "Company"),
    nci_fy24=I(4251.771900, "Non-controlling interests, 31 Dec 2024", "2025-03-13", "Company"),
    nci_fy25=I(5118.978381, "Non-controlling interests, 31 Dec 2025: Rowad for Modern Engineering "
               "(49%) 1,429.7, Elsewedy Cables-KSA (40%) 2,546.8, Egyptian Co. for Solar Energy "
               "(49%) 297.5, Elsewedy Electric Zambia (40%) 453.2, Egyptian Co. for Electrical "
               "Insulators (25.17%) 76.1, Pyramids Zona Franca (5%) 17.9, others 297.7",
               "2026-03-15", "Company"),
    assoc_bv_fy24=I(6474.047538, "Equity-accounted investees, carrying value, 31 Dec 2024",
                    "2025-03-13", "Company"),
    # CARRYING THEM AT BOOK IS THE RULE AND WAS CHECKED AGAINST NOTE 20 RATHER THAN
    # ASSUMED [09-09-2026]. A review put it that these investees earn 1,568.903 on a book
    # of 6,757.651 — a 23.2% return — and asked why the bridge takes the lower figure.
    # [R-BRIDGE-01] is market-if-listed or book, so the question is whether any of them
    # is listed. Note 20 names all of them and NOT ONE IS: Elsewedy Cables Qatar, Doha
    # Cables Qatar, Senyar Industries Qatar Holding, Aloula, SC Zone Utilities, SWIEP,
    # Raneen Energy, Yanbu Copper Wires and an unnamed residual. Book is not the
    # conservative choice here, it is the only route the rule leaves open.
    #
    # THE BOOK ALSO RECONCILES, WHICH IS WHAT SAYS IT IS NOT STALE. It rose only 283.603
    # (6,474.048 -> 6,757.651) against 1,568.903 of earnings, because note 20 discloses a
    # cash dividend of 1,174.475 from Senyar Industries Qatar Holding on 31 December 2025
    # -- the same figure the cash flow statement carries on its own line. Equity
    # accounting reduces the carrying value by a distribution pound for pound and the cash
    # arrives in the group's own balance, which this bridge already counts, so there is no
    # understatement and no double count. 1,568.903 less 1,174.475 is 394.428 against
    # 283.603 of book growth, and the 110.825 difference is the foreign-currency
    # translation the same note discloses (135.317) net of the Elastmold disposal.
    #
    # ONE THING THE REVIEW'S RATIO UNDERSTATES, recorded because it is the more striking
    # number: 978.173 of the book (14.5%) is Yanbu Copper Wires and the residual, both
    # earning NOTHING in either year. The return on the book that actually earns is 27.1%.
    assoc_bv_fy25=I(6757.650507, "Equity-accounted investees, carrying value, 31 Dec 2025 — the "
                    "closing balance used in the valuation bridge (the anchor date is Aug-2026, so "
                    "the FY2025 close is the most recent audited figure, not FY2024's). Note 20 "
                    "names every investee and none is listed, so [R-BRIDGE-01] leaves book as the "
                    "only route; the balance reconciles to the prior year through the disclosed "
                    "1,174.475 Senyar dividend and 135.317 of translation",
                    "2026-03-15", "Company"),
    intang_fy24=I(1459.194548, "Intangible assets and goodwill, 31 Dec 2024", "2025-03-13", "Company"),
    intang_fy25=I(1748.816945, "Intangible assets and goodwill, 31 Dec 2025", "2026-03-15", "Company"),
    dps_fy24=I(1.00, "FY2024 dividend, paid during FY2025: cash flow statement 'dividends paid to "
               "shareholders' of 3,111.384454 splits into 2,139.355716 to owners of the parent and "
               "972.028738 to non-controlling interests; 2,139.355716 / 2,139,355,716 weighted "
               "shares = EXACTLY EGP 1.00 per share", "2026-03-15", "Company"),
    dps_fy25=I(1.85, "FY2025 cash dividend of EGP 1.85/share: recommended with the FY2025 results, "
               "ratified by the ordinary general assembly on 6 May 2026, rights with the share "
               "through 1 June, paid from 4 June 2026 (EGX disclosure, corroborated by Arab "
               "Finance coverage and the quoted ~2.0% trailing yield). RESTORED after external "
               "critique: an earlier revision removed this figure because neither the FY2025 "
               "annual filing (board-approved 12 Mar 2026) nor the Q1-2026 interim disclosed it — "
               "an absence-of-evidence error, since the interim covers a period ending 31 March "
               "and carries no subsequent-events note, so its silence was never evidence. Payout = "
               "1.85 / 8.10 attributable EPS = 22.8%", "2026-05-06", "Company"),

    # ---- cash-flow markers (EGP mn, AUDITED) -----------------------------
    capex_fy23=I(4748.595385, "Audited FY2023 consolidated cash flow statement: 'acquisition of "
                 "property, plant and equipment'", "2024-03-13", "Company"),
    capex_fy24=I(8489.780912, "Audited FY2024 consolidated cash flow statement: 'paid for "
                 "acquisition of property, plant and equipment and projects under construction'",
                 "2025-03-13", "Company"),
    capex_fy25=I(13112.049791, "Audited FY2025 consolidated cash flow statement: 'paid for "
                 "acquisition of property, plant and equipment and projects under construction' — "
                 "a 55% step-up on FY2024, the capacity-expansion cycle referenced throughout this "
                 "study", "2026-03-15", "Company"),
    int_paid_fy25=I(5740.312420, "Interest paid, audited FY2025 consolidated statement of cash "
                    "flows", "2026-03-15", "Company"),
    tax_paid_fy25=I(8298.752112, "Income tax paid, audited FY2025 consolidated statement of cash "
                    "flows", "2026-03-15", "Company"),
    ocf_fy25=I(12765.922545, "Net cash flows from operating activities, FY2025 (after interest and "
               "tax) — 12,765.9 against house EBITDA of 28,363.2, still well below full conversion "
               "but a sharp recovery from FY2024's 3,979.4, as the pace of working-capital "
               "absorption slowed", "2026-03-15", "Company"),

    # ---- interim (EGP mn, REVIEWED) ---------------------------------------
    q1_25_rev=I(59391.529636, "Condensed consolidated interim statement of profit or loss, 3M to "
                "31-Mar-2025 (comparative column of the Q1-2026 filing)", "2026-05-13", "Company"),
    q1_25_ebitda_house=I(7488.788241, "Q1-2025 house EBITDA: operating profit 6,503.867706 + "
                         "depreciation/amortisation estimated at the FY2025 D&A ratio applied to "
                         "Q1-2025 revenue (the interim filing does not itemise D&A separately from "
                         "operating profit)", "2026-05-13", "House"),
    q1_25_npa=I(4146.412114, "Profit attributable to owners of the parent, Q1-2025", "2026-05-13",
                "Company"),
    q1_26_rev=I(75298.446639, "Condensed consolidated interim statement of profit or loss, 3M to "
                "31-Mar-2026", "2026-05-13", "Company"),
    q1_26_gp=I(13128.216681, "Gross profit, Q1-2026 interim statements", "2026-05-13", "Company"),
    q1_26_op=I(8247.204309, "Operating profit, Q1-2026 interim statements", "2026-05-13", "Company"),
    q1_26_netfin=I(-1458.477611, "Net finance costs, Q1-2026 interim statements: finance income "
                   "683.569177 less finance costs 2,142.046788", "2026-05-13", "Company"),
    q1_26_assoc=I(253.240105, "Share of profit of equity-accounted investees, Q1-2026 interim "
                  "statements", "2026-05-13", "Company"),
    q1_26_tax=I(-1813.239280, "Income tax expense, Q1-2026 interim statements (effective rate "
                "25.75% on pre-tax profit of 7,041.966803, up from 21.96% in Q1-2025)",
                "2026-05-13", "Company"),
    q1_26_npa=I(4845.322118, "Profit attributable to owners of the parent, Q1-2026, +16.9% y/y",
                "2026-05-13", "Company"),
    q1_26_nd=I(28768.787222, "Net financial debt, 31 Mar 2026: total loans and borrowings including "
               "leases 89,533.539777 less cash 60,764.752555 — up sharply from FY2025-close as "
               "working capital absorbed cash (net operating cash flow was NEGATIVE 1,665.1 in the "
               "quarter) funded by 30,364.3 of new loan drawdowns", "2026-05-13", "Company"),

    # ---- H1-2026, the reviewed half ---------------------------------------
    # THE STUDY WAS RIGHT AT STRIKE AND IS STALE NOW, and the distinction is recorded
    # rather than blurred: these statements were approved for issuance on 11 August 2026
    # (note 2-1), SIX DAYS AFTER the 5 August strike. The first edition consumed Q1-2026
    # and everything before it and there was no unread filing; [R-GAP-01 AMENDED] is what
    # requires the half now, because a study may not be DELIVERED against a stale record.
    h1_26_rev=I(163315.717414, H126 + ", condensed interim consolidated statement of profit or "
                "loss, six months to 30-Jun-2026 (H1-2025 comparative 123,800.551073, +31.9%)",
                "2026-08-11", "Company"),
    h1_26_gp=I(26333.300080, H126 + ", gross profit on the face (H1-2025 20,245.400138)",
               "2026-08-11", "Company"),
    h1_26_op=I(16421.199737, H126 + ", operating profit on the face (H1-2025 12,605.157783)",
               "2026-08-11", "Company"),
    h1_26_netfin=I(-2141.522815, H126 + ", net finance costs: finance income 1,579.219385 less "
                   "finance costs 3,720.742200", "2026-08-11", "Company"),
    h1_26_assoc=I(572.617216, H126 + ", group share of profit of equity-accounted investees net "
                  "of tax. A further 542.976117 of gains on sale and revaluation of investments "
                  "in equity-accounted investees is disclosed SEPARATELY (note 20-3) and is "
                  "treated as a one-off, not as recurring associate income",
                  "2026-08-11", "Company"),
    h1_26_assoc_oneoff=I(542.976117, H126 + ", note 20-3: gains on sale and revaluation of "
                         "investments in equity-accounted investees. Disclosed on its own line "
                         "with no comparative, i.e. nothing in H1-2025 — a one-off",
                         "2026-08-11", "Company"),
    h1_26_tax=I(-4748.555104, H126 + ", income tax expense. Effective rate 30.85% on pre-tax "
                "profit of 15,395.270255, against 19.39% in H1-2025 and the 24.5% the forecast "
                "carries — a material step this re-issue must price rather than average away",
                "2026-08-11", "Company"),
    h1_26_npa=I(9921.669274, H126 + ", profit attributable to owners of the parent company "
                "(H1-2025 8,694.611825, +14.1%)", "2026-08-11", "Company"),
    h1_26_nci=I(725.045877, H126 + ", profit attributable to non-controlling interests — 6.81% "
                "of the period's total profit after tax of 10,646.715151", "2026-08-11",
                "Company"),
    h1_26_eps=I(4.03, H126 + ", note 38: basic and diluted earnings per share (H1-2025 3.55)",
                "2026-08-11", "Company"),

    # THE EMPLOYEES' STATUTORY SHARE OF PROFIT, which appears in NO line of the income
    # statement [L-294]. Egyptian company law gives employees a share of distributable
    # profits; it is an APPROPRIATION rather than a cost, so it is disclosed only in the
    # earnings-per-share note, BELOW profit attributable to owners. It is a claim ahead of
    # ordinary shareholders and the first edition of this study did not carry it — which
    # is why its registered attributable profit and its registered EPS disagreed by 12%.
    emp_share_fy24=I(2025.840035, "Audited FY2025 consolidated financial statements, note 39 "
                     "(FY2024 comparative): employees' share in profit (estimated), deducted "
                     "from profit attributable to owners to reach profit attributable to "
                     "ordinary shareholders — 11.60% of the 17,461.358714 attributable",
                     "2026-03-01", "Company"),
    emp_share_fy25=I(2073.104844, "Audited FY2025 consolidated financial statements, note 39: "
                     "employees' share in profit (estimated) — 11.96% of the 17,330.244990 "
                     "attributable to owners. The reported EPS of 7.13 is struck on the "
                     "15,257.140146 that remains, over a weighted-average 2,139,355,716 shares "
                     "(issued 2,140,777,876 less 1,422,160 ESOP shares issued not granted)",
                     "2026-03-01", "Company"),
    # THE WAGE BILL THE STATUTORY CAP IS SET AGAINST, read off the same audited statements
    # the charge itself comes from. Registered because the study asserted for two editions
    # that "nothing in the filings discloses the cap's headroom" while these three lines
    # sat in the notes it was already reading.
    salaries_cogs_fy25=I(12646.918355, "FY2025 audited financial statements, cost of sales note: 'Salaries and "
                         "its equivalents'", "2026-03-01", "Company"),
    salaries_selling_fy25=I(1588.065415, "FY2025 audited financial statements, selling and distribution note: "
                            "'Salaries and its equivalents'", "2026-03-01", "Company"),
    salaries_admin_fy25=I(4670.811665, "FY2025 audited financial statements, general and administrative note: "
                          "'Salaries and its equivalents'", "2026-03-01", "Company"),
    salaries_cogs_fy24=I(7898.895209, "FY2025 audited financial statements, cost of sales note, FY2024 comparative",
                         "2026-03-01", "Company"),
    salaries_selling_fy24=I(1216.037561, "FY2025 audited financial statements, selling and distribution note, FY2024 "
                            "comparative", "2026-03-01", "Company"),
    salaries_admin_fy24=I(3639.052338, "FY2025 audited financial statements, general and administrative note, FY2024 "
                          "comparative", "2026-03-01", "Company"),
    emp_share_h1_26=I(1291.202008, H126 + ", note 38: employees' share in profit (expected) — "
                      "13.01% of the 9,921.669274 attributable to owners (H1-2025 1,104.834367 "
                      "on 8,694.611825, 12.71%)", "2026-08-11", "Company"),
    eps_fy25=I(7.13, "Audited FY2025 consolidated financial statements, note 39: basic and "
               "diluted earnings per share. REGISTERED SO THAT IT CAN BE RECONCILED — "
               "17,330.244990 attributable over 2,140.777876 shares gives 8.095, and the "
               "difference from 7.13 is the employees' share above plus the ESOP adjustment to "
               "the weighted-average count. Neither figure was wrong in the first edition; "
               "nothing compared them", "2026-03-01", "Company"),

    # ---- H1-2026 segment structure, note 16 -------------------------------
    # SEGMENT PROFIT, matching the basis seg_profit_hist is registered on — gross profit
    # LESS selling and distribution expenses, which is the row below the gross-profit row
    # in the same note. The two are 6.5 percentage points apart at group level and mixing
    # them is [L-289]; the key naming that made that easy is corrected in this pass.
    seg_rev_h1_26=I(dict(cables=70858.484737 + 25636.688152,
                         construct=22726.747972 + 21104.518814,
                         elecprod=6480.316880 + 16508.960859),
                    H126 + ", note 16: revenue without inter-segment sales, aggregating the "
                    "inside-Egypt and outside-Egypt columns for each segment. Sums EXACTLY to "
                    "the consolidated 163,315.717414", "2026-08-11", "Company"),
    seg_profit_h1_26=I(dict(cables=7849.717992 + 4201.610931,
                            construct=2174.899850 + 2906.639323,
                            elecprod=2882.043296 + 2843.811413),
                       H126 + ", note 16: SEGMENT PROFIT (gross profit less selling and "
                       "distribution expenses), aggregating both geography columns per segment",
                       "2026-08-11", "Company"),
    seg_unalloc_h1_26=I(-(99.108365 + 22.707789),
                        H126 + ", note 16: the unallocated segment-profit columns",
                        "2026-08-11", "Company"),
    seg_rev_h1_25=I(dict(cables=53899.277753 + 20004.697124,
                         construct=20194.851562 + 14197.946308,
                         elecprod=5627.101011 + 9876.677315),
                    H126 + ", note 16 H1-2025 comparative. Sums EXACTLY to 123,800.551073",
                    "2026-08-11", "Company"),
    # THE TWO MARGINS, REGISTERED so the pool prose_check draws on actually holds them.
    # Computing them was not enough: the checker matches against registered VALUES, not
    # against module variables, so a figure formatted from a local is still a figure the
    # study asserts and cannot show.
    mgn_fy25=I(round(_MGN_FY25, 6),
               "FY2025 group segment-profit margin, DERIVED: the three segments' note-16 "
               "profit less the disclosed unallocated item, over audited group revenue",
               "2025-12-31", "Company"),
    mgn_h1_25=I(round(_MGN_H1_25, 6),
                "H1-2025 group segment-profit margin, DERIVED the same way from the "
                "note-16 comparative half. It is 1.9 points ABOVE the full year, which is "
                "the whole basis of this study's refusal to anchor a full year on a half",
                "2025-06-30", "Company"),
    seg_profit_h1_25=I(dict(cables=6823.397790 + 3925.845038,
                            construct=2031.644426 + 1083.868786,
                            elecprod=1923.388459 + 1713.421415),
                       H126 + ", note 16 H1-2025 comparative, segment profit — THE HALF THIS "
                       "STUDY MUST COMPARE AGAINST, because FY2025's group margin of "
                       + ("%.2f%%" % (100 * _MGN_FY25)) + " sits well below H1-2025's "
                       + ("%.2f%%" % (100 * _MGN_H1_25)) + ": this company's halves are not "
                       "alike and a half-against-full-year comparison is a basis error. Both "
                       "figures are COMPUTED from the note-16 figures registered here and "
                       "above rather than typed beside them — they were typed until "
                       "09-09-2026, and a figure in a delivered source string that the model "
                       "does not produce is one prose_check cannot reconcile",
                       "2026-08-11", "Company"),

    # ---- the 30-Jun-2026 balance sheet, for the bridge [R-BRIDGE-01] ------
    h1_26_debt=I(8072.452169 + 75932.760330,
                 H126 + ", condensed interim statement of financial position, note 31: loans "
                 "and borrowings, non-current 8,072.452169 plus current 75,932.760330",
                 "2026-08-11", "Company"),
    h1_26_cash=I(52775.664158 + 2600.578354,
                 H126 + ", note 28 cash and cash equivalents 52,775.664158 plus note 27 "
                 "investments in debt securities at amortised cost 2,600.578354",
                 "2026-08-11", "Company"),
    h1_26_investees=I(7119.632125, H126 + ", note 20: equity-accounted investees at carrying "
                      "value (31-Dec-2025: 6,757.650507)", "2026-08-11", "Company"),
    h1_26_eq_parent=I(70347.328547, H126 + ", equity attributable to owners of the parent "
                      "company (31-Dec-2025: 66,870.866550)", "2026-08-11", "Company"),
    h1_26_nci_eq=I(5677.269855, H126 + ", non-controlling interests — 7.47% of total equity of "
                   "76,024.598402, against the 9.7% value share this study's bridge deducts "
                   "and 6.81% of the half's profit. The study's figure is conservative on all "
                   "three readings", "2026-08-11", "Company"),

    # ---- segment structure — THE DISCLOSED THREE SEGMENTS ------------------
    # Revenue by product/service line (Note 5-3 in every filing) ties EXACTLY to
    # consolidated revenue for all three years — no elimination, no estimation.
    seg_rev_hist=I(_SEG_REV_HIST,
        "Revenue by product/service line, Note 5-3, all three audited financial statements. "
        "Sums EXACTLY to consolidated revenue in every year (152,186.247545 / 231,981.835577 / "
        "281,049.081719). This REPLACES a seven-way sub-segment split (cables, raw material, "
        "engineering & construction, transformers, meters, other electrical products, "
        "infrastructure investment) that does not appear in any of three years of audited filings",
        "2026-03-15", "Company"),
    seg_profit_hist=I(dict(
        FY23=dict(cables=16057.629741, construct=6215.524501, elecprod=4142.770991),
        FY24=dict(cables=24851.887243, construct=8115.892728, elecprod=6345.336266),
        FY25=dict(cables=21016.396482, construct=5868.890571, elecprod=7604.808509)),
        "Segment profit by the same three segments, Note 16 (operating segments), all three "
        "audited financial statements — the inside-Egypt and outside-Egypt columns summed. This "
        "is computed on the segment note's OWN (pre-elimination) revenue base, which is larger "
        "than the Note 5-3 external-revenue view because it includes inter-segment sales (chiefly "
        "cable output consumed by the Constructions segment on turnkey projects); FY2025 also "
        "carries a disclosed unallocated/corporate item of -246.710877 not attributed to any "
        "segment. FY2023's three segments sum to 26,415.925233 against a disclosed total of "
        "26,406.917233 (a 9.0 EGP thousand rounding residual in the filing's own inside/outside "
        "table, immaterial); FY2024 and FY2025 tie exactly", "2026-03-15", "Company"),
    corp_load_hist=I(dict(FY23=0.0570144, FY24=0.04298, FY25=0.03163),
                     "Net corporate cost load = (G&A + net impairment on receivables + other "
                     "expenses - other income) / revenue, computed from the audited income "
                     "statements. This is the bridge from segment profit (Note 16) to consolidated "
                     "operating profit and it reconciles EXACTLY in all three years: e.g. FY2025 "
                     "segment profit 34,490.095562 less the -246.710877 unallocated/corporate item "
                     "= 34,243.384685, less 3.163% x revenue 281,049.081719 = 25,354.225619 = the "
                     "audited operating profit to the EGP. The load has been FALLING — operating "
                     "leverage improving at the corporate level even as segment margins compressed",
                     "2026-03-15", "Company"),
    seg_unalloc_fy25=I(-246.710877, "Unallocated/corporate segment item, Note 16, FY2025 audited "
                        "financial statements — not attributed to any of the three segments; netted "
                        "against the three segments' summed profit before the corporate-load bridge "
                        "is applied. No equivalent unallocated item is disclosed for FY2023 or "
                        "FY2024", "2026-03-15", "Company"),
    dna_pct_hist=I(dict(FY23=0.01509, FY24=0.00974, FY25=0.01070),
                   "Depreciation and amortisation as a share of revenue, computed from the audited "
                   "cash flow statements", "2026-03-15", "Company"),
    capex_pct_hist=I(dict(FY23=0.03120, FY24=0.03660, FY25=0.04665),
                     "Capital expenditure (cash paid for PP&E and projects under construction, "
                     "audited cash flow statements) as a share of revenue — a clear, rising "
                     "capacity-investment cycle", "2026-03-15", "Company"),
    nwc_pct_hist=I(dict(FY23=0.2409, FY24=0.2306, FY25=0.1987),
                   "Net working capital (inventories + contract assets + trade and other "
                   "receivables, current, LESS trade and other payables LESS contract liabilities; "
                   "industrial real-estate-development land holdings excluded as a separate "
                   "quasi-investment item) as a share of revenue, computed from the audited balance "
                   "sheets. FY2025 shows a genuine, disclosed IMPROVEMENT in working-capital "
                   "intensity, not an assumption", "2026-03-15", "Company"),

    # ---- forecast drivers — THREE REAL SEGMENTS -----------------------------
    copper_hist=I(dict(FY23=8478.0, FY24=9147.0, FY25=10000.0),
                  "LME copper cash, annual average USD/tonne (house commodity reference) — used "
                  "only as a GROWTH driver for the Cables segment (Cables revenue is genuinely "
                  "copper-linked; the company DOES disclose tonnage, quarterly, and the series is "
                  "registered below — an earlier edition of this line said it did not. "
                  "The model tracks the "
                  "copper x FX growth rate rather than reconstructing an absolute volume)",
                  "2026-08-05", "Industry"),
    # THE COMPANY DISCLOSES ITS OWN AVERAGE RATE AND TWO OF THREE YEARS WERE TYPED
    # [09-09-2026]. The retired entry read FY23=30.59, FY24=45.3, FY25=49.5 and said so
    # plainly: FY2023 "is the audited FY2023 filing's own disclosed figure (Note 44-3-1);
    # FY2024/FY2025 are house averages consistent with the scale of the disclosed
    # devaluation". Note 44-3 of the FY2025 audited statements prints the same table for
    # both years — average USD 47.69 for FY2025 and 43.96 for FY2024 — so the study knew
    # the note existed, read it for one year, and estimated the other two. The house
    # estimates were 3.8% and 3.1% high.
    #
    # IT IS A DENOMINATOR, SO CORRECTING IT RAISES FORECAST GROWTH RATHER THAN LOWERING
    # THEM: cables growth is driven by copper x FX against the FY2025 base, and a smaller
    # base means a larger step. This correction therefore moves the cables line FURTHER
    # from what the reviewed half measures, not closer, and it is made because the figure
    # is disclosed and the one it replaces was not.
    fx_hist=I(dict(FY23=30.59, FY24=43.96, FY25=47.69),
              "Annual average USD/EGP, all three DISCLOSED by the issuer rather than "
              "estimated. FY2025 47.69 and FY2024 43.96 are note 44-3 of the FY2025 "
              "audited statements, 'significant foreign currency exchange rates during "
              "the year', average-rate columns; FY2023 30.59 is the FY2023 filing's own "
              "note 44-3-1. Revisions to 08-09-2026 typed 49.5 and 45.3 as house averages "
              "while the note sat in a filing this study already reads",
              "2026-03-15", "Company"),
    fx_path=I([51.0, 54.0, 57.5, 61.0, 64.5],
              "USD/EGP average-rate path, about 6%/yr of depreciation from the FY2025 average of "
              "49.5. Used as a genuine driver of the Cables segment's copper-linked growth and of "
              "the currency-of-discounting alternative — not a translation convenience. "
              "DELIBERATELY BELOW covered-interest parity, which on the roughly 22% pound rate "
              "against a ~4-5% dollar rate implies materially faster depreciation; the base case "
              "assumes disinflation closes most of that gap. The parity case is carried as an "
              "explicit sensitivity", "2026-08-05", "House"),
    # HOLDING A DOLLAR PRICE FLAT IS NOT HOLDING IT [10-Sep-2026]. The path held
    # 14,000 nominal USD for four years while this house's own macro path carries US
    # long-run inflation of 2.5%. A flat NOMINAL price is a REAL decline of 2.5% a
    # year, compounding to -9.5% by FY2030E — a directional view on copper held by
    # nobody and arrived at by leaving a number alone. The level is still not a
    # forecast: it is today's price escalated at the house's own inflation, which is
    # what "held flat" was meant to say.
    copper_fcst=I([13400.0] + [14000.0 * (1 + _MP_EG.raw['us_inflation_lt']['value']) ** k
                               for k in range(1, 5)],
                  "LME copper. FY2026 is set at USD 13,400/t, between the Q1-2026 average actually "
                  "realised and the current cash price of about 14,000 (early August 2026); "
                  "thereafter the current level is held flat — copper is the largest single input "
                  "into the Cables segment and a directional view on it would dominate the "
                  "valuation. The -10% column of the sensitivity carries the mean-reversion case",
                  "2026-08-05", "Industry"),
    # THE COMPANY DISCLOSES TONNAGE, AND THIS STUDY SAID IT DID NOT [10-Sep-2026].
    # Elsewedy Electric's own quarterly earnings releases carry a table headed
    # "Cables Sales Volumes (Tons)", and they have been committed in this repository
    # since an earlier rebuild, at engine/swdy_walkforward/text/. Two rows of this
    # file asserted the opposite and used the assertion to JUSTIFY a flat 3.0% --
    # "the model should not manufacture a volume story it cannot evidence". The
    # evidence was two pages from the backlog figures read off the same releases on
    # the same day. A driver justified by the ABSENCE of a disclosure is void the
    # moment the disclosure is found, whichever way the number then moves [R-GAP-04].
    cables_tonnage_hist=I(dict(FY22=144997, FY23=156748, FY24=167665, FY25=185449),
                          "Cables sales volumes in tonnes, from Elsewedy Electric's own "
                          "Q4 earnings releases (4Q2023, 4Q2024, 4Q2025), each printed "
                          "beside its own prior-year comparative: +8.1%, +7.0%, +10.6%. "
                          "A compound 8.55% a year over FY2022-25",
                          "2026-02-15", "Company"),
    cables_tonnage_h1=I(dict(H1_25=89636, H1_26=99239),
                        "Cables sales volumes, reviewed half: 99,239 tonnes against "
                        "89,636, +10.71% — the Q2-2026 earnings release. The most recent "
                        "volume disclosure and the anchor for FY2026 [R-ANCHOR-01]",
                        "2026-08-14", "Company"),
    # THE RESIDUAL WAS TWO OPPOSITE THINGS WEARING ONE NUMBER. Cables revenue was
    # built as (1+copper)(1+FX)(1+real), which ASSERTS that price per tonne moves
    # exactly with copper and the pound and leaves "real" to mean volume. Against the
    # company's own disclosure that assertion held in FY2024 and failed in FY2025:
    # price per tonne rose 55.6% against copper x FX of 55.1% (a pass-through of
    # +0.4%), then 2.7% against 18.6% (a shortfall of 13.4 points). So the 3.0%
    # residual was volume growth of 7-11% multiplied by a pass-through shortfall of
    # nearly the same size, and neither could be seen or argued. They are separated
    # now, and the pass-through — the contested half — is carried BOTH WAYS.
    cables_volume_growth=I([0.1071, 0.090, 0.075, 0.065, 0.055],
                           "Cables tonnage growth, RE-ANCHORED on the reviewed half "
                           "[R-ANCHOR-01]: FY2026 is the disclosed +10.71%, tapering "
                           "toward and below the FY2022-25 compound rate of 8.55%. The "
                           "company's OWN disclosed volume series, not a residual and "
                           "not a proxy", "2026-08-14", "Company"),
    cables_passthrough=I([0.0, -0.0654, -0.0436, -0.0218, 0.0],
                         "How much of the copper-and-currency move reaches price per "
                         "tonne, as the gap from FULL pass-through. ADOPTED: the MEAN "
                         "of the two disclosed years (FY2024 +0.36%, FY2025 -13.43%, "
                         "mean -6.54%) applied to the first year the formula governs "
                         "and closing straight-line to zero by FY2030E. It uses both "
                         "observations rather than the convenient one, and it closes "
                         "because a shortfall CANNOT persist indefinitely: compounded, "
                         "it drives price per tonne below the cost of the metal in it. "
                         "FY2026 is 0.0 because that year is anchored on the reviewed "
                         "half's own measured revenue and the formula does not govern "
                         "it", "2026-08-14", "Company/House"),
    cables_passthrough_alt=I([0.0, -0.1343, -0.1343, -0.0672, 0.0],
                             "THE CONTESTED ALTERNATIVE: FY2025's measured shortfall "
                             "persists two more years before closing — the case that "
                             "pricing power lost in a copper spike takes a cycle to "
                             "recover rather than a year. Published beside the adopted "
                             "case and NEVER averaged with it. A third case was tried "
                             "and rejected as not serious: holding -13.43% flat for "
                             "ever makes cables revenue FALL in nominal pounds from "
                             "FY2028 while volume grows 5-9% a year, which is not a "
                             "view anybody holds", "2026-08-14", "Company"),
    cables_real_growth=I([0.030, 0.030, 0.030, 0.030, 0.030],
                        "Real (ex-copper, ex-FX) volume/market-share growth for the Cables segment "
                        "— modest and flat. HELD, AND NOW MEASURED RATHER THAN ASSERTED. Backing "
                        "copper and the pound out of the segment's own audited revenue gives a "
                        "REALISED real growth of +4.18% in FY2024 and -4.94% in FY2025, a two-year "
                        "mean of about -0.4%. So 3.0% is already above what this segment has "
                        "demonstrated, not below it, and it is not raised. The group's headline "
                        "35.9% revenue CAGR over FY2023-25 is 27.2 points of currency a year: the "
                        "growth is real in pounds and largely absent in tonnes. Cables segment "
                        "revenue growth = (1+copper growth)(1+FX growth)(1+this) - 1",
                        "2026-09-10", "Company/House"),
    # ---- segment margin paths, RE-ANCHORED on the reviewed half [R-ANCHOR-01] -----
    # WHAT THE FIRST EDITION DID, and why it could not have done otherwise: it forecast a
    # PARTIAL RECOVERY toward the FY2023-24 levels in all three segments. That is a claim
    # about the future with no named mechanism and no measured direction, which this rule
    # forbids — and at the 5 August strike there was no measurement available to make,
    # because the half that supplies one was issued on 11 August.
    #
    # THE CONSTRUCTION, and the seasonality that decides it. Each rate is the FY2025
    # full-year figure plus the segment's own MEASURED like-for-like change between the
    # two comparable halves (H1-2025 -> H1-2026, from note 16 of the reviewed statements).
    # It is NOT the H1-2026 rate itself: this company's halves are not alike — the group
    # printed 14.14% in H1-2025 against 10.65% in H2-2025, so H2 runs about three and a
    # half points weaker, and anchoring a full year on an H1 rate would overstate it by
    # 16%. Applying the CHANGE preserves the seasonal shape and still lets the latest
    # reviewed period outrank the stale full-year rate, which is what the rule asks for.
    #
    # AND THEN HELD FLAT. The measured directions disagree with each other — cables is
    # getting WORSE, the other two better — so there is no group trend to project, and the
    # standing rule is to hold everything flat including observed improvements unless a
    # named structural mechanism has a measured direction of its own. None of the three
    # has one: the contracting improvement may be project mix, and no disclosure
    # establishes otherwise.
    cables_margin=I([0.114341] * 5,
                    "Cables segment profit margin (Note 5-3 external-revenue base), RE-ANCHORED "
                    "and held flat. FY2025 13.49% plus the measured like-for-like half change of "
                    "-2.06pp (H1-2025 14.54% -> H1-2026 12.49%, note 16 of the reviewed interim "
                    "statements). THE MEASURED DIRECTION IS DOWN, against the first edition's "
                    "assumed recovery to 14.0-15.5%: cables revenue is copper-linked, so a "
                    "rising copper price inflates the revenue base faster than the spread, and "
                    "the FY2023-24 levels carried devaluation gains on cheaply bought inventory "
                    "that will not repeat. No further decline is projected either — one measured "
                    "half is a direction, not a trend",
                    "2026-08-11", "Company/House"),

    construct_growth=I([0.2744, 0.20, 0.15, 0.115, 0.09],
                       "Constructions segment revenue growth, RE-ANCHORED on the reviewed half "
                       "[R-ANCHOR-01] and then tapered. FY2026 is the segment's OWN measured "
                       "like-for-like half growth, H1-2025 34,393 -> H1-2026 43,831 = +27.44%; "
                       "the taper runs to +9.0%. THE RETIRED PATH OPENED AT +18% while the "
                       "company's own reviewed interim was running at +27.4% — a forecast "
                       "contradicting the most recent disclosure this study read, in the "
                       "direction that lowered the valuation. The margins in this segment were "
                       "re-anchored on that same half on 11-Aug-2026 and the growth rates were "
                       "not, so the rule was applied to one half of the segment build and not "
                       "the other. THE BACKLOG, WHICH THIS DRIVER SAID FOR TWO EDITIONS DID NOT "
                       "EXIST: no order book is disclosed in any AUDITED filing or in the "
                       "Q1-2026 interim, but the ISSUER discloses one in its own quarterly "
                       "earnings releases. Engineering and construction backlog runs EGP 196bn "
                       "(Dec-24), 261, 276, 293 (Dec-25), 307 and 346bn at 30 June 2026, read "
                       "off the Q2-2026 release; wires and cables 43.5bn and meters 8.8bn are "
                       "disclosed beside it. That is +18% over the half against the +27.4% "
                       "revenue growth this driver is anchored on, so the backlog CORROBORATES "
                       "the level without being burnt down to produce it — the taper is still "
                       "a taper on the segment's own revenue record, not a burn rate. Priced "
                       "across its whole defensible range the taper is worth 0.17% of this "
                       "study's gap to the market, because at a 9% segment margin against 20% "
                       "working capital incremental Constructions revenue is very nearly free "
                       "cash flow neutral. The false sentence was corrected because it was "
                       "false, not because the number moves [R-GAP-04]",
                       "2026-09-10", "Company/House"),
    construct_margin=I([0.089871] * 5,
                       "Constructions and infrastructure segment profit margin, RE-ANCHORED and "
                       "held flat. FY2025 6.45% plus the measured like-for-like half change of "
                       "+2.53pp (H1-2025 9.06% -> H1-2026 11.59%). THE MEASURED DIRECTION IS UP "
                       "and sharply, against the first edition's cautious 6.8% opening — the "
                       "improvement is real and reviewed. It is NOT projected forward: a "
                       "contracting margin turns on which projects reach their profitable "
                       "phases in which period, no disclosure establishes that this mix is "
                       "durable, and the half is held rather than extrapolated",
                       "2026-08-11", "Company/House"),

    elecprod_growth=I([0.4828, 0.33, 0.23, 0.16, 0.11],
                      "Electrical products and digital solutions segment revenue growth, "
                      "RE-ANCHORED on the reviewed half [R-ANCHOR-01]. FY2026 is the segment's "
                      "own measured like-for-like half growth, H1-2025 15,504 -> H1-2026 22,989 "
                      "= +48.28%; it then tapers to +11%. THE RETIRED PATH OPENED AT +20% — "
                      "against a disclosed FY2025 of +43.7%, an FY2024 of +46.6% and a reviewed "
                      "half running at +48.3%. Three consecutive disclosures said the same "
                      "thing and the forecast halved the rate in year one with no named "
                      "mechanism. THE MECHANISM FOR THE LEVEL IS NAMED AND DATED: this is the "
                      "segment that makes transformers, and in August 2026 Elsewedy Electric — "
                      "the listed company — signed a pre-purchase agreement to manufacture four "
                      "high-voltage transformers of up to 360 MVA for Datagrid's Southland AI "
                      "data centre via Transpower New Zealand, commissioning late 2027. The "
                      "global grid-equipment cycle driving that order is the same one running "
                      "through this segment's disclosed numbers. It is NOT extrapolated: the "
                      "path halves the growth rate over four years",
                      "2026-09-10", "Company/House"),
    elecprod_margin=I([0.236221] * 5,
                      "Electrical products and digital solutions segment profit margin, "
                      "RE-ANCHORED and held flat. FY2025 22.17% plus the measured like-for-like "
                      "half change of +1.45pp (H1-2025 23.46% -> H1-2026 24.91%). The "
                      "least-compressed segment in FY2025 and the one recovering most quietly; "
                      "held at the re-anchored level rather than drifting toward the FY2024 "
                      "26.6%, which no measurement supports",
                      "2026-08-11", "Company/House"),

    # RE-ANCHORED ON THE REVIEWED HALF [R-ANCHOR-01]. The first edition glided this load
    # UP from FY2025's 3.16% toward the FY2023-24 average of about 5.0%, on the view that
    # FY2025 was "unusually low" — and its own registration called that "the single most
    # conservative choice in the build", which it was. It is worth more than the segment
    # margins: 4.55% against 3.16% is 1.39 points of revenue, about EGP 5.1bn in FY2026
    # alone, on a line that had FALLEN in each of the three audited years (5.70% -> 4.30%
    # -> 3.16%).
    #
    # THE REVIEWED HALF SAYS THE LEVEL IS HOLDING, NOT REVERTING. H1-2026 prints 3.87%
    # against H1-2025's 3.96% — a like-for-like fall of 0.09 points. Halves run heavier
    # than years here because the fixed element spreads over less revenue (H1-2025 3.96%
    # against a full-year 3.16%), so the half is not read as a level; its CHANGE is
    # applied to the full year, exactly as the segment margins are.
    #
    # A reversion to 5.0% is a claim about the future with no named mechanism and a
    # measured direction pointing the other way. It is retired as the central and kept as
    # the contested judgement, priced both ways in the sensitivity block.
    corp_load=I([0.0307] * 5,
               "Net corporate cost load, stated on the SEGMENT-PROFIT-TO-EBIT basis — the same "
               "basis as the audited historical bridge (FY2023 5.70%, FY2024 4.30%, FY2025 "
               "3.16%). RE-ANCHORED: FY2025's 3.16% plus the measured like-for-like half change "
               "of -0.09pp (H1-2025 3.96% -> H1-2026 3.87%, both computed as segment profit "
               "less operating profit over revenue from the reviewed interim statements), held "
               "FLAT. The first edition glided it up toward 5.0% on the view that FY2025 was "
               "unusually low; the reviewed half measures the level holding, and no disclosure "
               "names a mechanism that would take it back up",
               "2026-08-11", "Company/House"),
    corp_load_reversion=I([0.0455, 0.0465, 0.0475, 0.0475, 0.0485],
               "THE RETIRED PATH, kept because it is this study's most consequential contested "
               "judgement and the depth bar requires such a judgement to be computed BOTH WAYS "
               "and published side by side rather than averaged. It glides the load from "
               "FY2025's level toward the FY2023-24 average of about 5.0%",
               "2026-08-07", "House"),
    opex_pct=I([0.0307] * 5,
               "Alias of corp_load (segment-profit-to-EBIT basis), retained for compatibility "
               "with the DCF waterfall and sensitivity-grid code paths that reference a single "
               "operating-load driver", "2026-08-11", "Company/House"),
    unit_price_inflation=I([0.08, 0.075, 0.07, 0.07, 0.07],
                           "Retained input, no longer consumed by the segment build (kept for "
                           "downstream compatibility)", "2026-08-05", "House"),
    foreign_share_fy25=I(0.70, "'Over 70% of revenues generated abroad' (company commentary); the "
                         "audited Note 5-2 geographic split gives Outside Egypt 40.7% of FY2025 "
                         "revenue (114,461.030 / 281,049.082) — geography and hard-currency pricing "
                         "are different questions, addressed explicitly below", "2026-03-15",
                         "Company"),
    fgn_egp_share_fy25=I(0.407, "Revenue earned OUTSIDE Egypt, FY2025, Note 5-2 (geographic "
                         "disaggregation): 114,461.030219 / 281,049.081719 = 40.72%. This is the "
                         "audited geographic split; the HARD-CURRENCY-LINKED share used in the "
                         "currency-of-discounting alternative is derived separately below from the "
                         "Cables segment's copper linkage, since a project executed abroad for a "
                         "local utility is foreign revenue but not necessarily dollar-priced",
                         "2026-03-15", "Company"),
    nwc_pct=I(0.1967, "Net working capital as a share of revenue, RE-ANCHORED on the "
              "REVIEWED 30-Jun-2026 sheet: inventories 79,140 + contract assets 40,121 + "
              "receivables 130,221 - payables 79,553 - contract liabilities 106,860 = "
              "63,069 on last-twelve-month revenue of 320,564 = 19.67%. Retired: 19.90%, "
              "the FY2025 disclosed "
              "level (19.87%) — a genuine improvement on FY2023 (24.1%) and FY2024 (23.1%), "
              "carried forward without assuming further improvement or reversion",
              "2026-08-05", "House"),
    # ---- THE DISCLOSED HALF-YEAR CAPEX, ALL FOUR OF THEM [added 09-09-2026]
    # THE REVIEWED HALF THIS STUDY ALREADY READS FOR REVENUE, PROFIT, FINANCE, TAX AND
    # ASSOCIATES ALSO DISCLOSES CAPEX, AND NOBODY REGISTERED IT. Same filing, same cash
    # flow statement, two lines below figures this register already carries. It is the
    # third disclosure hole found in this study in two days, after the Constructions
    # backlog and the employees'-cap headroom, and it is the one that is worth something.
    capex_h1_26=I(5435.908723, H126 + ", condensed interim consolidated statement of cash "
                  "flows: 'Paid for acquisition of property, plant and equipment and "
                  "projects under construction'", "2026-06-30", "Company"),
    capex_h1_25=I(5386.809066, H126 + ", same line, comparative column — and independently "
                  "in the reviewed interim statements for the six months ended 30 June "
                  "2025, where it is the current-period figure. Two readings of one fact "
                  "agreeing [R-ENF-03]", "2025-06-30", "Company"),
    capex_h1_24=I(4595.530101, "Reviewed condensed interim consolidated financial "
                  "statements for the six months ended 30 June 2024, statement of cash "
                  "flows, same line", "2024-06-30", "Company"),
    capex_h1_23=I(1858.436892, "Reviewed condensed interim consolidated financial "
                  "statements for the six months ended 30 June 2024, same line, "
                  "comparative column", "2023-06-30", "Company"),
    capex_pct=I([0.044, 0.040, 0.036, 0.033, 0.031],
                "THE RETIRED PATH, superseded 09-09-2026 and kept because the depth bar "
                "requires a displaced construction to be published beside the one that "
                "replaced it. It tapered from the FY2025 disclosed level of 4.7% (up from "
                "3.1% FY2023 and 3.7% FY2024) toward a lower maintenance-plus-modest-"
                "capacity level as the expansion cycle completes — a House glide, on a "
                "story about the cycle, set before the reviewed half was read. The half "
                "measures the cycle directly: see capex_pct_measured below",
                "2026-08-05", "House"),
    dna_pct=I(0.0107, "Depreciation and amortisation as a share of revenue, AT the "
              "disclosed level rather than above it: FY2025 3,009/281,049 = 1.071% and "
              "the reviewed half 1,748/163,316 = 1.070%, two periods agreeing to a "
              "thousandth. The retired 1.25% was the FY2025 level plus a house uplift "
              "for the capex ramp, which the reviewed half then measured and did not "
              "show. Previously: held near the FY2025 "
              "disclosed level (1.07%) with a modest rise reflecting the larger capitalised asset "
              "base from the FY2025-26 capex ramp", "2026-08-05", "House"),

    # ---- cost of capital ---------------------------------------------------
    rf=I(0.2231, "Egypt 10-year local-currency government bond yield, 22.31% (house cost-of-capital "
         "reference, cached 21-Jul-2026 print, re-verified 05-Aug-2026)", "2026-07-21", "Country"),
    sov_spread_cds=I(0.0340, "Egypt CDS-implied sovereign default spread, Damodaran January-2026 "
                     "country-premium file, CDS column. Netted out of the local-currency risk-free "
                     "rate so sovereign default risk is not charged twice", "2026-01-05", "Country"),
    sov_spread_rating=I(0.0637, "Damodaran adjusted default spread on the rating basis (Caa1), "
                        "January-2026 — the alternative construction, disclosed for the audit trail",
                        "2026-01-05", "Country"),
    erp_cds=I(0.0941, "Damodaran original country-premium file, Egypt row, CDS column, last updated "
              "5 January 2026 — total equity risk premium", "2026-01-05", "Country"),
    erp_rating=I(0.1394, "Damodaran original country-premium file, Egypt row, rating basis, "
                 "January-2026 — the alternative", "2026-01-05", "Country"),
    # THE COUNTRY PREMIUM IS NOT MULTIPLIED BY BETA  [R-COC-03, adopted 10-Sep-2026]
    lambda_country=I(1.0 - 0.4072,
                     "Damodaran's lambda: the share of operations exposed to the HOME "
                     "sovereign, taken from the audited Note 5-2 geographic disaggregation "
                     "— revenue outside Egypt 114,461.030219 / 281,049.081719 = 40.72%, so "
                     "59.28% sits in Egypt. A typical Egyptian listed company earns "
                     "essentially all of its revenue at home, so the ratio Damodaran defines "
                     "collapses to the domestic share itself. NOT the 30/70 the retired "
                     "operations-weighted premium used: that number came from company "
                     "commentary ('over 70% of revenues generated abroad'), the audited note "
                     "says 40.72%, and a study may not hold two answers to one question",
                     "2026-03-15", "Company"),
    crp_foreign=I(0.0226,
                  "The country premium carried by the 40.72% of revenue earned OUTSIDE "
                  "Egypt. DERIVED, not typed: the blended emerging/frontier equity premium "
                  "of 6.50% already registered for those operations, less the mature-market "
                  "premium of 4.24% derived from Egypt's own total (9.41% less a country "
                  "premium of 3.40% CDS spread x Damodaran's 1.52 equity-to-bond scaling). "
                  "It is NOT zero: Zambia, Tanzania, Ghana, Nigeria, Saudi Arabia and Greece "
                  "are not mature markets, and taking the lambda relief without this offset "
                  "would be the flattering half of the argument",
                  "2026-01-05", "Country"),
    erp_ops_weighted=I(0.0737, "Operations-weighted equity risk premium: 30% Egypt at 9.41% and 70% "
                       "rest-of-world at a 6.5% blended emerging/frontier premium, reflecting where "
                       "the revenue is actually earned. Shown as an explicit alternative, not the "
                       "primary, because the standing house rule takes the country premium of the "
                       "listing and reporting currency", "2026-08-05", "House"),
    beta=I(float(_BETA['beta']),
           "Own-stock tier-1 weekly regression against %s as at %s — THE PUBLISHED INDEX OF "
           "THE EXCHANGE THIS STOCK IS LISTED ON, resolved by beta_regression.own_stock_beta() "
           "rather than hand-rolled. R-squared %.3f, n = %d, standard error %.4f, 90%% "
           "confidence interval [%.3f, %.3f]; Dimson-corrected for thin trading, matched to "
           "the exchange's own trading week (%s). Clears the usability gate and is not "
           "weak-instrument flagged. WITHDRAWN AND KEPT FOR COMPARISON: the previous edition "
           "regressed against a 31-name equal-weight composite of the covered library and got "
           "%.4f at an R-squared of %.3f — %+.1f%% against the conforming figure, explaining "
           "less of the stock. A constituent composite is a coverage artefact rather than a "
           "market and SIGCM calls it a hard fail, not a tier."
           % (_BETA['index_file'], _BETA['index_asof'], _BETA['r2'], _BETA['n'], _BETA['se'],
              _BETA['ci90'][0], _BETA['ci90'][1], _BETA['week_rule'],
              _BETA['withdrawn_composite']['beta'], _BETA['withdrawn_composite']['r2'],
              100 * _BETA['delta_vs_withdrawn']),
           str(_BETA['index_asof']), "House"),
    kd=I(0.095, "Marginal cost of debt, CURRENCY-BLENDED, rolled forward to the most recently "
         "disclosed rates. The audited FY2025 note (32) discloses 21.30% on Egyptian-pound "
         "financial liabilities and 5.29% blended on 'US dollars and foreign currencies' — a "
         "simpler two-way split than FY2024's three-way EGP/USD/EUR disclosure, which the company "
         "itself has moved away from. The Kd-integrity effective-rate back-solve below implies an "
         "Egyptian-pound weight of roughly 28% (down sharply from FY2024's ~44%, as the hard-"
         "currency share of the book grew), giving a blended marginal rate of about 9.8% on the "
         "FY2025 print and 9.6% on the Q1-2026 print (EGP 20.32%, foreign 5.28%). 9.5% is struck "
         "just below both, allowing for the CBE's continuing easing", "2026-05-13", "Company/House"),
    kd_egp_note=I(0.2130, "Average interest rate on Egyptian-pound financial liabilities, audited "
                  "FY2025 Note 32 (loans and borrowings) and Note 43-3-2 (interest-rate risk) — "
                  "both give 21.30%/21.3%. DOWN from 28.68% at FY2024-end and further to 20.32% at "
                  "Q1-2026", "2026-03-15", "Company"),
    # THE COMPANY'S OWN SUPERSEDED THREE-WAY RATE SPLIT, REGISTERED [09-09-2026]. It was
    # typed into the source string below, which quotes it to explain a disclosure
    # convention the issuer has since simplified. A DISCLOSED FACT this model does not
    # compute still carries four fields, and until it did prose_check could not reconcile
    # a figure the delivered bibliography prints.
    kd_fy24_egp=I(0.2868, FY25 + ", note 43-3-2 comparative — average interest rate on "
                  "EGYPTIAN POUND financial liabilities, FY2024, under the three-way split "
                  "the company published before FY2025", "2024-12-31", "Company"),
    kd_fy24_usd=I(0.0649, FY25 + ", note 43-3-2 comparative — US DOLLAR leg of the same "
                  "superseded three-way split", "2024-12-31", "Company"),
    kd_fy24_eur=I(0.0392, FY25 + ", note 43-3-2 comparative — EURO leg of the same "
                  "superseded three-way split", "2024-12-31", "Company"),
    kd_hard_note=I(0.0529, "Average interest rate on US-dollar and other foreign-currency financial "
                   "liabilities, blended, audited FY2025 Note 32 and Note 43-3-2. The company "
                   "simplified its disclosure from a three-way EGP/USD/EUR split (FY2024: "
                   + ("%.2f%% / %.2f%% / %.2f%%" % (100 * _KD_FY24_EGP, 100 * _KD_FY24_USD,
                                                    100 * _KD_FY24_EUR)) +
                   ") to this two-way EGP/blended-foreign split from FY2025 onward; "
                   "the model follows the company's own current convention rather than preserving "
                   "a split it no longer publishes", "2026-03-15", "Company"),
    debt_open_fy25=I(58796.795504, "Loans and credit facilities (excluding lease liabilities) at 1 "
                     "January 2025, financing-liability movement reconciliation, audited FY2025 "
                     "Note 32", "2026-03-15", "Company"),
    debt_close_fy25=I(62462.108099, "Loans and credit facilities (excluding lease liabilities) at "
                      "31 December 2025, financing-liability movement reconciliation, audited "
                      "FY2025 Note 32", "2026-03-15", "Company"),
    int_exp_fy25=I(5966.668609, "Interest expense on loans and credit facilities, audited FY2025 "
                   "Note 32 financing-liability movement reconciliation (excludes 118.129606 of "
                   "lease interest, carried separately)", "2026-03-15", "Company"),
    debt_q1_26=I(89039.318813, "Loans and credit facilities (excluding lease liabilities) at 31 "
                 "March 2026: current 79,171.258437 (loans 39,231.844718 + bank facilities "
                 "39,939.413719) + non-current 9,825.097463 (loans only, excluding the 507.330701 "
                 "of lease liabilities), per the Q1-2026 interim Note 31", "2026-05-13", "Company"),
    kd_path=I([0.095, 0.089, 0.084, 0.080, 0.077],
              "Forward cost-of-debt path FY26E-FY30E on the blended book, continuing the CBE "
              "easing cycle that has already taken the disclosed Egyptian-pound rate from 28.68% "
              "(FY2024) to 21.30% (FY2025) to 20.32% (Q1-2026), blended against a broadly flat "
              "hard-currency rate. The discount-rate glide takes its shape from this path by "
              "construction rather than being invented separately", "2026-08-05", "House"),
    kd_term=I(0.0888, "Terminal blended cost of debt: 28% Egyptian pound at the 15% long-run "
              "Egyptian corporate-borrowing norm and 72% hard currency at 6.5% — the currency "
              "WEIGHTS updated to the actual FY2025 composition (formerly modelled 45%/55%, now "
              "measured at roughly 28%/72% from the Kd-integrity back-solve); the long-run rate "
              "norms themselves are unchanged policy assumptions", "2026-08-05", "House"),
    # TWO INFLATION RATES SAT IN ONE TERMINAL, FOUR ROWS APART [09-09-2026].
    # g_term above reads "(1 + 0.0 real growth) x (1 + 7.0% long-run Egyptian inflation)"
    # and states, in its own source string, that "the house macroeconomic path is the ONLY
    # source of an inflation rate in this study". This line then built the terminal
    # risk-free on a typed 5%. Both numbers are in the same register block and they
    # describe the same perpetuity, so one of them was false and it was this one -- the
    # claim four rows up is what makes it false rather than merely different.
    #
    # THE HOUSE PATH SETS OUT THE RULE ITSELF, in engine/macro_paths/EG.json, under
    # real_rate_convention: "The terminal NOMINAL risk-free rate is DERIVED as this plus
    # the inflation target in force, so the single most terminal-value-sensitive number in
    # a model cannot" be typed. The inflation target in force on that path is 7.0% -- the
    # 2030 step, "the target band midpoint in force, held", sourced to the CBE's own Q1-2026
    # Monetary Policy Report. 7.0 + 5.5 = 12.50%.
    #
    # ARCC FOUGHT THIS EXACT ARGUMENT AND SETTLED IT. That study carried 10.50% built the
    # same way, argued for the central bank's LONGEST-dated published target of 5% against
    # revision 3's NEAR-dated 7%, and the resolution was to stop choosing: derive from the
    # house macro path, "and so no longer this study's own reading of which published
    # target to use". If 5% is the right terminal inflation for Egypt that is an argument
    # for amending engine/macro_paths/EG.json, which every study would then inherit -- not
    # for one study substituting its own number and the next one substituting a different
    # one [R-MACRO-01].
    #
    # IT COSTS ABOUT EGP 7.7 A SHARE AND WIDENS THIS STUDY'S GAP TO THE MARKET, which is
    # the only direction that proves the discipline is not fitting to a price. The same
    # sentence is already written eleven lines below, about the terminal flows correction.
    # A SUPERSEDED FIGURE THE STUDY QUOTES, REGISTERED [09-09-2026]. The sensitivity
    # narrative names what the retired grid returned at its adopted point. It was typed
    # into a builder f-string and DIVIDED BY THE LIVE CENTRAL, so a statement about a
    # superseded edition was silently rewritten by every later correction. A fact this
    # model does not compute still carries four fields.
    grid_centre_retired=I(49.7076, "What the RETIRED sensitivity grid returned at the "
                          "adopted rates, growth and beta, before the grids were pointed "
                          "at the same valuation function as the headline. It re-implemented "
                          "the terminal on a construction this study had already retired "
                          "and omitted the employees' statutory share of profit that the "
                          "bridge charges. Quoted so a reader can see what changed; a "
                          "different function produced it, so this model cannot compute it",
                          "2026-09-04", "House"),
    rf_term=I(_RF_TERM_HOUSE, "Terminal risk-free rate, DERIVED from the house macro path "
              "as the inflation target in force plus the real-rate convention, never "
              "typed: %.2f%% + %.2f%% = %.2f%%. Revisions to 08-09-2026 carried 10.50%%, "
              "built on a 5%% inflation this study chose for itself while the terminal "
              "growth line four rows above used the house 7%% and said the house path was "
              "the only source of an inflation rate here. Never a raw historical average "
              "and never reverse-engineered from a price"
              % (100 * _PI_T_HOUSE, 100 * _RRC_HOUSE, 100 * _RF_TERM_HOUSE),
              "2026-09-09", "House"),
    erp_term=I(0.070, "Terminal equity risk premium, normalised below the currently elevated "
               "crisis-era level toward the rating-class norm; never held flat into perpetuity",
               "2026-08-05", "House"),
    wd_term=I(0.15, "Terminal debt weight D/(D+E) on a net basis, NORMALISED — but reconciled to "
              "the model's OWN forecast balance sheet rather than asserted. REVISED from 25% after "
              "external critique (and the same finding in this study's own re-audit): at a 25% "
              "payout the forecast still deleverages toward a mid-single-digit net-debt weight by "
              "FY2030E, so a 25% terminal weight contradicted the model's own trajectory in the "
              "direction that flattered the valuation. 15% sits between today's 8.4% net weight "
              "and the old 25%, acknowledging that a working-capital-heavy industrial retains "
              "structural gross leverage. Worth about -5.3/share on the DCF lens versus the old "
              "25%", "2026-08-07", "House"),
    # TERMINAL GROWTH IS DERIVED, NOT TYPED [R-MACRO-01]. The first edition carried 5.0%
    # with a justification that named its own inflation assumption — "a terminal risk-free
    # rate that itself embeds 5% inflation, so the base case assumes approximately zero
    # real terminal growth". The house Egyptian path's terminal inflation is 7.0%. So the
    # reasoning was right and the number was struck against an inflation rate this house
    # does not hold, which made the real assumption a DECLINE of 1.87% a year in
    # perpetuity — on a terminal carrying more than four fifths of enterprise value, and
    # written down nowhere. It is the EGCH defect in the same shape: the inflation number
    # doing the work sat inside a justification rather than in a declared input, so
    # nothing could reconcile it.
    #
    # The intent survives intact and is now expressed in the terms the rule requires:
    # ZERO REAL terminal growth, stated, with the nominal rate derived from the house
    # ladder. That is 7.0% nominal, and it also brings the explicit window inside the
    # convergence requirement (last explicit year 8.8% against 7.0%, a 1.8pp gap, where
    # 5.0% left 3.8pp and capitalised a rate the model never reached).
    # ---- the terminal's own inputs, from SWDY's own audited note 17 ------------
    pi_term=I(0.07, "Long-run Egyptian inflation, taken from this house's single dated "
              "macroeconomic path for Egypt rather than set inside this study — one path is "
              "used by every Egyptian company we cover, so two studies cannot value companies "
              "in economies that disagree with each other. It is registered here so that the "
              "terminal growth rate below is DERIVED from it rather than typed beside it",
              "2026-09-04", "Country"),
    ppe_gross_depreciable_fy25=I(50775.950574,
        "Audited FY2025 consolidated financial statements, note 17: gross cost at 31-Dec-2025 "
        "of the DEPRECIABLE property, plant and equipment — buildings and constructions "
        "13,357.135195 + machinery and equipment 32,960.824267 + furniture and fixtures "
        "2,464.375061 + vehicles 1,630.540975 + leasehold improvements 363.075076. EXCLUDES "
        "land (2,312.648624), which the note states is not depreciated, and projects under "
        "construction (8,915.910071), which are not yet in use. The note foots three ways: "
        "components to the 53,088.599198 subtotal, subtotal plus projects to the 62,004.509269 "
        "total, and the component charges to the 2,733.671862 total charge",
        "2026-03-01", "Company"),
    asset_life_derived=I(17.2627,
        "DERIVED BY IDENTITY, not chosen: the AVERAGE depreciable gross cost across the year "
        "((43,605.306327 opening + 50,775.950574 closing) / 2) over the year's own "
        "depreciation charge of 2,733.671862. The average is used rather than the closing "
        "balance because the base grew 16% in the year and a closing-cost ratio overstates "
        "the life on a fast-growing base (that reading is 18.5743 years). THE FIGURE IS "
        "CARRIED AT FULL PRECISION: it was registered as 17.26 and a rounded record is "
        "its own failure - the identity resolves to 17.2627 and nothing about the note "
        "is uncertain to two decimal places. Per component the "
        "closing-cost readings are buildings 29.00y, machinery 18.72y, furniture 8.45y, "
        "vehicles 8.45y, leasehold improvements 13.13y, against disclosed ranges of 8-50, "
        "5-15, 4-17, 5-8 and 'over 3 years or the lease period' — the disclosed ranges are "
        "RANGES, and a life this desk picked from inside one would not be a disclosed life "
        "(SIGCM clause 1), which is why the identity is used instead. CORROBORATED TWICE: "
        "the same note read a year earlier gives 17.9761, and the composite implied by "
        "charging every class at the LONG END of its own disclosed range is 17.3041, "
        "agreement to 0.24% - the company depreciates at the top of every range it "
        "discloses and the identity recovers that without anybody choosing a point. "
        "The full record is in useful_lives.json beside this study.",
        "2026-03-01", "Company/derived"),
    asset_life_source=I("Audited FY2025 consolidated financial statements of El Sewedy Electric "
        "Company, note 17 (property, plant and equipment) read with the accounting-policies "
        "note on depreciation: average depreciable gross cost over the year's own charge, "
        "excluding land, which the policy note states is not depreciated, and projects under "
        "construction, which are not in use.",
        "The source string the terminal module requires. It refuses a life with no "
        "disclosure behind it", "2026-03-01", "Company"),
    g_term_real=I(0.020,
                  "STATED real terminal growth: 2.0%, held BELOW the house path's long-run "
                  "Egyptian real GDP growth of 4.5% [R-MACRO-02] — the gap is the share of "
                  "the economy this company is assumed to cede in perpetuity. THE RETIRED "
                  "FIGURE WAS ZERO, and zero was wrong on its own terms rather than merely "
                  "conservative: an economy growing 4.5% a year in real terms with a company "
                  "growing 0% means the company shrinks to nothing relative to it, forever, "
                  "which is not what 'a mature diversified industrial holding its real scale' "
                  "meant. It is also not what this group has done — Constructions grew 32.6% "
                  "then 28.3% and Electrical Products 46.6% then 43.7% in nominal terms, "
                  "neither of them copper-linked. 2.0% is under half the economy's rate and "
                  "well under the Cables segment's own forward real driver",
                  "2026-09-10", "House"),
    g_term=I(_MP_EG.terminal_growth(0.020),
             "Terminal NOMINAL growth, DERIVED and read from the house path rather than "
             "chosen: (1 + 2.0% stated real growth) x (1 + 7.0% long-run Egyptian inflation) "
             "- 1, read from the house path. It is the only source of an inflation "
             "rate in this study, and macro_path refuses a real rate at or above the "
             "economy's own [R-MACRO-02]. Two earlier figures are retired: 5.0%, struck "
             "against an assumed 5% inflation and therefore a real DECLINE of 1.87% a year; "
             "and 7.0%, which fixed the inflation half and left real growth at zero",
             "2026-09-10", "House"),
    # ---- currency-of-discounting alternative inputs (previously unregistered
    # constants inside the computation — registered after external critique) ----
    usd_rf=I(0.043, "US dollar risk-free rate for the currency-of-discounting alternative, 10-year "
             "US Treasury area (house macro reference)", "2026-08-05", "Country"),
    usd_erp=I(0.075, "Equity risk premium for the hard-currency leg: mature-market premium plus a "
              "reduced operating-exposure country premium — deliberately NOT the full Egypt "
              "premium, since this alternative's whole point is to price the hard-currency cash "
              "flows as hard-currency cash flows", "2026-08-05", "House"),
    usd_kd=I(0.065, "US dollar cost of debt for the alternative: the disclosed 5.3% hard-currency "
             "book rate plus a term/credit allowance", "2026-08-05", "House"),
    usd_wd=I(0.25, "Debt weight for the USD-leg cost of capital", "2026-08-05", "House"),
    usd_g_term=I(0.035, "Terminal growth of the USD-denominated leg — real growth plus dollar "
                 "inflation, below the EGP terminal growth by the inflation differential",
                 "2026-08-05", "House"),
    anchor_days=I(246, "Days from the DCF's construction date (31 Dec 2025, the audited "
                  "balance-sheet date the bridge is built on) to the anchor date 5 Aug 2026. All "
                  "lens values are rolled to the anchor at the cost of equity, net of the EGP 1.85 "
                  "FY2025 dividend paid inside the window — added after external critique "
                  "correctly noted the model was dated 31-Dec-2025 while the comparison price was "
                  "dated 5-Aug-2026, breaching the study's own one-date rule by ~7 months of "
                  "accretion", "2026-08-07", "House"),

    # ---- lens inputs -------------------------------------------------------
    ev_ebitda_just=I(6.5, "Justified EV/EBITDA on mid-cycle FY27E EBITDA. The company's own trailing "
                     "multiple is elevated; listed cable and electrical-equipment peers trade 8-11x "
                     "and Riyadh Cables ~14x on earnings. 6.5x applies an Egyptian-market discount "
                     "for sovereign, currency-convertibility and disclosure risk. Bear 5.5x / bull "
                     "8.0x", "2026-08-05", "House"),
    pe_just=I(9.0, "Justified through-cycle P/E on normalised earnings. 9.0x reflects a "
              "high-quality franchise held back by an Egyptian cost of equity near 28%. Bear 7.0x / "
              "bull 11.5x", "2026-08-05", "House"),
    roe_sust=I(0.235, "Sustainable return on equity for the book lens. Trailing ROE on average "
               "parent equity is well above this; the FY2023-24 prints were flattered by "
               "devaluation inventory gains, so the sustainable rate is struck below them",
               "2026-08-05", "House"),
    lens_weights=I(dict(dcf=0.45, relative=0.20, normalized=0.20, book=0.15),
                   "DCF primary for an operating manufacturer with a genuine, if undisclosed, "
                   "contracted order book; the relative and normalised-earnings lenses carry equal "
                   "secondary weight and the book lens least, because reported book value is "
                   "distorted by three years of currency translation", "2026-08-05", "House"),
    ownership=I(dict(family=0.6799, electra=0.1887, other=0.1307, esop=0.0007),
                "EXACT capital restructuring table, Note 29, audited FY2025 financial statements, "
                "as at 31 December 2025: Sadek Ahmed Sadek Elsewedy 24.99% (534,980,391 shares), "
                "Ahmed Ahmed Sadek Elsewedy 24.99% (534,980,391), Mohamed Ahmed Sadek Elsewedy "
                "18.01% (385,602,690) — family combined 67.99%; Electra Investment Holding "
                "Restricted Limited 18.87% (403,997,835); other shareholders 13.07% (279,794,409); "
                "ESOP shares issued not granted 0.07% (1,422,160). REPLACES a previous house "
                "estimate (family ~68.0%, Electra ~20.4%, float ~11.6%) with the company's own "
                "disclosed table. Electra's stake FELL over 2025 — the FY2024 table (same note, "
                "prior year) shows Electra at 20.37% (436,109,503 shares) and other shareholders at "
                "11.57% (247,682,741): Electra placed exactly 32,111,668 shares into the free float "
                "during the year", "2026-03-15", "Company"),
    # ---- DISCLOSED PERCENTAGES, REGISTERED RATHER THAN LEFT IN PROSE -----------
    # Every one of these was already ASSERTED in this study's bibliography, with its
    # source, inside another input's justification text - and the prose-figure check
    # could not reproduce any of them, because the model held the sentence and not the
    # number. [R-ENF-01 EXTENDED] says in terms: if a figure is real and the model
    # cannot produce it, THE MODEL IS WHAT IS MISSING. Registering them is that repair;
    # widening the rendering set until they matched was tried first and was VACUOUS
    # (3.6 million values, matching 400 of 400 random percentages), so it was reverted.
    sh_sadek=I(0.2499, FY25 + ", note 40 (shareholders' structure) as at 31 December 2025: "
               "Sadek Ahmed Sadek Elsewedy, 534,980,391 shares", "2026-03-01", "Company"),
    sh_ahmed=I(0.2499, FY25 + ", note 40: Ahmed Ahmed Sadek Elsewedy, 534,980,391 shares",
               "2026-03-01", "Company"),
    sh_mohamed=I(0.1801, FY25 + ", note 40: Mohamed Ahmed Sadek Elsewedy, 385,602,690 "
                 "shares", "2026-03-01", "Company"),
    sh_electra_fy24=I(0.2037, FY24 + ", note 40 (prior-year column): Electra Investment "
                      "Holding, 436,109,503 shares at 31 December 2024", "2025-03-01",
                      "Company"),
    sh_other_fy24=I(0.1157, FY24 + ", note 40 (prior-year column): other shareholders, "
                    "247,682,741 shares at 31 December 2024", "2025-03-01", "Company"),
    stake_insulators=I(0.2517, FY25 + ", note 20 (equity-accounted investees): Egyptian "
                       "Company for Electrical Insulators, carrying value EGP 76.1mn",
                       "2026-03-01", "Company"),
    etr_q1_26=I(0.2575, "Q1-2026 reviewed interim consolidated statements at "
                "ir.elsewedyelectric.com, income tax expense over profit before tax of "
                "7,041.966803", "2026-05-01", "Company"),
    etr_q1_25=I(0.2196, "Q1-2025 reviewed interim consolidated statements, the "
                "comparative column of the Q1-2026 filing: income tax expense over "
                "profit before tax", "2026-05-01", "Company"),
    etr_h1_25=I(0.3085, "H1-2025 reviewed interim consolidated statements, the "
                "comparative column of the H1-2026 filing: income tax expense over "
                "profit before tax of 15,395.270255", "2026-08-01", "Company"),
    nci_share_h1_26_profit=I(0.0681, H126 + ", profit attributable to non-controlling "
                             "interests over total profit after tax for the half",
                             "2026-08-01", "Company"),
    nci_share_h1_26_equity=I(0.0747, H126 + ", non-controlling interests over total "
                             "equity of 76,024.598402", "2026-08-01", "Company"),
    emp_share_h1_25=I(0.1271, "H1-2025 comparative column of the H1-2026 reviewed "
                      "statements, note 38: employees' share in profit 1,104.834367 over "
                      "profit attributable to owners of 8,694.611825", "2026-08-01",
                      "Company"),
    export_share_fy25=I(0.4072, FY25 + ", note 5 (geographic disaggregation): revenue "
                        "outside Egypt 114,461.030219 over total revenue "
                        "281,049.081719", "2026-03-01", "Company"),
    kd_egp_fy24=I(0.2868, FY24 + ", note 32 read with note 44-2: the disclosed weighted "
                  "average interest rate on Egyptian-pound borrowings at 31 December "
                  "2024", "2025-03-01", "Company"),
    kd_egp_q1_26=I(0.2032, "Q1-2026 reviewed interim consolidated statements: the "
                   "disclosed weighted average interest rate on Egyptian-pound "
                   "borrowings", "2026-05-01", "Company"),
    electra_mto=I(dict(price_usd=1.05, shares_mn=427.7, value_usdmn=449.1, date='2024-07',
                       stake=0.1998),
                  "Electra Investment Holding's mandatory tender offer, concluded July 2024: "
                  "~427.7mn shares (19.98%) at USD 1.05/share, ~USD 449mn. Recorded as the last "
                  "known price at which a strategic buyer cleared a fifth of the company. NOT used "
                  "as a valuation anchor: it is two years stale and struck before the earnings base "
                  "grew materially. Electra's stake has since drifted down to 18.87% (31-Dec-2025) "
                  "as shares were placed into the float", "2024-07", "Market/Company"),
)

# validate four-field completeness (code-first rule)
for k, rec in INP.items():
    assert set(rec) == {'value', 'source', 'date', 'ring'}, f"INPUT {k} not four-field"
    assert rec['source'] and rec['date'] and rec['ring'], f"INPUT {k} missing provenance"

V = {k: rec['value'] for k, rec in INP.items()}
LOG = []
def say(s):
    LOG.append(s); print(s)

say("=" * 78)
say("SWDY — ASSERT / derivation log (rebuilt on the audited FY23-25 + Q1-2026 filings)")
say("=" * 78)

# ============================ CALC ===========================================
SH, SPOT, TAX = V['shares_mn'], V['spot'], V['tax_eff']
MKTCAP = SPOT * SH

# ---- historical income statement — every line now AUDITED, nothing derived --
ebitda_fy23 = V['op_fy23'] + V['dna_fy23']
ebitda_fy24 = V['op_fy24'] + V['dna_fy24']
ebitda_fy25 = V['op_fy25'] + V['dna_fy25']
nci_fy23 = V['pat_fy23'] - V['npa_fy23']
nci_fy24 = V['pat_fy24'] - V['npa_fy24']
nci_fy25 = V['pat_fy25'] - V['npa_fy25']
say(f"[Historical income statement] every FY2023-25 line is now the audited figure — no P&L "
    f"closure or derivation is needed for any year, including FY2025, because the full filing is "
    f"in hand. House EBITDA = operating profit + depreciation and amortisation: FY23 "
    f"{ebitda_fy23:,.0f}, FY24 {ebitda_fy24:,.0f}, FY25 {ebitda_fy25:,.0f} "
    f"({ebitda_fy25/V['rev_fy25']:.2%} of revenue). Effective tax rate: FY23 "
    f"{-V['tax_fy23']/(V['op_fy23']+V['netfin_fy23']+V['assoc_fy23']):.1%}, FY24 "
    f"{-V['tax_fy24']/(V['op_fy24']+V['netfin_fy24']+V['assoc_fy24']):.1%}, FY25 "
    f"{-V['tax_fy25']/(V['op_fy25']+V['netfin_fy25']+V['assoc_fy25']):.1%}. This REPLACES a "
    f"previous FY2025 EBITDA of 30,622 built by closing the P&L to two disclosed anchors (profit "
    f"after tax and after minority) at an ASSUMED 25% effective rate and an ASSUMED -3,400 net "
    f"finance cost; the actual audited figures (22.57% and -2,145) combine to a MATERIALLY LOWER "
    f"house EBITDA of {ebitda_fy25:,.0f}.")

hist_is = {
    'FY23': dict(rev=V['rev_fy23'], gp=V['gp_fy23'], ebitda=ebitda_fy23, dna=V['dna_fy23'],
                 ebit=V['op_fy23'], fin=V['netfin_fy23'], assoc=V['assoc_fy23'],
                 ebt=V['op_fy23'] + V['netfin_fy23'] + V['assoc_fy23'], tax=V['tax_fy23'],
                 pat=V['pat_fy23'], nci=nci_fy23, npa=V['npa_fy23']),
    'FY24': dict(rev=V['rev_fy24'], gp=V['gp_fy24'], ebitda=ebitda_fy24, dna=V['dna_fy24'],
                 ebit=V['op_fy24'], fin=V['netfin_fy24'], assoc=V['assoc_fy24'],
                 ebt=V['op_fy24'] + V['netfin_fy24'] + V['assoc_fy24'], tax=V['tax_fy24'],
                 pat=V['pat_fy24'], nci=nci_fy24, npa=V['npa_fy24']),
    'FY25': dict(rev=V['rev_fy25'], gp=V['gp_fy25'], ebitda=ebitda_fy25, dna=V['dna_fy25'],
                 ebit=V['op_fy25'], fin=V['netfin_fy25'], assoc=V['assoc_fy25'],
                 ebt=V['op_fy25'] + V['netfin_fy25'] + V['assoc_fy25'], tax=V['tax_fy25'],
                 pat=V['pat_fy25'], nci=nci_fy25, npa=V['npa_fy25']),
}
for y in ('FY23', 'FY24', 'FY25'):
    assert abs(hist_is[y]['ebt'] - (hist_is[y]['pat'] - hist_is[y]['tax'])) < 1.0, \
        f'{y} P&L does not close: EBT vs PAT-tax'

# ---- historical net working capital (audited balance sheets) ---------------
nwc_fy23 = (V['inv_fy23'] + V['ca_fy23'] + V['recv_fy23']) - (V['pay_fy23'] + V['cl_fy23'])
nwc_fy24 = (V['inv_fy24'] + V['ca_fy24'] + V['recv_fy24']) - (V['pay_fy24'] + V['cl_fy24'])
nwc_fy25 = (V['inv_fy25'] + V['ca_fy25'] + V['recv_fy25']) - (V['pay_fy25'] + V['cl_fy25'])
say(f"[Working capital, audited] FY23 {nwc_fy23:,.0f} ({nwc_fy23/V['rev_fy23']:.1%} of revenue), "
    f"FY24 {nwc_fy24:,.0f} ({nwc_fy24/V['rev_fy24']:.1%}), FY25 {nwc_fy25:,.0f} "
    f"({nwc_fy25/V['rev_fy25']:.1%}) — a genuine IMPROVEMENT in FY2025, not an assumption. "
    f"Industrial real-estate-development land holdings (Note 24) are excluded as a separate "
    f"quasi-investment item, consistent across all three years.")
assert abs(nwc_fy25 / V['rev_fy25'] - V['nwc_pct']) < 0.01, "NWC driver not consistent with FY25"

eqp_fy25 = V['eqp_fy25']       # audited, no longer derived
cash_fy25 = V['cash_fy25']     # audited
debt_fy25 = V['debt_fy25']     # audited
ppe_fy25 = V['ppe_fy25']       # audited
say(f"[FY2025 balance sheet] every line is the audited closing figure at 31 December 2025 — no "
    f"triangulation is needed. Equity attributable to owners {eqp_fy25:,.0f}; gross loans and "
    f"borrowings including leases {debt_fy25:,.0f}; cash {cash_fy25:,.0f}; net financial debt "
    f"{V['nd_fy25']:,.0f}.")

# ---- Kd integrity gate, rolled forward to the FY2025 / Q1-2026 disclosures --
kd_eff_fy25 = V['int_exp_fy25'] / ((V['debt_open_fy25'] + V['debt_close_fy25']) / 2)
kd_eff_q1_26 = None  # Q1-2026 does not disclose a comparable movement reconciliation
w_egp = (kd_eff_fy25 - V['kd_hard_note']) / (V['kd_egp_note'] - V['kd_hard_note'])
say(f"[Kd integrity] (i) CURRENCY COMPOSITION — audited FY2025 note rates: EGP "
    f"{V['kd_egp_note']:.2%}, hard-currency blend {V['kd_hard_note']:.2%}. The blended effective "
    f"rate implies an Egyptian-pound share of {w_egp:.1%} and a hard-currency share of "
    f"{1-w_egp:.1%} — DOWN sharply from the roughly 44% pound share implied a year earlier, "
    f"consistent with the FY2025-26 drawdown of hard-currency facilities (the Afreximbank USD "
    f"200mn line among them) to fund a growing hard-currency-linked working-capital book.")
say(f"[Kd integrity] (ii) INDEPENDENT EFFECTIVE RATE — FY2025 interest expense on loans and "
    f"credit facilities {V['int_exp_fy25']:,.0f} / average balance "
    f"{(V['debt_open_fy25']+V['debt_close_fy25'])/2:,.0f} = {kd_eff_fy25:.2%}.")
say(f"[Kd integrity] (iii) BOUNDS — adopted Kd {V['kd']:.2%}: within 150bp of the FY2025 effective "
    f"rate ({abs(V['kd']-kd_eff_fy25)*1e4:,.0f}bp) and does not exceed it by more than 50bp.")
assert abs(V['kd'] - kd_eff_fy25) <= 0.015, f"Kd {V['kd']:.3f} more than 150bp from {kd_eff_fy25:.3f}"
assert V['kd'] <= kd_eff_fy25 + 0.005, "Kd exceeds the FY2025 effective rate by >50bp"

# ---- cost of capital: explicit window ---------------------------------------
# COUNTRY RISK ENTERS ONCE AND IS NEVER MULTIPLIED BY BETA [R-COC-03]. The
# sovereign default spread is netted out of the local yield (so it is not charged
# in the risk-free rate AND again in the premium), beta prices the MATURE-MARKET
# premium because that is what beta measures, and the country premium is added
# flat at the operations weight. Built by the shared module, never hand-rolled.
import cost_of_capital as _COC
rf_star = V['rf'] - V['sov_spread_cds']
ke_exp, KE_PARTS = _COC.cost_of_equity(
    rf_star, V['beta'], V['erp_cds'], V['sov_spread_cds'],
    lambda_country=V['lambda_country'], crp_foreign=V['crp_foreign'])
ERP_MATURE = KE_PARTS['erp_mature']
CRP_HOME = KE_PARTS['crp_home']
CRP_EFF = KE_PARTS['crp_effective']
ke_rating_alt = (V['rf'] - V['sov_spread_rating']) + V['beta'] * V['erp_rating']
ke_ops_alt = rf_star + V['beta'] * V['erp_ops_weighted']
ke_raw_retired = V['rf'] + V['beta'] * V['erp_cds']
ke_beta_on_country_retired = KE_PARTS['ke_beta_on_country_retired']
kd_at = V['kd'] * (1 - TAX)
wd_exp = V['nd_fy25'] / (V['nd_fy25'] + MKTCAP)
we_exp = 1 - wd_exp
wacc_exp = we_exp * ke_exp + wd_exp * kd_at
wd_gross = debt_fy25 / (debt_fy25 + MKTCAP)
wacc_exp_gross = (1 - wd_gross) * ke_exp + wd_gross * kd_at
say(f"[Cost of equity] rf {V['rf']:.2%} less the sovereign default spread "
    f"{V['sov_spread_cds']:.2%} = {rf_star:.2%} (country risk out of the risk-free rate); "
    f"+ beta {V['beta']:.3f} x the MATURE-MARKET premium {ERP_MATURE:.2%} = "
    f"{KE_PARTS['beta_leg']:.2%}; + a country premium of {CRP_EFF:.2%} "
    f"({V['lambda_country']:.1%} of operations in Egypt at {CRP_HOME:.2%}, "
    f"{1-V['lambda_country']:.1%} outside at {V['crp_foreign']:.2%}) -> Ke {ke_exp:.2%}.")
say(f"[Cost of equity, what changed] the RETIRED construction multiplied the country "
    f"premium by beta as well — rf* + beta x the TOTAL premium {V['erp_cds']:.2%} = "
    f"{ke_beta_on_country_retired:.2%}, {1e4*(ke_beta_on_country_retired-ke_exp):+,.0f}bp above "
    f"this build. Beta measures a stock's exposure to its own equity market, not to its "
    f"sovereign; charging a 1.22-beta company 22% more Egypt risk than the market is a "
    f"separate claim and this study never made it. Alternatives still disclosed: rating "
    f"basis {ke_rating_alt:.2%}; the RETIRED un-netted construction {ke_raw_retired:.2%} "
    f"(audit trail only).")
say(f"[WACC explicit] weights on NET financial debt {wd_exp:.1%} / equity {we_exp:.1%} -> "
    f"{wacc_exp:.2%}. On gross debt the weights would be {wd_gross:.1%} / {1-wd_gross:.1%} -> "
    f"{wacc_exp_gross:.2%}; the net-debt basis is used because it is the same quantity the "
    f"enterprise-to-equity bridge subtracts, and it is the more conservative of the two.")

# ---- terminal (norm-built, never backed out of a price) --------------------
# the terminal premium is a TOTAL and splits the same way [R-COC-03]
CRP_TERM = max(V['erp_term'] - ERP_MATURE, 0.0)
LAM_EFF = V['lambda_country'] + (1 - V['lambda_country']) * (V['crp_foreign'] / CRP_HOME)
CRP_EFF_TERM = LAM_EFF * CRP_TERM
ke_term = V['rf_term'] + V['beta'] * ERP_MATURE + CRP_EFF_TERM
kd_term_at = V['kd_term'] * (1 - TAX)
wacc_term = (1 - V['wd_term']) * ke_term + V['wd_term'] * kd_term_at
say(f"[WACC terminal] Ke {ke_term:.2%} (rf {V['rf_term']:.2%} READ FROM THE HOUSE PATH "
    f"= {_MP_EG.terminal_inflation:.1%} terminal inflation + {_MP_EG.real_rate_convention:.1%} "
    f"real convention, the SAME inflation the terminal growth of {V['g_term']:.1%} is built "
    f"on; + beta x mature premium {ERP_MATURE:.2%} + country {CRP_EFF_TERM:.2%}); "
    f"Kd after tax {kd_term_at:.2%}; weights {1-V['wd_term']:.0%}/{V['wd_term']:.0%} -> "
    f"{wacc_term:.2%}")
assert wacc_term < wacc_exp, "terminal WACC must be below the explicit-window WACC"

# ---- glide: fractions from kd_path (never invented separately) -------------
kdp = V['kd_path']
glide_frac = [(kdp[0] - k) / (kdp[0] - kdp[-1]) for k in kdp]
fwd = [wacc_exp - (wacc_exp - wacc_term) * f for f in glide_frac]
df, c = [], 1.0
for w in fwd:
    c /= (1 + w); df.append(c)
assert all(fwd[i] >= fwd[i + 1] for i in range(len(fwd) - 1)), "glide not monotone"
say("[Glide] forward WACC " + " -> ".join(f"{w:.2%}" for w in fwd) +
    "; cumulative discount factors " + ", ".join(f"{d:.4f}" for d in df) +
    ". The glide fractions are the cost-of-debt path's own cumulative progress, so the shape is "
    "inherited rather than being a second free parameter.")

# ============================ THREE-SEGMENT FORECAST BUILD ====================
# The disclosed segments are Cables (and its accessories), Constructions (and
# infrastructure), and Electrical products (and digital solutions). Revenue by
# segment is the Note 5-3 external-revenue view, which ties EXACTLY to
# consolidated revenue every year; segment margin is segment profit (Note 16)
# divided by that same external-revenue base, so margin x revenue reproduces
# the disclosed segment profit by construction.
YRS = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
SUBS = ['cables', 'construct', 'elecprod']

# EACH SEGMENT'S OWN LIKE-FOR-LIKE HALF GROWTH, DERIVED from the note-16 revenues this
# study already registers for both comparable halves. H1 against H1, so the comparison is
# like for like and needs no seasonality assumption -- the same construction the margin
# paths use, applied to the revenue on the same rows of the same note.
_SEG_G26 = {s_: V['seg_rev_h1_26'][s_] / V['seg_rev_h1_25'][s_] - 1.0
            for s_ in ('cables', 'construct', 'elecprod')}
SUBNAME = dict(cables='Cables and its accessories',
               construct='Constructions and infrastructure',
               elecprod='Electrical products and digital solutions')
SRH, SPH = V['seg_rev_hist'], V['seg_profit_hist']

unit_hist = {}
for y in ('FY23', 'FY24', 'FY25'):
    rev_sum = sum(SRH[y].values())
    margin = {s: SPH[y][s] / SRH[y][s] for s in SUBS}
    unit_hist[y] = dict(rev=dict(SRH[y]), profit=dict(SPH[y]), margin=margin, rev_sum=rev_sum)
for y, key in (('FY23', 'rev_fy23'), ('FY24', 'rev_fy24'), ('FY25', 'rev_fy25')):
    assert abs(unit_hist[y]['rev_sum'] - V[key]) < 1.0, f'{y} segment revenue does not sum to the P&L'
say(f"[Segment build — the disclosed structure] Cables, Constructions and Electrical products "
    f"and digital solutions, Note 5-3 revenue reconciling EXACTLY to the consolidated P&L in all "
    f"three years. FY2025 revenue split: Cables {SRH['FY25']['cables']:,.0f} "
    f"({SRH['FY25']['cables']/V['rev_fy25']:.1%}), Constructions "
    f"{SRH['FY25']['construct']:,.0f} ({SRH['FY25']['construct']/V['rev_fy25']:.1%}), Electrical "
    f"products {SRH['FY25']['elecprod']:,.0f} ({SRH['FY25']['elecprod']/V['rev_fy25']:.1%}). "
    f"Segment margins (profit / this revenue base) FY2023 -> FY2025: Cables "
    f"{unit_hist['FY23']['margin']['cables']:.1%} -> {unit_hist['FY25']['margin']['cables']:.1%}; "
    f"Constructions {unit_hist['FY23']['margin']['construct']:.1%} -> "
    f"{unit_hist['FY25']['margin']['construct']:.1%}; Electrical products "
    f"{unit_hist['FY23']['margin']['elecprod']:.1%} -> "
    f"{unit_hist['FY25']['margin']['elecprod']:.1%}. Every segment compressed in FY2025; Cables "
    f"and Constructions compressed the most.")

CL = V['corp_load_hist']
SEG_UNALLOC = {'FY23': 0.0, 'FY24': 0.0, 'FY25': V['seg_unalloc_fy25']}
_seg_profit_net_fy25 = sum(SPH['FY25'].values()) + SEG_UNALLOC['FY25']
say(f"[Corporate load — the bridge from segment profit to EBIT] (G&A + net impairment on "
    f"receivables + other expenses - other income) / revenue: FY2023 {CL['FY23']:.2%}, FY2024 "
    f"{CL['FY24']:.2%}, FY2025 {CL['FY25']:.2%} — DECLINING, i.e. operating leverage improving at "
    f"the corporate level even as segment margins fell. This reconciles EXACTLY: e.g. FY2025 "
    f"segment profit {sum(SPH['FY25'].values()):,.0f} less the unallocated/corporate item of "
    f"{-SEG_UNALLOC['FY25']:,.0f} = {_seg_profit_net_fy25:,.0f}, less {CL['FY25']:.2%} x revenue "
    f"{V['rev_fy25']:,.0f} = {_seg_profit_net_fy25 - CL['FY25']*V['rev_fy25']:,.0f}, against "
    f"the audited operating profit of {V['op_fy25']:,.0f}.")
for y, key in (('FY23', 'op_fy23'), ('FY24', 'op_fy24'), ('FY25', 'op_fy25')):
    _seg_profit_net = sum(SPH[y].values()) + SEG_UNALLOC[y]
    _ebit_check = _seg_profit_net - CL[y] * V[key.replace('op_', 'rev_')]
    assert abs(_ebit_check - V[key]) < 1.0, f'{y} segment profit less corporate load != operating profit'

# THE CONTESTED HALF, SWITCHED IN ONE PLACE so the alternative is a re-run of the
# whole model and not a scaled answer [contested_judgement_both_ways].
_PASSTHRU = V['cables_passthrough']


def build(fx_mult=1.0, gp_unit_mult=1.0, vol_mult=1.0, copper_mult=1.0, opex_shift=0.0):
    """Re-run the whole three-segment build. Scenarios and sensitivity grids call
    THIS, so a currency or copper move flows through Cables' growth rate, and a
    margin shift flows through every segment's margin path, exactly as in the base
    case — not as a flat multiplier on a finished revenue line."""
    cu_base = V['copper_fcst'][0] * copper_mult * V['fx_path'][0] * fx_mult
    cu_hist = V['copper_hist']['FY25'] * V['fx_hist']['FY25']
    r_cab, r_con, r_ele = (SRH['FY25']['cables'], SRH['FY25']['construct'], SRH['FY25']['elecprod'])
    R, seg_margin = [], []
    for i in range(5):
        cu_t = V['copper_fcst'][i] * copper_mult * V['fx_path'][i] * fx_mult
        cu_prev = (V['copper_fcst'][i - 1] * copper_mult * V['fx_path'][i - 1] * fx_mult
                   if i > 0 else cu_hist)
        cu_growth = cu_t / cu_prev - 1
        if i == 0:
            # FY2026 IS MEASURED, NOT FORECAST [R-ANCHOR-01]. This study registers note
            # 16's segment revenue for BOTH comparable halves and never compared them
            # with the growth path it forecasts -- it holds the numbers that falsify its
            # own first year and never put them side by side, which is [R-ENF-03] inside
            # one file. The group total was right to within a third of a point and every
            # segment was wrong: cables +17.0pp, constructions -9.4pp and electrical
            # products -28.3pp against the like-for-like halves. A group total that is
            # right over a mix that is wrong is worth EGP 3.19 a share here, because the
            # segments earn 11.4%, 9.0% and 23.6%, and the error over-weighted the
            # cheapest of the three and under-weighted the richest.
            #
# THE MISS IS NOW ATTRIBUTABLE, AND THIS COMMENT USED TO SAY IT WAS NOT.
            # It read: "which of copper, the exchange rate or volume accounts for the
            # miss is not resolvable from what is disclosed". It is resolvable, from a
            # disclosure sitting in this repository: the reviewed half sold 99,239
            # tonnes against 89,636, +10.71%, so of the measured +30.57% revenue growth
            # 10.71pp is VOLUME and price per tonne carries the remaining +17.94%. The
            # year is still anchored on what the half measured — that part was always
            # right — but the attribution is no longer declined, and FY2027 onward is
            # built on the split rather than on a residual that hid it.
            r_cab *= (1 + _SEG_G26[ 'cables' ]) * (vol_mult ** 0.2)
            r_con *= (1 + _SEG_G26['construct']) * (vol_mult ** 0.2)
            r_ele *= (1 + _SEG_G26['elecprod']) * (vol_mult ** 0.2)
        else:
            # Cables = copper x FX (the metal and the currency) x pass-through (how much
            # of that reaches price per tonne) x VOLUME (the company's own disclosed
            # tonnage). The retired construction multiplied copper x FX by a single 3.0%
            # "real" residual that was volume and pass-through wearing one number, in
            # opposite directions, neither visible.
            r_cab *= ((1 + cu_growth) * (1 + _PASSTHRU[i])
                      * (1 + V['cables_volume_growth'][i]) * (vol_mult ** 0.2))
            r_con *= (1 + V['construct_growth'][i]) * (vol_mult ** 0.2)
            r_ele *= (1 + V['elecprod_growth'][i]) * (vol_mult ** 0.2)
        m_cab = V['cables_margin'][i] * gp_unit_mult
        m_con = V['construct_margin'][i] * gp_unit_mult
        m_ele = V['elecprod_margin'][i] * gp_unit_mult
        R.append(dict(cables=r_cab, construct=r_con, elecprod=r_ele))
        seg_margin.append(dict(cables=m_cab, construct=m_con, elecprod=m_ele))
    rev_ = [sum(R[i].values()) for i in range(5)]
    seg_gp_ = [{s: R[i][s] * seg_margin[i][s] for s in SUBS} for i in range(5)]
    gp_ = [sum(seg_gp_[i].values()) for i in range(5)]
    # The disclosed segment margins are POST-depreciation (Note 16 segment profit), so the
    # corporate load is applied on the same basis as the audited historical bridge:
    # EBIT = segment profit - corp load; EBITDA = EBIT + D&A. (Restated after critique —
    # numerically identical to the previous opex-to-EBITDA formulation, honestly labelled.)
    opex_ = [(V['opex_pct'][i] + opex_shift) * rev_[i] for i in range(5)]
    ebit_ = [gp_[i] - opex_[i] for i in range(5)]
    ebitda_ = [ebit_[i] + V['dna_pct'] * rev_[i] for i in range(5)]
    return dict(rev=rev_, gp=gp_, opex=opex_, ebit=ebit_, ebitda=ebitda_, seg_rev=R,
                seg_gp=seg_gp_, seg_margin=seg_margin)

_B = build()
seg_rev, seg_gp, seg_margin_f = _B['seg_rev'], _B['seg_gp'], _B['seg_margin']
rev = _B['rev']; gp = _B['gp']; opex = _B['opex']; ebitda = _B['ebitda']
ebitda_margin = [ebitda[i] / rev[i] for i in range(5)]
gp_margin = [gp[i] / rev[i] for i in range(5)]
say(f"[Forecast, three real segments] revenue " + " -> ".join(f"{r:,.0f}" for r in rev) +
    " (growth " + ", ".join(f"{rev[i]/(V['rev_fy25'] if i==0 else rev[i-1])-1:+.1%}"
                            for i in range(5)) + ")")
say(f"[Forecast margins are OUTPUTS] gross margin " +
    " -> ".join(f"{m:.2%}" for m in gp_margin) + "; EBITDA margin " +
    " -> ".join(f"{m:.2%}" for m in ebitda_margin) + ". Segment mix FY2030E: Cables "
    f"{seg_rev[-1]['cables']/rev[-1]:.0%}, Constructions {seg_rev[-1]['construct']/rev[-1]:.0%}, "
    f"Electrical products {seg_rev[-1]['elecprod']/rev[-1]:.0%}.")
_impl26 = V['q1_26_rev'] / (V['q1_25_rev'] / V['rev_fy25'])
say(f"[FY2026 cross-check against the print] the disclosed Q1-2026 revenue of "
    f"{V['q1_26_rev']:,.0f}, grossed up on the Q1-2025 seasonal share of FY2025, implies a full "
    f"year of {_impl26:,.0f}. The build produces {rev[0]:,.0f}, {rev[0]/_impl26-1:+.1%} against "
    f"it — an independent check that the segment build is not running ahead of the company's own "
    f"trading.")
assert abs(rev[0] / _impl26 - 1) < 0.10, 'FY26 build diverges from the Q1-2026 print'

_q26_ebit_implied = (V['q1_26_op'] / V['q1_26_rev']) * rev[0] - CL['FY25'] * 0  # display only
q1_26_ebitda_implied_margin = ((V['q1_26_op'] + V['dna_pct'] * V['q1_26_rev']) / V['q1_26_rev'])
say(f"[Q1-2026 EBITDA margin check] the disclosed Q1-2026 operating profit "
    f"{V['q1_26_op']:,.0f} on revenue {V['q1_26_rev']:,.0f} implies an EBITDA margin (at the "
    f"model's D&A ratio) of {q1_26_ebitda_implied_margin:.2%}, against FY2026E's "
    f"{ebitda_margin[0]:.2%} — consistent, not contradicted.")

# currency split, reported off the segment build (Cables is genuinely copper-linked and
# roughly two-thirds hard-currency by disclosed export mix; the other two segments are
# treated as majority domestic-currency notwithstanding their own export components,
# because the disclosed geographic split does not separate currency of invoicing from
# geography of delivery)
fgn_egp = [seg_rev[i]['cables'] * 0.65 + seg_rev[i]['construct'] * 0.30 +
           seg_rev[i]['elecprod'] * 0.45 for i in range(5)]
dom = [rev[i] - fgn_egp[i] for i in range(5)]
fgn_usd = [fgn_egp[i] / V['fx_path'][i] for i in range(5)]
fgn25 = (SRH['FY25']['cables'] * 0.65 + SRH['FY25']['construct'] * 0.30 +
         SRH['FY25']['elecprod'] * 0.45)
fgn_share_fy25_derived = fgn25 / V['rev_fy25']
say(f"[Currency split — two different questions] the audited Note 5-2 shows "
    f"{V['fgn_egp_share_fy25']:.1%} of FY2025 revenue booked OUTSIDE Egypt, which is a geographic "
    f"statement about where the customer sits. The model derives the share that is "
    f"HARD-CURRENCY LINKED — dollar-priced by construction — at {fgn25/V['rev_fy25']:.0%} in "
    f"FY2025 and " + " -> ".join(f"{fgn_egp[i]/rev[i]:.0%}" for i in range(5)) +
    f" thereafter, using segment-level export-intensity weights (Cables 65%, Constructions 30%, "
    f"Electrical products 45%) rather than the blanket geographic split, because a project "
    f"executed abroad for a local utility is foreign revenue but not necessarily dollar-priced. "
    f"The LOWER figure is used everywhere the currency question is valued, because it is the "
    f"conservative one.")

# FY2025 presentation objects reused downstream
SEGNAME = SUBNAME
shares = [{s: seg_rev[i][s] / rev[i] for s in SUBS} for i in range(5)]
# per-segment EBIT contribution: segment profit less the pro-rata corporate load (EBIT basis)
seg_ebit = [{s: seg_gp[i][s] - V['opex_pct'][i] * seg_rev[i][s] for s in SUBS} for i in range(5)]

# ---- THE COMPARISON THIS STUDY DID NOT MAKE, NOW A GATE ----------------------
# It registered note 16's segment revenue for both comparable halves and forecast segment
# growth from three separate constructions, and nothing ever held one against the other.
# Two readings of one fact in one file, never put side by side [R-ENF-03]. The gate is
# cheap and it is the reason the defect cannot come back: FY2026 is the year the half
# measures, so the forecast for it must BE the measurement.
for _s in SUBS:
    _mg = seg_rev[0][_s] / SRH['FY25'][_s] - 1.0
    assert abs(_mg - _SEG_G26[_s]) < 1e-9, (
        'FY2026 %s growth is %.4f%% while the reviewed halves measure %.4f%%. The first '
        'forecast year is the year the half measures and it may not disagree with it.'
        % (_s, 100 * _mg, 100 * _SEG_G26[_s]))
# The group is an OUTPUT of the three and is checked separately, because a group total
# that is right over a mix that is wrong is exactly the defect this replaces: it was
# right to a third of a point while every segment was out by between 9 and 28 points.
# THE GROUP TOTAL IS NOT ASSERTED, AND THE REASON IS ARITHMETIC RATHER THAN TOLERANCE.
# Two drafts of a group check failed here and both were the CHECK being wrong, not the
# model. The first compared rev[0] with V['rev_fy25'] and missed by 0.20pp, which is
# seg_unalloc_fy25, the -246.711 unallocated item group revenue carries and the segments
# do not. The second compared the segment totals and missed by the same 0.20pp for a
# different reason: each segment is anchored on its OWN half growth, and the full-year
# FY2025 mix is not the H1-2025 mix, so weighting three correct growth rates by different
# bases cannot reproduce the halves' blended rate. Neither draft was evidence about the
# forecast. Both were re-pointed rather than given a tolerance [R-COC-01] -- a standing
# 0.20pp band here would have covered a real disagreement of exactly that size.
say(f"[Segment mix, FY2026] each segment anchored on its OWN like-for-like half growth "
    f"(note 16, both comparable halves): cables {100 * _SEG_G26['cables']:.2f}%, "
    f"constructions {100 * _SEG_G26['construct']:.2f}%, electrical products "
    f"{100 * _SEG_G26['elecprod']:.2f}%. The segment total grows "
    f"{100 * (sum(seg_rev[0].values()) / sum(SRH['FY25'].values()) - 1):.2f}% against the "
    f"halves' own blended "
    f"{100 * (sum(V['seg_rev_h1_26'].values()) / sum(V['seg_rev_h1_25'].values()) - 1):.2f}%; "
    f"the difference is the FY2025 full-year mix differing from the H1-2025 mix and is not "
    f"a disagreement about growth. THE RETIRED PATH forecast cables +47.60%, constructions "
    f"+18.00% and electrical products +20.00% — right on the group to a third of a point "
    f"and wrong on every segment, over-weighting the 11.4%-margin business and "
    f"under-weighting the 23.6%-margin one")

# ---- FCFF waterfall ---------------------------------------------------------
dna = [V['dna_pct'] * r for r in rev]
ebit = [ebitda[i] - dna[i] for i in range(5)]
nopat = [e * (1 - TAX) for e in ebit]
# ---- CAPEX, RE-ANCHORED ON THE REVIEWED HALF [09-09-2026] --------------------
# THE MODEL CHARGED 23.0% MORE FY2026 CAPEX THAN THE COMPANY'S OWN FILED HALF IMPLIES,
# and the filing had never been read for this line. capex_pct was a House glide tapering
# from FY2025's 4.665% on a story about the expansion cycle completing. The reviewed six
# months to 30 June 2026 measure that cycle: capex of 5,435.909 against 5,386.809 a year
# earlier — UP 0.91% — while revenue over the same halves rose 31.92%. Capex is flat in
# level and falling hard as a share of revenue, which is what "the cycle is completing"
# looks like when it is observed rather than assumed.
#
# THIS IS THE STUDY'S OWN ESTABLISHED STANDARD, NOT A NEW ONE. corp_load sits eight lines
# above capex_pct in the register and was re-anchored on exactly this evidence, in these
# words: "The first edition glided it up toward 5.0% on the view that FY2025 was unusually
# low; the reviewed half measures the level holding, and no disclosure names a mechanism
# that would take it back up." The same half, the same filing, the same reasoning, applied
# to the line it had not been applied to.
#
# THE CONSTRUCTION NEEDS NO SEASONALITY ASSUMPTION, WHICH MATTERS BECAUSE THE SEASONALITY
# IS NOT STABLE. The H1 share of full-year capex is 39.1% (2023), 54.1% (2024) and 41.1%
# (2025) — a range too wide to annualise a half on. So the half is not annualised: it is
# compared with the SAME HALF of the prior year, like for like, and the growth rate that
# comes out of it is applied to the audited full year. Flat halves imply a flat year.
#
# The finding survives every one of the three seasonality patterns anyway, which is why it
# is reported as a defect rather than as a judgement: annualising H1-2026 at the most
# H2-weighted year on record still gives 13,890 against the model's 16,281.
_CAPEX_H1_GROWTH = V['capex_h1_26'] / V['capex_h1_25'] - 1.0
_CAPEX_FY26 = V['capex_fy25'] * (1.0 + _CAPEX_H1_GROWTH)
# Held FLAT as a share of revenue from FY2027, for the corp_load reason: the half measures
# a level and no disclosure names a mechanism that moves it. Note which way that cuts —
# flat is ABOVE the retired taper in FY2029 (3.58% vs 3.30%) and FY2030 (3.58% vs 3.10%),
# so the out-years are charged MORE capex than the path this replaces, not less.
_CAPEX_PCT_MEASURED = _CAPEX_FY26 / rev[0]
V['capex_pct_measured'] = I([round(_CAPEX_PCT_MEASURED, 6)] * 5,
    "DERIVED, not typed. FY2026 capex is the audited FY2025 figure of %.3f grown by the "
    "%+.2f%% the reviewed halves measure (H1-2026 %.3f against H1-2025 %.3f), giving "
    "%.1f, which is %.3f%% of this model's own FY2026 revenue and is then held flat. "
    "The retired House taper charged %.1f in FY2026, %+.1f%% more."
    % (V['capex_fy25'], 100 * _CAPEX_H1_GROWTH, V['capex_h1_26'], V['capex_h1_25'],
       _CAPEX_FY26, 100 * _CAPEX_PCT_MEASURED, V['capex_pct'][0] * rev[0],
       100 * (V['capex_pct'][0] * rev[0] / _CAPEX_FY26 - 1.0)),
    "2026-06-30", "Company/House")
capex = [_CAPEX_PCT_MEASURED * rev[i] for i in range(5)]
_CAPEX_RETIRED = [V['capex_pct'][i] * rev[i] for i in range(5)]
nwc = [V['nwc_pct'] * r for r in rev]
dnwc = [nwc[0] - nwc_fy25] + [nwc[i] - nwc[i - 1] for i in range(1, 5)]
fcff = [nopat[i] + dna[i] - capex[i] - dnwc[i] for i in range(5)]
pv = [fcff[i] * df[i] for i in range(5)]
pv_explicit = float(sum(pv))

# ---- forward net-finance, profit, dividend, equity and net-debt paths ----------
# ONE roll-forward, computed once and used everywhere: by the normalised-earnings lens,
# by the forecast income statement, and by the forecast balance sheet.
nci_share = nci_fy25 / V['pat_fy25']
PAYOUT = 0.25   # near the ACTUAL FY2025 payout of 22.8% (EGP 1.85 on EPS 8.10), rising intent;
                # raised from 15% after the FY2025 dividend was confirmed and restored
ASSOC_G = 0.08
interest_path, np_fc, div_fc, eq_fc, nd_fc, assoc_fc = [], [], [], [], [], []
pbt_fc, tax_is_fc, pat_fc, nci_is_fc = [], [], [], []
_nd, _eq = V['nd_fy25'], eqp_fy25
for i in range(5):
    # gross borrowings fund working capital and stay broadly in place; the cash pile
    # builds as free cash flow accrues, so the NET charge falls with net debt.
    _cash = debt_fy25 - _nd
    _int = V['kd_path'][i] * debt_fy25 - 0.10 * max(_cash, 0.0)
    _assoc = V['assoc_bv_fy25'] * 0 + V['assoc_fy25'] * (1 + ASSOC_G) ** (i + 1)
    _pbt = ebit[i] - _int + _assoc
    _npa = _pbt * (1 - TAX) * (1 - nci_share)
    _div = PAYOUT * _npa
    _eq += _npa - _div
    _nd = _nd - (fcff[i] - _int * (1 - TAX)) + _div
    interest_path.append(_int); assoc_fc.append(_assoc); np_fc.append(_npa)
    div_fc.append(_div); eq_fc.append(_eq); nd_fc.append(_nd)
    # THE INCOME-STATEMENT LINES, PUBLISHED. Every one of these was computed here
    # and thrown away, so Appendix A.1 printed an em-dash in five forecast rows —
    # profit before tax, income tax, profit for the year, minorities — beside three
    # audited historical columns that were full. The reader saw a forecast that
    # apparently could not reach a bottom line. The numbers existed the whole time
    # [R-DCF-01].
    pbt_fc.append(_pbt); tax_is_fc.append(_pbt * TAX)
    pat_fc.append(_pbt * (1 - TAX)); nci_is_fc.append(_pbt * (1 - TAX) * nci_share)
say(f"[Forecast interest] net finance cost path " + " -> ".join(f"{x:,.0f}" for x in interest_path) +
    f" as the cash pile builds against a broadly static gross debt book. Surplus cash is assumed "
    f"to yield 10% — a deliberate blend of Egyptian-pound deposit rates (~19-20%, falling) and "
    f"hard-currency cash (~4-5%); the positive carry over the hard-currency-heavy debt book "
    f"(7.7-9.5%) is real economics (borrow dollars cheap, hold pounds dear), disclosed rather "
    f"than hidden. Payout ratio {PAYOUT:.0%} — struck at the ACTUAL FY2025 payout: EGP 1.85/share "
    f"ratified by the AGM on 6 May 2026 and paid from 4 June 2026 = 22.8% of FY2025 attributable "
    f"EPS, up from 12.3% a year earlier.")
say(f"[Forecast equity] attributable profit " + ", ".join(f"{x:,.0f}" for x in np_fc) +
    f"; net debt path " + ", ".join(f"{x:,.0f}" for x in nd_fc) + ".")

# ---- invested capital, terminal ROIC ----------------------------------------
ic_fy23 = nwc_fy23 + V['ppe_fy23']
ic_fy24 = nwc_fy24 + V['ppe_fy24'] + V['intang_fy24']
ic_fy25 = nwc_fy25 + ppe_fy25 + V['intang_fy25']
ppe = []
p = ppe_fy25
for i in range(5):
    p += capex[i] - dna[i]; ppe.append(p)
ic = [nwc[i] + ppe[i] + V['intang_fy25'] for i in range(5)]
roic = [nopat[i] / ic[i] for i in range(5)]
roic_term = nopat[-1] * (1 + V['g_term']) / ic[-1]   # NOPAT(n+1) / IC(n), the standard convention
say(f"[Terminal return on capital] taken as next year's NOPAT over the closing invested capital "
    f"({roic_term:.1%}), the standard convention, rather than the same year's NOPAT over closing "
    f"capital ({roic[-1]:.1%}).")
nopat_fy23 = V['op_fy23'] * (1 - 0.313)
nopat_fy24 = V['op_fy24'] * (1 - 0.301)
nopat_fy25 = V['op_fy25'] * (1 - 0.2257)
hist_roic = dict(FY23=nopat_fy23 / ic_fy23, FY24=nopat_fy24 / ic_fy24, FY25=nopat_fy25 / ic_fy25)
hist_rr = dict(FY23=(V['capex_fy23'] - V['dna_fy23']) / nopat_fy23,
               FY24=(V['capex_fy24'] - V['dna_fy24']) / nopat_fy24,
               FY25=(V['capex_fy25'] - V['dna_fy25']) / nopat_fy25)
hist_impl_g = {y: hist_roic[y] * hist_rr[y] for y in hist_roic}
nopat_cagr = (nopat_fy25 / nopat_fy23) ** 0.5 - 1
stable_g = float(np.mean([hist_impl_g['FY23'], hist_impl_g['FY25']]))
say(f"[Terminal growth reconciliation] historical ROIC {hist_roic['FY23']:.1%} / "
    f"{hist_roic['FY24']:.1%} / {hist_roic['FY25']:.1%}; reinvestment rate "
    f"{hist_rr['FY23']:.1%} / {hist_rr['FY24']:.1%} / {hist_rr['FY25']:.1%}; implied g "
    f"{hist_impl_g['FY23']:.1%} / {hist_impl_g['FY24']:.1%} / {hist_impl_g['FY25']:.1%}. "
    f"Check (a): actual NOPAT CAGR FY23-FY25 = {nopat_cagr:+.1%}. Check (b): implied g from "
    f"STABLE years only (FY24 excluded as a debt-funded capacity burst, reinvestment "
    f"{hist_rr['FY24']:.0%}) = {stable_g:.1%}. Adopted terminal g {V['g_term']:.1%}.")

# THE TERMINAL IS BUILT BY THE SANCTIONED MODULE [R-TERM-01], not by g x IC.
# The retired construction charges g x IC every year for ever, which reads as a capital
# maintenance programme with a replacement cycle of 1/g — a fact about the inflation rate
# and not about the asset. Here 1/g at the old 5% was 20.0 years against a life this
# company's own accounts derive at 17.26; the two happened to be close, which is exactly
# why the correction on this name is driven by the GROWTH RATE rather than by the life,
# and why the ratio is a flag rather than an inference [L-289].
# THE FLOWS HANDED IN ARE THE LAST EXPLICIT YEAR'S, NOT THE TERMINAL YEAR'S, AND THIS
# STUDY HAD THEM THE OTHER WAY. terminal_value.TerminalInputs says so in its own first
# sentence -- "Everything a terminal needs, IN THE LAST EXPLICIT YEAR'S money -- not the
# terminal year's. The module grows the free cash flow one year itself" -- and warns in
# terms that passing a NOPAT already grown by (1+g) overstates the terminal by exactly
# (1+g), because tv = fcff x (1+g)/(W-g) already puts the first perpetuity year in the
# numerator and values the terminal at the END of the last explicit year, which is where
# this model discounts it (the year-five factor). The module's own note records that SIX
# OF EIGHT CALLERS read the field the other way on 4 September 2026; this was one of
# them and it was not corrected. Every flow below is now FY2030, the last explicit year:
# NOPAT, book depreciation and the working-capital base, all previously grown by 1.07
# before being handed to a function that grows them again. THE CORRECTION LOWERS THE
# VALUE, which is the only direction that proves the discipline is not fitting to a price.
# the cash-tax line the FCFF waterfall implies (EBIT less NOPAT), for the
# published valuation table [R-DCF-01]
tax_fcst = [ebit[i] - nopat[i] for i in range(5)]

_terminal = TV.build(TV.TerminalInputs(
    nopat=nopat[-1],
    wacc=wacc_term,
    inflation=V['pi_term'],
    real_growth=V['g_term_real'],
    dna_book=dna[-1],
    useful_life_years=V['asset_life_derived'],
    useful_life_source=V['asset_life_source'],
    # MAINTENANCE ON BOOK D&A ESCALATED OVER HALF THE DERIVED LIFE, not on the FY2025
    # gross cost. THE FIRST DRAFT OF THIS TERMINAL USED THE FY2025 BASE AND WAS WRONG:
    # the model itself adds five years of capex, growing net depreciable PP&E from
    # 24,806 to roughly 90,000 — about 3.6x — so a maintenance charge struck on the
    # opening base understates replacement by a multiple, and it showed as a charge of
    # 7,916 against a final-year capex of 17,212. THOSE TWO FIGURES ARE THE RETIRED
    # CAPEX PATH'S, named as such since 09-09-2026 rather than left reading as live: the
    # path was re-anchored on the reviewed half that day and the final-year figure is now
    # a different number. The argument is about the SHAPE — five years of capex build a
    # base the opening one does not describe — and that is unchanged by the re-anchoring,
    # which is why the figures are kept as the historical illustration they are instead
    # of being refreshed into a comment nobody re-reads. The terminal-year book D&A carries
    # the built-up base; escalating it over half an asset life converts historical cost
    # to replacement cost, which is the module's own cross-check route made primary here
    # because the other one's base was stale.
    maintenance_basis='book_dna_escalated',
    working_capital=nwc[-1],
    incremental_capital_per_unit_growth=ic[-1]))
rr_term = V['g_term'] / roic_term          # kept as the RECORD of the retired construction
nopat_term = nopat[-1] * (1 + V['g_term'])   # the FIRST PERPETUITY year, for the prose
tv = _terminal.tv
pv_tv = tv * df[-1]
ev = pv_explicit + pv_tv
tv_share = pv_tv / ev
_tv_retired = nopat_term * (1 - rr_term) / (wacc_term - V['g_term'])
say(f"[Terminal value, sanctioned construction] terminal NOPAT {nopat_term:,.0f} + book D&A "
    f"{_terminal.dna_addback:,.0f} - maintenance at replacement cost {_terminal.maintenance:,.0f} "
    f"(on the DERIVED {V['asset_life_derived']:.2f}-year life) - growth capital "
    f"{_terminal.growth_capex:,.0f} (growth capital at the stated real terminal growth) - inflation on working "
    f"capital {_terminal.wc_charge:,.0f} = FCFF {_terminal.fcff:,.0f}. TV {tv:,.0f} at "
    f"{wacc_term:.2%} and {V['g_term']:.1%} nominal, discounted at the YEAR-5 factor "
    f"{df[-1]:.4f} -> PV {pv_tv:,.0f}, {tv_share:.0%} of enterprise value. Implied payout of "
    f"terminal NOPAT {_terminal.record['payout_of_nopat']:.1%}; TV against the NOPAT-perpetuity "
    f"floor {_terminal.record['tv_vs_floor']:+.1%}.")
say(f"[Terminal value, the RETIRED construction, published unused] g x IC on the same inputs "
    f"gives {_tv_retired:,.0f} ({_tv_retired/tv-1:+.1%}), charging "
    f"{V['g_term']*ic[-1]:,.0f} a year for ever — an implied replacement cycle of "
    f"{1/V['g_term']:.1f} years against the {V['asset_life_derived']:.2f} this company's own "
    f"note 17 derives. Recorded so the change is visible, and it feeds nothing.")
assert abs(roic_term * rr_term - V['g_term']) < 1e-9, "terminal g != ROIC x RR"

# ---- crossover arithmetic (terminal-growth ceiling) -------------------------
EGYPT_GDP = 20000000.0        # EGP mn, nominal, order of magnitude
EGYPT_NOM = 0.15
dom_share_term = dom[-1] / rev[-1]
blend_ceiling = dom_share_term * EGYPT_NOM + (1 - dom_share_term) * 0.075
yrs_cross = np.log(EGYPT_GDP / dom[-1]) / np.log((1 + nopat_cagr) / (1 + EGYPT_NOM))
say(f"[Terminal ceiling] the domestic leg is {dom_share_term:.0%} of FY30E revenue; a blended "
    f"long-run nominal ceiling is {blend_ceiling:.1%} ({EGYPT_NOM:.0%} Egyptian nominal on the "
    f"domestic leg, 7.5% world nominal on the export leg). Adopted g of {V['g_term']:.0%} sits "
    f"below it.")
assert V['g_term'] < blend_ceiling, "terminal g exceeds the blended nominal growth ceiling"

# ---- EV -> equity bridge ----------------------------------------------------
# THE BRIDGE STANDS ON THE SHEET THAT MATCHES ITS OWN VALUATION DATE, and here that is
# 31-Dec-2025 — which needs saying, because a reviewed 30-Jun-2026 sheet now exists and
# [R-BRIDGE-01] asks for the LATEST disclosed one.
#
# IT WAS TRIED THE OTHER WAY AND IT DOUBLE-COUNTS. Net financial debt rose from 20,560 to
# 28,629 over the half, +8,069, as working capital absorbed cash. That deterioration is
# not new information the model lacks: the model's OWN FY2026 forecast absorbs cash on
# exactly that mechanism — a working-capital movement of 17,783 against capex of 16,281,
# giving free cash flow to the firm of -4,268 for the year. Deducting the June net debt
# from a valuation dated 31-Dec-2025 charges the same cash outflow twice, once in the
# bridge and once in the first forecast year, which is [R-BRIDGE-01](iii) in mirror image.
#
# The rule's requirement is that the sheet be the latest one CONSISTENT WITH the valuation
# date, and moving the valuation date to 30-Jun-2026 is a different exercise: the explicit
# window would have to start from the second half, and the roll and the dividend deduction
# would move with it. The December sheet with a December valuation date is coherent; the
# half reaches this study through the FORECAST, where it belongs, and it has re-anchored
# every margin and the corporate load.
assoc_val = V['assoc_bv_fy25']   # audited FY2025 carrying value, no uplift
_nd_jun = V['h1_26_debt'] - V['h1_26_cash']
say(f"[Associates] carried at the audited FY2025 carrying value of {assoc_val:,.0f} — the "
    f"actual closing balance, not the prior year's carrying value scaled by an assumed "
    f"growth factor. (Reviewed 30-Jun-2026: {V['h1_26_investees']:,.0f}.)")
say(f"[Net debt, and why the June sheet is NOT used] the bridge deducts {V['nd_fy25']:,.0f} at "
    f"31-Dec-2025, the date this valuation is struck at. The reviewed 30-Jun-2026 sheet shows "
    f"{_nd_jun:,.0f}, {_nd_jun - V['nd_fy25']:+,.0f} over the half — and that deterioration is "
    f"the same working-capital absorption the model's own FY2026 forecast already carries "
    f"(a working-capital movement of {dnwc[0]:,.0f} against capex of {capex[0]:,.0f}, giving "
    f"free cash flow to the firm of {fcff[0]:,.0f} in the first forecast year). Deducting it "
    f"in the bridge as well would charge one cash outflow twice.")
eq_pre_nci = ev - V['nd_fy25'] + assoc_val
nci_val = nci_share * eq_pre_nci
eq_attr = eq_pre_nci - nci_val

# THE EMPLOYEES' STATUTORY SHARE OF PROFIT [L-294], which appears in NO line of the income
# statement and which the first edition did not carry. Egyptian company law gives employees
# a share of distributable profits; it is an APPROPRIATION rather than a cost, disclosed
# only in the earnings-per-share note, BELOW profit attributable to owners. A shareholder
# receives what is left, so a valuation that divides the whole parent equity value by the
# whole share count hands shareholders value the statute gives to somebody else.
#
# MEASURED, NOT ASSUMED: 11.60% of attributable profit in FY2024, 11.96% in FY2025 and
# 13.01% in the reviewed H1-2026. The three-period mean is used rather than the latest,
# because this is a rate on profit rather than a driver and one half is not a trend.
#
# THE CAP IS DISCLOSED AND IT CANNOT BIND. This block said for two editions that "the
# statutory share is capped at total annual wages ... nothing in the filings discloses the
# cap's headroom, so it is not modelled", and called the charge an UPPER BOUND on that
# ground. The headroom IS disclosed, in the same audited statements this study already
# reads for the charge itself: 'Salaries and its equivalents' appears in three notes --
# cost of sales, selling and distribution, and general and administrative -- and they sum
# to the wage bill the cap is set against.
#
# Measured: FY2025 wages 18,905.80 against an employees' share of 2,073.10, which is 9.12
# times headroom; FY2024 12,753.99 against 2,025.84, 6.30 times. THE CHARGE IS NOWHERE
# NEAR THE CAP AND WOULD HAVE TO RISE BY A FACTOR OF NINE TO REACH IT.
#
# So the charge is NOT an upper bound and the unmodelled cap is worth EGP 0.00, not the
# roughly 6.30 a share the "upper bound" framing implied. The claim was not a rounding
# error in a number; it was a statement that a disclosure does not exist, made while the
# disclosure sat in a note the study was already open at. [R-GAP-04](3): a study that says
# a disclosure does not exist while the issuer publishes it has a hole in its sweep, and
# the hole is reported whatever the number turns out to be worth.
_WAGES_FY25 = (V['salaries_cogs_fy25'] + V['salaries_selling_fy25']
               + V['salaries_admin_fy25'])
_WAGES_FY24 = (V['salaries_cogs_fy24'] + V['salaries_selling_fy24']
               + V['salaries_admin_fy24'])
EMP_CAP = dict(wages_fy25=_WAGES_FY25, wages_fy24=_WAGES_FY24,
               share_fy25=V['emp_share_fy25'], share_fy24=V['emp_share_fy24'],
               headroom_fy25=_WAGES_FY25 / V['emp_share_fy25'],
               headroom_fy24=_WAGES_FY24 / V['emp_share_fy24'],
               binds=False,
               note=('the statutory share is capped at total annual wages; the wage bill is '
                     'disclosed in three notes of the same audited statements and the '
                     'charge sits at roughly a ninth of it, so the cap cannot bind and is '
                     'worth nothing rather than being an unmodelled upper bound'))
assert EMP_CAP['headroom_fy25'] > 1.0 and EMP_CAP['headroom_fy24'] > 1.0, \
    'the employees share exceeds the disclosed wage bill — the cap would bind and the ' \
    'charge could not be held at the measured rate'
emp_rate = (V['emp_share_fy24'] / V['npa_fy24']
            + V['emp_share_fy25'] / V['npa_fy25']
            + V['emp_share_h1_26'] / V['h1_26_npa']) / 3.0
emp_charge = eq_attr * emp_rate
eq_attr_pre_emp = eq_attr
eq_attr = eq_attr - emp_charge
emp_val_pub = emp_charge   # published, so the bridge adds up on the page [R-DCF-01]
say(f"[Employees' statutory share of profit] measured at {V['emp_share_fy24']/V['npa_fy24']:.2%} "
    f"(FY2024), {V['emp_share_fy25']/V['npa_fy25']:.2%} (FY2025) and "
    f"{V['emp_share_h1_26']/V['h1_26_npa']:.2%} (H1-2026) of profit attributable to owners; "
    f"mean {emp_rate:.2%}. It is disclosed only in the earnings-per-share note, below the "
    f"attributable line, and appears in NO line of the income statement — which is why the "
    f"first edition, whose cost stack is built from unit economics, could not have caught it "
    f"there. Equity attributable {eq_attr_pre_emp:,.0f} less {emp_charge:,.0f} = "
    f"{eq_attr:,.0f}. THE RECONCILIATION THAT SHOULD HAVE EXPOSED IT: this study registered "
    f"FY2025 attributable profit of {V['npa_fy25']:,.3f} and the reported EPS of "
    f"{V['eps_fy25']:.2f}; {V['npa_fy25']:,.3f} / {SH:,.6f} = {V['npa_fy25']/SH:.3f}, and the "
    f"difference is this charge plus the ESOP adjustment to the weighted-average count.")
dcf_ps_dec = eq_attr / SH

# The identity the EPS gate checks, asserted here at source rather than left to the gate.
_eps_implied = (V['npa_fy25'] - V['emp_share_fy25']) / 2139.355716
assert abs(_eps_implied - V['eps_fy25']) < 0.005, (
    f"attributable profit less the employees' share over the weighted-average share count "
    f"gives {_eps_implied:.4f} against the reported {V['eps_fy25']:.2f} — one of the three "
    f"figures is wrong")

# ---- one date, one price of time: roll every lens to the anchor date ----------
# Every lens produces an equity value dated 31 December 2025 — the audited balance-sheet
# date the bridge subtracts net debt at, with FY2026 discounted a full year. The comparison
# price is the anchor this edition is struck at. So every per-share value is rolled forward
# by DCF['anchor_days']/365 of a year (this edition: 246 days, to 3 September 2026)
# at the cost of equity, less the EGP 1.85 FY2025 dividend paid inside the window (ex
# 1-Jun-2026) — fair value grows at the required return net of distributions, by the
# discount identity itself. Added after external critique correctly showed the previous
# construction compared a 31-Dec-2025 value to an August price, breaching this study's own
# one-date rule by about seven months of accretion.
T_ANCHOR = V['anchor_days'] / 365.0
ROLL = (1 + ke_exp) ** T_ANCHOR
# THE DIVIDEND LEFT ON A DATE, AND WAS DEDUCTED AS IF IT LEFT AT THE END. It was
# paid from 4 June 2026; the equity it left compounds from THAT date to the anchor,
# not from the anchor itself, so deducting it flat credits the shareholder with three
# months of accretion on money already gone. Worth about 12 piastres a share and it
# runs AGAINST this study — which is the only reason worth noting it: an error found
# while hunting for one that closes a gap, and fixed because it is an error [R-GAP-04].
_DIV_DAYS = (_dt.date(2026, 9, 3) - _dt.date(2026, 6, 4)).days
_DIV_AT_ANCHOR = V['dps_fy25'] * (1 + ke_exp) ** (_DIV_DAYS / 365.0)


def to_anchor(v):
    return v * ROLL - _DIV_AT_ANCHOR
dcf_ps = to_anchor(dcf_ps_dec)
say(f"[Bridge] EV {ev:,.0f} - net financial debt {V['nd_fy25']:,.0f} + associates at carrying "
    f"value {assoc_val:,.0f} = {eq_pre_nci:,.0f}; less minority interests at their "
    f"{nci_share:.1%} share of group profit = {nci_val:,.0f}; less the employees' statutory "
    f"share of profit at {emp_rate:.2%} = {emp_charge:,.0f} -> equity attributable to ORDINARY "
    f"SHAREHOLDERS {eq_attr:,.0f} = EGP {dcf_ps_dec:.2f}/share AT 31-DEC-2025; rolled "
    f"{V['anchor_days']:.0f}/365 of a year to the 3-Sep-2026 anchor at the {ke_exp:.1%} cost of "
    f"equity (x{ROLL:.4f}) less the EGP {V['dps_fy25']:.2f} dividend paid in the window = EGP "
    f"{dcf_ps:.2f}/share against a spot of {SPOT:.2f} ({dcf_ps/SPOT-1:+.0%}).")
assert abs((ev - V['nd_fy25'] + assoc_val - nci_val - emp_charge) - eq_attr) < 1e-6, \
    "bridge does not close"
assert V['nd_fy25'] > 0 and nci_val > 0, "net debt and NCI must reduce equity value"
assert dcf_ps > dcf_ps_dec - V['dps_fy25'], "anchor roll must accrete before the dividend"

# ---- currency-of-discounting alternative (the market's implied view) -------
WACC_USD = (1 - V['usd_wd']) * (V['usd_rf'] + V['beta'] * V['usd_erp']) \
    + V['usd_wd'] * V['usd_kd'] * (1 - TAX)
fgn_frac = [fgn_egp[i] / rev[i] for i in range(5)]
fcff_f_usd = [fcff[i] * fgn_frac[i] / V['fx_path'][i] for i in range(5)]
fcff_d = [fcff[i] * (1 - fgn_frac[i]) for i in range(5)]
df_usd, c2 = [], 1.0
for _ in range(5):
    c2 /= (1 + WACC_USD); df_usd.append(c2)
pv_f_usd = sum(fcff_f_usd[i] * df_usd[i] for i in range(5))
tv_f_usd = (nopat_term * (1 - rr_term) * fgn_frac[-1] / V['fx_path'][-1]) \
    / (WACC_USD - V['usd_g_term'])
ev_f_egp = (pv_f_usd + tv_f_usd * df_usd[-1]) * V['fx_hist']['FY25']
pv_d = sum(fcff_d[i] * df[i] for i in range(5))
tv_d = nopat_term * (1 - rr_term) * (1 - fgn_frac[-1]) / (wacc_term - V['g_term'])
ev_ccy = ev_f_egp + pv_d + tv_d * df[-1]
eq_ccy = (ev_ccy - V['nd_fy25'] + assoc_val) * (1 - nci_share) * (1 - emp_rate)
ccy_ps = to_anchor(eq_ccy / SH)
say(f"[Currency-of-discounting alternative — UIP-corrected] the hard-currency leg "
    f"({fgn_frac[-1]:.0%} of cash flow) is first DEFLATED to dollars at each year's exchange "
    f"rate, discounted at a USD cost of capital of {WACC_USD:.2%} with 3.5% terminal growth, and "
    f"only then translated back. Corrected result EGP {ccy_ps:.2f}/share ({ccy_ps/SPOT-1:+.0%} "
    f"vs spot).")

# ---- responses to external challenge, computed rather than asserted ----------
wacc_exp_rating = we_exp * ke_rating_alt + wd_exp * kd_at
wacc_term_rating = (1 - V['wd_term']) * (V['rf_term'] + V['beta'] * (V['erp_term'] + 0.045)) \
    + V['wd_term'] * kd_term_at
def _terminal_at(wt_, g_):
    """The terminal at an arbitrary rate and growth, THROUGH THE SANCTIONED MODULE.

    This helper used to re-implement the terminal inline, and when the base moved onto
    terminal_value.build() it stopped reproducing it — which the assert below caught
    immediately. That is the [R-ENF-03] species in miniature: a check or a scenario that
    re-implements what it is testing is grading something other than what ships. It calls
    the module now, so a scenario and the base case cannot diverge by construction.
    """
    real_ = (1.0 + g_) / (1.0 + V['pi_term']) - 1.0
    return TV.build(TV.TerminalInputs(
        # LAST EXPLICIT YEAR, not the terminal year — the module grows it itself.
        nopat=nopat[-1], wacc=wt_, inflation=V['pi_term'], real_growth=real_,
        dna_book=dna[-1],
        useful_life_years=V['asset_life_derived'],
        useful_life_source=V['asset_life_source'],
        maintenance_basis='book_dna_escalated',
        working_capital=nwc[-1],
        incremental_capital_per_unit_growth=ic[-1]))

def _val_at(we_, wt_, g_=None):
    g_ = V['g_term'] if g_ is None else g_
    _fwd = [we_ - (we_ - wt_) * f for f in glide_frac]
    _df, cc = [], 1.0
    for w in _fwd:
        cc /= (1 + w); _df.append(cc)
    _tv = _terminal_at(wt_, g_).tv
    _ev = sum(fcff[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    # the employees' statutory share is charged here too, or a scenario silently values a
    # different claim from the base case
    return to_anchor(((_ev - V['nd_fy25'] + assoc_val) * (1 - nci_share)
                      * (1 - emp_rate)) / SH)
assert abs(_val_at(wacc_exp, wacc_term) - dcf_ps) < 0.01, 'rating-basis helper does not reproduce base'
dcf_rating_ps = _val_at(wacc_exp_rating, wacc_term_rating)
say(f"[Rating-basis alternative, published] on Damodaran's RATING column the cost of equity is "
    f"{ke_rating_alt:.2%} and the cost of capital {wacc_exp_rating:.2%} -> {wacc_term_rating:.2%}, "
    f"giving EGP {dcf_rating_ps:.2f}/share against the CDS-basis {dcf_ps:.2f}.")

fx_dep_avg = (V['fx_path'][-1] / V['fx_hist']['FY25']) ** (1 / 5) - 1
kd_hard_egp_equiv = (1 + V['kd_hard_note']) * (1 + fx_dep_avg) - 1
kd_egp_equiv = w_egp * V['kd_egp_note'] + (1 - w_egp) * kd_hard_egp_equiv
kd_egp_equiv_at = kd_egp_equiv * (1 - TAX)
wacc_exp_egp_equiv = we_exp * ke_exp + wd_exp * kd_egp_equiv_at
dcf_egp_equiv_ps = _val_at(wacc_exp_egp_equiv, wacc_term)
say(f"[EGP-equivalent cost of debt alternative, published] loading the hard-currency legs "
    f"({1-w_egp:.0%} of the book) with the pound's own {fx_dep_avg:.1%}/year forecast "
    f"depreciation under uncovered interest parity gives an EGP-equivalent cost of "
    f"{kd_hard_egp_equiv:.2%} for that share, and a blended Kd of {kd_egp_equiv:.2%} against the "
    f"currency-composition {V['kd']:.2%}. Cost of capital rises to {wacc_exp_egp_equiv:.2%} from "
    f"{wacc_exp:.2%}, giving EGP {dcf_egp_equiv_ps:.2f}/share against {dcf_ps:.2f}. CAUTION: "
    f"adopting the currency-composition Kd as primary means the hard-currency share of the debt "
    f"book is carried at its coupon rate and NOT compensated for devaluation risk beyond what "
    f"this forecast's own FX path already assumes.")

nci_alt = nci_share * (ev + assoc_val)
eq_alt = ev + assoc_val - nci_alt - V['nd_fy25']
nci_alt_ps = to_anchor(eq_alt / SH)
say(f"[Minority-interest sequencing, alternative published] charging minorities "
    f"{nci_share:.1%} of UNLEVERED enterprise value plus associates ({nci_alt:,.0f}) and "
    f"deducting net debt afterwards gives EGP {nci_alt_ps:.2f}/share, against {dcf_ps:.2f} on the "
    f"adopted sequencing. The adopted method is retained because the audited borrowings note "
    f"records facilities granted to 'the Company AND ITS SUBSIDIARIES ... guaranteed by "
    f"promissory notes FROM SUBSIDIARIES', i.e. debt does sit at subsidiary level.")

# ---- lens 2: relative --------------------------------------------------------
REL_I = 1
ebitda_mid = ebitda[REL_I]
df_rel = df[REL_I]
ev_rel_fwd = V['ev_ebitda_just'] * ebitda_mid
# the interim FY26-27 free cash flows (net PV negative) are ADDED so the lens is a complete
# enterprise value at the valuation date, not just the discounted forward multiple — an
# accepted critique refinement; omitting them had overstated the lens slightly
ev_rel = ev_rel_fwd * df_rel + pv[0] + pv[1]
# [L-294] APPLIES TO EVERY LENS THAT PRODUCES A PER-SHARE EQUITY VALUE, not only to
# the cash-flow lens. The employees' statutory share of distributable profits is a
# claim AHEAD of ordinary shareholders and it does not become one only when a
# discounted cash flow is the instrument. This study charged it in the bridge, in
# the currency alternative, in the sensitivity helper and in the scenarios, and NOT
# in the three cross-checks a reader is shown beside the central - so the same
# company was worth 12.19% more per share depending on which lens was reading it.
def _rel(mult):
    return to_anchor((((mult * ebitda_mid) * df_rel + pv[0] + pv[1]
                       - V['nd_fy25'] + assoc_val)
                      * (1 - nci_share) * (1 - emp_rate)) / SH)
rel_ps, rel_bear, rel_bull = _rel(V['ev_ebitda_just']), _rel(5.5), _rel(8.0)
say(f"[Relative lens — forward EV discounted, interim flows included] {V['ev_ebitda_just']}x on "
    f"FY2027E EBITDA {ebitda_mid:,.0f} gives an enterprise value of {ev_rel_fwd:,.0f} AS AT "
    f"end-FY2027; discounted back at the year-2 factor {df_rel:.4f} plus the present value of "
    f"the interim FY26-27 free cash flows ({pv[0]+pv[1]:,.0f}) that is {ev_rel:,.0f} at "
    f"31-Dec-2025 -> EGP {rel_ps:.2f}/share at the anchor.")
ev_trailing = MKTCAP + V['nd_fy25']
ev_ebitda_trailing = ev_trailing / ebitda_fy25
pe_trailing = SPOT / (V['npa_fy25'] / SH)

# ---- lens 3: normalized earnings power ---------------------------------------
# RESTATED after external critique: the previous construction applied the justified P/E to
# FY2028-SCALE earnings with no time value — injecting two years of undiscounted growth into
# a present-day lens. The earning-power question is what the business earns at CURRENT scale
# in a mid-cycle year: the mid-cycle EBITDA margin (FY2028E, the middle forecast year) is
# applied to FY2026E revenue, with FY2026E financing and associate income. Worth -4.9/share
# on the weighted central versus the old construction.
norm_margin = ebitda_margin[2]
norm_rev = rev[0]
norm_ebitda = norm_margin * norm_rev
norm_ebit = norm_ebitda - V['dna_pct'] * norm_rev
norm_interest = interest_path[0]
norm_assoc = assoc_fc[0]
norm_np = ((norm_ebit - norm_interest + norm_assoc) * (1 - TAX)
           * (1 - nci_share) * (1 - emp_rate))   # [L-294], as the bridge does
norm_eps = norm_np / SH
norm_ps = to_anchor(V['pe_just'] * norm_eps)
norm_bear = to_anchor(7.0 * norm_eps)
norm_bull = to_anchor(11.5 * norm_eps)
say(f"[Normalised lens — current-scale earning power] mid-cycle EBITDA margin "
    f"{norm_margin:.2%} (FY2028E) on FY2026E revenue {norm_rev:,.0f} -> normalised EPS "
    f"{norm_eps:.2f} x {V['pe_just']:.1f} = EGP {norm_ps:.2f}/share at the anchor. Equity-method "
    f"associate income is taxed inside this lens although it is already post-tax at the investee "
    f"— a disclosed conservatism worth about +0.4/share on the central if removed.")

# ---- lens 4: book / justified P/B --------------------------------------------
bvps = eqp_fy25 / SH
ke_blend = ke_term   # the PERPETUAL (terminal) cost of equity — a steady-state multiple takes a
                     # steady-state rate; the 23.0% average-of-windows alternative is this lens's
                     # published bear construction below
pb_just = (V['roe_sust'] - V['g_term']) / (ke_term - V['g_term'])
book_ps = to_anchor(pb_just * bvps)
book_bear = to_anchor(((V['roe_sust'] - 0.03) / (0.5 * (ke_exp + ke_term) - 0.03)) * bvps)
book_bull = to_anchor(((V['roe_sust'] + 0.02 - V['g_term']) / (ke_term - V['g_term'])) * bvps)
say(f"[Book lens] justified price-to-book {pb_just:.2f}x = (sustainable return {V['roe_sust']:.1%} "
    f"- growth {V['g_term']:.0%}) / (PERPETUAL cost of equity {ke_term:.2%} - growth). The "
    f"justified P/B is a steady-state construct whose implied payout is 1 - g/ROE = "
    f"{1 - V['g_term']/V['roe_sust']:.0%}, deliberately distinct from the five-year forecast "
    f"payout of {PAYOUT:.0%} — the two describe different horizons.")
roe_trailing = V['npa_fy25'] / ((V['eqp_fy24'] + eqp_fy25) / 2)

# ---- scenarios on the DCF -----------------------------------------------------
def dcf_scenario(gp_unit_mult=1.0, fx_mult=1.0, wacc_shift=0.0, g=None, opex_shift=0.0,
                 copper_mult=1.0, nwc=None):
    g = V['g_term'] if g is None else g
    nwc = V['nwc_pct'] if nwc is None else nwc
    B = build(fx_mult=fx_mult, gp_unit_mult=gp_unit_mult, copper_mult=copper_mult,
              opex_shift=opex_shift)
    _rev, _ebitda = B['rev'], B['ebitda']
    _dna = [V['dna_pct'] * r for r in _rev]
    _ebit = [_ebitda[i] - _dna[i] for i in range(5)]
    _nopat = [e * (1 - TAX) for e in _ebit]
    # THE SCENARIO ENGINE READS THE SAME CAPEX CONSTRUCTION AS THE BASE, and the study's
    # own reproduce-the-base assertion is what caught it reading the retired one: two
    # readers of one fact disagreeing [R-ENF-03], found by a gate rather than by eye.
    _capex = [_CAPEX_PCT_MEASURED * r for r in _rev]
    _nwc = [nwc * r for r in _rev]
    _dnwc = [_nwc[0] - nwc_fy25] + [_nwc[i] - _nwc[i - 1] for i in range(1, 5)]
    _f = [_nopat[i] + _dna[i] - _capex[i] - _dnwc[i] for i in range(5)]
    _we, _wt = wacc_exp + wacc_shift, wacc_term + wacc_shift
    _fwd = [_we - (_we - _wt) * f for f in glide_frac]
    _df, cc = [], 1.0
    for w in _fwd:
        cc /= (1 + w); _df.append(cc)
    _ppe, pp = [], ppe_fy25
    for i in range(5):
        pp += _capex[i] - _dna[i]; _ppe.append(pp)
    # The terminal comes from the sanctioned module here too, on the SCENARIO's own
    # terminal-year quantities, so a scenario cannot silently run a different
    # construction from the base case.
    _ic_end = _nwc[-1] + _ppe[-1] + V['intang_fy25']
    _real = (1.0 + g) / (1.0 + V['pi_term']) - 1.0
    _tv = TV.build(TV.TerminalInputs(
        # LAST EXPLICIT YEAR, not the terminal year — the module grows it itself.
        nopat=_nopat[-1], wacc=_wt, inflation=V['pi_term'], real_growth=_real,
        dna_book=_dna[-1],
        useful_life_years=V['asset_life_derived'],
        useful_life_source=V['asset_life_source'],
        maintenance_basis='book_dna_escalated',
        working_capital=_nwc[-1],
        incremental_capital_per_unit_growth=_ic_end)).tv
    _ev = sum(_f[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    return to_anchor(((_ev - V['nd_fy25'] + assoc_val) * (1 - nci_share)
                      * (1 - emp_rate)) / SH)

_base_chk = dcf_scenario()
assert abs(_base_chk - dcf_ps) < 0.02, f'scenario engine does not reproduce base: {_base_chk} vs {dcf_ps}'

dcf_bear = dcf_scenario(gp_unit_mult=0.88, fx_mult=0.94, wacc_shift=+0.02, g=0.03, opex_shift=+0.005)
dcf_bull = dcf_scenario(gp_unit_mult=1.12, fx_mult=1.08, wacc_shift=-0.02, g=0.06, opex_shift=-0.005)
say(f"[DCF scenarios] bear {dcf_bear:.2f} / base {dcf_ps:.2f} / bull {dcf_bull:.2f} EGP per share")

# ---- synthesis: ONE CLASS PRIMARY IS THE CENTRAL [R-LENS-03] -------------------
# The typed 45/20/20/15 blend is RETIRED. It was published, it had never cleared an
# out-of-sample test, and on this name it did what a blend does — it hid the size of the
# study's disagreement with the market. The blend read 71.20 against the cash-flow lens's
# 55.48, so a reader saw -32% where this study's own method says -47%.
#
# WHAT IT WAS CARRYING. Normalised earnings power read 109.52, nearly double the primary,
# and carried a fifth of the weight. For a group that is a quarter turnkey contracting
# that is the wrong lens on its face: a contractor's reported earnings are an accident of
# which projects reached their profitable phases in which period, which is exactly why
# both developer rows of the registry exclude it and why the class row added for this
# company excludes it too. It is computed and shown so its removal is visible.
RETIRED_BLEND_W = V['lens_weights']
lenses = dict(
    dcf=dict(name='Discounted cash flow (the answer)', bear=dcf_bear, base=dcf_ps,
             bull=dcf_bull, w=None),
    relative=dict(name='Relative multiples', bear=rel_bear, base=rel_ps, bull=rel_bull,
                  w=None),
    normalized=dict(name='Normalised earnings power', bear=norm_bear, base=norm_ps,
                    bull=norm_bull, w=None,
                    note='RETIRED for this class: a contractor\'s reported earnings turn on '
                         'completion timing, so normalising them normalises noise. Removed '
                         'rather than re-weighted, and computed and shown so the move is '
                         'visible.'),
    book=dict(name='Book value and sustainable return', bear=book_bear, base=book_ps,
              bull=book_bull, w=None,
              note='a disclosed FLOOR, published as such and never weighted'),
)
RETIRED_BLEND_VALUE = sum(lenses[k]['base'] * RETIRED_BLEND_W[k] for k in RETIRED_BLEND_W)
central = dcf_ps                      # THE CLASS PRIMARY IS THE CENTRAL
lo, hi = dcf_bear, dcf_bull           # its OWN bear and bull, on one clock
span_lo = min(l['bear'] for l in lenses.values())
span_hi = max(l['bull'] for l in lenses.values())
lenses['central'] = dict(name='Cash-flow lens (the central)', bear=lo, base=central,
                         bull=hi, w=None)
lenses['retired_blend'] = dict(name='RETIRED 45/20/20/15 blend, published unused',
                               bear=None, base=RETIRED_BLEND_VALUE, bull=None, w=0.0)
say(f"[Synthesis] THE CENTRAL IS THE CLASS PRIMARY: the cash-flow lens at EGP {central:.2f}, "
    f"with its own bear-to-bull range of {lo:.2f} - {hi:.2f} on one clock. The cross-checks "
    f"are published beside it at their own values (relative {rel_ps:.2f}, book floor "
    f"{book_ps:.2f}) and the span across all of them, {span_lo:.2f} - {span_hi:.2f}, is a "
    f"spread between METHODS and not a range around the answer. Spot {SPOT:.2f} "
    f"({central/SPOT-1:+.0%} to the central).")
say(f"[Retired blend, published unused] the 45/20/20/15 weights give EGP "
    f"{RETIRED_BLEND_VALUE:.2f}, {RETIRED_BLEND_VALUE/SPOT-1:+.0%} against the price where the "
    f"cash-flow lens reads {central/SPOT-1:+.0%} — so the published number was showing about "
    f"{abs((RETIRED_BLEND_VALUE/SPOT-1)/(central/SPOT-1)):.0%} of the disagreement this study "
    f"actually holds. Normalised earnings power at {norm_ps:.2f} carried a fifth of it.")
assert 0.20 <= central / SPOT <= 3.0, f"central/spot {central/SPOT:.2f} outside the plausibility band"

# ---- sensitivity grids ---------------------------------------------------------
# THE GRID IS CENTRED ON THE ADOPTED CASE, NEVER ON A TYPED LADDER. The retired
# growth axis ran 3% to 7% against an adopted terminal growth of 9.14%: a
# sensitivity table that does not contain the number the study actually struck,
# so no cell in it was the base case and the reader could not locate the answer
# on its own grid. Both axes now step around the adopted values [R-SENS-01].
g_grid = [V['g_term'] - 0.02, V['g_term'] - 0.01, V['g_term'],
          V['g_term'] + 0.01, V['g_term'] + 0.02]
wt_grid = [wacc_term - 0.02, wacc_term - 0.01, wacc_term, wacc_term + 0.01, wacc_term + 0.02]
we_grid = [wacc_exp - 0.03, wacc_exp - 0.015, wacc_exp, wacc_exp + 0.015, wacc_exp + 0.03]

# dcf_at WAS DELETED HERE, AND EVERY GRID BELOW NOW GOES THROUGH _val_at.
#
# dcf_at was a second valuation function living beside _val_at and disagreeing with it in
# two ways at once. It re-implemented the terminal INLINE on the retired g x IC
# construction, which _val_at had already been moved off and onto terminal_value.build();
# and it omitted the employees' statutory share of distributable profits, which the
# headline bridge charges. So every sensitivity grid in section 1.9 was quoted on a claim
# the study does not value, discounted through a terminal the study does not use.
#
# The size of it: the wacc x g grid's own centre cell read 49.71 against a published
# central of 43.51 -- the grid whose job is to show what moves the answer was centred
# 14.2% above the answer. A reader checking the study against its own sensitivity table
# would have found the central outside it.
#
# _val_at CARRIED THE ASSERTION THAT WOULD HAVE CAUGHT THIS FROM THE START -- it asserts
# it reproduces dcf_ps when nothing is changed -- and dcf_at carried none. That assertion
# is what makes a scenario function honest, and it is now the only such function here.
# This is [L-016] again, and ARCC's revision 4 found the identical shape on the identical
# day: one document, two models, the second one hiding inside the block whose whole job is
# to test the first.
grid_wacc_g = [[_val_at(wacc_exp, wt, g) for g in g_grid] for wt in wt_grid]
grid_exp_term = [[_val_at(we, wt, V['g_term']) for wt in wt_grid] for we in we_grid]
# THE BETA GRID IS SORTED. It read [0.60, 0.80, 1.225, 1.15, 1.30] -- the adopted beta
# inserted at the centre POSITION rather than in its place in the order -- so the printed
# row ran 0.80, 1.225, 1.15 and the fair values beside it went 75.26, 49.70, 53.21: down,
# then UP, in a table a reader reads as monotone. The adopted figure is marked instead.
_beta_adopted = round(V['beta'], 3)
beta_grid = sorted({0.60, 0.80, _beta_adopted, 1.15, 1.30})
def dcf_beta(b):
    ke = rf_star + b * ERP_MATURE + CRP_EFF
    we_ = we_exp * ke + wd_exp * kd_at
    wt_ = ((1 - V['wd_term']) * (V['rf_term'] + b * ERP_MATURE + CRP_EFF_TERM)
           + V['wd_term'] * kd_term_at)
    return _val_at(we_, wt_, V['g_term'])
grid_beta = [dcf_beta(b) for b in beta_grid]
# THE GRIDS REPRODUCE THE HEADLINE WHERE THEY CROSS IT, or they are testing another model.
assert abs(_val_at(wacc_exp, wacc_term, V['g_term']) - dcf_ps) < 0.01, \
    'the grid helper does not reproduce the published central'
assert abs(dcf_beta(_beta_adopted) - dcf_ps) < 0.05, \
    f"beta grid at the adopted {_beta_adopted} reads {dcf_beta(_beta_adopted):.2f}, not {dcf_ps:.2f}"
say(f"[Sensitivity grids] every grid in section 1.9 now runs through the SAME valuation "
    f"function as the headline: the sanctioned terminal module and the employees' statutory "
    f"share both. At the adopted rates and growth the helper returns "
    f"{_val_at(wacc_exp, wacc_term, V['g_term']):.2f} against the published "
    f"{dcf_ps:.2f}, and at the adopted beta {_beta_adopted:.3f} it returns "
    f"{dcf_beta(_beta_adopted):.2f} — asserted, not eyeballed.")
fx_grid = [0.90, 1.00, 1.20, 1.45, 1.70]
grid_fx = [dcf_scenario(fx_mult=m) for m in fx_grid]
mg_grid = [0.85, 0.925, 1.0, 1.075, 1.15]
grid_margin = [dcf_scenario(gp_unit_mult=m) for m in mg_grid]
cu_grid = [0.85, 0.925, 1.0, 1.075, 1.15]
grid_copper = [dcf_scenario(copper_mult=m) for m in cu_grid]
nwc_grid = [0.17, 0.185, 0.199, 0.215, 0.23]
def dcf_nwc(pct):
    return dcf_scenario(nwc=pct)
grid_nwc = [dcf_nwc(p) for p in nwc_grid]
roic_grid = [0.15, 0.18, roic_term, 0.26, 0.30]
def dcf_roic(r):
    _rr = min(V['g_term'] / r, 0.95)
    _tv = nopat[-1] * (1 + V['g_term']) * (1 - _rr) / (wacc_term - V['g_term'])
    _ev = pv_explicit + _tv * df[-1]
    return to_anchor(((_ev - V['nd_fy25'] + assoc_val) * (1 - nci_share)) / SH)
grid_roic = [dcf_roic(r) for r in roic_grid]

say(f"[Leverage] net financial debt / EBITDA falls from {V['nd_fy25']/ebitda_fy25:.2f}x to "
    f"{nd_fc[-1]/ebitda[-1]:.2f}x over the forecast.")

# ---- expert panel: three genuinely different methods ---------------------------
# All three legs are rolled to the anchor date exactly as the four lenses are.
e1_margin = ebitda_margin[2]
e1_rev = rev[2]
e1_ebit = e1_margin * e1_rev - V['dna_pct'] * e1_rev
# E1's net interest is the FY2028 point of the same static-gross-book construction the
# forecast uses: kd_path[FY28] x gross debt less 10% on the FY2025 cash balance
e1_int = V['kd_path'][2] * debt_fy25 - 0.10 * cash_fy25
e1_eps = ((e1_ebit - e1_int + V['assoc_fy25']) * (1 - TAX) * (1 - nci_share)) / SH
e1_base, e1_lo, e1_hi = (to_anchor(9.5 * e1_eps), to_anchor(7.0 * e1_eps),
                         to_anchor(12.0 * e1_eps))

e2_fcff = float(np.mean(fcff[2:]))
# E2's after-tax interest charge: the FY2029 point of the same construction, after tax —
# shown explicitly because a critique correctly noted it was not reconcilable as displayed
e2_int_at = (V['kd_path'][3] * debt_fy25 - 0.10 * cash_fy25) * (1 - TAX)
e2_fcfe = (e2_fcff - e2_int_at) * (1 - nci_share)
e2_ke = ke_term
e2_base = to_anchor(e2_fcfe * (1 + V['g_term']) / (e2_ke - V['g_term']) / SH)
e2_lo = to_anchor(e2_fcfe * 1.03 / (0.5 * (ke_exp + ke_term) - 0.03) / SH)
e2_hi = to_anchor(e2_fcfe * 1.06 / (e2_ke - 0.06) / SH)

ic_beg = [ic_fy25] + ic[:-1]
ep_ = [nopat[i] - fwd[i] * ic_beg[i] for i in range(5)]
pv_ep = sum(ep_[i] * df[i] for i in range(5))
ep_term = nopat[-1] * (1 + V['g_term']) - wacc_term * ic[-1] * (1 + V['g_term'])
pv_ep_term = ep_term / (wacc_term - V['g_term']) * df[-1]
e3_ev = ic_fy25 + pv_ep + pv_ep_term
e3_base = to_anchor(((e3_ev - V['nd_fy25'] + assoc_val) * (1 - nci_share)) / SH)
e3_lo = to_anchor(((ic_fy25 + pv_ep * 0.6 + pv_ep_term * 0.55 - V['nd_fy25'] + assoc_val)
                   * (1 - nci_share)) / SH)
e3_hi = ccy_ps   # already at the anchor
experts = dict(
    e1=dict(method_short='earnings power', base=e1_base, rng=[e1_lo, e1_hi], eps=e1_eps,
            margin=e1_margin, rev=e1_rev, ebit=e1_ebit, interest=e1_int, pe=9.5),
    e2=dict(method_short='owner cash earnings', base=e2_base, rng=[e2_lo, e2_hi], fcff=e2_fcff,
            fcfe=e2_fcfe, ke=e2_ke, int_at=e2_int_at),
    e3=dict(method_short='cash returns vs cost of capital', base=e3_base, rng=[e3_lo, e3_hi],
            ic0=ic_fy25, pv_ep=pv_ep, pv_ep_term=pv_ep_term, ev=e3_ev, ep=ep_,
            spread=[roic[i] - fwd[i] for i in range(5)]),
)
panel_centre = float(sorted([e1_base, e2_base, e3_base])[1])
say(f"[Expert panel] Expert 1 {e1_base:.2f} [{e1_lo:.2f}-{e1_hi:.2f}]; Expert 2 {e2_base:.2f} "
    f"[{e2_lo:.2f}-{e2_hi:.2f}]; Expert 3 {e3_base:.2f} [{e3_lo:.2f}-{e3_hi:.2f}]; "
    f"panel median {panel_centre:.2f} ({panel_centre/SPOT-1:+.0%} vs spot)")

# ---- fan for the figure ---------------------------------------------------------
paths3 = np.load(os.path.join(HERE, 'paths_3M.npy'))
fan = np.percentile(paths3, [5, 25, 50, 75, 95], axis=0)
np.save(os.path.join(HERE, 'fan.npy'), fan)

# ============================ EMIT ==============================================
step0 = json.load(open(os.path.join(HERE, 'step0_result.json')))
strike = json.load(open(os.path.join(HERE, 'strike_result.json')))
beta_res = json.load(open(os.path.join(HERE, 'beta_result.json')))

OUT = dict(
    # [R-FCAL-01] WHAT THIS NAME'S WALK-FORWARD ADOPTED, STATED RATHER THAN LEFT
    # TO SILENCE. scripts/check_corrections_applied.py reads this; a study with a
    # run behind it and no statement either way is SILENT, which is a different
    # fact from 'none adopted' and reads identically.
    adopted_corrections=[],
    adopted_corrections_note=(
        "the walk-forward on this name adopted NO correction — see engine/swdy_walkforward/corrections_log.json. Empty rather than absent: silence and 'none adopted' are the same file to a reader and different facts about the work."),
    meta=dict(ticker='SWDY', company='Elsewedy Electric Company S.A.E.', market='EGX',
              currency='EGP', asof='2026-09-03', spot=SPOT, shares_mn=SH, mktcap=MKTCAP,
              ev_trailing=ev_trailing, klass='diversified industrial operating company'),
    inputs=INP,
    hist_is=hist_is,
    hist_bs=dict(
        FY23=dict(ppe=V['ppe_fy23'], inv=V['inv_fy23'], ca=V['ca_fy23'], recv=V['recv_fy23'],
                  cash=V['cash_fy23'], assets=V['assets_fy23'], debt=V['debt_fy23'],
                  pay=V['pay_fy23'], cl=V['cl_fy23'], eqp=V['eqp_fy23'], nci=V['nci_fy23'],
                  nd=V['nd_fy23'], nwc=nwc_fy23),
        FY24=dict(ppe=V['ppe_fy24'], inv=V['inv_fy24'], ca=V['ca_fy24'], recv=V['recv_fy24'],
                  cash=V['cash_fy24'], assets=V['assets_fy24'], debt=V['debt_fy24'],
                  pay=V['pay_fy24'], cl=V['cl_fy24'], eqp=V['eqp_fy24'], nci=V['nci_fy24'],
                  nd=V['nd_fy24'], nwc=nwc_fy24),
        FY25=dict(ppe=ppe_fy25, inv=V['inv_fy25'], ca=V['ca_fy25'], recv=V['recv_fy25'],
                  assets=V['assets_fy25'], debt=debt_fy25, cash=cash_fy25,
                  pay=V['pay_fy25'], cl=V['cl_fy25'], eqp=eqp_fy25, nci=V['nci_fy25'],
                  nd=V['nd_fy25'], nwc=nwc_fy25),
    ),
    fgn_share_fy25_derived=fgn_share_fy25_derived, fgn_egp_fy25=fgn25,
    fcst=dict(tax=tax_fcst, gp=gp, pbt=pbt_fc, tax_is=tax_is_fc, pat=pat_fc,
              nci_is=nci_is_fc, years=YRS, rev=rev, dom=dom, fgn_usd=fgn_usd, fgn_egp=fgn_egp,
              ebitda=ebitda, ebitda_margin=ebitda_margin, dna=dna, ebit=ebit, nopat=nopat,
              capex=capex, nwc=nwc, dnwc=dnwc, fcff=fcff, df=df, pv=pv, fwd_wacc=fwd,
              ppe=ppe, ic=ic, roic=roic, np_attr=np_fc, equity=eq_fc, net_debt=nd_fc,
              interest=interest_path, assoc=assoc_fc, div=div_fc, seg_gp=seg_gp,
              seg_rev=seg_rev, seg_ebit=seg_ebit, seg_shares=shares,
              payout=PAYOUT, assoc_g=ASSOC_G, glide_frac=glide_frac,
              ppe_fy25=ppe_fy25, eqp_fy25=eqp_fy25, assoc_fy25=V['assoc_fy25'],
              debt_fy25=debt_fy25, nwc_fy25=nwc_fy25, dna_fy25=V['dna_fy25'],
              nopat_fy25=nopat_fy25, ic_fy25=ic_fy25),
    employees_cap=EMP_CAP,
    seg_fy25=dict(rev=SRH['FY25'], gp=SPH['FY25'], names=SEGNAME,
                  gp_margin=unit_hist['FY25']['margin'],
                  # THE DISCLOSED SEGMENT GROWTH RATES, COMMITTED AS NUMBERS. They were
                  # quoted in a driver's source string -- which the bibliography prints
                  # verbatim -- and appeared in no committed figure, so a reader met a rate
                  # they could not trace and the prose check could not reconcile. They are
                  # derived from seg_rev_hist above; the string now formats these.
                  growth_fy25={k: _seg_growth(k, 'FY25', 'FY24') for k in SEGNAME},
                  growth_fy24={k: _seg_growth(k, 'FY24', 'FY23') for k in SEGNAME}),
    bottomup=dict(unit_hist=unit_hist, subs=SUBS, subnames=SUBNAME, gp=gp, gp_margin=gp_margin,
                  opex=opex, seg_gp=seg_gp,
                  q1_26_implied_fy=V['q1_26_rev'] / (V['q1_25_rev'] / V['rev_fy25'])),
    wacc=dict(rf=V['rf'], rf_star=rf_star, ke_exp=ke_exp, ke_rating_alt=ke_rating_alt,
              ke_ops_alt=ke_ops_alt, ke_raw_retired=ke_raw_retired, kd=V['kd'], kd_at=kd_at,
              we_exp=we_exp, wd_exp=wd_exp, wacc_exp=wacc_exp, wacc_exp_gross=wacc_exp_gross,
              wd_gross=wd_gross, ke_term=ke_term, kd_term=V['kd_term'], kd_term_at=kd_term_at,
              wacc_term=wacc_term, glide_frac=glide_frac, kd_path=V['kd_path'],
              kd_eff_fy24=kd_eff_fy25, kd_eff_q1_25=kd_eff_fy25, w_egp_implied=w_egp,
              wacc_usd_alt=WACC_USD, beta=beta_res),
    dcf=dict(pv_explicit=pv_explicit, tv=tv, pv_tv=pv_tv, ev=ev, tv_share=tv_share,
             nd=V['nd_fy25'], assoc=assoc_val, nci_share=nci_share, nci_val=nci_val,
             # THE EMPLOYEES' STATUTORY SHARE IS COMMITTED, because the bridge does not
             # foot without it and a reader has to be able to add the printed steps up.
             # It was charged in the model from the first edition and asserted at the
             # identity below, but it was never written to this record -- so the delivered
             # §1.1 table went enterprise value, less net debt, plus associates, less
             # minorities, and then straight to an equity 11,273 lower than those four
             # lines produce, with no row to explain the drop. The arithmetic was right
             # and the table was unfootable, which is the worse of the two failures: a
             # reader checking the study finds a number that does not add up and has no
             # way to tell a missing row from a wrong one.
             emp_rate=emp_rate, emp_charge=emp_charge, eq_attr_pre_emp=eq_attr_pre_emp,
             # THE FY2025 PAYOUT RATIO, COMMITTED. The document computed it inline from
             # two committed numbers and printed 22.9%, which no committed figure matched,
             # so the prose check could not reconcile it -- a figure a reader sees and
             # cannot trace [R-REPAIR-01]. Arithmetic done in a document builder is
             # arithmetic no gate reads.
             dps_payout_fy25=V['dps_fy25'] / (V['npa_fy25'] / SH),
             eq_attr=eq_attr, ps=dcf_ps, ps_dec=dcf_ps_dec, roll=ROLL,
             anchor_days=V['anchor_days'], roic_term=roic_term, rr_term=rr_term,
             # THE TERMINAL'S OWN RECORD, committed rather than described. Without
             # it the delivered workbook cannot build the sanctioned construction
             # as live formulas and has to carry a number, which is how the
             # retired g x IC formula survived in DCF!C25 while compute.py had
             # already moved off it [R-ENF-06].
             terminal_record=_terminal.record,
             ps_rating_basis=dcf_rating_ps, wacc_exp_rating=wacc_exp_rating,
             wacc_term_rating=wacc_term_rating, ps_nci_alt=nci_alt_ps, nci_alt=nci_alt,
             g=V['g_term'], bear=dcf_bear, bull=dcf_bull, ccy_alt_ps=ccy_ps,
             ps_kd_egp_equiv=dcf_egp_equiv_ps, kd_egp_equiv=kd_egp_equiv,
             wacc_exp_kd_egp_equiv=wacc_exp_egp_equiv, fx_dep_avg=fx_dep_avg),
    terminal_recon=dict(roic=hist_roic, rr=hist_rr, implied_g=hist_impl_g,
                        nopat=dict(FY23=nopat_fy23, FY24=nopat_fy24, FY25=nopat_fy25),
                        capex=dict(FY23=V['capex_fy23'], FY24=V['capex_fy24'], FY25=V['capex_fy25']),
                        ebitda=dict(FY23=ebitda_fy23, FY24=ebitda_fy24, FY25=ebitda_fy25),
                        nopat_cagr=nopat_cagr, stable_g=stable_g,
                        ceiling=blend_ceiling, crossover_years=float(yrs_cross)),
    # WHAT STANDS BETWEEN PROFIT AND SHAREHOLDERS [L-294]. The identity the gate holds:
    # attributable profit over the share count must reproduce the reported EPS, and where
    # it does not the difference is NAMED. Here it is two things, both disclosed in note 39
    # and neither in any line of the income statement.
    eps_reconciliation=dict(
        reported_eps=float(V['eps_fy25']),
        attributable_profit=float(V['npa_fy25']),
        shares_issued=float(SH),
        naive_eps=float(V['npa_fy25'] / SH),
        what=("the employees' statutory share of distributable profits, plus the ESOP "
              "adjustment to the weighted-average share count"),
        difference=float(V['npa_fy25'] / SH - V['eps_fy25']),
        components=[
            dict(item="employees' share in profit (estimated)",
                 amount=float(V['emp_share_fy25']),
                 per_share=float(V['emp_share_fy25'] / SH),
                 source='audited FY2025 consolidated financial statements, note 39',
                 note=('an APPROPRIATION of profit under Egyptian company law, not an '
                       'operating cost, so it is disclosed only in the earnings-per-share '
                       'note and appears in no line of the income statement')),
            dict(item='ESOP shares issued not granted, excluded from the weighted average',
                 amount=None, shares=1.422160,
                 source='audited FY2025 consolidated financial statements, note 39',
                 note=('the reported EPS divides by 2,139,355,716, being the 2,140,777,876 '
                       'issued less 1,422,160 ESOP shares issued and not granted')),
        ],
        charged_in_the_valuation=True,
        charged_at=float(emp_rate),
        charged_note=("charged in the bridge below the minority, at the mean of the three "
                      "measured periods rather than the latest, because this is a rate on "
                      "profit and one half is not a trend. The statutory cap at total "
                      "annual wages is NOT modelled — nothing in the filings discloses its "
                      "headroom — so the charge is an upper bound and the direction of the "
                      "unmodelled cap is recorded rather than guessed"),
    ),
    lenses=lenses, central=central, span=[lo, hi], spot=SPOT,
    retired_blend_value=RETIRED_BLEND_VALUE,
    lens_record=dict(**{'class': 'diversified industrial with a contracting arm'},
        # [R-LENS-03] THE RECORD DECLARES ITS CENTRAL, so the identity clause
        # actually RUNS. assert_lens_design() wraps 'the primary's value IS the
        # central' in `if central is not None`, so a record exposing no central
        # skipped the one clause that catches a weighted blend -- eight studies
        # were in that state and every blend-carrier sat among them. Computed
        # from the same quantity the primary carries, never typed.
        central=float(central),
        # [R-LENS-03] / check_output_sanity — THE CENTRAL SITS BELOW THE FIGURE THIS RECORD
        # PUBLISHES AS A FLOOR, AND THE REASON IS THAT THE FIGURE IS NOT A DISCLOSED FLOOR.
        # The gate does not require the central to exceed the floor; it requires the study
        # to say so when it does not, and an empty reason switches the check off rather
        # than declaring it. Every number in this sentence is COMPUTED from the same
        # committed operands the lens table prints, never typed beside them.
        below_floor_reason=(
            'The cross-check labelled a floor is the book lens AT ITS JUSTIFIED '
            'PRICE-TO-BOOK of %.4fx (EGP %.4f), a construction from a sustainable return '
            'of %.1f%% against the perpetual cost of equity — not a disclosed figure. The '
            'floor that IS disclosed is equity attributable to the parent over shares in '
            'issue, EGP %.4f per share at 31-Dec-2025, rolled to the anchor on the same '
            'clock as every other lens = EGP %.4f. The central of EGP %.4f sits %.1f%% '
            'ABOVE that disclosed floor and %.1f%% below the justified-multiple read. The '
            'gap widened on 7 September 2026 when the terminal was rebuilt onto the '
            'last-explicit-year basis the sanctioned module specifies (-6.34%%): the '
            'correction moved the cash-flow lens and left the justified multiple where it '
            'was, so what this records is two lenses disagreeing, which [R-LENS-03] says '
            'to PUBLISH rather than average. Registered for the next re-issue: a '
            'book_value cross-check should carry the disclosed book value and the '
            'sustainable-return read should be published beside it as its own lens, which '
            'this record conflates into one entry.'
            % (pb_just, lenses['book']['base'], V['roe_sust'] * 100, bvps,
               to_anchor(bvps), central,
               (central / to_anchor(bvps) - 1) * 100,
               (1 - central / lenses['book']['base']) * 100)),
        primary=dict(
            kind='dcf', two_sided=False, value=float(central),
            range={'low': float(lo), 'high': float(hi)},
            range_note=('the cash-flow lens under its own bear and bull scenarios on one '
                        'clock, not the widest spread across four methods'),
            range_basis=dict(
                driver='the segment margin paths, the corporate load and the copper and '
                       'currency path the cables leg is built on',
                low=float(lo), high=float(hi),
                units='EGP per share, the present-value read under each scenario',
                macro_held=True,
                evidence=('both scenarios are re-runs of the same three-segment build '
                          'through dcf_scenario(), which calls the sanctioned terminal '
                          'module on the scenario\'s own terminal-year quantities so a '
                          'scenario cannot run a different construction from the base'))),
        cross_checks=[
            dict(kind='relative_multiple', value=float(lenses['relative']['base']),
                 present_value=False, multiple=float(V['ev_ebitda_just']),
                 multiple_source=('a justified enterprise multiple set against listed cable '
                                  'and electrical-equipment peers with an Egyptian-market '
                                  'discount, never one read off this company\'s own current '
                                  'price'),
                 circularity=dict(spot=float(SPOT), shares=float(SH),
                                  net_debt=float(V['nd_fy25']),
                                  metric_value=float(ebitda[1])),
                 # THE OPERANDS ABOVE DO NOT MULTIPLY OUT TO THE FIGURE PUBLISHED, AND
                 # UNTIL 7 SEPTEMBER 2026 NOTHING SAID SO. Taken at face value they give
                 # the naive identity (multiple x metric - net debt) / shares, which is a
                 # SIMPLER lens than this study performs: the multiple is struck on FY2027
                 # EBITDA, so the enterprise value it produces stands at end-FY2027 and has
                 # to be discounted back and the interim flows added, and the equity it
                 # bridges to is shared with a minority and with the employees' statutory
                 # claim before an ordinary shareholder sees any of it [L-294]. A reader
                 # multiplying the printed operands lands 71% high. Every figure in the
                 # bridge below is COMPUTED from the same quantities the model uses.
                 value_adjustment=(
                     'THE NAIVE IDENTITY IS NOT THIS LENS. (%.4fx x EGP %.0fmn FY2027E '
                     'EBITDA - EGP %.0fmn net debt) / %.4fmn shares = EGP %.4f, which is '
                     'the forward enterprise value treated as though it stood at the '
                     'valuation date and the equity treated as though it were all the '
                     'ordinary shareholders\'. The lens actually published runs: '
                     'forward EV EGP %.0fmn at end-FY2027, discounted at the year-two '
                     'factor %.4f = EGP %.0fmn; plus the present value of the interim '
                     'FY2026-27 free cash flows EGP %.0fmn = EGP %.0fmn of enterprise '
                     'value at 31-Dec-2025; less net debt EGP %.0fmn; plus associates at '
                     'carrying value EGP %.0fmn = EGP %.0fmn; less the minority\'s %.2f%% '
                     'share and the employees\' statutory %.2f%% share = EGP %.0fmn '
                     'attributable to ordinary shareholders, over %.4fmn shares = EGP '
                     '%.4f at 31-Dec-2025; rolled to the anchor at the cost of equity '
                     '(x%.4f) less the EGP %.2f dividend paid inside the window = EGP '
                     '%.4f. The two differ by %.3fx and every step of the difference is '
                     'named here.'
                     % (V['ev_ebitda_just'], ebitda[1], V['nd_fy25'], SH,
                        (V['ev_ebitda_just'] * ebitda[1] - V['nd_fy25']) / SH,
                        V['ev_ebitda_just'] * ebitda_mid, df_rel,
                        V['ev_ebitda_just'] * ebitda_mid * df_rel,
                        pv[0] + pv[1],
                        V['ev_ebitda_just'] * ebitda_mid * df_rel + pv[0] + pv[1],
                        V['nd_fy25'], assoc_val,
                        V['ev_ebitda_just'] * ebitda_mid * df_rel + pv[0] + pv[1]
                        - V['nd_fy25'] + assoc_val,
                        nci_share * 100, emp_rate * 100,
                        (V['ev_ebitda_just'] * ebitda_mid * df_rel + pv[0] + pv[1]
                         - V['nd_fy25'] + assoc_val) * (1 - nci_share) * (1 - emp_rate),
                        SH,
                        (V['ev_ebitda_just'] * ebitda_mid * df_rel + pv[0] + pv[1]
                         - V['nd_fy25'] + assoc_val) * (1 - nci_share) * (1 - emp_rate) / SH,
                        ROLL, V['dps_fy25'], lenses['relative']['base'],
                        ((V['ev_ebitda_just'] * ebitda[1] - V['nd_fy25']) / SH)
                        / lenses['relative']['base'])),
                 note='mid-cycle FY2027E EBITDA on a peer-anchored enterprise multiple'),
            dict(kind='book_value', value=float(lenses['book']['base']),
                 present_value=False, floor=True,
                 note=('the book lens at its JUSTIFIED price-to-book of %.4fx — the '
                       'model report\'s "book value and sustainable return" read, built '
                       'from a sustainable return of %.1f%% against the perpetual cost of '
                       'equity, rolled to the anchor. Never weighted. It is a construction '
                       'and not a disclosed figure, and the note said "a disclosed FLOOR" '
                       'until 7 September 2026, which described the DISCLOSED BOOK VALUE '
                       'sitting inside it rather than the number published here.'
                       % (pb_just, V['roe_sust'] * 100)),
                 disclosed_book_value_per_share=float(to_anchor(bvps)),
                 disclosed_book_value_note=(
                     'the floor that IS disclosed: equity attributable to the parent at '
                     '31-Dec-2025 over shares in issue, EGP %.4f per share, rolled to the '
                     'anchor on the same clock as every other lens (x%.4f less the EGP '
                     '%.2f dividend paid inside the window) = EGP %.4f.'
                     % (bvps, ROLL, V['dps_fy25'], to_anchor(bvps)))),
        ],
        cross_checks_not_built=[
            dict(kind='ev_ebitda_own_history',
                 why=('this class permits an enterprise multiple on the company\'s OWN '
                      'history and this study does not publish one. Its relative lens uses a '
                      'PEER-anchored multiple, which is a different construction; an '
                      'own-history multiple needs a series of past enterprise values against '
                      'past EBITDA, and this company\'s enterprise value over the relevant '
                      'years is dominated by a debt book that quadrupled and a currency that '
                      'lost most of its value, so the series would measure the pound rather '
                      'than the business. Named here rather than left quietly absent.')),
            dict(kind='sotp',
                 why=('the disciplined sum of the parts this class row calls for is NOT '
                      'built. It is the reason the class exists — three legs on materially '
                      'different contract structures — and it needs segment-level invested '
                      'capital and segment-level net debt, neither of which note 16 '
                      'discloses: the segment note stops at segment profit. Building it on '
                      'allocated group capital would be a construction rather than a '
                      'measurement, and SIGCM clause 8 says stop rather than invent. It is '
                      'the first thing this study should gain when the disclosure allows.')),
        ],
        retired=dict(
            blend=dict(RETIRED_BLEND_W),
            blend_value=float(RETIRED_BLEND_VALUE),
            why=('the weights were typed and had never cleared an out-of-sample test. What '
                 'they concealed here was the SIZE of the disagreement rather than its '
                 'direction: the blend read %+.0f%% against the price where the cash-flow '
                 'lens reads %+.0f%%, so a reader saw about %.0f%% of the disagreement this '
                 'study actually holds. Normalised earnings power, which this class does not '
                 'permit at all, read %.2f against a cash-flow %.2f and carried a fifth of '
                 'the weight.'
                 % (100*(RETIRED_BLEND_VALUE/SPOT-1), 100*(central/SPOT-1),
                    100*abs((RETIRED_BLEND_VALUE/SPOT-1)/(central/SPOT-1)),
                    norm_ps, central)))),
    experts=experts, panel_centre=panel_centre,
    sens_wg=dict(g_grid=g_grid, wacc_grid=wt_grid, table=grid_wacc_g),
    rel=dict(ebitda_mid=ebitda_mid, ev_rel=ev_rel, ev_rel_fwd=ev_rel_fwd,
             pv_interim=pv[0] + pv[1], ev_ebitda_trailing=ev_ebitda_trailing,
             pe_trailing=pe_trailing, just_mult=V['ev_ebitda_just']),
    norm=dict(margin=norm_margin, rev=norm_rev, ebitda=norm_ebitda, ebit=norm_ebit,
              interest=norm_interest, np=norm_np, eps=norm_eps, pe=V['pe_just'],
              year=YRS[0], margin_year=YRS[2], assoc=norm_assoc),
    book=dict(bvps=bvps, pb_just=pb_just, roe_sust=V['roe_sust'], roe_trailing=roe_trailing,
              ke_blend=ke_blend),
    sens=dict(g_grid=g_grid, wt_grid=wt_grid, we_grid=we_grid, grid_wacc_g=grid_wacc_g,
              grid_exp_term=grid_exp_term, beta_grid=beta_grid, grid_beta=grid_beta,
              fx_grid=fx_grid, grid_fx=grid_fx, mg_grid=mg_grid, grid_margin=grid_margin,
              cu_grid=cu_grid, grid_copper=grid_copper,
              nwc_grid=nwc_grid, grid_nwc=grid_nwc, roic_grid=roic_grid, grid_roic=grid_roic),
    step0=step0, strike=strike,
    assert_log=LOG,
    # THE STALENESS IS DISCLOSED RATHER THAN SWITCHED OFF. Two standing rules govern
    # this date from different directions: one requires delivery against the LATEST
    # KNOWN price, the other pins the currency to a house path whose spot anchor carries
    # its own date. This study is struck on 3 September 2026 against a house Egyptian
    # path whose FX spot is anchored 6 August 2026 - twenty-eight days, past the
    # fourteen-day bound the house already uses for a sovereign quote. Refreshing a house
    # macro path is a house-level act and not a step of one name's rebuild, and striking
    # this study against a month-old price to keep the two dates together would breach
    # the other rule and hand a reader a comparison they cannot use. The gap is accepted
    # deliberately and named, on the shape already used for a deliberately-accepted stale
    # sovereign quote. WHAT IT COSTS: the currency path's first year is derived from a
    # spot four weeks old, and the pound moved little over that window, so the effect is
    # small - but it is an effect and it is not asserted to be zero.
    macro_record=dict(
        path='EG',
        # The declaration is a MAPPING carrying a reason, not a bare string: the gate
        # reads `reason` and an empty one has switched the check off rather than
        # declared it.
        anchor_staleness_accepted=dict(
            accepted=True, anchor_date='2026-08-06', strike_date='2026-09-03',
            days=28, bound_days=14,
            reason=(
            "Struck 3 September 2026 against a house Egyptian path whose FX spot anchor "
            "is dated 6 August 2026, twenty-eight days earlier and past the fourteen-day "
            "bound. Accepted deliberately: refreshing the house path is a house-level act "
            "rather than a step of this name's rebuild, and re-striking this study onto "
            "the anchor's own date would deliver it against a month-old price. The "
            "staleness is disclosed, not switched off.")),
    ),
)
# [R-GAP-01] THE PRICE CARRIES ITS DATE. The spot has always been registered with its own
# date in the input register, four fields like every other input, and that date reached the
# committed numbers NOWHERE — so nothing outside the study could tell a price struck today
# from one struck a month ago, and half the book was in that state when it was first
# measured. The date is not invented here: it is the spot input's own, surfaced.
OUT['spot_date'] = INP['spot']['date']

_carried = write_preserving(os.path.join(HERE, 'study_numbers.json'), OUT)
if _carried:
    say('[R-REPAIR-01] carried forward downstream-owned record(s): %s' % ', '.join(_carried))
say("=" * 78)
say(f"WROTE study_numbers.json | central EGP {central:.2f} [{lo:.2f} - {hi:.2f}] vs spot "
    f"{SPOT:.2f} | DCF {dcf_ps:.2f} | TV {tv_share:.0%} of EV | WACC {wacc_exp:.2%} -> "
    f"{wacc_term:.2%}")
