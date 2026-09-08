# DU — gap review, 8 September 2026

**AUDITED CENTRAL: 15.5438** — the cash-flow lens, AED per share.
**AUDITED GAP: +36.6%** against the latest known price, AED 11.38 (7 September 2026, the last
session in this name's own library, `engine/raw_ohlc/AE/DU.csv`), which is also the price this
edition is struck at and the close the 07-Sep-2026 roll-forward struck this name's cone on.

This supersedes `GAP_REVIEW_04-09-2026.md`, which audited a central of 16.5778 and a gap of
+45.9%. Both halves moved: the answer fell 6.3% on the beta re-derivation and the price it is
measured against is a different, later and correctly dated one.

This fires the ABOVE-price half of the audit trigger. That half carries **no publication
block** — the block is one-sided below the price, because errors in a discounted cash flow are
not symmetric and a large discount is the high-prior-of-defect region. So nothing holds this
study on the gap, no authorisation is owed and none is asked for, and this review is the only
instrument standing here.

## What moved since the last review, and why

Written as a response to an outside forensic audit dated 8 September 2026 and to this desk's
own audit of the same documents. The full 53-row ledger is `CRITIQUE_RESPONSE_08-09-2026.md`.
Three levers moved the answer; every other correction moved a word, a label or a table.

| Lever | Rule it serves | Before | After | Move |
|---|---|---|---|---|
| Beta re-derived through the sanctioned house routine | SIGCM clause 6 / beta provenance | 16.5778 | 15.5321 | −6.31% |
| The AED 1.8bn combined fiscal floor modelled rather than quoted | completeness sweep | 15.5321 | 15.5321 | 0.00% |
| Re-struck on the latest known price and its own anchor date | the stale-price rule | 15.5321 | 15.5438 | +0.08% |

**The beta is the whole of it, and it moves the answer TOWARD the price.** The study published
0.488 from `beta_reg.py`, a study-local regression that this house forbids in the same words in
two places. Run through `beta_regression.own_stock_beta('DU','AE','DFM')` — which resolves the
regressor itself from `raw_indices/`, runs the data-quality gate on both series, matches the
weekly grid to the exchange's own trading week and Dimson-corrects for thin trading — the answer
is **0.5569** (R² 0.141, SE 0.149, n 249, CI90 0.31–0.80). The local script read a copy of the
index held inside this study directory, sampled its own weekly grid off calendar week numbers,
and applied no thin-trading correction.

---

## LATEST FILINGS

Every disclosed period has been read. The register was re-walked against du's own
investor-relations publications index rather than trusted.

| Document | Date | Read |
|---|---|---|
| Audited consolidated financial statements, year ended 31 Dec 2025 | 9 Feb 2026 | yes — full statements and notes 3.2, 6, 7, 8, 26, 31 |
| Reviewed condensed interim statements, six months to 30 Jun 2026 | 22 Jul 2026 | yes — including the statement of financial position, read by OCR because that page carries no text layer |
| Q2-2026 earnings release and analyst deck | 22 Jul 2026 | yes — subscribers, ARPU, capex intensity, revised guidance, interim dividend |
| Audited consolidated financial statements, FY2023 (carrying FY2022) | 13 Feb 2024 | yes — income statement and note 26 |
| du's own disclosure of the 2027-2029 federal royalty extension | 24 Jul 2026 | yes — and the AED 1.8bn floor it retains is now MODELLED, not merely quoted |
| TDRA licence renewal, twenty years effective 9 Aug 2026 | announced 12 Aug 2026 | yes — and the two stale catalysts built on its absence are rewritten |

The most recent filing of any kind is the 22 July 2026 interim set; Q3-2026 is not due. The
FY2026 build chains off the reviewed H1-2026 actuals rather than off FY2025.

One input was added by this review. The FY2024 federal royalty **as originally presented**
(1,675.9 against the 1,571.6 re-presented comparative the model carries) is now registered, so
the source-discrepancy note's 44.7% effective rate is computed rather than typed.

**Nothing found that changes the answer.**

## BASE YEAR

The base year foots to the audited statements line by line, to the thousand:

| | Audited FY2025 (AED 000) | This study (AED mn) |
|---|---|---|
| Total revenue | 15,905,421 | 15,905.4 |
| Operating profit before D&A | 7,338,388 | 7,338.4 |
| Depreciation and amortisation | 2,167,933 | 2,167.9 |
| Net profit for the year | 2,905,085 | 2,905.1 |

Nothing is annualised, scaled or solved. FY2026E is not a scaled full year: it is the reviewed
H1-2026 actual plus a unit-built second half, and the mobile unit build reproduces the audited
FY2025 segment to 0.04% (average base 9,310k × AED 63.3 × 12 = 7,072 against a disclosed 7,075).

**Nothing found.**

## MACRO COHERENCE

One path, and the study carries no inflation number of its own. Terminal inflation of 2.00%
comes from `engine/macro_paths/AE.json` and is now **registered as a Country-layer input** with
its value, date and source — it appeared in no layer of the register before this edition, which
an outside audit was right to call a breach of the register's own completeness contract. The
build asserts at run time that the registered figure IS the one the house path supplies.

Terminal growth is stored as a REAL rate (0.00%) and derives to nominal on that path. The bear
and bull scenario growths are now stored the same way (−0.50% and +1.00% real) — the bear
previously carried the BASE nominal rate, so the largest single lever in the study moved for the
bull and not for the bear.

The dirham is hard-pegged; there is no currency leg, no translation anywhere in the model, and
the cost of capital is nominal against nominal cash flows throughout.

**Nothing found.**

## DISCOUNT RATE

Country risk enters exactly once: 4 basis points of market-observed sovereign spread stripped
from the risk-free rate, and a 6 basis-point country premium scaled off that same 4bp added back
inside the equity premium. The stripped basis and the added-back basis match. The ratings basis
(42bp out, 64bp in) is published beside it and never averaged.

Cash is charged exactly once. The discount-rate weights are market-value equity against the
gross lease book — not net debt — so the equity weight does not lever above one on a net-cash
issuer, and the cash is added at face in the bridge and nowhere else.

The rate is not held flat across the window and the perpetuity: 6.686% gliding to 6.455%, on
the AED risk-free path's own cumulative progress rather than on a second free parameter.

**One thing found and fixed, and it is the largest correction in this edition.** The beta was
hand-rolled. See above. Two further defects in the same family were found and closed: the
regressor was read from a copy of the index inside this study directory rather than from the
registered `raw_indices/AE/FADGI.csv`, and the interim-index disclosure — which ends "Quote this
note wherever the beta is quoted, and never call such a beta conforming" — was quoted nowhere.
It is now quoted in the body, in the register and in the beta record, and the record carries
`conforming: false`.

## TERMINAL

Built through the sanctioned module on a life derived from the depreciation notes' own columns:
property 18.55 years, intangibles 14.59, right-of-use 10.24, blended **16.70**. The route
validates against a directly disclosed figure — note 7 states an average lease term of 10.1
years against the 10.24 the identity derives, 1.4% apart.

The terminal adds back the FULL depreciation charge, right-of-use included, and escalates all of
it into a replacement charge, because a lease renews in perpetuity like any other asset and the
one-off liability deduction in the bridge cannot cover renewals for ever. **The study said the
reverse of this in three places and the workbook cell label said it in a fourth.** The
arithmetic never changed; the account of it was inverted, and it is corrected here.

Terminal value is 80.0% of enterprise value and the study says so. The reinvestment identity is
explicitly rejected: its implied replacement cycle is 1/g — fifty years at 2.0% — which is a
fact about the dirham's peg rather than about a mobile network.

**One thing found and fixed.** Every discount-rate sensitivity in the study — Figure 3, both 5×5
grids, Table 11's beta row, the alternatives priced in Table 10, the figures quoted in sections
1.7 and 1.8, and Framing B's post-2029 tail — was still running the RETIRED reinvestment-identity
terminal while the headline ran the sanctioned one. Each returned a number AED 0.664 above the
headline it claimed to reproduce. The coincidence that the wedge was almost exactly the AED 0.66
of netted dividends is what let it survive an outside forensic audit as a mis-diagnosis. All of
them now run the sanctioned terminal, and `compute.py` asserts at build time that all ten grids
return the headline exactly at their base parameter — the check the study's own caption had been
claiming since its first edition while nothing tested it.

## BALANCE SHEET

The bridge stands on the 31 December 2025 audited sheet, which is the study's valuation date,
and rolls to the anchor at the cost of equity net of the AED 0.66 of dividends gone ex in
between. A reviewed 30 June 2026 balance sheet exists and was read.

**This is not the stale-sheet defect, and the receipt is a computation rather than an argument.**
Sheet, valuation date and roll agree, and the model's own cash walk reproduces the disclosed June
position: cash and term deposits ran 2,249.7 at 31 December against 307.2 at 30 June, a movement
of −1,942.6, of which −1,813.2 is the final FY2025 dividend the roll already accounts for. The
remainder, −129.4 over the half, sits against the model's own FY2026E full-year movement of
−226.6 — a difference of **AED 16.1mn on the half, AED 0.0036 per share**. Book equity fell
181.2 while 1,813.2 of dividends were paid, so equity before distributions rose about 35%
annualised against a 6.83% roll: the roll is conservative against the actual outturn. Moving the
bridge onto the June sheet while still deducting those dividends would charge the same
distribution twice, which is the bridge rule's own trap in mirror image.

The study carries no machine-readable bridge record and remains on that ratchet. Re-cutting the
explicit window to a 30 June valuation date is a rebuild rather than a patch and is owed at the
next re-issue.

**Nothing found.**

## CLAIMS AGAINST THE RECORD

Every absolute claim in the delivered documents is recomputed rather than typed, and the
recomputation is enforced: `prose_check.py` reconciles 511 figures across both delivered
documents against the model, with none unmatched.

- "the highest EBITDA margin of any period from FY2022 to the reviewed half-year ended 30 June
  2026" — recomputed over the window it names: 40.32 / 42.53 / 44.21 / 46.14 / 47.10 / **49.18**.
  True, over a stated window, with FY2022 read out of the FY2023 statements so the superlative
  has a record to be superlative over.
- "the four full years rising in every one of them" — 40.32 → 42.53 → 44.21 → 46.14. True.
- "total operating expenses before depreciation RISE 0.7% in FY2026E" — computed, not typed.
- "cash declines in every year of the forecast with no rebuild inside the window" — **FALSE and
  corrected.** The printed row is 2,023 → 1,899 → 1,856 → 1,979 → 2,158: three years of decline,
  two of rebuild.
- "every 0.10 on beta is worth roughly AED 1.34" — **FALSE PRECISION and corrected.** The
  relation is convex; the slope now prints segment by segment.
- "the panel median sits below because two of its three members set the terminal on a market
  multiple" — **FALSE and corrected.** One of three does.
- "no peer median is claimed" against three places that claimed one, and a workbook label that
  claimed a fourth — **corrected in all four.**
- The AED 12.76 (now 11.94) "disclosed floor" — **corrected.** The disclosed floor is book value
  per share, AED 2.24. A justified price-to-book on a sustainable-return construction is a
  valuation, and this one sits above the traded price.

## MULTIPLE CROSS-CHECK

What the fair value implies, against what du trades at and what its peers trade at:

| | This study's central | du today | Mobily (issuer filings) |
|---|---|---|---|
| Price / FY2026E earnings | **21.9×** | 16.0× | 12.9× |
| EV / FY2026E EBITDA | **8.8×** | 6.5× | — |
| Implied terminal exit multiple on FY2030E EBITDA | **8.1×** | 7.0× trailing | — |

**This is where the disagreement lives and the study says so.** The central asks the market to
pay 21.9× forward earnings for a single-market operator whose closest structural analogue trades
at 12.9×, and its terminal asks for a +16% re-rating on du's own current EBITDA multiple. The
study does not dissolve that: it publishes the no-re-rating case at AED 13.78 beside the central
at 15.54 and never averages them, and it publishes the two market-anchored lenses at AED 8.93
and 8.94 — 21% BELOW the traded price — rather than quietly weighting them away.

**The reverse read is the honest summary and it is now published in the study itself.** Holding
every other driver at its published value, the traded price implies an equity beta of **0.96** — a
required return of 8.54% — against the 0.5569 the regression measures. That is not an absurd
number for a single-market, single-licence operator, it sits just outside the regression's own
90% interval (top 0.80), and it means the disagreement is about the price of risk rather than
about the cash flows. A reader who thinks a licensed duopoly should carry market risk has a
coherent position that this study does not hold.

**The sign test says the study is not leaning.** Seven judgements are worth more than 5% of the
central, six of them material; four resolve toward a higher value and two toward a lower one, a
two-sided binomial p = 0.69. This study does not display the single-direction lean that survives
an audit of its steps.

---

## VERDICT

The gap is +36.6% and it is real. Nine percentage points of the previous review's +45.9% were
this desk's own defect — a beta produced by a script this house forbids — and that is now
corrected in the direction of the price, which is the only direction that shows the discipline is
not fitting. What remains is a disagreement about the required return, stated in the market's own
units, priced both ways, and left to the reader.

**No publication is requested and none is authorised by this review.** The study is re-issued to
the principal, not published.
