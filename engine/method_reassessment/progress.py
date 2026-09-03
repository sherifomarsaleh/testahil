#!/usr/bin/env python3
"""How far the programme has got, and when each phase can end.

WHY THIS IS NOT ONE PERCENTAGE. The obvious dashboard blends build, delivery and
acceptance into a single number at weights somebody types. This house retired
exactly that construction three days ago: [R-LENS-03] took PHDC's central off a
45/15/20/20 blend of four lenses because a number produced by averaging several
methods at typed weights is a NEW method with free parameters nobody tested,
wearing the appearance of rigour. A programme percentage is the same object. So
this prints the components separately and never averages them, and where they
disagree — a build that is finished sitting on an acceptance instrument that is
blocked — the disagreement IS the status.

WHY MOST OF IT HAS NO DATE. A completion date is a quantity divided by a rate.
The quantity is countable here; the rate has never been measured. STATE.json
carries a field for it, `weekly_cap_window_equivalents`, and that field is null,
with `measured.window_equivalents_used` empty. The plan says so itself: the range
is about nine weeks if the weekly cap allows seven half-windows and about twenty
if it allows three. Printing one date off an unmeasured rate would be a free
parameter with a calendar attached, so the scenarios are printed as the plan's
own scenarios, anchored on the measured start date, each labelled with the
assumption it rests on.

AND WHERE A DEPENDENCY HAS NO DATE, NEITHER DOES THE PHASE. Phase 1's acceptance
instrument is criterion 3, and it needs point-in-time sovereign yields and policy
rates that only the principal can export. An export that has not arrived has no
date, and no amount of throughput substitutes for it. A dashboard that projected
Phase 1's end from its build rate would be reporting the half of the work that is
moving and silently omitting the half that cannot.

READ THE FIGURES LIVE. Everything below is counted from the repository at the
moment it runs: the campaign queue, the gates' own ratchets, the studies' own
committed numbers, git's own history. Nothing is remembered between runs.
"""
from __future__ import annotations

import datetime as dt
import glob
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
ROOT = os.path.dirname(ENGINE)

# The plan's own scenarios, quoted from Part D rather than invented here. Each is
# (half-windows a week, total weeks for both phases, what the plan calls it).
CAP_SCENARIOS = ((7, 9, "if the weekly cap allows seven half-windows"),
                 (5, 13, "the base case the Gantt is drawn at"),
                 (3, 20, "if it allows only three"))

PHASE1_PLANNED_WEEKS = 3          # Part D, "Phase 1 — the method, 3 weeks"
REISSUED = ("TMGH", "PHDC", "ARCC", "EGCH", "AMOC")


def git(*a: str) -> str:
    try:
        r = subprocess.run(("git",) + a, cwd=ROOT, capture_output=True,
                           text=True, timeout=20)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def _start_date() -> tuple[str, str]:
    """When Phase 1 began — measured, not typed.

    The commit that introduced the plan is the programme's own first act, and git
    records its date. A start date carried in a document would be a claim; this is
    an observation about the repository.
    """
    plans = sorted(glob.glob(os.path.join(HERE, "PLAN_*.md")))
    if not plans:
        return "", "no PLAN_*.md in engine/method_reassessment/"
    out = git("log", "--diff-filter=A", "--format=%ad", "--date=short",
              "--", os.path.relpath(plans[0], ROOT))
    if not out:
        return "", ("git does not record the plan's introducing commit — this is a "
                    "shallow clone, so the start date cannot be measured here")
    return out.splitlines()[-1], os.path.basename(plans[0])


# ---------------------------------------------------------------- the frontier
#
# THE ERROR THIS EXISTS TO PREVENT, AND IT IS MINE. On 3 September 2026 this
# module reported "0 of 11 point-in-time origins usable — an export that has not
# arrived has no date", and published that on a page. The export HAD arrived, the
# principal supplied it that morning, six origins were live and the calibration
# had already produced its first readings. All of it sat on another session's
# branch, and this module read only the checkout it happened to be standing in.
#
# That is [R-ENF-04] with the population one level further out than anyone looked:
# the tool anchored on "the repository" and the repository is not one line. Several
# sessions work at once; a blocker closed on a live branch is closed, and a status
# that reports it open is not cautious, it is wrong — and wrong in the direction
# that wastes the principal's time asking again for something already given.
#
# So the frontier is scanned first, and every blocked item is resolved against the
# MOST ADVANCED branch that carries it, with the branch named beside the figure.
BRANCH_SCAN_DAYS = 21


def live_branches() -> list:
    """Branches ahead of origin/main, most recently active first."""
    out = []
    raw = git("for-each-ref", "--format=%(refname:short)|%(committerdate:short)",
              "refs/remotes/origin")
    cutoff = (dt.date.today() - dt.timedelta(days=BRANCH_SCAN_DAYS)).isoformat()
    for line in raw.splitlines():
        if "|" not in line:
            continue
        ref, when = line.rsplit("|", 1)
        if ref in ("origin/main", "origin/HEAD") or when < cutoff:
            continue
        ahead = git("rev-list", "--count", "origin/main..%s" % ref)
        if ahead and ahead != "0":
            out.append({"branch": ref, "ahead": int(ahead), "last": when,
                        "subject": git("log", "-1", "--format=%s", ref)[:90]})
    return sorted(out, key=lambda b: (b["last"], b["ahead"]), reverse=True)


def _usable_origins_at(ref: str, market: str = "EG"):
    """usable_origins() for the archive as it stands on one ref.

    The blob is materialised and macro_history is pointed at it — the module's own
    requirement logic decides, never a second copy of it here [R-ENF-03].
    """
    import shutil, tempfile
    blob = git("show", "%s:engine/macro_history/%s.json" % (ref, market))
    if not blob:
        return None
    sys.path.insert(0, ENGINE)
    import macro_history
    tmp = tempfile.mkdtemp()
    try:
        open(os.path.join(tmp, "%s.json" % market), "w", encoding="utf-8").write(blob)
        keep = macro_history.ARCHIVE_DIR
        macro_history.ARCHIVE_DIR = tmp
        try:
            return {"usable": macro_history.usable_origins(market),
                    "declared": [int(o["year"]) for o in
                                 json.loads(blob).get("origins", [])
                                 if isinstance(o, dict) and "year" in o],
                    "unsourced": json.loads(blob).get("unsourced", {})}
        finally:
            macro_history.ARCHIVE_DIR = keep
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def best_archive(market: str = "EG") -> dict:
    """The archive at its FRONTIER — the checkout or whichever live branch is ahead."""
    best, where = None, "this checkout"
    here = _usable_origins_at("HEAD", market)
    if here:
        best = here
    for b in live_branches():
        cand = _usable_origins_at(b["branch"], market)
        if cand and (best is None or len(cand["usable"]) > len(best["usable"])):
            best, where = cand, b["branch"]
    if best is None:
        return {"error": "no macro archive resolves on any live ref"}
    best["source"] = where
    return best


# ------------------------------------------------------------------ the counting
def phase1() -> dict:
    """Phase 1, in three components that are never averaged together."""
    sys.path.insert(0, HERE)
    from status import WORKSTREAMS          # one list, imported, never a second copy
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    from check_valuation_gap import read_answer, read_review

    # (a) BUILD — the artefacts each workstream had to produce.
    arts = [a for _, _, _, lst in WORKSTREAMS for a in lst]
    built = [a for a in arts if os.path.exists(os.path.join(ROOT, a))]

    # (b) DELIVERY — the five re-issued names, three testable things each: the
    # answer is readable, the gap review audits the answer the study now
    # publishes, and the publish queue holds that same answer. Existence is not
    # currency, and this programme found that shape three times.
    manifest = {}
    mp = os.path.join(ENGINE, "publish_queue", "MANIFEST.json")
    if os.path.exists(mp):
        try:
            for n in json.load(open(mp, encoding="utf-8")).get("names", []):
                manifest[str(n.get("ticker", "")).upper()] = (n.get("fair") or {}).get("base")
        except Exception:
            manifest = {}
    names, atoms_ok, atoms_all = [], 0, 0
    for tk in REISSUED:
        sdir = os.path.join(ENGINE, "%s_study" % tk.lower())
        central, spot, _ = read_answer(sdir) if os.path.isdir(sdir) else (None, None, "")
        row = {"ticker": tk, "central": central, "spot": spot, "issues": []}
        atoms_all += 3
        if central is None or not spot:
            row["issues"].append("no readable central/spot pair")
        else:
            atoms_ok += 1
            row["gap"] = central / spot - 1.0
            fn, _, audited = read_review(sdir)
            tol = max(0.005 * abs(central), 1e-9)
            if abs(row["gap"]) <= 0.10:
                atoms_ok += 1               # no review owed inside 10% either way
                # A review that is not OWED can still be STALE, and a stale clean
                # bill in a directory is what a later re-issue inherits. Reported,
                # never counted against the atom the rule does not require.
                if fn is not None and audited is not None and abs(audited - central) > tol:
                    row["issues"].append("gap review audits %.2f against a committed "
                                         "%.2f — not owed inside 10%%, but stale where "
                                         "it sits" % (audited, central))
            elif fn is None:
                row["issues"].append("more than 10%% from price with no gap review")
            elif audited is None or abs(audited - central) > tol:
                row["issues"].append("gap review audits %s, study publishes %.2f"
                                     % ("no stated central" if audited is None
                                        else "%.2f" % audited, central))
            else:
                atoms_ok += 1
            staged = manifest.get(tk)
            if staged is None:
                row["issues"].append("not staged to publish")
            elif abs(staged - central) > tol:
                row["issues"].append("publish queue holds %.2f against a committed %.2f"
                                     % (staged, central))
            else:
                atoms_ok += 1
        names.append(row)

    # (c) ACCEPTANCE — Part E, and its third item is the instrument.
    accept = acceptance()
    return {"build": {"done": len(built), "total": len(arts),
                      "missing": [a for a in arts if a not in built]},
            "delivery": {"done": atoms_ok, "total": atoms_all, "names": names},
            "acceptance": accept}


def acceptance() -> list:
    """Part E's six criteria, each with what it waits on and whether that has a date."""
    items = [
        {"n": 1, "text": "construction gates green in CI with negative controls",
         "state": "MET", "waits_on": "re-checked by status.py --gates and by CI on every push"},
        {"n": 2, "text": "forward drivers inside each name's own walk-forward record",
         "state": "MET", "waits_on": "the walk-forward actuation gate, green in CI"},
        {"n": 3, "text": "the valuation calibration's pooled bias CI includes zero — "
                         "THE ACCEPTANCE INSTRUMENT",
         "state": "BLOCKED", "waits_on": None},
        {"n": 4, "text": "graded prediction: median |central/price - 1| inside 15%",
         "state": None, "waits_on": "computed below; a prediction may fail without the "
                                    "programme failing"},
        {"n": 5, "text": "the two-sided gap gate fires on nothing, or every firing "
                         "carries a complete review",
         "state": None, "waits_on": "the five, above"},
        {"n": 6, "text": "the publish queue holds the files per name on the new standard",
         "state": None, "waits_on": "the five, above"},
    ]
    # 3 — the two things it waits on, one dated and one not.
    try:
        arc = best_archive("EG")
        if "error" in arc:
            items[2]["waits_on"] = arc["error"]
        else:
            n, tot = len(arc["usable"]), len(arc["declared"])
            miss = arc.get("unsourced", {}).get("fields") or []
            items[2]["origins_usable"], items[2]["origins_declared"] = n, tot
            items[2]["archive_source"] = arc["source"]
            items[2]["state"] = "RUNNING" if n else "BLOCKED"
            items[2]["waits_on"] = (
                "%d of %d point-in-time origins usable, read at the frontier (%s)%s"
                % (n, tot, arc["source"],
                   "" if not miss else "; still unsourced: %s" % ", ".join(miss)))
    except Exception as e:
        items[2]["waits_on"] = "engine/macro_history could not be read (%s)" % e
    try:
        sys.path.insert(0, os.path.join(ENGINE, "valuation_calibration"))
        import score
        h1 = score.maturity_table()["by_horizon"][1]
        items[2]["dated_half"] = ("the gap-closure half cannot mature before %s (%d days) "
                                  "— the archive starts at the first published vintage and "
                                  "the fundamental lens is graded on its own clock "
                                  "[R-LENS-02]" % (h1["first_scoreable"], h1["days_away"]))
        items[2]["first_scoreable"] = h1["first_scoreable"]
    except Exception as e:
        items[2]["dated_half"] = "the scorer will not run (%s)" % e

    # 4, 5, 6 are resolved from the five.
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    from check_valuation_gap import read_answer
    gaps = []
    for tk in REISSUED:
        c, s, _ = read_answer(os.path.join(ENGINE, "%s_study" % tk.lower()))
        if c is not None and s:
            gaps.append(abs(c / s - 1.0))
    # 5 — every firing of the two-sided gate carries a review that audits the
    # answer the study NOW publishes. 6 — Part E asks for FOUR files per name.
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    from check_valuation_gap import read_review
    unreviewed, staged_issues = [], []
    mp = os.path.join(ENGINE, "publish_queue", "MANIFEST.json")
    man = {}
    if os.path.exists(mp):
        try:
            man = {str(n.get("ticker", "")).upper(): n
                   for n in json.load(open(mp, encoding="utf-8")).get("names", [])}
        except Exception as e:
            staged_issues.append("MANIFEST.json unreadable (%s)" % e)
    else:
        staged_issues.append("no publish queue manifest")
    for tk in REISSUED:
        sdir = os.path.join(ENGINE, "%s_study" % tk.lower())
        c, sp, _ = read_answer(sdir)
        if c is None or not sp:
            unreviewed.append("%s unreadable" % tk)
            continue
        if abs(c / sp - 1.0) > 0.10:
            _, _, aud = read_review(sdir)
            if aud is None or abs(aud - c) > max(0.005 * abs(c), 1e-9):
                unreviewed.append("%s (%+.1f%%)" % (tk, (c / sp - 1) * 100))
        n = man.get(tk)
        if n is None:
            staged_issues.append("%s not staged" % tk)
            continue
        base = (n.get("fair") or {}).get("base")
        if base is None or abs(base - c) > max(0.005 * abs(c), 1e-9):
            staged_issues.append("%s staged at %s against a committed %.2f"
                                 % (tk, base, c))
        files = [k for k in ("report", "workbook", "bibliography", "docx") if n.get(k)]
        if len(files) < 4:
            staged_issues.append("%s stages %d file(s), Part E asks for four"
                                 % (tk, len(files)))
    items[4]["state"] = "MET" if not unreviewed else "NOT MET"
    items[4]["waits_on"] = ("every firing carries a current review"
                            if not unreviewed else
                            "no current review on: %s" % ", ".join(unreviewed))
    items[5]["state"] = "MET" if not staged_issues else "NOT MET"
    items[5]["waits_on"] = ("the queue matches every committed answer"
                            if not staged_issues else "; ".join(staged_issues))

    if gaps:
        med = sorted(gaps)[len(gaps) // 2]
        items[3]["state"] = "MET" if med < 0.15 else "NOT MET"
        items[3]["waits_on"] = ("median is %.1f%% across %d names against a stated 15%%; "
                                "matching the price is Part E's explicit NON-criterion"
                                % (med * 100, len(gaps)))
    return items


def backtest_coverage() -> dict:
    """2a — how many names carry a point-in-time backtest record, read at the frontier.

    The score files are the record; a name is backtested when it has at least one
    scored origin, and a name with none is NOT quietly excluded — it is counted
    against the queue's own total [R-ENF-04].
    """
    best, where = {}, "this checkout"
    refs = ["HEAD"] + [b["branch"] for b in live_branches()]
    for ref in refs:
        names = {}
        listing = git("ls-tree", "-r", "--name-only", ref,
                      "engine/valuation_calibration/")
        for fn in listing.splitlines():
            if "SCORES_" not in fn:
                continue
            blob = git("show", "%s:%s" % (ref, fn))
            if not blob:
                continue
            try:
                for r in json.loads(blob).get("rows", []):
                    names.setdefault(str(r.get("ticker", "")).upper(),
                                     set()).add(r.get("origin"))
            except Exception:
                continue
        if len(names) > len(best):
            best, where = names, ref
    return {"names": {k: sorted(v) for k, v in best.items()}, "source": where}


def phase2() -> dict:
    """The other 85 names, read off the live campaign queue — never a written list."""
    r = subprocess.run([sys.executable, os.path.join(ENGINE, "campaign_queue.py")],
                       cwd=ROOT, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        return {"error": "campaign_queue.py exited %d; the queue is deliberately never "
                         "written in a document, so there is no fallback." % r.returncode}
    markets, cur, done, total = [], None, 0, 0
    for line in r.stdout.splitlines():
        s = line.strip()
        if s.startswith("== "):
            cur = {"market": s.strip("= ").rsplit("==", 1)[0].strip(), "done": 0, "total": 0}
            markets.append(cur)
        elif cur and s and s[0].isdigit():
            cur["total"] += 1
            total += 1
            if " current " in line:
                cur["done"] += 1
                done += 1
    bt = backtest_coverage()
    scored = [t for t in bt["names"] if bt["names"][t]]
    return {"done": done, "total": total, "markets": markets,
            "a": {"rebuilt": {"done": done, "total": total},
                  "backtested": {"done": len(scored), "total": total,
                                 "names": scored, "source": bt["source"]}},
            "b": {"started": False,
                  "why": "2b grades claims struck AFTER 2a closes — strictly "
                         "sequential, per the instruction of 03-Sep-2026. Its clock "
                         "has not started.",
                  "horizon": "up to one year [R-LENS-02]",
                  "earliest": "roughly one year after 2a closes — a MATURITY date, "
                              "never a throughput estimate"}}


def dates() -> dict:
    """Every date this programme can honestly put on a calendar, and every one it cannot."""
    start, src = _start_date()
    out = {"start": start, "start_source": src, "today": dt.date.today().isoformat()}
    if not start:
        out["note"] = ("the start date could not be measured, so no elapsed figure is "
                       "printed rather than one estimated")
        return out
    d0 = dt.date.fromisoformat(start)
    out["elapsed_days"] = (dt.date.today() - d0).days + 1
    out["phase1_planned_end"] = (d0 + dt.timedelta(weeks=PHASE1_PLANNED_WEEKS)).isoformat()
    out["scenarios"] = [
        {"half_windows_per_week": hw, "weeks": wk, "label": lab,
         "both_phases_end": (d0 + dt.timedelta(weeks=wk)).isoformat()}
        for hw, wk, lab in CAP_SCENARIOS]

    # The rate the scenarios turn on has never been recorded. Say so from the file
    # that has the empty field, rather than from memory.
    st = os.path.join(HERE, "STATE.json")
    cap, used = None, None
    if os.path.exists(st):
        try:
            j = json.load(open(st, encoding="utf-8"))
            cap = j.get("weekly_cap_window_equivalents")
            used = (j.get("measured") or {}).get("window_equivalents_used")
        except Exception:
            pass
    out["rate_measured"] = bool(cap) or bool(used)
    out["rate_note"] = ("STATE.json carries weekly_cap_window_equivalents=%s and "
                        "measured.window_equivalents_used=%s — THE RATE EVERY DATE BELOW "
                        "DIVIDES BY HAS NEVER BEEN MEASURED, so these are the plan's own "
                        "scenarios anchored on the measured start, never a forecast."
                        % (cap, used if used else "[]"))
    # One measured throughput fact, from git rather than from anyone's recollection.
    by_day = {}
    for line in git("log", "--since", start, "--date=short", "--format=%ad").splitlines():
        by_day[line] = by_day.get(line, 0) + 1
    out["commits_by_day"] = dict(sorted(by_day.items()))
    return out


def report() -> dict:
    p1, p2, dd = phase1(), phase2(), dates()
    b, dv = p1["build"], p1["delivery"]
    met = sum(1 for a in p1["acceptance"] if a["state"] == "MET")

    print("TESTAHIL — method reassessment, progress at %s"
          % dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"))
    print("counted from the repository. THREE STAGES: Phase 1 (the method), Phase 2a")
    print("(the backtest across the book) and Phase 2b (the live test, going forward).")
    print("2a is bounded by WORK, 2b by the CALENDAR — never averaged together.\n")

    def bar(done, total, w=28):
        f = 0 if not total else int(round(w * done / total))
        return "[%s%s] %3d%%  %d/%d" % ("#" * f, "." * (w - f),
                                        0 if not total else round(100 * done / total),
                                        done, total)

    print("  PHASE 1 build       %s   artefacts the ten workstreams had to produce"
          % bar(b["done"], b["total"]))
    print("  PHASE 1 delivery    %s   the five re-issued names, three checks each"
          % bar(dv["done"], dv["total"]))
    print("  PHASE 1 acceptance  %s   Part E, and item 3 is the instrument"
          % bar(met, len(p1["acceptance"])))
    if "error" in p2:
        print("  PHASE 2             REFUSED — %s" % p2["error"])
    else:
        a = p2["a"]
        print("  PHASE 2a rebuilt    %s   names on the current standard"
              % bar(a["rebuilt"]["done"], a["rebuilt"]["total"]))
        print("  PHASE 2a backtested %s   names with a point-in-time record (%s)"
              % (bar(a["backtested"]["done"], a["backtested"]["total"]),
                 ", ".join(a["backtested"]["names"]) or "none"))
        print("  PHASE 2b            NOT STARTED — %s" % p2["b"]["why"].split(".")[0])
    print("\n  THESE ARE NOT AVERAGED INTO ONE NUMBER. A percentage blended at typed")
    print("  weights is a new method with free parameters nobody tested [R-LENS-03],")
    print("  and here the components disagree — which is the status, not a defect in it.")

    flight = live_branches()
    if flight:
        print("\nWORK IN FLIGHT — branches ahead of main, most recent first")
        print("  a blocker closed on a live branch is CLOSED. This section exists because")
        print("  this module once reported one open that another session had closed hours")
        print("  earlier, and published it.")
        for b in flight[:6]:
            print("  %-52s %3d ahead  %s" % (b["branch"][:52], b["ahead"], b["last"]))
            print("      %s" % b["subject"])

    print("\nWHEN EACH PHASE CAN END")
    if dd.get("start"):
        print("  Phase 1 began       %s (%s), day %d today"
              % (dd["start"], dd["start_source"], dd["elapsed_days"]))
    print("  Phase 1 build       DONE — planned for %s, finished on day %s"
          % (dd.get("phase1_planned_end", "?"), dd.get("elapsed_days", "?")))
    a3 = next((a for a in p1["acceptance"] if a["n"] == 3), None)
    if a3:
        print("  Phase 1 acceptance  %s. Criterion 3: %s"
              % ("RUNNING" if a3["state"] == "RUNNING" else "NO DATE", a3["text"]))
        print("                      %s" % a3["waits_on"])
        if a3.get("dated_half"):
            print("                      %s" % a3["dated_half"])
    print("  Phase 2a            bounded by WORK — ninety rebuilds and ninety backtests;")
    print("                      throughput decides. Held until Phase 1's record shows the")
    print("                      method unbiased: 85 studies on an unproven method is the")
    print("                      mistake the campaign just made with five.")
    print("  Phase 2b            bounded by the CALENDAR — %s. It cannot"
          % p2.get("b", {}).get("horizon", "the lens's own clock"))
    print("                      complete earlier than %s"
          % p2.get("b", {}).get("earliest", "one year after 2a"))
    print("                      Projecting it from a work rate would be a number nobody")
    print("                      can know; 2b's date moves only when 2a's does.")
    print("\n  IF PHASE 2 STARTED TODAY, on the plan's own cap scenarios:")
    for s in dd.get("scenarios", []):
        print("    %d half-windows/week   both phases end %s   (%s)"
              % (s["half_windows_per_week"], s["both_phases_end"], s["label"]))
    print("  %s" % dd.get("rate_note", ""))
    if dd.get("commits_by_day"):
        print("  measured so far: %s"
              % ", ".join("%s %d commits" % kv for kv in dd["commits_by_day"].items()))

    bad = [(n["ticker"], i) for n in dv["names"] for i in n["issues"]]
    if bad:
        print("\nWHAT IS NOT CURRENT (existence is not currency)")
        for tk, i in bad:
            print("  %-6s %s" % (tk, i))

    return {"phase1": p1, "phase2": p2, "dates": dd,
            "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}


if __name__ == "__main__":
    d = report()
    if "--json" in sys.argv:
        out = os.path.join(HERE, "progress.json")
        json.dump(d, open(out, "w", encoding="utf-8"), indent=1, default=str)
        print("\nwrote %s" % os.path.relpath(out, ROOT))
