# ADIB (EGX) — FUNDAMENTAL walk-forward: pre-registration

**Written 09-Sep-2026, before a single error was computed.** INTERNAL — never shown to a
reader. [R-FCAL-01 §2].

**Which walk-forward this is.** The FUNDAMENTAL one: drivers projected from a past origin
and scored against what ADIB-Egypt actually reported. It is not the price-engine
walk-forward (`{ticker}_study/backtest_5y.py`, band coverage on the Monte Carlo cone) and
not the technical walk-forward (`engine/lab/ta_calibration/`, the shipped read replayed on
a 5/10/21-session clock).

**Which company.** Abu Dhabi Islamic Bank – Egypt S.A.E., EGX: ADIB, Cairo-listed, EGP.
Not ADIB Group PJSC (ADX: ADIB), which is the separate covered name ADIBUAE.

**Class.** `bank`. Registered in `engine/lessons_register.py`; L-111 binds
(a bank is valued on what reaches the shareholder, not on enterprise value).

---

## 0 · Scope — decided first

**FULL.** Sixteen sourceable consolidated fiscal years, FY2010–FY2025, every one from the
issuer's own audited consolidated statements on adib.eg, every one footing against its own
arithmetic. Sixteen ≥ eight, so: all origins from the first year with a five-year history,
horizons 1–5.

**Origins (11):** FY2014 … FY2024. FY2014 is the first year with five years of
consolidated history behind it (FY2010–FY2014). FY2024 is the last year that has at least
one matured horizon.

**Horizons:** 1–5, truncated at FY2025, the last reported year. **45 origin-horizon cells
per driver.**

| origin | matured horizons | targets |
|---|---|---|
| FY2014 | 1–5 | FY2015–FY2019 |
| FY2015 | 1–5 | FY2016–FY2020 |
| FY2016 | 1–5 | FY2017–FY2021 |
| FY2017 | 1–5 | FY2018–FY2022 |
| FY2018 | 1–5 | FY2019–FY2023 |
| FY2019 | 1–5 | FY2020–FY2024 |
| FY2020 | 1–5 | FY2021–FY2025 |
| FY2021 | 1–4 | FY2022–FY2025 |
| FY2022 | 1–3 | FY2023–FY2025 |
| FY2023 | 1–2 | FY2024–FY2025 |
| FY2024 | 1 | FY2025 |

**The era sub-sample is REPORTED, not selected.** Basis break B2 puts FY2010–FY2013 in a
loss-making, recapitalising era. Origins FY2014 and FY2015 therefore have loss years inside
their own trailing windows. Every result below is reported twice: on all 11 origins, and on
the 9 origins FY2016–FY2024 whose whole five-year history sits in the profit era. Neither
is the headline; both are printed side by side. Choosing between them after seeing the
scores is the selection mistake this rule exists to stop.

---

## 1 · The driver list, by class — and why it is not the industrial list

**A bank has no units × price, no capex, no D&A that matters, and no working capital in the
industrial sense.** Its drivers are a balance sheet that grows, a spread earned on it, a
loss rate charged against it, a fee annuity, an overhead base and a tax rate. The
industrial driver list is not forced onto it. What IS carried over unchanged is the
protocol's own discipline: **volume comes from an exogenous market driver, never the
company's own trend alone**, and **margins are outputs, never inputs** [L-005].

### The two named traps, and what each becomes for a bank

**Trap 1 — "interest comes from the borrowings that actually bear it."** For an industrial
company this rules customer deposits OUT of the denominator. **For a bank it rules them
IN**, and this inverts the example while leaving the rule intact. ADIB-Egypt's
`Cost of deposits and similar costs` is precisely the return paid to depositors and to
the banks and subordinated lenders that fund it. The denominator here is therefore
**customers' deposits + due to banks + subordinated financing**, on average balances, and
nothing else: not total liabilities (which would fold in EGP 11.4bn of other liabilities,
EGP 4.2bn of current tax and EGP 1.8bn of provisions at FY2025 and understate the funding
rate by roughly a sixth), and not total assets. The rule is obeyed by construction —
`cost_of_funds()` takes its denominator from `interest_bearing_liabilities()` and from
nothing else.

**Trap 2 — "revenue and cost sit on the same recognition clock."** A bank's financing
income and its cost of deposits already accrue on the same effective-yield clock, so the
industrial version of this trap cannot fire. **Its bank-shaped analogue can, and it is the
one this run must not commit: income accrues on AVERAGE balances, not closing ones.**
ADIB-Egypt grew customer financing 54% in FY2025 and its balance sheet 33%. Applying a
yield to the CLOSING balance rather than the average would credit a full year of income to
half a year of assets and inflate projected net profit by a large, robust, entirely
spurious margin — exactly the shape of the PHDC error, in a bank's clothing. Every rate
driver below is applied to an **average of opening and closing balances**, and the closing
balance is never used as a rate base anywhere in the build.

### The rules

Every input to every rule is a figure published on or before its own origin. **No judgement
drivers at historical origins.** `k` is the trailing window and is **3 years** everywhere,
shortened only where the panel does not reach back that far.

| # | driver | mechanical rule at origin `o`, for horizon `h` |
|---|---|---|
| **R1** | **System credit (exogenous)** | Egyptian banking-system credit to the private sector in EGP = `credit_priv_pct_gdp × gdp_lcu` (World Bank WDI FS.AST.PRVT.GD.ZS and NY.GDP.MKTP.CN). Projected at its own trailing 3-year CAGR **computed on the series published through `o−1`**, because the current year's national accounts are not published at a December origin. This is the exogenous market driver. |
| **R2** | **Customer financing (volume)** | `share_o` = ADIB net customer financing / system credit at `o`, **held flat**. `financing(o+h) = system_credit(o+h) × share_o`. The company's own growth rate is never extrapolated on its own. |
| **R3** | **Customers' deposits** | `financing(o+h) / LDR_o`, where `LDR_o` is the trailing-`k` mean of financing / deposits. |
| **R4** | **Total assets** | `deposits(o+h) × M_o`, where `M_o` is the trailing-`k` mean of total assets / customers' deposits. |
| **R5** | **Interest-bearing liabilities** | `deposits + due_to_banks + subordinated`, the last two held at their trailing-`k` mean ratio to deposits. |
| **R6** | **Asset yield** | trailing-`k` mean of `fin_income / average total assets`. → `fin_income(o+h) = yield_o × avg_assets(o+h)`. |
| **R7** | **Cost of funds** | trailing-`k` mean of `−cost_funds / average interest-bearing liabilities`. → `cost_funds(o+h)`. **NIM and net financing income are OUTPUTS of R6 and R7 and are never inputs.** |
| **R8** | **Net fee income** | trailing-`k` mean of `net_fees / average total assets`. Window opens at FY2012 (break B3). |
| **R9** | **Other non-interest income** | trailing-`k` mean of `other_nii / average total assets`. `other_nii` is the derived block: dividends + trading + associates + investment and disposal gains. |
| **R10** | **Administrative expenses** | **Two-part, as the protocol specifies overheads.** `admin(o+h) = F_o × CPI_index(o+h)/CPI_index(o) + v_o × avg_assets(o+h)`, where `(F_o, v_o)` are the intercept and slope of an ordinary least squares of real admin on real average assets over the trailing `k+1` years, both deflated to origin-year money. Where fewer than 3 points are available, or the OLS returns a negative `v_o`, the rule falls back to **`admin(o+h) = admin_o × Π(1+cpi)`** — pure inflation escalation, which is the rule every other EGX run in this campaign uses. Which branch fired is recorded per origin. `(F_o, v_o)` are computed from origin-only data by a procedure stated here in advance; they are not tuned. |
| **R11** | **Other operating expenses** | trailing-`k` mean of `other_op / average total assets` (signed; the line is income in FY2015–FY2016 and expense elsewhere). |
| **R12** | **Cost of risk** | trailing-`k` mean of `−ecl / average net customer financing`. Not floored: a release is a real observation and flooring it at zero would be a judgement. → `ecl(o+h)`. |
| **R13** | **Tax** | **Primary:** trailing-`k` mean of `−tax / pbt`, clipped to [0, 0.80]. **Sensitivity, reported never selected:** the Egyptian statutory corporate rate known at the origin (22.5% from FY2015; 25% before). Both are computed at every origin and both are printed. |
| **R14** | **Attributable profit** | `np_parent = pbt × (1 − tax_rate) × (1 − nci_share_o)`, `nci_share_o` the trailing-`k` mean of `nci / np`. |
| **R15** | **Inflation path** | CPI projected at the trailing 3-year mean of published Egyptian CPI inflation (WDI FP.CPI.TOTL.ZG), on the series **published through `o−1`**. |

**Everything below the driver line is an output**: net financing income, NIM, cost-to-income,
gross profit, PBT, net profit, ROE, ROA. None is an input anywhere.

---

## 2 · The two naive benchmarks

Both are computed at every origin and every horizon, on every scored line.

- **FREEZE** — every line flat at its last actual: `x(o+h) = x(o)`.
- **TREND** — every line grown at its own trailing 3-year CAGR: `x(o+h) = x(o) × (1+g)^h`,
  `g` = CAGR of `x` over `[o−3, o]`. Where `x(o−3)` and `x(o)` do not share a sign, TREND is
  undefined for that line at that origin and the cell is dropped from TREND's score and from
  no other. (This happens on `pbt` and `np` at the FY2014 and FY2015 origins, where the
  window reaches into the loss era.)

**Skill is reported against both, at every horizon.** A method that cannot beat "no change"
has not earned the precision it displays, and where that happens this study will say so.

---

## 3 · The score

Per driver, per horizon: **log error `e = ln(projected / actual)`** where both are strictly
positive. Where a line changes sign between projection and actual, the log error is
undefined and the cell is recorded as **SIGN-BROKEN** and reported by count — it is never
replaced by a signed percentage, and it is never dropped silently.

Reported per driver per horizon: **bias** (mean `e`), **MAE** (mean `|e|`), **block-bootstrap
90% confidence interval**, **share of origins over-forecast**, and **sign by era**
(FY2014–FY2017 origins vs FY2018–FY2024 origins).

**Block bootstrap:** the resampling unit is the WHOLE ORIGIN — all of an origin's horizons
move together — because horizons within an origin share the origin's own trailing window and
are not independent. 10,000 resamples, seed 20260909, percentile interval.

**A bias that changes sign between eras is not a bias.** It is reported as instability and is
not corrected for.

---

## 4 · Macro / company split

**Exogenous:** Egyptian CPI inflation, EGP/USD, nominal GDP, banking-system credit to the
private sector, the CBE policy-rate regime, the statutory tax regime. **Endogenous:** ADIB's
share of system credit, its LDR, its asset yield, its cost of funds, its fee and other-income
ratios, its overhead base, its cost of risk, its NCI share.

Every origin is re-run three ways:

1. **AS PRE-REGISTERED** — macro projected mechanically from origin-available data (R1, R15).
2. **PERFECT MACRO** — the realised CPI path and the realised system-credit path substituted,
   every company driver left exactly as in (1).
3. **PERFECT FORESIGHT** — every driver set to its realised value; the residual is arithmetic
   error and must be zero.

`macro share = (error in 1 − error in 2) / error in 1`, per driver per horizon.
`company share = 1 − macro share`.

**The split's own check, in its bank form.** The protocol's check is that a unit volume
driver carries no inflation term and must return a zero macro share by construction. A bank
has no unit driver — every line it reports is nominal EGP. The bank-shaped equivalent is
**ADIB's share of system credit**: numerator and denominator are nominal EGP in the same
year, so inflation cancels identically and the share driver **must return a macro share of
exactly zero**. If it does not, the split is wired wrong and no result below it is safe.

---

## 5 · The two samples, and their roles

- **The rolling record** — all 45 origin-horizon cells — ESTIMATES candidate corrections.
- **The non-overlapping origins** — FY2014, FY2019 and FY2024, which share no target year —
  CONFIRM them. Three origins is a small confirmation set and that limitation is stated in
  the caveats rather than worked around.

**Corrections.** Expanding window only (errors resolved strictly before the origin), half
strength by default, applied only where the bias holds its sign across both eras, reset at
break B2. Aggregates rebuilt from adjusted drivers and tested adjusted-vs-raw by origin. A
correction enters the live drivers only if it passes its own test **and** is consistent with
how that driver class is built across the market's book; otherwise it is a **watch flag** —
recorded, graded live, acted on by nobody [L-003].

**Guidance is scored, never consumed.** ADIB-Egypt publishes no numeric forward guidance in
its consolidated statements; where the Board of Directors report or the IR pack carries a
forward statement it is recorded in the guidance ledger and scored against outcome. It is
never an input to any rule above.

---

## 6 · What is fixed here and may not move

- The origin list, the horizon list, the 13 driver rules and their `k = 3`.
- Both benchmarks and the log-error score.
- 10,000 bootstrap resamples, seed 20260909, origin as the block.
- The era split at FY2016 origins, reported alongside and never instead.
- The three-way macro re-run and its zero-macro-share check on the share driver.

Parameters are stated, never fitted. Sensitivities are reported, never selected.
