# THE OVERRIDING AIM (user, standing — supersedes every mechanic below)

> **Better drift prediction and smaller cone size, without compromising accuracy.
> If accuracy is compromised, stick to the time span that offers the best results.**

Everything else in this document is machinery for serving that sentence. Where a
mechanic and the aim disagree, the aim wins and the mechanic gets fixed.

Read carefully, the aim contains its own guard. "Smaller cone" and "without
compromising accuracy" are a PAIR, and the second half is not decoration — a
narrower cone bought with coverage is not progress, it is the same forecast with
the uncertainty hidden. So the test for any candidate is both halves at once:

  does it narrow the cone?   AND   does coverage / calibration hold?

If yes to both, adopt (subject to the 0.5% floor). If it narrows the cone but
coverage slips, REJECT — that is the compromise the aim forbids. If it neither
narrows nor improves, keep whatever span performs best, which is usually simply
the one already in production.

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

---

# First application — all six markets, 28-Jul-2026

Run at the 15-year ingest of KR, IN, QA, US and metals, on the 3-month horizon,
every candidate scored on identical origins against the same carry-anchored
benchmark.

| market | names | best candidate | paired vs unlimited, blocks {2,3,4} | jackknife flips | width move | decision |
|---|---|---|---|---|---|---|
| EG | 30 | 7 yr | PASS / PASS / **PARITY** — block-dependent | 0/30 | −0.43% | **no change** |
| AE | 18 | 3 yr | ROBUST PARITY | 1/18 | −1.79% | **no change** |
| SA | 11 | 5 yr | ROBUST PARITY | 0/11 | +0.72% | **no change** |
| KR | 3 | 3 yr | ROBUST PARITY | 1/3 (SAMSUNG) | −0.50% | **no change** |
| IN | 3 | *unlimited* | 7 yr is a ROBUST **FAIL** vs unlimited | 3/3 | −0.54% | **no change** |
| US | 3 | *unlimited* | ROBUST PARITY | 1/3 | +1.12% | **no change** |

**Six markets, six nulls. In none of them does a shorter span clear the guard.**

EG is the closest call and is instructive: 7 years leads on point skill and the
paired CI clears zero at two of three block sizes — but not the third. Under the
standing robustness rule that is BOUNDARY, not a pass, and it is exactly the
block-dependent sign flip the rule exists to catch. It would also have moved the
cone by 0.43%, an order of magnitude inside the materiality gate.

India is the clearest result in the other direction: truncation is *monotonically*
worse on both skill and `std_u` (1.039 unlimited → 1.078 at 3 years, further from
the ideal 1.0), and a 7-year window is a **robust FAIL** against the full history.
There, the extra decade is actively earning its place.

## What this says about the original question

The premise behind the rule — that a longer library widens the cone or degrades
the forecast — **is not supported in any market tested.** Every span-driven width
move above is under 2%, in both directions. History length is simply not the
lever that controls cone width.

The levers that do control it, in the order they mattered on 28-Jul-2026:

1. **which engine vintage struck the published cone** — legacy cones implied
   1.6–2.1× the volatility the current chain estimates;
2. **the fitted (ν, width_cal)** for the market;
3. **the volatility state at the anchor date**;
4. history length — a rounding error by comparison.

The rule stays in force regardless. It is cheap to run, it is the only way to know
rather than assume, and a null is a real result: it says the data we hold is not
costing us anything. Re-run it at every ingest, and record the nulls too.


---

# Adoption floor — 0.5% (user, 28-Jul-2026)

Amends the materiality rule. Two thresholds, and they do different jobs:

| move in the published 90% cone (or the drift) | action |
|---|---|
| **< 0.5%** | noise — leave the live cone alone |
| **0.5% – 5%** | **apply it** |
| **> 5%** | apply it, but via PR so a human sees it first |

The 0.5% floor replaces the previous habit of recording a real result and then
declining to act on it because it was "immaterial". If a change is established
and moves the cone by more than half a percent, it ships.

**This does not loosen the statistical guard.** Materiality decides whether a
change worth making is worth shipping. It never rescues a change that was never
established. Every history-span candidate rejected on 28-Jul-2026 failed
*upstream* of materiality — on a block-dependent CI, a jackknife flip, or simply
losing to the full history — so lowering the floor from 5% to 0.5% resurrects
none of them.

It does re-open exactly one prior decision: the **EG 15-year calibration sample**
(26-Jul-2026). It was measured at −0.65%, it cleared bootstrap-block robustness
AND a 30-name jackknife, and it was declined *solely* on immateriality. Under a
0.5% floor that reasoning no longer stands. Re-opening it still requires
re-running the devaluation-window coverage column on patched data first — skill
did not decide that break cut originally and must not decide it now.
