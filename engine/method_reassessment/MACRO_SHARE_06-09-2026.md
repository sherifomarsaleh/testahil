# Is the break effect macro? Three names, three different answers

Read live: `python3 engine/valuation_calibration/macro_share.py`

The five-name cut established that the under-forecast concentrates on the years
the currency moved, and that it compounds with the horizon. The obvious next
inference — that the devaluation is therefore the cause and a better currency
rule is the fix — is wrong on two of the three names that can answer.

Each run is re-run on its own pre-registered macro settings: as known at the
origin, perfect inflation only, and perfect foresight of every macro input.
**Every figure is on the intersection of cells scoreable in all three settings.**

| name | setting | n | bias | MAE |
|---|---|---:|---:|---:|
| EGCH | as known | 50 | -1.273 | 1.292 |
| | perfect CPI only | 50 | -1.144 | 1.155 |
| | perfect foresight | 50 | **-0.741** | 0.848 |
| AMOC | as known | 56 | -0.707 | 0.712 |
| | perfect CPI only | 56 | -1.136 | 1.136 |
| | perfect foresight | 56 | **+0.327** | 0.346 |
| ARCC | as known | 47 | -0.486 | 0.678 |
| | perfect CPI only | 47 | **-0.168** | 0.406 |
| | perfect foresight | 47 | -0.493 | 0.685 |

Macro share of the devaluation-year MAE: **AMOC 51%, EGCH 34%, ARCC -1%.**

## The three answers

**AMOC — macro, and the model transmits it correctly.** Handed the realised
Brent and the realised pound, the bias goes from -0.707 to **+0.327** and the
MAE more than halves. A refiner's revenue is a world price times a currency, and
this model knows what to do with both once it is told them. Nothing is wrong
with the driver rules; what is wrong is that nobody can forecast a devaluation.

**ARCC — not macro at all.** Perfect foresight of everything moves the bias from
-0.486 to -0.493. The break error on a domestic cement maker is company-side,
which is why the seven driver fixes in `RULE_AUDIT_06-09-2026.md` moved that run
and would move AMOC very little.

**EGCH — half and half**, and the half that is macro is mostly the currency
rather than inflation: perfect inflation alone recovers 0.13 of the 0.53.

## The result that matters most, and it is not in the headline

**On two of the three names, more macro truth makes the forecast worse.**

- AMOC's perfect-CPI-only setting is WORSE than knowing nothing (-1.136 against
  -0.707). Escalating a refiner's costs at realised Egyptian inflation while its
  dollar-priced revenue sits on the knowable path is [L-048] exactly: one event
  counted once and ignored once.
- ARCC's perfect-CPI-only setting is its BEST (-0.168), and adding the realised
  currency and the realised coal price takes it back to where it started
  (-0.493). Feeding the model the true currency makes it worse.

A model whose error INCREASES when it is handed the truth is mis-specified. That
is a specification error, not a calibration one, and [R-FCAL-01] already says no
correction factor may hide that class. It is also the direct evidence for the
coal-on-FX fix (F1): the transmission from the currency to the cost stack is
where ARCC's rule is wrong, and the foresight setting is what exposes it.

## What this does to the plan

A single house-wide correction for the break effect is ruled out by these three
names alone. The right response is per-name and per-class:

- where the break error is macro and the transmission is sound (AMOC), the fix
  is not a better point forecast, it is **ranges on years 3-5 from this record's
  own error distribution**, which [R-FCAL-01] already mandates and which no
  study yet publishes;
- where it is company-side (ARCC), the fix is the driver rules, one at a time,
  scored at ordinary origins;
- where handing the model truth makes it worse (AMOC on CPI, ARCC on FX), the
  transmission itself is the defect and is fixed before anything else is
  measured on that name.

## Correction, same day: AMOC's defect is a nominal freeze, not two clocks

This document first called AMOC's defect [L-048] — costs escalating while
revenue sits still. That is the shape this house has seen most often and it is
the wrong diagnosis here. Measured rather than read
(`engine/valuation_calibration/clock_test.py`), at three years:

| name | own inflation | revenue x | cost x | revenue clock | cost clock | gap |
|---|---:|---:|---:|---:|---:|---:|
| AMOC | 1.24 | 1.00 | 1.02 | **0.81** | **0.83** | +0.02 |
| EGCH | 1.39 | 1.31 | 1.39 | 0.94 | 1.00 | +0.06 |
| ARCC | 1.32 | 1.36 | 1.21 | 1.03 | 0.92 | -0.11 |
| TMGH | 1.54 | 2.95 | 2.92 | 1.92 | 1.90 | -0.02 |
| PHDC | — | — | — | — | — | untestable, reason printed |

**The GAP is the robust column and the levels are not.** Revenue is volume times
price, so a run forecasting real growth moves both clocks together for a reason
that is not escalation — TMGH sits near 1.9 on both because it forecasts a
growing book, which is a forecast rather than a defect. Volume cancels out of the
gap, so the gap is what tests [L-048].

**No run has a two-clock gap.** Every gap is inside ±0.11. So [L-048] — costs
escalating while revenue sits still — is not present anywhere in this book, and
the diagnosis this document first reached for is simply wrong about AMOC.

**Both of AMOC's sides are frozen.** The two clocks differ by two points; what
differs by twenty-four is the whole model against the economy it says it
believes in. Crude is both this company's product and, as feedstock, most of its
cost of sales, so freezing crude in pounds freezes almost the entire income
statement. A company standing still in nominal terms inside an economy inflating
at 7.4% a year is declining in real terms by construction — [R-MACRO-01]'s
terminal-growth-below-inflation defect arriving in the explicit window.

It also explains the setting that looks strangest above: perfect CPI alone is
worse than knowing nothing because it raises the only lines that were moving and
leaves the frozen 88% where it was, widening the gap rather than closing it.

EGCH, ARCC and TMGH are all at or above 0.92 on both clocks; AMOC alone sits
near 0.82 on both, which is what makes its figure readable at all.

## Two bugs this pass found

**In this session's own dump.** The first version of the ARCC per-cell dump
called `build_cells(cpi_only=True)` without `foresight=True`. ARCC's `_paths()`
only reads `cpi_only` inside its foresight branch, so the call fell through and
returned the as-known paths — and the table read "perfect CPI changes nothing on
ARCC" when the setting had never engaged. Caught because the number was exactly,
suspiciously identical to the as-known one.

**A third, in this document's own first diagnosis**, corrected above: the
elasticity draft of the clock test bumped inflation by a point and read the local
slope, which cannot see a level held still — it reported AMOC as "one clock" when
both its sides were frozen. Re-pointed at the escalation actually applied over
the horizon per [R-COC-01], never widened.

**In ARCC's own module, latent.** `_paths()` now REFUSES `cpi_only` without
`foresight` rather than silently returning the knowable paths. The run's own
published scores never called it that way, so no ARCC number moves; what changes
is that the next caller cannot make the same mistake quietly. [R-ENF-04]: an
absent answer wearing the costume of a result.
