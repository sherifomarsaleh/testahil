# TESTAHIL — project memory

This repo runs the TESTAHIL Standing Research Protocol: valuation studies, calibrated
probability cones, and a public ledger, published to the live site. Read this before
doing any research, study-build, critique-response, or publishing work here.

**Full governing rules — read before starting any study:**
@engine/PROJECT_INSTRUCTIONS_01-09-2026.md

That file is the condensed, binding digest (rules only, never volatile numbers). The
complete prose version, with the reasoning and the failures each rule was adopted from,
is `engine/Standing_Research_Protocol.md` — read it when a condensed rule needs its
full context, or before amending any rule.

**KEEP THE TWO IN SYNC — same discipline as `Publish_Protocol.md`'s standing prompt.**
Any new or amended standing rule gets added to BOTH files in the same commit: the full
account in `Standing_Research_Protocol.md`, and a condensed paragraph in
`PROJECT_INSTRUCTIONS_{DD-MM-YYYY}.md` (the digest — its filename carries the date of its
latest amendment and the include line above is updated in the same commit as any rename;
rule only, no narrative, no volatile numbers — the
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
- **Fundamental calibration — walk-forward testing the forecasting method on a company's own
  history, a standing step of every new study and every update → `engine/Fundamental_Walkforward_Prompt.md`
  [R-FCAL-01].** NOT the same test as the price-engine calibration; never write "the
  walk-forward" without saying which. Every run produces TWO documents: the updated
  fundamental analysis at full model-report depth, and the updated lessons register — a run
  that produces one and not the other is not finished.
- **Running that walk-forward across the WHOLE book, name after name →
  `engine/Fundamental_Walkforward_Campaign_Prompt.md`** (adopted 01-Sep-2026, per instruction).
  The campaign wrapper only — it changes no research method, and does not restate the
  single-name protocol above. Market order is fixed (EGX → UAE → KSA → Qatar → India → Korea →
  USA); within a market, oldest standard first [R-STD-01]. THE QUEUE IS NEVER WRITTEN IN A
  DOCUMENT — read it live with `python3 engine/campaign_queue.py` (`--next` for the next
  unstarted name), which refuses rather than returning a short list. Metals are excluded by
  construction (no issuer, no statements, no drivers) and named in the exclusion list. HARD
  STOP AFTER EGX to review whether the method generalises before UAE begins. FREEZE THE OLD
  FAIR VALUE FIRST — `python3 engine/fv_movement.py snapshot TK` — because the rebuild is the
  one sanctioned thing that moves `fair{bear,base,full}` and `data.js` carries no date or
  standard stamp, so a baseline taken afterwards is a fabricated zero.
- **What each rebuild did to fair value → `engine/Fundamental_Calibration_FV_Register.md`,
  the fair-value half of the Fundamental Analysis Calibration Register** (the lessons half is
  `Lessons_Register.md`; cross-referenced by lesson id, never duplicated). GENERATED from
  `engine/fv_movement.py` ← `fv_movement.json`, never hand-edited. `fv_movement.py check`
  anchors on the run directories on disk, so a register that stopped being fed FAILS rather
  than reporting clean. Internal — nothing here reaches the live site. For the 67 names with
  no prior study the "old" number came from no current-standard study at all, so the movement
  column measures a new study against a number of unknown provenance — say so wherever it is
  quoted.
- **THE LESSONS DOCUMENT CARRIES A CALIBRATED-STOCKS TABLE** [per instruction, 01-Sep-2026 —
  "I want the lessons document to keep track of all stocks that have been calibrated stating
  their Market / Class / Fair Price before calibration / Fair Price after calibration"].
  One row per calibrated name, in both the `.md` and the `.docx`. It is GENERATED at build
  time from `fv_movement.json` and `COMPANY_CLASS`, never typed and never hand-maintained —
  the same discipline as every other number in that document. THIS IS NOT A SECOND COPY OF
  THE FV REGISTER: the "never duplicated" clause below bars a number being *remembered* in
  two places, not being *rendered* in two, and both documents read the one store, so a
  figure cannot drift between them. A name with a run on disk and no row FAILS the gate
  rather than being quietly absent [R-ENF-04]; where the pre-calibration number came from no
  current-standard study its provenance is unknown and the row says so instead of printing a
  movement. THE TABLE OPENS THE DOCUMENT [same instruction] and carries TWO COMPANION
  SECTIONS beside it: **stocks attempted and BLOCKED**, each stating what stopped it and what
  would unblock it — read from that run's own `blocked.json`, so the reason is recorded by the
  run that hit it and a later session cannot quietly soften it, and a blocked run with no
  reason FAILS; and **stocks still to be calibrated**. That last one is the ONE PLACE the
  campaign queue may appear in a document, and it is not an exception to "THE QUEUE IS NEVER
  WRITTEN IN A DOCUMENT" — that rule bars a queue kept BY HAND, which goes stale the moment a
  name is run and looks authoritative the whole time it is wrong. This list is RESOLVED FROM
  `campaign_queue.py` AT BUILD TIME and a name leaves it the moment its run directory exists.
  The gate reconciles done + blocked + remaining against the queue's own total, so a document
  built before the last run FAILS rather than printing a stale list.
- **What every study taught us, and how far it travels → `engine/Lessons_Register.md` (and
  `.docx`) [R-LESSON-01].** READ IT BEFORE STARTING ANY STUDY OR UPDATE:
  `python3 engine/lessons.py TICKER --class CLASS` returns exactly what binds on that name —
  ALL (every study), CLASS (every company that works the same way), STOCK (that name alone;
  applying one of these elsewhere is superstition). GENERATED from `engine/lessons_register.py`,
  never hand-edited. After a run: `lessons_harvest.py TK` drafts candidates from the run's own
  numbers, you decide each scope (the one step deliberately not automated), `lessons_add.py TK`
  appends, `build_lessons_docx.py` refreshes Word. Fundamental lessons are PROVISIONAL while the
  method rests on too few names — read them, don't cite them as authority.
- **Technical calibration — the shipped technical read, walk-forward tested on its own
  under-one-month clock (5/10/21 sessions) against distance-matched placebos → the lab is
  `engine/lab/ta_calibration/`, the per-name record `engine/tech_record.py` →
  `engine/tech_records.json` (renders nowhere until instructed), the findings
  `engine/lab/ta_calibration/Technical_Lessons_Register.docx` (T-01…, generated, never
  typed) [R-TCAL-01].** The THIRD test called a walk-forward — never write "the
  walk-forward" without saying which. Any change to `engine/technicals.py` re-runs the
  harvest and the record IN THE SAME PASS (the record stores the hash of the read it
  graded; `scripts/check_tech_calibration.py` in CI goes red if they diverge). Findings
  feed nothing into the MC engine or the fundamentals — [R-LENS-01] stands; a change to
  the read or engine still clears the promotion rule.
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
  compiled, and that is stated in the file rather than implied.

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

**DO NOT ASK THE USER TO SCOPE A LESSON** [per instruction, 01-Sep-2026 — "do not ask me
that question ... I leave that to you"]. [R-LESSON-01]'s scope judgement is still made and
still signed, by whoever runs the harvest, and the rule itself is UNCHANGED: file at the
NARROWER scope when unsure and widen when a second company shows the same thing. The user's
own stated lean is the opposite — "everywhere, including class and across all tickers" —
and they delegated the decision rather than imposing it, so the rule wins over the lean.
Record that as the reason wherever a lesson is filed narrow, because a later session
reading only the lean would widen everything and quietly turn one company's quirk into a
house rule. The harvest is still fully resolved: every candidate ends registered or
declined with a reason [R-ENF-04]. Nothing else about the loop changes — one name at a
time, and the register is regenerated and sent at the end of each run rather than held by
the user, whose own copy is what went stale on 01-Sep-2026.
