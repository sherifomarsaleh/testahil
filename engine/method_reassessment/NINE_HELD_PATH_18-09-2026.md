# The nine held on the method — what actually blocks them, measured

**18 September 2026.** Read live: **4 studies may publish, 10 are held because the
central sits more than 10% below the latest price, 9 are held on the method and on
nothing else, 1 is unreadable.**

The nine are inside the publication band and carry no unfiled dissent. The only thing
between them and a reader is Part E criterion 3.

## What criterion 3 needs, and what it has

Per `[R-VCAL-02]`, clauses A, B, C and F gate Phase 1; D and E are Phase 2b's subject
and hold nothing. On the mechanical series today:

| clause | state | why |
|---|---|---|
| A — pooled contemporaneous bias covers zero | NOT MET | 5 cells, 5 origins, **1 name** |
| B — LONO-stable in sign | UNMEASURED | one name: leaving one out leaves nothing to pool |
| C — holds in both eras | UNMEASURED | one era populated |
| F — residual bias attributed to a named lever | follows A | — |

**One name is the whole blocker**, and it is not a data-availability fact. The
valuation-input census now reaches **104 of 110 cells across ten names** — 56 with a
complete bridge and a capex figure, 48 more where capex derives by the identity. The
inputs are carried. What is missing is the wiring that turns them into a value.

## The drops, tallied

| cells | reason | kind |
|---:|---|---|
| 17 | **no projector wired for this name** — PHAR, SCEM, SWDY | code |
| 8 | no quantity appears in both the run's panel and its valuation-input block | code |
| 9 | capex intensity needs 3 years and the block carries 1 or 2 | data |
| 13 | terminal refused — negative terminal cash flow, or payout outside [0,1] | **the module being right** |
| 2 | no finance charge in the as-reported panel at this origin | data |
| 1 | the projection has no revenue or operating profit at h=1 | data |
| 1 | `TypeError` | a bug |

**The largest class is code, not research.** A projector is a per-name adapter from a
run's own committed projection to the three quantities the lens needs — revenue,
operating profit, depreciation. Seventeen cells and three names are waiting on one.

## The population was always meant to include them

The sealed pre-registration says, in terms:

> **FULL** on the names with parsed statements: AMOC, ARCC, EGCH, PHDC, TMGH, **and
> each name the campaign adds thereafter.**

So wiring these is CARRYING OUT the registered population, not widening it after seeing
a verdict. The same paragraph sets the constraint that decides every adapter's shape:
the series is *"rebuilt at every origin from drivers the statement walk-forward
produces, **with no judgement**."*

**That constraint is why this is slower than it looks.** Each run writes its projector
in a different module, with a different signature, returning a different vocabulary —
five in `bottom_up.py`, GBCO in `score.py`; origin-and-horizon on AMOC and SWDY,
origin-only on PHAR and GBCO; horizon-keyed on some, fiscal-year-keyed on others,
D-numbered on SWDY. A reader expecting one convention finds nothing, which is `[L-355]`
in the place it costs most.

## What was wired today, and on what basis

**PHAR.** Its own arithmetic gives operating profit exactly:
`pbt = (rev − cogs) − expenses + other`, and on a non-condensed origin `expenses`
includes the finance charge, so **EBIT = pbt + finance** is the run's own identity
inverted rather than a composition of this desk's. The identity
`pbt == gross_profit − expenses_total + other_block` reproduces to the pound and is
asserted in the adapter rather than trusted.

**Its condensed origin is dropped and the reason is named.** On a condensed origin the
same function takes the other branch — `expenses = exp_r × rev`, one ratio fitted to a
statement publishing a single expense line — and whether that line includes finance is a
fact about the filing the projector cannot read. Adding it back might be right and might
double-count, and a fabricated cell corrupts the very error it is scored on. PHAR's own
panel marks FY2019 and FY2020 condensed, so FY2020 is the one origin lost.

## What is left, named rather than estimated

| name | what it needs | kind |
|---|---|---|
| **PHAR** | its panel reader exposes only income-statement keys, so no quantity is common to panel and block; the scale cannot be measured. Its `panel_export.json` carries the balance sheet (`ppe` matches the block to the pound at FY2023 and FY2024) — the reader has to reach it. Then three registry entries. | code |
| **GBCO** | the same: a projector is wired and the four registry entries are not, so all 8 cells drop on the scale | code |
| **SWDY** | **no operating profit anywhere in the run.** It carries the components — gross profit, SG&A, depreciation, other operating income and expense — and composes no EBIT. Whether its depreciation sits inside the leg costs is a fact about that run, and composing one here would be exactly the judgement the pre-registration forbids. **This one is the run's to declare, not the lens's to infer.** | research |
| **SCEM** | its own projector raises `KeyError: 'shares_from_capital'` at every origin tested. A defect in that run, not something to route around | fix |

## The honest statement

Wiring PHAR and GBCO takes the series from one name to three and makes **clause B
measurable**. It probably does not make clause C measurable, because those origins sit
in one era.

**So the nine do not publish tonight, and saying so is the point.** What has changed is
that the blocker is now named cell by cell with a kind against each — code, data,
research, or the terminal module correctly refusing — instead of standing as "criterion
3 is not met". Three of the four kinds are work with a rate. The fourth, SWDY's missing
operating profit, is a question its own run has to answer.


---

# Later the same day: the blocker is not the wiring

The section above reads the nine as blocked by projectors that are not wired and
valuation-input blocks that do not reach three years. **Both are true and neither is
what blocks Phase 1.**

Running the cash-flow lens against [R-MACRO-01]'s convergence bound — the house's
own, imported rather than minted — refuses **every cell it has ever scored**, and
the refusal became the largest drop class in the run at a stroke: 21 of 60, spanning
six of the nine names. The full measurement and its addendum are in
`engine/valuation_calibration/CONVERGENCE_REFUSAL_18-09-2026.md`.

**What that changes about this document.** Wiring SCEM, SWDY and GBCO would have
added cells of the same inadmissible kind. The queue in the section above is real
work and it is not the critical path; the critical path is that the mechanical lens
rebuilds PHDC's fifteen-year construction on five years, and would do the same to
every name added to it.

**What it does not change.** The nine stay held, for the reason they were already
held — [R-GAP-02] clause three, the method hold — and no fair value moves. The
difference is that the hold now has a measured cause with a named route out, rather
than a queue of wiring.


---

# End of the run: exactly what stands between the nine and publishing

`scripts/check_publish_block.py` names two open acceptance criteria and nothing else.
Both are now fully characterised, and neither is a queue of wiring.

## Criterion 3 — the backtest, and it cannot currently be run

`[R-VCAL-02 CLAUSE TWO]` makes Phase 1 the backtest: criterion 3's clauses A, B, C and F
**on the mechanical series**. That series now has **zero admissible cells**, because the
lens it is computed by does not rebuild the construction it is meant to grade — five
explicit years against PHDC's fifteen — and every cell it ever produced breached
`[R-MACRO-01]`'s convergence bound.

Closing it means **re-sealing the lens declaration**, which is the principal's call and
is registered as `mechanical-lens-window-reseal` in `engine/escalations.json` with its
routes, its measurement, a recommendation, a default and a date. The route out is real
and already in the repository: the IMF World Economic Outlook vintages in
`engine/macro_history/`, each dated before the origin it would serve, carry a forward
inflation ladder that converges to the house terminal on its own.

**Nothing about this was a clock**, which is worth saying because the previous reading of
criterion 3 was a 2027 date.

## Criterion 6 — the reading, and everything except the reading is done

Four files per name, each **opened and read**. The reading is a human act and the plan
says in terms that no script may attest it.

`python3 scripts/publish_queue.py` prints the queue in reading order with paths.
Measured today: **23 names deliver documents, all 23 hold all four — 92 files, nothing
short.** An earlier pass reported five studies missing two of four while every file was
on disk. They were always there.

## What each of the nine owes on its own account, separately

`python3 scripts/check_study_debt.py` prints it live: 274 ratchet entries across the 24
studies on disk. That debt does not block publication — the two criteria above do — but
it is what "finished" means for each name, and it is now countable rather than
remembered.
