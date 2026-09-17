# PHDC — response to the forensic audit of the 17-09-2026 edition

Critique_Response_Prompt.md v2, run in order. **Nothing is implemented. This is the step-8 report.**

- Audited document: `PHDC_Valuation_Study_17-09-2026` (27pp), `PHDC_Valuation_Model_17092026.xlsx`
  (16 sheets), `PHDC_Bibliography_17-09-2026` (125-row register), `GAP_REVIEW_17-09-2026.md`,
  `rebuild_ledger.json`. Supplied by the principal; **none of the five is in this repository.**
- Delivered central: **EGP 13.9129**. Price used: EGP 14.40. Gap −3.38%.
- The model was rebuilt independently from the workbook's own cells
  (`scratchpad/v17/model/phdc.py`) with no reference to the published answer. It reproduces
  **EGP 13.9129**, the 15-year PV of 44,489.4 against 44,489.5, the bridge to 39,789.7 against
  39,789.8, and **all 25 sensitivity cells to the cent**. Every price below is computed on that
  rebuild, one lever at a time.

---

## 0 · What the repository says about the document being audited

Established before any finding was assessed, because it changes what several of them mean.

| | Audited 17-09 edition | Committed repo (HEAD, 14-09) |
|---|---|---|
| `edition.py` EDITION | — (not in repo) | **2026-09-10** |
| central | **13.9129** | **21.0897** |
| terminal cost of capital | **16.1547%** | **14.9751%** |
| expansion WACC | 25.11% (swap) / 26.10% (rating) | 24.96% (swap) / 25.83% (rating) |
| bridge balance sheet | 30-Jun-2026 figures, labelled 31-Mar | 31-Mar-2026 figures |
| `rebuild_ledger.json` start_value | **17.847764793737** | — |

`git log` on `study_numbers.json` returns exactly two states: `080fa1d` (edition 2026-09-02,
central **17.847764793737**) and `78d6f1e` (edition 2026-09-10, central **21.08966329162309**).

**The 17-September rebuild began from 17.847764793737 — the 2 September central, to twelve
decimal places.** It did not begin from the live number. The workbook it delivered says so in
plain text: `READ FIRST!A2` = *"Edition of 2 September 2026. Supersedes 30 August 2026."*, and
`Assumptions!C28` is stamped *"As at this build date (30-Aug-2026)"*. The study's READ FIRST
page likewise says it *"supersedes the edition of 30 August 2026"* and moves the central *"from
EGP 10.94 to EGP 13.91"* — the 2-September edition's own change-log with one number swapped.

So the 17-September edition is the **2-September** edition re-struck on three levers, and it
silently discards the 3-September and 10-September editions, including the 10-September
recalibration that replaced the terminal cost of capital of 16.15% with 14.97% read off the
house Egyptian macro path. The audit's largest finding (row 1) is aimed at that 16.1547%
terminal. It is right that the number is underived. It does not know that this house
**replaced** the number a week before the edition date.

---

## 1 · Self-audit, done before the critique was read in detail

Eleven findings. The five marked **NEW** are not in the audit's 51.

| # | Finding | Price (EGP/sh) | Also in the audit? |
|---|---|---|---|
| **SA-1** | **The rebuild reverted the 10-Sep terminal recalibration.** It discounts years 5–15 and the terminal at 16.1547% — the rate this house retired on 10-Sep in favour of 14.9751% off the house macro path. The audit's row 1 attacks the *derivation*; nobody noticed the number is also contrary to standing house policy. | **+2.4177 (+17.4%)** | **NEW** |
| **SA-2** | **The delivered workbook is stamped with the wrong edition.** `READ FIRST!A2`: "Edition of 2 September 2026. Supersedes 30 August 2026." `Assumptions!C28`: "this build date (30-Aug-2026)". Delivered as the 17-September model. | 0.00 — destroys the edition record | **NEW** |
| **SA-3** | **The spot price exists in no data file we hold.** `engine/raw_ohlc/EG/PHDC.csv` ends **23-Aug-2026 at 15.200**; there is no 2-Sep, 3-Sep or 17-Sep observation. 14.40 is typed by hand in `inputs.py:164` with a prose source string, under a register sentence reading *"no study in this series is delivered against a stale price"*. `price_map.asof.mc_data` = 2026-08-23. | 0.00 on the central; the gap, the 2.2× book, §1.9, §4 and the implied-conversion solve all rest on it | partly — row 16 says the date is wrong; it does not know the price is unsourced in our own data |
| **SA-4** | **The circular reference is three cells, not one.** `Summary Financials!B14 = "=B14/B5"`, `C14 = "=C14/C5"`, `D14 = "=D14/D5"`. All three should read row 13 (cash from operations). An off-by-one row. | 0.00 | row 10 caught D14 only |
| **SA-5** | **§1.1's "13.91 per cent" finance rate does not describe the model.** The model holds the FY2025 charge flat at 3,348 nominal for 15 years; it applies no rate to anything. §1.8 calls the same charge 12.5%. | 0.00 | row 14 catches the contradiction, not that the model applies no rate at all |
| SA-6 | The revenue anchor stayed on 1Q2026 while the conversion and margin anchors moved to 1H2026. Two anchors, two vintages, one table. Implied H2-2026 revenue 20,619.8 and H2 net profit **396.0** against H1's 2,264.8. | 0.00 directly | row 32 / construction register, from the other end |
| SA-7 | `Relative & Normalized!B9 = "=14.4000/6.6124"` and `B11 = "=4216.7/((18765.8+14624.7)/2)"` — constants inside formulas, referencing no input cell, beside a hardcoded `B10 = 6.61`. Two book values in adjacent cells. | 0.00 | row 10 / row 17 adjacent |
| SA-8 | §1.1 opens "The model runs five years"; the table beside it is 15. | −1.4708 if honoured | row 9 |
| SA-9 | C.3's named sensitivity is **inverted**: "at a 26.10% cost of capital the implied rate would be lower still". A higher discount rate requires a **higher** conversion rate for the same price — 15.43% flat at 25.11% against 7.88% on the path. | 0.00 | **NEW** |
| SA-10 | §2 and §3 are struck on 23-Aug data in a document dated 17-Sep; the one-month cone resolves 23-Sep, six days after delivery and already 25/30 elapsed. | 0.00 | row 26 catches the two-closes symptom |
| SA-11 | Maintenance capex on the disclosed useful life is worth **+1.6105 (+11.6%)** — the audit called this "small in absolute terms" with no number, its own step-3 violation, and it crosses the 5% escalation bar. | **+1.6105 (+11.6%)** | row 39, unpriced |

A self-audit that found nothing would be a failed self-audit. This one found the largest single
value item in the whole exercise (SA-1) and the two artefact defects that prove the rebuild's
provenance (SA-2, SA-3).

---

## 2 · Ledger — 52 rows, the critique's own order, no grouping

Price = effect on EGP 13.9129, one lever at a time, on the independent rebuild.
P = premise, C = conclusion. Buckets: **1** accept & implement · **2** accept defect, reject fix ·
**3** unproven→resolved · **4** reject · **5** your decision.

| # | The audit's claim, its words | P | C | Price EGP/sh | % | Verdict |
|---|---|---|---|---|---|---|
| 1 | "The model discounts at 25.1085 / 21.9107 / 19.3525 / 17.4338 / 16.1547%, then holds 16.1547%… §1.8 never mentions a path" | ✓ | ✓ | **−9.4099** flat 25.11% | −67.6% | **1** — `DCF!B16:P16` is 15 hardcoded rates; `Assumptions!B12` (26.0967%) is read by no formula. Compounded by **SA-1**. |
| 2 | "Every figure in the '31 Mar 2026 (reviewed)' column is the 30 June column" | ✓ | ✓ | **+1.3927** | +10.0% | **1** — all five named figures verified against `balance_sheet_1q26`. Price corrected: see §3.2. |
| 3 | "The 2025 cash-flow statement is published in its three totals only" is false; it is "roughly 45 line items" | ? | ✓ | 0.00 | — | **3→1** — our own record holds only three totals, so the study asserted absence it never tested. The claim must be withdrawn or evidenced. |
| 4 | "7.676460% = 1,499.0682 ÷ 19,528.1177 = CFO ÷ revenue for the six months to 30 June 2026" | ✓ | ✓ | **+2.5422** at the stated mean | +18.3% | **1** — `Assumptions!C5` reads "mean of the three published cash-flow statements". Their mean is 8.7137%. |
| 5 | "The seven rows imply σₘ of 17.05% … 31.16% — a 1.83× spread. One index over one window forces one σₘ" | ✓ | ✓ | **−3.7648** at β 1.41 | −27.1% | **1** — reproduced: 17.03–31.13%, 1.83×. |
| 6 | "Cost per unit = price per unit × (1 − 0.354669): the margin is the input and cost the output" | ✓ | ✓ | 0.00 DCF; 8.37→11.17 earnings lens | — | **1** — `DCF!B10` uses `Assumptions!B8` = 38.3224% and reaches nothing; the IS prints 35.4718%. |
| 7 | "2,035.093 = the study's revenue anchor 40,147.923 ÷ its own assumed 19.727807" | ✓ | ✓ | 0.00 | — | **1** — `Assumptions!C22`: "FY2024 revenue over c. 2,000 units delivered, escalated". Revenue is the anchor; units are the plug. |
| 8 | "Following the printed instructions literally lands at −EGP 24,484.3mn" | ✓ | ✓ | 0.00 (cross-check) | gap 15.78/sh | **1** — reproduced to −24,484.3; unprinted assets 45,118.2. |
| 9 | "The model runs fifteen (2026–2040)… Seven printed figures carry the wrong year label" | ✓ | ✓ | **−1.4708** on a real 5-yr window | −10.6% | **1** — 5-yr PV 19,064.8; terminal share 68% not 31%. |
| 10 | "B4 (44,489.5) and B5 / DCF!B21 (19,819.9) are hardcoded constants… Summary Financials!D14 is =D14/D5" | ✓ | ✓ | 0.00 | — | **1** — confirmed; **three** circular cells, not one (SA-4). |
| 11 | "The only formula reaching value is FCFF = revenue × 7.676460% + 2,594.3 − revenue × 1%" | ✓ | ✓ | 0.00 value; total evidentiary | — | **1** — exact. 175 formulas in 2,241 populated cells; 152 of them on one sheet. |
| 12 | "the three regional unit series equal the disclosed company total exactly in every one" | ✓ | ✓ | 0.00 | — | **1** — tested on our own `regions.json`: 19 of 21 year/vintage pairs EXACT, worst −2.96%. "About a third" is false. |
| 13 | PHDC's Sept-2022 presentation "publishes ten-year annual series of average selling price per sqm" | ? | ✓ | 0.00 | — | **3** — needs the live document. Even unverified, "not disclosed" must become "not current". |
| 14 | "No such rate is disclosed by PHDC and no register row exists for it" | ✓ | ✓ | 0.00 | — | **1** — plus SA-5: the model applies no rate at all. |
| 15 | "2.62 is a grid cell at 27.11%… 45.11 appears in no published cell and requires 20.4% conversion" | ✓ | ✓ | 0.00 central | range 3.6× too wide / 16% too high | **1** — reproduced: 20.4049% required; the adopted-rate range is 4.7490–38.8970. |
| 16 | "The 3 September close was 14.84; 14.40 was the 2 September close" | ✓ partly | ✓ | 0.00 central | — | **2** — our file ends 23-Aug at 15.200 and holds no September observation, so I cannot confirm 14.84, but 14.40 is unsourced in our own data (SA-3), which is worse than mis-dated. |
| 17 | "4,216.7 ÷ ((18,765.8 + 14,624.7)/2) = 25.26% — parent profit over average total equity" | ✓ | ✓ | 0.00 | — | **1** — reproduced; the paragraph condemns the mismatch it commits. |
| 18 | "31.26% is the credit-rating basis. The adopted basis is the swap basis at 29.46%" | ✓ | ✓ | 6.66→**7.19** | +8% | **1** — reproduced. |
| 19 | "31,668.3 × 1.252 × 11.658% = 4,622.3 — escalated at the orphaned 25.2% cell" | ✓ | ✓ | 0.00 | — | **1** — reproduced (4,622.2); the model's own 16% gives 4,282.6. |
| 20 | "On the 30 June 2026 book of 35,275.5… the weights are 53.86 / 46.14 and the WACC 24.99%" | ✓ | ✓ | **+0.2964** | +2.1% | **1** — reproduced: We 53.8631%, WACC 24.9880%. Price is +0.30, not "+0.2". |
| 21 | Cost of debt 25.50% [narrowed by the critic] — what survives: the 23.00% base has no register row | ✓ | ✓ | 0.00 | — | **1** — the narrowed form is right; the bibliography carries no row for it (row 38). |
| 22 | "Six months of 2026 cash flow are inside the balance sheet the bridge deducts and inside the first discounted year" | ✓ | ✗ | **+1.7544** | +12.6% | **2** — the double count is real; **the audit's −0.70 has the wrong sign.** Stubbing to 30-Jun and dropping H1-2026 FCFF *raises* value. See §3.4. |
| 23 | "The model fades unit growth 15 → 13.5 → … → 0% by 2037… the report never mentions the fade" | ✓ | ✓ | **+18.3003** on the declared flat 15% | +131.5% | **1** — `DCF!Q6`: "the disclosed run, fading to nothing". Reproduced to 32.2131. |
| 24 | "The study adopts the lowest" of 4.68% / 5.94% / 8.35% | ✓ | ✓ | −0.1834 / **−0.5351** | −1.3% / −3.9% | **5** — reproduced (13.7295 / 13.3777). A judgement with a price; the reason is owed either way. |
| 25 | "PHDC publishes a separate 'Outstanding shares'… 2,839,980,164 at 31 Mar 2026" | ? | ✓ | **+0.0977** | +0.7% | **3** — arithmetic reproduced (14.0105); the outstanding count needs the filing. |
| 26 | "§2 uses the 23 August close, §4 the valuation close" | ✓ | ✓ | 0.00 | — | **1** — 15.38/15.20 = +1.18%; 15.38/14.40 = +6.81%. |
| 27 | "Every rung sits far below what the published cone implies" | ✓ partly | ✓ | 0.00 | — | **2** — three rungs below the reflection bound (15.55: 80% vs ~100%; 16.50: 43% vs 62%), one at it, **20.00 is above it (3% vs 2.4%)**. "Every rung" is false; the ladder still needs a stated generator. |
| 28 | "A 45% range (×0.90 to ×1.30) on a lens whose stated driver is nothing" | ✓ | ✓ | 0.00 | — | **1** — and §1.2 calls book not-a-floor while the table labels it one. |
| 29 | "The earnings cross-check is 6× / 9× / 14× the model's own forecast EPS of 0.9304" | ✓ | ✓ | 0.00 | — | **1** — 6/9/14 × 0.9304 = 5.58 / 8.37 / 13.03, the published lens exactly. An echo, not a check. |
| 30 | "251 weekly observations is 4.81 years" — **WITHDRAWN by the critic** | ✗ | ✗ | 0.00 | — | **4** — withdrawn at source; the withdrawal is correct and I adopt it. Row carried, not merged. |
| 31 | "se ÷ residual volatility is near-constant across all seven rows… implying n ≈ 39–80" | ✓ | ✓ | 0.00 | — | **1** — reproduced: 0.4901 ± 0.0221; implied n 43.5–132.9; OLS se at n=251 would be 0.1018 for PHDC, not 0.1820. |
| 32 | "The release and the reviewed statements both report 9,346.1mn" | ? | ✓ | **+0.0812** | +0.6% | **3** — arithmetic reproduced; the 9,346.1 needs the filing. |
| 33 | "The FY2023 statements print 'Finance costs & interests 1,503,563,734'" | ✓ | ✓ | 0.00 | — | **1** — **our own** `phdc_walkforward/fs_parsed.json` holds `.2024.is.finance_cost = [2311.395503, 1503.563734]`. Worse than stated: `.2023` parsed as 0.000734 and the bad parse was never reconciled against the comparative that holds it. |
| 34 | "17,837.2 is real… but cited to the wrong document" | ✓ | ✓ | 0.00 | — | **1** — accept the citation fix. |
| 35 | "The 1Q2026 release publishes FY2025 regional new sales… the three no longer sum to the group (163,992 vs 215,384)" | ? | ✓ | 0.00 direct | — | **3** — needs the release. If true it breaks the study's own named integrity check. |
| 36 | "the restatement is from 3,084.4… to 4,854.8… On the originally reported figure 2024 conversion is 11.35%, not 17.87%" | ? | ✓ | mean 8.7137%→**6.5414%**, value 16.4550→**11.1310** | −20.0% | **3** — arithmetic reproduced exactly; the 3,084.4 needs the FY2024 statement. Material: it sets the top of the crux range. |
| 37 | "The opening is already net of 1Q2026 sales of 52,000 and 1Q revenue of 9,300" | ✓ | ✓ | 0.00 (row is decorative) | — | **1** — double count 42,700 confirmed; 263,000 + 129,712 − 40,148 = 352,564 as printed. |
| 38 | "not one [row] covers the bond yield, either default spread, either ERP, the beta, the tax rate, the cost of debt or the inflation path" | ✓ | ✓ | 0.00 | — | **1** — the bibliography contains **zero** occurrences of "bond yield", "tax rate", "23.00", "25.50", "13.94", "9.41", "1.0493", "0.225". |
| 39 | "The model's terminal charges 2,430.9 on a base of 4,982.3 — 48.8%… roughly 5.4× its actual rate" | ✓ | ✓ | **+1.6105** | **+11.6%** | **1** — reproduced (48.8% vs the disclosed 9.1%). **The audit called this "small" with no number; it is the fourth-largest item in the exercise.** |
| 40 | "no ten-year EGP benchmark has been auctioned since 31 May 2022" | ? | ✓ | rate-driver | — | **3** — the study's own bibliography concedes the quote is dated and carries no row for it (row 38). Must be rebuilt from tenors that trade, or sourced. |
| 41 | "The principle is right if the operating cash flow being adjusted is after interest paid" | ✓ | ✓ | **−5.0694** if removed | −36.4% | **2** — I tested the double-count hypothesis and it **fails**: the forecast CFO is built net profit + D&A + ΔWC (2,661 + 393 + 29 = 3,082), so interest is inside it and the add-back is correct in form. What survives is real and unfixed: it is held **flat at 3,348 nominal for 15 years and into perpetuity** while revenue grows sixfold. |
| 42 | Listing continuity of ORHD and EMFD | ? | — | 0.00 | — | **3** — unresolved; needs the EGX register. |
| 43 | "Nothing… defines the test, the metric, the sample or the error measure" | ✓ | ✓ | 0.00 | — | **1** — no backtest artefact accompanies the three delivered files. The test exists in `engine/phdc_walkforward/`; it was not delivered or cited. |
| 44 | "the newest disclosure of any kind is 1Q2026"; 13 filings post-date 25 June | ? | ✓ | 0.00 | — | **3** — the workbook's scoped wording is literally true of the IR site; the study's unscoped versions are not. Needs the EGX filing list. |
| 45 | "EGP 8 billion syndicated financing contract… roughly 23% of the group's gross borrowings" | ? | ✓ | rate/net-debt driver | — | **3** — needs the 20-Aug disclosure. |
| 46 | "Receivables to be collected between 2022-2034, with an average life of 5-7 years" | ? | ✓ | 0.00 | — | **3** — needs the presentation. Would test the model's 941→390-day path. |
| 47 | FY2025 release: "The claim as worded is true; the impression… is not" | ✓ | ✓ | 0.00 | — | **1** — accept as a scoping fix. |
| 48 | "The 4Q2024 release discloses FY2024 handovers twice" | ? | ✓ | 0.00 | — | **3** — but the internal half is already proved: the study **uses** the FY2024 regional unit counts (4,192 / 2,839 / 453) its own note calls unpublished. |
| 49 | "The only statement PHDC has made about FY2026 handovers is 1,200 contractual units" | ? | ✓ | 0.00 | — | **3** — `Assumptions!C21` names the disclosed run as "1,308 / 1,281 / 1,500 / 2,000"; the model starts at 2,035.093. The reader is owed the company's own FY2026 figure and the reason for rejecting it. |
| 50 | 2026 land and project transactions filed and absent | ? | ✓ | 0.00 | — | **3** — needs the filings. |
| 51 | "an Article-48 disclosure was filed and cleared" | ? | ✓ | 0.00 | — | **3** — needs the FRA statement. |
| 52 | "The FY2025 balance sheet carries a treasury contra of (101,092,107)" | ? | ✓ | see row 25 | +0.7% | **3** — extends row 25. |

**Count reconciliation: 52 rows numbered, 1 withdrawn at source (row 30) = 51 live findings.
51 raised, 51 answered, 0 unaddressed.** Matches the audit's own tally
(22 TOTAL + 25 PARTIAL + 4 UNVERIFIABLE = 51) exactly.

---

## 3 · Escalated — every item over 5% of the central, re-derived

### 3.1 · SA-1 · The terminal rate is contrary to standing house policy — **+2.4177 (+17.4%)**
The rebuild discounts years 5–15 and the terminal at **16.1547%**. On 10 September this house
replaced that construction: `wacc_result.json` `schedule.rating.wacc_terminal` = **14.9751%**,
built from `rf_terminal` 10.50% + `erp_terminal` 7.00% × β with `kd_terminal_pretax` 15.00% and
`weight_debt_terminal` 44.8952% — every component named, which is precisely what row 1 says the
16.1547% lacks. The 10-Sep edition note records the effect on its own basis: central
17.86 → 21.09, **+18.2%**. On the 17-September basis the same substitution is **+17.4%**, the
same order from an independent direction. Row 1 and SA-1 are the same defect seen from two
ends: the published rate is underived *and* superseded.

### 3.2 · Row 2 · The bridge, and an arbitration against the audit — **+1.3927 (+10.0%)**
Premise confirmed on all five figures: `balance_sheet_1q26` holds total assets
**177,979.015**, cash **9,125.128**, WIP **21,337.803**, customer advances **72,867.832**,
NCI **1,432.671** — the audit's own "true 31 Mar" column — against the study's 194,767.3 /
7,804.2 / 23,915.9 / 83,483.3 / 1,723.0.

The audit prices this at +1.45 (→ 15.36) on net debt of 23,076.3. **That figure is wrong, and
the test is internal.** Summing the study's own *eight*-line gross-debt definition at 31 March
gives **32,369.847** exactly — loans LT, notes payable LT, lease liabilities LT, banks credit
balances, credit facilities, current portion of ST loans, notes payable ST, lease liabilities ST
— matching `balance_sheet_1q26_foot.gross_debt` to three decimals. The audit's 32,201.4 is the
same definition **less the two lease-liability lines** (168.408), i.e. six lines, not eight.
Net debt at 31 March is therefore **23,244.719**, and the correct price is **+1.3927 (+10.0%)**,
not +1.45. Arbitrated on the coherence test, not on authority.

### 3.3 · Row 23 · The undisclosed growth fade — **+18.3003 (+131.5%)**
`DCF` row 6 fades 0 / 15 / 13.5 / 12 / 10.5 / 9 / 7.5 / 6 / 4.5 / 3 / 1.5 / 0 / 0 / 0 / 0%,
annotated "the disclosed run, fading to nothing". The text says "growing 15 per cent a year" and
never mentions the fade. On the declared flat rule the answer is **32.2131**. This is the largest
single lever in the document and it is invisible to a reader. It is also the one large judgement
that runs *against* value, which is why it survived four editions unexamined.

### 3.4 · Row 22 · Premise right, conclusion wrong — **+1.7544 (+12.6%)**, not −0.70
The double count is real: `DCF!B17 = 1/(1+B16)` discounts full-year 2026 FCFF from 1 January
while the bridge deducts a balance sheet dated 30 June. But the audit's −0.70 has the wrong
sign and shows no arithmetic. Done properly — half of 2026's FCFF, and every period stubbed
half a year — the answer is **15.6672**. Dropping half a year of discounting on fourteen later
years outweighs giving up half of 2026's modest flow. Accept the defect, reject the price.

### 3.5 · Row 41 · The add-back tested and partly cleared — **−5.0694 if removed**
I tested the audit's suspicion that the add-back double-counts. **It fails.** The forecast cash
flow is built net profit + D&A + ΔWC (2,661 + 393 + 29 = 3,082, with ΔWC as the plug), so the
3,348 finance charge is deducted inside it and adding it back after tax is correct in form.
What survives is not the form but the level: **2,594.3 flat, nominal, for fifteen years and
into perpetuity**, while revenue runs 40,148 → 243,093. That is the unfixed part, and it is
worth 5.07 a share in total.

### 3.6 · Row 39 · The item the audit called small — **+1.6105 (+11.6%)**
Maintenance capex is 1% of revenue against a nearly flat asset base, so the implied replacement
cycle degrades from 11.5 years in 2026 to **2.1 years** in the terminal — 48.8% of the base
against PHDC's own disclosed 9.1%. Rested on the disclosed life instead, the answer is
**15.5234**. The audit wrote "Small in absolute terms" with no number beside the word. It is the
fourth-largest item here and it crosses the escalation bar. Logged as **SA-11**.

### 3.7 · Row 36 · The restatement that sets the top of the range — **−2.78 at the corrected mean**
On the FY2024 statements' own originally reported CFO of 3,084.4, 2024 conversion is **11.35%**
not 17.87%, and the three-year mean **6.5414%** not 8.7137% — value **11.1310**. The study names
the 2024 restatement in §1.7 and mis-sources a *different* restatement in A.1, while the one
that sets the upper bound of its own crux range goes unnamed. Held at bucket 3 only because
3,084.4 needs the filing.

### 3.8 · Rows 1, 5, 9, 15 — confirmed to the cent
Flat 25.11% → **4.5030** (audit 4.50). Beta 1.41 on the workbook's own additive parallel-shift
convention → **10.1480** (audit 10.17). Five genuine years → **12.4421**, terminal share **68%**
(audit 12.44 / 70%). The published 45.11 requires **20.4049%** conversion (audit 20.4%), above
every year PHDC has printed. All 25 sensitivity cells reproduce only under the parallel shift,
confirming §1.9's columns are first-year rates of a shifted path, not flat discount rates.

---

## 4 · Buckets

30 + 4 + 16 + 1 + 1 = **52 rows bucketed**, of which row 30 is the critic's own
withdrawal — so **51 live findings, all bucketed, 0 unaddressed.**

**1 · ACCEPT AND IMPLEMENT (30)** — 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 17, 18, 19, 20,
21, 23, 26, 28, 29, 31, 33, 34, 37, 38, 39, 43, 47 *(+ SA-1, SA-2, SA-3, SA-4, SA-5, SA-8, SA-9, SA-10, SA-11)*

**2 · ACCEPT THE DEFECT, REJECT THE FIX (4)**
- **16** — the price is worse than mis-dated: unsourced in our own data. Fix: strike against the
  latest close the repo can source, and refresh the OHLC first.
- **22** — real double count, wrong sign. Fix: stub to the bridge date; price it **+1.7544**.
- **27** — three rungs below the bound, not "every rung"; 20.00 is above it. Fix: publish the generator.
- **41** — the add-back's *form* is correct; its *flat nominal level* is the defect. Fix the level.

**3 · UNPROVEN — RESEARCH REQUIRED (16)** — 3, 13, 25, 32, 35, 36, 40, 42, 44, 45, 46, 48, 49,
50, 51, 52. Every one needs a primary document this session does not hold. Two are already half
proved from our own files: **48** (the study uses the FY2024 unit counts its note calls
unpublished) and **3** (our record holds only three totals, so absence was asserted, never tested).

**4 · REJECT (1)** — **30**, withdrawn at source by the critic; the withdrawal is correct and I adopt it.

**5 · YOUR DECISION (1)** — **24**, the minority basis: 4.68% as delivered, 5.94% → **13.7295**,
8.35% → **13.3777**. *Recommendation: the three-year mean (5.94%).* A single-year profit share is
the same one-observation anchor the study rejects everywhere else, and it happens to be the
branch that maximises value.

---

## 5 · Your three questions, answered with measurements

**Have I taken the critique seriously enough?** It is a good audit. Of 51 live findings I accept
26 outright, accept the defect and reject the fix on 4, hold 17 for primary sources, reject 1
(its own withdrawal), and refer 1. I corrected it in four places with shown arithmetic: row 2's
price (it dropped two lease lines), row 22's sign, row 27's "every rung", and row 39's
"small" — which it never priced and which is worth 11.6%. And its largest finding is incomplete:
it does not know the 16.1547% terminal was retired by this house on 10 September.

**Is the model built bottom up?** No. Measured: the entire valuation is one line —
`FCFF = revenue × 7.676460% + 2,594.3 − revenue × 1%`. Revenue is `units × price`, and units are
the revenue anchor divided by the price, so the driver apparatus is circular and decorative. The
Segments sheet, the 5,633 units, all three regional price series, the order book and the
gross-profit and overhead rows on the DCF sheet are read by no formula that reaches the answer.

**Are the equations in Excel, with as little hardcoding as possible?** No. Of **2,241** populated
cells, **175** are formulas, and **152** of those are on one sheet. Income Statement (274 cells),
Cash Flow (365), Sensitivity (38), Segments (108), Summary (57) and Assumptions (75) hold **zero**
formulas. Balance Sheet holds 2 in 852. The bridge's two inputs and the fifteen discount rates
and the terminal value are hardcoded constants; four labelled inputs are orphaned; three cells
are circular. The workbook's own warranty — "Change a blue cell and the statements, the
discounted cash flow and the value per share all recompute" — is false as delivered.

---

## 6 · The answer, re-checked against the price [R-GAP-01]

Not a forecast — the arithmetic of the accepted items, so the gap review is scoped before work
starts. Against the only price this repository can source (**15.200**, 23-Aug-2026):

| | EGP/sh | vs 15.200 |
|---|---|---|
| As delivered | 13.9129 | −8.5% |
| + SA-1 terminal at the house rate | 16.3306 | +7.4% |
| + row 2 bridge on the March sheet | ~17.8 | ~+17% |
| + row 39 capex on the disclosed life | ~19.6 | ~+29% |
| + row 22 stub | ~21.5 | ~+41% |

**Three of the accepted items individually breach the two-sided 10% band, and together they
breach it far.** So the response cannot finish without `GAP_REVIEW_{DD-MM-YYYY}.md` across all
eight headings and a clean `scripts/check_valuation_gap.py`. Note the direction: the accepted
corrections move the answer **away** from the price, which is the opposite of the 17-September
rebuild's own movement. That rebuild moved from +23.9% above the price to −3.4% below it and
argued in its gap review that this was not fitting. The argument rested on the levers being
mandated by rules written before the move — but the same pass reverted a terminal rate this house
had replaced eight days earlier, and that revert is worth −2.42 a share in the direction of the
price. [R-GAP-04] requires the hunt for our own error before a gap is referred; here the hunt
found the error inside the rebuild itself.

---

## 7 · What implementation would take, on approval

Not started. Six artefacts, in this order:

1. **Rebase on the live edition.** Re-strike from the 10-September committed state, not the
   2-September one. Restore the 14.9751% terminal and its named construction, or amend
   [R-VCAL-02]-class policy explicitly — never by silently reverting it.
2. **Rebuild the workbook bottom up.** Wire `Fundamental Valuation!B4` to `DCF!B20`; publish the
   terminal formula in cells; derive the fifteen discount rates from a stated build; drive revenue
   from the Segments engine or drop the engine; fix the three circular cells; connect or delete
   the four orphaned inputs; put the Income Statement, Balance Sheet, Cash Flow and Sensitivity
   sheets on formulas.
3. **Re-cut every date-bearing claim.** One balance-sheet date, correctly labelled; one price,
   sourced from a refreshed OHLC file; one window length; one inflation path; the growth fade
   printed; the six-gap table reduced to what is actually undisclosed.
4. **Rebuild the bibliography** with rows for the bond yield, both spreads, both ERPs, the beta,
   the tax rate, the cost of debt and the inflation path.
5. **Fetch the 17 bucket-3 documents** and move each finding to accept or reject with what was found.
6. **Re-run every gate**, then the gap review, then report before/after on each headline.
