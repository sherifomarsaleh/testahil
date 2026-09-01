# AMOC — fundamental walk-forward, pre-registration

**Written 1 September 2026, BEFORE a single forecast error was computed.** Fixed in
advance under [R-FCAL-01] §2. Parameters are stated, never fitted; sensitivities are
reported, never selected. An amendment after a result exists is tuning, not a choice
(L-042) — this file carries no amendments.

Ticker AMOC · Alexandria Mineral Oils Company S.A.E · EGX · market EG · class: petrochemical
(refining and specialty base oils / paraffin wax).

**Which walk-forward this is:** the FUNDAMENTAL one — drivers projected from a past origin
and scored against what the company actually reported. Not the price-engine walk-forward
(band coverage on the Monte Carlo cone) and not the technical walk-forward.

---

## 0 · Scope decision — LIGHT

**The archive supports five sourceable fiscal years: FY2021 through FY2025**, all July–June,
all from AMOC's own audited consolidated financial statements on its own investor-relations
archive. Under §0 that is a **LIGHT run**: the last five origins, horizons 1–3.

What was attempted for more, and what came back:

| route | outcome |
|---|---|
| `amoc.com.eg` | does not resolve — **it is not the company's domain**; the archive is `amoceg.com` |
| `amoceg.com` investor pages | **104 documents, 104 retrieved**; oldest annual accounts are FY2022 (carrying FY2021 as comparative) |
| Egyptian Exchange, FRA disclosure portal | refused at the egress proxy |
| Wayback Machine (older amoceg.com snapshots) | refused at the egress proxy; the availability API reports no snapshots |
| stockanalysis.com | FY2021–FY2025 only — the same five years, and restated rather than as-reported |

**The window stops at FY2021 because that is the oldest year AMOC itself publishes.** It
was not shortened for convenience and it was not padded to reach a threshold.

**Consequences accepted in advance, not discovered later:**

- **Nine scoreable origin-horizon cells per driver**, and that is the whole sample:
  FY2021 h1–h3, FY2022 h1–h3, FY2023 h1–h2, FY2024 h1. FY2025 has no matured horizon.
- **History at each origin is short.** An origin at FY2021 has one year behind it; FY2022
  two; FY2023 three; FY2024 four. **No driver rule may require more than one year of
  history**, or the early origins vanish. This shapes every rule in §2 and is the reason
  several are level-persistence rules moved by an exogenous path.
- **NO CORRECTION WILL BE ESTIMATED FROM THIS RECORD.** Nine cells cannot support an
  expanding-window correction and a separate confirmation sample. Every bias this run
  finds is recorded as a **WATCH FLAG** and nothing is fed into the live drivers. This is
  decided here, before any number exists, precisely so that a large clean-looking bias
  cannot later argue its own way into the model.
- **The era split cannot be load-bearing.** Three devaluations fall inside the window
  (B-9) but with five origins a by-era bias is one or two observations per era. It is
  computed and reported as instability, never as a correction.

## 1 · Origins and horizons

Origins are fiscal year ends, 30 June: **FY2021, FY2022, FY2023, FY2024, FY2025**.
Horizons **h = 1, 2, 3** years. A cell is scored only where the actual exists.

**Point-in-time discipline.** Each origin sees only what had been published by that date,
as originally reported. Two consequences bind here:

- FY2024's origin sees **majority profit 1,699,154,495**, its as-first-reported figure —
  not the 1,439,557,574 the FY2025 filing later restated it to (B-6).
- FY2022's origin sees the FY2022 filing's own other-revenue / investment-revenue split
  (B-5), not the FY2023 filing's restatement of it.

## 2 · Drivers — the mechanical rule and its parameters

Built on the constant eight-line taxonomy of B-2. **No judgement drivers.** No rule reads
guidance: management's forward targets lean the same way an optimistic model does, so a
driver taking guidance as an input inherits the lean instead of correcting for it.

Notation: `o` = origin, `h` = horizon, `Π CPI` = compounding Egyptian CPI over the horizon
on the path knowable at `o`, `BR(y)` = Brent in EGP for fiscal year y (monthly-mean Brent
USD × EGP/USD, derived on AMOC's July–June year).

| # | driver | rule | parameters |
|---|---|---|---|
| D1 | total throughput, tonnes | flat at the origin's actual | none |
| D2 | product mix, share of tonnes by the eight lines | flat at the origin's actual shares | none |
| D3 | realisation EGP/t, per line | `r(o) × [BR(o+h)/BR(o)]^β` | **β = 1.0** |
| D4 | raw materials (feedstock) | `rawPerTonne(o) × tonnes(o+h) × [BR(o+h)/BR(o)]^β` | **β = 1.0**, same β as D3 |
| D5 | salaries in cost of sales | `s(o) × Π CPI` | none |
| D6 | supporting materials | `perTonne(o) × tonnes(o+h) × Π CPI` | none |
| D7 | other cost of sales (gas, power, water, spares, EPROM) | `perTonne(o) × tonnes(o+h) × Π CPI` | none |
| D8 | depreciation in cost of sales | flat at the origin's actual | none |
| D9 | general and administrative | `ga(o) × Π CPI` | none |
| D10 | marketing and selling | `perTonne(o) × tonnes(o+h) × Π CPI` | none |
| D11 | other operating expenses | flat at the origin's actual | none |
| D12 | claims and disputes provision | flat at the origin's actual | none |
| D13a | other revenue — credit interest | `ci(o) × Π CPI` | none |
| D13b | other revenue — FX gain | **zero at every horizon** | none |
| D13c | other revenue — reversals, compensations, disposals, misc | **zero at every horizon** | none |
| D14 | investment revenue (ASPC dividend) | flat at the origin's actual | none |
| D15 | finance expenses | flat at the origin's actual — **the borrowing-rate driver is declared UNDEFINED for this name** | none |
| D16 | income tax | `22.5% × PBT` (Egyptian statutory rate) | **22.5%** |
| D17 | deferred tax | zero | none |
| D18 | non-controlling interest | origin's actual NCI share of net profit after tax, held flat | none |

### Three things about that table are the substance of the design

**D3 and D4 escalate on the SAME index with the SAME exponent, deliberately.** AMOC buys
fuel oil and wax distillate from EGPC and sells refined products drawn from the same
barrel, in the same months. Revenue and its dominant cost are one commodity complex, and
raw materials are **90.7% of cost of sales** (FY2025, note 15-A). Escalating the sell side
and the buy side on different indices would manufacture a margin path out of the index
choice alone — which is L-009's finding restated for a refiner, and on a pass-through
business it would be the entire result rather than a distortion of it. β is set to 1.0 and
**stated, not fitted**; β ∈ {0.8, 1.2} is reported as a sensitivity in §4 and is never
selected on the basis of its score.

**The borrowing-rate driver is refused, not widened (D15).** AMOC's interest-bearing
borrowings were EGP 20,977,437 at 31 December 2025 against total equity of EGP
4,824,774,948 — the company is effectively unlevered, and it holds net cash. A rate formed
on a denominator that small is noise, and the tempting repair is to divide the finance
charge by a broader liabilities total until the answer looks sensible. That is the trap
[R-FCAL-01] §3 names first and it is how a spurious bias gets manufactured. **The rate is
left undefined and the charge is held flat.** This is the pre-registered treatment, decided
before any number was computed, and it is an independent second observation of L-041.

**Cost is never driven per product, because there was no per-product costing system
(B-7).** Note 14-A gives revenue and tonnage per product for every year. Note 15-A gives
cost by NATURE for the company as a whole and never by product, and the FY2023 auditor
records that AMOC implemented a per-product costing system only from 1 July 2023. Every
per-line cost or per-line margin is therefore a construction; at these origins it is one
the company states it could not itself perform. **No per-product cost driver is
specified.** Revenue is built per line; cost is built by nature against total throughput.

## 3 · Benchmarks

Both are computed at every scoreable cell, per driver and on the aggregates.

- **FREEZE** — every line flat at the origin's last actual, in nominal EGP.
- **TREND** — every line grown at its own trailing CAGR over the longest window available
  at that origin, capped at three years. **Declared in advance:** the window is 0 years at
  origin FY2021 (no prior year — TREND is *not scored* there), 1 year at FY2022, 2 at
  FY2023, 3 at FY2024. The window length is recorded in every cell.

**Declared in advance, so it is not later reported as a finding:** D1, D2, D8, D11, D12,
D14 and D15 are level-persistence rules and are therefore **identical to FREEZE by
construction**. Their skill against FREEZE is zero by definition, not by measurement, and
will be reported as "n/a — rule equals benchmark" rather than as a result. Their ERRORS are
still computed and decomposed, which is the part that carries information. The rules that
can differ from FREEZE are D3, D4, D5, D6, D7, D9, D10, D13, D16 and D18, and the
aggregates built from them.

## 4 · Score, uncertainty, sensitivity

- **Score:** log error per driver per horizon, `e = ln(projected / actual)`. Reported as
  bias `mean(e)`, `MAE = mean(|e|)`, share of cells over- and under-forecast, and sign by
  era. Log points are translated to percentages wherever a reader sees them.
- **Uncertainty:** moving-block bootstrap over ORIGINS, block lengths **{2, 3}**, 2,000
  resamples, **seed 42**. Block 4 is excluded and the reason is stated in advance: with
  five origins a block of four leaves almost no resampling freedom and its interval would
  be an artefact of the block length, not a measurement.
- **Sensitivity:** β ∈ {0.8, 1.0, 1.2} on D3/D4 jointly, reported for every aggregate.
  Reported, never selected.
- **Decomposition:** the revenue error is decomposed into volume, mix and realisation; the
  net-profit error into revenue, cost of sales, opex, other revenue and tax.
- **Every origin's projected-versus-actual income statement is shown side by side.**

## 5 · Macro versus company

Exogenous inputs are Egyptian CPI, EGP/USD and Brent — nothing else. Every origin is
re-run three ways:

1. **Knowable** — the last published annual value at the origin, held flat forward. No
   forecast of a macro variable is permitted at an origin.
2. **Perfect foresight** — the realised CPI and Brent-in-EGP path.
3. **Perfect foresight of inflation only** — to separate the currency and crude channels
   from the domestic-cost channel.

`macro share = 1 − MAE(perfect foresight) / MAE(knowable)`, per driver and per horizon.

**The split carries its own check:** D1, D2, D8, D11, D12, D14, D15 contain no CPI and no
Brent term, so their macro share **must come back exactly zero by construction**. A
non-zero value there is a wiring error in the split, not a finding, and the run fails
rather than reports it.

## 6 · One-offs

Every one-off in the window is identified and the record is shown with it classified:
the FY2022 export-fuel-oil stop (B-3), the FY2024 restatement (B-6), FX gains inside other
revenue (D13b), and provision reversals (D13c). Classification is disclosed; the headline
record is reported on the unclassified basis as well, so nothing rests on the choice.

## 7 · What would make this run's findings worth acting on

Stated in advance so the bar is not set after the numbers arrive: a bias here would need
to hold its sign across both eras, survive the block bootstrap at both block lengths, and
match how the same driver class is built across the market's book. **Even then it would
not be adopted on this record**, because §0 has already ruled that nine cells cannot
support a correction. What this run can honestly produce is a per-driver map of where the
method breaks on a pass-through refiner, calibrated ranges for years 3–5 built from the
measured error distribution, and lessons scoped no wider than the evidence carries.
