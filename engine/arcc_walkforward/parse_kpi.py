"""Physical drivers from ARCC's OWN investor presentations — tonnes, prices per
tonne, cost per tonne, utilisation, market share, and the Egyptian market.

WHY THESE COME FROM THE DECKS AND NOT THE STATEMENTS: the audited accounts carry
no tonne.  Revenue is disclosed local/export and goods/services (note 4) and cost
by nature (note 5), and that is all.  Every unit driver in this walk-forward
therefore rests on the company's own IR channel, tagged COMPANY_IR and kept
distinct from the audited-statement tag so a reader can see how much of the
build stands on it.

WHY THE DECKS ARE CROSS-CHECKED AGAINST EACH OTHER RATHER THAN TRUSTED: each deck
reprints the three prior years beside the current one, so every year is stated
between two and four times across the archive — and THE ARCHIVE DISAGREES WITH
ITSELF.  The FY2016 deck prints FY2015 cement sales of 4,150kt where the FY2015
and FY2017 decks both print 4,271kt, and it prints FY2013 at 4,050kt against the
FY2015 deck's 4,021kt.  A single deck read once would have carried that in
silently.  The disagreements are collected, not resolved by preference: where two
decks differ, the value AS PUBLISHED AT THE ORIGIN is what the origin sees
(point-in-time), and the disagreement is registered.

The chart-block grammar is the deck's own: a run of data series, then axis ticks,
then the year labels, then the legend.  Series are taken as the FIRST
len(legend)*N numeric lines of the block, which is what the renderer emits, and
the YEAR LABELS ARE READ RATHER THAN ASSUMED — the FY2015 deck prints its
revenue chart in DESCENDING year order while every other deck ascends.
"""
import os, re, json, sys
import pymupdf

SCRATCH = os.environ.get("ARCC_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/82898002-da86-5df7-8203-457959546ece/scratchpad/arcc_src")
HERE = os.path.dirname(os.path.abspath(__file__))

YEAR = re.compile(r"^(?:FY\s?)(\d{2})$|^(FY\s?\d{4})$|^(20\d{2})$")
NUMLINE = re.compile(r"^\(?-?[\d,]+(?:\.\d+)?\)?%?$|^-$|^\(\d[\d,.]*\)$")


def is_year(s):
    s = s.strip()
    m = YEAR.match(s)
    if not m:
        return None
    if m.group(1):
        return 2000 + int(m.group(1))
    if m.group(2):
        return int(re.sub(r"\D", "", m.group(2)))
    return int(m.group(3))


def is_num(s):
    s = s.strip()
    return bool(s) and bool(NUMLINE.match(s))


def val(s):
    s = s.strip()
    neg = s.startswith("(") and s.endswith(")")
    pct = s.endswith("%")
    d = re.sub(r"[^\d.]", "", s)
    if not d or d == ".":
        return None
    v = float(d)
    if neg:
        v = -v
    return v / 100.0 if pct else v


def page_text(pdf, page_no):
    d = pymupdf.open(os.path.join(SCRATCH, pdf))
    return d[page_no - 1].get_text()


def charts(text, page_no=None):
    """Every (legend, {year: [series values]}) chart block on a page.

    The deck prints its own PAGE NUMBER as a bare integer in the header, which
    is number-shaped and sits ahead of the first chart's data.  Left in, it
    shifts every series on that page by one position — the first chart of every
    deck came back with the page number as its first data point and the whole
    row displaced.  It is removed by identity against the page number the caller
    resolved, not by a heuristic about small integers.
    """
    lines = [l.strip() for l in text.splitlines()]
    if page_no is not None:
        for i, l in enumerate(lines):
            if l == str(page_no):
                del lines[i]
                break
    out, i, block_start = [], 0, 0
    while i < len(lines):
        if is_year(lines[i]):
            j = i
            years = []
            while j < len(lines) and is_year(lines[j]):
                years.append(is_year(lines[j])); j += 1
            legend = []
            k = j
            while k < len(lines) and lines[k] and not is_num(lines[k]) and not is_year(lines[k]):
                legend.append(lines[k]); k += 1
            nums = [l for l in lines[block_start:i] if is_num(l)]
            n = len(years)
            series = {}
            for s_i, name in enumerate(legend):
                chunk = nums[s_i * n:(s_i + 1) * n]
                if len(chunk) == n:
                    series[name] = dict(zip(years, [val(c) for c in chunk]))
            if series:
                out.append({"years": years, "legend": legend, "series": series})
            block_start = k
            i = k
        else:
            i += 1
    return out


def kpi_page(pdf):
    """The 'Main KPIs' page of a deck, by its own heading."""
    d = pymupdf.open(os.path.join(SCRATCH, pdf))
    for i, pg in enumerate(d):
        t = pg.get_text()
        if "Main KPIs" in t:
            return i + 1, t
    return None, None


def market_page(pdf):
    d = pymupdf.open(os.path.join(SCRATCH, pdf))
    for i, pg in enumerate(d):
        t = pg.get_text()
        if "Domestic Consumption" in t:
            return i + 1, t
    return None, None


if __name__ == "__main__":
    pdf = sys.argv[1]
    no, t = kpi_page(pdf) if len(sys.argv) < 3 else market_page(pdf)
    print("%s  page %s" % (pdf, no))
    for c in charts(t or "", no):
        print("  legend=%s years=%s" % (c["legend"], c["years"]))
        for k, v in c["series"].items():
            print("     %-30s %s" % (k, v))


# ---------------------------------------------------------------------------
# The archive-wide harvest, with cross-deck agreement as the check.
# ---------------------------------------------------------------------------
CANON = {
    "clinker production": "clinker_prod_mt",
    "clinker utilization rate": "clinker_util",
    "cement production": "cement_prod_mt",
    "cement utilization rates": "cement_util",
    "cement sales volume": "sales_kt",
    "sales volume": "sales_kt",
    "market share": "market_share",
    "rev/ton": "rev_per_t",
    "cost/ton": "cost_per_t",
    "ebitda/ton": "ebitda_per_t",
    "domestic consumption": "eg_consumption_mt",
}

# Decks whose KPI page is the CHART layout.  The FY2024 and FY2025 decks moved
# to a printed table and are parsed from the table, not from chart geometry.
FY_DECKS = [
    ("ACC-FY-2015-Investors-presentation.pdf", "FY2015", "2016-02"),
    ("ACC-FY-2016-Investors-presentation.pdf", "FY2016", "2017-02"),
    ("ACC-FY-2017-Investors-presentation.pdf", "FY2017", "2018-02"),
    ("ACC_FY18_Investor_presentation.pdf",     "FY2018", "2019-02"),
    ("ACC_FY2019_Investor_Presentation.pdf",   "FY2019", "2020-02"),
    ("ACC_FY_20_INVESTOR_PRESENTATION.pdf",    "FY2020", "2021-02"),
    ("ACC_FY_2021_Investor_presentation.pdf",  "FY2021", "2022-02"),
    ("ACC_FY_2022_Investor_presentation.pdf",  "FY2022", "2023-02"),
    ("ACC_4Q_2023_Investor_presentation.pdf",  "FY2023", "2024-02"),
]


def harvest():
    """Every KPI every FY deck states, keyed (metric, fiscal year, deck).

    Nothing is reconciled here.  Two decks disagreeing about the same year is a
    FACT ABOUT THE ARCHIVE and is reported as one; silently preferring the later
    print would destroy exactly the point-in-time information the walk-forward
    runs on.
    """
    rows, seen = [], []
    for pdf, deck_fy, pub in FY_DECKS:
        if not os.path.exists(os.path.join(SCRATCH, pdf)):
            seen.append({"deck": pdf, "status": "absent"}); continue
        for finder in (kpi_page, market_page):
            no, t = finder(pdf)
            if not t:
                continue
            for c in charts(t, no):
                for name, series in c["series"].items():
                    key = CANON.get(name.strip().lower())
                    if not key:
                        continue
                    for y, v in series.items():
                        if v is None:
                            continue
                        rows.append({"metric": key, "fy": "FY%d" % y, "value": v,
                                     "deck": pdf, "deck_fy": deck_fy,
                                     "published": pub, "page": no, "label": name})
        seen.append({"deck": pdf, "status": "read"})
    return rows, seen


def disagreements(rows, tol=0.005):
    """Where two decks state the same (metric, year) differently."""
    by = {}
    for r in rows:
        by.setdefault((r["metric"], r["fy"]), []).append(r)
    out = []
    for k, rs in sorted(by.items()):
        vals = sorted({round(r["value"], 6) for r in rs})
        if len(vals) > 1:
            lo, hi = min(vals), max(vals)
            if hi == 0 or (hi - lo) / abs(hi) > tol:
                out.append({"metric": k[0], "fy": k[1],
                            "values": [{"deck": r["deck_fy"], "value": r["value"]} for r in rs]})
    return out


# ---------------------------------------------------------------------------
# Normalisation and the point-in-time physical series.
# ---------------------------------------------------------------------------
# From the FY2020 deck onward the sales-volume chart is printed in MILLION
# tonnes where the earlier decks printed THOUSAND tonnes (4.1 against 4,114).
# That is a UNIT CHANGE inside one series and it is exactly the kind of break
# that reads as a 99.9% collapse if it is not declared.  It is normalised to
# thousand tonnes here, by magnitude, and the rule is stated rather than
# applied silently: a sales figure below 100 is in millions.
def to_kt(v):
    return v * 1000.0 if v is not None and v < 100 else v


def physical(rows):
    """{metric: {FY: {"value":…, "sources":[…]}}} on the LATEST print, plus the
    full set of prints so a point-in-time reader can take the one its origin saw."""
    out = {}
    for r in rows:
        v = to_kt(r["value"]) if r["metric"] == "sales_kt" else r["value"]
        out.setdefault(r["metric"], {}).setdefault(r["fy"], []).append(
            {"value": v, "deck_fy": r["deck_fy"], "published": r["published"],
             "deck": r["deck"], "page": r["page"]})
    return out


def as_at(phys, metric, fy, origin_fy):
    """The value for `fy` AS PUBLISHED BY the deck for `origin_fy` — the number
    an origin standing at that year could actually have seen.  Falls back to the
    earliest later print only when the origin's own deck did not carry the year,
    and says which was used."""
    prints = phys.get(metric, {}).get(fy, [])
    if not prints:
        return None, None
    own = [p for p in prints if p["deck_fy"] == origin_fy]
    if own:
        return own[0]["value"], own[0]["deck_fy"]
    later = sorted((p for p in prints if p["deck_fy"] <= origin_fy),
                   key=lambda p: p["deck_fy"], reverse=True)
    if later:
        return later[0]["value"], later[0]["deck_fy"]
    return None, None
