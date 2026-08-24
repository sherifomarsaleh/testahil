#!/usr/bin/env python3
"""
STEP 1a — WHY did the probe get nothing? Is Yahoo blocking this runner, or is
the request wrong?

The Step 1 probe aborted with 8 consecutive RATE_LIMITED names: 64 requests,
every one HTTP 429, across two hosts' worth of candidate suffixes. That is a
different failure from "Yahoo does not carry these names", and the two must not
be confused — the first is a transport problem with workarounds, the second is
a coverage finding that would kill the whole Yahoo plan.

This separates them, cheaply. It asks for symbols whose existence is NOT in
question (AAPL, GC=F) alongside the covered-name suffixes actually in dispute.

  If AAPL 429s     -> the runner's IP is throttled. Says nothing about coverage.
  If AAPL succeeds -> transport is fine and a 404 on COMI.CA is real evidence.

It also tests the three things that plausibly fix a 429 on this endpoint:
  1. query2 instead of query1 (different edge, sometimes different limits)
  2. a cookie + crumb session, which Yahoo began requiring on some routes
  3. the v7 quote route as a second opinion on v8 chart

READ-ONLY. Writes nothing. Prints a status matrix. Standard library only.
"""
from __future__ import annotations

import http.cookiejar
import json
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# Existence is NOT in question for the first two. They are the control.
TARGETS = [
    ("AAPL",      "CONTROL — bare US symbol, certainly exists"),
    ("GC=F",      "CONTROL — gold future, certainly exists"),
    ("COMI.CA",   "EGX suffix (37 covered names ride on this)"),
    ("ADCB.AD",   "ADX suffix — the one the plan says is unlisted and must be tested"),
    ("EMAAR.DU",  "DFM suffix"),
    ("2222.SR",   "Tadawul suffix"),
]
HOSTS = ["query1.finance.yahoo.com", "query2.finance.yahoo.com"]

ctx = ssl.create_default_context()
jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def get(url: str, timeout: int = 20) -> tuple:
    """-> (status, body_or_error). Never raises."""
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json,text/plain,*/*"})
    try:
        with opener.open(req, timeout=timeout, context=ctx) as r:
            return r.status, r.read(400000)
    except urllib.error.HTTPError as e:
        return e.code, (e.read(400) or b"")
    except Exception as e:                       # timeout, DNS, TLS
        return 0, str(e).encode()[:200]


def n_points(body: bytes) -> str:
    try:
        p = json.loads(body)
        r = (p.get("chart") or {}).get("result")
        if not r:
            return "no result"
        return f"{len(r[0].get('timestamp') or [])} pts"
    except Exception:
        return "unparseable"


def main() -> int:
    print("=" * 78)
    print("A. Cookie + crumb handshake (does Yahoo hand this runner a session at all?)")
    print("=" * 78)
    s, b = get("https://fc.yahoo.com")
    print(f"  fc.yahoo.com            -> HTTP {s}   cookies now held: {len(jar)}")
    crumb = None
    s, b = get("https://query1.finance.yahoo.com/v1/test/getcrumb")
    if s == 200 and b and len(b) < 40:
        crumb = b.decode(errors="replace").strip()
    print(f"  v1/test/getcrumb        -> HTTP {s}   crumb: {crumb!r}")

    print()
    print("=" * 78)
    print("B. v8 chart, both hosts. CONTROL rows decide transport-vs-coverage.")
    print("=" * 78)
    print(f"  {'symbol':<12} {'host':<8} {'status':<8} {'detail':<14} note")
    verdicts = {}
    for sym, note in TARGETS:
        for host in HOSTS:
            url = (f"https://{host}/v8/finance/chart/"
                   f"{urllib.parse.quote(sym)}?range=1mo&interval=1d")
            if crumb:
                url += "&crumb=" + urllib.parse.quote(crumb)
            s, b = get(url)
            detail = n_points(b) if s == 200 else ""
            print(f"  {sym:<12} {host[:6]:<8} {s:<8} {detail:<14} {note if host==HOSTS[0] else ''}")
            verdicts.setdefault(sym, []).append(s)
            time.sleep(1.2)

    print()
    print("=" * 78)
    print("C. Stooq — an unrelated free vendor, as a reachability control on the")
    print("   runner itself. If Yahoo 429s everywhere but stooq answers, the")
    print("   runner's egress is fine and the block is Yahoo-specific.")
    print("=" * 78)
    for s_sym in ["aapl.us", "cib.eg"]:
        s, b = get(f"https://stooq.com/q/d/l/?s={s_sym}&i=d")
        head = b.decode(errors="replace").splitlines()[:2] if s == 200 else []
        print(f"  stooq {s_sym:<10} -> HTTP {s}   {head}")
        time.sleep(1.0)

    print()
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)
    ctrl = verdicts.get("AAPL", []) + verdicts.get("GC=F", [])
    if ctrl and all(c == 429 for c in ctrl):
        print("  Every CONTROL symbol 429'd. Yahoo is throttling this runner's IP.")
        print("  NOTHING can be concluded about whether Yahoo carries the covered")
        print("  names — the question was never actually asked. Step 1 is BLOCKED,")
        print("  not answered, and Step 2 must not read this as a coverage result.")
        return 3
    if ctrl and any(c == 200 for c in ctrl):
        print("  A CONTROL symbol returned 200: transport works from this runner.")
        print("  Non-200s on the covered-name suffixes are therefore real evidence")
        print("  about those symbols, and the full probe is worth re-running.")
        return 0
    print("  Mixed/!200 controls — inconclusive, see the matrix above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
