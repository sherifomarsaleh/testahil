# TESTAHIL — study initiation prompt

The single prompt used to start a new valuation study. Everything between the rules below is the
prompt; copy it whole. **Fill in two things: the company and its exchange.** Everything else is
derived by the analyst and stated back before the build starts.

Governing rules live in `Standing_Research_Protocol.md`. For responding to an external critique of a
delivered study, use `Critique_Response_Prompt.md` — a different procedure, not this one.

---

Run a full valuation study for **{COMPANY NAME}**, listed on **{EXCHANGE}**. This is NEW coverage — no existing study, ticker page or ledger cohort.

**Work out the rest yourself. Do not ask me for it.** Derive each of the following, state what you derived and on what evidence in your first response, then proceed without waiting for confirmation:

- **Ticker and market code** — the exchange gives the market code (EGX→EG, Tadawul→SA, ADX/DFM→AE, QE→QA, LSE→GB, NSE/BSE→IN, KRX→KR, B3→BR, NYSE/Nasdaq→US).
- **Reporting and valuation currency** — from the market (EG→EGP, SA→SAR, AE→AED, QA→QAR, GB→GBP, IN→INR, KR→KRW, BR→BRL, US→USD). If the company reports in a currency other than its listing currency, say so and state which one the valuation runs in and why.
- **OHLC price history** — repo convention is `engine/raw_ohlc/{MARKET}/{TICKER}.csv`. Use it if it is there. If it is not, and I have not attached one, **say so immediately and stop** — do not proceed on a partial or reconstructed price series, and do not substitute an index.
- **Company class, and therefore the valuation lens** — developer, recurring-income real estate, bank, holding company, contractor, operating company with a captive lender, aggregator, or something else. Derive it from the filings, not from the sector label: state the revenue mix and balance-sheet shape you based it on. **If the company genuinely straddles two classes, do not pick one — value the legs separately with the lens each needs and sum them.** The lens decision is the one that invalidates the whole study if it is wrong, so show your evidence for it.
- **Reference study to match** — the MODEL REPORT is **ADNOCLS_Valuation_Study_09-08-2026** (`engine/adnocls_study/`), minus the section "What changed in these editions, and why"; the built document is `engine/model_report/MODEL_REPORT_09-08-2026.docx` — open it beside the study you are writing. Its sections list, sheet list and research depth are the standard for EVERY class. The class picks the LENS PATTERN only, and **the reference set is closed at exactly three names** — ADNOCLS (operating company / diversified industrial), ADCB (bank), ALPHADHABI (holding company). No other company is a template or a reference study; if the class is none of these three, adapt the nearest pattern's lens inside ADNOCLS's skeleton and say which you adapted and why. Do not go looking for a fourth exemplar.
- **Sector** — for gate item (c) below.

Then follow the TESTAHIL Standing Research Protocol end-to-end without asking: read live state first (market_profiles.py + fitted_configs.json from the repo), then Step 0.0 data-quality gate → Step 0 calibration gate (scale-normalized, carry-anchored) → Step 2A four-ring Information Sweep → financials → build the 16-section Word + 16-sheet Excel + standalone bibliography document matching the MODEL REPORT, ADNOCLS_Valuation_Study_09-08-2026 (`engine/adnocls_study/`; machine-readable skeleton and depth bar in `engine/research_protocol.py` `MODEL_STUDY` / `MODEL_STUDY_DEPTH`) → unprompted QC gate as a filled evidence table, with `ModelStudyChecklist` attested alongside SIGCM.

**Step 2A's Company ring, primary-source discipline [ADDED 07-Aug-2026].** Try the company's own
official website / investor-relations page FIRST, before any aggregator — log the attempt and its
outcome in the Sweep Register even when it fails (a real case: a company's own site returned
`connect_rejected` at the build environment's proxy), and ask the user to attach the primary
document directly rather than silently substituting a weaker secondary source. Pull **audited
financial statements for a minimum of TWO, target FOUR, complete past fiscal years**, from the
filing itself. For the study year itself, pull **every quarter already disclosed** before the
build starts — not discovered afterward because a user asked. Treat **every available
investor-relations presentation and investor/earnings-call transcript** as a mandatory sweep
source, not optional colour: this is where volumes, per-unit prices, utilisation rates and segment
splits live, and none of it is in the financial statements. Tag these `COMPANY_INVESTOR_RELATIONS`
in the Sweep Register, kept separate from `AUDITED_FINANCIAL_STATEMENTS`.

**The Excel must CALCULATE, not store. A number that could be derived from a driver and is instead pasted is a defect, not a formatting choice.**

Build the workbook formula-first:

- **Everything arithmetically derivable from an input is a live Excel formula.** The cost of capital is BUILT in the sheet — cost of equity from the risk-free rate net of the sovereign spread, beta and the premium; cost of debt after tax; weights from net debt and market capitalisation; the terminal rate from its own components — never a pasted rate. The glide fractions are visibly derived from the cost-of-debt path and the discount factors compound. The DCF waterfall chains: margin from EBITDA over revenue, EBIT from EBITDA less D&A, NOPAT from EBIT and the tax rate, FCFF from its four components, PV from FCFF and the factor. The terminal block chains: reinvestment = g / return on capital, then the terminal value from terminal NOPAT, reinvestment, the terminal rate and g. The statements chain; the balance sheet rolls property, working capital, equity and net debt forward; the cash flow links to the waterfall; **every ratio and per-share figure on every sheet is a formula.**
- **Only three classes of cell may be pasted, and READ FIRST must name them:** (1) audited and disclosed history — and where a line is both disclosed and derivable, carry the DISCLOSED figure; (2) the output of a unit build that would be unreadable flattened into a grid — paste its output, formula everything downstream of it; (3) whole-model re-runs — Monte Carlo maps and sensitivity grids, where each cell is a complete revaluation. State plainly that those grids do NOT redraw when a driver changes. **Anything else pasted is a defect.**
- **Show triangulations on the sheet.** Where a figure is estimated by several methods, put the methods in the workbook and average them there rather than asserting the result.
- **Verify on the delivered file, not on the builder.** The builder records the model's own value for every formula cell as it writes; a recalculation script then evaluates the workbook independently and asserts every formula cell reproduces it and that none is left unchecked. A separate driver test perturbs each input in place, re-evaluates the whole workbook, and asserts the headline moves in the right DIRECTION, with a dead-input sweep over the rest. Keep the evaluator strict — anything it cannot parse is a FAILURE, never a skip.
- **If a driver test fails, the first hypothesis is that the expectation is wrong, not the model.** Decompose the mechanism and report what actually happens before changing anything.
- **A workbook that has to disclaim its own Assumptions sheet has failed.** Only state the live-driver claim on READ FIRST once the driver test passes.

**The forecast is anchored on the latest reviewed period, and the record says so [R-ANCHOR-01,
ADDED 03-Sep-2026].** A near-term reviewed actual outranks a stale full-year rate. Anchor every unit
rate on the most recent reviewed period; hold everything else flat, **including observed
improvements**; and let a rate drift only where a named structural mechanism has a **measured**
like-for-like direction in the company's own period pair.

Commit a `forecast_anchor` record in the study's numbers file — the rate forecast, the latest
reviewed period with its date and rate, the first forecast year's rate, and the whole forecast path.
Where the forecast opens materially below the latest reviewed period, **or declines materially
across the explicit window**, name a mechanism from the closed list, carry the disclosure that
establishes it from the filings, and supply the like-for-like measurement that gives it a direction.
`scripts/check_forecast_anchor.py` fails a new study directory that carries neither a record nor a
deliberate ratchet entry, so this is not optional and not something to come back to.

Two traps, both of which shipped in delivered studies on the day this rule was adopted and both of
which lowered the value:

- **One escalator per driver class, and the price and cost legs must sit on the same clock.**
  Escalating pound-denominated cost legs at domestic inflation while a dollar-linked price grows
  only at the currency differential is a real cost drift compounding for ever. It produces a margin
  decline the study then reports as a finding. If you assert a real cost drift, it is a *claim*:
  name it, source it, and measure its direction in the company's own filings.
- **A typed commodity-price path is not a driver.** "Constructed: mean-reverting toward the marginal
  producer's cash cost", with no cash cost quoted and no institution publishing the path, is an
  assumption wearing a forecast's clothes. Hold a traded commodity price FLAT unless a source says
  otherwise — and check what the rest of the book does with the same class of input, because **a
  driver out of line with the book usually means our method slipped on this one name.**

**Final QC gate.** Run as the last step before presenting the report and Excel. Before delivering, confirm every item below; fix and re-run anything that fails, then deliver.

(a) Study structure, content, format AND research depth exactly match the MODEL REPORT (ADNOCLS_Valuation_Study_09-08-2026, `engine/adnocls_study/`) — including the standalone bibliography document and every depth-bar standard in `MODEL_STUDY_DEPTH`

(b) Tables and graphs formatted the same as the reference files.

(c) Are these the best indicators for fundamental analysis of a company in the sector you identified

(d) Calibration backtest done a full 5 years back. **The gate is whether the BANDS HELD** [R-CAL-03] — realized coverage against the stated target on non-overlapping 3-month calendar windows, two-sided binomial at 5%, which is the same test the reader is shown. The width ratio against a naive carry-anchored band is DISCLOSED beside it and carries no threshold. CRPS skill and PASS/PARITY/FAIL are RETIRED: internal diagnostics only, never a gate, never on any surface a reader sees.

(e) Income statement and balance sheet carry 3 years historical + 5-year forecast, and a complete DCF valuation with 5-year forecast is included. DCF build to arrive at the Free Cashflow with EBITDA, D&A, EBIT, NOPAT (EBIT×(1−t)), + D&A, − Capex, − Δ working capital, Free cash flow to firm, Discount factor, PV of FCFF for the next 5 years.

(f) The expert appendix is worked in maximum detail.

(g) Experts are labelled "Expert 1 / Expert 2 / Expert 3" in the output, not their persona names (still cast by method from the Expert Persona Library).

(h) Also make sure numbers on all figures can be read as it has dark background.

(i) Make sure there is a summary valuation table

(j) Remove the calibration backtest from the appendix

(k) Remove references to our procedures like step 2A. The reader is an external party.

(l) I also want a bibliography table in a separate document stating where did you get the information from

(l2) **Every deliverable ships as a PDF.** The Word file is the build artifact; the PDF is what the reader gets, and no study is delivered without one. Render with `python3 engine/make_pdf.py <files>` and report the page and figure count of each. If a conversion fails, fix the toolchain — do not record it as an environment limitation until you have checked that the converter is actually installed COMPLETE (LibreOffice without libreoffice-writer/calc fails on every input, including a two-line CSV).

(l3) **Read the rendered PDF before delivering.** Open it and look at it — the rendered document is where layout breaks, table overflow and copy errors become visible. On the SWDY edition this step caught published site copy that stated the wrong lens weights.

(l4) **[ADDED 07-Aug-2026] Sweep Register shows primary-source depth in the Company ring.** The
register (feeding the bibliography document, item (l)) must show: an attempt at the company's own
website/IR page, logged whether it succeeded or failed; a minimum of two, target four, complete
past audited fiscal years cited to the filing itself; every quarter of the study year already
disclosed at build time; and at least one investor-relations presentation or call transcript,
tagged `COMPANY_INVESTOR_RELATIONS` distinctly from `AUDITED_FINANCIAL_STATEMENTS`. Missing any of
these is a QC FAIL, not a noted limitation, unless the shortfall itself is stated plainly (e.g. the
company genuinely discloses only one prior year).

(m) Remove any reference to the procedure like references to step 2A for example

(n) Review text on all graph to check that it is readable and there are no problems of contrast or over-writing one another

(o) Review width of all columns in tables to make sure words are displayed as a whole as much as possible and at the same time the widths are not excessively wide

(p) Terminal value as a percentage of enterprise value is visible to the READER — in the EV→equity bridge table and beside the DCF lens in the summary valuation table, in both Word and Excel, linked live in Excel and never typed

(q) **The workbook calculates.** Report the formula count against the pasted-value count. Every figure derivable from a driver is a live formula; the cost of capital, the glide, the discount factors, the DCF waterfall, the terminal block, the statement roll-forwards and every ratio are all built in the sheet. Only audited/disclosed history, the unit build's output, and whole-model re-run grids are pasted — and READ FIRST names those three classes explicitly.

(r) **Every formula cell reproduces the model, and drivers propagate.** Evidence, both run on the delivered file: "N of N formula cells reproduce the model, 0 unresolvable, 0 unchecked"; and the per-driver table showing each input perturbed in place moves the headline in the asserted direction, with zero dead inputs.

(s0) **[R-ANCHOR-01] The `forecast_anchor` record is committed and `python3 scripts/check_forecast_anchor.py` is clean** — the latest reviewed period, its rate, the first forecast year's rate and the whole path; and where the forecast opens materially below that period or declines materially across the window, a mechanism from the closed list with its disclosure and its like-for-like measurement. A gate that fails a new study carrying neither a record nor a deliberate ratchet entry.

(s) **[R-GAP-01] If the central fair value lands more than 10% from the latest known market price in EITHER direction, the study is not finished.** (Two-sided since 02-Sep-2026: a gate that can only fire one way teaches the work to drift the other, while looking rigorous. And the price is the LATEST KNOWN one, per the 03-Sep-2026 amendment — a study audited against a month-old quote is audited against its own past.) Write `GAP_REVIEW_{DD-MM-YYYY}.md` in the study's own directory covering all eight headings — LATEST FILINGS · BASE YEAR · MACRO COHERENCE · DISCOUNT RATE · TERMINAL · BALANCE SHEET · CLAIMS AGAINST THE RECORD · MULTIPLE CROSS-CHECK — and clear `python3 scripts/check_valuation_gap.py`. The answer does not have to change; it has to be audited. Errors in a DCF are not symmetric — nearly all of them push value DOWN — so a large discount is where the defects are, and every gate above checks the PROCESS while none of them looks at the ANSWER. Worked precedent: `engine/amoc_study/GAP_REVIEW_01-09-2026.md`.

Do NOT publish — publishing is a separate, explicitly-requested step. (The old token gate is retired: once I say "publish", go all the way to merged-and-deployed without stopping to ask. See `Publish_Protocol.md`.)

---

**What you fill in:** the company and its exchange. That is the whole input.

**The one thing that can still block the run** is the price history. Market data is not reachable
from the build environment, so the OHLC has to be in `engine/raw_ohlc/{MARKET}/{TICKER}.csv` or
attached to the message. The prompt instructs a hard stop rather than a reconstructed series,
because a fabricated price history would silently corrupt the calibration gate, the beta regression
and the Monte Carlo cone at once.

**Why company class is derived rather than asked.** It is a reading of the filings, not a fact the
requester holds — but it is also the single decision that invalidates a study if it is wrong, which
is why the prompt requires the evidence to be shown and forbids forcing a straddling company into
one lens.

**Two notes on the gate letters.** Item (c) previously hardcoded "telco"; it now refers to the
sector the analyst identified. Items (k) and (m) say the same thing and are both kept deliberately —
delivered studies cite these letters by name in their QC evidence tables, so re-lettering would
break those references.
