# The pooled bias is a manufactured margin expansion, and it is [L-048] in mirror image

**Measured 8 September 2026, under declaration 4.** Diagnostic only — nothing here changes
a declared run, a delivered study or a published fair value. It is written down because it
names what blocks the one gating test still failing.

## What was being chased

Two answers valued ARCC at roughly ten times its traded price — origin 2017 at +951% and
2023 at +982%. They survived a complete replacement of the terminal construction, so they
are not a terminal artefact. That negative result is what pointed at the projection.

## What the projection does

ARCC's forecast expands the operating margin at **every one of its eight origins, without
exception**, monotonically over five years:

| origin | year 1 → year 5 | fair value vs price |
|---|---|---|
| 2016 | 31.0% → 44.4% | +235% |
| 2017 | 22.3% → **55.7%** | **+951%** |
| 2018 | 15.0% → 28.9% | +237% |
| 2019 | 5.8% → 15.7% | +162% |
| 2020 | −1.5% → 5.2% | +100% |
| 2021 | 5.1% → 12.1% | +97% |
| 2022 | 20.1% → 37.8% | +279% |
| 2023 | 30.6% → **60.1%** | **+982%** |

Eight origins and eight expanding margins is not a forecast, it is a property of the
construction. **The overstatement tracks the terminal margin almost monotonically**, which
is what makes this the driver of the pooled bias rather than one more thing wrong.

The company's own filed operating margin over the same period runs 32.8, 28.0, 32.9, 18.3,
17.0, 10.0, 4.9, 10.2, 21.4, 24.3, 27.0 and 43.7 per cent — it swings **both ways**, which
no origin's forecast ever does.

## The mechanism, read off the code rather than inferred

`bottom_up.project()` escalates the revenue side at full domestic inflation — price at
`pi`, volume at population growth. On the cost side, at origin FY2023 over five years:

| line | multiplier |
|---|---|
| price, services, transport, overhead, G&A | **× 4.302** (full CPI) |
| coal half of raw materials | **× 1.000** — frozen |
| depreciation, amortisation, right-of-use | **× 1.000** — frozen |
| *the currency the same model carries* | *× 10.434* |

`_paths()` returns `coalm = 1.0` on the knowable path. Coal is a **dollar** commodity and
this is an **Egyptian pound** model, so freezing it in pounds through a 10.4× devaluation
is not a no-drift assumption — it is a large implicit real cost saving that compounds.
The defence in the code is that "a commodity price has no drift and assuming one would be
a forecast" — which is right about the *dollar* price and is being applied to the *pound*
cost. The model already carries its own currency path; the two were simply never joined.

Depreciation, amortisation and right-of-use are frozen outright, so a capital-intensive
plant's largest fixed cost stays nominally still while its revenue quadruples.

## The counterfactual, which confirms it by where it does *not* bite

Holding coal flat in **dollars** and converting at the model's own currency path — the
same no-drift assumption expressed in the right currency — gives final-year margins:

| origin | declared | coal in dollars | currency moved? |
|---|---|---|---|
| 2016 | 50.3% | 11.9% | yes |
| 2017 | 61.4% | −57.5% | yes, heavily |
| 2018 | 35.3% | 35.4% | no |
| 2019 | 22.3% | 28.8% | no |
| 2020 | 12.9% | 21.4% | no |
| 2021 | 18.7% | 19.7% | no |
| 2022 | 43.3% | 14.5% | yes |
| 2023 | 64.4% | 14.2% | yes |

**The two readings are nearly identical wherever the exchange rate was stable and diverge
enormously wherever it moved.** That is the signature of this defect and of no other, and
it is stronger evidence than the level of any single cell.

The counterfactual is **not proposed as the fix**: at 2017 it drives the margin to −57.5%,
which is an over-correction, because some of a coal cost increase does reach price. The
declared path assumes **zero** pass-through of the currency into the coal cost and the
counterfactual assumes **total** pass-through with none into price. The truth is between
them and neither end is a forecast anybody should ship.

## Why this is the house's own lesson arriving backwards

[L-048] and [R-MACRO-01] are written about escalating costs at domestic inflation while
holding the currency or the price still — "one event counted once and ignored once,
inflating every cost and freezing every price," and the forecast then reports the
manufactured margin **decline** as a finding. **This is the identical defect with the sign
reversed:** the event is counted on revenue and ignored on cost, and the forecast reports
a manufactured margin **expansion** as a valuation.

And the house has a gate for one direction only. [R-ANCHOR-01] catches a forecast opening
materially **below** the latest reviewed period, and its own text says it "does NOT fire on
a forecast ABOVE the latest period." Eight origins here forecast margins far above every
period the company ever filed, and nothing looked.

**The general lesson, which is not about cement:** a gate built from one incident inherits
that incident's direction. The first occurrence was a margin collapsing, so the rule was
written about collapse — and the same arithmetic running the other way had no owner for a
month. Where a rule fires on a sign, ask what happens at the other one.

## What is NOT done here

ARCC's projection is that run's own pre-registered method and its walk-forward scored its
drivers against it. Changing it moves that run's committed results and is not done in
passing or on this evidence alone. What this file establishes is the diagnosis; the
remedy — a pass-through assumption for a foreign-currency input, and the mirror clause on
[R-ANCHOR-01] — is a decision recorded separately.
