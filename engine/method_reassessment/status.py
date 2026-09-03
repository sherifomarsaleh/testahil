#!/usr/bin/env python3
"""Where the method reassessment stands — read from the repository, not from the state file.

WHY THIS EXISTS. The programme's state lives in STATE.json and MORNING.md, both
written by hand at the end of a run. They are the only record of the things a
machine cannot know — which decisions are the principal's, what was tried and
rejected, why. They are also, being hand-written, guaranteed to drift from the
repository the moment anything lands, and they drift SILENTLY: nothing in either
file goes stale in a way a reader can see.

The first run of this script found exactly that. STATE.json's "next" list carried
"DECISION: merge PR #336" while origin/main already contained the merge — the
decision had been taken and the file still asked for it. A status read out of that
file would have reported a programme waiting on something that had happened.

So this reads the REPOSITORY and shows the state file's claims beside it, never
instead of it. [R-ENF-04] in its usual form: the population is anchored somewhere
other than the thing being checked. Each workstream is measured on the artefacts
it had to produce; each re-issued name on its own committed numbers, through the
gap gate's own reader rather than a second one; the blocked items on the archive
that is actually blocking.

WHAT THIS IS NOT. It is a REPORT, not a gate, and presence is not correctness: it
says an artefact exists, never that it passes. `--gates` is the other half — it
runs CI's own step list through scripts/run_ci_gates.py, which parses the workflow
YAML so it cannot drift from CI the way a maintained list would. Default run is
about a second and touches no network; --gates takes a few minutes.

IT REFUSES TO REPORT CLEAN HAVING EXAMINED NOTHING. A missing state file, an
unreadable ratchet, zero study directories, a workflow directory that globs empty
— each prints as a REFUSAL and sets the exit code, because an absent answer wearing
the costume of a clean one is the failure this whole programme kept finding.
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
ROOT = os.path.dirname(ENGINE)
AUDIT = os.path.join(ENGINE, "build_depth_audit")

# Collected as we go. A refusal is a thing this script could not read, and it is
# never silently downgraded to "nothing to report".
REFUSALS: list[str] = []


def refuse(msg: str) -> None:
    REFUSALS.append(msg)
    print("  REFUSED — %s" % msg)


def rel(p: str) -> str:
    return os.path.relpath(p, ROOT)


def git(*args: str) -> str:
    try:
        r = subprocess.run(("git",) + args, cwd=ROOT, capture_output=True,
                           text=True, timeout=20)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def head(path: str, n: int = 1) -> str:
    try:
        with open(path, encoding="utf-8") as fh:
            return "".join(next(fh) for _ in range(n)).strip()
    except Exception:
        return ""


# ---------------------------------------------------------------- the workstreams
#
# Each workstream is measured on the artefacts the plan says it must produce.
# The list is the population; a workstream with a missing artefact prints what is
# missing rather than a verdict, because a verdict here would be this script's
# opinion and the gates are the instrument.
WORKSTREAMS = [
    ("WS1", "cost-of-capital schedule", "[R-COC-01]", [
        "engine/cost_of_capital.py",
        "scripts/check_cost_of_capital.py",
        "scripts/check_cost_of_capital_negative_control.py"]),
    ("WS2", "one house macro path", "[R-MACRO-01]", [
        "engine/macro_path.py",
        "engine/macro_paths/EG.json",
        "engine/Cost_of_Capital_Reference.md",
        "scripts/check_macro_coherence.py",
        "scripts/check_macro_coherence_negative_control.py"]),
    ("WS3", "lens architecture", "[R-LENS-03]", [
        "scripts/check_lens_design.py",
        "scripts/check_lens_design_negative_control.py"]),
    ("WS4", "enterprise-to-equity bridge", "[R-BRIDGE-01]", [
        "scripts/check_bridge.py",
        "scripts/check_bridge_negative_control.py"]),
    ("WS5", "walk-forward actuator", "[R-FCAL-01]", [
        "engine/walkforward/decision_rule.py",
        "scripts/check_walkforward_actuation.py",
        "scripts/check_walkforward_actuation_negative_control.py"]),
    ("WS6", "valuation calibration", "[R-VCAL-01]", [
        "engine/valuation_calibration/score.py",
        "engine/valuation_calibration/delivered.py",
        "engine/valuation_calibration/PRE_REGISTRATION_HASH.json",
        "engine/fv_vintages.json",
        "engine/macro_history/EG.json",
        "scripts/check_valuation_calibration.py",
        "scripts/check_valuation_calibration_negative_control.py",
        "scripts/check_fv_vintages.py",
        "scripts/check_fv_vintages_negative_control.py"]),
    ("WS7", "output gates", "[R-GAP-01, R-ENF-05]", [
        "scripts/check_valuation_gap.py",
        "scripts/check_valuation_gap_negative_control.py",
        "scripts/check_output_records.py",
        "scripts/check_output_records_negative_control.py"]),
    ("WS9", "generalise beyond the five", "", [
        "engine/method_reassessment/ws9_report.py"]),
]

# WS8's artefacts are the five studies themselves, reported in their own section.
REISSUED = ("TMGH", "PHDC", "ARCC", "EGCH", "AMOC")


def section(title: str) -> None:
    print("\n" + title)
    print("  " + "-" * (len(title) + 2))


# ---------------------------------------------------------------- from the other line
#
# TWO SESSIONS WROTE A status.py AT THE SAME TIME, and the merge is a merge rather
# than a choice: these two sections came from the other one, which had them and this
# one did not. The book() section in particular is the programme's own founding
# question — every delivered central against the price it was struck at — and
# discarding it because the surrounding file was mine would have been the parallel-
# session failure [R-IND-01] was adopted for, running the other way.

def clock():
    utc = dt.datetime.now(dt.timezone.utc)
    cairo = utc + dt.timedelta(hours=3)          # EEST; the plan's own offset
    night = cairo.hour >= 22 or cairo.hour < 8
    print("  %s Cairo   (%s UTC)" % (cairo.strftime("%a %d %b %Y  %H:%M"),
                                     utc.strftime("%H:%M")))
    print("  %s window — %s of the plan"
          % ("NIGHT" if night else "DAY", "100%" if night else "50%"))


def book():
    """The delivered book's own numbers, computed now."""
    sys.path.insert(0, os.path.join(ENGINE, "valuation_calibration"))
    try:
        import delivered as DEL
    except Exception as exc:
        print("  could not read the delivered book (%s: %s)" % (type(exc).__name__, exc))
        return
    rows, nonpos, unread, two = DEL.read_book()
    xs = sorted(r["log_gap"] for r in rows)
    if not xs:
        print("  no readable central/spot pairs")
        return
    import math
    mean = sum(xs) / len(xs)
    med = xs[len(xs) // 2] if len(xs) % 2 else (xs[len(xs)//2-1] + xs[len(xs)//2]) / 2
    print("  studies with a readable answer   %d" % len(rows))
    print("  published as two-sided           %d" % len(two))
    print("  central at or below zero         %d" % len(nonpos))
    print("  answer not readable              %d" % len(unread))
    print("  mean fair value vs price   %+.1f%%" % ((math.exp(mean) - 1) * 100))
    print("  MEDIAN                     %+.1f%%   <- the one that matters"
          % ((math.exp(med) - 1) * 100))
    print("  below the price            %d of %d"
          % (sum(1 for x in xs if x < 0), len(xs)))

# ---------------------------------------------------------------- 1. the branch
def where_the_work_is() -> None:
    section("WHERE THE WORK IS")
    branch = git("rev-parse", "--abbrev-ref", "HEAD") or "(unknown)"
    print("  branch            %s" % branch)

    # Whether main carries this is the whole question [R-MERGE-01]: a rule on a
    # branch binds nothing, because the next study starts from a fresh clone.
    if not git("rev-parse", "--verify", "origin/main"):
        refuse("origin/main does not resolve in this checkout, so whether this work "
               "binds cannot be answered. Fetch it rather than reading the absence "
               "as 'merged'.")
    else:
        ahead = git("rev-list", "--count", "origin/main..HEAD")
        behind = git("rev-list", "--count", "HEAD..origin/main")
        print("  vs origin/main    %s ahead, %s behind" % (ahead or "?", behind or "?"))
        if ahead == "0":
            print("  binds?            YES — origin/main carries this work")
        else:
            print("  binds?            NO — %s commit(s) live only on this branch, and a "
                  "rule on a branch\n                    binds nothing [R-MERGE-01]" % ahead)

    dirty = [l for l in git("status", "--porcelain").splitlines() if l.strip()]
    print("  working tree      %s" % ("clean" if not dirty
                                      else "%d file(s) modified or untracked" % len(dirty)))
    for line in dirty[:6]:
        print("                    %s" % line)
    if len(dirty) > 6:
        print("                    ... and %d more" % (len(dirty) - 6))

    digests = glob.glob(os.path.join(ENGINE, "PROJECT_INSTRUCTIONS_*.md"))
    if len(digests) != 1:
        refuse("%d files match engine/PROJECT_INSTRUCTIONS_*.md; [R-DOC-01] requires "
               "exactly one." % len(digests))
    else:
        stamp = head(digests[0])[:46]
        print("  digest            %s\n                    %s" % (rel(digests[0]), stamp))


# ---------------------------------------------------------------- 2. workstreams
def workstreams() -> None:
    section("PHASE 1 — WORKSTREAMS, each measured on what it had to produce")
    print("  presence, never correctness. --gates is the instrument that says whether")
    print("  any of it passes.\n")
    for ws, name, rule, arts in WORKSTREAMS:
        missing = [a for a in arts if not os.path.exists(os.path.join(ROOT, a))]
        mark = "built  " if not missing else "PARTIAL"
        print("  %-4s %-28s %-22s %s  %d/%d artefacts"
              % (ws, name, rule, mark, len(arts) - len(missing), len(arts)))
        for m in missing:
            print("       missing: %s" % m)

    # WS2 carries a fact no artefact list can express: six of seven markets declare
    # themselves pending and refuse to load. That is the design, not a shortfall.
    paths = sorted(glob.glob(os.path.join(ENGINE, "macro_paths", "*.json")))
    if not paths:
        refuse("engine/macro_paths/ globbed empty — WS2 cannot be reported on.")
    else:
        pend = []
        for p in paths:
            try:
                if (json.load(open(p, encoding="utf-8")).get("status") or "") == "pending":
                    pend.append(os.path.basename(p)[:-5])
            except Exception:
                refuse("engine/macro_paths/%s is unreadable" % os.path.basename(p))
        print("\n  WS2 macro paths   %d sourced, %d pending and refusing: %s"
              % (len(paths) - len(pend), len(pend), ", ".join(pend) or "none"))

    # WS10 is a documents question: a rule that appears in one governing document
    # and not the other is the drift [R-DOC-01] closes. The sync gate is the
    # instrument; this only counts.
    ids = {}
    for label, p in (("digest", (glob.glob(os.path.join(ENGINE, "PROJECT_INSTRUCTIONS_*.md")) or [None])[0]),
                     ("protocol", os.path.join(ENGINE, "Standing_Research_Protocol.md"))):
        if not p or not os.path.exists(p):
            refuse("%s not found; the rule-id comparison cannot run." % label)
            ids[label] = None
            continue
        ids[label] = set(re.findall(r"\[R-[A-Z]+-\d+\]", open(p, encoding="utf-8").read()))
    if ids.get("digest") and ids.get("protocol"):
        both = ids["digest"] & ids["protocol"]
        only = (ids["digest"] ^ ids["protocol"])
        print("  WS10 rule ids     %d in both documents%s"
              % (len(both), "" if not only else
                 ";  IN ONE ONLY: %s" % ", ".join(sorted(only))))


# ---------------------------------------------------------------- 3. the five
def the_five() -> None:
    section("WS8 — THE FIVE RE-ISSUED NAMES, from their own committed numbers")
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    try:
        from check_valuation_gap import read_answer, read_review   # the gate's own reader
    except Exception as e:
        refuse("the gap gate's reader will not import (%s); the five cannot be read "
               "without re-implementing it, which would grade something other than "
               "what ships." % e)
        return

    manifest = {}
    mpath = os.path.join(ENGINE, "publish_queue", "MANIFEST.json")
    if os.path.exists(mpath):
        try:
            for n in json.load(open(mpath, encoding="utf-8")).get("names", []):
                manifest[str(n.get("ticker", "")).upper()] = (n.get("fair") or {}).get("base")
        except Exception as e:
            refuse("engine/publish_queue/MANIFEST.json is unreadable (%s)" % e)
    else:
        refuse("no publish queue manifest — acceptance criterion 6 cannot be read.")

    print("  %-8s %10s %10s %9s   %-22s %s"
          % ("ticker", "central", "spot", "vs price", "gap review", "staged to publish"))
    stale = []
    for tk in REISSUED:
        sdir = os.path.join(ENGINE, "%s_study" % tk.lower())
        if not os.path.isdir(sdir):
            refuse("engine/%s_study/ does not exist" % tk.lower())
            continue
        central, spot, route = read_answer(sdir)
        if central is None or not spot:
            print("  %-8s %s" % (tk, "UNREADABLE — %s" % route))
            stale.append("%s: no central/spot pair" % tk)
            continue
        gap = central / spot - 1.0
        fn, covered, audited = read_review(sdir)[:3]
        # A review audits an ANSWER, and the answer moves; existence is not currency.
        if fn is None:
            rev = "none" + ("  (>10%, owed)" if abs(gap) > 0.10 else "")
            if abs(gap) > 0.10:
                stale.append("%s: %+.1f%% against price with no gap review" % (tk, gap * 100))
        elif audited is None:
            rev = "%s (states no central)" % fn.split("_")[-1][:10]
        elif abs(audited - central) > max(0.005 * abs(central), 1e-9):
            rev = "STALE — audited %.2f" % audited
            stale.append("%s: gap review audited %.2f, study publishes %.2f"
                         % (tk, audited, central))
        else:
            rev = "current (%.2f)" % audited
        staged = manifest.get(tk)
        if staged is None:
            st = "not staged"
        elif abs(staged - central) > max(0.005 * abs(central), 1e-9):
            st = "SUPERSEDED — queue holds %.2f" % staged
            stale.append("%s: publish queue holds %.2f against a committed %.2f"
                         % (tk, staged, central))
        else:
            st = "current"
        print("  %-8s %10.2f %10.2f %+8.1f%%   %-22s %s"
              % (tk, central, spot, gap * 100, rev, st))

    if stale:
        print("\n  NOT CURRENT — an artefact checked for existence rather than currency is")
        print("  the failure shape this programme found three times:")
        for s in stale:
            print("    · %s" % s)


# ---------------------------------------------------------------- 4. what blocks
def blocked() -> None:
    section("WHAT IS BLOCKED, AND ON WHAT")
    sys.path.insert(0, ENGINE)
    try:
        import macro_history
        usable = macro_history.usable_origins("EG")
        declared = sorted(int(o["year"]) for o in
                          (macro_history.load("EG").get("origins") or [])
                          if isinstance(o, dict) and "year" in o)
        missing = json.load(open(os.path.join(ENGINE, "macro_history", "EG.json"),
                                 encoding="utf-8")).get("unsourced", {}).get("fields", [])
        print("  macro history EG  %d of %d origins usable%s"
              % (len(usable), len(declared),
                 "" if usable else "  — the calibration cannot rebuild at any origin"))
        if missing:
            print("                    unsourced: %s  (an export from the principal; "
                  "both are\n                    observed figures, so this is access, "
                  "not point-in-time)" % ", ".join(missing))
    except Exception as e:
        refuse("engine/macro_history could not be read (%s) — a blocked item that "
               "cannot be read is not an unblocked one." % e)

    try:
        sys.path.insert(0, os.path.join(ENGINE, "valuation_calibration"))
        import score
        t = score.maturity_table()
        h1 = t["by_horizon"][1]
        print("  valuation score   %d vintages held; first scoreable %s (%d days away)"
              % (t["vintages"], h1["first_scoreable"], h1["days_away"]))
        print("                    the scorer returns a DATE until a vintage matures on "
              "its own\n                    clock [R-LENS-02]; that refusal is the "
              "substance, not politeness")
    except Exception as e:
        refuse("the valuation scorer will not run (%s)" % e)


# ---------------------------------------------------------------- 5. acceptance
def acceptance() -> None:
    section("ACCEPTANCE — Part E, resolved where a machine can resolve it")
    print("  1  gates green with negative controls          run --gates; CI is the authority")
    print("  2  drivers inside each walk-forward record     the actuation gate, in --gates")
    print("  3  pooled bias CI includes zero                NOT YET MEASURABLE — see above")
    print("  4  graded prediction (median |gap| < 15%)      computed below")
    print("  5  two-sided gap gate fires on nothing, or     the five, above")
    print("     every firing carries a complete review")
    print("  6  publish queue holds the files per name      the five, above")

    # Criterion 4 is a PREDICTION, not a criterion, and it is computed rather than
    # recalled — matching the price is explicitly not the goal (Part E's non-criterion).
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    try:
        from check_valuation_gap import read_answer
    except Exception:
        return
    gaps = []
    for tk in REISSUED:
        c, s, _ = read_answer(os.path.join(ENGINE, "%s_study" % tk.lower()))
        if c is not None and s:
            gaps.append((tk, abs(c / s - 1.0)))
    if not gaps:
        refuse("no re-issued study exposes a central/spot pair; criterion 4 cannot be "
               "computed and is not therefore satisfied.")
        return
    med = sorted(g for _, g in gaps)[len(gaps) // 2]
    outside = [tk for tk, g in gaps if g > 0.35]
    print("\n  prediction 4      median |central/price - 1| = %.1f%% across %d names "
          "(target < 15%%)" % (med * 100, len(gaps)))
    print("                    outside +/-35%%: %s" % (", ".join(outside) or "none"))
    print("                    a prediction can fail without the programme failing; "
          "matching the\n                    price is Part E's explicit NON-criterion")


# ---------------------------------------------------------------- 6. ratchets
def ratchets() -> None:
    section("GATE RATCHETS — what each gate is knowingly letting through")
    try:
        sys.path.insert(0, HERE)
        from ws9_report import GATES, _list
    except Exception as e:
        refuse("ws9_report will not import (%s); the ratchets cannot be summarised." % e)
        return
    studies = len(glob.glob(os.path.join(ENGINE, "*_study")))
    if not studies:
        refuse("zero study directories on disk — every gate below would report clean "
               "having opened nothing.")
    for label, fn, key in GATES:
        lst = _list(fn, key)
        if lst is None:
            refuse("ratchet unreadable: %s (%s) — not a gate everyone passes."
                   % (label, fn))
            continue
        print("  %-32s %2d outstanding of %d study directories" % (label, len(lst), studies))


# ---------------------------------------------------------------- 7. phase 2
def phase_two() -> None:
    section("PHASE 2 — the queue, read live")
    r = subprocess.run([sys.executable, os.path.join(ENGINE, "campaign_queue.py"), "--next"],
                       cwd=ROOT, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        refuse("campaign_queue.py --next exited %d; the queue is never written down, so "
               "there is no fallback to read." % r.returncode)
        return
    for line in r.stdout.strip().splitlines()[-3:]:
        print("  %s" % line.strip())


# ---------------------------------------------------------------- 8. the principal
def open_items() -> None:
    section("OPEN — what the state file says needs the principal")
    p = os.path.join(HERE, "STATE.json")
    if not os.path.exists(p):
        refuse("STATE.json is absent. Everything above is still true; the judgement "
               "items are the one population only this file holds, so their absence "
               "is unreported, not empty.")
        return
    try:
        st = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        refuse("STATE.json is unreadable (%s)" % e)
        return
    print("  hand-written, and shown as CLAIMS. Where the repository disagrees, the")
    print("  repository is above and this is the drift.\n")
    print("  updated           %s" % st.get("updated", "(unstamped)"))
    cur = st.get("current") or {}
    print("  claims            phase %s — %s / %s"
          % (st.get("phase", "?"), cur.get("workstream", "?"), cur.get("status", "?")))
    nxt = st.get("next") or []
    if not nxt:
        print("\n  nothing on the next list")
    for item in nxt:
        print("\n  · %s" % _wrap(str(item), 76))
        # THE DRIFT THIS SCRIPT WAS WRITTEN FOR. A decision item naming a pull
        # request is answerable from the repository: if main carries the merge,
        # the decision was taken and the list is asking for it anyway. Checked
        # rather than read, because a stale ask reads exactly like a live one.
        for pr in re.findall(r"PR #(\d+)", str(item)):
            if git("log", "--oneline", "--grep", r"(#%s)" % pr, "origin/main"):
                print("    ALREADY DONE — origin/main carries the merge of #%s. "
                      "This item is stale." % pr)
    for item in (st.get("stop_and_ask") or []):
        print("\n  STOP-AND-ASK · %s" % _wrap(str(item), 76))


def _wrap(s: str, w: int) -> str:
    import textwrap
    return ("\n    ").join(textwrap.wrap(s, w)) or s


# ---------------------------------------------------------------- 9. the gates
def run_gates() -> int:
    section("GATES — CI's own step list, per workflow")
    wf = sorted(glob.glob(os.path.join(ROOT, ".github", "workflows", "*.yml")))
    if not wf:
        refuse(".github/workflows/ globbed empty — running nothing is not running green.")
        return 1
    runner = os.path.join(ROOT, "scripts", "run_ci_gates.py")
    if not os.path.exists(runner):
        refuse("scripts/run_ci_gates.py is absent. It is deliberately not "
               "re-implemented here: a runner built from a maintained list is the "
               "drift it exists to prevent.")
        return 1
    # WHAT THIS CHECKOUT CANNOT CHECK, ESTABLISHED BEFORE ANYTHING RUNS. A gate
    # that refuses because of the environment is not a red gate and not a green
    # one — it is UNCHECKED, and saying which in advance is the difference between
    # a caveat and an excuse invented after the failure.
    limits = []
    if git("rev-parse", "--is-shallow-repository") == "true":
        limits.append("SHALLOW CLONE — any gate reading commit topology (the "
                      "valuation-calibration pre-registration gate) refuses here "
                      "by design; CI checks out at full depth. `git fetch "
                      "--unshallow` to check it locally.")
    limits.append("the runner skips any step that would mutate this checkout, needs "
                  "the GitHub runner, or carries an `if:` it cannot evaluate — so a "
                  "green here covers FEWER steps than CI does, and each skip is "
                  "printed by name below rather than counted as a pass.")
    print("  what this checkout cannot check:")
    for l in limits:
        print("    · %s" % _wrap(l, 72))
    print()

    # WHAT THE RUN ITSELF TOUCHED. MUTATES_THE_REPO guards the git verbs, but a
    # generator step legitimately WRITES: running the SEO workflow's step here
    # rewrote sitemap.xml's lastmod dates, which CI commits on main and which have
    # no business appearing in a person's working tree beside their own edit. The
    # run is not silently clean afterwards; it says what it moved.
    before = set(git("status", "--porcelain").splitlines())

    red = []
    for f in wf:
        name = os.path.basename(f)
        print("\n  == %s" % name)
        r = subprocess.run([sys.executable, runner, name], cwd=ROOT,
                           capture_output=True, text=True, timeout=3600)
        for line in r.stdout.strip().splitlines():
            print("  %s" % line)
        if r.returncode != 0:
            red.append(name)
        if r.stderr.strip():
            print("  stderr: %s" % r.stderr.strip().splitlines()[-1][:150])
    touched = sorted(set(git("status", "--porcelain").splitlines()) - before)
    if touched:
        print("\n  THIS RUN CHANGED THE WORKING TREE — generator steps write, and a "
              "checkout\n  that is quietly different afterwards is how an unrelated "
              "file gets swept into\n  somebody's commit. Revert unless you meant it:")
        for t in touched:
            print("    %s" % t)

    print("\n  %d workflow(s) run, %d red: %s"
          % (len(wf), len(red), ", ".join(red) or "none"))
    print("  CI remains the authority; a green run here is evidence, not a substitute,")
    print("  and every step it could not run locally is listed above as skipped.")
    return 1 if red else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--gates", action="store_true",
                    help="also run every workflow's steps through scripts/run_ci_gates.py "
                         "(minutes, not a second)")
    a = ap.parse_args(argv)

    print("TESTAHIL — fundamental method reassessment, status at %s"
          % dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"))
    print("read from the repository at %s" % ROOT)

    section("THE CLOCK")
    clock()
    where_the_work_is()
    workstreams()
    the_five()
    section("THE DELIVERED BOOK — every central against the price it was struck at")
    book()
    blocked()
    acceptance()
    ratchets()
    phase_two()
    open_items()

    rc = run_gates() if a.gates else 0
    if not a.gates:
        print("\n  (gates not run — this says what exists, never what passes. "
              "--gates runs them.)")

    if REFUSALS:
        print("\nREFUSALS — %d thing(s) this report could not read. An absent answer is "
              "not a\nclean one, so this exits nonzero:" % len(REFUSALS))
        for r in REFUSALS:
            print("  · %s" % _wrap(r, 74))
        return 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
