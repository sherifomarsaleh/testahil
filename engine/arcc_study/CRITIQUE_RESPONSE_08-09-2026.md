# ARCC — response to the forensic audit of 8 September 2026

**Status: IN PROGRESS. Two findings adjudicated and fixed, both DISCLOSURE. No valuation
figure has moved and none will move without its own entry here.**

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

---

## What both findings share, and it is the finding under the findings

The two total fails with the largest prices attached are **one root cause**: a calibration
that is computed, logged, reasoned about and applied — and then described to a reader in a
third of its extent, with a claim built on the part that was left out. Nothing was hidden
from the model. Everything was hidden from the page.

Every gate in this repository passed it, and they were right to: the recalculation
reconciles because the arithmetic is correct, the prose-figure check passed because 16.5%
is not printed anywhere to be checked against, and the numeric-traceability bar passed
because no figure was typed. **A number that is absent from a document cannot be checked
against the model, and a sentence that quotes one operand of two is not a wrong figure —
it is a true figure describing a different quantity.**

---

## Still to adjudicate

Twelve further findings, none implemented, listed with the auditor's own claimed price so
the debt is countable rather than remembered:

| # | Finding | Claimed impact |
|---|---|---|
| 3 | Terminal replacement-cost invested capital of EGP 51,191mn does not reproduce from the two operands the page states it is the product of (5.0Mt × USD 130/t × 50.30 = 32,695) | +14.5% if the printed operands are taken literally |
| 4 | Terminal risk-free of 12.50% reconciles to the 7% target the study's own section 7 says it stopped using, not the 5% target its bibliography cites | ~+12% understated |
| 5 | Terminal value discounted at 0.41558 while the page prints 0.4521, with the workbook's own cell comment stating the difference | +4.6% if the printed instruction is followed |
| 6 | FY2026 currency anchor hand-set 9.6% above the study's own observed spot, in the one year of a path the register calls "derived and never hand-set" | −4.7% to −5.8% |
| 7 | The 96% sector-utilisation claim mixes clinker into a cement-only denominator | narrative |
| 8 | Terminal beta 1.074 is a relevering the document never names, at a tax rate stated nowhere | disclosure |
| 9 | Two published equity-premium bases; the cheaper is adopted without disclosure | disclosure |
| 10 | The stated real price-cost erosion of −3.1% does not reproduce and its sign is inverted (+3.24%) | logic |
| 11 | The adopted beta is labelled in the workbook as the own-stock regression the study explicitly REJECTS; 0.9275 is the peer median | disclosure |
| 12 | "Reproduces audited FY2025 revenue to +0.000%" is an algebraic identity presented as a test that could fail | logic |
| 13 | Two irreconcilable accounts of the study's own discount schedule | logic |
| 14 | Three delivered artefacts publish two different values for the same named quantity | disclosure |

**Findings 3, 4, 5 and 6 each exceed the 5% escalation threshold and are escalated rather
than settled by this desk.** They are also not independent: 4 and 5 both concern how the
terminal is brought home, and taking them one at a time with a ledger entry each is the
rule, not a preference. **None of them is implemented.**
