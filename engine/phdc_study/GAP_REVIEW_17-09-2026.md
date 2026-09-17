# PHDC — GAP REVIEW [R-GAP-01]

- AUDITED CENTRAL: **13.9129** (EGP per share)
- AUDITED SPOT: **EGP 14.40**, the supplied close of 3 September 2026 — the latest price this repository holds
- AUDITED GAP: **−3.38%**

**THIS REVIEW IS NOT REQUIRED AND IS WRITTEN ANYWAY.** At −3.38% the central sits well inside
the ten per cent band, so [R-GAP-01] does not fire and [R-GAP-02] does not hold the study on
the gap. It is written because **this rebuild's own audit point said it would be** — declared
before any figure was recomputed and published in the commit that committed the source
extraction: *the sequence stops for an eight-heading review if the cumulative move passes 20
per cent or if the central crosses the traded price.* **Both conditions fired.** An audit
point that binds only when it is convenient is not an audit point.

**AND THE DIRECTION IS THE REASON TO BE CAREFUL.** The rebuild moved the central from
+23.9% above the price to −3.4% below it, which is *toward* the market. A correction that
moves an answer toward the price is the shape of fitting, and it is the shape this house
prohibits outright. What follows is the argument that it is not.

---

## WHY THIS IS NOT FITTING, AND THE EVIDENCE IS THE COMMIT ORDER

1. **Every lever was mandated by a standing rule that predates the move.** The bridge onto
   the latest disclosed balance sheet is [R-BRIDGE-01]; both anchoring levers are
   [R-ANCHOR-01]. Neither was chosen because of where it landed.
2. **The order was fixed and published BEFORE any figure was recomputed.** It is in the
   commit message that committed the 30-June extraction, which is an earlier commit than the
   one carrying any rebuilt number. That is a fact about commit order, not an assurance.
3. **A lever worth ZERO was kept in the ledger.** The gross-margin anchor moved the answer by
   nothing at four decimal places, and dropping it would have made the other two explain more
   of the move than they do.
4. **The largest lever replaced a three-year MEAN with a reviewed actual**, and its direction
   is measured like for like in the company's own period pair — the same half a year earlier,
   from the same statement's own prior-year column, 3.114% against 7.676%.
5. **Nothing was tuned.** No rate was solved, no weight was chosen, no discount was applied.

---

## 1 · LATEST FILINGS

**The trigger for this whole rebuild.** The reviewed consolidated statements at 30 June 2026,
with a limited review report from Mostafa Shawki / Forvis Mazars, are now read and consumed —
balance sheet, income statement and cash flow, all three footed. The information set moves
from 1Q2026 to **2Q2026**. Read by OCR off the rendered pixels; the extraction carries eleven
footing assertions and refuses if any fails.

**What is still not held: the 1H2026 EARNINGS RELEASE**, which is a different document from
the statements. It is where operating KPIs live. Recorded as a dated negative search with its
mechanism in `EXTERNAL_NEWS_17-09-2026.md`.

## 2 · BASE YEAR

FY2025 audited remains the projection's base year: a working-capital cycle measured on full
years is not restarted from a half. What moved is the **anchor**, not the base — the margin
and the conversion rate now sit on the reviewed half. Nothing is annualised: the conversion
rate is a ratio of two figures from the same six months, compared against the same six months
a year earlier.

## 3 · MACRO COHERENCE

Untouched by this rebuild and inherited from the house path [R-MACRO-01]. Inflation, the
currency and the discount-rate glide are one path; this study carries no inflation number of
its own. The levers here are company figures, not macro ones.

## 4 · DISCOUNT RATE

Untouched. The cost-of-capital schedule is unchanged — beta 1.0493 against EGX30, explicit
WACC 25.11% gliding to a terminal 16.15%, both ERP bases published, the sovereign counted
once. **Cash is charged exactly once**: it sits inside net debt, which is deducted once, and
the weights stand on gross debt. The company is net *debt*, so the net-cash pathology cannot
arise. The bridge lever moved the net debt figure, not the rate.

## 5 · TERMINAL

Unchanged in construction. The terminal is 30.8% of enterprise value, down from 31.2%, purely
because the explicit window's cash flows fell. Terminal growth remains the house terminal
inflation plus a stated real rate.

## 6 · BALANCE SHEET

**This is the lever.** The bridge stood on 31 March 2026 and now stands on the reviewed
30 June 2026 sheet. Net debt 23,244.7 → **27,471.2**, associates 3,838.7 → 3,898.5,
investment property 1,020.5 → 1,008.4, minority book 1,432.7 → 1,723.0. Every subtotal on
that sheet foots: assets equal liabilities plus equity exactly, current assets exactly,
current and non-current liabilities exactly, parent plus minority exactly.

**Two lines are recorded as NOT READ** rather than estimated — advance payments for
investments acquisition, and the deferred tax asset — and one, suppliers and contractors, is
**recovered from the statement's own subtotal and labelled as recovered**, because a figure
recovered by difference is not a figure read.

## 7 · CLAIMS AGAINST THE RECORD

The two claims this rebuild introduces are both recomputed rather than typed:

- **"The base no longer sits above both of the two most recent years."** The old base of
  8.714% was above FY2025's 3.938% and below FY2024's 17.870%; the new 7.676% is still
  between them. The claim as stated is about the *mean*, and it is true: a mean of three
  years was standing in for a reported rate.
- **"Half against half."** 1H2025 converted at 3.114% and 1H2026 at 7.676%, both from the
  same reviewed statement's own two columns.

The external-reader scrub is clean on both documents and the prose-figure check matches 225
figures with none unmatched.

## 8 · MULTIPLE CROSS-CHECK

The central implies a cash conversion of 7.676% against a **market-implied 7.875%** — the
rate the traded price pays for under this study's own drivers, solved and published in
`diagnostics.json` and reaching no builder's arithmetic. **Those two are now within twenty
basis points of each other**, which is the honest reading of a −3.4% gap: the price and the
company's own reviewed half agree about roughly the same conversion rate, and this study no
longer disagrees with the market about the thing its answer turns on.

---

## VERDICT

The answer is audited and stands at **13.9129 against 14.40, −3.38%**. The move is large, it
runs toward the price, and every lever behind it was required by a rule written before the
move and applied in an order published before the first figure was recomputed.

**What would overturn it:** the 1H2026 earnings release showing operating KPIs inconsistent
with the statements; a full-year 2026 conversion rate that lands back near the three-year
mean, which would say the reviewed half was seasonal after all; or a restatement of the
30 June balance sheet.
