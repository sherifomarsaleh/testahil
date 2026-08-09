"""BOROUGE — external-context inputs: macro, cost-of-capital and peer-market figures.

Nothing in this file is a source for any Borouge reported historical figure. Under the
source-integrity mandate the company's own past income statement, balance sheet and cash
flow come only from its own issued statements (inputs_company.py). What lives here is
external context and forecast drivers: rates, premia, inflation, industry multiples and
sector betas — each read from the original publisher's own file, not from a summary of it.

Two lookups in particular were made against the ORIGINAL published file rather than a
secondary report of it, because that is where they go wrong:

  * the country risk premium and equity risk premium come from Damodaran's own
    ctryprem.html, and the United Arab Emirates row was read out of that file directly;
  * the risk-free rate comes from the Final Terms document of the UAE Ministry of
    Finance's own Treasury Bond issue, read from the filing. An automated summary of the
    same document reported it as a USD 2 billion note at a 4.375% yield. It is not: it is
    an AED 550 million five-year bond issued at par with a 3.90% coupon. The filing was
    opened and read rather than trusted second hand.
"""

def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)


DAMO = ("Aswath Damodaran, 'Country Default Spreads and Risk Premiums', "
        "pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html, "
        "file last updated 5 January 2026, United Arab Emirates row read from the "
        "original file")
DAMO_US = ("Aswath Damodaran, same file, United States row: Aa1, adjusted default "
           "spread 0.23%, country risk premium 0.23%, equity risk premium 4.46%, "
           "sovereign CDS 0.30%")
DAMO_BETA = ("Aswath Damodaran, 'Betas by Sector (Global)', "
             "pages.stern.nyu.edu/~adamodar/pc/datasets/betaGlobal.xls, Industry "
             "Averages sheet, file dated 5 January 2026, Chemical (Basic) row: 909 "
             "firms, levered beta 1.2560, D/E 0.5048, effective tax rate 14.72%, "
             "unlevered beta 0.9123, cash/firm value 8.96%, unlevered beta corrected "
             "for cash 1.0021")
DAMO_EV = ("Aswath Damodaran, 'EV/EBITDA Multiples by Sector (Global)', "
           "pages.stern.nyu.edu/~adamodar/pc/datasets/vebitdaGlobal.xls, Industry "
           "Averages sheet, file dated 5 January 2026")
MOF = ("Government of the United Arab Emirates acting through the Ministry of Finance, "
       "Final Terms dated 29 January 2026, Treasury Bonds Programme, Series "
       "AED01826C264: aggregate face amount AED 550,000,000, issue price 100%, issue "
       "date 29 January 2026, maturity date 29 January 2031, coupon 3.90% fixed per "
       "annum payable semi-annually; listed on Nasdaq Dubai")
CBUAE = ("Central Bank of the United Arab Emirates, Quarterly Economic Review, "
         "March 2026")
NYFED = ("Secured Overnight Financing Rate as published by the Federal Reserve Bank of "
         "New York")

MAC = dict(

    # ---------------- risk-free rate: two currencies, both published ----------
    # The valuation runs in US dollars because Borouge reports, sells, buys its
    # feedstock and borrows in US dollars. The risk-free rate is therefore built on the
    # US dollar curve and NORMALISED the way Damodaran's own method specifies: the
    # Treasury yield less the United States' own default spread, because the US is no
    # longer rated Aaa. Country risk then enters exactly once, inside the UAE equity
    # risk premium — never twice.
    ust_10y=I(0.0465, "US 10-year Treasury note yield, 4.65% on 7 August 2026",
              "2026-08-07", "Global"),
    us_default_spread=I(0.0023, DAMO_US, "2026-01-05", "Global"),

    # The local-currency construction, published beside it. The dirham is hard-pegged,
    # so in theory these two should meet; observed, they do not, and the study says so
    # rather than quietly choosing the flattering one.
    uae_govt_yield_aed=I(0.0448, "UAE Ministry of Finance July 2026 Treasury Bond and "
                         "Sukuk auction, reported by the Emirates News Agency (WAM): the "
                         "January-2031 T-Bond cleared at a yield to maturity of 4.48%, a "
                         "spread of 4 basis points over the comparable US Treasury; AED "
                         "1.1 billion issued against AED 4.83 billion of bids, 4.4 times "
                         "covered. This is the SECONDARY-market-clearing yield on the "
                         "same bond whose Final Terms are cited below, and it supersedes "
                         "the January issue coupon as the current local risk-free "
                         "observation. " + MOF, "2026-07-30", "Country"),
    uae_govt_yield_aed_issue_coupon=I(0.0390, MOF + ". Carried as the issue-date "
                                      "observation; the same bond yielded 4.30% at the "
                                      "May 2026 auction and 4.48% at the July 2026 "
                                      "auction, so the local curve rose materially across "
                                      "the first half of 2026", "2026-01-29", "Country"),
    uae_default_spread_rating=I(0.0042, DAMO + " — Moody's rating Aa2, adjusted default "
                                "spread 0.42%", "2026-01-05", "Country"),

    # ---------------- equity risk premium: both published bases ---------------
    uae_crp=I(0.0064, DAMO + " — country risk premium 0.64%", "2026-01-05", "Country"),
    uae_erp_rating=I(0.0487, DAMO + " — total equity risk premium 4.87%, being the "
                     "mature-market premium plus a country risk premium scaled by "
                     "relative equity-market volatility", "2026-01-05", "Country"),
    mature_erp=I(0.0423, DAMO_US + "; the mature-market equity risk premium is the US "
                 "equity risk premium of 4.46% less the US default spread of 0.23%, "
                 "which is 4.23%, and the same 4.23% is recovered from the UAE row as "
                 "4.87% less the 0.64% country risk premium", "2026-01-05", "Global"),
    # The second basis: the unadjusted default-spread add-on, which Damodaran names in
    # the same file as "standard practice". The sovereign-CDS basis, which the house
    # method would otherwise publish as the second, DOES NOT EXIST for the UAE: the
    # original file prints "NA" in both the sovereign CDS and CDS-based ERP columns.
    uae_erp_default_spread_basis=I(0.0465, "Mature-market equity risk premium of 4.23% "
                                   "plus the UAE adjusted default spread of 0.42%, the "
                                   "construction Damodaran describes in the same file "
                                   "as standard practice. " + DAMO,
                                   "2026-01-05", "Country"),
    uae_cds_available=I(0.0, DAMO + " — the sovereign CDS and the CDS-based equity risk "
                        "premium columns both read NA for the United Arab Emirates, so "
                        "a CDS-basis cost of capital cannot be published for this "
                        "sovereign and none is invented", "2026-01-05", "Country"),

    # ---------------- cost of debt ------------------------------------------
    sofr=I(0.0365, NYFED + ", 3.65% for 6 August 2026", "2026-08-06", "Global"),
    cbuae_base_rate=I(0.0365, "Central Bank of the UAE Base Rate, held at 3.65% since "
                      "17 June 2026; the dirham peg means the Base Rate tracks the "
                      "Federal Reserve's policy path", "2026-06-17", "Country"),

    # ---------------- sector beta, from the original file --------------------
    sector_unlevered_beta=I(1.0021, DAMO_BETA + ". Chemical (Basic) is the right row: "
                            "Borouge sells commodity polyethylene and polypropylene "
                            "against published Northeast Asia benchmarks, not specialty "
                            "formulations", "2026-01-05", "Industry"),
    sector_unlevered_beta_diversified=I(0.9101, "Same file, Chemical (Diversified) row, "
                                        "unlevered beta corrected for cash, shown as the "
                                        "adjacent classification", "2026-01-05",
                                        "Industry"),

    # ---------------- peer multiples: three independent anchors --------------
    # Trailing multiples across this sector are currently distorted: global polyolefin
    # EBITDA is at a cyclical trough, so the denominator collapses and the printed
    # multiple explodes. LyondellBasell's own trailing figure is 24.0x against a
    # ten-year median of 7.18x on the same measure and the same publisher. The lens is
    # therefore built on THROUGH-CYCLE anchors and says so.
    peer_lyb_ltm=I(24.00, "GuruFocus, LyondellBasell EV-to-EBITDA (trailing twelve "
                   "months) of 24.00 as at 7 August 2026, reported by the same source "
                   "as 234% above its ten-year median", "2026-08-07", "Industry"),
    peer_lyb_10y_median=I(7.18, "GuruFocus, LyondellBasell ten-year median EV/EBITDA",
                          "2026-08-07", "Industry"),
    peer_lyb_forward=I(6.5, "Wells Fargo research note on LyondellBasell, cited in an "
                       "Investing.com report of the upgrade, applying a 2026 EV/EBITDA "
                       "multiple of approximately 6.5x to an adjusted EBITDA outlook of "
                       "USD 6.5 billion. Third-party opinion, used only as one of three "
                       "through-cycle anchors", "2026-03-19", "Industry"),
    peer_iqcd=I(9.90, "TradingView / PitchBook company profile, Industries Qatar "
                "(QE: IQCD) enterprise value to EBITDA of 9.90 as at 2 July 2026. "
                "Industries Qatar is the closest listed Gulf comparator: a "
                "state-affiliated producer of ethylene, polyethylene and other "
                "petrochemicals on advantaged regional feedstock", "2026-07-02",
                "Industry"),
    peer_sector_ev_ebitda=I(8.655, DAMO_EV + ", Chemical (Diversified) row, EV/EBITDA "
                            "8.655x across 63 firms", "2026-01-05", "Industry"),
    # The full listed peer set, observed together on one date. It is carried in the
    # study as a TABLE rather than collapsed to a median, because a median of it would
    # be dishonest: nine of the eleven names are loss-making on a trailing basis, two
    # have undefined EV/EBITDA because their EBITDA is negative, and three more print
    # inflated multiples only because the denominator collapsed. Aggregator-sourced and
    # used only as the cross-check the source-integrity mandate permits.
    peer_table=I({
        'SABIC (Tadawul 2010)': dict(ev_ebitda=10.83, pe_fwd=24.65, pb=1.02,
                                     div_yield=0.0435, ebitda_margin=0.1393,
                                     profit_margin=-0.1974, loss_making=True),
        'Saudi Kayan (2350)': dict(ev_ebitda=32.52, pe_fwd=None, pb=0.99,
                                   div_yield=0.0, ebitda_margin=0.0604,
                                   profit_margin=-0.3014, loss_making=True),
        'Yansab (2290)': dict(ev_ebitda=12.24, pe_fwd=33.04, pb=1.61,
                              div_yield=0.0669, ebitda_margin=0.2035,
                              profit_margin=0.0494, loss_making=False),
        'Industries Qatar (IQCD)': dict(ev_ebitda=9.90, pe_fwd=17.04, pb=1.86,
                                        div_yield=0.0638, ebitda_margin=None,
                                        profit_margin=None, loss_making=False),
        'LyondellBasell (LYB)': dict(ev_ebitda=12.96, pe_fwd=7.42, pb=1.80,
                                     div_yield=0.0463, ebitda_margin=0.0765,
                                     profit_margin=-0.0113, loss_making=True),
        'Dow Inc (DOW)': dict(ev_ebitda=13.39, pe_fwd=13.74, pb=1.34,
                              div_yield=0.0477, ebitda_margin=0.0658,
                              profit_margin=-0.0313, loss_making=True),
        'Westlake (WLK)': dict(ev_ebitda=None, pe_fwd=20.34, pb=1.14,
                               div_yield=0.0274, ebitda_margin=-0.0066,
                               profit_margin=-0.1094, loss_making=True),
        'Braskem (BAK)': dict(ev_ebitda=None, pe_fwd=None, pb=None,
                              div_yield=None, ebitda_margin=-0.0006,
                              profit_margin=-0.1368, loss_making=True),
        'Formosa Plastics (1301)': dict(ev_ebitda=55.97, pe_fwd=14.80, pb=0.91,
                                        div_yield=0.0090, ebitda_margin=0.0157,
                                        profit_margin=-0.0401, loss_making=True),
        'LG Chem (051910)': dict(ev_ebitda=13.39, pe_fwd=15.48, pb=0.43,
                                 div_yield=0.0072, ebitda_margin=0.1003,
                                 profit_margin=-0.0452, loss_making=True),
        'Petronas Chemicals (PCHEM)': dict(ev_ebitda=22.92, pe_fwd=21.18, pb=0.97,
                                           div_yield=0.0156, ebitda_margin=0.0512,
                                           profit_margin=-0.0642, loss_making=True),
    }, "stockanalysis.com company statistics pages, all eleven observed 9 August 2026, "
        "except Industries Qatar, whose figures come from TradingView and PitchBook "
        "profiles carrying no precise observation date and should be read as "
        "approximately July-August 2026. AGGREGATOR-SOURCED market data, used only as a "
        "relative-multiple cross-check and never as a source for any reported financial "
        "figure", "2026-08-09", "Industry"),
    peer_borouge_market=I({'ev_ebitda': 12.02, 'pe_trailing': 24.01, 'pe_fwd': 9.19,
                           'div_yield': 0.0675, 'ebitda_margin': 0.3305,
                           'shares_out_bn': 29.75},
                          "stockanalysis.com, Borouge plc statistics page observed 9 "
                          "August 2026. Shown for contrast against the peer table: "
                          "Borouge's 33.05% EBITDA margin against a peer set clustered "
                          "between zero and 14% is the whole question the ground-up "
                          "build has to answer from the feedstock position and the "
                          "product premia. Aggregator-sourced, cross-check only",
                          "2026-08-09", "Market"),

    # ---------------- country macro -----------------------------------------
    uae_cpi=I(0.021, "Central Bank of the UAE, Quarterly Economic Review, June 2026: "
              "inflation forecast of 2.3% for 2026 and 1.9% for 2027; the model carries "
              "the 2.1% average of the two as the escalator for domestic cost lines. "
              "NOTE: there is no retrievable UAE NATIONAL consumer price index — the "
              "Central Bank publishes emirate-level series only (Abu Dhabi +1.4% year on "
              "year for January-February 2026, Dubai +3.7% for January-April 2026). "
              "Dubai's June 2026 print of +5.7% is running well above the Central Bank's "
              "own full-year forecast, which was set on a 12 May 2026 cut-off, so this "
              "escalator is more likely too low than too high", "2026-06-30", "Country"),
    uae_gdp_growth_cbuae=I(0.017, "Central Bank of the UAE, Quarterly Economic Review, "
                           "June 2026 — real GDP growth of 6.2% actual for 2025, "
                           "forecast 1.7% for 2026 and 9.8% for 2027, the collapse and "
                           "rebound reflecting the conflict and the recovery of oil "
                           "output", "2026-06-30", "Country"),
    uae_gdp_growth_imf=I(0.031, "International Monetary Fund country page, April 2026 "
                         "World Economic Outlook vintage — UAE real GDP growth of 3.1% "
                         "for 2026, against 5.0% in the October 2025 vintage. Reported "
                         "beside the Central Bank's own 1.7% because the two genuinely "
                         "disagree by 1.4 percentage points and averaging them would "
                         "hide that", "2026-04-30", "Country"),
    global_growth_imf=I(0.030, "International Monetary Fund, World Economic Outlook "
                        "Update, July 2026, 'Global Economy in Crosscurrents of War and "
                        "Technology', published 8 July 2026, Table 1: global growth of "
                        "3.0% in 2026 and 3.4% in 2027, against 3.5% in each of 2024 and "
                        "2025", "2026-07-08", "Global"),
    hormuz_mou=I(1.0, "United States-Iran Memorandum of Understanding signed 18 June "
                 "2026 to end the conflict and reopen the Strait of Hormuz, recorded in "
                 "the US Energy Information Administration Short-Term Energy Outlook, "
                 "July 2026 edition. The EIA expects most shut-in crude production back "
                 "near pre-conflict averages by the end of 2026 and the majority back "
                 "online in the first quarter of 2027. This is the dated, external basis "
                 "on which the normalisation framing rests — it is an agreement, not a "
                 "completed restoration of traffic, and Borouge's own July guidance "
                 "still makes recovery conditional on freedom of navigation",
                 "2026-06-18", "Global"),
    brent_eia=I(82.0, "US Energy Information Administration, Short-Term Energy Outlook, "
                "July 2026: Brent spot averaging USD 69/bbl in 2025, USD 82/bbl in 2026 "
                "and USD 65/bbl in 2027; June 2026 actual USD 85/bbl, down USD 32/bbl "
                "from the April 2026 peak", "2026-07-31", "Global"),
    pe_capacity_growth=I(0.22, "Global polyethylene nameplate capacity rising 22% "
                         "between 2026 and 2034, from 158 million tonnes to 193 million "
                         "tonnes, per OPIS in the Asia Petrochemical Industry Conference "
                         "compiled proceedings of 29 May 2026, hosted by the Singapore "
                         "Chemical Industry Council. ICIS material in the same "
                         "proceedings states polyethylene capacity additions exceed "
                         "demand growth until 2030", "2026-05-29", "Industry"),
    pp_capacity_growth=I(0.20, "Global polypropylene capacity rising 20% between 2026 "
                         "and 2034, from 125 million tonnes to 151 million tonnes, per "
                         "OPIS in the same Asia Petrochemical Industry Conference "
                         "proceedings", "2026-05-29", "Industry"),
    operating_rate_recovery_year=I(2032.0, "Producer consensus on the return to "
                                   "1992-2021 average operating rates moved out to 2032, "
                                   "from 2030 a year earlier — ICIS Asian Chemical "
                                   "Connections, 'Five Forecasts for Global Chemical "
                                   "Markets in 2026', January 2026. This is why the "
                                   "forecast benchmark path settles below the 2023-2024 "
                                   "level rather than returning to it", "2026-01-31",
                                   "Industry"),
    uae_corporate_tax=I(0.09, DAMO + " — corporate tax rate column, 9.00%. Borouge's own "
                        "effective rate is far above this because its Abu Dhabi "
                        "operations are taxed under a separate concession-style regime; "
                        "the model uses the company's own disclosed effective rate, not "
                        "this headline", "2026-01-05", "Country"),

    # ---------------- model parameters, each justified -----------------------
    terminal_growth=I(0.020, "Long-run nominal growth in US dollars for a producer whose "
                      "owned capacity is fixed. Borouge plc owns no part of the Borouge 4 "
                      "expansion, so terminal growth cannot embed volume expansion; 2.0% "
                      "is a price-and-mix rate, below the 4.42% normalised risk-free and "
                      "below long-run global nominal growth. Sensitised across 1.0% to "
                      "3.0% in the study and in the workbook", "2026-08-09", "Model"),
    terminal_roc=I(0.120, "Terminal return on capital. Borouge earned a return on "
                   "invested capital in the high teens across the three audited years on "
                   "advantaged ethane feedstock; 12.0% carries a deliberate competitive "
                   "erosion toward the level a global polyolefin producer can defend "
                   "once the current capacity wave is absorbed, while staying above the "
                   "cost of capital. It sets the terminal reinvestment rate as growth "
                   "divided by return on capital rather than as a free assumption",
                   "2026-08-09", "Model"),
    maintenance_capex=I(320.0, "Steady-state maintenance capital expenditure, USD "
                        "million a year. The three audited years ran 199, 167 and 308; "
                        "2026 is guided below 300. The forecast carries 320 from 2027 "
                        "because the 2025 reassessment of asset useful lives defers "
                        "replacement spending without removing it, and a plant running "
                        "above nameplate consumes maintenance faster than one running "
                        "below it", "2026-08-09", "Model"),
    ethane_contract_real_escalation=I(0.0, "Real escalation on contracted ethane "
                                      "feedstock. Borouge does not publish the pricing "
                                      "formula of its ADNOC feedstock arrangement, so no "
                                      "escalator can be sourced; the model holds the "
                                      "contracted leg flat in real terms and flags this "
                                      "as an unsourced driver. It is recorded as a "
                                      "negative search result, not as a finding",
                                      "2026-08-09", "Model"),
    # ---------------- the Borouge 4 operator economics -----------------------
    # Borouge plc owns NO part of Borouge 4. It operates and markets the plant for its
    # owners in return for a fee. That is not nothing, and the sponsors have quantified
    # it, so it is valued as a separate stream rather than either ignored or wrongly
    # consolidated as owned capacity.
    b4_owner_adnoc=I(0.70, "ADNOC press release, 'ADNOC and OMV advance formation of "
                     "Borouge Group International AG', 19 March 2026 — Borouge 4 is "
                     "owned 70% by ADNOC and 30% by OMV, and is NOT owned by Borouge "
                     "plc", "2026-03-19", "Company"),
    b4_cumulative_net_profit_3y=I(400.0, "ADNOC press release, 19 March 2026 — the Asset "
                                  "Usage Agreement is expected to deliver Borouge plc "
                                  "USD 400 million of cumulative net profit over the "
                                  "next three years", "2026-03-19", "Company"),
    b4_accretion_post_rampup=I(0.10, "ADNOC press release, 19 March 2026 — approximately "
                               "10% annual earnings accretion to Borouge plc after "
                               "Borouge 4 ramp-up", "2026-03-19", "Company"),
    b4_capacity=I(1400.0, "Borouge 4 adds 1.4 million tonnes per annum of polyethylene, "
                  "making Ruwais the world's largest single-site polyolefin complex — "
                  "ADNOC and OMV completion releases. Borouge plc markets this volume "
                  "but does not own the capacity, so it never enters the unit build",
                  "2026-03-31", "Industry"),
    b4_recontribution=I(2029.0, "ADNOC press release, 19 March 2026 — recontribution of "
                        "Borouge 4 into Borouge Group International is 'not expected "
                        "before 2029', deferred from an original expectation of "
                        "end-2026. Any model built before 19 March 2026 carries the old "
                        "date", "2026-03-19", "Company"),
    bgi_ownership_omv=I(0.50, "OMV press release, 'OMV and XRG complete transactions to "
                        "create Borouge International', 31 March 2026 — at completion "
                        "Borouge Group International is held 50% by OMV and 50% by XRG, "
                        "a wholly owned ADNOC subsidiary, under joint control. The "
                        "46.94/46.94/6.12 split announced on 4 March 2025 was a "
                        "pro-forma structure contingent on Borouge plc's free float "
                        "accepting an exchange that has not happened. Borouge plc "
                        "minorities were NOT rolled in and Borouge plc remains "
                        "separately listed on ADX", "2026-03-31", "Company"),
    bgi_tender_year=I(2027.0, "ADNOC (19 March 2026) and OMV (31 March 2026) — a tender "
                      "offer converting Borouge plc shares into Borouge Group "
                      "International AG shares is expected in 2027, subject to market "
                      "conditions, a BGI equity raise and Securities and Commodities "
                      "Authority approval. NO EXCHANGE RATIO AND NO IMPLIED VALUATION "
                      "OF BOROUGE PLC HAS BEEN PUBLISHED as at 9 August 2026; this was "
                      "verified as absent across all three primary announcements rather "
                      "than assumed", "2026-03-19", "Company"),
    analyst_consensus_target=I(2.78, "Consensus of 13 analysts, average target price AED "
                               "2.78, reported by stockanalysis.com on 9 August 2026; a "
                               "second panel of 5 analysts on Investing.com averages AED "
                               "2.66 with a high of AED 3.048 and a low of AED 2.299. "
                               "THIRD-PARTY OPINION, recorded for contrast only and used "
                               "in no calculation", "2026-08-09", "Market"),

    nci_value=I(26.832, "Non-controlling interests carried at their book value of USD "
                "26.832 million from the FY2025 audited balance sheet. The minority "
                "holds 0.9% of group profit, so a market-value uplift on it would not "
                "move the per-share result at the second decimal", "2025-12-31", "Model"),
)
