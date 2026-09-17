# RECALIBRATION RUNBOOK — the whole process, one step after another

**RUNBOOK REVISION 2026-09-17c.** Every copy of this file carries this line as its
first characters after the title. If the copy you are holding does not, or carries an
earlier revision, IT IS STALE: the current text is
`engine/Recalibration_Runbook_17-09-2026.md` on the repository's own branch and nothing
else is authoritative. Bump the revision on every edit, however small — an unbumped
stamp is worse than none, because it certifies a copy that has moved. This stamp exists
because revision `a` was sent out, edited twice the same day, and the copy outside the
repository had no way to know: the same failure [R-DOC-01] was adopted on.

**Invoke with: "start a recalibration on {TICKER}".** The session then works steps 0
through 6 IN ORDER, stopping at each step's stop condition and reporting before it
moves on. ONE NAME AT A TIME. Never two in parallel — a defect found on the first
usually changes how the second is built, and running them together forfeits that.

**THIS FILE IS A SPINE, NOT A LIBRARY.** Where the repository already holds the
canonical prompt for a step, this names the path and does not restate it. A rule
restated in two places is the drift [R-DOC-01] closes, and this repository has paid
for it three times. Where a step has NO canonical prompt, the prompt is written
here in full and marked **NEW**.

**Nothing here is a standing rule.** It is an operating order over rules adopted
elsewhere, and it may not amend, soften or reinterpret any of them.

---

## THE SHAPE

```
0 FREEZE & ASK ─► 1 RECALIBRATE ─► 2 INTERNAL QC ─► 3 EXTERNAL NEWS
                                                          │
        6 PUBLISH GATE ◄─ 5 EXTERNAL AUDIT ◄─ 4 REISSUE? ◄┘
               │
        ┌──────┴──────┐
      LIVE          HELD
```

**Expect HELD.** As at 17-09-2026 nine of the book's studies are held at step 6 on
the METHOD — Phase 1 acceptance is not proven — and that includes both GBCO and
PHDC. Steps 0 to 5 run and finish; step 6 refuses. That is the gate working, not a
fault, and the work is not wasted: it is what publishes the day Phase 1 closes.
READ IT LIVE (`python3 scripts/check_publish_block.py`), never from this paragraph.

---

## WHERE A NAME IS — THE BOARD · **ADDED REVISION c**

This file is the order of work for ONE name. At ninety names, across seven steps, two of
which stop dead and hand the work to you, **the question nobody could answer was which
name to touch next and what it was waiting for.** A person remembers one name. Nobody
remembers ninety, and the failure is not forgetting — it is a name sitting in a hand-off
nobody is tracking while the desk works on something else.

```
python3 engine/recalibration_run.py             the board — every name, its step, whose move
python3 engine/recalibration_run.py --next      the next name the DESK can act on
python3 engine/recalibration_run.py --brief TK  where TK is, plus THIS FILE'S own words
                                                for the step it is at
python3 engine/recalibration_run.py --waiting   everything held by you, batched by market
python3 engine/recalibration_run.py --ticker TK one name, all seven steps, with evidence
```

**NOTHING IS MARKED DONE AND NO STEP POINTER IS STORED.** Each step is a PROBE over the
artefacts that step itself produces — the frozen baseline, the walk-forward run and its
harvested lessons, a QC gate AT THE CURRENT EDITION, the news hand-over and its returns,
the rebuild ledger, the audit hand-over and its answer, and the publish gate read live. A
name sits wherever the probes stop; delete an artefact and the name moves back. A board
somebody has to update by hand goes stale the first busy afternoon, and it goes stale
SILENTLY, which is the shape that survives — the stale digest, the stale library list and
the technical read that had to be told its library moved were all this, and so was the
defect in section 4's new clause below.

`--brief` lifts the step's prompt out of THIS FILE at the moment it is relied on rather
than copying it, so amending a step here amends what the desk is told [R-DOC-01].

---

## THE POPULATION — WHAT "NO STUDY" MEANS, AND WHAT IT DOES NOT · **ADDED REVISION c**

**EVERY ONE OF THE NINETY COVERED NAMES HAS A DELIVERED VALUATION STUDY.** They sit under
`files/` — 313 delivered documents, models and bibliographies. Twenty-three of them ALSO
commit an `engine/{ticker}_study/` record; sixty-seven do not.

**Those are two different facts and only one of them had ever been measured.** The campaign
queue resolved "does a study exist" by globbing `engine/*_study/`, which returns 24
directories, and reported the absence of a DIRECTORY as the absence of a STUDY — so this
programme was planned on 17-09-2026 as "22 re-issues and 67 studies built from nothing",
which was wrong about seventy-four per cent of the book. It is [R-ENF-04] and [L-355]
together: a probe that reads one naming convention finds nothing under the other and
REPORTS THAT AS A RESULT. It produced a number rather than an error, which is what let it
stand, and the repository already held the correct answer in
`engine/study_population.py` — nothing had ever joined the two.

**So the tiers mean:** `reissue` — a study with a record the gates can read.
`reissue-no-record` — a study that was delivered, whose RECORD has to be reconstructed
from the delivered documents before any gate can open it. **NONE of the ninety is a first
build**, and no step of this runbook may be skipped on the belief that one is.

---

## STEP 0 — FREEZE, THEN ASK · **NEW**

**Goal.** Capture what is about to be destroyed, and obtain the one input only the
principal can supply, BEFORE any driver is set.

> **PROMPT.** We are starting a recalibration of {TICKER}. Before anything is built:
>
> 1. `python3 engine/fv_movement.py snapshot {TICKER}` — freeze the current fair
>    value. THIS CANNOT BE DONE LATER AND THERE IS NO RECOVERY FROM SKIPPING IT: the
>    rebuild is the one sanctioned thing that moves `fair{bear,base,full}`, and
>    `data.js` carries no date or standard stamp, so a baseline taken afterwards is a
>    fabricated zero. If the snapshot refuses because one already exists, say so and
>    carry on — it is append-only by design.
> 2. Ask me for {TICKER}'s LATEST SHARE PRICE AND ITS DATE, and commit the answer to
>    `engine/prices/SUPPLIED_{DD-MM-YYYY}.json` [R-GAP-01 AMENDED]. Ask once, in one
>    line, then ROUTE AROUND IT — the price enters at the strike and at the gap review
>    and nowhere else, so do not stop work waiting. If no answer arrives, default to
>    the latest committed price, state its date and disclose its age.
> 3. `python3 engine/lessons.py {TICKER} --class {CLASS}` — read what already binds on
>    this name and this class. Lessons marked PROVISIONAL are findings from an
>    unvalidated method: read them, never cite them as authority.
> 4. Report the frozen baseline, the price you were given or defaulted to, and the
>    count of binding lessons by scope. Then stop.

**Stop condition.** A frozen baseline exists (or is declared unrecoverable WITH ITS
REASON), the price question has been asked, and the binding lessons have been read.

**What would make this step a lie.** Taking the snapshot after the rebuild has begun.
Looking the price up in the repository instead of asking for it — that is a different
quantity and looks identical from the inside.

---

## STEP 1 — RECALIBRATE THE FUNDAMENTALS · **canonical prompt exists**

**Goal.** Rebuild the forecasting method on the company's own history and re-derive
the value.

> **PROMPT.** Read `engine/Fundamental_Walkforward_Prompt.md` IN FULL and run it on
> {TICKER}. It is the canonical prompt for this step [R-FCAL-01] and it is not
> summarised here. Inside the book-wide campaign, also read
> `engine/Fundamental_Walkforward_Campaign_Prompt.md` for the wrapper — it changes no
> research method.
>
> Four things that prompt requires and that get skipped most often. Say explicitly
> that you did each:
> - **The valuation-input block at EVERY origin** — cash, interest-bearing debt, PP&E,
>   D&A, the working-capital lines, the share count footed against its par value.
>   A driver panel is not a record a value can be rebuilt from. This is the largest
>   single class of dropped cells in the acceptance series.
> - **The terminal on a DISCLOSED asset life**, through `engine/terminal_value.py`.
>   A life this desk chose is not a disclosed life, and finding a RANGE is not
>   finding a life [R-TERM-01].
> - **ONE CLASS PRIMARY IS THE CENTRAL** [R-LENS-03]. The other lenses are
>   cross-checks published in the same table; the bear/full envelope is the RANGE of
>   the present-value reads. **NEVER a weighted blend and never a set of typed
>   weights** — that construction is RETIRED, and it is what put one study 28% below
>   its own cash-flow lens.
> - **Margins are OUTPUTS.** A contribution or gross margin set as an input is a QC
>   fail wherever the filings disclose enough to build cost per unit instead.

**Stop condition.** The two documents [R-FCAL-01] requires both exist — the updated
fundamental analysis at full model-report depth AND the updated lessons register. A
run that produces one and not the other is not finished.

---

## STEP 2 — INTERNAL QC · **canonical instrument exists, framing NEW**

**Goal.** Establish, from outside the study, that it is deliverable.

> **PROMPT.** Run the internal QC on {TICKER} from OUTSIDE the study it audits.
>
> 1. Use the `testahil-qc-auditor` subagent — it fills every row of the QC gate with
>    the artefact, command or number that carries it, and it never edits what it
>    audits [R-ENF-02]. NEVER self-certify: a boolean a study sets on itself is not a
>    check, and this repository has closed that hole nine separate times.
> 2. Use the `testahil-gate-runner` subagent to run every gate exactly as CI runs it,
>    plus import-not-parse and the JS load-assert. It reports; it never fixes.
> 3. **If the central sits more than 10% from the latest known price EITHER WAY**, the
>    eight-heading `GAP_REVIEW_{DD-MM-YYYY}.md` is written BEFORE anything is staged
>    [R-GAP-01]. Eight headings, each individually capable of producing the whole gap:
>    latest filings · base year · macro coherence · discount rate · terminal · balance
>    sheet · claims against the record · multiple cross-check. State the GAP the review
>    audited, not only the central.
> 4. Report the filled table and every red gate. Fix what the gate NAMES
>    deterministically; for anything else produce a ranked work order. Do not edit a
>    gate, a negative control or a ratchet to make something pass [R-REPAIR-01].

**Stop condition.** The QC table is filled with evidence per row, every gate is green
or its redness is explained, and any gap over 10% has its review.

---

## STEP 3 — EXTERNAL NEWS RESEARCH · **NEW** · **HANDS OFF TO THE PRINCIPAL**

**Goal.** Find what the filings do not carry — and keep it out of the model until it
has been traced.

**THIS STEP STOPS.** The session builds the prompt and hands it over; the principal
runs it on Perplexity and Claude and feeds the answers back. The session does not
continue until it has them.

> **PROMPT — WHAT THE SESSION DOES.** Build the hand-over prompt for {TICKER} from
> what this repository already holds, and hand it to the principal. It must carry:
> - The company's registered name in English AND in the language its own regulator
>   and trade press write it in — a search in one language only misses the half of
>   the record that matters most on these exchanges.
> - The driver headings its industry actually turns on, taken from the study's own
>   driver list, not from a generic template.
> - **The study's OWN dated negative searches**, read live out of its sweep register,
>   so the external pass is told what has already been looked for and not found
>   rather than rediscovering the same absences.
> - The period the study's information set already covers, so anything earlier is
>   known to be already consumed.
>
> Then STOP and hand it over. Do not search the web from inside this session in place
> of the hand-off — the whole point is a second, independent pass.

> **PROMPT — WHAT COMES BACK.** When the principal returns the answers:
> 1. **WHAT COMES BACK IS A LEAD AND NEVER AN INPUT.** Every claim is traced to the
>    PRIMARY source and read there before it moves anything. Historicals come from the
>    company's own issued statements alone — no vendor, broker, or press-as-a-numbers
>    source, ever (SIGCM clause 1; two delivered studies have already breached it).
> 2. Keep the two returns APART. Where they agree on something neither can source,
>    that is agreement between two models and not evidence.
> 3. **Every untraceable claim is written back into the sweep register as a DATED
>    NEGATIVE SEARCH**, never dropped. A negative search is a search somebody actually
>    ran; inventing one to clear a coverage check is worse than the gap it clears.
> 4. Register every new source in `research_sweep.py`'s register, four fields each,
>    COMPANY_IR tagged distinctly. A period is not swept until BOTH its statements AND
>    its results release are registered.
> 5. Report: what was found, what traced to a primary source, what did not and became
>    a negative search, and which findings could move a driver.

**Stop condition.** The prompt has been handed over AND the returns have come back and
been traced. Nothing untraced has entered the model.

## STEP 4 — DOES IT MOVE A DRIVER? · **replaces your FUNDAMENTAL REFRESH prompt**

**Goal.** Decide whether the new information changes the answer, and rebuild only what
it touches.

> **PROMPT.** For {TICKER}, decide whether step 3's findings move a driver.
>
> **If NOTHING traced to a primary source moves a driver:** say so explicitly, record
> which rings you re-ran and which you carried forward, and go to step 5. An unchanged
> answer with a stated reason is a legitimate outcome and the commonest one.
>
> **If something does move a driver**, rebuild ONLY what it touches and re-run step 2:
>
> 1. **SCORE THE PRIOR STUDY FIRST.** Reconcile every newly disclosed actual against
>    what the published study forecast for that period — revenue, volume, price, gross
>    margin, capex, net debt — line by line in a variance table. A miss beyond 5% of
>    the central escalates: say WHICH PART OF THE DRIVER STACK was wrong, never just
>    that the number differed.
> 2. **REBUILD THE MOVED DRIVERS GROUND UP.** SIGCM in full. Revenue as volume x price,
>    cost as cost-per-unit, growth in BOTH. ONE ESCALATOR PER PHYSICAL COST-DRIVER
>    CLASS — never one blended index across materials, fuel, transport and wages, which
>    manufactures a margin decline out of arithmetic and then reports it as a finding.
>    Every inflation-class input maps to the house ladder [R-MACRO-01]; a study may not
>    carry an inflation number of its own.
> 3. **A NEAR-TERM REVIEWED ACTUAL OUTRANKS A STALE FULL-YEAR RATE.** Anchor on the
>    most recent reviewed period; let a rate drift only where a NAMED mechanism from the
>    closed list has a MEASURED like-for-like direction in the company's own period pair
>    [R-ANCHOR-01]. "The rate looked wrong" is not a mechanism.
> 4. **RE-CHECK THE COST OF CAPITAL, DO NOT INHERIT IT.** Through
>    `engine/cost_of_capital.py`: rf* normalised by that sovereign's OWN default spread,
>    country risk counted exactly once, marginal Kd above the local sovereign,
>    market-value weights, both ERP bases published. Beta ONLY through
>    `beta_regression.own_stock_beta()` against the published index of the exchange the
>    stock is LISTED on — read the exchange off the `assets/data.js` code prefix, never
>    from the `raw_ohlc/` folder. A constituent composite is a HARD FAIL.
> 5. **THE PRIMARY LENS IS THE CENTRAL. THERE IS NO BLEND.** [R-LENS-03] — the other
>    lenses are cross-checks in the same table and the envelope is the range of the
>    present-value reads.
> 6. **CARRY THE PRICE SIDE FORWARD, LABELLED.** Sections 2 and 3 reproduce the last
>    published technical read and probabilistic map UNCHANGED, with their
>    `asof.{mc,tech}` stamps quoted verbatim. If `asof.mc.data` is materially stale, say
>    so plainly rather than reconciling it silently. Fresh OHLC is a SEPARATE
>    roll-forward pass, reported separately.
> 7. **DELIVER THE FULL SET — the depth bar is not divisible.** 16-section Word,
>    16-sheet Excel, standalone bibliography, all eight depth standards, expert appendix
>    re-run against the new numbers. Then update `TICKERS.{TICKER}.fair{bear,base,full}`
>    and re-fit the slider's factor-stack constants, which a roll-forward may never do.
>    LEAVE `spot`, `spotDate`, `dist`, `touch`, `levels`, `tech` and `asof` ALONE and
>    say so explicitly.
> 8. Record the route in the REBUILD LEDGER [R-REBUILD-01] — the levers in the order
>    applied, each with the answer before and after and the rule it serves. Several
>    levers serving one rule are ONE piece of evidence, not several.
> 9. **THE RECORD AND THE PROSE MOVE WITH THE LEVER, IN THE SAME PASS.** · **ADDED
>    REVISION c.** For every lever applied, name the committed record it changes and the
>    sentences that describe it, and move both — `forecast_anchor`, `bridge_record`, the
>    lens record, the cost-of-capital schedule, the inflation inputs, and every sentence
>    in the document and the bibliography that states the old construction. Then
>    **RE-RENDER THE PDF**: the Word file is not the artefact a reader receives.

**A LEVER APPLIED TO THE MODEL AND NOT WRITTEN INTO THE RECORD IS INVISIBLE WHERE IT
COUNTS, AND THIS IS NOT HYPOTHETICAL.** On 17-09-2026 a re-issue correctly moved a study
onto its reviewed half-year — the bridge, the margin anchor and the cash-conversion rate,
three levers, all right. The record kept naming the superseded quarter, so a gate reported
that study as having read half a filing, which it had not; and the delivered document went
on telling a reader that three published years of 4.3, 17.9 and 3.9 per cent average to
7.7, because the carried rate was read out of a field still called `mean` after it had
stopped being one. **A NAME THAT OUTLIVES THE CONSTRUCTION IT DESCRIBES IS A FALSE
STATEMENT WITH A PLAUSIBLE NUMBER ATTACHED**, and nothing in the arithmetic was wrong:
every figure was computed and individually correct. Ask of each lever what now describes
something that is no longer true.

**Stop condition.** Either a stated no-change with its reason, or a rebuild whose
ledger walks from the prior answer to the published one, **with every record and every
sentence the levers touched moved in the same pass and the PDFs re-rendered.**

---

## STEP 5 — EXTERNAL AUDIT · **HANDS OFF TO THE PRINCIPAL**

**Goal.** Have the study examined by someone who did not build it.

**THIS STEP STOPS TWICE.** The session delivers the valuation document and the
financial model to the principal, who takes them OUTSIDE for an independent audit.
The session does not continue until the audit outcome comes back; it then evaluates
every finding, updates the documents, and only then goes to step 6.

> **PROMPT — HANDING OVER.** Deliver {TICKER}'s valuation document and workbook to the
> principal for external audit, with the QC gate beside them. Say plainly what the
> study's central is, what it was struck against, which contested judgements it resolved
> and which way, and what would overturn each. An auditor who has to reconstruct the
> claim before testing it is being asked to do our job.

> **PROMPT — WHEN THE AUDIT COMES BACK.** Read `engine/Critique_Response_Prompt.md` IN
> FULL and follow it. Its discipline is not optional and is the reason this step exists:
> SELF-AUDIT FIRST before judging any finding; ONE ROW PER FINDING with no grouping;
> PRICE each one before judging it; split premise from conclusion; REJECT ONLY WITH
> RECEIPTS; escalate anything worth more than 5% of the central; and STOP TO REPORT
> BEFORE IMPLEMENTING ANYTHING. Implementation happens on a second, explicit approval.
>
> A finding that is right costs the study nothing to accept and costs the reader a great
> deal to ignore. A finding that is wrong is refused with the arithmetic that refutes it,
> never with a restatement of what the study already said.

**Stop condition.** Every finding is priced, ruled on with receipts, and either
implemented or refused in writing. The documents reflect what survived.

> **The in-house alternative, where no outside audit is run:** use the
> `testahil-qc-auditor` subagent. It fills the QC gate from outside the study, never
> edits what it audits, and reads the rendered PDF page by page with every figure
> inspected as an image — two gates that have caught defects no programmatic check
> could see. It is NOT a substitute for the external pass when one is available. Fill the QC gate with
> the artefact, command or number that carries each row — never the study's own printed
> table and never `gate_result.json`. Re-run the builders in an isolated copy and diff
> cell by cell against the delivered file. READ THE RENDERED PDF PAGE BY PAGE and
> INSPECT EVERY FIGURE AS AN IMAGE: those two are gates, not formalities, and they have
> caught defects no programmatic check could see. Write only
> `QC_GATE_{DD-MM-YYYY}.md`; never edit the study you audit.
>
> Where an outside critique arrives instead, read `engine/Critique_Response_Prompt.md`
> and follow it — self-audit first, one row per finding, priced before judged, receipts
> on every rejection, and STOP to report before implementing anything.

**Stop condition.** A dated QC gate exists, written from outside, with a verdict.

---

## STEP 6 — THE PUBLISH GATE · **canonical protocol exists**

**Goal.** Find out whether this may reach a reader. It often may not.

> **PROMPT.** `python3 scripts/check_publish_block.py` and read the row for {TICKER}.
> Three tests, all must pass:
> - **THE GAP** — held only where the central is more than 10% BELOW the latest known
>   price, and released by a complete `MARKET_DISSENT_{DD-MM-YYYY}.md` carrying its
>   five headings. Above the price is the ordinary shape of finding something cheap and
>   is not held.
> - **THE METHOD HOLD** [R-GAP-02 CLAUSE THREE] — Phase 1 acceptance must be proven.
> - **READABILITY** — an unreadable study is held too, or unreadability becomes the
>   cheapest route past the block.
>
> If it clears, read `engine/Publish_Protocol.md` in full and run
> `python3 scripts/publish_site.py --ticker {TICKER} --ship`. **Publishing is a
> separate, explicitly-requested step** — never assume it from "finish the
> recalibration".
>
> If it is HELD, say which test held it and what would release it. Do not move the fair
> value toward the price to clear a gate: that is the reverse-engineered rate this house
> prohibits outright, arriving through the front door.

**Stop condition.** Live, or a stated hold naming the test that refused and its release
condition.

---

## WHERE YOUR TWO PROMPTS WENT

You had two. Both are now placed, and both were amended rather than adopted as
they stood.

**Your RECALIBRATION prompt is the repository's own
`engine/Fundamental_Walkforward_Prompt.md`** — not a separate document. Step 1 calls
it. Two defects were found in it on 17-09-2026 and fixed in the same commit as this
file, both of them [R-DOC-01] drift, a rule amended in one place and not the other:

- **§1.5 read "synthesis" with no mention of [R-LENS-03].** The prompt predates that
  rule (30-Aug against 02-Sep) and the digest's own model-report section was updated
  while this one was not. A session following it literally could rebuild the
  four-lens weighted blend — the construction that put PHDC's published central 28%
  below its own cash-flow lens. It now names the class primary as the central and
  says the blend is retired.
- **It named PHDC as "the depth standard"**, while the reference set is CLOSED at
  ADNOCLS, ADCB and ALPHADHABI and no other company is a template. PHDC is now
  described as what it is — a worked example of a study built to that standard.

**Your FUNDAMENTAL REFRESH prompt is step 4**, rewritten above. What it was missing,
each of which the protocol requires and none of which it mentioned: freezing the fair
value before anything moves it; asking for the price at the start rather than looking
it up at the end; the disclosed-life terminal [R-TERM-01]; the valuation-input block
at every origin; the house inflation ladder [R-MACRO-01]; the named-mechanism test on
a declining forecast [R-ANCHOR-01]; the rebuild ledger [R-REBUILD-01]; and the gap
review and publish block that decide whether any of it reaches a reader. Its step 5
also said "re-run all four lenses ... then the synthesis", which is the same retired
construction as the defect above.

**What it got right and is kept verbatim in substance**: scoring the prior study
against the new actuals before rebuilding it, with a 5% escalation threshold; the
one-escalator-per-physical-cost-driver rule; carrying the price side forward with its
stamps quoted; re-fitting the slider constants, which a roll-forward may never do; and
naming explicitly what was left untouched.

---

## WHAT THIS RUNBOOK MAY NEVER DO

- Move a fair value toward a price to clear a gate.
- Edit a gate, a negative control or a ratchet to make something pass [R-REPAIR-01].
- Invent an input. A missing figure is recorded as missing and escalated (SIGCM 8).
- Publish without an explicit ask.
- Run two names at once.
- Treat a lead from a language model as an input to a valuation.
- Leave a record, a field name or a sentence describing a model the study no longer has.
- Report an absence it never searched for. A probe that comes back empty has not found
  nothing; the first hypothesis is that the probe did not run [R-ENF-04].
