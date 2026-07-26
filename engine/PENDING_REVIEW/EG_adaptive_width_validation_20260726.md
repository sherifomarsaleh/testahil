# Adaptive-width overlay — validation on the merged 15-year EG library, 26-Jul-2026

Re-validates the overlay (adopted 23-Jul-2026) against the data it will actually run on:
the long histories merged to main in PR #22, scored on the PRODUCTION post-break window.

## Setup
30 EG names, gate-cleaned, non-overlapping h=60 origins from min_history=260, scored on
origins >= 2022-03-21 (the adopted break cut). 492 windows per arm. Proposed post-merge
config nu=5.0 / width_cal=0.93 on both arms; ONLY the per-name multiplier differs.
Walk-forward safe by construction — at each origin the multiplier is built solely from
that name's already-RESOLVED windows. Benchmark: the carry-anchored trailing-252d RW null.

## Result

| arm | cov90 | mean width | std_u | CRPS skill |
|---|---|---|---|---|
| baseline (mult = 1) | 0.8963 | 0.7877 | 0.9042 | +0.0174 |
| overlay | 0.8943 | 0.7794 | 0.9169 | +0.0164 |

Paired CRPS, overlay minus baseline: +0.000139.
Block bootstrap {2,3,4}: CI [-0.000188,+0.000438] / [-0.000187,+0.000432] /
[-0.000203,+0.000435] — **PARITY at every block size. No proper-score cost.**

Cone-sizing (the criterion the overlay targets):
- **22 of 30 names moved CLOSER to std_u = 1.**
- pooled |std_u - 1|: **0.096 -> 0.083**.

Consistent with the 23-Jul FINAL result (24/30, 0.096 -> 0.069) on a different split.
Multipliers stayed gentle: range 0.912 (JUFO) to 1.098 (TMGH); 4 names sat at exactly
1.000 under the MIN_WINDOWS=28 history gate (RMDA, FWRY, EFIH, PRDC).

## Correction to an earlier expectation — the overlay does NOT rescue ISPH

ISPH was expected to be the headline beneficiary (23-Jul pilot: std_u 1.32 -> 1.03,
cov90 0.71 -> 0.86, log-CRPS -0.0289 -> +0.0013). On the production post-break window it
is **unchanged**: multiplier 1.001, std_u 1.292 -> 1.292, cov90 75% -> 75%,
skill -0.0289 -> -0.0291.

Cause: adaptive lag, not a bug. Every ISPH window that broke the cone lies INSIDE the
scoring period (-41% Dec-2022, +89% Mar-2023, +58% Sep-2023, +66% Sep-2024). Its prior
resolved windows looked normal, so an online estimator built on resolved history had no
signal to widen on. The 23-Jul note flags this failure mode ("residual adaptive-lag on
names whose recent behaviour differs from the test window") without naming ISPH.
Verified the moves are genuine: the Dec-2022 -> Mar-2023 fall is gradual, largest single
day 14%, no corporate action, no bad rows; ISPH simply ran at ~53% annualised vol.

## Separate finding: the ISPH verdict does not follow the protocol's own rule

The standing rule is that a name-level FAIL must be ROBUST across bootstrap block sizes
{2,3,4}; a block-dependent sign flip is a BOUNDARY, recorded PARITY-flagged. ISPH:

| block | 90% CI | reading |
|---|---|---|
| 2 | [-0.0509, +0.0028] | **crosses zero — boundary** |
| 3 | [-0.0492, -0.0000] | fail, upper edge at zero |
| 4 | [-0.0471, -0.0055] | fail |

Block 2 straddles zero, so by the protocol ISPH is **BOUNDARY (PARITY-flagged)**, not
FAIL. EG_2026-07-26.md records it as FAIL. On 16 windows (4 misses vs 1.6 expected,
p = 0.068) that is a watch item, not a failing name. Raised as its own work item — the
verdict code appears not to apply the all-three-blocks rule.

## Recommendation
Adopt the overlay on its own merits: better per-name cone sizing at zero proper-score
cost, now confirmed on the production data and window. Do NOT adopt it as an ISPH fix.
ISPH needs more resolved windows to settle either way.
