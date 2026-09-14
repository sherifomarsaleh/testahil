#!/usr/bin/env python3
"""SCEM walk-forward — every source attempt, including the ones that failed.

[R-FCAL-01] requires the Sweep Register to log every source attempt including
failures, and L-007 says a site that will not load is a fact worth recording.
The failure that matters here is the Arabic FY2021 filing: its figures are set in
Eastern Arabic numerals and no OCR route available in this environment reads them,
so FY2020 is LEFT OUT and the window is shortened rather than filled from a vendor.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
IR = "https://sinaicement.com/wp-content/uploads/"

ATTEMPTS = [
 dict(target="sinaicement.com homepage", url="https://sinaicement.com/",
      date="2026-09-07", outcome="SUCCESS — HTTP 200",
      note="the company's own website, tried FIRST per the primary-source rule (L-007). "
           "It carries every published filing as a direct PDF link from the homepage: no "
           "authentication, no portal, no investor-relations sub-site to navigate. This is "
           "the fact the first two editions of the SCEM study did not establish before "
           "taking their historicals from trade press."),
 dict(target="SCC-AFS-E-1225.pdf — audited FY2025", url=IR + "2026/06/SCC-AFS-E-1225.pdf",
      date="2026-09-04", outcome="SUCCESS", note="already on disk from the study rebuild"),
 dict(target="SCC-AFS-E-1224.pdf — audited FY2024", url=IR + "2025/05/SCC-AFS-E-1224.pdf",
      date="2026-09-04", outcome="SUCCESS", note="already on disk from the study rebuild"),
 dict(target="SCC-AFS-E-0326.pdf — reviewed Q1-2026", url=IR + "2026/06/SCC-AFS-E-0326.pdf",
      date="2026-09-04", outcome="SUCCESS", note="already on disk from the study rebuild"),
 dict(target="SCC-AFS-E-1223.pdf — audited FY2023", url=IR + "2025/05/SCC-AFS-E-1223.pdf",
      date="2026-09-07", outcome="SUCCESS — 2,647,622 bytes, 30 pages",
      note="NOT PREVIOUSLY DOWNLOADED. It carries FY2023 as its own year and FY2022 as "
           "the comparative column, and it is what takes this run's span from three "
           "fiscal years to five."),
 dict(target="SCC-AFS-E-1222.pdf — audited FY2022", url=IR + "2025/05/SCC-AFS-E-1222.pdf",
      date="2026-09-07", outcome="SUCCESS — 1,101,601 bytes, 33 pages",
      note="NOT PREVIOUSLY DOWNLOADED. FY2022 own year, FY2021 comparative column."),
 dict(target="SCC-AFS-A-1221.pdf — audited FY2021, ARABIC",
      url=IR + "2025/05/SCC-AFS-A-1221.pdf",
      date="2026-09-07",
      outcome="DOWNLOADED AND UNREADABLE — FY2020 IS NOT SOURCED AND THE WINDOW IS "
              "SHORTENED",
      note="The document downloads (921,494 bytes, 36 pages) and its Arabic PROSE reads "
           "well under tesseract's Arabic model — the income statement's own caption "
           "renders as 'قائمة الدخل المستقلة'. Its FIGURES do not: they are Eastern Arabic "
           "numerals and both the English and the Arabic model return letters where the "
           "digits are, so not one number on the statement pages can be read by any route "
           "available here. Under the English model the page returns ZERO figures matching "
           "a thousands-separated pattern, which is the check that settled it. FY2020 is "
           "therefore left out: a fabricated cell corrupts the very error this run scores, "
           "and an interpolated year would have been invisible in the pooled result "
           "afterwards. WHAT WOULD CLOSE IT: an Arabic-Indic digit OCR model, or the "
           "company publishing an English FY2021 filing."),
 dict(target="EGX disclosure portal, older filings", url="https://www.egx.com.eg/",
      date="2026-09-07",
      outcome="NOT ATTEMPTED — the company's own site is the primary source and it "
              "publishes exactly six documents",
      note="Recorded rather than left silent. The prior study's own sweep register "
           "(finding F21) logs the EGX portal as refused by egress policy on the earlier "
           "attempt. Nothing older than FY2021 is obtainable from the issuer, so the span "
           "is a fact about the archive rather than about the effort."),
 dict(target="volume, tonnage, capacity or utilisation in any filing",
      url="the six filings themselves",
      date="2026-09-07",
      outcome="NEGATIVE SEARCH — NOTHING FOUND",
      note="Searched every OCR'd page of the FY2022 and FY2023 filings for tonne, tons, "
           "capacity and utilisation: no physical quantity is disclosed anywhere, in any "
           "year. This issuer's finest DISCLOSED level is the cost-note line, not the "
           "tonne, and SIGCM clause 2's flag is raised rather than a tonnage being "
           "imported from a plant register and treated as the company's own figure."),
]

if __name__ == '__main__':
    json.dump(ATTEMPTS, open(os.path.join(HERE, 'fetch_attempts.json'), 'w'), indent=1)
    ok = sum(1 for a in ATTEMPTS if a['outcome'].startswith('SUCCESS'))
    print('%d source attempts logged, %d succeeded, %d recorded as failures or negative '
          'searches' % (len(ATTEMPTS), ok, len(ATTEMPTS) - ok))
