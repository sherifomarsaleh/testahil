# TESTAHIL — study initiation prompt (v3, 06-Aug-2026)

Two parts: the instruction that starts the study, and the QC gate that closes it. Placeholders in
`{braces}` are filled per study; everything else is verbatim.

**Changed in v3 (06-Aug-2026):** the Excel deliverable must CALCULATE. Part One now specifies a
formula-driven workbook and the two gates that verify it on the delivered file; Part Two adds items
(p), (q) and (r). Driven by the SWDY build, where a 92-formula / 764-pasted-value workbook had to
disclaim its own Assumptions sheet; rebuilt formula-first it carries 589 formulas and the
live-driver claim is true and tested. Standing rule: `Standing_Research_Protocol.md`, section
"THE WORKBOOK IS A MODEL, NOT A PRINTOUT".

---

## Part One — procedure to conduct the research

Run a full valuation study for {TICKER} ({COMPANY NAME}), listed on {MARKET — EGX/Tadawul/ADX/QE/etc.},
currency {CCY}. This is NEW coverage — no existing study/ticker page/ledger cohort. OHLC is attached
at {path or filename}.

Follow the TESTAHIL Standing Research Protocol end-to-end without asking: read live state first
(`market_profiles.py` + `fitted_configs.json` from the repo), then Step 0.0 data-quality gate →
Step 0 calibration gate (scale-normalized, carry-anchored) → Step 2A four-ring Information Sweep →
financials → build the 16-section Word + 16-sheet Excel matching `TMPV_Valuation_Study_30-06-2026`
→ unprompted QC gate as a filled evidence table.

Company class is {developer / recurring-income RE / bank / holdco / contractor / operating-co+captive
lender / aggregator} → use the matching valuation lens. Reference study: {EAND operating-co /
ADCB bank / ALPHADHABI holdco}.

**The Excel is a working model, not a printout of one.** Build it formula-first:

- **Everything arithmetically derivable from an input is a live Excel formula.** The cost of capital
  is BUILT in the workbook — cost of equity from the risk-free rate net of the sovereign spread,
  beta and the premium; cost of debt after tax; weights from net debt and market capitalisation; the
  terminal rate from its own components — never a pasted rate. The glide and the discount factors
  compound, with the glide fractions visibly derived from the cost-of-debt path. The DCF waterfall
  chains through margin, EBIT, NOPAT, FCFF and PV. The terminal block chains through
  reinvestment = g / return on capital to the terminal value. The statements chain; the balance
  sheet rolls property, working capital, equity and net debt forward; the cash flow links to the
  waterfall; **every ratio and per-share figure on every sheet is a formula.**
- **Only three classes of cell may be pasted, and READ FIRST must name them:** (1) audited and
  disclosed history — and where a line is both disclosed and derivable, carry the DISCLOSED figure;
  (2) the output of a unit build that would be unreadable flattened into a grid — paste its output,
  formula everything downstream; (3) whole-model re-runs — Monte Carlo maps and sensitivity grids,
  where each cell is a complete revaluation. Say plainly that those grids do NOT redraw when a
  driver changes. Anything else pasted is a defect.
- **Show triangulations on the sheet.** Where a figure is estimated by several methods, put the
  methods in the workbook and average them there rather than asserting the result.
- **Verify on the delivered file, not on the builder.** The builder records the model's own value
  for every formula cell as it writes; the recalculation script evaluates the workbook independently
  and asserts every formula cell reproduces it and that none is left unchecked. A separate driver
  test perturbs each input in place, re-evaluates the whole workbook, and asserts the headline moves
  in the right DIRECTION, with a dead-input sweep over the rest. Only state the live-driver claim on
  READ FIRST once that test passes.
- **If a driver test fails, the first hypothesis is that the expectation is wrong, not the model.**
  Decompose the mechanism and report what actually happens before changing anything.

Do NOT publish — I'll request that separately with a token.

---

## Part Two — final QC gate

Run as the last step before presenting the report and Excel. Before delivering, confirm every item
below; fix and re-run anything that fails, then deliver.

**(a)** Study structure, content and format exactly match the reference files in the project.

**(b)** Tables and graphs formatted the same as the reference files.

**(c)** Are these the best indicators for fundamental analysis of a {SECTOR}?

**(d)** Calibration backtest done a full 5 years back, and it beats the random-walk benchmark on
CRPS skill (> 0) with a roughly uniform PIT.

**(e)** Income statement and balance sheet carry 3 years historical + 5-year forecast, and a
complete DCF valuation with 5-year forecast is included. DCF build to arrive at the free cash flow
with EBITDA, D&A, EBIT, NOPAT (EBIT×(1−t)), + D&A, − Capex, − Δ working capital, free cash flow to
the firm, discount factor, PV of FCFF for the next 5 years.

**(f)** The expert appendix is worked in maximum detail.

**(g)** Experts are labelled "Expert 1 / Expert 2 / Expert 3" in the output, not their persona names
(still cast by method from the Expert Persona Library).

**(h)** Numbers on all figures can be read — check against the dark background.

**(i)** There is a summary valuation table.

**(j)** The calibration backtest is removed from the appendix.

**(k)** References to our procedures (e.g. "Step 2A") are removed. The reader is an external party.

**(l)** A bibliography table in a separate document states where the information came from.

**(m)** Review text on all graphs for readability — no contrast problems, no overwriting.

**(n)** Review the width of all columns in tables: words display whole as far as possible, and the
widths are not excessively wide.

**(o)** Terminal value as a percentage of enterprise value is visible to the READER — in the
EV→equity bridge table and beside the DCF lens in the summary valuation table, in both Word and
Excel, linked live in Excel and never typed.

**(p) The workbook calculates.** Report the formula count against the pasted-value count. Every
figure derivable from a driver is a live formula; the cost of capital, the glide, the discount
factors, the DCF waterfall, the terminal block, the statement roll-forwards and every ratio are all
built in the sheet. Only audited/disclosed history, the unit build's output, and whole-model re-run
grids are pasted — and READ FIRST names those three classes explicitly. **A workbook that has to
disclaim its own Assumptions sheet has failed this item.**

**(q) Every formula cell reproduces the model.** The recalculation script evaluates the delivered
workbook independently and asserts each formula cell equals the value the model computed for it,
and that no formula cell is left unchecked. Evidence: "N of N formula cells reproduce the model,
0 unresolvable, 0 unchecked." Keep the evaluator strict — anything it cannot parse is a FAILURE,
never a skip.

**(r) Drivers propagate.** The driver test perturbs each input in place, re-evaluates the whole
workbook from scratch, and asserts the headline moves in the asserted direction; a dead-input sweep
bumps every remaining driver and requires it to move something. Evidence: the per-driver table with
zero failures and zero dead inputs.
