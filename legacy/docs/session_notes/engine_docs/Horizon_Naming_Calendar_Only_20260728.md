# STANDING AMENDMENT — horizons are calendar-named, everywhere — 28-Jul-2026

**Owner instruction, 28-Jul-2026: there is no "20 days" and no "60 days" anywhere in Testahil.** Every horizon is a calendar horizon: **1 month** and **3 months** (and 12 months where it exists). This supersedes every earlier passage in the Standing Research Protocol, the project instructions, and any doc that names a horizon in trading sessions.

Shipped in `216a7b2` on `main`.

## What the rule is now

- Published horizons are named **1 month** / **3 months**. Never `T+20`, `T+60`, "20 sessions", "60 sessions", "20 days", "60 days".
- This applies to **every row, including cohorts struck before the 27-Jul-2026 changeover.** Their forecast numbers are untouched and remain append-only — p5..p95, realized closes, grades, touch ladders and cycle numbers are byte-identical. Only the horizon **name** is now stated in calendar terms, so the ledger reads as one convention.
- The earlier carve-out — "cohorts struck before the changeover keep their published T+20/T+60 horizons" — is **withdrawn as to naming**. It still holds as to numbers: nothing published is ever recomputed or retro-edited.
- The grade date remains what `horizons.resolve()` returns: anchor + N calendar months, month-end clamped, rolled forward to the first real trading session on that exchange. A calendar month runs ~18–24 sessions depending on market and month; that variability is precisely why the date, not a session count, is the anchor.

## Superseded phrasings

Anywhere the older protocol text still reads **"h=60 trading days"**, **"resolved 60-day windows"**, or **"resolved 60-day residuals"**, read **"the 3-month calendar window"**. The live calibration gate already runs on the calendar tag (`HORIZON_TAG = '3m'` in `auto_refresh.py`; `HORIZON_SETS['3m']` in `panel_refresh.py`) — the session-counted `'60d'` set is retained only to re-score grandfathered windows and is not the live gate.

## What changed in the repo

**Data** (`assets/data.js`) — `horizon_label` "T+20"→"1 month" (79) and "T+60"→"3 months" (156); dist labels "1 month (T+20)"→"1 month" (14), "3 months (T+60)"→"3 months" (14), "12 months (T+252)"→"12 months" (3); 35 touch-ladder headers and assorted fan/percentile prose. Ledger labels are now exactly `{1 month: 142, 3 months: 142, 12 months: 2}`; zero `T+n` strings remain.

**Site** — `ledger.html`: the `HZ_DISPLAY` map is deleted (labels are calendar-named in the data, so a rendered cell is the stored label verbatim), `HZ_MONTHS`/`hzRank` drop their `T+n` entries and the `T+n` regex, and the *"Why some rows carry a (T+20) or (T+60) tag"* explainer is replaced by a short *"How we pick the check date"* note. `method.html` legacy paragraph rewritten. `app.js` `HZ_LEGACY` long labels and both horizon-convention comment blocks. `extra.html` / `elm.html` cross-check rows.

**Engine** — `horizons.py` docstring rewritten and the unused `LEGACY_LABEL` constant deleted; comments in `panel_refresh.py`, `auto_refresh.py`, `apply_rollforward.py`; the retired-gate label; `gbco_study/{build_xlsx4,docx_A,docx_B,figures}.py` table and figure captions; `publish_adh.py`, `build_adh_page.py`, `build_adh_ar_page.py`.

**Docs in repo** — `Standing_Research_Protocol.md`, `PROJECT_INSTRUCTIONS_11-07-2026.md`, `Calibration_Ledger.md`, `mc_v3_validation_20260710.md`.

Repo-wide residual across `.html` / `.js` / `.py` / `.md`: **zero files**.

## Verification

`node --check` on `data.js` and `app.js`; `data.js` loaded and asserted on the parsed `TICKERS`/`LEDGER` objects rather than on text. Every engine module on `main` **import**-verified, not merely parsed — `horizons`, `panel_refresh`, `auto_refresh`, `apply_rollforward`, `market_profiles`, `wacc_builder`, `research_protocol`, `strike_cohorts`, `data_quality`, `mc_v3` — per the standing verify-by-import rule. `gbco_study` scripts re-parsed. Live `main` confirmed byte-identical to local via `raw.githubusercontent.com`.

## Two things deliberately NOT changed

1. **`files/PHDC_Valuation_Study_09-06-2026_public.docx`** — a study delivered in June. Rewriting a published document is a different act from relabelling live data, so it is left intact and flagged rather than silently edited. Say so if it is ever cited.
2. **The `dist.t20` / `dist.t60` object keys in `data.js`** — internal identifiers, invisible to readers, referenced across ~80 files (`app.js`, every ticker page). Renaming them to `h1`/`h3` is mechanical but breakage-prone and deserves its own verified pass rather than riding along with a naming sweep. No reader ever sees them.

## Replacement text for the project-instructions block

The custom-instructions block cannot be edited from a session. Two passages there need replacing by hand:

Under the grading rule, replace *"count the ACTUAL number of trading rows from anchor_date in the library to find the true T+20/T+60 session, and grade against THAT close"* with:

> resolve the grade session through `horizons.resolve()` — anchor + 1 or 3 calendar months, month-end clamped, rolled forward to the first real trading session on that exchange — and grade against THAT close. Never grade off a stored `grade_date` alone; it is a projection and is holiday-blind.

And in the calibration-gate paragraph, replace *"5-year walk-forward, h=60"* with:

> 5-year walk-forward on the 3-month calendar horizon

Everything else in that block stands.
