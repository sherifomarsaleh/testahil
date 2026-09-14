# ARCC — reading the forecast against what happened, rule by rule

**6 September 2026.** Not a statistic about the whole book. One company, every driver
rule, against what the company actually reported. Reproduce with
`engine/arcc_walkforward/rule_audit.py`.

---

## 1. Almost nothing here is a level error

Twenty-four of the twenty-six scored drivers get **worse with every year forecast**.
Only total volume and manufacturing depreciation stay flat across horizons. An
intercept near zero with a growing miss is a *rate* error and nothing else: the base
year is right and the path is wrong. Re-anchoring the base year cannot touch it.

## 2. The model has two escalators. Reality has fifteen rates.

Every driver rule, against the compound annual rate the line actually ran at over the
window. Realised CPI, the escalator the model leans on, was **+15.2% a year**.

| line | realised | the rule applies | bias at 5 years |
|---|---|---|---|
| interest income | **+72.8%** | flat | −3.13 |
| provisions | +64.9% | flat | −2.47 |
| transport per tonne | **+35.5%** | CPI, +15.2% | −1.45 |
| services | +29.8% | CPI | −1.19 |
| other income | +28.9% | flat | −1.29 |
| price, local | **+21.4%** | CPI | −0.64 |
| general & admin | +19.8% | CPI | −0.51 |
| overhead per tonne | +19.2% | CPI | −0.35 |
| price, export | +18.6% | FX depreciation | −1.07 |
| **volume, export** | **+18.1%** | **flat** | −1.36 |
| raw material per tonne | +12.3% | half coal — and coal is **frozen** | −0.45 |
| manufacturing depreciation | +3.5% | flat | −0.11 |
| **volume, local** | **−3.9%** | **× population growth** | **+0.43** |
| amortisation | −8.1% | flat | +0.52 |
| finance costs | −10.8% | flat | +0.42 |
| currency result | — | **set to zero, "refused"** | not scored |

Realised rates span **−10.8% to +72.8%**. The model answers with CPI or with nothing.
Eight of the fifteen lines are frozen outright.

**In a currency that lost most of its value across this window, "flat" is not a
neutral prior. It is a forecast of steep real decline** — and it is the default for
more than half the model.

## 3. But the errors do not all run one way, and that changes what to do

Pricing each rule's miss in pounds of profit across every matured cell:

| | EGP |
|---|---|
| rules that make us forecast **less** profit | **−77.0 bn** |
| rules that make us forecast **more** profit | **+53.9 bn** |
| **net** | **−23.1 bn** |

**Gross mis-forecasting is EGP 131bn. The net is EGP 23bn.** The pessimism this
programme has been chasing is the *residue* of two much larger errors that nearly
cancel.

The largest single rules, by money rather than by bias:

| rule | share of all mis-forecasting | direction |
|---|---|---|
| price, local | 23.6% | under |
| **volume, local** | 18.2% | **over** |
| volume, export | 17.6% | under |
| **raw material per tonne** | 15.9% | **over** |
| price, export | 11.6% | under |

Two pairs, each nearly self-cancelling:

- **Total volume is right; the mix is wrong.** Total volume carries a bias of −0.019 —
  essentially perfect. Local is over-forecast by +0.43 and export under by −1.37,
  because the model grows local at population growth while local volume actually *fell*
  4% a year, and freezes export while export grew 18%. **The company is shifting to
  export and the model does not know it.** The two errors offset in tonnes and do not
  offset in pounds, because export and local prices differ.
- **Local price under-forecast (−31bn) against raw cost under-forecast (+21bn).**

## 4. What this means for the fix

**Fixing the biggest lever alone makes the model worse.** Correct only the local price
and the net swings from −23.1bn to **+7.9bn** — from pessimistic to optimistic — while
thirteen other rules stay wrong.

That is [R-VCAL-01]'s promotion guard arriving as arithmetic rather than as caution:
several individually-justified corrections stack into an overshoot. **These rules have
to be fixed together, with the net re-measured after each, and the sequence stopped the
moment it crosses zero.**

## 5. What is actually wrong, in one sentence

The protocol already requires every driver to be built at the finest sourced level with
its own escalator — *one escalator per driver class, never one blended index across
physically distinct cost lines*. **This model does not do that.** It applies general
consumer inflation to five lines that ran at 12% to 36%, freezes eight more in nominal
pounds, and drives the volume split off population growth. Transport does not follow
CPI, it follows diesel; raw materials follow coal and the model froze coal; interest
income follows the policy rate, which trebled.

The rule was written. It was not implemented here. That is the defect — and it is a
defect in the driver construction, not in the discount rate, the terminal, or the
bridge.

---

# Part two — the two obvious fixes both fail, and the third finding is the real one

## Fix A: give each line its own trailing rate. **Makes it worse.**

Applied in the order the audit's own numbers fixed — largest measured cost first,
net re-measured after each:

| after applying | net profit miss (EGP) |
|---|---|
| nothing — the model as it stands | −13.5 bn |
| + local price on its own premium over CPI | −24.0 bn |
| + the volume mix on its own drift | −23.0 bn |
| + coal on the currency | −29.6 bn |
| + export price on its own premium | −36.1 bn |
| + every remaining line on its own rate | **−37.0 bn** |

The sequence never crosses zero; it walks steadily away from it. **Trailing history is
a bad forecaster here because the window contains a regime break** — cement prices and
volumes *fell* in 2019 and 2020 and then exploded from 2021. At every origin before
2021 the trailing rate points downward. That is the same result the book-wide
comparison already gave: a trailing three-year trend scores worse than the model on
76 of 76 pooled drivers.

## Fix B: blame the macro. **The numbers refuse it.**

| | net profit miss | net revenue miss |
|---|---|---|
| as the model runs | −13.5 bn | −46.0 bn |
| knowing inflation perfectly | −7.9 bn | −33.6 bn |
| knowing inflation, currency **and** coal perfectly | −38.8 bn | −31.6 bn |

**With perfect foresight of every macro input, 69% of the revenue miss remains.** The
future being unknowable is not the explanation. Something structural is.

## The real finding: eight of nineteen drivers were pre-declared to be "no change"

The pre-registration says, in its own words:

> **Declared in advance, so it is not later reported as a finding:** D2, D3, D10, D11,
> D13, D14, D15 and D16 are level-persistence rules and are therefore **identical to
> FREEZE by construction**. Their skill against FREEZE is zero by definition, not by
> measurement.

Against what those eight lines actually did:

| | line | realised | |
|---|---|---|---|
| D14 | interest income | **+72.8%** a year | moves |
| D13 | provisions | +64.9% | moves |
| D15 | other income | +28.9% | moves |
| D2 | export volume | **+18.1%** | moves |
| D10 | manufacturing depreciation | +3.5% | genuinely stable |
| D11 | amortisation | −8.1% | moves |
| D16 | finance costs | −10.8% | moves |
| D3 | export mix | **1% → 48% of tonnes** | moves |

**Seven of the eight move materially. One does not.**

And the run's own basis-break register already knew. B-9, written by this same run,
records the export swing tonne by tonne and concludes: *"The channel mix is a
pre-registered driver in its own right, not a residual."* **The register says it is a
driver. The code freezes it. The pre-registration declares the freeze immune from
being reported as a finding.**

### Why this is the answer and not the gates

The declaration itself is good practice — stating in advance which rules are
level-persistence is exactly the transparency this protocol demands. **The failure is
that it was read as a licence rather than as a warning.** Nobody went back to ask
whether those eight *should* be frozen once the basis breaks documented that they
moved, because the pre-registration had already said their skill would be zero "by
definition, not by measurement" — and a thing declared not-a-finding does not get
found.

This is also why the method only beats "no change" on 58% of drivers book-wide.
**A large part of the method is no change, by declaration.**

### What it means for the fix

Not a better statistical rule — Fix A shows extrapolation fails across the break.
These lines need the **drivers they actually have**, each of them disclosed and
knowable at the origin:

- **export volume and mix** ← the company's own capacity, its export contracts, and
  the cement production quota regime, a dated public fact this run already registered
- **interest income** ← the policy rate × the cash balance, both point-in-time
- **finance costs** ← the disclosed debt schedule
- **amortisation** ← the disclosed asset schedule

That is SIGCM clause 2 — build from the ground up, volume × price, at the finest
sourced level — applied to the eight lines that opted out of it.

---

# Part four — the lean is not systematic. It is three origins.

Every fix above failed, and the reason is that they were all fixing the wrong thing.
Group the error by the ORIGIN it was forecast from, rather than by the driver:

| | ARCC revenue | TMGH, all drivers |
|---|---|---|
| **every origin** | −0.278 · actuals **32%** above | −0.280 · actuals **32%** above |
| **origins 2020, 2021, 2022** | −0.695 · actuals **100%** above | −0.692 · actuals **100%** above |
| **every other origin** | **+0.108 · actuals 10% BELOW** | **−0.041 · actuals 4% above** |

**Two companies, two different models, two different sectors, measured
independently — and they agree to the third decimal.** Thirty-two per cent under
overall. A hundred per cent under at the 2020–2022 origins. And essentially
unbiased everywhere else, one slightly over and one slightly under.

On ARCC those three origins account for **more than the whole lean** — take them out
and the model forecasts revenue 10% too HIGH. On TMGH they account for 91% of it,
and a block bootstrap over the remaining origins gives an interval of
[−0.222, +0.119] — **covering zero**.

## What those origins were

ARCC's own history, which the model was forecasting from:

| | total volume | export share | local price |
|---|---|---|---|
| FY2019 | 4,558 kt | 13% | 660 |
| **FY2020** | 4,078 kt | 9% | **581** |
| **FY2021** | 3,208 kt | 15% | 757 |
| FY2022 | 4,561 kt | 22% | 1,074 |
| FY2023 | 4,376 kt | 39% | 1,460 |
| FY2024 | 5,054 kt | 48% | 1,796 |
| FY2025 | 4,854 kt | 40% | **2,856** |

FY2020 and FY2021 are the floor — the lowest volume and the lowest price in the
record. Forecasting forward from there, on any rule, missed a price that quintupled
and an export share that went from 9% to 48%. **Egypt devalued, the cement quota
regime changed, and the export market opened.** No rule available at those origins
saw it, which is what a structural break is.

## What this means, and it is not what this programme assumed

**The 45% under-forecast that launched this reassessment is not a systematic lean.**
It is a regime break sitting inside the sample, and outside it the method is
unbiased on both names that can be measured this way.

That reframes every conclusion drawn from it:

- **The driver rules are broadly sound at ordinary origins.** Part one found fifteen
  of them mis-specified against realised rates, and that is still true — but the
  mis-specification does not produce a lean except across the break.
- **The three fixes in parts two and three all failed for one reason**: each tried to
  extrapolate through a break from data on the wrong side of it.
- **Perfect macro foresight leaves 69% of the miss** because the break was not only
  macro. The quota regime and the export market moved too.
- **Corrections already made stay right.** AMOC's six defects, the terminal, the
  macro path — those were found by auditing answers, not by chasing this lean, and
  they were real.

## What should change instead

Not the driver rules. **The claim.** [R-FCAL-01] already says the far years of a
projection support ranges and never points; this measurement says what the range has
to carry. A study struck from an ordinary origin is about right. A study struck at a
trough, before a devaluation or a regulatory change, can be **out by a factor of
two** — and nothing in the method will tell you in advance which one you are writing.

## Three of the five runs cannot be read this way at all

AMOC, EGCH and PHDC commit no per-cell error list, so the error cannot be grouped by
origin for them. **The single most valuable thing those runs could add is not another
driver — it is their own cells.** That is the same class of gap as the
valuation-input block: the run answered the question it was built for and left no
trace of the one asked next.

---

# Part five — the rules fixed anyway, and what that is worth

The rules are mis-specified whether or not they net out. A rule that escalates road
haulage at consumer inflation while haulage runs at 35% a year is wrong, and the next
break will not be kind in the same direction. Fixed in `driver_fixes.py`.

**The test changed, and that is why this comes after part four rather than before.**
Judging a rule on the pooled error judges it on three origins that dominate
everything — which is how all three earlier attempts failed. A well-specified rule
should show at **ordinary** origins, so that is where it is scored, with the break
origins printed beside it and never hidden.

| | ordinary: revenue bias | ordinary: PBT bias · MAE | break: revenue bias | break: PBT MAE |
|---|---|---|---|---|
| the model as it stands | **+0.108** | +0.604 · 1.019 | −0.695 | 1.822 |
| F1 imported coal carries the currency | +0.108 | +0.600 · 1.016 | −0.695 | **1.659** |
| **F2 the works price follows the cost stack** | **+0.011** | **+0.341 · 0.841** | −0.747 | 1.827 |
| F3 the export share is held, not the tonnage | +0.009 | +0.315 · 0.852 | −0.749 | 1.870 |
| F4–F6 interest, the euro book, the nominal lines | **+0.009** | **+0.303 · 0.866** | −0.749 | 1.861 |

**At ordinary origins the revenue lean goes from +10.8% to +0.9%, and the profit lean
halves while its error falls 15%.** At the break origins everything is marginally
worse. Both facts are the honest result: correcting a mis-specification removes the
residual lean where a forecast can be judged, and **nothing rescues a structural
break** — which part four already established.

**F2 is most of it.** Cement is a cost-plus commodity: its works price tracks the cost
of making it, not the consumer basket. Escalating it at CPI while its costs ride coal
and diesel is the single largest mis-specification in the model, and it is the one the
protocol already forbids in words — *one escalator per driver class, never one blended
index across physically distinct cost lines*.

## What was fixed, and what was left alone on purpose

**Fixed, each naming its driver and inventing no parameter:** imported coal on the
currency; the works price on the cost stack at the pass-through of 1.0 the
pre-registration already declares; the export share held rather than the tonnage;
interest income on cash and the policy rate from the point-in-time archive; the
currency result on the 91.1% euro book note 25 discloses, which the model had set to
zero and labelled refused; provisions and other income scaled to the business.

**Left alone, with the reason recorded rather than papered over:**

- **transport, overhead, general and administrative** — each follows fuel and wages in
  a mix nobody disclosed. A better escalator needs a weight, and inventing one is the
  free parameter the promotion rule forbids.
- **amortisation** — fully deterministic from the intangibles note, and **this run does
  not commit that table**. The driver exists; the data to build it does not.
- **finance costs** — debt times a rate, and the effective rate off the disclosed book
  swings from 4.4% to 85.5% year to year because year-end debt is the wrong
  denominator. That is [R-FCAL-01] trap (i), and building on a denominator known to be
  wrong is worse than leaving the line frozen.
- **manufacturing depreciation** — runs at +3.5% a year. Freezing it is defensible.

Two of those four are blocked by things this run could have committed and did not: the
intangibles schedule, and average rather than year-end debt.

---

# Part six — a correction to part five, and the sixteenth defect

## The correction: the profit improvement in part five was measured on a shrinking sample

Part five scored profit on `log(projected / actual)`. **A log ratio cannot score a
cell whose projection is negative, and it drops it silently.** The corrected rules
turn four ordinary cells into projected losses, so those cells left the sample and
the remaining bias looked better. The figure quoted there — +0.604 to +0.303 — was
computed on eleven cells before and seven after.

Re-scored on `(projected − actual) / |actual|`, which keeps every cell:

| profit before tax, ordinary origins | cells | mean error | MAE | cells projecting a loss |
|---|---|---|---|---|
| the model as it stands | 13 | +3.18 | 3.44 | 3 of 25 |
| the six corrected rules | 13 | **+0.81** | **1.73** | **10 of 25** |

**The improvement is real on identical cells** — the over-forecast falls from +318%
to +81% and the error halves. The revenue result of part five is unaffected: the same
thirteen cells score before and after, and the bias goes from +10.8% to +0.9%.

**But the fix triples the projected losses**, and that is the thread worth pulling.

## The tested alternative, which is worse

F2 ties the works price to the model's own **forecast** cost stack — and three lines
in that stack still escalate at consumer inflation, because their fuel and wage
shares are not disclosed. So the price inherits the very escalator errors F2 was
meant to route around. A variant tying the price to the **marginal input** instead —
imported energy on the currency, the one escalator properly specified after F1 — was
built and is worse on everything:

| | revenue bias | PBT mean | PBT MAE | losses |
|---|---|---|---|---|
| as the model stands | +0.108 | +3.18 | 3.44 | 3 |
| **F2 on the forecast cost stack** | **+0.009** | **+0.81** | **1.73** | 10 |
| F2 on imported energy alone | −0.143 | −2.32 | 2.47 | 18 |

F2 as built stands. The alternative was tested rather than assumed away.

## The sixteenth defect: nothing in this model reverts

**All ten loss-projections come from the FY2019 and FY2020 origins. Nine of the ten
are wrong** — the company's profit went on to multiply by thirty.

| projected loss at origin | actual profit that year |
|---|---|
| FY2019, one year out | −137mn — **correct** |
| FY2019, two to five years out | +55mn, +522mn, +930mn, +1,506mn |
| FY2020, one to five years out | +55mn, +522mn, +930mn, +1,506mn, +4,725mn |

**Every driver rule in this model is a level or an escalator. Not one of them
reverts.** From a cyclical trough the model extrapolates the trough for five years
and then capitalises it for ever; from a peak it would do the reverse. Mean reversion
is the most ordinary assumption in equity valuation and this model has no term for it.

**That is the real explanation for 2020–2022**, and it is a better one than "a break
nobody could see". The company was at a cyclical floor. A model that reverted its
margin toward mid-cycle would have been far less wrong without any foresight at all.

## And reversion was tested, and the data will not support it yet

Added with no new parameter — the contribution margin reverts linearly to its own
trailing median, arriving by the last explicit year, because a terminal value is
already a mid-cycle statement:

| | revenue bias | PBT mean | PBT MAE | losses |
|---|---|---|---|---|
| the six corrected rules | +0.009 | +0.81 | 1.73 | 10 |
| + margin reverts to its own median | +0.009 | +0.78 | 1.74 | 10 |

**It changes almost nothing, and the reason is in the data:**

| | margin | trailing median the origin can see |
|---|---|---|
| FY2019 | 15.1% | too short |
| **FY2020** | **11.1%** | **15.1%** |
| FY2021 | 17.3% | 16.2% |
| FY2025 | **42.9%** | 22.7% |

At the FY2020 origin the trailing median is 15.1% against a margin of 11.1%.
Reversion pulls up four points while the margin actually went to 42.9%. **Eight years
of history, most of it the trough, cannot locate a mid-cycle** — the median is
dragged down by the same years the model is trying to escape.

**So mean reversion is right in principle and needs an anchor from outside the
company's own short record**: an industry mid-cycle margin, a replacement-cost
return, a peer distribution. This run holds none of them. That is the largest single
gap remaining, and it is the one that turns a hard forecast into a catastrophic one.

---

# Part seven — looking for an external mid-cycle anchor

Part six said mean reversion is right in principle and needs an anchor from outside
the company's own short record. Three candidates exist, two of them genuinely
external. **Only one works, and it is the one that is not external.**

## Candidate 1 — replacement cost. External, already held, and it does not bind.

The study commits **USD 130 per annual tonne** of cement capacity (a 120–150 band)
and a replacement-cost invested capital of **EGP 51,191mn**. The textbook mid-cycle
condition for a commodity industry is that producers earn their cost of capital on
replacement cost — below it capacity closes, above it capacity is built.

| | |
|---|---|
| required EBIT to earn 18.34% on replacement cost | **EGP 12,114mn** |
| ARCC's FY2025 revenue | EGP 12,447mn |
| **the hurdle as a share of revenue** | **97%** |

**An impossible margin.** Egyptian cement runs at 52–79% domestic utilisation against
76 Mt of nameplate capacity, with **12.6 Mt more under revival**. No producer earns a
replacement-cost return and none will until capacity closes. Using this as a
reversion target would make the model wildly optimistic.

This is not a defect in the anchor — it is a fact about the industry, and it is the
same one the terminal work already found: *building capacity here does not clear this
company's cost of capital.*

## Candidate 2 — capacity utilisation. Available, and it points the wrong way.

Utilisation is the textbook driver of cement margins. Over this window it is
**negatively** correlated with margin, at **−0.50**:

| | utilisation | gross margin |
|---|---|---|
| FY2018 | 77% | 13.7% |
| FY2020 | 74% | **1.0%** |
| FY2024 | **52%** | 23.9% |
| FY2025 | 58% | **40.6%** |

Margin rose as domestic utilisation fell, because the company switched to export and
the currency moved. **The textbook driver is not the driver here.**

## Candidate 3 — peers. One year each, so no cycle.

Sinai Cement and Misr Beni Suef are committed at FY2025 only: profit margins of 25.2%
and 69.2% against ARCC's 28.9%. That places ARCC in the field. It says nothing about
mid-cycle.

## What works: the four years of its own history the model cannot see

`bottom_up.actual()` starts at FY2016 because that is where the full cost stack was
parsed. **`panel_export.json` carries the income statement from FY2014** — and those
early years are the only pre-trough normal period in the record:

| FY2014 | FY2015 | FY2016 | … | FY2020 |
|---|---|---|---|---|
| 29.2% | 24.4% | 29.6% | | **1.0%** |

The model's idea of mid-cycle is built entirely out of the decline and the trough.
Widening the window to twelve years moves the mid-cycle an origin can see from 6.7%
to 14.3% at FY2020, and from 16.3% to 20.1% today.

| | revenue bias | PBT mean | PBT MAE | at the break | losses |
|---|---|---|---|---|---|
| the model as it stands | +0.108 | +3.18 | 3.44 | −0.89 | 3 |
| the six corrected rules | +0.009 | +0.81 | 1.73 | −1.04 | 10 |
| **+ reversion to the twelve-year median** | **+0.009** | **+0.20** | **1.32** | −1.46 | 11 |

**Profit error at ordinary origins falls 62% from where the model stands** — 3.44 to
1.32 — and the over-forecast falls from +318% to +20%. The break origins get worse,
because at FY2022 and FY2023 the twelve-year median sits *below* the actual margin, so
reversion pulls down a margin that in fact kept climbing. That is mean reversion
behaving correctly and being wrong, which is what it is for.

## The honest answer to "find an external anchor"

**There is no usable external mid-cycle anchor for ARCC in what this house holds, and
each candidate fails for a stateable reason** — replacement cost does not bind in an
over-capacitised industry, utilisation has the wrong sign over this window, peers
carry one year. What works is four years of the company's own record that the model
was not reading.

Two things follow, and neither needs a new theory:

1. **Parse the cost stack back to FY2014.** The filings are in this run's own archive
   (`ARCC_FY2015_Consolidated.pdf` onward) and the income statement is already
   extracted. The gap is the cost stack, and it is a parse.
2. **A real external anchor needs peer history, not peer snapshots.** Sinai Cement and
   Misr Beni Suef are both EGX-listed with public filings. Five years of each would
   give an industry mid-cycle that does not depend on ARCC's own trough.
