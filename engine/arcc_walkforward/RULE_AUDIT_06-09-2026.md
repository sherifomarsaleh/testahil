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
