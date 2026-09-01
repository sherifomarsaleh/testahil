# PROMPT — BOOK-WIDE FUNDAMENTAL WALK-FORWARD CAMPAIGN

CAMPAIGN REVISION 2026-09-01a — bump this on every edit, however small. A copy without the
current stamp is stale on its face, without reading a word of it [R-DOC-01].

**Adopted 01-Sep-2026, per instruction — "fundamental backtest for all stocks in testahil
register one after the other", market order given, "the outcome in terms of the new vs old
fair value as well as the lessons learnt to go to the Fundamental Analysis Calibration
Register."**

This is the campaign wrapper. It runs `Fundamental_Walkforward_Prompt.md` — the single-name
protocol, unchanged — over every covered name in the register, in a fixed order, and routes
each run's two outcomes into the Fundamental Analysis Calibration Register.

**IT CHANGES NO RESEARCH METHOD.** Not a lens, not a driver rule, not a cost-of-capital
construction, not a calibration procedure. Scope decision, pre-registration, ground-up build,
scoring, corrections and the two required documents are exactly [R-FCAL-01] as written. What
is new here is only the order, the checkpoint, and the record of what moved.

---

## 0 · Which walk-forward this is

**THREE DIFFERENT TESTS IN THIS SYSTEM ARE ALL CALLED A WALK-FORWARD.** This campaign runs
exactly one of them — the FUNDAMENTAL one: drivers projected from a past origin, scored
against what the company actually reported. It is not the PRICE-ENGINE walk-forward (band
coverage on the Monte Carlo cone, `{ticker}_study/backtest_5y.py`) and not the TECHNICAL
walk-forward (`engine/lab/ta_calibration/`, the shipped read replayed on a 5/10/21-session
clock). Never write "the walk-forward" in any deliverable, commit message or reply without
saying which. Conflating them once already understated this project's evidence base badly, in
a document written to describe it.

Read the populations live, never from this file:

```
python3 scripts/check_lessons_register.py     fundamental runs, and their lessons
python3 scripts/check_tech_calibration.py     technical calibration population
python3 engine/campaign_queue.py              this campaign's queue and its position
```

---

## 1 · The queue — a rule here, the order in code

**MARKET ORDER IS FIXED BY THE INSTRUCTION AND IS NOT DERIVED FROM ANYTHING:**

> EGX → UAE (ADX + DFM) → KSA (Tadawul) → Qatar (QSE) → India (NSE) → Korea (KRX) → USA (NASDAQ)

**WITHIN EACH MARKET, OLDEST STANDARD FIRST** [R-STD-01], because that is what turns a
book-wide re-issue into a finite, countable queue instead of an open-ended one:

| tier | meaning |
|---|---|
| 1 · `reissue` | a study exists, built to an older standard or carrying no stamp at all |
| 2 · `first-build` | no study directory — the name carries a published fair value no current-standard study ever produced |
| 3 · `current` | a study stamped at the live `STANDARD_VERSION` — the incremental case, one new origin |

Alphabetical inside each tier, so the order is deterministic and two readings a week apart
differ only where the repository actually moved.

**THE ORDER ITSELF IS NEVER WRITTEN DOWN HERE.** The register moves — a name is added by
placing an OHLC file, a study is built, a standard is bumped — so a queue pasted into a
document would look authoritative and be wrong within a week. That is the stale-library
failure and the stale-digest failure, both already paid for. Resolve it live:

```
python3 engine/campaign_queue.py                 the whole queue, by market, with tiers
python3 engine/campaign_queue.py --market EG     one market
python3 engine/campaign_queue.py --next          the next name with no run directory
```

`campaign_queue.py` REFUSES rather than returning a short list: every covered name lands in
exactly one of queue-or-excluded and the two must sum to the register's own total, and every
study directory must resolve to a covered name or be declared. An empty or short queue is not
a clean queue [R-ENF-04].

**METALS ARE EXCLUDED BY CONSTRUCTION AND ARE NAMED, NOT DROPPED.** GOLD, SILVER and PLATINUM
have no issuer, no financial statements and no drivers; the fundamental method has nothing to
project and nothing to score. They appear in the exclusion list with that reason. Their absence
is a decision on the record, not a gap.

---

## 2 · Per name — the order of operations, and why the first step is first

For each name, in queue order:

### Step 1 — FREEZE THE OLD FAIR VALUE. BEFORE ANYTHING ELSE.

```
python3 engine/fv_movement.py snapshot {TICKER}
```

**THIS CANNOT BE DONE LATER AND THERE IS NO RECOVERY FROM SKIPPING IT.** The campaign's whole
purpose is new-versus-old fair value, and this campaign is the one sanctioned thing that MOVES
`TICKERS.{TICKER}.fair` — the standing rule is that `fair{bear,base,full}` is never touched
except by a real study refresh, and this is that refresh. The moment the rebuilt study writes
`assets/data.js`, the old number is gone from the only file that held it. `data.js` carries no
date and no standard stamp on `fair{}`, so it cannot be reconstructed afterwards either.

A FILE THAT STATES A FACT WHICH MOVES MUST NOT BE THE THING THAT REMEMBERS IT — the same rule
as the as-of stamps and the band record. `snapshot()` is append-only and refuses a second
capture, because a baseline read after the run is not a baseline and the movement computed
against it would be a fabricated zero. Where a baseline genuinely cannot be established, it is
declared unrecoverable **with its reason** (`--unrecoverable "..."`) and the movement is
reported as absent. PHDC is the worked case and the list may only ever shorten.

### Step 2 — Read what already binds on the name

```
python3 engine/lessons.py {TICKER} --class {CLASS}
```

ALL lessons bind. CLASS lessons bind only if the class matches. STOCK lessons bind on that name
alone — applying one elsewhere is superstition. Everything marked PROVISIONAL is a recorded
finding from a method that is not yet validated: read it, do not cite it as authority.

### Step 3 — Run the single-name protocol, unchanged

Follow `engine/Fundamental_Walkforward_Prompt.md` end to end: §0 scope decision (FULL / LIGHT /
SKIP, decided first and stated), §1 data with four-field provenance, §2 pre-registration written
before a single error is computed, §3 ground-up build at every origin, §4 score and diagnose,
§5 corrections tested under both clauses, §6 the two documents.

**IT IS NOT RESTATED HERE.** A rule restated in two places is the drift disease — this campaign
adds an order and a record, and if it also carried a copy of the protocol the two would part
company on the third amendment and nobody would know which was live.

Two things about that protocol bind harder in a campaign than in a single run:

- **CREATING `engine/{ticker}_walkforward/` IS THE COMMITMENT, NOT THE DELIVERY.**
  `scripts/check_lessons_register.py` anchors its population on the run directories on disk and
  FAILS — never warns — the moment one exists with no lesson behind it, or with a harvested
  candidate nobody ruled on. So CI goes red at Step 3 and stays red until Step 5 is finished.
  That is the gate working. Do not start a run you are not finishing.
- **THE SCOPE DECISION IS MADE PER NAME AND IS OFTEN `SKIP`.** Below five sourceable fiscal
  years the run does not happen, and the words are fixed: *"walk-forward not run — insufficient
  sourceable history (N years)"*, recorded in the study's register and its QC table. A SKIP is a
  completed queue position, not a deferred one.

### Step 4 — Record what the fair value did

```
python3 engine/fv_movement.py record {TICKER} \
    --bear {B} --base {M} --full {F} \
    --scope {full|light|skip} --origins "{FY.. h=..}" --lessons L-nnn,L-nnn
python3 engine/fv_movement.py build
```

`record` refuses a name with no frozen baseline, and refuses a range that is not ordered
bear ≤ base ≤ full. The register regenerates wholesale from the JSON and is never hand-edited.

### Step 5 — Route the lessons

```
python3 engine/lessons_harvest.py {TICKER}      drafts, evidence filled from the run's own numbers
#   rule on every draft: scope + applies_to + confirmed:true, OR declined:"<reason>"
python3 engine/lessons_add.py {TICKER}
python3 engine/build_lessons_docx.py
python3 scripts/check_lessons_register.py       must be green before the next name starts
python3 engine/fv_movement.py check             must be green before the next name starts
```

**THE JUDGEMENT IS THE SCOPE AND IT IS NOT AUTOMATED, DELIBERATELY.** Too narrow and the next
study repeats the mistake; too broad and one company's quirk becomes a house rule nobody can
dislodge. When unsure, file at the narrower scope and widen when a second company shows the
same thing — one observation is not a pattern. Every lesson carries what would overturn it; a
lesson with no falsifier is a habit, not a finding.

**A CLASS MUST BE REGISTERED BEFORE A LESSON CAN BE SCOPED TO IT.** `lessons_add.py` refuses an
unregistered class outright. The register holds eight classes today against ninety names
spanning many more, so registering a new class — in `engine/lessons_register.py`, with the same
commit as the lesson that needs it — is an ordinary and expected step of this campaign, not a
workaround.

### Step 6 — Close the position

Nothing is left half-done between names. Before moving to the next queue position, both gates
above are green, the Fundamental Driver Ledger carries this name's entry, and the study's own
code calls `assert_sigcm()`, `assert_beta_provenance()`, `assert_ground_up()` and
`assert_model_study()` with `scripts/check_study_provenance.py` reporting no new violation.

---

## 3 · THE CHECKPOINT — hard stop after EGX

**RUN ALL 37 EGX NAMES, THEN STOP. Do not begin the UAE block until the review below is
written.** [Per instruction, 01-Sep-2026.]

The reason is the honest state of the method, which this campaign does not get to assume away:
at the campaign's start the fundamental method had been walk-forward tested on **one name**.
Every finding it has produced is PROVISIONAL for that reason, and `lessons_register.py` refuses
to write one as adopted. A campaign that ran straight through would propagate a specification
error into ninety runs before anyone looked — and the PHDC record already contains two errors
of exactly that species, each large, robust and entirely spurious until it was taken apart.

The EGX review answers four questions in writing, and it is a document, not a feeling:

1. **Which of PHDC's findings generalised?** Name them, with the per-name evidence. A finding
   that held on one name and not on the other thirty-six is a STOCK lesson that was filed too
   broadly, and it is re-scoped now rather than left to harden.
2. **Which are class-bound?** EGX carries developers, banks, cement, pharma, chemicals and
   telecom. A rule true of developers is not evidence about banks. Where a finding differs by
   class, say so with the test that separates them — a set of per-class numbers is not a class
   finding.
3. **Did any driver specification break down?** Especially the two the protocol already calls
   out: interest built off anything other than the borrowings that actually bear it, and
   revenue and cost sitting on different recognition clocks. Both produced a large, robust,
   entirely spurious bias before. A specification error is not a calibration one and no
   correction factor may hide it.
4. **Is the method beating "no change" yet?** On PHDC it did not, on net profit, at any
   horizon. If it still does not across thirty-seven names, that is the campaign's most
   important finding and it is written down plainly — A METHOD THAT CANNOT BEAT "NO CHANGE"
   HAS NOT EARNED THE PRECISION IT DISPLAYS.

**THE CHECKPOINT CAN STOP THE CAMPAIGN.** If the review finds a specification defect, the fix
comes first and the affected EGX runs are re-run before UAE begins. A checkpoint that has never
changed an outcome is decorative, and this project has already retired one test for exactly
that.

---

## 4 · Where the outcomes go

The **Fundamental Analysis Calibration Register** is two generated files. Neither is
hand-edited; both regenerate wholesale.

| half | file | generated by | holds |
|---|---|---|---|
| lessons | `engine/Lessons_Register.md` / `.docx` | `engine/lessons_register.py` | every lesson, scoped ALL / CLASS / STOCK, with how it was learned and what would overturn it |
| fair value | `engine/Fundamental_Calibration_FV_Register.md` | `engine/fv_movement.py` ← `fv_movement.json` | old vs new fair value per name, by market, in queue order, cross-referenced to the lesson ids from that run |

They are cross-referenced by lesson id and **never duplicated** — a fact stated in two places
parts company on the third amendment.

**BOTH ARE INTERNAL.** The training record, the panel, the error cells, the pre-registration and
this register are never shown to a reader. Nothing reaches the live site without a separate,
explicit publish request. No rating, no price target, no buy/sell language anywhere in either —
a range and the reasoning behind it.

### One thing the fair-value column must not be read as saying

For the 67 names in the `first-build` tier, the "old" fair value is a number **no
current-standard study produced**. The 23-Aug-2026 book-wide audit found 63 of 90 names not
built ground up and only 4 carrying an attestable beta. So for most of the book the movement
column measures *a new study against a number of unknown provenance*, not one method against
another. Say that wherever the column is quoted. A large move on a first-build name is mostly
evidence about the old number, and reading it as a valuation change would be the same error as
publishing a percentage without its count.

---

## 5 · Resuming, and what "in flight" means

The campaign will be interrupted. `python3 engine/campaign_queue.py --next` reports the next
name with no run directory, and both gates report their own state, so the position is always
recoverable from the repository rather than from anyone's memory.

A name is **in flight** if it has a frozen baseline or a run directory and no recorded fair
value. `fv_movement.py check` names them, and it is anchored on the run directories on disk —
not on its own JSON — so a register that stopped being fed FAILS rather than reporting clean.
Finish an in-flight name before starting a new one.

---

## 6 · The scale, stated rather than discovered

Ninety names. Each `first-build` name needs a full study — 16-section Word document, 16-sheet
live-formula workbook, standalone bibliography, four gates, an independent recalculation of the
delivered workbook, the external-reader scrub, and every figure inspected as a rendered image —
**and** a walk-forward run beneath it. This is the largest programme this repository has
attempted, by a wide margin, and the estimate is not improved by leaving it unsaid.

Three consequences follow, and they are the campaign's design rather than concessions:

- **Names are finished one at a time.** Both gates green before the next begins. Ninety runs at
  partial completion is a book-wide half-finish that nobody can audit.
- **The first market is also the validation.** That is what §3's checkpoint is for.
- **A SKIP is a result.** Below five sourceable fiscal years the run does not happen, in those
  words. Sourceable history is a fact about the archive, not a failure of the campaign, and
  padding a panel to reach a threshold would corrupt the very error being scored.

---

## 7 · Standing refusals

- **NEVER estimate, interpolate or infer a figure to fill a gap.** Leave the year out and
  shorten the window. A fabricated cell corrupts the error it is scored on.
- **NEVER skip Step 1.** A movement computed against a post-run baseline is a fabricated zero.
- **NEVER promote a correction on the first clause alone.** It must also match how that driver
  class is built across the market's book. That second clause has already done its job once,
  and what it caught was arithmetic wearing the costume of evidence.
- **NEVER mark a fundamental lesson adopted.** They are PROVISIONAL while the method rests on
  too few names, and the code enforces it.
- **NEVER carry a finding sideways between lenses.** [R-LENS-01] stands: no output and no
  calibration record of one lens is an input to another. Comparison surfaces read both and feed
  nothing back.
- **NEVER publish from this campaign.** Moving `fair{}` in `assets/data.js` is part of the
  rebuild; putting it live is a separate, explicitly-requested step.
