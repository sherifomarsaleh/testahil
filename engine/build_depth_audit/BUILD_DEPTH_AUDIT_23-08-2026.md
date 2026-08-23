# Build-depth audit — which fundamental valuations were built from the bottom up

**Scope.** Every stock carrying a published fundamental fair value in `assets/data.js`
(**90** names). The four metals studies (XAUUSD, XAUUSD 12M, XAGUSD, XPTUSD) are
excluded — they have no corporate revenue build to classify. Each row was read out of the
latest delivered edition of that stock's own study, and for the 21
studies that carry a code-built `engine/<name>_study/` directory, cross-read against
`compute.py` / `bottom_up.json`.

**Standard applied.** SIGCM clause 2 and DRIVER DISCIPLINE in the Standing Research Protocol:
*revenue as VOLUME × PRICE and cost as COST-PER-UNIT, product by product or service by service
wherever segments are disclosed; where unit/segment data is not disclosed, drop to the finest
sourced level and FLAG the gap.* A study counts as **built bottom-up** only where the forecast
runs on a physical unit and a rate per unit, with margins falling out as outputs.

## Headline

| | Count | Share |
|---|---|---|
| **Built from the bottom up** | **27** | 30% |
| **Not built from the bottom up** | **63** | 70% |
| Total covered stocks | 90 | 100% |

### The seven build tiers

| Tier | Meaning | Count | Counts as bottom-up? |
|---|---|---|---|
| A | Bottom-up — disclosed units — revenue = a disclosed physical unit × a price/rate, cost per unit, margins as outputs | 15 | Yes |
| A− | Bottom-up — major legs — the unit build covers the major legs; the remainder sits at segment level because nothing finer is disclosed, and the study says so | 5 | Yes |
| B | Bottom-up — derived units — genuine unit economics, but the units are the preparer's estimate, an index, or back-solved from disclosed totals | 7 | Yes, with the caveat |
| C | Segment-level — each disclosed segment on its own driver, no unit economics; gap flagged | 6 | No |
| D | Top-down — a group or segment revenue-growth path plus a margin assumption or glide | 25 | No |
| E | Asset / NAV / stake marks — value comes from marking assets, stakes or segment earnings at multiples; no revenue build at all | 20 | No |
| F | Bank driver build — balances × margin (NIM / cost-of-risk / cost-to-income bridge) | 12 | No |

---

## A. Built from the bottom up — 27 stocks

| Ticker | Company | Exchange | Study edition | Build tier | How the forecast is actually built |
|---|---|---|---|---|---|
| **ADNOCDIST** | Abu Dhabi National Oil Company for Distribution (ADNOC Distribution) | ADX | 09-08-2026 | Bottom-up — disclosed units | Litres x margin per litre for retail fuel and commercial fuel; non-fuel retail on revenue x gross margin. 'No segment is grown on a blended rate.' Gross margin is shown last, as an OUTPUT. |
| **ADNOCDRILL** | ADNOC Drilling Company P.J.S.C. | ADX | 09-08-2026 | Bottom-up — disclosed units | Rigs in service x revenue per rig-year, by class; rates are arithmetic off disclosed segment revenue and disclosed rig counts. Oilfield services carries TWO disclosed rig populations after a one-driver build implied a negative rate. Margins fall out of a cost stack. |
| **ADNOCLS** | ADNOC Logistics & Services plc | ADX | 09-08-2026 | Bottom-up — disclosed units | Seven disclosed units, each on its own physical driver; tankers literally vessel by vessel - 12 chartered vessels at their own disclosed rates for the days their contracts run, the other 40 at a market rate solved out of the company's published class averages; gas carriers on contracted vessel-years x day rate; running cost USD 9,164 a vessel-day. |
| **AIRARABIA** | Air Arabia PJSC | DFM | 09-08-2026 | Bottom-up — disclosed units | Passengers x per-passenger rates (fare+baggage, ancillary, fuel = intensity x jet price, staff). Seats/ASK are not disclosed, so passengers is stated as the finest disclosed level. Margins are OUTPUTS. |
| **AMOC** | Alexandria Mineral Oils | EGX | 08-08-2026 | Bottom-up — disclosed units | Eight disclosed product lines, tonnes x realisation from note 14-A, rolled on a volume path per line. Cost built PER LINE in two legs - conversion allocated on processing-intensity weights, feedstock on net realisable value - giving a spread per tonne for every line. |
| **AMR** | Americana Restaurants International PLC | ADX | 09-08-2026 | Bottom-up — disclosed units | Restaurants x revenue per restaurant across seven market units; estate grows on the company's own net-new-store programme, revenue per restaurant on disclosed like-for-like, less a currency drag in the unpegged markets. Build reproduces reported revenue in all three audited years. |
| **ARCC** | Arabian Cement | EGX | 08-08-2026 | Bottom-up — disclosed units | Tonnes are DISCLOSED (FY2025 investor presentation) and reproduced to within 0.02%. Drivers are physical - kiln utilisation, clinker factor, two export shares - and all three realised prices are OUTPUTS. Three earlier editions that back-solved tonnes from an assumed price were withdrawn as circular. |
| **BOROUGE** | Borouge plc | ADX | 17-08-2026 | Bottom-up — disclosed units | Nameplate capacity x disclosed utilisation for volume; published benchmark + disclosed premium x a measured realisation residual for price; cost in dollars per tonne split by what physically drives it, one escalator per driver class. Capex is flagged as the one materially top-down driver. |
| **EGCH** | Egyptian Chemical Industries (KIMA) | EGX | 08-08-2026 | Bottom-up — disclosed units | One reported segment, so the build goes BELOW it to product and channel: tonnes x price channel by channel, cost as physical consumption x a unit price. 'Nothing in the model sets a margin.' |
| **EMPOWER** | Emirates Central Cooling Systems Corporation PJSC | DFM | 09-08-2026 | Bottom-up — disclosed units | Two-leg unit build: connected refrigeration tons x the capacity rate, plus consumption per connected ton x the connected base. Volume driver is disclosed connected capacity plus the 311k RT contracted backlog. Margins as OUTPUTS. |
| **FERTIGLB** | Fertiglobe plc | ADX | 09-08-2026 | Bottom-up — disclosed units | Installed capacity x utilisation by plant and product; realised price = published benchmark x a measured realisation ratio; cash cost per tonne calibrated against disclosed segment economics and cross-checked on gas intensity. The third-party trading leg is the one leg not built from unit economics and the study flags it. |
| **LULU** | Lulu Retail Holdings | ADX | 13-07-2026 | Bottom-up — disclosed units | Six country models driven by stores, retail space (m sqm) and sales density (US$ per sqm); operating cost tracks space x mature-store cost inflation, so the EBITDA margin is a derived break-even, not an input. |
| **PHAR** | Egyptian International Pharmaceutical Industries (EIPICO) | EGX | 09-08-2026 | Bottom-up — disclosed units | Three product lines, each with its own volume and price: 351.8m packs of own preparations split into export (60m at USD 1.00/pack) and domestic (291.8m at EGP 21.22/pack), plus contract manufacturing at EGP 9.00 a pack. The two disclosure splits are reconciled to the thousand pound. |
| **SALIK** | Salik Company | DFM | 11-07-2026 | Bottom-up — disclosed units | Peak trips x AED 6 plus off-peak trips x AED 4, from the company's own Q1-2026 disclosure; the rebuild reproduces reported toll revenue to five hundredths of one per cent - the study publishes that as an 'audit receipt' before setting any forward driver. |
| **SCEM** | Sinai Cement Company S.A.E. | EGX | 06-08-2026 | Bottom-up — disclosed units | Clinker and cement tonnes on kiln/mill utilisation and the clinker factor, split domestic vs export, priced per tonne; variable cost stacked per tonne across fuel, power, raw materials, packaging and distribution (bottom_up.json in the study directory). |
| **CLHO** | Cleopatra Hospitals Group | EGX | 13-07-2026 | Bottom-up — major legs | Five disclosed KPI lines, 59% of FY25 revenue, modelled as volume x average revenue per unit and faded from their own FY24-25 growth. The remaining ~41% (pharmacy, lab, IVF) has no disclosed volume/price split and grows top-down off bed capacity - the study cites the data-discipline gate for refusing to manufacture one. |
| **DSCW** | Dice For Ready-Made Garments | EGX | 19-07-2026 | Bottom-up — major legs | Export book (~65% of revenue) on pieces x USD price - 21.6m pieces at US$4.41 in FY25, tagged 'bottom-up (disclosed)' in the sourcing gate. Retail and the third-party dyeing/printing books run on growth rates. |
| **DU** | Emirates Integrated Telecommunications Company PJSC | DFM | 17-08-2026 | Bottom-up — major legs | Mobile and Fixed built as volume x price - quarterly customer base x blended ARPU, reproducing the audited FY2025 mobile segment to within 0.1% - with a genuine per-subscriber direct-cost stack (interconnect, capacity, commission). Wholesale and ICT grow on their own revenue because no volume unit is disclosed; stated. |
| **GBCO** | GB Corp (Ghabbour) | EGX | 08-07-2026 | Bottom-up — major legs | The Auto leg - the DCF engine of the SOTP - is built on disclosed units x ASP per line of business ('volumes and revenue are published per LoB, so ASP is arithmetic'). GB Capital is marked on adjusted-ROAE book and the associates on a transaction mark, as their class requires. |
| **SAVOLA** | Savola Group Company | TADAWUL | 19-08-2026 | Bottom-up — major legs | Oil, sugar and pasta are true unit builds on DISCLOSED volumes with gross profit per tonne; Panda is stores x sales per average store. Nuts & spices and the two small legs run on category revenue paths - the study says so in the driver table. Group EBITDA margin is an OUTPUT. |
| **ELEC** | Electro Cable Egypt | EGX | 05-08-2026 | Bottom-up — derived units | Revenue = tonnes shipped x price per tonne (LME copper x EGP/USD x a 1.387x fabrication uplift), EBITDA = tonnes x conversion EBITDA per tonne. But 'the company discloses no volumes', so the tonnage is back-solved and validated against the stated ~25,000 t/yr capacity; utilisation is called indicative. |
| **EMFD** | Emaar Misr for Development | EGX | 17-06-2026 | Bottom-up — derived units | Project-by-project bottom-up build from unit mix priced per square metre with construction and land per square metre; hotels and the retail/commercial base as separate EBITDA-multiple segments. Unit mixes and prices are the author's estimates calibrated to disclosed FY2025 totals. |
| **OCDI** | Sixth of October Development & Investment | EGX | 24-06-2026 | Bottom-up — derived units | Every development project from a derived unit mix (units x price/m2) and a derived cost stack (m2 x construction-cost/m2), unsold remainder only, execution-weighted. The study states plainly: 'No project-level data is disclosed by the company ... illustrative, not authoritative.' |
| **ORHD** | Orascom Development Egypt | EGX | 25-06-2026 | Bottom-up — derived units | Same construction as SODIC - each destination from a derived unit mix x price/m2 and a derived construction cost per m2, unsold remainder only, execution-weighted, calibrated to disclosed FY2025 totals and flagged as derived. |
| **PHDC** | Palm Hills Developments | EGX | 11-06-2026 | Bottom-up — derived units | Clean-sheet project-by-project build: every project from its unit mix (apartments, town/twin houses, villas, chalets) priced per square metre, construction and land costed per square metre, only the unsold remainder valued. Project-level inputs are the preparer's estimates. |
| **RIYADHCABLE** | Riyadh Cables Group Company | TADAWUL | 18-08-2026 | Bottom-up — derived units | Cables & wires (98% of revenue) is modelled as a metal converter on a cable-tonnage INDEX (FY2025 = 100): metal content per unit on its own copper/aluminium path, conversion cost per unit on domestic inflation, plus a conversion spread. 'The company does not disclose tonnage, so this is an index, not an absolute volume.' The two small legs carry disclosed segment margins. |
| **TMGH** | Talaat Moustafa Group Holding | EGX | 17-06-2026 | Bottom-up — derived units | Development leg built project by project from units x price/m2 and m2 x construction-cost/m2, self-liquidating with no perpetuity; hotels and recurring income are separate EBITDA-multiple segments. Project inputs are estimates calibrated to disclosed totals. |

---

## B. Not built from the bottom up — 63 stocks

| Ticker | Company | Exchange | Study edition | Build tier | How the forecast is actually built |
|---|---|---|---|---|---|
| **ALDAR** | Aldar Properties PJSC | ADX | 08-07-2026 | Segment-level | Split-leg SOTP: the development leg is a finite DCF off the disclosed AED 71.7bn backlog and a fading launch programme (backlog conversion, not units x price); Aldar Investment is carried at its stated AED 52bn recurring GAV on an implied cap rate. |
| **DEWA** | DEWA (Dubai Electricity and Water Authority) | DFM | 11-07-2026 | Segment-level | Driver table carries revenue as a growth rate (7.5% fading to 4.5%) that the study labels 'bottom-up: customer growth + demand/peak trends + Empower consolidation' - a driver-informed growth path, not a tariff x units build. D&A and finance cost are tagged top-down. |
| **EMAARDEV** | Emaar Development PJSC | DFM | 08-07-2026 | Segment-level | Split-NAV off the balance sheet: net cash plus the PV of profit still to be recognised on the secured sales backlog (125,200 x a 35% sustainable margin) plus a heavily haircut land-bank value, less central overhead. Backlog-and-margin, not a unit mix. |
| **MODON** | Modon Holding PSC | ADX | 10-08-2026 | Segment-level | Each leg on its own driver - development on disclosed backlog conversion plus new launches, the rest anchored on H1 actuals - but the study states it outright: 'Per-project volumes and prices are not disclosed; the build stops at segment level with unit-level anchors ... That gap is flagged, not papered over.' |
| **PRDC** | Pioneers Properties for Urban Development | EGX | 06-07-2026 | Segment-level | Split-leg SOTP: development leg an RNAV off contracted backlog and the launched/unlaunched pipeline with no terminal value; contracting on normalised earnings x a contractor multiple; rental on NOI and a cap rate. |
| **SWDY** | Elsewedy Electric | EGX | 05-08-2026 | Segment-level | Three disclosed reportable segments, each grown and margined on its own driver, reconciling exactly to audited revenue. But: 'None of the three audited filings ... discloses a tonnage, unit-volume or order-book figure for any segment, so the forecast is built as a taper on each segment's own recent revenue growth and margin path rather than a reconstructed unit model.' |
| **AAPL** | Apple Inc. | NASDAQ | 06-07-2026 | Top-down | Group revenue taken from $442bn to $540bn 'as Services compounds low-double-digits and hardware grows low-single-digits', with the operating margin lifted 32.5% to 34.5%. The segment SOTP marks Services and Products on EV/EBIT multiples. |
| **ABUK** | Abu Kir Fertilizers | EGX | 01-07-2026 | Top-down | Operating leg valued on a five-year FCFF with a NORMALIZING EBIT MARGIN (38% to 40%) as the input, then combined with investments and net cash in a three-part SOTP. Margin as an input is the opposite of the cost-per-unit rule. |
| **ADNOCGAS** | ADNOC Gas | ADX | 04-07-2026 | Top-down | 'ADNOC Gas does not disclose per-segment volume x price in the granularity a full bottom-up build would require, so - per the data-discipline gate - we forecast top-down on disclosed margins and split the revenue illustratively 60/40.' |
| **AGTHIA** | Agthia Group PJSC | ADX | 06-07-2026 | Top-down | 'Agthia discloses segment revenue and EBITDA but not volume/price splits by pack or SKU, so all forecasts here are top-down normalized margins on the disclosed segment averages; no packs-x-price build is manufactured.' |
| **ARAMCO** | Saudi Aramco | TADAWUL | 01-07-2026 | Top-down | Revenue growth tracks an oil-price deck grinding from $70 to a $72-74 mid-cycle; EBIT margins held near 44-45%; capex ~$52-54bn. The reserves-NAV lens marks 247.2bn boe at ~$7/boe - an asset mark, not a production x price build. |
| **BURJEEL** | Burjeel Holdings PLC | ADX | 11-07-2026 | Top-down | Revenue +11% fading to +8% against the guidance record; the modelled EBITDA-margin glide from 19.3% to 22.0% is named as the study's central judgment. No bed/case/occupancy unit build. |
| **EAND** | e& (Emirates Telecommunications Group) | ADX | 10-07-2026 | Top-down | Revenue steps +8.5% in FY26E on guidance and settles to 3.0-3.5%; EBITDA margin glides 42.4% to 43.6%. The sourcing gate is explicit that drivers are 'top-down, and flagged as such' wherever no disclosed unit figure was found. |
| **EFID** | Edita Food Industries | EGX | 03-07-2026 | Top-down | Revenue growth starts at 30% for FY2026 and fades to 13% by FY2030; EBITDA margin held at 19.2-19.5%. The segment table applies per-segment growth and margin assumptions. |
| **EFIH** | e-finance for Digital & Financial Investments | EGX | 03-07-2026 | Top-down | Revenue growth fades from ~32% toward the low teens with the EBITDA margin held near 50%. The segment SOTP marks each part on FY2025 segment EBITDA x a multiple. |
| **EGAL** | Egypt Aluminum | EGX | 03-07-2026 | Top-down | The primary DCF is built from revenue growth, gross margin, capex and working-capital drivers - anchored on the company's own EGP 11.1bn budget direction then ~10% nominal growth. LME x FX x volume appears only in the normalised-earnings expert lens. |
| **ELM** | Elm Company | TADAWUL | 10-07-2026 | Top-down | DCF with a segment scorecard whose BPO and Professional Services splits are 'estimated from disclosed growth rates and the Digital Business figure' - segment revenue paths, no unit economics. |
| **EXTRA** | United Electronics Company (eXtra) | TADAWUL | 10-07-2026 | Top-down | Split-legs SOTP - retail on an operating-co DCF, Tasheel on its equity book. 'Segment split partly estimated where not separately disclosed (flagged in the driver ledger).' No stores x basket or unit build. |
| **FWRY** | Fawry | EGX | 01-07-2026 | Top-down | FY26E built on 30% revenue growth and a 56% EBITDA margin, fading 20% to 12% over five years. The segment table shows where growth lives; there is no transactions x take-rate build. |
| **INFY** | Infosys Limited | NSE | 06-07-2026 | Top-down | Revenue compounds 5-7% through the window with the operating margin held in the guided 21-22% band. The vertical/geography section is a scorecard, not a driver build. |
| **ISPH** | Ibnsina Pharma | EGX | 07-07-2026 | Top-down | Revenue growth fades from the re-pricing-driven ~20% toward ~11%; EBITDA margin expands 5.1% to 5.5% on scale. Channels are a scorecard, not a driver build. |
| **JUFO** | Juhayna Food Industries | EGX | 01-07-2026 | Top-down | FCFF on a group growth-and-margin path; the segment sum is a cross-check that marks each segment's FY25 revenue at a normalized operating margin and an EV/EBIT multiple. No litres or tonnes. |
| **LCSW** | Lecico Egypt (S.A.E.) | EGX | 06-07-2026 | Top-down | Revenue grows 10-13% a year (nominal inflation plus modest export volume) with the EBITDA margin recovering from 12.6% to ~14.5%. Segment detail is used descriptively - 'we use it directly rather than manufacture splits'. |
| **LGES** | LG Energy Solution, Ltd. | KRX | 28-06-2026 | Top-down | Consolidated FCFF with revenue recovering '+17% in 2026e on guidance, easing to +9% by 2030e' and the operating margin climbing from ~6% to 12-13%. GWh appears only in the EV-per-GWh replacement cross-check, not in the forecast. |
| **NVDA** | NVIDIA Corporation | NASDAQ | 06-07-2026 | Top-down | Data Center revenue is a growth fade - '~73% (FY27E) toward ~9% (FY31E)' - driven off aggregate hyperscaler AI capex. No GPU units x ASP build. |
| **ORAS** | Orascom Construction | EGX | 30-06-2026 | Top-down | 'We grow the base at 8% through an explicit five-year window, fade to a 3.5% terminal' on normalized operating profit, with a normalized working-capital drag. Backlog is context, not the driver. |
| **ORWE** | Oriental Weavers | EGX | 01-07-2026 | Top-down | FCFE off attributable profit with the working-capital drag as the crux; the segment section describes export/Egypt-retail/tufted/US-plant mix but the forecast is a growth-and-margin path, not m2 x price. |
| **QGTS** | Nakilat | QSE | 05-07-2026 | Top-down | Charter hire grows in the low-single digits on contract escalators and a handful of deliveries; EBITDA margin held near 71%. Fleet-anchored, but not a vessel-by-vessel day-rate build. |
| **RMDA** | Rameda Pharmaceuticals | EGX | 13-07-2026 | Top-down | 'The five-year explicit forecast is driven top-down (the data-discipline guard: unit volumes and ASPs by product are not separately disclosed, so channel growth x normalized margins is the honest build).' |
| **SABIC** | Saudi Basic Industries Corp | TADAWUL | 07-07-2026 | Top-down | 'SABIC does not disclose clean segment-EBITDA splits, so per the data-discipline gate we frame the mix top-down rather than manufacture segment margins.' Revenue fades 2.0-3.5%; EBITDA margin lifted from 15.5% to 19.0%. |
| **STC** | stc Group (Saudi Telecom) | TADAWUL | 09-07-2026 | Top-down | States it explicitly: 'the revenue engine is the section 1.6 segment build (top-down: stc discloses unit revenue, not subscriber x ARPU detail, so per the house data-discipline gate we forecast disclosed segment lines rather than manufacture a bottom-up split)'. Group revenue compounds ~3.0%; EBITDA margin glides. |
| **2POINTZERO** | Two Point Zero Group | ADX | 11-07-2026 | Asset / NAV / stake marks | Starts from audited owners' equity of AED 83.9bn and does three jobs: re-mark the operating businesses, discount the unlisted portfolio, discount the wrapper. The operating leg is revenue x a disclosed 30% gross margin less 18% admin costs. |
| **ACWA** | ACWA Power Company | TADAWUL | 05-07-2026 | Asset / NAV / stake marks | SOTP/NAV on marks: operating portfolio at the capitalised value of distributions (cross-checked on EV per MW), the under-construction book at invested equity plus a development uplift, the pipeline as risk-weighted option value, NOMAC on a fee-stream DCF. |
| **ALPHADHABI** | Alpha Dhabi Holding | ADX | 10-07-2026 | Asset / NAV / stake marks | SOTP NAV: audited FY2025 book equity with the five externally priceable assets re-marked (two at ADX prices, Trojan at the ADQ transaction, dual-framed) and everything else at book. Drivers are a revenue-growth path and a margin. |
| **BTFH** | Beltone Financial Holding | EGX | 03-07-2026 | Asset / NAV / stake marks | Financial-services SOTP: attributable book allocated across four platforms on a stated judgment (the group does not disclose allocated equity) and each bucket marked at a justified price-to-book. |
| **CCAP** | Qalaa Holdings | EGX | 30-06-2026 | Asset / NAV / stake marks | Holdco SOTP on economic interest: ERC at Qalaa's 13.14% economic stake net of ERC debt, TAQA Arabia at ~55% associate economics, the rest marked. 'The crux that remains is the discount, not the assets.' |
| **EMAAR** | Emaar Properties PJSC | DFM | 01-07-2026 | Asset / NAV / stake marks | RNAV/SOTP on marks: listed stakes at market, the recurring mall/hospitality portfolio at ~14x EBITDA, international development and parent net cash, less a 20% NAV/conglomerate discount. |
| **ETEL** | Telecom Egypt | EGX | 03-07-2026 | Asset / NAV / stake marks | SOTP: the core marked on 2026E EBITDA of EGP 52.6bn at 3.25x EV/EBITDA, the 45% Vodafone Egypt stake marked on earnings at 8.0x and cross-checked against the 2022 Vodacom transaction. |
| **HELI** | Heliopolis Housing | EGX | 03-07-2026 | Asset / NAV / stake marks | RNAV of the estate block by block: the two JDAs with disclosed economics at the PV of their contractual minimum guarantees, the undisclosed JDAs at EGP 9mn per feddan, unallocated plots at a cash EGP 8mn/fd. Land marks, not a development revenue build. |
| **HRHO** | EFG Holding | EGX | 01-07-2026 | Asset / NAV / stake marks | Holdco SOTP: the Investment Bank at 8x normalized profit, the NBFI platform anchored on the listed Valu stake, Bank NXT's group share at ~5.6x, holdco treasury at book, less a 20% holdco discount. |
| **IHC** | International Holding Company | ADX | 04-07-2026 | Asset / NAV / stake marks | Look-through SOTP at spot: the ~60% of Alpha Dhabi at Alpha Dhabi's own ADX market cap, other listed stakes look-through, the unlisted platforms (IRH, RIQ, the private tail) on book or a flagged house estimate. |
| **IQCD** | Industries Qatar | QSE | 05-07-2026 | Asset / NAV / stake marks | Holdco SOTP: each of fertilizers, petrochemicals and steel valued on normalized mid-cycle earnings and a justified P/E, plus net cash, less a holdco discount. |
| **KABO** | El Nasr Clothing & Textiles (Kabo) | EGX | 06-07-2026 | Asset / NAV / stake marks | RNAV off audited net assets plus a flagged land-and-buildings re-mark and a conservative brand value, less working-capital haircuts. 'KABO does not disclose an asset register'. |
| **KAKAO** | Kakao Corp. | KRX | 28-06-2026 | Asset / NAV / stake marks | Holdco SOTP: listed stakes at market, the two large unlisted subsidiaries at transaction marks, the core KakaoTalk platform on a mark, parent net cash, then a 32% NAV discount. The discount is the whole valuation. |
| **MAADEN** | Saudi Arabian Mining Company (Ma'aden) | TADAWUL | 05-07-2026 | Asset / NAV / stake marks | SOTP by commodity segment: each business marked on a normalized near-forward EBITDA and a peer-plus EV/EBITDA multiple, less consolidated net debt. No tonnes x price build. |
| **OIH** | Orascom Investment Holding | EGX | 03-07-2026 | Asset / NAV / stake marks | Holding-company NAV: ten marks each with its basis - cash, DPRK cash at 50% recovery, the Koryolink loan near face, the Pyramids platform as a standalone DCF - less a 15% holdco discount. |
| **RAYA** | Raya Holding | EGX | 01-07-2026 | Asset / NAV / stake marks | Eleven operating companies each marked on an instrument-appropriate basis - Aman on a P/E, RACC at the August-2025 tender price, the rest on EV/EBITDA by business type - less a holdco discount. |
| **RELIANCE** | Reliance Industries Limited | NSE | 06-07-2026 | Asset / NAV / stake marks | Holdco SOTP: Jio at 13.5x EV/EBITDA, Retail at 28x, O2C at 7x, E&P at 5x, Media at 14x, New Energy at invested capital plus option value, less net debt, minorities and a holdco discount. |
| **SAMSUNG** | Samsung Electronics Co., Ltd. | KRX | 27-06-2026 | Asset / NAV / stake marks | SOTP on normalised segment operating profit x multiples - memory credited a ~KRW 175tn AI-era plateau capitalised at 9x, the rest marked segment by segment. No wafer/unit build. |
| **TMPV** | Tata Motors Passenger Vehicles Ltd. | NSE | 30-06-2026 | Asset / NAV / stake marks | Holdco SOTP: JLR on normalized mid-cycle EBITDA x a luxury-auto multiple, India PV-ICE on a domestic EV/EBITDA, India EV on a haircut to the TPG/ADIA private round, plus a conglomerate discount. |
| **TSLA** | Tesla, Inc. | NASDAQ | 30-06-2026 | Asset / NAV / stake marks | Segment SOTP on multiples: automotive at ~15x normalized EBIT, energy on a growth multiple, services at a modest multiple, plus a probability-weighted autonomy/AI bucket. No deliveries x ASP build. |
| **ADCB** | Abu Dhabi Commercial Bank | ADX | 10-07-2026 | Bank driver build | The house's bank reference study, and unusually blunt: 'All eight of ADCB's drivers are top-down, because the bank reports blended results - net interest margin, cost-to-income, cost of risk - rather than the deposit-repricing betas, fee volumes or product unit-economics a bottom-up build would need.' |
| **ADIB** | ADIB-Egypt | EGX | 03-07-2026 | Bank driver build | Attributable earnings from a driver-built income statement: revenue growth fading from +31% to +13.5%, financing growth +53% to +15%, cost-to-income drifting to 20%, cost of risk ~1.0-1.1%. Blended bank metrics, no product unit economics. |
| **ADIBUAE** | Abu Dhabi Islamic Bank | ADX | 11-07-2026 | Bank driver build | 'All of ADIB's drivers are top-down, for a specific and checkable reason: the bank reports blended results ... rather than the deposit-repricing betas, fee volumes or product unit economics a bottom-up build would need.' The negative searches are logged. |
| **ALINMA** | Alinma Bank | TADAWUL | 10-07-2026 | Bank driver build | Three linked schedules - the margin engine (volumes x NIM), the efficiency and risk lines, and the capital the growth consumes. Financing volumes x margin, not product unit economics. |
| **ALRAJHI** | Al Rajhi Bank | TADAWUL | 02-07-2026 | Bank driver build | Net income from a NIM bridge, a fee line, cost-to-income and cost of risk, feeding a DuPont decomposition and a capital schedule. The study calls this 'a legitimate bottom-up build' because the components are disclosed - the same structure ADCB later labels top-down. |
| **COMI** | Commercial International Bank | EGX | 29-06-2026 | Bank driver build | Justified price-to-book / residual income on a sustainable ROE of 29.5% against a nominal cost of equity - '(29.5-16)/(24-16) = 1.69x'. The driver section is a qualitative scorecard of the sovereign-carry book and the deposit franchise. |
| **DIB** | Dubai Islamic Bank | DFM | 11-07-2026 | Bank driver build | 'DIB does not [disclose the components]: it reports blended outcomes - a net profit margin, a cost-to-income ratio, a cost of risk ... So every driver here is set top-down from the outcomes the bank does report.' |
| **ENBD** | Emirates NBD Bank | DFM | 03-07-2026 | Bank driver build | Residual income: (ROTE - Ke) x opening tangible book with ROTE fading from ~19% to a sustainable ~15.5% and book compounding at the retained portion of earnings. |
| **FAB** | First Abu Dhabi Bank | ADX | 03-07-2026 | Bank driver build | Five years of dividends plus a terminal book x a justified P/B from the residual-income identity (ROE - g)/(Ke - g) on a sustainable terminal ROE of 15.5%. |
| **QNB** | QNB Group | QSE | 05-07-2026 | Bank driver build | FY25 EPS of QAR 1.74 grown at 4% then re-accelerating to 5-7%, payout rising 43% to 47%, terminal payout 60%. An EPS growth path, not a balance-sheet driver build. |
| **RIBL** | Riyad Bank | TADAWUL | 09-07-2026 | Bank driver build | Net income from a NIM path, a fee line, cost-to-income and cost of risk with a DuPont and capital schedule. 'FY23-25 are disclosed; the forward path is the house view.' |
| **SNB** | The Saudi National Bank | TADAWUL | 04-07-2026 | Bank driver build | 'We forecast net special commission income as NIM x average earning assets rather than a top-down growth rate', with a DuPont decomposition and an explicit forward capital schedule. |

---

## What the pattern shows

**1. Build depth tracks the study's vintage almost perfectly.**

| Study edition | Bottom-up | Not bottom-up |
|---|---|---|
| 2026-06 | 5 | 8 |
| 2026-07 | 5 | 53 |
| 2026-08 | 17 | 2 |

The August-2026 cohort is 17 bottom-up against 2 not; the
July-2026 cohort is 5 against 53. Bottom-up construction is
not distributed across the book — it arrived with the current protocol and has been applied
to whatever has been rebuilt since.

**2. The code-built studies are where the unit builds live.**
Of the 21 stocks whose study carries an
`engine/<name>_study/` directory with a `compute.py`, **18** are bottom-up and
3 are not (MODON and SWDY stop at segment level on disclosure grounds; STC is
top-down by an explicit gate decision). Of the 69 studies
with no code directory, only 9 are bottom-up — the five Egyptian developers,
plus SALIK, LULU, CLHO and DSCW.

**3. Most non-bottom-up studies say so, and say why.**
This is the protocol's flag-the-gap rule working rather than failing. STC, ADNOCGAS, AGTHIA,
RMDA, SABIC, SWDY, MODON and CLHO each name the missing disclosure in the delivered document
before falling back. The refusals are consistent: no study manufactures a volume/price split
the filings do not support.

**4. Tier B is a real distinction and should not be read as tier A.**
Seven studies have the full shape of a unit build on units that are *not disclosed*: ELEC
back-solves tonnage from LME copper and FX; RIYADHCABLE runs a tonnage *index* (FY2025 = 100)
because the company publishes no tonnage; and the five Egyptian developers (PHDC, TMGH, OCDI,
ORHD, EMFD) price every project from a unit mix per square metre that four of the five state
outright is "the preparer's estimates ... illustrative, not authoritative", calibrated so the
model reproduces disclosed totals. ARCC is the cautionary precedent inside the house: three
earlier editions back-solved cement tonnes from an assumed price and presented the resulting
utilisation as corroboration — an accounting identity that reproduces audited revenue for *any*
price. Those editions were withdrawn once the disclosed volumes were read.

**5. One live inconsistency in self-labelling, in the bank class.**
ADCB — the house's bank reference study — states that "all eight of ADCB's drivers are top-down,
because the bank reports blended results ... rather than the deposit-repricing betas, fee volumes
or product unit-economics a bottom-up build would need". ADIB and DIB repeat that wording.
But Al Rajhi, on a structurally identical NIM / cost-to-income / cost-of-risk bridge, calls the
same construction "a legitimate bottom-up build rather than a manufactured one", and SNB says it
forecasts net special commission income as "NIM × average earning assets rather than a top-down
growth rate". The substance is the same in all of them; only the label differs. This audit applies
the ADCB reading — the governing bank precedent — and puts all twelve banks in tier F, outside
bottom-up. Worth reconciling in the protocol so the term means one thing across the book.
