# PRE-REGISTRATION — SCEM fundamental walk-forward

**Sinai Cement Company S.A.E. · EGX · market EG · 7 September 2026**

**This is the FUNDAMENTAL walk-forward [R-FCAL-01]** — the driver model rebuilt as it
stood at a past origin, projected forward, and scored against what the company actually
reported. It is not the price-engine walk-forward (`scem_study/backtest_5y.py`, band
coverage on the Monte Carlo cone) and it is not the technical walk-forward
(`engine/lab/ta_calibration/`). Three tests in this system carry that name.

Written **before a single error is computed**. Nothing below was chosen after seeing a
result; parameters are stated, never fitted, and sensitivities are reported, never
selected. The panel (`panel.py`) and the macro conditioning (`macro.py`) existed when
this was written; no scoring code did.

---

## 0 · Scope decision — FIVE sourceable fiscal years, so **LIGHT**

| | |
|---|---|
| sourceable fiscal years | **5** — FY2021, FY2022, FY2023, FY2024, FY2025 |
| scope under [R-FCAL-01] | **LIGHT** (5–7 years): the last five origins, horizons 1–3 |
| origins | FY2021, FY2022, FY2023, FY2024, FY2025 |
| horizons | 1, 2, 3 years |
| resolved cells per driver | **9** (FY2021 h1–3, FY2022 h1–3, FY2023 h1–2, FY2024 h1, FY2025 none yet) |

**Why the span stops at FY2021 and not earlier.** Sinai Cement publishes exactly six
documents and they are all it publishes: five audited annual filings and one reviewed
interim. The oldest, `SCC-AFS-A-1221.pdf`, is **Arabic**, and its figures are set in
Eastern Arabic numerals which no OCR route available here reads — the Arabic model
returns letters where the digits are and the English model returns no
thousands-separated figure at all on the statement pages. FY2020 is therefore **left
out and the window shortened**, never filled from a vendor: a fabricated cell corrupts
the very error this run scores. The attempt is logged in `fetch_attempts.json`.

**FY2025 is an origin with no resolved horizon.** It is declared as one because the
live forecast stands there, and it will grade at the FY2026 filing. Its cells are
reported as pending, not as passes.

---

## 1 · What this issuer discloses, and what it does not

**SINAI CEMENT DISCLOSES NO PHYSICAL VOLUME. ANYWHERE.** Not a tonne of clinker, not a
tonne of cement, not an installed capacity, not a utilisation rate, in any of the six
filings, in any year. Every OCR'd page of the FY2022 and FY2023 filings was searched
for tonne, tons, capacity and utilisation and the search returned nothing.

The consequence is stated here rather than discovered downstream. SIGCM clause 2 asks
for revenue as volume × price and cost as cost-per-unit; where the unit is not
disclosed the build **drops to the finest sourced level and FLAGS the gap**, and for
this issuer that level is the **cost-note line**. A tonnage taken from a plant register
is an industry-ring forecast driver and is not the company's own reported figure, so no
tonne enters this panel. Under [R-SIGCM-02] this run's revenue lines are at level
`derived`, never `unit`, and that is a fact about the disclosure rather than about the
effort.

---

## 2 · The driver list, by class

| # | driver | class | source, every year |
|---|---|---|---|
| D1 | revenue | output | face of the income statement |
| D2 | raw materials, supplies, fuel, power, packing sacks | variable cost | cost-of-sales note |
| D3 | wages and salaries in cost of sales | semi-fixed cost | cost-of-sales note |
| D4 | maintenance expenses in cost of sales | semi-fixed cost | cost-of-sales note |
| D5 | transfer and loading (outbound haulage) | variable cost | selling-expenses note |
| D6 | general and administrative expenses | overhead | face of the income statement |
| D7 | depreciation and amortisation | capital charge | cash-flow statement, tied to note 4 |
| D8 | finance expense | financing | face of the income statement |
| D9 | interest income | financing | face of the income statement |
| D10 | capital expenditure | capital | cash-flow statement |
| D11 | working capital | balance sheet | balance sheet, operating lines only |
| D12 | EBITDA | **aggregate, rebuilt from D1–D7** | — |
| D13 | net profit after tax | **aggregate, rebuilt from D1–D9 and tax** | — |

Three cost-note lines are **excluded by the basis-break register** and scored nowhere:
"Operation and Development fees" (disclosed FY2021–FY2023 only) and "Clay resource
fees" and "Subcontractor" (disclosed FY2024–FY2025 only). A unit driver is scored only
inside its own definition window.

---

## 3 · The mechanical rule for each driver, with its parameters

**No judgement drivers at a historical origin.** The exercise tests the method, not the
analyst. Every rule below is a function of figures the origin could see.

Two exogenous indices, from the IMF World Economic Outlook edition that **existed at
that origin** (`macro.py`), mapped from the IMF's fiscal-June Egypt year onto Sinai's
calendar year by taking half of each of the two fiscal years that span it:

- `V_h = Π_{j=1..h} (1 + realGDPgrowth_{t+j})` — the **activity** anchor. Cement is an
  activity-linked commodity whose marginal buyer is the state building programme, and
  the issuer discloses no volume of its own, so the volume leg comes from outside the
  company entirely rather than from its own trend.
- `P_h = Π_{j=1..h} (1 + CPI_{t+j})` — the **price** anchor.

| driver | rule |
|---|---|
| D1 revenue | `revenue_t · V_h · P_h` |
| D2 materials | `materials_t · V_h · P_h` — variable in volume, escalated at price |
| D3 cogs wages | `wages_t · P_h` — fixed in real terms |
| D4 cogs maintenance | `maint_t · P_h` — fixed in real terms |
| D5 transport | `transport_t · V_h · P_h` — variable |
| D6 G&A | `ga_t · P_h` — overhead, fixed in real terms |
| D7 D&A | PP&E roll-forward: `dep_h = dep_{h-1} + capex_{h-1} · r`, `r = 3.8626%`, the weighted rate note 3/2's disclosed rates imply on note 4's own gross-cost mix, which reproduces the filed FY2025 charge to within 1.2% |
| D8 finance expense | `kd_t · debt_{h-1}`, `kd_t` = the origin's own realised rate **on the borrowings that actually bear interest** (finance expense ÷ average of bank facilities + long-term bank loans + loans from affiliated companies + lease liabilities); debt held flat at the origin's level |
| D9 interest income | `r_dep,t · cash_{h-1}`, `r_dep,t` = the origin's own realised rate on average cash |
| D10 capex | `capex_t · P_h` — the disclosed run rate held flat in real terms |
| D11 working capital | `wc%revenue_t · revenue_h` |
| D12 EBITDA | rebuilt from D1–D6, never forecast directly |
| D13 net profit | rebuilt: EBITDA − D7 − D8 + D9 − tax; **tax by the regime known at the origin** — Egypt's 22.5% statutory rate on positive pre-tax profit, zero on a loss, loss carry-forward ignored and that stated |

**Both traps are honoured by construction and the pre-registration says so.**
*(i) Interest comes from the borrowings that actually bear it.* Suppliers, other credit
accounts, provisions and the deferred-tax liability pay nothing and are excluded. On
this name the two denominators differ by a factor of **1.7x to 5.9x**, so the broad one
would have manufactured a bias that looks exactly like evidence.
*(ii) Revenue and cost sit on the same recognition clock.* Sinai recognises revenue on
despatch and its cost of sales in the same period; there is no percentage-of-completion
leg, and the cost note's own total plus its change in inventory **is** the cost of sales
the income statement prints, every year, which is asserted rather than assumed.

---

## 4 · The two naive benchmarks

- **FREEZE** — every line flat at the last actual. `x_{t+h} = x_t`.
- **TREND** — trailing 3-year CAGR of that line, applied for h years. Where fewer than
  four points of history exist at the origin the window is shortened to the longest
  available with a minimum of two points; **at origin FY2021 only one point exists, so
  the trend benchmark is UNDEFINED there and that origin is scored against freeze
  alone**, recorded rather than filled.

**A method that cannot beat "no change" has not earned the precision it displays.** If
that is what this record shows, this record says so.

---

## 5 · The score

- Per driver, per horizon: **log error** `e = ln(projected / actual)`, defined only
  where both are strictly positive. **Where a line is negative or crosses zero the cell
  is DROPPED and counted** — Sinai's EBITDA is negative in FY2021 and FY2022 and its
  net profit is negative in FY2021, FY2022 and FY2023, so several aggregate cells are
  not on a log scale at all and pretending otherwise would be arithmetic wearing the
  costume of a measurement. Those cells are scored on a **signed relative error against
  the absolute actual** and reported in a separate table, never pooled with the logs.
- Bias (mean error), MAE, share over- and under-forecast, sign by era.
- **Block bootstrap over origins**, blocks {2, 3}, 2,000 resamples, the house bar.
  Block 4 is not run: with five origins a block of four leaves one degree of freedom
  and the interval it returns is not an interval.
- Skill against both benchmarks at every horizon: `1 − MAE_model / MAE_benchmark`.

---

## 6 · Eras, and the cut-invariance test

Two eras, and the boundary is the currency's, which is the right cut for a currency and
is **not** presumed to be the right cut for any driver:

- **E1 — before the float**: FY2021, FY2022 (target years to 2023).
- **E2 — the devaluation sequence and the recovery**: FY2023 onward.

Per [R-FCAL-01 AMENDED 07-09-2026] a bias may only be corrected where **its sign holds
at every cut the data admits**, every boundary leaving at least five cells each side.
**With nine cells per driver, no cut leaves five each side.** That is stated here, in
advance, and its consequence is stated with it: **no correction can be promoted from
this run on the cut-invariance test, whatever the biases turn out to be.** Every bias
this run measures is therefore a **watch flag** at best. A driver too thin to cut is
UNTESTABLE, never counted stable, because an absence of contrary evidence is not
evidence.

---

## 7 · The macro / company split

Every origin is re-run three ways:

1. **as known** — the WEO edition that existed at the origin (the base case above);
2. **perfect foresight of inflation** — the outturn CPI, activity left as believed;
3. **perfect foresight of both** — outturn CPI and outturn real GDP growth.

The macro share of a driver's miss is `(MAE_as_known − MAE_perfect) / MAE_as_known`.

**The split carries its own check.** A driver with no inflation term in its rule must
return a **zero** macro share on leg 2 by construction. D7 (D&A, a roll-forward off a
disclosed rate) has no CPI term in its first year and is the internal control.

**Outturn cells landing on 2025 are reported separately.** The latest WEO edition
obtainable here is April 2025, which *projects* 2025 rather than reporting it, so
perfect foresight of 2025 is a projection and is labelled as one rather than passed off
as an outturn.

---

## 8 · The roles of the two samples

- The **rolling record** (all nine resolved cells, overlapping) estimates candidate
  corrections.
- The **non-overlapping origins** (FY2021 and FY2024 at h=1; FY2022 at h=3) confirm
  them.

Corrections, if any: expanding window only, half strength by default, aggregates
rebuilt from adjusted drivers and tested adjusted-versus-raw by origin. A correction
enters the live drivers only if it passes its own test **and** is consistent with how
that driver class is built across the market's book. Given §6, this run expects to
promote **nothing** and to record watch flags instead.

**Guidance is scored, never consumed.** Sinai Cement publishes no forward guidance in
any of the six filings; the guidance ledger for this name is therefore empty and says so.

---

## 9 · What is internal

The panel, the error cells, this document, the basis-break register and the training
record are INTERNAL and never shown to a reader. The two documents [R-FCAL-01] requires
are the updated fundamental analysis and the lessons register.
