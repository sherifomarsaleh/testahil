# Criterion 2's decisive cell, priced

**07-09-2026.** Part E criterion 2 asks that each study's forward drivers sit inside that
name's own walk-forward band, **or that the exception be priced**. Eleven cells sit outside.
Ten rest on fewer than nine observations; **one rests on a figure its own run calls a
percentile**, and that is the one priced here.

    EGCH   cost_of_sales   h=5   band [0.1447, 0.8456]   point 1.0   n=9   width 5.84x
           basis: "p10-p90 of the full record, widened by the KIMA-2-era bias +/- MAE
                   band where that is wider"     orientation: forecast over actual

Forecast-over-actual, so the record says the outturn ran **1.183x to 6.909x** the forecast,
and the study applies no correction.

## Method

A full re-run of the study's own model through `compute.run_case()` with one quantity moved
— the same discipline `egch_study/alternatives.py` uses, never a hand-adjusted rate. The
model assembles cost of sales at a single point (`cogs = gas_cost + other_mat + wages +
services + dep`); a per-forecast-year multiplier was applied **there**, in a sandbox copy of
the tree, because that is exactly the line the walk-forward scored. **Nothing in the
delivered study was touched.**

The baseline reproduces both published branches before any override is believed:
`base 4.0396` and `halt 8.0388` against the study's committed `central_two_sided`.

## The price

| year-5 cost of sales | base branch | halt branch |
|---|---|---|
| x1.000 — as published | **EGP 4.0396** | **EGP 8.0388** |
| x1.183 — the NEAR band edge | **EGP 1.5902  (−60.6%)** | EGP 5.5949 (−30.4%) |
| x1.301 | EGP 0.0242 — **equity reaches zero** | |
| x1.400 | EGP −1.3143 | |
| x1.500 and beyond | **REFUSED** | |
| x6.909 — the FAR band edge | **REFUSED** | |

Applying the near edge to all five forecast years rather than year five alone takes the base
branch to **EGP 0.3204 (−92.1%)**.

The refusal is the sanctioned terminal module's own, verbatim: *terminal free cash flow is
−37,449.3, not positive: a going concern that consumes cash for ever is not a terminal, it
is a liquidation, and it must be valued as one.*

## What this says, and it is about the criterion rather than about EGCH

**The band cannot be priced end to end, because most of it lies outside the domain where the
model exists.** Equity reaches zero at 1.30x and the model stops returning a number at all by
1.50x, while the band runs to 6.91x. Roughly **88% of the band's width sits beyond the point
where this study can produce a valuation**, and all of it beyond zero equity.

So for this cell, "price the exception" has no end-to-end answer. What *is* answerable, and
is answered above, is the **near edge**: the smallest departure the record admits is already
worth −60.6% of the base branch.

Three things follow, and none of them is a verdict on the study:

1. **The near edge is priceable and large.** Criterion 2 can be satisfied for this cell by
   pricing that edge, which is now done.
2. **A band six times as wide as its own point is not an interval a forward driver can be
   held inside**, and calling it a p10–p90 does not change what nine observations support.
   This is the same conclusion the record-length measurement reached from the other
   direction, arriving here as a hard refusal instead of a statistic.
3. **The criterion does not say what to do when a band edge is unevaluable.** That is a rule
   question, registered rather than answered here.

## Reproduce

Sandbox a copy of `engine/`, add a per-year multiplier on the assembled `cogs` line in
`egch_study/compute.py`, and re-run `compute.run_case('base')`. The baseline must reproduce
`4.0396` / `8.0388` first, or nothing below it means anything.
