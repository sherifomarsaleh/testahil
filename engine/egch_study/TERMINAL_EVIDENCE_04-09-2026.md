# EGCH — the fixed-asset evidence a terminal rebuild needs, and what it found

**Status: gathered 4 September 2026 and NOT yet spent.** The terminal is still on the
retired reinvestment identity. What this file records is the primary-source work, the
arithmetic that validates it, and a defect it exposed in the shared construction — which is
the reason the rebuild has not shipped, and the reason is a *missing measurement in a shared
module*, not an assessment of how hard the change looks.

## 1. The statements had to be read off the pixels, and the extraction foots four ways

The FY2024/25 audited statements (Central Auditing Organization, report dated 23 September
2025) carry a **48-character text layer across 48 pages**. Every figure below was read from
the rendered image of note 6, *الأصول الثابتة (بالصافي)*.

**Arithmetic is the arbiter, not the extractor's confidence:**

| check | reconstructed | printed |
|---|---:|---:|
| cost roll-forward: opening + additions − disposals | 17,022,493,238 | 17,022,493,238 |
| accumulated roll-forward: opening + charge − disposals | 3,435,299,807 | 3,435,299,807 |
| cost less accumulated | 13,587,193,431 | net book value 13,587,193,431 |
| land, against note 4-6's own total | 1,662,949 | 1,662,949 |

And **against figures this study had already committed from an earlier reading**: the year's
charge 771,213k against a registered 771,213k; net fixed assets 13,587,193k against
13,587,193k; assets fully depreciated and still in production 220,496k against 220,496k.
Three independent agreements on a scanned Arabic filing.

## 2. The disclosed rates, in more detail than the study currently carries

Note 5-2 gives depreciation **rates**, and a disclosed rate is a disclosed life:

| class | rate | life |
|---|---:|---:|
| Machinery — urea / ammonia plant | 3.95% | 25.3 y |
| Machinery — factories | 9.5% | 10.5 y |
| Machinery — workshops | 6.5% | 15.4 y |
| Buildings — factories, and the urea / ammonia plant | 6% | 16.7 y |
| Buildings — residential city 2%, water and sewage pipes 5% | 2–5% | 20–50 y |
| Intangibles — urea / ammonia plant | 4.75% | 21.1 y |
| Transport 12.5–20%, tools 7.5%, furniture 10%, computers 10% | | 5–13 y |

The study registers three of these. The others are recorded here so the next pass does not
have to re-read a scanned filing to find them.

## 3. What the base actually is, and it is the opposite of what the construction assumes

| | |
|---|---:|
| depreciable gross cost (cost less land) | 17,020,830,289 |
| the year's own charge | 771,213,489 |
| implied life, gross over charge | **22.07 y** |
| accumulated depreciation | 3,435,299,807 |
| **average age, accumulated over charge** | **4.45 y** |
| half the life — what the shared construction assumes the age to be | 11.04 y |
| fully depreciated and still in production | 220,495,594, **1.3% of the base** |

**This base is young, and the 1.3% figure is why that reading is safe.** Where a large share
of a base sits fully depreciated and still in service, the gross-over-charge identity
returns an *economic* cycle longer than the accounting life. Here almost nothing is past its
accounting life, so 22.07 years is close to a true weighted accounting life and the 4.45-year
age is what it appears to be: a plant rebuilt recently, with a project still under
construction. The FY2024 comparative column says the same thing — life 26.14 years, age 4.14.

## 4. The defect this exposes, and it is not in this study

`engine/terminal_value.py`'s `book_dna_escalated` basis charges maintenance as the book
depreciation escalated over **half the useful life**. That is the right identity *under
uniform vintages*: book depreciation is struck on historical cost, replacement costs
`(1+π)^age` more, and on a base in steady state the average asset is half its life old.

**On a base that is not in steady state the proxy is simply wrong, and the error scales with
inflation.** At Egypt's 7% terminal:

| escalator | |
|---|---:|
| on half the life, `1.07^11.04` | 2.110 |
| on the **measured** age, `1.07^4.45` | 1.352 |
| the construction over-charges by | **+56.1%** |

Run on EGCH's own committed terminal-year figures at the disclosed 25.3-year machinery life,
the sanctioned construction charges maintenance of EGP 5,506mn against a terminal profit
after tax of EGP 3,815mn — 144% of it — and drives the equity **negative**. That is not a
finding about this company. A company that has just spent EGP 20bn on a new plant is being
charged as though that plant were eleven years old and needed replacing at 2.1 times its
cost.

**The direction is not universal and that is the whole point.** On the two names rebuilt
before this one the same proxy erred in *opposite* directions — one base younger than
uniform, one older — and both were in 2% markets where the error is small. Egypt is where it
compounds.

## 5. What the sanctioned terminal gives on the measured age — priced, and buildable

With the age read rather than assumed, the construction builds cleanly and the answer is
large:

| | |
|---|---:|
| terminal-year profit after tax | 3,815 |
| plus book depreciation and amortisation | 2,338 |
| less capital maintenance, at the measured 4.45-year age | (3,160) |
| less growth capital — the terminal real growth is **zero**, so nothing | — |
| less inflation on working capital | (229) |
| **terminal free cash flow** | **2,764** |
| implied payout of terminal profit | 72.4% |

Terminal **25,524** against the retired identity's 20,121, **+26.8%**; per share **3.2905**
against 2.3109, **+42.4%**. The gap against the traded 14.41 narrows from about −84% to
**−77.2%** — still far enough below the price that this study stays held, which is the
right outcome: a correction is applied because it is the better measurement, not because of
where it leaves the answer.

**On the half-life proxy the same terminal REFUSES**, charging 5,506 of maintenance against
3,815 of profit and driving the equity negative. The difference between a refusal and a
+42% correction is one number, and it was sitting in the accounts.

## 6. Why the rebuild has not shipped in this pass

Fixing this inside the study would mean either bypassing the sanctioned construction or
feeding it a life it does not have, and a study quietly using a different escalator would be
outside the shared construction while appearing to be inside it. **The honest fix is to
re-point the shared module**: take the measured age where the accounts give it —
accumulated depreciation over the year's own charge, an identity, labelled derived — and
keep half the life as a stated fallback where they do not. That is a re-pointing rather than
a widening: a measurement replaces an assumption, and no parameter is chosen.

It moves five already-rebuilt names, so it needs its own pass: the amendment, a negative
control, the five re-runs, and both governing documents. It is not squeezed in beside a
study rebuild.

**Status, stated exactly.** The measurement is obtained and footed, the shared construction
has been re-pointed to take it, and the result is priced above. What remains is a BUILD —
routing this study's own `terminal()` through the module, the workbook, the documents, the
gap review and the ledger — on a study whose filings are scanned Arabic and whose central is
two-sided across four branches. It is the next pass, and it is a build rather than research.

**And the workbook was MEASURED rather than assessed from its shape**, which is the mistake
made once already this week and is not worth making twice. Its terminal block is a fixed row
map — `BLK` at rows 21 to 28 of the DCF sheet, two columns — and a fixed row map is exactly
what looked like a blocker on another name and was not. The arithmetic:

| | rows |
|---|---:|
| the sanctioned waterfall needs: book D&A, maintenance, inflation on working capital | +3 |
| row 26 is freed — it holds the retired reinvestment rate, which goes | −1 |
| **net rows needed** | **2** |
| free rows between the block's last row (28) and the next content (33) | **4** |

Growth capital is not a row here because this terminal's real growth is **zero**, so the
charge is zero by construction rather than by omission. **Nothing below has to move and no
address shifts.** The rest of the surface is small too: `reinv_rate`, `roc_terminal` and
`fcff_T` appear in only two files, `compute.py` and `build_xlsx.py`, and in the workbook only
at three lines.

**What is NOT the reason:** this was a missing measurement, now obtained, in a shared
module. It is not an obstacle assessed from the shape of the change — the terminal was
actually built, run and priced, and the number it produced is what sent the enquiry back to
the module.

**And the size is the reason it gets its own pass rather than being appended to another.** A
+42% move on the most-disagreeing study in the book is exactly the shape of change this
programme exists to be careful about: it is recorded here with its arithmetic so the next
pass starts from evidence rather than from memory.
