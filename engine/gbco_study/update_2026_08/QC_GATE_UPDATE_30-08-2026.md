# QC gate — GBCO fundamental update, 30-Aug-2026

Scope of this edition: fair-value re-issue (compute + report document + fair{} record).
It re-derives the valuation under the current standard; it is NOT the full model-report
document rebuild (see OPEN items — stated, not silently skipped).

| item | verdict | evidence |
|---|---|---|
| Step 0.0 data-quality gate on price series | PASS (inherited) | beta regression runs through beta_regression.own_stock_beta which applies Step 0.0 to stock and index series (index_dq/stock_dq empty in the record); no new OHLC entered this update |
| Historicals official-only (SIGCM 1) | PASS | 15-year panel engine/gbco_training/gbco_panel.json — every company figure tier A (audited FS / ARs / ERs from ir.gb-corporation.com); identity assertions pass on all 15 years |
| Forecast ground-up to finest sourced level (SIGCM 2, R-SIGCM-02) | PASS | assert_ground_up() on 6 DriverLines covering 100.0% of the FY26 revenue base: 76% unit level (PC, light mobility, CV units × disclosed ASPs), 18% derived (GB Capital portfolio momentum — product yields undisclosed, gap noted), 6% segment (trading + residual, gap noted). Output recorded in update_numbers_30082026.json.ground_up |
| Debt LC/FX split (SIGCM 3) | PASS | FY25 FS note 29 read: net USD exposure −EGP 2.19bn, EUR +0.14bn vs ~EGP 38bn debt book (variable-rate EGP 37.9bn) — EGP book, no FX tranche; evidence in WaccInputs.debt_currency_evidence |
| Asset-conversion cycle → BS/CF (SIGCM 4) | PASS | working capital modelled from the disclosed cycle: FY25 auto WC 28.5% of revenue (ER 4Q25 Table 6) normalizing to 24%; DIO/DSO/DPO history studied in the training panel |
| Competitors (SIGCM 5) | PASS (cross-check only) | relative lens band 5–9× vs EGX NBFS/auto peers; used as cross-check, never as source of GBCO's own numbers |
| Beta = own history vs published index (SIGCM 6, R-BETA-04) | PASS | own_stock_beta('GBCO','EG','EGX') re-run this session: β 0.8907, R² 0.243, n=251 weekly, window 2021-09-09→2026-07-16, index raw_indices/EG/EGX30.csv (as-of 2026-07-22), tier 1, conforming; assert_beta_provenance() called in compute_update.py |
| Formula-based model (SIGCM 7) | PASS | compute_update.py: INPUTS → drivers → legs → DCF/SOTP/lenses → fair; changing any input recomputes everything; report builder reads update_numbers_30082026.json exclusively (no typed numeral; prior-edition comparatives read from study_numbers.json) |
| Flags raised before issue (SIGCM 8) | PASS | flagged in the document and here: MNT-BV audit qualification every period since FY24; per-leg unit-cost stacks undisclosed; round mark is press-reported (tier C), not company-stated; NP back-test small-n |
| WACC v2 (rf* normalized, both ERP bases, marginal Kd, MV weights) | PASS | build_wacc(): rf* 16.50%/19.46%; Ke 28.92%/27.84%; Kd 24.37% pre-tax marginal (sovereign+150bp; short-tenor 22.0% as sensitivity); weights MV equity 59.9% / auto debt 40.1%; WACC 24.89%/24.25%; USD cross-check run (v2 EM reminder) |
| Sweep register | PASS | SWEEP_REGISTER_UPDATE.md — every live-source attempt logged incl. two failures (worldgovernmentbonds, tradingeconomics); company ring = training SWEEP_LOG.md |
| Beta reissue closes the standing WACC re-issue item | PASS | the digest's open item "GBCO WACC predates v2 and must be re-issued" is closed by this edition: Egypt's own default spread read fresh from Damodaran (6.37% rating / 3.41% CDS, Jan-2026 vintage), rf* normalized, no rf= passed to WaccInputs |
| Dual-framing rule on the central contested judgement | PASS | MNT-Halan stake computed BOTH ways and published side by side in the document, data.js comment, and JSON (carrying EGP 12.85bn vs round mark EGP 30.20bn); never averaged — base stands on the round mark, bear on carrying |
| Training carry-ins honoured | PASS | years 3–5 revenue as ranges (×[0.61..1.40]/[0.38..1.30]/[0.41..1.12]); associates modelled explicitly; capex anchored on FS note 31 committed programme; SGA watch flag as range context, not point bump; PC volumes never frozen off a truncated window |
| External-reader scrub of the delivered document | PASS | programmatic scan of word/document.xml: zero hits on internal-procedure vocabulary; rendered layout inspected page-by-page (mammoth+Chromium render — LibreOffice broken in this container, noted) |
| Verify-by-import | PASS | compute_update.py runs end-to-end (gates would raise); node --check on data.js + app.js; data.js LOADED in node and TICKERS.GBCO.fair asserted; 90 tickers intact |
| Repo gates after the data.js edit | PASS | check_band_vocabulary OK; its negative control OK (8 defects caught); coverage_floor 93/93, 0 failures; check_technical_read advisory-only (library staleness, pre-existing) |
| No rating / no price target | PASS | fair-value ranges and framings only, in every artifact |
| Three-lens independence | PASS | nothing here feeds the MC engine or the technical read; fair{bear,base,full} is the fundamental lens only; MC cone, technicals, ledger untouched |

## OPEN — stated per flag-before-issue, queued for the full re-issue / publish pass
1. **Full model-report rebuild** (16-section Word, 16-sheet Excel, standalone bibliography,
   expert appendix at maximum depth, cell-by-cell diff): NOT claimed — assert_model_study()
   deliberately not called. This edition is a fair-value update document. GBCO's full
   rebuild to STANDARD_VERSION 2026.08.23 remains on the rebuild queue.
2. **Publish pass** (not requested): gbco.html fundamental prose (the "in plain terms" box
   still describes the 09-Jul construction), the interactive slider's factor-stack constants
   (protected — re-fitting is a full-study task), and the live fair values all update only
   on an explicit publish.
3. **MNT-Halan second closing**: stake moves 42.93% → 41.61% on completion; re-touch the
   stake leg when the company confirms.
