# Gemini MC proposal — PART 2: REPAIRED AND RE-TESTED (26-Jul-2026)

Companion to `claude/v4_lab/Gemini_ACI_HARQ_SkewT_REJECTED_20260726.md` (Part 1: review + as-submitted head-to-head). Read that first.

Sherif's follow-up was the right challenge: *"if the idea is good, fix the bug and
re-run."* Done. All four defects repaired, re-run under the same gate, with each
component isolated so the credit lands where it belongs.

Artifacts: `/tmp/mcrev/repaired.py` (pass 1, expensive), `score_arms.py` (pass 2),
`lono.py` (LONO + block-robustness), `comp_{EG,SA}.csv`, `arms_{EG,SA}.csv`.

## The repairs

| # | Defect | Repair |
|---|---|---|
| a | harmonic-mean-of-nested-variances masquerading as HARQ, 0.54× realized | **true HARQ (Bollerslev–Patton–Quaedvlieg)** — HAR on daily/weekly/monthly variance with the *daily* coefficient attenuated by measured realized quarticity. RQ proxied as `(n/3)·Σvᵢ²` over 5 days on the YZ per-day variance proxy. Two variants: levels and log-space. |
| b | t(5) shocks with sd √(5/3)=1.291 | unit-variance mixture `√((ν−2)/χ²)`, skew-normal core renormalized *after* the mixture |
| c | Hurst-gated raw drift, zero 86% of the time | carry anchor `ln(1+rf) − ln(1+q)`, identical to production |
| d | tail-only ACI on an in-sample pass | **full-cone width multiplier, walk-forward** (only resolved windows). Two learners: multiplicative ACI on coverage misses, and shrunk running RMS of standardized residuals — the latter both per-name and pooled at market level |
| + | no data-quality gate | Step 0.0 applied to every series |

Repair (a) worked: median σ_h goes from 0.54× realized to **0.2409 (levels) / 0.2373
(log)** vs production's 0.2383 — the estimator is now in the right place.

**Fairness:** every arm, *including production*, gets its own (ν, width_cal) refitted by
the same pooled MLE (`fit_nu_scale` → `shrink_cal`) on its own residuals. No arm is
penalised for being uncalibrated, and PROD does not carry its shipped advantage.

## Results — EG (479 windows / 30 names)

| Arm | ν | cal | skill | CI | verdict | vs PROD (paired, block=3) |
|---|---|---|---|---|---|---|
| PROD log-HAR | 4.0 | 0.965 | +0.0195 | [+0.0127,+0.0266] | PASS | — |
| R1 true HARQ, **levels** | 4.0 | 0.972 | +0.0183 | [+0.0115,+0.0253] | PASS | −0.0012, P=0.13 |
| **R2 true HARQ, log-space** | 4.0 | 0.972 | **+0.0206** | [+0.0137,+0.0278] | PASS | **+0.0011, CI[+0.0003,+0.0019], P=0.99** |
| R3 PROD + skew-t | 4.0 | 0.965 | +0.0182 | [+0.0109,+0.0256] | PASS | −0.0012, P=0.16 |
| R4 PROD + online ACI width | 4.0 | 0.951 | +0.0072 | [−0.0009,+0.0153] | PARITY | **−0.0122, CI[−0.0196,−0.0056], P=0.00** |
| R5 PROD + online RMS (name) | 4.0 | 0.986 | +0.0177 | [+0.0111,+0.0247] | PASS | −0.0017, P=0.16 |
| R6 PROD + online RMS (pooled) | 4.0 | 0.972 | +0.0185 | [+0.0118,+0.0255] | PASS | −0.0010, P=0.09 |
| **R7 Gemini FULLY REPAIRED** | 4.0 | 0.951 | **+0.0103** | [+0.0022,+0.0188] | **PASS** | −0.0091, P=0.01 |

**The repairs work in the sense that matters most: R7 goes from −0.0837 FAIL to +0.0103
PASS.** The proposal is not unsalvageable — it was just wrong. But fully repaired it
still loses to production by 0.0091 with P(better)=0.01.

Two clean component findings:

- **The conformal/ACI layer is the problem, not the fix.** Even repaired into a proper
  walk-forward full-cone multiplier, R4 costs −0.0122 with a CI entirely below zero. The
  gentler RMS learners (R5/R6) are merely neutral. This is consistent with, and
  independent confirmation of, the `adaptive_width.py` finding: name-level width
  adaptation buys *calibration*, not *skill* — so it must be gentled, dead-zoned and
  history-gated, exactly as shipped. An aggressive online learner on 16 windows per name
  is pure variance.
- **R1 (levels) is numerically unstable** — one EG window produced a near-zero variance
  forecast, blowing std(u) to 114. Log-space is not a stylistic choice; it is why
  production works.

## The one real idea — and it does not generalise

R2 (true HARQ in log space) is the single arm that beat production anywhere. Pushed
through the full standing gate:

| | EG | SA |
|---|---|---|
| PROD, LONO cross-fitted | +0.0196 | +0.0002 |
| R2 HARQ-log, LONO cross-fitted | **+0.0206** | −0.0004 |
| paired delta, block=2 | +0.00102 CI[+0.00020,+0.00187] P=0.98 | −0.00066 CI[−0.00167,+0.00030] P=0.13 |
| paired delta, block=3 | +0.00103 CI[+0.00021,+0.00188] P=0.99 | −0.00065 CI[−0.00171,+0.00038] P=0.15 |
| paired delta, block=4 | +0.00104 CI[+0.00024,+0.00187] P=0.99 | −0.00066 CI[−0.00179,+0.00042] P=0.17 |
| beats PROD in | **20/30 names** | 5/11 names |

On EG it is real: survives LONO cross-fitting, robust across all three block sizes, CI
excludes zero on every one. On SA it **sign-flips** and is a coin flip by name count.

Stated plainly: **+0.0010 on a +0.0196 base is a ~5% relative improvement in skill, for
an extra regression per origin.** It is genuine but small, and it is EG-only on the
evidence in hand.

## Disposition

1. **The proposal as submitted stays REJECTED.** Nothing changes in Part 1.
2. **The repaired full engine (R7) is also rejected** — PASS, but −0.0091 vs production,
   P(better)=0.01.
3. **The ACI/conformal-width idea is REJECTED with prejudice** — it is the component that
   actively destroys skill (−0.0122, CI entirely below zero), before *and* after repair.
   Do not revive as a skill play. Add to the do-not-revive list alongside CRPS-selection
   and raw secular drift.
4. **The skew-t core is REJECTED** — parity-to-worse on both markets (EG −0.0012, SA
   +0.0014, both CIs straddling zero); the α driver is at its ±2 clip 21.5% of the time,
   which is a noise signature.
5. **True HARQ in log-space (R2) is a live EG-ONLY candidate.** It meets the promotion
   bar *on Egypt's panel* — LONO, block-robust, 20/30 names — and fails it on Saudi. That
   is precisely the pattern the standing per-market fit rule anticipates, and the same
   shape as `adaptive_width.py`'s EG-only adoption. If adopted it goes on a feature branch
   with an open PR, EG-only, and every other market stays on log-HAR until it clears this
   same gate on its own panel. **Open question before any PR:** the RQ proxy is built from
   daily OHLC, so realized quarticity is only weakly identified — the honest read is that
   R2's edge may be an artifact of the proxy rather than of quarticity attenuation, and
   that should be probed (e.g. against a placebo attenuator) before it goes near main.
6. Nothing was pushed. Per the GIT/PUBLISH MECHANICS rule, any push needs a fresh PAT
   supplied at that moment.

**Precedent this adds:** repairing a proposal is worth doing before rejecting it — the
repairs moved this from −0.0837 FAIL to +0.0103 PASS, and surfaced one genuine idea that
the broken implementation had completely buried. But "the idea survives repair" and "the
idea beats production" are different tests, and only one component passed even the first.

---

## Criterion D check (sponsor bar: cov90 of the 5%–95% cone within ±2pp of 90%, i.e. [88%, 92%])

| Arm | EG cov50/80/90 | EG 90% CI on cov90 | D | SA cov50/80/90 | SA 90% CI | D |
|---|---|---|---|---|---|---|
| **GEM as submitted** | — / — / **0.791** | — | **FAIL** | — / — / **0.800** | — | **FAIL** |
| PROD YZ-HAR (production) | 0.524 / 0.797 / **0.887** | [0.864,0.910] | PASS | 0.453 / 0.816 / **0.900** | [0.858,0.937] | PASS |
| R2 YZ-HARQ log-space | 0.522 / 0.797 / **0.889** | [0.866,0.912] | PASS | 0.458 / 0.821 / **0.900** | [0.858,0.937] | PASS |
| R4 PROD + online ACI width | 0.549 / 0.797 / **0.887** | [0.864,0.908] | PASS | 0.484 / 0.816 / **0.911** | [0.874,0.942] | PASS |
| **R7 Gemini FULLY REPAIRED** | 0.532 / 0.810 / **0.889** | [0.866,0.910] | **PASS** | 0.468 / 0.800 / **0.916** | [0.879,0.947] | **PASS** |

**As submitted the proposal misses criterion D by 8–10 percentage points** (79.1% / 80.0%
against an 88% floor) — the direct consequence of defects (a) and (b), a cone whose core
was ~17% too narrow.

**Fully repaired it passes D on both markets** (88.9% EG, 91.6% SA), as does the isolated
HARQ swap. So D is no longer the discriminator between the repaired candidate and the
incumbent — criterion C is. Both clear C against the dumb yardstick (R7 +0.0103 PASS,
PROD +0.0195 PASS); production simply scores nearly twice as well on it.

**Two honesty flags on this table.** First, each arm's `width_cal` was refitted in-sample
on the same panel its coverage is measured on, so these cov90 figures are the *best case*
for every arm — including production's. Second, the D band is narrow relative to the
sampling noise: ±2pp on 479 EG windows is roughly the width of the bootstrap CI itself,
and on 190 SA windows the CI is ±4pp — wider than the criterion. **On Saudi-sized panels
criterion D cannot currently distinguish a compliant cone from a non-compliant one**, and
should be read as a screen that catches gross miscalibration (which it did here, cleanly)
rather than as a fine discriminator between candidates.

**Bottom line on D:** the sponsor bar rejects the proposal as submitted and accepts it
once repaired — but passing A–D admits a candidate for consideration; it does not make it
better than the incumbent. On the head-to-head that decides that question, YZ-HAR still wins.
