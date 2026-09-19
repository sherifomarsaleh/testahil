# Forensic Audit — Egyptian Chemical Industries (KIMA), EGX: EGCH

**Subject of audit:** *Testahil* Independent Valuation Study dated 5 September 2026, the accompanying valuation workbook (16 sheets), and the 302-input bibliography and source register.
**Audit date:** 18 September 2026
**Auditor's method:** the model was rebuilt independently from the Assumptions sheet and re-executed; the company's own filings were then retrieved and read directly.

---

## Section A — Audit Scope

I rebuilt the model from the Assumptions sheet and reproduced the published answer to the last cell (EGP 4.0396 vs 4.04; PV explicit 3,842.7 vs 3,843; PV terminal 10,676.8 vs 10,677; stopped case 8.0388 vs 8.04).

**Audited:** the valuation study, the workbook (all formulas read and re-executed independently in Python), and the bibliography.

**Primary sources reached:** the company's own IR portal (kimaegypt.com → Mist), its filing index, and the full audited statements for the year to 30 June 2025 (48 pages, 16.7 MB, zero text layer — read off the rendered pixels), from which I verified notes 6, 14, 15, 16, 18, 20, 21, 22, 23, 24, 25, 26 and 28 and the statutory auditor's own report. EGX's company page is behind a bot challenge (confirmed: empty reply from server), exactly as the study states.

**Not checked:** the auditor's production and unit-cost table and the 1,025–1,771 m³/t gas range (I sampled ~10 of 48 pages and did not reach it); the three interim filings; the Damodaran Egypt row; the EGX30 beta regression; the 50,000-path simulation's own price history.

**Note on vintage:** the FY2025/26 annual exists on the portal but is dated **17 September 2026** — twelve days after the study. Its absence from the study is correct at the study's own information set.

---

## Section B — Fail Table

| # | Location | Item | Plane | Sev. | What the report says | What is correct (primary source, or recomputed) | Why it failed | Impact on fair value | Correct method |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Table 19 / Sensitivity sheet | The 5×5 export-price × terminal-rate grid | Constr. / Disc. | **TOTAL** | "each cell a full re-run of the model — the segment build, the waterfall, the terminal year and the bridge — not a multiplier applied to the central answer" | All **25 cells sit exactly EGP +0.95** above my re-run of the delivered model at the same inputs (offsets 0.945–0.954, the spread being 2dp rounding of the published cells). A grid of genuine re-runs cannot differ from the model by a constant. | The grid is a memory of a superseded model state | The grid implies a central of **~EGP 4.99**, not 4.04; the only cell equal to 4.04 is (17.0%, US$500), neither of which is a published input. Table 20's entire driver ranking is read off this grid | Re-run the grid, or label it as belonging to a prior edition |
| 2 | Table 14, §7 caveats, catalysts, bibliography Tables 11–12 | New complex nameplate | Constr. / Disc. | **TOTAL** | "Derived nameplate 264,000 t/yr — FLAGGED as derived: no filing states it… built from the ammonia design plate less the draw of urea at its own plate" | That construction gives **(438,000 − 574,875 × 0.61989) / 0.43 = 189,874 t/yr**. The 264,000 comes from 800 t/d × 330 d, sourced in the workbook and register to a **Tecnimont / Orascom EPC award** — i.e. a source, contradicting "no filing states it" three times over | The document states a construction that does not produce the number the model runs. The register carries **both** inputs (`anna_nameplate 189,863` and `anna_nameplate_disclosed_tpd 800`) and its judgements table still says "Not disclosed" | **−EGP 0.299 (−7.4%)** on the document's own stated construction | Publish one nameplate with one provenance |
| 3 | Table 11, Assumptions C33–C37 | Export-price escalator | Constr. | **TOTAL** | Table 11: "the export price on the commodity path"; §1.6: margins are pure outputs | The model holds **US$530 flat in nominal dollars** for five years and the terminal while every EGP cost escalates at full domestic inflation. That is a **−2.4%/yr real price forecast**, not the absence of one. Escalating at US inflation (flat in real terms — the no-forecast choice) gives **EGP 6.817** | Declaration vs practice; and it is the classic PASS-5 pattern — costs on the domestic index, price frozen, the manufactured margin decline then reported as a finding | **+EGP 2.78 (+68.8%)** at real-flat; **−EGP 6.70** at the study's own mid-cycle US$400 | One escalator per driver class; state the real price assumption |
| 4 | §1.3, bibliography `peer_ev_ebitda_high/low` | The 6.0×–9.9× "Egyptian industrial range" | Input / Constr. | **TOTAL** | "the range Egyptian fertilizer producers actually trade at"; register: "9.9 = the **median** of (Ezz Steel 4.35, MOPCO 5.92, Abu Qir ~8.2, EFIC 11.52, SKPC 17.61)" | Median of that set = **8.20**; mean = 9.52. **9.9 is neither.** The low of 6.0 sits *above* the two lowest observed. 3 of the 5 names are not fertilizer producers. Abu Qir's multiple rests on aggregator data (`stockanalysis.com`) plus an estimated D&A | Stated construction does not reproduce; and the study's own bibliography §4 bars aggregators as build sources. This is the **only lens above the traded price** | On a 6.0–8.2 band the central is **EGP 13.93**, below the price — the headline "one of them now reaches the traded price" fails | Build the band from the peers' own filed statements |
| 5 | Assumptions C143; register `an_conversion_cost_FY2425` | Project cash margin | Constr. | **TOTAL** | Register: "157.29 EGP/t… **ADDED 9 August 2026 to replace a flat 32% cash-margin assumption** — the company discloses what a tonne of this exact product costs to make, and the study was assuming a margin instead of using it" | The workbook **still runs the 32%** (C143). The 157.29 input appears nowhere in it. The disclosed cost table (AN at EGP 4,076/t incl. 0.43 t ammonia at EGP 9,114/t) implies **~68.5%** | A declared replacement that was never implemented | **+EGP 1.21 (+30.1%)** at 68.5%; +0.60 at 50% | Use the disclosed conversion cost, as the register says was done |
| 6 | §1.8 | Terminal risk-free rate | Disclosure | PARTIAL | "7.0% inflation **compounded with** a 5.5% real rate gives a normalised risk-free rate of 12.50%" | 1.07 × 1.055 − 1 = **12.885%**. The model adds (C113 = C111 + C112) | Says compounded, does additive | **−EGP 0.143 (−3.5%)** if the printed text were followed | Say "plus", or compound |
| 7 | Table 21 row 3; register `g_terminal` | Terminal growth 7% | Constr. | PARTIAL | Adopted 7% as "the central bank's medium-term inflation target"; register: "**A perpetuity takes the longest-horizon target there is**" | The CBE's longest-horizon target is **5% (Q4 2028)**; 7% is Q4 2026. The correction note argues the rule and then adopts the shorter horizon | Self-contradiction between the study's own stated rule and its adopted value | **+EGP 0.369 (+9.1%)** at a coherent 5% inflation and 5% growth | Apply the rule the register states |
| 8 | Table 21 row 3 | The priced terminal-growth alternative | Logic | PARTIAL | "Two percentage points below it… 2.45 (−1.59)" | Moving g to 3% in the delivered model gives **EGP 4.811 (+0.77)** — the **sign reverses**, because the "capital for REAL growth" line flips to a +EGP 2,032m perpetual cash release. No (g, inflation) pair tested produces 2.45 (3/7 → 4.81; 5/7 → 4.50; 3/5 → 4.73; 5/5 → 4.41; 3/3 → 4.76) | Ten of the other eleven alternatives reproduce to the penny; this one does not | Row is wrong in magnitude and in direction | Re-run it, or remove the growth-capital term's asymmetry |
| 9 | Table 23 | Maintenance-capex range | Disclosure | PARTIAL | "1.1% of revenue **against 0.7%**" | Every other table gives the alternative as **6.11%**; the workbook's own formula gives **5.76%**. 0.7% appears nowhere, and a lower rate would raise value, not lower it | A typed figure contradicting four other places in the same document | Row meaningless as printed | 1.12% against 5.76% |
| 10 | Appendix A.1 | Forecast income statement | Disclosure | PARTIAL | Gross profit, selling and distribution, administrative, EBIT | **No forecast year foots**: 5,337 − 856 − 410 = 4,071, not the printed 3,921. The gap is exactly the unprinted stoppage line (150 / 120 / 100 / 91 / 80) in all five years. The three historical years foot exactly | A deduction the model makes and the page does not print | None (model right, page incomplete) | Print the stoppage row |
| 11 | Table 35 (§C.6) | Panel divergence table | Logic | PARTIAL | E1 vs E2 = 1.04; E2 vs E3 = −2.36; E1 vs E3 = −1.32; panel vs DCF = −4.04 | From the panel's own centrals (4.47 / 4.29 / 4.98): **0.18, −0.69, −0.51**. "−4.04" is the DCF answer, not a gap | Three of six rows do not reproduce from figures printed four pages earlier | None on value; the table is the study's summary of its own panel | Recompute |
| 12 | §C.3 | Expert 3's published range | Logic | PARTIAL | "Range: EGP 0.00 to EGP 5.13"; "the **lowest** and the widest of the three" | The option reprices exactly (13,181 / 12,865 / 13,598 all verified to the pound) → **4.86 to 5.13**; the grid's own lowest cell is 3.84. **Nothing produces 0.00.** And 4.98 > 4.47 > 4.29 — it is the **highest** central, not the lowest | The 0.00 is what makes "the panel spans EGP 0.00 to 8.52" and the whole "ordering" narrative in §C.5 | Panel floor is 2.78, not 0.00 | Publish 4.86–5.13 |
| 13 | Table 39 | Expert 3's underlying | Constr. | PARTIAL | Underlying = EV incl. non-operating 18,057; strike = **gross** debt 14,639 | The underlying excludes the EGP 4,607m of cash while the strike is gross debt. Consistent treatment (cash in the underlying) → call 17,629, ×0.75 → **EGP 6.66/share** | Cash charged twice against that lens | **+EGP 1.68** on Expert 3 | Strike gross debt against an underlying that holds the cash |
| 14 | Table 17, Assumptions C105 | Debt currency split | Constr. | PARTIAL | 99.7% dollar, carried flat through five years and the perpetuity; Table 20 even says "the same dual-currency structure forward" | **Verified note 18-3**: the facility funding the remaining spend is **EGP 5,930,700,606 + US$82,945,038 — 58.8% EGP**. The study quotes both figures correctly and then models a 99.7%-dollar book forever | Pass-3 rule ("split the book into tranches") declared, read, and not applied. Terminal effect dominates: local 19.40% vs dollar-equivalent 13.90% | **−EGP 0.16 to −0.26 (−4% to −6%)** at a 25–40% local book | Amortise the split over the drawdown |
| 15 | Relative & Normalized B24 | Normalised lens exchange rate | Input | PARTIAL | 55.89, "The second year of the currency path" | The live path is **55.43 / 59.81 / 63.23 / 66.23 / 69.20**. 55.89 is the second year of the **retired** path in the register (53.49 / 55.89 / 57.85 / 59.32 / 60.83), built on the superseded 10/7/6/5/5 inflation array | A live lens consuming a withdrawn input, with a false source note | That lens moves to 4.07 (yr 1) or **6.19** (yr 2) vs 4.29 | Read the currency sheet |
| 16 | Assumptions C63–C67 | Other revenue path 140 → 186 | Input | PARTIAL | Register: `other_rev_FY2425 = 30 EGP m — note 20, merchant nitric acid, plant rent and services` | **Verified note 20**: revenue is export 6,608,751,963 + local 1,993,849,978 + services sold **EGP 4,430** + nil = 8,602,606,371. There is no EGP 30m line. Note 24 shows rents receivable of **EGP 3.87m** | A 4.7× opening step off a base that is not in the cited note, never shown to the reader | **−EGP 0.307 (−7.6%)** if the filed base is carried | Cite the note that holds it |
| 17 | §3, Table 22 | The price simulation | Logic | PARTIAL | "fifty thousand simulated paths… drifting at the carry" — rf 23.0%, vol 46.8% | From the published percentiles: σ implies **34.2%** (1M) and **37.5%** (3M) annualised, not 46.8%. And the **median** grows at 23.0%/yr (13.98·e^(0.23/12) = 14.25 vs published 14.26), so the mean runs **5.8–7.0 pp above** the declared carry | The declared volatility does not reproduce the published cone; the Itô correction is missing | None on value; inflates every up-touch probability | Set the mean, not the median, at the carry |
| 18 | §1.8, Table 1, §6, Table 19 caption | Typed prose figures | Disclosure | PARTIAL | "The narrowest is terminal growth, worth EGP 1.59"; "the **ten** priced alternatives" (×2) beside "**Eleven** choices" (×2); "US$540 — a long-run export price **above today's spot**"; "the two are close to each other" (13.0% vs 35.1%) | Five rows are narrower than 1.59 (0.21, 0.43, 0.84, 0.91, 1.15); the table has 11 rows; the study's own spot is **US$545**; 35.1% is 2.7× 13.0% | Four prose claims contradicted by the study's own tables | None | Compute, don't type |
| 19 | Bibliography Table 3 | Anchor price provenance | Disclosure | PARTIAL | "Share price \| EGP 14.41 \| **6 Aug 2026**" | The register's own `spot_price` row says 2026-09-03, and the study says the 6 August close was **13.98** | The source register misdates the single most-cited figure. Related: rf (6 Aug), FX spot (7 Aug) and urea (7 Aug) are four weeks older than the price that sets the equity weight | None directly; the cost of capital mixes two vintages | One date, or say there are two |
| 20 | "Read first", Table 14 | Project progress pairing | Input | PARTIAL | "12.9% built against a 37% plan **at the last reported date**" set against "27.8% of the money spent" (31 Mar 2026) | The 12.9% / 37% are the auditor's at **30 September 2025**. The FY2024/25 annual (verified) gives **8.3% against 21.7% at 30 June 2025** | Two figures six months apart presented as a matched pair, one of them mislabelled as the latest | Overstates the spend-vs-progress gap | Date both sides |
| 21 | Table 20, Assumptions C101 | Local cost of debt 19.40% | Disclosure | PARTIAL | "the company's own **disclosed** rate on a state-bank facility… used as disclosed" | **Verified**: note 26 discloses the EGP 96,896,001 of interest; note 18-2 discloses only a **combined balance of EGP 596,896,001**. The EGP 500m principal is inferred as balance less interest. The holdco balance was **nil** at 30 June 2024, so the facility was drawn in-year and 19.40% is a **floor**, not the rate | A derived rate presented as disclosed — and it is the rate that carries the "borrows below its sovereign" argument | Nil (0.31% of the book) | Call it derived; state that the drawdown date is unknown |
| 22 | §1.4, Table 9 | The 10× normalised multiple | Constr. | PARTIAL | "A mature single-asset industrial in a high-inflation economy does not deserve more than ten times" | On the study's own terminal capitalisation the consistent multiple is 1/(0.1833 − 0.07) = **8.82×** → EGP 3.40; on a flat nominal stream 1/0.1833 = 5.45× → EGP 0.85 | Not Fisher-derived; asserted, and generous against the study's own discount rate | −EGP 0.89 to −3.44 on that lens | Derive the multiple from the cost of capital |
| 23 | Register `local_free_price_FY2425` | Local free-market price | Logic | PARTIAL | "18,485 — export parity at the FY2024/25 realised price and rate, **times the 90% local clearing ratio**" | 385 × 49 × 0.90 = **16,979**. 18,485 = parity × 0.98 | Stated construction does not reproduce; the forecast then runs the 0.90 | ~−0.8% of revenue on the free-market leg | Reconcile the two |
| 24 | §1.2, Table 8 | Sustainable ROE 6.9% | Logic | PARTIAL | Return on **opening** equity of 7,250 (FY2023/24) | **Verified note 14**: the EGP 4.0bn capital increase was approved 20 March 2024, mid-year. On average equity the FY2023/24 return is **~4.6%** | Opening-equity denominator excludes in-year capital | None (lens floors at zero) | Average equity |
| 25 | Workbook | Stale and duplicated cells | Disclosure | PARTIAL | Workbook is "a live formula model" | Monte Carlo `B12 "Spot at the anchor date" = 14.41` against `B13 = 2026-08-06` — the whole "against spot" column computes off the wrong price (the document is right, the workbook is stale). The file carries **no cached values at all**. The "field" is defined twice: `Summary!B11` excludes the book lens; `Fundamental Valuation!B29` includes it at **8.16** while the document publishes that lens at **0.00** | Three internal inconsistencies between document and workbook | None on the headline | Recalculate before issue |
| U1 | §1.6, §7 | Realised gas price US$4.68/mmBtu | Input | **UNVERIFIABLE** | Anchored on a Q1 FY2025/26 disclosure (31,313,235 m³ at EGP 251m = EGP 8.016/m³) | The **FY2024/25 annual (verified)** discloses EGP **249m** of abnormal gas loss for the year. If the study's own FY2024/25 lost volume of 38,480,270 m³ is right, that is EGP 6.47/m³ = **US$3.74/mmBtu** | Two of the company's own disclosures give two prices; the study adopts the higher without saying the other exists. I could not reach the production table to verify the volume | **+EGP 2.38 (+59%)** at US$3.74 | Reconcile the two disclosures |
| U2 | Bridge, Table 35 | Contingent gas liability | Constr. | **UNVERIFIABLE** | Nothing | **Verified note 28 (contingent liabilities)**: the gas price was raised to **US$5.75/mmBtu from 1/11/2021** and again by formula from 13/9/2022, and the company has not received the authorising regulatory decisions. The bridge deducts nothing and the risk register does not name it | A disclosed contingency, unquantified in the filing, absent from the bridge | On the model's own volume (14.5m mmBtu/yr), four years at US$1.07 ≈ **EGP 3.0bn = EGP 1.53/share** | Deduct it, or disclose it |
| U3 | §1.6, note 21 | The cost stack's reconciliation | Constr. | **UNVERIFIABLE** | Five components: gas, other materials, wages, services, D&A | **Verified note 21 foots exactly** (4,398,635,932 + 212,857,408 + 62,556,751 + 776,471,327 + 2,056,278 + 69,990 − 87,164,710 − 65,173,061 = 5,300,309,915). The model's four components on FY2024/25 inputs give **5,450.6** against a reported **5,300.3** — it omits the two inventory-change lines. Separately, the auditor discloses an O&M contract costing **US$8.436m = EGP 417.746m** charged to FY2024/25; the model's entire purchased-services line is **EGP 62.557m** | The forecast stack is never reconciled to the note it is built from | Unknown; if the O&M fee is genuinely absent, >EGP 1/share understated | Foot the stack to note 21 |

---

## Section C — Arithmetic Reconciliation Appendix

### C.1 Cost of capital

| Line | Report | Recomputed | Δ |
|---|---|---|---|
| Normalised rf, CDS = 23.00 − 3.41 | 19.59% | 19.590% | 0 |
| Normalised rf, rating = 23.00 − 6.37 | 16.63% | 16.628% | 0 |
| Ke CDS = 19.590 + 1.03021 × 9.41 | 29.28% | 29.284% | 0 |
| Ke rating = 16.628 + 1.03021 × 13.9377 | 30.99% | 30.986% | 0 |
| Kd (USD) local-equivalent yr 1 = 1.117 × (1.14/1.024) − 1 | 24.35% | 24.354% | 0 |
| Blended Kd post-tax, yr 1 | 18.86% | 18.862% | 0 |
| WACC yr 1, CDS = .66165 × .29284 + .33835 × .18862 | 25.76% | 25.758% | 0 |
| WACC yr 1, rating basis | 26.88% | 26.884% | 0 — gap 113 bp ✓ |
| Terminal rf = 7.0 + 5.5 | 12.50% | 12.500% | 0 — **text says "compounded" → 12.885%** |
| Terminal WACC | 18.33% | 18.333% | 0 |
| Equity weight (28,626.6 / 43,265.6, gross debt) | 66.2% | 66.165% | 0 — textbook Damodaran construction, **undeclared but correct** |

### C.2 Cash-flow waterfall, programme carried through (EGP m)

| | FY2026/27 | FY2027/28 | FY2028/29 | FY2029/30 | FY2030/31 |
|---|---|---|---|---|---|
| Revenue — report / mine | 11,674 / 11,674.0 | 12,693 / 12,693.1 | 13,513 / 13,512.7 | 14,277 / 14,277.2 | 15,043 / 15,043.4 |
| EBITDA | 4,812 / 4,812.0 | 5,203 / 5,203.0 | 5,492 / 5,492.4 | 5,746 / 5,745.7 | 5,987 / 5,987.1 |
| D&A | 891 / 890.6 | 1,009 / 1,008.7 | 1,147 / 1,146.5 | 1,292 / 1,292.3 | 1,434 / 1,434.1 |
| NOPAT | 3,039 / 3,039.1 | 3,251 / 3,250.6 | 3,368 / 3,368.0 | 3,451 / 3,451.3 | 3,529 / 3,528.6 |
| Capital expenditure | −2,729 / −2,729.1 | −3,242 / −3,241.6 | −3,451 / −3,450.8 | −3,359 / −3,359.3 | −2,657 / −2,657.2 |
| Δ working capital | +788 / +788.2 | −220 / −219.8 | −190 / −189.7 | −182 / −181.9 | −183 / −183.4 |
| **FCFF** | 1,989 / 1,988.8 | 798 / 797.8 | 874 / 874.2 | 1,202 / 1,202.4 | 2,122 / 2,122.2 |
| Discount rate | 25.76 / 25.758 | 23.82 / 23.822 | 22.24 / 22.238 | 21.02 / 21.019 | 20.01 / 20.012 |
| Discount factor | .7952 / .79517 | .6422 / .64220 | .5253 / .52536 | .4341 / .43411 | .3617 / .36173 |
| **Present value** | 1,581 / 1,581.4 | 512 / 512.4 | 459 / 459.2 | 522 / 522.0 | 768 / 767.6 |

All lines reconcile. Compounding convention (year-end, glide compounded year by year, terminal brought home on the year-5 factor) confirmed.

**Undisclosed construction, no arithmetic error:** the +788 year-one release comes from applying FY2024/25 day counts to the **31 March 2026 interim** balance sheet (1,230 + 3,378 − 1,539 = 3,069.4). The reader can derive it from Table 31 but Table 16 never prints the 3,069.

### C.3 Terminal block, and the implied asset life

| Line | Report | Recomputed | Δ |
|---|---|---|---|
| Year-5 EBIT + project depreciation, × 1.07 | — | 5,387.3 | — |
| Project revenue (264,000 × 50% × US$280 × 72.29) | — | 2,671.8 | — |
| Project operating profit after own depreciation | 40 after tax | 51.5 → 39.9 after tax | 0 ✓ |
| Terminal EBIT / PAT | — | 5,438.8 / 4,215.0 | — |
| Book D&A in terminal | — | 1,822.4 | — |
| Capital maintenance = −D&A × 1.07^4.4544 | — | −2,463.4 | — |
| Capital for real growth (g = inflation ⇒ nil) | — | 0.0 | — |
| Working-capital inflation | — | −228.9 | — |
| **Terminal free cash flow** | — | **3,345.1** | positive ✓; implied payout 79.4% ∈ (0,1) ✓ |
| Terminal value / present value | — | 29,516 / 10,676.8 | vs 10,677 ✓ |
| Terminal value as a share of EV | 73.5% | 73.54% | 0 — above 70%, **disclosed and discussed** ✓ |

**Implied asset life — the pass that matters.** Accumulated depreciation ÷ the year's charge = 3,435,299,807 ÷ 771,213,489 = **4.4544 years**; depreciable gross cost ÷ charge = (17,022,493,238 − 1,662,949) ÷ 771,213,489 = **22.0702 years**. Both **verified to the pound against note 6** of the audited statements, together with the EGP 220,495,594 of fully-depreciated assets still in production (1.295% of the base). 22.07 years sits inside the disclosed 3.95% machinery rate (25.3 years). The study explicitly retired the reinvestment identity *because* it implied a 14.3-year cycle (1/0.07) — "a fact about the pound rather than about a urea plant". **This is the single most common terminal-value failure and the report does not commit it.**

### C.4 Enterprise-to-equity bridge

Foots in both columns and both units.

- Carried through: 3,842.7 + 10,676.8 = 14,519.5 EV; − 10,032.5 + 1,382.9 + 2,155.1 = 8,024.9; ÷ 1,986,578,999 = **EGP 4.0396**.
- Per share: 7.31 − 5.05 + 1.78 = 4.04 ✓
- Stopped: 11,012.7 + 11,451.5 = 22,464.2 → 15,969.7 → **EGP 8.0388** ✓

Latest disclosed balance sheet used ✓; no minority interest exists ✓; listed stakes at market ✓; no dividend declared ✓; cash charged exactly once ✓ (gross-debt weights with net debt deducted is the textbook construction).

### C.5 The published alternatives

**Ten of eleven reproduce to the penny:** beta 0.7165 → 5.784 (pub. 5.78); gas US$5.75 → 1.327 (1.33); gas 1,200 m³ → 4.884 (4.88); utilisation 70% → 4.465 (4.47); maintenance 6.11% → 3.130 (3.13); age 11.04 y → 1.820 (1.82); flat spot rate → 1.438 (1.44); rating basis → 2.510 (2.51). **Exceptions:** terminal growth (finding 8) and project capex (3.954 vs 3.83).

### C.6 Verified directly against the filings (all exact)

Revenue 8,602,606,371 and its export/local split 6,608,751,963 / 1,993,849,978 (note 20); COGS 5,300,309,915 with materials 4,398,635,932, wages 212,857,408, purchased services 62,556,751 (note 21, which foots); selling cost 786,462,833 with freight and commissions 610,164,356 and the other three lines summing to 176,298,477 (note 22, which foots); share count **1,986,578,999 × EGP 5 = 9,932,894,995** with the 69.825% holding and the 6.184% free float (note 14); stoppage cost 164,477,627 and 152,741,795 (note 25); project-loan interest 1,338,012,810 and holding-company interest 96,896,001 (note 26); loan balances 397,313,599 / 11,183,315,516 / 596,896,001 (note 18); provisions 309,113,094 (note 16); net fixed assets 13,587,193,431 and 14,144,466,955 (note 6); the ANNA approved cost **EGP 6,422,418,326 + US$278,384,958** and the 16/18-instalment schedule to 2035/2036 (note 18-3); the US$5.75/mmBtu contract price (note 28); the 1,200 t/d ammonia and 1,575 t/d urea design plates and the EGP 781m cumulative abnormal gas loss (auditor's report); the 12%-of-export-price Abu Qir arrangement; and one operating segment (note 29).

The filings have **zero text layer** across all 48 pages, exactly as the bibliography states — the OCR route is disclosed and correct. The bibliography's filing index matches the portal precisely, including the absence of annuals for 2012, 2015 and 2017.

---

## Section D — Construction Register

| | Declared | Actually done | Agree? |
|---|---|---|---|
| Primary lens | Cash flow, two-sided, others cross-checks, blend retired | Exactly that; blend published unused at 5.873 (reproduces) | **Yes** |
| Terminal construction | Replacement-cost maintenance on a **measured** age; reinvestment identity retired | Exactly that; both identities verified against note 6 | **Yes** |
| Cost-of-capital path | Glides from spot build to a terminal made of its own components | Glides; terminal rf is **additive** where the text says compounded | Partly (#6) |
| Country risk | Enters once — sovereign yield less own default spread, premium added back | Exactly that, on both bases, never mixed | **Yes** |
| Cost of debt | Local tranche at its own rate; dollar tranche at local-equivalent on the study's own inflation wedge | Exactly that — **the classic error pair is closed at both ends**; local rate is derived, not disclosed (#21) | **Yes**, with #21 |
| Currency split of the debt book | 99.7% dollar; "the same dual-currency structure forward" | 99.7% dollar to perpetuity, against a disclosed 58.8%-EGP forward facility it quotes correctly | **No** (#14) |
| Inflation path and escalators | One path, house-wide; one escalator per driver class; "a globally traded input is never put on [the domestic index]" | Domestic lines on CPI ✓, gas on its dollar price through the currency ✓, subsidised on its administered path ✓ — but the **export price carries no escalator at all** (#3), and the ad-valorem Abu Qir commission rides the domestic index | **No** (#3) |
| Terminal currency wedge | "terminal growth, the terminal risk-free rate and the terminal currency wedge now share one inflation" | C103 = 4.492% (built on 7%) and C133 = 2.539% (built on 5%) coexist; both source notes still say 5% | **No** (immaterial: 3 bp) |
| Forecast anchor | Opens on nine reviewed months plus a run-rated Q4 | Opens at 11,674 vs 10,379 (+12.5%), above the latest estimate ✓. **Mirror case fires** on the export price (+37.7% over the last filed realisation, then flat) and on other revenue (4.7× the filed base) — a mechanism is named for the first, none for the second | Partly (#3, #16) |
| The bridge | Latest balance sheet, market-value weights, net debt, stakes at market | Exactly that; foots in both columns | **Yes** |
| Margins | Outputs, never inputs | True of the workbook — every margin is a residual. But the **project** margin is a typed 32% input the register says was replaced (#5) | Partly (#5) |
| Sensitivities | Every cell a complete re-run | +EGP 0.95 constant across all 25 cells (#1) | **No** |

---

## Section E — Verdict Summary

### Counts by pass

| Pass | Fails |
|---|---|
| 1 — Input verification | 3 (2 partial, 1 unverifiable) |
| 2 — Market data | 1 |
| 3 — Cost of capital | 3 |
| 4 — Terminal value | 3 |
| 5 — Macro coherence | 1 **total** |
| 6 — Forecast anchoring | 2 |
| 7 — Lens architecture and the bridge | 5 |
| 8 — Calculation verification | 3 |
| 9 — The delivered page | 5 |
| 10 — Probabilistic content | 2 |
| 11 — The answer itself | 1 |
| 12 — Completeness | 3 |
| **Totals** | **5 TOTAL, 22 PARTIAL, 3 UNVERIFIABLE** |

These sit against a very large number of passes, including the full waterfall, the bridge, the cost-of-capital build, the cost-of-debt currency pair, the terminal's implied asset life, the option pricing (exact in all 15 grid cells and both branches), the backtest counts (54/57, 50/57, 32/57), the claim that no alternative closes the gap (all three favourable ones together give 7.35), and every filing figure I could reach.

### The three most valuation-critical findings

1. **The export-price escalator (#3).** Declared as "the commodity path", implemented as a frozen nominal dollar price against a fully inflating cost stack — a −2.4%/yr real price forecast worth **+EGP 2.78 (+69%)** at the neutral construction, while the study's own normalised lens values the same tonne at US$400, which would put the DCF at **−EGP 2.66**. Two lenses, one observable, never reconciled.
2. **The project's economics (#5 and #2).** The register records that the 32% cash margin was replaced by a disclosed conversion cost and the derived nameplate replaced by an EPC figure; the workbook runs the *old* margin and the *new* nameplate, and the document describes the *old* nameplate. Together these move the answer **−7.4% to +30%**, and they are the entire basis for the study's headline claim that the programme earns 0.2% on its capital.
3. **The sensitivity grid (#1).** A constant EGP 0.95 offset across 25 cells proves it is not a re-run of the delivered model, and Table 20 — the study's ranking of what drives the answer — is read off it.

### Direction of the contested-judgement count

Of 14 judgements worth more than 5% of value, **eight are resolved against the report's own answer** (export price vs real-flat −2.78; gas vs the FY2024/25 disclosure −2.38; beta −1.74; terminal inflation −0.37; debt currency −0.16 to −0.26; utilisation −0.43; nameplate as documented −0.30; project margin −1.21) and **six in its favour** (capital-maintenance age +2.22; maintenance rate +0.91; other revenue +0.31; terminal rf +0.14; nameplate as run +0.30; peer band high).

**This is not a one-directional book** — which is unusual and worth saying plainly. The study is conservative where it says it is, and generous in three places it does not flag.

### The reverse read, in the units the study never publishes

At the sanctioned construction the traded price of EGP 14.41 is reproduced by a long-run export price of **US$731/t** — a level the study's own Expert 3 states the market reached inside the preceding eighteen months ("the export price alone moved between US$380 and US$730"). The study publishes only the discount-rate reverse read (13.0% against a 23.0% sovereign, which is genuinely implausible) and never this one. A believable reverse read is evidence *against* the report's disagreement with the market, and this one is not obviously unbelievable.

### Does the headline range survive the corrections?

**It shifts materially.**

The carried-through central of EGP 4.04 is not defensible as published: correcting only the two constructions the report's own register says were already corrected (the project margin and a real-consistent dollar price) takes it to **EGP 8.03** — the same place as the "programme stopped" branch, and still 44% below the traded price. The relative lens at EGP 15.99, the only reading above the price, rests on a 9.9× labelled as a median of a set whose median is 8.20 and sourced to an aggregator the study's own rules forbid; on the band that label implies, that lens centres at **EGP 13.93** and the sentence "one of them now reaches the traded price" fails.

The **direction** of the study's conclusion — that this equity is worth materially less than EGP 14.41 on any cash-flow construction — survives every correction I can quantify. The **number** does not.

---

*This audit verifies what the documents assert. It does not propose an alternative valuation.*
