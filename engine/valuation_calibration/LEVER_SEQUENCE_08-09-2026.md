# The six levers, run in their written order — 08-09-2026

The pre-registration fixed six levers **in this order, before any score existed**, and
requires each to be evaluated one at a time on the current stack and promoted **only
while the stacked pooled bias moves toward zero**. None had ever been run. This is that
sequence, complete, with every reading printed by `score_cashflow.py` whether it was
promoted or not — a lever tried and rejected is evidence; a lever tried in silence is not.

## Result

| # | lever | pooled bias | vs stack | verdict |
|---|---|---|---|---|
| — | **declared run** | **+0.7880** | — | baseline |
| 1 | cost-of-capital glide | +1.0078 | **away** | **rejected** |
| 2 | terminal anchors | +0.8831 | **away** | **rejected** |
| 3 | rating-basis equity risk premium | **+0.7844** | toward, −0.0036 | **promoted** |
| 4 | country-premium lambda | — | — | **unbuildable, recorded** |
| 5 | beta shrinkage, on the stack {3} | +0.8114 | **away** | **rejected** |
| 6 | the lens set | — | — | **unbuildable, recorded** |

**Final stack: {3}. Pooled bias +0.7844, block-4 95% CI [+0.5970, +0.9671].** The interval
excludes zero at every block. **Criterion 3 clause A is NOT MET and the pre-registered
lever set does not reach it.**

## What each one turned out to be

**1 — the glide.** Built from the origin's *own* published forward inflation path, so the
front-loading is inherited from the disinflation that origin could actually see. 21 of 34
cells glide; the other 13 are **flat with a reason**, which is [R-COC-01]'s own language
for a market already at its terminal — Egypt in 2019 and 2021 published 7% for ever and
nothing then licensed a glide. Flat rather than dropped is also the only honest way to
evaluate a lever: dropping the cells it cannot build would compare a 15-cell mean against
a 9-cell one and call the difference the lever.

It moves the bias **away** from zero, and that is the finding rather than a
disappointment. **The declared run discounts five explicit years and a perpetuity at one
crisis-level rate — exactly what [R-COC-01] makes inexpressible in a delivered study — and
correcting it makes the calibration worse.** The wrong discount rate was silently
offsetting the margin-expansion error measured beside it. Two errors pointing opposite
ways is not a model that works; it is a model whose failure is hidden.

**2 — the terminal anchors.** Same direction, same reason, smaller.

**3 — the ERP basis.** The archive carries both bases at every vintage. Switching also
strips the *rating* default spread rather than the swap one — rating-to-rating, because
mixing them counts the sovereign on two measuring sticks, which is the double-count
[R-COC-01] exists to stop arriving through a side door. **Promoted, and worth 0.0036.**

**4 — the country-premium lambda. Unbuildable at these origins, and that is recorded
rather than skipped [R-ENF-04].** Lambda scales the *country* premium inside the equity
premium; the point-in-time archive holds only the **total** premium per vintage. Backing
the mature figure out by subtracting the default spread assumes the equity-to-bond scaling
is 1.00 — *which is the very quantity lambda is an alternative to*, so it would assume the
answer. It needs the implied mature premium by year, which nothing here holds: the extract
carries Egypt's rating, its default spread and both of its totals, and no US row.

**5 — beta shrinkage.** The declared run's 1.00 is the **full-shrinkage limit** — all
prior, no own history. Built the other end: point-in-time regressions through
`beta_regression.own_stock_beta()` with an `asof`, so the window ends at the origin and
sees only what had printed. The shrinkage weight is **measured, never chosen** — Vasicek
against the cross-sectional dispersion of every usable beta in the market's own library at
that same date (29–35 names, SD 0.27–0.31), so a noisy beta is pulled hard and a precise
one barely moves. Rejected on the stack.

*Its first stacked run read identical to lever 3 alone, and that was a bug rather than a
result:* the ERP branch recomputed the cost of equity from the flat constant and silently
discarded the beta beneath it. Caught by asserting the reading differed before believing
it — the same discipline that has caught four fixtures in this repository that never
injected their condition.

**6 — the lens set. Unbuildable at these origins, and the reason is the one adopted this
morning.** A per-origin block commits cash, debt, PPE, depreciation, capex, working
capital and shares. Every alternative primary the registry permits needs something else:
RNAV needs a land bank **at each origin**, and [R-ASSET-01] established today that the one
developer with a committed land bank commits it at a **single date**; replacement cost
needs a capacity or fleet vintage; an EV multiple on own history needs point-in-time
multiples nothing archives. Book value **is** constructible and may not be used — a
disclosed floor, never weighted, [R-LENS-03].

## The reading taken, stated because it is a reading

"Promotion stops the moment it would" is read as the **overshoot** the rule names in its
own next sentence — *"stacking five individually-justified moves into an overshoot"* — so
a lever that simply points the wrong way is not promoted and the sequence continues. The
alternative reading halts everything at lever 1, and would have left levers 3 to 6
untested on the strength of the first one failing.

## Where the bias actually is

Under lever 5 in isolation, **leave-one-name-out without ARCC reads +0.0240 over seven
cells and three names.** Three of the four names are essentially unbiased. ARCC alone
carries it, and its cause is already measured and committed beside this file: revenue
escalating at the full inflation ladder against cost lines held in the wrong currency and
at the wrong unit. **That is an input's specification, not the valuation construction's,
and no lever on this list can reach it** — which is what the six levers were run to
establish, and now have.
