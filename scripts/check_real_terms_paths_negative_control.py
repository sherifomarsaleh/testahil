"""Negative control for check_real_terms_paths.  [R-REAL-01]

Every condition the gate refuses, reinjected, and every clean case it must not fire on.
EVERY MUTATION ASSERTS THAT IT LANDED and the case COUNT is asserted against a declared
constant, because this repository has five times caught a control passing a fixture that
never injected its condition and reporting green on nothing.

THE CLEAN HALF IS WHERE THIS GATE CAN DO REAL DAMAGE. It reads per-unit money paths out of
a register that also holds volumes, margins and utilisation rates, and it compares them
against an inflation ladder that is wrong for a price set in another currency. Both
mistakes were MADE by the first two drafts and both are kept here as cases: a volume path
must not fire however fast it moves, and a dollar price growing 1% a year must be measured
against long-run foreign inflation (-7.1% real) and NOT against a 16% domestic ladder,
which reported it as a 35.5% collapse and would have condemned correct work.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "engine"))
import sandbox_reclaim as SBX       # noqa: E402

RED_EXPECTED = 9
CLEAN_EXPECTED = 5

GOOD_ENTRY = {
    "kind": "nominal_rate",
    "real_change": -0.1591,
    "mechanism": "administered_price",
    "disclosure": "the Egyptian Drug Authority sets the ceiling price and adjusts it in "
                  "periodic approved steps; note 3 to the FY2025 accounts states the "
                  "latest approved adjustment and its date",
}
# The measured real change of this path against the EG ladder, to four places. Written
# here as the CASE'S OWN ARITHMETIC rather than copied from the gate, so a change in
# either is visible as a disagreement between two independent statements of it.
PHAR_PATH = [0.05, 0.080, 0.075, 0.065, 0.055]


def _numbers(market_ticker, inputs, block=None):
    doc = {"market": market_ticker, "inputs": inputs}
    if block is not None:
        doc["real_terms_block"] = block
    return doc


def _sandbox(studies, ratchet=None):
    tmp = SBX.make("realterms_nc_")
    eng = os.path.join(tmp, "engine")
    os.makedirs(os.path.join(eng, "build_depth_audit"))
    for n in ("real_terms.py", "macro_path.py", "site_data.py", "sandbox_reclaim.py"):
        shutil.copy(os.path.join(ROOT, "engine", n), os.path.join(eng, n))
    shutil.copytree(os.path.join(ROOT, "engine", "macro_paths"),
                    os.path.join(eng, "macro_paths"))
    os.makedirs(os.path.join(tmp, "scripts"))
    shutil.copy(os.path.join(HERE, "check_real_terms_paths.py"),
                os.path.join(tmp, "scripts", "check_real_terms_paths.py"))
    for tk, doc in studies.items():
        d = os.path.join(eng, "%s_study" % tk.lower())
        os.makedirs(d)
        json.dump(doc, open(os.path.join(d, "study_numbers.json"), "w"))
    json.dump({"rule": "nc", "measurements": ratchet or {},
               "outstanding": sorted(ratchet or {})},
              open(os.path.join(eng, "build_depth_audit",
                                "real_terms_outstanding.json"), "w"))
    return tmp


def _run(tmp):
    r = subprocess.run([sys.executable,
                        os.path.join(tmp, "scripts", "check_real_terms_paths.py")],
                       capture_output=True, text=True, timeout=600, cwd=tmp)
    return r.returncode, r.stdout + r.stderr


def case(name, studies, want_red, landed, results, ratchet=None):
    tmp = _sandbox(studies, ratchet)
    try:
        ok_land, why = landed(tmp)
        if not ok_land:
            print("  MISS  %-58s FIXTURE DID NOT LAND: %s" % (name[:58], why))
            results.append(False)
            return
        rc, out = _run(tmp)
        red = rc != 0
        ok = (red == want_red)
        results.append(ok)
        print("  %-5s %-58s %s" % ("ok" if ok else "MISS", name[:58],
                                   "RED" if red else "green"))
        if not ok:
            for l in out.strip().splitlines()[-5:]:
                print("        " + l[:140])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    print("NEGATIVE CONTROL - check_real_terms_paths  [R-REAL-01]")
    print("   %d conditions that must go RED, %d that must stay GREEN"
          % (RED_EXPECTED, CLEAN_EXPECTED))
    res = []

    def has(tmp, tk, needle):
        p = os.path.join(tmp, "engine", "%s_study" % tk.lower(), "study_numbers.json")
        if not os.path.exists(p):
            return False, "no numbers file for %s" % tk
        return (needle in open(p).read()), "%s not present in %s" % (needle, tk)

    # ---------------------------------------------------------------- RED
    case("a material real fall, declared nowhere",
         {"AAA": _numbers("EG", {"dom_price_growth": {"value": PHAR_PATH}})},
         True, lambda t: has(t, "AAA", "dom_price_growth"), res)

    bad_number = dict(GOOD_ENTRY, real_change=-0.02)
    case("declared, and the stated real change does not reproduce",
         {"BBB": _numbers("EG", {"dom_price_growth": {"value": PHAR_PATH}},
                          {"paths": {"dom_price_growth": bad_number}})},
         True, lambda t: has(t, "BBB", "-0.02"), res)

    off_list = dict(GOOD_ENTRY, mechanism="the path looked about right")
    case("a mechanism off the closed list",
         {"CCC": _numbers("EG", {"dom_price_growth": {"value": PHAR_PATH}},
                          {"paths": {"dom_price_growth": off_list}})},
         True, lambda t: has(t, "CCC", "looked about right"), res)

    no_disc = dict(GOOD_ENTRY, disclosure="   ")
    case("a mechanism named with no disclosure behind it",
         {"DDD": _numbers("EG", {"dom_price_growth": {"value": PHAR_PATH}},
                          {"paths": {"dom_price_growth": no_disc}})},
         True, lambda t: has(t, "DDD", "administered_price"), res)

    no_measure = {k: v for k, v in GOOD_ENTRY.items() if k != "real_change"}
    case("declared with no measured real change at all",
         {"EEE": _numbers("EG", {"dom_price_growth": {"value": PHAR_PATH}},
                          {"paths": {"dom_price_growth": no_measure}})},
         True, lambda t: has(t, "EEE", "administered_price"), res)

    case("excluded from the block with an EMPTY reason",
         {"FFF": _numbers("EG", {"dom_price_growth": {"value": PHAR_PATH}},
                          {"not_price_class": {"dom_price_growth": {"reason": "  "}},
                           "paths": {"dom_price_growth": {"kind": "nominal_rate",
                                                          "reason": "  "}}})},
         True, lambda t: has(t, "FFF", "not_price_class"), res)

    case("ZERO register inputs across directories that are present [R-ENF-04]",
         {"GGG": _numbers("EG", {}), "HHH": _numbers("EG", {})},
         True, lambda t: (not json.load(open(os.path.join(
             t, "engine", "ggg_study", "study_numbers.json")))["inputs"],
             "the register is not empty"), res)

    case("a ratchet entry that has stopped breaching [R-ENF-02]",
         {"III": _numbers("EG", {"dom_price_growth": {"value": PHAR_PATH}},
                          {"paths": {"dom_price_growth": GOOD_ENTRY}})},
         True, lambda t: has(t, "III", "administered_price"), res,
         ratchet={"III": "seeded, and this study now conforms"})

    # ---------------------------------------------------------------- CLEAN
    case("CLEAN - declared with its mechanism, disclosure and measurement",
         {"JJJ": _numbers("EG", {"dom_price_growth": {"value": PHAR_PATH}},
                          {"paths": {"dom_price_growth": GOOD_ENTRY}})},
         False, lambda t: has(t, "JJJ", "administered_price"), res)

    case("CLEAN - a real move INSIDE the 5% line says nothing",
         {"KKK": _numbers("EG", {"dom_price_growth":
                                 {"value": [0.16, 0.12, 0.09, 0.075, 0.07]}})},
         False, lambda t: has(t, "KKK", "0.16"), res)

    case("CLEAN - a VOLUME path, however fast, is not a price",
         {"LLL": _numbers("EG", {"dom_pack_growth": {"value": [0.5, 0.5, 0.5, 0.5, 0.5]}})},
         False, lambda t: has(t, "LLL", "dom_pack_growth"), res)

    # THE PAIR THAT PROVES THE BASIS, and the first draft of this control got the first
    # one wrong in a way worth keeping. A dollar price at 1% a year IS material on the
    # right basis -- -5.7% against long-run foreign inflation over four years -- so it
    # must fire, and the NUMBER is the evidence: on the domestic ladder the same path
    # reads -35.5%, which is what the gate's own first draft printed and what would have
    # condemned work that is right. The case was written expecting green, the gate
    # disagreed, and the gate was correct.
    case("a dollar price at 1%/yr IS material on the foreign basis",
         {"MMM": _numbers("EG", {"exp_price_usd_growth":
                                 {"value": [0.01, 0.01, 0.01, 0.01]}})},
         True, lambda t: has(t, "MMM", "exp_price_usd"), res)

    # THE DISCRIMINATOR. At 2.2% a year against 2.5% long-run foreign inflation this is
    # -1.2% real and must stay GREEN; measured against the 16/12/9/7.5 domestic ladder the
    # SAME path reads -28.3% and would be red. One fixture, two bases, opposite verdicts --
    # so this case fails the moment the currency basis stops being read.
    case("CLEAN - a dollar price at 2.2%/yr, immaterial on the RIGHT basis",
         {"PPP": _numbers("EG", {"exp_price_usd_growth":
                                 {"value": [0.022, 0.022, 0.022, 0.022]}})},
         False, lambda t: has(t, "PPP", "exp_price_usd"), res)

    case("CLEAN - a breach that IS on the ratchet stays green",
         {"NNN": _numbers("EG", {"dom_price_growth": {"value": PHAR_PATH}})},
         False, lambda t: has(t, "NNN", "dom_price_growth"), res,
         ratchet={"NNN": "dom_price_growth moves -15.9% in REAL terms, seeded"})

    n_red, n_clean = RED_EXPECTED, CLEAN_EXPECTED
    assert len(res) == n_red + n_clean, (
        "cases ran: %d, declared %d. A control that loses a case reports fewer-of-fewer "
        "and reads as clean." % (len(res), n_red + n_clean))
    print("\n%d of %d conditions behaved as the gate claims." % (sum(res), len(res)))
    if all(res):
        print("OK - the gate fires on every injected defect and stays quiet on work that "
              "is right.")
        return 0
    print("FAILED - the gate does not behave as the rule says.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
