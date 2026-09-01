# EMFD — fundamental walk-forward training: PRE-REGISTRATION

**Instrument:** Emaar Misr for Development Company (S.A.E.) · EGX:EMFD · market EG · exchange EGX
**Class:** off-plan residential developer — **completed-contract basis to FY2020** (see §0)
**Written:** 1 September 2026 — BEFORE any projection was run and before any error was computed.
**Status:** training record only. Nothing here is published; nothing here changes a
delivered number until the correction it proposes has passed §8's test.

This file is fixed at the moment it is committed. Every parameter is **stated**, never
fitted; where a rule needs a number, the number is a stated function of data available at
the origin. Sensitivities are reported, never selected. If a later commit changes anything
here, the change is itself dated and the affected results are re-run and re-reported — the
pre-registration is not edited to match an outcome.

**It is written now, while the run is blocked, deliberately.** The documents §1 requires are
not yet in hand (`SCOPE_DECISION_01-09-2026.md`). Writing the rules before the data exists is
the strongest possible version of the discipline this section is for: there is no result to
tune towards, because there is no result.

---

## 0. The one thing to establish before anything else — the revenue-recognition basis

L-102 says check the revenue-recognition basis before anything else. Checked, from the
company's own earnings releases, which state it in terms:

> "revenues recognized according to the **Completed Contract (CC) method**"
> — FY2016 results release, and again in the FY2017 release

So through FY2020 this company recognised revenue **on handover**, not as construction
progressed. Three consequences, all of them structural:

1. **The house class label does not fit the pre-2021 window.** The registered class is
   "real-estate developer, off-plan, percentage-of-completion". EMFD to FY2020 is off-plan
   **completed-contract**. The class lessons are read, as required, but the ones that turn
   on percentage-of-completion are read as **not applying to this window** — which is the
   register working, not a licence to ignore it.
2. **L-001's own falsifier is met here.** That lesson — revenue and cost must sit on the
   same clock — records its overturning condition as *"an issuer that genuinely recognises
   revenue only on handover, where the two clocks already coincide."* Under completed
   contract, revenue and cost of revenue are both released at delivery, so the clocks
   coincide by construction. The driver design below still puts them on one clock
   explicitly, because a design that relies on an accounting basis staying put is a design
   that breaks silently when it moves — and it did move, at 1 January 2021.
3. **It moves at EAS 48.** From FY2021 the company adopted EAS 48 (the Egyptian IFRS 15) and
   restated. Whether that shifts it to over-time recognition, and for which projects, is a
   question the FY2021 statements answer and this session cannot. The driver definitions
   below are therefore written to be evaluated **inside a recognition-basis window**, and
   the first task when the blocked documents arrive is to date that boundary and split the
   panel on it. See `BASIS_BREAKS_01-09-2026.md` B1.

## 1. Origins

Annual origins at the fiscal year-end (31 December). An origin is admissible once the panel
holds **five prior complete fiscal years** for the driver being projected.

* Panel span **required by §1**: FY2012 – FY2025.
* First admissible origin: **FY2016**. Last scored origin: **FY2024** (h=1 resolves at
  FY2025).
* Origin FY2025 is *struck but unresolved*: it produces the forward projection the update
  consumes and contributes no error.

At each origin the model sees **only** what had been published by that date, **as originally
reported**. Where a later filing restates a figure the origin used, the origin keeps the
as-first-reported number and the restatement is recorded in the basis-break register beside
it. Two such restatements are already measured there and neither is adopted.

## 2. Horizons

**h = 1…5 years.** A pair (origin *o*, horizon *h*) is scored iff *o + h ≤ 2025*.

| origin | horizons that resolve | cells |
|---|---|---|
| FY2016 | 1, 2, 3, 4, 5 | 5 |
| FY2017 | 1, 2, 3, 4, 5 | 5 |
| FY2018 | 1, 2, 3, 4, 5 | 5 |
| FY2019 | 1, 2, 3, 4, 5 | 5 |
| FY2020 | 1, 2, 3, 4, 5 | 5 |
| FY2021 | 1, 2, 3, 4 | 4 |
| FY2022 | 1, 2, 3 | 3 |
| FY2023 | 1, 2 | 2 |
| FY2024 | 1 | 1 |

**35 scoreable (origin, horizon) cells per driver** on the required span. On the span
currently obtainable there are 10, which is why the run is blocked rather than
narrowed.

## 3. Drivers, by class

Built bottom-up. **Margins are outputs, never inputs** (L-005).

| # | driver | class | unit |
|---|---|---|---|
| D1 | units delivered | volume | units/yr |
| D2 | revenue per unit delivered | price | EGP/unit |
| D3 | cost per unit delivered | cost per unit | EGP/unit |
| D4 | net contracted sales value | volume × price | EGP |
| D5 | backlog (value and units) | conversion | EGP, units |
| D6a | selling and marketing expense | overhead, sales-linked | EGP |
| D6b | general and administrative expense | overhead, fixed | EGP |
| D7 | finance income | financing | EGP |
| D8 | finance cost | financing | EGP |
| D9 | depreciation and amortisation | non-cash | EGP |
| D10 | income tax | regulated | EGP |
| D11 | construction and development spend | capex | EGP |
| D12 | working capital (receivables, advances, inventory) | balance sheet | days |

Aggregates are **rebuilt from the drivers**, never projected directly: revenue, cost of
revenue, gross profit, EBITDA, profit before tax, profit for the year, and the balance-sheet
and cash-flow lines they drive.

**Why the driver tree is delivery-anchored rather than completion-anchored.** Under
completed contract, revenue *is* delivery: `revenue = D1 × D2` and `COGS = D1 × D3` with
both on the same year's delivery count. That satisfies L-001 by construction and satisfies
L-010 — *never divide one year's value by another year's volume* — because D2 and D3 are
formed from the same year's revenue and the same year's delivered units, never from a sales
value disclosed to one year and a unit count disclosed to another.

## 4. Mechanical rule for each driver, with parameters

Evaluated on information available at origin *o* only. `TTM3(x, o)` is the trailing
three-fiscal-year arithmetic mean of *x* ending at *o*; `TTM5` likewise over five.
**There are no judgement drivers at a historical origin — the method is tested, not the
analyst.**

* **D1 units delivered.** §3 requires an exogenous market anchor, so the primary rule is
  `units_{o+h} = Households_{o+h} × intensity_o`, `intensity_o = units_o / Households_o`
  held flat, with Egyptian urban household formation projected at the rate published
  **before** the origin (vintage recorded per origin).
  **This rule is also a pre-registered test of a provisional lesson.** L-101 states that a
  developer's volume is set by its launch and construction calendar and that no demographic
  anchor can see it. That is a falsifiable prediction: if D1's demographic anchor fails to
  beat *freeze* at every horizon, L-101 gains a second name; if it beats freeze, L-101 is
  challenged on its own terms. The rule is therefore **not** replaced by a launch-calendar
  rule — replacing it would be reading a provisional lesson as authority, which
  [R-LESSON-01] forbids. It is run, and its failure or success is a result.
  **Constraint (L-104):** cumulative deliveries may never exceed cumulative net contracted
  sales. `units_{o+h} = min(anchor, backlog units available)`. A projection that delivers
  what was never sold is arithmetic, not a forecast; the constraint binds, and every origin
  where it binds is reported.
* **D2 revenue per unit delivered.** `D2_{o+h} = D2_o × Π_{k=1..h} (1 + π_k)` with
  `D2_o = TTM3(revenue / units delivered, o)` and π the **expected Egyptian headline CPI
  path**. Two macro settings, both pre-registered, and the pair is what defines the
  macro/company split in §6:
  * **as-known:** π_k = TTM3(CPI, o) held flat — the honest information set at the origin.
  * **perfect-foresight:** π_k = realised CPI. Not a forecast; it exists only to price how
    much of the miss was macro.
* **D3 cost per unit delivered.** `D3_o = TTM3(cost of revenue / units delivered, o)`,
  escalated on a **construction-cost** path, not on headline CPI — one escalator per driver
  class (L-009). Where a construction-cost series cannot be sourced for a vintage, headline
  CPI is used and **the substitution is flagged in that cell**, never absorbed silently.
* **D4 net contracted sales.** `D4 = units contracted × price per unit contracted`, each on
  its own rule (volume on the D1 anchor, price on the D2 escalator).
  **Reported sensitivity, not a selected one (L-114):** that lesson records that a
  developer's new-sales value is under-forecast whenever price and volume are projected
  separately. The joint alternative — `D4` projected directly on its own trailing rule — is
  therefore computed at every origin **as well**, and both are reported. Neither is chosen
  on the strength of its score; choosing would be the CRPS-selection mistake in a new
  costume.
* **D5 backlog.** Rolled, in value and in units:
  `backlog_t = backlog_{t-1} + net sales_t − revenue recognised_t`, units likewise.
  **L-103:** the two contract positions move together. The contract-asset side (instalment
  and notes receivable) and the contract-liability side (advances from customers) are
  projected from the **same** backlog roll, never independently, and their sum is asserted
  against the disclosed balance-sheet lines at every historical year before any origin is
  built.
* **D6a selling and marketing.** `S&M_t = s_o × net sales_t`, `s_o = TTM3(S&M / net sales, o)`.
  Sales-linked, because that is what it is.
* **D6b general and administrative.** `G&A_t = a_o × Π (1 + π_k)`, `a_o = TTM3(G&A, o)`.
  Fixed and escalated, not revenue-linked. The two overhead lines are **not** pooled: they
  have different drivers and pooling them would hide which one moved.
* **D7 finance income.** This company's finance income is of the same order as its operating
  profit, so it is a first-class driver and not a residual.
  `finance income_t = r_o × (opening cash and deposits + opening instalment/notes
  receivable)`, `r_o = TTM3(finance income / that same opening base, o)`, and the rate is
  additionally run on the **exogenous** setting `r = CBE overnight deposit rate known at the
  origin`, giving the macro/company split for this line.
  **The base is the assets that actually earn it** — cash, time deposits and interest-bearing
  instalment receivables — never total assets and never total current assets. This is
  [R-FCAL-01]'s trap (i) applied to the asset side: a rate formed on a base that does not
  earn the income is arithmetic dressed as evidence, and it is what L-002 was learned from.
* **D8 finance cost.** `finance cost_t = kd_o × opening **interest-bearing borrowings**`,
  where interest-bearing borrowings means the facilities the debt note itself says bear
  interest — never total liabilities, never advances from customers, never retentions or
  payables.
  **This company appears to be substantially unlevered**: its FY2018 finance cost is under
  EGP 1 million against a multi-billion balance sheet. Where the debt note discloses no
  interest-bearing borrowings at an origin, `kd_o` is **undefined and is not computed**: the
  line carries `TTM3(finance cost, o)` and the cell is marked *rate not identified*. A ratio
  whose denominator is near zero produces a spectacular and meaningless rate, and the
  temptation at that moment is to widen the denominator until the answer looks sensible —
  which is exactly the mis-specification L-002 records. The rule refuses in advance.
* **D9 D&A.** PP&E roll-forward: `PPE_t = PPE_{t-1} + capex_t − D&A_t`,
  `D&A_t = d_o × PPE_{t-1}`, `d_o = TTM3(D&A / opening PP&E, o)`.
* **D10 income tax.** By formula under the regime **known at the origin**: the Egyptian
  statutory corporate rate as legislated at that date, applied to positive profit before
  tax, zero otherwise. A rate change legislated after the origin is a **macro/regulatory**
  miss, not a company miss, and is reported in that column.
* **D11 construction and development spend.** The disclosed programme or guidance at the
  origin where the company gave one, else `TTM3(construction spend, o)` escalated on the D3
  cost path. It is an **input** that drives inventory, deliveries and D&A — never an output.
* **D12 working capital.** DSO, DIO and DPO computed at the origin and held flat, applied to
  the projected revenue and cost lines to project receivables, development inventory,
  advances from customers and payables, and from there the balance sheet and the cash-flow
  statement. **No unexplained plugs where the driver is disclosed.**
  **L-105** records that for a developer the collection cycle and a fast growth path cannot
  both hold. That is not corrected for here; it is **tested**: where a projection implies
  both, the implied cash balance is reported and the contradiction is shown rather than
  reconciled away.

## 5. Naive benchmarks

Computed for every driver and every aggregate at every (origin, horizon):

* **freeze** — every line flat at the last actual: `F_{o+h} = A_o`.
* **trend** — trailing three-year CAGR from the origin:
  `T_{o+h} = A_o × (A_o / A_{o-3})^(h/3)`.

Skill is the reduction in mean absolute log error against each benchmark, per horizon. **A
method that cannot beat "no change" has not earned the precision it displays**, and where
that happens the record says so in those words.

## 6. Score

* **Primary:** log error `e = ln(projected / actual)`, per driver, per horizon; reported as
  **bias** (mean e) and **MAE** (mean |e|).
* **Sign cases:** where either side is ≤ 0 the log is undefined. Those cells are **not**
  dropped and **not** patched — they are counted in a separate sign-error tally scored as
  `(P − A)/|A|`, reported separately, never pooled into the log statistics.
* **Uncertainty:** moving-block bootstrap over **origins**, block lengths **{2, 3, 4}**,
  2000 resamples — the same robustness bar this repository uses elsewhere. A bias is called
  robust only if its sign holds across all three block lengths.
* **Shares:** fraction of origins over- and under-forecast, and the sign **by era**.
* **Macro vs company split:** every origin is projected twice, once on the as-known macro
  path and once on perfect foresight. The **perfect-foresight error is the company error**;
  the difference is the **macro/regulatory error**. Both are reported for every driver.
  **The split carries its own check:** D1 (units delivered) has no inflation term, so its
  macro share must come back **zero by construction**. A non-zero macro share on a volume
  driver is a wiring fault, not a finding, and the run stops there.
* **Eras — two independent partitions, pre-registered, dated, not chosen by outcome.** They
  do not coincide, and a driver must sit inside **both** windows to be scored:
  * *FX regime:* E1 pre-float FY2012–FY2016 · E2 post-float FY2017–FY2021 ·
    E3 devaluation cycle FY2022–FY2025.
  * *Recognition basis:* R1 completed contract, to FY2020 · R2 EAS 48, FY2021 onward — the
    exact boundary to be confirmed from the FY2021 statements when they arrive.

## 7. Roles of the two samples

* The **rolling record** — all admissible cells, horizons overlapping — **estimates** the
  corrections.
* The **non-overlapping origins** — spaced five apart so no two share a forecast year;
  on the required span that is FY2016, FY2021 — **confirm** them. This set is thin. Its thinness
  is stated here in advance as a limit of a single-name study and is not worked around.

## 8. Corrections — the rule, fixed before any error exists

* **Expanding window only:** a correction applied at origin *o* uses errors resolved
  **before** *o*. No correction is ever informed by an outcome it is then scored on.
* **Half strength by default:** applied correction = 0.5 × estimated bias.
* Applied **only** where the bias holds its sign across eras (§6). A bias that changes sign
  between eras is reported as **instability** and is not corrected — the average of two
  opposite regimes was true in neither.
* **Reset** after a structural break, defined as a driver error beyond its own two-sigma.
* A correction enters the live update's drivers only if it (a) passed the adjusted-versus-raw
  test here **and** (b) is consistent with how that driver class is built across the rest of
  this book. Otherwise it is a **watch flag** — recorded, graded live, revisited at the next
  update, acted on by nobody. The second clause is not a formality: it is what caught a
  finance-cost correction on another name that passed its own test and was hiding a wrong
  denominator.
* **Guidance is scored and never consumed.** Management's forward targets are logged against
  outcome with their own bias, and are never an input to a driver at a historical origin.

## 9. What would make this record misleading — stated in advance

So that none of it can be discovered later and quietly dropped:

* **One name, few origins.** 35 cells across 9 origins is a small sample for a
  five-horizon claim. Block-bootstrap intervals will be wide, and are reported wide.
* **Overlapping horizons.** The rolling record's cells are not independent. That is why the
  non-overlapping set exists and why it is reported even though it is thin.
* **A currency that moves everything at once.** Egypt's 2016 float and the 2022–24
  devaluation steps move every nominal driver together. If the corrections turn out to
  restate "the currency fell", that is a finding about the macro path and not about the
  driver rules, and it is reported that way.
* **A recognition basis that changes inside the span.** The EAS 48 boundary splits the panel
  into two definitions of revenue. Pooling across it would manufacture a step; the era
  partition exists to prevent that, and any driver that cannot be scored inside one window
  is reported unscored rather than scored wrongly.
* **Unit KPIs are thinner than the statements, and this is already measured rather than
  feared.** On the window obtained so far, delivered-unit counts exist for FY2015, FY2016, FY2017 and for
  FY2018, FY2019, FY2020 they exist in no document on the company's register at all. Any year without a
  sourced unit count drops out of D1, D2 and D3 and is reported as dropped; it is never
  interpolated. A shorter window is a smaller claim, and a filled cell is a false one.
