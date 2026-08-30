"""Extract PHDC's operating drivers from its own earnings releases.

The financial statements carry no units, no prices and no backlog — for a
developer those are the drivers, so they come from the release, which is a
company document and therefore still tier A.

Each release embeds four-to-five-year chart series (new sales value and number
of units, total and by region). Every fiscal year therefore appears in several
releases, which is used as the check: a year's value is accepted only where the
releases that report it agree, and any disagreement is recorded rather than
averaged away.
"""
import os, re, json, glob, collections

TXT = os.environ.get("PHDC_TXT",
    "/tmp/claude-0/-home-user-testahil/2283e95e-66db-5f22-bba6-0db833f32495/scratchpad/phdc_src/text")
NUMTOK = re.compile(r"^\(?-?[\d][\d,]*\)?$")


def tonum(s):
    neg = s.startswith("(")
    v = float(s.strip("()").replace(",", ""))
    return -v if neg else v


def chart_blocks(txt):
    """Every embedded chart series in a release, as (values, units?, years).

    A block is a run of figures followed by a run of year labels. Two shapes
    occur and both must be read: the by-region charts carry a units series as
    well as a value series and label it, while the all-regions chart in the
    later releases carries values only. Keying on the "Number of Units" label —
    which is what the first cut did — therefore silently skips the ALL-REGIONS
    series and leaves the largest region standing in for the company total.
    """
    lines = [l.strip() for l in txt.split("\n")]
    out = []
    i = 0
    while i < len(lines):
        if not re.fullmatch(r"20[0-2]\d", lines[i]):
            i += 1
            continue
        j, years = i, []
        while j < len(lines) and (not lines[j] or re.fullmatch(r"20[0-2]\d", lines[j])):
            if lines[j]:
                years.append(int(lines[j]))
            j += 1
        n = len(years)
        if n < 3 or years != sorted(years) or years[-1] - years[0] != n - 1:
            i = j
            continue
        k, vals = i - 1, []
        while k >= 0 and len(vals) < 3 * n:
            if not lines[k]:
                k -= 1
                continue
            if NUMTOK.match(lines[k]):
                vals.append(tonum(lines[k]))
                k -= 1
            else:
                break
        vals.reverse()
        # Three shapes occur. The 2015-16 releases plot GROSS sales, NET sales
        # (gross less that period's cancellations) and units together, so a
        # two-series reading takes NET as the sales line and understates the
        # company's own headline. New Sales is defined by the releases' own
        # footnote as GROSS new sales, so the first series is the one to keep.
        three = None
        if len(vals) >= 3 * n:
            a, b = vals[-3 * n:-2 * n], vals[-2 * n:-n]
            # Accept a gross/net/units reading ONLY where it is structurally
            # possible: net sales are gross less cancellations, so gross must
            # dominate net in every year. Without this test the walk-back runs
            # past the top of a two-series chart into the tail of the chart
            # above it and reads a REGION's series as the company's gross.
            if all(x >= y for x, y in zip(a, b)):
                three = {"years": years, "sales": a, "net_sales": b, "units": vals[-n:]}
        if three:
            out.append(three)
        elif len(vals) >= 2 * n:
            out.append({"years": years, "sales": vals[-2 * n:-n],
                        "net_sales": None, "units": vals[-n:]})
        elif len(vals) == n:
            out.append({"years": years, "sales": vals, "net_sales": None, "units": None})
        i = j
    return out


# Narrative drivers. Each is pinned to the SENTENCE it came from, and the
# sentence is re-checked against the source file — the value is never carried
# forward on its own. The cumulative-to-date phrasings ("As at end of FY2022,
# PHD delivered 13,564 units within its developments") are excluded explicitly,
# because they read exactly like the period figure and are an order of
# magnitude larger.
CUMULATIVE = re.compile(r"as at end of|within its developments|to date|since inception",
                        re.I)

NARR_PATTERNS = {
    "units_delivered": [
        r"(?:The )?Company delivered\s+(?:c\.\s?)?([\d,]+)\s+units",
        r"delivered\s+([\d,]+)\s+residential and commercial units",
        r"handed over\s+([\d,]+)\s+units during the (?:year|period)",
        r"including\s+([\d,]+)\s+units that were handed over to clients",
        r"handing over of\s+([\d,]+)\s+units",
        r"handed over\s+([\d,]+)\s+units",
        r"delivered\s+([\d,]+)\s+units",
    ],
    "construction_spend": [
        r"spent EGP\s?([\d.,]+)\s?(billion|bn|million|mn)\s+on construction",
        r"[Cc]onstruction spend(?:ing)?[^.]{0,70}?EGP\s?([\d.,]+)\s?(billion|bn|million|mn)",
        r"construction spend of\s+EGP\s?([\d.,]+)\s?(billion|bn|million|mn)",
    ],
    "backlog": [
        r"backlog[^.]{0,110}?EGP\s?([\d.,]+)\s?(billion|bn|million|mn)",
    ],
    "collections": [
        r"[Cc]ash collection[^.]{0,80}?EGP\s?([\d.,]+)\s?(billion|bn|million|mn)",
        r"collected EGP\s?([\d.,]+)\s?(billion|bn|million|mn)",
    ],
}


def sentences(txt):
    flat = re.sub(r"\s+", " ", txt)
    return re.split(r"(?<=[.])\s+", flat)


def scale(unit):
    return 1000.0 if unit and unit.lower() in ("billion", "bn") else 1.0


QUARTERLY = re.compile(r"\b[1-4]Q\s?20\d\d|\bQ[1-4]\s?20\d\d|during the quarter|"
                       r"for the quarter|in the quarter", re.I)


def parse_narrative(txt, fy):
    """Return {field: {value, sentence}} — never a bare number.

    All matching sentences are collected and then RANKED, rather than taking
    the first hit. The releases state the same driver at several scopes in the
    same document — full year, one quarter, and one project — and a
    first-match rule picks whichever the layout happens to put first: it read
    FY2017 handovers as 441 (that is 4Q alone against 1,781 for the year) and
    FY2019 as 133 (one project, Palm Valley, against 964). Period scope is the
    discriminator, so it is scored explicitly.
    """
    out = {}
    sents = sentences(txt)
    for field, pats in NARR_PATTERNS.items():
        cands = []
        for pat in pats:
            for sent in sents:
                if CUMULATIVE.search(sent):
                    continue
                m = re.search(pat, sent)
                if not m:
                    continue
                g = m.groups()
                val = tonum(g[0])
                if len(g) > 1 and g[1]:
                    val *= scale(g[1])
                score = 0
                if re.search(r"FY\s?%d" % fy, sent):
                    score += 3
                if re.search(r"during the year|for the year|full year|during %d" % fy, sent, re.I):
                    score += 2
                if QUARTERLY.search(sent):
                    score -= 5
                cands.append((score, -len(cands), val, sent.strip()[:300]))
        if cands:
            cands.sort(reverse=True)
            _, _, val, sent = cands[0]
            out[field] = {"value": val, "sentence": sent}
    return out


def build():
    """Per fiscal year, the company total for each chart driver.

    Regions are subsets of the company, so across the blocks in one release the
    ALL-REGIONS series is the elementwise maximum — that is what identifies it,
    rather than its position or its caption. Each year is reported by several
    releases; those readings are kept separately so agreement can be checked
    instead of assumed.
    """
    series = collections.defaultdict(lambda: collections.defaultdict(dict))
    narr = {}
    for path in sorted(glob.glob(os.path.join(TXT, "*_Q4_ER.txt"))):
        stem = os.path.basename(path)[:-4]
        fy = int(stem[:4])
        txt = open(path, encoding="utf-8").read()
        blocks = chart_blocks(txt)
        by_year_sales, by_year_units = {}, {}
        for b in blocks:
            for idx, y in enumerate(b["years"]):
                v = b["sales"][idx]
                if y not in by_year_sales or v > by_year_sales[y][0]:
                    by_year_sales[y] = (v, b)
        for y, (v, b) in by_year_sales.items():
            series["new_sales"][y][stem] = v
            if b["units"]:
                series["units_sold"][y][stem] = b["units"][b["years"].index(y)]
        narr[fy] = parse_narrative(txt, fy)
    return series, narr


if __name__ == "__main__":
    series, narr = build()
    print("=== new sales (EGP mn) and units sold, as reported by each release ===")
    for y in sorted(series["new_sales"]):
        s = series["new_sales"][y]
        u = series["units_sold"][y]
        vs, vu = set(s.values()), set(u.values())
        flag = "" if len(vs) <= 1 and len(vu) <= 1 else "   <-- RELEASES DISAGREE"
        print("  %d  sales=%-28s units=%-24s n=%d%s" % (
            y, sorted(vs), sorted(vu), len(s), flag))
    print("\n=== narrative drivers, per FY release (with source sentence) ===")
    for fy in sorted(narr):
        for k, v in sorted(narr[fy].items()):
            print("  FY%d %-19s %10.1f   %s" % (fy, k, v["value"], v["sentence"][:96]))
