# Automatic daily price feed — plan and current state (24-Aug-2026)

## Goal
Stop hand-posting investing.com CSV exports into `engine/raw_ohlc/{MARKET}/{TICKER}.csv`.
Replace with a scheduled job that appends each day's close automatically.

## Current state of the pipeline (verified against main, 24-Aug-2026)
- `.github/workflows/testahil-calibration.yml` already fires on any push to
  `engine/raw_ohlc/**.csv`. The refit half is done. Nothing schedules it.
- 93 library files: EG 37, AE 28 (19 ADX + 9 DFM), SA 13, IN 3, KR 3, QA 3,
  US 3, XAU 2 (GOLD, SILVER), XPT 1 (PLATINUM). 90 of these have an
  `assets/data.js` entry; the three metals do not carry an exchange code.
- Library format is the investing.com export (`Date, Price, Open, High, Low,
  Vol., Change %`). Row order is NOT consistent across files — some are stored
  newest-first, some oldest-first. Any tool reading "the last N rows" must sort
  by date, not slice the top of the file.

## The three obstacles (unchanged by vendor choice)
1. **Vendor mismatch.** The merge rule requires overlapping dates to agree to
   the 4th decimal. A second vendor will not agree by default, so adoption must
   be decided per name on measured disagreement, not on a symbol resolving.
2. **Coverage.** Yahoo's published exchange list carries EGX `.CA`,
   Tadawul `.SAU`, DFM `.AE`, QSE `.QA`, KRX `.KS`, NSE `.NS`, NASDAQ. It does
   not list ADX (19 names). That list is curated, not a manifest — Yahoo serves
   symbols it does not enumerate — so `.AD` must be TESTED, not assumed absent.
3. **A bot push does not trigger another workflow.** A commit made with the
   default `GITHUB_TOKEN` will not start `testahil-calibration.yml`. The fetch
   job must call `auto_refresh.py` itself or dispatch the workflow with a PAT.

## Seven steps
1. **Probe** — does Yahoo carry the 93 names, and do its prices agree with the
   library? Read-only. Script: `scripts/yahoo_probe.py` (attached alongside this
   document). Run: `python3 scripts/yahoo_probe.py` → writes
   `yahoo_probe_results.csv`. On a GitHub Actions runner, commit the script to a
   branch and drive it from a `workflow_dispatch` job.
2. **Decide** — read the results table; adopt per name, MATCH only.
3. **Top-up script** — appends only strictly-newer rows, never rewrites history.
4. **Shadow week** — writes to a side folder; diff against the next manual
   investing.com export before anything touches the real library.
5. **Schedule** — one cron per market close (six different closing times).
6. **Wire to the rest** — trigger the refit, then `data.js` spot/dist/touch,
   `apply_technicals.py --write`, `ta_chart.py --write`, gated by
   `check_ta_chart_overlay.js`.
7. **Alarms** — no new data for N days, or a move beyond that exchange's own
   daily price limit → stop and notify, never publish.

## Why Step 1 has to run on a runner
The Cowork session that wrote this plan could not reach Yahoo at all (its egress
proxy blocked yfinance, direct calls to query1/query2, WebFetch, stooq and
alphavantage — all five tested) and could not push to the repo (the sandbox git
proxy refuses any repo outside the session's authorized set; a user-supplied PAT
did not change that — tested). A second session reported HTTP 429 from
`query1.finance.yahoo.com`, i.e. reachable but rate-limited. A GitHub Actions
runner has clean egress and is the right place to run the probe.

## Notes for whoever runs Step 1
- The probe is READ-ONLY. It writes exactly one file, `yahoo_probe_results.csv`.
  It must not modify `engine/raw_ohlc/` or `assets/data.js`.
- It reads exchange codes straight out of `assets/data.js`, so it stays correct
  as coverage grows. Three filename/key mismatches are aliased in the script:
  `TWOPOINTZERO`→`2POINTZERO`, `RAJHI`→`ALRAJHI`, `AE/ADIB`→`ADIBUAE`.
- Candidate suffixes tried per exchange: EGX `.CA`; Tadawul `.SR` then `.SAU`;
  ADX `.AD` then `.AE`; DFM `.DU` then `.AE`; QSE `.QA`; KRX `.KS`; NSE `.NS`;
  NASDAQ bare; metals `GC=F`/`SI=F`/`PL=F` with `XAUUSD=X` etc. as fallback.
- Verdicts: MATCH (median abs diff ≤0.10% and max ≤1.0%), CLOSE (median ≤0.50%),
  DRIFT (worse), NO_OVERLAP, NOT_FOUND.
- Yahoo rate-limits. Keep `--sleep` at 0.6s or higher; on HTTP 429 back off.

## Licensing note
`yfinance` and the chart endpoint are unofficial access to Yahoo, and Yahoo's
terms restrict redistribution. Immaterial for a private library; a real question
for a product being licensed to a bank. A paid feed (EODHD ~USD 20/month) is the
alternative, but its public exchange list does not show ADX or Tadawul either —
confirm with the vendor before paying.

---

## Step 1 RESULT — 24-Aug-2026: BLOCKED, not answered

Run on a GitHub Actions runner as this plan proposed. **The coverage question
was never actually asked**, because Yahoo refused every request from the runner.

**The probe** (`.github/workflows/yahoo-probe.yml`, run 32748237167) aborted after
9m45s with 8 consecutive `RATE_LIMITED` names — ADCB, ADIB, ADNOCDIST,
ADNOCDRILL, ADNOCGAS, ADNOCLS, AGTHIA, AIRARABIA. The timing is exact evidence
that nothing got through: 4 attempts × (5+10+20s backoff) × 2 candidate suffixes
× 8 names ≈ 9m45s. All 64 requests were HTTP 429.

**The diagnostic** (`yahoo_reachability.py`, run 32749943207) settles what that
means, using symbols whose existence is not in question as controls:

| request | query1 | query2 |
|---|---|---|
| `AAPL` — CONTROL, certainly exists | **429** | **429** |
| `GC=F` — CONTROL, certainly exists | **429** | **429** |
| `COMI.CA` — EGX | 429 | 429 |
| `ADCB.AD` — ADX (the suffix in dispute) | 429 | 429 |
| `EMAAR.DU` — DFM | 429 | 429 |
| `2222.SR` — Tadawul | 429 | 429 |
| `fc.yahoo.com` (cookie handshake) | 404, 1 cookie set | — |
| `v1/test/getcrumb` | **429** | — |
| `stooq.com` — unrelated vendor, egress control | **200** | — |

**Reading it.** `fc.yahoo.com` completing at all (404, cookie set) proves TCP and
TLS to Yahoo are fine, and stooq answering 200 proves the runner's egress is fine.
So this is application-layer rate limiting keyed on the caller's IP, applied to
GitHub's Azure ranges. Two consequences:

1. **`.AD` is still untested.** Obstacle 2 above — "Yahoo's list does not carry
   ADX, so `.AD` must be TESTED, not assumed absent" — remains exactly as open as
   it was before this run. A 429 is not a 404.
2. **A cookie/crumb session does not fix it.** `getcrumb` is itself 429, so the
   usual workaround is unavailable from this IP.

**What must NOT be concluded:** that Yahoo lacks these names. Had the probe kept
its original 429 handling (catch, sleep 5s, move on) this run would have written a
complete, clean-looking table marking all 93 names `NOT_FOUND`, and Step 2 —
which adopts per name off exactly that column — would have read it as a coverage
finding and killed the Yahoo plan on evidence that was never gathered. The probe
now distinguishes `RATE_LIMITED` from `NOT_FOUND` and aborts rather than write a
partial table.

**Also learned:** stooq is no longer a drop-in fallback. It answers 200 but
returns a JavaScript proof-of-work bot-verification page, not CSV, from this IP.

### Where Step 1 goes next

The runner premise in "Why Step 1 has to run on a runner" above is **disproven
for Yahoo specifically** — clean egress is not the constraint; the IP's
reputation is. Options, best first:

1. **Run the probe from a non-datacenter IP.** It is standard-library-only, so on
   any normal machine: `python3 claude/ops/yahoo_probe.py`. This answers the
   coverage question today, and it is the only option that costs nothing.
2. **Self-hosted runner** on an IP Yahoo does not throttle — keeps it automated,
   but needs somewhere to host it.
3. **A keyed vendor** (EODHD ~USD 20/month) — authenticates per key rather than
   per IP, so datacenter egress is fine. Confirm ADX and Tadawul coverage with
   the vendor BEFORE paying; the licensing note below still applies.

The workflow stays in the repo, re-runnable by manual dispatch, in case the block
lifts or a self-hosted runner is added.
