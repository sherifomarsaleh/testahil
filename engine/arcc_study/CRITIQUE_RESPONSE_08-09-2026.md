# ARCC — response to the forensic audit of 8 September 2026

**Status: TEN OF FOURTEEN ADJUDICATED AND FIXED — 1, 2, 3, 5, 7, 8, 9, 10, 11, 12, 13 and
14. Every one of them turned out to be a DESCRIPTION rather than a calculation. No
valuation figure has moved and none will move without its own entry here. Findings 4 and 6
remain escalated: both are INPUTS, and correcting either moves the value.**

The audit is `EXTERNAL_AUDIT_08-09-2026.md` in this directory: 33 readers, 19 findings
surviving adversarial verification, 7 graded total fail. Six readers rebuilt the whole
model from the workbook's Assumptions sheet BEFORE reading the study's answer and all six
reproduce EGP 66.5300 a share and every printed intermediate. **The arithmetic is sound.**
Every finding is about construction, sourcing or description — which is worse rather than
better, because those are the things a recalculation cannot catch.

## How this response is written

One row per finding, no grouping. Each is PRICED before it is judged. A rejection carries
its receipt. Anything worth more than 5% of the central is escalated rather than settled
here. Nothing is implemented until it appears below with a verdict.

**The self-audit came first and it changed one verdict.** Before reading the auditor's
reasoning on findings 1 and 2, the model's own calibration block was read from the source.
That is what established that the auditor's *characterisation* of finding 1 is wrong and
its *substance* is right — a distinction that would have been invisible from the finding
alone.

---

## Finding 1 — the calibration factors

**The auditor says:** three level shifts ride on the declared index paths; one is
disclosed and two are silent; they move price and cost in opposite directions; removing
the two undisclosed ones takes EGP 66.53 to 48.90, **−26.5%**.

**PRICED FIRST.** The three factors are local price ×1.078760, export price ×0.871133 and
the whole cash-cost stack ×0.976364. The delivered document discloses the local factor and
calls it "the assumption in this study most capable of being wrong". It discloses neither
of the other two. The bibliography discloses none. **Confirmed by reading the document
rather than the finding.**

**VERDICT: the substance is ACCEPTED and the characterisation is REJECTED, with receipts.**

Accepted: a reader of the delivered study met one third of a calibration that sets the
level of every forecast year. That is a real disclosure failure and it is now fixed — the
document names all three factors, their common source and what the cost factor is for.

Rejected, and the receipt is the model's own log line: *"Cost calibrated on the SAME half,
so the margin stays an OUTPUT... Calibrating price WITHOUT cost would have manufactured a
margin out of the calibration."* These are not three covert adjustments pointing in
convenient directions. They are ONE calibration of the model to ONE reviewed half, and
they point in different directions because that is what the half reports: local sales of
goods rose, export sales of goods fell, and the half's own cost of sales grosses up below
what the uncalibrated model charged. Calibrating price and leaving cost alone is the
defect; doing both is the repair.

**The −26.5% is therefore not the price of fixing this.** It is the price of deleting two
thirds of a coherent calibration and keeping the third — which would leave the model
calibrated on one channel and not the others, a worse model rather than a corrected one. A
reader is owed the disclosure, not that number.

**MOVED: nothing. The document now carries what the model always did.**

## Finding 2 — the conservatism claim on the central driver

**The auditor says:** the study states an opening local-price step of 8.0% and calls it
"less than a point above a path in which prices stop rising altogether". The model applies
+16.50%. The study's own proof of conservatism is off by an order of magnitude, in the
direction that flatters value.

**PRICED FIRST.** Confirmed against the builder. The sentence quoted the growth index
alone (`price_local_path[1]`) while the model applies that index AND the calibration, so
the printed claim understated its own step by about half. The paragraph ended *"it can now
be checked rather than asserted"*, which makes it worse: it invited the check and failed
it.

**VERDICT: ACCEPTED IN FULL.** This is the sharpest finding in the audit. A study may
carry a step of 16.5%; what it may not do is describe that step as 8.0% and build a
conservatism claim on the smaller number.

**Fixed.** The paragraph now computes the step the model actually applies, prints it as
16.5%, states the distance from the flat-exit path honestly, says plainly that earlier
editions quoted the index and left the calibration out, and replaces the withdrawn claim
with the narrower one that survives: the price path grows below cost inflation in every
forecast year, and the first-year level is set by a filed half rather than by a view.

**MOVED: nothing.** The audit's EGP 14.10 a share is the price of deleting the
calibration, not of correcting the sentence.

## Finding 3 — the terminal replacement-cost total against its two printed operands

**The auditor says:** §1.8 prints "EGP 51,191mn, being 5.0Mt at USD 130 a tonne". Those
two operands and the exchange rate give 32,695. The printed total needs a further
undisclosed ×1.565711. A stated total is 56.6% larger than the operands it is stated to
be the product of.

**PRICED FIRST.** Confirmed against the builder. The 51,191 is right and it is FOUR
operands, not two: 5.0Mt × USD 130/t × the exchange rate × cumulative local cost
inflation to FY2030, because a terminal capital charge is levied in terminal-year
pounds against terminal-year cash flows. The workbook says "in terminal-year pounds".
The study did not.

**VERDICT: ACCEPTED AS A DISCLOSURE FAILURE, REJECTED AS AN ARITHMETIC ONE.** The
auditor's +14.5% is the price of taking the sentence literally and charging a FY2030
capital base in FY2025 pounds — which would deflate the charge against an inflated cash
flow and overstate value. That is the defect, not the repair.

**Fixed.** The sentence now states all four operands.

**MOVED: nothing.**

## Finding 5 — the factor the terminal is actually brought home on

**The auditor says:** Table 7's caption says the terminal is brought home on "year
five's own cumulative factor", printed as 0.4521. The model uses 0.41558. Three lenses
found it independently. The auditor's own conclusion: *"The end-of-window factor is the
better convention; the printed description is what fails."*

**PRICED FIRST, AND IT IS WORSE THAN THE FINDING.** Confirmed, and the contradiction
runs deeper than the caption. The study's own COMMITTED cost-of-capital record carried
`terminal_discount_factor` = 0.452058 with a note reading *"The terminal is brought home
on the LAST EXPLICIT factor, not on an end-of-window one"* — while the valuation applied
0.415551. So the machine-readable record contradicted the machine. The gate that tests
"one date, one price of time" was being run against a factor the valuation never used,
and passed.

**VERDICT: ACCEPTED IN FULL, AND THE CONSTRUCTION IS KEPT.** A terminal value is the
value at the END of the explicit window of everything after it, so under a mid-period
schedule it arrives half a year later than the last explicit cash flow and is worth
LESS. The model has always done that and it is right to. What was wrong was every
description of it — the caption, the record's note, and the record's own number.

**Fixed in three places, all of them descriptions.** The record now commits the factor
the model uses and declares `terminal_arrival_years`; the caption states the
end-of-window factor, its arrival, and why it sits below year five's; the workbook's
label is computed from the record.

**A FOURTH DEFECT INSIDE THIS ONE, WHICH THE AUDIT QUOTED WITHOUT NOTICING.** The
auditor cites the workbook cell as labelled *"t = 4.417y"*. The formula in that cell
spans (1 − stub) + 4 = **4.50** years. 4.417 is a stub of seven twelfths — a valuation
date this study moved off when its bridge went to the 30 June interims. It was a hand-
typed number sitting beside the formula that contradicts it, and no gate reads a
spreadsheet label. It is now computed.

**MOVED: nothing.** The audit's +4.6% is the price of FOLLOWING the wrong description —
of discounting a terminal that arrives at 4.50 years as though it arrived at 4.00. The
value does not move because the model was never wrong.

**THE GATE WAS RE-POINTED, NOT WIDENED [R-COC-01].** `check_cost_of_capital`'s test 4
demanded the terminal factor EQUAL the last explicit year's. The harm it names is a
PREMIUM — the same pound arriving on the same day priced twice — and equality also
caught the opposite and correct case. The test now refuses a premium outright, as
before, and where the terminal is discounted MORE it requires the record to declare when
the terminal arrives, that the arrival sit after the last explicit cash flow and inside
the window the forward rates cover, and that the factor reproduce from the same ladder
at that time. That is stricter than equality was, not looser: five new negative controls
hold it, and the harness reports 37 of 37 conditions behaving as claimed.

---

## What the four settled findings share, and it is the finding under the findings

Findings 1, 2, 3 and 5 are **one root cause with four faces**: in every one of them the
model is right and the page describing it is wrong. A calibration computed, logged and
applied, and disclosed in a third of its extent. A step of 16.5% applied and described as
8.0%. A capital base of four operands printed as the product of two. A terminal brought
home at 4.50 years and described as arriving at 4.00. Nothing was hidden from the model.
Everything was hidden from the page.

**Finding 5 goes one layer further than the other three, and that layer is the one worth
keeping.** There the wrong description had been committed to the study's own
MACHINE-READABLE record — the record said 0.452058 while the valuation used 0.415551 —
so the check that exists to test exactly this was reading a number the model never
touched, and passing. An artefact that describes the answer it was built against can
carry the right vintage marker and the wrong content [R-ENF-06]; here it carried the
right shape and the wrong number, which is the same failure one level down.

Every gate in this repository passed all four, and they were right to: the recalculation
reconciles because the arithmetic is correct, the prose-figure check passed because 16.5%
is not printed anywhere to be checked against, and the numeric-traceability bar passed
because no figure was typed. **A number that is absent from a document cannot be checked
against the model, and a sentence that quotes one operand of two is not a wrong figure —
it is a true figure describing a different quantity.** The one number that WAS typed —
the workbook's "t = 4.417y" — sat in a spreadsheet label, which no gate reads at all.

---


## Findings 7 to 14, adjudicated together after 5

Each is its own row below. What they have in common is worth naming first, because it is
the same thing findings 1, 2, 3 and 5 had: **in every case the model does one thing and
some delivered artefact says another.** Not one of them is an arithmetic error. Every one
of them was invisible to a recalculation, which is why six independent rebuilds of this
model reproduced EGP 66.5300 and none of them found any of this.

### Finding 7 — the sector utilisation. ACCEPTED IN FULL, and it is the largest of these.

The study divided 72.6Mt of cement-AND-CLINKER sales by 76Mt of CEMENT nameplate capacity
and printed a market running near 96%. On matched denominators it is **85.6%** — about
10.9Mt of grinding capacity idle. A clinker tonne leaves at the kiln and never enters a
cement mill, so it consumes no grinding capacity at all.

**The receipt is this study's own note.** Its export-line input says that earlier editions
failed "because it set a cement-plus-clinker export figure against a cement-only
production figure". The replacement did exactly that in the other direction, and the 65Mt
those editions discarded as a failed balance was the right cement-basis number all along.

**Read from the primary source, which was the page the study already cited.** The FY2025
presentation's Market Overview block splits the year three ways — domestic cement
53,992.9, cement exports 11,063.0, clinker exports 7,568.9 K Tons. All three are now
inputs; two assertions check the split closes; a third checks the corrected ratio came out
BELOW the one it replaced, because a repair that raised the number would mean the split
was read backwards.

**AND THE SENTENCES DID NOT AUTO-CORRECT WITH THE NUMBER.** Three passages asserted the
market is "NOT structurally slack"; one said "NOT currently slack" outright. At 86% with a
12.6Mt restart programme pending, that does not hold. The chart carried it too — 72.6 drawn
beside 76 under a caption calling the surplus the whole sector case — and no gate reaches
inside a picture.

**MOVED: nothing.** The price path never rested on the sector being tight: its first year
is a filed quarterly realisation and every later year holds flat in real terms. What
changes is the comfort around it, and the study now says so.

### Finding 8 — the terminal beta relevering. ACCEPTED IN FULL.

Terminal beta 1.074 is the explicit 0.928 unlevered and relevered, at a statutory 22.5%
that no delivered document stated. **This repository had already caught it**: ARCC sat on
`check_ke_reproduction`'s ratchet for exactly this, down to solving the implied tax rate
out of the answer. The record now declares the construction, the tax rate and both betas;
section 1.5 — which ran a full page on the beta and never mentioned a second one existed —
now states the construction, what it is worth, and why two tax rates appear in one model.
Ratchet shortens 3 → 2. **MOVED: nothing.**

### Finding 9 — two published premium bases. ACCEPTED IN FULL.

The cited country-risk file publishes a rating basis and a CDS basis in the same row, 4.53
points apart, and this study showed a reader one of them. The record already named the
alternative and carried `None` for its figure. **Read from the file, not from the audit**:
the workbook is committed in this repository. Applied consistently the rating basis costs
118 basis points more, and the adopted basis is the cheaper of the two. The study now says
that in those words. **MOVED: nothing** — but a reader who prefers the other basis now has
the number to substitute.

### Finding 10 — the real price-cost wedge. ACCEPTED, AND WORSE THAN REPORTED.

The auditor found two paragraphs printing opposite-signed numbers under one word. The
larger error is in the sentence beside them: **"the EBITDA margin falls from the audited
39.3% to 40.4% by FY2030"**, followed by an explanation that "part of the 2025 step-change
gives back". The path is 39.03, 39.49, 39.99, 40.20, 40.40 — it dips once and rises past
the audited year every year after.

What replaces it is a **weaker** claim, which is why it is worth stating carefully: on the
published ladders cost outruns price, but the cost the model CHARGES grows 3.1% slower
than price once the alternative-fuel saving is netted off. So the margin does not give
back — and a forecast ending above a company's best filed year needs its mechanism named
rather than a sentence saying the opposite. **MOVED: nothing.**

### Finding 11 — the workbook's beta label. ACCEPTED IN FULL.

The Assumptions sheet labelled the adopted beta "own-stock weekly regression", which is
the construction section 1.5 explicitly rejects, on the input the study calls its most
consequential contested judgement. The two are 12% of value apart. The label now names the
tier and the peer set, and the rejected regression sits beside it with its R-squared,
standard error and observation count — none of which the workbook held at all.
**MOVED: nothing.**

### Finding 12 — the tie presented as a test. ACCEPTED IN FULL.

"It is not forced to... a wrong price assumption would show up as a non-zero residual." It
is forced to. Prices are derived as revenue over volume, so revenue rebuilt as volume times
price reconstructs by construction, on any volume whatever. **The workbook has said so
since revision 4** — "Rows 76-81 are a TIE, not a test... Revision 3 presented exactly this
identity as 'a test that can fail'. It cannot." — and the document went on presenting it as
a test. The residuals stay, because a tie that failed to foot would be an arithmetic error;
the claim that footing corroborates the volume goes, and the test that CAN fail is named
instead — the three derived prices held against a market, including the export clinker
figure sitting a third below the trade-press range. **MOVED: nothing.**

### Finding 13 — the EFG reconciliation's discount bar. ACCEPTED IN FULL.

A typed receipt from an earlier edition: "our 24.5% → 14.5%" against a schedule running
27.60% → 18.34%, "our 0.4876" against factors that give nothing of the kind, and "the whole
bar is EGP 0.16" against a bar the build computes at −6.19. Two values for one bar, 38×
apart, in the one section sold to a reader as a reconciliation they can check. **Worse
than stale, the direction was reversed**: on EFG's own calendar it is OUR factor that
discounts the far end harder, and the receipt said the opposite. All of it is now written
from the live schedule and the computed bar. The same file's valuation-date label still
read "1 Jan → 6 Aug" after the date moved to 30 June. **MOVED: nothing.**

### Finding 14 — one name, two values. ACCEPTED IN FULL.

The workbook cell, the Fundamental Valuation sheet and the bibliography headline all
carried the retired construction — profit grown a year against an ungrown capital base —
under the name the document gives the adopted figure, which the document says in terms is
not used. Both are now published, each labelled as what it is, and the adopted one is a
formula rather than a paste. **MOVED: nothing.**

---
## Still to adjudicate — findings 4 and 6

**Two remain, both escalated, neither implemented.** They are the only two of the fourteen
where the sentence is right and the NUMBER behind it is the question — so correcting
either moves the value, which is precisely why they are not settled by this desk:

| # | Finding | Claimed impact |
|---|---|---|
| 4 | Terminal risk-free of 12.50% reconciles to the 7% target the study's own section 7 says it stopped using, not the 5% target its bibliography cites | ~+12% understated |
| 6 | FY2026 currency anchor hand-set 9.6% above the study's own observed spot, in the one year of a path the register calls "derived and never hand-set" | −4.7% to −5.8% |

**Findings 4 and 6 exceed the 5% escalation threshold and are escalated rather than
settled by this desk.** Both are INPUTS — a terminal risk-free rate and a currency anchor
— and correcting either moves the value, which is why neither is settled here. **Neither
is implemented.**

Findings 3 and 5 were on that escalation list and have come off it, for the same reason
in both cases: the auditor's price was the cost of FOLLOWING the study's wrong sentence,
not the cost of correcting it. A finding is escalated on what the repair costs, and a
repair that changes only a description costs nothing. **Findings 4 and 6 are not of that
kind — there the sentence is right and the number behind it is the thing in question.**
