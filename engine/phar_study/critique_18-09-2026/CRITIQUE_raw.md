# EIPICO Valuation Audit

**Forensic verification · Master audit protocol v2**

Egyptian International Pharmaceutical Industries Company (PHAR, The Egyptian Exchange). Audit of the independent valuation study, its workbook and its bibliography. Audit date 18 September 2026.

| Total fail | Partial fail | Unverifiable | Passes verified |
|---:|---:|---:|---:|
| **9** | **17** | **1** | **41** |

> The three artefacts reconcile to the last cell and disagree with each other about what they contain.

---

## Section A — Audit scope

Audited: the valuation study (5 sections, 28 tables), the delivered workbook (16 sheets, every formula re-implemented independently in Python and evaluated cell by cell), and the bibliography (278 registered inputs, 14 tables).

Primary sources reachable in this audit: **none directly**. The company's filings, the Egyptian Exchange, the central bank auction curve and the country-risk dataset were not accessible from this environment, so no figure was re-traced to an original document.

What that means for grading: every *input* verdict below rests on internal evidence only — one delivered artefact against another, or a figure against the arithmetic that must produce it. Nothing here is recorded as a source failure on the company's own numbers, which are **UNVERIFIABLE** as a class and are not counted in the table.

What was fully checkable, and was checked: every arithmetic chain in the model; every published figure against the workbook that produces it; every stated construction against the cells that implement it; and every cross-reference between the three documents. That is where the findings are.

> **Recomputation method.** The workbook ships with no cached values — every formula cell reads empty until Excel recalculates. The model was therefore rebuilt from the formula text alone and re-evaluated. It reproduces **EGP 32.9975** (Frame A) and **EGP 49.6789** (Frame B) against the workbook's own `Sensitivity!D5` of `32.99747064299516` and the study's EGP 33.00 / 49.68. Reconciliation is exact.

---

## Section B — Fail table

Twenty-seven findings, ordered by how much of the valuation each one moves. Impact is measured against the Frame A centre of EGP 33.00 by re-running the delivered model with the one item corrected and everything else held at its published value.

---

### 01 · The domestic price escalator does not do what both the workbook and the bibliography say it does

**Plane:** Input · Construction  **Severity:** TOTAL FAIL  **Pass:** 5

| Field | |
|---|---|
| **Location** | `Assumptions!C14:G14`; bibliography input `dom price growth`; study §1.6 Table 7; Table 20 gross-margin row |
| **Report says** | Both artefacts state the same basis: *"Administered prices track inflation, no real gain"* / *"price growth tracks domestic inflation as it converges on the central bank's target, with no real price gain."* The path carried is 5.0% / 8.0% / 7.5% / 6.5% / 5.5%. |
| **What is correct** | The model's own domestic inflation path (`Assumptions!C29:G29`, sourced as the central bank's published baseline) is 16% / 12% / 9% / 7.5% / 7.0%. Over five years the selling price compounds to **1.3697** while domestic prices compound to **1.6289** — a **15.9% cumulative real price cut**. The price never tracks inflation in any year. |
| **Why it failed** | The cost side rides the transitional inflation path — 68.4% of the cost stack escalates through an exchange-rate path *derived from that same CPI path*, labour runs above it, energy runs above it — while the selling price rides the long-run target. That is one event counted once on costs and ignored once on price. The bibliography's `fx path` note congratulates the study for closing exactly this trap on the currency limb; it stays open on the price limb. The model then reports the resulting gross-margin decline (44.0% audited → 39.2% → 36.5%) as an *output* of an honest unit build, which mechanically it is. |
| **Impact** | **+182%** — Frame A EGP 33.00 → **93.16**, Frame B EGP 49.68 → **111.85**; FY2030E gross margin 36.5% → 43.5% against a 44.0% audited actual. This single item closes 64% of the study's entire 74% gap to the market price. It is worth more than the provision judgement the study nominates as "its single most consequential contested judgement," and more than the biologicals-plant crux. |
| **Correct method** | Escalate the administered price on the same inflation path the costs are escalated on, or state the assumed pass-through ratio explicitly (the carried path implies 31% in FY2026 rising to 79% by FY2030), disclose the cumulative real price change as the real number it is, and put a grid on it. |

---

### 02 · The terminal value is not built on the construction the study declares

**Plane:** Construction  **Severity:** TOTAL FAIL  **Pass:** 4

| Field | |
|---|---|
| **Location** | `DCF!B18:B29`; study §1.1; Table 18 row "The terminal return on invested capital is now COMPUTED"; workbook `Fundamental Valuation!D2` |
| **Report says** | *"a terminal value on the growth-over-return reinvestment identity"*, and *"terminal reinvestment rises from 25.0% to 55.0% of terminal operating profit after tax."* `DCF!D19` states: *"This is what sets terminal reinvestment. It is not an assumption and there is no cell to type it into."* |
| **What is correct** | The sheet does not use the reinvestment identity. `DCF!B19` computes the FY2030E return on invested capital at **12.73%** — and **is referenced by no other cell in the workbook**. The terminal cash flow is built instead from four typed constants (book depreciation, maintenance at current cost, growth capital, working-capital inflation), producing a reinvestment rate of **40.9%**, not 55.0%. The 55.0% in Table 18 is `g ÷ ROIC = 7.00 ÷ 12.73 = 54.99%` — the identity's answer, printed beside a terminal that does not apply it. |
| **Why it failed** | A construction materially different from the one claimed, in the block holding 80% of core enterprise value. The delivered terminal reinvests 14 points less of profit than the study says it does, and every reader checking the identity will reproduce a different number. |
| **Impact** | **−27% to −34%** — run as declared, Frame A is EGP **21.77** (on terminal NOPAT) or EGP **24.00** (on FY2030E NOPAT), against the published EGP 33.00. |
| **Correct method** | Either implement the identity the study declares — `terminal FCF = NOPAT × (1 − g/ROIC)`, with `B19` actually feeding it — or describe the construction that is used: a maintenance-capex terminal with an explicit replacement charge. The second is the better construction; it is simply not the one on the page. |

---

### 03 · Beta is regressed against the analyst's own coverage universe, not the exchange's published index

**Plane:** Input · Construction  **Severity:** TOTAL FAIL  **Pass:** 2

| Field | |
|---|---|
| **Location** | `Assumptions!C49` = 0.629; study Table 10 and Table 19; bibliography §6.2 |
| **Report says** | *"Own-stock weekly regression against a 36-name local composite, five years; R-squared 0.235, n = 257, standard error 0.071."* The bibliography names the regressor: *"an equal-weighted composite of 36 Egyptian listed names **built from the full covered price library**"*, and lists all 36 tickers. |
| **What is correct** | PHAR is listed on the Egyptian Exchange, whose published indices are EGX 30 / EGX 70 / EGX 100. An equal-weighted basket of the analyst's own coverage library is a coverage artefact, not a market. R² of 0.235 leaves 76.5% of the stock's variance unexplained by the regressor, which is what a mismatched benchmark produces. |
| **Why it failed** | The protocol grades this tier explicitly. Compounding it, the composite *contains the subject at ~2.8% weight* — the study discloses this, honourably, but it means the regressand is inside the regressor. |
| **Impact** | **Direction indeterminate; magnitude large.** Each 0.10 of beta is worth roughly EGP 4–5 a share: β 0.45 → EGP **42.17**; β 0.629 → EGP **33.00**; β 0.90 → EGP **22.62**; β 1.00 → EGP **19.55**. The true EGX-regressed coefficient is **unverifiable** here — the index series was not supplied. |
| **Correct method** | Re-estimate against the published index of the listing exchange, with the subject necessarily inside it as any real index has it. Publish the regression diagnostics against that index. |

---

### 04 · A 3 September edition delivered under a 9 August masthead, with a false price date in three places

**Plane:** Input · Disclosure  **Severity:** TOTAL FAIL  **Pass:** 2 / 9

| Field | |
|---|---|
| **Location** | Study masthead; Table 10 source column; Table 18 remediation row; `Assumptions!C3` basis; workbook `READ FIRST!B11` |
| **Report says** | *"Prepared 9 August 2026 · share price EGP 127.30 at the close of 6 August 2026."* Table 10: the yield is an *"Observable print of 6 August 2026 — the SAME date as the share price used throughout."* Table 18 lists as a fixed defect: *"The risk-free rate and the share price are struck on ONE date … Both are now 6 August."* The workbook repeats it twice. |
| **What is correct** | The bibliography's own `spot` row settles it: *"127.3 \| 2026-09-03 \| Egyptian Exchange close, 3 September 2026 … **The previous edition was struck at EGP 130.05 on 6 August 2026.**"* Bibliography Table B6 prints the 6 August close as **130.05**. The study's own Table 3 correctly reads "Close of 3 September 2026." |
| **Why it failed** | EGP 127.30 is not the 6 August close and never was. The valuation price and the risk-free rate are therefore **28 days apart**, not on one date — so the defect Table 18 records as closed is open, and the assertion that closes it is false. The preparation date is the superseded edition's. At delivery the price is 15 days stale on its true date and 43 days stale on the date claimed. |
| **Impact** | **No effect on the computed value** (the model holds 127.30, which is the right number). The failure is that every date-alignment claim the study makes about its own evidence is wrong, including one it presents as a fix. |
| **Correct method** | Re-strike the risk-free rate on 3 September, or state plainly that the yield is a 6 August print carried against a 3 September price, and correct the masthead and both workbook notes. |

---

### 05 · The technical read and the whole probability map are memories of the superseded edition

**Plane:** Disclosure  **Severity:** TOTAL FAIL  **Pass:** 9 / 10

| Field | |
|---|---|
| **Location** | Study §2, §3, §6, Tables 13–15, 17; `Monte Carlo!B3:C4`; bibliography §6.1 |
| **Report says** | §3: *"The anchor is the EGP 130.05 close of 2026-08-06."* Check dates 2026-09-06 and 2026-11-08. §2 opens *"The price closed 130.05 above a rising 20-day (101.58)…"*. The dividend-yield carry in the simulation is *"EGP 3.50 … over the 130.05 close."* |
| **What is correct** | 130.05 / 6 August is the *previous* edition's anchor. The valuation beside it is struck on 127.30 / 3 September. The cleaned price series (bibliography §6.1) runs "02 Jan 2011 to **06 Aug 2026**" — it does not contain the close the valuation uses. At the audit date of 18 September the one-month check date of 2026-09-06 had already passed by 12 days. |
| **Why it failed** | A scenario artefact generated against a superseded central looks like a computed record while being a memory of an older answer. Every moving average, RSI, ATR, MACD reading, 52-week range, pivot cluster, volatility input, percentile and touch probability in the study is computed on data ending six weeks before the valuation date. The study publishes a forward-looking one-month band whose window is already closed. |
| **Impact** | **No effect on fair value** — §3 is correctly walled off from the valuation. The entire price-structure and probability half of the document is nonetheless not current with the answer it accompanies. |
| **Correct method** | Re-run the series, the indicators and the simulation to 3 September, or withdraw §§2–3 and 6 from this edition. |

---

### 06 · Appendix A.1 does not foot in any of its five forecast columns

**Plane:** Disclosure  **Severity:** TOTAL FAIL  **Pass:** 9

| Field | |
|---|---|
| **Location** | Study Table 20 (Appendix A.1); `Income Statement!E13:I14` and `!E25:I25` |
| **Report says** | Table 20 prints Revenue → Cost of sales → Gross profit → Selling and marketing → R&D → G&A → Credit losses and provisions → **Operating profit**, and states: *"Every forecast line is the model row the valuation itself uses."* |
| **What is correct** | Two deduction rows the model applies are not printed: board remuneration (−2.0 a year) and the 20.58% share of depreciation charged to selling and administrative expense (−62.6 to −91.7 a year). Following the table's own rows: FY2026E gives **2,175.5** against the **2,110.9** printed. Every forecast year is short by 64.6 / 89.5 / 93.7 / 92.0 / 89.1. The three audited columns foot, because both rows are zero or immaterial there. Separately, the step from "Profit for the year" to "Profit attributable" omits a −18.0 minority row. |
| **Why it failed** | A deduction the model makes and the page does not print. Every printed figure is individually correct; the reader still cannot reproduce the total from the rows above it. |
| **Impact** | **Nil on value.** The gap is 3.1% of the FY2026E operating profit the table states — above the protocol's own materiality threshold as a *disclosure* defect, nil as an arithmetic one. |
| **Correct method** | Print both rows, or add an "other operating expense" line carrying them, so the waterfall reaches the total it prints. |

---

### 07 · Four of the five terminal cash-flow lines are typed constants, against an explicit and tested claim that they are live

**Plane:** Disclosure  **Severity:** TOTAL FAIL  **Pass:** 8

| Field | |
|---|---|
| **Location** | `DCF!B22`, `B23`, `B24`, `B25`, `B44`; `READ FIRST!B3`; bibliography §7 |
| **Report says** | `READ FIRST!B3`: *"Change a driver on the Assumptions sheet and the cost of capital, the glide, the discount factors, the cash-flow waterfall, **the terminal block**, the three statements, the bridge and every ratio all move. **This claim is tested, not asserted**: a driver test perturbs each input in place, re-evaluates the whole workbook and checks the headline moves in the right direction."* The bibliography repeats it and cites "the study's quality-control table," which the study does not contain. |
| **What is correct** | The four lines are literals: `423.085728`, `−674.802126`, `−0.000000`, `−717.450174`. Frame B replaces all four with a single literal, `−969.166571`. Change the depreciation rate from 6.2% to 4.5% and FY2030E depreciation falls to 327.7 while the terminal still adds back 423.09 and still charges 674.80 of maintenance. The terminal block — 80% of core enterprise value — responds to no driver. |
| **Why it failed** | A hardcoded override mid-chain in the place holding most of the value, under a claim that it was tested and is not there. The three classes of pasted cell that `READ FIRST` does name do not include this one. |
| **Impact** | **Nil on the delivered answer.** Every one of the four constants is the *right* number for the delivered driver set — each was rebuilt from the live rows and matches to six decimals (Section C.3). The failure is that the workbook cannot be used as the study says it can. |
| **Correct method** | Replace with formulas: `=Segments!H41`, `=−Segments!H41*(1+g)^(life/2)`, `=−real_g*fixed_capital`, `=−'Balance Sheet'!I19*g`. Or list the terminal block as a fourth class of pasted cell. |

---

### 08 · The published price of the ex-subject beta is wrong by an order of magnitude

**Plane:** Disclosure  **Severity:** TOTAL FAIL  **Pass:** 9

| Field | |
|---|---|
| **Location** | Study Table 19 (caveats); bibliography §6.2 |
| **Report says** | *"Removing it gives 0.565 rather than 0.629, which would RAISE the two centres by about EGP 32.04 and EGP 23.18 a share"* / *"would RAISE the two fundamental centres to EGP 65.04 and EGP 72.86 from EGP 33.00 and EGP 49.68."* |
| **What is correct** | Running the delivered model at β = 0.5652 gives Frame A **36.01** and Frame B **53.53** — uplifts of EGP **3.01** and **3.85**, not EGP 32.04 and 23.18. The stated figures overstate the effect by EGP **29.03** and **19.33**, roughly tenfold. |
| **Why it failed** | A figure stated in prose and typed rather than computed — the category the protocol warns no arithmetic check will catch, because a typed word does not look like a figure. It sits in the caveat table, where it inflates the apparent cost of the conservative choice the study is defending. |
| **Impact** | **Nil on the published value**; it materially misstates the study's own risk display. The direction of the claim is right; its size is not. |
| **Correct method** | Compute the alternative from the model, as the sensitivity grid beside it already does (`Sensitivity!B10:F11`, which is correct). |

---

### 09 · Bibliography sections 3 and 4 and primary document P10 are the previous edition's, wholesale

**Plane:** Disclosure  **Severity:** TOTAL FAIL  **Pass:** 1 / 12

| Field | |
|---|---|
| **Location** | Bibliography Table B1 row P10; Table B3 (judgements); Table B4 (negative results) |
| **Report says** | The bibliography is *"the companion to the valuation study of 9 August 2026"*, and the study says *"Every figure in this study traces to a numbered source in the accompanying bibliography."* |
| **What is correct** | Eight material contradictions with the study it accompanies. The judgements register states: associate contribution normalised to **320** (study: 250); terminal growth **5%** (study: 7%); terminal debt weight **20%** (study: 25.5%); yield **22.31%**, spread **3.41%**, normalised **18.90%** (study: 23.00 / 3.42 / 19.58); relative-lens multiples **8.1× / 6.7× / 9.8×** and "the unadjusted peer median would give EGP 133" (study: 6.33 / 6.57 / 6.47 and EGP 182.39); imported inputs **79%** of the cash cost stack (study: 68.4%, and states that 79.4% is the reading the group's own packaging manufacture rules out); currency *"about 4% a year, narrowing to 3%"* (study: 11.4% narrowing to 4.4%); and *"the sensitivity table runs 3% to 7% and the value ranges from **EGP 78 to EGP 98**"* (study's grid: EGP 17 to 48). Table B4 still records the rate as "a dated house reference print of 21 July 2026." **P10** names the January-2026 vintage of the country-risk file and lists its four values (3.41 / 6.37 / 13.94 / 9.41) — none of which the model holds. |
| **Why it failed** | The document whose whole function is to let a reader audit the study contradicts it on the terminal growth rate, the discount rate, the bridge, the cost stack and the published range. A reader checking the model against P10 — the register's own first stop — finds four mismatches on the equity risk premium. |
| **Impact** | **Nil on value.** Note the mitigating half: the bibliography's *input register* (Table B5, §2) is current and correct — it names the mid-year July 2026 vintage and its four values (3.42 / 5.9702 / 13.4806 / 9.5164), all of which match the model exactly, and it states what the January vintage carried. The inputs are properly sourced. The document register, the judgements register and the negative-results register are not. |
| **Correct method** | Regenerate sections 1, 3 and 4 from the delivered model, as section 2 evidently was. |

---

### 10 · The local cost of debt does not reproduce from its own stated construction

**Plane:** Logic  **Severity:** TOTAL FAIL (reproduce test)  **Pass:** 3

| Field | |
|---|---|
| **Location** | `Assumptions!C50` = 24.81%; study Table 10; bibliography input `kd egp` |
| **Report says** | Study Table 10: *"Cost of debt, local currency \| 24.81% \| Sovereign yield plus 250 basis points — above the sovereign by construction."* The sovereign yield carried is 23.00%. |
| **What is correct** | **23.00% + 2.50% = 25.50%**, not 24.81%. The bibliography resolves the gap: its `kd egp` row derives 24.81% from *"the ten-year sovereign yield of **22.31%** plus a 250 basis-point corporate credit spread"* — the *previous* edition's yield. When the yield was re-struck at 23.00%, the cost of debt built on it was not. |
| **Why it failed** | Arithmetic that does not reproduce from the inputs printed beside it. The "above the sovereign by construction" floor now stands 181bp above a yield that moved 69bp, so the floor is no longer the construction it is described as. |
| **Impact** | **≈ +0.5%** — blended marginal cost of debt 18.55% against 18.89% correctly struck; first-year WACC 22.71% against 22.80%. Immaterial in value, but the reproduce test is absolute. |
| **Correct method** | Make `C50` a formula: `=C44+0.025`. |

---

### 11 · The associate stake is carried at a Gulf multiple without the cost-of-equity adjustment the study applies one page earlier

**Plane:** Construction  **Severity:** PARTIAL FAIL (material)  **Pass:** 7

| Field | |
|---|---|
| **Location** | `Assumptions!C64` = 11.0; `SOTP Bridge!B5`; study Table 5; bibliography input `assoc multiple` |
| **Report says** | Bridge line: *"Add: earning associates at normalised earnings times the multiple — 2,750 \| 16.30."* Basis: *"Below the Gulf listed range for a minority, unlisted, non-controlled stake."* |
| **What is correct** | The study adjusts the peer P/E from 21.35× to **6.47×** precisely because those companies face a ~10% cost of equity rather than this one's 16.9% — and prints the unadjusted answer (EGP 182.39) to show the size of the gap. The associate multiple is the same kind of number and receives no such adjustment. On the study's own perpetual terms (payout 62.7%, terminal cost of equity 16.903%, growth 7%) the implied multiple is **6.33×** → EGP 1,582m, or **9.38** a share. The bibliography further records that *"the one associate in the group that is itself listed trades on roughly 9.3 times trailing earnings"* — below the 11× applied. |
| **Why it failed** | Two constructions for one problem inside one document. The study also never discloses on its own page that one associate is listed, nor its observable multiple; a listed associate carried above its own market price owes that disclosure. |
| **Impact** | **−21% of the Frame A centre** — EGP **6.92** a share between the 11× carried and the study's own cost-of-capital-consistent 6.33×. On the observable 9.3× the difference is EGP 2.52. |
| **Correct method** | Apply the same cost-of-equity adjustment used on the peer leg, or carry the Saudi holding at a Gulf multiple and the Egyptian holdings at an Egyptian one, and say which is which. |

---

### 12 · Two useful lives in one model — the disclosed one used only where it raises the charge

**Plane:** Construction  **Severity:** PARTIAL FAIL (material)  **Pass:** 4 / 12

| Field | |
|---|---|
| **Location** | `Assumptions!C38` = 6.2%; `DCF!B23`; bibliography input `asset life weighted` = 13.8 years |
| **Report says** | `C38` basis: *"About a sixteen-year blended life"* — the only major driver in the sheet with no note reference. `DCF!B23`: *"book depreciation escalated over half the useful life **the company itself discloses**."* |
| **What is correct** | The bibliography computes a genuinely disclosed weighted life of **13.8 years** from note 3.1's stated lives (buildings 50, machines 15, transport 5, furniture 10) weighted by note 4.1's gross cost by class, and shows the base footing to the note's own total. `B23` uses it: `423.085728 × 1.07^(13.8/2) = 674.8021`, exact. The explicit window instead depreciates on a chosen 16.13-year life (1 ÷ 6.2%). |
| **Why it failed** | The disclosed life appears in the terminal, where the shorter life raises the maintenance charge; the chosen, longer life runs the five explicit years, where it lowers the depreciation charge. Each is defensible alone; together they are inconsistent, and only one carries a citation. |
| **Impact** | **−6.2%** — on the disclosed 13.8-year life throughout, Frame A EGP 33.00 → **30.94**; FY2026E D&A 304 → 354, FY2030E 423 → 476. |
| **Correct method** | Run one life. If the incoming EIPICO 3 asset genuinely shortens the blend, re-weight note 4.1's classes to include it and show the arithmetic, rather than asserting "about sixteen years." |

---

### 13 · The minority is charged 18 a year in profit and deducted at 4.0 of book in the bridge

**Plane:** Construction  **Severity:** PARTIAL FAIL (material)  **Pass:** 7

| Field | |
|---|---|
| **Location** | `Income Statement!E25:I25` = −18.0; `Assumptions!C80` = 3.9998; `SOTP Bridge!B10` |
| **Report says** | Bridge: *"Less: non-controlling interests \| (4) \| (0.02)"*, described as the post-deconsolidation figure from the reviewed March interim. |
| **What is correct** | The cash-flow model capitalises 100% of subsidiary cash flow, and the model's own income statement assigns 18.0 a year to minorities in every forecast year. Capitalised on the study's own terminal terms that stream is worth ≈ 194m, or **1.15** a share, against the **0.02** deducted. A minority is worth its share of value, not its historical book cost. |
| **Why it failed** | The −18.0 is itself a perimeter contradiction: audited minorities ran 0.99 / 1.21 / 16.24, and almost all of the FY2025 figure belonged to the company deconsolidated in Q1 2026 — the same event the bridge relies on to justify deducting 4.0. |
| **Impact** | **−3.4% of Frame A** on the bridge line. Offsetting and smaller: the −18.0 understates forecast EPS by ≈ 0.10, which feeds the ROE path, the sustainable return and hence the book and normalised lenses. |
| **Correct method** | Deduct the minority at its share of value, and set the forecast minority charge to the post-deconsolidation perimeter the bridge already uses. |

---

### 14 · §1.5 declares four weights and then states they give a number they do not give

**Plane:** Disclosure  **Severity:** PARTIAL FAIL  **Pass:** 7

| Field | |
|---|---|
| **Location** | Study §1.5; Table 1 rows "CENTRE — Frame A/B" and the memo row; `Fundamental Valuation!B7:B9` |
| **Report says** | *"the cash-flow weight of 50% is carried in full on ONE frame at a time, beside the three lenses that do not turn on the judgement at all — book value against sustainable return at 20%, relative multiples at 15%, and normalised earnings power at 15%. **That gives EGP 33.00 a share on Frame A** and EGP 49.68 on Frame B."* |
| **What is correct** | 0.50×33.00 + 0.20×43.91 + 0.15×48.65 + 0.15×56.78 = **41.10**, and the Frame B equivalent is **49.44** — which the same table prints two rows below as *"the weighted blend this edition replaced."* The published centre is the unweighted cash-flow reading; `Fundamental Valuation!B7` is simply `=B2`, and its own note says so. |
| **Why it failed** | The prose describes the retired construction while the table prints the current one. The weights exist in the workbook (`C2:C6`) and drive only the memo row. |
| **Impact** | **Nil** — the published numbers are the unweighted ones and are correct. The sentence explaining how they were reached is not. |
| **Correct method** | Say the centre is the cash-flow reading alone, and drop the weights or move them entirely into the memo. |

---

### 15 · The relative lens is built on an average of the two frames the study says it never averages

**Plane:** Construction  **Severity:** PARTIAL FAIL  **Pass:** 7

| Field | |
|---|---|
| **Location** | `Relative & Normalized!B11` = `=AVERAGE(B9:B10)`, feeding `C26`; study Table 6 leg 1; §1.5 |
| **Report says** | §1.5 describes *"the three lenses that do not turn on the judgement at all."* The study states five separate times that the frames are never averaged. The workbook's own note pleads: *"Averaging the two frames' EARNINGS is not averaging the two VALUATIONS."* |
| **What is correct** | The justified-multiple leg's earnings base of EGP 5.46 is the mean of Frame A's 5.2774 and Frame B's 5.6410. The relative lens therefore does turn on the contested judgement. On Frame A alone the lens is **48.27**; on Frame B alone, **49.04**; published, 48.65. |
| **Why it failed** | A breach of the document's own most-repeated rule, and a false claim about the independence of a lens the two centres are published beside. |
| **Impact** | **±EGP 0.4 on the lens**, nil on the two centres, which are the unweighted cash-flow readings. |
| **Correct method** | Publish the relative lens twice, once per frame, as the cash-flow lens is. |

---

### 16 · Three workbook basis notes describe the superseded build of the terminal — on the cells carrying 80% of core value

**Plane:** Disclosure  **Severity:** PARTIAL FAIL  **Pass:** 3 / 9

| Field | |
|---|---|
| **Location** | `Assumptions!B56`, `B62`; `Peer & Sector!D8` |
| **Report says** | `B56`: *"A sourced **5%** medium-term inflation target plus an UNSOURCED 5.5-point real convention"* — which gives 10.5%, while `C56` holds 12.5%. `B62`: *"Pound-nominal, against a **5%** terminal inflation rate — about zero in real terms"* — against 5%, the 7% carried is +1.9% real. `Peer & Sector!D8`: *"this company's perpetual cost of equity is **14.9%** and its current cost of equity **24.8%**"* — the model computes 16.903% and 25.566%, and 24.8% is the local cost of *debt*. |
| **What is correct** | The bibliography's `rf term` row gives the current derivation and it reproduces: *"the long-run inflation this valuation carries throughout, **7.0%**, plus the standard 5.5-point emerging-market real-rate convention"* = 12.5%. It states outright that *"the previous edition used 10.5%, built the same way but on a 5% inflation assumption."* 10.5% + 0.629×7% = 14.90% — exactly the number still sitting in `Peer & Sector!D8`. The notes are fossils of the prior edition. |
| **Why it failed** | A reader auditing `C56` against its own basis reproduces 10.5% and concludes the single most terminal-sensitive number in the model is 200bp wrong. It is not wrong — the note is. That gap is 39% of the Frame A centre in apparent error. |
| **Impact** | **Nil on value.** For reference, at the note's 10.5% the terminal WACC falls to 13.54% and Frame A rises to EGP **45.96**. Recorded as disclosure, not input: the delivered cell is correctly derived. |
| **Correct method** | Rewrite the three notes to the current build, and make `C56` the formula `=terminal_inflation + 0.055` so it cannot drift from the inflation the rest of the model carries. |

---

### 17 · Two tax rates still run, against a stated remediation that one now runs both

**Plane:** Logic  **Severity:** PARTIAL FAIL  **Pass:** 3

| Field | |
|---|---|
| **Location** | `Assumptions!C102`, `C112` (use `C9` = 22.5%); `DCF!B7` (uses `C10` = 23.5%); study Table 18 |
| **Report says** | Table 18: *"Free cash flow is taxed at the EFFECTIVE rate, not the statutory rate — the model conceded a 23.5% effective burden in one place and applied 22.5% in the cash-flow engine. **One rate now runs both.**"* |
| **What is correct** | The cash-flow engine was fixed; the debt tax shield was not. Both the first-year and the terminal after-tax cost of debt still multiply by `(1 − C9)`, the statutory 22.5%. |
| **Why it failed** | A declared fix that is half-made, and a claim about the model that the model contradicts. |
| **Impact** | **≈ 5 basis points** on the first-year WACC (22.71% against 22.66% on one rate). Immaterial. |
| **Correct method** | Point `C102` and `C112` at `C10`, or state that the shield is deliberately taken at the statutory rate. |

---

### 18 · The crux's "32% of FY2030 revenue" is 32% of a revenue figure the study does not publish

**Plane:** Disclosure  **Severity:** PARTIAL FAIL  **Pass:** 9

| Field | |
|---|---|
| **Location** | Study §1.7; `Sensitivity!A34` |
| **Report says** | *"an additional EGP 8,871 million of revenue by FY2030 … That is **32% of FY2030 revenue**."* The workbook's own row label reads the same. |
| **What is correct** | 8,871 ÷ 18,608 (the published FY2030E revenue) = **47.7%**. The 32.3% is 8,871 ÷ 27,479 — the *enlarged* revenue including the increment itself. Both are legitimate framings; only one is stated, and it is the smaller. |
| **Why it failed** | A figure with two legitimate framings stated in one, and the denominator is not on the page. |
| **Impact** | **Nil on value**; it makes the hurdle the market is pricing look a third smaller than it is against the business as forecast. |
| **Correct method** | State both, or label the base. |

---

### 19 · "2.3 times what the plant cost to build" converts a historical outlay at a 2030 exchange rate

**Plane:** Input  **Severity:** PARTIAL FAIL  **Pass:** 9

| Field | |
|---|---|
| **Location** | Study §1.7 |
| **Report says** | *"the market is paying EGP 94.30 a share — EGP 15,914 million … against a stated build cost of USD 100 million, **about EGP 7,011 million**. … it is paying roughly **2.3 times** what the plant cost to build."* |
| **What is correct** | 7,011 ÷ 100 = **70.11** — the model's FY2030E exchange rate. The spend occurred over FY2023–25; the company's own audited construction balance at 31 December 2025 is EGP **4,901m**, which is USD 100m at the FY2025 disclosed average of 49.48 the study itself carries. On the company's own recorded figure the market is paying **3.25×** the build cost, not 2.3×. |
| **Why it failed** | A period and currency mismatch: a future rate applied to a past outlay, in a comparison the study offers specifically as *"a multiple of an observable outlay."* The observable outlay is on the balance sheet in pounds. |
| **Impact** | **Nil on value**; it understates the study's own headline proposition by 40%. |
| **Correct method** | Use the audited EGP 4,901m construction balance, or convert USD 100m at the rates in force when it was spent. |

---

### 20 · The normalised-earnings lens reverses the depreciation step the whole study exists to charge

**Plane:** Construction  **Severity:** PARTIAL FAIL  **Pass:** 7

| Field | |
|---|---|
| **Location** | `Relative & Normalized!B32:B37`; study §1.4 |
| **Report says** | *"FY2025 was the best operating year in the company's history … This lens deliberately gives part of that back"* — applying the FY2023–25 average operating margin of 22.9% to FY2027 revenue. |
| **What is correct** | Those three years carried depreciation of 105, 103 and 118. Applying their average margin to FY2027 revenue gives operating profit of **2,888** against the model's own **2,254** after the 425 depreciation charge that is the study's central mechanism. The lens gives back the peak margin and the new plant's depreciation together. |
| **Why it failed** | It produces the highest of the five readings (EGP 56.78) by quietly undoing the thesis, and §1.4 describes only the first of the two givebacks. |
| **Impact** | **Nil on the two centres** (this lens is not in them); it widens the published field high by roughly EGP 8–10 on an undisclosed basis. |
| **Correct method** | Normalise the margin net of the post-licence depreciation run-rate, or state that the lens deliberately values the pre-EIPICO-3 business. |

---

### 21 · Two price anchors on one technical page

**Plane:** Disclosure  **Severity:** PARTIAL FAIL  **Pass:** 10

| Field | |
|---|---|
| **Location** | Study §2 and Table 13 |
| **Report says** | Prose: *"The price closed 130.05 … the last close sits 17% below that high and 198% above that low."* Table 13: *"Last close \| 127.30"*, with distances of +22.5% / +17.8% / +10.0% / −27.4% / −30.5% / −32.9%. |
| **What is correct** | Every ladder distance reproduces off **127.30** (156.00 → +22.55%, 85.40 → −32.91%). Every prose figure reproduces off **130.05** (156.00 → −16.6% ≈ "17%"; 43.60 → +198%). Off 127.30 the prose figures would be −18.4% and +192%. |
| **Why it failed** | Two anchors inside one section, with the narrative stating one close and the table beneath it printing another. A reader cannot tell which close the section is about. |
| **Impact** | **Nil on value.** |
| **Correct method** | One close, stated once, with every distance computed from it. |

---

### 22 · The workbook still calls Frame A's 5.25% "the three-year average" after the study retracted that label

**Plane:** Disclosure  **Severity:** PARTIAL FAIL  **Pass:** 9

| Field | |
|---|---|
| **Location** | `Assumptions!B34` |
| **Report says** | `B34`: *"Permanent, at the three-year average."* Study §1.9: *"That is NOT the three-year average, and this edition no longer calls it one."* |
| **What is correct** | The three-year average is 6.52%. 5.25% is struck marginally above the 5.15% mean of the two non-outlier years. The study and the bibliography both state this correctly; the workbook does not. |
| **Why it failed** | A retracted label surviving in the delivered model, on the study's own nominated contested judgement. |
| **Impact** | **Nil** — 6.52% would give EGP 24.55, and the study publishes that reading. |
| **Correct method** | Copy the corrected label across. |

---

### 23 · A table that says it is summed from its own column is not

**Plane:** Logic  **Severity:** PARTIAL FAIL  **Pass:** 9

| Field | |
|---|---|
| **Location** | Study Table 3; §1.6 |
| **Report says** | *"the disclosed revenue split, each total SUMMED from its own column"* — FY2025 total 9,302. §1.6: *"The channel disclosure puts domestic revenue at EGP 6,286 million."* |
| **What is correct** | 1,943 + 3,591 + 751 + 2,967 + 49 = **9,301**. The three domestic rows sum to **6,285**. The FY2024 column does foot, at 7,364. The model's own separate-company total is 9,301.478. |
| **Why it failed** | Rounding of the printed components, under a caption that promises the total is their sum. |
| **Impact** | **Nil** — under 0.02%. |
| **Correct method** | Print one more significant figure, or state that rows are rounded independently. |

---

### 24 · The Q1 finance-cost movement is stated two different ways

**Plane:** Disclosure  **Severity:** PARTIAL FAIL  **Pass:** 9

| Field | |
|---|---|
| **Location** | Study Headline, §1.7 and Table 17; bibliography input `int path` |
| **Report says** | Study, three times: *"financing expense of EGP 312.9 million ran DOWN **6.1%** year on year."* Bibliography: *"312.862 of financing expense in three months, DOWN **6.9%** year on year."* |
| **What is correct** | Not determinable from the delivered artefacts — the prior-year quarter's finance cost is not registered anywhere in the three documents. One of the two is wrong. |
| **Why it failed** | A figure appearing in more than one place is not identical, on the observation that carries the study's decision not to expense the EGP 551m of capitalised interest. |
| **Impact** | **Nil** — the model is calibrated to the level (1,250), not the change. |
| **Correct method** | Register the comparative and compute the change once. |

---

### 25 · The three-month check date is 94 days after the anchor

**Plane:** Logic  **Severity:** PARTIAL FAIL  **Pass:** 10

| Field | |
|---|---|
| **Location** | Study Table 14; `Monte Carlo!C4` |
| **Report says** | Anchor 2026-08-06; one-month check 2026-09-06; three-month check **2026-11-08**, described as *"a calendar date, resolved to the exchange's first real trading session."* |
| **What is correct** | The one-month date is +31 days, exactly one calendar month. Three calendar months is 2026-11-06 (a Friday); the date used is +94 days. The stated resolution rule does not produce it. |
| **Why it failed** | The horizon the band is labelled with is not the horizon it was simulated over. |
| **Impact** | **Negligible** — roughly 1% on the band width. |
| **Correct method** | Use the exchange calendar consistently, or state the horizon in days. |

---

### 26 · Three promised sensitivities are not delivered, and the largest driver has no grid at all

**Plane:** Disclosure  **Severity:** PARTIAL FAIL  **Pass:** 12

| Field | |
|---|---|
| **Location** | `Sensitivity` sheet; study §1.9; bibliography inputs `peer pe regional`, `assoc multiple`, `assoc norm` |
| **Report says** | The bibliography states that the peer leg *"is run across a 13–26 times band rather than on a point"*, that *"the enterprise-to-equity bridge is sensitised on"* the associate multiple, and that the associate normalisation *"leg is sensitised across"* 250 and 52.5. |
| **What is correct** | None of the three grids exists in the delivered workbook or study. The seven grids that do exist cover the cost of equity, terminal growth, beta, the provision charge, the exchange rate, domestic *volume* and the depreciation rate. There is no grid on the domestic *price* — the driver this audit finds is worth +182% of the centre (finding 01). |
| **Why it failed** | Disclosed ranges that were not produced, and the risk display omits the one input that dominates it. |
| **Impact** | **Nil on value**; the published risk display understates the model's true sensitivity. |
| **Correct method** | Produce the three promised grids and add a domestic-price grid. |

---

### 27 · The 2022 leg of the multiple history uses a year-end count under a rule that says weighted average, with no corporate-action check

**Plane:** Input  **Severity:** UNVERIFIABLE  **Pass:** 10

| Field | |
|---|---|
| **Location** | `Relative & Normalized!C17`; `Assumptions!C4`; study §1.3 |
| **Report says** | §1.3: *"Each year divides that year's audited attributable profit by that year's own weighted-average share count."* The 2022 leg uses `C4`, labelled *"Shares in issue at 31 December 2022"* = 99.1705m. |
| **What is correct** | Two open questions. The 2022 leg uses a closing count, not a weighted average, against the stated rule. And the count rose from 99.17m to 148.76m during 2023 — if that increase was a bonus or stock-dividend issue, the 2022 close of EGP 28.08 requires adjustment and the 4.74× leg is overstated by up to a third; if it was a cash rights issue at market, no adjustment is due. |
| **Why it failed** | Could not be resolved: the nature of the 2023 capital increase is not registered in any of the three documents, and the capital note was not reachable in this audit. The 2025 increase from 148.76m to 168.76m *is* documented as a 20m-share issue approved by the listing committee. |
| **Impact** | **Up to −0.4× on the four-year mean multiple**, worth roughly EGP 3 on the relative lens and nil on the two centres. |
| **Correct method** | State the nature of the 2023 increase and adjust the pre-2023 closes if it was a bonus issue. Resolved by the FY2023 capital note. |

---

## Section C — Arithmetic reconciliation appendix

Independent recomputation beside the report's figures, **including every line that matched**. The model was rebuilt from the workbook's formula text and evaluated without reference to the published answers.

### C.1 — Cost of capital

| Line | Construction | Report | Recomputed | Δ |
|---|---|---:|---:|---:|
| **First-year discount rate** | | | | |
| Normalised risk-free | 23.00% − 3.42% | 19.58% | 19.5800% | 0 |
| Cost of equity, swap basis | 19.58% + 0.629 × 9.5164% | 25.57% | 25.5658% | 0 |
| Cost of equity, rating basis | 17.0298% + 0.629 × 13.4806% | 25.51% | 25.5091% | 0 |
| Hard-currency debt, local-equivalent | 1.075 × 1.045 − 1 | 12.34% | 12.3375% | 0 |
| Cost of local-currency debt | stated: 23.00% + 250bp | 24.81% | **25.50%** | **−69bp** |
| Blended marginal cost of debt | 49.80% × 24.81% + 50.20% × 12.3375% | 18.55% | 18.5484% | 0 |
| Cost of debt after tax | × (1 − 22.5% statutory) | 14.38% | 14.3750% | 0 |
| Equity weight, net-debt basis | 21,482.6 ÷ 28,846.9 | 74% | 74.4711% | 0 |
| **WACC, year one** | 0.744711 × 25.5658% + 0.255289 × 14.3750% | **22.71%** | **22.7089%** | **0** |
| WACC, gross-debt basis | published alternative | 22.31% | 22.3144% | 0 |
| **Terminal discount rate** | | | | |
| Terminal risk-free | 7.0% inflation + 5.5% real (bibliography) | 12.50% | 12.5000% | 0 |
| — per `Assumptions!B56` | 5.0% inflation + 5.5% real | 12.50% | **10.50%** | **+200bp** |
| Terminal cost of equity | 12.5% + 0.629 × 7.0% | 16.90% | 16.9030% | 0 |
| Terminal cost of debt, after tax | [49.80%×15% + 50.20%×(1.065×1.03−1)] × 0.775 | 9.56% | 9.5610% | 0 |
| Terminal debt weight | 7,364.3 ÷ 28,846.9, market values | 25.5% | 25.5289% | 0 |
| **Terminal WACC** | 0.744711 × 16.9030% + 0.255289 × 9.5610% | **15.03%** | **15.0287%** | **0** |
| **Glide and factors** | shape from the normalised risk-free path, rebased to its own endpoints | | | |
| Discount rate, FY2026E–30E | terminal + glide × (year one − terminal) | 22.71 / 20.65 / 18.40 / 16.53 / 15.03 | 22.7089 / 20.6484 / 18.4006 / 16.5274 / 15.0287 | 0 |
| Discount factor | previous ÷ (1 + rate), year-end, compounding | 0.8149 / 0.6755 / 0.5705 / 0.4896 / 0.4256 | 0.81494 / 0.67547 / 0.57049 / 0.48958 / 0.42561 | 0 |

### C.2 — The free-cash-flow waterfall, Frame A (EGP million)

| Line | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E | Δ |
|---|---:|---:|---:|---:|---:|---:|
| Revenue — recomputed | 10,694.5 | 12,611.6 | 14,621.5 | 16,636.8 | 18,608.0 | 0 |
| Revenue — as published | 10,694 | 12,612 | 14,621 | 16,637 | 18,608 | |
| EBITDA | 2,414.9 | 2,679.0 | 3,037.2 | 3,394.2 | 3,713.4 | 0 |
| Depreciation and amortisation | (304.0) | (425.2) | (445.8) | (437.3) | (423.1) | 0 |
| EBIT | 2,110.9 | 2,253.9 | 2,591.4 | 2,956.9 | 3,290.3 | 0 |
| NOPAT at 23.5% effective | 1,614.8 | 1,724.2 | 1,982.4 | 2,262.0 | 2,517.1 | 0 |
| Add back D&A | 304.0 | 425.2 | 445.8 | 437.3 | 423.1 | 0 |
| Less capital expenditure | (1,336.8) | (567.5) | (511.8) | (532.4) | (558.2) | 0 |
| Less increase in working capital | (910.3) | (1,019.9) | (868.9) | (877.3) | (829.4) | 0 |
| **Free cash flow to the firm** | **(328.3)** | **562.0** | **1,047.6** | **1,289.7** | **1,552.6** | **0** |
| Present value | (267.5) | 379.6 | 597.7 | 631.4 | 660.8 | 0 |
| **Sum of present values** | \-- 2,001.95 against a published 2,002 -- | | | | | **0** |

### C.3 — The terminal block, and the implied asset life against the disclosed useful life

| Line | Cell & nature | Delivered | Rebuilt from the model's own rows | Δ |
|---|---|---:|---:|---:|
| Invested capital, FY2030E | `B18` · formula | 19,773.1 | 19,773.12 | 0 |
| Return on invested capital, FY2030E | `B19` · formula, **referenced by nothing** | 12.73% | 12.73% | 0 |
| Terminal depreciation catch-up | `B20` · formula, parked construction × 6.2% | 192.69 | 192.69 | 0 |
| Terminal NOPAT | `B21` · formula | 2,369.67 | 2,369.67 | 0 |
| Add book depreciation | `B22` · **typed literal** | 423.085728 | 423.085728 | 0 |
| Less maintenance at current cost | `B23` · **typed literal** = 423.0857 × 1.07^6.9 | (674.802126) | (674.802125) | 0 |
| Less capital behind real growth | `B24` · **typed literal** | (0.000000) | (0.000000) | 0 |
| Less inflation on working capital | `B25` · **typed literal** = NWC × 7.000% | (717.450174) | (717.450174) | 0 |
| **Terminal free cash flow** | `B26` | **1,400.51** | **1,400.51** | **0** |
| Terminal value | 1,400.51 × 1.07 ÷ (15.0287% − 7%) | 18,664.9 | 18,664.92 | 0 |
| Present value of terminal value | × 0.42561, the year-five factor | 7,944 | 7,944.04 | 0 |
| TV ÷ core enterprise value | 7,944 ÷ 9,946 | 80% | 79.87% | 0 |
| TV ÷ total enterprise value | 7,944 ÷ 12,937 | 61% | 61.41% | 0 |
| **Asset life** | | | | |
| Disclosed weighted useful life | note 3.1 lives × note 4.1 gross cost, per bibliography | 13.8 yrs | 13.8 yrs | cited |
| Life implied by the terminal maintenance line | 2 × ln(1.59495) ÷ ln(1.07) | — | 13.80 yrs | matches disclosure |
| Life used across the explicit window | 1 ÷ 6.2%, no note cited | 16.13 yrs | **13.8 disclosed** | **+2.3 yrs** |
| Life implied by 1 ÷ g, if the identity were used | 1 ÷ 7% | — | 14.29 yrs | no specification error |
| **Reinvestment** | | | | |
| Reinvestment the sheet applies | 1 − 1,400.51 ÷ 2,369.67 | — | 40.9% | |
| Reinvestment the study declares | g ÷ ROIC = 7.00 ÷ 12.73 | 55.0% | 54.99% | **−14.1pp applied** |
| Terminal real growth | 7% nominal vs 7% long-run inflation | 0% | 0% | coherent with B24 = 0 |

### C.4 — The enterprise-to-equity bridge (EGP million; per share on 168.75575m)

| Line | Report | Recomputed | Report /sh | Recomputed /sh | Δ |
|---|---:|---:|---:|---:|---:|
| Present value of five years of FCFF | 2,002 | 2,001.95 | 11.86 | 11.863 | 0 |
| Present value of the terminal value | 7,944 | 7,944.04 | 47.07 | 47.073 | 0 |
| **Core enterprise value** | **9,946** | **9,946.00** | **58.94** | **58.937** | **0** |
| Add earning associates, 250 × 11.0× | 2,750 | 2,750.00 | 16.30 | 16.297 | 0 |
| Add active-ingredient company at cost | 228 | 228.49 | 1.35 | 1.354 | 0 |
| Add assets held for sale | 12 | 12.33 | 0.07 | 0.073 | 0 |
| **Total enterprise value** | **12,937** | **12,936.81** | **76.66** | **76.661** | **0** |
| Less net debt (31 Dec 2025 audited) | (7,364) | (7,364.30) | (43.64) | (43.639) | 0 |
| Less non-controlling interests (31 Mar 2026) | (4) | (4.00) | (0.02) | (0.024) | see 13 |
| **Equity value — Frame A** | **5,569** | **5,568.51** | **33.00** | **32.9975** | **0** |
| **Equity value — Frame B** | **8,384** | **8,384.05** | **49.68** | **49.6789** | **0** |
| Workbook headline (`Sensitivity!D5`) | \-- 32.99747064299516, equal to the document headline -- | | | | **0** |

The bridge foots: every line sums to the stated equity value, and that value divides to the stated per-share figure on every row. The bridge does mix two consolidation perimeters — December net debt against a March minority — which the study discloses in Table 19 and prices at about EGP 3.04 a share.

### C.5 — The other three lenses, and the page-level checks

| Item | Construction | Report | Recomputed | Δ |
|---|---|---:|---:|---:|
| Forecast return-on-equity path | attributable profit ÷ average equity | 13.7/14.5/17.1/19.1/20.1 | 13.68/14.54/17.12/19.09/20.05 | 0 |
| Sustainable return | mean of the last three | 18.75% | 18.7547% | 0 |
| Justified price-to-book | (18.7547 − 7) ÷ (16.903 − 7) | 1.19× | 1.18698× | 0 |
| **Book-value lens** | 1.18698 × EGP 37.00 | **43.91** | **43.9126** | **0** |
| Own traded multiple history | year-end close ÷ audited EPS | 4.7/6.6/6.2/8.7 | 4.74/6.61/6.23/8.71 | 0 |
| Four-year mean | average | 6.57× | 6.5724× | 0 |
| Justified forward multiple | 62.68% payout ÷ 9.903% | 6.33× | 6.3290× | 0 |
| Peer reference, adjusted | 21.35 × (10% − 7%) ÷ (16.903% − 7%) | 6.47× | 6.4677× | 0 |
| **Relative lens** | average of 34.55 / 56.15 / 55.25 | **48.65** | **48.65** | **0** |
| Three-year average operating margin | 23.50% / 20.14% / 25.06% | 22.9% | 22.9004% | 0 |
| Normalised earnings per share | (0.229 × 12,612 − 2 − 1,210) × 0.765 + 232, ÷ shares | 8.97 | 8.9728 | 0 |
| **Normalised-earnings lens** | 8.9728 × 62.676% ÷ 9.903% | **56.78** | **56.789** | **0** |
| **Market data and page checks** | | | | |
| Market capitalisation | 127.30 × 168.75575m | 21,483 | 21,482.6 | 0 |
| Enterprise value | 21,482.6 + 7,364.3 + 4.0 | 28,851 | 28,850.9 | 0 |
| Trailing P/E, both counts | 127.30 ÷ (1,441.66 ÷ 168.756 / 162.016) | 14.90× / 14.31× | 14.902× / 14.304× | 0 |
| Share count foots | EGP 1,687,557,500 ÷ EGP 10 par | 168,755,750 | 168,755,750 | 0 |
| 20-day moving average | mean of the 20 closes printed in bibliography B6 | 101.58 | 101.5775 | 0 |
| The 44% two-session move | 104.00 → 149.76, two sessions at the 20% limit | 44% | +44.0% = 1.20² | 0 |
| Beta standard error, implied | β × √((1−R²) ÷ (R²(n−2))) | 0.07112 | 0.07113 | 0 |
| Every Q1-2026 cell in Table 9 | 10 lines, annualisation and ratios | all | all reproduce | 0 |
| Seven sensitivity grids, centre cells | each = the base case | 33.00 | 32.99747 ×7 | 0 |
| Table 12, all 25 cells | rounded from the workbook grid | 17 to 48 | all match | 0 |
| Balance sheet, forecast columns | assets − liabilities and equity | 0 | 0, borrowings the plug | 0 |
| Equity roll-forward | prior + attributable × 60% | 6,777 → 10,369 | 6,777.5 → 10,369.4 | 0 |
| Appendix A.1 operating profit | from the rows the table prints | 2,110.9 | **2,175.5** | **−64.6** |

### C.6 — Probabilistic content (Pass 10)

| Check | Result |
|---|---|
| Percentiles monotonic, both horizons | **Pass** — 103.80 < 120.56 < 131.69 < 143.94 < 167.17; 94.40 < 118.42 < 135.30 < 154.39 < 193.82 |
| Median inside the range, consistent with P(above anchor) | **Pass** — medians 131.69 and 135.30 above the 130.05 anchor; P(above) 54% and 58% |
| Every "X% chance above Y" follows from the percentiles | **Pass** — all four ±10% probabilities sit correctly against the 25th and 75th percentiles |
| Touch ≥ finish on all four pairs | **Pass** — 43>26, 64>39, 33>19, 48>23 |
| Lens independence | **Pass** — the fair value does not feed the simulation drift; §6 states plainly that both centres sit below the entire three-month band rather than reconciling them |
| Series screened for the exchange daily limit | **Pass** — maximum single-session move in the published tail is exactly +20.00%, twice |
| Calibration evidence complete | **Pass** — all three window sets published including the two that score negative; Tables B7/B8 internally consistent (band coverage reproduces from the histograms); the study states the method is indistinguishable from a random walk |
| Horizon labelling kept distinct | **Pass** — §6 separates the price band from the valuation explicitly |
| Support below the stated close | *Partial* — the ladder is internally ordered, but struck on a different close from the narrative (21) |
| Series current with the answer | **Fail** — ends 6 August against a 3 September valuation (05) |
| Corporate actions adjusted before indicators | *Unverifiable* for the 2023 capital increase (27) |

---

## Section D — Construction register

What the report declares against what it actually does. The most serious findings live in the gap.

### The primary lens and the treatment of the others — **partly agree**

**Declares:** Five readings, two centres, never averaged. The centre is the cash-flow lens carrying a 50% weight beside book at 20%, relative at 15% and normalised at 15%. Three lenses "do not turn on the judgement at all."

**Does:** The centre is the *unweighted* cash-flow reading; the declared weights produce 41.10 / 49.44, which the same table prints as the retired blend (14). The relative lens is built on an average of the two frames (15), so it does turn on the judgement. The two centres themselves are correct and are genuinely never averaged.

### The terminal construction — **do not agree**

**Declares:** "A terminal value on the growth-over-return reinvestment identity," with the return computed from the model's own final year and reinvestment at 55.0% of terminal profit after tax. The whole block is live and the claim was tested.

**Does:** A maintenance-capex terminal built from four typed constants, reinvesting 40.9%. The computed return on invested capital is referenced by nothing (02, 07). Every constant is the right number for the delivered drivers, and none of them moves. Run as declared, the answer is EGP 21.77–24.00, not 33.00.

### The cost-of-capital path — **partly agree**

**Declares:** Country risk charged once; a glide from today's crisis rate to a normalised terminal; market-value weights; one tax rate throughout; risk-free and share price on one date.

**Does:** The normalisation, the glide, the weights and the terminal build all reproduce exactly and are properly constructed — this is the strongest part of the study. But the local cost of debt is still built on the previous edition's yield (10), the tax shield still uses the statutory rate (17), and the risk-free and the price are 28 days apart, not one date (04).

### The currency split of the debt book — **agree**

**Declares:** Split from borrowings note (17) by lender and currency; the local tranche floored at the sovereign; the hard-currency tranche carried at local-equivalent cost with the depreciation taken from the model's own inflation differential.

**Does:** Exactly that. 49.80% / 50.20%, the hard-currency coupon compounded with 4.5% expected depreciation, and the effective-rate cross-check computed on interest-bearing borrowings (1,275.3 of facility interest, separated from the 1,332.9 finance-cost line that includes commissions) over average gross debt. Both limbs of the trap are closed. The floor's arithmetic has drifted (10); the construction has not.

### The inflation path and every escalator derived from it — **do not agree**

**Declares:** One escalator per physically distinct cost line, each derived from a named path; the currency derived by purchasing-power parity from the inflation path, never hand-set; administered prices tracking inflation with no real gain; margins an output.

**Does:** The cost side is exactly as declared and genuinely well built — five distinct lines, five distinct escalators, depreciation excluded so it enters once, and the currency path reproducing the inflation differential to four decimals year on year. The *price* side does not: it runs 11.0, 4.0, 1.5, 1.0 and 1.5 points below the model's own inflation path every year, a 15.9% cumulative real cut, under a basis note in both artefacts saying it tracks inflation (01). The margin decline the model reports as an output is the artefact of that one mismatch.

### The forecast anchor — **agree**

**Declares:** Anchored on the latest reviewed period; the first forecast year reset to the Q1-2026 outturn on revenue, capital expenditure and finance cost; the whole window tested against the quarter line by line.

**Does:** It does. FY2026E revenue sits 2.9% above the quarter's own seasonal read rather than below it; capital expenditure and finance cost are reset upward and downward respectively to the quarter; Table 9 tests ten lines including the bottom one and reports the −31% miss on attributable profit rather than claiming a hit. The base year is a full audited year, there is no fiscal-year change, and the share count foots to the capital note.

### The bridge — **partly agree**

**Declares:** Associates on earnings rather than carrying value because carrying value is not a usable proxy; the pre-revenue company on its own line at cost; the minority post-deconsolidation; the mixed perimeter disclosed and priced.

**Does:** The structure is right and the bridge foots to the pound. But the associate multiple escapes the cost-of-equity adjustment the study applies to the peer multiple one page earlier and sits above the one observable listed comparable (11); the minority is deducted at book while the model charges 18 a year against it (13); and the bridge stands on the December balance sheet rather than the March one, which the study discloses and prices at about EGP 3.04 a share.

### The evidence base and its register — **do not agree**

**Declares:** "Every figure in this study traces to a numbered source in the accompanying bibliography." Four consecutive audited years plus a reviewed interim, all from the company's own documents; three official sources logged as unreachable.

**Does:** The input register (278 rows, each with value, source, date and layer) is current and is the strongest document in the package — it carries its own falsifiers, its own failed searches and its own corrections. The document register, the judgements register and the negative-results register are the previous edition's and contradict the study on eight material points (09). The fallback on the unreachable sources is properly declared throughout, and nothing is claimed as audited that is not.

---

## Section E — Verdict summary

### Counts by pass

| Pass | Total | Partial | Unver. | Findings | Notable passes |
|---|---:|---:|---:|---|---|
| 1 · Input verification | 1 | 1 | — | 09, 23 | Base year full and audited; no fiscal-year change; share count foots to the capital note; cost-of-sales note split into five real lines |
| 2 · Market data | 2 | — | — | 03, 04 | Price × count = market capitalisation; both trailing multiples published with their share-count basis |
| 3 · Cost of capital | 1 | 2 | — | 10, 16, 17 | Country risk charged exactly once; both bases published and agreeing to 6bp; effective borrowing rate on the right denominator; rate not held flat; terminal on the year-five factor |
| 4 · The terminal value | 1 | 1 | — | 02, 12 | Terminal cash flow positive; one FCF definition; TV share disclosed on both bases as a bridge line; real growth coherent with the zero growth-capital charge; maintenance rests on a genuinely disclosed life |
| 5 · Macro coherence | 1 | — | — | 01 | Currency derived from the inflation differential, not hand-set; one escalator per driver class, genuinely implemented; depreciation excluded from the unit cost so it enters once |
| 6 · Forecast anchoring | — | — | — | none | Anchored on the reviewed quarter in both directions; the whole window tested, not just year one; margins genuinely an output of a unit build; guidance scored, not consumed |
| 7 · Lens architecture and the bridge | — | 4 | — | 11, 13, 14, 15, 20 | Peer multiple non-circular and cost-of-equity adjusted with the unadjusted figure shown; bridge foots; no lens clamped; book value not weighted into a central |
| 8 · Calculation verification | — | — | — | none | **Clean.** Every waterfall line, discount factor, present value, terminal, bridge and per-share figure reconciles; the workbook headline equals the document headline to eight decimals; all seven sensitivity grids reconcile to the base at their centre |
| 9 · The page a reader receives | 3 | 6 | — | 05, 06, 08, 18, 19, 21, 22, 23, 24 | Sign convention consistent throughout; the "best operating year" and "four-year mean" claims check out against the filings as registered |
| 10 · Probabilistic and technical | — | 2 | 1 | 21, 25, 27 | Percentiles monotonic; every probability follows; touch ≥ finish; limit screen holds; all three calibration sets published including the negative ones; lenses independent |
| 11 · The answer itself | — | — | — | see below | The gap is computed, the reverse read is published in observable units, and the ramp and reinvestment behind it are both stated |
| 12 · Completeness sweep | — | 1 | — | 12, 26 | The reviewed interim is consumed, the deconsolidation is carried through both halves, and the operating asset base is neither stale nor decorative — capacity, utilisation and pack counts all feed the model |

### Pass 11 — the reverse read

The centre sits 74% below the market, which is a high-prior-of-defect region. Solving the published model for EGP 127.30 on one driver at a time, everything else held at its published value:

| Driver | Required | Carried | Believable? |
|---|---:|---:|---|
| **Domestic price growth** | **12.52% a year** | 5.0–8.0% | **Yes** — below the 16% and 12% the model's own CPI path applies in FY2026–27 |
| Terminal growth | 12.22% | 7.00% | No — 5.2pp above terminal inflation |
| Terminal risk-free | 5.77% | 12.50% | No — implies a −1.2pt real rate |
| Provision charge | −8.88% of revenue | 5.25% | No — a permanent net credit |
| Beta | no solution ≥ 0 | 0.629 | No |

Four of the five reverse reads are absurd, which is the study's case. The fifth is not. The one driver that closes most of the gap is the one whose own basis note says it should already be doing so, and full pass-through alone takes the centre to EGP 93.16 — 73% of the traded price — without touching the plant the study declines to value. That is evidence against the *size* of the disagreement, not against its direction.

### Direction of the contested judgements

Twelve judgements worth more than 5% of value.

- **Four resolve conservatively** — the permanent-provision frame, the in-index beta, no revenue for the biologicals plant, and the real price cut.
- **Seven resolve toward value** — the 40.9% terminal reinvestment against a declared 55%, the 16.13-year life against a disclosed 13.8, the unadjusted 11× associate multiple, the minority at book, the normalised lens reversing the depreciation step, the December bridge, and the real currency appreciation.
- **One is two-sided by construction** and audited on both branches: Frame A and Frame B breach on the same findings and by the same proportions.

So there is no single-direction lean, and the protocol's flag does not fire. The pattern that does emerge is different and worth stating: **the conservative judgements are the disclosed ones and the value-positive judgements are the undisclosed ones.** Three of the four conservative calls are showcased in the caveat table, one with its price overstated tenfold; five of the seven value-positive calls appear nowhere on the page, and two are contradicted by the page.

### The three most valuation-critical findings

1. **The domestic price escalator (01).** A 15.9% cumulative real price cut under a basis note in both artefacts saying prices track inflation, while 68.4% of the cost stack escalates through that same inflation. Worth +182%. It is not disclosed, not sensitised, and larger than both judgements the study nominates as its own crux.
2. **The terminal is not the declared construction (02).** 80% of core enterprise value rests on four typed constants reinvesting 40.9%, under a declared reinvestment identity that would reinvest 55.0%. Worth −27% to −34%, and the cell that the workbook says "sets terminal reinvestment" sets nothing.
3. **The beta regressor is a coverage universe, not a market (03).** The cost of equity, the terminal cost of equity, both centres and all three non-cash-flow lenses hang off a coefficient regressed against an equal-weighted basket of the analyst's own library. Each 0.10 of beta is worth EGP 4–5 a share, and the true value cannot be established from what was delivered.

### Does the headline range survive the corrections?

**It collapses** — not in direction, but as a range.

The published field of EGP 33.00–56.78 and the two centres of EGP 33.00 / 49.68 are reproduced exactly from the delivered workbook, and the arithmetic behind them is clean to the last cell. But the two largest corrections pull hard in opposite directions and neither is small: running the terminal as the study says it is run gives EGP 21.77, and running the domestic price as the study says it is run gives EGP 93.16. A field that admits EGP 22 and EGP 93 on the report's own stated rules is not a EGP 33–57 field. The five readings agree with each other because four of them share the same cost of equity, the same terminal cost of equity and the same growth rate — their clustering measures shared inputs, not independent confirmation.

Two things nonetheless survive intact and should be said plainly. The **direction** survives: no combination of corrections found here reaches EGP 127.30 on believable inputs, and the study's central observation — that the market is paying about 74% of the share price for a plant with no disclosed revenue — is correct as stated and correctly framed as a question the study declines to answer. And the **machinery** survives: the cost-of-capital build, the currency-tranche treatment, the unit-cost build, the forecast anchoring on the reviewed quarter, the probabilistic calibration and the bridge are all constructed the way the discipline requires, and several of them close traps that most models of this kind leave open. This is a careful piece of work whose most consequential errors are all of one kind — the delivered artefacts have stopped describing themselves.

---

*Audit performed 18 September 2026 against the three delivered artefacts. No primary source was reachable from this environment, so no figure was re-traced to an original filing; every verdict above rests on internal evidence or on recomputation. The model was rebuilt independently from the workbook's formula text and reproduces the published Frame A centre as EGP 32.9975. Impacts are single-item re-runs of the delivered model with everything else held at its published value; they are not additive and no alternative valuation is proposed.*
