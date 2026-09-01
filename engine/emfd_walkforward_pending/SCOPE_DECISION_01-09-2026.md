# EMFD — fundamental walk-forward: SCOPE DECISION

**Instrument:** Emaar Misr for Development Company (S.A.E.) · EGX:EMFD · market EG · exchange EGX
**Class:** real-estate developer, off-plan, percentage-of-completion
**Decided:** 1 September 2026, before any projection was run.

## Decision

**The run does not start. It is BLOCKED at [R-FCAL-01] §1 and the documents are requested.**

This is not the §0 SKIP verdict and it must not be recorded as one. SKIP is for a company
whose history is too short — *"walk-forward not run — insufficient sourceable history (N
years)"*. EMFD's history is not short. Its recent statements are not reachable from here.
Those are different facts and they call for different words.

## Why

§1 is unconditional: *"The most recent 3 fiscal years and all current-year quarters MUST
come from the company's audited financial statements or its own website/investor-relations
documents. No exception: if they cannot be obtained, STOP and ask for the documents."*

The company's own investor-relations register publishes financial statements from FY2013
to H1-2021 and stops. Everything from FY2021 onward — which is to say the three most
recent fiscal years and every quarter of the current one — is absent from it. The exchange
carries those filings and answers automated requests with an anti-bot interstitial; the
company's own embedded IR backend serves on a port this session's egress policy does not
permit; a JavaScript-capable browser cannot reach any host from here, verified against a
control. Every route and its outcome is in `SOURCE_REGISTER_01-09-2026.md`.

Aggregator figures for the missing years are readily available and were deliberately not
used. SIGCM clause 1 bars a data vendor as the source of the subject's own reported
historicals; §1 restates it with the words "no exception". Substituting them would produce
a training record whose errors are partly transcription noise from somebody else's
spreadsheet — measuring our method against a vendor's arithmetic rather than against what
the company reported.

## What the obtainable window would and would not support

Even setting §1's rule aside, the window that IS obtainable does not carry a training
record. Complete fiscal years from the company's own statements: **2013–2020
(8 years)**. An origin needs five prior complete years, so the admissible
origins are FY2017, FY2018, FY2019, FY2020, and actuals stop at FY2020:

| origin | horizons that resolve | cells |
|---|---|---|
| 2017 | 1, 2, 3 | 3 |
| 2018 | 1, 2 | 2 |
| 2019 | 1 | 1 |
| 2020 | — | 0 |

**6 scoreable (origin, horizon) cells in total, none beyond horizon 3.** The
reference run on a comparable name carried 40 cells to horizon 5, and its own record still
states that its corrections rest on too few origins to be independent. 6 overlapping
cells is not a smaller version of that. It is not a training record.

Three further things are true of that window, each of them sufficient on its own:

1. **No era split exists.** Every one of those cells sits after the November 2016 float and
   before the 2022–24 devaluations. §5 applies a correction *only where the bias holds its
   sign across eras*; with one era there is nothing to hold a sign across. The corrections
   step is unevaluable by construction, not merely weak.
2. **The revenue definition changes at the window's edge.** EAS 48 took effect on
   1 January 2021 and this company adopted it then, restating the one overlapping period's
   revenue and cost (see `BASIS_BREAKS_01-09-2026.md`, B1). §1 scores unit drivers only inside
   their own definition window. The obtainable window ends where the current definition
   begins, so the two do not overlap at all.
3. **The purpose would not be served.** The two purposes are per-driver bias detection and
   calibrated ranges for years 3–5 of the update now being written. A record whose newest
   origin is FY2020 produces neither for a forecast starting in 2026 — it would describe
   how the method behaved in a currency regime and an accounting basis that have both since
   been replaced.

## What is needed to lift the block

Any of the following, for **FY2021, FY2022, FY2023, FY2024 and FY2025**, plus every 2026
quarter already disclosed:

1. the audited consolidated financial statements as filed (the exchange's own PDFs are the
   documents themselves and are acceptable — the obstacle is reaching them, not their
   provenance); or
2. the same statements from the company's investor-relations channel; or
3. the annual reports carrying them.

The earnings releases for those years are wanted alongside the statements, not instead of
them: L-008 — *a period is not researched until both its statements and its results release
are in*, because the release carries the sales value, the delivery counts and the backlog
that no financial statement holds, and this class of company is driven by exactly those.

With FY2021–FY2025 in hand the panel spans FY2013–FY2025 — thirteen complete fiscal
years, comfortably a **FULL** run under §0 — and the origins run to FY2024 with horizons to
five, spanning both currency eras and both revenue bases. That is a real record. It is
about five documents away.

## What was done anyway, and what was not

Done, and committed:

* the full source sweep, with every attempt logged and every obtained document hashed;
* the extraction survey — which statements yield a text layer, which need OCR, and whether
  each one **foots** against its own arithmetic;
* the restatement comparison, which found and measured two basis breaks;
* the basis-break register those findings feed;
* **the pre-registration, written in full now** — before any error has been computed, which
  is the only moment at which it can honestly be written. Nothing in it can be tuned to a
  result that does not exist yet.

Not done, and not to be represented as done: the panel, any projection, any error cell, any
correction, the two documents §6 requires, and any change to a delivered EMFD number. The
existing EMFD study and its published cone are untouched by this work.
