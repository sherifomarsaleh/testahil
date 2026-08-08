# MC-improvement research arc — session synthesis, 23-Jul-2026

Goal: a better MC system on the sponsor's four criteria — A (lifelike cones/drift),
B (per-stock individuality in cone shape/drift/return), C (beats the dumb yardstick),
D (stated 90% cone accurate to ±2%). This session took the 3-LLM triage candidates to real
walk-forward tests and, in doing so, produced a sharper diagnosis of where the engine actually
stands. Bottom line: **three more candidates fell to the out-of-sample gate, and the deeper
finding is that the engine is already near its achievable frontier on this data — the remaining
gap is criterion B (per-name width), which appears largely irreducible out-of-sample, not a
missing signal.**

## Candidates tested and closed this session (all via the standing OOS gate)

1. **Amihud illiquidity → dynamic tail-shape (nu).** REJECTED. Parity at best (doc [3,8]
   mapping), robustly WORSE at a fair EG-centered mapping. The decisive control — same average
   nu, differing only in the Amihud-driven time-variation — showed the conditioning itself is
   parity-to-worse. Full detail: `Amihud_DynamicDoF_Walkforward_REJECTED_20260723.md`.

2. **Bid-ask denoising (Roll 1984).** REJECTED at the precondition, no backtest needed. Roll's
   bounce requires NEGATIVE lag-1 return autocorrelation; **28 of 30 EG names show POSITIVE
   autocorrelation** (the opposite). The 2 exceptions (ORHD, ETEL) have a bounce component
   ≤10% of the range-based YZ proxy — and correcting it would double-count. Diagnostic:
   `lab_bidask_diag.py` / `bidask_diag.json`.

3. **Illiquidity-conditioned cone WIDTH (new, data-motivated).** REJECTED out-of-sample.
   Motivated by a strong in-sample signal (std_u vs Amihud r=-0.66: thin names' cones are too
   wide because thin trading inflates the high-low range → inflates the YZ proxy). One global
   parameter theta, fit on an early 60% DEV slice, one shot on the held-out 40% FINAL slice.
   DEV wanted only theta=0.05 (+0.0004 skill — marginal even in-sample); FINAL came out
   parity-to-worse (baseline +0.0329 vs candidate +0.0296, wins 36% of windows). Same fate as
   shrinkage_v2 and the CRPS-selection idea: an in-sample correlation that does not generalize.
   `lab_illiq_width.py` / `illiq_width_result.json`.

## The central diagnostic (the session's most valuable output)

`lab_width_calib_diag.py` measured the PRODUCTION engine's per-name width calibration on the
30-name EG panel, 538 walk-forward windows (std_u = std of the standardized 60d residual;
1.0 = perfectly width-calibrated):

- **Market level: already good.** Pooled n-weighted std_u = 0.925, cov90 = 0.892 (inside the
  ±2% band), cov80 = 0.801 (dead on). Criteria C and D are essentially met on average, and the
  cones are lifelike (A).
- **Per name: badly split.** std_u ranges 0.56 (EFID, far too wide) to 1.63 (TMGH, far too
  narrow); 15 names too wide, 5 too narrow, 10 ok; 22 of 30 fall outside the cov90 ±2% band
  individually. This IS criterion B failing, and it maps the standing "TOP OPEN ITEM" precisely.
- **The too-wide names are the illiquid ones** (r=-0.66) — the strongest single predictor, ahead
  of vol level (-0.38, and note: the sign is that high-vol names are too wide, not too narrow —
  my initial guess was backwards) and vol trend (~0). `lab_width_predictor.py`.

## What this means for the goal (the honest strategic read)

The per-name width error is **real in-sample but not reliably exploitable out-of-sample** by any
observable-conditioned correction tried so far: direct residual-variance shrinkage
(shrinkage_v2, 71 names) failed, and now illiquidity-conditioning (1 DoF, external observable —
the most defensible form) also failed OOS. The consistent pattern across four independent
attempts (CRPS-selection, shrinkage, Amihud-nu, illiquidity-width) is that the market-pooled
(nu, width_cal) fit sits at or near the achievable frontier for this data volume, and the
per-name "individuality" gap is dominated by estimation noise on ~17 windows / thin history,
not by a stable structured signal a cleverer feature would capture.

Concretely, criterion B (per-stock individuality in the CONE) is looking data-limited rather
than model-limited. Two implications worth putting to the sponsor:

- **The realistic lever is more DATA, not a cleverer estimator.** Per-name width becomes
  estimable only with materially more history/observations per name; every low-data shortcut has
  now failed the same gate. (Individuality in DRIFT/return via fundamentals was separately ruled
  out by policy this session — see `Round8_FVPull_RETIRED_20260723.md`.)
- **The engine may already be "good" for its data.** A/C/D are met at the market level; the
  honest "bands too broad" cases are the illiquid names, and their excess width is the price of
  not overfitting thin, range-noisy series — shrinking it did not survive OOS.

## Still untested from the triage (low expected value, not run)

- **CSAD herding → nu toggle.** A different conditioning variable than Amihud, but it drives the
  SAME nu knob, which this session showed has weak CRPS leverage on EG (coverage barely moved
  across nu 4→6.66). Not pre-judged, but low priority given the two nu-related nulls.
- GDR/parallel-FX premium, foreign-ownership, order-flow: still data-gated (repo lacks the feeds).

## Recommendation

Stop the candidate-by-candidate width/nu/drift hunt pending a strategic decision, because the
evidence now points to a data limit rather than a missing signal. Best next moves, for the
sponsor to choose: (a) invest in more history/coverage to make per-name width estimable; (b)
accept the market-pooled engine as near-optimal for its data and redirect effort to coverage
breadth and the fundamental (fair-value, non-MC) side; or (c) if still hunting signals, test
CSAD next but treat the nu knob's demonstrated weak leverage as a low prior. Production unchanged
throughout — nothing tested this session cleared the gate.
