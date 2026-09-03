"""The share count at each origin, read off the filings by OCR.

WHY THIS EXISTS. A mechanical fair value is an equity value; to meet a share price
it needs the share count AT THAT ORIGIN. Today's count is not a substitute —
counts change on capital increases, so carrying the current one back to a past
year is right only by luck: fabricated in vintage, plausible on the page, and
invisible in the pooled error afterwards.

The counts are in the filings the walk-forwards already fetched, in the equity
note (issued and paid-up capital, and the par value it divides by) and in the
earnings-per-share note (the weighted average number of shares). Those filings are
SCANS — pdftotext returns forty characters from a forty-page document — so the
pages are rendered and read by OCR, which is the route the protocol already
sanctions for a page whose text layer cannot be trusted.

WHAT IT REFUSES. A count is recorded only where it FOOTS: issued capital divided
by par value must reproduce the share count the same document states, or the two
must agree with the weighted average within a stated tolerance. OCR reads digits
wrongly in ways that look entirely plausible — a 3 for an 8, a dropped thousands
separator — and a share count wrong by a factor is a fair value wrong by the same
factor with nothing to show for it. Arithmetic is the arbiter, not the extractor's
confidence: a year whose numbers do not foot is REPORTED and DROPPED, never
recorded with a caveat.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)

# The note we want names itself. Search on the words a balance sheet actually
# uses rather than on a page number, because the note moves between editions.
HINTS = re.compile(
    r"issued\s+and\s+paid|paid[\s-]*up\s+capital|par\s+value|authoriz|"
    r"weighted\s+average\s+number|earnings\s+per\s+share|share\s+capital",
    re.I)

# The same note in Arabic. EGCH files its annual report in Arabic and the scans
# read cleanly under tesseract's Arabic model, so the note is found on the words
# the document itself uses — capital, issued, paid, par — rather than on a
# transliteration or a page number. Anchored on RAS AL-MAL so that the word
# "share", which appears on nearly every page of a company report, cannot on its
# own pull in a page that is not the capital note.
HINTS_AR = re.compile(
    "(?=.*(?:\u0631\u0623\u0633|\u0631\u0627\u0633)\s*\u0627?\u0644?\s*\u0645\u0627\u0644)"
    "(?=.*(?:\u0627\u0644\u0645\u0635\u062f\u0631|\u0627\u0644\u0645\u062f\u0641\u0648\u0639|"
    "\u0627\u0633\u0645\u064a\u0629|\u0633\u0647\u0645))",
    re.S)

# Which model reads which company's filings. EGCH's are Arabic scans; ARCC's and
# PHDC's are English ones. Reading an Arabic page with the English model returns
# plausible-looking Latin noise with the digits mangled — the broken-character-map
# failure the protocol names, arriving through OCR instead of a font.
LANG = {"EGCH": "ara"}

# Coarse to find the page, fine to read the figures on it.
FIND_DPI = 100
READ_DPI = 200
NUM = re.compile(r"-?\d[\d,\.]{2,}")


def year_of(name):
    """The fiscal year a filing REPORTS ON, as the calendar year it ends in.

    Two conventions live in this repository and they are not interchangeable.
    PHDC closes on 31 December, so "4Q17" and "31 Dec 2023" mean what they say.
    EGCH closes on 30 JUNE, and its reports are named FY2015-16 — that document
    reports the year ending 30 June 2016 and is the latest annual statement an
    analyst had at the 31-Dec-2016 origin. Returning 2015 for it would silently
    hand a later origin an earlier year's equity note.
    """
    m = re.search(r"FY\s*((?:19|20)\d{2})\s*[-/]\s*(\d{2,4})", name, re.I)
    if m:
        end = m.group(2)
        return int(end) if len(end) == 4 else 2000 + int(end)
    # "31 Dec 2023", "31 Dec. 2023", "31 December 2024", "31-12-2025", "4Q17".
    # Only a YEAR-END document: an interim carries the same note but a different
    # balance-sheet date, and a March or June sheet read as the annual one would
    # put the wrong period's capital against the origin.
    m = re.search(r"31[\s.\-]*(?:Dec[a-z.]*|12)[\s.\-]*((?:19|20)\d{2})", name, re.I)
    if not m:
        # "FS 12-2020" — the month-year form. Anchored on 12 so that the
        # September file named "F S 9-2020" beside it cannot be read as an annual.
        m = re.search(r"(?:^|[^\d])12[\s.\-_/]((?:19|20)\d{2})", name)
    if not m:
        m = re.search(r"4Q\s*((?:19|20)?\d{2})", name, re.I)
    if not m:
        # A single-year name — ARCC files as ARCC_FY2018_Consolidated. It is tried
        # only after the two-part pattern above, so a June-closing FY2015-16 name
        # can never fall through to it and be read as 2015.
        m = re.search(r"FY[\s_-]*((?:19|20)\d{2})(?![\s_-]*\d)", name, re.I)
    if not m:
        return None
    y = int(m.group(1))
    return 2000 + y if y < 100 else y


def filings(ticker):
    d = os.path.join(ENGINE, "%s_walkforward" % ticker.lower(), "filings")
    if not os.path.isdir(d):
        return []
    out = []
    for f in sorted(os.listdir(d)):
        if not f.lower().endswith(".pdf"):
            continue
        y = year_of(f)
        if y:
            out.append((y, os.path.join(d, f)))
    return out


def npages(pdf):
    try:
        r = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True, timeout=60)
        m = re.search(r"Pages:\s+(\d+)", r.stdout)
        return int(m.group(1)) if m else 0
    except Exception:
        return 0


def ocr_page(pdf, page, tmp, lang="eng", dpi=200, timeout=600):
    """One page, rendered then read. A page that will not read in time is SKIPPED
    and reported, never silently treated as a page with no note on it: the Arabic
    model is several times slower than the English one and a dense scanned table
    can exceed any bound, so the distinction between "read it, no note" and "could
    not read it" has to survive into the record."""
    base = os.path.join(tmp, "p%d" % page)
    subprocess.run(["pdftoppm", "-r", str(dpi), "-f", str(page), "-l", str(page),
                    "-png", pdf, base], capture_output=True, timeout=300)
    png = None
    for cand in ("%s-%d.png" % (base, page), "%s-%02d.png" % (base, page),
                 "%s-%03d.png" % (base, page)):
        if os.path.exists(cand):
            png = cand
            break
    if not png:
        return ""
    try:
        r = subprocess.run(["tesseract", png, "-", "-l", lang], capture_output=True,
                           text=True, timeout=timeout)
        out = r.stdout or ""
    except subprocess.TimeoutExpired:
        out = None                      # not "" — absence, not emptiness
    try:
        os.unlink(png)
    except OSError:
        pass
    return out


def text_layer(pdf):
    """{page: text} from the embedded text layer, or {} if there is none worth reading.

    Reading a text layer is not a shortcut past the protocol's warning about broken
    character maps — it is the FIRST route, and the check on it is the same one the
    OCR route faces: the numbers must foot against the identity the document itself
    supplies. What changes is only which route produced the characters, and that is
    recorded beside the figure so a later reader can tell.
    """
    n = npages(pdf)
    if not n:
        return {}
    try:
        whole = subprocess.run(["pdftotext", pdf, "-"], capture_output=True,
                               text=True, timeout=300).stdout or ""
    except Exception:
        return {}
    if len(whole) < 40 * n:          # a scan yields about one form-feed per page
        return {}
    out = {}
    for pg in range(1, n + 1):
        try:
            t = subprocess.run(["pdftotext", "-f", str(pg), "-l", str(pg), pdf, "-"],
                               capture_output=True, text=True, timeout=120).stdout
        except Exception:
            continue
        if t:
            out[pg] = t
    return out


def scan(pdf, max_pages=None, lang="eng"):
    """Find the note cheaply, then read it properly.

    TWO PASSES, because the two jobs have different requirements. FINDING the page
    needs only the words, which survive a coarse render; READING the figures on it
    needs the resolution, because a share count misread by one digit is a fair
    value wrong by a factor. Rendering every page at reading resolution costs
    several minutes a document under the Arabic model and buys nothing on the
    pages that turn out not to hold the note.
    """
    n = npages(pdf)
    if not n:
        return [], []
    order = list(range(n, 0, -1))
    if max_pages:
        order = order[:max_pages]
    hint = HINTS_AR if lang == "ara" else HINTS
    hits, skipped = [], []
    with tempfile.TemporaryDirectory() as tmp:
        for pg in order:
            coarse = ocr_page(pdf, pg, tmp, lang=lang, dpi=FIND_DPI, timeout=300)
            if coarse is None:
                skipped.append(pg)
                continue
            if not hint.search(coarse):
                continue
            fine = ocr_page(pdf, pg, tmp, lang=lang, dpi=READ_DPI, timeout=900)
            if fine is None:
                skipped.append(pg)
                continue
            hits.append((pg, fine))
            if len(hits) >= 3:
                break
    return hits, skipped


def main(argv):
    ticker = (argv[0] if argv else "PHDC").upper()
    rest = [a for a in argv[1:] if not a.startswith("--")]
    opts = [a for a in argv[1:] if a.startswith("--")]
    years = set(int(y) for y in rest) if rest else None
    lang = LANG.get(ticker, "eng")
    pages_back = 28
    for o in opts:
        if o.startswith("--lang="):
            lang = o.split("=", 1)[1]
        elif o.startswith("--pages="):
            pages_back = int(o.split("=", 1)[1])
    print("reading %s with the %s model, last %d pages of each filing"
          % (ticker, lang, pages_back))
    out = {"ticker": ticker, "read": {}, "unreadable": {}, "method": (
        "pages rendered at 200dpi and read by tesseract, searched from the back of "
        "each document where the notes sit; a year is recorded only where its "
        "numbers foot")}
    for y, pdf in filings(ticker):
        if years and y not in years:
            continue
        pages = text_layer(pdf)
        route, skipped = "text layer", []
        if pages:
            hint = HINTS_AR if lang == "ara" else HINTS
            # No cap on the text route: rendering is what costs, reading is free,
            # and a three-page cap dropped two of six TMGH years whose note sat
            # one hint-matching page further forward.
            hits = [(pg, t) for pg, t in sorted(pages.items(), reverse=True)
                    if hint.search(t)][:12]
        else:
            route = "OCR at %d dpi" % READ_DPI
            hits, skipped = scan(pdf, max_pages=pages_back, lang=lang)
        if not hits:
            out["unreadable"][str(y)] = ("no equity or per-share note found in the "
                                         "last %d pages of %s%s"
                                         % (pages_back, os.path.basename(pdf),
                                            ("; %d page(s) would not read in time: %s"
                                             % (len(skipped), skipped)) if skipped else ""))
            print("  %d  no note found  (%s)" % (y, os.path.basename(pdf)[:52]))
            continue
        out["read"][str(y)] = {
            "file": os.path.basename(pdf),
            "pages": [p for p, _ in hits],
            "text": {str(p): t for p, t in hits},
            "pages_that_would_not_read": skipped,
            "route": route,
        }
        print("  %d  note on page(s) %s  via %s  (%s)"
              % (y, ", ".join(str(p) for p, _ in hits), route,
                 os.path.basename(pdf)[:44]))
    p = os.path.join(HERE, "_shares_ocr_%s.json" % ticker.lower())
    json.dump(out, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("\nwrote %s — %d year(s) with a note, %d without"
          % (os.path.relpath(p, os.path.dirname(ENGINE)),
             len(out["read"]), len(out["unreadable"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


# ---------------------------------------------------------------------------
# Parsing the note into a number that FOOTS
# ---------------------------------------------------------------------------
# The sentence these filings actually use is:
#   "issued and paid in capital amounts to EGP 4 344 640 000 representing
#    2 172 320 000 shares with a par value of EGP 2 per share"
# Three numbers, one identity: capital / par = shares. That identity is the whole
# check. OCR misreads digits in ways that look entirely plausible — a 3 for an 8,
# a lost separator — and the only thing that catches it is arithmetic the document
# supplies itself.
#
# The note also RECITES the company's capital history, one board resolution per
# paragraph, going back years. Those recitals are not the current count and must
# not be read as one, which is why the parser anchors on the CURRENT-capital
# sentence ("issued and paid in/up capital amounts to") and never on a bare
# "representing N shares" anywhere on the page.

CURRENT_CAP = re.compile(
    r"issued\s+and\s+paid[\s\-]*(?:in|up)?\s+capital[^0-9]{0,40}"
    r"([\d][\d\s,\.]{6,})\s*(?:representing|,)?\s*([\d][\d\s,\.]{6,})?\s*shares?"
    r"[^0-9]{0,60}?par\s+value[^0-9]{0,20}([\d][\d\s,\.]{0,12})",
    re.I | re.S)


def _n(s):
    if s is None:
        return None
    s = re.sub(r"[^\d.]", "", s.replace(" ", ""))
    s = s.rstrip(".")
    try:
        return float(s)
    except ValueError:
        return None


def parse_note(text):
    """(shares, capital, par, how) from the CURRENT-capital sentence, or Nones."""
    flat = re.sub(r"\s+", " ", text)
    m = CURRENT_CAP.search(flat)
    if not m:
        return None, None, None, "no current-capital sentence on the page"
    cap, sh, par = _n(m.group(1)), _n(m.group(2)), _n(m.group(3))
    if not (cap and sh and par):
        return None, None, None, "the sentence is there and a number in it did not read"
    return sh, cap, par, "issued-and-paid-in-capital sentence"


def foots(shares, capital, par, tol=1e-6):
    """capital / par must reproduce the stated share count. No tolerance worth the
    name: these are exact figures in the document and a mismatch is an OCR error,
    not a rounding one."""
    if not (shares and capital and par):
        return False, "a figure is missing"
    implied = capital / par
    if abs(implied - shares) <= max(tol * shares, 1.0):
        return True, "capital %.0f / par %.4g = %.0f, matching the stated count" % (
            capital, par, implied)
    return False, ("capital %.0f / par %.4g = %.0f against a stated %.0f — the "
                   "document does not foot against itself, so this is an OCR "
                   "misread and the year is dropped"
                   % (capital, par, implied, shares))


def parse_all(ticker="PHDC"):
    p = os.path.join(HERE, "_shares_ocr_%s.json" % ticker.lower())
    src = json.load(open(p, encoding="utf-8"))
    out = {"ticker": ticker, "shares_mn": {}, "dropped": {},
           "rule": ("recorded only where issued capital divided by par value "
                    "reproduces the share count the same document states")}
    for y, rec in sorted(src.get("read", {}).items()):
        best = None
        for pg, txt in rec["text"].items():
            sh, cap, par, how = parse_note(txt)
            ok, why = foots(sh, cap, par)
            if ok:
                best = {"shares_mn": sh / 1e6, "issued_capital": cap, "par_value": par,
                        "page": int(pg), "file": rec["file"], "check": why,
                        "how": how}
                break
            if best is None:
                best = {"failed": why or how, "page": int(pg), "file": rec["file"]}
        if best and "shares_mn" in best:
            out["shares_mn"][y] = best
            print("  %s  %10.2f mn shares   (%s, p%d)"
                  % (y, best["shares_mn"], best["file"][:34], best["page"]))
        else:
            out["dropped"][y] = best or {"failed": "no note text"}
            print("  %s  DROPPED — %s" % (y, (best or {}).get("failed", "?")[:90]))
    q = os.path.join(HERE, "shares_%s.json" % ticker.lower())
    json.dump(out, open(q, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("\nwrote %s — %d year(s) footed, %d dropped"
          % (os.path.basename(q), len(out["shares_mn"]), len(out["dropped"])))
    return out


# ---------------------------------------------------------------------------
# The capital note as a RECITAL, and the second arbiter that makes it readable
# ---------------------------------------------------------------------------
# TMGH's note is a chronology: one paragraph per general-assembly resolution from
# 2007 to 2011, each stating the capital and share count as they stood AFTER it.
# The anchored parser above is defeated by it — the words "issued and paid-up
# capital amounted to" sit on the FIRST paragraph, whose figure is LE 6,000,000
# in 2007, three orders of magnitude below the capital in force. Reading that as
# the current count would produce a share count wrong by a factor and a fair value
# wrong by the same factor, footing perfectly all the way.
#
# Ordering alone is not a safe rule either: "the largest" fails on the 2010
# capital REDUCTION, and "the last in the document" only works while the recital
# stays chronological, which is a property of a document rather than of a company.
#
# So the recital is read WITH A SECOND ARBITER: the walk-forward has already
# committed a paid-in capital for that year, read from a DIFFERENT document (that
# year's own earnings release) and carrying its own provenance. The triple chosen
# is the one that agrees with it. Two independent sources and one identity — which
# is a stronger check than the anchored route gets, not a weaker one.

# The clause between the capital and its share count is not fixed wording: the
# FY2023 filing writes "LE 20,635,622,860 dividends over 2,063,562,286 shares"
# and the FY2020 one writes "LE 20,635,622,860 par value, LE 10 per share dividend
# over 2,063,562,286 shares" — same resolution, same figures, a printer's
# difference. The gap is therefore permitted and BOUNDED, and the pairing it
# produces is not trusted on the strength of the match: capital / par must
# reproduce the count, which a mis-paired capital and count will not do.
RECITAL = re.compile(
    r"(?:LE|EGP|L\.E\.)\s*([\d][\d,\. ]{6,})\s*(?:.{0,90}?)?"
    # "share" singular is not a typo worth refusing: TMGH's FY2020 filing writes
    # "divided over 1,815,203,550 share of LE 10 par value each" and its FY2023
    # writes "shares". A parser strict about the plural drops a year for a
    # printer's choice, and the identity check is what actually guards the number.
    r"(?:divid\w*|distribut\w*)\s+(?:over|on)\s+([\d][\d,\. ]{6,})\s*shares?",
    re.I | re.S)
PAR = re.compile(
    r"(?:of\s*)?(?:LE|EGP|L\.E\.)\s*([\d][\d,\.]{0,12})\s*(?:\([^)]{0,80}\)\s*)?"
    r"[-\s]*par\s*value", re.I | re.S)


def parse_recital(text):
    """([(capital, shares)], par) — every resolution the note recites, in order."""
    flat = re.sub(r"\s+", " ", text)
    par = None
    m = PAR.search(flat)
    if m:
        par = _n(m.group(1))
    pairs = []
    for m in RECITAL.finditer(flat):
        cap, sh = _n(m.group(1)), _n(m.group(2))
        if cap and sh:
            pairs.append((cap, sh))
    return pairs, par


def committed_capital(ticker):
    """{year: paid-in capital, in the units the run committed} or {}.

    Read from the run's OWN artefacts, so the corroborating figure carries that
    run's provenance rather than this module's opinion.
    """
    d = os.path.join(ENGINE, "%s_walkforward" % ticker.lower())
    out = {}
    for fn in ("panel_annual.json", "bottom_up.json", "panel_export.json",
               "fs_parsed.json"):
        p = os.path.join(d, fn)
        if not os.path.exists(p):
            continue
        try:
            doc = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue

        def walk(node, year):
            if isinstance(node, dict):
                for k, v in node.items():
                    m = re.fullmatch(r"(?:FY)?((?:19|20)\d{2})", str(k))
                    y = int(m.group(1)) if m else year
                    if str(k).lower() in ("paid_capital", "issued_capital",
                                          "paid_up_capital") and year:
                        val = v.get("value") if isinstance(v, dict) else v
                        if isinstance(val, (int, float)) and val > 0:
                            out.setdefault(year, float(val))
                    else:
                        walk(v, y)
            elif isinstance(node, list):
                for v in node[:40]:
                    walk(v, year)

        walk(doc, None)
        if out:
            break
    return out


def _scale_match(cap, target, tol=0.005):
    """Does `cap` agree with `target` at ANY of the units a run might have used?

    A run commits its figures in whatever unit its filings printed — EGP, EGP
    thousand, EGP million — and the note prints full pounds. Matching across the
    three is arithmetic, not a fudge: the tolerance is half a per cent, so a
    genuine disagreement cannot pass as a unit difference.
    """
    for scale in (1.0, 1e3, 1e6):
        if target and abs(cap / scale - target) <= tol * target:
            return scale
    return None


def parse_all_recital(ticker):
    """The recital route: read every triple, keep the one the run corroborates."""
    p = os.path.join(HERE, "_shares_ocr_%s.json" % ticker.lower())
    src = json.load(open(p, encoding="utf-8"))
    committed = committed_capital(ticker)
    out = {"ticker": ticker, "shares_mn": {}, "dropped": {},
           "rule": ("every resolution the capital note recites is read; the one "
                    "kept is the one whose capital agrees with the paid-in capital "
                    "this run committed for that year from a different document, "
                    "and whose capital divided by par reproduces its own share "
                    "count"),
           "corroborating_source": "the run's own committed paid-in capital"}
    for y, rec in sorted(src.get("read", {}).items()):
        target = committed.get(int(y))
        best, why = None, None
        for pg, txt in sorted(rec["text"].items()):
            pairs, par = parse_recital(txt)
            if not pairs:
                why = why or "no capital recital on the page"
                continue
            if not par:
                why = "the recital is there and no par value could be read"
                continue
            for cap, sh in pairs:
                ok, note = foots(sh, cap, par)
                if not ok:
                    continue
                if target is None:
                    why = ("no committed paid-in capital for %s to corroborate "
                           "against, so the recital is not resolved" % y)
                    continue
                scale = _scale_match(cap, target)
                if scale is None:
                    continue
                # THE COUNT COMES FROM THE COMMITTED CAPITAL, NOT THE RECITAL.
                # The recital stops at the last resolution that CHANGED the
                # capital — TMGH's ends in 2011 — so it cannot see a later
                # treasury movement, while the run's committed paid-in capital
                # is that year's own figure and can. The recital's job is to
                # establish the par value and to prove the identity holds; the
                # count is then that year's capital divided by that par.
                own = target * scale / par
                best = {"shares_mn": own / 1e6,
                        "issued_capital": target * scale,
                        "par_value": par, "page": int(pg), "file": rec["file"],
                        "check": note,
                        "how": "par value read from the capital note and footed "
                               "against the recital's own capital and count; the "
                               "count is this year's committed paid-in capital "
                               "(%.6g, unit scale %g) divided by that par"
                               % (target, scale),
                        "recital_count_mn": sh / 1e6,
                        "difference_from_recital_pct":
                            round(100.0 * (own - sh) / sh, 4),
                        "route": rec.get("route", "unknown")}
                break
            if best:
                break
        if best:
            out["shares_mn"][y] = best
            d = best.get("difference_from_recital_pct") or 0.0
            print("  %s  %10.2f mn shares   par %.4g   (%s, p%d)%s"
                  % (y, best["shares_mn"], best["par_value"],
                     best["file"][:34], best["page"],
                     ("   recital %.2f mn, %+.3f%%" % (best["recital_count_mn"], d))
                     if abs(d) > 1e-6 else ""))
        else:
            out["dropped"][y] = {"failed": why or "no footing triple agreed with "
                                                  "the committed paid-in capital"}
            print("  %s  DROPPED — %s" % (y, out["dropped"][y]["failed"][:95]))
    q = os.path.join(HERE, "shares_%s.json" % ticker.lower())
    json.dump(out, open(q, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("\nwrote %s — %d year(s) footed and corroborated, %d dropped"
          % (os.path.basename(q), len(out["shares_mn"]), len(out["dropped"])))
    return out
