# Equation Lab — Round 5: Bayes-Stein / Hierarchical Drift Shrinkage (23-Jul-2026)

**Trigger:** shortlist item #1 from `claude/mc_survey/MC_Family_Survey_and_Verdict_20260723.md` — "the one honest, literature-backed lever we have not yet pulled." This round builds and DEV-tests it. **Verdict: FAIL, monotonically, across the entire shrinkage grid. No FINAL-window shot taken (none of the 9 candidates showed DEV promise) — same discipline as Round 3 Arm 2 (LHAR).**

Lab-only: production files untouched throughout (`engine/mc_v3.py`, `market_profiles.py` etc. imported read-only). Script: `claude/v4_lab/lab_arm3_driftshrink.py` (session copy `/tmp/lab_arm3_driftshrink.py`).

## Harness validation

Rebuilt the Round 0-4 walk-forward harness independently (backtest_v3's own loop structure, imported not reimplemented, for HAR fit / simulation / scoring) to confirm it reproduces Round 0 before trusting a new candidate on it:

| | n windows (538 total) | DEV crps_skill | DEV cov90 | DEV PIT | DEV w90_ratio |
|---|---|---|---|---|---|
| Documented Round 0 | 447 DEV / 91 FINAL | +0.0322 | 0.890 | 0.539 | 1.074 |
| This harness, carry-only, same paths | 447 DEV / 91 FINAL | +0.0350 | 0.890 | 0.539 | 1.075 |

Window count matches exactly (538/447/91); cov90, PIT, and w90_ratio match to 3 decimals; crps_skill is within 0.003. Harness confirmed faithful — **no break-filter is applied inside `backtest_v3` itself** (it uses whichever `df` is passed and the profile's fixed `(nu, width_cal)` throughout); the 2022-03-21 break cut only enters the offline MLE that fits those constants, not the walk-forward backtest. Matching that (unfiltered history, fixed nu=4.0/width_cal=0.972) is what reconciles the window count.

## Candidate construction

```
own_mean_i(origin)  = expanding-window mean daily log return, close[0..origin]
                       (identical construction to mc_v2.backtest's retired "secular_drift")
grand_mean(date)     = LONO cross-sectional mean of other names' own_mean, asof date,
                       requiring >=130 sessions of their own history
mu_i(origin, w)      = grand_mean(date) + w * (own_mean_i(origin) - grand_mean(date))
drift_i(origin, w)   = mu_i(origin, w) * horizon
```

w=0 → fully pooled panel trend, zero per-name individuality. w=1 → raw unshrunk own-name trend (the already-RETIRED estimator). Shape (HAR vol forecast, nu, width_cal) held fixed at production values throughout — this is a center-only candidate, per the survey's own framing that MC families are shape technology and the center is a separate, freely-chosen input. Benchmark unchanged (carry-anchored lognormal RW). w swept on DEV only (447 windows, origin date < 2025-07-01); binding anti-overfitting protocol reserves the FINAL window (91 windows, >= 2025-07-01) for a single shot at a genuinely promising candidate.

## DEV sweep result

| w | crps_skill | cov50 | cov80 | cov90 | PIT | w90_ratio | drift spread (noisy metric, ppt/yr) |
|---|---|---|---|---|---|---|---|
| baseline (carry) | **+0.0350** | 0.528 | 0.801 | **0.890** | 0.539 | 1.075 | 0 (no per-name center) |
| 0.0 | +0.0265 | 0.501 | 0.794 | 0.881 | 0.538 | 1.065 | ~0 (calendar-coverage artifact, not real individuality) |
| 0.1 | +0.0248 | 0.492 | 0.796 | 0.875 | 0.537 | 1.066 | — |
| 0.2 | +0.0225 | 0.486 | 0.794 | 0.877 | 0.537 | 1.066 | — |
| 0.3 | +0.0194 | 0.486 | 0.799 | 0.879 | 0.536 | 1.066 | — |
| 0.4 | +0.0157 | 0.472 | 0.794 | 0.879 | 0.535 | 1.067 | — |
| 0.5 | +0.0113 | 0.474 | 0.796 | 0.877 | 0.535 | 1.067 | — |
| 0.6 | +0.0062 | 0.459 | 0.796 | 0.877 | 0.534 | 1.068 | — |
| 0.8 | −0.0062 | 0.459 | 0.794 | 0.879 | 0.533 | 1.069 | — |
| 1.0 | −0.0213 | 0.447 | 0.792 | 0.875 | 0.532 | 1.070 | 20.9 |

Every single w loses to the carry baseline, in a clean monotonic dose-response — **even w=0 (no individuality at all, purely the panel's own pooled historical trend replacing carry) already gives up ~0.85pp of skill and 0.9 points of cov90.** More shrinkage toward the noisier per-name estimate (rising w) only compounds the loss. All 9 candidates still beat the dumb carry-anchored yardstick (crps_skill stays positive through w=0.6), but none comes close to what production's own carry-only drift already achieves on the identical windows — so this is not a viable *replacement*.

## Why it fails (mechanism, not just the verdict)

PIT is essentially flat across the whole grid (0.538 at w=0, 0.539 baseline, drifting only to 0.532 at w=1) — **this is not a directional mis-centering problem** like Round 4a's wrong-signed trailing-ERP (which pushed PIT from 0.539 to 0.617). The grand mean sits close to carry in *level*. What degrades is pure **added estimation noise**: any realized-return-based center — even a 30-name pooled average — carries real sampling variance over a panel with only 538 windows dominated by a handful of large devaluation episodes, whereas carry is a smooth, low-variance, exogenously-known policy-rate schedule. Swapping a low-noise anchor for a noisier empirical one, without widening the band to price in the added centering uncertainty (shape was deliberately held fixed, per the survey's shape/center separation), makes the forecast overconfident in a new way: skill and cov90 degrade together, monotonically, as w — and with it estimation noise — rises. This matches the survey's own caveat almost exactly: the literature's winning hierarchical-shrinkage study "showed essentially zero OOS point-forecast skill for the return center." On this panel, "essentially zero" rounds down to negative.

## Drift ledger, updated

Six families now dead: secular / unshrunk trend (retired), β×trailing-ERP (Round 4a FAIL — wrong-signed), zero-net cross-sectional momentum (Round 4b FAIL), vol-rank / low-vol anomaly (Round 4c FAIL), LHAR vol-asymmetry (Round 3 Arm 2 FAIL — vol-side, closed without a FINAL shot), and now **Bayes-Stein / hierarchical-shrinkage trend (Round 5 FAIL — closed without a FINAL shot, same discipline)**.

**Standing conclusion, now doubly confirmed:** carry is the best drift 5.5yr of EGX price data can support. Per-name individuality lives entirely on the vol/shape side (own-HAR width, w90 0.45–1.14 per Round 0), not the center. The MC Family Survey's own top-ranked, literature-motivated shortlist item has been built and tested, not just argued from priors — and it does not survive the walk-forward gate on this panel. The survey's shortlist items #2 (MSGARCH regime-switching, shape-side), #3 (GJR-FHS simulation substrate, shape-side) and #4 (conformal calibration wrapper) remain open and untested, but none of them touch the center/individuality question — per the survey's own structural point, no shape technology can. That question stays closed until the Calibration Ledger itself accumulates enough FV-anchored, graded cohorts to test against (the path forward already flagged in the Round 0-4 synthesis) — not from more trailing-price-only estimators.
