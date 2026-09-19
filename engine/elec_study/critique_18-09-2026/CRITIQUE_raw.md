# Forensic Audit — Testahil *Independent Valuation Study*, Electro Cable Egypt Co. S.A.E. (EGX: ELEC)

**Subject documents:** `01_valuation_study.docx` (edition 05-08-2026) · `02_valuation_model.xlsx` (16 sheets) · `03_bibliography.docx` (Source Register)
**Audit date:** 18 September 2026
**Standard applied:** Master Audit Prompt v2 — 12-pass forensic verification
**Auditor's position:** Adversarial to every claim; a failure is recorded only where it can be demonstrated. Suspicions that could not be demonstrated are logged UNVERIFIABLE, never as FAIL. No alternative valuation is proposed.

---

## Section A — Audit Scope

Audited the valuation study, the 16-sheet companion workbook (479 formula cells, fully traced) and the Source Register, against primary and near-primary sources reachable on 18 September 2026.

**Reached:** Damodaran `ctryprem` original file (Egypt row, "Last updated January 5, 2026"); LME copper cash settlement (14-Aug-2026); El Sewedy Electric FY2025 results; **and Electro Cable Egypt's H1-2026 results, published c. mid-August 2026 — six weeks before this audit and absent from the study.**

**Not reached:** ELEC's audited FY2025 statements (the study's own stated blocker, independently confirmed); the Egypt 10-year local-currency yield for the stated date (worldgovernmentbonds served an unpopulated template; a re-run against a second host also failed to date-match — an empty result was not treated as a clean result); El Sewedy's FY25 EBITDA; Riyadh Cables' balance sheet.

The workbook recalculates cleanly and its headline value ties to the document. The failures below are almost entirely **construction and disclosure**, not arithmetic.

---

## Section B — Fail Table

### B.0 Summary index

| # | Location | Plane | Severity | One-line finding |
|---|---|---|---|---|
| F1 | §1.6, §5, §7 | Input | **TOTAL** | H1-2026 results published and not carried; FY26E loss 4.7× the annualised actual |
| F2 | §1.6, §7 | Input / Disclosure | **TOTAL** | "FY24 audited comparatives" are a retail aggregator's summary page |
| F3 | DCF!B21, §1.1 | Construction | **TOTAL** | Terminal ROIC denominator undisclosed; contradicts the model's own balance sheet; EV −19% |
| F4 | §1.8 | Construction | **TOTAL** | Beta regressed on a 30-name in-house basket, not the listing exchange's index |
| F5 | Register §C | Disclosure | **TOTAL** | Register's Global ring (C.3) does not exist; copper has no input record |
| F6 | Register §B, §D | Disclosure | **TOTAL** | Register publishes a materially different model from the one delivered |
| F7 | §1.5 | Construction / Disclosure | PARTIAL | 95.8% of the headline central comes from two lenses that assume the debt repaired |
| F8 | §1.2, §1.5 | Construction | PARTIAL | Book value weighted into the central; it is 54.2% of the answer |
| F9 | §1.2 | Construction | PARTIAL | Book lens discounts a 240%-geared book at the terminal, deleveraged Ke |
| F10 | §1.2, bridge | Input | PARTIAL | Book lens and bridge ignore the disclosed 1Q26 / H1-26 losses |
| F11 | §1.2 table | Logic | PARTIAL | Printed bull justified P/B 1.16× does not reproduce (1.061×) |
| F12 | §1.9 | Disclosure | PARTIAL | Grid note states terminal ROIC 10.3%; everywhere else 9.2% |
| F13 | §1.8 | Construction | PARTIAL | Terminal beta not relevered for the assumed deleveraging |
| F14 | §1.6, A.1 | Construction | PARTIAL | Conversion-EBITDA/t "history" back-solved through assumed finance costs |
| F15 | §1.8 | Logic | PARTIAL | Cost-of-debt effective-rate cross-check is circular |
| F16 | Register `net_debt_fy25_est` | Construction | PARTIAL | Load-bearing payables-scaling step is assertion; "skewed adverse" is one-sided |
| F17 | §1.6, Assumptions B46 | Construction / Disclosure | PARTIAL | D&A driven off revenue at 2× the historical ratio |
| F18 | §1.6, Assumptions B43 | Construction | PARTIAL | Currency path hand-set, not derived from the inflation differential |
| F19 | §1.6, §5 | Construction | PARTIAL | Copper enters the cost side only; a record flat anchor labelled "no view" |
| F20 | §1.6, READ FIRST | Construction | PARTIAL | "Margins are OUTPUTS" — conversion margin is a typed EGP/tonne input |
| F21 | §1.3, §1.5 | Construction / Disclosure | PARTIAL | Relative lens clamped in all three scenarios, carried as a range, weighted 20% |
| F22 | §1.1, C.2, C.3 | Disclosure / Logic | PARTIAL | Four unreconciled option-value floors; bridge does not reach its printed answer |
| F23 | §1.1, §1.8 | Construction | PARTIAL | Explicit window ends mid-recovery, then capitalises 5% |
| F24 | §1.1 | Disclosure | PARTIAL | Implied asset life, disclosed-life capex basis and filed-ROIC comparison all absent |
| F25 | §1.8 | Construction | PARTIAL | Gross debt in the WACC weights, net debt in the bridge |
| F26 | §1.8, A.2 | Construction | PARTIAL | Terminal 60/40 structure contradicts the model's own FY30 balance sheet |
| F27 | Discount convention | Logic | PARTIAL | No stub-period adjustment from a 5-Aug valuation date |
| F28 | Workbook vs study | Disclosure | PARTIAL | Peer multiples and FY24 net debt differ between workbook and document |
| F29 | `Income Statement!F13:I13` | Logic | PARTIAL | Loss-carryforward formulas reference the wrong prior-year column (latent) |
| F30 | Sensitivity / Monte Carlo | Disclosure | PARTIAL | Grids hardcoded; live base cell can silently diverge |
| F31 | A.3 | Disclosure | PARTIAL | Two definitions of operating cash flow in one row |
| F32 | Headline prose | Disclosure | PARTIAL | Uncheckable prose figures; 1-month cone label inconsistent with its own width |
| F33 | §1.8, B.1 | Input / Sourcing | PARTIAL | Aggregator risk-free at the low edge of its band; mislabelled spread; SWDY NP |
| F34 | Whole study | — | **FLAG** | ~15 of 17 contested judgements resolved the same way, all labelled "conservative" |
| F35 | §4, §11 | Disclosure | PARTIAL | The reverse read is never solved |

---

### F1 — TOTAL FAIL · Input · §1.6, §5, §7, Register §E

**Item:** The study's own named falsifier has already fired and is not carried.

**What the report says:** "H1-2026 results due ~mid-Aug-2026 — the single largest scheduled event"; "The single most important print of the year"; FY26E revenue 10,178, FY26E net loss **−1,873 mn**; "Q1 ran ~11k EGP/t conversion at 37% utilization, so the FY26E average of 40k requires Q2–Q4 near ~50k as utilization recovers — the H1-2026 statements (due ~mid-Aug) are the first checkpoint on that ramp."

**What is correct (primary):** H1-2026 consolidated net sales **EGP 4,329 mn** (vs 6,438 mn), net loss attributable **EGP 200.833 mn** (vs +487.121 mn), loss per share EGP 0.06; standalone loss 50.821 mn on revenue 2,050 mn — Arab Finance / Zawya reporting of the EGX filing, the same source class the study itself relies on throughout.

By subtraction against the disclosed Q1: **Q2-2026 revenue 2,235 mn** and **Q2-2026 net PROFIT +40.779 mn**.

**Why it failed:**

- FY26E net loss is **4.7× the annualised H1 actual** (−1,873 vs −402). The forecast now requires H2-2026 to lose **1,672 mn** after a quarter that made money.
- Revenue annualises to 8,658 — **14.9% below** the FY26E driver of 10,178. H2 would need +35% on H1.
- The YoY revenue decline decelerated sharply: Q1 −43.8% → **Q2 −17.7%**.
- On the study's own finance-cost run-rate (2,157/yr = 539/qtr), a +40.8 mn net quarter implies Q2 EBITDA ≈ **609 mn — 1.5× the study's entire FY26E EBITDA of 416 mn**.
- Implied Q2 conversion EBITDA per tonne is **131–255 k EGP/t** (bounds set by the register-flagged 243/qtr versus the modelled 539/qtr finance line), against a driver of 40 k and a stated checkpoint of ~50 k. The study's own stated falsifier was "conversion EBITDA per tonne back above ~100,000 EGP without currency help."

**Impact on fair value:** The FY26E P&L, the net-debt compounding schedule (13,620 FY27 → 19,602 FY30) and the "book equity breaches zero by FY29E" solvency claim are all built off a first forecast year the company did not print. The study forecast a **volume recovery with a margin trough**; the company printed a **volume shortfall with a margin recovery** — the decomposition is inverted.

**Correct method:** Re-anchor FY26E on the H1 actual, re-derive Q2 conversion economics from the disclosed lines, and re-run the debt schedule before publishing.

---

### F2 — TOTAL FAIL · Input / Disclosure · §1.6, §7, Register §C.4

**Item:** The "FY24 audited comparatives" are a retail aggregator's summary page.

**What the report says:** §1.6 — "the anchor is rolled forward from **the FY24 audited comparatives** (assets 14,970 · debt 8,960 · cash 828 · equity 3,600)."

**What is correct:** Register §C.4 records `cash_fy24 827.6`, `equity_fy24 3,600`, `liab_fy24 11,300`, `ebit_fy24 3,400` and `int_cover_fy24 2` — **all five sourced to Simply Wall St, 22 May 2025.** Only `debt_fy24 8,960` is genuinely a filing comparative ("vs 8.96bn in 2024"); `assets_fy24 14,970` is Zawya's FY25 note comparative.

**Why it failed:** Prime Directive 2. A fallback is permitted and must be declared; using one silently while calling it audited is a false claim about the report's own evidence — made on the single input that decides whether the equity is worth zero.

**Impact on fair value:** No direct arithmetic move. It removes the evidentiary basis for the stated ±EGP 0.19/share net-debt range and for the "skewed adverse" characterisation of the residual risk.

**Correct method:** State each FY24 line's actual document type, exactly as the Register (correctly) does and the study (incorrectly) does not.

---

### F3 — TOTAL FAIL · Construction · `DCF!B21`, §1.1, Appendix C.3

**Item:** The terminal ROIC denominator is an undisclosed construction that contradicts the model's own balance sheet.

**What the report says:** "terminal return on capital of 9.2%"; "Terminal value (g = 5.0%, ROIC-consistent: 9.2% ROIC × 55% reinvestment)"; Expert 3 — "Invested capital (terminal-year basis) 16,325." **The denominator is never stated anywhere in the study.**

**What is correct (recomputed):**

`DCF!B21 = NOPAT ÷ (NWC + 5% × revenue)` = 1,497.1 ÷ 16,325 = **9.171%**

The workbook's own Balance Sheet sheet computes invested capital as NWC + PP&E + other assets = 15,447 + 1,096 + 2,980 = **19,523** → ROIC **7.669%**, RR 65.20%, terminal FCFF 547, TV **5,471** (not 7,150), PV of TV 2,386, EV **3,081** (not 3,813), unfloored **−2.03/share** (not −1.81).

**Why it failed:** Two definitions of invested capital in one workbook, neither disclosed, and the flattering one sets the terminal. The report's own §1.9 ROIC grid carries 7.7% → TV 5,513 → −2.02 — **the correct figure is already in the report, labelled a downside sensitivity rather than the base.**

**Impact on fair value:** Enterprise value overstated by **733 mn (−19%)**; terminal value overstated 23%. The equity remains floored at zero, so the headline central does not move — but Expert 3's enterprise value and the whole terminal discussion do.

**Correct method:** Use one invested-capital definition across the workbook, and print it.

---

### F4 — TOTAL FAIL · Construction · §1.8, Register `beta`

**Item:** Beta regressed against an analyst-constructed basket rather than the listing exchange's published index.

**What the report says:** "Beta (own regression, weekly, 5yr) 0.964 — vs **30-name equal-weight EGX composite**: R² 0.222, n=257, SE 0.113, CI90 [0.78, 1.15] — passes the usability gate; not weak-flagged."

**What is correct:** The regressor must be the published index of the exchange the stock is listed on (EGX30 / EGX70, in which ELEC sits).

**Why it failed:** An equal-weight basket of the house coverage universe is a coverage artefact, not a market. The R² of 0.222 is disclosed but never treated as a limitation on the regressor's validity.

**Impact on fair value:** Small here, and the report proves it — the beta grid spans 0.60 to 1.30 for only ±0.18/share unfloored, entirely inside the floored conclusion. Material as a standing method failure rather than for this answer.

**Correct method:** Re-run against the published EGX index; retain the basket as a cross-check only.

---

### F5 — TOTAL FAIL · Disclosure · Register §C

**Item:** The Register's Global ring does not exist, and copper — the model's single largest driver — has no input record.

**What the report says:** Ring table — "Global | World-level facts that reach the company through prices (copper, rates) | **2 records**"; and, in the READ FIRST — "A bare numeral cannot enter the model: the build fails."

**What is correct:** Section C runs **C.1 → C.2 → C.4 → C.5. There is no C.3.** LME copper ($14,000/t, held flat for five years, driving every price per tonne, all revenue, and — through NWC set as a percentage of revenue — the entire working-capital load) appears in **no input record in any ring.**

**Why it failed:** A fabricated-provenance claim. The Register asserts an emitted four-field record that the delivered document does not contain.

**Impact on fair value:** None arithmetically. It voids the Register's central guarantee on the study's most load-bearing input.

**Correct method:** Emit C.3 with the copper and Fed records.

---

### F6 — TOTAL FAIL · Disclosure · Register §B, §D, §C.5

**Item:** The Source Register publishes a materially different model from the one delivered.

**What the report says (Register §D, "Numbers that are judgments, not observations" — "the rows a reader should attack first"):**

| Register §D | Delivered model | Δ |
|---|---|---|
| EBITDA margin path **13% → 19%** | 4.1% → 12.3% | gross |
| NWC intensity **108% → 88%** | 112% → 88% | 4pp |
| Net debt FY25 anchor **EGP 8,800 mn** | **9,805** (8,805 is the *bull* column) | **1,005 mn** |
| Kd path **23.5% → 15.5%** | **22.0%** → 15.5% | 150bp |
| Capex **1.6% of revenue** | 2.21% → 1.74%, built on EGP 9k/tonne | — |

Register §B adds: "Peer financials … SWDY P/E 10.4× / EV-EBITDA ~6×; Riyadh Cables 18×/15×", and §C.5 `ev_ebitda_base` / `pe_norm` cite the same superseded figures.

**What is correct:** Study §1.3 and §1.4 state, verbatim: "the 10.4×/6.0× aggregator prints previously carried here **did not reproduce from the filing and have been replaced**" — by 11.3× and 7.1×; Riyadh Cables is carried at 14.3× / 12.5×.

**Why it failed:** §D contradicts §C.5 *of the same document* and the study on five of eight rows. These are superseded-draft artefacts presented as a computed record — precisely the case of a subsidiary table implying a central the report no longer publishes. A reader attacking "the rows a reader should attack first" attacks a model that does not exist.

**Impact on fair value:** Roughly ±EGP 0.30/share of stated anchor error placed in the reader's hands; the 19% terminal margin implies a far more valuable company than the study publishes.

**Correct method:** Regenerate §D and §B from the live assumption layer.

---

### F7 — PARTIAL FAIL (materially, the study's central defect) · Construction / Disclosure · §1.5

**Item:** 95.8% of the headline central comes from two lenses that assume the balance sheet has already been repaired.

**What the report says:** "Weighted central EGP 0.34"; "Blend 40 / 20 / 20 / 20"; "The DCF carries the heaviest weight because it is the only lens that prices the working-capital problem explicitly."

**What is correct (recomputed):**

| Lens | Weight | Base | Contribution | Share of central |
|---|---|---|---|---|
| FCFF DCF (floored) | 40% | 0.01 | 0.004 | **1.2%** |
| Relative (clamped) | 20% | 0.05 | 0.010 | 3.0% |
| Normalized earnings | 20% | 0.70 | 0.140 | 41.7% |
| Book / replacement | 20% | 0.91 | 0.182 | **54.2%** |
| **Weighted central** | | | **0.3360** | |

Lenses pricing the actual balance sheet: **4.2%.** Lenses assuming it repaired: **95.8%.**

The normalized lens charges interest on a **hardcoded 6,000** net debt (`'Relative & Normalized'!C7`) against the model's own FY28E net debt of **16,045**. On the model's own balance sheet that lens is **−1.59**, not +0.70.

**Why it failed:** The blend mixes a state of the world in which the debt is unpayable with one in which it has been repaid, and headlines a number that no lens produces and no coherent state of the world produces. Each conditionality is disclosed in passing; the arithmetic consequence — that the declared "primary lens" contributes 1.2% of the answer — is not.

**Impact on fair value:** The whole headline. The "−85% vs spot" is not a measurement of the security as it exists.

**Correct method:** Publish the disagreement and say which lens the answer is, per the report's own §1.5 framing.

---

### F8 — PARTIAL FAIL · Construction · §1.2, §1.5

**Item:** Book value weighted into the central, and it is the largest single contributor.

**What the report says:** Book / replacement 0.91, weight 20%; "the book lens anchors the downside."

**What is correct:** Book value is a disclosed floor, published as such, and never weighted into a central. Recomputed, it is **54.2%** of the 0.336 central. Ex-book, the central is **0.193**.

**Impact on fair value:** +0.14/share on the headline — roughly 42% of it.

**Correct method:** Publish as a floor beside the football field.

---

### F9 — PARTIAL FAIL · Construction · §1.2

**Item:** The book lens discounts today's 240%-geared book at the *terminal, deleveraged* cost of equity.

**What the report says:** "against a ~17.3% normalised cost of equity and 5% growth, the justified multiple is (ROE−g)/(Ke−g) ≈ 0.73× book."

**What is correct:** 17.25% is `Assumptions!B23`, the **terminal** Ke — built on rf 10.5%, ERP 7.0% and a 60/40 capital structure that presupposes the deleveraging. The explicit-window Ke printed beside it is **27.98%**.

At 27.98%: justified P/B = (0.14 − 0.05)/(0.2798 − 0.05) = **0.392×**, fair value **0.485**, not 0.909.

**Why it failed:** The Ke choice is never disclosed as the terminal one. The lens is worth **0.43/share** on this single choice — **0.085 on the central, a quarter of the headline** — larger than the entire beta grid, and it is not gridded anywhere.

**Impact on fair value:** Central 0.34 → approximately **0.255** on this correction alone.

**Correct method:** Discount the current book at the current cost of equity, or state that the lens is a post-recapitalisation value and sensitise the Ke.

---

### F10 — PARTIAL FAIL · Input · §1.2, §1.1 bridge

**Item:** The book lens and the bridge ignore the disclosed 1Q26 loss (and now H1).

**What is correct:** BVPS = 4,100 ÷ 3,313.5 = **1.2373**. Net of the disclosed 1Q26 loss of 241.6: **1.1767**, base fair value **0.865**. Net of the disclosed H1 loss of 200.8: **1.1767**, same. The bridge likewise stands on a FY25 balance sheet with two disclosed loss-making quarters since.

**Impact on fair value:** −0.009 on the central; −0.045 on the lens. Immaterial alone; compounds with F9.

---

### F11 — PARTIAL FAIL · Logic · §1.2 book-lens table

**Item:** A printed row does not reproduce.

**What the report says:** Bull justified P/B **1.16×**; bull fair value 1.31.

**What is correct:** (0.18 − 0.05) ÷ (0.17248 − 0.05) = **1.061×**. And 1.061 × 1.2373 = 1.313 ✓ — **the fair value is right and the printed multiple is wrong.** 1.16 × 1.2373 = 1.438, a figure that appears nowhere.

**Impact on fair value:** Zero. A printed table a reader cannot reproduce.

---

### F12 — PARTIAL FAIL · Disclosure · §1.9

**Item:** Self-contradiction on the terminal return on capital.

**What the report says:** §1.9 grid note — "because the terminal return on capital (**10.3%**) sits below the terminal cost of capital (15.0%)." Everywhere else in the study and workbook: **9.2%**.

**What is correct:** 9.171%. The 10.3% reproduces from nothing in the model.

---

### F13 — PARTIAL FAIL · Construction · §1.8

**Item:** The terminal beta is not relevered for the deleveraging the terminal weights assume.

**What the report says:** Terminal Ke = 10.5 + **0.964** × 7.0 = 17.25%, printed beside terminal weights of 60/40, while the explicit window runs 41/59. The construction is never named.

**What is correct:** Unlevering at D/E 1.439, t = 22.5%: βu = 0.456. Relevered at D/E 0.667: **βL = 0.691**. Terminal Ke = **15.34%**, terminal WACC ≈ **13.85%**, not 15.00%.

**Impact on fair value:** TV ≈ 8,079 vs 7,150; EV +≈400; unfloored DCF −1.81 → ≈ −1.69. Direction of the unstated construction: **bearish**.

**Correct method:** State whether the terminal beta is the same or a relevered one, and give the leverage and tax rate that produce it. (Pass 3 requires exactly this.)

---

### F14 — PARTIAL FAIL · Construction · §1.6, Appendix A.1, Segments sheet

**Item:** The conversion-EBITDA-per-tonne "history" is back-solved through assumed finance costs, not observed.

**What the report says:** "The decomposition's central finding: the revenue collapse is a VOLUME collapse … and conversion EBITDA per tonne collapsed with it (146 → 11 k EGP/t)" — presented as an implied *history* calibrated on disclosed anchors.

**What is correct (traced through the workbook):**

```
FY25 EBITDA 2,871.294 = EBIT 2,795.561 + D&A 75.733
     EBIT 2,795.561 = EBT 645.561 + ASSUMED finance 2,150
     EBT   645.561 = reported NP 500.31 ÷ 0.775
     conversion/t   = 2,871.294 ÷ 15.8 = 182   ← back-solved
```

FY23 is identical (assumed finance 990 → 111 k/t). The Register concedes it: `fin_cost_fy25_est` — "closes FY25 P&L to the reported NP."

**Of the four calibration anchors, only FY24's 146 has an external source, and that source is a single aggregator's EBITDA print (Investing.com, flagged "(a)"). Only the Q1-26 trough of 11 rests on a disclosed line (operating profit 1.429).**

**Why it failed:** EBITDA and the finance cost are two unknowns solved from one equation, with the finance cost taken as an assumed rate × the debt the same exercise is trying to establish. The "collapse from 146 to 11" compares an assumption against an observation.

**Impact on fair value:** The entire mid-cycle margin judgment — the study's own §1.7 "SECOND" crux, worth ±0.48/share per 15% shift — rests on this series.

---

### F15 — PARTIAL FAIL · Logic · §1.8, Register `kd_eff_fy25`

**Item:** The cost-of-debt cross-check is circular.

**What the report says:** "Kd 22.0% — Corridor + credit margin; checked against effective rates 23.5% (FY24) and 22.1% (FY25, on the triangulated debt path) — inside 150bp."

**What is correct:** The FY25 numerator (2,150) was back-solved to close the P&L (F14), then divided by the debt path the same triangulation produced. The check tests the assumption against itself. The denominator is correctly the interest-bearing book, not broad liabilities — that part passes. FY24's 23.5% is genuinely independent (coverage 2.0×, from an aggregator).

The Register separately flags that the Q1-26 P&L implies **~243/qtr** of net finance — under a fifth of the modelled 539/qtr — "unexplained without the statements (possible FX/interest income offset or capitalised financing); flagged, does not change the marginal rate."

**Impact on fair value:** That flagged anomaly is load-bearing and under-weighted. At ~972/yr rather than 2,157/yr, either the debt or the rate is materially smaller than modelled, and **cross-check B of the net-debt triangulation — which takes interest 2,150 as an input — fails with it.**

---

### F16 — PARTIAL FAIL · Construction · Register `net_debt_fy25_est`

**Item:** The load-bearing step of the net-debt triangulation is assertion, and the "skewed adverse" claim is one-sided.

**What the report says:** Non-debt liabilities "FY24's 2,410 scaled with purchase value, −21.5%" → 1,890; and "the residual risk on this anchor is SKEWED ADVERSE."

**What is correct:** The step scales payables **down 21.5%** in the same year the working capital they fund grew **+16.6%** (10,500 → 12,245) — asserting that suppliers withdrew credit while the company's working capital ballooned. The stated justification ("thin payables consistent with LC/bank-financed copper imports") is an assertion, not evidence.

- Held flat at 2,410 → drawn debt 9,950, net debt **9,285**
- Scaled *with* the WC build (×1.166 → 2,810) → drawn 9,550, net **8,885**

**Why it failed:** The defensible range is roughly **8,885–10,465**, wider and lower-skewed than the stated 9,120–10,360. The skew claim counts only readings above the base and ignores the one assumption that could move it down.

**Impact on fair value:** ±0.28/share unfloored at the low end, plus the cascade through every forecast year's interest line.

---

### F17 — PARTIAL FAIL · Construction / Disclosure · §1.6, `Assumptions!B46`

**Item:** D&A is driven off revenue at double the historical ratio — hence off copper and FX.

**What the report says:** D&A printed as a currency line (132 → 228). The study never states the driver.

**What is correct:** `Segments!E17 = revenue × 1.3%`. Historical: FY24 90 ÷ 13,778 = **0.65%**; FY25 76 ÷ 10,819 = 0.70%. The Register concedes: "~0.7%; forecast set at 1.3% of revenue to fund modest PP&E renewal."

**Why it failed:** Depreciation rising because copper rose is not a mechanism — D&A should follow gross PP&E, not the commodity. Doubling it cuts NOPAT, cuts terminal ROIC and raises the reinvestment burden.

**Impact on fair value:** At the historical 0.7%, FY30 NOPAT 1,586 → ROIC 9.71% → TV ≈ 8,077 → **+0.28/share unfloored**. Direction: bearish.

---

### F18 — PARTIAL FAIL · Construction · §1.6, `Assumptions!B43`

**Item:** The currency path is hand-set, not derived from the inflation differential.

**What the report says:** "EGP/USD (~3%/yr crawl)"; Register — "the inflation differential narrows as the CBE targets bite … far below PPP catch-up."

**What is correct:** The study's own §1.8 states inflation 14.3% (Jun-26), target 7±2pp Q4-26, 5±2pp Q4-28, against US inflation ~2.5%. The implied differential runs ≈11pp / 5pp / 3pp / 2.5pp; the modelled path runs 3.17% / 2.88% / 2.80% / 2.73%. **By FY30 the modelled pound is ~9% stronger than the study's own inflation path implies.**

**Why it failed:** Pass 5 — one path, derived, not typed. The Register's own wording concedes the departure.

---

### F19 — PARTIAL FAIL · Construction · §1.6, §5

**Item:** Copper enters the cost side only, so a record-high flat anchor is presented as "no view" while being, inside this construction, maximally adverse.

**What the report says:** "Copper is anchored FLAT AT THE CURRENT MARKET (~$14,000/t, 3–4 Aug LME cash) — a 'no view' forecast must anchor on the tape."

**What is correct:** Price per tonne = copper × FX × 1.387 drives revenue and, because NWC is set as a percentage **of revenue**, the entire working-capital load. But **EBITDA = volume × a conversion margin typed in EGP per tonne, independent of copper.** Higher copper therefore raises the capital the model must fund with *zero* P&L offset — no inventory gain, no pass-through margin. Lower copper is unambiguously better; higher unambiguously worse.

**Why it failed:** This one-sided specification is the mechanism that produces the negative equity, and it is labelled a neutral anchor. The study's own words — "copper strength therefore inflates the working capital the model must fund, which is exactly the mechanism the tonnage build exists to price" — state the asymmetry without naming it as a choice.

**Impact on fair value:** Large. The −10% copper column is worth roughly +0.5/share unfloored through the invested-capital / ROIC channel alone.

**Also (Input, minor):** LME cash settled **$14,545/t on 14 August 2026** (record); the flat $14,000 anchor is now ~4% stale. Separately, the Register's own primary-document row reads "**LME ~$12.8k avg**" — the Register does not contain the value the model uses.

---

### F20 — PARTIAL FAIL · Construction · §1.6, READ FIRST (both documents)

**Item:** "Margins are OUTPUTS, not assumptions" is not what the build does.

**What the report says:** Study §1.6 and workbook READ FIRST, verbatim: "Margins are OUTPUTS of this build, not assumptions."

**What is correct:** `EBITDA = volume × Assumptions!C44:G44`, where C44:G44 = 40, 90, 115, 128, 135 — **a typed contribution margin in EGP per tonne.** No direct cost line is built: not copper, not wages, not conversion energy, not imported components, each on its own driver with its own escalator, with margin as the residual. The EBITDA *percentage* is an output of two typed inputs; the margin itself is an input in per-unit clothing.

**Why it failed:** Pass 6 — the declared construction and the practice differ on the study's headline methodological claim.

---

### F21 — PARTIAL FAIL · Construction / Disclosure · §1.3, §1.5

**Item:** A clamped lens carried as a range and weighted into the central.

**What the report says:** Relative bear / base / bull = **0.05 / 0.05 / 0.05** at 4.5× / 5.5× / 6.5×; "the lens is shown floored at EGP 0.05."

**What is correct (recomputed unfloored):** 4.5× → **−1.52**/share; 5.5× → −1.52; 6.5× → **−1.20**. Every cell is clamped. The 20% weight contributes a constant 0.010 to all three scenarios, and the published bear–bull span of 0.18–0.95 rests partly on a number that never moves.

**Impact on fair value:** Structural rather than numeric — but the "range" carries less information than it appears to.

---

### F22 — PARTIAL FAIL · Disclosure / Logic · §1.1, §1.3, C.2, C.3

**Item:** Four unreconciled prices for the same limited-liability option, and a waterfall that does not reach its printed answer.

**What is correct:** The same option is carried at **0.01** (DCF — a hardcoded `MAX(...,0.01)` in `SOTP Bridge!B11` and `DCF!B33`), **0.05** (relative), **0.10** (Expert 3) and **0.11** (Expert 2). No construction is given for any of them, and the 0.01 carries 40% weight.

Separately, the §1.1 bridge prints "Equity value — floored at zero (limited liability) | **0**" and then "per share (3,313.5 mn shares) | **EGP 0.01**". 0 ÷ 3,313.5 = 0.00. **Following the table's own instructions literally does not arrive where the page says.**

---

### F23 — PARTIAL FAIL · Construction · §1.1, §1.8

**Item:** The explicit window ends mid-recovery, then capitalises 5%.

**What is correct (recomputed):** FY30E revenue growth **+11.1%**, EBITDA growth **+14.0%**, utilization 64% and still climbing, conversion EBITDA/t still ramping (128 → 135). The terminal capitalises a steady state the model never reaches.

**Impact on fair value:** Bearish — terminal NOPAT is a still-ramping year.

**Correct method:** Extend the explicit window to convergence, or state the gap.

---

### F24 — PARTIAL FAIL · Disclosure · §1.1, Pass-4 requirements

**Item:** Three mandated terminal disclosures are absent.

**(a) Implied asset life is never computed.** Under the reinvestment identity the terminal charges g × invested capital every year forever, so the implied replacement cycle is the reciprocal of the growth rate: **1/g = 20.0 years**. That is a fact about the assumed 5% currency, not about a cable plant — at 7% it would be 14.3 years and at 2% it would be 50, for the same kilns. **No disclosed useful life is available** (audited statements unreachable), so the comparison cannot be closed — logged **UNVERIFIABLE** — but the computation is owed and absent.

**(b) Maintenance capex rests on an analyst-chosen norm, not a disclosed life.** "~EGP 9k per tonne of capacity (25 kt), escalated ~8%/yr". The Register concedes "no disclosed capex any year (flagged gap)." It is also struck on 25 kt the study elsewhere states is **parent-only**, while the model runs 10–16 kt of volume.

**(c) The terminal's return on capital is never compared with the company's filed returns.** Recomputed FY24: NOPAT 2,635 on invested capital ≈11,732 = **≈22.5%**, against a terminal 9.2%. The gap is argued thematically (the windfall thesis) but never measured.

---

### F25 — PARTIAL FAIL · Construction · §1.8, `Assumptions!B18` / `B28`

**Item:** Cash is charged for inconsistently between the WACC and the bridge.

**What is correct:** The weights use **gross** drawn debt 10,465 (E/D = 40.95 / 59.05); the bridge deducts **net** debt 9,805. On net debt the equity weight is 42.5% and the WACC 21.69%, not 21.53%.

**Impact on fair value:** ≈16bp on the explicit WACC — immaterial, but it is the two-conventions-in-one-model pattern.

---

### F26 — PARTIAL FAIL · Construction · §1.8, A.2

**Item:** The terminal capital structure contradicts the model's own forecast.

**What the report says:** Terminal weights 60/40 — "The steady state presupposes deleveraging; today's ~60% distress weight into perpetuity would be circular … Conservative direction: more weight on the dearer equity leg."

**What is correct:** The same workbook's A.2 shows FY30E net debt **19,602** against equity **−2,078** (ND/E −943%). The model forecasts the opposite of the structure its terminal assumes. The circularity objection to market-value weights is sound; the resolution is never reconciled to the model's own path.

---

### F27 — PARTIAL FAIL · Logic · Discount convention

**Item:** No stub-period adjustment from a 5 August 2026 valuation date.

**What is correct:** FY26E is discounted a **full year** (0.8229) from a date seven months into FY26, and every later year inherits the shift — while the FY26E working-capital release of 845 mn is largely historical by the valuation date and its Q1/Q2 outturn is disclosed.

**Impact on fair value:** PV understated ≈13%; EV +≈500, **+0.15/share unfloored**. Direction: bearish. Does not change the floored conclusion.

---

### F28 — PARTIAL FAIL · Disclosure · Workbook vs document

**Item:** Figures that differ between the workbook and the study.

| Cell | Workbook | Study | Recomputed |
|---|---|---|---|
| `Peer & Sector!D8` ELEC EV/EBITDA | ~5.3× FY25e | ~5.9× | **5.94×** — the workbook is stale |
| `Peer & Sector!C8` ELEC P/E | 14.6× | 14.5× | **14.50×** |
| `Balance Sheet!B11` FY24 net debt | **9,805** (hardcoded — the FY25 value) | **8,132** (A.2, §1.6) | 8,960 − 828 = **8,132** |

The FY24 hardcode also propagates a non-debt-liabilities plug of 745 in the workbook against the study's own 2,410 in §1.6.

---

### F29 — PARTIAL FAIL · Logic · `Income Statement!F13:I13`

**Item:** Latent formula error — the loss-carryforward offset references the wrong prior-year column.

**What is correct:** F13 references `C12` (FY24 — empty); G13 → `D12` (FY25 — empty); H13 → `E12`; I13 → `F12`. They should reference E12 / F12 / G12 / H12. **The offset is two columns out.**

**Impact on fair value:** Dormant in the base case — cumulative EBT is negative in every forecast year, so `MAX(0,·)` = 0 and the tax is zero regardless. It bites in any scenario where the company turns profitable, which is precisely the re-run the workbook invites ("change one and the whole model reprices").

---

### F30 — PARTIAL FAIL · Disclosure · Sensitivity & Monte Carlo sheets

**Item:** The grids are hardcoded, so the live base cell and the dead grids can silently diverge.

**What is correct:** Only `Sensitivity!B5` links to the DCF. All 25 margin/NWC cells, both WACC grids, the ROIC grid, the beta grid and every Monte Carlo output are pasted values. The sheet discloses "engine outputs," but the workbook's front page promises: "change one (volumes, copper, the EGP path, conversion EBITDA per tonne, the working-capital intensity, the net-debt anchor) and the whole model reprices."

**Note in the report's favour:** five grid cells were verified by full independent recomputation and reconcile **exactly** (Section C.6). The grids are correct — just not live.

---

### F31 — PARTIAL FAIL · Disclosure · Appendix A.3

**Item:** Two definitions of operating cash flow in one row.

**What is correct:** FY26E "Operating cash flow **+1,198** (release)" = FCFF 973 + capex 225 — an **unlevered, fully-taxed, pre-capex** figure. It sits in the same row as FY25's "~+690 pre-finance / ~−1,460 after finance," which is levered. The workbook's actual FY26E operating-minus-investing line is **−1,121**.

---

### F32 — PARTIAL FAIL · Disclosure · Headline prose and cone labelling

**(a)** "revenue rose **52%** then 59%" — the 59% checks (13,778 ÷ 8,673 = +58.9%); the 52% requires FY22 revenue, which appears in **no table in any of the three documents**.

**(b)** Headline sentence: "our weighted central estimate sits roughly 85% below the price of EGP 0.34" — reads as though 0.34 were the price. (The −84.5% itself checks.)

**(c)** The 1-month cone: implied σ from p5/p95 under the stated Student-t(6) is **33.3%**, against the label "≈37% effective". The 3-month cone reconciles at **36.9%** ✓.

---

### F33 — PARTIAL FAIL · Input / Sourcing

**(a)** The risk-free 22.31% is an **investing.com** print — an aggregator — for a figure the Ministry of Finance and the CBE publish. The Register itself concedes the credible early-August band is **22.3–23.0%** and that "the print sits at the LOW edge, worth ~−0.10/sh unfloored if the top of the band is right." Direction: **anti-thesis** (a lower rate raises value).

**(b)** The Register mislabels `sov_spread_rating 0.0637` as Damodaran's "**adjusted** default spread, rating basis." The original file's adjusted spread / country risk premium for Egypt is **9.71%**; 6.37% is the unadjusted Caa1 default spread. Right number, wrong label.

**(c)** SWDY FY25 net profit: study says **17.3 bn**; reported **17,461 mn**. P/E 11.3× against **11.22×** recomputed. Immaterial.

---

### F34 — FLAG (not a failure) · Pass 11 · Direction of the contested judgements

**Count: approximately 15 of 17 judgements worth more than ~5% of value are resolved the same way.**

**Bearish (15):** conversion margin below FY24 in nominal terms; copper flat at a record with no P&L offset (F19); FX crawl below the implied differential (F18); terminal beta unrelevered (F13); terminal weights "conservative direction: more weight on the dearer equity leg"; terminal ROIC 9.2% against ~22.5% filed; window ends mid-ramp (F23); D&A at twice the historical ratio (F17); the full 22.5% tax charged in every loss year (the study prices the forgone NOL shield at 0.1–0.2/share and takes it anyway); justified P/E 6.5× "held deliberately deep" against an 11.3× peer; EV/EBITDA at an 8–36% discount; sustainable ROE 14% against 35% prints; two clamped lenses carrying 60% of the weight; no stub discounting (F27); the net-debt base placed in the upper half of a one-sidedly-stated range (F16).

**Anti-thesis (2):** the risk-free print taken at the low edge of its band (F33a); the book lens ignoring the Q1 and H1 losses (F10).

**Why this matters:** every bearish choice here is labelled "conservative." In a report whose conclusion *is* bearish, a conservative assumption is one that pushes value **up**. The study has inverted the word throughout, and nowhere counts the direction. This is a flag, not a failure — a company with negative operating cash flow, 240% gearing and a collapsed quarter can genuinely deserve a consistent read.

---

### F35 — PARTIAL FAIL · Disclosure · Pass 11

**Item:** The reverse read is never solved.

**What is correct:** At EGP 2.19 the market pays equity of 7,257 → implied EV **17,062**, against a base EV of 3,813 — the price requires **4.5×** the modelled enterprise. The study's own best company-grid cell (+30% conversion, 76% NWC) reaches EV ≈8,600.

**Assessment:** The study's directional claim therefore survives its own reverse read; the omission is disclosure, not substance — but a reader cannot see that without doing the arithmetic themselves.

---

## Section C — Arithmetic Reconciliation Appendix

*Every figure below was recomputed independently from the stated inputs before reading the report's answer. Lines that matched are included, as required.*

### C.1 Cost of capital — all lines match

| Line | Recomputed | Report | Δ |
|---|---|---|---|
| rf* = 22.31 − 3.40 | 18.9100% | 18.91% | — |
| Damodaran file vintage | "Last updated January 5, 2026" | Jan-2026 | ✓ |
| CDS default spread (original file) | **3.41%** | 3.40% | +1bp ✓ |
| Rating-based total ERP (original file) | **13.94%** | 13.94% | **exact ✓** |
| CDS-based ERP, derived from the file: (13.94 − 9.71) + 3.41 × (9.71/6.37) | **9.428%** | 9.41% | +2bp ✓ |
| Ke = 18.91 + 0.964 × 9.41 | 27.9812% | 27.98% | — |
| Market cap = 2.19 × 3,313.5406 | 7,256.7 | ~7.3 bn | ✓ |
| Equity weight = 7,256.7 / (7,256.7 + 10,465) | 40.948% | 41% | — |
| WACC explicit = 0.4095 × 27.98 + 0.5905 × 17.05 | **21.5261%** | 21.53% | — |
| Ke terminal = 10.5 + 0.964 × 7.0 | 17.2480% | ~17.3% | — |
| WACC terminal = 0.6 × 17.248 + 0.4 × 11.625 | **14.9988%** | 15.00% | — |
| Share count: 662,708,074.60 ÷ 0.20 par | **3,313,540,373** | 3,313.540373 mn | **foots ✓** |
| Share count vs disclosed H1-26 LPS: 200.833 / 3,313.5 | **0.0606** | disclosed 0.06 | **third confirmation ✓** |

**Country risk is counted exactly once, correctly.** The report strips Damodaran's *own* CDS spread from the local yield and adds Damodaran's *own* CDS-based ERP — same basis, same vintage. This is the construction Pass 3 demands, and it verifies against the original file to two basis points. **PASS.**

### C.2 Cash-flow waterfall and discount factors — all lines match

| | FY26E | FY27E | FY28E | FY29E | FY30E |
|---|---|---|---|---|---|
| Revenue recomputed (vol × Cu × FX × 1.387) | 10,178.1 | 12,015.9 | 13,920.8 | 15,806.3 | 17,553.9 |
| *report* | 10,178 | 12,016 | 13,921 | 15,806 | 17,554 |
| EBITDA = volume × conversion/t | 416.0 | 1,071.0 | 1,541.0 | 1,894.4 | 2,160.0 |
| − D&A = revenue × 1.3% | (132.3) | (156.2) | (181.0) | (205.5) | (228.2) |
| EBIT | 283.7 | 914.8 | 1,360.0 | 1,688.9 | 1,931.8 |
| NOPAT = EBIT × 0.775 | 219.9 | 709.0 | 1,054.0 | 1,308.9 | 1,497.1 |
| + D&A | 132.3 | 156.2 | 181.0 | 205.5 | 228.2 |
| − Capex | (225) | (243) | (262) | (283) | (306) |
| − Δ working capital | +845.5 | (1,337.3) | (1,184.0) | (937.1) | (589.5) |
| **FCFF recomputed** | **972.7** | **(715.1)** | **(211.0)** | **294.3** | **829.8** |
| *report* | 973 | (715) | (211) | 294 | 830 |
| Forward WACC | 21.5261% | 19.5177% | 18.0114% | 16.3043% | 14.9988% |
| Cumulative discount factor | 0.8229 | 0.6885 | 0.5834 | 0.5016 | 0.4362 |
| **PV recomputed** | **800.4** | **(492.4)** | **(123.1)** | **147.6** | **362.0** |
| *report* | 800 | (492) | (123) | 148 | 362 |

Σ PV explicit = **694.5** (report 695).

Glide-fraction construction verified: `(0.22 − Kd_yr) / (0.22 − 0.155)` → 0%, 30.8%, 53.8%, 80.0%, 100% — matching the printed 0 / 31 / 54 / 80 / 100%. **All lines PASS.** The terminal is discounted at the identical year-5 factor (0.4362) — one date, one price of time, with no relabelling. **PASS.**

### C.3 Terminal value, and the implied asset life

| | Report's construction | Model's own balance sheet | Δ |
|---|---|---|---|
| Terminal NOPAT (FY30 × 1.05) | 1,572.0 | 1,572.0 | — |
| Invested capital | **16,325** (NWC 15,447 + 5%×rev 878) | **19,523** (NWC 15,447 + PP&E 1,096 + other 2,980) | **−3,198** |
| Terminal ROIC | **9.171%** | **7.669%** | −150bp |
| Reinvestment rate = g / ROIC | 54.52% | 65.20% | +10.7pp |
| Terminal FCFF = NOPAT × (1+g) × (1−RR) | **715** | **547** | −168 |
| Terminal value | **7,150** ✓ report | **5,471** | −1,679 |
| PV of terminal value | **3,119** ✓ report | 2,386 | −733 |
| Enterprise value | **3,813** ✓ report | **3,081** | **−733 (−19%)** |
| TV as % of EV | **81.8%** ✓ report 82% | 77.5% | — |
| Unfloored per share | **−1.81** ✓ report | **−2.03** | −0.22 |

The report's own §1.9 ROIC grid carries 7.7% → TV 5,513 → **−2.02**; my −2.03 reproduces it. **The correct denominator is already in the report, labelled a downside sensitivity.** (F3)

**Implied asset life.** Under the reinvestment identity the implied replacement cycle is **1/g = 20.0 years** — a fact about the assumed 5% currency, not about the asset. No disclosed useful life is available (audited statements unreachable), so the comparison Pass 4 requires cannot be closed: logged **UNVERIFIABLE**. The report never computes the 20 years at all.

Terminal net reinvestment steps up from FY30's 44.6% of NOPAT (capex 306 + ΔWC 590 − D&A 228 = 667) to 54.5% — a definitional step-change at the boundary, correctly applied but unremarked.

**One FCF definition? PASS.** The explicit window builds NOPAT + D&A − capex − ΔWC; the terminal uses NOPAT × (1−RR), which is the same definition in identity form (reinvestment = capex + ΔWC − D&A). No second, undisclosed definition hides in the place holding most of the value.

### C.4 Enterprise-to-equity bridge — foots

| Line | Recomputed | Report |
|---|---|---|
| Σ PV explicit FCFF | 694.5 | 695 |
| + PV of terminal value | 3,119 | 3,119 |
| = Enterprise value | 3,813 | 3,813 |
| − Net debt (FY25, triangulated) | (9,805) | (9,805) |
| − Non-controlling interests | (0) | (0) |
| = Equity value, intrinsic | **(5,992)** ✓ | (5,992) |
| ÷ 3,313.5 mn shares | **−1.808** | *not printed* |
| Equity floored at zero | 0 | 0 |
| **Printed per share** | **0.00** | **EGP 0.01** ✗ (F22) |

The bridge lines sum correctly and divide correctly to the unfloored per-share figure. NCI at zero is supported by the Register's note (consolidated-versus-attributable gap ~1.1 mn FY25), a reasonable inference — **PASS**, though the study prints the zero without the reasoning. But the bridge stands on a FY25 balance sheet with two disclosed loss-making quarters since (F10), and the last two printed lines do not follow from the lines above them (F22).

### C.5 Weighted central — foots, and decomposes badly

| Lens | Weight | Base | Contribution | Share of central |
|---|---|---|---|---|
| FCFF DCF | 40% | 0.01 | 0.004 | 1.2% |
| Relative (clamped) | 20% | 0.05 | 0.010 | 3.0% |
| Normalized (net debt assumed 6,000 vs the model's 16,045) | 20% | 0.70 | 0.140 | 41.7% |
| Book (terminal Ke on a 240%-geared book) | 20% | 0.91 | 0.182 | **54.2%** |
| **Weighted central** | | | **0.3360** ✓ report 0.34 | |

Bear 0.184 ✓ (printed 0.18) and bull 0.948 ✓ (printed 0.95) also foot.

**Lenses pricing the actual balance sheet: 4.2%. Lenses assuming it repaired: 95.8%.** Ex-book central **0.193**; book lens re-struck on the explicit-window Ke → central **≈0.255**.

### C.6 Sensitivity grids — verified live; five cells recomputed in full

| Cell | Full independent recomputation | Printed |
|---|---|---|
| Terminal WACC 15% × g 3% (RR 32.6%, TV 8,661, EV 4,471) | **−1.61** | −1.61 ✓ |
| Terminal WACC 15% × g 7% (RR 76.1%, TV 4,788, EV 2,783) | **−2.12** | −2.13 ✓ |
| Terminal WACC 13% × g 5% — **whole glide re-computed**, cumulative DF 0.4549 | **−1.51** | −1.51 ✓ |
| Conversion −30% × NWC 88% (ROIC 6.10%, RR 82.0%, TV 1,881, EV 615) | **−2.77** | −2.77 ✓ |
| Conversion +15% × NWC 88% (ROIC 10.71%, RR 46.7%, TV 9,783, EV 5,410) | **−1.33** | −1.33 ✓ |

The company grid is perfectly bilinear across all 25 cells (+0.48 per conversion step, +0.24 per NWC step), which is the classic signature of a grid built by adding two independent per-unit deltas rather than recomputing the model in each cell.

**The check fired on correct work, so the check was re-pointed, not widened.** The grid genuinely re-derives terminal ROIC in every cell and re-glides the entire discount schedule; the linearity is a real property of the functional form over this range. **PASS — and a strength. The stated specification is the one performed.**

### C.7 Monte Carlo — reconciles to its own label

| Check | Recomputed | Stated |
|---|---|---|
| 3-month implied σ from p5/p95 under standardized t(6), z = 1.586 | **36.9%** | "≈37% effective" ✓ |
| 1-month implied σ, same basis | **33.3%** | same 37% label ✗ (F32c) |
| 3-month median move | +4.57% | +4.7% ✓ |
| Carry over 3m: 1.195^0.25 − 1 | **+4.55%** | drift = 19.50% carry ✓ |
| P(above spot), log-interpolated from p25/p50 | **60.6%** | 61% (engine 0.6135) ✓ |
| P(+10%) | 38.3% | 37% ✓ |
| Odds ratio 37 / 18 | 2.06 | 2.1 : 1 ✓ |
| Zone probabilities sum | 100.0% | ✓ |
| Percentile monotonicity, both horizons | ✓ | ✓ |
| Median sits inside the stated ranges | ✓ | ✓ |
| Touch ladder vs terminal percentiles (reflection-consistent) | ✓ | ✓ |
| MACD histogram = line − signal: 0.011 − 0.015 | **−0.004** ✓ | −0.004 |
| Support 2.05 / 1.90 below and resistance 2.40 / 2.80 above the stated close of 2.19 | ✓ | no impossible ladder |
| Lens independence: drift is carry-only, no fair-value coupling | ✓ | explicitly stated |

**Section 3 is the strongest part of the study.** The cone reconciles to its stated distribution and its stated drift; the lenses are genuinely uncoupled; the walk-forward test is disclosed with its skill score and its coverage p-value.

### C.8 H1-2026 against the study's first forecast year

| | Study FY26E | H1-2026 actual (disclosed) | Implied H2 requirement |
|---|---|---|---|
| Revenue | 10,178 | **4,329** (annualised 8,658, −14.9%) | 5,849 (+35% on H1) |
| Net profit | **(1,873)** | **(200.8)** (annualised −402) | **(1,672)** |
| Q1 / Q2 revenue | — | 2,094 / **2,235** | — |
| Q1 / Q2 net profit | — | (241.6) / **+40.8** | — |
| YoY revenue | — | Q1 −43.8% → **Q2 −17.7%** | — |
| Q2 implied volume @ $13.5k / EGP 50 | driver 10.4 kt/yr | **2.39 kt → 9.55 kt/yr** | — |
| Q2 implied conversion EBITDA/t | driver 40 k; checkpoint ~50 k | **131–255 k** | — |

*The conversion-per-tonne band is bounded by the two available readings of the quarterly finance line: the register-flagged ~243/qtr implied by the Q1-26 P&L, and the study's own modelled 539/qtr. The quarterly finance split is not disclosed, so the reconstruction is bounded rather than point-estimated — but both bounds sit above the study's stated checkpoint.*

---

## Section D — Construction Register

*What the report declares, against what it actually does. Most serious findings live in the gap.*

| | **Declares** | **Actually does** | **Agree?** |
|---|---|---|---|
| **Primary lens & the others** | "FCFF DCF (primary)", 40% weight, "the anchor … the only lens that prices the working-capital problem explicitly" | The DCF contributes **1.2%** of the headline. 95.8% comes from the normalized and book lenses, both of which assume the debt problem away — the normalized one via a **hardcoded 6,000** net debt against the model's own 16,045 | ✗ **F7** |
| **Margins** | "Margins are OUTPUTS of this build, not assumptions" (study §1.6 *and* workbook READ FIRST) | EBITDA = volume × a **typed EGP-per-tonne contribution margin**. No direct cost line is built on its own driver with its own escalator | ✗ **F20** |
| **Terminal construction** | "ROIC-consistent: 9.2% ROIC × 55% reinvestment" | ROIC = NOPAT ÷ (**NWC + 5% of revenue**) — a denominator stated nowhere, 16% smaller than the workbook's own invested capital. Correct denominator → ROIC 7.67%, EV −19%. The right figure sits in the report's own grid as a sensitivity | ✗ **F3** |
| **Terminal beta** | Terminal Ke printed beside a 60/40 structure; the construction is unnamed | The same 0.964 equity beta at 40% debt as at 59% debt — **unrelevered**. Hamada gives 0.691 → terminal WACC 13.85%, not 15.00% | ✗ **F13** |
| **Cost-of-capital path** | "one assumed easing calendar, used everywhere, never two"; glide shape from the forward Kd path; terminal on the year-5 factor | **Genuinely done.** Glide fractions, forward WACCs, cumulative factors and the terminal-at-year-5 convention all reproduce exactly. Grids re-glide the whole schedule per cell | ✓ **PASS** |
| **Country risk** | "The local yield already prices default risk; charging it again in the ERP would double-count" | Strips Damodaran's own Jan-2026 CDS spread (3.40% vs file 3.41%) and adds Damodaran's own CDS-based ERP (9.41% vs 9.428% derived from the file). Same basis, same vintage, counted once | ✓ **PASS** — verified against the original file |
| **Currency split of the debt book** | "~100% EGP (presumption, flagged) — No facility disclosure reachable; no USD facility found in any search — the gap is stated, not assumed away" | Honestly declared as a gap rather than closed one-sidedly. Kd 22.0% sits 31bp *below* the sovereign 10Y, so the local-tranche rule is not breached in the wrong direction | ✓ **PASS** (gap correctly logged UNVERIFIABLE) |
| **Effective borrowing rate** | "checked against effective rates 23.5% (FY24) and 22.1% (FY25) — inside 150bp"; denominator is interest-bearing debt, not broad liabilities | Denominator is correct ✓. But the FY25 numerator was **back-solved to close the P&L**, then divided by the debt the same triangulation produced. FY24's check is independent. The Register's own flag — Q1-26 implies ~243/qtr, a fifth of the model — is under-weighted | ✗ **F15** |
| **Inflation path & escalators** | "one path"; CBE 14.3% → 7% → 5% | FX crawl typed at ~3%/yr, below the implied differential (**F18**). D&A escalates off **revenue** at 1.3%, twice the 0.7% history (**F17**). The conversion margin escalates in nominal EGP with no named index. Copper enters the working-capital side only, never the margin side, so a record flat anchor is a maximally adverse view labelled "no view" (**F19**) | ✗ |
| **Forecast anchor** | Anchored on the latest reviewed period; "the H1-2026 statements are the first checkpoint on that ramp" | FY26E opens ~21% above annualised 1Q26 with a named mechanism (grid capex) ✓. **But the H1 print arrived and the study was not updated:** FY26E net loss is 4.7× the annualised actual and Q2 printed a profit | ✗ **F1** |
| **Bridge** | On the latest disclosed balance sheet; net debt; NCI; foots to per share | Lines foot ✓, divide correctly ✓, NCI reasoned ✓. Stands on FY25 with two disclosed loss quarters since (**F10**). Gross debt in the weights, net in the bridge (**F25**). The final printed line does not follow from the one above it (**F22**) | ~ |
| **Balance-sheet integrity** | "Check row is zero by construction" | Honest — and therefore the check proves nothing: `B13 = B9 − B11 − B12`, so `B14 ≡ B9` identically. Correctly disclosed as such | ✓ (disclosed) |
| **Source Register contract** | "Every input … a four-field record emitted directly by compute.py … A bare numeral cannot enter the model: the build fails" | Section C.3 (Global, 2 records) **does not exist**; copper has no record anywhere (**F5**). Section D publishes a different model on five of eight rows, including a net-debt anchor 1,005 mn away from the one used (**F6**) | ✗ |
| **Workbook contract** | "All inputs live on the Assumptions sheet … change one and the whole model reprices" | **6,000** hardcoded in the normalized lens; **0.01** and **0.05** hardcoded floors; every grid and every simulation output hardcoded; FY24 net debt hardcoded at the FY25 value | ✗ **F28–F30** |
| **Terminal-value dependency** | "82% of the EV sits in the terminal value … stated prominently per house rule" | Correct and prominent ✓. The inverted growth gradient is genuinely a product of the construction, not an error — reproduced cell by cell ✓ | ✓ **PASS** |

---

## Section E — Verdict Summary

### Counts by pass

| Pass | TOTAL | PARTIAL | UNVERIFIABLE | PASS |
|---|---|---|---|---|
| 1 — Input verification | 2 | 4 | — | 1 |
| 2 — Market data | 1 | 2 | — | 2 |
| 3 — Cost of capital | — | 3 | — | 3 |
| 4 — Terminal value | 1 | 4 | 1 | 2 |
| 5 — Macro coherence | — | 3 | — | — |
| 6 — Forecast anchoring | 1 | 1 | — | — |
| 7 — Lens architecture & bridge | — | 5 | — | 2 |
| 8 — Calculation verification | — | 2 | — | 5 |
| 9 — The delivered page | — | 6 | — | 2 |
| 10 — Probabilistic & technical | — | 1 | — | 6 |
| 11 — The answer itself | — | 1 (+1 FLAG) | — | — |
| 12 — Completeness sweep | 2 | — | 1 | — |
| **Total** | **6** | **29** | **2** | **22** |

**UNVERIFIABLE (stated precisely):** (i) the implied 20.0-year asset life cannot be compared against a disclosed useful life, because ELEC's audited statements carry the accounting-policies note and were unreachable — resolved by publication of the FY25 audited statements; (ii) El Sewedy's FY25 EBITDA of 30.7 bn and Riyadh Cables' balance-sheet inputs were not confirmed against the filings — resolved by the respective annual reports. The Egypt 10-year yield print was also not date-matched to a primary bond-market source (worldgovernmentbonds returned an unpopulated template; a second host also failed), so F33(a) rests on the Register's own admission rather than on an independent print.

### The three most valuation-critical findings

**1 — The study's own named falsifier fired five weeks before this audit, and the study does not carry it (F1).** H1-2026 shows a net loss of 200.8 mn against a modelled FY26E loss of 1,873 mn, on revenue 14.9% below forecast — and **Q2-2026 printed a net profit of +40.8 mn**, which on the study's own finance-cost run-rate requires Q2 EBITDA of ≈609 mn against a modelled full-year 416 mn. The study forecast a volume recovery with a margin trough; the company printed a volume shortfall with a margin recovery. The FY26E P&L, the debt-compounding schedule and the entire "the equity is an option, not a claim" framing are built on a first year that did not happen.

**2 — 95.8% of the headline EGP 0.34 comes from the two lenses that assume the debt problem away (F7, F9).** The largest of them — the book lens, at 54.2% of the answer — discounts a 240%-geared balance sheet at the *terminal, deleveraged* cost of equity, a choice worth 0.085 on the central, a quarter of the headline, and gridded nowhere. The blend mixes a world in which the debt is unpayable with one in which it has been repaid, and publishes the average as a fair value.

**3 — The terminal ROIC's invested-capital denominator is an undisclosed construction (F3).** NWC + 5% of revenue (16,325) against the workbook's own NWC + PP&E + other assets (19,523), overstating ROIC by 150bp, terminal value by 23% and enterprise value by 19%. The correct figure already sits in the report's own sensitivity grid, labelled as a downside.

### Direction of the contested-judgement count

**Approximately 15 of 17 judgements worth more than ~5% of value are resolved the same way — all bearish, most labelled "conservative."** In a report whose conclusion is bearish, a bearish assumption is not conservative; it is thesis-confirming, and the word has been inverted throughout. The study never counts the direction. This is a flag, not a failure: a company with negative operating cash flow, 240% gearing and a collapsed first quarter can genuinely deserve a consistent read.

Pass 11's high-prior-of-defect list nonetheless fires on this answer: an unread filing (F1), contradictory macro paths (F18, F19), a bridge on a superseded balance sheet (F10), a terminal charging a capital intensity the company has never operated at (F24c), clamped lenses (F21), and figures typed rather than computed (F6, F32).

### Does the headline range survive the corrections?

> **It shifts materially.**

The **direction** survives. At EGP 2.19 the market pays 4.5× the modelled enterprise, and no correction in this audit closes a gap of that size — the equity remains floored on two of four lenses because the *debt*, not the cash flow, is binding, and the corrections run both ways (the terminal invested capital and the book-lens cost of equity push down; the unrelevered beta, stub discounting, the forgone NOL shield and the H1 margin evidence push up).

What does **not** survive is the number. Correcting only the book lens's cost of equity takes the central from 0.34 to ≈0.255; removing book value from the central, as it should be, takes it to 0.193; and the "−85%" is not a measurement of the security as it exists, but a weighted average of a floored zero and a counterfactual balance sheet. Meanwhile the first forecast year — the one the study itself nominated as the test — has been contradicted by the company's own disclosure.

**The book is in better order than most.** The arithmetic is honest, the discount schedule is genuinely one easing calendar, the country risk premium verifies against the original file to two basis points, the simulation reconciles to its own stated label and keeps its lenses uncoupled, the sensitivity grids do exactly what they claim, and the sourcing gaps are disclosed rather than papered over. The failures are almost entirely in what the page does not say about how it was built — and in a filing that was published and not read.

---

## Sources consulted

- Arab Finance — *Electro Cable Egypt shifts to losses in H1 2026* — http://arabfinance.com/en/news/newdetails/46766
- Zawya — *Egypt: Electro Cable incurs consolidated losses in Q1 2026* — https://www.zawya.com/en/capital-markets/equities/egypt-electro-cable-incurs-consolidated-losses-in-q1-2026-cfbqbyeo
- Aswath Damodaran — *Country Default Spreads and Risk Premiums* (Egypt row; "Last updated January 5, 2026") — https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html
- MINING.COM — *Copper price holds near record as London warehouse bidding war looms* (LME cash $14,545/t, 14-Aug-2026) — https://www.mining.com/copper-price-holds-near-record-as-london-warehouse-bidding-war-looms/
- stockanalysis.com — *El Sewedy Electric (EGX:SWDY)* FY2025 revenue and net income — https://stockanalysis.com/quote/egx/SWDY/

---

*Prepared as a forensic verification of the documents supplied. The auditor proposes no alternative valuation and takes no view on the security. Findings are recorded only where they could be demonstrated; unverified suspicions are logged as UNVERIFIABLE.*
