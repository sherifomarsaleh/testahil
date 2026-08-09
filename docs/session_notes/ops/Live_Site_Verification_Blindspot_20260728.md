# Verifying a site change actually reached readers — 28-Jul-2026

> **[SUPERSEDED IN PART — 8-Aug-2026]** The reachability findings below are an environment observation made on 28-Jul-2026, not a standing limitation of the system: pushes over git-HTTPS do work, and the current publish rule requires the session itself to merge to `main` and confirm deploy-pages went green on the merge SHA — so "no route to github.com, api.github.com, the Actions run list or testahil.com" must be re-tested in the session at hand rather than quoted from here. The diagnostic order in the second half is unaffected and still the right sequence. The rest of this document stands as the dated record of what was done at the time.

Written after six rounds of "still not working" on the trade.html/portfolio.html name picker,
where the change had in fact been live for hours and the real defect was elsewhere. The point of
this doc is the diagnostic order, not the specific bug.

## What is and isn't reachable from the sandbox

Tested directly, not assumed:

- `raw.githubusercontent.com` — **works** (HTTP 200, exact bytes). This is the reliable way to
  confirm what is on `main`.
- `git ls-remote` / `git fetch` — **work**. Authoritative for branch tips.
- `testahil.com` — **blocked** at the network layer. `curl` returns tunnel-connect failure;
  Playwright returns `net::ERR_TUNNEL_CONNECTION_FAILED`. Two different tools, same wall, so it's
  policy and not a tool quirk. [RETIRED 8-Aug-2026 — see header: environment observation of that date, re-test before repeating it]
- `github.com` web UI and `api.github.com` — **blocked** by the sandbox with a JSON 403 pointing
  at `add_repo`; that tool was not available in this session. So the Actions run list, PR pages,
  and deployment status are all unreadable from here. [RETIRED 8-Aug-2026 — see header: environment observation of that date; the publish rule now expects the session to merge and to confirm deploy-pages green on the merge SHA]
- `WebFetch` on `testahil.com` — **reaches the site but is useless for markup questions**: it
  converts HTML to markdown before the model sees it, so `id`, `class`, and tag type are gone. It
  reported all four of `t-sym-mount`, `class="t-combo`, `t-combo-input` AND `<select id="t-sym"`
  as absent — the old and new markup are indistinguishable through it. `WebFetch` on `sitemap.xml`
  returned "[binary data]", so XML is no better.
- `WebFetch` on the GitHub Actions run list — **returns confident, wrong answers** (commits that
  do not exist on `main`). It's a JS app a plain fetch can't render. Discard rather than cite.

Net: there is currently **no automated route from this sandbox to the bytes testahil.com serves a
reader.** Say that plainly rather than implying the live site was checked. [RETIRED 8-Aug-2026 — see header: true of that session only, not a standing property]

## The diagnostic order that actually worked

The failure mode across those six rounds was treating "user sees no change" as evidence of a
failed deploy, and re-pushing. What settled it in one step:

1. Confirm the commit is on `main` (`git fetch` + `raw.githubusercontent.com` byte-diff against
   the local file). This is cheap and authoritative.
2. **Render the old and new versions side by side locally and compare them as images.** This is
   the step that was missing. The new combobox turned out to differ from the native `<select>` it
   replaced by exactly one glyph — the caret (`▾` vs `⌄`) — because it inherited the same `.num`
   monospace and the same box. The user's screenshots were of the *working* control. No amount of
   re-pushing was ever going to change what they saw.
3. Only then look for a functional defect, and test the full journey — click, type, arrow keys,
   Enter, blur, Escape — not just "does it filter."

Corollary worth keeping: when a UI change is invisible by construction, ship a change that is
visible by construction (a label change, a hint line). It doubles as the deploy check the sandbox
can't otherwise perform — if the reader can see the new words, the deploy landed.

## The defect that was actually there

`portfolio.html#p-amt` and `trade.html#t-port` were both `type="number" value="100000" min="1"
step="1000"`. HTML validates `step` from `min`, so the valid set was 1, 1001, … 99001, 100001 —
**the shipped default of 100000 was itself invalid**, and Chrome rendered "the two nearest valid
values are 99001 and 100001" over the form on load. Every round amount a reader would type
(250000, 75000) was rejected the same way. Fixed to `min="1" step="any"` in `fde3d1e`.

Swept the other five number inputs on the site (`c-amt`, `p-target`, `m-target`, `t-risk`, the
per-name weight box) — all valid against their own defaults, no change needed. Worth re-running
that sweep whenever a `step` is added to a numeric field.
