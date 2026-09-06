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

## Two bugs this pass found

**In this session's own dump.** The first version of the ARCC per-cell dump
called `build_cells(cpi_only=True)` without `foresight=True`. ARCC's `_paths()`
only reads `cpi_only` inside its foresight branch, so the call fell through and
returned the as-known paths — and the table read "perfect CPI changes nothing on
ARCC" when the setting had never engaged. Caught because the number was exactly,
suspiciously identical to the as-known one.

**In ARCC's own module, latent.** `_paths()` now REFUSES `cpi_only` without
`foresight` rather than silently returning the knowable paths. The run's own
published scores never called it that way, so no ARCC number moves; what changes
is that the next caller cannot make the same mistake quietly. [R-ENF-04]: an
absent answer wearing the costume of a result.
