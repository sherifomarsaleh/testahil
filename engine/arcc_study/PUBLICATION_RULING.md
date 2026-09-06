# ARCC — PUBLICATION RULED ON, 6 September 2026

Closes escalation `ARCC-publication-held-by-R-GAP-02` in `engine/escalations.json`.

**The ruling: MERGE AND PUBLISH the 6-September roll-forward.** Given by the principal
in chat on 6 September 2026, in answer to a registered escalation carrying a
recommendation, a default and a default date. This file exists because an answer living
only in a conversation binds nothing — the container is rebuilt from the repository, and
a session that cannot see the ruling will ask for it again [R-IND-01].

## What was held, and by what

`scripts/check_publish_block.py` refused ARCC at step 0/6 of `publish_site.py`:

> the central is -13.1% below the price of 76.60 (2026-09-06), past the 10%
> publication limit — and no market dissent is filed

Two conditions of [R-GAP-02] were open at once:

1. **The gap.** Study central **EGP 66.53** against the 06-09-2026 close of **76.60**.
   No `MARKET_DISSENT` exists for any name on any live ref — the release that rule
   provides has never been exercised.
2. **The method.** Clause three's second condition: Phase 1 acceptance criteria **#3
   RUNNING** (the valuation calibration's pooled bias CI, which cannot mature until the
   first vintages resolve) and **#4 NOT MET**. Book-wide the gate cleared nobody.

## Why the ruling does not weaken the rule

**What this publish moves, and what it does not.** Diffed through a real JavaScript parse,
this branch against `origin/main`:

| field | main | this branch |
|---|---|---|
| `fair{bear,base,full}` | 49.53 / 54.65 / 61.71 | **unchanged** |
| `spot` | 59.00 (6 Aug) | 76.60 (6 Sep) |
| `dist` | 1M window expired 06-09-2026 | 1M to 06-10, 3M to 06-12 |
| `levels.res` | 60.34 / 62.00 / 63.00 | 78.00 / 80.00 / 91.72 |

**The quantity [R-GAP-02] holds does not move.** The valuation claim that disagrees with
the market is already live, at exactly the numbers it already carries, and this change
leaves every one of them alone. What ships is a current spot, a current cone, a current
technical read and one graded row.

**And what was live was defective by this project's own standing rule.** Before this
merge testahil.com served ARCC at a month-stale 59.00 against a traded 76.60, a 1-month
cone whose window had already expired, and three published resistances — 60.34, 62.00,
63.00 — **every one of them below the actual price**. That is the exact shape of the
29-Jul-2026 COMI defect the technical-read rule was written to close: *"when the library
moves, the technical read moves with it, IN THE SAME PASS."* Holding the merge kept that
page up. Publishing it fixed a live defect without advancing the held valuation one inch.

[R-GAP-02] also exempts this act in terms: *"WHAT IT DOES NOT HOLD is internal work:
rebuilding, auditing, re-issuing to the principal and merging to main all continue,
because this gate governs ISSUING A REPORT and publishing to the live site."*

## What was NOT done, and why it matters that it was not

**No dissent was manufactured.** A `MARKET_DISSENT` was the available release and it was
declined on the evidence rather than on effort. ARCC rose roughly 30% in a month on heavy
volume into a limit-up on 11-08-2026 — an ordinary re-rating. [R-GAP-02] states that *a
reverse read landing on a believable number is evidence AGAINST the dissent and the study
stays held*, and that is the case here. Writing one would have been manufacturing the
release rather than earning it.

**No valuation number was touched.** Closing the gap by moving the central toward the
price is the reverse-engineered rate the cost-of-capital procedure prohibits outright.
`fair{}`, the slider's factor-stack constants, `market_profiles.py` and
`fitted_configs.json` were all left exactly as they stood.

**The block was not routed around.** `publish_site.py --ticker ARCC --ship --republish`
refuses at step 0/6 and was never bypassed. The merge happened on an explicit ruling from
the principal, recorded here, not on an operator's reading of a carve-out. **A gate that
can be reasoned past by whoever is standing in front of it is not a gate** — so the gate
still refuses ARCC today, and it should. It will keep refusing until the gap closes or the
method proves, and the next session must not read this ruling as a precedent for any other
name or any later edition.

## Scope of this ruling

It covers **this roll-forward only** — the 6-September cone, grade, technical read and
calibration record for ARCC. It is **not** a release of the study, **not** a finding about
the gap, and **not** a precedent. A later ARCC edition, or any other held name, needs its
own ruling or its own release.

## What remains open

- ARCC's central still sits ~13% below the traded price. The study is still held for
  publication of its *valuation*; the gap gate and `GAP_REVIEW_03-09-2026.md` (audited
  central 66.53, audited gap −13.6%) remain the live record of it.
- Phase 1 acceptance criteria #3 and #4 remain open, and hold the book.
- The gap may close without anyone acting: the price moved ~30% in a month while the
  central did not move at all.
