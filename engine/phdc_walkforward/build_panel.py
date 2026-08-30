"""Assemble the PHDC annual panel from the company's own filings.

Primary source for reported historicals is the audited/reviewed consolidated
financial statement (SIGCM clause 1: official sources only). The earnings
releases supply operating KPIs no financial statement carries — units sold,
new-sales value by region, deliveries, construction spend, backlog — and serve
as an independent cross-check on the statement figures.

Every field lands with value / source / date / tier. Nothing is interpolated.
"""
import os, re, json, sys, difflib
import parse_fs

HERE = os.path.dirname(os.path.abspath(__file__))
MN = 1e6

# canonical field -> label patterns as they appear in the translated statements
IS_MAP = [
    ("revenue",        r"^revenue",                     "revenues"),
    ("cogs",           r"^cost of revenue",             "cost of revenues"),
    ("cash_discount",  r"^cash discount",               "cash discount"),
    ("gross_profit",   r"^gross (operating )?profit",   "gross profit"),
    ("sga",            r"^general administrative|^general, administrative|^administrative, selling",
                       "general administrative selling and marketing expenses"),
    ("admin_depr",     r"^administrative depreciation|^depreciation (and|&) amortization|^depreciation amortization",
                       "administrative depreciation"),
    ("finance_cost",   r"^finance cost",                "finance costs & interests"),
    ("npbt",           r"before income tax|before tax.*non-controlling|year before income",
                       "net profit for the year before income tax & non-controlling interest"),
    ("income_tax",     r"^income tax( expense)?$",       "income tax expense"),
    ("deferred_tax",   r"^deferred tax$",               "deferred tax"),
    ("nci",            r"^non-controlling interest share", "non-controlling interest share- subsidiaries"),
    ("npat_pre_nci",   r"before .{0,4}non-controlling interest$|before & non-controlling",
                       "net profit for the year before & non-controlling interest"),
    ("npat_mi",        r"after income tax & non-controlling|after tax & non-controlling|"
                       r"after income tax and non-controlling",
                       "net profit for the year after income tax & non-controlling interest"),
    ("eps",            r"^earnings per share",          "earnings per share"),
]
BS_MAP = [
    ("investments_associates", r"^investments in associates"),
    ("investment_property",    r"^investment property"),
    ("nr_long",                r"^notes receivable long term|^notes receivable - long"),
    ("projects_under_constr",  r"^projects under construction"),
    ("fixed_assets",           r"^fixed assets"),
    ("total_noncurrent_assets", r"^total non-?current assets|^total long-?term assets"),
    ("wip",                    r"^works in process|^work in process"),
    ("cash",                   r"^cash and cash equivalents|^cash & cash equivalents"),
    ("nr_short",               r"^notes receivable short term|^notes receivable - short"),
    ("ar",                     r"^accounts receivable"),
    ("total_current_assets",   r"^total current assets"),
    ("banks_credit",           r"^banks credit balances|^banks - credit"),
    ("overdraft",              r"^bank-? ?overdraft|^banks ?[-–] ?overdraft"),
    ("advances_customers",     r"^advances from customers"),
    ("np_short",               r"^notes payable short term|^notes payable - short"),
    ("loans_current",          r"^current portion of term loans|^current portion of loans"),
    ("suppliers",              r"^suppliers and contractors|^suppliers & contractors"),
    ("total_current_liabs",    r"^total current liabilities"),
    ("issued_capital",         r"^issued and paid|^paid-?in capital"),
    ("total_equity",           r"^total (shareholders|equity)"),
    ("np_long",                r"^notes payable long term|^notes payable - long"),
    ("loans_lt",               r"^loans$|^term loans$|^long-?term loans"),
    ("total_lt_liabs",         r"^total long-?term liabilities|^total non-?current liabilities"),
]


def norm(lab):
    lab = re.sub(r"\s+", " ", lab).strip().lower()
    lab = re.sub(r"[\(\)\[\],:;.\u060c]", " ", lab)
    lab = re.sub(r"\b[a-z]?\d{1,2}[a-z]?\b", " ", lab)        # note references
    return re.sub(r"\s+", " ", lab).strip()


def pick(rows, pat, canon=None, cutoff=0.78):
    """Match a statement line by its label.

    Regex first — exact where the text layer is clean. Where the page came
    through OCR the label itself is noisy ("Cast of revenucs" for "Cost of
    revenues"), so a regex that is tight enough to be safe on clean text is
    guaranteed to miss on scanned years. The fallback is a similarity match
    against the canonical label, which is only consulted after the regex fails
    and is still subject to the statement's footing check downstream.
    """
    rx = re.compile(pat, re.I)
    hits = [r for r in rows if rx.search(norm(r["label"]))]
    if hits:
        # A wrapped line item leaves a TRUNCATED fragment behind that still
        # matches — "net profit for the year before income tax & non-" carries
        # a different row's figures than the completed line does. The complete
        # label is the longer one, so prefer it; a first-match rule silently
        # took the fragment and its wrong figures.
        return max(hits, key=lambda r: len(norm(r["label"])))
    if not canon:
        return None
    best, best_r = 0.0, None
    for r in rows:
        lab = norm(r["label"])
        if len(lab) < 4:
            continue
        sc = difflib.SequenceMatcher(None, lab, canon).ratio()
        if sc > best:
            best, best_r = sc, r
    return best_r if best >= cutoff else None


def to_mn(v, scale):
    return None if v is None else v / scale


def parse_year(year, route, gutter='pooled'):
    """Return (current, prior) dicts in EGP million for FY<year>."""
    stem = "%d_Q4_FS" % year
    p = parse_fs.parse_statement(stem, route, gutter=gutter)
    out = {"_stem": stem, "_route": route, "_gutter": gutter,
           "_pages": p["_pages"], "checks": {}}
    for key, mp, section in (("is", IS_MAP, "is"), ("bs", BS_MAP, "bs")):
        sec = p.get(section)
        if not sec or "rows" not in sec:
            continue
        rows = sec["rows"]
        # scale: statements are in EGP units; a page whose revenue is < 1e6 is
        # already in thousands. Detect from the largest figure on the page.
        mx = max((abs(v) for r in rows for v in r["v"] if v), default=0)
        scale = MN if mx > 1e8 else 1e3
        out.setdefault("_scale_" + key, scale)
        for entry in mp:
            field, pat = entry[0], entry[1]
            canon = entry[2] if len(entry) > 2 else None
            r = pick(rows, pat, canon)
            if r:
                out["%s.%s" % (key, field)] = [to_mn(r["v"][0], scale),
                                               to_mn(r["v"][1], scale)]
                out["%s.%s._src" % (key, field)] = r["label"]
    return out


def foot(out):
    """Check the parse against the statement's own arithmetic."""
    c = out["checks"]

    def g(k, i):
        v = out.get(k)
        return v[i] if v and v[i] is not None else None

    for i, tag in ((0, "cur"), (1, "pri")):
        rev, cogs, cd, gp = (g("is.revenue", i), g("is.cogs", i),
                             g("is.cash_discount", i), g("is.gross_profit", i))
        if None not in (rev, cogs, gp):
            calc = rev - cogs - (cd or 0)
            c["gp_" + tag] = {"stated": round(gp, 3), "computed": round(calc, 3),
                              "diff": round(gp - calc, 3),
                              "ok": abs(gp - calc) < max(1.0, abs(gp) * 1e-4)}
        nca, ca = g("bs.total_noncurrent_assets", i), g("bs.total_current_assets", i)
        if None not in (nca, ca):
            c["ta_" + tag] = {"total_assets": round(nca + ca, 3)}
    return out


def parse_year_checked(year):
    """Parse FY<year>, then check the parse against the statement's own arithmetic.

    The text layer is tried first because it is exact when it is right. Several
    of these filings embed a font whose ToUnicode map is wrong: the page RENDERS
    3 560 584 644 and the text layer EXTRACTS 1 654 670 500 — same positions,
    wrong glyphs, and nothing about the extraction looks broken. The only thing
    that catches it is the statement's own footing, so footing IS the gate: a
    page that does not foot is re-read by OCR off the rendered pixels, and if
    OCR foots, OCR wins. A year where neither route foots is reported as
    unresolved, never quietly kept.
    """
    attempts = []
    for route in ("text", "ocr"):
        for gutter in ("pooled", "perrow", "fixed"):
            try:
                out = foot(parse_year(year, route, gutter))
            except Exception as e:
                attempts.append({"route": route, "gutter": gutter,
                                 "error": "%s: %s" % (type(e).__name__, e)})
                continue
            ok = out["checks"].get("gp_cur", {}).get("ok")
            attempts.append({"route": route, "gutter": gutter, "gp_ok": ok,
                             "revenue": (out.get("is.revenue") or [None])[0]})
            if ok:
                out["_attempts"] = attempts
                return out
    out = out if "out" in dir() else {"_stem": "%d_Q4_FS" % year}
    out["_attempts"] = attempts
    out["_unresolved"] = True
    return out


if __name__ == "__main__":
    years = [int(a) for a in sys.argv[1:]] or list(range(2015, 2026))
    man = json.load(open(os.path.join(parse_fs.SRC, "text", "_manifest.json"))) \
        if os.path.exists(os.path.join(parse_fs.SRC, "text", "_manifest.json")) else {}
    res = {}
    for y in years:
        r = parse_year_checked(y)
        res[y] = r
        used = [a for a in r["_attempts"] if a.get("gp_ok")]
        print("FY%-5d %-13s rev=%-10s prior=%-10s foot=%s%s" % (
            y, ("%s/%s" % (used[0]["route"], used[0]["gutter"])) if used else "NONE",
            (round(r["is.revenue"][0], 1) if r.get("is.revenue") else None),
            (round(r["is.revenue"][1], 1) if r.get("is.revenue") else None),
            bool(used),
            "   <-- UNRESOLVED" if r.get("_unresolved") else ""))
    json.dump(res, open(os.path.join(HERE, "fs_parsed.json"), "w"), indent=1)
