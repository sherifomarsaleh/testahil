# Answer challenges — ELEC, EGCH, SWDY, PHAR, 9 September 2026

**Internal. Nothing here is published, no fair value has been moved, and no study is
rebuilt on it yet.** Each name was interrogated from outside its own study under
`[R-GAP-01]`, with one standing instruction: **hunt OUR defect and price it; never propose
moving a fair value toward the price.** Where a correction points AWAY from the market it
is priced exactly as hard — that discipline is the whole point and it is visible below.

Recorded here because an answer that lives only in a session binds nothing: the container
is rebuilt from the repository and the next session cannot see the chat.

---

## ELEC — the published number is almost entirely floors

**Central 0.3357 against 2.12 (−84.2%), the widest in the book.**

The cash-flow lens contributes **1.2%** of the published answer. The model says −1.8054 and
`eq_dcf = max(eq_dcf_unfloored, 0.0)` / `dcf_ps = max(..., 0.01)` pin it at 0.01. The
unfloored central is **−0.7043**, and the published figure is invariant to the price
because two of four lenses are flat. The floors are worth **+1.0401**, or 310% of the
published central.

**THE QUARTERLY RECORD FALSIFIES THE STUDY'S STATED MECHANISM.** The 4.09% FY26E margin is
justified as under-absorption at ~42% utilisation. But Q3-25 and Q4-25 ran **28.8%** and
**23.3%** EBITDA margins at revenue *below* the study's own FY26E quarterly rate. Lower
volume, much higher margin — so under-absorption cannot be what happened. This is new and
it comes from the Quarterly tab the principal supplied on 09-09-2026.

| margin basis | FY26E EBITDA | central | vs 2.12 |
|---|---:|---:|---:|
| four calendar-2025 quarters, 26.49% | 2,696 | **2.4907** | +17.5% |
| LTM to Q1-26, 18.99% | 1,933 | 0.9841 | −53.6% |
| as published, struck off Q1-26, 4.09% | 416 | 0.3357 | −84.2% |
| Q1-26 alone, 0.74% | 75 | −0.1015 | −104.8% |

**Swing between the two brackets: EGP 2.59 — 7.7x the entire published fair value.**
Both sides belong in the contested register, priced, neither averaged.

Defects independent of that judgement, all of which move the answer FURTHER from the price:

| candidate | file | worth |
|---|---|---|
| normalised lens uses a TYPED net debt of 6,000 against the model's own FY28 16,045 | `compute.py:517` | **−0.4581** |
| book lens uses 4,100 against the model's own FY30 equity of −2,078 | `compute.py:525` | **−0.2740** |
| beta regressed on a 30-name equal-weight COMPOSITE — SIGCM clause 6 hard fail | `compute.py:217` | −0.0570 at CI top |
| D&A of 90mn is the DIFFERENCE OF TWO DIFFERENT VENDORS (Investing 3,490 − SWS 3,400); the same vendor's own record gives 46.13 and the accumulated-depreciation roll 47.84 | `compute.py:118` | +0.0876 |
| terminal WC intensity 88% of revenue vs a filed five-year median of 69.3% | `compute.py:196` | +0.3018 |

**Standalone vs consolidated, in three places** — including the ~42% utilisation that
anchors the FY26 margin: `capacity_kt = 25.0` is parent-only Mostorod, divided into
consolidated revenue. The 12.30% terminal margin is defended against a filed range that is
**standalone FY2020-23**, where the consolidated/standalone operating-profit wedge is
34.49x.

Everything except the margin, moved together: central **0.3489**, still −83.5%.
**No non-margin candidate closes any of the gap; the honest corrections widen it.**

---

## EGCH — no single line closes it, and two provenance defects carry 73.5% of EV

**Two-sided: 4.0396 / 8.0388 against 14.23 (−71.6% / −43.5%).**

Worked backwards, the price needs **EV +139.4%**, or a terminal 2.90x the study's. The
largest single priceable line is +2.683 — 26.3% of the gap. **Five lines reach 9.22 and
seven cross 14.23.** No single line does it.

| # | candidate | file | worth |
|---|---|---|---|
| 1 | **10% export duty carried for ever with NO filing behind it.** The two sibling policy inputs beside it cite "decree 241 of 2021" and "Cabinet decision 170 of 24 Nov 2021"; this one traces to press only. **Not in the study's 17-judgement contested table.** | `inputs.py:338` | **+2.683** |
| 2 | The stopped branch writes off EGP 5,653.5mn of CWIP at 100% while the same study's asset lens carries it at 60% | `compute.py:696,710-736` | **+1.708** on the stopped branch |
| 3 | Terminal prices the new complex's nitrate at a typed US$280/t on a FOUR-WORD source — the shortest in a 304-input register — while the same model prices the company's own granulated nitrate at EGP 20,000/t = US$408/t. Same product, 31% apart, terminal takes the lower. The study wrote 30 lines closing exactly this defect class for UREA and did not carry it across | `inputs.py:388` vs `706` | +0.487 |
| 4 | The five upward alternatives the study priced and declined are JOINTLY worth 15% more than their sum (volume x price x cost compound; equity is geared 2.4x to EV) | `alternatives.py` | +5.175 jointly vs +4.488 read off the table |
| 5 | **The base year is INERT.** `fy2526` is built, committed, and read by `build()`, `terminal()` and `bridge()` NEVER. Re-run at 0%, 3%, 15% and 50% haircuts the answer is identical to four decimals. The delivered document and the 5-Sep review both present it as carrying the model | `compute.py:423-443,887` | **0.000** |

**The sharpest sentence about this gap, which no review has said:** the study's OWN
relative-multiples lens lands at **EGP 15.99 — above the market price** — and the market's
implied EV of 38,659 sits within **1.1%** of that lens's own mid of 38,255. The price is
paying the Egyptian peer median on forward EBITDA, a number that prices neither the EGP
14.7bn still to be spent nor a perpetual maintenance charge 35% above book depreciation.

Priced and REJECTED as gap-closers: the terminal asset age across its whole defensible
range (a brand-new base still leaves −64.4%); the bridge (bounded at ±0.11); terminal
growth (7% is already the value-maximising point); the discount rate (the price implies
13.0% against a 23.0% sovereign). The capex-to-volume test **corroborates** the study —
the programme is expensive because note 18-3 says so, at US$1,548 per annual tonne against
a greenfield range of US$550-700.

**The binary framing is not robust.** Resolving three ANNA inputs the other way takes the
carried-through branch to 9.514, ABOVE the stopped branch's 8.039 — the headline finding
"stopping is worth more than finishing" flips on three constructed numbers, one of which
has a four-word source.

---

## SWDY — the gap stands, and two delivered sentences are false

**Central 43.5108 against 136.20 (−68.1%).** No candidate closes it; the whole defensible
set closes **18%**, leaving EGP 74.85 a share unexplained.

**TWO FALSE STATEMENTS IN THE DELIVERED STUDY, both correcting my own earlier account:**

1. **The employees' statutory share is NOT an upper bound and the cap cannot bind.** The
   study says "the statutory share is capped at total annual wages, headroom not
   disclosed". **The headroom IS disclosed, in the same audited FY2025 statements**: notes
   6-1-1, 7 and 8 print salaries of 12,646.9 + 1,588.1 + 4,670.8 = **EGP 18,905.8mn**
   against an employees' share of 2,073.1mn — **9.12x headroom** (FY2024: 6.30x). Worth
   **exactly zero**, not the EGP 6.30 the "upper bound" framing implies.
2. **The Constructions backlog IS disclosed.** The driver's source string says "No order
   book or backlog figure is disclosed in any of the audited filings or the Q1-2026
   interim" — true of the audited filings, **false of the issuer**. Six quarterly earnings
   releases in the study's OWN `engine/swdy_walkforward/filings/` disclose the E&C backlog:
   **196bn (Dec-24) → 261 → 276 → 293 (Dec-25) → 307 → 346bn (Jun-26)**, wires and cables
   43.5bn, meters 8.8bn. Verified directly from `2026Q2__Elsewedy-Electric-ER-2Q2026-E-v2.pdf`.
   Worth ±0.16 a share — reported anyway, because a study that says a number does not exist
   when it does has a hole in its sweep whatever the number turns out to be worth.

| candidate | file | worth |
|---|---|---|
| capex path against the H1-2026 print (capex +0.9% while revenue rose 31.9%; the model charges 23% above the company's own half) | `compute.py:676` | **+2.19 to +5.71** |
| FY2026 segment mix on each segment's OWN seasonality — group revenue unchanged, so pure mix; the model over-weights the 11.4%-margin segment | `compute.py:547,587,607` | **+3.19** |
| associates at book 6,758 while note 20 shows them earning 1,568.9 — a 23.2% return on that book | `compute.py:1408` | **+3.17 to +3.26** |
| terminal risk-free 10.50% vs the house-derived 12.50% (a recorded, ratcheted failure — the study is already generous here) | `compute.py:761` | −7.66 |
| **the Constructions taper** — priced across 8% flat to a backlog-led 27.4/24/20/16/13% | `compute.py:587` | **±0.16, i.e. 0.17% of the gap** |

That last row matters: at a 9.0% segment margin against 19.9% working capital and 3-4%
capex, incremental Constructions revenue is FCFF-neutral. **The claim that the whole
forecast rests on the taper is false, and the model says so.**

**The reverse read:** 136.20 requires a terminal cost of capital of 10.76%, from a terminal
risk-free of **2.90% in Egyptian pounds** against 7.00% terminal inflation — a real
risk-free of **−3.83% in perpetuity**, 19.4 points below the observed 10-year EGP
government yield. Or every segment margin x1.685: a 17.2% group operating margin for ever
against an all-time high of 12.65%. Not a belief; an impossibility.

Direction count: **6 up, 7 down. This study is not leaning.**

---

## PHAR — the largest item contradicts its own source string

**Two-sided: Frame A 31.2977 (−75.5%), Frame B 47.5063 (−62.9%) against 128.00.**

| # | candidate | file | Δ Frame A | dir |
|---|---|---|---|---|
| 1 | **The domestic price escalator (5.0/8.0/7.5/6.5/5.5) contradicts its OWN committed source string**, which says "price growth tracks domestic inflation… with no real price gain". The house CPI ladder is 16/12/9/7.5/7. That is a **−15.9% real price cut, compounding, permanent** — it sets the terminal margin | `compute.py:522` | **+57.22** | UP |
| 2 | Frame A's 5.25% is a COMPLETED programme carried for ever. FY2024 note 10: allowance 128.0→708.0 with **"Used: —"**; Q1-2026 charged **zero** ECL. The study holds only the three P&L charges, never the allowance balance, gross AR, or the write-off column | `compute.py:599,410-416` | +14.45 to +19.82 | UP |
| 3 | Terminal debt weight taken on today's market cap, not the forecast sheet (25.5% vs 47.9%) | `compute.py:925` | +14.42 | UP |
| 4 | **Associates.** [R-BRIDGE-01] admits market-if-listed, book otherwise, and nothing else. Note 8.2: Al-Batterjee (Saudi, **unlisted**, 30%) 105.8, MUP (**LISTED**, 10%) 329.8, Arab API 29.7. The rule's answer is a SPLIT — book for two, **market for MUP** — and the study read neither. The Saudi stake supplying 84% of the capitalised stream is carried at 105.8 | `compute.py:970,981,783` | **−12.29** | **DOWN** |
| 5 | Export price +1.0%/yr in USD against the **2.5% US inflation the same model's own PPP fx path is derived from** | `compute.py:530` | +11.47 | UP |
| 6 | Working-capital days assumed to IMPROVE vs holding FY2025 filed levels | `compute.py:639-650` | −9.79 | DOWN |
| 7 | Bridge on 31-Dec-2025 rather than the disclosed 31-Mar-2026 sheet | `compute.py:1355,1438` | −7.33 | DOWN |

**The 08-Sep review's mixed-dating defence FAILS its own test.** It says bridging on March
would double-charge the Q1 outflow. But the model's FY2026 closing net debt is **9,066.4
against an actual 31-March-2026 net debt of 9,065.2** — the forecast takes a full year to
reach where the company already stood after one quarter, in a quarter that also paid the
dividend. **The December bridge under-charges rather than avoids a double charge.** The
review's own price for the move, "EGP 10.08 a share", is the raw 1,700.9/168.756 and
ignores the discount-rate feedback its own model produces; measured, it is **7.33**.

**More volume DESTROYS value in this model:** +4pp/yr of domestic pack growth lifts FY2030
revenue by 2,396mn and FY2030 EBIT by **79mn — a 3.3% incremental margin** against filed
EBIT margins of 23.50 / 20.14 / 25.06%. Frame A falls 6.82. That is the margin-as-output
test failing, and it is caused by item 1.

Direction count: **10 up, 10 down — no sign-test failure.** But the split is STRUCTURAL:
every *ratio* judgement is resolved generously (sum −16.4) and every *price and escalator*
judgement severely (sum +70.3). **The unanimity is inside the price lines, not across the
file** — which a whole-file sign test cannot see.

Two things that could not be closed: the Q1-2026 PDF is image-only, so its ECL and
associate notes were not re-read from source; and MUP is not in `engine/raw_ohlc/EG/`, so
the market value [R-BRIDGE-01] requires for the listed associate cannot be produced from
this repository.

---

## What is owed

Nothing above is applied. In priority order, and each to be fixed IN THE GENERATOR:

1. **PHAR item 1** — a committed number contradicting its own committed source string is
   not a judgement call. The study's own `forecast_anchor` record already says so in as
   many words. Resolve it one way or the other and price both.
2. **SWDY's two false sentences** — a delivered study stating that a disclosure does not
   exist when the issuer publishes it, and claiming an upper bound whose cap is disclosed
   at 9.12x headroom.
3. **ELEC's margin** — both brackets into the contested register, priced, neither averaged.
   Then the four independent defects, all of which widen the gap.
4. **EGCH's two provenance defects** — a four-word source cannot carry 73.5% of enterprise
   value, and a press report cannot carry EGP 2.68 a share.
5. **EGCH's inert base year** — either wire `fy2526` into the model or stop presenting it
   as carrying it.
