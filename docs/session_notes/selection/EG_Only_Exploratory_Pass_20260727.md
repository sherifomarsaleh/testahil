# SELECTION ENGINE — EG-ONLY EXPLORATORY PASS

**Status: EXPLORATORY / NON-BINDING.** Run per `Selection_Engine_PreRegistration_v1`
§3-§6, EG alone, using the now-live 15-year clean library. **No factor can be
formally ADOPTED from this run** — §6 rule 3 requires the same sign in ≥2 of 3
markets (EG, AE, SA), and AE/SA are still on the short 5.5yr library (deferred).
This is a first look at what the pooled test will be working with, not a decision.

## What changed vs. the pre-registration's assumptions

The doc assumed ~62 cohorts on the 15-year library. The real, majority-quorum
EGX calendar (≥15/30 names trading) runs 2011-01-02 → 2026-07-22, 3,744 sessions.
Walking back non-overlapping 60-session anchors gives:

- **58 cohorts** usable by F1/F2/F4/F5/F6 (need 252d trailing) — 2012-03-25 → 2026-04-20
- **41 cohorts** usable by F3 (needs 1260d trailing, i.e. 5yr) — 2016-05-31 → 2026-04-20

Both below the assumed 62 — critical values below are **re-simulated at these real
dimensions**, not taken from the pre-registration's table (which is now stale and
should not be quoted).

## Recorded judgment calls (per §8/§10 discipline)

- **RAYA excluded from F4 only.** 34.6% flat High==Low corrupts its Yang-Zhang
  variance proxy specifically; Price/Volume are fine for the other five factors.
  A general guard (any name/window with >20% degenerate bars in the trailing
  252d) was applied on top, in case another name has a similar problem in some
  window — it didn't trigger for anyone else in this run.
- **Volume-unit screen run before F5** (§8 required this). Flagged **19 of 30
  names** with >50x single-day jumps against their trailing 20-day median volume.
  Spot-checked EFID manually — its raw recent volume looks like normal lumpy
  EGX liquidity (0.5M–3.4M range), not a unit swap, but the older history wasn't
  hand-checked name-by-name. **F5's result below should be treated as
  data-quality-unverified, not just statistically weak** — this needs a proper
  per-name forensic pass (same kind of check that found the non-positive-price
  bug) before it's trusted either way.
- **Minimum 6 names per cohort** to score IC/tercile-spread (need ≥2 per tercile).

## Results

| Factor | Cohorts | Mean IC | Expected sign | Sign OK? | Crit. (single, α=.05) | Crit. (Bonferroni×6) | Verdict | Jackknife |
|---|---|---|---|---|---|---|---|---|
| F1 Momentum 12-1 | 58 | **−0.0349** | + | **NO** | +0.0455 | +0.0662 | **WRONG SIGN** | robust (no flips) |
| F2 Short-term reversal | 58 | +0.0053 | − | **NO** | −0.0444 | −0.0638 | **WRONG SIGN** (~zero) | unstable — 6 names flip it |
| F3 Long-term reversal | 41 | −0.0187 | − | yes | −0.0555 | −0.0823 | not detected | robust (no flips) |
| F4 Low volatility | 58 | **+0.0481** | + | yes | +0.0491 | +0.0699 | not detected (just under bar) | robust (no flips) |
| F5 Amihud illiquidity | 58 | +0.0014 | + | yes (trivial) | +0.0452 | +0.0656 | not detected (~zero) | unstable — 11 names flip it |
| F6 52w-high proximity | 58 | +0.0303 | + | yes | +0.0453 | +0.0663 | not detected | robust (no flips) |

Tercile spreads (sd-units, informational): F1 −0.043, F2 +0.018, F3 −0.005, F4
+0.076, F5 +0.067, F6 +0.037. Block-bootstrap 90% CIs (block sizes 2/3/4) are in
the raw output — none of the six cross zero cleanly in the pre-registered
direction at all three block sizes, consistent with "not detected" rather than
a confident finding either way.

## Reading this per §7 (do not over-interpret a null)

At 41-58 EG-only cohorts, power is **below** the pre-registration's already-sobering
pooled-panel table (which needed all three markets to get real power). A "not
detected" here for F3/F4/F6 is exactly the kind of result §7 says must be recorded
as `NOT DETECTED at this power`, not `no signal` — especially **F4**, which
landed just 0.001 short of even the single-factor (not Bonferroni) bar, was
sign-correct, and was untouched by dropping any single name. That is a candidate
worth re-testing once AE/SA are pooled in, not a factor to discard.

**F1 and F2 are different** — F1 came back with the *wrong* sign outright (same
pattern as India's momentum prior, already refuted elsewhere in this project),
and F2's near-zero reading flips sign if any of six ordinary names is dropped,
meaning there's nothing there to lose by dropping it. Both look like genuine
non-findings rather than underpowered true positives, though EG-only still can't
close the book on either.

**F5 is unresolved, not negative** — the near-zero IC and 11-name jackknife
instability could be a real null, or could be an artifact of the unresolved
volume-unit questions above. Do not record this as a refutation until the
volume screen is cleared.

## What this does NOT do

- Does not touch `market_profiles.py`, the MC engine, or any live output.
- Does not constitute an ADOPT/REJECT decision for any factor — that requires
  AE+SA per the pre-registration's own rule.
- Does not amend the pre-registration — the cohort-count correction above is a
  factual update (real data landed), not a change to the test's design, so it
  doesn't need the §10 amendment procedure. If AE/SA pooling later changes the
  factor list, thresholds, or cohort construction, *that* would need §10.

## Next step

Source AE (5.5yr → target 15yr or best available) and SA history, run the same
pipeline pooled, and only then evaluate §6's five-part ADOPT checklist for real.
F4 and F6 are the two names worth prioritizing given this pass; F1/F2 can likely
be dropped from the frozen six without much loss (see §5 "adding a seventh
requires removing one" — this pass is the evidence for which one, if it comes to
that); F5 needs the volume forensic pass regardless of what AE/SA show.
