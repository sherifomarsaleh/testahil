# PHAR — gap review, 7 September 2026

Written because the fundamental walk-forward [R-FCAL-01] ran on this name today and
produced evidence that bears directly on the discount. The review of 4 September stands
as it was written and is not rewritten; this one carries what that one could not know.

A two-sided answer, so BOTH branches are audited; there is no single central and
averaging them would state a number neither branch supports.

**AUDITED CENTRAL: 36.6395** — Frame A, provision charge permanent at 5.25% of revenue
**AUDITED CENTRAL: 54.2420** — Frame B, provision charge normalising to 2.5% of revenue
**Audited spot:** EGP 127.30, the Egyptian Exchange close of 3 September 2026, the latest
price supplied to this repository (`engine/prices/SUPPLIED_07-09-2026.json`)
**AUDITED GAP: -71.2%** (Frame A) · Frame B −57.4%

Neither branch moved today. The walk-forward adopted no correction, so this review audits
the same two numbers the 4 September review audited, against the same price, with new
evidence about the method that produced them.

Both branches breach the trigger. The study remains **HELD** under [R-GAP-02] and no
market dissent is filed, because the honest conclusion is still that the gap is not
explained.

---

## The new evidence, before the eight headings

**The forecasting method was tested on this company's own history today and it
under-forecasts SCALE, systematically, at every horizon.** Five origins, FY2020 to
FY2024, horizons one to three, 150 scored cells, every figure out of EIPICO's own annual
reports:

| driver | bias (log) | 90% interval | what it means |
|---|---:|---|---|
| revenue | **−0.310** | −0.374 to −0.179 | the outturn came in about 36% above the projection |
| cost of sales | −0.294 | −0.355 to −0.182 | almost the same amount |
| gross profit | −0.331 | −0.407 to −0.186 | so the MARGIN is roughly right |
| net profit | −0.553 | −0.738 to −0.364 | and the profit is out by more than the revenue |

**The bias compounds with the horizon** — −0.157 at one year, −0.387 at two, −0.693 at
three — which is the signature of a RATE error rather than a base-year error, and it is
this house's own pooled census arriving on this name's own history rather than being
carried to it.

**Taken apart, the whole of the revenue miss is PRICE and none of it is VOLUME.** The
error decomposes exactly, by identity: mean revenue error −0.303 = volume **+0.044** +
price **−0.352** + a consolidation residual of +0.004. The method forecasts how many
packs EIPICO makes to within four and a half per cent over three years and misses what
each pack sells for by more than a third.

**And most of the price miss is MACRO, not company.** Re-running every origin on the
realised inflation path takes the price bias from −0.352 to −0.111 — a **68.3% macro
share** — and the revenue bias from −0.310 to −0.130. The volume driver, which carries no
inflation term in any leg, returns a macro share of **exactly zero**, which is the
split's own pre-registered check passing.

**Why this belongs in a gap review.** The one number in this valuation with the largest
committed uncertainty is the currency path, and the second is the domestic price ladder;
both are inflation-class inputs, both come from the house macro path, and the measurement
above says that on this company's own history the house-style escalation has been the
dominant source of a one-directional under-forecast of scale. A −71% discount is exactly
the output shape that error produces. **That is not a licence to multiply the answer** —
no correction passed its own test today and none was adopted — but it is the strongest
statement yet of WHERE this study's remaining error most likely is, and it agrees with
what the 4 September review already put first.

---

## 1. LATEST FILINGS — **still NOT cleared, and the routes were re-run today**

Every route was executed again rather than carried from the September log [R-IND-01]:

| route | outcome, 7 September 2026 |
|---|---|
| `eipico.com.eg` → Investor Relations → Annual Reports | **REACHABLE.** Seven annual reports listed, FY2019–FY2025, and **all seven retrieved today** — the first time this study has held the pre-2022 filings |
| `eipico.com.eg` → News and Media → Press Releases | reachable and carries **no financial documents at all**; no interim statements, no results releases |
| Egyptian Exchange `egx.com.eg/en/DisclosureNews.aspx` | **does not resolve** |
| Regulator `disclosure.efsa.gov.eg` | **does not resolve** |

The most recent period the model consumes is still **Q1-2026, reviewed**. A half-year to
30 June 2026 would ordinarily exist and **the company publishes no interim statement on
its own site in any year** — the investor-relations page carries annual reports and
nothing else — so this is a property of EIPICO's own disclosure rather than a document
this desk failed to open. It remains true that if an H1-2026 was lodged with the exchange,
the bridge stands on a superseded balance sheet. **NOT cleared, and it cannot be cleared
from here.**

What today's retrieval DID close: the pre-2022 archive. Seven fiscal years of audited
consolidated accounts, FY2019–FY2025, now sit behind this name where three did.

## 2. BASE YEAR — **cleared**

FY2025 audited: revenue EGP 9,441,379,305, profit for the year EGP 1,457,893,015 —
**both re-read today out of the 2025 annual report's own consolidated statements and
footed against that statement's own subtotals**, independently of the figures the study
already held, and both agree to the pound. Nothing in the base year is annualised, scaled
or solved.

**Six printed cells across these filings do not foot and every one was settled by the
statement's own arithmetic, none of them in the base year.** The largest is the FY2022
printed gross profit, EGP 18.0mn below both revenue-less-cost-of-sales and what the
statement's own chain to profit before tax requires — **and the same defective figure is
carried forward into the FY2023 comparative column**, so a reader checking one filing
against the next sees agreement and still holds the wrong number. They are listed in
`engine/phar_walkforward/panel.py:FOOTING_FAILURES`. None touches FY2025.

## 3. MACRO COHERENCE — **cleared for the study; A DEFECT FOUND IN THE ESCALATION, AND IT IS NOT THIS STUDY'S**

The study carries no inflation rate of its own: `esc_domestic_cpi` is the house calendar
ladder 16.0 / 12.0 / 9.0 / 7.5 / 7.0 to the basis point, terminal growth is stored as zero
real and derived, and the currency is derived by relative purchasing-power parity on that
same ladder. One economy, one path. **Cleared.**

**The registered tension of 4 September was about the wrong field, and this review says
so.** That review recorded — and [R-MACRO-01 AMENDED 06-09-2026] then adopted a rule on —
the fact that the house EG path's `fx.spot` anchor is dated 6 August 2026 while this study
was struck on 3 September, 28 days later and past the 14-day bound. PHAR sits on that
gate's ratchet with its −25.4% attached, described there as "worth −25.4% on PHAR by its
own rebuild ledger, the largest lever in it".

**Measured today: this study's currency path does not read `fx.spot`.**
`macro_path.fx_path()` defaults its base to `fx.average_2025` = 48.70, a completed annual
average dated 31 December 2025; `compute.py` binds `_FX_SPOT` at line 61 and **the name
occurs exactly once in the file**. The committed path [55.1141, 60.2223, 64.0413, 67.1652,
70.1139] reproduces from `fx_path(5)` with that default base, and `fx_path(5, base=50.25)`
— the spot-anchored construction the study's own `fx_path_note` describes — returns
**56.8683**, which is precisely the "56.87" that note quotes. **The note describes the
path the study REJECTED, not the one it committed.**

Three consequences, none of which moves a number today:

1. **Refreshing the EG path's `fx.spot` would change the gate's verdict on PHAR and would
   not change PHAR's fair value by a basis point.** The debt is real; it is filed against
   a field this study does not consume. That is [R-MACRO-01 AMENDED]'s own lesson —
   *a check that reads what a process declares is not checking what the process does* —
   arriving on the enforcement side rather than the study side.
2. **The study's `fx_path_note` states a figure that is not its committed path's first
   year** (56.87 against 55.1141) and a mechanism the model does not perform (compounding
   onto an August quote rather than onto the 2025 annual average). It is a number typed
   into a note rather than computed from the model, on the very field the largest lever in
   this rebuild rests on. **Registered for correction; not corrected in passing, because
   rewriting a committed record mid-run is how a route stops being walkable.**
3. **The substantive question is unchanged and is the house path's**: is a calendar-2026
   average of EGP 55.11 to the dollar coherent with a pound at 50.25 in early August 2026?
   It requires roughly 58–60 by December. Answering it needs a current quote this
   environment holds no route to, and the path is shared by four Egyptian studies in
   flight. **Escalated for the pass that owns the path; not answered here, and not
   answered by inventing an anchor.**

## 4. DISCOUNT RATE — **cleared**

The terminal risk-free rate is DERIVED at 12.5% — terminal inflation 7.0% plus the
5.5-point real convention — so it cannot disagree with the inflation the rest of the model
uses. Operations are discounted once, on a glide whose fractions are the cost-of-debt
path's own cumulative progress: 22.71% / 20.65% / 18.40% / 16.53% / 15.03%.

**Cost of debt, re-derived independently today from the walk-forward panel, and the three
figures in play are NOT the same quantity — which is the point.** Over average
INTEREST-BEARING debt only (long-term loans, long-term credit facilities, short-term loans
and creditor banks, and nothing else) the FINANCE-COST rate runs 9.59% (FY2021), 9.67%,
10.56%, 13.65%, **14.83% (FY2025)**. The study computes **14.17%** on the same denominator
because it divides INTEREST ON CREDIT FACILITIES of EGP 1,275.3mn rather than the income
statement's finance costs of 1,332.9mn, which carry 57.6mn of bank commissions — an
interest RATE is computed on interest, and the study is right to make that distinction.
Its all-in reading, adding the EGP 551.1mn of interest capitalised into construction, is
**20.30%**, and the adopted marginal local cost of debt is **24.81%**, above the 23.00%
sovereign as [R-COC-01] requires. **A trailing effective rate is not the comparator for a
marginal one on this book**: capitalised interest alone is 43% of the expensed charge, and
that is a named mechanism the cost-of-capital rule already admits.

**Trap (i) of [R-FCAL-01], tested rather than asserted**: dividing the same finance charge
by TOTAL liabilities gives 11.87% for FY2025 against 14.83% on the borrowings that
actually bear it — 296 basis points understated, on a book where trade payables, other
creditors, provisions and tax payable are a quarter of total liabilities. The trap bites
less hard here than on a name carrying customer deposits, and it still moves the rate by
nearly three points.

## 5. TERMINAL — **cleared, and the disclosed life re-confirmed on a second filing**

Built through the sanctioned construction on a disclosed weighted useful life of **13.7954
years**. That life is derived from EIPICO's own FY2024 note 3.1 lives weighted by note
4.1's gross cost; today the **FY2025 annual report's own accounting-policy note was read
and carries the identical table** — administration and factory buildings 50, production
and service machines 15, transport and tools 5, office furniture and equipment 10, land
not depreciated. **No life was reassessed between FY2024 and FY2025**, which is the
falsifier `useful_lives.json` names, tested and not triggered.

Terminal growth is stored as zero real and the nominal 7.0% derived from the house
terminal inflation.

**One thing the walk-forward found that bears on the terminal and is reported rather than
acted on**: the mechanical depreciation roll-forward is the ONE driver this method
OVER-forecasts, bias **+0.499**, and it is worse than freezing last year's charge by a
wide margin. The reason is specific to this company and is visible in its own accounts —
capital expenditure lands in projects under construction and stays there for years before
it enters the depreciable base, EGP 866mn at FY2022 becoming EGP 5,694mn at FY2024 — so a
roll-forward that depreciates spend on arrival charges depreciation the company has not
yet begun to charge. The delivered study does not make that error (it carries the
construction balance separately and charges the terminal for the depreciation the forecast
never charged), and the finding is recorded because a future rebuild could easily make it.

## 6. BALANCE SHEET — **conditionally cleared, unchanged**

The bridge stands on the FY2025 audited balance sheet, which is the latest EIPICO
publishes. Subject to heading 1: if an H1-2026 exists behind the exchange portal, this
sheet is superseded. Total assets EGP 18,272,906,249 and total equity EGP 6,531,836,087 at
31 December 2025, **re-read today and footed** — the sheet balances to the pound.

## 7. CLAIMS AGAINST THE RECORD — **cleared, and one claim strengthened by being tested**

The study's re-rating claim is recomputed rather than repeated: at EGP 127.30 the shares
trade on **14.90×** trailing attributable earnings on the 168,755,750 shares in issue
(EGP 1,441,657,700 attributable, EPS 8.5429), or 14.3× on the audited weighted average,
against a four-year own-history mean of 6.6× computed from year-end closes over audited
profit.

The study's claim that its volume build rests on the company's own disclosed packs was
tested today rather than accepted: the packs series is disclosed in every annual report
except the condensed FY2020 edition, and **the FY2024 figure was re-presented from
306,133 to 299,608 thousand packs between the FY2024 and FY2025 reports** — a 2.1% KPI
redefinition with no reconciliation given. Recorded; it does not move a forecast year.

## 8. MULTIPLE CROSS-CHECK — **STILL NOT CLEARED, and today's evidence sharpens it**

Frame A at EGP 36.64 implies **4.29×** trailing FY2025 attributable earnings. Frame B at
54.24 implies **6.35×** — almost exactly this company's own four-year mean of 6.6×. The
market pays 14.90×.

**A generic manufacturer with a third of its revenue in hard currency, a newly licensed
biosimilars plant and no distress on its balance sheet does not trade at four times
earnings unless the model is asserting something the market is not.** Frame B lands where
this company's own history says it should; Frame A lands below every year of it.

**And the walk-forward now says which direction the method's own error runs on this
name.** Its far-year bands, declared as SPANS over three to five observations rather than
percentiles because that is all this record supports, and oriented actual-over-forecast:

| | h1 (n=5) | h2 (n=4) | h3 (n=3) |
|---|---|---|---|
| revenue | 0.95 – 1.25 | 1.21 – 1.72 | **1.73 – 2.02** |
| net profit | 1.10 – 2.44 | 1.35 – 2.57 | **1.72 – 3.41** |

At three years the outturn exceeded the mechanical projection in **every one of three
cases** on both lines. That is a small sample and it is not a correction — every candidate
was DECLINED today, six of seven because a LIGHT run cannot admit a single cut and
untestable is never stable — but it is a measurement, it runs one way, and it runs in the
direction the discount would need.

---

## What this review concludes

**The gap is not explained and the answer does not move.** No number was adjusted toward
the price; a fair value adjusted to meet a quote is the reverse-engineered construction
this method prohibits outright.

**Where the remaining error most likely is, re-ordered on today's evidence:**

1. **The price escalation, and therefore the currency and the domestic ladder.** The
   walk-forward measures the whole of this method's revenue miss on this company as a
   PRICE miss — volume is right to 4.5% over three years — and 68% of that price miss as
   MACRO. Both of the study's price-side inputs come from the house macro path. This was
   third on the 4 September list and the measurement puts it first.
2. **The house EG path's first currency year**, which heading 3 shows is a question about
   `fx.average_2025` compounding rather than about the stale `fx.spot` the ratchet records,
   and which needs a quote this environment cannot source.
3. **The biosimilars plant carries every cost and no revenue.** Unchanged and still the
   right treatment of an undisclosed quantity, and still one-sided. The reverse read is
   published in the study and is testable against the first year the company discloses
   biosimilar revenue.
4. **The terminal rate charges Egyptian country risk on dollar-linked earnings.** A live
   method question across this book, registered, not resolved by moving one study's rate.

The study is HELD. The corrections stand. Nothing here licenses a publish.
