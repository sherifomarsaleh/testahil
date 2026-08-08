# Session close-out — 26 Jul 2026

## Done and landed
- **CHAR-MC audited, repaired, retested, REJECTED.** Metrics were hardcoded name-string lookups;
  no Monte Carlo; Student-t/YZ/HAR/conformal all absent from the code; charts drawn with λ moved
  from the new cone to the old. Repaired properly it gives +0.20% CRPS vs an uncalibrated RW and
  **loses to production by 3.75%** at h=60 (better on 3/26 names). Their own v2 backtest now
  reports 82.14% coverage vs 98.81% for the baseline. Their v2 "refactored" code file was
  byte-identical (MD5 `2428fbf…`) to v1.
  Docs: `claude/external_reviews/CHAR_MC_*`.
- **EG library extended to full vendor histories — MERGED (PR #22).** All 30 names, RAW as the
  library expects. Median history 5.5yr → 15.6yr, +51,150 rows. Overlap verified RAW-vs-RAW:
  19/30 zero differing rows, 11/30 differ only on the old file's final (provisional) close.
  Doc: `claude/data/EG_15yr_Library_Ingest_and_Calibration_Finding_20260726.md`.

## Two mistakes I made, both caught by Sherif — worth remembering
1. Compared the repo's RAW files against my own GATE-CLEANED files and reported a corporate-action
   "basis change" in OCDI/EFIH/DSCW. There was none. Worse, committing those cleaned files would
   have **double-adjusted 5 names**, since the library stores raw and `data_quality` adjusts at load.
2. Claimed the ISPH FAIL violated the protocol's robust-across-{2,3,4} rule. Running **their**
   `panel_refresh.robust_verdict` instead of my own bootstrap: all three blocks FAIL
   ([-0.0527,-0.0006] / [-0.0511,-0.0010] / [-0.0486,-0.0050]). The rule is implemented correctly.
   **No code fix needed — this work item is closed.**

   Standing lesson: when my numbers disagree with production's, run production's code first.

## Findings that stand
- **Calibration sample: PARITY.** Extending past the 2022-03-21 break cut is not significant on the
  30-name panel (492 windows, blocks {2,3,4} all straddle zero). **The break cut stands.** An earlier
  26-name run said otherwise; three added names flipped it. Block-bootstrap robustness ≠ robustness
  to panel composition — check both.
- **Adaptive-width overlay validated on the merged data**: 22/30 names get a better-sized cone,
  pooled |std_u−1| 0.096 → 0.083, CRPS PARITY (no cost). Pushed and ready on
  `feat/adaptive-width-overlay-eg` with evidence at `engine/PENDING_REVIEW/
  EG_adaptive_width_validation_20260726.md`.
- **The overlay does NOT rescue ISPH** (multiplier 1.001, coverage 75%→75%). Adaptive lag: all four
  ISPH cone breaks (−41%, +89%, +58%, +66%) fall inside the scoring window, so the online estimator
  had no prior signal. Moves verified genuine — gradual, worst single day 14%, no corporate action.
  **ISPH's FAIL is real.** 16 windows, ~53% annualised vol.
- **Data-quality flags:** EGX70 has High==Low on 100% of pre-2019 rows (no YZ variance before
  2020-01-20 — 6.5yr usable, not 15). RAYA has flat High==Low on 34.6% of sessions; decide its
  treatment before it enters a fit. EGX30/EGX70 deliberately NOT added to the EG equity folder.

## Open — needs the browser (GitHub API and merges are blocked for the agent session)
1. Merge `feat/adaptive-width-overlay-eg`.
2. Actions → "Testahil continuous calibration" → **Run workflow**. A code-only change does not
   auto-trigger; otherwise it waits for the 03:00 UTC cron.
3. Close the stale `calibration-review-20260726-153819` (pre-dates both the data merge and the overlay).
4. Then review the fresh calibration PR. Expect roughly nu 4.0 → 5.0, width_cal 0.972 → 0.93, and
   ISPH carrying an honest FAIL.

## Also open
- Two GitHub PATs were pasted into the chat this session. **Both should be revoked.**
- Optional engine improvement: the gate's CRPS uses `crps_sample` on 20k–50k simulated paths. Both
  predictive laws are analytic, so the exact quantile-integral CRPS is free and would remove Monte
  Carlo noise from the bootstrap CIs. Production still needs paths for published percentiles; this
  is a change to the gate only.
