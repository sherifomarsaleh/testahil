---
name: lessons
description: Read or update the TESTAHIL lessons register — what every study taught us, scoped to one company, to a class of company, or to every study. Use when the user asks what we learned from a study or walk-forward, what binds on a stock or a class before starting work, to add a lesson, or to rebuild the register documents. Also use before starting any new study or update, to load what already binds on that name.
---

# The lessons register

Everything this research has learned, in plain language, each tagged with how
far it travels: **ALL** (every study), **CLASS** (every company that works the
same way), **STOCK** (one company and nowhere else).

Applying a STOCK lesson to another company is superstition. Read the counts
live — never quote them from any document, including this one.

## Reading it

```
python3 engine/lessons.py                          what binds on every study
python3 engine/lessons.py PHDC                     ALL + PHDC's own
python3 engine/lessons.py PHDC --class developer   everything for a PHDC update
python3 engine/lessons.py --class telecom          for a new telecom study
python3 engine/lessons.py --classes                which classes are registered
python3 engine/lessons.py --scope CLASS            one scope only
python3 engine/lessons.py --search cash            anything mentioning a word
python3 engine/lessons.py --open                   recorded, not yet acted on
python3 engine/lessons.py --counts                 the live counts
```

The reader-facing documents are `engine/Lessons_Register.md` and
`engine/Lessons_Register.docx`. Both are GENERATED — never hand-edit either.

**Before starting any study or update**, run it for that name and class and
work from what comes back. That is the point of the register.

## Adding lessons after a walk-forward run

```
python3 engine/lessons_harvest.py <TICKER>     read the run, draft candidates
#   -> engine/<ticker>_walkforward/lessons_draft.json
#   decide each draft: set scope + applies_to + confirmed:true,
#   or set declined:"<reason>"
python3 engine/lessons_add.py <TICKER>         append and regenerate
python3 engine/build_lessons_docx.py           refresh the Word file
python3 scripts/check_lessons_register.py      confirm the gate is green
```

The harvester fills in the evidence from the run's own committed numbers, so a
lesson's "how we know" clause cannot drift from what was measured.

**Choosing the scope is deliberately not automated.** It is a judgement, and it
is costly in both directions: too narrow and the next study repeats the mistake,
too broad and one company's quirk becomes a house rule nobody can dislodge. When
unsure, file at the narrower scope and widen when a second company shows the
same thing — one observation is not a pattern.

Every drafted finding must end **registered** or **declined with a reason**. One
that is neither fails the gate: an unanswered question must not pass as a clean
result.

## Adding a lesson found any other way

A critique response, a self-audit or a QC gate can produce a lesson too. Append
it to `LESSONS` in `engine/lessons_register.py` **in the same commit that
records the finding**, then regenerate both documents and run the check. Every
entry needs a plain-English statement, a scope, the evidence, and what would
overturn it — the module refuses one missing any of them.

## Rules this obeys

The standing rule is **[R-LESSON-01]**, in both governing documents. The
register is generated from `engine/lessons_register.py`; a document that states
a fact which moves must not be the thing that remembers it.
`scripts/check_lessons_register.py` runs in CI and FAILS — never warns — if the
Markdown is not its generator's byte-for-byte output, if the Word file is
missing a lesson, if any id fails to resolve both ways, if a registered class is
empty, if a lesson names a company this repository does not study, if a
walk-forward run has no lesson behind it, or if a harvested finding was never
ruled on.
