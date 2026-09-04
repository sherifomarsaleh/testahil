# FERTIGLOBE — gap review, 4 September 2026

**AUDITED CENTRAL: 1.8105** — branch A, the marginal-cost-anchor framing, AED per share.
**AUDITED GAP: -32.2%** against the latest known price of AED 2.67 (3 September 2026).

The answer is two-sided and only one branch is audited here, because only one breaches.
Branch B — the structurally-tight framing — reads AED 2.6846, **+0.55%** against the same
price, which is inside the band and owes no review. That is not a detail beside the
finding; it is most of the finding, and this review says so at the top rather than at the
end.

A gap is EVIDENCE OF A POSSIBLE DEFECT and the price is the only instrument in the room
that measures it. What follows is the hunt for OUR error, before any conclusion about the
market's. Two real defects were found. Both push the value UP, so both are candidate
causes of this gap; neither was corrected in this pass and the reason is stated under
DISCOUNT RATE.

---

## 1. LATEST FILINGS

Every disclosed period is read. Audited consolidated financial statements for FY2022,
FY2023, FY2024 and FY2025 (the FY2025 set PwC-signed 4 March 2026); the reviewed
condensed interim statements for the six months ended **30 June 2026**; the Q2 2026
results MD&A of 28 July 2026; and the FY2025 annual report, whose notes 15, 16 and 22
this pass read directly for the minority percentages, the borrowings roll-forward and the
split of the finance charge.

The most recent disclosed period is the reviewed half to 30 June 2026. **No later period
exists**: the third quarter had not closed at the price date, so there is no unread
filing behind this gap. That is the defect this heading exists to catch and it is not
present here.

## 2. BASE YEAR

FY2026 is half reported and is built that way rather than annualised. The own-produced
segment's first half is the **disclosed actual** — revenue USD 1,597.0mn and EBITDA USD
709.6mn from the segment note — and only the second half is modelled, at the same
calibrated pass-through the rest of the forecast uses. Nothing in the base year is
annualised, scaled or solved out of a profit line.

The one line not built from unit economics is third-party trading, carried at a segment
margin because the company discloses traded volumes and never a purchase price. That gap
is stated in the study rather than papered over, and it is not large enough to carry a
third of the value.

## 3. MACRO COHERENCE

One path, and it is the house path rather than the study's own. The study commits a macro
record that reproduces against `engine/macro_paths/AE.json`: terminal growth of 2.00% is
the house terminal inflation plus a **stated** real growth of zero, derived rather than
typed; the currency path is flat, which is the derived purchasing-power path under a hard
peg and not a hand-set one; and the explicit window ends with revenue growing 1.37%,
within 2pp of the terminal.

The `inflation_inputs` block is declared **EMPTY**, and the question was asked of the
model rather than of the description of it. Revenue is tonnes times a US dollar
benchmark; cost per tonne is a regression on that same realised price, so there is no
escalator anywhere in the cost stack to sit on a ladder. Inflation enters once, in the
terminal, through the sanctioned builder.

**Nothing here explains the gap.**

## 4. DISCOUNT RATE

**A defect, measured, and it makes the value too LOW.** The cost-of-capital weights are
struck on NET debt while the bridge also deducts net debt, so the cash lightens the debt
weight — raising the rate the operations are discounted at — and then comes back through
the deduction. The two coherent conventions are gross weights with a net-debt deduction,
or net weights with a gross-debt deduction; this is neither.

Priced: the equity weight is 0.9018 on net debt against 0.7662 on gross, and the cost of
capital 11.897% against 10.848% — **105 basis points**, and correcting it raises the
value.

The company is net DEBT rather than net cash (USD 621.2mn at 30 June 2026), so the equity
weight stays below one and the operating rate below the cost of equity; the inversion
this test exists for cannot arise here. Country risk is counted once: the risk-free rate
is the Abu Dhabi sovereign yield less that sovereign's own default spread, and the
premium added back carries the country risk on the same rating basis.

**Why it was not corrected in this pass.** It is one of two levers found here that both
push the value up, and stacking two individually-justified moves in a single edition is
what the promotion guard forbids. Both are named in the study's own committed records
rather than left to memory, and they belong to a deliberate cost-of-capital pass with the
order fixed before either is applied.

## 5. TERMINAL

The terminal was **rebuilt in this pass** and is no longer the retired reinvestment
identity. It is built through the sanctioned module on a composite asset life of 22.04
years **derived from the company's own property note** (cost over annual depreciation),
not on 1/g — which at a 2% terminal would have implied a fifty-year replacement cycle,
a fact about the dirham's peg rather than about a plant.

Terminal growth of 2.00% is the house terminal inflation plus a stated real growth of
zero, so it is coherent with the inflation inside the terminal discount rate by
construction. The terminal is 56.35% of enterprise value under branch A, which is
inside the range this method treats as ordinary.

**The second defect, and it also makes the value too low.** The model discounts the
terminal at 4.73% risk-free — today's sovereign yield less today's default spread —
while the house path derives a terminal risk-free rate of 3.98% from the inflation
target plus its real-rate convention. A pegged market gets a flat schedule, but flat
should mean flat at the NORM, and this is flat at the spot. Worth about 75 basis points,
and correcting it raises the value. Recorded in the study's macro record under the field
the gate reads, so the gate fails on it rather than a green tick standing over it.

## 6. BALANCE SHEET

The bridge stands on the **reviewed 30 June 2026** balance sheet, which is the latest
disclosed — the stale-sheet defect is not present. Enterprise value 6,139.6, less net
debt 621.2, less minorities 1,451.3, giving equity attributable of 4,067.0 and AED 1.8105
per share on 8,249.6mn shares at the peg.

The minority is the largest single step and is deducted at its share of **equity value**,
proxied by its disclosed share of group profit rather than by ownership, because Sorfert
(49.01% outside) and Egypt Basic Industries (25.0% outside) are the group's most
profitable assets and an ownership-weighted deduction would understate the claim. Book,
profit share and proportional are published beside the adopted basis. No associates are
carried and the evidence for that is stated; no dividend is deducted, because the interim
distribution is already out of the 30 June equity the bridge stands on.

## 7. CLAIMS AGAINST THE RECORD

The delivered documents were scanned for absolute claims — "best ever", "highest",
"never", "record", "first time", "unprecedented". **Every hit is methodological rather
than factual**: "margins are outputs of the build, never inputs to it", "the weights had
never been tested against anything", and two statements that the company never discloses
a purchase price for traded volumes. Not one is a claim about the company's filed record,
so there is no typed superlative here to recompute. This is the heading that found a
false "above the best single quarter this company has ever filed" on another name; on
this one it finds nothing to correct.

## 8. MULTIPLE CROSS-CHECK

| Basis | Branch A implies | The price implies |
|---|---|---|
| EV / FY2026E EBITDA | 4.60x | 6.05x |
| EV / FY2025A EBITDA | 5.99x | 7.87x |
| Equity / FY2025A profit to owners | 9.37x | 13.82x |

The peer set trades from 5.2x to 10.4x forward EV/EBITDA (Yara 5.2, OCI 5.6, CF 6.1,
Nutrien 7.4, Industries Qatar 9.1, SABIC Agri-Nutrients 10.4).

**Branch A's implied 4.60x on 2026E EBITDA sits BELOW every peer**, and that is stated
plainly rather than buried: it is the sharpest thing in this review against branch A. It
is not incoherent — branch A's whole premise is that 2026 EBITDA is a peak that
normalises, so a multiple struck on a peak year should look low — but a forward multiple
outside the entire peer range is exactly the shape a defect makes. On FY2025 actual
EBITDA, which is not a peak, branch A implies 5.99x and sits inside the peer range,
which is the reading that resolves it.

---

## VERDICT

**The gap is not primarily a defect, and the reason is structural rather than a
judgement call.** Branch A and branch B differ only in the nitrogen price path, which is
this study's declared central contested judgement, published as two framings rather than
averaged. Branch B agrees with the market to within half a percentage point. What the
32% gap measures is therefore a disagreement about ONE question — whether nitrogen
prices normalise toward the marginal cost of the swing supplier or the current tightness
persists — and a reader is shown the question rather than a single number that asserts
the answer.

That said, **two real defects were found and both run the same way**, which is the part a
review of a below-price answer is for: the net-debt weighting (105bp) and the
spot-anchored terminal risk-free rate (75bp). Both raise the value, so both narrow this
gap, and neither was taken in the same pass as the terminal rebuild. They are registered
in the study's own committed records and belong to a deliberate cost-of-capital pass.

**The answer does not change here.** No number was moved toward the price: a fair value
adjusted to meet a quote is the reverse-engineered rate this method prohibits outright,
arriving through the front door instead of the side one. The honest output of this review
is an unchanged central with two named corrections owed and a stated reason for the
disagreement.

This study is in any case HELD from publication — the method has not cleared its own
Phase 1 acceptance criteria — so nothing here reaches a reader before those corrections
are made.
