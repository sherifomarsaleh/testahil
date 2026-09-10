# PHAR — valuation-gap review, 8 September 2026  [R-GAP-01]

**AUDITED CENTRAL: 31.3738** — Frame A, provision charge permanent at 5.25% of revenue
**AUDITED CENTRAL: 47.6035** — Frame B, provision charge normalising to 2.5% of revenue

**AUDITED GAP: -75.4%** (Frame A) · Frame B -62.6%

**A two-sided answer is audited on EVERY branch.** Both are stated above and both are
audited below; a review naming one of two answers has audited half the study.

**Why a new review one day after the last one.** The 7 September review audited Frame A at
32.9975 and Frame B at 49.6789 and audited them honestly. One further lever has since been
applied and both branches have moved, so those markers no longer name the answers this
study publishes. The gaps themselves moved 1.3 and 1.6 points — well inside the five-point
staleness tolerance — so **nothing in the earlier review's substance is withdrawn**; what
follows re-runs the eight headings against the new numbers and says, heading by heading,
what the lever changed and what it did not.

**The lever, and it is one.** The beta was re-derived against the published index of the
exchange this stock is listed on, replacing an equal-weight composite of 36 covered EGX
names. Frame A 32.9975 → 31.3738 (−4.9%), Frame B 49.6789 → 47.6035 (−4.2%).

**Outcome.** THE ANSWER IS AUDITED AND IT MOVED FURTHER FROM THE PRICE. Both branches
still breach the trigger, this study remains **HELD** under [R-GAP-02], and no market
dissent is filed, because the honest conclusion is unchanged: the gap is not explained.

---

## The correction made today, before the eight headings

**The beta was regressed against a composite, and the beta was typed.** The input carried a
literal 0.629 with a source describing an equal-weighted basket of 36 Egyptian listed names
built from the covered price library. Two defects sat in that one line, and the second is
why the first survived: SIGCM clause 6 calls a constituent composite a HARD FAIL rather
than a fallback — it changes whenever a stock is posted and it shares constituents with the
panel it prices, so it is a coverage artefact and not a market — and because the number was
typed, re-running the regression to any answer at all would have left the model discounting
at the old one.

Resolved through `beta_regression.own_stock_beta()` against `raw_indices/EG/EGX30.csv` as
at 8 September 2026: **beta 0.6658, R-squared 0.143, n = 256, standard error 0.1355, 90%
interval [0.443, 0.889]**, Dimson-corrected and matched to the exchange's own trading week.

**THE UNCOMFORTABLE PART, RECORDED RATHER THAN LEFT OUT: the withdrawn composite FIT
BETTER.** It gave 0.6295 at an R-squared of **0.235** against the conforming 0.143. That is
exactly what a coverage artefact does — a basket that shares constituents with the panel it
prices will track a member of that panel more closely than a blue-chip index does — and **a
better fit against the wrong regressor is not evidence for the wrong regressor.** The rule
is not a preference about goodness of fit; it is about what the regressor IS. Both figures
are published in the input register, with their statistics, so a reader can see the trade.

A beta below one remains what a defensive, price-regulated, domestically-consumed staple
should produce, and the conforming figure is still comfortably below one.

---

## 1. LATEST FILINGS — **still NOT cleared, and unchanged by this lever**

The most recent period the model consumes is Q1-2026, reviewed. EIPICO publishes annual
reports on its own investor-relations page and **no interim statement in any year**, the
exchange disclosure portal does not resolve and neither does the regulator's. If an H1-2026
was lodged with the exchange, the bridge stands on a superseded balance sheet. That is a
property of this company's own disclosure and of the routes available from here, and it
cannot be cleared from here. The 7 September retrieval closed the pre-2022 archive — seven
fiscal years of audited consolidated accounts, FY2019–FY2025, where three had stood.

## 2. BASE YEAR — **cleared, and untouched by this lever**

The base year foots to the filed periods; nothing is annualised, scaled or solved. A beta
correction reaches the discount rate and no line of the base year.

## 3. MACRO COHERENCE — **cleared**

Inflation, currency and price sit on the house Egyptian path and the study carries no
inflation number of its own. Untouched.

## 4. DISCOUNT RATE — **this is the heading the lever sits in, and it is stronger than it was**

Country risk enters exactly once — the risk-free is normalised by this sovereign's own
default spread on the same basis as the premium added back. Weights are market-value. The
schedule glides rather than sitting at a single crisis-level rate.

What changed is the beta, and with it the cost of equity and every rate built on it. The
construction is now attested rather than asserted: the committed record carries the index
file, its as-of date, the market, the exchange and the conforming flag, so
`assert_beta_provenance()` inspects the record instead of trusting a boolean the study set
on itself — which is the shape this rule exists to close, and the shape this study was in.

**The interval is wide and saying so is part of the audit.** The 90% interval on the
conforming beta runs 0.443 to 0.889, and this study's value is materially sensitive across
that span. The point estimate is used; the interval is published beside it and is not
narrowed by choosing the regressor that happened to fit better.

## 5. TERMINAL — **cleared, and the 7 September correction stands**

The terminal is built through the sanctioned module on a disclosed asset life, and the
defect found on 7 September — a cash flow handed to the module already grown a year, which
the module then grew again — remains corrected. The beta lever raises the terminal discount
rate and therefore shrinks the terminal's share of value, which is the arithmetic working
in the direction it should.

## 6. BALANCE SHEET — **conditionally cleared, unchanged**

The bridge stands on the audited 31-December-2025 sheet, which is the sheet the forecast
opens from; the minority is taken after the reviewed 31-March-2026 sheet because the
subsidiary carrying essentially all of it was deconsolidated in the first quarter of 2026 —
a change in the group's PERIMETER rather than a movement in a balance. The condition on
this heading is heading 1's: if an H1-2026 exists at the exchange, the sheet is superseded.

**This edition also commits the bridge as a RECORD for the first time**, and it surfaced
the largest deviation in the file: the associates are carried at 11× normalised earnings
plus the active-ingredient plant at cost, EGP 2,978.5mn against a disclosed carrying value
of EGP 675.9mn — 4.4× book, and **EGP 13.65 a share of a EGP 31.37 Frame A central**. The
rule admits market or book and this is neither. It is recorded under the basis it actually
uses rather than relabelled, and carrying the associates at book instead would take Frame A
to EGP 17.72 and Frame B to EGP 33.95. **It is not corrected in this pass** — whether an
unlisted associate contributing disclosed earnings is worth its carrying cost is a lens
question with its own rule — and it is now the second sharpest unexplained thing in the
file after heading 8.

## 7. CLAIMS AGAINST THE RECORD — **cleared**

Every superlative reproduces from the filed series. The lever adds one claim and it is
checked here: **"the composite fit better"** reproduces as R-squared 0.235 against 0.143,
and **"the composite understated the beta by 5.8%"** as 0.6658/0.6295 − 1. Neither is
typed; both are computed in `beta_reg.py` from the two regression records and printed.

## 8. MULTIPLE CROSS-CHECK — **STILL NOT CLEARED, and this lever makes it harder again**

Frame A at EGP 31.37 implies **3.67×** trailing FY2025 attributable earnings, against 3.86×
before this lever and 4.29× before the one on 7 September. Frame B at 47.60 implies
**5.57×**, against 5.82× and 6.35×. The market pays 14.90×.

**This is the heading every correction hurts, and that is the finding rather than a
complaint about it.** Frame B is now below every year of this company's own four-year
history except the 2022 low; Frame A is below all four. A generic manufacturer with a third
of its revenue in hard currency, a newly licensed biosimilars plant and no distress on its
balance sheet does not trade at under four times earnings unless the model is asserting
something the market is not. Each correction was required and each moved this study
further from both the price AND its own history — **and two consecutive levers running the
same way is the pattern worth naming, even though neither was chosen for its direction.**

---

## What this review concludes

**The answer is audited and it does not change for the price.** The correction was required
by a standing rule, it was taken on the filings, and it would have been taken had it landed
the other way.

**What a reader should weigh, stated plainly:** the beta's own 90% interval is wide enough
to matter to this valuation and the regressor that fits this stock best is the one the rule
forbids; the associates carry EGP 13.65 a share on a basis the bridge rule does not admit;
the most recent period consumed is Q1-2026 because this company publishes no interims; and
the implied earnings multiple now sits below this company's own filed history on both
branches. **This study remains HELD and nothing here reaches the live site.**
