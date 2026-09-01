"""Print, for every annual ARCC filing, the three pages the panel is built from:
the profit-and-loss statement, the revenue note and the cost-of-sales note.

Reading aid only — it decides nothing.  `panel.py` carries the figures with a
source and a page and FOOTS them, and where the footing refuses the page is
re-read.  This exists because the alternative, a parser that guesses which OCR
token was meant, would silently repair the very errors the footing is there to
find: on the FY2016 filing OCR turned a leading 1 into a 2 in three separate
places (income tax 124,683,515 -> 224,683,515; raw materials 1,257,697,536 ->
2,257,697,536; the cost-of-sales total with it), and each one is visible ONLY
because a printed subtotal refused to agree with its parts.
"""
import os, re, sys
import parse_fs as P

# Every annual consolidated filing held, with the fiscal year it REPORTS and
# the fiscal year it carries as a COMPARATIVE.  Both columns enter the panel:
# the comparative is how FY2014 is sourced at all, and it is the only route to
# the earliest year in the window.
ANNUAL = [
    ("ACC-2015-Consolidated-Financials-English",   "FY2015", "FY2014"),
    ("FY-2016-Consolidated-Financials-English",    "FY2016", "FY2015"),
    ("FY-2017-Consolidated-Financials-English",    "FY2017", "FY2016"),
    ("ARCC_FY_2018_Consolidated_Financials-English", "FY2018", "FY2017"),
    ("FY_2019_Consolidated_Financials-English",    "FY2019", "FY2018"),
    ("FY-2020-consolidated-financials-english",    "FY2020", "FY2019"),
    ("FY_2021_Consolidated_Financials-English",    "FY2021", "FY2020"),
    ("FY_2022_Consolidated_Financials-English",    "FY2022", "FY2021"),
    ("4Q2023_ACC_Consolidated_Financials",         "FY2023", "FY2022"),
    ("FY2024_Consolidated_Financials-English",     "FY2024", "FY2023"),
    ("FY-2025-Consolidated-Financials-English",    "FY2025", "FY2024"),
]
INTERIM = [
    ("Q1-2026-Consolidated-Financials-English", "Q1-2026", "Q1-2025"),
    ("2Q2026-Consolidated-Financials-English",  "H1-2026", "H1-2025"),
]

PL = re.compile(r"statement of profit", re.I)
REV = re.compile(r"(Local sales|Total Local Sales|Sales revenue|An analysis of the .{0,12}(Group|Company).{0,3}s revenue)", re.I)
COS = re.compile(r"Raw material", re.I)


def dump(doc, want, chars=2000):
    if not os.path.exists(os.path.join(P.TEXT, doc + ".txt")):
        print("!! %s  NOT EXTRACTED" % doc); return
    hits = 0
    for no, route, t in P.pages(doc):
        if want.search(t) and ("Cost of sales" in t or "Raw material" in t
                               or "Local sales" in t or "Sales (net)" in t
                               or "Sales revenue" in t):
            print("-" * 72)
            print("%s  page %d  route=%s" % (doc, no, route))
            print("-" * 72)
            print(t[:chars])
            hits += 1
            if hits >= 2:
                break
    if not hits:
        print("!! %s  no page matched %s" % (doc, want.pattern[:40]))


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    rows = ANNUAL + INTERIM
    if which != "all":
        rows = [r for r in rows if which in r[0] or which == r[1]]
    for doc, fy, comp in rows:
        print("\n" + "#" * 72)
        print("# %s   reports %s, comparative %s" % (doc, fy, comp))
        print("#" * 72)
        dump(doc, PL, 2200)
        dump(doc, COS, 1600)
