---
description: Watch covered names' own IR channels for filings and results releases published since each study's sweep cut-off.
argument-hint: "[optional: TICKER, or a market code, to narrow the watch]"
allowed-tools: Bash, Read, Grep, Glob, WebFetch, WebSearch
---

# TESTAHIL disclosure watch — catch the release before an auditor does

MODON's first edition swept the H1-2026 interim but not the 29-Jul-2026 results release,
whose AED 65.4bn backlog and AED 26bn H1 sales superseded its core drivers. An external
audit caught it and the study was restruck the same day. This watch exists so the next one
is caught here instead.

Scope to `$ARGUMENTS` if given; otherwise sweep every name carrying a delivered study.

## The rule being enforced

**A period is not swept until BOTH its financial statements AND its results announcement
are registered.** The release carries operating anchors the statements never do — backlog
and composition, sales and geography, the company's own net-debt definition and value,
adjusted EBITDA, current-perimeter portfolio counts. A newer release's anchors supersede
older ones in the driver set, or the study states why not.

Investor-relations presentations and earnings-call materials are MANDATORY, not optional,
for volumes, prices, utilisation and segment data no financial statement carries. Tag them
`COMPANY_IR` in the Sweep Register, distinctly from the audited-financial-statements tag,
so a reviewer can see how much of the Company ring rests on the primary IR channel.

## Each tick

1. For each in-scope name, find its study's sweep cut-off — the newest period registered in
   its `engine/{name}_study/` sweep register.
2. Go to **the company's OWN website / investor-relations page FIRST**, before any
   aggregator. Log the attempt and its outcome in the register **even when the site is
   unreachable** — a real prior case returned `connect_rejected` at the proxy, and logging
   the failure is the rule working.
3. Ask what has been published since that cut-off: annual or interim statements, results
   announcements, IR decks, call transcripts, material disclosures to the exchange.
4. For anything new, state in one line **which driver it would move and in which direction** —
   a release that changes nothing in the driver set is not a finding.
5. Separately, run the **post-publication check**: for any name whose first quarter after
   publication has now been reported, compare the realised figure against that study's own
   forecast. A miss above the >5%-of-central threshold escalates like any other critique
   finding — it is explicitly NOT something the user should have to surface.

## Boundaries

- **You do not restrike a study on a watch tick.** You report what was found and what it
  would move. Rebuilding is a study task with its own QC gate.
- Never substitute an aggregator for the company's own numbers. Historicals are
  official-sources-only; if required official data is inaccessible, STOP AND INFORM and ask
  for the primary document rather than quietly using a weaker source.
- Aggregator and press sources remain fine for Global/Country/Industry-ring context and
  forecast drivers — never as the source of the subject's own reported historicals.
- Flag dual listings explicitly: the same issuer can file on two exchanges, and only the
  series tells you which regressor is legitimate.

## Output

Nothing new → one line, "no new disclosures", and end the tick. Something new → the name,
the document, its date, the driver it moves, and the direction. Three or four sentences.
