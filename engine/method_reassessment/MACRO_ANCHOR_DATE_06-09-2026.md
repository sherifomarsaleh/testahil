# Two rules disagree about which date governs the currency, and it is worth 25% on one name

**Dated 6 September 2026.** Found by reading PHAR's rebuild ledger, which is exactly what
[R-REBUILD-01] was adopted for — the route, not just the arrival.

---

## What PHAR's ledger records

| # | lever | rule | before → after | move |
|---|---|---|---|---|
| 1 | terminal on the disclosed life; growth as a real rate | R-TERM-01 | 58.04 → 84.19 | **+45.0%** |
| 2 | re-struck on the latest known price | R-GAP-01 | 84.19 → 84.63 | +0.5% |
| 3 | domestic inflation to the house ladder; currency re-derived | R-MACRO-01 | 84.63 → 65.17 | −23.0% |
| 4 | terminal risk-free derived rather than quoted | R-MACRO-01 | 65.17 → 49.10 | −24.7% |
| 5 | currency conformed to the house derivation's own anchor | R-MACRO-01 | 49.10 → **36.64** | **−25.4%** |

Read as five corrections this is a landslide. Read as **two rules pulling opposite ways** — a
terminal correction worth +45% and a macro conformance worth −57% — it is a contest, which is
what the ledger exists to make visible.

## Lever 5 is where the rules collide

Its own `why`, verbatim: *"a first draft anchored FY2026 at the observed spot; the house
derivation does not admit a leading-year anchor for a currency and the study conforms rather
than inventing one"*, with `evidence`: *"the tension in the house path's first year is
registered, not resolved"*.

**The tension is real and it is not PHAR's.** Measured on the committed files:

| | date |
|---|---|
| `engine/macro_paths/EG.json` `as_of` | **2026-09-02** |
| its `fx.spot` anchor (USD/EGP 50.25) | **2026-08-06** |
| the close PHAR was re-struck against (lever 2) | **2026-09-03** |

**The house path is stamped 2 September and its currency anchor is dated 6 August — 27 days
apart, inside one file.**

So [R-GAP-01 AMENDED] requires a study to be delivered against the **latest known price**, and
[R-MACRO-01] pins its currency to an anchor four weeks older. A study obeying both is running
**two dates for one economy** — which is [L-048]'s own complaint (*"a study that escalates
costs at Egyptian inflation while depreciating the pound at a third of the differential is
running two views of one economy"*, in that path's own `derivation` field) arriving in a place
nobody looked.

## What is NOT claimed

**PHAR conformed correctly.** [R-MACRO-01] exists because five studies once carried five
inflation rates for one country in one year, and a study re-anchoring the currency on its own
strike date is exactly the per-study path that rule forbids. Lever 5 is the rule working, and
the ledger's phrase *"registered, not resolved"* is an honest flag rather than an excuse.

**Nor is this a reason to move PHAR toward the price.** It is worth stating plainly because
the correction happens to run that way: the argument here is a date inconsistency between two
committed files, and it would be exactly as valid if the pound had moved the other way.

## The candidate, stated and not adopted

**The house path's own anchors carry dates, and the path should not be usable at a strike date
materially later than the anchors it rests on.** [R-COC-01] already does this for one input —
*"a sovereign quote older than 14 days REFUSES rather than being used quietly; it may be
accepted deliberately and the staleness is then DISCLOSED in the record."* The currency anchor
has no such guard, and it is the input from which the whole purchasing-power wedge and every
translated line descend.

The natural shape is the one already in the book: refuse past a stated age, allow deliberate
acceptance, disclose the staleness in the record. That is a rule amendment for both governing
documents with an identifier and a negative control — recorded here with its arithmetic, not
done in passing.

**Read the dates live** — `python3 engine/macro_path.py EG` — never from this note.

---

## Measured: it is four names, not one

[R-LESSON-01] says to file at the narrower scope and widen only when a second company shows
the same thing, because one observation is not a pattern. PHAR was one observation. Measured
across every Egyptian study that commits a strike date:

| EGP study | strike date | days after the currency anchor |
|---|---|---|
| AMOC | 2026-09-03 | **+28** |
| ARCC | 2026-09-03 | **+28** |
| PHAR | 2026-09-03 | **+28** |
| SCEM | 2026-09-02 | **+27** |
| ELEC | 2026-08-05 | −1 |
| SWDY | 2026-08-05 | −1 |

**Four of six are struck 27–28 days after the anchor their currency path rests on.** The two
that are not were struck the day before it, which is the only reason they are clean — not a
property of those studies.

So this is not PHAR's quirk. It is what happens to **every** study delivered under
[R-GAP-01 AMENDED]'s latest-price requirement while the house path's currency anchor stays
where it was, and it will happen to every study delivered tomorrow.

**The bar for widening is met.** What is still owed before this becomes a rule is the thing
this house owes every rule: an identifier, both governing documents in one commit, and a
negative control that reinjects the condition — a path whose anchor is older than the strike
date must go RED, and a path refreshed to the strike date must stay GREEN.

**Read the dates live** — `python3 engine/macro_path.py EG` and each study's own strike date —
never from this table, because both move.
