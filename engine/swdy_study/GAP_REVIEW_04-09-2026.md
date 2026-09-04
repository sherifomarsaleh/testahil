# SWDY — gap review, 4 September 2026

**AUDITED CENTRAL: 55.4826** — the cash-flow lens, EGP per share.
**AUDITED GAP: −38.7%** against the latest known price, EGP 90.50 (3 September 2026,
`engine/prices/SUPPLIED_03-09-2026.json`). Against the price this study was struck at,
EGP 105.20 (5 August 2026), the gap is −47.3%.

This fires the BELOW-price half of the trigger, where [R-GAP-02] also blocks publication
until either the gap closes or a MARKET_DISSENT is filed. That is the right posture and
this review does not attempt to talk the study past it.

## What this review found, in one line

**Four material corrections were applied to this study before the review began, and they
nearly cancelled — and the review's own remaining findings run AGAINST the price, not
toward it.**

| correction | direction | effect on the cash-flow lens |
|---|---|---|
| Segment margins re-anchored on the reviewed half | away from the price | **−40.6%** |
| Terminal: growth derived, sanctioned construction | toward | **+12.6%** |
| Corporate load re-anchored on the reviewed half | toward | **+69.1%** |
| Employees' statutory share of profit, charged | away | **−12.5%** |
| **net** | | **−1.1%** (56.08 → 55.48) |

A study can be wrong in four material ways and land almost exactly where it started.
Nothing in the answer would have shown it.

---

## LATEST FILINGS

Every disclosed period has been read, and the register was re-walked against El Sewedy's
own investor-relations portal on the day of this review rather than trusted.

**The route is recorded because it was not trivial and an absence asserted from the first
404 would have been wrong** [R-IND-01]: `elsewedyelectric.com/en/investor-relations` returns
404, the homepage carries no `href` to investor relations at all — the link is rendered
into a social-icon block pointing at a separate host — and the results centre at
`ir.elsewedyelectric.com` is JavaScript-rendered, its document list arriving from
`api/filter_results_center_sections` on a POST needing a CSRF token paired with the session
cookie. A headless browser was tried first and reset through the proxy; calling the API
directly with a freshly-paired token worked. Both 2025 and 2026 filings are public.

| Document | Date | Read |
|---|---|---|
| Audited consolidated financial statements, year ended 31 Dec 2025 | Mar 2026 | yes — statements and notes 16, 17, 29, 39 |
| Reviewed condensed interim statements, six months to 30 Jun 2026 | **11 Aug 2026** | yes — statements and notes 16, 17, 20, 27, 28, 29, 31, 38 |
| Q1-2026 condensed interim statements | 13 May 2026 | yes, in the first edition |

**THE STUDY WAS RIGHT AT STRIKE.** The H1-2026 statements were approved for issuance on
**11 August 2026** (note 2-1), six days AFTER this study was struck on 5 August. The first
edition consumed Q1-2026 and everything before it, and there was no unread filing on its
desk — the opposite of the defect this heading exists for, recorded because it was checked
rather than assumed.

It was stale by the time of this review, and [R-GAP-01 AMENDED] forbids delivering against
a stale record. The half is now consumed, and it re-anchored every segment margin and the
corporate load.

**Found: nothing at strike; a stale record now, corrected.**

## BASE YEAR

FY2025 is a filed audited full year and every historical line reconciles: segment revenue
sums exactly to the consolidated figure in all three years, segment profit less the
corporate load reproduces the audited operating profit in all three, and the note-17 PP&E
table foots three ways (components to subtotal, subtotal plus projects under construction
to total, and component charges to the total charge).

**One naming defect was found and it nearly cost this review its own conclusion.** The
study registers the note-16 **segment profit** row — gross profit less selling and
distribution — under a key named `gp`. The first draft of the margin analysis compared that
series against a GROSS-profit margin computed from the reviewed half, which is [L-289]
exactly: a ratio between two quantities defined differently is not evidence about either.
It computes, it looks like a measurement, and it pointed the wrong way — 20.6% instead of
5.2%, and uniform instead of mixed by segment. The key is now documented; the value was
always right and the label was not.

**Found and corrected.**

## MACRO COHERENCE

The first edition carried a terminal growth rate of 5.0% nominal whose own registered
justification named its own inflation assumption: *"a terminal risk-free rate that itself
embeds 5% inflation, so the base case assumes approximately zero real terminal growth"*.
The house Egyptian path's terminal inflation is **7.0%**.

So the reasoning was right and the number was struck against an inflation rate this house
does not hold, making the real assumption a **decline of 1.87% a year in perpetuity** — on
a terminal carrying more than four fifths of enterprise value, and written down nowhere.
[R-MACRO-01] permits real decline and requires it to be stated as the real number it is.

It is the EGCH defect in the same shape: the inflation figure doing the work sat inside a
justification rather than in a declared input, where no gate could reconcile it.

Corrected: real growth is now a STATED zero and the nominal rate is DERIVED from the house
ladder at 7.0%. That also brings the explicit window inside the convergence requirement —
the last explicit year grows 8.8% against a 7.0% terminal, a 1.8pp gap, where 5.0% left
3.8pp and capitalised a rate the model never reached.

**One residual is registered rather than closed:** the study's terminal risk-free rate is
10.5% against the house derivation of 12.5% (7.0% terminal inflation plus the 5.5%
real-rate convention). Correcting it would LOWER this value further, i.e. widen the gap.

**Found and corrected; one residual named, running away from the price.**

## DISCOUNT RATE

**This is where the gap is, and every correction available here widens it.**

| | |
|---|---|
| Cost of equity, explicit window | 28.40% |
| Cost of capital, explicit window | 26.63% |
| Cost of capital, terminal | 15.93% |

That is an Egyptian cost of capital on an Egyptian risk-free rate of 22.31%, and it is
real: the sovereign yields what it yields. At a 15.93% terminal rate against 7.0% growth
the perpetuity capitalises free cash flow at 11.2x, and on this company's cash conversion
that lands at an implied **3.2x forward enterprise value to EBITDA** — see the multiple
cross-check below, which is the same finding from the other side.

Two things were checked here and BOTH run against the price:

- **The cost of debt.** The adopted Kd is 9.50% against a sovereign risk-free of 22.31% —
  a corporate borrowing 12.8 points BELOW its own government, which [R-COC-01] refuses
  outright on a local-currency book. The book is majority foreign-currency, so the figure
  is a foreign coupon, and the rule requires FX debt at LOCAL-EQUIVALENT cost. The study
  computes that equivalent at 13.90% and publishes the result — EGP 55.16 against 55.48 —
  as an alternative without adopting it. Adopting it lowers the value.
- **The terminal risk-free**, above: 200bp below the house derivation, and correcting it
  lowers the value.

**The one construction that runs the other way is published and is the crux of this
study**: 52.6% of forecast revenue is earned in hard currency, and discounting a
dollar-linked cash stream at a pound cost of capital over-penalises it. The
currency-of-discounting alternative — the hard-currency leg deflated to dollars, discounted
at a USD cost of capital of 10.13%, and only then translated back — reads **EGP 69.58**,
+25.4% on the central and −23.1% against the latest price. It is published beside the
central and never averaged into it.

**Found: the gap, and it is one parameter — the currency the cash flows are discounted in.**

## TERMINAL

The terminal carries **85.0%** of enterprise value, so any error here is most of the answer.

The published construction was the retired reinvestment identity `rr = g/ROIC`, which
charges `g × IC` every year for ever and implies a replacement cycle of `1/g`. **Unlike the
sister case, the implied cycle here was roughly right by accident**: 1/g at the old 5% is
20.0 years against a life this company's own accounts derive at 17.26, because Egypt's
higher inflation makes 1/g smaller. That is [R-TERM-01 CLAUSE TWO]'s direction problem from
a third angle, and it is why the correction on this name is driven by the GROWTH RATE
rather than by the life.

The life was derived by identity from note 17 — average depreciable gross cost over the
year's own charge, excluding land (which the policy note states is not depreciated) and
projects under construction (not yet in use) — at **17.26 years**, with every component
reading in or near its disclosed range.

**A second error of mine was caught by the model's own numbers and is recorded rather than
quietly fixed:** the first draft struck maintenance on the FY2025 gross cost escalated for
inflation alone, while the model itself adds five years of capex and grows net depreciable
PP&E from 24,806 to 90,938 — 3.67x. It showed as a maintenance charge of 7,916 against the
model's own FY2030 capex of 17,212. Moved onto book D&A escalated over half the derived
life, which carries the built-up base: 13,315.

Rebuilt through the sanctioned module the terminal is EGP 223,872 against the retired
construction's 208,581 on the same inputs — +6.8%, with an implied payout of 56.9% of
terminal NOPAT and 8.6% above the NOPAT-perpetuity floor.

**Found and corrected, worth +12.6%.**

## BALANCE SHEET

**The bridge stands on 31 December 2025, and the reviewed 30 June 2026 sheet is
deliberately NOT used.** That needs stating, because [R-BRIDGE-01] asks for the latest
disclosed sheet and one now exists showing net financial debt up from 20,560 to 28,629 over
the half.

It was tried the other way and it double-counts. That deterioration is not information the
model lacks: the model's OWN FY2026 forecast absorbs cash on exactly that mechanism — a
working-capital movement of 17,783 against capex of 16,281, giving free cash flow to the
firm of −4,268 for the year. Deducting the June net debt from a valuation dated 31 December
2025 charges one cash outflow twice, which is [R-BRIDGE-01](iii) in mirror image. The rule's
requirement is the latest sheet CONSISTENT WITH the valuation date; moving the valuation
date to June is a different exercise, with the explicit window starting from the second
half. The half reaches this study through the FORECAST, where it belongs.

One item runs against this study and is recorded because it does: the minority is deducted
at a 9.7% share of value, against non-controlling interests of 7.47% of total equity at 30
June 2026, 7.11% at December and 6.81% of the half's profit. The study's figure is
conservative on all three readings, and the alternative sequencing is published at EGP
62.37.

**Found: nothing, and one construction deliberately declined with its reason.**

## CLAIMS AGAINST THE RECORD

**One material claim was found to be missing rather than wrong**, and it is the largest
single defect this review corrected.

Egyptian company law gives employees a share of distributable profits. El Sewedy discloses
it BELOW profit attributable to owners, in the earnings-per-share note, because it is an
appropriation of profit rather than an operating cost — so **it appears in no line of the
income statement**, and a cost stack built from unit economics can never capture it:

| | attributable profit | employees' share | % |
|---|---:|---:|---:|
| FY2024 | 17,461.4 | 2,025.8 | 11.60% |
| FY2025 | 17,330.2 | 2,073.1 | 11.96% |
| H1-2026 | 9,921.7 | 1,291.2 | 13.01% |

The word "employee" occurred nowhere in the first edition's committed numbers, and the
valuation divided the whole parent equity value by the whole share count. The study held
both halves of the arithmetic that exposes it — attributable profit of 17,330.245 AND the
reported EPS of 7.13 — and 17,330.245 / 2,140.778 = 8.095. **Nothing reconciled them.**

Charged at the three-period mean of 12.19%, worth −12.5%. The statutory cap at total annual
wages is NOT modelled — nothing in the filings discloses its headroom — so the charge is an
upper bound and the direction of the unmodelled cap is recorded rather than guessed.

**Found and corrected, and it runs against the price.**

## MULTIPLE CROSS-CHECK

This is the discount-rate finding restated, and it is the sharpest thing in the review.

| | at the fair value of 55.48 | at the price of 90.50 | benchmark |
|---|---:|---:|---:|
| P/E on FY2025 earnings after the employees' share | **7.8x** | 12.7x | — |
| EV/EBITDA on FY2027E | **3.2x** | 4.9x | **6.5x** justified by this study's own relative lens |

**The cash-flow lens implies an enterprise multiple of 3.2x against the 6.5x this study
itself calls justified** — less than half, and below any plausible industrial multiple in
any market. The relative lens reads EGP 80.58 precisely because it applies that 6.5x.

So the disagreement between this study's own two lenses is entirely the multiple, and the
cash-flow lens's implied 3.2x is the outlier. That is not an argument that the cash-flow
lens is wrong: at a 26.63% pound cost of capital, 3.2x is what the arithmetic gives. It is
an argument that **the answer turns wholly on whether a company earning 52.6% of its
revenue in hard currency should be discounted at a pound rate** — which is exactly what the
currency-of-discounting alternative at EGP 69.58 prices, and which this study publishes
beside the central rather than averaging in.

**Found: the same single parameter, from the other side.**

---

## Verdict

The answer does not change, and this study remains held under [R-GAP-02] until it either
closes the gap or files a MARKET_DISSENT.

Four corrections were applied and nearly cancelled. Two further findings — the cost of debt
below its own sovereign and a terminal risk-free 200bp under the house derivation — both
run AWAY from the price and are registered rather than applied, because [R-VCAL-01]'s
promotion guard forbids stacking individually-justified moves without watching where the
total lands, and this study has already taken four in one pass.

**What a reader should weigh, and it is not resolved here.** Every heading either found
nothing, found something that was corrected, or found something pointing at one place: the
currency the cash flows are discounted in. A company earning most of its revenue in dollars
is being valued at a 26.63% pound cost of capital, and the market is paying 4.9x forward
EBITDA where that arithmetic says 3.2x. The alternative is computed, published at EGP
69.58, and left as an alternative — because choosing it would be choosing the answer, and
a fair value moved toward a price is the reverse-engineered rate this method prohibits
outright.

**What would change the verdict:** a defensible basis for discounting the hard-currency leg
at a hard-currency rate as the CENTRAL rather than the alternative. That is a method
question rather than a fact about this company, it applies to every exporter in this book,
and it belongs in the method reassessment rather than in one name's review.
