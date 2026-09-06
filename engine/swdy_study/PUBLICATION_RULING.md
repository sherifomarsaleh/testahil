# SWDY — PUBLICATION RULED ON, 6 September 2026

Closes escalation `SWDY-publish-blocked-by-gap-and-method` in `engine/escalations.json`.

**The ruling: PUBLISH the 6-September roll-forward — the MC cone, the technical read and
the ledger.** Given by the principal in chat on 6 September 2026, in answer to a
registered escalation carrying a recommendation, a default and a default date, and in
these terms:

> *"What we are doing here is a MC calibration that has nothing to do with the
> fundamental analysis. Go ahead and publish the prices to update the MC section and the
> ledger."*

This file exists because an answer living only in a conversation binds nothing — the
container is rebuilt from the repository, and a session that cannot see the ruling will
ask for it again [R-IND-01].

## What was held, and by what

`scripts/check_publish_block.py` refused SWDY at step 0/6 of `publish_site.py`:

> the central is -59.3% below the price of 136.20 (2026-09-06), past the 10%
> publication limit — and no market dissent is filed

Two conditions of [R-GAP-02] were open at once:

1. **The gap.** Study central **EGP 55.48** against the 06-09-2026 close of **136.20**.
   No `MARKET_DISSENT` exists for any name on any live ref.
2. **The method.** Clause three's second condition: Phase 1 acceptance criteria #3 and #4
   open. Book-wide the gate cleared nobody.

## HALF OF THIS WAS SETTLED AS A RULE THE SAME DAY, AND ONLY HALF

While this branch was in flight, **[R-GAP-02 AMENDED 06-Sep-2026]** landed on main in
#375 — adopted, per its own commit, on the identical instruction that produced this
ruling: *"this is a MC calibration that has nothing to do with the fundamental
analysis."* It exempts a publish that moves no fair value from the **METHOD** hold, on an
arithmetic condition: the entry the publish would write must carry the same `fair{}` and
the same `files{}` as the entry already on `origin/main`, read on both sides through a
real JavaScript parse [R-ENF-03].

**SWDY meets that condition and the gate now says so.** Re-run after merging the
amendment, `check_publish_block.py --ticker SWDY` reports **`0 HELD on the method`** where
it previously held on both. That half is no longer a ruling at all — it is the rule.

**The amendment does NOT release the gap half, in terms, and SWDY is held on the gap.**
The same gate still reports `1 HELD on the gap (more than 10% BELOW the price)`. So what
this ruling actually covers, after the amendment, is narrower than when it was given: the
gap half alone. The rest of this file is written against that narrower claim.

## The ruling's reasoning, which is a LENS argument and not an exception

[R-LENS-01] holds that the fundamental study, the MC price engine and the technical read
are INDEPENDENT lenses. This change is entirely the second and third of them. Diffed
through a real JavaScript parse, this branch against `origin/main` at the time of merge:

| field | main | this branch |
|---|---|---|
| `fair{bear,base,full}` | 19.95 / 69.73 / 138.73 | **byte-identical, unchanged** |
| `spot` | 105.20 (5 Aug) | 136.20 (6 Sep) |
| `dist` | 1M window expired 06-09-2026 | 1M to 06-10, 3M to 06-12 |
| `levels.res` | 110 / 114.50 / 120 | 139.50 / 150 / 160 |
| ledger | cycle-1 1M open, matured, ungraded | graded; cycle-2 1M and 3M struck |

**The quantity [R-GAP-02] holds does not move.** The valuation claim that disagrees with
the market is already live at exactly the numbers it already carries, and this change
leaves every one of them alone.

**And what was live was defective by this project's own standing rule.** Before this merge
testahil.com served SWDY at a month-stale 105.20 against a traded 136.20, a 1-month cone
whose window had already expired on 6 September, and three published resistances — 110,
114.50, 120 — **every one of them below the actual price**. That is the exact shape of the
29-Jul-2026 COMI defect the technical-read rule was written to close: *"when the library
moves, the technical read moves with it, IN THE SAME PASS."* Holding the merge kept that
page up.

## The honest part: the carve-out does NOT authorise this, the ruling does

[R-GAP-02] carves out internal work — *"rebuilding, auditing, re-issuing to the principal
and merging to main all continue, because this gate governs ISSUING A REPORT and
publishing to the live site."* **That carve-out rests on main not being live, and in this
repository that is false**: `.github/workflows/deploy-pages.yml` fires on any push to
`main`, so merging IS publishing. A parallel session recorded the same objection the same
day and it is recorded here rather than leaned on.

So this merge is not justified by the carve-out. It is justified by the principal's
explicit ruling, on a lens argument, given after the block was reported with its numbers
and its two available releases. The gate was not routed around: `check_publish_block.py`
still refuses SWDY, still should, and was neither weakened, skipped nor deleted.

## What was NOT done, and why it matters that it was not

**No dissent was manufactured.** A `MARKET_DISSENT` was the available release and it was
declined on the evidence. `GAP_REVIEW_06-09-2026.md` found that the market at 136.20 pays
**7.3x FY2027E EBITDA against the 6.5x this study itself calls justified** — a believable
multiple, and [R-GAP-02] states that a reverse read landing on a believable number is
evidence AGAINST the dissent. Writing one would have been manufacturing the release.

**No fair value moved toward the price.** The central is EGP 55.48 before and after, and
every residual the gap review left open — the cost of debt below its own sovereign, the
terminal risk-free 200bp under the house derivation — runs AWAY from the price.

**Scope.** This ruling covers the 6-September cone, grade, technical read and calibration
record for SWDY ONLY. It is not a release of the study, not a finding about the gap, and
**not a precedent for another name or a later edition**. The study remains HELD.

## What a reader sees, stated rather than discovered later

The live page will carry `fair{base 69.73}` beside a spot of 136.20 — a displayed
disagreement that widens from -34% to -49% purely because the spot caught up. Two things
about that number are worth recording and neither is changed here:

- **69.73 is not this study's current answer.** The committed central is **55.48**. The
  site's `fair{}` is a full edition behind.
- **69.73 is a RETIRED construction.** The entry's own note describes it as a *"Four-lens
  weighted central"*, and [R-LENS-03] retired the typed multi-lens blend outright: one
  class primary IS the central, the others are cross-checks.

Both predate this change and both survive it untouched, because moving `fair{}` is a study
re-issue and is exactly the act [R-GAP-02] holds. They are registered here so the next
session reads them rather than rediscovering them.
