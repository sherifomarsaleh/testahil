# ELEC — two lenses were fed numbers this model contradicts, and correcting them refuses the study

**09-09-2026 · internal · ELEC is HELD on SIGCM and nothing here reaches the live site ·
no published number has been changed**

## The defect, and it is not a judgement

Two of the four lenses were fed TYPED constants where the same model already forecasts
the quantity. [R-GAP-04](5): a lens fed a typed quantity the model computes elsewhere is
not an independent read; it is a second answer to a question already answered.

| lens | fed | the model's own forecast | worth |
|---|---:|---:|---:|
| normalised earnings power | `nd_mid = 6000.0` | `nd_path[3]` = **16,045** at the FY2028 year it takes its EBIT from | −0.4581 |
| book value | opening FY2025 book **4,100** | `eq_path[-1]` = **−2,078** at FY2030 | −0.2740 |

The normalised lens's own comment described the 6,000 as *"post-release, post-paydown
mid-cycle net debt"* — a deleveraging **this model does not contain.** Its forecast has net
debt RISING from 9,805 to 19,602 as the company funds losses. The comment described a
company the study is not modelling.

## What correcting them does, measured rather than estimated

    central          0.3357  ->  0.1978          against a spot of 2.08
    gap             -84.2%   ->  -90.5%

| lens | before | after |
|---|---:|---:|
| cash flow | 0.01 *(floored)* | 0.01 *(floored)* |
| relative | 0.05 *(floored)* | 0.05 *(floored)* |
| **normalised** | ~0.70 | **0.01 — floored** |
| book | 0.9092 | 0.9092 |

**THREE OF FOUR LENSES THEN SIT ON THEIR FLOORS AND THE BOOK LENS CARRIES THE WHOLE
ANSWER.** That is the finding. This model, fed its own forecasts throughout, says the
equity is worth approximately nothing, and the floors — which exist because limited
liability means equity cannot be worth less than zero — do the work the lenses used to.

## A second defect, found by the first

**Two of the four lenses carried no limited-liability floor at all.** The cash-flow lens
has been floored since the first edition (`eq_dcf` at zero, `dcf_ps` at 0.01) and the
relative lens at 0.05. The normalised and book lenses had none — which nobody noticed
while their inputs were typed numbers that could not go negative. Feeding them the model's
own forecasts made the normalised lens negative immediately, and **a negative lens is not
a deep-distress read; it is a claim the law does not permit.**

Three different floors across four lenses (0.00/0.01, 0.05, none, none) is itself
unexplained. The 0.05 predates the others and no record says why it differs.

## Why the study REFUSES on the corrections, and why that is not overridden

With them in, `central / spot` = **0.0951**, below the study's own plausibility band of
[0.10, 2.5], and `compute.py` raises rather than publishing.

**The band is not widened and the corrections are not dismissed.** [R-COC-01]: a check that
fires on work that is right is RE-POINTED, never widened. The band was already lowered
once, 0.25 → 0.10, with its own comment recording why: *"a deep-distress read is the
honest arithmetic for a 2.5x-levered name whose EV barely clears its net debt, not an
implausible model output."* Lowering it a second time, to admit the answer it was just
lowered to admit, is how a guard stops being one.

**The corrections are right, the band is right, and together they say this study cannot be
published on this basis.** A refusal is an answer — the same shape as
`terminal_value.TerminalRefused`, which this repository already treats as evidence rather
than an obstacle.

## What is needed, and it is a design question rather than a number

The corrections are NOT left in `compute.py`, so the tree stays buildable and every gate
stays green on a study that is HELD anyway. What they are worth is measured above rather
than estimated, so nothing is lost by waiting.

**The question is what this house publishes when a corrected model says an equity is worth
approximately nothing.** Three answers are defensible and they are different studies:

1. **Publish the floors as the answer**, with the plausibility band RE-POINTED to test
   whether the floors are binding and whether the study says so — rather than testing
   central-over-spot, which cannot distinguish "the model is broken" from "the model says
   this is worthless".
2. **Refuse the study outright**, as `TerminalRefused` does, and say ELEC cannot be valued
   on a going-concern basis while its own forecast takes equity negative.
3. **Value it as the option it is.** The equity of a company whose model says it is
   underwater is a call on recovery, and this study's own lens record already carries an
   *"EGP 0.01 option-value placeholder"* that nothing has ever priced.

None should be chosen at speed on the widest gap in the book, and the SIGCM hold means
none can issue tonight regardless.

## The margin question is separate and still open

Nothing above touches the FY2026 margin, which is the larger item: the study's 4.09%
is struck off the single worst quarter in the record, against a four-quarter mean of
30.1% gross, and the quarterly record the principal supplied falsifies the study's stated
under-absorption mechanism — Q3-25 and Q4-25 ran 28.8% and 23.3% EBITDA margins at revenue
BELOW the study's own FY2026E quarterly rate. Priced both ways the swing is EGP 2.59 a
share, 7.7x the entire published fair value. That belongs in the contested register,
priced, neither side averaged, and it is unaffected by any of the above.
