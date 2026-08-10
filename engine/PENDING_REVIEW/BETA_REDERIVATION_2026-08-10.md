# BETA RE-DERIVATION — every study, against the registered index — 2026-08-10

Produced by `engine/beta_regression.py`, the shared module that resolves the regressor
through `wacc_builder.market_index_path()` and cannot be pointed at a composite.
Weekly log returns, longest window up to 5 years, Dimson lead-lag correction, usability
gate n>=24 / R2>=5% / SE(beta)<|beta|.

OLD = the equal-weight composite of covered names that every study shipped with.

| study | market/exch | old beta | old R2 | NEW beta | new R2 | n | gate | change |
|---|---|---|---|---|---|---|---|---|
| AMOC | EG/EGX | 0.94 | 0.312 | **0.908** | 0.259 | 253 | PASS | -3.4% |
| ARCC | EG/EGX | 0.628 | 0.091 | **0.698** | 0.047 | 253 | **FAIL** | +11.2% |
| EGCH | EG/EGX | 1.053 | 0.283 | **1.030** | 0.250 | 253 | PASS | -2.2% |
| ELEC | EG/EGX | 0.964 | 0.222 | **1.033** | 0.193 | 254 | PASS | +7.2% |
| PHAR | EG/EGX | 0.629 | 0.235 | **0.648** | 0.166 | 253 | PASS | +3.0% |
| SCEM | EG/EGX | 0.485 | 0.038 | **0.607** | 0.025 | 252 | **FAIL** | +25.2% |
| SWDY | EG/EGX | 1.009 | 0.291 | **1.208** | 0.376 | 254 | PASS | +19.8% |
| STC | SA/TADAWUL | — | — | **0.710** | 0.302 | 254 | PASS | n/a (none held) |
| FERTIGLB | AE/ADX | 0.492 | 0.062 | **0.931** | 0.100 | 242 | PASS | +89.3% |

## Consequences

**ARCC and SCEM lose their tier-1 beta.** Against the real EGX30 both fall below the 5%
R-squared floor (ARCC 0.047, SCEM 0.025) and the Dimson correction does not rescue either.
Under the WACC beta hierarchy they must now fall to tier 2 — a same-country EGX peer beta,
median unlevered and re-levered to target structure — or, failing that, tier 3 (beta = 1.0)
shown with the failed diagnostics. Neither may keep its composite number.

**SWDY, the model study, moves +18.9%** (1.009 -> 1.208) and its R-squared IMPROVES
0.291 -> 0.376. Its WACC, fair-value range and every beta-anchored sensitivity move with it.

**STC gains a beta for the first time** (0.710, R2 0.302 vs TASI). It previously had none,
and its WACC also predates the v2 cost-of-capital method — both corrections in one pass.

**FERTIGLB** is rebuilt in this same branch; the others each need their own build pass.

## To apply

Each study adopts its row above via `beta_regression.own_stock_beta()`, then re-runs its
own compute -> workbook -> documents -> QC chain. No study may be re-issued or rolled
forward on a composite beta.
