# ABUK — FUNDAMENTAL WALK-FORWARD, TRAINING RECORD

**09-09-2026. INTERNAL — never shown to a reader.** [R-FCAL-01].

Abu Qir Fertilizers and Chemical Industries Company (S.A.E.), EGX:ABUK.CA.
Campaign entry #11, EGX block, tier `first-build`.

**WHICH WALK-FORWARD THIS IS.** The FUNDAMENTAL one — drivers projected from a
past origin and scored against what the company actually reported. Not the
price-engine walk-forward on the Monte Carlo cone, and not the technical
walk-forward on the shipped read.

---

## 1 · Scope, decided first

**FULL.** Eleven complete fiscal years are sourceable — FY-Jun-2015 to
FY-Jun-2025 — above the eight-year threshold.

**Origins FY2019, FY2020, FY2021, FY2022, FY2023, FY2024, horizons 1-5,
truncated by the last annual actual: 20 scoreable cells per driver.**

### The span obtained, and why it stops where it stops

It stops at FY-Jun-2025 because that is the last COMPLETE twelve-month fiscal
year the company reported. It then moved its year end from 30 June to 31
December and filed an audited SIX-MONTH transitional period; a half-year is not
an annual actual and is excluded from scoring rather than annualised.

It stops at FY-Jun-2015 because the FY-Jun-2016 audited statements are the
oldest annual filing recoverable anywhere, and FY2015 is their comparative
column. No FY-Jun-2014 or earlier annual filing exists on abuqir.net, in the
Internet Archive's capture of the old site, or through the exchange.

### The provenance, and one thing about it that matters

Every one of the eleven years is tier A, off the issuer's own audited
statements. But the company rebuilt its website in November 2025 and its live
shelf now begins at the quarter ended 30-Sep-2023, so **FY2015-FY2022 came from
the Internet Archive's capture of the old abuqir.net investor shelf.** The
documents are the company's own audited statements; the retrieval route is an
archive, and that is recorded on every figure.

Those eight filings are **pure scans in Arabic with Eastern-Arabic numerals and
zero characters of text layer.** Tesseract's Arabic model runs minutes per page
on them and mangles the digits, so **every figure was read off the rendered
pixels at 400 dpi and accepted only where the statement foots against its own
arithmetic.** Residuals that do not foot are recorded and not repaired. Eight of
the eleven years appear twice — once as their own year, once as the following
year's comparative in a separately filed document — and where both were read
they agree to the pound.

---

## 2 · THE SKILL VERDICT, first because it is the finding

| aggregate | model MAE | freeze MAE | trend MAE | verdict |
|---|---:|---:|---:|---|
| revenue | 0.497 | 0.530 | 0.427 | beats freeze, **loses to trend** |
| gross profit | 0.711 | 0.711 | 0.638 | **ties freeze**, loses to trend |
| profit before tax | 0.776 | 0.832 | 0.763 | beats freeze, **loses to trend** |
| net profit | 0.773 | 0.829 | 0.724 | beats freeze, **loses to trend** |

**The method beats "no change" on every aggregate and it loses to a trailing
three-year growth rate on every one of them.** It is not enough to have earned
the precision a point forecast displays, and the study built on this run
publishes years 3-5 as ranges for exactly that reason.

By horizon, the pattern is sharper than the aggregate: the model beats BOTH
benchmarks on revenue at h=1 and h=2 and on net profit at h=2, and loses to
trend at every horizon from three years out. **The ground-up build is worth
having for one and two years and is not yet worth having for three to five.**

| | h=1 | h=2 | h=3 | h=4 | h=5 |
|---|---|---|---|---|---|
| revenue, model | 0.239 | 0.338 | 0.637 | 0.853 | 0.857 |
| revenue, freeze | 0.244 | 0.367 | 0.683 | 0.911 | 0.918 |
| revenue, trend | 0.254 | 0.550 | 0.441 | 0.451 | 0.575 |
| net profit, model | 0.412 | 0.672 | 0.971 | 1.195 | 1.079 |
| net profit, freeze | 0.369 | 0.701 | 1.020 | 1.360 | 1.348 |
| net profit, trend | 0.508 | 0.935 | 0.883 | 0.619 | 0.683 |
| cells | 6 | 5 | 4 | 3 | 2 |

**Why trend wins at long horizons, stated rather than left to look like a
mystery.** The Egyptian pound went from 17.3 to 47.3 to the dollar across this
window. The pre-registered model holds the exchange rate flat at each origin —
a random walk, which is the only thing knowable at the origin — while the trend
benchmark extrapolates the growth rate that the devaluation itself produced. On
a currency that has devalued in three discrete steps inside six years, a
naive extrapolation of nominal growth is not a better model; it is a bet that
happened to be right, and the diagnosis below prices exactly how much of the
model's loss is that bet.

---

## 3 · Per-driver results

Log error, forecast over actual. Bias positive = over-forecast. The interval is
a block bootstrap over ORIGINS, 5,000 resamples, the block being a whole origin
with all its horizons, so overlapping horizons are not counted as independent.

| driver | n | bias | 90% CI on bias | MAE | over-forecast | freeze MAE | trend MAE | macro share | company share | era stability |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| volume proxy | 20 | +0.225 | [+0.104, +0.327] | 0.269 | 85% | 0.241 | 0.266 | 0% | 100% | same sign |
| revenue | 20 | -0.469 | [-0.640, -0.243] | 0.497 | 15% | 0.530 | 0.427 | 46% | 54% | **SIGN CHANGES** |
| cost of sales | 20 | -0.310 | [-0.422, -0.182] | 0.338 | 20% | 0.433 | 0.382 | -26% | 126% | **SIGN CHANGES** |
| gross profit | 20 | -0.643 | [-0.878, -0.281] | 0.711 | 20% | 0.711 | 0.638 | 65% | 35% | same sign |
| selling & distribution | 20 | -0.458 | [-0.577, -0.326] | 0.474 | 10% | 0.551 | 0.394 | 24% | 76% | **SIGN CHANGES** |
| general & administrative | 20 | -0.559 | [-0.798, -0.285] | 0.646 | 30% | 0.873 | 0.696 | 9% | 0% | **SIGN CHANGES** |
| non-operating income | 20 | -0.612 | [-0.849, -0.288] | 0.845 | 30% | 1.134 | 1.139 | 10% | 90% | **SIGN CHANGES** |
| profit before tax | 20 | -0.695 | [-0.928, -0.346] | 0.776 | 15% | 0.832 | 0.763 | 56% | 42% | same sign |
| net profit | 20 | -0.690 | [-0.922, -0.361] | 0.773 | 15% | 0.829 | 0.724 | 56% | 42% | same sign |

---

## 4 · The macro/company split, and the check it runs on itself

Each origin was re-run twice: once with the ACTUAL urea, exchange-rate and
inflation path substituted and every company driver left as the origin projected
it, and once with actual macro AND actual company ratios.

**56% of the net-profit error is macro** — the pound and the world urea price,
not the company. On gross profit it is 65%.

**THE SPLIT'S OWN CHECK PASSES.** The volume driver carries no inflation, FX or
urea term by construction, so substituting the actual macro path must leave its
error untouched. Its macro share came back **exactly 0.00** to machine
precision. Had it not, the split would have been wired wrong and this whole
section void.

Two readings are worth naming.

**The cost-of-sales driver has a NEGATIVE macro share (-26%).** Substituting the
actual macro path made the cost error WORSE, not better. That is not a paradox:
cost of sales is a ratio applied to revenue, so a revenue forecast that improves
carries a cost forecast that was already mis-set further from the actual. It is
a warning about the specification rather than about the macro path, and it is
why the cost ratio is scored as a driver in its own right and not read off the
gross-profit error.

**The general-and-administrative driver's residual is 91%.** Neither the macro
path nor the company's own ratios explain its error, because it is the only
driver built as a level escalated at inflation rather than as a ratio. Its error
is the specification's, and that is what a 91% residual means.

---

## 5 · Era stability — five of nine drivers are UNSTABLE, not biased

Eras: pre-spike FY2020-FY2021, spike and after FY2022-FY2025.

| driver | bias, pre | bias, post | verdict |
|---|---:|---:|---|
| volume proxy | +0.008 | +0.263 | same sign |
| revenue | +0.006 | -0.552 | **SIGN CHANGES** |
| cost of sales | +0.088 | -0.380 | **SIGN CHANGES** |
| selling & distribution | +0.041 | -0.546 | **SIGN CHANGES** |
| general & administrative | +0.110 | -0.677 | **SIGN CHANGES** |
| non-operating income | +0.310 | -0.775 | **SIGN CHANGES** |
| gross profit | -0.113 | -0.736 | same sign |
| profit before tax | -0.014 | -0.815 | same sign |
| net profit | -0.035 | -0.806 | same sign |

**A bias that changes sign between eras is not a bias.** Five of the nine change
sign, and every one of them is reported as instability and corrected for by
nothing. The three aggregates that hold their sign are aggregates OF the unstable
drivers, so their stability is arithmetic rather than evidence.

The one genuine driver-level survivor is the volume proxy — and its pre-era bias
is +0.008, which is not distinguishable from zero. It passes the letter of the
sign test on an essentially null pre-era observation, and that is said here
rather than allowed to look like two-era confirmation.

---

## 6 · Corrections — four blocked before any test, one proposed, none adopted

**BLOCKED, before a test was run:** cost of sales, selling & distribution,
general & administrative, non-operating income. Each because its bias changes
sign between eras.

**PROPOSED:** the volume proxy alone. Bias +0.225, 90% interval [+0.104, +0.327]
excluding zero, half-strength factor 0.8936.

**TESTED, expanding window, adjusted against raw, by origin:**

| origin | expanding bias | n resolved | factor | driver MAE raw -> adjusted | net profit MAE raw -> adjusted | |
|---|---:|---:|---:|---|---|---|
| FY2019 | — | 0 | — | no resolved history; the raw projection stands | | |
| FY2020 | -0.088 | 1 | 1.0450 | 0.347 -> 0.391 | 1.031 -> 1.002 | better |
| FY2021 | +0.008 | 3 | 0.9959 | 0.347 -> 0.343 | 1.127 -> 1.130 | WORSE |
| FY2022 | +0.229 | 6 | 0.8918 | 0.139 -> 0.208 | 0.460 -> 0.548 | WORSE |
| FY2023 | +0.142 | 10 | 0.9315 | 0.344 -> 0.273 | 0.203 -> 0.204 | WORSE |
| FY2024 | +0.196 | 15 | 0.9066 | 0.092 -> 0.006 | 0.409 -> 0.356 | better |

**It improved net profit at two of five origins tested. It fails its own first
clause and is not adopted.**

**And the second clause would have blocked it anyway, for a reason worth
recording.** EGCH and AMOC both show a flat-volume lean on EGX gas-fed
industrial names — L-206 records urea tonnes held flat over-forecasting by 9.3%,
AMOC +7.6% in eight of nine cells. This looks like the same finding a third
time. **It is not the same object.** EGCH and AMOC measured DISCLOSED TONNES.
ABUK discloses no tonnage anywhere, so this run's volume driver is revenue
deflated by the world urea price and the exchange rate — a volume-times-
realisation composite. Treating a haircut on one as confirmation of a haircut on
the other would be the superstition the register warns about.

**Outcome: no correction adopted. One WATCH FLAG** — the volume proxy
over-forecasts by about 25% on average, 85% of cells over-forecast, and the
question of how much of that is tonnes and how much is realisation is open until
the company discloses tonnage or a fourth name settles it.

**How much of the decline is volume, as far as the disclosure goes.** The
company's earnings-release charts put sales tonnes at roughly 2.18m in FY-Jun-2019
and roughly 1.85m in FY-Jun-2025, about -15%; the deflated proxy fell from 1.904m
to 1.289m, about -32%. So on the company's own (unreliably labelled) charts
roughly half the proxy's decline is tonnes and roughly half is realisation. That
is a reading, not a measurement, and it is why the flag is a flag.

---

## 7 · Guidance ledger — scored, never consumed

ABUK publishes no multi-year guidance at all. A negative search across the
FY-Jun-2025 and H1-2026 earnings releases for 'guidance', 'outlook', 'target'
returns zero hits. What it does publish is a single-page statutory planned
budget.

| period | management's own published forward number | outcome | grade |
|---|---|---|---|
| FY2026 planned budget, filed 31-Jan-2026 | revenue EGP 26,164m, expenses 17,329m, profit before tax 8,835m | H1-2026 ALONE delivered revenue 23,525m and profit before tax 12,658m | **revenue 89.9% of the full-year budget in six months; profit before tax 143% of the full-year budget in six months** |

Anchoring on that budget would have forecast a second half of EGP 2.6bn revenue
against a first half of EGP 23.5bn. **It is carried as evidence of forecast
dispersion for the scenario width and as a driver by nothing.**

The arithmetic settled a disputed digit in the source: the English column of the
filing reads 'Profit before 9936' and the Arabic-numeral column reads 8835;
26,164 - 17,329 = 8,835 exactly, so 8,835 is the figure and 9,936 is a misread.

---

## 8 · The two named traps, and what each turned out to be here

**1 · Interest comes from the borrowings that actually bear it.** ABUK is the
mirror image of the case this rule was written from. It discloses *"the company
has no loans at the reporting date"* in its H1-2026 interest-rate-risk note and
carried EGP 45,506 of borrowings at FY-Jun-2021. **The trap runs the other way
here: a yield built on total assets rather than on the balances that actually
earn.** The non-operating driver therefore divides by cash at banks plus
investments held to maturity or at amortised cost, and by nothing else — the
same balances the finance-income line is actually earned on. Had it divided by
total assets the implied yield would have been understated by roughly a third at
FY2019 and by more later, and the resulting "bias" would have been arithmetic.
**The specification did not break down.**

**2 · Revenue and cost on the same recognition clock.** ABUK recognises revenue
at the point of sale and charges cost of sales against the same tonnes in the
same period. There is no percentage-of-completion anywhere in its accounting
policy note. The trap does not arise on this name, and the model carries no
construction that could create it: the cost driver is a ratio on the SAME
period's revenue. **The specification did not break down.**

---

## 9 · One-offs classified

| year | item | treatment |
|---|---|---|
| FY-Jun-2024 | foreign-exchange gain of EGP 6,748,866,655 — half of that year's net profit | non-recurring, driven by the March-2024 devaluation. The model prices FX inside the non-operating block on the disclosed net position rather than as a revenue multiplier |
| FY-Jun-2022 | the global urea spike, world price averaging USD 714.9/t against USD 287.9 the year before | a market event, not a company one; the split assigns it to macro and the diagnosis shows it |
| FY-Jun-2020 | net fixed assets rose EGP 448.4m against capex of EGP 229.3m | a revaluation or transfer sits inside the movement. It breaks the capex identity, and the depreciation charge for that year is recorded as MISSING with that reason rather than derived from a broken identity |
| FY-Jun-2025 -> Dec-2025 | the six-month transitional period | excluded from scoring, in the basis-break register |
| FY-Jun-2026 (current) | the USD 8.50/mmBtu gas floor, the export duty imposed in May and CANCELLED from 1-Aug-2026 | outside the scored window; dated windows for any forward model, never permanent rates |

---

## 10 · The calibrated ranges this run hands forward

Multiplicative bands on a central forecast, from this record's own measured
error, pooled over horizons 3 to 5 (nine cells).

| | RAW band | MACRO-CONDITIONED band |
|---|---|---|
| revenue | x1.70 to x2.71 | x0.61 to x0.90 |
| gross profit | x2.03 to x3.81 | x0.72 to x1.34 |
| net profit | x2.19 to x4.13 | x0.80 to x1.86 |

**The study must not choose freely between them, and this is the single most
load-bearing sentence in this record.** The RAW band is dominated by the pound:
the model held the exchange rate flat while the currency went from 17.3 to 47.3,
so the raw band says "multiply by two to four" when what it means is "the
currency will devalue again". **A forward model that already carries an explicit
exchange-rate path and then applies the raw band counts the same devaluation
twice.** The macro-conditioned band is the company-only error and is the one a
study with its own FX path must use. The raw band applies only to a model whose
currency assumption is itself a flat random walk.

At h=4 and h=5 the cell counts are 3 and 2. Those bands rest on very few
observations and the study says so beside them.

---

## 11 · Caveats, stated plainly

- **Six origins and twenty cells.** The non-overlapping confirmation sample is
  one pair (FY2019, FY2024). Every finding here is provisional on that.
- **The volume driver is a proxy, not a tonnage.** ABUK discloses no per-product
  physical volume anywhere; that was searched for explicitly and the negative is
  on the record. The proxy conflates volume with realisation and its error
  carries both.
- **No continuous segment series exists.** Plant-level revenue is disclosed for
  FY2019-FY2020 and FY2024-2026 and not for FY2021-FY2023, so this run does not
  build segment drivers and does not pretend to.
- **There is no overlap year across the FY2023 presentation change**, so the
  cost-and-overhead split is two definition windows and no chain factor exists
  between them. Revenue and net profit are chained; the evidence for that is in
  the basis-break register.
- **Eight of eleven years were read off pixels.** Every accepted figure foots
  against its own statement and eight of the eleven are confirmed twice across
  separately filed documents, but this is a lower-quality read than a text layer
  and the residuals that do not foot are listed in the panel rather than
  smoothed.
- **The depreciation charge is DERIVED for four of six origins** and missing with
  a stated reason for one. The fixed-asset notes of the Arabic filings were not
  read.

---

## 12 · One housekeeping fact, recorded rather than left as an absence

The 40 source PDFs this run parsed totalled 145 MB. `engine/*_walkforward/filings/`
is gitignored, so they were never committed; the container's root filesystem
then filled to 100% and they were deleted to free it. **The deletion is provably
lossless.** `fetch_attempts.json` records for every file its exact URL, its byte
count and the first sixteen hex digits of its SHA-256, and `refetch_filings.py`
re-fetches each one and VERIFIES both before accepting it. It was tested on one
file and returned it byte-identical. Run it before re-reading any figure sourced
to a filing.

---

## 13 · What this run did NOT produce

**The delivered valuation study — Document 1 of [R-FCAL-01] §6 — is NOT built.**
The walk-forward, its panel, its scoring, its diagnosis, its corrections test,
its calibrated ranges, its valuation-input block and its disclosed-life record
are complete. The 16-section Word document, the 16-sheet live-formula workbook,
the standalone bibliography and the QC gate are not, and no fair value has been
struck. `fair{bear,base,full}` in `assets/data.js` is UNTOUCHED at the frozen
baseline of 50 / 60 / 72 EGP.

That baseline came from **no current-standard study at all**, so whenever the
movement is finally recorded it will measure a new study against a number of
unknown provenance — not one method against another. That has to be said
wherever the column is quoted.
