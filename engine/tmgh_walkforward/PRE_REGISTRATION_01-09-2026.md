# TMGH — fundamental walk-forward training: PRE-REGISTRATION

**Instrument:** Talaat Moustafa Group Holding (EGX:TMGH) · market EG · exchange EGX
**Class:** real-estate developer, off-plan — but **point-in-time on handover**, not
percentage-of-completion. See B2 of the basis-break register; this is not the PHDC case.
**Written:** 1 September 2026, BEFORE any projection was run or any error computed.
**Status:** training record only. Nothing here is published, and nothing here changes a
delivered number until the correction it proposes has passed §8's test.

This file is fixed at the moment it was committed. Every parameter below is **stated**, not
fitted; where a rule needs a number, the number is a stated function of data available at the
origin, never a value chosen because it scored well. Sensitivities are reported, never
selected. If a later commit changes anything here, the change is itself dated and the affected
results are re-run and re-reported — the pre-registration is not edited to match the outcome.

**Read first:** `python3 engine/lessons.py TMGH --class "real-estate developer, off-plan,
percentage-of-completion"` — 39 lessons bind on this name and class. The ones that shaped the
rules below are cited where they bite. Lessons marked PROVISIONAL are recorded findings from an
unvalidated method: read, not obeyed.

---

## 0. Scope decision

**FULL run.** The panel holds **16 sourceable fiscal years** — FY2009 and FY2011–FY2025 — well
above the eight the standing rule requires. FY2007, FY2008 and FY2010 were published and their
releases are held, but survive only as scans whose summary tables do not resolve into columns;
they are excluded and the reason is stated (B9). Nothing was estimated to extend the window.

## 1. Origins

Annual origins at the fiscal year end (31 December). An origin is admissible once the panel
holds **five prior complete fiscal years** for the driver being projected.

* Panel span obtained: **FY2009, FY2011–FY2025**. Depth is not uniform; the score only ever
  uses years actually sourced, and a driver with a hole simply has fewer cells.
* First admissible origin: **FY2015** (FY2011–FY2015 in hand).
* Last scored origin: **FY2024** (h=1 resolves at FY2025).
* Origin FY2025 is **struck but unresolved**: it produces the forward projection the current
  update consumes and contributes no error.

At each origin the model sees **only** what had been published by that date, **as originally
reported**. Where a later filing restates a figure — TMG restated FY2024 in its FY2025
statements, B5 — the origin keeps the as-first-reported number and the restatement is recorded
beside it. This is enforced in `panel.py`'s ranking, not by remembering.

## 2. Horizons

**h = 1, 2, 3, 4, 5 years.** A pair (origin *o*, horizon *h*) is scored iff *o + h ≤ 2025*.

| origin | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|---|---|---|
| horizons resolved | 5 | 5 | 5 | 5 | 5 | 5 | 4 | 3 | 2 | 1 |

40 resolvable (origin, horizon) cells per driver, before per-driver definition windows (B10)
and sourcing holes cut into them.

## 3. Drivers, by class

Projected bottom-up. **Margins are OUTPUTS, never inputs** [L-005].

| # | driver | class | unit |
|---|---|---|---|
| D1 | new sales value (contracted) | volume × price | EGP mn |
| D2 | backlog conversion rate δ | conversion | fraction of (opening backlog + new sales) |
| D3 | development revenue | = D2 × (opening backlog + D1) | EGP mn |
| D4 | development cost ratio | cost per unit of revenue | fraction |
| D5 | recurring revenue (hospitality + other, combined) | volume × price | EGP mn |
| D6 | recurring cost ratio | cost per unit of revenue | fraction |
| D7 | SG&A | overhead | EGP mn (fixed + variable) |
| D8 | D&A | non-cash | EGP mn |
| D9 | finance cost | financing | EGP mn |
| D10 | income tax | regulated/tax | EGP mn |
| D11 | customer advances | working capital | EGP mn |
| D12 | development properties | working capital | EGP mn |

Aggregates are **rebuilt from the drivers, never projected directly**: total revenue, cost of
revenue, gross profit, operating profit, PBT, net profit, and the balance-sheet lines D11–D12
drive.

**Why no unit-and-price pair.** TMG does not publish a continuous unit-count series (B9).
Building `units × price` on its occasional mentions would divide one year's value by another
year's count — the arithmetic error [L-010] records, which on PHDC produced a price per unit of
28.5 against a true 11.2. The build therefore stands at **segment level with the gap stated**,
[R-SIGCM-02]'s "segment", not "unit".

## 4. Mechanical rule for each driver, with parameters

Evaluated with information available at origin *o* only. `TTM3(x, o)` is the trailing
three-fiscal-year arithmetic mean of *x* ending at *o*; `TTM5` likewise over five.
**No judgement drivers exist at a historical origin — the method is tested, not the analyst.**

* **D1 new sales value** — anchored on an exogenous market driver, never on the company's own
  trend alone:
  `newsales_{o+h} = UrbanPop_{o+h} × intensity_o × Π_{k=1..h}(1 + π_k)`, where
  `intensity_o = newsales_o / (UrbanPop_o × 1)` in EGP per urban head, held flat, and π is the
  Egyptian CPI path of the macro setting in force (below). Urban population from World Bank
  WDI `SP.URB.TOTL`, projected at the growth rate observable before the origin.
  **This rule is expected to run low and is kept anyway** [L-101]: volume is set by the launch
  calendar and no demographic anchor can see it. Its miss at the FY2023–FY2024 launch origins
  is a finding, not a defect to patch.
* **Two macro settings, both pre-registered**, run at every origin — the pair is what defines
  the macro/company split in §6:
  * **as-known:** π_k = `TTM3(CPI, o)` held flat — the honest information set at the origin.
  * **perfect-foresight:** π_k = realised CPI. Not a forecast; it exists solely to price how
    much of the miss is macro.
* **D2 conversion rate δ** — `δ_o = TTM3(dev_revenue / (opening backlog + new sales), o)`, held
  flat over the horizon. Scored only over FY2012–FY2024, never across the
  percentage-of-completion break (B2).
* **D3 development revenue** — `rev_{o+h} = δ_o × (backlog_{o+h-1} + newsales_{o+h})` with the
  backlog rolled forward: `backlog_t = backlog_{t-1} + newsales_t − rev_t`. Never projected as
  its own series. **Deliveries cannot outrun the order book by construction** — the guard
  [L-104] records as missing on PHDC is built into the roll rather than left unguarded, and
  δ is clipped to (0, 1].
* **D4 development cost ratio** — `c_o = TTM3(dev_cost / dev_revenue, o)`, held flat;
  `dev_cost_{o+h} = c_o × rev_{o+h}`. Gross margin is the residual and is never set.
  Revenue and cost sit on the **same recognition clock** by construction, both being handover
  quantities [L-001].
* **D5 recurring revenue** — `rec_{o+h} = rec_o × Π(1 + π_k) × (1 + g_o)^h`, with
  `g_o = TTM3(real growth of recurring revenue, o)` — the trailing real growth rate, so the
  driver escalates on inflation once and on its own real trend once, never twice.
* **D6 recurring cost ratio** — `TTM3(recurring cost / recurring revenue, o)`, held flat.
  One escalator per driver class [L-009]: the recurring leg escalates on its own cost ratio,
  not on the development escalator.
* **D7 SG&A** — fixed + variable, `SGA_t = a_o + b_o × revenue_t`, with `(a_o, b_o)` from
  **OLS on the trailing five fiscal years at the origin**, no shrinkage, no winsorising.
  `a_o` escalates with the same CPI path as D1.
* **D8 D&A** — PP&E roll-forward: `PPE_t = PPE_{t-1} + capex_t − D&A_t`,
  `D&A_t = d_o × PPE_{t-1}`, `d_o = TTM3(D&A / opening PP&E, o)`; capex held at
  `TTM3(capex, o)` escalated on the CPI path where the panel carries it, else zero and flagged.
  This driver is expected to compound its own error [L-028] and the record will say so.
* **D9 finance cost** — `interest_t = kd_o × interest_bearing_debt_{t-1}`, with
  **`interest_bearing_debt` = long-term loans + current portion of loans + credit facilities +
  bank overdrafts + lease liabilities, AND NOTHING ELSE.** Customer advances (EGP 117.7bn at
  FY2025), suppliers and contractors, obligations against notes receivable and creditors are
  all funding and none of them pays a coupon. `kd_o = TTM3(finance cost / opening
  interest-bearing debt, o)`. **This is written into the pre-registration, not left to the
  build**, because dividing by a broader liabilities total is exactly what manufactured a
  large, robust and entirely spurious finance-cost bias on PHDC — a denominator 4.4x too big,
  implying a 3.19% borrowing rate for a company borrowing at 13.91% [L-002]. Debt is held flat
  at its origin level: a stated, parameter-free path, because any repayment schedule would be
  a judgement.
* **D10 tax** — by formula under the regime **known at the origin**: Egypt's statutory
  corporate rate as legislated at that date (22.5% from FY2015), applied to positive PBT, zero
  otherwise. A regime change after the origin is a macro/regulatory miss, not a company miss.
* **D11 customer advances** — `advances_t = advances_{t-1} + newsales_t × col_o − rev_t × rec_o`,
  with `col_o = TTM3(Δadvances + dev_revenue) / new sales` at the origin, clipped to [0, 1.5].
  **Both contract positions move together** [L-103]: advances and the receivable leg are both
  driven off the same order book, never one off revenue and the other off backlog.
* **D12 development properties** — `dp_t = dp_{t-1} + build_t − dev_cost_t`, with
  `build_t = TTM3(Δdp + dev_cost, o)` escalated on the CPI path.

## 5. Naive benchmarks

Computed for every driver and every aggregate at every (origin, horizon):

* **freeze** — every line flat at the last actual: `F_{o+h} = A_o`.
* **trend** — trailing three-year CAGR from the origin:
  `T_{o+h} = A_o × (A_o / A_{o-3})^{h/3}`.

Skill is the reduction in mean absolute log error against each benchmark, per horizon. **A
method that cannot beat "no change" has not earned the precision it displays** — where that
happens the record says so plainly.

## 6. Score

* **Primary:** log error `e = ln(projected / actual)`, per driver, per horizon. Reported as
  **bias** (mean e) and **MAE** (mean |e|).
* **Sign cases:** where either side is ≤ 0 the log is undefined. Those cells are **not**
  dropped and **not** patched — they are counted in a separate sign-error tally and scored as
  `(P − A) / |A|`, reported separately and never pooled into the log statistics.
* **Uncertainty:** moving-block bootstrap over **origins**, block lengths **{2, 3, 4}**, 2000
  resamples — the house robustness bar. A bias is called robust only if its sign holds across
  all three block lengths.
* **Shares:** fraction of origins over- and under-forecast, and the sign by era.
* **Macro vs company split:** the same projection is run twice per origin — as-known and
  perfect-foresight. The **perfect-foresight error is the company error**; the difference is
  the **macro/regulatory error**. Both are reported for every driver.
  **The split carries its own check:** a driver with no inflation term in its rule must return
  a macro share of exactly zero by construction, and the record prints that check rather than
  asserting it.
* **Eras** (fixed here by FX regime, dated, never re-cut after seeing a result — B3):
  * **E1 pre-float:** FY2011–FY2015
  * **E2 post-float:** FY2016–FY2021
  * **E3 devaluation cycle:** FY2022–FY2025

## 7. Roles of the two samples

* The **rolling record** — all admissible (origin, horizon) cells, horizons overlapping —
  **estimates** the corrections.
* The **non-overlapping origins** — spaced ≥ 5 apart so no two share a forecast year —
  **confirm** them. With a FY2015 first origin this set is thin ({2015, 2020} and its shifts);
  the thinness is stated as a limit of a single-name study, not worked around.

## 8. Corrections (rule fixed in advance)

* **Expanding window only**: a correction applied at origin *o* uses errors resolved **before**
  *o*. No correction is ever informed by an outcome it is then scored on.
* **Half strength by default**: applied correction = 0.5 × estimated bias.
* Applied **only** where the bias holds its sign across eras [L-029], [L-030].
* **Reset** after a structural break, defined as a driver error beyond its own two-sigma, and
  at the dated breaks of B4 and B8.
* A correction enters the live update's drivers only if it (a) passed the adjusted-vs-raw test
  here **and** (b) is consistent with how that driver class is built across the market's book
  [L-003]. Otherwise it is a **watch flag** — recorded, graded live, revisited at the next
  update, acted on by nobody.
* Management **guidance** is logged separately (guidance vs outcome, and its bias). **Guidance
  is scored, never consumed** [L-012]: a driver taking guidance as an input inherits its lean
  instead of correcting for it.

## 9. What would make this record misleading

Stated in advance so it cannot be discovered later and quietly dropped:

1. **The cells are not independent.** Ten origins × five horizons is 40 cells drawn from
   fifteen years of one company. Overlapping horizons share outcome years; the block bootstrap
   is the response, and it does not make the sample large.
2. **One name.** Nothing here is evidence about developers in general. Every lesson this run
   produces is filed PROVISIONAL under [R-LESSON-01] and the code refuses to write one as
   adopted.
3. **The launch calendar dominates the late origins.** FY2023–FY2025 contracted sales run
   142.8 → 504.0 → 382.2 EGP bn on SouthMed and The Spine. No mechanical rule anchored on
   population and inflation can see a launch, so the late-origin misses will be enormous and
   they measure the launch, not the method's ordinary accuracy. Both are reported, separately.
4. **The devaluation era is half the record.** E3 is four of fifteen years but carries most of
   the nominal growth. A bias measured pooled across E1–E3 is an average of regimes that were
   never the same regime.
5. **The recognition break is live, not historical.** The Saudi percentage-of-completion leg
   starts in the last panel year and is already 52.5% of segment revenue by 1H2026. The
   scored record therefore describes a company whose development revenue is recognised on a
   basis that is currently changing.
6. **Backlog before FY2018 is approximate.** "Approximately EGP 20 BN" is what the company
   published; the conversion rate δ at early origins inherits that roundness.
