"""[R-FCAL-01 amended] — the walk-forward is an ACTUATOR, not a diary.

WHAT THIS GATE IS FOR. The fundamental walk-forward has measured five companies
and moved almost nothing. The standing rule allowed a correction to be adopted or
carried as a WATCH FLAG, and watch became the default — so the measurement layer
produced the two largest findings this project has about its own method (PHDC's
profit over-forecast of +1.12 log on 97% of cells; TMGH's sales under-forecast of
-0.88) and neither reached a driver. A measurement nobody acts on and nobody has
to explain not acting on is a diary.

Three things are checked from outside the study:

  1. THE RULE WAS RUN, AND ITS OUTPUT IS THE STUDY'S OUTPUT.
     engine/walkforward/decision_rule.py is pre-registered and mechanical. What
     it adopts on a record must equal what that record's corrections_log claims
     to have adopted. A study that adopts something the rule declines is fitting;
     a study that declines something the rule adopts is the diary again.

  2. THE STUDY'S FORWARD DRIVERS SIT INSIDE ITS OWN RECORD.
     A study that forecasts a driver outside the p10-p90 its own walk-forward
     measured for that driver is disagreeing with its own evidence. That is
     allowed — the record is five origins, not a law — but it must be NAMED and
     PRICED in the study's numbers file, not passed over in silence.

  3. THE LOG RECONCILES TO THE CLAIM.
     The corrections a study says it carries equal the corrections its log
     records. TMGH's log and its prose disagreed once, and nothing could see it.

RATCHETED [R-ENF-02], POPULATION-ANCHORED [R-ENF-04]: the population is the
walk-forward run directories on disk, counted somewhere other than this gate's
own list, and a run that examines zero of them FAILS rather than reporting clean.
"""
from __future__ import annotations

import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
sys.path.insert(0, ENGINE)
sys.path.insert(0, os.path.join(ENGINE, "walkforward"))

OUTSTANDING_FILE = os.path.join(ENGINE, "build_depth_audit", "actuation_outstanding.json")

import decision_rule as DR  # noqa: E402


def runs():
    """The population, anchored on the run directories rather than on a list this
    gate keeps for itself — defeating it would mean deleting the runs, which is a
    far louder failure than an empty list."""
    return sorted(glob.glob(os.path.join(ENGINE, "*_walkforward")))


def ticker_of(d):
    return os.path.basename(d).replace("_walkforward", "").upper()


def study_dir(tk):
    d = os.path.join(ENGINE, "%s_study" % tk.lower())
    return d if os.path.isdir(d) else None


def _load(path):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return None


def audit(rundir):
    """Return (state, detail) for one walk-forward run."""
    tk = ticker_of(rundir)
    scores = _load(os.path.join(rundir, "scores.json"))
    if scores is None:
        return "fail", "scores.json is missing or will not parse — the record " \
                       "this gate exists to read does not exist"

    verdicts = DR.run(scores)
    if not verdicts:
        return "fail", "the decision rule found no drivers in scores.json. An " \
                       "empty result is not a clean result."
    summ = DR.summary(verdicts)
    adopted = set(summ["adopted"])

    fails = []

    # ---- 1 & 3: the log reconciles to what the rule adopts -------------------
    log = _load(os.path.join(rundir, "corrections_log.json"))
    if log is None:
        fails.append("no corrections_log.json: the run records no decision about "
                     "its own findings, so there is nothing to reconcile and "
                     "nothing anyone has to explain")
    else:
        entries = log.get("log") if isinstance(log, dict) else log
        claimed = set()
        for e in (entries or []):
            for drv, c in (e.get("corrections") or {}).items():
                if abs(float(c.get("applied") or 0.0)) > 1e-9:
                    claimed.add(drv)
        extra = sorted(claimed - adopted)
        missing = sorted(adopted - claimed)
        if extra:
            # A run seeded on the ratchet applied these under the PREVIOUS rule
            # — three or more resolved errors, half strength — which was the
            # rule in force when it ran. That is not fitting, it is history, and
            # the ratchet is where history belongs. What this line catches once
            # a run is off the list is a NEW divergence: a correction the
            # pre-registered rule declines and a study applies anyway.
            fails.append("the log applies corrections the pre-registered rule "
                         "does not adopt: %s. Under the previous rule (three "
                         "resolved errors, half strength) these were legitimate; "
                         "under this one they are not, and a correction the rule "
                         "declines and a study applies anyway is fitting."
                         % ", ".join(extra))
        if missing:
            fails.append("the rule adopts %s and the log applies none of them. A "
                         "measurement nobody acts on, and nobody has to explain "
                         "not acting on, is a diary." % ", ".join(missing))

    # ---- 2: the study's forward drivers sit inside its own record ------------
    sdir = study_dir(tk)
    fr = _load(os.path.join(rundir, "forward_ranges.json"))
    if sdir and fr:
        nums = _load(os.path.join(sdir, "study_numbers.json")) or {}
        exceptions = (nums.get("walkforward_exceptions")
                      or (nums.get("walkforward") or {}).get("exceptions") or {})
        outside = []
        for drv, years in (fr.get("years") or {}).items():
            for h, blk in (years or {}).items():
                raw = blk.get("raw_projection")
                p10, p90 = blk.get("p10"), blk.get("p90")
                if raw is None or p10 is None or p90 is None:
                    continue
                if raw < p10 or raw > p90:
                    outside.append("%s h%s (%.4g outside %.4g-%.4g)"
                                   % (drv, h, raw, p10, p90))
        unpriced = [o for o in outside if o.split()[0] not in exceptions]
        if unpriced:
            fails.append("the study forecasts %d driver-year(s) outside the "
                         "p10-p90 its own walk-forward measured, with no named "
                         "mechanism and no price: %s. Disagreeing with your own "
                         "record is allowed; doing it silently is not."
                         % (len(unpriced), "; ".join(unpriced[:4])))

    if fails:
        return "fail", "  - ".join([""] + fails).strip()
    return "ok", ("%d drivers -> adopt %d, watch %d, none %d%s"
                  % (summ["drivers"], summ["adopt"], summ["watch"], summ["none"],
                     ("; adopted: " + ", ".join(summ["adopted"])) if adopted else ""))


def main(argv):
    prune = "--prune" in argv
    if not os.path.exists(OUTSTANDING_FILE):
        print("FAIL — the ratchet list %s does not exist."
              % os.path.relpath(OUTSTANDING_FILE, ROOT))
        return 1
    out = json.load(open(OUTSTANDING_FILE, encoding="utf-8"))
    known = set(out.get("outstanding", []))

    rundirs = runs()
    if not rundirs:
        print("FAIL — examined zero walk-forward runs. An empty result is not a "
              "clean result [R-ENF-04].")
        return 1
    on_disk = {ticker_of(d) for d in rundirs}
    vanished = sorted(known - on_disk)
    if vanished:
        print("FAIL — the outstanding list names runs that do not exist on disk: "
              "%s. Either the glob did not run or the runs were removed without "
              "pruning; neither is a pass." % ", ".join(vanished))
        return 1

    ok, fixed, still, hard = [], [], [], []
    for d in rundirs:
        tk = ticker_of(d)
        try:
            state, detail = audit(d)
        except Exception as exc:
            # a crash is never "allowed for now": it is an unknown shortfall, not
            # a known one, and the other runs are still owed an answer
            state, detail = "fail", ("%s while auditing this run: %s"
                                     % (type(exc).__name__, exc))
        listed = tk in known
        if state == "ok":
            (fixed if listed else ok).append((tk, detail))
        else:
            (still if listed else hard).append((tk, detail))

    print("walk-forward runs examined: %d   actuating: %d   outstanding (allowed): %d"
          % (len(rundirs), len(ok) + len(fixed), len(still)))
    for tk, detail in sorted(ok):
        print("   %-12s %s" % (tk, detail))
    if fixed:
        print("\nNOW ACTUATING — remove from the outstanding list (%d):" % len(fixed))
        for tk, detail in fixed:
            print("   %-12s %s" % (tk, detail))
    if still:
        print("\nstill outstanding, allowed for now (%d):" % len(still))
        for tk, detail in still:
            print("   %-12s %s" % (tk, detail[:220]))
    if hard:
        print("\nFAIL — not on the outstanding list and not actuating (%d):" % len(hard))
        for tk, detail in hard:
            print("   %-12s %s" % (tk, detail[:600]))

    if prune:
        out["outstanding"] = sorted(known - {tk for tk, _ in fixed})
        json.dump(out, open(OUTSTANDING_FILE, "w", encoding="utf-8"), indent=1)
        print("\npruned — now %d entries" % len(out["outstanding"]))
        return 0
    if hard:
        print("\nA walk-forward that measures and never acts is a diary. Either "
              "the correction the rule adopts is applied, or the study says in "
              "its own numbers why it is not.")
        return 1
    print("\nOK — no new violations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
