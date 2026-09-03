# [R-LENS-03] holds in the records and fails in the documents

**3 September 2026.** Found while building EGCH's [R-ENF-05] output records. No
number moves here; what moves is the count of studies that are actually compliant,
from twenty-four to six.

## What was measured

[R-LENS-03] retired the typed multi-lens blend on 02-09-2026: **one class primary
IS the central**, every other lens is a cross-check published beside it. It is
enforced by `assert_lens_design()` over each study's committed `lens_record`, and
that gate is green.

A reader does not receive the lens record. They receive a PDF. Scanning the latest
delivered document of every study:

| | |
|---|---:|
| delivered documents on disk | 20 |
| carrying no weighted-blend claim | **6** |
| publishing a weighted central as the study's own answer | **14** |

The six clean are ADNOCDIST, BOROUGE, FERTIGLOBE, PHAR, PHDC and TMGH — the last
two being the studies WS3 migrated by hand.

## The two that matter most

**ARCC, re-issued 02-09-2026 — after the rule.** Its lens record names the
cash-flow lens as the primary and its numbers file carries EGP 53.46. Its
delivered document prints:

> END — this study's weighted central **54.65** · four lenses, weighted
> … Other three lenses −0.73 · **50/20/22/8 weights** and share count

Two different centrals in one delivery, and the one a reader sees is the retired
construction.

**ADNOCLS — the model report.** Twenty-two assertions, including its own synthesis
row: *"Weighted central: discounted cash flow 40% · relative 25% · normalised
…"*. This is the deepest form of the problem. `CLAUDE.md` instructs that the model
report is opened **beside** the study being written and that every study matches
its sections, content and depth. So until ADNOCLS's own edition is rebuilt, the
exemplar is teaching the retired architecture to every study that follows, and a
new study can be fully compliant with the instruction it was given and in breach
of the rule.

## Why every gate missed it

Each gate was looking at the thing it was built to look at, and the thing a reader
receives was not it:

- `check_lens_design.py` reads `lens_record` — conformant.
- `check_workbook_structure.py` reads sheet names — conformant.
- the external-reader scrub looks for **internal-procedure vocabulary**; "weighted
  central" is not internal vocabulary, it is a perfectly ordinary phrase, and the
  scrub was right not to flag it.
- the recalculation gates reconcile the workbook to itself — and a blend
  recalculates perfectly.

This is [R-ENF-03] restated: *a checker that models the artefact is checking a
different file from the one that ships.* That rule was adopted for a JavaScript
parse and never generalised to the documents.

## What was built

`scripts/check_lens_vocabulary.py` reads the **delivered PDF** and flags a
weighted blend asserted as the study's own central. It deliberately does **not**
flag a study for *describing* the retirement — a document that says "the retired
blend weighted a justified price-to-book of zero at 15%" is doing exactly what the
rule wants, and a gate that went red on it would be the check that cries wolf
which [R-CAL-02] names as the one everybody learns to ignore. A hit is discounted
when a retirement marker sits within 260 characters of it, and the negative
control carries that case explicitly, alongside PHDC's and TMGH's own conforming
sentences.

Ratcheted at the fourteen; the list may only shorten, one entry per re-issue.
Negative-controlled on six defect conditions and four clean ones. In CI.

## What this does to the WS8 queue

WS8 was "re-issue the five on the new standard". This says the standard has a
second half nobody had counted: **a study is not migrated until its DOCUMENT
carries one primary as the central.** ARCC and AMOC were re-issued after
[R-LENS-03] and neither document was. PHDC and TMGH are the only two that are, and
they are the two that were rebuilt end to end rather than patched.

ADNOCLS goes to the front of that queue rather than the back, because it is the
one whose staleness propagates.

## What would overturn this

If the fourteen documents turn out to publish the blend only as a **labelled
cross-check** beside a primary — the construction [R-LENS-03] permits — then the
gate is reading a table caption as an answer and the rule for discounting a hit
needs widening rather than the studies needing re-issue. The test is reading them,
and on the two checked closely (ARCC and AMOC) the blend is the answer, not a
cross-check.
