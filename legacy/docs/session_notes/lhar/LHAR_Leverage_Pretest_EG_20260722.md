# LHAR Leverage-Effect Pre-Test — EG Panel (22 Jul 2026)

> **OUTCOME (same day, prototype simulation): CLOSED — DO NOT BUILD.** The effect is statistically real in daily data but IMMATERIAL at product horizons. See "Prototype cone comparison" section at the bottom. LHAR is not the individuality lever; the open candidates remain the fundamentals drift tilt and the factor-HAR.

**Question:** Does volatility on EGX rise more after down moves than after equal-sized up moves (leverage effect), name by name — i.e., is there signal for a per-name asymmetric HAR (LHAR) extension to mc_v3?

**Status of this section: PRE-TEST — in-sample association, NOT a promotion test.**

## Method

Per name, on the full cleaned library series (Step 0.0 gate applied via `data_quality.clean_ohlc`, market='EG'):

```
log v[t+1] = a + b_d·log RV_d + b_w·log RV_w + b_m·log RV_m + g_neg·max(−r_t,0) + g_pos·max(r_t,0)
```

- v = YZ variance proxy (`mc_v2.yz_variance_proxy`) — the engine's own vol input
- RV_d/w/m = 1/5/22-day trailing means of v (the HAR terms; these control for vol clustering, so g_neg/g_pos measure asymmetry *beyond* "big moves happen in turbulent times")
- r_t = close-to-close log return; separate down/up magnitude terms
- Newey-West (L=10) errors; asym = g_neg − g_pos; one-sided test of asym > 0
- Non-finite windows dropped; all 30 names retained (n_obs ≈ 1,000–2,050 each)

## Results (sorted by t_asym)

| ticker | n_obs | g_neg | g_pos | asym | t_asym | vol bump after −3% | after +3% |
|---|---|---|---|---|---|---|---|
| FWRY | 1246 | 13.03 | 6.81 | 6.22 | 3.55 | +21.6% | +10.8% |
| EFIH | 1030 | 16.70 | 7.68 | 9.02 | 3.23 | +28.5% | +12.2% |
| CCAP | 1126 | 12.12 | 8.36 | 3.75 | 2.48 | +19.9% | +13.4% |
| OIH | 1086 | 11.45 | 7.45 | 4.00 | 2.41 | +18.7% | +11.8% |
| RMDA | 1126 | 11.68 | 7.82 | 3.86 | 2.01 | +19.2% | +12.4% |
| HRHO | 1140 | 15.79 | 9.27 | 6.52 | 1.97 | +26.7% | +14.9% |
| PHDC | 1255 | 14.67 | 11.23 | 3.45 | 1.76 | +24.6% | +18.3% |
| ISPH | 1207 | 12.97 | 9.39 | 3.58 | 1.72 | +21.5% | +15.1% |
| BTFH | 1252 | 12.02 | 9.37 | 2.65 | 1.69 | +19.8% | +15.1% |
| TMGH | 1151 | 13.72 | 10.26 | 3.46 | 1.65 | +22.9% | +16.6% |
| EMFD | 1053 | 11.88 | 8.48 | 3.40 | 1.45 | +19.5% | +13.6% |
| RAYA | 1168 | 5.83 | 3.47 | 2.36 | 1.40 | +9.1% | +5.3% |
| LCSW | 1310 | 9.22 | 6.99 | 2.22 | 1.40 | +14.8% | +11.1% |
| KABO | 1285 | 9.42 | 6.74 | 2.68 | 1.33 | +15.2% | +10.6% |
| DSCW | 1774 | 11.04 | 8.99 | 2.05 | 1.28 | +18.0% | +14.4% |
| ADIB | 1217 | 10.62 | 7.47 | 3.15 | 1.24 | +17.3% | +11.9% |
| HELI | 1158 | 12.27 | 8.93 | 3.34 | 1.21 | +20.2% | +14.3% |
| GBCO | 1248 | 9.82 | 7.83 | 2.00 | 1.10 | +15.9% | +12.5% |
| ORAS | 1268 | 20.61 | 17.58 | 3.04 | 0.97 | +36.2% | +30.2% |
| EFID | 1193 | 10.77 | 7.68 | 3.09 | 0.94 | +17.5% | +12.2% |
| OCDI | 1131 | 9.89 | 7.70 | 2.19 | 0.88 | +16.0% | +12.3% |
| PRDC | 996 | 10.11 | 8.15 | 1.96 | 0.80 | +16.4% | +13.0% |
| ORHD | 1303 | 9.22 | 8.27 | 0.95 | 0.51 | +14.8% | +13.2% |
| COMI | 987 | 19.72 | 18.46 | 1.26 | 0.34 | +34.4% | +31.9% |
| ETEL | 1256 | 14.26 | 13.28 | 0.97 | 0.31 | +23.8% | +22.1% |
| JUFO | 1236 | 14.09 | 13.80 | 0.29 | 0.12 | +23.5% | +23.0% |
| ORWE | 1181 | 9.03 | 8.64 | 0.39 | 0.11 | +14.5% | +13.8% |
| ABUK | 1206 | 11.14 | 11.78 | −0.64 | −0.25 | +18.2% | +19.3% |
| CLHO | 2050 | 8.29 | 9.58 | −1.29 | −0.67 | +13.2% | +15.5% |
| EGAL | 1238 | 8.22 | 9.62 | −1.40 | −0.68 | +13.1% | +15.5% |

## Panel verdict (statistical)

- **asym > 0: 27/30 names. Significant leverage (t>1.645, one-sided 10%): 10. t>1.96: 6. Significantly inverted: 0.**
- Under a no-effect null: ~15/30 positive expected, ~3 significant by chance. Sign-test p ≈ 4×10⁻⁶. The panel-level effect is REAL.
- Median g_neg 11.56 vs g_pos 8.56 (median asym 2.67): after a −3% day the median name's next-day vol jumps ~+19%, vs ~+13% after a +3% day.
- ISPH and ORHD are vol twins (46.6%/46.8% forecast vol) but not leverage twins: ISPH asym 3.58 (t=1.72), ORHD 0.95 (t=0.51).

## Prototype cone comparison (same day) — WHY THIS IS CLOSED

Prototype simulator: per-path 22-day rolling variance window, LHAR update reacting to each simulated path's own returns, EG profile (ν, width_cal), carry drift, seed 42, 50k paths, H=756. Three runs on ISPH + ORHD:

1. **Naive LHAR (linear response, uncapped): EXPLODES.** ORHD 3-yr p5 −33%, p95 +45% vs the symmetric arm. Cause: t(ν≈4) draws produce daily moves far outside the fitted support; exp(g·|r|) then multiplies variance by huge factors → vol-of-vol feedback loop. This is an extrapolation artifact, not leverage (ORHD has the *least* asymmetry). Any future path-dependent vol model MUST bound its response to the fitted data range.
2. **Guarded LHAR (response capped at in-sample p99.5 ≈ 10–11% daily move): cone ≈ unchanged.** ISPH 3-yr p5 +1.2%/p95 −3.5%; ORHD p5 −7.2%/p95 +5.9% (this residual is refit noise across all coefficients, not the leverage term — see run 3). T+60: within ±2% for both names.
3. **Isolated asymmetry (same fitted model, same seed, only g_neg/g_pos vs their average): ≤1.1% everywhere.** ISPH 3-yr p5 −1.1%, p95 −0.9%, terminal log-return skew +0.02 → −0.02; ORHD ≤0.5%, skew +0.02 → −0.00. T+60 ≤0.6%.

**Mechanism of the washout:** leverage moves *next-day* vol after down days, but over 240–756 sessions up-days and down-days nearly balance in count, so cumulative variance and terminal skew barely move. Materiality bar for published cones is 5% — the honest effect is ~1%. Statistically real ≠ material at testahil's horizons.

**Standing conclusions:**
- LHAR: closed, do not build (re-open only if the product ever publishes short-horizon (≤1 month) skew/tail products, where daily leverage might matter).
- The naive-spec explosion is a documented hazard for ANY future path-dependent vol candidate (incl. factor-HAR): bound responses to fitted support, and remember (ν, width_cal) must be refit on the new engine's residuals.
- Individuality roadmap now: (a) fundamentals-anchored drift tilt (fv_convergence) — per-name medians, the axis currently uniform at carry; (b) factor-HAR (β²×EGX30 + idio) — per-name vol responsiveness. Both must clear the Step 0 walk-forward gate.

Scripts (session): /tmp/leverage_pretest.py, /tmp/lhar_cone_compare.py, /tmp/lhar_cone_compare2.py, /tmp/lhar_isolate.py. Companion finding: v3 1-yr mean EV cross-section spans 22.7%–45.3% across the 30 EG names (corr 0.98 with own HAR vol) — the engine is already per-name on vol LEVEL; medians are uniform at carry (~18.6%) by design.
