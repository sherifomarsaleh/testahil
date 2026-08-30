# Repaired CHAR-MC vs live production engine — head-to-head (26 Jul 2026)

**Verdict: production wins. Repaired CHAR-MC is 3.75% WORSE in CRPS, robust across all bootstrap
block sizes, and beats production on only 3 of 26 names.**

Live EG profile read from repo at run time: `nu=4.0, width_cal=0.972, signal_active=False`.

## Protocol
Same 26 EGX names, same `data_quality.clean_ohlc` gate (market='EG'), same origins
(min_history=260, non-overlapping step 60), h=60, 461 windows, 2017-07 → 2026-04.
Both arms scored with the SAME exact analytic CRPS (quantile integral — no MC sampling noise for
either side) and against the SAME yardstick: production's own carry-anchored trailing-252d RW.
CHAR-MC's (λ, ν) LONO cross-fitted at h=60 on the other 25 names.

## Result

| arm | cov@90 | width | CRPS/spot | median APE | skill vs yardstick |
|---|---|---|---|---|---|
| **PRODUCTION** mc_v3 carry-anchored YZ-HAR-t | 0.8937 | 0.776 | **0.1373** | 14.94% | **+1.73%** |
| Repaired CHAR-MC (M3b) | 0.8829 | 0.764 | 0.1424 | 15.02% | −1.95% |
| Yardstick: carry RW, trailing 252d | 0.8547 | 0.745 | 0.1397 | — | 0.00% |

Paired CRPS diff (CHAR-MC − production) **+0.005150 = +3.75% of production CRPS**.
Block bootstrap: block2 [+0.00328, +0.00704], block3 [+0.00333, +0.00693], block4 [+0.00342, +0.00690]
— **CHAR-MC worse at every block size, no sign flip.**

Note the repaired CHAR-MC also lands *below* the carry-RW yardstick at h=60 (−1.95%), even though it
beat an uncalibrated carry RW when horizons were pooled. The pooled +0.20% was carried by short
horizons; at h=60 alone it does not survive.

## Where production's edge comes from
Three ingredients the repaired CHAR-MC lacks, all already in `mc_v3`:

1. **Time-varying carry schedule.** Production reads rf from the EG `carry_schedule` (8.25% in 2020
   rising to 19.50% by Apr-2026). CHAR-MC inherits the original's flat rf = 19.50% for the entire
   history, which is anachronistic by up to 11 pp over 2021–2023 and systematically over-drifts the
   early sample. This is the single largest contributor.
2. **Lognormal bias correction `exp(s²/2)` + 0.8/0.2 log-space shrink** toward the trailing-252d
   proxy mean in `har_forecast_v3`. CHAR-MC uses the raw HAR forecast.
3. **Fitted `width_cal = 0.972`** against CHAR-MC's LONO-fitted λ = 1.031 on the same panel —
   production's corrected vol forecast needs slightly *narrowing*, CHAR-MC's raw one needs widening.

ν is the one place they agree: production 4.0, CHAR-MC LONO-fitted 4.07.

## Per-name
CHAR-MC is better on ABUK, HELI, ORWE only (3/26); production is better or level on the other 23.
Coverage is near-identical name-by-name — the gap is in the score, not the calibration.

Artefacts: `head2head.py`, `head2head_h60.csv` (session workspace).
