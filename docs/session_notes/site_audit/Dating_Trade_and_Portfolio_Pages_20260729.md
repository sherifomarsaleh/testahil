# Dating the trade and portfolio pages — 29-Jul-2026

**Problem (owner, 29-Jul-2026):** the trade page asserts upside/risk with no date attached.
"There is upside" is a claim about nothing. The published object is: *from this close, on
this date, the simulation puts the price here by this date.* Two of those three were on the
page; the dates were not. The portfolio page is worse, because a mix is assembled from
forecasts struck on **different days**.

Status: **LIVE on testahil.com**, 29-Jul-2026, commit `b189828`. `trade.html` +
`portfolio.html` only, +274/−10. No engine, no `data.js`, no numbers touched.

## The data was already there — this is presentation only

Every one of the 71 names with a full distribution already carries `spotDate`,
`dist.t20.resolve` and `dist.t60.resolve`. Swept all 71: **zero missing, and every
resolve date is correctly ordered after its anchor.** Nothing was inferred, recomputed or
back-filled; no forecast was re-anchored. The pages were simply not printing what the data
already said.

Before this change, `trade.html` printed exactly two dates: `spotDate` in one line *below*
the odds table, and t60's resolve as a raw ISO string labelled "Checked on". The 1-month
column had **no date anywhere on the page**. `portfolio.html` printed **none at all**.

## trade.html

- **Dateline** under the odds headline: "Struck from the last close, EGP 15.01 on 22 Jul
  2026. The first column is where the simulation puts the price on 23 Aug 2026, the second
  on 22 Oct 2026." Adds an age warning past 21 days.
- **Dated column headers** on both the odds table and the touch ladder — horizon name on
  line 1, `by <date>` on line 2.
- **Both** horizons now show a check date, in site format. The old single "Checked on" cell
  showed t60's only, in raw ISO.
- **Matured windows are marked, not hidden** (owner decision): amber `closed <date>` in the
  header plus a notice — *"1 month: that window closed on 28 Jul 2026. What follows is the
  forecast as it was published at the time, left standing rather than quietly refreshed…"*
  linking the ledger. Consistent with append-only / never-retro-edit.

## portfolio.html — the genuinely harder case

A mix is not one forecast. Today's coverage spans anchors from **30 Jun to 28 Jul** — a
28-day spread — and the arithmetic combines those distributions as if they were
contemporaneous, because published data supports nothing else. Chosen approach (owner
decision): **show the spread, never re-align it.**

- **Per-name dateline on every row**: `from 22 Jul 2026 close → to 22 Oct 2026`. Amber when
  the anchor is >21 days old or the window has already closed. Applied to the optimiser's
  mix cards too — an optimised mix is built from the same differently-dated forecasts and
  has no better claim to a shared window.
- **Combined window line** under the headline chance: "Each name runs its own 3 months from
  its own last close: struck 30 Jun–28 Jul 2026, ending 22 Sept–28 Oct 2026."
- **Amber notes**, only when they mean something: a name past its end date (named, with the
  ledger link), or an anchor spread >10 days — *"…lines their distributions up as if they
  shared one start date, because that is what published data allows; a name anchored weeks
  ago has already used part of its window."*
- Caveats paragraph rewritten to state the as-if-aligned assumption explicitly.
- Build marker bumped `return-first-v14` → `return-first-v15-dated`.

## What was deliberately NOT done

- **No re-simulation, no re-anchoring, no exclusion of stale names.** Aligning every name to
  a common as-of date would be a *new forecast per name* — engine work, and a retro-edit of
  published output. Blocking stale names from the mix was offered and declined; they are
  labelled instead.
- No change to `data.js`, any distribution, any touch ladder, or the correlation assumption.
- Object keys `dist.t20` / `dist.t60` untouched (the standing "internal identifiers, own
  verified pass" carve-out).

## Verification (render, not grep)

Playwright/Chromium, per the standing site rule. `node --check` on all 9 inline script
blocks; **all 71 names swept on the live-rendered trade page** — every one produces a
dateline with a year and two dated column headers, zero page errors. Portfolio exercised
with the starting mix, a deliberately stale mixed-currency mix (TMPV 30 Jun + KAKAO 28 Jul +
PHDC 22 Jul), both horizons, the optimiser card, dark mode, and a 390px viewport. No page
errors anywhere.

**The full verification suite was re-run after rebasing** onto the 29-Jul `data.js` refresh
(1,082 changed lines: 2POINTZERO roll-forward + computed technicals fanned out to 74 names).
Verifying once before a rebase would not have been verification.

`scripts/check_page_integrity.py` run locally before the push (the repo's own
`page-integrity.yml` gate): **clean — no hard findings** across 74 ticker pages / 92 HTML
files, including the `cache-buster-drift` check. Only the three long-standing advisory
`duplicate-rows` pairs, unrelated to this change.

**One real bug caught in verification:** the first draft round-tripped `Date` objects through
`toISOString().slice(0,10)` to re-format range endpoints. A local-midnight `Date` serialises
to the *previous* calendar day in UTC — so every reader in Cairo (UTC+3) would have seen
every portfolio range endpoint one day early. Dates are now formatted directly and ISO
strings are parsed from parts, never handed to `new Date(str)`.

## Push record

Pushed to `main` as `b189828`, on top of `0b2282b`. Main moved **twice** during this session
(the unattended pipeline is active) — 5 commits between clone and first push attempt, one
more between rebase and push — so the change was rebased twice and the first push was
correctly rejected rather than forced.

Per GIT/PUBLISH MECHANICS: PAT supplied by the owner at the moment of the push, injected as
an authenticated URL for that single push, never written to `.git/config` or memory;
confirmed `remote.origin.url` is tokenless afterwards and `.git/config` contains no
credential.

**Post-push check:** `raw.githubusercontent.com/.../main/{trade,portfolio}.html` fetched and
compared — **byte-identical** to the locally rendered-and-verified files (sha256
`5738a175…` / `ebc6385e…`).

## Deploy verification — and how the sandbox blindspot was worked around

`curl`/Playwright cannot reach `testahil.com` from this sandbox (only
`raw.githubusercontent.com` is allowlisted) — the gap recorded in
`Live_Site_Verification_Blindspot_20260728.md`. **`WebFetch` does reach it**, which
partially closes that blindspot and is worth reusing.

Two caveats learned the hard way, both of which produced a false "not deployed" reading
before the right test was found:

1. **WebFetch converts to markdown, so `<script>` and `<style>` bodies are stripped.**
   Probing for a JS function name or a CSS class always returns "no" and proves nothing.
   Probe for **static visible prose** instead.
2. **WebFetch caches 15 minutes per URL.** A re-check after a deploy must use a
   cache-busting query string (`?cb=…`) or it re-reads the pre-deploy copy.

The working probe: `portfolio.html` carries two static markers — the `#p-diag` build string
and the rewritten caveats sentence. First fetch (immediately post-push) returned the OLD
values, correctly showing the Pages build had not finished. After the Actions deploy
completed, `?cb=…` returned **`build return-first-v15-dated`** and **"Dates are the other
thing a mix quietly blurs"** — the new page, live.

`trade.html` cannot be probed the same way: its dated output is all JS-rendered at runtime
and its added markup is CSS/script only, so it has no new static prose. It is covered by
deployment atomicity — `deploy-pages.yml` uploads the whole repo as one artifact
(`path: '.'`) and deploys it in a single step, so both files shipped in the same deploy.
Stated as an inference, not an observation.

## Findings worth acting on separately

1. **Two names are live on the site with a window that has already closed** — TMPV and TSLA
   (1-month, resolved 28 Jul 2026). They are now labelled rather than silent, but they are
   due a grading + roll-forward.
2. **Anchor staleness is visible now.** Oldest live anchors: TMPV/TSLA 30 Jun (29 days),
   IQCD/QNB/QGTS 5 Jul, RELIANCE/NVDA/INFY/AAPL 6 Jul. Dating the pages makes the refresh
   cadence a reader-facing fact.
3. `spotDate` is stored as prose with inconsistent zero-padding (`close 5 Jul 2026` vs
   `close 03 Jul 2026`). Normalised at render, but an ISO field alongside would be cleaner.
4. Display convention is `toLocaleDateString('en-GB', {day:'numeric',month:'short',year:'numeric'})`
   — identical to `ledger.html`, so September renders as "Sept" on both. One convention across
   the site by construction.
5. The dating helpers are duplicated in both pages (the standing "data.js only,
   self-contained per page" convention). If a third page needs dates, they belong in
   `assets/app.js`.
6. **`ledger.html`, `compare.html` and the individual ticker pages were not touched** — this
   change was scoped to the two pages you named. If the same date-blindness exists there, it
   is a separate pass.
