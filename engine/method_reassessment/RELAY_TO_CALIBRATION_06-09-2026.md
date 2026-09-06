# Relay to the calibration chat — 06-09-2026

Written here rather than said in a conversation, per [R-IND-01]: an answer living
only in a chat binds nothing, because the container is rebuilt from the repository.

## What closes criterion 3, in order — and the first item is the blocker

**1. The valuation-input block has to exist per origin.** `bridge_inputs.py`
measured it: across the five names run, not one origin carried a complete bridge
AND a capex figure. Without cash, debt, capex, working capital and a footed share
count at each past origin, a cash-flow lens cannot be built. That is why series (a)
today is a contracted-order-book FLOOR rather than a fair value, and why
`SCORES_contemporaneous_03-09-2026.json` says in its own text that a reading below
the price is the expected case. [R-FCAL-01 AMENDED] binds forward only, so each
name gets its block at its NEXT walk-forward run.

**2. Series (a) is then rebuilt as a real fair value** on those inputs, replacing
the floor.

**3. The panel has to be large enough to carry a bootstrap CI.** It holds four
origins on one name today (PHDC 2016-19), and the scores file says so in terms:
"four origins on one name is not a finding."

**4. Then the score runs**, per Part E criterion 3: pooled contemporaneous bias
CI includes zero, LONO-stable in sign, holds in both eras, beats "FV = price" and
trailing P/E x EPS on MAE, residual attributed to a named lever.

## The knot, raised rather than resolved

Step 3 needs many names. Many names is Phase 2a. The plan holds Phase 2a until
Phase 1's record shows the method unbiased — and Phase 1 cannot reach a credible
interval on five names. As written the two wait on each other.

This is a decision for the principal, not something the calibration can settle on
its own. It is recorded here so it is visible rather than discovered later. Note
that [R-GAP-02] clause three holds ISSUING AND PUBLISHING, not internal work, so
running backtests on further names is not itself blocked by that gate — what is
sequenced is the plan's own Part D ordering.

---

# Correction to item 1 above — 06-09-2026, on the principal's challenge

The principal read the relay and objected, correctly: *"that is strange as we have
IS, BS and CF statements forecasted in all tickers."* The objection stands and the
first framing above was too broad. What follows is measured, not argued —
`python3 engine/valuation_calibration/bridge_inputs.py`.

## Two different artefacts were being conflated

- **The delivered study** forecasts a full three-statement model. That is mandatory
  (Appendix A.1/A.2/A.3, and the Balance Sheet and Cash Flow sheets of the 16-sheet
  workbook). Nothing is missing there.
- **The walk-forward run** is a separate artefact. It commits a panel of FILED
  ACTUALS at each past year, which is what the forecasts are scored against. That
  panel is what is patchy.

So "the balance sheet was never forecast" is WRONG and should not be repeated.
PHDC's own panel carries eighteen balance-sheet lines — cash, banks credit, fixed
assets, receivables, payables, equity, the lot.

## What is actually absent, across 55 name-origin cells

| item | present | direction when absent |
|---|---|---|
| debt | 33 (60%) | overstates equity value |
| depreciation | 23 (42%) | what a declared capex substitution would use |
| PPE | 15 (27%) | makes capex derivable by identity |
| working capital | 15 (27%) | sign depends on growth |
| cash | 14 (25%) | understates equity value |
| share count (footed) | 9 (16%) | no comparison with a price is possible at all |
| **capex** | **0 (0%)** | **overstates equity value** |

Cells with a complete bridge AND a capex figure: **0 of 55**.
Cells where capex is DERIVABLE by identity (ΔPPE + D&A) on top of a complete
bridge: **3 of 55** — TMGH 2020, 2021, 2022.
Cells with a bridge but no route to capex at all: **5 of 55** — PHDC 2015-2019.

**No cash-flow statement was committed at any origin, on any of the five names.**

## The sharpened statement of the blocker

The gap is not a missing FORECAST. It is a missing HISTORICAL record. The studies
model the future correctly; what nobody wrote down is the company's own cash-flow
statement, and in most cells its cash and share count, AS THEY STOOD at 2016, 2017,
2018. A past valuation cannot be rebuilt without them, which is exactly
[R-FCAL-01 AMENDED]'s general lesson: what a process commits decides what can ever
be asked of it later, and nobody notices the missing field until the question
arrives.

Practical consequence for the next runs, unchanged in substance: the valuation-input
block is a COPY out of filings already parsed cell by cell, not new research —
cash, interest-bearing debt, PPE, D&A, the working-capital lines, the share count
footed against its par value, and capex disclosed or labelled as derived.

---

# Where this standard actually sits against a top-tier sell-side desk — 06-09-2026

The principal asked whether the standard being built is high enough to compete
with top-notch investment banks. The answer given, recorded here so the next
session inherits the judgement rather than re-deriving it, and so nothing in the
programme is built on a flattering version of it.

## The split: checkable and uncheckable

**Ahead, on the checkable half.**

- PROVENANCE. Historicals from the company's own filings only (SIGCM clause 1),
  arithmetic as the arbiter rather than the extractor's confidence, OCR off the
  rendered pixels where a text layer lies, the route recorded per figure. Most
  bank models begin at a data vendor.
- ENFORCEMENT FROM OUTSIDE [R-ENF-01]. No self-attested boolean is a check; gates
  run over the work rather than inside it, and FAIL rather than warn.
- IT GRADES ITSELF. The band record [R-CAL-02], the three walk-forwards, and
  criterion 3 mean the house publishes whether it was right before. Sell-side
  almost never scores its own expired targets — and this programme's own scoring
  of an outside house on ARCC found that house's capex forecast wrong by 64%.
- THE ANSWER IS AUDITED, NOT ONLY THE STEPS [R-GAP-01, R-ENF-05]. Eight headings,
  the reverse read, and a sign test on which way every contested judgement went.

**Behind, on the uncheckable half — and this is STRUCTURAL, not a method gap.**

- MANAGEMENT ACCESS. A top desk sits with the CFO, visits sites, runs channel
  checks. No filing carries that, and much of a good analyst's edge lives there.
- SECTOR DEPTH BUILT OVER A DECADE — which kiln is down, who is discounting this
  quarter, what the informal market does.
- PAID INDUSTRY DATA — Argus, Wood Mackenzie, proprietary volume feeds.

## The realistic position, stated plainly

This house can match or beat a top desk on RIGOUR AND HONESTY and will lose to it
on PROPRIETARY INFORMATION. That is a fair trade for a published, calibrated range,
which is a different product from a rating written partly to win banking business.

## The caveat that binds the programme

NONE OF IT IS PROVEN YET. Criterion 3 has not closed, so today the claim is
"carefully built and enforced", not "measurably right". Phase 1 exists to convert
the first into the second, and until it does the standard is an aspiration with
good machinery behind it. No document, deck or page may describe it as more than
that, which is the same discipline [R-FCAL-01] applies to a provisional lesson and
[R-CAL-02] applies to a cautious label: understating in the wrong direction is not
a safe error, and neither is overstating in the comfortable one.

---

# PRIORITY FROM THE PRINCIPAL — 06-09-2026, and the pace that rides with it

Given by the principal after reading the two sections above. Written here so it
survives a container rebuild and binds on a session that starts cold [R-IND-01].

## 1. What moves to the front

Criterion 3 is the only Phase 1 item that is EVIDENCE rather than hygiene, and it
is blocked on one thing: the per-origin valuation-input block. ARCC's landed
overnight (`engine/arcc_walkforward/valuation_inputs.json`, 06-Sep 02:12).
**PHDC, TMGH, EGCH and AMOC have not.**

Measured, not asserted — `python3 engine/valuation_calibration/bridge_inputs.py`:
across 55 name-origin cells, capex is present in 0, cash in 25%, a footed share
count in 16%, and NOT ONE cell carries a complete bridge together with a capex
figure. Until those four blocks exist, series (a) stays a contracted-order-book
FLOOR and no pooled bias can be computed at all.

**So: finish those four before further gate-conformance work on other names.**
They are a COPY out of filings already parsed cell by cell — cash, interest-bearing
debt, PPE, D&A, the working-capital lines, the share count footed against its par
value, capex disclosed or LABELLED as derived. Refuse rather than invent, exactly
as ARCC refused its share count.

## 2. The escape hatch is real and is meant to be used

If taking these four first genuinely damages the LOGIC or the ACCURACY — a
dependency not visible from outside, a shared instrument that must land first, a
correctness reason — **do not force it.** Record the reason in `STATE.json` and
`MORNING.md`, proceed in the order you judge right, and say so at the next question
slot. This is a priority from outside, not a claim to know the sequencing better
than the session doing the work. What is NOT acceptable is silently
deprioritising it.

## 3. The pace — both halves bind

- **WORK CONTINUOUSLY.** Do not end a turn idle with work outstanding, and do not
  treat stopping as the goal.
- **AT MOST 50% OF THE WEEK'S TOKEN BUDGET**, spread across the week. The other 50%
  belongs to the principal and must be there when they want it. Running the week's
  budget down early is a failure of the instruction even when the work is good.
- **NO FLEETS.** Subagents only where the work genuinely needs an OUTSIDE READER —
  a QC audit, a gate-runner confirmation, a census somebody who did not do the work
  should check. Never for throughput, never to consume capacity before it expires.
- **STEADY UNITS.** One coherent piece at a time, committed and pushed as it lands,
  so the work survives any stop.

## 4. When the four are in

Rebuild series (a) as a real cash-flow lens on those inputs, run the pre-registered
score, and report the pooled interval with its LONO stability — WHATEVER IT SAYS.
If five names cannot carry a credible interval, say that plainly rather than
reporting a weak one. [R-VCAL-01]'s guard is symmetric and a finding of bias in
either direction is a successful measurement, not a failure.
