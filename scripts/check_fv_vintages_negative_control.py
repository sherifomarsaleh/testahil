"""Negative control for the fair-value vintage gate.

A gate nobody has seen fail is not evidence — and this one guards against a
failure that is INVISIBLE by construction: a stale vintage is a plausible number
in the right place. Every case below is injected into an isolated copy.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, "scripts", "check_fv_vintages.py")
LIVE_DATA = os.path.join(ROOT, "assets", "data.js")
LIVE_ARCH = os.path.join(ROOT, "engine", "fv_vintages.json")

DATA_JS = """
const TICKERS = {
  ALPHA: { code:"EGX:ALPHA", spot: 10, spotDate:"2026-08-01",
           fair: { bear: 8, base: 12, full: 16 } },
  BETA:  { code:"EGX:BETA",  spot: 5,  spotDate:"2026-08-01",
           fair: { bear: 3, base: 4, full: 6 } },
  GAMMA: { code:"EGX:GAMMA", spot: 2,
           hz: { h1:20, h3:63, l1:"1 month" } }
};
"""

ARCHIVE = {
    "series": {
        "ALPHA": [{"source": "reconstructed", "fair": {"bear": 8, "base": 12, "full": 16},
                   "first_seen": "2026-08-01"}],
        "BETA": [{"source": "reconstructed", "fair": {"bear": 3, "base": 4, "full": 6},
                  "first_seen": "2026-08-01"}],
    },
    "reconstruction": {"revisions_walked": 12, "ref": "origin/main",
                       "earliest": "2026-06-01", "latest": "2026-08-01",
                       "shallow_clone": False},
}


def run_case(name, mutate, must_fail, results):
    tmp = tempfile.mkdtemp(prefix="fvv-")
    try:
        os.makedirs(os.path.join(tmp, "assets"))
        os.makedirs(os.path.join(tmp, "engine", "valuation_calibration"))
        os.makedirs(os.path.join(tmp, "scripts"))
        shutil.copy(os.path.join(ROOT, "engine", "valuation_calibration",
                                 "fv_vintages.py"),
                    os.path.join(tmp, "engine", "valuation_calibration",
                                 "fv_vintages.py"))
        shutil.copy(GATE, os.path.join(tmp, "scripts", "check_fv_vintages.py"))
        data, arch = DATA_JS, json.loads(json.dumps(ARCHIVE))
        data, arch = mutate(data, arch)
        if data is not None:
            open(os.path.join(tmp, "assets", "data.js"), "w").write(data)
        if arch is not None:
            json.dump(arch, open(os.path.join(tmp, "engine", "fv_vintages.json"), "w"))
        r = subprocess.run([sys.executable,
                            os.path.join(tmp, "scripts", "check_fv_vintages.py")],
                           capture_output=True, text=True, timeout=300)
        red = r.returncode != 0
        ok = (red == must_fail)
        results.append(ok)
        print("  %-56s %s   exit %d   %s"
              % (name[:56], "ok  " if ok else "MISS", r.returncode,
                 (r.stdout.strip().splitlines() or [""])[-1][:60]))
        if not ok:
            for line in (r.stdout + r.stderr).strip().splitlines()[-6:]:
                print("        " + line[:150])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _stale(d, a):
    a["series"]["ALPHA"][-1]["fair"]["base"] = 9.99
    return d, a


def _drop(d, a):
    del a["series"]["BETA"]
    return d, a


def _nofair(d, a):
    return DATA_JS.replace("fair: { bear: 8, base: 12, full: 16 }", "x: 1") \
                  .replace("fair: { bear: 3, base: 4, full: 6 }", "y: 2"), a


def main():
    print("fair-value vintage gate — negative control")
    res = []

    run_case("a vintage that no longer matches what the site publishes",
             _stale, True, res)
    run_case("a published name with no vintage at all", _drop, True, res)
    run_case("no archive file", lambda d, a: (d, None), True, res)
    run_case("an archive with no reconstruction — never built, or built empty",
             lambda d, a: (d, {"series": a["series"], "reconstruction": {}}), True, res)
    run_case("no data.js", lambda d, a: (None, a), True, res)
    run_case("data.js that will not load", lambda d, a: ("const TICKERS = {", a),
             True, res)
    run_case("data.js loads but no name carries a fair value", _nofair, True, res)

    run_case("CLEAN — archive current with the site, must PASS",
             lambda d, a: (d, a), False, res)
    run_case("CLEAN — a nested hz object is not a ticker, must PASS",
             lambda d, a: (d, a), False, res)
    run_case("CLEAN — an older vintage behind the current one, must PASS",
             lambda d, a: (d, {**a, "series": {
                 **a["series"],
                 "ALPHA": [{"source": "reconstructed",
                            "fair": {"bear": 1, "base": 2, "full": 3},
                            "first_seen": "2026-07-01"}] + a["series"]["ALPHA"]}}),
             False, res)
    run_case("CLEAN — a SHALLOW-clone archive is a stated limit, not a failure",
             lambda d, a: (d, {**a, "reconstruction": {**a["reconstruction"],
                                                       "shallow_clone": True}}),
             False, res)

    print()
    if all(res):
        print("negative control OK — the gate goes red on every injected defect "
              "and stays green on every clean case")
        return 0
    print("NEGATIVE CONTROL FAILED — %d of %d cases came back wrong."
          % (sum(1 for r in res if not r), len(res)))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
