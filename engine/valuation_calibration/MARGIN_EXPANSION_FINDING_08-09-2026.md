# The pooled bias is a manufactured margin expansion, and it is [L-048] in mirror image

**Measured 8 September 2026, under declaration 4.** Diagnostic only — nothing here changes
a declared run, a delivered study or a published fair value. It is written down because it
names what blocks the one gating test still failing.

## What was being chased

Two answers valued ARCC at roughly ten times its traded price — origin 2017 at +951% and
2023 at +982%. They survived a complete replacement of the terminal construction, so they
are not a terminal artefact. That negative result is what pointed at the projection.

## What the projection does

ARCC's forecast expands the operating margin at **every one of its eight origins, without
exception**, monotonically over five years:

| origin | year 1 → year 5 | fair value vs price |
|---|---|---|
| 2016 | 31.0% → 44.4% | +235% |
| 2017 | 22.3% → **55.7%** | **+951%** |
| 2018 | 15.0% → 28.9% | +237% |
| 2019 | 5.8% → 15.7% | +162% |
| 2020 | −1.5% → 5.2% | +100% |
| 2021 | 5.1% → 12.1% | +97% |
| 2022 | 20.1% → 37.8% | +279% |
| 2023 | 30.6% → **60.1%** | **+982%** |

Eight origins and eight expanding margins is not a forecast, it is a property of the
construction. **The overstatement tracks the terminal margin almost monotonically**, which
is what makes this the driver of the pooled bias rather than one more thing wrong.

The company's own filed operating margin over the same period runs 32.8, 28.0, 32.9, 18.3,
17.0, 10.0, 4.9, 10.2, 21.4, 24.3, 27.0 and 43.7 per cent — it swings **both ways**, which
no origin's forecast ever does.

## The mechanism, read off the code rather than inferred

`bottom_up.project()` escalates the revenue side at full domestic inflation — price at
`pi`, volume at population growth. On the cost side, at origin FY2023 over five years:

| line | multiplier |
|---|---|
| price, services, transport, overhead, G&A | **× 4.302** (full CPI) |
| coal half of raw materials | **× 1.000** — frozen |
| depreciation, amortisation, right-of-use | **× 1.000** — frozen |
| *the currency the same model carries* | *× 10.434* |

`_paths()` returns `coalm = 1.0` on the knowable path. Coal is a **dollar** commodity and
this is an **Egyptian pound** model, so freezing it in pounds through a 10.4× devaluation
is not a no-drift assumption — it is a large implicit real cost saving that compounds.
The defence in the code is that "a commodity price has no drift and assuming one would be
a forecast" — which is right about the *dollar* price and is being applied to the *pound*
cost. The model already carries its own currency path; the two were simply never joined.

Depreciation, amortisation and right-of-use are frozen outright, so a capital-intensive
plant's largest fixed cost stays nominally still while its revenue quadruples.

## The counterfactual, which confirms it by where it does *not* bite

Holding coal flat in **dollars** and converting at the model's own currency path — the
same no-drift assumption expressed in the right currency — gives final-year margins:

| origin | declared | coal in dollars | currency moved? |
|---|---|---|---|
| 2016 | 50.3% | 11.9% | yes |
| 2017 | 61.4% | −57.5% | yes, heavily |
| 2018 | 35.3% | 35.4% | no |
| 2019 | 22.3% | 28.8% | no |
| 2020 | 12.9% | 21.4% | no |
| 2021 | 18.7% | 19.7% | no |
| 2022 | 43.3% | 14.5% | yes |
| 2023 | 64.4% | 14.2% | yes |

**The two readings are nearly identical wherever the exchange rate was stable and diverge
enormously wherever it moved.** That is the signature of this defect and of no other, and
it is stronger evidence than the level of any single cell.

The counterfactual is **not proposed as the fix**: at 2017 it drives the margin to −57.5%,
which is an over-correction, because some of a coal cost increase does reach price. The
declared path assumes **zero** pass-through of the currency into the coal cost and the
counterfactual assumes **total** pass-through with none into price. The truth is between
them and neither end is a forecast anybody should ship.

## Why this is the house's own lesson arriving backwards

[L-048] and [R-MACRO-01] are written about escalating costs at domestic inflation while
holding the currency or the price still — "one event counted once and ignored once,
inflating every cost and freezing every price," and the forecast then reports the
manufactured margin **decline** as a finding. **This is the identical defect with the sign
reversed:** the event is counted on revenue and ignored on cost, and the forecast reports
a manufactured margin **expansion** as a valuation.

And the house has a gate for one direction only. [R-ANCHOR-01] catches a forecast opening
materially **below** the latest reviewed period, and its own text says it "does NOT fire on
a forecast ABOVE the latest period." Eight origins here forecast margins far above every
period the company ever filed, and nothing looked.

**The general lesson, which is not about cement:** a gate built from one incident inherits
that incident's direction. The first occurrence was a margin collapsing, so the rule was
written about collapse — and the same arithmetic running the other way had no owner for a
month. Where a rule fires on a sign, ask what happens at the other one.

## What is NOT done here

ARCC's projection is that run's own pre-registered method and its walk-forward scored its
drivers against it. Changing it moves that run's committed results and is not done in
passing or on this evidence alone. What this file establishes is the diagnosis; the
remedy — a pass-through assumption for a foreign-currency input, and the mirror clause on
[R-ANCHOR-01] — is a decision recorded separately.

---

# The attribution, measured — 08-09-2026, later the same day

The diagnosis above named a defect. This section prices it, because a named cause with
no magnitude beside it cannot be the "residual bias attributed to a named lever" the
acceptance criterion asks for.

## Three readings, all published, none of them the declared run

`score_cashflow.py` now prints all three beside the declared score. The declared run is
untouched and byte-identical to what it was before this measurement existed.

| reading | cells | pooled mean log(FV/P) | block-4 95% CI |
|---|---|---|---|
| **DECLARED** — the run's own projection | 15 | **+0.7880** | [+0.6090, +1.0052] |
| coal held flat in DOLLARS, carried on the run's own currency path; D&A escalated | 14 | +0.5019 | [+0.5019, +0.7918] |
| **COHERENT** — the level rule applied consistently | 15 | +0.6917 | [+0.5805, +0.9141] |

## The two errors are one error

The run's own docstring states the principle correctly — *"a commodity price has no drift
and assuming one would be a forecast, not a rule"* — and then applies the **level** rule
and the **rate** rule to the wrong quantities.

- **Coal** is held at its level in **pounds**, but `coal_egp()` is the South African
  dollar price *multiplied by* the exchange rate. Holding that flat through a window in
  which the pound fell 10.434× asserts a dollar coal price falling about ninety per cent.
  That is not a rule about a commodity; it is a forecast, and an impossible one.
- **The currency** is held at a **rate** — the origin's last realised annual move,
  compounded five years. Inflation is a rate; **a devaluation is a step**:

  | origin | compounds to | realised over the same five years |
  |---|---|---|
  | FY2016 | ×3.763 | ×1.560 |
  | FY2017 | ×17.557 | **×1.077** |
  | FY2018 | ×0.996 | ×1.724 |
  | FY2019 | ×0.749 | ×2.701 |
  | FY2020 | ×0.733 | ×3.124 |
  | FY2023 | ×10.434 | not yet resolved |

  Wrong by a factor of sixteen at the float year and wrong in the **opposite** direction
  at three consecutive origins — so it is not a bias a reader could correct for.

The coherent specification is that sentence applied consistently: a price held at its
level **in its own currency**, and the currency held at its level too. **It is chosen on
that argument and not on its score.** The score agrees with it — on the five resolved
five-year margin cells, mean error +0.0393 against the declared +0.1075 and the
intermediate −0.2110, mean absolute error 0.1959 against 0.2561 and 0.2399 — and that
agreement is evidence, never the reason. Three specifications were run and the best was
reported, which is recorded here plainly so a reader can discount it accordingly.

## What this settles, and it is not what it was built to settle

**The unit errors are real and they are not the answer.** They are worth between 0.10 and
0.29 of the +0.7880, and **every one of the three readings leaves the pooled bias positive
with all three bootstrap intervals excluding zero.** Correcting them does not reach
criterion 3's clause A and no further correction inside this lens will.

Under the coherent reading the bias decomposes as **ARCC +1.1722 over 8 cells, PHDC
+0.6210 over 4, EGCH −0.7409 over 2, TMGH −0.0041 over 1** — so ARCC still dominates
after its own specification is repaired, because what remains is structural: half its
raw-material stack is pegged to a commodity held at a level while revenue escalates at the
full inflation ladder, which expands a margin by construction in any inflationary market.

**That is an input's property, not the valuation construction's.** The lens inherits every
run's projection, so this bias is not removable here, and it is not one of the six levers
the pre-registration fixed in order before any score existed — the projection is not on
that list, and adding a seventh after seeing the scores is the fitting this method forbids
everywhere else. The sanctioned route to clause A is those six levers, in their written
order, and none of them has been run.

## What is NOT done here, restated because the temptation grew rather than shrank

The intermediate reading over-corrects at exactly the two devaluation origins — ARCC 2017
drops out entirely, its last forecast year consuming cash — and the coherent reading is
better at five of seven five-year cells and worse at two. **Neither is the truth**, and
nobody may claim in advance which way a repair moves a value. The remedy for a unit error
is to fix the unit **in the run that carries it**, which re-scores that run's own drivers,
lessons and corrections record, and is its own pass with its own declared amendment and
its own audit — not a branch inside this lens that somebody could later flip.
