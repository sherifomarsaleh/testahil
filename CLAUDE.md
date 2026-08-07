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

**Other governing documents, by task:**
- Starting a brand-new study → `engine/Study_Initiation_Prompt.md`
- Responding to an external critique of a delivered study → `engine/Critique_Response_Prompt.md`
- Publishing a study or update to the live site → `engine/Publish_Protocol.md`
- Rolling forward / grading a matured ledger cohort → `engine/Rollforward_and_Grading_Protocol.md`
- Fundamental study ↔ Monte Carlo cone integration → `engine/Fundamental_MC_Integration_Protocol.md`
- Cost of capital reference tables → `engine/Cost_of_Capital_Reference.md`
- Prior driver decisions by name/class → `engine/Fundamental_Driver_Ledger.md`

**Shared code every study should use, not reinvent:**
- `engine/research_sweep.py` — the Step 2A Information Sweep register and its enforced
  invariants (coverage, provenance, consequence, gate linkage, primary access, FS depth,
  study-year quarter coverage, IR coverage). Import this rather than hand-rolling a
  study-local sweep script — `engine/scem_study/sweep.py` is the pattern to follow.
- `engine/wacc_builder.py` — bottom-up cost of capital, including the beta-regression
  usability gate.
- `engine/data_quality.py` — Step 0.0, mandatory before any calibration, fit or study.
- `engine/mc_v3.py` + `engine/market_profiles.py` — the production Monte Carlo engine.
  A study's own calibration check must reproduce the committed fit, never re-derive one.

**Never** quote a calibration figure, fitted parameter, or panel membership from memory
or from a document — always read `engine/market_profiles.py` and
`engine/fitted_configs.json` live first; they are volatile and refit on every post.

**Response style in this repo:** 3-4 sentences max, no preamble, lead with the answer.
Expand only if asked. Never a rating or a price target — fair-value ranges and
distributions only.
