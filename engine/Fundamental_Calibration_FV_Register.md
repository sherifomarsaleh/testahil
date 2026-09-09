# Fundamental Analysis Calibration Register — fair-value movement

**GENERATED** by `engine/fv_movement.py` from `engine/fv_movement.json`. Never hand-edited. Rebuilt wholesale at every run.

This is the fair-value half of the register. The lessons half is `engine/Lessons_Register.md`, generated from `engine/lessons_register.py`; the two are cross-referenced by lesson id and never duplicated.

Internal record. No rating, no price target, no recommendation — a range and what moved it. Nothing here reaches the live site.

| | |
|---|---|
| covered names | 93 |
| in the campaign queue | 90 |
| excluded (metals — no issuer, no statements, no drivers) | 3 |
| baselines frozen | 11 |
| fair values re-derived | 10 |
| live study standard | 2026.09.07 |


## Egypt / EGX

| # | name | ccy | scope | old base | new base | base | bear | full | built to → | lessons |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | AMOC | EGP | full | 5.9500 | 17.6329 | +196.4% | -59.1% | +180.8% | (study carries no stamp) → 2026.09.07 | — |
| 2 | ARCC | EGP | full | 54.6500 | 66.5300 | +21.7% | -50.3% | +16.9% | (study carries no stamp) → 2026.09.07 | — |
| 3 | EGCH | EGP | full | 3.6400 | 4.0396 / 8.0388 (two-sided) | n/a | n/a | -48.0% | (study carries no stamp) → 2026.09.07 | L-326, L-330, L-331, L-332, L-333 |
| 4 | ELEC | EGP | skip | 0.3400 | 0.3357 | -1.3% | +1.4% | -0.1% | (study carries no stamp) → 2026.09.07 | — |
| 5 | GBCO | EGP | full | 35.7000 | 41.3484 / 52.3453 (two-sided) | n/a | -17.2% | +2.6% | (study carries no stamp) → 2026.09.07 | — |
| 6 | PHAR | EGP | full | 61.2100 | 31.3738 / 47.6035 (two-sided) | n/a | -45.9% | -34.8% | (study carries no stamp) → 2026.09.07 | — |
| 7 | PHDC | EGP | full | unrecoverable | 17.8617 | n/a | n/a | n/a | 2026.08.23 → 2026.09.07 | — |
| 8 | SCEM | EGP | light | 53.1200 | 111.6213 | +110.1% | -42.1% | +88.9% | (study carries no stamp) → 2026.09.07 | L-367, L-368, L-369 |
| 9 | SWDY | EGP | full | 69.7300 | 43.5108 | -37.6% | -18.9% | -39.6% | (study carries no stamp) → 2026.09.07 | — |
| 10 | TMGH | EGP | full | 147.1200 | 91.9728 | -37.5% | -23.7% | -35.0% | (study carries no stamp) → 2026.09.07 | — |

Percentages are the delivered edition against the **frozen pre-campaign baseline**, captured before the run touched `assets/data.js`. Where a name carries more than one edition, `vs_previous_pct` in the JSON holds the edition-on-edition move.

