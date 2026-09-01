"""TMGH walk-forward — the operating drivers, read out of the company's prose.

New sales, units sold, units delivered and backlog are the drivers a developer
is actually forecast on, and TMG publishes them in the narrative of its results
releases rather than in a table. Prose is a worse source than a statement and
is treated as one: every candidate is emitted WITH THE SENTENCE IT CAME FROM,
so each figure can be read against its own context before it enters the panel,
and a figure whose sentence does not support it is dropped rather than kept.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import parse_fs as P

MULT = {"bn": 1000.0, "billion": 1000.0, "mn": 1.0, "million": 1.0}


def _egp(numtxt, unit):
    return float(numtxt.replace(",", "")) * MULT[unit.lower().rstrip(".")]


PATTERNS = {
    # value of contracted (gross) sales in the period
    "new_sales_value": [
        # the 2011-2017 releases' standing sentence, which states the period
        re.compile(r"new sales of real estate units[^.]{0,60}?amounted to\s+"
                   r"EGP\s?([\d,]+(?:\.\d+)?)\s*(bn|billion|mn|million)", re.I),
        re.compile(r"EGP\s?([\d,]+(?:\.\d+)?)\s*(BN|bn|billion|mn|million)\s+"
                   r"(?:of|in)\s+new sales value", re.I),
        re.compile(r"(?:new|net|contracted|gross)\s+sales[^.]{0,60}?"
                   r"EGP\s?([\d,]+(?:\.\d+)?)\s*(bn|billion|mn|million)", re.I),
        re.compile(r"EGP\s?([\d,]+(?:\.\d+)?)\s*(bn|billion|mn|million)[^.]{0,40}?"
                   r"(?:in\s+)?(?:new|net|contracted)\s+sales", re.I),
    ],
    "units_sold": [
        re.compile(r"(?:representing|comprising|totall?ing|of)\s+(?:some\s+|c\.\s*)?"
                   r"([\d,]{3,7})\s+units", re.I),
        re.compile(r"([\d,]{3,7})\s+units\s+(?:were\s+)?sold", re.I),
    ],
    "units_delivered": [
        re.compile(r"deliver\w*\s+(?:some\s+|c\.\s*)?([\d,]{3,7})\s+"
                   r"(?:residential|non-residential|units)", re.I),
        re.compile(r"deliver\w*\s+(?:of\s+|some\s+)?([\d,]{3,7})\s+"
                   r"(?:residential|units|non-residential)", re.I),
        re.compile(r"([\d,]{3,7})\s+units\s+(?:were\s+)?deliver", re.I),
        re.compile(r"([\d,]{3,7})\s+(?:residential\s+and\s+non-residential\s+)?units?\s+"
                   r"deliver\w*", re.I),
    ],
    "backlog": [
        re.compile(r"backlog[^.]{0,80}?EGP\s?([\d,]+(?:\.\d+)?)\s*(bn|billion|mn|million)", re.I),
        re.compile(r"EGP\s?([\d,]+(?:\.\d+)?)\s*(bn|billion|mn|million)[^.]{0,40}?backlog", re.I),
    ],
    "landbank_msqm": [
        re.compile(r"([\d,]+(?:\.\d+)?)\s*(?:mn|million)\s*sqm[^.]{0,30}land", re.I),
        re.compile(r"land\s?bank[^.]{0,50}?([\d,]+(?:\.\d+)?)\s*(?:mn|million)\s*sqm", re.I),
    ],
}


def sentence_at(text, i, span=240):
    lo = max(0, i - span)
    hi = min(len(text), i + span)
    s = re.sub(r"\s+", " ", text[lo:hi]).strip()
    return s


def scan(name, period):
    text = P.load(name)
    out = []
    for field, pats in PATTERNS.items():
        for pat in pats:
            for m in pat.finditer(text):
                g = m.groups()
                if field in ("new_sales_value", "backlog"):
                    v = _egp(g[0], g[1])
                elif field == "landbank_msqm":
                    v = float(g[0].replace(",", ""))
                else:
                    v = float(g[0].replace(",", ""))
                    if v < 100:
                        continue          # a stray small count is not a unit total
                pg, route = P.page_of(text, m.start())
                out.append({"field": field, "value": v, "doc": name,
                            "period": period, "page": pg, "route": route,
                            "match": re.sub(r"\s+", " ", m.group(0))[:120],
                            "sentence": sentence_at(text, m.start())})
    return out


def main():
    reg = json.load(open(os.path.join(HERE, "ir_register.json")))
    rows = []
    for r in reg:
        if r["kind"] not in ("earnings_release", "market_update", "ir_presentation"):
            continue
        if r.get("fetched") not in ("ok", "cached"):
            continue
        base = re.sub(r"[^A-Za-z0-9._-]+", "_", r["name"])[:150][:-4]
        if not os.path.exists(os.path.join(P.TEXT, base + ".txt")):
            continue
        rows += scan(base, r["period"])
    json.dump(rows, open(os.path.join(HERE, "kpi_candidates.json"), "w"), indent=1)
    by = {}
    for r in rows:
        by[r["field"]] = by.get(r["field"], 0) + 1
    print("%d candidates: %s" % (len(rows), by))


if __name__ == "__main__":
    main()
