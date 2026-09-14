# The mechanical fair value — third declaration, on inputs the second one waited for

**6 September 2026.** This supersedes `MECHANICAL_LENS_2_03-09-2026.md`, which is not
edited and stays in the repository as it was sealed, beside the first. **Nothing below
was computed before this file was committed.**

---

## The second declaration forbade a third shape. It did not forbid this one, and the
## difference is its own sentence rather than my reading of it

The second declaration closed with a bar on itself:

> **There is no third declaration.** If this construction also fails, the finding is
> that a mechanical developer valuation is not constructible from what the
> walk-forward commits — which is a real and reportable result — and **the calibration
> waits for the projection to carry the missing items rather than trying a third
> shape.** A construction adjusted until it produces a comfortable number is a fit, and
> the third attempt is where that becomes indistinguishable from one.

That paragraph names two different futures and only one of them is closed. **Trying a
third SHAPE on the same inputs is forbidden.** Building the shape the second
declaration itself said it would have used, once the missing items exist, is what the
same sentence instructs — it is the release, written into the bar at the time, by the
same hand, before any of this was in prospect.

The second declaration is explicit about which items were missing and why they decided
the shape:

> A full FCFF is not constructible here — the walk-forward projects revenue, cost,
> gross profit, overheads, finance cost and profit, but **no capital expenditure and no
> working capital**, and inventing either would be the fabrication this project refuses
> everywhere else.

**Those items are now committed.** [R-FCAL-01 AMENDED] requires every fundamental
walk-forward to commit a valuation-input block per origin — cash, interest-bearing
debt, PPE, D&A, the working-capital lines, the share count footed against its par
value, and capex disclosed or derived by the identity `capex = ΔPPE + D&A` and labelled
as derived. All five runs now carry one. The census that measured the gap is the same
instrument that now measures its closure: `python3 engine/valuation_calibration/bridge_inputs.py`,
read live, never from this file.

**This declaration is not triggered by a number.** No figure under it existed when it
was written; the trigger is the arrival of the inputs, which is a fact about the
repository and is checkable by anyone. That is the same test the second declaration set
itself — *the trigger is the rule, not the size of the number* — and it is why this
file is committed before the code that reads it.

**The bar carries forward and hardens.** If this construction fails, there is no fourth.
The finding then is that a mechanical valuation is not constructible from what these
runs commit even with the valuation-input block in hand, and that is reportable exactly
as it stands.

---

## What changes, and what deliberately does not

**The order-book floor is retired as the series (a) value.** It was a floor on one class
and could never be more than that: it valued the contracted book of a developer and
nothing else, so it was not comparable across the five names and it could not be a
measure of the house lean in either direction. It is still computed and still reported
beside the new series as a cross-check on the developer names, because a construction
that disappears cannot be compared with the one that replaced it.

**Fixed from declaration 2, unchanged, and not revisited here:** beta = 1.00 at every
origin and every name; point-in-time discipline absolute; an origin missing any input is
DROPPED and never filled; the macro comes from `engine/macro_history/` at that origin's
own vintage and from nowhere else.

---

## The construction

At origin *t*, for one name, using only what was published by that date.

### 1. The explicit window

The walk-forward's own projection at horizons **1 to 5**, run at that origin under its
own pre-registered mechanical rules with `macro="as_known"` — no foresight, no
judgement drivers. This is what series (a) is defined on and it is not re-derived here.

**Operating profit** is taken from the projection's own lines, named per run because the
five runs do not share a schema and a pattern loose enough to match all five would match
things that are not operating profit:

| run | EBIT is | D&A is |
|---|---|---|
| AMOC | `operating_profit` | `depreciation` |
| ARCC | `gross_profit − ga − provisions + reversals − impairments` | `mfg_dep + amort` |
| EGCH | `revenue − cost_of_sales − selling − admin − provisions + other_bucket` | **not projected** — see §2 |
| PHDC | `is.gross_profit − is.sga − is.admin_depr` | `is.admin_depr` |
| TMGH | `gross_profit + sga + da` (the run signs costs negative) | `−da` |

Where a run's projection carries D&A, **that** figure is used, because it is the
walk-forward's own mechanical output and substituting an intensity rule for it would be
replacing the thing being calibrated. EGCH is the one run whose projection carries no
separate D&A line — its depreciation sits inside cost of sales — and it takes the
intensity rule in §2. That is a named exception for a named reason, not a fallback
anybody may reach for.

### 2. Capex, working capital, and D&A where it is not projected

None of these is projected by any run but TMGH, so each is carried forward on a **fixed
intensity of the projection's own revenue**, the intensity being the **median of the
three fiscal years to the origin** read from that name's own valuation-input block and
its own as-reported panel:

- `capex_intensity` = median( capex / revenue ) over *t−2 … t*
- `wc_intensity` = median( working capital / revenue ) over *t−2 … t*
- `dep_intensity` = median( D&A / revenue ) over *t−2 … t* — **EGCH only**

Forward at horizon *h* on projected revenue *R<sub>h</sub>*:

- `capex_h = capex_intensity × R_h`
- `WC_h = wc_intensity × R_h`, and `ΔWC_h = WC_h − WC_{h−1}` with `WC_0` the origin's
  own actual working capital from the block
- `D&A_h = dep_intensity × R_h` — EGCH only

**Three years, median, fixed here.** Three because the block's own coverage will not
reliably support more at the early origins and a window that changes per cell is a free
parameter; median rather than mean because one exceptional capex year — TMGH's FY2024 at
twenty-three times the prior year — would otherwise set the whole forward path.

**Where a name's block carries a capex figure at fewer than three of the three years,
the origin is DROPPED.** Not filled from a neighbouring year, not substituted by
depreciation. TMGH's own projection carries a forward capex line; it is used where
present, and the intensity rule is the fallback for the names whose projection does not.

### 3. Free cash flow

`FCFF_h = NOPAT_h + D&A_h − capex_h − ΔWC_h`, where `NOPAT_h = EBIT_h × (1 − τ)`.

**One definition of free cash flow in the whole model**, explicit window and terminal
alike — [R-TERM-01]'s second, independent error is a model carrying two.

τ is the **statutory rate as each run committed it**: 22.5% from 2015 and 25% before
(PHDC's own committed regime rule, which is where it is sourced), except at EGCH origins
where that run's own `TAX_REGIME` governs because KIMA's rate is company-specific.

### 4. The discount rate, point-in-time

- **Ke** = `rf* + 1.00 × ERP`, where `rf* = sovereign_10y − default_spread` at that
  origin's own vintage. Country risk enters once, through the ERP.
- **Kd** = the company's **own effective rate**, computed as the origin year's finance
  charge over the **interest-bearing borrowings that actually bear it** — the block's
  `debt`, and nothing broader. [R-FCAL-01] trap (i) is the reason that denominator is
  named: dividing the charge by a wider liabilities total understates the rate by a
  multiple and manufactures a bias that looks exactly like evidence.
  **Floored at the origin's own sovereign yield**, because a same-currency corporate
  cannot borrow below its sovereign ([R-COC-01], a standing refusal). **Which bound each
  cell took is recorded**, so a book where the floor did the work is visible rather than
  buried in an average.
- **Weights are MARKET VALUE**: equity at the origin's close × the footed share count
  from the block; debt at the block's own figure. Never book equity.
- `WACC = w_e·Ke + w_d·Kd·(1 − τ)`.

**One rate for every explicit year and for the terminal.** A glide is what [R-COC-01]
requires of a *study*; it is a construction with its own anchors and this instrument has
no judgement-free way to build one at a 2016 origin. The flat rate is stated as the
simplification it is, and its direction is stated too: on a disinflating path a flat
crisis-level rate **understates** value, which runs the same way as the pessimism
hypothesis under test and is therefore recorded as a construction bias, not read as
evidence for it.

### 5. The terminal

Built **only** through `engine.terminal_value.build()`, the sanctioned module — the
construction `g × IC` cannot be expressed in it at all.

- `real_growth = 0.0`, fixed. This is what the house macro path returns for every
  terminal it builds, and at zero real growth the module charges exactly zero growth
  capital, by construction.
- `inflation` = the origin's own known forward inflation for the last explicit year,
  from the point-in-time archive.
- `maintenance_basis = 'disclosed_capex'`, `maintenance_capex` = the trailing median
  capex of §2 escalated to the last explicit year on that same known inflation path.
  **At zero real growth the asset base is constant in real terms, so the whole of that
  spend is maintenance by construction.** Where the trailing window contained genuine
  expansion this OVERSTATES maintenance and therefore UNDERSTATES the terminal, and that
  direction is stated rather than discovered later.
- `nopat`, `dna_book` and `working_capital` are the **last explicit year's**, which is
  the basis the module's own contract demands.
- A terminal the module **refuses** drops the origin. It is not floored, not retried on
  another basis, and not rebuilt by hand.

**No disclosed useful life is used and none is invented.** [R-TERM-01] requires the
`disclosed_life` basis to rest on a life from the accounting-policies note, and only one
of these five names has one on file. A life this desk chose is not a disclosed life, so
the `disclosed_capex` basis — which the module offers, and which rests on the company's
own committed capex — is the one taken.

### 6. The bridge, and what it is missing

`equity = Σ PV(FCFF_1..5) + PV(TV) + cash − debt`, cash and debt from the block, at the
origin's own balance sheet date. Discount factors are end-of-year, which is the
convention a record that declares nothing gets ([R-COC-01 AMENDED]) and this one
declares nothing else.

`per share = equity / the footed share count for that year`, never today's count carried
back.

**THE MINORITY INTEREST IS NOT DEDUCTED, BECAUSE NO RUN COMMITS IT.** [R-BRIDGE-01]
requires it deducted from equity value, and the valuation-input block as [R-FCAL-01
AMENDED] defines it does not name it. **The sign is known and it is upward**: every cell
with a real minority is overstated by that minority's share. It is recorded as a stated
bias on every cell, it is registered as the next item the block should carry, and it is
**not** estimated — that is the same refusal as the share count.

Associates are likewise not carried, in either direction, for the same reason.

---

## Fixed here, never fitted

beta = 1.00 · horizons 1–5 · intensity window 3 years, median · real growth 0.0 ·
maintenance basis `disclosed_capex` · one flat WACC · end-of-year factors ·
τ from each run's own committed regime · Kd floored at the sovereign · minority not
deducted and its sign stated · an origin missing any input is DROPPED

---

## What would make this the wrong instrument

- **If it does not resemble the as-delivered series** once that record is long enough
  to compare — the pre-registration's own falsifier, unchanged and unweakened.
- **If the pooled interval turns out to be driven by the construction biases rather
  than by the house.** Three are named above and all three point the same way — the flat
  crisis-level rate, maintenance charged at total trailing capex, and the terminal built
  with no disclosed life — so a negative pooled bias is **not by itself** evidence of a
  house lean, and the report must say which part of it these could account for.
- **If it fails as the first two did.** Then there is no fourth construction. The
  finding is that a mechanical valuation is not constructible from what these runs
  commit, and it is reported in those words.

---

*Committed before this construction was computed. The first and second declarations are
not edited; they stand as sealed, beside the runs that withdrew them.*
