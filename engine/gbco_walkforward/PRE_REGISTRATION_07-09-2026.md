# GBCO — FUNDAMENTAL walk-forward [R-FCAL-01]: pre-registration

**Written 07 September 2026, BEFORE a single error was computed.** Internal. Never shown
to a reader.

**WHICH WALK-FORWARD.** This is the FUNDAMENTAL one — the driver model rebuilt as it stood
at a past origin, projected forward, each driver scored against what GB Corp actually
reported. It is not the price-engine walk-forward (`gbco_study/backtest_rows.csv`, band
coverage on the Monte Carlo cone) and it is not the technical walk-forward
(`engine/lab/ta_calibration/`). The three are different machinery on different evidence.

## 0 · Scope decision, made first

**FULL.** Fourteen sourceable fiscal years, FY2012–FY2025, every one tier A from a document
GB Corp published itself, every one footed against its own arithmetic before entering the
panel (`build_panel.py`). ≥8 years, so §0's FULL branch applies: origins from the first year
with five years of history (FY2016) to the last testable one (FY2024), horizons 1–5.

Origins: **FY2016, FY2017, FY2018, FY2019, FY2020, FY2021, FY2022, FY2023, FY2024** — nine.
Horizons 1–5, scored only where the actual exists (≤FY2025): 5+5+5+5+5+4+3+2+1 = **35 cells
per driver**, before any cell is dropped for a driver whose definition window does not reach.

## 1 · Data and its provenance

Source of record, in the order the archive supplies it:

| span | document | route | tier |
|---|---|---|---|
| FY2012–FY2018 | GB Auto annual report for that year, reproducing the audited consolidated statement of income | PDF text layer | A |
| FY2019–FY2025 | GB Corp's OWN 4Q earnings release for that year — the figures **as originally reported at that origin** | PDF text layer | A |
| balance sheet, FY2019–FY2025 | the same releases' segmented balance sheet (GB Auto / GB Capital / elimination / group) | PDF text layer | A |
| 1H2026 | 2Q26 earnings release, 13 August 2026, and the reviewed consolidated statements to 30 June 2026 | text layer / scanned | A |

The audited consolidated statement PDFs for FY2022–FY2025 and both 2026 interims carry **no
text layer at all** (0 characters across 51–60 pages). The same audited statements, with the
same auditor's report, are reproduced inside the annual report for each year and those DO
carry a text layer, so the annual report is the ROUTE and the audited statement is the
DOCUMENT. Where both exist (FY2020, FY2021) the figures were cross-read and agree.

**Never estimate, interpolate or infer.** A year that cannot be sourced is left out and the
window shortened.

## 2 · Basis-break register (built before modelling)

| break | year | treatment |
|---|---|---|
| EGP float | Nov 2016 | era boundary A: FY2012–FY2016 "pre-float", FY2017–FY2021 "post-float", FY2022–FY2025 "second devaluation cycle" |
| EGP devaluations | Mar 2022, Oct 2022, Jan 2023, Mar 2024 | era boundary B |
| **Operating-profit definition moved** | between the 4Q24 and 4Q25 releases | provisions sit BELOW operating profit in the FY19–FY24 vintages and ABOVE it in the FY25 vintage. Arithmetic confirms it is presentation only: FY2024 6,176.6 − 355.7 = 5,820.9 against the FY25 vintage's 5,820.8. **Scored on the ORIGINAL vintage at each origin**, which is what point-in-time means. |
| GB Capital deconsolidation of revenue presentation | FY2023 | GB Capital revenue falls 7,995.1 → 4,463.2 while the group's total does not move proportionately; the segment driver is scored only inside its own definition window |
| MNT-Halan stake revaluation | FY2022 | EGP 8,207.3mn one-off gain inside FY2022 EBT — classified as a one-off, and the net-profit driver is scored both with and without it |
| Company renamed GB Auto → GB Corp | 2023 | naming only; the consolidation is continuous |
| **FY2025 audit opinion is QUALIFIED** | FY2025 | the auditors were not provided with MNT-BV's consolidated audited financials for 2025 and the group's ~44% share of its profit rests on management-prepared statements. Recorded, not adjusted. |

## 3 · Drivers, and the MECHANICAL rule for each

No judgement drivers at historical origins. Every rule below is computable from the panel
as it stood at the origin, with no input from anything published later.

| driver | mechanical rule at origin *t*, for h = 1..5 |
|---|---|
| `revenue` | trailing 3-year revenue CAGR, applied and **damped 20% a year** toward the trailing mean growth |
| `gross_margin` | trailing 3-year mean of GP/revenue, **held flat** across the horizon |
| `gross_profit` | `revenue` × `gross_margin` — an OUTPUT, never an input |
| `sga_ratio` | trailing 3-year mean of (selling + admin)/revenue, held flat |
| `operating_profit` | gross profit − SG&A + trailing 3-year mean other income ratio − trailing 3-year mean provisions ratio |
| `finance_cost` | **the auto leg's own interest-bearing borrowings × the rate those borrowings actually bear.** Never the group finance charge over a broader liabilities total: GB Capital's borrowings fund a LENDING BOOK and their interest is that leg's cost of revenue, not the group's cost of debt. Where the segmented split is not disclosed at the origin the driver is recorded UNTESTABLE for that origin rather than computed on a blended denominator. |
| `tax_rate` | the Egyptian statutory corporate rate known at that origin (22.5% from FY2015; 25% before) |
| `net_profit` | operating profit + associates − finance cost, taxed at `tax_rate` |
| `capex` | trailing 3-year mean capex/revenue × projected revenue |

**Revenue and cost sit on the same recognition clock.** GB Corp recognises vehicle revenue at
delivery and its cost of revenue with it; GB Capital recognises finance income over the life
of the receivable and its funding cost with it. The two legs are therefore built and scored
SEPARATELY wherever the disclosure supports it, and never netted into one margin.

**NOT RUN, and recorded rather than faked:** a volume-anchored revenue driver
(Egypt passenger-car market registrations × GB Corp share × price per unit). Unit volumes are
disclosed in the earnings releases from FY2019 and in the annual-report business reviews
before that, but an exogenous market-size series dated at EVERY origin from the company's own
documents was not obtained inside this run. Under §1 the honest outcome is to flag the gap,
not to substitute a third-party series mid-run. Revenue is therefore scored at the group and
segment level only, and the driver ledger records the gap.

## 4 · Benchmarks, score and inference

- **freeze** — every line flat at the last actual. **trend** — trailing 3-year CAGR on every line.
- **score** — log error `ln(projected / actual)` per driver per horizon; bias = mean, MAE = mean |·|.
- **CI** — block bootstrap over ORIGINS (block sizes 2, 3, 4; 2,000 resamples), because cells
  from one origin are not independent.
- **macro/company split** — every origin re-run (a) on the knowable Egyptian inflation path and
  (b) on perfect foresight of it. **Volume drivers carry no inflation term and must return a
  zero macro share by construction** — that is the split's own check.
- **eras** — boundary A (the 2016 float) and boundary B (the 2022–24 devaluation cycle), plus
  **every cut the data admits** leaving at least five cells each side [R-FCAL-01 AMENDED
  07-09-2026]. A bias whose sign depends on where the line was drawn is reported, never
  corrected for.
- **samples** — the rolling record estimates corrections; the non-overlapping origins confirm them.

Parameters are STATED, never fitted. Sensitivities are reported, never selected. A better
point estimate is a by-product and is not the aim.

## 5 · Corrections

Expanding window only, half strength by default, applied only where the bias holds its sign at
**every cut the data admits**, reset after a structural break, aggregates rebuilt from adjusted
drivers and tested adjusted-vs-raw by origin. A correction enters the live drivers only if it
passes its own test AND is consistent with how that driver class is built across the market's
book; otherwise it is a **watch flag**. Guidance is scored, never consumed.

## 6 · What would overturn this run

That the release-vintage figures differ materially from the audited statements they precede.
Both are held; where they disagree the disagreement is the finding, not a reason to pick one.
