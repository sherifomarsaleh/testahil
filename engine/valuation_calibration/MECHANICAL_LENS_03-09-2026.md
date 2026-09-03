# The mechanical fair value — declared before any of it is computed

**3 September 2026.** The pre-registration of the same date fixes the SCORES. It
deliberately does not fix the *form* of series (a), the mechanical fair value,
beyond saying it is "rebuilt at every origin from drivers the statement
walk-forward produces, with no judgement". This document fixes that form, and it
is committed **before a single value is computed**, for the same reason the
pre-registration was: a construction chosen after seeing what it produces is not a
construction, it is a result.

---

## What it is, and what it is not

**It is not the house method.** The delivered studies value a developer on a
cash-flow model with an RNAV cross-check, a bridge, a lens table and a dozen
judgements. None of that can be rebuilt at a past origin without a person, and a
person at a past origin is the thing this exercise exists to remove.

**It is a fixed, mechanical construction applied identically at every origin and
to every name**, so that the *movement* of `log(FV/P)` across origins is a
property of the method rather than of who was looking. Its absolute level carries
much less information than its behaviour across origins, and the report says so
wherever it prints a level.

The pre-registration already carries the falsifier this raises: *if the mechanical
series turns out not to resemble the as-delivered one once the delivered record is
long enough to compare, this calibration is grading a method the house does not
use and its promotions must be withdrawn.*

## The construction

At origin *t*, for a name whose walk-forward projects net profit attributable to
the parent:

1. **Drivers.** The walk-forward's own projection at *t*, `as_known` — the
   inflation path a forecaster could have used at that origin, never the realised
   one. Horizons 1 to 5. No correction, no judgement, no adjustment of any kind.
2. **Discount rate.** The cost of equity from the point-in-time macro archive at
   *t*:
   `Ke = (sovereign_10y − default_spread) + beta × ERP`
   — the sovereign yield and the default spread of that vintage, the equity risk
   premium published at that origin, and **beta fixed at 1.00 for every name and
   every origin**. Beta is fixed rather than regressed on purpose: a rolling
   regression is a second moving part whose own history would need its own
   point-in-time discipline, and a lens whose level is not the claim does not earn
   it. The choice is stated here so it cannot be tuned later.
3. **Terminal.** After horizon 5, a perpetuity at the point-in-time terminal
   growth: the archive's own inflation forecast for the last projected year, plus
   a real growth of **zero**. Where `Ke − g` is not positive the origin is
   **dropped**, not floored.
4. **Value.** Discount the five projected profits and the terminal at Ke, divide
   by the shares outstanding as reported at *t*.
5. **Compare.** Against the last close on or before 31 December of *t*, from the
   persistent OHLC library.

## Fixed here, never fitted

- beta = 1.00, every name, every origin
- real terminal growth = 0.0
- horizons 1–5, the walk-forward's own
- macro mode = `as_known`, never `foresight`
- no correction factors, no bias adjustment, no smoothing
- an origin missing any input is **dropped and the window shortened**

## What would make this the wrong instrument

- If the mechanical series does not resemble the as-delivered one (the
  pre-registration's own falsifier).
- If the level is quoted as though it were a house fair value. It is not, and the
  report is written to make that hard to do by accident.
- If `Ke − g` turns negative often enough that dropping those origins selects the
  sample. The report prints the drop count for exactly this reason.

---

*Committed before any value was computed. A later change to this construction is a
new dated declaration that supersedes this one and says so; this file is never
edited.*
