# Continuous calibration — the unattended pipeline

**Contract:** mechanical work is unattended. Anything that would change a
published verdict, imply a signal change, or move a config beyond a small
tolerance stops and asks a human. This split exists because, on 11-Jul-2026,
data cleaning ALONE flipped Korea's tail shape (nu 6 -> Gaussian) and changed
two names' robust verdicts (SA/RAJHI PARITY->PASS, AE/ALPHADHABI PARITY->FAIL).
A naive "run the pipeline on a cron" would have pushed both to production with
no one looking. `auto_refresh.py`'s materiality gate is the fix.

## How to add or refresh a name — ONE STOCK AT A TIME IS THE NORMAL CASE

`raw_ohlc/` is a **persistent library**, not an inbox. Every covered stock keeps its
current OHLC there permanently (65 stocks across 8 markets as of 11-Jul-2026). To add
or refresh ONE stock, add or overwrite ONE file:

    engine/raw_ohlc/{MARKET_CODE}/{TICKER}.csv

The pipeline then refits that stock's **whole market** against the full library, so a
single-stock post is the default, cheapest path — not a broken one. (An earlier design
treated `raw_ohlc/` as "this session's uploads", which meant every one-at-a-time post
left the other panel names without a raw CSV and falsely tripped the gate. Fixed.)

**Cost of a one-stock post: ~12 seconds** (Egypt, 27 names). Panels are content-hashed,
so only the changed CSV is rebuilt; every other name is re-scored via `fast_rescore`,
which is bit-for-bit identical to re-running the engine but skips the O(n^2) HAR refit.
A cold rebuild of all 65 stocks is ~4 minutes and happens only once.

Market codes: EG, SA, US, GB, BR, KR, AE, IN, QA, XAU (must match
`market_profiles.PROFILES`). The ticker is whatever you name the file — this
is deliberate. File placement IS the human decision about what a series is;
the pipeline never tries to infer a ticker from a company name (that ambiguity
— e.g. ADNOC Gas vs. Abu Dhabi Islamic Bank's two differently-listed entities —
is exactly the kind of judgment call that stays manual).

Push to `main`. The GitHub Action (`.github/workflows/testahil-calibration.yml`)
picks it up automatically, or trigger it manually from the Actions tab, or wait
for the daily 03:00 UTC sweep.

## What happens automatically (no approval)

- `data_quality.clean_ohlc` — market-aware artifact repair (drops pre-listing
  placeholder rows and non-trading phantom rows; back-adjusts unadjusted
  corporate actions using each exchange's own daily price limit as the
  detection threshold, not a global guess)
- panel rebuild + pooled (nu, width_cal) MLE refit for every touched market
- LONO per-name and market-panel verdicts (PASS/PARITY/FAIL/BOUNDARY, robust
  across bootstrap block sizes {2,3,4})
- ...**provided the materiality gate finds nothing that needs a human.**

## What stops and opens a PR instead (never auto-merged)

- any EXISTING name's verdict category changes
- a NEW name arrives already FAILING (likely a misfiled or bad file)
- **the published 90% cone moves more than 5%** — this is measured on the band the
  reader actually sees, `cal x q95(t(nu))`, NOT on nu and width_cal separately. Those
  two trade off against each other, so watching them individually both misses real
  changes and fires on noise. (Concretely: cleaning 8 stale gold rows moved the MLE
  from nu=12 to Gaussian — which a naive "nu regime" rule called material, but the two
  are statistically indistinguishable, dlogL=0.31, and the cone moves 0.3%. The cone
  rule ignores it, while still catching every real change from 11-Jul: Saudi +15.6%,
  Korea +11.8%, Egypt +5.8%.)
- the market-level panel verdict changes
- a panel carries a name with NO raw CSV in the library (stale residuals)

**A new name is NOT material by itself.** Adding a stock is the most common thing that
happens here; blocking on it would mean a PR on every post. You placing the file at
`raw_ohlc/{MKT}/{TICKER}.csv` IS the human decision about what the series is. New names
are always named explicitly in the run output so an arrival is never invisible.

None of these are auto-applied even when the LONO evidence looks solid — see
`gate_scale_fix_20260711.md` for why a CRPS-skill selection procedure that
looked good in-sample was tested out-of-sample and REJECTED. Anything that
changes what gets published goes through the same discipline, whether a human
or a cron triggered it.

## Files

- `panel_refresh.py` — the fitting engine (`refresh_market`, break-filtering,
  scale-normalized CRPS gate). `update_registry=True` by default (the
  interactive behaviour used all session); `auto_refresh.py` calls it with
  `update_registry=False` so registry writes go through the gate too.
- `data_quality.py` — per-market OHLC cleaning gate.
- `auto_refresh.py` — the orchestrator + materiality gate. Run
  `python3 auto_refresh.py` (dry run) or `--apply` locally to test before
  relying on the Action.
- `fitted_configs.json` — derived mirror of `market_profiles.py`. Never
  hand-edit; it's written by `write_production` / interactive sessions only.
- `PENDING_REVIEW/*.md` — generated when something material is found; deleted
  once reviewed (the PR that carries it is the durable record).

## Local dry run

    cd engine
    python3 auto_refresh.py            # prints what WOULD happen, changes nothing
    python3 auto_refresh.py --apply     # actually writes (production or PENDING_REVIEW)
