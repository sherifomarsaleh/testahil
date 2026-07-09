# Testahil analytics engine

The full production engine referenced by the Standing Research Protocol, versioned here
alongside the site it publishes to. Reconciled end-to-end against real OHLC (PHDC) on
2026-07-09: full `study_runner.py` run completed all 8 stages without error, Step 0 passed
(CRPS skill +0.124, 18 non-overlapping 5-yr origins), and the QC gate correctly separated
mechanized checks (PASS) from analyst-authored narrative items (PENDING, with receipts).

## Files
- `data_io.py` — OHLC loader (investing.com CSV export format)
- `factor_library.py` — per-asset-class factor sets (16-factor structure, Appendix A)
- `mc_v2.py` — the "YZ-HAR" Monte Carlo engine (gap-aware Yang-Zhang width, pooled log-HAR
  cascade, unit-variance Student-t(5), asset-class-conditional drift)
- `monte_carlo.py` — the original v1 engine that `mc_v2.py` is a drop-in replacement for
- `step0_backtest.py` — Step 0 calibration backtest (CRPS skill / Winkler / PIT vs the
  zero-drift random-walk benchmark)
- `house_figures.py` — fan chart, distribution figures, touch ladder, PIT histogram, MA-stack
- `model_builder.py` — 16-sheet Excel model builder (Assumptions-linked, fully wired DCF)
- `report_builder.py` — Word study skeleton builder (TMPV house structure)
- `qc_gate.py` — Final QC gate, reads the produced .docx/.xlsx and emits a filled evidence table
- `study_runner.py` — orchestrator; CLI: `python study_runner.py <ohlc_csv> <TICKER> [out_dir] [shares_mn]`
- `wacc_builder.py` — bottom-up WACC engine (house rule §3.5-G). Arithmetic only — every input
  (rf, ERP, beta, Kd, weights) must be sourced by the analyst before calling it; raises on any
  missing input rather than defaulting. Includes `RegressionBetaAttempt`, a usability gate that
  rejects unreliable regression betas (n too small, R² too low, SE(beta) exceeding the estimate)
  so a rejected regression can't quietly get used — falls back to beta=1.0 per house rule instead.
  Adapted by market type (mature / GCC-pegged / other floating EM / metals-excluded — see the
  module docstring and `Cost_of_Capital_Reference.md` in project files for the full guidance).
  Built and reconciled against GBCO (09-07-2026): reproduces WACC 22.94% (CDS-based ERP) /
  25.08% (rating-based ERP) exactly against the hand-verified figures in that study.

## Known open item
Step 0 interval-coverage diagnostics on the PHDC reconciliation run under-covered relative to
target (50/80/90% targets vs 39/67/78% empirical) despite a passing CRPS skill. Coverage is a
diagnostic only, not the pass gate, but worth investigating before treating Step 0 passes as
fully trustworthy at scale.

## Honest boundary
The runner does not pull financials (Step 2) or author the §1 narrative / three-expert
appendix — those are the analyst/model layer applied on top of this spine.
