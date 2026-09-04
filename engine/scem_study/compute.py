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
import macro_path as MP       # [R-MACRO-01] the ONE house path; a study carries no inflation of its own

# [R-MACRO-01] EVERY INFLATION-CLASS INPUT IS DERIVED HERE, FROM THE HOUSE LADDER, AND
# NONE OF THEM IS TYPED. Revision 3 carried a cost index of 14.0/11.0/7.9/6.2/5.5 per
# cent against a house ladder of 16.0/12.0/9.0/7.5/7.0, a spot of 49.80 against the
# house 50.25 for the SAME 6-August quote, and a terminal growth of 5% against a
# terminal risk-free rate embedding 7% -- a perpetual real decline of two points that
# nothing in the study disclosed. The pound's forward path was derived from the study's
# own ladder rather than the house one, so conforming the ladder moves the currency too.
_PATH = MP.load('EG')
_YRS = [2026, 2027, 2028, 2029, 2030]
_LADDER = [_PATH.inflation(y) for y in _YRS]                 # the house calendar ladder
_CUM = [1.0]
for _r in _LADDER:
    _CUM.append(_CUM[-1] * (1.0 + _r))                       # cumulative, FY2025 = 1.000
_FXSPOT = _PATH.fx_spot
_FXPATH = [_FXSPOT] + list(_PATH.fx_path(5))                 # relative PPP, derived
_GTERM = _PATH.terminal_growth(0.0)                          # zero real, DERIVED

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
        "rules of thumb summing to EGP 2,553.7mn, which is " +
        format(100 * (2553.7 / 3592.466202 - 1), '.1f') + " per cent BELOW the disclosed "
        "line, the disclosed line being " +
        format(100 * (3592.466202 / 2553.7 - 1), '.1f') + " per cent above the assumption",
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
    price_dom_egp_t=I([3503.0 * c for c in _CUM],
                      "Domestic realised price ex-works. FY2025 is the level the disclosed "
                      "revenue implies given the volume build \u2014 13.9% below the ~EGP "
                      "4,070/t market average, which is what an ex-works price net of "
                      "freight and rebates looks like. THE REAL SPREAD PER TONNE IS THEN "
                      "HELD FLAT: price escalates on the HOUSE inflation ladder at zero "
                      "real growth [R-MACRO-01], the same index the domestic cost lines "
                      "carry, so the margin is an OUTPUT of the two and neither side "
                      "carries an inflation number of its own. Revision 3 typed the path, "
                      "and a typed nominal rate is unfalsifiable \u2014 nobody can tell "
                      "whether 14.0% meant inflation plus nothing or inflation minus two. "
                      "The path before that grew nominal prices well below the domestic "
                      "cost path this same model escalates costs on, and the register "
                      "described it as \'a REAL decline against CBE inflation\' while "
                      "sourcing no mechanism for it. [R-ANCHOR-01] refuses that mechanism "
                      "on the company\'s own measurement: cost per unit of revenue FELL "
                      "across the reviewed quarter pair and the audited year between them, "
                      "where the forecast needed it to rise, and a mechanism contradicted "
                      "by the filings is the assumption wearing one. The 12.6Mt of dormant "
                      "Egyptian capacity queuing to restart is a real risk to price; it "
                      "belongs in the bear case and the sensitivity grid, which carry it, "
                      "not in the base path", "2026-09-04", "House"),
    price_exp_usd_t=I([48.0, 47.0, 46.0, 45.5, 45.0, 45.0],
                      "Export FOB per tonne, declining because the EU carbon border "
                      "mechanism raises the landed cost of Egyptian cement into Europe "
                      "from 2026", "2026-01-01", "Industry"),
    fx=I(_FXSPOT, "USD/EGP spot, from the house macro path [R-MACRO-01] and not from this "
         "study. Revision 3 carried 49.80 for the 6-August-2026 quote and the house path "
         "carries 50.25 for the SAME quote on the same date \u2014 two numbers for one "
         "fact, which is the defect that rule was adopted on. The house figure governs",
         "2026-08-06", "Country"),
    fx_path=I(_FXPATH, "USD/EGP path, the HOUSE derived purchasing-power path "
              "[R-MACRO-01] \u2014 relative PPP on the house inflation ladder against "
              "long-run United States inflation, read from engine/macro_paths/EG.json and "
              "not computed here. Revision 3 derived the same identity from THIS STUDY\'s "
              "own ladder, which was two points a year below the house one, so the pound "
              "slid more slowly than the house path says it does: one economy cannot have "
              "two inflations, and the currency is where that shows. Raises the EGP cost "
              "of imported fuel AND the EGP value of export revenue",
              "2026-09-02", "Country"),
    cost_infl=I(_CUM,
                "Cumulative local cost inflation index on the EGP cost lines, compounded "
                "from the HOUSE calendar ladder [R-MACRO-01] \u2014 16.0/12.0/9.0/7.5/7.0 "
                "per cent for 2026-2030, sourced to the Central Bank of Egypt\'s own "
                "baseline and its published glide to the target band. Revision 3 typed "
                "14.0/11.0/7.9/6.2/5.5, roughly two points a year below the house path, "
                "and no source in this study supported the gap",
                "2026-09-02", "Country"),

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
    rf=I(_PATH.sovereign_10y, "Egypt 10-year local-currency government yield, from the "
         "HOUSE macro path [R-MACRO-01] and not from this study. Revision 3 carried "
         "22.31% at a 21-July quote while the house path carries 23.00% at 6-August: one "
         "sovereign, one yield, and the later quote is the right one for a study struck "
         "in September. THE QUOTE IS OLDER THAN THE 14-DAY BOUND [R-COC-01] and is "
         "accepted deliberately with its age disclosed in the cost-of-capital record, "
         "rather than used quietly", _PATH.sovereign_asof, "Country"),
    sov_spread_cds=I(0.0340, "Egypt CDS-implied sovereign default spread, Damodaran "
                     "January-2026, CDS column. NETTED OUT of the local risk-free rate so "
                     "sovereign default risk is not charged twice. One reviewer called "
                     "this a manipulation; two others cleared it explicitly, and it is "
                     "Damodaran's own construction — the country premium in the ERP is "
                     "DERIVED from this same spread", "2026-01-05", "Country"),
    sov_spread_rating=I(0.0637, "Egypt RATING-implied sovereign default spread, "
                        "Damodaran January-2026, rating column. Published as the "
                        "alternative basis to the adopted CDS one, never mixed with it: "
                        "the spread netted out of the risk-free rate and the spread added "
                        "back through the premium must be the SAME basis or the sovereign "
                        "is counted one and a half times", "2026-01-05", "Country"),
    erp_rating=I(0.1394, "Damodaran Egypt, RATING-BASED, January-2026. The alternative "
                 "premium basis, published beside the adopted CDS one under [R-COC-01]. "
                 "Revision 1 cited 'Damodaran, Egypt row' without naming the variant, and "
                 "a checker following that citation lands here rather than on the 9.41% "
                 "actually used", "2026-01-05", "Country"),
    erp_cds=I(0.0941, "Damodaran Egypt, CDS-BASED, January-2026: mature-market 4.23% + "
              "3.40% x (9.71/6.37) = 9.4127%. Revision 1 cited 'Damodaran, Egypt row' "
              "without naming the variant; a checker following that citation lands on the "
              "rating-based 13.94%", "2026-01-05", "Country"),
    beta=I(1.00, "Adopted beta. The own-stock regression FAILS the usability gate "
           "(R-squared 0.038 against a 0.05 floor) though n=256 and SE 0.153 both pass. "
           "The lead-lag corrected estimate is 0.837 and its 90% interval contains 1.00. "
           "Rounding up to 1.00 COSTS 1.84% of the central; that price is now stated "
           "rather than left implicit", "2026-08-06", "House"),
    kd=I(0.0, "PLACEHOLDER — replaced below by the sovereign-plus-spread construction, "
         "because a marginal cost of debt is not a free-standing input once the "
         "sovereign it must sit above comes from the house path", "2026-09-04", "House"),
    kd_spread=I(0.0200, "Corporate credit spread over the local sovereign. THE ADOPTED "
                "COST OF DEBT IS THE SOVEREIGN PLUS THIS, and the sovereign comes from "
                "the house path, so the two cannot disagree. Revision 3 typed 21.50% "
                "against a sovereign of 22.31% IN THE SAME FILE — 81bp BELOW the "
                "government that taxes it, which [R-COC-01] refuses outright and which "
                "the gate found the hour this record was first committed. The audited "
                "statements disclose no rate on the EGP %s of borrowings, so the "
                "construction the protocol asks for is sovereign plus spread; 200bp is a "
                "STATED judgement and its price is 1 basis point of weighted cost of "
                "capital, because the book is 0.5%% of the capital structure",
                "2026-09-04", "House"),
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
    g_term=I(_GTERM, "Terminal growth, DERIVED as the house terminal inflation of 7.0% "
             "plus a STATED real growth of ZERO [R-MACRO-01]. Revision 3 held 5% against "
             "a terminal risk-free rate of 12.5% built on that same 7% inflation \u2014 a "
             "perpetual REAL DECLINE of about two points a year that nothing in the study "
             "disclosed and nothing supports. Real decline in perpetuity stays permitted "
             "and must be written down as the real number it is; this study assumes none",
             "2026-09-02", "Country"),
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
# [R-COC-01] A SAME-CURRENCY CORPORATE CANNOT BORROW BELOW ITS OWN SOVEREIGN. Derived
# here rather than typed, so the two can never drift apart again.
V['kd'] = V['rf'] + V['kd_spread']
INP['kd']['value'] = V['kd']
# [R-COC-01] THE GLIDE'S FRACTIONS ARE THE POLICY-RATE PATH'S OWN CUMULATIVE PROGRESS,
# so the front-loading is inherited from the central bank's easing calendar rather than
# being a second free parameter somebody typed. Revision 3 carried a hand-set kd ladder
# and the WACC glide inherited its shape from that.
_PP = list(_PATH.policy_path)
GLIDE_F = [(_PP[0] - x) / (_PP[0] - _PP[-1]) for x in _PP]
V['kd_path'] = [V['kd'] - (V['kd'] - V['kd_term']) * f for f in GLIDE_F]
INP['kd_path']['value'] = V['kd_path']
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


def build_bu(util=None):
    """The physical build, parameterised on KILN UTILISATION only.

    A contested judgement about the ramp is then priced through THIS construction
    rather than through a second copy of it, which is [R-ENF-03] applied inside a
    study: two implementations of one claim are two claims."""
    util = V['kiln_util'] if util is None else util
    BU = []
    for i in range(6):
        clk = V['cap_clinker_mt'] * util[i]
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
        BU.append(dict(clinker=clk, cement=cem, dom=dom, exp=exp, util=util[i],
                       rev=rev, price=rev / cem, c_mat=mat_t, c_dist=dist_t,
                       var_t=var_t, var=var_t * cem,
                       fixed=fixed, ebitda=eb, mgn=eb / rev))
    return BU


BU = build_bu()

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
# Hamada must start from an ASSET beta. Re-levering an already-levered beta levers it
# twice. Unlever at the OBSERVED structure first. On a book that is 0.5% of capital
# this moves the terminal beta in the fourth decimal, and it is corrected anyway:
# a construction that is only harmless because the input is small is still wrong,
# and the next study to copy it may not have a small input.
beta_u = V['beta'] / (1 + (1 - TAX) * wd_exp / (1 - wd_exp))
beta_t = beta_u * (1 + (1 - TAX) * V['wd_term'] / (1 - V['wd_term']))
ke_term = V['rf_term'] + beta_t * V['erp_term']
wacc_term = (1 - V['wd_term']) * ke_term + V['wd_term'] * V['kd_term'] * (1 - TAX)
assert wacc_term < wacc_exp
say(f"\n[Cost of capital] Ke {ke_exp:.2%} | WACC explicit {wacc_exp:.2%} | terminal beta "
    f"RE-LEVERED {V['beta']:.2f} -> {beta_t:.3f} | terminal WACC {wacc_term:.2%}")

glide = list(GLIDE_F)      # the easing calendar's own progress, not the debt ladder's
fwd = [wacc_exp - (wacc_exp - wacc_term) * g for g in glide]
# Time from the VALUATION DATE to the mid-point of each period. FY2026 is stubbed to
# the 5 months not yet earned; the 7 months already earned are rolled into the opening
# cash balance instead, so they are counted exactly once rather than twice or not at all.
REM = 1.0 - V['stub_years']
t_mid = [REM / 2] + [REM + (k - 0.5) for k in range(1, 5)]
# EACH FORWARD RATE OWNS A SLICE OF CALENDAR AND THE FACTORS DO NOT REPRODUCE WITHOUT
# THAT. The previous construction walked the rates in WHOLE-YEAR steps from t=0, so the
# whole 0.917 years to the FY2027 midpoint compounded at the FY2026 rate and the FY2030
# rate never entered any discount factor at all. On a path that FALLS from 28.26% to
# 19.01% that over-discounts every year after the first — the identical defect ARCC
# revision 3 carried, found there and not looked for here until now.
EDGES = [0.0, REM] + [REM + k for k in range(1, 5)]


def chain(f_, t):
    fa = 1.0
    for j_ in range(5):
        lo, hi = EDGES[j_], EDGES[j_ + 1]
        span = max(0.0, min(t, hi) - lo)
        if span > 0:
            fa *= (1 + f_[j_]) ** span
    return 1.0 / fa


def factors(f_):
    return [chain(f_, t) for t in t_mid]


df_ = factors(fwd)
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
# [R-TERM-01] THE EXPLICIT WINDOW CONVERGES ON THE TERMINAL'S OWN CAPITAL CHARGE, AND
# THE STEP AT THE BOUNDARY IS ZERO BY CONSTRUCTION. The company's own cash-flow
# statements show capital spending of EGP 120.8mn, 526.4mn and 262.4mn across FY2023-25,
# an average of 303.2mn. The terminal charges maintenance at CURRENT COST on the
# disclosed life, which is EGP 959mn a year in today's money. THE TWO DIFFER BY 3.2x AND
# THE REASON IS NOT THAT THE PLANT IS YOUNG: note 4 of the audited statements shows
# accumulated depreciation of EGP 1,875.0mn against a gross cost of 3,140.9mn — 59.7 per
# cent written down, MACHINERY 68.4 PER CENT — with EGP 379.4mn of assets fully
# depreciated AND STILL IN USE. Replacement cost is 7.9x the book cost this plant was
# built at, because it was built in pre-devaluation pounds.
#
# Holding the company's recent spend flat for five years while simultaneously running the
# kilns HARDER, from 71.0 per cent of clinker capacity to 79.1, is two assumptions that
# cannot both be true: a plant cannot be run harder and maintained less. So the charge
# GLIDES from the company's own disclosed run rate in FY2026 to the terminal's own
# current-cost maintenance by FY2030, and the explicit window ends exactly where the
# terminal begins. It costs EGP 5.16 a share, which is the price of the incoherence.
#
# The book depreciation base still rolls on the CASH actually spent, because that is what
# enters the accounts; the divergence between an EGP 3.1bn book base and an EGP 24.8bn
# replacement base is the finding rather than an error, and it is why book depreciation
# is never the maintenance charge.
_CONV_DEFAULT = [0.0, 0.25, 0.50, 0.75, 1.00]


def build_dcf(bu=None, life=None, repl_usd_t=None, conv=None, df_over=None):
    """Everything from the physical build to the value per share, in ONE place.

    The base case and every contested judgement run through this function, so a
    judgement priced both ways measures THE CHOICE and never the construction —
    the defect found on AMOC and registered as L-070. Each argument is one
    contested input; passing none reproduces the published figure exactly, and an
    assertion below proves it."""
    bu = BU if bu is None else bu
    rev_f_ = [b["rev"] for b in bu[1:]]
    ebitda_f_ = [b["ebitda"] for b in bu[1:]]
    df_l = df_ if df_over is None else df_over
    conv = _CONV_DEFAULT if conv is None else conv
    repl = V["repl_usd_t"] if repl_usd_t is None else repl_usd_t
    life_ = (1.0 / V["dep_rate_disclosed"]) if life is None else life
    ic_repl_pre = V['cap_cement_mt'] * 1e6 * repl * V['fx'] / 1e6
    gross_fa, dna_f, capex = [], [], []
    _g = V['gross_fixed_fy25']
    _maint_cc = ic_repl_pre / life_                                # today's money
    _CONV = conv
    for i in range(5):
        esc = V['cost_infl'][i + 1] / V['cost_infl'][0]
        own = V['capex_run_rate'] * esc
        cx = own + (_maint_cc * esc - own) * _CONV[i]
        _g += cx
        capex.append(cx)
        gross_fa.append(_g)
        dna_f.append(_g * V['dep_rate_disclosed'])
    ebit_f = [ebitda_f_[i] - dna_f[i] for i in range(5)]
    nopat = [ebit_f[i] * (1 - TAX) for i in range(5)]
    prev = [V['rev_fy25']] + rev_f_[:-1]
    dwc = [(rev_f_[i] - prev[i]) * V['wc_pct_drev'] for i in range(5)]
    ic_repl = ic_repl_pre
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
    pv = [fcff[i] * df_l[i] for i in range(5)]
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
    _life = life_
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
    pv_tv = tv * df_l[-1]
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
    return dict(fv=fv_dcf, eq=eq_dcf, ev=ev, tv=tv, pv_tv=pv_tv, sum_pv=sum_pv,
                tv_share=tv_share, net_cash=net_cash, fcff=fcff, capex=capex,
                dna_f=dna_f, nopat=nopat, dwc=dwc, gross_fa=gross_fa,
                ebit_f=ebit_f, reinv=reinv, pv=pv, term=_term, tin=_tin,
                ic_repl=ic_repl, life=life_, roic_t=roic_t, rr_t=rr_t,
                cash_at_val=cash_at_val, rev_f=rev_f_, ebitda_f=ebitda_f_,
                maint_cc=_maint_cc)


# THE BASE CASE IS build_dcf() WITH NO OVERRIDES, and the names below are its fields.
# Nothing downstream recomputes any of them.
_D = build_dcf()
ic_repl = _D['ic_repl']; gross_fa = _D['gross_fa']; dna_f = _D['dna_f']
capex = _D['capex']; ebit_f = _D['ebit_f']; nopat = _D['nopat']; dwc = _D['dwc']
roic_t = _D['roic_t']; fcff = _D['fcff']; reinv = _D['reinv']; pv = _D['pv']
sum_pv = _D['sum_pv']; _life = _D['life']; _tin = _D['tin']; _term = _D['term']
tv = _D['tv']; rr_t = _D['rr_t']; pv_tv = _D['pv_tv']; ev = _D['ev']
tv_share = _D['tv_share']; cash_at_val = _D['cash_at_val']; net_cash = _D['net_cash']
eq_dcf = _D['eq']; fv_dcf = _D['fv']; _maint_cc = _D['maint_cc']
_stub_from_mar = (V['stub_years'] - 0.25)

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
# [R-LENS-03] THE CLASS PRIMARY IS THE CENTRAL AND THE OTHER LENSES ARE CROSS-CHECKS.
# The registry gives this class a cash-flow primary with replacement cost, an enterprise
# multiple and the disclosed book beside it. NORMALISED EARNINGS IS NOT A LENS FOR THIS
# CLASS and is retired outright, not re-weighted; the full record of what was retired,
# what it read, and what retiring it cost is in LENS_RECORD below.
lenses = {'DCF (cash flow)': fv_dcf, 'Relative multiples': fv_rel,
          'Asset / replacement cost': fv_asset,
          'Book value (disclosed floor)': V['eq_fy25_rep'] / V['shares_fy25']}
fv_central = float(fv_dcf)
say(f"\n[Normalised lens] cash added at FACE, not capitalised at {V['pe_just']:.0f}x — "
    f"revision 1 valued the cash at an 18.6% discount to itself")
say(f"[Lenses] " + " | ".join(f"{k.split()[0]} {v:.2f}" for k, v in lenses.items()))
say(f"[Central] EGP {fv_central:.2f} vs spot {V['spot']:.2f} "
    f"({fv_central/V['spot']-1:+.1%}) — THE CASH-FLOW LENS, not a blend of four")

# ============ 6. SENSITIVITY, incl. NET CASH (revision 1 omitted it) =======
def reval(nc=None, g=None, we=None, beta_=None, mgn_shift=0.0):
    nc = net_cash if nc is None else nc
    g = V['g_term'] if g is None else g
    we = wacc_exp if we is None else we
    if beta_ is not None:
        we = (1 - wd_exp) * (rf_star + beta_ * V['erp_cds']) + wd_exp * kd_at
        bt = (beta_ / (1 + (1 - TAX) * wd_exp / (1 - wd_exp))) \
            * (1 + (1 - TAX) * V['wd_term'] / (1 - V['wd_term']))
        wt = (1 - V['wd_term']) * (V['rf_term'] + bt * V['erp_term']) + \
            V['wd_term'] * V['kd_term'] * (1 - TAX)
    else:
        wt = wacc_term
    f_ = [we - (we - wt) * gg for gg in glide]
    d_ = factors(f_)          # the SAME chain the base case uses, never a second copy
    eb = [ebitda_f[i] + rev_f[i] * mgn_shift for i in range(5)]
    ei = [eb[i] - dna_f[i] for i in range(5)]
    np_ = [ei[i] * (1 - TAX) for i in range(5)]
    rt = np_[-1] * (1 + g) / ic_repl
    # [R-TERM-01] ONE DEFINITION OF FREE CASH FLOW, AND THE SENSITIVITY IS NOT AN
    # EXCEPTION. This grid ran the explicit window on the RETIRED identity — NOPAT less
    # the growth in NOPAT over ROIC — while the base case ran the waterfall, so every
    # cell answered a question about a construction the study does not use. The note
    # below records that revision 2's grid re-derived the retired identity and that the
    # TERMINAL was re-pointed at the sanctioned module; the explicit window was left
    # behind, and nothing noticed because no assertion tied the grid to its own centre.
    # It read EGP 109.82 at a zero shift against a published 128.80, 15% apart.
    fc = [np_[i] + dna_f[i] - capex[i] - dwc[i] for i in range(5)]
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
# THE GRID'S OWN CENTRE MUST BE THE PUBLISHED ANSWER. Nothing tied the two together, and
# for one edition they were 15% apart while every cell looked perfectly reasonable on its
# own. A sensitivity is the base case with one driver moved; where the unmoved cell does
# not reproduce it, the grid is answering a different question from the study.
assert abs(reval() - fv_dcf) < 1e-6, (reval(), fv_dcf)
assert abs(sens_mgn[2] - fv_dcf) < 1e-6, (sens_mgn[2], fv_dcf)
assert abs(sens_nc[2] - fv_dcf) < 1e-6, (sens_nc[2], fv_dcf)
say(f"\n[Net cash sensitivity, on the REVIEWED 31-March-2026 balance sheet] " + " ".join(f"{x:.2f}" for x in sens_nc))


# ============ 5b. THE FOUR CONSTRUCTION RECORDS ============================
# [R-LENS-03] ONE CLASS PRIMARY IS THE CENTRAL. The typed 48/21/23/8 blend is RETIRED.
# Three of the four lenses it averaged read the company off reported accounting earnings
# and historical-cost book, and the weights had never cleared any out-of-sample test —
# chosen, written down, inherited. NORMALISED EARNINGS goes entirely: the registry does
# not permit it for this class, and on a single-asset cement plant whose margin is an
# OUTPUT of utilisation against a fixed cost stack there is no mid-cycle margin to
# normalise that the cash-flow lens does not already carry.
_RETIRED_BLEND = {'DCF (cash flow)': V['w_dcf'], 'Relative multiples': V['w_rel'],
                  'Normalised earnings': V['w_norm'], 'Asset / replacement cost': V['w_asset']}
_blend_value = float(fv_dcf * V['w_dcf'] + fv_rel * V['w_rel']
                     + fv_norm * V['w_norm'] + fv_asset * V['w_asset'])

# THE RANGE IS THE COMPANY'S OWN AUDITED MARGIN SPAN, macro held still — never a grid of
# terminal growth against the discount rate, whose corners are the two least coherent
# cells in it [R-MACRO-01].
_HIST_MGN = [FIL['derived'][y]['ebitda_margin'] for y in HIST]
_mgn_fc0 = BU[1]['mgn']
_UTIL23 = (V['rev_fy23'] / 2118.0) * cf / V['cap_clinker_mt']   # the filed year's own kilns
_mgn_lo = min(_HIST_MGN)
_range_lo = float(reval(mgn_shift=_mgn_lo - _mgn_fc0))

# ---------------------------------------------------------------- [R-ENF-05]
# EVERY CONTESTED JUDGEMENT WORTH MORE THAN 5 PER CENT OF VALUE, BOTH WAYS, THROUGH THE
# SAME CONSTRUCTION. Any single one is defensible; what is not is a study resolving all
# of them the same way and never noticing, which is exactly how a lean survives an audit
# of its steps. Each alternative below runs through build_dcf(), so the difference
# measures THE CHOICE and not the construction.
_alt_util = [V['kiln_util'][0]] + [V['kiln_util'][0]] * 5      # the filed FY2025 rate, held
CONTESTED = []


def _judge(choice, adopted, alternative, fv_alt, note):
    CONTESTED.append(dict(choice=choice, adopted=adopted, alternative=alternative,
                          fv_adopted=float(fv_dcf), fv_alternative=float(fv_alt),
                          effect=abs(float(fv_alt) - float(fv_dcf)) / float(fv_dcf),
                          direction=('the adopted side is HIGHER' if fv_dcf > fv_alt
                                     else 'the adopted side is LOWER'),
                          note=note))


_judge('kiln utilisation through the forecast',
       'ramps from %.1f%% of clinker capacity to %.1f%%' % (100 * V['kiln_util'][1],
                                                            100 * V['kiln_util'][5]),
       'held flat at the filed FY2025 rate of %.1f%%' % (100 * V['kiln_util'][0]),
       build_dcf(bu=build_bu(_alt_util))['fv'],
       'the company\'s own filed volumes ran 53.2%, 62.7% and 71.0% of clinker capacity '
       'across FY2023-25, so the ramp is a DECELERATING extrapolation of its own three-year '
       'trend rather than a new claim — but it is an extrapolation and not a disclosure, '
       'and roughly 12.6Mt of dormant Egyptian capacity is queuing to restart against it. '
       'This is the single largest judgement in the study and the one a reader should '
       'contest first.')

_judge('the depreciable life behind the terminal maintenance charge',
       'the weighted %.1f-year life implied by note 3/2\'s disclosed rates on note 4\'s '
       'own gross-cost mix' % (1.0 / V['dep_rate_disclosed']),
       'the 20-year MACHINERY life alone, note 3/2',
       build_dcf(life=20.0)['fv'],
       'note 3/2 discloses 2-2.5%% on buildings and utilities, 5%% on machinery, 20%% on '
       'vehicles and tools and 10-25%% on furniture. Weighted on note 4\'s own cost mix '
       'that is a %.1f-year life and it reproduces the filed FY2025 charge to within 1.2 '
       'per cent, which is what makes it sourced. Machinery alone is 20 years and is the '
       'part that actually wears out; the buildings carry most of the weighting and last '
       'far longer. Both are the company\'s own disclosure and the choice between them is '
       'a judgement.' % (1.0 / V['dep_rate_disclosed']))

_judge('replacement cost per annual tonne of cement capacity',
       'USD %.0f per tonne' % V['repl_usd_t'],
       'USD 120 per tonne, the bottom of the industry band',
       build_dcf(repl_usd_t=120.0)['fv'],
       'the greenfield band for an integrated plant in this region is USD 120-150 a tonne. '
       'It sets the maintenance charge in BOTH windows, so it is the input the whole '
       'capital-charge argument turns on.')

_judge('the explicit window\'s capital charge',
       'glides from the company\'s own disclosed spend to the terminal\'s current-cost '
       'maintenance by FY2030',
       'the company\'s own three-year average spend, escalated and held',
       build_dcf(conv=[0.0] * 5)['fv'],
       'the company spent EGP 120.8mn, 526.4mn and 262.4mn across FY2023-25 against a '
       'current-cost maintenance requirement of EGP %.0fmn. The plant is %.1f per cent '
       'written down on cost and its machinery %.1f per cent, with EGP %.1fmn fully '
       'depreciated AND STILL IN USE, so this is deferral rather than a young plant '
       'spending less. Holding the recent rate while running the kilns HARDER is two '
       'assumptions that cannot both be true.'
       % (_maint_cc,
          100 * FIL['fixed_assets_totals']['acc_dep'] / FIL['fixed_assets_totals']['cost'],
          100 * FIL['fixed_assets_fy2025']['machinery_equipment']['acc_dep']
          / FIL['fixed_assets_fy2025']['machinery_equipment']['cost'],
          FIL['fixed_assets_totals']['fully_depreciated_in_use'] / 1e6))

_judge('the adopted beta',
       '1.00, the tier-3 default',
       '0.837, the lead-lag corrected own-stock estimate',
       reval(beta_=0.837),
       'the own-stock regression against EGX30 returns an R-squared of 0.038 against the '
       '0.05 usability floor, so it is NOT usable and the hierarchy falls to unity. The '
       'lead-lag corrected point estimate is 0.837 and its 90 per cent interval contains '
       '1.00. Rounding UP to unity COSTS value rather than adding it, which is the '
       'direction worth stating.')

_MATERIAL = [c for c in CONTESTED if c['effect'] > 0.05]
_UP = sum(1 for c in _MATERIAL if c['fv_adopted'] > c['fv_alternative'])
say(f"\n[Contested judgements] {len(CONTESTED)} recorded, {len(_MATERIAL)} worth more "
    f"than 5% of value; {_UP} of {len(_MATERIAL)} material judgements resolved UPWARD")
for c in CONTESTED:
    say(f"    {c['choice'][:52]:<52} {c['fv_adopted']:7.2f} vs {c['fv_alternative']:7.2f}"
        f"  ({c['effect']:+.1%})")

# ---------------------------------------------------------------- [R-MACRO-01]
_PI = _LADDER
_INFL_INPUTS = [
    dict(key='cost_infl', mapping='calendar', first_year=2026,
         values=[round(V['cost_infl'][i + 1] / V['cost_infl'][i] - 1, 6) for i in range(5)],
         note='the house calendar ladder compounded; no leading year is exempt because '
              'no company disclosure anchors an inflation RATE here — the LEVEL is '
              'anchored on the filed FY2025 cost lines and the path above it is the '
              'house ladder to the basis point'),
    dict(key='price_dom_egp_t', mapping='calendar', first_year=2026,
         values=[round(V['price_dom_egp_t'][i + 1] / V['price_dom_egp_t'][i] - 1, 6)
                 for i in range(5)],
         note='the SAME index the cost lines carry, so the real spread per tonne is held '
              'flat and the margin is an OUTPUT of the two rather than an assumption'),
]
MACRO_RECORD = dict(
    market='EG', path_as_of=_PATH.as_of,
    inflation_inputs=_INFL_INPUTS,
    growth_lines=[
        dict(name='domestic realised cement price per tonne',
             years=_YRS,
             nominal=[round(V['price_dom_egp_t'][i + 1] / V['price_dom_egp_t'][i] - 1, 6)
                      for i in range(5)],
             real=0.0,
             basis='the house inflation ladder at zero real growth. The FY2025 level is '
                   'the price the DISCLOSED revenue implies against the volume this '
                   'model builds; everything above it is the ladder. Holding the real '
                   'spread flat is what [R-ANCHOR-01] left standing after the company\'s '
                   'own measurement refused the alternative: cost per unit of revenue '
                   'FELL from 67.91 per cent in Q1-2025 to 61.99 for FY2025 and 58.93 in '
                   'Q1-2026, where a real cost drift needed it to rise.'),
        dict(name='local cash cost per tonne and fixed cash cost',
             years=_YRS,
             nominal=[round(V['cost_infl'][i + 1] / V['cost_infl'][i] - 1, 6)
                      for i in range(5)],
             real=0.0,
             basis='the house inflation ladder at zero real growth, the same path the '
                   'price carries'),
        dict(name='export cement price, US dollars',
             years=_YRS,
             nominal=[round(V['price_exp_usd_t'][i + 1] / V['price_exp_usd_t'][i] - 1, 6)
                      for i in range(5)],
             real=0.0,
             exempt_reason='a US-dollar price set by the European carbon border mechanism '
                           'and landed-cost competition into Europe, not by Egyptian '
                           'inflation. It is converted into pounds through the house '
                           'currency path, which is where the Egyptian inflation enters'),
    ],
    fx_path=[round(x, 6) for x in V['fx_path'][1:]],
    terminal=dict(g_nominal=V['g_term'], real=0.0, rf=V['rf_term'],
                  inflation_in_rf=_PATH.terminal_inflation),
    explicit_years=5,
    growth_at_horizon_end=round(V['cost_infl'][5] / V['cost_infl'][4] - 1, 6),
    note='the explicit window ends on the terminal growth rate exactly: FY2030 escalates '
         'at the house terminal inflation of 7 per cent at zero real, which IS the '
         'terminal, so nothing is capitalised that the model never reached.',
)

# ---------------------------------------------------------------- [R-COC-01]
COC_RECORD = dict(
    market='EG', regime=_PATH.regime, years=5,
    rf_observed=V['rf'], default_spread=V['sov_spread_cds'], rf_star=rf_star,
    erp=V['erp_cds'], erp_basis='cds', beta=V['beta'],
    ke_exp=ke_exp, kd_pretax=V['kd'], kd_aftertax=kd_at,
    weight_equity=1 - wd_exp, weight_debt=wd_exp, wacc_exp=wacc_exp,
    rf_terminal=V['rf_term'], erp_terminal=V['erp_term'], ke_terminal=ke_term,
    kd_terminal_pretax=V['kd_term'], kd_terminal_aftertax=V['kd_term'] * (1 - TAX),
    weight_debt_terminal=V['wd_term'], wacc_terminal=wacc_term,
    glide_fractions=[float(g) for g in glide], forward_wacc=[float(f) for f in fwd],
    discount_factors=[float(d) for d in df_],
    terminal_discount_factor=float(df_[-1]),
    discounting_convention=dict(
        kind='mid_period',
        cumulative_years=[float(t) for t in t_mid],
        # THE EDGES ARE PART OF THE CONVENTION AND THE FACTORS DO NOT REPRODUCE WITHOUT
        # THEM. Each forward rate owns a slice of calendar and the first owns only the
        # stub. A reader who assumes each rate owns a whole year from t=0 recomputes
        # different factors — which is exactly what this study's own code did until this
        # edition, so the FY2030 rate never entered any discount factor at all.
        rate_edges=[float(e) for e in EDGES],
        note='the valuation date sits %.0f months into FY2026, so the first forward rate '
             'owns only the %.0f months still unearned and every later rate owns one '
             'whole year. The terminal is brought home on the SAME factor as the last '
             'explicit year: one date, one price of time.'
             % (V['stub_years'] * 12, REM * 12)),
    kd_integrity=dict(
        currency_composition='the borrowings are wholly Egyptian-pound bank facilities; '
                             'the audited statements disclose no foreign-currency tranche',
        currency_source='note 17 of the audited statements for the year ended 31 December '
                        '2025',
        interest_bearing_note=(
            'THE EFFECTIVE RATE IS NOT COMPUTABLE ON THIS BOOK AND THAT IS STATED RATHER '
            'THAN WORKED AROUND. Interest-bearing borrowings are EGP %.1fmn against total '
            'assets above EGP 12bn — 0.5 per cent of the capital structure — and the '
            'finance line of the income statement is a NET charge dominated by items that '
            'are not interest on debt. Dividing it by a broader liabilities total is the '
            'trap [R-COC-01] names in terms: it understates the rate by a multiple and '
            'manufactures evidence. The adopted %.2f per cent is the marginal rate a '
            'corporate of this standing borrows at against a sovereign yielding %.2f, '
            'which is the construction the rule asks for, and a plus or minus 700 basis '
            'point error on it moves the weighted cost of capital by under 2 basis points.'
            % (V['debt_fy25'], 100 * V['kd'], 100 * V['rf'])),
        effective_rate_unavailable=(
            'the audited statements disclose no interest expense on borrowings separately '
            'from the net finance line, so no rate can be computed independently from the '
            'filings. Named rather than approximated [SIGCM clause 8].'),
        above_sovereign=bool(V['kd'] > V['rf'] - V['sov_spread_cds']),
    ),
    sensitivity=dict(
        other_basis='rating',
        other_erp=V['erp_rating'],
        other_default_spread=V['sov_spread_rating'],
        other_ke_exp=(V['rf'] - V['sov_spread_rating']) + V['beta'] * V['erp_rating'],
        note='BOTH BASES ARE PUBLISHED AND ONE IS NAMED CENTRAL. The CDS basis is central '
             'by default under [R-COC-01] — it is the market\'s own live pricing of this '
             'sovereign\'s credit, against an agency judgement that moves in steps. On '
             'this sovereign the two are far apart, and the whole of the difference is '
             'the country risk counted the same way on both sides: the rating basis '
             'normalises the risk-free rate by %.2f points and adds %.2f back through the '
             'premium, the CDS basis by %.2f and %.2f. The adopted cost of equity is '
             '%.2f per cent; on the rating basis it is %.2f.'
             % (100 * V['sov_spread_rating'], 100 * V['erp_rating'],
                100 * V['sov_spread_cds'], 100 * V['erp_cds'],
                100 * ke_exp,
                100 * ((V['rf'] - V['sov_spread_rating'])
                       + V['beta'] * V['erp_rating'])),
    ),
    disclosures=[
        'the sovereign quote behind the house path is dated %s and is older than the '
        '14-day bound. It is accepted deliberately and the age is disclosed here rather '
        'than used quietly; on a book that is 0.5 per cent of capital and an equity '
        'weight above 99 per cent it moves the answer through the risk-free rate alone.'
        % _PATH.sovereign_asof,
        'the beta is TIER 3. The own-stock regression against EGX30 returns an R-squared '
        'of 0.038 against the 0.05 usability floor, so it is not usable; 1.00 is adopted '
        'and rounding up from the lead-lag corrected 0.837 COSTS value rather than adding '
        'it. Both are published.',
    ],
)

# ---------------------------------------------------------------- [R-BRIDGE-01]
BRIDGE_RECORD = dict(
    market='EG',
    balance_sheet_date='2026-03-31', latest_disclosed_date='2026-03-31',
    latest_disclosed_source=(
        'the reviewed condensed interim financial statements for the three months ended '
        '31 March 2026, downloaded from the company\'s own website and read by OCR off '
        'the rendered pixels (the file carries a 37-byte text layer across 37 pages), '
        'every statement footed against its own arithmetic. It is the LATEST disclosed '
        'sheet; there is none between it and the valuation date.'),
    register='sweep_register.json',
    lines=[
        dict(label='Enterprise value', value=float(ev)),
        dict(label='plus cash and bank balances, 31 March 2026', value=float(V['cash_mar26'])),
        dict(label='plus free cash flow earned from 31 March to the valuation date',
             value=float(fcff[0] / REM * _stub_from_mar)),
        dict(label='less interest-bearing debt, 31 March 2026', value=float(-V['debt_mar26'])),
        dict(label='less non-controlling interests', value=float(-V['nci'])),
    ],
    equity_value=float(eq_dcf), shares_mn=float(V['shares_mn']), per_share=float(fv_dcf),
    cash_charged_once=True,
    cash=dict(treatment='added_at_face', weights_basis='gross'),
    cash_note=(
        'the operations are discounted at a rate weighted on GROSS debt and the cash is '
        'then added at face exactly ONCE. This company is heavily net cash, and a '
        'net-debt weighting would drive the debt weight negative, lever the equity weight '
        'above one, put the operating rate ABOVE the cost of equity — and then add the '
        'same cash back in the bridge, which is the double charge [R-BRIDGE-01] names.'),
    nci=dict(
        basis='value_share', value=float(V['nci']), deduction=float(V['nci']),
        book=float(V['nci']), profit_share=float(V['nci']), proportional=float(V['nci']),
        proxy='the minority\'s carrying value at 31 March 2026, adopted AS the value '
              'share because at EGP %.0fmn against an equity value above EGP 33bn the '
              'three framings cannot differ by anything that reaches the second decimal '
              'of a per-share number' % V['nci'],
        proxy_source='the reviewed statement of financial position at 31 March 2026',
        framings_note='the three reference framings are the same number here, and that '
                      'is the finding rather than a shortcut.',
        deducted_from='equity'),
    dividend=dict(declared_after_balance_sheet_date=False, amount=0.0,
                  note='the filed statements of changes in equity show NO distribution at '
                       'all across FY2025 and the reviewed quarter, twice over and to the '
                       'pound, so there is none to deduct.'),
    associates=dict(basis='none', note='no equity-accounted associate is disclosed'),
)

# ---------------------------------------------------------------- [R-ANCHOR-01]
FORECAST_ANCHOR = dict(
    # THE FIELD NAMES ARE THE SHARED READER'S. This record was written in the same session
    # with nested keys of its own and the gate could not read it; it reported OK because
    # this study was on the ratchet, and A RATCHETED STUDY'S FAILURE REASON WAS NEVER
    # PRINTED. The record looked right, the gate looked green, and neither was.
    rate_name='EBITDA margin',
    latest_reviewed_period='FY2025, audited',
    latest_reviewed_date='2025-12-31',
    latest_reviewed_rate=float(_HIST_MGN[2]),
    latest_reviewed_source='the audited statements for the year ended 31 December 2025, '
                           'revenue and the cost lines of notes 24, 25 and 26',
    first_forecast_rate=float(_mgn_fc0),
    forecast_path=[float(b['mgn']) for b in BU[1:]],
    note=('THE FORECAST OPENS ABOVE THE LATEST AUDITED PERIOD AND RISES FROM THERE, which '
          'this rule does not fire on and which is printed anyway so the shape is visible '
          'rather than merely not-red. FY2026 opens at %.2f per cent against a filed '
          'FY2025 of %.2f, %.2f points above it, and FY2030 reaches %.2f — above every '
          'year the company has ever filed. The mechanism is operating leverage and it is '
          'an OUTPUT rather than an assumption: the kilns run from %.1f per cent of '
          'clinker capacity to %.1f while the fixed cash cost escalates only with the '
          'house inflation ladder. It is also the whole of this study\'s downside, which '
          'is why the primary lens publishes its range by flexing exactly this rate down '
          'to the lowest the company has filed.'
          % (100 * _mgn_fc0, 100 * _HIST_MGN[2], 100 * (_mgn_fc0 - _HIST_MGN[2]),
             100 * BU[5]['mgn'], 100 * V['kiln_util'][1], 100 * V['kiln_util'][5])),
)

LENS_RECORD = dict(
    **{'class': 'cement and heavy industrial'},
    primary=dict(
        kind='dcf', value=float(fv_dcf),
        range=dict(low=_range_lo, high=float(fv_dcf)),
        range_note='the cash-flow lens with the EBITDA margin flexed down to the lowest '
                   'the company has ever filed, the macro path held still',
        range_basis=dict(
            driver='the EBITDA margin, across its own audited span',
            low=float(_mgn_lo), high=float(_mgn_fc0), macro_held=True,
            evidence=(
                'Sinai Cement filed an EBITDA margin of %.2f per cent in FY2023, %.2f in '
                'FY2024 and %.2f in FY2025, every one audited. THE FORECAST OPENS AT %.2f '
                'PER CENT, ABOVE THE BEST OF THEM, and rises to %.2f by FY2030 — so this '
                'driver has NO UPSIDE CORNER against the company\'s own record and the '
                'whole of the range is downside. That is the finding rather than a '
                'defect in the range: the margin is an OUTPUT of a physical cost stack '
                'and it rises because the kilns run harder (utilisation %.1f per cent to '
                '%.1f) against a fixed cost that escalates only with the house inflation '
                'ladder. What the range prices is that mechanism failing. The FY2023 '
                'corner carries a plant at %.1f per cent utilisation through a currency '
                'collapse; it is the company\'s own filed record and it is used as the '
                'floor without adjustment.'
                % (100 * _HIST_MGN[0], 100 * _HIST_MGN[1], 100 * _HIST_MGN[2],
                   100 * _mgn_fc0, 100 * BU[5]['mgn'],
                   100 * V['kiln_util'][1], 100 * V['kiln_util'][5],
                   100 * _UTIL23))),
        note='the cash-flow lens on the company\'s own tonnes and prices, discounted on '
             'the glide from the house macro path, with the terminal built by the '
             'sanctioned module on the DISCLOSED asset life'),
    cross_checks=[
        dict(kind='replacement_cost', value=float(fv_asset),
             note='USD %.0f per annual tonne of cement capacity against a market paying '
                  'USD %.1f' % (V['ev_t_just'], ev_per_t)),
        dict(kind='relative_multiple', value=float(fv_rel), present_value=False,
             multiple=float(V['ev_ebitda_just']),
             circularity=dict(spot=float(V['spot']), shares=float(V['shares_mn']),
                              net_debt=float(-net_cash), metric_value=float(eb_norm)),
             multiple_source=(
                 'a HOUSE multiple of %.1fx on normalised EBITDA, disclosed as weakly '
                 'anchored and NOT read off the current price: the Egyptian listed peer '
                 'set is two names and neither publishes an EBITDA series this study '
                 'could measure a multiple from. The traded enterprise value over the '
                 'same normalised EBITDA is committed beside it in the circularity '
                 'block, and the two are far apart. Revision 1 used 5.0x anchored on a '
                 'peer quoted at 5.03x, an anchor that does not reproduce — that peer\'s '
                 'own market capitalisation over its own profit gives 3.48x against the '
                 '6.44x printed beside it.' % V['ev_ebitda_just'])),
        dict(kind='ev_per_tonne', value=float(ev_per_t), present_value=False,
             note='the market\'s own implied enterprise value per annual tonne of cement '
                  'capacity, in US dollars, against a replacement cost of USD %.0f'
                  % V['repl_usd_t']),
        dict(kind='book_value', value=float(V['eq_fy25_rep'] / V['shares_fy25']),
             note='the DISCLOSED floor at 31 December 2025 — equity of EGP %.1fmn over '
                  'the %.1fmn shares that equity was struck against. Published as a '
                  'floor and NEVER weighted into a central.'
                  % (V['eq_fy25_rep'], V['shares_fy25'])),
    ],
    envelope=dict(low=_range_lo, high=float(fv_dcf)),
    central=float(fv_dcf),
    retired=dict(
        blend=_RETIRED_BLEND, blend_value=_blend_value,
        why=('the weights were chosen, written down and inherited, and had never cleared '
             'an out-of-sample test. THREE OF THE FOUR LENSES read a cement plant off '
             'reported accounting earnings and historical-cost book — a floor, not a '
             'value, for an asset whose worth is the cash the kilns throw off. Retiring '
             'the blend moves the published answer from EGP %.2f to EGP %.2f and the gap '
             'to the latest known price from %+.1f per cent to %+.1f per cent: it moves '
             'the answer AWAY from the market, which is the evidence that the rule is '
             'structural rather than fitted.'
             % (_blend_value, fv_dcf, 100 * (_blend_value / V['spot'] - 1),
                100 * (fv_dcf / V['spot'] - 1))),
        normalised_earnings=dict(
            value=float(fv_norm),
            why='dropped as a lens for this class. The registry does not permit it, and '
                'on a single-asset plant whose margin is an output of utilisation there '
                'is no mid-cycle earnings level the cash-flow lens does not already '
                'carry. It read EGP %.2f and carried %.0f per cent of the retired blend.'
                % (fv_norm, 100 * V['w_norm'])),
    ),
)

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
say(f"  the central IS the cash-flow lens; no weights are carried")

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
              wacc_exp=wacc_exp, beta_term=beta_t, beta_u=beta_u, ke_term=ke_term,
              kd_term_at=V['kd_term'] * (1 - TAX), wacc_term=wacc_term,
              ke_raw_retired=V['rf'] + V['beta'] * V['erp_cds']),
    dcf=dict(cash_fy25=cash_at_val, cash_reported=V['cash_fy25'],
             term_maintenance=_term.maintenance, term_dna_addback=_term.dna_addback,
             term_wc_charge=_term.wc_charge, term_fcff=_term.fcff,
             term_floor=_term.floor, term_life_years=_life,
             df_tv=float(df_[-1]),   # the terminal is brought home on the LAST EXPLICIT
             #                        year's own factor: one date, one price of time
             term_below_floor=_term.below_floor, terminal_record=_term.record, sum_pv=sum_pv, tv=tv, pv_tv=pv_tv, ev=ev, tv_share=tv_share,
             net_cash=net_cash, nci=V['nci'], equity=eq_dcf, fv=fv_dcf, roic_term=roic_t,
             rr_term=rr_t, ic_repl=ic_repl, nopat_term=nopat[-1] * (1 + V['g_term'])),
    contested=CONTESTED, conv_weights=list(_CONV_DEFAULT),
    # THE HOUSE PATH'S OWN FIGURES, COMMITTED so the document computes them rather
    # than typing them. A policy rate typed into a builder is a figure nothing can
    # check, and this study carried two that had gone stale.
    macro_live=dict(policy_rate=_PATH.policy_rate,
                    terminal_inflation=_PATH.terminal_inflation,
                    sovereign_10y=_PATH.sovereign_10y,
                    sovereign_asof=_PATH.sovereign_asof,
                    inflation_ladder=list(_LADDER), as_of=_PATH.as_of),
    macro_record=MACRO_RECORD, cost_of_capital_record=COC_RECORD,
    bridge_record=BRIDGE_RECORD, lens_record=LENS_RECORD,
    forecast_anchor=FORECAST_ANCHOR,
    lenses=dict(values=lenses, central=fv_central, low=min(lenses.values()),
                high=max(lenses.values()), ebitda_norm=eb_norm, nopat_norm=nopat_norm,
                ev_per_t_spot=ev_per_t, ev_asset=ev_asset,
                earn_norm=nopat_norm, eq_fy25_roll=V['eq_fy25_rep'],
                bvps=V['eq_fy25_rep']/V['shares_fy25'],
                roe_sust=nopat_norm/V['eq_fy25_rep']),
    sensitivity=dict(nc_grid=nc_grid, net_cash=sens_nc, wacc_grid=wacc_grid,
                     g_grid=g_grid, wacc_g=sens_wg, beta_grid=beta_grid, beta=sens_beta,
                     mgn_grid=mgn_grid, mgn=sens_mgn),
    lens_ranges={
        # [R-LENS-03] THE PRIMARY'S RANGE IS THE PUBLISHED ENVELOPE, and it is produced by
        # flexing the EBITDA margin across the span the company's own audited accounts
        # have printed — never by nudging terminal growth against the discount rate, whose
        # bull corner is inflation high and low simultaneously. The retired 'Weighted
        # central' row is gone with the blend that made it.
        'DCF (cash flow)': dict(bear=_range_lo, base=fv_dcf, bull=fv_dcf),
        'Relative multiples': dict(
            bear=(eb_norm * (V['ev_ebitda_just'] - 1) + net_cash - V['nci']) / V['shares_mn'],
            base=fv_rel,
            bull=(eb_norm * (V['ev_ebitda_just'] + 1) + net_cash - V['nci']) / V['shares_mn']),
        'Asset / replacement cost': dict(
            bear=((V['ev_t_just'] - 15) * V['cap_cement_mt'] * 1e6 * V['fx'] / 1e6
                  + net_cash - V['nci']) / V['shares_mn'],
            base=fv_asset,
            bull=((V['ev_t_just'] + 15) * V['cap_cement_mt'] * 1e6 * V['fx'] / 1e6
                  + net_cash - V['nci']) / V['shares_mn']),
        'Book value (disclosed floor)': dict(
            bear=V['eq_fy25_rep'] / V['shares_fy25'],
            base=V['eq_fy25_rep'] / V['shares_fy25'],
            bull=V['eq_fy25_rep'] / V['shares_fy25']),
    },
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
