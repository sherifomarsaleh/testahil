# ELEC — the class decision

**7 September 2026 · INTERNAL**

`study_numbers.json` records **no class** for ELEC, and `research_protocol.LENS_REGISTRY`
carries **no row for a cable or wire manufacturer**. Both facts were checked live rather
than assumed.

## The decision

> **ELEC is run as the nearest pattern — *refiner, commodity pass-through on a thin
> spread* — adapted inside the ADNOCLS skeleton. No registry row is added.**

Lens set inherited: **DCF primary**, cross-checked by EV/EBITDA on the company's own
history, replacement cost, a relative multiple, and book value published as a disclosed
floor and never weighted.

## Why that row and not another

A cable maker buys copper at a globally-quoted price and sells cable at that price plus a
**conversion spread**. The delivered study already models it that way — its central driver
is *conversion EBITDA per tonne*, and its revenue is copper-and-currency linked. That is
the same economic shape the refiner row exists for: a commodity passing through at
market price with the value sitting in a thin conversion margin over it.

Two rows were considered and declined, with reasons, because declining them is part of
the decision:

- **cement and heavy industrial** — its `ev_per_tonne` cross-check means *cement
  capacity*, and a kiln has no traded input passing through it. A cement price sits
  behind freight protection; a copper price does not. The pass-through is the difference
  and it is the thing that matters.
- **petrochemical** — closer, but its replacement-cost cross-check carries the weight for
  an integrated plant, whereas a cable line's value is overwhelmingly the spread it earns
  on someone else's metal.

## Why no registry row is added

[R-LENS-03] says in terms that **a class is added when a DIFFERENT LENS carries the
weight, never merely when the industry differs.** A cable maker's lens set is identical
to the refiner row's. Adding a row would be adding it for an industry difference, which
that rule forbids — and the protocol already supplies the answer for exactly this case:
*adapt the nearest pattern's lens inside the ADNOCLS skeleton and say which and why*.

This is the same wall SAVOLA and EMPOWER met, and it is open as
`lens-registry-has-no-row-for-a-food-and-grocery-group` in the escalation register. ELEC
is a **third** independent name meeting it. That is recorded there rather than resolved
here, because whether the registry should key on a lens SET rather than an industry NAME
is a rule amendment and not something a single run decides in passing.

## What this decision does NOT do

It does not licence a rebuild. This run's scope is SKIP and the study is not rebuilt —
see `TRAINING_RECORD_07-09-2026.md` §6. The class is recorded now so that whoever does
rebuild this name starts from a decision that was made and reasoned rather than from a
blank field.
