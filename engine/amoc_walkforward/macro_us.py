"""US consumer inflation, for the purchasing-power-parity currency identity.

WHY A SEPARATE FILE RATHER THAN A FIELD IN macro.json. Re-running macro.py would
re-fetch every series and rewrite the file the delivered walk-forward reads. The
World Bank revises annual series for years afterwards, so a re-fetch would move a
delivered run's numbers silently, as a side effect of adding one input. This
fetches the one series that is missing, into its own file, and macro.json is not
touched.

Tier C, exactly as macro.json's own note says: a credible third party used ONLY
for an exogenous country variable. No AMOC figure comes from here.

    python3 macro_us.py
"""
import json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
URL = ("https://api.worldbank.org/v2/country/USA/indicator/FP.CPI.TOTL.ZG"
       "?format=json&per_page=200&date=2004:2026")


def _get(url, timeout=180):
    """curl rather than urllib -- same reason macro.py gives: this session
    reaches the internet through an agent proxy curl is configured for."""
    r = subprocess.run(["curl", "-sS", "--max-time", str(timeout), url],
                       capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("curl failed: %s" % r.stderr.decode()[:400])
    return r.stdout.decode()


def main():
    raw = json.loads(_get(URL))
    ann = {}
    for rec in raw[1]:
        if rec.get("value") is not None:
            ann[rec["date"]] = rec["value"]
    out = {"_retrieved": raw[0].get("lastupdated"),
           "_tier": "C",
           "_note": ("US annual consumer price inflation, World Bank WDI. Held "
                     "separately from macro.json so adding it cannot re-fetch and "
                     "silently move a delivered run's Egyptian series."),
           "_source": {"url": URL, "desc": "annual consumer price inflation, %",
                       "basis": "calendar year"},
           "cpi_us_pct_cy": ann}
    json.dump(out, open(os.path.join(HERE, "macro_us.json"), "w"), indent=1)
    for y in sorted(ann, reverse=True)[:12]:
        print("%s  %5.2f%%" % (y, ann[y]))


if __name__ == "__main__":
    main()
