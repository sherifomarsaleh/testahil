# TESTAHIL — Standing Research Protocol
### Updated 13 July 2026 (rev. 2) — terminal growth · beta · Ke/Kd/WACC · engine-reconciliation

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
