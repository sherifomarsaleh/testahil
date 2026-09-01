# PROMPT — FUNDAMENTAL WALK-FORWARD TRAINING (run with every new study or update)

**Standing rules: [R-FCAL-01] (this exercise) and [R-LESSON-01] (its second document).**

Ticker: {TICKER} · Exchange: {EXCHANGE} · Market code: {MARKET} · Update date: {DATE}

Train the fundamental method on this company's own history and carry the result into the update.

**TWO DIFFERENT TESTS ARE BOTH CALLED A WALK-FORWARD. THIS IS ONE OF THEM.** The FUNDAMENTAL walk-forward, below, tests the forecasting method: drivers projected from a past origin, scored against what the company actually reported. The PRICE-ENGINE walk-forward (`{ticker}_study/backtest_5y.py`, `backtest_rows.csv`) tests the probability cone: band coverage and a proper score against a naive rule. They test different machinery on different evidence and neither substitutes for the other. Say which one you mean, every time — conflating them once already understated the evidence base badly.

The worked pattern is the PHDC run of 30-Aug-2026 (`engine/phdc_walkforward/`: `panel.py`, `bottom_up.py`, `score.py`, `diagnose.py`, `corrections.py`, `forward.py`, and `TRAINING_RECORD_30-08-2026.md`) — replicate its structure, never its numbers. An earlier du reference run is named in previous editions of this prompt (`du_panel.py`, `du_IS_projected_vs_actual_all_origins.md`); those files are not in this repository, so locate them before relying on them and do not assume their contents.

**What is internal and what is delivered.** The training record, the panel, the error tables and the pre-registration are INTERNAL and are never shown to a reader. The two documents required by §6 ARE the deliverables. Nothing reaches the live site without a separate, explicit publish request.

## 0. Scope decision — decide this first and state it

- **Full run** when the archive supports at least 8 sourceable fiscal years under §1: all origins from the first year with a five-year history, horizons 1–5.
- **Light run** when it supports 5–7 years: the last five origins only, horizons 1–3, same rules otherwise.
- **Skip** when fewer than 5 years can be sourced under §1: record "walk-forward not run — insufficient sourceable history (N years)" in the study's register and QC table, and move on.
- **Never delay a first delivery for it.** For a NEW study, run the training alongside the build; its corrections feed the next edition, and the first edition carries a one-line note that the training is pending or running. For an UPDATE of a covered name, the training is a standing step of the update.
- **Incremental thereafter.** After the first run, each update adds one origin (the new fiscal year), grades the forecasts that have matured, and re-tests the corrections — the full 15-year rebuild is done once per name, not every time.
- **Two purposes, not three.** The training exists for per-driver bias detection and for calibrated ranges on years 3–5. A better point estimate is a by-product, never the aim; do not tune toward one. (Distinct from the two DOCUMENTS of §6, which are what the run produces.)

## 1. Data — no hallucination, graded provenance

- Target 15 complete fiscal years of income statement, balance sheet, cash flow and operating KPIs (units, prices, cost per unit, capex, headcount where disclosed), plus every quarter already disclosed for the current year. If 15 are not available, use every year that is, and state the span you actually obtained and why it stops where it stops.
- **The most recent 3 fiscal years and all current-year quarters MUST come from the company's audited financial statements or its own website/investor-relations documents.** No exception: if they cannot be obtained, STOP and ask for the documents.
- Years older than the last three may come from any credible source that supports a DCF (exchange disclosure archive, regulator filings, annual reports held on third-party archives, a reputable data provider), with the company's own documents preferred wherever they exist.
- Every number carries four fields — value, source document or URL, document date, provenance tier (A = audited/company, B = exchange or regulator filing, C = credible third party). A number with no source does not enter the panel. If a year cannot be sourced, leave it out and shorten the window; never estimate, interpolate or infer a figure to fill a gap. Anything derived (a ratio, a chained series, a sum) is marked DERIVED with its formula. Anything provisional is marked as such and listed in the caveats.
- **Accept a statement only if it foots against its own arithmetic.** Fonts with a broken character map extract figures that look clean and are wrong — one filing renders revenue of 3,560,584,644 and its text layer yields 1,654,670,500. Re-read any page that does not foot from the rendered pixels, and record which route each figure came by.
- Build a basis-break register before modelling: accounting-standard changes (IFRS 15/16/17/18), segment re-cuts, KPI redefinitions, currency or FX-regime changes, one-offs the company itself attributed (M&A, disposals, regulatory cleanups, pandemic). For each break state the overlap year, the chain factor and the treatment. Score unit drivers only inside their own definition window.
- Point-in-time discipline: each origin sees only what had been published by that date, as originally reported; note where later restatements differ.
- Log every source attempt, including failures, in the Sweep Register.

## 2. Pre-register before computing a single error

State in writing, before any result: origins (annual, from the first year with a five-year history to the current year); horizons 1–5 years; the driver list by class (units, price, cost per unit, overheads, D&A, regulated/tax lines, capex, working capital); the mechanical rule for each driver with its parameters (test the method, not the analyst — no judgement drivers at historical origins); the naive benchmarks (freeze = every line flat at last actual; trend = trailing 3-year CAGR); the score (log error per driver per horizon); the block bootstrap over origins; the macro/regulatory conditioning (which inputs are exogenous — inflation, FX, population, rates, the tax or royalty regime — and how the error is split into macro vs company); and the roles of the samples (the rolling record estimates corrections, the non-overlapping origins confirm them). Parameters are stated, never fitted; sensitivities are reported, never selected.

**Before writing the pre-registration, read what already binds on this name and class:** `python3 engine/lessons.py {TICKER} --class {CLASS}`. Lessons marked PROVISIONAL are recorded findings from an unvalidated method — read them, do not treat them as rules.

## 3. Build bottom-up at every origin

Units × price by segment from the finest disclosed level; cost per unit; overheads as a fixed component escalated with inflation plus a variable component per unit; D&A from a PP&E roll-forward; interest from the debt schedule; tax and any royalty by formula under the regime known at that origin; capex from the disclosed programme and guidance, treated as an input that drives volume and D&A; working capital from the disclosed cycle (DSO/DIO/DPO) → IS, BS and CF. Volume anchored on an exogenous market driver from the Country/Industry rings dated at the origin (population × penetration × share, system credit × share, activity × share as the class dictates), never on the company's own trend alone. Price anchored on the market's inflation and FX where they are not negligible.

**Interest comes from the borrowings that actually bear it**, never from a broader liabilities total. Customer deposits, supplier balances and cheques under collection pay no interest; dividing by them understates the borrowing rate by a multiple and produces a bias that is arithmetic, not evidence.

**Revenue and cost must sit on the same recognition clock.** Where revenue is recognised as work completes, cost must be too. The two on different clocks makes every year look more profitable than it was, and no correction factor should be allowed to hide it.

## 4. Score and diagnose

Per driver and per horizon: bias, MAE, block-bootstrap CI, share of origins over- and under-forecast, sign by era. Decompose the revenue and net-profit errors into their drivers. Split each miss into macro/regulatory versus company. Identify every one-off in the history and show what the record looks like with it classified. Show the projected-versus-actual income statement side by side for every origin. Report skill against freeze and trend at every horizon.

**A bias that changes sign between eras is not a bias.** Report it as instability and do not correct for it.

## 5. Learn, adjust, test

Expanding window only (errors resolved before the origin). Corrections per driver, at half strength by default. Apply a correction only where the bias holds its sign across eras; reset it after a structural break (a driver error beyond its own two-sigma). Rebuild the aggregates from adjusted drivers and test adjusted against raw on the origins that had a correction; report by origin. Keep a guidance ledger: management's own guidance versus outcome, and its bias. A correction enters the current update's drivers only if it passed here **and** is consistent with the same driver class across the market's book; otherwise it is recorded as a watch flag.

**That second clause is not a formality.** A correction that works on one name and does not match how the driver is built everywhere else is usually correcting our own mis-specification, and adopting it would hide the defect rather than fix it. When the two tests disagree, find the wiring error before reaching for a multiplier.

## 6. Deliver — TWO DOCUMENTS, EVERY RUN

Every walk-forward run ends by producing both of the following. A run that produces one and not the other is not finished.

### Document 1 — the updated fundamental analysis, at full model-report depth

The delivered valuation study, rebuilt to carry this run's results. **The depth standard is the PHDC study of 30-Aug-2026** (`engine/phdc_study/`), which was itself built to the model report and passes `assert_model_study()`. Match it exactly:

- **16-section Word document**, in this order: Masthead + READ FIRST · Headline · Valuation summary · Company overview · §1 Fundamental valuation (1.1 cash-flow model with the full FCFF waterfall and the EV→equity bridge; 1.2 book value and sustainable return; 1.3 relative multiples; 1.4 normalised earnings power; 1.5 synthesis; 1.6 drivers — each disclosed segment on its own driver, margins as OUTPUTS; 1.7 the crux; 1.8 macro and cost of capital; 1.9 sensitivity) · §2 Technical and price structure · §3 Probabilistic price map · §4 Comparison of the lenses · §5 Catalysts · §6 Reading the probability zones · §7 Caveats and what would change our mind · Appendix A financial statements (A.1 income statement, 3 years reported + 5 forecast; A.2 balance sheet as reported; A.3 the FULL projected balance sheet and cash flow) · Appendix B peers, risk register, research register · Appendix C expert panel (C.1–C.3 by method, C.4 cross-examination, C.5 the three in one room, C.6 divergence table) · About · Disclosure.
- **16-sheet workbook**, same order: READ FIRST, Summary, Fundamental Valuation, Assumptions, SOTP Bridge, Segments, Relative & Normalized, DCF, Income Statement, Balance Sheet, Cash Flow, Summary Financials, Monte Carlo, Sensitivity, Per-Share & Ratios, Peer & Sector. Live formulas throughout — change a blue input and the value per share recomputes.
- **Standalone bibliography document**: primary documents · the full input register, every entry four-field · judgements with what would overturn each · negative results · where two sources disagree · what is not disclosed.
- **Carried in from this run**: the corrected drivers that passed §5; years 3–5 published as RANGES built from this record's own driver-error distribution, never as points; the graded maturities of earlier forecasts on an incremental run; and a one-line statement in §7 where the run was light or skipped, in those words.
- **The gates**: `assert_sigcm()`, `assert_beta_provenance()`, `assert_ground_up()`, `assert_model_study()` called in the study's own code, an independent recalculation of the DELIVERED workbook with zero mismatches, the external-reader scrub clean, every figure REBUILT before it is checked, and the rendered PDF read with every figure inspected as an image. Output the QC gate as a filled table with real evidence per row — never self-certified.
- **[R-GAP-01] If the central fair value lands more than 10% BELOW the latest known market price, the study is not finished.** Write `GAP_REVIEW_{DD-MM-YYYY}.md` in the study's own directory covering all eight headings — LATEST FILINGS · BASE YEAR · MACRO COHERENCE · DISCOUNT RATE · TERMINAL · BALANCE SHEET · CLAIMS AGAINST THE RECORD · MULTIPLE CROSS-CHECK — and clear `python3 scripts/check_valuation_gap.py`. The answer does not have to change; it has to be audited. Errors in a DCF are not symmetric — nearly all of them push value DOWN — so a large discount is where the defects are, and every gate above checks the PROCESS while none of them looks at the ANSWER. Worked precedent: `engine/amoc_study/GAP_REVIEW_01-09-2026.md`.
- **No rating, no price target, no buy/sell language.** A range and the reasoning behind it.

### Document 2 — the updated lessons-learnt document

`engine/Lessons_Register.md` and `engine/Lessons_Register.docx`, regenerated to include what this run taught. Both are GENERATED from `engine/lessons_register.py`; neither is hand-edited.

```
python3 engine/lessons_harvest.py {TICKER}     draft candidates from the run's own numbers
#   decide each draft: scope + applies_to + confirmed:true, or declined:"<reason>"
python3 engine/lessons_add.py {TICKER}         append and regenerate the Markdown
python3 engine/build_lessons_docx.py           regenerate the Word document
python3 scripts/check_lessons_register.py      confirm the gate is green
```

- **Every lesson is scoped** — **ALL** (binds on every study: method, arithmetic, how work is checked), **CLASS** (every company that works the same way), or **STOCK** (this company and nowhere else). Applying a STOCK lesson to another company is superstition.
- **Choosing the scope is the judgement and it is not automated.** Too narrow and the next study repeats the mistake; too broad and one company's quirk becomes a house rule nobody can dislodge. When unsure, file at the narrower scope and widen when a second company shows the same thing — one observation is not a pattern.
- **Every lesson carries what would overturn it.** A lesson with no falsifier is a habit, not a finding.
- **Every harvested finding ends registered or declined with a reason.** One that is neither fails the gate: an unanswered question must not pass as a clean result.
- **Fundamental walk-forward lessons are marked PROVISIONAL** while the method rests on too few names to be called validated. They are a record, not a rule, and the register binds nothing.

### Also produced, and internal

The scope decision and its reason; the training-record files (panel with provenance, error cells, the per-origin side-by-side income statements); the pre-registration text; the basis-break register; the corrections proposed with their test results; the caveats stated plainly (span obtained, provisional inputs, single-name limits); and an appended entry in the Fundamental Driver Ledger. None of this is shown to a reader.
