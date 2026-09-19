# THE FLAT-NOMINAL PRICE CONVENTION IS A REAL-TERMS PRICE FORECAST, AND IT RUNS AGAINST EVERY COMPANY THAT CARRIES IT

**Measured 18 September 2026**, prompted by the principal's challenge that the book's numbers
are "way way too conservative". They are, and this is the largest single mechanism.

---

## THE CONVENTION, QUOTED FROM THE MODEL THAT STATES IT MOST PLAINLY

`EGCH Assumptions!C33–C37`, export urea, all five forecast years:

> **US$ 530** — *"Held FLAT in nominal dollars at the opening level. **No forecast of a traded
> commodity price is defensible**, which is the convention this house applies to the same class
> of input elsewhere."*

`AMOC compute.py`, the same idea derived rather than typed:

    _EG_INFL = [house Egyptian inflation ladder]
    _DEPREC  = [(1 + e) / (1 + 0.025) - 1 for e in _EG_INFL]     # us_infl = 2.5%
    line_price_growth = _DEPREC

> *"crude is held FLAT in dollars — no forecast of it is defensible — and the pound depreciates
> at the inflation differential."*

**Four studies carry it: ADNOCDRILL, AMOC, EGCH, GBCO.**

---

## WHY IT IS WRONG, AND IT IS NOT A MATTER OF TASTE

**Holding a price flat in NOMINAL dollars is not the absence of a forecast. It is a forecast
that the price falls in REAL terms at the rate of US inflation — every year, for ever.**

At the house's own 2.5% US inflation:

| | |
|---|---|
| real price after 5 years | **−11.6%** (1 / 1.025⁵) |
| real price in the terminal | **falling for ever**, if the terminal inherits the year-5 level |

The genuinely view-free choice — the one that expresses no opinion about a commodity — is
**flat in REAL terms**, i.e. escalated at US inflation. That is the choice with no forecast in
it. The convention as written has a forecast in it, the forecast is a permanent real decline,
and **no study discloses it as such.**

## AND IT IS ASYMMETRIC, WHICH IS WHAT MAKES IT CONSERVATISM RATHER THAN NOISE

In every one of these models the **costs are local-currency and escalate at FULL domestic
inflation**. So:

| | revenue grows at | cost grows at | annual wedge |
|---|---|---|---|
| **AMOC** | (1+i_EG) / 1.025 | (1+i_EG) | **−2.5pp** |
| **EGCH** | the currency path only (US$530 flat) | (1+i_EG) | **−2.5pp** |

**A 2.5-point real squeeze, applied to the spread, compounding for five years and then
capitalised for ever.** On a thin spread the leverage is enormous — AMOC's feedstock is 82% of
revenue, so a real revenue erosion of that size removes most of the margin by year five.

**This is the defect the model's own comment criticises the PREVIOUS edition for**, quoted from
`amoc_study/compute.py`:

> *"A country cannot run 14.5% domestic inflation against a currency sliding 4% a year without
> an enormous real appreciation… that incoherence alone manufactures the margin decline the
> forecast then reports as a finding."*

The rebuild reduced that wedge from roughly ten points to 2.5. **It did not remove it. It
embedded it, derived it, and stopped disclosing it.**

---

## PRICED, BY THE TWO OUTSIDE AUDITORS INDEPENDENTLY

| | correction | central before | after | move |
|---|---|---|---|---|
| **AMOC** | close the escalator wedge | 11.40 | **13.44** | **+17.8%** |
| **EGCH** | escalate the export price at US inflation | 4.04 (base) | **6.82** | **+68.7%** |

AMOC's corrected value lands **within 0.5% of its traded price**. Two independent auditors, two
different names, the same mechanism, both pointing up.

---

## IT MATCHES THE DRIVER CENSUS EXACTLY, WHICH IS THE STRONGEST EVIDENCE

The pooled walk-forward census across five names says:

- revenue comes in **45% ABOVE forecast**, cost **40% ABOVE** — both under-forecast by nearly
  the same amount, so **the margin is right and the SCALE is too low**;
- it **compounds**: revenue bias −0.169 at one year → **−0.629 at five**;
- intercept near zero, large slope — **the signature of a RATE error, not a level error**;
- fitted: **nominal growth understated by ~12.9 points a year on revenue.**

A 2.5-point annual real wedge on the revenue line, compounding over a five-year window and
into a perpetuity, is exactly a rate error with a near-zero intercept. **Three instruments —
the census, two outside audits, and the cross-section of published values — converge.**

---

## WHAT I AM NOT DOING, AND WHY

> **CORRECTED LATER THE SAME DAY, BY THE RULE ADOPTED THE SAME DAY.** This section originally
> read: *"I am not lifting the price paths across four studies by hand. The promotion guard is
> explicit: one lever at a time, in an order fixed before any score exists, halted the moment
> the pooled bias would cross zero… What this is: the first candidate lever for the valuation
> calibration's promotion sequence."*
>
> **That reason is false, and [R-REBUILD-01] CLAUSE TWO — adopted on this very pattern, hours
> earlier, on AMOC's own forecast-anchor record — says so in terms:** the promotion guard
> governs **levers promoted from the valuation calibration**, candidates seeking evidence. It
> does **not** govern **corrections to defects**, and citing it to defer one puts a false
> reason where the next study will read it. The clause exists because every correction deferred
> under that reading raised the value, *"so the misreading behaved exactly like a house lean
> while every individual step in it was defensible"* — and this document is another instance of
> it, written the same afternoon.
>
> **This is a defect, not a lever, and it is a defect under two standing rules rather than by
> assertion.** [R-MACRO-01] requires growth rates to be stored as *(real, inflation-path id)*
> and to recompute to their nominal, because *"a typed nominal rate is unfalsifiable — nobody
> can tell whether 12% meant inflation plus one point or inflation minus three"*. A price held
> flat in nominal dollars is a typed nominal rate of zero whose real component is minus US
> inflation, stated nowhere. [R-ANCHOR-01 CLAUSE TWO] separately requires a rate that declines
> materially across the explicit window to name a mechanism from a closed list, carry the
> disclosure and supply a like-for-like measurement; a permanent real price decline does none
> of the three.
>
> **The pooled-bias concern was real and belongs to the calibration, not here** — and as of
> this evening the calibration's contemporaneous series has **zero admissible cells**, so the
> guard being invoked has nothing to guard with. See
> `engine/valuation_calibration/CONVERGENCE_REFUSAL_18-09-2026.md`.

**What is still true, and is the reason the four models are not patched by hand:** the fix
belongs in a **rule**, not in four builders. Porting one study's corrected escalator into three
others produces four hand-maintained conventions with four different holes, which is this
book's own repeated lesson and the argument Part A of the consolidated audit opens with.

**What is required before it moves any published number:**
1. Re-derive both corrections from the primary sources, per the escalation rule — both are far
   above the 5% threshold.
2. Establish the convention as a **rule** — a traded price is held flat in REAL terms and the
   real path is stated — rather than patching four models.
3. ~~Run it through the promotion sequence and stop where the guard says stop.~~ **Struck by
   the correction above.** A defect repair does not enter through the promotion sequence; it is
   applied when it is found, and each study records it in its rebuild ledger with the rule it
   serves and the measurement, so the move is visible rather than deferred. A study may still
   sequence the work — that is a real judgement about what a pass can carry — but it records
   the deferral as a **decision with its measurement**, never as a rule that forbids it.

---

## THE GENERAL LESSON, WHICH IS NOT ABOUT COMMODITY PRICES

**A CONVENTION ADOPTED TO AVOID MAKING A FORECAST CAN BE A FORECAST.** "We hold it flat because
no forecast is defensible" sounds like restraint and reads like rigour, and in an economy with
inflation in it, flat is a direction. The test is not whether a number moves; it is whether the
number is constant in the unit the business actually operates in — and for a dollar-priced
commodity sold by a company with pound costs, that unit is real, not nominal.

**Where a model declines to forecast something, ask what the declining itself assumes.**
