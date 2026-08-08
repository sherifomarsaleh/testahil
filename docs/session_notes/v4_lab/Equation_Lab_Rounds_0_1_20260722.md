# v4 Equation Lab — Rounds 0–4 (22 Jul 2026)

Goal (user directive): iterate on the engine equation to make cones more individualistic per stock, while keeping cov90 ≈ 0.90 on the 5–95 band, beating the carry-anchored RW ("dumb yardstick") on CRPS, and optimizing (narrowing) cone width. **User constraint (22-Jul): all testing is lab-only — no change to system data, engine files, fitted configs, or the website. Honoured throughout: every artifact lives in the session /tmp; production untouched.**

**Anti-overfitting protocol (binding):** candidates iterate freely on the DEV window only; the FINAL window is held out and each shortlisted candidate runs there ONCE, every attempt logged. Tuning against the full walk-forward repeatedly = the CRPS-selection sin (already REJECTED in the ledger). Split: origins < 2025-07-01 = DEV (447 windows), ≥ 2025-07-01 = FINAL (91 windows). Harness: `backtest_v3` + `pooled_scores` (engine/mc_v3.py), h=60, non-overlapping, use_signal=False (EG profile), nu=4.0, width_cal=0.972, 30 names, 538 windows total.

## Round 0 — production v3 baseline

| window | n | crps_skill | cov50 | cov80 | cov90 | w90/bench | mean w90 | per-name w90 range | w90 std |
|---|---|---|---|---|---|---|---|---|---|
| ALL | 538 | +0.0303 | 0.526 | 0.803 | 0.892 | 1.083 | 0.793 | 0.451 (COMI) – 1.140 (LCSW) | 0.161 |
| DEV | 447 | +0.0322 | 0.523 | 0.803 | 0.890 | 1.074 | 0.817 | 0.461 – 1.228 | 0.176 |
| FINAL | 91 | +0.0264 | 0.538 | 0.802 | 0.901 | 1.127 | 0.675 | 0.409 – 0.984 | 0.108 |

Baseline PIT mean: ALL 0.548, DEV 0.539, FINAL 0.591 — realized prices land above the carry median 53% of windows. Genuine mis-centering exists on the drift axis (motivated Round 4). Baseline rows: /tmp/lab_round0_v3.csv (session).

## Round 1 — factor-HAR dev sweep (λ = 0.25/0.50/0.75)

Factor: leave-one-out cross-sectional MEDIAN of the 30 names' daily YZ variance. dv_mix = (1−λ)·dv_own + λ·b²ᵢ·dv_market, b²ᵢ = trailing-252d mean(v_i)/mean(factor). DEV: skill flat (+0.0322→+0.0319), cov90 ~0.886–0.888, width −1.3% at λ=0.75, per-name w90 std 0.176→0.159 (HOMOGENIZES — not the individuality lever). λ=0.75 shortlisted as marginal sharpness tweak.

## Round 2 — width-refit procedure REJECTED (validation failure)

Attempted per-arm width_cal refit by MLE (t(ν) scale, then joint (ν,c)) on DEV h=60 standardized window residuals. **Validation on the BASELINE's own dev residuals returned ν≈4.3, scale≈0.71 — i.e., the procedure calls even production "over-wide," yet empirical cov90 at production width is 0.890.** The h=60 window residuals are not t-shaped (peaked core + heavier tails from per-window vol estimation noise); MLE fits the core and destroys coverage (arm at refit width: cov90 0.80). **Standing lesson: do NOT fit width_cal by MLE on h-horizon window residuals — production's pooled LONO-cross-fitted procedure is not equivalent and must be used as-is. Lab candidates inherit production (ν, width_cal) unchanged.**

## Round 3 — vol-side FINAL verdicts

**ARM 1 — factor-mix λ=0.75 @ production calibration. FINAL (single run, logged): FAIL.**
| FINAL window | crps_skill | cov90 | w90 |
|---|---|---|---|
| baseline v3 | +0.0264 | 0.901 | 0.675 |
| factor-mix | +0.0157 | 0.879 | 0.662 |
Dev flatness did not transfer — gave up ~1.1 points of skill and coverage on the held-out year. REJECTED, do not revive without new evidence.

**ARM 2 — LHAR (leverage asymmetry), honest walk-forward (coefs refit per origin on prior data only, response capped at in-sample p99.5, 20k paths/window, production calibration). DEV: FAIL — never earned a FINAL shot.**
| DEV window | crps_skill | cov90 | w90 | per-name w90 std |
|---|---|---|---|---|
| baseline v3 | +0.0322 | 0.890 | 0.817 | 0.176 |
| LHAR | **−0.0118** | 0.937 (over) | 1.124 (+37%) | 0.402 |
Walk-forward LHAR inflates vol (s2/2 correction + feedback on origin-limited fits), over-covers, and drops below the dumb yardstick. Consistent with the immateriality finding in claude/lhar/ — conclusively CLOSED by the test itself.

## Round 4 — data-only per-name DRIFT (user constraint: NO fair-value contamination). ALL THREE FAILED DEV.

**4a — β × market-premium: FAIL.** β_i from weekly own-vs-LONO-panel regression (tier-1 style, clip [0, 2.5], p10–p90 spread 0.36–1.31); ERP = trailing 3-yr panel median weekly excess return vs carry, walk-forward. Root cause of failure: the trailing ERP estimate is persistently NEGATIVE (median −25.1%/yr — panel's past median return sat below the ~20% EGP rf), so the tilt pushed medians DOWN while realized prices ran UP; PIT worsened 0.539→0.559/0.579/0.617 at shrink 0.25/0.5/1.0; skill fell monotonically (+0.0252/+0.0146/−0.0167 vs +0.0322). **The mis-centering is forward-looking; a trailing estimator points backward. Textbook drift-estimation trap.**

**4b — zero-net cross-sectional momentum (12-1, relative to LONO panel median, tilt capped ±0.15): FAIL.** Skill degrades monotonically (+0.0309/+0.0257/+0.0096 at shrink 0.1/0.25/0.5 vs +0.0322); pooled PIT unmoved at 0.538 — by construction a zero-net tilt cannot fix a market-level mis-centering, and the cross-sectional ranking itself carries no CRPS signal on this panel (consistent with the TA-signal ablation).

**4c — vol-rank drift (low-vol-anomaly sign, tilt = −s·volrank·20%/yr): FAIL.** +0.0315/+0.0294/+0.0215 at s=0.25/0.5/1.0, all below baseline; PIT drifts the wrong way (0.543–0.555).

**Drift ledger now: secular (retired), unshrunk trend (retired), β×trailing-ERP (failed dev), zero-net momentum (failed dev), vol-rank (failed dev). Five families dead. Standing conclusion: carry is the best drift 5.5yr of EGX price data can support. The residual PIT≈0.55 is the price of not gambling on regime persistence — it is not harvestable from trailing price data, and per the user's purity constraint it must NOT be harvested from our own fair values. It becomes testable only as the Calibration Ledger accumulates FV-anchored cohorts.**

## Session synthesis (rounds 0–4 complete)

Production v3 beat every challenger on every axis: vol level (already per-name — THE source of cone individuality, w90 0.45–1.14), tail shape (homogeneous), asymmetry (fails the yardstick), factor structure (fails FINAL), and all three data-only drifts (fail dev). The engine's per-name individuality is real and lives where the data supports it — in each stock's own volatility dynamics. Multiplicity note: ~12 dev-window candidate-configs were examined across rounds 1–4 (all logged above); only one FINAL-window shot was ever taken (ARM 1) and it failed — the FINAL window remains clean for future candidates.

## Presentation fix (standing)
For the "conformity" optics: show the per-name panel spread (COMI 22.7% … KABO 45.3% 1-yr mean EV; w90 0.45–1.14) instead of vol-twin pairs like ISPH/ORHD.
