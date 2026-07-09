# Testahil analytics engine

This folder was previously populated with a parallel, generic multi-ticker engine
(`model_builder.py`, `report_builder.py`, `study_runner.py`, etc.) built in a session this
one has no visibility into and could not verify against the corrections made to the GBCO
study (MNT-Halan stake, sourced WACC). To avoid two unreconciled implementations sitting
side by side, that version was removed on 09-07-2026 and replaced with what is actually
verified: the exact scripts that built the current GBCO study, plus the standing WACC
module, both reconciled against the delivered `.docx`/`.xlsx` line by line.

## What's here now

- **`mc_v2.py`** — the "YZ-HAR" Monte Carlo engine (gap-aware Yang-Zhang width, pooled
  log-HAR cascade, unit-variance Student-t(5), asset-class-conditional drift). The version
  actually used to produce GBCO's Step 0 backtest and §3 Monte Carlo section.
- **`wacc_builder.py`** — the standing bottom-up WACC engine (house rule §3.5-G). Arithmetic
  only — every input (rf, ERP, beta, Kd, weights) must be sourced by the analyst before
  calling it; raises rather than defaulting on anything missing. Includes
  `RegressionBetaAttempt`, a usability gate that rejects unreliable regression betas (too
  few observations, R² too low, SE(beta) exceeding the estimate) instead of letting a
  rejected estimate get used — this is what caught GBCO's own n=5 annual regression
  (beta=-0.15, R²=0.008) and forced the beta=1.0 fallback. Adapted by market type (mature /
  GCC-pegged / other floating EM / metals-excluded — see the module docstring and the
  companion project file `Cost_of_Capital_Reference.md` for the full guidance). Reproduces
  GBCO's WACC exactly: 22.94% (CDS-based ERP, primary) / 25.08% (rating-based, alternative).
- **`gbco_study/`** — the exact source that produced `GBCO_Valuation_Study_08-07-2026_public.docx`
  and `GBCO_Valuation_Model_08072026_public.xlsx` (see that folder's own README). A worked
  example / template for the next study, not a generic plug-and-play pipeline — every file
  in it is hardcoded to GBCO's own numbers.

## Honest boundary
There is no generic `study_runner.py`-style orchestrator here anymore — building the next
study means following the pattern in `gbco_study/` (Step 0 → §1 fundamental build → DCF →
SOTP → Monte Carlo → docx/xlsx render → QC gate) adapted to the new ticker's own numbers,
not running unmodified code against a new CSV. Step 2 (pulling historical financials) and
the Step 4 expert-appendix authoring happen as research/writing in conversation, not as code.

## Prior state (for the record, not for reuse)
The removed generic-engine attempt (`model_builder.py`, `report_builder.py`,
`study_runner.py`, `qc_gate.py`, `step0_backtest.py`, `data_io.py`, `factor_library.py`,
`house_figures.py`, an earlier `mc_v2.py`/`monte_carlo.py` pair) claimed to have been
"reconciled end-to-end against real OHLC (PHDC)" with a passing Step 0 run. That claim was
never independently verified by this session before removal — noted here only so the
history isn't silently erased, not as a statement that the removal was wrong.
