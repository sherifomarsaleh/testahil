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
- THE MODEL STUDY (canonical template + research-depth bar, adopted 08-Aug-2026) →
  `engine/swdy_study/` — SWDY_Valuation_Study_05-08-2026 + its Excel + its standalone
  bibliography + `QC_GATE_05-08-2026.md`. Every study matches its sections list, sheet list
  and depth; machine-readable form in `engine/research_protocol.py` (`MODEL_STUDY`,
  `MODEL_STUDY_DEPTH`, `ModelStudyChecklist` + `assert_model_study()`). THE REFERENCE SET IS
  CLOSED AT THREE NAMES — SWDY (model study + operating-co pattern), ADCB (bank), ALPHADHABI
  (holdco); `REFERENCE_SET` asserts on exactly those. No other company is a template or an
  exemplar. Company names elsewhere in the protocol are evidence or coverage, not references.
- Responding to an external critique of a delivered study → `engine/Critique_Response_Prompt.md`
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
- Prior driver decisions by name/class → `engine/Fundamental_Driver_Ledger.md` — **also
  referenced but not present as of 07-Aug-2026.** Rebuilding it means compiling real driver
  decisions out of each delivered study's own compute.py/QC docs — a real research task, not
  something to fabricate from a template.

**Shared code every study should use, not reinvent:**
- `engine/research_sweep.py` — the Step 2A Information Sweep register and its enforced
  invariants (coverage, provenance, consequence, gate linkage, primary access, FS depth,
  study-year quarter coverage, IR coverage). Import this rather than hand-rolling a
  study-local sweep script — `engine/scem_study/sweep.py` is the pattern to follow.
- `engine/wacc_builder.py` — bottom-up cost of capital, including the beta-regression
  usability gate (`RegressionBetaAttempt`).
- `engine/research_protocol.py` — SIGCM: `SIGCMChecklist` + `assert_sigcm()`, the standing
  hard gate. A violation must not issue, not just warn.
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
