# EIPICO (EGX: PHAR) — response to four external critiques

Study audited: `EIPICO_Valuation_Study_09-08-2026` (2nd edition) + `EIPICO_Valuation_Model_09082026.xlsx`.
Baseline being defended: **weighted centre EGP 66.5672**, Frame A **67.2233**, Frame B **79.3291**, field 50.09–79.33.

Sources of critique, and the tag used for their findings throughout:

| tag | document | findings raised |
|---|---|---|
| **A** | Claude Cowork — *Forensic Valuation Audit* | 32 (A1–A32) |
| **B** | Claude Code — *Fail Table + Arithmetic Reconciliation* | 34 (B1–B34) |
| **C** | Gemini Deep Thinking — *Zero-Trust Adversarial Verification memo* | 8 (C1–C8) |
| **D** | Gemini Deep Research — *Quantitative Model Risk Audit* | 10 (D1–D10) |

**Reconciliation: 84 raised, 84 answered, 0 unaddressed.**

Bucket split (each finding assigned exactly one primary bucket): ① 57 · ② 4 · ③ 7 · ④ 9 · ⑤ 7 = **84**.

Every price in this document is a **whole-model re-run**, not an elasticity. `compute.py` now carries an
audit hook (`PHAR_OVERRIDE`) that replaces a named input and rebuilds the entire chain — history →
unit build → cost stack → three statements → WACC → both frames → all five lenses → weighted centre.
Structural findings that are not a single input (de-averaging, terminal depreciation, the bridge
perimeter, period-matching) are re-derived closed-form from the model's own committed numbers in
`price2.py`. Both scripts are committed; `audit_pricing.json` and `audit_pricing_2.json` hold the runs.

---

## Step 1 — Self-audit, run before the critiques were read

### The anchoring disclosure, stated plainly

**The Claude Cowork critique (A) was auto-loaded into my context in full before I could begin.** I could
not run an unanchored self-audit against that document. B, C and D I had not opened when the self-audit
below was run — they were extracted to text and their sizes printed, nothing more. Where a self-audit
item could plausibly have been absorbed from A, it is marked `[ANCHOR-RISK]`.

### What the self-audit found (SA-1 … SA-14), all mechanically verified

| # | defect | verified how | also raised by |
|---|---|---|---|
| SA-1 | Frame A provision labelled "the three-year average" is 5.25%; the true three-year mean of ratios is **6.5161%** (5.0653 / 9.2483 / 5.2346) | recomputed from the three audited income statements | A6 |
| SA-2 | Book lens written `=('Balance Sheet'!G18)*0+1.706200*'Balance Sheet'!D18`; `roe_sust` a literal `0.21896499` | read from the delivered workbook | A4, A5, B8, B9 |
| SA-3 | Forecast ROIC 11.47 / 12.19 / 13.71 / 15.14 / **16.36%** against a terminal 20% | model output | A18, B2 |
| SA-4 | DCF taxes FCFF at statutory 22.5% while the model's own effective rate is 23.5% | `Assumptions!C6` vs `DCF!B7` | A17 |
| SA-5 | Forecast balance sheet does not balance: **+1,267.4 / +1,404.8 / +1,145.4 / +701.5 / +15.4**; FY2025 balances to +0.4 | recomputed | A9, B14 |
| SA-6 | Appendix A.1 attributable-profit row prints 608/756/989/1,231/1,462 = exactly 0.6 × the model's 1,014/1,260/1,648/2,051/2,437 | recomputed | A1, B5 |
| SA-7 | Appendix A.1 finance-cost row (1,548/1,451/…) is the retired first-edition `kd_path` construction, not `int_path` | traced to the retired formula | A2 |
| SA-8 | Table 3 FY2024 channel total prints 7,478.9; the column sums to **7,364.1**. Consolidation factor 1.0149 (FY2025) vs **1.0308** (FY2024) | recomputed | A8, B13 |
| SA-9 | Key-figures EV 29,600 uses the superseded NCI 288.7; every other use is 29,315 | recomputed | A10, B12 |
| SA-10 | Peer 19.5× is neither the median nor the midpoint (**21.35×**) of the only two disclosed observations | recomputed | A7, B22 |
| SA-11 | Legs labelled "trailing P/E" applied to FY2026E EPS 6.1844, not trailing 8.5429 | read | A14 |
| SA-12 | Duplicate Table 11 and Table 17; narrative probes "79% of the cash cost stack", "EGP 428 / EGP 190", "between EGP 70 and EGP 100", "roughly EGP 700 million" all still live | programmatic scan | A16, A21, A22, A23, A25, B6, B19, B28 |
| SA-13 | Figure 8 expert centres are literals (74/86/101, 62/74/88, 96/118/141) against model values 67.22 / 63.12 / 130.05 | read from `figures.py` | A20 |
| SA-14 | Model hard-currency share **68.39%**; narrative says 79% (= API + *all* packaging, 79.44%) | recomputed | A23, B16 |

### The honest scorecard on step 1

**14 self-audit findings. 14 of them were also raised by at least one critic. Zero originals.**
Measured against the standard the procedure sets — a self-audit that finds nothing is a failed
self-audit — this one found real defects, but it produced nothing the reviewers did not. That is the
result, and I am not going to dress it up. Six of the fourteen (SA-2, SA-3, SA-4, SA-10, SA-11, SA-13)
were found by reading the delivered artefacts rather than the builders, which is the right method;
they were still not original.

**What the critics found that the self-audit missed — 21 distinct items:**
A3/B1 (the headline breaks the "never averaged" rule), B3 (terminal debt weight),
B4 (terminal NOPAT under-depreciated), B7 (a fresher Damodaran vintage exists),
A11/B10/D1 (stale risk-free print), A12/B11 (Damodaran column mislabelled),
A13/B23 (three share-count bases), A15/B26 (interest path and its mislabelled basis row),
A19 (unsourced 5.5% terminal real rate), A24 (tornado input ranges never printed),
A26/B27 (crux ramp unpublished, incremental revenue uncharged for reinvestment),
A27 (Q1 check omits the bottom line), A28/A32/B21/B33 (Monte Carlo vol vs published bands),
B15 (1,275 vs 1,332.9), B17 (Table 11 caption), B18 (terminal range misquoted),
B20 (third calibration set omitted), B24 ("core" dropped from the TV share),
B34 (FY2022 close and EPS untraceable), C3/D8 (consolidation-perimeter mismatch in the bridge),
D4 (lens-independence violation).

The two that should most have been caught internally are **A3/B1** — a rule the document states five
times, broken by its own headline arithmetic — and **C3** — a perimeter mismatch sitting in the four-line
equity bridge.

---

## Step 2 + 3 + 4 — Every finding, in each source's order, priced, premise split from conclusion

Bucket codes (step 7): **①** accept and implement · **②** accept the defect, reject the fix ·
**③** unproven → research now · **④** reject with receipts · **⑤** your decision.

Price convention: Δ to the **weighted centre 66.5672**, from a full model re-run. "nil" means a
mechanically verified **0.00 / 0.00%** — presentation or narrative only, no path into any number.

### Source A — Claude Cowork (32 findings)

| # | their words (verbatim, trimmed) | price | premise | conclusion | bucket |
|---|---|---|---|---|---|
| A1 | "The row publishes **retained earnings** under an attributable-profit label… 608 / 756 / 989 / 1,231 / 1,462" | nil (0.00, 0.00%) — appendix only | TRUE | TRUE | ① |
| A2 | "Model `Assumptions!C51:G51` = 1,250 / 1,210 / 1,150 / 1,090 / 1,030… delete the first-edition artefact" | nil | TRUE | TRUE | ① |
| A3 | "Weights of 0.25/0.25 **are** a straight average… contributing 36.64 of the 66.57 centre — 55% of the headline" | de-averaged: **63.33 / 69.81** (−3.24 / +3.24; ∓4.87%) | TRUE | TRUE | ① |
| A4 | "The lens is a frozen number, 63.1210, for every possible driver value" | nil at current inputs; **±10.15/share** of false stability under perturbation | TRUE | TRUE | ① |
| A5 | "Hardcoded literal 0.21896499… it never equals 21.90% in any year and does not 'settle' there" | at FY2030 ROE 23.08%: **67.64** (+1.07, +1.61%); at the 5-yr mean 19.72%: **64.54** (−2.02, −3.04%) | PART | PART | ② |
| A6 | "5.25% is presented as 'the three-year average'; the study's own income statement gives 6.52%" | at 6.5161%: **63.66** (−2.91, −4.37%), Frame A 60.90 | TRUE | PART | ① label / ⑤ level |
| A7 | "The midpoint — and the median — of two points is **21.35×**, not 19.5×" | at 21.35×: **66.86** (+0.29, +0.43%); leg deleted: **65.76** (−0.81, −1.22%) | TRUE | TRUE | ① |
| A8 | "1,530 + 2,664 + 634 + 2,500 + 36 = **7,364**… the factor is 1.0149 in FY2025 but **1.0308** in FY2024" | nil on the total; factor question ③ | TRUE | TRUE | ① + ③ |
| A9 | "Assets − (liabilities + equity): FY2026 +1,267.4 (+6.3%)… there is **no financing plug**" | nil on the DCF | TRUE | TRUE | ① |
| A10 | "29,600 requires NCI of 288.7 — the superseded pre-deconsolidation minority" | nil | TRUE | TRUE | ① |
| A11 | "22.70% on 21 Jul 2026; **23.00% on 6 Aug 2026** (the report's own pricing date)" | at 23.00%: **66.08** (−0.49, −0.74%) | TRUE | TRUE | ① |
| A12 | "Egypt's actual **Country Risk Premium is 9.71%**… the label is wrong" | nil (use is correct) | TRUE | TRUE | ① |
| A13 | "`IS!D27` = 1,441.66/**162.016024** = 8.898, and everything else = /168.75575 = 8.543" | ≈ **−0.08** (−0.12%) on the centre | TRUE | TRUE | ① |
| A14 | "Both are applied to FY2026E EPS of 6.1844, which is **below** trailing FY2025 EPS of 8.5429" | period-matched: **68.51** (+1.95, +2.92%) | TRUE | TRUE | ① |
| A15 | "the implied rate falls **14.21% → 11.71%**… no deleveraging is modelled or stated" | at the blended marginal 18.55%: **59.55** (−7.02, **−10.55%**) | TRUE | PART | ③ → ⑤ |
| A16 | "the model's finance cost goes 1,332.9 → **1,250 (−82.9)**… Net charge actually taken: **+103.3**, not ~700" | nil | TRUE | TRUE | ① |
| A17 | "The model concedes a 23.5% cash burden in one sheet and applies 22.5% in the cash-flow engine" | **65.98** (−0.58, −0.88%), Frame A 66.11 | TRUE | TRUE | ① |
| A18 | "Terminal ROIC of 20% is a **364bp step above** the last forecast year, asserted with no bridge" | at 16.36%: **63.78** (−2.78, −4.18%), Frame A 61.98 | TRUE | TRUE | ① |
| A19 | "The 5.5% perpetual **real** risk-free rate is asserted with no source and exceeds Egypt's real GDP growth" | rf_t 10.0%: **70.25** (+3.68, +5.53%); 9.5%: **74.31** (+7.74, **+11.63%**); 9.0%: **78.82** (+12.25, +18.41%) | TRUE | PART | ③ |
| A20 | "The experts' own published workings give **67.22**, **63.12** and **130.05**" | nil | TRUE | TRUE | ① |
| A21 | "Expert 1 = 67.22, Expert 2 = 63.12 — both **below 70**" | nil | TRUE | TRUE | ① |
| A22 | "the basis note cites two figures that do not match it… Q1-2026 actual was 13.1 (≈52 annualised) against 250 carried" | at the Q1 run-rate 52.47: **56.24** (−10.33, **−15.52%**); at the stated 3-yr mean 246.1: **66.36** (−0.20) | TRUE | PART | ① note / ⑤ level |
| A23 | "The model's own hard-currency exposure is **68.39%**… 79.44% is API plus the *entire* packaging line" | nil | TRUE | TRUE | ① |
| A24 | "for beta, provision charge, exchange-rate path, domestic volume and depreciation rate **no input range is stated**" | nil | TRUE | TRUE | ① |
| A25 | "'Table 11' labels both the Q1 forecast check and the support/resistance table" | nil | TRUE | TRUE | ① |
| A26 | "the added revenue carries **no incremental capex and no incremental working capital**… Terminal-only arithmetic requires **7,721m**" | nil on fair value; the published hurdle is understated by **16%** | TRUE | TRUE | ① |
| A27 | "**No attributable-profit row and no EPS row**, the two lines Appendix A.1 misstates" | nil | TRUE | TRUE | ① |
| A28 | "the published bands imply **49.8% (1M)** and **43.1% (3M)** — a consistent 0.79–0.80 ratio" | nil (price map) | TRUE | UNPROVEN | ③ |
| A29 | "Not reachable: EIPICO's IR annual-report link resolves to FY2019… no financial-statement item is passed" | n/a | TRUE | n/a | ① supply the filings |
| A30 | "**No price series is supplied in either document**, so no indicator can be recomputed" | nil | TRUE | TRUE | ① |
| A31 | "the return series and the composition of the '36-name local composite' are not disclosed" | nil | TRUE | TRUE | ① |
| A32 | "The coverage figures appear in neither document's data" | nil | TRUE | TRUE | ① |

### Source B — Claude Code (34 findings)

| # | their words (verbatim, trimmed) | price | premise | conclusion | bucket |
|---|---|---|---|---|---|
| B1 | "B4 = AVERAGE(B2:B3), labelled on the sheet 'Average of the two frames'" — *same defect as A3, plus the cell that names it* | see A3 | TRUE | TRUE | ① |
| B2 | "Reinvestment should be 5/16.36 = 30.6%, not 25.0%. Terminal FCFF 2,210 not 2,388" — *= A18* | see A18 | TRUE | TRUE | ① |
| B3 | "net debt 7,364 / (7,364 + equity 11,289) = **39.5%**; on market-value equity = **25.1%**. Neither is 20%" | 25.1%: **68.04** (+1.47, +2.21%); 39.5%: **72.76** (+6.19, **+9.30%**) | TRUE | TRUE | ① |
| B4 | "FY2030 closing CIP **2,947 never depreciates**. At the model's own 6.2%: +183 D&A" | **64.99** (−1.57, −2.36%), Frame A 64.08 | TRUE | TRUE | ① |
| B5 | "The printed row is exactly 60% of these" — *= A1* | nil | TRUE | TRUE | ① |
| B6 | "the narrative overstates the charge ~7×" — *= A16* | nil | TRUE | TRUE | ① |
| B7 | "ctrypremJuly26.xlsx, posted 2 Jul 2026, has Egypt: adj. default spread **5.9702%**, ERP **13.4806%**, CDS 3.42%, CDS-basis ERP **9.5164%**" | **66.53** (−0.04, −0.06%); with the 6-Aug yield too: **66.04** (−0.53, −0.80%) | TRUE (verified) | PART | ① |
| B8 | "`=('Balance Sheet'!G18)*0 + 1.706200*'Balance Sheet'!D18`… G18*0 is a dead reference" — *= A4* | see A4 | TRUE | TRUE | ① |
| B9 | "No cell in the workbook produces 0.21896499" — *= A5* | see A5 | PART | PART | ② |
| B10 | "22.700% on 21 Jul 2026, 23.000% on 6 Aug 2026" — *= A11* | see A11 | TRUE | TRUE | ① |
| B11 | "Damodaran's column heading for 13.9377% is 'Equity Risk Premium' (total)" — *= A12* | nil | TRUE | TRUE | ① |
| B12 | "Model formula C96+C97+C74 = **29,315.0**" — *= A10* | nil | TRUE | TRUE | ① |
| B13 | "Sums to 7,364… Column total does not add, by +115 (+1.6%)" — *= A8* | nil | TRUE | TRUE | ① |
| B14 | "Cash (C70) and gross borrowings (C71) are pinned at the FY2025 audited figures through FY2030" — *= A9* | nil | TRUE | TRUE | ① |
| B15 | "'expensed EGP 1,275 million of interest in FY2025'… Table 17 gives finance costs of **1,332.9** for the same year, unreconciled" | nil | FALSE | FALSE | ④ |
| B16 | "API 54.88% + 55% of packaging 24.56% = **68.4%**" — *= A23* | nil | TRUE | TRUE | ① |
| B17 | "Only net sales uses it… D&A 225, transfers 3,670, finance cost 1,251, associates 52, capex 1,299 are all plain ×4" | nil | TRUE | TRUE | ① |
| B18 | "Table 10 / `Sensitivity!B26:F30` runs EGP **47.83 to 110.21**" against a claimed "68 to 112" | nil | TRUE | TRUE | ① |
| B19 | "Expert 1 = 67.22 and Expert 2 = 63.12, both below the stated floor" — *= A21* | nil | TRUE | TRUE | ① |
| B20 | "The workbook holds a third set — post-break 2022-06-20→2026-03-24, 16 windows, score −0.01086 — which is omitted" | nil | TRUE | TRUE | ① |
| B21 | "Two vols were used: 62.90% (one-month) and 53.55% (three-month). Only the lower is stated" | nil | TRUE | TRUE | ① |
| B22 | "19.5 is neither their mean (21.35) nor the median of any disclosed set" — *= A7* | see A7 | TRUE | TRUE | ① |
| B23 | "Three share-count bases in one lens" — *= A13* | see A13 | TRUE | TRUE | ① |
| B24 | "Model computes 75.93% of **core** enterprise value… Against total EV of 18,713 it is **63.8%**" | nil | TRUE | TRUE | ① |
| B25 | "2,978.5 = associates at 250 × 11 plus the active-ingredient company at carrying cost 228.5… folded into a line labelled 'on normalised earnings'" | nil | TRUE | TRUE | ① |
| B26 | "**18.9% is neither the cost of local-currency debt (24.81%) nor the blended marginal cost of debt (18.55%) — it is the normalised risk-free rate (C90 = 18.90%)**" | nil directly; the glide it shapes is priced under A15/A19 | TRUE | TRUE | ① |
| B27 | "placing all 6,642 in FY2030 values only 9,121 — leaving 1,482 that must come from an explicit-year ramp" — *= A26* | nil | TRUE | TRUE | ① |
| B28 | "Two tables numbered 11, two numbered 17… §1.5 titled 'four methods' over five lenses" — *= A25 +* | nil | TRUE | TRUE | ① |
| B29 | "EIPICO's IR annual-report link resolves to FY2019" — *= A29* | n/a | TRUE | n/a | ① |
| B30 | "All are internally consistent… but none can be traced without the filing" | n/a | TRUE | n/a | ① |
| B31 | "the peers are anonymised and no financials are given" | ~5% of headline weight | TRUE | TRUE | ③ |
| B32 | "Neither the composite nor the return series is supplied… Usable and not fabricated" — *= A31* | nil | TRUE | TRUE | ① |
| B33 | "no distribution is described that reconciles the two" — *= A28* | nil | TRUE | UNPROVEN | ③ |
| B34 | "FY2022 close 28.08 and EPS 5.9195… Hardcoded constants with no trace anywhere in the workbook" | four-year mean multiple, ~5% of weight | PART | PART | ③ |

### Source C — Gemini Deep Thinking (8 findings)

| # | their words (verbatim, trimmed) | price | premise | conclusion | bucket |
|---|---|---|---|---|---|
| C1 | "10Y Sovereign Yield · 22.31% · 22.31%–23.00% · Central Bank of Egypt · **+3.00%**" — *= A11* | see A11 | TRUE | TRUE | ① |
| C2 | "**The Double-Counted Bad Debt Trap**… it fails to add this non-cash charge back to the FCFF waterfall… the model double-counts the bad debt expense" | their fix: **82.21** (+15.64, **+23.50%**), Frame A 108.18 | FALSE | FALSE | ④ |
| C3 | "**The Consolidation Perimeter Chimera**… You cannot mix a pre-deconsolidation debt load with a post-deconsolidation NCI deduction. This illegally injects EGP 513.2m of phantom equity" | Dec-25 perimeter: **65.05** (−1.52, −2.28%), Frame A 64.18 | TRUE | PART | ① + ⑤ |
| C4 | "**Interest Hallucination**… the math silently ignores the model's own printed FY27 finance cost of EGP 1,451m… inflates EPS from a reality-based EGP 7.40 up to EGP 8.38" | recomputing with the real FY2027 charge: **66.58** (+0.01, +0.02%) | FALSE | FALSE | ④ |
| C5 | "Normalised Earnings Power · 65.27 · 66.06 · **+1.21%**" | +0.01% on a like-for-like rebuild | FALSE | FALSE | ④ |
| C6 | "**The 'Sandbag'**… steadfastly refuses to model a single dollar of associated revenue. This is an ultra-conservative stress-test, not a neutral base-case" | the crux prices it: USD 115m of FY2030 revenue closes the whole gap | TRUE | PART | ⑤ |
| C7 | "**Cost of Equity Duration**… This ignores the fact that near-term cash flows must clear the current, crisis-level Ke of 24.82%" | their fix (Ke 19.8%): **62.39** (−4.18, **−6.27%**) | FALSE | FALSE | ④ |
| C8 | "a **Corrected Central Fair Value of EGP 75.37 per share** (Frame A: 105.21 · Frame B: 97.97 · Book 42.18 · Normalised 57.56 · Relative 50.09)" | +8.80 (+13.2%) — built on C2, C4 and C7 | FALSE | FALSE | ④ |

### Source D — Gemini Deep Research (10 findings)

| # | their words (verbatim, trimmed) | price | premise | conclusion | bucket |
|---|---|---|---|---|---|
| D1 | "CBE treasury bond auction data from May 2026 indicates a weighted average yield of **23.407%**. The report therefore underestimates the raw risk-free rate by approximately 110 basis points" | at 23.407%: **65.79** (−0.78, −1.17%) | PART | PART | ① via A11 / ③ |
| D2 | "MUP trades at a market capitalization of EGP 1.08 billion with a trailing P/E of **9.33×**… the model's application of an 11× multiple is mildly aggressive" | at 9.33×: **65.33** (−1.24, −1.86%); with the stream at 246.1 too: **65.15** (−1.42, −2.13%) | PART | PART | ③ |
| D3 | "**The Stale Anchor**… the report inflates the Equity Value by approximately EGP 1,701 million, which equates to an artificial premium of **EGP 10.08 per share**… flatters the fair value by over 15%" | their arithmetic: **61.53** (−5.04, −7.57%). Their own prescribed fix (roll the period forward a quarter): **63.24** (−3.33, −5.00%) | PART | FALSE | ② + ⑤ |
| D4 | "**Lens Independence Violation**… Including a model-derived intrinsic multiple inside a purely relative valuation bucket is a severe architectural break" | drop that leg: **66.71** (+0.14, +0.21%); drop both intrinsic legs: **65.23** (−1.33, −2.00%) | TRUE | PART | ⑤ |
| D5 | "**The Put Option Fallacy**… The EGP 67 valuation represents the equity value of the company if the EIPICO 3 facility is a complete and total commercial failure" — *= C6* | see C6 | TRUE | PART | ⑤ |
| D6 | "The auditor explicitly qualified the Q1 2026 review because the company booked **zero expected credit losses** in the quarter, despite an EGP 798 million expansion in trade receivables" | n/a — recorded by them as a pass on the dual frame | TRUE | TRUE | ④ as a finding (already disclosed) |
| D7 | "the Terminal Value represents a staggering **75.94%**… The model **lacks a dedicated sensitivity boundary for terminal collapse**" | nil | PART | FALSE | ② |
| D8 | "masking pre-revenue assets carried at cost beneath an earnings-multiple valuation bucket represents poor institutional hygiene" — *= B25* | nil | TRUE | TRUE | ① |
| D9 | "Normalised Earnings Power · 65.27 · 66.20 · **+1.42%**… stems from minor differences in forecasting the FY2027 net interest deduction and the precise application of the statutory solidarity tax" — *= C5* | +0.02% on a like-for-like rebuild | FALSE | FALSE | ④ |
| D10 | "The Recalculated Central Fair Value (the Base Case, assuming Zero Plant Revenue) falls drastically to **EGP 57.19 per share**" | −9.38 (−14.1%) — built on D3's arithmetic and D4 | FALSE | FALSE | ④ |

---

## Step 5 — Receipts for every rejection

No rejection below rests on "standard practice", "the critic misunderstands", "a matter of judgement",
"immaterial" without a number, or "already disclosed" without a location.

### B15 — "1,275 and 1,332.9 are one line item carrying two values, unreconciled" — REJECTED

Both figures are in the study, both are sourced to the same note, and they are different things.
Input register, `fin_fy25`, four-field source, verbatim:

> "…finance costs note (30): **interest on credit facilities 1,275.312 plus bank commissions and charges 57.634**"

1,275.312 + 57.634 = 1,332.946. The §1.8 sentence says *"expensed EGP 1,275 million of **interest**"* and
the income statement line is *"finance costs"*. The critic's own arithmetic confirms it: they write
"the derived 14.2% / 20.3% / average gross debt 8,999 arithmetic is itself correct on 1,275" — the
interest-rate calculation must use interest, not interest plus commissions.
**Conceded on one point:** the document never states the 57.6 bridge in prose. That is a one-line
disclosure fix, filed under ①, not a reconciliation failure. Priced: **nil**.

### C2 — "The Double-Counted Bad Debt Trap" — REJECTED, on two independent grounds

**Ground 1 — the cash-flow identity.** Let G be gross receivables, A the loss allowance, N = G − A the
net balance the model forecasts. Roll-forwards: G₁ = G₀ + Rev − Cash − Writeoffs, and
A₁ = A₀ + Provision − Writeoffs. Subtracting, Cash = Rev − ΔN − Provision. The model charges the
provision once through EBIT and absorbs ΔN once through working capital — which is exactly
Rev − ΔN − Provision. Adding the provision back would recognise as collected the cash the provision
says will never arrive.

**Ground 2 — the premise is factually wrong about the model.** The critic states the working-capital
schedule "projects Accounts Receivable directly off gross revenue days." It does not project a gross
balance. Input register, `ar_fy25`, verbatim:

> "…note (10) trade and notes receivable **net of the expected credit-loss allowance**"

and the Q1-2026 statement of financial position reads *"Accounts and notes receivable (net)"*. The DSO
path (126 → 112) is calibrated on that net balance: 3,325.044 / 9,441.379 × 365 = **128.6 days**.
There is no gross-receivable row anywhere in the model to double-count against.

**Ground 3 — the line is not what the critic thinks it is.** The 5.25% charge is applied to the
*Formed provisions* line, whose audited composition is in the input register, `prov_fy25`:

> "expected credit losses **376.158**, inventory impairment **13.061**, other provisions **105.0**
> (note 31: disputed taxes 18.5, claims 1.5, end-of-service 85.0)"

End-of-service benefits, disputed taxes and legal claims are cash-settled. Inventory impairment flows
through inventory, not receivables. Adding the whole line back as "non-cash" would treat future cash
payments as free cash flow. **Price of their fix: +15.64/share, +23.50%** — a quarter of the valuation
created by an add-back that the identity forbids.

### C4 and C5 / D9 — "Interest Hallucination in the Normalised Lens" — REJECTED

The normalised lens already charges interest. `compute.py`:

```python
norm_pat = ((norm_ebit - BOARD_FEE - V['int_path'][1]) * (1 - V['tax_eff_fwd'])
            + V['assoc_norm'] - NCI_FWD)
```

`int_path[1]` = **1,210**, the model's FY2027 finance cost. Rebuilding the lens from the outside with
that charge reproduces **EGP 8.39** a share against the published 8.3767 — a **+0.02%** difference, not
+1.21% and not +1.42%.

The critic's 1,451 is not "the model's own printed FY27 finance cost". It is the **stale Appendix A.1
row** that A2, B2 and my own SA-7 all identify as a retired first-edition artefact. So C4's premise is
built on a genuine defect that the other two critics found — and reading that defect as the model's
truth converts a presentation error into a fabricated valuation error. C5 and D9 are the same mistake
surfacing as an unexplained "variance" in their reconciliation tables.

### C7 — "Cost of Equity Duration" (book lens should use the current 24.82%) — REJECTED

The book lens is a Gordon multiple, (ROE − g)/(Ke − g), applied in perpetuity. A perpetuity multiple
takes a perpetuity rate; discounting an infinite-lived stream at a crisis rate that the model itself
forecasts to decay to 14.90% within five years asserts the crisis is permanent. The study says so on
its face, in the normalised-lens paragraph:

> "Using today's crisis-level cost of equity of 24.82% in a perpetuity would be a category error — a
> steady-state multiple takes a steady-state rate."

The near-term rate is where it belongs: the DCF discounts FY2026 at 22.19% and glides to 13.83%. The
critic's own memo praises that same glide as "top-tier institutional precision" two paragraphs earlier
— the two positions cannot both hold. **Price of their fix: −4.18/share, −6.27%.** Escalated and
re-derived in step 6 anyway, because it crosses the threshold.

### C8 and D10 — the two "corrected fair values" (EGP 75.37 and EGP 57.19) — REJECTED

C8 = C2 (+23.50%) + C3 + C7 (−6.27%). Two of the three components are rejected above; the third is
accepted in part. D10 = D3's arithmetic (rejected below) + D4 (your call). Neither number survives its
own components. They also disagree with each other by **EGP 18.18 a share, 27% of the centre**, on the
same workbook and the same anchor date — which is itself evidence that neither aggregate is a
re-derivation.

### D3 — "EGP 10.08 per share" of stale-anchor inflation — the CONCLUSION rejected, the premise accepted in part

**What is true:** the bridge deducts 31-Dec-2025 net debt of 7,364.3 while the 31-Mar-2026 reviewed
interim shows 9,065.2. That is a real inconsistency of dating.

**What is false — the arithmetic.** Deducting the March balance while retaining a full-year FY2026 FCFF
charges the same quarter twice: the Q1 working-capital build and capex are *inside* the FY2026 free
cash flow the model already discounts. The critic concedes the correct method in the next sentence —
*"Institutional best practice dictates rolling the DCF forward by one quarter (utilizing a 0.75-year
discount factor for the first explicit period) and bridging with the latest available net debt"* — and
then does not do it. Done properly: **63.24 (−3.33, −5.00%)**, not −10.08/share.

**What is false — the stated mechanism.** The critic attributes the cash burn to "the cash outflow for
the FY2025 dividend payout." The Q1-2026 statement of financial position, read directly:

| | 31/3/2026 | 31/12/2025 |
|---|---|---|
| Dividends Payable | **720,803,546** | 434,651 |

The dividend was **declared, not paid** — it moved into a payable, it did not leave the bank. The Q1
cash absorption is working capital (inventory 3,887 → 4,047, receivables 3,325 → 4,123) and capex, not
dividends. And the dividend outflow is still ahead of the company, which if anything strengthens the
critic's direction while invalidating their reason.

### D6 — the auditor's zero-ECL qualification, offered as a finding — already in the study

Correct on the fact, and I verified it against the review report itself (Forvis Mazars, 14 May 2026):
*"The company's management did not recognize expected credit losses on financial assets for the
financial period ending March 31, 2026."* It is already in the study's input register, `q1_prov`:

> "…**THERE IS NO EXPECTED-CREDIT-LOSS CHARGE AT ALL, which is one of the three matters the auditor
> qualified**"

Recorded as answered, not as a defect.

### D7 — "the model lacks a dedicated sensitivity boundary for terminal collapse" — CONCLUSION rejected

Table 10 / `Sensitivity!B26:F30` is a 25-cell terminal grid across terminal cost of equity (±200bp) and
terminal growth (3–7%), running **47.83 to 110.21** a share. B18 independently revalued all 25 cells and
reproduced them exactly. What is true is the narrower point B18 makes: the *prose* misquotes that grid
as "EGP 68 to 112", deleting its own lower half. Filed ① under B18. The 76%-of-core-EV concentration is
disclosed on the face of the bridge, which the same critic records as a verified clearance.

### A5 / B9 — "0.21896499 is not derived from any cell; almost certainly a first-edition residue" — DEFECT ACCEPTED, DIAGNOSIS REJECTED

The workbook hardcode is real and is fixed. But the constant is not a residue. `compute.py`:

```python
roe_sust = float(np.mean(roe_fwd[-3:]))
```

The model's forecast ROE path is 15.49 / 17.42 / 20.34 / 22.27 / 23.08%; the mean of the last three is
**21.8965%** — the literal, to eight digits. So the number is derived; what failed is that the builder
wrote the *value* into the sheet instead of the *link*, and the prose called it a level the forecast
"settles at" when it is a three-year average of a rising path. Both of those are ①. The critic's
inference that no cell produces it is wrong, and it matters: their prescribed replacement (the FY2030
ROE, 23.08%) moves the centre **up** 1.07 (+1.61%), not down.

---

## Step 6 — Escalation: everything above 5% of the centre, re-derived from primary sources

Eight findings cross ±5%. Each was re-derived from the filing or the original dataset, not from the
critique and not from the model.

**E1 · C2, provision add-back (+23.50%) — rejected.** Re-derived from the audited provisions note
(composition above) and the Q1-2026 income statement, *Formed provisions 65,000,000*, of which the
auditor states **none** is ECL. There is no non-cash receivables charge of the size the fix assumes, and
the cash-flow identity forbids the add-back regardless. No change.

**E2 · A22, associates at the Q1 run-rate (−15.52%).** Re-derived from the Q1-2026 statement of profit
or loss: *"Profits of subsidiaries and associates · 13,118,430 · (31/3/2025) 33,445,212"* — a 60.8%
year-on-year fall, annualising to 52.5 against 250 carried. **But** the same review report states the
auditor *"[has] not received the audited periodic financial statements for the Arab Company for
Pharmaceutical Raw Materials (Arab API) and Medical Professions Company"*, so the quarter's associate
line is incomplete by construction. It is evidence, not a run-rate. The three disclosed full years are
74.5 / 151.6 / 512.1; their mean is 246.1, which prices at **−0.20 (−0.31%)**. Recommendation: hold 250,
fix the basis note, and disclose the quarter beside it. The level itself is ⑤.

**E3 · A19, terminal risk-free rate (+5.53% to +18.41%).** The 5% inflation leg is sourced (CBE
medium-term target; IMF WEO 2030 ≈ 5.3%). The 5.5-point real leg is **not sourced** — the input's own
basis field says "the standard 5.5-point emerging-market real-rate convention", which is an assertion.
Against IMF long-run real GDP growth of 4.4–4.6%, a perpetual real risk-free rate above real growth is
not sustainable in a Gordon framework. This is the single widest lever in the study and it is
currently unanchored. ③ — it needs a sourced long-run real yield before the next edition, and until
then both ends should be published.

**E4 · A15/B26, the interest path (−10.55%).** Re-derived from the Q1-2026 income statement:
*"Financing expenses · (312,861,801) · (335,979,171)"* — down 6.9% year on year, annualising to 1,251
against the model's FY2026 charge of 1,250. **FY2026 is confirmed against the filing.** FY2027–30 fall a
further 220 on a debt balance the model freezes at 8,797.7, which is the defect: either the debt
amortises (and the balance sheet must show it) or the rate holds. Charging the blended marginal rate
flat costs 7.02 (−10.55%). Note this touches only the EPS-based lenses (30% of weight); the DCF is
EBIT-based and does not move. ③ → ⑤: the fix requires a financing schedule, which is a build change.
B26 is separately and simply true — `kd_path[0]` = 0.1890 is `rf_star` exactly, so the row's basis note
is mislabelled. ①.

**E5 · B3b, terminal debt weight at the book reading (+9.30%).** Re-derived: the model's frozen net debt
is 7,364.3 and FY2030 forecast equity is 11,288.8, giving **39.48%** — the critic's 39.5% confirmed to
two decimals. On market-value equity it is 25.1%. The input's basis note claims it is "reconciled to
the model's own forecast balance sheet"; neither reading is 20%, and the sheet it names is the one that
does not balance (A9). ① — either re-derive it from a balance sheet that balances, or relabel it an
assumption and publish the range 68.04–72.76.

**E6 · D3, the March bridge (−7.57% as they compute it, −5.00% done correctly).** Re-derived from the
Q1-2026 statement of financial position: long-term loans 4,021,835,282 + lease LT 11,867,322 + short-term
loans 965,585,755 + credit bank facilities 4,428,322,532 + lease ST 402,127 = **9,428,013,018**, less cash
362,815,296 = **9,065,197,722**. The critic's 9,065 is exact. Their −10.08/share is not, for the
double-count reason above. ② on the magnitude, ⑤ on which anchor to publish.

**E7 · C3/D8, the consolidation perimeter.** This is the finding I most needed the filing for, and the
filing settles it. The Forvis Mazars review report, verbatim:

> "The company's management recognized the investment in the Arab Company for Pharmaceutical Raw
> Materials **at cost** as of March 31, 2026, **in violation of Egyptian Accounting Standard No. (42)**…
> regarding… **the exclusion of the subsidiary's assets and liabilities**, the recognition of the
> investment at its **remeasured value**, the recognition of gains or losses related to the loss of
> control… and the use of the **equity method**."

So Arab API **was consolidated at 31-Dec-2025** — its assets and liabilities, including any debt, sit
inside the 7,364.3 net-debt figure, and the 288.7 NCI is the minority in it. At 31-Mar-2026 it is out.
The study's bridge deducts **Dec-2025 net debt** while deducting **Mar-2026 NCI (4.0)** and separately
adding the retained stake at 228.5. The critic's premise is correct: those are two different perimeters.
Two coherent bridges exist, and the current one is neither:

| bridge | net debt | NCI | associate line | Frame A | centre | Δ |
|---|---|---|---|---|---|---|
| as published | 7,364.3 (Dec) | 4.0 (Mar) | 2,750 + 228.5 | 67.22 | **66.57** | — |
| Dec-2025 perimeter | 7,364.3 | 288.7 | 2,750 only | 64.18 | **65.05** | −1.52 (−2.28%) |
| Mar-2026 perimeter, period rolled a quarter | 9,065.2 | 4.0 | 2,750 + 228.5 | 60.35 | **63.24** | −3.33 (−5.00%) |

Their "EGP 513.2m of phantom equity" is 288.7 + 228.5 = 3.04/share on the DCF lenses, which matches the
Dec-2025 row exactly. The premise is accepted and the arithmetic is right; whether it is "illegal" is
overstated — carrying a deconsolidated stake at cost is what the *company* did, and the auditor
qualified the company for it, not the model. ① on fixing the perimeter, ⑤ on which of the two to publish.

**E8 · C7, the book lens on a current cost of equity (−6.27%).** Rejected on the grounds in step 5. Priced
at all three plausible readings of "average Ke": the 5-year discount-glide mean 17.79% → 63.72 (−4.28%);
the current/terminal midpoint 19.86% → 62.36 (−6.33%); the critic's 19.8% → 62.39 (−6.27%). No change.

---

## Step 7 — The buckets

### ① Accept and implement — 57 findings

*Presentation and published-statement defects (no valuation effect, all mechanically confirmed nil):*
A1/B5 (appendix profit row), A2 (appendix finance-cost row), A8/B13 (Table 3 total), A9/B14 (balance
sheet plug and a liabilities-and-equity total with a balance check), A10/B12 (EV 29,600),
A12/B11 (Damodaran column label), A16/B6 (the "EGP 700 million" claim), A20 (Figure 8 centres),
A21/B19 ("EGP 70 to 100"), A23/B16 (79% → 68.4%), A24 (print the tornado input ranges),
A25/B28 (renumber; "four methods" over five lenses), A26/B27 (publish the crux ramp and charge the
incremental revenue the same reinvestment identity — the published USD 115m hurdle is 16% too low),
A27 (add attributable profit and EPS to the Q1 check), A29/B29/B30 (attach the four audited filings and
the reviewed interim — they are committed in this repository), A30 (publish the cleaned OHLC series),
A31/B32 (publish the beta index constituents and return series), A32 (publish the 19 window outcomes and
their PITs), B15-partial (state the 1,275 + 57.6 = 1,332.9 bridge in prose), B17 (Table 11 caption),
B18 (quote the grid as 48–110), B20 (publish all three calibration sets), B21 (publish both volatilities),
B24 (restore "core", or publish both TV shares), B25/D8 (split the cost-carried entity onto its own line),
B26 (relabel the cost-of-debt path row — 18.90% is `rf_star`), D6 (already disclosed; no action).

*Corrections that move the number:*

| finding | fix | Δ centre |
|---|---|---|
| A3/B1 | publish two centres, drop the single averaged headline | 63.33 / 69.81 (∓4.87%) |
| A4/B8 + A5/B9 | make the book lens live: `((ROE−g)/(Ke_term−g)) × BVPS`, both terms linked | 0.00 today, removes ±10.15 of false stability |
| A6 | relabel the provision basis truthfully (the level is ⑤) | 0.00 for the relabel alone |
| A7/B22 | call 19.5× a struck reference, or move to the 21.35× midpoint | +0.29 (+0.43%) |
| A11/B10/C1 + B7 | restrike rf on the pricing date (23.00%) and move to the July-2026 Damodaran vintage | −0.53 (−0.80%) |
| A13/B23 | one share basis per period; publish both trailing P/Es | ≈ −0.08 |
| A14 | period-match the trailing legs | +1.95 (+2.92%) |
| A17 | tax FCFF at the effective 23.5% | −0.58 (−0.88%) |
| A18/B2 | terminal ROIC at the model's own 16.36% | −2.78 (−4.18%) |
| B3 | terminal debt weight derived, or relabelled an assumption | +1.47 to +6.19 |
| B4 | terminal NOPAT charged D&A on the 2,947 parked balance | −1.57 (−2.36%) |
| C3/E7 | one perimeter in the bridge | −1.52 or −3.33 |

### ② Accept the defect, reject the fix — 4 findings (A5, B9, D3, D7)

- **A5/B9** — hardcode and prose accepted; "not derived from any cell" rejected (receipt above). Their
  replacement moves the centre *up* 1.07.
- **D3** — the dating inconsistency accepted; the −10.08/share magnitude rejected as a double count.
  The correct version of their own prescription is −3.33 (−5.00%).
- **D7** — the 76% concentration accepted and already disclosed; "lacks a sensitivity boundary" rejected
  (Table 10 is a 25-cell terminal grid, 47.83–110.21, which B18 revalued cell by cell).

### ③ Unproven — research before the next edition — 7 findings (A19, A28, B31, B33, B34, D1, D2)

| finding | what has to be established | why it cannot be closed today |
|---|---|---|
| *(sub-item of A8, counted under ①)* | the consolidation factor on both years (1.0149 FY2025 vs 1.0308 FY2024) | needs the FY2023 separate-company revenue note to get a third observation |
| A15/E4 | a financing schedule — does the debt amortise, or does the rate hold? | FY2026 is confirmed against Q1; FY2027–30 is a build change, −7.02 if the rate holds |
| A19/E3 | a sourced long-run Egyptian real yield | the 5.5-point real convention is an assertion; the lever is worth +3.68 to +12.25 |
| A28/B33/B21 | the path model behind the published bands (implied 49.8%/43.1% vs stated 62.90%/53.55%) | the simulator's mean-reversion structure is not disclosed in the study |
| B31 | name the peers and rebuild the multiple from their filings | the 19.5× is currently unbuildable from anything published |
| B34 | the FY2022 close (28.08), share count (99.1705m) and EPS (5.9195) | FY2022 statements are not in the committed source set |
| D1/D2 | the 6-Aug-2026 10-year print from a primary curve, and a real associate comparable set | the CBE auction page was unreachable this session; the May-2026 auction average (23.407%) is a different instrument and date |

### ④ Reject with receipts — 9 findings

B15 · C2 · C4 · C5 · C7 · C8 · D6 · D9 · D10. All receipted in step 5. Combined effect of the rejected
fixes, had they been applied: **+8.80/share from C8's stack and −9.38/share from D10's** — two audits of
the same workbook, 27% of the centre apart.

### ⑤ Your decision — 7 findings across 6 choices, each with the price of both branches

| # | the choice | branch 1 | branch 2 | my recommendation |
|---|---|---|---|---|
| A6 | the Frame A provision level | keep **5.25%** (66.57) — sits between the two non-outlier years (5.15%) and the ECL-only three-year mean (3.03%) | move to the labelled **6.5161%** (63.66, −4.37%) | **keep 5.25% and fix the label.** Q1-2026 booked *zero* ECL — the auditor qualified for it — so 6.52% is 2.6× a quarter that charged nothing. The critics are right about the word, not the number. |
| A22 | the associate stream | keep **250** (66.57) | Q1 run-rate **52.5** (56.24, −15.52%) or the 3-yr mean **246.1** (66.36) | **keep 250, publish the quarter beside it.** The auditor did not receive Arab API's or Medical Professions' statements, so Q1's 13.1 is incomplete by construction. |
| C3/E7 | which perimeter | **Dec-2025** (65.05, −2.28%) | **Mar-2026 + quarter roll** (63.24, −5.00%) | **Mar-2026 with the roll-forward.** It matches the valuation date, it is the perimeter the market is buying, and it retires D3 at the same time. |
| C6/D5 | zero EIPICO 3 revenue | keep the show-me stance (66.57) | model a ramp | **keep it, and reframe the label.** Both Gemini audits are right that EGP 66.57 is a floor, not a neutral base case, and the study should say so in the Headline rather than only in the crux. |
| D4 | the justified multiple inside the relative lens | keep three legs (66.57) | drop it (66.71, +0.21%) or drop both intrinsic legs (65.23, −2.00%) | **drop the justified leg.** It costs +0.14 and removes a circularity that two independent reviewers flagged. |
| A15/E4 | the forward interest path | keep the glide (66.57) | hold the marginal rate flat (59.55, −10.55%) | **neither yet** — build the financing schedule first; picking a number before the debt schedule exists is guessing. |

### What the accepted corrections do to the answer, stacked

Applying only ① items with a price — terminal ROIC 16.36%, effective tax 23.5%, the 6-Aug yield,
the July Damodaran vintage, the peer midpoint, terminal D&A on the parked balance, the period-matched
relative lens, and the de-averaged headline:

| perimeter | Frame A centre | Frame B centre |
|---|---|---|
| Dec-2025 | **59.32** (−10.9%) | **64.93** (−2.5%) |
| Mar-2026 + quarter roll | **55.80** (−16.2%) | **61.42** (−7.7%) |

Still open on top of that: the provision level (⑤), the associate level (⑤), the terminal real rate
(③, worth up to +12.25), the interest path (③, worth up to −7.02) and the peer set (③).

**Does the conclusion survive?** Yes, and it moves further from the market, not closer. Every stack
above sits below the published 66.57, against a spot of EGP 130.05. The three critics who computed a
"corrected" number all still land far below the price. The study's directional finding — that the market
is paying for a biosimilar revenue ramp the company has not disclosed, roughly USD 115m by FY2030 and
nearer USD 133m once the incremental revenue is charged the same reinvestment identity as the existing
business (A26) — is unaffected by all 84 findings.

---

## Step 9 — Implemented, and proved

Bucket ① was approved and is implemented. Nothing from ②, ③ or ⑤ was touched; the four
open decisions are listed at the end of this section.

### Before and after, on the numbers

| | 2nd edition | 3rd edition |
|---|---|---|
| Headline | one centre, EGP 66.5672 | **two centres, EGP 61.6837 (Frame A) and EGP 69.1536 (Frame B)** |
| Frame A / Frame B | 67.2233 / 79.3291 | **58.8951 / 73.8348** |
| Field | 50.09 – 79.33 | **58.90 – 73.83** |
| Book / relative / normalised | 63.12 / 50.09 / 65.27 | **63.12 / 65.47 / 65.27** |
| Terminal ROIC | asserted 20% | **computed 16.15% / 18.13%** |
| Terminal reinvestment | 25.0% | **31.0%** |
| Terminal depreciation charged | none | **EGP 182.7m a year** |
| Terminal debt weight | 20% | **derived 25.1% (book reading 39.5% published beside it)** |
| Tax on FCFF | 22.5% | **23.5%** |
| Cost of equity | 24.82% | **25.57%** (6-Aug yield, July country-risk vintage) |
| Terminal discount rate | 13.83% | **13.56%** |
| Reverse-valuation hurdle | USD 115m, ramp unpublished | **USD 119m, ramp published, reinvestment charged** |
| Forecast balance sheet | out by up to 6.6% | **balances to zero in every column** |

The centre moved DOWN and away from the market price, which is what the adjudication predicted.

### Every gate, re-run on the delivered files

| Gate | 2nd edition | 3rd edition |
|---|---|---|
| Recalculation | 785 / 785 cells, 10 headline checks | **824 / 824 cells, 0 unresolvable, 0 unchecked, 0 mismatched, 17 headline checks** |
| Driver test | 29 directions, 134 live, 0 dead | **30 directions, 133 live, 0 dead, 3 disclosure rows** |
| External-reader scrub | 0 hits | **0 hits (study, bibliography, workbook)** |
| Table discipline | 41 tables, 0 problems | **45 tables, 0 problems, numbers assigned in document order** |
| Figure discipline | 8 figures, 0 problems | **8 figures, 0 problems, all re-inspected as rendered images** |
| Numeric traceability | 0 typed numerals | **0 typed numerals** |
| Sweep register | PASS | **PASS — 4/4 rings, 27 findings, 4 audited years** |
| Import-not-parse | 14 modules | **13 modules import cleanly; REFERENCE_SET intact** |
| PDFs | study 20pp, biblio 20pp | **study 25pp, biblio 22pp, workbook 55pp — all read** |

### Defects the fixes themselves surfaced

1. **Two driver-test expectations went stale, and the model was right both times.** The
   statutory tax rate no longer taxes free cash flow, so raising it now RAISES value through
   a larger interest shield. And bringing construction into service earlier now HELPS: the
   explicit-year tax shield is worth +22.5 on the sum of present values and the smaller
   never-depreciated balance left for the terminal block is worth +21.5. Both were decomposed
   before either expectation was changed, and the decomposition is recorded beside them.
2. **The historical balance-sheet columns do not balance exactly.** Adding the check row
   exposed residuals of −4.1 / +0.2 / +0.4 million on the three audited columns — under 0.05%
   of total assets, from grouping the filed statement into the sheet's captions. Published
   rather than suppressed; only the forecast columns are zero by construction.
3. **The beta composite contains the subject.** Publishing the constituent list, which A31 and
   B32 asked for, made this visible. At 36 equal-weighted names the company
   carries about 2.8% of the index it is regressed against.
   Removing it gives 0.5652 against 0.6295, which would RAISE the
   two centres to EGP 65.04 and EGP
   72.86. The in-index coefficient is kept — it is the more
   conservative and it is what a real local index produces — and both are now published with
   the price of the choice. No critic raised this; it is a defect the fix uncovered.

### What was NOT touched, and is waiting on you

- **⑤ A6** — the Frame A provision LEVEL stays at 5.25%. Only the label changed. Every reading
  is now priced side by side in the study (Table 12).
- **⑤ A22** — the associate stream stays at 250. Only the basis note was reconciled to the
  income statement, and the quarter is published beside it.
- **⑤ C3** — the bridge still mixes December net debt with March non-controlling interests.
  It is now named as a caveat with its price; choosing a perimeter is your call.
- **⑤ A15 / ③** — the interest path is unchanged. The funded balance sheet makes the tension
  worse and visible: the implied average borrowing rate now falls to
  11.25% against a marginal 18.55%,
  and that is stated in the study rather than left in the model.
- **⑤ C6 / D5** and **⑤ D4**, and all seven ③ research items, are untouched.

---

## Step 8 — Stopped here

Nothing above is implemented. No document, workbook, figure or input has been changed in response to
these critiques; the only code added is the audit hook and the two pricing harnesses, which change no
delivered number (baseline reproduces at 66.5672 exactly).

On approval I will implement bucket ①, take your calls on ⑤, open the ③ items as research, then re-run
every gate — `recalc.py` (785/785 formula cells), `driver_test.py` (29 asserted directions, dead-input
sweep), `qc_checks.py` (scrub, table, figure, traceability), the sweep register, SIGCM and the
model-study checklist — and report before/after for each, plus any further defect the fixes surface.


---

## Step 10 — Recalibrated after being told the critique was taken too lightly

Not a defence. Three things were re-checked at finding level, and all three found something.

### (a) Four findings were "priced" in words, not numbers — which rule 3 forbids

Rule 3 says a finding may not be called immaterial without a number beside the word. Four
were dismissed with a phrase. They are now priced, on the corrected model:

| finding | how it was priced before | priced properly |
|---|---|---|
| **B31** — the peer leg cannot be rebuilt from peer filings | "~5% of headline weight" | delete the leg: relative lens 65.42 → 52.09, centres **59.21 / 66.70** (−2.00 each) |
| **B34** — the FY2022 close and earnings per share are untraceable | "~5% of headline weight" | drop that one observation: four-year mean 6.572× → 7.182×, centres **61.47 / 68.96** (+0.26 each) |
| **D6** — the auditor's zero-credit-loss qualification | "already disclosed" | Frame A's own 5.25% on the quarter's sales would have charged **EGP 133.0 million — 47% of the quarter's reported attributable profit**; the three-year credit-loss mean would have charged EGP 76.6 million, 27% of it. Now in the study. |
| **C6 / D5** — the plant carried at zero revenue | "the crux prices it" | the market pays **EGP 72.01 a share, EGP 12,152 million, 55% of the share price** for it — about 2.1× its stated build cost. Now in the study. |

### (b) The build was not bottom-up enough, and mining the disclosure again found an error

The board report splits the same separate-company revenue TWO ways — by sales channel and by
product line — and the second split had not been used. Reconciling them separates the
company's own preparations from preparations it manufactures under contract for third parties,
and the two only close once that is done.

The earlier build divided a domestic revenue figure that INCLUDED contract-made product by a
pack count that EXCLUDED contract packs. The realised domestic price per pack read EGP
21.5401 when the company actually realised EGP
21.2216 — 1.50% too high, in every forecast year, and the measured
year-on-year price growth read +8.98% when it was **+12.59%**. No critic found this.

The forecast now carries three product lines, each a volume times a price:

| line | FY2025 volume | FY2025 price | FY2025 revenue |
|---|---|---|---|
| Own preparations, domestic | 291.810m packs | EGP 21.2216/pack | EGP 6,192.7m |
| Own preparations, export | 60.000m packs | USD 0.9996/pack | EGP 2,967.5m |
| Contract manufacturing — fee | 5.485m packs | EGP 9.00/pack | EGP 49.4m |
| Contract manufacturing — product resold through own channels | the same packs | EGP 16.95/pack | EGP 93.0m |
| | | **total** | **EGP 9,302.469m** |

Two assertions now guard it: the product-line split must sum to the disclosed total in both
years, and it must reconcile to the channel split in both years. Also swept in and published:
the board report's **eleven-year** history of total revenue, domestic sales, export sales,
contract-manufacturing revenue and production value at selling price (FY2015–FY2025), which
had not been read before.

Centres move to **61.2060** and **68.7011**.

### (c) The workbook still had derived constants pasted where formulas belonged

| | before | after |
|---|---|---|
| Formula cells | 824 | **869** |
| Pasted numeric cells | 471 | **457** |
| Pasted "unit build" cells | 14 | **5** |
| Typed constants in the model that were not four-field inputs | 14 | **0** |

Every constant that was typed into `compute.py` rather than sourced is now an input with a
value, a source, a date and a research layer: the disclosed separate-company revenue total,
the depreciation inside cost of sales, the depreciation-versus-amortisation split, the three
historical share counts, the three expected-credit-loss components, the board fee, the
minority share, the plant's stated cost, the Saudi associate's contribution in two years, the
two peer observations, and all four lens weights. The input register goes from 249 to
276 entries.

In the workbook these became live cells: the four-year mean multiple (was pasted, now
`=AVERAGE` over the history table), the historical earnings per share (now profit over that
year's own share count), the struck peer reference (now `=AVERAGE` of its two observations),
the realised price per pack in BOTH history years (now revenue over packs, on the sheet), the
FY2025 return on equity, the grouped balance-sheet lines, and the whole three-line unit build.
The forecast openers no longer read duplicate Assumptions rows — they read the computed FY2025
column, so each figure exists in exactly one place.

One input is genuinely inert and the driver test named it: the contract-manufacturing FEE.
Raising it raises the fee per pack by exactly what it lowers the resale price per pack, so the
product value reaching revenue is unchanged. It is now labelled a disclosure row with that
reason, rather than left looking like a driver.
