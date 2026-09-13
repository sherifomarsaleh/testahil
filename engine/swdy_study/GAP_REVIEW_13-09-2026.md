# SWDY — valuation-gap review, 13 September 2026  [R-GAP-01] [R-GAP-04] [R-STAR-01]

AUDITED CENTRAL: 87.7633

The cash-flow lens reads **EGP 87.76** against the price this valuation is measured
against, **EGP 130.00** on 2026-09-03 — a gap of **-32.5%**.

## What this review replaces, and why a new file rather than an edit

The 10-September review audited a central of 87.82 against a price of 136.20 read on
6 September. Both numbers have moved and neither moved for the same reason.

**The price.** That 136.20 was the last row of the price library, three sessions after
this study's own valuation date. The cone, the moving-average stack and the percentile
map were struck on it while the fair value was measured against 130.00, so one document
described two prices. The strike is anchored at the valuation date now and refuses to
run if the library's close on that date is not the spot the study publishes.

**The central.** 87.82 became 87.7633 when the share count was reverted to the issued
2,140,777,876. The 10-September pass had cut it to 2,139,355,716 on the strength of an
extraordinary general assembly of 19 May 2026 said to have cancelled 1,422,160
incentive shares. THAT CORRECTION IS WITHDRAWN AND THIS REVIEW WITHDRAWS ITS OWN LEAD:
note 39's 2,139,355,716 is the IAS 33 weighted-average denominator — issued capital
less shares issued under the incentive scheme and not yet granted, excluded from
earnings per share because they are not outstanding for that purpose. It is not a
capital reduction, the shares exist, the same statements state issued capital at
2,140,777,876 on the face of the balance sheet, and the assembly appears on no filing
in the company's own regulatory-filings index. One convention was read as the other, in
the direction that raised the answer. The reversion is worth -0.0611 a share.

## The gap, priced [R-STAR-01]

Each assumption below is moved ALONE on a full re-run of the model — not a multiplier
applied to a finished line — and priced against the gap of EGP 42.24 a share.

| What the market must believe | Worth per share | Share of the gap |
|---|---:|---:|
| all three segment margins permanently back at FY2023-24 levels | +113.00 | 268% |
| cost of capital two points lower throughout | +52.43 | 124% |
| terminal growth at the economy cap | +30.24 | 72% |
| copper a fifth above the escalated path | +5.82 | 14% |
| the pound weaker than the house path | +2.33 | 6% |

**2 of the 5 clear the gap on their own.** The margin re-run at 268% of it is the
largest by a distance; the cost-of-capital re-run also clears it, which the study now
states rather than claiming a single assumption stands alone.

## What argues against the largest of them

The company's own disclosure rather than our opinion. Cables revenue per tonne tracked
copper times the pound almost exactly in FY2024 and then failed to in FY2025 — a
measured pass-through shortfall computed from audited segment revenue against the
issuer's own disclosed tonnage. The FY2023-24 margins were earned on inventory bought
before a devaluation. A repeat requires that pricing power to return, and the most
recent full year measures it leaving.

## The lenses, at their own values

| Lens | Bear | Base | Bull | Role | vs price |
|---|---:|---:|---:|---|---:|
| Discounted cash flow (the answer) | 28.56 | 87.76 | 137.73 | THE ANSWER | -32% |
| Relative multiples | 65.64 | 78.72 | 98.35 | cross-check | -39% |
| Normalised earnings power | 80.07 | 103.51 | 132.81 | not published for this class | -20% |
| Book value and sustainable return | 36.88 | 66.61 | 76.17 | a floor, never weighted | -49% |
| RETIRED 45/20/20/15 blend, published unused | — | 85.93 | — | retired | -34% |

The central is the cash-flow lens itself and is not an average of the four. An earlier
edition did settle it by weight and reported EGP 85.93.

## The price map, on the same date as the value

Anchor 2026-09-03 at 130.00. Three-month median 137.99, 5th-to-95th 98.49 to 193.01, probability above
spot 63%. The central sits below the 5th percentile of that distribution: the price
map and the valuation genuinely disagree, and stating the gap at its full size is the
point. [R-LENS-01] keeps the two apart — nothing here reaches the fair value.

## Our defect first, and what it was

The rule is to hunt our own error before explaining the market. This review found one,
and it was not in the model: five files read a study-local price file that this study
had already discredited in writing, ending 5 August 2026 at 105.20. It cost six
published figures — the moving-average stack, the cone, the percentile table, an
expired one-month check date, a "probability above spot" that was the probability above
105.20, and a figure drawing a cone opening at 105.20 under a line labelled "spot
130.00". None of them touched the fair value, and the gap does not close from any of
them. What closed instead is the class: there is one price reader now and it refuses
rather than returning something plausible.
## The eight standing headings, re-run against EGP 87.76

Every figure below is read out of `study_numbers.json` on this run. The 10-September
edition of this section carried a terminal risk-free of 12.50%, a terminal growth of
9.14% off a 2.0% real rate, a WACC gliding to 17.85% and a terminal value at 85% of
enterprise value. Three of those four have since moved and the section did not, which
is the defect this rewrite exists to stop rather than an argument about any one number.

### 1. LATEST FILINGS
Audited FY2023, FY2024 and FY2025 consolidated statements; the reviewed Q1-2026 interim
(13 May 2026) and the reviewed half to 30 June 2026 (11 August 2026), which is the most
recent disclosure and is read for segment revenue, segment margins, capex, net debt,
associates, minorities and the employees' statutory share. The issuer's own quarterly
earnings releases are read separately, and are labelled unaudited, for the cables
tonnage series and the engineering backlog. No disclosed period is skipped; the sweep
register records all of it with dates, and its study-year declaration lists Q1-2026 and
H1-2026 as disclosed and swept.

### 2. BASE YEAR
FY2025 is fully disclosed and every income-statement and balance-sheet line is the
audited figure, none derived. Two rows in Appendix A.1 are house derivations and are
labelled: EBITDA (EBIT plus D&A — the statements carry no EBITDA line) and earnings per
share. Segment revenue ties EXACTLY to consolidated revenue in every year. FY2026E is
anchored on the reviewed half's own measured like-for-like growth for all three segments
rather than a typed path [R-ANCHOR-01], and is cross-checked — not calibrated — against
the Q1-2026 print: the build's 370,194 against a 356,323 grossed-up implied full year.

### 3. MACRO COHERENCE
One inflation path governs the model: the house Egyptian terminal of 7.0%. The
terminal risk-free of 10.50% is DERIVED from it (7.0% inflation + 3.5% real
convention) and terminal growth of 9.14% is derived from the same inflation and a
stated real growth of 2.0%, so neither is a nominal rate somebody typed beside an
inflation assumption. Copper is escalated at the house US inflation rate, and the pound
path is the house EGP/USD path — the same one the hard-currency alternative deflates at.

### 4. DISCOUNT RATE
Ke = rf* + beta x the MATURE-MARKET premium + a country premium charged flat beside it
[R-COC-03] = 28.09%, where rf* = 18.91% is the local 10-year of 22.31% less the
sovereign default spread of 3.40%, so the country is charged exactly once and the
un-netted construction is retired. Beta 1.2249 is an own-stock weekly regression against
the published EGX30, and it applies to the mature leg only. The country weight is
0.5928 from the audited geographic split. WACC glides 26.65% to 15.34%. Cash is charged
for once, in the bridge, and the forecast interest is net of the cash balance the model
itself builds — the bridge record carries the disclosure that the same cash is both
added at face and netted inside the weights.

### 5. TERMINAL
Terminal growth 9.14% nominal = 2.0% real compounded with 7.0% inflation, held
BELOW Egypt's long-run real GDP growth [R-MACRO-02] — the gap is the share of the
economy the company is assumed to cede. It is coherent with the inflation inside the
terminal discount rate BY CONSTRUCTION rather than by coincidence: both read the same
house path. Terminal beta is carried to 1.00 under the named construction
`beta_to_one_split`, not held at the measured 1.225. Terminal value is 89% of
enterprise value, which is disclosed in the summary table, in the bridge and in the
caveats, and is why the sensitivity grid is centred on the adopted case [R-SENS-01].

### 6. BALANCE SHEET
The bridge stands on the audited 31 December 2025 sheet, the date the cash-flow model is
constructed at: EV 218,783 less net debt 20,560 plus associates 6,758 less minorities 19,832 less the
employees' statutory share, giving equity attributable of 162,574 — EGP 75.94 a share at that
date, rolled 246/365 of a year to the anchor. The June sheet is read and deliberately
not substituted. Minorities are charged at their PROFIT share, not at book, and the
difference is disclosed.

### 7. CLAIMS AGAINST THE RECORD
Every "does not disclose" and every "never" in this study was re-checked against the
filings. THIS PASS FOUND FOUR STANDING AND WITHDREW ALL FOUR. (a) The claim that the
company's quarterly releases "were not reachable from this research environment" —
withdrawn in section 7 and still standing in four other places, including the workbook
panel; the releases were held here throughout and carry the tonnage the Cables driver
is built on. (b) "No filing discloses the cap's headroom" in the equity bridge, while
this study computes that headroom at 9.1x from the wage bill disclosed in three notes
of the same statements. (c) Figure 3's caption, "no cell in the tested range reaches
the market price", over a grid with four cells above it. (d) The [R-STAR-01] case's
"one assumption reaches the market and nothing else comes close", above its own
decomposition showing two that clear the gap. All four now read their own numbers.

### 8. MULTIPLE CROSS-CHECK
At EGP 130.00 the market pays **11.9x the model's own FY2026E attributable earnings** and
an implied **EV/EBITDA of about 7.6x** on FY2026E EBITDA, against the model's own 5.7x
on its enterprise value. The trailing figures the study publishes are a P/E of 16.1x and
an EV/EBITDA of 10.5x. The earnings yield of 8.4% sits against an Egyptian 10-year at
22.31%: the market is paying a multiple that requires the cost of capital to be lower
than an Egyptian investor's alternative, which is the same disagreement the currency-of-
discounting question states from the other side.
