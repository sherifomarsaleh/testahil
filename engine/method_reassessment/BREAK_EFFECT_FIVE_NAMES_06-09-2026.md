# The break effect, on all five names

Read live: `python3 engine/valuation_calibration/break_effect.py`

## What this replaces

The 06-09-2026 three-name note cut the errors by a TYPED range of origin years
(2020-2022) on the three runs that then committed per-cell errors. Two things
have changed since, and both change the answer:

1. **AMOC, EGCH and ARCC now write `error_cells.json`.** All three already BUILT
   the rows and aggregated them away without writing them; ARCC's were computed
   off the model for that note and never persisted. Three runs, one dump each.
   The scores those runs publish are unchanged -- the dump adds a file, it moves
   no number.

2. **The cut is no longer a typed year range.** Two cuts are run instead, because
   the typed one silently conflated two different questions:

   - the **ORIGIN-side** cut, on each run's own declared era label, asking WHAT
     THE ANALYST KNEW when the forecast was made;
   - the **TARGET-side** cut, on the calendar year being forecast, asking WHAT
     HIT THE WINDOW.

   They disagree, and the disagreement is not noise. ARCC's own pre-registration
   labels its FY2020 and FY2021 origins "E1 pre-2022" -- correctly, since nothing
   about the devaluation was knowable then -- while those origins' five-year
   windows ran straight through all of it. On the origin cut ARCC's effect is
   +0.392; on the target cut it is -2.215. Neither is a correction of the other.

## The result — target-side cut, mean log error

Devaluation years: FY2022, FY2023, FY2024, FY2025.

| name | family | n | in deval | outside | effect |
|---|---|---:|---:|---:|---:|
| AMOC | all | 63 | -0.774 | — | no contrast |
| ARCC | all | 90 | -0.798 | **+1.417** | -2.215 |
| | revenue | 25 | -0.484 | +0.376 | -0.860 |
| | profit | 40 | -0.912 | +2.297 | -3.209 |
| EGCH | all | 190 | -1.295 | -0.172 | -1.123 |
| | revenue | 55 | -1.460 | -0.102 | -1.359 |
| | cost | 55 | -0.973 | -0.223 | -0.750 |
| | profit | 46 | -1.755 | -0.428 | -1.327 |
| PHDC | all | 35 | -0.849 | -0.009 | -0.840 |
| TMGH | all | 197 | -0.485 | -0.031 | -0.454 |
| | revenue | 68 | -0.726 | -0.149 | -0.577 |
| | profit | 34 | -0.094 | +0.544 | -0.638 |

**Eleven of eleven family-level effects carry the same sign**, on four names,
spanning 0.45 to 3.2 log points. Every one says the same thing: the method
under-forecasts the level in the devaluation years and does not, or does so
much less, outside them.

**Outside the devaluation years the residual is small on three of the four
names** — EGCH -0.172, PHDC -0.009, TMGH -0.031 — and strongly positive on
ARCC at +1.417 across 18 cells.

## What this does to the reassessment's founding premise

The premise was a systematic house lean of roughly -45% on revenue and cost,
diagnosed as a compounding rate error and answered by [R-TERM-01]. That
diagnosis rested on the pooled figure. Split by what the window ran into, the
pooled figure is a devaluation effect plus a small and inconsistently-signed
residual. On these five names:

- **there is no evidence of a uniform house lean outside the devaluation years**;
- **there is strong, consistent evidence of one inside them**;
- **the residual outside them changes sign between names** (+1.417 on ARCC
  against -0.172 on EGCH), which under [R-FCAL-01] is instability to be
  reported, never corrected for.

This does not retire [R-TERM-01]. That rule was adopted on an arithmetic
argument about the terminal — the implied asset life being the reciprocal of the
inflation rate — which stands on its own and was never a fit to the pooled bias.
What it does retire is the pooled figure as EVIDENCE FOR a general correction:
a correction fitted to -0.45 would be fitted to an average of two regimes, and
[R-FCAL-01] already says the average of two opposite regimes was true in neither.

## Three things this deliberately does not claim

**AMOC is not a null result.** Every one of AMOC's targets falls in a
devaluation year, so it has no outside-the-break side at all. The instrument
prints that in words rather than showing a blank effect column that reads as
nothing found.

**The pooled LEVELS are not comparable across names.** Each run scores its own
driver list and the intersection is not the same mix name to name — PHDC
contributes one revenue line where TMGH contributes six drivers including two
balance-sheet items. What is comparable is the within-name effect, which holds
the mix fixed by construction, and the per-family rows, which hold it fixed by
selection. The first draft of this instrument pooled the levels across names and
that number was about the mixes.

**The devaluation is a proxy, not a mechanism.** These cells say the errors
concentrate on the years the currency moved; they do not say which driver rule
carried the error there. The seven ARCC fixes are the only place that has been
worked out line by line so far.

## Does it compound? Yes to h=3, then it splits

Inside the devaluation years, mean log error by horizon:

| name | h=1 | h=2 | h=3 | h=4 | h=5 |
|---|---:|---:|---:|---:|---:|
| AMOC | -0.536 | -0.924 | -1.023 | — | — |
| ARCC | -0.239 | -0.589 | -0.959 | -1.191 | -1.075 |
| EGCH | -0.510 | -1.119 | -1.311 | -1.764 | -2.114 |
| PHDC | -0.605 | -1.047 | -1.050 | -0.883 | -0.662 |
| TMGH | -0.076 | -0.557 | -0.658 | -0.516 | -0.647 |

**All five compound monotonically from h=1 to h=3.** That is the signature of a
RATE error rather than a one-off level shock: a shock would show a step and then
a flat line, and none of them does.

Past h=3 the names split. ARCC and EGCH keep compounding (EGCH reaching -2.114,
the largest cell block in the book); PHDC turns back toward zero at h=4 and h=5;
TMGH flattens. A rate error that stops compounding is not a rate error at those
horizons, so the honest reading is a rate error out to three years and something
name-specific beyond it — with the caveat that the h=4 and h=5 cells are the
thinnest in every run, since only the earliest origins reach them.

## What is still not read

- The residual outside the devaluation years is +1.417 on ARCC across 18 cells
  and small elsewhere. Eighteen cells is not enough to call it a finding.
- The horizon shape above is not bootstrapped. It is a mean over cells that are
  not independent — the same origin contributes to several horizons — so it says
  which way the effect runs, not how confidently.
