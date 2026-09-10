# TRAINING RECORD — SCEM fundamental walk-forward, 07-09-2026

**Sinai Cement Company S.A.E. · EGX · market EG · INTERNAL — never shown to a reader**

**THIS IS THE FUNDAMENTAL WALK-FORWARD [R-FCAL-01].** The driver model rebuilt as it
stood at five past origins, projected forward, and scored against what the company
actually reported. It is not the price-engine walk-forward
(`scem_study/backtest_5y.py`, band coverage on the Monte Carlo cone) and not the
technical walk-forward (`engine/lab/ta_calibration/`). Three tests in this system carry
that name and they measure different machinery on different evidence.

Everything below was pre-registered in `PRE_REGISTRATION_07-09-2026.md` before a single
error was computed.

---

## 1 · Scope — LIGHT, on five sourceable fiscal years

Five fiscal years, FY2021 to FY2025, every figure from the company's own audited
statements. Five origins, horizons one to three, **nine resolved driver-cells**.

**Why the span stops at FY2021.** Sinai Cement publishes exactly six documents. Three
of them — the FY2022 and FY2023 audited filings, and the Arabic FY2021 one — had never
been downloaded before this run; opening the two English ones is what took the span
from three sourceable years to five and the scope decision from SKIP to LIGHT. The
Arabic filing was downloaded and is **unreadable**: its figures are Eastern Arabic
numerals and neither OCR model available here returns a digit from them, so FY2020 is
left out and the window shortened rather than filled from a vendor.

**Every filing is an image-only scan** — `pdftotext` returns 30 to 37 characters for
documents of 30 to 36 pages — so every number arrived by OCR off the rendered pixels
and ARITHMETIC IS THE ARBITER. `panel.py` runs the footings the filings themselves
print, at import. Two misreads were caught by them and neither was visible on the
page:

| what | read | filed | how it was caught |
|---|---|---|---|
| FY2022 short-term loans from affiliates | 960,000,000 | 950,000,000 | the filing's own current-liabilities subtotal refuses the first reading |
| FY2021 deferred tax | 11,761,441 | 11,751,441 | only one of the two closes profit before tax to profit after tax |

## 2 · What this issuer does not disclose

**NO PHYSICAL VOLUME. ANYWHERE.** Not a tonne of clinker, not a tonne of cement, not
an installed capacity, not a utilisation rate — in any of the six filings, in any
year. Every OCR'd page of the FY2022 and FY2023 filings was searched and the search
returned nothing.

So the ground-up build cannot reach volume × price on a DISCLOSED unit and drops to
the finest sourced level, which for this issuer is the **cost-note line**. Under
[R-SIGCM-02] these revenue lines are `derived`, never `unit`. This is a fact about the
disclosure rather than about the effort, and it is the single most important thing
this run establishes about the delivered study: the tonnage and utilisation that
study's model runs on come from a plant register and the trade press, not from the
company.

## 3 · The company the panel actually shows

| | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|---:|---:|
| Revenue | 1443.4 | 2343.2 | 4285.5 | 6428.0 | 9089.1 |
| EBITDA | -154.6 | -24.1 | 283.6 | 1585.5 | 3455.2 |
| EBITDA margin | -10.7% | -1.0% | 6.6% | 24.7% | 38.0% |
| Profit after tax | -345.0 | -319.8 | -117.6 | 3072.4 | 2284.5 |
| Interest-bearing debt | 1846.0 | 1753.9 | 2608.0 | 577.9 | 137.6 |
| Cash | 744.0 | 124.7 | 350.0 | 2038.0 | 4762.3 |
| Equity | -146.5 | -496.4 | -614.0 | 3735.8 | 6020.3 |
| Shares (mn) | 68.1 | 133.1 | 133.1 | 133.1 | 260.8 |

EGP million except where stated. **A company transformed inside the panel:** revenue
6.3 times over four years, an EBITDA margin from -10.7 per cent to 38.0, negative
equity of EGP -614.0mn at FY2023 becoming EGP 6020.3mn at FY2025, and interest-bearing
debt of EGP 2608.0mn becoming EGP 137.6mn. Any record scored across that is a record of
one extraordinary arc, and every interval below should be read knowing it.

## 4 · Trap (i), measured on this name

**Interest comes from the borrowings that actually bear it.** Suppliers, other credit
accounts, provisions and the deferred-tax liability pay nothing. The two denominators
on this company:

| | FY2022 | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|---:|
| on the borrowings that bear interest | 10.22% | 12.64% | 12.20% | 7.97% |
| on total liabilities | 5.83% | 7.34% | 6.40% | 1.35% |

A factor of **1.7x to 5.9x**. Dividing by the broad total would have implied this
company borrowed at 1.35 per cent in FY2025, in an economy whose policy rate was 19.5
per cent, and the bias that produced would have looked exactly like evidence.

## 5 · The score

Log error `ln(projected / actual)`. **A negative bias means the method forecast BELOW
what the company reported**, and the `outturn/forecast` column is how many times the
outturn came in above the forecast.

| driver | n | bias | MAE | outturn/forecast | 95% block CI | by era | era sign |
|---|---:|---:|---:|---:|---|---|---|
| ebitda | 6 | -2.220 | 2.220 | 9.21x | [-3.312, -1.265] \* | E1 -3.18 / E2 -1.26 | — |
| pat | 2 | -1.885 | 1.885 | 6.59x | n<3 | E2 -1.89 | — |
| interest income | 9 | -0.953 | 1.627 | 2.59x | [-2.355, +0.446] | E1 -0.58 / E2 -1.70 | — |
| capex | 9 | -0.831 | 1.022 | 2.29x | [-1.463, -0.408] \* | E1 -1.12 / E2 -0.26 | — |
| working capital | 3 | -0.704 | 0.843 | 2.02x | [-1.170, -0.685] \* | E1 -1.16 / E2 +0.21 | FLIPS |
| ga | 9 | -0.590 | 0.622 | 1.80x | [-0.910, -0.395] \* | E1 -0.75 / E2 -0.27 | — |
| revenue | 9 | -0.561 | 0.561 | 1.75x | [-0.833, -0.353] \* | E1 -0.75 / E2 -0.18 | — |
| cogs maintenance | 9 | -0.503 | 0.538 | 1.65x | [-0.836, -0.245] \* | E1 -0.44 / E2 -0.62 | — |
| transport | 9 | -0.452 | 0.737 | 1.57x | [-1.105, +0.032] | E1 -0.82 / E2 +0.28 | FLIPS |
| materials | 9 | -0.287 | 0.425 | 1.33x | [-0.654, +0.102] | E1 -0.53 / E2 +0.21 | FLIPS |
| cogs wages | 9 | -0.241 | 0.241 | 1.27x | [-0.380, -0.146] \* | E1 -0.24 / E2 -0.24 | — |
| dna | 9 | -0.025 | 0.096 | 1.02x | [-0.114, +0.069] | E1 +0.01 / E2 -0.10 | FLIPS |
| finance expense | 9 | +0.477 | 0.794 | 0.62x | [-0.335, +1.324] | E1 +0.07 / E2 +1.29 | — |

`\*` marks an interval whose sign holds across both bootstrap block lengths.

Three drivers cross zero somewhere and are not on a log scale at all — this company
lost money in three of five years — and they are reported separately rather than
pooled:

| driver | n | bias (relative) | MAE (relative) |
|---|---:|---:|---:|
| ebitda | 3 | -1.988 | 1.988 |
| pat | 7 | -1.000 | 1.000 |
| working capital | 6 | +6.791 | 7.995 |

## 6 · THE SKILL VERDICT — the method beats both naive benchmarks at every horizon

| | h=1 | h=2 | h=3 |
|---|---:|---:|---:|
| skill vs FREEZE (flat at last actual) | +0.185 | +0.129 | +0.123 |
| skill vs TREND (trailing CAGR) | +0.239 | +0.231 | +0.205 |
| cells scored, freeze | 45 | 32 | 20 |
| cells scored, trend | 30 | 20 | 10 |

**This is a name where the answer to "is the method beating no change yet" is YES at
every horizon tested.** On PHDC it was not, on net profit, at any horizon. The margin
is real but it is not large — between a tenth and a quarter of the naive error removed
— and it rests on nine cells from one company through one extraordinary arc, which is
exactly why [R-FCAL-01] calls every finding from a run like this PROVISIONAL.

**The trend benchmark is undefined at origin FY2021** and that was pre-registered: one
point of history admits no trailing growth rate. That origin is scored against freeze
alone and the cell counts above say so.

## 7 · The direction of the miss, and it agrees with the book

**Eleven of thirteen drivers came in BELOW what the company reported.** Revenue by a
factor of 1.75, EBITDA by 9.2, capital spending by 2.3. Only finance expense ran the
other way, and for a reason the model's own specification explains rather than excuses:
the rule holds debt flat at the origin's level, and this company REPAID essentially all
of it.

That direction is the pooled census's own finding arriving on another name. It is also
the single most useful thing this run says about the delivered study: if that study is
wrong about FY2026 onward, this company's own history says the more likely error is
that the forecast is too LOW.

## 8 · Macro versus company

Each origin re-run on the outturn inflation path, then on outturn inflation and
activity together.

| driver | MAE as known | MAE, perfect inflation | macro share |
|---|---:|---:|---:|
| materials | 0.425 | 0.264 | +37.8% |
| cogs wages | 0.241 | 0.159 | +34.1% |
| revenue | 0.561 | 0.376 | +32.9% |
| ga | 0.622 | 0.434 | +30.2% |
| transport | 0.737 | 0.568 | +22.9% |
| working capital | 0.843 | 0.685 | +18.8% |
| capex | 1.022 | 0.833 | +18.4% |
| cogs maintenance | 0.538 | 0.468 | +13.0% |
| ebitda | 2.220 | 2.076 | +6.5% |
| dna | 0.096 | 0.096 | -0.1% |
| pat | 1.885 | 1.901 | -0.8% |
| finance expense | 0.794 | 0.794 | +0.0% |
| interest income | 1.627 | 1.627 | +0.0% |

**THE SPLIT'S OWN CHECK PASSES.** Depreciation, finance expense and interest income
carry no inflation term in their rules and return a macro share of zero — exactly 0.0
per cent for the two financing drivers and −0.1 per cent for depreciation, which has no
CPI term in its first year. A split that could not return zero where zero is the right
answer would be measuring something other than what it claims.

**About a third of this method's miss on this company is the macro path and two thirds
is the company.** At origin FY2021 the IMF's own October 2021 edition projected
Egyptian inflation of 6.7, 7.1 and 7.1 per cent for 2022, 2023 and 2024. The outturn
was 16.5, 28.9 and 26.5. No forecasting method available in 2021 had that path, and the
two thirds that remains is what the method actually owns.

## 9 · The revenue error decomposed

| cell | total log error | from the activity anchor | from the price anchor | residual |
|---|---:|---:|---:|---:|
| FY2021 h=1 | -0.367 | +0.053 | +0.065 | -0.485 |
| FY2021 h=2 | -0.847 | +0.108 | +0.133 | -1.088 |
| FY2021 h=3 | -1.128 | +0.164 | +0.202 | -1.494 |
| FY2022 h=1 | -0.462 | +0.047 | +0.095 | -0.604 |
| FY2022 h=2 | -0.742 | +0.099 | +0.168 | -1.009 |
| FY2022 h=3 | -0.965 | +0.154 | +0.236 | -1.356 |
| FY2023 h=1 | -0.132 | +0.042 | +0.231 | -0.405 |
| FY2023 h=2 | -0.272 | +0.093 | +0.387 | -0.752 |
| FY2024 h=1 | -0.138 | +0.045 | +0.164 | -0.346 |

**THE EXOGENOUS ANCHOR IS THE PROBLEM AND THE RESIDUAL SAYS SO.** Egypt's real GDP
growth contributed between +0.04 and +0.16 of log revenue growth across every cell
while the company's revenue was compounding at 58 per cent a year in nominal terms.
Real GDP growth is not Egyptian cement demand: domestic cement consumption rose 13.4
per cent in 2025 against GDP growth around 4, and the production quota regime that had
capped output since 2021 was permanently lifted in July 2025. This is L-058 arriving on
another name — an exogenous volume anchor has to be scored against "no change" before
it is trusted, and this one loses badly on its own leg even while the whole model beats
freeze.

**It is a SPECIFICATION finding, not a calibration one**, and no correction factor may
hide it. What would fix it is an Egyptian cement-consumption series at each origin's
own vintage, which this run did not have and did not invent.

## 10 · Corrections — NOTHING PROMOTED, AND THAT WAS PRE-REGISTERED

The cut-invariance test [R-FCAL-01 AMENDED 07-09-2026] was run through the shared
instrument `engine/valuation_calibration/boundary_sensitivity.py`, never
reimplemented. **Every driver returns ZERO admissible cuts**: nine cells spread over
four target years admit no boundary leaving five on each side. Every bias this run
measured is therefore UNTESTABLE for stability, never stable — an absence of contrary
evidence is not evidence.

`PRE_REGISTRATION_07-09-2026.md` section 6 states that consequence in advance, before
any error existed, so nothing here is a verdict reached after seeing which way the
numbers went.

| candidates measured | promoted | watch flags | refused as aggregates |
|---:|---:|---:|---:|
| 13 | **0** | 11 | 2 |

4 candidates improve the out-of-sample error when the expanding-window half-strength
factor is applied — cogs maintenance, cogs wages, ga, revenue — and **none of them is promoted**, on clause one. 7 more make
it worse, which is L-061's signature: a correction that degrades out of sample is a
specification defect, not a bias.

Clause two would refuse most of them anyway and the reasons are recorded per driver in
`corrections_log.json`. Two are worth naming: a multiplier on revenue would be papering
over the activity anchor identified in section 9, and a multiplier on capital spending
points the opposite way from L-063 and L-275, which say the recent run rate on an old
plant is a CEILING rather than a central estimate.

**The guidance ledger is EMPTY and that is a finding.** Sinai Cement publishes no
forward guidance, no results presentation and no earnings call — so no driver in this
model can have inherited a management lean, because there is no management forward
number to inherit.

## 11 · The forward bands, with their basis, count and orientation

[R-FCAL-01 AMENDED 07-09-2026] a published band declares all three in the file. This
run's are **span**, counted per cell, oriented **actual over forecast**: multiply a
point projection by the band. A band above 1.0 means the method forecast below the
outturn.

| driver | h=1 (n=4) | h=2 (n=3) | h=3 (n=2) |
|---|---|---|---|
| revenue | 1.14 – 1.59 | 1.31 – 2.33 | 2.62 – 3.09 |
| materials | 0.76 – 1.65 | 0.73 – 2.50 | 1.38 – 2.21 |
| cogs wages | 1.01 – 1.21 | 1.07 – 1.44 | 1.48 – 1.86 |
| cogs maintenance | 0.94 – 2.12 | 0.94 – 2.55 | 2.34 – 3.07 |
| transport | 0.64 – 3.90 | 0.66 – 3.16 | 2.06 – 3.24 |
| ga | 0.86 – 1.73 | 1.51 – 2.88 | 2.73 – 3.65 |
| dna | 0.94 – 1.10 | 0.91 – 1.25 | 0.93 – 1.25 |
| capex | 0.42 – 3.46 | 1.48 – 7.30 | 3.40 – 8.24 |

**HORIZONS FOUR AND FIVE CARRY NO BAND**, and the delivered study says so in those
words rather than borrowing the three-year band. Five sourceable fiscal years give a
longest resolved horizon of three; nothing in this company's own record speaks to a
four- or five-year forecast.

## 12 · The valuation-input block

Committed at every one of five origins, built as the run went: cash, interest-bearing
debt, PP&E, depreciation and amortisation, the working-capital lines, capital
expenditure and the share count. `python3 scripts/check_valuation_inputs.py` reports
SCEM conforming.

**THE SHARE COUNT IS FOOTED TWICE AT EVERY ORIGIN** and that is what makes a
carried-back count impossible here rather than merely discouraged: issued capital over
the EGP 10 par reproduces the count, and that count then reproduces the year's own
PRINTED earnings per share. The count is 68,058,443 at FY2021, 133,065,867 at FY2022 to
FY2024 and 260,812,477 at FY2025 — it moves twice inside a five-year panel, so today's
count carried back would have shown up immediately as an EPS that refused to
reproduce.

FY2020 appears under `prior_year_anchor` carrying one figure — the opening cash of EGP
17,035,796, read off the FY2022 cash-flow statement's comparative column — with
everything else RECORDED AS MISSING and its reason named. It is not listed as an
origin, because the run did not test it.

## 13 · One-offs

| year | line | value | treatment |
|---|---|---:|---|
| FY2023 | change in inventory inside cost of sales | 138,243,904 | left in and RECORDED. |
| FY2024 | gain on sale of investments | 1,517,386,642 | EXCLUDED from every driver rule and from the profit the drivers rebuild. |
| FY2025 | provisions other than depreciation | -28,192,283 | left in. |

The FY2024 disposal of the Sinai White Portland Cement stake is 48.2 per cent of that
year's pre-tax profit and is excluded from every driver rule. A model that cannot
foresee a stake sale should not be scored as though it should have — and net profit is
shown both ways in the side-by-side statements.

## 14 · Caveats, stated plainly

* **Nine cells, one company, one extraordinary arc.** Every interval here is wide and
  several straddle zero. Nothing in this record is validated.
* **The panel spans a devaluation sequence and a recovery from near-insolvency.** A
  method scored across that is being asked a harder question than it will usually face,
  which cuts both ways: the skill result is more impressive and the bias measurement is
  less transferable.
* **The activity anchor is mis-specified** and section 9 says so. The skill verdict
  holds in spite of it, not because of it.
* **The macro conditioning for origin FY2025 uses the April 2025 WEO edition**, not the
  October one, which could not be sourced from any of four URL patterns. It existed at
  that origin so the point-in-time discipline holds; it is simply not the freshest
  edition that did. No scored cell depends on it.
* **Perfect foresight of 2025 is a projection, not an outturn.** The latest edition
  obtainable here projects that year rather than reporting it, and cells landing on it
  are labelled.
* **This is a first full run on this name.** The next update adds one origin — FY2026,
  which grades the cells standing at FY2023, FY2024 and FY2025 — and re-tests every
  watch flag on a panel that will admit its first real era cut at around fifteen cells.
