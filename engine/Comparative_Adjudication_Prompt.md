# TESTAHIL — comparative adjudication prompt (v1, 09-Aug-2026)

The instruction used when a set of delivered TESTAHIL studies is set against a set of third-party
sell-side studies on the same names, and the question is **which set is closer to reality** — most
often raised as "are the TESTAHIL studies too conservative?"

Placeholders in `{braces}` are filled per use. Related: `Critique_Response_Prompt.md` (single
critique, single study), `Standing_Research_Protocol.md` (standing rules).

---

## Why this is a different document from `Critique_Response_Prompt.md`

The critique prompt answers *"is this specific finding right?"* one finding at a time. It assumes the
critic is the challenger and the study is the defendant. That asymmetry is correct for a critique and
**wrong here** — here both sets are on trial, and the interesting quantity is not any single gap but
whether the gaps share a **sign**.

Two failure modes this document exists to prevent:

1. **The vibe verdict.** Asked "which is more realistic", a reader compares two documents and picks
   the one that reads better. Nothing about a document's readability is evidence about the future.
2. **"Conservative" used as a single word for four different things.** See the decomposition below;
   only one of the four is conservatism, and the other three are settled by arithmetic or by a
   primary document, not by judgement.

**Precedent this is built on.** `engine/arcc_study/efg_bridge.py` already does the per-company half of
this against EFG Hermes on ARCC, under invariants I1–I9, and it changed a standing rule: the
COST-STACK ESCALATION rule was adopted because the reconciliation showed TESTAHIL's whole forecast
margin decline was a mechanical artifact of one blended cost index — a real conservatism defect, found
by pricing the gap line by line, and already contradicted by a realised 42.9% Q1-2026 gross margin.
That is the standard. The bridge is computed and gated, not eyeballed.

---

## What "too conservative" actually decomposes into

Every EGP of gap between two valuations of the same company falls into exactly one of four classes.
Sort before judging — the prompt below forces this.

| Class | What it is | How it is settled | Is it conservatism? |
|---|---|---|---|
| **A. Defect** | An arithmetic error, an internal inconsistency, a double-count, a discount factor that contradicts its own stated rate | Recomputation. Has a right answer. | **No.** It is just wrong, on whichever side it sits. |
| **B. Fact** | The two sides use different values for something that is disclosed and dated | The primary document. Has a right answer. | **No.** It is a sourcing failure. |
| **C. Convention** | Valuation date, ex-dividend treatment, mid-year vs year-end discounting, share count, gross vs net | Declare both, show the gap is convention-only, and price it | **No.** It looks like conservatism and carries none. |
| **D. Judgement** | Same facts, same arithmetic, different view — terminal growth, reinvestment charge, ERP, capex intensity, volume path, margin glide | Cannot be settled by argument. Only realised outcomes and repeated sign discriminate. | **Yes. This is the only place conservatism lives.** |

A verdict of "TESTAHIL is too conservative" is only meaningful if it survives after A, B and C are
stripped out. Most of the ARCC gap was A and C.

---

## The scope table — fill this before running anything

| Company | TESTAHIL study + date | Counterpart study + date | Gap (central, %) | Quarters printed since both dates |
|---|---|---|---|---|
| {TICKER} | {file, date} | {file, date} | {x%} | {list} |

Rules for the set:

- **Pair only on comparable dates.** Two studies four months apart on an EGX name are not comparable
  without a date-convention step; put that step in the bridge (class C), never in the verdict.
- **State N and its power.** N = 1 says nothing whatsoever about house bias. N = 3 says very little.
  The sign test in step 4 below needs the honest count printed next to it.
- **Do not drop a pair because it is inconvenient.** A pair where TESTAHIL is *higher* is the most
  informative row in the table for the question being asked. If the set was selected by anyone for
  any reason, say so — a set chosen because the gaps looked large is not a sample.

---

## The prompt

> Attached are two sets of valuation studies covering the same {N} companies. Set A and Set B were
> produced by two different research houses. For each company you have both studies, and you have the
> underlying primary documents: the audited financial statements, the investor-relations materials,
> and the realised share prices and reported results from the study dates to today.
>
> Adjudicate which set is closer to reality. Work under the following procedure. It is a procedure,
> not a suggestion.
>
> ### 0. Before anything else — declare your priors and your tells
>
> State, in advance and in writing:
>
> - which set you expect to favour and why, before you have read either in detail;
> - every feature you can already see that identifies the authorship of a set — document length,
>   section count, presence of an expert appendix or a bibliography, house boilerplate, formatting,
>   whether a rating or price target is printed. **List them, then commit to not using any of them as
>   evidence.** Length, citation count, appendix depth and internal rigour of presentation are
>   evidence about *effort*, not about *accuracy*, and a longer document being closer to the truth is
>   a claim you must demonstrate, never assume.
>
> If you believe you can identify the authorship of a set, say so plainly rather than pretending to a
> blindness you do not have. A stated bias can be discounted; an unstated one cannot.
>
> ### 1. Build a per-company bridge. One driver per step
>
> For each company, do not compare the two headline numbers. Start at Set A's equity value per share
> and substitute **one driver at a time** with Set B's, re-solving each time, until the state *is*
> Set B's model. Record the value change of each substitution. The steps sum to the gap by
> construction, not by a plug.
>
> Enforce, and report, these invariants on each bridge:
>
> - the bars sum to (B − A);
> - every step declares exactly **one** driver, and no driver appears in two steps;
> - the terminal value is carried **undiscounted** through the state, so the rate step and the date
>   step both re-price it;
> - every printed number is reproduced by an independent recomputation.
>
> A step that changes the discount *rate* and the discount *date* together is two steps wearing one
> label. Split it.
>
> ### 2. Classify every step A / B / C / D before judging it
>
> Assign each step to exactly one class: **defect**, **fact**, **convention**, **judgement** (per the
> definitions supplied with this prompt). Then:
>
> - **Defect and fact steps get a verdict from a closed set — {A is off, B is off, OPEN, NEITHER} —
>   and every verdict carries a receipt**: a recomputation, or a quoted primary document with its own
>   words and its date. A step may not be left unjudged, and no step may be judged in favour of a set
>   without a receipt. "Standard practice", "conventional", "a matter of judgement", "immaterial" with
>   no number, and "the other side misunderstands the model" are not verdicts, and using one is itself
>   a finding against you.
> - **Convention steps must be shown to be convention-only** — price the same company on both
>   conventions and show the two agree once the convention is aligned. If they do not agree, it was
>   never a convention step; reclassify it.
> - **Judgement steps get no verdict here.** Carry them, with their price and their direction, into
>   step 4 and step 5. Resist the pull to referee them — that pull is the whole bias this procedure
>   is guarding against.
>
> Report the split: **"{X}% of the total gap is defect, {Y}% fact, {Z}% convention, {W}% judgement."**
> The conservatism question is a question about W only.
>
> ### 3. Escalate by magnitude
>
> Any single step worth more than 5% of the smaller of the two centrals gets an independent
> re-derivation from the primary sources, whatever your first read of it was, and its own paragraph.
>
> ### 4. The sign test — this is the actual question
>
> Tabulate, across all {N} companies, one row per recurring **judgement** driver class: terminal
> growth, terminal reinvestment charge, discount rate, capex intensity, revenue/volume path, margin
> path, working capital, net-cash bridge, lens weighting. In each cell record the **sign**: which set
> is lower, and by how much.
>
> Then:
>
> - Under the null "neither house has a systematic view", the signs within a driver class are coin
>   flips. Report, per class, the count and the exact binomial two-sided p-value. Print the arithmetic
>   (k of N, p = …) — and print N, prominently, because at small N almost nothing is significant and
>   claiming otherwise is the easiest error available here.
> - A gap that is large in one company and absent in the others is **noise**. A gap that is small but
>   the **same sign in every company** is a house view, and it is the thing being asked about.
> - Distinguish the driver classes where a house has a *policy* (e.g. always charging a reinvestment
>   burden against terminal growth, always normalising the risk-free rate for the sovereign's own
>   default spread) from those where it has drifted. A stated, defensible, uniformly applied policy is
>   not the same finding as an unexamined habit, and both produce identical signs in this table.
>
> ### 5. The referee — realised outcomes
>
> Everything above is argument. This step is evidence, and it outranks every other step in the
> procedure.
>
> For every forecast line in either study that has **since printed** — quarterly and full-year
> revenue, volume, realised price, gross and EBITDA margin, capex, EPS, dividend, net debt — tabulate
> the forecast from each set beside the realised figure from the filing, with the filing's date.
> Compute per set: mean signed error (**the bias**) and mean absolute error (**the accuracy**). These
> are different questions and a set can win one and lose the other.
>
> Then, separately, the price test: the realised share price at each study's own check dates against
> each set's published range or point. Note explicitly where a set publishes a *point target* and the
> other publishes a *range or distribution* — these are not commensurable, and scoring a range as
> though it were a point (or vice versa) is a category error. Score a range on **coverage** (did the
> outcome land inside, and where in the range) and a point on **error**. Say which you did.
>
> **A range that contains the outcome is calibrated, not conservative.** A central that sits below
> every realised print is conservative. Keep those two findings apart.
>
> Where the printed history is too short to discriminate — say so, and say how many more quarters
> would be needed. "Insufficient realised data" is a legitimate and useful answer to step 5. A
> confident verdict built only on steps 1–4 is a verdict about reasoning, not about reality; label it
> as such.
>
> ### 6. Answer the question asked, in this exact form
>
> 1. The share of the gap that is defect / fact / convention / judgement, with the count of defects
>    found on **each** side. A comparison that finds defects on only one side has almost certainly not
>    looked hard enough at the other; go back and look before you report that.
> 2. Whether Set A or Set B is systematically lower, on which driver classes, at what k-of-N and p.
> 3. Whether that systematic lowness is **contradicted by realised outcomes** — which is the only
>    sense in which "too conservative" is a defect rather than a house style.
> 4. Where each set is *more* conservative than the other. Neither set will be uniformly one way; if
>    your answer has no counter-examples in it, that is a symptom, not a result.
>
> ### 7. State your falsifier
>
> Before you finish: what specific, observable evidence would reverse your verdict? Name the figure,
> the source it would come from, and the threshold. A verdict with no falsifier is an opinion.
>
> ### 8. The authorship check — last, and only last
>
> Only after everything above is written, you will be told which set is which. Then answer: **which of
> your findings would you have reached differently had you known?** Answer honestly, including "none"
> if that is true. This is the measurement of the bias, and it is a deliverable of the exercise, not
> an afterthought to it.

---

## Notes for whoever runs this

- **Run it outside the project.** See the next section — this is load-bearing.
- **Steps 1 and 5 are compute, not reading.** The bridge and the realised-outcome table should be
  built by script from the two sets' own published numbers, and gated, exactly as
  `arcc_study/efg_bridge.py` is. An adjudicator eyeballing two PDFs will produce a vibe verdict no
  matter how good the prompt is. Hand it computed tables and ask it to judge them.
- **Step 5 outranks steps 1–4** and the prompt says so twice on purpose. If the realised data is thin
  today, the right answer is to run the bridge now, record the forecast-vs-realised table as a
  standing scorecard, and re-adjudicate as quarters print. That is the same discipline as the ledger:
  the forecast is committed in advance and graded on arrival.
- **The set is the deliverable's weakest link.** Whoever assembles the pairs decides the answer if
  they are not careful. Assemble the set on a rule stated before any gap is looked at — every name
  where both houses have published within {window} — never by picking interesting pairs.
- **Expect defects on both sides.** On ARCC the reconciliation put EFG off mark on five steps
  (a date inconsistency, capex below their own D&A, an unfunded terminal growth, a dividend already
  gone ex, a stale net-cash figure) and left two OPEN with TESTAHIL plausibly wrong on one of them —
  the margin glide, which the very next realised quarter contradicted. Both of those are the exercise
  working.

---

## Where to run it

**Two sessions, split by task. The build happens inside the project; the adjudication happens
outside it.**

| Phase | Where | Why |
|---|---|---|
| Assemble the pairs; build each bridge; build the forecast-vs-realised table | **Inside** the project | The numbers live here — `study_numbers.json`, `compute.py`, the audited filings under `{ticker}_study/filings`. A bridge built anywhere else is retyped numbers, and the numeric-traceability rule forbids that. |
| Adjudicate | **Outside** — a fresh session, no repository access, no `CLAUDE.md`, no protocol files | Everything below. |

The adjudicator gets: both sets of studies, the computed bridges, the forecast-vs-realised tables,
the primary filings, and this prompt. It gets **no** protocol document.

That last exclusion is the important one. `PROJECT_INSTRUCTIONS` and `Standing_Research_Protocol.md`
are not neutral background — they are the rulebook that *generated* one of the two sets, and several
of the standing rules are precisely the judgement calls under dispute: the terminal reinvestment
charge, the sovereign-default-spread normalisation of the risk-free rate, marginal Kd above the
sovereign, market-value weights, no-price-targets. An adjudicator holding that rulebook does not
evaluate those choices, it *applies* them — and then scores the counterpart's every departure as an
error by definition. That is not a comparison, it is a compliance check with the answer written into
the reference material.

Loading the repo also drags in every prior conclusion about the counterpart house — `efg_bridge.py`'s
receipts already state who is off mark on ARCC, in prose, with the answer at the top of the file. A
fresh adjudicator that reads it is not adjudicating.

---

## Does it matter that one set is our own?

**Yes, materially — and the biases do not all point the same way, which is why "just tell it to be
objective" does not work.**

Pushing toward the house set:

1. **Authorship and self-consistency.** A model asked to evaluate reasoning of a kind it produces
   will find that reasoning persuasive, because it is reconstructing rather than testing it.
2. **Length and apparatus.** A 16-section study with an expert appendix, a standalone bibliography
   and a sourced input register beside a 4-page sell-side note is a confound that **survives
   anonymisation** — the documents are structurally unmistakable. LLM adjudicators reliably prefer
   longer, more-cited, more-elaborately-reasoned documents, and none of those properties is evidence
   about accuracy. This is the single largest bias in the exercise and step 0 of the prompt names it
   explicitly for that reason.
3. **Rulebook capture** — only if run inside the project. See above.
4. **Same-family priors.** An Anthropic model adjudicating an Anthropic-authored study is not an
   independent draw: it shares priors on how a DCF should be built, so agreement is partly
   correlation, not corroboration.

Pushing the other way:

5. **Instructed-independence over-correction.** Told to be critical of its own side, a model
   manufactures criticism of it — and a fabricated concession is as much a failure as a defended
   error. This is the counterpart to the "a response that accepts everything is as uncalibrated as
   one that accepts nothing" rule in `Critique_Response_Prompt.md`.
6. **Authority deference.** A named sell-side institution reads as authoritative in a way an
   in-house study does not.

**What actually reduces it, in descending order of effectiveness:**

- **Realised outcomes** (step 5). No LLM bias touches a printed quarterly figure. This is why step 5
  outranks the rest of the procedure, and why a thin realised record should be reported as thin
  rather than papered over with a confident argument-based verdict.
- **Forcing the verdict down to priced, single-driver steps with receipts** (steps 1–3). A global
  "which is more realistic" invites the confound; "who is off mark on this step, and quote the
  document" mostly does not.
- **Running it outside the project** — removes bias 3 outright.
- **A second adjudicator from a different model family** (GPT / Gemini) on the identical package.
  Where the two agree, biases 1 and 4 are not driving it; where they disagree, that disagreement is
  the finding. This is worth doing on any conclusion that would change a standing rule.
- **Blind labels with the mapping randomised per company**, so the house set is not always Set A.
  Worth doing, but treat it as reducing the effect, not eliminating it — see bias 2, which it cannot
  touch.
- **Step 8**, which measures the residual rather than assuming it away.

**The honest summary:** an LLM verdict on which set *reads* more realistic is weak evidence and
should never on its own move a standing rule. A computed bridge and a forecast-vs-realised scorecard
are strong evidence and can. The prompt above is built to convert the first kind of question into the
second.
