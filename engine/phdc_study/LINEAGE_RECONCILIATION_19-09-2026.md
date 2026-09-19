# PHDC — what the two lineages each found, and what is owed

Recorded 19-09-2026, in the commit that reconciles the two protocol lineages.
This is a RECORD OF OUTSTANDING WORK, not a valuation. Nothing here moves a number.

## The fork

Both lineages descend from the same study of 3 September 2026, central **EGP 17.8478**
against a spot of 14.40. `compute.py` is byte-identical on both sides at that commit.
Each lineage then produced its own next edition, and neither saw the other:

| | edition | central | what it did |
|---|---|---|---|
| trunk | 10-09-2026 | 21.0897 | applied the terminal-rate correction, **+20.6%** |
| side branch | 17-09-2026 | 18.9737 | applied the bridge and conversion corrections, **−7.8%** then **−15.45%**, then the 2% real rate |

**These are not two scenarios and must never be presented as a choice.** They are two
half-updates of one study. Each applied a correction the other did not know about.

## What each lineage is missing, measured

**The 10-09 edition is missing the reviewed half.** Its bridge stands on the balance sheet
of **31 March 2026** and its committed numbers contain **no reference at all** to the
reviewed statements to **30 June 2026** — which exist, which the company published, and
which the side branch read (114 references). That is the stale-sheet defect [R-BRIDGE-01]
was adopted on, in the study this house has rebuilt most often.

Two corrections rest on that document and are owed:

1. **[R-BRIDGE-01] — the bridge onto the reviewed 30-June-2026 balance sheet.**
   Measured on the side branch: 17.8478 → 16.4551, **−7.80%**.
2. **[R-ANCHOR-01] — the cash-conversion rate onto the reviewed half.** The base case was
   the MEAN of three full-year conversion rates (4.333%, 17.870%, 3.938%) — a three-year
   average standing in for a rate the company has since reported. Measured: 16.4551 →
   13.9129, **−15.45%**.

Two further levers were applied on the side branch and moved the value by nothing: the
gross-margin anchor onto the reviewed half ([R-ANCHOR-01]) and the envelope onto one
driver and one clock ([R-LENS-03]). They are still corrections and are still owed.

**The 17-09 edition is missing the terminal-rate correction** the trunk applied on 10-09,
worth **+20.6%**, and was built against a rule layer thirteen rules short of the one this
repository now carries.

## What was done here, and what was not

The trunk's study is kept as the base, because it conforms to the current rule layer. The
side branch's 17-09 documents, workbook and bibliography are **withdrawn from the tree**:
they publish EGP 18.9737, which is not a number either lineage will end at, and leaving
them beside the 10-09 edition would put two centrals in one directory with nothing saying
which stands.

**PHDC is therefore not finished.** It owes ONE rebuild carrying BOTH lineages' corrections
— the trunk's terminal rate and the side branch's reviewed-half evidence — on the current
rule layer, with its rebuild ledger recording the levers in the order applied per
[R-REBUILD-01]. Until that rebuild lands, the committed central of 21.0897 stands on a
balance sheet that has been superseded, and this file is the record that somebody knows it.

The corrections are **not deferred because any rule forbids applying them**
([R-REBUILD-01 CLAUSE TWO]: "the guard forbids it" is not a reason). They are deferred
because the rebuild is its own pass and this commit is a merge.
