# PHAR — fundamental walk-forward, pre-registration

**Written 7 September 2026, BEFORE a single forecast error was computed.** Fixed in advance
under [R-FCAL-01] §2. Parameters are stated, never fitted; sensitivities are reported, never
selected. An amendment after a result exists is tuning, not a choice — this file carries no
amendments.

Ticker **PHAR** · Egyptian International Pharmaceutical Industries Company (EIPICO) · EGX ·
market EG · class **pharmaceutical manufacturer, generic and branded** · fiscal year =
calendar year.

**Which walk-forward this is:** the FUNDAMENTAL one — drivers projected from a past origin
and scored against what the company actually reported. It is NOT the price-engine
walk-forward (band coverage on the Monte Carlo cone, `engine/phar_study/backtest_5y.py`) and
NOT the technical walk-forward (`engine/lab/ta_calibration/`, the shipped read replayed on a
5/10/21-session clock). They test different machinery on different evidence and neither
substitutes for the other.

**What already binds, read before this was written** (`python3 engine/lessons.py PHAR --class
"pharmaceutical manufacturer, generic and branded"`): 245 lessons resolve on this name — the
ALL-scope set plus exactly one CLASS lesson, **[L-302]**, *a generic manufacturer that exports
can still be net short hard currency*, which this company itself produced on 4 September 2026.
Everything marked PROVISIONAL is a recorded finding of an unvalidated method: read, never
cited as authority. Four ALL-scope lessons shape the rules below and are named where they do:
[L-001] one recognition clock, [L-005] margins are outputs, [L-009] one escalator per driver
class, [L-012] guidance is scored and never consumed.

---

## 0 · Scope decision — **LIGHT**

**The archive supports seven sourceable fiscal years, FY2019 through FY2025.** Under §0 that
is a **LIGHT run**: the last five origins, horizons 1–3.

What was attempted, and what came back:

| route | outcome |
|---|---|
| `eipico.com.eg` → Investor Relations → Annual Reports | **reachable; seven annual reports listed and all seven retrieved**, FY2019 through FY2025 |
| the FY2020 report | carries the full consolidated AND standalone statements with notes and auditor's reports, in English, with FY2019 as its comparative column — **this is where the window starts** |
| the FY2019 report | is the board of directors' report ONLY. It carries the operating KPI tables (units produced, sales, exports, gross profit, equity, back to 2010 on some lines) and **no financial statements at all**, which is why FY2018 cannot be a panel year |
| Egyptian Exchange `egx.com.eg/en/DisclosureNews.aspx` | **does not resolve from this environment** — the same failure the delivered study logged on 9 August 2026, re-run today rather than carried from that log [R-IND-01] |
| regulator `disclosure.efsa.gov.eg` | **does not resolve** |
| any older EIPICO annual report | the investor-relations page lists 2019 as its oldest; there is nothing behind it |

**The window was not shortened for convenience and it was not padded to reach a threshold.**
FY2018 has KPIs and no statements; a panel year built on KPIs alone would be a fabricated
cell, and [R-FCAL-01] says to leave the year out and shorten the window.

### Origins and horizons

Origins are fiscal year ends, 31 December: **FY2020, FY2021, FY2022, FY2023, FY2024** — the
last five, as a LIGHT run specifies. Horizons **h = 1…3**. A cell is scored only where the
actual exists, which gives **twelve scoreable origin-horizon cells per driver**:

| origin | scoreable horizons | targets |
|---|---|---|
| FY2020 | 1–3 | FY2021, FY2022, FY2023 |
| FY2021 | 1–3 | FY2022, FY2023, FY2024 |
| FY2022 | 1–3 | FY2023, FY2024, FY2025 |
| FY2023 | 1–2 | FY2024, FY2025 |
| FY2024 | 1 | FY2025 |
| FY2025 | — | nothing has matured |

FY2019 is the **prior-year anchor**: the year the trailing window reaches and the run does not
test. It is committed under `prior_year_anchor` in `valuation_inputs.json` rather than under
`origins`, because recording it as an origin would misstate what was tested.

### Consequences accepted in advance, not discovered later

- **Twelve cells is a small sample and this file says so before any of them is computed.**
  It is under half of ARCC's twenty-five. A correction estimated here rests on five origins,
  and the fifth of them contributes one cell.
- **THE FY2020 ORIGIN IS IMPOVERISHED AND IS KEPT ANYWAY, WITH THE GAP FLAGGED.** The FY2020
  annual report is a condensed COVID-year edition. It carries no packs-produced figure, no
  consolidated depreciation charge, no consolidated capex, and a consolidated income
  statement with one lumped `expenses` line. So at that origin the volume × price build is
  not possible and the revenue driver drops to the finest level the disclosure supports —
  the parent's own local and export SALES VALUES, which that report does publish — with the
  gap flagged, which is SIGCM clause 2 as written rather than a departure from it. The
  alternative, taking those figures out of the FY2021 report's comparative column, is
  forbidden: a figure right in value and wrong in vintage is invisible in the pooled error
  afterwards.
- **The window contains a devaluation and a capital programme, and neither is a nuisance
  term.** The pound was devalued in March 2022, October 2022, January 2023 and March 2024;
  projects under construction went from EGP 866mn at FY2022 to EGP 5,694mn at FY2024. Both
  are real and both are what the errors will measure.
- **Point-in-time discipline BITES on this name.** Eight re-presentations sit inside this
  window, recorded in `panel.REPRESENTATIONS`: two revenue gross-up/net-down reclassifications,
  a net-profit presentation change worth EGP 34.5mn, a receivables netting, an administrative-
  expense split, a borrowings split, a PACKS-PRODUCED redefinition worth 2.1% of the FY2024
  figure, and a two-million-pound disagreement between the FY2024 income statement and the
  FY2025 comparative cash-flow statement about the same profit before tax. Every origin sees
  its own filing's own column.
- **Five printed cells in these filings do not foot, and a sixth foots only at its subtotal.**
  They are listed in `panel.FOOTING_FAILURES` with the arithmetic that settles each one.
  The largest is the FY2022 printed gross profit, EGP 18.0mn below what revenue less cost of
  sales gives and below what the statement's own chain to profit before tax requires — **and
  the same defective figure is carried forward into the FY2023 report's comparative column**,
  so a reader checking one filing against the next sees agreement and still holds the wrong
  number. Arithmetic is the arbiter, not the extractor's confidence, and not consistency
  between two filings either.

## 1 · Data and provenance

Every figure carries four fields — value, source document, document date, tier. **Every
financial figure in this panel is tier A**: EIPICO's own audited consolidated financial
statements, out of EIPICO's own annual reports, from EIPICO's own investor-relations page.
**Every physical and operating figure is tier A COMPANY_IR**: the company's own annual-report
indicator tables, tagged distinctly from the audited-statement tag. **No vendor, no broker, no
press appears anywhere in this panel** (SIGCM clause 1).

The two macro series are Country-ring institutional figures and are named as such in
`macro.py`: World Bank WDI inflation and population, plus the point-in-time inflation vintages
this repository already holds in `engine/macro_history/EG.json`. Neither is a company figure.

**Route.** Text layer (PyMuPDF), with Arabic-Indic digits normalised to Latin before any
figure was read. **The FY2024 report's Arabic glyph map is partly broken** — several header
strings render as mojibake while the Latin digits extract cleanly, which is precisely the
condition [R-FCAL-01] warns about, so every statement in every filing was footed against its
own subtotals before it was recorded, and `panel.assert_all()` raises rather than warns.

## 2 · The driver list, by class, and the MECHANICAL rule for each

**NO JUDGEMENT DRIVERS AT HISTORICAL ORIGINS.** The exercise tests the method, not the
analyst. Every rule below is a function of figures published on or before its origin.

The trailing window is `k = min(3, years of history available at the origin)`, stated per
origin rather than varied by result: k = 2 at FY2020 (FY2019 and FY2020 in the panel, plus
FY2018 KPIs where the driver is a KPI), k = 3 at every later origin.

### Volume and price — origins FY2021…FY2024 (its own definition window)

| # | driver | rule |
|---|---|---|
| **R1** | packs produced (thousand) | `units(t+h) = units(t) × (1+g)^h`, where `g` = the company's trailing k-year compound growth in packs, **CLIPPED to [g_pop − 2pp, g_pop + 2pp]** and `g_pop` = Egypt's trailing 3-year compound population growth at the origin (World Bank SP.POP.TOTL). The clip is what makes this an exogenously anchored volume driver rather than the company's own trend alone, per §3. The band is ±2pp, stated here and not varied. |
| **R2** | revenue per pack (parent, EGP) | `p(t+h) = p(t) × (1+e)^h`. `e` is the leg's escalator: **baseline** = trailing k-year compound growth in realised revenue per pack; **knowable-macro** = the origin's own vintage CPI print held flat; **perfect-foresight** = the realised calendar CPI of each forecast year. |
| **R5a** | cost per pack (parent, EGP) | `c(t+h) = c(t) × (1+e)^h`, **on the SAME escalator `e` as R2**. This is [L-001]/trap (ii) obeyed structurally: revenue and cost sit on one recognition clock and one price clock, so the gross margin is an OUTPUT of the two unit rules and is never set ([L-005]). |

### Revenue at the FY2020 origin only — the coarser level, with the gap flagged

| # | driver | rule |
|---|---|---|
| **R3** | parent local sales, parent export sales | each `× (1+g)^h` at its own trailing k-year compound growth, from the FY2020 report's own indicator table (FY2018, FY2019, FY2020). |
| **R5b** | cost of sales | the cost-of-sales RATIO to revenue held at the origin's own value; cost of sales = forecast revenue × that ratio. Same clock by construction. |

### Consolidation

| # | driver | rule |
|---|---|---|
| **R4** | consolidation ratio | consolidated revenue ÷ the parent's own disclosed sales value, **held at the origin's own value** with no growth term. It is the EIACO ampoules subsidiary and it has run between 1.015 and 1.059 over the window. |

### Charges below gross profit

| # | driver | rule |
|---|---|---|
| **R6a** | marketing | trailing k-year mean of marketing ÷ revenue, applied to forecast revenue (variable). |
| **R6b** | administrative block (R&D + general and administrative + board) | `× (1+e)^h` off the origin's own level (fixed, escalated) — [L-009]: a fixed domestic cost stack gets the domestic escalator, and the unit price and unit cost get theirs, rather than one blended index across all of them. |
| **R6c** | provisions and credit losses | trailing k-year mean of provisions ÷ revenue, applied to forecast revenue. |
| **R6d** | finance cost | `r × average interest-bearing debt over the year`, `r` = the origin's own effective rate. **THE DENOMINATOR IS THE BORROWINGS THAT ACTUALLY BEAR INTEREST** — long-term loans, long-term credit facilities, short-term loans and creditor banks — and `panel.interest_bearing_debt()` is the only route to it. Trade and notes payable, other creditors, provisions, income tax payable, dividends payable and lease liabilities are excluded. This is trap (i) and [L-002]: dividing the finance charge by a broader liabilities total understates the rate by a multiple and manufactures a bias that looks exactly like evidence. |
| **R6e** | total charges below gross profit, FY2020 origin only | trailing k-year mean of `expenses_total ÷ revenue`, applied to forecast revenue. The FY2020 consolidated statement carries one lumped expenses line, so the component rules above have no origin to start from. |

### Capital, debt and the balance sheet

| # | driver | rule |
|---|---|---|
| **R8** | capex | trailing k-year mean of capex ÷ revenue, applied to forecast revenue. Capex is an INPUT that drives the capital base and depreciation, per §3, and is not solved out of anything. |
| **R9** | depreciation and amortisation | a roll-forward of the CAPITAL BASE (net PP&E **plus** projects under construction, because on this company spend lands in construction for years before it reaches PP&E): `base(t+h) = base(t+h−1) + capex(t+h) − D&A(t+h)`, `D&A(t+h) = d × base(t+h−1)`, `d` = the origin's own book rate `D&A(t) ÷ base(t−1)`. The rate is the accounts' own, not a life this desk picked. |
| **R7** | interest-bearing debt | the funding identity: `debt(t+h) = debt(t+h−1) + capex(t+h) + dividends(t+h) + Δworking capital(t+h) − net profit(t+h) − D&A(t+h)`, floored at zero. Dividends = the trailing k-year mean payout ratio × the previous forecast year's net profit. Working capital = the trailing k-year mean of net working capital ÷ revenue, so Δ working capital = that ratio × Δ revenue. The identity is circular through the finance cost and is resolved by **two fixed-point iterations**, stated here and not tuned. |
| **R10** | associates and interest income | trailing k-year mean of that block ÷ revenue, applied to forecast revenue. |
| **R11** | capital gains, foreign-exchange result and other income | **SET TO ZERO at every origin and every horizon.** A mechanical rule cannot forecast a currency result, and inventing one would be the judgement driver this exercise forbids. Their realised size is therefore part of the measured error and is classified as a one-off in §4 — WHICH IS THE POINT: on this name the FY2022 and FY2024 foreign-exchange results alone are EGP 286mn and EGP 700mn, and a method that quietly forecasts them would be scoring its own currency view rather than its driver model. |
| **R12** | tax | trailing k-year mean effective rate on profit before tax, being `(income tax + deferred tax + the takaful social contribution) ÷ profit before tax`, applied to forecast profit before tax. |
| **R13** | net profit | profit before tax less tax. An OUTPUT. |

**Guidance is scored and never consumed** [L-012]. EIPICO's annual reports carry forward
statements about capacity, new products and export markets. None enters any rule above. Where
a statement can be graded against an outcome it is graded in §4 and reported.

## 3 · The two naive benchmarks

- **FREEZE** — every line flat at the origin's last actual, at every horizon.
- **TREND** — every line grown at its own trailing k-year compound growth rate.

Both are computed for every driver at every origin-horizon cell, and skill is reported against
**both**, at every horizon. **A method that cannot beat "no change" has not earned the
precision it displays**, and if that is what this record shows, the record will say so.

## 4 · The score, and the bootstrap

- **Score**: the log error `e = ln(forecast ÷ actual)` per driver, per origin, per horizon.
  Positive is over-forecast. A cell whose actual or forecast is non-positive is dropped and
  counted, never signed around.
- **Bias** = mean `e`. **MAE** = mean `|e|`. **Share over** = the fraction of cells with
  `e > 0`.
- **Interval**: a moving-block bootstrap over ORIGINS, block sizes {2, 3}, 2,000 resamples,
  seed 42, reported as the 5th and 95th percentiles. Cells inside one origin are not
  independent and the block is what respects that.
- **Skill** against each benchmark = `(MAE_benchmark − MAE_model) ÷ MAE_benchmark`, per driver
  per horizon and pooled.
- **Sign by era, and by every cut the data admits** [R-FCAL-01 AMENDED 07-09-2026]. The
  market's era boundary is the currency: pre-2022 and 2022-onward. That boundary was chosen
  for the market and not for any driver here, so the sign is also tested at **every cut
  leaving at least five cells on each side**, through `engine/boundary_sensitivity.py`, and a
  bias whose sign depends on where the line was drawn is REPORTED, never corrected for.

## 5 · The macro / company split, and its own check

Every origin is re-run three ways:

1. **Baseline** — the rules above, with `e` = the company's own trailing growth. **No
   inflation term anywhere.**
2. **Knowable macro** — `e` = the inflation print available AT the origin, held flat, from
   `engine/macro_history/EG.json`. **Available at FY2020, FY2021, FY2022 and FY2023 only.
   The archive stops at 2023, so the FY2024 origin is REPORTED AS UNMEASURED on this leg and
   is not filled from a later vintage.**
3. **Perfect foresight** — `e` = the realised calendar inflation of each forecast year, World
   Bank WDI.

The macro share of a driver's error is `1 − |bias under perfect foresight| ÷ |bias under
baseline|`, reported per driver.

**THE SPLIT CARRIES ITS OWN CHECK, PRE-REGISTERED HERE:** the volume driver **R1** contains no
inflation term in any of the three legs, so its macro share must come out at **exactly zero by
construction**. If it does not, the split is wired wrong and the split's own output is void.

## 6 · The roles of the two samples

- The **rolling record** — all twelve cells — estimates any correction.
- The **non-overlapping origins** — FY2020 and FY2023, whose three- and two-year windows do
  not share a forecast year — confirm it. Two origins is a thin confirmation sample and this
  file says so in advance rather than after seeing which way it goes.

## 7 · Corrections — the test they must pass, fixed before any of them exists

- **Expanding window only**: a correction at origin *t* uses errors resolved strictly before
  *t*.
- **Half strength by default.**
- **Applied only where the bias holds its sign at EVERY cut the data admits**, not merely
  across the market's currency era [R-FCAL-01 AMENDED 07-09-2026].
- **Reset after a structural break**, defined in advance as a driver error beyond its own two
  standard deviations.
- Aggregates **rebuilt from adjusted drivers**, and adjusted tested against raw **by origin**.
- **A correction enters the live drivers only if it passes that test AND is consistent with
  how that driver class is built across the market's book.** Otherwise it is a **watch flag**
  — recorded, graded live, acted on by nobody. That second clause has already done its job
  once in this repository and what it caught was arithmetic wearing the costume of evidence.

## 8 · What this run may not do

It may not tune toward a better point estimate. **Two purposes, not three**: per-driver bias
detection, and calibrated ranges on the far years. A better central is a by-product and never
the aim; tuning toward one is the CRPS-selection mistake in a new costume, which this house
retired on out-of-sample evidence and does not revive.

It may not move the fair value toward the traded price. PHAR's committed central of EGP 36.64
sits 71.2% below the EGX close of EGP 127.30 supplied on 7 September 2026. That gap is
EVIDENCE that a defect may exist and it gets the eight-heading audit [R-GAP-01] — it is never
a target, and the honest output of such a review is frequently an unchanged central with a
stated reason.

## 9 · What would overturn this run's findings

- A pre-2019 EIPICO filing surfacing, which would lengthen the window and could turn LIGHT
  into FULL and change which origins carry the weight.
- A point-in-time inflation vintage for 2024 reaching `engine/macro_history/EG.json`, which
  would complete the knowable-macro leg at the fifth origin.
- The company restating any year inside the window, which is not idle here: eight
  re-presentations already sit in the panel and one of them moves a KPI this run scores.
