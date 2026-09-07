# The framework that works — specification and date

**14 September 2026.** Seven working sessions from 07-09-2026, at the principal's own
rate of one bounded session per day.

Three properties, stated as the principal stated them, each with the test that says it
holds. A property with no test is not delivered.

---

## P1 — IT REACHES ALL 90 NAMES, AND EVERY NEW ONE

**Today it does not.** 24 of the 90 published fair values have a study directory; every
construction gate globs `engine/*_study/`, so **66 names are outside all of it** — not
failing, not passing, invisible. That is the dangerous state, because an empty result
reads exactly like a clean one.

**AND IT CANNOT BE FIXED BY GATING HARDER, WHICH IS THE HONEST PART.** You cannot check
the construction of a valuation that has no construction committed. For those 66 there is
a `fair{bear,base,full}` in `assets/data.js` and no model behind it. So reach arrives in
two tiers and only the first is in this week:

- **Tier A — in this week.** Every one of the 90 carries a minimal **provenance record**:
  class, lens, central, spot and its date, and an explicit declaration of whether a model
  exists behind the number. Gates then bind on all 90 for what is checkable, and a name
  with no model is **VISIBLY** modelless instead of silently unexamined. The population is
  anchored on `assets/data.js`, not on the study directories, so a gate that examined 24
  names when the book holds 90 FAILS.
- **Tier B — NOT in this week, and the cost is stated rather than discovered.** Building
  the 66 missing models is Phase 2a, about nine weeks. Nothing in this specification
  pretends otherwise.

**Test:** a gate run reports 90 examined, 0 unaccounted. A ticker added to `data.js`
with no record makes the build red.

## P2 — IT CATCHES THE ERRORS THAT ACTUALLY HAPPEN

Measured 07-09-2026 against the principal's three named errors: one caught, two not.

- a fair value far from price — **caught** (`check_valuation_gap`, `check_publish_block`)
- a developer's asset base going stale — **uncovered**; `landbank` occurs in zero gates
  and zero governing documents, and PHDC carries a land base dated 2024-12-31 in a study
  edition-dated 2026-09-02
- the LEVEL of Ke and Kd — **uncovered**; no file in `scripts/` reproduces
  `Ke = rf* + beta x ERP`, while ARCC's own beta interval spans a fair value from 59.35
  to 102.54

A 14-lens census of every way a fair value goes wrong is running, each gap claim
adversarially refuted before it counts. Its output is the rest of this list.

**Test:** every gap the census confirms is either closed by a gate or listed with a
reason. A closed gap has a negative control that re-injects the real defect and asserts
the mutation landed before the gate runs.

## P3 — A RED GATE IS WORKED UNTIL IT IS GREEN

**This does not exist today and it is the property that makes 90 names tractable.** Today
a gate goes red and a human reads the output. At 90 names that does not scale, which is
why 47 ratchet entries have accumulated on five studies.

**The repair loop:** the runner runs every gate over every name, collects each failure
with its name and reason, and hands each one to a repair pass scoped to that single
failure, with the gate itself as the oracle — fix, re-run that gate, repeat. Bounded
attempts; on exhaustion it registers an escalation carrying what it tried, per the
existing escalation register, and moves to the next failure rather than stopping.

**THE THREE THINGS THE REPAIR LOOP MAY NEVER DO, because each would turn the framework
into a machine for manufacturing green:**

1. **It may not edit a gate, a negative control, or a ratchet.** Passing a check by
   weakening it is the defect wearing the fix's clothes.
2. **It may not move a fair value toward the price.** The price is evidence that a defect
   may exist, never a target — a value adjusted to meet a quote is the reverse-engineered
   rate this method prohibits outright.
3. **It may not invent an input.** A missing figure is recorded as missing and escalated.
   SIGCM clause 1 and clause 8 bind on the repair loop exactly as on a person.

**Test:** the loop is run against studies with defects deliberately planted in them, and
must fix the fixable, escalate the rest, and — checked by `check_tree_unmodified` — leave
every gate, control and ratchet byte-identical.

---

## The proof, which is an injection and not a maturity date

`check_error_injection.py`: a catalogue of NAMED REAL ERRORS, each planted into a copy of
a REAL study inside a sandbox, then the whole gate set run against it. Every mutation
asserts it landed before the gates run — this project has four times caught a control
passing a fixture that never injected its condition. A catalogued error that no gate
catches is RED, so the catalogue is the specification of what the framework must catch and
the harness is the standing proof that it does.

It starts with the principal's three, and grows with the census.

**This is showable.** It runs in minutes, it names the gate that caught each error, and an
investor can read it without taking anything on trust.

---

## What 14 September does NOT deliver, stated rather than discovered later

- **The 66 missing models.** Those names will be visibly modelless, which is the fix for
  the dangerous state; they will not be modelled.
- **Proof that the method is unbiased out of sample.** That is Part E criterion 3 and, for
  its forward half, 2027 at the earliest. A framework that catches known error classes is
  not the same claim as a method measured unbiased, and the two must not be sold as one.
- **Publication.** Publishing to the live site remains a separate, explicitly-requested
  step and `[R-GAP-02]` is untouched.
