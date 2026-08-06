# TESTAHIL — Standing Research Protocol
### Updated 29 July 2026 (rev. 4) — computed technical read · as-of stamps
### (rev. 3, 13 July 2026 — terminal growth · beta · Ke/Kd/WACC · engine-reconciliation · maximum-history calibration)

This supersedes the 12-July text and the first 13-July revision. Changes new in **rev. 2** are marked
**[NEW 13-Jul r2]**; the same-day **[NEW 13-Jul]**, **[NEW 12-Jul]** and **[NEW 11-Jul]** markers are
retained for provenance. Everything not marked is unchanged and still binding.

**Rev. 2 adds two procedures, both adopted from live failures caught in the RMDA build:**
a **Ke/Kd/WACC standing procedure** (the discount rate is a sliding schedule, not a flat number; the
sovereign double-count is removed; the terminal anchor is norm-built; and a Kd-integrity gate now blocks
the specific error that understated Rameda's cost of debt by 350bp), and an **engine-reconciliation rule**
(a study's Step-0 must reproduce the committed production fit exactly — enforced by assertion, after a
study script was found silently scoring windows production excludes).

---

## [NEW 06-Aug-2026, per instruction] THE PRIMARY-SOURCE ACCESS GATE — STOP AND ASK

**If the company's own financial statements cannot be reached, STOP WORK AND ASK. Do not build the
forecast on anything else.**

This is a standing hard gate on every study, every update and every re-forecast, for every ticker
in every market. It outranks the default "run the whole study end-to-end without asking": the
unattended run has exactly **two** stopping conditions, and this is the second of them.

| Blocking condition | Behaviour |
|---|---|
| No OHLC price history in `engine/raw_ohlc/{MARKET}/{TICKER}.csv` and none attached | Say so immediately and **stop** — never reconstruct a series, never substitute an index |
| The company's own issued financial statements cannot be reached | **Stop and ask Sherif what to do** — never substitute unofficial data |

### What counts as the primary source

The company's own issued statements — full IS / BS / CF plus the notes — obtained from a source the
company or its regulator publishes. In descending order, and **all of them are official**:

1. The company's own website / investor-relations page (annual and interim report PDFs, financial
   statement downloads).
2. The exchange's own disclosure portal — EGX, Tadawul, ADX, DFM, QE, KRX/DART, NSE/BSE, SEC EDGAR,
   LSE RNS.
3. The regulator's filing archive where it is separate from the exchange (e.g. FRA, CMA).

Anything else — aggregators (stockanalysis.com, Investing.com, simplywall.st, TradingView, Mubasher,
Zawya), broker notes, press coverage, search-result extracts of any of the above — is a **cross-check
only**, never a build source. That distinction is SIGCM clause #1 and it does not bend.

### Try before you stop

A stop is only honest after a real attempt. Work the list above in order and record each attempt
(URL + failure mode). **A proxy or TLS failure is not a company-website failure until it has been
checked** — a 403/405/407 from the egress proxy, or a CA-bundle rejection, is an environment fault
first: follow `/root/.ccr/README.md` and `curl -sS "$HTTPS_PROXY/__agentproxy/status"` before
concluding the source is unreachable. Never disable TLS verification or unset the proxy to get
around it.

### What "cannot be reached" means

Any of these, and partial access counts:

- The site, IR page or filing portal will not load, or egress to it is blocked and the block survives
  the proxy check above.
- The filings are simply not published there for the periods the forecast needs.
- The documents load but are unreadable (scanned images that will not parse, corrupt or truncated
  PDFs).
- The statements are reachable but **fall below the two-year floor** (see immediately below).

### The floor is TWO COMPLETE FINANCIAL YEARS

**A complete financial year means the full IS, BS and CF *plus the notes* for that year, from an
official source.** A year with a summary income statement and no cash flow, or with no notes behind
the debt and D&A lines, is not complete and does not count toward the floor.

| Complete years obtainable officially | Behaviour |
|---|---|
| **0 or 1** | **STOP AND ASK.** One year gives no growth rate, no working-capital delta, no roll-forward — there is nothing to build a ground-up forecast on |
| **2** | **Build, and say so.** State on delivery which year is missing, where it was looked for, and what it costs the forecast; record the shortfall against QC items (e) and (s) rather than passing them silently |
| **3 or more** | Normal run — item (e) is satisfied on its own terms |

The distinction is real, not bureaucratic: two years is the minimum from which a growth rate, a
working-capital movement and a capex-to-revenue relationship can be *observed* rather than assumed,
which is what separates a ground-up forecast from a guess. It is nonetheless thinner than the house
standard, so it is disclosed on the face of the study, never absorbed quietly. A ground-up forecast
still missing gross profit, SG&A, D&A, interest expense or the debt schedule within those years is
not a forecast at all — that is a stop regardless of the year count.

### What the stop looks like

Halt the build at that point — no model, no partial deliverable, no "provisional" study. Report, in
this shape, and then **wait for an answer**:

- the ticker and what was needed (which statements, which periods, why);
- every official source attempted, with the URL and the exact failure mode for each;
- what is still missing and what it blocks downstream (which drivers, which lens, which sheets);
- the options as you see them — Sherif supplies the statements or the PDFs; Sherif explicitly
  authorises a named non-official source **with the disclosure that this breaches SIGCM #1 and that
  the study carries the breach on its face**; or coverage is deferred.

**Do not pick one of those yourself.** A sourcing caveat in the front matter is not a substitute for
a source, and "best available data, labelled as such" is not the standard this engine publishes to.

### Precedent — the failure this closes

**ELEC (El Sewedy Electric, 05-Aug-2026).** The egress proxy blocked direct fetches of EGX, Mubasher,
Zawya, Arab Finance, stockanalysis.com, simplywall.st, Investing.com, TradingView, WSJ **and the
company website (ececables.com)**. The research file
(`engine/elec_study/research/elec_company_financials.md`) says so openly in its first line: every
figure was collected from web-search extracts of those same sources, and *"exact financial-statement
line items (gross profit, SG&A, D&A, interest expense, facility-level debt) were not obtainable
line-by-line; best-available aggregator figures and derived approximations are given and labelled as
such."* The study was built and published anyway, on a disclosed caveat.

Under this rule that run stops at the sweep and asks. Honest labelling is not the remedy — the whole
point of SIGCM is that a forecast built on aggregator approximations is not a Testahil study
regardless of how clearly the approximation is flagged. **Existing studies are not retroactively
withdrawn** (append-only governs, as with the Ke/Kd/WACC scope clause); the gate binds prospectively,
and any name rebuilt for its own reasons rebuilds under it.

### Where it is enforced

- `engine/research_protocol.py` — clause `primary_source_access`, checklist field
  `primary_source_access_confirmed`, and `assert_primary_source_access()`, which raises
  `PrimarySourceUnavailable` rather than returning a degraded build.
- QC gate item **(s)** — evidence is the list of official sources actually read, per statement and
  per period, plus the count of complete financial years obtained against the two-year floor; an
  aggregator appearing as a *build* source is a hard fail.
- The condensed project-instruction block and `Study_Initiation_Prompt.md` both carry the carve-out,
  so the "do not ask me, derive it yourself" default cannot be read as overriding it.

---

## STEP 0 — The calibration gate (before anything else)

Walk-forward backtest over **every non-overlapping window from the market's last structural
break to today**, **h = the calendar 3-month horizon** (see *Horizon convention* immediately
below), scored against a **carry-anchored** lognormal random-walk benchmark (spot × exp(carry);
carry = ln(1+rf) − ln(1+q)), so skill isolates signal and width and can never harvest the
time-value of money.

> **[CORRECTED 04-Aug-2026] This step was described here as a "5-year walk-forward" and never
> was one.** The gate has always scored full post-break history — `primitives` walks every
> non-overlapping window from `min_history`, and `panel_refresh.apply_breaks` then drops
> pre-break origins. Measured on the live fits: EG 16.5 scored windows/name against its
> 2022-03-21 break, IN 57.3/name with no break, XAU 60/name. "Five years" was EGYPT's number
> — its post-break history is 4.4 years, i.e. 17 quarters — mistaken for the engine's. The
> published calibration PANEL *did* wrongly freeze at 17 windows for every market, discarding
> 45 of 62 valid windows for Korea, India, the US and Qatar and 27 of 44 for Saudi; that was
> corrected the same day (`engine/metal_backtest.py`), and the picture now matches the gate.
> This is consistent with, not a change to, MAXIMUM AVAILABLE HISTORY below: the break removes
> structurally invalid data, and everything after it is used.

### [CHANGED 27-Jul-2026] Horizon convention — calendar, not session count

**The two published horizons are 1 MONTH and 3 MONTHS, as calendar objects.** This replaces the
retired session-counted session counts for every cohort struck on or after 27-Jul-2026.

    target_date = anchor_date + 1 (or 3) calendar months, month-end clamped
                  (31-Jan + 1M -> 28/29-Feb)
    grade_date  = the first REAL trading session on or after target_date on that
                  exchange's own calendar; weekend/holiday rolls FORWARD, never back
    h           = the session count spanning that calendar window — NOT a constant
                  (18-24 for a month, 55-67 for a quarter, by market and anchor)

Why: "1 month" is roughly a month and "3 months" roughly a quarter, but the drift landed in the check
DATE. Every public holiday pushed it, so a published `grade_date` was routinely 2 sessions wrong
and needed a manual `grade_note` correction at grade time (PHDC, TMGH and EMFD each carry one). A
calendar target cannot drift; only which session it lands on can, and by at most a few days.

**GRANDFATHERING IS ABSOLUTE.** Cohorts struck before 27-Jul-2026 keep the horizon they were
issued on, grade on it, and count in the score exactly as before. Nothing is re-labelled and
nothing is re-struck — the Calibration Ledger's append-only rule governs, and `horizon_label` is
the field that records which convention a row belongs to.

**Mechanics live in `engine/horizons.py`** — never hand-computed, never assumed:

- Each market's trading calendar is the UNION of session dates across its whole
  `raw_ohlc/{MARKET}/` library, passed through Step 0.0 first. Union, not intersection: one name
  being suspended for a day does not close the exchange.
- The week-mask is derived empirically per market from recent sessions, so a market that changed
  its trading week (ADX/DFM moved Sun–Thu → Mon–Fri in Jan-2022) is described by the week it
  actually keeps now.
- At publish time the target is in the future, so `h` is PROJECTED — the average of a
  session-density leg and a same-season median leg. All three candidates were backtested
  out-of-sample on every market; the blend was adopted because it wins on the loss that matters
  (cone-width error, since width goes as √h): mean 1.33% vs 1.39% seasonal and 1.51% density,
  worst cell 2.84%. Sessions-error alone would have picked seasonal — and would have meant
  selecting a different rule per horizon on the same sample used to score it, which is exactly
  the failure the PROMOTION RULE names. Worst-case residual sits inside the 5% materiality
  threshold and touches only the published cone.
- At GRADE time the projection is discarded. Grading reads the real calendar and grades on the
  actual first session on or after `target_date`.

**In the gate, `h_grade` and `h_size` are NOT the same number** (`mc_v3.calendar_horizons`). The
window ENDS where the calendar says (`h_grade`), but the cone is SIZED on a causally projected
session count (`h_size`) built only from data up to the origin. Using the realized count for both
would put hindsight in the gate: a name suspended for two of the three months has `h_grade ≈ 6`
while any live forecaster would still have sized a full quarter, so scoring that outcome against
a 6-session cone would credit the engine with a cone it could never have drawn. The gap return
stays in the sample and is scored against the quarter-wide cone that was actually issuable.
Carry, likewise, now runs on the EXACT calendar year-fraction rather than h/252 — with a calendar
target the elapsed time is known, so there is no reason to infer it from a session count. (The
legacy fixed-h path keeps h/252 *and its exact floating-point expression order*, so every panel
already on disk still reproduces bit-for-bit — verified on EG/AE/QA/SA/KR.)

Panels are namespaced by horizon set (`{MKT}_{NAME}_60d.csv` vs `_3m.csv`) so the retired gate
stays re-runnable for the grandfathered cohorts and the two calibrations never overwrite each
other.

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

**[NEW 13-Jul r2] The filter is a PRODUCTION rule, and a study script that does not apply it is
WRONG — see the engine-reconciliation rule below.** This was not hypothetical: RMDA's study script
scored all 22 windows, including 9 origins before Egypt's 2023-01-11 break, and reported skill
+1.7% / **PARITY**. Production, applying the filter, scored 13 post-break windows and reported
+2.8% / **robust PASS**. The study was understating its own name, and the error was invisible
because both numbers looked plausible.

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

### [NEW 13-Jul] MAXIMUM AVAILABLE HISTORY — standing rule, decided against a real alternative

**Always calibrate on the maximum available history for a market — 5, 10, 15 years, whatever the
raw OHLC covers — never carve out a shorter "post-shock" or "current regime" sub-period as the
production fit.** This was tested, not asserted: Sherif proposed a genuine two-model design for
Egypt (full 2016→ history vs. post-1-Apr-2024-float only), reasoning that a shorter, calmer window
would be too naive to price a market where devaluation, rate spikes and political shocks recur.

Both regimes were fit and simulated on CLHO (the pilot name, per his instruction to test on one
stock before adopting anything as a procedure) before either was accepted. Result: the two cones
were **not meaningfully different** — median identical at every horizon, and even the tails only
diverged by single-digit percentages, because Egypt's variance is driven by more than the
devaluation calendar (political risk, regional geopolitics, rate policy all load onto the same
tail whether or not a float happened in the sample window). A shorter "calm" window narrows the
cone without actually removing the risk that makes Egypt Egypt — it just removes some of the
*evidence* of that risk from the fit. Conclusion, confirmed independently of (and consistent
with) the 2022-03-21 break-point already adopted market-wide: **more history is better history**
for this market, and by extension the same logic applies to every other covered market — a
shorter window should never be adopted merely because it is calmer or produces a tighter-looking
cone. The corresponding two-regime engine build (dual `MarketProfile.regimes`, both published
side-by-side) was implemented, pilot-tested, and then **closed unmerged** on this evidence
(PR #6).

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

## [NEW 29-Jul] THE TECHNICAL READ IS COMPUTED, AND EVERY BLOCK IS STAMPED

**Retires the roll-forward carve-out that said `levels` and `tech` "need an actual fresh
chart read" and must be left alone.** That rule was written to protect a hand-authored
judgement and in practice protected staleness: on 28-Jul-2026 COMI's live page carried a
142.00 spot beside a narrative reading "the price closed 129.25 below a falling 20-day", with
all three published resistances *below* spot; SAMSUNG's three published *supports* all sat
*above* its spot. A block that is never refreshed is not a preserved judgement — it is an
unmarked expiry date.

**Standing rule: when the library moves, the technical read moves with it, in the same pass.**

    python3 engine/apply_technicals.py --write         # all names
    python3 engine/apply_technicals.py --only COMI     # one name

`engine/technicals.py` computes the read from the same cleaned series `mc_v3` runs on, through
the same Step 0.0 gate — SMA 20/50/200 with slope state, Wilder RSI(14), Wilder ATR(14) on the
true range, MACD(12,26,9), 50/200 cross recency, 52-week range, and S/R from fractal pivots
clustered with a recency weight. Moving averages, the 52-week extremes and round numbers are
admitted as level candidates but score strictly below real swing structure. Prose is templated:
every clause is selected by a computed number. Nothing is fitted or forecast, so the PROMOTION
RULE's out-of-sample test does not apply — there is no free parameter to overfit. Re-running on
an unchanged library is a no-op; the pass is idempotent by construction.

Binding conventions:

- **R1/S1 always mean NEAREST to the close.** The retired hand-authored levels were
  inconsistent about this (TSLA ascending, COMI descending), so R1 meant different things on
  different pages.
- **No fundamental assertions in the technical block.** Some retired narratives closed with a
  valuation sentence ("the equity case rests on a ~30% ROE against a ~24% cost of equity"). A
  deterministic module cannot source that, so it does not say it. Fundamental context belongs
  to the study, the fair-value gauge and the driver stack.
- **`apply_technicals.py` never re-strikes a cone.** It reads the published cone's anchor date
  off the newest LEDGER row for that instrument and its run date off that row's own note, and
  stamps them. Re-striking is a roll-forward decision, never a side effect of a technicals pass.
- **VERIFY BY IMPORT, NOT BY PARSE applies to both new modules**, exactly as it does to
  `market_profiles.py`, `wacc_builder.py`, `research_protocol.py` and `adaptive_width.py`.

### The chart is part of the technical read, not scenery

`engine/ta_chart.py` regenerates the static `<svg id="ta-chart-svg">` on every
ticker page from the same cleaned library. Run it in the SAME pass as
`apply_technicals.py` — refreshing the levels onto a frozen chart is worse than
leaving both stale, which is exactly what 29-Jul-2026 proved: COMI's axis topped
out at 148 against a freshly computed resistance of 160, and `injectLevels` drew
a line at y=-21, outside the viewBox, silently.

    python3 engine/apply_technicals.py --write     # levels, tech, asof
    python3 engine/ta_chart.py --write             # the chart underneath them
    node scripts/check_ta_chart_overlay.js         # the gate below

**The SVG is a contract.** `injectLevels()` recovers price->y by regressing over
the chart's own muted axis labels, and `renderZoomChart()` re-reads the same
element. Change the label markup and both mis-scale without throwing. The
y-range is fitted to the union of the price window, both moving averages AND the
published S/R ladder, so an overlay cannot fall outside the plot by construction.

**MANDATORY GATE — `scripts/check_ta_chart_overlay.js`.** Renders every page with
a chart and fails if any injected level line escapes the viewBox. Nothing else
catches this: no exception is raised, the page looks fine, a level is just gone.
Negative-controlled on the 29-Jul defect — it reports `comi.html … y=-21.2` on
the pre-fix chart and exits 1, and passes on the fix.

### As-of stamps — two dates, never one

Every `TICKERS`/`METALS` entry carries:

    asof: { mc:   { data:"YYYY-MM-DD", computed:"YYYY-MM-DD" },
            tech: { data:"YYYY-MM-DD", computed:"YYYY-MM-DD" } }

`data` = the last session the block was built on. `computed` = the day it was run. A single
"as of" cannot distinguish a block recomputed today on last week's prices from one recomputed
last week — which is exactly the failure being closed. `assets/app.js` renders both stamps off
this field, hooked into `renderStaticFan` (the one function every ticker page already calls),
so no page template needs editing and a new page inherits the stamps automatically.

**Read the stamps as a diagnostic.** When `asof.mc.data` is older than `asof.tech.data`, the
published cone is stale relative to its own library. Report it; never reconcile it silently
inside a technicals pass. The 29-Jul-2026 fan-out surfaced exactly one — 2POINTZERO, cone
anchored 03 Jul against a library running to 24 Jul, page spot 2.16 vs a 2.06 library close.

## [NEW 12-Jul] THE CODE-FIRST RULE — QC gate v2.2 (items n, o, p)

**No financial arithmetic outside executed code.** Every figure that reaches a delivered study
must originate in an executed, asserting compute script — SOTP aggregation, DCF discounting,
bridge algebra, and multiples are never performed in the narrative layer. Adopted 12-Jul-2026 as
the single compatible element of an external QC-architecture prompt; the remainder of that prompt
was rejected on standing rules (its GBM cone is exactly the Step-0 null benchmark, its "Headline
Verdict" breaches the no-rating rule, its third-party identity breaches the branding rule, and a
flat 10–25% holdco discount is inferior to disciplined-SOTP).

**compute.py structure (enforced per study):**
- **INPUTS** — every hardcoded figure is a four-field dict `{value, source, date, ring}`.
  A bare numeral in the inputs block fails the build.
- **CALC** — unchanged from current practice.
- **ASSERT** — the script raises (no study_numbers.json is emitted) unless: the EV→equity bridge
  closes exactly; terminal value as a % of EV is computed and printed (mechanizing device A-7 /
  gate item (g)'s disclosure); implied fair-value-to-spot sits inside a stated plausibility band;
  and net debt and NCI carry the correct signs into the bridge.

**Builders** (docx_*, build_xlsx*) read study_numbers.json exclusively; a numeral typed directly
into a builder script is an item-(n) fail.

**QC gate v2.2 — three rows appended after the existing (a)–(m):**
- **(n) Numeric traceability.** At the existing item-(l) cell-by-cell diff, every number in the
  delivered Word/Excel traces to a study_numbers.json key or a Sweep-Register-logged source.
  Evidence: the trace log with zero orphans.
- **(o) Assertion log.** compute.py's printed ASSERT output pasted verbatim as evidence.
- **(p) Provenance completeness.** The INPUTS block validates four-fields-complete and
  cross-checks against Sweep-Register IDs (extends item (m)'s register validation to the
  compute layer).

**Lettering note (correction on the record):** the session that adopted this rule initially
labeled the new items (j)–(l), working from a stale memory summary describing the gate as
"(a)–(i)". The gate has in fact been (a)–(m) since 11-Jul — (j) probability-read table,
(k) driver-ledger logging, (l) script-reconciliation diff, (m) Sweep-Register validation — so
the code-first items are (n)–(p). Verified against the master file before adoption, per the
standing corrections pattern.

---

## [NEW 06-Aug, per instruction — SWDY study] THE WORKBOOK IS A MODEL, NOT A PRINTOUT

**The delivered Excel must CALCULATE. A number that could be derived from a driver and is instead
pasted is a defect, not a formatting choice.** The code-first rule above governs where numbers
come from (executed, asserting code). This clause governs what the *reader* receives: a workbook
they can trace, interrogate and re-drive — not a screenshot of one.

**What triggered this.** The SWDY workbook shipped with 92 formulas against 764 pasted values, and
its READ FIRST sheet claimed that changing an input repriced the model. It did not: no formula
referenced the Assumptions sheet. The claim was withdrawn and the sheet re-labelled a "register,
not a live driver" — an honest patch to a workbook that should not have needed it. Rebuilt
formula-first the same file carries 589 formulas against 395 values, and the claim is now true and
tested. **A workbook that has to disclaim its own Assumptions sheet has failed.**

**The rule.** Everything arithmetically derivable from an input is a live formula:
- the **cost of capital is built in the workbook** — Ke from the risk-free rate net of the
  sovereign spread, beta and the premium; Kd after tax; weights from net debt and market
  capitalisation; the terminal rate from its own components. Never a pasted rate;
- the **glide and the discount factors are computed**, and the glide fractions are visibly derived
  from the cost-of-debt path so the reader can see the shape is inherited, not invented;
- the **DCF waterfall** chains: margin from EBITDA over revenue, EBIT from EBITDA less D&A, NOPAT
  from EBIT and the tax rate, FCFF from its four components, PV from FCFF and the factor;
- the **terminal block** chains: RR = g / ROIC, TV from terminal NOPAT, RR, the terminal rate and g;
- the **statements chain**: EBIT, PBT, tax, PAT, minorities and attributable profit are formulas in
  the forecast; the balance sheet rolls PPE, working capital, equity and net debt forward; the cash
  flow links to the waterfall; **every ratio and per-share figure on every sheet is a formula.**

**Only three classes of cell may be pasted, and READ FIRST must name them:**
1. **audited and disclosed history** — the primary record, not a calculation. Where a disclosed
   line can also be derived, the DISCLOSED figure is carried (closing SWDY's audited FY2023 account
   arithmetically landed EGP 0.1mn under the printed profit after tax; the print wins);
2. **the unit build's output** — a multi-line volume-and-price model does not survive being
   flattened into a spreadsheet grid. Paste its OUTPUT; everything downstream of it is formula;
3. **whole-model re-runs** — Monte Carlo maps and sensitivity grids, where each individual cell is
   a complete revaluation. These do NOT redraw when a driver changes, and the workbook must say so.

Anything else pasted is a fail. Triangulated figures are shown and averaged **on the sheet** rather
than asserted (SWDY's FY2025 gross debt carries its three methods and an AVERAGE over them).

**Two verification gates, both run on the DELIVERED file:**
- **(q) Cell-level agreement.** The builder records the model's own value for every formula cell as
  it writes them. The recalculation script evaluates the workbook independently and asserts every
  formula cell reproduces it, AND that no formula cell is left unchecked. This is what makes a
  formula-driven workbook safe: a formula that computes the right thing the wrong way, or points
  one row off, fails here instead of shipping a different number from the study. Evidence: "N of N
  formula cells reproduce the model, 0 unchecked."
- **(r) Driver propagation.** A driver test perturbs each input in place, re-evaluates the whole
  workbook from scratch, and asserts the headline moves in the asserted DIRECTION. A dead-input
  sweep bumps every remaining driver and requires it to move something. Evidence: the per-driver
  table. **The live-driver claim on READ FIRST is only permitted once this test passes.**

Both gates earn their keep. On SWDY (q) caught a market-capitalisation formula pointing one row off
its share count — it returned revenue — and (r) forced the depreciation question to be understood
rather than assumed: raising D&A *lowers* the fair value here, because in the terminal state capex
is unchanged, so a permanently higher charge is a business consuming its asset base, and with the
terminal value at 77% of EV that beats the explicit-window tax shield. **When a driver test fails,
the first hypothesis is that the expectation is wrong, not the model — decompose before "fixing".**

**Corollary — one roll-forward per quantity.** Unifying the workbook exposed that the study's
normalised-earnings lens and its financial statements were consuming two different interest paths
that disagreed by up to EGP 117mn, because one was computed before a dependency existed. **A
quantity is computed once and consumed everywhere.** Building the workbook formula-first is a
structural audit of the engine, and defects it surfaces are engine defects, not workbook defects.

**Tooling note.** Recalculation runs through a purpose-built evaluator (`xlcalc.py`) rather than
through the spreadsheet application. Keep the evaluator strict: anything it cannot parse is a
FAILURE, never a skip. Its own sheet-name pattern once allowed hyphens, so
`C34-Assumptions!$C$45` parsed as a reference to a sheet named "C34-Assumptions" and silently
swallowed the subtraction — **a permissive verifier is worse than no verifier.**

The evaluator began as a workaround for LibreOffice failing to load ANY document here. That
diagnosis was wrong and stood for several editions: LibreOffice was installed, but only
`libreoffice-core` — the Writer and Calc import filters were never present, so every conversion
died with "source file could not be loaded". **A tool that fails on every input, including a
trivial CSV, is incomplete, not fussy.** Installing `libreoffice-writer` and `libreoffice-calc`
fixed it, PDFs are now built by `engine/make_pdf.py`, and the evaluator is kept on merit.

---

## [NEW 13-Jul] TERMINAL GROWTH — standing procedure

Adopted from the CLHO (Cleopatra Hospitals Group) terminal-value stress test. Extends QC gate
items (d)/(g). Applies to **every future study with a perpetuity/terminal-value component**.

**What triggered this.** The delivered CLHO study assumed an 11% terminal growth rate funded by a
reinvestment rate of only 16.5% of NOPAT. Back-solving `g = ROIC × RR` for the implied return
(`ROIC = g ÷ RR`) gives an implied terminal ROIC of **67%** — roughly 4x what the study's own
EV-per-bed lens says a new hospital bed actually earns (~16%), and roughly 4x the return realized
in the one clean historical stable year (17.0% ROIC, 2022). The terminal value was not wrong
because 11% was too high in isolation; it was wrong because growth was let through without paying
for the capital it required.

**1. Default terminal g grid.** Center **5%**, sensitized **3% / 4% / 5% / 6% / 7%**, crossed
against a WACC range — never a single point. 5% is the standard analyst convention for
well-established Egyptian/EM companies once currency turbulence and hyperinflation have passed.
This **replaces** any company-specific macro-derived point estimate (e.g. "CBE inflation target +
real growth") as the default center. Deviating from 5% must be **explicitly argued**, not asserted.

**2. Mandatory historical reconciliation table**, built as far back as reliable financials allow:

| Year | Capex | Capex/EBITDA | Character | NOPAT | Actual NOPAT growth | ROIC | RR | Implied g (ROIC×RR) |
|---|---|---|---|---|---|---|---|---|

- **Character** = stable (self-funded, RR<100%) or burst (debt-funded capacity step-change, RR>100%).
- Flag any year sourced from an aggregator rather than the company's own filings.
- ROIC = NOPAT ÷ average invested capital. RR = net reinvestment (capex − D&A, ex-ΔWC) ÷ NOPAT.

**3. Two check numbers, stated explicitly in every report:**
- **(a)** actual historical NOPAT CAGR over the maximum available look-back window, dated and sourced.
- **(b)** the ROIC×RR-implied g computed **only from stable years** — burst/debt-funded years
  (RR>100%) are excluded, with the reason stated: they reflect debt-funded capacity step-changes,
  not steady-state reinvestment, and including them contaminates the identity (a reinvestment rate
  above 100% is financed by new debt, not retained profit, and produces an implied ROIC or implied
  g with no economic meaning).

**4. Framing rule.** Historical actual growth, however high, belongs in the **explicit forecast
years**, describing a specific, dated, disclosed capacity/growth event. The **terminal** rate
describes what happens *after* that story ends and carries a hard, non-negotiable ceiling: it
cannot exceed the long-run nominal growth of the economy the company sits in, else the company
mathematically overtakes total GDP within a finite, checkable horizon. **Show this crossover-year
math** whenever a historical CAGR is floated as a terminal candidate — this is arithmetic
necessity, not a modeling assumption, and is the strongest single disqualifier for an inflated
terminal g.

**5. QC consequence.** A terminal-growth section with no WACC×g grid (center 5%, range 3–7%) +
historical reconciliation table + the two stated check numbers shown as receipts is a **QC FAIL**
going forward.

**6. [NEW 05-Aug, per instruction — ELEC study] TV-share disclosure in the study DOCUMENT.**
The code-first rule already requires terminal value as a % of EV to be computed and printed in
the ASSERT log (engine-side). This clause extends it to the reader-facing deliverables: **every
study presenting a DCF valuation must state the percentage of the valuation coming from the
terminal value in the study document itself** — at minimum (i) as a labelled row in the DCF
EV→equity bridge table, and (ii) in the summary valuation table alongside the DCF lens (both
Word and Excel; the Excel cell links live to the DCF sheet, never typed). A DCF presented
anywhere without its TV share visible to the reader is a QC FAIL (extends gate item (g)).

---

## [NEW 13-Jul] BETA — standing procedure

Adopted from the CLHO WACC beta stress test. Extends the existing `RegressionBetaAttempt`
usability gate (n≥24, R²≥5%, SE(β)<|β|) in `wacc_builder.py`. Applies to **every future study**
that uses a regression beta in the cost-of-equity build.

**What triggered this.** CLHO's regression beta was 0.446 (weekly vs. a 27-name equal-weight EGX
composite, n=103), with R² = 5.9% and SE(β) = 0.177 — clearing the usability gate, but only just.
The implied 90% confidence interval is roughly **[0.15, 0.74]**, a ~5x span top-to-bottom. The gate
correctly allowed the regression instead of defaulting to 1.0; but a beta this weakly identified
needs more than a bare point estimate reaching the report.

**1. Report the full diagnostic triple, always.** n, R², and SE(β), plus the resulting confidence
interval, next to the beta — never the point estimate alone.

**2. Weak-instrument flag.** If R²<10% (within 2x the 5% floor) or the 90% CI (β ± 1.645×SE) spans
more than 2x the point estimate: explicitly label the beta as **statistically weak / wide-CI**, and
never restate it elsewhere in the narrative as if precise (never "beta of 0.446" without the
qualifier, every time it's used to support a conclusion).

**3. Mandatory beta sensitivity table**, spanning at minimum the 90% CI, plus fixed round anchors
for cross-study comparability: **0.6 / 0.8 / 1.0 / 1.15 / 1.3**.

**4. Plausibility cross-check** against **(a)** an unlevered/relevered peer or sector beta where
available, and **(b)** a simple prior (defensive/staple ~0.6–0.9, cyclical/leveraged ~1.0–1.5). If
the regression beta is a clear outlier vs both, state a plausible reason (thin trading, a managed
currency peg dampening observed co-movement, index composition effects, a short listing history)
rather than accepting it at face value.

**5. No silent default to 1.0** — unchanged: only on a genuine gate failure (n<24, R²<5%, or
SE(β)≥|β|), shown with the failed diagnostics that triggered it.

**QC consequence.** A WACC/Ke section stating a beta without the diagnostic triple + CI, the
weak-instrument flag where applicable, the sensitivity table, and the plausibility cross-check
where the beta is an outlier, is a **QC FAIL** going forward.

---

## [NEW 13-Jul r2] KE / KD / WACC — standing procedure

**[NEW 13-Jul r3] SCOPE, stated explicitly before the mechanics.** The sliding schedule is a device for
markets in monetary transition, not a universal replacement for a flat WACC. It applies where the
current risk-free rate sits materially above its own long-run/norm-built level — currently: **Egypt**.
It does **not** apply to currency-pegged markets (UAE, Saudi, Qatar) where the risk-free rate already
sits at its long-run level by construction of the peg — there, today *is* the terminal, the glide
collapses to flat, and applying it produces zero effect while adding needless complexity (measured on
EAND: +0.0%). The sovereign-double-count fix (Ke section, item 3) is a **separate, market-agnostic**
correction and applies everywhere a country ERP is stacked on a local rf, GCC included.

**[NEW 13-Jul r3] APPLICATION: PROSPECTIVE ONLY, NOT RETROSPECTIVE.** This procedure governs every
**new** Egyptian study and every Egyptian study that is next **substantively updated** (a refresh, a
reforecast, a driver revision). It does **not** trigger a mandatory rebuild of the ~27 Egyptian studies
already live. Each of those keeps its published flat-WACC DCF, understated as it may be, until it is
naturally revisited for its own reasons — no name is pulled forward solely to apply this procedure.
This mirrors the append-only rule already governing the Calibration Ledger: corrections attach to the
next cycle, not to history. Adopted after Sherif's explicit instruction, 13-Jul-2026: *"Apply the glide
only in Egypt going forward — not in retrospect."*

Adopted from the RMDA discount-rate stress test (a line-by-line reconciliation of the Testahil DCF
against a published sell-side DCF on the same company). Governs the discount-rate construction in
**every future study**. The prior flat-WACC and flat-two-stage conventions are **RETIRED as primary**.

**What triggered this.** Three separate defects, all found in one study:
1. A **single flat WACC** was applied to both the five explicit years and a perpetuity — which asserts
   that Egypt's cost of capital never normalises, an implausible claim given the CBE's own published
   disinflation path, and one the model's *own* `kd_path` (easing 23.0% → 16.0%) already contradicted
   internally. The study was discounting at a rate its own interest-expense forecast said would fall.
2. Ke stacked a full CDS-based country ERP **on top of an un-netted local-currency risk-free rate** —
   double-charging Egypt's sovereign default risk, which is already the reason the EGP 10Y prints
   22.55% rather than 4–5%.
3. **Kd was taken as the midpoint of a disclosed contractual range** (15–25.27%, FS Note 20 → 20.5%)
   instead of the rate the company actually pays. The paid rate, computed independently, was **24.0%**
   (1Q26 interest ÷ average facilities) — a **350bp understatement** of the single input the whole
   valuation is most convex to.

**1. Sliding schedule — not flat, not two-stage-flat.** Each explicit year is discounted at **that
year's own forward rate**, moving from the explicit-window WACC (Y1) to the terminal WACC (Y5). The
terminal value is capitalised at the terminal WACC and discounted using the **identical cumulative
factor as year 5's cash flow**. `WACC_TERM < WACC_EXP` is a **hard ASSERT**.

**The error this exists to prevent — "two prices for one date."** The common sell-side construction
discounts the explicit years at one rate and then brings the *terminal value alone* home at a much
lower one. Measured on the RMDA comparison: a pound arriving 31-Dec-2030 as a forecast **cash flow**
carried a discount factor of 0.410, while the same pound arriving the same day inside the **terminal
value** carried 0.532 — a **30% premium for relabelling it**. That single inconsistency manufactured
roughly EGP 1.0–1.3 of a EGP 5.35 target. One date, one price of time. Always.

**2. The glide SHAPE is tied to `kd_path`, never invented separately.** Use `kd_path`'s own
cumulative-progress fractions as the WACC glide fractions:

    GLIDE_FRAC[i] = (kd_path[0] - kd_path[i]) / (kd_path[0] - kd_path[-1])
    FWD[i]        = WACC_EXP - (WACC_EXP - WACC_TERM) * GLIDE_FRAC[i]

Ke and Kd then normalise on **one** assumed central-bank easing calendar rather than two independent
judgment calls. Because `kd_path` is typically front-loaded (bigger cuts early, tapering later), the
WACC glide inherits that shape **by construction** — front-loading is not a second free parameter.

**3. Explicit-window Ke — sovereign double-count removed.**

    Ke_explicit = (rf − CDS_spread) + β × ERP_cds     ← PRIMARY
    Ke_raw      =  rf              + β × ERP_cds      ← RETIRED, disclosed only for the audit trail

**4. Terminal Ke/Kd — norm-built, never backed out of a price.** No terminal input is an observable
quote; each is a named, arguable **house macro view**, disclosed as such:
- **Terminal rf** = the central bank's *own stated* medium-term inflation target + a standard EM
  real-rate convention (~5.5pp). Deliberately **not** a raw historical average that cannot be
  re-verified live.
- **Terminal Kd** = the market's long-run corporate-borrowing norm (Egypt: **14–16%**, midpoint 15%
  absent a name-specific reason to deviate).
- **Terminal ERP** = normalised **below** the currently-elevated crisis-era level; never held flat
  into perpetuity.

A terminal rate that is *reverse-engineered from a target price* is the sell-side's quietest lever
and is prohibited outright.

**5. THE KD-INTEGRITY GATE — mandatory, three hard ASSERTs.** A disclosed contractual rate *range's*
midpoint is **NOT sufficient evidence** for Kd and may never be used as Kd on its own. Every study
must show, as evidence rather than narrative:

- **(i) Currency composition of the debt book**, sourced to the facility note — % local vs % foreign
  currency, bank-by-bank where disclosed. A name with meaningful foreign-currency debt gets a
  **currency-blended Kd**; a single-currency shortcut is a fail. *(RMDA: 100% EGP across all 11
  facilities; the FX exposure sits in import payables and LC margins, not in debt — so no cheap-dollar
  blend was available to lower it. The evidence cut **against** the valuation, which is exactly why it
  must be produced rather than assumed.)*
- **(ii) An INDEPENDENTLY computed effective rate** — interest expense ÷ average interest-bearing debt,
  over **at least two periods** — cross-checked against the adopted Kd.
- **(iii) Bounds:** Kd must sit **within 150bp** of the most recent effective-rate check, and may not
  exceed the peak-year effective rate by more than **50bp**.

All three raise. The build **fails**, it does not warn.

**6. Mandatory sensitivity: an explicit-window × terminal-WACC grid**, in addition to the existing
WACC × terminal-g grid, each anchor varied **independently** around its own base. This shows what the
valuation needs *the economy* to do, not merely what growth rate the model needs.

**7. QC consequence.** A WACC/Ke/Kd section without **(a)** the two-anchor schedule shown year-by-year
(forward rate + cumulative discount factor), **(b)** the Kd-integrity evidence triple, **(c)** the
glide-shape disclosure, and **(d)** the explicit × terminal WACC grid, is a **QC FAIL** going forward.

---

## [NEW 06-Aug, per instruction — SWDY study] MULTI-CURRENCY COST OF DEBT — standing procedure

Adopted when SWDY's cost of debt was challenged: its blended Kd of 13.0% is a currency-composition
average across pound, dollar and euro liabilities (28.68% / 6.49% / 3.92% per the audited note),
and an external critique argued the hard-currency legs should instead be loaded with the pound's
own expected depreciation before blending — pushing Kd toward ~19.6%. **Applies to every future
study where a name's debt spans more than one currency.**

**The rule, in two parts, both mandatory whenever the currency-composition basis is used as
primary:**

1. **Always compute and publish the local-currency-equivalent alternative as a VALUE**, never
   merely described. Load the hard-currency debt legs with the local currency's own forecast
   depreciation path under uncovered interest parity — the identical convention already used for
   the currency-of-discounting alternative (never a separately invented depreciation assumption) —
   reblend, and run the DCF at the resulting WACC. Publish the resulting fair value alongside the
   primary, in the same contested-choices table as the other computed alternatives (rating basis,
   NCI sequencing, gross-vs-net debt weights).
2. **Always attach an explicit devaluation-risk caution** next to the currency-composition figure:
   adopting it as primary means the hard-currency debt is carried at its coupon rate and is NOT
   compensated for devaluation beyond what the study's own exchange-rate path already assumes. If
   the currency depreciates faster than that path, the true local-currency cost of servicing that
   debt is understated by construction.

**Compute the effect before calling it material.** SWDY's own case is the cautionary example: the
critique's approximation ("lifts Kd from 13% to roughly 19.6%, genuine and material") was recorded
as material without being run through the model. Computed properly, EGP-equivalent Kd is 18.65%
and the fair-value effect is **−0.65%** (EGP 62.69 vs 63.10) — because net debt carries only 8.08%
of the capital structure, so even a 660-basis-point swing in Kd barely moves the blended WACC
(26.90% → 27.24%). **A currency-composition critique's materiality depends entirely on the debt
weight in the capital structure, which is a company-specific fact, not something to assume from
the size of the rate swing.** State the computed effect plainly, including when — as here — it
turns out to be small: disclosure does not require drama, and a footnote-sized effect dressed up
as material is as much a QC defect as an unpriced one dismissed as immaterial (see
`Critique_Response_Prompt.md`, step 3).

---

## [NEW 13-Jul r2] ENGINE RECONCILIATION — a study may not disagree with production

Adopted after the RMDA publish, where a study script and the production engine were found to be
scoring **different window sets** and therefore reporting **different verdicts** for the same name on
the same day — PARITY in the study, robust PASS in the committed fit.

**The rule.** A study's Step-0 block is not an independent re-derivation and is not free to use its
own methodology. It must **reproduce the committed production fit**, and prove it:

- Read the live fit **before** scoring: `engine/fitted_configs.json` and `engine/market_profiles.py`.
  Never quote a fit from a document, from memory, or from a previous session.
- Apply **every** production transform: `data_quality.clean_ohlc` → `backtest_v3` → **`apply_breaks`**
  (the break filter) → **scale-normalisation** (`crps ÷ spot`) → `robust_verdict` on the *normalized*
  series across bootstrap block sizes **{2, 3, 4}**.
- **A hard ASSERT reconciling the study's recomputed skill and verdict to the committed
  `fitted_configs.json` entry for that name.** The build fails if they diverge.

**Two specific traps this closes**, both live in the RMDA script:
- **Missing break filter** — 9 pre-break origins scored that production excludes (skill +1.7% vs the
  true +2.8%; PARITY vs the true PASS).
- **Wrong CI estimator** — the study used a *calendar*-block bootstrap on the **raw**,
  price-denominated CRPS series; production uses a *moving*-block bootstrap on the **scale-normalized**
  series with a robustness requirement across block sizes. Two different estimators silently answering
  the same question differently.

**Corollary — the site may never contradict the engine.** Before publishing, re-read the live fit. If
a name has entered a panel since the study was built, its verdict, panel membership and (ν, width_cal)
must be refreshed in the document **before** it goes to the site — a study that says "provisional,
not yet in the panel" while the engine says "panel constituent, PASS" is a publication defect, not a
harmless staleness.

---

## UNCHANGED AND STILL BINDING

- **Template:** match TMPV + its Excel exactly. Reference studies by class: EAND (operating-co),
  ADCB (bank, primary), Alpha Dhabi (holdco).
- **Step 2A Information Sweep** — four mandatory rings (Global/Country/Industry/Company),
  classified B/S/D/C — runs BEFORE any forecast driver is set, on every study and every update.
- **Primary-source access gate** — historicals come only from the company's own issued statements
  (its website/IR, the exchange disclosure portal, or the regulator's archive). If they cannot be
  reached, **STOP AND ASK** — never build on aggregators, search extracts or a disclosed caveat.
- **WACC** bottom-up, market-adapted; local govt bond rf even for pegged currencies; ERP from
  Damodaran's *original* file only; genuine beta regression with a real usability gate.
- **Lens by instrument class**; never blend legs that need different methods.
- **DCF waterfall rule** — full build to PV of FCFF shown inline; stopping at FCFF is a hard QC fail.
- **The workbook calculates.** Every derivable figure is a live formula; only audited history, the
  unit build's output and whole-model re-run grids may be pasted, and READ FIRST must name them.
  Gates (q) cell-level agreement and (r) driver propagation both run on the delivered file.
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
3. **Metals is the weakest calibration in the system — say so plainly.** **[CORRECTED
   04-Aug-2026 — this item had inverted since it was written.]** It used to read "Gold is a
   single-name self-fit, and silver is published with no fit of its own — it borrows gold's."
   Both halves are now false: SILVER joined the XAU panel, so gold and silver each receive a
   genuine leave-one-out fit from the other, exactly as IQCD/QNB de-circularised Qatar.
   **PLATINUM is now the circular one** — XPT is a single-name panel, and `panel_refresh` falls
   back to the pooled (i.e. self-) fit when there is no second name to leave out, so platinum's
   verdict grades itself. Merging XPT into XAU was TESTED on 04-Aug and NOT adopted: every
   verdict stays PARITY and platinum's honest skill is −0.13% rather than the self-graded
   +0.78%, but the merged pooled fit narrows gold's published cone 3.3% — the wrong direction
   for a name already covering only 64.7% in the current regime — and widens platinum's 8.9%,
   which trips the materiality gate. The circularity is therefore DISCLOSED on platinum's panel
   rather than traded for a worse cone. A genuine fourth metal (copper) would settle it properly.
   Two names is still a thin panel: metals remains the least-evidenced thing Testahil publishes
   and must not be presented with the confidence of an EGX or GCC name.
4. **UK and Brazil have no covered names**; their profiles are stubs.
5. **[DONE 13-Jul r2 — sweep executed; 4 contradictions found and corrected]** Every covered name's
   published calibration claim was run against the live production fit (65 names carry a fitted
   verdict). **Four contradicted the site**, and they did not all fail in the same direction:
   - **ALPHADHABI was OVER-CLAIMING** — the site described a 9-name UAE panel at ν=4 / width 1.07,
     *a fit that no longer exists*, and called the name PARITY, "a calibrated distribution". Under the
     live 14-name fit (ν=10, width 1.049) it is a **robust FAIL**: skill −1.2%, CI entirely below zero
     at every block size. It had **no calibration disclosure on its coverage page at all**. Now carries
     the FAIL and the illustrative-only framing. Diagnosis: **over-coverage, not mis-centring**
     (50/80/90 = 0.69/0.81/0.94) — i.e. open item 1, the name-level `width_cal` problem, in the wild.
   - **DIB, ISPH, KABO were UNDER-claiming** — all three publish "FAILED its calibration"; all three are
     PARITY under the current fits. Labels corrected, **but the caution was deliberately retained**: all
     three still carry *negative point estimates* (−0.15% / −4.2% / −0.02%), so the cone is not
     demonstrably better than a random walk, merely not provably worse. **A classification technicality
     is never used to upgrade a weak name.**
   **Append-only was respected**: no registered forecast was retro-edited — every percentile and touch
   probability is frozen as published and will be graded against exactly those numbers. Original note
   text is *preserved* with a dated correction appended after it, so the record shows both what was said
   and what was wrong with it. **Standing lesson: a verdict is not a fact you publish once — it is a
   function of a fit that keeps moving, so the site must be re-reconciled against the engine on every
   publish, not only when a study is built.**
6. **[NEW 13-Jul r3, SCOPED — prospective only, per Sherif's explicit instruction]** The Ke/Kd/WACC
   procedure applies to Egypt **going forward**, not retroactively; the ~27 live Egyptian studies are
   **not** queued for a mandatory rebuild (see the SCOPE clause above). The first draft of this item named the GCC reference studies
   (EAND, ADCB, ALPHADHABI). **That was the wrong priority, and measuring it proved so:**
   - **For GCC names the sliding schedule does nothing.** The AED is pegged to the USD and rf 4.30%
     **is already at its long-run norm** — today *is* the terminal, so explicit = terminal and the glide
     collapses to flat. Measured on EAND's published model: **+0.0%**.
   - **What does bite in the GCC is the sovereign double-count fix**, and by more than intuition
     suggests: netting UAE's ~40–55bp default spread out of rf lifts EAND's EV **+4% to +6%**, because
     the WACC−g spread is only **5.1%** and **79% of EV is terminal**. In a low-rate model small rate
     moves are not small.
   - **The real exposure is EGYPT**, where both changes bite hard. Capitalising the terminal at a
     norm-built ~18.8% instead of a flat ~29% lifts the terminal multiple from **4.2× to 7.3×**.
     Measured on RMDA: the DCF lens moved **0.66 → 1.73 (+162%)**. **Every Egyptian DCF still on a flat
     WACC is therefore materially understated**, and there are ~27 of them live.
   **What the earlier measurement remains useful for**: it quantifies the honest cost of *not*
   rebuilding — every live Egyptian DCF is understated by a magnitude roughly like RMDA's (terminal
   multiple 4.2× → 7.3×, DCF lens +162% in RMDA's case, amplified further by leverage on the
   EV→equity bridge since net debt is fixed while EV moves). That number is disclosed here so the
   backlog is a known, sized cost, not a hidden one — but it is a **backlog**, not a queue. If and when
   a name IS next rebuilt for its own reasons, Egypt-market names apply the sliding schedule as a
   matter of course; GCC names apply only the double-count fix. Each rebuild is a full pipeline run
   through the QC gate — none move silently.

---

### [ADDED 29-Jul-2026] Open items surfaced by the as-of stamps

The stamp pass did not create these; it made latent staleness legible on the live pages.

1. **2POINTZERO's published cone is stale relative to its own library.** Anchored 03 Jul at a
   2.16 spot, on a library running to 24 Jul with a 2.06 close — a 4.6% gap. Its two stamps now
   disagree in public. This wants a roll-forward (Step 4), **not** a silent reconciliation.
2. **Stale libraries, now self-reporting on every page.** TMPV and TSLA end 30 Jun; QSE (IQCD,
   QNB, QGTS) 05 Jul; US (AAPL, NVDA) and IN (RELIANCE, INFY) 06 Jul; SILVER 03 Jul; PLATINUM
   20 Jul. Only COMI, EMFD, KAKAO and LGES reach 28 Jul.
3. **The fundamental sentence retired from the technical block** is recoverable if wanted, via
   an optional human `tech_note` that survives refreshes and carries its own date. Considered
   and not taken on 29-Jul — noted here so the choice is visible rather than forgotten.
