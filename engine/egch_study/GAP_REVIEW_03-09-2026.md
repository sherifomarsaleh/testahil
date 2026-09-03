# EGCH — valuation gap review, 3 September 2026

**Trigger.** [R-GAP-01], as amended 03-Sep-2026. The answer is **TWO-SIDED** and both
branches breach:

| branch | value | vs spot 14.41 |
|---|---:|---:|
| cash-flow lens, ANNA capital programme **carried through** | **EGP 1.79** | **−87.6%** |
| cash-flow lens, ANNA capital programme **stopped** | **EGP 5.90** | **−59.1%** |

Spot is the close on the Egyptian Exchange on 3 September 2026, supplied by the principal
and committed at `engine/prices/SUPPLIED_03-09-2026.json`. The previous edition was struck
at 13.98 on 6 August.

**Two defects were found and corrected. The carried-through branch moved from EGP −1.06 to
EGP +1.79.** A negative fair value for a company with EGP 8.16 a share of disclosed book
equity, positive gross profit of EGP 5.2bn on revenue of EGP 11.3bn and no distress was
never a conclusion — it was a symptom, and it should have been read as one.

**The residual gap is the largest unexplained disagreement in this book and this review says
so plainly rather than closing it with more corrections.** Even corrected, the cash-flow
lens sits 88% below the market. What the two corrections bought is that the answer is now
*wrong-looking in a legible way* rather than impossible; what remains is set out at heading
8 with the reverse read that measures it.

---

## 1. LATEST FILINGS

Every disclosed period is read. The audited annual statements are read from the filings
themselves and the auditor's own report is used for the Damietta urea stock note and the
export-levy disclosure — the export realisation of US$385/t for FY2024/25 comes from that
report rather than from any aggregator. The interim disclosures for FY2025/26 are swept and
registered.

**No unread filing sits behind this gap.** The corrections below are both in the forecast
drivers, not in the historical record.

## 2. BASE YEAR

The base year foots to the filed accounts. FY2026/27 opens on revenue EGP 11,310.2mn and
gross profit EGP 5,164.7mn — a gross margin of 45.66% — built from disclosed tonnage, the
disclosed gas price and the export realisation, not from a growth rate on a prior total.

**THE DEFECT WAS NOT IN THE BASE YEAR. IT WAS IN THE PATH LEAVING IT** — the same place the
companion AMOC review found its own, and for a related reason.

As it stood, gross margin fell 45.66% → 42.20% → 38.23% → 35.07% → **33.02%** on essentially
flat revenue. That 12.6-point collapse was one typed array:

> `export_usd_path = [530.0, 500.0, 470.0, 450.0, 440.0]` — "Constructed: export price path,
> mean-reverting from the August 2026 quote toward the cash cost of the marginal gas-based
> producer."

A **−17% dollar output price over five years**, with no marginal cash cost quoted, no
institution publishing the path, and the source layer recorded as "Constructed". Meanwhile
the gas input is dollar-linked and held **flat in dollars** — the EGP gas price grows at
4.49% / 3.52% / 2.54% / 2.54%, which is exactly the currency path. So the construction was a
falling output price against a flat input price, and it then set a terminal worth 60% of
enterprise value.

**What settles it is not judgement, it is the book.** [R-FCAL-01] requires a driver to be
consistent with how that driver class is built across the market's book, and says a number
out of line with the rest of the book usually means our own method slipped on this one
name. AMOC — same house, same market, same week — holds *its* dollar commodity price flat
and registers the reason in as many words: *"crude is held FLAT in dollars — no forecast of
it is defensible."* Two studies in the same book cannot carry opposite conventions for the
same class of input, and the difference here ran the value-destroying way.

**Corrected: held flat in nominal dollars at US$530/t.** Margin path 45.7% / 44.9% / 43.9%
/ 43.0% / 42.1%. It is deliberately **not** raised to the US$545 CME FOB Egypt settlement of
7 August 2026 — declining to forecast a fall is not the same as adopting an improvement.
The bull path (560 → 515) is retained as the published alternative.

## 3. MACRO COHERENCE

One path, and it is derived rather than typed. The currency path is built year by year from
the relative purchasing-power identity on the study's own Egyptian inflation path against
long-run US inflation — `usd_egp_path` is a computed expression in the register, not an
array of typed numbers, and the register itself records that the 08-08-2026 edition typed a
4.5%-a-year path beside a derivation producing a different number in every year.

The same identity carries the dollar debt at local-equivalent cost, so the currency
assumption inside the cost of debt is the same one that sits inside revenue.

**With the export price now flat in dollars, the price and cost legs are on one clock**: both
are dollar-linked, both translate at the same derived rate, and neither is escalated at a
domestic inflation the other does not see. That was not true before the correction at
heading 2, and it is the [L-048] failure in its third variant this session.

## 4. DISCOUNT RATE

**THE SECOND DEFECT, AND IT IS AN INCONSISTENCY ACROSS THE BOOK RATHER THAN AN ERROR INSIDE
THE STUDY.**

[R-COC-01] is explicit: *"Both premium bases are published and one is named CENTRAL (the
swap basis by default — the market's own live pricing of the sovereign's credit, against an
agency judgement updated in steps)."* AMOC names the CDS basis central and records the
choice as its single largest contested number; ARCC's committed record carries
`erp_basis: "cds"`.

**EGCH published the RATING basis.** For the same sovereign on the same day:

| | rating basis | CDS basis |
|---|---:|---:|
| sovereign default spread | 6.372% | **3.410%** |
| equity risk premium | 13.937% | **9.410%** |
| cost of equity | 30.99% | **29.28%** |
| WACC | 25.64% | **24.62%** |

Three studies in one market on two conventions is the incoherence [R-MACRO-01] exists to
close, and the odd one out took the higher premium — again the value-destroying direction.
**Corrected to the CDS basis, which is the one the rule names.** Both remain published.

What is unchanged and correct: country risk enters once (the observed 23.0% sovereign yield
is normalised by Egypt's own default spread and the premium added back on the same basis);
weights are market-value; the dollar debt is carried at local-equivalent cost through the
same purchasing-power identity as the revenue.

**One disclosure that is carried and not resolved.** The study's own cost-of-capital record
warns that in FY2028/29 onward the local-equivalent FX cost of debt falls below the
normalised risk-free rate — *"looks like a raw FX coupon not grossed up for expected
depreciation"*. It is registered as a warning rather than a refusal. On a book that is
99.7% foreign-currency this is not immaterial, and it is listed at the foot of this review
as outstanding rather than quietly carried.

## 5. TERMINAL

Terminal growth 7.00% — the central bank's published inflation target, the same figure that
sits inside the terminal risk-free rate, so terminal growth is inflation with zero real
growth. Coherent, and the same construction as AMOC and ARCC.

Terminal value is **65.2% of enterprise value**, which is high, and it is high for a reason
this review can now name: the terminal is struck on a year that used to carry the collapsed
margin. With the dollar price flat the terminal EBIT is EGP 4,305.6mn against EGP 2,355.0mn
before — the terminal was capitalising an artefact.

A terminal at 65% of enterprise value remains the most sensitive part of this valuation and
is flagged as such rather than presented as settled.

## 6. BALANCE SHEET

The bridge stands on the latest disclosed balance sheet and foots:

| line | EGP mn |
|---|---:|
| present value of the explicit window | 3,493.1 |
| present value of the terminal | 6,548.2 |
| **enterprise value** | **10,041.3** |
| less net debt (debt 14,639.0 less cash 4,606.5) | −10,032.5 |
| plus investments at fair value through OCI | +1,382.9 |
| plus investment property | +2,155.1 |
| **equity value** | **3,546.8** |
| shares (mn) | 1,986.6 |
| **per share, carried through** | **EGP 1.79** |

**The structural fact a reader must see: equity is the thin residual between two large
numbers.** Enterprise value 10,041 against net debt 10,033. A 10% error in enterprise value
is a 28% error in the equity, and a 30% error in enterprise value roughly doubles or
eliminates it. This is why the two corrections above moved the answer so violently — from
−1.06 to +1.79 — and it is the honest reason to hold this study's precision lightly.

## 7. CLAIMS AGAINST THE RECORD

The contested judgement is **binary and its two answers straddle the interesting range**, so
it is published as two branches and never averaged: is the ANNA capital programme carried
through, or stopped? The gap between them is **EGP 4.11 a share, EGP 8,174mn of equity**.

The study's stated finding — that on the disclosed bank-approved cost and the derived
nameplate the programme does not earn the capital sunk into it, so stopping is worth more
than finishing — is recomputed and still holds after both corrections, though by a smaller
margin than before.

Recomputed in this pass: sustainable return on equity **6.9%** against a cost of equity of
**31.0%**, implying a justified price-to-book of 0.00x where the market pays **1.77x**. That
is the sharpest single statement of the disagreement, and it is computed rather than typed.

The retired weighted blend of ~3.76 that the delivered documents still published is removed
in this edition: the answer is two branches and a set of cross-checks, and a weighted
average of them describes a half-built plant, which is a world nobody is proposing.

## 8. MULTIPLE CROSS-CHECK

| | carried through (1.79) | stopped (5.90) | at the market (14.41) |
|---|---:|---:|---:|
| equity value, EGP mn | 3,547 | 11,721 | **28,627** |
| implied enterprise value, EGP mn | 10,041 | 18,216 | **35,121** |
| price to disclosed book (8.158/share) | 0.22x | 0.72x | **1.77x** |

The two cross-checks that are not the cash-flow lens **both sit far above it**:

- **Book value, EGP 8.16 a share** — the disclosed floor, published as such and never
  weighted. The cash-flow lens sits at 22% of it on the carried-through branch.
- **Relative multiple, EGP 15.47** — forward EBITDA on a multiple from own history and
  regional peers. Above the market.

**A cash-flow lens at a fifth of disclosed book, on a company with a 45% gross margin and no
distress, is not a conclusion. It is a flag,** and this review treats it as one.

**THE REVERSE READ — WHAT THE PRICE MUST BELIEVE, AND WHY IT IS NOT CREDIBLE EITHER.**

Solved on this study's own committed cash flows, holding every driver at its published
value and moving only the discount rate:

> EGP 14.41 implies a **flat nominal EGP discount rate of about 11%** on the
> committed-capital case and about 13% on the capital-discipline case — against an Egyptian
> sovereign ten-year yield of **23.0%** and a built cost of capital of 24.6% falling to
> 18.6%.

The market is discounting this company's cash flows at roughly **half the rate at which the
Egyptian government borrows**. That is not a defensible cost of capital for a leveraged
petrochemical producer, so the reverse read does *not* vindicate the price — it says the
two views cannot be reconciled by any plausible discount rate, and the disagreement must
therefore live in the cash flows or the balance sheet rather than in the rate.

**WHAT THIS REVIEW COULD NOT CLOSE, STATED RATHER THAN PAPERED OVER.** After both
corrections the cash-flow lens remains 88% below the market and 78% below its own disclosed
book floor. Candidate explanations that this review examined and could not settle from the
committed record:

- the nameplate capacity and bank-approved cost of the ANNA programme are **derived**, not
  disclosed as a matched pair, and the whole binary judgement turns on them;
- investment property and the OCI portfolio enter the bridge at carrying value, and a
  market value for either would move the equity materially on so thin a residual;
- the FX cost-of-debt disclosure at heading 4 is carried as a warning rather than resolved.

None of these is corrected here. Inventing a correction to close an 88% gap is precisely
what [R-GAP-01] prohibits — the rule says audit the answer, not move it — and each of the
three is a sourcing job rather than a modelling choice. They are registered as this study's
outstanding work and named in the register below.

---

## Register

| item | state |
|---|---|
| answer | **TWO-SIDED**: carried through EGP 1.7854, stopped EGP 5.9001 |
| moved by this review | carried through **−1.0621 → +1.7854**; stopped **2.8182 → 5.9001** |
| spot | EGP 14.41, 3 September 2026, `engine/prices/SUPPLIED_03-09-2026.json` (was 13.98, struck 6 August) |
| gap | −87.6% / −59.1% |
| headings clean | 1, 3, 5, 6, 7 |
| headings with findings | 2 — a typed, unsourced dollar price path falling 17%, against a flat dollar input, out of line with the same house's treatment of the same class of input (corrected); 4 — the rating ERP basis published as central where [R-COC-01] names the CDS basis and both peer Egyptian studies use it (corrected); 8 — the residual gap is unexplained and is stated as such |
| outstanding, not corrected | the derived ANNA nameplate and cost pair; investment property and the OCI portfolio at carrying value; the FX cost-of-debt disclosure carried as a warning |
| removed | the retired weighted central of ~3.76 the delivered documents still published |

---

*AUDITED CENTRAL: 1.7854* — the carried-through branch.
*AUDITED CENTRAL: 5.9001* — the capital-discipline branch. A two-sided study has two
answers, and a review that audits one of them has audited half the study.
