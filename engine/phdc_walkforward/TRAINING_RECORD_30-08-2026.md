# PHDC — fundamental walk-forward training record

**Palm Hills Developments · EGX:PHDC · market EG · exchange EGX · 30 August 2026**

Training record only. **Nothing here is published, nothing reaches the live
site, and there is no rating, target or recommendation anywhere in it.** The
output is a measured record of how this repository's fundamental method would
have performed on this company's own history, and a small set of driver
corrections that were tested rather than asserted.

Companion files: `PRE_REGISTRATION_30-08-2026.md` (written before any error was
computed), `BASIS_BREAKS_30-08-2026.md`, `phdc_IS_projected_vs_actual_all_origins.md`,
and the machine-readable `panel.json`, `error_cells.json`, `scores.json`,
`corrections_log.json`, `forward_ranges.json`, `diagnostics.json`.

---

## 1 · What the record says, in five lines

1. **The bottom-up build forecasts revenue respectably and net profit terribly.**
   Revenue: bias +0.11 log, MAE 0.43, beating both naive benchmarks from two
   years out (skill +0.62 vs freeze and +0.70 vs trend at five years). Net
   profit: bias **+1.12 log — over-forecast by about 3x — in 97% of cells**,
   robust across every bootstrap block, and **worse than simply freezing last
   year's number at every one of the five horizons**.
2. **About 80% of the revenue miss is the company, not the currency.** Running
   every origin twice, once on the inflation path knowable there and once with
   perfect foresight, the macro share of the revenue error is 21.5%. That was
   the finding most at risk of being an artefact of four devaluations, and it
   is not one.
3. **The profit failure is operating leverage on a gross-profit miss, not a
   broken bridge.** Replace every projected driver with its realised value and
   the arithmetic still misses by 0.13 log — so the bridge is roughly right.
   Gross profit alone accounts for +0.45 of the 1.12 error.
4. **Only one correction passed its own test, and it is still not promoted.**
   The finance-cost correction cut that driver's MAE from 0.85 to 0.40. It fails
   the second clause — consistency with the driver class across the market's
   book — because the EG studies build interest from a named facility-by-facility
   debt schedule, and what this record actually measured was the bias of a
   *degraded* implementation. The right answer is a specification fix, not a
   correction factor.
5. **Years 3-5 cannot honestly be published as points.** At five years the
   record's own 10th-to-90th spread on revenue is 83,620 to 214,090 EGP mn.
   That is what ten origins support.

## 2 · Data obtained, and where it stops

| | |
|---|---|
| span targeted | 15 complete fiscal years |
| span obtained, core drivers | **FY2011 – FY2024** (units sold, new sales, ASP) |
| span obtained, full IS/BS | **FY2014 – FY2025** |
| current-year quarters | 1Q2026 (statements and results release) |
| primary documents | **88** — 44 consolidated financial statements, 44 results releases, 1Q2015 to 1Q2026 |
| records in the panel | 551 · **479 tier A**, 72 tier C |

Every reported historical is **tier A**: the company's own filed statements and
its own results releases, from its own investor-relations result centre. The
only tier-C content is the exogenous macro (Egyptian CPI, EGP/USD, urban
population, World Bank WDI), which is a forecast input and never a source for
the company's own reported figures. **Nothing was interpolated.** Where a year
could not be sourced for a field it has no record, and the gap is visible.

**Why the span stops where it does.** The company's result centre publishes from
1Q2015; nothing earlier exists there. FY2011–FY2013 are therefore carried at the
headline level only, from the five-year chart series inside the FY2015 release —
a company document, so still tier A, but it carries revenue, EBITDA, net profit,
gross and net sales and units sold, not a full statement. **FY2025 operating
drivers do not exist in any published document**: the result centre holds the
FY2025 consolidated statements but no FY2025 results release, and it is the
release that carries units and new sales. So units sold stop at FY2023 and new
sales at FY2024 even though revenue runs to FY2025.

Three provenance facts worth stating plainly:

* **FY2022's filed statements are published in Arabic only.** FY2022 is taken
  from the comparative column of the FY2023 filing — same auditor, same
  statements, one year later — and every FY2022 record says so.
* **Several filings embed a font whose character map is wrong.** The FY2015 page
  *renders* revenue of 3 560 584 644 and its text layer *extracts*
  1 654 670 500 — right positions, wrong glyphs, and nothing about the
  extraction looks broken. Every statement is therefore accepted only if it
  **foots against its own arithmetic**; a page that does not foot is re-read by
  OCR off the rendered pixels. All eleven filed years foot.
* **The releases and the filings disagree in places, and the disagreements are
  kept.** FY2023 revenue is 17,462.1 in the filing and 17,454.6 in the following
  release. FY2016 new sales were first reported at 8,194 and later at 8,467.
  Each origin uses the as-first-reported figure; the restatements sit beside it.

## 3 · The record, driver by driver

All horizons pooled, as-known macro. **Bias** and **MAE** are mean and mean
absolute log error. **ROBUST** means the bias keeps its sign across bootstrap
block lengths {2,3,4}.

| driver | n | bias | MAE | share over | robust |
|---|---|---|---|---|---|
| units sold | 30 | −0.215 | 0.340 | 27% | **yes** |
| ASP per unit | 30 | +0.041 | 0.271 | 57% | no |
| new sales | 35 | −0.369 | 0.480 | 34% | **yes** |
| revenue | 35 | +0.105 | 0.425 | 63% | no |
| cost of revenue | 40 | −0.241 | 0.476 | 33% | no |
| gross profit | 35 | **+0.540** | 0.624 | 86% | **yes** |
| units delivered | 30 | +0.294 | 0.427 | 73% | no |
| SG&A | 35 | −0.079 | 0.366 | 54% | no |
| D&A | 39 | +0.586 | 1.112 | 77% | **yes** |
| finance cost | 32 | **−1.074** | 1.076 | 3% | **yes** |
| profit before tax | 31 | +1.098 | 1.108 | 97% | **yes** |
| **net profit after tax and MI** | 31 | **+1.116** | 1.117 | 97% | **yes** |

The shape is consistent and it is diagnosable. Volume is **under**-forecast
(the exogenous population anchor cannot see a launch calendar), cost is
**under**-forecast, and the two do not cancel — gross profit comes out **86%
over**, and net profit, a residual of an order of magnitude smaller than either
side, comes out three times too high.

### Skill against the naive benchmarks

| horizon | revenue vs freeze | revenue vs trend | net profit vs freeze | net profit vs trend |
|---|---|---|---|---|
| 1 | +0.118 | −0.063 | **−3.827** | **−4.034** |
| 2 | +0.221 | +0.208 | −1.705 | −1.747 |
| 3 | +0.153 | +0.377 | −1.459 | −0.904 |
| 4 | +0.307 | +0.543 | −1.225 | −0.221 |
| 5 | **+0.620** | **+0.703** | −0.138 | +0.246 |

Read this honestly. At one year the bottom-up revenue build is **worse than a
three-year trend line**, and only pulls ahead from two years out — which is
where a trend extrapolation starts compounding its own error, so some of that
gain is the benchmark decaying rather than the model improving. On net profit
the build loses to **freezing last year's number at all five horizons**, and to
the trend line at four of five. A method that cannot beat "no change" on its own
bottom line has not earned the authority its precision implies.

## 4 · Macro versus company

Every origin was run twice, exactly as pre-registered. The perfect-foresight
error is the company error; the gap is macro.

| driver | as-known MAE | perfect-foresight MAE | macro share |
|---|---|---|---|
| revenue | 0.425 | 0.334 | **21.5%** |
| cost of revenue | 0.476 | 0.379 | 20.4% |
| ASP | 0.271 | 0.215 | 20.4% |
| new sales | 0.480 | 0.401 | 16.4% |
| SG&A | 0.366 | 0.298 | 18.6% |
| gross profit | 0.624 | 0.578 | 7.4% |
| net profit | 1.117 | 1.074 | 3.9% |
| units sold, units delivered, finance cost | — | — | **0.0%** |

Units and deliveries carry **no** macro share by construction — they are
volume drivers with no inflation term — which is the check that the split is
measuring what it claims to. Four devaluations across the window explain about
a fifth of the revenue miss and almost none of the profit miss.

## 5 · Where the net-profit error actually comes from

Replacing **one** projected driver at a time with its realised value, and
measuring how much absolute log error disappears:

| substitute in the actual… | n | error removed (of 1.117) |
|---|---|---|
| gross profit | 29 | **+0.454** |
| finance cost | 27 | +0.034 |
| D&A | 31 | −0.063 |
| SG&A | 31 | −0.085 |
| **every driver at once** | 27 | leaves **0.130** |

Two things follow. First, **the bridge is sound**: with all four drivers right,
net profit lands within 13%. Second, the substitutions do not sum to the total
(+0.34 against a gap of 0.99), so the drivers interact strongly — which is what
operating leverage on a thin residual looks like, and it means single-driver
attribution understates how much of the profit error is really the gross-profit
error.

**Root cause, stated as a defect rather than a curiosity.** The projection
recognises **revenue** on `δ × (opening backlog + new sales)` but recognises
**cost** on `cost per unit × units delivered`. Since January 2016 the company
recognises standalone-unit revenue on percentage of completion (basis break B1),
so revenue accrues with construction while the model's costs accrue with
handover. The two legs are on different clocks. That is a specification error,
not a calibration one, and no bias correction should be allowed to hide it.

## 6 · Corrections: what was tested, and what passed

The rule was fixed in advance — expanding window, half strength, applied only
where the bias holds its sign across eras, reset after a two-sigma break.

**Corrections only became eligible at origin FY2023.** Era-sign-stability needs
two eras each carrying two or more *resolved* errors, and the devaluation era
does not accumulate that until FY2023. Seven of the ten origins therefore carry
no correction at all — not because nothing was biased, but because nothing had
yet been demonstrated stable. That is the rule working, and it is also the
sharpest limit of a single-name study.

| driver | bias at FY2024 | applied | outcome |
|---|---|---|---|
| finance cost | −0.889 | −0.445 | **MAE 0.848 → 0.403 (−0.445)** |
| units sold | −0.215 | −0.108 | **no resolved cells** — FY2024-25 units are not disclosed, so the correction cannot be scored |
| ASP | +0.041 | 0 | sign not stable across eras |
| units delivered | +0.295 | 0 | sign not stable across eras |
| SG&A | +0.124 | 0 | sign not stable across eras |

Rebuilding the aggregates from the adjusted drivers:

| aggregate | n | raw MAE | adjusted MAE | change |
|---|---|---|---|---|
| finance cost | 3 | 0.848 | 0.403 | **−0.445** |
| new sales | 1 | 0.752 | 0.732 | −0.019 |
| revenue | 3 | 0.058 | 0.080 | +0.022 |
| cost of revenue | 3 | 0.519 | 0.646 | +0.128 |
| gross profit | 3 | 0.590 | 0.678 | +0.089 |
| net profit | 3 | 1.229 | 1.306 | +0.077 |

By origin: FY2023 +0.006 (no better), FY2024 −0.039 (better). **Two origins and
at most seventeen cells is not evidence of anything at the aggregate level**,
and it is reported as such rather than dressed up.

### What is promoted, and what is not

**Nothing is promoted into the live drivers.** The pre-registration requires a
correction to pass *both* the test here *and* consistency with the same driver
class across the market's book. The finance-cost correction passes the first
and fails the second: the EG studies in this repository build interest from a
named facility-by-facility debt schedule (ARCC carries CIB, NBE and EBRD
tranches each at its own cost of debt), whereas this exercise's D9 was
implemented as a ratio of finance cost to opening total current liabilities —
a **stated deviation from the pre-registration**, forced because the scanned
filings' individual debt lines do not resolve across the whole window. So the
−0.89 bias is largely the bias of the wrong base, and correcting it would be
calibrating a mis-specification.

**Carried into the update as changes to method, not as factors:**

1. **Build interest from the disclosed debt schedule**, per the EG book's own
   convention — not from a liabilities ratio.
2. **Put revenue and cost on the same recognition clock.** Cost must accrue with
   percentage of completion where revenue does, from FY2016 on.
3. **Publish years 3-5 as ranges** from §8's distribution, never as points.

**Recorded as watch flags** — graded live, revisited at the next update, acted
on by nobody in the meantime: the units-sold under-forecast (robust, −0.215),
the gross-profit over-forecast (robust, +0.540), and the D&A over-forecast
(robust, +0.586).

## 7 · Guidance ledger

Nineteen statements referencing a management target were found in the releases.
**Two different things get called guidance here, and pooling them would flatter
the record**: a target a release quotes *retrospectively* (which it only tends
to do when the target was beaten) and a *forward* target for a year not yet run.
Only the second is a forecast.

| for FY | metric | kind | target | actual | gap | outcome |
|---|---|---|---|---|---|---|
| 2016 | units delivered | referenced | 1,800 | 2,049 | +13.8% | beaten |
| 2017 | units delivered | referenced | 1,600 | 1,781 | +11.3% | beaten |
| 2018 | units delivered | referenced | 1,500 | 1,541 | +2.7% | beaten |
| 2020 | new sales, EGP mn | referenced | 12,000 | 12,779 | +6.5% | beaten |
| **2019** | units delivered | **forward** | 1,350 | 964 | **−28.6%** | **missed** |
| **2021** | units delivered | **forward** | 1,450 | 1,308 | **−9.8%** | **missed** |

**Referenced targets: 4 of 4 beaten, mean log error −0.082. Forward targets: 2
of 2 missed, mean log error +0.220** — management over-forecast its own
handovers by about 25% on the only two occasions this archive lets us score a
target *before* the outcome was known.

That is a small sample and it is stated as one. But the direction matters for
this exercise: the model's own delivery bias is **+0.294**, also an
over-forecast, and management's forward guidance leans the same way. A driver
that took company guidance as an input would inherit that lean rather than
correct for it. Guidance is scored here and is never used as a driver at a
historical origin.

## 8 · What the update should carry forward

From origin FY2025, with the volume anchor two years stale (units sold last
disclosed FY2023, new sales FY2024 — the lag is recorded on every cell), and
ranges built from this record's own error distribution at each horizon:

| EGP mn | FY2026 | FY2027 | FY2028 | FY2029 | FY2030 |
|---|---|---|---|---|---|
| revenue, central | 34,006 | 49,326 | 55,971 | 73,575 | 93,927 |
| revenue, 10th–90th | 21,479–46,083 | 25,990–79,131 | 32,614–136,914 | 46,856–205,806 | 83,620–214,090 |
| net profit, central | 3,189 | 4,462 | 6,877 | 8,898 | 12,393 |
| net profit, 10th–90th | 2,583–4,278 | 3,617–7,999 | 4,766–13,575 | 6,481–18,145 | 10,028–33,474 |
| resolved errors behind the range | 9 | 8 | 7 | 6 | 5 |

The last row is the important one. A FY2030 range resting on **five** resolved
observations is a statement about how little is known, and the width is the
honest expression of it.

## 9 · Caveats, stated plainly

* **One name, ten origins, three macro eras.** Block-bootstrap intervals are
  wide and are reported wide. Several of them straddle zero, and where they do
  the bias is reported as not robust rather than as a small effect.
* **Overlapping horizons.** The rolling record's cells are not independent. The
  non-overlapping confirmation set the pre-registration named ({2015, 2020} and
  its shifts) is too thin to confirm anything, and no attempt was made to
  present it as if it were.
* **Corrections rest on two origins.** Everything in §6 beyond the finance-cost
  result is directional at best.
* **A stated deviation from the pre-registration.** D9's interest base is
  opening total current liabilities, not opening gross debt, because the panel
  does not carry a complete gross-debt series across the window. This is
  disclosed rather than papered over, and it materially affects the finance-cost
  result specifically.
* **A stated extension.** Where a driver's base year is not disclosed at the
  origin (FY2025 units and new sales), the rule was extended, uniformly and in
  advance of scoring, to the most recent year that does disclose it, with the
  lag recorded. Re-scoring the whole record under this extension moved revenue
  MAE from 0.436 to 0.425 and left every other driver essentially unchanged, so
  it is a coverage fix rather than a tuning choice.
* **A rejected shortcut, recorded.** Summing the disclosed regional unit series
  to recover FY2024's missing company total was tried and **rejected on its own
  evidence**: on the four years where the total *is* disclosed the sum overstates
  it by about a third, because the regional charts overlap. FY2024 and FY2025
  units sold therefore have no entry at all rather than an inferred one.
* **A perimeter change with no chain factor.** The FY2024 acquisitions (Taaleem
  32.6%, Macor to 69.5%, Novotel October 20%) added education and hospitality
  verticals, and the company publishes no restated pre-acquisition series, so
  FY2024–FY2025 aggregate errors carry that flag and should not be read purely
  as forecasting misses.

## 10 · Reproducing this

```
python3 fetch_sources.py     # the company's own IR register, all 88 documents
python3 extract_text.py      # text layer; OCR where the scan has none
python3 build_panel.py       # statements, each accepted only if it foots
python3 panel.py             # four-field panel + cross-checks + reconciliation
python3 bottom_up.py         # the projection at any origin
python3 score.py             # the record, bootstrap, macro split, eras
python3 diagnose.py          # decomposition, per-origin statements, guidance
python3 corrections.py       # expanding-window corrections and their test
python3 forward.py           # the ranges the update carries
```
