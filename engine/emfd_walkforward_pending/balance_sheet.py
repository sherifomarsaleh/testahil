#!/usr/bin/env python3
"""EMFD — the balance-sheet panel, gated on the statement's own subtotals.

The profit-or-loss panel (panel.py) carries the lines the income statement
publishes. Three of the pre-registered drivers need the balance sheet instead:

  D7  finance income — built on the assets that ACTUALLY EARN IT (cash, time
      deposits and interest-bearing receivables), never on a broader total.
      [R-FCAL-01] trap (i), applied to the asset side.
  D8  finance cost   — built on INTEREST-BEARING BORROWINGS, and left undefined
      where the filing discloses none.
  D9  D&A            — a PP&E roll-forward.
  D12 working capital— receivables, development properties, advances from
      customers, payables.

Every balance sheet in this archive is an image, including the ones inside files
whose profit-or-loss page carries a text layer, so all of it comes by OCR. OCR
of a wide two-column statement drops separators — one page renders
"9,268,434,113" as "9 268,434,113" and another renders "26,641,389,960" as
"26,64 1,389,960" — and neither looks broken. So nothing here is accepted on the
extractor's say-so: every subtotal the statement prints is re-derived from the
components printed above it, and a year that fails is re-read at higher
resolution and then DROPPED if it still fails. Arithmetic is the arbiter.

Output: balance_sheet.json
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import extract as E                                    # noqa: E402

TOL = 1.0

# THE SEPARATOR IS A COMMA, NEVER A SPACE. Allowing a space to stand in for a
# thousands separator looks like tolerance and is in fact greed: on a two-column
# statement it runs straight through the gap between the columns and returns one
# twenty-digit number made of both years. That is a wrong answer with no error,
# and it is what the first draft of this file did -- "Fixed assets under
# construction 5 974,670,923 958,519,586" came back as 5,974,670,923,958,519,808.
MONEY = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?")

# OCR does drop whitespace around a comma INSIDE a number ("2,743 ,482,268",
# "2, 148,856,278", "4,990, 167,462"). That is repaired first, because it is
# unambiguous: a comma with digits on both sides is a separator wherever the
# spaces fell. A comma the scan lost entirely ("9 268,434,113") is NOT repaired
# by guesswork -- the page is re-read at higher resolution instead, and the
# identity check below decides whether the re-read worked.
SPACED_COMMA = re.compile(r"(?<=\d)\s*,\s*(?=\d)")


# A NIL COLUMN IS PRINTED AS A DASH, AND A DASH IS DATA. Reading a row as "the
# first two money figures after the label" silently shifts the comparative into
# the current column whenever the current year is nil -- which is exactly what
# FY2020's non-current credit facilities are ("Credit facilities 13 - 10,255,590",
# nil in 2020 against 10.3m in 2019). That row is D8's own base, so the error
# would have landed in the borrowing rate.
# The dash must be FREE-STANDING. "Deferred tax assets : 30.— 309,830,931"
# carries an em-dash glued to the note reference, and reading that as a nil cell
# put a zero where a 310m deferred tax asset belongs -- caught by the
# non-current subtotal, not by anything about the text looking wrong.
CELL = re.compile(r"(?P<n>\d{1,3}(?:,\d{3})+(?:\.\d+)?)"
                  r"|(?:(?<=\s)|^)(?P<d>[-–—])(?=\s|$)")


def cells(s):
    """The row's value cells, in order: a money figure, or 0.0 for a printed
    dash. A bare note reference carries no separator and is neither."""
    return [0.0 if m.group("d") else float(m.group("n").replace(",", ""))
            for m in CELL.finditer(SPACED_COMMA.sub(",", s))]


def money(s):
    return [float(m.group(0).replace(",", ""))
            for m in MONEY.finditer(SPACED_COMMA.sub(",", s))]


# label key -> pattern. Matched at the start of a line; the value is the first
# money figure after the label on that line, then on the lines below it.
LINES = [
    ("fixed_assets",              r"Fixed assets\b(?!\s+under)"),
    ("fixed_assets_under_constr", r"Fixed assets under construction\b"),
    ("investment_properties",     r"Investment propert"),
    ("deferred_tax_assets",       r"Deferred tax assets?\b"),
    ("total_non_current_assets",  r"Total non[- ]current assets\b"),
    ("development_properties",    r"Development propert"),
    ("investments",               r"(?:Held to maturity investments|"
                                  r"Investments? (?:held|at))"),
    ("accounts_notes_receivable", r"Accounts and notes receivabl"),
    ("due_from_related",          r"Due from related part"),
    ("prepayments_other_recv",    r"Prepayments,? other receivables"),
    ("cash",                      r"Cash on hand and at bank"),
    ("total_current_assets",      r"Total current assets\b"),
    ("total_assets",              r"TOTAL ASSETS\b"),
    ("share_capital",             r"Share capital\b"),
    ("legal_reserve",             r"Legal reserve\b"),
    ("retained_earnings",         r"Retained earnings\b"),
    ("total_equity",              r"Total equity\b(?!\s+of)"),
    ("credit_facilities",         r"Credit facilities\b"),
    ("long_term_liabilities",     r"Long term liabilities\b"),
    ("eosb_provision",            r"Provision for employees"),
    ("total_non_current_liab",    r"Total non[- ]current liabilities\b"),
    ("provisions_liab",           r"Provisions\b"),
    ("trade_payables",            r"Trade payables"),
    ("due_to_related",            r"Due to related part"),
    ("income_tax_payable",        r"Income tax payable\b"),
    ("advances_from_customers",   r"Advances from customers\b"),
    ("retentions_payable",        r"Retentions payable\b"),
    # OCR mangles the two all-caps totals badly enough that they are matched
    # loosely ("Totalgurrent Habilitic", "TOTAL GIABILTIES"); they are used only
    # as identity targets, never as data
    ("total_current_liabilities", r"Total\s*\S*urrent\s*\S*abilit"),
    ("borrowings_related",        r"Borrowings? from related part"),
    ("current_portion_ltl",       r"Current portion of long term liabilit"),
]

# Two labels appear in BOTH the non-current and the current block, and the first
# match wins would take the wrong one. The section is tracked as the statement is
# walked and those keys are qualified by it.
SECTIONS = [
    (r"^\s*Non[- ]current assets\b",      "nca"),
    (r"^\s*Current assets\b",             "ca"),
    (r"^\s*EQUITY AND LIABILITIES\b|^\s*Equity\s*$", "eq"),
    (r"^\s*Non[- ]current liabilities\b", "ncl"),
    (r"^\s*Current liabilities\b",        "cl"),
]
QUALIFY = {"credit_facilities", "provisions_liab"}

# Subtotal identities the statement itself prints. Each is re-derived; a year is
# accepted only if every identity it can form closes.
IDENTITIES = [
    ("total non-current assets", "total_non_current_assets",
     ["fixed_assets", "fixed_assets_under_constr", "investment_properties",
      "deferred_tax_assets"]),
    ("total current assets", "total_current_assets",
     ["development_properties", "investments", "accounts_notes_receivable",
      "due_from_related", "prepayments_other_recv", "cash"]),
    ("total assets", "total_assets",
     ["total_non_current_assets", "total_current_assets"]),
    ("total current liabilities", "total_current_liabilities",
     ["provisions_liab_cl", "trade_payables", "due_to_related",
      "income_tax_payable", "advances_from_customers", "retentions_payable",
      "credit_facilities_cl", "borrowings_related", "current_portion_ltl"]),
    ("total non-current liabilities", "total_non_current_liab",
     ["credit_facilities_ncl", "long_term_liabilities", "eosb_provision"]),
    ("assets = equity + liabilities", "total_assets",
     ["total_equity", "total_non_current_liab", "total_current_liabilities"]),
]


def locate(path, lang="eng"):
    """Find the balance-sheet page ONCE, at the cheap resolution."""
    i, text, route, rot = E.find_statement(path, E.BS, lang, min_money=12)
    return i, route, rot


def read_bs(path, page_index, lang="eng", dpi=300):
    """Parse the balance sheet from one known page at one resolution.

    The page is located once and only re-read here, because re-running the page
    SEARCH at 600 dpi means OCR'ing a dozen pages four ways to find one -- a
    minute of work per page for a page whose index is already known.
    """
    text, route, rot = E.page(path, page_index, lang, dpi=dpi)
    if not text:
        return None, None, None
    lines = [l.strip() for l in text.splitlines()]
    secs = [(re.compile(p, re.I), tag) for p, tag in SECTIONS]
    rxs = [(k, re.compile(r"^\s*" + p, re.I)) for k, p in LINES]

    cols, section = {"current": {}, "comparative": {}}, None
    for n, ln in enumerate(lines):
        for rx, tag in secs:
            if rx.match(ln):
                section = tag
                break
        for key, rx in rxs:
            m = rx.match(ln)
            if not m:
                continue
            k = "%s_%s" % (key, section) if key in QUALIFY and section else key
            if k in cols["current"]:
                break                       # first occurrence in a section wins
            found = cells(ln[m.end():])
            for j in range(n + 1, min(len(lines), n + 4)):
                if len(found) >= 2:
                    break
                found += cells(lines[j])
            if len(found) >= 2:
                cols["current"][k] = found[0]
                cols["comparative"][k] = found[1]
            break
    return cols, route, rot


def check(col):
    out = []
    for name, total, parts in IDENTITIES:
        if total in col and all(p in col for p in parts):
            lhs = sum(col[p] for p in parts)
            out.append({"identity": name, "derived": lhs, "printed": col[total],
                        "foots": abs(lhs - col[total]) < TOL})
    return out


FILES = {
    2016: "Emaar-Misr-IR-Reports-Financial-Statements-2016-Year-End-EN.pdf",
    2017: "Emaar-Misr-IR-Reports-Financial-Statements-2017-Year-End-EN.pdf",
    2018: "Emaar-Misr-IR-Reports-Financial-Statements-2018-Year-End-EN-"
          "Consolidated.pdf",
    2019: "Emaar-Misr-IR-Reports-Financial-Statements-2019-Year-End-EN-"
          "Consolidated.pdf",
    2020: "Emaar-Misr-IR-Reports-Financial-Statements-2020-Q4-EN-"
          "Consolidated.pdf",
}


def main():
    reg = {d["name"]: d for d in
           json.load(open(os.path.join(HERE, "ir_register.json")))["documents"]}
    panel, checks, dropped = {}, [], []

    for year, doc in sorted(FILES.items()):
        path = os.path.join(E.SCRATCH, doc)
        if not os.path.exists(path):
            dropped.append({"year": year, "why": "document not present"})
            continue
        # Escalate resolution until the statement's own subtotals close. A
        # dropped comma at 300 dpi is usually there at 450; if it is still
        # missing at 600 the year is dropped rather than guessed at.
        pg, route, rot = locate(path)
        if pg is None:
            dropped.append({"year": year, "why": "no balance-sheet page found"})
            continue
        cols = res = None
        used_dpi = 300
        for dpi in (300, 450, 600):
            c, route, rot = read_bs(path, pg, dpi=dpi)
            if c is None or not c["current"]:
                continue
            r = check(c["current"])
            if cols is None or (r and all(x["foots"] for x in r)):
                cols, res, used_dpi = c, r, dpi
            if r and all(x["foots"] for x in r):
                break
        if cols is None or not cols["current"]:
            dropped.append({"year": year, "why": "no balance-sheet page parsed"})
            continue
        checks.append({"year": year, "document": doc, "route": route,
                       "page": pg, "rotation": rot, "dpi": used_dpi,
                       "identities": res})
        if not res or not all(c["foots"] for c in res):
            dropped.append({"year": year,
                            "why": "subtotals do not re-derive from the "
                                   "components printed above them; not used",
                            "failed": [c["identity"] for c in res
                                       if not c["foots"]]})
            continue
        panel[year] = {
            "lines": cols["current"],
            "provenance": {
                "source_document": doc,
                "source_url": reg.get(doc, {}).get("url"),
                "tier": "A — the company's own audited financial statements",
                "route": route, "page_index": pg, "page_rotation": rot,
                "ocr_dpi": used_dpi, "column": "current",
            }}

    # --- what the drivers actually need, derived and labelled --------------
    derived = {}
    for y, d in sorted(panel.items()):
        L = d["lines"]
        earning = [k for k in ("cash", "investments",
                               "accounts_notes_receivable") if k in L]
        derived[y] = {
            "interest_earning_asset_base": {
                "value": sum(L[k] for k in earning),
                "DERIVED": " + ".join(earning),
                "why": "D7's base is the assets that actually earn the finance "
                       "income. Total assets and total current assets are NOT "
                       "used: development properties and prepayments earn "
                       "nothing, and dividing finance income by a base that "
                       "does not earn it manufactures a rate.",
            },
            "interest_bearing_borrowings": {
                "value": sum(L[k] for k in
                             ("credit_facilities_ncl", "credit_facilities_cl",
                              "long_term_liabilities", "current_portion_ltl",
                              "borrowings_related") if k in L),
                "DERIVED": "credit facilities (both blocks) + long term "
                           "liabilities + its current portion + borrowings "
                           "from related parties",
                "why": "D8's base. Advances from customers, trade payables and "
                       "retentions bear no interest and are excluded — that "
                       "exclusion is the whole point of the rule.",
            },
            "advances_from_customers": {
                "value": L.get("advances_from_customers"),
                "DERIVED": None,
                "why": "the contract-liability side of D5's backlog roll (L-103)",
            },
        }

    # --- specification check on the two financing rules --------------------
    # NOT a forecast error and NOT a finding about the company: this asks only
    # whether the rules the pre-registration fixed in advance are computable on
    # this name's own disclosure. D7's rate should land somewhere a deposit rate
    # could plausibly be; D8's should be refused, because the pre-registration
    # says it is undefined where the filing discloses no material
    # interest-bearing borrowings, and refusing it is the point.
    rate = []
    pl = {}
    pj = os.path.join(HERE, "panel.json")
    if os.path.exists(pj):
        pl = {int(y): v["lines"] for y, v in
              json.load(open(pj))["years"].items()}
    for y in sorted(panel):
        if y - 1 not in derived or y not in pl:
            continue
        base = derived[y - 1]["interest_earning_asset_base"]["value"]
        debt = derived[y - 1]["interest_bearing_borrowings"]["value"]
        fi = pl[y].get("finance_income")
        fc = pl[y].get("finance_cost")
        row = {"year": y,
               "opening_earning_assets": base,
               "finance_income": fi,
               "implied_earning_rate": (fi / base) if fi and base else None,
               "opening_interest_bearing_borrowings": debt,
               "finance_cost": fc,
               "implied_borrowing_rate": (abs(fc) / debt) if fc and debt else None}
        # THE PRE-REGISTERED REFUSAL, APPLIED — and deliberately not turned
        # into a threshold. A rate above 100% is arithmetically impossible and
        # can be rejected here with nothing sourced. A rate of 1-3% is just as
        # certainly not a borrowing rate for an Egyptian corporate — the cost of
        # capital rule says a same-currency corporate cannot borrow below its
        # own sovereign — but adjudicating THAT needs the sovereign yield at
        # each origin, which is a Country-ring input this run has not sourced.
        # Inventing a cutoff to stand in for it would be a free parameter with
        # no evidence behind it, which the promotion rule forbids, so the
        # verdict says what it is waiting for instead of guessing.
        r = row["implied_borrowing_rate"]
        row["verdict"] = (
            "no borrowings disclosed — rate undefined, line carries TTM3"
            if not debt else
            "NOT IDENTIFIED — implied rate is arithmetically impossible"
            if r is not None and r >= 1.0 else
            "pending — needs the Egyptian sovereign yield at this origin to "
            "test the floor (a corporate cannot borrow below its sovereign)")
        rate.append(row)

    out = {"years": {str(k): v for k, v in sorted(panel.items())},
           "identity_checks": checks, "dropped": dropped,
           "driver_bases": {str(k): v for k, v in sorted(derived.items())},
           "financing_rule_specification_check": rate}
    json.dump(out, open(os.path.join(HERE, "balance_sheet.json"), "w"),
              indent=1, sort_keys=True)

    print("balance sheets accepted : %s" % sorted(panel))
    print("dropped                 : %s" % (dropped or "none"))
    print()
    print("  year   total assets        earning assets      borrowings        "
          "advances from customers")
    for y in sorted(panel):
        d = derived[y]
        print("  {}  {:>17,.0f} {:>19,.0f} {:>17,.0f} {:>22,.0f}".format(
            y, panel[y]["lines"].get("total_assets", float("nan")),
            d["interest_earning_asset_base"]["value"],
            d["interest_bearing_borrowings"]["value"],
            d["advances_from_customers"]["value"] or float("nan")))
    if rate:
        print("\n  specification check on the two financing rules "
              "(NOT a forecast error, NOT a finding about the company):")
        print("  year   D7 implied rate on opening earning assets    "
              "D8 implied rate on opening borrowings")
        for r in rate:
            print("  {}   {:>12}                                {:>14}  {}"
                  .format(r["year"],
                          "{:.1%}".format(r["implied_earning_rate"])
                          if r["implied_earning_rate"] else "—",
                          "{:.0%}".format(r["implied_borrowing_rate"])
                          if r["implied_borrowing_rate"] else "—",
                          r["verdict"]))

    if dropped:
        raise SystemExit("some years dropped — see balance_sheet.json")


if __name__ == "__main__":
    main()
