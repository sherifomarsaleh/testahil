# MC v4 ("Per-Stock Drift + Optimized Width") — tested and REJECTED

**Date:** 26-Jul-2026
**Object under test:** externally-submitted `mc_v4.py`, "MC v4 Engine — Per-Stock Drift + Optimized Width"
**Panel:** the live EG library, `engine/raw_ohlc/EG` — all 30 names
**Verdict:** **REJECTED — do not revive.** Fails the standing Step 0 gate outright, and fails head-to-head against production v3. Its two headline ideas contribute nothing once the arithmetic is repaired.

---

## 1. Headline result

Walk-forward, non-overlapping, h=20, scale-normalised CRPS (`crps/spot`), scored against the
standing carry-anchored lognormal RW null, calendar-block bootstrap 90% CI, 30 names, 1,603 origins,
all after the Step 0.0 data-quality gate.

| arm | CRPS skill vs null | 90% CI | verdict | cov90 | std_u | w90 / null |
|---|---|---|---|---|---|---|
| V3 production (nu=4.0, cal=0.972) | **+0.0087** | [+0.0028, +0.0153] | **PASS** | 0.893 | 0.992 | 1.05 |
| **V4 as written** | **−0.0493** | [−0.0767, −0.0265] | **FAIL** | 0.953 | 0.783 | 1.59 |
| V4, scale bugs repaired | +0.0126 | [−0.0006, +0.0245] | PARITY | 0.883 | 1.123 | 1.01 |
| V4, repaired + carry anchor | +0.0083 | [+0.0014, +0.0152] | PASS | 0.877 | 1.124 | 1.00 |
| carry-anchored RW (null) | 0.0000 | — | — | 0.872 | 1.125 | 1.00 |

Head-to-head against what is live today:

| arm | skill vs V3 | 90% CI | verdict |
|---|---|---|---|
| V4 as written | −0.0585 | [−0.0885, −0.0321] | **FAIL** |
| V4, repaired | +0.0039 | [−0.0082, +0.0157] | PARITY |
| V4, repaired + carry | −0.0004 | [−0.0045, +0.0035] | PARITY |

Per name, v4 as written is **beaten by a plain random walk on 17 of 30 names** (production v3: 7 of 30).
Its median per-name cov90 is 0.959 against a 0.900 target, and 16 of 30 names sit at cov90 ≥ 0.95 —
the same over-coverage pathology the adaptive-width work was built to cure, except a factor of three larger.

Two things make this result stronger than it looks. First, v4 was run with **full-sample parameters**
— nu, sigma, mu and omega all fitted on data that includes the scoring window. It was given look-ahead
and still failed. Second, the arm that finally passes the gate is the one where v4's own drift has been
deleted and replaced by the production carry anchor — at which point it is statistically indistinguishable
from v3 (−0.0004, CI straddling zero). **Every point of skill in the best v4 arm comes from the piece
borrowed from v3. Neither of v4's two headline contributions survives.**

---

## 2. Eight defects, each verified numerically

### 2.1 nu is algebraically cancelled out of the width calibration — *fatal*

```python
pred_upper = mu_d*h + q95_ref * sigma_h / (q_range_ref / 2)
```
`q_range_ref = q95 − q05`, and the Student-t is symmetric, so `q_range_ref/2 = q95` exactly and the
whole factor reduces to `+1.000` for every nu from 2.2 to Gaussian (verified to six decimals).
The calibration band is always `mu_d*h ± 1.000·sigma_h`. The fitted nu never touches omega; the entire
Student-t apparatus is inert in the one step it was written to serve. Worse, a ±1σ band is ~68% under
normality but is being solved to cover 90%, so omega silently absorbs a spurious ~1.6× inflation factor.

### 2.2 `stats.t.rvs()` is not standardised — *fatal*

`Var[t_nu] = nu/(nu−2)`, not 1. The simulator writes `mu_d + omega*sigma*innov` with a raw t draw, so
the realised conditional sd is `omega·sigma·sqrt(nu/(nu−2))`. The inflation is nu-dependent, so it
varies invisibly from name to name. At the configured `nu_min = 2.1` the t has infinite variance.
Production v3 gets this right via the chi-square mixture `sqrt((nu−2)/chi)`, which is unit-variance by construction.

### 2.3 Calibration and simulation use different variance laws — *fatal*

Calibration: `var_h = (omega·sigma)² · h · (1 + 0.7(h−1)/h)`. Simulation: a sum of h daily draws from
the AR(1) sigma recursion. The band the simulator actually produces, divided by the band omega was
solved to make cover 90%:

| nu | h=1 | h=5 | h=10 | h=20 |
|---|---|---|---|---|
| 4 | 2.13 | 1.80 | 1.79 | 1.78 |
| 14 | 1.76 | 1.42 | 1.39 | 1.37 |
| 20 | 1.73 | 1.39 | 1.36 | 1.34 |

Omega is fitted against one distribution and applied to a different one, 1.3× to 1.8× wider. This is
the direct cause of the published cone being 59% wider than the RW null, and of the script's own
yardstick reporting 100% coverage on 26 of 30 names.

### 2.4 The James-Stein shrinkage is inverted

James-Stein is `mu_JS = grand + (1−c)(mu_i − grand)` with `c = (k−3)·var/dispersion`. The code sets
`lambda = 1 − c` and then multiplies by `(1 − lambda)`, i.e. by `c` — the shrinkage factor and its
complement are swapped. The consequence is exactly backwards: the *stronger* the cross-sectional
signal (large dispersion → small c), the *harder* it shrinks. On the live EG panel every one of the
30 names reported λ = 0.95, the clip ceiling, keeping 5% of its own drift. **Raw drifts spanning
10.5%–61.0% p.a. are compressed to 30.8%–33.3%** — a 50pp spread flattened to 2.5pp. Correct JS on
this panel would have retained ~95%+ of each name's own estimate. The feature advertised as
"per-stock drift" delivers, in practice, one pooled number for the whole market.

### 2.5 The drift is a retired construct regardless

Even repaired, `mean(log returns) × 252` is raw secular historical drift, explicitly **RETIRED
(do-not-revive)** under the standing protocol. On EGX across the devaluation window it books ~32%/yr
of realised past appreciation as a forward expectation — roughly +2.6% of median drift over every
20-day cone. There is no rf, no dividend yield and no carry anywhere in the file, so the model cannot
be scored against the carry-anchored null on equal terms: any apparent skill would be drift luck, which
is precisely what the carry anchor exists to prevent.

### 2.6 Off-by-one in the calibration target

`actual = np.sum(returns[t : t+h+1])` sums h+1 returns against an h-day forecast band. At h=1 the
realised object carries 41% more sd than the forecast it is scored against, biasing omega upward;
the bias shrinks with h but never vanishes and is pooled across h.

### 2.7 The "dumb yardstick" is in-sample and time-reversed

The simulation is launched from the last close and covers T+1…T+20. `actual_rets =
df['log_return'].values[-20:]` is T−19…T. **The realised path it scores against ends where the
forecast begins.** It is not out-of-sample and it is not even the right 20 days. It is also 20
overlapping cumulative points from a single realisation, so the statistic can only take values k/20
and has an effective sample size near 1. "Passed: 2/30" carries no information in either direction.

### 2.8 nu is fitted on the wrong object, and pre-trimmed

Two compounding errors. (a) The 6×MAD pre-trim deletes exactly the tail observations nu exists to
measure — on COMI it discards 19 points and lifts nu from 9.8 to 18.9. (b) nu is fitted on
*unconditional* returns but used as the *innovation* df on top of a time-varying sigma; volatility
clustering and fat tails are different objects, and production correctly fits nu on cross-fitted
residuals. Across the panel the script returns nu ∈ [14.1, 22.3], median 18.4, against **EG's
LONO-cross-fitted production value of 4.0**. It is reporting near-Gaussian tails for the fattest-tailed
market in the system.

### 2.9 No Step 0.0, and silent no-op fallbacks

There is no data-quality gate. `clean()` interpolates up to 5 missing prices with
`limit_direction='both'` (fabricating prices, including backfill at the series start) and then computes
returns across the fabricated stretches. Run on the raw library the script books a **+2,696% one-day
move in EFIH as volatility**, producing sigma_ann = 163.5%; EGX has a hard ±20% daily limit, so that
move is a corporate action or a vendor error and can never be a trade. The production Step 0.0 gate
back-adjusted three names (DSCW, EFIH, OCDI) on this same panel.

Separately, `calibrate_width` returns `(1.0, nan)` whenever n < 1310 and raises nothing. Five of 30
EG names (EFIH, PRDC, OCDI, EMFD, TMGH) take that path: they are published **uncalibrated**, with the
only trace an "N/A" in a column a reader skims past. That violates the no-silent-caps rule.

---

## 3. Is the underlying idea salvageable?

Two ideas were on offer. Both were tested with the arithmetic repaired.

**Per-stock drift — no.** It is a retired construct, it is unanchored to carry, and the shrinkage
that was supposed to discipline it runs backwards. Replacing it with the production carry anchor is
what moves the repaired model from PARITY to PASS. The drift is not a contribution; it is a drag.

**Per-stock width — no, and it is already in the engine, done properly.** With the scale bugs fixed,
per-name omega collapses to a 0.72–1.19 range (from the 0.83–2.96, 3.6× spread the script produces),
the cone width converges on the RW null at 1.00×, and the skill lands at PARITY against both the null
and v3. std_u actually *degrades* to 1.123 versus v3's 0.992 — the per-name width machinery is worse
calibrated in shape than v3's HAR, not better. Meanwhile `engine/adaptive_width.py`, adopted 23-Jul-2026,
already implements the per-name width idea the right way: an online multiplier learned from each name's
own resolved residuals, gentled and dead-zoned, shrunk toward the pooled market fit, history-gated at
MIN_WINDOWS=28, and cleared through the same LONO gate at proper-score parity with a genuine
`|std_u − 1|` improvement of 0.096 → 0.069.

The v4 approach is the version of that idea that the promotion rule already rejected once: selecting a
per-name parameter by maximising an in-sample fit criterion. It is the same failure mode as the
CRPS-selection experiment — better in-sample, no better out of it. Coverage is additionally not a proper
scoring rule; a distribution can hit 90% coverage while being arbitrarily mis-shaped, which is why v4
can report cov≈0.90 in its own calibration table and still lose to a random walk on 17 of 30 names.

---

## 4. Protocol compliance

| Gate | Result |
|---|---|
| Step 0.0 data-quality gate | **absent** — no per-market limit screen, no corporate-action back-adjustment; ingests a +2,696% print as volatility |
| Step 0 calibration gate | **FAIL** — −0.0493, CI [−0.0767, −0.0265], entirely below zero |
| Carry-anchored benchmark parity | **absent** — no rf, no q, no carry anywhere in the file |
| Promotion rule (survive the same OOS test) | **FAIL** — loses to production v3 by −0.0585 even with look-ahead parameters |
| No silent caps | **violated** — 5 of 30 names silently uncalibrated |
| Unit-variance innovations | **violated** — raw `t.rvs`, nu-dependent inflation |
| Horizon | h=20 only; the standing gate is h=60 |

---

## 5. Recommendation

Do not adopt, and do not adopt any part of it. Log alongside
`Amihud_DynamicDoF_Walkforward_REJECTED_20260723.md` and `Gemini_ACI_HARQ_SkewT_REJECTED_20260726.md`.

The one item worth carrying forward is not from the model but from the exercise: the failure signature
here — a per-name width parameter selected to hit a coverage target on its own sample, producing a
3.6× spread across a single market and over-coverage on more than half the panel — is the same
signature the adaptive-width overlay was designed around. It is further evidence for keeping that
overlay history-gated and shrunk toward the pooled fit rather than letting per-name width float free.

**Reproduction:** `mc_v4.py` (submitted code, only the file-path block changed to point at
`engine/raw_ohlc/EG`), `diagnose.py` (the eight defect proofs), `g_params.py` / `g_score.py` /
`report.py` (the five-arm gate). All parameters and per-origin scores retained in `params.csv`,
`rows.csv`, `pername.csv`.
