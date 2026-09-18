# The mechanical lens never checked that its explicit window converged

**18 September 2026. Measured, not argued. Nothing here moves a fair value.**

## What was found

The mechanical cash-flow lens — [R-VCAL-01] series (a), the instrument criterion 3
clause A is computed on — builds a value at each past origin from a run's own
pre-registered projection and capitalises the last explicit year into a terminal.

**It never checked that the projection had converged to the terminal.**

[R-MACRO-01], adopted 02 September 2026 — four days *before* the declaration that
sealed this construction — says in its own words:

> THE EXPLICIT WINDOW RUNS UNTIL GROWTH IS WITHIN 2pp OF TERMINAL: a model whose
> last explicit year still grows far above its terminal capitalises a rate it
> never reached.

Measured on every cell the lens had ever scored:

| cell | growth at the last explicit year | terminal | gap | terminal share of EV |
|---|---|---|---|---|
| PHAR 2023 | 22.1% | 9.5% | 12.6pp | **1820%** |
| PHDC 2017 | 21.4% | 7.0% | 14.5pp | 102% |
| PHDC 2018 | 22.6% | 7.0% | 15.6pp | 125% |
| PHDC 2019 | 20.7% | 7.1% | 13.6pp | 108% |
| PHDC 2020 | 12.1% | 8.2% | 3.8pp | 102% |
| PHDC 2021 | 11.6% | 7.1% | 4.5pp | 109% |
| PHDC 2022 | 13.9% | 7.0% | 6.9pp | 62% |

**All seven breached it.** The smallest gap is 3.8pp against a bound of 2pp; the
largest is 15.6pp. Six of the seven carry a terminal worth **more than the whole
enterprise value**, which is another way of saying the explicit window contributes
nothing or less: PHDC 2019's five explicit years have a present value of
**−EGP 2.28bn** against a terminal of +EGP 32.52bn.

The mechanism is not obscure. A developer's working capital runs at 169% of
revenue, so a path compounding at 21% a year consumes 1.69 × ΔRevenue in cash
every year and free cash flow is negative throughout the window. The terminal
then charges working capital at inflation alone, because real growth there is
zero — which is correct *for a terminal*, and is a different economy from the one
the explicit window just described. The value is entirely a capitalisation of a
NOPAT level reached by growing at a rate the model then abandons.

## What was done

`cashflow_lens.cell()` now refuses a cell whose last explicit year sits more than
`research_protocol.HORIZON_CONVERGENCE` from the terminal nominal growth rate.

Three things about that refusal:

- **The bound is imported, never typed.** `HORIZON_CONVERGENCE` is the figure
  `assert_macro_coherence()` already holds every study to. Minting a second one
  for a scorer would be the free parameter the promotion rule forbids, and would
  let two instruments disagree about what a converged window is.
- **The reading is two-sided**, matching the study gate exactly. AMOC 2023 ends
  at 0.0% nominal against a terminal of 9.5% — converged to something *below*
  terminal, which is the perpetual-real-decline half of the same rule.
- **It is a refusal, not a fade.** Growing the path down to the terminal inside
  the lens would be the lens choosing a construction, which its own docstring
  forbids, and would need a fade rate nobody has tested. A window that does not
  converge is work owed by **the run**, whose projection it is.

## What it costs, stated rather than discovered later

The declared run goes to **zero admissible cells**, from five.

Criterion 3 clause A therefore moves from **NOT MET** to **UNMEASURED**, and
clauses B, C and F with it. That is not a softening. A verdict of NOT MET reached
on five cells built on a construction the house forbids is a false verdict; no
verdict on no admissible evidence is the true one. Phase 1 does not close either
way, so **no publish decision changes and no fair value moves**. What changes is
what the record says about why.

Three instruments had to be corrected to report this state at all, and each was a
small instance of the same species:

1. `criterion3.clause_a` **crashed** on an empty series rather than reporting it.
2. Its verdict line collapsed `None` onto NOT MET — three states printed as two,
   in the one clause that gates Phase 1 hardest. B and C already printed all three.
3. `score_cashflow.report()` printed `WHY 28 OF 33 READY CELLS` as a **typed
   literal**, and went on printing it after the population had moved twice. The
   standing rule "a number stated in prose must be computed, not typed" has been
   in force since 07 August 2026, and this was in the calibration's own reporter.
4. Its drop taxonomy filed the new refusal under `other`, where 21 of 58 drops —
   the largest single cause in the table — would have been invisible.
5. The narrative under the blocking table asserted "the largest class is a
   DATA-CARRY job" as prose beside a computed table. It is now **selected by the
   table**. The reading it had been carrying was the comfortable one: work with a
   rate, owed by nobody's method.

## Negative-controlled, and the control caught its own first draft

`scripts/check_convergence_refusal_negative_control.py` reinjects the condition on
eight cases — four red (20pp above the terminal, 2.1pp above it, far below it, and
PHDC's own 21.4%-against-7.0% shape) and four clean (exactly at the terminal, 1.9pp
either side of it, and the bound being the house's rather than a copy). It writes
nothing: every mutation is to an in-memory projector in a process that then exits.

**Its first draft proved nothing and that is recorded rather than quietly fixed.**
It selected its fixture cell by asking only whether a projection was reachable, and
picked one that dies several checks earlier on an incomplete valuation-input block.
All four red cases came back quiet — correctly, the refusal never being reached —
and **all three clean cases passed for exactly the same reason**. That is the fifth
time in this project a control has been caught passing a fixture that never injected
its condition, and the only thing that exposed it here was that the red half failed
loudly first. The fixture is now selected by running the real `cell()` and keeping
one whose outcome is decided *at* the convergence check.

## Why this matters more than the five cells it removed

The plan for this calibration set out to add names until the pool was large
enough to answer clause A. Nine names were queued. **Wiring more projectors would
have added more non-converged cells**, because the defect is in the construction
rather than in any name: the 21 refusals span six names — AMOC, ARCC, EGCH, PHAR,
PHDC, TMGH — and it is now the largest drop class in the run.

A larger pool of inadmissible cells is not closer to an answer than a small one.

This is also the first live evidence bearing on [R-VCAL-01]'s own stated
falsifier — *"if the mechanically rebuilt series turns out not to resemble the
as-delivered one … this calibration is grading a method the house does not
use"*. PHDC as delivered publishes a central of 17.85. The mechanical series
produced 6.08, 2.49, 8.81, 6.37, 6.46 and 7.51 at its six origins, every one on a
window the house's own rules forbid. That is not yet the falsifier firing — the
falsifier speaks of a long record — but it is the shape of it, and it is written
down here so the comparison does not have to be remembered.

## What would close it

Not a fade, and not a wider bound. The runs' own projections must reach a year
where growth has converged, which is a change to the pre-registered window of
each run and belongs in that run's next pass. Until one does, clause A has no
admissible cell and says so.

**The general lesson, which is not about convergence:** a rule adopted four days
before an instrument was built did not reach it, because the instrument was not a
study and every gate for that rule was pointed at studies. Where a rule governs a
*construction*, ask what else in the repository performs that construction.
