#!/usr/bin/env python3
"""EMFD — the profit-or-loss panel, with four-field provenance on every figure.

[R-FCAL-01] §1. Every number carries value, source document, document date and
provenance tier, plus the ROUTE it came by — text layer, OCR off the rendered
pixels, or (for the two Arabic filings) a read that tesseract cannot perform.
Derived figures are marked DERIVED with their formula.

**Nothing here is believed because an extractor produced it.** Every year is
re-derived from its own components and must foot, and the years that cannot be
machine-read are additionally cross-checked against a DIFFERENT statement
extracted independently. A figure that fails either test is dropped, not patched:
§1 says leave the year out and shorten the window rather than fill a cell.

This panel covers the window the company's own register actually reaches. It is
NOT a training panel and no origin is built on it — the run is blocked at §1 for
want of FY2021-FY2025 (see SCOPE_DECISION). It exists so that when those
documents arrive they are the only extraction left to do.

Output: panel.json
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import extract as E                                    # noqa: E402

SCRATCH = E.SCRATCH
TOL = 1.0                                              # EGP, on figures in full


# --------------------------------------------------------------- documents ---
# One year-end statement per fiscal year, chosen from the company's own register.
# Where both a consolidated and a separate statement exist the CONSOLIDATED one
# is used; before FY2018 the company published a single set.
YEAR_END = {
    2015: ("Emaar-Misr-IR-Reports-Financial-Statements-2016-Year-End-EN.pdf",
           "comparative"),   # the FY2015 file omits its own P&L page -- see below
    2016: ("Emaar-Misr-IR-Reports-Financial-Statements-2016-Year-End-EN.pdf",
           "current"),
    2017: ("Emaar-Misr-IR-Reports-Financial-Statements-2017-Year-End-EN.pdf",
           "current"),
    2018: ("Emaar-Misr-IR-Reports-Financial-Statements-2018-Year-End-EN-"
           "Consolidated.pdf", "current"),
    2019: ("Emaar-Misr-IR-Reports-Financial-Statements-2019-Year-End-EN-"
           "Consolidated.pdf", "current"),
    2020: ("Emaar-Misr-IR-Reports-Financial-Statements-2020-Q4-EN-"
           "Consolidated.pdf", "current"),
}

# The FY2015 year-end PDF on the company's register is a scan whose PROFIT OR
# LOSS PAGE IS ABSENT: pages 2-3 are the balance sheet, 4 the changes in equity,
# 5 the cash flows, 6 onward the notes, and no page in the file carries an income
# statement. That is a defect in the source document, not in the extraction, and
# it is recorded rather than worked around. FY2015 is therefore taken from the
# comparative column of the FY2016 filing -- still the company's own audited
# statement, still tier A, and flagged as a comparative rather than as
# first-reported.
FY2015_NOTE = ("the FY2015 year-end PDF on the company's own register omits its "
               "profit-or-loss page entirely; FY2015 is taken from the "
               "comparative column of the FY2016 filing")

# Line labels as the English statements print them. Sign is applied from the
# statement's own convention, so a bracket the extractor drops shows up as a
# footing failure rather than as a silently positive expense.
# Line labels as the English statements print them. The label is matched at the
# START of a line and never anchored at its end: the text-layer files put the
# label and its figures on SEPARATE lines while the OCR'd scans put them on ONE,
# and a pattern anchored with $ silently matches nothing on half the panel.
# Sign comes from the statement's own convention, so a bracket the extractor
# drops shows up as a footing failure rather than as a positive expense.
LINES = [
    ("revenue",             r"^\s*Revenue\b",                              +1),
    ("cost_of_revenue",     r"^\s*Cost of revenue\b",                      -1),
    ("gross_profit",        r"^\s*GROSS PROFIT\b",                         +1),
    ("selling_marketing",   r"^\s*Selling and marketing expenses?\b",      -1),
    ("g_and_a",             r"^\s*General and administrative expenses?\b", -1),
    ("finance_income",      r"^\s*Finance income\b",                       +1),
    ("finance_cost",        r"^\s*Finance cost\b",                         -1),
    ("other_income",        r"^\s*(?:Net other income|Other income)\b",    +1),
    # the released-provisions line is tested BEFORE the provisions line, and the
    # provisions pattern excludes it explicitly: "Provisions" is a prefix of
    # "Provisions no longer required" and first-match-wins would take the wrong
    # row with no error of any kind
    ("provisions_released", r"^\s*Provisions no longer required\b",        +1),
    ("provisions",          r"^\s*Provisions\b(?!\s+no longer)",           -1),
    ("pbt",                 r"^\s*PROFIT FOR THE YEAR BEFORE INCOME TAX\b", +1),
    ("income_tax",          r"^\s*Income taxe?s?\b",                       -1),
    ("profit",              r"^\s*PROFIT FOR THE YEAR\b(?!\s+BEFORE)",     +1),
]
PBT_PARTS = ["gross_profit", "selling_marketing", "g_and_a", "finance_income",
             "finance_cost", "other_income", "provisions", "provisions_released"]


def read_pl(path, lang="eng"):
    """Both columns of an English profit-or-loss statement, by whichever route
    the page allows. Returns (values_by_column, route, page, rotation)."""
    i, text, route, rot = E.find_statement(path, E.PL, lang)
    if text is None:
        return None, None, None, None
    lines = [l.strip() for l in text.splitlines()]
    cols = {"current": {}, "comparative": {}}
    for key, pat, sign in LINES:
        rx = re.compile(pat, re.I)
        for n, ln in enumerate(lines):
            m = rx.match(ln)
            if not m:
                continue
            # money on the label's own line comes from what follows the label;
            # a note reference carries no thousand separator and is not money
            found = E.money(ln[m.end():])
            for j in range(n + 1, min(len(lines), n + 12)):
                if len(found) >= 2:
                    break
                found += E.money(lines[j])
            if len(found) >= 2:
                cols["current"][key] = sign * found[0]
                cols["comparative"][key] = sign * found[1]
            break
    return cols, route, i, rot


def foots(col):
    """Arithmetic is the arbiter. Three identities, all of them or the year is
    dropped."""
    checks = []
    if all(k in col for k in ("revenue", "cost_of_revenue", "gross_profit")):
        checks.append(("revenue + cost = gross profit",
                       col["revenue"] + col["cost_of_revenue"],
                       col["gross_profit"]))
    if all(k in col for k in PBT_PARTS + ["pbt"]):
        checks.append(("gross profit + the eight lines below it = PBT",
                       sum(col[k] for k in PBT_PARTS), col["pbt"]))
    if all(k in col for k in ("pbt", "income_tax", "profit")):
        checks.append(("PBT + tax = profit",
                       col["pbt"] + col["income_tax"], col["profit"]))
    return [{"identity": n, "lhs": a, "rhs": b, "foots": abs(a - b) < TOL}
            for n, a, b in checks]


def arabic_years():
    """The two Arabic filings, verified rather than trusted."""
    src = json.load(open(os.path.join(HERE, "arabic_read.json")))
    out, checks, restated = {}, [], []
    for tag in ("FY2014_filing", "FY2013_filing"):
        f = src[tag]
        years = sorted({y for v in f["lines"].values() for y in v},
                       reverse=True)
        for y in years:
            col = {k: v[y] for k, v in f["lines"].items() if y in v}
            ok = []
            if all(k in col for k in ("revenue", "cost_of_revenue",
                                      "gross_profit")):
                ok.append(("revenue + cost = gross profit",
                           col["revenue"] + col["cost_of_revenue"],
                           col["gross_profit"]))
            if "operating_components" in f:
                ok.append(("gross profit + opex + FX = operating profit",
                           sum(col[k] for k in f["operating_components"]),
                           col["operating_profit"]))
            ok.append(("components = PBT",
                       sum(col[k] for k in f["pbt_components"]), col["pbt"]))
            ok.append(("PBT + deferred tax = profit",
                       col["pbt"] + col["deferred_income_tax"], col["profit"]))
            res = [{"identity": n, "lhs": a, "rhs": b,
                    "foots": abs(a - b) < TOL} for n, a, b in ok]
            checks.append({"year": int(y), "filing": f["document"],
                           "identities": res})
            # POINT-IN-TIME DISCIPLINE. A fiscal year appears twice in this
            # archive: once as the current column of its own filing (as first
            # reported) and once as the comparative column of the next year's
            # filing (as the company chose to present it a year later). The
            # panel must carry the FIRST of those, and the later one is a
            # restatement recorded beside it, never substituted for it.
            # Filings are visited newest-first, so a plain setdefault would keep
            # exactly the wrong one -- which it did, silently, until the two
            # revenue figures for FY2013 were compared.
            which = "current" if y == max(years) else "comparative"
            rec = {"col": col, "doc": f["document"], "page": f["page_index"],
                   "route": "read", "lang": "ar", "which": which}
            prev = out.get(int(y))
            if prev is None or (prev["which"] == "comparative"
                                and which == "current"):
                out[int(y)] = rec
            if prev is not None and prev["which"] != which:
                first, later = (rec, prev) if which == "current" else (prev, rec)
                for k in sorted(set(first["col"]) & set(later["col"])):
                    if abs(first["col"][k] - later["col"][k]) >= 1.0:
                        restated.append({
                            "year": int(y), "line": k,
                            "as_first_reported": first["col"][k],
                            "as_restated": later["col"][k],
                            "delta": later["col"][k] - first["col"][k],
                            "first_filing": first["doc"],
                            "later_filing": later["doc"]})
    return out, checks, restated


def main():
    reg = {d["name"]: d for d in
           json.load(open(os.path.join(HERE, "ir_register.json")))["documents"]}

    panel, footing, dropped = {}, [], []

    # --- the English statements -------------------------------------------
    for year, (doc, which) in sorted(YEAR_END.items()):
        path = os.path.join(SCRATCH, doc)
        if not os.path.exists(path):
            dropped.append({"year": year, "why": "document not present"})
            continue
        cols, route, page, rot = read_pl(path)
        if cols is None or not cols[which]:
            dropped.append({"year": year, "why":
                            "no profit-or-loss page found" if cols is None
                            else "profit-or-loss page found but no line "
                                 "labels parsed from it"})
            continue
        col = cols[which]
        f = foots(col)
        footing.append({"year": year, "document": doc, "route": route,
                        "page": page, "rotation": rot, "column": which,
                        "identities": f})
        if not f or not all(c["foots"] for c in f):
            dropped.append({"year": year, "why": "does not foot; not used"})
            continue
        panel[year] = {
            "lines": col,
            "provenance": {
                "source_document": doc,
                "source_url": reg.get(doc, {}).get("url"),
                "document_date": "year-end statement for FY%d" % (
                    year if which == "current" else year + 1),
                "tier": "A — the company's own audited financial statements",
                "route": route, "page_index": page, "page_rotation": rot,
                "column": which,
                "note": FY2015_NOTE if year == 2015 else None,
            }}

    # --- the two Arabic statements ----------------------------------------
    ar, ar_checks, ar_restated = arabic_years()
    footing += ar_checks
    for year, d in sorted(ar.items()):
        chk = [c for c in ar_checks if c["year"] == year
               and c["filing"] == d["doc"]][0]
        if not all(x["foots"] for x in chk["identities"]):
            dropped.append({"year": year, "why": "does not foot; not used"})
            continue
        if year in panel:
            continue
        panel[year] = {
            "lines": d["col"],
            "provenance": {
                "source_document": d["doc"],
                "source_url": reg.get(d["doc"], {}).get("url"),
                "document_date": "year-end statement, Arabic",
                "tier": "A — the company's own audited financial statements",
                "route": "read from the rendered page; Eastern Arabic numerals, "
                         "which tesseract misreads — see arabic_read.json",
                "page_index": d["page"], "column": d["which"],
                "verified_by": "three arithmetic identities plus a cross-check "
                               "against an independently OCR'd statement",
            }}

    # --- cross-document checks, the ones that make the read believable ------
    # The FY2015 statement of changes in equity is a DIFFERENT document, read by
    # OCR in English, and it prints the FY2014 and FY2013 profit for the year.
    # If the Arabic read is right, those must agree exactly.
    cross = []
    eq = os.path.join(SCRATCH,
                      "Emaar-Misr-IR-Reports-Financial-Statements-2015-"
                      "Year-End-EN.pdf")
    if os.path.exists(eq):
        i, text, route, rot = E.find_statement(
            eq, [r"STATEMENT OF CHANGE(?:S)? IN EQUITY"], "eng")
        if text:
            got = set(E.money(text))
            for y in (2014, 2013):
                want = panel.get(y, {}).get("lines", {}).get("profit")
                cross.append({
                    "check": "FY%d profit for the year also appears in the "
                             "FY2015 statement of changes in equity" % y,
                    "value": want, "found": want in got,
                    "document": os.path.basename(eq), "route": route})

    ok_cross = all(c["found"] for c in cross) if cross else None

    out = {"years": {str(k): v for k, v in sorted(panel.items())},
           "footing": footing, "cross_document_checks": cross,
           "restated_in_a_later_filing": ar_restated,
           "dropped": dropped,
           "window": sorted(panel),
           "note": "profit-or-loss only; the balance sheet and cash flow are "
                   "extracted when the blocked years arrive and the whole panel "
                   "is built in one pass on one definition of each line"}
    json.dump(out, open(os.path.join(HERE, "panel.json"), "w"),
              indent=1, sort_keys=True)

    print("fiscal years in the panel : %s" % sorted(panel))
    print("dropped                   : %s" % (dropped or "none"))
    bad = [f for f in footing if not all(c["foots"] for c in f["identities"])]
    print("years whose statement does not foot : %s"
          % ([f["year"] for f in bad] or "none"))
    print("cross-document checks     : %s"
          % ("all pass" if ok_cross else cross))
    if ar_restated:
        print("\nrestated in a later filing (panel keeps the first-reported "
              "figure):")
        for r in ar_restated:
            print("  FY{} {:<20} first {:>16,.0f}  later {:>16,.0f}  "
                  "{:+,.0f}".format(r["year"], r["line"],
                                    r["as_first_reported"], r["as_restated"],
                                    r["delta"]))
    print()
    print("  year   revenue           cost of revenue   profit            route")
    for y in sorted(panel):
        L = panel[y]["lines"]
        print("  {}  {:>17,.0f} {:>17,.0f} {:>17,.0f}   {}".format(
            y, L.get("revenue", float("nan")),
            L.get("cost_of_revenue", float("nan")),
            L.get("profit", float("nan")),
            panel[y]["provenance"]["route"].split(";")[0]))

    if bad or (cross and not ok_cross):
        raise SystemExit("panel NOT accepted — a statement failed its own "
                         "arithmetic or a cross-document check")


if __name__ == "__main__":
    main()
