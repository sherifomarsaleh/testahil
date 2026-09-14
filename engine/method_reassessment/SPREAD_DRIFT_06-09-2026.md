# The spread moves with the price, and that is the whole error

Read live: `python3 engine/valuation_calibration/spread_drift.py`

The clearest generalisable result of the night, and the one that reaches the
other eighty-five names.

## What was measured

For every run committing both a volume series and its own price and cost, the
REALISED escalation of revenue per unit against cost per unit, on that company's
own filed accounts:

| name | class | window | revenue | cost | **cost drift** | margin |
|---|---|---|---:|---:|---:|---|
| TMGH | developer | 2011-2025, **14y** | +16.0%/yr | +15.5%/yr | **-0.37%/yr** | 0.235 → 0.274 |
| PHDC | developer | 2015-2023, 8y | +22.7%/yr | +23.5%/yr | **+0.61%/yr** | 0.350 → 0.318 |
| AMOC | refiner | FY2021-FY2025, 4y | +44.6%/yr | +46.0%/yr | **+0.97%/yr** | 0.102 → 0.066 |
| EGCH | fertiliser | FY2023-FY2025, 2y | +21.9%/yr | +30.1%/yr | +6.76%/yr | 0.459 → 0.384 |

**On the three windows long enough to mean anything — twenty-six name-years — the
cost drift is inside one per cent a year and it is NOT one-signed.** TMGH runs
-0.37%, PHDC +0.61%, AMOC +0.97%. Price and cost move together at whatever rate
the economy is running — 16% on a developer through the 2010s, 44.6% on a refiner
in the devaluation years — and the spread stays roughly where it was. It holds
across two classes and across a 14-year window that spans two devaluations.

A drift bounded within ±1% with mixed signs is what a genuinely flat spread looks
like. A one-signed drift of the same size would be a slow trend.

EGCH's figure is not evidence: two years, and its margin swings 0.459 → 0.327 →
0.384 inside the window, so the endpoint drift is a swing rather than a trend.
Recorded rather than counted.

TMGH's is read on TOTALS rather than per unit, because that run commits no volume
series — a weaker measurement, since a mix shift would show up in it, and the
instrument labels it rather than presenting it as the same thing. ARCC commits no
volume series either and is reported not measured, never clean.

## Why this is the error

Every defect found tonight is the same shape once this is on the table.

**AMOC needed 44.6% a year and the model used zero.** `brent_ratio()` returns
exactly 1.0 outside foresight, so both revenue and cost are frozen in pounds. The
realised requirement is now measured: 44.6% on the revenue side, 46.0% on the
cost side. The house PPP identity supplies about 11% a year, which is why F8 gets
the bias from -0.774 only to -0.443 and no further — **no currency rule this house
has is within a factor of four of what actually happened**, and that residual is
the width the far years should carry rather than a rule waiting to be found.

**PHDC pinned cost to consumer inflation at 15.2% a year while cost ran at
23.5%**, and its revenue arrived through the backlog release rather than through
the same escalator. One side on a path, the other on a different one. Its own
realised drift is +0.61%/yr, so a model holding the spread flat would have been
close to right.

**ARCC's seven fixes were all of this family** — coal on the currency rather than
frozen, the works price following the model's own cost stack, non-operating lines
scaling with revenue. Its clocks measure 1.03 and 0.92, the healthiest in the
book.

## What it says for the remaining names

The standing protocol already carries the rule — AMOC's own study registers "the
gross SPREAD per tonne is held flat in real terms", and the near-term-actual rule
says to hold everything else flat including observed improvements. **What this
adds is the measurement behind it**: on the two long windows available, the drift
is under 1% a year, so holding the spread flat is not a conservatism, it is what
the record shows.

It also says where the effort goes. **The escalation RATE is worth far more than
the spread.** AMOC's whole 0.52 log points of bias comes from using 0% where 44.6%
was needed; the spread over the same window moved 0.97% a year. A house spending
its effort on margin drivers and leaving the escalator frozen is optimising the
smaller quantity by two orders of magnitude.

## Which escalation rule gets closest

Read live: `python3 engine/valuation_calibration/escalation_rules.py`

If the rate is the thing that matters, the next question is which rule a study
could have followed at the origin. Four candidates, none of them a forecast and
none fitted: **freeze** (no escalation at all — what AMOC's model does), **cpi**
(the origin's last published consumer inflation), **ppp** (relative purchasing-
power parity on the CPI differential), **trail3** (the company's own trailing
three-year escalation of the line).

| name | cells | freeze | cpi | ppp | trail3 |
|---|---:|---:|---:|---:|---:|
| PHDC (per unit) | 12 | 0.346 | **0.264** | 0.281 | 0.346 |
| AMOC (per unit) | 1 | 0.236 | 0.035 | **0.010** | 0.177 |
| TMGH (totals) | 30 | 0.364 | — | — | **0.153** |

Mean absolute log error. **Freezing is the worst rule on every name that can be
measured**, and it is what one of these models actually does. Against the paired
cells: trail3 42% better than freezing, cpi 27%, ppp 23%.

**No rule is selected.** Choosing one because it scores best here is the
CRPS-selection mistake the promotion rule forbids. What this establishes is
narrower and firm: **freezing is ruled out**, on three names and three rules, and
AMOC's 0.52 log points of bias is what ruling it out is worth.

Two things this table is not. TMGH contributes 30 of the 43 cells and is measured
on TOTALS, so its escalation carries real volume growth — which flatters a
trailing rule, because a trailing rule extrapolates growth and the others do not.
And this does NOT reverse the earlier finding that trailing trend is the weakest
of the three pre-registered benchmarks: that pooled every driver, this scores only
the escalation rate of the revenue line. A rule can be poor in general and good
at one job, and saying which object is being scored is the whole of the
difference.

## What would overturn it

Three names is not a book. If further long windows come in above two per cent a
year, or if the drift turns out to differ systematically by class — the two
developers here run -0.37% and +0.61% and the one refiner +0.97%, which is no
separation at all on three names — then "hold the spread flat" is a class rule
rather than a house one and must be filed at the narrower scope.
Nothing here is registered as adopted; it is measured, and the register is where
a scope ruling would go.
