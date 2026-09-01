"""TMGH walk-forward training — primary-source acquisition.

Talaat Moustafa Group Holding publishes its whole disclosure archive as flat
PDFs behind one investor-relations page on its own domain. This resolves that
page live, classifies every document it links, and downloads the ones a
walk-forward needs: consolidated financial statements, earnings releases,
investor presentations and annual reports.

Every attempt is logged — successes AND failures — per the Sweep Register rule
(L-007: a site that will not load is a fact worth recording). PDFs are written
OUTSIDE the repo; only the register and the extracted numbers are committed.
"""
import json, os, re, sys, time, html, hashlib, urllib.parse, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get("TMGH_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/ba35918b-2c34-5691-9e47-05ae974e86f1/scratchpad/tmgh_src")
IR_PAGE = "https://talaatmoustafa.com/investor-relations/"

ATTEMPTS = []


def _get(url, binary=False, timeout=180):
    t0 = time.time()
    rec = {"url": url, "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "testahil-research/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            rec.update(status=r.status, bytes=len(body), ok=True,
                       secs=round(time.time() - t0, 2),
                       sha256=hashlib.sha256(body).hexdigest())
            ATTEMPTS.append(rec)
            return body if binary else body.decode("utf-8", "replace")
    except Exception as e:                        # log the failure, never swallow it
        rec.update(ok=False, error="%s: %s" % (type(e).__name__, e),
                   secs=round(time.time() - t0, 2))
        ATTEMPTS.append(rec)
        return None


# --- classification ------------------------------------------------------
# Every rule below keys on the company's OWN filename, which is how TMG labels
# the document. Nothing is inferred from content we have not read yet.

def classify(name):
    n = name.lower()
    if "seperate" in n or "separate" in n or "standalone" in n or "\u0627\u0644\u0645\u0633\u062a\u0642\u0644\u0629" in n:
        return "separate_fs"          # holding-company-only; not the consolidated group
    if ("consolidated" in n or "consilidated" in n or "conso " in n or "cons. fs" in n
            or "\u0627\u0644\u0642\u0648\u0627\u0626\u0645 \u0627\u0644\u0645\u0627\u0644\u064a\u0629 \u0627\u0644\u0645\u062c\u0645\u0639" in n):
        return "consolidated_fs"      # Arabic: al-qawa'im al-maliyya al-mujamma'a
    # TMG labels its results release five different ways across nineteen years.
    # Keying on "earning" alone silently dropped the FY2015, FY2016, FY2025 and
    # 1Q2026 releases into the residual bucket, where nothing would have looked
    # for them (L-015: an empty result is not a clean result).
    if ("earning" in n or re.search(r"\ber\b", n)
            or "full year and fourth quarter" in n):
        return "earnings_release"
    if "presentation" in n:
        return "ir_presentation"
    if "annual report" in n and "governance" not in n and "board" not in n:
        return "annual_report"
    if "market update" in n or "sales disclosure" in n:
        return "market_update"
    if "executive management report" in n or "executive managment report" in n:
        return "exec_mgmt_report"
    if "board of directors" in n and "annual report" in n:
        return "bod_annual_report"
    return "other"


PERIOD_RX = [
    # (regex, handler) — resolved from the company's own filename
    (re.compile(r"(\d{1,2})\s*[-/ ]\s*(\d{1,2})\s*[-/ ]\s*(20\d\d)"), None),
]
MONTHS = {"january": 3, "march": 3, "jun": 6, "june": 6, "sep": 9, "september": 9,
          "sepetember": 9, "septembe": 9, "dec": 12, "december": 12, "mar": 3}


def period_of(name):
    """(year, month) of the reporting period, from the company's own filename.

    Returns None where the filename does not state one — the document is still
    downloaded and registered; the period is then read off the document itself.
    """
    n = name.lower().replace("%20", " ")
    m = re.search(r"(1q|2q|3q|4q|fy|1h|9m)\s*-?\s*(20\d\d|\d\d)\b", n)
    if m:
        tag, yr = m.group(1), m.group(2)
        yr = int(yr) if len(yr) == 4 else 2000 + int(yr)
        return (yr, {"1q": 3, "2q": 6, "1h": 6, "3q": 9, "9m": 9, "fy": 12, "4q": 12}[tag])
    m = re.search(r"(first quarter|second quarter|third quarter|fourth quarter|"
                  r"first half|nine months|full year)\D{0,30}(20\d\d)", n)
    if m:
        yr = int(m.group(2))
        return (yr, {"first quarter": 3, "second quarter": 6, "first half": 6,
                     "third quarter": 9, "nine months": 9,
                     "fourth quarter": 12, "full year": 12}[m.group(1)])
    m = re.search(r"(\d{1,2})\s*[-.]\s*(\d{1,2})\s*[-.]\s*(20\d\d)", n)
    if m:                                          # dd-mm-yyyy
        return (int(m.group(3)), int(m.group(2)))
    m = re.search(r"(\d{1,2})?\s*(january|march|mar|jun|june|sep|september|sepetember|"
                  r"dec|december)\.?,?\s*(20\d\d)", n)
    if m:
        return (int(m.group(3)), MONTHS[m.group(2)])
    m = re.search(r"(20\d\d)\s*q([1-4])", n)
    if m:
        return (int(m.group(1)), int(m.group(2)) * 3)
    m = re.search(r"year ended\D{0,20}(20\d\d)", n)
    if m:
        return (int(m.group(1)), 12)
    m = re.search(r"\b(20\d\d)\b", n)
    if m:
        return (int(m.group(1)), None)
    return None


def register():
    """The company's own document register, as its IR page publishes it."""
    raw = _get(IR_PAGE)
    if raw is None:
        raise SystemExit("TMG investor-relations page unreachable — "
                         "STOP AND INFORM (SIGCM clause 8)")
    urls = sorted(set(html.unescape(u) for u in
                      re.findall(r'href="([^"]*\.pdf)"', raw, re.I)))
    out = []
    for u in urls:
        absu = urllib.parse.urljoin(IR_PAGE, u)
        # the page mixes http/https and a capitalised host; normalise the scheme
        # and host but NEVER the path, which is the company's own filename
        p = urllib.parse.urlsplit(absu)
        # re-encode the path: some of TMG's own hrefs carry literal Arabic
        # characters, which urlopen cannot put on the wire as-is
        path = urllib.parse.quote(urllib.parse.unquote(p.path), safe="/%:@!$&'()*+,;=~")
        absu = urllib.parse.urlunsplit(("https", p.netloc.lower(), path, p.query, ""))
        name = urllib.parse.unquote(p.path.rsplit("/", 1)[-1])
        out.append({"name": name, "url": absu, "href_as_published": u,
                    "kind": classify(name), "period": period_of(name)})
    return out


WANTED = {"consolidated_fs", "earnings_release", "ir_presentation",
          "annual_report", "market_update", "bod_annual_report", "exec_mgmt_report"}


def _repairs(url):
    """Repaired forms of a malformed href, in the order they are tried."""
    out = []
    if "//ir.talaatmoustafa.com/" in url:
        out.append(url.replace("//ir.talaatmoustafa.com/", "//talaatmoustafa.com/"))
    if "/upload/upload/" in url:
        out.append(url.replace("/upload/upload/", "/upload/"))
    if "/upload/" in url:
        out.append(url.replace("/upload/", "/Upload/"))
    if "/Upload/" in url:
        out.append(url.replace("/Upload/", "/upload/"))
    return out


def download(reg, kinds=WANTED):
    os.makedirs(SCRATCH, exist_ok=True)
    got = []
    for r in reg:
        if r["kind"] not in kinds:
            continue
        safe = re.sub(r"[^A-Za-z0-9._-]+", "_", r["name"])[:150]
        dest = os.path.join(SCRATCH, safe)
        if os.path.exists(dest) and os.path.getsize(dest) > 5000:
            r["local"] = dest
            r["bytes"] = os.path.getsize(dest)
            r["sha256"] = hashlib.sha256(open(dest, "rb").read()).hexdigest()
            r["fetched"] = "cached"
            got.append(r)
            continue
        body = _get(r["url"], binary=True)
        if body is None or len(body) < 5000 or not body[:5].startswith(b"%PDF"):
            # An empty result is not a clean result (L-015): two of TMG's own
            # hrefs are malformed rather than dead — one points at a retired
            # ir. subdomain, one doubles the /upload/ segment. Try the repaired
            # form before recording the document as unobtainable. Every probe,
            # including these, stays in the attempts log.
            for alt in _repairs(r["url"]):
                body = _get(alt, binary=True)
                if body is not None and len(body) >= 5000 and body[:5].startswith(b"%PDF"):
                    r["url_as_published"] = r["url"]
                    r["url"] = alt
                    r["url_repaired"] = True
                    break
                body = None
        if body is None:
            r["fetched"] = "FAILED"
            continue
        with open(dest, "wb") as f:
            f.write(body)
        r.update(local=dest, bytes=len(body), fetched="ok",
                 sha256=hashlib.sha256(body).hexdigest())
        got.append(r)
    return got


def main():
    reg = register()
    got = download(reg)
    with open(os.path.join(HERE, "ir_register.json"), "w") as f:
        json.dump(reg, f, indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, "fetch_attempts.json"), "w") as f:
        json.dump(ATTEMPTS, f, indent=1, ensure_ascii=False)
    by = {}
    for r in reg:
        by[r["kind"]] = by.get(r["kind"], 0) + 1
    print("register: %d documents linked by the company's own IR page" % len(reg))
    for k in sorted(by):
        print("   %-20s %3d" % (k, by[k]))
    fails = [a for a in ATTEMPTS if not a["ok"]]
    print("downloaded %d of %d wanted; %d failed attempts logged"
          % (len(got), sum(1 for r in reg if r["kind"] in WANTED), len(fails)))
    for a in fails[:20]:
        print("   FAIL %s  %s" % (a["url"][-70:], a["error"][:60]))


if __name__ == "__main__":
    main()
