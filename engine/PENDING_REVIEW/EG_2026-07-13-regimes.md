# PENDING REVIEW — EG — TWO REGIMES, BOTH PUBLISHED — 2026-07-13

**Engine change + methodology change. Changes the published cone for every EGX name.**

## The instruction

> "Egypt is a country where political turmoil, geopolitical uncertainty in the region and currency
> sudden devaluation and interest rate spikes are the order of the day. I want to train the model on
> as much data as possible and that would be one model... Then there is another MC model trained post
> the sudden shocks from 1 April 2024 to date, where there is currency fluctuation but less severe."

## Why one cone cannot answer this

A single calibration silently picks one answer to a question with two legitimate answers:

- **"What if Egypt keeps doing what Egypt does?"** -> every devaluation in the sample. Fat tail, wide cone.
- **"What if the current calm holds?"** -> post-shock only. Thinner tail, narrower cone.

Both defensible. Neither is *the* answer. **Averaging destroys the only thing worth knowing.**

## What changed in the engine

- `Regime` dataclass + `MarketProfile.regimes` + `profile.for_regime(key)`.
  The swap returns a profile with that regime's `breaks/nu/width_cal`, so `apply_breaks`,
  `backtest_v3` and `mc_v3` run a regime with **zero** further changes. No regime-aware
  branching scattered through the engine.
- `refresh_market` now fits **every** declared regime. Panels are rebuilt ONCE (they hold full
  history; `apply_breaks` filters at read time) and each regime just filters them differently.
- `_fit_and_score()` extracted so the regime loop and the primary path run the **identical** code
  — duplicating it would have been the obvious way to let the two silently drift apart.
- A market with **no** `regimes` declared behaves exactly as before. Fully backward-compatible.

## The two Egypt regimes

| | **full** (primary) | **current** |
|---|---|---|
| window | 2016 -> today, `breaks=[]` | 1-Apr-2024 -> today |
| nu / width_cal | **4.0 / 0.958** | 5.0 / 0.850 |
| windows | 508 (~17/name) | 232 (~8/name) |
| panel verdict | PASS +0.0169 CI[0.011,0.024] | PASS +0.0388 CI[0.026,0.054] |
| name-level FAILs | **CLHO** | KABO |

## What it revealed — the tail is where they disagree

Because **a devaluation IS a tail event**. CLHO, 3 months out, spot 16.31:

| | full | current |
|---|---|---|
| median | 17.02 | **17.02 — identical** |
| 90% band | 12.50 | 11.46 (+9%) |
| **99% band** | **29.36** | 24.19 **(+21%)** |
| **P(fall > 50%)** | **0.63%** | 0.32% — **2x as likely** |
| **CLHO verdict** | **FAIL (-3.8%)** | PARITY (+0.2%) |

**Read the last row.** On the all-crises model our cone does **not** beat a carry-anchored random walk
on CLHO. On the calm model it just about does. One blended number would have hidden that. It is now the
headline on the ticker page and in the ledger, published as a FAIL rather than buried.

## Site

- `data.js`: `dist.regimes.{full,current}` with both cones + crash probabilities.
  `dist.t20/t60` still resolve to the **primary (full)** cone, so every existing page keeps working.
- `clho.html`: new "Two models, not one" section — side-by-side cards + the tail-divergence table.
- Ledger notes and coverage thesis disclose the FAIL explicitly.

## Append-only

CLHO's published T+20/T+60 cohorts stay frozen and will be graded against exactly the percentiles
issued. The correction attaches to the next cycle. Verdict LABELS are updated (they describe the
current fit, not a frozen forecast).
