# Cells that wrap mid-number in a delivered document

**03-Sep-2026. Found by rendering the PDFs and reading the text back, not by any gate.**

A table cell one character too narrow wraps, and Word breaks after a hyphen — so a
negative number renders as **a bare dash with the digits on the line beneath**, which a
reader takes for a positive figure or for a dash meaning "not applicable". A percent sign
orphans the same way. **The sign or the magnitude of a printed figure changes as it is
read, from a purely typographic cause.**

`column_audit` reports these tables CLEAN and is right by its own lights: it measures
whether a column is starved or bloated across the table, and this is a property of ONE
CELL, one character wider than its neighbours. An average cannot see one row.

## Detected across every delivered study, current editions only

| study | the row above | the orphan |
|---|---|---|
| **PHDC** 03-09 | `Order book, closing 352,564 446,131 …` | `1` `8` — **FIXED** |
| ADNOCDRILL 09-08 | `Group 4,903 100.0 2,19` | `%` |
| ADNOCLS 09-08 | `12 vessels` | `2028` |
| ARCC 03-09 | `CIB credit facilities 100` | `20.60%` |
| ARCC 03-09 | `National Bank of Egypt / KfW 146` | `5.49%` |
| EMPOWER 09-08 | `NOPAT at 9% / at 15% —` | `1,061 1,172 1,252 1,325` |
| FERTIGLOBE 09-08 | `Four-year aggregate cash rate` | `2025` |
| TMGH 02-09 | `Development revenue 21,579 24,518` | `7` |

## What was fixed and what was learned

PHDC's is closed. **The first widening was not enough and the second measurement says
why:** at a 4.0cm label the cost row fitted and the order-book row did not — its cells are
`1,152,921` and `1,658,388`, **nine** characters against the cost row's eight. The fix
looked complete because the row that provoked it was fixed. **A column has to clear the
widest cell in the TABLE, not the widest cell in the row somebody was looking at.**

A non-breaking minus (U+2212) was tried first and made it *worse* — it is typographically
correct and offers no break, and it is **wider** than a hyphen, so every cell in the row
then wrapped mid-number. Per [R-COC-01], when a fix makes the thing worse the diagnosis was
wrong.

## The remaining seven

Each is in a study that is **not being re-issued in this pass**, and rebuilding a delivered
document to move a column is not a change worth making on its own — it would produce a new
edition of seven studies for a layout fix. **They get it at their next re-issue**, and this
file is the list. The detector is eight lines of pdftotext and is worth making a gate once
the list is short enough that it would not be red on arrival.
