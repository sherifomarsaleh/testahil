"""Egypt macro panel for the SWDY walk-forward — EXOGENOUS inputs only.

The Country/Industry-ring anchors the pre-registration names, and the series the
macro-versus-company error split re-runs each origin on. Fetched live so the panel
carries its own retrieval date rather than inheriting one.

THREE THINGS ARE SPECIFIC TO THIS NAME:

1. SWDY's fiscal year IS the calendar year — every filing in the archive is "for the
   financial year ended 31 December" — so no fiscal-to-calendar conversion is performed
   and none is needed. Stated because a construction carried across from another name
   without checking is an invented adjustment.

2. THE INPUT IS COPPER, AND COPPER IS NOT DOMESTIC INFLATION. A cable is metal: the
   company's own investor sheets publish a cable cost per tonne that tracks the metal,
   and the class lesson [L-110] from another name in this book says the same thing in
   general terms — a globally traded input follows the world price and the exchange
   rate, and escalating it with the domestic cost of living invents a margin story.
   Copper is the escalator for the copper leg and ALUMINIUM is carried beside it for
   the aluminium leg, never blended into a single metal series that nobody publishes.

3. THE CONTRACTING LEG HAS NO COMMODITY. Turnkey revenue is recognised as work
   completes on multi-year contracts, so its exogenous anchor is domestic activity —
   real GDP — and its cost anchor is domestic inflation. That the two legs need two
   different anchors IS the class finding [L-295], and it is why they are not averaged.
"""
import json, os, subprocess, datetime

os.environ.setdefault('OMP_THREAD_LIMIT', '1')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "macro.json")
SCRATCH = os.environ.get(
    "SWDY_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/82898002-da86-5df7-8203-457959546ece/scratchpad/swdy_src")

WB = ("https://api.worldbank.org/v2/country/%s/indicator/%s"
      "?format=json&per_page=300&date=2000:2026")
PINK = ("https://thedocs.worldbank.org/en/doc/"
        "74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/"
        "CMO-Historical-Data-Monthly.xlsx")

SERIES = [
    ("cpi_pct",    "EGY", "FP.CPI.TOTL.ZG",    "annual consumer price inflation, %"),
    ("cpi_index",  "EGY", "FP.CPI.TOTL",       "consumer price index, 2010 = 100"),
    ("egp_usd",    "EGY", "PA.NUS.FCRF",       "official exchange rate, EGP per USD, period average"),
    ("population", "EGY", "SP.POP.TOTL",       "total population"),
    ("gdp_g",      "EGY", "NY.GDP.MKTP.KD.ZG", "real GDP growth, %"),
    ("gfcf_g",     "EGY", "NE.GDI.FTOT.KD.ZG", "gross fixed capital formation, real growth, %"),
]
METALS = [("copper", "Copper"), ("aluminum", "Aluminum")]


def _get(url, dest=None, timeout=300):
    """curl, not urllib — this session reaches the internet through an agent proxy with
    its own CA bundle that curl is configured for. urllib succeeds against one host and
    is closed on by another, which reads as 'the source is unavailable' when it means
    'the client is misconfigured' — an absent answer wearing a finding's costume."""
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
    return url, {int(row["date"]): row["value"] for row in d[1] if row["value"] is not None}


def metals():
    """World Bank Pink Sheet monthly -> calendar-year means, per metal, unblended."""
    import openpyxl
    os.makedirs(SCRATCH, exist_ok=True)
    dest = os.path.join(SCRATCH, "CMO-Historical-Data-Monthly.xlsx")
    if not (os.path.exists(dest) and os.path.getsize(dest) > 100000):
        _get(PINK, dest)
    ws = openpyxl.load_workbook(dest, read_only=True, data_only=True)["Monthly Prices"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[4]
    col = {}
    for i, c in enumerate(hdr):
        s = str(c or "").strip()
        for tag, name in METALS:
            if s == name or s.startswith(name + ","):
                col[tag] = i
    missing = [t for t, _ in METALS if t not in col]
    if missing:
        raise RuntimeError("pink sheet metal columns not found: %s" % missing)
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
    return PINK, out


def main():
    got = {"retrieved": datetime.date.today().isoformat(), "series": {}}
    for key, ctry, ind, label in SERIES:
        url, vals = wb(ctry, ind)
        got["series"][key] = {"label": label, "source": url, "tier": "C",
                              "provider": "World Bank World Development Indicators",
                              "values": {str(k): v for k, v in sorted(vals.items())}}
        print("%-11s %d years  %s..%s" % (key, len(vals), min(vals), max(vals)), flush=True)
    url, m = metals()
    for tag, name in METALS:
        got["series"][tag] = {
            "label": "%s, $/mt, calendar-year mean of the published monthly series" % name,
            "source": url, "tier": "C",
            "provider": "World Bank Commodity Price Data (the Pink Sheet), monthly",
            "derived": "calendar-year arithmetic mean of the published monthly series",
            "values": {str(k): v for k, v in sorted(m[tag].items())}}
        print("%-11s %d years  ..%s" % (tag, len(m[tag]), max(m[tag])), flush=True)
    json.dump(got, open(OUT, "w"), indent=1)
    return got


if __name__ == "__main__":
    main()
