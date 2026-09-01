# PHDC — valuation gap review, 01-Sep-2026

**[R-GAP-01].** The delivered central of **EGP 10.94** sits **28.0% below** the
last known market price of **EGP 15.20** (close 23-Aug-2026). That is past the
10% trigger, so the study is not finished until this review has covered the
eight headings below.

Internal record. Nothing here reaches the live site, and nothing here retro-edits
a delivered number. Every figure that is not read straight off a filing is
computed by `gap_review_calcs.py` in this directory from the study's own
committed numbers and printed by it; nothing below is typed.

The trigger is evidential, not deferential. A 28% discount is a legitimate
conclusion and this project publishes ranges precisely because prices are
sometimes wrong. What the rule requires is that the answer be audited before
it ships, because the errors that produce a large discount are not symmetric:
a stale base year, an over-charged discount rate, a missed revenue line, a
real-terms terminal decline and an unread filing all push value down.

---

## Where the gap actually is — read this first

The discounted cash flow is **not** the source of the discount. It comes out at
**EGP 14.86**, 2.2% below the price. The gap is produced almost entirely by the
three lenses blended around it:

| Lens | Base, EGP/sh | Weight | Contribution to the −4.26 gap |
|---|---:|---:|---:|
| Discounted cash flow | 14.86 | 45% | −0.15 |
| Book value of equity | 6.56 | 15% | −1.30 |
| Earnings multiple on own history | 11.17 | 20% | −0.81 |
| **Normalised earnings power** | **5.17** | **20%** | **−2.01** |
| **Weighted central** | **10.94** | 100% | **−4.26** |

Forty-seven per cent of the gap comes from one lens carrying a fifth of the
weight. That is where this review spends its attention, and it is where it finds
the one defect of the kind [R-GAP-01] was written to catch.

---

## 1. LATEST FILINGS — every disclosed period actually read

**Checked live on 01-Sep-2026, not taken from the study.** The company's own
result centre (`ir.palmhillsdevelopments.com/en-us/financial/resultcenter`) was
fetched and parsed. The newest posting of any kind is **Q1 2026** — both the
consolidated financial statements and the earnings release. There is no
2Q/H1-2026 filing. The study's stated information set, ending at 1Q2026, is
current as at this review date.

Two corroborations fell out of the same check. Q4 2025 carries a financial
statement and **no** earnings release, which is exactly the gap the study
registered as `fy2025_results_release` — so FY2025 genuinely has audited
financials and no operating drivers, as the study says. And the FY2025
comparative column inside the 1Q2026 filing reproduces the study's FY2025
balance sheet line for line (cash 9,419,526,159; parent equity 17,431,419,763;
NCI 1,334,332,140; total assets 172,129,812,858), an independent confirmation
of the base balance sheet from a document the study did not use.

**Finding — one filing was on the archive and was not opened.** The 1Q2026
*earnings release* was swept; the 1Q2026 *reviewed financial statements*, on the
same page, were not. The study registered 1Q2026 revenue, gross profit, net
profit, backlog and new sales from the release, and no balance-sheet line from
the statements. This is the AMOC defect in miniature. It is quantified under
heading 6.

## 2. BASE YEAR — foots to the filed periods

FY2025, a filed full year. Nothing annualised, nothing scaled, nothing solved.

```
FY2023  revenue 17,462.1 − cogs 11,907.2 − cash discount  47.2 =  5,507.7  vs filed gross profit  5,507.6   +0.10
FY2024  revenue 27,167.3 − cogs 17,739.9 − cash discount  97.3 =  9,330.1  vs filed gross profit  9,330.1   −0.00
FY2025  revenue 36,169.3 − cogs 21,118.9 − cash discount 162.8 = 14,887.6  vs filed gross profit 14,887.6   +0.00
```

The 162.8 wedge between revenue less cost and gross profit is the **disclosed
cash-discount line**, not an unexplained difference — it was checked because a
1.1% miss on gross profit is exactly the shape a mis-keyed figure takes.
Balance sheet: assets 172,129.8 = liabilities 153,364.1 + equity 18,765.8, to
0.1. Below gross profit the residual to filed NPBT is 1,430.3, which is the
filed other-income and FX line, consumed by the model and not a plug.

One presentational inconsistency, no effect on any number: the registry's
`cogs_fy24` (17,837.2, taken from the FY2024 release) bundles the cash discount
that `historical_is` (17,739.9, taken from the statements) shows separately.
Both foot; the model uses the statements.

## 3. MACRO COHERENCE — inflation, currency and price as one path

Revenue is a single volume-and-price build off the delivery capacity, and both
legs escalate on **one** stated inflation path: `CPI_TRAILING3 = 25.2%`, Egypt's
2023-25 mean from the World Bank WDI. Capacity grows on it, sales grow on it,
cost is recognised on the same completion clock as revenue, and gross margin is
the residual. There is no second inflation assumption anywhere in the forecast
and no currency path at all — the model is nominal EGP end to end, with no
foreign-currency revenue, cost or debt leg to reconcile. [L-048]'s failure mode
(three contradictory macro paths inside one model) does not occur here.

**One real tension, and it runs against the price, not toward it.** The explicit
years grow on a *trailing* 25.2%, while the discount rate is built on a
*forward* market yield (10-year EGP govvie at 23.00%). If the forward path is
the lower of the two — which is what a 23% ten-year yield against 25% trailing
inflation implies — then the explicit-year revenue is too high and the DCF lens
is, if anything, generous. Correcting it would widen the discount, not close it.

## 4. DISCOUNT RATE — operations discounted at the right rate, cash charged once

Beta is tier 1 and conforming: own-stock weekly regression against EGX30 read
from `raw_indices/EG/EGX30.csv`, β 1.049, R² 0.299, SE 0.182, n 251 over 4.85
years, Dimson-adjusted, Blume cross-check 1.033, `usable: true`, and
`conforming: true`. It clears the usability gate on all three legs. rf* is
normalised by Egypt's own adjusted default spread (23.00% − 6.37% = 16.63% on
the rating basis, 19.59% on CDS), so country risk enters once, through the ERP,
and both ERP bases are carried. Kd is marginal and sits above the sovereign
(23.00% + 250bp = 25.50%); the study flags that 250bp as its one unsourced
cost-of-capital input and refuses the 12.5% FY2025 accounting rate, correctly.

**Cash is charged exactly once.** Weights are market-value equity 43,470.8
against gross debt 33,552.7 — we 0.5644, wd 0.4356 — giving WACC 26.25%, which
reproduces the study's `wacc_rating` to four decimals. The equity weight is
below one, so the net-cash pathology that produced the AMOC defect (negative
debt weight → equity weight above one → an operating rate above the cost of
equity, with the cash then added back at face) cannot arise here: PHDC is net
*debt*, and cash is removed once, in the bridge.

The gross-debt convention is the textbook one and is the study's choice. It is
not free: on net-debt weights (we 0.6430, wd 0.3570) WACC is **27.15%, 90bp
higher**, and the DCF lens falls from 14.86 to **13.43**, −9.7%. Disclosed here
rather than adopted — but note the direction. The convention the study chose is
the *higher-value* one, so the discount is not an artefact of an over-charged
discount rate.

## 5. TERMINAL — growth coherent with the inflation inside the terminal rate

**This is the heading that finds the defect, and it is not in the DCF.**

The terminal rate embeds Egyptian inflation through rf* = 16.63%. At a 1-3% real
sovereign rate that is a long-run inflation expectation of **13.6% to 15.6%**.

The DCF's own terminal growth of **12.0%** therefore runs a real terminal decline
of −1.6% to −3.6% a year in perpetuity. That is a real assumption and it is a
conservative one, but it is *stated* and it is *sensitised*:

```
g = 10.00%  →  DCF 12.97 /sh   (terminal 59% of EV)
g = 12.00%  →  DCF 14.86 /sh   (terminal 63% of EV)   ← published
g = 13.63%  →  DCF 16.85 /sh   (terminal 66% of EV)   ← inflation at a 3% real rate
g = 14.63%  →  DCF 18.34 /sh   (terminal 68% of EV)   ← inflation at a 2% real rate
```

**The normalised-earnings-power lens does the same thing and does not disclose
it.** It capitalises normalised earnings of EGP 4,622.3mn at the *nominal* cost
of equity with **zero growth** — `E / ke` — for **EGP 5.17 a share**. In a
currency whose own discount rate embeds 14-15% inflation, zero nominal growth is
not conservatism, it is a company shrinking about 13% a year in real terms
forever. Standard earnings-power value assumes no *real* growth; it does not
assume nominal stasis under 15% inflation, and applying the low-inflation form
of the formula in a high-inflation currency is a specification error, not a
prudent choice.

Priced both ways:

| Normalised earnings power | EGP/sh | Weighted central | Gap vs spot |
|---|---:|---:|---:|
| `E / ke` — as published | 5.17 | 10.94 | −28.0% |
| `E / (ke − g)`, g = 12.0% (the study's own terminal growth) | 8.39 | 11.59 | −23.8% |
| `E / (ke − g)`, g = 9.5% (rf* less a 2% real rate) | 7.44 | 11.39 | −25.1% |

**This is a defect of the species [R-GAP-01] names** — "terminal growth against a
terminal discount rate embedding inflation, i.e. a perpetual real decline nothing
disclosed" — and it is the single largest contributor to the gap. It does not
close the gap; it accounts for about 0.65 of the 4.26.

## 6. BALANCE SHEET — the bridge stands on the latest disclosed balance sheet

**It does not.** The bridge stands on 31-Dec-2025 while a reviewed **31-Mar-2026**
balance sheet was posted to the company's own result centre on 20-May-2026 and
is the same document set the study drew its 1Q2026 income figures from.

That statement has been downloaded, read (the file is a scan with no text layer,
so the figures were OCR'd off the rendered pixels at 300dpi), and recorded in
`bs_1q2026.json` in this directory with full four-field provenance. Every
subtotal foots to the third decimal — non-current assets, current assets, total
assets, parent equity plus NCI, both liability subtotals, total liabilities, and
assets = liabilities + equity. One line whose OCR the scan breaks
(`joint_shares_lt`) is recovered from the statement's own subtotal and marked as
recovered rather than read. Arithmetic is the arbiter, not the extractor.

The debt stack read off the new statement on the same eight lines the study uses
reproduces the study's own gross debt at FY2025 exactly (33,552.7), which is the
check that the two periods are being compared like for like.

```
31 Dec 2025 (used)   gross debt 33,552.7   cash 9,419.5   net debt 24,133.2
31 Mar 2026 (filed)  gross debt 32,369.8   cash 9,125.1   net debt 23,244.7
net debt −888.5 · associates + investment property +215.1 · equity effect +1,103.6
```

| | DCF lens | Book lens | Weighted central | Gap vs spot |
|---|---:|---:|---:|---:|
| as delivered (31-Dec-2025) | 14.86 | 6.56 | **10.94** | −28.0% |
| on the latest disclosed balance sheet | 15.25 | 7.13 | **11.20** | −26.3% |

**+2.4% on the central.** Real, and it does not explain the gap.

**A second balance-sheet defect, running the other way.** The bridge deducts net
debt, associates and investment property, and deducts **no minority interest**,
while dividing by parent shares. NCI at book is EGP 1,334.3mn = **0.47 a share**,
which the DCF lens overstates by. The book-value lens has the mirror of the same
inconsistency, dividing *total* equity (18,765.8) by *parent* shares, where
parent-only equity gives 6.10 rather than 6.56. Correcting both would widen the
discount, not close it — which is why they are recorded here rather than used to
argue the answer up.

## 7. CLAIMS AGAINST THE RECORD — every superlative recomputed

The delivered document was scanned programmatically for superlative and
absolute claims (`best`, `worst`, `highest`, `lowest`, `record`, `never`,
`always`, `first time`, `unprecedented`, `ever`, `largest`, `only`). **No claim
about the company's own history is asserted anywhere in the study.** The
strongest statements it makes are about itself and about its own measurement,
and each resolves to a computed figure rather than a typed one:

- "the largest single uncertainty in this valuation" — the EGP 20,085mn
  balance-sheet working-capital rise against the EGP 3,146mn the cash-flow
  statement implies, a 16,939mn wedge; both figures are filed, the wedge is
  arithmetic, and it is registered as the `cash_flow_statement_detail` gap.
- "overstated net profit by about three times, consistently and in 97 per cent
  of tested cases" — from this company's own fundamental walk-forward, not an
  impression. **Note the direction: the method's own measured bias is to
  overstate profit, so a corrected model would sit lower, not higher.** The
  discount is not the residue of an optimistic model.
- "Over 57 resolved three-month forecasts … inside the 90 per cent band 91.2%
  of the time … about 1.47 times as wide" — generated by the band-record
  machinery under [R-CAL-02], not typed.
- "first resistance and first support are always the nearest to the close" — a
  definition, and the one `technicals.py` enforces.

Nothing here needed recomputing against the filings because nothing here is a
claim about the filings. That is the honest finding, and it is a pass.

## 8. MULTIPLE CROSS-CHECK — what the fair value implies

| | EGP/sh | mcap | EV | P/E FY25 | P/E FY26e | EV/EBITDA FY25 | P/B | mcap ÷ backlog |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| central | 10.94 | 31,291 | 50,780 | 7.42x | 8.82x | 5.10x | 1.80x | 11.9% |
| DCF lens base | 14.86 | 42,510 | 61,999 | 10.08x | 11.98x | 6.23x | 2.44x | 16.2% |
| market, 23-Aug-2026 | 15.20 | 43,471 | 62,960 | 10.31x | 12.25x | 6.33x | 2.49x | 16.5% |

FY25 EPS 1.4744 · FY26e EPS 1.2410 · FY25 EBITDA 9,952.3 · 1Q26 backlog 263,000.

Nothing here is absurd in either direction. The central puts the company on 7.4x
trailing earnings, 5.1x EV/EBITDA and 1.8x book, against a market price at
10.3x, 6.3x and 2.5x. For an Egyptian developer with 7.3 years of contracted
backlog at the current delivery rate, both sets are inside the range the sector
has traded. The multiple cross-check neither confirms nor refutes the discount;
it establishes that the discount is not arithmetic nonsense.

---

## Verdict

**The answer stands, and it is not clean.** The 28% discount is not produced by
any of the failure modes [R-GAP-01] was written to catch inside the cash-flow
model: the base year foots, the discount rate charges cash once and uses the
*higher*-value weighting convention, the macro path is single and consistent,
the beta is tier 1 and conforming, the multiples are sane, and the study makes
no unverified claim about the company's record. The discounted cash flow lands
within 2.2% of the market price.

Three defects were found, and they do not point the same way.

| # | Defect | Effect on the central | Direction |
|---|---|---:|---|
| 1 | Normalised earnings power capitalised at a *nominal* rate with **zero nominal growth**, in a 15%-inflation currency — a perpetual real decline, undisclosed. The largest single contributor to the gap. | +0.65 | closes |
| 2 | The bridge stands on 31-Dec-2025 while a reviewed 31-Mar-2026 balance sheet was on the company's own archive, unopened. | +0.26 | closes |
| 3 | No minority interest deducted in the bridge (0.47/sh), and the book lens divides total equity by parent shares. | −0.55 approx. | widens |

Net of all three the central moves from 10.94 to roughly **11.2 to 11.4**, a gap
of −25% to −27% rather than −28%. **The discount survives the audit.** What
produces it is the lens blend, not the model: three of four lenses value this
company on its *reported accounting earnings and book equity*, and for a
developer whose value sits in an undelivered EGP 263bn backlog carried at
historical cost in a currency that has lost most of its value since 2022, those
lenses measure a floor rather than a value. That is a defensible construction
and it is stated in the study; it is also the whole of the answer to "why is the
fair value 28% below the price".

## What this obliges

Defects 1 and 3 are specification errors in `valuation_v2.lenses()`, not input
errors, and defect 2 is an unregistered filing. All three fold back into the
build scripts per the standing rule, not into the delivered file — no delivered
number is retro-edited here. They are carried as the first tasks of PHDC's next
edition, which must run before this study is published in the campaign's
combined release:

1. `valuation_v2.lenses()` — capitalise normalised earnings at `ke − g` on the
   same terminal growth the DCF uses, or state in the document why nominal
   stasis is the intended assumption.
2. `build_numbers.py` — register `bs_1q2026.json` and move the bridge, the book
   lens and the debt schedule onto the 31-Mar-2026 balance sheet.
3. `valuation_v2.bridge()` / `lenses()` — deduct NCI, and put the book lens on
   parent equity, so both sit on the same numerator as the share count.

## Evidence in this directory

- `gap_review_calcs.py` → `gap_review_calcs.json` — every computed figure above.
- `bs_1q2026.json` — the 31-Mar-2026 balance sheet, four fields per line, footed.
