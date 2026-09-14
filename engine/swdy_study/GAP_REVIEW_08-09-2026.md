# SWDY — valuation-gap review, 8 September 2026  [R-GAP-01]

**AUDITED CENTRAL: 43.5108**
**AUDITED GAP: -66.5%**

**Why a new review one day after the last one.** The 7 September review audited a central
of EGP 52.6969 at a gap of −59.5%, and it audited that gap honestly. One further lever has
since been applied and it moves the gap by seven points — past the five-point staleness
tolerance, which is half the ten-point trigger this rule is stated in. A review of a
different disagreement is not a review, so this one replaces it. **Everything the earlier
review found still stands**; what follows re-runs the eight headings against the new
number and states, heading by heading, what the lever changed and what it did not.

**The lever, and it is one.** The beta was re-derived against the published index of the
exchange this stock is listed on, replacing an equal-weight composite of the covered EGX
library. Beta 1.0087 → 1.2249, cost of equity 28.40% → 30.44%, explicit cost of capital
26.94% → 28.84%, terminal 15.93% → 17.22%, central EGP 52.6969 → 43.5108. The route is in
`rebuild_ledger.json`, where it is the fifth lever and the declared audit point.

**Outcome.** THE ANSWER IS AUDITED AND IT DOES NOT CHANGE FOR THE PRICE — and this lever
is the sharpest available evidence of that, because it moves the answer FURTHER FROM the
price on a name already sitting far below it. The composite beta was understating the
discount rate; correcting it was required whichever way it landed.

---

## 1. LATEST FILINGS

Unchanged and re-confirmed. Every disclosed period is read: the audited FY2023, FY2024 and
FY2025 consolidated statements, the Q1-2026 condensed interim, and the **reviewed condensed
interim consolidated statements for the six months ended 30 June 2026**, approved for
issuance on 11 August 2026. That half is the latest disclosed and nothing newer exists at
this date. The beta lever touches no filing.

## 2. BASE YEAR

Unchanged. The forecast is built segment by segment on the note 5-3 external-revenue view
and the note 16 segment-profit view, both of which reconcile EXACTLY to the consolidated
revenue line their own filings print — asserted in code before either is used. The
corporate-load bridge reproduces the audited FY2025 operating profit to within a pound.
Nothing is annualised, scaled or solved.

**The open item on this heading is the forecast anchor and it is unchanged too.** The
forecast opens at a group segment-profit margin of 12.08% against a latest reviewed
H1-2026 of 13.9966% — 13.69% relatively below, with no mechanism on the closed list
supported. The study's own record states plainly that the gap is a HALF-AGAINST-YEAR basis
difference on an issuer whose filed halves are 3.33 points apart (H1-2025 14.1369%, implied
H2-2025 10.8036%, a seasonal ratio of 0.764), and that "the latest reviewed period is a
half" is not on the closed list. It is recorded as failing rather than argued away, and
this study stays on the forecast-anchor ratchet with the reason printed. **On a like-for-like
half against half the forecast is 0.99% below, not 13.69%** — which is why nothing is being
corrected here on a comparison of two quantities defined differently.

## 3. MACRO COHERENCE

Unchanged. Inflation, currency and price sit on the house Egyptian path; the study carries
no inflation number of its own. The beta lever changes no macro input.

## 4. DISCOUNT RATE

**This is the heading the lever sits in, and it is now stronger than it was.**

The cost of capital glides rather than sitting at one crisis-level rate: 28.84% → 24.96% →
21.74% → 19.16% → 17.22%, terminal 17.22%, with the glide fractions taken from the
cost-of-debt path's own cumulative progress rather than chosen. Country risk enters exactly
once — the risk-free is normalised by this sovereign's own default spread on the same basis
as the premium added back. Weights are market-value.

**What changed.** The beta is now 1.2249 from `beta_regression.own_stock_beta()` against
`raw_indices/EG/EGX30.csv`, R-squared 0.368 over 256 weekly observations, Dimson-corrected,
conforming. The withdrawn composite gave 1.0087 at an R-squared of 0.291 — **21.4% low, and
explaining less of the stock**. Two defects sat in one line: the regressor was a coverage
artefact rather than a market, and the number was TYPED into the input register as a
literal 1.009, so re-running the regression to any answer at all would have moved nothing.
It now reads the committed regression record, which asserts its own conformity.

**Two things this heading still flags, both recorded and neither corrected in this pass:**

- **Cash is netted in the weights and added back at face in the bridge.** The debt weight is
  6.88% net against 18.34% gross. On a net-DEBT company this runs opposite to the case the
  rule was written on — net weights understate the debt weight and, with a cost of debt far
  below the cost of equity, RAISE the discount rate and LOWER the value. Correcting it moves
  the answer UP.
- **The cost of debt is the currency-blended rate, not the local-equivalent one.** The book
  is 28.4% pound and 71.6% foreign, back-solved from two disclosed rates. The amended rule
  requires the foreign tranche at local-equivalent cost — the foreign coupon plus expected
  depreciation — and the study computes that blend and publishes it unused. Adopting it
  RAISES the cost of capital and LOWERS the value.

**They point opposite ways and that is why neither is taken here.** A lever is applied one
at a time with its own ledger entry, and a pass that took both because they roughly cancel
would be recording a net effect nobody could audit.

## 5. TERMINAL

Unchanged in construction, and the terminal now discounts at 17.22% rather than 15.93%.
Terminal value is 82% of enterprise value — down from 84%, because a higher terminal rate
shrinks the terminal's share, which is the arithmetic working in the direction it should.
The terminal is built through the sanctioned module on the DISCLOSED useful life of 17.2627
years derived from note 17, and is brought home on the same cumulative factor as the last
explicit year.

**Still recorded and still not corrected: the terminal risk-free is 10.50% against a
house-derived 12.50%.** That is a lever worth its own entry, and it runs the same way as
the two above — conforming it would raise the terminal rate and lower the value further.

## 6. BALANCE SHEET

Unchanged. The bridge deducts net financial debt at 31 December 2025, the date the
valuation is struck at, and every lens is rolled to the 3 September 2026 anchor at the cost
of equity net of the dividend paid inside the window. **The roll now compounds at 30.44%
rather than 28.40%**, which is the one place the beta lever reaches the bridge, and it is
mechanical.

The bridge stands on the December sheet while the latest disclosed is 30 June 2026, and the
record says so rather than claiming otherwise. The study's reason — that the +EGP 8,208.8mn
deterioration over the half is the same working-capital absorption the FY2026 forecast
already carries, so deducting it again charges one outflow twice — is real and is not what
the rule tests. This study stays on the bridge ratchet with that stated.

## 7. CLAIMS AGAINST THE RECORD

Re-run. Every superlative in the delivered document reproduces from the filed series the
study commits. The beta lever introduces one new claim and it is checked here: **"the
composite understated the beta by 21.4%"** reproduces as 1.2249/1.0087 − 1 = +21.4%, and
**"explains less of the stock"** as 0.368 against 0.291. Neither is typed; both are computed
in `beta_reg.py` from the two regression records and printed.

## 8. MULTIPLE CROSS-CHECK

At EGP 43.51 the cash-flow lens sits below every cross-check this study publishes: the
relative multiple reads 70.15, the book floor 49.21, and the span across all lenses is
16.18 to 126.96. **The central is the class primary and the cross-checks are published
beside it, never averaged in** — and the disagreement is wider after this lever than before
it, which is information rather than a problem to be smoothed.

**The reader should weigh what that disagreement means.** Three lenses built on trailing
earnings and historical-cost book sit above a cash-flow lens discounting at 28.84% falling
to 17.22%. On a company whose value is two-thirds terminal, the cash-flow lens is the one
most sensitive to the discount rate, and this pass has just raised that rate. A reader who
thinks the correct beta for this issuer is nearer the market's own 1.0 has the withdrawn
figure and its full statistics published beside the adopted one.

---

## Verdict

**The answer is audited and it moved further from the price because a standing rule
required it.** The correction was not withheld for where it lands and would not have been
taken for where it lands.

**What a reader should weigh.** The gap is now 66.5% and three separate levers remain
recorded and unapplied — the gross-weight construction, the local-equivalent cost of debt,
and the house terminal risk-free — of which one raises the value and two lower it further.
None is applied in this pass because levers are taken one at a time. **This study remains
HELD under [R-GAP-02] and nothing here reaches the live site.**
