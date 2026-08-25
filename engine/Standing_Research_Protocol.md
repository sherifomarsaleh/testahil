PROTOCOL REVISION 2026-08-24c — [R-DOC-01] if your copy does not carry this line, or carries an earlier revision, it is STALE. The current text lives at engine/Standing_Research_Protocol.md
on the repository's default branch; nothing else is authoritative. Bump on every edit.

TESTAHIL — Standing Research Protocol
Updated 23 August 2026 (rev. 7) — THREE-LENS INDEPENDENCE · COMMITTED DRIFT · per-name discipline · negative control (investor-critique session)
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

engine/raw_ohlc/{MARKET}/{TICKER}.csv is a persistent library of every covered stock, not an inbox — 65 stocks across 8 fitted markets (27 EG · 11 SA · 14 AE · 3 QA · 3 US · 3 KR · 3 IN · 1 XAU). To add or refresh ONE stock, add or overwrite ONE file. The pipeline then refits that stock's whole market against the full library.

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
Break-aware volatility estimation inside the engine (currently only the calibration sample is filtered). Moves every published distribution — a deliberate decision, not a silent fix.
Metals is the weakest calibration in the system — say so plainly. Gold is a single-name self-fit: it is calibrated on its own data, so its PARITY verdict is circular in exactly the way Qatar's was until IQCD and QNB de-circularised it. Worse, silver is a PUBLISHED instrument with no fit of its own — it borrows gold's. Every other market has been pulled onto a real panel; metals has not. Until silver/copper/platinum history arrives, the metals cone is the least-evidenced thing Testahil publishes, and it should not be presented with the same confidence as an EGX or GCC name.
UK and Brazil have no covered names; their profiles are stubs.
[NEW 29-Jul] Eleven libraries are STALE, and now self-report it on every page via the tech as-of stamp — TMPV/RELIANCE/INFY (IN), TSLA/AAPL/NVDA (US), IQCD/QNB/QGTS (QA), SILVER, PLATINUM. The stamp made latent staleness legible; it did not create it. A fresh vendor export placed at engine/raw_ohlc/{MARKET}/{TICKER}.csv is the only fix — nothing else unblocks them.
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

Closes open item 1 above, for Egypt only. engine/adaptive_width.py. An OVERLAY, not a refit: the pooled per-market (ν, width_cal) fit is untouched; drift stays pure carry; tail ν is untouched. What it adds is a per-name online multiplier on cone width, learned from that name's own resolved 3-month-window residuals: m_raw = clip(sqrt(EWMA_0.85(u²)), 0.7, 1.5), then gentled and dead-zoned so small deviations don't move the cone at all — mult = 1 + 0.5·sign(m_raw−1)·max(0, |m_raw−1| − 0.10). A name whose own volatility has consistently sat below the panel average narrows toward its own history; a name running hotter than the panel widens toward its own history. Flag off (or insufficient history) reproduces the prior engine bit-for-bit.

Promotion evidence (30-name EG panel, strict LONO/held-out FINAL split, block bootstrap {2,3,4} — the same gate that killed the CRPS-selection idea in "THE PROMOTION RULE" above): proper score held at PARITY (log-CRPS 0.0154 → 0.0152, effectively zero cost) while calibration improved (pooled |std_u−1| 0.096 → 0.069; cov90 0.903 → 0.893, both still in-band; 24 of 30 names moved closer to std_u=1). This targets exactly the over-coverage failure mode described in open item 1 (LGES/Korea, ALPHADHABI/UAE: cov90≈1.00, PIT well-centred) — a market-level cone was too wide for names whose own volatility sits below their panel's average, and the overlay corrects that without touching the pooled fit every other name's cone depends on.

History gate — the reason it does nothing today. The 30-name validation ran on 15-year histories (~30 resolved 3-month windows/name). Production's raw_ohlc/EG currently holds ~5-year histories (~17 windows/name) — short enough that the estimator itself gets noisy, which is exactly the regime the validation flagged as prone to over-correcting. So the overlay carries a hard floor, MIN_WINDOWS=28: below that many resolved windows, the multiplier is forced to exactly 1.0. Verified by import against both the long lab histories (reproduces the validated multipliers, e.g. ISPH m_raw 0.924→mult 1.000, ORHD 0.753→mult 0.926) and current production data (every EG name currently returns mult=1.000 [insufficient_history]). The overlay is real, adopted, and dormant simultaneously — it starts doing something, name by name, only as each name's own library crosses 28 windows.

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
  coverage. Horizons stay 1M/3M by instruction; a shorter-horizon product was offered and
  declined.
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


## [R-CAL-02] The band record replaces PASS / PARITY / FAIL on every public surface (24-Aug-2026, per instruction — "I want to challenge the concept of pass, parity or fail for the MC. Too complicated and the investor would not necessarily understand it")

The challenge was made on legibility. It is upheld on legibility and on a second ground
that turned out to be worse: **the label was factually wrong about the names it flagged.**

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
