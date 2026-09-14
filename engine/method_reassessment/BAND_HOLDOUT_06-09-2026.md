# The far-year ranges do not hold, and they fail worst where they are used

Read live: `python3 engine/valuation_calibration/band_holdout.py`

[R-FCAL-01] requires every study carrying a fundamental walk-forward to publish
years three to five as RANGES from that record's own driver-error distribution
rather than as points. All five runs do — checked, and that clause is honoured
across the book. **Nothing had ever tested whether the ranges hold.**

## Two tests that cannot answer it, and one that can

**In-sample is hopeless.** Every run states its band as the observed span of the
very cells the band is built from, so coverage is 100% by construction.

**Leave-one-origin-out measures nothing, and that is not obvious.** It is the
discipline this repository applies to every fitted parameter, and it was the
first draft of this instrument. For a group of k+1 origins each contributing one
cell, the held-out value falls inside the min-max of the other k exactly when it
is not the overall minimum or maximum — so across all k+1 hold-outs exactly two
fail, **every time, whatever the data**. Coverage is (k-1)/(k+1) by arithmetic.
It was caught only because the benchmark was computed rather than typed: observed
and expected agreed to the last decimal place on five names and five horizons,
which is five rows too clean to be a measurement.

**The test that works matches how a band is used.** At each origin the band is
built from the origins strictly BEFORE it, and the next outturn is asked whether
it lands inside. Time-ordering breaks the symmetry that made leave-one-out an
identity, and it is the only honest question anyway: a study published in 2022
could not have used 2024's error to set its band.

The null is the same formula and is now a real null — under exchangeability a
fresh draw falls inside the min-max span of k previous draws with probability
(k-1)/(k+1), computed per cell on that cell's own k. **It is not 90%**, and
reading it as 90% is the mistake this guards against: a span of four observations
is not a 90% interval however a document labels it.

## The result

| name | n | inside | coverage | expected | skill | p | below | above |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| AMOC | 7 | 4 | 57.1% | 50.0% | +7.1pp | 1.000 | 0 | 3 |
| ARCC | 40 | 30 | 75.0% | 56.9% | **+18.1pp** | 0.024 | 10 | 0 |
| EGCH | 115 | 62 | 53.9% | 67.6% | **-13.6pp** | 0.003 | 35 | 18 |
| PHDC | 20 | 4 | 20.0% | 62.9% | **-42.9pp** | 0.000 | 13 | 3 |
| TMGH | 77 | 44 | 57.1% | 62.4% | -5.3pp | 0.348 | 29 | 4 |

**Pooled: 259 tested, 55.6% against an expected 63.5%, -7.9pp, p=0.010.**
Of 115 misses, **87 fall BELOW the band** — the outturn beat the projection by
more than the band allowed. 284 further cells are untestable for want of three
prior origins, counted rather than dropped quietly.

### It degrades with the horizon, monotonically

| h | n | coverage | expected | skill | below | above |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 84 | 63.1% | 65.0% | -1.9pp | 18 | 13 |
| 2 | 64 | 59.4% | 64.7% | -5.3pp | 20 | 6 |
| 3 | 51 | 58.8% | 62.6% | -3.8pp | 17 | 4 |
| 4 | 36 | 44.4% | 61.3% | -16.8pp | 16 | 4 |
| 5 | 24 | **29.2%** | 60.9% | **-31.7pp** | 16 | 1 |

**At five years the published range catches under a third of outcomes, and
sixteen of its seventeen misses are on the low side.** Years three to five are
exactly where [R-FCAL-01] mandates ranges *because* points are unreliable there —
and the ranges are unreliable there too, in the same direction.

## It is not the break effect in a new costume

A band needs prior origins, so only the later origins are testable, and on an
Egyptian book the later origins are disproportionately the ones whose windows ran
into the devaluations. A pooled failure could therefore be the band being too
narrow, or simply the break effect arriving in a new instrument. Split:

| | n | coverage | expected | skill | below | above |
|---|---:|---:|---:|---:|---:|---:|
| devaluation years | 188 | 58.5% | 65.1% | -6.6pp | 72 | 6 |
| other years | 71 | 47.9% | 59.3% | -11.4pp | 15 | 22 |

**The bands under-cover in both regimes**, and outside the devaluation years they
under-cover MORE. The direction of the miss flips — 72 of 78 misses below inside
the break, 22 of 37 above outside it — so the break effect is a lean on top of a
band that is simply too narrow in both directions.

## What follows

1. **The ranges published in years three to five understate the uncertainty**,
   and a study saying "this is the method's own measured error at this horizon"
   is making a claim this measurement does not support. The honest number is
   wider than the observed span of four to eight origins.
2. **A min-max span of a handful of observations is not an interval.** Its
   nominal coverage is (k-1)/(k+1), around 60-70% here, and the studies present
   it without saying so. That is fixable in words today, before any question of
   widening it: state the count and what a span of that count can mean.
3. **ARCC is the exception and it is worth understanding**, at +18.1pp on 40
   cells with every one of its ten misses below the band. Its bands are wide
   because its early origins were volatile; whether that is a property of cement
   or of its origin window is not answerable on one name.
4. Widening the bands is NOT done here. A widening factor chosen to make this
   table pass is the free parameter the promotion rule forbids, and it would be
   fitted to 259 cells across five correlated Egyptian names in one regime.
   What this establishes is that the current bands fail, out of sample, with a
   p-value — which is what a widening would have to be justified against.
