# DU (Emirates Integrated Telecommunications Company PJSC) — primary source documents

## What is here

- `FS_FY2025.pdf` / `FS_FY2025.txt` — FY2025 audited consolidated financial statements,
  KPMG Lower Gulf, unmodified opinion 9 February 2026.
- `FS_FY2024.pdf` / `FS_FY2024.txt` — FY2024 audited consolidated financial statements,
  held as the prior-year cross-check on the accounting-policies note.

The `.txt` is `pdftotext -layout` output and is what the reading was done from; the `.pdf`
is the document itself. `../source_access.json` records the public URL on the company's own
investor-relations library, the byte count and the SHA-256 of each.

## Two independent fetches of the same two documents, byte-identical

These files were placed here on 6 September 2026 and, within the same hour, fetched again
independently from the URLs in `../source_access.json` while sourcing the disclosed useful
life. **Every one of the four blobs hashes identically between the two fetches** — same
SHA-256, same git blob id. Two routes to the same bytes is stronger provenance than either
route alone, and it is recorded here rather than assumed.

## Route, and why the text layer is trusted here

The FY2025 filing carries a real text layer — 209,686 characters across 66 pages, Microsoft
Word producer — so the ARCC condition that forced OCR off the rendered pixels (47 characters
across 47 pages) does not hold. **Arithmetic is the arbiter, not the extractor's confidence**:
notes 6, 7 and 8 were footed against their own printed totals in three directions in both
years — every movement row down each class column, every class row across to the Total
column, and cost less accumulated depreciation against printed net book value — 38 tests, no
break, and the printed net book values are the figures `study_numbers.json` had already
committed independently as `ppe_fy25` and `ppe_fy24`.

A column of useful lives has no arithmetic to foot against, so the ranges themselves were
additionally read off the rendered pixels (`pdftoppm -r 150`, PDF pages 18 and 19 of the
FY2025 filing and PDF page 18 of the FY2024 filing, read as images). Pixels and text layer
agree exactly on every range.

## What the sourcing found

`engine/valuation_calibration/disclosed_lives.json`, entry `DU`. In short: the lives are
disclosed as RANGES per class; the class carrying 98.9% of the depreciating base discloses
3-25 years; and no note in either filing discloses a carrying amount for the six
plant-and-equipment sub-classes the FY2024 filing names separately. The lives and the weights
are disclosed at different levels of aggregation, so **no single disclosed life can be read
off the accounts** — the weighted band is 3.00 to 23.93 years, and picking a point inside it
is this desk choosing a life, which [R-TERM-01] refuses (SIGCM clause 1).
