# EMAAR (Emaar Properties PJSC, DFM/AE) — mid-cycle refresh, 29-Jul-2026

**Trigger:** fresh OHLC posted for an already-covered name → Roll-Forward workflow (trigger b),
not a new study. Classified **mid-cycle** under Rollforward_and_Grading_Protocol v3 STEP 0(a):
the current cycle-2 cohorts were struck 24-Jul-2026 (5 days earlier, in the market-wide EG/AE/SA
re-strike) and the 1-month metronome does not fall until **24-Aug-2026**.

**Identity note:** this is EMAAR = Emaar Properties PJSC (DFM, AED), `engine/raw_ohlc/AE/EMAAR.csv`.
NOT EMFD (Emaar Misr for Development, EGX, EGP) and NOT EMAARDEV (Emaar Development PJSC, DFM).
All three are separately covered; only the AE EMAAR entry was touched.

## STEP 1 — merge, not overwrite

| check | result |
|---|---|
| export type | FULL history superset — 3,897 rows vs library 3,895; zero library-only dates |
| overlap | 3,895 dates, **0** price mismatches at 4dp on Price/Open/High/Low; 0 volume mismatches |
| back-adjustment | none detected |
| genuinely new | 2 sessions: 27-Jul (11.300) and 28-Jul (11.200) |
| write | +2 / −0 line diff — nothing rewritten, vendor format and BOM preserved |

Library now spans 02-Jan-2011 → 28-Jul-2026.

## STEP 2 — Step 0.0 gate + full AE panel refit

`data_quality.clean_ohlc(market='AE')`: **0 repairs, 0 drops**, 3,897 rows in = 3,897 out.
No non-trading placeholders, no corporate-action jumps beyond the ADX/DFM ±15% limit.

Panel refit on the **full 18-name AE panel** (never just the touched name), 3-month calendar gate:

| | live (pre) | new | move |
|---|---|---|---|
| ν | 10.0 | 10.0 | unchanged |
| width_cal | 0.979 | **0.972** | −0.72% |
| published 90% cone `width_cal × q95(t(ν))` | 1.77440 | 1.76171 | **−0.715%** (tol ±5%) |
| market verdict | PARITY | PARITY | unchanged |
| market skill (scale-normalized) | 0.0068 | 0.0069 | CI [−0.001, 0.014] both |
| resolved windows | 261 | 262 | +1 |

**Verdict flips: NONE** — all 18 names checked pairwise against the live registry. EMAAR itself
stays **PASS** (skill 0.0182 → 0.0184, LONO ν=12.0 / width_cal 0.965, CI [0.011, 0.036]).
Materiality gate: **NOT MATERIAL** → auto-applied to `market_profiles.py` + `fitted_configs.json`.
Diff confined to the AE block; every other market's panel hash was unchanged, so their fits are
bit-identical (used as the control).

ν is weakly identified as always — the honest object is the (ν, width_cal) pair and the cone they
jointly produce, which moved less than three quarters of a percent.

## STEP 3 — grading

**Nothing graded — nothing has matured.** EMAAR's two open rows grade 24-Aug-2026 (1M) and
26-Oct-2026 (3M). Across the whole 150-row open ledger there are **zero** matured-and-ungraded
rows as of 29-Jul-2026.

## STEP 4 — strike

**Skipped, per STEP 0(a).** No ledger rows written; LEDGER stays at 161 (150 open / 11 graded).
Striking a cycle-3 five days into cycle 2 would demote the 24-Jul 3M to an aging tail after 5 days
and add an overlapping 1M tail — the exact accumulation the 29-Jul lifecycle adoption removed.

Note also that `rollforward_one.py` could not have been used here unmodified: its per-row note is
hardcoded to "this name was NOT in the 28-Jul market-wide re-strike", which is **false** for EMAAR —
it *was* in that pass. The cone refresh below therefore ran the same `strike_cohorts.strike()`
production chain directly, ledger append omitted.

## STEP 5 — ticker page (displayed cone refreshed, both horizons)

Anchor 28-Jul-2026 @ 11.20. Production chain, no approximation: Step 0.0 → YZ variance proxy →
`fit_har_v3` → `har_forecast_v3` → carry drift `ln(1+rf_live)−ln(1+q)` → `simulate_paths_v3`,
50,000 paths, seed 42, AE fit ν=10.0 / width_cal 0.972, signal **OFF**, width overlay **inactive**
(EG-only), rf_live 3.65% CBUAE base rate (AED peg → Fed path). `q_annual = 0` — **FLAGGED**, house
convention; the drift is a gross-of-dividend price carry and overstates the centre by roughly the
yield. Horizons from `horizons.resolve()` on AE's own realized calendar (h1 = 22 sessions, h3 = 63 —
projected only to size the cone, never to define the check date).

| horizon | p5 | p25 | p50 | p75 | p95 | resolve |
|---|---|---|---|---|---|---|
| 1 month | 9.90 | 10.70 | 11.23 | 11.80 | 12.75 | 2026-08-28 |
| 3 months | 8.98 | 10.35 | 11.31 | 12.35 | 14.26 | 2026-10-28 |

Touch recomputed at the **same 7 absolute levels already on the page** (15.50 / 14.00 / 13.00 /
11.50 / 10.50 / 9.50 / 8.50), not re-picked.

**Changed:** `spot`, `spotDate`, `dist.t20`, `dist.t60`, `hz`, `touch`, `levels`, `tech`, `asof`,
the page chart, `SITE.updated`.
**Deliberately left alone:** `fair {bear 11.08, base 14.80, full 18.75}` — separate clock, moves
only on a genuine study refresh (asserted unchanged in verification); and the interactive slider's
bespoke factor-stack constants (`CONT_FIXED`/`EV_FIXED`/`GEO_MEAN`/etc.), which were fit once to
the fundamental driver stack, not to the carry-anchored engine. The slider still re-anchors to the
new spot because it reads `T.spot` live.

## STEP 5B — technical read, chart, stamps

Recomputed in the same pass. Supports moved 10.91 → 10.90; resistances unchanged
(12.75 / 13.04 / 13.81). Narrative re-derived: close 11.20 below a falling 20/50/200-day stack,
RSI(14) ~40 (was ~34), ATR ~0.27 (~2.4%), MACD negative and still falling. Chart regenerated to
28-Jul-2026, axis 7.376..17.474.

### Engine gap found and worked around — `apply_technicals` mis-stamps `asof.mc` on a mid-cycle pass

`apply_technicals.ledger_index()` derives `asof.mc` from the **newest LEDGER row** — anchor date off
the row, run date parsed out of its note. On a mid-cycle pass there is deliberately no new ledger
row, so it stamped EMAAR `mc: {data:"2026-07-24", computed:"2026-07-28"}` against a cone actually
anchored 28-Jul and computed 29-Jul. That is a **false staleness report** on the freshest block on
the page — the two-part stamp inverted into a false positive.

Protocol v3 anticipates this in prose ("the stamp source for `asof.mc` is then the `dist` resolve
dates") but the code does not implement it. The stamp was corrected by hand to the cone's true
provenance for this pass. **Open engine item:** make `ledger_index`'s result yield to the `dist`
resolve dates when those imply a newer anchor than the newest ledger row (3M resolve − 3 calendar
months = the anchor). Engine change → feature branch + PR, not folded into a data pass.

## Verification (evidence, not self-certification)

| check | result |
|---|---|
| `node --check` data.js / app.js | both OK |
| LOAD data.js, assert parsed objects | TICKERS **71** (known 71), LEDGER **161** (known 161) |
| open/graded split | 150 / 11 — unchanged, this pass appended zero rows |
| lifecycle invariant | **HOLDS** across all 150 (instrument, horizon) pairs; EMAAR 1×1M, 1×3M |
| `fair{}` untouched | asserted equal to {11.08, 14.80, 18.75} |
| import-not-parse | 13 engine modules import cleanly, incl. `market_profiles` (AE ν=10.0, width_cal 0.972) |
| chart overlay gate | EMAAR **passes**; 74 pages checked |
| rendered page | zero page errors; spot 11.20, caption "to 28 Jul 2026", both stamps read "data through 28 Jul 2026 · computed 29 Jul 2026", percentile table matches data.js |

### Pre-existing gate failure, NOT caused by this pass

`node scripts/check_ta_chart_overlay.js` exits 1 on **aapl.html (y=−28.3)** and **tsla.html
(y=−17.1)**. Reproduced identically on a pristine `HEAD` worktree — pre-existing, untouched here.

Root cause: AAPL / TSLA / NVDA carry `asof: undefined` — they were **never processed by the 29-Jul
`apply_technicals --write` pass**, so their `levels` are still the retired hand-authored ladders
while their charts are frozen at 30-Jun / 6-Jul. TSLA's published supports (405 / 360 / 294) all sit
**above** its 309.22 spot — the SAMSUNG defect, still live. Their US libraries are in fact current
to **27-Jul-2026**, so this is a stale *page*, not a stale library (distinct from the eleven
genuinely stale libraries in the open-items register). A dry run confirms
`apply_technicals --only AAPL TSLA NVDA` handles all three with 0 skips — one pass plus `ta_chart`
would clear it. Not done here: out of scope for a single-name roll-forward, reported instead.

## STEP 6 — ledger page / backtest PNG

Ledger page: no grade written, so nothing new to render. Backtest PNG
(`assets/calibration_EMAAR.png`): **regeneration not warranted** — it is a five-year quarterly
construct and this pass added 2 sessions and zero cohorts.

## STEP 7 — publish

Everything local. Not pushed; needs a fresh PAT at the moment of push, injected for that push only
and the tokenless remote restored immediately after.
