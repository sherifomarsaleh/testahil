# TMGH — valuation gap review, 01-Sep-2026

**[R-GAP-01].** This study deliberately publishes **no central**: its four cases
are published side by side and, in its own words, "never averaged". A summary
figure is nonetheless exposed to the gate, because a study whose answer cannot
be read is treated as a failure and not as a skip. The figure is the **median of
the four published cases on the book-minority framing, EGP 39.33**, against a
last known price of **EGP 97.80** (close 23-Aug-2026) — **59.8% below**.

**Nothing turns on that choice.** Every one of the four published cases is below
the price, and the *highest* of them is 39.0% below:

| Case | EGP/sh | vs spot |
|---|---:|---:|
| rating ERP · recovery | 22.30 | −77.2% |
| CDS ERP · recovery | 25.62 | −73.8% |
| rating ERP · capacity | 53.05 | −45.8% |
| CDS ERP · capacity | 59.67 | −39.0% |

The rule fires on any reading. This is the largest gap in the campaign so far
and it gets the most scrutiny.

Internal record. Nothing here reaches the live site and nothing here retro-edits
a delivered number. Every figure below that is not read off a filing is computed
by `gap_review_calcs.py` in this directory, which imports the study's own model
and reproduces the published `rating|capacity` case to 1e-6 before it varies
anything; nothing below is typed.

---

## 1. LATEST FILINGS — every disclosed period actually read

**Checked live on 01-Sep-2026.** The company's investor-relations page was
fetched and every PDF link enumerated. The newest financial statements posted
are the **reviewed consolidated statements for the six months ended 30 June 2026**
(`TMG Cons. FS 30 June 2026 - English.pdf`), alongside the separate statements
for the same date and the `Earnings release report for the financial period ended
30 June 2026`. There is nothing later: the September quarter has not closed.

The study reads all three. Its input register carries the 30-Jun-2026 reviewed
interim statements as the source of every balance-sheet line, and the 12-Aug-2026
H1 release as the source of the order book, contracted sales, hotel and land-bank
figures. **This heading passes with no finding** — unlike PHDC, where the same
check found a filing on the archive that had not been opened.

## 2. BASE YEAR — foots to the filed periods

FY2025, a filed audited year, reconstructed line by line from the study's own
register and checked against each filed subtotal:

```
three segments net of their own cost                     20,855.4  vs filed gross profit    20,855.4   −0.0
gross + revaluation + other income − G&A − marketing
        + fx − donations − ECL                           23,749.3  vs filed operating       23,749.3   +0.0
− D&A + finance income − finance cost + associates       23,653.6  vs filed PBT             23,653.6   +0.0
− current tax − deferred tax                             18,202.0  vs filed net profit      18,202.0   −0.0
parent 14,383.9 + minority 3,818.1                     = 18,202.0  vs filed net profit      18,202.0   +0.0
balance sheet: assets 477,897.9 = liabilities 310,574.2 + equity 167,323.6                              −0.1
```

Every line foots. Nothing is annualised, scaled or solved: the base is a filed
full year, and the balance sheet the bridge stands on is the reviewed 30-Jun-2026
one. The 2024 comparatives were restated by the company inside the measurement
period for its hotel acquisition, and the study carries both the original and the
restated figures rather than substituting one.

## 3. MACRO COHERENCE — inflation, currency and price as one path

**This heading finds the first defect.** The terminal rate embeds Egyptian
inflation through rf* = 16.63%; at a 1–3% real sovereign rate that is a long-run
expectation of 13.6% to 15.6%. Against 14.63% (the mid), the model's nominal
growth rates are:

| Driver | Nominal | Real |
|---|---:|---:|
| hospitality revenue | +20.00% | +4.68% |
| other recurring revenue | +22.00% | +6.43% |
| terminal growth | +15.00% | +0.32% |
| deposit yield | +20.00% | +4.68% |
| **replenishment contracted sales** | **−15.00%** | **−25.85%** |

Five nominal rates and no stated inflation path binding them — the [L-048]
failure mode, which this project has now met on three consecutive Egyptian names.
Four of the five are defensible: recurring revenue growing a few points in real
terms, a terminal at roughly zero real.

The fifth is not. `SALES_FADE = 0.85` takes contracted sales from EGP 300bn to
about EGP 69bn by 2035 **in nominal pounds**, which is roughly **−26% a year in
real terms**, compounding to a real decline of about 92% over the window. The
code's stated reason — "replenishment sales converge on the delivery rate" — is a
real-quantity argument (a developer cannot sell faster than it builds for ever)
applied to a nominal series, so it silently prices in a currency collapse in the
unit price as well as a volume convergence.

It is stacked on a conservatism that was already taken: the EGP 300bn starting
level is itself below the H1-2026 annualised run rate of EGP 438bn, below FY2025's
EGP 382bn, and far below FY2024's EGP 504bn. Normalising down is a judgement the
study is entitled to make and states. Fading the normalised figure by a further
15% a year, nominal, is a second haircut on the same driver, and it is not
disclosed as a real-terms assumption anywhere in the document.

## 4. DISCOUNT RATE — operations discounted at the right rate, cash charged once

**Cash is charged exactly once, and this is the heading where that had to be
checked hardest**, because TMGH is heavily net cash: EGP 75,773.4mn of cash and
deposits against EGP 16,493.0mn of borrowings, **net cash EGP 59,280.4mn**, and
the 2026 projection earns EGP 15,154.7mn of finance income on it — more than half
of that year's pre-tax profit.

- Free cash flow is `ebit × (1 − t) + D&A − capex − (Δ properties under
  development − Δ customer advances)`. **Finance income is not in it.** It reaches
  the projected income statement and EPS and stops there.
- The bridge adds cash and deposits once, at face.
- The equity weight is 0.9222, below one. The AMOC pathology — net cash producing
  a negative debt weight, an equity weight above one, an operating rate above the
  cost of equity, and then the same cash added back at face — **cannot arise
  here**, and was checked rather than assumed.

The beta is tier 1 and conforming: own-stock weekly regression against EGX30 from
`raw_indices/EG/EGX30.csv`, β 1.4718, R² 0.326, SE 0.185, n 251, Dimson-adjusted,
Blume cross-check 1.3145, `usable` and `conforming`. Ke = 16.63% + 1.4718 × 13.94%
= **37.15%**, WACC **35.79%** on the rating ERP and 32.37% on CDS. rf* is
normalised by Egypt's own adjusted default spread, so country risk enters once.
Kd is marginal and above the sovereign.

**Every step is method-conforming, and the rate still does most of the work.**
The study says so itself in the delivered document. Holding everything else fixed:

| | EGP/sh | vs spot |
|---|---:|---:|
| WACC 35.79% (published) | 53.05 | −45.8% |
| WACC 30% | 65.64 | −32.9% |
| WACC 25% | 85.22 | −12.9% |
| WACC 20% | 135.07 | +38.1% |

This is not a defect — a conforming rate is a conforming rate, and lowering it to
meet the price would be the deference this rule explicitly forbids. It is
recorded because it is the honest answer to "what would have to be different".
See heading 8.

## 5. TERMINAL — growth coherent with the inflation inside the terminal rate

**No finding, and the construction is better than the class norm.** There is no
perpetuity on the development leg at all: the order book is finite, so it is
converted over 14 years as a level annuity rather than capitalised, on the
explicit reasoning that "capitalising a finite pipeline for ever is a free
number". A growing perpetuity is taken only on the hotels and the recurring
estate, at 15% nominal — about +0.3% real against the inflation inside the same
rate, which is coherent.

The result is that the terminal is **not** where this answer comes from:

```
explicit ten years                          88,580.4    90.7% of enterprise value
residual order book, 14-year annuity         1,119.4     1.1%
recurring-leg perpetuity                     7,967.6     8.2%
```

One consequence deserves stating plainly rather than leaving in the arithmetic:
the residual order book at the end of the window is EGP 1,366bn and it is valued
at EGP 1.1bn — about a tenth of one per cent of its face — purely because it is
discounted at 35.79% from year ten. That is arithmetically correct and
economically severe, and it is a second-order consequence of heading 4, not an
independent defect. Excess work in progress is credited at cost where it exists;
here it computes to zero.

## 6. BALANCE SHEET — the bridge stands on the latest disclosed balance sheet

**It does.** Every bridge line — cash, current and non-current deposits, loans,
credit facilities, leases, investment property, associates, FVOCI, minority
equity, total equity — is dated 2026-06-30 and sourced to the reviewed interim
statements. Assets foot to liabilities plus equity to 0.1.

**But the minority is measured on the wrong axis, and this is the second defect.**

The bridge removes the minority two ways, and *both are book-based*: at book
value (EGP 75,652.8mn) and at the minority's share of book equity (45.21%).
The company's own filed profit split says the minority earns far less than that:

| | Minority share |
|---|---:|
| of book equity, 30-Jun-2026 | **45.21%** |
| of FY2025 profit, as filed | **20.98%** |
| of FY2024 profit, as filed | 25.88% |
| of FY2024 profit, as restated | 29.32% |

The dual-framing rule was honoured on the *wrong axis*: the study computes the
minority two ways and both answer the same question — what is the minority's
share of *book*. Neither tests what it earns. On the FY2025 filed profit share
the capacity case moves from **53.05 to 70.93**, +34%.

Which is right is genuinely contested — a minority sitting in asset-heavy hotel
and land subsidiaries can be worth more than its current earnings contribution —
and that is precisely why it belongs in the published framing rather than in a
review. As it stands the study's "both ways" spans 49.18 to 53.05 while the real
question spans 49.18 to 70.93.

## 7. CLAIMS AGAINST THE RECORD — every superlative recomputed

The delivered document was scanned programmatically for superlative and absolute
claims. Each one that is a claim about the record was recomputed:

- **"has traded between 8.9 and 15.2 times earnings over the period"** —
  recomputes exactly from the study's own eight years with a disclosed
  attributable EPS: 8.93 (2022) to 15.22 (2017). ✓
- **"at the last close it is on 14.0 times its 2025 result"** — 97.80 ÷ 6.98 =
  14.01. ✓
- **"Egypt's largest listed developer"** — true on every disclosed measure the
  study carries: market capitalisation EGP 201.5bn, order book EGP 491.0bn,
  landbank about 20mn sqm, against the next largest covered Egyptian developer at
  EGP 43.5bn. ✓
- **"New contracted sales came back about 58% low, consistently, in every part of
  the record"** — from this company's own fundamental walk-forward, not an
  impression. **See heading 8: this is the finding the model then contradicts.**
- **"The discount rate does most of the work… The June 2026 edition of this study
  used 18%, which is below the Egyptian government's own ten-year borrowing cost
  of 23.00%"** — correct, and the right way round: the prior edition's rate was
  not defensible and this edition says so.

**No unverified claim about the company's record was found.** The document's
strongest statements are about its own method and each resolves to a computed
figure.

## 8. MULTIPLE CROSS-CHECK — what the fair value implies

| | EGP/sh | mcap | group operating business | P/E FY25 | P/B | opco ÷ order book |
|---|---:|---:|---:|---:|---:|---:|
| lowest case | 22.30 | 45,943 | 33,788 | 3.19x | 0.50x | 6.9% |
| median (the exposed figure) | 39.33 | 81,052 | 68,897 | 5.63x | 0.88x | 14.0% |
| published capacity case | 53.05 | 109,308 | 97,153 | 7.60x | 1.19x | 19.8% |
| highest case | 59.67 | 122,960 | 110,805 | 8.55x | 1.34x | 22.6% |
| market, 23-Aug-2026 | 97.80 | 201,532 | 189,377 | 14.01x | 2.20x | 38.6% |

"Group operating business" is what each per-share figure implies the whole
group's development, hospitality and recurring businesses are worth, before any
minority split: market value plus the minority deducted at book, less the
non-operating assets the bridge adds at face (net cash 59,280.4 + investment
property 25,228.0 + associates 1,496.6 + FVOCI 1,802.8 = **87,807.8, which is
47.5% of the pre-minority equity**).

Two readings fall straight out.

**The low cases are hard to defend.** At EGP 22.30 the whole group's operating
business — a EGP 491bn contracted order book, roughly 20mn sqm of land, 3,500
operating hotel keys with 1,500 more under construction, and the recurring estate
— is worth EGP 33.8bn, under 7% of the order book alone, and the shares sit at
half of parent book value. That is not an implausible-but-bearish valuation; it
is close to saying the development business has no value, which is the argument
the study's own Expert 3 makes deliberately and labels "the floor".

**And the market's own reading is not obviously right either.** Solving this
model for the traded price gives an implied discount rate of **23.09%** on the
capacity reading and 19.43% on the recovery one, against Egypt's own ten-year
sovereign yield of **23.00%**. The price implies an equity return at or below the
government's borrowing cost — no risk premium at all for an Egyptian developer
with a beta of 1.47.

That is the honest shape of this disagreement: the study charges 35.79% and the
market appears to charge about 23%, and the truth is very unlikely to be at
either end.

---

## Verdict

**The answer does not stand as published, and the reason is not the discount rate.**

The cash-flow machinery survives the audit. The base year foots to the filed
statement on every subtotal, the balance sheet is the latest disclosed one, cash
is charged exactly once and the net-cash pathology was checked and excluded, the
beta is tier 1 and conforming, rf\* is normalised so country risk enters once, the
terminal refuses to capitalise a finite order book, and every superlative in the
document recomputes. No claim in the delivered study was found to be false.

Two defects were found, and unlike PHDC's they point the same way.

| # | Defect | Effect on the capacity case | Direction |
|---|---|---:|---|
| 1 | Contracted sales faded 15% a year **nominal** — about −26% real — stacked on an already-normalised starting level, and never disclosed as a real-terms assumption. | 53.05 → 76.51 | closes |
| 2 | The minority removed on its share of **book** in both published framings, while its filed share of **profit** is less than half that. The dual framing is on the wrong axis. | 53.05 → 70.93 | closes |
| **both together** | | **53.05 → 89.47** | **−8.5% vs spot** |

Correcting the two defects moves the capacity case from 45.8% below the price to
**8.5% below it** — inside the 10% threshold that fires this rule at all — with
no change to the discount rate, the terminal, the base year or the bridge.

**A third finding, which is not a defect but is evidence.** This study's own
fundamental walk-forward produced a corrected FY2026 central for every driver.
The model sits below all of them:

| FY2026 | model | walk-forward central | model vs |
|---|---:|---:|---:|
| contracted sales | 300,000 | 488,369 | −38.6% |
| development revenue | 49,337 | 58,890 | −16.2% |
| recurring revenue | 31,165 | 46,304 | −32.7% |
| total revenue | 80,502 | 105,194 | −23.5% |
| gross profit | 25,463 | 36,051 | −29.4% |

And the driver the model cuts hardest is the one the walk-forward specifically
found the method already forecasts **58% low, consistently, in every part of the
record**. The study measured its own bias on contracted sales, wrote the finding
into the delivered document, and then built the forecast in the same direction as
the bias. **That is [L-048] on this project's own record rather than on a
company's** — a lesson produced by a run and not applied to the study beside it,
which is precisely the failure [R-GAP-01] was adopted after.

The 39% to 77% discount does not survive the audit intact. A corrected TMGH sits
around the high eighties against a price of 97.80, and the residual disagreement
is then a legitimate one about the discount rate, where the study charges 35.79%
and the price implies about 23%.

## What this obliges

TMGH must be re-issued before it is published in the campaign's combined release.
This is not a documentation fix. Per the standing rule the corrections fold back
into the build scripts, not into the delivered file, and no delivered number is
retro-edited here.

1. `model.SALES_FADE` — restate the convergence of contracted sales on delivery
   capacity as a **real** assumption on a stated inflation path, so the nominal
   series carries the price level. Publish the resulting sales path in the
   document, since it is now the study's second-largest lever.
2. `valuation.bridge()` — add the minority measured on its **filed share of
   profit** as a third framing, and put the three side by side. The dual-framing
   rule is satisfied by framings that answer different questions, not by two
   readings of the same one.
3. `docx_tmgh.py` — state the model's FY2026 drivers against the study's own
   walk-forward centrals, and say why the model sits below every one of them, or
   move it.
4. Re-run the [R-GAP-01] gate afterwards. If the corrected central lands within
   10% of the price the rule stops firing on its own; if it does not, this review
   is superseded by a dated successor, not amended.

## Evidence in this directory

- `gap_review_calcs.py` → `gap_review_calcs.json` — every computed figure above.
  It imports the study's own `model` and `valuation` modules and asserts it
  reproduces the published `rating|capacity` case before varying anything.

---

## Addendum, 02-Sep-2026 — the two corrections applied (interim class-A edition)

Both corrections this review computed were applied in the study's own code on 02-Sep-2026, under the standing rule that a computed correction is applied or blocks: contracted sales restated flat in real terms (`model.SALES_FADE` 0.85 → 1.15, the review's own figure), and the minority deducted at its share of **value**, proxied by the filed FY2025 profit share (20.98%), with book and proportional printed beside it as the more punitive reads (protocol lines 383–387). No rate, terminal, driver or bridge item other than these two moved. Reproduced by `build_numbers.py` from `valuation.py`:

| Case | 01-Sep (book minority) | 02-Sep (value-share minority, flat-real sales) | vs 97.80 |
|---|---:|---:|---:|
| rating ERP · capacity | 53.05 | **89.47** | −8.5% |
| CDS ERP · capacity | 59.67 | **98.17** | +0.4% |
| rating ERP · recovery | 22.30 | 47.10 | −51.8% |
| CDS ERP · recovery | 25.62 | 50.36 | −48.5% |
| median (the exposed figure) | 39.33 | 69.92 | −28.5% |

The capacity reading now sits inside the gate on both ERP bases, exactly as this review predicted (89.47). The recovery reading remains far below the price for the reason heading 4 named and this edition does not touch: every year of a ten-year window, a fourteen-year residual annuity and the perpetuity are discounted at a flat 35.79%, in breach of the protocol's own sliding-schedule rule. That is the cost-of-capital workstream (WS1 of the reassessment plan), a class-A item in its own right, and it is applied when the module lands — not here, because the module does not yet exist and a hand-made glide would be a second convention where the plan calls for one. The exposed median still breaches the gate at −28.5%; this addendum is the review of that breach: the residual is one named lever with a written rule behind it.

The delivered document and workbook are rebuilt on these numbers with the minority basis stated as adopted; the reverse-DCF and the two-sided review of a re-issue that lands above the price (the CDS capacity case at +0.4% does not) follow when WS7 lands.
