# THE 90-NAME RECALIBRATION — how the programme runs

**PLAN REVISION 2026-09-17d.** Per instruction, 17 September 2026: *"I want all 90 stocks
recalibrated. All of them."*

**THIS IS A SPINE OVER THREE DOCUMENTS THAT ALREADY EXIST AND IT RESTATES NONE OF THEM.**
`Recalibration_Runbook_17-09-2026.md` is the order of work for ONE name.
`Fundamental_Walkforward_Campaign_Prompt.md` is the book-wide wrapper and owns the queue,
the per-name order and the standing refusals. `Publish_Protocol.md` owns going live. What
none of them answers is the question this file exists for: **in what ORDER, with how much
outside auditing, and where does Phase 1 sit.**

Nothing here is a standing rule. It is an operating order over rules adopted elsewhere and
it may not amend, soften or reinterpret any of them.

---

## 0 · WHAT REVISION a GOT WRONG, AND WHY IT MATTERS MORE THAN THE CORRECTION

**Revision a said 67 of the 90 names had no study. Every one of the ninety has a delivered
valuation study.** The principal said so and was right; this document said otherwise because
it took its population from `python3 engine/campaign_queue.py`, which resolved "does a study
exist" by globbing `engine/*_study/`. That glob returns 24 directories. The studies live
under `files/` — 313 delivered documents, models and bibliographies — and the queue had
never looked there.

**It is [R-ENF-04] and [L-355] together**: a probe that reads one naming convention finds
nothing under the other and reports that as a result. It produced a number rather than an
error, which is what let it stand.

**The repository already held the correct answer.** `engine/study_population.py` opens with
it in terms — *"The book carries 90 covered names and ALL NINETY HAVE A DELIVERED VALUATION
STUDY, under `files/`"* — and the campaign queue never imported it. Two measurements of one
fact, disagreeing, with nothing comparing them: the exact defect `engine/study_aliases.py`
was created to close for the alias table, arriving one level up for the population itself.
Fixed the same way: the queue now imports that module, and the tier is renamed from
`first-build` to `reissue-no-record`, which is what it always was.

**Why the correction changes the plan rather than a word in it.** A first build is the whole
depth bar from nothing. A reissue-no-record is a study that exists — read, sourced, modelled
— whose RECORD this repository cannot read. Those are different jobs with different costs,
and revision a's ordering, scale and wave structure were all derived from the wrong one.

---

## 1 · WHAT "ALL 90" ACTUALLY CONSISTS OF

Read live — `python3 engine/campaign_queue.py` and `python3 engine/study_population.py` —
never from this paragraph.

| | names | what it is |
|---|---|---|
| **REISSUE** | **22** | a study exists AND commits a record the gates can read; rebuilt on the current standard |
| **REISSUE — NO RECORD** | **67** | a study exists and was delivered; it commits no `engine/{ticker}_study` record, so the record is reconstructed from the delivered documents before anything is rebuilt |
| current | 1 | PHDC, on standard 2026.09.07 |

**ALL NINETY ARE REISSUES. NONE IS A FIRST BUILD.**

**What the 67 already carry, measured rather than assumed** (17-09-2026, across their latest
delivered workbook):

- a **16-sheet workbook** on the model report's sheet list, with the class-specific fifth
  sheet substituted as the lens rule requires — Emaar carries `RNAV & SOTP`, QNB carries
  `DDM`;
- a **live formula model**, median 453 formulas at 37.8% of populated cells, against 802 and
  39.7% for the 23 record-backed names. **The difference is depth, not kind**;
- a delivered document and its PDF, in every one of the 67.

**What they do not carry, and this is the size of the job:**

- **no record directory at all** — so no committed numbers file, no bridge record, no lens
  record, no cost-of-capital schedule, no macro-path block, no forecast anchor, no
  ground-up register, no sweep register, no rebuild ledger. Every gate in this repository
  reads one of those, so **all 67 are UNREADABLE rather than clean** [R-ENF-04], which is
  the state `coverage_outstanding.json` already records;
- **63 of the 67 ship no standalone bibliography** — depth-bar standard 1. Four do
  (2POINTZERO, LULU, RMDA, SALIK);
- a beta that predates the exchange-index rule in most cases, and a cost of capital that
  predates the v2 method in all of them.

**The honest scale, from the one observation there is.** GBCO's reissue — freeze, rebuild,
internal QC, external news, external audit, 34 findings implemented, documents and workbook
rebuilt, every gate green — took approximately one working session, and GBCO is
record-backed. A reissue-no-record costs more than that and less than a first build: the
research substrate exists, the record does not. **This is a programme measured in months,
and saying so is part of the design rather than a concession.**

---

## 2 · THE ORDERING DECISION, AND WHY IT IS THE WHOLE PLAN

**EGX IS FINISHED BEFORE ANY OTHER MARKET STARTS** [per instruction, 17-09-2026: *"Delay
other markets till we finish EGX first"*]. **This SUPERSEDES the record-backed-first
ordering below**, which reordered the queue across markets; the queue's own fixed market
order now runs, and all thirty-seven EGX names — both tiers — complete before UAE begins.
Inside EGX the record-backed names still go first, for the reason the rest of this section
gives.

**"Finished" means step 6, not step 7, and that is not a softening.** While the method hold
stands NO name can reach step 7 — the publish gate refuses every study in the book until
Phase 1 closes — so a constraint keyed on step 7 would never release, which is the gate
with no release `[R-CAL-01]` forbids, arriving as an ordering rule instead of a gate. A
name standing at step 6 has had every step of the runbook done to it and waits on a
book-wide event.

**The cost is stated rather than discovered.** Every other market now waits the length of
the EGX campaign — thirty-seven names rather than the nine the previous ordering would
have taken before UAE started — and their pages carry their pre-rebuild fair values
throughout. That is the debt `[R-GAP-03]` measures, and it does not shorten meanwhile.

**What it buys.** Phase 1's panel becomes EGX-dense rather than thin across three markets,
which is what its gating clauses actually need: leave-one-name-out has more to leave out,
and one market means one macro path, so nothing in the panel is comparing companies valued
in economies the study beside them does not recognise. The campaign's own hard stop after
EGX still applies at the boundary.

**Encoded, not noted.** `recalibration_run.py --next` sorts the first market ahead of every
other and refuses to name a non-EGX name while EGX is short, with the count and the names
outstanding. A `--next` that named a UAE name and printed a caution beside it would be
handing out the work it is meant to withhold.

---

### The superseded ordering, kept because its argument still governs INSIDE a market

**ALL 22 RECORD-BACKED REISSUES FIRST. NO RECORD RECONSTRUCTION UNTIL THEY ARE DONE.**

Revision a reached this same order for a reason that turned out to be false — that the other
67 were first builds and would inherit defects the reissues had not yet surfaced. **The
conclusion survives the correction and the argument is replaced, which is worth stating
rather than quietly keeping the answer.**

**THE REPLACED ARGUMENT: A DEFECT IN A NO-RECORD STUDY IS INVISIBLE.** Every instrument here
reads a committed record. The 67 commit none, so no gate can see a bridge on a stale sheet,
a cash charged twice, a terminal on an invented life or a minority deducted at book in any
of them — not because the gates are weak but because there is nothing for them to open. **A
class defect is cheapest to find where it can be found at all**, and that is the 22.

**And every defect found in a reissue becomes an instrument the other 89 inherit for free.**
GBCO's external audit, on 17-09-2026, produced at least four findings that are not about
GBCO:

- a cash-flow walk anchored on one balance-sheet date while the bridge stood on another;
- three capital structures inside one discount rate;
- a minority deducted at book out of a value that capitalises all of its cash flow;
- an earnings multiple struck on one earnings basis and applied to another.

Those are constructions, not numbers. **A study rebuilt before they were found carries all
four**, and sixty-seven record reconstructions done now would be sixty-seven studies
rebuilt against instruments that do not exist yet.

**The campaign queue's own market order is not overridden — it is read INSIDE each wave.**
EGX, then UAE, KSA, Qatar, India, Korea, USA, and the hard stop after EGX stands.

**AND THE SAME ORDERING IS WHAT MAKES PHASE 1 MEASURABLE.** Its gating clauses are pooled
bias, leave-one-name-out stability, and stability across eras. Leave-one-out needs at least
two names; the acceptance series currently has **one**, and prints *"nothing left to pool."*
Twenty-two rebuilt studies across four markets is a panel those clauses can actually be
computed on. The two problems have one solution.

---

## 3 · THE FIVE WAVES

```
  W1  the 9 EGX record-backed   ─►  W2  the 13 UAE + KSA record-backed
                                              │
  W5  the 67 reconstructions ◄─  W4  publish ◄┘  W3  Phase 1, measured ONCE
```

**THE WAVE STRUCTURE BELOW IS RESTATED UNDER THE EGX-FIRST ORDERING.** W1 and W2 were two
markets' record-backed names; they are now W1 (EGX record-backed, 9) followed by W1b (EGX
record reconstructions, 27), with every other market after Phase 1. W3, W4 and W5 keep
their meaning. **AND "WAVE" WAS DOING TWO JOBS IN THIS PLAN** — W1..W5 label programme
PHASES here, two of which ("Phase 1", "publish") are not batches of names at all, while
the board and the release unit use "wave" for a BATCH OF NAMES RELEASED TOGETHER. The
release batch is the one to decide about; where this section says W-something it means a
phase.

**W1 — the nine EGX record-backed reissues.** AMOC · ARCC · EGCH · ELEC · GBCO ✔ · PHAR ·
SCEM · SWDY · TMGH. Serial, full runbook, one name at a time. The campaign's own **hard stop
after EGX** stands: before any name of W2 starts, state whether the method generalised.

**W2 — the thirteen remaining record-backed reissues.** Ten UAE, three Saudi. Serial, full
runbook, but see §4 — by here the gates should be carrying what the audits found, not the
auditors.

**W3 — Phase 1, measured once.** On the twenty-two rebuilt studies, on a method that has
stopped moving. Not before: every rebuild changes the method, and a measurement taken
mid-campaign grades something already replaced. That is not an argument for postponing it;
it is the reason it has never closed.

**W4 — publish.** `check_publish_block.py` per name, `Publish_Protocol.md`, and an explicit
ask. The gap test and the dissent requirement are untouched by any of this.

**W5 — the sixty-seven record reconstructions**, in the queue's market order. With a proven
method and the full gate set, so each is rebuilt once rather than rebuilt and rebuilt.

**W5 IS WHERE THE READER-FACING RISK ACTUALLY SITS, AND IT IS ALREADY MEASURED.** These
sixty-seven are not dormant: their fair values are on the live site today, struck against
prices from June and July. [R-GAP-03] measures that exposure — the gap a reader sees against
the gap the house holds — and `python3 scripts/check_published_gap.py` reads it live. W5
being last is a decision about where the gap is closed correctly, not a claim that it is
small.

---

## 4 · THE EXTERNAL AUDIT IS A METHOD INSTRUMENT, NOT A PER-NAME QC STEP

Ninety external audits cannot be commissioned and do not need to be. **GBCO's audit found
34 findings and almost all of the consequential ones were class defects** — true of every
study of that shape, not of GBCO.

**THE RULE THAT MAKES THE PROGRAMME FINITE: a name does not close until every CLASS-LEVEL
finding from it is an instrument that runs over the book.** Not a fix in that study; a gate,
a shared module, or an assertion in a shared builder. Otherwise the same defect is found 90
times and fixed 90 times, and the 90th audit costs exactly what the first did.

**This was not done today and it is the largest single thing this session got wrong.**
Twelve separate duplicated quantities were fixed inside GBCO — its working capital lived in
the model and again in the workbook, its minority in the bridge and in two grids and in the
diagnostics and in the recalculation — and no instrument was built that finds a quantity
computed in two places from different inputs. Over 90 names that is the difference between
1,000 fixes and one check.

**How many audits, and when to stop.** Audit until an audit produces no NEW class of
finding. It is a measurable stopping rule, not a budget: count the class-level findings each
audit yields. While that count is positive the audits are buying method; when it reaches
zero they are buying per-name QC, which the gates already do more cheaply. **On present
evidence, expect two or three in W1 and none in W2.**

---

## 5 · WHEN SERIAL CAN RELAX, AND HOW THAT IS DECIDED

The runbook's ONE NAME AT A TIME is right for a stated reason: *a defect found on the first
usually changes how the second is built.* That reason is strongest when defects are frequent
and weakest when they have stopped.

**So it is not a permanent constraint — it is a constraint with a live condition.** Count
the NEW classes of defect a name produces. While a market's names are still producing them,
serial. Once three consecutive names of the same kind produce none, that kind may be batched
within its market.

**It never relaxes across a market boundary** and it never relaxes for a record-backed
reissue. The first three reconstructions of any market are serial whatever came before,
because a market's disclosure regime is itself a source of new defect classes — which is
precisely what the EGX checkpoint exists to test.

---

## 6 · BATCHING THE TWO HAND-OFFS

The runbook stops twice per name and both stops are the principal's: step 3 (external news)
and step 5 (external audit). Ninety names would be 180 round trips, and that — rather than
the modelling — is what would make the programme fail.

- **Step 3 batches by market.** Build every prompt for a market's wave at once, hand over as
  one pack, take the returns as one pack. Nothing in the step requires them separately; what
  it requires is that each return is traced to a primary source before it moves a driver,
  and that is per name whenever the pack arrives.
- **Step 5 does not batch — it SAMPLES**, per §4.

Both are hand-offs, so a wave's throughput is set by how fast the packs come back. That is
worth knowing before the wave starts rather than discovering it in the middle.

---

## 7 · WHAT STAYS EXACTLY AS IT IS

Nothing in this plan changes a research method, a gate, a threshold or a rule. In
particular: the per-name runbook is unchanged; the campaign prompt's standing refusals are
unchanged; the queue is read live from code and is never written into a document; the
publish block, the gap test and the dissent requirement are untouched; and **publishing
remains a separate, explicitly-requested step**.

**The one thing this plan changes is the ORDER the queue is worked in** — record-backed
names before record reconstructions, against the queue's own market order. That is a
decision for the principal rather than a change to make quietly, and it is recorded here as
a decision rather than applied silently in code.

---

## 8 · HOW IT ACTUALLY RUNS — `engine/recalibration_run.py`

Sections 1 to 7 decide the order and the shape. **None of them answers the question this
programme asks every morning: WHICH NAME DO I TOUCH NEXT, AND WHAT IS IT WAITING FOR.**
At one name a person remembers. At ninety, across seven steps, two of which stop dead and
hand the work to the principal, nobody does — and the failure is not that somebody
forgets, it is that a name sits in a hand-off nobody is tracking while the desk works on
something else.

```
python3 engine/recalibration_run.py                the board — every name, its step, whose move
python3 engine/recalibration_run.py --next         the next name the DESK can act on
python3 engine/recalibration_run.py --brief TK     where TK is, plus the runbook's OWN words
python3 engine/recalibration_run.py --waiting      everything held by the principal, by market
python3 engine/recalibration_run.py --ticker TK    one name, all seven steps, with evidence
python3 engine/recalibration_run.py --selfcheck    every artefact name this reader looks for
```

**STATE IS DERIVED, NEVER STORED, AND THAT IS THE ONE DESIGN DECISION THAT MATTERS.**
There is no step pointer per name and no "mark step 2 done" command. Each step is a PROBE
over the artefacts that step itself produces — the frozen baseline in `fv_movement.json`,
the walk-forward run directory and its harvested lessons, a `QC_GATE_{date}.md` **at the
current edition**, the news hand-over and its returns, the rebuild ledger, the audit
hand-over and its answer, and `check_publish_block.verdict()` read live. A name's position
is wherever the probes stop. Delete an artefact and the name moves back; that is wanted.

A hand-maintained board would go stale the first afternoon somebody was in a hurry, and it
would go stale SILENTLY, which is the shape that survives. This repository has paid for
that record repeatedly — the stale digest, the stale library list, and this same week a
lever applied to a model and never written into the record a gate outside it reads.

**THE WAVE IS ENCODED OR IT IS IGNORED.** The campaign queue runs market-major; §2 decides
something the queue does not — all 22 record-backed re-issues before any record
reconstruction. Left unencoded, `--next` would hand out an EGX reconstruction the moment
the ninth EGX re-issue closed, and this plan would be quietly contradicted by the tool
meant to implement it. The wave is computed from the tier and the queue's market order
runs inside it. The EGX checkpoint is ANNOUNCED when reached and never enforced silently:
a tool that refused to name the next name would look like a bug, and one that crossed the
boundary without saying so would hide the decision.

**IT READS THE RUNBOOK, IT DOES NOT COPY IT.** `--brief` lifts the step's own prompt out of
`Recalibration_Runbook_17-09-2026.md` at the moment it is relied on. A prompt copied into a
second file stops moving when the first is amended, which is [R-DOC-01] in miniature.

**WHAT IT DELIBERATELY DOES NOT DO.** It runs no step, decides nothing and writes nothing.
The steps are judgement work governed by the runbook and the standing rules. What it
supplies is the thing neither of those can — an honest answer to where ninety names are.

**AS AT 17-09-2026, ON ITS FIRST RUN:** 89 names are the desk's move and one is held on the
method; 79 of the 89 have not had their fair value frozen, which is step 0 and cannot be
done afterwards. Read it live — never from this paragraph.

---

## 9 · THE GENERAL LESSON, WHICH IS NOT ABOUT THIS PROGRAMME

**A PLAN INHERITS THE POPULATION ITS FIRST PROBE HAPPENED TO RETURN.** Every number in
revision a — the sixty-seven, the ordering, the wave structure, the months — descended from
one glob that answered a question nobody had asked it. The plan was internally consistent,
argued from measured evidence, and wrong at the root, and the only thing that caught it was
the principal saying, for the tenth time, that every ticker has a study.

**Before a programme is designed over a population, ask what would have to be true for the
count to be wrong** — and where a second measurement of the same fact already exists in the
repository, join them before either is relied on.
