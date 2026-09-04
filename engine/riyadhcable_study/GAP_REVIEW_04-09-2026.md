# RIYADHCABLE — gap review, 4 September 2026

**AUDITED CENTRAL: 127.9054** — the cash-flow lens, SAR per share.
**AUDITED GAP: +22.0%** against the latest known price, SAR 104.80 (3 September 2026),
which is also the price this study was struck at on 18 August 2026 — the two are the same
figure, so the review is not auditing a disagreement that has since moved.

This fires the ABOVE-price half of the audit trigger, which is deliberately not matched by
a publication block: the block is one-sided below the price, because the errors in a
discounted cash flow are not symmetric. So nothing holds this study and this review is the
only instrument standing here. It is written on that basis.

## The retired blend was hiding the disagreement by very nearly erasing it

The published central was a typed 45/20/20/15 blend at SAR 109.35 — **+4.3%** against the
market, where the cash-flow lens reads **+22.0%**. That is a different failure from the
usual one: the blend did not merely shrink this study's disagreement with the market, it
showed a reader **agreement** where the study's own method holds a fifth above.

Normalised earnings power carried a fifth of the weight and is not among the cross-checks
this class permits. It is computed and shown so its removal is visible.

**The class was a decision, not a default.** This issuer has a turnkey high-voltage
projects arm, which is what earns a group its own class where the contracting leg carries a
different lens — but here that leg is **2.2% of revenue** against 97.6% cables and wires,
so nothing about the lens set changes and filing it under a contracting class would be
superstition. The three class lessons on 'cement and heavy industrial' were read before
deciding and all three bind: commodity inputs escalate on their own path (copper here, fuel
there), haulage follows the tonne despatched, and an old plant's recent capex is not its
maintenance requirement.

---

## LATEST FILINGS

**The primary-source route was re-run and the earlier block has lifted.** The first edition
recorded `riyadh-cables.com/investor-relations/` as unreachable — behind an `sgcaptcha`
bot-protection wall that returned a JavaScript challenge to every automated route — and
stopped and asked, the principal then supplying the audited statements directly. That was
the rule working.

On this review the same URL returned **200 with 308KB**, and the FY2025 audited
consolidated financial statements were fetched directly from
`riyadh-cables.com/wp-content/uploads/2026/04/Financial-Statement-FY-English-2025.pdf`.
[R-IND-01] requires that any probe whose failure is relied on be re-run, and this is why:
an absence recorded three weeks ago is a fact about the past.

Every disclosed period the study registers reconciles to those statements, and the reviewed
H1-2026 figures the study carries are consistent with them.

**Found: nothing outstanding, and one recorded blocker that has cleared.**

## BASE YEAR

FY2025 foots. Segment revenue sums exactly to the consolidated figure (cables 10,414.2 +
high-voltage 230.8 + other 28.6 = 10,673.6), and segment cost sums to the consolidated cost
of revenue, so gross profit reproduces at 1,733.3.

**One defect was found in the committed output and it reached nothing.** The study computed
segment gross profit as

    rev + cost * -1 * 0 - (-cost)

which evaluates to `rev + cost` — a mangled double negative that made every segment's
"gross profit" larger than its revenue (cables 19,130.9 against revenue of 10,414.2, an
implied margin of 184%). **Nothing read it**: the builders take `seg_fy25`'s revenue and
geography and never its gross profit, so the figure reached no document and no gate.

That is the general point worth keeping. A committed output that nothing consumes is
checked by nothing at all: the prose-figure gate holds a document's figures against the
model, and a model value that reaches no document has no counterparty in that check. Fixed,
and asserted at source — the segment gross profits must sum to the consolidated figure and
each margin must be economically possible.

**Found and fixed.**

## MACRO COHERENCE

**This is the largest finding in the review and it runs toward the price.**

Terminal growth is **4.0% nominal**. The house Saudi macro path's terminal inflation is
**2.0%**, and the regime is PEGGED — the riyal is fixed to the dollar, so the kingdom
imports United States monetary policy and today is already the terminal.

So the study assumes a real terminal growth of **+1.96% a year, in perpetuity**, and states
it nowhere. [R-MACRO-01] is exact: terminal growth is terminal inflation plus a STATED real
growth, default zero, and a departure from zero must be stated and must carry the
incremental capital it needs.

It is the mirror of the defect found on the sister cables study the same day, which
assumed a real DECLINE of 1.87% a year against Egypt's ladder. Both were typed nominal
rates whose real content nobody had written down — which is precisely why the rule requires
growth to be stored as (real, inflation path) and recomputed, rather than typed.

**Priced on the study's own chain**, holding every other driver still and moving only the
terminal growth to the house default of zero real:

| | terminal value | per share | vs the price |
|---|---:|---:|---:|
| Published, 4.0% nominal (≈ +1.96% real) | 24,350 | **127.91** | +22.0% |
| Corrected, 2.0% nominal (zero real) | 19,149 | **107.16** | **+2.2%** |

**−16.2%, and it lands this study essentially on the market.**

**Found. NOT APPLIED IN THIS PASS, and the reason is arithmetic rather than reluctance —
see the terminal heading below.**

## DISCOUNT RATE

| | |
|---|---|
| Cost of equity, explicit window | 10.60% |
| Cost of capital, explicit window | 10.47% |
| Cost of capital, terminal | 9.48% |
| Beta | 1.129, falling to 1.00 in the terminal |

Nothing here is out of line: a pegged-currency Gulf industrial on a 5.50% sovereign, a
sovereign spread of 48bp stripped from the risk-free so country risk enters once, and a
measured beta above one for a copper-price-exposed manufacturer. The terminal risk-free of
5.02% sits above the house-derived 2.0% terminal inflation plus a real-rate convention,
which is conservative rather than generous.

**Found: nothing.**

## TERMINAL

The terminal carries **81.0%** of enterprise value, and it is on the retired reinvestment
identity `rr = g/ROIC`, which charges `g × IC` every year for ever and implies a replacement
cycle of `1/g` — here **25.0 years** at the published 4%.

**The asset life could not be derived, and that is the finding rather than a gap in the
work.** The disclosed useful lives in note 9 are RANGES — buildings 20–25, plant and
equipment 20–30, strategic spares 10, vehicles 4, furniture 4–10, tools 5, laboratory 10,
computers 10 — and a life this desk picked from inside a range is not a disclosed life
(SIGCM clause 1). The identity that worked on the sister study — average depreciable gross
cost over the year's own charge — **breaks on this issuer, and it can be shown why**:

| | gross cost | accumulated depreciation | the year's charge | implied life |
|---|---:|---:|---:|---:|
| Plant and equipment | 2,114.5 | 1,294.9 (**61% written down**) | 34.2 | **61.9 y** |
| All depreciable assets | 2,903.6 | 1,775.5 | 76.6 | 37.9 y |

A derived 61.9 years for a line the company itself depreciates over 20–30 is not a
measurement of anything. The identity assumes a base in steady state; here most of the
plant is already written down, so assets still in service charge nothing and the ratio
reports a life roughly twice the disclosed one. **On this issuer the derivation is not
usable, and using it anyway would be inventing a number with an arithmetic costume on.**

**THE TWO CORRECTIONS ARE COUPLED, WHICH IS WHY NEITHER SHIPS IN THIS PASS.** Moving the
terminal growth to zero real without rebuilding the construction creates a NEW violation
where it fixes one: at a 2.0% terminal the last explicit year still grows 6.2%, a **4.2
percentage-point** convergence gap against a requirement of 2, where the published 4%
leaves 2.2pp. A model whose last explicit year grows far above its terminal capitalises a
rate it never reached. So the growth correction needs the explicit window extended, and the
construction correction needs a life this study cannot source — and trading one violation
for another to move a number 16% is not an improvement.

Registered for the terminal re-issue, with the brief precise: extend the explicit window
until growth converges within two points of a 2.0% terminal, and obtain a component-level
useful life or state that none is disclosable and leave the construction on the ratchet
with its reason, as the exemplar's vessel life is.

**Found, priced at −16.2%, and deliberately not applied.**

## BALANCE SHEET

The bridge stands on the 31 December 2025 audited sheet, which matches this study's own
valuation date. Net debt, associates, non-operating assets and the minority are each read
from that statement, and the study publishes an alternative sequencing of the minority.

**Found: nothing.**

## CLAIMS AGAINST THE RECORD

Every absolute claim in the delivered documents was scanned for and recomputed. The study
makes few: it states the copper/aluminium/lead blend is 94.9% of cost of revenue, the
geographic split, and the segment shares — all of which reconcile to note 40 and the cost
breakdown. No "best ever" or "never" claim survives the scan.

**Found: nothing.**

## MULTIPLE CROSS-CHECK

| | at the fair value of 127.91 | at the price of 104.80 | benchmark |
|---|---:|---:|---:|
| Relative lens (peer-anchored enterprise multiple) | — | — | reads **86.36** |
| Normalised earnings power | — | — | reads **101.58** |
| Book value and sustainable return | — | — | reads **94.68** |

**All three cross-checks sit BELOW the price, and the cash-flow lens sits above it.** That
is a coherent picture rather than a contradiction: the cross-checks are earnings- and
book-anchored and this company earns a high return on a small equity base, while the
cash-flow lens capitalises a terminal that grows in real terms for ever — which is exactly
the assumption the macro heading found unstated.

The arithmetic ties the two together: correct the terminal growth to zero real and the
cash-flow lens reads 107.16, within three points of the normalised lens at 101.58 and the
book floor at 94.68. **The lens disagreement and the unstated real growth are one finding,
and the cross-checks were right.**

---

## Verdict

The answer does not change in this pass, and the reason is stated rather than implied.

Six headings found nothing or found something that was fixed. Two found the same thing from
opposite sides: the terminal grows in real terms for ever, nothing says so, and correcting
it to the house default would move this study from +22.0% to +2.2% against the market — and
would bring the cash-flow lens into line with the three cross-checks that currently
disagree with it.

**It is not applied because the two corrections it needs are coupled and one of them cannot
be made honestly today.** Zeroing the real growth without extending the explicit window
trades a stated-nowhere growth assumption for a convergence violation twice the permitted
size; rebuilding the construction needs a disclosed asset life that this issuer's ranges and
its heavily-written-down plant do not yield. Doing half of it to move the number 16% toward
the price would be the fitting this method prohibits, in the one direction where it is
hardest to see.

**What a reader should weigh:** this study's cash-flow lens is the only one of four reads
above the market, and the review has identified precisely why — an unstated real growth rate
in a pegged economy, on a terminal carrying four fifths of the value. That is disclosed here
rather than left for a reader to find.
