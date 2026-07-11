# Continuous calibration — the unattended pipeline

**Contract:** mechanical work is unattended. Anything that would change a
published verdict, imply a signal change, or move a config beyond a small
tolerance stops and asks a human. This split exists because, on 11-Jul-2026,
data cleaning ALONE flipped Korea's tail shape (nu 6 -> Gaussian) and changed
two names' robust verdicts (SA/RAJHI PARITY->PASS, AE/ALPHADHABI PARITY->FAIL).
A naive "run the pipeline on a cron" would have pushed both to production with
no one looking. `auto_refresh.py`'s materiality gate is the fix.

## How to add or refresh a name

Drop the raw OHLC CSV at:

    engine/raw_ohlc/{MARKET_CODE}/{TICKER}.csv

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

- any name's verdict category changes
- a NEW name enters a panel (one human glance at the ticker mapping)
- width_cal moves >5% relative, or nu crosses the Gaussian/fat-tail boundary
- the market-level panel verdict changes
- a name's raw CSV was dropped from this run but the panel still carries it
  (ambiguous: intentional removal, or an accidental omission?)

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
