"""ADNOCDIST (ADNOC Distribution PJSC, ADX) — four-ring Information Sweep register.

Runs BEFORE any forecast driver is set. Every mandatory category of every ring is
closed by a dated finding or a dated negative search.

SOURCING NOTE, recorded rather than hidden: the company's OWN investor-relations site
was reachable and is the build source for every historical figure — three complete
audited consolidated years (FY2023, FY2024, FY2025), the FY2022 comparative column
inside the FY2023 filing, and both 2026 reviewed interims, plus the management
discussion reports and results presentations that carry the operating data no financial
statement contains. The Central Bank of the UAE's EIBOR page was NOT reachable: it
answers automated access with HTTP 403. That is why the marginal cost of debt is built
from the sovereign bond yield plus the company's own disclosed credit margin, and why
that construction is recorded here rather than presented as a live interbank rate.

PROVENANCE DISCIPLINE, stated once: fuel volumes, station and store counts, transaction
counts, segment EBITDA, cash opex, capex and INVENTORY GAINS appear in NO financial
statement — they are management-discussion and results-presentation measures only.
They are tagged COMPANY_IR with is_fs_data=False. Only audited/reviewed statement line
items carry is_fs_data=True, and those are COMPANY_OFFICIAL without exception.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-08-09"
R = SweepRegister("ADNOCDIST", AssetClass.STOCK, SWEEP_DATE)

CO, IR, REG, PMD, PRESS, AGG = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
                                SourceType.REGULATOR_OFFICIAL, SourceType.PRIMARY_MARKET_DATA,
                                SourceType.REPUTABLE_PRESS, SourceType.AGGREGATOR)

IR_SITE = "https://www.adnocdistribution.ae/en/investor-relations"
IR_DOWNLOADS = "https://www.adnocdistribution.ae/en/investor-relations/downloads"
CTRYPREM = "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html"

# ---- primary-source access, logged whether it succeeded or failed -------------
R.record_primary_access(
    IR_SITE, True, SWEEP_DATE,
    "The company's own investor-relations site was reachable and returned all audited "
    "financial statements and interim filings directly — no aggregator or press source "
    "stands between this study and the subject's reported historicals.")

R.record_primary_access(
    IR_DOWNLOADS, True, SWEEP_DATE,
    "The downloads page listed every filing by year and was the route to the FY2023, "
    "FY2024 and FY2025 audited consolidated financial statements and to both 2026 "
    "reviewed interim statements, together with the management discussion reports, the "
    "results presentations and the 2025 integrated report.")

R.record_primary_access(
    "https://www.centralbank.ae/en/forex-eibor/eibor-rates/", False, SWEEP_DATE,
    "NOT REACHABLE: the Central Bank of the UAE's EIBOR page returned HTTP 403 to "
    "automated access. This study's own egress proxy was checked and reported healthy "
    "with no relay failures, so this is the site's own bot protection rather than a "
    "network fault on our side. CONSEQUENCE: the marginal cost of debt was built from "
    "the sovereign bond yield plus the company's OWN disclosed credit margin (borrowings "
    "note: EIBOR + 0.60% on the dirham tranche) instead of from a live interbank rate. "
    "The construction is disclosed as such and sensitised, not presented as observed.")

R.record_primary_access(
    CTRYPREM, True, SWEEP_DATE,
    "The original country default spreads and risk premiums file was reachable and the "
    "January 2026 vintage United Arab Emirates row was read from it directly — not from "
    "a summary, a repost or a third-party table.")

R.declare_study_year("2026", ["Q1-2026", "Q2-2026"])

# ================================================================ RING 1 GLOBAL
g_rates = R.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "The Federal Open Market Committee held the federal funds target range at 3.50%-3.75% "
    "on 29 July 2026. The vote was 9-3, and all three dissents were for a QUARTER-POINT "
    "INCREASE, not a cut. The ten-year United States Treasury stood at 4.68%. Because the "
    "dirham is pegged to the dollar, the Central Bank of the UAE held its own base rate at "
    "3.65% the same day",
    "Federal Reserve Board statement of 29 July 2026; Central Bank of the UAE base-rate "
    "announcement of 29 July 2026", REG, "2026-07-29",
    url="https://www.federalreserve.gov/newsevents/pressreleases/monetary20260729a.htm",
    model_impact="Sets the direction of travel for every rate in the build. The dirham peg "
                 "means the discount rate cannot be forecast down on an easing assumption: "
                 "the risk-free rate is carried flat off the observed local-currency "
                 "sovereign yield and the floating-rate debt cost is escalated, not "
                 "declined. A rising-rate path is the opposite of a standard emerging-market "
                 "cost-of-capital glide and is priced explicitly rather than assumed away.")

g_crude = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.S,
    "Brent stood at USD 83.55 a barrel on 7 August 2026, 25.5% above a year earlier, after a "
    "year that ran from about USD 63 in January to a peak near USD 126 in April on the Iran "
    "conflict and the Strait of Hormuz closure, back below USD 70 in late June, above USD 100 "
    "on 23 July and down to the low eighties in early August. The official short-term energy "
    "outlook published in July 2026 forecasts Brent averaging USD 74 in the third quarter of "
    "2026, USD 70 in the fourth and USD 65 through 2027",
    "Brent spot quotation 7 August 2026; United States Energy Information Administration "
    "July 2026 Short-Term Energy Outlook", REG, "2026-07-07",
    url="https://www.eia.gov/outlooks/steo/pdf/steo_full.pdf",
    model_impact="Drives the whole price side of the revenue build. The regulated UAE retail "
                 "price is a monthly pass-through of average global prices plus operating "
                 "costs, so the crude path IS the realised-price-per-litre path. The official "
                 "forecast of mean reversion to USD 65 is the reason the first half of 2026 "
                 "realised price is NOT carried forward; the price path converges back toward "
                 "the pre-shock band instead.")

g_trade = R.add(Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.S,
    "Refined-product cracks reached records in 2026: the prompt NYMEX 3-2-1 crack hit USD "
    "64.58 a barrel on 8 July 2026 and European diesel margins passed USD 60 a barrel after "
    "Russia halted diesel exports during a domestic fuel crisis worsened by strikes on its "
    "refineries; European gasoline traded at a four-year-high premium of USD 41 a barrel over "
    "crude. Separately, the Strait of Hormuz disruption is the single event behind the 2026 "
    "crude path",
    "Reported refining-margin data for 2026, including the record NYMEX 3-2-1 crack of 8 July "
    "2026", PRESS, "2026-07-23",
    url="https://www.forbes.com/sites/garthfriesen/2026/07/23/refining-stocks-soar-as-crack-spread-hits-record-high-in-2026/",
    model_impact="Cracks are an input cost to this company, which buys finished product from "
                 "its parent rather than refining it. But the monthly pricing formula counts "
                 "international refining margins explicitly, so cracks flow into the retail "
                 "price as well. The cost stack therefore escalates product cost on its own "
                 "crude-plus-crack path and NEVER on domestic consumer inflation — one "
                 "escalator per physically distinct driver class.")

g_ev = R.add(Ring.GLOBAL, "global sector demand", FindingClass.D,
    "Global electric passenger-car sales passed 20 million units in 2025 and reached 25% of "
    "all new car sales for the first time; 23 million units and about 28% of sales are "
    "projected for 2026",
    "International Energy Agency Global EV Outlook 2026, published May 2026", REG,
    "2026-05-01", url="https://www.iea.org/reports/global-ev-outlook-2026/executive-summary",
    model_impact="The outer bound on long-run fuel-volume growth and therefore the anchor for "
                 "the terminal growth rate. It is applied as a SALES-share fact that must be "
                 "converted into a PARC-share drag before it touches volumes — the UAE fleet "
                 "turns over slowly, so the effect inside the explicit forecast is small and "
                 "the exposure sits in the terminal value.")

g_nonfuel = R.add(Ring.GLOBAL, "global sector demand", FindingClass.D,
    "At United States convenience and fuel-retail peers, inside sales generate roughly 70% to "
    "78% of gross profit on about 22% of revenue: fuel runs at a 2% to 4% gross margin, "
    "in-store merchandise at 32% to 38% and foodservice at 48% to 58%. Against that, this "
    "company's non-fuel gross profit was USD 140 million in the first half of 2026 versus "
    "total half-year EBITDA of USD 786 million",
    "Convenience-store industry margin and mix data, February 2026; peer corporate releases",
    REG, "2026-02-11",
    url="https://www.raymondjames.com/-/media/rj/dotcom/files/corporations-and-institutions/investment-banking/industry-insight/convenience_store_insight.pdf",
    model_impact="Sets the ceiling the non-fuel leg is forecast toward and shows how far below "
                 "it the company sits today. The non-fuel driver is therefore built as its own "
                 "leg on disclosed transaction counts and store-level gross margin, growing "
                 "toward — never to — the peer benchmark inside the explicit window.")

g_neg_steo = R.add_negative(Ring.GLOBAL, "commodity complex (input/output)",
    "The official Short-Term Energy Outlook PDF itself, sought directly at eia.gov: the file "
    "returned binary content that could not be parsed and the outlook's own price tables page "
    "returned no data. The Brent forecasts of USD 70 for the fourth quarter of 2026 and USD 65 "
    "for 2027 therefore rest on reporting of that outlook rather than on the tables read "
    "first-hand, and the crude path is sensitised rather than fixed on a single point",
    SWEEP_DATE)

# =============================================================== RING 2 COUNTRY
c_rf = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.D,
    "The UAE federal dirham-denominated Treasury Bond maturing January 2031 cleared at 4.48% "
    "at the July 2026 auction, a spread of just 4 basis points over comparable United States "
    "Treasuries; the October 2027 Treasury Sukuk tranche cleared at 4.49%, 24 basis points "
    "over. Bids totalled AED 4.83 billion against AED 1.1 billion issued. NO 10-YEAR DIRHAM "
    "FEDERAL BOND EXISTS, so this roughly four-and-a-half-year point is the longest sourced "
    "local-currency anchor available",
    "UAE Ministry of Finance July 2026 Treasury Sukuk and Bonds auction results", REG,
    "2026-07-30", url="https://www.wam.ae/en/article/c1hd5hx-treasury-sukuk-bonds-auctions-attract-aed",
    model_impact="THE risk-free anchor, and a local-currency government yield exactly as the "
                 "cost-of-capital method requires — never a dollar shortcut, even under a peg. "
                 "It is normalised by the sovereign's own adjusted default spread so country "
                 "risk enters once, through the country premium inside the equity risk premium. "
                 "The tenor shortfall is disclosed as a construction wherever a ten-year point "
                 "is needed, never presented as an observed yield.")

c_macro = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.S,
    "UAE consumer price inflation averaged 1.3% in 2025 and the December 2025 reading was 2.04% "
    "year on year; the central bank forecasts 1.8% for 2026 and 2.0% for 2027. The dirham is "
    "pegged to the dollar and the central bank base rate stands at 3.65%. The 2026 inflation "
    "forecast predates the more-than-60% retail fuel price surge since late February 2026, and "
    "transport is a consumer-price component",
    "Central Bank of the UAE Quarterly Economic Review, March 2026", REG, "2026-03-01",
    url="https://www.centralbank.ae/media/lgnfakgc/qer-march_2026.pdf",
    model_impact="The escalator for GENUINELY DOMESTIC cost lines only — station wages, local "
                 "services, site running costs. It is explicitly NOT applied to product cost or "
                 "any globally traded input, which escalate on their own commodity path. Its "
                 "pre-shock vintage is why the domestic escalator is carried at the upper end "
                 "of the forecast range rather than at the printed 1.8%.")

c_damodaran = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through",
    FindingClass.D,
    "The January 2026 country risk file, read from the original source, gives the United Arab "
    "Emirates a Moody's rating of Aa2, an adjusted default spread of 0.42%, a country risk "
    "premium of 0.64% and a total equity risk premium of 4.87%, against a mature-market premium "
    "of 4.23% implied by the United States row (4.46% total less a 0.23% default spread). Abu "
    "Dhabi carries an IDENTICAL row. Sharjah does not — 2.13% spread and a 7.47% equity risk "
    "premium — and neither does Ras Al Khaimah at 5.78%. The UAE is not one risk block",
    "Country default spreads and risk premiums file, United Arab Emirates row, header vintage "
    "'Last updated: January 5, 2026', read live from the original file on 9 August 2026", REG,
    "2026-01-05", url=CTRYPREM,
    model_impact="The cost-of-equity input. Because the Abu Dhabi row is identical to the "
                 "federal row, no emirate-level adjustment is applied to this Abu Dhabi-"
                 "domiciled issuer — and that is a sourced finding, not a convenience. Country "
                 "risk enters ONCE, through the 0.64% premium already inside the 4.87% figure; "
                 "the local sovereign yield is stripped of the SAME rating basis of default "
                 "spread that is added back, and both equity-risk-premium bases are published.")

c_ratings = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through",
    FindingClass.C,
    "All three sovereign ratings are current and all sit in the AA band with stable outlooks: "
    "Moody's Aa2 affirmed 12 June 2026, S&P AA with A-1+ short term affirmed 6 March 2026, and "
    "Fitch AA-minus affirmed 23 May 2026",
    "Sovereign rating affirmations reported through 2026", PRESS, "2026-06-12",
    url="https://www.thenationalnews.com/business/economy/2026/06/12/uae-moodys-rating/",
    model_impact="")

c_tax = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.S,
    "The UAE domestic minimum top-up tax sets a 15% minimum effective rate on UAE profits and "
    "applies to financial years beginning on or after 1 January 2025, for multinational groups "
    "with consolidated global revenue of EUR 750 million or more; the federal headline rate is "
    "9% above AED 375,000 of taxable profit, and the upstream extraction carve-out does not "
    "reach a downstream retailer. BUT THE COMPANY'S OWN AUDITED FY2025 TAX RECONCILIATION "
    "RECONCILES AT THE 9% DOMESTIC RATE for a 10.2% effective rate, applies the transitional "
    "country-by-country reporting safe harbour, and records NO top-up tax; both 2026 interims "
    "repeat that no significant top-up impact is anticipated",
    "UAE Ministry of Finance domestic minimum top-up tax guidance and Cabinet Decision No. 142 "
    "of 2024, read against the company's own audited FY2025 tax note", REG, "2025-02-11",
    url="https://mof.gov.ae/en/public-finance/tax/uae-domestic-minimum-top-up-tax/",
    model_impact="Sets the forecast tax rate in the free-cash-flow waterfall. THE BASE CASE "
                 "FOLLOWS THE FILING — a low-double-digit effective rate built off the 9% "
                 "domestic rate plus the disclosed overseas-rate difference — because the "
                 "company's own audited reconciliation, not the regime description, is the "
                 "evidence. The 15% minimum is priced as a stated sensitivity showing the full "
                 "value effect, so a reader can see the consequence of the safe harbour lapsing "
                 "after 31 December 2027 without the study having chosen for them.")

c_neg_tenor = R.add_negative(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    "A ten-year dirham federal government bond, sought across the Ministry of Finance auction "
    "programme, the central bank and market quotation sources. NONE EXISTS: the UAE has not "
    "issued a ten-year local-currency federal bond, and the longest observed federal dirham "
    "point is the January 2031 tranche at roughly four and a half years. Any ten-year "
    "local-currency point in this study is therefore an extrapolation, disclosed as such",
    SWEEP_DATE)

c_neg_imf = R.add_negative(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    "A 2026 International Monetary Fund Article IV consultation for the UAE. Only the October "
    "2025 consultation was located, so every official 2026-2027 growth forecast available "
    "predates the 2026 oil shock entirely. Those forecasts are cited with their vintage stated "
    "and are not used as a volume driver",
    SWEEP_DATE)

c_neg_erp = R.add_negative(Ring.COUNTRY, "fiscal / political events with sector read-through",
    "The July 2026 vintage of the United Arab Emirates country-risk row, sought in the ORIGINAL "
    "file. A July 2026 update exists and was published on 3 July 2026 with a mature-market "
    "premium of 4.17%, but the canonical file itself still reads 'Last updated: January 5, "
    "2026' and its UAE row could not be verified at the July vintage. A third-party figure of "
    "4.99% was found, CONTRADICTS the original file and is NOT USED. The study takes the "
    "January 2026 row from the original file, states the vintage, and carries the premium "
    "choice as a published sensitivity",
    SWEEP_DATE)

# ============================================================== RING 3 INDUSTRY
i_price = R.add(Ring.INDUSTRY, "pricing", FindingClass.S,
    "UAE retail fuel prices are SET MONTHLY BY A GOVERNMENT FUEL PRICE COMMITTEE, chaired by "
    "the Undersecretary of the Ministry of Energy, which announces the following month's prices "
    "on the 28th as average global prices plus operating costs, weighing benchmark crude, "
    "international refining margins and domestic operating costs by grade. The prices are "
    "UNIFORM NATIONALLY AND ACROSS ALL RETAILERS, so THERE IS NO RETAIL PRICE COMPETITION in "
    "UAE fuel — share is won on network and convenience alone. August 2026 Special 95 was AED "
    "3.49 a litre; the 2026 path ran from AED 2.33 in February to AED 3.83 in June, against a "
    "tight AED 2.46-2.77 band through the whole of 2025",
    "UAE Government portal on fuel-price deregulation and the monthly pricing committee; "
    "announced monthly price schedules for 2025 and 2026, August 2026 effective 1 August", REG,
    "2026-08-01",
    url="https://u.ae/en/information-and-services/environment-and-energy/water-and-energy/energy-and-fuel-prices/deregulation-of-fuel-prices",
    model_impact="The single most consequential external driver. Revenue per litre is a "
                 "formulaic pass-through, not a competitive outcome, so it is forecast off the "
                 "crude-and-crack path rather than off a market-share or pricing-power "
                 "assumption. It is also why the 2025 AED 2.46-2.77 band, not the August 2026 "
                 "AED 3.49, is the anchor for the normalised-earnings lens and the terminal "
                 "year — and why a peer set of price-competitive United States retailers is "
                 "read with care.")

i_saudi = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "The Saudi network grew 65% year on year to 231 stations at the half year, on a "
    "CAPITAL-LIGHT DEALER-OWNED, COMPANY-OPERATED model — 161 stations contracted under it, of "
    "which 52 were operational under the group's own brand at end-June 2026 against 1 a year "
    "earlier. The total network reached 1,045 stations (569 UAE, 231 Saudi, 245 Egypt) against "
    "939 a year earlier, and the company targets 1,150 by 2028. Saudi petroleum retail requires "
    "ministry licensing under the Petroleum and Petrochemical Materials Law, which is forcing "
    "sub-scale independents to upgrade or exit",
    "Half-year 2026 management discussion report and results presentation; Saudi Ministry of "
    "Energy licensing regime", IR, "2026-08-05",
    url=IR_DOWNLOADS,
    model_impact="The Saudi leg is modelled as its OWN driver leg — contracted sites times "
                 "throughput times a dealer margin — never blended into UAE unit economics, "
                 "because the dealer-owned model consumes almost no capital and earns a thinner "
                 "per-site margin. Its growth is tied to a regulatory consolidation window, so "
                 "above-trend site additions are carried for a stated number of years and then "
                 "faded, rather than extrapolated to the terminal year.")

i_parc = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "UAE registered vehicles reached 4.56 million by June 2025, up 9.35% year on year — some "
    "390,000 additional vehicles — with new registrations of about 157,000 in the first half of "
    "2025, up 11%. Dubai alone reports up to 3.5 million vehicles circulating in daytime hours, "
    "up 10% in two years. AGAINST THAT, the company's own fuel volumes grew 1.6% in the first "
    "half of 2026",
    "UAE Ministry of Interior and Dubai Roads and Transport Authority registration data as "
    "reported for June 2025", PRESS, "2025-06-30",
    url="https://www.khaleejtimes.com/uae/transport/traffic-390000-vehicles-roads-12-months",
    model_impact="The gap between a 9% vehicle parc and 1.6% realised volumes is the reason the "
                 "volume driver is NOT parc-based. Volume is built from the company's own "
                 "disclosed segment litres and site count; the parc series enters only as a "
                 "plausibility ceiling, with the divergence — fleet efficiency, price "
                 "elasticity after a 60% price rise, and mix — resolved explicitly in the driver "
                 "discussion rather than averaged over. Its June 2025 vintage is stated.")

i_ev = R.add(Ring.INDUSTRY, "technology substitution", FindingClass.S,
    "Electric-vehicle charging points in the UAE reached 406 at the half year, up 35% from 301 "
    "a year earlier, with a target of 500 to 750 by 2028 and 50 to 60 additions in 2026 alone. "
    "The national policy targets about 10% of vehicles ON THE ROAD electric by 2030 and 50% by "
    "2050, with a 42,000-vehicle government fleet by 2030",
    "Half-year 2026 management discussion report; UAE National Electric Vehicles Policy", IR,
    "2026-08-05", url=IR_DOWNLOADS,
    model_impact="The substitution threat to the volume base, and it is modelled as a "
                 "PARC-SHARE drag, never a new-sales-share drag: a 10% parc target for 2030 is a "
                 "low-single-digit cumulative volume effect inside the explicit forecast, and "
                 "the real exposure sits in the terminal value. The charging build is carried as "
                 "the partial offset it is — a growing but still small gross-profit line, not a "
                 "replacement for fuel margin.")

i_comp = R.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.S,
    "Three operators hold about 85% of UAE retail fuel volumes: this company, the largest, "
    "present in all seven emirates; ENOC with 198 stations as at 2024, including the former "
    "EPPCO sites, which are an ENOC brand and NOT a fourth competitor; and Emarat with roughly "
    "100 stations across Dubai and the Northern Emirates. TotalEnergies also competes in UAE "
    "retail. Because prices are uniform by regulation, a competitor PRICE move is structurally "
    "impossible — only capacity moves exist. In Saudi Arabia the listed competitors are Aldrees "
    "Petroleum and Transport Services and Saudi Automotive Services",
    "UAE fuel-station market structure and competitor corporate disclosures, 2024-2025", AGG,
    "2025-12-31",
    url="https://www.mordorintelligence.com/industry-reports/united-arab-emirates-fuel-station-market",
    model_impact="Supports a stable UAE market-share assumption in the volume driver with low "
                 "competitive-erosion risk, and simultaneously CAPS organic UAE volume upside — "
                 "which is why the growth legs in this model are Saudi, Egypt and the proposed "
                 "South African acquisition, not the home market. EPPCO is explicitly not "
                 "modelled as a separate competitor.")

i_peers = R.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.D,
    "Same-day peer multiples: Aldrees Petroleum and Transport Services at 12.89 times enterprise "
    "value to EBITDA on a 9.93% return on invested capital and a 1.64% profit margin; Saudi "
    "Automotive Services 12.28 times; Couche-Tard 10.66; Casey's General Stores 22.41; Murphy "
    "USA 10.03; OMV Petrom 9.91; Vibra Energia 7.70; Ultrapar 6.80. The subject trades at 10.93 "
    "times on a 50.7% return on invested capital and an 8.73% margin. The peer band runs 6.8 to "
    "22.4 times",
    "Same-day market statistics for the peer set, 9 August 2026", AGG, "2026-08-09",
    url="https://stockanalysis.com/quote/tadawul/4200/statistics/",
    model_impact="Feeds the relative lens, and it is built as a RANGE with a stated applicable "
                 "end rather than a blended median — a 3-times spread driven by non-fuel mix and "
                 "country risk makes a single median meaningless. Only Aldrees is treated as a "
                 "like-for-like comparable, on enterprise value to EBITDA rather than earnings, "
                 "because its large low-margin transport business distorts the earnings axis.")

i_neg_entrants = R.add_negative(Ring.INDUSTRY, "new entrants (named-competitor level)",
    "A named new entrant to UAE fuel retail during 2025 or 2026, sought across the market "
    "structure research, competitor corporate sites and 2026 news. NONE WAS FOUND: the market "
    "remains the same three incumbents at about 85% of volumes plus TotalEnergies, and the "
    "licensing and land constraints on new service stations are the reason. The same search "
    "could not refresh the ENOC (2024) or Emarat (undated) station counts to a 2026 vintage, and "
    "no 2025 or 2026 UAE electric-vehicle share of NEW car sales could be sourced — the only "
    "figure located is a 2023 vintage of about 13%, which is not used",
    SWEEP_DATE)

i_neg_unlisted = R.add_negative(Ring.INDUSTRY, "competitor capacity / price moves (named)",
    "Traded equity multiples for Jio-bp and Puma Energy, both requested as peers. NEITHER IS "
    "LISTED: Jio-bp is an unlisted Reliance and BP joint venture — the 2026 Reliance listing in "
    "the pipeline is the telecom entity, a different company — and Puma Energy is "
    "Trafigura-controlled and reaches public markets through debt only. Neither enters the peer "
    "table, and eight listed comparables were obtained without them",
    SWEEP_DATE)

i_neg_prices = R.add_negative(Ring.INDUSTRY, "pricing",
    "A complete month-by-month 2025 UAE retail price series published by the Ministry of Energy "
    "itself. Only five 2025 months could be located from the monthly announcements, plus the "
    "full-year Special 95 range of AED 2.46-2.77; the complete 2026 monthly series was obtained "
    "but from a compiled tracker of the committee's announcements rather than from the "
    "ministry's own publication. The normalised price anchor is therefore built on the 2025 "
    "RANGE, which is directly sourced, rather than on a monthly average of a reconstructed "
    "series, and the April-May 2026 diesel print is carried with its provenance flagged",
    SWEEP_DATE)

# =============================================================== RING 4 COMPANY
k_fs25 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "Audited consolidated financial statements for the year ended 31 December 2025, with the "
    "auditor's report and full notes, obtained from the company's own investor-relations "
    "downloads page. Revenue AED 35,896,617 thousand; gross profit AED 6,945,790 thousand; "
    "operating profit AED 3,505,604 thousand; profit before tax AED 3,173,933 thousand; income "
    "tax AED 322,891 thousand; profit attributable to equity holders AED 2,794,000 thousand; "
    "earnings per share AED 0.224 on 12,497,785 thousand weighted-average shares",
    "Audited consolidated financial statements FY2025", CO, "2026-02-01", url=IR_DOWNLOADS,
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="The first of the modelled history years and the base the forecast rolls "
                 "forward from. Every historical income-statement, balance-sheet and cash-flow "
                 "line in this study is the audited consolidated figure or a disclosed note to "
                 "it — no vendor, broker or press number enters the subject's own historicals.")

k_fs24 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "Audited consolidated financial statements for the year ended 31 December 2024, obtained "
    "from the same source and cross-confirmed against the comparative column of the FY2025 "
    "filing. Revenue AED 35,453,716 thousand; operating profit AED 3,068,895 thousand; profit "
    "attributable to equity holders AED 2,420,275 thousand",
    "Audited consolidated financial statements FY2024", CO, "2025-02-01", url=IR_DOWNLOADS,
    is_fs_data=True, fiscal_period="FY2024",
    model_impact="Second modelled history year; supplies the prior-year base for every growth "
                 "rate and the comparative that validates the FY2025 filing line by line.")

k_fs23 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "Audited consolidated financial statements for the year ended 31 December 2023, obtained "
    "from the same source and cross-confirmed against the comparative column of the FY2024 "
    "filing. Revenue AED 34,629,178 thousand; operating profit AED 2,983,249 thousand; profit "
    "attributable to equity holders AED 2,601,421 thousand; income tax of only AED 18,837 "
    "thousand, the last year before the federal corporate tax regime bit fully",
    "Audited consolidated financial statements FY2023", CO, "2024-02-01", url=IR_DOWNLOADS,
    is_fs_data=True, fiscal_period="FY2023",
    model_impact="Third modelled history year, and the year that shows the tax step-up: an "
                 "effective rate near zero in FY2023 against 10.3% and 10.2% in the two years "
                 "since. The forecast tax rate is set off the post-regime years, not the "
                 "three-year average.")

k_fs22 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2022 audited figures, taken from the COMPARATIVE COLUMN of the FY2023 audited filing "
    "rather than from any restated summary: revenue AED 32,111,061 thousand, of which retail "
    "fuel AED 20,308,082 thousand, retail non-fuel AED 1,149,929 thousand, commercial corporate "
    "AED 9,603,265 thousand and aviation AED 1,049,785 thousand; operating profit AED 2,973,416 "
    "thousand; profit AED 2,748,508 thousand with NO income tax charge printed",
    "Audited consolidated financial statements FY2023, FY2022 comparative column", CO,
    "2024-02-01", url=IR_DOWNLOADS, is_fs_data=True, fiscal_period="FY2022",
    model_impact="The fourth audited year, which lifts the history to the target depth rather "
                 "than the floor. It supplies a pre-tax-regime margin and a four-year revenue "
                 "mix series for the normalised-earnings lens, and it is cited to the filing's "
                 "own comparative column, never to an aggregator's restatement.")

k_tax = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "The audited tax note reconciles at the 9% UAE domestic rate in FY2023, FY2024 and FY2025. "
    "FY2025: profits subject to tax AED 3,173,933 thousand, tax at the domestic rate AED 285,654 "
    "thousand, plus non-deductible items AED 3,503 thousand, a transfer-pricing adjustment AED "
    "3,376 thousand, an overseas-rate difference of AED 25,723 thousand and other items AED "
    "4,635 thousand, giving AED 322,891 thousand and a 10.2% effective rate against 10.3% in "
    "FY2024. The note states that for FY2025 the group applied the transitional "
    "country-by-country reporting safe harbour, that its jurisdictional effective rate exceeded "
    "15%, and that NO top-up tax arose; relief runs to 31 December 2027",
    "Taxation note, audited consolidated financial statements FY2025 and FY2024", CO,
    "2026-02-01", url=IR_DOWNLOADS, is_fs_data=True, fiscal_period="FY2025",
    model_impact="Fixes the forecast tax rate off the company's OWN realised reconciliation "
                 "rather than off the regime description — a low-double-digit effective rate "
                 "built as 9% domestic plus the disclosed overseas-rate difference. The safe "
                 "harbour's 2027 expiry is what makes the 15% minimum a dated, priced "
                 "sensitivity rather than a hypothetical.")

k_debt = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "The borrowings note discloses THE COMPANY'S OWN CREDIT MARGINS: variable interest at the "
    "Secured Overnight Financing Rate plus 0.85% on the dollar-denominated portion and EIBOR "
    "plus 0.60% on the dirham-denominated portion, on a term loan refinanced on 26 October 2022 "
    "for a further five-year term and since converted to a sustainability-linked facility with "
    "ESG covenants tied to the margin. Balances at 31 December 2025: term loan AED 5,499,591 "
    "thousand non-current plus AED 46,384 thousand short-term, AED 5,545,975 thousand in total. "
    "Parent revolving facilities of USD 375,000 thousand and AED 1,377,188 thousand were "
    "undrawn at both 31 December 2025 and 30 June 2026, and the Egyptian subsidiary holds three "
    "one-year EGP 1,000,000 thousand facilities priced off the Central Bank of Egypt corridor",
    "Borrowings note, audited consolidated financial statements FY2025 and the reviewed interim "
    "statements to 30 June 2026", CO, "2026-02-01", url=IR_DOWNLOADS, is_fs_data=True,
    fiscal_period="FY2025",
    model_impact="THIS IS WHAT MAKES THE MARGINAL COST OF DEBT A SOURCED FIGURE RATHER THAN AN "
                 "ASSUMPTION, and it is the reason the blocked interbank page did not stop the "
                 "build: the dirham cost of debt is the sovereign yield plus the company's own "
                 "disclosed 0.60% margin, which sits above the sovereign as the method requires, "
                 "and the Egyptian tranche is carried at its local-equivalent cost rather than "
                 "at a raw foreign coupon.")

k_rev = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "The audited revenue disaggregation splits revenue by line of business for all four years — "
    "FY2025 retail fuel AED 22,796,987 thousand, retail non-fuel AED 1,783,747 thousand, "
    "commercial corporate AED 9,571,682 thousand and aviation AED 1,744,201 thousand — and the "
    "IFRS 8 note reports two segments with revenue, direct costs, gross profit and operating "
    "profit each: FY2025 retail gross profit AED 5,217,283 thousand on AED 24,580,734 thousand "
    "of revenue and commercial gross profit AED 1,728,507 thousand on AED 11,315,883 thousand. "
    "The parent supplies the great majority of product: related-party purchases were AED "
    "22,125,902 thousand of AED 28,696,068 thousand of materials cost, and the supply agreement "
    "gives protection against per-litre gross profit falling below specified levels",
    "Revenue and segment notes and the related-party note, audited consolidated financial "
    "statements FY2025 with FY2024, FY2023 and FY2022 comparatives", CO, "2026-02-01",
    url=IR_DOWNLOADS, is_fs_data=True, fiscal_period="FY2025",
    model_impact="Gives the audited revenue and gross-profit denominators that, divided by the "
                 "separately disclosed litres, produce a REALISED PRICE PER LITRE and a MARGIN "
                 "PER LITRE for each of the retail and commercial legs. Without this note the "
                 "build would be a blended growth rate; with it, both legs are volume times "
                 "price with an independently checkable unit margin.")

k_q1 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Reviewed interim consolidated financial statements for the three months ended 31 March "
    "2026, published 13 May 2026. Borrowings AED 5,534,430 thousand; the UAE corporate tax "
    "component of the charge AED 76,255 thousand against AED 63,866 thousand a year earlier, "
    "struck at a 9% weighted-average annual rate; segment note and taxation note both present",
    "Reviewed interim consolidated financial statements, three months ended 31 March 2026", CO,
    "2026-05-13", url=IR_DOWNLOADS, is_fs_data=True, fiscal_period="Q1-2026",
    model_impact="The first quarter of the study year, swept in BEFORE the build rather than "
                 "discovered after it. It resets the FY2026 opening tax and finance-cost run "
                 "rates and confirms the 9% weighted-average rate carries into the study year.")

k_q2 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.B,
    "Reviewed interim consolidated financial statements for the six months ended 30 June 2026, "
    "published 5 August 2026 — the second quarter of the study year, also already disclosed. "
    "Borrowings AED 5,598,547 thousand; the UAE corporate tax component AED 210,816 thousand "
    "against AED 132,791 thousand a year earlier at the same 9% weighted-average rate. Note 25 "
    "discloses the South African acquisition agreement as an event AFTER the reporting date",
    "Reviewed interim consolidated financial statements, six months ended 30 June 2026", CO,
    "2026-08-05", url=IR_DOWNLOADS, is_fs_data=True, fiscal_period="Q2-2026",
    model_impact="The second quarter of the study year and the base the forecast is struck "
                 "from. It resets the FY2026 revenue, tax and finance-cost paths onto realised "
                 "half-year outturn instead of a full-year estimate, and it is the filing that "
                 "puts the South African transaction on the record as a post-balance-sheet "
                 "event — outside the base case by construction.")

k_vols = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "THE RESULTS PRESENTATIONS AND MANAGEMENT DISCUSSION REPORTS DISCLOSE FUEL VOLUMES SPLIT "
    "RETAIL AND COMMERCIAL, and at the half year split commercial into corporate and aviation "
    "as well, with a GCC-versus-Egypt geography split on each. FY2025 total 15,710 million "
    "litres — retail 11,042, commercial 4,668 of which corporate 4,181 and aviation 487 — "
    "against 15,029 million litres in FY2024. First half 2026 total 7,748 million litres "
    "(retail 5,376, corporate 2,015, aviation 357) against 7,624 a year earlier, +1.6%. A "
    "product split is also given: FY2025 gasoline 8,668, diesel 5,741, aviation 487, other 814. "
    "NONE OF THIS APPEARS IN ANY FINANCIAL STATEMENT",
    "FY2025 and half-year 2026 management discussion reports and results presentations", IR,
    "2026-08-05", url=IR_DOWNLOADS, fiscal_period="Q2-2026",
    model_impact="THIS IS WHAT CONVERTS THE REVENUE BUILD FROM TOP-DOWN TO VOLUME TIMES PRICE. "
                 "Divided into the audited segment revenue and gross profit it yields a realised "
                 "price per litre and a margin per litre for each leg, each grown separately — "
                 "volume on site count and throughput, price on the regulated pass-through path. "
                 "Without it there is no ground-up build, only a growth assertion.")

k_kpi = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "The same channel carries the rest of the operating dataset, none of it in any financial "
    "statement: 1,045 service stations at the half year against 939; 541 convenience stores; "
    "UAE fuel transactions of 100.9 million in the half, up 4.9%, and non-fuel transactions of "
    "26.4 million; GCC throughput of 12.5 million litres per station in FY2025; convenience-"
    "store GCC revenue AED 1,059 million and gross profit AED 393 million at a 37.1% margin in "
    "FY2025; segment EBITDA of AED 3,142 million retail and AED 1,163 million commercial in "
    "FY2025; cash operating costs of AED 2,548 million in FY2025 and AED 1,277 million in the "
    "half, up 4.0%; capital expenditure of AED 1,051 million accrual in FY2025 broken down by "
    "category, and AED 339 million in the half; 2.78 million loyalty members",
    "FY2025 and half-year 2026 management discussion reports and results presentations", IR,
    "2026-08-05", url=IR_DOWNLOADS, fiscal_period="Q2-2026",
    model_impact="Supplies the unit denominators for the cost and capital legs — cash operating "
                 "cost per site and per transaction, capital expenditure by category against "
                 "site additions, non-fuel gross profit per transaction — so the cost stack and "
                 "the capital-expenditure line are built per unit and escalated per driver "
                 "class, not set as percentages of revenue.")

k_inv = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "THE FIRST HALF OF 2026 CARRIED AED 762 MILLION OF INVENTORY GAINS (AED 528 million fuel "
    "retail, AED 233 million commercial) AGAINST AED 147 MILLION A YEAR EARLIER, WHILE FUEL "
    "VOLUMES GREW ONLY 1.6%. Headline EBITDA rose 38.8% to AED 2,886 million while UNDERLYING "
    "EBITDA, which the company defines as EBITDA excluding inventory movements and one-off "
    "items, rose about 13.9% to AED 2,215 million. The second quarter alone carried AED 738 "
    "million of gains against AED 37 million. FY2025 gains were AED 335 million and FY2024 AED "
    "254 million. These figures are MANAGEMENT-COMMENTARY MEASURES ONLY — no inventory "
    "gain, no EBITDA and no underlying EBITDA is a line in any audited or reviewed statement, "
    "and no reconciliation from the accounts to them is published",
    "Half-year 2026 and FY2025 management discussion reports and results presentations", IR,
    "2026-08-05", url=IR_DOWNLOADS, fiscal_period="Q2-2026",
    model_impact="THE STUDY'S CENTRAL JUDGEMENT, AND IT RESETS THE FORECAST BASE. The forecast "
                 "is struck off UNDERLYING EBITDA, not headline: capitalising a half-year that "
                 "is four-fifths price and inventory timing would embed a crude spike in "
                 "perpetuity. Because it is the study's single most consequential contested "
                 "judgement it is computed BOTH WAYS — normalised base and headline base — and "
                 "published side by side in the summary table, the body, the workbook and an "
                 "expert's range, never averaged into one number.")

k_shell = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    FindingClass.B,
    "THE PROPOSED ACQUISITION OF SHELL DOWNSTREAM SOUTH AFRICA: a definitive agreement signed in "
    "July 2026 for 100% of the share capital at an enterprise value of approximately USD 1 "
    "billion, covering about 580 stations — roughly +55% network to about 1,600 sites, +70% "
    "convenience stores to about 900 and +20% fuel volumes to about 19 billion litres. "
    "Management states +6% earnings per share and +13% EBITDA in the first full year after "
    "completion, a free-cash-flow yield near 15% and USD 30-40 million of run-rate synergies "
    "within five years. A 28% stake is expected to be sold down post-closing to a local "
    "empowerment partner and an employee share ownership plan. COMPLETION IS EXPECTED IN 2027, "
    "subject to regulatory approvals, and it is disclosed as an event after the reporting date",
    "Note 25, reviewed interim consolidated financial statements to 30 June 2026; half-year 2026 "
    "management discussion report and results presentation", CO, "2026-08-05", url=IR_DOWNLOADS,
    fiscal_period="Q2-2026",
    model_impact="IT HAS NOT CLOSED, SO THE BASE CASE EXCLUDES IT ENTIRELY — no South African "
                 "revenue, volume, station, debt or currency exposure enters the standalone "
                 "valuation, and the balance sheet it is struck from is the one that exists. It "
                 "is carried instead as a fully separate PRO-FORMA valuation published beside "
                 "the standalone one, never averaged with it and never blended into a single "
                 "number, because the transaction is binary and dated: it either completes in "
                 "2027 or it does not.")

k_stakes = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    FindingClass.D,
    "The other ownership facts, each a NAMED transaction rather than an estimate: a 50% interest "
    "in TotalEnergies Marketing Egypt acquired from TotalEnergies Marketing Afrique in February "
    "2023 for approximately USD 186 million, bringing 240 stations, and consolidated — the "
    "audited related-party note records TotalEnergies revenue of AED 711,619 thousand, purchases "
    "of AED 156,836 thousand, management fees of AED 54,084 thousand and dividends paid of AED "
    "28,904 thousand in FY2025, and the Egyptian subsidiary's own borrowings sit on the "
    "consolidated balance sheet. The parent holds about 77% with roughly 23% free float and a "
    "stated commitment to remain at or above 70%, and amounts due to the parent were AED "
    "3,598,366 thousand at 31 December 2025",
    "Related-party note, audited consolidated financial statements FY2025", CO, "2026-02-01",
    url=IR_DOWNLOADS, is_fs_data=True, fiscal_period="FY2025",
    model_impact="No ownership driver in this study is estimated. Egypt is consolidated, not "
                 "equity-accounted, so its litres, stations and borrowings are inside the "
                 "operating build and its currency exposure is priced on the leg rather than "
                 "netted at the bottom; and the concentrated parent holding is what makes the "
                 "supply agreement a related-party arrangement whose renewal terms are carried "
                 "in the risk register.")

k_div = R.add(Ring.COMPANY, "management & capital actions", FindingClass.S,
    "The dividend policy runs 2024 to 2030 at AED 2.57 billion a year — 20.57 fils a share, "
    "about USD 700 million — OR 75% of net profit, whichever is higher, and moved to quarterly "
    "payment from 2026. The first and second quarters of 2026 were each declared at 5.14 fils, "
    "the second payable 1 September 2026: THE FLOOR, NOT 75% OF THE SPIKED HALF-YEAR PROFIT. "
    "Leverage was about 0.7 times net debt to EBITDA at the half year, unchanged from the 2025 "
    "close, and the parent revolving facilities remain wholly undrawn",
    "Dividends note, audited consolidated financial statements FY2025; half-year 2026 management "
    "discussion report and dividend declarations", CO, "2026-08-05", url=IR_DOWNLOADS,
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="Sets the payout in the equity roll-forward and the carry offset in the "
                 "probability map. It is also corroborating evidence for the normalised base: "
                 "the board itself is paying the floor rather than 75% of a spiked profit, which "
                 "is the company's own signal that it does not treat the first half of 2026 as "
                 "the earnings base either.")

k_guid = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.D,
    "Guidance for 2026, reaffirmed at the half year: capital expenditure of USD 250-300 million "
    "(AED 0.9-1.1 billion), weighted to the second half; 60 to 70 new stations across the three "
    "markets; 50 to 60 new charging points; five new hub sites. Medium-term targets: 1,150 "
    "stations by 2028 excluding South Africa, double the non-fuel transactions between 2023 and "
    "2030, 500 to 750 charging points by 2028, and up to AED 184 million of like-for-like "
    "operating-cost reduction across 2024-2028, of which AED 66 million, AED 24 million and AED "
    "9 million were delivered in FY2024, FY2025 and the first half of 2026",
    "Half-year 2026 management discussion report and results presentation; FY2025 management "
    "discussion report and 2025 integrated report", IR, "2026-08-05", url=IR_DOWNLOADS,
    fiscal_period="Q2-2026",
    model_impact="Sets the capital-expenditure line of the free-cash-flow waterfall directly and "
                 "the site-addition schedule that drives the volume leg. The 1,150-by-2028 "
                 "target predates the South African agreement and is already close to met "
                 "organically at 1,045, so it is used as the ORGANIC path only and its vintage "
                 "is stated. The delivered operating-cost savings are run through the cost stack "
                 "at their realised rate, not at the headline target.")

k_beta = R.add(Ring.COMPANY, "market data & own-stock beta regression", FindingClass.D,
    "An own-stock beta regression on five years of weekly returns from 20 August 2021 to 7 "
    "August 2026 against a local Abu Dhabi exchange composite, run on the study's own cleaned "
    "price history. Against the composite excluding the subject itself: beta 0.509, standard "
    "error 0.065, R-squared 19.4%, 257 observations, 90% interval 0.402 to 0.615 — comfortably "
    "through the usability gate of at least 24 observations, R-squared at or above 5% and a "
    "standard error below the absolute beta. Including the subject the beta is 0.633 with "
    "R-squared 27.8%; an all-UAE composite gives 0.510 excluding the subject",
    "Own-stock weekly return regression against the local exchange composite, computed 9 August "
    "2026 from the study's own daily price library", PMD, "2026-08-07",
    model_impact="Beta comes from the stock's OWN price history against its OWN local index, "
                 "which is the first tier of the preference order — no peer beta and no default "
                 "of 1.0 is used, because the own-stock regression is available and passes the "
                 "gate. The excluding-subject composite is chosen so the name's own index weight "
                 "cannot pull its beta mechanically toward one, and the difference between the "
                 "two constructions is published rather than buried.")

# ---- negative results, recorded rather than hidden ----------------------------
k_neg_tranche = R.add_negative(Ring.COMPANY, "official financial statements",
    "The outstanding dirham-versus-dollar split of the term loan at any balance-sheet date, "
    "sought in the borrowings note of the FY2023, FY2024 and FY2025 audited filings and both "
    "2026 reviewed interims. NOT DISCLOSED at any reporting date: the notes give the ORIGINAL "
    "2017 drawdown split (USD 375,000 thousand and AED 4,128,750 thousand) and the per-currency "
    "margin basis, but never the current outstanding balance by tranche. Nor is an explicit "
    "maturity date given — only 'refinanced on 26 October 2022 for another 5-year term'. The "
    "local-currency versus foreign-currency debt split is therefore built on the original "
    "drawdown proportions, and the gap is flagged in the study rather than papered over",
    SWEEP_DATE)

k_neg_hist = R.add_negative(Ring.COMPANY, "one-off base-resetting transactions",
    "Inventory gains or losses, EBITDA and underlying EBITDA for FY2023 and FY2022, sought "
    "across the audited filings, the FY2025 management discussion report and the 2025 integrated "
    "report. NOT DISCLOSED anywhere: these are management measures published only from FY2024 "
    "onward in the documents available, and no reconciliation from the audited accounts to them "
    "exists in any of them. A through-cycle inventory-movement average can therefore be computed "
    "over FY2024, FY2025 and the first half of 2026 ONLY — three observations, one of which is "
    "the shock itself",
    SWEEP_DATE)

k_neg_kpi = R.add_negative(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    "FY2023 and FY2022 operating statistics — fuel volumes by segment, station and store counts, "
    "transaction counts, charging points — sought in every supplied filing and report. NOT "
    "AVAILABLE: the FY2023 and FY2024 management discussion reports and results presentations "
    "are not among the obtained documents, the FY2025 report carries only 2025 and 2024 columns, "
    "and the 2025 integrated report's index carries only environmental and workforce series for "
    "2022-2025. The volume-times-price build therefore runs on TWO full disclosed years plus six "
    "quarters, and the earlier revenue history is carried at the audited line-of-business level "
    "only, with that limitation stated",
    SWEEP_DATE)

k_neg_guid = R.add_negative(Ring.COMPANY, "strategic plans & guidance",
    "Quantitative FY2026 EBITDA or fuel-volume guidance, sought in the half-year and FY2025 "
    "management discussion reports, both 2026 results presentations and the integrated report. "
    "NONE IS GIVEN as a number in any of them — guidance covers capital expenditure, station "
    "additions and charging points only. There is consequently no company forecast to anchor the "
    "earnings path to, which is why every forecast driver here is built from disclosed history "
    "and the regulated price mechanism, and why the crux is posed as an observable-units question "
    "rather than a check against guidance",
    SWEEP_DATE)

k_neg_shell = R.add_negative(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    "The funding structure of the South African acquisition — debt, equity, mix, and any "
    "disclosed purchase-price allocation — sought in the subsequent-events note, the half-year "
    "management discussion report and the results presentation. NOT DISCLOSED in any of them. "
    "The pro-forma leg is therefore built on a stated funding assumption, disclosed as an "
    "assumption and sensitised across an all-debt to all-equity range, rather than presented as "
    "a sourced capital structure",
    SWEEP_DATE)

# ---- driver gate ---------------------------------------------------------------
R.add_driver("Retail (B2C) fuel volume, litres", DriverMode.BOTTOM_UP,
             "Retail litres are disclosed by the results presentations and management discussion "
             "reports, split GCC versus Egypt and by product, for FY2024, FY2025 and every "
             "quarter since. Grown as a volume in its own right on disclosed site additions and "
             "throughput per station, cross-checked against transaction counts, with the vehicle "
             "parc used only as a ceiling.",
             [k_vols, k_kpi, k_rev, i_parc])

R.add_driver("Commercial (B2B) fuel volume — corporate and aviation, litres", DriverMode.BOTTOM_UP,
             "Commercial litres are disclosed and split into corporate and aviation at the half "
             "year, with a GCC/Egypt geography split. The two are forecast separately: aviation "
             "on flight-activity-driven growth off its own disclosed base, corporate on the "
             "disclosed base with management's stated withdrawal from declining-price windows "
             "reflected explicitly.",
             [k_vols, k_rev])

R.add_driver("Retail margin per litre", DriverMode.BOTTOM_UP,
             "Audited retail segment gross profit divided by the separately disclosed retail "
             "litres, computed for each disclosed period, then held on the regulated unit margin "
             "with inventory timing stripped out. The parent supply agreement's disclosed "
             "protection against per-litre gross profit falling below specified levels bounds "
             "the downside case.",
             [k_rev, k_vols, i_price])

R.add_driver("Commercial margin per litre", DriverMode.BOTTOM_UP,
             "Audited commercial segment gross profit divided by disclosed commercial litres, "
             "computed separately from retail because the commercial leg carries no regulated "
             "price and swings hardest on inventory timing — its FY2024 inventory position was a "
             "loss where retail's was a gain.",
             [k_rev, k_vols, k_inv])

R.add_driver("Non-fuel retail revenue and gross profit", DriverMode.BOTTOM_UP,
             "Built as disclosed non-fuel transactions times revenue per transaction times the "
             "disclosed store gross margin, against the audited non-fuel revenue line, with the "
             "store, property and car-care counts as the capacity driver. The peer benchmark sets "
             "the ceiling it grows toward, never the level it is set at.",
             [k_rev, k_kpi, g_nonfuel])

R.add_driver("Realised price per litre", DriverMode.BOTTOM_UP,
             "Audited segment fuel revenue divided by disclosed litres gives the realised price "
             "for each leg; it is then projected on the regulated monthly pass-through — the "
             "crude and crack path through the committee formula — converging from the August "
             "2026 level back toward the 2025 band, NOT held at the first-half-2026 realisation.",
             [k_rev, k_vols, i_price, g_crude])

R.add_driver("Cash operating costs", DriverMode.BOTTOM_UP,
             "Built per unit from the disclosed cash operating cost base — cost per site and per "
             "transaction — with ONE ESCALATOR PER DRIVER CLASS: domestic wages and local "
             "services on the UAE consumer-price path, energy and transport on their own "
             "commodity paths, and the disclosed like-for-like savings programme applied at its "
             "realised delivery rate. Depreciation is excluded here and enters once from the "
             "asset roll-forward.",
             [k_kpi, k_fs25, c_macro])

R.add_driver("Capital expenditure", DriverMode.BOTTOM_UP,
             "Built from the disclosed category breakdown — service-station projects, industrial "
             "projects, machinery, fleet and technology — against the guided station and charging-"
             "point additions, and reconciled to the audited cash-flow investing line. The "
             "capital-light dealer-owned Saudi sites are costed separately from owned UAE sites.",
             [k_guid, k_kpi, k_fs25])

R.add_driver("Inventory movements", DriverMode.TOP_DOWN,
             "TOP-DOWN BY NECESSITY, not by convenience. Inventory gains are a management measure "
             "with no financial-statement line and no published reconciliation, and no FY2023 or "
             "FY2022 figure exists at all, so a through-cycle rate can be estimated over three "
             "observations only. They are therefore normalised to zero in the forecast base and "
             "the first-half-2026 gain is shown separately in both framings, rather than being "
             "modelled as a recurring line.",
             [k_neg_hist, k_inv])

R.add_driver("Risk-free rate (local currency)", DriverMode.BOTTOM_UP,
             "The observed dirham federal Treasury Bond yield at the July 2026 auction, "
             "normalised by the sovereign's own adjusted default spread so that country risk "
             "enters once through the country premium inside the equity risk premium.",
             [c_rf, c_neg_tenor])

R.add_driver("Ten-year local-currency rate point", DriverMode.TOP_DOWN,
             "Constructed, and disclosed as a construction. No ten-year dirham federal bond "
             "exists, so the ten-year point is extrapolated from the observed four-and-a-half-"
             "year federal yield and the Abu Dhabi dollar spread over Treasuries, and it is never "
             "presented as an observed yield.",
             [c_neg_tenor, c_rf])

R.add_driver("Equity risk premium", DriverMode.BOTTOM_UP,
             "The United Arab Emirates row read from the ORIGINAL country risk file, at its "
             "stated January 2026 vintage, with the mature-market premium implied from the same "
             "file's United States row. Both premium bases are published and the vintage choice "
             "is carried as a stated sensitivity rather than a silent selection.",
             [c_damodaran, c_neg_erp])

R.add_driver("Beta", DriverMode.BOTTOM_UP,
             "The stock's own five-year weekly return regression against its own local exchange "
             "composite, passing the usability gate on observations, explanatory power and "
             "standard error. First tier of the preference order — no peer beta, no default of "
             "1.0, and no short-window daily stopgap.",
             [k_beta])

R.add_driver("Cost of debt (marginal, local currency)", DriverMode.BOTTOM_UP,
             "The sovereign dirham yield plus THE COMPANY'S OWN DISCLOSED CREDIT MARGIN of 0.60% "
             "over the interbank rate from the borrowings note, which sits above the sovereign as "
             "the method requires. The dollar tranche is carried at its local-equivalent cost and "
             "the Egyptian facilities at their own corridor-linked local rate, never at a raw "
             "foreign coupon in a local-nominal capital cost. This is what let the blocked "
             "interbank-rate page fail without blocking the build.",
             [k_debt, g_rates])

R.add_driver("Effective tax rate", DriverMode.BOTTOM_UP,
             "Built off the company's OWN audited reconciliation — the 9% domestic rate plus the "
             "disclosed overseas-rate difference, giving the low-double-digit effective rate the "
             "filing reports — with the 15% minimum top-up priced as a dated sensitivity from the "
             "safe harbour's stated 2027 expiry.",
             [k_tax, c_tax])

R.add_driver("Saudi dealer-owned network leg", DriverMode.BOTTOM_UP,
             "Contracted and operational site counts are disclosed separately from owned sites, "
             "so the Saudi leg is built as sites times throughput times a dealer margin on its "
             "own capital intensity, faded as the licensing consolidation window closes rather "
             "than extrapolated to the terminal year.",
             [i_saudi, k_kpi, k_guid])

R.add_driver("Egypt leg", DriverMode.BOTTOM_UP,
             "Egypt is consolidated, and its litres, stations, stores and local-currency "
             "borrowings are all disclosed separately, so the leg is built on its own volumes and "
             "its own local funding cost rather than being netted into the group at the bottom.",
             [k_vols, k_kpi, k_stakes])

R.add_driver("UAE electric-vehicle substitution drag", DriverMode.TOP_DOWN,
             "No 2025 or 2026 UAE share of new electric-vehicle sales could be sourced, so the "
             "drag cannot be built from a current adoption series. It is instead applied as a "
             "policy-target-implied PARC-share glide toward the stated 2030 target, small inside "
             "the explicit forecast and carried mainly in the terminal growth rate.",
             [i_neg_entrants, i_ev, g_ev])

R.add_driver("South Africa pro-forma leg", DriverMode.TOP_DOWN,
             "EXCLUDED FROM THE BASE CASE ENTIRELY — the transaction has not closed. The separate "
             "pro-forma valuation is built top-down on management's own stated accretion and "
             "network figures because no target financial statements and no funding structure "
             "have been disclosed, and it is published beside the standalone valuation, never "
             "averaged into it.",
             [k_neg_shell, k_shell])

R.add_driver("Dividend and payout", DriverMode.BOTTOM_UP,
             "The disclosed policy floor and the 75%-of-net-profit test are both applied period "
             "by period against the modelled profit, taking whichever binds — which is the floor "
             "in the current cycle, exactly as the board has declared it.",
             [k_div])

errors, warnings = R.validate()
print(f"Sweep register: {R.counts()}")
print(R.qc_line())
for w in warnings: print("  warning:", w)
R.to_json(os.path.join(HERE, 'sweep_register.json'))
assert not errors, f'{len(errors)} sweep errors — build must not proceed'
