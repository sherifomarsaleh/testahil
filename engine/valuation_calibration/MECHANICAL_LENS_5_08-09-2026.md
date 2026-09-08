# Mechanical lens, declaration 5 — the terminal converges before it capitalises

**Sealed and committed BEFORE any figure under it was computed.** That is the whole of
this document's claim on credibility and it is a fact about commit order, checkable from
outside: the commit introducing this file must be an ancestor of the commit introducing
any score computed under it.

This supersedes declaration 4 (`MECHANICAL_LENS_4_08-09-2026.md`) **in the terminal and
in nothing else.** Origins, projections, cost of capital, bridge, point-in-time
discipline, benchmarks, bootstrap, leave-one-name-out and era tests stand exactly as
declaration 3 wrote them and declaration 4 left them.

---

## 1. The defect this replaces, measured

[R-MACRO-01] states, in the house's own words:

> THE EXPLICIT WINDOW RUNS UNTIL GROWTH IS WITHIN 2pp OF TERMINAL: a model whose last
> explicit year still grows far above its terminal capitalises a rate it never reached.

**Measured across all seventeen scoring cells, ELEVEN BREAK IT:**

| cell | growth, last explicit year | terminal | over by |
|---|---|---|---|
| ARCC 2017 | 30.8% | 7.0% | **+23.9pp** |
| ARCC 2023 | 31.2% | 9.5% | **+21.7pp** |
| SWDY 2019 | 17.5% | 7.1% | +10.4pp |
| ARCC 2016 | 16.0% | 7.1% | +8.9pp |
| ARCC 2018 | 15.6% | 7.0% | +8.6pp |
| SWDY 2016 | 14.6% | 7.1% | +7.4pp |
| ARCC 2022 | 14.4% | 7.0% | +7.4pp |
| PHDC 2022 | 13.9% | 7.0% | +6.9pp |
| TMGH 2021 | 12.5% | 7.1% | +5.3pp |
| SWDY 2015 | 10.6% | 7.0% | +3.6pp |
| ARCC 2019 | 10.4% | 7.1% | +3.3pp |

The model forecasts five years, and in year five the company is still growing at thirty
per cent because the ECONOMY is still inflating at thirty per cent. It then takes that
year and treats it as the permanent base for ever. **The terminal carries 45% to 72% of
the value on every one of these cells** — a peak the model's own macro path says will
fade, capitalised as though it will not.

## 2. Why the window is not simply lengthened

The obvious repair is to run the explicit window to convergence, which is what the rule
says. **It is refused here and the reason is not convenience.** Every run's projection
declares HORIZONS = 1..5 in its own pre-registration. Extending a projector past its
declared scope to make a cell score is the selection this method forbids everywhere else
— it is the same move the lens already refused for AMOC, whose run declares horizons 1-3
because it is a LIGHT-scope name, and whose cells are dropped rather than extended.

**A pre-registration is not overridden to improve a result.** So the convergence happens
where this lens is entitled to act: in the terminal it builds itself.

## 3. The terminal

For each origin, with the projection and cost-of-capital schedule unchanged:

```
STAGE 1 — CONVERGENCE.  From the last explicit year N, the cash flow is carried
          forward year by year at the growth the ORIGIN'S OWN PUBLISHED INFLATION
          LADDER states for that year, until that growth is within 2pp of terminal.
          Each such year is discounted at the same rate the explicit window uses.

STAGE 2 — CAPITALISATION.  The converged year is then capitalised:
              TV = FCF_M x (1 + g) / (WACC_terminal - g)
          and brought home on the cumulative factor of year M.
```

- **`g`** is `terminal_inflation(market) + real_growth`, `real_growth = 0.0`, exactly as
  declaration 4 defines it. Unchanged.
- **The convergence path is READ, NEVER CHOSEN.** It is the same
  `cpi_annual.forward_path` the archive already holds for that origin, point-in-time —
  at origin 2021 it says 6-7% for ever, so the stub is EMPTY there and the construction
  collapses to declaration 4. **Where the rule is already satisfied, nothing changes.**
- **The stub is capped at ten years beyond the explicit window.** The cap is not a
  parameter chosen to produce a result: it exists because a published ladder can be
  short, and a path that has not converged in fifteen years total is a path this lens
  should refuse rather than extrapolate. **A cell that has not converged at the cap is
  DROPPED**, with its reason, exactly as an unbuildable terminal is dropped.
- Every refusal declaration 4 carries stands unchanged: `g >= WACC_terminal`,
  non-positive terminal free cash flow, non-positive equity per share, and non-positive
  explicit-window present value.

## 4. What this gives up, stated now rather than discovered later

The stub years are **mechanical rather than modelled** — the company's cash flow is
carried at an inflation rate with no volume or margin path behind it. That is weaker
than a forecast and it is deliberately so: this lens is not entitled to forecast years
the run's own pre-registration declined to project. **What it buys is that the figure
finally capitalised is one the model's own macro path says the economy will actually be
at**, instead of a crisis peak.

**The direction is not predicted here and may not be.** A longer discounting chain
lowers the present value; a compounding cash flow raises it; which dominates is measured
after this file is committed, never before. Declaration 4's own text says the same of its
own change and it is repeated because it is the part most easily forgotten.

## 5. Falsifier

Unchanged from declaration 4: if the mechanically rebuilt series does not resemble the
series the house actually delivers, once that record is long enough to compare, this
calibration is grading a method the house does not use and every finding under it must be
withdrawn.
