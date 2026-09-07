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

---

## EGCH — Egyptian Chemical Industries "KIMA" · EGX · gas-fed nitrogen fertiliser (registered class: petrochemical) · fundamental walk-forward 1 September 2026, FULL scope

Run directory `engine/egch_walkforward/`; study rebuilt as the 1 September 2026 edition in
`engine/egch_study/` (STANDARD_VERSION 2026.09.01). Eighteen fiscal years FY2008–FY2025 from the
company's own audited statements (ten older annuals retrieved from its portal for this run), 13
origins, horizons 1–5, 55 cells. Central EGP 3.76 (field 0.00–15.47) against a 13.98 close,
audited under `engine/egch_study/GAP_REVIEW_01-09-2026.md` (the edition's first pass printed
3.79; the cost-of-debt ruling in item 9 moved it).
Lessons registered from this run: L-064 and L-065 (ALL), L-206 and L-207 (STOCK, EGCH only); the
other 23 harvested drafts are declined with reasons in `engine/egch_walkforward/lessons_draft.json`.

### Driver decisions, and what each would take to overturn

1. **The macro path is ONE path, pre-registered (L-048 applied before the run).** World urea
   flat in dollars, the currency by relative PPP on the last published CPI differential, costs on
   the same CPI. Measured against the frozen-currency counterfactual it is better on every line
   (net-profit MAE 162% vs 205%), and it is still far from the outturn because Egypt held the pound
   through FY2017–FY2021 and then devalued in steps. The cost lives in the macro share (22% on
   revenue), not in a multiplier.
   *What would overturn it:* a currency regime that follows PPP, where the macro share would rise
   and the coherent path would be the whole answer.

2. **Currency losses on project debt do not sit in the income statement of a company that
   capitalises borrowing costs.** Driver D7 (loss on dollar debt × ΔFX) was the single largest
   source of net-profit error (−41% of revenue on average): the company booked a currency result of
   0 in FY2023 and +279m in FY2024 during a 52% devaluation, because the revaluation of the KIMA-2
   consortium loan goes to construction in progress (the 9M FY2026 auditor's letter names the
   exception). For the study this means the translation loss reaches equity through net debt in
   the bridge, never through EBIT — which the FCFF build already respects.
   *What would overturn it:* a filing in which the loan revaluation is charged to profit, after the
   qualifying asset is complete.

3. **Interest formed on the borrowings that bear it was still wrong during construction.** Rates
   of 0.0%, 0.5% and 2.4% at origins FY2018–FY2020 are what the income statement shows while
   interest is capitalised; they are not the loan's cost. The rate was declared undefined below 10%
   of revenue (L-041) and held flat there.
   *What would overturn it:* a company that expenses all borrowing costs, where the opening-base
   rate is the loan rate.

4. **Tax by statutory formula on a company that has paid no current tax since the new complex
   started** was the second-largest profit error. The study keeps 22.5% (the loss carry-forwards
   and the accelerated first-year deduction are not sourced at line level) and prices the
   explicit-window charge as an open construction: PV EGP 1,968m, EGP 0.99 a share.
   *What would overturn it:* the deferred-tax note read at line level showing the shield and its
   expiry, at which point the explicit-window tax becomes a sourced driver.

5. **Flat urea tonnes over-forecast by 9.3% in all three unit-window cells** (586kt → 522kt →
   513kt on gas curtailment) — the same flat-volume lean AMOC measured (+7.6%, 8 of 9). The study's
   utilisation path (91–95% of plate) starts below the FY2022/23 actual and is banded by gas
   availability.
   *What would overturn it:* a year in which the summer gas curtailment does not recur.

6. **The terminal inflation equals the terminal growth (5%/5%, zero real growth) — L-055
   applied.** The 8 August edition discounted a 5%-growth perpetuity at a rate built on 7%
   inflation. Worth +EGP 0.15 on the carried-through lens together with the conforming beta.
   *What would overturn it:* a stated case for real decline, which the disclosed capacity does not make.

7. **A conforming EGX30 beta (1.030) replaces a withdrawn 35-name composite (1.053)** through
   `beta_regression.own_stock_beta()`; the interval is wide (0.72–1.34) and its lower bound is priced
   as the beta alternative (+EGP 0.82).

8. **The cost-by-nature notes in the prior extraction did not foot and were not used** (misses of
   247k, 36.3m and 63k EGP against the printed cost of sales). An extracted note that does not foot
   is not a source; cost of sales is one line on one escalator in the calibration, and the study's
   gas/materials split remains a flagged construction.
   *What would overturn it:* the notes re-read from the rendered pages and footing.

9. **The cost of debt is built year by year on the study's own currency wedge, through the
   house builder, with its warnings printed and the sovereign floor priced — not adopted.**
   The book is 99.7% dollar; the 11.7% dollar coupon is carried at local-equivalent cost
   Kd_t = (1 + 11.7%)(1 + wedge_t) − 1 on the same relative-PPP wedge the revenue build uses
   (7.4% → 2.5%), giving 19.99% in year one gliding to 14.54%; the 0.3% local facility at its
   disclosed 19.4%. Two consistency warnings fire and are printed in §1.8: the local facility
   sits below the 23.00% sovereign yield, and the dollar leg sits below the 16.63% normalised
   risk-free rate in FY2028/29–FY2030/31. The sovereign-floored alternative (every leg at
   23.00% + the company's own spread over the policy rate, which its facilities print as nil)
   is a labelled row in the contested-constructions table and the Sensitivity sheet: −EGP 0.44
   on the carried-through lens (−0.63 → −1.06). The disclosed rates lean toward the price, so
   using them as disclosed is the conservative direction for a study already far below it.
   *What would overturn it:* a new facility priced at or above the sovereign, or a refinancing
   of the dollar loan, at which point the disclosed rate and the floor coincide.

### Constructed drivers carried without a source, with their values (the register's L5 layer)

Each is an assumption the filings do not supply, flagged as such in the study, and priced
where it moves the answer. Listed here so the next petrochemical study reads them before
constructing its own.

*Refreshed 5 September 2026 after an outside audit found this block a full edition stale —
it still named a driver [R-TERM-01] had removed from the study, and quoted a terminal
risk-free rate built on a construction and an inflation path the study no longer uses. A
ledger that describes an edition the study has moved past is worse than an empty one,
because the next study of this class reads it as current. Every figure below is now from
the committed record.*

| driver | value | what it does | what would overturn it |
|---|---|---|---|
| ~~`roc_terminal` — terminal return on invested capital, 18%~~ | **RETIRED 5 September 2026** | It set the terminal reinvestment rate through g / ROIC, and this entry called it "the largest unsourced input in the study". [R-TERM-01] removed that construction from this study entirely: the terminal no longer reinvests a share of profit, it charges what replacing the plant costs at today's prices, so there is no reinvestment rate left to contest. Kept struck through rather than deleted, because a driver that WAS the largest unsourced input and then stopped existing is the more useful record. | — |
| `gas_share_of_materials` — the share of the single disclosed materials line allocated to gas | 75% | The largest modelled allocation in the study. It implies **1,292 m³ of gas per tonne of ammonia**, and that implied rate is now BRACKETED by two disclosed figures rather than only sanity-checked against a range: the auditor's own standard of 1,200 m³/t below it, and that standard plus the auditor's disclosed FY2024/25 loss of 120.9 m³/t (1,320.9) above it. Adopting the bare standard is priced at **+EGP 0.84**. | A statement that splits the materials line, or a segment disclosure giving gas cost directly. |
| `fa_avg_age_years` — the measured average age of the fixed-asset base | 4.45 years (DERIVED) | Accumulated depreciation over the year's own charge — an identity, not an assumption. It sets the escalator that turns book depreciation into replacement cost in the terminal. Where a company discloses too little to measure it, half the implied life (11.04 years) has to be assumed, which on this base is worth **−EGP 2.22**. | A residual-value or reassessed-life disclosure, either of which breaks the identity [L-328]. Neither is in these accounts, and that is what makes this one of only two names in the book where the age is measured rather than assumed. |
| `kd_usd_lt` — long-run dollar cost of debt | 9% | The terminal dollar coupon after the project loan reprices, carried at (1+9%)(1+2.54%)−1 = 11.77% local-equivalent on the dollar leg (11.79% once the 0.3% local facility is blended in). | A refinancing at a disclosed rate; a dollar loan priced off a published Egyptian corporate curve. |
| `real_rate_lt` — long-run real policy rate | 5.5% | Builds the terminal normalised risk-free rate, and the CONSTRUCTION was corrected on 5 September 2026: it is the house macro path's own **additive** form, 7% terminal inflation plus 5.5% = **12.50%**, not the compounded 12.885% this study computed for itself while its terminal GROWTH already came from the same path additively. One model, two conventions about inflation [L-055]. | A published long-run neutral-rate estimate for Egypt, or a decade of real rates settling elsewhere. |
| `anna_cash_margin` — nitrate conversion margin over own ammonia | 32% | The new complex's contribution before its depreciation; with it the complex earns −66m after depreciation at 50% utilisation. | The company's own first full-year segment disclosure for the complex. |
| `anna_util_base` / `anna_util_bull` — project utilisation in the terminal year | 50% / 70% | Half is the existing plant's observed record against its own plate under the same gas regime; 70% is a well-run nitrate line. The 70% alternative is **+EGP 0.43**. | A year in which the existing plant runs above 70% of plate, or a gas-supply contract that removes the summer curtailment. |
| `dep_escalation` — escalation on the existing depreciation base | 2% a year | Ordinary additions to the pre-project asset base; project depreciation is built separately from its own cost. | A fixed-asset note showing additions to the old base running materially above or below 2%. |
| `fx_terminal_wedge` — terminal currency wedge | 2.54% (DERIVED) | (1+5.0%)/(1+2.4%)−1: the steady-state depreciation implied against US inflation; carries the terminal dollar debt and the terminal revenue. Derived, not typed. | A terminal inflation other than the one this wedge was struck against, which would move the wedge with it. |
| `anna_winddown_cost` — cost of stopping the programme | EGP 1,000m | Charged in year one of the capital-discipline case only: contractor settlement and preservation on a 27.8%-spent site. | A disclosed termination schedule in the consortium loan or the construction contract. |

### Findings recorded but NOT acted on

- **No correction was adopted.** Every driver correction that passed the expanding-window sign
  test made the following origin worse when applied (revenue 0 helped / 3 hurt; cost of sales 0/3;
  debit interest 0/2; selling 1/2; admin 2/1), and none matches how the driver class is built
  across the book. All five are watch flags in `corrections_log.json`.
- **The method loses to "no change" on net profit** (skill −0.559 on the log record, at four of
  five horizons) and beats it on revenue (+0.146) and cost of sales (+0.273). Stated in the
  delivered study's §7; years three to five published as ranges (Appendix A.4).
- **The plant replacement** (old electrolytic plant shut FY2019; gas-fed complex from FY2020) is the
  structural break the record turns on: excluding every cell touching FY2020–FY2022 halves the
  revenue error and leaves the margin over "no change" about the same.

---

## ARCC — Arabian Cement · EGX · integrated cement (registered class: cement and heavy industrial) · re-struck 3 September 2026

The ledger carried **no ARCC entry at all** against 23 House-ring drivers until this date.
An outside audit found that on 3 September 2026, and the omission is worth stating rather
than quietly filled: the ledger exists so the NEXT study of a class does not re-derive what
this one decided, and a study with no entry contributes nothing to that.

### The driver decision this edition did NOT change, and why it is recorded

**PRICE IS ANCHORED ON THE EXIT QUARTER AND COST ON THE FULL YEAR. The two legs are on
different clocks and the study does not say so.**

| leg | anchor | value |
|---|---|---:|
| realised local price | **Q4-2025 exit rate**, disclosed | EGP 3,118/t |
| — the full-year average it is 7.2% above | FY2025 | ~EGP 2,908/t |
| cash cost per tonne sold | **FY2025 full year**, from notes 5 and 6 | EGP 1,541.90/t |

The price leg follows the standing rule that a near-term reviewed actual outranks a stale
full-year rate. The cost leg does not. Applying that rule to one leg and not the other
produces a spread that is **neither** of the two coherent readings — it sits between the
full-year spread and the exit-quarter spread — and nothing in the study tells a reader that
its numerator and its denominator come from different periods.

**Direction, stated so it is not mistaken for a neutral choice:** on the figures above the
mixed clock gives a **narrower** spread than an exit-quarter pair would. The inconsistency
runs AGAINST the value.

**Why it is not corrected in this edition.** The outside audit reports that the FY2025
investor presentation discloses **Cash Cost/Ton of EGP 1,448** for 4Q2025 on the *same
slide* as the EGP 3,118/t price this study already uses. **That figure is not in this
repository**: `grep` returns zero hits across the study's committed artefacts, and the
presentation itself is absent from `sweep_register.json`. Under SIGCM clause 1 a figure
this desk cannot open is a figure this desk does not use, so it is recorded here with its
source named rather than typed in from a report. It is the first thing the next ARCC pass
should fetch.

### Sweep gaps carried, both of which this edition inherited

1. **The FY2025 investor presentation is not in the sweep register.** [The Step 2A rule
   makes investor-relations material MANDATORY, not optional, for volumes, prices,
   utilisation and segment data no financial statement carries — and it is the source of
   every tonne in this build.] Tagged `COMPANY_IR` nowhere; the register carries no IR tag
   at all.
2. **The H1-2026 interim is not in the sweep register either** — and it is the balance
   sheet the bridge stands on. The bridge is right; the register does not record where it
   came from.
3. **`engine/arcc_study/sweep.py` is hand-rolled and never imports `research_sweep.py`**, so
   the eight enforced invariants that module exists to apply have never run over this
   study's register. That is the [R-ENF-01] species inside a study rather than around one.

### What would overturn any of this

Fetching the presentation and finding the 4Q2025 cash cost is NOT 1,448, or that it is
measured on a different basis from the study's own cash-cost definition (which excludes
provisions and expected credit losses — revision 3 of this study carried them inside "cash
cost" and they are not cash). Either would settle the question the other way, and neither
can be decided from the repository as it stands.

---

## STC · Saudi Telecom Company · Tadawul 7010 · 05-Sep-2026
**Class:** telecom operator with a captive bank and a listed systems-integration subsidiary
**Context:** delivered study, rebuilt; `engine/stc_study/`
**No fundamental walk-forward exists on this name.** The scope decision is FULL on 16
sourceable fiscal years back to FY2010 and the run is PENDING — so every entry below is a
driver decision that has NOT been tested against what this company went on to report. Read
them as decisions taken, never as findings.

### Drivers set, and from what

| # | driver | rule as set | set from | tested? |
|---|---|---|---|---|
| D1 | segment revenue, 12 disclosed segments | each grows at its OWN measured two-year real rate, deflated by a published price index, fading to zero real by the last explicit year | note 9 of the audited statements, revenue and gross profit for every segment, three filed years | no |
| D2 | the Saudi operating segment's revenue | volume times price: mobile and fixed subscribers times revenue per subscriber, each faded to zero real | subscriber counts from the earnings presentations, price BACK-SOLVED against the audited segment revenue — a derived rate, not a disclosed one | no |
| D3 | gross margin, four cost lines | on the bases the filings name: the provisioning levy on the Saudi segment, the licence fee at its own rate, repairs on the asset base, contract amortisation on subscribers | note 35, seven lines by nature, three filed years | no |
| D4 | gross margin, the other three cost lines | HELD at each segment's own disclosed margin | no sourced driver exists — no unit rate for network access, no headcount anywhere in the filings, and "Others" is a residual of three unrelated things | no |
| D5 | operating cost between gross profit and EBITDA | its own three-year average share of revenue | filed statements | no |
| D6 | capital intensity | the three filed years' own mean of 1.161 times the depreciation of the base being renewed, held flat | filed statements — NOT management's guided band, which is scored and never consumed | no |
| D7 | depreciation | the FY2025 filed ratio to revenue, held flat | filed statements | no |
| D8 | working capital | projected from the asset-conversion cycle rather than plugged | filed statements | no |
| D9 | tax | 8.03% measured on EBIT with the disclosed prior-year reversal taken out; the debt shield stays at the statutory rate | note 33(a), which discloses the reversal on its own line | no |
| D10 | beta | own-stock weekly regression against the published index of the exchange it is listed on, at its point estimate | 4.91-year window, 252 paired weeks, R² 30.2% | n/a |
| D11 | terminal | maintenance at the 21-year average asset life the accounts themselves imply, on the sanctioned module | the property, plant and equipment note | no |
| D12 | terminal growth | 2.0% nominal, stored as a REAL rate of 0.0% on the house Saudi path | the house macro path, never a number of this study's own | no |

### Decisions worth carrying to the next same-class study

1. **A telecom's cost side is only partly buildable and the split is worth knowing in
   advance.** Of the seven cost lines a Saudi operator discloses by nature, four have a
   sourced base that is not group revenue and three do not. Building the four is a real
   correction and it is SMALL — -0.163% of the answer on this name — because the offsets run
   both ways: the provisioning levy and the licence fee fall against a group growing faster
   than their own bases, while repairs and contract amortisation rise. **Expect the effect
   to be small and build it anyway**, because the alternative is a margin nobody can trace.

2. **The unit price is usually derived, not disclosed.** Subscriber counts come from the
   earnings presentation and are footnoted as unaudited; revenue per subscriber has to be
   back-solved against the audited segment revenue. That is unit economics on a derived
   rate, which is level `derived` and not level `unit` — and this study's unit share is
   therefore 0%, not the two thirds a reader might infer from "built as volume times
   price". **Say which half of the unit economics is disclosed.**

3. **Headcount is not disclosed and employee cost is the second-largest line.** Searched
   across every audited set and both presentations; the negative search is registered.
   A same-class study should expect to hold this line rather than build it.

4. **Segment growth measured beats segment growth typed, and the difference is
   composition rather than level.** Group real growth measured from the audited segment
   table came out close to what the previous edition's typed arrays implied in aggregate;
   what changed was that 12 segments growing at their own rates compound differently from
   four aggregates growing at an average of them. The answer moved -15.4% on that lever
   alone.

5. **A pegged currency means the cost-of-capital schedule is FLAT and that is not an
   oversight.** The riyal's peg puts this economy at its terminal cost of capital by
   construction, so there is no normalisation to glide toward; the module returns a flat
   ladder and says so. A same-class study in a transition market must NOT copy this shape.

### The most consequential contested judgement, both ways

which lens is the answer: the cash-flow model is the central at 38.0806 against the enterprise multiple on this company's own trading history at 48.0753. Published side by side, never averaged.

---

## ELEC — Electro Cable Egypt (EGX) · fundamental walk-forward, 07-09-2026 · **SKIP**

**Scope: SKIP — walk-forward not run — insufficient sourceable history (4 years).**
Run directory `engine/elec_walkforward/`. No driver was projected and none was scored,
so this entry records what the filings decided rather than what a forecast measured.

**Class.** No registry row exists for a cable manufacturer and ELEC recorded no class.
Run as the nearest pattern — *refiner, commodity pass-through on a thin spread* —
adapted inside the ADNOCLS skeleton, because a cable maker buys copper at a quoted
world price and sells cable at that price plus a conversion spread, which is the shape
that row exists for. **No registry row was added**: [R-LENS-03] adds a class when a
different LENS carries the weight, never when the industry differs, and a cable maker's
lens set is identical to the refiner row's. Reasoning in `CLASS_DECISION_07-09-2026.md`.
ELEC is the **third** independent name to meet this wall (after SAVOLA and EMPOWER) and
is noted on that open escalation rather than resolved here.

### What the archive decided

| basis | years sourceable | note |
|---|---:|---|
| consolidated — **the basis this study models** | 2 (FY2019–FY2020) | the company has issued no consolidated statement since FY2020 while holding a 99.99% subsidiary (note 5) |
| standalone | 4 (FY2020–FY2023) | the parent entity only |

Re-probed 07-09-2026 rather than taken from the record: the issuer's index returns HTTP
200 and lists **61 statement files**; **19 of 19** on the live host return HTTP 404; the
**42** consolidated ones sit on a host whose DNS does not resolve; the index carries no
period after 30-09-2025. **Scoreable origins: zero**, by construction.

### Driver decisions a same-class study should inherit

1. **Interest is built from bank credit facilities + the long-term loan + the lease and
   financing-arrangement liabilities (note 4/2), and from nothing else.** Trade payables,
   related-party balances, tax liabilities, provisions, deferred tax and dividends
   payable bear no interest. Measured on this company's own accounts, the broad
   denominator understates the rate by **3.09 to 4.15 points** and puts it **below the
   Egyptian sovereign in two of three years** — which is [R-COC-01]'s own refusal, and
   is a way of catching trap (i) without knowing the right answer.

2. **The useful life is DERIVED and is a band, not a point.** Route (1) failed: the
   policy note discloses spans (10–50, 4–25, 5–20, 5–20, 5, 5–10) with no dominant class
   and no weighting. Route (2) gives **24.13 years** on the full depreciable base and
   **17.54** excluding the 27.3% of that base the note itself calls fully depreciated and
   still in use, with a prior-year control at 24.99. `engine/elec_study/useful_lives.json`.

3. **Capex is DISCLOSED, and the identity must not be used here.** These years carry
   large disposals (FY2021 proceeds of 103.5mn on a book gain of 78.1mn), so
   `capex = ΔPP&E + D&A` does not close. The cash-flow statement discloses the figure and
   it reconciles exactly to note 3's own additions.

4. **The consolidated/standalone wedge is measured, never assumed, and it is not a single
   ratio.** At FY2020, the one year existing on both bases, the group is **1.73x** the
   parent on revenue, **3.58x** on gross profit, **34.49x** on operating profit and
   **2.04x** on net profit. Non-controlling interests are EGP 44, so this is not a
   minority effect. **The two bases are not chained.**

5. **The share count comes from the recital's par, and no count is carried back.** Note
   13 of the FY2021 filing states issued capital of EGP 711,447,385 in 711,447,385 shares
   of EGP 1, a 1:5 split ratified 24-01-2021 taking par to EGP 0.20 and the count to
   3,557,236,925 — which the identity reproduces exactly. FY2020 is therefore recorded
   **pre-split**.

### The most consequential finding, and it corrects an earlier reading

The 06-09-2026 audit's `[R-ANCHOR-01]` claim — that the study's terminal EBITDA margin of
12.30% is "less than half of the lowest filed year" against a filed record of
25.33%–30.68% — **does not survive the filings, and its premise is withdrawn.** That
range is the study's own committed `hist_is`, which is vendor data, and two of its three
years have no filing at all. The filed standalone range is **1.43%–17.49%**, which puts
12.30% **inside** it; the price's reverse read of 27–28% sits at **1.6x** the highest
margin the company has filed. **`fair{}` was not moved in either direction** — the study
is not rebuilt, because this run establishes that its historical panel cannot be
reconciled to anything the issuer has published, which is a SIGCM clause 1 condition
rather than a disagreement with the market.

---

## PHAR — Egyptian International Pharmaceutical Industries (EIPICO) · EGX · generic and branded pharmaceutical manufacturer · fundamental walk-forward, 07-09-2026 · **LIGHT**

**Scope: LIGHT.** Seven sourceable fiscal years, FY2019–FY2025, every one out of EIPICO's
own annual reports from its own investor-relations page. Five origins FY2020–FY2024,
horizons 1–3, twelve scoreable cells per driver, 150 scored cells. The window stops at
FY2019 because the FY2019 annual report is a board report carrying operating KPIs and no
financial statements, so FY2018 has units and no accounts and is left out rather than
fabricated. The exchange and regulator disclosure portals were re-attempted on the day and
neither resolves.

### Drivers, and the mechanical rule each was scored under

| driver | source of the level | rule at a historical origin |
|---|---|---|
| packs produced (thousand) | the company's own annual-report indicator table, every year but FY2020 | trailing compound growth CLIPPED to Egypt's population growth ±2pp — the exogenous anchor, so the volume driver is never the company's own trend alone |
| revenue per pack | parent sales value ÷ packs, both from the same indicator table | trailing compound growth; on the macro legs, the origin's own inflation vintage or the realised path |
| cost per pack | consolidated cost of sales ÷ the consolidation ratio ÷ packs | **the SAME escalator as price**, so the gross margin is an OUTPUT and the two cannot drift apart |
| consolidation ratio | consolidated revenue ÷ parent sales value | held at the origin's own value; it has run 1.015–1.059 across the window (the EIACO ampoules subsidiary) |
| marketing | consolidated income statement, FY2021 onward | trailing mean share of revenue (variable) |
| administrative block (R&D + G&A + board) | same | escalated at inflation off the origin's own level (fixed) |
| provisions and credit losses | same | trailing mean share of revenue |
| **finance cost** | **long-term loans + long-term credit facilities + short-term loans + creditor banks, AND NOTHING ELSE** | the origin's own effective rate × average interest-bearing debt |
| capex | consolidated cash-flow statement, FY2021 onward | trailing mean share of revenue; an INPUT, never solved out |
| depreciation and amortisation | consolidated cash flow: depreciation + right-of-use + intangibles | roll-forward of PP&E **plus projects under construction** at the origin's own book rate |
| interest-bearing debt | balance sheet | the funding identity, capex + dividends + ΔWC − net profit − D&A, two fixed-point iterations |
| capital gains, FX result, other income | — | **SET TO ZERO at every origin.** A mechanical rule cannot forecast a currency result and inventing one is the judgement driver this exercise forbids |
| tax | income tax + deferred tax + the takaful contribution | trailing mean effective rate on profit before tax |

### Decisions a later study of this name or class should not have to rediscover

- **THE INTEREST DENOMINATOR IS THE BORROWINGS, NOT THE LIABILITIES.** On FY2025 the same
  finance charge gives 14.83% over average interest-bearing debt and 11.87% over total
  liabilities — 296 basis points, because trade payables, other creditors, provisions and
  tax payable are a quarter of this balance sheet.
- **THREE COST-OF-DEBT FIGURES EXIST HERE AND THEY ARE NOT THE SAME QUANTITY**: the
  finance-cost rate (14.83% FY2025), the interest rate on credit facilities the study
  computes (14.17%, which excludes EGP 57.6mn of bank commissions — an interest rate is
  computed on interest), and the all-in rate including EGP 551.1mn capitalised into
  construction (20.30%). Capitalised interest is 43% of the expensed charge, which is a
  named mechanism [R-COC-01 AMENDED] admits and the reason a trailing effective rate is
  not the comparator for a marginal one on this book.
- **CAPEX LANDS IN PROJECTS UNDER CONSTRUCTION AND STAYS THERE FOR YEARS.** EGP 866mn at
  FY2022 became EGP 5,694mn at FY2024 and EGP 2,086mn was transferred into fixed assets in
  FY2025 alone. Any depreciation roll-forward that charges capex on arrival over-charges;
  this run's did, by +0.499 log, its only over-forecast driver and its worst against the
  naive benchmark.
- **THE DISCLOSED USEFUL LIFE IS A SCALAR TABLE, WHICH IS UNUSUAL.** Buildings 50,
  production and service machines 15, transport and tools 5, furniture 10, land not
  depreciated — no bands, so the gross-cost weighting to 13.7954 years is unambiguous.
  The FY2025 report carries the identical table, so no life was reassessed.
- **THE PACKS SERIES HAS A HOLE AND A REDEFINITION.** The condensed FY2020 report
  publishes no packs figure at all, and the FY2024 figure was re-presented from 306,133 to
  299,608 thousand between the FY2024 and FY2025 reports with no reconciliation. Score the
  unit driver against each origin's own report.
- **SIX PRINTED CELLS IN THESE FILINGS DO NOT FOOT**, and the largest — the FY2022 gross
  profit, EGP 18.0mn low — is carried forward into the next year's comparative, so
  checking one filing against the next confirms the wrong number. Only the statement's own
  chain to profit before tax separates them.

### What the run concluded

No correction adopted; every candidate DECLINED, six of seven because a LIGHT run at three
horizons cannot admit a single cut under the cut-invariance clause and untestable is never
stable. Fair value unchanged at EGP 36.64 (Frame A) / 54.24 (Frame B). Far-year bands
published for horizons one to three only, declared as SPANS over three to five
observations rather than percentiles, oriented actual-over-forecast.

---

## GBCO — GB Corp S.A.E (EGX) — fundamental walk-forward, 07-09-2026

**Class: no registered row.** GB Corp is an automotive assembler-distributor (GB Auto) with a
**captive non-bank lender** (GB Capital) and one large unlisted associate. `LENS_REGISTRY` has
thirteen rows and none of them is this: `holding company` stores exactly the lens set the name
needs (SOTP primary, relative multiple and book beside it) and refuses it on the ROW'S NAME
alone, and GB Corp is not a holdco by that rule's own test — a holdco IS its stakes; this is an
assembler with a finance arm. Filing it as one would put a wrong label in the committed record.
**Proposed for registration:** `automotive assembler-distributor with a captive lender` →
`('sotp', ('relative_multiple', 'book_value', 'ev_ebitda_own_history'))`. Not registered in
this run because `lessons_register.py` is a shared register and four other runs are in flight.
The name is the fifth on the lens-registry escalation and stays on the [R-LENS-03] ratchet.

**REGISTERED, 07-09-2026, later the same day — appended rather than rewritten, because a
dated record says what was true when it was written.** The principal ruled: build a model
for this company rather than adopting the holding-company lens, and fall back to that lens
only if the bespoke one fails. It did not fail. The row registered is
`automotive assembler and distributor with a captive lender` →
`('sotp', ('dcf', 'residual_income', 'relative_multiple', 'book_value'))`.

**IT IS NOT THE SET PROPOSED ABOVE AND THE DIFFERENCE IS THE WHOLE POINT.** The proposal
carried neither `dcf` nor `residual_income`, and both turned out to be the reason a new row
was owed at all rather than a rename. A group cash flow cannot reach a 41.61% interest in an
unlisted company the group does not consolidate, so the sum of the parts must be the primary
with the cash-flow lens INSIDE it as one of the parts — which is what `sotp` has always meant
in `LENS_KINDS`. And the lender has to be valued on its own equity against what that equity
earns, which is residual income arriving as a PART; the delivered study carried it at book
times one, and book times one is the weighting of book value [R-LENS-03] forbids outright.
`ev_ebitda_own_history` is NOT in the registered set: an enterprise multiple on a group whose
reported earnings swing on associate marks measures the marks rather than the business.

The escalation `lens-registry-has-no-row-for-an-auto-assembler-with-a-captive-lender` is
closed with the answer written into `research_protocol.py` and `lessons_register.py`. The
name is OFF the [R-LENS-03] ratchet. The SAVOLA escalation beside it is untouched and is a
different question, as that escalation's own recommendation said it should be.

**Scope: FULL.** FY2012–FY2025, fourteen sourceable fiscal years, all tier A from GB Corp's own
documents, all footed. Nine origins FY2016–FY2024, horizons 1–5, 245 scored cells.

| driver | mechanical rule at the origin | outcome |
|---|---|---|
| revenue | trailing 3-year CAGR damped 20% a year toward the trailing 5-year CAGR | bias −0.004; **flips sign at 6 of 6 admissible cuts** — a mean, not a bias. Beats freeze at every horizon. |
| gross_margin | trailing 3-year mean, held flat | bias −0.223; flips at 2 of 6 cuts; **LOSES to freeze at h1–h4** |
| sga_ratio | trailing 3-year mean of (selling + admin) / revenue | bias −0.180; sign holds at every cut |
| operating_profit | built from the above, margins an OUTPUT | bias −0.379; sign holds at every cut; CI excludes zero at every horizon |
| finance_cost | *as scored*: net finance cost as a ratio to revenue | bias +0.401, MAE 0.890, CI straddles zero at every horizon, **LOSES to freeze at four of five** |
| tax | Egyptian statutory rate known at the origin (22.5% from FY2015) | — |
| net_profit | operating profit less finance cost, taxed | bias −0.692, n=15, thin |

**THE FINANCE-COST DRIVER IS THE ENTRY WORTH READING.** Built as a ratio to revenue it
inherits the 2016–17 float's funding shock and carries it forward five years, forecasting
LOSSES at the FY2016, FY2017 and FY2018 origins for years GB Corp was profitable. The correct
construction is the borrowings that actually bear the interest — and on this name the leak runs
the OPPOSITE way from trap (i)'s usual shape: the numerator is too NARROW, because **GB
Capital's cost of funds (EGP 3,756.9mn in FY2025) is booked in that segment's cost of revenue**
rather than in the group finance line. Group charge over total liabilities reads 7.05%, over
group borrowings 11.27%, and over the whole interest actually incurred **26.53%** — which
reproduces the disclosed CBE lending rate, and which the study now adopts.

**Corrections: none promoted; four watch flags** (gross_profit, operating_profit, sga,
net_profit — all pass the cut-invariance clause and all are OUTPUTS of two inputs whose own
signs are unstable, so a correction on them would be a multiplier standing in for a
mis-specified margin rule).

**Macro/company split:** 22.1% macro, 77.9% company, over 23 revenue cells against Egypt's own
point-in-time IMF WEO vintages. The split's own check is inverted here and worth more than the
split: **the model carries no inflation term at all**, so the attribution is after the fact.

**Not built, and flagged rather than filled:** a volume-anchored revenue driver. Unit volumes
are disclosed from FY2019 and in the annual-report business reviews before that, but an
exogenous Egyptian market-size series dated at every origin was not obtained from company
documents inside this run.


---

## SCEM — Sinai Cement Company S.A.E. (EGX) · fundamental walk-forward, 07-09-2026

**Class:** cement and heavy industrial · **Scope:** LIGHT — five sourceable fiscal years
(FY2021–FY2025), five origins, horizons 1–3, **nine resolved driver-cells** ·
**Central:** EGP 123.27 → **116.93** against a spot of 100.50.

**THE ARCHIVE IS THE SCOPE DECISION.** Sinai Cement publishes exactly six documents on its
own website. Three of them had never been downloaded before this run; opening the two
English ones (FY2022 and FY2023 audited) took the span from three sourceable years to five
and the scope from SKIP to LIGHT. The sixth is Arabic and its figures are Eastern Arabic
numerals that no OCR route available here reads, so **FY2020 is left out and the window
shortened rather than filled from a vendor**.

**THE DISCLOSURE GAP THAT DECIDES EVERY DRIVER ON THIS NAME: NO PHYSICAL VOLUME IS
DISCLOSED ANYWHERE.** Not a tonne, not a capacity, not a utilisation, in any of the six
filings, in any year. The finest sourced level for this issuer is the **cost-note line**,
so revenue is `derived` and never `unit` under [R-SIGCM-02], and the tonnage the delivered
study's model runs on is an industry-ring driver from a plant register and the trade press.
The next study of this class should expect the same and check before assuming a unit build
is available.

| driver | mechanical rule at the origin | what it scored |
|---|---|---|
| revenue | revenue_t x point-in-time Egypt real GDP growth x point-in-time CPI, from the IMF WEO edition that EXISTED at that year-end | bias -0.561, n=9, outturn 1.75x the forecast |
| materials, fuel, power, packing | the same volume and price legs — variable in both | bias -0.287, n=9, outturn 1.33x the forecast; **era sign FLIPS** |
| cost-of-sales wages | escalated at CPI alone; fixed in real terms | bias -0.241, n=9, outturn 1.27x the forecast |
| cost-of-sales maintenance | escalated at CPI alone | bias -0.503, n=9, outturn 1.65x the forecast |
| transfer and loading (haulage) | volume x price; variable | bias -0.452, n=9, outturn 1.57x the forecast; **era sign FLIPS** |
| general and administrative | CPI alone; overhead fixed in real terms | bias -0.590, n=9, outturn 1.80x the forecast |
| depreciation and amortisation | PP&E roll-forward at the DISCLOSED weighted rate on gross cost | bias -0.025, n=9, outturn 1.02x the forecast; **era sign FLIPS** |
| finance expense | the origin's own realised rate ON THE BORROWINGS THAT BEAR IT x debt held flat | bias +0.477, n=9, outturn 0.62x the forecast |
| interest income | the origin's own realised deposit rate x the modelled cash balance | bias -0.953, n=9, outturn 2.59x the forecast |
| capital expenditure | the disclosed cash-flow run rate held flat in real terms | bias -0.831, n=9, outturn 2.29x the forecast |
| working capital | the origin's own working capital as a share of revenue | bias -0.704, n=3, outturn 2.02x the forecast; **era sign FLIPS** |
| EBITDA | REBUILT from the drivers above, never forecast | bias -2.220, n=6, outturn 9.21x the forecast |
| net profit after tax | rebuilt; tax by the regime known at the origin, 22.5% on positive profit | bias -1.885, n=2, outturn 6.59x the forecast |

**THE SKILL VERDICT IS POSITIVE AND IT IS THE FIRST THING TO READ.** Against FREEZE
(every line flat at last actual): +0.185 / +0.129 / +0.123 at horizons one, two and three.
Against TREND (trailing CAGR): +0.239 / +0.231 / +0.205. The method beat both at every horizon
tested — which PHDC's run did not, on net profit, at any horizon. The margin is a tenth to
a quarter of the naive error and it rests on nine cells from one company.

**TRAP (i), MEASURED ON THIS NAME AND WORTH CARRYING TO THE NEXT.** Finance expense over
the borrowings that actually bear it runs 7.97–12.64 per cent across FY2022–FY2025; over
total liabilities it runs 1.35–7.34 per cent. A factor of 1.7x to 5.9x, and the broad
denominator would have implied this company borrowed at 1.35 per cent in an economy whose
policy rate was 19.5.

**THE DRIVER THAT IS MIS-SPECIFIED, AND IT IS THE VOLUME ANCHOR.** Egypt's real GDP growth
contributed between +0.04 and +0.16 of log revenue growth in every cell while revenue
compounded at 58 per cent nominal. Real GDP is not cement demand: domestic consumption rose
13.4 per cent in 2025 against GDP around 4, and the quota regime that capped output since
2021 was lifted permanently in July 2025. **This is L-058 on a second name.** The fix is an
Egyptian cement-consumption series at each origin's own vintage, which this run did not
have and did not invent.

**CORRECTIONS: NONE PROMOTED, 11 WATCH FLAGS, 2 REFUSED AS AGGREGATES — AND THAT WAS
PRE-REGISTERED.** Nine cells over four target years admit **zero** boundaries leaving five
on each side, so under [R-FCAL-01 AMENDED 07-09-2026] every driver here is UNTESTABLE for
stability rather than stable. Four candidates improve the out-of-sample error and none is
promoted; four make it worse, which is L-061's signature. Run through the shared instrument
`boundary_sensitivity.cuts_for()`, never reimplemented.

**MACRO/COMPANY SPLIT: about a third macro, two thirds company** on the drivers that carry
an inflation term. The split's own check passes — depreciation, finance expense and
interest income carry no inflation term and return zero to within a tenth of a point.

**THE LEVER THIS RUN APPLIED TO THE DELIVERED STUDY:** the terminal's useful life, from a
25.89-year figure (two disclosed RANGES resolved at their midpoints, then an ARITHMETIC
mean of the five classes' lives) to the **disclosed SCALAR 20-year machinery life** —
machinery being 69.5 per cent of note 4's gross cost. Worth −5.1 per cent. **The validation
the old figure carried was two errors cancelling**: an arithmetic-mean rate understating
the disclosed rates' own product, compared against a total that included intangible
amortisation. Recorded because the next name of this class will meet the same table shape:
note 3/2 discloses RATES, two of five classes as RANGES, and the two ordinary ways of
blending them disagree by a quarter.

**GUIDANCE LEDGER: EMPTY, and that is a finding.** This issuer publishes no forward
guidance, no results presentation and no earnings call, so no driver here can have
inherited a management lean.

---

## SWDY — Elsewedy Electric Company S.A.E. (EGX) — 7 September 2026

**Class: diversified industrial with a contracting arm.** Fundamental walk-forward
[R-FCAL-01], FULL scope: seventeen sourceable fiscal years FY2009–FY2025 from the company's
own investor-relations archive (233 documents retrieved), twelve origins FY2014–FY2025,
horizons 1–5, **750 scoreable driver cells and 105 recorded unscoreable** — the largest
fundamental sample this book holds and still one company.

**THE DRIVER ARCHITECTURE, AND WHY IT IS THREE LEGS.** [L-295], produced by this issuer,
says a group whose legs sit on different contract structures cannot be forecast on one
margin path. The scored revenue drivers are therefore the three groupings that survive both
segment re-cuts — CABLES, CONTRACTING, OTHER — each paired with its own cost driver on the
same recognition clock, and **there is no group-level cost driver in the table at all**.
One would break the matching by construction, and this issuer's contracting leg recognises
revenue over time (EGP 29.9bn of contract assets against EGP 81.3bn of contract liabilities
at FY2025), so trap (ii) is live here in a way it is not on a point-in-time seller.

**THE UNIT BUILD IS POSSIBLE ON THIS NAME AND ONLY INSIDE A WINDOW.** The company's own
"results at a glance" investor sheets publish cable tonnage, price per tonne and cost per
tonne from FY2012 to 3Q2022 and then stop. The unit drivers are scored only inside
FY2012–FY2020 and their cell count (20) is published against the rest (45). **The next name
of this class should look for the investor sheet before assuming the statements are the
finest level** — the audited statements carry no tonne and never did.

**THE BORROWING RATE, AND WHY THIS NAME MAKES TRAP (i) EASY.** At FY2025 total liabilities
are EGP 239.1bn of which loans and borrowings are EGP 62.5bn: trade and other payables,
contract liabilities, related-party balances and provisions together are more than TWO AND
A HALF TIMES the borrowings and none bears interest. Dividing the finance charge by the
liabilities total gives about 2.4% against a real 9.4%. The rate is formed on loans and
borrowings alone at every origin: 3.70% to 13.14% across the twelve.

**SKILL: BEATS "NO CHANGE" EVERYWHERE, LOSES TO A TRAILING CAGR ON THE TOP LINE.** Revenue
skill against FREEZE +15.7% / +19.5% / +17.7% / +30.3% / +46.0% at h=1..5; against TREND
+0.0% / **−3.3%** / **−13.1%** / **−6.4%** / **−5.2%**. Gross profit beats both. What the
ground-up build buys on this name is the MARGIN, not the scale, and the reason is that an
exogenous activity anchor cannot see a company taking share of a market being built —
contracting revenue went from EGP 2.7bn to EGP 87.1bn against Egyptian real GDP.

**BIAS: THE POOLED CENSUS SIGNATURE AGAIN.** Revenue −0.222 and cost of revenue −0.215 —
both under-forecast by nearly the same amount, so the margin is roughly right and the SCALE
is too low. Perfect foresight of inflation and the currency removes at most 28% of the
error on a company whose currency lost 85% of its value inside the window.

**CORRECTIONS: NONE ADOPTED. Two watch flags, two specification defects named.**
Depreciation offers the largest improvement any candidate makes (five origins of five, MAE
0.820 → 0.373) and is REFUSED: the roll-forward models additions and not the translation of
foreign subsidiaries, and note 17 adds EGP 9.94bn to machinery cost in FY2024 as an exchange
movement alone against additions of EGP 2.06bn. Finance costs pass on seven of eight and are
REFUSED for the same species of reason — the rule holds a flat charge on a debt book that
grew nine and a half times. **The next name of this class inherits both: a PP&E roll-forward
with no translation term and a level-persistent finance charge will under-forecast on any
issuer with a foreign asset base and a growing book, and the bias is arithmetic rather than
evidence.**

**THE DISCLOSED USEFUL LIFE: ROUTE ONE FAILS AND THE IDENTITY IS CORROBORATED TWICE.** The
policy note discloses five RANGES and no scalar — buildings 8–50, machinery 5–15, furniture
4–17, vehicles 5–8, leasehold "over 3 years or the lease period". The identity gives
**17.2627 years** (average depreciable gross cost over the year's own charge), and it is
confirmed by a second fiscal year of the same note (17.9761) and by the composite implied
by charging every class at the LONG END of its own range (17.3041, agreement to 0.24%).
**The company depreciates at the top of every range it discloses and the identity recovers
that without anybody choosing a point** — which is the reading to try first on the next
name whose per-component figures sit outside their disclosed ranges.

**THE LEVERS THIS RUN APPLIED TO THE DELIVERED STUDY** (`swdy_study/rebuild_ledger.json`,
four levers, three rules, cumulative −5.02%): the disclosed life at full precision
(−0.00%); the strike moved to the latest known price (+1.42%); **terminal flows put on the
LAST EXPLICIT YEAR'S basis (−6.34%)**; and the workbook made to publish the study's answer
(central unmoved, workbook 59.3132 → 52.6969).

**THE ONE TO CARRY FORWARD IS THE THIRD.** `terminal_value.TerminalInputs` takes the last
explicit year's flows and grows them one year itself; this study passed NOPAT, book
depreciation AND the working-capital base all pre-grown by (1+g), so the terminal was
overstated by exactly (1+g) — a year-seven flow discounted at the year-five factor, on a
terminal carrying 84% of enterprise value. The module's own note records six of eight
callers reading the field that way. **And the same construction was re-implemented inline in
three more files of this one study** — the base case, the reverse read and the cost-of-debt
sensitivity — each with its own omissions, and in two of them the errors CANCELLED so their
reproduce-the-base asserts passed. Correcting one made the others visible.

**GUIDANCE LEDGER: the earnings releases carry forward statements and no driver reads
them.** Guidance is scored and never consumed.
