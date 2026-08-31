# TESTAHIL — project memory

This repo runs the TESTAHIL Standing Research Protocol: valuation studies, calibrated
probability cones, and a public ledger, published to the live site. Read this before
doing any research, study-build, critique-response, or publishing work here.

**Full governing rules — read before starting any study:**
@engine/PROJECT_INSTRUCTIONS_11-07-2026.md

That file is the condensed, binding digest (rules only, never volatile numbers). The
complete prose version, with the reasoning and the failures each rule was adopted from,
is `engine/Standing_Research_Protocol.md` — read it when a condensed rule needs its
full context, or before amending any rule.

**KEEP THE TWO IN SYNC — same discipline as `Publish_Protocol.md`'s standing prompt.**
Any new or amended standing rule gets added to BOTH files in the same commit: the full
account in `Standing_Research_Protocol.md`, and a condensed paragraph in
`PROJECT_INSTRUCTIONS_11-07-2026.md` (rule only, no narrative, no volatile numbers — the
file's own header says as much). This digest has gone stale three times already this
session from exactly this drift. After editing it, send the user its full current text in
chat (not just a diff) — they paste it into their own external project files, so a
diff-only summary leaves that copy silently behind.

**Other governing documents, by task:**
- Starting a brand-new study → `engine/Study_Initiation_Prompt.md`
- THE MODEL REPORT (the document every study is modelled on, adopted 19-Aug-2026) →
  ADNOCLS_Valuation_Study_09-08-2026 (`engine/adnocls_study/` + its Excel + its standalone
  bibliography + `QC_GATE_09-08-2026.md`) MINUS the section "What changed in these editions,
  and why" — edition history is internal QC evidence, never in a delivered document. The built
  document is `engine/model_report/MODEL_REPORT_09-08-2026.docx` (produced and asserted by
  `build_model_report_docx.py`) — **open it beside the study you are writing**. Every study
  matches its sections list, sheet list, content and depth; machine-readable form in
  `engine/research_protocol.py` (`MODEL_STUDY`, `MODEL_STUDY_DEPTH`, `ModelStudyChecklist` +
  `assert_model_study()`). THE REFERENCE SET IS CLOSED AT THREE NAMES — ADNOCLS (model report +
  operating-co pattern), ADCB (bank), ALPHADHABI (holdco); `REFERENCE_SET` asserts on exactly
  those, and that SWDY is gone (displaced 19-Aug-2026, one-in-one-out, removed outright). No
  other company is a template or an exemplar. Company names elsewhere in the protocol are
  evidence or coverage, not references.
- Responding to an external critique of a delivered study → `engine/Critique_Response_Prompt.md`
- Re-deriving a study's beta against its exchange's index and rebuilding on it →
  `engine/Beta_Reissue_Prompt.md` (canonical prompt + the FERTIGLB worked precedent)
- Publishing a study or update to the live site → `engine/Publish_Protocol.md`
- Rolling forward / grading a matured ledger cohort → `engine/Rollforward_and_Grading_Protocol.md`
- Fundamental study ↔ Monte Carlo cone integration → `engine/Fundamental_MC_Integration_Protocol.md`
- SIGCM (source-integrity & ground-up construction mandate, QC hard gate) →
  `engine/Source_Integrity_and_Ground_Up_Mandate.md`
- Cost of capital reference tables → `engine/Cost_of_Capital_Reference.md` — **referenced by
  `wacc_builder.py` and `market_profiles.py` but not present in the repo as of 07-Aug-2026.**
  It would need to hold live-sourced, per-market rf/ERP/policy-rate figures with dates — exactly
  the volatile-number class this protocol says never to reconstruct from memory. Source it live
  per-market before relying on it, don't assume it exists.
- Prior driver decisions by name/class → `engine/Fundamental_Driver_Ledger.md` — created
  30-Aug-2026 after being referenced since 07-Aug-2026 while absent. It holds the PHDC
  walk-forward entry; entries for the studies delivered before that date have NOT been
  compiled, and that is stated in the file rather than implied. Compiling them means reading
  each study's own committed compute and QC docs — a real research task, not something to
  fabricate from a template.
- **What every study taught us, and how far it travels → `engine/Lessons_Register.md`
  [R-LESSON-01].** READ IT BEFORE STARTING ANY STUDY OR UPDATE. Every lesson is tagged ALL
  (binds on every study), CLASS (binds on every off-plan developer, telecom operator, bank…)
  or STOCK (binds on one company and nowhere else — applying one of these to another company
  is superstition). Call `lessons_register.lessons_for(ticker, klass)` for exactly the set
  that binds on the name in hand. GENERATED from `engine/lessons_register.py` by
  `engine/build_lessons_register.py` and never hand-edited; `scripts/check_lessons_register.py`
  fails the build if the document is not its generator's byte-for-byte output, if a
  walk-forward run exists with no lesson behind it, or if a registered class is empty.
  APPEND IN THE SAME COMMIT that records a finding, and read the counts live rather than from
  any document. **After a walk-forward run: `python3 engine/lessons_harvest.py TK` drafts the
  candidate lessons from the run's own numbers, you decide each one's scope (the one step that
  is deliberately not automated), then `python3 engine/lessons_add.py TK` appends them and
  `python3 engine/build_lessons_docx.py` refreshes the Word file. Every draft must end
  registered or declined with a reason — the gate fails on one that is neither.** Read it any
  time with `python3 engine/lessons.py [TICKER] [--class X]`, or the `/lessons` skill.

**Shared code every study should use, not reinvent:**
- `engine/research_sweep.py` — the Step 2A Information Sweep register and its enforced
  invariants (coverage, provenance, consequence, gate linkage, primary access, FS depth,
  study-year quarter coverage, IR coverage). Import this rather than hand-rolling a
  study-local sweep script — `engine/scem_study/sweep.py` is the pattern to follow.
- `engine/beta_regression.py` — **THE ONLY sanctioned way to produce a regression beta.**
  `own_stock_beta(ticker, market, exchange)` resolves the regressor itself, runs Step 0.0 on
  both series, matches the weekly grid to the exchange's real trading week, and returns
  provenance with the number. **Never hand-roll a study-local beta script.** Every study in
  this repo once did, and every one of them regressed against an equal-weight composite of
  the covered names — on FERTIGLB that understated beta by ~40% (0.492 vs 0.931 against the
  real index) and overstated fair value by 21.6%.
- `engine/wacc_builder.py` — bottom-up cost of capital, the beta-regression usability gate
  (`RegressionBetaAttempt`), and `market_index_path(market, exchange)` / `EXCHANGE_INDEX` /
  `index_interim_note()`. The regressor is the published index of the exchange the stock is
  **listed on**, read from `engine/raw_indices/{MARKET}/{INDEX}.csv`. A constituent composite
  is not a substitute and not a tier. **Match the exchange, not the country** — market `AE`
  spans ADX and DFM, so `market_index_path('AE')` deliberately RAISES. If the index is not
  held, STOP AND ASK; do not build a composite and proceed.
- `engine/raw_indices/{MARKET}/{INDEX}.csv` — the published index series, deliberately
  OUTSIDE `raw_ohlc/` so an index never enters a calibration panel as a covered name.
  Registered: AE/ADX→FADGI, AE/DFM→FADGI *(labelled interim)*, EG/EGX→EGX30, IN/NSE→NIFTY50,
  KR/KRX→KOSPI100, QA/QSE→QATAR10 *(weekly-only caveat)*, SA/TADAWUL→TASI, US/NASDAQ→NASDAQCOMP.
  **BR and GB are unregistered — no conforming beta is possible there.**
- `engine/research_protocol.py` — SIGCM: `SIGCMChecklist` + `assert_sigcm()`, the standing
  hard gate. A violation must not issue, not just warn. Also `assert_beta_provenance()`,
  which inspects the actual beta record rather than trusting a checklist boolean — that
  boolean was set `True` by every study while it regressed on a composite.
- `engine/adaptive_width.py` — the EG-only, history-gated per-stock cone-width overlay.
  Overlay only; never touches the pooled (ν, width_cal) fit, drift, or tail.
- `engine/data_quality.py` — Step 0.0, mandatory before any calibration, fit or study.
- `engine/mc_v3.py` + `engine/market_profiles.py` — the production Monte Carlo engine.
  A study's own calibration check must reproduce the committed fit, never re-derive one.

All of the above — plus `technicals.py`, `apply_technicals.py`, `ta_chart.py`,
`rollforward_one.py` — are verified by **import, not by parsing** before any commit relies
on them (`nu=Gaussian` parses cleanly and only dies at import — that exact bug once reached
`main`).

**Never** quote a calibration figure, fitted parameter, or panel membership from memory
or from a document — always read `engine/market_profiles.py` and
`engine/fitted_configs.json` live first; they are volatile and refit on every post.

**Response style in this repo:** 3-4 sentences max, no preamble, lead with the answer.
Expand only if asked. Never a rating or a price target — fair-value ranges and
distributions only.
