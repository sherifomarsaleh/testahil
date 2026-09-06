# PHDC over-forecasts, and it is one driver on the wrong clock

Read live: `python3 engine/phdc_walkforward/driver_fixes.py`

PHDC is the one name of five that OVER-forecasts its own history — **+0.468
pooled on 160 cells** — and the one whose published central sits well above the
market. Every other name in the book under-forecasts. Whatever is wrong here runs
the opposite way to everything the reassessment was built around.

## Two observations fix its shape before any fix is tried

**The bias does not compound**: +0.459, +0.475, +0.479, +0.484, +0.439 at
horizons one to five. A rate error compounds — that is what the under-forecasting
names do, and it is the signature [R-TERM-01] was adopted on. A flat bias at
every horizon is a LEVEL error.

**The level is the recognition rate.** `delta = revenue / (opening backlog + new
sales)` is a trailing three-year mean held flat forward, which is the correct
mechanical choice a priori — no judgement is involved and [R-FCAL-01] would
forbid one at a historical origin. But this company's realised delta fell
monotonically as its backlog compounded faster than it could deliver:

| year | delta realised |
|---|---:|
| 2016 | 0.3393 |
| 2017 | 0.3279 |
| 2018 | 0.3059 |
| 2019 | 0.2095 |
| 2020 | 0.1436 |
| 2021 | 0.1596 |
| 2022 | 0.2041 |
| 2023 | 0.1552 |
| 2024 | **0.1104** |

New sales went 8,194 to 151,016 while revenue went 5,631 to 27,167 — the
denominator grew 14.8x against revenue's 4.8x, so the rate had to fall
arithmetically. **Every origin used a delta above what happened**, eight of eight:

| origin | used | realised at h=1 | realised at h=3 |
|---|---:|---:|---:|
| 2016 | 0.3393 | 0.3279 | 0.2095 |
| 2017 | 0.3336 | 0.3059 | 0.1436 |
| 2018 | 0.3244 | 0.2095 | 0.1596 |
| 2019 | 0.2811 | 0.1436 | 0.2041 |
| 2020 | 0.2197 | 0.1596 | 0.1552 |
| 2021 | 0.1709 | 0.2041 | 0.1104 |
| 2022 | 0.1691 | 0.1552 | — |
| 2023 | 0.1730 | 0.1104 | — |

## The defect is [R-FCAL-01]'s trap (ii), named in the standing rule

Revenue is `delta x (backlog + new sales)` — a backlog-release clock. Cost is
`unit cost x DELIVERIES` — a delivery clock. **Two clocks.** The rule says in
terms that where revenue is recognised as work completes, cost must be too, or
operating leverage on a thin residual turns a gross-profit bias into a net-profit
forecast several times too high.

That is exactly what is measured. Revenue's own bias is only +0.107; **gross
profit's is +0.540**, and net profit's is +1.170.

## Both framings, neither adopted

One clock can be reached from either end. Both are defensible, both are
published, neither is averaged into the other:

| driver | n | as shipped | revenue on the delivery clock | cost on the revenue clock |
|---|---:|---:|---:|---:|
| revenue | 34 | +0.107 | -0.087 | +0.107 |
| cost of sales | 39 | -0.235 | -0.235 | **-0.066** |
| gross profit | 34 | **+0.540** | **+0.028** | +0.221 |
| profit before tax | 27 | +1.170 | +0.837 | +1.018 |
| attributable profit | 26 | +1.170 | +0.611 | +0.972 |
| **pooled bias** | 160 | **+0.468** | **+0.171** | +0.383 |
| pooled MAE | 160 | 0.732 | 0.838 | 0.697 |

Putting revenue on the delivery clock removes most of the lean and leaves gross
profit essentially unbiased, at a cost in MAE. Putting cost on the revenue clock
removes less of the lean and improves MAE. **Choosing between them changes a
delivered study's answer and is a ruling, not a measurement** — it is not made
here, and [R-FCAL-01] is explicit that a better point estimate is never the aim.

## In LEVELS the ranking is different, and a valuation is built on levels

The table above is log bias — the typical proportional error. A valuation adds
up pounds, so the same 26 cells decomposed in levels (every line present in both
projection and actual, so the identity closes):

| line | mean projected | mean actual | gap |
|---|---:|---:|---:|
| revenue | 15,221 | 14,274 | +947 |
| cost of sales | 6,747 | 8,989 | **-2,242** |
| gross profit | 8,474 | 5,208 | +3,266 |
| SG&A | 1,852 | 2,157 | -305 |
| admin depreciation | 540 | 169 | +370 |
| finance cost | 256 | 999 | **-742** |
| **profit before tax** | **5,827** | **2,215** | **+3,612** |

The identity closes to within 332 (other income, outside this list).

**Cost of sales under-forecast is 62% of the whole profit error**; revenue
over-forecast is 26% and finance cost 21%. The log table put revenue at +0.107
and cost at -0.235, which reads as revenue being the larger problem. It is not.
Log weights the small cells and levels weight the large ones, and they rank these
two differently — both are honest and the level ranking is the one a fair value
inherits.

This bounds what the clock fix achieves. Putting revenue on the delivery clock
takes gross profit from +0.540 to +0.028 in LOG terms, but in levels it removes
roughly the 947 of revenue over-forecast and leaves the 2,242 of cost
under-forecast standing.

## The largest line: construction cost escalated at consumer inflation

`cogs = cpu0 x infl x deliveries`, where `cpu0` is the trailing three-year unit
cost and `infl` is the Egyptian consumer-price path. Measured on this run's own
panel, PHDC's realised unit cost ran far ahead of consumer prices in almost every
year:

| year | cost of sales | units delivered | unit cost | unit cost y/y | CPI |
|---|---:|---:|---:|---:|---:|
| 2015 | 2,313 | 1,573 | 1.5 | — | 1.104 |
| 2016 | 3,887 | 2,049 | 1.9 | 1.290 | 1.138 |
| 2017 | 4,386 | 1,781 | 2.5 | 1.298 | 1.295 |
| 2018 | 4,743 | 1,541 | 3.1 | 1.250 | 1.144 |
| 2019 | 3,865 | 964 | 4.0 | 1.302 | 1.092 |
| 2020 | 3,176 | 633 | 5.0 | 1.251 | 1.050 |
| 2021 | 5,016 | 1,308 | 3.8 | 0.764 | 1.052 |
| 2022 | 9,038 | 1,281 | 7.1 | 1.840 | 1.139 |
| 2023 | 11,907 | 1,500 | 7.9 | 1.125 | 1.339 |

**Over 2015-2023 unit cost compounded 5.40x — 23.5% a year — against CPI's 3.10x
at 15.2%. That is 7.2% a year in real terms, 1.74x over the window.**

This is the cost-stack escalation rule the standing protocol already carries:
a per-unit cost stack gets one escalator per driver class, never one blended
index. Construction cost is steel, cement, rebar and site labour — a different
basket from consumer prices, and on this company's own record a materially
faster-moving one. Escalating it at CPI under-forecasts cost by construction, and
that under-forecast is **62% of the whole profit error** in levels.

Whether to correct it is a ruling, not a measurement. The defensible alternatives
each cost something: a construction-cost index is a new external source
(stop-and-inform under SIGCM), and the company's own realised unit-cost trend is
a trailing extrapolation, which this method's own evidence ranks as the weakest
of the three benchmarks.

## The finance cost is [R-FCAL-01]'s trap (i), and correcting it naively is worse

`kd = ttm_ratio("is.finance_cost", "bs.total_current_liabs", 3)` and
`interest = kd x debt0` with `debt0 = bs.total_current_liabs`. The standing rule
names this exactly: interest comes from the borrowings that actually bear it, and
dividing the finance charge by a broader liabilities total understates the rate by
a multiple. On a developer that total is mostly CUSTOMER ADVANCES, which bear no
interest at all. Measured on this run's own panel, interest-bearing borrowings are
between **0.9% and 35.8%** of total current liabilities, and the share moves by
year:

| year | total current liabilities | interest-bearing | share |
|---|---:|---:|---:|
| 2015 | 8,459 | 3,030 | 35.8% |
| 2018 | 17,985 | 1,159 | 6.4% |
| 2019 | 20,399 | 382 | 1.9% |
| 2023 | 41,069 | 3,596 | 8.8% |
| 2025 | 105,099 | 939 | 0.9% |

The run's own panel already carries `bs.loans_current`, `bs.loans_lt`,
`bs.overdraft` and `bs.banks_credit`, so the right denominator needed no new data
and was simply not used.

**Correcting the denominator alone makes the forecast WORSE**: finance cost goes
from -1.093 to -1.422 and the profit lines do not move. The rate rises, but it is
applied to an interest-bearing base that is FROZEN at the origin and that swings
thirty-fold across origins, so the product falls further than the rate rises.

There are two defects in one line — a denominator that includes balances bearing
no interest, and a base held flat while the company's borrowings moved by an
order of magnitude — and fixing one without the other is worse than leaving both.
A proper fix needs a projected debt path, which this model does not build.
**That is a stop-and-inform, not something to invent**: the digest's own warning
about this trap is that a correction which passes its first test and fails its
second is how a broken model gets a plausible answer today and fails differently
tomorrow.

## The measurement's own bug, recorded

The first version of the cost-side framing negated the cost line. The mutation
produced non-positive cells, the log score silently dropped them, the common-cell
count fell from 160 to 39, and the table read as "no change" — the shipped answer
under a fix's label. `build()` now raises when a mutation fails to land, which is
the negative-control discipline this repository applies to its gates, applied to
its own measurements.
