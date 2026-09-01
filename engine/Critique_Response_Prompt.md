# TESTAHIL — external critique response prompt (v2, 06-Aug-2026)

The instruction used when another AI system, or a human reviewer, critiques a delivered study and
its model. Placeholders in `{braces}` are filled per use.

**Why v2 exists.** On the SWDY study a critique raised roughly 96 findings. The response grouped
them into themes and argued about ten individually; the rest were dismissed in aggregate. **The
single largest error in the study — a relative lens that never discounted a forward enterprise
value back to today, worth EGP 44 per share — was inside the dismissed batch.** It was only found
after the instruction "You are taking the criticism lightly and I do not like that. Straighten up."

The failure was structural, not attitudinal, and four features of the old prompt caused it:

| Old prompt feature | What it produced |
|---|---|
| "Give me a concise response point by point" | Concise won. Findings were grouped into themes, and a theme-level answer let individual findings vanish without anyone noticing. |
| No requirement to quantify before judging | Findings were rejected as immaterial without ever being priced. The 44/share error was never costed before it was waved away. |
| Rejection required no evidence, acceptance did | Rejecting was cheap and implementing was expensive, so the reasoning drifted toward rejection under cost pressure. |
| "Do not implement till you get to me" **and** "implement the plausible comments" | Directly contradictory, which left the decision about when to stop entirely to the responder. |

v2 fixes each with a forcing function rather than an exhortation. Standing rule:
`Standing_Research_Protocol.md`. Related: `Study_Initiation_Prompt.md`.

---

## The prompt

Attached is a critique of {the study / the model / both} for {TICKER} by {source}. Work through it
under the following procedure. It is a procedure, not a suggestion — the structure is there because
a previous response to a critique of this kind grouped the findings and lost a EGP-44-per-share
error inside a batch it dismissed.

### 1. Self-audit FIRST, before you read the critique in detail

Before assessing anyone else's findings, audit the study yourself and list what you find. Do this
first so your own list is not anchored on theirs. **A self-audit that finds nothing is a failed
self-audit — go back and look harder.** Say explicitly which of your findings the critique also
caught and which it missed; a defect only you found is the strongest evidence the audit was real.

### 2. Enumerate EVERY finding. No grouping, no batching, no themes

Build a numbered ledger with one row per finding, in the critique's own order, quoting its own
words for the claim. If the critique raises 96 findings, the ledger has 96 rows. Then state the
count reconciliation explicitly: **"N findings raised, N answered, 0 unaddressed."** If two findings
genuinely duplicate, say so and give the duplicate its own row pointing at the original — do not
silently merge them.

Grouping is the failure mode this whole procedure exists to prevent. Themes are for the summary you
write at the end, never for the assessment you do at the start.

### 3. Price every finding BEFORE you judge it

For each row, compute the effect on the valuation — in currency per share and as a percentage of the
weighted central — **before** deciding whether to accept it. If it cannot move the valuation, say
what else it damages (a wrong number in a table, an unsupported claim, a misleading chart).

You may not call a finding immaterial without a number next to the word. You cannot know something
is small until you have measured it.

### 4. Split the PREMISE from the CONCLUSION

A finding has a factual premise and an analytical conclusion, and they fail independently. Assess
both, separately:

- **premise right, conclusion right** → accept;
- **premise right, conclusion wrong** → the critic saw something real and drew the wrong inference.
  Fix the real thing;
- **premise wrong, conclusion right by accident** → fix the underlying issue, and say the stated
  reason was wrong;
- **premise wrong, conclusion wrong** → reject, and quote the primary source that shows the premise
  is false.

A critique that is confidently wrong about its reason may still be pointing at a real defect. **For
every finding you reject, ask what a careful reader would have had to misread to land there — and
whether that thing is unclear, unsourced or wrong.** Log any adjacent defect as a new finding of
your own.

### 5. A rejection needs receipts, at the same standard as an acceptance

State the verdict as a test that was run, not as reasoning that was performed. Acceptable evidence
for a rejection: a computation showing the effect is what you say it is; a quoted primary source
(the audited note, the filing, the published data file, with its own words); an internal coherence
test that the critique's version fails and yours passes.

**These are not verdicts, and using one is itself a defect:**

> "this is standard practice" · "the critic misunderstands the model" · "this is a matter of
> judgement" · "immaterial" with no number · "the method is conventional" · "already disclosed"
> without saying where · "the effect is small" with no number · "we considered this"

Where two critiques contradict each other, arbitrate with an internal coherence test on the
underlying data, never by which source sounds more authoritative. (On SWDY, one source's segment
figure forced an implied fabrication uplift of 1.077 — below every historical year — while the
other's gave 1.204, inside the historical range. The second was adopted **on the test**, not on
authority.)

### 6. Escalate by magnitude

Any finding priced at more than 5% of the weighted central gets a full independent re-derivation
from the primary sources, whatever your first read of it was, and its own paragraph in the response.
The cost of over-examining a small finding is a few minutes. The cost of under-examining a large one
is the study.

### 7. Then, and only then, sort into four buckets

1. **ACCEPT AND IMPLEMENT** — the finding is right and the fix is clear.
2. **ACCEPT THE DEFECT, REJECT THE FIX** — something is wrong, but the proposed remedy is not the
   right one. State what you will do instead.
3. **UNPROVEN — RESEARCH REQUIRED** — plausible but asserted without evidence. Go and check it
   against primary sources, then move it into bucket 1 or 4 with what you found. Do not leave it
   parked.
4. **REJECT** — with the receipts from step 5.

Where a finding is genuinely a judgement call with material value at stake, do not resolve it
yourself. Add a fifth bucket, **YOUR DECISION**, with the price of each branch and a recommendation.

### 8. Stop and report

Report at this point. Do not implement anything yet. The report is: the self-audit list, the full
ledger with prices and verdicts, the count reconciliation, and the bucket summary. Be concise
**within** each row and exhaustive **across** rows — those are not in tension, and if you find
yourself trading one for the other you are grouping again.

### 9. On my approval, implement — then prove it

Implement the approved findings, then re-run every gate on the delivered files and report:
the before/after value of each headline, the gate output, and **any finding whose implementation
surfaced a further defect.** Restructuring for a fix routinely exposes something else; that
discovery is part of the deliverable, not a distraction from it.

### 9b. Re-check the answer against the price  [R-GAP-01]

Implementing findings moves the number, so a study that did not breach before the response can breach after it. If the restruck central lands more than 10% BELOW the latest known market price, the response is not finished until `GAP_REVIEW_{DD-MM-YYYY}.md` covers all eight headings and `python3 scripts/check_valuation_gap.py` is clean. This applies to a self-audit exactly as it does to an outside critique — a self-audit that only re-checks the work it did will keep missing the work it never did.

### 10. Calibration, not capitulation

The goal is to be right, not to be agreeable. Accepting a wrong finding is as much a failure as
dismissing a right one, and a response that accepts everything is as uncalibrated as one that
accepts nothing. Reject what deserves rejecting — with receipts — and say so plainly.

**If I tell you that you are taking the critique lightly, the correct response is not to defend the
assessment. It is to redo it at individual-finding level under this procedure, and to check first
whether the findings you dismissed in a batch were ever priced.**

---

## Notes for whoever runs this

- **The old prompt's contradiction is fixed by phase separation.** Step 8 stops; step 9 implements
  on approval. Never ask for both in one instruction.
- **"Concise" is the trap.** It was in the old prompt and it is what caused the grouping. v2 keeps
  brevity where it is safe (per row) and forbids it where it is not (across rows).
- **The pricing rule is the load-bearing one.** If you keep only one change from v2, keep step 3.
  An unpriced finding is an unassessed finding, and the SWDY failure was exactly that.
- **Expect the self-audit to find things the critique missed.** On SWDY it found a balance-check row
  hardcoded to zero — a check that could never fail — and a false live-driver claim in the workbook.
  Neither was in any critique.
