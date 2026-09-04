# SWDY — what the re-issue found, before any of it is built

Measurements only. Nothing here has been applied to the study; each item is priced on the
study's own committed numbers or on primary filings fetched for this pass, so that the
order of correction can be decided rather than stumbled into ([R-VCAL-01]'s promotion
guard: one lever at a time, in an order fixed before the answers are known).

**The study as it stands:** published central EGP 69.73 (a typed 45/25/20/10 blend), its
own primary cash-flow lens EGP 56.08, spot EGP 105.20 at the 5 August 2026 strike. The
blend moves the published answer 19.6% ABOVE the study's own primary — toward the price —
so a reader sees −33.7% where the study's own method says −46.7%.

## The primary source was reached, and it took a route worth recording

`elsewedyelectric.com/en/investor-relations` 404s and the homepage carries no `href` to
investor relations — the link is rendered into a social-icon block pointing at a separate
host, `ir.elsewedyelectric.com`. That portal's results centre is JavaScript-rendered and
its document list arrives from `api/filter_results_center_sections`, a POST needing a CSRF
token that must come from the same session as the cookie. A headless browser was tried
first and its connection was reset through the proxy; calling the API directly with a
freshly-paired token and cookie worked. **Both 2025 and 2026 filings are public and
one command away**, which is the point: an absence asserted from a 404 would have been
wrong, and [R-IND-01] requires the ladder to be climbed rather than recalled.

Fetched and read: the audited FY2025 consolidated statements, and the reviewed condensed
interim consolidated statements for the six months to 30 June 2026.

## 1 — The latest filings: the study was RIGHT at strike and is stale now

The H1-2026 condensed interim consolidated statements were **approved for issuance on 11
August 2026**, six days AFTER this study was struck on 5 August. The study consumed
Q1-2026 (registered, dated 13 May 2026) and everything before it. **There is no unread
filing at the strike date** — the opposite of the defect this check exists for, recorded
because it was checked rather than assumed.

It is stale NOW, and [R-GAP-01 AMENDED] forbids delivering against a stale record. The
re-issue must consume the half:

| EGP mn | H1-2026 | H1-2025 | change |
|---|---:|---:|---:|
| Revenue | 163,315.7 | 123,800.6 | +31.9% |
| Gross profit | 26,333.3 | 20,245.4 | +30.1% |
| Operating profit | 16,421.2 | 12,605.2 | +30.3% |
| Profit attributable to owners | 9,921.7 | 8,694.6 | +14.1% |

Gross margin 16.12% against 16.35% a year earlier. The study's FY2026 revenue forecast is
370,029.5; the realised half is 44.1% of it.

## 2 — THE EMPLOYEES' SHARE IN PROFIT IS NOT CHARGED, and it is 12% of the answer

Egyptian company law gives employees a share of distributable profits. El Sewedy discloses
it, and discloses it **below** attributable profit — it is an appropriation ahead of
shareholders, not an operating cost, so it appears in no line of the income statement:

| | profit attributable to owners | employees' share | % |
|---|---:|---:|---:|
| FY2024 | 17,461.4 | 2,025.8 | 11.6% |
| FY2025 | 17,330.2 | 2,073.1 | 12.0% |
| H1-2026 | 9,921.7 | 1,291.2 | 13.0% |

The word "employee" does not occur anywhere in this study's committed numbers. The study
registers FY2025 attributable profit of 17,330.245 AND the reported EPS of 7.13 — and
those two disagree by exactly this charge (17,330.245 / 2,140.778 = 8.095 against a
reported 7.13). Both figures are correctly sourced; nothing reconciled them.

The valuation divides the full parent equity value by the full share count, so it hands
shareholders roughly **12% of value that the statute gives to employees**. Priced at the
three-year average: about **−12% on every lens**.

**It runs AGAINST the direction this study needs**, which is why it is recorded first. The
cap matters and is stated: the statutory share is capped at total annual wages, so the
percentage is an upper bound as profit grows, and the re-issue must model the cap rather
than a flat 12%.

Checked across the Egyptian book: only ARCC's register mentions it, where it is 0.5% of
distributable profit and immaterial. Whether the other seven are affected is a separate
measurement and is not asserted here.

## 3 — The terminal: a real DECLINE of −1.87% a year, for ever

Terminal growth is a typed 5.0% nominal against the EG house path's terminal inflation of
7.0% — a stated-nowhere real decline of **−1.87% per year in perpetuity**, on a terminal
carrying **84.8% of enterprise value**. [R-MACRO-01] permits real decline and requires it
to be WRITTEN DOWN as the real number it is; nothing in the study does.

The construction is the retired `g × IC`. Rebuilt through `terminal_value.build()` on a
life DERIVED by identity from SWDY's own audited note 17 — average depreciable gross cost
(excluding land, which the note says is not depreciated, and projects under construction,
which are not in use) over the year's own charge, **17.26 years**, with every component
sitting in or near its disclosed range:

| | gross cost (EGP) | FY2025 charge | implied |
|---|---:|---:|---:|
| Buildings & constructions | 13,357,135,195 | 460,515,584 | 29.00 y |
| Machinery & equipment | 32,960,824,267 | 1,760,913,546 | 18.72 y |
| Furniture & fixtures | 2,464,375,061 | 291,595,783 | 8.45 y |
| Vehicles | 1,630,540,975 | 192,986,364 | 8.45 y |
| Leasehold improvements | 363,075,076 | 27,660,585 | 13.13 y |

The note foots three ways — components to subtotal, subtotal plus projects under
construction to total, and the component charges to the total charge — which is what makes
the derivation usable rather than a plausible ratio.

**Unlike DU, the retired construction's implied cycle is roughly right here by accident**:
1/g at 5% is 20.0 years against a derived 17.26, because Egypt's higher inflation makes
1/g smaller. So the correction here is driven by the GROWTH RATE rather than by the life,
which is [R-TERM-01 CLAUSE TWO]'s direction-reversal from a third angle.

| | terminal value | vs published | cash-flow lens |
|---|---:|---:|---:|
| Published (`g × IC`, 5% nominal) | 286,048 | — | **56.08** |
| Sanctioned, the study's 5% restated as real −1.87% | 350,357 | +22.5% | 70.26 |
| **Sanctioned, ZERO real growth (the house default)** | **391,472** | **+36.9%** | **78.14** |

At zero real growth the cash-flow lens moves **+39.3%**, and the gap to the price goes from
−46.7% to −25.7%. Note that the real-decline case charges NEGATIVE growth capital
(−3,798), because a firm shrinking in real terms releases capital — arithmetically
consistent, and evidence that a real decline is an assumption rather than a prudence.

## 3b — The forecast opens 5.2% below the latest reviewed period — CORRECTED

**This section was written wrong and is corrected here rather than quietly rewritten.**
The first version claimed the forecast opened 20.6% below a margin the company had already
printed, comparing the study's forecast series against a GROSS-profit margin computed from
the reviewed half. It is not a gross-profit series. The study registers the note-16
**segment profit** row — gross profit less selling and distribution expenses — under a key
named `gp`, and FY2025 segment profit of 21,016.4 for cables is 11,707.2 + 9,309.2 from
that row, against a gross profit of 25,197.5 on the row above it. Comparing the two is
[L-289] exactly: a ratio between two quantities defined differently is not evidence about
either. It computes, it looks like a measurement, and it points the wrong way.

On the correct basis, and comparing **half to half** rather than a half to a full year —
because FY2025's 12.18% sits well below H1-2025's 14.06%, so this company's halves are not
alike and a half-against-year comparison is a second basis error waiting to happen:

| segment | FY2023 | FY2024 | FY2025 | H1-2025 | H1-2026 | forecast FY2026E |
|---|---:|---:|---:|---:|---:|---:|
| Cables and accessories | 19.48% | 18.11% | 13.49% | 14.54% | **12.49%** | 14.00% |
| Constructions and infrastructure | 11.62% | 11.44% | 6.45% | 9.06% | **11.59%** | 6.80% |
| Electrical products and digital | 25.44% | 26.58% | 22.17% | 23.46% | **24.91%** | 22.00% |
| **Group** | | | 12.18% | 14.06% | **13.92%** | 12.80% |

The forecast rates applied to the H1-2026 revenue mix give **13.19%** against a realised
**13.92%** — the forecast opens **5.2% below** the latest reviewed period, mix held
constant so that mix is not doing the work. That is just past [R-ANCHOR-01]'s relative 5%
threshold rather than four times it.

**The composition is the interesting part and it is genuinely mixed.** Cables, 59% of
revenue, is forecast ABOVE what it has just delivered — 14.00% against a realised 12.49%,
with the margin FALLING year on year from 14.54%. The contracting arm went the other way
and hard: 9.06% to 11.59%, against a forecast of 6.80%. So this is not a study that is
uniformly too pessimistic on margin; it is a study whose margin forecast is wrong in both
directions at once, and the group effect is the small residual of two large offsetting
errors.

That matters for the re-issue in a way the wrong version would have obscured: re-anchoring
on the reviewed half **raises** the contracting leg and **lowers** cables, and anybody who
had taken the first reading at face value would have raised all three.

**What must NOT be done with it.** One half is not a permanent margin, and the contracting
leg's improvement in particular may be project mix rather than a re-rating of the book. The
re-issue anchors on the reviewed half and lets each rate DRIFT only where a named mechanism
has a measured like-for-like direction in the company's own period pair — the discipline
that forbids projecting the improvement forbids ignoring it equally, and here it must be
applied to a fall as well as to two rises.

**And a defect in the study that this exposed, worth its own line:** the key is named `gp`
and holds segment profit. Nothing in the register says which row it is, and the study's own
prose calls it both things. That naming is what made the wrong comparison easy to reach —
it is the source-field defect of [L-290] in another costume, where the value is right and
the label is not.

## 4 — Still to measure, and not measured here

- The cost-of-capital schedule against [R-COC-01]: the terminal risk-free should DERIVE as
  7.0% + 5.5% = 12.5% from the house path; the study's `ke_term` is 17.563% and its `kd` of
  9.50% sits **12.8 points BELOW its own sovereign** at 22.31%, which [R-COC-01] refuses
  outright on a local-currency book. The study computes an EGP-equivalent Kd of 13.90% and
  publishes the alternative without adopting it.
- The class decision. SWDY is cables (13.5% gross margin), EPC contracting (6.5%) and
  electrical products (22.2%) — three businesses on materially different contract
  structures. `LENS_REGISTRY` carries no diversified-industrial row. Whether that earns a
  new class under [R-LENS-03]'s test — a DIFFERENT lens carrying the weight, not merely a
  different industry — is a judgement to be made and recorded, not assumed.
- The bridge: no `bridge_record` exists, so [R-BRIDGE-01] cannot be checked from outside.
  The minority is deducted at a 9.7% share of value (`nci_share`), which is a value-share
  proxy and needs its source named.

## 5 — The balance sheet has moved, and against the study

From the reviewed 30 June 2026 statement of financial position, read against the
31 December 2025 comparative it prints beside:

| EGP mn | 30 Jun 2026 | 31 Dec 2025 |
|---|---:|---:|
| Loans and borrowings, non-current | 8,072.5 | 8,620.7 |
| Loans and borrowings, current | 75,932.8 | 53,888.5 |
| Cash and cash equivalents | 52,775.7 | 41,949.2 |
| Investments in debt securities at amortised cost | 2,600.6 | 706.5 |
| **Net financial debt** | **28,628.9** | **19,853.5** |
| Equity attributable to owners | 70,347.3 | 66,870.9 |
| Non-controlling interests | 5,677.3 | 5,119.0 |

Net debt has risen about EGP 8.8bn over the half — roughly 4 per share against the
study's bridge figure of 20,560.0 — as working capital absorbed cash. The bridge stands
on the December sheet and [R-BRIDGE-01] requires the LATEST disclosed one.

One item runs the other way and is recorded because it does: the study deducts the
minority at a **9.7%** value share, against non-controlling interests of 7.47% of total
equity at 30 June 2026 (7.11% at December) and 6.81% of the half's profit. The study's
figure is conservative on all three readings.

## The order these must be applied in

[R-VCAL-01]'s promotion guard forbids stacking individually-justified moves without
watching where the total lands. Fixed here, before the answers are known:

1. **H1-2026** — a filed actual outranks everything. It re-anchors the base, the margin
   and the bridge, and it is the largest of these by some way.
2. **The employees' share** — a statutory claim ahead of shareholders, worth about −12%,
   and it runs AGAINST the direction the rest of this list runs.
3. **The terminal** — [R-MACRO-01] and [R-TERM-01], worth about +39%.
4. **The cost-of-capital schedule** — [R-COC-01], sign unknown.
5. **The blend** — [R-LENS-03], after the class decision.

Roughly: 56.08 × 0.88 × 1.39 ≈ 68.6 before the margin re-anchoring and before items 4 and
5, against a price of 105.20. That arithmetic is indicative and is NOT the answer; each
step is rebuilt on the real chain.

**What the shape of these findings says, and it is the point of the gap gate.** SWDY's
primary lens sits 46.7% below the market. None of these corrections was found by looking at
the price — they were found by asking the eight headings' questions of a study whose answer
was surprising, which is precisely why [R-GAP-01] calls a large discount a
high-prior-of-defect region.

But they do not all run one way, and the honest tally after the correction above is:

| finding | direction | size |
|---|---|---|
| The terminal in real decline, on the retired construction | toward the price | about **+39%** |
| The employees' statutory share, never charged | away from the price | about **−12%** |
| The margin re-anchoring on the reviewed half | toward the price, slightly | about **+5%**, and mixed by segment |
| Net debt up EGP 8.8bn over the half | away from the price | about **−4 a share** |

Two of four run away from the price, and the largest single correction is arithmetic
mandated by two standing rules rather than a judgement. **The first version of section 3b
put the margin finding at four times its true size and in a direction that was uniform when
it is not** — which is the strongest argument in this document for measuring rather than
reading a shape, and it is left in the record for that reason.
