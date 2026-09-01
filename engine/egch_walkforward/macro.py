"""Egypt macro panel for the EGCH (KIMA) walk-forward — EXOGENOUS inputs only.

The Country/Industry-ring anchors the pre-registration names, and the series the
macro-versus-company split re-runs each origin on. Fetched live so the panel carries
its own retrieval date.

THREE THINGS ARE SPECIFIC TO THIS NAME:

1. KIMA's fiscal year runs JULY to JUNE. Calendar-year series (World Bank CPI, FX)
   are converted as the mean of the two calendar years the fiscal year spans; monthly
   series (World Bank pink-sheet urea, European natural gas) are averaged over the
   actual twelve months. Both are DERIVED and are marked as such.

2. KIMA is a nitrogen-fertiliser producer. Its exogenous PRICE anchor is the world urea
   price (World Bank CMO 'Urea', bulk, f.o.b. Middle East, US$/t) translated at the
   EGP/USD rate. Its dominant physical input since the KIMA-2 complex (FY2020) is
   natural gas at an ADMINISTERED dollar price (US$4.50/mmBtu, raised to US$5.75 from
   November 2021) — the world gas price is fetched as context only, because the
   company does not pay it.

3. THE MACRO PATH IS ONE PATH (L-048). The knowable path at an origin holds the world
   urea price flat in dollars and moves the currency by relative purchasing-power
   parity on the last published CPI differential, so domestic costs, the currency and
   the product price are the same event seen once. This is a pre-registration choice
   made before any result and its reason is stated in PRE_REGISTRATION_01-09-2026.md.
"""
import json, os, time, subprocess, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get("EGCH_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/4dcd71a4-ebf9-53cb-b878-3d0038ce9944/scratchpad")
WB = "https://api.worldbank.org/v2/country/%s/indicator/%s?format=json&per_page=200&date=2004:2026"
CMO_PAGE = "https://www.worldbank.org/en/research/commodity-markets"
CMO_URL = ("https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/"
           "related/CMO-Historical-Data-Monthly.xlsx")

SERIES = [
    ("cpi_eg_pct", "EGY", "FP.CPI.TOTL.ZG", "Egypt annual consumer price inflation, %"),
    ("cpi_us_pct", "USA", "FP.CPI.TOTL.ZG", "United States annual consumer price inflation, %"),
    ("egp_usd",    "EGY", "PA.NUS.FCRF",    "official exchange rate, EGP per USD, period average"),
    ("gdp_pc_kd",  "EGY", "NY.GDP.PCAP.KD", "GDP per capita, constant 2015 USD"),
]


def _get(url, timeout=180, dest=None):
    """curl, not urllib — this session's egress proxy is configured for curl."""
    args = ["curl", "-sSL", "--max-time", str(timeout), url]
    if dest:
        args += ["-o", dest]
    r = subprocess.run(args, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("fetch failed %s: %s" % (url, r.stderr.decode()[:200]))
    return r.stdout if not dest else open(dest, "rb").read()


def wb(country, ind):
    url = WB % (country, ind)
    d = json.loads(_get(url).decode("utf-8"))
    return url, {row["date"]: row["value"] for row in d[1] if row["value"] is not None}


def cmo_monthly():
    """World Bank pink sheet — urea (US$/t) and European natural gas (US$/mmBtu)."""
    import openpyxl
    dest = os.path.join(SCRATCH, "cmo2026.xlsx")
    if not os.path.exists(dest):
        _get(CMO_URL, dest=dest)
    wb_ = openpyxl.load_workbook(dest, read_only=True)
    ws = wb_["Monthly Prices"]
    rows = list(ws.iter_rows(values_only=True))
    updated = str(rows[3][0])
    hdr = rows[4]
    idx = {str(h).strip(): i for i, h in enumerate(hdr) if h}
    out = {"urea_usd_t": {}, "gas_eu_usd_mmbtu": {}}
    for r in rows[6:]:
        if not r[0] or "M" not in str(r[0]):
            continue
        key = str(r[0]).replace("M", "-")
        u, g = r[idx["Urea"]], r[idx["Natural gas, Europe"]]
        if isinstance(u, (int, float)):
            out["urea_usd_t"][key] = float(u)
        if isinstance(g, (int, float)):
            out["gas_eu_usd_mmbtu"][key] = float(g)
    return updated, out


def fy_from_months(monthly, fy_end_year):
    keys = ["%d-%02d" % (fy_end_year - 1, m) for m in range(7, 13)] + \
           ["%d-%02d" % (fy_end_year, m) for m in range(1, 7)]
    vals = [monthly[k] for k in keys if k in monthly]
    return statistics.fmean(vals) if len(vals) == 12 else None


def fy_from_calendar(annual, fy_end_year):
    a, b = annual.get(str(fy_end_year - 1)), annual.get(str(fy_end_year))
    if a is None or b is None:
        return None
    return (a + b) / 2.0


def main():
    out = {"_retrieved": time.strftime("%Y-%m-%d"), "_tier": "C",
           "_note": ("World Bank WDI (CPI, FX) and the World Bank Commodity Markets pink sheet "
                     "(urea, European gas). Tier C — credible third parties, used ONLY for "
                     "exogenous country and commodity variables. No KIMA figure comes from here."),
           "_fy_convention": ("KIMA's fiscal year is 1 July to 30 June. Calendar-year series are "
                              "converted as the mean of the two calendar years the fiscal year "
                              "spans; monthly series are averaged over the actual twelve months. "
                              "Both are DERIVED and marked."),
           "sources": {}}
    ann = {}
    for key, ctry, ind, desc in SERIES:
        url, vals = wb(ctry, ind)
        ann[key] = vals
        out[key + "_cy"] = vals
        out["sources"][key] = {"url": url, "desc": desc, "basis": "calendar year"}
    updated, cmo = cmo_monthly()
    out["urea_usd_monthly"] = cmo["urea_usd_t"]
    out["gas_eu_usd_monthly"] = cmo["gas_eu_usd_mmbtu"]
    out["sources"]["cmo"] = {"url": CMO_URL, "found_on": CMO_PAGE, "file_updated": updated,
                             "desc": "World Bank Commodity Markets Outlook, monthly prices: "
                                     "Urea (bulk, f.o.b. Middle East, US$/t); Natural gas, "
                                     "Europe (US$/mmBtu)", "basis": "monthly"}
    fy = {}
    for y in range(2006, 2027):
        rec = {}
        for key in ("cpi_eg_pct", "cpi_us_pct", "egp_usd", "gdp_pc_kd"):
            v = fy_from_calendar(ann[key], y)
            if v is not None:
                rec[key] = v
        # the last PUBLISHED calendar-year rate at a fiscal-year-end origin: CY(y-1)
        for key in ("cpi_eg_pct", "cpi_us_pct"):
            v = ann[key].get(str(y - 1))
            if v is not None:
                rec[key + "_last_published"] = v
        u = fy_from_months(cmo["urea_usd_t"], y)
        if u is not None:
            rec["urea_usd"] = u
        g = fy_from_months(cmo["gas_eu_usd_mmbtu"], y)
        if g is not None:
            rec["gas_eu_usd"] = g
        if rec.get("urea_usd") and rec.get("egp_usd"):
            rec["urea_egp"] = rec["urea_usd"] * rec["egp_usd"]
        fy["FY%d" % y] = rec
    out["fiscal_year_derived"] = fy
    # the administered gas price KIMA actually pays, from its own filings (note 28)
    out["administered_gas_usd_mmbtu"] = {
        "to_FY2022": 4.50, "from_FY2023": 5.75,
        "source": "KIMA audited FY2024/25 statements, note 28: price raised from US$4.50 to "
                  "US$5.75/mmBtu under the November-2021 decision, applied from 13 September 2022",
        "tier": "A"}
    json.dump(out, open(os.path.join(HERE, "macro.json"), "w"), indent=1)
    for y in sorted(fy):
        r = fy[y]
        print("%s  cpiEG %5.1f%% (pub %5.1f)  cpiUS %4.1f%%  egp/usd %6.2f  urea $%6.1f  urea EGP %8.0f  gasEU %5.2f"
              % (y, r.get("cpi_eg_pct", float("nan")), r.get("cpi_eg_pct_last_published", float("nan")),
                 r.get("cpi_us_pct", float("nan")), r.get("egp_usd", float("nan")),
                 r.get("urea_usd", float("nan")), r.get("urea_egp", float("nan")),
                 r.get("gas_eu_usd", float("nan"))))


if __name__ == "__main__":
    main()
