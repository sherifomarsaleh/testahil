# EGCH (KIMA) — fundamental walk-forward, pre-registration

**Written 1 September 2026, BEFORE a single forecast error was computed.** Fixed in
advance under [R-FCAL-01] §2. Parameters are stated, never fitted; sensitivities are
reported, never selected. An amendment after a result exists is tuning, not a choice
(L-042) — this file carries no amendments.

Ticker EGCH · Egyptian Chemical Industries "KIMA" · EGX · market EG · fiscal year ends
30 June · class: registered as *petrochemical* for reading the register; the company is a
gas-fed nitrogen-fertiliser producer (ammonia/urea since FY2020, ammonium nitrate from an
electrolytic plant before that), and whether that is its own class is proposed in the
report, not decided here.

**Which walk-forward this is:** the FUNDAMENTAL one — drivers projected from a past origin
and scored against what the company actually reported. Not the price-engine walk-forward
(band coverage on the Monte Carlo cone) and not the technical walk-forward.

**Queue position, recorded as a decision.** `campaign_queue.py --next` returns ARCC; EGCH
is second in the EGX reissue tier and was named explicitly by the user for this run. It
runs out of queue order on that instruction. ARCC's position is unchanged.

---

## 0 · Scope decision — FULL

**The archive supports eighteen sourceable fiscal years, FY2008 through FY2025**, all
July–June, all from KIMA's own audited statements on its own investor-relations channel,
plus the reviewed nine months to 31 March 2026. Under §0 that is a **FULL run**: every
origin from the first with five years of history, horizons 1–5.

What was attempted, and what came back:

| route | outcome |
|---|---|
| `kimaegypt.com` investor-relations page | reachable (HTTP 200); embeds the Mist IR portal |
| `mistnews.com/ir/financial.aspx` listing | timed out on one attempt, returned a 709-byte stub on the retry; the 08-08-2026 listing (`egch_study/filings/SOURCES.md`) is the index used |
| `mistnews.com/mistsat/companies/mezanyat/...` PDFs | **10 of 10 older annuals retrieved** (2009, 2010, 2011, 2013, 2014, 2016, 2018, 2019, 2020, 2021), each a real PDF; the 2022–2025 annuals and the three FY2025/26 interims were already held |
| `kima.com.eg` | refused at the egress proxy — it is not the company's domain |
| Egyptian Exchange | reachable but carries nothing older than the company's own portal |

**The window starts at FY2008 because that is the oldest comparative the company's own
archive carries** (the 2009 annual). It stops at FY2025 because FY2025/26 has not yet
been reported as a year. Nothing older exists on any channel reached.

**Consequences accepted in advance, not discovered later:**

- Three years exist only as comparatives (FY2008, FY2012, FY2015, FY2017 — the archive
  lists no annual for 2012, 2015 or 2017); FY2014 is partial (a 367×519 px scan whose
  profit lines cannot be read). These holes are left as holes — no year is estimated.
- The plant was replaced inside the window (B-2). The record will contain a group of
  cells where a mechanical method projects a business that then ceased to exist. That is
  the point of scoring across it, and the era split is drawn at it.
- Unit drivers exist only for FY2023–FY2025 (three cells). They are reported and cannot
  carry weight; the aggregates carry the record.

## 1 · Origins, horizons, cells

Origins are fiscal year ends, 30 June: **FY2012 through FY2024** — thirteen origins.
FY2012 is the first year with five years of history (FY2008–FY2012). Horizons
**h = 1…5**. A cell is scored only where the actual exists and the origin's inputs exist.

Maximum cells: 45 (origins FY2012–FY2020 × 5) + 4 + 3 + 2 + 1 = **55 per line**, less
the FY2014 holes on profit lines (targets from FY2012/FY2013 and every cell from origin
FY2014) and less the FY2020/FY2021 non-positive cells on profit lines (B-3).

**Point-in-time discipline.** Each origin sees only its own filing as first reported. An
origin at FY2022 sees gross profit 2,021,090 (not the 2,117,712 the FY2023 filing
restated it to); an origin at FY2009 sees cost of units sold 123,225,776. Comparative-only
origins (FY2012, FY2015, FY2017) see the next filing's comparative column, which is the
only column that exists, and that is flagged.

## 2 · Drivers — the mechanical rule and its parameters

**No judgement drivers. No rule reads guidance** (the 9M FY2026 filing prints a company
budget column; it is scored in §6 and consumed nowhere).

Notation: `o` origin, `h` horizon, `t = o + h` target. `Π CPI` = compounding Egyptian CPI
over the horizon on the path knowable at `o`. `FXk(t)` = the knowable currency path (§5).
`U(o)` = world urea price, fiscal-year mean of the World Bank monthly series, US$/t.

**THE MACRO PATH IS ONE PATH (L-048).** The knowable path at every origin holds the world
urea price flat in DOLLARS and moves the currency by relative purchasing-power parity on
the last published CPI differential: `FXk(t) = FX(o) × Π[(1+cpiEG)/(1+cpiUS)]`, with both
rates the last published calendar-year values at the origin. Domestic costs compound on
the same `cpiEG`. Inflation, the currency and the product price are therefore the same
event seen once. This is chosen here — before any result — because AMOC's record showed
that a path which compounds domestic inflation while freezing the currency manufactures
a one-sided profit miss out of the scenario rather than the company; it is a
pre-registration choice and its cost is that a currency that does NOT follow PPP (Egypt
held the pound through FY2017–FY2021 and then devalued in steps) will show up as macro
error, which is where it belongs.

| # | driver | rule | parameters |
|---|---|---|---|
| D1 | revenue | `rev(o) × [U_egp_k(t)/U_egp(o)]^β`, where `U_egp_k(t) = U(o) × FXk(t)` — i.e. the origin's realisation carried on the currency path | **β = 1.0**; β ∈ {0.5, 1.0} reported |
| D1v | urea tonnes (unit window FY2023+ only) | flat at the origin's actual | none |
| D2 | cost of sales | `cos(o) × Π CPI` | none; sensitivity: cost on the FX path for origins ≥ FY2021 |
| D3 | selling | `sell(o) × Π CPI` (only where disclosed as its own line) | none |
| D4 | admin | `admin(o) × Π CPI` | none |
| D5 | provisions formed | flat at the origin's actual | none — freeze-equivalent |
| D6 | other bucket (other revenues − other expenses ± the small items, EXCLUDING the FY2024 revaluation gain) | flat at the origin's actual | none — freeze-equivalent; L-050 is the reason a bucket is carried rather than zeroed, read as a provisional finding, not a rule |
| D7 | currency result | `−B_usd(o) × [FXk(t)/FXk(t−1) − 1]` for origins with bank borrowings (the KIMA-2 consortium loan is dollar-denominated); zero where borrowings are nil or entirely holding-company (EGP) | bank loans treated as 100% dollar — a stated simplification, since the filings do not split the EGP tranche year by year |
| D8 | investment income (dividends, associates) | flat at the origin's actual | freeze-equivalent |
| D9 | credit interest | flat at the origin's actual | freeze-equivalent |
| D10 | debit interest | `r(o) × B(o) × FXk(t)/FX(o)`, where `r(o) = debit(o) / B(o−1)` on OPENING interest-bearing borrowings (bank + holding company + current portion). **Where `B(o−1)` is below 10% of the year's revenue the rate is UNDEFINED and the charge is held flat** (L-041) | the 10% floor is stated, not fitted |
| D11 | income tax | `τ(o) × max(PBT, 0)` with τ the statutory rate in force at the origin (B-11); deferred tax and the solidarity contribution zero | τ ∈ {20%, 25%, 22.5%} by origin |

Aggregates rebuilt from those lines: gross profit = D1 − D2; profit before tax; net.

**What the table refuses, and why.** Interest is formed on the borrowings that bear it
and on nothing wider — supplier balances, provisions and the deferred-tax liability are
excluded from `B` by construction. Revenue and cost sit on the same recognition clock
(sale of goods, no percentage-of-completion). There is no cost-by-nature driver because
the notes as extracted do not foot (B-7). There is no volume driver outside the unit
window because no filing before FY2023 discloses tonnes in a table that has been read.

## 3 · Benchmarks

Both are computed at every scoreable cell, per line and on the aggregates.

- **FREEZE** — every line flat at the origin's last actual, in nominal EGP.
- **TREND** — every line grown at its own trailing CAGR over the longest window available
  at that origin, capped at three years; where the base or the origin value is
  non-positive the line is held flat. The window length is recorded in every cell.

**Declared in advance:** D5, D6, D8, D9 and D1v are level-persistence rules and are
therefore **identical to FREEZE by construction**. Their skill against FREEZE is "n/a —
rule equals benchmark", not a measurement. Their errors are still computed.

## 4 · Score, uncertainty, sensitivity

- **Score:** log error `e = ln(projected/actual)` per line per horizon, on cells where
  both are positive (B-3); the excluded count and a sign-hit rate are printed beside.
  Reported as bias, MAE, share over-forecast, sign by era.
- **Uncertainty:** moving-block bootstrap over ORIGINS, block lengths **{2, 3, 4}**, 2,000
  resamples, seed 42.
- **Sensitivity:** β ∈ {0.5, 1.0} on D1; cost of sales on the FX path instead of CPI for
  origins ≥ FY2021. Reported, never selected.
- **Decomposition:** the net-profit error into revenue, cost of sales, opex, other,
  currency, finance and tax contributions; the revenue error into realisation (all years)
  and, inside the unit window, volume vs realisation.
- **Every origin's projected-versus-actual income statement is shown side by side.**

## 5 · Macro versus company

Exogenous inputs are Egyptian CPI, US CPI, EGP/USD and the world urea price — nothing
else (the administered gas price is a company-specific fact, not a macro path). Every
origin is re-run three ways:

1. **Knowable** — the last published calendar-year CPI rates at the origin held flat, the
   currency on PPP from the fiscal-year level at the origin, urea flat in dollars.
2. **Perfect foresight** — the realised CPI, currency and urea-in-EGP paths.
3. **Perfect foresight of inflation only** — realised Egyptian CPI on the cost lines; the
   currency and urea on the knowable path.

`macro share = 1 − MAE(perfect foresight) / MAE(knowable)`, per line and per horizon.

**The split carries its own check:** D1v, D5, D6, D8 and D9 contain no CPI, no currency
and no urea term, so their macro share **must come back exactly zero by construction**. A
non-zero value there is a wiring error, not a finding, and the run fails rather than
reports it.

## 6 · One-offs and guidance

Every one-off in B-8 is classified and the headline record is reported with and without
the FY2024 revaluation gain. The company's own budget column in the 9M FY2026 interim
(revenue 7,150,675k; net 1,021,912k for the nine months) is scored against the outturn
and consumed by nothing.

## 7 · Samples, corrections, and what would make a finding worth acting on

Thirteen origins allow an expanding-window record. **Roles:** the rolling record
(all cells resolved before an origin) estimates a correction; the non-overlapping
origins {FY2012, FY2017, FY2022} confirm it. A correction on driver `d` at origin `o` is
`−½ × mean(e_d)` over the cells resolved before `o`, applied only where the sign has held
across every era resolved so far and the block bootstrap keeps the sign at every block
length; it RESETS at the plant replacement (B-2) and after any driver error beyond its own
two-sigma; aggregates are rebuilt from adjusted drivers and adjusted-vs-raw is reported by
origin. A correction enters the live drivers only if it passes that test **and** matches
how the driver class is built across the market's book; otherwise it is a watch flag.

Stated in advance so the bar is not set after the numbers arrive: with a plant
replacement in the middle of the window, a bias that holds its sign across all three
eras is the only kind this record could honestly promote, and the expectation — written
here before the run — is that most will not.

## 8 · Two purposes, not three

Per-driver bias detection and calibrated ranges on years 3–5. A better point estimate is
a by-product and never the aim.
