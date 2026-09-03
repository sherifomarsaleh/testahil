# Cost of capital — the reference tables, generated

**GENERATED from `engine/macro_paths/*.json` by `engine/build_coc_reference.py`. Never hand-edited.** Every figure below resolves from a committed macro path at build time; a number whose source has moved fails the build rather than printing stale. To change a figure, change the path file and re-run this.

Sourced 2026-09-03. Read the live state with `python3 engine/macro_path.py`, never this file from memory — it is regenerated whenever a path is re-sourced.


## What is held

| Market | State | Regime | Currency |
|---|---|---|---|
| EG | sourced, as of 2026-09-02 | transition | EGP |
| AE | sourced, as of 2026-09-03 | pegged | AED |
| SA | sourced, as of 2026-09-03 | pegged | SAR |
| QA | sourced, as of 2026-09-03 | pegged | QAR |
| IN | sourced, as of 2026-09-03 | mature | INR |
| KR | sourced, as of 2026-09-03 | mature | KRW |
| US | sourced, as of 2026-09-03 | mature | USD |

A market reading **pending** RAISES on load. There is no fallback to a neighbouring market, a region or a global average: an empty answer is not a clean answer, and the cost of a missing path is a study that stops, not a study built on a number nobody sourced.


---

## EG — EGP

Regime: **transition**. The policy rate sits far above its own long-run level and the central bank publishes a disinflation path, so the cost-of-capital glide applies here [Standing_Research_Protocol, 13-Jul r3 SCOPE]. Contrast the pegged markets, where today is already the terminal.


### Inflation

| Year | Rate | Basis |
|---|---:|---|
| 2026 | 16.00% | CBE baseline, average annual headline |
| 2027 | 12.00% | CBE baseline, average annual headline |
| 2028 | 9.00% | interpolated on the CBE's own stated glide from the 2027 baseline to the Q4-2028 target band midpoint, no year outside the published endpoints |
| 2029 | 7.50% | interpolated, as 2028 |
| 2030 | 7.00% | the target band midpoint in force, held |
| terminal | 7.00% | the target band midpoint in force |

Latest print: **14.90%** (July 2026, annual headline). Target: **7.0% ± 2.0pp**, Q4 2026.


### Rates

| | Value | As of |
|---|---:|---|
| Policy rate | 19.00% | 2026-08-20 |
| Sovereign 10-year | 23.00% | 2026-08-06 |
| Default spread, rating basis | 6.37% | |
| Default spread, market basis | 3.41% | |
| Terminal cost of debt | 15.00% | long-run corporate norm |
| Terminal equity risk premium | 7.00% | normalised |

**Policy-rate path** (the SHAPE input for the cost-of-capital glide, never a second free parameter): 19.00% → 16.50% → 14.50% → 13.00% → 12.00%


### The derived terminal

Nothing in this block is a quote. Each line is an identity on the numbers above, because a terminal rate reverse-engineered from a price is the quietest lever there is.

| | Identity | Value |
|---|---|---:|
| Terminal risk-free | terminal inflation + real-rate convention (5.50%) | **12.50%** |
| Terminal growth, zero real | terminal inflation + stated real growth (0.00%) | **7.00%** |

### The currency, derived

Relative purchasing-power parity on this path's own inflation against long-run United States inflation of 2.50%. A study may not set this by hand.

| Year | Depreciation | USD/EGP |
|---|---:|---:|
| 2026 | 13.17% | 55.11 |
| 2027 | 9.27% | 60.22 |
| 2028 | 6.34% | 64.04 |
| 2029 | 4.88% | 67.17 |
| 2030 | 4.39% | 70.11 |

### Sources

- **inflation.latest** — Central Bank of Egypt, Monetary Policy Committee statement of 20 August 2026: annual headline inflation 14.9% in July 2026 against 14.3% in June; core 14.7% against 14.3%; monthly headline and core both 0.0% in July.
- **inflation.path** — Central Bank of Egypt Q1-2026 Monetary Policy Report as reported 11 May 2026: baseline average annual headline inflation 16.0% in 2026 and 12.0% in 2027 (alternative scenario, conflict persisting to end-2026: 17.0% and 13.0%, single digits in H2-2027). The 2028-2030 steps are a straight glide between the published 2027 baseline and the target midpoint; they are INTERPOLATION BETWEEN PUBLISHED ENDPOINTS and are labelled as such, never presented as a central-bank forecast.
- **inflation.target** — CBE inflation target 7% (+/-2pp) for Q4 2026; the bank states inflation will remain ABOVE the band in Q4 2026 and expects a return to it in the second half of 2027.
- **inflation.terminal** — The target band midpoint IN FORCE at the terminal horizon. The 5% (+/-2pp) figure once quoted for Q4 2028 is NOT used: the bank's own August 2026 guidance puts the return to the 7% band in the second half of 2027, so a terminal built on 5% would assume an undershoot the bank does not forecast. AMOC's edition of 06-Aug-2026 made exactly this correction and it is inherited here rather than re-litigated.
- **policy_rate** — Central Bank of Egypt Monetary Policy Committee, 20 August 2026 — rates held for a fourth consecutive meeting.
- **policy_rate.path** — Overnight deposit rate, 2026-2030, gliding with the published inflation path at an approximately constant real policy rate. It is the SHAPE input for the cost-of-capital glide and for the cost-of-debt path; it is not a second free parameter and no valuation input is set from it independently.
- **sovereign** — Egypt 10-year EGP government bond yield, market quote 6 August 2026, the quote already registered and used by the PHDC and EGCH cost-of-capital records. RE-SOURCE BEFORE ANY NEW STRIKE: this is the input the 14-day staleness rule bites on.
- **sovereign.spreads** — Damodaran country risk file, Egypt row, as registered by the studies' own cost-of-capital records (rating basis 6.37%, market basis 3.41%, which for Egypt is the credit-default-swap quote). Both bases are carried; which one is CENTRAL is a cost-of-capital decision, not a macro one. [FIELD RENAMED 03-Sep-2026: the two bases are RATING and MARKET. A CDS is one market instrument and it is the one Egypt has; the UAE has no CDS series at all, so a field named cds could not be filled there honestly.]
- **fx** — USD/EGP 50.25, quote of 6 August 2026 as registered in the AMOC cost-of-capital record; the pound closed 50.30/50.40 on 4 August 2026 and its 52-week range is 46.64-54.86, so the currency is not range-bound.
- **fx.derivation** — The forward currency path is DERIVED from this path's own inflation ladder against long-run United States inflation by relative purchasing-power parity, never set by hand. A study that escalates costs at Egyptian inflation while depreciating the pound at a third of the differential is running two views of one economy [L-048].
- **us_inflation_lt** — Long-run United States consumer price inflation, the foreign leg of the purchasing-power-parity relation. Registered at 2.5% by AMOC (06-Aug-2026) and at 2.4% by EGCH; 2.5% is adopted for the house path and the 10bp difference is immaterial to any derived figure at this precision.
- **cost_of_debt_norm** — The long-run Egyptian corporate-borrowing norm, 14-16%, midpoint 15% absent a name-specific reason to deviate [Standing_Research_Protocol 13-Jul r2, clause 4].
- **real_rate_convention** — The standard emerging-market terminal real risk-free convention (~5.5pp). The terminal NOMINAL risk-free rate is DERIVED as this plus the inflation target in force, so the single most terminal-value-sensitive number in a model cannot be typed.
- **erp_terminal** — Terminal equity risk premium, normalised below the currently elevated crisis-era level toward the rating-class norm; never held flat into perpetuity.

---

## AE — AED

Regime: **pegged**. The dirham is hard-pegged to the dollar at 3.6725, so the UAE imports United States monetary policy and TODAY IS ALREADY THE TERMINAL: the cost-of-capital glide does not apply here and cost_of_capital.py returns a FLAT schedule for this market by construction of the peg, not by a choice made in this file. What the peg does NOT supply is a domestic inflation ladder, and the cost escalators need one — which is why this path exists at all and why it was the stated blocker on 28 UAE names.


### Inflation

| Year | Rate | Basis |
|---|---:|---|
| 2026 | 2.50% | IMF World Economic Outlook projection |
| 2027 | 2.00% | IMF World Economic Outlook projection |
| 2028 | 2.00% | IMF World Economic Outlook projection |
| 2029 | 2.00% | IMF World Economic Outlook projection |
| 2030 | 2.00% | IMF World Economic Outlook projection |
| terminal | 2.00% | the target band midpoint in force |

Latest print: **1.30%** (2025, annual average consumer prices). Target: **2.0% ± 0.5pp**, long run.


### Rates

| | Value | As of |
|---|---:|---|
| Policy rate | 3.75% | 2026-09-03 |
| Sovereign 10-year | 4.48% | 2026-07-30 |
| Default spread, rating basis | 0.42% | |
| Default spread, market basis | 0.04% | |
| Terminal cost of debt | 5.20% | long-run corporate norm |
| Terminal equity risk premium | 4.29% | normalised |

**Policy-rate path** (the SHAPE input for the cost-of-capital glide, never a second free parameter): 3.75% → 3.45% → 3.25% → 3.10% → 3.10%


### The derived terminal

Nothing in this block is a quote. Each line is an identity on the numbers above, because a terminal rate reverse-engineered from a price is the quietest lever there is.

| | Identity | Value |
|---|---|---:|
| Terminal risk-free | terminal inflation + real-rate convention (1.98%) | **3.98%** |
| Terminal growth, zero real | terminal inflation + stated real growth (0.00%) | **2.00%** |

### The currency, derived

Relative purchasing-power parity on this path's own inflation against long-run United States inflation of 2.20%. A study may not set this by hand.

| Year | Depreciation | USD/AED |
|---|---:|---:|
| 2026 | 0.00% | 3.67 |
| 2027 | 0.00% | 3.67 |
| 2028 | 0.00% | 3.67 |
| 2029 | 0.00% | 3.67 |
| 2030 | 0.00% | 3.67 |

### Sources

- **inflation.latest** — International Monetary Fund, World Economic Outlook database, series PCPIPCH (inflation, average consumer prices, annual percent change), United Arab Emirates (ARE), read live from the IMF datamapper API on 3 September 2026.
- **inflation.path** — International Monetary Fund, World Economic Outlook database, series PCPIPCH (inflation, average consumer prices, annual percent change), United Arab Emirates (ARE), read live from the IMF datamapper API on 3 September 2026. The published series runs to 2031 and prints 2.0% flat from 2027 onward, so NO STEP HERE IS INTERPOLATED — every year is a published figure and none is a house view. The 2025 actual of 1.3% and the 2024 actual of 1.7% are from the same series and are recorded above as the latest observation.
- **inflation.target** — THE UAE PUBLISHES NO INFLATION TARGET OF ITS OWN AND THIS FILE DOES NOT INVENT ONE. Under a hard peg the anchor is the one the currency is pegged TO: the Federal Reserve's 2 percent longer-run objective, transmitted through the peg. The band of 0.5pp is the dispersion of the IMF's own published UAE projections about that anchor over 2026-2031 (2.5% in 2026, 2.0% thereafter), not a tolerance chosen here.
- **inflation.terminal** — The IMF's own published UAE figure for every year from 2027 to 2031, held. It coincides with the Federal Reserve's longer-run objective, which is what a hard peg should produce and is a coherence check rather than a second assumption.
- **policy_rate** — The CBUAE Base Rate is set at the Fed's interest on reserve balances and moves with it by construction of the peg, so the POLICY anchor for this market is the United States policy rate. Federal Reserve H.15 via FRED, series DFEDTARU (target range upper limit) 3.75% and DFF (effective federal funds rate) 3.63%, read live on 3 September 2026.
- **policy_rate.path** — A glide from the live 3.75% target upper limit to the FOMC's OWN longer-run median federal funds projection of 3.1% (Summary of Economic Projections, 17 June 2026, FRED series FEDTARMDLR), reached by 2029 and held. The endpoints are both published; the two years between them are a straight line and are the only interpolated figures in this file. It is the SHAPE input for the glide and for the cost-of-debt path, and no valuation input is set from it independently. Under the peg the glide's SCOPE is nil in any case: this market is already terminal.
- **sovereign** — AED risk-free anchor: the UAE federal AED Treasury Bond, JANUARY-2031 tranche, auction yield 4.48%, UAE Ministry of Finance / WAM results release of 30 July 2026. THE TENOR IS ABOUT FIVE YEARS, NOT TEN, AND THAT IS SAID HERE RATHER THAN LEFT IN THE FIELD NAME: the AED federal curve does not print a liquid ten-year point, and the alternative is a peg-extrapolated proxy (Abu Dhabi sovereign USD 10-year 4.73%, February-2026 issue at UST+25bp, less the ~4bp AED-through-USD basis = 4.69%) which is a different issuer in a different currency. The federal AED instrument is adopted because the risk-free rate and the default spread below are then measured on the SAME instrument, which is what keeps country risk entering exactly once. Registered and audited against an external critique by the DU study, 17 August 2026.
- **sovereign.spreads** — RATING BASIS 0.42%: A. Damodaran, country default spreads and risk premiums (ctryprem), 5 January 2026, United Arab Emirates row, Moody's Aa2 rating-based adjusted default spread; paired with the 4.87% rating-basis total ERP (4.23% mature base + 0.64% country premium). MARKET BASIS 0.04%: the spread the very instrument above prices at over the comparable US Treasury, read from the MoF/WAM auction release; paired with the 4.29% market-basis ERP (4.23% mature base + a 6bp country premium scaled off the 4bp spread on Damodaran's own CRP/spread multiple of 0.64/0.42). THE MARKET BASIS COULD NOT HAVE BEEN A CDS AT ALL, AND THAT IS WHY THE FIELD IS NAMED FOR THE BASIS RATHER THAN THE INSTRUMENT: the original Damodaran file, read live on 3 September 2026, carries the United Arab Emirates row as Aa2 with an adjusted default spread of 0.42%, a country risk premium of 0.64%, a total ERP of 4.87%, a corporate tax rate of 9.00% — and 'NA' in BOTH credit-default-swap columns. An existing study records the same fact in as many words ('NA for UAE'). A field named default_spread_cds could therefore only ever have been filled here by putting something that is not a CDS into it, which is precisely the key-that-lies defect found the same day in a study's own register. A THIRD FIGURE EXISTS AND IS NOT ADOPTED: an Abu Dhabi sovereign CDS spread of 0.46% registered by the FERTIGLOBE study on 9 August 2026. It appears nowhere in the original file today, and it is a DIFFERENT ISSUER in a DIFFERENT CURRENCY — an emirate's USD CDS against the federation's AED bond — so adopting it would break the same-instrument discipline the market basis exists to keep. Recorded so a later session finds it named rather than absent. WHICH BASIS IS CENTRAL IS A COST-OF-CAPITAL DECISION, NOT A MACRO ONE; both are carried. DU adopted the market basis on 17 August 2026 after an external critique, on the ground that the rating basis breaches the matched-tenor Treasury floor.
- **fx** — The dirham has been pegged to the United States dollar at 3.6725 since 1997. World Bank series PA.NUS.FCRF (official exchange rate, LCU per US$, period average), United Arab Emirates, 2025 = 3.6725, read live 3 September 2026.
- **fx.derivation** — THE CURRENCY PATH IS THE PEG AND IS NOT DERIVED FROM PURCHASING-POWER PARITY. Egypt's path derives its currency from its own inflation ladder against long-run foreign inflation because the pound floats; applying that identity here would manufacture a drift the peg forbids, and the 0.5pp gap between UAE and US long-run inflation is a REAL exchange-rate movement absorbed inside a fixed nominal rate, not a nominal depreciation. A study that depreciates the dirham is making a claim about the peg breaking and must argue it as one.
- **us_inflation_lt** — Long-run United States consumer price inflation, 2.2%, the IMF World Economic Outlook's own published United States figure for 2029, 2030 and 2031 (series PCPIPCH, USA), read live 3 September 2026. SOURCED RATHER THAN CONVENTIONAL: the EG path carries 2.5% registered from two studies' own conventions, and where a published figure exists it is used.
- **cost_of_debt_norm** — The long-run UAE corporate borrowing norm, 4.9-5.6%, midpoint 5.2%, taken from the TERMINAL costs of debt this house has already sourced and audited across six UAE names from their own facility notes: DU 4.90%, AIRARABIA 5.00%, ADNOCLS 5.01%, ADNOCDIST 5.08%, MODON 5.36%, BOROUGE 5.55%. It is a range with a midpoint, and a name with a facility note of its own uses that note rather than this figure — the norm is the floor of last resort, not a substitute for the three-assert Kd gate.
- **real_rate_convention** — DERIVED, NEVER QUOTED, so the single most terminal-value-sensitive number in a model cannot be typed. The long-run United States real ten-year rate = the FOMC's own longer-run median federal funds projection (3.1%, Summary of Economic Projections of 17 June 2026, FRED FEDTARMDLR) plus the ten-year term premium (0.8751%, Kim-Wright, FRED THREEFYTP10, 28 August 2026) less long-run US inflation (2.2%, IMF WEO above) = 1.9751%. Under the peg the AED real rate is the USD real rate. CROSS-CHECK, NOT AN INPUT: the observed ten-year TIPS real yield is 2.45% (FRED DFII10, 2 September 2026), which is a SPOT price carrying today's cyclical position and is 48bp above this long-run construction — the direction and size a reader should expect, and it is recorded rather than averaged in. The derived terminal AED risk-free rate is therefore 2.0% + 1.9751% = 3.9751%, against a live 4.48% federal auction yield: a mild normalisation, not a rate call.
- **erp_terminal** — Terminal equity risk premium held at the market-basis UAE ERP of 4.29%. NO STRUCTURAL CONVERGENCE IS ASSUMED, and unlike Egypt that is not a normalisation declined: an Aa2 sovereign already priced at 4bp over US Treasuries has essentially no country premium left to converge. Registered by the DU study, 1 August 2026.

---

## SA — SAR

Regime: **pegged**. The riyal is pegged to the dollar at 3.75, so Saudi Arabia imports United States monetary policy — SAMA's repo rate tracks the Fed — and TODAY IS ALREADY THE TERMINAL: the cost-of-capital glide does not apply and cost_of_capital.py returns a FLAT schedule by construction of the peg. What the peg does not supply is a domestic inflation ladder, which the cost escalators need.


### Inflation

| Year | Rate | Basis |
|---|---:|---|
| 2026 | 2.30% | IMF World Economic Outlook projection |
| 2027 | 2.10% | IMF World Economic Outlook projection |
| 2028 | 2.00% | IMF World Economic Outlook projection |
| 2029 | 2.00% | IMF World Economic Outlook projection |
| 2030 | 2.00% | IMF World Economic Outlook projection |
| terminal | 2.00% | the target band midpoint in force |

Latest print: **2.00%** (2025, annual average consumer prices). Target: **2.0% ± 0.5pp**, long run.


### Rates

| | Value | As of |
|---|---:|---|
| Policy rate | 3.75% | 2026-09-03 |
| Sovereign 10-year | 5.52% | 2026-07-31 |
| Default spread, rating basis | 0.51% | |
| Default spread, market basis | 0.98% | |
| Terminal cost of debt | 5.50% | long-run corporate norm |
| Terminal equity risk premium | 5.01% | normalised |

**Policy-rate path** (the SHAPE input for the cost-of-capital glide, never a second free parameter): 3.75% → 3.45% → 3.25% → 3.10% → 3.10%


### The derived terminal

Nothing in this block is a quote. Each line is an identity on the numbers above, because a terminal rate reverse-engineered from a price is the quietest lever there is.

| | Identity | Value |
|---|---|---:|
| Terminal risk-free | terminal inflation + real-rate convention (1.98%) | **3.98%** |
| Terminal growth, zero real | terminal inflation + stated real growth (0.00%) | **2.00%** |

### The currency, derived

Relative purchasing-power parity on this path's own inflation against long-run United States inflation of 2.20%. A study may not set this by hand.

| Year | Depreciation | USD/SAR |
|---|---:|---:|
| 2026 | 0.00% | 3.75 |
| 2027 | 0.00% | 3.75 |
| 2028 | 0.00% | 3.75 |
| 2029 | 0.00% | 3.75 |
| 2030 | 0.00% | 3.75 |

### Sources

- **inflation.latest** — International Monetary Fund, World Economic Outlook database, series PCPIPCH (inflation, average consumer prices, annual percent change), Saudi Arabia (SAU), read live from the IMF datamapper API on 3 September 2026.
- **inflation.path** — International Monetary Fund, World Economic Outlook database, series PCPIPCH (inflation, average consumer prices, annual percent change), Saudi Arabia (SAU), read live from the IMF datamapper API on 3 September 2026. The series runs to 2031 and prints 2.0% flat from 2028 onward, so NO STEP HERE IS INTERPOLATED — every year is published.
- **inflation.target** — SAUDI ARABIA PUBLISHES NO INFLATION TARGET AND THIS FILE DOES NOT INVENT ONE. Under a hard peg the anchor is the one the currency is pegged to: the Federal Reserve's 2 percent longer-run objective. The 0.5pp band is the dispersion of the IMF's own published Saudi projections about that anchor over 2026-2031.
- **inflation.terminal** — The IMF's own published Saudi figure for every year from 2028 to 2031, held; it coincides with the Federal Reserve's longer-run objective, which is what a hard peg should produce.
- **policy_rate** — SAMA's policy rate tracks the Fed by construction of the peg, so the policy ANCHOR for this market is the United States policy rate. Federal Reserve H.15 via FRED, DFEDTARU 3.75% and DFF 3.63%, read live 3 September 2026.
- **policy_rate.path** — A glide from the live 3.75% target upper limit to the FOMC's own longer-run median federal funds projection of 3.1% (Summary of Economic Projections, 17 June 2026, FRED FEDTARMDLR), reached by 2029 and held. Both endpoints published; the two years between are a straight line and are the only interpolated figures here. Under the peg the glide's SCOPE is nil: this market is already terminal.
- **sovereign** — PUBLISHED SAR sovereign curve: FTSE Saudi Government Bond Index (SAGBI) factsheet of 31 July 2026, 7-10 year maturity bucket, yield to maturity 5.52%. Registered by the SAVOLA study and independently re-derived by RIYADHCABLE after an external audit (5.50% on the 10-year local-currency sukuk), so two studies agree to 2bp on separate routes.
- **sovereign.spreads** — A. Damodaran, 'Country Default Spreads and Risk Premiums', ctryprem, LAST UPDATED 5 JANUARY 2026, read live from the original file on 3 September 2026. Saudi Arabia row: Moody's Aa3; adjusted default spread 0.51% (rating basis); credit-default-swap spread 0.98% (market basis); country risk premium 0.78%; total equity risk premium 5.01% on the rating basis and 5.72% on the CDS basis. THE LIVE FILE IS THE JANUARY-2026 VINTAGE and that is stated rather than implied: two Saudi studies cite a JULY-2026 vintage carrying 0.48% and 4.94%, which is an archived mid-year file and not what the original now serves. This path carries the ORIGINAL FILE AS IT STANDS, which is what the standing rule requires ('looked up FRESH in the ORIGINAL ctryprem file for that specific sovereign'). A DISAGREEMENT BETWEEN TWO STUDIES IS RESOLVED HERE RATHER THAN LEFT: SAVOLA registers a market-basis ERP of 5.72% and RIYADHCABLE '~4.90%'. The live file says 5.72% to the basis point and 4.90% appears in it nowhere, so SAVOLA's figure is adopted and RIYADHCABLE's is recorded as unreproducible against the original.
- **fx** — The riyal has been pegged to the United States dollar at 3.75 since 1986. World Bank series PA.NUS.FCRF (official exchange rate, LCU per US$, period average), Saudi Arabia, 2024 and 2025 both 3.75, read live 3 September 2026.
- **fx.derivation** — THE CURRENCY PATH IS THE PEG. Egypt's path derives its currency from its own inflation ladder by relative purchasing-power parity because the pound floats; applying that identity here would manufacture a drift the peg forbids, and macro_path.depreciation_path() returns zeros for a pegged regime for exactly that reason. A study that depreciates the riyal is making a claim about the peg breaking and must argue it as one.
- **us_inflation_lt** — Long-run United States consumer price inflation 2.2%, the IMF World Economic Outlook's own published United States figure for 2029, 2030 and 2031 (PCPIPCH, USA), read live 3 September 2026.
- **cost_of_debt_norm** — The long-run Saudi corporate borrowing norm, 5.40-5.75%, midpoint 5.50%, from the terminal and marginal costs of debt this house has already sourced from the two Saudi names' own facility notes: RIYADHCABLE terminal 5.50% (marginal 5.90%) and SAVOLA blended SAR 5.74% (loans 5.88%, leases 5.86%, other 5.50%). A name with a facility note of its own uses that note; the norm is the floor of last resort and never a substitute for the three-assert Kd gate.
- **real_rate_convention** — DERIVED, NEVER QUOTED. Under the peg the SAR real rate is the USD real rate: the FOMC's own longer-run median federal funds projection (3.1%, Summary of Economic Projections of 17 June 2026, FRED FEDTARMDLR) plus the ten-year term premium (0.8751%, Kim-Wright, FRED THREEFYTP10, 28 August 2026) less long-run US inflation (2.2%, IMF WEO above) = 1.9751%. CROSS-CHECK, NOT AN INPUT: the observed ten-year TIPS real yield is 2.45% (FRED DFII10, 2 September 2026), a spot price carrying today's cyclical position, 48bp above this long-run construction. The derived terminal SAR risk-free rate is 2.0% + 1.9751% = 3.9751% against a live 5.52% index yield: a normalisation, not a rate call, and the 154bp gap is larger than the UAE's because the SAR curve prints well above the AED one.
- **erp_terminal** — A. Damodaran, 'Country Default Spreads and Risk Premiums', ctryprem, LAST UPDATED 5 JANUARY 2026, read live from the original file on 3 September 2026. Terminal equity risk premium held at the RATING-basis Saudi ERP of 5.01% rather than compressed. RIYADHCABLE registers 4.70%, 'a mild compression of the current 4.94% as the country risk premium narrows with Vision-2030'; that is a HOUSE VIEW ABOUT A REFORM PROGRAMME and this path does not carry one — a terminal premium below the sovereign's own published premium has to be argued, and the argument is not in the sourced record. Recorded so the declined figure is named rather than absent.

---

## QA — QAR

Regime: **pegged**. The riyal is pegged to the dollar at 3.64, so Qatar imports United States monetary policy and TODAY IS ALREADY THE TERMINAL: cost_of_capital.py returns a FLAT schedule by construction of the peg. What the peg does not supply is a domestic inflation ladder, which the cost escalators need.


### Inflation

| Year | Rate | Basis |
|---|---:|---|
| 2026 | 3.90% | IMF World Economic Outlook projection |
| 2027 | 2.50% | IMF World Economic Outlook projection |
| 2028 | 2.00% | IMF World Economic Outlook projection |
| 2029 | 2.00% | IMF World Economic Outlook projection |
| 2030 | 2.00% | IMF World Economic Outlook projection |
| terminal | 2.00% | the target band midpoint in force |

Latest print: **0.60%** (2025, annual average consumer prices). Target: **2.0% ± 0.5pp**, long run.


### Rates

| | Value | As of |
|---|---:|---|
| Policy rate | 3.75% | 2026-09-03 |
| Sovereign 10-year | 5.26% | 2026-09-03 |
| Default spread, rating basis | 0.42% | |
| Default spread, market basis | 0.47% | |
| Terminal cost of debt | 5.25% | long-run corporate norm |
| Terminal equity risk premium | 4.87% | normalised |

**Policy-rate path** (the SHAPE input for the cost-of-capital glide, never a second free parameter): 3.75% → 3.45% → 3.25% → 3.10% → 3.10%


### The derived terminal

Nothing in this block is a quote. Each line is an identity on the numbers above, because a terminal rate reverse-engineered from a price is the quietest lever there is.

| | Identity | Value |
|---|---|---:|
| Terminal risk-free | terminal inflation + real-rate convention (1.98%) | **3.98%** |
| Terminal growth, zero real | terminal inflation + stated real growth (0.00%) | **2.00%** |

### The currency, derived

Relative purchasing-power parity on this path's own inflation against long-run United States inflation of 2.20%. A study may not set this by hand.

| Year | Depreciation | USD/QAR |
|---|---:|---:|
| 2026 | 0.00% | 3.64 |
| 2027 | 0.00% | 3.64 |
| 2028 | 0.00% | 3.64 |
| 2029 | 0.00% | 3.64 |
| 2030 | 0.00% | 3.64 |

### Sources

- **inflation.latest** — International Monetary Fund, World Economic Outlook database, series PCPIPCH (inflation, average consumer prices, annual percent change), Qatar (QAT), read live from the IMF datamapper API on 3 September 2026.
- **inflation.path** — International Monetary Fund, World Economic Outlook database, series PCPIPCH (inflation, average consumer prices, annual percent change), Qatar (QAT), read live from the IMF datamapper API on 3 September 2026. The series runs to 2031 and prints 2.0% flat from 2028 onward; no step here is interpolated. THE NEAR YEARS ARE UNUSUALLY WIDE — a 0.6% actual in 2025 against a 3.9% projection for 2026 — and that swing is the published series, recorded rather than smoothed toward the terminal.
- **inflation.target** — QATAR PUBLISHES NO INFLATION TARGET AND THIS FILE DOES NOT INVENT ONE. Under a hard peg the anchor is the one the currency is pegged to: the Federal Reserve's 2 percent longer-run objective. The 0.5pp band is the dispersion of the IMF's own published Qatari projections about that anchor over 2028-2031, where the series has settled; the wide 2026-27 years are transition, not dispersion about a long-run anchor.
- **inflation.terminal** — The IMF's own published Qatari figure for 2028 through 2031, held; it coincides with the Federal Reserve's longer-run objective, which is what a hard peg should produce.
- **policy_rate** — The Qatar Central Bank's policy rates track the Fed by construction of the peg, so the policy ANCHOR for this market is the United States policy rate. Federal Reserve Economic Data (FRED), series DFEDTARU 3.75% and DFF 3.63%, read live 3 September 2026.
- **policy_rate.path** — A glide from the live 3.75% target upper limit to the FOMC's own longer-run median of 3.1% (SEP, 17 June 2026, FRED FEDTARMDLR), reached by 2029 and held. Under the peg the glide's SCOPE is nil: this market is already terminal.
- **sovereign** — DERIVED, AND LABELLED AS DERIVED BECAUSE NO PUBLISHED QAR SOVEREIGN CURVE WAS OBTAINABLE. Every other path on this book carries an OBSERVED local-currency government yield — an auction result, an index factsheet, a central-bank series — and Qatar has none this session could reach: FRED publishes no Qatari long-term rate series, and the World Bank's Qatari rate series is a COMMERCIAL LENDING rate (4.754% for 2025), which is a bank's price to a borrower and not a sovereign yield. Substituting it would have been the wrong instrument wearing the right field name, which is the defect this book spent the day removing. THE IDENTITY USED INSTEAD: under a hard peg a QAR sovereign yield is the USD sovereign yield plus Qatar's own credit spread. US ten-year Treasury 4.79% (FRED DGS10, 2 September 2026) plus the Qatar credit-default-swap spread of 0.47% (Damodaran, 5 January 2026) = 5.26%. Both legs are published; only their sum is constructed. IT IS A SYNTHETIC AND A STUDY MUST SAY SO WHEREVER IT QUOTES A QATARI RISK-FREE RATE, and the first Qatari study that can obtain a real QAR auction or index yield replaces this outright rather than reconciling to it.
- **sovereign.spreads** — A. Damodaran, 'Country Default Spreads and Risk Premiums', ctryprem, LAST UPDATED 5 JANUARY 2026, read live from the original file on 3 September 2026. Qatar row: Moody's Aa2; adjusted default spread 0.42% (rating basis); credit-default-swap spread 0.47% (market basis); country risk premium 0.64%; total ERP 4.87% on the rating basis and 4.94% on the CDS basis. UNLIKE THE UAE, QATAR DOES CARRY A CDS IN THIS FILE, and the two bases sit 5bp apart — so which is central barely moves a Qatari valuation, which is worth stating because on India the same choice is worth 185bp of equity premium.
- **fx** — The Qatari riyal has been pegged to the United States dollar at 3.64 since 2001. World Bank series PA.NUS.FCRF (official exchange rate, LCU per US$, period average), Qatar, 2025 = 3.64, read live 3 September 2026.
- **fx.derivation** — THE CURRENCY PATH IS THE PEG. macro_path.depreciation_path() returns zeros for a pegged regime, so the purchasing-power-parity identity that governs a floating currency cannot manufacture a drift the peg forbids. A study that depreciates the riyal is making a claim about the peg breaking and must argue it as one.
- **us_inflation_lt** — Long-run United States CPI inflation 2.2%, the IMF's own published figure for 2029-2031.
- **cost_of_debt_norm** — The long-run Qatari corporate borrowing norm, taken as the derived terminal risk-free rate of 3.975% plus a 90-165bp spread, midpoint 5.25%. NO QATARI NAME IN THIS BOOK HAS HAD ITS FACILITY NOTE READ — there are three covered Qatari instruments and no Qatari study at all — so this rests on no in-house sourced Kd and is the floor of last resort: the first Qatari study to reach the three-assert Kd gate replaces it with its own note. The range is set beside the UAE norm because the two sovereigns carry the same Aa2 rating and the same 0.42% rating spread.
- **real_rate_convention** — DERIVED, NEVER QUOTED. Under the peg the QAR real rate is the USD real rate: the FOMC's own longer-run median federal funds projection (3.1%, Summary of Economic Projections of 17 June 2026, FRED FEDTARMDLR) plus the ten-year term premium (0.8751%, Kim-Wright, FRED THREEFYTP10, 28 August 2026) less long-run US inflation (2.2%) = 1.9751%. The derived terminal QAR risk-free rate is 2.0% + 1.9751% = 3.9751% against the 5.26% synthetic ten-year above. NOTE WHAT THIS MEANS: the anchor is derived and the terminal is derived, so for Qatar alone NEITHER end of the risk-free construction rests on an observed local-currency government yield. That is a real weakness of this path and it is written here rather than discovered by whoever uses it.
- **erp_terminal** — A. Damodaran, 'Country Default Spreads and Risk Premiums', ctryprem, LAST UPDATED 5 JANUARY 2026, read live from the original file on 3 September 2026. Terminal equity risk premium held at the rating-basis Qatari ERP of 4.87%; no convergence is assumed for an Aa2 sovereign already priced at 47bp.

---

## IN — INR

Regime: **mature**. Inflation sits at the Reserve Bank of India's published 4 percent target and the call rate is near its own long-run level, so the glide has nothing to travel and cost_of_capital.py returns a FLAT schedule for any regime other than 'transition'. INDIA IS NOT A LOW-INFLATION ECONOMY AND THE REGIME LABEL DOES NOT SAY IT IS: 'mature' here means the policy rate is AT its long-run level, not that the level is low. The terminal inflation of 4% is double the pegged markets' and every escalator carries it.


### Inflation

| Year | Rate | Basis |
|---|---:|---|
| 2026 | 4.70% | IMF World Economic Outlook projection |
| 2027 | 4.00% | IMF World Economic Outlook projection |
| 2028 | 4.00% | IMF World Economic Outlook projection |
| 2029 | 4.00% | IMF World Economic Outlook projection |
| 2030 | 4.00% | IMF World Economic Outlook projection |
| terminal | 4.00% | the target band midpoint in force |

Latest print: **2.10%** (2025, annual average consumer prices). Target: **4.0% ± 2.0pp**, long run.


### Rates

| | Value | As of |
|---|---:|---|
| Policy rate | 5.50% | 2026-06-01 |
| Sovereign 10-year | 6.89% | 2026-06-01 |
| Default spread, rating basis | 1.87% | |
| Default spread, market basis | 0.66% | |
| Terminal cost of debt | 8.00% | long-run corporate norm |
| Terminal equity risk premium | 7.08% | normalised |

**Policy-rate path** (the SHAPE input for the cost-of-capital glide, never a second free parameter): 5.50% → 5.50% → 5.50% → 5.50% → 5.50%


### The derived terminal

Nothing in this block is a quote. Each line is an identity on the numbers above, because a terminal rate reverse-engineered from a price is the quietest lever there is.

| | Identity | Value |
|---|---|---:|
| Terminal risk-free | terminal inflation + real-rate convention (1.98%) | **5.98%** |
| Terminal growth, zero real | terminal inflation + stated real growth (0.00%) | **4.00%** |

### The currency, derived

Relative purchasing-power parity on this path's own inflation against long-run United States inflation of 2.20%. A study may not set this by hand.

| Year | Depreciation | USD/INR |
|---|---:|---:|
| 2026 | 2.45% | 89.29 |
| 2027 | 1.76% | 90.86 |
| 2028 | 1.76% | 92.46 |
| 2029 | 1.76% | 94.09 |
| 2030 | 1.76% | 95.75 |

### Sources

- **inflation.latest** — International Monetary Fund, World Economic Outlook database, series PCPIPCH (inflation, average consumer prices, annual percent change), India (IND), read live from the IMF datamapper API on 3 September 2026.
- **inflation.path** — International Monetary Fund, World Economic Outlook database, series PCPIPCH (inflation, average consumer prices, annual percent change), India (IND), read live from the IMF datamapper API on 3 September 2026. The series runs to 2031 and prints 4.0% flat from 2027 onward; no step here is interpolated. The 2025 print of 2.1% is an unusually low actual against a 4% target and the IMF's own 2026 projection of 4.7% is a rebound to and through it — recorded rather than smoothed.
- **inflation.target** — The Reserve Bank of India's published flexible inflation target: 4 percent on the consumer price index with a tolerance band of +/- 2 percentage points. An EXPLICIT target with an EXPLICIT band, which is why the band here is the central bank's own rather than a dispersion computed from projections as in the pegged markets.
- **inflation.terminal** — The Reserve Bank's target midpoint, which is also the IMF's own published figure for 2027 through 2031.
- **policy_rate** — Federal Reserve Economic Data (FRED), series IRSTCI01INM156N (immediate rates, call money / interbank rate), 5.50% for June 2026, read live 3 September 2026.
- **policy_rate.path** — FLAT AT THE OBSERVED CALL RATE. The regime is 'mature', so the glide's scope is nil and a shaped path would do no work while implying a rate call nothing here sources. The Reserve Bank publishes no forward rate path; inventing a glide to fill the field would be the free parameter the promotion rule forbids.
- **sovereign** — Federal Reserve Economic Data (FRED), series INDIRLTLT01STM (long-term government bond yields, 10-year), 6.89% for June 2026, read live 3 September 2026.
- **sovereign.spreads** — A. Damodaran, 'Country Default Spreads and Risk Premiums', ctryprem, LAST UPDATED 5 JANUARY 2026, read live from the original file on 3 September 2026. India row: Moody's Baa3; adjusted default spread 1.87% (rating basis); credit-default-swap spread 0.66% (market basis); country risk premium 2.85%; total ERP 7.08% on the rating basis and 5.23% on the CDS basis. THE TWO BASES DIVERGE FAR MORE HERE THAN IN ANY OTHER MARKET ON THIS BOOK — 121bp of spread and 185bp of ERP — because a Baa3 rating and a 66bp CDS are two quite different readings of the same sovereign. Which is central is a cost-of-capital decision and it MATTERS here in a way it does not for an Aa2 name; both are carried and a study must say which it used and why.
- **fx** — World Bank series PA.NUS.FCRF (official exchange rate, LCU per US$, period average), India, 2025 = 87.158, read live 3 September 2026.
- **fx.derivation** — The forward currency path is DERIVED from this path's own inflation ladder against long-run United States inflation by relative purchasing-power parity, never set by hand. On a 4.0% domestic terminal against a 2.2% foreign one the rupee depreciates about 1.8% a year in the long run, and a study that escalates rupee costs at 4% while holding the currency still is running two views of one economy [L-048].
- **us_inflation_lt** — Long-run United States CPI inflation 2.2%, the IMF's own published figure for 2029-2031, the foreign leg of the purchasing-power parity relation.
- **cost_of_debt_norm** — The long-run Indian investment-grade corporate borrowing norm, taken as the derived terminal risk-free rate of 5.975% plus a 150-250bp spread, midpoint 8.00%. NO INDIAN NAME IN THIS BOOK HAS HAD ITS FACILITY NOTE READ, so this rests on no in-house sourced Kd and is the floor of last resort: the first Indian study to reach the three-assert Kd gate replaces it with its own note.
- **real_rate_convention** — DERIVED, NEVER QUOTED. the FOMC's own longer-run median federal funds projection (3.1%, Summary of Economic Projections of 17 June 2026, FRED FEDTARMDLR) plus the ten-year term premium (0.8751%, Kim-Wright, FRED THREEFYTP10, 28 August 2026) less long-run US inflation (2.2%) = 1.9751%. THE COMMON-REAL-RATE ASSUMPTION IS WEAKER HERE THAN IN KOREA AND IT IS SAID SO: India's observed ten-year of 6.89% less a 4.0% terminal inflation is a 2.89% real rate, 91bp ABOVE this convention, against Korea's 21bp. The gap is what a partially open capital account and a Baa3 rating look like, so the derived terminal INR risk-free of 4.0% + 1.9751% = 5.9751% sits about 92bp below the live ten-year. That is a real normalisation rather than a rounding, and the first Indian study to use this path should say whether it accepts it.
- **erp_terminal** — A. Damodaran, 'Country Default Spreads and Risk Premiums', ctryprem, LAST UPDATED 5 JANUARY 2026, read live from the original file on 3 September 2026. Terminal equity risk premium held at the RATING-basis Indian ERP of 7.08%, the more conservative of the two bases, and NOT converged: a Baa3 sovereign's country premium narrowing is a house view about a rating upgrade and nothing here sources one.

---

## KR — KRW

Regime: **mature**. Inflation is at the Bank of Korea's published 2 percent target and the call rate sits near its own long-run level, so the cost-of-capital glide has nothing to travel and cost_of_capital.py returns a FLAT schedule for any regime other than 'transition'. The won floats, so unlike the pegged markets the CURRENCY path is derived rather than fixed.


### Inflation

| Year | Rate | Basis |
|---|---:|---|
| 2026 | 2.50% | IMF World Economic Outlook projection |
| 2027 | 1.90% | IMF World Economic Outlook projection |
| 2028 | 2.00% | IMF World Economic Outlook projection |
| 2029 | 2.00% | IMF World Economic Outlook projection |
| 2030 | 2.00% | IMF World Economic Outlook projection |
| terminal | 2.00% | the target band midpoint in force |

Latest print: **2.10%** (2025, annual average consumer prices). Target: **2.0% ± 0.5pp**, long run.


### Rates

| | Value | As of |
|---|---:|---|
| Policy rate | 2.54% | 2026-06-01 |
| Sovereign 10-year | 4.18% | 2026-06-01 |
| Default spread, rating basis | 0.42% | |
| Default spread, market basis | 0.20% | |
| Terminal cost of debt | 4.50% | long-run corporate norm |
| Terminal equity risk premium | 4.87% | normalised |

**Policy-rate path** (the SHAPE input for the cost-of-capital glide, never a second free parameter): 2.54% → 2.54% → 2.54% → 2.54% → 2.54%


### The derived terminal

Nothing in this block is a quote. Each line is an identity on the numbers above, because a terminal rate reverse-engineered from a price is the quietest lever there is.

| | Identity | Value |
|---|---|---:|
| Terminal risk-free | terminal inflation + real-rate convention (1.98%) | **3.98%** |
| Terminal growth, zero real | terminal inflation + stated real growth (0.00%) | **2.00%** |

### The currency, derived

Relative purchasing-power parity on this path's own inflation against long-run United States inflation of 2.20%. A study may not set this by hand.

| Year | Depreciation | USD/KRW |
|---|---:|---:|
| 2026 | 0.29% | 1426.62 |
| 2027 | -0.29% | 1422.43 |
| 2028 | -0.20% | 1419.64 |
| 2029 | -0.20% | 1416.87 |
| 2030 | -0.20% | 1414.09 |

### Sources

- **inflation.latest** — International Monetary Fund, World Economic Outlook database, series PCPIPCH (inflation, average consumer prices, annual percent change), Korea (KOR), read live from the IMF datamapper API on 3 September 2026.
- **inflation.path** — International Monetary Fund, World Economic Outlook database, series PCPIPCH (inflation, average consumer prices, annual percent change), Korea (KOR), read live from the IMF datamapper API on 3 September 2026. The series runs to 2031 and prints 2.0% flat from 2028 onward; no step here is interpolated.
- **inflation.target** — The Bank of Korea's published inflation target, 2 percent on the consumer price index — an EXPLICIT target set by the central bank, unlike the pegged markets where the anchor has to be imported. The 0.5pp band is the dispersion of the IMF's own published Korean projections about it over 2026-2031 (2.5%, then 1.9%, then 2.0% held).
- **inflation.terminal** — The Bank of Korea's 2 percent target, which is also the IMF's own published figure for 2028 through 2031 — the two agree, which is a coherence check rather than a second assumption.
- **policy_rate** — Federal Reserve Economic Data (FRED), series IRSTCI01KRM156N (immediate rates, call money / interbank rate) 2.537% and IR3TIB01KRM156N (3-month interbank) 2.91%, both June 2026, read live 3 September 2026.
- **policy_rate.path** — FLAT AT THE OBSERVED CALL RATE, and that is a statement rather than a placeholder: this market's regime is 'mature', so the glide's scope is nil and a shaped path would do no work while implying a rate call nothing here sources. The Bank of Korea publishes no dot plot; inventing a glide to fill the field would be the free parameter the promotion rule forbids.
- **sovereign** — Federal Reserve Economic Data (FRED), series IRLTLT01KRM156N (long-term government bond yields, 10-year), 4.181% for June 2026, read live 3 September 2026.
- **sovereign.spreads** — A. Damodaran, 'Country Default Spreads and Risk Premiums', ctryprem, LAST UPDATED 5 JANUARY 2026, read live from the original file on 3 September 2026. Korea row: Moody's Aa2; adjusted default spread 0.42% (rating basis); credit-default-swap spread 0.20% (market basis); country risk premium 0.64%; total ERP 4.87% on the rating basis and 4.53% on the CDS basis.
- **fx** — World Bank series PA.NUS.FCRF (official exchange rate, LCU per US$, period average), Korea, 2025 = 1422.44, read live 3 September 2026.
- **fx.derivation** — The forward currency path is DERIVED from this path's own inflation ladder against long-run United States inflation by relative purchasing-power parity, never set by hand. A study that escalates costs at domestic inflation while holding the currency still is running two views of one economy [L-048].
- **us_inflation_lt** — Long-run United States CPI inflation 2.2%, the IMF's own published figure for 2029-2031, the foreign leg of the purchasing-power parity relation.
- **cost_of_debt_norm** — The long-run Korean investment-grade corporate borrowing norm, taken as the derived terminal risk-free rate of 3.975% plus a 25-90bp spread, midpoint 4.50%. NO KOREAN NAME IN THIS BOOK HAS HAD ITS FACILITY NOTE READ, so this rests on no in-house sourced Kd and is the floor of last resort: the first Korean study to reach the three-assert Kd gate replaces it with its own note.
- **real_rate_convention** — DERIVED, NEVER QUOTED. the FOMC's own longer-run median federal funds projection (3.1%, Summary of Economic Projections of 17 June 2026, FRED FEDTARMDLR) plus the ten-year term premium (0.8751%, Kim-Wright, FRED THREEFYTP10, 28 August 2026) less long-run US inflation (2.2%) = 1.9751%. THE UNITED STATES REAL RATE IS USED FOR A FLOATING CURRENCY AND THAT IS AN ASSUMPTION, NOT AN IDENTITY: it says the long-run real rate is common across open capital markets, which is the textbook position and is what the observed Korean curve supports here — 4.181% nominal less 2.0% terminal inflation is a 2.18% real rate, 21bp from this convention. That agreement is a cross-check, not the source. The derived terminal KRW risk-free rate is 2.0% + 1.9751% = 3.9751% against a live 4.181%.
- **erp_terminal** — A. Damodaran, 'Country Default Spreads and Risk Premiums', ctryprem, LAST UPDATED 5 JANUARY 2026, read live from the original file on 3 September 2026. Terminal equity risk premium held at the rating-basis Korean ERP of 4.87%; no convergence is assumed for an Aa2 sovereign.

---

## US — USD

Regime: **mature**. The policy rate sits near its own published long-run level — 3.75% target upper against an FOMC longer-run median of 3.1% — so the cost-of-capital glide has essentially nothing to travel and cost_of_capital.py returns a FLAT schedule for any regime other than 'transition'. This is the reference economy the pegged paths import.


### Inflation

| Year | Rate | Basis |
|---|---:|---|
| 2026 | 3.20% | IMF World Economic Outlook projection |
| 2027 | 2.10% | IMF World Economic Outlook projection |
| 2028 | 2.20% | IMF World Economic Outlook projection |
| 2029 | 2.20% | IMF World Economic Outlook projection |
| 2030 | 2.20% | IMF World Economic Outlook projection |
| terminal | 2.20% | the target band midpoint in force |

Latest print: **2.70%** (2025, annual average consumer prices). Target: **2.2% ± 0.3pp**, long run.


### Rates

| | Value | As of |
|---|---:|---|
| Policy rate | 3.75% | 2026-09-03 |
| Sovereign 10-year | 4.79% | 2026-09-02 |
| Default spread, rating basis | 0.23% | |
| Default spread, market basis | 0.30% | |
| Terminal cost of debt | 5.70% | long-run corporate norm |
| Terminal equity risk premium | 4.46% | normalised |

**Policy-rate path** (the SHAPE input for the cost-of-capital glide, never a second free parameter): 3.75% → 3.45% → 3.25% → 3.10% → 3.10%


### The derived terminal

Nothing in this block is a quote. Each line is an identity on the numbers above, because a terminal rate reverse-engineered from a price is the quietest lever there is.

| | Identity | Value |
|---|---|---:|
| Terminal risk-free | terminal inflation + real-rate convention (1.98%) | **4.18%** |
| Terminal growth, zero real | terminal inflation + stated real growth (0.00%) | **2.20%** |

### The currency, derived

Relative purchasing-power parity on this path's own inflation against long-run United States inflation of 2.20%. A study may not set this by hand.

| Year | Depreciation | USD/USD |
|---|---:|---:|
| 2026 | 0.00% | 1.00 |
| 2027 | 0.00% | 1.00 |
| 2028 | 0.00% | 1.00 |
| 2029 | 0.00% | 1.00 |
| 2030 | 0.00% | 1.00 |

### Sources

- **inflation.latest** — International Monetary Fund, World Economic Outlook database, series PCPIPCH (inflation, average consumer prices, annual percent change), United States (USA), read live from the IMF datamapper API on 3 September 2026.
- **inflation.path** — International Monetary Fund, World Economic Outlook database, series PCPIPCH (inflation, average consumer prices, annual percent change), United States (USA), read live from the IMF datamapper API on 3 September 2026. The series runs to 2031 and prints 2.2% flat from 2028 onward, so NO STEP HERE IS INTERPOLATED.
- **inflation.target** — THE FEDERAL RESERVE'S 2 PERCENT OBJECTIVE IS ON THE PCE BASIS AND THIS LADDER IS CPI, WHICH IS NOT THE SAME INDEX. CPI has run persistently above PCE, so a CPI terminal of 2.2% against a 2.0% PCE objective is the coherent pairing rather than a 20bp house view; the 0.3pp band is the dispersion of the IMF's own published US CPI projections about it over 2027-2031. Stating the basis is the point: a target quoted on one index against a ladder built on another is two views of one economy.
- **inflation.terminal** — The IMF's own published United States CPI figure for 2028 through 2031, held.
- **policy_rate** — Federal Reserve Economic Data (FRED), series DFEDTARU (target range upper limit) 3.75% and DFF (effective federal funds rate) 3.63%, read live 3 September 2026.
- **policy_rate.path** — A glide from the live 3.75% target upper limit to the FOMC's own longer-run median of 3.1% (SEP, 17 June 2026, FRED FEDTARMDLR), reached by 2029 and held. Both endpoints published; the two years between are a straight line and are the only interpolated figures here.
- **sovereign** — Federal Reserve Economic Data (FRED), series DGS10 (10-year Treasury constant maturity), 4.79% on 2 September 2026, read live 3 September 2026.
- **sovereign.spreads** — A. Damodaran, 'Country Default Spreads and Risk Premiums', ctryprem, LAST UPDATED 5 JANUARY 2026, read live from the original file on 3 September 2026. United States row: Moody's Aa1; adjusted default spread 0.23% (rating basis); credit-default-swap spread 0.30% (market basis); total equity risk premium 4.46% on the rating basis and 4.69% on the CDS basis. THE UNITED STATES CARRIES A NON-ZERO DEFAULT SPREAD IN THIS FILE and that is not an error: the source explains that the Moody's downgrade means the USD risk-free rate is the Treasury yield MINUS the US default spread, so the normalisation applies here exactly as it does to an emerging sovereign.
- **fx** — The domestic currency of this path IS the dollar; there is no pair to quote.
- **fx.derivation** — No currency path. Relative purchasing-power parity here would be the dollar against itself, and depreciation_path() is not consulted for a market whose own currency is the numeraire.
- **us_inflation_lt** — Long-run United States CPI inflation 2.2%, the IMF's own published figure for 2029-2031 — for this path it is the DOMESTIC terminal, and it is carried under this name because every other path measures its own currency against it.
- **cost_of_debt_norm** — The long-run United States investment-grade corporate borrowing norm, taken as the derived terminal risk-free rate of 4.175% plus a 130-200bp investment-grade spread, midpoint 5.70%. NO US NAME IN THIS BOOK HAS YET HAD ITS FACILITY NOTE READ, so unlike the AE and SA norms this one rests on no in-house sourced Kd at all and is the floor of last resort in the strictest sense: the first US study to reach the three-assert Kd gate replaces it with its own note.
- **real_rate_convention** — DERIVED, NEVER QUOTED. The long-run United States real ten-year rate = the FOMC's own longer-run median federal funds projection (3.1%, Summary of Economic Projections of 17 June 2026, FRED FEDTARMDLR) plus the ten-year term premium (0.8751%, Kim-Wright, FRED THREEFYTP10, 28 August 2026) less long-run US inflation (2.2%, IMF WEO above) = 1.9751%. CROSS-CHECK, NOT AN INPUT: the observed ten-year TIPS real yield is 2.45% (FRED DFII10, 2 September 2026), a spot price carrying today's cyclical position, 48bp above this long-run construction. The derived terminal USD risk-free rate is 2.2% + 1.9751% = 4.175% against a live 4.79% ten-year: a mild normalisation, not a rate call.
- **erp_terminal** — A. Damodaran, 'Country Default Spreads and Risk Premiums', ctryprem, LAST UPDATED 5 JANUARY 2026, read live from the original file on 3 September 2026. Terminal equity risk premium held at the rating-basis United States ERP of 4.46%; there is no country premium to converge.

---


## The rules these tables serve

- **One economy, one inflation.** Every growth rate in a model is stored as a real rate against a path id and recomputes to its nominal; a typed nominal rate is unfalsifiable and is refused. [L-048]
- **Terminal growth agrees with the inflation inside the terminal discount rate.** Growth below it is a perpetual real decline, which may be assumed but must be stated as the real number it is. [L-055]
- **The terminal risk-free rate is derived, never quoted.**
- **The explicit window runs until growth has converged on terminal** (within 2pp), so the terminal does not capitalise a rate the model never reached.
- **A sovereign quote older than 14 days is re-sourced before a strike.**

Enforced from outside by `scripts/check_macro_coherence.py`, negative-controlled by `scripts/check_macro_coherence_negative_control.py`, both in CI. [R-MACRO-01], [R-ENF-01]
