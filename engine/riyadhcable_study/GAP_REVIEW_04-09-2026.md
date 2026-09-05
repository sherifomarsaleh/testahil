# RIYADHCABLE — gap review, 4 September 2026

**AUDITED CENTRAL: 124.8948** — the cash-flow lens, SAR per share.
**AUDITED GAP: +19.2%** against the latest known price, SAR 104.80 (3 September 2026),
which is also the price this study was struck at on 18 August 2026 — the two are the same
figure, so the review is not auditing a disagreement that has since moved.

*Revised the same day. This review first audited a central of 127.9054 at +22.0% and
recorded the terminal rebuild as one that could not be made honestly. That assessment was
tested and it was wrong; the terminal is rebuilt and the TERMINAL heading below carries both
the correction and the reasoning that failed, rather than the correction alone. It then took
a second correction the same day — the age its maintenance charge rests on, measured off the
notes rather than assumed. **And then a third, which corrected the first two**: the terminal
was handed a profit figure already grown by one year, which the sanctioned construction
grows again, overstating the terminal by exactly (1+g) — 4.00% here. So the central is
124.8948 and the route is 127.9054 → 126.1849 → 124.8948, recorded lever by lever. The
direction reverses with that correction: BOTH levers now move the answer DOWN, toward the
price, where the first version of this review reported the terminal moving it away.*

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

The terminal carries **81.4%** of enterprise value. It was on the retired reinvestment
identity `rr = g/ROIC`, which charges `g × IC` every year for ever and implies a replacement
cycle of `1/g` — **25.0 years** at a 4% nominal terminal. It is now built through the
sanctioned construction, and the two things that were said to make that impossible were
tested rather than reasoned about.

### What the first version of this review said, and why it was wrong

It said two things, both carefully argued and both false.

**First, that the asset life could not be derived.** The evidence offered was that the
identity — gross cost over the year's own charge — returns **61.9 years** for the plant and
equipment line the company itself depreciates over 20 to 30, so "the derivation is not
usable on this issuer". The observation is exactly right and the inference from it is not.
The identity does not return the ACCOUNTING life and is not trying to: it returns the
**economic replacement cycle**, and it comes out longer than the accounting life *for a
reason the company discloses in the same note* — **SAR 841.7mn of cost, 29.0% of the
depreciable base, is fully depreciated and still in use.** Those assets are in service and
will one day need replacing, and they charge nothing. A maintenance charge asks how much
must be spent each year to keep the base intact, which is the economic cycle; using the
accounting life instead would charge for replacing plant that is demonstrably still running.

The method is validated on this issuer's own accounts, on the one leg where a single life IS
disclosed: **software, at 14.43 years derived against a stated 15, 3.8% apart.** A
derivation that reproduces a disclosed figure is the strongest evidence a derivation can
carry, and it is available here.

| | gross cost (SAR) | the year's charge | implied life |
|---|---:|---:|---:|
| Property, plant and equipment, less land and assets under construction | 2,903,588,021 | 76,616,111 | 37.90 y |
| Software (note 10) | 80,879,539 | 5,603,548 | 14.43 y *(disclosed 15)* |
| Right-of-use assets (note 13) | 68,978,523 | 3,175,978 | 21.72 y |
| **Blended** | **3,053,446,083** | **85,395,637** | **35.76 y** |

The three charges sum to **85,395,637**, which *is* the depreciation and amortisation this
model carries for FY2025 — the base and the charge are the same object, not two figures
brought together. On FY2024's own columns the same identity gives 40.27 years; the FY2025
reading is the shorter and therefore charges the heavier maintenance, and it is the one
adopted.

**Second, that the growth correction and the construction correction were coupled, so
neither could ship.** The argument was that moving terminal growth to zero real would leave
the last explicit year growing 6.2% against a 2.0% terminal — a 4.2-point convergence gap
where two is permitted. That is true of *zeroing* the growth. It is not what the rule
requires. A stated real growth is permitted and must simply be **written down as the real
number it is**, so the 4% nominal this study always carried is now stored as **+1.96% real
on the house Saudi path**, from which 4.00% is derived to the basis point. Nothing moves,
the convergence gap is unchanged at 2.2 points, and what a reader gains is the ability to
see that this business is assumed to grow ~2% a year in real terms for ever — which is the
claim, and it was previously invisible inside a nominal rate.

**The general shape is worth naming because it is the second time in one day:** an obstacle
assessed from the structure of a change is not the same as an obstacle measured. Both
premises here were true and neither conclusion followed.

### What the terminal now charges

| | SAR mn |
|---|---:|
| Terminal-year operating profit after tax | 1,586.9 |
| Plus depreciation and amortisation charged inside it | 133.6 |
| Less capital maintenance, at what replacement costs today | (190.3) |
| Less the capital that real growth needs | (128.4) |
| Less inflation on working capital | (88.0) |
| **Terminal free cash flow** | **1,313.8** |

That is **82.8%** of terminal profit paid out for ever. The retired identity gave a terminal
of 24,350 against the sanctioned **23,961**, **−1.60%**, worth **−1.34%** on the answer:
127.9054 → **126.1849**.

*This figure read +2.34% for part of 4 September 2026 and the correction is worth recording.
The construction was handed a profit figure ALREADY GROWN by one year, and it grows the flow
itself — `tv = fcff(1+g)/(w−g)` puts the first perpetuity year in the numerator and values
the terminal at the end of the last explicit year, which is where it is discounted. Handing
in a grown figure therefore values a year-seven flow at a year-five date and overstates the
terminal by exactly (1+g), 4.00% here. Corrected, the sanctioned terminal is BELOW the
retired one rather than above it.*

**The direction here is DOWN, and the first version of this review said the opposite.**
The reasoning it gave was sound as far as it went — 1/g charges 25 years against a base the
accounts turn over in 35.8, so on the replacement-cycle argument alone it charges too little
— but the sanctioned construction does not only change the cycle. It charges maintenance at
what replacement costs today and adds book depreciation back, and on this base those two
outweigh the growth charge the identity was levying. Corrected for the growth-basis error
above, the sanctioned terminal comes out 1.60% BELOW the retired one, and the answer moves
**toward** the price rather than away from it. Nothing about that makes the correction
optional: it is applied because it is the better construction, and the direction is reported
rather than chosen.

### The one reading that was recorded and not applied — now applied

The construction escalates the book charge over **half** the life, as a proxy for the age of
the average asset. On this issuer the age can be **measured** rather than assumed:
accumulated depreciation over the year's own charge is, under the straight-line method these
accounts use, exactly the charge-weighted average age of the assets bearing that charge — an
identity, not an estimate.

| | accumulated | the year's charge | age |
|---|---:|---:|---:|
| Property, plant and equipment (note 9) | 1,775,547,325 | 76,616,111 | 23.17 y |
| Software (note 10) | 29,319,636 | 5,603,548 | 5.23 y |
| **Charge-weighted** | **1,804,866,961** | **82,219,659** | **21.95 y** |

Against the **17.88** years half a 35.76-year life implies. The two legs differ sharply — an
old plant and a young accounting system — and the blend is the point.

The right-of-use note discloses balances *net* of depreciation and carries no accumulated
column, so its 3.7% of the charge is left out of both sides. Those assets are new (the land
lease was recognised in 2025), so excluding them **overstates** the age and therefore the
charge, which is the conservative direction.

**When this review was first written, this was recorded and NOT applied**, on the ground
that replacing the shared construction's own proxy inside one study is a rule change made in
the wrong place. That was right, and the answer was to make the change in the right place
instead: the shared construction now takes a measured age where one is supplied and sourced,
and says on its own record which of the two it used. So the reason for holding it is gone
and it is applied here.

It raises maintenance **8.4%** (190.3 → 206.3), takes the terminal to 24,616 and the central
to **124.8948** — **−1.02%**, and toward the price. It is applied because it is the better
measurement, not because of the direction it moves. **This name is one of only two in six
where the accounts permit the measurement at all**: three deduct residual values from the
depreciable amount and one assembled its base by acquisition, and on those the identity does
not return an age.

**Found and applied: −1.34% from the construction, then −1.02% from measuring the age it
rests on rather than assuming it. Net −2.35%, 127.9054 → 124.8948 — both levers moving the
same way, toward the price.**

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

**The answer changed in this pass, by −2.35%, and it moved toward the price.**

Six headings found nothing or found something that was fixed. The terminal found the one
material thing, and it found it twice: the construction was the retired identity, and this
review's own first attempt talked itself out of correcting it on two premises that were
individually true and jointly wrong. Both were tested. The life derives, and validates
against the one life this issuer discloses; the growth rate needed storing, not zeroing.

**What a reader should weigh.** This study's cash-flow lens remains the only one of four
reads above the market, and it is now further above it. That is not a finding about the
market: it is the arithmetic of a terminal that carries four fifths of the value being
charged for what keeping a cable plant intact actually costs, on the life the company's own
notes imply, rather than for rebuilding the whole plant every twenty-five years because that
is one over the inflation rate. The cross-checks that disagree — a relative multiple at
86.36 and a book floor at 94.68 — are published beside it at their own values and are not
averaged into it.

**And the maintenance charge no longer rests on an assumption.** The construction escalates
the book charge over the age of the base; this study now supplies the age its own notes
measure — 21.95 years — rather than the 17.88 half a life implies. That is the smaller of
the two corrections in this pass and it runs the other way, which is worth saying plainly:
the two moves are −1.34% and −1.02%, and neither was chosen for its direction. An earlier
version of this review reported the first as +1.97% on a terminal handed a profit figure
already grown by a year; that is corrected above and the direction reverses with it.
