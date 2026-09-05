# GBCO — what actually blocks this study, measured rather than inherited

**5 September 2026.** Written because the blocker this directory has carried since July was
CLOSED by a rule adopted on 2 September and nothing noticed, and because the programme
state asserted this name could take the [R-LENS-03] lever tonight when it cannot.

## 1. The recorded blocker is closed

`beta_result.json` carries, beside a conforming tier-1 beta:

> `wacc_reissue_blocked_on`: *"Egypt's own sovereign default spread, rating basis and CDS
> basis, read fresh from Damodaran's original ctryprem.html. … Not reconstructed from
> memory: stop and inform."*

That was correct when written. It is no longer true. `engine/macro_paths/EG.json` carries
Egypt's own default spread on both bases — **rating 6.37%, market 3.41%** — sourced and
dated, and `engine/macro_path.py EG` prints them. [R-MACRO-01] supplied the number this
study was waiting for, three days ago, and the waiting note went on standing.

**This is [R-IND-01]'s own failure mode inside a study rather than inside a message: an open
blocker whose resolving condition is already met.** That rule's gate re-checks the escalation
register on every run for exactly this; a blocker recorded in a study's own artefact is
checked by nothing.

## 2. What the study's own figures then say, and why it is a rebuild and not a patch

`compute.py` does not run. Line 171 passes `rf=` to a `WaccInputs` that has taken
`rf_observed` since the v2 method, so the file raises `TypeError` before it reaches a
number. **Renaming the argument would not fix it and would be worse than leaving it
broken**, because `sov_default_spread_rating` and `sov_default_spread_cds` default to zero:
the call would then run, reproduce today's figures exactly, and go on committing the v1
double-count — the raw local yield PLUS a country-risk-loaded equity premium, which is the
systemic bug the v2 method exists to close.

Done properly, with the spreads the house path now supplies:

| | as committed | v2, rating basis | v2, CDS basis |
|---|---:|---:|---:|
| risk-free used | 22.55% (raw local yield) | 16.18% | 19.14% |
| the arithmetic | — | 22.55 − 6.37 | 22.55 − 3.41 |

That lowers the cost of equity by several points, lowers the weighted average cost of
capital, and **raises** the value of a study already sitting well above its price. It is a
valuation change and it belongs in a rebuild with a declared audit point [R-REBUILD-01] and
a gap review [R-GAP-01], not in a passing edit.

## 3. Two further things the same pass has to carry

- **Terminal growth is a typed nominal 11.5%** against a cost of capital of 22.94%.
  [R-MACRO-01] requires growth stored as (real, inflation-path id) and recomputed to its
  nominal, and the house Egyptian terminal is 7.0%. A typed nominal rate is unfalsifiable —
  nobody can tell whether 11.5% meant inflation plus four points or minus three.
- **The blend.** The published central is a four-lens weighted blend at 0.40 / 0.15 / 0.20 /
  0.25, and one of the four is the same lens with the holding-company discount switched off,
  which is a sensitivity rather than a lens.

## 4. And the lens class is genuinely blocked, which the programme state had wrong

The study's own masthead and section 1.1 say what it is: *"we value GB Corp as an operating
company with a captive finance arm and split the legs"*, primary lens *"split-the-legs
sum-of-the-parts (operating company + captive lender)"*. `research_protocol.LENS_REGISTRY`
has no such row, so this name is the **fifth** blocked by the lens-registry escalation
(`lens-registry-has-no-row-for-a-food-and-grocery-group`, default 18 September), not one of
the three that could proceed.

It is also the sharpest case for that escalation's own default fix rather than a
complication of it: the registry already stores **exactly** the lens set this study needs —
a sum-of-the-parts primary with a relative multiple and book beside it — under
`holding company`, and refuses it on the row's NAME alone, because a holding company IS its
stakes and this is an auto assembler with a captive lender and one large associate.
Registered as [L-337].

## 5. What is left readable, and what the answer is against today's price

The gap gate still cannot see this study: its central sits at `lenses.central.base` and its
spot at the top level, and the shared reader looks for `central`. Exposing it needs
`compute.py` to run, which needs section 2. For the record, and computed rather than typed:
the committed central of **EGP 35.7469** against the latest known close of **EGP 28.98
(3 September 2026)** is **+23.4%**, which under [R-GAP-01]'s two-sided trigger owes the
eight-heading review before any delivery, and which [R-GAP-02] does not hold, because that
block is one-sided and below.

## 6. The order the rebuild runs in, declared here so it is not chosen afterwards

1. the cost-of-capital schedule through `engine/cost_of_capital.py` on the house Egyptian
   path ([R-COC-01]) — the correction that unblocks the file at all;
2. growth stored as a real rate on that path ([R-MACRO-01]);
3. the terminal through `engine/terminal_value.py` on a disclosed life ([R-TERM-01]) — and
   the life has to be sourced first, from GB Corp's own audited accounting-policies note,
   which is **not in this directory**: `README.md` records that the historical financials
   were gathered in conversation rather than by code, so this study holds no filings at all
   and SIGCM clause 1 has nothing behind it here either;
4. the lens architecture ([R-LENS-03]) — **blocked**, and the reason is section 4;
5. the re-strike on the latest known price and the eight-heading review ([R-GAP-01]).

Steps 1–3 and 5 are available today. Step 4 is not, and a rebuild that took 1–3 and left
the blend standing is the SAVOLA and EMPOWER precedent of 4 September: legitimate, recorded,
and the name stays on the lens ratchet with its reason.

## 7. The filings were looked for, and the ladder found something worth more than the answer

**Added the same day.** Section 3 records that this study holds no filings at all. Six routes
were run to get them; all six are in `engine/escalations.json` under
`GBCO-audited-statements-not-reachable-from-this-container` with their dates and outcomes.
The short version:

- **GB Corp's own domain.** Eight candidate hostnames. Seven fail to connect. One —
  `gbauto.com` — returns a 5,900-byte **Cloudflare "Just a moment..." challenge**, which is a
  JavaScript bot check rather than a refusal: the host exists and curl cannot pass it.
- **The Egyptian Exchange**, `egx.com.eg`, where a listed company's disclosures are lodged.
  **HTTP 200 with 47KB — and the body is an F5 `/TSPD/` bot-defence interstitial** carrying
  three links, none of them content. Reachable and unusable without JavaScript.
- **The regulator** (`disclosure.efsa.gov.eg`, `mist.gov.eg`) — neither resolves.
- **web.archive.org**, as a delivery route to documents the company itself published —
  unreachable from this container.
- **Every live ref in the repository**, in case another branch held them: 239 searched, and
  the only GBCO PDFs anywhere are this study's own delivered document.

### The control is the part worth keeping

The tool that defeats a JavaScript challenge is a headless browser, and this container has
Chromium installed. It launched — Playwright's own build was mismatched and was pointed at
the installed binary first — and then returned `ERR_CONNECTION_RESET` on `gbauto.com`.

**That looked exactly like "GB Corp blocks automated readers", and it is not.** The same
browser returns the same reset on a **control host that curl fetches with a 200 in the same
minute**, and the proxy's own status endpoint names the reason: twenty recent
`ws_closed_mid_exchange` entries, *tunnel closed after 6s, 39 bytes received*. The browser's
traffic is dropped by the relay regardless of destination.

**Without the control, "the site blocks us" would have gone into this file as a fact.** It is
a different fact with a different remedy, and it is [L-343] again from the other side: a
recorded failure is a fact about one attempt on one day. The same pass found another study's
sweep register carrying `egx.com.eg` as *"connect_rejected at the proxy"* — the outcome is
still failure and **the reason has changed**, which nobody would have noticed.

### What proceeds anyway

Steps 1, 2 and 5 of section 6 need no filing and are the rebuild. **Step 3 needs a DISCLOSED
useful life and stays on the ratchet with this as its reason** — a life this desk chose is
not a disclosed life. The default, if no filings arrive by 19 September, is to rebuild on
those three and have the study state plainly that SIGCM clause 1 is unmet: the historicals
were gathered in conversation and no filing backs them. Not an aggregator, and not a chosen
life.
