# ELEC — gap review [R-GAP-01]

**AUDITED CENTRAL: 0.3357**
**AUDITED GAP: -83.9%**

EGP 0.3357 a share against the latest known close of **EGP 2.08 on 3 September 2026** —
83.9% below, the largest gap in the book. It was struck at EGP 2.19 on 5 August, where it
sat 84.7% below.

Written because the answer was invisible: the study carried its spot at the top level and
its central at `lenses.central.base`, so the shared reader could see neither pair and **the
largest disagreement this house holds went unaudited for a month.**

**The verdict is that the gap is OURS, and the finding is worse than a mispricing: the
published number is not a valuation at all.** Two of the four lenses are pinned at floors,
they carry 60% of the weight and produce 4.2% of the answer, and sixteen of the nineteen
corrections priced below move the published central by **exactly zero** because the lens
they act on never leaves its clamp. Beneath the clamp the honest read is **−0.71 a share**.
The reverse read lands on a margin the company printed in all three filed years, which under
[R-GAP-02] is evidence *against* dissent. **The study is correctly HELD and it should not be
repaired**, because every input beneath it is a vendor print or a house solve.

---

## The clamp, which comes before the eight headings because it decides them

`compute.py:389` and `:493`:

```
eq_dcf = max(eq_dcf_unfloored, 0.0)        # enterprise 3,813 less net debt 9,805 = -5,992
dcf_ps = max(eq_dcf / SH, 0.01)
rel    = {tag: max((m * ebitda_27 * (1 + s) - nd_fy26) / SH, 0.05) for ...}
```

| lens | what it computes | what it publishes |
|---|---:|---:|
| cash flow, base | −1.8082 | **0.01** |
| cash flow, bear | −3.2531 | **0.01** |
| relative, bear (4.5×) | −2.2791 | **0.05** |
| relative, base (5.5×) | −1.5196 | **0.05** |
| relative, bull (6.5×) | −0.5661 | **0.05** |

The blend at 0.4 / 0.2 / 0.2 / 0.2 gives 0.4(0.01) + 0.2(0.05) + 0.2(0.6994) + 0.2(0.9092)
= **0.3357**. Unfloored the same blend is **−0.7055**, so **the floors are worth +1.0412 a
share, 310% of the published central.**

Three consequences. **The published bear equals the published base** (both 0.01) because
both are clamped, so the stated "range 0.18–0.95" is a range of two clamps against two
unclamped lenses. **The study's entire published sensitivity grid on its primary lens is
negative in all twenty-five cells** (−3.257 to −0.359) — it moves a number that never leaves
the floor. And **correcting the clamp moves the answer AWAY from the price**: the clamp is
not why this study is pessimistic, it is why it looks less pessimistic than its own model.

**The two surviving lenses contradict the model's own forecast, both upward.** The
normalised lens (20% of the weight, 42% of the central) uses a typed mid-cycle net debt of
6,000 where the study's own forecast debt schedule prints **16,045** for the same year; on
the model's own number that lens is **−1.59**, not +0.70 — worth −0.458 of the central. The
book lens capitalises FY2025 equity of 4,100 while the model's own equity roll runs 4,100 →
2,227 → 956 → −203 → −1,210 → −2,078, and the study's own Appendix A says so: "book equity
erodes toward zero by FY29–30E." Made internally consistent, the central is **−0.1224**.

---

## 1. LATEST FILINGS

The model consumes FY2023, FY2024 and FY2025 annual figures and the first quarter of 2026
(31 March, press-carried). **The half-year 2026 statements were due in mid-August and are
not in the model** — the study names the gap itself: *"the H1-2026 statements (due ~mid-Aug)
are the first checkpoint on that ramp."* Also unconsumed although held in the study's own
research file: **the first half of 2025** (revenue 6,438, net profit 486.4), **FY2022** and
**FY2021**.

## 2. BASE YEAR

**It does not foot to any filed period.** FY2025 revenue and net profit are press figures;
**everything between them — EBITDA, operating profit, depreciation, finance cost — is solved
or typed.** FY2023 is the same. Only FY2024 EBITDA and operating profit come from
aggregators, and from two different ones. The FY2026 forecast is +21.5% on revenue and about
3.9 times the first quarter's annualised EBITDA, which the study states honestly.

**The FY2025 anchor the whole forecast is calibrated against is a plug.** The study's own
flag says the first quarter of 2026 implies about 243 a quarter below the operating line
(about 972 a year) on a *higher* debt base — an effective rate near 10% against the 23.2%
assumed:

| assumed finance cost | FY2025 EBITDA | margin | conversion EBITDA per tonne |
|---:|---:|---:|---:|
| 972 (first-quarter implied) | 1,694 | 15.65% | 107.5k |
| 1,500 | 2,222 | 20.53% | 141.0k |
| **2,150 (adopted)** | **2,871** | **26.54%** | **182.2k** |
| 2,600 | 3,322 | 30.70% | 210.8k |

**The "FY2025 conversion EBITDA of 183k per tonne, copper-gain inflated" anchor — the
study's own evidence for a windfall — moves 40% on an input nothing sources.**

## 3. MACRO COHERENCE

**Three clocks in one model, and it fails [R-MACRO-01] on a quantity rather than on a
declaration.** The house Egyptian path, read live as of 2 September: ladder
16 / 12 / 9 / 7.5 / 7, terminal inflation 7.0%, **terminal risk-free 12.50% DERIVED**,
derived currency 55.11 → 70.11.

The study **carries its own inflation number**: a terminal risk-free of 10.5%, being *"the
central bank's Q4-2028 target of 5% plus 5.5 points"* — against a house terminal of 7% and
12.5%. Worth **−0.13** a share corrected. Terminal growth of 5% nominal against a house
terminal inflation of 7% is **−1.87% real in perpetuity**, stated nowhere; worth **−0.32**
corrected. The currency escalates at **3% a year** against the house purchasing-power path
of 13.2 / 9.3 / 6.3 / 4.9 / 4.4%.

**And the structural one: revenue is fully copper-and-currency linked while EBITDA per tonne
is typed in nominal pounds.** So a stronger copper price inflates revenue *and* the working
capital charged against free cash flow, and adds **nothing** to EBITDA — copper is pure
value destruction in this model by construction, and it is anchored at the top of the tape
(USD 14,000 against the FY2025 realised USD 10,000). At the realised level the cash-flow
lens is worth **+1.39** a share.

The study's own terminal-growth reconciliation states plainly that FY2023 and FY2024 are
excluded as burst years and *"no clean stable year exists in the disclosed record"* — so the
return-and-reinvestment identity is checked against nothing.

## 4. DISCOUNT RATE

**The shape conforms and the discount rate cannot be the explanation.** The schedule is a
real glide from 21.53% to 15.00% with fractions taken from the cost-of-debt path — which is
what [R-COC-01] requires of a transition market — and country risk is counted once
(normalised 22.31 − 3.40 = 18.91).

Two defects, both small. **The cost of debt of 22.00% sits 100bp BELOW its own sovereign of
23.00%**, which [R-COC-01] refuses outright; worth −0.03. And the weights use **gross** debt
of 10,465 while the bridge deducts **net** 9,805; worth about zero.

**At a terminal risk-free of ZERO the equity is still negative.** No cost-of-capital
correction reaches the price.

## 5. TERMINAL

**The retired reinvestment identity, and it was invisible to the gate built to find it until
tonight.** `compute.py:366-372` builds terminal value as profit × (1+g) × (1 − g/return) /
(rate − growth), with a terminal return on capital of **9.17% against a terminal cost of
capital of 15.00%** — a spread of −583bp — and **54.5% of terminal profit reinvested at that
destroying spread in perpetuity.** Terminal invested capital is working capital plus a typed
5% of revenue, 95% of it working capital.

This study was **not** on the terminal ratchet and `check_terminal_floor.py` reported "no new
terminal carries the 1/g construction" while this one did: the census could not recover the
terminal profit, so the charge was never scored and the name fell into a bucket nothing
reported. That hole is closed as of 5 September, and on the corrected census **ELEC carries
an implied replacement cycle of 20.0 years against 1/g of 20.0, charges 54.5% of terminal
profit — the heaviest charge in the book, more than double the next — and sits 28.4% BELOW
its own floor**, against the only other name below it at −7.5%.

**Correcting it moves the answer DOWN**: the sanctioned construction −0.21, and on the house
path −0.32. [R-TERM-01 CLAUSE TWO CORRECTED] working exactly as written.

## 6. BALANCE SHEET

**The bridge stands on a triangulated FY2025 sheet, not a disclosed one.** Net debt per share
is **2.96 against a price of 2.08** — the bridge is 142% of the market capitalisation — and
it rests on total assets from one aggregator less equity from another less scaled payables.
The study's own `nd_challenge` at 10,386 is worth −0.18 a share against the published 9,805.

**The 8,960 FY2024 debt anchor is quoted from the same sentence the study itself declares
ambiguous**: *"obtained credit facilities of EGP 10.9bn during 2025 vs 8.96bn in 2024"*. The
study correctly refuses to read 10.9bn as drawn debt and then uses the 2024 comparative of
the identical quantity as a hard drawn-debt anchor. Working capital at **113% of revenue** is
a derivation, not a disclosure.

## 7. CLAIMS AGAINST THE RECORD

**Two fail.**

*"The terminal 12.3% matches the pre-windfall 2022 norm (about 12%)."* **The study holds no
FY2022 income statement anywhere.** The phrase occurs exactly twice — in a source note and
in the delivered document. Its own research file *does* hold FY2022 revenue of 5,699 and net
profit of 542.2; reconstructed from those, the FY2022 EBITDA margin comes out at **15–21%,
not 12%**. **The single number driving 82% of enterprise value is justified against a year
the model never opened.**

*"The price still pays for devaluation-era earnings the company itself is no longer
printing"* and *"FY2023–24 were windfall years."* Net margins from the study's own research
file: FY2021 **8.44%**, FY2022 **9.51%**, FY2023 14.39%, FY2024 **9.64%**, FY2025 4.62%.
**FY2024 — named as a windfall year — printed the pre-devaluation norm.** Only FY2023 is
elevated.

**And a hard internal contradiction nobody put side by side.** The copper uplift factor of
1.387 encodes copper at 72.1% of the cable price. Then:

| year | EBITDA margin | all non-copper cost implied |
|---|---:|---:|
| FY2023 | 30.68% | **−2.78%** — arithmetically impossible |
| FY2024 | 25.33% | 2.57% |
| FY2025 | 26.54% | 1.36% |
| FY2030 terminal | 12.30% | 15.60% — plausible |

**At that uplift the filed-era margins are impossible and only the forecast margin is
coherent**, and the model uses both: the uplift sets the revenue path and the utilisation
narrative while the margins set the windfall narrative. The tonnage build is also **not
identified** — only volume × uplift is pinned by revenue — so at an uplift of 2.0, FY2024 is
16.6kt and 66% utilisation, not 96%, with the margin unchanged. The "96% of capacity,
VALIDATION not calibration" claim is circular, and against a capacity the study itself says
is parent-only.

## 8. MULTIPLE CROSS-CHECK

At the published 0.3357 the implied enterprise value is 10,917 = **10.2× FY2027 EBITDA** —
*above* the study's own justified 5.5× and above the sector comparator's 7.05×. The
cash-flow lens at 0.01 implies **9.2×**. **The valuation is not cheap on its own multiple;
the multiple is high because net debt swamps it.** At the market's 2.08 the enterprise value
is 16,697 = **15.6×** the study's FY2027 EBITDA — but **7.6×** the same year's EBITDA at the
lowest filed margin, which is the comparator's own multiple. The cross-check independently
confirms that the entire gap is one number.

---

## What the price implies under this study's own drivers

At 2.08 the market pays an enterprise value of 16,697 against the model's 3,813 — it must
find **12,884** more. Solved one driver at a time:

- **conversion EBITDA per tonne × 2.208 → a terminal EBITDA margin of 27.17%.** The company's
  own filed record is **30.68% / 25.33% / 26.54%**. **The reverse read lands inside the filed
  range on all three years.**
- working capital — **unreachable** at any intensity down to 5% of revenue.
- terminal growth — **unreachable** at any growth below the terminal cost of capital.
- discount rate — **unreachable even at a terminal risk-free of zero.**
- net debt — the price needs **net cash of 3,079** against a published net debt of 9,805.

**Only one door opens, and behind it is the company's own filed margin.** The study's own
bull column (×1.30 → 15.99%) never reaches any year the company has printed. [R-GAP-02] is
explicit: a reverse read landing on a believable number is evidence against the dissent.

## The corrections, priced

Each moved alone. `cash flow` is the unfloored lens — the only responsive number; `Δcentral`
is the effect on the published 0.3357.

| # | correction | cash flow / sh | Δ central |
|---:|---|---:|---:|
| 1 | **terminal margin at FY2025's filed 26.54%** | **+1.92** | +0.889 |
| 2 | **terminal margin at FY2024's filed 25.33%, the lowest filed** | **+1.60** | +0.725 |
| 3 | **the two lens floors removed** | −1.81 | **−1.041** |
| 4 | normalised lens on the model's own FY2028 net debt | — | −0.458 |
| 5 | copper at the FY2025 realised USD 10,000/t | −0.42 | 0 |
| 6 | terminal with no growth charge at all (a bound) | −0.68 | 0 |
| 7 | working capital at 60% of revenue | −0.68 | 0 |
| 8 | working capital at 40% (an ordinary manufacturer) | +0.12 | +0.046 |
| 9–14 | copper at −10%, FY2024 net debt, FY2024 working capital, the NOPAT-perpetuity floor, depreciation at 50 rather than 90, the unverified net debt | −1.3 to −2.0 | 0 |
| 15 | cost of debt 22.0% → 25.5% ([R-COC-01]) | −1.84 | 0 |
| 16 | terminal risk-free 10.5% → the house 12.5% | −1.93 | 0 |
| 17 | the sanctioned terminal on the house path ([R-TERM-01]) | −2.13 | 0 |
| 18 | growth 5% → 7% nominal (house, zero real) | −2.13 | 0 |
| 19 | the house currency path, spread on the same clock | −2.13 | 0 |
| 20 | **all house-standard corrections at once** | **−2.54** | 0 |

**One candidate closes the gap and it is the margin path.** Everything else — the terminal
construction, terminal growth, the terminal rate, the currency, the cost of debt, net debt,
the entire [R-TERM-01] / [R-MACRO-01] / [R-COC-01] correction set — is worth **−0.73 a share
in total and moves the answer FURTHER from the price.** Bringing this study to house
standard makes it *more* extreme.

**Direction of the contested judgements.** The study commits no reverse read and no sign test
— it is on the [R-ENF-05] ratchet — so this count is the reviewer's: **10 resolved toward a
lower value and 5 toward a higher one, n = 15, two-sided p = 0.302.** Not unanimous, and the
count is what matters: **the split is structural rather than balanced.** Every downward
judgement sits in the cash-flow model, which is clamped away; every upward one sits in the
terminal, the currency or one of the two lenses that survive the clamp. **The published
central therefore carries only the upward ones.**

## What runs the study's way, reported fairly

The first quarter of 2026 was genuinely bad — revenue −44%, gross margin 5.7% against 33.1%,
operating profit EGP 1.4mn, a net loss of 241.6. FY2025 revenue fell 21.5% and net profit
62%, with no dividend. Total assets rose 9.9% while revenue fell 21.5%, so working capital
really did swell. The controlling group is reported selling at EGP 2.00–2.21 through 2026. A
cable maker at 22% money with net debt at 91% of revenue is genuinely fragile. **None of that
is priced away by anything above** — and none of it establishes a 12.3% mid-cycle EBITDA
margin, which is the whole answer.

## The sourcing, which is why this does not get repaired

`ELEC-primary-financial-statements` in the escalation register records the position and it
holds on re-probing: the 2021–2025 statement files all return 404 on the live host and the
2015–2020 links point at a host that does not resolve.

**One fact the register did not carry, from enumerating the archive rather than counting
it**: it lists **no FY2025 annual, no first quarter of 2026 and no half year of 2026 at
all**, and every statement listed from 2021 onward is **STANDALONE**. **The last CONSOLIDATED
statement this company published is 31 December 2020**, and every income and balance-sheet
figure this study uses is consolidated. **The issuer has served no consolidated statement in
six years.**

What that leaves the model standing on: equity FY2024 = 3,600 from a retail data site,
driving net debt one-for-one (±1,000 is worth ∓0.30 a share); total assets FY2025 = 16,460
from an aggregator, driving net debt *and* working capital together; operating profit FY2024
= 3,400 from the same retail site, quoted to two significant figures; EBITDA FY2024 = 3,490
from a third source — so **depreciation of 90 is the difference of two figures from two
different aggregators**, and at 3.35 or 3.44 under the same rounding it would be 140 or 50
(±0.10 a share). That 90 is the sole basis for the property estimate, the depreciation ratio,
the "light fixed-asset base" claim and the terminal's typed 5% of revenue.

## Conclusion

**Do not repair this study.** Its central is an artefact of two clamps; its most consequential
driver is justified against a year it holds no data for; its two calibrations — the copper
uplift and the filed margins — cannot both be true; and every historical figure is a vendor
print or a house solve on one, against an issuer that has published no consolidated statement
since 2020. **That is a SIGCM clause 1 condition, not a valuation disagreement.**

The escalation's standing default — withdraw from coverage rather than re-issue on aggregator
data — is the right one, and today's probe strengthens it: the archive lists nothing after
30 September 2025 and nothing consolidated after 31 December 2020.

**The 83.9% is ours, and it is not a claim about the world that this house is currently in a
position to make.**
