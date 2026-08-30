# GBCO fundamental walk-forward training — PRE-REGISTRATION

**Ticker:** GBCO (GB Corp S.A.E., EGX) · **Market:** EG · **Written:** 30-Aug-2026, BEFORE any
forecast error was computed. Committed to the training branch before `bottom_up.py` first ran.
The du reference run named in the training prompt (du_panel.py / bottom_up.py /
du_IS_projected_vs_actual_all_origins.md, 30-Aug-2026) is **not present in this repository on any
branch** (searched every remote ref); structure below follows the training prompt's own
specification directly, with the same file naming.

## 0. Panel and point-in-time convention

- Panel: FY2011–FY2025 annual consolidated actuals + H1-2026, all four-field sourced
  (value, source, date, tier). Fiscal year = calendar year.
- Origin = 30 April of year Y (by then FY Y-1 annual results are always published: GB files
  its 4Q earnings release and audited FS in late February / early March).
- Origin Y sees: company figures for FY ≤ Y-1 **as originally reported** (not as later
  restated); macro (CPI, FX) through calendar Y-1; Egypt market volumes through Y-1 as
  quoted in company documents published by the origin date.
- Origins: 2016, 2017, …, 2025 (first origin = first year with a 5-year panel history,
  2011–2015). Origin 2026 is the live origin carried into the current update; it is not scored.
- Horizons: h1–h5 = FY Y … FY Y+4. Scored where the actual has resolved (≤ FY2025):
  h1 has 10 scored origins (2016–2025), h2 has 9, h3 has 8, h4 has 7, h5 has 6.

## 1. Driver list by class and the mechanical rule for each

No judgement inputs at historical origins — the method is tested, not the analyst. All
trailing statistics use the last 3 resolved fiscal years visible at the origin ("t3");
CAGRs use endpoints of that 3-year window. Parameters below are **stated, not fitted**;
the named sensitivities are **reported, never selected**.

**Exogenous inputs (macro/regulatory), fixed at origin:**
- π (inflation path): t3 average of Egypt CPI inflation (World Bank/CAPMAS series as known
  at origin, i.e. through Y-1), held flat over h1–h5.
- d (EGP/USD depreciation path): t3 average annual depreciation of the EGP/USD
  period-average rate, held flat. Sensitivity reported: d = 0 (freeze FX).
- M (Egypt PC market volume): last market volume quoted in company documents published by
  the origin date, grown at the market's own t3 CAGR. Where no market figure is quotable at
  an origin, the fallback (flagged per-origin) is GB's own segment-volume t3 CAGR.
- Tax regime: statutory rate as in force at origin (22.5% from FY2015 era onward; earlier
  rates as disclosed in the FS of the era).

**Company drivers:**

| class | driver | mechanical rule at origin | stated parameters (sensitivity reported) |
|---|---|---|---|
| units | PC volume (Egypt; from FY2024 basis Egypt+Iraq+Jordan combined, per break register) | share × market: share = last actual share where market quotable, else volume t3 CAGR | — |
| units | Motorcycles & 3W volume; CV&CE volume | own t3 CAGR (no reliable external market series at most origins; flagged company-trend) | — |
| price | ASP per segment (revenue ÷ units) | ASP × (1 + π + 0.5·d) per year | FX pass-through 0.5 (0.25 / 0.75) |
| cost/unit | unit cost per volume segment (segment COGS ÷ units); non-volume revenue COGS ratio | unit cost × (1 + π + 0.75·d) per year; non-volume COGS ratio frozen at last actual | pass-through 0.75 (0.5 / 1.0) — imported content is costlier in FX than the price side can recover |
| non-volume revenue | tires+after-sales+trading; regional (where separate); financing (GB Capital) revenue | each line's own t3 CAGR; financing flagged company-trend (portfolio series does not exist at older origins) | — |
| overheads | SG&A (S&M + G&A) | φ fixed share escalated at (1+π), (1−φ) share scaled with revenue growth | φ = 0.5 (0.3 / 0.7) |
| D&A | depreciation & amortization | PP&E roll-forward: PPE_t = PPE_{t−1} + capex_t − D&A_t; D&A_t = δ·PPE_{t−1} + capex_t·δ/2, δ = t3 average D&A / opening PP&E | — |
| capex | capital expenditure | t3 average capex/revenue × forecast revenue (an input driving volume capacity and D&A, not an output) | — |
| interest | net finance cost | effective rate i = last actual net finance cost ÷ average total debt, held flat; applied to modelled average debt | — |
| debt | total debt | rolls with the modelled cash shortfall/surplus: debt_t = debt_{t−1} + max(0, −FCF_t) − min(debt reduction, max(0, FCF_t)) | — |
| associates | share of associates' results | frozen at last actual (no visibility into associate book at origin) | — |
| tax | effective tax rate | t3 average effective rate (tax ÷ PBT over positive-PBT years); if no positive-PBT year in window, statutory rate | — |
| working capital | DIO, DSO, DPO | t3 averages, applied to forecast COGS / revenue → inventory, receivables, payables → ΔWC | — |
| one-offs | disclosed non-recurring items | never forecast (zero at every origin); actuals are scored both as-reported and with registered one-offs removed | — |

Aggregation: segment revenues = units × ASP (+ non-volume lines); COGS = units × unit cost
(+ ratio lines); GP; SG&A; other operating income frozen at last actual share of revenue;
OP; net finance; associates; PBT; tax; NP (total). BS/CF: inventory, receivables, payables
from the cycle; PP&E from the roll-forward; debt from the schedule; CFO ≈ NP + D&A − ΔWC.

## 2. Naive benchmarks

- **freeze**: every scored line flat at its last actual.
- **trend**: every scored line at its own t3 CAGR (line ≤ 0 anywhere in the window → freeze
  that line).

## 3. Score

- Per driver and per aggregate line, per horizon: log error e = ln(F/A) where F, A > 0;
  where either side is ≤ 0 (possible for NP), the scaled error (F − A)/|A_origin last
  actual| is used and the case is flagged. Bias = mean e; MAE = mean |e|.
- Block bootstrap over origins: moving blocks of length 3, 2,000 resamples, 5–95% CI on bias.
- Share of origins over/under; sign by era. Eras: E1 2016–2019 (float and recovery),
  E2 2020–2021 (COVID), E3 2022–2024 (devaluation/import crisis), E4 2025– (recovery).
- Decomposition: revenue error into volume/price/mix by segment; NP error into GP, SG&A,
  finance cost, associates, tax, one-offs.
- Macro vs company split: re-run every origin with realized π, d, and market volume in
  place of their forecast paths; the error that survives is the company component,
  the difference is the macro component.
- Skill vs freeze and trend at every horizon: 1 − MAE_model/MAE_naive.

## 4. Learning rule (set before scoring)

- Expanding window: a correction proposed at origin Y uses only errors from origins whose
  scored horizon resolved before Y.
- Correction per driver: multiply the driver's growth factor by exp(−λ · median bias),
  λ = 0.5 (half strength).
- Eligibility: bias sign consistent across all eras that contain ≥ 2 resolved
  observations of that driver; reset (drop the correction) after a structural break,
  defined as a driver error beyond 2σ of its own resolved history.
- Test: rebuild aggregates from corrected drivers at the origins that had a correction
  active; report corrected vs raw per origin. A correction is carried into the live 2026
  update only if it improves MAE on those origins AND is consistent with the same driver
  class across the market's book; otherwise it is recorded as a watch flag.
- Guidance ledger: management's stated expectations (AR/ER outlook sections) vs outcome,
  per year; its bias is recorded but never used as a driver at historical origins.

## 5. Sample roles

The rolling record (all origins) **estimates** corrections; the non-overlapping origin
subsets **confirm** them: h1 all origins are non-overlapping; h3 confirmation set
{2016, 2019, 2022}; h5 confirmation set {2016, 2021}. A correction that helps on the
rolling record but not on the non-overlapping subset is a watch flag, not a correction.

## 6. Deliverables bound to this pre-registration

gbco_panel.py (+ panel JSON with per-figure provenance), BASIS_BREAKS.md, bottom_up.py,
errors tables (CSV), GBCO_IS_projected_vs_actual_all_origins.md, corrections + tests,
TRAINING_RECORD.md with caveats, Fundamental Driver Ledger entry. Nothing here is
published; no rating, target, or buy/sell language anywhere.
