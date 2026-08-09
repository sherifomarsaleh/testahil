# Gemini "ACI-HARQ-SkewT" MC proposal — REVIEWED, RUN, REJECTED (26-Jul-2026)

**Verdict: REJECTED. Do not revive.** Robust FAIL on both markets tested, under the
standing gate (Step 0.0 cleaned data, non-overlapping h=60, scale-normalized CRPS vs
the carry-anchored lognormal RW, block bootstrap {2,3,4}). Beat production in **0 of 30**
EGX names and 3 of 11 Tadawul names. This is a rejection on evidence, not on style.

Artifacts: `/tmp/mcrev/headtohead.py`, `instrument.py`, `salvage.py`,
`h2h_EG.csv`, `h2h_SA.csv`, `salvage_EG.csv` (session-local; numbers reproduced below).

---

## 1. It fails its own self-test

Ran `run_calibration_sweep` unmodified on the 30-name EGX library. It targets 90%
coverage; it delivers a mean of **82.6%**, and only 10/30 names clear its own already-
lowered 85% "PASSED" bar. The conformal factor Q ends at **1.4–5.4** (mean 3.3) — the
outer tails need 2–5× stretching just to get that far, which is the signature of a
badly under-dispersed core, not of a well-specified one.

Separately: the sweep is **unseeded** (`np.random.randn`, `chi2.rvs`), so it is not
reproducible run-to-run. The house engine is seed=42 throughout.

## 2. The head-to-head, under the real gate

Identical cleaned data, identical origins, identical benchmark draws, identical 20,000
paths per arm. Only the forecast distribution differs. My re-implementation of
`generate_cone` (injectable RNG) matches the original to **0.4% max** on p05/p50/p95.

| Arm | EG skill | CI | Verdict | SA skill | CI | Verdict |
|---|---|---|---|---|---|---|
| **PROD** mc_v3, live profile | **+0.0199** | [+0.0132,+0.0271] | PASS | **+0.0023** | [-0.0035,+0.0082] | PARITY |
| **GEM** as written | **−0.0837** | [−0.1036,−0.0641] | **FAIL** | **−0.0264** | [−0.0477,−0.0056] | **FAIL** |
| GEM + carry drift substituted | −0.0249 | [−0.0373,−0.0118] | FAIL | −0.0348 | [−0.0522,−0.0174] | FAIL |
| GEM with q_tail pinned at 1.0 | −0.0850 | [−0.1053,−0.0653] | FAIL | −0.0271 | [−0.0483,−0.0060] | FAIL |

EG: 479 windows / 30 names. SA: 190 windows / 11 names.
PROD's +0.0199 reproduces the committed EG panel figure (+0.0204) — the harness is sound.

Calibration: PROD cov90 **0.889** on a 0.781 mean band; GEM cov90 **0.791** on a 0.657
band. GEM is not "a tighter cone that pays for itself" — it is a **narrower cone that
misses more often**, which is the worst quadrant. Its band is also narrower than the
naive RW benchmark's (0.770), while scoring worse than it.

**GEM has negative skill — i.e. is worse than a plain carry-anchored random walk — in
28 of 30 EGX names and 8 of 11 Tadawul names.**

## 3. Why it fails — four concrete defects

**(a) The "HARQ" block is not HARQ, and it is biased ~46% low.**
`quarticity = recent_vols ** 2` is *variance*, not realized quarticity. Weighting by
`1/(σᵢ²)` and then averaging σᵢ² returns the **harmonic mean** of the nested-window
variances — an estimator mathematically pinned at-or-below the smallest window's
variance. Measured over 474 EGX windows: the raw output is **0.540×** the realized
forward 60-day vol (median). The `i=1` term is a single day's `|r_{t−1}|`, and when
yesterday was quiet it takes >90% of the weight (6.8% of windows) — so the estimator
degenerates to yesterday's absolute return. The arbitrary `0.5 × trailing-60d` floor
binds in **43.9%** of windows, which is the only thing keeping it usable.

Real HARQ (Bollerslev–Patton–Quaedvlieg) uses realized quarticity to *attenuate the HAR
coefficient on the daily term* when it is noisily measured. It does not inverse-variance-
weight nested windows. This is a different estimator wearing the name.

**(b) The t(5) shocks are never renormalized to unit variance.**
`t_shocks = Z / sqrt(V/5)` has sd `sqrt(5/3) = 1.291`, so `daily_vol × t_shocks` produces
a cone **1.30× wider than `daily_vol` claims**. Production's `simulate_terminal_v3` handles
this correctly with `mix = sqrt((nu−2)/chi)`.

Two bugs partially cancel: 0.540 (low vol) × 1.30 (un-normalized t) × the floor lands at
**0.828×** realized. Still ~17% too narrow — and cancelling errors is not calibration.
The reported "HARQ Vol" column in `Master_Audit_Table.csv` is therefore wrong on its face:
it prints `daily_vol × √252`, but the cone is actually drawn 30% wider than that.

**(c) The drift is uncarried, and gated off 86% of the time.**
The Hurst gate (`H > 0.55`) is closed in **85.6%** of EGX windows, so the forecast is
centred at **zero log drift**. Egypt's carry anchor is `ln(1+rf) − ln(1+q)` ≈ **+4.24%
over 60 sessions** at rf 19.50%. Centring at zero is an implicit, unstated forecast that
every EGX name underperforms T-bills by ~4% a quarter. When it *does* fire, it injects a
scaled raw historical mean — which is exactly the **raw secular drift** the protocol has
on the do-not-revive list.

Substituting the production carry into GEM lifts it from −0.0837 to −0.0249. So roughly
**70% of the damage is the missing carry anchor**; the remaining 30% is the variance
machinery. Both are still FAIL.

**(d) The ACI conformal layer buys essentially nothing, and its self-reported coverage
is circular.** Pinning `q_tail = 1.0` moves EG skill by 0.0013 and SA by 0.0007 — noise.
It only stretches mass beyond p10/p90, so p25/p50/p75 are untouched (the ledger publishes
those), and it leaves a density kink at the splice. It also cannot fix mis-centring, which
is this design's actual problem. Worse, in the original sweep the "Coverage %" is measured
*while* `q_tail` adapts on the same pass — an in-sample number an adaptive method is
built to hit. Coverage is not a proper score in any case: a cone can hit 90% by being
absurdly wide. **The code contains no benchmark and no proper score anywhere.**

Structural: the sweep steps origins by 5 days at h=60, so forecasts overlap ~12×. The
reported `total` overstates the effective sample size by roughly an order of magnitude,
and it delays the ACI feedback loop by 12 updates, which is why Q hunts at 2–5 instead
of settling.

## 4. Also missing vs. house standards

- No Step 0.0 data-quality gate. On this same library that gate found EFIH pre-IPO
  placeholder rows and an unadjusted 3:2 split, plus OCDI's unadjusted corporate action.
  The Gemini sweep would ingest all of it and read a fake −73% day as a real tail.
- No break handling, no per-market anything, no dividend yield.
- `except Exception: print(...)` swallows every failure into a skipped row.
- The published p05/p95 come from a distribution whose interior was never calibrated.

## 5. Salvage — the one idea worth testing, tested

The skew-t core is the only component with a defensible motivation. Tested honestly:
production mc_v3 unchanged (same HAR width, same carry, same nu=4.0, same width_cal=0.972),
swapping **only** the terminal shock shape for an Azzalini skew-t at unit variance, with
`alpha = clip(2 × trailing-252d skew, ±2)`:

| | EG skill | CI | Verdict |
|---|---|---|---|
| PROD as shipped (symmetric t) | +0.0199 | [+0.0132,+0.0271] | PASS |
| PROD + skew-t shape overlay | **+0.0187** | [+0.0115,+0.0258] | PASS |

Paired delta +0.000181 (slightly worse); the skew arm wins **50.7%** of windows — a coin
flip. Under the promotion rule this does not enter the engine. Caveat stated plainly: a
fully fair test would re-fit (nu, width_cal) jointly with the skew under LONO, since a
skewed shape and the pooled width trade off. That refit is only worth running if something
better-motivated than "2× the trailing sample skew, clipped at ±2" is on the table — the
alpha here is at its ±2 clip in 21.5% of windows, which is a sign the driver is noise.

## 6. What this does not say

The proposal's *diagnosis* is not crazy — a name-level, adaptive width is a real gap, and
it is the same gap `engine/adaptive_width.py` was adopted for on 23-Jul-2026 (EG-only,
history-gated, currently dormant). The difference is that adaptive_width learns a
multiplier from each name's own **resolved 60-day residuals** and cleared the LONO gate at
parity-or-better on the proper score. This proposal reaches for the same goal through an
online tail stretch bolted onto a downward-biased variance estimate and an uncarried drift,
and loses to a plain random walk.

**Standing precedent recorded: an engine change is not adopted because its coverage
number looks reasonable. It is adopted because it survives the same out-of-sample proper-
score test the forecasts survive. This one does not.**
