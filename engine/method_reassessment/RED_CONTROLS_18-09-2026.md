# Six negative controls cannot inject their condition, and CI has been red since 17 September

> **CORRECTED, SAME DAY.** This document and the message reporting it first said **four**.
> The number came from a partial sweep; the full run over all 161 checks names **six**.
> The two additional ones are the SAME species and neither was caused by that day's work
> — `check_terminal_record_shape_negative_control` fails on
> *"MUTATION DID NOT LAND: renamed 38 markers, expected 37"*, a fixture pinned to a live
> COUNT of terminal-record markers in the tree, and it is red at the pre-session commit
> too; and `check_new_study_gauntlet_negative_control` was reported red by that sweep and
> is a twenty-minute run not re-confirmed at head, so it is listed as reported rather than
> verified. **A count taken from a partial sweep is not a count**, which is this document's
> own subject arriving in the document.

**Measured 18 September 2026, at the end of the night's work, by running every check
including the negative controls — which the usual sweep excludes.**

## What is red

| control | why it fails |
|---|---|
| `check_bibliography_negative_control` | *"fixture: the ratchet is empty, so this proves nothing"* |
| `check_correction_boundary_negative_control` | *"MUTATION DID NOT LAND: asp carried no applied correction"* |
| `check_corrections_applied_negative_control` | *"FIXTURE IS NOT THE REAL CASE: PHDC's applied count moved"* |
| `check_anchor_ordering_negative_control` | two cases *"MUTATION DID NOT LAND"*, two *"expected RED, got GREEN"* |
| `check_terminal_record_shape_negative_control` | *"MUTATION DID NOT LAND: renamed 38 markers, expected 37"* |
| `check_new_study_gauntlet_negative_control` | reported red by the full sweep; not re-confirmed at head |

**All six run in CI.** `[R-MERGE-01]` requires every gate green before a branch merges,
so nothing has been able to merge cleanly while these stand.

## They pre-date tonight and the window is narrow

Walked back through the branch's history:

| commit | date | red |
|---|---|---|
| tonight's head | 18 Sep | 4 of 4 |
| before tonight's work | 18 Sep | **4 of 4** |
| the preceding session | 17 Sep | **4 of 4** |
| `decb28681` | 7 Sep | **0 of 4** |

**Nothing in tonight's work caused any of them**, verified name by name against the pre-session commit. They broke somewhere in the 128
commits between 7 and 17 September — a window that includes a commit whose own title
reads *"the anchor-ordering release now needs a measurement, and six controls were
reporting a constant."*

## Five of the six are one species, and it is the mirror of tonight's

A negative control pinned to **live repository state** stops being able to inject its
condition the moment that state legitimately moves — and **refuses rather than
reporting green**:

- the bibliography ratchet was **pruned to empty**, which is the ratchet working, and the
  control's "a ratcheted breach stays green" case then has no ratcheted breach to use;
- the `asp` driver no longer carries an applied correction, so the mutation that removes
  one removes nothing;
- PHDC's applied-correction count moved off the 6 the fixture is pinned to.

**That is the right behaviour and it is the opposite failure to the one this session kept
finding.** Five times tonight a control was caught *passing* a fixture that never landed.
These four fail loudly instead. The cost is the same in one respect and different in
another: four gates presently have **no live evidence**, but the book knows it.

## The fourth carries something more than a stale fixture

`check_anchor_ordering_negative_control` reports two cases **expected RED, got GREEN** —
*"a bare SENTENCE no longer releases — it is an assertion, not a measurement"* and
*"anchored on the HIGHER of two figures held, with no mechanism."* The gate prints its
ordinary green line on both. That is not a stale fixture; it is a control asserting a
behaviour the gate does not currently have, and it needs reading before it is touched.

## Not repaired in this pass, and the reason is the rule's own

`[R-REPAIR-01]`'s first prohibition is that a repair **may not edit a gate, a negative
control or a ratchet** — *"passing a check by weakening it is the defect wearing the fix's
clothes and is the single most likely thing an automated repairer does."* Re-pointing four
control fixtures at the end of a long unattended run is exactly the act that prohibition
describes, and three of the four would be repaired by changing the very thing that is
supposed to prove the gate works.

**What each needs is small and is named above**, so the work is countable rather than a
mystery: the three stale fixtures want a **synthetic** injected state rather than a live
one — which is what makes a control durable — and the fourth wants somebody to read
whether the gate or the control is right.

---

## The lesson was already registered, and that is the finding

`[L-278]`, registered **4 September**, says it in its own words:

> **A NEGATIVE CONTROL THAT NAMES A LIVE RATCHET ENTRY HAS AN EXPIRY DATE ON IT** … a
> control case built by reaching into a live ratchet and moving whichever entry it was
> written around stops being constructible the day that entry is cleared — and then it
> fails for a reason that has nothing to do with the property it tests, **which reads
> exactly like failing for the right one. Plant the starting state; do not assume it.**

It was learned from **three controls breaking this way in one day**, on the exemplar's
ratchets. It is correct. It binds nothing — it is a register entry, and the register binds
nothing by design.

**A fortnight later, six more controls broke the same way.**

That is `[R-MACRO-01]`'s own general lesson arriving on the checking machinery rather than
on a study: *a lesson that binds nothing is advice, and advice loses to the next deadline.*
The half of `[L-278]` that **did** reach the code — *assert the mutation landed* — is
exactly why all six failed loudly instead of quietly passing. The half that stayed prose —
*plant the starting state* — is why they failed at all.

**Where a test needs a state, give it that state rather than finding it** — and where a
lesson about how tests are written can be made arithmetic, that is the only way it
survives.


## What this means for the nine, which is the only scope that matters now

The nine held on method are **ADNOCDIST, BOROUGE, DU, FERTIGLOBE, GBCO, PHDC,
RIYADHCABLE, SCEM, TMGH**.

Five of the six red controls protect gates that bear on names among them — the
anchor-ordering gate (SCEM is on its ratchet), the bibliography source gate (SCEM),
the two correction gates (PHDC and TMGH are walk-forward runs), and the terminal
record shape (GBCO is on the terminal ratchet). The sixth is system-level.

**More directly: all six run in CI, so CI is red, so nothing merges — including
anything done for the nine.** That makes them scope whatever else is.

Counted from the ratchets, **the nine carry 103 of the book's 276 study-side entries**:

| | | | |
|---|---|---|---|
| BOROUGE 14 | TMGH 14 | PHDC 13 | SCEM 13 |
| ADNOCDIST 11 | RIYADHCABLE 11 | FERTIGLOBE 10 | DU 9 |
| GBCO 8 | | | |

That debt does not block publication — criteria 3 and 6 do — but it is what
"finished" means for each name.
