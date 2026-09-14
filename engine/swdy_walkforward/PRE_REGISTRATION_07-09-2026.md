# SWDY — fundamental walk-forward, pre-registration

**Written 7 September 2026, BEFORE a single forecast error was computed.** Fixed in advance
under [R-FCAL-01] §2. Parameters are stated, never fitted; sensitivities are reported, never
selected. An amendment after a result exists is tuning, not a choice — this file carries no
amendments.

Ticker SWDY · Elsewedy Electric Company S.A.E. · EGX · market EG · class **diversified
industrial with a contracting arm** · fiscal year = calendar year, every filing in the
archive being "for the financial year ended 31 December".

**Which walk-forward this is:** the FUNDAMENTAL one — drivers projected from a past origin
and scored against what the company actually reported. Not the price-engine walk-forward
(band coverage on the Monte Carlo cone, `swdy_study/backtest_5y.py`, `backtest_rows.csv`)
and not the technical walk-forward (`engine/lab/ta_calibration/`, the shipped read replayed
on a 5/10/21-session clock). They test different machinery on different evidence and neither
substitutes for the other.

**What already binds, read before this was written** (`python3 engine/lessons.py SWDY --class
"diversified industrial with a contracting arm"`): 246 lessons resolve on this name, of which
two are CLASS-scoped and were produced by this company itself in September 2026 —

- **[L-295]** a group whose legs sit on different contract structures cannot be forecast on
  one margin path. Measured on SWDY's own comparable halves the legs moved in OPPOSITE
  directions at once (cables 14.54% → 12.49% while contracting went 9.06% → 11.59%) while the
  group margin barely moved. **This pre-registration builds every leg on its own driver for
  that reason, and it is why no group margin appears in the driver table below.**
- **[L-296]** normalised earnings power is not a lens for a group with a contracting arm.
  Relevant to the study this run feeds, not to the driver rules here.

and one ALL-scoped lesson this company produced that bears directly on the aggregates:

- **[L-294]** the employees' statutory share of profit is an APPROPRIATION disclosed only in
  the earnings-per-share note, below profit attributable to owners, so **no cost driver can
  ever capture it, however carefully the cost stack is built**. It is therefore scored as its
  own line here rather than expected to fall out of the cost build.

Everything marked PROVISIONAL is a recorded finding of a method that is not yet validated:
read, not cited as authority.

---

## 0 · Scope decision — FULL

**The archive supports seventeen sourceable fiscal years, FY2009 through FY2025**, every one
of them from Elsewedy Electric's own documents. Under §0 that is a **FULL run**: every origin
from the first year with five years of history, horizons 1–5.

What was attempted, and what came back — the whole log is in `fetch_attempts.json`:

| route | outcome |
|---|---|
| `elsewedyelectric.com` | resolves; carries no financial archive of its own, one link to the investor site |
| `ir.elsewedyelectric.com/en/results-center` | **the archive, and it is deep.** A JavaScript-rendered results centre whose document list is served by a POST endpoint guarded by a per-session CSRF token; the token is read out of the rendered page in the same session, so it is reached without a headless browser. **293 documents listed across 2007–2026, 233 retrieved**, every one tier A |
| annual CONSOLIDATED audited statements | FY2007–FY2011, FY2013–FY2016, FY2018–FY2025 — **17 of 19 years** |
| FY2012 and FY2017 annual statements | **not published in the results centre.** Both years are carried by the comparative column of the FOLLOWING year's audited statements and by their own earnings releases, and both are recorded that way rather than treated as present |
| annual earnings releases | FY2010–FY2025, **sixteen consecutive years**, each carrying a full consolidated income statement and (from FY2016) a consolidated balance sheet |
| "results at a glance" investor sheets | FY2012 – 3Q2022, carrying **cable volume in tonnes, price per tonne and cost per tonne** — the finest disclosed level, and the reason a unit build is possible on this name at all |
| segment-analysis sheets | FY2014 – 3Q2022 |
| current-year quarters | Q1-2026 and Q2-2026, both the audited-basis consolidated interim statements AND their earnings releases and presentations |
| fetch failures | **one**, and it was the probe rather than the archive: the FY2018 consolidated annual statement is published at a URL containing a literal space and curl refused it with http 000. Re-run with the path percent-encoded, it is there [R-ENF-04] |

**The window was not shortened for convenience and it was not padded to reach a threshold.**

### Origins and horizons

Origins are fiscal year ends, 31 December: **FY2014 … FY2025**, twelve of them. FY2014 is the
first year with five years of history behind it *on every driver in the table below* — the
group lines reach back to FY2009 and would allow FY2013, but the SEGMENT split is first
disclosed for FY2010, so an FY2013 origin would have four years of history on the segment
drivers and five on the rest. **One origin set, and it is set by the thinnest driver**, because
an origin that sees a different amount of history per line is not one origin.

Horizons **h = 1…5**, giving **45 scoreable origin-horizon cells per driver**:

| origin | scoreable horizons | targets |
|---|---|---|
| FY2014 | 1–5 | FY2015 … FY2019 |
| FY2015 | 1–5 | FY2016 … FY2020 |
| FY2016 | 1–5 | FY2017 … FY2021 |
| FY2017 | 1–5 | FY2018 … FY2022 |
| FY2018 | 1–5 | FY2019 … FY2023 |
| FY2019 | 1–5 | FY2020 … FY2024 |
| FY2020 | 1–5 | FY2021 … FY2025 |
| FY2021 | 1–4 | FY2022 … FY2025 |
| FY2022 | 1–3 | FY2023 … FY2025 |
| FY2023 | 1–2 | FY2024, FY2025 |
| FY2024 | 1 | FY2025 |
| FY2025 | — | nothing has matured |

**Consequences accepted in advance, not discovered later:**

- **Forty-five cells is the largest sample this campaign has run and it is still one company.**
  A correction estimated here is estimated on eleven origins, and eleven origins of one issuer
  are not eleven independent observations.
- **The window contains a currency collapse and a boom on the same drivers.** Revenue runs
  from EGP 17.0bn (FY2014) to EGP 281.0bn (FY2025), a factor of sixteen and a half, while the
  pound went from about 7 to the dollar to about 48. A log-error score handles the scale; it
  does not make those two worlds one population, and §5 will not average across them.
- **The unit drivers stop before the window does, and that is a fact about the disclosure.**
  The investor sheets that publish cable tonnes, price per tonne and cost per tonne run to
  3Q2022 and were discontinued. Unit drivers are therefore scored **only inside their own
  definition window** and the count of scoreable cells is published per driver rather than
  quietly shared with the lines that have more.
- **Point-in-time discipline is absolute and it BITES on this name.** FY2015 revenue is
  EGP 20,571,703,734 in the FY2015 audited statements and EGP 18,894,528 thousand in the
  FY2016 earnings release's comparative column — a re-presentation of 8.1% on the top line.
  Every origin sees the figure **as first reported in that year's own filing**; the restated
  figure is carried beside it and never substituted.

## 1 · Data and provenance

Every figure carries four fields — value, source document, document date, tier. Financial
figures are tier A from the audited consolidated statements where those exist and parse;
segment and unit figures are tier A **COMPANY_IR** from the company's own earnings releases
and investor sheets, tagged distinctly from the audited-statement tag because the statements
carry no tonne and a reader is owed the difference.

**No number enters the panel until it foots against its own arithmetic**, and that is not a
formality here. Three things this archive does:

1. **A dense text layer is not a good text layer.** The FY2015 audited statements yield
   173,819 characters over 42 pages — dense by any density test — off an EMBEDDED OCR layer
   that renders 2,583,062,094 as `2S83062094` and 598,240,111 as `598 240 Ill`. Every figure
   looks clean. Density passes and arithmetic does not, which is why the footing test decides
   the route and the character count only decides where to start.
2. **A document-level route is not a page-level route.** The FY2025 audited statements yield
   329,052 characters over 70 pages and **pages 3, 4 and 5 carry one character each** — they
   are the auditor's report, the statement of financial position and the statement of changes
   in equity. The words "Total assets" occur NOWHERE in the extracted text of a seventy-page
   audited annual report. Those pages are re-read by OCR off the rendered pixels and the route
   is recorded **per page**, so a figure taken off page 5 is known to have come by OCR while a
   figure off page 6 is known to have come off the text layer.
3. **The OCR agrees with the statements' own arithmetic and with a second document.** The
   OCR'd FY2025 balance sheet reads cash as `Al 949 208 624`; the cash-flow statement on a
   text-layer page states `41 949 208 624` and total assets equal total equity plus total
   liabilities to the pound. Arithmetic is the arbiter, not the extractor's confidence.

Nothing is estimated, interpolated or inferred to fill a gap. Where a year cannot be sourced
the window shortens.

## 2 · Drivers — the mechanical rule and its parameters

**No judgement drivers at any historical origin.** No rule reads guidance: management's
forward targets lean the same way an optimistic model does, so a driver that consumes
guidance inherits the lean instead of correcting for it. Guidance is scored separately in §5
and consumed nowhere.

Notation. `o` = origin, `h` = horizon in years. Every macro term uses **only what had been
published at `o`**:

- `Π CPI(o,h) = (1 + cpi(o))^h`, `cpi(o)` = the last published Egyptian annual inflation rate at o.
- `Π FX(o,h) = (1 + fx(o))^h`, `fx(o)` = the last published EGP/USD annual depreciation at o.
- `Π GDP(o,h) = (1 + g(o))^h`, `g(o)` = the last published Egyptian real GDP growth at o.
- `CU(o)`, `AL(o)` = the origin's calendar-year mean copper and aluminium price in USD/tonne,
  **held flat**. A metal price has no drift and assuming one would be a forecast, not a rule.

### The three legs, and why they are three

The disclosed segments are re-cut twice inside the window (basis breaks B-3 and B-4), so the
scored revenue drivers are the **three groupings that survive every re-cut**:

| leg | FY2010–FY2016 | FY2017–FY2021 | FY2022–FY2025 |
|---|---|---|---|
| CABLES | Wires & Cables | Wires & Cables | Wire, Cable & Accessories |
| CONTRACTING | Turnkey Projects | Turnkey Projects | Engineering & Construction |
| OTHER | Electrical Products | Electrical Products + Meters + Transformers + Renewables-IPP | Electrical Products + Digital Solutions + Infrastructure Investment |

The three foot to total revenue to the pound in every year FY2011–FY2025, which is the check
that the grouping is a re-grouping and not a reconstruction.

### The table

| # | driver | rule | parameters |
|---|---|---|---|
| D1 | cable volume, tonnes | `vol(o) × Π GDP(o,h)` | none |
| D2 | cable realised price, EGP/t | `p(o) × [w_p × CU(o)/CU(o) × Π FX(o,h) + (1−w_p) × Π CPI(o,h)]` | **w_p = 0.7** |
| D3 | cable cost per tonne, EGP/t | `c(o) × [w_c × Π FX(o,h) + (1−w_c) × Π CPI(o,h)]` | **w_c = 0.7** |
| D4 | CABLES revenue | `D1 × D2` inside the unit window; `cab(o) × Π GDP × Π CPI` outside it | none |
| D5 | CONTRACTING revenue | `con(o) × Π GDP(o,h) × Π CPI(o,h)` | none |
| D6 | OTHER revenue | `oth(o) × Π GDP(o,h) × Π CPI(o,h)` | none |
| D7 | CABLES cost of revenue | `D1 × D3` inside the unit window; `cabcost(o) × Π GDP × [w_c FX + (1−w_c) CPI]` outside | **w_c = 0.7** |
| D8 | CONTRACTING cost of revenue | `concost(o) × Π GDP(o,h) × Π CPI(o,h)` | none |
| D9 | OTHER cost of revenue | `othcost(o) × Π GDP(o,h) × Π CPI(o,h)` | none |
| D10 | selling, general and administrative | `sga(o) × Π CPI(o,h)` | none |
| D11 | depreciation and amortisation | PP&E roll-forward: `opening PP&E ÷ L`, `L` = the **disclosed** useful life | `L` from `useful_lives.json` |
| D12 | capital expenditure | `capex(o) × Π CPI(o,h)`, an INPUT that drives PP&E and therefore D11 | none |
| D13 | other operating income | flat at the origin's actual | none |
| D14 | other operating expense | flat at the origin's actual | none |
| D15 | finance costs | `rate(o) × borrowings(o)`, **rate(o) = finance cost(o) ÷ INTEREST-BEARING loans and borrowings(o)** | none |
| D16 | finance income | flat at the origin's actual | none |
| D17 | foreign-exchange differences | **zero at every horizon** | none |
| D18 | income tax | `t(o) × PBT`, `t(o)` = the statutory rate in force at the origin, read from that year's own tax note | none |
| D19 | non-controlling interests | the origin's actual NCI share of profit after tax | none |
| D20 | employees' statutory share of profit | the origin's actual share of profit attributable to owners | none |

### Five things in that table are the substance of the design

**D15 is the trap [R-FCAL-01] §3 names first, and it is closed by construction.** The
borrowing rate is formed on **loans and borrowings, current and non-current** — the lines the
audited statements label as such — and never on a broader liabilities total. SWDY's balance
sheet makes this trap unusually easy to fall into: at 31-Dec-2025 total liabilities are
EGP 239.1bn of which **loans and borrowings are EGP 62.5bn**, so trade and other payables
(EGP 68.9bn), contract liabilities (EGP 81.3bn), due to related parties and provisions —
none of which pay interest — are more than TWO AND A HALF TIMES the borrowings. Dividing the
finance charge by the liabilities total would understate the borrowing rate by a factor of
about four and manufacture a bias that is arithmetic rather than evidence. That is exactly
what happened on PHDC ([L-002], [L-041]) and it is pre-registered closed here.

**Revenue and cost sit on the same recognition clock, and on THIS name that has to be checked
rather than assumed.** SWDY's contracting leg recognises revenue **over time as work
completes** — the audited statements' revenue note says so in terms and the FY2025 balance
sheet carries EGP 29.9bn of contract assets against EGP 81.3bn of contract liabilities — so
the second trap of [R-FCAL-01] §3, the one that produced [L-001] on PHDC, **is live here in a
way it was not on a cement maker**. It is closed by construction: D5/D8 and D4/D7 are matched
pairs, each leg's cost recognised on the same clock as that leg's revenue, and the legs are
never mixed. **A group-level cost driver would break this by construction and there is not
one in the table.**

**D2 and D3 carry a DECLARED blend and it is stated, not fitted.** A cable is metal, and the
company's own investor sheets publish a cable cost per tonne that moves with the metal. But
SWDY's cable revenue is not purely metal pass-through — it carries conversion, energy, labour
and freight — and the filings never split the metal out of the cost per tonne. The honest
construction is a declared blend: `w = 0.7` on the metal-and-currency path and `1 − w` on
domestic inflation, for both price and cost, **the same w on both sides so the blend cannot
by itself manufacture a margin**. `w ∈ {0.5, 0.9}` is reported as a sensitivity in §4 and is
**never selected on the basis of its score**.

**D11 rests on a DISCLOSED useful life or it does not run.** [R-TERM-01] refuses a life with
no source and a life this desk chose is not a disclosed life. The life is read out of the
accounting-policies and fixed-asset notes into `swdy_study/useful_lives.json` with its route,
and if no life can be sourced the driver is recorded as UNSOURCEABLE and the D&A line is
scored as FREEZE with that stated — never filled with a number somebody picked.

**D20 exists because no cost driver could ever have found it.** [L-294]: the employees'
statutory share of distributable profits is an appropriation below the attributable line,
disclosed only in the earnings-per-share note. It is scored as its own driver at the rate the
company itself discloses, and its absence from every cost driver is a property of Egyptian
company law rather than an omission in the build.

## 3 · Benchmarks

Both are computed at every scoreable cell, per driver and on the aggregates.

- **FREEZE** — every line flat at the origin's last actual, in nominal EGP.
- **TREND** — every line grown at its own trailing CAGR over the longest window available at
  the origin, **capped at three years**. Every origin in this window has at least three prior
  years, so TREND is scoreable at all eleven; the window length is recorded in every cell.

**Declared in advance, so it is not later reported as a finding:** D13, D14, D15, D16, D19 and
D20 are level-persistence rules and are therefore **identical to FREEZE by construction** on
their own line. Their skill against FREEZE is zero by definition, not by measurement, and is
reported as "n/a — rule equals benchmark". Their errors are still computed and decomposed,
which is the part that carries information. The rules that can differ from FREEZE are D1–D12,
D18 and every aggregate built from them.

## 4 · Score, uncertainty, sensitivity

- **Score:** log error per driver per horizon, `e = ln(projected / actual)`. Reported as bias
  `mean(e)`, `MAE = mean(|e|)`, share of cells over- and under-forecast, and sign by era. Log
  points are translated to percentages wherever a reader sees them.
- **A cell whose actual is zero or negative is not scored and is COUNTED.** The count of
  unscoreable cells is published per driver, because a denominator that quietly shrinks is how
  a bad driver looks good.
- **Uncertainty:** moving-block bootstrap over ORIGINS, block lengths **{2, 3, 4}** — the house
  robustness bar — 2,000 resamples, **seed 42**. Eleven scoreable origins support all three
  block lengths; nothing is excluded and no block length is chosen after the fact.
- **Sensitivity:** `w ∈ {0.5, 0.7, 0.9}` on D2/D3/D7, reported for every aggregate. Reported,
  never selected.
- **Decomposition:** the revenue error is decomposed into the three legs and, inside the unit
  window, the cables error into volume and realised price; the profit-before-tax error into
  revenue, cost of revenue by leg, SG&A, D&A, other items and net finance.
- **Eras, named in advance so the split is not chosen after seeing the signs:** **pre-float**
  (targets FY2015–FY2016), **first float** (FY2017–FY2021) and **second float** (FY2022–FY2025),
  cut at the two Egyptian devaluations of November 2016 and March 2022. **And per
  [R-FCAL-01 AMENDED 07-09-2026] the era cut is NOT the test:** a correction requires the sign
  to hold at **every cut the data admits** with at least five cells each side, and a bias whose
  sign depends on where the line was drawn is reported, never corrected for.

## 5 · Macro versus company, corrections, guidance

- **The split:** every origin is re-run (a) on the knowable inflation, currency and activity
  path — what was published at `o` — and (b) on **perfect foresight** of those same series.
  The difference is the macro share; the residual is the company share. **D1 carries no
  inflation term and must return a zero macro share by construction** — that is the split's
  own check, and if it does not return zero the split is wrong rather than interesting.
- **Corrections:** expanding window only, errors resolved before the origin, **half strength by
  default**, applied only where the bias holds its sign **at every cut the data admits**, reset
  after a structural break, aggregates rebuilt from adjusted drivers and tested adjusted
  against raw by origin. A correction enters the live drivers only if it passes its own test
  **and** is consistent with how that driver class is built across this market's book;
  otherwise it is a **watch flag** — recorded, graded live, acted on by nobody.
- **Guidance is scored and never consumed.** Management's own forward statements in the
  earnings releases are logged against outcome with their bias, and no driver reads them.

## 6 · The valuation-input block

Committed per origin beside the driver panel [R-FCAL-01 AMENDED 03-Sep-2026], from the same
statements and under the same point-in-time discipline: cash and equivalents · interest-bearing
debt · PP&E · depreciation and amortisation · the working-capital lines · the share count with
the par value it was footed against · capex, disclosed where the cash-flow statement gives it
and otherwise DERIVED by `capex = ΔPP&E + D&A` and **labelled derived**. FY2013, the year the
window reaches but the run does not test, is committed under `prior_year_anchor` rather than
`origins`, because recording it as an origin would misstate what this run tested. **A missing
item is recorded as missing with its reason, never omitted.**

## 7 · What would overturn this run

- A driver bias that reverses when the blend `w` moves inside its stated range is a finding
  about `w` and not about the company, and is reported as such.
- A cables bias that holds inside the unit window and reverses outside it is evidence the
  segment-level fallback is a different driver wearing the same name, and the two are then
  scored separately rather than pooled.
- If the method cannot beat FREEZE on net profit at any horizon, **that is this run's most
  important finding and it is written down plainly.** A method that cannot beat "no change"
  has not earned the precision it displays.
