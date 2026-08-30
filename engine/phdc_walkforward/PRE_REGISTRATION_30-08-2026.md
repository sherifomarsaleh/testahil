# PHDC — fundamental walk-forward training: PRE-REGISTRATION

**Instrument:** Palm Hills Developments (EGX:PHDC) · market EG · exchange EGX
**Written:** 30 August 2026, BEFORE any projection was run or any error computed.
**Status:** training record only. Nothing here is published, and nothing here changes a
delivered number until the correction it proposes has passed §5's test.

This file is fixed at the moment it was committed. Every parameter below is **stated**,
not fitted; where a rule needs a number, the number is a stated function of data available
at the origin, never a value chosen because it scored well. Sensitivities are reported,
never selected. If a later commit changes anything in this file, that change is itself
dated and the affected results are re-run and re-reported — the pre-registration is not
edited to match the outcome.

---

## 1. Origins

Annual origins, each set at the company's fiscal year-end (31 December). An origin is
admissible once the panel holds **five prior complete fiscal years** for the driver being
projected.

* Panel span obtained: **FY2011 – FY2025** (see the panel's own coverage table for what
  each year actually holds; depth is not uniform across the span and the score only ever
  uses years that are sourced).
* First admissible origin: **FY2015** (2011–2015 in hand).
* Last scored origin: **FY2024** (h=1 resolves at FY2025).
* Origin FY2025 is *struck but unresolved* — it produces the forward projection the current
  update consumes; it contributes no error.

At each origin the model sees **only** what had been published by that date, **as
originally reported**. Where a later filing restates a figure the origin used, the
restatement is recorded in the basis-break register and the origin keeps the
as-first-reported number. Restated-vs-original differences are reported, not silently
adopted.

## 2. Horizons

**h = 1, 2, 3, 4, 5 years.** A pair (origin *o*, horizon *h*) is scored iff *o + h ≤ 2025*.
That yields 40 resolvable (origin, horizon) cells per driver:

| origin | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|---|---|---|
| horizons resolved | 5 | 5 | 5 | 5 | 5 | 5 | 4 | 3 | 2 | 1 |

## 3. Drivers, by class

Projected bottom-up. Margins are **outputs**, never inputs.

| # | driver | class | unit |
|---|---|---|---|
| D1 | units sold (contracted) | volume | units/yr |
| D2 | average selling price per unit | price | EGP mn/unit |
| D3 | new-sales value (= D1 × D2) | volume × price | EGP mn |
| D4 | revenue-recognition rate δ | conversion | fraction of (opening backlog + new sales) |
| D5 | units delivered | volume | units/yr |
| D6 | cost per unit delivered | cost per unit | EGP mn/unit |
| D7 | SG&A | overhead | EGP mn (fixed + variable) |
| D8 | D&A | non-cash | EGP mn |
| D9 | interest expense | financing | EGP mn |
| D10 | income tax | regulated/tax | EGP mn |
| D11 | construction spend | capex | EGP mn |
| D12 | working capital (DSO/DIO/DPO) | balance sheet | days |

Aggregates rebuilt from the drivers — never projected directly: revenue, COGS, gross
profit, EBITDA, PBT, net profit, and the balance-sheet and cash-flow lines they drive.

## 4. Mechanical rule for each driver, with parameters

Every rule is evaluated with information available at origin *o* only. `TTM3(x, o)` is the
trailing three-fiscal-year arithmetic mean of *x* ending at *o*; `TTM5` likewise over five.
**No judgement drivers exist at a historical origin — the method is tested, not the analyst.**

* **D1 units sold** — anchored on an exogenous market driver, never on the company's own
  trend alone:
  `units_{o+h} = UrbanPop_{o+h} × intensity_o × 1`, with
  `intensity_o = units_o / UrbanPop_o` held flat over the horizon, and `UrbanPop` projected
  at the growth rate published before the origin (Egypt urban population, CAPMAS/World Bank
  series; the vintage used at each origin is recorded in the panel).
* **D2 ASP** — `ASP_{o+h} = ASP_o × Π_{k=1..h} (1 + π_k)`, where π is the **expected
  Egyptian CPI inflation path**. Two macro settings are run at every origin, both
  pre-registered, and the pair is what defines the macro/company split in §6:
  * **as-known:** π_k = TTM3(CPI, o) held flat — the honest information set at the origin.
  * **perfect-foresight:** π_k = realised CPI. Not a forecast; it exists solely to price
    how much of the miss is macro.
* **D3 new-sales value** = D1 × D2. Never projected as its own series.
* **D4 recognition rate** — `δ_o = TTM3(revenue / (opening backlog + new sales), o)`, held
  flat. `revenue_{o+h} = δ_o × (backlog_{o+h-1} + newsales_{o+h})`, with backlog rolled:
  `backlog_t = backlog_{t-1} + newsales_t − revenue_t`.
* **D5 units delivered** — `delivered_{o+h} = ρ_o × opening backlog units`, with
  `ρ_o = TTM3(delivered / opening backlog units, o)`; where backlog units are not disclosed
  the rule falls back to `delivered_{o+h} = TTM3(delivered, o) × (units_{o+h} / units_o)`
  and the fallback is flagged in the record.
* **D6 cost per unit delivered** — `cpu_{o+h} = cpu_o × Π (1 + c_k)`, `cpu_o = TTM3(COGS /
  delivered, o)`, escalator `c` = construction-cost inflation on the **same two settings as
  D2**. One escalator per driver class: the build cost escalates on construction cost, not
  on headline CPI, wherever a construction series is sourced; where it is not, headline CPI
  is used and the substitution is flagged.
* **D7 SG&A** — fixed + variable, `SGA_t = a_o + b_o × revenue_t`, with `(a_o, b_o)` from
  **OLS on the trailing five fiscal years at the origin**, no shrinkage, no winsorising.
  `a_o` escalates with the same CPI path as D2.
* **D8 D&A** — PP&E roll-forward: `PPE_t = PPE_{t-1} + capex_t − D&A_t`,
  `D&A_t = d_o × PPE_{t-1}`, `d_o = TTM3(D&A / opening PP&E, o)`.
* **D9 interest** — `interest_t = kd_o × gross debt_{t-1}`, `kd_o = TTM3(finance cost /
  opening gross debt, o)`. Gross debt is held flat at its origin level: a stated,
  parameter-free path, chosen because any repayment schedule would be a judgement.
* **D10 tax** — by formula under the regime **known at the origin**: Egypt's statutory
  corporate rate as legislated at that date (22.5% from FY2015; 25% before), applied to
  positive PBT, zero otherwise. A regime change after the origin is a macro/regulatory
  miss, not a company miss.
* **D11 construction spend** — the disclosed programme/guidance at the origin where the
  company gave one, else `TTM3(construction spend, o)` escalated on the D6 cost path.
  Construction spend drives WIP and therefore deliveries; it is an input, not an output.
* **D12 working capital** — DSO, DIO and DPO computed at the origin and held flat, applied
  to the projected revenue and cost lines to project notes/accounts receivable, works in
  process, advances from customers and suppliers, and from there the balance sheet and the
  cash-flow statement. No unexplained plugs where the driver is disclosed.

## 5. Naive benchmarks

Both are computed for every driver and every aggregate at every (origin, horizon):

* **freeze** — every line flat at the last actual: `F_{o+h} = A_o`.
* **trend** — trailing three-year CAGR from the origin:
  `T_{o+h} = A_o × (A_o / A_{o-3})^{h/3}`.

Skill is reported as the reduction in mean absolute log error against each benchmark,
per horizon. A bottom-up model that cannot beat freeze at h=1 is reported as such.

## 6. Score

* **Primary:** log error `e = ln(projected / actual)`, per driver, per horizon.
  Reported as **bias** (mean e) and **MAE** (mean |e|).
* **Sign cases:** where either side is ≤ 0 the log is undefined. Those cells are **not**
  dropped and **not** patched — they are counted in a separate sign-error tally and scored
  as `(P − A) / |A|`, reported separately and never pooled into the log statistics.
* **Uncertainty:** moving-block bootstrap over **origins**, block lengths **{2, 3, 4}**,
  2000 resamples, the house robustness bar used elsewhere in this repo. A bias is called
  robust only if its sign holds across all three block lengths.
* **Shares:** fraction of origins over-forecast and under-forecast, and the sign by era.
* **Macro vs company split:** the same projection is run twice per origin — once on the
  as-known macro path, once on perfect foresight. The **perfect-foresight error is the
  company error**; the difference between the two is the **macro/regulatory error**. Both
  are reported for every driver.
* **Eras** (pre-registered by FX regime, dated, not chosen by outcome):
  * **E1 pre-float:** FY2011 – FY2016 (EGP pegged near 7.8–8.8/USD to Nov-2016).
  * **E2 post-float:** FY2017 – FY2021 (float, then broadly range-bound 15.7–17.5).
  * **E3 devaluation cycle:** FY2022 – FY2025 (Mar-2022, Oct-2022, Jan-2023 and Mar-2024
    steps).

## 7. Roles of the two samples

* The **rolling record** — all admissible (origin, horizon) cells, horizons overlapping —
  **estimates** the corrections.
* The **non-overlapping origins** — origins spaced ≥ 5 apart so no two share a forecast
  year — **confirm** them. With a FY2015 first origin this set is thin ({2015, 2020} and
  its shifts); the thinness is stated as a limit of a single-name study, not worked around.

## 8. Corrections (rule fixed in advance)

* Expanding window only: a correction applied at origin *o* uses errors **resolved before
  *o***. No correction is ever informed by an outcome it is then scored on.
* **Half strength by default**: applied correction = 0.5 × estimated bias.
* Applied **only** where the bias holds its sign across eras (§6).
* **Reset** after a structural break, defined as a driver error beyond its own two-sigma.
* A correction enters the live update's drivers only if it (a) passed the adjusted-vs-raw
  test here and (b) is consistent with the same driver class across the market's book.
  Otherwise it is recorded as a **watch flag** — graded live, revisited at the next update,
  never acted on.
* Management **guidance** is logged separately (guidance vs outcome, and its bias). Guidance
  is scored, never used as a driver at a historical origin.

## 9. What would make this record misleading

Stated in advance so it cannot be discovered later and quietly dropped:

* **One name, few origins.** Ten origins and three macro eras is a small sample for a
  five-horizon claim; block-bootstrap intervals will be wide and are reported wide.
* **Overlapping horizons.** The rolling record's cells are not independent; that is why the
  non-overlapping set exists, and why it is reported even though it is thin.
* **A regime that dominates.** Egypt's 2016 float and the 2022–2024 devaluation steps move
  every nominal driver at once. If the record's corrections turn out to be a restatement of
  "the currency fell", that is a finding about the macro path, not about the company's
  driver rules, and it is reported that way.
* **Survivorship in the disclosure.** The company's own KPI definitions changed (see the
  basis-break register); a driver scored across a redefinition is scored inside its own
  definition window only.
