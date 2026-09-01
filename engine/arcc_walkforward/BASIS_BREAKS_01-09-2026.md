# ARCC — fundamental walk-forward, basis-break register

**Written before any driver was modelled**, per [R-FCAL-01] §1. A break is anything that
makes a number in one year a different object from the number under the same label in
another: an accounting-standard change, a segment or KPI re-cut, a definition change, a
currency regime, or a one-off the company itself attributed. Each carries its overlap year,
its size where the company disclosed enough to measure it, and the treatment the panel
applies.

Ticker ARCC · Arabian Cement Company S.A.E. · EGX · market EG · class **cement and heavy
industrial** · fiscal year = **calendar year**, every filing "for the year ended 31 December".

---

## B-1 · Every statement page is a SCAN, and the scan misreads a leading 1 as a 2

ARCC files its statements as images. Across the eleven annual filings **2,418 pages carry no
text layer at all** — the extraction route is OCR for every primary statement, and a text
layer only for the investor presentations and earnings releases.

The failure mode is not random noise, it is systematic and it is invisible in the extracted
figure. On the FY2016 filing OCR turned a **leading 1 into a 2 in three separate places**:

| line | OCR read | true value | how it was caught |
|---|---|---|---|
| income tax expense FY2016 | 224,683,515 | **124,683,515** | PBT − tax ≠ printed profit after tax |
| raw materials FY2016 | 2,257,697,536 | **1,257,697,536** | note 5 parts ≠ note 5 total |
| cost of sales, note 5 total FY2016 | 2,655,408,051 | **1,655,408,051** | note total ≠ the income statement |

All three were then **confirmed independently** by the FY2017 filing's comparative column,
which prints 1,655,408,051, (124,683,515) and 245,016,131 — the numbers the footing had
already recovered.

**Treatment.** No figure enters the panel until it foots against its own arithmetic:
revenue − cost of sales = gross profit; the parts of every note = the note's total; profit
before tax − tax = profit after tax; owners + non-controlling = profit after tax. Where a
page will not foot it is re-read. **Arithmetic is the arbiter, not the extractor's
confidence.** Four pages of the H1-2026 filing are set LANDSCAPE inside a portrait page box
and OCR upright into wreckage that still looks like text (2,444 characters, 25 word-like
tokens); turned 90 degrees the same page gives 1,889 characters and 93. Those pages are the
profit-and-loss statement and the changes-in-equity statement, so losing them silently would
have lost the newest disclosure in the archive. Route and rotation are recorded per page.

## B-2 · Overhead cost inside cost of sales is re-presented against G&A in the comparative

Twice in the window the company restated a prior year between **overhead cost (inside cost of
sales)** and **general and administration expenses**, leaving profit before tax untouched:

| year | as FIRST reported | as restated the following year | move |
|---|---|---|---|
| FY2018 cost of sales | 2,826,502,704 | 2,821,949,633 | −4,553,071 |
| FY2018 G&A | 108,388,819 | 112,941,890 | +4,553,071 |
| FY2019 cost of sales | 2,894,882,469 | 2,899,331,819 | +4,449,350 |
| FY2019 G&A | 103,266,465 | 98,817,115 | −4,449,350 |

**The two moves run in OPPOSITE directions**, so this is not one reclassification carried
forward — it is each year being presented differently when it becomes a comparative.

**Treatment.** The panel carries every year **as first reported**, from its own filing, and
keeps the restated figure beside it. An origin standing at FY2018 saw 2,826,502,704 and could
not have seen 2,821,949,633 (L-037, point-in-time). Gross profit and the cost-per-tonne
drivers are therefore scored on the as-reported basis, and the restatement is disclosed
rather than substituted.

## B-3 · Right-of-use assets enter cost of sales in FY2019

"Amortization of right of use" first appears as a cost-of-sales line in FY2019 (4,312,948);
the FY2018 comparative is nil. This is the leasing standard (Egyptian Accounting Standard 49
/ the local IFRS 16 analogue) arriving, and it moves cost between operating lease expense
inside overheads and an amortisation line.

**Treatment.** The cost stack is scored on the FIVE lines that exist for the whole window —
raw materials, manufacturing depreciation, licence amortisation, transportation, overheads —
and right-of-use amortisation is carried as a sixth line **scored only from FY2019**, inside
its own definition window. It never enters a per-tonne cost driver measured across the break.

## B-4 · Revenue note re-cut at FY2022: one services line becomes two

Through FY2021 the revenue note reads **Local sales · Export sales · Services** — a single
services line covering both channels. From FY2022 it reads **Local (sales + transportation
services) · Export (sales + transportation services)**, so services are attributed to a
channel for the first time.

| | FY2021 (old cut) | FY2022 (new cut) |
|---|---|---|
| local | 2,052,924,236 sales | 3,821,544,846 sales + 103,058,888 transport services |
| export | 239,005,072 sales | 667,514,155 sales + 82,884,935 transport services |
| services | 156,702,045 (unattributed) | — attributed above |

The FY2022 filing restates FY2021 onto the new cut (local 2,054,119,583 + 92,559,521;
export 237,809,726 + 64,142,523), which is how the two cuts can be tied at all.

**Treatment.** Channel PRICE drivers are built on the GOODS lines only, so the services
re-cut cannot move a realised price per tonne; services are a separate driver. The channel
split before FY2022 uses the goods lines as printed and the services line is carried
unattributed, which is what the filing supports.

## B-5 · Egyptian Accounting Standard 48 (revenue from contracts with customers)

EAS 48 governs revenue recognition across the later window and is cited in the FY2022 and
FY2025 filings. ARCC's obligation is the sale of cement and clinker, satisfied at a point in
time, so unlike a developer there is no percentage-of-completion clock here and **revenue and
cost sit on the same clock by construction** — the trap [R-FCAL-01] §3 names second, and the
one that produced [L-001], does not bite on this name. It is checked rather than assumed: the
FY2025 filing states the obligation is "selling cement", recognised on transfer.

## B-6 · Three currency regimes inside one window

Egypt devalued in November 2016, March 2022, January 2023 and March 2024. On the World Bank
period-average series the pound went 7.69 (2015) → 10.03 (2016) → 17.78 (2017) → 19.16 (2022)
→ 30.63 (2023) → 45.30 (2024) → 49.23 (2025), and annual inflation ran 10.4%, 13.8%, 29.5%,
14.4%, 9.2%, 5.0%, 5.2%, 13.9%, 33.9%, 28.3%, 14.1% across FY2015–FY2025.

**Treatment.** Two eras are declared in advance: **E1 = FY2015–FY2021** (the 2016 float and
the long stable stretch after it) and **E2 = FY2022–FY2025** (the 2022–2024 sequence). A bias
that changes sign between them is reported as instability and is **never corrected for** —
the average of two opposite regimes was true in neither.

## B-7 · The fuel base changed twice, and it is not a pure import

The company's own presentations date the energy conversion: RDF from November 2013 (line II),
the line-I hot disc from June 2015, and **the second coal mill in 2Q2018**, after which ACC
"was able to get rid of the diesel input, depending only on coal, pet-coke and RDF". The same
page records that ACC sources **70–80% of its coal needs through LOCAL pet-coke**.

This matters directly for [L-110], the class lesson this company itself produced: fuel and
imported inputs escalate on their own commodity path, not on domestic inflation. **But the
fuel here is not wholly imported** — a majority of the thermal input is domestically sourced
pet-coke and refuse-derived fuel. Treating the whole fuel bill as a coal import would be the
mirror of the error [L-110] warns about.

**Treatment.** Raw materials is one disclosed line and the filings never split fuel out of
it. The pre-registration therefore sets the raw-materials escalator as a **stated blend of
the coal path and domestic inflation, with the blend weight declared in advance and reported
as a sensitivity at both extremes** — never chosen on its score.

## B-8 · Investor-presentation KPIs are restated, mis-aligned, and change units

The decks are the only source of tonnes, so they are cross-checked against each other and
against audited revenue rather than trusted:

- **FY2015 cement sales volume** is printed 4,271kt by the FY2015, FY2017 and FY2018 decks and
  **4,150kt by the FY2016 deck**. Audited FY2015 revenue of 2,256,645,854 against the deck's
  own FY2015 revenue-per-tonne of 524 implies ~4,271kt (528 on the audited total), so the
  FY2016 deck is the outlier and the arithmetic says so.
- **FY2016** is 4,090kt in the FY2016 deck and 4,040kt in the FY2017, FY2018 and FY2019 decks.
- **The FY2021 deck's utilisation series is shifted by one year** against its own production
  series — it prints FY18–FY21 utilisation of 82/98/92/77% for clinker, which are the FY17–FY20
  values of the FY2020 deck.
- **The sales-volume chart switches from thousand to million tonnes at the FY2020 deck**
  (4,114 becomes 4.1). Undeclared, this reads as a 99.9% collapse.

**Treatment.** Utilisation is DERIVED from production over disclosed capacity, never taken
from a deck. Volume is taken from the **earnings releases**, whose fixed table prints local,
export and total tonnes in one place and which foot exactly for every year FY2016–FY2025
(local + export = total, ten years out of ten). Units are normalised by magnitude and the
rule is stated. Where two decks disagree, the origin sees **the number published at its own
date**, and the disagreement is registered rather than resolved by preference.

## B-9 · The cement export quota, and the export mix swing

Export volumes go 50kt (FY2016) → 401 → 602 → 614 → 364 → 497 → ~1,002 → 1,701 → 2,436 →
1,930kt (FY2025): from 1% of tonnes to 48% and back to 40%. Within that, the split between
CEMENT exports and CLINKER exports is only disclosed separately from FY2022. Clinker exports
carry a materially lower realisation than bagged local cement, so a volume driver that
ignores the mix prices the wrong tonne.

**Treatment.** Volume is driven by channel — local, cement export, clinker export — from
FY2022, and by local/export only before that, with the coarser split flagged where it binds.
The channel mix is a pre-registered driver in its own right, not a residual.

## B-10 · Treasury shares cancelled in H1-2026

The H1-2026 balance sheet shows issued and paid-up capital falling from 757,479,400 to
749,734,890 and treasury shares of 143,327,985 going to nil. At the EGP 2 par value that is
378,739,700 shares issued becoming **374,867,445** — exactly the count the FY2025-based study
already used (issued less treasury), so the cancellation CONFIRMS the share count rather than
changing it. Registered because a per-share number that moved for a mechanical reason and a
per-share number that moved for a valuation reason must not be confused.

## B-11 · Auditor firm name

The signing firm is a Deloitte Egypt member throughout: **Saleh, Barsoum & Abdel Aziz** to
FY2021 and **Wafik, Ramy & Partners** from FY2022. A firm rename, not a change of auditor,
and no restatement accompanies it. Recorded so that it is not later read as one.

## B-12 · Export subsidy income steps up 14x in H1-2026

FY2025 other income of 53,339,508 "includes export subsidies amounted to EGP 32,642,586". The
H1-2026 cash-flow statement carries **export subsidy income of 467,813,139** for the six
months, received in cash in the period. That is a step change of an order of magnitude in a
line the FY2025-based model treats as immaterial.

**Treatment.** It is NOT a driver of the walk-forward, whose last scored origin is FY2024;
it is registered here because the rebuilt study must decide explicitly whether it is
recurring, and because a study that had not read the H1-2026 filing would not know it exists.
