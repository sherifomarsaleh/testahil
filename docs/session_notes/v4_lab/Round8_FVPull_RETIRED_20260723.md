# Round 8 (Fair-Value-Pull) — RETIRED by policy, 23-Jul-2026

**Status: RETIRED.** Not an empirical rejection — the shadow cohort never reached
a gradeable sample (0/30 graded as of today; earliest T+60 maturity ~mid-Oct-2026).
Retired instead by explicit sponsor decision: MC drift must not depend on the
accuracy of a separate fundamental/valuation study, on principle, regardless of
what a future shadow-cohort verdict might have shown.

Full technical history stays untouched in `Equation_Lab_Round8_FVPull_Shadow_20260723.md`
and `Shadow_Cohort_Grading_Status_20260723.md` (ledgers/history are append-only —
not retro-edited). This doc is the current-status pointer that supersedes them.

Action taken same day: cancelled the monthly scheduled grading check
(`trig_01Gy5V3TZ8EHT74k5bawPGSM`) — no reason to keep polling a candidate that's
dead regardless of outcome. The shadow_cohort JSON and grading script are left in
place as reusable infra / historical record, not deleted.

## New standing constraint on future drift/enhancement candidates

Effective 23-Jul-2026: any candidate proposed to replace or augment the carry-only
drift must NOT depend on the accuracy of a separate fundamental/valuation analysis
(DCF, SOTP, DDM fair value, analyst consensus targets, peer-multiple-implied value,
or similar). Not because such signals are untestable — on principle: the MC
engine's own honesty must not be hostage to a separate, independently-fallible
research process. Price-technical, market-structural, flow, ownership, and
macro/regime signals remain in scope; fundamentals-derived target-price signals
do not.

## The four acceptance criteria for a good updated MC (sponsor-stated, 23-Jul-2026)

- **A** — Cones and drift must mimic real life.
- **B** — Each stock's individuality must be maintained: cone shape, drift, and return.
- **C** — Must pass the "dumb yardstick" test.
- **D** — Stated 90% coverage (5%-95% cone) must hold to within +/-2 percentage points.

### How these map onto existing machinery

- **C** is already the Step 0 calibration gate's own benchmark: CRPS-normalized
  skill vs. the carry-anchored lognormal random-walk. Every candidate already gets
  scored against this "dumb" baseline first.
- **D** is already the promotion protocol's hard gate used for Round 8
  (cov90 in [88%, 92%]) — same tolerance, now elevated to a general acceptance
  bar rather than Round-8-specific.
- **B** partially already holds today: each stock's own OHLC history drives its
  own HAR-cascade variance forecast (per-stock, not pooled), and drift already
  varies per stock via its own dividend yield. What IS pooled at the market level
  is the width_cal scaling multiplier and nu (tail shape). The specific idea of
  also letting width_cal vary per stock was already tested twice — most rigorously
  across 71 names / 1,154 windows (`Shrinkage_v2_Full_Universe_Walkforward_20260722.md`)
  — and conclusively REJECTED under LONO: zero net improvement, actively regresses
  SA. A literal reading of B ("cone shape varies per stock too") is a closed,
  already-failed door via that mechanism — a genuinely different mechanism for
  per-stock shape would need to be a different idea, not a re-test of shrinkage.
- **A** is the most open-ended of the four and has no single existing numeric
  gate — it's closest to "does the walk-forward/CRPS/block-bootstrap machinery,
  taken together, produce forecasts a domain expert would call realistic," which
  A/C/D collectively probe but don't reduce to one clean test.

## Standing instruction

Until a candidate clears A-D without a fundamental-analysis dependency,
production stays on the current carry-only, market-pooled-width_cal/nu system.
No production change is warranted or pending.
