# Fundamental Analysis Calibration Register — fair-value movement

**GENERATED** by `engine/fv_movement.py` from `engine/fv_movement.json`. Never hand-edited. Rebuilt wholesale at every run.

This is the fair-value half of the register. The lessons half is `engine/Lessons_Register.md`, generated from `engine/lessons_register.py`; the two are cross-referenced by lesson id and never duplicated.

Internal record. No rating, no price target, no recommendation — a range and what moved it. Nothing here reaches the live site.

| | |
|---|---|
| covered names | 93 |
| in the campaign queue | 90 |
| excluded (metals — no issuer, no statements, no drivers) | 3 |
| baselines frozen | 2 |
| fair values re-derived | 2 |
| live study standard | 2026.08.23 |


## Egypt / EGX

| # | name | ccy | scope | old base | new base | base | bear | full | built to → | lessons |
|---|---|---|---|---|---|---|---|---|---|---|
| 36 | ARCC | EGP | full | 54.65 | 50.2 | -8.1% | -7.9% | -8.7% | (study carries no stamp) → 2026.08.23 | L-034, L-035, L-115, L-206 |
| 37 | PHDC | EGP | full | unrecoverable | 15.89 | n/a | n/a | n/a | 2026.08.23 → 2026.08.23 | L-028, L-029, L-030, L-114 |

## Editions and corrections

A name with more than one edition shows every one. Nothing is overwritten: a superseded number stays on the record with the reason it was superseded, the same append-only discipline the ledgers keep.

**ARCC**

| edition | delivered | bear | base | full | note |
|---|---|---|---|---|---|
| 1 | 2026-09-01 | 31.39 | 53.17 | 70.02 | — |
| 2 | 2026-09-01 | 45.63 | 50.2 | 56.37 | SUPERSEDES EDITION 1, which was recorded from a leaner interim valuation written during this run before the study's own established build was re-run. Edition 2 is the authoritative one: engine/arcc_study/compute.py revision 4, which passes its own 23 assertions — among them that the unit build reproduces AUDITED FY2025 revenue and EBITDA to +0.000% and every disclosed tonne to within 0.012%. The substantive change against the pre-campaign baseline is the BETA: the study carried 0.6281 regressed against an equal-weight composite of the covered EGX names, which is a hard fail under SIGCM clause 6. Re-derived through beta_regression.own_stock_beta against the published EGX30, the own-stock fit returns 0.6981 with R2 0.047 and FAILS the usability gate, so the strict preference order falls to a tier-2 same-country peer median of 1.0302. That single correction carries Ke from about 25.2% to 29.24% and the centre from 54.65 to 50.20. |

Percentages are the delivered edition against the **frozen pre-campaign baseline**, captured before the run touched `assets/data.js`. Where a name carries more than one edition, `vs_previous_pct` in the JSON holds the edition-on-edition move.

