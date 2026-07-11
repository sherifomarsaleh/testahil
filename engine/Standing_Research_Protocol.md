# TESTAHIL — Standing Research Protocol
### Updated 11 July 2026 — the continuous-learning release

This supersedes the 10-July text. Changes are marked **[NEW 11-Jul]**. Everything not
marked is unchanged and still binding.

---

## STEP 0 — The calibration gate (before anything else)

5-year walk-forward backtest, h=60 trading days, non-overlapping windows, scored against a
**carry-anchored** lognormal random-walk benchmark (spot × exp(carry); carry = ln(1+rf) −
ln(1+q)), so skill isolates signal and width and can never harvest the time-value of money.

**[NEW 11-Jul] Step 0.0 — the data-quality gate runs FIRST, before any calibration.**
`engine/data_quality.py::clean_ohlc`. No series enters a panel, a fit, or a study without
passing it. Two failure modes it exists to catch, both found live in production data:

- **Pre-listing / non-trading placeholder rows** — flat price, no volume. EFIH (e-finance)
  carried 0.50 placeholders before its Oct-2021 IPO, which the engine read as a **+333%**
  one-day return. The Korean vendor export carried **~160 phantom rows per name**, of which
  144 of Samsung's fell on a **Sunday** (KOSPI closed) — raw density 276.8 rows/yr against a
  real calendar of 245.8. These inject fake zero-return, zero-range days straight into the
  Yang-Zhang variance proxy and **depress the volatility estimate**.
- **Unadjusted corporate actions** — EFIH's 3:2 split (26-May-2025) and OCDI/SODIC's action
  (14-Aug-2025, reading as a fake **−73% crash**). OCDI was *inside the live production Egypt
  fit* when this was found.

**Detection is principled, not a guessed threshold.** Each exchange's own **daily price limit**
defines what a single session can physically do — a move beyond it is not reachable by trading,
so it can only be a corporate action or a data error. Thresholds are therefore **per-market**
(EGX ±20%, Tadawul ±10%, ADX ±15%, QE ±10%, KOSPI ±30%, NSE ±20%; US/metals have no limit and
use a high threshold). **A global threshold is wrong**: an EGX-calibrated cutoff would falsely
"repair" a legitimate Korean limit-down.

**[NEW 11-Jul] STANDING RULE — the calendar screen.** When adding a market or a name, screen its
trading-day density against that exchange's real calendar *before* trusting any fit built on it.
Vendor corruption is **per-export**: India was checked against the identical Korean pattern and
came back clean, so never assume a vendor is clean because another file from it was.

**[NEW 11-Jul] The gate is SCALE-NORMALIZED.** CRPS is denominated in price, so pooling raw CRPS
across a panel weights every market by **share price**, not information. Measured live: IHC (382
AED) carried **57.9%** of the 14-name UAE panel; ELM (874 SAR) carried **58.7%** of Saudi's. A
"panel verdict" was arithmetically a one-name verdict. The same defect operated *within* a name
across time (IHC ran 42 → 382, so its late windows outweighed its early ones ~9:1). Every window
is now normalized by its own spot before pooling. Effect on the existing record: **zero verdict
changes**, but CIs tighten sharply and headline skills de-inflate — Egypt's pooled PASS restates
from +0.059 to **+0.039**; the old figure was ~50% overstated by TMGH's 42% price weight.

**[NEW 11-Jul] Break filtering applies to the CALIBRATION SAMPLE.** `MarketProfile.breaks` was
declared on every profile and documented in this protocol but **never read by the engine** — the
rule existed only on paper. Windows whose origin precedes a market's last structural break are
now excluded from the fit. Adopted on evidence, not assertion: on Egypt, calibrating post-2023
only **beats** calibrating on everything out-of-sample (LONO +0.0211 vs +0.0198, both scored on
the same post-break windows) *and* narrows the cone (0.972 → 0.909).
**Open gap, honestly flagged:** the engine's *per-origin volatility estimation* inside mc_v3 is
still not break-aware. Fixing that would move every published distribution and is a deliberate,
separate decision.

**Verdicts.** Three-way and pooled. The name's own bootstrap CI gives PASS/PARITY/FAIL as a
diagnostic; the **market-panel pooled CI is the standing gate**. Proceed if the market panel is
PASS or the name is PARITY-or-better. Stop only on a name-level FAIL that is **robust across
bootstrap block sizes {2,3,4}** — a block-dependent sign flip is a BOUNDARY case, recorded
PARITY-flagged, never a silent proceed.

---

## THE MC ENGINE — mc_v3.py + market_profiles.py

"Carry-anchored YZ-HAR-t". Gap-aware Yang-Zhang width with a lognormal bias correction and a
per-market `width_cal`; Student-t(ν) shape with ν **fitted per market** on pooled LONO
cross-fitted residuals; drift = carry anchor + an IC-shrunk, dead-zoned, capped signal alpha.
50,000 paths, seed 42. Raw secular drift and unshrunk trend drift remain **retired, do-not-revive**.

### [NEW 11-Jul] Production fits — RULES ONLY, never a number

**Do not quote a fit from this document.** Every figure below (name counts, window counts, ν,
width_cal, verdicts) is exactly what the unattended loop refits every time a stock is posted —
they were already stale by the next commit on 11-Jul, and this file is not live-updated by the
pipeline. Read the live state before quoting anything:

    curl -s https://raw.githubusercontent.com/sherifomarsaleh/testahil/main/engine/market_profiles.py
    curl -s https://raw.githubusercontent.com/sherifomarsaleh/testahil/main/engine/fitted_configs.json

No token needed — the repo is public. `market_profiles.py` is the single source of truth (what
production reads); `fitted_configs.json` is a derived mirror.

What IS stable and worth stating here: eight markets are fitted (Egypt, Saudi, UAE, Qatar, USA,
Korea, India, Metals); UK and Brazil have no covered names yet. Egypt is the largest and only
panel to reach a robust PASS verdict on the market level. Metals is the weakest calibration in
the system (see below) and should never be read with the confidence of an EGX or GCC name.

**[NEW 11-Jul] EVERY MARKET NOW RUNS CARRY-ONLY.** Egypt's `rev_1m` was the last active signal
anywhere in the system and was **ablated off on evidence**: on the 27-name panel its empirical IC
is **+0.018** against a contrarian `sign=−1` prior (i.e. the *sign is refuted* and the magnitude
is ~zero); carry-only (+0.0252) beats signal-on (+0.0211); it helped in only 13/25 names on the
25-name panel the test was run against (11-Jul-2026, a fixed historical result, not the current
panel size); paired bootstrap P(signal helps) = **0.31**. India's `mom_12_1` shows the same wrong-sign pattern
(IC −0.093 against a +1 prior). Priors are **retained in the profiles for re-estimation** as
panels grow, but `signal_active=False` everywhere.

### [NEW 11-Jul] ν IS WEAKLY IDENTIFIED — never quote it as precise

Likelihood profiling: on the UAE panel **every ν from 5 through the Gaussian limit** sits inside
the 95% interval (ν=4 is only ΔlogL=2.23 away); on Saudi, ν=4–15 are indistinguishable. ν also
**trades off against width_cal** — a fatter tail wants a wider scale to fit the same residuals.
**The (ν, width_cal) PAIR is what is fitted.** Neither coordinate is individually meaningful;
the honest object is the cone they jointly produce.

### [NEW 11-Jul] THE PROMOTION RULE (standing)

**Nothing enters the engine — from a human or from the pipeline — without surviving the same
out-of-sample test the forecasts must survive.**

Precedent, and the reason this is a rule and not a slogan: selecting (ν, width_cal) by
**maximising CRPS skill** instead of by MLE looked clearly better in-sample (UAE +0.0038 vs the
incumbent's −0.0017). Tested honestly leave-one-name-out on two markets, it **LOST both times**
(UAE +0.0021 vs MLE's +0.0032; Saudi −0.0011 vs +0.0008). **It overfits. REJECTED — do not
revive.** What the exercise established was that the incumbent *configs* were stale, not that the
*procedure* was wrong.

---

## [NEW 11-Jul] THE UNATTENDED LOOP

`engine/raw_ohlc/{MARKET}/{TICKER}.csv` is a **persistent library of every covered stock**, not an
inbox — **65 stocks across 8 fitted markets** (27 EG · 11 SA · 14 AE · 3 QA · 3 US · 3 KR · 3 IN · 1 XAU).
To add or refresh ONE stock, add or overwrite ONE file. The
pipeline then refits that stock's **whole market** against the full library.

**One-stock post ≈ 12 seconds**, even on Egypt (the largest panel — check its current size live):
panels are content-hashed (only the
changed file rebuilds) and re-scoring uses `fast_rescore`, a closed-form re-simulation that is
**bit-for-bit identical** to re-running the engine (verified) but skips the O(n²) HAR refit.

**Market and ticker are decided by FILE PLACEMENT, never inferred from a filename.** This is
deliberate — the ADNOC-Gas / ADIB-Egypt-vs-ADIB-UAE class of ambiguity is exactly what must not
be automated.

### The materiality gate — automation, not unsupervised drift

**Auto-commits, no approval:** cleaning, panel rebuild, refit, LONO verdicts — *provided nothing
about the conclusion changed*.

**STOPS and opens a PR (never auto-merged):**
- any **existing** name's verdict category changes
- a **new** name arrives already **FAILING** (the signal that a file is misfiled or bad)
- **the published 90% cone moves >5%** — measured on `width_cal × q95(t(ν))`, the band a reader
  actually sees, **not** on ν and width_cal separately (they trade off, so watching them
  individually both misses real changes and fires on noise)
- the market-level verdict changes
- a panel carries a name with **no raw data** behind it

**A new name is NOT material by itself.** Adding coverage is the most common event; blocking on it
would mean a review request on every post. Placing the file *is* the human decision.

**Why the gate exists (empirical, not theoretical):** on 11-Jul, **data cleaning alone** flipped
Korea's tail from ν=6 to Gaussian and changed two names' robust verdicts. A bare cron job would
have shipped both silently.

**Guard:** `market_profiles.py` is verified by **IMPORT**, not `ast.parse`, before any commit —
`nu=Gaussian` is a bare identifier that *parses* perfectly and only dies at import. That exact bug
reached `main` on 11-Jul and left the engine unloadable while a digit-only regex check reported it
"intact". The workflow now carries an engine import smoke-test.

### Sources of truth

- **`engine/market_profiles.py` — THE source of truth. This is what production reads.**
- `engine/fitted_configs.json` — a **derived mirror**. Never hand-edit.
- `engine/panel_hashes.json` — a rebuild cache. Never hand-edit.

---

## UNCHANGED AND STILL BINDING

- **Template:** match TMPV + its Excel exactly. Reference studies by class: EAND (operating-co),
  ADCB (bank, primary), Alpha Dhabi (holdco).
- **Step 2A Information Sweep** — four mandatory rings (Global/Country/Industry/Company),
  classified B/S/D/C — runs BEFORE any forecast driver is set, on every study and every update.
- **WACC** bottom-up, market-adapted; local govt bond rf even for pegged currencies; ERP from
  Damodaran's *original* file only; genuine beta regression with a real usability gate.
- **Lens by instrument class**; never blend legs that need different methods.
- **DCF waterfall rule** — full build to PV of FCFF shown inline; stopping at FCFF is a hard QC fail.
- **Expert appendix** — three experts, genuinely different methods, a falsifier each.
- **Ledgers are append-only.** No published forecast is ever retro-edited.
- **Never a rating or a price target.** Fair-value ranges and distributions only.

---

## OPEN ITEMS (honestly ranked)

1. **Name-level `width_cal`, shrunk toward the market fit.** This is the real answer to the
   "bands are too broad" complaint, and it is *proposed, not built*. Both current robust FAILs
   fail for the SAME reason and it is **not** mis-centring — they are **over-covered**:
   LGES has `cov80 = 1.00` and `cov90 = 1.00` (every single outcome inside the 80% band), a cone
   1.11× the benchmark, and a PIT of 0.471 (perfectly centred). ALPHADHABI is the same shape.
   A market-level cone **over-widens any name whose own volatility sits below the panel average**.
   Must clear the same LONO gate that killed the CRPS-selection idea.
2. **Break-aware volatility estimation inside the engine** (currently only the calibration sample
   is filtered). Moves every published distribution — a deliberate decision, not a silent fix.
3. **Metals is the weakest calibration in the system — say so plainly.** Gold is a **single-name
   self-fit**: it is calibrated on its own data, so its PARITY verdict is **circular** in exactly the
   way Qatar's was until IQCD and QNB de-circularised it. Worse, **silver is a PUBLISHED instrument
   with no fit of its own — it borrows gold's.** Every other market has been pulled onto a real
   panel; metals has not. Until silver/copper/platinum history arrives, the metals cone is the
   least-evidenced thing Testahil publishes, and it should not be presented with the same confidence
   as an EGX or GCC name.
4. **UK and Brazil have no covered names**; their profiles are stubs.
