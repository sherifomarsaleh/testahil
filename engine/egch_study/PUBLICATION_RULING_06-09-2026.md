# EGCH — publication ruling, 6 September 2026

**Status: the study remains HELD. The 6-September roll-forward was published.**

## What was blocked, and by what

`scripts/publish_site.py` refused EGCH at STEP 0/6 on two independent grounds, both of
which **still stand and are not released by this ruling**:

| rule | condition |
|---|---|
| **[R-GAP-02]** | both branches of the two-sided answer sit more than 10% below the latest known price — EGP 4.0396 at **−71.6%** and EGP 8.0388 at **−43.5%** against a close of 14.23 on 6 September 2026 — and no `MARKET_DISSENT` is filed |
| **[R-GAP-02 clause three]** | Phase 1 is not proven; 2 of 6 acceptance criteria are open, one of which cannot mature until the first vintages resolve |

Book-wide on that date the gate reported **0 of 93 may publish**.

## The ruling

Put to the principal with the arithmetic. The ruling was: **publish — "the cone refresh is
not the study."**

## Why the ruling is consistent with what shipped

This was verified against the diff rather than accepted on the description. Between this
branch and `main`:

- **no study document, workbook or bibliography is touched** — zero files matching
  `_study/`, `.docx`, `.pdf` or `.xlsx` appear in the diff;
- **no diff line matches `fair{`, `CONT_FIXED`, `EV_FIXED` or `GEO_MEAN`** — zero, counted;
- EGCH's published `fair{bear:0, base:3.64, full:15.47}` is **byte-identical** on this
  branch and on `main`.

What reached the live site is the price cone, the spot and its date, the technical read and
chart, one **graded** ledger row and the cycle-2 strike. The held valuation reaches no
reader it was not already reaching, and it reaches them at exactly the number it already
carried.

## Scope — deliberately narrow

The ruling scopes what [R-GAP-02] *governs*: issuing a valuation. It says a roll-forward
that moves no valuation number is not that act.

It was given **for this action**. It is **not** recorded as a standing amendment to
[R-GAP-02], and nothing here changes the rule's text, its ratchet, its enforcement or its
negative control. Making it bind generally is a rule change and needs its own instruction
through the protocol path — a carve-out written down by whoever is publishing, on the day
they want to publish, is the shape of exemption this method exists to prevent.

## What is still owed on this name

The site's `fair{}` is a full edition behind the study, whose 5 September edition publishes
4.0396 and 8.0388 against the 3.64 the site carries. Moving it is a study refresh on the
study's own clock, not a roll-forward, and it is still subject to both holds above.

<!-- PUBLICATION RULING RECORDED — 06-09-2026 -->
