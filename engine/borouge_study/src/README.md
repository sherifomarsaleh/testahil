# BOROUGE — primary source documents

## What is here, and what is not

Committed:
- `*.txt` — the extracted text of every primary document. **This is what the build reads.**
  `inputs_company.py` cites these page by page.
- `ADB_*.xlsx` — Abu Dhabi Securities Exchange monthly market-statistics workbooks, used
  only to cross-check traded shares and market capitalisation. Never a source for a
  reported figure.

Not committed:
- `*.pdf` — the 21 Borouge plc source documents themselves, 78 MB in total. They are
  excluded from git deliberately, and their absence does **not** weaken the provenance
  chain, because that chain is carried by hash rather than by storage.

## Why excluding the PDFs is safe

`../source_access.json` records, for each of the 21 documents:
- the exact URL on the company's own investor-relations library it was downloaded from,
- its size in bytes,
- its **SHA-256**.

`../verify_sources.py` re-downloads every one of them from that URL and asserts the hash
matches. On 9 August 2026 all 21 matched byte-for-byte. Anyone can re-run it:

```bash
cd engine/borouge_study && python3 verify_sources.py
```

A hash plus a public URL is a stronger provenance record than a committed binary: it
proves the copy the study read is the copy the company published, which a committed file
on its own cannot.

## Restoring the PDFs

`verify_sources.py` fetches each document as it checks it. To keep local copies, run it
and the files land under this directory; or fetch any single one from the URL in
`source_access.json`.

If a fetch fails, treat a 403/407 or a TLS error as an egress-proxy fault and check the
proxy before concluding the company's site is down — `www.borouge.com` sits behind a web
application firewall that rejects some request signatures while serving the document
paths in `source_access.json` normally.

## The four complete audited years

FY2022, FY2023, FY2024 and FY2025 were all obtained as full statutory sets. The model
carries FY2023–FY2025 as its three historical columns. FY2022 was read and is held as a
check rather than carried: it is the post-listing peak-price year, and including it would
flatter every through-cycle average the study takes. That exclusion is a stated judgement,
recorded in the study and in the bibliography, not a gap in the record.
