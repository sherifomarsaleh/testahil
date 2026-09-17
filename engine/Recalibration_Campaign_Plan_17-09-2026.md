# THE 90-NAME RECALIBRATION — how the programme runs

**PLAN REVISION 2026-09-17a.** Per instruction, 17 September 2026: *"I want all 90 stocks
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

## 1 · WHAT "ALL 90" ACTUALLY CONSISTS OF

Read live — `python3 engine/campaign_queue.py` — never from this paragraph. As at
17-09-2026 it divides into two jobs of very different size:

| | names | what it is |
|---|---|---|
| **REISSUE** | **22** | a study exists; it is rebuilt on the current standard |
| **FIRST BUILD** | **67** | **no study exists at all** — a published fair value with nothing behind it |
| current | 1 | PHDC, on standard 2026.09.07 |

**A first build is not a recalibration.** It is the full study the depth bar defines — the
16-section document, the 16-sheet live workbook, the standalone bibliography, the four
gates, the independent recalculation, the scrub, every figure inspected as an image — with
a walk-forward run beneath it. The campaign prompt states this and it is repeated here
only because the instruction says "recalibrate", and 67 of the 90 cannot be.

**The honest scale, from the one observation there is.** GBCO's reissue — freeze, rebuild,
internal QC, external news, external audit, 34 findings implemented, documents and workbook
rebuilt, every gate green — took approximately one working session. Twenty-one reissues
remain. A first build is more work than a reissue, not less. **This is a programme measured
in months, and saying so is part of the design rather than a concession.**

---

## 2 · THE ORDERING DECISION, AND WHY IT IS THE WHOLE PLAN

**ALL 22 REISSUES FIRST. NO FIRST BUILD UNTIL THEY ARE DONE.**

The campaign queue runs in fixed market order — EGX, then UAE, KSA, Qatar, India, Korea,
USA — and within EGX that puts nine reissues ahead of twenty-seven first builds. The market
order exists for a good reason, stated in the campaign prompt: a method is tested on a whole
market before it travels. **This plan changes the order and the reason is measured, not
preferred.**

**Every defect found in a reissue becomes an instrument that every later study inherits for
free.** GBCO's external audit, on 17-09-2026, produced at least four findings that are not
about GBCO at all:

- a cash-flow walk anchored on one balance-sheet date while the bridge stood on another;
- three capital structures inside one discount rate;
- a minority deducted at book out of a value that capitalises all of its cash flow;
- an earnings multiple struck on one earnings basis and applied to another.

Those are constructions, not numbers. **A study built before they were found carries all
four.** Twenty-seven EGX first builds done now would be twenty-seven studies inheriting
every defect the remaining reissues have not yet surfaced — and would then need rebuilding,
which is the work done twice.

**AND THE SAME ORDERING IS WHAT MAKES PHASE 1 MEASURABLE.** Its gating clauses are pooled
bias, leave-one-name-out stability, and stability across eras. Leave-one-out needs at least
two names; the acceptance series currently has **one**, and prints *"nothing left to pool."*
Twenty-two rebuilt studies across four markets is a panel those clauses can actually be
computed on. The two problems have one solution.

---

## 3 · THE FIVE WAVES

```
  W1  the 9 EGX reissues        ─►  W2  the 13 UAE + KSA reissues
                                              │
  W5  the 67 first builds  ◄─  W4  publish  ◄─┘  W3  Phase 1, measured ONCE
```

**W1 — the nine EGX reissues.** AMOC · ARCC · EGCH · ELEC · GBCO ✔ · PHAR · SCEM · SWDY ·
TMGH. Serial, full runbook, one name at a time. The campaign's own **hard stop after EGX**
stands: before any name of W2 starts, state whether the method generalised.

**W2 — the thirteen remaining reissues.** Ten UAE, three Saudi. Serial, full runbook, but
see §4 — by here the gates should be carrying what the audits found, not the auditors.

**W3 — Phase 1, measured once.** On the twenty-two rebuilt studies, on a method that has
stopped moving. Not before: every rebuild changes the method, and a measurement taken
mid-campaign grades something already replaced. That is not an argument for postponing it;
it is the reason it has never closed.

**W4 — publish.** `check_publish_block.py` per name, `Publish_Protocol.md`, and an explicit
ask. The gap test and the dissent requirement are untouched by any of this.

**W5 — the sixty-seven first builds.** With a proven method and the full gate set, so that
each one is built right the first time rather than built and rebuilt.

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

**It never relaxes across a market boundary** and it never relaxes for a reissue. The first
three first builds of any market are serial whatever came before, because a market's
disclosure regime is itself a source of new defect classes — which is precisely what the
EGX checkpoint exists to test.

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

**The one thing this plan changes is the ORDER the queue is worked in** — reissues before
first builds, against the queue's own market order. That is a decision for the principal
rather than a change to make quietly, and it is recorded here as a decision rather than
applied silently in code.
