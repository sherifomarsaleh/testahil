# Grade-date audit vs the calendar rule — 29 Jul 2026 (session close-out)

Every LEDGER row checked against `engine/horizons.py` by IMPORT — `resolve(market,
anchor, N)` recomputed independently and compared to the stored `grade_date`. Market
resolved from the new `assets/markets.js` registry. Audited twice: once at `03bd0bb7`,
then again after PR #44 (`962fbfa7`) merged on top at 23:52.

## Result on current main (`962fbfa7`)

**158 of 161 rows match exactly.** All 151 open rows are correct — every one resolves to
`anchor + 1 or 3 calendar months`, month-end clamped, rolled to that exchange's first
real session. Spot checks: EMAAR 24-Jul → 24-Aug (Mon) and 26-Oct (24 Oct is a Saturday);
COMI/EMFD 28-Jul → 30-Aug (28 Aug is a Friday, EGX trades Sun–Thu).

**3 graded rows are off the calendar rule** — all struck before the 27-Jul changeover and
graded under the retired session-count method:

| name | anchor | calendar target | graded on | off | note? |
|---|---|---|---|---|---|
| PHDC | 11-Jun | Sat 11-Jul → 12-Jul | 13-Jul | +1 late | yes |
| OCDI | 23-Jun | Thu 23-Jul (Revolution Day, EGX shut) → 26-Jul | 22-Jul | −4 early | yes |
| COMI | 29-Jun | Wed 29-Jul, a real session | 28-Jul | −1 early | yes |

Grading **early** is the direction that matters — it takes a close before the forecast's
own commitment date. Two of the three are early. All three carry a `grade_note`, so the
deviation is disclosed rather than silent; under the append-only rule the published rows
are not re-dated.

PR #44 fixed two of the five found in the first pass: **Gold** now grades 26-Jul (was
23-Jul, −3) and matches; **TMPV** was returned to open, so its −2 early grade is gone.

## Lifecycle shape vs the adopted diagram

| check | state |
|---|---|
| every name carries one current 1M + one current 3M | ✅ 74/74, zero duplicate open anchors |
| open rows per name | **2** for 71 names, 3 for Gold/TMPV/+1 — the diagram's **M0 start state**, not steady-state 4 |
| graded by horizon | `{1 month: 10, 3 months: 0}` |
| aging 3M tails | only Gold and TMPV |
| 12-month metals | 2 open, on their own annual clock |

The steady state of 4 open per name is only reached if the aging 3M tails survive the next
two monthly strikes — which is exactly what the 29-Jul cleanup destroyed the first time.
**No 3-month window has ever been graded**; the earliest possible is 28-Oct-2026 for the
28-Jul strikes.

## Shipped this session

- `95df0aa0` — market comes from library placement, not `asset_class`. Fixes 34
  international names rendering under EGX. New `scripts/build_market_registry.py` →
  `assets/markets.js`; loud "Unplaced" group instead of silent EGX default. See
  `claude/ops/Market_Registry_Fix_Tabs_Mislabelled_EGX_20260729.md`.
- `03bd0bb7` — reverted the experimental action-queue table sort; the ledger reads as one
  ascending `grade_date` sequence across past and future, as before.

## Open when this session ended

1. **EMAAR 1M cohort deleted on its grade date.** Anchor 29-Jun @ 12.14 AED, p5–p95
   9.98–14.86, `grade_date` 2026-07-29. Removed by the 304→161 cleanup while inside its
   final window — the only one of 139 removals that was. Numbers recoverable from git
   (`e32df4cf~1`). Blocked: the uploaded export's newest row is **28-Jul (11.200)**, so
   the 29-Jul close it needs is not in the file. Re-pull with 29-Jul and it grades.
   Detail in `claude/ops/Ledger_Cleanup_Audit_and_Due_Ordering_20260729.md`.
2. **EMAAR library is 4 sessions stale** — live AE library stops 24-Jul; the upload
   carries 27 and 28 Jul (full 2011→2026 history, 3,896 rows, so a full-export merge).
   Mid-cycle rule: cone + technical read refresh only, no ledger rows. Not done.
3. **`scripts/check_ta_chart_overlay.js` was failing on main before this session** —
   `aapl.html` (level line at y=−28.3) and `tsla.html` (y=−17.1) drew S/R lines outside
   the chart viewBox. Confirmed pre-existing against a pristine checkout. PR #44 touched
   both pages; re-run the gate to see whether it still fails.
4. **QNB / IQCD / QGTS libraries are 24 days stale** (last session 5-Jul) — worst on the
   board.
5. Nothing was gradeable on 29-Jul: the earliest open check date is **Silver, 3-Aug**.
