# THE SEVEN FORENSIC AUDITS, CONSOLIDATED — WHAT IS FIXED ONCE AND WHAT IS FIXED SEVEN TIMES

**18 September 2026.** Seven independent forensic audits, one per name, each rebuilding the
delivered workbook from its own inputs before reading the study's answers.

| Name | Raised | Answered | Accept | Accept-defect-reject-fix | Unproven | Reject |
|---|---|---|---|---|---|---|
| ARCC | 45 | 45 | 32 | 4 | 9 | 0 |
| EGCH | 25 | 25 | 15 | 1 | 9 | 0 |
| ELEC | 35 | 35 | 33 | 0 | 2 | 0 |
| PHAR | 27 | 27 | 25 | 0 | 2 | 0 |
| SCEM | 44 | 44 | 38 | 0 | 3 | 0 |
| AMOC | 34 | 34 | 32 | 0 | 2 | 0 (1 remedy) |
| TMGH | 82 | 82 | 79 | 0 | 2 | 0 (1 conclusion) |
| **Total** | **292** | **292** | **254** | **5** | **29** | **0 findings** |

**Two hundred and ninety-two findings and not one rejected outright.** Two remedies and one
conclusion are declined, each with a receipt from a standing rule; every underlying defect is
accepted.

---

## PART A — THE EIGHT THINGS THAT ARE FIXED ONCE

A defect present in several studies is fixed in the shared place or not at all. Porting one
study's fix into six others produces six hand-maintained variants with six different holes —
which is this book's own repeated lesson, and it is why this list comes before the per-name
work.

### A1 — The beta is a Dimson estimate and the page says it is a simple regression
**Found on:** TMGH (18). **Binds:** all ten studies with a committed beta record.

`beta_regression.own_stock_beta()` regresses against lead, contemporaneous and lag market
returns, sums three coefficients for β and takes the square root of the summed 3×3 covariance
block for the standard error. Ten of ten committed records carry `dimson: true`. **Five
delivered documents say so; the rest describe a simple regression against an index.**

A reader applying the textbook one-regressor identity `t² = R²(n−2)/(1−R²)` to TMGH's four
published diagnostics concludes they cannot come from one regression. They cannot — and they
are correct. **The estimator is sound; the disclosure is not.**

**Fix:** one sentence, emitted from the beta record rather than typed, wherever a beta is
quoted. Not a model change; no number moves.

### A2 — A price held flat in nominal dollars is a real-terms decline forecast
**Found on:** AMOC (1), independently and priced to four decimals of our own figure.
**Binds:** ADNOCDRILL, AMOC, EGCH, GBCO. Measured in
`FLAT_NOMINAL_PRICE_WEDGE_18-09-2026.md`.

On AMOC, closing it is **+17.84%, EGP 11.4012 → 13.4350**, re-run through the study's own
`compute.py`. Three other studies carry the same convention.

### A3 — The retired terminal identity is still running
**Found on:** AMOC (20, C.4), which derived the implied replacement cycle as **1/g = 14.3
years** with no access to the rule that retired it, and matched our own ratchet entry's figure
to one decimal. **Binds:** every study on `terminal_outstanding`.

### A4 — The promotion guard is being used to defer corrections
**Found on:** AMOC, in the study's own words. **Binds:** the whole book.

`[R-VCAL-01]`'s one-lever-at-a-time guard governs **levers promoted from the valuation
calibration** — candidates seeking evidence. It does not govern **corrections to defects**, and
`[R-REBUILD-01]` says so in terms: *a study wrong in six ways moves a long way when all six are
fixed, and a cutoff would be a free parameter; what is forbidden is the move being invisible.*

AMOC's own forecast-anchor record invokes the guard to hold a correction priced at +55%. Four
undisputed corrections stack there to **EGP 14.8165 — 9.8% above the traded price.** This needs
a rule clarification, not a study edit.

### A5 — `erp_terminal` in the house macro path names no institution and no date
**Found on:** TMGH (17), worth **≥EGP 10.72 a share** there. **Binds:** every Egyptian study.

`engine/macro_paths/EG.json` carries `erp_terminal: 0.07` sourced to *"normalised below the
currently elevated crisis-era level toward the rating-class norm."* `[R-MACRO-01]` requires
every level to be **published by a named institution on a named date, or DERIVED by an identity
from numbers that are.** This is neither. A terminal ERP of 7.00% against a year-1 rating ERP of
13.94% retires 9.71 points of Egypt country risk, and the path does not say on whose authority.

### A6 — The workbook-recalculation gate reads a two-name allowlist
**Found on:** AMOC self-audit. **Binds:** the gate.

`scripts/check_workbook_values.py` carries `SCRIPTS = ('recalc.py', 'lo_recalc_gate.py')`.
AMOC's live recalculator is a third name; it is the only study in 23 with a third name; and it
is the one the ratchet records as **failing** a check that in fact passes 6,069 formula cells
with zero disagreements. **The debt is recorded against a file, not against the work.**

*The fix belongs to the study, not the gate: AMOC's `recalc.py` stub delegates to `recalc_v5.py`
instead of refusing. Editing a gate so that a study goes green is what `[R-REPAIR-01]` forbids,
and the distinction is worth keeping even though the gate is the thing that is wrong.*

### A7 — A source claim in a delivered bibliography is read by no gate
**Found on:** AMOC (24). **Binds:** the enforcement set.

`check_source_integrity.py` reads the committed **input register**, where AMOC's sources all
name filings — and it passes. The aggregator citation (*stockanalysis.com; Investing.com;
TradingView* for total assets, total liabilities, cash and total debt) is in the
**bibliography's sources table**, which that gate does not read.

### A8 — A declared absence is asserted without the last search being run
**Found on:** TMGH (1, 2, 3, 4) — **four declared gaps, all four disclosed**, two of them in a
single filing the register already lists as primary. **Binds:** SIGCM clause 8 everywhere.

The clause exists to make an absence visible. Nothing checks that the absence is real. That is
`[R-IND-01]`'s lesson — *where a question can be answered by a command available in the room,
asking it is the cost of not having run the command* — arriving inside a study instead of
inside a session. TMG's investor-relations archive answered on the first request.

---

## PART B — THE PER-NAME WORK

### The four largest single items in the book, all verified

| Name | Item | Worth |
|---|---|---|
| TMGH | Work-in-progress cover at 4.0 years against an actual 5.57 | **−25% / −64%** |
| AMOC | The base anchor on the latest reviewed half (the study's own committed figure) | **+54.5%** |
| TMGH | The sales escalator through the advances line | **+32%** |
| TMGH | The minority basis | **−31%** |

### The direction, which is the finding behind the findings

Three of the four mechanisms measured today understate value — the flat-nominal price
convention, the retired terminal identity, and the promotion guard used to defer corrections.
**TMGH's run the other way**: a compounding sales annuity the model never delivers, a
working-capital harvest worth 110% of terminal free cash flow, and two typed segment growth
rates the study says it does not use.

**A house that had only ever measured one direction would have called TMGH conservative too.**
That is `[R-TERM-01 CLAUSE TWO]`'s own lesson — *a defect measured only where it hurts looks
like a bias with a direction* — and it is the reason this consolidation is worth more than seven
separate fixes.

---

## PART C — WHAT THE SEVEN AUDITS AGREE ON, WHICH IS THE PART TO KEEP

Every one of the seven reports the arithmetic sound. AMOC's says *"the most cleanly reproducing
model one could hope to audit"*; TMGH's says *"almost nothing here is an arithmetic mistake. The
model computes what it says it computes. What it says it computes is, repeatedly, not what it
does."*

**That sentence is the whole result.** 254 accepted findings, and the overwhelming majority are
Construction and Disclosure rather than Input and Logic. The gates in this repository check how
a number was built and whether it reconciles. They do not check whether the page describes the
model that produced it — and on seven studies audited by three different outside readers, that
is where almost everything was found.
