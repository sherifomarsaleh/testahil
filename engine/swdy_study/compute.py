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
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import terminal_value as TV          # [R-TERM-01] — verified by import, not by parse

# ============================ INPUTS =========================================
def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)

H126 = ("Reviewed condensed interim consolidated financial statements for the six months "
        "ended 30 June 2026, El Sewedy Electric Company, approved for issuance by the board "
        "on 11 August 2026 (note 2-1), published on the company's own investor-relations "
        "portal at ir.elsewedyelectric.com")

INP = dict(
    # ---- anchors --------------------------------------------------------
    spot=I(105.20, "Uploaded EGX daily price history, last close", "2026-08-05", "Market"),
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
    assoc_bv_fy25=I(6757.650507, "Equity-accounted investees, carrying value, 31 Dec 2025 — the "
                    "closing balance used in the valuation bridge (the anchor date is Aug-2026, so "
                    "the FY2025 close is the most recent audited figure, not FY2024's)",
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
    seg_profit_h1_25=I(dict(cables=6823.397790 + 3925.845038,
                            construct=2031.644426 + 1083.868786,
                            elecprod=1923.388459 + 1713.421415),
                       H126 + ", note 16 H1-2025 comparative, segment profit — THE HALF THIS "
                       "STUDY MUST COMPARE AGAINST, because FY2025's group margin of 12.18% "
                       "sits well below H1-2025's 14.06%: this company's halves are not alike "
                       "and a half-against-full-year comparison is a basis error",
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
    seg_rev_hist=I(dict(
        FY23=dict(cables=82421.265314, construct=53482.804001, elecprod=16282.178230),
        FY24=dict(cables=137189.798892, construct=70921.447985, elecprod=23870.588700),
        FY25=dict(cables=155792.929738, construct=90958.550228, elecprod=34297.601753)),
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
                  "copper-linked; the company does not disclose tonnage, so the model tracks the "
                  "copper x FX growth rate rather than reconstructing an absolute volume)",
                  "2026-08-05", "Industry"),
    fx_hist=I(dict(FY23=30.59, FY24=45.3, FY25=49.5),
              "Annual average USD/EGP. FY2023 average of 30.59 is the audited FY2023 filing's own "
              "disclosed figure (Note 44-3-1); FY2024/FY2025 are house averages consistent with the "
              "scale of the disclosed devaluation", "2026-08-05", "Country/House"),
    fx_path=I([51.0, 54.0, 57.5, 61.0, 64.5],
              "USD/EGP average-rate path, about 6%/yr of depreciation from the FY2025 average of "
              "49.5. Used as a genuine driver of the Cables segment's copper-linked growth and of "
              "the currency-of-discounting alternative — not a translation convenience. "
              "DELIBERATELY BELOW covered-interest parity, which on the roughly 22% pound rate "
              "against a ~4-5% dollar rate implies materially faster depreciation; the base case "
              "assumes disinflation closes most of that gap. The parity case is carried as an "
              "explicit sensitivity", "2026-08-05", "House"),
    copper_fcst=I([13400.0, 14000.0, 14000.0, 14000.0, 14000.0],
                  "LME copper. FY2026 is set at USD 13,400/t, between the Q1-2026 average actually "
                  "realised and the current cash price of about 14,000 (early August 2026); "
                  "thereafter the current level is held flat — copper is the largest single input "
                  "into the Cables segment and a directional view on it would dominate the "
                  "valuation. The -10% column of the sensitivity carries the mean-reversion case",
                  "2026-08-05", "Industry"),
    cables_real_growth=I([0.030, 0.030, 0.030, 0.030, 0.030],
                        "Real (ex-copper, ex-FX) volume/market-share growth for the Cables segment "
                        "— modest and flat, since the company does not disclose tonnage and the "
                        "model should not manufacture a volume story it cannot evidence. Cables "
                        "segment revenue growth = (1+copper growth)(1+FX growth)(1+this) - 1",
                        "2026-08-05", "House"),
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

    construct_growth=I([0.18, 0.14, 0.11, 0.09, 0.08],
                       "Constructions segment revenue growth, tapering from the FY2025 disclosed "
                       "rate of +28.3% (FY2024: +32.6%) toward a more sustainable long-run pace. No "
                       "order book or backlog figure is disclosed in any of the audited filings or "
                       "the Q1-2026 interim, so — unlike the previous build — this is NOT a "
                       "burn-rate-on-a-backlog construction; it is a direct taper on the segment's "
                       "own revenue history", "2026-08-05", "House"),
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

    elecprod_growth=I([0.20, 0.16, 0.13, 0.11, 0.10],
                      "Electrical products and digital solutions segment revenue growth, tapering "
                      "from the FY2025 disclosed rate of +43.7% (FY2024: +46.6%) off a smaller "
                      "revenue base", "2026-08-05", "House"),
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
    nwc_pct=I(0.199, "Net working capital as a share of revenue, held at the FY2025 disclosed "
              "level (19.87%) — a genuine improvement on FY2023 (24.1%) and FY2024 (23.1%), "
              "carried forward without assuming further improvement or reversion",
              "2026-08-05", "House"),
    capex_pct=I([0.044, 0.040, 0.036, 0.033, 0.031],
                "Capex as a share of revenue, tapering from the FY2025 disclosed level of 4.7% "
                "(up from 3.1% FY2023 and 3.7% FY2024) toward a lower maintenance-plus-modest-"
                "capacity level as the current expansion cycle completes", "2026-08-05", "House"),
    dna_pct=I(0.0125, "Depreciation and amortisation as a share of revenue, held near the FY2025 "
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
    erp_ops_weighted=I(0.0737, "Operations-weighted equity risk premium: 30% Egypt at 9.41% and 70% "
                       "rest-of-world at a 6.5% blended emerging/frontier premium, reflecting where "
                       "the revenue is actually earned. Shown as an explicit alternative, not the "
                       "primary, because the standing house rule takes the country premium of the "
                       "listing and reporting currency", "2026-08-05", "House"),
    beta=I(1.009, "Own-stock tier-1 regression: SWDY weekly log-returns against a 31-name "
           "equal-weight EGX composite built from the full covered library, 5-year window. "
           "R-squared 0.291, n = 258, standard error 0.098, 90% confidence interval [0.85, 1.17]. "
           "Comfortably clears the usability gate and is NOT weak-instrument flagged (R-squared "
           "well above 10%, interval span 0.32 against a 1.009 point estimate)", "2026-08-05", "House"),
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
    kd_hard_note=I(0.0529, "Average interest rate on US-dollar and other foreign-currency financial "
                   "liabilities, blended, audited FY2025 Note 32 and Note 43-3-2. The company "
                   "simplified its disclosure from a three-way EGP/USD/EUR split (FY2024: 28.68% / "
                   "6.49% / 3.92%) to this two-way EGP/blended-foreign split from FY2025 onward; "
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
    rf_term=I(0.105, "Terminal risk-free rate, norm-built: the CBE's own stated medium-term "
              "inflation target of 5% plus the standard ~5.5pp emerging-market real-rate "
              "convention. Never a raw historical average and never reverse-engineered from a price",
              "2026-08-05", "House"),
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
    pi_term=I(0.07, "Terminal Egyptian inflation, read from the HOUSE MACRO PATH "
              "(engine/macro_paths/EG.json) and not from this study. [R-MACRO-01]: a study "
              "may not carry an inflation number of its own. Registered here so that the "
              "terminal growth rate below can be DERIVED from it rather than typed beside it",
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
    asset_life_derived=I(17.26,
        "DERIVED BY IDENTITY, not chosen: the AVERAGE depreciable gross cost across the year "
        "((43,605.306327 opening + 50,775.950574 closing) / 2) over the year's own "
        "depreciation charge of 2,733.671862. The average is used rather than the closing "
        "balance because the base grew 16% in the year and a closing-cost ratio overstates "
        "the life on a fast-growing base (that reading is 18.57 years). Per component the "
        "closing-cost readings are buildings 29.00y, machinery 18.72y, furniture 8.45y, "
        "vehicles 8.45y, leasehold improvements 13.13y, against disclosed ranges of 8-50, "
        "5-15, 4-17, 5-8 and 'over 3 years or the lease period' — the disclosed ranges are "
        "RANGES, and a life this desk picked from inside one would not be a disclosed life "
        "(SIGCM clause 1), which is why the identity is used instead",
        "2026-03-01", "Company/derived"),
    asset_life_source=I("Audited FY2025 consolidated financial statements of El Sewedy Electric "
        "Company, note 17 (property, plant and equipment) read with the accounting-policies "
        "note on depreciation: average depreciable gross cost over the year's own charge, "
        "excluding land, which the policy note states is not depreciated, and projects under "
        "construction, which are not in use.",
        "The source string the terminal module requires. It refuses a life with no "
        "disclosure behind it", "2026-03-01", "Company"),
    g_term_real=I(0.0, "STATED real terminal growth: zero. A mature diversified industrial "
                  "holding its real scale in perpetuity; real growth costs incremental capital "
                  "and none is assumed. The nominal rate is DERIVED from this and the house "
                  "path's terminal inflation, never quoted beside it", "2026-09-04", "House"),
    g_term=I(0.07, "Terminal NOMINAL growth, DERIVED: (1 + 0.0 real) x (1 + 0.07 house "
             "Egyptian terminal inflation) - 1 = 7.0%. The house macro path is the only "
             "source of an inflation rate in this study [R-MACRO-01]; the first edition's "
             "5.0% was struck against an assumed 5% inflation and was therefore a real "
             "decline of 1.87% a year for ever", "2026-09-04", "House"),
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
    anchor_days=I(217, "Days from the DCF's construction date (31 Dec 2025, the audited "
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

# ---- cost of capital: explicit window (sovereign double-count removed) -----
rf_star = V['rf'] - V['sov_spread_cds']
ke_exp = rf_star + V['beta'] * V['erp_cds']
ke_rating_alt = (V['rf'] - V['sov_spread_rating']) + V['beta'] * V['erp_rating']
ke_ops_alt = rf_star + V['beta'] * V['erp_ops_weighted']
ke_raw_retired = V['rf'] + V['beta'] * V['erp_cds']
kd_at = V['kd'] * (1 - TAX)
wd_exp = V['nd_fy25'] / (V['nd_fy25'] + MKTCAP)
we_exp = 1 - wd_exp
wacc_exp = we_exp * ke_exp + wd_exp * kd_at
wd_gross = debt_fy25 / (debt_fy25 + MKTCAP)
wacc_exp_gross = (1 - wd_gross) * ke_exp + wd_gross * kd_at
say(f"[Cost of equity] rf {V['rf']:.2%} less sovereign CDS spread {V['sov_spread_cds']:.2%} = "
    f"{rf_star:.2%}; + beta {V['beta']:.3f} x ERP {V['erp_cds']:.2%} -> Ke {ke_exp:.2%}. "
    f"Alternatives disclosed: rating basis {ke_rating_alt:.2%}; operations-weighted premium "
    f"{ke_ops_alt:.2%}; the RETIRED un-netted construction {ke_raw_retired:.2%} (audit trail only).")
say(f"[WACC explicit] weights on NET financial debt {wd_exp:.1%} / equity {we_exp:.1%} -> "
    f"{wacc_exp:.2%}. On gross debt the weights would be {wd_gross:.1%} / {1-wd_gross:.1%} -> "
    f"{wacc_exp_gross:.2%}; the net-debt basis is used because it is the same quantity the "
    f"enterprise-to-equity bridge subtracts, and it is the more conservative of the two.")

# ---- terminal (norm-built, never backed out of a price) --------------------
ke_term = V['rf_term'] + V['beta'] * V['erp_term']
kd_term_at = V['kd_term'] * (1 - TAX)
wacc_term = (1 - V['wd_term']) * ke_term + V['wd_term'] * kd_term_at
say(f"[WACC terminal] Ke {ke_term:.2%} (rf {V['rf_term']:.2%} + beta x ERP {V['erp_term']:.2%}); "
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
        r_cab *= (1 + cu_growth) * (1 + V['cables_real_growth'][i]) * (vol_mult ** 0.2)
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

# ---- FCFF waterfall ---------------------------------------------------------
dna = [V['dna_pct'] * r for r in rev]
ebit = [ebitda[i] - dna[i] for i in range(5)]
nopat = [e * (1 - TAX) for e in ebit]
capex = [V['capex_pct'][i] * rev[i] for i in range(5)]
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
_terminal = TV.build(TV.TerminalInputs(
    nopat=nopat[-1] * (1 + V['g_term']),
    wacc=wacc_term,
    inflation=V['pi_term'],
    real_growth=V['g_term_real'],
    dna_book=dna[-1] * (1 + V['g_term']),
    useful_life_years=V['asset_life_derived'],
    useful_life_source=V['asset_life_source'],
    # MAINTENANCE ON BOOK D&A ESCALATED OVER HALF THE DERIVED LIFE, not on the FY2025
    # gross cost. THE FIRST DRAFT OF THIS TERMINAL USED THE FY2025 BASE AND WAS WRONG:
    # the model itself adds five years of capex, growing net depreciable PP&E from
    # 24,806 to 90,938 — 3.67x — so a maintenance charge struck on the opening base
    # understates replacement by a multiple, and it showed as a charge of 7,916 against
    # the model's own FY2030 capex of 17,212. The terminal-year book D&A already carries
    # the built-up base; escalating it over half an asset life converts historical cost
    # to replacement cost, which is the module's own cross-check route made primary here
    # because the other one's base was stale.
    maintenance_basis='book_dna_escalated',
    working_capital=nwc[-1] * (1 + V['g_term']),
    incremental_capital_per_unit_growth=ic[-1]))
rr_term = V['g_term'] / roic_term          # kept as the RECORD of the retired construction
nopat_term = nopat[-1] * (1 + V['g_term'])
tv = _terminal.tv
pv_tv = tv * df[-1]
ev = pv_explicit + pv_tv
tv_share = pv_tv / ev
_tv_retired = nopat_term * (1 - rr_term) / (wacc_term - V['g_term'])
say(f"[Terminal value, sanctioned construction] terminal NOPAT {nopat_term:,.0f} + book D&A "
    f"{_terminal.dna_addback:,.0f} - maintenance at replacement cost {_terminal.maintenance:,.0f} "
    f"(on the DERIVED {V['asset_life_derived']:.2f}-year life) - growth capital "
    f"{_terminal.growth_capex:,.0f} (zero, because real growth is zero) - inflation on working "
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
# THE CAP IS STATED AND IS WHY THIS IS AN UPPER BOUND: the statutory share is capped at
# total annual wages, so as profit grows faster than the wage bill the percentage falls.
# Nothing in the filings discloses the cap's headroom, so it is not modelled — the charge
# is held at the measured rate and the direction of the unmodelled cap is recorded.
emp_rate = (V['emp_share_fy24'] / V['npa_fy24']
            + V['emp_share_fy25'] / V['npa_fy25']
            + V['emp_share_h1_26'] / V['h1_26_npa']) / 3.0
emp_charge = eq_attr * emp_rate
eq_attr_pre_emp = eq_attr
eq_attr = eq_attr - emp_charge
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
# price is dated 5 August 2026. So every per-share value is rolled 217/365 of a year forward
# at the cost of equity, less the EGP 1.85 FY2025 dividend paid inside the window (ex
# 1-Jun-2026) — fair value grows at the required return net of distributions, by the
# discount identity itself. Added after external critique correctly showed the previous
# construction compared a 31-Dec-2025 value to an August price, breaching this study's own
# one-date rule by about seven months of accretion.
T_ANCHOR = V['anchor_days'] / 365.0
ROLL = (1 + ke_exp) ** T_ANCHOR
def to_anchor(v):
    return v * ROLL - V['dps_fy25']
dcf_ps = to_anchor(dcf_ps_dec)
say(f"[Bridge] EV {ev:,.0f} - net financial debt {V['nd_fy25']:,.0f} + associates at carrying "
    f"value {assoc_val:,.0f} = {eq_pre_nci:,.0f}; less minority interests at their "
    f"{nci_share:.1%} share of group profit = {nci_val:,.0f}; less the employees' statutory "
    f"share of profit at {emp_rate:.2%} = {emp_charge:,.0f} -> equity attributable to ORDINARY "
    f"SHAREHOLDERS {eq_attr:,.0f} = EGP {dcf_ps_dec:.2f}/share AT 31-DEC-2025; rolled "
    f"{V['anchor_days']:.0f}/365 of a year to the 5-Aug-2026 anchor at the {ke_exp:.1%} cost of "
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
        nopat=nopat[-1] * (1 + g_), wacc=wt_, inflation=V['pi_term'], real_growth=real_,
        dna_book=dna[-1] * (1 + g_),
        useful_life_years=V['asset_life_derived'],
        useful_life_source=V['asset_life_source'],
        maintenance_basis='book_dna_escalated',
        working_capital=nwc[-1] * (1 + g_),
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
def _rel(mult):
    return to_anchor((((mult * ebitda_mid) * df_rel + pv[0] + pv[1]
                       - V['nd_fy25'] + assoc_val) * (1 - nci_share)) / SH)
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
norm_np = (norm_ebit - norm_interest + norm_assoc) * (1 - TAX) * (1 - nci_share)
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
    _capex = [V['capex_pct'][i] * r for i, r in enumerate(_rev)]
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
        nopat=_nopat[-1] * (1 + g), wacc=_wt, inflation=V['pi_term'], real_growth=_real,
        dna_book=_dna[-1] * (1 + g),
        useful_life_years=V['asset_life_derived'],
        useful_life_source=V['asset_life_source'],
        maintenance_basis='book_dna_escalated',
        working_capital=_nwc[-1] * (1 + g),
        incremental_capital_per_unit_growth=_ic_end)).tv
    _ev = sum(_f[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    return to_anchor(((_ev - V['nd_fy25'] + assoc_val) * (1 - nci_share)
                      * (1 - emp_rate)) / SH)

_base_chk = dcf_scenario()
assert abs(_base_chk - dcf_ps) < 0.02, f'scenario engine does not reproduce base: {_base_chk} vs {dcf_ps}'

dcf_bear = dcf_scenario(gp_unit_mult=0.88, fx_mult=0.94, wacc_shift=+0.02, g=0.03, opex_shift=+0.005)
dcf_bull = dcf_scenario(gp_unit_mult=1.12, fx_mult=1.08, wacc_shift=-0.02, g=0.06, opex_shift=-0.005)
say(f"[DCF scenarios] bear {dcf_bear:.2f} / base {dcf_ps:.2f} / bull {dcf_bull:.2f} EGP per share")

# ---- synthesis ----------------------------------------------------------------
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
say(f"[Synthesis] weighted central EGP {central:.2f}; full span across lenses and scenarios "
    f"{lo:.2f} - {hi:.2f}; spot {SPOT:.2f} ({central/SPOT-1:+.0%} to the central).")
assert 0.20 <= central / SPOT <= 3.0, f"central/spot {central/SPOT:.2f} outside the plausibility band"

# ---- sensitivity grids ---------------------------------------------------------
g_grid = [0.03, 0.04, 0.05, 0.06, 0.07]
wt_grid = [wacc_term - 0.02, wacc_term - 0.01, wacc_term, wacc_term + 0.01, wacc_term + 0.02]
we_grid = [wacc_exp - 0.03, wacc_exp - 0.015, wacc_exp, wacc_exp + 0.015, wacc_exp + 0.03]

def dcf_at(we_, wt_, g_):
    _fwd = [we_ - (we_ - wt_) * f for f in glide_frac]
    _df, cc = [], 1.0
    for w in _fwd:
        cc /= (1 + w); _df.append(cc)
    _rr = min(g_ / roic_term, 0.95)
    _tv = nopat[-1] * (1 + g_) * (1 - _rr) / max(wt_ - g_, 0.02)
    _ev = sum(fcff[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    return to_anchor(((_ev - V['nd_fy25'] + assoc_val) * (1 - nci_share)) / SH)

grid_wacc_g = [[dcf_at(wacc_exp, wt, g) for g in g_grid] for wt in wt_grid]
grid_exp_term = [[dcf_at(we, wt, V['g_term']) for wt in wt_grid] for we in we_grid]
beta_grid = [0.60, 0.80, round(V['beta'], 3), 1.15, 1.30]
def dcf_beta(b):
    ke = rf_star + b * V['erp_cds']
    we_ = we_exp * ke + wd_exp * kd_at
    wt_ = (1 - V['wd_term']) * (V['rf_term'] + b * V['erp_term']) + V['wd_term'] * kd_term_at
    return dcf_at(we_, wt_, V['g_term'])
grid_beta = [dcf_beta(b) for b in beta_grid]
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
    meta=dict(ticker='SWDY', company='Elsewedy Electric Company S.A.E.', market='EGX',
              currency='EGP', asof='2026-08-05', spot=SPOT, shares_mn=SH, mktcap=MKTCAP,
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
    fcst=dict(years=YRS, rev=rev, dom=dom, fgn_usd=fgn_usd, fgn_egp=fgn_egp,
              ebitda=ebitda, ebitda_margin=ebitda_margin, dna=dna, ebit=ebit, nopat=nopat,
              capex=capex, nwc=nwc, dnwc=dnwc, fcff=fcff, df=df, pv=pv, fwd_wacc=fwd,
              ppe=ppe, ic=ic, roic=roic, np_attr=np_fc, equity=eq_fc, net_debt=nd_fc,
              interest=interest_path, assoc=assoc_fc, div=div_fc, seg_gp=seg_gp,
              seg_rev=seg_rev, seg_ebit=seg_ebit, seg_shares=shares,
              payout=PAYOUT, assoc_g=ASSOC_G, glide_frac=glide_frac,
              ppe_fy25=ppe_fy25, eqp_fy25=eqp_fy25, assoc_fy25=V['assoc_fy25'],
              debt_fy25=debt_fy25, nwc_fy25=nwc_fy25, dna_fy25=V['dna_fy25'],
              nopat_fy25=nopat_fy25, ic_fy25=ic_fy25),
    seg_fy25=dict(rev=SRH['FY25'], gp=SPH['FY25'], names=SEGNAME,
                  gp_margin=unit_hist['FY25']['margin']),
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
             eq_attr=eq_attr, ps=dcf_ps, ps_dec=dcf_ps_dec, roll=ROLL,
             anchor_days=V['anchor_days'], roic_term=roic_term, rr_term=rr_term,
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
    lenses=lenses, central=central, span=[lo, hi], spot=SPOT,
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
)
with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(OUT, f, indent=1, default=float)
say("=" * 78)
say(f"WROTE study_numbers.json | central EGP {central:.2f} [{lo:.2f} - {hi:.2f}] vs spot "
    f"{SPOT:.2f} | DCF {dcf_ps:.2f} | TV {tv_share:.0%} of EV | WACC {wacc_exp:.2%} -> "
    f"{wacc_term:.2%}")
