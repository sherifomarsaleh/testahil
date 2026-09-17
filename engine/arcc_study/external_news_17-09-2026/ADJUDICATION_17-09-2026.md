# ARCC — external news returns, adjudicated

**Received 2026-09-17.** Two returns, kept apart: **PERPLEXITY** (chat) and **GEMINI**
(Word document). Runbook step 4. No valuation figure has moved.

---

## 0. THE PROMPT WAS WRONG, AND BOTH ENGINES OBEYED IT

The prompt I issued told both engines that ARCC's information set "already covers everything
up to and including **FY2025, audited (2025-12-31)**". **That is false.** This study's own
committed bridge record reads:

    balance_sheet_date      = 2026-06-30
    latest_disclosed_date   = 2026-06-30
    latest_disclosed_source = the reviewed condensed consolidated interim financial statements
                              for the six months ended 30 June 2026, from the company's own
                              investor-relations channel

The generator read the study's `forecast_anchor` for the information-set end. **That field
names the latest reviewed period the FORECAST is anchored on; it is not the end of the
information set.** On this study the two differ by six months.

The cost was immediate and one-directional: Perplexity took "after early August 2026" as its
cutoff and **explicitly excluded the July 2026 treasury-share cancellation and capital
reduction as out of period** — a corporate action that changes the share count, i.e. exactly
the class of event that most deserves checking. (It turns out the study already had it
right; see §2. But the engine excluded it on my instruction, not on its own judgement.)

**Fixed in `engine/news_pack.py`** so the remaining six prompts do not repeat it.

---

## 1. THE REAL FINDING: ARCC's OWN WEBSITE IS REACHABLE, AND IT WAS NOT WHEN THIS STUDY WAS BUILT

`arabiancementcompany.com` returns **HTTP 200** from this environment on 2026-09-17. The
standing protocol carries this company as its worked example of the primary-source rule
precisely because the site "returned connect_rejected at the proxy this session" on
07-Aug-2026. **That blocker is open.** The full investor-relations tree is readable:

- 176 PDFs spanning 2015–2026: consolidated and standalone financials, earnings releases and
  investor presentations.
- **Q1 2026** consolidated, standalone and investor presentation (uploaded 2026/06).
- **Q2 2026** consolidated and standalone financials (uploaded 2026/08).
- **Q2 2026 Investor Presentation (uploaded 2026/09)** — see §3.

This is worth more than any lead in either return, and it is not a lead: I opened the
documents.

---

## 2. WHAT I VERIFIED AGAINST THE PRIMARY DOCUMENT, AND THE STUDY IS RIGHT

The 2Q2026 consolidated filing has **no usable text layer (20 characters across 20 pages)**,
the same condition as this company's FY2025 filing, so it was read by **OCR off the rendered
pixels at 300 dpi**. Page 4, the condensed consolidated interim statement of financial
position as of June 30, 2026, reads cleanly:

| Line | 30 June 2026 | 31 Dec 2025 |
|---|---|---|
| Issued and paid-up capital | **749,734,890** | 757,479,400 |
| Cash and bank balances | **1,970,501,140** | 3,459,391,229 |
| Total assets | 9,273,971,602 | 8,783,721,849 |
| Assets under construction | 897,084,167 | 391,543,753 |
| Inventories | 1,752,292,718 | 1,053,646,218 |
| Property, plant and equipment (net) | 2,478,746,697 | 2,522,323,523 |

Against what this study committed:

- **Share count.** 749,734,890 ÷ EGP 2 par = **374,867,445**. The bridge divides by
  `shares_mn = 374.867445`. **Foots exactly.** Gemini's table reports the same three figures
  independently. The treasury-share cancellation is consumed and correct.
- **Cash.** The bridge carries `plus cash and bank balances, 30 June 2026 = 1,970.50114`.
  **Matches the filing to the pound.**
- **Bridge date.** 2026-06-30, the latest disclosed. [R-BRIDGE-01] satisfied.

**Nothing here moves.** Recording that plainly matters: a check that only ever reports
defects teaches nobody what a clean result looks like.

---

## 3. WHAT IS GENUINELY UNCONSUMED — THE Q2 2026 INVESTOR PRESENTATION

Uploaded to the company's own site in **September 2026**, after the 3 September re-strike.
It has a clean text layer and it carries **the operating anchors the statements never do** —
which is the standing rule that results releases are swept *with* their statements. Read
directly, 1H2026 against 1H2025:

| Volumes (K tons) | 1H2026 | 1H2025 | |
|---|---|---|---|
| Local sales | 1,596.8 | 1,466.0 | +9% |
| Cement exports | 271.3 | 247.4 | +10% |
| Clinker exports | 269.3 | 549.5 | **−51%** |
| **Total volumes** | **2,137.4** | 2,263.0 | **−6%** |
| Clinker production | 1,897.0 | 1,754.7 | +8% |
| Clinker utilisation | 90% | 84% | |
| Cement utilisation | 68% | 74% | |

| Financial | 1H2026 | 1H2025 | |
|---|---|---|---|
| Total revenues (EGP mn) | 6,008 | 5,446 | +10% |
| **Revenue per ton (EGP)** | **2,811** | 2,407 | **+17%** |
| **Cash cost per ton (EGP)** | **1,565** | 1,407 | +11% |
| Cash gross profit margin | **44%** | 42% | |
| EBITDA (EGP mn) | 2,854 | 1,162 | +146% |
| Net profit (EGP mn) | **2,159** | 1,394 | +55% |

**Two of this study's ten committed drivers are named in that table** — sales volume (Mt) and
realised price (EGP/t) — at a granularity the study's FY2025 base cannot reach.

### 3.1 The flag this raises, stated as a question and not as a finding

The standing anchor rule fires where a forecast opens **materially below** the latest
reviewed period, at a relative 5%. This study's forecast opens on a gross margin of
**39.03%**. The company's own 1H2026 **cash** gross margin is **44%**; deducting the
disclosed 1H2026 D&A of EGP 159mn on revenue of 6,008mn (2.6pp) puts the comparable figure
near **41.4%** — **about 6% relative above the forecast's opening year.**

**That is a flag, not a verdict, and the difference matters.** "Cash gross profit" as the
company defines it and "gross margin" as this study builds it are not established to be the
same measure, and until they are reconciled on one basis the comparison is suggestive only.
What it does establish is that the question must be asked against a document the study has
not read. The register also records the study's own last sweep as 2026-08-06 — before this
presentation existed.

### 3.2 An unresolved discrepancy between two of the company's own documents

Gemini reports 1H2026 consolidated net profit of **EGP 2,172,453,474**, precise to the pound.
The company's own investor presentation reports **EGP 2,159mn**. The gap is ~13mn, 0.6% —
**too large to be rounding**. Most likely consolidated versus attributable, but that is a
guess. **It is resolved from the statements or not at all**, and neither figure is used here.

---

## 4. THE OTHER LEADS, UNTRACED

| Lead | Return | Status |
|---|---|---|
| **EGX30 removal effective 1 Sep 2026** (with ORWE, OIH and Kima) | Perplexity | Untraced — EGX refuses from here. Market structure, not operations. Does **not** touch the beta method: the regressor is the published index of the exchange the stock is listed on, never the index the stock belongs to. |
| **EGX Listing Committee, EGP 20,000, repeated Article 38 non-compliance** | Perplexity | Untraced. Financially negligible; a disclosure-control datapoint only. |
| **Ministry of Industry roundtable, 16 Sep 2026** — national capacity 75.5 Mt, directive to reactivate idle kilns and raise exports, relaxing the ECA quota regime in force since July 2021 | Gemini | Untraced, and the **most consequential** of the untraced items: it bears directly on the volume driver. Needs the ministry's own release. Note the company's 1H2026 cement utilisation is **68% and falling**, which is the constraint such a directive would relieve. |
| **Alternative fuel, Ramliya Line 2 complete, 25 t/h, up to 40% substitution, 18% TSR run-rate** | both | Perplexity's source is a **contractor's LinkedIn post**; Gemini asserts an 18% run-rate without one I can open. Bears on the fuel driver. Untraced. |
| **Cement quoted at EGP 3,830–3,860/t, early September** | both | Retail/market quotes, not ARCC realised price. Gemini's four-grade ex-factory/retail table is a market survey, not a company disclosure. The study's realised price is EGP 2,811/t in 1H2026 on the company's own figures — **a different quantity from a bagged retail quote**, and conflating them would overstate revenue by a third. Do not model. |

**Both returns agree** on no management change, no new debt facility beyond the existing EBRD
loan, no litigation, no new licence. Two engines agreeing on an absence neither can source.

---

## 5. WHAT MAY NOT ENTER

- Gemini's four-grade price table, and any retail cement quote, as realised price (§4).
- Gemini's H1 2026 figures as historicals — they come to it through press and vendors. **The
  statements are on the company's own site and reachable**; that is where they come from.
- Any CBE policy-rate or sovereign-yield reading from either return: the house macro path owns
  those, on a named institution's publication.
