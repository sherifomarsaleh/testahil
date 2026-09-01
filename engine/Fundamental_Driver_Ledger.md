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

### Pre-registered predictions this run will test when it is unblocked

Recorded here so they cannot be quietly dropped: **L-101** (a developer's volume is set by
its launch calendar and no demographic anchor can see it) is run as the primary D1 rule
rather than replaced by one, so its failure or success against *freeze* is a result rather
than an assumption; and **L-114** (new-sales value is under-forecast when price and volume
are projected separately) is computed both ways at every origin, with both reported and
neither selected on its score.
