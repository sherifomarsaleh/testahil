# Beta re-issue prompt — canonical text

Paste this into a fresh session, replacing `{TICKER}`. It re-derives one study's beta
against the published index of its own exchange and rebuilds the study and workbook on it.

Adopted 10-Aug-2026, after the discovery that every study in the repo — SWDY, the model
study, included — had regressed against an equal-weight composite of the covered names.

---

## THE PROMPT

> Re-derive the beta for **{TICKER}** against the published index of the exchange it is
> listed on, then reproduce the valuation study and the Excel model on the corrected
> number. Follow the standing protocol; this is not a new study and not a roll-forward.
>
> **1 — Read the live rules first.** `engine/PROJECT_INSTRUCTIONS_11-07-2026.md` and the
> BETA section of `engine/Standing_Research_Protocol.md`. Do not work from memory of them.
>
> **2 — Resolve the regressor, do not choose it.** Read the ticker's exchange from its
> `code` prefix in `assets/data.js` (`ADX:`, `DFM:`, `EGX:`, `TADAWUL:`, `QSE:`, `KRX:`,
> `NSE:`, `NASDAQ:`) — never infer it from the `raw_ohlc/{MARKET}/` folder, which groups by
> market code and mixes exchanges. Then call
> `engine.beta_regression.own_stock_beta(ticker, market, exchange)`.
> It resolves the index through `wacc_builder.market_index_path()`, runs Step 0.0 on both
> series, and matches the weekly grid to that exchange's real trading week.
> **Do not write a study-local beta script. Do not build a composite of covered names.**
> If the index is not registered, STOP AND ASK for it — do not substitute anything.
>
> **3 — Gate it.** Call `research_protocol.assert_beta_provenance()` on the record. If the
> fit fails the usability gate (n≥24, R²≥5%, SE(β)<|β|), do NOT keep the old number: fall to
> tier 2, a same-country peer beta re-levered to target structure, or tier 3, β = 1.0 shown
> with the failed diagnostics. Say which tier you landed on and why.
> If the regressor is an interim substitution, quote `index_interim_note()` in the study.
>
> **4 — Rebuild the whole chain, in order**, never editing a delivered file by hand:
> `beta_reg.py` → `compute.py` → `figures.py` → `build_xlsx_*.py` → `docx_*.py` →
> `docx_biblio.py` → `engine/make_pdf.py`.
>
> **5 — Hunt the stale prose.** The number propagates automatically; the words describing it
> do not. Grep every builder for `composite`, for the old beta value, and for any hardcoded
> description of the regressor, and drive those strings off the beta record instead of
> retyping them. On FERTIGLB the source line still read *"equal-weight ADX/DFM composite
> built from the 17-name UAE price library"* while the model already carried the index beta —
> a false provenance statement that would have shipped in the study and the bibliography.
>
> **6 — Re-run every gate and show me the output**: `gate_checks.py`, `check_figures.py`,
> `recalc.py`, `driver_test.py`, `qc_checks.py`. Then render the PDFs and **read them** —
> at minimum the valuation-summary page and the cost-of-capital page.
>
> **7 — Report before and after**: beta, R², WACC, each lens, the weighted centre, both
> framings, and the terminal-value share. State plainly if the conclusion changed direction.
>
> **8 — Verify by import, not by parse**, and commit on a feature branch with an open PR.
> Never push protocol or engine changes straight to main.

---

## WHAT GOOD LOOKS LIKE

The FERTIGLB pass, 10-Aug-2026, as the worked precedent:

| | before | after |
|---|---|---|
| regressor | 17-name equal-weight ADX/DFM composite | FTSE ADX General (`raw_indices/AE/FADGI.csv`) |
| beta | 0.492 | **0.931** |
| R² | 0.062 | **0.100** |
| WACC | 8.53% | **11.90%** |
| weighted centre | AED 2.74 | **AED 2.15** |
| framings A / B | 2.60 / 3.95 | **1.76 / 2.62** |
| terminal share | 66.2% | **55.2%** |

Against a spot of AED 2.54 the conclusion **inverted** — from a 7.8% discount to fully
priced. A beta correction is not cosmetic; say so when it moves the answer.

## STUDIES STILL OWED THIS PASS

`PENDING_REVIEW/BETA_REDERIVATION_2026-08-10.md` holds every re-derived number.
AMOC, ARCC, EGCH, ELEC, PHAR, SCEM, SWDY and STC each need their own rebuild.
**ARCC and SCEM fail the gate outright** against the real index and must go to tier 2 or 3.
**SWDY is the model study and moves +19.8%**, so its rebuild changes the reference every
other study is matched against.
