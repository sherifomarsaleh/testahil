# What the framework catches, and what it does not

Measured 07-09-2026, on the principal's three named errors. Every figure below is read
from a committed artefact in this repository, not estimated.

## The scorecard on the three errors named

| the error, in the principal's words | caught? | by what |
|---|---|---|
| "erroneous fair values that are 60% of the current prices in a wrong way" | **YES** | `check_valuation_gap` (audit, 8 headings) + `check_publish_block` (holds it) |
| "takes into consideration current landbank of a developer but does not account for new land added" | **NO** | nothing — see §1 |
| "creates wrong cost or high Ke and Kd" | **PARTLY** | the *construction* is gated; the *level* is not — see §2 |

## §1 — THE ASSET BASE HAS NO FRESHNESS RULE, AND ONE STUDY IS 21 MONTHS STALE ON IT

`landbank` — in any spelling — appears in **zero** gates and in **zero** governing
documents. Searched: `scripts/`, `engine/*.py`, both governing documents, for
`landbank | land bank | land_bank`. The only hit anywhere is a fixture string inside
`check_lens_design_negative_control.py`.

Measured on the two developers in the book:

| | quantity | its date | study edition | information set | bridge sheet |
|---|---|---|---|---|---|
| **PHDC** | `land_bank_sqm_mn` = 33.0 | **2024-12-31** | 2026-09-02 | 1Q2026 | 2026-03-31 |
| TMGH | `landbank_msqm` = 20.0 | 1H 2026 release | 2026-09-02 | 1H2026 | — |

PHDC's land base is sourced to the **FY2024 earnings release** and carried into a study
whose every other input is held to a freshness discipline and whose bridge stands on a
31-March-2026 balance sheet. It is not decorative: `build_xlsx_phdc.py:336` prints it to
the delivered workbook as "Land bank (mn sqm)".

**Why no gate sees it.** `[R-BRIDGE-01]` requires the *balance sheet* to be the latest
disclosed one and is enforced by `check_bridge.py`. Nothing states the same of the
**operating asset base** — the land, the fleet, the kilns, the keys, the connected
capacity — which is what a developer's or an asset-owner's value actually rests on. The
rule was written about one balance sheet and the quantity that matters here sits beside it.

This is `[R-BRIDGE-01]`'s own general lesson arriving one object over: where a
construction can be recorded as a set of choices, record the choices and check those.

## §2 — THE COST OF EQUITY IS NEVER REPRODUCED FROM ITS OWN INPUTS

`check_cost_of_capital.py` enforces a great deal: the sovereign counted exactly once, Kd
above its own sovereign, market-value weights, the glide, `WACC_TERM < WACC_EXP`, the
three-assert Kd gate, the 150bp bound and its re-pointing. **It does not reproduce Ke.**

Searched all of `scripts/*.py` for `ke_exp | cost_of_equity | ke_terminal | capm |
rf_star +` — **no file matches**. `check_cost_of_capital.py` reads `rf_star` once, at
line 134, to check the *risk-free normalisation* identity, and never the CAPM one.

The identity holds on ARCC and nothing established that:

    rf_star + beta x erp  =  0.195500 + 0.9275221 x 0.0941  =  0.282780
    committed ke_exp                                        =  0.282780

**What that is worth, on ARCC's own committed sensitivity grids:**

- +300bp on the explicit WACC alone: 66.53 -> 64.45, **-3.1%**
- beta 0.80 -> 1.15, both well inside the study's own confidence interval:
  70.35 -> 59.24, **-16%**
- the study's own 95% beta interval, 0.2505 to 1.1457:
  **fair value 102.54 to 59.35** — a **73% spread**, against a published central of
  66.53 and a spot of 77.00

So the single input with the widest committed uncertainty in the model is the one input
whose arithmetic no gate reproduces. A Ke typed 300bp high, or a beta taken from the
wrong window, passes every check in this repository.

## What this says about where the effort belongs

The framework is not missing. `check_new_study_gauntlet.py` run 07-09-2026:
**38 of 38 gates refuse a new study** — every directory gate by name, every artefact gate
on a planted offender, with 14 exclusions each carrying a stated reason.

Two things are wrong with it and neither is the ratchet debt:

1. **Uncovered classes**, of which the asset base is one and the Ke level is another.
2. **Reach**: 66 of the 90 published fair values have no study directory, and every
   construction gate globs `engine/*_study/`. They are outside all of it.

The 47 ratchet entries on the five re-issued names are debt on five old studies. Clearing
them turns one acceptance criterion green and protects no future study, because a ratchet
excuses a listed name and binds on everything else. That work is deprioritised here, and
saying so is the point rather than quietly dropping it.
