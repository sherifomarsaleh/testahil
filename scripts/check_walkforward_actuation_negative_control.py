"""Negative control for the walk-forward actuation gate.

A gate nobody has seen fail is not evidence. Every condition below is a defect
the gate claims to catch, injected into an isolated copy of a run directory, plus
clean cases that must NOT fire — because a check that goes red where no rule
exists is the permanently-red check [R-ENF-02] forbids.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, "scripts", "check_walkforward_actuation.py")

# A record whose bias is large, robust across every block, era-stable and beating
# FREEZE — i.e. one the pre-registered rule ADOPTS. Every case below starts here.
ADOPTABLE = {
    "by_driver": {
        "new_sales": {
            "n": 33, "bias": -0.8768, "mae": 1.022, "median": -0.7186, "over": 0.242,
            "boot": {"2": {"lo": -1.496, "hi": -0.3219},
                     "3": {"lo": -1.5927, "hi": -0.4754},
                     "4": {"lo": -1.5795, "hi": -0.408}},
            "robust_sign": True,
        },
    },
    "by_era": {"new_sales": {"E2 post-float": {"n": 14, "bias": -0.2746},
                             "E3 devaluation": {"n": 19, "bias": -1.3206}}},
    "by_horizon": {"new_sales": {"1": {"skill_freeze": {"n": 8, "model_mae": 0.51,
                                                        "bench_mae": 0.60,
                                                        "skill": 0.15}}}},
}

APPLIED = {"log": [{"origin": 2020,
                    "corrections": {"new_sales": {"applied": -0.7745,
                                                  "reason": "rule", "n": 33}},
                    "any_applied": True}]}
NOT_APPLIED = {"log": [{"origin": 2020,
                        "corrections": {"new_sales": {"applied": 0.0,
                                                      "reason": "watch", "n": 33}},
                        "any_applied": False}]}


def make_run(engine, tk, scores=ADOPTABLE, log=APPLIED, forward=None):
    d = os.path.join(engine, "%s_walkforward" % tk.lower())
    os.makedirs(d, exist_ok=True)
    if scores is not None:
        json.dump(scores, open(os.path.join(d, "scores.json"), "w"))
    if log is not None:
        json.dump(log, open(os.path.join(d, "corrections_log.json"), "w"))
    if forward is not None:
        json.dump(forward, open(os.path.join(d, "forward_ranges.json"), "w"))
        sd = os.path.join(engine, "%s_study" % tk.lower())
        os.makedirs(sd, exist_ok=True)
        json.dump({"central": 1.0, "spot": 1.0},
                  open(os.path.join(sd, "study_numbers.json"), "w"))
    return d


def run_case(name, build, outstanding, must_fail, results):
    tmp = tempfile.mkdtemp(prefix="wfact-")
    try:
        engine = os.path.join(tmp, "engine")
        os.makedirs(os.path.join(engine, "build_depth_audit"), exist_ok=True)
        # the rule module the gate imports must travel with the fixture
        shutil.copytree(os.path.join(ROOT, "engine", "walkforward"),
                        os.path.join(engine, "walkforward"))
        json.dump({"outstanding": outstanding},
                  open(os.path.join(engine, "build_depth_audit",
                                    "actuation_outstanding.json"), "w"))
        build(engine)
        gate = os.path.join(tmp, "scripts", "check_walkforward_actuation.py")
        os.makedirs(os.path.dirname(gate), exist_ok=True)
        shutil.copy(GATE, gate)
        r = subprocess.run([sys.executable, gate], capture_output=True, text=True,
                           timeout=300)
        red = r.returncode != 0
        ok = (red == must_fail)
        results.append(ok)
        print("  %-58s %s   exit %d   %s"
              % (name[:58], "ok  " if ok else "MISS", r.returncode,
                 (r.stdout.strip().splitlines() or [""])[-1][:70]))
        if not ok:
            print("        ---- what the gate printed ----")
            for line in r.stdout.strip().splitlines()[-8:]:
                print("        " + line[:150])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    print("walk-forward actuation gate — negative control")
    results = []

    # ---- defects that must go RED -------------------------------------------
    run_case("the rule adopts a correction and the log applies none",
             lambda e: make_run(e, "NEW", log=NOT_APPLIED), [], True, results)

    run_case("the log applies a correction the rule does not adopt",
             lambda e: make_run(e, "NEW", log={"log": [{"origin": 2020,
                 "corrections": {"invented": {"applied": -0.4, "n": 40}},
                 "any_applied": True}]}), [], True, results)

    run_case("no corrections log at all — nothing to reconcile",
             lambda e: make_run(e, "NEW", log=None), [], True, results)

    run_case("no scores file — the record this gate reads does not exist",
             lambda e: make_run(e, "NEW", scores=None), [], True, results)

    run_case("a forward driver outside its own p10-p90, unpriced",
             lambda e: make_run(e, "NEW", forward={"years": {"new_sales": {
                 "1": {"raw_projection": 50.0, "p10": 100.0, "p90": 200.0}}}}),
             [], True, results)

    run_case("emptied population — zero runs is not zero problems",
             lambda e: None, [], True, results)

    run_case("a listed run no longer resolves on disk",
             lambda e: make_run(e, "NEW"), ["VANISHED"], True, results)

    def _crash(e):
        d = make_run(e, "NEW")
        open(os.path.join(d, "scores.json"), "w").write('{"by_driver": {"x": 3}}')
    run_case("a record shaped so the rule would crash — never silent",
             _crash, [], True, results)

    # ---- clean cases that must stay GREEN ------------------------------------
    run_case("CLEAN — the rule adopts and the log applies, must PASS",
             lambda e: make_run(e, "NEW"), [], False, results)

    run_case("CLEAN — a listed outstanding run, allowed for now, must PASS",
             lambda e: make_run(e, "NEW", log=NOT_APPLIED), ["NEW"], False, results)

    run_case("CLEAN — a forward driver INSIDE its own p10-p90, must PASS",
             lambda e: make_run(e, "NEW", forward={"years": {"new_sales": {
                 "1": {"raw_projection": 150.0, "p10": 100.0, "p90": 200.0}}}}),
             [], False, results)

    run_case("CLEAN — outside the range but NAMED and PRICED, must PASS",
             lambda e: (make_run(e, "NEW", forward={"years": {"new_sales": {
                 "1": {"raw_projection": 50.0, "p10": 100.0, "p90": 200.0}}}}),
                 json.dump({"central": 1.0, "spot": 1.0,
                            "walkforward_exceptions": {
                                "new_sales": "the order book fell after the "
                                             "record's last origin; priced at "
                                             "-0.3 a share"}},
                           open(os.path.join(e, "new_study",
                                             "study_numbers.json"), "w"))),
             [], False, results)

    print()
    if all(results):
        print("negative control OK — the gate goes red on every injected defect "
              "and stays green on every clean case")
        return 0
    print("NEGATIVE CONTROL FAILED — %d of %d cases came back wrong. A gate that "
          "cannot be shown to fail is not evidence."
          % (sum(1 for r in results if not r), len(results)))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
