# The valuation calibration — pre-registration

**3 September 2026.** Written and committed BEFORE any score exists, and hashed,
so that the claim "no lever was fitted to the gap" is a fact about the commit
order rather than an assurance. `scripts/check_valuation_calibration.py` asserts
that this file's commit precedes every score file it finds; if it does not, the
calibration is not evidence and the gate says so.

---

## The question

The principal's test, in their words: *does calibration bring the fair value
closer to the actual price?*

No fair value this house has published has ever been graded against what
happened. The price-engine cones are graded — that is the band record, and it is
broad. The statement walk-forward is graded — that is five names and it measures
drivers, not values. Between them sits the thing the house actually publishes,
and it has no instrument at all.

This document fixes the instrument before it is built.

## What is being graded

At each year-end origin from **2013 to 2023**, the house fair value is rebuilt
using point-in-time information only, and compared with the price at that origin
and with what the price did afterwards.

**Point-in-time is absolute.** Each origin sees only what was published by that
date: statements as originally reported, the sovereign curve and CPI print and
policy rate of that month, the ERP vintage of that year. A restatement is noted
beside, never substituted. Where a vintage cannot be sourced, **the origin is
dropped and the window shortened — never interpolated.** A fabricated input
corrupts the very error it is scored on.

## The two scores, and why there are two

A fair value struck today is **not** a forecast of the price in three years, and
grading it as one is mis-specified. At a 27–37% cost of equity, a fair value that
agrees perfectly with the price at *t* should sit 15–30 log points BELOW the
price at *t+1* purely by construction — the value compounds at the discount rate
and the comparison does not. A raw `log(FV_t / P_{t+h})` with a zero-bias
acceptance would therefore condemn a perfectly calibrated method.

Two series are pre-registered instead:

**(i) CONTEMPORANEOUS AGREEMENT** — `log(FV_t / P_t)` at every origin. This is
the direct measure of the house lean, and it is the number the whole reassessment
is about. Zero means the house agrees with the market on average; negative means
systematically pessimistic, which is the hypothesis under test.

**(ii) GAP CLOSURE** — whether `log(FV_t / P_t)` predicts the subsequent one-,
two- and three-year total return **net of carry**. This is the measure of whether
the lean is *information*. A house can be systematically pessimistic and right;
it can also be systematically pessimistic and merely wrong. Only this series
separates them.

The two answer different questions and neither substitutes for the other. A
method could score well on (i) and badly on (ii) — agreeing with the market on
average while carrying no information about where it goes next — and that is a
real and interesting outcome, not a contradiction.

## Statistics, fixed here

- **Bias, MAE, sign**, per origin and pooled.
- **Block bootstrap** over origins, blocks {2, 3, 4}, **seed 42** — the house
  robustness bar, unchanged.
- **Era split**: pre-2016, 2016–2021 (post-float), 2022–2024 (devaluation). The
  same eras the statement walk-forward uses, so the two records are comparable.
- **Leave-one-name-out** across the panel.
- **The effective independent n is printed beside the cell count.** Eleven
  origins across a panel of names is not 11 × N independent observations: the
  origins share a market and the names share a year. The effective n is about the
  origin count, and every interval is read against that number rather than the
  cell count. A record that quotes the cell count alone overstates its own
  precision, which is the failure this line exists to prevent.

## Two fair-value series, because one cannot be both

**(a) MECHANICAL** — rebuilt at every origin from drivers the statement
walk-forward produces, with no judgement. This is the series the promotion rule
reads, because it is the only one that exists at every origin.

**(b) AS-DELIVERED** — the fair values this house actually published, from
`engine/fv_vintages.json`. This exists only from 2025 and is far too short to
score, and it is carried anyway as the honest check on whether (a) resembles what
the house really does. Where they diverge, the divergence is reported and the
mechanical series is NOT adjusted toward the delivered one.

## Population

- **FULL** on the names with parsed statements: AMOC, ARCC, EGCH, PHDC, TMGH, and
  each name the campaign adds thereafter.
- **LIGHT** on further EGX names with at least ten years of prices, using a fixed
  point-in-time proxy model declared in `panel.py` before it is run. A proxy is
  **declared as a proxy** wherever its number appears and is never dressed as the
  full method.

## Promotion — sequential, ordered, with a stop rule

Levers are evaluated **one at a time on the current stack**, in this order,
written here before any score exists:

1. the cost-of-capital glide
2. the terminal anchors
3. the equity-risk-premium basis
4. the country-premium lambda
5. beta shrinkage
6. the lens set

A lever is promoted **only while the stacked pooled contemporaneous bias moves
toward zero without crossing it by more than the bootstrap half-width**, and
promotion **stops the moment it would**. This replaces any per-lever "improves on
three of four names" rule, which can stack five individually-justified moves into
an overshoot — five corrections each right on its own, wrong together, which is
exactly the failure mode the whole reassessment was called to fix.

**The guard is symmetric: a positive bias is a finding exactly as a negative one
is.** A house that corrects its pessimism into optimism has not fixed anything.

## What this is not

- **Not an input to any study.** No study reads this record, at any origin.
- **Not a way to fit fair values to prices.** The promotion bar is out-of-sample
  and cross-name. The CRPS-selection precedent applies in full: a lever that
  looks better in sample and loses under leave-one-out is rejected, however
  sensible it sounds.
- **Not a licence to move a delivered number.** A promoted lever changes the
  method; delivered studies change only at their next edition, through the
  ordinary path.

## What would overturn the whole exercise

If the mechanical series (a) turns out not to resemble the as-delivered series
(b) once (b) is long enough to compare — say, a pooled divergence wider than the
bootstrap interval on (a) — then this calibration is grading a method the house
does not actually use, and its promotions must be withdrawn. That condition is
written here, in advance, because a test with no stated falsifier is a habit.

---

*Nothing in this document may be edited after its commit. A correction is a new
dated pre-registration that supersedes it and says so, and the gate reads the
commit dates.*
