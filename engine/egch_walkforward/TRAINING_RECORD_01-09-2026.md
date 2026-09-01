# EGCH (KIMA) — fundamental walk-forward training record

**1 September 2026 · Egyptian Chemical Industries "KIMA" · EGX · registered class:
petrochemical (the company is a gas-fed nitrogen-fertiliser producer; see the report for
the class proposal) · scope FULL · 13 origins FY2012–FY2024 · horizons 1–5 · 55 cells**

**Internal.** The panel, the error cells, the pre-registration and this record are never
shown to a reader. Nothing here reaches the live site.

**Which walk-forward:** the FUNDAMENTAL one — drivers projected from a past origin and
scored against what the company reported. Not the price-engine walk-forward (band coverage
on the Monte Carlo cone) and not the technical walk-forward.

**Queue position, recorded as a decision:** `campaign_queue.py --next` returns ARCC; EGCH
was named explicitly by the user and runs out of queue order on that instruction.

Companion files: `PRE_REGISTRATION_01-09-2026.md` (written first, unamended),
`BASIS_BREAKS_01-09-2026.md`, `panel.py` (footings as import-time assertions),
`macro.py`/`macro.json`, `bottom_up.py`, `score.py` → `scores.json`, `diagnose.py` →
`diagnostics.json`, `corrections.py` → `corrections_log.json`, `forward.py` →
`forward_ranges.json`, `egch_IS_projected_vs_actual_all_origins.md`,
`fetch_attempts.json`, `ir_register.json`, `lessons_draft.json`.

---

## 1 · The span, and why it stops where it stops

Eighteen fiscal years, FY2008–FY2025, every one from the company's own audited
statements on its own investor-relations channel (kimaegypt.com → the Mist portal it
embeds), plus the reviewed nine months to 31 March 2026. Ten older annuals (2009, 2010,
2011, 2013, 2014, 2016, 2018, 2019, 2020, 2021) were retrieved for this run; the 2022–2025
annuals and the three FY2025/26 interims were already held. All are scanned images: every
figure was read off the rendered page and footed, and 17 of 18 years foot on every
subtotal. **FY2014 is partial** — the company's own 2014 annual is a 367×519 pixel scan
whose profit lines cannot be read; the blocks that foot are carried and nothing is
reconstructed. **FY2008, FY2012, FY2015 and FY2017 exist only as comparatives** (the
archive lists no annual for 2012, 2015 or 2017, nothing older than 2009). The window
stops at FY2025 because FY2025/26 has not been reported as a year; the listing page could
not be re-read on 1 September (a 709-byte stub) and no newer document is known.

Two things a reader of the earlier study should know about its own extraction. The FY2022
income statement in `extract_history.json` was the FY2023 filing's *restated* comparative
(cost of sales reclassified) and mis-read provisions formed as 21,000 against the printed
210,000; and the cost-of-sales notes by nature do not foot in any of the three years they
were extracted for (misses of 247k, 36.3m and 63k EGP). Both are corrected or excluded
here (B-5, B-7).

## 2 · The headline, stated plainly

**On net profit the method does not beat "no change" on the log record, and on the whole
record the miss is dominated by two lines the pre-registered rules got wrong for reasons
that are specification, not calibration.**

| | n | excluded (non-positive) | bias | MAE | over-forecast | skill vs freeze | skill vs trend |
|---|---:|---:|---:|---:|---:|---:|---:|
| Revenue | 55 | 0 | −44.9% | 125% | 33% | **+0.146** | +0.178 |
| Cost of sales | 55 | 0 | −39.1% | 86% | 22% | **+0.273** | +0.091 |
| Gross profit | 34 | 21 | −14.8% | 118% | 41% | +0.024 | +0.229 |
| Profit before tax | 23 | 25 | −50.9% | 148% | 26% | **−0.407** | +0.111 |
| Net profit | 23 | 25 | −56.7% | 162% | 26% | **−0.559** | −0.023 |

A skill of −0.559 means the method's average miss on net profit is 1.56 times the miss
you get by writing down last year's profit and stopping. By horizon the net-profit skill
against freeze is −0.97 (h1, n=6), −0.57 (h2, 6), −0.09 (h3, 5), +0.28 (h4, 3), −1.10
(h5, 3): it loses at four of five horizons. Revenue and cost of sales beat both
benchmarks at most horizons (revenue vs freeze: −0.02, +0.01, +0.14, +0.22, +0.23 at
h1–h5). **The lines the method models as volume × price on a coherent currency path are
better than "no change"; the profit residual is not.**

Twenty-five of forty-eight profit cells are non-positive on one side and are outside the
log score (B-3). On those the sign check reads 58% right for profit before tax and net
profit, 64% for gross profit. The scale-free diagnostic — (projected − actual) / actual
revenue, every cell — puts the pre-registered net-profit miss at 64.5% of revenue against
74.4% for freeze (skill +0.13) and the profit-before-tax miss at 48.7% against 45.5%
(skill −0.07). So the two scores disagree in sign on net profit; neither says the method
has earned precision on the profit line.

## 3 · Where the profit error lives — three specification findings

The net-profit error decomposed by line (mean signed contribution, % of target revenue,
48 cells): revenue −22.6 · cost of sales +20.2 · admin +9.0 · **currency −41.2** · debit
interest +11.9 · **tax +31.6** · everything else within ±4. Three of those are the model
being wrong rather than the company being surprising.

**F1 — The currency line. The company does not run the translation of its dollar debt
through profit the way a coherent currency path says it must.** Driver D7 charges
`−B_usd × ΔFX` each year on the KIMA-2 consortium loan (US$292m at signing, EGP 11–14bn
on the balance sheet by FY2024–FY2026). On the realised path that is a loss of EGP
2.7–4.4bn in each of FY2023 and FY2024. The company reported a currency result of **0**
in FY2023 and a **gain of +279m** in FY2024 — during a 52% devaluation — and −265m in
FY2025. The 9M FY2026 auditor's letter says why: the revaluation loss on the project loans
is *capitalised into construction in progress* (the auditor flags EGP 197.8m of ANNA-loan
revaluation "expensed rather than capitalised" as the exception). Under Egyptian
Accounting Standard 14 the borrowing cost — interest and exchange differences — on a
qualifying asset goes to the asset. The driver is therefore mis-specified against the
company's accounting: the loss is real, it is in the balance sheet, and it is not in the
income statement the method is scored on. **This is [R-FCAL-01]'s trap (i) in a new
form: the finance charge and the currency charge are not where the debt says they are.**
With perfect foresight of the currency the net-profit MAE gets WORSE (162% → 357%),
which is the macro split's way of saying the same thing (net-profit macro share −58%).

**F2 — The tax line. A statutory-rate formula on a company that has paid almost no
current tax since FY2019.** Tax by formula at the origin's rate (20%/25%/22.5%) misses
the FY2020 deferred charge of EGP 915m (290% of that year's revenue — the write-off of the
old plant's deferred-tax position) and, in the other direction, the deferred credits of
FY2024–FY2025 (+234m, +11m) on a company carrying forward the FY2020–FY2021 losses of
EGP 2.77bn. The rule is the right rule for a regime; the record says this company's tax
line is a balance-sheet story, and the study now carries a zero-current-tax sensitivity
rather than assuming it away.

**F3 — The plant replacement.** Every mechanical rule projects the business that existed
at the origin. Origins FY2015–FY2019 project the 1960 electrolytic plant into the years
in which it was shut and a gas-fed urea complex twelve times its revenue replaced it;
FY2020 and FY2021 were loss years on both sides. The plant-replacement split
(`diagnostics.json`) removes every cell whose origin or target sits in FY2020–FY2022:
revenue MAE falls from 125% to 60% (freeze 159% → 82%), net-profit MAE from 162% to 127%
(freeze 186% → 163%). **The method's margin over freeze is about the same with or without
the replacement; the level of error is not.** This is L-043's finding (a projected asset
base cannot see an acquisition) at the scale of the whole company.

## 4 · Per driver

Log bias and MAE translated to percentages; CIs are the 5th–95th percentiles of the
moving-block bootstrap over origins at block lengths 2 / 3 / 4; macro share is
`1 − MAE(perfect foresight)/MAE(knowable)`.

| driver | n | bias | MAE | over | CI (block 2) | CI (block 3) | CI (block 4) | robust sign | macro share | skill vs freeze | skill vs trend |
|---|---:|---:|---:|---:|---|---|---|---|---:|---|---|
| revenue | 55 | −44.9% | 125% | 33% | −80%..−6% | −85%..−8% | −80%..−10% | yes | 22% | +0.146 | +0.178 |
| urea tonnes (unit window) | 3 | +9.3% | 9% | 100% | n/a | n/a | n/a | — | 0% | n/a (rule = benchmark) | 0.000 |
| cost of sales | 55 | −39.1% | 86% | 22% | −68%..−9% | −73%..−13% | −68%..−17% | yes | 6% | +0.273 | +0.091 |
| gross profit | 34 | −14.8% | 118% | 41% | −42%..+12% | −42%..−1% | −36%..−2% | no | −48% | +0.024 | +0.229 |
| selling | 21 | −32.9% | 83% | 33% | −74%..+24% | −69%..+25% | −66%..+22% | no | 18% | +0.095 | +0.156 |
| admin | 55 | −24.9% | 57% | 31% | −49%..+13% | −52%..+16% | −49%..+9% | no | 2% | +0.316 | +0.402 |
| provisions | 38 | −40.7% | 482% | 37% | −86%..+73% | −83%..+46% | −81%..+6% | no | 0% | n/a | +0.228 |
| other bucket | 23 | +17.9% | 130% | 61% | −45%..+179% | −38%..+92% | −18%..+53% | no | 0% | n/a | +0.581 |
| investment income | 55 | −23.8% | 118% | 44% | −70%..+79% | −74%..+92% | −70%..+79% | no | 0% | n/a | +0.333 |
| credit interest | 48 | −1.3% | 1009% | 50% | −96%..+537% | −96%..+677% | −95%..+537% | no | 0% | n/a | +0.333 |
| debit interest | 28 | −72.1% | 294% | 14% | −90%..−35% | −86%..−41% | −83%..−35% | yes | 4% | +0.154 | +0.020 |
| profit before tax | 23 | −50.9% | 148% | 26% | −68%..−9% | −71%..−32% | −66%..−35% | yes | −75% | −0.407 | +0.111 |
| tax | 21 | −72.7% | 348% | 33% | −90%..+3% | −89%..−48% | −88%..−66% | no | −35% | −0.329 | +0.099 |
| net | 23 | −56.7% | 162% | 26% | −74%..−9% | −77%..−35% | −72%..−40% | yes | −58% | −0.559 | −0.023 |

Five things in that table are worth naming.

**Revenue is under-forecast in two thirds of cells and the sign is robust.** Realisation
carried on a PPP currency path could not see the 2016 float (revenue doubled in FY2017),
the plant (FY2022 ×3) or the urea spike of FY2022–FY2023. By era: E1 −16%, E2 −65%, E3
−52% — one sign, three magnitudes. The β = 0.5 sensitivity makes it worse (−52%), which is
what it should do on a company whose revenue is a dollar commodity.

**Debit interest is under-forecast by 72% with a robust sign, and the reason is the
same as F1.** The rate formed on opening borrowings at origins FY2018–FY2020 is 0.0%,
0.5% and 2.4% because the interest was *capitalised* during construction. Formed on the
borrowings that bear it, exactly as the protocol requires, the rate was still wrong,
because the charge the income statement shows during construction is not the rate the
loan carries. The rate was declared undefined (floor of 10% of revenue) at every origin
through FY2015, and defined at FY2016 (7.1%) and FY2017 (5.8%) on the holding-company
loans. Nothing about this driver's construction can be corrected by a multiplier.

**Gross profit's macro share is −48% and net profit's −58%.** Perfect foresight of the
macro path improves revenue (MAE 125% → 89%) and cost of sales (86% → 79%) and makes the
profit lines worse, for the reason in F1: the realised currency path feeds a currency
loss the company did not book. A macro split that comes back negative on the aggregate
while positive on every line below it is the fingerprint of a line whose accounting the
model has not understood.

**The macro split's own check passed.** The five drivers carrying no CPI, no currency and
no urea term (urea tonnes, provisions, other bucket, investment income, credit interest)
returned a macro share of exactly zero, as they must by construction; the run asserts on it.

**The unit window is three cells.** Urea tonnes flat at the origin over-forecast by 9.3%
in all three (output fell 586kt → 522kt → 513kt on gas curtailment) — the same flat-volume
lean AMOC showed (+7.6%, 8 of 9). Inside that window the revenue error is entirely
realisation (+11%, +49%, +34%), not volume (−11%, −12%, −2%).

## 5 · The currency path — coherent, and still wrong in a managed regime

The pre-registration chose one coherent macro path (L-048): urea flat in dollars, the pound
moving by PPP on the last published CPI differential, costs on the same CPI. The
counterfactual AMOC path (currency frozen, costs compounding) is run as a diagnostic:

| line | pre-registered (PPP) | currency frozen (diagnostic) | perfect foresight |
|---|---|---|---|
| revenue | bias −44.9% · MAE 125% | −57.5% · 159% | −32.3% · 89% |
| cost of sales | −39.1% · 86% | −39.1% · 86% | −35.4% · 79% |
| gross profit (n) | −14.8% · 118% (34) | −64.6% · 204% (21) | −34.3% · 217% (39) |
| net (n) | −56.7% · 162% (23) | −66.1% · 205% (15) | −54.5% · 357% (20) |

The coherent path is better than the frozen one on every line, and it is still a long way
from the outturn, because Egypt's currency did not follow PPP: the pound held or
appreciated through FY2017–FY2021 (17.8 → 15.7) with published inflation of 14–30%, then
fell 200% in three steps. The cost of that is stated in the pre-registration and it is
where it belongs — in the macro share (22% on revenue), not in a correction factor.

## 6 · Corrections — estimated, tested, none promoted

Thirteen origins allow the expanding-window estimate the protocol describes, and it was
run: half strength, sign held across resolved eras and bootstrap blocks, reset at the
plant replacement and after a two-sigma shock. Clause 1 passed at some origin for every
correctable driver — and **applying it hurt more often than it helped**:

| driver | origins where clause 1 passed | helped / hurt | mean ΔMAE when applied |
|---|---|---:|---:|
| revenue | FY2017, FY2023, FY2024 | 0 / 3 | +0.446 |
| cost of sales | FY2017, FY2023, FY2024 | 0 / 3 | +0.247 |
| selling | FY2015–FY2019, FY2024 | 1 / 2 | +0.172 |
| admin | FY2015, FY2017, FY2019 | 2 / 1 | +0.013 |
| debit interest | FY2023, FY2024 | 0 / 2 | +0.253 |

The revenue and cost corrections estimated at FY2023–FY2024 are large (+0.7 to +0.8 log)
because the resolved KIMA-2-era record is three cells of a currency shock; applied
forward they over-corrected. Clause 2 would have blocked every one of them independently
(revenue is volume × realisation on a disclosed unit everywhere in the book; interest is a
rate on the borrowings that bear it; no study carries a multiplier on an aggregate). All
five are **watch flags** — recorded, graded at the next update, acted on by nobody — and
the dominant errors (F1–F3) are specification defects that no multiplier may hide.

## 7 · What this licenses the study to say about years 3–5

Multiplicative bands from this record's own error distribution (`forward_ranges.json`);
p10–p90 where a horizon holds at least nine observations, bias ± MAE below that; the
published band is the wider of the full record and the KIMA-2-era band; every figure
carries its count.

| horizon | revenue | gross profit | net |
|---|---|---|---|
| 3 years | ×0.11 – ×1.18 (n=11) | ×0.26 – ×2.00 (n=6) | ×0.14 – ×1.25 (n=5) |
| 4 years | ×0.04 – ×1.20 (n=10) | ×0.23 – ×1.81 (n=5) | ×0.48 – ×1.00 (n=3) |
| 5 years | ×0.08 – ×1.33 (n=9) | ×0.08 – ×1.35 (n=5) | ×0.06 – ×1.12 (n=3) |

A ten-fold band on year-3 revenue is not a forecast and the study does not pretend it is.
It is an honest measurement of what a mechanical method knows about a company that
replaced its plant, floated its currency and tripled its output inside the record. The
study carries the bands into Appendix A as ranges and says in §7 that the far years
support a range and never a point.

## 8 · Guidance, scored and never consumed

The company's own budget column in the 9M FY2025/26 interim against the outturn: revenue
−2.2%, cost of sales +13.1%, gross profit −22.7%, profit before tax +87.8%, net +92.3%
(budget/actual − 1). Management budgeted the operating line conservatively and the profit
line optimistically — the currency line (−1,072m) was not in the budget. Consumed by no driver.

## 9 · Caveats, stated rather than implied

- **Everything above is provisional under [R-LESSON-01].** Fifty-five cells, thirteen
  origins, one company.
- **The record spans two businesses.** The era split is drawn at the plant replacement and
  the by-era table is reported; a bias that held its sign across all three eras (revenue,
  cost of sales, debit interest, profit before tax, net) did so with magnitudes that differ
  by a factor of three or more.
- **FY2014 is partial and four years are comparatives.** Stated in B-4/B-6; no cell was
  estimated.
- **No cost-by-nature driver, no volume driver before FY2023.** The notes as extracted do
  not foot (B-7); tonnes are disclosed only in the auditor's tables from FY2023.
- **The currency finding (F1) is an accounting-policy finding, not a company finding.**
  Any issuer capitalising borrowing costs on a qualifying asset will show it; whether that
  is a class is proposed in the report and decided by nobody here.
- **The 9M FY2026 auditor's flags are on the record**: an ABUK stake not re-marked
  (+112m unbooked), an 11.6kt Damietta stock overstatement (116m), electricity invoices not
  issued since October 2025 (49.7m accrued), and KIMA-2 loan interest under-booked by 27.6m.
