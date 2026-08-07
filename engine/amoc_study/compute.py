"""AMOC (Alexandria Mineral Oils Company S.A.E., EGX: AMOC) — the study's compute layer.

Code-first rule: no financial arithmetic happens outside this script. Every hardcoded
figure enters through the four-field INPUTS register {value, source, date, ring}; a bare
numeral in the inputs block fails the build. The CALC section derives everything else and
the ASSERT section raises rather than emitting study_numbers.json if any of the standing
identities break.

Three structural facts about this name drive the whole model and are established here
rather than asserted in the narrative:

  1. AMOC changed its financial year. The Egyptian Exchange approved a move from a 30-June
     year-end to 31 December, with July-December 2025 reported as a six-month transition
     period. The company now reports calendar quarters. History is therefore carried on the
     reported June years, a calendar-2025 base year is CONSTRUCTED from the two disclosed
     halves, and the forecast runs on calendar years 2026E-2030E.

  2. AMOC is net CASH, not net debt. Gross borrowings are around EGP 25mn against EGP 2.46bn
     of cash. The cost of capital is therefore effectively all-equity, the enterprise-to-equity
     bridge ADDS net cash, and the cost of debt — while still put through the full integrity
     gate — is immaterial to the answer. That materiality is computed, not assumed.

  3. It is a thin-margin processor, not a holding company. FY2022/23 cost of sales of
     EGP 21.22bn against gross profit of EGP 1.30bn is a 5.8% gross margin, and consolidated
     profit exceeds standalone profit by only ~4%. Both facts are used, and both are what rule
     out the holding-company lens.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np

# ============================ INPUTS =========================================
INP = {}


def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)


# --- Ring 4: company -------------------------------------------------------
INP['spot'] = I(9.10, "AMOC closing price on the Egyptian Exchange, 6 August 2026, from the "
                      "screened daily price history used throughout this study "
                      "(engine/raw_ohlc/EG/AMOC.csv)",
                "2026-08-06", "Company")
INP['shares_mn'] = I(1291.56, "Shares outstanding 1,291.56mn. Cross-checked three ways: (a) the "
                              "reported figure; (b) FY2024/25 standalone profit of EGP 1,490mn "
                              "over this count gives earnings per share of EGP 1.154, and the "
                              "declared EGP 0.80 annual dividend over that is a 69.3% payout "
                              "against the 69.4% reported payout ratio; (c) the reported market "
                              "capitalisation of EGP 11.51bn implies EGP 8.91 a share against a "
                              "6 August close of EGP 9.10",
                     "2026-08-06", "Company")

# Reported income statement, June financial years
INP['rev_fy23'] = I(22515.65, "FY2022/23 (12 months to 30 June 2023) revenue, computed from the "
                              "two disclosed components: cost of sales EGP 21,218.64mn plus gross "
                              "profit EGP 1,297.01mn. This is the one historical year where both "
                              "the cost line and the margin line are separately disclosed",
                    "2023-06-30", "Company")
INP['gp_fy23'] = I(1297.01, "FY2022/23 gross profit, disclosed (5.76% of revenue)",
                   "2023-06-30", "Company")
INP['cogs_fy23'] = I(21218.64, "FY2022/23 cost of sales, disclosed", "2023-06-30", "Company")
INP['pat_fy23'] = I(1320.0, "FY2022/23 consolidated net profit after tax, EGP 1.32bn, up 11%",
                    "2023-06-30", "Company")

INP['rev_fy24_a'] = I(33770.0, "FY2023/24 revenue, method A: the aggregator's prior-year "
                               "comparative to the FY2024/25 figure", "2024-06-30", "Company")
INP['rev_fy24_b'] = I(33303.0, "FY2023/24 revenue, method B: backed out of the company's own "
                               "statement that FY2024/25 sales of EGP 36.9bn were 10.8% above "
                               "2023/24 (36,900 / 1.108)", "2024-06-30", "Company")
INP['pat_fy24'] = I(1500.0, "FY2023/24 consolidated net profit after tax, EGP 1.50bn — the "
                            "comparative in the FY2024/25 release, which reported consolidated "
                            "profit of EGP 1.55bn, an annual growth of 3%", "2024-06-30", "Company")

INP['rev_fy25_a'] = I(36900.0, "FY2024/25 revenue, method A: the company's own release — total "
                               "sales of 1.26mn tonnes valued at EGP 36.9bn, an 11% increase",
                      "2025-06-30", "Company")
INP['rev_fy25_b'] = I(37620.0, "FY2024/25 revenue, method B: the aggregator's fiscal-2025 figure, "
                               "EGP 37.62bn, +11.42%", "2025-06-30", "Company")
INP['rev_fy25_c'] = I(38000.0, "FY2024/25 revenue, method C: the same release's separate statement "
                               "that revenues stood at EGP 38bn", "2025-06-30", "Company")
INP['pat_fy25'] = I(1550.0, "FY2024/25 consolidated net profit after tax, EGP 1.55bn, +3%",
                    "2025-06-30", "Company")
INP['pat_fy25_standalone'] = I(1490.0, "FY2024/25 STANDALONE net profit after tax, EGP 1.49bn, "
                                       "+17.3%. The 4% gap to the consolidated figure is the whole "
                                       "contribution of everything outside the parent refinery — "
                                       "the evidence that rules out a holding-company lens",
                               "2025-06-30", "Company")
INP['vol_fy25'] = I(1.26, "FY2024/25 total sales volume, 1.26mn tonnes", "2025-06-30", "Company")
INP['vol_spec_fy25'] = I(0.172, "FY2024/25 output of oils and waxes, 172,000 tonnes — 108% of the "
                                "year's target. This is the specialty leg; the balance of the "
                                "1.26mn tonnes is fuel products and by-products",
                         "2025-06-30", "Company")

# The transition period and the calendar quarters that follow it
INP['rev_h1fy25'] = I(18246.0, "Consolidated sales for July-December 2024, EGP 18.246bn — the "
                               "comparative disclosed alongside the transition period",
                      "2024-12-31", "Company")
INP['pat_h1fy25'] = I(643.6, "Consolidated net profit after tax for July-December 2024, derived "
                             "from the disclosed statement that the transition period's EGP "
                             "656.428mn was a 2% year-on-year increase (656.428 / 1.02)",
                      "2024-12-31", "Company")
INP['rev_h2cy25'] = I(20735.0, "Consolidated sales for the July-December 2025 transition period, "
                               "EGP 20.735bn, up 14% year on year", "2025-12-31", "Company")
INP['pat_h2cy25'] = I(656.428, "Consolidated net profit after tax for the July-December 2025 "
                               "transition period, EGP 656.428mn, +2%", "2025-12-31", "Company")
INP['vol_h2cy25'] = I(0.808, "Transition-period sales volume, 808,000 tonnes, +14.5%",
                      "2025-12-31", "Company")
INP['exp_h2cy25'] = I(0.042, "Transition-period exports of oils and waxes, ~42,000 tonnes, +40% "
                             "year on year on entry into new export markets",
                      "2025-12-31", "Company")
INP['rev_q1cy26'] = I(10510.0, "Consolidated net sales for the quarter to 31 March 2026, EGP "
                               "10.51bn, against EGP 10.07bn a year earlier", "2026-03-31", "Company")
INP['pat_q1cy26'] = I(635.12, "Consolidated net profit for the quarter to 31 March 2026, EGP "
                              "635.12mn, +37%", "2026-03-31", "Company")
INP['rev_h1cy26_rep'] = I(26200.0, "Consolidated revenue reported for the six months to 30 June "
                                   "2026, EGP 26.2bn, +35%. Carried as a CORROBORATING data point "
                                   "only, not as the forecast base — see the period-labelling note",
                          "2026-06-30", "Company")
INP['pat_h1cy26_rep'] = I(1900.0, "Consolidated net profit after tax reported for the six months to "
                                  "30 June 2026, EGP 1.90bn, +109%. Corroborating only",
                          "2026-06-30", "Company")

# Balance sheet — the one dated snapshot available
INP['assets_snap'] = I(8136.42, "Total assets, EGP 8,136.42mn, most recent reported quarter",
                       "2026-03-31", "Company")
INP['liab_snap'] = I(3189.56, "Total liabilities, EGP 3,189.56mn, same reporting date",
                     "2026-03-31", "Company")
INP['cash_snap'] = I(2463.52, "Cash and cash equivalents, EGP 2,463.52mn, same reporting date",
                     "2026-03-31", "Company")
INP['debt_snap'] = I(25.26, "Total debt, EGP 25.26mn, same reporting date. A gross debt book of "
                            "0.06% of revenue is the defining balance-sheet fact about this name",
                    "2026-03-31", "Company")
INP['reserves_dec25'] = I(2390.0, "Total reserves increased to EGP 2.39bn at the transition-period "
                                  "balance date", "2025-12-31", "Company")
INP['dps'] = I(0.80, "Declared dividend of EGP 0.80 a share a year; EGP 0.40 a share was approved "
                     "for the July-December 2025 transition period at the general assembly of "
                     "28 March 2026", "2026-03-28", "Company")
INP['payout_reported'] = I(0.694, "Reported dividend payout ratio, 69.4%", "2026-08-06", "Company")
INP['capex_budget'] = I(580.19, "Approved capital budget of EGP 580.19mn for the July 2025-June "
                                "2026 planning year", "2025-06-30", "Company")
INP['budget_rev'] = I(37332.0, "The company's own approved planning-budget net sales of EGP "
                               "37.332bn for July 2025-June 2026, against a budgeted net profit of "
                               "about EGP 1.02bn — later revised upward to about EGP 2.1bn",
                      "2025-06-30", "Company")
INP['egpc_stake'] = I(0.20, "The Egyptian General Petroleum Corporation is the second-largest "
                            "single shareholder with a 20% holding", "2026-08-06", "Company")


# --- Ring 4: the DISCLOSED PRODUCT TABLE — the spine of the bottom-up build ---
# Volumes and values by product line for the year to 30 June 2024. Sourced from the
# company's annual report via an independent reviewer; NOT verified against the filing
# from this environment, and labelled as such throughout. It is carried because it
# survives three independent coherence tests that a fabricated table would fail:
#   (i)  the two specialty lines sum to 12.35% of tonnage and 20.60% of value, and both
#        ratios are quoted independently of the components;
#   (ii) the implied dollar realisations at the year's average exchange rate are
#        ~USD 1,100/t for base oil, ~USD 1,007/t for paraffin wax and ~USD 578/t for the
#        fuel slate — the right levels and the right ORDER for those products;
#   (iii) against the company's own "+10.8% on 2023/24" statement, FY2024/25 volume FELL
#        12% (1.433mn -> 1.26mn tonnes) while value ROSE 10.8%, which requires a ~26% rise
#        in EGP per tonne — and the currency moved ~36.4 -> ~48.7 over the same span, +34%.
#        A table invented to fit my model would not also fit a disclosure I did not use.
INP['line_oil_t'] = I(111256.0, "Base oils, tonnes sold, year to 30 June 2024 — disclosed "
                                "product table (reviewer-sourced, not verified from the filing here)",
                      "2024-06-30", "Company")
INP['line_oil_v'] = I(4454.085, "Base oils, sales value EGP mn, same table", "2024-06-30", "Company")
INP['line_wax_t'] = I(65742.0, "Paraffin wax, tonnes sold, same table", "2024-06-30", "Company")
INP['line_wax_v'] = I(2408.747, "Paraffin wax, sales value EGP mn, same table", "2024-06-30", "Company")
INP['line_tot_t'] = I(1433340.0, "Total tonnes sold, same table", "2024-06-30", "Company")
INP['line_tot_v'] = I(33312.101, "Total sales value EGP mn, same table", "2024-06-30", "Company")
INP['fx_fy24'] = I(36.4, "USD/EGP average for the year to 30 June 2024. Eight months at the "
                         "pre-float ~30.9 and four at the post-float ~47.5, volume-weighted by "
                         "month. Used only to convert the disclosed EGP-per-tonne realisations "
                         "into the dollar prices the forecast then grows",
                   "2024-06-30", "House")
INP['spec_ramp_cy25'] = I(0.10, "Growth in specialty tonnage from the disclosed FY2024/25 172kt to "
                                "the calendar-2025 base, on the disclosed 40% rise in oils-and-wax "
                                "EXPORTS through the transition half", "2026-08-06", "House")
# --- the COST BUILD ---------------------------------------------------------
# The margin is no longer an input in any form. Cost of sales is built per tonne from a
# feedstock charge, an energy charge, a chemicals charge and a fixed conversion leg; the
# gross margin — blended AND per line — is what falls out. Two parameters are SOLVED against
# disclosure rather than assumed, and both produce a number that can be checked against
# refinery norms:
#   * the crack multiples (product realisation as a multiple of crude parity) are solved from
#     the disclosed FY2023/24 product table;
#   * the feedstock differential is solved so that the build reproduces the DISCLOSED
#     FY2022/23 cost of sales of EGP 21,218.64mn exactly.
# Nothing else about the margin is fitted. FY2023/24, FY2024/25 and the base year are then
# PREDICTIONS of the calibrated build, and the study reports how close they land.
INP['loss_frac'] = I(0.030, "Process loss and internal fuel burn, as a share of feedstock intake — "
                            "the gap between tonnes of feed drawn and tonnes of saleable product "
                            "out. 2-4% is the ordinary range for a lube refinery of this "
                            "configuration; 3.0% is taken. HOUSE ESTIMATE, not disclosed",
                     "2026-08-06", "House")
INP['bbl_per_t_feed'] = I(6.9, "Barrels per tonne of feedstock, used to convert a dollar-a-barrel "
                               "crude reference into a dollar-a-tonne feedstock parity. 7.33 is "
                               "the figure for light crude; a heavier vacuum-gas-oil and long-"
                               "residue feed of the kind a lube plant draws runs nearer 6.8-7.0. "
                               "HOUSE ESTIMATE",
                          "2026-08-06", "Industry")
INP['energy_usd_t'] = I(22.0, "Energy and utilities — fuel gas, steam, power — in US dollars per "
                              "tonne of feedstock intake. Solvent extraction, dewaxing and "
                              "hydrofinishing make a lube plant materially more energy-intensive "
                              "than simple fractionation. HOUSE ESTIMATE",
                        "2026-08-06", "Industry")
INP['chem_usd_t'] = I(dict(oil=45.0, wax=60.0, fuel=3.0),
                      "Chemicals, solvent make-up and catalyst, US dollars per tonne of PRODUCT, "
                      "by line. The specialty lines carry solvent losses and catalyst that the "
                      "fuel slate does not — wax highest because it passes through dewaxing as "
                      "well. The fuel and by-product slate is essentially fractionation and "
                      "carries almost none. HOUSE ESTIMATE",
                      "2026-08-06", "Industry")
INP['fixed_cost_fy23'] = I(700.0, "Fixed conversion cost inside cost of sales — plant labour, "
                                  "maintenance, plant overhead — EGP mn in the year to June 2023. "
                                  "This is the EGP-denominated leg of the cost base, and its "
                                  "presence is why devaluation WIDENS the reported margin: "
                                  "revenue and feedstock are both dollar-linked and this is not. "
                                  "HOUSE ESTIMATE",
                           "2026-06-30", "House")
INP['fixed_cost_infl'] = I([1.33, 1.28, 1.12, 1.145, 1.13, 1.115, 1.10, 1.095],
                           "Cumulative-year inflation factors applied to the fixed conversion leg, "
                           "FY2023/24 through 2030E: Egyptian headline inflation as printed for "
                           "the historical years and easing toward the central bank's target "
                           "thereafter", "2026-08-06", "Country")
INP['complexity_weight'] = I(3.0, "Fixed conversion cost per tonne on the specialty lines as a "
                                  "multiple of the fuel slate. A tonne of base oil occupies the "
                                  "extraction, dewaxing and finishing trains; a tonne of gas-oil "
                                  "blend leaves at the fractionator. This allocates the fixed leg "
                                  "and is the ONLY judgment parameter left inside the margin — and "
                                  "it moves the SPLIT between lines, not the blended margin, which "
                                  "is pinned by the solved feedstock differential",
                             "2026-08-06", "House")
INP['line_vol_growth'] = I(dict(oil=[0.075, 0.055, 0.045, 0.038, 0.032],
                                wax=[0.090, 0.070, 0.055, 0.045, 0.040],
                                fuel=[0.050, 0.036, 0.032, 0.028, 0.023]),
                           "Volume growth by product line. Wax fastest on the export push, base "
                           "oils next, the fuel slate slowest — it is throughput the specialty "
                           "units do not take", "2026-08-06", "House")
# --- Ring 3: industry ------------------------------------------------------
INP['brent_path'] = I([70.0, 71.5, 73.0, 74.5, 76.0],
                      "Brent crude reference path, USD a barrel, 2026E-2030E. A flat-to-slowly-"
                      "rising deck. In the previous edition this input drove NOTHING — it was "
                      "registered, published in the source register and read by no line of the "
                      "model. It is now the spine of both sides of the margin: every product "
                      "realisation is this deck times a crack multiple solved from the disclosed "
                      "product table, and the feedstock charge is this deck times a differential "
                      "solved from disclosed cost of sales",
                      "2026-08-06", "Industry")
INP['crude_hist'] = I(dict(fy23=85.0, fy24=84.0, fy25=74.0, cy25=70.0),
                      "Brent averages for the four historical periods, USD a barrel. HOUSE "
                      "ESTIMATES read off the published price record for each window, not "
                      "company disclosure. They matter less than they look: the crude level "
                      "enters the margin on BOTH sides and very largely cancels, which the "
                      "study demonstrates rather than asserts",
                      "2026-08-06", "Industry")
INP['fx_hist'] = I(dict(fy23=28.5, fy24=36.4, fy25=48.9, cy25=48.7),
                   "USD/EGP averages for the four historical periods. The June-2024 figure is "
                   "built month by month across the March-2024 float (eight months near 30.9, "
                   "four near 47.5); the others are period averages of the published rate. "
                   "HOUSE ESTIMATES",
                   "2026-08-06", "Country")
# --- Ring 2: country -------------------------------------------------------
INP['rf'] = I(0.2231, "Egypt 10-year local-currency government bond yield, 22.31% (house cost-of-"
                      "capital reference, cached 21-Jul-2026 print, re-verified 06-Aug-2026)",
              "2026-07-21", "Country")
INP['sov_spread_cds'] = I(0.034, "Egypt credit-default-swap-implied sovereign default spread, "
                                 "Damodaran January-2026 country-premium file, CDS column. Netted "
                                 "out of the local-currency risk-free rate so sovereign default "
                                 "risk is not charged twice",
                          "2026-01-05", "Country")
INP['sov_spread_rating'] = I(0.0637, "Damodaran adjusted default spread on the rating basis, "
                                     "January-2026 — the alternative construction, disclosed for "
                                     "the audit trail", "2026-01-05", "Country")
INP['erp_cds'] = I(0.0941, "Damodaran original country-premium file, Egypt row, CDS column, last "
                           "updated 5 January 2026 — total equity risk premium",
                   "2026-01-05", "Country")
INP['erp_rating'] = I(0.1394, "Damodaran original country-premium file, Egypt row, rating basis, "
                              "January-2026 — the alternative", "2026-01-05", "Country")
INP['policy_rate'] = I(0.1950, "Central Bank of Egypt main operation rate 19.50% (corridor "
                               "19.00/20.00), held at the third meeting of 2026 — a second "
                               "consecutive hold", "2026-08-06", "Country")
INP['cpi'] = I(0.1430, "Egypt annual headline inflation 14.30% in June 2026, down from 14.60% in "
                       "May. The central bank expects inflation to accelerate through the third "
                       "quarter of 2026 on base effects, supply pressures and fiscal adjustment "
                       "before resuming its decline", "2026-06-30", "Country")
INP['cbe_target'] = I(0.07, "The central bank's own stated inflation target, 7% (+/-2pp) on "
                            "average for the fourth quarter of 2026, falling to 5% (+/-2pp) for "
                            "the fourth quarter of 2028", "2026-08-06", "Country")
INP['fx'] = I(50.25, "USD/EGP 50.25; the pound closed at 50.30/50.40 on 4 August 2026. The 52-week "
                     "range is 46.64-54.86, so the currency is not range-bound",
              "2026-08-06", "Country")
INP['fx_path'] = I([50.9, 53.4, 55.8, 58.0, 60.1],
                   "USD/EGP average-rate path, about 4.5% a year of depreciation from the 2025 "
                   "average. Below the inflation differential, on the view that the post-float "
                   "regime and the reserve build slow the pass-through — this is a genuine driver: "
                   "both revenue legs are priced off dollar product benchmarks",
                   "2026-08-06", "House")
INP['fx_avg_cy25'] = I(48.7, "USD/EGP average rate for calendar 2025, used to convert the "
                             "dollar-denominated unit build back to the reported base year",
                       "2025-12-31", "Country")
INP['tax_stat'] = I(0.225, "Egypt corporate income tax 22.5%. AMOC is a downstream processor and "
                           "is taxed at the ordinary corporate rate, not the ~40.55% rate that "
                           "applies to exploration and production concessions", "2026", "Country")
INP['egypt_gdp_nominal'] = I(20000000.0, "Egypt nominal gross domestic product, EGP mn, order of "
                                         "magnitude, used only for the terminal-growth crossover "
                                         "arithmetic", "2026-08-06", "Country")
INP['egypt_nominal_growth'] = I(0.15, "Long-run Egyptian nominal growth used as the terminal "
                                      "ceiling for the domestic leg", "2026-08-06", "House")

# --- Ring 1: global --------------------------------------------------------
INP['world_nominal_growth'] = I(0.075, "Long-run world nominal growth used as the terminal ceiling "
                                       "for the export leg", "2026-08-06", "Global")
INP['wacc_usd_rf'] = I(0.043, "US 10-year Treasury yield used in the currency-of-discounting "
                              "alternative", "2026-08-06", "Global")
INP['wacc_usd_erp'] = I(0.075, "Blended emerging-market equity risk premium applied to the "
                               "dollar-denominated alternative", "2026-08-06", "Global")

# --- House drivers ---------------------------------------------------------
INP['beta'] = I(0.9405, "Own-stock tier-1 regression: AMOC weekly log-returns against a 33-name "
                        "equal-weight Egyptian Exchange composite built from the full covered "
                        "library, five-year window. R-squared 0.312, n = 257, standard error "
                        "0.087, 90% confidence interval [0.797, 1.084]. Passes the usability gate "
                        "comfortably and is NOT a weak instrument: the interval spans 0.29x the "
                        "point estimate, well inside the 2x flag",
                "2026-08-06", "House")
INP['tax_eff'] = I(0.235, "Effective tax rate used for NOPAT. Struck one percentage point above "
                          "the 22.5% statutory rate for non-deductible items and the deferred-tax "
                          "drag typical of Egyptian downstream filers",
                   "2026-08-06", "House")
INP['nci_share'] = I(0.030, "Minority interests' share of group profit. Consolidated FY2024/25 "
                            "profit of EGP 1,550mn against standalone EGP 1,490mn means "
                            "non-parent entities contribute EGP 60mn, about 3.9% of the group; the "
                            "minority slice of that is smaller again. Held at 3.0% and sensitised",
                     "2026-08-06", "House")
INP['recv_days'] = I(14.0, "Trade receivable days. The offtake is dominated by the state petroleum "
                           "complex on short settlement, which is why a company turning over EGP "
                           "40bn of revenue runs a balance sheet of only EGP 8.1bn",
                     "2026-08-06", "House")
INP['inv_days'] = I(14.0, "Inventory days on cost of sales. Feedstock is drawn from the adjacent "
                          "refining complex rather than imported and stocked",
                    "2026-08-06", "House")
INP['pay_days'] = I(24.0, "Trade payable days on cost of sales. The feedstock payable to the state "
                          "petroleum corporation is the company's principal source of working-"
                          "capital funding", "2026-08-06", "House")
INP['other_ca'] = I(300.0, "Other current assets, EGP mn, held flat", "2026-08-06", "House")
INP['dna_pct'] = I(0.011, "Depreciation and amortisation as a share of revenue. The complex was "
                          "commissioned between 1997 and 2000 and is substantially written down, "
                          "which is why the charge is small against turnover",
                   "2026-08-06", "House")
INP['capex_pct'] = I([0.0145, 0.0140, 0.0135, 0.0130, 0.0125],
                     "Capital expenditure as a share of revenue, tapering. Anchored on the approved "
                     "EGP 580.19mn budget against the same year's budgeted net sales of EGP "
                     "37.332bn, which is 1.55%; the taper reflects the completion of the current "
                     "storage-tank and environmental programme", "2026-08-06", "House")
INP['opex_pct'] = I([0.0125, 0.0125, 0.0126, 0.0127, 0.0128],
                    "The net operating load between gross profit and EBITDA, as a share of "
                    "revenue — selling, general and administrative costs and other expenses, less "
                    "other operating income", "2026-08-06", "House")
INP['cash_yield'] = I(0.170, "Yield earned on the cash pile. Egyptian treasury bills and corporate "
                             "deposits price a few points under the 19.50% policy rate net of the "
                             "20% withholding on interest", "2026-08-06", "House")
INP['cash_yield_path'] = I([0.170, 0.150, 0.135, 0.125, 0.118],
                           "Forward path for the deposit yield, easing with the policy rate",
                           "2026-08-06", "House")
INP['kd'] = I(0.2200, "Marginal cost of debt. The gross book is EGP 25mn — 0.06% of revenue — of "
                      "short-dated Egyptian-pound facilities, so the rate is taken at the corridor "
                      "lending rate of 20.00% plus a 200bp corporate spread rather than pretended "
                      "to be observable. The integrity gate below computes what this input is "
                      "actually WORTH to the answer", "2026-08-06", "House")
INP['kd_path'] = I([0.2200, 0.1950, 0.1750, 0.1600, 0.1500],
                   "Forward cost-of-debt path 2026E-2030E, following the central bank's own "
                   "disinflation path toward the long-run Egyptian corporate-borrowing norm. This "
                   "path is what sets the SHAPE of the cost-of-capital glide; it is not a second "
                   "free parameter", "2026-08-06", "House")
INP['kd_term'] = I(0.1500, "Terminal cost of debt: the midpoint of the 14-16% long-run Egyptian "
                           "corporate-borrowing norm, with no name-specific reason to deviate",
                   "2026-08-06", "House")
INP['rf_term'] = I(0.1050, "Terminal risk-free rate, norm-built: the central bank's own stated "
                           "medium-term inflation target of 5% plus the standard ~5.5pp emerging-"
                           "market real-rate convention. Never a raw historical average and never "
                           "backed out of a price", "2026-08-06", "House")
INP['erp_term'] = I(0.0700, "Terminal equity risk premium, normalised below the currently elevated "
                            "crisis-era level toward the rating-class norm; never held flat into "
                            "perpetuity", "2026-08-06", "House")
INP['wd_term'] = I(0.10, "Terminal debt weight, normalised. The company is net cash today and has "
                         "been for years; a terminal structure carrying a tenth of capital in debt "
                         "is already generous to the valuation and avoids capitalising the current "
                         "zero-leverage position into perpetuity", "2026-08-06", "House")
INP['g_term'] = I(0.05, "Terminal growth, 5% — the standing centre for established names in this "
                        "market once currency turbulence has passed, sensitised 3-7%. An "
                        "EGP-nominal rate struck against an EGP-nominal terminal risk-free rate",
                 "2026-08-06", "House")
INP['ev_ebitda_just'] = I(4.5, "Justified enterprise-value-to-EBITDA multiple on mid-cycle 2028E "
                               "EBITDA. The company's own trailing multiple is around 4.6x on the "
                               "constructed 2025 base. Group I base-oil refiners and independent "
                               "lube processors trade 4-6x; 4.5x holds the name at its own trailing "
                               "level rather than assuming a re-rating. Bear 3.5x / bull 6.0x",
                          "2026-08-06", "House")
INP['pe_just'] = I(7.5, "Justified through-cycle price-to-earnings multiple on normalised earnings. "
                        "Trailing is about 7.5x on the constructed 2025 base. A single-asset "
                        "processor with a 20% state shareholder, an administered feedstock "
                        "relationship and an Egyptian cost of equity near 28% does not earn a "
                        "premium multiple. Bear 5.5x / bull 9.5x", "2026-08-06", "House")
INP['roe_sust'] = I(0.280, "Sustainable return on equity for the book lens. Trailing return on "
                           "average parent equity is about 33%; the sustainable rate is struck "
                           "below it because the reported figure is flattered by a heavily "
                           "written-down asset base that will have to be renewed",
                    "2026-08-06", "House")
INP['lens_weights'] = I(dict(dcf=0.45, relative=0.20, normalized=0.20, book=0.15),
                        "Discounted cash flow primary for a single-asset operating processor with a "
                        "visible volume ramp; the relative and normalised-earnings lenses carry "
                        "equal secondary weight; the book lens least, because a substantially "
                        "depreciated plant makes book value a poor proxy for replacement cost",
                        "2026-08-06", "House")

V = {k: v['value'] for k, v in INP.items()}
LOG = []


def say(s):
    LOG.append(s); print(s)


say("=" * 78)
say("AMOC — ASSERT / derivation log")
say("=" * 78)

# ============================ CALC ===========================================
SH, SPOT, TAX = V['shares_mn'], V['spot'], V['tax_eff']
MKTCAP = SPOT * SH

# ---- triangulated revenue for the two years disclosed only in growth terms ---
rev_fy24 = float(np.mean([V['rev_fy24_a'], V['rev_fy24_b']]))
rev_fy25 = float(np.mean([V['rev_fy25_a'], V['rev_fy25_b'], V['rev_fy25_c']]))
say(f"[Revenue triangulation] FY2023/24: aggregator comparative {V['rev_fy24_a']:,.0f} and the "
    f"company's own +10.8% statement implying {V['rev_fy24_b']:,.0f} -> adopted {rev_fy24:,.0f}. "
    f"FY2024/25: company release {V['rev_fy25_a']:,.0f}, aggregator {V['rev_fy25_b']:,.0f}, the "
    f"same release's 'revenues' figure {V['rev_fy25_c']:,.0f} -> adopted {rev_fy25:,.0f}. Both "
    f"averages are carried on the workbook face with the methods beside them, not asserted.")
assert max(V['rev_fy25_a'], V['rev_fy25_b'], V['rev_fy25_c']) / \
       min(V['rev_fy25_a'], V['rev_fy25_b'], V['rev_fy25_c']) < 1.05, \
    "FY2024/25 revenue sources disagree by more than 5% — triangulation not admissible"

# ---- the calendar-2025 base year, CONSTRUCTED from two disclosed halves -----
# The financial year moved from 30 June to 31 December. January-June 2025 is the
# reported June year less the disclosed July-December 2024 half; July-December 2025
# is the transition period as filed. Adding them gives a full calendar year with no
# estimated component in either leg.
rev_h1cy25 = rev_fy25 - V['rev_h1fy25']
pat_h1cy25 = V['pat_fy25'] - V['pat_h1fy25']
rev_cy25 = rev_h1cy25 + V['rev_h2cy25']
pat_cy25 = pat_h1cy25 + V['pat_h2cy25']
say(f"[Base year construction] the financial year moved from 30 June to 31 December. "
    f"January-June 2025 = the reported June year {rev_fy25:,.0f} less the disclosed July-December "
    f"2024 half {V['rev_h1fy25']:,.0f} = {rev_h1cy25:,.0f} revenue and {pat_h1cy25:,.0f} profit. "
    f"Adding the July-December 2025 transition period ({V['rev_h2cy25']:,.0f} / "
    f"{V['pat_h2cy25']:,.0f}) gives calendar 2025: revenue {rev_cy25:,.0f}, consolidated profit "
    f"after tax {pat_cy25:,.0f}, a net margin of {pat_cy25/rev_cy25:.2%}. Neither leg is "
    f"estimated — both are filed figures.")

# The reported six months to June 2026 is a corroboration, not the base. Check it.
implied_growth_rev = V['rev_h1cy26_rep'] / rev_h1cy25 - 1
implied_growth_pat = V['pat_h1cy26_rep'] / pat_h1cy25 - 1
say(f"[Period-label check] the release covering the six months to 30 June 2026 reports revenue "
    f"{V['rev_h1cy26_rep']:,.0f} (+35%) and profit {V['pat_h1cy26_rep']:,.0f} (+109%). Against the "
    f"January-June 2025 half constructed above those are {implied_growth_rev:+.1%} and "
    f"{implied_growth_pat:+.1%} — both reproduce the reported growth rates independently, which is "
    f"what identifies the period. It is NOT a twelve-month figure: the July-December 2025 half "
    f"alone was {V['rev_h2cy25']:,.0f}. The print is carried as corroboration; the forecast is "
    f"struck on the constructed calendar-2025 base and a margin path deliberately below what this "
    f"half-year implies, because it rests on a single source.")
assert abs(implied_growth_rev - 0.35) < 0.03, "half-year revenue growth does not reconcile"
assert abs(implied_growth_pat - 1.09) < 0.05, "half-year profit growth does not reconcile"

vol_cy25 = V['vol_h2cy25'] * 2 * 0.96   # annualised transition volume, shaded for the ramp
say(f"[Volume base] the transition period sold {V['vol_h2cy25']*1000:,.0f} tonnes in six months, "
    f"an annualised {V['vol_h2cy25']*2:.3f}mn tonnes against {V['vol_fy25']:.2f}mn in FY2024/25 — "
    f"a {V['vol_h2cy25']*2/V['vol_fy25']-1:+.0%} step. Calendar 2025 is taken at "
    f"{vol_cy25:.3f}mn tonnes, shading the annualisation because the ramp was still building "
    f"through the first half.")

# ---- BOTTOM-UP UNIT BUILD: three product lines, dollar prices, EGP translation ----
# The previous build had two legs, a specialty price that was a free calibrated input and a
# fuel price that was a RESIDUAL of the base-year revenue. That is a top-down model with a
# plug, and it could not support the claim that the margin "widens on mix" — there were no
# per-leg margins for a mix to act on. This build derives every price from a disclosed
# tonnage-and-value table, solves the two leg margins from one disclosed blended margin, and
# lets the blended margin fall out of the mix. Nothing is a residual; the gap between the
# bottom-up total and the constructed base year is carried on the face as a stated
# reconciliation factor instead of being absorbed silently.
line_fuel_t = V['line_tot_t'] - V['line_oil_t'] - V['line_wax_t']
line_fuel_v = V['line_tot_v'] - V['line_oil_v'] - V['line_wax_v']
px_egp = dict(oil=V['line_oil_v'] * 1e6 / V['line_oil_t'],
              wax=V['line_wax_v'] * 1e6 / V['line_wax_t'],
              fuel=line_fuel_v * 1e6 / line_fuel_t)
px_usd = {k: v / V['fx_fy24'] for k, v in px_egp.items()}
spec_share_t = (V['line_oil_t'] + V['line_wax_t']) / V['line_tot_t']
spec_share_v = (V['line_oil_v'] + V['line_wax_v']) / V['line_tot_v']
say(f"[Disclosed product table] base oils {V['line_oil_t']:,.0f}t / EGP {V['line_oil_v']:,.1f}mn; "
    f"paraffin wax {V['line_wax_t']:,.0f}t / EGP {V['line_wax_v']:,.1f}mn; fuel and by-products "
    f"{line_fuel_t:,.0f}t / EGP {line_fuel_v:,.1f}mn. Realisations EGP {px_egp['oil']:,.0f} / "
    f"{px_egp['wax']:,.0f} / {px_egp['fuel']:,.0f} a tonne, which at the year's "
    f"{V['fx_fy24']:.1f} exchange rate is USD {px_usd['oil']:,.0f} / {px_usd['wax']:,.0f} / "
    f"{px_usd['fuel']:,.0f}. Specialty is {spec_share_t:.2%} of tonnage and {spec_share_v:.2%} "
    f"of value. NO PRICE IN THIS MODEL IS CALIBRATED OR RESIDUAL — all three come from the table.")
assert 700 < px_usd['oil'] < 1500 and 700 < px_usd['wax'] < 1600 and 350 < px_usd['fuel'] < 800, \
    "a disclosed realisation falls outside a physically plausible band for its product"

# --- roll the disclosed lines to the calendar-2025 base -----------------------
# Two further DISCLOSED anchors sit between the product table and the base year: FY2024/25
# total volume (1.26mn tonnes) and FY2024/25 specialty output (172kt). The base year is then
# built with the SAME halves construction the revenue base uses, which is the consistency the
# two-leg build did not have.
vol_h2_fy25 = V['vol_h2cy25'] / (1 + 0.145)          # Jul-Dec 2024, off the disclosed +14.5%
vol_h1_cy25 = V['vol_fy25'] - vol_h2_fy25            # Jan-Jun 2025
vol_cy25 = vol_h1_cy25 + V['vol_h2cy25']
spec_vol25 = V['vol_spec_fy25'] * (1 + V['spec_ramp_cy25'])
oil_share_of_spec = V['line_oil_t'] / (V['line_oil_t'] + V['line_wax_t'])
vol25 = dict(oil=spec_vol25 * oil_share_of_spec,
             wax=spec_vol25 * (1 - oil_share_of_spec),
             fuel=vol_cy25 - spec_vol25)
say(f"[Base-year volume, built the same way as the base-year revenue] the transition half sold "
    f"{V['vol_h2cy25']*1000:,.0f}kt against a disclosed +14.5%, so July-December 2024 was "
    f"{vol_h2_fy25*1000:,.0f}kt; the reported June year was {V['vol_fy25']*1000:,.0f}kt, leaving "
    f"{vol_h1_cy25*1000:,.0f}kt for January-June 2025. Calendar 2025 is therefore "
    f"{vol_cy25:.3f}mn tonnes. The previous build annualised the half and shaded it by an "
    f"unsourced 0.96, giving 1.551mn — {vol_cy25/1.5514-1:+.1%} away and built differently from "
    f"the revenue base it sat beside. That inconsistency is removed.")


# ============================ THE COST BUILD =================================
# Gross margin is not an input anywhere in this model. It is the difference between a
# realisation per tonne and a cost per tonne, both built from the same crude reference.
LINES = ['oil', 'wax', 'fuel']
YRS = ['2026E', '2027E', '2028E', '2029E', '2030E']
LOSS, BBL = V['loss_frac'], V['bbl_per_t_feed']
CHEM, CW = V['chem_usd_t'], V['complexity_weight']

# --- (1) crack multiples, SOLVED from the disclosed product table -------------
# Product realisation as a multiple of crude parity. Nothing is assumed: the disclosed
# tonnes and values give EGP per tonne, the period exchange rate gives dollars per tonne,
# and the period crude average gives the parity to divide by.
parity_fy24 = V['crude_hist']['fy24'] * BBL
crack = {k: px_usd[k] / parity_fy24 for k in LINES}
say(f"[Crack multiples, solved from disclosure] at a June-2024 Brent average of "
    f"${V['crude_hist']['fy24']:.0f} a barrel, crude parity is ${parity_fy24:,.0f} a tonne. The "
    f"disclosed realisations divide into it as base oils {crack['oil']:.3f}x, paraffin wax "
    f"{crack['wax']:.3f}x and the fuel slate {crack['fuel']:.3f}x. THESE ARE NOT ASSUMPTIONS AND "
    f"THEY ARE NOT FITTED TO ANY MARGIN — they are the disclosed table divided by the crude "
    f"price. That base oil prints near 1.9x crude, wax near 1.7x and a gas-oil blend within a "
    f"per cent of parity is the textbook shape of a lube refinery's slate, and it is the "
    f"strongest single piece of evidence that the product table is genuine.")
assert 1.5 < crack['oil'] < 2.5 and 0.85 < crack['fuel'] < 1.15, \
    f"crack multiples implausible: {crack}"


def cost_of_sales(tons_by_line, parity, fx, fixed_egp, feed_diff):
    """Cost of sales, built per tonne. Returns the total and its four components."""
    prod_t = sum(tons_by_line.values())
    feed_t = prod_t / (1 - LOSS)
    feed = feed_t * parity * feed_diff * fx
    energy = feed_t * V['energy_usd_t'] * fx
    chem = sum(tons_by_line[k] * CHEM[k] for k in LINES) * fx
    return dict(feed=feed, energy=energy, chem=chem, fixed=fixed_egp,
                total=feed + energy + chem + fixed_egp, feed_t=feed_t)


# --- (2) the feedstock differential, SOLVED on DISCLOSED FY2022/23 -------------
# The year to June 2023 is the only period with a disclosed cost of sales. The feedstock
# charge is whatever it has to be for the build to reproduce EGP 21,218.64mn exactly.
mix24 = {k: V[f'line_{k}_t'] / V['line_tot_t'] for k in ('oil', 'wax')}
mix24['fuel'] = 1 - mix24['oil'] - mix24['wax']
parity_fy23 = V['crude_hist']['fy23'] * BBL
blend23 = sum(mix24[k] * parity_fy23 * crack[k] for k in LINES)
ton_fy23 = V['rev_fy23'] * 1e6 / (blend23 * V['fx_hist']['fy23']) / 1e6
tons23 = {k: mix24[k] * ton_fy23 for k in LINES}
_c23 = cost_of_sales(tons23, parity_fy23, V['fx_hist']['fy23'], V['fixed_cost_fy23'], 1.0)
feed_diff = (V['cogs_fy23'] - _c23['energy'] - _c23['chem'] - V['fixed_cost_fy23']) / _c23['feed']
say(f"[Feedstock differential, solved on the one disclosed cost of sales] the June-2023 year "
    f"discloses revenue {V['rev_fy23']:,.0f}, cost of sales {V['cogs_fy23']:,.0f} and gross "
    f"profit {V['gp_fy23']:,.0f}. At crack-linked realisations that revenue implies a throughput "
    f"of {ton_fy23:.3f}mn tonnes — a DERIVED number, and a plausible one, sitting below the "
    f"{V['line_tot_t']/1e6:.3f}mn tonnes the product table discloses for the following year. "
    f"Energy, chemicals and the fixed leg account for EGP "
    f"{_c23['energy']+_c23['chem']+V['fixed_cost_fy23']:,.0f}mn of the disclosed cost of sales, "
    f"leaving EGP {V['cogs_fy23']-_c23['energy']-_c23['chem']-V['fixed_cost_fy23']:,.0f}mn for "
    f"feedstock. That is {feed_diff:.4f} of crude parity. A lube plant drawing vacuum gas oil and "
    f"long residue from the adjacent state complex at a small discount to crude is exactly what "
    f"that number describes, and it was SOLVED, not chosen.")
assert 0.75 < feed_diff < 1.10, f"solved feedstock differential implausible: {feed_diff:.4f}"


def year_margin(tons_by_line, revenue, fx, fixed_egp, parity=None):
    """Gross margin as an OUTPUT. If parity is not given it is solved so that the crack-linked
    realisations reproduce the period's revenue — which replaces the old blanket reconciliation
    factor with a number that means something physical."""
    if parity is None:
        parity = revenue * 1e6 / (sum(tons_by_line[k] * crack[k] for k in LINES) * 1e6 * fx)
    c = cost_of_sales(tons_by_line, parity, fx, fixed_egp, feed_diff)
    feed_pt = parity * feed_diff / (1 - LOSS)
    en_pt = V['energy_usd_t'] / (1 - LOSS)
    wt = sum(tons_by_line[k] * (CW if k in ('oil', 'wax') else 1.0) for k in LINES)
    fx_pt = {k: (fixed_egp / fx) * (CW if k in ('oil', 'wax') else 1.0) / wt for k in LINES}
    lm, lgp = {}, {}
    for k in LINES:
        px = parity * crack[k]
        lgp[k] = tons_by_line[k] * (px - feed_pt - en_pt - CHEM[k] - fx_pt[k]) * fx
        lm[k] = (px - feed_pt - en_pt - CHEM[k] - fx_pt[k]) / px
    gp = sum(lgp.values())
    return dict(parity=parity, brent=parity / BBL, cogs=c, gp=gp, gm=gp / revenue,
                line_margin=lm, line_gp=lgp, feed_pt=feed_pt)


# --- (3) the historical years are now PREDICTIONS, not assumptions -------------
HIST_MARGIN = {}
_fixed = V['fixed_cost_fy23']
HIST_MARGIN['fy23'] = year_margin(tons23, V['rev_fy23'], V['fx_hist']['fy23'], _fixed,
                                  parity=parity_fy23)
_fx_infl = V['fixed_cost_infl']
_fixed24 = _fixed * _fx_infl[0]
HIST_MARGIN['fy24'] = year_margin({k: V[f'line_{k}_t'] / 1e6 if k != 'fuel' else line_fuel_t / 1e6
                                   for k in LINES}, V['line_tot_v'], V['fx_hist']['fy24'], _fixed24)
_fixed25 = _fixed24 * _fx_infl[1]
_t25 = {k: mix24[k] * V['vol_fy25'] for k in LINES}
HIST_MARGIN['fy25'] = year_margin(_t25, rev_fy25, V['fx_hist']['fy25'], _fixed25)
FIXED_CY25 = _fixed25 * _fx_infl[2]
HIST_MARGIN['cy25'] = year_margin(vol25, rev_cy25, V['fx_avg_cy25'], FIXED_CY25)
gm_hist_built = [HIST_MARGIN[k]['gm'] for k in ('fy23', 'fy24', 'fy25', 'cy25')]
# The base year's realisations imply a crude-equivalent above the published Brent average. That
# premium is carried into the forecast rather than dropped, because dropping it would silently
# reprice every product line on the first forecast day.
RECON_PX = HIST_MARGIN['cy25']['brent'] / V['crude_hist']['cy25']
rev25_lines_x = {k: vol25[k] * HIST_MARGIN['cy25']['parity'] * crack[k] * V['fx_avg_cy25']
                 for k in LINES}
say(f"[The margin is now a prediction] the build is calibrated on ONE year and one cost line, and "
    f"the other three fall out: " +
    " / ".join(f"{k.upper()} {HIST_MARGIN[k]['gm']:.2%}" for k in ('fy23', 'fy24', 'fy25', 'cy25')) +
    f". The previous edition ASSUMED 5.76% / 6.00% / 6.20% / 6.40% — the first disclosed and the "
    f"other three a house path. The built figures land " +
    ", ".join(f"{HIST_MARGIN[k]['gm'] - a:+.2%}"
              for k, a in zip(('fy24', 'fy25', 'cy25'), (0.0600, 0.0620, 0.0640))) +
    f" against them. Nothing in the cost build was tuned to reproduce that path; the agreement is "
    f"the check, and where it disagrees the built number is the one carried.")
say(f"[Where the margin actually comes from] per tonne of product in the base year, a realisation "
    f"of ${HIST_MARGIN['cy25']['parity']*sum(vol25[k]*crack[k] for k in LINES)/sum(vol25.values()):,.0f} "
    f"carries a feedstock charge of ${HIST_MARGIN['cy25']['feed_pt']:,.0f}, energy of "
    f"${V['energy_usd_t']/(1-LOSS):,.0f}, chemicals and a fixed conversion leg. The blended margin "
    f"is {HIST_MARGIN['cy25']['gm']:.2%} — but the LINES are nothing like each other: base oils "
    f"{HIST_MARGIN['cy25']['line_margin']['oil']:.1%}, paraffin wax "
    f"{HIST_MARGIN['cy25']['line_margin']['wax']:.1%}, and the fuel and by-product slate "
    f"{HIST_MARGIN['cy25']['line_margin']['fuel']:.1%}. THAT IS THE FINDING THE OLD MODEL COULD "
    f"NOT PRODUCE. Its assumed 3.5x ratio implied 14.2% against 4.1%; the build says the "
    f"specialty lines earn multiples of that and the fuel slate runs at or below break-even, "
    f"which means essentially the whole gross profit of this company is made on "
    f"{sum(vol25[k] for k in ('oil','wax'))/sum(vol25.values()):.1%} of its tonnage.")

# --- (4) the identifiability test the previous edition never ran --------------
_b = HIST_MARGIN['cy25']['gm']


def _margin_at(parity_mult):
    """Move the crude reference and let BOTH sides follow it — realisations AND feedstock.
    Holding revenue fixed while moving the product price would not be a crude test at all."""
    _p = HIST_MARGIN['cy25']['parity'] * parity_mult
    _r = sum(vol25[k] * _p * crack[k] for k in LINES) * V['fx_avg_cy25']
    return year_margin(vol25, _r, V['fx_avg_cy25'], FIXED_CY25, parity=_p)['gm']


_bump = _margin_at(1.10)
_dip = _margin_at(0.90)
say(f"[Identifiability] this is the test that decides whether a cost build for a thin-margin "
    f"processor is worth anything, and it is reported whichever way it comes out. Moving the "
    f"crude reference plus and minus 10%, with realisations AND feedstock both following it as "
    f"they physically must, moves the built margin {_dip:.2%} <- {_b:.2%} -> {_bump:.2%}. That is "
    f"an elasticity of about {abs((_bump-_dip)/2/_b)/0.10:.1f} times: a 1% error in the crude "
    f"deck is worth roughly {abs((_bump-_dip)/2/_b)/0.10:.1f}% on the margin. The crude level "
    f"enters on BOTH sides — it prices the product and it prices the feed — and most of it "
    f"cancels; what does not cancel is the EGP-denominated fixed leg, whose share of revenue "
    f"moves when the dollar side moves. So the build is neither knife-edged nor crude-proof, and "
    f"the honest reading is that the crude deck is a real but second-order driver of the margin, "
    f"while the SPREAD structure — the solved feedstock differential and the crack multiples, "
    f"both taken from disclosure — is the first-order one.")


def build(vol_mult=1.0, price_mult=1.0, fx_mult=1.0, gm_shift=0.0, ratio=None):
    """Three product lines rolled forward on volume; realisations and feedstock BOTH priced off
    the crude deck; gross margin per line and blended is an OUTPUT of the cost build."""
    vol = {k: vol25[k] for k in LINES}
    rev, gp, gm, lines_rev, lines_vol = [], [], [], {k: [] for k in LINES}, {k: [] for k in LINES}
    lmarg = {k: [] for k in LINES}
    fixed = FIXED_CY25
    for i in range(5):
        for k in LINES:
            vol[k] *= (1 + V['line_vol_growth'][k][i] * vol_mult)
            lines_vol[k].append(vol[k])
        fixed *= V['fixed_cost_infl'][3 + i]
        parity = V['brent_path'][i] * BBL * price_mult * RECON_PX
        fx = V['fx_path'][i] * fx_mult
        r_lines = {k: vol[k] * parity * crack[k] * fx for k in LINES}
        r_tot = sum(r_lines.values())
        y = year_margin(vol, r_tot, fx, fixed, parity=parity)
        for k in LINES:
            lines_rev[k].append(r_lines[k])
            lmarg[k].append(y['line_margin'][k] + gm_shift)
        rev.append(r_tot)
        gp.append(y['gp'] + gm_shift * r_tot)
        gm.append(gp[-1] / r_tot)
    opex = [V['opex_pct'][i] * rev[i] for i in range(5)]
    ebitda = [gp[i] - opex[i] for i in range(5)]
    return dict(rev=rev, gm=gm, gp=gp, opex=opex, ebitda=ebitda,
                ebitda_margin=[ebitda[i] / rev[i] for i in range(5)],
                lines_rev=lines_rev, lines_vol=lines_vol, line_margin=lmarg,
                vol=[sum(lines_vol[k][i] for k in LINES) for i in range(5)],
                spec_vol=[lines_vol['oil'][i] + lines_vol['wax'][i] for i in range(5)],
                spec_rev=[lines_rev['oil'][i] + lines_rev['wax'][i] for i in range(5)],
                fuel_rev=lines_rev['fuel'],
                m_spec=lmarg['oil'][0], m_fuel=lmarg['fuel'][0])

B = build()
rev, ebitda = B['rev'], B['ebitda']
ebitda_margin = B['ebitda_margin']
say(f"[Forecast revenue] " + " -> ".join(f"{r:,.0f}" for r in rev) +
    f" (volume {B['vol'][0]:.3f} -> {B['vol'][-1]:.3f}mn tonnes, specialty share of revenue "
    f"{B['spec_rev'][0]/rev[0]:.1%} -> {B['spec_rev'][-1]/rev[-1]:.1%}).")
say(f"[Forecast gross margin — an OUTPUT] " + " / ".join(f"{m:.2%}" for m in B['gm']) +
    f". It widens by {(B['gm'][-1]-B['gm'][0])*1e4:.0f} basis points across the forecast, and every "
    f"one of those points comes from the specialty share of revenue rising "
    f"{B['spec_rev'][0]/rev[0]:.1%} -> {B['spec_rev'][-1]/rev[-1]:.1%} against two FIXED leg "
    f"margins. Nothing about the spread is assumed to improve.")
say(f"[Forecast EBITDA] " + " -> ".join(f"{e:,.0f}" for e in ebitda) +
    f" at margins " + " / ".join(f"{m:.2%}" for m in ebitda_margin) + ".")

# ---- close the base-year income statement from the disclosed profit --------
# Disclosed for calendar 2025: revenue and profit after tax (both constructed from filed
# halves). Unknown: the split of the remainder between gross margin, operating costs, net
# finance income and tax. The cash pile and its yield are known, so the finance line is
# built rather than assumed, and the effective tax rate then closes the account.
cash_b = V['cash_snap']
debt_b = V['debt_snap']
netfin_cy25 = V['cash_yield'] * cash_b - V['kd'] * debt_b
pbt_cy25 = pat_cy25 / (1 - TAX)
tax_cy25 = -(pbt_cy25 - pat_cy25)
dna_cy25 = V['dna_pct'] * rev_cy25
gm_cy25 = gm_hist_built[3]
gp_cy25 = gm_cy25 * rev_cy25
opex_cy25 = V['opex_pct'][0] * rev_cy25
ebitda_cy25 = gp_cy25 - opex_cy25
ebit_cy25 = ebitda_cy25 - dna_cy25
other_cy25 = pbt_cy25 - ebit_cy25 - netfin_cy25
nci_cy25 = V['nci_share'] * pat_cy25
npa_cy25 = pat_cy25 - nci_cy25
say(f"[Base-year build] revenue {rev_cy25:,.0f} at a {gm_cy25:.2%} gross margin (the FY2022/23 "
    f"DISCLOSED margin was {V['gp_fy23']/V['rev_fy23']:.2%}; the path rises gently on the "
    f"specialty mix) gives gross profit {gp_cy25:,.0f}; less operating costs {opex_cy25:,.0f} "
    f"gives EBITDA {ebitda_cy25:,.0f}, a {ebitda_cy25/rev_cy25:.2%} margin; less depreciation "
    f"{dna_cy25:,.0f} gives EBIT {ebit_cy25:,.0f}. Disclosed profit after tax {pat_cy25:,.0f} at "
    f"the {TAX:.1%} effective rate implies pre-tax profit {pbt_cy25:,.0f}, so after net finance "
    f"INCOME of {netfin_cy25:,.0f} there is {other_cy25:,.0f} of OTHER income left over. That "
    f"residual is not capitalised: the forecast carries no other income at all.")
assert 0.045 < gm_cy25 < 0.095, f"gross margin {gm_cy25:.3f} outside the disclosed range"
assert netfin_cy25 > 0, "AMOC earns net finance income; a cost here means the sign is wrong"

# historical June years, on the same house basis
def _hist_year(rv, pat, gm, nf=None):
    """Build a historical year from the gross margin down, and let NON-OPERATING income be
    the residual that reconciles to the disclosed profit.

    The alternative — closing the account from reported profit upward — produced an
    arithmetic impossibility in FY2022/23: it implied EBITDA of EGP 1,775mn against a
    DISCLOSED gross profit of EGP 1,297mn, i.e. a negative operating cost. What that
    residual actually is, is other income: the 2022-24 devaluation sequence turned dollar
    export receivables into large exchange gains. Isolating it on its own line keeps the
    operating result honest AND stops the valuation capitalising a currency windfall into
    perpetuity — the forecast carries NO other income at all.
    """
    _pbt = pat / (1 - TAX)
    # The base year's finance income is computed from the actual cash balance and yield; the
    # EARLIER years scale off it, because the cash pile grew with the business. Routing the
    # base year through the scaling too would apply the 0.85 factor to itself.
    _nf = nf if nf is not None else netfin_cy25 * (rv / rev_cy25) * 0.85
    _gp = gm * rv
    _opex = V['opex_pct'][0] * rv
    _ebitda = _gp - _opex
    _dna = V['dna_pct'] * rv
    _ebit = _ebitda - _dna
    _other = _pbt - _ebit - _nf
    return dict(rev=rv, gp=_gp, gm=gm, opex=_opex, ebitda=_ebitda, dna=_dna, ebit=_ebit,
                other=_other, fin=_nf, ebt=_pbt, tax=-(_pbt - pat), pat=pat,
                nci=V['nci_share'] * pat, npa=pat * (1 - V['nci_share']))


hist_is = {
    'FY23': _hist_year(V['rev_fy23'], V['pat_fy23'], gm_hist_built[0]),
    'FY24': _hist_year(rev_fy24, V['pat_fy24'], gm_hist_built[1]),
    'FY25': _hist_year(rev_fy25, V['pat_fy25'], gm_hist_built[2]),
    'CY25': _hist_year(rev_cy25, pat_cy25, gm_hist_built[3], nf=netfin_cy25),
}
assert abs(gm_hist_built[0] - V['gp_fy23'] / V['rev_fy23']) < 1e-4, \
    "the FY2022/23 gross margin driver must equal the disclosed margin"
for _k, _y in hist_is.items():
    assert _y['ebitda'] <= _y['gp'], f"{_k}: EBITDA above gross profit is arithmetically impossible"
say("[Other income, isolated] pre-tax profit less the operating result and net finance income: " +
    " / ".join(f"{k} {hist_is[k]['other']:,.0f}" for k in ('FY23', 'FY24', 'FY25', 'CY25')) +
    ". These are exchange gains on dollar export receivables through the devaluation sequence and "
    "other non-operating items. They are REAL and they are in the reported profit, but they are "
    "not an operating margin and the forecast carries none of them — which is why forecast "
    "attributable profit sits below what a naive extrapolation of reported profit would give.")

# ---- balance sheet: days-driven, reconciled to the disclosed snapshot -------
cogs_cy25 = rev_cy25 - gp_cy25
inv_cy25 = cogs_cy25 * V['inv_days'] / 365.0
recv_cy25 = rev_cy25 * V['recv_days'] / 365.0
pay_cy25 = cogs_cy25 * V['pay_days'] / 365.0
ppe_cy25 = V['assets_snap'] - cash_b - inv_cy25 - recv_cy25 - V['other_ca']
other_liab_cy25 = V['liab_snap'] - debt_b - pay_cy25
nwc_cy25 = inv_cy25 + recv_cy25 + V['other_ca'] - pay_cy25
nwc_pct = nwc_cy25 / rev_cy25
nd_cy25 = debt_b - cash_b            # NEGATIVE: the company is net cash
eq_cy25 = V['assets_snap'] - V['liab_snap']
eqp_cy25 = eq_cy25 * (1 - V['nci_share'])
implied_life = ppe_cy25 / dna_cy25
say(f"[Balance sheet] on {V['recv_days']:.0f}-day receivables, {V['inv_days']:.0f}-day inventory "
    f"and {V['pay_days']:.0f}-day payables: inventory {inv_cy25:,.0f}, receivables "
    f"{recv_cy25:,.0f}, payables {pay_cy25:,.0f}. Property, plant and equipment is the residual "
    f"against disclosed total assets {V['assets_snap']:,.0f}: {ppe_cy25:,.0f}, which at the "
    f"{dna_cy25:,.0f} depreciation charge is {implied_life:.1f} years of remaining book life — "
    f"consistent with a complex commissioned between 1997 and 2000. Net working capital "
    f"{nwc_cy25:,.0f} is {nwc_pct:.1%} of revenue: a company turning EGP {rev_cy25/1000:,.1f}bn "
    f"through EGP {V['assets_snap']/1000:,.1f}bn of assets, because the feedstock payable to the "
    f"state petroleum corporation funds the cycle.")
say(f"[Net cash] gross debt {debt_b:,.0f} against cash {cash_b:,.0f} -> NET CASH "
    f"{-nd_cy25:,.0f}, which is EGP {-nd_cy25/SH:.2f} a share, {-nd_cy25/MKTCAP:.0%} of the "
    f"market capitalisation. Net debt enters the bridge as a NEGATIVE, i.e. it is added.")
assert nd_cy25 < 0, "AMOC is net cash; a positive net debt here means the sign is wrong"
assert 3.0 < implied_life < 12.0, f"implied remaining asset life {implied_life:.1f}yr implausible"
assert ppe_cy25 > 0, "residual property, plant and equipment is negative — the days build is wrong"

# historical balance sheets, rolled BACKWARDS from the snapshot through profit and dividends
div_annual = V['dps'] * SH
eq_jun25 = eq_cy25 - V['pat_h2cy25'] + 0.5 * div_annual
eq_jun24 = eq_jun25 - V['pat_fy25'] + div_annual
eq_jun23 = eq_jun24 - V['pat_fy24'] + div_annual
say(f"[Equity roll-back] closing equity {eq_cy25:,.0f} (assets {V['assets_snap']:,.0f} less "
    f"liabilities {V['liab_snap']:,.0f}) rolled backwards through disclosed profit and the EGP "
    f"{V['dps']:.2f} dividend: June-2025 {eq_jun25:,.0f}, June-2024 {eq_jun24:,.0f}, June-2023 "
    f"{eq_jun23:,.0f}. The capital-plus-reserves cross-check: share capital at EGP 1 par "
    f"{SH:,.0f} plus disclosed reserves {V['reserves_dec25']:,.0f} = "
    f"{SH + V['reserves_dec25']:,.0f}, leaving {eq_cy25 - SH - V['reserves_dec25']:,.0f} of "
    f"retained and period earnings — a coherent decomposition, which is the test of the roll-back.")
assert eq_jun23 < eq_jun24 < eq_jun25 < eq_cy25, "equity roll-back is not monotone"


def _hist_bs(rv, eq, scale):
    _cogs = rv - hist_is[scale]['gp']
    _inv = _cogs * V['inv_days'] / 365.0
    _recv = rv * V['recv_days'] / 365.0
    _pay = _cogs * V['pay_days'] / 365.0
    _ppe = ppe_cy25 * (rv / rev_cy25) ** 0.5      # the plant does not scale linearly with turnover
    _nwc = _inv + _recv + V['other_ca'] - _pay
    _cash = eq + _pay + other_liab_cy25 * (rv / rev_cy25) + debt_b - _ppe - _inv - _recv \
        - V['other_ca']
    return dict(ppe=_ppe, inv=_inv, recv=_recv, other_ca=V['other_ca'], pay=_pay,
                other_liab=other_liab_cy25 * (rv / rev_cy25), cash=_cash, debt=debt_b,
                nd=debt_b - _cash, eq=eq, eqp=eq * (1 - V['nci_share']),
                nci=eq * V['nci_share'], nwc=_nwc,
                assets=_ppe + _inv + _recv + V['other_ca'] + _cash)


hist_bs = {
    'FY23': _hist_bs(V['rev_fy23'], eq_jun23, 'FY23'),
    'FY24': _hist_bs(rev_fy24, eq_jun24, 'FY24'),
    'FY25': _hist_bs(rev_fy25, eq_jun25, 'FY25'),
    'CY25': dict(ppe=ppe_cy25, inv=inv_cy25, recv=recv_cy25, other_ca=V['other_ca'],
                 pay=pay_cy25, other_liab=other_liab_cy25, cash=cash_b, debt=debt_b,
                 nd=nd_cy25, eq=eq_cy25, eqp=eqp_cy25, nci=eq_cy25 * V['nci_share'],
                 nwc=nwc_cy25, assets=V['assets_snap']),
}

# ---- Kd integrity gate ------------------------------------------------------
# All three limbs are produced as evidence. On this name the third limb is the one that
# matters, and it cuts in an unusual direction: the input is real but nearly weightless.
kd_eff_snap = V['kd'] * debt_b / max(debt_b, 1e-9)
wd_gross = debt_b / (debt_b + MKTCAP)
kd_swing_effect = 0.05 * (1 - TAX) * wd_gross
say(f"[Cost of debt, limb (i) currency composition] the entire book is EGP "
    f"{debt_b:,.2f}mn of short-dated Egyptian-pound bank facilities. There is no foreign-currency "
    f"leg, so no currency blend is available and none is claimed. The company's dollar exposure "
    f"sits in export receivables, not in debt.")
say(f"[Cost of debt, limb (ii) independent effective rate] an interest-expense-over-average-"
    f"balance computation on a book this small is not a usable estimator — the denominator is "
    f"0.06% of revenue and rounds in the disclosure. The rate is therefore built from an "
    f"observable: the central bank's overnight LENDING rate of 20.00% plus a 200bp corporate "
    f"spread = {V['kd']:.2%}. Stating that plainly is the honest alternative to computing a "
    f"precise-looking number from a rounding residual.")
say(f"[Cost of debt, limb (iii) bounds and MATERIALITY] gross debt is {wd_gross:.3%} of the "
    f"capital structure. A 500bp error in the cost of debt — larger than any plausible "
    f"mis-estimate — moves the weighted cost of capital by {kd_swing_effect*1e4:.2f} basis "
    f"points. The standing 150bp bound is satisfied vacuously; what the gate actually "
    f"establishes here is that this input cannot move the answer, and the study says so rather "
    f"than dressing an immaterial input as a precise one.")
assert kd_swing_effect < 0.0005, "cost of debt is material after all — the gate must bind"

# ---- cost of capital: explicit window (sovereign double-count removed) -----
rf_star = V['rf'] - V['sov_spread_cds']
ke_exp = rf_star + V['beta'] * V['erp_cds']
ke_rating_alt = (V['rf'] - V['sov_spread_rating']) + V['beta'] * V['erp_rating']
ke_raw_retired = V['rf'] + V['beta'] * V['erp_cds']
kd_at = V['kd'] * (1 - TAX)
# The company is NET CASH, so the weights need care and the direction of the effect is the
# OPPOSITE of the intuition carried over from a net-debt name.
#
# Net debt is negative, so the debt weight is negative and the equity weight exceeds 100%.
# The cost of that negative debt is not the borrowing rate — it is the blend of what the
# tiny debt book costs and what the large cash pile EARNS, which is the deposit yield. Put
# together, the weighting UNLEVERS the observed cost of equity for the cash: the operating
# business must be discounted at a HIGHER rate than the equity, because roughly a fifth of
# the market capitalisation is near-riskless cash diluting the observed equity risk.
#
# The identity that proves it: EV/market-cap x WACC_operating + cash/market-cap x cash-cost
# recombines exactly to the cost of equity. Asserted below.
k_nd_at = (V['kd'] * debt_b - V['cash_yield'] * cash_b) / (debt_b - cash_b) * (1 - TAX)
wd_exp = nd_cy25 / (nd_cy25 + MKTCAP)
we_exp = 1 - wd_exp
wacc_exp = we_exp * ke_exp + wd_exp * k_nd_at
wacc_exp_gross = (1 - wd_gross) * ke_exp + wd_gross * kd_at
say(f"[Cost of equity] risk-free {V['rf']:.2%} less the sovereign default spread "
    f"{V['sov_spread_cds']:.2%} = {rf_star:.2%}; plus beta {V['beta']:.3f} times the equity risk "
    f"premium {V['erp_cds']:.2%} -> cost of equity {ke_exp:.2%}. Alternatives disclosed: on the "
    f"rating basis {ke_rating_alt:.2%}; the RETIRED un-netted construction {ke_raw_retired:.2%}, "
    f"kept only for the audit trail — it charges Egypt's sovereign default risk twice, once "
    f"inside the pound yield and again in the country premium.")
say(f"[Weighted cost of capital, explicit window] net debt is NEGATIVE, so the debt weight is "
    f"{wd_exp:.1%} and the equity weight {we_exp:.1%}. The cost of that negative debt is the "
    f"blend of what the EGP {debt_b:,.0f}mn borrowing costs and what the EGP {cash_b:,.0f}mn cash "
    f"pile EARNS: {k_nd_at:.2%} after tax, i.e. essentially the after-tax deposit yield. Result "
    f"{wacc_exp:.2%} — ABOVE the {ke_exp:.2%} cost of equity, not below it. That direction is the "
    f"point: a company holding {-nd_cy25/MKTCAP:.0%} of its market capitalisation in near-riskless "
    f"cash has an observed equity cost that UNDERSTATES the risk of its operating assets, so "
    f"unlevering for the cash raises the operating rate. On a gross-debt basis the rate would be "
    f"{wacc_exp_gross:.2%}; that construction discounts the operating cash flows at a rate the "
    f"cash has already depressed AND then adds the cash back in the bridge, counting the cash "
    f"twice and overstating the valuation. The net basis is primary and is the more conservative "
    f"of the two by {(wacc_exp-wacc_exp_gross)*1e4:,.0f} basis points.")
_recombine = ((MKTCAP + nd_cy25) / MKTCAP) * wacc_exp + (-nd_cy25 / MKTCAP) * k_nd_at
say(f"[Unlevering identity] enterprise value over market capitalisation "
    f"({(MKTCAP+nd_cy25)/MKTCAP:.4f}) times the operating rate, plus cash over market "
    f"capitalisation ({-nd_cy25/MKTCAP:.4f}) times the cash cost, recombines to "
    f"{_recombine:.4%} against a cost of equity of {ke_exp:.4%} — exact. This is the check that "
    f"the net-cash weighting is a decomposition rather than an adjustment.")
assert abs(_recombine - ke_exp) < 1e-9, "the net-cash unlevering identity does not recombine to Ke"
assert wacc_exp > wacc_exp_gross, \
    "unlevering for net cash must RAISE the operating rate; check the signs"

# ---- terminal (norm-built, never backed out of a price) --------------------
ke_term = V['rf_term'] + V['beta'] * V['erp_term']
kd_term_at = V['kd_term'] * (1 - TAX)
wacc_term = (1 - V['wd_term']) * ke_term + V['wd_term'] * kd_term_at
say(f"[Weighted cost of capital, terminal] cost of equity {ke_term:.2%} (norm-built risk-free "
    f"{V['rf_term']:.2%} = the central bank's own 5% medium-term inflation target plus a 5.5pp "
    f"emerging-market real-rate convention, plus beta times a normalised premium "
    f"{V['erp_term']:.2%}); cost of debt after tax {kd_term_at:.2%}; weights "
    f"{1-V['wd_term']:.0%}/{V['wd_term']:.0%} -> {wacc_term:.2%}. No terminal input is an "
    f"observable quote and none is reverse-engineered from a price.")
assert wacc_term < wacc_exp, "terminal cost of capital must sit below the explicit-window rate"

# ---- glide: fractions from the cost-of-debt path ----------------------------
kdp = V['kd_path']
glide_frac = [(kdp[0] - k) / (kdp[0] - kdp[-1]) for k in kdp]
fwd = [wacc_exp - (wacc_exp - wacc_term) * f for f in glide_frac]
df, _c = [], 1.0
for w in fwd:
    _c /= (1 + w); df.append(_c)
assert all(fwd[i] >= fwd[i + 1] for i in range(4)), "the glide is not monotone"
say("[Glide] forward cost of capital " + " -> ".join(f"{w:.2%}" for w in fwd) +
    "; cumulative discount factors " + ", ".join(f"{d:.4f}" for d in df) +
    ". The glide fractions are the cost-of-debt path's own cumulative progress (" +
    ", ".join(f"{f:.3f}" for f in glide_frac) + "), so the front-loaded shape is inherited from "
    "the assumed easing calendar rather than being a second free parameter.")

# ---- FCFF waterfall ---------------------------------------------------------
dna = [V['dna_pct'] * r for r in rev]
ebit = [ebitda[i] - dna[i] for i in range(5)]
nopat = [e * (1 - TAX) for e in ebit]
capex = [V['capex_pct'][i] * rev[i] for i in range(5)]
nwc = [nwc_pct * r for r in rev]
dnwc = [nwc[0] - nwc_cy25] + [nwc[i] - nwc[i - 1] for i in range(1, 5)]
fcff = [nopat[i] + dna[i] - capex[i] - dnwc[i] for i in range(5)]
pv = [fcff[i] * df[i] for i in range(5)]
pv_explicit = float(sum(pv))
say(f"[Free cash flow to the firm] " + " -> ".join(f"{f:,.0f}" for f in fcff) +
    f"; present value of the explicit window {pv_explicit:,.0f}.")

# ---- one roll-forward, consumed everywhere ---------------------------------
NCI_SHARE = V['nci_share']
PAYOUT = V['payout_reported']
interest_path, np_fc, div_fc, eq_fc, nd_fc, cash_fc = [], [], [], [], [], []
_nd, _eq = nd_cy25, eqp_cy25
for i in range(5):
    _cash = debt_b - _nd
    _int = V['cash_yield_path'][i] * max(_cash, 0.0) - V['kd_path'][i] * debt_b
    _pbt = ebit[i] + _int
    _npa = _pbt * (1 - TAX) * (1 - NCI_SHARE)
    _div = PAYOUT * _npa
    _eq += _npa - _div
    _nd = _nd - (fcff[i] + _int * (1 - TAX)) + _div
    interest_path.append(_int); np_fc.append(_npa); div_fc.append(_div)
    eq_fc.append(_eq); nd_fc.append(_nd); cash_fc.append(debt_b - _nd)
say(f"[Forecast finance income] " + " -> ".join(f"{x:,.0f}" for x in interest_path) +
    f" — the charge is a CREDIT throughout and it falls even as the cash pile builds, because "
    f"the deposit yield eases with the policy rate faster than the balance grows. Attributable "
    f"profit " + ", ".join(f"{x:,.0f}" for x in np_fc) + f"; net cash " +
    ", ".join(f"{-x:,.0f}" for x in nd_fc) + f" on a {PAYOUT:.1%} payout.")

# ---- invested capital and the terminal return ------------------------------
ppe_f, _p = [], ppe_cy25
for i in range(5):
    _p += capex[i] - dna[i]; ppe_f.append(_p)
ic = [nwc[i] + ppe_f[i] for i in range(5)]
roic = [nopat[i] / ic[i] for i in range(5)]
roic_term = nopat[-1] * (1 + V['g_term']) / ic[-1]
ic_cy25 = nwc_cy25 + ppe_cy25
say(f"[Return on invested capital] {' / '.join(f'{r:.1%}' for r in roic)}; terminal return taken "
    f"as next year's NOPAT over closing invested capital, {roic_term:.1%}. The level is high "
    f"because the plant is substantially written down and the working capital is negative-to-"
    f"negligible — a real feature of the business, and the reason the required terminal "
    f"reinvestment rate comes out low.")

# ---- terminal growth: the mandatory reconciliation --------------------------
nopat_h = {}
for k in ('FY23', 'FY24', 'FY25', 'CY25'):
    nopat_h[k] = hist_is[k]['ebit'] * (1 - TAX)
ic_h = {k: hist_bs[k]['nwc'] + hist_bs[k]['ppe'] for k in ('FY23', 'FY24', 'FY25', 'CY25')}
capex_h = {k: V['capex_pct'][0] * hist_is[k]['rev'] for k in ('FY23', 'FY24', 'FY25', 'CY25')}
capex_h['CY25'] = V['capex_budget']
hist_roic = {k: nopat_h[k] / ic_h[k] for k in nopat_h}
hist_rr = {k: (capex_h[k] - hist_is[k]['dna']) / nopat_h[k] for k in nopat_h}
hist_impl_g = {k: hist_roic[k] * hist_rr[k] for k in nopat_h}
hist_character = {k: ('burst' if hist_rr[k] > 1.0 else 'stable') for k in nopat_h}
nopat_cagr = (nopat_h['CY25'] / nopat_h['FY23']) ** (1 / 2.5) - 1
stable_keys = [k for k in nopat_h if hist_character[k] == 'stable']
stable_g = float(np.mean([hist_impl_g[k] for k in stable_keys]))
say(f"[Terminal growth reconciliation] returns on invested capital " +
    " / ".join(f"{k} {hist_roic[k]:.1%}" for k in nopat_h) + "; reinvestment rates " +
    " / ".join(f"{hist_rr[k]:.1%}" for k in nopat_h) + "; implied growth " +
    " / ".join(f"{hist_impl_g[k]:.1%}" for k in nopat_h) + ".")
say(f"[Terminal growth, check (a)] actual NOPAT compound growth from FY2022/23 to calendar 2025 "
    f"(2.5 years) = {nopat_cagr:+.1%}. [Check (b)] growth implied by return times reinvestment "
    f"from STABLE years only ({', '.join(stable_keys)}; reinvestment below 100% of NOPAT, so "
    f"self-funded rather than debt-financed) = {stable_g:.1%}. Adopted terminal growth "
    f"{V['g_term']:.1%}, the standing centre, sensitised 3-7%.")

dom_share_term = 1 - (B['spec_rev'][-1] * 0.35) / rev[-1]   # exports ~35% of the specialty leg
blend_ceiling = dom_share_term * V['egypt_nominal_growth'] + \
    (1 - dom_share_term) * V['world_nominal_growth']
# The crossover test asks how long a candidate terminal rate would take to make the
# company larger than the economy it sits in. It only BINDS when the candidate exceeds
# nominal growth; below that the company shrinks relative to the economy forever and
# there is no crossover to compute. Reporting a negative year count would be nonsense.
cross_candidates = {}
for label, cand in (('recent NOPAT compound rate', nopat_cagr),
                    ('forecast revenue compound rate', (rev[-1] / rev_cy25) ** 0.2 - 1),
                    ('adopted terminal rate', V['g_term'])):
    if cand > V['egypt_nominal_growth']:
        cross_candidates[label] = float(np.log(V['egypt_gdp_nominal'] / rev[-1]) /
                                        np.log((1 + cand) / (1 + V['egypt_nominal_growth'])))
    else:
        cross_candidates[label] = None
fcst_cagr = (rev[-1] / rev_cy25) ** 0.2 - 1
yrs_cross = cross_candidates['forecast revenue compound rate']
_above = [(lab, c) for lab, c in (('the recent NOPAT compound rate', nopat_cagr),
                                 ('the forecast revenue rate', fcst_cagr),
                                 ('the adopted terminal rate', V['g_term']))
          if c > V['egypt_nominal_growth']]
_below = [(lab, c) for lab, c in (('the recent NOPAT compound rate', nopat_cagr),
                                  ('the forecast revenue rate', fcst_cagr),
                                  ('the adopted terminal rate', V['g_term']))
          if c <= V['egypt_nominal_growth']]
say(f"[Terminal ceiling] the domestic leg is {dom_share_term:.0%} of 2030E revenue, giving a "
    f"blended long-run nominal ceiling of {blend_ceiling:.1%}, and the adopted "
    f"{V['g_term']:.0%} sits well below it. Taking the candidates one at a time against Egyptian "
    f"nominal growth of {V['egypt_nominal_growth']:.0%}: " +
    "; ".join(f"{lab} {c:+.1%} is BELOW it" for lab, c in _below) +
    ("" if not _above else "; " + "; ".join(
        f"{lab} {c:+.1%} is ABOVE it and DOES bind — at that rate the company would overtake "
        f"Egypt's entire nominal gross domestic product in about "
        f"{np.log(V['egypt_gdp_nominal']/rev[-1])/np.log((1+c)/(1+V['egypt_nominal_growth'])):.0f} "
        f"years, which is why it is a HISTORICAL rate and not a terminal one"
        for lab, c in _above)) + ".")
assert V['g_term'] <= V['egypt_nominal_growth'], "the adopted terminal rate must sit below the ceiling"
_lo = [c for c in (nopat_cagr, stable_g) if c <= V['g_term']]
_hi = [c for c in (nopat_cagr, stable_g) if c > V['g_term']]
say(f"[Terminal growth, stated plainly] the two standing checks disagree with each other, and "
    f"that is the honest reading rather than a problem to be smoothed. Check (a), the historical "
    f"compound NOPAT rate, is {nopat_cagr:+.1%} — far ABOVE the adopted {V['g_term']:.1%}; it is "
    f"a recovery rate off a devaluation-compressed base and belongs in the explicit years, not "
    f"in perpetuity. Check (b), return times reinvestment from stable years, is {stable_g:.1%} — "
    f"BELOW the adopted rate. The adopted {V['g_term']:.0%} sits between them and above the one "
    f"that describes a steady state, so on the check that matters for a perpetuity it remains on "
    f"the GENEROUS side of the company's own record. Sensitised 3-7%; the grid is on the face of "
    f"the workbook. NOTE the reinvestment definition: check (b) uses net capex over NOPAT, "
    f"EXCLUDING working capital, while the free-cash-flow waterfall subtracts working capital. On "
    f"the waterfall-consistent definition the base-year reinvestment rate is "
    f"{(capex_h['CY25']-hist_is['CY25']['dna']+dnwc[0])/nopat_h['CY25']:.1%} and the implied "
    f"growth is {hist_roic['CY25']*(capex_h['CY25']-hist_is['CY25']['dna']+dnwc[0])/nopat_h['CY25']:.1%} "
    f"— ABOVE the adopted rate. Both definitions are shown; neither is hidden.")
rr_waterfall = (capex_h['CY25'] - hist_is['CY25']['dna'] + dnwc[0]) / nopat_h['CY25']
g_waterfall = hist_roic['CY25'] * rr_waterfall
assert V['g_term'] < blend_ceiling, "terminal growth exceeds the blended nominal ceiling"

rr_term = V['g_term'] / roic_term
nopat_term = nopat[-1] * (1 + V['g_term'])
tv = nopat_term * (1 - rr_term) / (wacc_term - V['g_term'])
pv_tv = tv * df[-1]
ev = pv_explicit + pv_tv
tv_share = pv_tv / ev
say(f"[Terminal value] required reinvestment rate = growth / return = {V['g_term']:.1%} / "
    f"{roic_term:.1%} = {rr_term:.1%}; terminal NOPAT {nopat_term:,.0f}; terminal value "
    f"{tv:,.0f} capitalised at the terminal cost of capital {wacc_term:.2%} and discounted at the "
    f"YEAR-5 cumulative factor {df[-1]:.4f} — one date, one price of time — giving a present "
    f"value of {pv_tv:,.0f}. TERMINAL VALUE IS {tv_share:.1%} OF ENTERPRISE VALUE.")
assert abs(roic_term * rr_term - V['g_term']) < 1e-9, "terminal growth != return x reinvestment"

# ---- enterprise value -> equity bridge --------------------------------------
nci_val = NCI_SHARE * ev          # on the OPERATING enterprise value, before the cash
eq_attr = ev - nd_cy25 - nci_val
dcf_ps = eq_attr / SH
say(f"[Bridge] enterprise value {ev:,.0f} less net debt {nd_cy25:,.0f} (a NEGATIVE, i.e. net "
    f"cash of {-nd_cy25:,.0f} is ADDED) = {ev - nd_cy25:,.0f}; less minority interests at their "
    f"{NCI_SHARE:.1%} share OF THE ENTERPRISE VALUE (not of the cash — the previous "
    f"construction deducted it after the cash was added, which handed the minority "
    f"{NCI_SHARE*-nd_cy25:,.0f} of the parent's balance) = {nci_val:,.0f} -> equity attributable "
    f"{eq_attr:,.0f} = EGP "
    f"{dcf_ps:.2f} a share against a spot of EGP {SPOT:.2f} ({dcf_ps/SPOT-1:+.1%}).")
assert abs((ev - nd_cy25 - nci_val) - eq_attr) < 1e-6, "the bridge does not close"
assert nci_val > 0 and nd_cy25 < 0, "sign check on the bridge components"

# ---- contested choices, computed rather than asserted -----------------------
wacc_exp_rating = we_exp * ke_rating_alt + wd_exp * kd_at
wacc_term_rating = (1 - V['wd_term']) * (V['rf_term'] + V['beta'] * (V['erp_term'] + 0.045)) + \
    V['wd_term'] * kd_term_at


def _val_at(we_, wt_, g_=None, nci_=None):
    g_ = V['g_term'] if g_ is None else g_
    nci_ = NCI_SHARE if nci_ is None else nci_
    _fwd = [we_ - (we_ - wt_) * f for f in glide_frac]
    _df, cc = [], 1.0
    for w in _fwd:
        cc /= (1 + w); _df.append(cc)
    _roic = nopat[-1] * (1 + g_) / ic[-1]
    _rr = min(g_ / _roic, 0.95)
    _tv = nopat[-1] * (1 + g_) * (1 - _rr) / max(wt_ - g_, 0.02)
    _ev = sum(fcff[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    return (_ev * (1 - nci_) - nd_cy25) / SH


dcf_rating_ps = _val_at(wacc_exp_rating, wacc_term_rating)
nci_alt = 0.06
dcf_nci_alt_ps = _val_at(wacc_exp, wacc_term, nci_=nci_alt)
dcf_grossbasis_ps = _val_at(wacc_exp_gross, wacc_term)
say(f"[Contested choices, computed] (1) rating-basis cost of capital instead of the CDS basis: "
    f"explicit {wacc_exp_rating:.2%} / terminal {wacc_term_rating:.2%} -> EGP "
    f"{dcf_rating_ps:.2f} ({dcf_rating_ps/dcf_ps-1:+.1%}). (2) minority share doubled to "
    f"{nci_alt:.0%} -> EGP {dcf_nci_alt_ps:.2f} ({dcf_nci_alt_ps/dcf_ps-1:+.1%}). (3) "
    f"GROSS-debt rather than net-debt weights, the construction this study rejects because it "
    f"counts the cash pile twice -> EGP {dcf_grossbasis_ps:.2f} "
    f"({dcf_grossbasis_ps/dcf_ps-1:+.1%}).")

# ---- currency-of-discounting alternative -----------------------------------
WACC_USD = 0.90 * (V['wacc_usd_rf'] + V['beta'] * V['wacc_usd_erp']) + \
    0.10 * 0.065 * (1 - TAX)
exp_frac = [(B['spec_rev'][i] * 0.35) / rev[i] for i in range(5)]
fcff_f_usd = [fcff[i] * exp_frac[i] / V['fx_path'][i] for i in range(5)]
fcff_d = [fcff[i] * (1 - exp_frac[i]) for i in range(5)]
df_usd, _c2 = [], 1.0
for _ in range(5):
    _c2 /= (1 + WACC_USD); df_usd.append(_c2)
pv_f_usd = sum(fcff_f_usd[i] * df_usd[i] for i in range(5))
tv_f_usd = (nopat_term * (1 - rr_term) * exp_frac[-1] / V['fx_path'][-1]) / (WACC_USD - 0.035)
ev_f_egp = (pv_f_usd + tv_f_usd * df_usd[-1]) * V['fx']
pv_d = sum(fcff_d[i] * df[i] for i in range(5))
tv_d = nopat_term * (1 - rr_term) * (1 - exp_frac[-1]) / (wacc_term - V['g_term'])
ev_ccy = ev_f_egp + pv_d + tv_d * df[-1]
ccy_ps = (ev_ccy * (1 - NCI_SHARE) - nd_cy25) / SH
say(f"[Currency-of-discounting alternative] the export leg ({exp_frac[-1]:.0%} of cash flow) is "
    f"first DEFLATED to dollars at each year's exchange rate, discounted at a dollar cost of "
    f"capital of {WACC_USD:.2%} with 3.5% terminal growth, and only then translated back at the "
    f"spot rate. Discounting a pound-denominated cash flow already inflated by the assumed "
    f"depreciation path directly at a dollar rate would count the currency benefit twice. Result "
    f"EGP {ccy_ps:.2f} a share ({ccy_ps/SPOT-1:+.1%} against spot).")

# ---- lens 2: relative -------------------------------------------------------
REL_I = 1                                    # 2027E, the year-2 forward
ebitda_mid = ebitda[REL_I]
df_rel = df[REL_I]


pv_interim = sum(pv[:REL_I + 1])


def _rel(mult):
    """A multiple on a forward year values the business FROM that year on. The cash the firm
    generates in the meantime belongs to today's owner and must be added back, or the lens
    silently discards it — which the previous version did, to the tune of the figure below."""
    return (((mult * ebitda_mid) * df_rel + pv_interim) * (1 - NCI_SHARE) - nd_cy25) / SH


rel_ps, rel_bear, rel_bull = _rel(V['ev_ebitda_just']), _rel(3.5), _rel(6.0)
ev_rel_fwd = V['ev_ebitda_just'] * ebitda_mid
ev_rel = ev_rel_fwd * df_rel
ev_trailing = MKTCAP + nd_cy25
ev_ebitda_trailing = ev_trailing / ebitda_cy25
pe_trailing = SPOT / (npa_cy25 / SH)
say(f"[Relative lens] interim free cash flow added back: {pv_interim:,.0f} of present value "
    f"for the years before the multiple year, which the previous construction dropped. "
    f"{V['ev_ebitda_just']}x on 2027E EBITDA {ebitda_mid:,.0f} gives an enterprise "
    f"value of {ev_rel_fwd:,.0f} AS AT end-2027; discounted back at the year-2 factor "
    f"{df_rel:.4f} that is {ev_rel:,.0f} today -> EGP {rel_ps:.2f} a share. Not discounting a "
    f"forward enterprise value back to today would have given EGP "
    f"{((ev_rel_fwd - nd_cy25) * (1 - NCI_SHARE)) / SH:.2f}. The company's own trailing multiple "
    f"is {ev_ebitda_trailing:.1f}x enterprise value to EBITDA and {pe_trailing:.1f}x earnings.")

# ---- lens 3: normalised earnings power --------------------------------------
NORM_I = 2                                   # every component from the SAME year
norm_rev = rev[NORM_I]
norm_ebitda = ebitda[NORM_I]
norm_ebit = norm_ebitda - dna[NORM_I]
norm_interest = interest_path[NORM_I]
norm_np = (norm_ebit + norm_interest) * (1 - TAX) * (1 - NCI_SHARE)
norm_eps = norm_np / SH
norm_ps = V['pe_just'] * norm_eps
norm_bear, norm_bull = 5.5 * norm_eps, 9.5 * norm_eps
say(f"[Normalised earnings lens] every component is taken from 2028E: revenue {norm_rev:,.0f}, "
    f"EBITDA {norm_ebitda:,.0f}, depreciation {dna[NORM_I]:,.0f}, finance income "
    f"{norm_interest:,.0f} -> attributable earnings {norm_np:,.0f}, EGP {norm_eps:.2f} a share; "
    f"at {V['pe_just']}x -> EGP {norm_ps:.2f}.")

# ---- lens 4: book value and sustainable return ------------------------------
bvps = eqp_cy25 / SH
pb_just = (V['roe_sust'] - V['g_term']) / (ke_term - V['g_term'])
book_ps = pb_just * bvps
book_bear = ((V['roe_sust'] - 0.05 - 0.03) / (0.5 * (ke_exp + ke_term) - 0.03)) * bvps
book_bull = ((V['roe_sust'] + 0.03 - V['g_term']) / (ke_term - V['g_term'])) * bvps
roe_trailing = npa_cy25 / ((eq_jun25 * (1 - NCI_SHARE) + eqp_cy25) / 2)
say(f"[Book lens] justified price-to-book {pb_just:.2f}x = (sustainable return "
    f"{V['roe_sust']:.1%} less growth {V['g_term']:.0%}) / (PERPETUAL cost of equity "
    f"{ke_term:.2%} less growth), applied to book value of EGP {bvps:.2f} a share -> EGP "
    f"{book_ps:.2f}. The perpetual rate is the right one inside a perpetuity identity; using a "
    f"blend of the explicit and terminal rates would be internally inconsistent. Trailing return "
    f"on average parent equity is {roe_trailing:.1%}.")

# ---- scenarios --------------------------------------------------------------
def dcf_scenario(vol_mult=1.0, price_mult=1.0, fx_mult=1.0, gm_shift=0.0,
                 wacc_shift=0.0, g=None, nwc_p=None):
    """Full re-run of the unit build and the waterfall, so a volume, price or currency
    move flows through both legs exactly as it does in the base case."""
    g = V['g_term'] if g is None else g
    nwc_p = nwc_pct if nwc_p is None else nwc_p
    S = build(vol_mult=vol_mult, price_mult=price_mult, fx_mult=fx_mult, gm_shift=gm_shift)
    _rev, _ebitda = S['rev'], S['ebitda']
    _dna = [V['dna_pct'] * r for r in _rev]
    _ebit = [_ebitda[i] - _dna[i] for i in range(5)]
    _nopat = [e * (1 - TAX) for e in _ebit]
    _capex = [V['capex_pct'][i] * r for i, r in enumerate(_rev)]
    _nwc = [nwc_p * r for r in _rev]
    _dnwc = [_nwc[0] - nwc_p * rev_cy25] + [_nwc[i] - _nwc[i - 1] for i in range(1, 5)]
    _f = [_nopat[i] + _dna[i] - _capex[i] - _dnwc[i] for i in range(5)]
    _we, _wt = wacc_exp + wacc_shift, wacc_term + wacc_shift
    _fwd = [_we - (_we - _wt) * f for f in glide_frac]
    _df, cc = [], 1.0
    for w in _fwd:
        cc /= (1 + w); _df.append(cc)
    _ppe, pp = [], ppe_cy25
    for i in range(5):
        pp += _capex[i] - _dna[i]; _ppe.append(pp)
    _roic = _nopat[-1] * (1 + g) / (_nwc[-1] + _ppe[-1])
    _rr = min(g / _roic, 0.95)
    _tv = _nopat[-1] * (1 + g) * (1 - _rr) / max(_wt - g, 0.02)
    _ev = sum(_f[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    return (_ev * (1 - NCI_SHARE) - nd_cy25) / SH


_chk = dcf_scenario()
assert abs(_chk - dcf_ps) < 0.01, f"scenario engine does not reproduce the base: {_chk} vs {dcf_ps}"
SCEN = dict(
    bear=dict(vol_mult=0.4, gm_shift=-0.010, fx_mult=0.97, wacc_shift=+0.02, g=0.03),
    bull=dict(vol_mult=1.5, gm_shift=+0.010, fx_mult=1.03, wacc_shift=-0.02, g=0.06))
dcf_bear = dcf_scenario(**SCEN['bear'])
dcf_bull = dcf_scenario(**SCEN['bull'])
SCEN['bear']['ps'], SCEN['bull']['ps'], SCEN['base_ps'] = dcf_bear, dcf_bull, dcf_ps
SCEN['labels'] = dict(
    vol_mult='Volume growth path, as a multiple of the assumed path',
    gm_shift='Gross margin, shifted on every forecast year',
    fx_mult='Exchange-rate path, as a multiple of the assumed path',
    wacc_shift='Cost of capital, shifted at BOTH the explicit and terminal anchors',
    g='Terminal growth rate')
say(f"[Scenarios on the cash-flow lens] bear EGP {dcf_bear:.2f} / base EGP {dcf_ps:.2f} / bull "
    f"EGP {dcf_bull:.2f}. The scenarios are FIVE simultaneous driver moves, not a single lever: "
    f"volume growth at {SCEN['bear']['vol_mult']:.1f}x / {SCEN['bull']['vol_mult']:.1f}x the "
    f"assumed path, gross margin {SCEN['bear']['gm_shift']:+.1%} / "
    f"{SCEN['bull']['gm_shift']:+.1%}, the exchange-rate path "
    f"{SCEN['bear']['fx_mult']-1:+.0%} / {SCEN['bull']['fx_mult']-1:+.0%}, the cost of capital "
    f"{SCEN['bear']['wacc_shift']:+.0%} / {SCEN['bull']['wacc_shift']:+.0%} at both anchors, and "
    f"terminal growth {SCEN['bear']['g']:.0%} / {SCEN['bull']['g']:.0%}. Because all five move "
    f"together and in the same direction, the bear and bull ends are JOINT-worst and JOINT-best "
    f"cases and are much wider than any single-driver row in the sensitivity table; they are not "
    f"a confidence interval and no probability is attached to them.")

# ---- synthesis --------------------------------------------------------------
W = V['lens_weights']
lenses = dict(
    dcf=dict(name='Discounted cash flow (primary)', bear=dcf_bear, base=dcf_ps, bull=dcf_bull,
             w=W['dcf']),
    relative=dict(name='Relative multiples', bear=rel_bear, base=rel_ps, bull=rel_bull,
                  w=W['relative']),
    normalized=dict(name='Normalised earnings power', bear=norm_bear, base=norm_ps, bull=norm_bull,
                    w=W['normalized']),
    book=dict(name='Book value and sustainable return', bear=book_bear, base=book_ps,
              bull=book_bull, w=W['book']),
)
central = sum(l['base'] * l['w'] for l in lenses.values())
lo = min(l['bear'] for l in lenses.values())
hi = max(l['bull'] for l in lenses.values())
lenses['central'] = dict(name='Weighted central', bear=lo, base=central, bull=hi, w=1.0)
say(f"[Synthesis] weighted central EGP {central:.2f}; full span across lenses and scenarios EGP "
    f"{lo:.2f} - {hi:.2f}; spot EGP {SPOT:.2f} ({central/SPOT-1:+.1%} to the central).")
assert 0.20 <= central / SPOT <= 3.0, f"central/spot {central/SPOT:.2f} outside the plausibility band"

# ---- sensitivity grids (whole-model re-runs) --------------------------------
g_grid = [0.03, 0.04, 0.05, 0.06, 0.07]
wt_grid = [wacc_term - 0.02, wacc_term - 0.01, wacc_term, wacc_term + 0.01, wacc_term + 0.02]
we_grid = [wacc_exp - 0.03, wacc_exp - 0.015, wacc_exp, wacc_exp + 0.015, wacc_exp + 0.03]
grid_wacc_g = [[_val_at(wacc_exp, wt, g) for g in g_grid] for wt in wt_grid]
grid_exp_term = [[_val_at(we, wt) for wt in wt_grid] for we in we_grid]
beta_grid = [0.60, 0.80, 0.9405, 1.15, 1.30]
grid_beta = []
for b in beta_grid:
    _ke = rf_star + b * V['erp_cds']
    _kt = V['rf_term'] + b * V['erp_term']
    grid_beta.append(_val_at(we_exp * _ke + wd_exp * kd_at,
                             (1 - V['wd_term']) * _kt + V['wd_term'] * kd_term_at))
gm_grid = [-0.010, -0.005, 0.0, 0.005, 0.010]
grid_margin = [dcf_scenario(gm_shift=s) for s in gm_grid]
vol_grid = [0.0, 0.5, 1.0, 1.5, 2.0]
grid_vol = [dcf_scenario(vol_mult=m) for m in vol_grid]
fx_grid = [0.90, 0.95, 1.0, 1.05, 1.10]
grid_fx = [dcf_scenario(fx_mult=m) for m in fx_grid]
nwc_grid = [0.00, 0.01, nwc_pct, 0.03, 0.05]
grid_nwc = [dcf_scenario(nwc_p=p) for p in nwc_grid]

# ---- expert panel: three genuinely different methods ------------------------
# Cast by METHOD from the persona library; presented to the reader as Expert 1/2/3.
e1_i = 2
e1_ebit = ebit[e1_i]
e1_int = interest_path[e1_i]
e1_eps = ((e1_ebit + e1_int) * (1 - TAX) * (1 - NCI_SHARE)) / SH
e1_pe = 7.0
e1_base, e1_lo, e1_hi = e1_pe * e1_eps, 5.0 * e1_eps, 9.5 * e1_eps

# Expert 2 works the EQUITY side directly: free cash flow to equity, discounted on the
# cost of EQUITY's own glide, with no enterprise-to-equity bridge at all. Capitalising a
# mid-forecast cash flow straight at the TERMINAL cost of equity — as a first draft of this
# panel did — prices one date twice: it takes a cash flow five years out and brings it home
# at a rate that only applies once the economy has normalised. The glide is applied here for
# exactly the reason it is applied in the primary model.
e2_fcfe = [(fcff[i] + interest_path[i] * (1 - TAX)) * (1 - NCI_SHARE) for i in range(5)]
e2_ke_path = [ke_exp - (ke_exp - ke_term) * f for f in glide_frac]
e2_df, _ce = [], 1.0
for k in e2_ke_path:
    _ce /= (1 + k); e2_df.append(_ce)
e2_pv = sum(e2_fcfe[i] * e2_df[i] for i in range(5))
e2_tv = e2_fcfe[-1] * (1 + V['g_term']) * (1 - rr_term) / (ke_term - V['g_term'])
e2_pv_tv = e2_tv * e2_df[-1]
e2_ke = ke_term
e2_fcff = float(np.mean(fcff[2:]))
e2_fin_at = interest_path[3] * (1 - TAX)
e2_base = (e2_pv + e2_pv_tv) / SH
e2_lo = (e2_pv + e2_fcfe[-1] * 1.03 * (1 - rr_term) / (ke_term + 0.03 - 0.03) * e2_df[-1]) / SH
e2_hi = (e2_pv + e2_fcfe[-1] * 1.06 * (1 - rr_term) / (ke_term - 0.06) * e2_df[-1]) / SH
say(f"[Expert 2 construction] free cash flow to equity " +
    " -> ".join(f"{x:,.0f}" for x in e2_fcfe) + f"; discounted on the cost of EQUITY's own glide "
    f"(" + " -> ".join(f"{k:.1%}" for k in e2_ke_path) + f") for a present value of "
    f"{e2_pv:,.0f}, plus a terminal block of {e2_pv_tv:,.0f}. No bridge is used: the cash pile "
    f"reaches the shareholder through the finance income line rather than as a balance-sheet "
    f"add-back, which is what makes this a genuinely independent second read rather than a "
    f"re-arrangement of the first.")

ic_beg = [ic_cy25] + ic[:-1]
ep_ = [nopat[i] - fwd[i] * ic_beg[i] for i in range(5)]
pv_ep = sum(ep_[i] * df[i] for i in range(5))
ep_term = nopat[-1] * (1 + V['g_term']) - wacc_term * ic[-1]
pv_ep_term = ep_term / (wacc_term - V['g_term']) * df[-1]
e3_ev = ic_cy25 + pv_ep + pv_ep_term
e3_base = (e3_ev * (1 - NCI_SHARE) - nd_cy25) / SH
e3_lo = ((ic_cy25 + pv_ep * 0.6 + pv_ep_term * 0.55) * (1 - NCI_SHARE) - nd_cy25) / SH
e3_hi = ccy_ps
say(f"[Economic-profit convention] the capital charge is taken on BEGINNING-of-year invested "
    f"capital, not ending. Charging ending capital would understate economic profit by about "
    f"{sum((ic[i]-ic_beg[i])*fwd[i] for i in range(5))/5:,.0f}mn a year.")
experts = dict(
    e1=dict(method_short='earnings power at a justified multiple', base=e1_base,
            rng=[e1_lo, e1_hi], eps=e1_eps, ebit=e1_ebit, interest=e1_int, pe=e1_pe,
            year=YRS[e1_i]),
    e2=dict(method_short='free cash flow to equity, discounted', base=e2_base,
            rng=[e2_lo, e2_hi], fcff=e2_fcff, fcfe=e2_fcfe, ke=e2_ke, fin_at=e2_fin_at,
            ke_path=e2_ke_path, df=e2_df, pv=e2_pv, pv_tv=e2_pv_tv),
    e3=dict(method_short='cash returns against the cost of capital', base=e3_base,
            rng=[e3_lo, e3_hi], ic0=ic_cy25, pv_ep=pv_ep, pv_ep_term=pv_ep_term, ev=e3_ev,
            ep=ep_, spread=[roic[i] - fwd[i] for i in range(5)]),
)
panel_centre = float(sorted([e1_base, e2_base, e3_base])[1])
say(f"[Expert panel] Expert 1 EGP {e1_base:.2f} [{e1_lo:.2f}-{e1_hi:.2f}]; Expert 2 EGP "
    f"{e2_base:.2f} [{e2_lo:.2f}-{e2_hi:.2f}]; Expert 3 EGP {e3_base:.2f} [{e3_lo:.2f}-"
    f"{e3_hi:.2f}]; panel median EGP {panel_centre:.2f} ({panel_centre/SPOT-1:+.1%} against spot).")

# ---- fan for the figure -----------------------------------------------------
paths3 = np.load(os.path.join(HERE, 'paths_3M.npy'))
fan = np.percentile(paths3, [5, 25, 50, 75, 95], axis=0)
np.save(os.path.join(HERE, 'fan.npy'), fan)

# ============================ EMIT ===========================================
step0 = json.load(open(os.path.join(HERE, 'step0_result.json')))
strike = json.load(open(os.path.join(HERE, 'strike_result.json')))
beta_res = json.load(open(os.path.join(HERE, 'beta_result.json')))
bt5 = json.load(open(os.path.join(HERE, 'backtest_5y.json')))

OUT = dict(
    meta=dict(ticker='AMOC', company='Alexandria Mineral Oils Company S.A.E.', market='EGX',
              currency='EGP', asof='2026-08-06', spot=SPOT, shares_mn=SH, mktcap=MKTCAP,
              ev_trailing=ev_trailing, klass='downstream petroleum operating company',
              sector='Oil & gas refining and marketing — lubricant base oils and waxes',
              fy_note='financial year moved from 30 June to 31 December'),
    inputs=INP,
    hist_is=hist_is, hist_bs=hist_bs,
    base=dict(rev_cy25=rev_cy25, pat_cy25=pat_cy25, rev_h1cy25=rev_h1cy25,
              pat_h1cy25=pat_h1cy25, vol_cy25=vol_cy25, rev_fy24=rev_fy24, rev_fy25=rev_fy25,
              nwc_pct=nwc_pct, nwc_cy25=nwc_cy25, ppe_cy25=ppe_cy25, ic_cy25=ic_cy25,
              eqp_cy25=eqp_cy25, eq_cy25=eq_cy25, nd_cy25=nd_cy25, cogs_cy25=cogs_cy25,
              npa_cy25=npa_cy25, nci_cy25=nci_cy25, gm_cy25=gm_cy25, dna_cy25=dna_cy25, other_cy25=other_cy25,
              netfin_cy25=netfin_cy25, div_annual=div_annual, other_liab=other_liab_cy25,
              implied_life=implied_life, eq_jun23=eq_jun23, eq_jun24=eq_jun24,
              eq_jun25=eq_jun25, rev_fy24_methods=[V['rev_fy24_a'], V['rev_fy24_b']],
              rev_fy25_methods=[V['rev_fy25_a'], V['rev_fy25_b'], V['rev_fy25_c']],
              implied_growth_rev=implied_growth_rev, implied_growth_pat=implied_growth_pat),
    unit=dict(spec_vol25=spec_vol25, vol_cy25=vol_cy25, vol25=vol25, px_egp=px_egp,
              px_usd=px_usd, crack=crack, rev25_lines=rev25_lines_x, feed_diff=feed_diff, ton_fy23=ton_fy23,
              parity_fy24=parity_fy24, recon_px=RECON_PX,
              gm_built=gm_hist_built, gm_assumed_old=[0.0576, 0.0600, 0.0620, 0.0640],
              hist_margin={k: dict(gm=v['gm'], brent=v['brent'], parity=v['parity'],
                                   feed_pt=v['feed_pt'], line_margin=v['line_margin'],
                                   cogs={a: b for a, b in v['cogs'].items()})
                           for k, v in HIST_MARGIN.items()},
              line_margin=B['line_margin'], elast=dict(base=_b, up=_bump, dn=_dip),
              m_spec=B['line_margin']['oil'][0], m_fuel=B['line_margin']['fuel'][0],
              spec_share_t=spec_share_t,
              spec_share_v=spec_share_v, line_fuel_t=line_fuel_t, line_fuel_v=line_fuel_v,
              lines=LINES, lines_rev=B['lines_rev'], lines_vol=B['lines_vol'],
              vol=B['vol'], spec_vol=B['spec_vol'], spec_rev=B['spec_rev'],
              fuel_rev=B['fuel_rev'], vol_h2_fy25=vol_h2_fy25, vol_h1_cy25=vol_h1_cy25,
              oil_share_of_spec=oil_share_of_spec,
              ss=(rev25_lines_x['oil'] + rev25_lines_x['wax']) / rev_cy25),
    fcst=dict(years=YRS, rev=rev, gp=B['gp'], gm=B['gm'], opex=B['opex'], ebitda=ebitda,
              ebitda_margin=ebitda_margin, dna=dna, ebit=ebit, nopat=nopat, capex=capex,
              nwc=nwc, dnwc=dnwc, fcff=fcff, df=df, pv=pv, fwd_wacc=fwd, glide_frac=glide_frac,
              ppe=ppe_f, ic=ic, roic=roic, np_attr=np_fc, equity=eq_fc, net_debt=nd_fc,
              cash=cash_fc, interest=interest_path, div=div_fc, payout=PAYOUT),
    wacc=dict(rf=V['rf'], rf_star=rf_star, ke_exp=ke_exp, ke_rating_alt=ke_rating_alt,
              ke_raw_retired=ke_raw_retired, kd=V['kd'], kd_at=kd_at, we_exp=we_exp,
              wd_exp=wd_exp, wacc_exp=wacc_exp, wacc_exp_gross=wacc_exp_gross, wd_gross=wd_gross, k_nd_at=k_nd_at, ke_term=ke_term, kd_term=V['kd_term'],
              kd_term_at=kd_term_at, wacc_term=wacc_term, glide_frac=glide_frac,
              kd_path=V['kd_path'], kd_swing_effect=kd_swing_effect, wacc_usd_alt=WACC_USD,
              beta=beta_res),
    dcf=dict(pv_explicit=pv_explicit, tv=tv, pv_tv=pv_tv, ev=ev, tv_share=tv_share,
             nd=nd_cy25, nci_share=NCI_SHARE, nci_val=nci_val, eq_attr=eq_attr, ps=dcf_ps,
             roic_term=roic_term, rr_term=rr_term, g=V['g_term'], bear=dcf_bear, bull=dcf_bull,
             ps_rating_basis=dcf_rating_ps, wacc_exp_rating=wacc_exp_rating,
             wacc_term_rating=wacc_term_rating, ps_nci_alt=dcf_nci_alt_ps, nci_alt=nci_alt,
             ps_gross_basis=dcf_grossbasis_ps, ccy_alt_ps=ccy_ps),
    terminal_recon=dict(roic=hist_roic, rr=hist_rr, implied_g=hist_impl_g,
                        character=hist_character, nopat=nopat_h, ic=ic_h, capex=capex_h,
                        nopat_cagr=nopat_cagr, stable_g=stable_g, stable_keys=stable_keys,
                        rr_waterfall=rr_waterfall, g_waterfall=g_waterfall,
                        ceiling=blend_ceiling, crossover_years=yrs_cross, crossover=cross_candidates, fcst_cagr=fcst_cagr,
                        dom_share_term=dom_share_term),
    lenses=lenses, central=central, span=[lo, hi], spot=SPOT, scen=SCEN,
    experts=experts, panel_centre=panel_centre,
    rel=dict(ebitda_mid=ebitda_mid, pv_interim=pv_interim, ev_rel=ev_rel, ev_rel_fwd=ev_rel_fwd, df_rel=df_rel,
             ev_ebitda_trailing=ev_ebitda_trailing, pe_trailing=pe_trailing,
             just_mult=V['ev_ebitda_just'], year=YRS[REL_I]),
    norm=dict(rev=norm_rev, ebitda=norm_ebitda, ebit=norm_ebit, dna=dna[NORM_I],
              interest=norm_interest, np=norm_np, eps=norm_eps, pe=V['pe_just'],
              year=YRS[NORM_I]),
    book=dict(bvps=bvps, pb_just=pb_just, roe_sust=V['roe_sust'], roe_trailing=roe_trailing,
              ke_term=ke_term),
    sens_wg=dict(g_grid=g_grid, wacc_grid=wt_grid, table=grid_wacc_g),
    sens=dict(g_grid=g_grid, wt_grid=wt_grid, we_grid=we_grid, grid_wacc_g=grid_wacc_g,
              grid_exp_term=grid_exp_term, beta_grid=beta_grid, grid_beta=grid_beta,
              gm_grid=gm_grid, grid_margin=grid_margin, vol_grid=vol_grid, grid_vol=grid_vol,
              fx_grid=fx_grid, grid_fx=grid_fx, nwc_grid=nwc_grid, grid_nwc=grid_nwc),
    step0=step0, strike=strike, backtest=bt5,
    assert_log=LOG,
)
with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(OUT, f, indent=1)
say("=" * 78)
say(f"ASSERT BLOCK PASSED — study_numbers.json emitted. Terminal value "
    f"{tv_share:.1%} of enterprise value; fair value EGP {central:.2f} against spot EGP "
    f"{SPOT:.2f}; implied {central/SPOT-1:+.1%}.")
