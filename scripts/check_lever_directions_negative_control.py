#!/usr/bin/env python3
"""The lever-direction gate must fire on every shape it claims to catch, and on nothing else.

Every FAILING case here is a construction that actually shipped on the live site, or one
the 13-Sep-2026 move of the levers into assets/levers.js made newly possible -- a page
that stops reading that file, or starts carrying a lever of its own again.

Every CLEAN case is one a careless version of this gate would have called wrong, above all
the CBE-EASING family: those sliders run from today's money to a LOWER rate, so a POSITIVE
impact is correct. Five pages carry that lever. A gate matching on the lever's NAME rather
than reading the rate off its own labels would have reported all five as inverted, which is
the permanently-red check [R-ENF-02] forbids.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join("scripts", "check_lever_directions.py")

PAGE = """<!doctype html><html><head><title>%(tk)s</title></head><body>
<div id="fl-lever-card"></div>
%(tags)s
<script>
(function(){ %(call)s })();
</script>
</body></html>
"""
TAGS = '<script src="/assets/data.js"></script>\n<script src="/assets/levers.js"></script>'
CALL = 'renderFairLevers("fl-lever-card", T, (typeof LEVERS!=="undefined"&&LEVERS["%s"])||[]);'

DQ = ('  {{ name:"{0}", min:{1}, max:{2}, step:0.01, def:{3}, impact:{4},\n'
      '    lo:"{5}", hi:"{6}",\n    fmt:v=>v.toFixed(2) }}')
# the single-quoted spelling: the syntax a first cut of this gate could not read, which
# left it blind to 72 of the 93 panels on the book
SQ = ("  {{ name:'{0}', min:{1}, max:{2}, step:0.01, def:{3}, impact:{4},\n"
      "    lo:'{5}', hi:'{6}',\n    fmt:v=>v.toFixed(2) }}")

CLEAN_BETA = DQ.format("Beta \\u2014 how the market is measured", 0.70, 1.62, 1.10, -38.78,
                       "0.71 \\u2014 equal-weight composite of the exchange",
                       "1.62 \\u2014 top of the 90% interval")
INVERTED_BETA = DQ.format("Beta \\u2014 how the market is measured", 0.70, 1.62, 1.10, 34.4,
                          "0.71 \\u2014 equal-weight composite of the exchange",
                          "1.62 \\u2014 top of the 90% interval")
CLEAN_EASING = DQ.format("CBE easing \\u2014 cost of capital", 0, 3, 0, 0.58,
                         "today\\u2019s money (24.52% WACC)", "3pp of easing (21.52%)")
INVERTED_EASING = DQ.format("CBE easing \\u2014 cost of capital", 0, 3, 0, -0.58,
                            "today\\u2019s money (24.52% WACC)", "3pp of easing (21.52%)")
INVERTED_TERMINAL = DQ.format("Terminal cost of capital", -1.0, 1.0, 0, 0.55,
                              "10.9% \\u2014 a maturing, deleveraging developer", "12.9%")
INERT = DQ.format("Net-debt anchor (triangulated, not disclosed)", -685, 555, 0, 0,
                  "low end of the range (9,120)", "high end (10,360)")
UNREADABLE = DQ.format("CBE facility-cost path (WACC glide)", -3, 3, -0.7, 1,
                       "sharp depreciation", "firm / tailwind")
CLEAN_WORDED = SQ.format("CBE rate path \\u2014 impact on the discount rate", -8, 8, 2, 1,
                         "tighter / rate headwind", "easier / rate tailwind")
INVERTED_WORDED = SQ.format("CBE rate path \\u2014 impact on the discount rate", -8, 8, 2, -1,
                            "tighter / rate headwind", "easier / rate tailwind")
CLEAN_OPERATING = DQ.format("Panda store cadence (net new stores a year)", 8, 20, 20, 0.924,
                            "8 \\u2014 the observed H1-2026 run-rate", "20 \\u2014 company guidance")
NO_CAPTION = ('  { name:"Terminal growth", min:1.0, max:2.5, step:0.25, def:2.0, impact:2.72,\n'
              '    lo:"1.0%", hi:"2.5%" }')


def build(root, book, outstanding=(), levers_js=None, page_src=None, extra_pages=None):
    """book: {TICKER: [lever source, ...]}. page_src overrides the page for one ticker.

    extra_pages: {relative path: source} for surfaces that are not TICKER/study/index.html
    -- the legacy site, which carries its own copy of every one of these pages and on
    which all four inverted levers were also live.
    """
    os.makedirs(os.path.join(root, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(root, "assets"), exist_ok=True)
    os.makedirs(os.path.join(root, "engine", "build_depth_audit"), exist_ok=True)
    shutil.copy(os.path.join(ROOT, GATE), os.path.join(root, GATE))
    json.dump({"why": "negative control", "adopted": "2026-09-13",
               "outstanding": list(outstanding)},
              open(os.path.join(root, "engine", "build_depth_audit", "lever_outstanding.json"),
                   "w", encoding="utf-8"), indent=1)
    if levers_js is None:
        body = ",\n".join('"%s": [\n%s\n]' % (tk, ",\n".join(lv)) for tk, lv in book.items())
        levers_js = "const LEVERS = {\n%s\n};\n" % body
    if levers_js is not False:
        open(os.path.join(root, "assets", "levers.js"), "w", encoding="utf-8").write(levers_js)
    for tk in book:
        d = os.path.join(root, tk, "study")
        os.makedirs(d, exist_ok=True)
        src = page_src.get(tk) if page_src else None
        if src is None:
            src = PAGE % {"tk": tk, "tags": TAGS, "call": CALL % tk}
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(src)
    for rel, src in (extra_pages or {}).items():
        f = os.path.join(root, rel)
        os.makedirs(os.path.dirname(f), exist_ok=True)
        open(f, "w", encoding="utf-8").write(src)


def run(root):
    p = subprocess.run([sys.executable, GATE], cwd=root, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


CASES = [
    ("an inverted BETA lever FAILS and is named",
     {"ADNOCLS": [INVERTED_BETA]}, True, "Beta"),
    ("an inverted NUMERIC rate lever FAILS",
     {"MODON": [INVERTED_TERMINAL]}, True, "Terminal cost of capital"),
    ("an inverted WORDED rate lever FAILS",
     {"FWRY": [INVERTED_WORDED]}, True, "CBE rate path"),
    ("an inverted EASING lever FAILS (the direction is read, not assumed)",
     {"ARCC": [INVERTED_EASING]}, True, "CBE easing"),
    ("a lever with impact exactly 0 FAILS",
     {"ELEC": [INERT]}, True, "inert lever"),
    ("a rate lever whose labels say neither a rate nor a direction FAILS",
     {"CLHO": [UNREADABLE]}, True, "unverifiable"),
    ("a lever with no caption at all FAILS",
     {"SAVOLA": [NO_CAPTION]}, True, "no caption"),
    ("CLEAN: a CBE-easing lever with POSITIVE impact does not fire",
     {"ARCC": [CLEAN_EASING]}, False, None),
    ("CLEAN: a beta lever whose hi label says '90% interval' does not fire",
     {"ADNOCLS": [CLEAN_BETA]}, False, None),
    ("CLEAN: a worded rate lever pointing the right way does not fire",
     {"FWRY": [CLEAN_WORDED]}, False, None),
    ("CLEAN: an operating lever with positive impact does not fire",
     {"SAVOLA": [CLEAN_OPERATING]}, False, None),
    ("CLEAN: single-quoted and double-quoted levers are both read",
     {"FWRY": [CLEAN_WORDED], "ADNOCLS": [CLEAN_BETA, CLEAN_OPERATING]}, False, None),
]


def main():
    bad = 0

    def case(title, want_fail, needle, **kw):
        nonlocal bad
        tmp = tempfile.mkdtemp(prefix="nclev")
        try:
            build(tmp, **kw)
            rc, out = run(tmp)
            ok = (rc != 0) == want_fail
            if ok and needle:
                ok = needle in out
            print("%-4s %s" % ("PASS" if ok else "FAIL", title))
            if not ok:
                print("       rc=%d\n%s" % (rc, "\n".join("       " + l
                                                          for l in out.splitlines()[:12])))
            bad += 0 if ok else 1
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    for title, book, want_fail, needle in CASES:
        case(title, want_fail, needle, book=book)

    case("a listed lever is allowed to fail", False, None,
         book={"CLHO": [UNREADABLE]},
         outstanding=("CLHO::CBE facility-cost path (WACC glide)",))
    case("a listed lever does NOT excuse a different one on the same page", True, "Beta",
         book={"CLHO": [UNREADABLE, INVERTED_BETA]},
         outstanding=("CLHO::CBE facility-cost path (WACC glide)",))

    # --- the conditions the 13-Sep-2026 move made possible -------------------------
    case("a page carrying an inline lever array again FAILS", True, "inline lever array",
         book={"ADNOCLS": [CLEAN_BETA]},
         page_src={"ADNOCLS": PAGE % {"tk": "ADNOCLS", "tags": TAGS,
                                      "call": 'renderFairLevers("fl-lever-card", T, [\n'
                                              + CLEAN_BETA + "\n]);"}})
    case("a page that never loads assets/levers.js FAILS", True, "never loads",
         book={"ADNOCLS": [CLEAN_BETA]},
         page_src={"ADNOCLS": PAGE % {"tk": "ADNOCLS",
                                      "tags": '<script src="/assets/data.js"></script>',
                                      "call": CALL % "ADNOCLS"}})
    case("a page loading levers.js AFTER the call FAILS", True, "AFTER",
         book={"ADNOCLS": [CLEAN_BETA]},
         page_src={"ADNOCLS": PAGE % {"tk": "ADNOCLS",
                                      "tags": '<script src="/assets/data.js"></script>',
                                      "call": CALL % "ADNOCLS"}
                   + '<script src="/assets/levers.js"></script>'})
    case("a page reading a LEVERS key the file does not hold FAILS", True, "does not hold",
         book={"ADNOCLS": [CLEAN_BETA]},
         page_src={"ADNOCLS": PAGE % {"tk": "ADNOCLS", "tags": TAGS, "call": CALL % "ADNOCGAS"}})
    case("assets/levers.js missing FAILS", True, "does not exist",
         book={"ADNOCLS": [CLEAN_BETA]}, levers_js=False)
    case("assets/levers.js that does not evaluate FAILS", True, "did not evaluate",
         book={"ADNOCLS": [CLEAN_BETA]}, levers_js="const LEVERS = { oops:: };\n")
    case("assets/levers.js holding no lever at all FAILS [R-ENF-04]", True, "no lever at all",
         book={"ADNOCLS": [CLEAN_BETA]}, levers_js="const LEVERS = {};\n")
    case("a book with no page to hold it against FAILS [R-ENF-04]", True, "no page to hold",
         book={}, levers_js='const LEVERS = {"ADNOCLS": [\n%s\n]};\n' % CLEAN_BETA)

    # --- the legacy site carries its own copy of every one of these pages -----------
    LEGACY_TAGS = ('<script src="assets/data.js"></script>'
                   '<script src="assets/levers.js"></script>')
    case("a LEGACY page carrying an inline lever array FAILS", True, "inline lever array",
         book={"ADNOCLS": [CLEAN_BETA]},
         extra_pages={"legacy/adnocls.html":
                      PAGE % {"tk": "ADNOCLS", "tags": LEGACY_TAGS,
                              "call": 'renderFairLevers("fl-lever-card", T, [\n'
                                      + CLEAN_BETA + "\n]);"}})
    case("a LEGACY page that never loads levers.js FAILS", True, "never loads",
         book={"ADNOCLS": [CLEAN_BETA]},
         extra_pages={"legacy/adnocls.html":
                      PAGE % {"tk": "ADNOCLS",
                              "tags": '<script src="assets/data.js"></script>',
                              "call": CALL % "ADNOCLS"}})
    case("CLEAN: a LEGACY page wired the relative way does not fire", False, None,
         book={"ADNOCLS": [CLEAN_BETA]},
         extra_pages={"legacy/adnocls.html":
                      PAGE % {"tk": "ADNOCLS", "tags": LEGACY_TAGS,
                              "call": CALL % "ADNOCLS"}})

    total = len(CASES) + 13
    print("\n%d/%d conditions behaved as specified" % (total - bad, total))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
