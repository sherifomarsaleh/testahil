# An income-statement chain check, measured and NOT adopted

**03-Sep-2026. This records a gate that was built, measured twice and declined, so the
next session starts from the measurement rather than from the idea.**

## What provoked it

Reading PHDC's delivered page 4 and adding the column up. The forecast income statement
printed Revenue, Cost of revenue, Gross profit, Overheads, Operating profit — and
`gross − overheads` came out **EGP 393mn above the printed operating profit** in 2026,
rising to **1,039mn** by 2031. The model computes `EBIT = gross − sga − da` and the table
never printed the depreciation row. Every figure in it was individually correct.

That is the same shape as ARCC's Table 3, which deducted provisions and credit losses in
the model and never printed the line. **Two studies, one defect, found both times by a
person reading rather than by any gate** — so it is a class, and [R-ENF-01] says close the
class.

`engine/table_footing.py` cannot see it, and the reason is exact: it fires on rows whose
LABEL declares them a total (`total`, `sum`, `subtotal`, `weighted average`, `blended`),
and **an income statement's subtotals are never labelled that way**. Gross profit,
operating profit, profit before tax and net profit are all roll-ups a reader adds up, and
none of them says so.

## What was measured

Over every delivered valuation study — 1,051 tables, 277 rows whose label is an
income-statement subtotal:

| construction | fires |
|---|---|
| each subtotal against **revenue** less every row between | **53%** |
| each subtotal against the **previous subtotal** less the rows between — an income statement is a CHAIN, not a set of independent totals | **27%** |

The second is the right shape and it halved the rate, which is the [R-COC-01] move working:
re-point the instrument at how the object really behaves rather than widen the tolerance.
It is still **one table in four**, and a gate firing at that rate is the permanently-red
check [R-ENF-02] forbids. **So it is not adopted.** Nothing here was loosened to make the
number look better, and the number is reported as it stands.

## Why the residue is not obviously defects

Spot-checked against the surviving cases, the instrument is still wrong about ordinary
layouts in at least these ways, and each would need its own fix before the rate means
anything:

- a **cost row skipped by the not-a-component filter** — ADNOCLS's gross profit prints 752
  where the chain expects 4,758, a gap the size of the cost line, so the cost row is being
  excluded by a label word rather than being absent
- **volume, per-unit and rate rows interleaved with currency rows**, which a filter keyed on
  label words catches unreliably; the honest discriminator is the UNIT of the column, which
  a table does not always state
- **an anchor that is not revenue** — several tables open on a segment or a volume and the
  first currency row is further down
- **sign conventions**: a cost shown in brackets is already negative and must be added, not
  subtracted, and both conventions appear across the book

## The alternative worth building instead

The defect is not really "the page does not add up" — it is **"the model deducts a term the
table does not print"**, which is a fact about the MODEL and the page together, and is
exact. A study declaring its own income-statement chain (`ebit = gross - sga - da`) can be
checked for a printed row per term with no ambiguity and no false positives. That is the
per-study-instrument pattern `prose_figures` and `footing_check` already use, and it is
where this should go next.

## What WAS done

PHDC's table now prints the depreciation line, and the printed rows reconcile to the
printed operating profit exactly. ARCC's was fixed when it was found. No gate yet stops the
third one.

---

# A second gate measured and declined the same hour: counts written as words

**The defect that provoked it was real.** PHDC's section 7 opened *"Five things are not
disclosed by the company"* while the READ FIRST twelve pages earlier computed the same
count from the model and said **six** — a study contradicting itself, in the sentence that
introduces the list a reader is about to count. A sixth gap had been registered and the
typed word stayed. Both are now computed from one helper, so they cannot disagree.

`check_prose_figures` could not see it, and the reason is exact: **"Five" is a word.** That
check matches numerals, and a count spelled out escapes it entirely.

## Measured

Across all 31 delivered valuation studies: **775 spelled-out counts qualifying a noun** —
"four lenses", "six gaps", "five origins", "three analysts". Every study carries them. So
the class is real and book-wide.

Of those, 92 use a noun that looked mappable to a collection the study commits, and 74
"disagreed" — **and almost every one of those is the instrument being wrong, not the
document.** ADNOCLS's `lenses` object has seven keys because it holds the central and two
beta-alternates alongside the four actual lenses; and "two lenses" inside *"the four lenses
are less independent of one another than four lenses should be"* is a phrase about a
subset, not a total.

## Declined, for the same reason as the chain check

A count word only means something against a collection somebody has NAMED, and no rule
maps `lenses` in a sentence to a key in a JSON file. Building it on a guess produces a gate
that fires four times in five on correct work — the permanently-red check [R-ENF-02]
forbids.

**The tractable design is the same one this repository already uses twice**: a per-study
declaration mapping a count phrase to the collection it counts, checked against the model.
That is what `prose_figures` and `footing_check` do, and it is where both this and the
income-statement chain should go.
