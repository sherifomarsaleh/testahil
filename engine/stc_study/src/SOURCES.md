# STC — primary sources, where they came from, and how to get them again

**Fetched 5 September 2026.** The PDFs themselves are not committed (20 MB); the text
extracted from them is, together with the exact URL each came from, because the container is
rebuilt from the repository and a session that cannot see how a source was reached will go
looking for it again. Finding them took several dead ends and those are recorded below.

Every file is Saudi Telecom Company's OWN consolidated financial statements — SIGCM clause 1
material, not an aggregator's restatement. The FY2025 and FY2024 sets carry an independent
auditor's report from Deloitte and Touche & Co.; the 2026 sets are the reviewed interims.

| file | period | source URL |
|---|---|---|
| `stc_Annual-2025-en.txt` | year ended 31 Dec 2025, audited | `https://www.stc.com/content/dam/groupsites/en/pdf/stc_Annual-2025-en.pdf` |
| `stc_Annual-2024-en.txt` | year ended 31 Dec 2024, audited | `https://www.stc.com/content/dam/groupsites/en/pdf/stc_Annual-2024-en.pdf` |
| `STC_FY2023_FS_en.txt` | year ended 31 Dec 2023, audited | `https://www.stc.com/content/dam/groupsites/ar/pdf/STC-2023-English-YE-FS-Final-Draft-AC-Copy-Final-Shared-with-report.pdf` |
| `financial-statementsQ1-2026En.txt` | three months to 31 Mar 2026, reviewed | `https://www.stc.com/content/dam/groupsites/en/pdf/financial-statementsQ1-2026En.pdf` |
| `financial-statementsQ2-2026En.txt` | six months to 30 Jun 2026, reviewed | `https://www.stc.com/content/dam/groupsites/en/pdf/financial-statementsQ2-2026En.pdf` |
| `EarningsPresentationQ4-2025En.txt` | FY2025 earnings presentation (COMPANY_IR) | `https://www.stc.com/content/dam/groupsites/en/pdf/EarningsPresentationQ4-2025En.pdf` |
| `EarningsPresentationQ2-2026En.txt` | H1-2026 earnings presentation (COMPANY_IR) | `https://www.stc.com/content/dam/groupsites/en/pdf/EarningsPresentationQ2-2026En.pdf` |

All five carry a real text layer (64k–396k characters over 23–112 pages), so no OCR was
needed; extraction was `pdftotext -layout`. Arithmetic remains the arbiter — anything that
does not foot gets re-read off the rendered pixels, whatever the extractor's confidence.

## The route, including what did not work

The investor-relations path in this study's own delivered document no longer resolves. Four
candidate URLs return the site's own 404 page **with HTTP 200**, which is worth recording
because a status code alone would have read as success:

- `www.stc.com.sa/content/stc/sa/en/personal/about-stc/investor-relations.html` → 404 page
- `www.stc.com.sa/en/investors` → 404 page (Arabic)
- `www.stc.com.sa/en/investor-relations` → 404 page (Arabic)
- `ir.stc.com.sa` → HTTP 200, and it is a Drupal **login screen** for the content-management
  system, not the public site. A 7.6 KB body that parses cleanly is not a source.

What worked: `www.stc.com.sa/sitemap.xml`, which lists the investor pages and redirects to
the group site at `www.stc.com`, whose financial-statements page carries every set back to
2010. The recent links sit inside an escaped JSON blob rather than as plain `href`s, so a
naive scrape of the rendered anchors finds only the pre-2017 files — unescape twice before
matching.

## The investor-relations channel WAS reachable, and four guessed URLs said otherwise

**Added 5 September 2026, and the correction matters more than the documents.** The section
above records four investor-relations URLs that return the site's own 404 page with HTTP 200,
and concluded that the path in the delivered study no longer resolves. That conclusion was
true of those four URLs and FALSE of the site: `www.stc.com.sa/sitemap.xml` lists an entire
investor section under `/content/stcgroupwebsite/sa/en/investors/`, including
`financial-reports/presentations-and-report.html`, which carries every earnings presentation
and call transcript back to 2017.

**Four probes failing is not evidence that a thing does not exist** — it is evidence that
four guesses were wrong, and the difference is exactly what [R-IND-01] means when it says
the first hypothesis on an empty result is that the probe did not run. The sitemap was
already the route that found the financial statements; nobody pointed it at the presentations.

The two most recent are now registered. They carry what no financial statement does: **mobile
and fixed subscriber counts by category**, which is the unit data SIGCM clause 2 asks for and
which the segment panel cannot supply.

## What is still needed before this study can be rebuilt

`stc_compute.py` imports `mc_v2`, renamed to `primitives` on 2 August 2026, so it does not
run. Its cost of capital predates the v2 method. Its central is a four-lens weighted blend
at 0.35 / 0.25 / 0.20 / 0.20 that [R-LENS-03] retires, and unlike the other blocked names
its class — telecom operator — IS in the lens registry, so this is the one name of the seven
unreadable studies whose lens architecture can be corrected today. There is no bibliography
document and no inputs register with four-field provenance: the delivered study was recovered
from project files on 8 August 2026 and its build scripts were never written to produce one.

The disclosed useful lives [R-TERM-01] needs are RANGES — buildings 25–50 years,
telecommunication network and equipment 3–30, other assets 2–20 (note 10, FY2025) — so the
life has to come from the identity, and note 10 gives what that needs: cost and the year's
own charge, by class, with a complete roll-forward. Land is disclosed separately at SAR
1,996 million (2024: 1,835), and capital work in progress is SAR 4,910,376 thousand
(2024: 3,829,207), both of which come out of the depreciable base. **Check [L-328]'s three
conditions on the policy note before trusting either identity** — that is where the last four
names stopped.
