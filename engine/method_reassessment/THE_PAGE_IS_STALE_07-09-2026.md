# The hold is showing readers worse numbers than the house's own answer

Found 07-09-2026 by building [R-GAP-03] — a gate whose subject is the fair value **a
reader sees on the site**, rather than the one a study commits.

## What was measured

`assets/data.js` carries `fair{bear,base,full}` and a spot for all 90 published names, and
a reader divides one by the other. All 90 gaps are computable. **58 of them exceed ten per
cent either way. Two are currently audited.**

Thirty-six of the rest have no study directory, so nothing could audit them — that
population is already tracked by `check_published_coverage`. **The other kind is the
serious one**, and it is not a review going stale. It is a page going stale:

| name | SITE publishes | STUDY's own central | site / study | gap a READER sees | gap the STUDY has |
|---|---|---|---|---|---|
| SCEM | 53.12 | 123.27 | 0.43x | **−46.1%** | **+25.1%** |
| TMGH | 147.12 | 91.83 | 1.60x | **+50.4%** | **−6.1%** |
| AMOC | 5.95 | 11.40 | 0.52x | −56.1% | −15.8% |
| SWDY | 69.73 | 55.48 | 1.26x | −48.8% | −59.3% |
| ARCC | 54.65 | 66.53 | 0.82x | −28.7% | −13.1% |
| PHDC | 15.89 | 17.85 | 0.89x | +4.5% | +17.4% |

**On SCEM and TMGH the sign is opposite.** A reader looking at SCEM sees a company the
house appears to think is worth less than half its price. The house's own current answer is
that it is worth a quarter more than its price. The same is true of TMGH in the other
direction.

## Why it happened, and it is nobody's carelessness

[R-GAP-02] holds a study from publishing while its fair value disagrees with the market by
more than ten per cent. That rule is correct and it was adopted to protect a reader from a
number the house had not audited.

The rebuilds of the last week corrected several of these studies — AMOC, ARCC, SCEM, PHDC,
TMGH — and every corrected number is sitting in the repository behind the hold. So the
hold, whose purpose is to keep an unaudited number away from a reader, **is currently
keeping the AUDITED number away from the reader and leaving the unaudited one on the page.**

The protocol anticipated half of this in its own words — "while the book is held a page
carries the fair value it carried BEFORE its rebuild ... so the gap a READER sees and the
gap the gate reports are two different numbers, each honest about a different thing" — and
said the divergence "closes when the campaign publishes the book together". That is a plan
rather than a check: it cannot go red, it cannot shorten, and nothing would have noticed if
it grew. What it did not anticipate is that on two names the two numbers point OPPOSITE
WAYS.

## What this does NOT license

**Nothing here is a reason to publish.** [R-GAP-02] holds, publishing to the live site
remains a separate and explicitly-requested step, and no fair value moves toward any price
because of this finding. What is established is the COST of the hold, measured rather than
asserted, so the decision to keep it or release it is made on evidence.

## What was built

`scripts/check_published_gap.py` [R-GAP-03] — population is the site through a real
JavaScript load, an unreadable answer fails rather than being skipped, the trigger and the
staleness tolerance are both BORROWED from [R-GAP-01] rather than minted, and it imports
[R-GAP-01]'s own review readers rather than modelling them [R-ENF-03]. Ratcheted at 56 with
every entry carrying its measured gap, and the ratchet's own text splits the two kinds of
debt because they are not the same debt.

## The general lesson, which is not about publishing

**A GATE PROTECTS THE THING IT TAKES AS ITS SUBJECT, AND EVERY GATE HERE TOOK THE STUDY.**
Twenty-two studies are audited to the basis point by instruments that read what a study
commits. The artefact a reader actually receives — one number on one page — was checked for
its technical read, its band record, its stamps and its chart, and never for whether the
valuation on it was the valuation the house currently holds. Where a rule exists to protect
somebody, check the thing that reaches them.
