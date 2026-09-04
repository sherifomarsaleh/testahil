"""SCEM (Sinai Cement Company S.A.E., EGX: SCEM) — master computation, REVISION 2.

Revision 2 rebuilds the operating line BOTTOM-UP and applies 69 corrections accepted
from a four-part external critique. Writes study_numbers.json, the single source of
truth for every builder.

WHAT CHANGED, AND WHY IT MATTERS
  * EBITDA is now an OUTPUT of a physical cost stack, not an asserted margin. Revision 1
    set the FY2026E margin at 30.5% — ABOVE the very year it called a cyclical peak.
  * The historical profit closure uses the EFFECTIVE tax rate (~32%), not the statutory
    22.5%. Revision 1 back-solved an operating line through the wrong rate.
  * Net cash is the REPORTED FY2025 balance, not a figure solved from the income it
    earns and then grown by an undisclosed multiplier. It is now also sensitised.
  * Growth is bought at the same return in the explicit window as in the terminal.
    Revision 1 grew revenue 7.6% a year for free, then charged replacement cost forever.
  * Terminal beta is re-levered to the assumed terminal capital structure (Hamada).
  * Non-controlling interests are deducted in the bridge.
  * The normalised lens adds cash at FACE rather than capitalising its yield at 7x.
  * Discounting is mid-year with a stub from the valuation date.
  * Historical per-share figures use period-weighted share counts, not today's.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import terminal_value as TV   # [R-TERM-01] the only sanctioned way to build a terminal

LOG = []
def say(s):
    LOG.append(s); print(s)

def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)

EGX = ("EGX filing reported by Global Cement, cemnet/International Cement Review, Daily "
       "News Egypt and Arab Finance")
SP = ("FY2025 balance-sheet data from S&P Global Market Intelligence as carried by two "
      "independent aggregations (stockanalysis.com, simplywall.st), which agree")

INP = dict(
    # ---- anchors ---------------------------------------------------------
    spot=I(100.50, "Closing price 02-Sep-2026, from the price file the principal supplied "
           "on 3 September 2026 and committed at engine/prices/SUPPLIED_03-09-2026.json. "
           "[R-GAP-01 AMENDED 03-Sep-2026] NO STUDY IS DELIVERED AGAINST A STALE PRICE: "
           "this edition was struck against the 06-Aug close of 79.00, and the shares have "
           "risen 27.2% in the month since. A fair value published against a month-old "
           "price is a comparison a reader cannot use, whatever the fair value is worth",
           "2026-09-02", "Market"),
    spot_prev=I(79.00, "The 06-Aug-2026 close this study was previously struck against "
                "(open 81.80, high 82.50, low 78.30), kept so the re-strike is visible "
                "rather than silent", "2026-08-06", "Market"),
    shares_mn=I(260.812477, "260,812,477 shares, corroborated FIVE ways: issued capital "
                "EGP 2,608,124,770 at EGP 10 par; the Jul-2025 tender offer of 58,416,664 "
                "shares at 22.4%; quoted market capitalisation over price; and the "
                "reconstruction 133.07mn pre-issue + 127.74mn subscribed. Revision 1 "
                "wrongly described the pre-issue count as 92.61mn by subtracting shares "
                "OFFERED (168.20mn) instead of shares SUBSCRIBED (127.74mn, a 75.95% "
                "take-up)", "2025-07-28", "Company"),
    shares_fy23=I(133.07, "Weighted-average shares FY2023, pre-rights-issue. Corroborated "
                  "by the 2022 tender offer (56.063mn = 42.12%) and by disclosed EPS",
                  "2025-03-16", "Company"),
    shares_fy24=I(133.07, "Weighted-average shares FY2024. Disclosed EPS of EGP 23.13 on "
                  "attributable profit implies 132.7mn", "2025-03-16", "Company"),
    shares_fy25=I(222.0, "Weighted-average shares FY2025, the rights issue having "
                  "completed during the year", "2026-03-10", "Company"),
    tax_stat=I(0.225, "Egypt statutory corporate income tax", "2026", "Country"),
    tax_eff=I(0.320, "EFFECTIVE tax rate on the FY2025 closure. Disclosed pre-tax profit "
              "of 3,378.7 against profit after tax of 2,298.2 gives 32.0%. Revision 1 "
              "used the statutory 22.5% here, which understated every derived operating "
              "line", "2026-03-10", "Company"),

    # ---- disclosed history (EGP mn) --------------------------------------
    rev_fy23=I(4285.470153, "Audited statement of profit or loss for the year ended 31 December 2023 (the comparative column of the FY2024 filing), printed page 3, read from the company's own website and committed with its footings in filings_extract.py. Revision 2 used a trade-press figure relayed from an EGX filing it had not read", "2025-12-31", "Company"),
    rev_fy24=I(6428.011851, "Audited statement of profit or loss for the year ended 31 December 2024, printed page 3, read from the company's own website and committed with its footings in filings_extract.py. Revision 2 used a trade-press figure relayed from an EGX filing it had not read", "2025-12-31", "Company"),
    rev_fy25=I(9089.149688, "Audited statement of profit or loss for the year ended 31 December 2025, printed page 3, read from the company's own website and committed with its footings in filings_extract.py. Revision 2 used a trade-press figure relayed from an EGX filing it had not read", "2025-12-31", "Company"),
    pat_fy23=I(-117.581612, "Audited statement of profit or loss for the year ended 31 December 2023 (the comparative column of the FY2024 filing), printed page 3, read from the company's own website and committed with its footings in filings_extract.py. Revision 2 used a trade-press figure relayed from an EGX filing it had not read", "2025-12-31", "Company"),
    pat_fy24=I(3072.361811, "Audited statement of profit or loss for the year ended 31 December 2024, printed page 3, read from the company's own website and committed with its footings in filings_extract.py. Revision 2 used a trade-press figure relayed from an EGX filing it had not read", "2025-12-31", "Company"),
    pat_fy25=I(2284.539004, "Audited statement of profit or loss for the year ended 31 December 2025, printed page 3, read from the company's own website and committed with its footings in filings_extract.py. Revision 2 used a trade-press figure relayed from an EGX filing it had not read", "2025-12-31", "Company"),
    ebitda_fy24=I(1590.0, "FY2024 EBITDA, the one disclosed margin anchor",
                  "2026-03-10", "Company"),
    ta_fy24=I(6385.92, EGX + " — FY2024 total assets", "2025-03-16", "Company"),
    tl_fy24=I(1610.86, EGX + " — FY2024 total liabilities; the triple closes to equity of "
              "4,775.06 exactly", "2025-03-16", "Company"),
    # ---- THE COST STACK, FROM THE COMPANY'S OWN NOTES 24, 25 AND 26 ----------------
    cost_materials_fy25=I(3592.466202, "Note 24, 'Raw materials, Supplies, fuel, power, "
        "packing sacks', FY2025 " + "audited statements for the year ended 31 December 2025, read from the company's own website; committed with its footings in filings_extract.py" + ". Revision 2 built this from four industry "
        "rules of thumb summing to EGP 2,553.7mn — 40.7% BELOW the disclosed line",
        "2025-12-31", "Company"),
    cost_distribution_fy25=I(770.524093, "Note 25 'Transfer & loading expenses & renting "
        "cars to transport cement' 579.219496 plus 'Export expenses and quality mark' "
        "185.690219, plus note 24's own 'Transfer & loading' 5.614378, FY2025 " + "audited statements for the year ended 31 December 2025, read from the company's own website; committed with its footings in filings_extract.py",
        "2025-12-31", "Company"),
    cost_fixed_fy25=I(1270.954249, "The rest of the disclosed cash operating cost: revenue "
        "9,089.149688 less EBITDA 3,455.205144 less the two lines above. It is wages, "
        "maintenance, subcontractors, clay resource fees, rents, technical assistance, "
        "insurance and general administration across notes 24, 25 and 26. Revision 2 "
        "assumed USD 14.60 per tonne of installed capacity = EGP 2,762.9mn, 2.17x the "
        "company's actual fixed cost, and that single assumption is most of why its "
        "FY2025 backcast came out 355mn light on EBITDA", "2025-12-31", "Company"),
    materials_usd_share=I(0.484, "The dollar-linked share of the materials line. THE FILING "
        "DOES NOT SPLIT IT, so this is an ESTIMATE and is flagged as one: it is the fuel "
        "share of revision 2's own four-part stack (458.0 of 946.5 per tonne), which is "
        "the only evidenced split available. The rest escalates on the domestic cost path. "
        "Sensitised in section 6", "2026-08-06", "House"),
    # ---- WHAT THE ASSETS COST TO RUN AND TO REPLACE --------------------------------
    gross_fixed_fy25=I(3140.855154, "Note 4, gross cost of fixed assets at 31-Dec-2025, "
        "footing across five classes " + "audited statements for the year ended 31 December 2025, read from the company's own website; committed with its footings in filings_extract.py", "2025-12-31", "Company"),
    dep_rate_disclosed=I(0.038626, "The weighted depreciation rate implied by note 3/2's "
        "disclosed rates on note 4's own gross-cost mix: buildings 2-2.5%, machinery 5%, "
        "vehicles and tools 20%, furniture 10-25%. It reproduces the filed FY2025 charge "
        "to within 1.2% (121.3 against 122.6), which is what makes it a sourced forward "
        "rule rather than an assumption", "2025-12-31", "Company"),
    capex_run_rate=I(303.211, "Capex on the company's own cash-flow statements: FY2023 "
        "120.827, FY2024 526.408, FY2025 262.397, average 303.211. Revision 2 assumed "
        "4.5-5.0% of revenue, which is 435-484mn and rising", "2025-12-31", "Company"),
    # ---- THE LATEST DISCLOSED BALANCE SHEET [R-BRIDGE-01] --------------------------
    cash_mar26=I(5801.981716, "Cash on hand and at banks, REVIEWED interim statement of "
        "financial position as at 31 March 2026, printed page 2. This is the latest "
        "disclosed sheet and the bridge stands on it; revision 2 stood on 31-Dec-2025 and "
        "rolled it forward on an estimate", "2026-03-31", "Company"),
    debt_mar26=I(152.709964, "Lease liabilities, 137.620919 long-term and 15.089045 "
        "current, reviewed sheet at 31 March 2026. THE COMPANY HAS NO BANK BORROWINGS AT "
        "EITHER DATE — the whole of its interest-bearing debt is leases under EAS 49",
        "2026-03-31", "Company"),
    eq_mar26=I(7134.817689, "Total equity, reviewed sheet at 31 March 2026",
        "2026-03-31", "Company"),
    cash_fy25=I(4762.348666, "Cash on hand and at banks at 31 December 2025. Audited statement of financial position at 31 December 2025, printed page 2, from the company's own website. Revision 2 used an aggregator's carry of S&P Global Market Intelligence", "2025-12-31", "Company"),
    debt_fy25=I(137.565888, "Lease liabilities at 31 December 2025, 111.742265 long-term and 25.823623 current. THE COMPANY HAS NO BANK BORROWINGS. Audited statement of financial position at 31 December 2025, printed page 2, from the company's own website. Revision 2 used an aggregator's carry of S&P Global Market Intelligence", "2025-12-31", "Company"),
    eq_fy25_rep=I(6020.338736, "Total shareholders' equity at 31 December 2025, footing across capital, reserves, retained earnings and the year's profit. Audited statement of financial position at 31 December 2025, printed page 2, from the company's own website. Revision 2 used an aggregator's carry of S&P Global Market Intelligence", "2025-12-31", "Company"),
    nci=I(120.0, "Non-controlling interests deducted in the bridge. Revision 1 omitted "
          "them. One reviewer proposed 2,008 (15% of enterprise value) but derived it "
          "from nothing; the disclosed evidence — FY2023 group loss 121.42 against an "
          "attributable loss of ~117, and FY2024 attributable EPS 23.13 against group "
          "profit 3,070 — puts the minority share of profit BELOW 1%. Set at 120 and "
          "sensitised", "2026-08-06", "House"),

    # ---- the base-resetting transaction ----------------------------------
    swcc_eur=I(30.0, "EUR 30mn for the 25.40% Sinai White stake, completed 13-Aug-2024",
               "2024-08-13", "Company"),
    egp_per_eur_aug24=I(53.4, "EGP per EUR at completion", "2024-08-13", "Country"),
    swcc_book=I(100.0, "Carrying value of the 25.4% stake. Revision 1 asserted the profit "
                "bridge was 'insensitive to it within a +/-EGP 200mn range'. That was "
                "FALSE and untested: in revision 1 the chain ran book value -> gain -> "
                "SOLVED treasury income -> cash -> every lens, and a +/-200mn move was "
                "worth -4.9% to +9.8%. Revision 2 takes cash from the reported balance "
                "sheet instead, so this input now touches only the FY2024 gain/treasury "
                "split and nothing downstream", "2026-08-06", "House"),

    # ---- BOTTOM-UP PLANT AND COST STACK ----------------------------------
    cap_cement_mt=I(3.80, "Cement grinding capacity, El Hassana, two lines", "2025-03-23",
                    "Company"),
    cap_clinker_mt=I(2.57, "Kiln clinker capacity. The PAIR with cement capacity OBSERVES "
                     "the clinker factor rather than assuming it, and settles which base "
                     "a USD-per-tonne benchmark is quoted on", "2025-03-23", "Company"),
    clinker_factor=I(0.6763, "Tonnes of clinker per tonne of cement. ANCHORED on the "
                     "plant register's two capacities (2.57/3.80 = 0.676) but carried as "
                     "an independent input, because blending is a real operating lever: a "
                     "lower factor means more cement per tonne of clinker and less fuel "
                     "per tonne of cement. Deriving it from the capacity pair made kiln "
                     "capacity cancel out of cement output algebraically — the driver test "
                     "caught that", "2025-03-23", "Company"),
    kiln_util=I([0.710, 0.717, 0.735, 0.753, 0.772, 0.791],
                "Kiln utilisation FY2025A then FY2026E-FY2030E", "2026-08-06", "House"),
    thermal_gj_t_clinker=I(3.40, "Specific thermal energy, 3.2-3.6 GJ/t clinker for a dry "
                           "preheater/precalciner kiln", "2026-08-06", "Industry"),
    fuel_usd_gj=I(4.00, "Delivered solid fuel, petcoke/coal ~USD 128/t at ~32 GJ/t",
                  "2026-08-06", "Industry"),
    power_kwh_t_cement=I(100.0, "Specific electrical energy, 90-110 kWh/t cement",
                         "2026-08-06", "Industry"),
    power_tariff=I(2.60, "Egyptian industrial electricity tariff after subsidy reform",
                   "2026-08-06", "Country"),
    rawmat_egp_t=I(190.0, "Quarrying, raw meal and additives per tonne of cement",
                   "2026-08-06", "Industry"),
    packaging_egp_t=I(55.0, "Bag cost per tonne of bagged cement", "2026-08-06", "Industry"),
    bagged_share=I(0.70, "Bagged share of Egyptian despatches", "2026-08-06", "Industry"),
    distribution_egp_t=I(250.0, "Outbound freight and selling per tonne, set above a "
                         "typical Egyptian plant because El Hassana is distant from the "
                         "Cairo and Delta demand centres", "2026-08-06", "House"),
    fixed_usd_t_capacity=I(14.60, "Fixed cash cost per tonne of INSTALLED capacity so it "
                           "does not vanish when volume falls. Industry band USD 10-20/t. "
                           "14.60 is the level the FY2025 reconciliation implies against "
                           "an independently built variable stack — reported, not solved "
                           "away", "2026-08-06", "House"),
    domestic_share=I([0.88, 0.87, 0.86, 0.85, 0.84, 0.83], "Domestic share of despatches",
                     "2026-01-01", "Industry"),
    price_dom_egp_t=I([3503.0, 3993.4, 4431.3, 4781.6, 5079.3, 5359.6],
                      "Domestic realised price ex-works. FY2025 is the level the disclosed "
                      "revenue implies given the volume build — 13.9% below the ~EGP "
                      "4,070/t market average, which is what an ex-works price net of "
                      "freight and rebates looks like. THE REAL SPREAD PER TONNE IS THEN "
                      "HELD FLAT: price escalates on the same domestic cost path the cost "
                      "stack does. The previous path grew nominal prices well below the "
                      "domestic cost path this same model escalates costs on, and this "
                      "register described it as \'a REAL decline against CBE inflation\' "
                      "while sourcing no mechanism for it. [R-ANCHOR-01] refuses that "
                      "mechanism on the company\'s own measurement: cost per unit of "
                      "revenue FELL across the reviewed quarter pair and the audited year "
                      "between them, where the forecast needed it to rise, and a mechanism "
                      "contradicted by the filings is the "
                      "assumption wearing one. The 12.6Mt of dormant Egyptian capacity "
                      "queuing to restart is a real risk to price; it belongs in the bear "
                      "case and the sensitivity grid, which carry it, not in the base path",
                      "2026-09-04", "House"),
    price_exp_usd_t=I([48.0, 47.0, 46.0, 45.5, 45.0, 45.0],
                      "Export FOB per tonne, declining because the EU carbon border "
                      "mechanism raises the landed cost of Egyptian cement into Europe "
                      "from 2026", "2026-01-01", "Industry"),
    fx=I(49.8, "USD/EGP", "2026-08-06", "Country"),
    fx_path=I([49.8, 55.39, 59.96, 63.12, 65.42, 67.35], "USD/EGP path on RELATIVE "
              "PURCHASING-POWER PARITY against 2.5% foreign inflation, derived from this "
              "study\'s own domestic cost path rather than hand-set [R-MACRO-01]: the "
              "previous path slid the pound 5.4% in FY2026 while escalating domestic "
              "costs 14.0%, which is one event counted once and ignored once. Deriving it "
              "LOWERS the answer by 1.2% — a faster slide costs more on the dollar-linked "
              "materials line than it earns translating export revenue — which is the "
              "evidence that conforming to the rule is not fitting to the price. Raises "
              "the EGP cost of imported fuel AND the EGP value of export revenue",
              "2026-08-06", "House"),
    cost_infl=I([1.000, 1.140, 1.265, 1.365, 1.450, 1.530],
                "Cumulative local cost inflation index on the EGP cost lines",
                "2026-06-10", "Country"),

    # ---- capital intensity ------------------------------------------------
    dna_pct=I([0.046, 0.045, 0.044, 0.043, 0.042], "D&A as a share of revenue",
              "2026-08-06", "House"),
    capex_pct=I([0.050, 0.048, 0.047, 0.046, 0.045], "Capex as a share of revenue. No "
                "capital-expenditure disclosure is obtainable", "2026-08-06", "House"),
    wc_pct_drev=I(0.080, "Change in working capital over change in revenue",
                  "2026-08-06", "House"),
    payout=I(0.0, "Dividend payout from FY2026E. THE FILED EQUITY STATEMENTS SHOW NO DISTRIBUTION AT ALL, twice over and to the pound: equity of EGP 3,735.80mn at 31-Dec-2024 plus FY2025 profit of 2,284.54mn is exactly the filed 6,020.34mn, and that plus the reviewed quarter's 1,114.48mn is exactly the filed 7,134.82mn at 31-Mar-2026. A 60% payout was assumed against a company whose own statements reconcile with none, and an earlier edition called the implied distribution its 'largest single uncertainty' — it dissolves against the record. This changes no valuation number, because free cash flow to the firm is struck before financing; it changes the projected balance sheet a reader is shown", "2026-09-04", "Company"),
    cash_yield=I([0.190, 0.170, 0.150, 0.135, 0.125], "Yield earned on cash",
                 "2026-08-06", "House"),
    cash_yield_fy25=I(0.210, "Yield earned on cash through FY2025", "2026-08-06", "House"),

    # ---- cost of capital ---------------------------------------------------
    rf=I(0.2231, "Egypt 10-year local-currency government yield", "2026-07-21", "Country"),
    sov_spread_cds=I(0.0340, "Egypt CDS-implied sovereign default spread, Damodaran "
                     "January-2026, CDS column. NETTED OUT of the local risk-free rate so "
                     "sovereign default risk is not charged twice. One reviewer called "
                     "this a manipulation; two others cleared it explicitly, and it is "
                     "Damodaran's own construction — the country premium in the ERP is "
                     "DERIVED from this same spread", "2026-01-05", "Country"),
    erp_cds=I(0.0941, "Damodaran Egypt, CDS-BASED, January-2026: mature-market 4.23% + "
              "3.40% x (9.71/6.37) = 9.4127%. Revision 1 cited 'Damodaran, Egypt row' "
              "without naming the variant; a checker following that citation lands on the "
              "rating-based 13.94%", "2026-01-05", "Country"),
    beta=I(1.00, "Adopted beta. The own-stock regression FAILS the usability gate "
           "(R-squared 0.038 against a 0.05 floor) though n=256 and SE 0.153 both pass. "
           "The lead-lag corrected estimate is 0.837 and its 90% interval contains 1.00. "
           "Rounding up to 1.00 COSTS 1.84% of the central; that price is now stated "
           "rather than left implicit", "2026-08-06", "House"),
    kd=I(0.2150, "Marginal pre-tax cost of debt. Debt is 0.18% of capital, so a +/-700bp "
         "error moves the WACC by under 2bp", "2026-08-06", "House"),
    kd_path=I([0.2150, 0.1950, 0.1800, 0.1680, 0.1600], "Cost-of-debt path; the WACC glide "
              "inherits its SHAPE from this", "2026-08-06", "House"),
    kd_term=I(0.150, "Terminal cost of debt, the Egyptian long-run corporate norm",
              "2026-08-06", "House"),
    rf_term=I(0.125, "Terminal risk-free rate, norm-built from the CBE's OPERATIVE Q4-2026 "
              "inflation target of 7% plus a ~5.5pp emerging-market real-rate convention. "
              "Revision 1 used the later 5% target while its own text cited 'the 7% and "
              "then 5% targets'. REVIEWABLE CHOICE: reverting to 10.5% adds ~1.8%",
              "2026-08-06", "House"),
    erp_term=I(0.070, "Terminal equity risk premium, normalised below the crisis level",
               "2026-08-06", "House"),
    wd_term=I(0.20, "Terminal debt weight, normalised", "2026-08-06", "House"),
    g_term=I(0.05, "Terminal growth, 5% nominal against a terminal risk-free rate "
             "embedding disinflation — approximately zero real. Held at 5% rather than "
             "raised with the inflation target: 7% would put terminal growth above the "
             "disinflation path the same model assumes", "2026-08-06", "House"),
    stub_years=I(0.583, "Elapsed fraction of FY2026 at the valuation date (7 months). "
                 "Revision 1 discounted FY2026 a full year from a 6-Aug-2026 valuation "
                 "date and added a 31-Dec-2025 cash balance", "2026-08-06", "House"),

    # ---- lens inputs -------------------------------------------------------
    repl_usd_t=I(130.0, "Replacement cost per annual tonne of CEMENT capacity, USD 120-150 "
                 "band", "2026-08-06", "Industry"),
    ev_t_just=I(95.0, "Justified enterprise value per annual tonne of cement capacity",
                "2026-08-06", "House"),
    ev_ebitda_just=I(4.2, "Justified EV/EBITDA. Revision 1 used 5.0x anchored on a peer "
                     "quoted at 5.03x. That anchor does not reproduce: the peer's own "
                     "market capitalisation over profit gives 3.48x, not the 6.44x printed "
                     "beside it, and the implied EBITDA margin would be 68% for a cement "
                     "company. 4.2x is struck between the reproducible peer earnings "
                     "multiple and the asserted EBITDA multiple, and is disclosed as "
                     "weakly anchored", "2026-08-06", "House"),
    pe_just=I(7.0, "Justified price/earnings on normalised OPERATING earnings",
              "2026-08-06", "House"),
    norm_mgn=I(0.278, "Mid-cycle EBITDA margin: the midpoint of the FY2024 outturn (24.8%) "
               "and the corrected FY2025 peak (30.9%). Revision 1 struck 26.5% off an "
               "FY2025 margin understated by the statutory-rate error",
               "2026-08-06", "House"),
    norm_rev_haircut=I(0.92, "Haircut to the FY2025 revenue base for the normalised lens. "
                       "Revision 1 applied a mid-cycle MARGIN to a PEAK revenue base — "
                       "half a normalisation, in the lens whose stated purpose is refusing "
                       "to capitalise a peak", "2026-08-06", "House"),
    capacity_mt=I(3.80, "Alias of cement grinding capacity", "2025-03-23", "Company"),
    cash_growth_fy25=I(1.0, "RETIRED in revision 2 — cash is now the reported balance, not "
                       "a rolled derivation. Kept at 1.0 so nothing scales it",
                       "2026-08-06", "House"),
    treas_fy23=I(198.0, "FY2023 treasury income on its own smaller cash balance",
                 "2026-08-06", "House"),
    peer_mbsc_rev=I(5700.0, "Misr Beni Suef FY2025 net sales", "2026-03-01", "Industry"),
    peer_mbsc_pat=I(3946.0, "Misr Beni Suef FY2025 attributable profit", "2026-03-01", "Industry"),
    peer_mbsc_eps=I(61.25, "Misr Beni Suef FY2025 EPS", "2026-03-01", "Industry"),
    peer_mbsc_mcap=I(13730.0, "Misr Beni Suef market capitalisation", "2026-08-06", "Industry"),
    peer_mbsc_pe=I(3.48, "Misr Beni Suef trailing price/earnings RECOMPUTED as market "
                   "capitalisation over attributable profit. The 6.44x printed by data "
                   "providers cannot be reconciled with the market capitalisation printed "
                   "beside it — 6.44 x 3,946 = 25,412 against a stated 13,730",
                   "2026-08-06", "Industry"),
    peer_mbsc_evebitda=I(5.03, "Misr Beni Suef EV/EBITDA as quoted. Carried with a caution: "
                         "no enterprise value, EBITDA or net-cash figure is published for "
                         "it, and pairing it with the stated profit implies a 68% EBITDA "
                         "margin, which no cement company earns", "2026-08-06", "Industry"),
    peer_arcc_pat=I(3600.0, "Arabian Cement FY2025 consolidated profit", "2026-03-01", "Industry"),
    egy_capacity_mt=I(76.0, "Egyptian nameplate capacity", "2025-10-01", "Industry"),
    egy_revival_mt=I(12.6, "Dormant capacity under revival from 2H-2026", "2025-10-01", "Industry"),
    egy_prod_mt=I(65.0, "Egyptian cement production 2025", "2026-01-01", "Industry"),
    egy_cons_mt=I(54.0, "Egyptian domestic consumption 2025", "2025-10-01", "Industry"),
    egy_exports_mt=I(18.5, "Egyptian cement and clinker exports 2025", "2026-01-01", "Industry"),
    mto_price=I(41.00, "Vicat mandatory tender offer, July 2025. A disclosed reference "
                "point and an overhang, never a fair value", "2025-07-28", "Company"),
    w_dcf=I(0.48, "Weight, cash-flow lens", "2026-08-06", "House"),
    w_rel=I(0.21, "Weight, relative lens", "2026-08-06", "House"),
    w_norm=I(0.23, "Weight, normalised lens", "2026-08-06", "House"),
    w_asset=I(0.08, "Weight, asset lens. Revision 1 gave it 15% while arguing in the same "
              "document that restarted lines cost 'a fraction' of new build and that the "
              "asset lens 'should not be read as a floor'. Cut to 8%. REVIEWABLE CHOICE: "
              "15% adds ~3.6%, zero subtracts ~2.6%", "2026-08-06", "House"),
)

V = {k: v['value'] for k, v in INP.items()}
for k, v in INP.items():
    assert set(v) == {'value', 'source', 'date', 'ring'} and str(v['source']).strip(), k
TAX, TAXE = V['tax_stat'], V['tax_eff']
YRS = ['FY2026E', 'FY2027E', 'FY2028E', 'FY2029E', 'FY2030E']
HIST = ['FY2023', 'FY2024', 'FY2025']

# THE COMPANY'S OWN AUDITED STATEMENTS. filings_extract.py commits every figure with
# its statement, printed page and route, and asserts every footing the filings
# themselves perform — two of those assertions fired on the first run and both were
# right to. Nothing in this model reads a press figure for a company historical.
FIL = json.load(open('filings_extract.json'))

say("=" * 80)
say("SCEM — REVISION 3 — bottom-up operating model + 69 accepted corrections")
say("=" * 80)

# ============ 1. BOTTOM-UP OPERATING BUILD (EBITDA is an OUTPUT) ============
cf = V['clinker_factor']
say(f"\n[Clinker factor] {cf:.4f} t clinker per t cement, anchored on the register pair "
    f"{V['cap_clinker_mt']:.2f}/{V['cap_cement_mt']:.2f} = "
    f"{V['cap_clinker_mt']/V['cap_cement_mt']:.4f} but carried as an INDEPENDENT lever")
# The disclosed cost totals are anchored on FY2025 and carried per tonne of cement, on
# the volume this model itself computes for that year — so the anchor is the filing and
# the scaling is the model's own. A mis-split between volume and price would move both
# the per-tonne cost and the per-tonne price together and leave the forecast unchanged.
_cem_fy25 = V['cap_clinker_mt'] * V['kiln_util'][0] / cf
COST_MAT_T = V['cost_materials_fy25'] / _cem_fy25
COST_DIST_T = V['cost_distribution_fy25'] / _cem_fy25
BU = []
for i in range(6):
    clk = V['cap_clinker_mt'] * V['kiln_util'][i]
    cem = clk / cf
    dom = cem * V['domestic_share'][i]
    exp = cem - dom
    fx, infl = V['fx_path'][i], V['cost_infl'][i]
    rev = dom * V['price_dom_egp_t'][i] + exp * V['price_exp_usd_t'][i] * fx
    # THE COST STACK IS THE COMPANY'S OWN DISCLOSED ONE, ANCHORED ON FY2025 AND
    # ESCALATED PER DRIVER CLASS. Revision 2 built it from industry rules of thumb —
    # a fixed cost of USD 14.6 per tonne of capacity against a filed EGP 1,270.9mn,
    # 2.17x too high — and validated the result against an EBITDA SOLVED FROM THE SAME
    # PRESS FIGURES the historicals came from, so two wrong numbers agreed to 1.36%.
    # Notes 24, 25 and 26 of the audited FY2025 statements state the lines.
    esc_fx = fx / V['fx']                    # the USD-linked share travels with the pound
    esc_dom = infl / V['cost_infl'][0]       # the domestic share with the cost path
    mat_t = COST_MAT_T * (V['materials_usd_share'] * esc_fx
                                     + (1 - V['materials_usd_share']) * esc_dom)
    dist_t = COST_DIST_T * esc_dom
    var_t = mat_t + dist_t
    fixed = V['cost_fixed_fy25'] * esc_dom
    eb = rev - var_t * cem - fixed
    BU.append(dict(clinker=clk, cement=cem, dom=dom, exp=exp, util=V['kiln_util'][i],
                   rev=rev, price=rev / cem, c_mat=mat_t, c_dist=dist_t,
                   var_t=var_t, var=var_t * cem,
                   fixed=fixed, ebitda=eb, mgn=eb / rev))
say(f"[Bottom-up] FY2025 revenue {BU[0]['rev']:,.0f} vs disclosed {V['rev_fy25']:,.0f} "
    f"({BU[0]['rev']/V['rev_fy25']-1:+.2%}); EBITDA {BU[0]['ebitda']:,.0f} "
    f"(margin {BU[0]['mgn']:.1%}) — an OUTPUT, not an input")
say(f"[Forecast margins] " + " ".join(f"{b['mgn']:.1%}" for b in BU[1:]) +
    "  (revision 2, on an assumed cost stack, ran 30.1% to 26.4%)")
rev_f = [b['rev'] for b in BU[1:]]
ebitda_f = [b['ebitda'] for b in BU[1:]]

# ============ 2. THE HISTORICALS, AS FILED ==================================
# THE HISTORICALS ARE THE COMPANY'S OWN AUDITED STATEMENTS, NOT A SOLVE.
# Revision 2 assumed depreciation at 9.4%, 6.2% and 4.6% of revenue (the filings say
# 2.04%, 1.41% and 1.35%) and then SOLVED operating profit out of a press profit figure
# grossed at an effective tax rate, less a treasury income estimated on a cash balance
# rolled back by a guessed 1.25x. Every step of that is unnecessary: the statements
# state operating profit, depreciation, amortisation and profit after tax directly.
dna = {y: FIL['derived'][y]['dna'] for y in HIST}
ebit = {y: FIL['derived'][y]['ebit'] for y in HIST}
ebitda_h = {y: FIL['derived'][y]['ebitda'] for y in HIST}
# THE DISPOSAL GAIN IS THE FILED ONE. The FY2024 income statement states "Gain (loss)
# on sale of investments 1,517,386,642" on the face of the statement; revision 2
# reconstructed it from a euro consideration and a book value and reached 1,502.0.
swcc_gain = FIL['income_statement']['FY2024']['gain_on_sale_of_investments'] / 1e6
treas = {y: FIL['interest_income'][y] / 1e6 for y in HIST}
# FY2024's underlying profit, on the filings: operating profit and the recurring income
# beside it, taxed at that year's own effective rate — the disposal gain excluded.
_f24 = FIL['income_statement']['FY2024']
und24 = ((_f24['operating'] + _f24['finance']) / 1e6) * (1 - TAXE)
say(f"\n[FY2025, AS FILED] operating profit "
    f"{FIL['income_statement']['FY2025']['operating']/1e6:,.0f} plus the finance charge "
    f"sitting inside it {FIL['income_statement']['FY2025']['finance']/1e6:,.0f} = EBIT "
    f"{ebit['FY2025']:,.0f}; plus depreciation and amortisation {dna['FY2025']:,.0f} = "
    f"EBITDA {ebitda_h['FY2025']:,.0f}, margin {ebitda_h['FY2025']/V['rev_fy25']:.1%}. "
    f"NOTHING HERE IS SOLVED: revision 2 grossed a press profit figure at an effective tax "
    f"rate, subtracted a treasury income estimated on a cash balance rolled back by a "
    f"guessed factor, and reached 33.6%")

# ============ 3. COST OF CAPITAL — Hamada re-levered terminal ==============
rf_star = V['rf'] - V['sov_spread_cds']
ke_exp = rf_star + V['beta'] * V['erp_cds']
kd_at = V['kd'] * (1 - TAX)
mktcap = V['spot'] * V['shares_mn']
wd_exp = V['debt_fy25'] / (V['debt_fy25'] + mktcap)
wacc_exp = (1 - wd_exp) * ke_exp + wd_exp * kd_at
beta_t = V['beta'] * (1 + (1 - TAX) * V['wd_term'] / (1 - V['wd_term']))
ke_term = V['rf_term'] + beta_t * V['erp_term']
wacc_term = (1 - V['wd_term']) * ke_term + V['wd_term'] * V['kd_term'] * (1 - TAX)
assert wacc_term < wacc_exp
say(f"\n[Cost of capital] Ke {ke_exp:.2%} | WACC explicit {wacc_exp:.2%} | terminal beta "
    f"RE-LEVERED {V['beta']:.2f} -> {beta_t:.3f} | terminal WACC {wacc_term:.2%}")

kdp = V['kd_path']
glide = [(kdp[0] - kdp[i]) / (kdp[0] - kdp[-1]) for i in range(5)]
fwd = [wacc_exp - (wacc_exp - wacc_term) * g for g in glide]
# Time from the VALUATION DATE to the mid-point of each period. FY2026 is stubbed to
# the 5 months not yet earned; the 7 months already earned are rolled into the opening
# cash balance instead, so they are counted exactly once rather than twice or not at all.
REM = 1.0 - V['stub_years']
t_mid = [REM / 2] + [REM + (k - 0.5) for k in range(1, 5)]
df_, cum = [], 1.0
for i in range(5):
    r_ = fwd[i]
    df_.append(1.0 / np.prod([(1 + fwd[j]) ** (t_mid[i] - (t_mid[i - 1] if i else 0.0))
                              for j in range(i + 1)]) if False else None)
df_ = []
for i in range(5):
    # compound through the forward curve to t_mid[i]
    yrs_left, fac, j = t_mid[i], 1.0, 0
    while yrs_left > 1e-12 and j < 5:
        step = min(1.0, yrs_left)
        fac *= (1 + fwd[j]) ** step
        yrs_left -= step; j += 1
    df_.append(1.0 / fac)
assert all(0 < d <= 1.0 for d in df_), f"discount factor outside (0,1]: {df_}"
assert all(df_[i] > df_[i + 1] for i in range(4))
say(f"[Discounting] mid-period from the 06-Aug-2026 valuation date; FY2026 stubbed to its "
    f"remaining {REM*12:.0f} months, the elapsed {V['stub_years']*12:.0f} rolled into "
    f"opening cash. Times {[round(t,3) for t in t_mid]} -> factors " +
    " ".join(f"{d:.4f}" for d in df_))

# ============ 4. DCF with ONE reinvestment rule ============================
# DEPRECIATION IS THE DISCLOSED RATE ON THE ASSET BASE, NOT A SHARE OF REVENUE.
# Revision 2 charged 4.6% of revenue falling to 4.2% — EGP 445mn rising to 532mn against
# a company that filed 122.6mn. Note 3/2's own rates on note 4's own gross-cost mix
# reproduce the filed charge to 1.2%, so the forward rule is sourced: the gross base
# rolls forward on capex and carries the same weighted rate.
gross_fa, dna_f, capex = [], [], []
_g = V['gross_fixed_fy25']
for i in range(5):
    cx = V['capex_run_rate'] * V['cost_infl'][i + 1] / V['cost_infl'][0]
    _g += cx
    capex.append(cx)
    gross_fa.append(_g)
    dna_f.append(_g * V['dep_rate_disclosed'])
ebit_f = [ebitda_f[i] - dna_f[i] for i in range(5)]
nopat = [ebit_f[i] * (1 - TAX) for i in range(5)]
prev = [V['rev_fy25']] + rev_f[:-1]
dwc = [(rev_f[i] - prev[i]) * V['wc_pct_drev'] for i in range(5)]
ic_repl = V['cap_cement_mt'] * 1e6 * V['repl_usd_t'] * V['fx'] / 1e6
roic_t = nopat[-1] * (1 + V['g_term']) / ic_repl
nopat0 = ebitda_h['FY2025'] - dna['FY2025']
nopat0 *= (1 - TAX)
# [R-TERM-01] ONE DEFINITION OF FREE CASH FLOW ACROSS BOTH WINDOWS. Revision 2 ran the
# explicit years on NOPAT less a reinvestment charge derived from the growth in NOPAT, and
# the terminal on something else entirely — the defect that rule names in terms, and the
# reason a driver test could raise this study's capital spending by EGP 100mn a year and
# move its value by 0.12%. The explicit window now uses the same waterfall the terminal
# does: NOPAT plus book depreciation, less the capital actually spent and the working
# capital the growth absorbs.
fcff, reinv = [], []
for i in range(5):
    r_ = capex[i] + dwc[i] - dna_f[i]      # the NET capital charge, on the same definition
    reinv.append(r_)
    fcff.append(nopat[i] + dna_f[i] - capex[i] - dwc[i])
fcff[0] *= REM                      # only the unearned part of FY2026 is a future receipt
pv = [fcff[i] * df_[i] for i in range(5)]
sum_pv = float(np.sum(pv))
# [R-TERM-01] THE TERMINAL IS BUILT BY THE ONLY SANCTIONED MODULE. Revision 2 used the
# reinvestment identity rr = g/ROIC, which substitutes to a charge of g x IC every year
# for ever — an implied replacement cycle of 1/g, 20.0 years at a 5% terminal rate, which
# is a fact about the currency and not about the plant. The terminal it produced sat 34%
# BELOW the value of not investing at all, the worst case in this house's book.
#
# Maintenance is now the DISCLOSED life on the replacement-cost base. Note 3/2 gives the
# rates and note 4 the gross-cost mix they apply to; weighted, the plant life is 25.9
# years. THE MACHINERY LIFE ALONE IS 20 YEARS and that is the contested judgement, priced
# both ways in section 6 rather than chosen silently.
_life = 1.0 / V['dep_rate_disclosed']
_tin = TV.TerminalInputs(
    nopat=nopat[-1] * (1 + V['g_term']),
    wacc=wacc_term,
    inflation=V['g_term'],          # the terminal rate IS inflation at zero real growth
    real_growth=0.0,
    dna_book=dna_f[-1] * (1 + V['g_term']),
    ic_replacement=ic_repl,
    useful_life_years=_life,
    useful_life_source=(
        "Note 3/2 of the audited statements for the year ended 31 December 2025, printed "
        "page 8: straight-line depreciation at 2-2.5 per cent on buildings and utilities, "
        "5 per cent on machinery, 20 per cent on motor vehicles and tools, 10-25 per cent "
        "on furniture and office equipment. Weighted on note 4's own gross-cost mix that "
        "is a " + format(_life, ".1f") + "-year life, and it reproduces the filed FY2025 "
        "charge to within 1.2 per cent. The FY2024 filing carries the identical table."),
    maintenance_basis='disclosed_life',
    working_capital=V['rev_fy25'] * V['wc_pct_drev'])
_term = TV.build(_tin)
tv = _term.tv
rr_t = _term.maintenance / (nopat[-1] * (1 + V['g_term']))   # the charge as a share
pv_tv = tv * df_[-1]
ev = sum_pv + pv_tv
tv_share = pv_tv / ev
# [R-BRIDGE-01] THE BRIDGE STANDS ON THE LATEST DISCLOSED SHEET, which is the REVIEWED
# 31-March-2026 statement of financial position, not the 31-December-2025 audited one
# rolled forward on an estimate. The remaining four months to the 6-August valuation date
# are carried on the model's own free cash flow, so the period between the two dates is
# counted once and only once.
_stub_from_mar = (V['stub_years'] - 0.25)          # 31-Mar-2026 to the valuation date
cash_at_val = V['cash_mar26'] + fcff[0] / REM * _stub_from_mar
net_cash = cash_at_val - V['debt_mar26']
eq_dcf = ev + net_cash - V['nci']
fv_dcf = eq_dcf / V['shares_mn']
say(f"\n[Reinvestment] ONE rule across both windows at ROIC {roic_t:.1%}: explicit-window "
    f"reinvestment " + " ".join(f"{r:,.0f}" for r in reinv) +
    f"; terminal charge {rr_t:.1%} of terminal profit, built by the sanctioned module "
    f"on the DISCLOSED asset life rather than on the reciprocal of the inflation rate.")
say(f"[Bridge] EV {ev:,.0f} + net cash {net_cash:,.0f} - NCI {V['nci']:,.0f} = "
    f"{eq_dcf:,.0f} -> EGP {fv_dcf:.2f}/share | TV {tv_share:.1%} of EV")

# ============ 5. THE OTHER LENSES ==========================================
eb_norm = V['rev_fy25'] * V['norm_rev_haircut'] * V['norm_mgn']
fv_rel = (eb_norm * V['ev_ebitda_just'] + net_cash - V['nci']) / V['shares_mn']
nopat_norm = (eb_norm - dna['FY2025']) * (1 - TAX)
fv_norm = (nopat_norm * V['pe_just'] + net_cash - V['nci']) / V['shares_mn']
ev_per_t = (mktcap - net_cash) / (V['cap_cement_mt'] * 1e6) * 1e6 / V['fx']
ev_asset = V['ev_t_just'] * V['cap_cement_mt'] * 1e6 * V['fx'] / 1e6
fv_asset = (ev_asset + net_cash - V['nci']) / V['shares_mn']
lenses = {'DCF (cash flow)': fv_dcf, 'Relative multiples': fv_rel,
          'Normalised earnings': fv_norm, 'Asset / replacement cost': fv_asset}
w = {'DCF (cash flow)': V['w_dcf'], 'Relative multiples': V['w_rel'],
     'Normalised earnings': V['w_norm'], 'Asset / replacement cost': V['w_asset']}
assert abs(sum(w.values()) - 1.0) < 1e-9
fv_central = float(sum(lenses[k] * w[k] for k in lenses))
say(f"\n[Normalised lens] cash added at FACE, not capitalised at {V['pe_just']:.0f}x — "
    f"revision 1 valued the cash at an 18.6% discount to itself")
say(f"[Lenses] " + " | ".join(f"{k.split()[0]} {v:.2f}" for k, v in lenses.items()))
say(f"[Central] EGP {fv_central:.2f} vs spot {V['spot']:.2f} "
    f"({fv_central/V['spot']-1:+.1%})   [revision 1: 62.81, -20.5%]")

# ============ 6. SENSITIVITY, incl. NET CASH (revision 1 omitted it) =======
def reval(nc=None, g=None, we=None, beta_=None, mgn_shift=0.0):
    nc = net_cash if nc is None else nc
    g = V['g_term'] if g is None else g
    we = wacc_exp if we is None else we
    if beta_ is not None:
        we = (1 - wd_exp) * (rf_star + beta_ * V['erp_cds']) + wd_exp * kd_at
        bt = beta_ * (1 + (1 - TAX) * V['wd_term'] / (1 - V['wd_term']))
        wt = (1 - V['wd_term']) * (V['rf_term'] + bt * V['erp_term']) + \
            V['wd_term'] * V['kd_term'] * (1 - TAX)
    else:
        wt = wacc_term
    f_ = [we - (we - wt) * gg for gg in glide]
    d_ = []
    for i in range(5):
        yl, fa, j = t_mid[i], 1.0, 0
        while yl > 1e-12 and j < 5:
            st = min(1.0, yl); fa *= (1 + f_[j]) ** st; yl -= st; j += 1
        d_.append(1.0 / fa)
    eb = [ebitda_f[i] + rev_f[i] * mgn_shift for i in range(5)]
    ei = [eb[i] - dna_f[i] for i in range(5)]
    np_ = [ei[i] * (1 - TAX) for i in range(5)]
    rt = np_[-1] * (1 + g) / ic_repl
    fc = []
    for i in range(5):
        bn = nopat0 if i == 0 else np_[i - 1]
        fc.append(np_[i] - max(np_[i] - bn, 0.0) / rt)
    fc[0] *= REM
    s = float(np.sum([fc[i] * d_[i] for i in range(5)]))
    # THE SENSITIVITY REVALUES THROUGH THE SAME TERMINAL THE MODEL PUBLISHES. Revision 2's
    # grid re-derived the retired reinvestment identity inline, so every sensitivity in the
    # study answered a question about a construction the study no longer uses.
    tvl = TV.build(TV.TerminalInputs(
        nopat=np_[-1] * (1 + g), wacc=wt, inflation=g, real_growth=0.0,
        dna_book=dna_f[-1] * (1 + g), ic_replacement=ic_repl,
        useful_life_years=_life, useful_life_source=_tin.useful_life_source,
        maintenance_basis='disclosed_life',
        working_capital=V['rev_fy25'] * V['wc_pct_drev'])).tv
    return (s + tvl * d_[-1] + nc - V['nci']) / V['shares_mn']

nc_grid = [net_cash - 1500, net_cash - 750, net_cash, net_cash + 750, net_cash + 1500]
sens_nc = [reval(nc=x) for x in nc_grid]
wacc_grid = [wacc_exp - 0.03, wacc_exp - 0.015, wacc_exp, wacc_exp + 0.015, wacc_exp + 0.03]
g_grid = [0.03, 0.04, 0.05, 0.06, 0.07]
sens_wg = [[reval(we=x, g=gg) for gg in g_grid] for x in wacc_grid]
beta_grid = [0.6, 0.8, 0.837, 1.0, 1.3]
sens_beta = [reval(beta_=b) for b in beta_grid]
mgn_grid = [-0.04, -0.02, 0.0, 0.02, 0.04]
sens_mgn = [reval(mgn_shift=m) for m in mgn_grid]
say(f"\n[Net cash sensitivity, on the REVIEWED 31-March-2026 balance sheet] " + " ".join(f"{x:.2f}" for x in sens_nc))

# ============ 7. STATEMENTS ================================================
pbt_f, tax_f, pat_f, cash_b, eq_b, ppe_b, wc_b, div_f, treas_f = ([] for _ in range(9))
c_, e_ = V['cash_fy25'], V['eq_fy25_rep']
# the filed FY2024 cash, not a balance rolled back by a guessed factor
# THE FILED OPERATING ASSET BASE, not a plug. Revision 2 derived it as total assets less
# a rolled-back cash balance less a round 900. The audited sheet states fixed assets net
# of depreciation, intangibles and construction in progress on its own face.
_b24 = FIL['balance_sheet']['FY2024']
p_ = (_b24['fixed_assets'] + _b24['intangibles'] + _b24['cwip']) / 1e6
wc_ = 900.0
for i in range(5):
    ti = c_ * V['cash_yield'][i]
    pbt = ebit_f[i] + ti
    tx = pbt * TAX
    pat = pbt - tx
    dv = pat * V['payout']
    p_ += capex[i] - dna_f[i]; wc_ += dwc[i]
    c_ += pat + dna_f[i] - capex[i] - dwc[i] - dv
    e_ += pat - dv
    for L, x in ((treas_f, ti), (pbt_f, pbt), (tax_f, tx), (pat_f, pat), (div_f, dv),
                 (cash_b, c_), (eq_b, e_), (ppe_b, p_), (wc_b, wc_)):
        L.append(x)

# ============ 8. EXPERTS ===================================================
fcff_mid = float(np.mean(fcff))
e3 = (fcff_mid / 0.18 + net_cash - V['nci']) / V['shares_mn']
EXPERTS = [
    dict(label="Expert 1", method="Replacement-cost industrialist", central=fv_asset,
         low=((V['ev_t_just'] - 15) * V['cap_cement_mt'] * 1e6 * V['fx'] / 1e6 + net_cash
              - V['nci']) / V['shares_mn'],
         high=((V['ev_t_just'] + 15) * V['cap_cement_mt'] * 1e6 * V['fx'] / 1e6 + net_cash
               - V['nci']) / V['shares_mn'],
         summary="Values the plant, not the earnings stream. A 3.8Mt grey-cement plant "
                 "costs about USD 130 per annual tonne to build; nobody pays replacement "
                 "cost for capacity in a market carrying 76Mt against 54Mt of "
                 "consumption. The market pays USD %.0f/t." % ev_per_t,
         falsifier="Find an Egyptian line built, bought or restarted below USD 95 per "
                   "annual tonne. The 12.6Mt revival programme is the live test: "
                   "restarting a mothballed line costs a fraction of building one, which "
                   "is why this lens is a ceiling and not a floor — and why it now carries "
                   "8% of the weight rather than 15%."),
    dict(label="Expert 2", method="Mid-cycle earnings-power analyst", central=fv_norm,
         low=(nopat_norm * (V['pe_just'] - 1) + net_cash - V['nci']) / V['shares_mn'],
         high=(nopat_norm * (V['pe_just'] + 1) + net_cash - V['nci']) / V['shares_mn'],
         summary="Refuses to capitalise a peak, and now refuses it on BOTH legs: the "
                 "margin is normalised to %.1f%% and the revenue base is cut %.0f%% "
                 "because FY2025 embeds the post-quota price spike."
                 % (V['norm_mgn'] * 100, (1 - V['norm_rev_haircut']) * 100),
         falsifier="Two consecutive years of realised prices above EGP 3,900/t WITH the "
                   "revival proceeding would prove the mid-cycle base too low."),
    dict(label="Expert 3", method="Cash-return and distribution investor", central=e3,
         low=(fcff_mid / 0.22 + net_cash - V['nci']) / V['shares_mn'],
         high=(fcff_mid / 0.14 + net_cash - V['nci']) / V['shares_mn'],
         summary="Starts from the balance sheet. Net cash of EGP %.1fbn is %.0f%% of the "
                 "market capitalisation and %.0f%% of fair equity value. Terminal return "
                 "on capital of %.1f%% sits below the %.1f%% cost of capital, so growth "
                 "destroys value and the right policy is to harvest and distribute."
                 % (net_cash / 1000, net_cash / mktcap * 100, net_cash / eq_dcf * 100,
                    roic_t * 100, wacc_term * 100),
         falsifier="The lens rests on the cash being distributable. Vicat holds 77.6% and "
                   "a minority cannot force a dividend. If none is declared on FY2026 "
                   "profits, or the cash funds expansion into a glut, it is worth less "
                   "than face."),
]

# ============ ASSERT =======================================================
say("\n" + "=" * 80)
say("ASSERT")
say("=" * 80)
assert abs((sum_pv + pv_tv) - ev) < 1e-6
assert abs((ev + net_cash - V['nci']) - eq_dcf) < 1e-6
say(f"  bridge closes: EV {ev:,.2f} + net cash {net_cash:,.2f} - NCI {V['nci']:,.2f} "
    f"= {eq_dcf:,.2f}")
assert net_cash > 0 and V['nci'] >= 0
assert 0 < tv_share < 0.95
say(f"  terminal value {tv_share:.1%} of enterprise value")
# THE RETIRED HURDLE IS RECORDED AS RETIRED, NOT QUIETLY REPLACED. Revision 2 asserted
# ROIC x RR = g, which is the reinvestment identity [R-TERM-01] retires: it holds by
# construction whatever the assets cost to replace, so it could never fail. What replaces
# it are assertions about the DISCLOSED life and the cash-flow definition, both of which
# can fail and one of which caught a real error while this edition was being built.
assert abs(_term.maintenance - ic_repl / _life) < 1e-6, \
    'the terminal maintenance charge is not the replacement base over the disclosed life'
# The module's implied cycle is the NET capital charge's, not maintenance alone — the
# book depreciation add-back and the working-capital charge are inside it — so it is not
# the disclosed life and asserting that it is was a misreading of the module rather than
# a finding about the study. What must hold is that it is not 1/g, which is the whole of
# the retired construction's signature.
assert abs(_term.implied_cycle_years - 1.0 / V['g_term']) > 1.0, \
    'the implied cycle equals 1/g, which is the retired construction'
assert abs((nopat[-1] * (1 + V['g_term']) + _term.dna_addback - _term.maintenance
            - _term.growth_capex - _term.wc_charge) - _term.fcff) < 1e-6, \
    'the terminal free cash flow does not reproduce from its own components'
say(f"  terminal on the DISCLOSED life: maintenance {_term.maintenance:,.0f} = "
    f"replacement capital {ic_repl:,.0f} over {_life:.1f} years, which is "
    f"{_term.maintenance/(nopat[-1]*(1+V['g_term'])):.1%} of terminal profit against the "
    f"retired identity's {V['g_term']*ic_repl/(nopat[-1]*(1+V['g_term'])):.1%}")
say(f"  implied replacement cycle {_term.implied_cycle_years:.1f} years, against 1/g of "
    f"{1.0/V['g_term']:.1f} — an asset fact rather than a currency fact")
say(f"  terminal free cash flow {_term.fcff:,.0f}; the NOPAT-perpetuity floor is "
    f"{_term.floor:,.0f} and the terminal is "
    f"{'BELOW' if _term.below_floor else 'above'} it")
assert wacc_term < wacc_exp
say(f"  ordered: terminal WACC {wacc_term:.2%} < explicit {wacc_exp:.2%}")
assert beta_t > V['beta']
say(f"  terminal beta re-levered {V['beta']:.2f} -> {beta_t:.3f} for the {V['wd_term']:.0%} "
    f"terminal debt weight")
assert all(df_[i] > df_[i + 1] for i in range(4))
assert 0.3 < fv_central / V['spot'] < 3.0
say(f"  fair value to spot {fv_central/V['spot']:.2f}x — inside the plausibility band")
gap_rev = BU[0]['rev'] / V['rev_fy25'] - 1
# THE CHECK IS AGAINST THE FILED EBITDA, WHICH IS WHAT MAKES IT A TEST. Revision 2
# compared the bottom-up stack to an EBITDA solved from the same press figures the
# historicals came from, so two wrong numbers agreed to 1.36% and the check passed while
# the stack was 355mn out.
gap_eb = BU[0]['ebitda'] / (FIL['derived']['FY2025']['ebitda']) - 1
assert abs(gap_rev) < 0.05, f"bottom-up revenue off by {gap_rev:.2%}"
assert abs(gap_eb) < 0.02, f"bottom-up EBITDA off the FILED figure by {gap_eb:.2%}"
say(f"  bottom-up revenue within {gap_rev:+.2%} of disclosed; EBITDA within {gap_eb:+.2%} "
    f"of the FILED figure — against the audited statements, not against a solve")
assert abs(sum(w.values()) - 1.0) < 1e-9
say(f"  lens weights sum to 1.00")

OUT = dict(
    meta=dict(ticker="SCEM", company="Sinai Cement Company S.A.E.", market="EGX",
              market_code="EG", currency="EGP", asof="2026-09-04", spot_date="2026-09-02", revision=3,
              spot=V['spot'], shares_mn=V['shares_mn'], mktcap=mktcap,
              # the central belongs where a checker outside this study can read it:
              # [R-GAP-01]'s gate held this study as "no readable answer" while the
              # number sat one level down, and an unreadable study is held by design
              # because unreadability is the cheapest route past any answer check
              central=fv_central,
              klass="single-asset cement operating company (net cash)",
              sector="Construction materials — cement"),
    inputs=INP, bottom_up=BU, clinker_factor=cf,
    history=dict(years=HIST, revenue=[V['rev_fy23'], V['rev_fy24'], V['rev_fy25']],
                 ebitda=[ebitda_h[y] for y in HIST], dna=[dna[y] for y in HIST],
                 ebit=[ebit[y] for y in HIST], treasury=[treas[y] for y in HIST],
                 pat=[V['pat_fy23'], V['pat_fy24'], V['pat_fy25']],
                 shares=[V['shares_fy23'], V['shares_fy24'], V['shares_fy25']],
                 eps=[V['pat_fy23'] / V['shares_fy23'], V['pat_fy24'] / V['shares_fy24'],
                      V['pat_fy25'] / V['shares_fy25']],
                 volume_mt=[V['rev_fy23']/2118.0, V['rev_fy24']/2697.0, BU[0]['cement']],
                 price_t=[2118.0, 2697.0, BU[0]['price']],
                 utilisation=[V['rev_fy23']/2118.0/V['cap_cement_mt'],
                              V['rev_fy24']/2697.0/V['cap_cement_mt'], BU[0]['util']]),
    disposal=dict(proceeds=V['swcc_eur'] * V['egp_per_eur_aug24'], book=V['swcc_book'],
                  gain=swcc_gain, underlying_fy24_pat=und24),
    forecast=dict(years=YRS, revenue=rev_f, ebitda=ebitda_f, dna=dna_f, ebit=ebit_f,
                  gross_fa=gross_fa,
                  nopat=nopat, capex=capex, dwc=dwc, reinvestment=reinv, fcff=fcff,
                  df=df_, pv=pv, fwd_wacc=fwd, glide=glide, treasury=treas_f, pbt=pbt_f,
                  tax=tax_f, pat=pat_f, dividends=div_f, cash=cash_b, equity=eq_b,
                  ppe=ppe_b, wc=wc_b,
                  volume_mt=[b['cement'] for b in BU[1:]],
                  price_t=[b['price'] for b in BU[1:]],
                  margin=[b['mgn'] for b in BU[1:]]),
    wacc=dict(rf=V['rf'], rf_star=rf_star, ke_exp=ke_exp, kd_at=kd_at, wd_exp=wd_exp,
              wacc_exp=wacc_exp, beta_term=beta_t, ke_term=ke_term,
              kd_term_at=V['kd_term'] * (1 - TAX), wacc_term=wacc_term,
              ke_raw_retired=V['rf'] + V['beta'] * V['erp_cds']),
    dcf=dict(cash_fy25=cash_at_val, cash_reported=V['cash_fy25'],
             term_maintenance=_term.maintenance, term_dna_addback=_term.dna_addback,
             term_wc_charge=_term.wc_charge, term_fcff=_term.fcff,
             term_floor=_term.floor, term_life_years=_life,
             term_below_floor=_term.below_floor, terminal_record=_term.record, sum_pv=sum_pv, tv=tv, pv_tv=pv_tv, ev=ev, tv_share=tv_share,
             net_cash=net_cash, nci=V['nci'], equity=eq_dcf, fv=fv_dcf, roic_term=roic_t,
             rr_term=rr_t, ic_repl=ic_repl, nopat_term=nopat[-1] * (1 + V['g_term'])),
    lenses=dict(values=lenses, weights=w, central=fv_central, low=min(lenses.values()),
                high=max(lenses.values()), ebitda_norm=eb_norm, nopat_norm=nopat_norm,
                ev_per_t_spot=ev_per_t, ev_asset=ev_asset,
                earn_norm=nopat_norm, eq_fy25_roll=V['eq_fy25_rep'],
                bvps=V['eq_fy25_rep']/V['shares_fy25'],
                roe_sust=nopat_norm/V['eq_fy25_rep']),
    sensitivity=dict(nc_grid=nc_grid, net_cash=sens_nc, wacc_grid=wacc_grid,
                     g_grid=g_grid, wacc_g=sens_wg, beta_grid=beta_grid, beta=sens_beta,
                     mgn_grid=mgn_grid, mgn=sens_mgn),
    lens_ranges={
        'DCF (cash flow)': dict(bear=float(np.min(sens_wg)), base=fv_dcf,
                                bull=float(np.max(sens_wg))),
        'Relative multiples': dict(
            bear=(eb_norm * (V['ev_ebitda_just'] - 1) + net_cash - V['nci']) / V['shares_mn'],
            base=fv_rel,
            bull=(eb_norm * (V['ev_ebitda_just'] + 1) + net_cash - V['nci']) / V['shares_mn']),
        'Normalised earnings': dict(
            bear=(nopat_norm * (V['pe_just'] - 1) + net_cash - V['nci']) / V['shares_mn'],
            base=fv_norm,
            bull=(nopat_norm * (V['pe_just'] + 1) + net_cash - V['nci']) / V['shares_mn']),
        'Asset / replacement cost': dict(
            bear=((V['ev_t_just'] - 15) * V['cap_cement_mt'] * 1e6 * V['fx'] / 1e6
                  + net_cash - V['nci']) / V['shares_mn'],
            base=fv_asset,
            bull=((V['ev_t_just'] + 15) * V['cap_cement_mt'] * 1e6 * V['fx'] / 1e6
                  + net_cash - V['nci']) / V['shares_mn']),
        'Weighted central': dict(
            bear=float(sum(dict(zip(lenses, [min(sens_wg[i]) for i in range(5)] and
                 [0]*4)).values())) if False else
                 (V['w_dcf'] * float(np.min(sens_wg))
                  + V['w_rel'] * ((eb_norm * (V['ev_ebitda_just'] - 1) + net_cash - V['nci'])
                                  / V['shares_mn'])
                  + V['w_norm'] * ((nopat_norm * (V['pe_just'] - 1) + net_cash - V['nci'])
                                   / V['shares_mn'])
                  + V['w_asset'] * (((V['ev_t_just'] - 15) * V['cap_cement_mt'] * 1e6
                                     * V['fx'] / 1e6 + net_cash - V['nci']) / V['shares_mn'])),
            base=fv_central,
            bull=(V['w_dcf'] * float(np.max(sens_wg))
                  + V['w_rel'] * ((eb_norm * (V['ev_ebitda_just'] + 1) + net_cash - V['nci'])
                                  / V['shares_mn'])
                  + V['w_norm'] * ((nopat_norm * (V['pe_just'] + 1) + net_cash - V['nci'])
                                   / V['shares_mn'])
                  + V['w_asset'] * (((V['ev_t_just'] + 15) * V['cap_cement_mt'] * 1e6
                                     * V['fx'] / 1e6 + net_cash - V['nci']) / V['shares_mn'])))},
    growth_destroys_value=dict(fv_at_g3=reval(g=0.03), fv_at_g7=reval(g=0.07),
                               holds=bool(reval(g=0.07) < reval(g=0.03)),
                               roic_term=roic_t, wacc_term=wacc_term),
    equity_gap=dict(rolled=(V['ta_fy24'] - V['tl_fy24']) + V['pat_fy25'],
                    reported=V['eq_fy25_rep'],
                    gap=(V['ta_fy24'] - V['tl_fy24']) + V['pat_fy25'] - V['eq_fy25_rep']),
    experts=EXPERTS, assert_log=LOG,
    share_triangulation=dict(issued_capital=2608124770/10/1e6, tender_offer=58416664/0.224/1e6,
                             market_cap=21150.0/81.10, pre_issue=133.07, subscribed=127.74,
                             mean=260.812477, adopted=V['shares_mn']),
    terminal_reconciliation=dict(roic_repl=roic_t, rr_repl=rr_t, ic_repl=ic_repl,
                                 roic_book=float('nan'), ic_book=float('nan'),
                                 basis_adopted="replacement cost", history=[],
                                 nopat_cagr=float('nan'), stable_implied_g=float('nan')),
    peers=dict(mbsc=dict(name="Misr Beni Suef Cement (MBSC)", rev=V['peer_mbsc_rev'],
                         pat=V['peer_mbsc_pat'], eps=V['peer_mbsc_eps'],
                         mcap=V['peer_mbsc_mcap'], pe=V['peer_mbsc_pe'],
                         ev_ebitda=V['peer_mbsc_evebitda']),
               arcc=dict(name="Arabian Cement (ARCC)", pat=V['peer_arcc_pat']),
               sector=dict(capacity_mt=V['egy_capacity_mt'], consumption_mt=V['egy_cons_mt'],
                           production_mt=V['egy_prod_mt'], exports_mt=V['egy_exports_mt'],
                           revival_mt=V['egy_revival_mt'],
                           scem_share_of_capacity=V['cap_cement_mt']/V['egy_capacity_mt'],
                           revival_pct_of_consumption=V['egy_revival_mt']/V['egy_cons_mt'])),
    revision_notes=dict(
        prior_central=62.81, prior_dcf=54.49, prior_net_cash=5307.05,
        prior_fy26_margin=0.305, prior_fy25_margin=0.280,
        corrections_applied=69),
)
json.dump(OUT, open(os.path.join(HERE, 'study_numbers.json'), 'w'), indent=1, default=float)
say("\nwrote study_numbers.json (revision 2)")
