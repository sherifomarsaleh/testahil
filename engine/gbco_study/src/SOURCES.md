# GBCO — the filings, and how they were finally reached

**7 September 2026.** This file is the resolving artefact named by
`engine/escalations.json` → `GBCO-audited-statements-not-reachable-from-this-container`
(`resolves_when.file`). **THE ANSWER IS WRITTEN WHERE THE NEXT SESSION READS IT** — into the
artefact that held the block, not into a conversation, because the container is rebuilt from
the repository and a session that cannot see an answer asks the question again [R-IND-01].

## The block is closed

**GB Corp's audited financial statements are reachable and are now held.** SIGCM clause 1 is
met on this name for the first time: every historical figure the study and the walk-forward
consume comes from a document GB Corp published itself.

## Why the earlier ladder concluded otherwise, and what it actually established

The 5-September escalation ran six routes and recorded them accurately. Re-run today, as
[R-IND-01] requires of any probe whose failure is relied on:

| host | recorded 05-09 | measured 07-09 |
|---|---|---|
| `gbauto.com` | "403, a Cloudflare 'Just a moment' challenge — the host exists" | it exists and **is not GB Corp**: 301 → `sedo.com/search/details/?domain=gbauto.com`, a domain-sales lander. The challenge was the parking service's. |
| `gb-corp.com` | "fails to connect (curl 000)" | HTTP 200 — and also a parking lander (`window.location.href="/lander"`) |
| `egx.com.eg` | F5 bot interstitial | unchanged: curl 000 today |
| `disclosure.efsa.gov.eg`, `mist.gov.eg` | do not resolve | unchanged |
| `web.archive.org` | unreachable | unchanged |
| **`gb-corporation.com` / `ir.gb-corporation.com`** | **never tried** | **HTTP 200, 277KB and 109KB — GB Corp's own site and its own investor-relations portal, no authentication, no challenge** |

**THE LADDER WAS CLIMBED CAREFULLY AND IT GUESSED A NAMING CONVENTION.** Every route was real
and every outcome was honestly recorded; the hostname list was assembled from what the company
used to be called. The headless-browser control in that entry remains valid and remains
useful — it is what stopped "the site blocks us" being written down as a fact — and it was
answering a question about the wrong host.

## What is held, and the route each came by

All under `engine/gbco_study/src/`, downloaded from `https://ir.gb-corporation.com`:

| set | files | route |
|---|---|---|
| audited consolidated statements | 31 Dec 2020, 2021, 2022, 2023, 2024, 2025 | FY2020 and FY2021 carry a text layer; **FY2022–FY2025 carry NONE (0 characters across 51–60 pages)** and the same audited statements are reproduced inside the annual report for those years, which do — so the annual report is the ROUTE and the audited statement is the DOCUMENT |
| reviewed interim statements | 31 Mar 2026, 30 Jun 2026 (consolidated) | scanned, no text layer |
| annual reports | 2013–2025 | PDF text layer |
| earnings releases | 4Q20, 4Q21, 4Q22, 4Q23, 4Q24, 4Q25, **1Q26, 2Q26** | PDF text layer |
| investor presentation | 1Q26 | PDF text layer |

**ARITHMETIC IS THE ARBITER.** Fourteen fiscal years, FY2012–FY2025, each footed against the
statement's own additions before entering the panel (`engine/gbco_walkforward/build_panel.py`
prints FOOTS or BROKEN per year; all fourteen foot).

## One thing found in the filings that nothing else would have surfaced

**The FY2025 audit opinion is QUALIFIED.** The auditors state they were not provided with the
consolidated audited financial statements of MNT-BV (MNT-Halan) for 2025 and that the group's
~44% share of its profit rests on management-prepared statements. That associate carries 58%
of this study's equity value and 86% of GB Corp's traded market capitalisation.

## What is still not held

- Audited statements for **FY2018 and FY2019**: GB Corp's own filings index begins at 31 March
  2020, and the annual reports for those years lay the statements out numbers-first in a split
  two-column form the text layer cannot attach to labels. The affected balance-sheet items are
  recorded as **missing with that reason** in `engine/gbco_walkforward/valuation_inputs.json`,
  never estimated.
- A **disclosed useful life**. See `engine/gbco_study/useful_lives.json`: the policy note gives
  rate ranges only and the derived identity contradicts them. STOP AND INFORM stands.
