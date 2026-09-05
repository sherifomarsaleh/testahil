# EGCH — the fixed-asset evidence a terminal rebuild needs, and what it found

**Status: SPENT 5 September 2026. The terminal is rebuilt** and this file is the
evidence it rests on, kept because the route by which each figure was obtained is part of
the record. What shipped is NOT what this file first priced, in two ways, and both are set
out below rather than tidied away.

> **EVERY PRICED FIGURE IN THIS FILE WAS RESTATED ON 5 SEPTEMBER 2026 AND EVERY ONE CAME
> DOWN.** The first pricing handed the sanctioned construction this study's *terminal-year*
> figures — profit, book depreciation and working capital all already grown by (1+g) — and
> that construction grows them again. At Egypt's 7% terminal the terminal was overstated by
> exactly 7%, and the same defect was found in six of the eight studies then using the
> module. The correction does not change a single conclusion here: the direction is
> unchanged, the rebuild is still worth making, and this study is still held either way.
> It changes the size, and **it destroys one corroboration this file had claimed** — see
> §6, where the agreement with the study's own priced alternative was itself an artefact of
> the double growth. What this file records is the primary-source work, the
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
the sanctioned construction charges maintenance of EGP 5,145mn against a terminal profit
after tax of EGP 3,566mn — 144% of it — and drives the equity **negative**. That is not a
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

**The figures are the LAST EXPLICIT YEAR's, not the terminal year's**, because the module
applies (1+g) itself and values the terminal at the end of that year — which is where this
study's own year-five factor discounts it. That is the same convention this study already
uses in its own words: *"base_ebit is ALREADY the year-six flow … the Gordon numerator must
therefore be FCFF_6, not FCFF_6 × (1+g)"*. The first pricing of this table handed over the
year-six figures and let the module grow them a second time.

| | |
|---|---:|
| profit after tax, last explicit year, on the terminal year's economics | 3,566 |
| plus book depreciation and amortisation | 2,185 |
| less capital maintenance, at the measured 4.45-year age | (2,954) |
| less growth capital — the terminal real growth is **zero**, so nothing | — |
| less inflation on working capital | (214) |
| **free cash flow the perpetuity is struck on** | **2,583** |
| implied payout of profit | 72.4% |

Terminal **23,854** against the retired identity's 20,121, **+18.6%**; per share **2.9877**
against 2.3109, **+29.3%**. The gap against the traded 14.41 narrows from about −84% to
**−79.3%** — still far enough below the price that this study stays held, which is the
right outcome: a correction is applied because it is the better measurement, not because of
where it leaves the answer.

**On the half-life proxy the same terminal REFUSES**, charging 5,145 of maintenance against
3,566 of profit and driving the equity negative. The difference between a refusal and a
+29% correction is one number, and it was sitting in the accounts.

**AND IT BUILDS ON ALL FOUR OF THIS STUDY'S CASES, not just the one quoted.** That was worth
testing before committing to the rebuild, because a case with a thinner profit and the same
asset base is where a maintenance charge refuses:

| case | terminal profit | book D&A | maintenance | terminal cash flow | payout | terminal | vs retired |
|---|---:|---:|---:|---:|---:|---:|---:|
| base | 3,566 | 2,185 | 2,954 | 2,583 | 72.4% | 23,854 | +18.6% |
| bull | 3,546 | 2,185 | 2,954 | 2,565 | 72.3% | 23,684 | +18.4% |
| bear | 2,644 | 1,434 | 1,939 | 1,926 | 72.8% | 17,782 | +19.2% |
| halt | 3,902 | 952 | 1,287 | 3,353 | 85.9% | 30,962 | +40.6% |

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
| the sanctioned construction, on a measured-age maintenance charge | **2.9877** |
| the two agree to | **8.4%** |

**Two entirely different routes to the same neighbourhood.** One raises an assumed return
on capital inside the retired identity; the other throws the identity away and charges what
keeping the plant intact costs on the age the accounts measure. They were built
independently, months apart, and they land eight per cent apart on the same side of a
published number they both say is too low.

**THIS PARAGRAPH READ "they differ by a percent and a half" UNTIL 5 SEPTEMBER 2026, AND
THAT AGREEMENT WAS MANUFACTURED BY THE DEFECT.** On the doubly-grown arithmetic the
sanctioned construction gave 3.2905 against the study's own 3.2396 — 1.6% apart, which was
written up here as the strongest corroboration available. Correcting the growth basis moved
one of the two numbers and not the other, and the agreement widened to 8.4%. It is still
corroboration and it still points the same way; it is no longer remarkable, and the reason
it looked remarkable was an error. **A defect can manufacture agreement as easily as
disagreement, and agreement is the one nobody re-checks.**

This is worth contrasting with the two other cases in this programme where a study priced a
correction it declined: RIYADHCABLE's review predicted −16.2% and the build gave +1.97%, and
DU's predicted +5.6% against a built −2.6% — both wrong in sign. **Here the study's estimate
was right, and what it got wrong was the decision to keep the number anyway.**

## 7. What the rebuild will NOT fix, and the gap review will have to say so

**This study is TWO-SIDED and both branches move**, which matters because a two-sided answer
is held only if *every* branch sits more than ten per cent below the price:

| branch | published | corrected | move | gap now |
|---|---:|---:|---:|---:|
| capital programme carried through | 2.3109 | **2.9877** | +29.3% | −79.3% |
| capital programme stopped | 6.2591 | **7.8807** | +25.9% | −45.3% |

Both remain far below the traded 14.41, so **EGCH stays held either way** — the correction
does not change its publication status, and it was not made in the hope that it would.

Corrected, this study reads 2.9877 against a traded 14.41 — **still 79% below the price**,
so it stays held and its eight-heading review still has to explain a very large
disagreement. Two things about that are worth writing down before the rebuild, because they
change what the review should be looking at.

**The equity gap overstates the modelling gap, because the equity is a thin sliver.** Net
debt is EGP 10,032mn against an enterprise value of 11,085mn, so almost all of the
enterprise value is spoken for before equity gets any:

| | EGP mn |
|---|---:|
| study enterprise value, as published | 11,085 |
| study enterprise value, terminal corrected | 12,430 |
| price-implied enterprise value (market capitalisation plus net debt) | 38,659 |
| **the enterprise disagreement, corrected** | **3.1x** |
| the equity disagreement, corrected | 4.8x |

**So the honest statement of the disagreement is about 3x on enterprise value, not 5x on
equity** — leverage does the rest, and it does it in both directions. It is also why the
terminal correction is worth +29% on equity for +18.6% on the terminal: the same gearing.
*(The two enterprise figures are not on identical bases — the price-implied one carries the
listed stakes and investment property that the study's operating enterprise value excludes
and then adds in the bridge. Putting both on the study's basis gives 15,968 against 38,659,
2.4x. The point the row is making — that leverage, not the terminal, is doing most of the
work in the equity ratio — holds on either basis, and the mismatch is named rather than
left for a reader to find.)*

**And it means the terminal is not where the remaining gap can live.** After the correction
the enterprise value is 12,430mn against a price-implied 38,659mn. Closing that on the
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

---

## 9. What shipped, 5 September 2026, and the second defect this file did not find

The rebuild landed at **EGP 3.8967 carried through and 7.8807 stopped**, not at the 2.9877
and 7.8807 §5 and §7 above predict. The carried-through branch is 30.4% higher than this
file's own corrected pricing, and the reason is a defect the terminal rebuild EXPOSED rather
than caused.

**The project's depreciation was charged twice.** The explicit window depreciates the new
complex as it is spent, so the last explicit year already carried the charge on the part in
service — EGP 481.9mn — and the terminal then charged the whole plant on top. Grossing the
last explicit year without first removing the in-service part therefore charged it twice.

**Under the retired construction that error only depressed profit.** Under the sanctioned
one, book depreciation is also the BASE of the replacement charge, so an overstated charge
took value out twice: once through profit, and once through a maintenance charge struck on a
depreciation figure 32% too large. That is why the defect became worth finding only after
the first correction was made, and it is the general shape worth keeping: **a correction that
makes a quantity load-bearing makes every error in that quantity visible.**

**The model already knew how to do this**, which is what settles it as a defect rather than a
choice: the programme-stopped branch strips exactly that charge before it grosses the year,
which is why that branch was never wrong. Corrected, the two branches carry the identical
year-five formula and differ only in the project's own revenue, profit and depreciation.

Neither this file nor the four rounds of critique behind it found that. What found it was
building the waterfall and asking what number the depreciation add-back should be — a
question the retired construction never asks, because it never adds depreciation back.

**And one prediction in §7 above was wrong in the direction that matters least and is
recorded anyway.** This file said the correction "does not change its publication status".
It does not: at −73.0% and −45.3% both branches remain far below the price and the study
stays held. But it also said the terminal was where the remaining gap could NOT live, and
that was too strong — the terminal rebuild plus the double-count fix was worth EGP 1.59 a
share, a sixth of the outstanding gap. The conclusion survives; the confidence in it should
have been lower.
