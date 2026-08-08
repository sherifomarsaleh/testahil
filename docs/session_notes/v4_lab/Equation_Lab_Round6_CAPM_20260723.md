# Equation Lab — Round 6: CAPM Level-Fix + Illiquidity Tilt (23-Jul-2026)

**Trigger:** direct response to the "carry is one-size-fits-all and that's unrealistic" pushback. Six prior drift families (secular/unshrunk trend, β×trailing-ERP, zero-net momentum, vol-rank, LHAR, Bayes-Stein shrinkage — Rounds 3–5) all failed because they re-sliced the *same* noisy trailing-return series. This round deliberately used two data sources never touched before: (1) beta/CAPM theory + an **exogenous** ERP, (2) trading volume (Amihud illiquidity). **Result: one real, positive, validated finding — but it is a level fix, not a per-name individuality fix — plus one inconclusive lead. Reported straight, not oversold.**

## Finding 1 — CAPM level-fix: REAL, but decomposes to level, not beta

Candidate: `drift_i = carry + s*(Ke_i - carry)`, `Ke_i = rf* + beta_i * ERP`. `rf*`/ERP from `Cost_of_Capital_Reference.md`'s already-sourced Damodaran Egypt row (CDS-basis: rf*=18.91%, ERP=9.41%; rating-basis: rf*=15.94%, ERP=13.94% — both tested, near-identical results). Beta: walk-forward weekly regression, own return vs an equal-weighted proxy of the same 30-name panel (no EGX30 index series was obtainable in this environment — checked project files, uploads, repo; only a 49-day ad hoc proxy existed from an earlier study, too short to reuse — this substitution is a flagged simplification), same usability gate as `wacc_builder.py` (n≥24, R²≥5%, SE(β)<|β|; else fallback β=1.0). Shape unchanged.

DEV sweep (447 windows), s = 0 → carry only, s = 1 → full Ke:

| s | crps_skill | cov90 | PIT | w90_ratio |
|---|---|---|---|---|
| 0.00 (baseline) | +0.0293 | 0.890 | 0.539 | 1.076 |
| 0.25 | +0.0326 | 0.893 | 0.533 | 1.082 |
| 0.50 | +0.0356 | 0.895 | 0.527 | 1.087 |
| 0.75 | +0.0383 | 0.897 | 0.520 | 1.093 |
| 1.00 | +0.0407 | 0.897 | 0.514 | 1.099 |

Clean, monotonic improvement on **all three axes at once** — skill up ~0.011, cov90 moving toward the 0.90 target from below, PIT moving toward the ideal 0.50 from 0.539. This is the first candidate in six rounds to do that. Mechanism: Round 0 already flagged "genuine mis-centering... realized prices land above the carry median 53% of windows" — carry (a policy-rate anchor) omits any equity risk premium; Ke reintroduces one from a properly-sourced, non-trailing input.

**Decomposition check (the one that matters):** re-ran s=1.0 with beta forced to a flat 1.0 for every name (zero cross-sectional differentiation) against the real, per-name regression beta:

| variant | crps_skill | cov90 | PIT |
|---|---|---|---|
| flat beta=1.0 for all (pure level shift) | +0.0440 | 0.893 | 0.514 |
| real per-name beta (level shift + differentiation) | +0.0449 | 0.897 | 0.514 |

Gap: +0.0009 — inside noise. Per-name, `corr(beta, real_minus_flat) = -0.31`: names with higher beta do **not** coherently benefit more from getting their own beta vs. the flat assumption (e.g. HELI β=1.40 is *worse off* with its real beta; ABUK β=0.57 is *better off*). **Verdict: essentially all of the gain is the level correction (carry → a risk-premium-bearing anchor). The beta-based differentiation itself adds nothing distinguishable from noise.** Same underlying lesson as every prior round, arrived at through a different door: this panel's cross-sectional return structure does not support per-name drift differentiation from anything tested so far — but the *aggregate* carry-only level does appear to be measurably too low, and fixing that is a real, separate, workable improvement.

**Caveat, stated plainly:** rf*/ERP are a single Jan/Jul-2026 snapshot applied uniformly across the full 2016–2026 backtest, unlike `carry_schedule` which is a genuine historical policy-rate time series. This is the same kind of gate-neutral backtest simplification the codebase already accepts elsewhere (breaks, carry schedules) but has not been stress-tested here — a mildly favorable snapshot could be inflating the win. **No FINAL-window shot has been taken on this candidate.** Recommend either (a) spend it now accepting the caveat, or (b) build a proper historical Egypt ERP/rf* schedule first (Damodaran vintages are dated, so this is buildable, just not done yet) and re-run DEV before committing the one FINAL shot.

## Finding 2 — Amihud illiquidity tilt: inconclusive, not adopted

First-ever use of volume data (not price/return) as a drift input: trailing 252d illiquidity = mean(|daily return| / EGP volume), cross-sectionally z-scored, tilt = `z * annual_rate`, added to carry.

| tilt (ann./z) | crps_skill | cov90 |
|---|---|---|
| 0.00 | +0.0233 | 0.890 |
| +0.02 | +0.0250 | 0.890 |
| +0.05 | +0.0264 | 0.886 |
| +0.08 | +0.0262 | 0.888 |
| +0.12 | +0.0236 | 0.890 |
| −0.05 (wrong sign, sanity check) | +0.0159 | 0.888 |

Peaks at tilt≈0.05 then declines — a peak-and-reverse shape, not a monotonic or plateauing one, which is the signature of noise, not a real effect (and picking the grid peak would be exactly the CRPS-selection-by-maximization move already REJECTED in the ledger for a different candidate). The wrong-sign check at least confirms the theoretical direction (illiquid → higher return) beats the reverse, but the effect is too small and too grid-shaped to trust. **Not adopted. Would need a walk-forward-safe cross-sectional standardization (this pass pooled the full DEV sample to z-score, a simplification) and a principled — not grid-searched — tilt size before it's a real candidate.**

## Standing conclusion, updated

Per-name drift individuality remains unsupported by every angle tested so far — trailing-return-based (six ways) and now beta-based (one way, cleanly decomposed and ruled out). What *is* now supported: **the common carry-only anchor is measurably too low relative to what a risk-premium-bearing anchor achieves**, a market-wide (not per-name) fix that is new, real, and actionable pending the ERP-schedule caveat above. Illiquidity is a genuinely fresh, untested-elsewhere data axis with a marginal, inconclusive first read — the most promising thread left to pull if per-name individuality is still the goal, but it needs a cleaner, non-grid-searched test before it means anything.

## Addendum (same day) — real EGX30 index supplied; verdict re-tested and CONFIRMED

Sherif provided the actual EGX30 daily OHLC (2011–2026, ~3,740 rows). Kept session-side (an index is not a covered name; `engine/raw_ohlc` placement stays a human decision). Betas recomputed against the real index (walk-forward weekly, same usability gate, 505/538 windows on own regression): they differ materially from the panel-proxy betas — corr only 0.588; COMI 0.64→1.21 (the equal-weighted proxy buried COMI's index dominance), RAYA 1.47→0.78. Re-run with deterministic crc32 seeds (the salted-hash seeds of the first attempt triggered a −8.1 skill blowup that became the tail-instability finding — see `MC_TailInstability_BlockMix_20260723.md`):

| variant (DEV, 447 windows) | crps_skill | cov90 | PIT |
|---|---|---|---|
| carry only | +0.0314 | 0.890 | 0.539 |
| flat β=1.0, s=1.0 (level only) | +0.0418 | 0.890 | 0.514 |
| REAL-INDEX β, s=1.0 | +0.0405 | 0.893 | 0.517 |

Per-name beta gain vs flat: −0.0013 pooled; 16/30 names helped (coin flip); corr(β, gain) = −0.073. **Verdict unchanged and strengthened against the genuine index: the CAPM improvement is entirely the level correction (carry → risk-premium-bearing anchor); per-name beta differentiation of the center adds nothing.** The seed-noise finding (±~0.5pt on pooled skills at 20k paths) means the +0.010-order level gain should be re-confirmed with paired seeds before the FINAL shot — the runs above ARE paired (shared per-row seeds), so the deltas quoted here are clean.
