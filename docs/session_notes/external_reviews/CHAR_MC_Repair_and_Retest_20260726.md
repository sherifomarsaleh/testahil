# CHAR-MC — Repaired, Re-run and Re-tested (26 Jul 2026)

Follow-up to `claude/external_reviews/CHAR_MC_Authentication_Audit_20260726.md`. All seven audited
defects were fixed and every component the spec claimed but never shipped was actually implemented,
then the result was tested under the standing gate.

**Verdict: θ (saturation) REJECT. γ (illiquidity momentum) REJECT. ν (Student-t) and a fitted flat λ
ACCEPT — and those two are already in production. Repaired CHAR-MC is a re-derivation of the current
engine, not a new one. Honest gain +0.20% CRPS, not the claimed +15%/+44%.**

## Repairs made
Real Yang-Zhang (overnight² + Rogers-Satchell); real direct h-step HAR on forward log-variance;
Student-t with ν fitted by MLE; λ fitted by MLE instead of hardcoded by share-price bucket; λ removed
from the variance drag; γ fitted instead of clipped; coverage/CRPS computed instead of typed in.

## Protocol
26 EGX names, real OHLC 2017-08→2026-07, 38,093 panel rows. LONO cross-fitting (every parameter —
HAR coefficients, λ, θ, ν, γ — fitted on the other 25 names). **Five horizons h ∈ {5,10,20,40,60}** —
essential, because at a single horizon θ and λ are perfectly confounded and the original only ever
showed one parameter set, making its saturation term untestable by construction. Non-overlapping
scoring (10,053 rows), CRPS/spot, block bootstrap {2,3,4}.

## Ladder

| model | cov@90 | width | CRPS/spot | \|std_u−1\| | λ | θ | ν | γ | skill vs M0 |
|---|---|---|---|---|---|---|---|---|---|
| M0 carry RW, uncalibrated | 88.8% | 0.301 | 0.05510 | 0.178 | 1.00 | — | — | — | 0.00% |
| M1 + fitted flat λ | 91.4% | 0.341 | 0.05542 | 0.047 | 1.129 | — | — | — | −0.58% |
| M2 + saturation θ | 91.4% | 0.338 | 0.05541 | 0.044 | 1.168 | 0.021 | — | — | −0.56% |
| M3 + Student-t ν | 89.9% | 0.315 | 0.05500 | 0.032 | 1.169 | 0.014 | 4.04 | — | +0.20% |
| M4 + momentum γ | 89.9% | 0.314 | 0.05501 | 0.032 | 1.169 | 0.014 | 4.03 | −0.006 | +0.16% |
| **M3b flat λ + t, no θ** | 89.9% | 0.316 | **0.05495** | 0.034 | 1.142 | 0 | 4.03 | — | **+0.21%** |

M3b — saturation dropped entirely — is the best model.

## Bootstrap (blocks 2/3/4, all consistent)
- **θ on vs flat λ**: no significant difference (both with and without Student-t).
- **Generalised power-law horizon term** `sd ∝ σ·h^(0.5−β)`, the most generous possible form of the
  idea: fitted β = 0.0163 (exponent 0.484 vs 0.500), **no significant CRPS difference**.
- **γ on vs carry only**: γ **WORSE**, CI [+1.2e−5, +3.1e−5], all blocks.
- **M3 vs M0**: better, CI [−14.6e−5, −7.6e−5], all blocks.

## Component verdicts
- **θ — REJECT.** Fitted 0.014–0.021, i.e. **3–6× smaller than the 0.03–0.08 assigned by hand**. Zero
  proper-score benefit; improves a dispersion diagnostic only. Same "improves a diagnostic, fails the
  gate" pattern as the CRPS-selection and FVPull rejections.
- **γ — REJECT, note the sign.** Fitted γ = **−0.006**, i.e. *negative*: illiquidity-damped 20-day
  momentum predicts mild **reversal** over this panel, the opposite of the premise, which the original
  then clipped at its positive upper bound for 25/32 names.
- **ν — ACCEPT.** Fits to **4.03**, close to the ν=5 the spec asserted. Largest single contributor:
  turns M1's −0.58% into M3b's +0.21%. The original specified it and left it out of the code.
- **λ — ACCEPT but small.** Fitted 1.13–1.17 vs hardcoded 1.34–1.80 → the original over-widened by
  3–5× more than the evidence supports.

## One finding worth keeping
Miscalibration IS horizon-dependent. Uncalibrated std_u by horizon: h=5 → 1.242, h=10 → 1.164,
h=20 → 1.080, h=40 → 1.038, h=60 → 1.000. Short horizons are materially **too narrow**; h=60 is about
right. So a horizon-dependent width term is legitimately motivated — but the fix is to **widen the
short end**, not compress the long end, and the required gradient (~1.24×) far exceeds any fitted θ
or β. Student-t absorbs most of it; the residual doesn't pay. Relevant to the open per-origin
vol-estimation work.

## Caveats
One market, 26 names. Drift is carry-anchored throughout, so this tests the cone, not the drift (γ was
the only drift variation tried, and it failed). ν weakly identified as always — read as "fat, ~4".
No Monte Carlo used: the predictive law is analytic so quantiles are exact.

Artefacts: `char_mc_fixed.py`, `run_fixed.py`, `run_power.py` (session workspace).
