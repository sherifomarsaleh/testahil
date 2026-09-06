# EGCH — the disclosed useful life, sourced; and the weighted life REFUSED

**Dated 6 September 2026. This pass changes no published number.** It sources the disclosed
useful life from the filing, foots the page it came off, and records what could NOT be
sourced. Nothing here rebuilds the study, re-renders a document or moves a central; no
figure below is an input to anything until a rebuild takes it, and a rebuild is a re-issue
with a ledger [R-REBUILD-01].

The census reports this name's life as **`sourced 5-50 yrs`** — a BAND, not a life. This
file establishes why it is still a band and what it would take to collapse it.

---

## 1. The route, because the filing has no text layer

`EGCH_FY2024-25_Annual.pdf` — audited statements for the year ended 30 June 2025, Central
Auditing Organization, report dated 23 September 2025 — yields **48 characters across 48
pages** to `pdftotext`: one page break per page and nothing else. Every figure below was
read **by OCR off the rendered pixels**, `pdftoppm` at 200 and 400 dpi and the page read as
an image; ambiguous cells were re-cropped at 2.6x-4x. Tesseract was used only to locate
pages and its digit output was not relied on anywhere.

**ARITHMETIC IS THE ARBITER, AND IT ARBITRATED.** One cell — the comparative accumulated
depreciation at the opening of the prior year — read `2,310,555,434` at 200 dpi. On that
reading the comparative column failed to roll by exactly EGP 5,000,000. The figure that
makes it roll is `2,315,555,434`; magnified 4x the pixels say `٢٣١٥٥٥٥٤٣٤`, and the prior
year's own page prints the same number as its closing total. The arithmetic found it, the
pixels confirmed it, and the extractor's confidence had nothing to do with it.

## 2. What the accounting-policies note actually discloses — RATES, not lives

**Note 5-2 `الأصول الثابتة وإهلاكاتها`, sub-heading `الإهلاك`, PDF page 31** (printed note
page 2):

> يتم تحميل الإهلاك على قائمة الدخل وفقا لطريقة القسط الثابت وفقا لمعدلات تتماشي مع العمر
> الإنتاجي المقدر لكل أصل عدا الأراضي وفيما يلي بيان بمعدلات الإهلاك لكل نوع من الأصول
> الثابتة لغرض حساب الإهلاك

*Depreciation is charged to the income statement on the straight-line method at rates
consistent with the estimated useful life of each asset, land excepted.* The table that
follows, exactly as it stands:

| بيان (class) | معدل الإهلاك (rate), verbatim | derived years |
|---|---|---|
| **مباني** (buildings) | 2% residential-city buildings / 5% water and sewage pipes / 10% air-conditioning units / 12.5% overhead cranes / 6% plants / 6% urea-ammonia plant / **+30%** cinema and cafeteria building / 16.5% rest-house building 26 / 10% iron and steel buildings | 50 · 20 · 10 · 8 · 16.7 · 16.7 · *(see below)* · 6.1 · 10 |
| **آلات ومعدات** (machinery and equipment) | 9.5% plants / 6.5% workshops / 3.95% urea-ammonia plant | 10.53 · 15.38 · 25.32 |
| **أصول غير ملموسة** (intangibles) | 4.75% urea-ammonia plant | 21.05 |
| **وسائل نقل وإنتقال** (vehicles) | 12.5% cranes, loader, bulldozers / 20% lorry, bus, passenger cars, tractors | 8 · 5 |
| **عدد وأدوات** (tools and implements) | 7.5% | 13.33 |
| **أثاث وتجهيزات** (furniture and fittings) | 10% | 10 |
| **حاسب آلي** (computers) | 10% | 10 |

**THE YEARS ARE DERIVED, NOT DISCLOSED** — they are 100/rate, an identity, and the label is
what keeps the two apart.

**One cell is still not read and is named rather than guessed.** The cinema-and-cafeteria
building prints as `+٣٠٪`. A 30% rate is a 3.3-year building, which is implausible on its
face; a rates table carries no internal arithmetic, so the usual arbiter is unavailable and
there is nothing to settle it against. **A figure this desk cannot read is a figure this
desk does not use (SIGCM clause 8).** It is immaterial — the cinema is not a production
asset — but it is not quietly rounded into the band either. Two cells previously carried as
unread are now read cleanly at 400 dpi and recorded above: **iron and steel buildings 10%**
and **furniture and fittings 10%**.

**Residual values do not enter the depreciable amount.** They appear only in the
annual-review boilerplate (`ويعاد النظر في العمر الإفتراضي المقدر والقيم التخريدية وطرق
الإهلاك المطبقة في نهاية كل سنه مالية`), never in the charge. The charge is a RATE against
COST, so a 3.95% rate is cost/25.32 with nothing deducted — which is the condition the
`accumulated ÷ charge` age identity needs, and §5 tests it three independent ways off the
company's own columns rather than taking the note's word for it.

## 3. The page foots — nine cross-foots, six roll-forwards, both directions

**Note 6 `الأصول الثابتة (بالصافي)`, sub-note 6/1 `الأصول الثابتة في ٢٠٢٥/٦/٣٠`, PDF page 35.**
Columns: أراضي · مباني/إنشاءات · آلات معدات · وسائل نقل · عدد وأدوات · أثاث ومعدات مكاتب ·
إجمالي · رصيد مقارن.

| | land | buildings | machinery | vehicles | tools | furniture | **total** |
|---|---:|---:|---:|---:|---:|---:|---:|
| cost, opening | 1,664,662 | 838,529,045 | 14,899,567,203 | 52,129,116 | 972,264,389 | 44,130,819 | **16,808,285,234** |
| additions | — | 166,109,468 | 22,380,390 | 6,912,164 | 6,096,672 | 12,842,983 | **214,341,677** |
| disposals | 1,713 | — | — | 6,300 | 74,159 | 51,501 | **133,673** |
| **cost, closing** | 1,662,949 | 1,004,638,513 | 14,921,947,593 | 59,034,980 | 978,286,902 | 56,922,301 | **17,022,493,238** |
| accumulated, opening | — | 286,925,872 | 2,007,203,259 | 46,649,842 | 305,503,251 | 17,936,054 | **2,664,218,278** |
| the year's charge | — | 50,606,799 | 638,236,944 | 5,267,368 | 72,833,835 | 4,268,543 | **771,213,489** |
| on disposals | — | — | — | 6,300 | 74,159 | 51,501 | **131,960** |
| **accumulated, closing** | — | 337,532,671 | 2,645,440,203 | 51,910,910 | 378,262,927 | 22,153,096 | **3,435,299,807** |
| **net book value** | 1,662,949 | 667,105,842 | 12,276,507,390 | 7,124,070 | 600,023,975 | 34,769,205 | **13,587,193,431** |

Every one of the nine rows cross-foots to its printed total; every class rolls forward in
both cost and accumulated depreciation; cost less accumulated reproduces net book value in
every class and in total. **Exact to the pound, no tolerance.**

A fifth independent check: **note 6-3**, fully depreciated and still in production at
30/6/2025 — buildings 16,470,389 · machinery 174,124,497 · vehicles 19,685,296 · tools
3,512,434 · furniture 6,702,978 · **total 220,495,594**, which foots and equals the figure
the study already registers.

Four of these figures were already committed by this study from an earlier reading and are
reproduced here independently: charge 771,213,489 · accumulated 3,435,299,807 · net fixed
assets 13,587,193,431 · fully depreciated in use 220,495,594.

## 4. THE WEIGHTING REFUSES, and the refusal is the finding

The task a terminal needs is ONE maintenance life. Weighting the disclosed rates by the
property note's own carrying amounts needs **one rate per note-6 class**, and the two notes
do not meet:

| note-6 class | share of depreciable NBV | disclosed rates inside it | weightable? |
|---|---:|---|---|
| machinery and equipment | **90.36%** | 3.95% · 6.5% · 9.5% | **NO** |
| buildings and constructions | 4.91% | 2% · 5% · 6% · 6% · 10% · 12.5% · 16.5% · 10% · (30%?) | **NO** |
| tools and implements | 4.42% | 7.5% | yes — 13.33 y |
| furniture and office equipment | 0.26% | 10% | yes — 10 y |
| vehicles | 0.05% | 12.5% · 20% | **NO** |
| land | n/a | not depreciated | n/a |

**The three classes the note will not split are 95.32% of net book value**, and the one that
carries the company — machinery, 90.36% — spans 3.95% to 9.5%, which is **25.32 years to
10.53 years**. Nothing in the filing apportions the machinery column between the
urea/ammonia plant, the older plants and the workshops.

**IT IS MATERIAL, NOT PEDANTIC.** Holding every other class at the life its own disclosure
gives and moving machinery across its own disclosed band:

| machinery taken at | weighted life | maintenance on the 17.02bn depreciable base |
|---|---:|---:|
| 3.95% (urea/ammonia) | 23.29 y | 730.7 mn |
| 6.5% (workshops) | 15.26 y | 1,115.5 mn |
| 9.5% (plants) | 10.85 y | 1,568.2 mn |

**2.15x on the single number the terminal turns on**, at historical cost and wider at
replacement cost — against a terminal free cash flow of order EGP 2.6bn. Choosing among
those three is choosing the answer.

**So none was chosen.** This is the exemplar's own refusal, on the same grounds: where the
note does not split the line, the life that would split it cannot be derived, and **A LIFE
THIS DESK CHOSE IS NOT A DISCLOSED LIFE** (SIGCM clause 1, stop and inform per clause 8).

## 5. What the note's own columns DO give, by identity — and it is not a disclosed life

The charge column is itself the weighting: the company applied each disclosed rate to each
of its own sub-classes and printed the sum. So the cost-weighted life is an identity off
the note's own figures and needs no split at all:

**depreciable gross cost ÷ the year's own charge = 17,020,830,289 ÷ 771,213,489 = 22.07
years** (21.79 on the opening base). This is what the study already commits as
`fa_life_implied_years`, labelled DERIVED, sourced to the note 6 register — **not** to the
accounting-policies note, and it must never be cited to it.

Per class, the same identity against what note 5-2 discloses:

| class | effective rate (charge ÷ opening cost) | effective life | disclosed |
|---|---:|---:|---|
| buildings | 6.035% | 16.57 y | **6% plants — agrees to 3.5bp** |
| machinery | 4.284% | 23.34 y | between 3.95% and 6.5%, nearest the urea/ammonia rate |
| vehicles | 10.104% | 9.90 y | **below both disclosed rates — see below** |
| tools | 7.491% | 13.35 y | **7.5% — agrees to 0.9bp** |
| furniture | 9.672% | 10.34 y | **10%, on an opening base carrying part-year additions** |

**Three classes reproduce their own disclosed rate to within a few basis points off the
company's own columns.** That is independent evidence that the charge is cost x rate with
no residual deducted — the condition the age identity rests on — established by arithmetic
rather than by trusting the policy note's wording.

**Vehicles is where the identity visibly breaks, and the reason is disclosed.** 88% of the
vehicle cost is already written off (NBV 7,124,070 on cost 59,034,980), and an asset past
its life stops charging, so cost-over-charge overstates the life. Note 6-3 bounds the
aggregate effect: fully depreciated and still in use is 220,495,594, **1.30% of the
depreciable base**. Large inside vehicles, which are 0.35% of cost; small in total.

## 6. Cross-check against the prior year's identical table

`EGCH_FY2023-24_Annual.pdf` (42 pages, 42-byte text layer — same route). Rates table PDF
page 25; note 6/1 PDF page 29.

* **Identical presentation and the identical six classes.** The FY2024-25 split is not a
  one-off.
* **Every FY2024 closing figure ties to the FY2024-25 opening, class by class, with ONE
  exception:** machinery cost closes at **14,899,567,202** in the FY2023-24 filing and
  opens at **...203** in the FY2024-25 filing. That single pound is the whole of the EGP 1
  break visible on the FY2024-25 page between its own comparative total (16,808,285,233)
  and its opening total (16,808,285,234). **Located, not merely noted.**
* **The rates table is the same, plus three building sub-classes added in FY2024-25** —
  cinema and cafeteria, rest-house building 26, iron and steel buildings. The last is
  corroborated by note 6/2's own bullet: six buildings in the iron-and-steel area,
  EGP 46,811,754, recognised at 30/6/2025.
* **The prior year prints the urea/ammonia machinery rate with its digits visually
  transposed** — `٩٥,٣` where FY2024-25 prints `٣,٩٥`. A 95.3% rate is impossible and
  arithmetic settles it without appeal to the later page: that year's machinery charge over
  its own opening machinery cost is **516,762,388 ÷ 11,775,504,938 = 4.389%**. The rate is
  3.95%.
* **The prior-year page does NOT fully foot, and it is recorded rather than smoothed.** Its
  cost block foots exactly in every row and column. Its accumulated-depreciation *opening*
  and *charge* rows each miss their printed totals by **EGP 1,000,010** on the reading
  obtained, in opposite directions, so the closing row foots exactly and ties to the next
  year's opening. Immaterial (4 parts in ten million) and outside the current-year figures
  this file sources, but it is the prior year's page, not this desk's arithmetic, that does
  not add up.

## 7. What this leaves, exactly

* **The disclosed life is FOUND and it is a BAND**: 5 to 50 years across classes, as the
  census already reports. The census is right.
* **The single weighted maintenance life is REFUSED**: it cannot be sourced from this
  disclosure, because the property note's classes are coarser than the rate table's and the
  class carrying 90.4% of the value spans a 2.4x range of lives.
* **22.07 years is available as an IDENTITY** off the note's own cost and charge columns,
  is already committed, and is labelled derived. It is not a disclosed weighted life and
  changes nothing here.
* **Nothing above requires the study to move.** Its terminal is already built through the
  sanctioned module on the `book_dna_escalated` basis with a MEASURED average age of 4.45
  years, which does not consume a weighted life at all; the life it carries is inert at the
  central, where real growth is zero.
