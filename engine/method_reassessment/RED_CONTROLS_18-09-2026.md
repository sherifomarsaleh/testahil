# Four negative controls cannot inject their condition, and CI has been red since 17 September

**Measured 18 September 2026, at the end of the night's work, by running every check
including the negative controls — which the usual sweep excludes.**

## What is red

| control | why it fails |
|---|---|
| `check_bibliography_negative_control` | *"fixture: the ratchet is empty, so this proves nothing"* |
| `check_correction_boundary_negative_control` | *"MUTATION DID NOT LAND: asp carried no applied correction"* |
| `check_corrections_applied_negative_control` | *"FIXTURE IS NOT THE REAL CASE: PHDC's applied count moved"* |
| `check_anchor_ordering_negative_control` | two cases *"MUTATION DID NOT LAND"*, two *"expected RED, got GREEN"* |

**All four run in CI.** `[R-MERGE-01]` requires every gate green before a branch merges,
so nothing has been able to merge cleanly while these stand.

## They pre-date tonight and the window is narrow

Walked back through the branch's history:

| commit | date | red |
|---|---|---|
| tonight's head | 18 Sep | 4 of 4 |
| before tonight's work | 18 Sep | **4 of 4** |
| the preceding session | 17 Sep | **4 of 4** |
| `decb28681` | 7 Sep | **0 of 4** |

**Nothing in tonight's work caused any of them.** They broke somewhere in the 128
commits between 7 and 17 September — a window that includes a commit whose own title
reads *"the anchor-ordering release now needs a measurement, and six controls were
reporting a constant."*

## Three of the four are one species, and it is the mirror of tonight's

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

**The general lesson, which is not about controls:** *a fixture pinned to live data has an
expiry date nobody sets.* Every one of these was correct when written and was invalidated
by ordinary, legitimate work elsewhere — a ratchet paid down, a correction withdrawn, a
count moved. A control that builds its own condition survives that; one that borrows the
repository's does not. **Where a test needs a state, give it that state rather than finding
it.**
