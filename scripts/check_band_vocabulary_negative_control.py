#!/usr/bin/env python3
"""Negative control for [R-CAL-02]'s gate: prove it catches the real defect.

A check nobody has seen fail is not evidence. This reinjects the exact text the
site carried on 24-Aug-2026 -- and a band record deliberately disagreeing with
its panel -- into throwaway copies, and asserts the gate goes red on each. If any
case passes, the gate is asleep and this exits nonzero.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CASES = [
    ("the FAIL banner", "ledger.html",
     lambda s: s.replace("</body>",
                         '<p>⚠ INDICATIVE ONLY · FAILED CALIBRATION TEST</p></body>', 1)),
    ("a PARITY verdict in a thesis", "assets/coverage.js",
     lambda s: s.replace("const COVERAGE_EN = [",
                         'const X = "\\u00a73 The calibration is PARITY, not skill.";\n'
                         'const COVERAGE_EN = [', 1)),
    ("a matches-benchmark chip", "method.html",
     lambda s: s.replace("</body>", "<p>◆ Indicative · matches benchmark</p></body>", 1)),
    ("CRPS beside a company", "savola.html",
     lambda s: s.replace("</body>", "<p>SAVOLA scored +0.9% CRPS skill.</p></body>", 1)),
    ("a band record that disagrees with its panel", "assets/data.js",
     lambda s: re.sub(r'(  SAVOLA: \{mkt:"SA", n:)\d+', r'\g<1>999', s, count=1)),
]


def main():
    failures = []
    for label, rel, mutate in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            work = os.path.join(tmp, "repo")
            shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns(
                ".git", "__pycache__", "node_modules", "*.png", "*.xlsx", "*.docx", "*.pdf"))
            path = os.path.join(work, rel)
            src = open(path, encoding="utf-8").read()
            out = mutate(src)
            if out == src:
                failures.append(f"{label}: could not inject into {rel} — control is stale")
                continue
            open(path, "w", encoding="utf-8").write(out)
            r = subprocess.run([sys.executable,
                                os.path.join(work, "scripts", "check_band_vocabulary.py")],
                               capture_output=True, text=True, cwd=work)
            if r.returncode == 0:
                failures.append(f"{label}: gate PASSED on injected defect in {rel}")
            else:
                print(f"  caught: {label}  ({rel})")

    if failures:
        print("NEGATIVE CONTROL FAILED:")
        for f in failures:
            print("  " + f)
        return 1
    print(f"negative control OK — the gate caught all {len(CASES)} injected defects")
    return 0


if __name__ == "__main__":
    sys.exit(main())
