# RMDA (Rameda / Tenth of Ramadan Pharmaceuticals) — Stage-1 Research Pack
### Testahil pipeline shakedown · EGX · pharma operating-co · 12-Jul-2026

> **[SUPERSEDED IN PART — 8-Aug-2026]** Two things here are no longer current. (1) The lens in §0 is chosen "per the EAND operating-co exemplar", but EAND was removed from the reference layer on 08-Aug-2026 — the set is closed at SWDY (operating-co / model study), ADCB (bank) and ALPHADHABI (holdco), so an operating-co lens is now referenced to SWDY. (2) The §3 WACC stacks a CRP-loaded ERP on the RAW Egypt 10Y local government-bond yield, which is the v1 sovereign double-count: under the v2 cost-of-capital method rf must first be normalised by that sovereign's own default spread (rf* = local yield − Egypt's own default spread) before the CRP-loaded ERP is added, so every Ke and WACC figure in §3 is overstated and must be rebuilt before use. The rest of this document stands as the dated record of what was done at the time.

**Status:** P2 (data gate) and P3-Step 0 (calibration) COMPLETE; this is the P3 research leg (sweep + financials + WACC + lens) for your review before I build the model and documents. Figures below are provenance-labeled; the FCFF-waterfall line items still needed from audited FS are listed at the end.

---

## 0. Lens decision (flagged for your sign-off)
**Pharma operating company → single-entity 5-year FCFF DCF**, per the EAND operating-co exemplar. **No SOTP:** Rameda's "segments" are sales *channels* of one integrated generics business (2Q25: private/pharmacy 77%, tender/UMPA 9%, contract-manufacturing 8%, export 6%), not separable businesses. The **2025 product-portfolio acquisitions are modeled as a base-changer (B)** folded into the operating base — not a separate leg. Cross-check crux sensitized in real units (see §4). [RETIRED 8-Aug-2026 — see header: EAND is no longer a reference exemplar; the operating-co pattern is SWDY]

---

## 1. Step-2A Information Sweep Register (four rings; B=base-changer · S=structural · D=driver-unlock · C=color · NEG=negative search)

| Ring | Category | Cl. | Finding | Source | Date |
|---|---|---|---|---|---|
| 1 Global | Rates/USD | S | Fed 3.50–3.75%; EGP floating (not pegged) — global rates bind Egypt via the IMF program & carry, not a peg | market data | Jul-26 |
| 1 Global | Pharma inputs | S | API/excipient imports USD-priced → EGP devaluation is the key COGS risk; global generic pricing competitive | industry | Jul-26 |
| 2 Country | FX / devaluation | B | EGP floated Mar-2024 (~30→~48/USD); FY25 deck assumes fixed 51 EGP/USD, 25% inflation. Step-devaluation = the single nastiest margin scenario | CBE / co. guidance | Jul-26 |
| 2 Country | Policy rate | S | CBE main operation 19.50% (corridor 19.00/20.00); EGP 10Y govt bond 22.55% → the WACC rf and the interest burden that compresses NI | CBE / investing.com | 3-Jul-26 |
| 2 Country | Regulator (EDA) | S | Egyptian Drug Authority sets/【caps】pharma prices; price catch-up post-devaluation is regulated & lagged — the FY23 margin trough vs FY24/25 recovery | EDA context | Jul-26 |
| 3 Industry | Demand | C | Egyptian pharma structurally growing (population, chronic disease, volume); defensive demand | industry | Jul-26 |
| 3 Industry | Competition | C | Fragmented generics (EIPICO, EPICO, Amoun, Pharco, etc.); Rameda mid-tier by revenue | industry | Jul-26 |
| 4 Company | Base-changer (M&A) | B | 2025 acquisition of a 2-product CNS/pain portfolio; combined addressable market >EGP 1.3bn, 3Y CAGR >25%, accretive margins, profit contribution from 2H25. Purchase price NOT disclosed in the release | Rameda IR (Initiates-First-Acquisition-of-2025) | Jul-25 |
| 4 Company | Capital action | S | **Share-count discrepancy to resolve:** FY24 deck states 1,503,464,931 shares; a market-data aggregator implied ~2.0bn from stake %s. Official = 1,503.5mn used; confirm against FY25 FS | Rameda FY24 deck vs aggregator | Apr-25 |
| 4 Company | Ownership | D | Aquinox Pharma Holding 19.2%, Saudi Seventh Investment 11.1%, Kuwait Investment Co 10.1%, Old Mutual 3.5%, Evli 2.4%; free float ~41% (aggregator — for color, confirm against official disclosure) | MarketScreener | Jul-26 |
| 4 Company | Leverage | B | Net debt EGP 2.0bn (Jun-25) → **2.2bn (Dec-25)**; net debt/EBITDA ~1.9x, above the 1.0–1.5x guide — the source of NI compression | Rameda IR ER | Mar-26 |
| 4 Company | Dividend | D | FY25 dividend EGP 60mn (H1+H2 2026); target payout ~40% going forward → q ≈ 0.8% | Rameda FY25 ER | Mar-26 |
| 4 Company | Capex | D | "USD 0 growth-capex required" — plant invested for ~5yr → low capex, high FCFF conversion (maintenance-only) | Rameda 1H25 deck | Sep-25 |
| 4 Company | Guidance | D | FY25 guide: revenue EGP 4.2–4.5bn (+60–75%), GM 48–52%, EBITDA margin 30%+, NI growth +25–35% (ex-price-hikes, ex-M&A) | Rameda 1H25 deck | Sep-25 |

**Negative searches:** no USD-denominated debt facility found (treat debt ~100% EGP, pending FS); no rights issue / capital increase found post-FY24 (confirm against FY25 FS to close the share-count item).

---

## 2. Financials — 4-year history (provenance-labeled)

| EGP mn | FY2022 | FY2023 | FY2024 | FY2025 |
|---|---|---|---|---|
| Revenue | 796.3 | 1,418.6 | 2,769 | 4,096 |
| Gross profit | n/s | n/s | 1,284 | 1,982 |
| Gross margin | — | — | 46.4% | 48.4% |
| EBITDA | 120.3 | 189.5 | 807 | 1,166 |
| EBITDA margin | 15.1% | 13.4% | 29.1% | 28.5% |
| Net income | 64.7 | 134.0 | 402 | 313 |
| Net margin | 8.1% | 9.4% | 14.5% | 7.6% |
| Net debt | n/s | n/s | ~1.3bn (1.6x) | 2.2bn (~1.9x) |

*Sources:* FY22/23/24 — Rameda FY24 investor presentation (official IR); FY25 — Rameda 4Q/FY25 earnings release (**via ent.news filing mirror — to be re-sourced from the official IR URL to satisfy the provenance hard rule**). All figures cross-checked for internal consistency (revenue × margin = EBITDA ties). **These headline figures came through WebFetch's summarizer** and must be tied to the audited FS at the QC gate.

---

## 3. Bottom-up WACC (wacc_builder.py, house §3.5-G)

| Input | Value | Source |
|---|---|---|
| rf | 22.55% | Egypt 10Y local govt bond, investing.com 3-Jul-26 (cache, <60d fresh) | [RETIRED 8-Aug-2026 — see header: raw local yield, not normalised by Egypt's own default spread — v1 double-count]
| ERP (CDS, primary) | 9.41% | Damodaran original ctryprem.html, Egypt row |
| ERP (rating, alt) | 13.94% | same |
| Beta | 1.00 (provisional) | RMDA-vs-EGX30 regression not yet run; GBCO-style fallback pending EGX30 daily |
| Ke (CDS / rating) | 31.96% / 36.49% | rf + β×ERP | [RETIRED 8-Aug-2026 — see header: built on the un-normalised rf above]
| Kd pre-tax | 20.70% | CBE EGP lending rate (proxy; RMDA facility rates pending FS) |
| Kd after-tax (28%) | 14.90% | |
| Weights E / D | 77.4% / 22.6% | mcap 7,517 (5.00 × 1,503.5mn) vs net debt 2,200 (gross debt pending FS) |
| **WACC (CDS, primary)** | **28.10%** | | [RETIRED 8-Aug-2026 — see header: sovereign risk double-counted, rebuild under v2]
| **WACC (rating, alt)** | **31.60%** | | [RETIRED 8-Aug-2026 — see header: sovereign risk double-counted, rebuild under v2]

Both ERP-basis WACCs published per house rule. Terminal growth ~11.5% nominal EGP (GBCO house view, to be sensitized).

---

## 4. The crux to sensitize (real observable units)
**EBITDA rose +45% in FY25 but net income fell −22%** (402→313mn). Operating engine is strong (revenue +48%, GM expanding to 48%); the bottom line is being eaten by **interest on EGP 2.2bn net debt at ~20% rates**. The valuation therefore hinges on two observables: (a) the **CBE rate path** (every ~100bp ≈ EGP ~22mn pre-tax interest), and (b) **deleveraging speed** (net debt/EBITDA back toward the 1.0–1.5x guide). A step-devaluation is the tail risk (USD-priced inputs vs regulated EGP pricing).

---

## 5. Step 0 calibration (done, P3 engine leg)
Borrowed EG config (nu=4, width_cal=0.909; RMDA not yet in the panel), h=60, 22 windows: **CRPS skill +0.017, 90% CI [−0.007, +0.045] → PARITY**, coverage 0.50/0.82/0.91, PIT 0.539 — well-calibrated, centered. Live **T+60 fair-value cone off spot 5.00**: 3.95 / 4.74 / **5.21** / 5.74 / 6.91 (5/25/50/75/95); q≈0.8% (small dividend) barely shifts it.

---

## 6. Open provenance items — needed to finish the FCFF waterfall to grade
To build the full Revenue→EBITDA→D&A→EBIT→NOPAT→+D&A→−Capex→−ΔWC→FCFF→PV waterfall at provenance grade, I need from the **audited FY2025 (and FY2024) financial statements** (the line items WebFetch can't reliably transcribe): **D&A, capex, change in working capital** (cash-conversion-cycle ~215 days implies a large ΔWC drag), **interest expense, effective tax rate, gross debt & cash split, total equity**, and **share-count confirmation**. Same clean fix as the OHLC CSV: attach the audited FS (or the official FY25 ER + FS PDFs) and I complete the model + the 16-section Word / 16-sheet Excel to grade.
