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

## The order these must be applied in

[R-VCAL-01]'s promotion guard forbids stacking individually-justified moves without
watching where the total lands. Fixed here, before the answers are known:

1. **H1-2026** — a filed actual outranks everything, and it re-anchors the base.
2. **The employees' share** — a statutory claim ahead of shareholders, worth about −12%,
   and it runs AGAINST the direction the rest of this list runs.
3. **The terminal** — [R-MACRO-01] and [R-TERM-01], worth about +39%.
4. **The cost-of-capital schedule** — [R-COC-01], sign unknown.
5. **The blend** — [R-LENS-03], after the class decision.

Roughly: 56.08 × 0.88 × 1.39 ≈ 68.6 before items 4 and 5, against a price of 105.20. That
arithmetic is indicative and is NOT the answer; each step is rebuilt on the real chain.
