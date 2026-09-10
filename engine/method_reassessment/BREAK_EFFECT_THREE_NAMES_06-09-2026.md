# The break effect holds on three names. The "house lean" does not.

**6 September 2026, 19:35.** A correction to what was reported at 18:00, found by
reading a file that was there all along.

## PHDC does commit per-cell errors, in a shape the scan did not recognise

The 18:00 report said *"three of five runs commit no per-cell error list — AMOC, EGCH
and PHDC"*. **PHDC commits one.** `engine/phdc_walkforward/error_cells.json`, 303KB,
written by that run's own `score.py`. It is keyed as a dict of four settings, with
`field` and `e` where TMGH writes `driver` and `log_error`, so a scan looking for
TMGH's key names read it as absent. That is the same shape-mismatch failure that has
now cost four separate readings today, and it is the reason the reading below was
delayed rather than the reason it is different.

## Three names, and the third one disagrees about the level

| | ARCC | TMGH | **PHDC** |
|---|---|---|---|
| every origin | −0.278 | −0.280 | **+0.144** |
| origins 2020–2022 | −0.695 | −0.692 | −0.257 |
| every other origin | +0.108 | −0.041 | **+0.292** |
| **the break, relative to the rest** | **−0.803** | **−0.651** | **−0.549** |

**What survives on all three is the BREAK EFFECT.** Forecasts struck from the
2020–2022 origins come in **0.55 to 0.80 log points lower** against actual than
forecasts struck from any other origin — the same direction and the same order of
magnitude on three companies in two different sectors.

**What does NOT survive is the level.** ARCC and TMGH sit close to unbiased outside
the break. **PHDC over-forecasts by 25% there**, and is 13% over-forecast pooled
across every origin. Two names lean low; one leans high.

## What that changes

The 18:00 report said the 32% under-forecast *"is not systematic, it is three
origins, and outside them the method is unbiased"*. **The first half stands and the
second does not.**

- **The break effect is real, consistent and now measured on three names.** It is the
  largest single component of the pooled error and it is not a modelling defect: no
  rule available at those origins saw a devaluation, a quota change and an export
  market opening.
- **There is no single house lean to correct.** Outside the break the three names run
  +11%, −4% and +29%. That is heterogeneity, not a bias — and [R-FCAL-01] is explicit
  that a driver whose bias changes sign is REPORTED and never corrected for, because
  the average of two opposite regimes was true in neither.
- **It also lands where it should.** PHDC is the name whose published central sits
  **+23.9% above the market**, and it is the name that over-forecasts its own history.
  Those are the same fact seen twice.

## Still unread

AMOC, EGCH and ARCC write no per-cell file at all. AMOC and EGCH *build* the rows —
`build_cells()` in each `score.py` returns them with origin, horizon and per-driver
log error — and then aggregate them away without writing them. ARCC's were computed
directly off the model for this audit and never persisted. Three runs, one line of
JSON each.
