# Two thirds of the driver biases are not biases

Read live: `python3 engine/valuation_calibration/boundary_sensitivity.py`

[R-FCAL-01] permits a correction only where a bias **holds its sign across eras**,
and says in terms that a bias which changes sign between eras is not a bias —
report the instability, never correct for it. Every stability claim in this book
has been made at **one** boundary, chosen for the market: the year its currency
moved.

## That boundary is not every driver's break, and assuming it is cost a conclusion

TMGH's depreciation reads **-0.397 before 2023 and -0.342 after** — exactly the
shape a correctable bias has — and an hour ago I wrote it up as the one
correctable driver in that run. Its own break is a year later: realised
depreciation over property, plant and equipment rose 0.0378 to 0.0761 from 2017
to 2023 and then **collapsed to 0.0141** as the asset base jumped elevenfold in
2024. Cut at each year the data admits:

| cut | before | after |
|---|---:|---:|
| 2021 | -0.463 | -0.346 |
| 2022 | -0.430 | -0.339 |
| 2023 | -0.397 | -0.342 |
| 2024 | -0.393 | -0.322 |
| **2025** | **-0.516** | **+0.364** |

**It flips.** The conclusion was withdrawn within the hour it was written.

## Run over the book, most drivers do this

Every driver with at least five cells either side of a cut, at every cut the data
admits:

- **42 drivers flip sign at some cut point.** Under [R-FCAL-01] not one of them
  is a bias.
- **24 survive every cut** — among them TMGH's total revenue (-0.310 to -0.002),
  its development revenue and cost, EGCH's cost of sales and administrative
  expense, PHDC's new sales and finance cost, and ARCC's volume and manufacturing
  depreciation.
- 22 more have too few cells to cut at all, reported rather than counted as
  stable.

**Nearly two thirds of the testable drivers have a bias whose sign depends on
where somebody drew the line.** ARCC's gross profit runs +1.578 / -0.909 at a
2022 cut and -0.084 / -1.225 at a 2025 one; its interest income runs +1.116 /
-2.512 and then -1.191 / -3.443.

## What this does and does not say

It does **not** choose a boundary, and it must not. Picking the cut that makes a
bias look stable is the selection this method forbids, and picking the one that
makes it look unstable is the same offence facing the other way. Every cut is
reported and the pattern is left to speak.

It does **not** say a sign-stable driver is correctable — that needs
[R-FCAL-01]'s whole procedure, of which the sign clause is one part.

What it does say is that **the sign clause has been tested at one point per market
and passes far less often when tested properly**, and that any correction adopted
on a boundary-sensitive bias is fitted to where a line was drawn rather than to
anything about the company.

## Why this matters more than the drivers

The reassessment's premise was itself an era claim: a systematic house lean,
measured pooled and then split at the devaluation. Both the break effect and the
spread result were measured at boundaries chosen for the market. **The break
effect survives its own boundary test** — new sales and PPE are robust at every
cut, and the target-side cut used earlier is a calendar fact rather than a chosen
line. What has not been re-tested this way is every per-driver stability claim in
the five runs' own records, and this instrument is what tests them.
