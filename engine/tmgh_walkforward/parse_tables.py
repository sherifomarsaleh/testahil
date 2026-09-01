"""Read TMGH's income statement and balance sheet out of each primary document.

One document reports two periods — its own and the comparative — and the two
document families put them in OPPOSITE ORDER: the audited statements print
current then prior ("31 December 2024   31 December 2023"), the earnings
releases print prior then current ("FY2018   FY2019   Change"). The column
order is therefore READ OFF THE TABLE'S OWN HEADING, never assumed, and a
document whose heading cannot be read yields nothing rather than a guess.

Scale is read the same way: the statements report in LE (units), the releases
in EGP mn. Everything leaves here in EGP mn.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import parse_fs as P
import labels as L

YEAR_HDR = [
    (re.compile(r"31\s*[/ ]?\s*(?:December|12)\s*[/ ]?\s*(20\d\d)", re.I), "fs"),
    (re.compile(r"\bFY\s?(20\d\d)\b"), "er"),
    (re.compile(r"\b(20\d\d)\b"), "bare"),
]


def column_years(text, at, back=2600):
    """The two period columns a table declares, in the order it prints them.

    Read off the table's own heading, never assumed — the two document families
    print the same two periods in OPPOSITE order. The heading is taken from the
    SAME PAGE as the label and from the year pair CLOSEST to it: searching a
    wider window let a year mentioned in the surrounding prose stand in for a
    column heading, which silently mislabelled whole years of the panel.
    """
    lo = text.rfind("<<<PAGE", 0, at)
    head = text[max(lo, at - back) if lo >= 0 else max(0, at - back): at]
    for rx, kind in YEAR_HDR:
        yrs = rx.findall(head)
        if len(yrs) >= 2:
            a, b = int(yrs[-2]), int(yrs[-1])
            if a != b and abs(a - b) <= 3 and 2005 <= min(a, b) <= 2027:
                return [a, b], kind
    return None, None


NOTE = re.compile(r"^\(\w{1,3}\)$")


# A note reference is stripped by SHAPE before tokenising, not skipped by
# position afterwards. The positional rule handled "(33)" and "(3)" and missed
# "(39+765+4)" and "(4,7,8)" — the multi-note forms — reading 39 and 478 as
# figures and putting a D&A of EGP 0.0mn into two panel years, which then
# produced a spectacular and entirely spurious D&A bias. A figure carries a
# decimal point, a comma-separated group of three, or a run of four digits;
# anything else in parentheses at the head of a row is a note.
NOTEREF = re.compile(r"\((?![^)]*(?:\.\d|,\d{3}|\d{4}))[0-9A-Za-z][0-9A-Za-z+,\-/ ]{0,18}\)")


def strip_notes(tail, head=30):
    return NOTEREF.sub(" ", tail[:head]) + tail[head:]


def values_after(text, m, want=2, window=300):
    """Numeric tokens after a label, with note references dropped.

    A note reference is a parenthesised one- or two-digit integer standing
    before any real figure. Dropping it by shape rather than by position is
    what lets the same reader handle both document families.
    """
    tail = strip_notes(P.repair_ocr(text[m.end(): m.end() + window]))
    out, seen_big = [], False
    for t in P.NUM.finditer(tail):
        tok = t.group().strip()
        v = P.to_num(tok)
        if v is None:
            continue
        # A note reference stands before the figures and is distinguishable by
        # shape: a small bare integer carrying a parenthesis and NO thousands
        # separator or decimal point. The releases' own small figures — "(38.5)"
        # of marketing spend, "(1.1)" of board fees — all carry a decimal point,
        # so they survive this test while "(33)", "(3)" and the OCR'd "G7)" do
        # not.
        if (not seen_big and "(" not in tok[1:] and ")" in tok
                and "," not in tok and "." not in tok and abs(v) < 100):
            continue
        if abs(v) >= 1000:
            seen_big = True
        out.append(v)
        if len(out) >= want:
            break
    return out


def pages(text):
    """Split an extracted file into (page_no, route, body) blocks."""
    out, marks = [], list(re.finditer(r"<<<PAGE (\d+) route=(\S+)>>>", text))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out.append((int(m.group(1)), m.group(2), text[m.start():end], m.start()))
    return out


def statement_pages(text, table, take):
    """The pages that actually carry the statement, by label density.

    A label like "Gross profit" or "Hospitality revenue" appears in the prose
    of page one and again in a note twenty pages later. Neither is the
    statement. The statement is the page where the most DIFFERENT lines of the
    table appear at once, which no single stray mention can imitate.
    """
    scored = []
    for pno, route, body, off in pages(text):
        hit = sum(1 for pats in table.values()
                  if any(re.search(pat, body, re.I | re.M) for pat in pats))
        scored.append((hit, pno, off, off + len(body)))
    scored.sort(reverse=True)
    return [s for s in scored[:take] if s[0] >= 4]


# The document's own statement of the period it covers. Both forms are
# collected and the EARLIEST occurrence wins: an interim statement also prints
# "For The Year Ended 31 December" further down, over the comparative column of
# its statement of changes in equity, and matching that instead read a
# three-month document as a full year.
PERIOD_RX = re.compile(
    r"(?:[Ff]or\s+[Tt]he\s+)?(?P<span>Year|Three\s+Months?|Six\s+Months?|"
    r"Nine\s+Months?|Twelve\s+Months?|Period)\s*(?:Period\s*)?"
    r"[Ee]nded\s*:?\s*(?P<d>\d{1,2})?\s*(?:/|-)?\s*"
    r"(?P<m>January|February|March|April|May|June|July|August|September|"
    r"October|November|December|1[0-2]|[1-9])\s*(?:/|-)?\s*(?P<y>20\d\d)",
    re.I)
MONTHNO = {m.lower(): i + 1 for i, m in enumerate(
    "January February March April May June July August September October "
    "November December".split())}


def period_from_text(text, head=60000):
    """The period the document itself says it covers.

    A filename is a label somebody typed; the statement's own heading is the
    document speaking. "TMG Consolidated F S 9-2020" carries no month a
    filename reader can see, and reading it as an annual document would have
    put nine months of revenue into a full-year panel cell.
    """
    m = PERIOD_RX.search(text[:head])
    if not m:
        return None
    mo = m.group("m").lower()
    month = MONTHNO.get(mo) or int(mo)
    span = re.sub(r"\s+", " ", m.group("span")).lower()
    if span == "year" and month != 12:
        return None                # a heading that contradicts itself
    return (int(m.group("y")), month)


MN_MARK = re.compile(r"In\s*EGP\s*mn|\(EGP\s*mn\)|EGP\s*mn\b|EGP\s*million", re.I)
LE_MARK = re.compile(r"^\s*L\.?\s?E\.?\s*$|^\s*EGP\s*$", re.M)


def declared_unit(body):
    """The unit the table itself declares, not the one its family usually uses.

    The pre-2018 earnings releases EMBED the audited statements, which report
    in LE, while the same release's own summary tables report in EGP mn. A
    scale keyed on the document family put balance sheets a million times too
    large into the panel and they footed perfectly, because every identity is
    scale-invariant. The unit is therefore read per table, and a table that
    declares neither is rejected rather than assumed.
    """
    if MN_MARK.search(body):
        return 1.0, "declared EGP mn"
    if LE_MARK.search(body):
        return 1e-6, "declared LE"
    return None, "no unit declared"


def read_doc(name, table, scale, take=2):
    """{field: {year: value}} for one document, plus provenance per cell."""
    text = P.load(name)
    spans = statement_pages(text, table, take)
    units = {}
    for pno, route, body, off in pages(text):
        u, why = declared_unit(body)
        units[off] = (u, why)
    out, prov = {}, {}
    for field, pats in table.items():
        best = None
        for pat in pats:
            for m in re.finditer(pat, text, re.I | re.M):
                if not any(lo <= m.start() < hi for _, _, lo, hi in spans):
                    continue                # not on a statement page
                yrs, kind = column_years(text, m.start())
                if not yrs:
                    continue
                vals = values_after(text, m)
                if len(vals) < 2:
                    continue
                pg, route = P.page_of(text, m.start())
                best = {"years": yrs, "vals": vals, "page": pg, "route": route,
                        "at": m.start(),
                        "label": m.group(0).strip()[:70], "hdr": kind}
                break
            if best:
                break
        if not best:
            continue
        off = max((o for o in units if o <= best["at"]), default=None)
        u, why = units.get(off, (None, "no page"))
        sc = u if u is not None else scale
        for y, v in zip(best["years"], best["vals"]):
            out.setdefault(field, {})[y] = v * sc
            prov.setdefault(field, {})[y] = {
                "doc": name, "page": best["page"], "route": best["route"],
                "label": best["label"], "scale": sc, "unit_evidence": why}
    return out, prov


def main():
    reg = json.load(open(os.path.join(HERE, "ir_register.json")))
    held = {r["name"]: r for r in reg if r.get("fetched") in ("ok", "cached")}
    out = {}
    for r in held.values():
        if r["kind"] not in ("consolidated_fs", "earnings_release"):
            continue
        base = re.sub(r"[^A-Za-z0-9._-]+", "_", r["name"])[:150][:-4]
        if not os.path.exists(os.path.join(P.TEXT, base + ".txt")):
            continue
        # the audited statements report in LE; the releases in EGP mn
        scale = 1e-6 if r["kind"] == "consolidated_fs" else 1.0
        is_, isp = read_doc(base, L.IS, scale, take=2)
        bs, bsp = read_doc(base, L.BS, scale, take=3)
        stated = period_from_text(P.load(base))
        out[base] = {"kind": r["kind"],
                     "period": stated or r["period"],
                     "period_from_filename": r["period"],
                     "period_from_document": stated,
                     "scale_to_mn": scale,
                     "url": r["url"], "is": is_, "bs": bs,
                     "prov_is": isp, "prov_bs": bsp}
    kept, refused = {}, {}
    for k, v in out.items():
        yr = v["period"][0] if v["period"] else None
        cols = set()
        for tbl in ("is", "bs"):
            for byyear in v[tbl].values():
                cols |= set(byyear)
        if yr is not None and cols and yr not in cols:
            # the table's own headings do not contain the period the document
            # reports: the columns were misread, so nothing from it is used
            refused[k] = {"reports": yr, "columns_read": sorted(cols)}
            continue
        kept[k] = v
    json.dump(kept, open(os.path.join(HERE, "fs_parsed.json"), "w"), indent=1)
    json.dump(refused, open(os.path.join(HERE, "refused_documents.json"), "w"), indent=1)
    print("parsed %d documents, refused %d whose column headings did not "
          "contain their own reporting period" % (len(kept), len(refused)))
    return kept


if __name__ == "__main__":
    o = main()
    n = sys.argv[1] if len(sys.argv) > 1 else None
    if n:
        for k, v in o.items():
            if n.lower() in k.lower():
                print("\n==", k, v["period"])
                for f, d in sorted(v["is"].items()):
                    print("  IS %-22s %s" % (f, {y: round(x, 1) for y, x in d.items()}))
                for f, d in sorted(v["bs"].items()):
                    print("  BS %-22s %s" % (f, {y: round(x, 1) for y, x in d.items()}))
