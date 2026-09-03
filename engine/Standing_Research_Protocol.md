PROTOCOL REVISION 2026-09-03e — [R-DOC-01] if your copy does not carry this line, or carries an earlier revision, it is STALE. The current text lives at engine/Standing_Research_Protocol.md
on the repository's default branch; nothing else is authoritative. Bump on every edit.

TESTAHIL — Standing Research Protocol
Updated 1 September 2026 (rev. 10) — CAMPAIGN WORK IS MERGED ON GREEN [R-MERGE-01] (an unmerged rule binds on nothing)
(rev. 9, 1 September 2026 — VALUATION-GAP AUDIT [R-GAP-01]: a central fair value more than 10% below the traded price is audited before it ships)
(rev. 8, 24 August 2026 — GUARDED MID-BAND SHAPE SELECTION [R-SHAPE-01] · width-overlay live reading [R-WIDTH-01] · bounded early grading [R-GRADE-01], investor sessions)
(rev. 7, 23 August 2026 — three-lens independence · committed drift · per-name discipline · negative control)
(rev. 6, 23 August 2026 — ENFORCEMENT: the rules that make the other rules bind)
(rev. 5, 07 August 2026 — cost-stack escalation · primary-source financial research)
(rev. 4, 29 July 2026 — computed technical read · regenerated charts · as-of stamps)
(rev. 3, 13 July 2026 — value-driver TV · NCI at fair value · one-clock lenses · cross-sheet integrity · the Kd capitalised-interest trap)

This supersedes the 12-July text and both earlier 13-July revisions. Changes new in rev. 5 are marked [NEW 07-Aug]; the [NEW 29-Jul], [NEW 23-Jul], [NEW 21-Jul], [NEW 13-Jul r3], [NEW 13-Jul r2], [NEW 13-Jul] and [NEW 11-Jul] markers are retained for provenance. Everything not marked is unchanged and still binding.

Rev. 6 comes from a different kind of review: not of a study, but of this document. A
build-depth audit of all 90 covered stocks on 23 Aug 2026 found 63 were not built ground-up
and only 4 carried a beta whose provenance the gate could attest — while every rule requiring
both was already written here, correctly, and had been for weeks. That is the same shape as
the composite-beta failure this protocol records: *"Writing the rule down did not stop it."*
The rules were never the problem. Rev. 6 therefore adds no new research method at all. It adds
the machinery that makes the existing rules bind, and one general rule from which the other six
follow — because this protocol has now learned the same lesson three separate times in
particular (beta, the technical read, the digest drift) and never once in general.

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

engine/raw_ohlc/{MARKET}/{TICKER}.csv is a persistent library of every covered stock, not an inbox — 65 stocks across 8 fitted markets ON 11-JUL-2026, WHEN THIS ENTRY WAS WRITTEN (27 EG · 11 SA · 14 AE · 3 QA · 3 US · 3 KR · 3 IN · 1 XAU). That roster is dated evidence for the library model, NOT a current count: it grows whenever a file is posted, and by 24-Aug-2026 it had reached 93 across 9 markets. Read it from engine/raw_ohlc/ or assets/markets.js, never from this document [R-DOC-02]. To add or refresh ONE stock, add or overwrite ONE file. The pipeline then refits that stock's whole market against the full library.

One-stock post ≈ 12 seconds, even on Egypt (the largest panel — check its current size live): panels are content-hashed (only the changed file rebuilds) and re-scoring uses fast_rescore, a closed-form re-simulation that is bit-for-bit identical to re-running the engine (verified) but skips the O(n²) HAR refit.

Market and ticker are decided by FILE PLACEMENT, never inferred from a filename. This is deliberate — the ADNOC-Gas / ADIB-Egypt-vs-ADIB-UAE class of ambiguity is exactly what must not be automated.

The materiality gate — automation, not unsupervised drift

Auto-commits, no approval: cleaning, panel rebuild, refit, LONO verdicts — provided nothing about the conclusion changed.

MATERIAL — applied, but never silently:

any existing name's verdict category changes
a new name arrives already FAILING (the signal that a file is misfiled or bad)
the published 90% cone moves >5% — measured on width_cal × q95(t(ν)), the band a reader actually sees, not on ν and width_cal separately (they trade off, so watching them individually both misses real changes and fires on noise)
the market-level verdict changes
a panel carries a name with no raw data behind it

A new name is NOT material by itself. Adding coverage is the most common event; blocking on it would mean a review request on every post. Placing the file is the human decision.

Why the gate exists (empirical, not theoretical): on 11-Jul, data cleaning alone flipped Korea's tail from ν=6 to Gaussian and changed two names' robust verdicts. A bare cron job would have shipped both silently.

[R-CAL-01] MATERIAL NO LONGER MEANS BLOCKED — AMENDED 23-Aug-2026, per instruction

Until this amendment each of the conditions above stopped the pipeline and opened a PR that was never auto-merged. The reason above survives intact and is not in dispute: data cleaning alone really did flip a tail and two verdicts, and shipping that with nobody looking would have been indefensible. What was wrong was the remedy. The defect is SILENCE, and blocking turned out to be its own form of silence.

The measurement that forced the change, taken on 23-Aug-2026. Between 6-Aug and 23-Aug the gate produced 66 unmerged review PRs — one per trigger, every one re-reporting the same standing finding, 61 of them fired by a human posting data and 18 by the nightly cron. In the same window 18 covered names across EG, AE and SA had never entered a production fit at all: ADNOCLS — the model report's own company — DU, MODON, FERTIGLB and SAVOLA among them, all with live pages carrying cones struck from a fit that had never seen them. Production ran a 29-Jul EG fit for twenty-five days and announced that nowhere. A reader of the site could not tell, and neither could we without going and counting.

Two structural faults sat underneath it, and both are worth stating because each is a general shape, not an incident.

A gate with no release is a stall. The review PR's own closing line read "either merge this PR to accept" — but merging accepted nothing: the workflow staged only PENDING_REVIEW and panels, and market_profiles.py is deliberately never written for a material market. The instruction was not executable. Adopting meant hand-editing production, which the protocol forbids elsewhere, so nobody did it, and the queue grew until it was ignored on sight. STANDING RULE: whenever a rule can say STOP, the same commit must define what saying GO looks like — a command, a script, a documented path. A rule that can only refuse will be worked around or ignored, never obeyed. scripts/adopt_calibration.py is the release built for this one.

One blocked market froze every other market. The runner returns nonzero if ANY market is material, and the job committed only on exit 0 — so every healthy market's applied fit was written to disk and then discarded. SA was non-material, "safe to auto-apply" by its own verdict, and still sat at 11 of its 13 names for weeks because EG and AE were material. STANDING RULE: a per-item gate must fail per item. A single process-wide exit code cannot carry a per-market decision, and using it as though it can silently converts one item's caution into every item's paralysis.

What replaces it. A material change APPLIES, and is announced in three places at once: the evidence file under engine/PENDING_REVIEW/, the reasons repeated verbatim in the commit message — the announcement that reaches anyone reading git log without knowing an evidence file exists — and the config it replaced, stored under `superseded` in fitted_configs.json. Reverting that one commit restores market_profiles.py and fitted_configs.json together, in step; hand-editing either one alone cannot, which is why the revert is defined as a commit and not as a value. auto_refresh.py --halt-on-material restores the pre-amendment behaviour for anyone who wants it on a particular run.

What still stops the run: a market that RAISES. Its production config is left untouched, a PENDING_REVIEW/{MARKET}_{date}-ERROR.md carries the traceback, the healthy markets still apply, and the run ends RED — an exception is not evidence, and a crashed market that looked green is how EG sat unprocessed from 19-Jul until someone noticed.

What this amendment does NOT do: no lens, driver rule, cost-of-capital construction or calibration procedure changes, and the materiality thresholds themselves are untouched. The same conditions are material as before. Only the consequence of being material changes.

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

[AMENDED 10-Aug-2026, per instruction] 6. THE REGRESSOR IS THE PUBLISHED MARKET INDEX FOR THE STOCK'S OWN EXCHANGE. NOT A COMPOSITE.

The rule above always said "its own local index." It was not honoured. Every beta in this repo — all eight studies, SWDY the model study included — was regressed against an **equal-weight composite of whichever names the engine happened to cover in that market**. Clause 4 of this same procedure even names "a 27-name equal-weight EGX composite" in the CLHO precedent that established the procedure, so the substitution was not an oversight in one study: the house pattern normalised it, and each new study copied the last.

What it cost, measured on FERTIGLB (ADX) on 10-Aug-2026, the first name regressed both ways:

| regressor | β | R² |
|---|---|---|
| FTSE ADX General, Dimson | **0.931** | **10.0%** |
| FTSE ADX General, naive | 0.810 | 9.1% |
| 17-name equal-weight composite, naive *(what shipped)* | 0.492 | 6.2% |
| 17-name turnover-weighted composite, naive | 0.376 | 4.3% — fails the gate |

The composite understated beta by ~40% and explained materially less of the variance. It carried the WACC from 11.90% to 8.53% and the fair-value centre from AED 2.15 to AED 2.74 — a 21.6% overstatement of value, from the choice of regressor alone. Three defects, none subtle:

- **It mixed exchanges.** The `AE` library holds ADX names (ADCB, FAB, ALDAR, ADNOCGAS) beside DFM names (EMAAR, DIB, ENBD, SALIK). FERTIGLB is ADX-listed. An ADX share was being regressed against an ADX/DFM mongrel.
- **It was a coverage artefact, not a market.** 17 names this engine happens to hold, not the exchange. The composite changes every time a stock is posted.
- **Equal weighting is not a weighting scheme.** It gave TWOPOINTZERO the weight of FAB. Turnover weighting only proxied the free-float-cap scheme the real index applies properly.

There is a second, subtler harm. A composite built from the covered panel shares constituents with the panel it is used to price, injecting self-covariance; `scem_study/beta_reg.py` already noted this and proceeded anyway.

THE RULE, from now on:

(a) The regressor is the **published index of the exchange the stock is listed on**, read from `engine/raw_indices/{MARKET}/{INDEX}.csv`. EGX30 for EGX, FTSE ADX General for ADX, TASI for Tadawul, and so on. Where a market has several indices, prefer the broad all-share over a blue-chip subset unless the study states why.

(b) **A constituent composite is not a substitute and is not a tier.** It may be reported as a labelled cross-check; it may never be the regressor.

(c) **Match the exchange, not the country — and key the resolver on the exchange.** A DFM-listed name is regressed against a DFM index, not an ADX one, even though both are "AE" in the engine's market coding. If the correct index is not held, that is case (d).

[RE-KEYED 10-Aug-2026, the same day, per instruction] The first implementation of this rule mapped **one index per market code** and therefore contradicted the clause it existed to enforce. Market `AE` spans **both ADX and DFM**, so every DFM-listed name resolved to `FADGI`, an ADX index — six of them at the time (DEWA, DIB, EMAAR, EMAARDEV, ENBD, SALIK), nine today. The live count belongs in `assets/data.js`; a standing rule must not carry one, because it goes stale the moment a stock is posted and the rule then reads as false. The counter-example was written into the rule and the code did the forbidden thing anyway, in the same commit.

`wacc_builder.EXCHANGE_INDEX` is now keyed `(market, exchange)`, and `market_index_path(market, exchange)` **refuses to resolve a market that spans more than one exchange** unless told which. Unknown market, ambiguous market, unregistered exchange and missing file all raise.

| market / exchange | index | status |
|---|---|---|
| AE / ADX | FADGI (FTSE ADX General) | registered |
| AE / DFM | FADGI | **INTERIM by instruction 10-Aug-2026** — see below |
| EG / EGX | EGX30 | registered, blue-chip subset |
| IN / NSE | NIFTY50 | registered, subset |
| KR / KRX | KOSPI100 | registered, subset |
| QA / QSE | QATAR10 | registered, subset |
| SA / TADAWUL | TASI | registered, **broad all-share** |
| US / NASDAQ | NASDAQCOMP | registered, tech-weighted |
| BR, GB | — | not supplied |

**The DFM interim [instruction, 10-Aug-2026; HELD OPEN by instruction, 23-Aug-2026].** The DFM-listed names — DEWA, DIB, EMAAR, EMAARDEV, ENBD, SALIK, and since then AIRARABIA, DU and EMPOWER, nine in total — stand on FTSE ADX General. This is a deliberate, labelled exception to clause (c), not a quiet fallback: `wacc_builder.INTERIM_INDEX` carries the disclosure and `index_interim_note()` returns it, and **any beta built on it must quote that note**. It is not a conforming clause-(a) regressor.

It is also the better-evidenced half of the substitution, which is worth stating because the intuition runs the other way. Over five years of weekly returns, FADGI explains the DFM names **better** than it explains the ADX names it actually covers:

| | median R² vs FADGI | median β | range |
|---|---|---|---|
| ADX names (15) | 0.127 | 1.037 | AGTHIA 0.037 → FAB 0.606 |
| DFM names (6) | **0.240** | 1.067 | DEWA 0.101 → ENBD 0.304 |

All six DFM names clear the R²≥5% usability gate — the measurement is the 10-Aug one, taken on the six DFM names covered at that date; AIRARABIA, DU and EMPOWER were added after and are not in it. Several ADX names barely do (AGTHIA 0.037 fails it outright, IHC 0.088, FERTIGLB 0.091). The large Dubai names co-move with the UAE market as a whole, while Abu Dhabi carries more low-float and ADNOC-family idiosyncrasy. The substitution is therefore defensible on evidence for the interim — but it remains a substitution, and it is NOT a conforming clause-(a) regressor however long it stands.

**A DFM series is now held, and the interim stands anyway [instruction, 23-Aug-2026].** `engine/raw_indices/AE/DFMGI.csv` (DFM General, 2015-01-05 → 2026-07-16, 2,306 rows) is in the repository. The 10-Aug clause said "a real DFM index replaces it"; that replacement condition is now met and has been **explicitly declined for the time being**. The nine DFM names continue on FTSE ADX General. DFMGI is therefore HELD BUT NOT REGISTERED — `EXCHANGE_INDEX` must keep mapping `("AE","DFM")` to FADGI, and a later session must not "helpfully" register it on the reasoning that the file exists. Registration now needs its own instruction.

Three things follow, and none of them is optional:

1. **The disclosure obligation gets stronger, not weaker.** A stopgap that persists by choice is a standing methodological position, so every DFM beta must carry `index_interim_note()` verbatim wherever the beta is quoted — study body, bibliography, cost-of-capital table and workbook alike — and must not be described as conforming.
2. **The cost is measured, and it is not nil.** Where both regressions have been run, DFMGI has the materially higher explanatory power, so the interim is knowingly the weaker fit on the names tested:

| name | on FADGI (adopted) | on DFMGI (declined) |
|---|---|---|
| AIRARABIA | β 0.812, R² 0.135 | β 1.086, R² 0.402 |
| EMPOWER | β 0.863, R² 0.103 | β 0.652, R² 0.157 |

   Both move beta by roughly a quarter to a third, in opposite directions — so this is not a uniform bias that a reader can mentally correct for, and it must not be presented as one.
3. **It is a dual-framing case.** Under the standing dual-framing rule, a DFM study that has both numbers publishes the declined one as a labelled cross-check beside the adopted one, exactly as AIRARABIA already does, rather than suppressing it. `airarabia_study/beta_reg.py` is the worked precedent: it runs both, adopts the registered regressor, prints the difference, and says in the study why the other was not used.

Revisit only on a further instruction.

**Where the exchange comes from.** `assets/data.js` records it per ticker as the `code` prefix (`ADX:`, `DFM:`, `EGX:`, `TADAWUL:`, `QSE:`, `KRX:`, `NSE:`, `NASDAQ:`). Read it. Never infer the exchange from the `raw_ohlc/{MARKET}/` folder — that groups by market code and is exactly what mixed ADX with DFM.

**Dual-listed names.** Orascom Construction trades on both ADX and EGX. The same issuer therefore has two legitimate regressors, and only the *series* tells you which: an EGP-denominated series filed under `EG` regresses on the EGX index; a dirham series of the same company would regress on the ADX index. Verify the series' currency and price magnitude against the exchange it is filed under before regressing, and flag dual listings explicitly in the Sweep Register. Nothing in the file name carries this.

**Broad versus subset — SETTLED 10-Aug-2026, per instruction.** Clause (a) prefers the broad all-share, and only TASI actually is one: EGX30 is a 30-name blue-chip index against a broader covered panel that includes small caps (KABO, DSCW, LCSW); NIFTY50, KOSPI100 and QATAR10 are subsets by construction; NASDAQCOMP is tech-weighted rather than a market proxy. **The user supplied all seven series explicitly as "the indices to use", so these ARE the regressors** and the subset question is closed by decision, not left as a drifting compromise. All seven uploads were byte-identical to the copies already in `raw_indices/`, so the registrations were already correct. The documented "why" required by clause (a) is this instruction. Revisit only on a further instruction.

**All seven passed Step 0.0 on 10-Aug-2026** — density screened against each exchange's real calendar, max one-day move against that exchange's own price limit:

| market / exchange | index | rows | sessions/yr 2021-25 | max abs 1-day log move | limit |
|---|---|---|---|---|---|
| AE / ADX | FADGI | 3,883 | 238–252 | 0.084 | 0.211 |
| EG / EGX | EGX30 | 3,745 | 241–244 | 0.111 | 0.290 |
| IN / NSE | NIFTY50 | 3,857 | 246–249 | 0.139 | 0.290 |
| KR / KRX | KOSPI100 | 3,624 | 243–248 | 0.127 | 0.464 |
| QA / QSE | QATAR10 | 2,878 | **188–201** | 0.116 | 0.137 |
| SA / TADAWUL | TASI | 3,882 | 248–251 | 0.087 | 0.137 |
| US / NASDAQ | NASDAQCOMP | 3,913 | 250–252 | 0.132 | none |

**QATAR10 carries a standing caveat — weekly only.** It runs ~198 sessions a year while QSE stocks (QNB, IQCD, QGTS) all carry 248–250, a systematic ~20% shortfall that is stable at 188–201 every year for fourteen years. That consistency means it is a property of how the series is published, not vendor corruption, so Step 0.0 correctly passes it. It does NOT impair the weekly regression this protocol mandates: over the last five years the index supplies 255 weekly points against a stock's 259, and 255 of them align — 98.5% coverage. It WOULD impair any daily use of QATAR10, which is therefore not permitted without re-screening. Quote this caveat wherever a Qatari beta is quoted.

(d) **If the index is not in `raw_indices/`, STOP AND ASK for it** — the same stop-and-inform discipline SIGCM applies to missing primary financials. Do not build a composite and proceed. The index is one file; the request costs a message.

(e) The index series passes **Step 0.0** like any other series before use, and its as-of date is quoted wherever the beta is quoted.

(f) Every beta previously built on a composite is **non-conforming and must be re-derived before that study is re-issued or rolled forward**. Affected: AMOC, ARCC, EGCH, ELEC, PHAR, SCEM, SWDY (all EGX, all against the EG composite; EGX30 has been in the repo since 09-Aug-2026) and FERTIGLB (corrected 10-Aug-2026). The WACC/Ke, fair-value range and any sensitivity anchored on beta all move with it.

(h) **Never hand-roll a study-local beta script; the rule is enforced in code, not in prose.**

Writing (a)–(f) down did not make them obeyed. `market_index_path()` raised for an unregistered index, but nothing forced a study to CALL it — eight study-local `beta_reg.py` scripts went on building composites and passing every gate, including the QC gate. Prose cannot execute. Three mechanisms now close that:

- **`engine/beta_regression.py` is the only sanctioned way to produce a regression beta.** `own_stock_beta(ticker, market, exchange)` resolves the regressor itself through `wacc_builder`, runs Step 0.0 on both series, matches the weekly grid to the exchange's real trading week (EG/SA/QA Sun–Thu → `W-THU`; AE post-2022 and the rest → `W-FRI` — a mismatched grid silently drops observations), and returns provenance with the number. A study cannot reach a basket without deleting the call, which a reviewer can see in the diff.
- **`research_protocol.assert_beta_provenance()` inspects the record, not a boolean.** `SIGCMChecklist.beta_own_history_vs_egx30` is a flag a study sets itself, and every study set it `True` while regressing on a composite. A self-attestation cannot catch that. The gate fails a regressor outside `raw_indices/`, a beta missing the usability gate without a documented tier-2/3 fallback, and an interim substitution whose disclosure note is absent.
- **The exchange is read from `assets/data.js`**, as the ticker's `code` prefix — never inferred from the `raw_ohlc/{MARKET}/` folder, which groups by market code and is precisely what mixed ADX with DFM.

(i) **Re-deriving a study's beta has its own canonical prompt** — `engine/Beta_Reissue_Prompt.md`, with the FERTIGLB pass as the worked precedent. It carries a step most rebuilds forget: **hunt the stale prose.** The number propagates through the build chain automatically; the sentences describing it do not. FERTIGLB's own source line still read *"equal-weight ADX/DFM composite built from the 17-name UAE price library"* while the model already carried the index beta — a false provenance statement that would have shipped in both the study and the bibliography. Provenance strings must be BUILT FROM THE RECORD, never typed.

(g) Markets whose index is still absent as of 10-Aug-2026: **BR, GB.** SA/TASI was supplied 10-Aug-2026, so every Tadawul beta (STC and any future Saudi name) must be re-derived against it. No conforming beta can be produced for a name in those markets until the file is supplied.

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
Template [CHANGED 19-Aug — see THE MODEL REPORT entry below]: match the MODEL REPORT — ADNOCLS_Valuation_Study_09-08-2026 + its Excel + its standalone bibliography document, minus the excluded edition-history section — exactly, in structure, PER-SECTION CONTENT AND research depth. THE REFERENCE SET IS CLOSED AT THREE NAMES: ADNOCLS (the model report, and the operating-co lens pattern), ADCB (bank), ALPHADHABI (holdco). No other company is a template, an exemplar or a reference study anywhere in this protocol.
Step 2A Information Sweep — four mandatory rings (Global/Country/Industry/Company), classified B/S/D/C — runs BEFORE any forecast driver is set, on every study and every update.
WACC bottom-up, market-adapted; local govt bond rf even for pegged currencies; ERP from Damodaran's original file only; genuine beta regression with a real usability gate.
Lens by instrument class; never blend legs that need different methods.
DCF waterfall rule — full build to PV of FCFF shown inline; stopping at FCFF is a hard QC fail.
Expert appendix — three experts, genuinely different methods, a falsifier each.
Ledgers are append-only. No published forecast is ever retro-edited.
Never a rating or a price target. Fair-value ranges and distributions only.
OPEN ITEMS (honestly ranked)
[ADOPTED 23-Jul — EG only, history-gated; see "ADAPTIVE PER-STOCK WIDTH OVERLAY" below] Name-level width_cal, shrunk toward the market fit. This was the real answer to the "bands are too broad" complaint. Both robust FAILs at the time this item was written failed for the SAME reason and it was not mis-centring — they were over-covered: LGES had cov80 = 1.00 and cov90 = 1.00 (every single outcome inside the 80% band), a cone 1.11× the benchmark, and a PIT of 0.471 (perfectly centred). ALPHADHABI was the same shape. A market-level cone over-widens any name whose own volatility sits below the panel average. The overlay cleared a strict LONO/held-out gate on the 30-name EG panel (block bootstrap {2,3,4}) — proper-score parity, improved calibration — and now lives in the engine, EG-only, forced to exact baseline (mult=1.0) on any name with fewer than 28 resolved 3-month windows of history. Other markets have not been tested and remain on the market-level cone until each clears the same gate on its own panel.
Panel filenames still carry the retired session-counted tag. 93 calendar `_3m` panels exist on
disk but only 74 `_60d`, and `panel_refresh.DEFAULT_TAG` is still `60d` — a contradiction of the
calendar-only rule at the filename level. It does NOT narrow the materiality gate: `refresh_market`
builds its name list as `existing_panel_names(tag)` UNION the raw CSVs, so with the library present
the [R-CAL-03] coverage-flag condition covers all 93, which a dry run confirms (AE 28, EG 37, SA
13, …). That distinction is recorded because the first draft of this entry asserted the opposite
and was corrected by measuring rather than by re-reading — the same discipline the entries above
were written under. Deliberately NOT fixed in passing: DEFAULT_TAG selects which panels the refit
itself runs on, so changing it is a calibration decision, not a rename.

GBCO and STC now carry conforming tier-1 betas — 0.8907 against EGX30 and 0.7107 against TASI,
both produced by `own_stock_beta` and attested by `assert_beta_provenance` in the studies' own
committed code, replacing an assumed 1.0 and a daily 9-week stopgap respectively. Their WACCs are
still NOT re-issued: that needs each sovereign's own default spread read fresh from Damodaran's
original file, which this protocol forbids reconstructing from memory. Both studies also pass
`rf=` to a v2 `WaccInputs` that rejects it outright, and `stc_compute.py` imports the retired
`mc_v2`, so the re-issue is a rebuild rather than a patch.

Break-aware volatility estimation inside the engine (currently only the calibration sample is filtered). Moves every published distribution — a deliberate decision, not a silent fix.
Metals is the weakest calibration in the system — say so plainly. Gold is a single-name self-fit: it is calibrated on its own data, so its PARITY verdict is circular in exactly the way Qatar's was until IQCD and QNB de-circularised it. Worse, silver is a PUBLISHED instrument with no fit of its own — it borrows gold's. Every other market has been pulled onto a real panel; metals has not. Until silver/copper/platinum history arrives, the metals cone is the least-evidenced thing Testahil publishes, and it should not be presented with the same confidence as an EGX or GCC name.
UK and Brazil have no covered names; their profiles are stubs.
[NEW 29-Jul; RESTATED AS A RULE 25-Aug-2026 under R-DOC-02] **Library staleness is a standing condition, not a list.** This entry used to name eleven stale libraries — TMPV/RELIANCE/INFY, TSLA/AAPL/NVDA, IQCD/QNB/QGTS, SILVER, PLATINUM. On 25-Aug-2026 that list was measured against the repository for the first time since it was written, and it was wrong in both directions at once: it named PLATINUM, whose library was four days old, and it omitted forty-three names that were stale. Book-wide the median library age was eighteen days, 26 of 93 instruments were within three days, 54 were past ten and 34 past twenty-five — and the composition had moved wholesale, the AE and SA books having gone stale in their entirety while the list still pointed at IN/US/QA. Neither number is the point, and neither belongs in a standing document. A library goes stale BY THE CALENDAR, on its own, every day nobody posts an export; a written list moves only when a person edits it. The list was therefore guaranteed to drift out of true, and equally guaranteed to look authoritative while it did — the R-DOC-02 species exactly, and it gets the R-DOC-02 remedy: do not carry the fact, carry the instruction to measure it. **Never quote a stale-library list from this document, from the digest, or from memory** — the same read-live discipline that governs a calibration figure, adopted for the same reason. **Read it live:** `scripts/check_technical_read.py` prints the current library-age distribution and names every instrument past ten days. It reports staleness as an ADVISORY and never as a failure, deliberately. Staleness is a data-supply fact rather than a defect in the read: a month-old library still yields a technical read that is internally coherent and exactly reproducible, and only a fresh vendor export placed at engine/raw_ohlc/{MARKET}/{TICKER}.csv fixes it. Failing on it would make the gate permanently red for reasons no one in the room can clear, which is the R-ENF-02 ratchet lesson applied one document over. The two-part tech as-of stamp still makes each page self-report its own age — the stamp made latent staleness legible and did not create it — but a stamp shows one page at a time and cannot say how much of the book is affected. Only a sweep can, which is why the sweep is now a job rather than a sentence.
[DONE 13-Jul r2 — sweep executed; 4 contradictions found and corrected] Every covered name's published calibration claim was run against the live production fit (65 names carry a fitted verdict). Four contradicted the site, and they did not all fail in the same direction:
ALPHADHABI was OVER-CLAIMING — the site described a 9-name UAE panel at ν=4 / width 1.07, a fit that no longer exists, and called the name PARITY, "a calibrated distribution". Under the live 14-name fit (ν=10, width 1.049) it is a robust FAIL: skill −1.2%, CI entirely below zero at every block size. It had no calibration disclosure on its coverage page at all. Now carries the FAIL and the illustrative-only framing. Diagnosis: over-coverage, not mis-centring (50/80/90 = 0.69/0.81/0.94) — i.e. open item 1, the name-level width_cal problem, in the wild.
DIB, ISPH, KABO were UNDER-claiming — all three publish "FAILED its calibration"; all three are PARITY under the current fits. Labels corrected, but the caution was deliberately retained: all three still carry negative point estimates (−0.15% / −4.2% / −0.02%), so the cone is not demonstrably better than a random walk, merely not provably worse. A classification technicality is never used to upgrade a weak name. Append-only was respected: no registered forecast was retro-edited — every percentile and touch probability is frozen as published and will be graded against exactly those numbers. Original note text is preserved with a dated correction appended after it, so the record shows both what was said and what was wrong with it. Standing lesson: a verdict is not a fact you publish once — it is a function of a fit that keeps moving, so the site must be re-reconciled against the engine on every publish, not only when a study is built.
[NEW 13-Jul r3, SCOPED — prospective only, per Sherif's explicit instruction] The Ke/Kd/WACC procedure applies to Egypt going forward, not retroactively; the ~27 live Egyptian studies are not queued for a mandatory rebuild (see the SCOPE clause above). The first draft of this item put the GCC studies first. That was the wrong priority, and measuring it proved so:
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

Closes open item 1 above, for Egypt only. It is a WIDTH-CORRECTION, not a narrowing device — see the both-directions sentence below and [R-WIDTH-01]. engine/adaptive_width.py. An OVERLAY, not a refit: the pooled per-market (ν, width_cal) fit is untouched; drift stays pure carry; tail ν is untouched. What it adds is a per-name online multiplier on cone width, learned from that name's own resolved 3-month-window residuals: m_raw = clip(sqrt(EWMA_0.85(u²)), 0.7, 1.5), then gentled and dead-zoned so small deviations don't move the cone at all — mult = 1 + 0.5·sign(m_raw−1)·max(0, |m_raw−1| − 0.10). A name whose own volatility has consistently sat below the panel average narrows toward its own history; a name running hotter than the panel widens toward its own history. Flag off (or insufficient history) reproduces the prior engine bit-for-bit.

Promotion evidence (30-name EG panel, strict LONO/held-out FINAL split, block bootstrap {2,3,4} — the same gate that killed the CRPS-selection idea in "THE PROMOTION RULE" above): proper score held at PARITY (log-CRPS 0.0154 → 0.0152, effectively zero cost) while calibration improved (pooled |std_u−1| 0.096 → 0.069; cov90 0.903 → 0.893, both still in-band; 24 of 30 names moved closer to std_u=1). This targets exactly the over-coverage failure mode described in open item 1 (LGES/Korea, ALPHADHABI/UAE: cov90≈1.00, PIT well-centred) — a market-level cone was too wide for names whose own volatility sits below their panel's average, and the overlay corrects that without touching the pooled fit every other name's cone depends on.

History gate — why it starts as a no-op and switches on name by name. The 30-name validation ran on 15-year histories (~30 resolved 3-month windows/name). At adoption (23-Jul-2026) production's raw_ohlc/EG held ~5-year histories (~17 windows/name) — short enough that the estimator itself gets noisy, which is exactly the regime the validation flagged as prone to over-correcting, and the reason the floor exists at all. Libraries lengthen, so that count is dated evidence for the floor, not a description of production today. So the overlay carries a hard floor, MIN_WINDOWS=28: below that many resolved windows, the multiplier is forced to exactly 1.0. Verified by import against both the long lab histories (reproduces the validated multipliers, e.g. ISPH m_raw 0.924→mult 1.000, ORHD 0.753→mult 0.926) and, AT ADOPTION (23-Jul-2026), production data, where every EG name then returned mult=1.000 [insufficient_history]. The overlay starts doing something name by name, only as each name's own library crosses 28 windows — so WHICH names carry it is a live reading, never a fact recorded in a document. [R-DOC-02] Everything this paragraph once said in the present tense — that the overlay was 'dormant', that every EG name returned 1.000 — went false silently the first time a name crossed the gate. Dated measurements are kept as evidence for the floor; present-tense claims about which names are active are not written here at all, because that set moves without anyone editing this document.

How to read whether a published cone actually carries it — recompute, never read prose. [R-WIDTH-01, adopted 24-Aug-2026] The multiplier a cone was struck under is recovered by recomputing it: adaptive_width.live_width_mult() on that name's own library, or by re-striking the name and comparing the percentiles against the published row. THE LEDGER NOTE IS NOT AN INDICATOR. The "PER-NAME WIDTH OVERLAY APPLIED … live_width_mult() returns X" clause is emitted by engine/rollforward_one.py and by nothing else, so a cone struck through any other path carries the overlay silently — the clause's presence is evidence, its ABSENCE is not. This was found the only way it could have been. Asked how many live cones carried the overlay, a session COUNTED THE LEDGER NOTES, reported a number, and was wrong twice over: recomputing the multiplier name by name showed an order of magnitude more names past the gate than the notes disclosed, and among the silent ones was a cone the overlay was WIDENING — so the count was wrong AND the direction of the correction was misread, from the same single mistake of reading a disclosure as an indicator (24-Aug-2026; the per-name figures are a live reading, not recorded here). The general rule is the one this protocol already applies to numbers typed into prose: a disclosure emitted by one code path is a property of that code path, not a fact about the world, and it may only ever be read in the direction that one path can support.

**A rule with a threshold in it schedules its own staleness.** `MIN_WINDOWS=28` guarantees that
names cross it as time passes, with no commit, no refit and no announcement, so any sentence
describing which side of that threshold production sits on is dated the moment it is written.
Where a standing rule carries a gate, a floor or a minimum, this document states the RULE and
names the command that reads the current side of it — never the side. This is the same discipline
the stale-library entry above was rewritten under on 25-Aug-2026, and the two were found within a
day of each other, which is the argument for treating it as a class rather than two incidents.

The two are not equally serious, and the difference is worth keeping. A stale library is inert:
the read it produces is old but coherent. A crossed history gate CHANGES A PUBLISHED NUMBER — the
cone is simulated at an effective width the pooled figure does not describe — so anyone quoting
`profile.width_cal` for such a name is quoting a width no cone was built on.

Scope and status. EG-only. Every other market runs mult=1.0 unconditionally until it clears this same LONO gate on its own panel — this is not assumed to generalize. Going-forward only, per the standing append-only rule: applies to cohorts anchored on or after adoption; nothing already published or graded is retro-touched. STATUS, RE-VERIFIED 23-Aug-2026 AGAINST main RATHER THAN AGAINST THIS PARAGRAPH: MERGED AND LIVE. engine/adaptive_width.py is on main and market_profiles.py carries width_overlay_active=True for EG. The sentence that stood here until today still said "open PR, not yet merged to main", and it had been wrong for some time — nobody re-read it after the merge. It also carried two further claims that had gone stale underneath it: that engine changes open a PR "per the materiality-gate convention", which R-CAL-01 has now separated (the materiality gate no longer opens PRs at all; engine changes still go through a PR, but under GIT/PUBLISH MECHANICS, which is a different rule with a different reason), and that a push to the live site needs "a fresh token supplied at the moment of the write", which the 07-Aug-2026 amendment retired along with the token gate itself.

Being live does NOT mean being active: the overlay is history-gated at MIN_WINDOWS resolved 3-month windows and forces an exact 1.0 below it, so read live whether any EG name has actually cleared the gate before describing a published cone as carrying it. [R-DOC-02] STANDING RULE, and the reason this correction is written out rather than quietly patched: A STATUS SENTENCE IN A PROTOCOL IS A CLAIM ABOUT THE WORLD, AND IT ROTS. Anything of the form "as of this entry, X is on a branch / pending / not yet merged" must either be re-verified against the repository at the moment it is relied on, or not written into a standing document at all. The three defects here all shared one shape — a fact frozen in prose while the thing it described moved on — which is the same shape as the stale digest copy R-DOC-01 was written for.

[NEW 17-Aug-2026, per instruction — DU study] FOUR RULES ADOPTED FROM THE DU EDITION-4 REBUILD

Adopted after three challenge questions on a delivered study — had the critique been taken seriously enough, was the model built bottom up, was the workbook calculating rather than storing — all three of which answered NO on audit. The failure was not arithmetic; every gate had passed. It was that the model had never consumed disclosure the company publishes in every filing, and the self-audit had only ever re-checked the work already done.

1. MARGINS ARE OUTPUTS OR THE COST SIDE IS NOT BUILT. A contribution or gross margin set as an INPUT — however well sourced the rate — is a QC FAIL wherever the filings disclose enough to build cost per unit instead. DU edition 3 held one contribution margin per segment at the audited full-year rate while the company disclosed direct costs THREE ways by nature on the face of the income statement and FOUR ways by segment in the segment note, in every filing, including both interims of the study year. Neither cut was used. The rebuild made mobile direct cost a three-line per-subscriber stack (interconnect, commission, devices), each with its own escalator and its own named mechanism, and the margin became whatever was left. The diagnostic value is the point: group gross margin then DECLINED across the forecast while not one segment margin declined — pure mix dilution by the fastest-growing, thinnest segment, a result a blended margin assumption structurally cannot express and a reader cannot distinguish from erosion.

2. WHERE A COMPANY DISCLOSES THE SAME TOTAL TWO WAYS, RECOVER THE JOINT AND TEST IT. Two disclosed marginals plus a defensible structural assumption often pin down a cross-tabulation the company never publishes. DU discloses direct costs by nature and by segment and never crosses them; under two structural assumptions (fixed and wholesale carry no acquisition commission or device cost; commission is entirely mobile) the joint is recoverable EXACTLY. The obligation is to TEST it, not assert it: the residual must be economically possible (positive, and small where it should be small) and must foot exactly to the independently disclosed line in EVERY disclosed period. Both held in all four DU periods and are asserted in code. If the residual comes out negative or fails to foot, the assumption set is wrong and the joint must not be used.

3. A NEAR-TERM REVIEWED ACTUAL OUTRANKS A STALE FULL-YEAR RATE — AND THE CARRY-FORWARD MUST BE SHOWN CONSERVATIVE WITH NUMBERS. Anchor every unit rate on the most recent reviewed period, and let a rate DRIFT only where a named structural mechanism has a MEASURED like-for-like direction in the company's own half-year (or quarter-on-quarter) pair. Everything else is held flat, including observed improvements: stopping a measured improvement dead is the conservative choice when the mechanism is real but decays at a rate the disclosure cannot size. Where a first-half rate is carried into the second half, prove with the prior year's actual halves that this overstates rather than understates cost — in DU, three of four second-half 2025 rates came in cheaper than the first half, which is the evidence, not the assertion. And DELETE stories that cannot be measured: edition 3 projected a 2.1pp ICT margin gain on a data-centre-scale argument against a series that worsened before it improved. It was withdrawn.

4. AN UNIDENTIFIED SPLIT MUST BE DEMONSTRATED UNIDENTIFIED, NEVER ASSERTED — AND NEVER FILLED WITH AN IMPORTED RATIO. Where a finer split is wanted but a needed price/rate is undisclosed, do not estimate it and do not merely note the gap. SOLVE for the implied parameter across EVERY available period pair and publish the range. DU discloses its mobile base split prepaid/postpaid every quarter but only one blended ARPU; solving for the implied leg ratio across all 21 available quarter pairs gave -45x to +17x, with 9 pairs negative and only 5 inside the peer band observed at the one Gulf operator that discloses both legs. An estimator that unstable is not identifying anything, so the split was NOT built. Note also that such a split is typically MIX-PRESERVING — at unchanged mix every ratio in the plausible band reproduces the same blended figure and the same audited revenue — so building it would add an unsourced driver and NO information while looking more precise. Instead, DECOMPOSE and PRICE what the coarse figure hides: DU's flat blended ARPU proved to be a mix tailwind of about +2.6% against per-leg erosion of about -2.4%, and because the study's own subscriber path assumed the mix shift would reverse, the exhaustion case was worth -17% on the cash-flow lens — the largest operating downside in the study, invisible until the coarse number was taken apart.

Two procedural rules adopted in the same pass:

5. A NUMBER STATED IN PROSE MUST BE COMPUTED, NOT TYPED — extended from builders to the four-field register's OWN justification text. Two register notes quoted like-for-like deltas of "-4.2%" and "+3.1%" against computed values of -4.13% and +2.98%. This is the same defect class as a financial numeral typed into a builder, and it is worse in one respect: the note is the audit trail. Deltas quoted in a justification are now computed in a pre-pass from the raw disclosed figures and interpolated into the note, with an assertion tying that pre-pass to the independent route the model computes later. Caught by a rendered-PDF read, not by any programmatic gate that existed at the time.

6. READING THE RENDERED PDF AND INSPECTING FIGURES AS IMAGES ARE GATES, NOT FORMALITIES — and delivering without them must never be described as verified. On one DU delivery both were skipped under time pressure and the delivery was presented as gate-passed. Run properly minutes later, they caught four real defects nothing else could see: the study CONTRADICTED ITSELF four lines apart (a new table caption correctly reporting a declining group margin beside an unrevised figure caption calling it "flat by construction"); the two typed percentages in rule 5; a forward-cone x-axis labelled in TRADING SESSIONS, a retired unit that must never appear in a deliverable under the calendar-only horizon rule; and a sensitivity heatmap whose title promised bold cells near spot when every cell in it sat above spot. Programmatic checks confirmed canvas, transparency, column widths and vocabulary throughout — and could see none of these.

7. A SELF-AUDIT THAT ONLY RE-CHECKS THE WORK IT DID WILL KEEP MISSING THE WORK IT NEVER DID. DU's edition-3 self-audit found seven defects no critique had raised and still missed the largest one, because every question it asked was of the form "do the model's numbers tie?". The question that found the real defect was "what do the filings disclose that the model does not consume?". Ask it explicitly, against the sweep register, before declaring a self-audit complete.

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

[NEW 08-Aug, per instruction — SWDY study] [SUPERSEDED 19-Aug-2026 — see THE MODEL REPORT below; ADNOCLS displaced SWDY under the one-in-one-out rule and SWDY is removed from the reference layer outright. The eight depth standards below stand unchanged and a ninth was added; only the exemplar changed.] THE MODEL STUDY — SWDY sets the structural template AND the research-depth bar

Adopted at Sherif's instruction, 08-Aug-2026, because the level of recent valuation reports had slipped below par. The fix is not a new checklist item — it is a new exemplar: SWDY_Valuation_Study_05-08-2026 (engine/swdy_study/ — the study, its Excel model, its standalone bibliography document, and its filled QC evidence table QC_GATE_05-08-2026.md) is THE MODEL STUDY. Every future study matches its sections list, its sheet list, and its depth of research. Machine-readable form: MODEL_STUDY + MODEL_STUDY_DEPTH + ModelStudyChecklist + assert_model_study() in engine/research_protocol.py — verified by IMPORT, not parse, same as the rest of the guard list.

THE REFERENCE SET IS CLOSED — exactly three names [08-Aug-2026, per Sherif's instruction]. SWDY is the MODEL STUDY and carries the operating-company lens pattern; ADCB carries the bank pattern; ALPHADHABI carries the holdco pattern. Those two are LENS-PATTERN references only: class adapts the lens and the indicator set (SWDY's own QC item (c) is the precedent — the telco checklist was rejected for a diversified industrial and the metrics re-cast for the actual class, inside the same skeleton), never the structure or the depth.

Every other company has been removed from the reference layer outright, not carried as a retired entry — a study named as "the old template" is still a name a future build can reach for, and a secondary exemplar of a class whose primary already covers it is redundant by construction. The set is enforced in code: REFERENCE_SET in engine/research_protocol.py asserts on exactly SWDY / ADCB / ALPHADHABI, so a fourth name cannot be added without displacing one of these three and failing the import first. That is deliberate — expanding the reference set is a protocol decision, not a documentation edit.

Note the boundary. This closes the REFERENCE layer only. Company names still appear throughout this protocol as EVIDENCE for a rule — the audit that produced the terminal-value procedure, the reconciliation that produced the cost-stack rule, the chart defect that produced the overlay gate — and as covered names in the calibration record. Those are the protocol's proof and its append-only history; stripping them would turn measured findings into unsourced assertions. A company name is only in scope for removal when it is being held up as something to copy.

The sections list (Word, 16 sections, in order): Masthead + READ FIRST · Headline · Valuation summary — every read at a glance · Company overview · §1 Fundamental valuation (1.1 the cash-flow model with the full FCFF waterfall AND the EV→equity bridge; 1.2 book value & sustainable return; 1.3 relative multiples; 1.4 normalised earnings power; 1.5 synthesis — the class primary IS the central under [R-LENS-03], the other lenses published beside it as cross-checks and the RANGE of their present-value reads as the envelope; NEVER a weighted blend, and never a set of typed weights; 1.6 the drivers — each disclosed segment grown on its own driver, margins as OUTPUTS; 1.7 the crux; 1.8 macro & country — the sourced cost of capital, the cost-of-debt evidence table, and every contested construction PRICED, not just named; 1.9 sensitivity) · §2 Technical and price structure · §3 A probabilistic price map (percentile map + level-touch ladder) · §4 Comparison of the lenses · §5 Catalysts to watch · §6 Reading the probability zones · §7 Caveats and what would change our mind · Appendix A financial statements (A.1 income statement 3y historical + 5y forecast; A.2 balance sheet; A.3 forecast balance sheet and cash-flow markers) · Appendix B peer frame, risk register — and the research register · Appendix C the expert panel (C.1–C.3 Expert 1/2/3 by method; C.4 cross-examination; C.5 the three in one room; C.6 reading the divergence) · About this series · Disclosure & Disclaimer.

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


## Results releases are swept WITH their statements [ADOPTED 09-Aug-2026 — MODON revision 2]

A reporting period is not swept until BOTH its financial statements AND its results
announcement are in the register. The two are different documents with different content:
the statements carry the audited/reviewed record; the release carries the operating
anchors that never appear in the statements — backlog and its composition, sales and
their geography, management's own net-debt definition and its current value, adjusted
EBITDA, portfolio counts on the current perimeter.

Adopted from a real failure, same day, same study. The first edition of the MODON study
(09-Aug-2026) swept the H1-2026 interim STATEMENTS — P&L, balance sheet, cash flow, even
citing them in the register with an 07-Aug date — but never fetched the H1-2026 RESULTS
RELEASE of 29-Jul-2026. That release carried a revenue backlog of AED 65.4bn (95%
development, +42% vs FY2025) and H1 real-estate sales of AED 26bn: the study's single
most consequential driver (the development backlog, struck at the 31-Dec-2025 value of
AED 42.6bn) and its central contested judgement ("does the surge persist?") were both
already answered by a disclosure the study partially cited. Four external audits caught
it; the study was restruck on the 30-Jun-2026 balance sheet the same day (DCF 6.02 →
5.29, weighted central 3.71 → 3.38).

The rule: the sweep's Company-ring "IR communications" category is not satisfied for the
study year until the LATEST results release is registered, and the quarter-coverage
invariant reads a period as covered only when both documents carry findings. When a
release post-dates the statements it accompanies, the release's operating anchors
(backlog, sales, net debt on the company definition) supersede any older anchors in the
driver set, or the study must state explicitly why they do not.

## Beta — the MODON worked example, and sensitivity bands in standard errors [ADOPTED 10-Aug-2026]

Companion to the beta-regressor rule above, which is canonical. That section settles WHAT the
regressor must be; this one records the case that priced it and adds one rule the earlier
section does not carry.

**The priced swap.** MODON revisions 1 and 2 regressed against an equal-weight composite of the
house UAE library after ten failed attempts to obtain the FTSE ADX General series. When the
series arrived (10-Aug-2026) the proxy proved to have under-read beta at EVERY window — 5-year
1.118 proxy against 1.278 official; the 3-year and 2-year official windows read 1.800 and 1.581.
The mechanism is arithmetic: β = corr × (σ_stock / σ_market), and the official index ran 11.5%
annualised volatility against the composite's 14.9%, a factor of 1.30, at a similar correlation
(0.298 vs 0.343). A better-diversified benchmark is a smaller denominator, so the true regressor
RAISES beta. Ke 9.08% → 10.28%, WACC 8.30% → 9.30%, the cash-flow lens AED 5.29 → 4.51, the
weighted central AED 3.38 → 2.98 — an 11.6% cut, past the 5%-of-central threshold that mandates
a full re-derivation. **This is what "price the swap" means in practice: publish what the proxy
read on the same weeks, what the index reads, and what the difference was worth per share.**

**A proxy's error has no reliable sign.** Before the official series arrived, a turnover-weighted
composite — built precisely because it approximated cap weighting better than equal weighting —
pointed the OTHER way (β 0.842, central AED 3.78), and a paired block bootstrap confirmed that
difference excluded zero at every block size {2,3,4}. Real, robust, and wrong about the
destination. Never reason about the direction of a missing input's effect from a proxy and
present the reasoning as a finding.

**NEW RULE — sensitivity bands are a property of the measurement, not round numbers.** MODON
revision 2 sensitised beta 0.8–1.2. The true value, 1.278, sat OUTSIDE that band, so the study's
own disclosed range did not bracket the answer while presenting itself as if it did. Beta strips
are centred on the adopted estimate in steps of ONE STANDARD ERROR of that regression. The same
discipline applies to any sensitised input carrying a measurable standard error.


## THE MODEL REPORT — ADNOCLS replaces SWDY as the document every study is modelled on [ADOPTED 19-Aug-2026, per instruction]

Sherif put two delivered studies side by side — ADNOC Logistics & Services (09-Aug-2026) and
Riyadh Cables (18-Aug-2026) — and said the obvious thing: they are both ours and they are
vastly different. The instruction was to settle on a model report, with ADNOCLS as the
superior document on depth and analysis, minus one section.

**ADNOCLS_Valuation_Study_09-08-2026 is THE MODEL REPORT.** Under the standing one-in-one-out
rule it DISPLACES SWDY, which is removed from the reference layer outright rather than carried
as a retired entry. The set stays at three: ADNOCLS (model report + operating-company lens
pattern), ADCB (bank), ALPHADHABI (holdco). `REFERENCE_SET` in `engine/research_protocol.py`
asserts on exactly those at import.

Why ADNOCLS: it prices every contested construction instead of naming it, publishes the beta
both ways, builds the cost of debt from six disclosed instruments rather than one asserted
range, drives seven disclosed units on seven physical drivers with margins as outputs,
reconciles the build against management's own guidance, and gives each expert a worked
valuation table with every intermediate line. Its beta is also the first in the reference
layer produced by the sanctioned routine against a published index
(`raw_indices/AE/FADGI.csv`, conforming); SWDY's was regressed on a composite.

**One section is excluded.** "What changed in these editions, and why" is in the exemplar and
is NOT part of the model: edition history is internal QC evidence and belongs in the study's QC
gate and critique adjudication, not in a document an external reader receives.

**The model report is a document, not a description.**
`engine/model_report/build_model_report_docx.py` produces
`engine/model_report/MODEL_REPORT_09-08-2026.docx` from the exemplar and asserts every edit, so
a future build opens the model rather than reconstructing it from a paragraph. Three
consequences were handled, and one is a small standing precedent in its own right:

1. **A live caveat was rescued out of the section before the cut.** The note that the
   sanctioned beta routine now returns 1.103 on 159 weekly observations, where every table in
   the study carries the adopted 1.085, is not edition history — it is a live discrepancy
   between an adopted number and the routine meant to produce it. It moved into §7 with the
   other caveats. STANDING RULE: before deleting a block of a document, check whether anything
   inside it is a live disclosure rather than history. A correction record can be dropped; a
   disclosure inside it cannot.
2. The READ FIRST box lost its edition paragraph, the same content class in the front matter.
3. "About this series" was repaired — it promised the reader a correction list "under 'What
   changed in these editions, and why'". The correction RULE stays; the mechanism is now stated
   as what the document does: the correction is made at the point it bears on, with the
   superseded construction reprinted beside the new one at full size. A document must not
   promise a section it does not have.

NOT removed: the inline "an earlier edition of this study…" passages in 1.2, 1.7, 1.8 and 7.
Each prices a live construction against the superseded one at the point the number is used,
which is the dual-framing rule doing its job.

**QC consequence.** Gate item (a) is unchanged in substance and now names ADNOCLS: structure,
content, format AND DEPTH match the MODEL REPORT. The eight depth standards adopted 08-Aug
stand exactly as they were.


## ENFORCEMENT — the rules that make the other rules bind [ADOPTED 23-Aug-2026, per instruction]

Everything in this section exists because of one measured fact: on 23 Aug 2026 an audit of
all 90 covered stocks found 63 not built ground-up and only 4 with an attestable beta, at a
moment when every rule requiring both was already written in this document and in the digest.
No one disagreed with a rule. No one read one and declined. The rules simply were not present
at the moment they bound, and nothing outside the study was looking.

### [R-ENF-01] A rule that can be checked must be checked from outside the thing it governs

**A self-attested boolean is never a check.** Where a standing rule can be expressed as a test,
that test must exist in code, must run over the work rather than inside it, and must fail the
build rather than warn. Where a rule genuinely cannot be tested — a judgement about a peer set,
the choice of a lens — it stays prose, and the QC gate carries the evidence a reader can weigh.

This is the generalisation of three lessons already recorded here separately:

- **beta** — `SIGCMChecklist.beta_own_history_vs_egx30` was a flag every study set `True` while
  regressing against a composite. Fixed by `assert_beta_provenance()`, which inspects the record.
- **the technical read** — the carve-out saying "leave the levels alone" protected staleness
  rather than judgement, until COMI published a 142.00 spot beside a narrative reading 129.25.
  Fixed by computing the read and gating the chart with `check_ta_chart_overlay.js`.
- **the digest** — kept in sync with this document by an instruction to remember, which
  CLAUDE.md itself records has failed three times in one session.

Each was fixed in its own place. None was generalised, so the identical hole stayed open in
eight of the nine SIGCM clauses for another two weeks. **When a defect of this species is found
again, close the class, not the instance.**

### [R-ENF-02] Every study calls the three gates, and a job outside the study verifies it

A study must call `assert_sigcm()`, `assert_beta_provenance()` and `assert_model_study()` in its
own committed code. `scripts/check_study_provenance.py` runs over every `engine/*_study/` from
outside, in CI (`.github/workflows/study-provenance.yml`), and fails on a study that calls none.

Written because 13 of the 21 study directories called none of them and no automated job ran any:
**a study passed by not checking itself.** The job also refuses a surviving study-local
regression script — the standing ban on hand-rolling one had produced two post-rule studies that
still did, one of them still building a composite alongside as a "corroboration".

The job is a RATCHET, not a cliff. Studies knowingly outstanding are listed in
`engine/build_depth_audit/outstanding.json` and are allowed to fail; the build breaks only on a
NEW violation or a study directory added with no gate at all. The list may only ever shorten —
`--prune` rewrites it — and its length is the honest measure of progress. A permanently red
check is one everybody learns to ignore, which is worse than no check.

#### [AMENDED 01-Sep-2026] `assert_model_study()` is itself a self-attestation, and one of its
#### nine fields is now measured from outside

`ModelStudyChecklist` has nine boolean fields and a study sets all nine on itself. On
01-Sep-2026 the AMOC rebuild set `structure_matches_model=True`, `assert_model_study()`
passed on that boolean, and the delivered workbook carried **seven sheets** — READ FIRST,
Assumptions, Base Year, Product and Cost, Forecast, Sensitivity, Lenses — against the model
report's sixteen.

What makes this the [R-ENF-01] species rather than an oversight is what the other gates were
doing at the time. The workbook recalculated through an independent evaluator with **zero
disagreements across 5,775 formula cells**. The external-reader scrub was clean. Table
discipline reported zero problems across both documents. The valuation-gap review had just
been written and passed. Every one of them was examining the workbook's **contents**; not one
was examining its **shape**, and the only thing that claimed to was a boolean the study had
written about itself.

`scripts/check_workbook_structure.py` now opens the LATEST-DATED workbook in every
`engine/*_study/` — the one that would be published, chosen by the date in the filename rather
than by modification time, so the answer does not depend on what a checkout happened to touch —
and asserts its sheet names ARE `research_protocol.MODEL_STUDY['excel_sheets']`, in that order.
It **imports** that list rather than carrying a copy: a check holding its own copy of a standard
stops testing the standard the moment one of them moves.

Same discipline as the gates around it. A RATCHET per this rule
(`engine/build_depth_audit/workbook_outstanding.json`, `--prune`, may only ever shorten — GBCO,
SCEM, STC and XPT were already off the standard on adoption day and are listed). The population
anchored elsewhere per [R-ENF-04]: a run that examined zero workbooks FAILS, and every listed
ticker must resolve to a directory on disk. Negative-controlled by
`scripts/check_workbook_structure_negative_control.py`, which reinjects the seven-sheet file
exactly as it shipped, a renamed sheet, a right-names-wrong-order file, a study with no
workbook, one that will not open, a listed study that vanished and an emptied population — and
runs three CLEAN cases that must stay green, among them a superseded off-standard edition
sitting beside a good current one.

**The general form, which is [R-ENF-01] applied to the attestations themselves: where a standard
can be read off the delivered file, read it off the delivered file.** An attestation is worth
only what an outside reader could not otherwise see. The fields that should survive as
attestations are the judgements a script genuinely cannot make — whether an expert appendix is at
maximum detail, whether the contested judgement was the right one to publish both ways — not the
ones a script can measure in a line.

A second defect of the same family surfaced in the same pass, and it is named here because it
will recur at every re-issue rather than once. Two of ARCC's own gates, `driver_test.py` and
`label_gate.py`, opened `ARCC_Valuation_Model_06082026_public.xlsx` while the delivered file was
the 01-09-2026 edition. Both reported clean. Re-pointed at the delivered file, five of 144
driver assertions failed immediately: revision 4 had moved the valuation date to 30 June 2026 and
put the bridge on that reviewed balance sheet, so the FY2025 cash, minority and declared-dividend
rows no longer move the headline, and the assertions saying they did had never been run against
the model that shipped. **A check that opens a delivered file by name moves with the re-issue.**
Both findings are registered as L-066 and L-067 under [R-LESSON-01].

### [R-ENF-03] The published technical read is checked from outside, through a real JS parse

`scripts/check_technical_read.py` hands `assets/data.js` to node and asserts on **the object the
page renders**, not on a model of it. Six invariants: no entry declares `levels`/`tech`/`asof`
twice; three resistances ascending and three supports descending; R1 above and S1 below the close
the narrative itself states; `bull`/`bear` naming the levels the table publishes; the whole read
reproducing from the raw library; a coherent two-part stamp whose `tech.data` IS the library's
last session. It runs in CI beside the two gates it backstops
(`.github/workflows/page-integrity.yml`).

Written because a READER, not a check, found it. On 25-Aug-2026 gbco.html published a key-levels
table whose nearest support sat ABOVE its own close, three lines beneath a narrative quoting a
different and correct ladder; clho.html had all three published resistances BELOW its close. Both
existing gates reported both pages clean that same day. They parse data.js with regexes,
`re.search` returns the FIRST match, a JavaScript object literal takes the LAST — and both entries
declared `levels` twice, so `apply_technicals.py` rewrote the first while the browser rendered the
second. Valid markup, no console error, a freshly computed narrative sitting over a superseded
ladder, and every automated check looking at the half the reader never saw.

**A checker that models the parser is checking a different file from the one that ships.** This is
the JS analogue of VERIFY BY IMPORT, NOT BY PARSE, a rule this protocol already carried before
either older gate was written — which is the uncomfortable part: the principle was present, the
gates were built without it, and nothing compared them. Same family as the unquoted-key regex that
silently dropped 2POINTZERO from three tools at once and the indentation-keyed `dist` match that
deleted `touch` on nine entries: a pattern standing in for a parser is silently correct on exactly
the entries shaped the way its author's were.

Two design points that are load-bearing rather than stylistic. The bracket test anchors on the
close the NARRATIVE states, never on `spot`: those are two clocks, since a mid-cycle library
arrival refreshes the technical read without re-striking the cone, so anchoring on spot would fire
on a legitimate divergence and still miss an impossible ladder struck the same day. And library
age is reported as an advisory, never a failure — see the staleness rule above for why.

Negative-controlled, not merely observed green: against the pre-fix data.js the gate returns 14
failures across the two entries, from four independent checks, and exits 1; against the corrected
file, zero.

### [R-ENF-04] An empty result is not a clean result

**Adopted 25-Aug-2026.** The same failure shape appeared four times in a single session,
and every one of them nearly shipped as a pass:

* a local `origin/main` ref, 24 commits stale, read as current — and produced a confident,
  wrong "this was never merged";
* an Actions query keyed on a TRUNCATED commit SHA returned `0 runs`, which read as "no
  failures" when it meant "the query matched nothing";
* a negative control searched for `"EMFD"` while `data.js` writes object keys UNQUOTED, so
  it modified nothing, the gate went green, and that green was evidence only that the file
  was untouched;
* a `gh` route was declared impossible on the strength of `command -v gh` — the binary
  installs from apt in one line, and the route then failed for a completely different and
  far more informative reason.

None of these were wrong ANSWERS. They were absent answers wearing the costume of a clean
one, which is strictly worse: a failure announces itself, an empty result does not.

This protocol already carried two rules of exactly this species — COUNT AGAINST A KNOWN
TOTAL, never trust a tool's own "0 skipped", and VERIFY BY IMPORT, NOT BY PARSE — each
adopted after its own incident and neither generalised. [R-ENF-01] says that when a defect
of this species is found again, the CLASS gets closed rather than the instance. This is that.

**Measured, not assumed.** `assets/data.js` was emptied to a valid, loadable file holding
zero entries and every gate re-run. `check_page_integrity`, `check_data_freshness` and
`check_technical_read` ALL EXITED 0 AND REPORTED CLEAN. They were not broken; they
faithfully checked every one of nothing.

**The rule.** Every gate declares what it examined and is held against a population counted
somewhere else. `scripts/coverage_floor.py` anchors on the persistent OHLC libraries on
disk, chosen because it is independent of `data.js`: defeating the check would mean emptying
the libraries too, which is a far louder failure than an empty page file. The comparison is
EXACT, never a threshold — a threshold would be a free parameter with no evidence behind it,
which the promotion rule forbids elsewhere for the same reason. A library staged but not yet
published therefore FAILS the gate and is named, which is the intended behaviour: "counting
one side alone is what let 9 names rot unnoticed" is already written into
`check_data_freshness`'s own first check.

**A gate's SECOND population is guarded too.** `check_page_integrity` builds its scope from
the HTML files on disk, so an empty `data.js` leaves its page count untouched and merely
makes its data.js cross-checks VACUOUS. The negative control caught precisely that against
the first draft of this fix — 93 pages walked, "Clean" printed, nothing actually compared.
A cross-check that would compare against nothing now refuses instead. Zero is the only
value that makes a comparison vacuous, so zero is what is refused; a 92-of-93 coverage is a
real property of the book, not a floor violation.

**Negative-controlled**, because a check nobody has seen fail is not evidence:
`scripts/check_coverage_floor_negative_control.py` reinjects the measured condition, asserts
every gate goes red, and restores `data.js` verified byte-for-byte. It runs in CI beside the
gates it backstops.

**The general lesson, which is not about these gates.** WHEN A PROBE COMES BACK EMPTY, THE
FIRST HYPOTHESIS IS THAT THE PROBE DID NOT RUN. Re-run the exact operation before believing
the absence, name the specific path that failed rather than the category, and never
generalise one failed probe into "impossible" — the four incidents above were each caught
only by re-running the exact operation, and three of them had already been reported as clean.

### [R-SIGCM-02] The ground-up clause is attested on a record, not a flag

`forecast_ground_up` is no longer a boolean a study sets on itself. A study records, for **every**
revenue line, how that line was actually built — the physical unit, the disclosure the unit came
from, the price basis, the cost-per-unit basis — and `research_protocol.assert_ground_up()`
inspects it. Four levels are recognised, and only the first is the standard:

| level | meaning |
|---|---|
| `unit` | volume × price on a **disclosed** physical unit, cost per unit, margin an output |
| `derived` | real unit economics on a volume that is indexed, estimated or back-solved rather than disclosed |
| `segment` | the disclosed segment on its own driver; no unit economics available |
| `topdown` | a growth path plus a margin assumption — the floor of last resort |

Two refusals are built in and both matter. The lines must cover **100% of revenue**, because a
line left out of the record is a line nobody checked. And any line below `unit` must carry a
`gap_note`: the rule has always permitted a coarser level where the disclosure stops, and has
never permitted going quiet about it. Claiming `unit` without naming the unit, its source and the
price basis also fails — claiming the level is not the same as having built it.

Adopted because the audit found 63 of 90 studies not built ground-up while the flag sat available
to be set `True`. The delivered studies already write all of this in prose in §1.6; the record
only asks for it once more in a form a machine can refuse.

### [R-BETA-04] The beta record has a required shape, and the shape is checked even when the study is silent

`assert_beta_provenance()` already demands `beta, r2, se, n, usable, index_file, index_asof,
market, exchange, conforming` and a `raw_indices/` path. The hole was that a study which never
called it could record whatever it liked. Across the 21 directories the regressor was recorded
four different ways — a full path, a bare filename, a prose name with no file, and nothing — and
the weakest shape silently defeated the gate. The repo-level job now applies the same test from
outside, so the record's shape is enforced whether or not the study checks itself.

### [R-STD-01] Every study is stamped with the standard it was built to

`research_protocol.STANDARD_VERSION` names the current standard; a study records the version it
was built against; the repo-level job reports any study built to an older one. Bump the version
only when a change would alter a delivered number or a required artefact — never for prose.

Written because the question *"is this study finished, or finished-for-now?"* had no answer in
the repository. Without a version, a book-wide re-issue is an open-ended obligation: a name
re-issued in September can silently need re-issuing in November, and nobody can tell which names
are current. With one, the rebuild queue is finite and its remainder is countable.

### [R-IDX-01] One index, one filename, registered — or documented as deliberately held

Every `.csv` under `engine/raw_indices/` is either registered in `wacc_builder.EXCHANGE_INDEX` or
listed, with a reason, under `held_unregistered` in `outstanding.json`. Nothing else may sit there.

Written because `ADXGENERAL.csv` was a byte-identical duplicate of `FADGI.csv` under a filename
the resolver does not register. ADNOCDIST and ADNOCDRILL regressed against that copy: the right
number, with provenance that cannot resolve. No rule said a file in this directory must be either
registered or gone, so nothing objected. The Dubai series `DFMGI.csv` is the documented case of a
file held deliberately — see the DFM interim above.

### [R-DOC-01] Standing rules carry an identifier, and both documents are checked against each other

Every rule adopted from 23 Aug 2026 carries a stable identifier of the form `[R-AREA-NN]`. The
identifier appears in this document, in the condensed digest, and in the code that enforces the
rule. `scripts/check_protocol_sync.py` compares the identifier sets and fails on any rule present
in one document and not the other.

Rules adopted before 23 Aug 2026 are **not** retro-tagged in bulk — a large mechanical edit across
a hundred kilobytes of prose carries real transcription risk and no reader benefit. Each acquires
an identifier the next time it is amended, so the tagged set grows from the bottom up and the
check binds only what has been tagged.

Written because the digest is kept in sync with this document by an instruction to remember, and
on 23 Aug 2026 the copy held outside the repository was found to be one amendment behind. Three further
rounds of "is this the version to adopt?" that same day each pasted back a copy one edit stale, because
every revision of a 54,000-character block looks identical to every other. **Both documents therefore
carry a REVISION STAMP as their first line** — a copy that does not carry the current stamp is stale on
its face, without reading a word of it. Bump the stamp on every edit, however small: an unbumped stamp
is worse than none, because it certifies a copy that has moved. The
identifier also gives an amendment one obvious place to land, and lets a QC gate cite the rule it
is testing rather than paraphrasing it.

**THE DIGEST FILE IS NAMED FOR THE DAY OF ITS LATEST AMENDMENT** [AMENDED 31-Aug-2026, per
instruction — "The project instructions need to be named as of today and the revision a, b,
c"]: `engine/PROJECT_INSTRUCTIONS_{DD-MM-YYYY}.md`, so the filename and the revision stamp
agree on their face, and the revision letters restart at "a" on each new amendment day. The
rename happens IN THE SAME COMMIT as the first edit of a new day, and every live reference
moves with it: the sync gate, the text gate and the digest-page builder resolve the file BY
PATTERN (exactly one file on the `engine/PROJECT_INSTRUCTIONS_{DD-MM-YYYY}.md` pattern, or they fail loudly), so a rename
cannot strand them; the CI trigger paths glob it; and the one reference that cannot glob —
the include line at the top of CLAUDE.md — is updated in that same commit. DATED RECORDS ARE
NOT REWRITTEN: a session note, QC gate or PENDING_REVIEW file that quotes an older digest
filename quotes it as it stood, the same append-only discipline as the ledgers.

### What rev. 6 deliberately does NOT change

No research method changes. No lens, no driver rule, no cost-of-capital construction, no
calibration procedure is altered by this revision, and no delivered number moves because of it.
Every rule above is about whether the existing rules execute.

Nor does rev. 6 touch the thing this protocol does best: **almost every rule here names the
failure it came from.** That is why the rules are obeyed when they are met at all, and it is the
most unusual property of this document. Every amendment above arrives with its own failure
attached, in the same voice, and every future one should.

---

## [R-LENS-01] THREE-LENS INDEPENDENCE — the fundamental study, the MC engine, and the technical read never feed each other (23-Aug-2026, per instruction)

**The rule.** The fundamental study, the MC price engine, and the technical read are three
INDEPENDENT lenses on the same stock. No lens's output is ever an input to another. They are
published side by side, so agreement between them is information; a blended lens is just one
opinion wearing three names. Stated by Sherif on 23-Aug-2026, while reviewing the view-layer
prototype: "the direction should be based on the MC alone and not the fundamental study. The
reason is that we want the fundamental, MC and technical studies to be independent from each
other."

**Where it came from.** An investor told Sherif the published MC "looks nice but is not
useful," then sharpened it to two findings: the cone is very wide, and it has no direction.
Both were verified true on the live library (the 3-month 90% band averaged ~57% of spot across
the 90 covered names that day; the center of every cone was the interest-rate carry alone).
Two responses were built the same day on the feature branch, neither published:

1. **A view-layer prototype** (`engine/view_layer_prototype/`) — the typical (middle-half)
   band leading, the 9-in-10 band demoted to a whisker, and a direction object. The FIRST CUT
   drew that direction as a fan from spot to the study's fair values. That is the construction
   this rule retires: it made the MC card's direction a consumer of the fundamental lens.
2. **A direction tournament** (`engine/direction_tournament/`) — six price-only candidates on
   the full cleaned library under the Phase B direction-aware referee (`direction_score.py`),
   both calendar horizons, cross-sectional and pooled framings, block-bootstrap {2,3,4}, LONO,
   split-half, MIN_N=100. Momentum-family candidates survived all four tests at once in AE and
   (more weakly) EG and SA; several technical-family constructions (200-day trend, 52-week-high
   proximity) also tested well. Read the RESULTS file for numbers; they are not repeated here.

**Consequences, each binding:**

1. **MC direction comes from price-native signals only**, fitted through the engine's existing
   per-market signal socket (`signal_type`/`ic`/`signal_active` in `market_profiles.py`),
   promotion-gated exactly as before. A fair value never enters drift. The
   `Fundamental_MC_Integration_Protocol.md` §8 engine hook — value-gap IC into `profile.ic` —
   is **permanently retired as a drift source** (its header now says so). Phases A–C continue
   as a *measurement and comparison* layer: the value-gap IC may be measured forever as a
   diagnostic of the fair values themselves, and `fv_overlay` remains a downstream comparison
   surface. Comparison reads both lenses' outputs and feeds nothing back; that is the one
   sanctioned way the lenses may meet.
2. **Technical-family constructions are ineligible as MC drift signals** even where they test
   well — moving-average distances, 52-week-high proximity, RSI and kin belong to the
   technical lens, and wiring them into the MC would make two of the three lenses agree by
   construction. The eligible pool for an MC lean is the momentum family (12-1, 6-1) and other
   constructions the technical read does not use. The tournament's technical-family survivors
   stand recorded as evidence, excluded from promotion on this ground alone.
3. **Nothing is adopted as of 23-Aug-2026.** Tournament survivors are candidates for the
   standing promotion rule (the honest next step is a pre-registered forward shadow cohort,
   as `lab_round8_fvpull.py` already prescribes for a different candidate). Until a lean
   passes, any product surface showing one labels it ILLUSTRATIVE and leaves every published
   cone number untouched — the prototype demonstrates the labelling.

**Why the rule is right, recorded so it survives staff turnover of one:** the site's product
is three independently-computed answers to the same question. The moment one lens borrows
another's output, their agreement stops being evidence and the reader has no way to see that
it stopped. Independence is also what makes the grading honest — each lens can be scored on
its own record, and a lens that fails can be fixed or retired without contaminating the others.

### [R-LENS-02] Each lens is calibrated on its own clock, beside the MC calibration and never inside it (31-Aug-2026, per instruction — "beside MC and not added to it. Technical is up to 1 month, MC 1 to 3 months and fundamental up to 1 year")

Adopted in a parallel session on the same day the technical and fundamental calibrations
were adopted, and folded in here SLIMMED: the original text restated both of those
calibrations in miniature, and a rule restated in two places is the drift disease
[R-DOC-01] exists to close — the per-lens machinery is owned by [R-CAL-02] (MC),
[R-TCAL-01] (technical) and [R-FCAL-01] (fundamental), and this rule states only what
none of them states alone.

**THE SYSTEM CARRIES THREE LENS-LEVEL CALIBRATIONS OF THE SAME SPECIES** — a dated
claim, frozen when made, graded against what happened:

- **MC** — the band record, per [R-CAL-02]. The only one published.
- **TECHNICAL** — the walk-forward replay of the shipped read plus the per-name record,
  per [R-TCAL-01].
- **FUNDAMENTAL** — the pre-registered walk-forward training record, per [R-FCAL-01];
  `engine/phdc_walkforward/` is the worked precedent and pattern.

**CALIBRATING A LENS DOES NOT COUPLE IT — [R-LENS-01] EXTENDS FROM LENS OUTPUTS TO LENS
CALIBRATION RECORDS.** No record, score or lesson from one lens's calibration is ever an
input to another lens's fit, drift, width or read. The reasoning is the parent rule's
own: a calibration record is a measurement OF a lens, and feeding it sideways recreates
the echo [R-LENS-01] removed — two lenses that agree because one was tuned on the
other's report card are one lens wearing two hats. Comparison surfaces (`fv_overlay`,
`three_lens_trial`) remain the one sanctioned meeting place: they read outputs and
records to compare them, and feed nothing back.

**THE HORIZON LADDER IS A ROLE ASSIGNMENT, NOT A STRIKE, GRADING OR METHOD CHANGE.**
TECHNICAL speaks to up to one month — the immediate entry/exit reference, on its own
short clock, and per [R-TCAL-01] the read no longer promises the far zone. MC speaks to
one to three months — the calendar cones, 1M/3M standing by the 23-Aug-2026 instruction.
FUNDAMENTAL speaks to up to one year — the fair-value range. Three clarifications keep
the ladder honest:

1. The DCF still projects five forward years to DERIVE the value. The ladder assigns
   the horizon of the published CLAIM, never the modelling horizon — and the fundamental
   walk-forward's own finding is that the far years of a projection support ranges,
   never points.
2. **No lens gains a claim its evidence does not support because a horizon was assigned
   to it.** The strength ladders — [R-CAL-02]'s and tech_record's — still decide per
   name what may be said at all.
3. The MC 1-month cone, the monthly metronome, and metals' 12-month clock are untouched.
   Nothing here strikes, grades, or re-times anything.

**RENDER DISPOSITION UNCHANGED.** What a reader is shown remains exactly [R-CAL-02]'s
list. The technical and fundamental records stay generated-never-typed internal records
on the CALIB disposition until a render instruction names what a reader sees —
surfacing any of them beside the band record is its own explicitly-requested step.

### [R-DRIFT-01] Addendum, same day — COMMITTED DRIFT ADOPTED (23-Aug-2026, per instruction)

Hours after the rule above was recorded, Sherif closed the loop on the investor's second
finding: "we have to find a way to commit to a drift up or down. The investor is adamant."
Adopted, by explicit instruction, in lieu of the shadow-cohort step consequence 3 had
prescribed:

- **The momentum lean is ACTIVE in the engine.** `signal_type="mom_12_1"`,
  `signal_sign=+1`, `signal_active=True` in AE, SA and EG — the three markets where the
  tournament's momentum cells survived all four tests. Each market's `ic` is the SMALLER of
  its two tournament horizon readings (conservative; read `market_profiles.py` live for
  values). SA's 3M ic is disclosed as carried from its 1M measurement — the 3M pooled read
  was underpowered, while its cross-sectional read agreed in sign. The old rev_1m priors
  (EG, AE) and SA's contrarian momentum sign are refuted by measurement and replaced.
- **Every covered name's forecast states a direction call** — the sign of its own momentum
  z — even inside the engine's dead zone (|z| < 0.5 → call printed as WEAK, tilt 0). The
  strike path already records `signal_z`/`signal_alpha` per horizon, so every call is
  graded at its maturity; a sustained failed-direction record triggers the standing
  out-of-cycle review. Markets with no surviving cell (QA/IN/US/KR/metals) stay
  carry-centered and call-only on product surfaces.
- **[R-NEG-01] The document-techniques backtest is the negative control** (`engine/doc_techniques_backtest/`,
  same day): GBM-historical-drift, ARIMA-family, pooled neural nets, Markov/fuzzy chains,
  Kalman drift, seasonality and their ensemble all failed to beat the carry center on 15
  walk-forward years — most robustly worse. None may return as a drift source without new
  evidence. AE month-of-year seasonality stands flagged as a rank-signal candidate only.
- **Width floors are measured facts:** the middle half of real 3-month moves spans ~13%
  (AE), ~19% (SA), ~26% (EG) of price. An honest 50% band cannot average narrower at these
  horizons, whatever the technique — the tested alternatives narrowed nothing at honest
  coverage. The sanctioned levers are the per-name width overlay (both directions — it
  answers "is this name's cone the right width", never "make the bands smaller"), the
  guarded mid-band shape selection ([R-SHAPE-01], which calibrates the 25–75 band at a
  FIXED 90% edge), and the horizon. Horizons stay 1M/3M by instruction; a
  shorter-horizon product was offered and declined.
- **Mechanics:** the adoption changes future strikes only (next roll-forward onward);
  nothing retroactive, nothing published until the standing publish flow runs. Panel
  refits under signal-ON route through the materiality gate; an engine-change PR carries
  this to main per GIT/PUBLISH MECHANICS. A subset ON-vs-OFF ablation record accompanies
  the adoption commit (`engine/PENDING_REVIEW/signal_on_ablation_20260823.py`).

**Same-day upgrade — "the tilt is still very conservative" (client, relayed; per
instruction).** The first cut carried three conservatism choices that were mine, not the
evidence's: ic shrunk to the smaller horizon reading, the tested-but-cautious socket knobs
(dead zone 0.5, z clip 2.0, alpha cap 0.5σ), and a single signal per market. All three
revised to track the measurement exactly:

1. **mom_combo** (equal-weight 12-1 + 6-1 momentum z) measured on the tournament rig —
   `engine/direction_tournament/COMBO_MOMENTUM_23-08-2026.json`. It passes all four tests
   in AE (1M +0.108, 3M +0.185 — the strongest direction result in the system) and EG
   (+0.062 / +0.068) and is adopted there; in SA the combo measured WEAKER than mom_12_1
   (+0.082 vs +0.093 at 1M, PARITY at 3M) and was NOT adopted — SA keeps mom_12_1. A
   candidate that tests worse does not ship because it is newer.
2. **Per-horizon ic** via `profile.ic_by_h`, at each horizon's own measured value; the
   min-horizon shrink is retired. SA's 3M value remains carried from its 1M measurement,
   disclosed as before.
3. **Socket knobs** softened to dead zone 0.25, z clip 2.5, alpha cap 0.75σ: the ICs were
   measured on raw z with no dead zone, so the knobs now follow the evidence rather than a
   caution preference. Typical strong-trend tilts roughly double (UAE ±2–3% becomes
   ±3–6.5% at 3M); Egypt's stay ~±1–3% because Egypt's measured IC is genuinely small —
   the honest ceiling, stated to the client as such rather than inflated.

The hard line that remains: the tilt never exceeds IC × σ × z. Beyond that point a bigger
number is not more commitment, it is a worse forecast on purpose, and the public grading
would document it within a few cycles.

### [R-DRIFT-02] Per-name discipline on the tilt (same day, per instruction — "Do it per stock. This is a delicate exercise and needs to be done carefully")

The per-stock record for every covered name is maintained under the exact production
construction: the careful dossier (`engine/direction_tournament/PER_STOCK_CAREFUL_23-08-2026.md`
— house robust bootstrap across blocks {2,3,4}, Wilson intervals on hit rates, split-half
consistency, conditional call records) and the full seed-paired ON-vs-OFF production
backtest of all 93 tickers (`TILT_BACKTEST_ALL93_23-08-2026`). Read those files for
numbers, never any digest.

The ONLY sanctioned per-name exception to a market's tilt is the PRE-REGISTERED
suppression bar, fixed before the numbers were computed: a name's tilt is suppressed iff,
at either horizon, its own-history IC is a robust FAIL across all bootstrap blocks AND
split-half both-halves-negative AND n ≥ 40. Anything weaker — a contrary point estimate, a
single-block excursion, an inconsistent split — is a WATCH FLAG: recorded, graded live,
revisited at every refit, never acted on. Per-name tilt exceptions outside this bar are
curve-fitting and PROHIBITED. A suppressed name still prints its direction call, flagged
low-confidence. Rationale: with ~186 stock-horizon tests at 90% CIs, a handful of false
single-test excursions arise by chance alone; the joint bar keeps the expected
false-suppression count well under one, and the first full sweep (23-Aug-2026) suppressed
zero names while flagging thirty.

### [R-GRADE-01] Early grading — opt-in, bounded, annotated (24-Aug-2026, per instruction — "We deal based on calendar days as per the project instructions and research protocol")

A horizon is a CALENDAR commitment, so a row matures when its calendar grade date
arrives — not when some number of sessions have printed. The two can separate: the month
is up while the exchange has not yet exported that last session. Until today the grader
treated that case as BLOCKED, identically to a library weeks behind, and a name whose data
ran right up to the calendar boundary sat ungraded beside one that was nowhere near it.

`grade_ledger.grade_session()` now returns HOW the session was reached — `exact`, `rolled`
(a closure pushed the first real session past the stored date, the pre-existing case) or
`early` — and `allow_early` grades a matured row on the LAST session inside its window.
Two properties make it safe, and both are structural rather than remembered:

1. **It is OFF by default**, so every existing caller is byte-identical. The negative
   control proves it: the replay of all already-graded rows reproduces them exactly, and
   the default sweep on the day of adoption returned the same 0 gradable / 19 blocked it
   returned before the change.
2. **It is BOUNDED by `EARLY_MAX_DAYS` (7 calendar days)**, and it is scoped to NAMED
   instruments. On 24-Aug-2026 nineteen rows were matured and blocked. EAND's library
   reached 21-Aug against a 24-Aug grade date — ONE session short, a real export lag.
   Eighteen AE names stopped at 24-Jul, a full month short, where "grade it early" would
   score a cone against a window that mostly never ran. An unbounded flag would have
   graded all nineteen alike. A row outside the bound stays BLOCKED with the flag on.

Scoping to named instruments is the second half of the lesson and was added after the
bound was already in place. With the bound alone, `--allow-early` would have graded
ADIBUAE and ADNOCGAS too — both had libraries at 21-Aug that week — turning a decision
about ONE name's permanent record into a decision about every name whose export happened
to be lagging. A blocked row inside the bound but not named now says so explicitly
("within the 7-day early-grade bound, but X was not named for early grading"), so the
un-taken decision is visible rather than absent.

An early grade is ANNOTATED on exactly the same terms as a rolled one, because the reason
is the same: the stored commitment is never overwritten in silence. `grade_date` becomes
the session actually graded, `grade_date_projected` keeps the original calendar date, and
`grade_note` states the gap in calendar days. The frozen percentiles are untouched — a
grade appends an outcome, it never revises the claim.

The cost is real and is not hidden: a window graded a session short is marginally narrower
than the one committed to, which very slightly favours the cone. That is why this is opt-in
per name and bounded at a week, rather than a new default. The alternative on the table —
grading against a close that does not exist — is not available at any bound.

### [R-SHAPE-01] Guarded mid-band shape selection (24-Aug-2026, per instruction — "Reshape UAE and Egypt to make it less conservative")

**What was found.** The investor read the live record as "slightly cautious in Egypt and
extremely cautious in the UAE." Measured under the actual production cones, half of that
held: the 90% edges were on target everywhere, but the 25–75 band was catching materially
more than half in exactly two markets — a mid-band-only distortion the pooled MLE cannot
see, because ν is weakly identified. The standing protocol has said since the (ν,
width_cal) fit was adopted that several tail-shapes sit inside the 95% likelihood region
and that the honest object is the cone the PAIR jointly produces. The MLE breaks that tie
blindly, and the tie is not innocuous: shapes on the same **iso-90% ridge** — width_cal ×
T95(ν) held exactly constant, which is also R-CAL-01's materiality metric, so every ridge
point publishes the identical 90% edge — differ visibly in how wide the middle band is.
On adoption day, AE's MLE shape caught 53.8% in its 50% band while a ridge-mate about two
log-likelihood units away caught 50.9%, with a 25–75 band roughly a tenth narrower.
Choosing the ridge point whose 50% band catches half is **calibration, not narrowing.**

**Why this is not the retired CRPS-selection mistake.** That precedent chased an
in-sample score across the whole parameter space and lost under LONO. This rule confines
the choice to likelihood-equivalent shapes on one ridge and releases it only through five
pre-registered guards, three of them out-of-sample in character:

1. **G-flat** — the candidate sits inside the 95% joint likelihood region (ΔLL ≤ 3.0
   against the unconstrained MLE) with width_cal inside the shrink legality clip: only
   shapes the data cannot tell apart are eligible at all.
2. **G-improve** — it must close at least one full point of |cov50 − 50%|. SA's
   adoption-day decline: 0.4 points from target, nothing to fix, noise-chasing refused.
3. **G-split** — BOTH calendar halves must move strictly toward 50%. EG's adoption-day
   decline: its mid-band over-coverage lives entirely in the late half while the early
   half already under-covers, so no single shape helps both — a regime artifact, not a
   shape property.
4. **G-lono** — pooled leave-one-name-out coverage must improve, every name scored under
   a shape selected without it.
5. **G-crps** — the reshaped cone's pooled crps/spot must not be robustly worse than the
   MLE shape's across bootstrap blocks {2,3,4} (the house robustness bar, mirrored).

**The guards are the release** — the R-CAL-01 lesson applied at birth rather than
retrofitted: a market reshapes automatically at any refit where all five pass, and
reverts to the MLE shape the refit they stop passing. There is no per-market flag to
remember and nothing for a later session to forget; live state is
`fitted_configs.json`'s `mid_band_reshape` field, never a status sentence here
([R-DOC-02]).

**The promotion rule binds instructions too.** The adoption instruction named Egypt.
Egypt's candidate failed G-split and the decline stood. A reshape that fails its guards
does not ship on anyone's say-so — the same clause that stops the pipeline from
promoting an unearned signal stops a human from promoting an unearned shape, and the
client is told plainly why, with the numbers.

**Mechanics.** `panel_refresh.reshape_mid_band()`, called inside `refresh_market()`
immediately after `fit_nu_scale` + `shrink_cal`; every future refit — unattended or via
`scripts/adopt_calibration.py` — reproduces the selection under the same guards, so an
adopted reshape survives refits without any hand-carried number.
`auto_refresh.write_production()` records the full reshape note (applied or declined,
with the failing guard) in `fitted_configs.json`. The 90% edge never moves by
construction, so a reshape can never fire R-CAL-01's cone-move reason by itself; the
verdict machinery (per-name LONO fits, `robust_verdict`) is untouched. R-NEG-01's width
floors stand — the objective pins the 50% band to catching half, which IS the floor.
Adoption-day numbers of record live in the dated evidence file under
`engine/PENDING_REVIEW/` and in `fitted_configs.json` — never in this document.

### [R-REC-01] Every stock's page carries its own calibration record (24-Aug-2026, per instruction — "we need to stop looking at stocks in a country as a bulk; look at each stock individually")

**Why.** The market aggregate hid a per-name spread the investor could see with his own
eyes: on the same Egyptian panel whose pooled 50% band catches ~52%, RAYA and SCEM caught
70% in their middle band while ISPH's wide band caught only 77% — one market number, names
wrong in both directions. The judgement unit is the stock, so the published record must be
per stock.

**What.** `engine/build_name_calibration.py` computes, for every covered stock, its own
backtest record under the LIVE production cone — resolved three-month tests in its history,
and how often its middle (25–75) and wide (5–95) bands actually caught the close — and
writes one generated `CALIB` block into `assets/data.js`, keyed by the entry's exchange
code (ticker keys are not unique across markets: EG ADIB vs UAE ADIBUAE). `app.js` renders
it in plain language under the fan on every page through the same universal
`renderStaticFan` hook the as-of stamps use, so no page template is edited and a new page
inherits the record.

**Discipline.** Regenerate in the same pass as any refit, reshape, panel rebuild or
roll-forward — the record rots the moment the fit moves, the same defect class as the
stale technical read closed on 29-Jul-2026. The builder is self-verifying: `node --check`
on the result plus a load-assert that counts records against the full TICKERS total and
fails loudly on any unresolved name (the count is not decoration: on adoption day it
caught ALRAJHI, whose Tadawul code is the numeric 1120 and whose raw file is RAJHI.csv —
a silent skip would have shipped 89 of 90 and reported success). Numbers are computed by
the exact fast_rescore band algebra on the panels' invariant residuals — verified against
the stored panel flags at 99.4–100% agreement — never typed.

**Companion executors, same day, same instruction.** `engine/direction_record.py` is the
computing executor of [R-DRIFT-01]'s promise that every direction call is graded at its
maturity: it joins each ledger row's frozen `signal_z` with its graded outcome and prints
the per-name and pooled hit record (first run: 68 calls recorded and open, 0 graded — all
graded rows predate the adoption; the scoreboard accrues from the September maturities).
`engine/lab/width_overlay_ae_sa/validate.py` is the standing, re-runnable promotion gate
for extending the per-name width overlay beyond Egypt: on its first run (24-Aug-2026) AE
DECLINED on breadth (7 of 14 moved names closer; pooled |std_u−1| improved 0.036→0.022,
CRPS parity, cov90 in-band) and SA DECLINED on the pooled measure (0.051→0.053 despite
7-of-9 breadth) — the GCC's histories are still mostly below the 28-window gate, so the
evidence is thin exactly where the mechanism would act. Re-run at any roll-forward; adopt
per market only when all four gate rows pass. Egypt's overlay is untouched.


## [R-FCAL-01] FUNDAMENTAL CALIBRATION — the forecasting method is walk-forward tested on the company's own history before it is trusted on its future (31-Aug-2026, per instruction — "It is time now to add the walk forward fundamental training (fundamental calibration) to the research protocol and the standing instructions")

### The name, and the confusion it exists to prevent

THREE DIFFERENT TESTS IN THIS SYSTEM ARE ALL CALLED A WALK-FORWARD, AND THEY ARE NOT
THE SAME THING [AMENDED 31-Aug-2026 by R-TCAL-01 — the count was two at this rule's
adoption]. Conflating them once already understated this project's evidence base
badly, in a document written to describe it.

**PRICE-ENGINE CALIBRATION [R-CAL-01 … R-CAL-03]** tests the Monte Carlo cone: strike
it at a past origin, score band coverage and a proper score against a carry-anchored
random walk. Its evidence base is broad — every covered name with a
`{ticker}_study/backtest_rows.csv`.

**FUNDAMENTAL CALIBRATION [R-FCAL-01], this rule** tests the FORECASTING METHOD:
rebuild the driver model as it would have stood at a past origin, project it forward,
and score each driver against what the company actually reported. Its evidence base is
narrow and must be described as such.

**TECHNICAL CALIBRATION [R-TCAL-01]** tests the TECHNICAL READ: replay the shipped
read at every historical origin and grade each templated sentence against what price
then did, on the lens's own under-one-month clock. Its evidence base is the broadest
of the three.

They test different machinery on different evidence and none substitutes for another.
NEVER write "the walk-forward" without saying which. READ THE POPULATIONS LIVE —
`python3 scripts/check_lessons_register.py` prints the fundamental and price-engine
counts, `python3 scripts/check_tech_calibration.py` the technical record's — and never
from this document, because a written count of how many names have been through any of
the tests drifts the moment one more runs, exactly as the stale-library list did.

### When it runs

FUNDAMENTAL CALIBRATION IS A STANDING STEP OF EVERY NEW STUDY AND EVERY UPDATE, on the
same footing as Step 0.0 and the Step 2A sweep. The canonical prompt is
`engine/Fundamental_Walkforward_Prompt.md`; it is the operative text and this section
is the reasoning behind it.

**Scope is decided FIRST and stated in the study**, because the honest scope depends on
what the archive supports and a run that quietly shrinks is a run nobody can weigh:

- **FULL** where at least 8 fiscal years are sourceable under the data rule below: every
  origin from the first year with five years of history, horizons 1–5.
- **LIGHT** at 5–7 years: the last five origins, horizons 1–3, every other rule unchanged.
- **SKIP** below 5 years: record *"walk-forward not run — insufficient sourceable history
  (N years)"* in the study's register and its QC table, in those words.

**NEVER DELAY A FIRST DELIVERY FOR IT.** On a new study the training runs alongside the
build and its corrections feed the next edition; the first edition carries a one-line
note that the training is pending or running. On an update it is a standing step.

**INCREMENTAL THEREAFTER.** Each update adds one origin, grades the forecasts that have
matured, and re-tests the corrections. The full rebuild happens once per name.

**TWO PURPOSES, NOT THREE.** The training exists for per-driver bias detection and for
calibrated ranges on years three to five. A better point estimate is a by-product and
never the aim — TUNING TOWARD ONE IS THE CRPS-SELECTION MISTAKE IN A NEW COSTUME, and
the PROMOTION RULE forbids it.

### Data — the same source discipline as any study, plus one gate

Target 15 complete fiscal years of IS, BS, CF and operating KPIs, plus every disclosed
quarter of the current year. **THE MOST RECENT THREE FISCAL YEARS AND ALL CURRENT-YEAR
QUARTERS MUST COME FROM THE COMPANY'S OWN AUDITED STATEMENTS OR ITS OWN IR DOCUMENTS**
— no exception; if they cannot be obtained, STOP AND ASK, exactly as SIGCM clause 1
requires of any study. Older years may come from any credible source that supports a
DCF, the company's own documents preferred.

Four fields on every number (value, source, date, tier A/B/C). **NEVER ESTIMATE,
INTERPOLATE OR INFER A FIGURE TO FILL A GAP** — leave the year out and shorten the
window, because a fabricated cell corrupts the very error it is being scored on.

**ACCEPT A STATEMENT ONLY IF IT FOOTS AGAINST ITS OWN ARITHMETIC.** Fonts with a broken
character map extract figures that look perfectly clean and are wrong: one PHDC filing
renders revenue of 3,560,584,644 while its text layer yields 1,654,670,500 — right
positions, wrong glyphs, and nothing about the extraction looks broken. Every statement
is therefore accepted only if it foots; a page that does not foot is re-read by OCR off
the rendered pixels, and the route each figure came by is recorded. ARITHMETIC IS THE
ARBITER, NOT THE EXTRACTOR'S CONFIDENCE.

A basis-break register precedes the modelling (standards changes, segment re-cuts, KPI
redefinitions, FX-regime changes, attributed one-offs), with the overlap year, chain
factor and treatment for each; unit drivers are scored only inside their own definition
window. POINT-IN-TIME DISCIPLINE IS ABSOLUTE: each origin sees only what had been
published by that date, as originally reported, and later restatements are noted beside
it rather than substituted for it.

### Pre-registration — before a single error is computed

Written down in advance: origins, horizons, the driver list by class, the MECHANICAL
rule for each driver with its parameters, the naive benchmarks (freeze = every line flat
at last actual; trend = trailing three-year CAGR), the score, the block bootstrap over
origins, the macro/regulatory conditioning and how the error is split into macro versus
company, and the roles of the two samples. **NO JUDGEMENT DRIVERS AT HISTORICAL
ORIGINS** — the exercise tests the method, not the analyst, and a driver the analyst
would have set by hand cannot be scored. Parameters are stated, never fitted;
sensitivities are reported, never selected.

**BEFORE WRITING THE PRE-REGISTRATION, READ WHAT ALREADY BINDS ON THE NAME AND ITS
CLASS**: `python3 engine/lessons.py {TICKER} --class {CLASS}` per [R-LESSON-01].

### Building at every origin — two traps this project has already fallen into

The build is the ordinary ground-up construction of SIGCM clause 2, run at a past date.
Two specific errors are called out because each produced a large, robust, entirely
spurious bias:

**INTEREST COMES FROM THE BORROWINGS THAT ACTUALLY BEAR IT.** Dividing the finance
charge by a broader liabilities total — customer deposits, supplier balances, cheques
under collection, none of which pay interest — understates the borrowing rate by a
multiple. On PHDC the denominator was 4.4x too big (EGP 105,099mn against EGP 24,069mn),
implying a 3.19% borrowing rate for a company that borrows at 13.91%, and it produced a
finance-cost bias of −1.074 log that looked exactly like evidence.

**REVENUE AND COST MUST SIT ON THE SAME RECOGNITION CLOCK.** Where revenue is recognised
as work completes, cost must be too. On PHDC, revenue accrued with construction while
cost accrued with handover, and the two clocks produced a gross-profit bias of +0.540
log — over-forecast in 86% of cells — which operating leverage on a thin residual turned
into a net-profit bias of +1.116, about three times too high, in 97% of cells, WORSE
THAN FREEZING LAST YEAR'S NUMBER AT EVERY ONE OF THE FIVE HORIZONS. THAT IS A
SPECIFICATION ERROR, NOT A CALIBRATION ONE, and no correction factor may be allowed to
hide it.

### Scoring, and what the numbers are allowed to mean

Per driver and per horizon: bias, MAE, block-bootstrap CI, share of origins over- and
under-forecast, sign by era. The revenue and net-profit errors are decomposed into their
drivers. Each miss is split into macro/regulatory versus company by re-running every
origin twice — once on the inflation path knowable there, once with perfect foresight.
Every one-off is identified and the record shown with it classified. The
projected-versus-actual income statement is shown side by side for every origin. Skill
is reported against BOTH naive benchmarks at every horizon.

**A METHOD THAT CANNOT BEAT "NO CHANGE" HAS NOT EARNED THE PRECISION IT DISPLAYS.** That
is not a figure of speech: on PHDC the net-profit build lost to freezing last year's
number at all five horizons and to the trend line at four of five, and the study says so.

**A BIAS THAT CHANGES SIGN BETWEEN ERAS IS NOT A BIAS.** Report the instability; do not
correct for it. The average of two opposite regimes is a number that was never true in
either.

**THE MACRO SPLIT IS THE CHECK THAT THE DECOMPOSITION MEASURES WHAT IT CLAIMS**: volume
drivers carry no inflation term and must come back at a zero macro share by
construction. On PHDC, across four devaluations, macro explained 21.5% of the revenue
error and 3.9% of the net-profit error — so the currency was not the story, and the
decomposition earned the right to say so.

### Corrections — the two-clause promotion test, and why the second clause exists

Expanding window only. Corrections at HALF STRENGTH by default, applied only where the
bias holds its sign across eras, reset after a structural break. Aggregates are rebuilt
from adjusted drivers and tested adjusted-against-raw on the origins that carried a
correction, reported by origin.

**A CORRECTION ENTERS THE LIVE DRIVERS ONLY IF IT PASSES ITS OWN TEST *AND* IS
CONSISTENT WITH HOW THAT DRIVER CLASS IS BUILT ACROSS THE MARKET'S BOOK.** Otherwise it
is a WATCH FLAG — recorded, graded live, revisited at every refit, acted on by nobody.

THE SECOND CLAUSE IS NOT A FORMALITY, AND IT HAS ALREADY DONE ITS JOB. PHDC's
finance-cost correction passed the first test convincingly — half strength, MAE 0.848 →
0.403. It failed the second, because every other Egyptian study builds interest from a
named facility-by-facility schedule, and that failure is what exposed the wrong
denominator described above. THE "BIAS" WAS ARITHMETIC, NOT EVIDENCE. Adopting the
correction would have produced roughly the right answer today while leaving a broken
model in place to fail differently tomorrow.

**THE GENERAL RULE: A CORRECTION FACTOR IS HONEST WHEN THE MODEL IS RIGHT AND REALITY IS
AWKWARD. WHEN THE MODEL IS WRONG, A CORRECTION HIDES IT.** A number out of line with the
rest of the book usually means our own method slipped on this one name, not that the
company is unusual — and asking which is the only way to tell them apart.

**GUIDANCE IS SCORED AND NEVER CONSUMED.** Management's forward targets lean the same
way an optimistic model does: on the only two PHDC targets gradable BEFORE the outcome,
handovers were over-forecast by +0.220 log, while every target quoted retrospectively
had been beaten. A driver that takes guidance as an input inherits the lean instead of
correcting for it.

### What a run must produce — two documents, and neither is optional

**DOCUMENT 1 — THE UPDATED FUNDAMENTAL ANALYSIS**, at full model-report depth: the
16-section Word document, the 16-sheet workbook, the standalone bibliography and the QC
gate, exactly as the MODEL REPORT section requires. It carries the corrections that
passed, and it publishes YEARS THREE TO FIVE AS RANGES built from this record's own
driver-error distribution, never as points. On PHDC the measured five-year spread on
revenue ran 83,620 to 214,090 EGP mn on five resolved observations, and a single figure
would have implied a precision ten origins cannot support.

**DOCUMENT 2 — THE UPDATED LESSONS-LEARNT DOCUMENT**, per [R-LESSON-01].

A run that produces one and not the other is NOT FINISHED. The training record, the
panel, the error tables and the pre-registration are INTERNAL and never shown to a
reader; the two documents above are the deliverables. Nothing reaches the live site
without a separate explicit publish request.

### The honest limits, stated in the rule rather than discovered later

**THIS METHOD IS NOT YET VALIDATED, AND THE PROTOCOL SAYS SO.** As at adoption, one
company had been through a full fundamental run. That run's own record states its
corrections rest on two origins, its bootstrap intervals are wide with several
straddling zero, and its cells are not independent because the horizons overlap.

THE PROMOTION RULE THEREFORE APPLIES TO THIS RULE'S OWN OUTPUT. What is adopted here is
the PROCESS — a standing step, with a stated scope decision, a fixed pre-registration
and two required documents. What is NOT adopted is any particular finding as a house
rule: every lesson a fundamental run produces is PROVISIONAL under [R-LESSON-01] until
the method has been validated across more names. **A FINDING MEASURED ON ONE NAME HAS
NOT SURVIVED THE OUT-OF-SAMPLE TEST THE FORECASTS MUST SURVIVE**, and this project does
not exempt itself from its own bar.

### Enforced from outside, per [R-ENF-01]

The register gate (`scripts/check_lessons_register.py`, in CI) fails when a fundamental
run exists on disk with no lesson behind it, or when a harvested finding was never ruled
on. The study gates (`scripts/check_study_provenance.py`) are unchanged and still bind
the study this run feeds. THE POPULATION IS ANCHORED OFF THE RUN DIRECTORIES ON DISK per
[R-ENF-04], so a register that has stopped being fed FAILS rather than reporting clean.


### [R-FCAL-01 AMENDED] A run also commits the inputs a VALUE is rebuilt from, not only the drivers (3-Sep-2026, method reassessment WS6)

**A DRIVER PANEL IS NOT A RECORD A VALUE CAN BE REBUILT FROM, AND THE DIFFERENCE WAS
INVISIBLE UNTIL SOMETHING TRIED.** [R-VCAL-01] grades the fair value itself against
what happened, and its series (a) rebuilds one at every past origin from what these
runs commit. Twice a construction was declared for it and twice the binding
constraint turned out to be the same one, asked too late: **the input was not
committed.** A cash-flow lens needs capital expenditure and working capital; the
enterprise-to-equity bridge needs cash and debt; a value cannot meet a price without
a share count. The lens was being chosen by what happened to be in the repository.

MEASURED RATHER THAN ARGUED (`engine/valuation_calibration/bridge_inputs.py`, which
reads each run's OWN committed artefacts and names the file that carries each item):
across the five names then run, **NOT ONE origin carried a complete bridge and a
capital-expenditure figure**; three carried a bridge where capex was derivable by the
identity capex = ΔPPE + D&A; five more carried a bridge and no route to capex at all.
Eight cells, two names, both of one class. Read the census live — never from a
document, this one included.

**WHAT RULES OUT AN INSTRUMENT BUILT ON WHAT HAPPENS TO BE PRESENT IS THE DIRECTION OF
WHAT IS MISSING, NOT THE COUNT.** Each omission has a known sign and they do not agree:
no cash UNDERSTATES equity value, no capex OVERSTATES it, working capital does either
depending on growth. So the bias varies cell by cell in unknown direction and unknown
magnitude — which is worse than a large bias, because a floor at least tells you which
way it points and this cannot be corrected, disclosed as a direction, or reasoned
around. Where such a bias runs the same way as the hypothesis under test, the
instrument confirms it BY CONSTRUCTION. On a net-cash company the omitted cash is not
a rounding error, it is most of the answer.

**THE RULE.** Every fundamental walk-forward commits a VALUATION-INPUT BLOCK beside its
driver panel, per origin, from the same statements the drivers were built on and under
the same point-in-time discipline: **cash and equivalents · interest-bearing debt ·
property, plant and equipment · depreciation and amortisation · the working-capital
lines · the share count with the par value it was footed against.** Capital expenditure
is committed where the cash-flow statement discloses it and is otherwise DERIVED by the
identity above and labelled as derived — an identity is not an assumption, and the
label is what keeps the two apart.

**FOUR CLAUSES RIDE WITH IT.**
- **A MISSING ITEM IS RECORDED AS MISSING, NEVER OMITTED.** A line the filings do not
  disclose is named with the reason, exactly as SIGCM clause 8 already requires of a
  driver — because a block that quietly carries five of six reads as complete.
- **THE SHARE COUNT IS FOOTED OR IT IS NOT RECORDED.** Issued capital divided by par
  must reproduce the count the same document states. Today's count is never carried
  back to a past origin: counts change on capital increases, and a carried count is
  fabricated in vintage, plausible on the page, and invisible in the pooled error
  afterwards. Where the note is a CHRONOLOGY of resolutions rather than a single
  current-capital sentence, the recital establishes the par value and the identity,
  and the count is that year's own committed capital divided by that par — the recital
  stops at the last resolution that CHANGED the capital and cannot see a later treasury
  movement.
- **THE ROUTE IS RECORDED.** Text layer or OCR, page and file, on the same footing as
  the four-field rule for a driver. Arithmetic remains the arbiter for both routes.
- **IT BINDS FORWARD, NOT BACKWARD.** Runs completed before this amendment are not
  re-opened for it; they are listed as outstanding and the block is added at each name's
  next run. A ratchet, per [R-ENF-02] — a rule that made every existing run red would be
  the permanently-red check that rule forbids.

**WHY IT IS WORTH THE COST, WHICH IS SMALL.** Every one of these items sits on a balance
sheet or cash-flow statement in filings the run has already opened and parsed cell by
cell; carrying them out is a copy, not new research. Not carrying them is not a gap in
a table — it is that **no valuation this house makes can ever be rebuilt at a past
origin**, and that loss is PERMANENT for any year whose filings are no longer to hand.

**THE GENERAL LESSON, WHICH IS NOT ABOUT VALUATION: WHAT A PROCESS COMMITS DECIDES WHAT
CAN EVER BE ASKED OF IT LATER, AND NOBODY NOTICES THE MISSING FIELD UNTIL THE QUESTION
ARRIVES.** The five runs were correct, careful and well evidenced; they simply answered
the question they were built for and left no trace of the figures beside it. When a
record is designed, the cheap discipline is to ask what a LATER question would need —
because a figure not written down at the time is not merely inconvenient afterwards, it
is gone.


## [R-LESSON-01] Every lesson is registered, explained plainly, and scoped (31-Aug-2026, per instruction — "I want lessons learnt from all the walk forward fundamental training from all stocks to be kept in a register, explained simply and then categorized")

A LESSON IS USELESS UNTIL YOU KNOW HOW FAR IT CARRIES. Findings had been accumulating in
three places with no scope on any of them — the standing protocol (implicitly "every
study, always"), each study's own critique response and self-audit (implicitly "this
study, once"), and the Fundamental Driver Ledger (meant to be "the next company of this
class") — so the universal ones were applied and the rest were lost.

THE REGISTER IS `engine/Lessons_Register.md` AND `engine/Lessons_Register.docx`,
GENERATED from `engine/lessons_register.py` and NEVER hand-edited. A document that
states a fact which moves must not be the thing that remembers it — the same rule the
as-of stamps and the band records already obey.

**THREE SCOPES, NOT INTERCHANGEABLE.** ALL — method, arithmetic, or how work is checked;
binds on every study ever run. CLASS — true of every company that works the same way;
the next study of that class must read them and a study of a different class must not,
because a rule true of developers is not evidence about airlines. STOCK — true of one
company and nothing else; APPLYING A STOCK LESSON TO ANOTHER COMPANY IS SUPERSTITION.

**CHOOSING THE SCOPE IS THE JUDGEMENT AND IT IS COSTLY IN BOTH DIRECTIONS**: too narrow
and the next study repeats the mistake, too broad and one company's quirk becomes a
house rule nobody can dislodge. WHEN UNSURE, FILE AT THE NARROWER SCOPE AND WIDEN WHEN A
SECOND COMPANY SHOWS THE SAME THING — one observation is not a pattern.

**EVERY LESSON RECORDS HOW IT WAS LEARNED**, because the evidence differs enormously in
strength: a fundamental walk-forward, a price-engine walk-forward, an outside critique, a
self-audit, or a defect found while building. WHERE TWO DISAGREE THE WALK-FORWARD ONE
WINS, and the register says which is which rather than presenting them as equals.

**EVERY LESSON CARRIES WHAT WOULD OVERTURN IT.** A lesson with no falsifier is a habit,
not a finding, and habits are how a house method quietly stops being tested. The field is
required and may not be empty.

**FUNDAMENTAL WALK-FORWARD LESSONS ARE PROVISIONAL** while [R-FCAL-01]'s method rests on
too few names to be called validated — the code refuses to write one as adopted.
Price-engine lessons are not, because their evidence base is broad. THE REGISTER IS A
RECORD AND NOT A GATE: no QC item consults it, and a provisional lesson is read, never
cited as authority.

**THE LOOP IS AUTOMATED UP TO THE JUDGEMENT AND STOPS THERE ON PURPOSE.**
`engine/lessons_harvest.py` reads a run's OWN committed outputs and drafts every
candidate lesson those numbers support, with the evidence clause filled in from the
measured figures — nothing in a "how we know" clause is typed by hand, so it cannot
drift from what the run measured. Its selection rules are fixed in the module AHEAD of
any run, so they cannot be tuned after seeing a particular run's numbers. Every draft is
emitted UNSCOPED with `confirmed: false`, and `engine/lessons_add.py` refuses anything
unconfirmed, anything scoped to an unregistered class, and anything with no falsifier.
THE EVIDENCE IS MECHANICAL; THE JUDGEMENT IS SIGNED.

**NOTHING IS SILENTLY DROPPED.** Every harvested draft ends `registered: "L-nnn"` or
`declined: "<reason>"`. A candidate nobody ruled on is an unanswered question wearing the
costume of a clean result, which is [R-ENF-04] applied here.

READ IT ON DEMAND: `python3 engine/lessons.py [TICKER] [--class X]` returns exactly the
set that binds on the name in hand. ENFORCED FROM OUTSIDE per [R-ENF-01] by
`scripts/check_lessons_register.py`, negative-controlled, both in CI.


## [R-TCAL-01] TECHNICAL CALIBRATION — the technical read is walk-forward tested on its own clock, sentence by sentence, against a null that could have been believed instead (31-Aug-2026, per instruction — "It is time now to add the walk forward technical training to the research protocol and the standing instructions")

### The third test called a walk-forward

[R-FCAL-01] opens by separating the two tests this system called a walk-forward. This
rule adds the third, and the disambiguation in [R-FCAL-01] is amended to count it:

**PRICE-ENGINE CALIBRATION [R-CAL-01 … R-CAL-03]** tests the Monte Carlo cone — band
coverage against a stated target.

**FUNDAMENTAL CALIBRATION [R-FCAL-01]** tests the forecasting method — rebuild the
driver model at a past origin, score each driver against what the company reported.

**TECHNICAL CALIBRATION [R-TCAL-01], this rule** tests the TECHNICAL READ — replay the
shipped read at every historical origin and grade each templated sentence it emits
against what price then did. Its evidence base is the broadest of the three, because
every OHLC library supplies hundreds of weekly origins: at adoption the harvest replayed
the read across the full book of libraries and 89,190 graded claims spanning 2011–2026,
and the register itself rests on 45,331 tape readings across 85 names — figures that
grow with every posting, so READ THE POPULATIONS LIVE:
`python3 scripts/check_tech_calibration.py` prints the current record's counts, and
never quote them from this document.

The three tests share one bar (the block bootstrap over {2,3,4}, LONO, split-half — the
same robustness battery everything else must survive) and none substitutes for another.
NEVER write "the walk-forward" without saying which.

### The clock is the lens's own — grading on another lens's clock understates every claim

In this project the technical read is the UNDER-ONE-MONTH lens: the fundamental study
owns the year, the cone owns one to three months, and the chart read owns the weeks
(per instruction, 31-Aug-2026 — "we use technical analysis for less than 1 month price
monitoring"). THE CALIBRATION IS THEREFORE SCORED AT 5, 10 AND 21 SESSIONS AHEAD, on
weekly origins, and every record and result carries the horizon it was measured at.

This was learned by doing it wrong first: the first edition graded every claim at three
calendar months — the cone's exam, not the chart's — and the published level edge
measured +3.4pp there against +9.8pp at one week, so the wrong clock reported the
weakest available reading of every sentence and one wrong conclusion (that per-name
level records were merely data-starved) was drawn from it before the mistake was
caught. A LENS IS GRADED OVER THE HORIZON IT IS USED FOR. The general form is already
in this protocol — the band record prints its count beside its percentage because a
number without its basis misleads — and the horizon is part of the basis.

### The shipped read is replayed, never re-implemented

The harvest (`engine/lab/ta_calibration/replay.py`) calls the production module's own
`technicals.compute(frame=...)` at each origin, on the same cleaned series the pages
are built from, through the same Step 0.0 gate. NO RE-IMPLEMENTATION, EVER: a
re-implementation is graded instead of the read, and the two drift — the same species
as [R-ENF-03]'s checker that modelled the parser and checked a different file from the
one that shipped. The read itself has no fitted parameter, so the PROMOTION RULE's
out-of-sample test does not bind on the read — but it binds in full on anything this
calibration might promote INTO the read or the engine, and on the calibration's own
findings (below).

### The null is the whole point — every level is raced against a placebo that could have been believed

"Price stopped at support" is unfalsifiable until you say how often price stops at a
line that means nothing. EVERY LEVEL CLAIM IS THEREFORE SCORED AGAINST A DISTANCE-
MATCHED, NON-STRUCTURAL PLACEBO: an invented price the same distance from spot, placed
where the chart shows no structure at all, and the claim earns only the DIFFERENCE.

THE PLACEBO IS DRAWN TWO-SIDED BY CONSTRUCTION — an inner and an outer candidate
straddling the real level's distance, both clear of all published structure by the
module's own cluster tolerance — because the first cut searched inward first and drew
placebos 1.4% to 4.3% NEARER than the levels they stood in for, and a nearer price is
touched more and broken more for reasons of arithmetic, not structure. That offset was
enough on its own to manufacture "support holds". A trigger's two-rung ladder is
placebo'd the same way, both rungs scaled together, so the null preserves the
geometry of the claim. THE GENERAL RULE: A BENCHMARK MUST BE MATCHED ON EVERYTHING
EXCEPT THE THING CLAIMED, and an unmatched benchmark does not weaken the test — it
reverses it, producing confident evidence for whichever side the mismatch favours.

And every directional claim is measured against ITS OWN MARKET'S BASE RATE, never
against 50%: over a month the coin is tilted, by different amounts in different
markets, and a "signal" credited against a fair coin inherits the tilt as fake skill.

### Three scopes, and the guard the narrowest one must pass

Findings are scored at the same three scopes as [R-LESSON-01]'s register, per the
adopting instruction ("learning per stock, per asset class (if that is a thing) and
across all tickers"):

- **EVERY TICKER** — the pooled book, under the house bar.
- **A CLASS OF TICKER** — and A SET OF PER-CLASS NUMBERS IS NOT A CLASS FINDING: the
  classes must genuinely DIFFER, tested by Cochran's Q with I² beside it, or the
  finding is the pooled one wearing subscripts. At adoption the exchange was a real
  class — on the level test Q returned p=0.008 at one week with I² 79%, Saudi roughly
  doubling Egypt — while sector splits mostly dissolved once the venue was accounted
  for. THE VENUE (price limits, liquidity, the trading week) IS THE CLASS THAT EARNS
  ITS KEEP ON CHARTS; the industry mostly does not, which is the reverse of the
  fundamental register's taxonomy, and each register uses its own.
- **ONE TICKER ONLY** — the highest bar in the calibration, guarded by the SYMMETRIC-
  SPLIT TEST: single names clear significance by chance, so a per-name claim exists
  only if the names clearing it lean overwhelmingly ONE way (a sign test on earned
  versus reversed). The precedent is the withdrawn per-name trend claim: the first
  edition named the tickers the stack sentence "works on"; on the correct clock the
  split came back 13 earned against 12 reversed (p = 1.00) — more significance than
  chance produces, pointing both ways, WHICH IS PER-NAME HETEROGENEITY, NOT A PER-NAME
  CLAIM. The clause was withdrawn, the record prints the sign test at every rebuild,
  and the pooled finding (+3.2pp at adoption) belongs to every ticker or to none.

A claim can also be UN-EARNABLE at a scope for reasons of arithmetic, and the record
says so rather than waiting for data that cannot arrive: a per-name LEVEL record needs
roughly 560 paired observations to resolve a 3–4pp edge, fifteen years of weekly
origins yield a median of 62 per name (best name 239), and denser origins do not help
because the windows overlap. A FIGURE THAT CANNOT SEPARATE AN HONEST READ FROM A
BROKEN ONE IS NOT PUBLISHED AT THAT SCOPE.

### What the calibration may change, and what it may never touch

THE CALIBRATION GRADES THE READ'S SENTENCES AND CORRECTS THEIR WORDING; IT FEEDS
NOTHING INTO THE OTHER LENSES. [R-LENS-01] stands in full: no finding here becomes an
MC drift signal (technical-family constructions remain ineligible there even where
they test well), no fair value is touched, and this rule creates no promotion path
around that independence. A finding that would change the ENGINE goes through the
promotion rule like anything else.

What it has already changed — four corrections adopted 31-Aug-2026, shipped through
the normal regeneration pass and live on every page:

1. RSI words: "stretched" and "washed out" whisper reversal, and both were followed by
   the OPPOSITE — strong kept going, weak kept sliding. Replaced with "very strong" /
   "very weak". THE CAUTIOUS-SOUNDING WORD WAS THE ONE POINTING BACKWARDS, which is
   [R-CAL-02]'s lesson again: conservative-sounding language is audited like a claim,
   because it is one.
2. The far-zone promise ("a close above resistance opens the next zone") measured
   BACKWARDS — clearing a real level makes the far target LESS likely than clearing a
   placebo, because the far level is real too and holds against the approach. The
   sentence now reports the crossing and names the next charted level, promising
   nothing about it.
3. The fresh-cross drama ("a momentum-regime change rather than noise") measured as
   noise: a fresh golden cross is followed by slightly worse months than a stale one,
   a fresh death cross by slightly better, and volatility does not shift. The read
   still reports the cross; the regime clause is deleted.
4. The retired skill-verdict emitter was removed from the roll-forward path entirely
   ([R-CAL-03] applied at the source rather than filtered downstream).

THE STANDING RULE THESE FOUR INSTANTIATE: A TEMPLATED CLAUSE IS A CLAIM AND IS
CALIBRATED LIKE ONE. Every sentence the read emits is either measured, or worded to
promise nothing unmeasured. A clause added to the read after this rule adopts arrives
with its measurement or arrives hedged.

### The per-name record — the band record's analogue for this lens

`engine/tech_record.py` builds `engine/tech_records.json`: per name, per horizon, what
that name's own history has EARNED the right to say. What it may and may not say is
settled by measurement, recorded in the module's own header — the tape sentence is
per-name (the one claim that survives that bar: significantly positive on 84 of 92
names at one week, 87 at one month, against 1 and 2 significantly negative), the trend
sentence is pooled-only (the symmetric split above), and levels are never per-name
(the arithmetic above). It is keyed on (market, ticker) because ticker strings collide
across markets, counted against the libraries on disk per [R-ENF-04], and REGENERATED
IN THE SAME PASS AS ANY CHANGE TO THE READ — the record stores the sha256 of the
`technicals.py` it graded, so "the read moved but its record did not" is a checkable
condition in CI, not a remembered one.

IT RENDERS NOWHERE UNTIL INSTRUCTED — the same disposition as CALIB under [R-REC-01]:
generated, committed, regenerated, consulted when investigating the read, and shown to
a reader only on an explicit instruction that has not been given.

### The register — every finding in plain words, scoped, drawn, and never typed

The findings live in the TECHNICAL LESSONS REGISTER
(`engine/lab/ta_calibration/Technical_Lessons_Register.docx`, lessons T-01 through
T-27 at adoption), the sibling of [R-LESSON-01]'s register and built to the same
discipline: three scopes, plain language, every lesson carrying what would overturn
it, and EVERY NUMBER RESOLVED FROM THE COMMITTED RESULTS FILES AT BUILD TIME
(`lessons_source.py` → `build_register.py` → `build_register.js`) — a lesson whose
evidence disappears from those files fails the build rather than printing a stale
figure. Real named tickers demonstrate every demonstrable finding, because a lesson a
reader cannot see happening on a chart is a lesson half-taught.

THE TWO REGISTERS STAY SEPARATE ON PURPOSE. [R-LESSON-01]'s register is append-only
judgement — a human scopes each lesson and signs it. This one is REGENERATED WHOLESALE
from the panels at every rebuild, figures included, so hand-appending to it would be
hand-editing a generated file. A technical finding that generalises beyond the lens
(about method, arithmetic, or how work is checked) is additionally filed to
[R-LESSON-01]'s register through the ordinary harvest-and-judge path, and the two
cross-reference rather than duplicate.

STATUS VOCABULARY, deliberately its own: **ACTED ON** (the finding changed the shipped
read — the four corrections above), **WATCH** (real in aggregate but failed a
durability guard — at adoption the stack-sentence lean, which held before 2020 and has
not since, and the sector taxonomy; recorded, re-tested at every rebuild, acted on by
nobody), **PROVISIONAL** (measured and robust, standing as a finding, consulted but
binding nowhere). PROVISIONAL here is the register's own caution about acting, not
[R-FCAL-01]'s one-name caveat — this calibration's evidence base is broad — and the
path from any status to a change in the read or the engine runs through the promotion
rule, never through the register.

### When it re-runs

- **MANDATORY, in the same pass, whenever `engine/technicals.py` changes** in any way
  that could move a computed value or an emitted clause: re-harvest, rebuild
  `tech_records.json`, rebuild the register. The stored hash makes skipping this
  visible in CI. This is the 29-Jul-2026 rule one layer up — the read moves with its
  library; the record moves with its read.
- **On instruction, as libraries lengthen.** Staleness of the calibration against
  freshly posted data is a data-supply fact like library staleness — reported by the
  live population print, never silently "fixed", and not a gate, because a gate nobody
  in the room can clear is one everybody learns to ignore.
- The harvest cache (`claims_short.pkl`) is a regenerable convenience, never
  committed; the committed evidence is the RESULTS files, the record, and the payload.

### Enforced from outside, per [R-ENF-01]

`scripts/check_tech_calibration.py`, in CI beside the lessons-register gate, fails —
never warns — when: the record grades a `technicals.py` that is no longer the one on
disk; the population does not anchor to the OHLC libraries per [R-ENF-04] (including a
HALF-LOST record — one horizon missing while the name survives — which this checker's
own negative control caught it missing on its first run); the register payload is not
byte-identical to its generator's output; or the delivered document cites a lesson id
that resolves to nothing. That last check caught a real defect the day it was written:
the 31-Aug-2026 renumbering mapped every id in the sources it knew about and missed
one in `build_register.py`, so the delivered document told readers volume was "scored
in T-013" — an id that no longer existed. `scripts/check_tech_calibration_negative_control.py`
injects all four defects and fails if any is missed.

### The honest limits, stated here rather than discovered later

Everything this calibration found is a LEAN, NOT A SIGNAL: the largest robust edge in
the book at adoption was under ten points in a hundred at one week, most are three to
five, and every one is quoted against its own market's tilted coin. The register says
so in its own voice ("anyone offering +40 in 100 is selling something"). Nothing here
is a trading rule, nothing here changes what a reader is promised — it changes what
the read is allowed to CLAIM, which is the direction the errors actually ran. What
remains untested is listed in the register rather than implied absent: intraday
structure, and level-drawing methods other than the module's own.


## [R-CAL-02] The band record replaces PASS / PARITY / FAIL on every public surface (24-Aug-2026, per instruction — "I want to challenge the concept of pass, parity or fail for the MC. Too complicated and the investor would not necessarily understand it")

The challenge was made on legibility. It is upheld on legibility and on a second ground
that turned out to be worse: **the label was factually wrong about the names it flagged.**


**Render settled, 25-Aug-2026, under the R-CAL-03 precedent: CALIB is an internal diagnostic and
does not reach a reader.** [R-REC-01] and [R-CAL-02] were adopted on the SAME DAY on two branches
that never saw each other, and were merged for the first time on 25-Aug-2026. They do not measure
the same thing. `BANDS` (band_record.py) scores the bands as they were actually PUBLISHED; `CALIB`
(build_name_calibration.py) re-scores the same windows under TODAY's fit — `cal * tq(.25, nu) <= u
<= cal * tq(.75, nu)`. Window counts agree on every name; 70 of 88 disagree on cov50 or cov90 (DU
71% vs 66%, AIRARABIA 57% vs 47%), and regenerating both from the merged fits does NOT converge
them — both blocks came back byte-identical — so the difference is definitional, not staleness.

**The protocol already decided this, and it was not read closely enough the first time.** R-CAL-02
enumerates what a reader is shown on every public surface — the band record, record strength, and a
flag only when earned — and that list is exhaustive. It is also already PER-NAME, which is
R-REC-01's own stated purpose: "stop looking at stocks in a country as a bulk; look at each stock
individually." R-REC-01's requirement is therefore already met by what is published; what it
additionally proposed was a SECOND rendering of the same fact on a different sample.

R-CAL-03 then set the disposition for exactly this shape of thing — a second measure that is real
and worth keeping but must not reach a reader: CRPS "stays in the codebase as an internal
DIAGNOSTIC ... but the diagnostic may never again gate, trigger, block, or reach a reader." CALIB
takes the same disposition. It stays generated, committed and regenerated in every pass, because it
answers a question the band record genuinely cannot — how would today's cone have done on this
name's own history — and that is a fair thing to consult when investigating a fit change. It
renders nowhere.

Publishing both would state one page's record twice, in two numbers, with nothing on the page
saying which sample each came from. That is the defect R-CAL-02 exists to close, in its own words:
"the original defect was not the sample but that nothing said which sample it was." It is also the
defect a reader reported on a ticker page the same week. Reversible on an instruction — one
commented call in `assets/app.js`. No research method changes and no delivered number moves.

### What the verdict actually was

PASS / PARITY / FAIL is the outcome of a SKILL test. A name's cone is scored against a
carry-anchored random walk on a scale-normalised proper score, the difference is
bootstrapped, and the verdict reports whether that interval clears zero. It answers a
modelling question — *is our score better than a naive alternative's?* — and it answers it
well. It is not, and never was, a test of whether the published bands hold.

The site nonetheless labelled the negative outcome **"⚠ INDICATIVE ONLY · FAILED
CALIBRATION TEST"**.

### The measurement that settles it

Taken on the live panels on 24-Aug-2026, across the whole 93-name book. Every name then
carrying the FAIL label, with its own 90%-band coverage against a 90% target:

| Name | resolved 3-month windows | inside the 90% band |
|---|---|---|
| ADNOCDRILL | 15 | 100.0% |
| ADNOCDIST | 30 | 100.0% |
| BOROUGE | 12 | 100.0% |
| EMPOWER | 10 | 100.0% |
| CLHO | 36 | 97.2% |

Not one of them was mis-calibrated in the direction the label implies. Every one contained
*more* outcomes than it advertised: their bands were too WIDE, the opposite failure and a
far more benign one. And the five names whose bands genuinely ran NARROW — ISPH 76.7%,
EMAAR 78.9%, RIBL 78.9%, IHC 80.9%, TMPV 81.0%, each significant at p < 0.05 — carried no
flag at all. The scheme warned about cones that contained everything and stayed silent on
cones that missed more often than they promised. It was pointing at the wrong names.

This was not unknown. The adaptive-width entry above already records that both robust FAILs
at the time it was written failed for exactly this reason (LGES: cov80 = cov90 = 1.00,
PIT 0.471, perfectly centred). The fact was in the protocol; the label on the page was
never reconciled with it. That is the [R-ENF-01] species of defect — a rule known and
written down, with nothing looking at the surface it governed.

### What is published instead

Two facts a reader can check on the ledger, and a flag only when it is earned.

1. **THE BAND RECORD.** "Over N resolved three-month forecasts, the price finished inside
   the 90% band X% of the time." No benchmark, no significance test, no vocabulary to
   learn. The count is printed beside the percentage every time — a percentage without its
   count is precisely the number that misleads.
2. **RECORD STRENGTH** — long / short / market-only, from the resolved-window count.
3. **A FLAG ONLY WHEN EARNED** — *bands ran narrow* or *bands ran wide*, when the name's own
   coverage sits outside a two-sided binomial test against the 90% target at the 5% level.
   Otherwise nothing is said. The ordinary case is a cone whose bands held about as often as
   promised, and **silence is the honest response to it.** A verdict token on every name
   made the ordinary case look like a judgement.

The strength thresholds are DERIVED, not chosen round, and two independent readings agree
on them. By POWER: a name's own coverage figure is worth printing only if it could catch a
badly miscalibrated cone, and testing a claimed 90% against a true 75% at the 5% level,
power reaches the conventional 90% bar at n = 40 (n = 30: 80%; n = 22: 68%; n = 16: 60%);
below about 22 the interval on the estimate is wider than ±10pp and cannot separate an
honest cone from a broken one. By THE BOOK'S OWN SHAPE: the window counts are not uniform —
there is an EMPTY BAND at 17–21 windows and a second gap at 31–35 — so cuts at 22 and 40
fall in real gaps and no name sits one resolved window from a boundary. MIN_WINDOWS = 28 in
adaptive_width.py is a different gate for a different job (how much own-history before a
per-name width multiplier may move off 1.0) and is deliberately NOT reused.

### What does not change

**No research method changes here.** The skill test still runs, unaltered, as the Step 0
gate; the market-panel CI is still the standing gate a name enters the book under; the
materiality rule still triggers on a verdict change; PENDING_REVIEW still records verdicts.
Not one fitted parameter, cone, drift or delivered number moves. The verdict simply stops
being something a reader is handed. Where a curious reader wants it, the methodology page
carries an expandable note explaining what is tested internally and why a wide cone can
fail a skill test without anything having gone wrong for them.

### The generator, and why the prose could not stay hand-written

A coverage figure moves the moment a forecast is graded. The old calibration prose was typed
once per page and never revisited, and it had drifted: on 24-Aug-2026 riyadhcable.html
claimed "13 non-overlapping three-month windows have resolved" with "coverage 85% / 92%"
while its own committed panel held 10 windows at 70% / 90%, and both egch.html and
scem.html carried the *same* liquidity paragraph — the 29.3% unchanged-close figure is
SCEM's; EGCH's is 5.0%, below the Egyptian median of 8.9%, so egch.html asserted a
mechanism that was not true of it. Hand-written volatile numbers rot, and a copied
paragraph rots silently in two places at once.

So the record is GENERATED and refreshed twice over: `scripts/build_band_records.py` writes
a `BANDS` block into `assets/data.js` from the committed panels, and every page's volatile
clause is marked `<span data-band-record="TK">` and rewritten in the browser by
`refreshBandRecords()` in `assets/app.js`. Static text is correct at build time; the span is
correct at render time even if a refit lands between the two. Same reasoning as the as-of
stamps: **a page that states a fact which moves must not be the thing that remembers it.**

Ledger instrument names are NOT panel filenames, and the difference bites: ADIB is a
different bank in each market — ledger `ADIB` is the Egyptian one, `ADIBUAE` the UAE one,
against panels `EG_ADIB` and `AE_ADIB`. Records are therefore keyed `(market, instrument)`
and every non-identical name is resolved through an explicit asserted `LEDGER_ALIAS`, never
inferred from a filename. The generator asserts the map is a bijection in BOTH directions —
every ledger name resolves, and no panel goes unclaimed — because a tool reporting "0
skipped" is not evidence.

### Enforcement, per [R-ENF-01]

`scripts/check_band_vocabulary.py` runs over every delivered surface FROM OUTSIDE and FAILS
rather than warns: no verdict vocabulary on any page, every published band record agreeing
with its panel, every `data-band-record` naming a real one. `PARITY` is matched
case-sensitively in caps, because lowercase "parity" is an ordinary word this book uses for
a currency peg and an export price basis — a case-insensitive ban flagged five such lines,
and a check that cries wolf is one everyone learns to ignore ([R-ENF-02]). `CRPS` is
permitted on the methodology page, where the scoring rule is being taught, and nowhere else:
naming it beside a company is the verdict wearing a different hat.
`scripts/check_band_vocabulary_negative_control.py` reinjects the 24-Aug text into throwaway
copies and asserts the gate goes red on each — a check nobody has seen fail is not evidence.

### The sample: every resolved forecast, deliberately not break-filtered

The engine's own calibration reads a panel through `panel_refresh.apply_breaks()`, which
drops windows whose origin precedes the market's last structural break (EG 2016-11 and
2022-03, SA 2015-06, AE 2022-01). That is correct for FITTING — a volatility regime that
no longer exists should not shape today's cone — and it stays exactly as it is for the
Step 0 gate, the skill verdict and every fitted parameter.

It is NOT correct for a track record. The band record answers "how often have the
published bands actually held", and every dropped window is a real forecast that really
resolved. Applying the filter would cut 58 of the 93 panels — most AE names from 58
windows to 18, most EG names from 57 to 17 — and push 69 of 93 names below the readable
threshold, so three quarters of the book would report "market record only" because of a
workweek change in January 2022. A reader asking how often our bands held is owed the
whole record, not the post-break slice of it.

So the two samples are held apart ON PURPOSE, and the choice is written down rather than
left implicit — which is the part that was genuinely wrong when this was first built: not
the sample, but that nothing said which sample it was. THE HEADLINE EVIDENCE IS UNCHANGED
EITHER WAY: all five names the site had flagged FAIL sit at 94–100% 90%-band coverage on
BOTH samples, so the defect this rule was adopted to fix does not turn on this choice.

One consequence to carry: the strength thresholds are derived from the FULL-sample window
counts. The empty band at 17–21 windows is a property of those counts and not of the
filtered ones, so anyone switching the record to the filtered sample must re-derive both
cuts rather than carrying 22 and 40 across.

### The general lesson, which is not about this label

A label is a claim, and it is checkable against the thing it claims to describe. "Failed
calibration test" was checkable against the actual calibration and had never been checked;
it survived because it *sounded* like a conservative disclosure, and conservative-sounding
language is not audited the way a flattering claim would be. **A cautious label is still a
claim about the world, and understating in the wrong direction is not a safe error — it is
the same error.** Where a rule can name what a surface asserts, the assertion is tested from
outside; where it cannot, the QC gate carries the evidence.


## [R-CAL-03] The skill verdict is RETIRED — the gate is calibration, and sharpness is disclosed (25-Aug-2026, per instruction — "whether this test is useful in the first place. Afterall, we have the test in the bands and whether or not the prediction falls into them. So why complicate matters with a test that the users and investors will not be interested in?")

[R-CAL-02] stopped PUBLISHING the PASS/PARITY/FAIL verdict. This retires it. The
challenge that produced it was sharper than the one before: not "is this the right way
to show the test" but "is the test doing any work at all, given we already measure
whether the price lands in the band". Measured against the book, it is not.

### What the evidence said

**The gate has never gated.** On the live fits, nine of the ten fitted markets print
PARITY and the tenth prints PASS; the skills span −0.8% to +1.4%. Across every verdict
ever recorded under `engine/PENDING_REVIEW/`: 213 PARITY, 94 PASS, 12 FAIL. No market has
ever been excluded by it. A test whose answer is "proceed" for everything is a ceremony,
not a gate — and the protocol was calling it "the standing gate" in both documents.

**Where it disagrees with the band record, the band record is the one that matters.**
Across the 90 names with a readable history, 36 — forty percent of the book — carry a
NEGATIVE skill number alongside coverage of 88% or better. In every one of those the
skill test says "worse than a coin-flip model" while the bands did exactly what they
promised. Only 10% of the skill number is explained by coverage and width together, so it
is measuring something independent; the question this rule answers is whether that
something is worth a reader's attention, and it is not.

**The one real job it did is done better by a number already in every panel.** Coverage
alone cannot tell an honest cone from a uselessly wide one: a band twice as wide as it
needs to be scores perfect coverage and says nothing. That is the genuine gap, and the
skill test was the only thing watching it. But `w90 / w90_b` — our 90% band over a naive
random walk's — measures exactly that, directly and legibly. RAYA's band is 2.01x a naive
one at 93% coverage; its skill number is −0.030. "Twice as wide as a simple rule" is a
sentence a reader can act on. "−3% CRPS skill" is not, and it is the same finding.

### What replaces it

**THE GATE IS CALIBRATION.** A market or name enters and stays in the book on whether its
bands hold: the realized coverage against the stated target, tested two-sided on the
binomial at the 5% level, which is the same test [R-CAL-02] already publishes as the
narrow/wide flag. There is now ONE test, it is the test the reader is shown, and the thing
that gates is the thing that is published.

**SHARPNESS IS DISCLOSED, NOT GATED.** The width ratio is published beside the record and
carries NO threshold. A band wider than a naive one is not automatically wrong — the
Egyptian panel runs a median 1.40x because EGX tail risk is real and a close-to-close
estimator genuinely understates it, against 1.11x for AE and 1.00x for US and QA. Setting
a cutoff would be a free parameter with no out-of-sample evidence behind it, which the
standing PROMOTION RULE forbids in terms. So the number is shown and the reader judges.
This is the standard *calibration and sharpness* decomposition, not a weakened substitute
for a proper score: it is the same information, split into the two questions people
actually ask, and each half is separately checkable on the public ledger.

### What is retired, and what merely stops being a gate

RETIRED: the three-way verdict as an object with authority — as the Step 0 gate, as the
materiality trigger, as a PENDING_REVIEW field with standing, and everywhere on every
public surface. No document, page, figure or deliverable states it. The materiality gate's
"an existing name's verdict changes / the market verdict changes" conditions are replaced
by "a name's coverage flag changes, or the published 90% cone moves >5%" — the cone-width
condition already carried most of that weight.

NOT retired: `mc_v3.crps_skill()` and the bootstrap remain in the codebase as an internal
DIAGNOSTIC, because CRPS is a proper scoring rule and is a reasonable thing to look at
when investigating a model change. What is forbidden is the diagnostic acquiring authority
again — it may not gate, trigger, block, or appear in front of a reader.

### The general lesson

A test that never changes an outcome is not conservative, it is decorative, and it costs
something real: it occupied the place a working check should have held, it had to be
explained on the methodology page, and its label was actively wrong about the names it
flagged ([R-CAL-02]). **BEFORE ADDING OR KEEPING A GATE, ASK WHAT IT HAS EVER REJECTED.**
If the answer is nothing, either the bar is in the wrong place or the thing it measures is
not the thing that matters — and the honest move is to find the check that would have
caught something, not to keep the one that reads as rigour.

---

## [R-GAP-01] A fair value far below the traded price is a claim about the world, and it is audited like one (1-Sep-2026, per instruction — "Whenever the fair value is less than the latest known market price for a stock by more than 10% then check thoroughly what you have missed and do a thorough check on all valuation aspects")

### The incident that produced it

On 1 September 2026 the AMOC rebuild finished, and its central fair value printed at
EGP 5.53 against a market price of EGP 9.10 — thirty-nine per cent below.

Every gate in this repository passed it. Step 0.0 passed. SIGCM passed, clause by clause.
The beta was conforming, regressed against EGX30 through `beta_regression.own_stock_beta()`
and attested by `assert_beta_provenance()`. The model-report depth bar passed on all eight
standards. The workbook recalculated with zero disagreements across 5,775 formula cells.
The external-reader scrub returned zero hard hits. The table-discipline check returned zero
problems in both delivered documents. Nothing in that list was wrong, and not one item on
it was looking at the answer.

The user looked at the answer, in four words: *how come the fair value is half what AMOC is
trading today.*

What the discount was hiding, found only because that question was asked:

1. **The reviewed half-year statements had been downloaded and never opened.** They sat in
   the run's own source directory, retrieved from the company's archive and logged as
   retrieved. The study was still describing that period as "a press release rather than a
   filing" and had *solved* its gross profit out of the profit line rather than reading it.
2. **The coherence test that licensed the solve was itself wrong.** It estimated the half's
   other income by doubling one quarter's — EGP 451mn against a filed 197mn — and then
   rejected the released gross profit for disagreeing with a number the model had invented.
3. **Three macro paths contradicted each other** inside one model: domestic inflation, the
   currency path, and the product-price path each carried their own assumption, none
   reconciled to the others. This is [L-048], a lesson produced by *this same run's own
   walk-forward* hours earlier and not applied to the study being rebuilt beside it.
4. **The company's cash was charged for twice.** AMOC holds net cash, so a debt weight below
   zero levered the equity weight above one and pushed the operating discount rate 374bp
   ABOVE the cost of equity — and then the same cash was added back at face in the bridge.
5. **Terminal growth of 5% sat against a terminal discount rate embedding 7% inflation**, so
   the terminal business was assumed to shrink in real terms forever with nothing saying so.
6. **A headline claim was typed rather than computed, and was false.** The study said the
   traded price required a gross margin "above the best single quarter this company has ever
   filed". The company had filed a higher one twice (13.84% in FY2022, 13.92% in Q2-2026);
   the margin actually required, solved by bisection, is 9.37% — comfortably inside the
   company's own filed range.

Corrected, the study prints 5.53 / **8.64** / 12.48 against a spot of 9.10 — a five per cent
discount rather than a thirty-nine per cent one.

### What the rule is

**Whenever a study's central fair value sits more than 10% BELOW the latest known market
price for that name, the study is not finished until a thorough review of every valuation
aspect has been done and written down.** The review is a dated document in the study's own
directory (`GAP_REVIEW_{DD-MM-YYYY}.md`) and it covers, at minimum, the eight headings
below. It is a hard gate on delivery, not a note in the QC table.

The eight headings are not invented. Each names a defect that was actually present in AMOC
on the day this rule was adopted, and **each one was individually capable of producing the
whole gap**:

| Heading | What it must establish |
|---|---|
| LATEST FILINGS | every disclosed period has actually been READ, the most recent named with its date and its route |
| BASE YEAR | the base year foots to filed periods, and anything annualised, scaled or solved is named as such |
| MACRO COHERENCE | inflation, currency and price paths are one path, mutually consistent — [L-048] |
| DISCOUNT RATE | the rate operations are discounted at is the right one, and cash is charged for exactly once |
| TERMINAL | terminal growth is coherent with the inflation embedded in the terminal discount rate |
| BALANCE SHEET | the equity bridge stands on the latest disclosed balance sheet, not a stale one |
| CLAIMS AGAINST THE RECORD | every "best ever" / "never" / "unprecedented" statement recomputed against the filings |
| MULTIPLE CROSS-CHECK | the earnings and enterprise multiples the fair value implies, stated and defended |

### Why the trigger is the market price, and why that is not deference to it

This project does not treat the market price as correct. It publishes fair-value ranges
precisely because it thinks prices are sometimes wrong, and a genuine 39% discount is a
legitimate thing for a study to conclude. **The rule does not say the answer must change.**
It says the answer must be *audited* before it ships.

The reason is evidential, not deferential. A large discount is the one output shape that is
consistent with almost every modelling error this repository has ever made: a stale base
year, an over-charged discount rate, a missed revenue line, a real-terms terminal decline, a
half-year annualised wrongly, an unread filing. Errors are not symmetric in their effect on
a DCF — most of them push the value DOWN. So a large discount is a **high-prior-of-defect
region**, and the price is the only instrument in the room that measures it.

Note what happened at AMOC: all six defects were of the *the model was wrong* kind. Not one
was of the *the company turned out better than we thought* kind. That is the pattern the
rule is fitted to, and it is why the review's headings are all about the MODEL and none of
them about the company's prospects.

### One-sided, on purpose, and the cost of that is stated

The rule fires on a central far BELOW the price. It does **not** fire on a central far
above. That is the instruction as given, and it is left as given rather than symmetrised on
my own initiative — but the asymmetry is a real cost and is recorded here rather than
discovered later: a study that is too optimistic gets no automatic audit from this gate, and
nothing else in the protocol supplies one. The counterweight is that an optimistic study
faces the guidance rule ([R-FCAL-01]: *guidance is scored and never consumed*), the
margins-are-outputs rule, and the fundamental walk-forward's own finding that this house's
forecasts lean optimistic — none of which have a downside analogue. Revisit on instruction.

### The threshold is the instruction's, and it is not disguised as a derivation

10% is the number the instruction gave. It is not derived from anything, and this document
does not dress it up as though it were — the PROMOTION RULE forbids a free parameter with no
out-of-sample evidence behind it, and inventing a justification for a number somebody chose
is the same offence wearing better clothes. What is defensible is the SHAPE: a threshold
here is cheap in both directions (a review costs an hour; a shipped 39% error costs the
study), so precision in the cutoff buys very little. AMOC's own first pass was at −39% and
its corrected pass is at −5%, so on this one worked case the line at −10% separates them
with room on both sides.

### Enforced from outside, per [R-ENF-01]

`scripts/check_valuation_gap.py` runs over every `engine/*_study/` from outside the studies,
in CI. It reads each study's OWN committed numbers for a central fair value and the spot it
was struck against, computes the gap, and where the gap breaches, requires a dated review
covering all eight headings. **A self-attested boolean is never a check**: the study does not
get to declare that it looked.

Three refusals are built in:

- **An unreadable answer is not a clean answer.** A study whose committed numbers do not
  expose a central/spot pair FAILS rather than being skipped. On adoption day 16 of 24 study
  directories were in that state, and every one of them would silently have been "clean".
- **The population is anchored somewhere else** [R-ENF-04]. The gate globs `engine/*_study`,
  so a mis-resolved path would find nothing and report no violations — an absent answer
  wearing the costume of a clean one. It therefore holds its glob against the tickers named
  in `gap_outstanding.json`, every one of which must resolve on disk, and it FAILS outright
  on a run that examined zero studies.
- **A review that skips a heading is not a review.** The rubber stamp is how a review
  requirement normally dies, so heading coverage is checked, not the file's existence.

It is a RATCHET, not a cliff, per [R-ENF-02]: `engine/build_depth_audit/gap_outstanding.json`
lists what was already breaching or unreadable on adoption day and allows it to fail; the
build breaks on a NEW breach, a NEW unreadable study, or a study directory with no entry
either way, and the list may only ever SHORTEN (`--prune` rewrites it). Seeded 1-Sep-2026
with four breaching studies and sixteen unreadable ones. Negative-controlled by
`scripts/check_valuation_gap_negative_control.py`, which reinjects all five failure
conditions and three clean cases — including a central far ABOVE spot, which must NOT fire,
because a check that goes red where no rule exists is the permanently-red check [R-ENF-02]
forbids.

The worked precedent is `engine/amoc_study/GAP_REVIEW_01-09-2026.md`.

### The general lesson, which is not about this threshold

**Every gate in this repository checked the study's PROCESS and none of them looked at its
ANSWER.** That is not an accident of which gates happened to get written; it is what
process gates are for, and it is why they are all individually right and were collectively
blind. Provenance, arithmetic, source discipline and recalculation can every one of them be
perfect while the number at the end is absurd, and on 1 September 2026 they all were and it
was.

So: **when a result is surprising, that is evidence, and evidence gets a gate.** The place to
look for a missing check is not among the steps — those are well covered — but at the
output, asking the question a reader would ask on seeing it. Here the reader asked it in
four words and found six defects. A gate that asks the same question automatically is
cheaper than a reader who has to.

---

## [R-MERGE-01] A run that ends on a branch has not ended (1-Sep-2026, per instruction — "can you merge the branch to the main automatically in this exercise from now on or at least create a PR to draw my attention, otherwise I will forget")

### The rule

At the end of every campaign name: **open the PR unprompted, wait for CI, and merge it once every
repo gate is green.** Don't ask, don't park it, don't end a session with the work on a branch.

### Why this is not about convenience

On adoption day, [R-GAP-01] was written into both governing documents, enforced in code,
negative-controlled and pushed to a feature branch. **It would have bound on nothing.** The next
name in the campaign starts from a fresh clone of `main`, and `main` did not carry it. The rule
would have existed and not executed — which is [R-ENF-01]'s exact failure one level up: nobody
disagreed with it, it simply was not present at the moment it bound.

That generalises past this one rule. Every lesson in the register, every corrected prompt, every
`STANDARD_VERSION` bump reaches the next study through `main` or it does not reach it at all. The
branch is where work is *made*; it is not where work *lands*.

Measured the same day: the AMOC branch carried eight commits and sat unmerged for the entire
session, including the digest rename, the two stale QC items in the study-initiation checklist
(one of which would have had a new study gate on a verdict retired on 25-Aug), and lessons
L-048 through L-056.

### Green means every gate, not a subset

Protocol sync · protocol text and its negative control · study provenance · lessons register and
its negative control · technical calibration and its negative control · campaign queue ·
fair-value register · valuation gap and its negative control · band vocabulary · technical read ·
coverage floor — plus the PR's own CI runs. **A gate that cannot be run is not a green gate.**

### The pause that was proposed and overruled

It was proposed that a name be held for a human look before merging in the two cases where this
session actually went wrong: where the central lands more than 10% below the price, or where fair
value moves a long way. The evidence for it was direct — the first AMOC pass cleared *every* gate
at 39% below the traded price, and what caught it was a person looking at the answer, in four
words.

**The instruction declined the pause, and the instruction stands.** The cost is recorded here
rather than discovered later: [R-GAP-01] is now the only thing standing between a wrong study and
`main` on precisely the shape of error that produced this session's worst defect, and it is **one
run old with no live catch to its name** — its four seeded breaches are historical, not caught in
flight. If it ever passes a study a reader then finds wrong by a large margin, that is the evidence
to revisit this clause. It is written down so the revisit does not depend on anyone remembering.

### The reporting threshold

*Added 1-Sep-2026, per instruction — "tell me the number if it is more than 10% only."*

**Within 10% either way: merge on green and say nothing about the fair value.** An ordinary result
does not need reporting, and a number quoted at the end of every one of ninety names is a number
nobody reads by the tenth. This is the reasoning [R-CAL-02] already uses when it says nothing at all
about a cone that held as often as it promised: **silence is the honest response to an ordinary
outcome**, and it is what makes the exception legible.

**More than 10% either way: the closing message carries the central, the spot and the gap** — called
out, not buried.

**Symmetric on purpose, and deliberately unlike [R-GAP-01].** That *audit* gate fires only below the
price — one-sided by instruction — and records as its own stated cost that an over-optimistic study
gets no automatic audit and nothing else supplies one. This threshold fires **both** ways, so a
central far above the price stops passing unremarked.

**Reporting is not auditing, and the two must not be confused.** The merge does not wait for a
reply, so this clause buys a chance to catch a bad answer *after* the fact, never before it.
Merging is not gated on it either: [R-GAP-01] already blocks a study more than 10% below the price
at CI until its `GAP_REVIEW` exists, so the audit happens before the merge regardless of what is
reported. This clause governs what reaches the user, never what reaches `main`.

### What is unchanged

**Publishing to the live site is still a separate, explicitly-requested step, and nothing here
touches it.** Merging a rebuild to `main` moves `fair{bear,base,full}` in the repository, not on
testahil.com; the campaign prompt's NEVER PUBLISH FROM THIS CAMPAIGN clause stands in full.

Engine and protocol changes still go through a PR rather than a direct push to `main`. What changed
is who closes it, not whether one is opened.

### Enforcement is prose, and that is said plainly

Per [R-ENF-01], a rule that can be tested is tested — and this one cannot be, honestly. It governs
what the operator does at the end of a run, not a property of the repository a checker can read. A
gate running on the feature branch cannot know whether that branch will be merged, and one
demanding that every run directory already be on `main` would be red on every branch by
construction, which is the permanently-red check [R-ENF-02] forbids.

The honest backstop is the campaign register itself: `fv_movement.py check` anchors on the run
directories on disk, so a name whose work never reached `main` surfaces as a run with no delivered
edition the next time the campaign is read from a fresh clone.

[R-MACRO-01] ONE HOUSE MACRO PATH PER MARKET, AND EVERY GROWTH RATE IN EVERY MODEL SITS ON IT [ADOPTED 02-Sep-2026, method reassessment WS2]

The failure. Five studies delivered under one standard carried five different inflation rates for the same fiscal year in the same country — 25.2%, 14.5%, 11.5%, 10.0%, and one with no inflation number at all — three different sovereign quotes, and terminal inflations of 5%, 7% and about 15%. Not one of them was indefensible on its own; every one was sourced, and each study's own reviewer could read its number and agree with it. What nobody could do was read two studies together, because a company cannot be valued in an economy the study beside it does not recognise, and the differences moved fair values by more than most of the driver work did.

Why it is not tidiness. The incoherence is DIRECTIONAL, and it points the same way every time. Escalating costs at domestic inflation while holding the currency or the selling price still is one event counted once and ignored once: it inflates every cost, freezes every price, and manufactures a margin decline the forecast then reports as a finding. That is [L-048], measured on AMOC's own history at a bias of -0.570 log — about 1.8 times too low — wrong in the same direction in every case. Setting terminal growth below the inflation buried inside the terminal discount rate is the same defect at the far end of the model: PHDC published 12% terminal growth against roughly 14.6% of embedded inflation, a perpetual real decline of two to three points a year that nothing in the company's record supports and no reader was told about. That is [L-055]. Both lessons were registered, both were true, and neither bound anything: they were advice in a document, and the next study set its own number as before.

The rule. engine/macro_path.py holds ONE dated, sourced path per market — an inflation ladder from the central bank's own published forecasts to a terminal, the policy-rate glide, the sovereign quote, the currency, the long-run corporate cost-of-debt norm, the real-rate convention and the terminal equity risk premium — in engine/macro_paths/{MARKET}.json. A study imports it and MAY NOT CARRY AN INFLATION NUMBER OF ITS OWN. Every level in a path is either published by a named institution on a named date, or DERIVED by an identity from numbers that are; the one class in between, a year between two published endpoints, is labelled "interpolated between published endpoints" in the file itself and is never described as anyone's forecast.

The identities, so that nothing downstream re-derives them differently. The currency path is relative purchasing-power parity on that path's own inflation against long-run foreign inflation, never set by hand. The terminal nominal risk-free rate is the terminal inflation plus the real-rate convention, derived and never quoted — a terminal rate reverse-engineered from a price is the quietest lever there is and stays prohibited outright. Terminal growth is terminal inflation plus a STATED real growth, default zero: assuming real decline in perpetuity remains permitted, and it must be written down as the real number it is.

Growth rates are STORED as (real, inflation-path id) and recompute to their nominal. A nominal rate typed into a model is unfalsifiable — nobody can tell whether 12% meant inflation plus one point of real growth or inflation minus three — and every one of the five studies' rates was typed.

THE EXPLICIT WINDOW RUNS UNTIL GROWTH HAS CONVERGED. A model whose last explicit year still grows far above its terminal capitalises a rate it never reached and puts most of its value there: a five-year window on a name compounding at 44% nominal, capitalised at a normalised terminal rate, leaves 75-87% of value in the terminal. The window extends until the modelled growth path is within 2pp of terminal growth.

A MARKET WITH NO SOURCED PATH RAISES. There is no fallback to a neighbour, a region or a global average — the same stop-and-inform discipline the index resolver already applies. An empty answer is not a clean answer [R-ENF-04]. On adoption only EG was sourced; the other six markets carry files that declare themselves pending, say why, and refuse.

SCOPE OF THE GLIDE IS UNCHANGED. A path's regime says whether the cost-of-capital glide applies: transition markets glide, pegged markets are already at their terminal by construction of the peg and the glide collapses to flat. This rule supplies the anchors; it does not extend the glide's scope.

ENFORCED FROM OUTSIDE per [R-ENF-01]: research_protocol.assert_macro_coherence() holds a study's own committed record to the path, and scripts/check_macro_coherence.py runs it over every engine/*_study/ in CI — ratcheted per [R-ENF-02] (every study predating the path is listed in engine/build_depth_audit/macro_outstanding.json and allowed to fail; the list may only ever SHORTEN), population-anchored per [R-ENF-04] (every listed ticker must resolve on disk, and a run that examined zero studies FAILS), and negative-controlled by scripts/check_macro_coherence_negative_control.py, which reinjects all nine failure conditions — including the exact PHDC and AMOC terminals and AMOC's hand-set currency path — plus three clean cases, among them a STATED real growth of 2%, which must NOT fire.

The file the protocol has referenced since July 2026 is finally written: engine/Cost_of_Capital_Reference.md, GENERATED from the paths by engine/build_coc_reference.py and compared byte-for-byte in CI. A document that states a fact which moves must not be the thing that remembers it — the same rule the as-of stamps and the band records obey.

THE GENERAL LESSON, WHICH IS NOT ABOUT INFLATION: A LESSON THAT BINDS NOTHING IS ADVICE, AND ADVICE LOSES TO THE NEXT DEADLINE. [L-048] and [L-055] were both registered, both correct, and both re-violated by the studies delivered after them. What changed here is not the finding but its enforcement: the number lives in one place, the identity is computed rather than trusted, and a gate outside the study fails the build. Where a lesson can be made arithmetic, making it arithmetic is the only way it survives.

[R-BRIDGE-01] THE ENTERPRISE-TO-EQUITY BRIDGE IS A RECORD, AND IT IS CHECKED FROM OUTSIDE THE STUDY [ADOPTED 02-Sep-2026, method reassessment WS4]

The failure. Four defects, all of them shipped, none of them visible to any gate this repository had, because every one sat inside a study's own arithmetic — and that arithmetic recalculated perfectly. A recalculation proves the model computes what it says it computes; it says nothing about whether what it computes is the right bridge.

THE BRIDGE STOOD ON A STALE SHEET. PHDC's bridge stood on 31 December 2025 while a reviewed 31 March 2026 balance sheet sat on the company's own result centre — in the very document set the study had already drawn its first-quarter income figures from. AMOC's did the same. Nobody had opened the filing, and nothing in the study could tell a reader that. The bridge now stands on the LATEST DISCLOSED sheet, and the record must name the register that establishes what "latest" means: a study with neither a sweep register nor an investor-relations register cannot claim to stand on the latest sheet and FAILS rather than being skipped [R-ENF-04].

THE MINORITY CAME OUT AT BOOK, OR NOT AT ALL. The model capitalises one hundred per cent of the subsidiaries' cash flow, so the minority's claim on it is worth its SHARE OF THAT VALUE, not what it historically cost. CLHO deducted book and overstated parent equity by roughly a third of the minority; PHDC deducted nothing whatever while dividing by parent shares. The adopted basis is the subsidiaries' own economics where the minority's subsidiaries are disclosed, and a value-share proxy — with the proxy and its source NAMED — where they are not. Book, the profit share and the proportional read are published beside the adopted basis so a reader sees the choice rather than only its result. The minority is deducted from EQUITY value and never from enterprise value: an equity share applied to an enterprise number hands the minority a share of growth assets it does not own.

THE CASH WAS CHARGED FOR TWICE. AMOC discounted its operations at a net-debt-weighted rate — which on a net-cash company drives the debt weight negative, levers the equity weight above one, and puts the operating rate 374 basis points ABOVE the cost of equity — and then added the same cash back at face in the bridge. A reader may value the whole firm at a blended rate and add nothing, or value the operations at the operating rate and add the cash. Not both, and the record now says which.

THE BRIDGE DID NOT HAVE TO FOOT. Nobody outside the model that produced the lines was adding them up. The lines are now asserted to sum to the stated equity value, and the equity value to divide to the stated per-share figure.

Two smaller clauses ride with them: associates are carried at market where the associate is listed, at book otherwise, and a LISTED associate carried at book must say why; and a dividend is deducted only if it was declared AFTER the bridge's balance-sheet date, because one declared before it is already out of the equity it would be deducted from.

ENFORCED FROM OUTSIDE per [R-ENF-01]: research_protocol.assert_bridge() reads a study's own committed bridge_record and scripts/check_bridge.py runs it over every engine/*_study/ in CI — ratcheted per [R-ENF-02] (PHDC and TMGH conform at adoption; the other twenty-two are listed in engine/build_depth_audit/bridge_outstanding.json and allowed to fail, and the list may only ever SHORTEN), population-anchored per [R-ENF-04], and negative-controlled by scripts/check_bridge_negative_control.py, which reinjects all nine construction defects plus a missing record, an unparseable file and an emptied population, and four clean cases — among them NET weights with the cash NOT re-added, which is a legitimate construction and must not fire.

THE GENERAL LESSON, WHICH IS NOT ABOUT BRIDGES: A MODEL THAT RECALCULATES IS NOT A MODEL THAT IS RIGHT. Every one of these four defects lived inside arithmetic that reconciled to the last cell, and the study's own recalculation gate reported zero mismatches while it did. Where a construction can be recorded as a set of choices — which sheet, which basis, charged how often — record the choices and check them, because the number they produce cannot be checked by recomputing it.

[R-LENS-03] ONE CLASS PRIMARY IS THE CENTRAL; THE OTHER LENSES ARE CROSS-CHECKS [ADOPTED 02-Sep-2026, method reassessment WS3]

The failure. PHDC's published central was a weighted blend of four lenses at typed weights — 45% discounted cash flow, 15% book value, 20% an earnings multiple on its own history, 20% normalised earnings power. THREE OF THE FOUR VALUE A DEVELOPER ON ITS REPORTED ACCOUNTING EARNINGS AND ITS HISTORICAL-COST BOOK. For a company whose value sits in an undelivered order book of EGP 263bn carried at historical cost, in a currency that has lost most of its value since 2022, those three measure a floor and not a value. The cash-flow lens landed within 2.2% of the market price. The blend landed 28% below it. Nothing in that study was wrong except its architecture — and the weights had never cleared any out-of-sample test whatever. They were chosen, written down, and inherited by the next study, which is how a free parameter survives in a house that forbids free parameters everywhere else.

What is adopted. ONE class primary is the central. Every other lens is a CROSS-CHECK: published in the same table, and defining the bear/full envelope as the RANGE of the present-value reads on one clock — never averaged into the answer, and never a spread invented around it. Whether any blend beats the primary alone is a question for the valuation calibration to answer OUT OF SAMPLE; until it does, the typed blend is retired, because it never cleared the bar it was always required to clear. That is the promotion rule applied to an architecture rather than to a parameter.

The registry. research_protocol.LENS_REGISTRY is keyed on lessons_register.CLASSES BY IMPORT, and the import fails if the two disagree — a second taxonomy for the same companies is how two registers drift apart, and this repository has paid for that once already. Developers take the cash-flow lens with RNAV, a relative multiple and book value beside it; refiners, petrochemicals and cement take enterprise-value multiples on their own history and replacement cost; banks take dividends discounted with residual income beside them; holding companies take a disciplined sum of the parts.

RNAV IS SPECIFIED BEFORE IT MAY BE A PRIMARY: a PRESENT-VALUE net asset value on one clock — land at cost with a labelled market cross-check and never market as the base, absorption on the company's own delivery rate, discounted on the cost-of-capital schedule, no gross NAV. Where land value per unit of area is an undisclosed gap the class primary stays the cash-flow lens and RNAV is a cross-check, which is SIGCM clause 8: stop rather than invent.

Four clauses ride with the architecture. BOOK VALUE IS A DISCLOSED FLOOR, published as such and never weighted into a central. A RELATIVE MULTIPLE IS NON-CIRCULAR — forward earnings times a multiple from peers or from the company's own history, never from the current price, which values the company at what it already trades at. NORMALISED EARNINGS IS FISHER-CONSISTENT OR ABSENT: capitalised at a real rate against real earnings, or at a nominal rate net of growth; nominal stasis in a currency whose discount rate embeds fifteen per cent inflation is a perpetual real decline, not prudence. And NORMALISED EARNINGS IS NOT A DEVELOPER LENS AT ALL — its absence from both developer rows is deliberate: a developer recognising revenue on handover reports earnings that are an accident of which project completed in which year, and capitalising a mid-cycle figure treats that schedule as a steady state. It was PHDC's worst read, at EGP 5.17 against a cash-flow lens of 14.86, and it carried a fifth of the weight.

ENFORCED FROM OUTSIDE per [R-ENF-01]: research_protocol.assert_lens_design() reads a study's own committed lens record and scripts/check_lens_design.py runs it over every engine/*_study/ in CI, ratcheted per [R-ENF-02] and population-anchored per [R-ENF-04]. Negative-controlled by scripts/check_lens_design_negative_control.py, whose cases include PHDC's architecture EXACTLY AS IT SHIPPED. That control did its job on its first run, and against this rule's own author: it caught an inconsistency in the registry itself, where a case written as "clean" used a lens the class does not permit. A check tested only against the defect that inspired it is fitted to that defect.

THE GENERAL LESSON, WHICH IS NOT ABOUT LENSES: A NUMBER PRODUCED BY AVERAGING SEVERAL METHODS IS NOT MORE ROBUST THAN THE BEST OF THEM — it is a new method, with free parameters nobody tested, wearing the appearance of caution. Averaging feels conservative and is not: it imports every weakness in the weakest lens at whatever weight somebody typed. Where several methods disagree, publish the disagreement and say which one the answer is.

[R-COC-01] THE COST-OF-CAPITAL SCHEDULE LIVES IN ONE MODULE, AND A STUDY CALLS IT [ADOPTED 02-Sep-2026, method reassessment WS1]

The failure, and it is the same shape as every other enforcement failure this repository has recorded. The sliding-schedule procedure has been written down since 13 July 2026, in both governing documents, in full: each explicit year discounted at its own forward rate, the glide's shape taken from the cost-of-debt path rather than invented, a norm-built terminal none of whose lines is an observable quote, and a three-assert integrity gate on the cost of debt. On 2 September 2026 exactly ONE study in the repository implemented it. AMOC carries the glide, the monotonicity assert and the wacc_term < wacc_exp assert inline in its own compute.py; every other study discounts a five-year forecast and a perpetuity alike at a single crisis-level rate — PHDC at 26.25%, TMGH at 32.37% — which asserts that Egypt's cost of capital never normalises, while the central bank publishes a disinflation path and the studies' own cost-of-debt assumptions already follow it. The rule was correct, and it was not present at the moment it bound.

What is adopted. engine/cost_of_capital.py takes a market, a beta record, the debt book, the market capitalisation and the tax rate, and returns the whole ladder: the explicit-window cost of equity and debt, market-value weights, one forward rate per explicit year, the norm-built terminal, and the cumulative discount factors — with the terminal value brought home on THE SAME factor as the last explicit year's cash flow. A study calls it and cannot accidentally discount a forecast at a rate the economy is not expected to hold, because that is not a thing the function can return.

Every anchor comes from the house macro path [R-MACRO-01], so the terminal is derived rather than chosen: terminal risk-free = the inflation target in force plus the real-rate convention; terminal cost of debt = the long-run corporate norm; terminal premium = normalised below the crisis level. The glide's fractions are the policy-rate path's own cumulative progress, so the front-loaded shape is inherited from the easing calendar rather than being a second free parameter.

SCOPE IS UNCHANGED AND IS ENFORCED BY THE PATH, NOT BY MEMORY. A pegged market is already at its terminal by construction of the peg; the module returns a FLAT schedule there and says so, rather than manufacturing movement the peg forbids. Only a market the path calls a transition glides.

The hard refusals, each of which raises rather than warning. WACC_TERM < WACC_EXP in a transition market. A monotone ladder. Country risk counted exactly once — the risk-free rate normalised by this sovereign's OWN default spread, on the same basis as the premium added back. Market-value equity weights, never book. A cost of debt above its own sovereign on an all-local-currency book. And the three-assert cost-of-debt gate: the currency composition sourced to the facility note; an INDEPENDENTLY computed effective rate over at least two periods, with its DENOMINATOR described, because dividing the finance charge by a broader liabilities total that includes balances bearing no interest understates the rate by a multiple and manufactures a bias that looks exactly like evidence; and the adopted rate within 150 basis points of the latest effective rate and no more than 50 above the peak.

A SOVEREIGN QUOTE OLDER THAN FOURTEEN DAYS REFUSES rather than being used quietly. It may be accepted deliberately, and then the staleness is disclosed in the schedule's own record.

Both premium bases are published and one is named CENTRAL; the swap basis is the default because it is the market's own live pricing of the sovereign's credit, while the rating basis is an agency judgement updated in steps. The country premium may be scaled by a lambda, whose default is 1.00, and any other value is a stated judgement published beside the equity-to-bond scaling it is an alternative to. A noisy beta may be shrunk toward its market-class prior by the Vasicek weight, which moves a tight estimate barely and a loose one a long way; where it is applied, the raw beta and the shrinkage are disclosed.

WHAT THE MODULE FOUND ON ITS FIRST RUN. AMOC's own committed record carries a cost of debt of 22.00% against a sovereign yield of 22.31% recorded in the same file — thirty-one basis points below the government that taxes it, which the standing rule has forbidden since the method's adoption. On a company that is net cash the number barely moves the answer, and the rule is the rule: it is registered for correction at that study's next re-issue. A gate whose first run finds a real defect in the one study that implemented the procedure is the argument for gates.

ENFORCED FROM OUTSIDE per [R-ENF-01]: scripts/check_cost_of_capital.py reads each study's own committed schedule record and asserts every clause above, ratcheted per [R-ENF-02] and population-anchored per [R-ENF-04], negative-controlled by scripts/check_cost_of_capital_negative_control.py — whose cases include the flat rate exactly as PHDC and TMGH publish it, the two-prices-for-one-date construction, the sovereign counted twice, and AMOC's own Kd pair.

[R-GAP-01 AMENDED] THE GAP GATE IS TWO-SIDED [AMENDED 02-Sep-2026, method reassessment WS7]

The rule as adopted on 1 September 2026 fired only where the central fair value sat more than ten per cent BELOW the latest known price. The one-sidedness was the instruction's, it was taken as given, and its cost was stated at adoption rather than discovered later: an over-optimistic study would get no automatic audit, and nothing else supplied one.

The reassessment measured what that cost. Because only the downside was audited, every correction the house made ran the same way — each individually right, and collectively a lean. A GATE THAT CAN ONLY FIRE IN ONE DIRECTION TEACHES THE WORK TO DRIFT IN THE OTHER, and it does so while looking rigorous, because the audits it does perform are real.

From 2 September 2026 the same ten per cent ABOVE the price fires the same eight-heading review. Nothing else changes: the headings, the ratchet, the enforcement and the negative control are as they were.

The trigger stays EVIDENTIAL rather than deferential, in both directions. A large gap either way is a high-prior-of-defect region and the price is the only instrument in the room that measures it. The rule does not say the answer must change — a genuine thirty-nine per cent discount and a genuine thirty-nine per cent premium are both legitimate conclusions, and this project publishes ranges precisely because prices are sometimes wrong. It says the answer is AUDITED before it ships.

MANDATORY INSIDE THE PROGRAMME, NOT ONLY AT PUBLISH: every re-issue that lands more than ten per cent either side of the price gets its review before its files are staged.

WHAT THE FIRST TWO-SIDED RUN FOUND. DU: a central thirteen per cent ABOVE the spot it was struck at, with no review — invisible to the one-sided rule by construction. It is listed on the ratchet rather than fixed on the night the rule changed, because the list is the honest record of what is outstanding, and it is reviewed when that study is next re-issued.

THE NEGATIVE CONTROL'S OWN CASE IS INVERTED RATHER THAN DELETED. It carried a case asserting that a central far above the price must NOT fire, which was correct evidence for the one-sided rule. That same construction now must go red. Keeping the case and flipping its expectation is the sharpest available evidence that the extension actually took effect; deleting it would have left the change untested in exactly the place it matters.

[R-ENF-05] THE STUDY AUDITS ITS OWN ANSWER: THE REVERSE READ AND THE SIGN TEST [ADOPTED 02-Sep-2026, method reassessment WS7]

Every gate this repository had examined how a study was BUILT. [R-GAP-01] was the first to look at the answer, and it looked at one number in one direction. Two further instruments are adopted here, both aimed at the same failure: a house that leans one way and cannot see it, because each individual choice was defensible.

THE REVERSE READ. Every study states what it believes; almost none states what the PRICE believes, and the two are the same model read backwards. Each study now publishes the growth, margin, conversion rate or discount rate that the traded price implies UNDER ITS OWN DRIVERS, solved by holding everything else at its published value. That turns a disagreement into a measurable one: not "we are 28% below" but "the price is paying for a conversion rate of 7.9% and we forecast 8.7%, and the company's own three cash-flow statements show 3.9%, 17.9% and 4.4%". A reader can then judge the disagreement rather than the conclusion.

THE HARD PART IS KEEPING IT OUT OF THE MODEL, and the rule is structural rather than remembered. The reverse read lives in the study's own diagnostics.json, never in the numbers file every builder reads, and research_protocol.assert_reverse_dcf() REFUSES any study whose builders read that file back in. A quantity solved from a price and re-entering the valuation is the reverse-engineered terminal the cost-of-capital procedure prohibits outright, arriving through a side door; the prohibition is worth nothing if the side door is open.

THE SIGN TEST. Any single contested choice in a valuation is defensible. What is not defensible is a study that resolves EVERY contested choice in the same direction and never notices — which is precisely how a lean survives an audit of its steps. Each study records every judgement worth more than five per cent of value with BOTH framings' values, the side adopted and why, and a binomial sign test is printed on the set. A study that lands them all one way at p < 0.05 is FLAGGED, NOT FAILED: a company can genuinely deserve a consistent read, and a gate that failed on it would push studies to resolve their judgements inconsistently in order to stay green, which is the opposite of what this measures. What a study may not do is go unmeasured.

WHAT THE FIRST RUN SHOWED. PHDC carries five material contested judgements and resolved two of them upward — a sign test of p = 1.00, no lean at all. That is the instrument doing its job in the direction nobody expects: the study whose central had just moved from 25% below the price to 13% above it turns out not to have taken every fork in the same direction, which is evidence for the rebuild rather than against it. TMGH shows the same, at p = 0.50.

ENFORCED FROM OUTSIDE per [R-ENF-01]: scripts/check_output_records.py over every engine/*_study/ in CI, ratcheted per [R-ENF-02] and population-anchored per [R-ENF-04], negative-controlled by scripts/check_output_records_negative_control.py — thirteen conditions including a builder importing the diagnostic, a judgement stated without its other framing, and a flagged study that must stay GREEN.

THE GENERAL LESSON, WHICH IS NOT ABOUT VALUATION: MEASURE THE DIRECTION OF YOUR OWN DECISIONS, NOT ONLY THEIR QUALITY. A process can pass every check on every step and still drift, because drift lives in the pattern of choices rather than in any one of them. The cheapest instrument against it is to write down which way each judgement went and count.


[R-VCAL-01] THE FAIR VALUE ITSELF IS GRADED AGAINST WHAT HAPPENED, ON A DESIGN COMMITTED BEFORE THE DATA [ADOPTED 03-Sep-2026, method reassessment WS6]

NO FAIR VALUE THIS HOUSE HAS EVER PUBLISHED HAD BEEN GRADED. The price cones are graded and the record is broad — that is the band record under [R-CAL-02]. The statement walk-forward is graded — that is [R-FCAL-01], and it measures DRIVERS, on a handful of names. Between those two sits the number the house actually publishes and a reader actually acts on, and it had no instrument at all. This rule builds one, and the order in which it was built is the whole of its claim on credibility: the pre-registration was written, hashed and committed BEFORE a single figure existed, so "no lever was fitted to the gap" is a fact about the commit order rather than an assurance. Every such document says it was written first.

TWO SCORES, AND THERE ARE TWO BECAUSE ONE WOULD BE MIS-SPECIFIED. (i) CONTEMPORANEOUS AGREEMENT, log(FV_t / P_t) at every origin — the direct measure of the house lean, which is what the reassessment was called to examine. (ii) GAP CLOSURE, whether log(FV_t / P_t) predicts the subsequent one-, two- and three-year total return NET OF CARRY — the measure of whether the lean is INFORMATION. A house can be systematically pessimistic and right; it can equally be systematically pessimistic and merely wrong, and only the second series separates them. A FAIR VALUE STRUCK TODAY IS NOT A FORECAST OF THE PRICE IN THREE YEARS: at the cost of equity these markets carry, a fair value that agrees perfectly with the price at t SHOULD sit well below the price at t+1 purely by construction, because the value compounds at the discount rate and the comparison does not. A raw log(FV_t / P_{t+h}) with a zero-bias acceptance would therefore condemn a perfectly calibrated method, which is why the naive single score is prohibited here rather than merely discouraged.

A LENS IS GRADED OVER THE HORIZON IT IS USED FOR, AND THE SCORER REFUSES RATHER THAN OBLIGE. The fundamental lens speaks to horizons of up to one year [R-LENS-02], so a vintage is not scoreable on its own clock before a year has passed. Shorter subsequent returns exist, are easy to compute, and would look exactly like evidence — they are evidence about the PRICE CONE's question, which has its own calibration and its own published record. Grading a lens on another lens's clock is the mistake [R-TCAL-01] caught in its own first edition, where a sub-monthly read scored at three months reported the weakest available reading of every claim it made. engine/valuation_calibration/score.py therefore returns a DATE and not a number until a vintage matures, and the date is the honest output.

TWO ARCHIVES, BECAUSE NEITHER EXISTED AND NEITHER CAN BE RECONSTRUCTED LATER. engine/fv_vintages.json holds every fair value the site has published, dated, with the spot it was struck against — assets/data.js carries ONE undated fair{} per name, so "what did we say this was worth in March, and against what price?" previously had no answer but a walk through git history. Its reconstructed half is recovered from the published first-parent line and says in its own records that its dates are when a value APPEARED IN THE REPOSITORY, not when a study was struck; its recorded half is written at publication and carries the study's own strike date. A vintage with no known spot is EXCLUDED and counted, never paired with a later price, because log(FV/P) against the wrong price is not a weaker observation but a plausible number that poisons a pooled mean invisibly. engine/macro_history/ holds what was KNOWN at each past origin, for a rebuild that must not reach for today's numbers.

POINT-IN-TIME IS ABSOLUTE, AND IT MEANS TWO DIFFERENT THINGS. Every figure in the macro archive carries a REVISION CLASS. An OBSERVED figure — a market close, an administered rate, an auction result — is fixed at its date and no institution revises it, so today's database is a legitimate route to it and the observation date is all the evidence needed. An ESTIMATED figure — a price index, a national-accounts aggregate, a computed premium — is revised and rebased for years afterwards, and is REFUSED without naming the publication that existed at the origin. The distinction is not fastidiousness: measured on Egypt's own record, the inflation figure published AT an origin and the figure reported for that same year today differ by several percentage points in BOTH directions, which moves every escalator, the currency path derived from them and the terminal. A FIGURE FILED IN THE WRONG CLASS IS RIGHT IN VALUE, WRONG IN DATE, AND INVISIBLE AFTERWARDS. An origin whose required figures are not all sourced is DROPPED and the window shortened — never interpolated, never carried forward from a neighbouring year — so a thin archive shows up as fewer origins rather than as a fuller-looking record built on filled-in cells.

PROMOTION IS SEQUENTIAL, ORDERED IN ADVANCE, AND STOPS. Levers are evaluated one at a time on the current stack, in an order fixed in the pre-registration before any score exists, and a lever is promoted only while the stacked pooled contemporaneous bias moves TOWARD zero without crossing it by more than the bootstrap half-width. Promotion stops the moment it would cross. This replaces any per-lever "improves on most names" rule, which can stack five individually-justified moves into an overshoot — five corrections each right on its own and wrong together, which is precisely the failure that called this reassessment. THE GUARD IS SYMMETRIC: a positive bias is a finding exactly as a negative one is, and a house that corrects its pessimism into optimism has not fixed anything. The CRPS-selection precedent applies in full: a lever that looks better in sample and loses under leave-one-out is rejected however sensible it sounds. Nothing here is an input to any study, at any origin, and a promoted lever changes the METHOD — delivered studies change only at their next edition, through the ordinary path.

WHAT THE FIRST MEASUREMENT FOUND, AND IT CHANGED THE DIAGNOSIS. Measured across every fair value the site has published, against the price each was struck at: the MEAN sits about a tenth below the price and the MEDIAN sits essentially ON it, with the names split almost evenly either side. The whole of the mean is a TAIL — a handful of names far below their price against a very few far above. THE HOUSE WAS NOT UNIFORMLY PESSIMISTIC; IT WAS INCONSISTENT. That is a different diagnosis with a different remedy, and the obvious remedy would have been the wrong one: moving a rate or a terminal to correct the mean would have pushed every well-centred name off its price in order to fix the few that were wrong. It is also why the construction rules adopted alongside this one — one macro path, one class primary, a checked bridge, one cost-of-capital ladder — are aimed at dispersion rather than at level. READ THE FIGURES LIVE with python3 engine/valuation_calibration/delivered.py; never from this document, because they move whenever a study is re-issued.

ENFORCED FROM OUTSIDE per [R-ENF-01]. scripts/check_valuation_calibration.py establishes the one thing the calibration cannot assert about itself: it reads COMMIT TOPOLOGY, not timestamps — the pre-registration's introducing commit must be an ancestor of every score file's — and the document must still hash to its seal. Timestamps were tried and are not sufficient: two commits in the same second compare equal, and the gate's own negative control caught it passing a fixture in which a score was committed first. It REFUSES on a shallow clone rather than reporting clean, so the job checks out at full depth. scripts/check_fv_vintages.py holds the vintage archive to what the site actually publishes today — CURRENCY, not existence — loading data.js through a real JavaScript parse per [R-ENF-03], and refusing to rebuild from a shallow clone, which would silently replace a long archive with a short one that looks equally authoritative. Both are negative-controlled.

WHAT WOULD OVERTURN THIS. If the mechanically rebuilt fair-value series turns out not to resemble the as-delivered one once the delivered record is long enough to compare, this calibration is grading a method the house does not actually use, and every promotion it made must be withdrawn. That condition is written in the pre-registration in advance, because a test with no stated falsifier is a habit.

THE GENERAL LESSON, WHICH IS NOT ABOUT VALUATION: AN INSTRUMENT HAS TO EXIST BEFORE THE CLOCK CAN START. Both archives this rule depends on record things that cannot be reconstructed after the fact — what a number was on the day it was published, and what the world knew on the day a forecast was made — and neither existed until it was built, which is why the first honest output of the scorer is a date in the future rather than a result. The cost of not having built them earlier is not a gap in a table; it is a year.


## [R-IND-01] INDEPENDENCE: A QUESTION IS THE LAST RESORT, AND IT CARRIES THE PROOF THAT IT IS
*Adopted 3 September 2026, per instruction — "when I say running independently, I mean it.
You should run independently. Don't come to me with your problems. Sort it ... You need to
strengthen your protocols and procedures in terms of independence and problem solving."*

### The two failures this was adopted on, both in one session, three hours apart

Part H of the reassessment plan already said *never ask*. It stopped neither of these,
because it set no bar for what must be exhausted first, because it lived in a programme
plan rather than in the standing protocol, and because it bound nothing.

**(1) A question already answered.** The session asked the principal for the ten-year
Egyptian government yield and the CBE policy rate at each year-end 2013–2023. **They had
been supplied that morning.** One supplied figure had already been found wrong and
corrected against the CBE decision record; six origins were live; the calibration had
already produced its first readings on four of them. All of it was on another session's
branch, and the session had read `main`. One `git branch -r` would have found it. Worse,
the archive on `main` still read *"the one thing I would ask you for"*, so the record
itself was asking — and nothing compared that sentence to the world.

**(2) A failure that was not one.** The session reported that all five re-issued studies
were missing two of their four deliverables. Every file was on disk. The check had counted
keys in a publish manifest that lists two by design: it modelled one artefact and reported
on another, which is the [R-ENF-03] species.

**Neither was hard.** Each was one command away. What they have in common is not
carelessness about facts — the reasoning in both was careful — but a DEFAULT THAT POINTED
OUTWARD: on meeting an obstacle, the session composed a message instead of exhausting a
search. That default is what this rule removes.

### The rule

**A QUESTION REACHING THE PRINCIPAL IS AN ARTEFACT, NOT A MESSAGE.** It is registered in
`engine/escalations.json` before it is asked, and it carries: the routes actually run and
what each returned, with dates; how many refs were searched; why only the principal can
close it; **what was done in the meantime**; the default that will be taken if no answer
comes; and the date that default fires. A question with no such record is not asked.

**THE LADDER IS CLIMBED FIRST, AND CLIMBED, NOT RECALLED.** Before anything is escalated:
the artefact itself is opened — never a document, manifest or register that describes it;
the checkout is searched and then **every live ref**, because work in flight on another
branch is work that exists; any probe whose failure is being relied on is **RE-RUN**, since
an empty result is first evidence that the probe did not run [R-ENF-04] and a written
outcome is a fact about the past; every tool the environment actually provides is used,
its own description being the list — a headless browser defeats a JavaScript-rendered
source, and calling one impossible with the browser installed is a claim about the operator
rather than about the world; and the repository's own registers are searched for whether
this was asked and **answered** before.

**THE REPOSITORY IS NOT ONE REF.** No claim of the form *not present, not supplied, not
done, cannot be obtained* may be made from a single checkout. Several sessions work at
once. A status that reports a closed blocker as open is not cautious — it is wrong, and
wrong in the direction that spends the principal's time on work already delivered.

**AN ANSWER IS WRITTEN WHERE THE NEXT SESSION READS IT, NOT WHERE IT WAS GIVEN.** The
moment a question is answered, the answer goes into the artefact that holds the block, and
the register entry names that file. An answer that lives only in a conversation binds
nothing: the container is rebuilt from the repository, and a session that cannot see the
answer will ask again — which is exactly what happened.

**THE DEFAULT IS TO ACT.** Where a choice is reversible and inside the stated scope, it is
taken, recorded with its reasoning, and REPORTED AS TAKEN — never offered as a question.
Where it is genuinely the principal's, it is registered with a recommendation and a default,
and **the work routes around it** rather than stopping. Nothing waits on an answer that can
proceed without one.

**NEVER A MENU.** A turn does not end by handing the principal a list of options to choose
between. That converts the operator's work into the principal's queue, which is the
instruction's own complaint. One recommendation, taken or registered.

**A GATE WITH NO RELEASE IS A STALL** [R-CAL-01], and it applies to questions too. Every
registered escalation carries a default and a date. When the date arrives the default is
taken and the entry closed. An open entry past its date means the work stopped to wait,
which this rule forbids.

**REPORTING IS NOT ESCALATING, AND THE DIFFERENCE IS WHETHER ANYTHING IS OWED.** Telling
the principal what was found, decided and done is the job. Asking them to unblock something
is the last resort. A message that ends in a question mark where the answer was available
in the repository is the failure this rule names.

### Enforced from outside, per [R-ENF-01]

`scripts/check_escalations.py` reads the register and refuses five ways, each earned:
a missing field; a ladder not climbed (fewer than three routes on a data escalation, no
route marked as a re-run, or fewer than two refs searched); **an open entry whose own
resolving condition is already met on some live ref** — the clause this rule exists for,
which catches the re-ask mechanically rather than relying on anyone remembering; a resolved
entry whose answer is written nowhere; and an entry left open past its own default date.
Negative-controlled by `scripts/check_escalations_negative_control.py`, whose eighteen
conditions include **the 3 September re-ask rebuilt exactly as it would have been written**,
and four clean cases that must stay green — among them an empty register, because nothing
escalated is a legitimate state, and an instruction-class entry, which needs no route
ladder because no route could answer it.

**There is deliberately no ratchet.** A ratchet exists so that a new standard does not
redden work predating it; this register is created by this rule and holds only entries
written under it, so an allowance would exempt the rule from itself.

### The general lesson, which is not about escalation

**AN OBSTACLE IS WORK, NOT NEWS.** The instinct on meeting one is to describe it accurately
to somebody else, and describing it accurately feels like diligence — the message is
truthful, the evidence is real, the tone is appropriately careful. That is what makes this
failure mode survive: it looks exactly like good practice. The test is not whether the
report is accurate; it is whether the search was finished. **Where a question can be
answered by a command available in the room, asking it is not caution — it is the cost of
not having run the command.**
[R-COC-01 AMENDED] THE 150bp COST-OF-DEBT BOUND IS RE-POINTED, NEVER SWITCHED OFF, WHERE THE TRAILING RATE IS THE WRONG INSTRUMENT [AMENDED 03-Sep-2026, per instruction]

THE BOUND EXISTS TO STOP AN INVENTED COST OF DEBT, and it does that by holding the adopted rate against a rate computed independently from the filings. On most books the trailing effective rate is exactly that. On some books it is not, and the reason is mechanical rather than a matter of opinion: interest CAPITALISED into assets under construction never reaches the expensed charge, so the numerator is not the interest the company actually incurred; and a book that RE-BASED WITHIN THE PERIOD — a facility mix that changed materially part-way through — is described by an average balance that existed for none of it. In both cases the trailing average is a real number measuring something other than what the bound is asking about, and dragging the adopted rate toward it would be the smoothing this method forbids everywhere else.

ARCC IS THE WORKED CASE AND IT IS WHY THE AMENDMENT IS NARROW. Its FY2025 effective rate computes to about 5% against an adopted 13.36% — 833bp outside the bound — on a book that is 91% euro-denominated at Euribor-linked rates, re-based from pound credit facilities inside the year, with borrowing costs on the alternative-fuel assets under construction capitalised rather than expensed. Both mechanisms are disclosed in the company's own notes. The adopted rate is the contractual blend with the euro legs carried at local-equivalent cost, which is what the standing FX rule requires; the trailing average simply is not measuring it.

WHAT A RECORD MUST DO TO RE-POINT THE BOUND, AND IT IS A HARDER TEST THAN THE ONE IT REPLACES. Name a mechanism from a CLOSED list — capitalised interest, a book re-based in period, a facility drawn mid-period — because an open list would let any study opt out by inventing a reason, and "the rate looked wrong" is not a mechanism. Carry the DISCLOSURE that establishes it, from the filings rather than asserted. Then supply a CONTRACTUAL ANCHOR: every facility with its balance, its own rate and the note that rate comes from, foreign legs at local-equivalent cost. THE ADOPTED RATE MUST REPRODUCE FROM THOSE LINES. A weighted average either comes out or it does not, which is why this is stronger than the bound it replaces and why it is verifiable from outside the study. A record that declares the exception and supplies no anchor has switched the check off rather than re-pointed it, and fails.

NOTHING ELSE MOVES. A book with no declared mechanism still faces the 150bp bound and the 50bp peak test exactly as before; silence is not an exception. The three-assert Kd gate stands in full — currency composition sourced to the facility note, an independently computed effective rate with its denominator described, and now either the bound or the anchor. Adding a mechanism to the list is a rule amendment, which is the point.

ENFORCED FROM OUTSIDE per [R-ENF-01]: scripts/check_cost_of_capital.py reads the exception and reproduces the adopted rate from the anchor's own lines, refusing an unregistered mechanism, an exception with no named disclosure, an anchor line whose rate has no source, and an anchor that blends to something other than the rate it justifies. Negative-controlled on all six conditions plus a clean exception that must pass.

THE GENERAL LESSON, WHICH IS NOT ABOUT COST OF DEBT: WHEN A CHECK FIRES ON WORK THAT IS RIGHT, THE ANSWER IS ALMOST NEVER TO WIDEN IT. Widening a bound is a free parameter, and moving the number to satisfy it corrupts the thing being measured. The third option — establish that the check is pointed at the wrong measurement, and re-point it at one that can actually be reproduced — is more work and it is the only one that leaves the check stronger than it found it.

[R-COC-01 AMENDED] A STUDY MAY DECLARE ITS DISCOUNTING CONVENTION, AND THEN IT IS CHECKED AGAINST WHAT IT DECLARED [AMENDED 03-Sep-2026]

END-OF-YEAR ARRIVAL WAS AN ASSUMPTION, NOT THE RULE. The gate tested each cash flow as though it arrived on the last day of its year and flagged ARCC, whose factors are a legitimate mid-period schedule struck part-way through a fiscal year — cumulative discounting of 0.25, 0.94, 1.88, 2.83 and 3.79 years off its valuation date. This rule requires ONE DATE, ONE PRICE OF TIME, which that schedule obeys and which the terminal test is what actually enforces; it nowhere mandates year-end arrival. The defect was never the convention. It was that nobody wrote it down.

A RECORD MAY THEREFORE DECLARE ITS CONVENTION — the cumulative discounting time of every explicit year AND the slice of calendar each forward rate owns, without which the factors do not reproduce, since a first period that is a stub is not a unit-width slice from time zero. The factors are then checked against the declaration. A record that declares nothing still gets the end-of-year test, because accepting any factors at all where none is declared would delete the check rather than generalise it, and a declaration that does not reproduce its own factors fails — it reads as evidence, which is worse than an assumption. Negative-controlled on four conditions plus a clean mid-period schedule that must pass.
