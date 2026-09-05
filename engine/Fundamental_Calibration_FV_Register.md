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
| 33 | AMOC | EGP | light | 5.9500 | 11.4012 | +91.6% | -59.1% | +180.6% | (study carries no stamp) → 2026.09.01 | L-082 |
| 34 | ARCC | EGP | full | 54.6500 | 66.5300 | +21.7% | -50.3% | +16.9% | (study carries no stamp) → 2026.09.01 | — |
| 35 | EGCH | EGP | full | 3.6400 | 4.0396 / 8.0388 (two-sided) | n/a | n/a | -48.0% | (study carries no stamp) → 2026.09.01 | L-326, L-330, L-331, L-332, L-333 |
| 36 | PHDC | EGP | full | unrecoverable | 17.8478 | n/a | n/a | n/a | 2026.08.23 → 2026.09.01 | L-073 |
| 37 | TMGH | EGP | full | 147.1200 | 91.8306 | -37.6% | -23.8% | -35.1% | (study carries no stamp) → 2026.09.01 | — |

Percentages are the delivered edition against the **frozen pre-campaign baseline**, captured before the run touched `assets/data.js`. Where a name carries more than one edition, `vs_previous_pct` in the JSON holds the edition-on-edition move.

