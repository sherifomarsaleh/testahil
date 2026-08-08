# ISTETHMAR (private, graded track) vs production mc_v3 — PHDC note, issued 2026-07-17

Istethmar is a PRIVATE, positions-taken-and-graded track. It does NOT change the production
engine and does NOT touch any published study/cone. It reuses the EXACT same live Egypt cone —
mc_v3 carry-anchored YZ-HAR-t, nu=4, width_cal=0.972, 50k paths, seed 42, carry rf=19.5%,
q_annual=0 — and layers on three decision/presentation choices that the production track
deliberately forbids. Same engine, same cone; only the framing differs.

## The three differences (this is what the user's table describes)

1. **With-trend tilt.** +/-0.15 * sigma_H drift added by SMA100 side (price above SMA100 -> +0.15,
   below -> -0.15), fixed ex-ante as a standard trend-following prior. Here it is +3.3% at 3M, on
   top of the +4.6% carry. It moves the 3M median 15.32 -> 15.82 (+3.3%) and lifts P(up) to 68%.
   The note's own walk-forward shows the tilt carries ~0 measured alpha AND ~0 measured cost
   (errors move by 0-4% on small samples; direction hit 56%/69% vs 60%/63% always-up). It is a
   declared STANCE, not an edge. Production keeps ALL trend/secular drift RETIRED (do-not-revive);
   istethmar runs it only because a private track is allowed to take declared, graded risk.

2. **Inner percentiles.** Prints P40-P60 (core) and P30-P70 (working range) of the SAME
   distribution instead of the public 80%/90% cones. 3M working range 14.54-17.24 vs the P5/P95
   tail 11.50/21.77. This narrows the PRINTED range honestly — true containment odds are stated
   (~40% for the working range) — rather than faking precision by shrinking width_cal (the
   rejected shortcut; realized coverage already runs slightly tight, so shrinking would be a lie).

3. **Point + stance.** Commits to a single fair price (3M 15.82, +8.0%), a direction (UP), a
   stretch objective (17.70), and a HARD invalidation (a CLOSE below 13.96 kills the call). This
   turns the distribution into a gradeable call whose error profile is measured (3M empirical MAE
   ~19%, close-at/above-point odds 50/50 by construction) and is graded against its own frozen
   numbers at maturity. Production NEVER prints a rating or a price target — ranges/distributions
   only.

## Honest caveats carried in the note (do not drop these when citing it)

- PHDC is a PARITY name at the production gate (2026-07-13): name skill +2.6%, CI [-1.3%, 9.6%]
  — straddles zero. The call is judgment layered on a parity name and says so.
- Realized bands run slightly TIGHT of nominal: 80/90 = 72%/84% at 1M, 75%/75% at 3M. Widen
  mentally, most at 1M.
- 3M error backtest n=16 (small). Origin data ends 2026-06-28; ~60% of the 1M window had already
  elapsed at issue — refresh the library file to re-cut the note.
- Dividend leg assumed zero. nu is weakly identified — the cone, not its coordinates, is the
  fitted object.

## Bottom line

Same engine, same cone. Istethmar differs only in that it (a) shades the median with a declared
zero-alpha trend tilt, (b) prints an inner slice of the cone instead of the full public cone, and
(c) takes a graded directional stance with a mechanical invalidation. All three are things the
production track forbids precisely because they trade calibration for a stance — legitimate on a
private graded track, never on the published engine.
