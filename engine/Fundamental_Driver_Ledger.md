# Fundamental Driver Ledger

Append-only. One entry per driver decision that a delivered study or a training
run actually made, with what it was set to, what it was set from, and what would
overturn it. A driver decision recorded here is available to later studies as a
same-class prior; it is never a default.

**Status of this file, stated plainly.** `CLAUDE.md` has referenced this ledger
since 07-Aug-2026 while the file did not exist. It is created here and started
from the first entry that had real, tested driver decisions to record — the PHDC
walk-forward training run of 30-Aug-2026. **The entries for the studies
delivered before that date have NOT been compiled**, and nothing in this file
should be read as covering them. Compiling them means reading each delivered
study's own committed compute and QC documents and recording what those studies
actually decided; that is a real research task and is outstanding, not done.

---

## PHDC · Palm Hills Developments · EGX · 30-Aug-2026
**Class:** real-estate developer, off-plan, percentage-of-completion
**Context:** fundamental walk-forward training run, `engine/phdc_walkforward/`
**Nothing in this entry has been published.**

### Drivers set, and from what

| # | driver | rule as set | set from | tested? |
|---|---|---|---|---|
| D1 | units sold | urban population × origin-year intensity, held flat | CAPMAS/World Bank urban population, dated at origin | yes — bias **−0.215**, robust |
| D2 | ASP per unit | origin ASP escalated on trailing 3y Egyptian CPI | new sales ÷ units sold, both from the same disclosed year | yes — bias +0.041, not robust |
| D4 | revenue recognition rate δ | trailing 3y mean of revenue ÷ (opening backlog + new sales), held flat | releases' disclosed backlog, rolled between anchors | scored only inside the post-2016 basis window |
| D5 | units delivered | trailing 3y delivery rate scaled by the units-sold path | releases' handover disclosures | yes — bias +0.294, not robust |
| D6 | cost per unit delivered | trailing 3y COGS ÷ deliveries, escalated on the cost path | filed statements ÷ release handovers | yes — **mis-specified, see below** |
| D7 | SG&A | fixed + variable, OLS on the trailing five years, fixed leg escalated | filed statements | yes — bias −0.079, not robust |
| D8 | D&A | rate × opening PP&E, PP&E rolled with construction spend | filed statements | yes — bias +0.586, robust |
| D9 | interest | trailing 3y finance cost ÷ opening liabilities base | filed statements | yes — bias −1.074, **base is a stated deviation** |
| D10 | tax | statutory rate in force at the origin (22.5% from FY2015) | Egyptian corporate rate | not separately scored |

### Decisions worth carrying to the next same-class study

1. **Revenue and cost must sit on the same recognition clock.** Recognising
   revenue on percentage of completion while recognising cost on handover is a
   specification error, not a calibration one. On PHDC it produced a gross-profit
   bias of **+0.540 log, robust, over-forecast in 86% of cells**, which
   compounded through operating leverage into a **+1.12** net-profit bias — worse
   than freezing last year's number at four of five horizons. Any developer study
   built on a POC issuer must check this first.
   *What would overturn it:* an issuer that genuinely recognises on handover
   only, where the two clocks coincide.

2. **Interest comes from the named debt schedule, not from a liabilities
   ratio.** This is already the EG book's convention (ARCC carries CIB, NBE and
   EBRD tranches each at its own cost of debt). The ratio implementation used
   here carried a **−1.074 robust bias**, and a bias correction fitted to it
   would have been calibrating the wrong base. Recorded as a defect, not a prior.
   *What would overturn it:* an issuer whose filings do not disclose facilities
   individually, where the ratio is the finest sourced level available.

3. **An exogenous population anchor under-forecasts a launch-driven
   developer.** Units sold came in **−0.215 log, robust, under-forecast in 73% of
   cells**, and the miss widens sharply in the devaluation era (−0.490). Volume
   for this class is set by the launch calendar, which a demographic anchor
   cannot see. The anchor is still the right *starting* point — it keeps the
   driver exogenous — but a study using it should say that it under-shoots and
   should not treat the shortfall as conservatism.
   *What would overturn it:* a developer with a stable, disclosed launch
   pipeline, where volume can be built from the pipeline instead.

4. **Never divide one year's value by another year's volume.** PHDC's
   disclosure stops at different years for new sales (FY2024) and units sold
   (FY2023), and taking each one's latest separately produces a "price per unit"
   of 28.5 against a true FY2023 ASP of 11.2. An ASP anchor must come from a
   single year that discloses both halves.
   *What would overturn it:* nothing — this is an arithmetic rule.

5. **Management's forward handover guidance leans the same way the model
   does.** Scored on the only two forward targets this archive lets us grade
   before the outcome, guidance over-forecast handovers by **+0.220 log** (FY2019
   1,350 against 964; FY2021 1,450 against 1,308), while every target quoted
   *retrospectively* had been beaten. A driver that consumes company guidance
   inherits that lean.
   *What would overturn it:* a longer guidance record, or an issuer whose
   forward targets are graded in its own disclosures.

### Corrections tested and NOT promoted

The finance-cost correction (−0.445 at half strength) cut that driver's MAE from
0.848 to 0.403 and **passed** the adjusted-vs-raw test. It was **not promoted**,
because it fails the second clause — consistency with the same driver class
across the market's book — for the reason in decision 2 above. Recorded as watch
flags instead: units sold (−0.215), gross profit (+0.540), D&A (+0.586), all
robust, all to be re-graded at the next update.

### Macro conditioning

About **21.5%** of the revenue error and **3.9%** of the net-profit error is
macro, measured by re-running every origin on a perfect-foresight inflation path.
Units and deliveries carry zero macro share by construction, which is the check
that the split measures what it claims. Egypt's four devaluations across
FY2016–FY2024 do **not** explain this record.

---

## TMGH — Talaat Moustafa Group Holding (EGX) · 1 September 2026

**Class:** real-estate developer, off-plan — **point-in-time on handover**, not
percentage-of-completion. That distinction is the entry's most important line: it
is a different class from PHDC's, and it is registered as one, because [L-102]
makes the recognition basis the class-defining question for developers and filing
a point-in-time issuer under a percentage-of-completion class would be exactly the
superstition the lessons register warns about.

**Evidence base:** ten annual origins (FY2015–FY2024), horizons 1–5, both macro
settings, scored against both naive benchmarks. Panel span FY2009 and
FY2011–FY2025 from the company's own archive; FY2007, FY2008 and FY2010 excluded
because their releases survive only as scans whose tables do not resolve.

### Drivers set without a company disclosure, and what stands behind each

| Driver | What was used | Why, and what would replace it |
|---|---|---|
| Order-book conversion period | 14 years (slower) and 10 years (faster), published side by side | The company publishes no delivery schedule. Its own conversion rate fell from ~15% before 2023 to 5.4% in FY2025 as the book quadrupled — construction capacity binds, not the order book. **A disclosed delivery schedule by project replaces this.** |
| Replenishment sales | EGP 300bn a year, fading 15% a year toward the delivery rate | TMG sold roughly **ten times** what it delivered in FY2025. That is not a steady state and is not extrapolated: modelling sales and deliveries as independent compounding series drove the order book to EGP 4.8 **trillion** inside ten years. **Sustained sales at the current rate alongside deliveries rising to meet them would replace it.** |
| Work-in-progress cover | 4.0 years of development cost, moved over 4 years | The company's own position at 30 June 2026. A fixed multiple of cost was tried and rejected: it made the company build ever faster for ever and drove cash to minus EGP 4 trillion — [L-105] made quantitative. |
| Marginal cost of debt | Sovereign 23.00% + 250bp = 25.50% | **TMG discloses no rate on any of its own facilities**, in any statement or release held. Labelled rather than presented as the company's own cost. **Any disclosed facility pricing replaces it.** |
| Recurring-leg growth | 20% hospitality, 22% other recurring | Stated, sensitised. No segment capex or occupancy disclosure exists to build them finer. |
| Minority deduction | Computed BOTH at book and proportionally, on every case | Non-controlling interests are **45.2%** of consolidated equity and the company does not disclose its economic share project by project. |

### What the record decided

1. **The backlog-conversion rule works and the volume rule does not.** Development
   revenue: bias −0.055 log, MAE 0.276, n=35 — the strongest positive result in the
   run, and the reason the valuation is built on the order book rather than on a
   revenue growth rate. New contracted sales: bias **−0.877**, robust across every
   bootstrap block, in both eras.
2. **The volume miss is a launch calendar, and its SIZE is not transferable.**
   PHDC's equivalent miss was −19%; TMGH's is −58%. Registered as [L-118]: a
   multiplier fitted on one developer cannot be carried to another.
3. **The method is a long-horizon instrument.** It beats "no change" almost
   everywhere from two years out and beats a trailing three-year growth rate on net
   profit at three to five years, where that benchmark compounds into nonsense
   (MAE 2.106 at h=5). At **one year** it beats **neither** benchmark on development
   revenue or net profit, and the study says so.
4. **Almost none of the error is the currency.** Perfect foresight of Egyptian
   inflation removes 4 points of a 9-point revenue miss and 5 of a 68-point
   net-profit miss, across three devaluations. Registered as [L-046].

### Corrections tested and NOT promoted

The **finance-cost** correction (−0.612 at half strength) cut that driver's MAE
from 0.812 to 0.445 and **passed** its own test convincingly — robust across every
block, sign holding in both eras, zero origins over-forecast. It was **not
promoted**. TMG's reported finance charge of EGP 3,936.5mn against opening
interest-bearing debt of EGP 8,928mn implies **44%**, against an Egyptian policy
rate that peaked near 27.25%; the excess is the unwinding of the significant
financing component recognised on customer contracts, and the statements do not
split it. **This is the same species as the correction blocked on PHDC, reached
from the opposite direction: there the DENOMINATOR was too broad, here the
NUMERATOR is.** Recorded as a watch flag and as [L-044].

Adopted at half strength, expanding window: new sales, backlog, development
properties and D&A. The two-sigma structural-break reset fires at the FY2024 and
FY2025 launch origins, so the new-sales correction carried into the forward
projection is **0.000** — the pre-registered reset doing exactly its job.

### Macro conditioning

Macro share of the error: revenue **4.2 points of 9.0**, net profit **4.3 of
68.0**, new sales **7.5 of 87.7**. Finance cost and development properties both
return a macro share of **exactly zero by construction**, which is the check that
the split measures what it claims — their rules carry no inflation term.

**Fair-value movement, and what the base leg in that register is not.** The
run is recorded in the fair-value half of the calibration register (edition 1,
scope FULL, origins FY2015–FY2024). Its baseline is a genuine one rather than a
declared exception: this run was made under the standing instruction that
nothing reaches the live site, `assets/data.js` was never written, and TMGH's
`fair{}` on this branch is byte-identical to the one on the default branch — so
the frozen number is the pre-run number and not a reading of our own output. The
movement is **−73.3% on the base leg**, and essentially all of it is the cost of
capital: the superseded edition discounted at a hardcoded 18%, below Egypt's own
23.00% sovereign yield, while this one builds 35.79%/32.37% from the sovereign's
own default spread on both published bases. That is the same defect the previous
developer run carried, found the same way, and it is the whole difference between
the editions.

**The base leg is not a delivered number.** This study publishes four cases and
no point estimate — two cost-of-capital bases against two readings of the crux,
held apart under the dual-framing rule and never averaged. The register stores
three legs, so bear (22.30) and full (59.67) are the study's own published
extremes and the base leg (39.33) is the median of the four cases, computed in
`engine/tmgh_study/fv_record.py` from the committed numbers file solely so a
movement can be computed against the old triple. It appears on no delivered
surface and it is not this study's answer.

---

## EMFD · Emaar Misr for Development · EGX · 01-Sep-2026
**Class:** off-plan residential developer — **completed-contract basis to FY2020**,
EAS 48 from FY2021 (see below; this is NOT the registered
"off-plan, percentage-of-completion" class for the pre-2021 window)
**Context:** fundamental walk-forward training run, **BLOCKED at [R-FCAL-01] §1** —
`engine/emfd_walkforward_pending/`
**Nothing in this entry has been published, and no driver here has been set on a delivered
number.** The existing EMFD study and its published cone are untouched.

### Why there are no driver decisions to record yet

The run did not start. §1 requires the most recent three fiscal years and every disclosed
current-year quarter to come from the company's own audited statements or its own IR
documents, and FY2023–FY2025 cannot be obtained from any permitted route. The company's
investor-relations register publishes financial statements from FY2013 to H1-2021 and then
stops; the exchange holds the later filings and serves an anti-bot interstitial to automated
requests; the company's own embedded IR backend serves on a port this session's egress
policy does not permit. Every route and outcome is logged in
`engine/emfd_walkforward_pending/SOURCE_REGISTER_01-09-2026.md`.

Aggregator figures for the missing years exist and were not used. That is the rule working.

### What IS recorded, because it was measured rather than assumed

1. **The revenue-recognition basis is completed contract to FY2020, not
   percentage-of-completion.** The company's own results releases say so in terms
   ("revenues recognized according to the Completed Contract (CC) method", FY2016 and FY2017
   releases). Revenue and cost of revenue are both released at handover, so the two clocks
   coincide by construction and **L-001's own stated falsifier is met for this window**.
   A same-class prior taken from a percentage-of-completion developer does not transfer to
   EMFD's pre-2021 years.
   *What would overturn it:* the FY2021+ statements showing the EAS 48 transition moved this
   company to over-time recognition, which would make the post-2021 window a different class
   again — and is one of the first things to check when those documents arrive.

2. **EAS 47/48/49 redefine revenue at 1 January 2021, and the size of the redefinition is
   measured, not assumed.** The six months to 30 June 2020 is the one period this company
   published on both bases. Restated onto EAS 48 its revenue rises **+2.72%**, its cost of
   revenue rises **+8.05%**, and its gross profit falls **−8.42%**. A revenue or
   cost-per-unit driver may not be scored across that boundary.
   *What would overturn it:* nothing about the measurement; it is two filings differenced.
   The open question is only whether the FY2021 annual accounts restate FY2020 as well.

3. **FY2019 was reclassified in the FY2020 accounts: a gross-up, invisible at the bottom
   line.** Revenue restated **+3.78%** and cost of revenue **+5.46%** against an equal and
   opposite fall in other income, with profit before tax and profit for the year identical
   on both bases (FY2020 note 36). A revenue driver scored across FY2019 would carry a 3.8%
   step that is presentation, not business, and no check that watches profit would see it.
   *What would overturn it:* nothing — it is the company's own two presentations differenced.

4. **This company is substantially unlevered, and that is a trap on the finance lines.**
   FY2018 finance cost is under EGP 1 million against a multi-billion balance sheet, while
   finance income is of the same order as operating profit. The pre-registration therefore
   fixes, in advance, that finance cost is built from **interest-bearing borrowings only** —
   and where the debt note discloses none, the borrowing rate is **undefined and not
   computed**, the line carrying a trailing mean and the cell marked *rate not identified*.
   Widening the denominator until the rate looks sensible is exactly the mis-specification
   L-002 records, and the rule refuses it before any number exists.
   *What would overturn it:* a debt note disclosing material interest-bearing facilities, at
   which point the ordinary rate × opening-borrowings rule applies.

5. **Finance income is a first-class driver for this name, not a residual.** It is built on
   the assets that actually earn it — cash, time deposits and interest-bearing instalment
   receivables — never on total assets, and it is additionally run on the exogenous CBE
   deposit rate so its macro share can be priced. The FY2017 release attributes that year's
   finance income to "the high interest rate environment", which is a macro attribution the
   company itself makes and the split can therefore be checked against.
   *What would overturn it:* a period where finance income is small relative to operating
   profit, making a simpler treatment adequate.

6. **The revenue line on this issuer is a presentation choice, and it has been revisited
   more than once.** FY2013 was restated in the FY2014 accounts — revenue **−4.77%**, gross
   profit **−12.67%**, offset in selling expenses and other income, with cost of revenue and
   profit before tax identical on both bases. That is the same species as the FY2019
   gross-up six years later. Two of the nine years in the panel carry a revenue
   reclassification invisible at the bottom line, so the panel keeps the **as-first-reported**
   figure at every origin and records the later presentation beside it.
   *What would overturn it:* nothing about the measurement. What it does not tell us is
   whether the practice continued through FY2021–FY2025, which the blocked filings answer.

7. **A source document can be incomplete, and the arithmetic is what says so.** The FY2015
   year-end PDF on the company's own register omits its profit-or-loss page entirely — the
   file runs balance sheet, changes in equity, cash flows, notes. FY2015 is therefore taken
   from the comparative column of the FY2016 filing and flagged as a comparative. A pipeline
   that had assumed "the filing exists, therefore the year is sourced" would have carried a
   hole.
   *What would overturn it:* a complete FY2015 filing from the company or the exchange.

8. **The operating KPIs this class needs stop three years before the statements do.**
   Delivered-unit counts and contracted-sales values are published in the results releases,
   and the company's register carries releases only for FY2015, FY2016 and FY2017. For
   FY2018–FY2020 no unit count exists in any document on the register: no release was
   published and the management annual reports for those years are Arabic scans of the
   board's governance report, carrying no operating data. Units delivered, revenue per unit
   and cost per unit — the three drivers that carry a developer — are unscoreable on those
   years, and a unit count is never interpolated to fill the gap.
   *What would overturn it:* the FY2018–FY2020 releases or an investor presentation carrying
   the counts, from the company or the exchange.

9. **The two pre-registered financing rules were checked against the disclosure, and one of
   them refuses — as written.** On opening earning assets (cash, time deposits and
   interest-bearing receivables) the implied D7 rate lands between **8.8% and 26.6%** across
   FY2017–FY2020, which is where an Egyptian deposit rate belongs; on total assets it would
   have landed near 3%, which is the trap the rule was written to avoid. D8's implied
   borrowing rate on this name's disclosed interest-bearing borrowings comes out at **238%
   in FY2019 and 69% in FY2020** — the company is effectively unlevered and the denominator
   is noise — so the rule's "rate not identified" branch fires, exactly as pre-registered.
   Nothing was widened to make the number look sensible.
   *What would overturn it:* the FY2021+ filings disclosing material interest-bearing
   borrowings, at which point the ordinary rate × opening-borrowings rule applies.

10. **A rate formed on an opening base is not the same driver as one formed on an average
    base when the base is doubling.** EMFD's earning-asset base roughly doubles across
    FY2016–FY2017, and the opening-base D7 rate ranges from under 9% to over 26% on that
    account alone. The pre-registration was **amended on 1 September 2026, dated, while no
    error had been computed**, to compute both conventions at every origin and report both
    without selecting either. Recorded here because the amendment is only legitimate at that
    moment: after an error existed it would have been tuning.
    *What would overturn it:* a company whose earning-asset base is stable enough that the
    two conventions coincide.

### Pre-registered predictions this run will test when it is unblocked

Recorded here so they cannot be quietly dropped: **L-101** (a developer's volume is set by
its launch calendar and no demographic anchor can see it) is run as the primary D1 rule
rather than replaced by one, so its failure or success against *freeze* is a result rather
than an assumption; and **L-114** (new-sales value is under-forecast when price and volume
are projected separately) is computed both ways at every origin, with both reported and
neither selected on its score.

---

## AMOC — Alexandria Mineral Oils Company S.A.E. · EGX · 1 September 2026

**Class registered for this name: "refiner, commodity pass-through on a thin spread".** It is a
NEW class, not petrochemical. AMOC buys fuel oil and wax distillate from the state oil company
and sells refined products drawn from the same barrel, in the same months, at prices set off the
same international quotes; its margin is a ~6.6% spread between two flows each above EGP 35bn.
A petrochemical producer's product prices can move independently of its feedstock for long
stretches. The two react to the same shock in opposite ways, and filing one's lessons under the
other would be the superstition the register warns about.

**Scope: LIGHT** — five sourceable fiscal years, FY2021–FY2025, nine scoreable cells. AMOC
publishes no accounts older than FY2022; the exchange, the regulator's portal and the web archive
are refused at this environment's egress proxy.

### Driver decisions, and why each was made

1. **Revenue is built per product line; cost is NOT.** Note 14-A discloses tonnage and value for
   every product in every year, so revenue is volume × realisation on a disclosed unit. Note 15-A
   discloses cost **by nature** for the company as a whole and never by product, and the FY2023
   auditor's emphasis of matter records that AMOC implemented a per-product costing system only
   **from 1 July 2023**. Every driver line is therefore filed at `derived`, not `unit`, with the
   gap stated. Any per-line margin in the study is a construction and now says so.
   *What would overturn it:* a filing that discloses cost per product.

2. **Revenue and feedstock escalate on the SAME index with the SAME exponent (β = 1.0).** Raw
   materials are 90.7% of cost of sales and are the same barrel the revenue is priced off.
   Escalating the two sides on different indices would manufacture the entire margin path out of
   the index choice — L-009 restated for a spread business, where it is not a distortion but the
   whole result.
   *What would overturn it:* a disclosed contractual formula that decouples AMOC's selling prices
   from its feedstock cost.

3. **The borrowing-rate driver is declared UNDEFINED and the finance charge is held flat.**
   Interest-bearing borrowings are EGP 20,977,437 against equity of EGP 4,824,774,948; the
   company holds net cash. A rate on that denominator is noise, and the repair everyone reaches
   for — divide the charge by a broader liabilities total — is the trap. **This is the second
   independent observation of L-041**, on a different company in a different industry from EMFD,
   which produced it. Decided in the pre-registration before any number was computed.
   *What would overturn it:* AMOC disclosing material interest-bearing borrowings.

4. **Volume is FLAT, and flat is the optimistic case here.** The previous edition grew every
   line and took its ranking from value growth between two disclosed halves. Audited tonnage ran
   1,492 / 1,548 / 1,449 / 1,433 / 1,262 thousand tonnes over FY2021–FY2025 — down 18.5% from the
   peak, six of eight lines shrinking. The base year is the transition half annualised at 1,616kt,
   **12.5% above the five-year mean and above every full year in the record**. The walk-forward
   measures even a flat rule as over-forecasting by 7.6% in eight of nine cells. Registered as
   **L-052**.
   *What would overturn it:* a disclosed increase in EGPC's feedstock allocation, which is what
   actually sets this plant's throughput.

5. **Other revenue is driven from credit interest, not from currency gains.** Note 14-B shows the
   line is dominated by interest on the company's own cash (EGP 417mn of EGP 800mn in FY2025).
   The previous edition described it as devaluation FX gains and assumed it to zero. The
   walk-forward then showed that zeroing the volatile remainder loses to simply carrying the
   whole line forward — registered as **L-051**.
   *What would overturn it:* a year in which the non-interest components are genuinely nil.

### Findings recorded but NOT acted on

- **No correction was adopted.** Ruled before any error was computed: nine cells cannot support
  an estimated correction and a separate confirmation sample. Sixteen of twenty-one drivers
  "pass" the sign-stability clause, which is a degenerate test at this size rather than sixteen
  warranted corrections.
- **The method loses to "no change" on the profit line** (skill −1.128). Registered as **L-050**
  and stated in the delivered study's §7.

### AMOC — second pass, 1 September 2026: what the first pass of this rebuild got wrong

The first pass published EGP 5.53 against a market price of 9.10 and was challenged on exactly
the right ground — a fair value at half the traded price is a finding about the model until it
has been shown to be a finding about the company. Recorded here because four of the five defects
are driver decisions, and because one of them is this run's own lesson going unapplied.

6. **The reviewed H1-2026 statements were downloaded on day one and never opened.** The study
   went on calling that half "a press release rather than a filing", rejected its gross-profit
   line and solved gross profit from the profit line. The filing confirms the released figure to
   0.03%. Base-year gross margin 8.997% → 9.653%.
   *What would overturn it:* nothing. Read the filings you have.

7. **The coherence test that rejected it estimated the half's other income by doubling one
   quarter's** — 451mn against a filed 197mn — and other income is the most volatile line in
   this statement. Registered as **L-053**.
   *What would overturn it:* a rejection built on an extrapolated volatile line that a later
   filing confirms was right.

8. **Three macro paths ran side by side and contradicted each other**: costs at Egyptian
   inflation 14.5%→9.5%, realisation at 9.0%→5.2%, the currency at 7.7%→3.6%. Both the price
   path and the currency path are now DERIVED from the one registered inflation series by
   relative purchasing-power parity, with crude held flat in dollars. **Two free parameters were
   removed, not added.** THIS IS L-048 — the lesson this name's own walk-forward produced hours
   earlier — sitting unapplied in the study being rebuilt. A register is only worth what it
   changes.
   *What would overturn it:* a disclosed pricing formula that decouples AMOC's realisations from
   the currency.

9. **The cash was charged for twice.** Operating cash flows discounted at a net-cash-weighted
   31.19% — 374bp above the cost of equity — and the same cash added back at face in the bridge.
   Now discounted at the unlevered rate, which for gross borrowings of 0.14% of the capital
   structure is the cost of equity. Registered as **L-054**.
   *What would overturn it:* nothing; the other consistent pair (blended rate, no add-back) is
   equally acceptable and is named in the lesson.

10. **Terminal growth of 5% against a terminal risk-free of 12.5%** that embeds the 7% inflation
    target — a business contracting 2% a year in real terms for ever, never stated as an
    assumption. Now 7%, inflation only, zero real growth.
    *What would overturn it:* a stated case for real decline, which the disclosed tonnage does
    not yet make.

**The balance sheet was a year stale** and is rolled to 30 June 2026: net cash 3,002mn (EGP 2.32
a share), book equity EGP 4.70 a share, dividends payable halved.

**What survived unchanged:** the walk-forward and its finding that the method does not beat "no
change"; the conforming beta; the flat volume path — the filed twelve-month tonnage of 1,502,325 t
is a better base than the annualised half it replaced, and since the half to June 2026 annualises
to 1,388,482 t, flat remains the optimistic case.
