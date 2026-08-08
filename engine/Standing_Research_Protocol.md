TESTAHIL — Standing Research Protocol
Updated 07 August 2026 (rev. 5) — cost-stack escalation · primary-source financial research
(rev. 4, 29 July 2026 — computed technical read · regenerated charts · as-of stamps)
(rev. 3, 13 July 2026 — value-driver TV · NCI at fair value · one-clock lenses · cross-sheet integrity · the Kd capitalised-interest trap)

This supersedes the 12-July text and both earlier 13-July revisions. Changes new in rev. 5 are marked [NEW 07-Aug]; the [NEW 29-Jul], [NEW 23-Jul], [NEW 21-Jul], [NEW 13-Jul r3], [NEW 13-Jul r2], [NEW 13-Jul] and [NEW 11-Jul] markers are retained for provenance. Everything not marked is unchanged and still binding.

Rev. 5 comes from a line-by-line reconciliation of the Testahil DCF for ARCC (Arabian Cement Company, EGX) against a published EFG Hermes sell-side report on the same company, plus a direct instruction given during that exchange. The reconciliation surfaced a cost-side defect of the same species rev. 3's five procedures closed on the CLHO audit: a number that looked like a forecast disagreement was actually a mechanical artifact of one input choice, invisible until priced out line by line. The instruction added a second procedure strengthening how company-level source material is gathered in the first place, so the next such defect is caught at the sweep stage rather than three revisions later.

Rev. 3 merges two independent workstreams from the same day, and they came from opposite directions. The first — the SCOPE and PROSPECTIVE-ONLY clauses inside the Ke/Kd/WACC section, and the completed calibration sweep in the open items — came from measuring the r2 procedure against the live book and finding it had been mis-scoped (the sliding schedule does nothing in a pegged market; the sovereign double-count fix bites everywhere). The second — the five procedures below — came from an external audit of the delivered CLHO study, which found six structural defects that had all shipped, and every one of which biased the valuation in the same direction: upward. That is not noise. A model whose errors are independent should get some of them wrong in each direction; one whose errors all point the same way has a systematic tilt, and the rules below exist to remove it.

Rev. 2 adds two procedures, both adopted from live failures caught in the RMDA build: a Ke/Kd/WACC standing procedure (the discount rate is a sliding schedule, not a flat number; the sovereign double-count is removed; the terminal anchor is norm-built; and a Kd-integrity gate now blocks the specific error that understated Rameda's cost of debt by 350bp), and an engine-reconciliation rule (a study's Step-0 must reproduce the committed production fit exactly — enforced by assertion, after a study script was found silently scoring windows production excludes).

STEP 0 — The calibration gate (before anything else)

5-year walk-forward backtest on the 3-month calendar window, non-overlapping windows, scored against a carry-anchored lognormal random-walk benchmark (spot × exp(carry); carry = ln(1+rf) − ln(1+q)), so skill isolates signal and width and can never harvest the time-value of money.

[NEW 11-Jul] Step 0.0 — the data-quality gate runs FIRST, before any calibration. engine/data_quality.py::clean_ohlc. No series enters a panel, a fit, or a study without passing it. Two failure modes it exists to catch, both found live in production data:

Pre-listing / non-trading placeholder rows — flat price, no volume. EFIH (e-finance) carried 0.50 placeholders before its Oct-2021 IPO, which the engine read as a +333% one-day return. The Korean vendor export carried ~160 phantom rows per name, of which 144 of Samsung's fell on a Sunday (KOSPI closed) — raw density 276.8 rows/yr against a real calendar of 245.8. These inject fake zero-return, zero-range days straight into the Yang-Zhang variance proxy and depress the volatility estimate.
Unadjusted corporate actions — EFIH's 3:2 split (26-May-2025) and OCDI/SODIC's action (14-Aug-2025, reading as a fake −73% crash). OCDI was inside the live production Egypt fit when this was found.

Detection is principled, not a guessed threshold. Each exchange's own daily price limit defines what a single session can physically do — a move beyond it is not reachable by trading, so it can only be a corporate action or a data error. Thresholds are therefore per-market (EGX ±20%, Tadawul ±10%, ADX ±15%, QE ±10%, KOSPI ±30%, NSE ±20%; US/metals have no limit and use a high threshold). A global threshold is wrong: an EGX-calibrated cutoff would falsely "repair" a legitimate Korean limit-down.

[NEW 11-Jul] STANDING RULE — the calendar screen. When adding a market or a name, screen its trading-day density against that exchange's real calendar before trusting any fit built on it. Vendor corruption is per-export: India was checked against the identical Korean pattern and came back clean, so never assume a vendor is clean because another file from it was.

[NEW 11-Jul] The gate is SCALE-NORMALIZED. CRPS is denominated in price, so pooling raw CRPS across a panel weights every market by share price, not information. Measured live: IHC (382 AED) carried 57.9% of the 14-name UAE panel; ELM (874 SAR) carried 58.7% of Saudi's. A "panel verdict" was arithmetically a one-name verdict. The same defect operated within a name across time (IHC ran 42 → 382, so its late windows outweighed its early ones ~9:1). Every window is now normalized by its own spot before pooling. Effect on the existing record: zero verdict changes, but CIs tighten sharply and headline skills de-inflate — Egypt's pooled PASS restates from +0.059 to +0.039; the old figure was ~50% overstated by TMGH's 42% price weight.

[NEW 11-Jul] Break filtering applies to the CALIBRATION SAMPLE. MarketProfile.breaks was declared on every profile and documented in this protocol but never read by the engine — the rule existed only on paper. Windows whose origin precedes a market's last structural break are now excluded from the fit. Adopted on evidence, not assertion: on Egypt, calibrating post-2023 only beats calibrating on everything out-of-sample (LONO +0.0211 vs +0.0198, both scored on the same post-break windows) and narrows the cone (0.972 → 0.909). Open gap, honestly flagged: the engine's per-origin volatility estimation inside mc_v3 is still not break-aware. Fixing that would move every published distribution and is a deliberate, separate decision.

[NEW 13-Jul r2] The filter is a PRODUCTION rule, and a study script that does not apply it is WRONG — see the engine-reconciliation rule below. This was not hypothetical: RMDA's study script scored all 22 windows, including 9 origins before Egypt's 2023-01-11 break, and reported skill +1.7% / PARITY. Production, applying the filter, scored 13 post-break windows and reported +2.8% / robust PASS. The study was understating its own name, and the error was invisible because both numbers looked plausible.

Verdicts. Three-way and pooled. The name's own bootstrap CI gives PASS/PARITY/FAIL as a diagnostic; the market-panel pooled CI is the standing gate. Proceed if the market panel is PASS or the name is PARITY-or-better. Stop only on a name-level FAIL that is robust across bootstrap block sizes {2,3,4} — a block-dependent sign flip is a BOUNDARY case, recorded PARITY-flagged, never a silent proceed.

THE MC ENGINE — mc_v3.py + market_profiles.py

"Carry-anchored YZ-HAR-t". Gap-aware Yang-Zhang width with a lognormal bias correction and a per-market width_cal; Student-t(ν) shape with ν fitted per market on pooled LONO cross-fitted residuals; drift = carry anchor + an IC-shrunk, dead-zoned, capped signal alpha. 50,000 paths, seed 42. Raw secular drift and unshrunk trend drift remain retired, do-not-revive.

[NEW 11-Jul] Production fits — RULES ONLY, never a number

Do not quote a fit from this document. Every figure below (name counts, window counts, ν, width_cal, verdicts) is exactly what the unattended loop refits every time a stock is posted — they were already stale by the next commit on 11-Jul, and this file is not live-updated by the pipeline. Read the live state before quoting anything:

curl -s https://raw.githubusercontent.com/sherifomarsaleh/testahil/main/engine/market_profiles.py
curl -s https://raw.githubusercontent.com/sherifomarsaleh/testahil/main/engine/fitted_configs.json

No token needed — the repo is public. market_profiles.py is the single source of truth (what production reads); fitted_configs.json is a derived mirror.

What IS stable and worth stating here: eight markets are fitted (Egypt, Saudi, UAE, Qatar, USA, Korea, India, Metals); UK and Brazil have no covered names yet. Egypt is the largest and only panel to reach a robust PASS verdict on the market level. Metals is the weakest calibration in the system (see below) and should never be read with the confidence of an EGX or GCC name.

[NEW 11-Jul] EVERY MARKET NOW RUNS CARRY-ONLY. Egypt's rev_1m was the last active signal anywhere in the system and was ablated off on evidence: on the 27-name panel its empirical IC is +0.018 against a contrarian sign=−1 prior (i.e. the sign is refuted and the magnitude is ~zero); carry-only (+0.0252) beats signal-on (+0.0211); it helped in only 13/25 names on the 25-name panel the test was run against (11-Jul-2026, a fixed historical result, not the current panel size); paired bootstrap P(signal helps) = 0.31. India's mom_12_1 shows the same wrong-sign pattern (IC −0.093 against a +1 prior). Priors are retained in the profiles for re-estimation as panels grow, but signal_active=False everywhere.

[NEW 11-Jul] ν IS WEAKLY IDENTIFIED — never quote it as precise

Likelihood profiling: on the UAE panel every ν from 5 through the Gaussian limit sits inside the 95% interval (ν=4 is only ΔlogL=2.23 away); on Saudi, ν=4–15 are indistinguishable. ν also trades off against width_cal — a fatter tail wants a wider scale to fit the same residuals. The (ν, width_cal) PAIR is what is fitted. Neither coordinate is individually meaningful; the honest object is the cone they jointly produce.

[NEW 11-Jul] THE PROMOTION RULE (standing)

Nothing enters the engine — from a human or from the pipeline — without surviving the same out-of-sample test the forecasts must survive.

Precedent, and the reason this is a rule and not a slogan: selecting (ν, width_cal) by maximising CRPS skill instead of by MLE looked clearly better in-sample (UAE +0.0038 vs the incumbent's −0.0017). Tested honestly leave-one-name-out on two markets, it LOST both times (UAE +0.0021 vs MLE's +0.0032; Saudi −0.0011 vs +0.0008). It overfits. REJECTED — do not revive. What the exercise established was that the incumbent configs were stale, not that the procedure was wrong.

[NEW 11-Jul] THE UNATTENDED LOOP

engine/raw_ohlc/{MARKET}/{TICKER}.csv is a persistent library of every covered stock, not an inbox — 65 stocks across 8 fitted markets (27 EG · 11 SA · 14 AE · 3 QA · 3 US · 3 KR · 3 IN · 1 XAU). To add or refresh ONE stock, add or overwrite ONE file. The pipeline then refits that stock's whole market against the full library.

One-stock post ≈ 12 seconds, even on Egypt (the largest panel — check its current size live): panels are content-hashed (only the changed file rebuilds) and re-scoring uses fast_rescore, a closed-form re-simulation that is bit-for-bit identical to re-running the engine (verified) but skips the O(n²) HAR refit.

Market and ticker are decided by FILE PLACEMENT, never inferred from a filename. This is deliberate — the ADNOC-Gas / ADIB-Egypt-vs-ADIB-UAE class of ambiguity is exactly what must not be automated.

The materiality gate — automation, not unsupervised drift

Auto-commits, no approval: cleaning, panel rebuild, refit, LONO verdicts — provided nothing about the conclusion changed.

STOPS and opens a PR (never auto-merged):

any existing name's verdict category changes
a new name arrives already FAILING (the signal that a file is misfiled or bad)
the published 90% cone moves >5% — measured on width_cal × q95(t(ν)), the band a reader actually sees, not on ν and width_cal separately (they trade off, so watching them individually both misses real changes and fires on noise)
the market-level verdict changes
a panel carries a name with no raw data behind it

A new name is NOT material by itself. Adding coverage is the most common event; blocking on it would mean a review request on every post. Placing the file is the human decision.

Why the gate exists (empirical, not theoretical): on 11-Jul, data cleaning alone flipped Korea's tail from ν=6 to Gaussian and changed two names' robust verdicts. A bare cron job would have shipped both silently.

Guard: market_profiles.py is verified by IMPORT, not ast.parse, before any commit — nu=Gaussian is a bare identifier that parses perfectly and only dies at import. That exact bug reached main on 11-Jul and left the engine unloadable while a digit-only regex check reported it "intact". The workflow now carries an engine import smoke-test.

Sources of truth
engine/market_profiles.py — THE source of truth. This is what production reads.
engine/fitted_configs.json — a derived mirror. Never hand-edit.
engine/panel_hashes.json — a rebuild cache. Never hand-edit.
[NEW 12-Jul] THE CODE-FIRST RULE — QC gate v2.2 (items n, o, p)

No financial arithmetic outside executed code. Every figure that reaches a delivered study must originate in an executed, asserting compute script — SOTP aggregation, DCF discounting, bridge algebra, and multiples are never performed in the narrative layer. Adopted 12-Jul-2026 as the single compatible element of an external QC-architecture prompt; the remainder of that prompt was rejected on standing rules (its GBM cone is exactly the Step-0 null benchmark, its "Headline Verdict" breaches the no-rating rule, its third-party identity breaches the branding rule, and a flat 10–25% holdco discount is inferior to disciplined-SOTP).

compute.py structure (enforced per study):

INPUTS — every hardcoded figure is a four-field dict {value, source, date, ring}. A bare numeral in the inputs block fails the build.
CALC — unchanged from current practice.
ASSERT — the script raises (no study_numbers.json is emitted) unless: the EV→equity bridge closes exactly; terminal value as a % of EV is computed and printed (mechanizing device A-7 / gate item (g)'s disclosure); implied fair-value-to-spot sits inside a stated plausibility band; and net debt and NCI carry the correct signs into the bridge.

Builders (docx_, build_xlsx) read study_numbers.json exclusively; a numeral typed directly into a builder script is an item-(n) fail.

QC gate v2.2 — three rows appended after the existing (a)–(m):

(n) Numeric traceability. At the existing item-(l) cell-by-cell diff, every number in the delivered Word/Excel traces to a study_numbers.json key or a Sweep-Register-logged source. Evidence: the trace log with zero orphans.
(o) Assertion log. compute.py's printed ASSERT output pasted verbatim as evidence.
(p) Provenance completeness. The INPUTS block validates four-fields-complete and cross-checks against Sweep-Register IDs (extends item (m)'s register validation to the compute layer).

Lettering note (correction on the record): the session that adopted this rule initially labeled the new items (j)–(l), working from a stale memory summary describing the gate as "(a)–(i)". The gate has in fact been (a)–(m) since 11-Jul — (j) probability-read table, (k) driver-ledger logging, (l) script-reconciliation diff, (m) Sweep-Register validation — so the code-first items are (n)–(p). Verified against the master file before adoption, per the standing corrections pattern.

[NEW 13-Jul] TERMINAL GROWTH — standing procedure

Adopted from the CLHO (Cleopatra Hospitals Group) terminal-value stress test. Extends QC gate items (d)/(g). Applies to every future study with a perpetuity/terminal-value component.

What triggered this. The delivered CLHO study assumed an 11% terminal growth rate funded by a reinvestment rate of only 16.5% of NOPAT. Back-solving g = ROIC × RR for the implied return (ROIC = g ÷ RR) gives an implied terminal ROIC of 67% — roughly 4x what the study's own EV-per-bed lens says a new hospital bed actually earns (~16%), and roughly 4x the return realized in the one clean historical stable year (17.0% ROIC, 2022). The terminal value was not wrong because 11% was too high in isolation; it was wrong because growth was let through without paying for the capital it required.

1. Default terminal g grid. Center 5%, sensitized 3% / 4% / 5% / 6% / 7%, crossed against a WACC range — never a single point. 5% is the standard analyst convention for well-established Egyptian/EM companies once currency turbulence and hyperinflation have passed. This replaces any company-specific macro-derived point estimate (e.g. "CBE inflation target + real growth") as the default center. Deviating from 5% must be explicitly argued, not asserted.

2. Mandatory historical reconciliation table, built as far back as reliable financials allow:

Year	Capex	Capex/EBITDA	Character	NOPAT	Actual NOPAT growth	ROIC	RR	Implied g (ROIC×RR)
Character = stable (self-funded, RR<100%) or burst (debt-funded capacity step-change, RR>100%).
Flag any year sourced from an aggregator rather than the company's own filings.
ROIC = NOPAT ÷ average invested capital. RR = net reinvestment (capex − D&A, ex-ΔWC) ÷ NOPAT.

3. Two check numbers, stated explicitly in every report:

(a) actual historical NOPAT CAGR over the maximum available look-back window, dated and sourced.
(b) the ROIC×RR-implied g computed only from stable years — burst/debt-funded years (RR>100%) are excluded, with the reason stated: they reflect debt-funded capacity step-changes, not steady-state reinvestment, and including them contaminates the identity (a reinvestment rate above 100% is financed by new debt, not retained profit, and produces an implied ROIC or implied g with no economic meaning).

4. Framing rule. Historical actual growth, however high, belongs in the explicit forecast years, describing a specific, dated, disclosed capacity/growth event. The terminal rate describes what happens after that story ends and carries a hard, non-negotiable ceiling: it cannot exceed the long-run nominal growth of the economy the company sits in, else the company mathematically overtakes total GDP within a finite, checkable horizon. Show this crossover-year math whenever a historical CAGR is floated as a terminal candidate — this is arithmetic necessity, not a modeling assumption, and is the strongest single disqualifier for an inflated terminal g.

5. QC consequence. A terminal-growth section with no WACC×g grid (center 5%, range 3–7%) + historical reconciliation table + the two stated check numbers shown as receipts is a QC FAIL going forward.

[NEW 13-Jul] BETA — standing procedure

Adopted from the CLHO WACC beta stress test. Extends the existing RegressionBetaAttempt usability gate (n≥24, R²≥5%, SE(β)<|β|) in wacc_builder.py. Applies to every future study that uses a regression beta in the cost-of-equity build.

What triggered this. CLHO's regression beta was 0.446 (weekly vs. a 27-name equal-weight EGX composite, n=103), with R² = 5.9% and SE(β) = 0.177 — clearing the usability gate, but only just. The implied 90% confidence interval is roughly [0.15, 0.74], a ~5x span top-to-bottom. The gate correctly allowed the regression instead of defaulting to 1.0; but a beta this weakly identified needs more than a bare point estimate reaching the report.

1. Report the full diagnostic triple, always. n, R², and SE(β), plus the resulting confidence interval, next to the beta — never the point estimate alone.

2. Weak-instrument flag. If R²<10% (within 2x the 5% floor) or the 90% CI (β ± 1.645×SE) spans more than 2x the point estimate: explicitly label the beta as statistically weak / wide-CI, and never restate it elsewhere in the narrative as if precise (never "beta of 0.446" without the qualifier, every time it's used to support a conclusion).

3. Mandatory beta sensitivity table, spanning at minimum the 90% CI, plus fixed round anchors for cross-study comparability: 0.6 / 0.8 / 1.0 / 1.15 / 1.3.

4. Plausibility cross-check against (a) an unlevered/relevered peer or sector beta where available, and (b) a simple prior (defensive/staple ~0.6–0.9, cyclical/leveraged ~1.0–1.5). If the regression beta is a clear outlier vs both, state a plausible reason (thin trading, a managed currency peg dampening observed co-movement, index composition effects, a short listing history) rather than accepting it at face value.

5. No silent default to 1.0 — unchanged: only on a genuine gate failure (n<24, R²<5%, or SE(β)≥|β|), shown with the failed diagnostics that triggered it.

QC consequence. A WACC/Ke section stating a beta without the diagnostic triple + CI, the weak-instrument flag where applicable, the sensitivity table, and the plausibility cross-check where the beta is an outlier, is a QC FAIL going forward.

[NEW 13-Jul r2] KE / KD / WACC — standing procedure

[NEW 13-Jul r3] SCOPE, stated explicitly before the mechanics. The sliding schedule is a device for markets in monetary transition, not a universal replacement for a flat WACC. It applies where the current risk-free rate sits materially above its own long-run/norm-built level — currently: Egypt. It does not apply to currency-pegged markets (UAE, Saudi, Qatar) where the risk-free rate already sits at its long-run level by construction of the peg — there, today is the terminal, the glide collapses to flat, and applying it produces zero effect while adding needless complexity (measured on EAND: +0.0%). The sovereign-double-count fix (Ke section, item 3) is a separate, market-agnostic correction and applies everywhere a country ERP is stacked on a local rf, GCC included.

[NEW 13-Jul r3] APPLICATION: PROSPECTIVE ONLY, NOT RETROSPECTIVE. This procedure governs every new Egyptian study and every Egyptian study that is next substantively updated (a refresh, a reforecast, a driver revision). It does not trigger a mandatory rebuild of the ~27 Egyptian studies already live. Each of those keeps its published flat-WACC DCF, understated as it may be, until it is naturally revisited for its own reasons — no name is pulled forward solely to apply this procedure. This mirrors the append-only rule already governing the Calibration Ledger: corrections attach to the next cycle, not to history. Adopted after Sherif's explicit instruction, 13-Jul-2026: "Apply the glide only in Egypt going forward — not in retrospect."

Adopted from the RMDA discount-rate stress test (a line-by-line reconciliation of the Testahil DCF against a published sell-side DCF on the same company). Governs the discount-rate construction in every future study. The prior flat-WACC and flat-two-stage conventions are RETIRED as primary.

What triggered this. Three separate defects, all found in one study:

A single flat WACC was applied to both the five explicit years and a perpetuity — which asserts that Egypt's cost of capital never normalises, an implausible claim given the CBE's own published disinflation path, and one the model's own kd_path (easing 23.0% → 16.0%) already contradicted internally. The study was discounting at a rate its own interest-expense forecast said would fall.
Ke stacked a full CDS-based country ERP on top of an un-netted local-currency risk-free rate — double-charging Egypt's sovereign default risk, which is already the reason the EGP 10Y prints 22.55% rather than 4–5%.
Kd was taken as the midpoint of a disclosed contractual range (15–25.27%, FS Note 20 → 20.5%) instead of the rate the company actually pays. The paid rate, computed independently, was 24.0% (1Q26 interest ÷ average facilities) — a 350bp understatement of the single input the whole valuation is most convex to.

1. Sliding schedule — not flat, not two-stage-flat. Each explicit year is discounted at that year's own forward rate, moving from the explicit-window WACC (Y1) to the terminal WACC (Y5). The terminal value is capitalised at the terminal WACC and discounted using the identical cumulative factor as year 5's cash flow. WACC_TERM < WACC_EXP is a hard ASSERT.

The error this exists to prevent — "two prices for one date." The common sell-side construction discounts the explicit years at one rate and then brings the terminal value alone home at a much lower one. Measured on the RMDA comparison: a pound arriving 31-Dec-2030 as a forecast cash flow carried a discount factor of 0.410, while the same pound arriving the same day inside the terminal value carried 0.532 — a 30% premium for relabelling it. That single inconsistency manufactured roughly EGP 1.0–1.3 of a EGP 5.35 target. One date, one price of time. Always.

2. The glide SHAPE is tied to kd_path, never invented separately. Use kd_path's own cumulative-progress fractions as the WACC glide fractions:

GLIDE_FRAC[i] = (kd_path[0] - kd_path[i]) / (kd_path[0] - kd_path[-1])
FWD[i]        = WACC_EXP - (WACC_EXP - WACC_TERM) * GLIDE_FRAC[i]

Ke and Kd then normalise on one assumed central-bank easing calendar rather than two independent judgment calls. Because kd_path is typically front-loaded (bigger cuts early, tapering later), the WACC glide inherits that shape by construction — front-loading is not a second free parameter.

3. Explicit-window Ke — sovereign double-count removed.

Ke_explicit = (rf − CDS_spread) + β × ERP_cds     ← PRIMARY
Ke_raw      =  rf              + β × ERP_cds      ← RETIRED, disclosed only for the audit trail

4. Terminal Ke/Kd — norm-built, never backed out of a price. No terminal input is an observable quote; each is a named, arguable house macro view, disclosed as such:

Terminal rf = the central bank's own stated medium-term inflation target + a standard EM real-rate convention (~5.5pp). Deliberately not a raw historical average that cannot be re-verified live.
Terminal Kd = the market's long-run corporate-borrowing norm (Egypt: 14–16%, midpoint 15% absent a name-specific reason to deviate).
Terminal ERP = normalised below the currently-elevated crisis-era level; never held flat into perpetuity.

A terminal rate that is reverse-engineered from a target price is the sell-side's quietest lever and is prohibited outright.

5. THE KD-INTEGRITY GATE — mandatory, three hard ASSERTs. A disclosed contractual rate range's midpoint is NOT sufficient evidence for Kd and may never be used as Kd on its own. Every study must show, as evidence rather than narrative:

(i) Currency composition of the debt book, sourced to the facility note — % local vs % foreign currency, bank-by-bank where disclosed. A name with meaningful foreign-currency debt gets a currency-blended Kd; a single-currency shortcut is a fail. (RMDA: 100% EGP across all 11 facilities; the FX exposure sits in import payables and LC margins, not in debt — so no cheap-dollar blend was available to lower it. The evidence cut against the valuation, which is exactly why it must be produced rather than assumed.)
(ii) An INDEPENDENTLY computed effective rate — interest expense ÷ average interest-bearing debt, over at least two periods — cross-checked against the adopted Kd.
(iii) Bounds: Kd must sit within 150bp of the most recent effective-rate check, and may not exceed the peak-year effective rate by more than 50bp.

All three raise. The build fails, it does not warn.

6. Mandatory sensitivity: an explicit-window × terminal-WACC grid, in addition to the existing WACC × terminal-g grid, each anchor varied independently around its own base. This shows what the valuation needs the economy to do, not merely what growth rate the model needs.

7. QC consequence. A WACC/Ke/Kd section without (a) the two-anchor schedule shown year-by-year (forward rate + cumulative discount factor), (b) the Kd-integrity evidence triple, (c) the glide-shape disclosure, and (d) the explicit × terminal WACC grid, is a QC FAIL going forward.

[NEW 13-Jul r2] ENGINE RECONCILIATION — a study may not disagree with production

Adopted after the RMDA publish, where a study script and the production engine were found to be scoring different window sets and therefore reporting different verdicts for the same name on the same day — PARITY in the study, robust PASS in the committed fit.

The rule. A study's Step-0 block is not an independent re-derivation and is not free to use its own methodology. It must reproduce the committed production fit, and prove it:

Read the live fit before scoring: engine/fitted_configs.json and engine/market_profiles.py. Never quote a fit from a document, from memory, or from a previous session.
Apply every production transform: data_quality.clean_ohlc → backtest_v3 → apply_breaks (the break filter) → scale-normalisation (crps ÷ spot) → robust_verdict on the normalized series across bootstrap block sizes {2, 3, 4}.
A hard ASSERT reconciling the study's recomputed skill and verdict to the committed fitted_configs.json entry for that name. The build fails if they diverge.

Two specific traps this closes, both live in the RMDA script:

Missing break filter — 9 pre-break origins scored that production excludes (skill +1.7% vs the true +2.8%; PARITY vs the true PASS).
Wrong CI estimator — the study used a calendar-block bootstrap on the raw, price-denominated CRPS series; production uses a moving-block bootstrap on the scale-normalized series with a robustness requirement across block sizes. Two different estimators silently answering the same question differently.

Corollary — the site may never contradict the engine. Before publishing, re-read the live fit. If a name has entered a panel since the study was built, its verdict, panel membership and (ν, width_cal) must be refreshed in the document before it goes to the site — a study that says "provisional, not yet in the panel" while the engine says "panel constituent, PASS" is a publication defect, not a harmless staleness.

[NEW 13-Jul r3] SCOPE OF THE FIVE PROCEDURES BELOW — market-agnostic, all of them

The sliding-schedule scope clause above is deliberately narrow: it applies to markets in monetary transition and collapses to nothing under a peg. The five procedures that follow carry no such limitation. A terminal value that pays for growth it never funds, a minority interest deducted at book, a forward multiple read as a present value, two statements that disagree about cash, and a cost of debt computed from an income statement that never saw most of the interest — none of these are Egyptian problems. They are arithmetic and accounting problems, and they apply to every study in every market, GCC and EM alike. They are stated here so nobody re-scopes them the way the glide was initially mis-scoped.

[NEW 13-Jul r3] TERMINAL VALUE — the value-driver formula is mandatory

The failure. The CLHO study capitalised final-year FCFF directly: TV = FCFF_N × (1+g) / (WACC−g). That looks neutral. It is not. It silently adopts whatever reinvestment rate happens to fall out of the capex and D&A lines — in CLHO's case 14.6% of NOPAT — and a 5% growth rate funded by reinvesting only 14.6% of profit requires a return on capital of 34.2%, forever. The study then asserted that this figure sat "inside CLHO's realized book-ROIC range of 17.0–23.0%." It does not. 34.2% is far above anything the company has ever earned. The claim was false, it shipped, and an external auditor found it.

The rule. Terminal value is built with the value-driver formula, always:

TV = NOPAT_{N+1} × (1 − g / ROIC_terminal) / (WACC_terminal − g)

Terminal reinvestment is no longer a free input. It is forced to RR = g / ROIC, so the identity g = ROIC × RR — already mandated by the 13-Jul terminal-growth procedure — now holds by construction rather than by assertion. ROIC_terminal is a named, argued input, anchored on the company's own realized ROIC and its marginal return on new capacity, and sensitized. A terminal value that does not state its implied ROIC, and show that ROIC inside a range the company has actually earned, is a QC FAIL.

Note the interaction with the r2 glide: on a name already running a two-stage WACC the glide moves little, so do not expect the r2 uplift and this haircut to net out. On CLHO they did not — the discount rate barely moved (25.15%/17.87% vs 25.23%/17.80%) while the terminal discipline cut the DCF outright.

[NEW 13-Jul r3] NCI — deduct at FAIR VALUE, never at book

The failure. The CLHO bridge deducted non-controlling interests at book value (EGP 452.8mn). But the DCF capitalises 100% of subsidiary cash flow, so the minority's claim on that cash flow must come out at what it is worth, not what it historically cost. Fair value was ~EGP 780mn. The error inflated parent equity by roughly EGP 330mn — and it inflates it in every consolidated study with minorities, which is most of them.

The rule. Identify which subsidiaries carry the minority (CLHO: ~92% of all NCI sits in one hospital, 57.01% owned), value those subsidiaries on their own disclosed economics, and deduct the minority percentage of that. Do not apply the NCI's share of group profit to group EV — that applies an equity share to an enterprise number, and it also hands the minority a share of growth assets it does not own. Book NCI may be shown for reference; it may never be the deduction. Disclose the uniform-share alternative as a sensitivity, since it is the more punitive read and the reader is entitled to both.

[NEW 13-Jul r3] ONE CLOCK — every lens in the blend must be a present value

The failure. The CLHO central estimate blended four lenses denominated in different units of time: a DCF (a value today), a multiple on FY27E earnings (a value at end-2027), and a transaction mark on 1,320 beds that do not exist yet (a value in 2027). Three of four were forward figures read as present ones. The study's own two-clocks rule already forbade this and it happened anyway.

The rule. Any lens applied to forward earnings or forward capacity is discounted back to today — the earnings lens at Ke, the capacity lens at WACC — before it enters the blend. The undiscounted forward reading is disclosed alongside, labelled for what it is (a full-execution ceiling), never blended. A blend that mixes clocks is a QC FAIL.

Corollary — an equity multiple may only be applied to a POST-interest number. The CLHO normalized-earnings lens added net interest back (producing NOPAT — an unlevered figure) and then applied a P/E to it: it capitalised debt-free earnings and never deducted the debt. If the intent is to strip a temporary rate spike, re-price the interest at the long-run Kd — do not delete it.

Corollary — a transaction mark must be anchored to the subject market's cost of capital. CLHO's per-bed lens imported Gulf marks (~27.5mn/bed) into a 25% discount-rate country, implying a ~10.7% unlevered return on a bed. Re-anchored on CLHO's own disclosed build cost (EGP 17.2mn/bed) the mark falls to roughly 1.0× replacement — which is what a ROIC of 17–23% against a ~17.9% WACC actually supports. Adopt the machinery, not the optimism — the EFG portable lesson — applies to transaction comparables as much as to driver trees.

[NEW 13-Jul r3] CROSS-SHEET INTEGRITY — the statements must agree with each other (QC gate item (q))

The failure. The CLHO model's Cash Flow statement and Balance Sheet computed cash on different definitions and disagreed by ~EGP 440mn per year, every forecast year. The Balance Sheet carried cash as the plug; the Cash Flow derived it from a top-down working-capital driver and ignored the tax-payable, provisions and debt-base movements entirely. Both sheets shipped. The QC gate never looked — item (l) checks scripts against the delivered file, and it never checked the statements against each other. A clean recalc and a clean script-diff were both true of the broken model.

The rule — new QC gate item (q). Every model with a three-statement build carries a hard, visible, per-year tie-out:

Δcash (Cash Flow statement)  ==  Δcash (Balance Sheet cash line, y/y)      → ASSERT, every year

The Cash Flow's working-capital and liability movements are derived from the Balance Sheet's own lines, not from a separate driver. Zero recalc errors and a clean cell-by-cell diff are necessary and not sufficient — the gate must also prove the statements agree with each other.

[NEW 13-Jul r3] THE KD CAPITALISED-INTEREST TRAP — extends the r2 §5 gate

The failure. r2 §5(ii) requires an independently computed effective rate = interest expense ÷ average interest-bearing debt. Run naively on CLHO it returns 7.7% — against an adopted Kd of ~20%. A 1,300bp miss that would have failed the gate and sent the analyst chasing a phantom.

The number is a fiction. Most of CLHO's economic interest never touched the income statement: it was capitalised into projects under construction. The FY2024 audited accounts put the capitalised balance at EGP 386.2mn against EGP 40.6mn a year earlier — a flow of EGP 345.6mn, nearly three times the EGP 122.0mn that reached the P&L. Add it back and the true effective rate is 30.3%, which corroborates the 28.90% contractual rate the company discloses in the very same accounts.

The rule. The effective-rate check of r2 §5(ii) is computed on economic interest:

effective Kd = (P&L interest expense + interest CAPITALISED into PP&E) ÷ average interest-bearing debt

Source the capitalised-interest flow from the fixed-assets note, always. A capex-heavy company mid-construction will ALWAYS understate its cost of debt on a P&L-only basis — and those are precisely the companies whose valuations are most convex to it. Where policy rates have moved materially between the last audited year-end and the valuation date, the §5(iii) bound is applied to the rate-adjusted check (the audited spread over the contemporaneous policy corridor, carried forward to today's corridor), and both the raw and the adjusted checks are shown as evidence.

[NEW 29-Jul] THE TECHNICAL READ IS COMPUTED, THE CHART IS REGENERATED, AND EVERY BLOCK IS STAMPED

Retires the roll-forward carve-out that said levels and tech "need an actual fresh chart read" and must be left alone. That rule was written to protect a hand-authored judgement and in practice protected staleness: on 28-Jul-2026 COMI's live page carried a 142.00 spot beside a narrative reading "the price closed 129.25 below a falling 20-day", with all three published resistances BELOW spot; SAMSUNG's three published supports all sat ABOVE its spot. A block that is never refreshed is not a preserved judgement — it is an unmarked expiry date.

The rule. When the library moves, the technical read moves with it, in the same pass — levels, narrative AND the chart underneath them.

  python3 engine/apply_technicals.py --write     # levels, tech, asof
  python3 engine/ta_chart.py        --write      # the chart underneath them
  node scripts/check_ta_chart_overlay.js         # mandatory gate

engine/technicals.py computes the read from the same cleaned series mc_v3 runs on, through the same Step 0.0 gate: SMA 20/50/200 with slope state, Wilder RSI(14), Wilder ATR(14) on the true range, MACD(12,26,9), 50/200 cross recency, 52-week range, and S/R from fractal pivots clustered with a recency weight. Moving averages, the 52-week extremes and round numbers are admitted as level candidates but score strictly below real swing structure. Prose is templated — every clause is selected by a computed number.

THE PROMOTION RULE DOES NOT APPLY HERE, and the reason matters: nothing is fitted, so there is no free parameter to overfit. The pass is idempotent — re-running on an unchanged library is a no-op.

Binding conventions. R1/S1 ALWAYS mean nearest to the close (the retired hand-authored levels were inconsistent — TSLA ascending, COMI descending, so R1 meant different things on different pages). NO FUNDAMENTAL ASSERTIONS in a technical block: a deterministic module cannot source "ROE against cost of equity", so it does not say it — that context belongs to the study, the fair-value gauge and the driver stack. apply_technicals NEVER re-strikes a cone; it reads the published cone's anchor off the newest LEDGER row and its run date off that row's own note, and stamps them. Re-striking is a roll-forward decision.

THE CHART IS PART OF THE READ, NOT SCENERY. engine/ta_chart.py regenerates the static <svg id="ta-chart-svg"> and its figcaption from the same library. Refreshing levels onto a frozen chart is WORSE than leaving both stale — measured, not hypothetical: COMI's axis topped out at 148, captioned "last 500 sessions to 29 Jun 2026", against a freshly computed resistance of 160, and injectLevels drew that line at y=−21, outside the 0..320 viewBox. No exception, no console error, the page looked fine, the level was simply gone. THE SVG IS A CONTRACT: injectLevels() recovers price→y by regressing over the chart's own muted axis labels and renderZoomChart() re-reads the same element, so changing the label markup silently mis-scales both. The y-range is fitted to the union of the price window, both moving averages AND the published S/R ladder, so an overlay cannot escape the plot by construction rather than by anyone remembering to look.

MANDATORY GATE — scripts/check_ta_chart_overlay.js. Renders every page carrying a chart and fails (exit 1) if any injected level line escapes the viewBox. Nothing else catches this failure mode. NEGATIVE-CONTROLLED before being trusted: restoring the pre-fix comi.html makes it report "comi.html … y=-21.2" and exit 1; the fix makes it pass and exit 0. A gate never seen to fail is not evidence.

AS-OF STAMPS — TWO DATES, NEVER ONE. Every TICKERS/METALS entry carries asof:{mc:{data,computed}, tech:{data,computed}}. data = the last session the block was built on; computed = the day it was run. A single "as of" cannot distinguish a block recomputed today on last week's prices from one recomputed last week — exactly the failure being closed. assets/app.js renders both off renderStaticFan, the one function every ticker page already calls, so no page template needs editing and a new page inherits the stamps. READ THE STAMPS AS A DIAGNOSTIC: asof.mc.data older than asof.tech.data means the published cone is stale relative to its own library — report it, never reconcile it silently inside a technicals pass.

Two verification rules earned here, binding on every assets/data.js write:

(1) node --check on data.js and app.js, then LOAD data.js in node and assert on the parsed TICKERS/LEDGER objects. An assert-guarded string replacement verifies the old text existed; it cannot see whether the surrounding structure survived. A missing comma before an appended LEDGER row is valid-looking text and invalid JavaScript — the JS analogue of the nu=Gaussian import trap above.

(2) COUNT AGAINST A KNOWN TOTAL — never trust a tool's own "0 skipped". A regex matching unquoted object keys only silently dropped "2POINTZERO" (which MUST be quoted; a JS identifier cannot start with a digit) from THREE separate tools, each reporting success. In apply_rollforward that dropped it from the 28-Jul market-wide re-strike — 58 cones where EG 30 + AE 18 + SA 11 = 59 — which is why its published cone sat three weeks behind its own library until 29-Jul.

Engine guard list now reads: market_profiles.py, wacc_builder.py, research_protocol.py, adaptive_width.py, technicals.py, apply_technicals.py, ta_chart.py, rollforward_one.py — all verified by IMPORT, not parse.

Single-name roll-forwards use engine/rollforward_one.py. apply_rollforward.py is the RECORD of the 28-Jul market-wide pass — its header comment and per-row note are hardcoded to that pass, so re-running it for one name stamps today's cohort with last week's story.


UNCHANGED AND STILL BINDING
Template [CHANGED 08-Aug — see THE MODEL STUDY entry below]: match the MODEL STUDY — SWDY_Valuation_Study_05-08-2026 + its Excel + its standalone bibliography document — exactly, in structure AND research depth. TMPV is retired as the structural template and EAND as the operating-co exemplar (one-in-one-out). Lens-pattern references by class: SWDY (operating-co), ADCB (bank, primary), Alpha Dhabi (holdco).
Step 2A Information Sweep — four mandatory rings (Global/Country/Industry/Company), classified B/S/D/C — runs BEFORE any forecast driver is set, on every study and every update.
WACC bottom-up, market-adapted; local govt bond rf even for pegged currencies; ERP from Damodaran's original file only; genuine beta regression with a real usability gate.
Lens by instrument class; never blend legs that need different methods.
DCF waterfall rule — full build to PV of FCFF shown inline; stopping at FCFF is a hard QC fail.
Expert appendix — three experts, genuinely different methods, a falsifier each.
Ledgers are append-only. No published forecast is ever retro-edited.
Never a rating or a price target. Fair-value ranges and distributions only.
OPEN ITEMS (honestly ranked)
[ADOPTED 23-Jul — EG only, history-gated; see "ADAPTIVE PER-STOCK WIDTH OVERLAY" below] Name-level width_cal, shrunk toward the market fit. This was the real answer to the "bands are too broad" complaint. Both robust FAILs at the time this item was written failed for the SAME reason and it was not mis-centring — they were over-covered: LGES had cov80 = 1.00 and cov90 = 1.00 (every single outcome inside the 80% band), a cone 1.11× the benchmark, and a PIT of 0.471 (perfectly centred). ALPHADHABI was the same shape. A market-level cone over-widens any name whose own volatility sits below the panel average. The overlay cleared a strict LONO/held-out gate on the 30-name EG panel (block bootstrap {2,3,4}) — proper-score parity, improved calibration — and now lives in the engine, EG-only, forced to exact baseline (mult=1.0) on any name with fewer than 28 resolved 3-month windows of history. Other markets have not been tested and remain on the market-level cone until each clears the same gate on its own panel.
Break-aware volatility estimation inside the engine (currently only the calibration sample is filtered). Moves every published distribution — a deliberate decision, not a silent fix.
Metals is the weakest calibration in the system — say so plainly. Gold is a single-name self-fit: it is calibrated on its own data, so its PARITY verdict is circular in exactly the way Qatar's was until IQCD and QNB de-circularised it. Worse, silver is a PUBLISHED instrument with no fit of its own — it borrows gold's. Every other market has been pulled onto a real panel; metals has not. Until silver/copper/platinum history arrives, the metals cone is the least-evidenced thing Testahil publishes, and it should not be presented with the same confidence as an EGX or GCC name.
UK and Brazil have no covered names; their profiles are stubs.
[NEW 29-Jul] Eleven libraries are STALE, and now self-report it on every page via the tech as-of stamp — TMPV/RELIANCE/INFY (IN), TSLA/AAPL/NVDA (US), IQCD/QNB/QGTS (QA), SILVER, PLATINUM. The stamp made latent staleness legible; it did not create it. A fresh vendor export placed at engine/raw_ohlc/{MARKET}/{TICKER}.csv is the only fix — nothing else unblocks them.
[DONE 13-Jul r2 — sweep executed; 4 contradictions found and corrected] Every covered name's published calibration claim was run against the live production fit (65 names carry a fitted verdict). Four contradicted the site, and they did not all fail in the same direction:
ALPHADHABI was OVER-CLAIMING — the site described a 9-name UAE panel at ν=4 / width 1.07, a fit that no longer exists, and called the name PARITY, "a calibrated distribution". Under the live 14-name fit (ν=10, width 1.049) it is a robust FAIL: skill −1.2%, CI entirely below zero at every block size. It had no calibration disclosure on its coverage page at all. Now carries the FAIL and the illustrative-only framing. Diagnosis: over-coverage, not mis-centring (50/80/90 = 0.69/0.81/0.94) — i.e. open item 1, the name-level width_cal problem, in the wild.
DIB, ISPH, KABO were UNDER-claiming — all three publish "FAILED its calibration"; all three are PARITY under the current fits. Labels corrected, but the caution was deliberately retained: all three still carry negative point estimates (−0.15% / −4.2% / −0.02%), so the cone is not demonstrably better than a random walk, merely not provably worse. A classification technicality is never used to upgrade a weak name. Append-only was respected: no registered forecast was retro-edited — every percentile and touch probability is frozen as published and will be graded against exactly those numbers. Original note text is preserved with a dated correction appended after it, so the record shows both what was said and what was wrong with it. Standing lesson: a verdict is not a fact you publish once — it is a function of a fit that keeps moving, so the site must be re-reconciled against the engine on every publish, not only when a study is built.
[NEW 13-Jul r3, SCOPED — prospective only, per Sherif's explicit instruction] The Ke/Kd/WACC procedure applies to Egypt going forward, not retroactively; the ~27 live Egyptian studies are not queued for a mandatory rebuild (see the SCOPE clause above). The first draft of this item named the GCC reference studies (EAND, ADCB, ALPHADHABI). That was the wrong priority, and measuring it proved so:
For GCC names the sliding schedule does nothing. The AED is pegged to the USD and rf 4.30% is already at its long-run norm — today is the terminal, so explicit = terminal and the glide collapses to flat. Measured on EAND's published model: +0.0%.
What does bite in the GCC is the sovereign double-count fix, and by more than intuition suggests: netting UAE's ~40–55bp default spread out of rf lifts EAND's EV +4% to +6%, because the WACC−g spread is only 5.1% and 79% of EV is terminal. In a low-rate model small rate moves are not small.
The real exposure is EGYPT, where both changes bite hard. Capitalising the terminal at a norm-built ~18.8% instead of a flat ~29% lifts the terminal multiple from 4.2× to 7.3×. Measured on RMDA: the DCF lens moved 0.66 → 1.73 (+162%). Every Egyptian DCF still on a flat WACC is therefore materially understated, and there are ~27 of them live. What the earlier measurement remains useful for: it quantifies the honest cost of not rebuilding — every live Egyptian DCF is understated by a magnitude roughly like RMDA's (terminal multiple 4.2× → 7.3×, DCF lens +162% in RMDA's case, amplified further by leverage on the EV→equity bridge since net debt is fixed while EV moves). That number is disclosed here so the backlog is a known, sized cost, not a hidden one — but it is a backlog, not a queue. If and when a name IS next rebuilt for its own reasons, Egypt-market names apply the sliding schedule as a matter of course; GCC names apply only the double-count fix. Each rebuild is a full pipeline run through the QC gate — none move silently.
[NEW 21-Jul] SOURCE-INTEGRITY & GROUND-UP CONSTRUCTION MANDATE (SIGCM) — standing hard gate, QC item (r)

Adopted at Sherif's instruction, 21-Jul-2026. Applies to EVERY study and EVERY update, every ticker, every market. Canonical text: Source_Integrity_and_Ground_Up_Mandate.md; machine-readable form + assert_sigcm() gate: engine/research_protocol.py (verify by IMPORT, not parse — same rule as market_profiles.py / wacc_builder.py). This mandate does not replace any procedure above; it makes explicit and enforceable what the sourcing, Step-2A, driver-discipline and code-first rules already imply, and adds the formula-based-model requirement. A violation is a HARD FAIL — the report must not issue. Eight clauses:

1. Historicals = official sources only. Build the past IS/BS/CF using ONLY the company's own issued financial statements and full disclosures — no vendors, brokers, press-as-a-numbers-source, or third-party estimates for the subject's reported historicals. The Step-2A sweep's Global/Country/Industry rings remain valid for external context and forecast drivers, never as the source of the company's own reported numbers. If required official data is inaccessible, STOP and inform — never substitute unofficial data; never issue a report built on unofficial company information. (This is the same discipline the Claude/Gemini audit prompts already enforce as Prime Directive 1 / Phase 1.)
2. Forecast from the ground up. Product-by-product / service-by-service wherever segments are disclosed; revenue as volume × price and cost as cost-per-unit, growth projected in BOTH volume and price; where unit/segment data isn't disclosed, drop to the finest sourced level and FLAG the gap (Driver Ledger row).
3. Debt & FX. Study balance-sheet debt in full; split local-currency vs foreign-currency; FX debt at local-equivalent cost — consistent with the r2 §5 Kd-integrity gate and the v2 cost-of-capital method.
4. Asset-conversion cycle → BS/CF. Study DSO/DIO/DPO and the cash-conversion cycle from the statements and project the BS and CF items from them — no unexplained plugs where the drivers are disclosed. Reinforces cross-sheet-integrity item (q).
5. Competitors. Study peers within and outside the country for operating KPIs and valuation multiples (cross-check / relative multiples only — never a source for the subject's historicals).
6. Beta. From the stock's own price history regressed vs its own local index (EGX30 for EGX names) — the SAME beta produced by the beta procedure and the wacc_builder usability gate, not a second method.
7. Formula-based always. Every constructed financial statement is a live formula model (driver → IS → BS → CF → DCF; blue = input / black = formula; fair value recomputes when a driver changes) — never hardcoded values. Sits alongside the code-first rule: compute.py owns the arithmetic; the delivered Excel is itself a live model, not a values dump of study_numbers.json.
8. Flag-before-issue / stop. Flag any missing input BEFORE issuing; if the website or disclosed statements can't be read and that blocks a detailed ground-up build, STOP and inform — do not proceed on assumptions or unofficial substitutes.

QC consequence — new gate item (r): SIGCM attested, with evidence per clause. Absence of any element is a QC FAIL. The engine guard list now reads: market_profiles.py, wacc_builder.py, research_protocol.py — all verified by import, not parse.

[NEW 23-Jul] ADAPTIVE PER-STOCK WIDTH OVERLAY — adopted, EG-only, going-forward

Closes open item 1 above, for Egypt only. engine/adaptive_width.py. An OVERLAY, not a refit: the pooled per-market (ν, width_cal) fit is untouched; drift stays pure carry; tail ν is untouched. What it adds is a per-name online multiplier on cone width, learned from that name's own resolved 3-month-window residuals: m_raw = clip(sqrt(EWMA_0.85(u²)), 0.7, 1.5), then gentled and dead-zoned so small deviations don't move the cone at all — mult = 1 + 0.5·sign(m_raw−1)·max(0, |m_raw−1| − 0.10). A name whose own volatility has consistently sat below the panel average narrows toward its own history; a name running hotter than the panel widens toward its own history. Flag off (or insufficient history) reproduces the prior engine bit-for-bit.

Promotion evidence (30-name EG panel, strict LONO/held-out FINAL split, block bootstrap {2,3,4} — the same gate that killed the CRPS-selection idea in "THE PROMOTION RULE" above): proper score held at PARITY (log-CRPS 0.0154 → 0.0152, effectively zero cost) while calibration improved (pooled |std_u−1| 0.096 → 0.069; cov90 0.903 → 0.893, both still in-band; 24 of 30 names moved closer to std_u=1). This targets exactly the over-coverage failure mode described in open item 1 (LGES/Korea, ALPHADHABI/UAE: cov90≈1.00, PIT well-centred) — a market-level cone was too wide for names whose own volatility sits below their panel's average, and the overlay corrects that without touching the pooled fit every other name's cone depends on.

History gate — the reason it does nothing today. The 30-name validation ran on 15-year histories (~30 resolved 3-month windows/name). Production's raw_ohlc/EG currently holds ~5-year histories (~17 windows/name) — short enough that the estimator itself gets noisy, which is exactly the regime the validation flagged as prone to over-correcting. So the overlay carries a hard floor, MIN_WINDOWS=28: below that many resolved windows, the multiplier is forced to exactly 1.0. Verified by import against both the long lab histories (reproduces the validated multipliers, e.g. ISPH m_raw 0.924→mult 1.000, ORHD 0.753→mult 0.926) and current production data (every EG name currently returns mult=1.000 [insufficient_history]). The overlay is real, adopted, and dormant simultaneously — it starts doing something, name by name, only as each name's own library crosses 28 windows.

Scope and status. EG-only. Every other market runs mult=1.0 unconditionally until it clears this same LONO gate on its own panel — this is not assumed to generalize. Going-forward only, per the standing append-only rule: applies to cohorts anchored on or after adoption; nothing already published or graded is retro-touched. As of this entry the change is committed and pushed to branch feat/adaptive-width-overlay-eg (open PR, not yet merged to main — the materiality-gate convention above: engine changes open a PR, they are never auto-merged). Merging, and any push to the live site, still require the standing GIT/PUBLISH MECHANICS step — a fresh token supplied at the moment of the write; nothing reaches the site on its own.

[NEW 07-Aug, per instruction — ARCC study] COST-STACK ESCALATION — standing procedure

Adopted when a reconciliation against an EFG Hermes sell-side report on ARCC (Arabian Cement Company, EGX) surfaced that the model's entire margin decline was manufactured by one input choice rather than forecast: the local price path (8.0/9.0/8.0/7.0/6.5%) was set below the cost-inflation path (11.5/10.0/9.0/8.0/7.0%) in every single year, by construction. The direction was not the defect on its own — a realised Q1-2026 margin of 42.9%, above the FY2025 full-year average and still widening, had already contradicted it. The defect was structural: a single blended domestic-CPI-convergence index was escalating a cost line that is dominantly a globally-traded USD commodity. Applies to every future study with a per-unit cost stack (materials/fuel, transport, overhead, or equivalent).

1. One escalator per driver class, never one blended index across all of them. A cost stack allocated to its own physical driver (materials/fuel per tonne of throughput, transport per tonne despatched, overhead per tonne sold) must inflate each line with the index that actually governs that input. Globally-traded commodity inputs (coal, gas, other imported energy or raw materials) get a commodity-price path in their own currency, converted through the model's own FX path — never a domestic CPI-convergence assumption; the commodity does not know the central bank's inflation target. Genuinely domestic inputs (local wages, local services, local transport) keep the domestic disinflation/CPI path. A single blended index applied to every line is a QC FAIL once the cost stack is granular enough to name its own drivers.

2. The cost side needs the same source-discipline already required of the price side. Every study anchors its price path to a disclosed price history and, where available, a recent exit rate. The cost path must clear the same bar: seek a disclosed, dated, near-term cost figure — a peer broker's per-unit cash cost, the company's own disclosed input-cost commentary, a published commodity index — before defaulting to a house-asserted macro proxy. A cost path resting only on "converges to the central bank's target" while the price path carries a disclosed exit rate is an asymmetry of evidence between the two sides of the same margin, and is itself a finding to price, not wave through.

3. The first realised quarter is a standing check, not a discovery the user makes. Extend Step 0's calibration discipline to the operating build: the first actual quarter or half-year disclosed after a study's publication must be checked against that study's own forecast for the equivalent period, and the result — met, beat, or missed — stated in the next revision or ledger entry without being prompted. A miss above the study's own >5%-of-central escalation threshold triggers the same full-finding treatment as an external critique.

QC consequence. A cost stack with one blended escalator across physically distinct drivers, a cost path with no sourced near-term anchor where the price path has one, or a study revision that does not state what the first realised quarter actually did against the prior forecast, is a QC FAIL going forward.

[NEW 07-Aug, per instruction — ARCC study] PRIMARY-SOURCE FINANCIAL RESEARCH — standing procedure

Adopted from the same ARCC exchange, from a direct instruction: the company's own investor-relations page was reachable and had not been the first place looked. The FY2025 investor presentation, once supplied, proved the point — it confirmed the physical unit build (kiln utilisation, clinker factor, three product volumes) to 0.02% and gave the Q4 exit price rate that anchors the local price path, neither of which exists anywhere in the audited financial statements alone. Extends the Company ring of Step 2A's Information Sweep, applies to every future study.

1. The company's own official website / investor-relations page is the first channel attempted for every Company-ring figure, before any aggregator or third-party data provider. Record the attempt and its outcome in the Sweep Register regardless of result. If the site is unreachable, say so plainly and ask the user to attach the primary documents directly — do not silently fall back to a weaker secondary source. This is not hypothetical: arabiancementcompany.com returned connect_rejected at the build environment's proxy this session. The user then attaching the FY2025 presentation is this fallback working as designed, not evidence the rule failed.

2. Audited financial statements: minimum two, target four, complete past fiscal years, sourced from the filing itself — the company's own published annual report or its regulator — never an aggregator's restated summary. This makes concrete what the terminal-growth procedure's historical reconciliation table already asks for ("as far back as reliable financials allow"): two years is the floor below which that table and its two check numbers may not be built at all — state the shortfall explicitly instead of thinning the table — four years is the target.

3. The study year itself: every quarter already disclosed, pulled into the sweep before the build, not discovered after. If a study is built partway through a fiscal year, every quarter of that year already on the public record belongs in the Company ring from the start. This closes the gap from the other side of cost-stack escalation's point 3, which checks the first quarter released after publication — this rule requires every quarter released before it to already be in. ARCC's own Q1-2026 actual (42.9% gross margin) was on the public record before the study's own base date and was not swept in; it only entered the analysis because the user asked about margins. Together, no disclosed quarter on either side of the study date is allowed to sit outside the sweep or the check.

4. Investor-relations presentations and investor/earnings-call materials — decks, transcripts, webcast notes — are a mandatory sweep source, not optional colour, specifically for the volumes, per-unit prices, utilisation rates, capacity and segment splits that never appear in a financial statement at all. Pull every IR presentation and call transcript covering the sourced fiscal years, not only the most recent one. Tag these distinctly in the Sweep Register — a COMPANY_IR source type, kept separate from the audited-financial-statements tag — so a reviewer can see how much of the Company ring rests on the company's own primary channel rather than a filing or a secondary source.

5. QC consequence. A Sweep Register showing no attempt at the company's own site, fewer than two audited fiscal years, a gap in the study-year's disclosed quarters, or zero investor-relations sources in the Company ring is a QC FAIL going forward.

[NEW 08-Aug, per instruction — SWDY study] THE MODEL STUDY — SWDY sets the structural template AND the research-depth bar

Adopted at Sherif's instruction, 08-Aug-2026, because the level of recent valuation reports had slipped below par. The fix is not a new checklist item — it is a new exemplar: SWDY_Valuation_Study_05-08-2026 (engine/swdy_study/ — the study, its Excel model, its standalone bibliography document, and its filled QC evidence table QC_GATE_05-08-2026.md) is THE MODEL STUDY. Every future study matches its sections list, its sheet list, and its depth of research. Machine-readable form: MODEL_STUDY + MODEL_STUDY_DEPTH + ModelStudyChecklist + assert_model_study() in engine/research_protocol.py — verified by IMPORT, not parse, same as the rest of the guard list.

One-in-one-out, applied explicitly. TMPV_Valuation_Study_30-06-2026 is RETIRED as the structural template; EAND is RETIRED as the operating-company exemplar — SWDY takes both roles. ADCB (bank; RIBL secondary) and ALPHADHABI (holdco) remain as LENS-PATTERN references only: class adapts the lens and the indicator set (SWDY's own QC item (c) is the precedent — the telco checklist was rejected for a diversified industrial and the metrics re-cast for the actual class, inside the same skeleton), never the structure or the depth.

The sections list (Word, 16 sections, in order): Masthead + READ FIRST · Headline · Valuation summary — every read at a glance · Company overview · §1 Fundamental valuation (1.1 the cash-flow model with the full FCFF waterfall AND the EV→equity bridge; 1.2 book value & sustainable return; 1.3 relative multiples; 1.4 normalised earnings power; 1.5 synthesis — four lenses, one field; 1.6 the drivers — each disclosed segment grown on its own driver, margins as OUTPUTS; 1.7 the crux; 1.8 macro & country — the sourced cost of capital, the cost-of-debt evidence table, and every contested construction PRICED, not just named; 1.9 sensitivity) · §2 Technical and price structure · §3 A probabilistic price map (percentile map + level-touch ladder) · §4 Comparison of the lenses · §5 Catalysts to watch · §6 Reading the probability zones · §7 Caveats and what would change our mind · Appendix A financial statements (A.1 income statement 3y historical + 5y forecast; A.2 balance sheet; A.3 forecast balance sheet and cash-flow markers) · Appendix B peer frame, risk register — and the research register · Appendix C the expert panel (C.1–C.3 Expert 1/2/3 by method; C.4 cross-examination; C.5 the three in one room; C.6 reading the divergence) · About this series · Disclosure & Disclaimer.

The Excel (16 sheets, same names, same order): READ FIRST, Summary, Fundamental Valuation, Assumptions, SOTP Bridge, Segments, Relative & Normalized, DCF, Income Statement, Balance Sheet, Cash Flow, Summary Financials, Monte Carlo, Sensitivity, Per-Share & Ratios, Peer & Sector. Blue = input, black = formula, green = cross-sheet link; the workbook CALCULATES (the initiation prompt's formula-first rules and driver test apply unchanged).

The depth bar — eight standards, every one of which the SWDY build actually demonstrated (evidence in engine/swdy_study/QC_GATE_05-08-2026.md), so none is aspirational:

1. BIBLIOGRAPHY DOCUMENT, STANDALONE. Every study ships a separate bibliography document: READ FIRST + research-layer guide, a primary-documents table (publisher, date, what was taken from each), the FULL input register — every single input with value / date / source-and-construction, grouped by layer (SWDY: 134 inputs, all four-field complete) — a judgements table with what-would-overturn-it per row, a negative-results table, and a note on any material aggregator discrepancy found.

2. PROVENANCE, FOUR-FIELD, ASSERTED. Every input carries value, source, date and layer, validated by assertion, and appears in the bibliography document. No orphan numbers anywhere in the deliverables.

3. NUMERIC TRACEABILITY. Every builder — Word, Excel, bibliography, figures — reads the study's committed numbers file exclusively; no financial numeral is typed into a builder. An independent evaluator recalculates the delivered workbook and reports anything it cannot parse as a FAILURE, never a skip (SWDY precedent: LibreOffice could not load any spreadsheet in the build environment, so recalc.py evaluated every formula the builder emitted rather than downgrading the check).

4. EXTERNAL-READER SCRUB. The reader is an external party. A programmatic scrub of every delivered document for internal-procedure vocabulary — step names, gate names, sweep/ring vocabulary, engine module names, verdict tokens, register jargon — must return zero hits (SWDY: 34 patterns, zero hits; two scrub false positives fixed in the CHECKER, not by rewording legitimate finance prose). Calibration evidence lives in §3 as plain-language sentences with the statistics inline; there is NO calibration appendix.

5. FIGURE DISCIPLINE. Figures render on a solid light canvas with ink text — zero transparency, verified programmatically, so they are legible on any page background — and every figure is INSPECTED AS A RENDERED IMAGE, not just generated; label collisions and contrast defects are fixed in-pass (SWDY caught two this way).

6. TABLE DISCIPLINE. Fixed table layout with explicit per-column and per-cell widths, plus a programmatic check across every table in every delivered document: none exceeds the text block, no starved columns (below the width at which ordinary labels wrap mid-word), no bloated columns.

7. EXPERT APPENDIX AT MAXIMUM DETAIL. Each expert carries: worldview; when-it-works / when-it-fails; a worked valuation table with EVERY intermediate line; a named sensitivity with numbers; and an explicit falsifier stated in advance. Plus C.4 cross-examination (each challenge explicitly conceded or rejected), C.5 the three in one room with the ranges figure, and C.6 a divergence table isolating which assumption drives which gap.

8. THE CONTESTED JUDGEMENT, BOTH WAYS. The study's single most consequential contested judgement is computed BOTH ways and published side by side — summary table, body, workbook, and an expert's range — never averaged into a single number that would hide the disagreement. SWDY's precedent: full Egyptian cost of equity against a hard-currency-leg discounting, central 24% below spot against an alternative above it, both shown, the reader told exactly which question decides between them. This extends the standing dual-framing rule from individual figures to the study's central judgement.

QC consequence. Gate item (a) now reads: structure, content, format AND DEPTH match the MODEL STUDY (SWDY). A study missing the bibliography document, the four-field input register, the recalc evidence, the scrub, the figure/table checks, the maximum-detail expert appendix, or the side-by-side contested judgement is a QC FAIL — not a noted limitation. ModelStudyChecklist is attested alongside SIGCM before issue.
