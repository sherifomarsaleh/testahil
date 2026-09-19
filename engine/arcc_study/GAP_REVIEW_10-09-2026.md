# ARCC — valuation gap review, 10 September 2026

**AUDITED CENTRAL: 77.1781**

**AUDITED GAP: +0.76%** against EGP 76.60, the latest known close (6 September 2026). The
study strikes at 77.00, where the gap is +0.23%. **Both are inside the ten per cent trigger
on either side**, so this name is not referred.

## Why this review exists at all, when the trigger is not breached

The review of 9 September audited a central of **69.2217** at a gap of −9.63%. The answer
has since moved to 77.1781 and that review now audits a number this study does not publish
— which is the failure the review gate exists to catch, whether or not the trigger is met.
This supersedes it.

## What moved, and what did not

The central moved on the house cost-of-capital work of 10 September, not on anything found
in this company: country risk is charged once and flat rather than multiplied by beta, and
the terminal rate is read from the house macro path. Nothing in the segment build changed.

**An external research pass was worked through on 10 September and it moved nothing.** What
it established, and where each item already sat:

| Finding | Status in this study |
|---|---|
| The Egyptian Competition Authority's production quota was cancelled in July 2025 | Already carried. The price path is an erosion path *because* the quota that supported price is gone |
| 12.6 Mt of dormant capacity under revival from H2 2026 | Already carried, at exactly that figure |
| Two new production licences, 1.5–2.0 Mt each | **NEW. Registered as sector supply**, 3.5 Mt at the midpoint, on top of the revival. Neither was awarded to this company |
| Industrial electricity tariffs up ~18% from April 2026 | Inside the reviewed half already. Price and cost ride one path here and the H1-2026 gross margin printed 40.5% against 40.6% for FY2025 — the company absorbed or passed it through, and the model is anchored on that half |
| Hydrogen injection targeting ~55% thermal substitution | **2031, outside this forecast window.** Recorded, not credited |
| Exports capped at 30% of production | No conflict. This study's clinker export share is a FY2025 audited actual of 33.77% on clinker production — a different denominator — tapering to 30.0% by FY2030 |
| Domestic cement ~EGP 3,900/t post-quota | Consistent with the erosion path already run |

## The gate that was broken, and had been since this morning

`driver_test.py` had raised on this study since the cost of equity moved to the split
premium: it looks up its rows by exact label, the premium row was renamed to say it had
been split, and the lookup refused. **The whole driver sweep had not run on ARCC since.**

Behind it sat a second defect the sweep then found. The published TOTAL premium was a typed
value that nothing in the workbook consumed — the discounting reads the two legs — so it
agreed with them by arithmetic nothing enforced. It is a formula over its own legs now, and
the mature leg is relabelled: it had called itself "of which", which this workbook's own
convention treats as an inert breakdown of a live total. After the split that is backwards.
The leg is what beta multiplies and the total is derived from it.

928 of 928 formula cells reproduce, 57 headline reconciliations, 145 driver assertions every
one in the asserted direction, 0 dead inputs.
