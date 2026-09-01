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
| 9 | TMGH | EGP | full | 147.12 | 63.76 | -56.7% | -41.6% | -59.1% | (study carries no stamp) → 2026.08.23 | L-043, L-044, L-045, L-046, L-047, L-117, L-118 |
| 37 | PHDC | EGP | full | 15.89 | 10.94 | -31.2% | -39.6% | -6.4% | 2026.08.23 → 2026.08.23 | L-028, L-029, L-030, L-114 |

Percentages are the delivered edition against the **frozen pre-campaign baseline**, captured before the run touched `assets/data.js`. Where a name carries more than one edition, `vs_previous_pct` in the JSON holds the edition-on-edition move.

