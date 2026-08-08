# Master Evaluations Workbook — build note (26-Jul-2026)

Deliverable: `Testahil_MC_v3_Master_Evaluations_26-07-2026.xlsx` — 74 instruments,
9 markets, one row per name. Built to the *shape* of the uploaded CHAR MC master-
evaluation sheet, but on the Testahil v3 engine, not that model.

Build scripts (local, not committed): `engine/build_master_eval.py` (engine run →
`master_eval_records.json`) and `engine/make_workbook.py` (records → workbook).

## Chain executed (production, no approximation)

Per ticker in `engine/raw_ohlc/{MARKET}/{TICKER}.csv`:
Step 0.0 `data_quality.clean_ohlc(market=…)` → gap-aware YZ proxy → `fit_har_v3` →
`har_forecast_v3` (fitted separately at h=20 and h=60) → carry drift
`ln(1+rf_live) − ln(1+q)`, q=0 → `simulate_paths_v3` with the profile's live
(ν, width_cal), 50,000 paths, seed 42. `market_profiles.py` verified by IMPORT
before the run. Every profile has `signal_active=False`, so no signal enters any
number.

## Build decisions (user, this session)

- Scope: full library, all 74 names / 9 markets.
- Horizon: **T+20 and T+60 only**. No 1-year column — the uploaded file has one,
  but the gate, the (ν, width_cal) fit and every coverage figure are calibrated at
  h=60. A T+250 cone would be extrapolation with zero OOS evidence.
- `q_annual = 0` for every name, flagged per row and in READ FIRST. Drift is a
  GROSS-OF-DIVIDEND price carry; overstates drift for high-payout names (Gulf/EGX
  banks, ETEL, ARAMCO, ABUK, QNB) by ~the yield. Sourcing q per name is the single
  highest-value upgrade to this file.

## What replaced the uploaded model's parameters

The uploaded sheet carries saturation θ, calibration λ*, an explicit volatility
drag and a "g number". None exist in v3. Replaced by ν, width_cal, and the **90%
cone multiple = width_cal × q95(unit-variance t(ν))** — the object the materiality
gate actually watches. Drift is not estimated from price history at all, so within
a market every name shares the same carry and all cross-sectional cone variation
comes from volatility.

The uploaded sheet marks every asset PASSED with coverage ≈0.90 and CRPS skill
≥+15%. Ours does not: 51 PARITY, 8 PASS, 9 BOUNDARY, 1 PROVISIONAL, **3 robust
FAILs (SA/ELM, KR/LGES, QA/IQCD)**.

## Two discrepancies found while building (both worth action)

1. **`engine/fitted_configs.json` is STALE** (derived mirror, not source of truth).
   It still carries the retired one-name XAU self-fit (ν=Gaussian, cal=1.00, GOLD
   PARITY +0.0035, SILVER absent) instead of the merged two-name fit in
   `market_profiles.py` (ν=20, cal=1.035, market PASS +0.0099, GOLD PARITY +0.0011,
   SILVER PASS +0.0181), and it is missing EG/DSCW entirely. Nothing in production
   reads the mirror, so no live forecast was affected — but it should be
   regenerated. All workbook numbers were taken from `market_profiles.py`.
2. **`engine/adaptive_width.py` is not on main** — still on its feature branch with
   the PR open. Confirmed live via git. Also moot today: the deepest EG history in
   the library carries **17** resolved 60-day windows vs the overlay's
   `MIN_WINDOWS=28` gate, so it would be forced to exactly 1.0 for every EG name
   even if merged. (Only GOLD/67 and PLATINUM/62 clear 28 windows, and the overlay
   is EG-only.)

## Other observations

- **The spots are not a same-day cross-section.** Library refresh is one stock at a
  time; spot dates run 23-Jun-2026 → 20-Jul-2026. Each row carries its own spot
  date and an age flag. Not usable as a same-day screen.
- **KR/SAMSUNG carries the highest conditional vol in the library, 79% p.a.**
  (h60). Not a DQ artifact: the cleaned series runs ~60k → 339.5k KRW over twelve
  months with repeated ±13% sessions, continuously, no split signature. Genuine in
  the data as held — but worth a source check before this name is published.
- EG/ADIB (ADIB Egypt) and AE/ADIB (the UAE parent) are the same ticker string on
  two panels. Flagged per row; distinct from the ADIBUAE duplicate already fixed.

## QC performed

`recalc.py`: 370 formulas, 0 errors. Cell-by-cell diff of the delivered file
against the engine records: 1,850 Master cells + 518 Diagnostics cells + all Data
Quality row counts, **zero mismatches**; Market Calibration ν/width_cal/rf_live
tied back to `market_profiles.py` by assertion. Cone multiple independently
re-derived from (ν, width_cal), max error 0.0. Percentile monotonicity checked on
all 148 (name × horizon) cones.

Realized coverage, std(u) and cone width on the Diagnostics sheet are recomputed
under the LIVE (ν, width_cal) rather than the panel-build baseline. Because every
profile is carry-only (alpha ≡ 0, asserted in code), the live standardized residual
is exactly the stored `u / width_cal` — an exact rescaling, not an approximation.
