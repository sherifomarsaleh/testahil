# XPTUSD (Platinum) — Study Pack, 20-07-2026 — NEW COVERAGE (unpublished)

Full study delivered per the Standing Research Protocol trigger (a): `XPTUSD_Valuation_Study_20-07-2026_public.docx` (16 sections) + `XPTUSD_Valuation_Model_20072026_public.xlsx` (16 sheets) + PDF, delivered in-conversation 20-07-2026. **NOTHING PUSHED — publish needs a fresh PAT.** (Binary docx/xlsx could not be attached to the project via the API this session — they live in the conversation delivery; re-upload to project files manually if wanted.)

## Decisions taken (stated, per protocol)
- **The prompt template said "{COPPER}" — resolved to PLATINUM.** XPT is the ISO code for platinum; the uploaded series trades at $900–2,772 (platinum levels; copper is ~$4–5/lb) and matches gold/silver's 30-Jan-2026 crash day cross-sectionally. Copper remains uncovered (copper.html is still a placeholder).
- **New metal = new single-instrument market XPT** (silver-precedent file layout `raw_ohlc/XAG/SILVER.csv`), NOT pooled into XAU. Per the standing per-market fit rule, its first action was its own PROVISIONAL self-fit. The pooled 3-metal fit (ν≈20, cal 0.965, 148 windows) is computed and recorded as the likely future config — not adopted (must clear its own gate when metals pool).
- **Adopted engine config: ν = Gaussian (sentinel 250.0), width_cal = 0.853** (MLE scale 0.790, house clip floor 0.85 active). PARITY everywhere (self-fit −0.0004; LONO gold+silver-trained OOS −0.0114; borrowed live metals −0.0094). Platinum does NOT arrive failing. Reproduction check vs the live gold registry: EXACT (67 windows, +0.0035, CI[−0.005,+0.013]).
- **q_annual = 0** (METALS precedent + dated negative search: no holder yield; lease rate is a borrow cost). rf_live 3.63% (Fed midpoint held 18-Jun-2026), FED_SCHEDULE carry.
- **Fair-value zone $1,310–2,139, centre $1,634** (weights 30/30/20/20 ratio/consensus/balance/cost — Driver Ledger rows 37–39). Spot $1,608.37 = −1.6% vs centre.
- **MC cohorts (seed 42, 50k, production chain):** T+20 grade 2026-08-17: p5/25/50/75/95 = 1,381.97/1,514.01/1,612.84/1,718.44/1,881.84, touch +5/+10/−5/−10 = 53/27/49/21%. T+60 grade 2026-10-12: 1,238.91/1,452.81/1,623.02/1,813.36/2,128.49, touch 73/53/69/46%. anchor_vol 0.3356/0.3395. T+252 (study horizon): 961.14/1,332.64/1,668.58/2,085.84/2,896.85, resolve 2027-07-07. Cohort JSON: `claude/xpt/ledger_cohorts_XPTUSD.json` in this folder (drop-in for data.js at publish).

## FLAG for Sherif — silver raw file is being SKIPPED by the pipeline
`engine/raw_ohlc/XAG/SILVER.csv` exists in the library, but `auto_refresh.discover_touched_markets()` skips any dir not in `PROFILES` — and there is no XAG profile. The 19-Jul auto-refresh ran with panel_names ['GOLD'] only. If the intent of posting SILVER.csv was to give silver its own fit (or join a metals panel), that never happened and nothing said so. Same applies to XPT at publish: **the raw file alone is not enough — the profile must be added** (ready-to-paste snippet below), plus `'XPT'` in auto_refresh's class_name map and `DAILY_LIMIT['XPT']=None` in data_quality.py. Verify by IMPORT before commit.

## Publish staging (local, prepared, NOT pushed)
- `engine/raw_ohlc/XPT/PLATINUM.csv` = the raw vendor upload (library keeps raw; gate cleans on read).
- XPT MarketProfile snippet (fit_meta written): see below.
- Site: platinum.html is currently a "coming soon" placeholder; full ticker page needs the study refresh workflow (fair zone, dist, touch, S/R, narrative all new — no prior page constraints).

```python
PLATINUM = MarketProfile("XPT", "Platinum (USD)", FED_SCHEDULE, 0.0363,
    "USD cost-of-carry anchor: Fed funds midpoint schedule (q=0, no yield). Same "
    "documented assumption as METALS: the carry-anchored null for a zero-yield USD "
    "store of value is spot x exp(rf); gate-neutral (same anchor both sides).",
    None, +1, 0.0, False,
    nu=250.0, width_cal=0.853,
    fit_meta=("PROVISIONAL single-instrument self-fit 20-Jul-2026 (PLATINUM, 62 windows "
              "2012-2026, production chain, reproduction check vs live gold registry EXACT): "
              "nu=Gaussian (MLE scale 0.790 -> width_cal 0.853, clip floor 0.85 active). "
              "Verdict PARITY -0.0004 CI[-0.009,+0.009] robust {2,3,4}. De-circularized "
              "cross-check (fit gold+silver, score platinum OOS): PARITY -0.0114 "
              "CI[-0.032,+0.009]. Borrowed live METALS (Gaussian/1.0): PARITY -0.0094. "
              "Pooled 3-metal fit (nu=20, cal=0.965, 148 windows) is the likely future "
              "config once metals pool - NOT adopted. Platinum does NOT arrive failing."),
    notes="Carry-only. Single-name PROVISIONAL self-fit, flagged circular like gold's "
          "first fit; metals remain the weakest calibration in the system.")
```

## Data quality (Step 0.0, engine/data_quality.py, market=None → 0.70 threshold)
4,041 raw rows → 4,032 clean (1 leading placeholder 03-Jan-2011 + 8 interior holiday stale rows — same dates pattern as gold's library file). 260.0 rows/yr = exact metals Mon–Fri calendar (gold 260.4, silver 260.3); no Korean-style phantom rows. Max |1-day log| 0.194 (30-Jan-2026) — REAL (gold −10.4%, silver −31.6% same session), far under threshold; zero corporate-action repairs. Vendor artifact: ~12% of rows have Open marginally outside [Low, High] (spot-splicing; gold 0.5%, silver 0.6% — platinum's rate is higher, stated in study §7); YZ proxy's degenerate-bar guard handles it.

## Files in this folder
compute_xpt.py (all study numbers), step0_calibration.py (fit battery), sweep_xpt.py (register builder, validates 0 errors), figures_xpt.py, docx_xpt.py, xlsx_xpt.py (deterministic — cell-by-cell diff clean), qc_verify.py battery, study_numbers_xpt.json, step0_results.json, sweep_register_xpt.json, ledger_cohorts_XPTUSD.json. Cleaned series staged as XPT_clean_staged.csv (session workspace; regenerate from the raw upload via step00_dq.py).
