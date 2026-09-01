"""Egypt macro panel for the AMOC walk-forward — EXOGENOUS inputs only.

These are the Country/Industry-ring anchors the pre-registration names, and the
series the macro-versus-company error split re-runs each origin on. Fetched live
so the panel carries its own retrieval date rather than inheriting one.

TWO THINGS ARE SPECIFIC TO THIS NAME AND MATTER:

1. AMOC's fiscal year ran JULY to JUNE for the whole scored window, while every
   published macro series is on the calendar year. A July-June year is converted
   as the mean of the two calendar years it spans. That is a DERIVED figure and
   is marked as one; it is not the same object as the published annual rate and
   is never presented as if it were.

2. AMOC is a refiner. Its revenue and its dominant cost are the SAME commodity
   complex bought and sold in the same months, so the honest exogenous price
   anchor is the crude path in EGP, not domestic CPI. Escalating the two sides
   on different indices is what manufactures a margin trend out of nothing
   (L-009), and on a pass-through refiner it would be the whole result.
"""
import json, os, time, subprocess, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
WB = "https://api.worldbank.org/v2/country/%s/indicator/%s?format=json&per_page=200&date=2004:2026"
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=%s"

SERIES = [
    ("cpi_pct",   "EGY", "FP.CPI.TOTL.ZG", "annual consumer price inflation, %"),
    ("egp_usd",   "EGY", "PA.NUS.FCRF",    "official exchange rate, EGP per USD, period average"),
    ("gdp_pc_kd", "EGY", "NY.GDP.PCAP.KD", "GDP per capita, constant 2015 USD"),
    ("population","EGY", "SP.POP.TOTL",    "total population"),
]


def _get(url, timeout=180):
    """Fetched through curl rather than urllib.

    Not a style choice: this session reaches the internet through an agent
    proxy with its own CA bundle, which curl is configured for and urllib is
    not. urllib succeeds against one host and is closed on by another, which
    would have looked like "FRED is unavailable" rather than "the client is
    misconfigured" — an absent answer wearing the costume of a finding.
    """
    r = subprocess.run(["curl", "-sS", "--max-time", str(timeout), url],
                       capture_output=True)
    if r.returncode != 0 or not r.stdout:
        raise RuntimeError("fetch failed %s: %s" % (url, r.stderr.decode()[:200]))
    return r.stdout


def wb(country, ind):
    url = WB % (country, ind)
    d = json.loads(_get(url).decode("utf-8"))
    return url, {row["date"]: row["value"] for row in d[1] if row["value"] is not None}


def brent_monthly():
    """Daily Brent -> monthly means, so a July-June year can be built properly."""
    url = FRED % "DCOILBRENTEU"
    rows = _get(url).decode("utf-8").splitlines()[1:]
    by_month = {}
    for line in rows:
        parts = line.split(",")
        if len(parts) != 2:
            continue
        d, v = parts
        try:
            val = float(v)
        except ValueError:
            continue                      # FRED prints "." for a holiday
        by_month.setdefault(d[:7], []).append(val)
    return url, {k: statistics.fmean(v) for k, v in sorted(by_month.items())}


def fy_from_months(monthly, fy_end_year):
    """AMOC's fiscal year: July of (y-1) through June of y."""
    keys = ["%d-%02d" % (fy_end_year - 1, m) for m in range(7, 13)] + \
           ["%d-%02d" % (fy_end_year, m) for m in range(1, 7)]
    vals = [monthly[k] for k in keys if k in monthly]
    return statistics.fmean(vals) if len(vals) == 12 else None


def fy_from_calendar(annual, fy_end_year):
    """Mean of the two calendar years a July-June year spans. DERIVED."""
    a, b = annual.get(str(fy_end_year - 1)), annual.get(str(fy_end_year))
    if a is None or b is None:
        return None
    return (a + b) / 2.0


def main():
    out = {"_retrieved": time.strftime("%Y-%m-%d"), "_tier": "C",
           "_note": ("World Bank WDI and FRED. Tier C — credible third parties, used ONLY for "
                     "exogenous country and commodity variables. No AMOC figure comes from here."),
           "_fy_convention": ("AMOC's fiscal year is 1 July to 30 June. Calendar-year series are "
                              "converted as the mean of the two calendar years the fiscal year "
                              "spans; Brent is built from monthly means over the actual twelve "
                              "months. Both are DERIVED and marked."),
           "sources": {}}
    ann = {}
    for key, ctry, ind, desc in SERIES:
        url, vals = wb(ctry, ind)
        ann[key] = vals
        out[key + "_cy"] = vals
        out["sources"][key] = {"url": url, "desc": desc, "basis": "calendar year"}

    url, bm = brent_monthly()
    out["brent_usd_monthly"] = bm
    out["sources"]["brent_usd"] = {"url": url, "desc": "Brent crude, USD/bbl, monthly mean of daily",
                                   "basis": "monthly"}

    fy = {}
    for y in range(2016, 2027):
        rec = {}
        for key in ("cpi_pct", "egp_usd", "gdp_pc_kd", "population"):
            v = fy_from_calendar(ann[key], y)
            if v is not None:
                rec[key] = v
        b = fy_from_months(bm, y)
        if b is not None:
            rec["brent_usd"] = b
        if rec.get("brent_usd") and rec.get("egp_usd"):
            rec["brent_egp"] = rec["brent_usd"] * rec["egp_usd"]
        fy["FY%d" % y] = rec
    out["fiscal_year_derived"] = fy
    json.dump(out, open(os.path.join(HERE, "macro.json"), "w"), indent=1)
    for y in sorted(fy):
        r = fy[y]
        print("%s  cpi %5.1f%%  egp/usd %6.2f  brent $%6.2f  brent EGP %8.0f"
              % (y, r.get("cpi_pct", float("nan")), r.get("egp_usd", float("nan")),
                 r.get("brent_usd", float("nan")), r.get("brent_egp", float("nan"))))


if __name__ == "__main__":
    main()
