# Direction-Signal Tournament — 23-Aug-2026

**STATUS: RESEARCH ONLY. Not adopted, not promoted, not published.** No engine
config, published cone, ledger row, or site surface is touched by anything in
this folder. Adopting any finding requires the standing promotion rule
(out-of-sample gate, materiality review, PR) exactly as for every prior
candidate.

## Why

Client critique (23-Aug-2026, relayed by Sherif): the published cones are very
wide and carry no direction. Both are factually right — every live cone's
center is the interest-rate carry, because every directional candidate ever
tested was ablated. But the recorded ablations were scored under CRPS, which
`direction_score.py`'s own header documents as near-blind to direction. The
Phase B direction-aware referee existed and had never been pointed at a broad
candidate set. This tournament is that sweep.

## What ran

Six price-only, parameter-free candidates — 12-month and 6-month momentum
(skip-month), 1-month reversal, distance from 52-week high, distance from the
200-session average, Wilder RSI(14)−50 — at the calendar 1M and 3M clocks, on
every covered market's cleaned library (Step 0.0 gate per series, per-market
artifact thresholds). Forward returns are excess of each market's own carry.
Two framings: cross-sectional ("which of these names") and pooled time-series
("which way is this one"), the latter scored by `direction_score.score()` with
its block bootstrap {2,3,4}, LONO, and MIN_N=100 power gate.

A **survivor** must, in one market at pooled n≥100: hold a same-sign CI across
all blocks AND be LONO sign-stable AND same-sign in both halves of history AND
agree in sign across framings. Six features × 2 horizons × 2 framings ×
9 markets is a multiple-testing minefield; anything less than all four tests
at once is noise with a decimal point.

## Files

- `tournament.py` — the sweep (import-verified; reuses `data_quality.clean_ohlc`,
  `direction_score`, `technicals`, `market_profiles`)
- `RESULTS_23-08-2026.{json,md}` — full per-market tables and the survivor list

## Reproduce

    python3 engine/direction_tournament/tournament.py \
        --generated 2026-08-23 \
        --json engine/direction_tournament/RESULTS_23-08-2026.json \
        --md engine/direction_tournament/RESULTS_23-08-2026.md

Seed 42 throughout; deterministic.

## Known limits (flagged, not hidden)

- Dividends are not netted from forward returns (q=0): level-harsh on
  high-dividend names, materially neutral for rank/sign scoring.
- AE pools ADX + DFM names (one country factor), consistent with the
  calibration panel's market grouping — the beta/index exchange-matching rule
  is about regressors, not about this research grouping.
- 3M cross-sectional dates overlap month-to-month; the block bootstrap over
  the date series is the correction. Pooled 3M uses quarter-end origins only.
- A survivor here is still selection-biased by construction (six candidates
  were tried). The standing promotion gate — not this tournament — decides
  adoption; the honest next step for any survivor is a pre-registered forward
  shadow cohort, as `lab_round8_fvpull.py` already prescribes for FV-pull.
