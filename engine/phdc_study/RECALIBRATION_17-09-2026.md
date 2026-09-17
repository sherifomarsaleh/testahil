# PHDC — recalibration, steps 0 and 1

**17 September 2026.** Palm Hills Developments · EGX: PHDC · class *real-estate developer,
off-plan, percentage-of-completion*.

## THE ANSWER DID NOT MOVE, AND THAT IS THE RESULT RATHER THAN THE ABSENCE OF ONE

**bear 4.01 · base 17.85 · full 46.50** against **EGP 14.40**, the close of 3 September —
byte-identical to the delivered edition. Across three separate regenerations of the study's
committed numbers, **exactly two numeric fields in the whole file changed**, and neither is a
valuation figure:

| field | was | is |
|---|---|---|
| `registry/land_bank_sqm_mn/value` | 33.0 | **37.0** |
| `walkforward/corrections_applied_in_walkforward` | 6 | **8** |

Everything else that moved is a declaration, a reworded disclosure or a record-shape field.
**No rebuild ledger entry is written** — [R-REBUILD-01] records a route between two answers and
there are not two.

---

## STEP 0 — FREEZE, THEN ASK

**The baseline was already frozen on 1 September and the snapshot refused**, which is correct:
a baseline is a historical fact and is append-only, because a second capture would read a fair
value this campaign itself moved.

**THE PRICE WAS ASKED FOR AND NOT SUPPLIED, SO THE DEFAULT FIRED AND IS DISCLOSED** rather than
substituted silently [R-GAP-01 AMENDED]: the study stands on **EGP 14.40 of 3 September 2026**,
the latest price this repository holds, **fourteen days old at the date of this pass.** That is
the shape [R-COC-01] uses for a deliberately-accepted stale sovereign quote — taken, stated,
aged — and it is not the same quantity as "the latest known price", which is the whole reason
the rule says to ask at the start rather than look it up at the end.

**272 lessons bind on this name**, of which 8 are its class's and 5 are its own. **Two are
OUTSTANDING — registered, correct, and acted on by nobody:** L-104, deliveries must be
constrained by what has actually been sold; L-203, Palm Hills' 2025 balance sheet and cash-flow
statement disagree by 47% of revenue. Both are named here because a lesson that binds nothing
is advice, and neither is closed by this pass.

## STEP 1 — WHAT THE RECALIBRATION ACTUALLY DID

This name already carries a full fundamental walk-forward, so step 1 is the incremental path:
the work outstanding on it, not a new run. Three things were outstanding and all three are now
closed.

### 1 · The corrections, rebuilt under the cut-invariant rule

[R-FCAL-01] was amended on 7 September: a bias must hold its sign **at every cut the data
admits**, not merely across eras. This run's `corrections.py` still compared era means of its
own, and its three flipping corrections sat on a ratchet whose own entry said rebuilding them
"is its own measured pass". **This is that pass.** The module now CALLS
`boundary_sensitivity.cuts_for()` rather than reimplementing the test [R-ENF-03], and a driver
too thin to cut is UNTESTABLE rather than stable [R-ENF-04].

**IT CUT BOTH WAYS, AND THE HALF THAT WAS NOT EXPECTED IS THE INTERESTING ONE:**

| origin | driver | was | now | why |
|---|---|---|---|---|
| 2023 | average selling price | +0.0535 | **withdrawn** | flips at 2 of 4 cuts |
| 2023 | units sold | −0.0729 | **withdrawn** | flips at 1 of 4 cuts |
| 2024 | units sold | −0.1077 | **withdrawn** | flips at 1 of 5 cuts |
| 2021 | units delivered | — | **+0.2628** | holds at all 2 cuts |
| 2021 | finance charge | — | **−0.4207** | holds at all 2 cuts |
| 2022 | units delivered | — | **+0.2247** | holds at all 3 cuts |
| 2022 | selling and admin | — | **+0.1349** | holds at all 2 cuts |
| 2022 | finance charge | — | **−0.4095** | holds at all 3 cuts |

Three withdrawn and **five admitted**, at origins the old test could not reach at all: the era
rule needed two eras each holding two resolved errors, and in 2021 and 2022 only one era
qualified, so it returned "not stable" for want of data rather than for want of stability. The
amended rule asks a question those origins CAN answer. **A stricter-sounding rule is not
uniformly stricter, and saying so is the honest reading of it.**

**THE UNCOMFORTABLE PART, RECORDED RATHER THAN LEFT FOR A READER TO FIND.** Judged
point-in-time, `is.sga` at 2022 survives both cuts its information set admits; judged on the
whole record it flips at **six of six**. Both statements are true and they answer different
questions — what an origin could see, and what the driver turns out to be — and point-in-time
discipline is absolute, so the correction stands as an act and the driver is unstable in
hindsight. The gate prints both for exactly this reason. And the adjusted-versus-raw test says
the newly admitted corrections make those origins **worse**: 2021 +0.058, 2022 +0.067 in mean
absolute log error, against 2024 −0.082. **No correction was promoted into the live drivers and
none ever has been**, so nothing published rests on any of this.

### 2 · The land bank — the defect the asset-base rule was adopted on

The study committed **33.0 mn sqm as at 31 December 2024** inside an information set ending
1Q2026. The 1H2025 earnings release — **already in this repository and already parsed by this
name's own walk-forward** — states **37 million square meters** in the *same* "spreading over N
million square meters" sentence of the same boilerplate. Like for like, one year apart: the
committed figure understated a developer's operating asset base by **12.1%**, and the release
says in its own words that the company is "actively seeking to replenish our landbank in 2025",
so the movement is disclosed rather than inferred.

Corrected, and an `asset_base_record` now commits the vintage. The base is still behind the
information set, so `not_restated_since` **names the three later filings actually checked** —
the 1Q2026, FY2025 and Q3 2025 consolidated statements — and the reason none carries the
figure: **a land bank is an operating KPI and operating KPIs are disclosed in earnings
releases, not in financial statements.** Which is what this name's own registered lessons
already say twice over (L-116, L-205). **The search that would close it is a DOCUMENT to
obtain, not a page to re-read**, and it is named so the next pass looks for the right thing:
the FY2025 and 1H2026 earnings releases.

**AND CORRECTING IT MOVED NOTHING, WHICH IS THE SECOND HALF OF THE SAME DEFECT** [R-ASSET-02]:
the figure is printed to the workbook and reaches no arithmetic anywhere in the model. New land
raises this valuation by zero and exhausted land lowers it by zero.

### 3 · The cost-of-equity record, which was older in shape than the module that writes it

`engine/cost_of_capital.py` already emits `ke_terminal_construction`; this study's
`wacc_result.json` predated the field, so regenerating supplied it — **`same_beta`**, which is
what the shared instrument independently said the record reproduces under. `beta_source` is now
**DERIVED from the attested beta record rather than typed**: GBCO writes the literal, which is
true there and is a second place for a fact to drift, and a study whose regression later failed
its usability gate would fall to a tier-3 beta while keeping a token saying otherwise. Here the
study **raises** instead of defaulting. Beta 1.0493 and the explicit cost of capital 25.11% are
unchanged.

Both ratchet entries pruned in the commit that fixes them, so PHDC's standard-version claim of
2026.09.07 is now one it actually meets — which it was not, because the generator takes the
stamp from the live constant and **re-asserted it on every rebuild with nobody deciding**
[R-STD-02]. The gate caught that on this pass, which is what it was written for.

---

## WHAT IS CARRIED TO STEP 4, AND IT IS NOT VISIBLE TO ANY GATE

**The delivered workbook prints the superseded land bank.** `Segments!A35` reads **33** against
a committed **37**. Every relevant gate passes — `check_workbook_values` runs the study's own
recalculation, which reconciles the workbook **to itself**, so a workbook one edition behind the
record reconciles perfectly and reports clean; `check_prose_figures` matches figures against the
model and the delivered *document* never prints this one at all.

It is **not** re-issued here. The depth bar is not divisible, so a fresh workbook means a fresh
document, bibliography and QC gate, and the recalibration is at step 1 with its documents due at
step 4 regardless. **Recorded so it is carried rather than remembered**, and it is a real gap in
the instrument set: *a check that reconciles an artefact to itself cannot see that the artefact
is one edition behind the record.*

## STOP CONDITION

Step 0 complete — baseline frozen, price defaulted with its age disclosed, lessons read. Step 1
complete on the incremental path: the corrections rebuilt under the standing rule, the asset
base committed and corrected, the cost-of-equity record brought to the shape its module emits.
**Next: step 2, internal QC.**
