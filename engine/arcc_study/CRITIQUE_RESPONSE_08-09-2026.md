# ARCC — response to the forensic audit of 8 September 2026

**Status: IN PROGRESS. Four findings adjudicated and fixed — 1, 2, 3 and 5 — every one of
them DISCLOSURE. No valuation figure has moved and none will move without its own entry
here.**

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

## Still to adjudicate

Ten further findings, none implemented, listed with the auditor's own claimed price so
the debt is countable rather than remembered:

| # | Finding | Claimed impact |
|---|---|---|
| 4 | Terminal risk-free of 12.50% reconciles to the 7% target the study's own section 7 says it stopped using, not the 5% target its bibliography cites | ~+12% understated |
| 6 | FY2026 currency anchor hand-set 9.6% above the study's own observed spot, in the one year of a path the register calls "derived and never hand-set" | −4.7% to −5.8% |
| 7 | The 96% sector-utilisation claim mixes clinker into a cement-only denominator | narrative |
| 8 | Terminal beta 1.074 is a relevering the document never names, at a tax rate stated nowhere | disclosure |
| 9 | Two published equity-premium bases; the cheaper is adopted without disclosure | disclosure |
| 10 | The stated real price-cost erosion of −3.1% does not reproduce and its sign is inverted (+3.24%) | logic |
| 11 | The adopted beta is labelled in the workbook as the own-stock regression the study explicitly REJECTS; 0.9275 is the peer median | disclosure |
| 12 | "Reproduces audited FY2025 revenue to +0.000%" is an algebraic identity presented as a test that could fail | logic |
| 13 | Two irreconcilable accounts of the study's own discount schedule | logic |
| 14 | Three delivered artefacts publish two different values for the same named quantity | disclosure |

**Findings 4 and 6 exceed the 5% escalation threshold and are escalated rather than
settled by this desk.** Both are INPUTS — a terminal risk-free rate and a currency anchor
— and correcting either moves the value, which is why neither is settled here. **Neither
is implemented.**

Findings 3 and 5 were on that escalation list and have come off it, for the same reason
in both cases: the auditor's price was the cost of FOLLOWING the study's wrong sentence,
not the cost of correcting it. A finding is escalated on what the repair costs, and a
repair that changes only a description costs nothing. **Findings 4 and 6 are not of that
kind — there the sentence is right and the number behind it is the thing in question.**
