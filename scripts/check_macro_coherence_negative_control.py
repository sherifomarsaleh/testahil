"""A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE.

This reinjects, into a throwaway copy of the repository's study directories,
every condition scripts/check_macro_coherence.py claims to catch, and asserts
that the gate goes RED on each one. It also injects three CLEAN cases that must
NOT fire, because a check that cries wolf is one everybody learns to ignore.

The failure cases are not invented. Each is a defect this repository actually
shipped:

  1. TYPED GROWTH — a nominal rate that does not recompute to the path's
     inflation plus the real growth the model claims. Five studies carried five
     rates for one fiscal year in one country.
  2. TERMINAL REAL DECLINE — terminal growth below the inflation inside its own
     terminal discount rate, never stated as the real assumption it is. PHDC
     shipped 12% against roughly 14.6%; AMOC shipped 5% against 7% [L-055].
  3. TWO ECONOMIES — a hand-set currency path against the model's own inflation.
     AMOC escalated costs at 14.5% while depreciating the pound at 7.7% [L-048].
  4. QUOTED TERMINAL RISK-FREE — a terminal rate set by hand rather than derived
     from the target plus the real-rate convention.
  5. UNCONVERGED HORIZON — an explicit window that ends far from terminal
     growth, so the terminal capitalises a rate the model never reached.
  6. OWN MACRO INPUT — a study registering its own inflation number beside the
     house path.
  7. NO RECORD, NOT LISTED — a new study directory carrying no macro record and
     no entry in the ratchet list.
  8. UNREADABLE — a numbers file that will not parse. An unreadable answer is
     not a clean answer.
  9. EMPTY POPULATION — no study directories at all, and a ratchet list naming
     studies that do not exist. A gate that examined nothing must never report
     clean [R-ENF-04].

    python3 scripts/check_macro_coherence_negative_control.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join("scripts", "check_macro_coherence.py")

GOOD = {
    "market": "EG",
    "path_as_of": "2026-09-02",
    "growth_lines": [
        {"name": "selling price", "years": [2026, 2027, 2028, 2029, 2030],
         "nominal": [0.16, 0.12, 0.09, 0.075, 0.07], "real": 0.0},
        {"name": "volumes", "years": [2026, 2027], "nominal": [0.05, 0.05],
         "exempt_reason": "a disclosed capacity ladder, not a price"},
    ],
    "terminal": {"g_nominal": 0.07, "real": 0.0, "rf": 0.125, "inflation_in_rf": 0.07},
    "explicit_years": 5,
    "growth_at_horizon_end": 0.07,
}


def sandbox():
    """A throwaway repo with the modules and scripts, and NO study directories."""
    tmp = tempfile.mkdtemp(prefix="macro_nc_")
    os.makedirs(os.path.join(tmp, "engine", "build_depth_audit"))
    os.makedirs(os.path.join(tmp, "scripts"))
    for f in ("macro_path.py", "research_protocol.py"):
        shutil.copy(os.path.join(ROOT, "engine", f), os.path.join(tmp, "engine", f))
    shutil.copytree(os.path.join(ROOT, "engine", "macro_paths"),
                    os.path.join(tmp, "engine", "macro_paths"))
    for f in ("check_macro_coherence.py",):
        shutil.copy(os.path.join(ROOT, "scripts", f), os.path.join(tmp, "scripts", f))
    return tmp


def put_study(tmp, ticker, record, extra=None, raw=None):
    d = os.path.join(tmp, "engine", "%s_study" % ticker.lower())
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "study_numbers.json")
    if raw is not None:
        open(p, "w").write(raw)
        return
    doc = {"meta": {"ticker": ticker}, "macro_record": record}
    if extra:
        doc.update(extra)
    json.dump(doc, open(p, "w"), indent=1)


def put_list(tmp, tickers):
    json.dump({"why": "negative control", "adopted": "2026-09-02",
               "outstanding": sorted(tickers)},
              open(os.path.join(tmp, "engine", "build_depth_audit",
                                "macro_outstanding.json"), "w"), indent=1)


def run(tmp):
    r = subprocess.run([sys.executable, GATE], cwd=tmp, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def case(name, build, expect_red, results):
    tmp = sandbox()
    try:
        build(tmp)
        rc, out = run(tmp)
        red = rc != 0
        ok = red == expect_red
        results.append((name, ok, rc, out.strip().splitlines()[-1] if out.strip() else ""))
        if not ok:
            print("\n---- %s: full output ----\n%s" % (name, out))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    results = []

    def broken(mutate):
        def build(tmp):
            rec = json.loads(json.dumps(GOOD))
            mutate(rec)
            put_study(tmp, "NCA", rec)
            put_list(tmp, [])
        return build

    def m_typed(rec):
        rec["growth_lines"][0]["nominal"][1] = 0.055      # a typed 5.5% in a 12% year

    def m_terminal(rec):
        rec["terminal"]["g_nominal"] = 0.12
        rec["terminal"]["inflation_in_rf"] = 0.146

    def m_fx(rec):
        rec["fx_path"] = [51.0, 52.0, 53.0, 54.0, 55.0]   # hand-set, ~3.5%/yr not ~13%

    def m_rf(rec):
        rec["terminal"]["rf"] = 0.105                      # quoted, not derived

    def m_horizon(rec):
        rec["growth_at_horizon_end"] = 0.44                # nowhere near terminal

    case("1 typed growth rate", broken(m_typed), True, results)
    case("2 terminal real decline", broken(m_terminal), True, results)
    case("3 hand-set currency path", broken(m_fx), True, results)
    case("4 quoted terminal risk-free", broken(m_rf), True, results)
    case("5 unconverged explicit window", broken(m_horizon), True, results)

    def b_own(tmp):
        put_study(tmp, "NCA", GOOD, extra={"registry": {
            "cpi": {"value": 0.143, "source": "the study's own reading of the statistics office"}}})
        put_list(tmp, [])
    case("6 study sets its own inflation", b_own, True, results)

    def b_norecord(tmp):
        d = os.path.join(tmp, "engine", "nca_study")
        os.makedirs(d)
        json.dump({"meta": {"ticker": "NCA"}}, open(os.path.join(d, "study_numbers.json"), "w"))
        put_list(tmp, [])
    case("7 new study, no record, not listed", b_norecord, True, results)

    def b_unreadable(tmp):
        put_study(tmp, "NCA", None, raw="{ this will not parse")
        put_list(tmp, [])
    case("8 numbers file will not parse", b_unreadable, True, results)

    def b_empty(tmp):
        put_list(tmp, ["GHOST"])           # names a study that does not exist, and none on disk
    case("9 empty population", b_empty, True, results)

    # ---- clean cases, which must NOT fire --------------------------------
    def c_good(tmp):
        put_study(tmp, "NCA", GOOD)
        put_list(tmp, [])
    case("clean: a coherent study", c_good, False, results)

    def c_listed(tmp):
        rec = json.loads(json.dumps(GOOD)); m_terminal(rec)
        put_study(tmp, "NCA", rec)
        put_list(tmp, ["NCA"])             # knowingly outstanding: allowed to fail
    case("clean: a listed outstanding study", c_listed, False, results)

    def c_real(tmp):
        rec = json.loads(json.dumps(GOOD))
        # real growth of 2%, STATED — nominal is inflation compounded with it
        rec["growth_lines"][0]["real"] = 0.02
        rec["growth_lines"][0]["nominal"] = [round((1 + i) * 1.02 - 1, 6)
                                             for i in (0.16, 0.12, 0.09, 0.075, 0.07)]
        rec["terminal"]["real"] = 0.02
        rec["terminal"]["g_nominal"] = 0.09
        rec["growth_at_horizon_end"] = 0.0914
        put_study(tmp, "NCA", rec)
        put_list(tmp, [])
    case("clean: stated real growth of 2%", c_real, False, results)

    print("\nNEGATIVE CONTROL — scripts/check_macro_coherence.py")
    for name, ok, rc, last in results:
        print("  %-38s %-4s exit %d   %s" % (name, "ok" if ok else "MISS", rc, last[:70]))
    bad = [n for n, ok, _, _ in results if not ok]
    if bad:
        print("\nFAILED: the gate did not behave as claimed on: %s" % ", ".join(bad))
        return 1
    print("\nAll %d conditions behave as claimed." % len(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
