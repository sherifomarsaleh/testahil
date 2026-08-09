# TESTAHIL — comparative adjudication prompt (v1, 09-Aug-2026)

Used when a set of delivered TESTAHIL studies is set against a third party's studies on the same
names, and the question is "are ours too conservative?". Placeholders in `{braces}` filled per use.
Single critique of a single study → `Critique_Response_Prompt.md`.

Precedent: `engine/arcc_study/efg_bridge.py` already does the per-company half of this against EFG
Hermes on ARCC. It changed a standing rule (COST-STACK ESCALATION) by pricing the gap line by line.

## What "too conservative" decomposes into

Every unit of gap is one of four things. Only the last is conservatism.

| Class | Settled by | Conservatism? |
|---|---|---|
| **Defect** — arithmetic error, double-count, internal inconsistency | Recomputation | No — just wrong |
| **Fact** — different values for something disclosed and dated | The primary document | No — a sourcing failure |
| **Convention** — valuation date, ex-dividend, discounting basis, share count | Align both, price the difference | No — looks like it, carries none |
| **Judgement** — same facts, different view: terminal growth, reinvestment charge, ERP, capex, margin path | Realised outcomes and repeated sign only | **Yes** |

On ARCC most of the gap was defect and convention. A verdict of "too conservative" only means
anything after the first three are stripped out.

## The prompt

> Attached are two sets of valuation studies covering the same {N} companies, from two research
> houses — Set A and Set B — plus the audited filings and the results and prices realised since.
> Adjudicate which set is closer to reality, under this procedure.
>
> **0. Declare your priors.** Say which set you expect to favour, and list every feature that
> identifies the authorship — length, section count, expert appendix, bibliography, boilerplate,
> whether a rating is printed. Commit to not using any of them as evidence. Length and apparatus are
> evidence about effort, not accuracy. If you can tell who wrote what, say so rather than claiming a
> blindness you don't have.
>
> **1. Bridge each company, one driver per step.** Don't compare headline numbers. Start at Set A's
> value per share, substitute one driver at a time with Set B's, re-solve, record each change, until
> the state *is* Set B's model. Invariants: bars sum to (B − A); one driver per step and no driver in
> two steps; the terminal value carried undiscounted so the rate and date steps both re-price it;
> every printed number independently recomputed. A step that changes the discount rate and the
> discount date together is two steps in one label — split it.
>
> **2. Classify each step defect / fact / convention / judgement, before judging it.**
> Defect and fact steps get a verdict from {A off, B off, OPEN, NEITHER}, each with a receipt — a
> recomputation, or a primary document quoted in its own words with its date. No step unjudged; no
> step judged in a set's favour without a receipt. Not verdicts: "standard practice", "conventional",
> "a matter of judgement", "immaterial" without a number. Convention steps must be *shown* to be
> convention-only by pricing both ways; if the two don't then agree, reclassify. Judgement steps get
> no verdict here — carry them to steps 4 and 5. Report the split as percentages of the gap.
>
> **3. Any step worth >5% of the smaller central** gets an independent re-derivation from primary
> sources and its own paragraph.
>
> **4. The sign test.** One row per recurring judgement driver across all {N} companies; record which
> set is lower and by how much. Report k-of-N and the exact binomial p per driver class, with N
> printed prominently — at small N almost nothing is significant. A large gap in one name is noise; a
> small gap with the same sign in every name is a house view. Separate a stated uniform policy from
> an unexamined habit — both produce identical signs here.
>
> **5. The referee — realised outcomes. This outranks everything above.** For every forecast line
> that has since printed (revenue, volume, price, margins, capex, EPS, net debt), tabulate both sets
> against the filing. Report mean signed error (bias) and mean absolute error (accuracy) separately —
> a set can win one and lose the other. Then the price test, scoring a range on coverage and a point
> target on error, and saying which you did; the two are not commensurable. **A range containing the
> outcome is calibrated, not conservative; a central below every realised print is conservative.** If
> the printed history is too short to discriminate, say so and say how many more quarters are needed.
>
> **6. Report:** the defect/fact/convention/judgement split with defects counted on *each* side; which
> set is systematically lower, on which drivers, at what k-of-N and p; whether that lowness is
> contradicted by realised outcomes; and where each set is *more* conservative than the other. An
> answer with defects on only one side, or with no counter-examples, hasn't looked hard enough.
>
> **7. State your falsifier** — the figure, its source, and the threshold that would reverse you.
>
> **8. Then, and only then,** you'll be told which set is which. Which findings would you have
> reached differently had you known? "None" is an acceptable answer if true.

## Where to run it

Build the bridges and the realised-outcome tables **inside** the project — the numbers are here, and
retyping them elsewhere breaks numeric traceability. Adjudicate **outside**: fresh session, no repo,
and **no protocol file attached**. `PROJECT_INSTRUCTIONS` is the rulebook that generated one of the
two sets, and several of its rules *are* the disputed judgements (terminal reinvestment charge, rf
normalised by the sovereign's own default spread, marginal Kd above the sovereign). An adjudicator
holding it applies those rules rather than evaluating them, and scores every departure as an error by
definition. `efg_bridge.py` likewise states who is off mark on ARCC in prose at the top of the file.

## Bias

Real, and not all in one direction.

**Toward the house set:** authorship self-consistency; same-family priors (an Anthropic model
agreeing with an Anthropic-authored DCF is correlation, not corroboration); rulebook capture, if run
in-repo; and the largest — **length and apparatus**, which survives anonymisation, since a 16-section
study with an expert appendix beside a 4-page sell-side note is structurally unmistakable and LLM
adjudicators reliably prefer the longer, more-cited document.

**Away from it:** instructed-independence over-correction (a manufactured concession fails as badly
as a defended error); deference to a named institution.

**Mitigations, most effective first:** realised outcomes — no adjudicator bias touches a printed
quarter; priced single-driver steps with receipts instead of a global verdict; running outside the
project; a second adjudicator from a different model family on the identical package, worth doing for
anything that would move a standing rule; blind labels randomised per company, which helps but cannot
touch the length confound; step 8, which measures the residual rather than assuming it away.

An LLM's read on which set *seems* more realistic is weak evidence and shouldn't move a standing rule
alone. A computed bridge plus a realised scorecard is strong evidence and can.

## Assembling the set

Pick the pairs on a rule stated **before** any gap is looked at — every name where both houses
published within {window}. Otherwise whoever picks the pairs decides the answer. Pairs where TESTAHIL
is *higher* are the most informative rows in the table. N = 1 says nothing about house bias; N = 3
says very little. Print N next to the verdict.
