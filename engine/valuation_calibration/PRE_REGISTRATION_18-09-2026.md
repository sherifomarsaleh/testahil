# The valuation calibration — pre-registration, second edition

**18 September 2026.** This SUPERSEDES `PRE_REGISTRATION_03-09-2026.md` and says so,
which is the route that document itself set out: *"Nothing in this document may be
edited after its commit. A correction is a new dated pre-registration that supersedes
it and says so, and the gate reads the commit dates."* The first edition is not edited,
not withdrawn and not hidden; it stands as written and this one states exactly what
moved and what it cost.

---

## What is NOT changed, and saying so first is the point

Every clause of the first edition stands unless named below. The question, the two
scores and why there are two, the point-in-time discipline, the statistics, the block
bootstrap and its seed, the era split, the leave-one-name-out, the effective-n warning,
the promotion order, the stop rule and its symmetry, the four *what this is not*
clauses, and the falsifier — all unchanged, word for word.

**No fair value moves because of this document.** No study reads it, at any origin.

---

## The honest part, stated before the changes rather than after them

**This edition was written with a measurement already in view, and the first edition
was not.** That is the whole of what it costs and it is not dressed down.

The first edition's claim on credibility is commit order: it was written and hashed
before any score existed, so *"no lever was fitted to the gap"* is a fact about the
repository rather than an assurance. This edition cannot make that claim about the
clauses it changes. On 18 September 2026 the lens was run, every one of its seven
scored cells was found to breach a standing rule, and the construction below was
written afterwards. A reader is entitled to ask whether the new construction was
chosen because it produces a friendlier number.

Three things bound that risk, and none of them is a promise:

1. **The change was forced by a rule that predates the first edition by four days.**
   [R-MACRO-01] was adopted 2 September 2026 and requires an explicit window to run
   until growth is within 2pp of terminal. The first edition's construction never
   satisfied it and nobody had asked. The bound is IMPORTED from
   `research_protocol.HORIZON_CONVERGENCE`, not restated here, so this document cannot
   soften it.
2. **The substituted input is read, not chosen.** The inflation path below comes out of
   the point-in-time archive exactly as published. There is no parameter in it to tune,
   and a horizon the archive does not reach is REFUSED rather than extrapolated.
3. **It made the result worse, not better.** Under the first edition's construction the
   lens scored seven cells. Under this one it scores NONE — every cell is refused, and
   the refusals are printed by name. A construction chosen to flatter a result does not
   delete the result.

---

## Change 1 — the escalator is the archive's own forward ladder

**What it was.** Each cell was built from its run's own projection, and every run
escalates its drivers on the LAST PUBLISHED inflation print at the origin, compounded
FLAT at every horizon. That is the correct point-in-time choice for scoring a DRIVER —
the run is testing whether a forecaster standing at that date could have got the line
right — and it is the wrong one for building a VALUE, because a flat crisis-level rate
converges to nothing and no window of any length can satisfy [R-MACRO-01].

**What it is.** The point-in-time archive already carries, at every origin, the IMF
World Economic Outlook vintage's own forward projection for that origin's year and the
four after it — published at the origin by a named institution on a named date, and
declining on its own with no fade applied:

| origin | h=1 | h=2 | h=3 | h=4 | h=5 |
|---|---|---|---|---|---|
| 2017 | 16.92% | 10.91% | 8.09% | 7.18% | 6.96% |
| 2023 | 32.18% | 19.88% | 13.77% | 11.47% | 9.50% |

A forecaster standing at the origin could have used exactly this and nothing else was
knowable. **Point-in-time discipline forbids foresight, not a declining forecast**, and
that sentence is the whole of the claim.

`engine/valuation_calibration/pit_inflation.py` reads the ladder. Only INFLATION moves:
every driver rule, volume path, margin rule, tax regime, commodity convention and
currency mechanism stays exactly as its run pre-registered it — and where a run derives
its currency from its own inflation print by purchasing-power parity, the substitution
flows through to the currency too, because [R-MACRO-01] requires ONE path and a model
escalating costs on one inflation and its currency on another is the incoherence that
rule exists to close.

**ONE NAMED ADAPTER PER RUN**, in `pit_substitution.py`, because nine runs carry nine
seams and a reader that guesses a convention silently finds nothing and reports it as a
result. **Every patch asserts that it landed**: a substitution that silently fails to
bind returns the run's own answer under a new label, which is the absent answer wearing
a clean one's clothes [R-ENF-04], and this repository has caught a fixture that never
injected its condition five times.

## Change 2 — the terminal rate is read at the window's last year

**What it was.** `terminal_inflation()` read the ladder at a FIXED module horizon of
five, whatever window the cell actually built. A run pre-registered at three horizons —
which [R-FCAL-01]'s LIGHT scope licenses — therefore capitalised a rate two years
further down the ladder than anything it projected.

**What it is.** The terminal rate is the ladder's own rate in the LAST EXPLICIT YEAR
the window reached. Convergence is then a test of what is left, which is the run's own
REAL growth — the thing the bound should have been measuring all along.

## Change 3 — a power of ten is a unit, not a view

The first run of the rebuilt lens scored exactly one cell and it read **+75,727.6%** —
a fair value of 2,782.87 against a price of 3.67. That is not a disagreement with a
market; it is a share count or a price series in the wrong unit. Every gate passed it:
the unit ratio measured, the terminal built, the bridge footed, the convergence bound
held. **Nothing in the module was looking at the ANSWER** — which is [R-GAP-01]'s own
lesson arriving inside the instrument built to measure gaps.

A cell whose fair value differs from its price by a factor of ten or more is recorded
as a UNIT SUSPECT and not pooled. **The bound is not chosen**: it is one order of
magnitude because the failure it catches IS an order of magnitude, the same argument
`panel_scale()` already makes when it pins a unit to a power of ten — reused rather
than minted, which is the only honest justification for a cutoff here.

## Change 4 — two names join the population, under the first edition's own clause

The first edition sets the population as FULL on *"AMOC, ARCC, EGCH, PHDC, TMGH, and
each name the campaign adds thereafter"*. **SWDY** and **SCEM** have completed runs and
are wired. This is carrying out the registered population, not widening it.

SWDY is wired **on instruction**, and its two wiring defects are recorded because both
are this book's standing failure mode: its projector returns a `(drivers, paths)` TUPLE
where every other run returns the mapping alone, and its panel names the finance charge
`interest_exp` in the release years and `finance_cost` in the audited ones — an alias
its own source documents with the warning that one spelling *"reads half the window as
absent"*, and a reader taught one spelling duly read half the window as absent.

SCEM needed **no patch at all**: its projector takes `macro_override` as an argument, so
the ladder goes in through the run's own public signature and its year-by-year rates are
used as published. Every other run would have this shape if anyone had known to ask for
it, and the difference is worth naming — a hook is a declaration that the macro path is
an INPUT, and the seven runs without one had made it a constant.

---

## What the rebuild measured, and it is not what was hoped for

**Zero cells score.** The refusals, by count:

| cells | refused for |
|---|---|
| 22 | the explicit window never converges to the terminal [R-MACRO-01] |
| 10 | the block carries fewer than three years for a trailing intensity |
| 10 | other, named individually in the record |
| 8 | the panel's unit cannot be measured against the block |
| 3 | terminal refused: implied payout outside [0, 1] |
| 3 | the projection carries no revenue or operating profit |
| 2 | terminal refused: free cash flow not positive |
| 2 | the panel carries no finance charge at the origin |

**The convergence bucket is structural and was tested rather than assumed.** The obvious
repair is to run the window longer, and it does not work: asked for fifteen horizons
instead of five, PHDC's projection ends growing at **20.66%** and TMGH's at **39.37%** —
these driver rules ACCELERATE. They compound a population or intensity term that never
decays, because they were built to score three to five years of drivers and nothing
more. **A longer window makes it worse.**

So the finding is sharper than a data gap: **the mechanical lens cannot value these
companies under [R-MACRO-01] at any window length, on these runs' projections.** The
house's own delivered studies converge because their explicit windows run until growth
settles — PHDC's runs fifteen years on drivers that genuinely decay as a land bank
exhausts. The walk-forward projectors are a different instrument built for a different
question, and using them to build values was the assumption nobody had tested.

## What is NOT decided here, and why it is not

The obvious next construction is to let the terminal carry a STATED real growth equal to
the window's own last real growth, which would satisfy the bound by construction and
charge the incremental capital behind it. **That is a methodological decision with a
large and one-directional effect on every value, and it is not taken at the bottom of a
document by the person who found the problem.** It is registered in
`engine/escalations.json` with the routes run, a recommendation, a default and a date
[R-IND-01], and the work routes around it meanwhile.

## What would overturn this edition

Unchanged from the first, and now with a second clause: if the mechanically rebuilt
series turns out not to resemble the as-delivered one once that record is long enough to
compare, this calibration is grading a method the house does not use and every promotion
must be withdrawn. **And if a scored mechanical series never becomes constructible at
all, then series (b) — the fair values this house actually published — is the only
instrument there is, and the criterion that reads series (a) has to say so rather than
wait.**

---

*Nothing in this document may be edited after its commit. A correction is a third dated
pre-registration that supersedes it and says so, and the gate reads the commit dates.*
