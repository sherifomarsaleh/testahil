"""The VALUATION-INPUT BLOCK for this run — the figures a VALUE is rebuilt from.

[R-FCAL-01 AMENDED, 03-09-2026].  A driver panel is not a record a value can be
rebuilt from.  This run's `panel.py` committed what its own scoring needed — the
segment income statement as first reported, the unit and sales drivers off the
earnings releases, and the balance-sheet lines its working-capital driver
consumes — and answered the question it was built for.  Measured by
`engine/valuation_calibration/bridge_inputs.py`, TMGH then read as the
best-covered run in the book and STILL carried no capital expenditure at ANY
origin, no cash at FY2023 between two years that both have it, and no share
count before FY2020.

WHAT WAS ACTUALLY MISSING, AND WHY THE COUNT WOULD HAVE MISLED.  The census
reported capex 0 of 11 origins and called it a true zero rather than a parsing
miss, which was exactly right about THIS RUN'S ARTEFACTS and wrong about the
world: every one of the six annual consolidated statements on disk prints the
figure on the face of its own cash-flow statement, on a page with a text layer,
under the heading CASH FLOWS FROM INVESTING ACTIVITIES.  The run never claimed
it because no driver needed it.  That is the amendment's general lesson in one
line — what a process commits decides what can ever be asked of it later — and
the cost of carrying it out now was one afternoon of copying.

WHAT IS HERE.  For every origin this run declares — FY2015 to FY2025, fiscal
years ending 31 December, per PRE_REGISTRATION_01-09-2026.md section 1 — cash
and equivalents, interest-bearing debt, property, depreciation and amortisation,
the working-capital lines, capital expenditure, and the share count with the par
value it was footed against.

THREE ROUTES IN, RANKED, AND EVERY RECORD SAYS WHICH IT TOOK.

  panel    the run's own committed panel_annual.json cell, with the provenance
           that panel already carries (document, page, text layer or OCR).  That
           record has been through this run's own footing gate, its
           point-in-time ranking and its corroboration test, so where it carries
           a line nothing here second-guesses it.
  filing   read off a filing on disk that REPORTS the origin year, footed
           against that statement's own printed subtotals and cross-checked
           against the panel wherever the panel carries the same line.  This is
           the route for capital expenditure at every origin whose own annual
           statements are held, for the FY2023 cash the panel lacks, and for the
           capital note.
  block    a footed block from this run's own parse that REPORTS the origin year
           and that the panel's merge did not take — accepted ONLY where a
           second, independent document reads the same line to the same figure.
           This is the route for the FY2015 and FY2016 balance sheets, which the
           panel refused for a reason about the MERGE rather than about the
           figures: those releases print their summary table in EGP million and
           their balance sheet in EGP units, the two blocks share no line, and
           this run's rule is that zero shared lines is silence rather than
           agreement.  The corroboration test here is STRICTER than the panel's,
           not looser: the panel takes a lead block on its own, this takes
           nothing without a second document.

POINT-IN-TIME IS ABSOLUTE AND IT COST THIS BLOCK REAL FIGURES.  A value is
committed to an origin only from a document that REPORTS that year — the
as-first-reported rule this run's own panel.py score() implements.  A later
filing's COMPARATIVE column is never substituted, however clean it looks: the
FY2020 statements print FY2019 capital expenditure of LE 1,244,444,904 on the
face of their own cash-flow statement, and FY2019 still records capex as
MISSING, because at that origin the FY2020 statements did not exist.  The figure
is named beside instead.  The same discipline is why FY2015 to FY2019 carry no
capex and why the FY2023 restatement visible in the FY2024 statements is
recorded beside FY2023's own closing cash rather than swapped in.

ARITHMETIC IS THE ARBITER AND IT CAUGHT A CLEAN-LOOKING WRONG READING.  The
FY2025 filing is a translation of an Arabic original and its COMPARATIVE column
extracts with the digit groups REVERSED — capital expenditure comes back as
"536,614,577,72" where the FY2024 statements print 72,577,614,536.  Nothing
about that string looks broken; it parses, it is the right length, and it is
wrong by four orders of magnitude.  What exposes it is that the reversed reading
foots against the prior filing's own column and the literal one does not.  It is
the broken-character-map trap in a different costume, and the only defence is
the one clause (iii) names: foot it, never trust the extractor.

WHAT IS NOT HERE IS NAMED, ONE ITEM AT A TIME [clause (i)].  A block quietly
carrying five of six reads as complete, so every absence carries its reason and
its SIGN.  The largest of them is FY2015 and FY2016 debt, and it is worth
stating in full because it is the shape this clause exists for: those years'
short-term borrowing legs are all present and corroborated, and the long-term
leg cannot be separated from other non-current liabilities, because two
documents label the SAME figure two different ways.  A debt figure carrying only
the short legs would look complete, would foot against nothing, and would
understate debt and therefore OVERSTATE equity value.  It is recorded missing
and the short legs are named beside.

GENERATED by this module and never hand-edited; it foots at import.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import panel as PN                                            # noqa: E402

FILINGS = os.path.join(HERE, "filings")
OUT = os.path.join(HERE, "valuation_inputs.json")

# The origins this run declares. PRE_REGISTRATION_01-09-2026.md section 1:
# first admissible FY2015, last scored FY2024, FY2025 struck but unresolved.
ORIGINS = list(range(2015, 2026))

# The annual consolidated statements held on disk, by the fiscal year each one
# REPORTS. Only these six origins can read their own cash-flow statement; the
# releases the earlier origins stand on carry no cash-flow statement at all.
ANNUAL_FS = {
    2020: "TMG Consolidated FS 12-2020 _ Final _ Eng.pdf",
    2021: "TMG Conso  FSs 31 December 2021 Final.pdf",
    2022: "Eng- TMG Consolidated FS 31 December 2022.pdf",
    2023: "TMG Consolidated FS 31 Dec. 2023.pdf",
    2024: "TMG Conso  FS 31 December 2024-English.pdf",
    2025: "Consolidated financial statements for the year ended 31-12-2025-English.pdf",
}

MAG_MAX = PN.MAG_MAX          # EGP 5 trillion in EGP mn — this run's own bound
TOL_REL, TOL_ABS = PN.TOL_REL, PN.TOL_ABS

SIGN = {
    "cash":   "absent UNDERSTATES equity value",
    "debt":   "absent OVERSTATES equity value",
    "capex":  "absent OVERSTATES equity value",
    "ppe":    "no direct sign — it is what makes capex derivable by identity",
    "dep":    "no direct sign — it is what a declared capex substitution would use",
    "wc":     "sign depends on growth",
    "shares": "absent, no value can be compared with a price at all",
    "cap":    "not a share count on its own — it needs the par value beside it",
}

# ---------------------------------------------------------------------------
# the run's own committed record
# ---------------------------------------------------------------------------

def load_panel():
    return json.load(open(os.path.join(HERE, "panel_annual.json"), encoding="utf-8"))


def to_mn(v):
    """This run's own unit rule: nothing on this balance sheet is EGP 5tn."""
    return v * 1e-6 if abs(v) > MAG_MAX else v


def close(a, b):
    return abs(a - b) <= max(TOL_ABS, TOL_REL * max(abs(a), abs(b)))


def footed_blocks():
    """Every block this run parses, through this run's own footing gate."""
    out = []
    for b in PN.blocks():
        b["cells"] = PN.normalise(b["cells"])
        b, note = PN.unit_guard(b)
        b["unit_note"] = note
        b["cells"], b["derived"] = PN.fill_missing(b["cells"])
        b["foot"] = PN.foot(b["cells"])
        b["quarantined"] = []
        if any(v == "BREAK" for v in b["foot"].values()):
            b["cells"], b["quarantined"] = PN.quarantine(b["cells"], b["foot"])
            b["foot"] = PN.foot(b["cells"])
        b["ok"] = sum(1 for v in b["foot"].values() if v == "ok")
        b["broken"] = [t for t, v in b["foot"].items() if v == "BREAK"]
        if not b["broken"] and b["ok"] >= 1:
            out.append(b)
    return out


def readings(blocks, year, field):
    """Every footed reading of one line in one year, normalised to EGP million.

    Split by vintage, because the two are not interchangeable: `own` REPORTS the
    year and may be committed, `later` quotes it from a subsequent filing and may
    only corroborate or be named beside.
    """
    own, later = [], []
    for b in blocks:
        if b["year"] != year:
            continue
        v = b["cells"].get(field)
        if v is None:
            continue
        rec = {"doc": b["doc"], "kind": b["kind"], "reports": b["reports"],
               "value_mn": round(to_mn(v), 6),
               "route": (b["prov"].get(field) or {}).get("route"),
               "page": (b["prov"].get(field) or {}).get("page"),
               "interim_source": b["interim_source"]}
        (own if b["reports"] == year else later).append(rec)
    return own, later


def corroborated(own, later):
    """A value plus the documents that agree with it, or None.

    Accepted only where a SECOND, INDEPENDENT document reads the same line to the
    same figure after this run's own unit normalisation. One document alone is
    not enough here — that is the whole reason the panel was right to refuse
    these blocks and the reason this route is safe to use where it does not.
    """
    if not own:
        return None
    for cand in own:
        agree = [r for r in own + later
                 if r["doc"] != cand["doc"] and close(r["value_mn"], cand["value_mn"])]
        if agree:
            return cand, agree
    return None


# ---------------------------------------------------------------------------
# the filings on disk
# ---------------------------------------------------------------------------

NUM = re.compile(r"^-?[\d,]+(?:\.\d+)?$")


def _rows(page, ytol=6.0, xsplit=300.0):
    """Statement rows rebuilt from the text layer's word boxes.

    The two value columns of these statements sit at stable x positions while
    their y positions differ by a point or two, so a line-oriented read pairs the
    wrong figures with the wrong labels. Bracketing is read from the separate
    parenthesis TOKENS this layout emits either side of the digits.
    """
    ws = page.get_text("words")
    band = {}
    for w in ws:
        band.setdefault(round(w[1] / ytol), []).append(w)
    out = []
    for y in sorted(band):
        g = sorted(band[y], key=lambda w: w[0])
        lab = " ".join(w[4] for w in g
                       if w[0] < xsplit and not NUM.match(w[4]) and w[4] not in "()").strip()
        vals = []
        for j, w in enumerate(g):
            t = w[4]
            if w[0] < xsplit or not NUM.match(t) or not re.search(r"\d", t):
                continue
            neg = (any(x[4] == "(" for x in g[max(0, j - 2):j])
                   and any(x[4] == ")" for x in g[j + 1:j + 3]))
            f = float(t.replace(",", ""))
            vals.append((w[0], -f if neg else f))
        out.append((lab, vals))
    return out


def _ocr(path, pno, dpi=300):
    import pymupdf
    d = pymupdf.open(path)
    pix = d[pno - 1].get_pixmap(dpi=dpi)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
        t.write(pix.tobytes("png"))
        png = t.name
    try:
        r = subprocess.run(["tesseract", png, "stdout", "-l", "eng", "--psm", "6"],
                           capture_output=True, timeout=600)
        return r.stdout.decode("utf-8", "replace")
    finally:
        os.unlink(png)
        d.close()


def cf_statement(year):
    """The face of that year's own consolidated statement of cash flows.

    Read in LINEAR order rather than by word box, because on this statement a
    label wraps over two lines while its figures sit on a third, and a y-band
    read pairs the capital-expenditure label with the DISPOSAL row's figures —
    which is a clean-looking wrong answer of exactly the kind clause (iii) is
    about.  It was caught by footing the chain: FY2020 came back at LE 9,635,649
    against a comparative column in the FY2021 filing reading LE 2,379,865,913.

    Returns the OWN column and the comparative separately.  They are not
    interchangeable: the comparative is a later document's reading of an earlier
    year and is used ONLY to foot the chain, never committed to that earlier
    origin.
    """
    import pymupdf
    path = os.path.join(FILINGS, ANNUAL_FS[year])
    d = pymupdf.open(path)
    page = None
    for i, pg in enumerate(d):
        low = (pg.get_text() or "").lower()
        if "investing activities" in low and "cash flow" in low:
            page = i
            break
    if page is None:
        raise SystemExit("REFUSED: no cash-flow statement page in %s" % ANNUAL_FS[year])
    lines = [l.strip() for l in (d[page].get_text() or "").splitlines()]
    d.close()

    rows, label, nums = [], [], []
    for ln in lines:
        if not ln or ln in "()":
            continue
        t = ln.strip("()").replace(",", "").strip()
        if re.fullmatch(r"-?\d+(?:\.\d+)?", t):
            v = float(t)
            nums.append(-v if ln.strip().startswith("(") else v)
            continue
        if nums:
            rows.append((" ".join(label).lower(), nums))
            label, nums = [], []
        label.append(ln)
    if nums:
        rows.append((" ".join(label).lower(), nums))

    want = {
        "dep":      (("depreciation",), ("amortization", "amortisation")),
        "capex":    (("acquire fixed assets", "purchase of fixed assets"), None),
        "disposal": (("proceeds from sale of fixed", "proceeds from disposal of fixed"), None),
        "close":    (("cash and cash equivalent",), ("end of the",)),
        "open":     (("cash and cash equivalent",), ("beginning",)),
    }
    got = {}
    for lab, vals in rows:
        for key, (needles, extra) in want.items():
            if key in got or not any(n in lab for n in needles):
                continue
            if extra and not any(e in lab for e in extra):
                continue
            big = [v for v in vals if abs(v) > 1e5]
            if not big:
                continue
            got[key] = {"value": big[0], "comparative": big[1] if len(big) > 1 else None,
                        "page": page + 1, "label": lab[:160]}
    return got


def capital_note(year):
    """The capital note's recital, and the last resolution that CHANGED capital.

    The note is a CHRONOLOGY of general-assembly resolutions rather than one
    current-capital sentence — precisely the case clause (ii) names — so the par
    value and the identity come from the recital and the count is that year's own
    committed capital over that par. The recital's LAST step is what this returns.
    """
    import pymupdf
    path = os.path.join(FILINGS, ANNUAL_FS[year])
    d = pymupdf.open(path)
    steps, par, page_of = [], None, None
    pat = re.compile(
        r"(?:become|becomes|became)\s+(?:LE|EGP)\s*([\d,]{9,})"
        r"[^.]{0,220}?over\s*([\d,]{9,})\s*shares?", re.I | re.S)
    parpat = re.compile(r"(?:LE|EGP)\s*(\d+)\s*(?:\(\s*Ten[^)]*\)\s*)?-?\s*par\s*value", re.I)
    for i, pg in enumerate(d):
        t = (pg.get_text() or "").replace("\n", " ")
        if "CAPITAL" not in t.upper() or "assembly" not in t.lower():
            continue
        for m in pat.finditer(t):
            cap = float(m.group(1).replace(",", ""))
            cnt = float(m.group(2).replace(",", ""))
            steps.append({"issued_capital": cap, "count": cnt, "page": i + 1})
        pm = parpat.search(t)
        if pm and par is None:
            par = float(pm.group(1))
            page_of = i + 1
    d.close()
    return {"steps": steps, "par_value": par, "page": page_of,
            "file": ANNUAL_FS[year]}


def _ocr_numbers(line):
    """Comma-grouped figures off one OCR'd statement line.

    Tokens are merged where OCR has split a group across a space — this page
    yields "127,232,472, 166" for 127,232,472,166 — and a token is accepted only
    if it is a properly grouped figure. A regex run straight over the line
    concatenates the two YEAR COLUMNS into one 22-digit number that still looks
    like a figure, which is why the split is done on tokens rather than by
    pattern.
    """
    toks, buf = [], ""
    for t in line.split():
        t = buf + t
        buf = ""
        if t.endswith(","):
            buf = t
            continue
        toks.append(t)
    out = []
    for t in toks:
        t = t.strip("()")
        if re.fullmatch(r"\d{1,3}(?:,\d{3})+", t):
            out.append(float(t.replace(",", "")))
    return out


def bs_2023_ocr():
    """FY2023's own balance sheet, read by OCR off the rendered pixels.

    The FY2023 filing's statement pages carry NO text layer, so the cash line and
    the assets-under-construction line the panel lacks are read the way clause
    (iii) requires — off the page — and footed against the printed subtotals the
    panel already committed from the same statement.
    """
    path = os.path.join(FILINGS, ANNUAL_FS[2023])
    txt = _ocr(path, 5)
    out = {}
    for line in txt.splitlines():
        low = line.lower().strip()
        nums = _ocr_numbers(line)
        if not nums:
            continue
        for key, needle in (("cash", "cash on hand"),
                            ("puc", "fixed assets under construction"),
                            ("ppe", "fixed assets ("),
                            ("investment_properties", "investment properties"),
                            ("total_ca", "total current assets"),
                            ("total_nca", "total non-current assets"),
                            ("total_assets", "total assets")):
            if key in out or needle not in low:
                continue
            out[key] = {"own": nums[0], "comparative": nums[1] if len(nums) > 1 else None,
                        "line": line.strip()[:120]}
    return out, 5, txt
