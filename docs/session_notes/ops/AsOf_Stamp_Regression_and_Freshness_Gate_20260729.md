# As-of stamp regression, calendar grading, and the gate that now catches both — 29-Jul-2026

**PR #44**, branch `fix/asof-stamp-regression-and-freshness-gate`.
Commits `77d954de` (stamps + gate) and `38f00495` (calendar grading + horizons). Pushed,
open, **not merged**. Gate is green: 0 failures, 4 warnings.

## What broke

`fcee684d` (08:44) stamped the computed technical read + `asof{mc,tech}` onto all 74 names.
`c33b3ada` (11:27, "Reconcile with the concurrent session's fix/dq-phantom-split-prints")
silently reverted **9** of those blocks to their pre-adoption state: `asof` dropped entirely,
hand-authored `levels`/`tech` restored. The 9 were exactly IN + US + KR — TMPV, RELIANCE,
INFY, AAPL, NVDA, TSLA, SAMSUNG, KAKAO, LGES.

**Why no one noticed.** That merge's own commit message records its verification: *"71
tickers before/after (none lost) … COMI confirmed byte-identical."* It counted containers and
byte-compared a name it had never touched. Counting containers cannot see fields disappear
from inside them; byte-comparing an untouched name cannot see a regression in a touched one.
This is the COUNT-AGAINST-A-KNOWN-TOTAL rule applied to the wrong total.

The stamping rule was written down — *"when the library moves, the technical read moves with
it, IN THE SAME PASS"* — but lived **only as prose**. No CI job ran `apply_technicals`,
`ta_chart`, or `check_ta_chart_overlay`; no gate asserted stamp coverage. A documented rule
with no executable enforcement survived exactly three hours.

## TMPV specifically

The **MC was current** — cycle 2 struck at anchor 2026-07-28 resolving 28-Aug / 28-Oct. The
**technical read was not**: the page still narrated "low-350s" and "RSI in the low-30s"
against a 324.15 spot, on the retired hand-authored ladder. Neither carried a stamp, so the
page could not self-report either fact.

## Everything else the pass turned up

| Finding | Detail |
|---|---|
| **PLATINUM `mc.computed: "2012-01-05"`** | `apply_technicals` scraped the first `dd-Mon-yyyy` anywhere in the ledger note. Platinum's note opens `"origins 05-Jan-2012 → 13-Feb-2026"` — its **calibration sample start**. Stamped as the run date. |
| **GOLD phantom session** | Published spot 4090.87 labelled `"close 28 Jul 2026"`. 4090.87 is the **27-Jul** close; the XAU library has no 28-Jul row. |
| **QNB + PLATINUM legacy resolve dates** | Retired session-counted dates on the pages (2026-08-02 / 2026-09-27 and 2026-08-17 / 2026-10-12) against calendar 2026-08-05 / 2026-10-05 and 2026-08-20 / 2026-10-20. Ledger `grade_date`s were already right. |
| **5 more stale technical reads** | IQCD, QNB, QGTS, ORAS, SILVER — the DQ fix changed the **cleaned** series and ORAS/SILVER libraries moved later in the day, with no technicals re-run after either. |
| **Six pages on the retired 20/60 session grid** | IQCD, QNB, QGTS, GOLD, SILVER, PLATINUM carried **no `hz` block at all** → app.js fell through to `HZ_LEGACY {h1:20, h3:60, cal:false}`. Their published percentiles were pinned at 20/60 sessions when their own spans project to **22/63** (QA) and **23/66** (metals) — the metals cone drawn ~10% short on its own x-axis — and `cal:false` selected the retired session naming in axis, hover and prose. Same root as the QNB/PLATINUM resolve dates. |
| **The fan axis mixed two units** | Intermediate ticks were labelled `t + "d"`, so 2pointzero.html read *latest, 11d, 1 month, 32d, 42d, 53d, 3 months*. Only 0/h1/h3 carry a committed calendar meaning; "32d" invited 32 sessions to be read as 32 calendar days when it is nearer 1.5 months. Zoom buttons had the same slip ("90d" = 90 sessions ≈ 4.3 months). |
| **`median_err` unit outlier** | TMPV stored **-8.17** (percent) where the other ten graded rows store a fraction. Surfaced when its row was nulled — worth knowing before anything averages that column. |

**Correction to the protocol block:** the "ELEVEN LIBRARIES ARE STALE" list is itself stale.
QA, IN and KR all run to **2026-07-28**. Only US (2026-07-27) and XPT/PLATINUM (2026-07-20)
genuinely lag.

## Grading is by calendar date, not session count

Both cycle-1 cohorts had been graded on the **T+20 session**, not the calendar maturity the
forecast commits to:

- **Gold**, anchor 2026-06-25, graded 2026-07-23 — exactly 20 sessions. Calendar maturity is
  anchor + 1 month = 2026-07-25 (Saturday) → first real session **2026-07-26**. True window
  22 sessions. Re-graded: `realized_close` 4048.78 → **4094.18**, `realized_quantile` 0.577 →
  **0.625**, `median_err` 0.0186 → **0.0300**. High/low unchanged (the two added sessions set
  no new extreme), every `touch_hit` unchanged, forecast untouched.
- **TMPV**, anchor 2026-06-30, graded 2026-07-28 against a maturity of **2026-07-30** that
  has not arrived. **Re-opened** — all `realized_*` and score fields nulled, `grade_date`
  moved to 2026-07-30. Sits alongside cycle 2 as an aging 1-month tail; lifecycle invariant
  holds.

Both carry a `grade_note` recording exactly what moved and why.

## Fixes shipped

1. `apply_technicals` + `ta_chart` re-run across all 74 — restores the 9, refreshes the 5.
2. **Strike date is a field, not scraped prose.** All 161 ledger rows carry `run_date`,
   backfilled from the commit that introduced each row's anchor. `NOTE_RUN_RE` deleted, no
   prose fallback.
3. GOLD spotDate label; QNB + PLATINUM resolve dates.
4. `hz` computed from each name's own anchor via `horizons.resolve` for all six that lacked it.
5. Axis and zoom labels say **sessions** where they mean sessions; the retired `T+` form is
   gone from app.js entirely, including the now-unreachable legacy prose branch.
6. Gold re-graded, TMPV re-opened.
7. **`scripts/check_data_freshness.py`**, wired into page-integrity CI.

## The gate

Stamps present and coherent (`computed` never precedes its own `data`, never in the future) ·
technical read on the current **cleaned** library (Step 0.0 applied — LCSW's raw tail carries
a no-trade print the gate drops, so a raw comparison would cry wolf) · calendar-only horizons
on **both** page and ledger · `hz` present, calendar, and matching the name's own projected
span · published spot proven against a real session in the library · sourced `run_date` ·
lifecycle invariant · every published name reaching a ledger instrument **in both directions**.
Warns rather than fails when `asof.mc.data` < `asof.tech.data` — the cone-stale-vs-its-own-library
diagnostic, reported and never silently reconciled.

**Negative-controlled** against the morning's defect: **184 FAILs** on the pre-fix file, **0** now.

## Still open (gate warnings, not failures)

SILVER's published cone is anchored 28-Jul but its newest ledger anchor is **2026-07-03** — a
published forecast with no committed grading record at that anchor. SAMSUNG shows the same
shape one day apart. Both are consistent with the mid-cycle-refresh rule, but page and ledger
are describing different strikes. ORAS and QNB are cones lagging a refreshed library.

## Verification

All 11 engine modules **imported**, not parsed · `node --check` on data.js and app.js, then
data.js **loaded in node** and asserted — 74 entries, 161 rows, `2POINTZERO` present, zero
unstamped, zero rows without `run_date`, zero on a legacy `hz`, lifecycle invariant holds ·
`check_page_integrity` clean · `check_ta_chart_overlay` PASS on all 74 pages.
