#!/usr/bin/env python3
"""EMFD — extraction survey and footing check over the obtained documents.

[R-FCAL-01] §1: "ACCEPT A STATEMENT ONLY IF IT FOOTS AGAINST ITS OWN ARITHMETIC.
... a page that does not foot is re-read by OCR off the rendered pixels and the
route each figure came by is recorded — ARITHMETIC IS THE ARBITER, NOT THE
EXTRACTOR'S CONFIDENCE."

This does not build the panel. The walk-forward is blocked on §1 (see
SCOPE_DECISION_01-09-2026.md), so there is no panel to build yet. What it does
is establish, document by document and page by page, WHICH route each figure
would have to come by when the blocked years arrive:

  * text     — the page carries a text layer and the statement parses from it
  * image    — the page carries no text layer at all and needs OCR off pixels
  * mixed    — the file has a text layer but this particular statement does not

and, wherever a profit-or-loss statement did parse, whether it FOOTS. A file
that extracts cleanly and does not foot is the dangerous case the rule was
written about, so the check is run now rather than discovered mid-build.

Output: extraction_survey.json  (committed — it is the evidence for the claim
that the obtainable window is 2013-2020 plus H1-2021, and for the claim that
four of those eight years will need OCR).
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PDFS = os.environ.get(
    "EMFD_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/5c3bac54-80e7-5e98-82bb-8cfd0b2244dd"
    "/scratchpad/emfd_src/pdfs")

HEADINGS = {
    "profit_or_loss": re.compile(r"(?i)statement of profit or loss"),
    "financial_position": re.compile(r"(?i)statement of financial position"),
    "cash_flows": re.compile(r"(?i)statement of cash flows"),
    "changes_in_equity": re.compile(r"(?i)statement of changes in equity"),
}

# Money on these statements is printed in full EGP with thousand separators and
# negatives in parentheses. Nothing shorter than four digits is a money figure
# on these pages (note references are 1-37), so the guard is on length.
NUM = re.compile(r"\(?\s*(\d{1,3}(?:,\d{3})+(?:\.\d+)?)\s*\)?")


def numbers(line):
    out = []
    for m in NUM.finditer(line):
        v = float(m.group(1).replace(",", ""))
        neg = "(" in line[max(0, m.start() - 2):m.start() + 1] or \
              ")" in line[m.end() - 1:m.end() + 2]
        out.append(-v if neg else v)
    return out


def first_number_after(text, label_re, window=3):
    """The label and its figure are frequently on different lines in the text
    layer, so look at the label's line and the next few. Returns the FIRST money
    figure found, which on these statements is the current-year column."""
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if label_re.search(ln):
            for j in range(i, min(len(lines), i + window + 1)):
                ns = numbers(lines[j])
                if ns:
                    return ns[0]
    return None


LABELS = {
    "revenue": re.compile(r"^\s*revenue\s*$|^\s*revenue\s+\d", re.I),
    "cost_of_revenue": re.compile(r"(?i)cost of revenue"),
    "gross_profit": re.compile(r"(?i)gross profit"),
    "pbt": re.compile(r"(?i)profit .*before income tax"),
    "income_tax": re.compile(r"(?i)^\s*income tax"),
    "profit": re.compile(r"(?i)^\s*profit for the (year|period)\s*$"),
}


def survey_file(path):
    import pymupdf
    doc = pymupdf.open(path)
    pages = [doc[i].get_text() for i in range(doc.page_count)]
    has_any_text = any(p.strip() for p in pages)

    rec = {"file": os.path.basename(path), "pages": doc.page_count,
           "file_has_text_layer": has_any_text, "statements": {}}

    for key, rx in HEADINGS.items():
        hit = None
        for i, t in enumerate(pages):
            # The table of contents names every statement, so a page that only
            # lists them is not the statement. Require a money figure on it.
            if rx.search(t) and len(numbers(t)) >= 4:
                hit = i
                break
        if hit is None:
            rec["statements"][key] = {
                "route": "image" if not has_any_text else "mixed",
                "page": None,
                "note": ("no text layer anywhere in the file" if not has_any_text
                         else "file has a text layer but this statement does not")}
        else:
            rec["statements"][key] = {"route": "text", "page": hit}

    pl = rec["statements"]["profit_or_loss"]
    if pl["route"] == "text":
        t = pages[pl["page"]]
        vals = {k: first_number_after(t, rx) for k, rx in LABELS.items()}
        pl["values"] = vals
        checks = []
        if None not in (vals["revenue"], vals["cost_of_revenue"],
                        vals["gross_profit"]):
            lhs = vals["revenue"] - abs(vals["cost_of_revenue"])
            checks.append({"check": "revenue - cost = gross profit",
                           "lhs": lhs, "rhs": vals["gross_profit"],
                           "foots": abs(lhs - vals["gross_profit"]) < 1.0})
        if None not in (vals["pbt"], vals["income_tax"], vals["profit"]):
            lhs = vals["pbt"] - abs(vals["income_tax"])
            checks.append({"check": "PBT - income tax = profit",
                           "lhs": lhs, "rhs": vals["profit"],
                           "foots": abs(lhs - vals["profit"]) < 1.0})
        pl["footing"] = checks
        pl["foots"] = bool(checks) and all(c["foots"] for c in checks)
    return rec


def main():
    reg = json.load(open(os.path.join(HERE, "ir_register.json")))
    docs = [d for d in reg["documents"]
            if d["kind"] == "FS" and d.get("is_pdf")
            and d["basis"] in ("consolidated", "unspecified")]
    out = []
    for d in sorted(docs, key=lambda x: (x["year"], x["period"])):
        path = os.path.join(PDFS, d["name"])
        if not os.path.exists(path):
            continue
        r = survey_file(path)
        r.update(year=d["year"], period=d["period"], lang=d["lang"],
                 basis=d["basis"], url=d["url"], sha256=d["sha256"])
        out.append(r)

    years_text = sorted({r["year"] for r in out
                         if r["period"] in ("Q4", "Year-End")
                         and r["statements"]["profit_or_loss"]["route"] == "text"})
    years_ocr = sorted({r["year"] for r in out
                        if r["period"] in ("Q4", "Year-End")
                        and r["statements"]["profit_or_loss"]["route"] != "text"})
    footed = [r for r in out if r["statements"]["profit_or_loss"].get("foots")]
    failed = [r for r in out
              if r["statements"]["profit_or_loss"].get("foots") is False]

    doc = {"documents": out,
           "year_end_pl_from_text_layer": years_text,
           "year_end_pl_needing_ocr": years_ocr,
           "pl_statements_that_foot": len(footed),
           "pl_statements_that_do_not_foot": [r["file"] for r in failed]}
    with open(os.path.join(HERE, "extraction_survey.json"), "w") as f:
        json.dump(doc, f, indent=1, sort_keys=True)

    print("consolidated / unspecified-basis statements surveyed : %d" % len(out))
    print("year-end P&L readable from the text layer            : %s" % years_text)
    print("year-end P&L that will need OCR off the pixels       : %s" % years_ocr)
    print("P&L statements checked and footing                   : %d" % len(footed))
    print("P&L statements that extracted and did NOT foot       : %s"
          % ([r["file"] for r in failed] or "none"))


if __name__ == "__main__":
    main()
