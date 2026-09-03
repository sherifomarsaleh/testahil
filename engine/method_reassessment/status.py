"""Where the method reassessment actually stands, read live.

ONE COMMAND, NOTHING REMEMBERED. Every line below is computed from the repository
at the moment you run it — the programme state, what is blocked, what is waiting
on a decision, how far the branch is from main, and the delivered book's own
numbers. Nothing here is typed and nothing goes stale, which is the same rule the
calibration figures and the band records obey: a document that states a fact which
moves must not be the thing that remembers it.

    python3 engine/method_reassessment/status.py           # fast, no gates
    python3 engine/method_reassessment/status.py --gates    # also runs every CI step

The gate sweep is opt-in because it takes a few minutes; without it this prints in
about a second and is the thing to run when you want to know where we are.
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
STATE = os.path.join(HERE, "STATE.json")
MORNING = os.path.join(HERE, "MORNING.md")


def _git(*a):
    return subprocess.run(["git", "-C", ROOT] + list(a),
                          capture_output=True, text=True, timeout=120).stdout.strip()


def _rule(t=""):
    print("\n" + (("── %s " % t) if t else "").ljust(72, "─"))


def clock():
    utc = dt.datetime.now(dt.timezone.utc)
    cairo = utc + dt.timedelta(hours=3)          # EEST; the plan's own offset
    night = cairo.hour >= 22 or cairo.hour < 8
    print("  %s Cairo   (%s UTC)" % (cairo.strftime("%a %d %b %Y  %H:%M"),
                                     utc.strftime("%H:%M")))
    print("  %s window — %s of the plan"
          % ("NIGHT" if night else "DAY", "100%" if night else "50%"))


def programme():
    if not os.path.exists(STATE):
        print("  no STATE.json — the programme has no recorded state, which is itself news")
        return {}
    d = json.load(open(STATE, encoding="utf-8"))
    cur = d.get("current") or {}
    print("  phase %s · %s" % (d.get("phase", "?"), cur.get("workstream", "?")))
    print("  status: %s" % cur.get("status", "?"))
    print("  step  : %s" % (cur.get("step", "")[:300]))
    print("  done  : %d recorded steps" % len(d.get("done") or []))
    print("  state written %s" % d.get("updated", "never"))
    return d


def waiting_on_you(d):
    nxt = d.get("next") or []
    mine = [x for x in nxt if not x.upper().startswith(("BLOCKED", "DECISION"))]
    yours = [x for x in nxt if x.upper().startswith(("BLOCKED", "DECISION"))]
    print("  %d item(s) need YOU:" % len(yours))
    for x in yours:
        print("     • %s" % x[:200])
    if mine:
        print("\n  %d item(s) I can do without you:" % len(mine))
        for x in mine:
            print("     • %s" % x[:200])


def morning():
    if not os.path.exists(MORNING):
        return
    txt = open(MORNING, encoding="utf-8").read()
    items = [l for l in txt.splitlines() if l[:3].strip().rstrip(".").isdigit()
             and l.lstrip()[:1].isdigit()]
    print("  %d numbered items in MORNING.md (%s)"
          % (len(items), os.path.relpath(MORNING, ROOT)))
    if items:
        print("  latest: %s" % items[-1].strip()[:160])


def repo():
    branch = _git("rev-parse", "--abbrev-ref", "HEAD")
    head = _git("log", "--oneline", "-1")
    ahead = _git("rev-list", "--count", "origin/main..HEAD")
    behind = _git("rev-list", "--count", "HEAD..origin/main")
    dirty = _git("status", "--short")
    print("  branch %s" % branch)
    print("  head   %s" % head[:100])
    print("  %s ahead of origin/main, %s behind" % (ahead or "?", behind or "?"))
    print("  working tree: %s"
          % ("clean" if not dirty else "%d changed file(s)" % len(dirty.splitlines())))


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


def ratchets():
    rows = []
    for p in sorted(glob.glob(os.path.join(ENGINE, "build_depth_audit",
                                           "*outstanding*.json"))):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            rows.append((os.path.basename(p), "UNREADABLE"))
            continue
        # THE RATCHETS DO NOT SHARE A SHAPE, so this says WHICH KEY it counted
        # rather than guessing silently. Counting lists alone read the
        # dict-shaped valuation-input ratchet as "0 outstanding" while it held
        # five; counting every collection then over-read four others, because
        # some files also carry a conforming-at-adoption list, an alias map or an
        # exemption beside the thing that is actually outstanding. Both were
        # wrong in the one place whose whole job is to break that silence
        # [R-ENF-04], and the fix is not a cleverer guess — it is printing the
        # key, so a miscount is visible instead of plausible.
        keys = [k for k in ("outstanding", "runs", "entries", "figures",
                            "breach_no_review", "unreadable",
                            "review_central_unstated")
                if isinstance(d.get(k), (list, dict))]
        if keys:
            n = sum(len(d[k]) for k in keys)
        else:
            keys = [k for k, v in d.items()
                    if isinstance(v, (list, dict)) and not str(k).startswith("_")]
            n = sum(len(d[k]) for k in keys)
        rows.append((os.path.basename(p).replace("_outstanding.json", ""), n,
                     "+".join(keys) or "nothing countable"))
    for name, n, keys in rows:
        print("  %-26s %-16s %s"
              % (name, ("%d outstanding" % n) if isinstance(n, int) else n, keys))


def gates():
    r = subprocess.run([sys.executable,
                        os.path.join(ROOT, "scripts", "run_ci_gates.py")],
                       capture_output=True, text=True, timeout=1800)
    tail = [l for l in r.stdout.strip().splitlines() if l.startswith("ran ")
            or l.startswith("OK") or l.startswith("RED")]
    for l in tail[-6:]:
        print("  " + l)
    if r.returncode:
        print("  RED — see: python3 scripts/run_ci_gates.py")


def main():
    print("\nMETHOD REASSESSMENT — live status")
    _rule("clock"); clock()
    _rule("programme"); d = programme()
    _rule("waiting on you"); waiting_on_you(d)
    _rule("the delivered book, computed now"); book()
    _rule("ratchets (each may only shorten)"); ratchets()
    _rule("repository"); repo()
    _rule("morning list"); morning()
    if "--gates" in sys.argv:
        _rule("every CI step, run now"); gates()
    else:
        _rule()
        print("  gates not run — add --gates (a few minutes) to include them")
    print()


if __name__ == "__main__":
    main()
