# Fundamental Analysis Calibration Register — fair-value movement

**GENERATED** by `engine/fv_movement.py` from `engine/fv_movement.json`. Never hand-edited. Rebuilt wholesale at every run.

This is the fair-value half of the register. The lessons half is `engine/Lessons_Register.md`, generated from `engine/lessons_register.py`; the two are cross-referenced by lesson id and never duplicated.

Internal record. No rating, no price target, no recommendation — a range and what moved it. Nothing here reaches the live site.

| | |
|---|---|
| covered names | 93 |
| in the campaign queue | 90 |
| excluded (metals — no issuer, no statements, no drivers) | 3 |
| baselines frozen | 12 |
| fair values re-derived | 11 |
| live study standard | 2026.09.10 |


## Egypt / EGX

| # | name | ccy | scope | old base | new base | base | bear | full | built to → | lessons |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ADIB | EGP | full | 54.3000 | 44.4610 | -18.1% | +36.6% | -51.7% | delivered 03-07-2026; no engine directory → 2026.09.10 | — |
| 2 | AMOC | EGP | full | 5.9500 | 20.0503 | +237.0% | -59.3% | +223.0% | (study carries no stamp) → 2026.09.10 | — |
| 3 | ARCC | EGP | full | 54.6500 | 77.1781 | +41.2% | -39.8% | +26.1% | (study carries no stamp) → 2026.09.10 | — |
| 4 | EGCH | EGP | full | 3.6400 | 5.0224 / 9.1288 (two-sided) | n/a | n/a | -41.0% | (study carries no stamp) → 2026.09.10 | — |
| 5 | ELEC | EGP | full | 0.3400 | 0.3229 | -5.0% | -12.3% | +0.6% | (study carries no stamp) → 2026.09.10 | L-386 |
| 6 | GBCO | EGP | full | 35.7000 | 45.7826 / 56.7795 (two-sided) | n/a | -17.2% | +11.3% | (study carries no stamp) → 2026.09.10 | — |
| 7 | PHAR | EGP | full | 61.2100 | 85.2465 / 102.8915 (two-sided) | n/a | +46.9% | +40.9% | (study carries no stamp) → 2026.09.10 | L-386 |
| 8 | SCEM | EGP | full | 53.1200 | 122.6685 | +130.9% | -52.4% | +107.6% | (study carries no stamp) → 2026.09.10 | — |
| 9 | SWDY | EGP | full | 69.7300 | 87.7633 | +25.9% | +44.3% | -3.6% | (study carries no stamp) → 2026.09.10 | L-386 |
| 36 | PHDC | EGP | full | unrecoverable | 21.0897 | n/a | n/a | n/a | 2026.08.23 → 2026.09.10 | — |
| 37 | TMGH | EGP | full | 147.1200 | 108.1943 | -26.5% | -7.7% | -25.8% | (study carries no stamp) → 2026.09.10 | — |

Percentages are the delivered edition against the **frozen pre-campaign baseline**, captured before the run touched `assets/data.js`. Where a name carries more than one edition, `vs_previous_pct` in the JSON holds the edition-on-edition move.

