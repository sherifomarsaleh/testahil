# SWDY — valuation-gap review, 9 September 2026  [R-GAP-01] [R-GAP-04]

**AUDITED CENTRAL: 39.5540**
**AUDITED GAP: -71.0%** against 136.20, the latest known close. Against the 130.00 the
study is struck at, -69.6%.

**THIS EDITION SUPERSEDES THE REVIEW OF 8 SEPTEMBER, which audited 43.5108 at -66.5%.**
Four corrections landed between them and **three of the four moved the answer AWAY from
the traded price.** The net is -3.96 a share and the gap widens by four and a half points.

That sentence is the point of this document. [R-GAP-04] was adopted because referral is
the easy way out of a gap; it says the search for OUR OWN error must be exhaustive and
recorded before a gap is called genuine. It does not say the search must find something
that closes it. On this name the search found four real defects and the arithmetic went
the other way.

## What moved

| # | correction | worth |
|---|---|---|
| 1 | Capex re-anchored on the reviewed half — the model charged 23.0% more FY2026 capex than the company's own filed half implies | **+0.87** |
| 2 | Exchange-rate history: two of three years typed as house averages while note 44-3 discloses them | **+1.00** |
| 3 | Segment mix: every segment's FY2026 growth wrong while the group total was right to a third of a point | **+2.20** |
| 4 | Terminal risk-free built on a typed 5% inflation four rows below a growth line using the house 7% | **-8.03** |
| | **net** | **-3.96** |

### 1. The reviewed half discloses capex, and nobody had registered it

This study already reads the six months to 30 June 2026 for revenue, gross profit,
operating profit, net finance costs, associates, tax and attributable profit. Two lines
below those, in the same statement of cash flows, it discloses capex. All four half-year
figures are registered now, 2023 through 2026.

Capex of 5,435.909 against 5,386.809 a year earlier — **up 0.91%** — while revenue over
the same halves rose **31.92%**. `capex_pct` was a House glide tapering from FY2025's
4.665% on a story about the expansion cycle completing, set before the half was read, and
it charged FY2026 capex of 16,281 against 13,232.

The standard is this study's own: `corp_load` sits eight lines above `capex_pct` in the
same register and was re-anchored on the same filing in these words — *"the reviewed half
measures the level holding, and no disclosure names a mechanism that would take it back
up"*.

**No seasonality assumption is used, because the seasonality will not support one:** the
H1 share of full-year capex is 39.1%, 54.1% and 41.1% across the three disclosed years.
The half is compared with the SAME HALF of the prior year and that growth rate applied to
the audited full year. The finding survives every one of the three patterns anyway —
annualising H1-2026 at the most H2-weighted year on record still gives 13,890.

Note which way the out-years cut: the measured rate is held flat rather than tapered, so
FY2029 and FY2030 are charged MORE capex than the retired path. Over five years the two
differ by under 1%; the +0.87 is almost entirely timing.

### 2. The issuer discloses its own exchange rate and two of three years were typed

`fx_hist` read FY23=30.59, FY24=45.3, FY25=49.5, and said so plainly: FY2023 *"is the
audited FY2023 filing's own disclosed figure (Note 44-3-1); FY2024/FY2025 are house
averages consistent with the scale of the disclosed devaluation"*. Note 44-3 of the FY2025
audited statements prints the same table for both years — **average USD 47.69 and 43.96**.
The study knew the note existed, read it for one year, and estimated the other two, 3.8%
and 3.1% high.

It is a DENOMINATOR, so correcting it raises forecast growth: this correction moves the
cables line **further** from what the reviewed half measures, not closer, and it is made
because the figure is disclosed and the one it replaces was not.

### 3. A right group total over a wrong mix

This study registers note 16's segment revenue for **both comparable halves** —
`seg_rev_h1_26` and `seg_rev_h1_25`, footing exactly to the two group figures — and
forecasts segment growth from three separate constructions, and **nothing ever held one
against the other.** Two readings of one fact in one file, never put side by side
[R-ENF-03].

| segment | model FY2026 | halves, like-for-like | error | segment margin |
|---|---|---|---|---|
| Cables | +47.60% | +30.57% | **+17.0pp** | 11.4% |
| Constructions | +18.00% | +27.44% | −9.4pp | 9.0% |
| Electrical products | +20.00% | +48.28% | **−28.3pp** | 23.6% |
| group | +34.65% | +31.92% | +2.7pp | |

The group was nearly right and every segment was wrong, and the error over-weighted the
cheapest of the three and under-weighted the richest. FY2026 is now anchored on each
segment's own like-for-like half growth; the constructions still govern FY2027 onward.

**The cables correction is deliberately NOT pushed into `cables_real_growth`.** Forcing
the copper x FX x real construction to hit the measured 30.57% implies a **5.4% real
volume decline**, and that input exists to refuse exactly such a story: *"the model should
not manufacture a volume story it cannot evidence"*. Which of copper, the rate or volume
accounts for the miss is not resolvable — the interim omits the average-rate table the
audited statements carry — so the study declines to attribute it.

The comparison is now a gate, verified by breaking the anchor and watching it fire. Two
drafts of an accompanying GROUP check failed and **both were the check being wrong**: one
missed the −246.711 unallocated item, the other missed that three correct growth rates
weighted by a full-year mix cannot reproduce a half's blended rate. Both were re-pointed
rather than given a tolerance [R-COC-01] — a standing 0.20pp band would have covered a
real disagreement of exactly that size.

### 4. Two inflation rates in one terminal, four rows apart — the one that cost 8.03

`g_term` reads *"(1 + 0.0 real growth) x (1 + 7.0% long-run Egyptian inflation)"* and
states, in its own source string, that **"the house macroeconomic path is the ONLY source
of an inflation rate in this study"**. `rf_term`, four rows below it in the same register
block, built the terminal risk-free on a typed 5%: 5.0 + 5.5 = 10.50%.

Both describe the same perpetuity, so one of them was false — and it is the claim four
rows up that makes it false rather than merely different.

The house path sets out the rule itself, in `engine/macro_paths/EG.json` under
`real_rate_convention`: *"The terminal NOMINAL risk-free rate is DERIVED as this plus the
inflation target in force, so the single most terminal-value-sensitive number in a model
cannot"* be typed. The target in force there is 7.0% — the 2030 step, *"the target band
midpoint in force, held"*, sourced to the CBE's own Q1-2026 Monetary Policy Report.
**7.0 + 5.5 = 12.50%.**

**ARCC fought this exact argument and settled it.** That study carried 10.50% built the
same way, argued for the central bank's LONGEST-dated published target of 5% against
revision 3's NEAR-dated 7%, and the resolution was to stop choosing: derive from the house
path, *"and so no longer this study's own reading of which published target to use"*. If
5% is the right terminal inflation for Egypt, that is an argument for amending EG.json —
which every study would then inherit — not for one study substituting its own number and
the next one substituting a different one [R-MACRO-01].

The terminal cost of capital moves 17.22% to 18.92% and the terminal falls from 81% to
77% of enterprise value.

## What was searched and did NOT move the answer

**The associates, carried at book while earning 23.2% on that book.** A review asked why
the bridge takes the lower figure. [R-BRIDGE-01] is market-if-listed or book, so the
question is whether any investee is listed. **Note 20 names all of them and not one is:**
Elsewedy Cables Qatar, Doha Cables Qatar, Senyar Industries Qatar Holding, Aloula, SC Zone
Utilities, SWIEP, Raneen Energy, Yanbu Copper Wires and an unnamed residual. Book is not
the conservative choice here; it is the only route the rule leaves open.

The book also reconciles, which is what says it is not stale: it rose only 283.603 against
1,568.903 of earnings because note 20 discloses a **1,174.475 cash dividend from Senyar on
31 December 2025** — the same figure the cash-flow statement carries on its own line.
Equity accounting reduces carrying value by a distribution pound for pound and the cash
arrives in the group's own balance, which this bridge already counts. 1,568.903 less
1,174.475 is 394.428 against 283.603 of book growth, and the 110.825 difference is the
foreign-currency translation the same note discloses (135.317) net of the Elastmold
disposal.

One thing the review's ratio understates: **978.173 of the book (14.5%) is Yanbu Copper
Wires and the residual, both earning nothing in either year.** The return on the book that
actually earns is 27.1%.

## The eight standing headings, re-run against the new number

### 1. LATEST FILINGS

Unchanged and re-confirmed, and this pass READ MORE OF THEM than any before it. Every
disclosed period is covered: audited FY2023, FY2024 and FY2025 consolidated statements,
the Q1-2026 condensed interim, and the reviewed condensed interim for the six months
ended 30 June 2026, approved for issuance 11 August 2026. That half remains the latest
disclosed and nothing newer exists at this date.

What changed is how much of it the study uses. Three of tonight's four corrections come
out of filings this study already held and had not fully read: the half's statement of
cash flows (capex, all four years), note 44-3 of the FY2025 statements (the exchange-rate
table), and note 16's segment revenue for both comparable halves — the last of which was
already REGISTERED and simply never compared with the forecast. That is a sweep finding as
much as a valuation one.

### 2. BASE YEAR

Unchanged in construction. The forecast is built segment by segment on the note 5-3
external-revenue view and the note 16 segment-profit view, both reconciling EXACTLY to the
consolidated revenue line their own filings print, asserted in code before either is used.
The corporate-load bridge reproduces audited FY2025 operating profit to within a pound.
Nothing is annualised, scaled or solved.

**The forecast-anchor item on this heading is materially improved and is not closed.** The
FY2026 first year is now MEASURED rather than forecast at the segment level — each
segment's growth is its own like-for-like half growth from note 16 — so the first year no
longer disagrees with the half at all on revenue. The margin anchor is unchanged and this
study stays on the forecast-anchor ratchet with its reason printed: "the latest reviewed
period is a half" is not on the closed list, and on a like-for-like half-against-half the
forecast is 0.99% below rather than 13.69%.

### 3. MACRO COHERENCE

**This is the heading that changed, and it changed because it was WRONG.** The previous
review recorded it as "unchanged — the study carries no inflation number of its own". That
was false and this pass found it: `rf_term` carried a typed 5% inflation while `g_term`
used the house 7% and asserted the house path was the only source of an inflation rate
here. One model, one perpetuity, two inflation rates. Both are now the house path's, read
live from `engine/macro_paths/EG.json` rather than copied, so a house amendment moves both
or neither. Inflation, currency and price paths are mutually consistent for the first
time on this name.

### 4. DISCOUNT RATE

The explicit-window schedule is unchanged: 28.84% in FY2026 gliding down. The TERMINAL
rate moves 17.22% to 18.92%, entirely from the risk-free correction above, and it is
derived rather than chosen. The beta is unchanged from the 8 September re-derivation
against the published EGX30. Nothing in the discount rate is reverse-engineered from a
price, and the reverse read below states what rate the price would require.

### 5. TERMINAL

The terminal is built through the sanctioned module on book depreciation escalated over
half the derived asset life, not on g x IC. It now falls from 81% to **77% of enterprise
value**, which is the one respect in which tonight's corrections make the answer rest less
on the perpetuity and more on the explicit window. The capex re-anchoring does not reach
it — the maintenance charge is struck on book D&A, not on the capex path — and that is
stated so nobody infers a link that is not there.

### 6. BALANCE SHEET

Unchanged. The bridge deducts net financial debt at 31 December 2025, the date the
valuation is struck at, and every lens is rolled to the 3 September 2026 anchor at the
cost of equity net of the dividend paid inside the window.

The bridge stands on the December sheet while the latest disclosed is 30 June 2026, and
the record says so rather than claiming otherwise. The study's reason — that the
+EGP 8,208.8mn deterioration over the half is the same working-capital absorption the
FY2026 forecast already carries, so deducting it again charges one outflow twice — is real
and is not what the rule tests. This study stays on the bridge ratchet with that stated.

The associates leg was interrogated this pass and stands: see the section above.

### 7. CLAIMS AGAINST THE RECORD

Re-run, and this pass found claims that were false and fixed them rather than confirming
them. Three delivered sentences asserted things the filings contradict or the model does
not produce:

- `capex_pct`'s story about a completing expansion cycle, set before the half that
  measures the cycle was read.
- `fx_hist`'s "house averages consistent with the scale of the disclosed devaluation",
  against a note that discloses the averages.
- `rf_term`'s "the CBE's own stated medium-term inflation target of 5%", against a house
  path recording 7% as the target band midpoint in force.

Separately, the sensitivity narrative carried a ratio that **rewrote itself on every
correction**: it divided a fixed historical 49.7076 by the LIVE central, so a statement
about a superseded edition was silently re-measured against every later answer. It now
quotes the absolute figure, registered as the superseded number it is.

`prose_check` reports **556 figures checked, 0 unmatched** — from 7 at the start of this
pass. Every figure in the delivered documents now reconciles to a number this study
produces.

### 8. MULTIPLE CROSS-CHECK

At EGP 39.55 the cash-flow lens sits below every cross-check this study publishes: the
relative multiple reads 73.89, normalised earnings 102.05, the book lens 41.95, and the
span across all lenses is 15.72 to 102.05. The central is the class primary and the
cross-checks are published beside it, never averaged in — **and the disagreement is wider
after this pass than before it**, which is information rather than a problem to smooth.

The reader should weigh what that means. Three lenses built on trailing earnings and
historical-cost book sit above a cash-flow lens discounting at 28.84% falling to 18.92%.
On a company whose value is three-quarters terminal, the cash-flow lens is the one most
sensitive to the discount rate, and this pass has just raised that rate by 170 basis
points at the terminal. That is the honest shape of the disagreement and it is published
rather than reconciled.

## The reverse read

136.20 requires a terminal cost of capital of **10.76%**, from a terminal risk-free of
**2.90% in Egyptian pounds** against 7.00% terminal inflation — a real risk-free of
**−3.83% in perpetuity**, 19.4 points below the observed ten-year EGP government yield.
Or every segment margin multiplied by 1.685: a **17.2% group operating margin for ever**
against an all-time high of 12.65%.

That is not a belief somebody could hold. It is an impossibility, and it is now further
out of reach than it was this morning, because correcting the terminal risk-free raised
the rate the price has to argue down.

## Standing

The gap is **-71.0%** and this review does not close it. Four defects were found and
priced; the net took the answer further from the market. Under [R-GAP-04] the direction is
not the test — the search is — and what the search says on this name is that the model's
errors were not the reason for the disagreement.

No fair value was moved toward a price at any point. Nothing here is published;
`assets/data.js` carries the pre-calibration range.
