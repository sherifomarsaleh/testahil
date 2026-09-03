# The pessimism has a mechanism, and it is in the terminal
### Plan of record, 3 September 2026

**Read this first.** The reassessment has been finding defects one study at a time. This
document is the point at which the defects stopped looking like accidents. What follows is
a measured mechanism, a reason to believe it is a class rather than a name, and a plan that
fixes it at the level of the method. It will take several passes. It is written down
because a plan in a conversation binds nothing.

---

## 1. The mechanism, measured

ARCC's terminal block is

```
ic_repl = capacity x replacement cost per tonne x fx x cost inflation
roic    = NOPAT(1+g) / ic_repl
rr      = g / roic
TV      = NOPAT(1+g) x (1 - rr) / (W - g)
```

Substitute `rr` and the reinvestment charge collapses to a constant:

```
TV = [ NOPAT(1+g)  -  g . IC ] / (W - g)
```

So the model charges **g x IC**, on the whole replacement-cost capital base, every year, for
ever. On ARCC's own committed numbers:

| | |
|---|---|
| terminal NOPAT (FY2030) | EGP 5,385.2mn |
| replacement-cost capital | EGP 51,190.9mn (book FY2025: 5,777.7mn — **8.86x**) |
| the charge `g x IC` at g = 7% | **EGP 3,583.4mn a year, for ever** |
| that as a share of terminal NOPAT | **62.2%** |
| the REAL growth it buys | **zero** — the study's own `macro_record` sets terminal real growth to 0.0 |

**The model charges 62% of profit in perpetuity to buy nothing.** g = 7% is the house
terminal inflation at zero real growth. Inflation does not require capacity. A company
whose volumes are flat and whose prices rise with the price level needs *maintenance*
capital, not *growth* capital. The reinvestment identity `g = rr x ROIC` is a statement
about **real** growth; applied to a nominal rate that is pure inflation it charges the
company for something inflation supplies free.

There is a second, independent error in the same six lines. The explicit window builds
`FCFF = NOPAT + D&A - capex - dWC`. The terminal builds `NOPAT(1+g) - g.IC` and **never adds
D&A back**, though NOPAT is already net of it. One model, two definitions of free cash flow,
and the terminal carries 41.4% of enterprise value.

## 2. Why this is a class and not a name

Three properties, and each is what makes it dangerous rather than merely wrong.

**It is invisible to every check.** Nothing in it is arithmetically false. `roic` is computed
correctly, `rr` follows, the algebra of `TV` is textbook, the workbook recalculates to the
cell, the study even derives the analytic sign condition for the growth lever and verifies
that the model agrees with its own algebra. Every gate in this repository passes it. The
defect is a **specification** error, and [R-FCAL-01] already says of that class that no
correction factor may hide it.

**It is one-directional.** The charge is always subtracted, so the error always lowers value.
It never shows up as noise.

**Its size scales with exactly the conditions this book operates in.** The charge is
`g x IC`, so it grows with terminal inflation and with the replacement-to-book ratio. In
Egypt at 7% terminal inflation, on plant carried at a ninth of what it costs to rebuild, the
charge is enormous. Every Egyptian industrial study using this identity carries it, and the
higher the inflation the worse it gets — which is the opposite of prudence.

That is the shape of a systematic lean. It explains why the pessimism looked like a house
temperament: it was a formula.

## 3. The instrument that catches it without needing an opinion

A firm can always choose not to invest. Zero growth with full payout is always available, so
a terminal can never be worth less than a no-growth perpetuity:

```
TV  >=  NOPAT_term / W_term          (the floor)
```

This needs no view on ROIC, on the capital basis, on asset lives or on growth. It is a
dominance argument. On ARCC:

| | terminal | equity | fair value | vs price 77.00 |
|---|---|---|---|---|
| as published | 19,209.9 | 19,946 | **53.21** | **-30.9%** |
| at the unconditional floor | 29,359.8 | 24,164 | **64.46** | **-16.3%** |

**The published answer sits 34.6% below the floor its own model implies.** Half the ARCC gap
is this, and it is not a judgement anyone has to win.

The floor is the deep instrument, and it is why this plan is not a patch: one test, stated as
a dominance condition, catches the whole class on every name for ever, and it cannot be
tuned because it has no parameters.

## 4. The plan

Ordered so each stage's output is the next one's input. Each ends in a committed artefact and,
where the rule can be tested, in a gate that FAILS rather than warns [R-ENF-01].

**WS-A — one terminal, in shared code.** `engine/terminal_value.py` becomes the only
sanctioned way to build a terminal, on the pattern of `beta_regression.own_stock_beta()` and
`cost_of_capital.py`: every study once hand-rolled its own beta and every one of them was
wrong the same way. Its contract makes the real/nominal split *structural* —

- it takes **real** growth (default zero) and reads inflation from the house macro path
  [R-MACRO-01], so a nominal rate cannot arrive as a growth assumption at all;
- it builds `FCFF_term = NOPAT + D&A_book - maintenance_at_current_cost - real_growth_capex
  - pi x WC`, the same definition the explicit window uses, so the two cannot diverge;
- it REFUSES a reinvestment charge attached to a nominal rate — the ARCC construction is not
  expressible;
- it REFUSES an implied payout outside [0, 1];
- it returns the floor beside the answer, always.

**WS-B — the floor test, from outside the study.** `scripts/check_terminal_floor.py` over
every `engine/*_study/`, ratcheted [R-ENF-02], population-anchored [R-ENF-04],
negative-controlled on ARCC's terminal exactly as it shipped plus clean cases that must stay
green. A study whose terminal sits below `NOPAT/W` fails.

**WS-C — measure the class before treating it.** Re-express every study's terminal in the
identity above and apply the floor. That turns "are we pessimistic" from a temperament into a
table: which names are below their own floor, by how much, and how much of each gap it
explains. Published as a dated finding. This is the stage that says whether ARCC is one name
or twenty, and nothing downstream is decided before it is read.

**WS-D — the invested-capital basis, priced rather than defaulted.** Replacement cost and
book differ by 8.86x here and the honest answer is *neither*: the quantity the identity needs
is the return on **new** capital. All three framings priced, entered in the [R-ENF-05]
contested-judgement register with both sides, and published as a disagreement rather than
chosen silently. The company's own cash-flow statements are the arbiter and they say capex has
run about 2x book D&A, not 8.9x — a fact the study holds and never consumed.

**WS-E — re-issue on the corrected identity, then measure the direction of the whole set.**
ARCC and EGCH first (both HELD under [R-GAP-02]). Then the [R-ENF-05] sign test across all
five rebuilt names **together**, because a lean lives in the pattern of choices and five names
is the population it was built for.

**WS-F — bind it.** [R-TERM-01] into both governing documents in one commit, the lessons
registered with their falsifiers, and the queue's remainder recorded.

## 5. What would overturn this

If a study can show that its company is **contractually obliged** to spend `g x IC` — a
concession, a licence condition, a take-or-pay — then the floor argument fails for that name,
because the no-investment option is not actually available. No such obligation is disclosed
for ARCC. If the replacement-to-book ratio turns out to be a measurement error rather than a
real gap between historical cost and current cost, WS-D's arithmetic changes but WS-B's floor
does not, because the floor never touches the capital base.

## 6. What this plan deliberately does not do

It does not move any number toward the price. [R-GAP-01] is explicit that a fair value
adjusted to meet a quote is the reverse-engineered rate this method prohibits, arriving through
the front door. The price is the instrument that told us to look here; the correction is
justified by the identity, and it would be justified in the same direction and by the same
amount if ARCC were trading at 40.

**The general lesson, which is not about terminals.** A formula that is right in real terms and
wrong in nominal terms passes every arithmetic check that will ever be written, because nothing
in it is arithmetically wrong. Recalculation, provenance, source discipline and four-field
registers were all clean on this study. Where a quantity carries a unit — real or nominal, this
year's money or that year's — the unit is the thing to check, and no amount of care inside the
arithmetic will supply it.
