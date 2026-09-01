"""The pre-2018 earnings releases' own summary table, read on its own geometry.

Between FY2010 and FY2017 TMG published its results in a "Key Operational
Highlights" table rather than a statement layout: revenue and cost by segment,
gross profit, overheads and financing, with a share-of-revenue percentage
between every pair of figures and both a quarter and a full-year pair of
columns. The column ORDER moves between years — FY2012, FY2013, FY2015 and
FY2016 print the annual pair first, FY2014 prints it last — so the geometry is
read off the table's own heading every time, and a table whose heading cannot
be read yields nothing.

Percentages are dropped by their trailing sign rather than by position. That
one rule is what lets the same reader handle this table, the 2018-onward
release layout and the audited statements: in all three, a figure followed by
"%" is a share or a change and never a value.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import parse_fs as P
import parse_tables as T

COL = re.compile(r"\b(?:(FY|F|12M)\s?-?\s?((?:20)?\d{2})|([1-4])\s?Q\s?-?\s?((?:20)?\d{2})"
                 r"|(?<![\d-])(20[01-2]\d)(?![\d]))\b")


def _yr(y):
    y = int(y)
    return y if y > 100 else 2000 + y


def header_columns(text, at, back=1400):
    """The period columns the table declares, in the order it prints them."""
    lo = text.rfind("<<<PAGE", 0, at)
    head = text[max(lo, at - back) if lo >= 0 else max(0, at - back): at]
    hi = head.rfind("Key Operational Highlights")
    if hi < 0:
        return None
    tagged, bare = [], []
    for m in COL.finditer(head[hi:]):
        if m.group(1):
            tagged.append({"year": _yr(m.group(2)), "annual": True})
        elif m.group(3):
            tagged.append({"year": _yr(m.group(4)), "annual": False})
        else:
            bare.append({"year": _yr(m.group(5)), "annual": True})
    # A bare year is only a column heading where the table tags NONE of its
    # columns (the FY2010 layout, "2010 / 2009 / change"). Where FY- and Q-
    # tags are present, a bare year in the heading is the release's own title
    # date — reading it as an annual column turned every interim release into
    # a source of full-year figures.
    cols = tagged or bare
    # a heading repeats the year in its own title line; collapse a run that
    # merely restates the period the release covers
    out = []
    for c in cols:
        if not out or c != out[-1]:
            out.append(c)
    return out or None


VAL = re.compile(r"(\(?-?\d[\d,.]*\)?)(\s*%)?")


def row_values(text, m, ncols, window=420):
    """The row's figures, with every percentage dropped by its trailing sign."""
    tail = P.repair_ocr(text[m.end(): m.end() + window])
    out, seen_big = [], False
    for t in VAL.finditer(tail):
        tok = t.group(1)
        if t.group(2):
            continue                       # a share or a change, never a value
        v = P.to_num(tok)
        if v is None:
            continue
        if (not seen_big and "(" not in tok[1:] and ")" in tok
                and "," not in tok and "." not in tok and abs(v) < 100):
            continue                       # note reference
        if abs(v) >= 1000:
            seen_big = True
        out.append(v)
        if len(out) >= ncols:
            break
    return out


LEGACY = {
    "dev_revenue":   [r"^\s*Revenues? from units sold\b"],
    "hosp_revenue":  [r"^\s*Revenues? from [Hh]otels\b"],
    "other_revenue": [r"^\s*Other revenues?\b"],
    "total_revenue": [r"^\s*Total consolidated revenue\b"],
    "dev_cost":      [r"^\s*Real Estate (?:&|and) Construction Cost\b"],
    "hosp_cost":     [r"^\s*Hotels? Cost\b"],
    "other_cost":    [r"^\s*Services? Cost\b"],
    "total_cost":    [r"^\s*Total cost of goods sold\b"],
    "gross_profit":  [r"^\s*Gross profit\b"],
    "sga":           [r"^\s*Selling, [Gg]eneral and [Aa]dministrative [Ee]xpenses\b"],
    "finance_cost":  [r"^\s*interest expense\b"],
    "finance_income": [r"^\s*interest income\b"],
    "investment_income": [r"^\s*investment income\b"],
    "da":            [r"^\s*[Dd]epreciation\b"],
    "pbt":           [r"^\s*Net profit before tax\b", r"^\s*Profit before tax\b"],
    "tax":           [r"^\s*Income tax\b", r"^\s*Tax\b"],
    "net_profit":    [r"^\s*Net profit after tax\b"],
    "npat_parent":   [r"^\s*Net profit after tax and minority\b",
                      r"^\s*Net profit attributable to (?:the )?parent\b"],
}


def read_doc(name):
    """{year: {field: value}} for one legacy release, EGP mn."""
    text = P.load(name)
    out, prov = {}, {}
    for field, pats in LEGACY.items():
        for pat in pats:
            hit = None
            for m in re.finditer(pat, text, re.I | re.M):
                cols = header_columns(text, m.start())
                if not cols:
                    continue
                vals = row_values(text, m, len(cols))
                if len(vals) < len(cols):
                    continue
                hit = (cols, vals, m)
                break
            if hit:
                cols, vals, m = hit
                pg, route = P.page_of(text, m.start())
                for c, v in zip(cols, vals):
                    if not c["annual"]:
                        continue
                    out.setdefault(c["year"], {})[field] = v
                    prov.setdefault(c["year"], {})[field] = {
                        "doc": name, "page": pg, "route": route,
                        "label": m.group(0).strip()[:60], "scale": 1.0,
                        "unit_evidence": "Key Operational Highlights, EGPmn",
                        "columns": [("%dA" % c0["year"]) if c0["annual"]
                                    else ("%dQ" % c0["year"]) for c0 in cols]}
                break
    return out, prov


def main():
    reg = json.load(open(os.path.join(HERE, "ir_register.json")))
    out = {}
    for r in reg:
        if r["kind"] != "earnings_release" or r.get("fetched") not in ("ok", "cached"):
            continue
        # only a FULL-YEAR release states full-year columns
        if not re.search(r"full year|FY|financial year|4Q|12M", r["name"], re.I):
            continue
        base = re.sub(r"[^A-Za-z0-9._-]+", "_", r["name"])[:150][:-4]
        if not os.path.exists(os.path.join(P.TEXT, base + ".txt")):
            continue
        vals, prov = read_doc(base)
        if not vals:
            continue
        out[base] = {"url": r["url"], "period_from_filename": r["period"],
                     "by_year": {str(y): v for y, v in vals.items()},
                     "prov": {str(y): v for y, v in prov.items()}}
    json.dump(out, open(os.path.join(HERE, "legacy_parsed.json"), "w"), indent=1)
    print("legacy tables read in %d releases" % len(out))
    for k, v in sorted(out.items()):
        print("  %-62s %s" % (k[:60], sorted(v["by_year"])))


if __name__ == "__main__":
    main()
