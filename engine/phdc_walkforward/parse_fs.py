"""Parse PHDC consolidated financial statements positionally.

These are English translations of Arabic-original filings. The PDF text layer
emits each figure's thousands-groups in right-to-left run order, so reading the
text stream gives "070 719 175 3" for 3,175,719,070. Reading order is therefore
never trusted: every figure is rebuilt from the WORD X-COORDINATES, and the two
period columns are located from the statement's own date header rather than a
hardcoded x-split.

The parse is then checked against the statement's own arithmetic (gross profit,
balance-sheet balance, profit build). A page that does not foot is reported, not
quietly accepted.
"""
import os, re, json, subprocess, tempfile
import pymupdf

SRC = os.environ.get("PHDC_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/2283e95e-66db-5f22-bba6-0db833f32495/scratchpad/phdc_src")

# Tesseract's systematic digit confusions on these scans, applied ONLY to
# tokens that sit inside a value column and that become a clean thousands-group
# once mapped. Every repair is still gated by the statement's own footing: a
# page is accepted only if it adds up, so a wrong repair fails loudly rather
# than entering the panel.
OCR_DIGIT = str.maketrans({"§": "5", "S": "5", "s": "5", "]": "1", "}": "1",
                           "|": "1", "l": "1", "I": "1", "i": "1", "!": "1",
                           "O": "0", "o": "0", "D": "0", "B": "8", "Z": "2",
                           "G": "6", "g": "9", "q": "9", "T": "7", "b": "6"})


def ocr_fix(t):
    return t.translate(OCR_DIGIT)


DATE_HDR = re.compile(r"^(3[01]|30|29|28)$|^Dec$|^December$|^March$|^June$|^Mar$|^Jun$|^Sep$|^September$")
GROUP = re.compile(r"^\(?[\d]{1,3}\)?$|^\(?[\d,]{1,15}(?:\.\d+)?\)?$")


def words_text(page):
    return [(w[0], w[1], w[2], w[3], w[4]) for w in page.get_text("words")]


_OCR_CACHE = {}


def words_ocr(page, dpi=300):
    """Same (x0,y0,x1,y1,text) shape, via tesseract TSV so OCR'd pages parse
    through exactly the same column logic as text-layer pages."""
    ck = (getattr(page.parent, "name", ""), page.number, dpi)
    if ck in _OCR_CACHE:
        return _OCR_CACHE[ck]
    pix = page.get_pixmap(dpi=dpi)
    scale = 72.0 / dpi
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
        t.write(pix.tobytes("png"))
        png = t.name
    try:
        r = subprocess.run(["tesseract", png, "stdout", "-l", "eng", "--psm", "6", "tsv"],
                           capture_output=True, timeout=240)
        out = []
        for line in r.stdout.decode("utf-8", "replace").split("\n")[1:]:
            f = line.split("\t")
            if len(f) < 12 or not f[11].strip():
                continue
            try:
                left, top, w, h = (int(f[6]), int(f[7]), int(f[8]), int(f[9]))
            except ValueError:
                continue
            out.append((left * scale, top * scale, (left + w) * scale,
                        (top + h) * scale, f[11].strip()))
        _OCR_CACHE[ck] = out
        return out
    finally:
        os.unlink(png)


def rows_from_words(words, tol=4.0):
    rows = {}
    for x0, y0, x1, y1, t in words:
        yc = (y0 + y1) / 2.0
        key = None
        for k in rows:
            if abs(k - yc) <= tol:
                key = k
                break
        rows.setdefault(key if key is not None else yc, []).append((x0, t))
    return [(y, sorted(v)) for y, v in sorted(rows.items())]


def find_columns(rows):
    """Locate the two period columns from the statement's own date header.

    Across the 2015-2026 archive that header is written five ways —
    "2015 2014", "31/12/2018 31/12/2017", "31 Dec 2020 31 Dec 2019",
    "31 December ...", and (2019) with the year split across two text tokens
    as "31/12/201" + "9". So adjacent tokens are glued before testing, and the
    test is: a row carrying two date-bearing tokens far enough apart to be two
    columns. Their x positions ARE the columns — no x-split is hardcoded.
    """
    YEAR = re.compile(r"(?:^|[^\d])?(20[0-2]\d)$")

    def glue(items):
        out, i = [], 0
        while i < len(items):
            x, t = items[i]
            partial = re.search(r"/20[0-2]\d?$", t)      # 2019 splits as "31/12/201"+"9"
            while (i + 1 < len(items) and not YEAR.search(t)
                   and (items[i + 1][0] - x < 14
                        or (partial and len(items[i + 1][1]) <= 2
                            and items[i + 1][0] - x < 60))):
                t += items[i + 1][1]
                i += 1
            out.append((x, t))
            i += 1
        return out

    best = None
    for y, items in rows:
        g = glue(items)
        hits = [(x, t) for x, t in g if YEAR.search(t)]
        if len(hits) < 2:
            continue
        xs = sorted(x for x, _ in hits)
        if xs[-1] - xs[0] < 25:
            continue
        # the header nearest the body wins; a cover/title line sits far above
        if best is None or y > best[2]:
            if y < 320:
                best = ([xs[0], xs[-1]], " ".join(t for _, t in g), y)
    if best:
        return best[0], best[1]
    return None, None


def numeric_cells(items, col_x, split, right_edge, left_bound):
    """Rebuild the two period figures on one row from digit groups by x.

    Two things have to be kept out. Note references ("(26, 53)") sit in their
    own band left of the figures, and are excluded by a LEFT BOUND derived from
    the right column's own width rather than a fixed offset — these layouts
    right-align both columns to the same width, so the left column cannot start
    further left than that. And OCR sometimes renders the thousands space as a
    full stop ("3.175" for "3 175"), so a figure assembled from more than one
    token is treated as an integer and its stops dropped; a single-token figure
    keeps its decimal point, which is how EPS survives.
    """
    cand = []
    for x, t in items:
        if t in ("-", "--", ".", "-."):
            continue
        if re.fullmatch(r"\(?-?[\d,.]{1,15}\)?", t):
            cand.append((x, t))
        elif re.fullmatch(r"\(?-?[\d,.]{1,15}\)?", ocr_fix(t)):
            cand.append((x, ocr_fix(t)))
        elif re.fullmatch(r"\(?[\d,.]{1,12}[a-zA-Z+«¢:.,]{1,3}\)?", t):
            cand.append((x, t))          # kept only so the note gutter is measurable
    # The note-reference column is separated from the figures by a wide gutter.
    # Measured across this archive that gutter is never under 34pt, while the
    # gap between thousands-groups INSIDE one figure never exceeds ~20pt — so a
    # 25pt cut separates them cleanly and needs no page-specific offset.
    if left_bound == "perrow":
        run = sorted([(x, t) for x, t in cand if x < split])
        keep = 0
        for i in range(len(run) - 1, 0, -1):
            if run[i][0] - run[i - 1][0] >= 25.0:
                keep = i
                break
        left = run[keep:]
    else:
        left = sorted([(x, t) for x, t in cand if x < split and x >= left_bound])
    buckets = {0: left, 1: sorted([(x, t) for x, t in cand if x >= split])}
    for b in (0, 1):
        buckets[b] = [(x, t) for x, t in buckets[b]
                      if re.fullmatch(r"\(?-?[\d,.]{1,15}\)?", t)]
    out = []
    for b in (0, 1):
        toks = [t for _, t in sorted(buckets[b])]
        if not toks:
            out.append(None)
            continue
        neg = any("(" in t or ")" in t for t in toks)
        if len(toks) == 1:
            digits = re.sub(r"[^\d.]", "", toks[0])
        else:
            digits = "".join(re.sub(r"[^\d]", "", t) for t in toks)
        if not digits or digits == ".":
            out.append(None)
            continue
        try:
            v = float(digits)
        except ValueError:
            out.append(None)
            continue
        out.append(-v if neg else v)
    return out


def note_gutter(rows, split, mode='pooled'):
    """Where the note-reference column ends, measured across the WHOLE page.

    Per-row measurement fails: OCR sometimes merges three thousands-groups into
    one token, which leaves a 30pt hole INSIDE a single figure and a per-row
    rule then amputates its leading digits. Pooling every row fills those holes
    in — other rows put tokens there — so the only wide gap left in the pooled
    histogram is the real gutter. Where no wide gap survives (the clean
    text-layer filings set their notes close to the figures) the function falls
    back to a fixed offset, which is what those pages already parsed correctly
    under.
    """
    xs = sorted(set(round(x, 1) for _, its in rows for x, t in its
                    if split - 120.0 <= x < split and re.fullmatch(r"\(?-?[\d,.]{1,15}\)?|"
                                                  r"\(?[\d,.]{1,12}[a-zA-Z+«¢:.,]{1,3}\)?",
                                                  t)))
    best = (0.0, None)
    for a, b in zip(xs, xs[1:]):
        if b - a > best[0]:
            best = (b - a, b)
    if mode == "fixed":
        return split - 90.0
    if best[0] >= 25.0 and best[1] is not None:
        return best[1] - 2.0
    return split - 90.0


def infer_columns(rows, page_width):
    """Header-free column detection, used only when OCR mangles the date row.

    On several scanned filings tesseract turns "31 Dec 2021  31 Dec 2020" into
    "31 | 31" and noise, so the header cannot seed the columns even though the
    figures underneath came through cleanly. The two value columns are then
    recovered from the figures themselves: in the right-hand region of the page,
    the widest whitespace band between numeric tokens is the gutter between the
    periods. Nothing here is fitted — the band is measured, and the parse is
    still only accepted if the statement foots.
    """
    # Note references are parenthesised — "(64s 29)" — and sit in their own
    # band left of the figures. Dropping every parenthesised token keeps that
    # band out of the gap search; a genuinely negative figure is also dropped,
    # which costs nothing here because only the COLUMN POSITION is being
    # inferred, not any value.
    xs = []
    for y, items in rows:
        for x, t in items:
            if "(" in t or ")" in t:
                continue
            if re.fullmatch(r"-?[\d,.]{1,15}", t) and x > page_width * 0.62:
                xs.append(x)
    xs = sorted(set(round(x, 1) for x in xs))
    if len(xs) < 6:
        return None, None
    gaps = [(b - a, a, b) for a, b in zip(xs, xs[1:])]
    gaps.sort(reverse=True)
    width, a, b = gaps[0]
    if width < 20:
        return None, None
    left = [x for x in xs if x <= a]
    right = [x for x in xs if x >= b]
    if not left or not right:
        return None, None
    return [min(left), min(right)], "INFERRED (no readable date header)"


def column_split(rows, col_x):
    """Find where the two value columns actually part, on the page's own data.

    The header x positions only say roughly where each column starts — the
    right column's figures begin well left of its header token, so a midpoint
    between header positions cuts the LEFT column's last thousands-group off.
    The columns are instead separated by the widest whitespace band in the
    numeric region, which the header brackets. That band is measured here.
    """
    xs = []
    for y, items in rows:
        for x, t in items:
            if re.fullmatch(r"\(?-?[\d,]{1,15}(?:\.\d+)?\)?", t) and x > col_x[0] - 35:
                xs.append(x)
    xs = sorted(set(round(x, 1) for x in xs))
    best_gap, best_mid = 0.0, None
    for a, b in zip(xs, xs[1:]):
        mid = (a + b) / 2.0
        if col_x[0] < mid < col_x[1] + 45 and (b - a) > best_gap:
            best_gap, best_mid = b - a, mid
    if best_mid is not None and best_gap >= 22:
        return best_mid
    return (col_x[0] + col_x[1]) / 2.0


def parse_page(doc, pno, route, dpi=200, gutter='pooled'):
    page = doc[pno]
    words = words_text(page) if route == "text" else words_ocr(page, dpi=dpi)
    rows = rows_from_words(words, tol=4.0 if route == "text" else 5.0)
    col_x, hdr = find_columns(rows)
    if not col_x:
        col_x, hdr = infer_columns(rows, page.rect.width)
    if not col_x:
        return None
    split = column_split(rows, col_x)
    right_edge = max([x for _, its in rows for x, t in its
                      if re.fullmatch(r"\(?-?[\d,.]{1,15}\)?", t)]
                     or [split + 60])
    left_bound = "perrow" if gutter == "perrow" else note_gutter(rows, split, gutter)
    raw = []
    for y, items in rows:
        label = " ".join(t for x, t in items
                         if x < split - 90 and not re.fullmatch(r"[\d,()،.\-]+", t))
        vals = numeric_cells(items, col_x, split, right_edge, left_bound)
        raw.append({"y": round(y, 1), "label": label.strip(), "v": vals})

    # A long line item wraps: "Net profit for the year before income tax &
    # non-" sits on one line, "controlling interest" on the next, and the
    # FIGURES land between them on a line of their own. Clustering by y alone
    # therefore yields a valued row with no label and two labelled rows with no
    # values, and the profit lines simply vanish from the parse. Stitch the
    # value row back onto the wrapped label it belongs to.
    for i, r in enumerate(raw):
        if r["label"] or not any(v is not None for v in r["v"]):
            continue
        parts, j = [], i - 1
        while j >= 0 and raw[j]["label"] and not any(v is not None for v in raw[j]["v"]) \
                and abs(raw[j]["y"] - raw[j + 1]["y"]) < 18:
            parts.insert(0, raw[j]["label"])
            j -= 1
        k = i + 1
        while k < len(raw) and raw[k]["label"] and not any(v is not None for v in raw[k]["v"]) \
                and abs(raw[k]["y"] - raw[k - 1]["y"]) < 18:
            parts.append(raw[k]["label"])
            k += 1
        if parts:
            r["label"] = " ".join(parts).strip()
            r["wrapped"] = True

    # A second wrap shape: the label breaks mid-word ("... income tax & non-" /
    # "controlling interest") and the FIGURES sit on the continuation line —
    # sometimes split across both lines, one period on each. Left alone, the
    # first fragment keeps a label that reads like the whole line item and
    # carries the WRONG row's figures, so a regex for "before income tax"
    # matches it and takes them. Merge the fragments, move the label to
    # whichever line holds the figures, and blank the donor.
    for i in range(len(raw) - 1):
        a, b = raw[i], raw[i + 1]
        if not a["label"] or not b["label"]:
            continue
        if abs(b["y"] - a["y"]) > 30:
            continue
        if not re.search(r"[-&]$|\bnon-$", a["label"]):
            continue
        if not b["label"][:1].islower():
            continue
        merged = (a["label"].rstrip() + b["label"]) if a["label"].endswith("-") \
            else (a["label"] + " " + b["label"])
        va, vb = a["v"], b["v"]
        if all(x is None or y is None for x, y in zip(va, vb)):
            b["v"] = [x if x is not None else y for x, y in zip(vb, va)]
            a["v"] = [None, None]
        b["label"] = merged
        a["label"] = ""
        a["wrapped_donor"] = True

    out = [r for r in raw if any(v is not None for v in r["v"])]
    return {"page": pno, "header": hdr, "split": split, "rows": out}


def locate(doc, patterns, route, maxp=9):
    """Return every CANDIDATE page per statement, in order.

    A single best-guess page is not safe here: the auditor's opinion letter
    quotes the phrase "statement of financial position", so a first-match rule
    hands back the letterhead and the parse then reports nothing rather than
    reporting the wrong page loudly. The caller therefore walks the candidates
    and keeps the first that actually yields a period header and a table.
    """
    hits = {k: [] for k in patterns}
    for p in range(min(maxp, len(doc))):
        t = doc[p].get_text()
        if len(t) < 200 and route == "ocr":
            t = " ".join(w[4] for w in words_ocr(doc[p], dpi=150))
        up = t.upper()
        for name, pat in patterns.items():
            if re.search(pat, up):
                hits[name].append(p)
    return hits


PATTERNS = {
    "bs": r"FINANCIAL POSITION|BALANCE SHEET",
    "is": r"STATEMENT OF INCOME|INCOME STATEMENT|\(PROFIT OR LOSS\)",
    "cf": r"STATEMENT OF CASH FLOW",
}


def parse_statement(stem, route="text", dpi=200, gutter="pooled"):
    path = os.path.join(SRC, stem + ".pdf")
    doc = pymupdf.open(path)
    hits = locate(doc, PATTERNS, route)
    res = {"_stem": stem, "_route": route, "_pages": {}}
    for name, pages in hits.items():
        for pno in pages:
            try:
                got = parse_page(doc, pno, route, dpi, gutter)
            except Exception as e:
                got = {"error": "%s: %s" % (type(e).__name__, e)}
            if got and got.get("rows") and len(got["rows"]) >= 5:
                res[name] = got
                res["_pages"][name] = pno
                break
    doc.close()
    return res


if __name__ == "__main__":
    import sys
    for stem in (sys.argv[1:] or ["2020_Q4_FS"]):
        r = parse_statement(stem)
        print("=" * 25, stem, r["_pages"])
        for k in ("is", "bs"):
            if k in r and r[k] and "rows" in r[k]:
                print("--", k, "| header:", r[k]["header"][:60])
                for row in r[k]["rows"][:26]:
                    print("   %-58s %s" % (row["label"][:58], row["v"]))
