"""Generate Lessons_Register.md from lessons_register.py.

The register is GENERATED, never typed. This project has twice had two copies of
the same rules drift apart — the two protocol documents, and a page that stated
a fact it was also supposed to remember. A document that states something which
moves must not be the thing that remembers it.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import lessons_register as LR

OUT = os.path.join(HERE, "Lessons_Register.md")

ORIGIN_WORDS = {
    "walk_forward_fundamental": "fundamental walk-forward test",
    "walk_forward_price": "price-engine walk-forward test",
    "critique": "outside critique",
    "self_audit": "self-audit",
    "build": "found while building",
}


def population():
    """What evidence actually exists on disk, counted rather than remembered.

    Two different tests are both called a walk-forward and the first edition of
    this register conflated them, which understated the evidence base badly.
    Both are counted here, from the directories and files themselves.
    """
    import csv, glob
    fund = sorted(d[:-len("_walkforward")].upper() for d in os.listdir(HERE)
                  if d.endswith("_walkforward")
                  and os.path.isdir(os.path.join(HERE, d)))
    price, origins = [], 0
    for f in sorted(glob.glob(os.path.join(HERE, "*_study",
                                           "backtest_rows.csv"))):
        n = sum(1 for _ in csv.DictReader(open(f)))
        if n:
            price.append((os.path.basename(os.path.dirname(f))[:-6].upper(), n))
            origins += n
    return {"fundamental": fund, "price": price, "price_origins": origins}

def calibrated():
    """The calibrated-stocks table, read from the one store that holds it.

    [per instruction, 01-Sep-2026 — "I want the lessons document to keep track
    of all stocks that have been calibrated stating their Market / Class /
    Fair Price before calibration / Fair Price after calibration"]

    NOT A SECOND COPY OF THE FAIR-VALUE REGISTER.  The rule that the two halves
    of the calibration register are "cross-referenced, never duplicated" bars a
    figure being REMEMBERED in two places, because then the two can disagree
    and nothing says which is right.  It does not bar the same store being
    RENDERED twice.  Both documents read fv_movement.json, so a number here
    cannot drift from the number there -- editing the store moves both, and
    editing either document moves neither.

    Anchored on the RUNS ON DISK, not on the store's own key list: a run whose
    fair value was never recorded must show up as missing rather than be
    silently absent, which is what an empty result looks like when nobody
    counted [R-ENF-04].
    """
    import json
    sys.path.insert(0, HERE)
    import lessons_register as LR
    store = os.path.join(HERE, "fv_movement.json")
    entries = (json.load(open(store, encoding="utf-8"))["entries"]
               if os.path.exists(store) else {})
    runs = sorted(d[:-len("_walkforward")].upper() for d in os.listdir(HERE)
                  if d.endswith("_walkforward")
                  and os.path.isdir(os.path.join(HERE, d)))
    rows = []
    for tk in runs:
        e = entries.get(tk)
        if not e:
            rows.append({"ticker": tk, "market": "?", "klass": "?", "ccy": "",
                         "before": None, "after": None, "move": None,
                         "note": "no fair-value record — the run is on disk and "
                                 "its fair value was never recorded"})
            continue
        ed = e["editions"][-1] if e["editions"] else None
        base = e["baseline"]["fair"]
        rows.append({
            "ticker": tk,
            "market": "%s / %s" % (e.get("market") or "?", e.get("exchange") or "?"),
            "klass": LR.COMPANY_CLASS.get(tk, "— not mapped —"),
            "ccy": e.get("ccy") or "",
            "before": base["base"] if base else None,
            "after": ed["fair"]["base"] if ed else None,
            "move": (ed["vs_baseline_pct"]["base"]
                     if ed and ed.get("vs_baseline_pct") else None),
            "note": ("" if base else
                     "before-calibration price not recoverable — %s"
                     % (e["baseline"]["unrecoverable"] or "reason not recorded")),
        })
    return rows


def blocked():
    """Names we tried to calibrate and could not, and why.  [per instruction,
    01-Sep-2026 — "mention the stocks like EMFD that you tried calibrating but
    could not and state why"]

    A run that stopped is evidence too, and leaving it out makes the calibrated
    list read as though nothing else was attempted. Each blocked run states its
    own status in blocked.json, in its own directory, so the reason is recorded
    by the run that hit it rather than retyped here from memory — and so a
    later session cannot quietly soften it.
    """
    import json
    out = []
    for d in sorted(os.listdir(HERE)):
        if not d.endswith("_walkforward_pending"):
            continue
        p = os.path.join(HERE, d, "blocked.json")
        if not os.path.exists(p):
            out.append({"ticker": d.split("_")[0].upper(),
                        "reason_short": "blocked, but the run recorded no "
                                        "blocked.json saying why",
                        "_incomplete": True})
            continue
        b = json.load(open(p, encoding="utf-8"))
        b["_incomplete"] = False
        out.append(b)
    return out


def remaining():
    """What is still to be calibrated, read LIVE from the campaign queue.

    THE STANDING RULE IS THAT THE QUEUE IS NEVER WRITTEN IN A DOCUMENT, and it
    is a good rule: a typed list goes stale the moment a name is run, and it
    looks authoritative the whole time it is wrong. This does not type it. The
    queue is resolved from campaign_queue.py at BUILD time, every build, and a
    name drops off it the moment its run directory exists — so the list cannot
    disagree with the queue unless the document was never rebuilt, which the
    gate catches. Rendering a computed list is not the failure that rule
    guards against; remembering one is.
    """
    sys.path.insert(0, HERE)
    import campaign_queue as cq
    queue, excluded, standard, _ = cq.build_queue()
    done = {d[:-len("_walkforward")].upper() for d in os.listdir(HERE)
            if d.endswith("_walkforward")
            and os.path.isdir(os.path.join(HERE, d))}
    blocked_tk = {b["ticker"] for b in blocked()}
    todo = [q for q in queue
            if q["ticker"] not in done and q["ticker"] not in blocked_tk]
    by_market = {}
    for q in todo:
        by_market.setdefault(q["market_label"], []).append(q)
    return {"todo": todo, "by_market": by_market, "excluded": excluded,
            "standard": standard, "total": len(queue), "done": sorted(done),
            "blocked": sorted(blocked_tk)}


def money(v, ccy):
    return "—" if v is None else "%s %s" % (ccy, ("%.2f" % v).rstrip("0").rstrip("."))


def status_block():
    """Where the calibration campaign stands — done, blocked, and still to do.

    AT THE FRONT [per instruction, 01-Sep-2026 — "I want you to bring this
    table to the start"]. All three parts are computed at build time: the
    fair values from fv_movement.json, the blocked runs from each run's own
    blocked.json, the remainder from the live campaign queue. Nothing here is
    typed, so nothing here can go stale while looking authoritative.
    """
    cal, blk, rem = calibrated(), blocked(), remaining()
    b = ["\n---\n\n# Where the calibration stands\n\n"]

    b.append("**%d calibrated · %d attempted and blocked · %d still to go**, "
             "of %d names in the book.\n\n"
             % (len(cal), len(blk), len(rem["todo"]), rem["total"]))

    # ---- done -----------------------------------------------------------
    b.append("## Stocks that have been calibrated\n\n"
             "*Generated from the fair-value store, never typed — the same "
             "figures the fair-value register renders, so the two cannot "
             "disagree.*\n\n")
    b.append("| Stock | Market | Class | Fair price before | "
             "Fair price after | Move |\n|---|---|---|---|---|---|\n")
    for r in cal:
        b.append("| **%s** | %s | %s | %s | %s | %s |\n"
                 % (r["ticker"], r["market"], r["klass"],
                    money(r["before"], r["ccy"]), money(r["after"], r["ccy"]),
                    "—" if r["move"] is None else "%+.1f%%" % r["move"]))
    for r in [x for x in cal if x["note"]]:
        b.append("\n- **%s** — %s.\n" % (r["ticker"], r["note"]))
    b.append("\nThe fair price is the **central case**. Where a study "
             "publishes several cases and no single point, this column carries "
             "the median of them so the before-and-after can be compared at "
             "all; the study's own range is the thing to quote, never this "
             "cell. A move against a before-price that came from no "
             "current-standard study measures a new study against a number of "
             "unknown provenance, and the note above says so where that is the "
             "case.\n\n")

    # ---- blocked --------------------------------------------------------
    b.append("## Stocks we tried to calibrate and could not\n\n"
             "*A run that stopped is evidence too. Leaving these out would "
             "make the list above read as though nothing else was attempted. "
             "Each reason is recorded by the run that hit it, in its own "
             "directory, rather than retyped here.*\n\n")
    if not blk:
        b.append("None. Every name attempted so far has completed.\n\n")
    for x in blk:
        b.append("### %s — %s\n\n" % (x["ticker"], x.get("company", "")))
        b.append("**Blocked at %s.** %s.\n\n"
                 % (x.get("blocked_at", "an unrecorded step"),
                    x.get("reason_short", "no reason recorded")))
        if x.get("reason_full"):
            b.append("%s\n\n" % x["reason_full"])
        if x.get("documents_needed"):
            b.append("**What would unblock it:**\n\n")
            for d in x["documents_needed"]:
                b.append("- %s\n" % d)
            b.append("\n")
        if x.get("would_still_be_short"):
            b.append("**And what would still be missing.** %s\n\n"
                     % x["would_still_be_short"])
        if x.get("what_was_still_learned"):
            b.append("**What was learned anyway.** %s"
                     % x["what_was_still_learned"])
            if x.get("lessons"):
                b.append(" (%s)" % ", ".join(x["lessons"]))
            b.append("\n\n")
        if x.get("not_filed"):
            b.append("**What could not be recorded.** %s\n\n" % x["not_filed"])

    # ---- remaining ------------------------------------------------------
    b.append("## Stocks still to be calibrated\n\n"
             "*Resolved from the campaign queue at the moment this document "
             "was built, in the order the campaign runs them — never written "
             "down and kept by hand. A name leaves this list the moment its "
             "run exists.*\n\n")
    b.append("| Market | Still to go | Names, in queue order |\n"
             "|---|---|---|\n")
    for label, rows in rem["by_market"].items():
        b.append("| %s | %d | %s |\n"
                 % (label, len(rows), ", ".join(r["ticker"] for r in rows)))
    if rem["excluded"]:
        ex = ", ".join(e[0] if isinstance(e, (tuple, list)) else str(e)
                       for e in rem["excluded"])
        why = (rem["excluded"][0][1]
               if isinstance(rem["excluded"][0], (tuple, list))
               else "excluded by construction")
        b.append("\n%d name%s excluded from the campaign by construction "
                 "(%s) — %s, so there is no forecasting method to test.\n"
                 % (len(rem["excluded"]),
                    "" if len(rem["excluded"]) == 1 else "s", ex, why))
    b.append("\nThe campaign stops after the first market to review whether "
             "the method generalises before the next one begins, so this list "
             "is an order rather than a schedule.\n")
    return "".join(b)


HEAD = """# The Lessons Register

**Every lesson this project has learned, in plain language, and how far each one
travels.**

> **NOTHING IN THIS REGISTER BINDS ANY STUDY.** It is a record, not a gate. No
> standing rule refers to it and no quality gate consults it, deliberately —
> the walk-forward method that produced its strongest lessons has not itself
> been validated. One company has been through a run; that run's own training
> record states its corrections rest on two starting points, its intervals are
> wide with several straddling zero, and its observations are not independent.
> The house rule is that nothing enters the method without surviving the same
> out-of-sample test the forecasts must survive, and a finding measured on one
> name has not survived it. **Every walk-forward lesson is therefore marked
> PROVISIONAL** and stays that way until the method is validated across more
> names. Read this register to think with; do not cite it as authority.

GENERATED FROM `lessons_register.py` — do not edit this file by hand. Edits here
are overwritten; `scripts/check_lessons_register.py` fails the build if the two
disagree.

---

## How to read this

A lesson is useless until you know how far it carries. Every entry is therefore
tagged with one of three scopes, and the difference is not a matter of taste.

| scope | means | who must read it |
|---|---|---|
| **ALL** | true of every study we will ever run — about method, arithmetic, or how work gets checked | every study, every time |
| **CLASS** | true of every company that works the same way (every off-plan developer, every telecom operator) | the next study of that class only |
| **STOCK** | true of this one company and nothing else — a quirk of its disclosure, history or accounting | that company's next update only |

**Applying a STOCK lesson to another company is superstition.** Applying an ALL
lesson is mandatory. The middle category is where most of the value is, and it
is the one that takes longest to fill.

Every lesson also records **how it was learned**, because the strength of the
evidence differs enormously:

- **walk-forward test** — measured against real outcomes across many starting
  points. The strongest evidence this project produces.
- **outside critique** — found by an external reviewer of a delivered study.
- **self-audit** — found by re-examining our own work before anyone else read it.
- **found while building** — usually because a check reported clean on something
  it was not actually looking at.

Where two lessons disagree, the walk-forward one wins.

And every lesson carries **what would overturn it**. A lesson with no falsifier
is a habit, not a finding, and habits are how a method quietly stops being
tested.

---

## What is in here, and what is honestly missing

"""


def _row(x):
    lines = []
    lines.append("### %s · %s\n" % (x["id"], x["headline"]))
    lines.append(x["plain"] + "\n")
    if x["scope"] == "ALL":
        who = "**Applies to:** every study"
    elif x["scope"] == "CLASS":
        who = "**Applies to:** every %s" % x["applies_to"]
    else:
        who = "**Applies to:** %s only" % x["applies_to"]
    tail = "" if x["status"] == "adopted" else "  ·  **status: %s**" % x["status"]
    lines.append("%s  ·  *Learned from:* %s, %s%s\n"
                 % (who, ORIGIN_WORDS[x["origin"]], x["source"], tail))
    lines.append("> **What it cost, or how we know.** %s\n" % x["evidence"])
    lines.append("> **What would overturn it.** %s\n" % x["overturned_by"])
    return "\n".join(lines) + "\n"


def build():
    LR.assert_lessons_register()
    c = LR.counts()
    body = [HEAD]
    body.append(status_block())
    pop = population()
    body.append(
        "**%d lessons**, of which %d bind on every study, %d on a class of "
        "company, and %d on a single name.\n\n"
        "By how they were learned: %d from fundamental walk-forward testing, "
        "%d from price-engine walk-forward testing, %d from outside critiques, "
        "%d from self-audits, %d found while building.\n\n"
        "### Two different tests are both called a walk-forward\n\n"
        "They test different machinery on different evidence, and the first "
        "edition of this register conflated them — which understated the "
        "evidence base badly and is recorded here rather than quietly "
        "corrected.\n\n"
        "| | what it tests | names | resolved forecasts |\n|---|---|---|---|\n"
        "| **Fundamental** | the forecasting method — project each driver from "
        "a past origin, score revenue, cost and profit against what happened |"
        " %d (%s) | 10 origins x 5 horizons |\n"
        "| **Price engine** | the probability cone — strike it at a past "
        "origin and score band coverage and a proper score against a naive "
        "rule | %d | %d |\n\n"
        "**The price engine is well tested; the fundamental method is not.** "
        "%d names carry price-engine evidence, including DU (%s forecasts) and "
        "GBCO (%s). The fundamental method has been through a full training run "
        "on %s alone, and that run's own record states its corrections rest on "
        "two starting points, its intervals are wide with several straddling "
        "zero, and its observations are not independent. **Every lesson from "
        "the fundamental method is therefore marked PROVISIONAL**; price-engine "
        "lessons are not, because they rest on %d forecasts across %d names.\n"
        % (c["total"], c["ALL"], c["CLASS"], c["STOCK"],
           c["by_origin"]["walk_forward_fundamental"],
           c["by_origin"]["walk_forward_price"], c["by_origin"]["critique"],
           c["by_origin"]["self_audit"], c["by_origin"]["build"],
           len(pop["fundamental"]), ", ".join(pop["fundamental"]),
           len(pop["price"]), pop["price_origins"], len(pop["price"]),
           dict(pop["price"]).get("DU", "no"),
           dict(pop["price"]).get("GBCO", "no"),
           " and ".join(pop["fundamental"]),
           pop["price_origins"], len(pop["price"])))

    outstanding = [x for x in LR.LESSONS if x["status"] == "outstanding"]
    if outstanding:
        body.append("\n**Not yet acted on (%d):** %s. These are recorded as "
                    "open rather than quietly carried as done.\n"
                    % (len(outstanding),
                       ", ".join("%s (%s)" % (x["id"], x["headline"].rstrip("."))
                                 for x in outstanding)))

    body.append("\n---\n\n# Lessons that bind on EVERY study\n\n"
                "*Read these before starting any study, of any company, in any "
                "market.*\n\n")
    for x in sorted([l for l in LR.LESSONS if l["scope"] == "ALL"],
                    key=lambda y: y["id"]):
        body.append(_row(x))

    body.append("\n---\n\n# Lessons that bind on a CLASS of company\n\n"
                "*Read the section for the class being studied. Do not read "
                "across classes — a rule true of developers is not evidence "
                "about airlines.*\n")
    for k in LR.CLASSES:
        rows = sorted([l for l in LR.LESSONS
                       if l["scope"] == "CLASS" and l["applies_to"] == k],
                      key=lambda y: y["id"])
        if not rows:
            continue
        body.append("\n## %s\n\n" % (k[0].upper() + k[1:]))
        for x in rows:
            body.append(_row(x))

    body.append("\n---\n\n# Lessons that bind on ONE company\n\n"
                "*Read only the section for the company being updated. These do "
                "not generalise and must not be applied to another name.*\n")
    for t in sorted({l["applies_to"] for l in LR.LESSONS
                     if l["scope"] == "STOCK"}):
        body.append("\n## %s\n\n" % t)
        for x in sorted([l for l in LR.LESSONS
                         if l["scope"] == "STOCK" and l["applies_to"] == t],
                        key=lambda y: y["id"]):
            body.append(_row(x))

    body.append("\n---\n\n## Adding a lesson\n\n"
                "A walk-forward run, a critique response or a QC gate that "
                "produced a finding worth keeping appends it to "
                "`lessons_register.py` and regenerates this file in the same "
                "commit. Every entry needs a plain-English statement, a scope, "
                "the evidence, and what would overturn it — the module refuses "
                "an entry missing any of them, and refuses a class name that is "
                "not registered.\n\n"
                "**Choosing the scope is the judgement, and getting it wrong is "
                "costly in both directions.** Too narrow and the next study "
                "repeats the mistake. Too broad and a company's quirk becomes a "
                "house rule nobody can dislodge. When genuinely unsure, record "
                "it at the narrower scope and widen it when a second company "
                "shows the same thing — one observation is not a pattern.\n")
    return "".join(body)


if __name__ == "__main__":
    text = build()
    open(OUT, "w").write(text)
    print("wrote %s (%d chars)" % (os.path.basename(OUT), len(text)))
    c = LR.counts()
    print("  ALL %d · CLASS %d · STOCK %d · total %d"
          % (c["ALL"], c["CLASS"], c["STOCK"], c["total"]))
