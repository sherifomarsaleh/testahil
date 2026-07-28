# History-span rule — history is instrumental, and must earn its place

**Adopted 28-Jul-2026 (user directive).** Amends the Standing Research Protocol.

## The rule

History is kept for exactly two purposes: **a tighter cone and a better-centred
drift, at unchanged accuracy.** A longer library is not a virtue and is never
assumed to be better for being longer. It is a hypothesis, and it goes through
the same out-of-sample promotion rule as every other engine parameter.

Where a shorter span demonstrably produces a better forecast, the engine uses
the shorter span. Where accuracy would be compromised, the engine keeps
whatever span performs best — length is never the tie-breaker, performance is.

## What is NOT done

**The raw library is never truncated.** `engine/raw_ohlc/` stays complete.
Three other subsystems read it and would silently degrade if rows were deleted:

- `horizons.py` builds each exchange's trading calendar from it, and the
  seasonal leg of the h-projection needs years of prior anchors to capture
  Eid / Ramadan / Seollal / Golden Week clustering;
- the calibration panels score against it;
- grading reads the actual sessions from it.

Span is therefore a **fitted parameter**, not a deletion. Excluded history stays
on disk, unused by the fit and instantly recoverable if a later re-fit says
otherwise. Deleting it would be a one-way door justified by a marginal result.

## Two levers, never conflated

| lever | what it controls | governed by |
|---|---|---|
| **calibration sample** | which windows train (ν, width_cal) | `breaks` + `apply_breaks` |
| **HAR lookback** | how much past each per-origin variance forecast may see | `history_span.py` |

These are different questions with different answers and must be tested
separately. The second is what actually sets the width of a cone struck today,
and until 28-Jul-2026 it had never been tested at all.

The lookback is a **rolling trailing window**, not a fixed start date. A fixed
start is a break filter and it silently lengthens as the calendar advances —
"2011+" means 5 years of lookback in 2016 and 15 in 2026, so it can never be a
stationary answer to "how much past should the model weigh".

## Selection criterion

**CRPS, out-of-sample.** Not "narrowest wins". Narrowness alone is trivially
gamed — halve every cone and sharpness improves right up until coverage
collapses. CRPS is a *proper* scoring rule: it is already, by construction,
sharpness subject to calibration, and it cannot be improved by a cone that is
narrow in the wrong place. Mean 90% width, coverage and PIT are reported
alongside as diagnostics, never as the criterion.

Every candidate is scored on **identical origins** against the **same**
carry-anchored benchmark. Only the HAR training set differs.

## The guard — five conditions, all required

Selecting a span by maximising a score is the same class of move that was
already **REJECTED** here: choosing (ν, width_cal) by CRPS grid search beat MLE
in-sample and lost under LONO. So a span change is adopted only if:

1. scored held-out / cross-fitted, never in-sample;
2. the winner holds across bootstrap block sizes {2, 3, 4};
3. a drop-one-name jackknife does not flip it;
4. 80/90% coverage and PIT centring do not degrade;
5. it clears the 5% materiality gate to move a live cone.

**A candidate that wins on skill while coverage falls is REJECTED** — that is
buying narrowness with accuracy, the one trade this rule forbids.

A result that is real but immaterial does not move a live cone (precedent: the
EG 15-year calibration sample, 26-Jul-2026 — it won robustly and moved the
published cone by 0.65%, and was correctly not adopted).

## Standing application

Run the span test on **every market, at every library ingest**, and record the
verdict — including the nulls. A null is a result: it says the current span is
already the best available and the extra history costs nothing.
