# Fundamental Analysis Calibration Register — fair-value movement

**GENERATED** by `engine/fv_movement.py` from `engine/fv_movement.json`. Never hand-edited. Rebuilt wholesale at every run.

This is the fair-value half of the register. The lessons half is `engine/Lessons_Register.md`, generated from `engine/lessons_register.py`; the two are cross-referenced by lesson id and never duplicated.

Internal record. No rating, no price target, no recommendation — a range and what moved it. Nothing here reaches the live site.

| | |
|---|---|
| covered names | 93 |
| in the campaign queue | 90 |
| excluded (metals — no issuer, no statements, no drivers) | 3 |
| baselines frozen | 5 |
| fair values re-derived | 5 |
| live study standard | 2026.09.01 |


## Egypt / EGX

| # | name | ccy | scope | old base | new base | base | bear | full | built to → | lessons |
|---|---|---|---|---|---|---|---|---|---|---|
| 33 | AMOC | EGP | light | 5.95 | 8.64 | +45.2% | +35.2% | +46.5% | (study carries no stamp) → 2026.09.01 | L-048, L-049, L-050, L-051, L-052, L-053, L-054, L-119 |
| 34 | ARCC | EGP | full | 54.65 | 54.1 | -1.0% | -1.6% | -3.5% | (study carries no stamp) → 2026.09.01 | L-057, L-058, L-059, L-060, L-061, L-120 |
| 35 | EGCH | EGP | full | 3.64 | 3.76 | +3.3% | n/a | +0.0% | (study carries no stamp) → 2026.09.01 | L-064, L-065, L-206, L-207 |
| 36 | PHDC | EGP | full | unrecoverable | 10.9412 | n/a | n/a | n/a | 2026.08.23 → 2026.09.01 | L-028, L-029, L-030, L-114 |
| 37 | TMGH | EGP | full | 147.12 | 69.92 | -52.5% | -43.7% | -48.2% | (study carries no stamp) → 2026.09.01 | — |

Percentages are the delivered edition against the **frozen pre-campaign baseline**, captured before the run touched `assets/data.js`. Where a name carries more than one edition, `vs_previous_pct` in the JSON holds the edition-on-edition move.

