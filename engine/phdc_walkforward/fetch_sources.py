"""PHDC walk-forward training — primary-source acquisition.

Resolves the company's OWN investor-relations document register (Kontent.ai
delivery API behind ir.palmhillsdevelopments.com) and downloads every
consolidated financial statement and earnings release it publishes.

Every attempt is logged — successes AND failures — per the Sweep Register rule.
PDFs are written OUTSIDE the repo (scratch dir); only the register and the
extracted numbers are committed.
"""
import json, os, sys, time, urllib.request, urllib.error, hashlib

PROJECT = "9d7970fc-dc69-001d-cf10-ddbde8cd2225"
DELIVER = "https://deliver.kontent.ai/%s" % PROJECT
HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get("PHDC_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/2283e95e-66db-5f22-bba6-0db833f32495/scratchpad/phdc_src")

ATTEMPTS = []


def _get(url, binary=False, timeout=120):
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
            return body if binary else body.decode("utf-8")
    except Exception as e:                                    # log the failure, don't swallow it
        rec.update(ok=False, error="%s: %s" % (type(e).__name__, e),
                   secs=round(time.time() - t0, 2))
        ATTEMPTS.append(rec)
        return None


def register():
    """The company's own quarterly document register, as IR publishes it."""
    raw = _get(DELIVER + "/items?system.type=financial_result_report_item_model"
                         "&limit=200&depth=2")
    if raw is None:
        raise SystemExit("IR register unreachable — STOP AND INFORM (SIGCM clause 8)")
    d = json.loads(raw)
    mods = d["modular_content"]

    def files(cn):
        m = mods.get(cn)
        if not m:
            return []
        return [{"name": a["name"], "url": a["url"], "size": a.get("size")}
                for a in m["elements"].get("file_url", {}).get("value", [])]

    out = []
    for it in d["items"]:
        e = it["elements"]
        yc = e["year"]["value"][0] if e["year"]["value"] else None
        year = (mods.get(yc, {}).get("system", {}).get("name") or str(yc))
        year = "".join(ch for ch in year if ch.isdigit())
        qc = e["quarter"]["value"][0] if e["quarter"]["value"] else None
        q = (mods.get(qc, {}).get("elements", {})
                 .get("quarter_short_text", {}).get("value") or str(qc))
        out.append({
            "year": int(year) if year else None,
            "quarter": q,
            "item": it["system"]["codename"],
            "last_modified": it["system"]["last_modified"],
            "financial_statement": files(e["financial_statement"]["value"][0])
                if e["financial_statement"]["value"] else [],
            "earning_release": files(e["earning_release"]["value"][0])
                if e["earning_release"]["value"] else [],
        })
    out.sort(key=lambda r: (r["year"] or 0, r["quarter"]))
    return out


def download(reg):
    os.makedirs(SCRATCH, exist_ok=True)
    got, miss = 0, 0
    for r in reg:
        for kind in ("financial_statement", "earning_release"):
            for f in r[kind]:
                tag = "%s_%s_%s" % (r["year"], r["quarter"],
                                    "FS" if kind == "financial_statement" else "ER")
                path = os.path.join(SCRATCH, tag + ".pdf")
                f["local"] = path
                f["kind"] = kind
                if os.path.exists(path) and os.path.getsize(path) > 5000:
                    f["fetched"] = "cached"
                    got += 1
                    continue
                body = _get(f["url"], binary=True)
                if body and body[:4] == b"%PDF":
                    open(path, "wb").write(body)
                    f["fetched"] = "ok"
                    f["sha256"] = hashlib.sha256(body).hexdigest()
                    got += 1
                else:
                    f["fetched"] = "FAILED"
                    miss += 1
    return got, miss


if __name__ == "__main__":
    reg = register()
    got, miss = download(reg)
    json.dump(reg, open(os.path.join(HERE, "ir_register.json"), "w"), indent=1)
    json.dump(ATTEMPTS, open(os.path.join(HERE, "fetch_attempts.json"), "w"), indent=1)
    print("periods: %d  documents downloaded: %d  failed: %d" % (len(reg), got, miss))
    print("attempts logged: %d  (failures: %d)"
          % (len(ATTEMPTS), sum(1 for a in ATTEMPTS if not a["ok"])))
