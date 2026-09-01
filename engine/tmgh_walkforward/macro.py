"""Egypt (and Saudi) macro panel for the TMGH walk-forward.

Exogenous inputs only — inflation, FX, population, urbanisation. These are the
Country-ring anchors the pre-registration names, and they are the series the
macro-vs-company error split re-runs each origin on. Fetched live from the
World Bank WDI so the panel carries its own retrieval date rather than
inheriting one from another run.
"""
import json, os, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
WB = "https://api.worldbank.org/v2/country/%s/indicator/%s?format=json&per_page=200&date=2004:2026"

SERIES = [
    ("cpi_pct",    "EGY", "FP.CPI.TOTL.ZG", "annual consumer price inflation, %"),
    ("egp_usd",    "EGY", "PA.NUS.FCRF",    "official exchange rate, EGP per USD, period average"),
    ("population", "EGY", "SP.POP.TOTL",    "total population"),
    ("urban_pop",  "EGY", "SP.URB.TOTL",    "urban population"),
    ("gdp_pc_kd",  "EGY", "NY.GDP.PCAP.KD", "GDP per capita, constant 2015 USD"),
    ("sa_cpi_pct", "SAU", "FP.CPI.TOTL.ZG", "Saudi annual consumer price inflation, %"),
    ("sar_usd",    "SAU", "PA.NUS.FCRF",    "official exchange rate, SAR per USD, period average"),
]


def fetch(country, ind):
    url = WB % (country, ind)
    with urllib.request.urlopen(urllib.request.Request(
            url, headers={"User-Agent": "testahil-research/1.0"}), timeout=120) as r:
        d = json.loads(r.read().decode("utf-8"))
    return url, {row["date"]: row["value"] for row in d[1] if row["value"] is not None}


def main():
    out = {"_retrieved": time.strftime("%Y-%m-%d"), "_tier": "C",
           "_note": ("World Bank WDI. Tier C by the provenance ladder — a credible "
                     "third party, used only for EXOGENOUS country variables. No "
                     "company figure comes from here.")}
    for key, ctry, ind, desc in SERIES:
        url, vals = fetch(ctry, ind)
        out[key] = {k: v for k, v in sorted(vals.items())}
        out[key + "_source"] = {"url": url, "indicator": ind, "country": ctry,
                                "description": desc}
        print("%-12s %s  %d years %s-%s" % (key, ind, len(vals),
                                            min(vals), max(vals)))
    json.dump(out, open(os.path.join(HERE, "macro.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
