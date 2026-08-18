---
description: Grade every matured cohort and strike the fresh 1M + 3M. The monthly roll-forward, run as a watch.
argument-hint: "[optional: TICKER to restrict the pass to one name]"
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
---

# TESTAHIL metronome — grade what matured, strike what is due

This is trigger (b), the ROLL-FORWARD workflow, not a new study. It is the one carve-out
from "publishing needs an explicit ask": *a matured 1-month or 3-month cohort is graded and
rolled forward under the current engine WITHOUT waiting for a separate publish request.*
That carve-out covers **permission only** — every gate below still runs.

Restrict to `$ARGUMENTS` if a ticker is given.

## Step 1 — is there anything to do?

    node -e "const fs=require('fs');const {LEDGER}=new Function(fs.readFileSync('assets/data.js','utf8')+';return {LEDGER};')();const T=new Date().toISOString().slice(0,10);const due=LEDGER.filter(r=>r.realized_close==null&&r.grade_date<=T);console.log(JSON.stringify(due.map(r=>[r.instrument,r.horizon_label,r.grade_date,r.cycle_no]),null,0));"

**Empty → stop.** Say "nothing matured" and end the tick. Do not strike a cohort early to
have something to do; ledger strikes stay on the monthly rhythm, and an off-rhythm strike
demotes a 3M tail that had not finished earning its grade.

## Step 2 — grade against the DATE, not a session count

The forecast is a calendar commitment. Grade against the close on the row's stored
`grade_date` (`horizons.resolve()`: anchor + 1/3 calendar months, month-end clamped,
rolled to the exchange's first real trading session), **regardless of how many sessions the
window actually held.** Never re-derive the target by counting rows.

If an unscheduled closure pushed the first real session past it: grade the next actual
session in the library, keep `grade_date` as the date actually graded, and add
`grade_date_projected` plus a one-line `grade_note`.

Ledgers are append-only. A routine update never deletes a row.

## Step 3 — the library, then the gates, before anything is struck

1. **MERGE, NEVER OVERWRITE.** Diagnose partial vs full export; splice new rows onto the
   persistent library at `engine/raw_ohlc/{MARKET}/{TICKER}.csv`; verify overlapping dates
   match to the 4th decimal; no back-adjustment.
2. **Step 0.0** data-quality gate, then the **materiality gate on the FULL market panel** —
   never just the touched name. Same infrastructure as any other library update.
3. If the gate trips (verdict flip, new name already FAILING, market verdict change, panel
   name with no raw data, or the published 90% cone moving >5% on `width_cal × q95(t(ν))`),
   **stop and report.** Do not strike on a fit a human has not accepted.

## Step 4 — strike the fresh 1M and 3M

Through the ACTUAL production chain, never an approximation: `fit_har_v3` →
`har_forecast_v3` → `carry_log_h` (profile `rf_live`) → `simulate_paths_v3`, profile's live
ν/width_cal, signal per `signal_active`, seed 42, 50,000 paths. For EG, width_cal passes
through `adaptive_width.live_width_mult()` first — a no-op until the name clears
MIN_WINDOWS=28.

`cycle_no` = prior + 1, `reanchor_from` = prior `anchor_date`, anchored at the latest close.
`q_annual` must be SOURCED; if genuinely disputed, default 0 and flag it — never split the
difference. `grade_date` comes from `horizons.resolve()`; h1/h3 are projected only to size
the cone, never hardcoded 20/60. Same touch and percentile conventions as the existing
cohort.

The fresh 3M demotes the prior 3M to an aging calibration tail: open, untouched, graded at
its own maturity, used for nothing else.

## Step 5 — the page, in ONE pass

Update `TICKERS.{TICKER}.spot / spotDate / dist / touch` (touch at the SAME absolute levels
already on the page, never re-picked), then **in the same pass**:

    python3 engine/apply_technicals.py --write
    python3 engine/ta_chart.py --write
    node scripts/check_ta_chart_overlay.js

When the library moves, the technical read moves with it — levels, narrative AND the chart
underneath them. Refreshing levels onto a frozen chart is worse than leaving both stale.
The overlay gate is the only thing that catches a level line drawn outside the viewBox;
nothing throws and the page looks fine.

## Step 6 — verify, then say what you left alone

- Assert the lifecycle invariant: exactly one open latest-anchor row per (instrument, horizon).
- `node --check` both JS files, then LOAD `data.js` and assert on the parsed objects.
- Count tickers and ledger rows against a known total — never trust a tool's own "0 skipped".
- Import the engine modules; verify by import, not by parse.

**NEVER touched by this pass, and say so explicitly:** `fair{bear,base,full}` (separate
clock — needs a real study refresh) and the interactive slider's factor-stack constants
(`CONT_FIXED`/`EV_FIXED`/`GEO_MEAN`/…, fit to the fundamental driver stack, not to the
carry-anchored engine). Re-fitting either is a full study task.

The five-year quarterly backtest PNG is coarse enough that one new cohort essentially never
moves it — state plainly whether a regen is warranted rather than doing it by default.

A genuine outlier grade triggers an immediate out-of-cycle re-fit. Report it the same tick.
