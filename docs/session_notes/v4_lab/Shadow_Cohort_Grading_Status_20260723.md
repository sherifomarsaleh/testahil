# Shadow Cohort #1 — grading infrastructure built, and a real blocker found (23-Jul-2026)

> **[SUPERSEDED IN PART — 8-Aug-2026]** The grading mechanism described here counts 60 actual trading rows since anchor "per the standing grading rule" — that rule is retired: horizons are calendar-only (1 month / 3 months, 12 months for metals) and a forecast is graded on its stored calendar `grade_date` resolved by `engine/horizons.py` (anchor + N calendar months, month-end clamped, rolled forward to the exchange's first real trading session), regardless of how many sessions the window actually held; session counts are projected only at strike time to size the cone. Note also that this note's companion scripts moved from `claude/v4_lab/` to `engine/lab/v4_lab/` in the repo on 08-Aug-2026, so the paths in "Files" below no longer resolve. The rest of this document stands as the dated record of what was done at the time.

**"Start testing the remaining idea" (Sherif, 23-Jul) — here's what that
means concretely for Round 8 (fair-value-pull), and what it turned up.**

There is nothing to retroactively test (look-ahead, per the Round 8 doc) and
nothing forward-gradeable yet either way — Cohort #1 was anchored the same
day this was written. What's actually actionable today is building the
grading mechanism itself, so October is "run the script," not "write the
script." That's done: `grade_shadow_cohort.py`, checked in here alongside
the cohort. Per name it: counts ACTUAL trading rows elapsed since anchor
(never calendar days, per the standing grading rule), and once >=60 have [RETIRED 8-Aug-2026 — see header]
elapsed, regenerates both the prod and shadow sample paths at the stored
seed (deterministic — verified this reproduces the originally-stored
quantiles before trusting any score), then scores both on CRPS (raw and
log-space), which quantile band caught the realized close, and PIT.
Tested end-to-end with an artificially-lowered threshold against real
current data before being trusted on the real 60-session bar. [RETIRED 8-Aug-2026 — see header]

## The finding: it can't advance yet, and not because of the calendar

Ran it for real: **0/30 graded, and every single name shows 0 (not some
small number — zero) trading sessions elapsed since its anchor.** Checked
why: `raw_ohlc/EG/*.csv` hasn't received a new row for ANY of these 30
tickers since each one's own last-posted date (the same dates that became
each row's anchor — ABUK stuck at 1-Jul, ORHD at 24-Jun, ISPH at 7-Jul,
DSCW at 19-Jul, etc.). This isn't a per-ticker fluke; it's the whole EG
library.

This matters beyond Round 8. Per the standing protocol, `raw_ohlc/{MARKET}/
{TICKER}.csv` is a persistent library that gets refreshed by someone
actively posting new data per ticker — there's no live market-data feed
wired in. If nothing is posted, the calibration pipeline, the ledger
grading, AND this shadow test all sit still no matter how much calendar
time passes. October only works if the library gets refreshed between now
and then. This is worth Sherif's attention independent of Round 8.

## What's scheduled

A monthly check-in (scheduled task, not a durable in-session cron) that
re-runs this script and reports: still stalled (and how stale), or now
showing real progress, or — if the full 60 sessions are in for enough names
— an actual first read on the delta. First grading window remains targeted
for ~mid-October per the original doc, contingent on data actually flowing. [RETIRED 8-Aug-2026 — see header: maturity is the stored calendar grade_date, not a session count]

## Files [RETIRED 8-Aug-2026 — see header: these moved to engine/lab/v4_lab/ on 08-Aug-2026]

`claude/v4_lab/grade_shadow_cohort.py` (this note's companion). Depends on
`claude/v4_lab/shadow_cohort_20260723.json` (already saved) and a live
clone of the engine repo (public, anonymous read).
