"""Fetch ARCC primary documents from the company's OWN investor-relations site.

L-007: the company's own site is tried FIRST, before any aggregator, and EVERY
attempt is logged — including the failures.  A site that will not load is a
fact worth recording.  (The 07-Aug-2026 ARCC study logged
arabiancementcompany.com as connect_rejected at the proxy; it resolves now, so
the failure was transient and the archive behind it is deep.)

The archive is enumerated from the IR page itself rather than guessed, so a
document the company publishes but we did not think to ask for still lands in
the register.
"""
import os, re, json, subprocess, sys, time
from html import unescape

IR = "https://arabiancementcompany.com/investor-relations/financial-information/"
SCRATCH = os.environ.get("ARCC_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/82898002-da86-5df7-8203-457959546ece/scratchpad/arcc_src")
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "fetch_attempts.json")

# What the walk-forward needs.  Standalone (parent-only) filings are recorded
# as SEEN but not fetched: the study values the consolidated group, and mixing
# the two bases inside one panel is a basis break nobody declared.
WANT = re.compile(r"(consolidated[_-]financials|financials[_-]english|earnings[_-]?release|"
                  r"investor[s]?[_-]?presentation)", re.I)
SKIP = re.compile(r"(arabic|standalone|sustainability|company-profile|climate|ogm|minutes)", re.I)


def curl(url, dest, timeout=90):
    t0 = time.time()
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", str(timeout),
                        "-w", "%{http_code}", "-o", dest, url],
                       capture_output=True)
    code = r.stdout.decode().strip()[-3:] if r.stdout else "000"
    size = os.path.getsize(dest) if os.path.exists(dest) else 0
    ok = code == "200" and size > 2000
    if not ok and os.path.exists(dest):
        os.unlink(dest)
    return {"http": code, "bytes": size, "ok": ok,
            "secs": round(time.time() - t0, 2),
            "err": r.stderr.decode()[:200] or None}


def enumerate_archive():
    dest = os.path.join(SCRATCH, "_ir_financial_information.html")
    os.makedirs(SCRATCH, exist_ok=True)
    rec = curl(IR, dest)
    if not rec["ok"]:
        return [], {"url": IR, "role": "archive-index", **rec}
    html = open(dest, encoding="utf-8", errors="replace").read()
    urls = sorted({unescape(u) for u in
                   re.findall(r'href="([^"]+\.pdf)"', html, re.I)})
    return urls, {"url": IR, "role": "archive-index", "found_pdfs": len(urls), **rec}


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    attempts = []
    urls, idx = enumerate_archive()
    attempts.append(idx)
    print("archive index: %s  %d pdfs" % (idx.get("http"), len(urls)), flush=True)

    for u in urls:
        name = u.rsplit("/", 1)[-1]
        if SKIP.search(name) or not WANT.search(name):
            attempts.append({"url": u, "role": "seen-not-fetched",
                             "reason": "arabic/standalone/non-financial"})
            continue
        dest = os.path.join(SCRATCH, name)
        if os.path.exists(dest) and os.path.getsize(dest) > 2000:
            attempts.append({"url": u, "role": "primary", "http": "cached",
                             "bytes": os.path.getsize(dest), "ok": True})
            continue
        rec = curl(u, dest)
        attempts.append({"url": u, "role": "primary", **rec})
        print("  %-3s %8d  %s" % (rec["http"], rec["bytes"], name), flush=True)

    got = sum(1 for a in attempts if a.get("ok") and a.get("role") == "primary")
    seen = sum(1 for a in attempts if a.get("role") == "seen-not-fetched")
    json.dump({"source": IR, "fetched": got, "seen_not_fetched": seen,
               "attempts": attempts}, open(LOG, "w"), indent=1)
    print("\nfetched %d primary documents; %d seen and deliberately not fetched"
          % (got, seen))
    return got


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
