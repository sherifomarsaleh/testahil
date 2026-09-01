"""Egypt macro panel for the ARCC walk-forward — EXOGENOUS inputs only.

The Country/Industry-ring anchors named in the pre-registration, and the series
the macro-versus-company error split re-runs each origin on.  Fetched live so
the panel carries its own retrieval date rather than inheriting one.

TWO THINGS ARE SPECIFIC TO THIS NAME:

1. ARCC's fiscal year IS the calendar year (every filing is "for the year ended
   31 December"), so no fiscal-to-calendar conversion is performed and none is
   needed.  Stated because the AMOC run immediately before this one DID need
   one, and carrying that construction across without checking would have been
   an invented adjustment.

2. ARCC burns imported COAL and sells cement, and those are two different price
   worlds.  [L-110], the class lesson this name itself produced: a globally
   traded input follows the world price and the exchange rate, and escalating it
   with the domestic cost of living invents a margin story.  So the fuel
   escalator is the SOUTH AFRICAN coal price in EGP — South African rather than
   Australian because that is the grade the Egyptian conversion actually imports
   — and the Australian series is carried beside it as a cross-check, never
   blended into it.
"""
import json, os, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "macro.json")
SCRATCH = os.environ.get("ARCC_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/82898002-da86-5df7-8203-457959546ece/scratchpad/arcc_src")

WB = ("https://api.worldbank.org/v2/country/%s/indicator/%s"
      "?format=json&per_page=300&date=2004:2026")
PINK = ("https://thedocs.worldbank.org/en/doc/"
        "74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/"
        "CMO-Historical-Data-Monthly.xlsx")

SERIES = [
    ("cpi_pct",    "EGY", "FP.CPI.TOTL.ZG", "annual consumer price inflation, %"),
    ("cpi_index",  "EGY", "FP.CPI.TOTL",    "consumer price index, 2010 = 100"),
    ("egp_usd",    "EGY", "PA.NUS.FCRF",    "official exchange rate, EGP per USD, period average"),
    ("population", "EGY", "SP.POP.TOTL",    "total population"),
    ("gdp_g",      "EGY", "NY.GDP.MKTP.KD.ZG", "real GDP growth, %"),
]


def _get(url, dest=None, timeout=240):
    """curl, not urllib — this session reaches the internet through an agent
    proxy with its own CA bundle that curl is configured for.  urllib succeeds
    against one host and is closed on by another, which reads as 'the source is
    unavailable' when it means 'the client is misconfigured' — an absent answer
    wearing the costume of a finding [R-ENF-04]."""
    cmd = ["curl", "-sS", "-L", "--max-time", str(timeout), url]
    if dest:
        cmd += ["-o", dest]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("fetch failed %s: %s" % (url, r.stderr.decode()[:200]))
    return r.stdout


def wb(country, ind):
    url = WB % (country, ind)
    d = json.loads(_get(url).decode("utf-8"))
    if not isinstance(d, list) or len(d) < 2 or d[1] is None:
        raise RuntimeError("World Bank returned no rows for %s" % ind)
    return url, {int(row["date"]): row["value"]
                 for row in d[1] if row["value"] is not None}


def coal():
    """World Bank Pink Sheet monthly -> calendar-year means.

    Both grades are returned.  South African is the escalator; Australian is a
    cross-check and is never averaged into it — two grades blended is a third
    series nobody publishes.
    """
    import openpyxl
    dest = os.path.join(SCRATCH, "CMO-Historical-Data-Monthly.xlsx")
    if not (os.path.exists(dest) and os.path.getsize(dest) > 100000):
        _get(PINK, dest)
    ws = openpyxl.load_workbook(dest, read_only=True, data_only=True)["Monthly Prices"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[4]
    col = {}
    for i, c in enumerate(hdr):
        if c and str(c).startswith("Coal, South African"):
            col["sa"] = i
        elif c and str(c).startswith("Coal, Australian"):
            col["au"] = i
    if set(col) != {"sa", "au"}:
        raise RuntimeError("pink sheet coal columns not found: %s" % col)
    acc = {}
    for r in rows:
        k = str(r[0] or "")
        if len(k) == 7 and k[4] == "M" and k[:4].isdigit():
            y = int(k[:4])
            for tag, i in col.items():
                v = r[i]
                if isinstance(v, (int, float)):
                    acc.setdefault((tag, y), []).append(float(v))
    out = {}
    for (tag, y), vals in acc.items():
        out.setdefault(tag, {})[y] = round(sum(vals) / len(vals), 4)
    return PINK, out, {tag: max(v) for tag, v in out.items()}


def main():
    got = {"retrieved": datetime.date.today().isoformat(), "series": {}}
    for key, ctry, ind, label in SERIES:
        url, vals = wb(ctry, ind)
        got["series"][key] = {"label": label, "source": url, "tier": "C",
                              "provider": "World Bank World Development Indicators",
                              "values": {str(k): v for k, v in sorted(vals.items())}}
        print("%-11s %d years  %s..%s" % (key, len(vals), min(vals), max(vals)), flush=True)
    url, cl, last = coal()
    for tag, label in (("sa", "Coal, South African, $/mt, calendar-year mean of monthly"),
                       ("au", "Coal, Australian, $/mt, calendar-year mean of monthly")):
        got["series"]["coal_" + tag] = {
            "label": label, "source": url, "tier": "C",
            "provider": "World Bank Commodity Price Data (the Pink Sheet), monthly",
            "derived": "calendar-year arithmetic mean of the published monthly series",
            "values": {str(k): v for k, v in sorted(cl[tag].items())}}
        print("coal_%-6s %d years  ..%s" % (tag, len(cl[tag]), last[tag]), flush=True)
    json.dump(got, open(OUT, "w"), indent=1)
    return got


if __name__ == "__main__":
    main()
