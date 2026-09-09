# PHAR — valuation gap review, 9 September 2026

**AUDITED CENTRAL: 88.5201** — Frame A, provision charge permanent at 5.25% of revenue
**AUDITED CENTRAL: 106.6812** — Frame B, provision charge normalising to 2.5% of revenue

Two-sided; **every** branch is audited here, because a review naming one of two answers has
audited half the study.

**AUDITED GAPS: −30.8% (Frame A) · −16.6% (Frame B)** against 128.00, the latest known
close (6 September 2026). Frame A still breaches the ten per cent trigger and the study
stays HELD; Frame B is inside 20%.

**THIS EDITION SUPERSEDES THE REVIEW OF 8 SEPTEMBER, which audited 31.3738 and 47.6035 at
−75.5% and −62.9%.** One correction landed between them and it is the largest single move
this study has ever taken: **+57.22 on Frame A and +59.18 on Frame B.**

## What moved, and why it is a correction rather than a view

**The domestic realised price per pack was a TYPED path that contradicted this study in
both of its own records.** It read [5.0, 8.0, 7.5, 6.5, 5.5]% against a house CPI ladder of
[16, 12, 9, 7.5, 7]% — a real price cut of **15.9% compounding over five years, and 9.5%
in the first year alone**, which is a larger real cut than this company has ever been
observed to take.

Three things in this study said it did the opposite:

1. **The input's own source string**: "the path assumes price growth tracks domestic
   inflation as it converges on the central bank's target, **with no real price gain**".
2. **The committed macro record**: `esc_domestic_cpi` is "the house calendar ladder
   exactly, **at zero real**: this study carries no inflation rate of its own".
3. **[R-MACRO-01]**, which line 34 of `compute.py` imports the house path under, in those
   words — "the house path, never a typed rate".

The rule had been applied to the escalators and not to the price they escalate. That is
the same rule and the harder half of it, and nothing in the study argued for the typed
path; it simply sat there while three records said something else.

**It is corrected in the generator and the retired path is published as the contested
alternative**, computed through `dcf_at()` — the same function the headline uses — so the
difference measures the CHOICE and not the construction. Both branches are re-priced on
it, because a two-sided answer whose halves are built differently is not a pair.

**A REAL LAG IS REAL AND ITS SIZE IS NOT EVIDENCED.** The Egyptian Drug Authority sets
medicine prices in periodic approved adjustments, and realised price per pack rose 12.59%
in FY2025 — one observation of a lag. A lag observed once is not a lag that compounds for
ever, and no filing supports the −15.9% size. What would settle it is named rather than
left open: a disclosed EDA price-approval schedule, or an FY2026 filing carrying domestic
revenue per pack.

**THE DIRECTION IS NOT THE REASON.** This correction moves the answer toward the price.
The associates finding below moves it away by 12.29 and is recorded identically; ELEC's
four independent defects, found in the same pass tonight, every one widen that study's
gap and were made anyway. A correction is not more welcome for closing a gap
[R-GAP-04].

## What the correction also fixed, without being aimed at it

- **Terminal return on invested capital reads 19.17% on Frame A against 12.73% before**,
  and the terminal cost of capital is 15.22%. The study previously reinvested into a
  terminal return BELOW its own cost of capital — a symptom of the price path, not an
  independent defect, and it cleared when the cause did.
- **More volume no longer destroys value.** Under the retired path, +4pp a year of
  domestic pack growth added EGP 2,396mn of FY2030 revenue and EGP 79mn of FY2030 EBIT —
  a 3.3% incremental margin against filed EBIT margins of 23.50 / 20.14 / 25.06%. That is
  the margin-as-output test failing, and it failed because the price path drove the
  terminal margin toward zero by construction.

## The residual, and it is now a small, observable number

The base build charges the new biosimilars facility's depreciation and its interest — both
mechanical consequences of the company's own disclosed December-2025 licensing — and
carries **no revenue line for it**, because the company has published no volume, price or
utilisation guidance.

Solving the study's own model for the market price: the plant must reach **EGP 3,774mn of
revenue by FY2030E at a 45% contribution margin**, phased 0/10/30/60/100% and charged
capex and working capital on the existing business's own ratios. That is about **USD 54
million a year — an asset turn of 0.54x on the USD 100 million the company says it
invested.** Against the retired price path the same hurdle was USD 133mn, a turn of 1.33x.

**0.54x is not a heroic belief about a licensed biosimilars plant, and it is testable
against the first year the company discloses biosimilar revenue.**

## Headings 1-8

1. **LATEST FILINGS** — unchanged. Q1-2026 reviewed is the most recent period consumed;
   its PDF is image-only, so its ECL and associate notes have not been re-read from
   source. Named, not cleared.
2. **BASE YEAR** — unchanged and unaffected. Nothing annualised, scaled or solved.
3. **MACRO COHERENCE** — **this is the heading that moved, and it moved into compliance.**
   The study now carries no price path of its own; it carries the house ladder at a stated
   real drift of zero.
4. **DISCOUNT RATE** — unchanged. Country risk enters once. The 90% interval on the
   conforming beta runs 0.443 to 0.889 and the value is materially sensitive across it;
   the point estimate is used and the interval published beside it.
5. **TERMINAL** — improved as a consequence, per above. The maintenance age remains the
   open item: depreciable cost over the charge implies a 28.28-year life against a
   13.80-year disclosed class life, 105% apart, so the charge is not cost-over-life and
   the age cannot be read off it either way. Worth −13.85 at the implied life, +5.08 at an
   age of 3.0. **Unresolved and named.**
6. **BALANCE SHEET** — **the 8-September defence of the mixed dating FAILS its own test
   and is withdrawn.** It said bridging on the 31-March sheet would double-charge the Q1
   outflow. But the model's FY2026 CLOSING net debt is 9,066.4 against an actual
   31-March-2026 net debt of **9,065.2** — the forecast takes a full year to reach where
   the company already stood after one quarter, in a quarter that also paid the dividend.
   The December bridge UNDER-charges rather than avoiding a double charge. Worth −7.33,
   not the −10.08 the earlier review stated, because that figure was the raw
   1,700.9/168.756 and ignored the discount-rate feedback the model itself produces.
   **Not corrected in this pass** and now the sharpest open item in the file.
7. **CLAIMS AGAINST THE RECORD** — the associates remain carried at 11x normalised
   earnings plus the active-ingredient plant at cost, EGP 2,978.5mn against a 31-March
   carrying value of 904.361. [R-BRIDGE-01] admits market-if-listed or book and this is
   neither. Note 8.2 makes the rule's answer a **split**: Al-Batterjee (Saudi, unlisted,
   30%) at book 105.8, **MUP (LISTED, 10%) at market**, Arab API at book 29.7 — and the
   study read neither basis. **MUP is not in `engine/raw_ohlc/EG/`, so the market value
   the rule requires cannot be produced from this repository.** Worth −12.29 at the whole
   line's carrying value. Unresolved; the missing price series is the blocker and it is
   nameable work.
8. **MULTIPLE CROSS-CHECK** — at 88.52 Frame A implies 10.4x trailing FY2025 attributable
   earnings against 3.67x before, and the three cross-check lenses (book 73.22, relative
   56.67, normalised 74.70) now bracket rather than sit far above the cash-flow read. The
   field across all five readings runs 56.67 to 106.68.

## Direction count [R-ENF-05]

Twenty judgements priced, **ten up and ten down** — no whole-file sign-test failure. But
the split is STRUCTURAL and the sign test cannot see it: every *ratio* judgement
(marketing, general and administrative, inventory days, receivable days, payable days,
capex) is resolved generously, summing −16.4, and every *price and escalator* judgement is
resolved severely, summing +70.3. **The unanimity is inside the price lines.** That is
recorded here because a category-level lean is invisible to a test run across the file,
and it is what a whole-file p-value of 1.00 would have concealed.
