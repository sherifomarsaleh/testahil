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
