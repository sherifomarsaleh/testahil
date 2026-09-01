# EMFD — fundamental walk-forward training: BLOCKED, awaiting documents

**Instrument:** Emaar Misr for Development Company (S.A.E.) · EGX:EMFD · market EG
**Opened:** 1 September 2026 · **Standing rule:** [R-FCAL-01], with [R-LESSON-01] for its
second document.

## Status in one line

The run is **blocked at §1** — the three most recent fiscal years cannot be obtained from
the company's audited statements or its own investor-relations documents — and the
documents are requested. No panel exists, no projection has been run, no error has been
computed, and no delivered EMFD number has moved.

## Why this directory is not named `emfd_walkforward`

`scripts/check_lessons_register.py` anchors its population on directories ending in
`_walkforward` and fails when one of them has produced no lesson and no resolved harvest.
That is correct, and it is aimed at exactly this shape of thing: a directory that looks like
a completed run while holding nothing. This run has produced no walk-forward lesson because
it has produced no walk-forward, so it does not claim the name. When the blocked documents
arrive and the run executes, its outputs move to `engine/emfd_walkforward/` and the gate
applies to it in full.

## What is here

| file | what it is |
|---|---|
| `fetch_sources.py` | resolves the company's own IR document register, downloads and hashes every document on it, and probes — and logs — every route to the years it stops short of |
| `ir_register.json` | the register as the company publishes it: 50 documents, FY2013–H1-2021, with sha256 and byte counts |
| `fetch_attempts.json` | every HTTP attempt, successes **and** failures, one record per try |
| `extract_survey.py` → `extraction_survey.json` | which statement pages carry a text layer, which are scans needing OCR, and whether each profit-or-loss statement **foots against its own arithmetic** |
| `restatement_check.py` → `restatements.json` | each annual statement's two columns differenced, so the restatement history is measured rather than remembered; also the one interim period published on both revenue bases |
| `build_records.py` | renders the four documents below from the JSON above — **nothing in them is typed** |
| `SOURCE_REGISTER_01-09-2026.md` | the Sweep Register: what was obtained, from where, and every route that failed |
| `SCOPE_DECISION_01-09-2026.md` | the decision, its arithmetic, and exactly what is needed to lift the block |
| `BASIS_BREAKS_01-09-2026.md` | the basis-break register — two breaks found and measured |
| `PRE_REGISTRATION_01-09-2026.md` | origins, horizons, drivers, mechanical rules, benchmarks, score, bootstrap, macro split, sample roles and corrections — fixed in advance |

## Reproduce

```
python3 engine/emfd_walkforward_pending/fetch_sources.py       # ~92 MB, writes PDFs to scratch
python3 engine/emfd_walkforward_pending/extract_survey.py
python3 engine/emfd_walkforward_pending/restatement_check.py
python3 engine/emfd_walkforward_pending/build_records.py
```

PDFs are written outside the repository (`EMFD_SCRATCH`); only the register, the hashes and
the extracted numbers are committed.

## What lifts the block

FY2021–FY2025 audited consolidated financial statements plus every disclosed 2026 quarter,
and the results releases alongside them (L-008 — the release carries the delivered-unit
counts and contracted-sales values that no financial statement holds, and this class of
company is driven by exactly those). With those in hand the panel spans FY2013–FY2025, the
origins run FY2017–FY2024 with horizons to five, and the run is a **FULL** one under §0.
