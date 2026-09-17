# GBCO — the lever order for the audit rebuild, declared before any figure is recomputed

[R-REBUILD-01] requires the levers of a rebuild to be ordered **before** any figure moves and
the running total read at each step, with the audit point **declared in advance**. This file is
committed in its own commit, ahead of every recomputed number, so that the order is a fact about
the commit graph rather than an assurance. It is the discipline used on PHDC earlier in this
session and it is used here for the same reason: findings 2, 11 and 12 all move the GB Auto leg
and interact, so a rebuild that applies them and reports one number has published a result
nobody can decompose.

**Authorisation:** the principal's approval of bucket 5 option 1 — *"Keep both branches and
relabel, then implement the findings. But call the branches something understandable"* — on the
response in `CRITIQUE_RESPONSE_17-09-2026.md`.

---

## 1. THE TWO BRANCHES, RELABELLED

Finding 1 is accepted in full: the US$1,400mn round is **not** one of GB Corp's own two
disclosures. `mnt_halan_stake_source` cites the company's 9-June release for the **41.61%
stake**; `mnt_halan_round_usd` carries **no source field at all**, and the 19-entry input
register holds neither the round, nor the associates line, nor EGP/USD. The round price is not
thereby worthless — it is a recent primary transaction and a legitimate reference — but it
cannot be called a company disclosure, and the labels said it was.

| was | is, from this edition |
|---|---|
| "B — the reviewed carrying value" | **the associate at its carrying value** — what GB Corp's own reviewed 30-June-2026 accounts carry the MNT-Halan stake at |
| "A — the round price" | **the associate at the round price** — what the June-2026 funding round implies for the same stake: a price set by other investors in a transaction GB Corp took part in and **has never adopted as its own carrying value** |

Both are published, side by side, exactly as now. What is retired is the framing that called
them two company disclosures.

**The ledger's tracked quantity changes with them.** Every committed artefact in this study
already declares the **carrying** branch as `published_central` (41.3484); the rebuild ledger has
been walking the **round** branch (52.3453). That is an inconsistency in the ledger, not a new
decision, and it is corrected as the first lever of this pass with its full arithmetic move
recorded rather than absorbed.

---

## 2. THE LEVER ORDER

Numbering continues the existing `rebuild_ledger.json`, which walks the route from the delivered
08-07-2026 edition (L1–L9). This pass is L10 onwards.

**Inputs before constructions.** A wrong number and a wrong method are not the same kind of
correction, and putting the inputs first means the construction levers are measured against a
model whose inputs are already right — otherwise the two are confounded and neither can be read.

| # | lever | finding | rule it serves |
|---|---|---|---|
| **L10** | the ledger tracks the study's **declared central** — the carrying branch | 1 | bookkeeping · [R-ENF-06] |
| **L11** | the associate carrying value: 15,733.523 → **15,723.523** | 16 | SIGCM clause 1 |
| **L12** | GB Auto net debt to **the company's own published 14,493.6** | 24 / self-audit S-2 | [R-BRIDGE-01] |
| **L13** | the GB Capital Dec-25 base on a **consistent restated basis** | 8 | SIGCM clause 1 (like for like) |
| **L14** | the **fifth GB Auto revenue line carried, not zeroed** | 5 | SIGCM clause 2 (the record covers 100% of revenue) |
| **L15** | the **working-capital anchor**: the walk and the bridge on one date, the intensity held at the latest reviewed level | 2 | [R-ANCHOR-01] · [R-BRIDGE-01] |
| **L16** | **one capital structure throughout** — GB Auto's own debt book and its own cost of debt | 11 | [R-COC-01] |

### What L15 actually does, stated now rather than after

Three parts, because finding 2's complaint is *"two balance-sheet dates in one calculation"* and
only the first of the three is the audit's own remedy:

- **(a) the opening stock.** `WC_OPENING` moves from the 31-Dec-2025 stock to the 30-June-2026
  stock, so the walk starts where the bridge stands.
- **(b) the intensity ladder is held flat** at the latest reviewed level, rather than gliding to
  a typed 21.5%. [R-ANCHOR-01] permits a drift away from the latest reviewed actual only where a
  mechanism from a closed list has a **measured like-for-like direction in the company's own
  period pair**. The study's stated mechanism has two halves and the company's own conversion
  cycle (`asset_cycle.json`, built this session from the disclosed segment tables, every table
  footed) **measures them in opposite directions**: the stock build is unwinding (DIO 149.0 →
  127.1 days, the claim holds) while payables are **shortening**, not re-extending (DPO 112.7 →
  83.3 days, the claim is contradicted). Net, the cash cycle got **worse**, 61.3 → 69.3 days. A
  mechanism contradicted by the company's own filings is not a mechanism.
- **(c) the first forecast period.** If the walk starts at 30 June 2026 and the bridge is struck
  at 30 June 2026, then discounting a **full** FY2026E free cash flow counts the first half of
  2026 twice — once in the net debt the bridge already deducts, and once in the FY26E cash flow.
  This is a defect the implementation surfaces rather than one the audit raised; it is inside
  finding 2's own scope, because it is the same two-dates-in-one-calculation error one layer
  down. It is priced, and if the correction is taken the discounting convention is **declared**
  per [R-COC-01 AMENDED] rather than left to the end-of-year default.

### What L16 actually does

GB Auto's leg is valued with a bridge on **GB Auto's** net debt, so the rate that discounts it
must be **GB Auto's**: its own debt book in the weights and its own cost of debt, not the
group's. Market-value equity weights are required by [R-COC-01] and a segment's equity has no
quoted price, so the weight is taken to a **fixed point** — the leg is valued, its own equity
value becomes the weight, and the loop is iterated to convergence. That is reproducible
arithmetic rather than a chosen number.

---

## 3. THE AUDIT POINT, DECLARED IN ADVANCE

**Two stops, plus one standing trigger.**

1. **After L14** — the inputs are complete and the constructions have not yet been touched. The
   running total is read here so that the construction levers are measured against a clean base.
2. **After L16** — the constructions are complete. The running total is read before any document
   is rebuilt.
3. **Standing, at every lever:** if the running total passes **±10% of the latest known price**
   in either direction, [R-GAP-01]'s eight-heading review is written **before** any file is
   staged. The carrying branch begins this pass at **+42.7%** against EGP 28.98, so the trigger
   is already live and the review is owed whatever the levers do; what the stops decide is
   whether it is written once or twice.

**The price.** The latest committed close is **EGP 28.98 as at 3 September 2026**, which is
**fourteen days old** at this rebuild's date. [R-GAP-01 AMENDED 07-09-2026] requires the price to
be asked for at the start and the work to route around the answer rather than wait for it; the
standing default where none arrives is the latest committed price **used with its date stated and
its age disclosed**, which is what this rebuild does. This is also finding 15's accepted remedy —
the defect is accepted, the audit's fix is not executable in this container, and the house rule
is the stricter one.

---

## 4. WHAT THIS PASS DOES NOT DO

The non-value findings — the expert appendix arithmetic (3, 7, 33, 34), the disclosure repairs
(4, 22, 23, 25, 27, 30), the document/workbook defects (6, 9, 10, 17, 18, 19, 20, 21, 26, 28,
29, 32) and the absent constructions (S-1, S-5, S-6, S-7) — move no figure in the valuation and
are therefore not levers. They are implemented after the levers land, against the rebuilt
numbers, and are listed in the completion report rather than in this ledger.

Findings 14 and 31 stay in bucket 3, unproven and research-required. Findings 15, 25 and the
fix-half of 1 stay in bucket 2, defect accepted and fix rejected with the reason on the record.
