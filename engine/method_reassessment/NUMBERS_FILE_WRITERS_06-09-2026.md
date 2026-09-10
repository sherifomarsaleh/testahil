# Three studies' numbers files need two generators, and nothing said so

**Dated 6 September 2026.** Found while closing an unrelated defect: adding one line to
SWDY's lens record and rebuilding it produced an **18-line diff**, and the sixteen deleted
lines were that study's entire [R-ANCHOR-01] `forecast_anchor` record.

---

## What happened

`engine/swdy_study/study_numbers.json` is written **whole** by `compute.py`. Its
`forecast_anchor` block is appended **afterwards** by a second script,
`swdy_study/forecast_anchor.py`. Nothing in either file, or anywhere else, said so.

So running the main generator alone deleted a long, carefully evidenced standing-rule
record — the one stating that no closed-list mechanism in [R-ANCHOR-01] is supported by
that company's filings. Restored by running the second generator; verified byte-identical
against HEAD.

**It was caught by reading a diffstat, not by a gate.** No gate could have caught it: a gate
reads the file that is there and cannot know what a rebuild removed.

## The class, measured

`study_numbers.json` written by more than one script:

| study | main generator | second writer | what the second writer adds |
|---|---|---|---|
| **EGCH** | `compute.py` | `lenses.py` | `central`, `central_two_sided`, `spot`, `fair`, `lens_record`, `bridge_record`, `macro_record`, `forecast_anchor` |
| **SAVOLA** | `compute.py` | `forecast_anchor.py` | `forecast_anchor` |
| **SWDY** | `compute.py` | `forecast_anchor.py` | `forecast_anchor` |

**EGCH is the severe one.** A rebuild running only its `compute.py` removes **the study's
own central and spot** — the two fields `check_valuation_gap` reads — plus three
standing-rule records. Every gate downstream would then report on a file that had quietly
lost them, and would report clean, because each of those gates treats a missing field as an
*unreadable study* rather than as *a rebuild that deleted the answer*.

Run-order notes are now the first thing in all three files' docstrings.

## The instrument already exists, in three studies out of twenty-four

`empower_study/diagnostics_empower.py`, and the same shape in `borouge` and `du`:

```python
NUMBERS = os.path.join(HERE, 'study_numbers.json')
_BEFORE = open(NUMBERS, 'rb').read()
import compute as C
if open(NUMBERS, 'rb').read() != _BEFORE:
    open(NUMBERS, 'wb').write(_BEFORE)
    raise SystemExit('REFUSED: importing the model moved study_numbers.json. Restored. '
                     'A diagnostic may not move the valuation it is measuring.')
```

Read the file, run the model, and if the bytes moved, **restore and refuse.** That is
exactly the check this defect needs, generalised: *a study's committed numbers file
reproduces from its own declared generators, run in their declared order.* It is
implemented in three places and binds nowhere else — which is the prose-figures finding
verbatim: **a rule that one study implements is a rule that one study obeys.**

## The detector had to be re-pointed twice, and both directions are recorded

Static detection of "which scripts write this file" is not the one-line grep it looks like.

1. **It under-detected.** A first pass resolved only `X = <literal mentioning
   study_numbers>` and reported **DU as having no writer at all** — DU builds the filename
   through a ternary and then a join, two hops. An absent answer wearing the costume of a
   clean one [R-ENF-04]. Fixed by following the variable chain to a fixpoint.
2. **It then over-detected.** Following the chain tainted `doc = json.load(open(NUMBERS))`
   and everything built from it, so **EMPOWER and FERTIGLOBE** were flagged — both of which
   write `diagnostics.json`. Fixed by not tainting through file *content*: a path is not
   what a file said.
3. **And one of those false positives was the opposite of a defect.** EMPOWER's flagged
   write is the restore-and-refuse guard above. The detector's second draft was pointing at
   the one study that had already solved the problem.

The final detector finds a writer for all 24 studies and excludes both known-clean cases,
which is the pair of conditions any successor must keep passing.

## Not done here

Turning the three-study guard into a shared instrument — *the committed numbers file
reproduces from its declared generators in their declared order* — with the declaration
somewhere a checker can read, is a rule amendment with a gate, a ratchet and a negative
control. It is the next unit, not a change made in passing.
