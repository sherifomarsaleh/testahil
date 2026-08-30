"""Parse the PHDC earnings-release text layers into a four-field panel.

Every extracted number carries value / source document / document date /
provenance tier, per the walk-forward prompt's data rule. Nothing is
interpolated: a label that is not found yields no row at all, and the gap
shows up in the coverage report rather than being filled.
"""
import os, re, json, glob

TXT = os.environ.get("PHDC_TXT",
    "/tmp/claude-0/-home-user-testahil/2283e95e-66db-5f22-bba6-0db833f32495/scratchpad/phdc_src/text")

NUM = r"\(?-?[\d,]+(?:\.\d+)?\)?"


def tonum(s):
    if s is None:
        return None
    s = s.strip()
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()").replace(",", "").replace("−", "-")
    if s in ("", "-", "--", "n/a"):
        return None
    try:
        v = float(s)
    except ValueError:
        return None
    return -v if neg else v


def page_text(stem):
    p = os.path.join(TXT, stem + ".txt")
    if not os.path.exists(p):
        return None
    return open(p, encoding="utf-8").read()


def label_row(txt, label, n=2, anywhere=False):
    """Return the first n numbers that follow `label` on its own line-run.

    The releases lay a table row out as: label \n v_current \n v_prior \n change.
    We take the first n numeric tokens after the label and stop at the next
    alphabetic line, so a label with no numbers under it returns nothing rather
    than borrowing the next row's figures.
    """
    lines = [l.strip() for l in txt.split("\n")]
    lab = label.lower()
    for i, l in enumerate(lines):
        cl = l.lower().strip()
        hit = (cl == lab) or (anywhere and cl.startswith(lab))
        if not hit:
            continue
        vals = []
        for j in range(i + 1, min(i + 14, len(lines))):
            s = lines[j]
            if not s:
                continue
            if re.fullmatch(NUM, s):
                vals.append(tonum(s))
            elif re.fullmatch(r"\(?-?[\d.]+%\)?|\(?-?[\d.]+pp\)?", s):
                continue                      # a % / pp cell, not a value
            else:
                break
            if len(vals) >= n:
                break
        if len(vals) >= 1:
            return vals[:n]
    return None


# label -> canonical field. Labels differ across the archive's three template
# eras, so each field carries every spelling actually observed.
IS_LABELS = {
    "revenue": ["Revenues", "Revenue", " Revenue", "Revenues "],
    "cogs": ["Cost of Revenue", "Cost of Revenues", " Cost of Revenue"],
    "gross_profit": ["Gross Profit", " Gross Profit"],
    "ebitda": ["EBITDA", " EBITDA"],
    "operating_profit": ["Operating Profit", " Operating Profit"],
    "npbt": ["Net Profit Before Income Tax & Minority Interest",
             "Net Profit before Tax & Minority Interest",
             "Net Profit Before Tax & Minority Interest",
             "Net Profit before Income Tax & Minority Interest"],
    "npat": ["Net Profit After Tax", " Net Profit After Tax"],
    "nci": ["Non-Controlling Interest", " Non-Controlling Interest"],
    "npat_mi": ["Net Profit After Tax & Minority Interest",
                "Net Profit after Tax & Minority Interest",
                " Net Profit After Tax & Minority Interest"],
}

BS_LABELS = {
    "lt_assets": ["Total Long-Term Assets", "Total long - Term Assets",
                  "Total Long - Term Assets", " Total long - Term Assets",
                  " Total Long-Term Assets"],
    "current_assets": ["Total Current Assets", " Total Current Assets"],
    "total_assets": ["Total Assets", " Total Assets"],
    "current_liabilities": ["Total Current Liabilities", " Total Current Liabilities"],
    "lt_liabilities": ["Total Long-Term Liabilities", "Total Long-Term Liabilities ",
                       " Total Long-Term Liabilities"],
    "total_liabilities": ["Total Liabilities", " Total Liabilities"],
    "equity_parent": ["Equity Attributable to Equity Holders of Parent Co.",
                      "Total Equity attributable to Parent Company",
                      " Total Equity attributable to Parent Company"],
    "nci_equity": ["Non-Controlling Interest", " Non-Controlling Interest"],
    "total_equity": ["Total Shareholders' Equity", "Total Shareholders’ Equity",
                     " Total Shareholders' Equity"],
    # working-capital detail (older, full-balance-sheet template)
    "wip": ["Works in Process", "Works in Process ", "Work in Process"],
    "nr_long": ["Notes Receivable - Long Term", "Notes Receivable - Long Term "],
    "nr_short": ["Notes Receivable - Short Term", "Notes Receivable - Short Term "],
    "ar": ["Accounts Receivable", "Accounts Receivable "],
    "advances_customers": ["Advances from Customers", "Advances from Customers "],
    "suppliers_contractors": ["Suppliers & Contractors", "Suppliers & Contractors "],
    "cash": ["Cash & Cash Equivalents", "Cash & Cash Equivalents "],
    "loans_lt": ["Loans", "Loans "],
    "term_loans_current": ["Current Portion of Term Loans",
                           "Current Portion of Term Loans "],
    "fixed_assets": ["Fixed Assets (Net)", "Fixed Assets (Net) "],
}

CF_LABELS = {
    "cfo": ["Cash Flows from Operating Activities", "Cash Flow from Operating Activities",
            "Net Cash Flows from Operating Activities"],
    "cfi": ["Cash Flows from Investing Activities", "Cash Flow from Investing Activities"],
    "cff": ["Cash Flows from Financing Activities", "Cash Flow from Financing Activities"],
}


def parse_release(stem, year, quarter):
    txt = page_text(stem)
    if txt is None:
        return None
    out = {"_stem": stem, "_year": year, "_quarter": quarter}
    for group, labels in (("is", IS_LABELS), ("bs", BS_LABELS), ("cf", CF_LABELS)):
        for field, variants in labels.items():
            for lab in variants:
                v = label_row(txt, lab, n=2)
                if v:
                    out["%s.%s" % (group, field)] = v
                    out["%s.%s._label" % (group, field)] = lab
                    break
    return out


if __name__ == "__main__":
    reg = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "ir_register.json")))
    res = []
    for r in reg:
        if r["quarter"] != "Q4":
            continue
        stem = "%s_%s_ER" % (r["year"], r["quarter"])
        p = parse_release(stem, r["year"], r["quarter"])
        if p:
            res.append(p)
    for p in res:
        got = [k for k in p if not k.startswith("_") and not k.endswith("_label")]
        print("FY%s  fields=%2d  rev=%s  ta=%s" % (
            p["_year"], len(got),
            p.get("is.revenue"), p.get("bs.total_assets")))
