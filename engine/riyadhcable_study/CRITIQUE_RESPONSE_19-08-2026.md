# RIYADHCABLE — critique response and second edition (19-Aug-2026)

Four external critiques of the 18-Aug-2026 first edition were worked under
`engine/Critique_Response_Prompt.md` v2: a self-audit first (recorded before reading three of the
four documents; the fourth was auto-loaded on attachment and that anchoring is disclosed), then a
one-row-per-finding ledger, every finding priced through the study's own `compute.py` before any
verdict, premise split from conclusion, rejections with receipts, and >5%-of-central findings
re-derived from primary sources. **69 findings raised (Claude Cowork 36, Gemini research 5, Gemini
think 1, Claude Code 27), 69 answered, 0 unaddressed.** The full row-by-row ledger was delivered in
the session record; this file is the permanent summary and the implementation proof.

## The verdict that survived verification

Three independent full rebuilds plus this response's own harness reproduced the first edition's
entire arithmetic to four decimals — the machinery was sound; the failures were in the input layer,
the exhibits, and the narrative. The second edition corrects them **through the model**, and the
weighted central moves **SAR 118.73 → SAR 108.32** against the settled SAR 104.90 close (+3.3%,
from the first edition's claimed +13%).

## Findings accepted and implemented (master list, priced at the first edition's central 118.73)

| Finding | Price | Receipt | Fix |
|---|---|---|---|
| rf 4.85% below the published SAR curve (Cowork #1 = CC #1; **escalated, re-derived**) | **−9.79/sh (−8.25%)** at 5.52% | FTSE SAGBI factsheet 31-Jul-2026: 7–10y YTM **5.52%** at 8.24y avg life, whole curve 5.22–5.83%; FRED UST10 4.68–4.72% kills the register's own "UST ~4.3%+55bp" cross-check (true value 5.23%); same-day SAVOLA construction 5.53%; iBoxx 5.44% @6.07y | rf = 5.52% dated; enters explicit AND terminal; ±50bp grid now published |
| In-window dividend 1.90 → **2.25** (Cowork #5 = CC #3) | −0.35/sh (−0.29%) | FY2025 Note 47 (SR 336.8mn @ 2.25, rec. 15-Mar-26); Argaam: ex 10-May, paid 18-May-26. Note 22's "1.9" label contradicts its own 299.4mn (=2.00/sh) | div_window 2.25; **cone q 3.63%→4.05%** (own extension — same root defect in a second site) |
| Peer multiples stale (Cowork #2/#29 = CC #2/#7; escalated) | +2.9–3.7/sh if band-mid | Prysmian PR 30-Jul-26: FY26 guidance raised to €2.8–2.9bn vs ~€40bn EV → **~14x**, not 8.5x; Nexans ~8.7x; KEI ~31x NTM | Peer table rebuilt from own guidance with dates and year bases; justified multiple 9.0x → **10.0x as a stated discount** to the corrected 8.5–14.5x band (+2.9% central) |
| Metal exhibit contradicts the live workbook in SIGN (CC #11) + margin-as-input (CC #17) | nil at base; sign-critical | Measured on the delivered file: workbook metal +2%/yr → DCF **+12.52**; pasted exhibit ×1.15 → **−12.52**. `driver_test.py` had *excluded* metal, citing the pasted grid | **Segments rebuilt as the live spread-per-tonne engine** (spread calibrated at base metal, held under shocks; margin an OUTPUT cell); metal multiplier is a driver, direction-tested on the sheet (margin −10.75% at ×1.15); grid regenerated from the same convention |
| Beta grid base row ≠ base case (Cowork #3 = CC #12) | nil headline; exhibit unusable | Reproduced from `dcf_beta()`: β silently drove terminal Ke (130.90 vs 145.80) | Stated convention (terminal β = 1.0) enforced; **base-row asserts added to every grid** |
| WACC×g grid corner non-Gordon (Cowork #4 = CC #13) | nil headline | Exact mechanism found: undisclosed `max(wt−g, 2%)` clamp | Clamped cells now print **n/m** with the rule stated; figure masks them |
| Terminal 5% debt weight vs the model's own net-cash path (CC #19) | −2.55/sh (−2.15%) | Model forecasts net cash from FY2028E (−744 by FY30) | **All-equity terminal** adopted |
| Capex "under 2%" false for FY2024; taper below both actuals (Cowork #9) | ~−0.3% | Audited CF lines: FY24 195.0 (2.17%), FY25 188.9 (1.77%) | Path floored at the FY2025 actual 1.77%; C.4 sentence corrected |
| ERP vintage (CC #4) | **+0.04%** (their +0.7% was >10× overstated — repriced through the model) | July-2026 Damodaran vintage exists | 0.48%/0.74%/4.94%/4.20% adopted; CDS leg flagged as Jan-vintage |
| FY23 D&A copied from FY24 (Cowork #7 = CC #5) | nil (display) | FY23 notes: 59.53+5.57+1.33 = **66.43** | `source_financials.json` + input added; FY23 EBITDA 716→714 |
| Headers offset one column on five sheets (Cowork #14 = CC #16) | nil; severe auditability | On-file | Realigned + **build-time header-alignment assert** |
| Hardcoded/×0-disguised ratios (Cowork #15 ⊂ CC #24) | nil; contract breach | PS!B8 `Segments!B10*0+1352.03…` + 4 pasted derivables | Every ratio wired as formulas (incl. TTM P/E row); ×0 dummy gone; NCI share and reference profits are sourced Assumptions cells |
| 1.90-seeded remainder, lens-text roll omissions (CC #14), TTM labels (CC #9), FY23 payables basis (CC #10), Kd estimate label (CC #8), Qatar/Artikul narrative omission (Cowork #26), H2-split (Cowork #22), Q2-exit margin display (Cowork #23, priced −1.84% central through the engine — their −5.2%-of-DCF interpolation overstated), half-vs-half comparative (Cowork #24), ROC>30% basis (Cowork #8 = CC #18), rating-language (Cowork #21), calibration wording + n (Cowork #12 = CC #15), MA-claim (Cowork #13 = CC #21 — computed §2 now), book-lens triple + bear-Ke disclosure (Cowork #10/#11), expert framing and constructions (Cowork #16/#17 ⊂ CC #24 — **E3 terminal fixed to reconcile to the DCF EV to the riyal, asserted**), buyback note (Cowork #27 = CC #23), settled close 104.90 (Cowork #36 = CC #6), beta diagnostics + Dimson/OLS disclosure (Cowork #20 = CC #25), discount-convention statement (Cowork #19 — also flagged house-wide for SAVOLA), H1-2026 interim balance sheet logged as an open follow-up (CC #22) | each ≤0.5% or nil | per the session ledger | all implemented in the second edition |

**Kept with fixed language (accept defect, reject fix):** tax 9.5% retained as a disclosed forward
uplift above the audited 9.0% (the +0.45% variant is stated in §1.1); the H1 margin anchor retained
with the quarterly path and the Q2-exit variant (SAR 119) published and the 14.5% falsifier
unchanged; net-debt WACC weights retained with the labelled convention (gross-debt alternative
+0.15%).

## Rejected, with receipts

| Claim | Receipt |
|---|---|
| Gemini research: share count "must be 150.00mn; report mathematically invalid; corrected value 116.01" | 150.00mn issued − 282,500 treasury = **149,717,500**, the audited EPS Note 41 divisor; treasury shares carry no claim; **Gemini's own sibling document verifies 149.7175 at 0.00% variance and clears the study** |
| Gemini research: relative lens "misapplied interim FCFF bridging" | Three exact independent reproductions of the study's construction (Cowork Δ0.00; Gemini think 83.467; this response 83.4667) |
| Gemini research: terminal reliance "not contextualized" | Printed in the bridge, summary table, §4 and §7's caveat |
| Gemini (both docs): rf 4.85% and tax 9.5% "verified, 0.00% variance" | Refuted by the index publisher's dated factsheet and the audited effective rates (7.0/7.3/9.0%) — false clearances, rejected in arbitration |
| Cowork #25: customer 19% "is a nine-month figure" | FY2025 statements: "…19% of the group's total revenue **as at 31 December 2025**. (2024: 18%)" |
| Cowork #12's conclusion: 70% coverage "proof the PIT is not uniform" | n=10: exact binomial p≈0.34; the artifacts' own χ² p=0.911 / KS p=0.803. The premise (the study's "essentially on target" phrasing) was accepted and §3 rewritten with n and the tests |
| Cowork #31–34 (unverifiables: segment split, non-op 20.4, gross debt 621.22, geography 73/27) | All four verified **correct** against the FY2025 statements text the critics could not read |

## What the rebuild's own gates surfaced (step-9 disclosure)

1. **A zakat sign bug in the historical ROIC**: `zakat_fy25` is stored negative, so
   `1 − zakat/PBT` *added* the tax — FY2025 ROIC printed 31.2% instead of 26.0%. This is the likely
   origin of the first edition's "return on capital above 30%". Fixed with a plausibility assert.
2. **The workbook's relative bear/bull literals didn't track the model's band change** — caught as
   6 drifting cells by the expected-value recalc, fixed, and now covered by the same gate.
3. **Note 22's own per-share label is internally inconsistent** (299.4mn at "SR 1.9" implies 157.6mn
   shares) — a filing typo the first edition propagated; recorded in the bibliography's
   discrepancy note with the amounts governing.
4. During this response's own edit pass, a first draft briefly reproduced the ×0-disguise
   anti-pattern for the plain-OLS beta figure; it was caught in-pass and replaced by computing the
   OLS cross-check into `beta_result.json` via `beta_regression(dimson=False)` (0.9285).

## Before → after (all gates re-run on the delivered files)

| | First edition | Second edition |
|---|---|---|
| Weighted central | 118.73 (+13% vs 104.80) | **108.32 (+3.3% vs settled 104.90)** |
| DCF lens / TV share | 145.80 / 83% | 123.28 / 80% |
| Relative / Normalised / Book | 83.47 / 102.14 / 106.66 | 91.07 / 102.16 / 94.69 |
| WACC explicit → terminal | 9.88% → 8.88% | 10.49% → 9.72% (all-equity terminal) |
| Margin framings (bear/anchor/Q2/peak) | 132 / 146 / — / 159 | 112 / 123 / **119** / 135 |
| Experts (E1/E2/E3 → median) | 119 / 150 / 144 → 144 (pasted) | 119 / 131 / 123 → 123 (**live MEDIAN; E3 ≡ DCF asserted**) |
| Workbook | 486 formulas / 211 pasted; 18 drivers, metal excluded | **536 formulas / 216 pasted; 23 drivers incl. the metal sign test, 0 dead, 0 exclusions** |
| RECALC | 486/486, 21 headlines | **536/536, 0 unresolvable, 0 unchecked, 23 headlines** |
| Cone (3M p5/p50/p95) | 76.5 / 105.1 / 144.1 (q 3.63%) | 76.5 / 105.1 / 144.1 (q 4.05%, settled spot) |
| §3 candor | "essentially on target", 1M silent | n=10 + χ²/KS stated; **1-month robust shortfall disclosed** |
| Study | 13pp | 14pp with a dated revision note |

Deliverables rebuilt end-to-end and re-read as rendered pages: study PDF 14pp/14 images (every page
inspected), model PDF 19pp landscape with 536 baked values (key sheets inspected), bibliography 9pp
(118-input register). The first edition's arithmetic reproduction, this response's pricing harness,
and every rerun artifact (`step0`, `backtest_5y`, `beta_result` incl. the OLS cross-check, `strike`)
are committed alongside.

Not published: no site page, ticker page or ledger cohort exists or was touched; publication remains
a separate, explicit request.
