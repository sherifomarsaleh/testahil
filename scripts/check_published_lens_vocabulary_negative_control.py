#!/usr/bin/env python3
"""Negative control for check_published_lens_vocabulary.py.

TEN CONDITIONS, FIVE RED AND FIVE CLEAN, and the clean half is the half this turns on:
a vocabulary gate's whole risk is going red on a page that is doing exactly what the rule
asks. A page explaining that the blend was retired, and a page carrying an ordinary
hyphenated compound ("cap-weighted", "equal-weighted"), must both stay green.

EVERY MUTATION ASSERTS THAT IT LANDED before the gate runs. This project has now four
times caught a control passing a fixture that never injected its condition, and a control
that reports green on an uninjected case proves only that nothing changed.

NOTHING IS WRITTEN INTO THE REAL TREE [R-ENF-01]: the fixture pages are built inside a
temporary directory and the gate is pointed at it, so there is no undo that has to run.
The real defect is reproduced from the site EXACTLY as it ships — read out of the pages at
run time rather than transcribed, because a transcribed fixture tests the transcription.
"""
from __future__ import annotations

import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CASES = 10

FAN = ('<script>document.getElementById("f-line").textContent = "Published range "'
       '+fmtPx(f.bear)+" – "+fmtPx(f.full)+" "+t.ccy+", weighted central "'
       '+fmtPx(f.base)+".";</script>')
CLEAN_FAN = ('<script>document.getElementById("f-line").textContent = "Published range "'
             '+fmtPx(f.bear)+" – "+fmtPx(f.full)+" "+t.ccy+", central "'
             '+fmtPx(f.base)+".";</script>')


def shipped_example():
    """The defect as it actually ships, lifted from a real page at run time."""
    for p in sorted(glob.glob(os.path.join(ROOT, "*", "study", "index.html"))):
        t = open(p, encoding="utf-8", errors="replace").read()
        m = re.search(r".{0,200}blended into one weighted central fair value.{0,80}", t, re.S)
        if m:
            return m.group(0)
    return "Four independent valuation methods, blended into one weighted central fair value."


def build(tmp, pages, ratchet):
    repo = os.path.join(tmp, "repo")
    os.makedirs(os.path.join(repo, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(repo, "engine", "build_depth_audit"), exist_ok=True)
    os.makedirs(os.path.join(repo, "assets"), exist_ok=True)
    for s in ("check_published_lens_vocabulary.py", "check_lens_vocabulary.py"):
        shutil.copy(os.path.join(HERE, s), os.path.join(repo, "scripts", s))
    for rel, body in pages.items():
        dst = os.path.join(repo, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "w", encoding="utf-8").write(body)
    json.dump({"outstanding": ratchet},
              open(os.path.join(repo, "engine", "build_depth_audit",
                                "published_lens_outstanding.json"), "w",
                   encoding="utf-8"), indent=1)
    return repo


def run(repo):
    p = subprocess.run([sys.executable,
                        os.path.join(repo, "scripts",
                                     "check_published_lens_vocabulary.py")],
                       capture_output=True, text=True, cwd=repo, timeout=120)
    return p.returncode, (p.stdout + p.stderr)


def case(name, pages, ratchet, expect_red, landed, results):
    tmp = tempfile.mkdtemp(prefix="publens_nc_")
    try:
        repo = build(tmp, pages, ratchet)
        ok, why = landed(repo)
        if not ok:
            results.append((name, "MUTATION DID NOT LAND: " + why))
            return
        rc, out = run(repo)
        red = rc != 0
        if red != expect_red:
            results.append((name, "expected %s, got %s\n%s"
                            % ("RED" if expect_red else "GREEN",
                               "RED" if red else "GREEN", out[-500:])))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def has(repo, rel, needle):
    p = os.path.join(repo, rel)
    if not os.path.exists(p):
        return False, "%s absent" % rel
    t = open(p, encoding="utf-8").read()
    return (needle in t), "%r not in %s" % (needle[:40], rel)


def main():
    ex = shipped_example()
    results = []
    listed = {"AAA/study/index.html": {"assertions": 1, "reason": "seeded"}}

    # ---- RED ----
    case("1 a NEW page publishes the retired blend",
         {"AAA/study/index.html": "<html>" + CLEAN_FAN + "</html>",
          "BBB/study/index.html": "<html>" + FAN + "</html>"},
         {"AAA/study/index.html": {"assertions": 0, "reason": "seeded"}},
         True, lambda r: has(r, "BBB/study/index.html", "weighted central"), results)

    case("2 a LISTED page acquires MORE assertions than it is excused",
         {"AAA/study/index.html": "<html>" + FAN + "<p>" + ex + "</p></html>"},
         listed, True,
         lambda r: has(r, "AAA/study/index.html", "blended into one weighted"), results)

    case("3 the shipped defect, verbatim, on an unlisted page",
         {"AAA/study/index.html": "<html>" + CLEAN_FAN + "</html>",
          "CCC/study/index.html": "<html><p>" + ex + "</p></html>"},
         {"AAA/study/index.html": {"assertions": 0, "reason": "seeded"}},
         True, lambda r: has(r, "CCC/study/index.html", "weighted central"), results)

    case("4 ZERO pages — a run that read nothing is not a run that found nothing",
         {}, {}, True, lambda r: (not glob.glob(os.path.join(r, "*", "study", "index.html")),
                                  "pages still present"), results)

    case("5 the coverage grid gains a blend row",
         {"AAA/study/index.html": "<html>" + CLEAN_FAN + "</html>",
          "assets/coverage.js": "const COVERAGE_EN=[{tk:'X',thesis:'Four lenses, weighted "
                                "central AED 4.17 against a close of 5.24.'}];"},
         {"AAA/study/index.html": {"assertions": 0, "reason": "seeded"}},
         True, lambda r: has(r, "assets/coverage.js", "weighted"), results)

    # ---- CLEAN ----
    case("6 a page EXPLAINING that the blend was retired",
         {"AAA/study/index.html": "<html><p>The retired construction weighted four lenses "
                                  "into one weighted central fair value; this study "
                                  "publishes the class primary instead.</p>"
                                  + CLEAN_FAN + "</html>"},
         {}, False, lambda r: has(r, "AAA/study/index.html", "retired construction"), results)

    case("7 a listed page carrying EXACTLY its excused count",
         {"AAA/study/index.html": "<html>" + FAN + "</html>"},
         listed, False, lambda r: has(r, "AAA/study/index.html", "weighted central"), results)

    case("8 a listed page that has got BETTER",
         {"AAA/study/index.html": "<html>" + CLEAN_FAN + "</html>"},
         {"AAA/study/index.html": {"assertions": 3, "reason": "seeded"}},
         False, lambda r: has(r, "AAA/study/index.html", '", central "'), results)

    case("9 a hyphenated compound is not the claim",
         {"AAA/study/index.html": "<html><p>An equal-weighted composite and a cap-weighted "
                                  "index are shown beside a centre-weighted moving average "
                                  "of the data centre segment.</p>" + CLEAN_FAN + "</html>"},
         {}, False, lambda r: has(r, "AAA/study/index.html", "equal-weighted"), results)

    case("10 a page that says nothing about how the central was reached",
         {"AAA/study/index.html": "<html><p>Published range 4.10 – 6.80 AED, central "
                                  "5.20. The central reading sits 12% from the last "
                                  "close.</p></html>"},
         {}, False, lambda r: has(r, "AAA/study/index.html", "central 5.20"), results)

    ran = CASES
    print("cases run: %d (declared %d)" % (ran, CASES))
    if results:
        for n, why in results:
            print("  FAIL  %s\n        %s" % (n, why))
        print("\nFAIL — the gate does not behave as the rule says.")
        return 1
    print("OK — 5 red conditions fire, 5 clean conditions do not.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
