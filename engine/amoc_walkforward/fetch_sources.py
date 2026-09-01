"""AMOC walk-forward training — primary-source acquisition.

Alexandria Mineral Oils Company publishes its disclosure archive as flat PDFs
behind several investor-relations pages on its own domain, amoceg.com.

THE DOMAIN IS NOT THE OBVIOUS ONE.  amoc.com.eg does not resolve; the company's
site is amoceg.com.  The first probe of this run went to amoc.com.eg, was
refused at the proxy, and would have been logged as "company site unreachable"
— a false negative that would have pushed the whole Company ring onto
aggregators (L-007).  Every attempt below is logged, successes AND failures,
and the resolved domain is recorded so the next reader does not repeat it.

A document counts as retrieved only if its first five bytes are %PDF- (L-038:
judge a source by the payload it returns, never by its status code).
PDFs are written OUTSIDE the repo; only the register is committed.
"""
import json, os, re, time, html, hashlib, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get("AMOC_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/50e83873-11d1-59bd-8752-622f52dccf21/scratchpad/amoc_src")
BASE = "https://amoceg.com"

# The company's own IR pages.  Listed explicitly rather than crawled: a crawl
# would also pull the news and gallery trees, and what a walk-forward needs is
# exactly the disclosure archive.
IR_PAGES = [
    ("financial_statement", "/en/investor/financial-report/financial-statement"),
    ("annual_report",       "/en/media-center/annual-report"),
    ("bod_activity",        "/en/investor/corporate-governance/disclosures/bod-activity-report"),
    ("disclosure_reports",  "/en/investor/corporate-governance/disclosures/disclosure-reports"),
    ("general_assembly",    "/en/investor/general-assembly/general-assembly-report"),
    ("governance_reports",  "/en/investor/corporate-governance/disclosures/corporate-governance-reports"),
    ("ir_presentation",     "/en/investor/financial-report/ir-presentation"),
    ("esg",                 "/en/investor/sustainability/esg"),
    ("sustainability",      "/en/investor/sustainability/sustainability-report"),
    # The Arabic tree is the same document set under different labels; it is
    # fetched because EGX-era filings are sometimes posted there only.
    ("financial_statement_ar", "/ar/investor/financial-report/financial-statement"),
    ("annual_report_ar",       "/ar/media-center/annual-report"),
]

ATTEMPTS = []


def _get(url, binary=False, timeout=180):
    t0 = time.time()
    rec = {"url": url, "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "testahil-research/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            rec.update(status=r.status, bytes=len(body), secs=round(time.time() - t0, 2),
                       sha256=hashlib.sha256(body).hexdigest())
            # L-038: the payload decides, not the header.
            if binary:
                rec["is_pdf"] = body[:5] == b"%PDF-"
                rec["ok"] = rec["is_pdf"]
                if not rec["is_pdf"]:
                    rec["error"] = "HTTP %s but payload is not a PDF (first bytes %r)" % (
                        r.status, body[:16])
            else:
                rec["ok"] = True
            ATTEMPTS.append(rec)
            return body if rec["ok"] else None
    except Exception as e:
        rec.update(ok=False, error="%s: %s" % (type(e).__name__, e),
                   secs=round(time.time() - t0, 2))
        ATTEMPTS.append(rec)
        return None


def _label_for(block):
    """The company's own caption for a document, as printed beside the link."""
    txt = re.sub(r"<[^>]+>", " ", block[:1200])
    txt = html.unescape(re.sub(r"\s+", " ", txt)).strip()
    # The caption ends where the next card or the newsletter form begins.
    txt = re.split(r"Subscribe To Newsletters|Read More", txt)[0]
    return txt.strip()[:160]


def harvest():
    os.makedirs(SCRATCH, exist_ok=True)
    docs = {}
    for page_name, path in IR_PAGES:
        body = _get(BASE + path)
        if body is None:
            continue
        s = body.decode("utf-8", "replace")
        for block in re.split(r'(?=<a[^>]+\.pdf")', s)[1:]:
            m = re.search(r'href="([^"]+\.pdf)"', block)
            if not m:
                continue
            url = m.group(1)
            if not url.startswith("http"):
                url = BASE + url
            fn = url.rsplit("/", 1)[-1]
            # The same PDF is linked from several pages; keep the first caption
            # but record every page it appeared on.
            d = docs.setdefault(url, {"url": url, "file": fn, "label": _label_for(block),
                                      "pages": []})
            d["pages"].append(page_name)
    return docs


def download(docs):
    for url, d in sorted(docs.items()):
        dest = os.path.join(SCRATCH, d["file"])
        if os.path.exists(dest) and os.path.getsize(dest) > 1000:
            d["local"], d["bytes"] = dest, os.path.getsize(dest)
            d["retrieved"] = True
            continue
        body = _get(url, binary=True)
        if body is None:
            d["retrieved"] = False
            continue
        with open(dest, "wb") as f:
            f.write(body)
        d.update(local=dest, bytes=len(body), retrieved=True,
                 sha256=hashlib.sha256(body).hexdigest())
    return docs


if __name__ == "__main__":
    docs = download(harvest())
    got = sum(1 for d in docs.values() if d.get("retrieved"))
    with open(os.path.join(HERE, "ir_register.json"), "w") as f:
        json.dump({"resolved_domain": BASE,
                   "domain_note": ("amoc.com.eg does NOT resolve and is not the company's "
                                   "site; the IR archive is amoceg.com."),
                   "documents": list(docs.values())}, f, indent=1)
    with open(os.path.join(HERE, "fetch_attempts.json"), "w") as f:
        json.dump(ATTEMPTS, f, indent=1)
    print("documents linked: %d   retrieved: %d   attempts logged: %d"
          % (len(docs), got, len(ATTEMPTS)))
    for d in sorted(docs.values(), key=lambda x: x["file"]):
        print("  %-40s %-9s %s" % (d["file"][:40],
                                   "ok" if d.get("retrieved") else "FAILED",
                                   d["label"][:70]))
