#!/usr/bin/env python3
"""[R-CAL-02] / [R-ENF-01] Gate: no skill-verdict vocabulary on a public surface,
and no published band record that disagrees with the live panels.

Checked from OUTSIDE the pages it governs, and it FAILS rather than warns. The
rule this enforces was true and written down before today; what was missing was
anything looking at the pages from outside, which is how riyadhcable.html sat for
weeks claiming 13 resolved windows against a panel holding 10.

Run:  python3 scripts/check_band_vocabulary.py
"""
import glob
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import band_record as br  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Verdict vocabulary. Banned everywhere a reader can see it.
# PARITY is matched CASE-SENSITIVELY in caps: the verdict was always written that
# way, while lowercase "parity" is an ordinary English word this book uses in two
# unrelated senses — a currency peg ("the riyal's fixed parity to the dollar") and
# an export price basis. A case-insensitive ban flagged five such lines and would
# have trained everyone to ignore the check, which is the failure mode [R-ENF-02]
# calls a permanently red check.
BANNED_CASE_SENSITIVE = [
    (r"\bPARITY\b", "PARITY"),
    (r"\bROBUST FAIL\b", "ROBUST FAIL"),
]
BANNED = [
    (r"matches benchmark", "matches benchmark"),
    (r"failed calibration", "failed calibration"),
    (r"BOUNDARY\s*\(PARITY", "BOUNDARY(PARITY)"),
    (r"no single-name edge", "no single-name edge"),
    (r"calibration (?:test |gate )?(?:FAILS?|PASSES?)\b", "calibration PASS/FAIL"),
    (r"skill-validated", "skill-validated"),
]
# CRPS is a legitimate methodology explanation on method.html and nowhere else:
# naming the scoring rule where it is being taught is transparency; naming it
# beside a company is the verdict wearing a different hat.
CRPS_OK = {"method.html"}

# Files a reader actually receives.
def surfaces():
    for f in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        yield f
    for f in ["assets/coverage.js", "assets/app.js"]:
        yield os.path.join(ROOT, f)


def strip_comments(src, path):
    """Ledger provenance comments record the INTERNAL verdict and are meant to.
    Only rendered text is in scope."""
    if path.endswith(".js"):
        src = re.sub(r"^\s*//.*$", "", src, flags=re.M)
    else:
        # An HTML page carries its own <script>/<style> comments, and those are
        # code commentary, not text a reader is shown.
        src = re.sub(r"^\s*//.*$", "", src, flags=re.M)
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    src = re.sub(r"<!--.*?-->", "", src, flags=re.S)
    return src


def main():
    fails = []

    # ---- 1. vocabulary ------------------------------------------------------
    for path in surfaces():
        rel = os.path.relpath(path, ROOT)
        text = strip_comments(open(path, encoding="utf-8").read(), path)
        for pat, label in BANNED_CASE_SENSITIVE:
            for m in re.finditer(pat, text):
                line = text[:m.start()].count("\n") + 1
                fails.append(f"{rel}:{line}: verdict vocabulary {label!r}")
        for pat, label in BANNED:
            for m in re.finditer(pat, text, re.I):
                line = text[:m.start()].count("\n") + 1
                fails.append(f"{rel}:{line}: verdict vocabulary {label!r}")
        if rel not in CRPS_OK:
            for m in re.finditer(r"\bCRPS\b", text):
                line = text[:m.start()].count("\n") + 1
                fails.append(f"{rel}:{line}: 'CRPS' outside the methodology page")

    # ---- 2. published records match the live panels -------------------------
    out = subprocess.run([sys.executable,
                          os.path.join(ROOT, "scripts", "build_band_records.py")],
                         capture_output=True, text=True)
    if out.returncode != 0:
        fails.append(f"build_band_records.py failed: {out.stderr.strip()[:400]}")
    else:
        data = open(os.path.join(ROOT, "assets", "data.js"), encoding="utf-8").read()
        recs = br.by_key()
        for name, key in list(br.LEDGER_ALIAS.items()) + []:
            pass
        for m in re.finditer(r'^  ("?)([A-Za-z0-9_$]+)\1: \{mkt:"([A-Z]+)", n:(\d+), '
                             r'hits:(\d+), c50:([\d.]+), c80:([\d.]+), c90:([\d.]+|null), '
                             r'strength:"([a-z-]+)", flag:(null|"[a-z]+")\}', data, re.M):
            tk, mkt, n, hits = m.group(2), m.group(3), int(m.group(4)), int(m.group(5))
            try:
                r = br.resolve(tk, recs)
            except KeyError as e:
                fails.append(f"data.js BANDS.{tk}: {e}")
                continue
            if (r.market, r.n, r.hits) != (mkt, n, hits):
                fails.append(f"data.js BANDS.{tk}: published {mkt}/{n}/{hits}, "
                             f"panel says {r.market}/{r.n}/{r.hits} — re-run "
                             f"scripts/build_band_records.py --write")

    # ---- 3. every data-band-record span names a real record -----------------
    recs = br.by_key()
    for path in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        rel = os.path.relpath(path, ROOT)
        for m in re.finditer(r'data-band-record="([^"]+)"',
                             open(path, encoding="utf-8").read()):
            try:
                br.resolve(m.group(1), recs)
            except KeyError:
                fails.append(f"{rel}: data-band-record=\"{m.group(1)}\" has no panel")

    if fails:
        print(f"[R-CAL-02] FAIL — {len(fails)} problem(s):")
        for f in fails[:60]:
            print("  " + f)
        if len(fails) > 60:
            print(f"  ... and {len(fails) - 60} more")
        return 1
    print("[R-CAL-02] OK — no verdict vocabulary on any public surface; "
          "every published band record agrees with its panel.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
