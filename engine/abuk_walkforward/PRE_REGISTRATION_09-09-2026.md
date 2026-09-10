# ABUK — FUNDAMENTAL WALK-FORWARD, PRE-REGISTRATION

**Written 09-09-2026, BEFORE a single error was computed.** [R-FCAL-01] §2.
Internal. Never shown to a reader.

Abu Qir Fertilizers and Chemical Industries Company (S.A.E.), EGX:ABUK.CA.
Campaign entry #11, EGX block, tier `first-build`.

**WHICH WALK-FORWARD THIS IS.** The FUNDAMENTAL one: drivers projected from a
past origin and scored against what the company actually reported. Not the
price-engine walk-forward (band coverage on the Monte Carlo cone), and not the
technical walk-forward (the shipped read replayed on a 5/10/21-session clock).

---

## 0 · Scope decision, made first

**FULL.** Eleven complete fiscal years are sourceable under §1 — FY-Jun-2015 to
FY-Jun-2025 — which is above the eight-year threshold. Origins therefore run
from the first year with five years of history behind it, at horizons 1 to 5.

**Origins: FY2019, FY2020, FY2021, FY2022, FY2023, FY2024.** Horizons 1..5,
truncated by the last annual actual (FY2025): 5+5+4+3+2+1 = **20 scoreable
cells per driver**.

FY2019 is the first origin because FY2015..FY2019 is the first five-year window.
FY2025 is the last actual because the company then changed its year end from 30
June to 31 December and filed an audited SIX-MONTH transitional period; a
six-month stub is not an annual actual and is excluded from scoring rather than
annualised.

---

## 1 · Drivers, by class, and the MECHANICAL rule for each

No judgement drivers at historical origins. Every rule below is a formula over
information published on or before the origin's own filing date. Parameters are
STATED, never fitted. Where a rule uses a trailing mean or CAGR the window is
three fiscal years ending at the origin unless stated.

| # | driver | class | mechanical rule at origin *o*, horizon *h* |
|---|---|---|---|
| D1 | volume proxy `v` | volume | `v(o+h) = min( v(o) x (1+g)^h , max v over the 5 years to o )` where `g` = Egypt population CAGR over the five calendar years ending at *o* (World Bank SP.POP.TOTL, tier C, exogenous, dated at *o*) |
| D2 | world urea price, USD/t | price / macro | held FLAT at the FY-*o* average (random walk — the standard no-arbitrage forecast for a traded commodity, and the only thing knowable at the origin) |
| D3 | EGP per USD | price / macro | held FLAT at the FY-*o* average |
| D4 | cost-of-sales ratio | cost per unit | trailing three-year mean of `cogs/revenue` to *o*, held flat across the horizon |
| D5 | selling & distribution ratio | variable overhead | trailing three-year mean of `sell/revenue` to *o*, held flat |
| D6 | general & administrative | fixed overhead | `admin(o) x (1+pi)^h`, `pi` = trailing three-year mean Egypt CPI inflation to *o* |
| D7 | non-operating income block | financial | `y(o) x B(o) x (1+pi)^h`, `y` = trailing three-year mean of the block divided by the INVESTABLE BALANCE, `B` = cash at banks + investments held to maturity / at amortised cost at *o* |
| D8 | effective tax rate | tax | trailing three-year mean of `tax/pbt` to *o*, held flat |

**Revenue** `= D1 x D2 x D3` — an OUTPUT of a volume driver and two price
drivers, never a growth rate on itself.
**Cost of sales** `= D4 x revenue`. **Gross profit is an OUTPUT** [L-005]:
no margin is typed anywhere in this model.
**Profit before tax** `= gross profit - D5 x revenue - D6 + D7`.
**Tax** `= D8 x pbt`. **Net profit is an OUTPUT.**

### Why the volume driver is a proxy and what that costs

ABUK discloses no per-product tonnage anywhere. That was searched for
explicitly across the earnings releases, the EGX financial-indicator filings and
the audited statements, and the result is recorded as a negative: total volumes
appear only as bar-chart captions whose labels do not reconcile with the same
release's own narrative. The finest sourceable physical driver is therefore
revenue deflated by the world urea price and the exchange rate, which is a
volume-times-realisation composite rather than a tonnage. **This is stated in
the study, and it means D1's error carries realisation drift that a disclosed
tonnage would have separated out.**

### The two named traps, and what each becomes on this name

1. **Interest comes from the borrowings that actually bear it.** ABUK is the
   mirror image of the case the rule was written from: it discloses "no loans at
   the reporting date" and carried EGP 45,506 of borrowings at FY-Jun-2021. The
   trap here runs the other way — a yield built on TOTAL ASSETS rather than on
   the balances that actually earn. D7 therefore divides by cash at banks plus
   investments held to maturity or at amortised cost, and by nothing else.
2. **Revenue and cost on the same recognition clock.** ABUK recognises revenue
   at the point of sale and cost of sales against the same tonnes in the same
   period; there is no percentage-of-completion anywhere in its accounting
   policy note. The trap does not arise, and the model carries no construction
   that could create it: D4 is a ratio ON THE SAME PERIOD'S revenue.

---

## 2 · Both naive benchmarks

- **FREEZE** — every line flat at the FY-*o* actual, at every horizon.
- **TREND** — every line grown at its own trailing three-year CAGR to *o*.

Reported at every horizon, per driver and on revenue and net profit.

---

## 3 · The score

Log error `e = ln(projected / actual)` per driver per horizon. Reported per
driver: **bias** (mean e), **MAE** (mean |e|), **share over-forecast**, **sign
by era**, and a **block bootstrap over ORIGINS** — 5,000 resamples, the block
being a whole origin with all its horizons, so overlapping horizons cannot be
counted as independent evidence.

Eras: **pre-spike FY2019-FY2021** and **spike and after FY2022-FY2025**. A bias
that changes sign between them is reported as instability and is NOT corrected
for.

---

## 4 · Macro / company conditioning, and the split's own check

Exogenous, and held at their origin values in the base run: world urea price
(World Bank CMO monthly, tier C), EGP per USD (World Bank WDI, tier C), Egypt
CPI (World Bank WDI, tier C), Egypt population (World Bank WDI, tier C). The
regulatory regime known at the origin — the gas price formula, the export-duty
regime and the 22.5% statutory tax rate — is exogenous and is not forecast.

Every origin is re-run twice more:

- **MACRO-PERFECT** — the ACTUAL urea, FX and CPI path substituted, every
  company driver left exactly as the origin projected it. The change in error
  is the MACRO share.
- **FULL FORESIGHT** — actual macro AND actual company ratios. The residual is
  the COMPANY share.

**The split's own check:** D1 carries no inflation, FX or urea term by
construction, so its macro share must come back **exactly zero**. If it does
not, the split is wired wrong and the diagnosis is void.

---

## 5 · The two samples

The **rolling record** (all six origins, overlapping horizons) estimates any
correction. The **non-overlapping origins** (FY2019, FY2024 — the only pair
whose horizon sets do not intersect at h=1) confirm it. With six origins the
confirmation sample is small and that limit is stated rather than worked around.

---

## 6 · Corrections — the rule, fixed before any result

Expanding window only. Half strength by default. Applied ONLY where the bias
holds its sign across BOTH eras. Reset after a structural break, defined as a
driver error beyond its own two-sigma. Aggregates rebuilt from adjusted drivers
and tested adjusted-against-raw by origin.

A correction enters the live drivers only if it passes that test **and** is
consistent with how that driver class is built across the market's book.
Otherwise it is a **watch flag** — recorded, graded live, acted on by nobody.

Management guidance is SCORED and never consumed as an input. ABUK publishes a
single-page statutory planned budget and no multi-year guidance; the FY2026
budget is in the ledger and is graded, not used.

---

## 7 · What already binds on this name

Read before any driver was set: `python3 engine/lessons.py ABUK --class petrochemical`
returns 258 lessons — 257 at ALL scope, one at CLASS `petrochemical` (L-109, a
forecast year must be producible from the disclosed half-year), and none at
STOCK scope for ABUK. Everything marked PROVISIONAL is a recorded finding from a
method that is not yet validated; they were read to think with and none is cited
as authority.

**The class is provisionally recorded as `petrochemical`** because it is the
nearest registered class. It is a poor fit and that is stated: ABUK's feedstock
price is contractually linked BY FORMULA to the export price of its own output
and to USD/EGP, with a regulatory floor underneath — which makes it neither a
petrochemical producer whose input and output prices move independently, nor the
thin-spread refiner AMOC was separated out as. Whether it earns its own class is
a scope question for the user at Step 10, not a decision this run makes.

---

## 8 · What is NOT tested here, stated in advance

- The transitional six-month period and the 2026 calendar periods: not annual
  actuals, excluded from scoring, carried in the basis-break register.
- Segment-level drivers: plant-level revenue is disclosed for FY2019-FY2020 and
  FY2024-2026 but not for FY2021-FY2023, so there is no continuous segment
  series and the run does not pretend to one.
- Depreciation and capex as SCORED drivers: they are committed in the
  valuation-input block per origin but they do not enter the profit build, which
  is anchored on the disclosed cost-of-sales ratio.
