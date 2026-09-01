#!/usr/bin/env python3
"""EMFD fundamental walk-forward — primary-source acquisition.  [R-FCAL-01] §1

Emaar Misr for Development S.A.E. (EGX:EMFD) publishes its investor-relations
document register at https://www.emaarmisr.com/about-emaar/ir-reports/ (and an
Arabic mirror).  This script resolves that register, downloads every financial
statement, earnings release and management annual report it carries, and logs
EVERY attempt -- successes AND failures -- per the Sweep Register rule.

It also probes, and logs, the routes that would have supplied the years the
company's own register no longer carries.  Those probes are part of the record:
a source that could not be reached is a fact worth committing, and the reason
this run stopped is only legible if the failures are visible beside the
successes.  [R-ENF-04] -- an empty result is not a clean result.

PDFs are written OUTSIDE the repo (scratch dir); only the register, the hashes
and the extracted numbers are committed.
"""
import hashlib, json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get(
    "EMFD_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/5c3bac54-80e7-5e98-82bb-8cfd0b2244dd"
    "/scratchpad/emfd_src/pdfs")

IR_EN = "https://www.emaarmisr.com/about-emaar/ir-reports/"
IR_AR = "https://www.emaarmisr.com/ar/about-emaar/ir-reports/"
# The company's CDN (NitroPack in front of WordPress) answers the full
# Chrome user-agent string with HTTP 403 and the abbreviated one with HTTP 200,
# from the same client, same second. Recorded here because it is exactly the
# kind of transport artefact that reads as "the document is not published"
# when it means nothing of the sort. [R-ENF-04]
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"

ATTEMPTS = []


# The fetch goes through curl rather than urllib on purpose: the company's CDN
# answers urllib with HTTP 403 while serving the identical request from curl,
# and the point of this script is to record what the source actually does, not
# to have the transport decide the answer for us.
CURL = ["curl", "-sS", "-L", "-A", UA]


def _get(url, binary=False, timeout=120, tries=4):
    """One logged attempt per try. A transient 403/429 from a CDN is not the
    same fact as a host that refuses the document, so the retries are recorded
    individually and the caller sees the last outcome. [R-ENF-04] -- when a
    probe comes back empty the first hypothesis is that the probe did not run."""
    for attempt in range(tries):
        t0 = time.time()
        rec = {"url": url, "attempt": attempt + 1,
               "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        try:
            p = subprocess.run(
                CURL + ["--max-time", str(timeout),
                        "-w", "\n%{http_code}\t%{content_type}", url],
                capture_output=True, timeout=timeout + 30)
            raw = p.stdout
            cut = raw.rfind(b"\n")
            body, tail = raw[:cut], raw[cut + 1:].decode("utf-8", "ignore")
            status, _, ctype = tail.partition("\t")
            ok = p.returncode == 0 and status.startswith("2")
            rec.update(status=int(status) if status.isdigit() else None,
                       bytes=len(body), ok=ok, content_type=ctype,
                       secs=round(time.time() - t0, 2),
                       sha256=hashlib.sha256(body).hexdigest())
            if not ok:
                rec["error"] = (p.stderr.decode("utf-8", "ignore")[:200]
                                or "HTTP %s" % status)
            ATTEMPTS.append(rec)
            if ok:
                return body if binary else body.decode("utf-8", "ignore")
        except Exception as e:              # log the failure, don't swallow it
            rec.update(ok=False, error="%s: %s" % (type(e).__name__, e),
                       secs=round(time.time() - t0, 2))
            ATTEMPTS.append(rec)
        if attempt < tries - 1:
            time.sleep(2 ** attempt)
    return None


# ---------------------------------------------------------------- register ---
DOC_RE = re.compile(r'href="(https://www\.emaarmisr\.com/wp-content/uploads/'
                    r'[^"]+\.pdf)"')

# The company files each document under a name that carries its own period.
PERIOD = re.compile(r"Financial-Statements-(\d{4})-(Q[1-4]|Year-End)")
# The two oldest statements on the register carry no period token at all --
# "Financial-Statements-2013-AR.pdf" is the full-year Arabic filing. Matching
# only the period-tagged names silently drops the two earliest fiscal years,
# which is a two-year shortening of the window nobody would have seen.
ANNUAL_NOPERIOD = re.compile(r"Financial-Statements-(\d{4})-(AR|EN)\.pdf$")
RELEASE = re.compile(r"Earning-Releases-(\d{4})-(Q[1-4]|Year-End)")
ANNUAL = re.compile(r"Annual-Report-.{0,3}-?(\d{4})")


def classify(name):
    m = PERIOD.search(name)
    if m:
        return {"kind": "FS", "year": int(m.group(1)), "period": m.group(2),
                "basis": ("consolidated" if "Consolidated" in name else
                          "separate" if "Seperate" in name or "Separate" in name
                          else "unspecified"),
                "lang": "AR" if name.endswith("-AR.pdf") else "EN"}
    m = ANNUAL_NOPERIOD.search(name)
    if m:
        return {"kind": "FS", "year": int(m.group(1)), "period": "Year-End",
                "basis": "unspecified", "lang": m.group(2)}
    m = RELEASE.search(name)
    if m:
        return {"kind": "ER", "year": int(m.group(1)), "period": m.group(2),
                "basis": None,
                "lang": "AR" if name.endswith("-AR.pdf") else "EN"}
    m = ANNUAL.search(name)
    if m:
        return {"kind": "AR", "year": int(m.group(1)), "period": "Year-End",
                "basis": None, "lang": "EN"}
    return None


def register():
    """The company's OWN document register, as its IR site publishes it."""
    docs = {}
    for url in (IR_EN, IR_AR):
        html = _get(url)
        if html is None:
            continue
        for href in sorted(set(DOC_RE.findall(html))):
            name = href.rsplit("/", 1)[-1]
            cls = classify(name)
            if cls is None:
                continue
            docs.setdefault(href, dict(cls, name=name, url=href,
                                       register=url))
    if not docs:
        raise SystemExit("IR register unreachable or empty — STOP AND INFORM "
                         "(SIGCM clause 8). An empty register is not an empty "
                         "company. [R-ENF-04]")
    return sorted(docs.values(), key=lambda d: (d["year"], d["period"],
                                                d["kind"], d["name"]))


# ------------------------------------------------------------------ probes ---
# Routes that WOULD carry the fiscal years the company's own register stops
# short of. Each is attempted and its outcome recorded, so the reason this run
# could not proceed is evidence in the repository rather than a recollection.
GAP_PROBES = [
    ("EGX disclosure portal (English)",
     "https://www.egx.com.eg/en/DisclosureNews.aspx"),
    ("EGX-hosted audited FS PDF, FY2024 consolidated",
     "https://www.egx.com.eg/downloads/Bulletins/318451_1.pdf"),
    ("EGX-hosted separate FS PDF",
     "https://www.egx.com.eg/downloads/News/171509_090244.pdf"),
    ("EGID IR data API (company's own embedded IR widget backend)",
     "https://ir.egidegypt.com:8080/api/identity/Settings/getCompanySettings/"
     "grtCLq1LRjYQd1LLygQrAPAirGoZfVsT5uX7h5ISUnM!"),
    ("EGID attachment host",
     "https://data.egidegypt.com/"),
    ("Company IR sub-domain",
     "https://ir.emaarmisr.com/"),
    ("Internet Archive CDX over the company's own domain",
     "https://web.archive.org/cdx/search/cdx?url=emaarmisr.com&"
     "matchType=domain&fl=original&collapse=urlkey&limit=200"),
    ("Company filename pattern extended past the register (FY2022 year-end)",
     "https://www.emaarmisr.com/wp-content/uploads/2025/10/Emaar-Misr-IR-"
     "Reports-Financial-Statements-2022-Year-End-EN-Consolidated.pdf"),
    ("Company filename pattern extended past the register (FY2024 Q4)",
     "https://www.emaarmisr.com/wp-content/uploads/2025/10/Emaar-Misr-IR-"
     "Reports-Financial-Statements-2024-Q4-EN-Consolidated.pdf"),
]


def probe_gap():
    out = []
    for label, url in GAP_PROBES:
        body = _get(url, binary=True, timeout=60)
        rec = ATTEMPTS[-1]
        # A 200 that returns HTML where a PDF was asked for is NOT a success:
        # egx.com.eg answers every request with an F5 interstitial that carries
        # HTTP 200. Judge the payload, never the status code.
        served_pdf = bool(body) and body[:5] == b"%PDF-"
        out.append({"label": label, "url": url, "ok": rec.get("ok", False),
                    "status": rec.get("status"), "bytes": rec.get("bytes"),
                    "content_type": rec.get("content_type"),
                    "served_pdf": served_pdf,
                    "error": rec.get("error"),
                    "verdict": ("usable PDF" if served_pdf else
                                "reachable but not the document" if rec.get("ok")
                                else "unreachable")})
    return out


# -------------------------------------------------------------- downloader ---
def download(docs):
    os.makedirs(SCRATCH, exist_ok=True)
    for d in docs:
        path = os.path.join(SCRATCH, d["name"])
        if os.path.exists(path) and os.path.getsize(path) > 0:
            body = open(path, "rb").read()
            d.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                     local=path, cached=True, is_pdf=body[:5] == b"%PDF-")
            continue
        body = _get(d["url"], binary=True)
        if body is None:
            d.update(local=None, cached=False, is_pdf=False)
            continue
        with open(path, "wb") as f:
            f.write(body)
        d.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                 local=path, cached=False, is_pdf=body[:5] == b"%PDF-")
    return docs


def main():
    docs = register()
    docs = download(docs)
    gap = probe_gap()

    got = [d for d in docs if d.get("is_pdf")]
    fs_years = sorted({d["year"] for d in got if d["kind"] == "FS"})
    complete = sorted({d["year"] for d in got if d["kind"] == "FS"
                       and d["period"] in ("Q4", "Year-End")})

    out = {
        "ticker": "EMFD", "exchange": "EGX", "market": "EG",
        "run_date": time.strftime("%Y-%m-%d"),
        "registers": [IR_EN, IR_AR],
        "documents": docs,
        "downloaded": len(got),
        "fs_years_touched": fs_years,
        "fs_years_with_a_year_end_statement": complete,
        "gap_probes": gap,
    }
    with open(os.path.join(HERE, "ir_register.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    with open(os.path.join(HERE, "fetch_attempts.json"), "w") as f:
        json.dump(ATTEMPTS, f, indent=1)

    print("documents in the company's own register : %d" % len(docs))
    print("downloaded as real PDFs                 : %d" % len(got))
    print("fiscal years touched by a statement     : %s" % fs_years)
    print("fiscal years with a year-end statement  : %s" % complete)
    print("\ngap probes (the years the register stops short of):")
    for g in gap:
        print("  %-58s %s" % (g["label"][:58], g["verdict"]))


if __name__ == "__main__":
    main()
