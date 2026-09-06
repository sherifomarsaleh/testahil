"""Negative control for check_macro_anchor_age.py.

A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE. Every case below builds a sandbox, plants one
condition, ASSERTS THE MUTATION LANDED IN THE FILE ON DISK before the gate runs, and requires
the gate to go red or stay green.

The asserted-landing is not ceremony. Four times in this project a negative control has been
caught passing a fixture that never injected its condition — a regex matching nothing, a case
that searched for a quoted key where the file writes them unquoted, three cases silently
deleted — and each time the green proved only that the file was unchanged.

THE CLEAN CASES ARE THE HALF THAT MATTERS HERE, because this gate's whole design risk is
firing where no defect exists: a pegged market is struck 246 days after its anchor and MUST
NOT fire, since the anchor is the peg.
"""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import check_macro_anchor_age as G                                      # noqa: E402

CASES = []


def case(name, red, build):
    CASES.append((name, red, build))


def _mk(paths, studies, ratchet=None):
    """paths: {mkt: (regime, fx_date)}; studies: {tk: (spot_date, currency, accepted)}"""
    d = tempfile.mkdtemp()
    eng = os.path.join(d, "engine")
    os.makedirs(os.path.join(eng, "macro_paths"))
    os.makedirs(os.path.join(eng, "build_depth_audit"))
    for mkt, (regime, fxd) in paths.items():
        json.dump({"market": mkt, "regime": regime,
                   "fx": {"spot": {"value": 1.0, "date": fxd}}},
                  open(os.path.join(eng, "macro_paths", "%s.json" % mkt), "w",
                       encoding="utf-8"), indent=1)
    for tk, (sd, cur, acc) in studies.items():
        sdir = os.path.join(eng, "%s_study" % tk.lower())
        os.makedirs(sdir)
        rec = {"meta": {"spot_date": sd, "currency": cur}}
        if acc is not None:
            rec["anchor_staleness_accepted"] = acc
        json.dump(rec, open(os.path.join(sdir, "study_numbers.json"), "w",
                            encoding="utf-8"), indent=1)
    json.dump({"outstanding": ratchet or {}},
              open(os.path.join(eng, "build_depth_audit",
                                "anchor_age_outstanding.json"), "w",
                   encoding="utf-8"), indent=1)
    return d, eng


# ---- the condition the rule exists for, exactly as it stands on 6 September ----------
case("a transition market struck 28 days after its own currency anchor — AMOC's shape", True,
     lambda: _mk({"EG": ("transition", "2026-08-06")},
                 {"AMOC": ("2026-09-03", "EGP", None)}))
case("the same study one day inside the 14-day bound", False,
     lambda: _mk({"EG": ("transition", "2026-08-06")},
                 {"AMOC": ("2026-08-19", "EGP", None)}))
case("exactly on the bound — 14 days, which must NOT fire", False,
     lambda: _mk({"EG": ("transition", "2026-08-06")},
                 {"AMOC": ("2026-08-20", "EGP", None)}))
case("one day past the bound", True,
     lambda: _mk({"EG": ("transition", "2026-08-06")},
                 {"AMOC": ("2026-08-21", "EGP", None)}))
case("a MATURE market struck long after its anchor — floating, so it fires", True,
     lambda: _mk({"US": ("mature", "2025-12-31")},
                 {"AAPL": ("2026-09-03", "USD", None)}))

# ---- THE CLEAN CASE THIS GATE IS MOST AT RISK OF GETTING WRONG -----------------------
case("a PEGGED market struck 246 days after its anchor — the anchor IS the peg, and firing "
     "here would overstate the finding threefold", False,
     lambda: _mk({"AE": ("pegged", "2025-12-31")},
                 {"AIRARABIA": ("2026-09-03", "AED", None)}))
case("three pegged studies at 219-246 days, none of which may fire", False,
     lambda: _mk({"AE": ("pegged", "2025-12-31"), "SA": ("pegged", "2025-12-31")},
                 {"DU": ("2026-09-03", "AED", None),
                  "MODON": ("2026-08-07", "AED", None),
                  "SAVOLA": ("2026-09-03", "SAR", None)}))

# ---- the release, and the way a release is normally defeated -------------------------
case("a breach DECLARED and REASONED — deliberate acceptance, as a stale sovereign quote "
     "may be", False,
     lambda: _mk({"EG": ("transition", "2026-08-06")},
                 {"AMOC": ("2026-09-03", "EGP",
                           {"reason": "the pound has not moved outside its quoted range "
                                      "since the anchor and the path is refreshed at the "
                                      "next refit"})}))
case("a breach declared with an EMPTY reason — switching the check off, not declaring it",
     True,
     lambda: _mk({"EG": ("transition", "2026-08-06")},
                 {"AMOC": ("2026-09-03", "EGP", {"reason": "   "})}))
case("a breach declared with the key present and no reason at all", True,
     lambda: _mk({"EG": ("transition", "2026-08-06")},
                 {"AMOC": ("2026-09-03", "EGP", {})}))

# ---- the ratchet -------------------------------------------------------------------
case("a listed study still breaching — allowed to fail while it waits its turn", False,
     lambda: _mk({"EG": ("transition", "2026-08-06")},
                 {"AMOC": ("2026-09-03", "EGP", None)},
                 ratchet={"AMOC": "predates the bound"}))
case("a listed study beside a NEW one — the new breach still breaks the build", True,
     lambda: _mk({"EG": ("transition", "2026-08-06")},
                 {"AMOC": ("2026-09-03", "EGP", None),
                  "ARCC": ("2026-09-03", "EGP", None)},
                 ratchet={"AMOC": "predates the bound"}))
case("a ratchet naming a study that does not resolve on disk [R-ENF-04]", True,
     lambda: _mk({"EG": ("transition", "2026-08-06")},
                 {"AMOC": ("2026-08-10", "EGP", None)},
                 ratchet={"GHOST": "no such study"}))

# ---- population anchoring, BOTH ways -------------------------------------------------
case("zero study directories — an empty population is not a clean one", True,
     lambda: _mk({"EG": ("transition", "2026-08-06")}, {}))
case("studies present but NONE pairs a strike date with an anchor — read nothing, so it "
     "must refuse rather than report clean", True,
     lambda: _mk({"EG": ("transition", "2026-08-06")},
                 {"XPT": (None, None, None), "GBCO": (None, None, None)}))

# ---- the currency must be DECLARED, never guessed ------------------------------------
case("a study that declares no currency is NOT assigned one, so a stale anchor cannot be "
     "pinned on it — but it also cannot be the only study, or the run read nothing", True,
     lambda: _mk({"EG": ("transition", "2026-08-06")},
                 {"MYSTERY": ("2026-09-03", None, None)}))


def main():
    real = G.OUTSTANDING_FILE
    caught = passed = 0
    red = sum(1 for c in CASES if c[1])
    green = len(CASES) - red
    try:
        for name, expect_red, build in CASES:
            d, eng = build()
            G.OUTSTANDING_FILE = os.path.join(eng, "build_depth_audit",
                                              "anchor_age_outstanding.json")
            # ASSERT THE MUTATION LANDED. A control that never injected its condition
            # reports green and proves only that the sandbox was untouched.
            assert os.path.isdir(os.path.join(eng, "macro_paths")), name
            assert os.path.exists(G.OUTSTANDING_FILE), name
            try:
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = G.main(["--engine=%s" % eng])
                out = buf.getvalue()
            finally:
                shutil.rmtree(d, ignore_errors=True)
            ok = (rc != 0) == expect_red
            if ok:
                caught += 1 if expect_red else 0
                passed += 0 if expect_red else 1
            print("  %-6s %s" % ("CAUGHT" if (ok and expect_red) else
                                 "PASSED" if ok else "MISSED", name))
            if not ok:
                print(out)
    finally:
        G.OUTSTANDING_FILE = real
    print("\ndefects caught %d/%d | clean cases passed %d/%d" % (caught, red, passed, green))
    return 0 if (caught == red and passed == green) else 1


if __name__ == "__main__":
    raise SystemExit(main())
