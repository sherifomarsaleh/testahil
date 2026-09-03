# Cost of capital — the reference tables, generated

**GENERATED from `engine/macro_paths/*.json` by `engine/build_coc_reference.py`. Never hand-edited.** Every figure below resolves from a committed macro path at build time; a number whose source has moved fails the build rather than printing stale. To change a figure, change the path file and re-run this.

Sourced 2026-08-20. Read the live state with `python3 engine/macro_path.py`, never this file from memory — it is regenerated whenever a path is re-sourced.


## What is held

| Market | State | Regime | Currency |
|---|---|---|---|
| EG | sourced, as of 2026-09-02 | transition | EGP |
| AE | **pending** | — | — |
| SA | **pending** | — | — |
| QA | **pending** | — | — |
| IN | **pending** | — | — |
| KR | **pending** | — | — |
| US | **pending** | — | — |

A market reading **pending** RAISES on load. There is no fallback to a neighbouring market, a region or a global average: an empty answer is not a clean answer, and the cost of a missing path is a study that stops, not a study built on a number nobody sourced.


---

## EG — EGP

Regime: **transition**. The policy rate sits far above its own long-run level and the central bank publishes a disinflation path, so the cost-of-capital glide applies here [Standing_Research_Protocol, 13-Jul r3 SCOPE]. Contrast the pegged markets, where today is already the terminal.


### Inflation

| Year | Rate | Basis |
|---|---:|---|
| 2026 | 16.00% | CBE baseline, average annual headline |
| 2027 | 12.00% | CBE baseline, average annual headline |
| 2028 | 9.00% | interpolated on the CBE's own stated glide from the 2027 baseline to the Q4-2028 target band midpoint, no year outside the published endpoints |
| 2029 | 7.50% | interpolated, as 2028 |
| 2030 | 7.00% | the target band midpoint in force, held |
| terminal | 7.00% | the target band midpoint in force |

Latest print: **14.90%** (July 2026, annual headline). Target: **7.0% ± 2.0pp**, Q4 2026.


### Rates

| | Value | As of |
|---|---:|---|
| Policy rate | 19.00% | 2026-08-20 |
| Sovereign 10-year | 23.00% | 2026-08-06 |
| Default spread, rating basis | 6.37% | |
| Default spread, swap basis | 3.41% | |
| Terminal cost of debt | 15.00% | long-run corporate norm |
| Terminal equity risk premium | 7.00% | normalised |

**Policy-rate path** (the SHAPE input for the cost-of-capital glide, never a second free parameter): 19.00% → 16.50% → 14.50% → 13.00% → 12.00%


### The derived terminal

Nothing in this block is a quote. Each line is an identity on the numbers above, because a terminal rate reverse-engineered from a price is the quietest lever there is.

| | Identity | Value |
|---|---|---:|
| Terminal risk-free | terminal inflation + real-rate convention (5.50%) | **12.50%** |
| Terminal growth, zero real | terminal inflation + stated real growth (0.00%) | **7.00%** |

### The currency, derived

Relative purchasing-power parity on this path's own inflation against long-run United States inflation of 2.50%. A study may not set this by hand.

| Year | Depreciation | USD/EGP |
|---|---:|---:|
| 2026 | 13.17% | 55.11 |
| 2027 | 9.27% | 60.22 |
| 2028 | 6.34% | 64.04 |
| 2029 | 4.88% | 67.17 |
| 2030 | 4.39% | 70.11 |

### Sources

- **inflation.latest** — Central Bank of Egypt, Monetary Policy Committee statement of 20 August 2026: annual headline inflation 14.9% in July 2026 against 14.3% in June; core 14.7% against 14.3%; monthly headline and core both 0.0% in July.
- **inflation.path** — Central Bank of Egypt Q1-2026 Monetary Policy Report as reported 11 May 2026: baseline average annual headline inflation 16.0% in 2026 and 12.0% in 2027 (alternative scenario, conflict persisting to end-2026: 17.0% and 13.0%, single digits in H2-2027). The 2028-2030 steps are a straight glide between the published 2027 baseline and the target midpoint; they are INTERPOLATION BETWEEN PUBLISHED ENDPOINTS and are labelled as such, never presented as a central-bank forecast.
- **inflation.target** — CBE inflation target 7% (+/-2pp) for Q4 2026; the bank states inflation will remain ABOVE the band in Q4 2026 and expects a return to it in the second half of 2027.
- **inflation.terminal** — The target band midpoint IN FORCE at the terminal horizon. The 5% (+/-2pp) figure once quoted for Q4 2028 is NOT used: the bank's own August 2026 guidance puts the return to the 7% band in the second half of 2027, so a terminal built on 5% would assume an undershoot the bank does not forecast. AMOC's edition of 06-Aug-2026 made exactly this correction and it is inherited here rather than re-litigated.
- **policy_rate** — Central Bank of Egypt Monetary Policy Committee, 20 August 2026 — rates held for a fourth consecutive meeting.
- **policy_rate.path** — Overnight deposit rate, 2026-2030, gliding with the published inflation path at an approximately constant real policy rate. It is the SHAPE input for the cost-of-capital glide and for the cost-of-debt path; it is not a second free parameter and no valuation input is set from it independently.
- **sovereign** — Egypt 10-year EGP government bond yield, market quote 6 August 2026, the quote already registered and used by the PHDC and EGCH cost-of-capital records. RE-SOURCE BEFORE ANY NEW STRIKE: this is the input the 14-day staleness rule bites on.
- **sovereign.spreads** — Damodaran country risk file, Egypt row, as registered by the studies' own cost-of-capital records (rating basis 6.37%, credit-default-swap basis 3.41%). Both bases are carried; which one is CENTRAL is a cost-of-capital decision, not a macro one.
- **fx** — USD/EGP 50.25, quote of 6 August 2026 as registered in the AMOC cost-of-capital record; the pound closed 50.30/50.40 on 4 August 2026 and its 52-week range is 46.64-54.86, so the currency is not range-bound.
- **fx.derivation** — The forward currency path is DERIVED from this path's own inflation ladder against long-run United States inflation by relative purchasing-power parity, never set by hand. A study that escalates costs at Egyptian inflation while depreciating the pound at a third of the differential is running two views of one economy [L-048].
- **us_inflation_lt** — Long-run United States consumer price inflation, the foreign leg of the purchasing-power-parity relation. Registered at 2.5% by AMOC (06-Aug-2026) and at 2.4% by EGCH; 2.5% is adopted for the house path and the 10bp difference is immaterial to any derived figure at this precision.
- **cost_of_debt_norm** — The long-run Egyptian corporate-borrowing norm, 14-16%, midpoint 15% absent a name-specific reason to deviate [Standing_Research_Protocol 13-Jul r2, clause 4].
- **real_rate_convention** — The standard emerging-market terminal real risk-free convention (~5.5pp). The terminal NOMINAL risk-free rate is DERIVED as this plus the inflation target in force, so the single most terminal-value-sensitive number in a model cannot be typed.
- **erp_terminal** — Terminal equity risk premium, normalised below the currently elevated crisis-era level toward the rating-class norm; never held flat into perpetuity.

---


## The rules these tables serve

- **One economy, one inflation.** Every growth rate in a model is stored as a real rate against a path id and recomputes to its nominal; a typed nominal rate is unfalsifiable and is refused. [L-048]
- **Terminal growth agrees with the inflation inside the terminal discount rate.** Growth below it is a perpetual real decline, which may be assumed but must be stated as the real number it is. [L-055]
- **The terminal risk-free rate is derived, never quoted.**
- **The explicit window runs until growth has converged on terminal** (within 2pp), so the terminal does not capitalise a rate the model never reached.
- **A sovereign quote older than 14 days is re-sourced before a strike.**

Enforced from outside by `scripts/check_macro_coherence.py`, negative-controlled by `scripts/check_macro_coherence_negative_control.py`, both in CI. [R-MACRO-01], [R-ENF-01]
