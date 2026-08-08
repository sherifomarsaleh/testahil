# CHAR-MC + Gemini-MC — what to keep, what to bin (26-Jul-2026)

Synthesis across two independently-reviewed external MC proposals, both audited today:
CHAR-MC (`claude/external_reviews/CHAR_MC_*`) and Gemini-MC
(`claude/v4_lab/Gemini_MC_Part{1,2,3}*`). Written from the Gemini side, after reading
all four CHAR-MC notes and independently re-testing their one actionable claim.

## 1. Can we use CHAR-MC? No.

Already rejected twice on its own evidence: the shipped code assigns `Coverage %` and
`CRPS Skill` by matching the **asset's name string** — no price data, no realised outcome,
`calculate_crps_skill_score()` called zero times — and the v2 "full audit response" shipped
a file **byte-for-byte identical** to the audited one (MD5 match, difflib zero changed
lines). Repaired properly it is **3.75% worse in CRPS than production**, robust across
bootstrap blocks {2,3,4}, and beats production on **3 of 26 names**.

That is the same landing point as Gemini-MC: rejected as submitted, still loses after
repair. Two unrelated external systems, two independent reviewers, same verdict.

## 2. The convergences are worth more than either system

Four things are now confirmed by multiple independent code paths, which is stronger
evidence than any single panel fit:

**(a) ν ≈ 4 for EGX is settled.** Production's pooled MLE → 4.0. CHAR-MC's LONO fit →
4.03–4.07. The repaired Gemini engine's pooled fit → 4.0. And a per-horizon fit run today
gives **exactly 4.0 at every horizon h ∈ {5,10,20,40,60}**. Four independent
implementations, one answer. Egypt's fat tail is not an artifact of our estimator.

**(b) EGX has no exploitable 20-day momentum, in either direction — stop re-testing it.**
CHAR-MC's γ (illiquidity-damped momentum) fits **−0.006**, i.e. mild *reversal*, the
opposite of its premise, which the original then clipped at its positive upper bound for
25 of 32 names. Our own EG ablation found rev_1m IC = +0.018 with the house contrarian
sign **refuted** and magnitude ~0. Gemini's Hurst-gated drift is closed 86% of the time
and destroys skill when it opens. Three independent tests, three nulls. Carry-only stands.

**(c) Hand-set or aggressive width adaptation fails; gentled and history-gated is the
only form that survives.** CHAR-MC's λ is hardcoded by **share-price bucket**
(`spot<5 → 1.34`, `spot>25 → 1.80`); fitted properly it is 1.13–1.17, so the original
over-widened by 3–5× the evidence. Gemini's ACI tail-stretch costs −0.0122 with the CI
entirely below zero even after being repaired into a proper walk-forward multiplier. Add
our own Shrinkage v2 rejection (71 names, 1,154 windows) and that is **four independent
rejections** of per-name width adaptation, against exactly one narrow acceptance —
`adaptive_width.py`, gentled, dead-zoned, history-gated at 28 windows, and adopted for
*calibration* at proper-score parity, never for skill. The boundary is now well mapped.

**(d) The multi-horizon protocol is the one real methodological upgrade on offer.**
CHAR-MC's repair tested h ∈ {5,10,20,40,60} and made a point our gate does not: **at a
single horizon, two width parameters are perfectly confounded** — the original's
saturation term was untestable by construction because it only ever showed one horizon.
Our Step 0 gate runs at h=60 only, while we publish and grade T+20. Adopting a
multi-horizon panel as standing practice costs little and closes a real blind spot.

## 3. Their most actionable claim does NOT replicate on production — checked today

`CHAR_MC_Repair_and_Retest` flags, under "one finding worth keeping", that miscalibration
is horizon-dependent: uncalibrated std_u = 1.242 (h=5), 1.164 (10), 1.080 (20), 1.038 (40),
1.000 (60) — "short horizons are materially too narrow". Taken at face value that is a
live exposure, because **T+20 is published on every ticker page and graded in the ledger,
but is never gated**.

It does not survive replication. Read their ladder: **M0 is the carry-anchored trailing-252d
RW** — that horizon table describes the *benchmark*, not production's engine. A constant-vol
random walk IS too narrow at short horizons; forecasting an h-specific variance is precisely
what the HAR cascade exists to do.

Re-run through production's own chain (`fit_har_v3` → `har_forecast_v3` → carry), 28 EGX
series, patched data-quality gate, 5,468 windows:

| h | windows | ν fitted | width_cal | cov50 | **cov90** | D |
|---|---|---|---|---|---|---|
| 5 | 1,222 | 4.0 | 0.958 | 0.522 | **0.899** | PASS |
| 10 | 1,194 | 4.0 | 0.958 | 0.517 | **0.894** | PASS |
| 20 | 1,151 | 4.0 | 0.979 | 0.500 | **0.907** | PASS |
| 40 | 1,085 | 4.0 | 1.021 | 0.526 | **0.885** | PASS |
| 60 | 816 | 4.0 | 0.993 | 0.504 | **0.901** | PASS |

**And the specific question that matters — the cost of reusing the h=60 fit at T+20:**
h=60 fit (ν=4.0, cal=0.993) applied at h=20 gives **cov90 = 0.910**, versus 0.907 for a
purpose-fitted h=20 config. Both inside [88%, 92%]. **The published T+20 cone is fine.**

Recorded because the wrong action here — widening T+20 by ~24% to "fix" the reported
1.242 — would have broken a cone that is currently in band. Their number is right about
what it measured; it is just not measured on us.

## 4. One methodological note back to the CHAR-MC work

Both CHAR-MC notes score with an "exact analytic CRPS (quantile integral)". That
sidesteps — but also **masks** — the defect found today: for a lognormal-Student-t,
E[exp(σT)] is infinite for every σ>0, so price-space CRPS has no finite expectation and a
sampled estimator is dominated by its largest draw (measured: one window carried **99.45%**
of a 1,293-window panel under production's own `simulate_terminal_v3` at ν=4.0). A
truncated quantile grid bounds the integral by construction, so the divergence never shows
up — but the underlying score is still not the thing it is presented as. Both review
streams should move to **log-space CRPS**, which is finite, scale-free, and already house
precedent in the Round 8 shadow-cohort protocol.

## 5. Disposition

| item | action |
|---|---|
| CHAR-MC as a system | **REJECT — do not revive.** Same class as CRPS-selection, Round-8 FVPull, Gemini-MC. |
| CHAR-MC θ (saturation) | REJECT — fitted 3–6× smaller than asserted, zero proper-score benefit |
| CHAR-MC γ (momentum) | REJECT — fits negative; third independent EGX momentum null |
| CHAR-MC λ (width) | Already ours, fitted, and smaller than they assert |
| CHAR-MC ν=4 | Already ours — but valuable as independent corroboration |
| **Multi-horizon gate protocol** | **ADOPT as standing practice** — cheap, closes the T+20 blind spot, and prevents single-horizon confounding of width parameters |
| Their horizon-narrowness claim | **Do not act on it** — measured on the RW benchmark; production is in band at every horizon (verified above) |
| Log-space CRPS | Open PR item from Part 3; applies to both review streams |

**Net:** there is no code to take from either system. What both delivered is *confirmation*
— of ν≈4, of the momentum null, and of where per-name width adaptation stops working — plus
one protocol upgrade (multi-horizon testing). That is a real return, and it is worth
recording as settled so neither idea comes back a fourth time.
