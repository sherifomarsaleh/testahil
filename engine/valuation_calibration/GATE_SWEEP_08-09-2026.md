# The gates, run from outside the work they govern — 08-09-2026

**Condition 2 of [R-VCAL-02 CLAUSE TWO].** The clause defines this half as *"the
standing set every study is held to"* and says in terms that nothing else is an
adoption condition.

**READ IT LIVE.** This file records what was run on one day. The population and the
verdicts both move — a gate is added, a study is delivered, a ratchet shortens — so
this is evidence about 08-09-2026 and not a description of the gate set.

---

## What was run

**Every `scripts/check_*.py` in the repository — 159 of them** — each with its own
timeout, plus the import-not-parse checks on the modules the protocol names and the
JavaScript load-assert on `assets/data.js`.

**Result: 158 completed, 156 green, and BOTH reds were artefacts of how the sweep was
run rather than defects in the book** — each is named below with the serial re-run that
settles it. The import checks passed on all nine named modules and `node --check` passed
on `assets/data.js`.

**The 159th, `check_new_study_gauntlet_negative_control`, took three attempts and the
first two were killed by the operator, not by the gate** — it plants a weakened gate and
re-runs the whole set inside a sandbox for EVERY case, which is the most expensive check
in the repository. Its subject, `check_new_study_gauntlet`, was GREEN both serially and
in the parallel sweep.

**AND IT FILLED THE DISK, WHICH IS THE THIRD OPERATOR ARTEFACT OF THE DAY AND THE ONLY
ONE THAT COULD HAVE COST SOMETHING.** Each sandbox is a 1.4 GB copy of the repository;
running the control several times over and killing the copies mid-flight orphaned eight
of them, and `/tmp` reached zero bytes free. Writes then failed with ENOSPC while
DELETES still succeeded, so clearing the orphans recovered 17 GB immediately.

**THE REPOSITORY WAS UNTOUCHED AND THAT IS THE POINT WORTH RECORDING**, not a relief:
zero tracked files modified or deleted, HEAD where it was, nothing unpushed. The gauntlet
works entirely inside its own copies, so a disk filling and being cleared reached nothing
committed — which is [R-ENF-01]'s own rule about a check that needs different inputs
being GIVEN different inputs rather than handed the real ones with a plan to put them
back. **A control that had sandboxed less politely would have taken the tree down with
it.**

**An unfinished run is not a green run**, and neither is one whose sandbox ran out of
room — a check starved of disk reports on a partial copy, which is [R-ENF-04]'s absent
answer wearing a clean one's clothes with a filesystem underneath it.

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

A SECOND RED WAS THE SAME KIND OF THING AND IS RECORDED FOR THE SAME REASON.
`check_tree_unmodified` failed with *"the baseline was recorded at c5762580 and HEAD is
now b193d268, so it describes a different tree."* **That is the gate working exactly as
it is built to.** It is a TWO-HALVES instrument — `--record` first, the comparison last,
with the checks in between — and a bulk sweep that runs every script alphabetically runs
the comparison half against whatever baseline happens to be lying about. Run as the two
halves it is: **0 tracked files modified before the run, 0 after.**

Both are recorded rather than quietly dropped because a parallel sweep is a convenience
that can manufacture exactly the failure the house's own rules are written about, and
the next operator reaching for one should know. **NEITHER WAS A DEFECT IN THE BOOK AND
BOTH LOOKED LIKE ONE.**

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
