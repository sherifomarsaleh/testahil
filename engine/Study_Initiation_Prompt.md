# TESTAHIL — study initiation prompt

The single prompt used to start a new valuation study. Everything between the rules below is the
prompt; copy it whole. Fill the `{braces}`. Nothing outside the rules is part of the prompt.

Governing rules live in `Standing_Research_Protocol.md`. For responding to an external critique of a
delivered study, use `Critique_Response_Prompt.md` — a different procedure, not this one.

---

Run a full valuation study for {TICKER} ({COMPANY NAME}), listed on {MARKET — EGX/Tadawul/ADX/QE/etc.}, currency {CCY}. This is NEW coverage — no existing study/ticker page/ledger cohort. OHLC is attached at {path or filename}. Follow the TESTAHIL Standing Research Protocol end-to-end without asking: read live state first (market_profiles.py + fitted_configs.json from the repo), then Step 0.0 data-quality gate → Step 0 calibration gate (scale-normalized, carry-anchored) → Step 2A four-ring Information Sweep → financials → build the 16-section Word + 16-sheet Excel matching TMPV_Valuation_Study_30-06-2026 → unprompted QC gate as a filled evidence table. Company class is {developer / recurring-income RE / bank / holdco / contractor / operating-co+captive lender / aggregator} → use the matching valuation lens. Reference study: {EAND operating-co / ADCB bank / ALPHADHABI holdco}. Do NOT publish — I'll request that separately with a token.

**The Excel must CALCULATE, not store. A number that could be derived from a driver and is instead pasted is a defect, not a formatting choice.**

Build the workbook formula-first:

- **Everything arithmetically derivable from an input is a live Excel formula.** The cost of capital is BUILT in the sheet — cost of equity from the risk-free rate net of the sovereign spread, beta and the premium; cost of debt after tax; weights from net debt and market capitalisation; the terminal rate from its own components — never a pasted rate. The glide fractions are visibly derived from the cost-of-debt path and the discount factors compound. The DCF waterfall chains: margin from EBITDA over revenue, EBIT from EBITDA less D&A, NOPAT from EBIT and the tax rate, FCFF from its four components, PV from FCFF and the factor. The terminal block chains: reinvestment = g / return on capital, then the terminal value from terminal NOPAT, reinvestment, the terminal rate and g. The statements chain; the balance sheet rolls property, working capital, equity and net debt forward; the cash flow links to the waterfall; **every ratio and per-share figure on every sheet is a formula.**
- **Only three classes of cell may be pasted, and READ FIRST must name them:** (1) audited and disclosed history — and where a line is both disclosed and derivable, carry the DISCLOSED figure; (2) the output of a unit build that would be unreadable flattened into a grid — paste its output, formula everything downstream of it; (3) whole-model re-runs — Monte Carlo maps and sensitivity grids, where each cell is a complete revaluation. State plainly that those grids do NOT redraw when a driver changes. **Anything else pasted is a defect.**
- **Show triangulations on the sheet.** Where a figure is estimated by several methods, put the methods in the workbook and average them there rather than asserting the result.
- **Verify on the delivered file, not on the builder.** The builder records the model's own value for every formula cell as it writes; a recalculation script then evaluates the workbook independently and asserts every formula cell reproduces it and that none is left unchecked. A separate driver test perturbs each input in place, re-evaluates the whole workbook, and asserts the headline moves in the right DIRECTION, with a dead-input sweep over the rest. Keep the evaluator strict — anything it cannot parse is a FAILURE, never a skip.
- **If a driver test fails, the first hypothesis is that the expectation is wrong, not the model.** Decompose the mechanism and report what actually happens before changing anything.
- **A workbook that has to disclaim its own Assumptions sheet has failed.** Only state the live-driver claim on READ FIRST once the driver test passes.

**Final QC gate.** Run as the last step before presenting the report and Excel. Before delivering, confirm every item below; fix and re-run anything that fails, then deliver.

(a) Study structure, content and format exactly match the reference files in the project

(b) Tables and graphs formatted the same as the reference files.

(c) Are these the best indicators for fundamental analysis of a {SECTOR}

(d) Calibration backtest done a full 5 years back, and it beats the random-walk benchmark on CRPS skill (> 0) with a roughly uniform PIT.

(e) Income statement and balance sheet carry 3 years historical + 5-year forecast, and a complete DCF valuation with 5-year forecast is included. DCF build to arrive at the Free Cashflow with EBITDA, D&A, EBIT, NOPAT (EBIT×(1−t)), + D&A, − Capex, − Δ working capital, Free cash flow to firm, Discount factor, PV of FCFF for the next 5 years.

(f) The expert appendix is worked in maximum detail.

(g) Experts are labelled "Expert 1 / Expert 2 / Expert 3" in the output, not their persona names (still cast by method from the Expert Persona Library).

(h) Also make sure numbers on all figures can be read as it has dark background.

(i) Make sure there is a summary valuation table

(j) Remove the calibration backtest from the appendix

(k) Remove references to our procedures like step 2A. The reader is an external party.

(l) I also want a bibliography table in a separate document stating where did you get the information from

(m) Remove any reference to the procedure like references to step 2A for example

(n) Review text on all graph to check that it is readable and there are no problems of contrast or over-writing one another

(o) Review width of all columns in tables to make sure words are displayed as a whole as much as possible and at the same time the widths are not excessively wide

(p) Terminal value as a percentage of enterprise value is visible to the READER — in the EV→equity bridge table and beside the DCF lens in the summary valuation table, in both Word and Excel, linked live in Excel and never typed

(q) **The workbook calculates.** Report the formula count against the pasted-value count. Every figure derivable from a driver is a live formula; the cost of capital, the glide, the discount factors, the DCF waterfall, the terminal block, the statement roll-forwards and every ratio are all built in the sheet. Only audited/disclosed history, the unit build's output, and whole-model re-run grids are pasted — and READ FIRST names those three classes explicitly.

(r) **Every formula cell reproduces the model, and drivers propagate.** Evidence, both run on the delivered file: "N of N formula cells reproduce the model, 0 unresolvable, 0 unchecked"; and the per-driver table showing each input perturbed in place moves the headline in the asserted direction, with zero dead inputs.

---

**Placeholders:** `{TICKER}` `{COMPANY NAME}` `{MARKET}` `{CCY}` `{path or filename}` `{company class}` `{reference study}` `{SECTOR}`.

**Two things to know about the gate letters.** Item (c) read "of a telco" — a leftover from an earlier study — and is now `{SECTOR}`. Items (k) and (m) say the same thing; both are kept so the existing lettering does not shift, since the QC evidence tables of delivered studies reference these letters by name. Items (p), (q) and (r) are new: (p) was already binding from the ELEC study but had never been written into this prompt, and (q)–(r) are the workbook rule above.

**Why (q) and (r) exist.** The SWDY workbook shipped with 92 formulas against 764 pasted values and a READ FIRST sheet claiming that changing an input repriced the model. It did not — no formula referenced the Assumptions sheet — and the claim had to be withdrawn. Rebuilt formula-first, the same file carries 589 formulas against 395 values and the claim is true and tested. The two gates caught a market-capitalisation formula pointing one row off its share count, and the rebuild exposed two different interest roll-forwards for the same company disagreeing by up to EGP 117mn.
