# The cash-flow lens, scored — and the answer is that five names cannot carry it

**6 September 2026.** [R-VCAL-01] series (a), score (i), on the construction sealed in
`MECHANICAL_LENS_3_06-09-2026.md` before any figure below existed. Read the numbers live
with `python3 engine/valuation_calibration/score_cashflow.py`; the committed run is
`SCORES_cashflow_06-09-2026.json`.

---

## The instruction, and the answer to it

> *When the four are in, rebuild series (a) as a real cash-flow lens on them, run the
> pre-registered score, and report the pooled interval with its LONO stability —
> whatever it says. If five names cannot carry a credible interval, say that plainly
> rather than reporting a weak one.*

**They cannot, and the reason is sharper than "too few cells".** Of 33 panel cells that
are READY — macro, as-reported statements, mechanical drivers, a price and a footed
share count all present — **the declared construction produced a value on 5, and all
five are one name.**

| | |
|---|---|
| cells with a value | **5** |
| distinct origins | 5 |
| **distinct names** | **1** (PHDC) |
| mean log(FV/P) | **+0.9842** (+167.6%) |
| median | +1.1760 (+224.1%) |
| below the price | **0 of 5** |
| block bootstrap {2,3,4} | [+0.33, +1.57] · [+0.56, +1.50] · [+0.78, +0.98] |
| **leave-one-name-out** | **without PHDC: nothing left to pool** |

**THE LEAVE-ONE-NAME-OUT LINE IS THE WHOLE RESULT.** A bootstrap interval over five
origins of one company is a statement about PHDC's own five years, and the
pre-registration says so in advance: *the effective n is about the origin count, and
every interval is read against that number rather than the cell count.* Here even that
is generous — the five origins are consecutive years of one balance sheet, and the
block bootstrap at block 4 collapses to a half-width of 0.10 precisely because there is
almost nothing left to resample.

**No pooled bias is reported, because there is nothing to pool.** Reporting +167.6%
with a confidence interval would be the precision overstatement the pre-registration
was written to prevent.

## The one thing the reading does say, and it points the other way

The five values sit **167% ABOVE** the prices they were struck at, none below. The
reassessment's founding complaint was house pessimism; this instrument, on the one name
it can compute, is wildly optimistic — **and that is a fact about the construction, not
about the house.** Every one of the five carries **102% to 125% of enterprise value in
the terminal**, which is only possible because the explicit five-year window's present
value is NEGATIVE: a developer's working capital grows with revenue, so the full growth
in working capital is charged over the window while the terminal at zero real growth
charges only inflation on it. The lens is therefore reading almost nothing but its own
terminal, and a terminal is exactly the part [R-TERM-01] says cannot be built without a
disclosed asset life — which none of these five names but one has on file.

**The sealed declaration's own ambiguity turns out not to matter.** It was published
both ways rather than resolved by choosing, and the two readings of the maintenance
figure give +0.9842 and +0.9834. The choice was worth nothing, which is worth knowing.

---

## Why 28 cells produced no value, by cause

| cells | cause | whose fault |
|---|---|---|
| **11** | the block carries fewer than three years for a trailing intensity | **the inputs** |
| 6 | terminal refused — implied payout outside [0,1] | **the module, firing on sound work** |
| 6 | terminal refused — terminal free cash flow not positive | **the construction** |
| 3 | the run projects a shorter window than the declared five years | the run |
| 1 | the projection carries no revenue or operating profit | the inputs |
| 1 | the panel carries no finance charge at the origin | the inputs |

### 11 cells: the blocks do not reach back far enough, and the shortfall is countable

This is the largest cause and it is **purely a coverage fact**. Capex is well committed
where the blocks reach — disclosed at 39 of 43 origin-years across the five, derivable
by the identity at 2 more — but a trailing three-year intensity at origin *t* needs
*t−2*, and each block begins at or after the first origin the panel declares READY:

| | first READY origin | block must start | block starts | short by |
|---|---|---|---|---|
| AMOC | 2021 | 2019 | 2021 | 2 years |
| ARCC | 2017 | 2015 | 2018 | 3 years |
| EGCH | 2013 | 2011 | 2012 | 1 year |
| PHDC | 2015 | 2013 | 2015 | 2 years |
| TMGH | 2020 | 2018 | 2020 | 2 years |

**Ten additional origin-years of valuation-input block would close all eleven cells.**
That is a finite, countable, actionable number, and it is the [R-FCAL-01 AMENDED]
general lesson arriving one layer up: *what a process commits decides what can ever be
asked of it later.* The blocks were built to cover each run's own recent origins; the
calibration asks about 2013 onward, and nobody was wrong — the question simply arrived
after the record was designed.

### 6 cells: the maintenance charge falls BELOW book depreciation — the same proxy, failing the other way

ARCC 2020–2023 and EGCH 2022–2023 are refused with *implied payout of terminal NOPAT is
102% to 665%, outside [0,1]*.

**A first reading of this section attributed the refusals to ARCC's negative working
capital, and that was wrong.** ARCC's working capital IS negative — −10.1%, −20.2%,
−12.8%, −12.6% and −4.4% of revenue in FY2018–FY2022, because a cement company collects
from customers before it pays its suppliers — but it is not what the guard is firing on.
Re-running every refused ARCC origin with working capital set to **zero** leaves the
payout at **238.9%, 172.5%, 107.0% and 101.1%**, against 264.9%, 182.3%, 110.0% and
102.0% with its own. The working capital moves it by a few points; it does not cause it.

**The cause is that maintenance at trailing capex comes out BELOW book depreciation.**
With zero real growth the module charges `fcff = nopat + dna_book − maintenance`, so the
payout exceeds one exactly when `maintenance < dna_book`. On ARCC 2020 the trailing
capex proxy gives maintenance of EGP 62.1mn against book depreciation of EGP 247.8mn;
on EGCH 2022, EGP 113.3mn against EGP 1,858mn.

**This is [R-TERM-01 CLAUSE TWO]'s inference, and the module is right to refuse: a
terminal charging less than its own book depreciation cannot be maintaining the asset
base, because book depreciation is struck on historical cost and replacement costs
more.** ARCC's own delivered study, on the **disclosed 20-year machinery life from its
audited accounting-policies note**, charges maintenance of **EGP 2,560mn a year against
book depreciation of EGP 643mn** — four times the book charge. The trailing-capex proxy
gave a figure an order of magnitude too small.

**So the proxy fails in BOTH directions and has no consistent sign:** catastrophically
too HIGH on a company mid-build (EGCH 2017–2021, capex at 2.1x–7.8x revenue), and far
too LOW on a company harvesting a built-out base whose recent capex is small against its
depreciation (ARCC, EGCH 2022–2023). That is [R-TERM-01 CLAUSE TWO CORRECTED]'s own
general lesson arriving on a new object: *where a cheap proxy is adopted because the
real calculation is expensive, the proxy is a hypothesis until the real calculation has
been run on at least one case.* It has now been run on two, and the proxy loses both.

**`terminal_value.py` is NOT changed, and the reason is not that it is right by
accident — it is right.** The refusals are the module doing the job [R-TERM-01] built it
for. What is missing is the input the rule has demanded all along: **a disclosed useful
life.**

### 6 cells: the construction's own declared bias, and it is not mild

EGCH 2017–2021 and TMGH 2022 are refused because terminal free cash flow is negative.
The declaration named this in advance — *where the trailing window contained genuine
expansion this OVERSTATES maintenance and therefore UNDERSTATES the terminal* — and the
measurement shows it is not an overstatement but a wipe-out: **EGCH's capex ran 2.1x,
3.5x, 4.2x, 7.8x and 4.2x of revenue** across those origins, because the company was
building the KIMA-2 plant. Charging a build programme as perpetual maintenance is not a
small error on a company mid-build; it makes the terminal negative.

**The declaration also barred a fourth construction, and that bar holds.** The honest
reading is not that a better maintenance proxy should now be invented — it is that
**maintenance needs a disclosed asset life**, which is what [R-TERM-01] has required all
along, and which `engine/valuation_calibration/disclosed_lives.json` carried for exactly
one of these five names when this was written.

### 3 cells: AMOC is blocked twice over, and both are recorded

AMOC's own walk-forward projects three horizons against a declared window of five, so it
drops on that clause first. It would drop again on a second, independent one: **no
quantity appears in both AMOC's exported panel and its valuation-input block**, so the
unit relating them cannot be measured and is declared unavailable rather than guessed.
Recording the second is what keeps it from disappearing behind the first.

---

## Two defects found by building this, neither of them in this instrument

**1. The panels and the blocks do not share a unit, and nothing said so.** AMOC and ARCC
report in EGP, **EGCH in thousands, PHDC and TMGH in millions**, while every
valuation-input block is in EGP because it is copied off the face of the statement. A
cost of debt built from a charge in millions over borrowings in units is wrong by a
factor of a million **and looks like a rate**. The lens now MEASURES the scale per name
against a quantity both records carry, named rather than guessed, asserts it is a clean
power of ten across every year both cover, and refuses the name where it is not. Its
first draft paired AMOC's cost-of-sales depreciation with the block's group charge and
EGCH's bank borrowings with the block's total debt, and **refused both — correctly**;
the fix was to re-point the pair, not to widen the tolerance.

**2. TMGH's own projection carries depreciation with the wrong sign, and its own scorer
hides it.** `bottom_up.py` fits `da_rate` off the panel's `da`, which is stored NEGATIVE
(the company's own convention), so `da = d_rate * ppe` is negative and `f["da"] = -da`
comes out **positive** — measured at origin 2023, horizon 5: `da = +726.7` where the
panel's own FY2023 actual is `−491.8`. The next line, `pbt = gross_profit + sga + da +
finance_cost`, then **ADDS depreciation to profit instead of deducting it**.

Its own `score.py` lists `da` in `MAGNITUDE` and scores it on `|x|`, so the depreciation
cells are unaffected — but **`net_profit` is not in that set and is overstated by twice
the charge at every cell**, and `net_profit` is a scored driver. This is a defect in a
committed run's published error record, found only because something else tried to build
on it. It is fixed in that run as its own unit with its score re-run; this lens takes the
magnitude, which is both the panel's convention and the run's own scoring convention.

---

## What this does not say

- **It does not say the house method is optimistic.** The +167.6% is one name's five
  consecutive years, read almost entirely off a terminal the construction cannot build
  properly, and the pre-registration prohibits reading a level from an instrument this
  thin.
- **It does not retire the instrument.** The two blockers are now separated and their
  sizes are known: nine more block-years would close eleven cells, and a **disclosed
  useful life** for the four names that lack one would close twelve — the six refused
  for maintenance below book depreciation and the six refused for a terminal free cash
  flow the build-programme proxy drove negative. **The second is the binding one**, and
  it is not a question about the module.
- **It does not license a fourth declaration.** The sealed bar stands: if this failed,
  the finding is that a mechanical valuation is not yet constructible from what these
  runs commit. **That is the finding, and it now has a price list.**


---

## CORRECTION, later the same day — the six payout refusals

The section above originally read that the module refused ARCC's and EGCH's
*legitimately negative working capital*. **It does not.** Setting working capital to
zero leaves every one of those origins refused, at 238.9%, 172.5%, 107.0% and 101.1%.
The cause is `maintenance < dna_book`, measured and stated above.

The correction matters because it reverses what the finding asks for. On the first
reading the blocker was a shared module's guard, and the recommendation was to leave it
alone. **On the measurement the guard is correct and the blocker is a missing input** —
the disclosed asset life [R-TERM-01] has required since it was written. That is work
this house can do from filings it already holds, rather than a question about a module
that delivered studies depend on.


---

## THE SENSITIVITY ON A DISCLOSED LIFE — and the answer does not move

The correction above named the binding blocker as a missing input. Two of the five
lives were read from the companies' own accounting-policies notes the same day (ARCC's
and AMOC's; EGCH already had one), so the question could be asked: **what does this
instrument produce with the input [R-TERM-01] has always required?**

It is run as a **third reading published beside the declared one, never as a replacement**.
The sealed declaration bars a fourth construction if the third failed, and it did; it
also justifies its own maintenance basis on a statement about the repository — *"only
one of these five names has [a disclosed life] on file"* — that is no longer true. Both
readings of that bar are defensible, and **resolving it in the direction that produces a
better number is the fitting this house forbids**. So it is not resolved. The declared
run stays the declared run.

The life is not one this module chose: it is the **scalar each name's own delivered
study already committed to its terminal record**, sourced to an accounting-policies
note. ARCC 20.0 years; EGCH 22.07. AMOC, PHDC and TMGH commit no scalar — AMOC's note
gives a 10–30 band and collapsing a band is a judgement — so they are skipped with that
reason.

**The panel is still one name.**

| reading | cells | names | mean log(FV/P) |
|---|---|---|---|
| DECLARED (trailing capex, median amount) | 5 | **1** (PHDC) | +0.9842 |
| maintenance as intensity × origin revenue | 5 | **1** (PHDC) | +0.9834 |
| **maintenance on the disclosed life** | **3** | **1** (ARCC) | +1.1068 |

**Three constructions, three answers, one name every time.** That is a stronger version
of the finding than the declared run alone supports: the panel does not thin because of
one construction choice, and no reading of the maintenance basis rescues it.

**EGCH refuses on BOTH bases, in opposite directions.** On trailing capex its terminal
free cash flow is negative because a build programme was charged as perpetual
maintenance; on the disclosed life it is negative again because escalating a book charge
of EGP 1,858mn over half a 22-year life at Egyptian inflation produces a maintenance
requirement several times the company's terminal profit. **The second is not obviously
an error** — replacing a 22-year-old asset base in that currency really does cost a
multiple of its historical cost, and the module is saying that this company cannot
sustain its asset base out of its earnings. Whether that is a defect or a finding about
KIMA is a question for a rebuild of that name, not for this instrument.

## What the sensitivity found in ARCC's own projection, which is not about this lens

ARCC 2023 reads a fair value of **EGP 105.78 against a close of 10.00**. The cause is in
the run's own forward model, not in the bridge: its projected **EBIT margin compounds
from 30.6% at horizon 1 to 60.1% at horizon 5**, against filed gross margins of 21.2%
(FY2023) and 40.6% (FY2025).

**No gate looks at this.** [R-ANCHOR-01] tests a forecast that opens materially BELOW
the filed record, and its second clause tests a rate that DECLINES from its own opening
year; it says in terms that it does not fire on a forecast above the latest period.

**A first reading of this section added a second reason — that the run's own score
cannot see horizons 4 and 5 from a 2023 origin, so the error record is blind to the part
of the projection a discounted cash flow leans on hardest. The structural half is true;
the attribution is not, and the census says so.**
`engine/valuation_calibration/unscored_horizons.py` measures, per run and per origin,
how far the projected operating margin travels from the first horizon to the last and
how many of those horizons the run could grade:

| | origins | mean \|drift\| |
|---|---|---|
| every horizon gradeable | 19 | **7.0 pp** |
| at least one horizon ungradeable | 13 | **9.0 pp** |

**The two are barely different, and the single largest drift in the book — ARCC 2017,
22.3% to 55.7%, +33.4 points — sits on an origin where ALL FIVE horizons were graded.**
So the drift is a property of these projections generally rather than an artefact of
what could not be graded, and ARCC's is large at every origin, most of them graded. The
run's own error record has seen it and reports revenue and cost UNDER-forecast, which is
the direction a rising margin path produces.

**What that leaves is a question about the driver rule, not about grading coverage:**
whether a 60% EBIT margin at horizon 5 is credible for a cement company whose filed
gross margin has ranged 21.2% to 40.6%. That is a question for a rebuild of that run.
The blindness at recent origins is real and is worth naming — 2 of 5 horizons gradeable
from a 2023 origin — but it is not what produced this number.

Recorded here as a finding about that run. It is not corrected in this pass: changing a
committed walk-forward's forward model is its own unit, as the depreciation-sign fix
was, and it needs its own before-and-after on that run's scored record.
