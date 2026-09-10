# check_published_gap resolves a ticker to a directory by lowercasing it, and one name does not survive that

**Found 08-09-2026 while diagnosing a CI red on PR #409. NOT that PR's defect — it
reproduces on `origin/main`'s own ratchet, `data.js` and price file.** Recorded first, then FIXED on the principal's
'do as you see fit' — with the fix proving, rather than asserting, that it is not a route
to green.

## The false message

`scripts/check_published_gap.py:84`

```python
def study_dir(ticker):
    d = os.path.join(ENGINE, "%s_study" % ticker.lower())
```

The site publishes **FERTIGLB**, so this resolves to `engine/fertiglb_study` — which does
not exist. The gate therefore reports:

> `FERTIGLB  -24.3%  no study directory, so nothing can carry a review`

**Both halves of that sentence are false.** `engine/fertiglobe_study/` exists and carries
`GAP_REVIEW_04-09-2026.md`, which audits a central of 1.8105 at a gap of −32.2%.

This is [L-355] exactly — a reader that guesses a naming convention silently finds nothing
and reports that as a result — and the repository has already solved this identical problem
once, for band records, with an **explicit asserted LEDGER_ALIAS, never inferred from a
filename**.

## Bounded, and that is the useful half

Every site ticker was held against every `*_study` directory. **FERTIGLOBE is the only real
mismatch**; the only other unresolved directory is XPT, platinum, excluded by construction
as a metal. So this is one alias, not a class of drift.

## What fixing it does and does NOT do

It converts a FALSE reason into a TRUE one and makes the gate MORE demanding, which is why
it is worth doing: with the alias, FERTIGLB resolves to a study whose review audits −32.2%
against a published −24.3%, a 7.9-point difference — beyond the 5-point staleness tolerance,
so the gate would still refuse, now saying the page is stale relative to the study, which is
[R-GAP-03]'s actual subject.

**IT DOES NOT MAKE CI GREEN AND MUST NOT BE MISTAKEN FOR A WAY TO.** The ratchet entry
excuses a deviation of 15.4% and the live breach is 24.3%; under [R-ENF-08] an entry excuses
a deviation only up to the size it recorded, the list may only ever SHORTEN, and the honest
routes to green are the page being refreshed (a publish, which is a separate explicitly
requested step) or the study's review being re-issued against the current gap.

## A prune was run and reverted, and that is recorded

`--prune` removed EMPOWER (genuinely no longer breaching) **and FERTIGLB** — after which the
same run immediately reported FERTIGLB as a NEW breach. A prune that shortens a list and a
breach test that re-adds the same name in one pass are disagreeing about one company under
two names. The prune was reverted; the ratchet is byte-identical to what it was.


---

## FIXED 08-09-2026, and the proof that it is not a route to green

`study_dir()` now resolves through an **explicit, asserted `STUDY_ALIAS`** rather than by
lowercasing — the shape `band_record.LEDGER_ALIAS` already uses for the same problem. It is
deliberately not a fuzzy or prefix match, because a name resolving to the WRONG study is
worse than one resolving to none, and `_assert_alias_targets_exist()` refuses at import if
an alias ever names a directory that is not there.

**The red stands, which is the point.** Before: `FERTIGLB -24.3% no study directory, so
nothing can carry a review` — false. After: `FERTIGLB -24.3% review GAP_REVIEW_04-09-2026.md
audits 1.8105; the site publishes 2.15 — the ratchet excuses a deviation of 15.4%; it is now
24.3% ... a materially WORSE breach on a listed name is a NEW breach [R-ENF-08]` — true, and
[R-GAP-03]'s actual subject.

## What this gate still lacks, recorded rather than built unsupervised

**It has no negative control.** Every other gate adopted under [R-ENF-01] carries one and
this one does not, so nothing has ever demonstrated that it fires on its own conditions —
which is the standing argument for controls, and it applies to the gate that just produced
today's only red.
