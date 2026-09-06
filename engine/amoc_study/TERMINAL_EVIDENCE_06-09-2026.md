# AMOC — the disclosed useful life, SOURCED. The block of 5 September is cleared.

**Supersedes the status of `TERMINAL_EVIDENCE_05-09-2026.md`**, which recorded this name as
BLOCKED on a document and registered the block as an escalation. The block was not a fact
about the world. It rested on a probe pointed at the wrong host.

**This pass changes no published number.** It sources the life, prices what the sanctioned
terminal would give, and stops there. A rebuild is a re-issue with a rebuild ledger
[R-REBUILD-01] and an audit point declared in advance.

## How the block was cleared, and it is worth recording

The 5 September escalation recorded the company's own website as refusing at the proxy on
`www.amoc.com.eg` "and two alternates", re-run twice. Re-run again today: that host does not
resolve at all. **AMOC's investor site is `amoceg.com`.** It answers 200, it is not
authenticated, and it carries the audited statements one click from the homepage — the
2025 and 2024 annual filings and every interim back to 2023.

The register's other routes were sound and its arithmetic was right. What was wrong was a
single hostname, and everything downstream of it read as an absence rather than a mistake —
which is [R-ENF-04] exactly: **an empty result is not a clean result, and the first
hypothesis on an empty probe is that the probe did not run.**

Three filings are now committed under `filings/`:

| file | pages | text layer |
|---|---:|---:|
| `AMOC_CONSOL_31-12-2025.pdf` (audited, transition period) | 50 | **0 characters** |
| `AMOC_STANDALONE_31-12-2025.pdf` (audited) | 51 | **0 characters** |
| `AMOC_CONSOL_30-06-2025.pdf` (audited, year to 30 June 2025) | 53 | **0 characters** |

**Route: OCR off the rendered pixels** (`pdftoppm -r 150 -png`, then the page read as an
image). Not a fallback — these are pure scans and there is no text layer to prefer. The
worked case is the same shape at 47 characters across 47 pages; this is zero across 154.

## 1. The accounting-policies note, quoted as it stands

Note **5/2 "Fixed assets and their depreciation"**, A — Initial measurement and recognition,
consolidated statements for the period ended 31 December 2025 (page 12):

> "Fixed assets are stated according to the historical cost after deducting the accumulated
> depreciation and impairment loss."
>
> "... Depreciation is calculated using the straight-line method according to the assets
> estimated useful life as follows:"

| Item | Estimated Useful Life (yearly) |
|---|---|
| Machinery, equipment and devices | 10-30 |
| Buildings, constructions and utilities | 10-30 |
| Vehicles | 5-15 |
| Tools | 5-10 |
| Furniture, fixtures and computers | 4-10 |

**The depreciable amount is COST.** No residual is deducted anywhere in the sentence that
establishes it. The only reference to remaining values is on the following page — "The
remaining values of assets, their useful lives and depreciation methods are reviewed at the
end of each financial year" — which is the annual-review boilerplate, **not** a statement
about the depreciable amount. That is precisely the shape already ruled clean on
RIYADHCABLE, and the opposite of the shape that stopped EMPOWER ("at rates calculated to
reduce the cost of assets to their estimated residual values"), SAVOLA and AIRARABIA.

**So [L-328] condition (i) is satisfied and the age identity is valid on this name.**

## 2. The page foots — 46 of 46, to the pound

Note 6 was transcribed by eye off the rendered pixels and then held to its own arithmetic
(`footing_check` reproduced in this session): every class roll-forward on cost, every class
roll-forward on accumulated depreciation, every closing and opening net book value, all ten
cross-casts to the printed Total column, and the narrative sentence. **Zero failures.**
The fully-depreciated table foots exactly too (273,435,209 + 30,912 intangibles =
273,466,121 as printed). Arithmetic is the arbiter, and it validates the read.

| | EGP |
|---|---:|
| cost 31/12/2025 | 2,740,810,692 |
| less land, never depreciated | (75,752,185) |
| **depreciable gross cost** | **2,665,058,507** |
| the half's charge | 67,747,372 |
| **annualised charge** | **135,494,744** |
| accumulated depreciation | 1,847,794,418 |
| implied life, gross cost over charge | **19.67 y** |
| **measured average age**, accumulated over charge | **13.64 y** |

## 3. Weighting the classes — and what the note will not support

Weighted on Note 6's own carrying amounts by class, **the disclosed ranges do not collapse
to a point**:

| weighting basis | disclosed lives weight to |
|---|---|
| gross depreciable cost | **9.61 – 28.61 years** |
| still-depreciating cost | 9.71 – 28.95 years |
| net book value | 9.42 – 27.95 years |

A span of 2.98x on every basis. **Picking one number inside 10-30 is a choice this desk
would be making, and a life this desk chose is not a disclosed life.** So the single life is
not taken from the ranges. It is **measured off the note's own cost and charge columns** —
2,665,058,507 / 135,494,744 = **19.67 years**, which is the cost-weighted harmonic mean of
the lives the company actually applies, and which is not a figure anybody selected.

**The cheap cross-check the module asks for passes, and one class settles it.** Per class,
stripping the assets that are fully depreciated and therefore no longer charging:

| class | implied life | disclosed | inside? |
|---|---:|---|---|
| Buildings | 20.02 | 10-30 | yes |
| Machinery | 20.29 | 10-30 | yes |
| Vehicles | **5.0000** | 5-15 | **at the boundary** |
| Tools | 6.47 | 5-10 | yes |
| Furniture | 4.83 | 4-10 | yes |

Vehicles: remaining depreciable cost 3,423,027 against an annual charge of 684,606 is
**5.0000 years — the bottom of the disclosed 5-15 range, to within EGP 3 on 3.4 million.**
A charge struck on cost less a residual could not land on the disclosed boundary like that.
The arithmetic and the note agree, which is the test AIRARABIA failed at +48%.

**Caveat, recorded rather than buried:** EGP 273,435,209 of assets — **10.26% of depreciable
cost** — are fully depreciated and still in production. They carry cost into the numerator
and nothing into the charge, so 19.67 years is an **upper** reading of the accounting life;
on still-depreciating cost alone it is 17.65. The distortion is visible in the raw vehicles
figure, which reads 36.5 years before the adjustment against a disclosed 5-15.

## 4. The other two conditions, and the prior-year cross-check

- **(ii) reassessment — clean.** The prior year's filing (year ended 30 June 2025, page 12)
  carries the **identical** note 5/2: identical wording, identical five classes, identical
  ranges. Unchanged across two consecutive audited filings, so no life was reassessed and
  the charge is level across the base's history.
- **(iii) business combination — clean.** Note 6's movement table carries three movements
  only: additions, disposals and depreciation. There is no acquisition row. The subsidiary
  (Alexandria Wax Products S.A.E., 86.45%) was established in 1981 and is long held, so no
  acquiree's accumulated history sits against a short charge. This is not MODON.

**One honest limit on the negative search.** `tesseract` in this container reads a synthetic
control correctly and then times out on every real A4 scan, producing zero-byte output for
all 50 pages. So **no automated whole-document sweep for the word "residual" was actually
run**, and none is claimed. What is claimed is what was read: the fixed-asset policy note in
full, in two consecutive audited filings, plus the arithmetic above.

## 5. What the sanctioned terminal gives — priced, not applied

Built through `engine/terminal_value.build()` on the last explicit year (2030E): NOPAT
2,585.0, book D&A 228.6, working capital 4,878.9, terminal rate 18.1386%, terminal inflation
7.00%, **stated real growth zero** so the nominal 7.00% is derived and growth capital is nil.

| | retired g x IC | sanctioned |
|---|---:|---:|
| maintenance at current cost | — | 575.2 |
| working-capital charge | — | 341.5 |
| book D&A added back | — | (228.6) |
| **net capital charge** | **639.4** | **688.1** |
| **terminal value** | **19,091.5** | **18,221.9** |
| implied replacement cycle | 14.3 y (= 1/g) | 16.4 y |

Both sanctioned bases agree **exactly** — maintenance on the disclosed life over a
consistently derived replacement base, and book D&A escalated over the **measured** age of
13.64 years, both give 575.2. That is the two-route agreement that validates the base and
the life together.

`assert_terminal()` passes the rebuilt record and **refuses the published one by name**:
*"growth capital of 639.4 is charged against a STATED REAL GROWTH of zero."*

**Direction, reported as measured and against the expectation this file's predecessor
carried.** [R-TERM-01 CLAUSE TWO] says the defect starves a kiln at 7% inflation, so a
rebuild in this market would be *expected* to raise the value. **It does not. It lowers it:**
terminal −4.6%, value per share 11.4012 → 11.1593, **−2.12%**, terminal share of enterprise
value 56.0% → 54.8%. The reason is the one the 5 September file anticipated in its
conditional: **this base is older than uniform** — 13.64 years measured against 9.83 if
vintages were uniform, 39% older — and an older base costs more to replace at today's
prices, so maintenance rises. Run on the half-life fallback instead, the same rebuild would
have printed **+2.0%**; the measured age is worth 6.6 points and reverses the sign.

That is [R-TERM-01 CLAUSE TWO CORRECTED] landing a second time. The census flags this
terminal at **2.80x its own book depreciation** — the highest in the book after the worked
case — and the natural reading of that flag is that the terminal is charging heavily and a
rebuild would relieve it. The arithmetic says the opposite: the retired construction was
**under**-charging this name. **A ratio between two quantities defined differently is not
evidence about either**, and the sign is measured per name or not stated.

**A correction that moves the answer away from the price is not a reason to reconsider the
correction.** It is recorded and left where it fell.

## 6. What is outstanding

AMOC stays on the terminal ratchet until a rebuild is run deliberately, with its ledger and
its audit point declared in advance. The life is no longer the obstacle: it is sourced,
footed, cross-checked against the prior year and priced. The jurisdictional hypothesis
registered under [L-328] — that the measured-age route works where a company writes off cost
at disclosed rates with no residual — **has its second Egyptian success and is no longer
one-for-one.**
