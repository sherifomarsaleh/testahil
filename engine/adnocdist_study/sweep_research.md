# ADNOC Distribution (ADX: ADNOCDIST) — Step 2A Information Sweep, external rings

**Valuation date:** 09-Aug-2026 · **Currency:** AED · **Access date:** 09-Aug-2026
**Structured register:** `sweep_research.json` — 55 entries (9 GLOBAL / 20 COUNTRY / 15 INDUSTRY / 11 COMPANY), 16 classified Critical, 23 Driver, 13 Supporting, 3 Background, plus 10 recorded gaps and negative results.

> **SIGCM note.** COMPANY-ring entries here are **secondary context only**. The company's reported historicals (IS / BS / CF) must be constructed from ADNOC Distribution's own audited filings. Nothing in this file may be used as a source of the subject's reported numbers.

---

## The five things that matter most

1. **This is a regulated pass-through business with a guaranteed margin floor, not a commodity retailer.** UAE retail fuel prices are set monthly by a government Fuel Price Committee (on which the ADNOC Distribution CEO sits) as average global prices plus operating costs. On top of that, the ADNOC parent supply agreement guarantees a **minimum ~45 fils/litre margin with no upper limit**, and cash-settles inventory losses quarterly when prices fall. This bounds the downside and is the strongest argument for a lower cost of capital than commodity peers carry.
2. **2026 is a geopolitical price shock, not a cycle.** The Iran conflict and Strait of Hormuz crisis drove Brent from ~USD 63 to ~USD 126 and back to USD 83.55. UAE Special 95 went AED 2.33 (Feb) → AED 3.83 (Jun) → AED 3.49 (Aug), +64% peak-to-trough.
3. **H1-2026 revenue growth is price, not volume.** Revenue +29%, volumes **+1.6%**. Headline EBITDA +39%, but **underlying EBITDA ex-inventory only +14%** — roughly USD 183m of H1 EBITDA is inventory gain that reverses when prices fall.
4. **The EIA forecasts crude back to USD 70 by 4Q26 and USD 65 in 2027.** The market agrees: forward P/E (16.8x) sits *above* trailing (14.3x). The Board is paying the USD 700m dividend floor, not 75% of the spiked profit. Three independent signals say normalise, don't capitalise the peak.
5. **A USD 1bn acquisition closes inside the forecast window.** Shell Downstream South Africa (~580 stations, +55% network, +20% volumes) signed 07-Jul-2026, closing 2027.

---

## 1. Risk-free rate — the anchor

| Instrument | Yield | Date | Note |
|---|---|---|---|
| **UAE federal AED T-Bond, Jan-2031 (~4.5y)** | **4.48%** | 30-Jul-2026 | **Primary anchor.** +4bp over comparable UST |
| UAE federal AED T-Sukuk, Oct-2027 | 4.49% | 30-Jul-2026 | +24bp over UST |
| Same Jan-2031 bond, May-2026 auction | 4.30% | 23-May-2026 | Curve rising through 2026 |
| Abu Dhabi sovereign USD 10Y | 4.73% at issue, **+25bp over UST** | Feb-2026 | Level stale; **spread** is the durable quantity |
| US 10Y Treasury | 4.68% | 08-Aug-2026 | Backbone via the AED/USD peg |
| CBUAE Base Rate (ODF) | 3.65% | held 29-Jul-2026 | Policy floor, not the DCF rf |
| US Fed funds target | 3.50–3.75% | held 29-Jul-2026 | **3 dissents for a HIKE**; Sept hike priced |

**Recommended anchor:** the AED federal T-Bond at **4.48%**, normalised under the v2 method to **rf\* = 4.48% − 0.42% = 4.06%**, with country risk entering *once* via the CRP inside the ERP.

**Tenor gap (flagged):** the UAE has issued **no 10-year AED T-bond**. The longest AED federal point is ~4.5 years. A 10-year point must be *constructed* — Abu Dhabi's +25bp USD spread on today's UST 10Y gives ~4.93% — and must be disclosed as a construction, never as an observed yield.

Sources: [MoF/WAM July-2026 auction](https://www.wam.ae/en/article/c1hd5hx-treasury-sukuk-bonds-auctions-attract-aed) · [MoF May-2026 auction](https://mof.gov.ae/en/news/uae-successfully-concludes-may-2026-treasury-bond-auction/) · [Zawya, Abu Dhabi dual-tranche](https://www.zawya.com/en/capital-markets/bonds/abu-dhabi-raises-3bln-as-investor-demand-drives-tight-spreads-on-dual-tranche-bond-yiw9i6l9) · [CBUAE Base Rate](https://www.centralbank.ae/media/kc0p2tuf/cbuae-maintains-the-base-rate-at-3-65-en.pdf) · [FOMC 29-Jul-2026](https://www.federalreserve.gov/newsevents/pressreleases/monetary20260729a.htm)

---

## 2. Damodaran — the UAE row, read live from the original file

Read from `pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html`. Header reads verbatim: **"Last updated: January 5, 2026"**.

| Entity | Moody's | Adj. default spread | CRP | **ERP** |
|---|---|---|---|---|
| **United Arab Emirates** | **Aa2** | **0.42%** | **0.64%** | **4.87%** |
| **Abu Dhabi** (separate row, identical) | Aa2 | 0.42% | 0.64% | 4.87% |
| Ras Al Khaimah (Emirate of) | A3 | 1.02% | 1.55% | 5.78% |
| Sharjah | Ba1 | 2.13% | 3.24% | 7.47% |
| United States | — | 0.23% | — | 4.46% |

Implied **mature-market ERP = 4.46% − 0.23% = 4.23%**.

The Abu Dhabi row being identical to the UAE row means no emirate-level adjustment is warranted for an Abu Dhabi-domiciled issuer — but note "UAE" is not one risk block: Sharjah carries a 7.47% ERP.

**⚠️ Vintage discrepancy (flagged, C-13).** A Damodaran **July-2026 update exists** (published 03-Jul-2026: mature-market ERP 4.17%, US ERP 4.45%, equity volatility multiplier 1.5545, 157 markets) — but the **canonical HTML file has not been refreshed** and still reads January 2026. The July UAE row could **not** be verified from the original file. A third-party figure (ERP 4.99% / CRP 0.66% / spread 0.49%) was found, **contradicts** the original file, and **must not be used**. Either source `ctryprem.xlsx` directly, or use the January row and disclose the vintage — and show the ERP choice as a stated sensitivity.

Sovereign ratings all current and all in the AA band: **Moody's Aa2 stable** (12-Jun-2026) · **S&P AA/A-1+ stable** (06-Mar-2026) · **Fitch AA− stable** (23-May-2026).

---

## 3. UAE fuel pricing — mechanism and levels

### Mechanism (in force since 1 August 2015, unchanged)
- Prices **deregulated** 01-Aug-2015; a pricing policy **linked to global prices** was adopted.
- A **Fuel Price Committee** — chaired by the Undersecretary of the Ministry of Energy, with the Undersecretary of the Ministry of Finance, **the CEO of ADNOC Distribution** and the CEO of ENOC as members — reviews prices against average international levels each month.
- On the **28th of each month** it announces the following month's prices: **average global prices plus operating costs**, evaluating benchmark crude, **international refining margins** and domestic operating costs per grade.
- Explicitly designed so distributors "make reasonable profits and limit their losses"; deliberately not tied to a single global market.
- **Prices are uniform nationally and across all retailers** — there is no price competition in UAE fuel retail. Share is won on network and convenience.

### Levels (AED/litre)

| 2026 | Super 98 | Special 95 | E-Plus 91 | Diesel |
|---|---|---|---|---|
| Jan | 2.53 | 2.42 | 2.34 | 2.55 |
| Feb | 2.45 | **2.33** | 2.26 | 2.52 |
| Mar | 2.59 | 2.48 | 2.40 | 2.72 |
| Apr | 3.39 | 3.28 | 3.20 | **4.69** |
| May | 3.66 | 3.55 | 3.48 | 4.69 |
| Jun | 3.95 | **3.83** | 3.76 | 4.33 |
| Jul | 3.40 | 3.29 | 3.21 | 3.60 |
| **Aug (current)** | **3.60** | **3.49** | **3.41** | **3.80** |

August prices announced 31-Jul-2026, effective 01-Aug-2026; every grade +AED 0.20 on July. Special 95 rose **+64%** from the February low to the June peak; retail prices surged **>60%** from late February. Diesel spiked hardest (+86% Feb→Apr), consistent with record global diesel cracks.

**Pre-shock normal:** 2025 Special 95 traded in a tight **AED 2.46–2.77** band all year (2024: 2.50–3.22). That ~AED 2.60 mid-cycle level is the honest anchor for the normalised-earnings lens and the terminal year, against AED 3.49 today.

*Caution: the 2026 monthly series is from a compiled tracker, not the Ministry's own publication — spot-check before fixing as a driver, especially the Apr–May diesel figure of 4.69. The 2025 monthly series is incomplete (5 months located).*

Sources: [UAE Government Portal — deregulation](https://u.ae/en/information-and-services/environment-and-energy/water-and-energy/energy-and-fuel-prices/deregulation-of-fuel-prices) · [UAE Cabinet, 2015](https://uaecabinet.ae/en/news/fuel-prices-to-be-deregulated-with-effect-from-1-august-2015) · [Khaleej Times, Aug-2026](https://www.khaleejtimes.com/business/energy/uae-petrol-diesel-prices-august-2026-announced) · [OneClickDrive 2026 tracker](https://blog.oneclickdrive.com/uae-petrol-prices-2026-tracker/)

---

## 4. Peer multiples — all as of 09-Aug-2026

| Company | Ticker | Mkt cap | EV | P/E | Fwd P/E | **EV/EBITDA** | Div yld | ROIC | Margin | Role |
|---|---|---|---|---|---|---|---|---|---|---|
| **ADNOC Distribution** | ADX:ADNOCDIST | AED 50.86bn | AED 55.74bn | 14.27 | 16.83 | **10.93** | 5.05% | 50.74% | 8.73% | **subject** |
| Aldrees Petroleum | Tadawul:4200 | SAR 11.97bn | SAR 16.49bn | 26.13 | 22.79 | **12.89** | 1.67% | 9.93% | 1.64% | **closest peer** |
| SASCO | Tadawul:4050 | SAR 2.66bn | SAR 7.27bn | 73.32 | 70.93 | 12.28 | n/a | 2.39% | 0.30% | cross-check (exclude P/E) |
| Couche-Tard | TSX:ATD | CAD 85.65bn | CAD 104.17bn | 20.23 | 20.19 | 10.66 | 0.92% | 11.93% | 4.11% | cross-check |
| Casey's General Stores | NASDAQ:CASY | USD 30.86bn | USD 33.24bn | 43.53 | 39.11 | 22.41 | 0.31% | 12.61% | 4.07% | cross-check |
| Murphy USA | NYSE:MUSA | USD 9.56bn | USD 12.12bn | 15.88 | 17.22 | 10.03 | 0.49% | 21.77% | 3.23% | cross-check |
| OMV Petrom | BVB:SNP | RON 79.14bn | RON 75.63bn | 28.56 | 14.61 | 9.91 | 6.13% | 8.09% | 7.07% | cross-check (integrated) |
| Vibra Energia | B3:VBBR3 | BRL 40.82bn | BRL 59.81bn | 13.79 | 6.34 | 7.70 | 4.30% | 13.69% | 1.56% | cross-check (EM floor) |
| Ultrapar (ADR) | NYSE:UGP | USD 6.56bn | USD 9.71bn | 11.43 | 8.29 | 6.80 | 3.41% | 12.85% | 2.06% | cross-check (EM floor) |

All from StockAnalysis.com, same-day. **Only Aldrees is a genuine like-for-like comparable** (GCC fuel retail, same regulated-price structure, same Saudi market); everything else is labelled cross-check.

**Reading:** the peer band runs **6.8x to 22.4x EV/EBITDA** — a 3x spread driven almost entirely by non-fuel mix and country risk. ADNOC Distribution at 10.93x sits below Aldrees (12.89x) despite ROIC of 50.7% vs 9.93% and margin of 8.73% vs 1.64%. A single blended peer median would be meaningless here; the relative lens must show the range and say which end applies and why.

**Not listed — recorded as negative results:** Jio-bp (unlisted Reliance 51% / BP 49% JV; the 2026 Reliance IPO is Jio Platforms, the telecom entity) and Puma Energy (Trafigura-controlled, debt markets only). Neither has traded equity multiples; neither enters the peer table.

---

## 5. UAE tax position

| Item | Position |
|---|---|
| Federal corporate tax | **9%** on taxable profit above AED 375,000 |
| Upstream extraction carve-out | Applies to ADNOC's **extraction** subsidiaries (emirate-level fiscal regime) — **does NOT cover ADNOC Distribution**, a downstream retailer |
| **DMTT (Pillar Two)** | **15%** minimum effective rate, effective for FYs beginning on/after **01-Jan-2025**, Cabinet Decision No. (142) of 2024; applies to MNE groups with **consolidated global revenue ≥ EUR 750m** |
| **Does DMTT apply?** | **Almost certainly yes.** ADNOC Group is far above the threshold; ADNOC Distribution alone reports ~AED 40.8bn TTM revenue |

**Practical conclusion:** the forecast tax rate should be built at **15%, not 9%** — a 6-point difference flowing straight through the FCFF waterfall. **This is not resolved by the sweep** and is a flag-before-issue item: read the tax note and DMTT disclosure from the audited FY2025 statements and H1-2026 interims. A secondary source reported an AED 183m tax charge but with an ambiguous period — **unusable**, and excluded.

Sources: [PwC Worldwide Tax Summaries — UAE](https://taxsummaries.pwc.com/united-arab-emirates/corporate/taxes-on-corporate-income) · [UAE MoF — Top-up Tax](https://mof.gov.ae/en/public-finance/tax/uae-domestic-minimum-top-up-tax/) · [EY Global Tax Alert](https://www.ey.com/en_gl/technical/tax-alerts/uae-issues-domestic-minimum-top-up-tax-legislation)

---

## 6. Global ring in brief

- **Brent USD 83.55** (07-Aug-2026, +25.5% y/y); **WTI USD 78.18**. 52-week WTI range USD 54.97 – 119.47.
- **2026 path:** Brent ~63 (Jan) → Iran war, +28% in a week (Mar) → peak ~126 (Apr) → below 70 (late Jun, Hormuz transits resume) → back above 100 (23-Jul) → 82–83 (early Aug).
- **EIA July-2026 STEO:** Brent **USD 74/bbl in 3Q26, USD 70 in 4Q26, USD 65 in 2027** (cut USD 15–19 from the June vintage). *STEO PDF was not machine-readable — figures via EIA-sourced secondary reporting; re-verify against the tables.*
- **Cracks at records:** NYMEX 3-2-1 hit **USD 64.58/bbl** on 08-Jul-2026; European diesel margins above USD 60/bbl after Russia halted diesel exports. Raises ADNOC Distribution's input cost *and* flows into the retail price via the Committee formula.
- **Global EV:** 25% of new car sales in 2025 (>20m units); IEA projects **28% in 2026** (23m units).
- **Non-fuel at global peers:** inside sales drive **70–78% of gross profit** on ~22% of revenue. ADNOC Distribution's USD 140m H1 non-fuel gross profit against USD 786m EBITDA is far below that — long runway, small near-term contribution.
- **Fed:** 3.50–3.75%, held 29-Jul-2026, **9-3 with three dissents for a hike**; September hike priced. UST 10Y 4.68%.

---

## 7. Country ring in brief (UAE)

- **GDP:** 2025 +4.8% (IMF; non-oil +4.6%) / +5.6% (World Bank; non-oil +6.1%) / +4.9% (CBUAE). 2026 forecast +5.0% IMF (hydrocarbon +6.3%, non-oil +4.6%), +5.6% CBUAE. *All predate the 2026 oil shock — flag the vintage. No 2027 official forecast located.*
- **Inflation:** 2025 averaged **1.3%**; Dec-2025 CPI +2.04% y/y. CBUAE forecasts **1.8% (2026)** and 2.0% (2027) — a forecast that predates the >60% fuel price surge and is likely superseded. Use for **domestic** cost lines only; per the cost-stack rule, product cost and globally-traded inputs escalate on their own commodity path, never on domestic CPI.
- **Vehicle parc:** 4.56m registered vehicles (Jun-2025), **+9.35% y/y** (+390k). New registrations 157k in H1-2025 (+11%). Dubai 3.5m daytime vehicles, +10% in two years. **Stale (Jun-2025)** — no 2026 update found.
- **⚠️ The volume tension:** parc **+9%** against company fuel volumes **+1.6%**. That gap must be resolved explicitly — a parc-based volume driver would materially overstate volumes.

---

## 8. Industry ring in brief

- **UAE structure:** ADNOC Distribution + ENOC + Emarat hold **~85% of retail volumes** (2025). ADNOC Distribution 977 stations at Q3-2025, all seven emirates; ENOC 198 (2024), including former EPPCO sites — **EPPCO is an ENOC brand, not a fourth competitor**; Emarat ~100 (Dubai and Northern Emirates). Market size USD 17.40bn (2026), 4.15% CAGR to 2031 (paid research — background only).
- **Saudi:** all petroleum activity requires Ministry of Energy licensing under the Petroleum and Petrochemical Materials Law, forcing consolidation of sub-scale independents — the structural opportunity behind the expansion. ADNOC Distribution at **231 Saudi sites (H1-2026, +65% y/y)**, ~70% capital-light DUCCO. *Target-date contradiction to resolve: earlier reporting said 300 by 2026; the H1-2026 call says 300 by 2029.* Listed Saudi peers: Aldrees, SASCO.
- **Egypt:** 50% of TotalEnergies Marketing Egypt acquired Feb-2023 for ~USD 186m (240 stations, 100+ convenience stores, wholesale/aviation/lubricants); expected +6% EBITDA from year 1. Adding ~6 stations/year. Management says performance exceeds the investment case and **"85–90% of the business is naturally protected against any EGP devaluation"** via USD-linked aviation and lubricants — a material, testable claim to verify against segment disclosure. Confirm from the filings whether Egypt is consolidated or equity-accounted.
- **UAE EV:** National EV Policy targets **~10% of the parc electric by 2030**, 50% by 2050; 42,000 government EVs by 2030. EV+PHEV was ~13% of new sales in 2023 (stale). **Model EV as a parc-share drag, never a new-sales-share drag** — over a 5-year horizon the UAE volume effect is low single digits; the real exposure is terminal value. Company guides 50–60 new charging points in 2026 and 10–15x fast/super-fast points by 2028 vs 2023.

---

## 9. Company ring — context only

| Item | Value |
|---|---|
| Share price / market cap | AED 4.070 (07-Aug-2026) / AED 50.86bn; EV AED 55.74bn |
| Shares / free float / parent | 12.50bn shares; **23% float** (31-Dec-2025, stale) → ADNOC ~77%; parent committed to ≥70% |
| H1-2026 | Net profit USD 568m (+59%, record); revenue +29%; **EBITDA USD 786m (+39%) but underlying ex-inventory USD 603m (+14%)**; ROCE 40% |
| Q2-2026 | Net profit USD 358m (+94%); revenue AED 13.2bn (+53%) |
| Volumes / network | **7.75bn litres (+1.6%)**; 1,045 stations (+11% y/y); UAE transactions >100m (+4.8%) |
| Non-fuel | Gross profit USD 140m H1-2026 (vs USD 67m H1-2021); Oasis >40% of non-fuel GP (was 20%) |
| Leverage / capex | Net debt/EBITDA **~0.7x**; FY2026 capex guidance **USD 250–300m**; FCF AED 3.74bn TTM |
| Dividend policy | **USD 700m p.a. (20.57 fils) or 75% of net profit, whichever higher, 2024–2030**; quarterly from 2026 |
| 2026 dividends | Q1 5.14 fils (paid Jun); Q2 5.14 fils / USD 175m (payable 01-Sep-2026) — **the floor, not 75% of the spiked profit** |
| **ADNOC supply agreement** | **~45 fils/litre guaranteed minimum margin, no cap**; quarterly cash-settled inventory backstop |
| Shell South Africa | ~USD 1bn EV, ~580 stations, signed 07-Jul-2026, closing 2027; +55% network, +20% volumes to 19.2bn litres; 6% EPS accretive yr 1, +13% EBITDA, USD 30–40m synergies in 5 yrs |
| Cost of debt evidence | Parent ADNOC Murban USD 1.5bn 10Y sukuk at **4.75%, +60bp over UST** (May-2025). No ADNOC Distribution-specific bond found; USD 2.25bn loan facilities reporting dates from 2022 |
| Sell-side (**cross-check only**) | 16 analysts, consensus Buy, target AED 4.63 (+13.8%) — *never a build input; this study issues ranges, not targets* |

### Modelling consequences flagged
- **Two-way valuation required (Shell SA):** value standalone ex-South Africa **and** pro-forma, side by side, never averaged.
- **Normalise, don't capitalise:** strip the ~USD 183m H1 inventory gain; the backstop cash-settles it back out as prices fall.
- **Bear case is bounded:** build the downside off 45 fils/litre × volume, not a proportional margin squeeze.
- **Beta caution:** a 23% float means thin trading — check the regression gate (n ≥ 24, R² ≥ 5%, SE(β) < |β|) against EGX-equivalent local index (ADX) rather than assuming a usable own-stock beta.
- **Kd:** parent's +60bp spread on the 4.48% AED sovereign implies ~5.0–5.2% AED Kd, comfortably above the sovereign as the rule requires — but the subsidiary's own stack and LC/FX split must come from the filings.

---

## 10. Gaps, negative results and staleness

### Must resolve before the build
| # | Item | Action |
|---|---|---|
| GAP-01 | Damodaran July-2026 UAE row unverified; original file is a Jan-2026 vintage | Source `ctryprem.xlsx` directly, or use the Jan row and disclose. Never use the unverified 4.99% figure |
| GAP-02 | **No 10-year AED risk-free point exists** | Construct from Abu Dhabi's +25bp USD spread and disclose as a construction |
| GAP-03 | ADNOC Distribution's own effective tax rate (9% vs 15% DMTT) | Read the tax note from the audited FY2025 statements — **stop-and-inform candidate** |
| GAP-05 | 45 fils/litre floor sourced only from secondary reporting | Confirm from the related-party/supply-agreement disclosure — it is the study's most consequential structural input |
| GAP-06 | Company debt stack, LC/FX split, marginal rate | Read from the filings per SIGCM clause 3 |

### Noted limitations
| # | Item |
|---|---|
| GAP-04 | 2025 monthly fuel price series incomplete (5 months); 2026 series from a compiled tracker, not the Ministry — spot-check, especially Apr–May diesel at 4.69 |
| GAP-07 | ENOC (2024) / Emarat (undated) station counts stale; UAE EV share of new sales is a 2023 vintage; vehicle parc is Jun-2025 |
| NEG-01 | Jio-bp and Puma Energy — **not listed**, no equity multiples exist |
| NEG-02 | EIA STEO PDF not machine-readable; Brent forecasts via EIA-sourced secondary reporting — re-verify |
| NEG-03 | Only the **2025** IMF Article IV located; the 2026–27 GDP forecasts predate the oil shock entirely |

### Staleness summary
**Current (< 6 months):** all peer multiples (same-day), Brent/WTI/UST (1–2 days), UAE fuel prices (8 days), AED T-bond auction (10 days), CBUAE and FOMC (11 days), H1-2026 results (4 days), all three sovereign ratings, UAE inflation (Mar-2026), EIA STEO (Jul-2026), IEA EV Outlook (May-2026).

**Stale (> 6 months) — flagged:** Damodaran ctryprem.html (05-Jan-2026, ~7 months) · Abu Dhabi USD 10Y *level* (Feb-2026; spread treated as current) · IMF UAE GDP (Oct-2025) · UAE vehicle parc (Jun-2025) · free float (31-Dec-2025) · ENOC/Emarat station counts (2024) · UAE EV sales share (2023) · ADNOC Distribution loan facilities (2022) · parent sukuk (May-2025, moderately stale).
