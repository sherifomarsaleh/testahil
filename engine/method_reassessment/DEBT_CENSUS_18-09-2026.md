# What the book owes, counted in one place

**18 September 2026. Measured across every ratchet. Nothing here moves a fair value.**

## The number nobody had

`[R-ENF-02]` is right that a ratchet is the way to carry a known debt: a check red from
the day it is written is one everybody learns to ignore. `[R-REPAIR-01]` is right that a
system which only detects accumulates debt at exactly the rate it detects, and that
**every individual entry is legitimate**, which is what makes the total invisible.

`[R-REPAIR-01]` was adopted on *"47 ratchet entries accumulated on five studies"* — read
off the lists somebody happened to open. Counted across all **67** ratchets:

| | entries | names |
|---|---|---|
| studies that exist on disk | **274** | 24 |
| names the site publishes with **no study directory** | **112** | 70 |
| **total** | **386** | **94** |

The gap between 47 and 386 is not an error in either number. It is what a total looks
like when nothing computes it.

## The reader refuses rather than classifies, and that is where the findings were

`engine/study_debt.py` classifies every ratchet key against two **closed named lists**
and raises on anything else. Its first run refused **eleven keys** across the 67 files,
and every one needed a decision no pattern could make:

- an **unrunnable** figure script *is* a debt (red, never skipped);
- **findings**, **breach_no_review**, **review_central_unstated**, **unscored** and
  **runs** are debts;
- **closed** (entries resolved and kept as the record of why), **aliases** (a name
  mapping), **signature** (`[R-ENF-08]` failure signatures beside their entries) and
  **scope_widened** (a dated record that a gate's scope grew) are not.

It then refused **two names** — `ADXGENERAL` and `DFMGI` — which turned out to be
**index series** under `[R-IDX-01]`'s held-unregistered list, resolving against
`engine/raw_indices/` rather than against the study directories. A name checked against
the wrong population is worse than one unchecked.

And it found **`2POINTZERO`**. The first draft's ticker pattern required a leading
letter and silently dropped it — **the same name this protocol already records as
having been dropped from three separate tools by a regex written the same way.** It
surfaced only because the reader refuses an unclassified key instead of skipping it.

## No ceiling, deliberately

`scripts/check_study_debt.py` sets **no bar on the total**. A new standard legitimately
adds entries on the day it is adopted — that is what `[R-ENF-02]` exists for — so a
ceiling would fire on a rule being written, which is the permanently-red check that rule
forbids. What it refuses is the three ways a count stops being a count:

1. an **unrecognised key**, which a reader would otherwise absorb silently;
2. a **name that resolves to no study, no published name and no index**;
3. **zero ratchets read**, or zero entries found across them.

The count is reported, dated and committed to `debt_snapshot.json`, so **movement** is
visible — the one thing a pile of individually-correct lists cannot show.

## Beside it: criterion 6 is not blocked by anything missing

Part E criterion 6 asks that the publish queue hold **four files per name** — the study
in Word and in PDF, the standalone bibliography, and the 16-sheet workbook — **each
opened and read**. The reading is a human act and no script may attest it.

`scripts/publish_queue.py` resolves the rest. Measured today: **23 names deliver
documents and all 23 hold all four — 92 files, nothing short.** The queue prints in
reading order with paths.

That matters because an earlier pass in this same programme reported five studies
missing two of four deliverables while every file was on disk, having counted keys in a
publish manifest that lists two by design. **The files were always there.** Criterion 6
is one sitting away from closed, and it is the principal's to close.

---

**The general lesson, which is not about ratchets:** *a pile of individually-correct
lists has a total, and nobody who maintains one of them can see it.* Each list is owned
by whoever wrote the rule it belongs to, each may only shorten, and each is read by
somebody checking one thing. The total belongs to nobody, which is exactly why it grew
eight-fold without anyone being wrong.
