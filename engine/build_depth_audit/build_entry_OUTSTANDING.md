# Studies with no single build entry point

**03-Sep-2026. Measured, not estimated: 2 of 24 study directories have one.**

| has one | scripts |
|---|---|
| EGCH `run_all.py` | 33 |
| TMGH `build_all.py` | 23 |

The other twenty-two carry between 7 and 32 scripts each that must be run in the right
order, by hand, from memory: AMOC 32, ADNOCDRILL 24, ARCC 24, ADNOCLS 22, PHDC 22,
BOROUGE 21, FERTIGLOBE 21, SAVOLA 21, AMR 20, DU 20, PHAR 19, SWDY 19, AIRARABIA 18,
MODON 18, SCEM 18, ADNOCDIST 17, EMPOWER 17, RIYADHCABLE 16, ELEC 13, GBCO 13, STC 12,
XPT 7.

## Why this is the cause rather than another instance

[R-ENF-06] was adopted on three studies whose delivered documents were built from artefacts
that had moved: AMOC's `case_adversarial.json` at a base central of 5.954 against a
published 11.834, ARCC's `efg_bridge.json`, EGCH's `diagnostics.json` and
`contested_judgements.json` a full edition behind. Its remedy is that an artefact declares
the answer it was generated against, so a stale one can be told from a current one.

**That detects staleness; it does not prevent it.** In a single afternoon on TMGH — a study
already conforming to that rule — four more artefacts went stale, every one for the same
reason and none of them carelessness about a number:

- `statements.json` two days behind the model, and read by nothing at all;
- `peers.json` five weeks behind **this repository's own committed price libraries**;
- `experts.json` quoting a reverse read that had since been corrected;
- a note added to `experts.py` that never reached the page, because the script that writes
  its file was not re-run after the edit.

Each is the ordinary consequence of a pipeline whose steps a person has to remember. The
fix for that is not to remember harder.

## The companion to [R-ENF-06]'s lesson

That rule says: a file every builder reads and nothing writes is a number frozen at the
moment somebody last typed it. **The companion is that a file something writes, when
nothing makes it run, is frozen just the same** — and it is harder to see, because it has a
generator, so the question "what writes this?" gets a reassuring answer.

## What closes an entry

The study's next re-issue. An entry point costs an hour, states the dependency order
explicitly rather than leaving it implicit in the order somebody happens to run things, and
ends with the checks, so a build that produced a stale artefact cannot also report clean.
`engine/tmgh_study/build_all.py` is the worked pattern.

## Deliberately not a gate yet

A gate requiring the file would be ratcheted at 22 of 24 — nearly everything — and would
check that a file EXISTS rather than that the build is current, which is the "count the
file, don't run the instrument" failure that every gate adopted this week was careful to
avoid. The check worth having re-runs each generator and compares its output to what is
committed; that is affordable per study and not yet affordable book-wide. Recorded here so
the decision is visible rather than forgotten.
