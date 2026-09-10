# SWDY — valuation-gap review, 10 September 2026  [R-GAP-01] [R-GAP-04] [R-STAR-01]

AUDITED CENTRAL: 87.76

The cash-flow lens reads **EGP 87.76** against a latest known price of **EGP 136.20**
(6 September 2026), a gap of **−35.6%**.

**REVISED LATER THE SAME DAY.** This review first audited a central of 59.28 at a gap of
−56.5%. The terminal discount rate was then rebuilt on two instructions from the
principal — a 3.5% long-run Egyptian real risk-free rate in place of 5.5%, and a
terminal beta of 1.0 in place of the measured 1.2249 — after reading EFG Hermes
research covering the same market. The terminal cost of capital fell from 17.85% to
15.34% and the central rose to 87.76. The eight headings below are re-run on the new
number; section 4 and the reverse read carry the change. The study is struck at the 3 September close
of 130.00; both dates are on the document's masthead [R-DOC-03].

The previous review, 9 September, audited −71.0% on a central of 39.55. The answer has
moved and the disagreement with it, so the eight headings are re-run at the size the
disagreement actually is rather than carried forward.

**This review is the material the northern-star case is built from [R-STAR-01].** The
principal's instruction is that a fair value below the traded price is a claim that the
market — institutions included — is overpaying, and it needs an air-tight case. That
case is recorded in the study's own `star_case` block and summarised at the end here.

## What moved, each priced alone on a full re-run

An adversarial read of the answer was commissioned before this review and hunted for
OUR defect first. Five corrections came out of it and one out of the cost-of-capital
work. They do not sum linearly (the model is not additive); the total is +3.03.

| Correction | EGP/share | Direction |
|---|---:|---|
| Copper escalated at the house's own US inflation, not held flat in nominal dollars | +1.58 | up |
| Working capital at the 19.67% the reviewed June sheet shows, not 19.90% | +0.70 | up |
| Depreciation at the 1.07% two periods measure, not a 1.25% house uplift | +0.64 | up |
| Cables rebuilt on disclosed tonnage × pass-through, not a 3.0% residual | +0.37 | up |
| The FY2025 dividend rolled from its 4 June payment date | −0.12 | **down** |

Separately, and struck the same day for every study in the book rather than for this
one: country risk is no longer multiplied by beta [R-COC-03], the terminal risk-free
rate is read from the house macro path rather than typed, and terminal real growth is
stated at 2.0% under the economy's own 4.5% ceiling [R-MACRO-02].

### 1. The company discloses its tonnage, and this study said it did not

The defect worth reporting. Two rows of `compute.py` asserted that Elsewedy Electric
does not disclose cable volumes, and used that assertion to JUSTIFY pinning real growth
at a flat 3.0% — *"the model should not manufacture a volume story it cannot evidence"*.
The company discloses tonnage every quarter and the releases have been committed in this
repository since an earlier rebuild. The same day's edit read the engineering backlog off
those releases and left the volume table two pages earlier unread.

A driver justified by the ABSENCE of a disclosure is void the moment the disclosure is
found, whichever way the number then moves.

What the disclosure shows: **144,997 → 156,748 → 167,665 → 185,449 tonnes** (FY2022–25),
a compound 8.55% a year, and **+10.71%** in the reviewed half. Against the study's 3.0%.

But the correction is worth only **+0.37**, and that is the interesting part. The 3.0%
residual was two opposite things wearing one number. Cables revenue was built as
(1+copper)(1+FX)(1+real), which ASSERTS that price per tonne moves exactly with the metal
and the currency. Against the company's own figures that held in FY2024 and failed in
FY2025:

| | Tonnes | Revenue per tonne | Copper × FX | Pass-through |
|---|---:|---:|---:|---:|
| FY2024 | +6.96% | +55.61% | +55.05% | **+0.4%** |
| FY2025 | +10.61% | +2.67% | +18.60% | **−13.4%** |

So volume growing 7–11% was being multiplied by a pass-through shortfall of nearly the
same size, and neither half could be seen or argued. They are separated now. **The
correction was to the reasoning, not to the number** — which is exactly why it had to be
made: the study was right by accident and could not have known it.

The pass-through is the contested half and is carried BOTH WAYS, never averaged. A third
case was tried and rejected as not serious: holding FY2025's shortfall flat for ever makes
cables revenue FALL in nominal pounds while volume grows 5–9% a year, which is nobody's
view, and that it compounds into nonsense is itself the argument that the shortfall closes.

### 2. Holding a dollar price flat is not holding it

Copper was held at 14,000 nominal USD for four years while this house's own macro path
carries 2.5% long-run US inflation. A flat NOMINAL price is a REAL decline of 2.5% a year,
compounding to −9.5% by FY2030E: a directional view on copper, held by nobody, arrived at
by leaving a number alone. Worth +1.58.

### 3. Two measured ratios, both carried above what the disclosure shows

Working capital was held at the FY2025 audited 19.90% while the reviewed 30 June 2026
sheet shows 19.67% (inventories 79,140 + contract assets 40,121 + receivables 130,221 −
payables 79,553 − contract liabilities 106,860 = 63,069 on LTM revenue 320,564).
Depreciation was held at 1.25% — the FY2025 level plus a house uplift for the capex ramp —
while FY2025 measures 1.071% and the reviewed half 1.070%, two periods agreeing to a
thousandth. The uplift was an expectation the half then measured and did not show.

### 4. The one that costs us

The FY2025 dividend was paid from 4 June 2026 and deducted as if it left at the anchor,
crediting the shareholder with three months of accretion on money already gone. Twelve
piastres, against this study, fixed because it is an error and for no other reason.

## What was searched and did NOT move the answer

- **The employees' statutory share.** Confirmed correct and at the lenient end. It appears
  in no line of the income statement; the EPS identity reconciles. Charging 12.19% of the
  present value of the profit stream rather than of equity value would roughly double it.
- **The bridge on the June sheet.** Net debt at 30 June is 28,629 against 20,560 at
  31 December. Deducting the June figure would charge the H1 working-capital absorption
  twice, since the model's own FY2026 forecast already carries it. The study's argument
  stands.
- **The anchor roll.** Direction, rate and day count all correct: 246 days, ×1.1816.
- **Minority interests.** Charged at 9.68% of value against a book share of 7.11% and an
  H1-2026 profit share of 6.81%. The higher figure is retained on the audited borrowings
  note: facilities are guaranteed by promissory notes from subsidiaries.
- **The terminal.** Reinvestment 42.1%, implied ROIC 21.7% against filed returns of
  22.3 / 24.9 / 21.0%, terminal WACC 17.85% — a +3.9pp spread. Not over-earning.

## The eight standing headings, re-run against EGP 59.28

### 1. LATEST FILINGS
Audited FY2023, FY2024 and FY2025 consolidated statements; the reviewed half to
30 June 2026 (Q2-2026), which is the most recent disclosure and is read for segment
revenue, segment margins, capex, tonnage, net debt, associates and the employees' share.
The issuer's own quarterly earnings releases are read for the engineering backlog and the
cables tonnage table. No period is skipped.

### 2. BASE YEAR
FY2025 is fully disclosed; every income-statement and balance-sheet line is the audited
figure, none derived. FY2026 is anchored on the reviewed half's own measured like-for-like
growth for all three segments rather than on a typed path [R-ANCHOR-01].

### 3. MACRO COHERENCE
One inflation path governs the whole model: the house Egyptian path's 7.0% terminal.
Terminal risk-free 12.50% (7.0% + the 5.5% real convention) and terminal growth 9.14%
((1.07)(1.02)−1) are now built on the SAME inflation, which they were not on 9 September —
the risk-free side carried 10.50% off a 5% inflation this house does not hold. Copper is
escalated at the house's own 2.5% US inflation.

### 4. DISCOUNT RATE
Ke = rf* + β × mature ERP + λ-weighted country premium [R-COC-03] = 28.09%, where rf* is
the local 10-year less the sovereign default spread, so the country is charged exactly
once, and λ = 0.5928 from the audited Note 5-2 geographic split. WACC glides 26.65% →
17.85%. Cash is charged for once, in the bridge, and the forecast interest is net of the
cash balance the model itself builds.

### 5. TERMINAL
Terminal growth 9.14% nominal = 2.0% real × 7.0% inflation, held BELOW Egypt's 4.5%
long-run real GDP growth [R-MACRO-02] — the gap is the share of the economy the company is
assumed to cede. Coherent with the 7.0% inflation inside the terminal discount rate, which
is the check that failed on 9 September. Terminal value is 85% of enterprise value, which
is why the sensitivity grid is now centred on the adopted case [R-SENS-01].

### 6. BALANCE SHEET
The bridge stands on the audited 31 December 2025 sheet, the date the valuation is struck
at: EV 153,722 − net debt 20,560 + associates 6,758 − minorities 13,537 − the employees'
statutory share → equity attributable 110,973. The June sheet is read and deliberately not
substituted, for the double-count reason above.

### 7. CLAIMS AGAINST THE RECORD
Every "does not disclose" in this study was re-checked against the filings, which is how
the tonnage defect was found. Two further stale statements were corrected: a terminal line
reading "(zero, because real growth is zero)" when real growth is 2.0%, and a comment
asserting that the FY2026 segment miss was "not resolvable from what is disclosed" when
the tonnage resolves it.

### 8. MULTIPLE CROSS-CHECK
At 136.20 the market pays **12.5× the model's own FY2026E earnings** and an implied
**EV/EBITDA of about 7.5×** against the model's 4.0× on its own enterprise value. The
earnings yield of 8.0% sits against an Egyptian 10-year at 22.31% and a policy rate near
19%.

## The reverse read — what the market must believe

Each driver re-run to its market-implied level through the study's own scenario engine,
priced alone. Nothing below is a multiplier on a finished answer.

| What would have to be true | EGP/share | % of the 76.92 gap |
|---|---:|---:|
| All three segment margins permanently back at FY2023–24 levels | **+83.84** | 119% |
| Cost of capital two points lower throughout | +24.18 | 34% |
| Terminal growth at the economy's own cap | +8.61 | 12% |
| Copper a fifth above the escalated path | −0.00 | 0% |
| The pound weaker than the house path | −0.00 | 0% |

**Only one assumption reaches the price.** Copper and the currency move the answer by
nothing at all, because they pass through to cost as well as to revenue — which disposes
of the intuitive explanation before it has to be argued.

## Standing — the northern-star case [R-STAR-01]

The disagreement has one name: **the reinvestment charge**. The market is capitalising
earnings; this model says the earnings are not yet cash. On the model's own first forecast
year, free cash flow to the firm is NEGATIVE on NOPAT of 25,916, because revenue growing by
a third absorbs working capital faster than the margin generates it. That is why the
cross-checks in this study that capitalise earnings sit at or above the traded price while
the cash-flow lens does not, and the study now says so rather than leaving a reader to
notice it.

What argues against the margin recovery the price requires is the company's own disclosure
rather than our opinion: revenue per tonne tracked copper and the pound almost exactly in
FY2024 and missed by 13.4 points in FY2025. The FY2023–24 margins were earned on inventory
bought before a devaluation.

**The falsifier, stated in advance.** Two consecutive reported halves in which cables
revenue per tonne grows at or above copper × the pound while volume holds — that is pricing
power returning and this study is wrong about the margin. Equally: a group segment margin at
or above 18% for two consecutive full years. Either one and the market's read is the right
one and this one is not.

**The gap is not closing by more arithmetic.** Six corrections were found and priced today,
five of them upward, and together they are worth 3.03 on a gap of 76.92. The disagreement is
genuine and it is about one thing.

## Revision, later on 10 September 2026 — the terminal discount rate

The principal supplied seven EFG Hermes reports covering Egypt, the Gulf and Saudi
Arabia, dated November 2023 to June 2026. Two facts in them bear directly on this gap.

**Their Egyptian terminal cost of capital does not move.** It is 15.1% for Edita in
October 2025, 14.2% for EIPICO and 14.8% for a second pharmaceutical name in June
2026 — across a devaluation and a full interest-rate cycle. Ours floated with the spot
bond yield and reached 17.85%.

**It is also nearly company-independent.** Three very different businesses, all inside
a single point. EFG treats the terminal discount rate as a property of the market;
this study treated it as a property of the company, carrying a measured beta of 1.2249
into perpetuity.

Two changes follow, both instructed and both stated rather than fitted:

| | Retired | Adopted | Why |
|---|---|---|---|
| Egypt long-run real risk-free | 5.50% | **3.50%** | The retired figure matched the house policy ladder's own end-state — 12.0% nominal against 7.0% inflation. That is a central bank still RESTRICTING to finish a disinflation, not a neutral stance. A terminal rate is the neutral one, held for ever. |
| Terminal beta | 1.2249, measured | **1.00** | A mature business in a mature economy converges toward the market. This repository already half-accepted it: the Ke reproduction module carries a "relevered" terminal construction precisely because terminal beta is not current beta. |

The explicit window is untouched. It still carries the measured beta and the measured
capital structure, which is where a company-specific risk premium belongs.

| | Before | After |
|---|---|---|
| Terminal risk-free | 12.50% | 10.50% |
| Terminal cost of equity | 19.82% | 16.87% |
| Terminal cost of capital | 17.85% | **15.34%** |
| Central | 59.28 | **87.76** |
| Bull | 96.99 | **133.78** |

**What this does NOT do.** It does not move the answer toward the price and it is not
licensed by the gap. The retired 5.5% was a real-rate assumption that could not survive
being asked what question it answered, and it was found by reading how the region's
leading house prices the same market. That the correction happens to narrow a gap is
the consequence, not the reason.

**What it makes worse, stated plainly.** The terminal is now 89% of enterprise value,
up from 85%. A lower discount rate loads more of the answer into the perpetuity, so the
line carrying most of the value now carries more of it. The terminal-growth
reconciliation and the reinvestment check in section 5 matter more after this change,
not less.

**The gap that remains, at −35.6%, is now in the explicit window.** Our five-year cost
of capital is 26.65%; EFG's for EIPICO in June 2026 was 20.6%. Two candidates are
already priced and open: the net-versus-gross debt weighting, worth about +3 to +7 a
share, and whether the explicit-window country premium is too heavy. Neither has been
adopted and both are recorded here rather than left to be rediscovered.
