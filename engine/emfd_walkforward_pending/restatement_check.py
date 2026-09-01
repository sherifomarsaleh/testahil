#!/usr/bin/env python3
"""EMFD — as-reported versus as-restated, from the company's own statements.

[R-FCAL-01] §1: "POINT-IN-TIME DISCIPLINE IS ABSOLUTE (each origin sees only
what was published by that date, as originally reported, restatements noted
beside not substituted)."

Every annual statement prints two columns: the year it reports on, and that
year's comparative as the company chose to present it one year later. Reading
both columns for every year the text layer allows turns the restatement history
into a measured object rather than a thing to be remembered.

This ran before any modelling and found one. It is committed because the finding
belongs to the basis-break register, and because a reclassification that leaves
profit untouched is invisible to every check that looks at the bottom line.

Output: restatements.json
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PDFS = os.environ.get(
    "EMFD_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/5c3bac54-80e7-5e98-82bb-8cfd0b2244dd"
    "/scratchpad/emfd_src/pdfs")

# Label -> the sign the statement itself prints it with. Cost, expenses and tax
# are shown in brackets; the parser reads magnitudes and the sign is applied
# here, so a bracket the extractor missed shows up as a footing failure rather
# than as a silently wrong number.
LINES = [
    ("revenue",            r"^\s*Revenue\s*$",                          +1),
    ("cost_of_revenue",    r"^\s*Cost of revenue\s*$",                  -1),
    ("gross_profit",       r"^\s*GROSS PROFIT\s*$",                     +1),
    ("selling_marketing",  r"^\s*Selling and marketing expenses\s*$",   -1),
    ("g_and_a",            r"^\s*General and administrative expenses\s*$", -1),
    ("finance_income",     r"^\s*Finance income\s*$",                   +1),
    ("finance_cost",       r"^\s*Finance cost\s*$",                     -1),
    ("other_income",       r"^\s*(Net other income|Other income)\s*$",  +1),
    ("provisions",         r"^\s*Provisions\s*$",                       -1),
    ("provisions_released", r"^\s*Provisions no longer required\s*$",   +1),
    ("pbt",                r"^\s*PROFIT FOR THE YEAR BEFORE INCOME TAX\s*$", +1),
    ("income_tax",         r"^\s*Income tax\s*$",                       -1),
    ("profit",             r"^\s*PROFIT FOR THE YEAR\s*$",              +1),
]

# One comma group is enough: a finance cost of 536,779 has only one, and
# requiring two silently dropped it -- which then made the whole column fail to
# foot. The footing check caught it; nothing about the extraction looked wrong.
MONEY = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?")


def pl_page(doc):
    import pymupdf
    for i in range(doc.page_count):
        t = doc[i].get_text()
        if re.search(r"(?i)statement of profit or loss", t) and \
                len(MONEY.findall(t)) >= 8:
            return t
    return None


def read_two_columns(text):
    """The text layer emits the statement one cell per line, label first, then
    the note reference, then the two year columns. Walk forward from each label
    and take the next two money figures: current year, then comparative."""
    lines = [l.strip() for l in text.splitlines()]
    out = {}
    for key, pat, sign in LINES:
        rx = re.compile(pat, re.I)
        for i, ln in enumerate(lines):
            if not rx.match(ln):
                continue
            found = []
            for j in range(i + 1, min(len(lines), i + 12)):
                found += [float(m.replace(",", ""))
                          for m in MONEY.findall(lines[j])]
                if len(found) >= 2:
                    break
            if len(found) >= 2:
                out[key] = {"current": sign * found[0],
                            "comparative": sign * found[1]}
            break
    return out


def foots(col):
    """Arithmetic is the arbiter. Both identities, on both columns."""
    ok = []
    if all(k in col for k in ("revenue", "cost_of_revenue", "gross_profit")):
        ok.append(abs(col["revenue"] + col["cost_of_revenue"]
                      - col["gross_profit"]) < 1.0)
    if all(k in col for k in ("pbt", "income_tax", "profit")):
        ok.append(abs(col["pbt"] + col["income_tax"] - col["profit"]) < 1.0)
    parts = ["gross_profit", "selling_marketing", "g_and_a", "finance_income",
             "finance_cost", "other_income", "provisions", "provisions_released"]
    if all(k in col for k in parts + ["pbt"]):
        ok.append(abs(sum(col[k] for k in parts) - col["pbt"]) < 1.0)
    return ok



def eas48():
    """The one period the company published on both revenue bases.

    EAS 47/48/49 (the Egyptian analogues of IFRS 9/15/16, Ministerial Resolution
    69 of 2019) were adopted for the FIRST time in the 2021 interims; the FY2020
    statements say in terms that the Group elected not to early adopt. The H1
    2021 filing therefore prints its H1 2020 comparative marked "(Restated)",
    and the H1 2020 filing printed the same period on the old basis.

    Differencing the two measures what the standard did to this company's
    revenue and cost. It is the only place in the obtainable window where that
    measurement can be made at all, and it is the reason the pre-2021 years and
    the post-2021 years are not one series.

    THE COLUMN ORDER IS NOT THE SAME IN THE TWO FILINGS and it is not
    guessable: the 2020 interim prints six-month columns first (2020, 2019)
    then three-month (2020, 2019), and the 2021 interim prints three-month
    first (2021, 2020) then six-month (2021, 2020). Taking "the second number"
    from each would compare six months against three and produce a confident
    nonsense, so the index is stated per file and asserted against the header
    the file itself prints.
    """
    import pymupdf

    SPEC = {
        "pre": {"file": "Emaar-Misr-IR-Reports-Financial-Statements-"
                        "2020-Q2-EN-Consolidated.pdf",
                "header": "Six Months",       # six-month block comes first
                "col": 0},                    # 6M-2020, as originally reported
        "post": {"file": "Emaar-Misr-IR-Reports-Financial-Statements-"
                         "2021-Q2-EN-Consolidated.pdf",
                 "header": "Three-month period",   # three-month block first
                 "col": 3},                   # 6M-2020 comparative, restated
    }
    LBL = [("revenue", "Revenue", +1),
           ("cost_of_revenue", "Cost of revenue", -1),
           ("gross_profit", "GROSS PROFIT", +1)]

    def grab(spec):
        path = os.path.join(PDFS, spec["file"])
        if not os.path.exists(path):
            return None, "file not present"
        doc = pymupdf.open(path)
        for i in range(doc.page_count):
            t = doc[i].get_text()
            if "Cost of revenue" not in t or len(MONEY.findall(t)) < 12:
                continue
            flat = " ".join(t.split())
            if spec["header"] not in flat:
                return None, ("column header %r not found — the layout moved "
                              "and the column index can no longer be trusted"
                              % spec["header"])
            out = {}
            for key, label, sign in LBL:
                m = re.search(re.escape(label) + r"\b(.{0,180})", flat)
                if not m:
                    continue
                ns = [float(x.replace(",", ""))
                      for x in MONEY.findall(m.group(1))]
                if len(ns) > spec["col"]:
                    out[key] = sign * ns[spec["col"]]
            return out, None
        return None, "no profit-or-loss page found"

    a, err_a = grab(SPEC["pre"])
    b, err_b = grab(SPEC["post"])
    if a is None or b is None:
        return {"lines": {}, "note": err_a or err_b}

    # Arithmetic is the arbiter here too: if the three lines picked out of each
    # filing do not foot among themselves, the column index is wrong and the
    # comparison must not be published.
    for name, col in (("pre", a), ("post", b)):
        if all(k in col for k in ("revenue", "cost_of_revenue", "gross_profit")):
            if abs(col["revenue"] + col["cost_of_revenue"]
                   - col["gross_profit"]) >= 1.0:
                return {"lines": {}, "note": "%s column does not foot — "
                                             "wrong column picked" % name}

    lines = {}
    for k in sorted(set(a) & set(b)):
        if a[k]:
            lines[k] = {"as_reported": a[k], "as_restated": b[k],
                        "delta": b[k] - a[k],
                        "pct": 100.0 * (b[k] - a[k]) / abs(a[k])}
    return {"period": "six months ended 30 June 2020",
            "pre_basis_source": SPEC["pre"]["file"],
            "post_basis_source": SPEC["post"]["file"], "lines": lines}


FILES = {
    2017: "Emaar-Misr-IR-Reports-Financial-Statements-2017-Year-End-EN.pdf",
    2018: "Emaar-Misr-IR-Reports-Financial-Statements-2018-Year-End-EN-Consolidated.pdf",
    2019: "Emaar-Misr-IR-Reports-Financial-Statements-2019-Year-End-EN-Consolidated.pdf",
    2020: "Emaar-Misr-IR-Reports-Financial-Statements-2020-Q4-EN-Consolidated.pdf",
}


def main():
    import pymupdf
    reported, restated, footing = {}, {}, {}
    for year, name in sorted(FILES.items()):
        path = os.path.join(PDFS, name)
        if not os.path.exists(path):
            continue
        text = pl_page(pymupdf.open(path))
        if text is None:
            continue
        cols = read_two_columns(text)
        cur = {k: v["current"] for k, v in cols.items()}
        cmp_ = {k: v["comparative"] for k, v in cols.items()}
        reported[year] = cur                      # year, as it reported itself
        restated[year - 1] = cmp_                 # prior year, one year later
        footing[year] = {"current": foots(cur), "comparative": foots(cmp_)}

    diffs = []
    for year in sorted(set(reported) & set(restated)):
        a, b = reported[year], restated[year]
        for k in sorted(set(a) & set(b)):
            if abs(a[k] - b[k]) >= 1.0:
                diffs.append({"year": year, "line": k,
                              "as_reported": a[k], "as_restated": b[k],
                              "delta": b[k] - a[k]})

    # THE REPORTING ENTITY IS READ OFF THE FILING, NEVER INFERRED FROM THE
    # FILENAME. The company published a single set of statements to FY2017 and a
    # consolidated set from FY2018; a panel that mixes the two without saying so
    # is comparing two different entities.
    entity = {}
    for year, name in sorted(FILES.items()):
        path = os.path.join(PDFS, name)
        if not os.path.exists(path):
            continue
        head = " ".join(" ".join(pymupdf.open(path)[i].get_text()
                                 for i in range(3)).split())
        entity[year] = ("consolidated"
                        if re.search(r"CONSOLIDATED FINANCIAL STATEMENTS", head,
                                     re.I) else "single entity")

    out = {"as_reported": reported, "as_restated_one_year_later": restated,
           "footing_checks": footing, "differences": diffs,
           "reporting_entity_by_filing": entity,
           "eas_48_interim": eas48()}
    with open(os.path.join(HERE, "restatements.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)

    print("years read as reported   : %s" % sorted(reported))
    print("years read as restated   : %s" % sorted(restated))
    bad = [(y, c) for y, d in footing.items() for c, r in d.items()
           if r and not all(r)]
    print("columns that do not foot : %s" % (bad or "none"))
    e = out["eas_48_interim"]
    if e.get("lines"):
        print("\nEAS 47/48/49 first-time adoption, measured on the one interim")
        print("period the company published on BOTH bases (six months to 30 June 2020):")
        for k, v in sorted(e["lines"].items()):
            print("  {:<16} pre-EAS48 {:>16,.0f}   post-EAS48 {:>16,.0f}   "
                  "{:+.2f}%".format(k, v["as_reported"], v["as_restated"],
                                    v["pct"]))
    print("\nlines restated one year later:")
    if not diffs:
        print("  none")
    for d in diffs:
        print("  FY{} {:<20} reported {:>18,.0f}  restated {:>18,.0f}  "
              "delta {:+,.0f}".format(d["year"], d["line"], d["as_reported"],
                                      d["as_restated"], d["delta"]))


if __name__ == "__main__":
    main()
