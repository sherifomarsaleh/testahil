# ARCC — fundamental walk-forward, pre-registration

**Written 1 September 2026, BEFORE a single forecast error was computed.** Fixed in advance
under [R-FCAL-01] §2. Parameters are stated, never fitted; sensitivities are reported, never
selected. An amendment after a result exists is tuning, not a choice ([L-042]) — this file
carries no amendments.

Ticker ARCC · Arabian Cement Company S.A.E. · EGX · market EG · class **cement and heavy
industrial** · fiscal year = calendar year.

**Which walk-forward this is:** the FUNDAMENTAL one — drivers projected from a past origin
and scored against what the company actually reported. Not the price-engine walk-forward
(band coverage on the Monte Carlo cone, `arcc_study/backtest_5y.py`) and not the technical
walk-forward (`engine/lab/ta_calibration/`). They test different machinery on different
evidence and neither substitutes for the other.

**What already binds, read before this was written** (`python3 engine/lessons.py ARCC --class
"cement and heavy industrial"`): 56 ALL-scope lessons and one CLASS lesson, [L-110] — *fuel
and imported inputs escalate on their own commodity path, not on domestic inflation* — which
this company itself produced in August 2026. Everything marked PROVISIONAL is a recorded
finding of an unvalidated method: read, not cited as authority.

---

## 0 · Scope decision — FULL

**The archive supports twelve sourceable fiscal years, FY2014 through FY2025**, every one of
them from ARCC's own audited consolidated financial statements, downloaded from its own
investor-relations archive at `arabiancementcompany.com`. Under §0 that is a **FULL run**:
every origin from the first year with five years of history, horizons 1–5.

What was attempted, and what came back:

| route | outcome |
|---|---|
| `arabiancementcompany.com` — the company's own IR archive | **175 documents listed, 128 retrieved**; annual consolidated accounts for FY2015–FY2025, quarterly accounts from 1Q2015, earnings releases from 2014, investor presentations from 2014 |
| the same site, on 07-Aug-2026 | `connect_rejected` at the egress proxy — the failure recorded in the study of that date. It resolves now, and the archive behind it is deep. **The block was transient and the log is what made that checkable** ([L-007]) |
| Egyptian Exchange `egx.com.eg` | does not resolve from this environment |
| oldest annual accounts on the site | FY2015, whose comparative column carries **FY2014** — that is where the window stops, and it stops there because that is the oldest year ARCC itself publishes |

**The window was not shortened for convenience and it was not padded to reach a threshold.**

### Origins and horizons

Origins are fiscal year ends, 31 December: **FY2018, FY2019, FY2020, FY2021, FY2022, FY2023,
FY2024, FY2025**. FY2018 is the first year with five years of history behind it
(FY2014–FY2018). Horizons **h = 1…5**. A cell is scored only where the actual exists, which
gives **25 scoreable origin-horizon cells per driver**:

| origin | scoreable horizons | targets |
|---|---|---|
| FY2018 | 1–5 | FY2019 … FY2023 |
| FY2019 | 1–5 | FY2020 … FY2024 |
| FY2020 | 1–5 | FY2021 … FY2025 |
| FY2021 | 1–4 | FY2022 … FY2025 |
| FY2022 | 1–3 | FY2023 … FY2025 |
| FY2023 | 1–2 | FY2024, FY2025 |
| FY2024 | 1 | FY2025 |
| FY2025 | — | nothing has matured |

**Consequences accepted in advance, not discovered later:**

- **Twenty-five cells is a real sample by this project's standards and a small one in
  absolute terms.** It is 2.8x AMOC's nine and it is still one company. A correction
  estimated here is estimated on eight origins.
- **The window contains a loss year and a boom.** FY2020 lost money at the profit-before-tax
  line (−137,411,687) and FY2025 earned 4,725,157,878 — a spread of a factor of thirty-five
  on the same drivers. A log-error score handles the scale; it does not make the two eras one
  population, and §5 will not average across them.
- **Point-in-time discipline is absolute and it BITES on this name.** FY2018, FY2019 and
  FY2015 were each re-presented in the following year's comparative column (B-2, B-8 of the
  basis-break register). Every origin sees the figure **as first reported in that year's own
  filing**; the restatement is carried beside it and never substituted.

## 1 · Data and provenance

Every figure carries four fields — value, source document, document date, tier. **Every
financial figure in this panel is tier A**: the company's own audited consolidated financial
statements. **Every physical figure is tier A COMPANY_IR**: the company's own earnings
releases and investor presentations, tagged distinctly from the audited-statement tag,
because the statements carry no tonne and a reader is owed the difference.

**No number enters the panel until it foots against its own arithmetic.** That is not a
formality on this name: ARCC files its statements as SCANS with no text layer, and the OCR
misreads a leading 1 as a 2 (B-1). Three FY2016 figures came off the page wrong and looking
perfectly clean, and each was caught only because a printed subtotal refused to agree with
its parts — then confirmed independently by the FY2017 filing's comparative column. Four
pages of the H1-2026 filing are set landscape and OCR upright into wreckage that still looks
like prose; they are re-read rotated. **Arithmetic is the arbiter, not the extractor's
confidence.**

Nothing is estimated, interpolated or inferred to fill a gap. Where a year cannot be sourced
the window shortens.

## 2 · Drivers — the mechanical rule and its parameters

Built on the cost taxonomy the filings themselves use throughout the window — raw materials,
manufacturing depreciation, licence amortisation, transportation, overheads — and the revenue
taxonomy of note 4 — local goods, export goods, services. **No judgement drivers at any
historical origin.** No rule reads guidance: management's forward targets lean the same way
an optimistic model does, so a driver that consumes guidance inherits the lean instead of
correcting for it.

Notation. `o` = origin, `h` = horizon in years. Every macro term uses only what had been
published at `o`:

- `Π CPI(o,h) = (1 + cpi(o))^h`, `cpi(o)` = the last published Egyptian annual inflation rate at o.
- `Π FX(o,h) = (1 + fx(o))^h`, `fx(o)` = the last published EGP/USD annual depreciation at o.
- `Π POP(o,h) = (1 + pop(o))^h`, `pop(o)` = the last published Egyptian population growth at o.
- `COAL(o)` = the origin's calendar-year mean South African coal price in EGP, **held flat**.
  A commodity price has no drift and assuming one would be a forecast, not a rule.

| # | driver | rule | parameters |
|---|---|---|---|
| D1 | local sales volume, tonnes | `local(o) × Π POP(o,h)` | none |
| D2 | export sales volume, tonnes | flat at the origin's actual | none |
| D3 | export mix (cement vs clinker) | flat at the origin's actual shares | none |
| D4 | local realised price, EGP/t | `p_loc(o) × Π CPI(o,h)` | pass-through **1.0** |
| D5 | export realised price, EGP/t | `p_exp(o) × Π FX(o,h)` | pass-through **1.0** |
| D6 | services revenue | `svc(o) × Π CPI(o,h)` | none |
| D7 | raw materials per tonne | `rm_t(o) × [w × COAL(o+h)/COAL(o) + (1−w) × Π CPI(o,h)]` | **w = 0.5** |
| D8 | transportation cost per tonne | `tr_t(o) × Π CPI(o,h)` | none |
| D9 | overhead cost per tonne | `ov_t(o) × Π CPI(o,h)` | none |
| D10 | manufacturing depreciation | flat at the origin's actual | none |
| D11 | licence amortisation | flat at the origin's actual | none |
| D12 | general and administration | `ga(o) × Π CPI(o,h)` | none |
| D13 | provisions and impairments | flat at the origin's actual | none |
| D14 | interest income | flat at the origin's actual | none |
| D15 | other income | flat at the origin's actual | none |
| D16 | finance costs | `rate(o) × borrowings(o)`, **rate(o) = finance cost(o) ÷ interest-bearing borrowings(o)** | none |
| D17 | foreign-exchange differences | **zero at every horizon** | none |
| D18 | income tax | `22.5% × PBT` (Egyptian statutory rate) | **22.5%** |
| D19 | non-controlling interest | the origin's actual NCI share of profit after tax | none |

### Four things in that table are the substance of the design

**D7 is where [L-110] meets this company's actual fuel, and the blend is stated in advance.**
[L-110] — ARCC's own class lesson — says a globally traded input escalates on the world price
and the exchange rate, not on the domestic cost of living. But ARCC's fuel is **not wholly
imported**: its own presentations record that it sources **70–80% of its coal needs through
LOCAL pet-coke**, alongside refuse-derived fuel it partly produces itself (B-7). Escalating
the whole raw-materials line on seaborne coal would be the mirror image of the error [L-110]
warns about. The filings never split fuel out of raw materials, so the honest construction is
a **declared blend**: `w = 0.5` on the coal path and `1 − w` on domestic inflation. **w is
stated, not fitted.** `w ∈ {0.3, 0.7}` is reported as a sensitivity in §4 and is **never
selected on the basis of its score**.

**D16 is the trap [R-FCAL-01] §3 names first, and it is closed by construction.** The
borrowing rate is formed on **the borrowings that actually bear interest** — the disclosed
borrowings, current portion and credit facilities — and never on a broader liabilities total.
Trade and notes payable, creditors and other credit balances and current tax liabilities pay
no interest; dividing the finance charge by them would understate the rate by a multiple and
manufacture a bias that is arithmetic rather than evidence. That is exactly what happened on
PHDC ([L-002], [L-041]), and it is pre-registered closed here rather than discovered later.

**D17 is refused, not modelled.** Foreign-exchange differences swing from −245,925,656
(FY2016) to +66,332,750 (FY2019) to −192,058,477 (FY2022) with no persistence. A non-zero
rule would smuggle a currency forecast into a driver that is meant to be mechanical. It is
set to zero at every horizon and the resulting error is reported in full, so the cost of the
refusal is visible rather than hidden.

**Revenue and cost sit on the same recognition clock, and this is checked rather than
assumed.** ARCC's performance obligation is the sale of cement and clinker, satisfied at a
point in time under Egyptian Accounting Standard 48 (B-5). There is no percentage-of-
completion clock here, so the second trap of [R-FCAL-01] §3 — the one that produced [L-001]
on PHDC — does not bite on this name. Stated because a check that is skipped because it
"obviously" passes is not a check.

## 3 · Benchmarks

Both are computed at every scoreable cell, per driver and on the aggregates.

- **FREEZE** — every line flat at the origin's last actual, in nominal EGP.
- **TREND** — every line grown at its own trailing CAGR over the longest window available at
  the origin, **capped at three years**. Every origin in this window has at least three prior
  years, so TREND is scoreable at all eight; the window length is recorded in every cell.

**Declared in advance, so it is not later reported as a finding:** D2, D3, D10, D11, D13, D14,
D15 and D16 are level-persistence rules and are therefore **identical to FREEZE by
construction**. Their skill against FREEZE is zero by definition, not by measurement, and is
reported as "n/a — rule equals benchmark". Their errors are still computed and decomposed,
which is the part that carries information. The rules that can differ from FREEZE are D1, D4,
D5, D6, D7, D8, D9, D12, D18 and the aggregates built from them.

## 4 · Score, uncertainty, sensitivity

- **Score:** log error per driver per horizon, `e = ln(projected / actual)`. Reported as bias
  `mean(e)`, `MAE = mean(|e|)`, share of cells over- and under-forecast, and sign by era. Log
  points are translated to percentages wherever a reader sees them.
- **A cell whose actual is zero or negative is not scored and is COUNTED.** FY2020's
  profit before tax is negative and FY2017's tax line is a credit; a log error does not exist
  there. The count of unscoreable cells is published per driver, because a denominator that
  quietly shrinks is how a bad driver looks good.
- **Uncertainty:** moving-block bootstrap over ORIGINS, block lengths **{2, 3, 4}** — the
  house robustness bar — 2,000 resamples, **seed 42**. Eight origins support all three block
  lengths; nothing is excluded and no block length is chosen after the fact.
- **Sensitivity:** `w ∈ {0.3, 0.5, 0.7}` on D7, reported for every aggregate. Reported, never
  selected.
- **Decomposition:** the revenue error is decomposed into volume, channel mix and realised
  price; the profit-before-tax error into revenue, cost of sales, G&A, other items and
  finance.
- **Every origin's projected-versus-actual income statement is shown side by side.**

## 5 · Macro versus company

Exogenous inputs are Egyptian CPI, EGP/USD, Egyptian population and the South African coal
price — nothing else. Every origin is re-run three ways:

1. **Knowable** — the last published annual value at the origin, projected by the rules in §2.
   No forecast of a macro variable is permitted at an origin.
2. **Perfect foresight** — the realised CPI, FX and coal-in-EGP paths.
3. **Perfect foresight of inflation only** — to separate the currency and coal channels from
   the domestic-cost channel.

`macro share = 1 − MAE(perfect foresight) / MAE(knowable)`, per driver and per horizon.

**The split carries its own check.** D2, D3, D10, D11, D13, D14, D15, D16, D17 and D19 contain
no CPI, FX, population or coal term, so their macro share **must come back exactly zero by
construction**. A non-zero value there is a wiring error in the split, not a finding, and the
run fails rather than reports it.

## 6 · One-offs

Every one-off in the window is identified and the record is shown with it classified: the
FY2020 pandemic loss year, the FY2022 provisions charge of 111,939,885 against a FY2023
charge of 15,220,195, the FY2017 tax credit, the FY2018/FY2019 cost-of-sales-to-G&A
re-presentations (B-2), the FY2019 arrival of right-of-use amortisation (B-3), and the
abolition of the cement production quota in May 2025. Classification is disclosed; the
headline record is reported on the **unclassified** basis as well, so nothing rests on the
choice.

## 7 · Corrections — the bar, set before any number exists

A correction is proposed only where a driver's bias **holds its sign across both eras**
(E1 = origins FY2018–FY2021, E2 = origins FY2022–FY2025) **and** survives the block bootstrap
at all three block lengths. It is estimated on an expanding window of origins resolved before
the origin it is applied to, at **half strength**, and reset after a structural break.

**Both clauses of [R-FCAL-01] §5 apply and the second is not a formality.** A correction
enters the live drivers only if it also **matches how that driver class is built across the
market's book**. A number out of line with the rest of the book usually means our own method
slipped on this one name, not that the company is unusual — and on PHDC that second clause is
what exposed a "bias" that was arithmetic rather than evidence ([L-003]). Anything that fails
either clause is a **WATCH FLAG**: recorded, graded live, revisited at every refit, acted on
by nobody.

**What this run can honestly produce**, stated now so the bar is not set after the numbers
arrive: a per-driver map of where the method breaks on a cement producer with a swinging
export mix, calibrated ranges for years 3–5 built from the measured error distribution, and
lessons scoped no wider than twenty-five cells on one company can carry. Every lesson it
produces is PROVISIONAL under [R-LESSON-01]. A better point estimate is a by-product and
never the aim.
