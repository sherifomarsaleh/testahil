# GBCO study — source

The exact scripts that produced `GBCO_Valuation_Study_08-07-2026_public.docx` and
`GBCO_Valuation_Model_08072026_public.xlsx` (files/ in the repo root), including the
09-07-2026 corrections: the MNT-Halan stake (unsourced ~20% → confirmed 41.61%, GB Corp's
own 9-Jun-2026 press release) and the bottom-up WACC rebuild (rf/ERP sourced from primary
data, beta=1.0 per a genuinely-attempted-then-rejected regression, WACC 22.94%/25.08%).

**Reconciled and verified end-to-end, 09-07-2026.** `build_xlsx.py` → `build_xlsx4.py`,
run in sequence from scratch, reproduce `GBCO_Valuation_Model_08072026_public.xlsx`
**exactly** — every cell, every formula, every annotation, checked programmatically
against the delivered file with zero discrepancies (0 formula errors, 0 numeric diffs,
0 text diffs across all 16 sheets). This was not true earlier the same day: an initial
audit found a circular SOTP formula (`=SUM(C7:C9)`, self-referencing), an orphaned
duplicate row in Segments, six stale forecast-driver arrays (Associates income,
borrowings, Group opex, and three Balance Sheet working-capital drivers) that had
drifted from the live file via one-off patches never folded back into the scripts, and
a set of Assumptions-sheet annotations shifted one row from their intended target. All
fixed; the reconciliation process (diff the fresh build against the verified file,
cell-by-cell, not just "does it run without error") is worth repeating for any future
study built the same way — a clean recalc with zero formula errors is necessary but
not sufficient proof that a rebuilt file matches the one actually delivered.

**This is a worked example, not a generic multi-ticker engine.** Every file here is
hardcoded to GBCO — its own historical financials, its own MNT-Halan stake, its own
forecast drivers. Building the next study means copying the *pattern* (Step 0 → §1
fundamental build → DCF → SOTP → Monte Carlo → docx/xlsx render → QC gate), not running
these files unmodified against a new ticker.

## Files, in the order they run
0. `GB_AUTO_Stock_Price_History.csv` — the raw daily OHLC input (3 Jan 2021 → 7 Jul 2026,
   1,334 rows, spot 31.25 on the last row). Everything downstream depends on this; it was
   never saved anywhere before 09-07-2026 and would have been unrecoverable if the working
   sandbox had been discarded.
1. `compute.py` — the master computation: Step 0 backtest, MC engine call, DCF, SOTP,
   relative/normalized lenses, expert panel figures, sensitivity grids. Writes
   `study_numbers.json`, the single source of truth every other script reads from.
2. `figures.py` — all 8 study figures (football field, sensitivity heatmap, MA-stack,
   fan chart, two distributions, calibration 3-panel, expert ranges), reading
   `study_numbers.json`.
3. `docx_base.py` + `docx_A.py` / `docx_B.py` / `docx_C.py` — the Word study, built as
   three sequential imports sharing one `docx_base.doc` object (masthead → §1–2;
   §3 Monte Carlo → §7 caveats; Appendices A–D → disclosure).
4. `build_xlsx.py` → `build_xlsx4.py` — the 16-sheet Excel model, built in four passes
   (Assumptions/READ FIRST → Segments/DCF → IS/BS/CF → SOTP/Summary/Sensitivity/etc.),
   each script loading and re-saving the same `.xlsx`. Verified byte-for-byte equivalent
   in output to the delivered `GBCO_Valuation_Model_08072026_public.xlsx` (also included
   in this folder) — see the reconciliation note above.

## Data files also included
- `study_numbers.json` — the actual computed output `compute.py` produced for the
  delivered study (saved directly, not just left to be regenerated, in case any future
  library-version drift in numpy/mc_v2 ever produces a slightly different result on rerun).
- `backtest_rows.csv` — the 17 Step 0 non-overlapping backtest origins/results.
- `GBCO_Valuation_Model_08072026_public.xlsx` — the verified, delivered model, included
  here alongside its source so the two can be diffed against each other directly if the
  scripts are ever modified again.

## Dependency on the parent `engine/` folder
`compute.py` imports `mc_v2` and `wacc_builder` as sibling modules — both actually live
one level up, at `engine/mc_v2.py` and `engine/wacc_builder.py`, not inside this folder.
To run `compute.py` as-is: copy (or symlink) those two files into this directory first,
or add the parent `engine/` directory to `PYTHONPATH` before running. They were kept
canonical in `engine/` rather than duplicated here so there is exactly one copy of each
to keep current.

## What this does NOT include
Step 2 (pulling historical financials via web research) and the Step 4 expert-appendix
authoring happened as part of the conversation that produced this study, not as code —
there is no script here that does either. `compute.py` takes the already-researched
figures as hardcoded inputs.
