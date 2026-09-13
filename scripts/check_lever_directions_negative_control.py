#!/usr/bin/env python3
"""The lever-direction gate must fire on every shape it claims to catch, and on nothing else.

Every FAILING case here is a construction that actually shipped on the live site.
Every CLEAN case is one a careless version of this gate would have called wrong --
above all the CBE-EASING family, where the slider runs from today's money to a LOWER
rate, so a POSITIVE impact is correct. Five pages carry that lever. A gate that
matched on the lever's NAME instead of reading the rate off its own labels would have
reported all five as inverted, which is the permanently-red check [R-ENF-02] forbids.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join("scripts", "check_lever_directions.py")

PAGE = """<!doctype html><html><head><title>%s</title></head><body>
<div id="fl-lever-card"></div>
<script>
(function(){
  renderFairLevers("fl-lever-card", T, [
%s
]);
})();
</script>
</body></html>
"""

# name, min, max, def, impact, lo, hi   -- rendered with double quotes
DQ = ('  {{ name:"{0}", min:{1}, max:{2}, step:0.01, def:{3}, impact:{4},\n'
      '    lo:"{5}", hi:"{6}",\n    fmt:v=>v.toFixed(2) }}')
# the same, single-quoted: the syntax that made a first cut of this gate blind to
# 72 of the 93 panels on the book
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


def build(root, pages, outstanding=()):
    os.makedirs(os.path.join(root, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(root, "engine", "build_depth_audit"), exist_ok=True)
    shutil.copy(os.path.join(ROOT, GATE), os.path.join(root, GATE))
    json.dump({"why": "negative control", "adopted": "2026-09-13",
               "outstanding": list(outstanding)},
              open(os.path.join(root, "engine", "build_depth_audit", "lever_outstanding.json"),
                   "w", encoding="utf-8"), indent=1)
    for tk, levers in pages.items():
        d = os.path.join(root, tk, "study")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as fh:
            fh.write(PAGE % (tk, ",\n".join(levers)))


def run(root):
    p = subprocess.run([sys.executable, GATE], cwd=root, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


CASES = [
    ("an inverted BETA lever FAILS and is named",
     {"ADNOCLS": [INVERTED_BETA]}, (), True, "Beta"),
    ("an inverted NUMERIC rate lever FAILS",
     {"MODON": [INVERTED_TERMINAL]}, (), True, "Terminal cost of capital"),
    ("an inverted WORDED rate lever FAILS",
     {"FWRY": [INVERTED_WORDED]}, (), True, "CBE rate path"),
    ("an inverted EASING lever FAILS (the direction is read, not assumed)",
     {"ARCC": [INVERTED_EASING]}, (), True, "CBE easing"),
    ("a lever with impact exactly 0 FAILS",
     {"ELEC": [INERT]}, (), True, "inert lever"),
    ("a rate lever whose labels say neither a rate nor a direction FAILS",
     {"CLHO": [UNREADABLE]}, (), True, "unverifiable"),
    ("CLEAN: a CBE-easing lever with POSITIVE impact does not fire",
     {"ARCC": [CLEAN_EASING]}, (), False, None),
    ("CLEAN: a beta lever whose hi label says '90% interval' does not fire",
     {"ADNOCLS": [CLEAN_BETA]}, (), False, None),
    ("CLEAN: a worded rate lever pointing the right way does not fire",
     {"FWRY": [CLEAN_WORDED]}, (), False, None),
    ("CLEAN: an operating lever with positive impact does not fire",
     {"SAVOLA": [CLEAN_OPERATING]}, (), False, None),
    ("CLEAN: single-quoted and double-quoted panels are both read",
     {"FWRY": [CLEAN_WORDED], "ADNOCLS": [CLEAN_BETA, CLEAN_OPERATING]}, (), False, None),
    ("a listed lever is allowed to fail",
     {"CLHO": [UNREADABLE]}, ("CLHO/study/index.html::CBE facility-cost path (WACC glide)",),
     False, None),
    ("a listed lever does NOT excuse a different one on the same page",
     {"CLHO": [UNREADABLE, INVERTED_BETA]},
     ("CLHO/study/index.html::CBE facility-cost path (WACC glide)",), True, "Beta"),
]


def main():
    bad = 0
    for title, pages, outstanding, want_fail, needle in CASES:
        tmp = tempfile.mkdtemp(prefix="nclev")
        try:
            build(tmp, pages, outstanding)
            rc, out = run(tmp)
            ok = (rc != 0) == want_fail
            if ok and needle:
                ok = needle in out
            print("%-4s %s" % ("PASS" if ok else "FAIL", title))
            if not ok:
                print("       rc=%d\n%s" % (rc, "\n".join("       " + l for l in out.splitlines()[:14])))
            bad += 0 if ok else 1
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # an empty population is a broken gate, not a clean book [R-ENF-04]
    tmp = tempfile.mkdtemp(prefix="nclev")
    try:
        build(tmp, {})
        rc, out = run(tmp)
        ok = rc != 0 and "examined no pages" in out
        print("%-4s a run that examines no page at all FAILS [R-ENF-04]" % ("PASS" if ok else "FAIL"))
        bad += 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # a panel that cannot be parsed must never read as clean
    tmp = tempfile.mkdtemp(prefix="nclev")
    try:
        build(tmp, {"ADNOCLS": [CLEAN_BETA]})
        p = os.path.join(tmp, "ADNOCLS", "study", "index.html")
        src = open(p, encoding="utf-8").read().replace("[\n  { name:", "[\n  ( name:")
        open(p, "w", encoding="utf-8").write(src)
        rc, out = run(tmp)
        ok = rc != 0 and "could not be read" in out
        print("%-4s an unreadable lever panel FAILS rather than being skipped"
              % ("PASS" if ok else "FAIL"))
        bad += 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    total = len(CASES) + 2
    print("\n%d/%d conditions behaved as specified" % (total - bad, total))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
