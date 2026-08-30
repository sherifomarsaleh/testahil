# TA-Signal Ablation — EG panel, h=5/10 (22-Jul-2026)

**Question.** Does a technical-analysis drift signal, injected through the engine's own
`signal_alpha` hook (alpha = b·sigma_H·clip(z,±2), dead zone |z|<0.5, cap ±0.5·sigma_H),
improve pooled scale-normalized CRPS out-of-sample on the EG panel at short horizons?
Prompted by: "can we combine the MC simulation with technical analysis" (1–2-week use case).

**Verdict: NO — DO NOT PROMOTE.** 6 of 8 (signal × horizon) cells are robust FAILs
(CI < 0 across block sizes {2,3,4}); the other 2 are PARITY. No cell shows positive skill.
This matches the standing precedent twice over: the rev_1m ablation that switched EG's
signal OFF at h=60, and the CRPS-selection idea that won in-sample and lost under LONO.

## Design (production-exact, paired)
- 29-name EG panel (fitted_configs.json panel_names), data_quality-cleaned, origins
  ≥ 2022-03-21 (adopted break cut), non-overlapping, min_history 260, q=0 (gate-neutral).
- Engine leg: fit_har_v3/har_forecast_v3 per origin → sigma_H = √(dv·h)·0.972, carry from
  the EG schedule, nu=4, 20k paths, seed 42+origin — identical on both legs; the on-leg
  terminal sample is EXACTLY off_sample·exp(alpha) (same RNG draws), so the paired CRPS
  difference isolates the signal and nothing else. Verified bit-for-bit (assert in script),
  as was the incremental HAR fast path vs fit_har_v3 (6 sample origins).
- Signals, z = trailing-252 z-score of the raw stat (min 60 obs), engine clip/dead-zone
  semantics: brk20 = ln(close/prior-20d-high); macd = MACD(12,26,9) histogram / close;
  rsi = RSI(14) Wilder; rev_1m = engine signal_z. Slope b (sign+magnitude) LONO
  cross-fitted: for name j, OLS slope of u on clip(z) pooled over the other 28 names,
  capped |b| ≤ 0.10. u = (log(y/spot) − carry)/sigma_H.
- Gate: Δskill = 1 − Σ(crps_on/spot)/Σ(crps_off/spot); house robust_verdict
  (panel_refresh.verdict_ci, blocks {2,3,4}, 3000 draws, seed 42).
- Windows: 5,879 (h=5), 2,934 (h=10).

## Results
| h | signal | Δskill | fired | verdict | CI(block2) |
|---|--------|--------|-------|---------|------------|
| 5 | brk20  | +0.00005 | 61% | PARITY | [−0.0001, +0.0002] |
| 5 | macd   | −0.00025 | 58% | FAIL   | [−0.0004, −0.0001] |
| 5 | rsi    | −0.00033 | 64% | FAIL   | [−0.0006, −0.0001] |
| 5 | rev_1m | −0.00006 | 57% | PARITY | [−0.0003, +0.0001] |
| 10 | brk20 | −0.00026 | 61% | FAIL   | [−0.0004, −0.0001] |
| 10 | macd  | −0.00034 | 59% | FAIL   | [−0.0005, −0.0002] |
| 10 | rsi   | −0.00037 | 64% | FAIL   | [−0.0005, −0.0002] |
| 10 | rev_1m| −0.00044 | 58% | FAIL   | [−0.0006, −0.0003] |

CI(3) and CI(4) agree with CI(2) in every FAIL cell (no block-dependent sign flips).

**Why it fails (the tercile table).** Mean standardized forward return u by z-tercile is
U-shaped/flat, not monotone — e.g. h=10 macd: lo +0.128 / mid +0.014 / hi +0.166;
h=10 rev_1m: lo +0.151 / mid +0.017 / hi +0.140. Pooled LONO slopes are |b| ≤ 0.009
(vs the 0.08 literature IC prior) — there is no monotone conditional signal for the
linear alpha to harvest, so the fitted drift shift is noise and degrades the cone.
This also kills the route-3 idea (conditional-odds overlays keyed on these four TA
states): the conditioning does not separate outcomes.

## Side findings
1. **Short-horizon baseline holds.** Signal-off engine vs carry-anchored RW benchmark:
   +0.0123 (h=5), +0.0089 (h=10) pooled CRPS skill — the h=60-calibrated engine remains
   positive when extrapolated to 1–2-week horizons, though thinner than the h=60 gate's
   ~+0.020. (Context only — the standing gate remains h=60; no gate change proposed.)
2. **Everything-positive u.** Mean u > 0 in every tercile (post-break bull drift above
   carry). That is unconditional drift, not a TA signal; raw secular drift stays RETIRED.
3. **Multiplicity note.** 8 cells tested; the finding is negative, so multiple-testing
   inflation is not a concern (it would only flatter the signals, and none survived anyway).

## What remains sanctioned
Combining MC with TA at the OUTPUT layer (route 1): reading P(touch level), time-to-touch,
P(close beyond S/R) off the existing 50k paths at chart-chosen levels. That uses the
calibrated distribution without touching drift and needs no gate.

Scripts: ta_ablation.py (pass 1, records + HAR verification), pass2.py (LONO scoring,
verdicts, terciles), verdicts.json (machine-readable results). Engine NOT modified;
nothing promoted; repo untouched.
