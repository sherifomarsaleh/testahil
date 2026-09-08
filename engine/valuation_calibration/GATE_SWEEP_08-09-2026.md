# The gates, run from outside the work they govern — 08-09-2026

**Condition 2 of [R-VCAL-02 CLAUSE TWO].** The clause defines this half as *"the
standing set every study is held to"* and says in terms that nothing else is an
adoption condition.

**READ IT LIVE.** This file records what was run on one day. The population and the
verdicts both move — a gate is added, a study is delivered, a ratchet shortens — so
this is evidence about 08-09-2026 and not a description of the gate set.

---

## What was run

Every `scripts/check_*.py` in the repository, each with its own timeout, plus the
import-not-parse checks on the modules the protocol names and the JavaScript
load-assert on `assets/data.js`.

## A finding about the SWEEP rather than about the book

The first pass ran the gates **eight at a time** and one came back red:
`check_data_freshness` reported *"TICKERS parsed to an empty object; an empty result
is not a clean result [R-ENF-04]"*. **Run alone it is green** — 93 entries against 93
libraries, zero failures.

The gate was right and the sweep was wrong: eight concurrent node processes contending
on one machine, and the parse returned nothing. **That is [R-ENF-04]'s own lesson
landing on the operator rather than on the repository** — when a probe comes back
empty, the first hypothesis is that the probe did not run, and re-running the exact
operation is what separates the two. **Every non-green result below was re-run
SERIALLY before it was believed.**

It is recorded here rather than quietly dropped because a parallel sweep is a
convenience that can manufacture exactly the failure the house's own rules are written
about, and the next operator reaching for one should know.

## Five gates were red at the start of the day and every one is closed

| gate | what it was | what it turned out to be |
|---|---|---|
| `fv_movement.py check` | a register recording a single base for a study now publishing a TWO-SIDED answer | **registered** as a new edition in the shape the study publishes, through the module |
| `build_publish_queue.py --check` | one study reported as shipping no report and no workbook | its files ship under **the company's other name**, not its ticker — matched by SHAPE now, as the bibliography gate already does |
| `check_anchor_ordering_negative_control` | 6 of 7 red cases passing | a study got **BETTER** and disarmed them: every release case stood on a live record that happened to be behind, and it caught up |
| `check_terminal_record_shape_negative_control` | asserted it renamed exactly 37 markers | the book grew to 38 — a study **gaining** a terminal record |
| `check_bibliography_negative_control` | the ratchet case had nothing to prove | that ratchet was **emptied** — the debt PAID |

**THREE OF THE FIVE ARE ONE DEFECT, and it was closed as a class rather than three
times [R-ENF-01]: a fixture whose subject is LIVE STATE moves when the state does.** It
moves in the direction that leaves a control looking thorough while injecting nothing,
or makes it refuse and report a sound gate as broken. **All three failed because the
work went RIGHT** — a study re-struck, a record added, a debt paid. Build the
condition; never borrow it.

## The debt that remains, countable rather than remembered

**78 ratchet entries across the five re-issued names.** Part E's own criterion 1 asks
the lists to carry only names not yet re-issued and is therefore NOT met — **on the
ratchet debt, not on any gate's colour**, all seven of the gates it names being green.
[R-VCAL-02 CLAUSE TWO]'s definition governs adoption and that reading is recorded in
the adoption record beside this file, with the number printed, because it is the one
reading in this record that could be self-serving.
