# PHDC — external news pass, 17 September 2026

**Step 3 of the recalibration runbook.** Window: 25 June 2026 to 17 September 2026. TWO
returns supplied by the principal and kept apart, as the step requires: one from Perplexity,
one from Gemini (delivered as a research document). Where they agree on something neither can
source, that is two models agreeing and not evidence.

**WHAT COMES BACK IS A LEAD, NEVER AN INPUT.** Every item below is classified by whether it
reached a PRIMARY document. Only one did — and it corrects both returns *and* this session.

---

## 1 · THE ONE THING THAT TRACED, AND IT CORRECTS EVERYBODY

**The land bank is 46 million square meters as at 31 March 2026.**

| source | figure | status |
|---|---|---|
| the study as delivered | 33.0 as at 31-12-2024 | superseded |
| **this session's correction, this morning** | **37.0 as at 30-06-2025** | **WRONG — a year stale** |
| Perplexity return | 38, "Egypt and the UAE" | press, not admissible |
| Gemini return | 40.5, "verified" | press and a corporate-profile page, not admissible |
| **PHD 1Q2026 earnings release, Cairo 20 May 2026** | **46.0 as at 31-03-2026** | **PRIMARY — adopted** |

Retrieved from the company's own investor-relations result centre, in the SAME boilerplate
sentence that carried the 33 and the 37: *"one of the most diversified land bank portfolios in
Egypt and Abu Dhabi, spreading over 46 million square meters."* Against the delivered 33.0 the
understatement was **28.3%**.

**THE PART THAT MATTERS MOST IS WHERE IT WAS FOUND.** This study **already consumes that
release** — it is cited in `inputs.py` as `ER26Q1` and eight committed inputs come from it:
backlog 263,000, new sales 52,000, the Village de la Capitale launch, revenue 9,300, gross
profit 3,300, the year-on-year rate and net profit after tax. The study read the release
carefully **for its results tables and never read its "About the company" paragraph**, which
is where the land bank is stated. All three land-bank figures in this study's history —
33, 37 and 46 — come from that same marketing boilerplate.

**AND THE CORRECTION IS AS AT THE STUDY'S OWN INFORMATION-SET END**, so the asset base now
satisfies [R-ASSET-01]'s ordering test outright and the relief clause written this morning is
deleted rather than re-worded.

**THIS SESSION MADE THE SAME MISTAKE IT DIAGNOSED, HOURS LATER.** The morning correction was
reached by searching the PDFs sitting in `filings/`. The right document was one the study
already cited, referenced by URL through the walk-forward's investor-relations register and
never stored as a file — so a filesystem search could not see it and a search of the study's
own sources would have found it immediately. **Searching the directory is not searching the
record.**

## 2 · THE DOCUMENT THAT WOULD MOVE DRIVERS, AND COULD NOT BE REACHED

Both returns report a **1H2026 results release lodged with the EGX on 18 August 2026**, and
between them report revenue EGP 19.52bn (+25.3%), net profit EGP 2.29bn (−11.2%), new sales
EGP 96.1bn against EGP 143bn, gross margin 35.5% against 42.8%, construction spend EGP 8.9bn,
2,128 units released from construction and 925 handed over.

**NONE OF IT MAY ENTER, AND THE REASON IS NOT SCEPTICISM ABOUT THE FIGURES.** Every one is
press reporting of a release neither return retrieved. SIGCM clause 1 forbids press as a
source for a number, and the two returns already disagree with each other on the profit basis
(2.29bn versus 2.26bn) and on backlog (284bn versus 263bn) — which is exactly what a primary
document would settle and commentary cannot.

**THE LADDER WAS CLIMBED AND IS RECORDED WITH ITS OUTCOMES**, because a route dismissed
untried is a claim about the operator:

| route | outcome |
|---|---|
| Company IR result centre, English | **REACHED**, 88 documents enumerated; newest is the 1Q2026 release. **No 1H2026 release and no 2Q2026 statements are posted.** |
| Company IR result centre, Arabic | **REACHED**; carries fewer 2026 items than the English page |
| Company IR "EGX Disclosures" page | **REACHED**; carries no documents itself — it embeds an EGX-operated feed |
| That embedded feed (`ir.egidegypt.com`) | **REACHED but JavaScript-rendered**; curl returns the shell only |
| Headless Chromium against the feed | **FIRST ATTEMPT FAILED** on the proxy CA. Not worked around by disabling verification — the CA was installed into the browser's own trust store, and the page then loaded. It renders no disclosure list. |
| The feed's data API | **UNREACHABLE.** Its config puts the API on **port 8080**, and this environment's network policy resets that port. Probed twice, from the shell and from the browser. |

**SO THE 1H2026 RELEASE IS RECORDED AS A DATED NEGATIVE SEARCH WITH A NAMED MECHANISM**, not
as an absence. It exists; this container cannot reach it. **It is the highest-value document
request outstanding on this name**, and it would close the study's own gap 2 outright.

## 3 · WHAT ELSE THE RETURNS RAISED, AND WHY EACH STAYS OUT

- **EGP 8.0bn syndicated facility (Banque Misr / NBE), reported 19–20 August 2026.** Real if
  sourced, and **no coupon, margin, tenor or covenant is disclosed in any retrieved material**,
  so it cannot close the securitisation-coupon gap either. Registered as a lead.
- **Hacienda Ras El Hekma launch, 26 July 2026, and EGP 75bn of sales in two weeks.** A launch
  and a company sales claim, both press-carried. **A post-period event that must not be folded
  into any half-year figure** whatever else happens to it.
- **A CBE audit of developer credit exposures, September 2026** (Gemini only; Perplexity did
  not report it). One return, no primary document, and a macro-regulatory claim of exactly the
  kind that would change a discount rate. **It stays out and is named**, because a rate moved
  on a single unsourced return is the reverse-engineering this house prohibits.
- **Land transactions of October 2025 and January 2026** (Gemini). These are the moves that
  plausibly explain 37 → 46, and the 1Q2026 release already carries the resulting total, so
  the total is sourced and its decomposition is not. The decomposition is not needed.
- **Kuwait bid shortlist, 3 September 2026.** Bid stage; no award, no land, no quantity.
- **FY2025 results release.** Both returns searched and neither found one. **That agrees with
  the study's own recorded gap** and is now a twice-confirmed dated negative search.

## 4 · DOES ANY OF IT MOVE A DRIVER?

**One input moved: the land bank, 33.0 → 46.0.** It is the operating asset base of a
developer and **nothing in this model reads it** [R-ASSET-02] — it is printed to the workbook
and reaches no arithmetic — so **no valuation figure moves.** bear 4.01 / base 17.85 /
full 46.50 stand.

**That is the uncomfortable finding rather than a comfortable one.** A 28% error in a
developer's land bank changed the answer by exactly zero, twice, which is why neither the
original defect nor this morning's half-correction could ever have surfaced as a wrong number.

## 5 · THE LESSON THIS PASS EARNED, PROPOSED FOR THE REGISTER

**A developer's operating asset base is disclosed in the "About the company" boilerplate of
its earnings release, not in the results tables.** A study that reads a release for its
numbers misses it by construction — which is how the same figure went stale across three
releases while eight other inputs from the newest of them were consumed correctly. Scope to be
ruled on; the evidence is this name's own three-release history.
