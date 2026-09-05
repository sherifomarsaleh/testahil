# The seven studies invisible to the valuation-gap gate — measured, on the third attempt

Written 5 September 2026. **Three earlier versions of this note were wrong**, each written
from a partial reading. What follows is what was verified in each study's own code, with
the verification named per row.

## The three wrong versions, kept because the pattern is the lesson

1. *"The causes split three ways — a filename, a bear/base/bull dict, a retired blend — and
   some fixes are cheap."* The filename and the dict are real and **neither is a sufficient
   cause**. Fix STC's filename and it is still unreadable.
2. *"AMR, and probably ADNOCDIST, ADNOCDRILL and BOROUGE, carry the retired blend."* Written
   with an explicit "probably" and then relied on anyway.
3. *"ADNOCDIST needs no valuation judgement at all — its two centres are already decided."*
   Written after opening the file and reading the top-level keys, stopping at the first
   interpretation that fit. `centre_A` and `centre_B` are each a **typed 40/25/20/15
   four-lens blend**, in two framings. Opening `items_A` would have taken ten seconds.

**The third is the instructive one**, because it was not a failure to look — it was
stopping at the first plausible reading of what was found. [L-334] is registered on the
first two; the third sharpens it.

## What is actually in each, verified in the study's own code

| study | the combination it publishes | verified at |
|---|---|---|
| **ADNOCDIST** | typed **40 / 25 / 20 / 15** across DCF, normalised earnings, relative and book — twice, as `centre_A` and `centre_B` | `lenses.items_A` / `items_B` / `shared` carry the weights explicitly |
| **ADNOCDRILL** | typed **25 / 25 / 20 / 15 / 15** across two DCF frames, relative, book and normalised | `fair_value.weights` |
| **BOROUGE** | the **MEDIAN of nine lens readings** spanning two beta framings and two scenarios | `compute.py:722`, `FAIR_MID = float(np.median(vals))` |
| **ELEC** | typed **40 / 20 / 20 / 20**, and the delivered document prints the words "Blend 40 / 20 / 20 / 20" | `compute.py:505`; `docx_elec.py:103` |
| **GBCO** | typed **40 / 15 / 20 / 25** across SOTP, pre-discount, relative and normalised | `compute.py:258-260` |
| **STC** | typed **35 / 25 / 20 / 20** across DCF, dividend model, relative and normalised | `stc_compute.py:277` |
| **AMR** | typed **50 / 20 / 20 / 10** across DCF, relative, normalised and book | `lenses.weights` |

## The finding, which was my first hypothesis, dismissed, and is now measured

**All seven carry a multi-lens combination that [R-LENS-03] retired**, and that is *why*
none of them exposes a single central. **Unreadability to the valuation-gap gate is a
symptom of the retired blend, not a separate defect.** The group is homogeneous; there is
no cheap subset, and the ordering in the previous version of this note was built on a
distinction that does not exist.

BOROUGE is the one worth naming separately, and not because it is easier: a *median across
constructions* is not a weighted average, and it is caught by the same rule for the same
reason — *"a number produced by averaging several methods is not more robust than the best
of them; it is a NEW method with free parameters nobody tested."* A median across two beta
framings and two scenarios answers a question nobody asked.

**And that is the right outcome rather than a disappointing one.** A gate satisfiable by
re-keying a JSON file would be satisfiable by publishing exactly the number the standing
rule retired. These studies are invisible because the lens decision has not been made, and
the gate is correct to say nothing about them until it has.

## What each one needs, which is the same thing

Per [R-LENS-03]: **one class primary IS the central**; every other lens is a cross-check
published in the same table; the bear/full envelope is the RANGE of the present-value reads
on one clock, never an average. The registry is `research_protocol.LENS_REGISTRY`, keyed on
`lessons_register.CLASSES` by import.

The classes are already recorded in each study's own metadata — ADNOCDIST an operating
company, STC a telecom, GBCO a holdco, BOROUGE petrochemical, AMR a restaurant group,
ADNOCDRILL an offshore driller, ELEC a cable manufacturer — so no taxonomy work is needed
first. **What each needs is one decision, applied, and the blend removed** — the same lever
AIRARABIA took, where it was worth +9.8%.

STC carries a second, independent reason to be a rebuild rather than a patch: it predates
the v2 cost-of-capital method, and its own compute imports a retired engine module.
