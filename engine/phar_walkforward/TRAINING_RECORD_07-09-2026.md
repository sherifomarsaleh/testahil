# PHAR — fundamental walk-forward training record, 7 September 2026

**INTERNAL.** This record, the panel, the error cells, the pre-registration and the
basis-break register are never shown to a reader [R-FCAL-01].

**Which walk-forward this is:** the FUNDAMENTAL one — drivers rebuilt at a past origin and
scored against what EIPICO reported. Not the price-engine walk-forward (band coverage on
the Monte Carlo cone, `engine/phar_study/backtest_5y.py`) and not the technical
walk-forward (`engine/lab/ta_calibration/`, the shipped read replayed on a 5/10/21-session
clock). Three different tests in this system are called a walk-forward and they are not
the same thing.

Ticker **PHAR** · EIPICO · EGX · class **pharmaceutical manufacturer, generic and
branded**. Pre-registration: `PRE_REGISTRATION_07-09-2026.md`, committed before a single
error was computed and unamended.

---

## 1 · Scope — LIGHT, and what stopped the window

**Seven sourceable fiscal years, FY2019–FY2025.** Five origins (FY2020–FY2024), horizons
1–3, **twelve scoreable origin-horizon cells per driver** and 150 scored cells in all.

The window stops at FY2019 because that is where EIPICO's own archive stops. Its
investor-relations page lists seven annual reports and all seven were retrieved; the
FY2019 edition is a board-of-directors report carrying operating KPIs and **no financial
statements at all**, so FY2018 has units, sales and exports and no accounts. It is left
out rather than fabricated. The exchange and regulator disclosure portals were
re-attempted today and neither resolves, so nothing behind them was reachable.

**Every financial figure in the panel is tier A** — EIPICO's own audited consolidated
statements, out of EIPICO's own annual reports. **Every operating figure is tier A
COMPANY_IR** — the company's own indicator tables. No vendor, no broker, no press.

---

## 2 · What the arithmetic found in the filings, before any modelling

`panel.assert_all()` foots every income statement, balance sheet, share count and KPI
table against its own subtotals and RAISES rather than warns. **Six printed cells across
these filings do not foot.** Each was settled by the statement's own chain, never by
preference, and the defective cell is named:

| # | filing | printed | correct | how it was settled |
|---|---|---|---|---|
| F-1 | FY2022 | gross profit 1,635,187,843 | **1,653,187,843** | revenue less cost of sales gives 1,653,187,843, and only that figure carries the statement's own chain to its printed profit before tax of 804,744,041. **The same defective figure is carried forward into the FY2023 comparative**, so two filings agree and both are wrong |
| F-2 | FY2023 | fixed assets 963,645,369 | 963,645,365 | the sheet misses balancing by four pounds as printed; the FY2024 comparative balances exactly |
| F-3 | FY2024 | income taxes payable 344,864,967 | 344,846,967 | only 344,846,967 reproduces the printed current-liability subtotal; the FY2025 comparative agrees |
| F-4 | FY2024 | long-term lease liabilities 10,705,609 | 10,706,509 | only 10,706,509 reproduces the printed non-current subtotal |
| F-5 | FY2024 | total liabilities 10,715,372,056 | 10,715,372,065 | its own two components sum to 065 |
| F-6 | FY2023 | associates + interest income sub-total 100,751,986 | carried as printed | its two components sum to 100,751,983, three pounds below. **The sub-total is the figure the statement uses** and it is what carries the chain to the printed profit before tax, so it is carried and the three pounds are recorded rather than allocated to one component on a guess |

**F-1 is the one worth remembering.** It is EGP 18.0mn, it is a plain transposition, and
the ordinary check — read the next year's comparative and see whether it agrees — CONFIRMS
IT. Only the statement's own arithmetic separates the two.

The FY2024 report's Arabic glyph map is partly broken: several header strings render as
mojibake while the Latin digits extract cleanly, which is exactly the condition
[R-FCAL-01] warns about. Three of the six failures are in that filing.

**Eight re-presentations** sit inside the window and are recorded beside the figures they
would replace, never substituted: two revenue gross-up/net-down reclassifications (FY2020,
FY2021), a FY2021 net-profit presentation change worth EGP 34.5mn, a receivables netting,
a FY2023 administrative-expense split of exactly the dividend-tax line, a FY2024
borrowings split that leaves total interest-bearing debt unchanged to the pound, **a
packs-produced redefinition worth 2.1% of the FY2024 figure** — a KPI this run scores —
and a two-million-pound disagreement between the FY2024 income statement and the FY2025
comparative cash-flow statement about the same profit before tax.

---

## 3 · The result: the SCALE is under-forecast and the MARGIN is roughly right

Pooled over 150 cells, log error `e = ln(forecast/actual)`; negative is under-forecast.
Intervals are the pre-registered moving-block bootstrap over origins, blocks {2,3}, 2,000
resamples, seed 42.

| driver | n | bias | 90% interval | MAE | vs FREEZE | vs TREND |
|---|---:|---:|---|---:|---:|---:|
| revenue | 12 | **−0.310** | −0.374 to −0.179 | 0.318 | +29% | +28% |
| cost of sales | 12 | −0.294 | −0.355 to −0.182 | 0.300 | +31% | +42% |
| gross profit | 12 | −0.331 | −0.407 to −0.186 | 0.342 | +27% | −5% |
| charges below gross profit | 12 | −0.396 | −0.487 to −0.231 | 0.432 | +25% | −118% |
| profit before tax | 12 | −0.584 | −0.750 to −0.408 | 0.584 | **−35%** | +4% |
| **net profit** | 12 | **−0.553** | −0.738 to −0.364 | 0.553 | **−32%** | +5% |
| associates + interest income | 12 | −0.550 | −1.069 to −0.130 | 0.695 | +20% | +39% |
| interest-bearing debt | 12 | −0.415 | −0.585 to −0.133 | 0.511 | +30% | −17% |
| packs produced | 9 | **+0.044** | +0.008 to +0.070 | 0.071 | −35% | +2% |
| revenue per pack | 9 | −0.352 | −0.459 to −0.183 | 0.375 | +25% | +0% |
| cost per pack | 9 | −0.341 | −0.435 to −0.192 | 0.360 | +26% | +19% |
| finance cost | 9 | −0.572 | −0.701 to −0.369 | 0.610 | +40% | +32% |
| capex | 9 | −0.733 | −1.016 to −0.288 | 0.989 | +3% | +38% |
| depreciation and amortisation | 9 | **+0.499** | +0.388 to +0.637 | 0.499 | **−402%** | −304% |

**Not one interval on any of the fourteen drivers covers zero.** On a twelve-cell record
that is a statement about consistency rather than about magnitude, and the consistency is
one-directional: thirteen of fourteen drivers are under-forecast.

**The bias compounds with the horizon**, which is the signature of a rate error rather
than a base-year error:

| horizon | n | bias | MAE | vs FREEZE | vs TREND |
|---|---:|---:|---:|---:|---:|
| 1 year | 64 | −0.157 | 0.294 | −0.0% | −6.4% |
| 2 years | 50 | −0.387 | 0.494 | +19.5% | +13.4% |
| 3 years | 36 | −0.693 | 0.763 | +13.3% | +20.4% |

### The decomposition, and it is an identity rather than a regression

Revenue = packs × price per pack × the consolidation ratio, so the three log errors sum to
the revenue log error exactly:

> mean revenue error **−0.303** = volume **+0.044** + price **−0.352** + consolidation
> residual **+0.004**

**The whole of the revenue miss is PRICE. None of it is VOLUME.** The method forecasts how
many packs EIPICO makes to within four and a half per cent over three years — anchored on
Egypt's population growth with the company's own trend allowed ±2pp around it — and misses
what each pack sells for by more than a third.

### Net profit, and the line the rule deliberately does not forecast

> mean net-profit error **−0.553**; gross profit −0.331; charges below gross profit
> −0.396; associates and interest income −0.550

Rule R11 sets capital gains, the foreign-exchange result and other income to **zero** at
every origin, because a mechanical rule cannot forecast a currency result and inventing
one would be the judgement driver this exercise forbids. Those lines are **23.8% of actual
profit before tax on average and 48.2% at their peak** — FY2024, the year of the float.
So roughly two fifths of the gap between the gross-profit error and the net-profit error
is a line the method declines to forecast, by design, and the record says so rather than
letting a driver quietly carry a currency view.

---

## 4 · Skill against the two naive benchmarks

**A METHOD THAT CANNOT BEAT "NO CHANGE" HAS NOT EARNED THE PRECISION IT DISPLAYS, AND ON
THE LINE THAT MATTERS MOST THIS ONE DOES NOT.**

| line | horizon | vs FREEZE | vs TREND |
|---|---|---:|---:|
| revenue | 1 / 2 / 3 | +43% / +34% / +18% | +26% / +27% / +28% |
| gross profit | 1 / 2 / 3 | +38% / +33% / +17% | −2% / −7% / −4% |
| **net profit** | 1 / 2 / 3 | **−97% / −17% / −11%** | −91% / +11% / +33% |

On **revenue** the method beats both benchmarks at every horizon, comfortably. On **gross
profit** it beats freezing and is indistinguishable from a trailing trend. On **net
profit** it is beaten by freezing last year's number at every horizon, and beaten worst at
one year, where it is nearly twice as wrong.

That is the same verdict PHDC returned on the same line, and the reason here is nameable
rather than mysterious: net profit is where the below-the-line currency result lands, and
freezing last year's net profit implicitly carries a currency result forward while the
mechanical rule carries none. **It does not mean the driver model is worse than no model.
It means the published NET-PROFIT path of a study on this name should not be read as
carrying more information than "roughly last year's, plus the drivers", and the study's
own far-year ranges must be built from this record rather than from the point path.**

The one driver the method OVER-forecasts is **depreciation**, at +0.499, and it is worse
than freezing by 402%. The reason is this company's own capital programme: spend lands in
projects under construction and stays there for years — EGP 866mn at FY2022 becoming EGP
5,694mn at FY2024 — so a roll-forward that depreciates capex on arrival charges
depreciation the company has not begun to charge. **The delivered study does not make that
error**; it carries construction separately and charges the terminal for the depreciation
the forecast never charged. The finding is recorded because a future rebuild could easily
make it.

---

## 5 · The macro / company split, and its own check

Every origin re-run three ways. **Baseline** carries no inflation term at all.
**Perfect foresight** escalates price and cost per pack at the realised calendar
inflation. **Knowable at the origin** uses the vintage print the origin could have read,
from `engine/macro_history/EG.json` — **which stops at 2023, so the FY2024 origin has no
knowable leg and is REPORTED AS UNMEASURED rather than filled from a later vintage.**

| driver | baseline bias | perfect-foresight bias | macro share |
|---|---:|---:|---:|
| revenue per pack | −0.352 | −0.111 | **68.3%** |
| cost per pack | −0.341 | −0.101 | 70.5% |
| revenue | −0.310 | −0.130 | 58.2% |
| gross profit | −0.331 | −0.150 | 54.5% |
| net profit | −0.553 | −0.378 | 31.7% |
| interest-bearing debt | −0.415 | −0.207 | 50.1% |
| **packs produced** | **+0.044** | **+0.044** | **0.0%** |

**THE SPLIT'S OWN PRE-REGISTERED CHECK PASSES.** The volume driver carries no inflation
term in any leg and returns a macro share of exactly zero, to the last decimal place the
computation holds.

**Most of this method's error on this name is macro and it is one-directional.** Two
thirds of the price miss disappears if the forecaster knows the inflation that actually
arrived. That is not an excuse — the forecaster never knows it — but it says where the
error lives, and both of the study's price-side inputs come from the house macro path.

---

## 6 · Corrections — NONE ADOPTED, and the reason is arithmetic rather than judgement

Every candidate was dispositioned through the HOUSE cut instrument
(`engine/valuation_calibration/boundary_sensitivity.cuts_for`), imported by path rather
than reimplemented, so the arithmetic this record reports and the arithmetic a gate
re-runs are one arithmetic [R-ENF-03].

| driver | n | bias | admissible cuts | flips | disposition |
|---|---:|---:|---:|---:|---|
| packs produced | 9 | +0.044 | 0 | 0 | **DECLINED — untestable** |
| revenue per pack | 9 | −0.352 | 0 | 0 | **DECLINED — untestable** |
| cost per pack | 9 | −0.341 | 0 | 0 | **DECLINED — untestable** |
| capex | 9 | −0.733 | 0 | 0 | **DECLINED — untestable** |
| finance cost | 9 | −0.572 | 0 | 0 | **DECLINED — untestable** |
| depreciation | 9 | +0.499 | 0 | 0 | **DECLINED — untestable** |
| associates + interest income | 12 | −0.550 | 1 | **1** | **DECLINED — the sign flips** |
| revenue, cost of sales, gross profit, charges, profit before tax, net profit, debt | 12 | — | 1 | 0 | **NOT CANDIDATES — aggregates** |

**A LIGHT RUN CANNOT PRODUCE A CORRECTABLE DRIVER ON THIS DESIGN, AND THAT IS A FINDING
ABOUT THE SCOPE RULE RATHER THAN ABOUT THIS COMPANY.** Five origins at horizons one to
three give nine cells on any driver whose earliest origin lacks it. The cut-invariance
clause [R-FCAL-01 AMENDED 07-09-2026] needs a boundary leaving five cells on each side,
which needs ten. **Every primitive driver in this run falls one cell short of being
testable at all**, and untestable is never counted stable — an absence of contrary
evidence is not evidence [R-ENF-04].

The one non-aggregate driver with twelve cells, the associates-and-interest-income block,
**flips sign at the single cut it admits** and is declined on the clause's plain terms.

**The expanding-window rule was run anyway, at every origin, and applied nothing** — at
each origin the window it may see is shorter still, so no cut is admissible there either.
The adjusted-versus-raw test therefore reports the identical figure on both sides (revenue
MAE 0.315 raw and 0.315 adjusted over nine rebuilt cells), which is the correct output of a
rule that correctly declined to fire.

**The second clause was not reached and is stated anyway**, so the next run does not
rediscover it: a half-strength shift bolted onto EIPICO's price line would be a per-name
escalator nothing else in this book carries, while every other Egyptian study escalates a
domestic price line on the house ladder. That is precisely the inconsistency the second
clause exists to catch.

**No watch flags.** A watch flag records a bias that passed the first clause and failed
the second; nothing here passed the first.

---

## 7 · The far-year ranges this record supports, and the two it does not

Published in `forward_ranges.json` with **BASIS, COUNT and ORIENTATION declared on every
cell** [R-FCAL-01 AMENDED 07-09-2026]. Orientation is **actual over forecast**: multiply a
point projection by these to get the outturn range.

| | h1 (n=5) | h2 (n=4) | h3 (n=3) |
|---|---|---|---|
| revenue | 0.95 – 1.25 | 1.21 – 1.72 | 1.73 – 2.02 |
| gross profit | 0.93 – 1.34 | 1.19 – 1.85 | 1.83 – 2.13 |
| net profit | 1.10 – 2.44 | 1.35 – 2.57 | 1.72 – 3.41 |

**THE BASIS IS A SPAN AND NOT A PERCENTILE, at every cell.** The largest count is five. A
span over five observations is the range of five numbers, and calling it a p10–p90 would
be the free parameter the promotion rule forbids.

**HORIZONS FOUR AND FIVE HAVE NO BAND AT ALL.** The run is LIGHT and tests one to three
years, so the delivered study's forecast years four and five carry no measured range from
this record. The study says so in those words rather than stretching the three-year band
over five.

---

## 8 · Guidance, scored and not consumed

No forward statement from any EIPICO annual report enters any rule in this run [L-012].
Two are gradeable against outcomes and both were consumed by nothing:

- **Capacity and utilisation.** The FY2025 indicator table publishes available capacity
  and achieved utilisation by pharmaceutical form (tablets 67% of 1,900mn, antibiotic
  capsules 84% of 270mn, and so on). Utilisation is a fact rather than a target and is
  disclosed after the event; there is nothing to grade.
- **The biosimilars plant.** The company has published **no** volume, price or utilisation
  guidance for EIPICO 3 in any of the seven annual reports. That absence is the reason the
  delivered study charges the plant's depreciation and interest and books no revenue
  against it — a one-sided treatment of an undisclosed quantity, correctly, and the study
  publishes the reverse read instead.

There is nothing here to inherit a lean from, which is a fact about this issuer's
disclosure rather than a virtue of the method.

---

## 9 · Caveats, stated plainly

- **Twelve cells per driver, five origins, one company.** The fifth origin contributes one
  cell. Nothing here is validated; every lesson it produces is PROVISIONAL.
- **Nine cells on every primitive driver, one short of testable.** See §6. It is the
  binding constraint on this run and it is a property of the LIGHT scope.
- **The FY2020 origin is impoverished and is kept with the gap flagged.** The condensed
  COVID-year edition carries no packs figure, no consolidated depreciation and no
  consolidated capex, so its revenue build drops to the parent's own local and export
  sales values and two items of its valuation-input block are recorded as MISSING with
  their reason.
- **The knowable-inflation leg is unmeasured at the FY2024 origin**, because the
  point-in-time archive stops at 2023.
- **The cells are not independent.** Overlapping horizons share forecast years, which is
  what the block bootstrap over origins respects and does not remove.
- **The window contains one devaluation sequence and one capital programme**, and the
  errors measure both rather than controlling for them.

---

## 10 · What would overturn this

- A pre-2019 EIPICO filing surfacing, which would lengthen the window, could turn LIGHT
  into FULL, and would give the primitive drivers their tenth cell.
- A point-in-time inflation vintage for 2024 reaching `engine/macro_history/EG.json`.
- The company restating any year inside the window; eight re-presentations already sit in
  the panel and one of them moves a KPI this run scores.
- A second pharmaceutical manufacturer showing the opposite price/volume decomposition,
  which would confine §3's finding to this name.
