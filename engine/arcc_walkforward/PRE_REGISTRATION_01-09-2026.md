# ARCC — pre-registration
### Fundamental walk-forward. Written 01-Sep-2026, BEFORE any error was computed.

Per [R-FCAL-01] §2 this document fixes the origins, the horizons, the driver
list, the mechanical rule and parameters for every driver, both naive
benchmarks, the score, the bootstrap, the macro conditioning, and the roles of
the two samples — **in writing, before a single error exists**. Parameters are
stated, never fitted. Sensitivities are reported, never selected.

Read first, and binding on what follows: `python3 engine/lessons.py ARCC --class
"cement and heavy industrial"`. L-002, L-003, L-005, L-009, L-010, L-028, L-029,
L-030 and L-110 all bind here and each is named at the driver it governs.

---

## 0 · Scope decision — decided first, and stated

**FULL.** Twelve sourceable fiscal years, FY2014 through FY2025, every one from
ARCC's own audited consolidated filings, downloaded from the company's own
website. The threshold for a full run is eight.

Origins run from the first year carrying five years of history (FY2018, which
sees FY2014–FY2018) to the last year with a matured horizon (FY2024). Horizons 1
to 5, truncated where the actual has not yet been reported.

| origin | sees | horizons graded |
|---|---|---|
| 2018 | 2014–2018 | 1–5 (2019–2023) |
| 2019 | 2015–2019 | 1–5 (2020–2024) |
| 2020 | 2016–2020 | 1–5 (2021–2025) |
| 2021 | 2017–2021 | 1–4 (2022–2025) |
| 2022 | 2018–2022 | 1–3 (2023–2025) |
| 2023 | 2019–2023 | 1–2 (2024–2025) |
| 2024 | 2020–2024 | 1   (2025) |

**25 graded cells per driver.** Cells are not independent: horizons from one
origin share an origin, and origins overlap. This is stated here rather than
discovered in the results, and it is why the confidence intervals below come
from a block bootstrap over origins and not from a t-test over cells.

---

## 1 · The drivers, and the mechanical rule for each

**NO JUDGEMENT DRIVERS AT HISTORICAL ORIGINS.** Every rule below is arithmetic
on figures published by the origin date. The exercise tests the method, not the
analyst. Where a rule needs a parameter it is fixed here and applied at every
origin identically.

### D1 · Sales volume (thousand tonnes) — exogenously anchored

    vol(h) = national(origin) × (1 + g_nat)^h × share(origin)
    g_nat  = trailing 3-year CAGR of Egypt's national cement market at the origin
    share  = ACC's own market share as reported at the origin

Anchored on the country's market and the company's share of it, **never on the
company's own volume trend** (§3). Both inputs come from ARCC's own releases,
which publish the national market beside ACC's volume. Capped at the origin's
disclosed cement production capacity implied by its utilisation rate: a volume
forecast above the plant's stated capability is not a forecast, it is an error.

**AMENDMENT A-1, made 01-Sep-2026 before any error was computed, for a SOURCING
reason and not a results one.** The rule as first written projected total volume
as *national total market × ACC total share*. Egypt's national market is reported
by ARCC as domestic + export up to FY2020 and as "Cement Domestic Sales" from
FY2021, so a consistent total-market series does not exist across the window
while a domestic one does. The rule therefore becomes:

    vol(h) = dom(h) + rest(origin)
    dom(h) = national_dom(origin) × (1 + g_nat)^h × share(origin)
    share  = ACC domestic cement volume ÷ national domestic market, at the origin
    rest   = everything that is not domestic cement — exports, and local clinker
             where disclosed — held flat at the origin's level

The export leg is held flat rather than grown because ARCC's disclosure carries
no exogenous anchor for global clinker demand, and inventing one would be a
judgement driver at a historical origin. Holding it flat is stated as the
conservative mechanical choice, and its consequence is reported rather than
tuned away.

**The share reproduces the company's own published ratio**, which is the check
that the numerator and denominator describe the same thing: FY2019 8.14% against
a printed 8.1%, FY2021 5.58% against 5.6%, FY2022 6.29% against 6.3%. Local
clinker is deliberately outside the numerator — including it breaks the
reproduction (FY2022 6.95% against a printed 6.3%), and a denominator that
cannot reproduce the company's own ratio is the wrong denominator.

### D2 · Revenue per tonne, cement segment (EGP/t) — two legs, two escalators

    rpt(h) = rpt(origin) × Π[ w_dom×(1+cpi_t) + w_exp×(1+fx_dep_t) ]
    w_exp  = export share of ACC volume at the origin;  w_dom = 1 − w_exp

Domestic cement is priced in pounds and tracks domestic inflation. Exports are
priced in dollars and track the exchange rate. Weighted by the export share **as
it stood at the origin** — never by a later share the origin could not know
[B-6].

### D3 · Cash cost per tonne (EGP/t) — ONE ESCALATOR PER DRIVER CLASS [L-009, L-110]

    cpt(h) = cpt(origin) × Π[ w_raw×(1+fx_dep_t) + w_dom_cost×(1+cpi_t) ]
    w_raw      = raw materials ÷ (cash cost lines), note 5 of the audited filing
    w_dom_cost = 1 − w_raw   (transportation and overheads)

Raw materials are dominated by imported coal and petcoke, which are globally
traded and priced through the exchange rate; transportation and overheads are
domestic. **A single blended index across physically distinct cost lines is
prohibited** — that shortcut manufactured an entire forecast margin decline in
this very company's published study and is the case L-009 and L-110 were adopted
from.

`w_raw` is fixed at **0.79**, the FY2024/FY2025 note-5 average, applied at every
origin. It is a stated parameter, not a fitted one; the sensitivity to it is
reported at ±0.10 and is not selected on.

**Declared gap** [R-SIGCM-02, B-9]: fuel is not separately disclosed inside raw
materials, so this driver is `derived`, not `unit`. It is not described as
unit-level anywhere in the delivered study.

### D4 · Non-cement revenue (EGP) — the segment the releases do not cover

    other(h) = other(origin) × (1 + cpi_t)^h

Ready-mix and alternative fuels; domestic, so domestic inflation [B-1].

### D5 · General and administrative expenses

    ga(h) = ga_ratio(origin) × group_sales(h),  ga_ratio = ga ÷ sales at origin

### D6 · Depreciation and amortisation — from the disclosed base, NOT a projected one

    dna(h) = dna(origin), held flat in nominal terms

**[L-028] binds here and is the reason this rule is deliberately dull.**
Depreciation projected as a rate on a fixed-asset balance that the model has also
projected stacks two forecasts on each other and drifted 1.8× high on the one
name previously tested. ARCC's plant is built and its capex has been at
maintenance level; the origin's own disclosed charge is the better anchor. The
alternative (escalating with capex) is reported as a sensitivity, not adopted.

### D7 · Finance costs — from the borrowings that actually bear interest [L-002]

    rate(origin) = fin(origin) ÷ mean(debt(origin), debt(origin−1))
    debt(h)      = max(0, debt(origin) − h × amort),  amort = mean annual
                   reduction in debt over the origin's trailing 3 years, floored at 0
    fin(h)       = debt(h) × rate(origin)

The denominator is interest-bearing borrowings — note 25's credit facilities plus
bank loans — and **nothing else**. Trade payables, creditors, tax liabilities and
dividends payable bear no interest; dividing by them understates the rate by a
multiple and manufactures a bias that looks exactly like evidence. That is the
error L-002 was adopted from, and it is not repeated here.

### D8 · Foreign exchange differences

    fx(h) = 0 at every origin and horizon.

**Stated as a parameter, not an omission.** A currency result is not forecastable
from a company's own history, and pretending otherwise would import the analyst's
view of the pound into a test of the method. The whole of the resulting error is
attributed to macro in §4's split, by construction.

### D9 · Income tax

    tax(h) = −0.225 × max(0, pbt(h))

Egypt's statutory corporate rate, the regime in force at every origin in the
window. No deferred-tax modelling: the deferred component is disclosed but is
not projectable by a mechanical rule, and its error is reported inside net profit
rather than being hidden in a fitted effective rate.

### D10 · Net profit after tax — an OUTPUT, assembled, never forecast directly

    sales = vol×rpt + other ;  cogs = vol×cpt + dna
    pbt   = sales − cogs − ga + fx − fin ;  npat = pbt + tax

**Margins are outputs of this construction and are never inputs** [L-005].

---

## 2 · The two naive benchmarks

- **FREEZE** — every line flat at the origin's last actual, at every horizon.
- **TREND** — every line grown at its own trailing 3-year CAGR from the origin.

Both are computed at every origin and horizon for every scored driver.
**A METHOD THAT CANNOT BEAT "NO CHANGE" HAS NOT EARNED THE PRECISION IT
DISPLAYS.** If the build loses to freeze, this run says so in those words and
does not reach for a correction to rescue it.

---

## 3 · The score

Log error per driver per horizon:

    e = ln(projected ÷ actual)

reported as bias (mean e), MAE (mean |e|), share of origins over- and
under-forecast, and sign by era (E1 2014–16, E2 2017–21, E3 2022–25 per B-5).

**Net profit changes sign in this history** — FY2020 is a loss of EGP 122.8mn —
so the log is undefined for some cells. Fixed here, before the results are seen:
a cell where either the projection or the actual is non-positive is a **SIGN
CASE**. Sign cases are counted, listed and reported separately with their signed
levels; they are **never silently dropped**, because dropping the loss year would
delete the single hardest thing this method had to forecast and would flatter
every statistic that survived.

Confidence intervals: **moving-block bootstrap over origins**, block lengths
{2, 3, 4}, 2,000 resamples each. Blocks are over origins because horizons within
an origin are not independent. A finding is called robust only if its sign holds
across all three block lengths — the house bar, unchanged.

---

## 4 · Macro conditioning and the macro/company split

Exogenous: Egyptian CPI inflation, EGP/USD, population, and the national cement
market. Endogenous: everything the company chooses or executes.

Every origin is re-run twice:

- **KNOWABLE** — the macro path as it could have been believed at the origin:
  the last realised CPI and FX change, carried flat. This is the production run.
- **FORESIGHT** — the realised macro path substituted, drivers otherwise identical.

The macro share of a driver's error is the part that disappears under foresight;
the remainder is the company share.

**THE SPLIT CARRIES ITS OWN CHECK.** D1 (volume) has no inflation and no FX term
in its rule. **It must therefore return a macro share of exactly zero by
construction.** If it does not, the split is wired wrong and the whole
decomposition is void — this is a negative control on the diagnostic, not a
result, and it is asserted in code.

---

## 5 · The two samples and their roles

- **Rolling sample** — all seven origins, overlapping. Estimates candidate
  corrections. Expanding window only: a correction at origin *o* may use errors
  resolved strictly before *o*.
- **Non-overlapping sample** — origins 2018, 2021 and 2024, which share no
  forecast year. Confirms or refuses. A correction that lives only in the
  overlapping sample has not been confirmed.

---

## 6 · Corrections — the two-clause promotion test, fixed here

A correction is applied at **half strength**, to one driver, only where:

1. the bias holds its **same sign in every era** it is observed in [L-029, L-030]; and
2. it survives the block bootstrap at all three block lengths; and
3. **it is consistent with how that driver class is built across the market's
   book** [L-003].

**Clause 3 is not a formality and it has already done its job once.** On PHDC a
finance-cost correction passed its own test convincingly, failed clause 3, and
that failure is what exposed a wrong denominator — the "bias" was arithmetic, not
evidence. A correction that fails clause 3 is recorded as a **WATCH FLAG**:
graded live, revisited at every refit, acted on by nobody.

Corrections reset after a structural break (a driver error beyond its own two
sigma). Aggregates are rebuilt from adjusted drivers and tested adjusted-against-
raw by origin.

**AND THE PRIOR QUESTION IS ASKED FIRST** [L-002]: where a bias is large and
robust, the first hypothesis is that the model is mis-specified, not that reality
needs a multiplier. A correction factor is honest when the model is right and
reality is awkward; when the model is wrong, a correction hides it.

---

## 7 · What this run may and may not conclude

**Two purposes, not three:** per-driver bias detection, and calibrated ranges for
years 3–5 built from this record's own error distribution. **A better point
estimate is a by-product and never the aim.** Tuning toward one is the
CRPS-selection mistake in a new costume, and the promotion rule forbids it.

Every lesson this run produces is **PROVISIONAL** [R-LESSON-01]. ARCC is the
second name ever put through this method. A finding measured on two companies has
not survived the out-of-sample test the forecasts themselves must survive, and
this project does not exempt itself from its own bar.
