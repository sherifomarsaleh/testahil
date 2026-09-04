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

**AND IT BUILDS ON ALL FOUR OF THIS STUDY'S CASES, not just the one quoted.** That was worth
testing before committing to the rebuild, because a case with a thinner profit and the same
asset base is where a maintenance charge refuses:

| case | terminal profit | book D&A | maintenance | terminal cash flow | payout | terminal | vs retired |
|---|---:|---:|---:|---:|---:|---:|---:|
| base | 3,815 | 2,338 | 3,160 | 2,764 | 72.4% | 25,524 | +26.8% |
| bull | 3,794 | 2,338 | 3,160 | 2,745 | 72.3% | 25,342 | +26.7% |
| bear | 2,829 | 1,535 | 2,074 | 2,061 | 72.8% | 19,027 | +27.5% |
| halt | 4,175 | 1,019 | 1,377 | 3,588 | 85.9% | 33,129 | +50.5% |

No refusals; every payout sits inside [0, 1]. **The halt case gains most and that is
coherent rather than odd:** a board that does not build the complex carries no project
depreciation, so its profit is higher and its asset base smaller — and the sanctioned
construction charges maintenance on the base rather than, as the retired one did, a
reinvestment rate scaled to profit. A company with less plant to keep intact should be
charged less for keeping it intact.

## 6. The study already says this, in its own delivered words

This is not a defect found from outside. The delivered document's own cost-of-capital
section carries it:

> *"The terminal reinvestment rate is now the largest unsourced input left in the model. It
> is set by terminal growth over an assumed 18% return on invested capital, which charges
> 38.9% of terminal operating profit after tax back into the business every year for ever —
> **on a plant that has just been rebuilt and needs no further building.** … The conservative
> reading is kept and the alternative is priced."*

The diagnosis is exact and it is the study's own. What follows it is the move this
programme keeps finding: **priced, named, and kept because it looked conservative.** It is
the same shape as EMPOWER's terminal declared blocked, RIYADHCABLE's review ruling out its
own correction, and EMPOWER's measured age withdrawn — and it is the largest single item in
the most-disagreeing study in the book.

The paragraph will need rewriting in the rebuild, and it is worth quoting here because it
answers the obvious objection in advance: nobody has to be persuaded that this charge is
wrong on this company. It was written down as wrong, and then kept.

**AND THE STUDY'S OWN PRICE FOR THE CORRECTION LANDS WHERE THE SANCTIONED CONSTRUCTION
DOES**, which is the strongest corroboration available and was not looked for. Its
`alternatives.json` prices the reinvestment framing it declined — an 18% terminal return
raised to the 30% "a newly completed line earns while it is still filling":

| | per share |
|---|---:|
| published | 2.3109 |
| the study's own priced alternative, on a raised return on capital | **3.2396** |
| the sanctioned construction, on a measured-age maintenance charge | **3.2905** |
| the two agree to | **1.6%** |

**Two entirely different routes to the same place.** One raises an assumed return on
capital inside the retired identity; the other throws the identity away and charges what
keeping the plant intact costs on the age the accounts measure. They were built
independently, months apart, and they differ by a percent and a half.

This is worth contrasting with the two other cases in this programme where a study priced a
correction it declined: RIYADHCABLE's review predicted −16.2% and the build gave +1.97%, and
DU's predicted +5.6% against a built −2.6% — both wrong in sign. **Here the study's estimate
was right, and what it got wrong was the decision to keep the number anyway.**

## 7. What the rebuild will NOT fix, and the gap review will have to say so

**This study is TWO-SIDED and both branches move**, which matters because a two-sided answer
is held only if *every* branch sits more than ten per cent below the price:

| branch | published | corrected | move | gap now |
|---|---:|---:|---:|---:|
| capital programme carried through | 2.3109 | **3.2905** | +42.4% | −77.2% |
| capital programme stopped | 6.2591 | **8.2737** | +32.2% | −42.6% |

Both remain far below the traded 14.41, so **EGCH stays held either way** — the correction
does not change its publication status, and it was not made in the hope that it would.

Corrected, this study reads 3.2905 against a traded 14.41 — **still 77% below the price**,
so it stays held and its eight-heading review still has to explain a very large
disagreement. Two things about that are worth writing down before the rebuild, because they
change what the review should be looking at.

**The equity gap overstates the modelling gap, because the equity is a thin sliver.** Net
debt is EGP 10,032mn against an enterprise value of 11,085mn, so almost all of the
enterprise value is spoken for before equity gets any:

| | EGP mn |
|---|---:|
| study enterprise value | 11,085 |
| price-implied enterprise value | 38,659 |
| **the enterprise disagreement** | **3.5x** |
| the equity disagreement | 6.2x |

**So the honest statement of the disagreement is 3.5x on enterprise value, not 6.2x on
equity** — leverage does the rest, and it does it in both directions. It is also why the
terminal correction is worth +42% on equity for +26.8% on the terminal: the same gearing.

**And it means the terminal is not where the remaining gap can live.** After the correction
the enterprise value is 16,569mn against a price-implied 38,659mn. Closing that on the
terminal alone would need a terminal several times larger again, which no maintenance
assumption reaches. **Whatever else is wrong here — or whatever the market believes that
this model does not — it is in the operating build, the capital programme's returns, or the
price the market puts on the balance sheet, not in the terminal charge.** The review should
be pointed there rather than re-litigating the terminal it will just have corrected.

## 8. Why the rebuild has not shipped in this pass

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
