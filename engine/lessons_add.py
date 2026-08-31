"""Append confirmed drafts into the register, and close the loop.

Reads a run's `lessons_draft.json`, appends every draft whose scope has been
decided and marked `confirmed: true`, regenerates `Lessons_Register.md`, and
writes the outcome back into the draft file so NOTHING IS SILENTLY DROPPED.

Every draft ends in one of exactly two states:

  registered : "L-nnn"       it is in the register
  declined   : "<reason>"    a deliberate decision, with the reason recorded

A draft in neither state fails the gate. That is the whole point: the harvester
finds candidates mechanically, but a candidate nobody ruled on is not a clean
result, it is an unanswered question wearing the costume of one.

Refuses, loudly:
  - an unconfirmed draft (the scope judgement has not been made)
  - scope UNSCOPED, or a CLASS scope naming an unregistered class
  - a lesson with no falsifier
  - a headline that already exists in the register, which usually means the
    same finding is being filed twice under two ids
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import lessons_register as LR
import build_lessons_register as BUILD

SRC = os.path.join(HERE, "lessons_register.py")


def _next_id(scope):
    """Ids are blocked by scope: 0xx ALL, 1xx CLASS, 2xx STOCK."""
    base = {"ALL": 0, "CLASS": 100, "STOCK": 200}[scope]
    used = [int(x["id"].split("-")[1]) for x in LR.LESSONS
            if base < int(x["id"].split("-")[1]) <= base + 99]
    return "L-%03d" % ((max(used) if used else base) + 1)


def _py(s):
    """A python string literal, wrapped to stay inside the file's own margin."""
    import textwrap
    parts = textwrap.wrap(s, 62) or [""]
    if len(parts) == 1:
        return '"%s"' % parts[0].replace('\\', '\\\\').replace('"', '\\"')
    return "\n".join('      "%s"' % (p.replace('\\', '\\\\')
                                     .replace('"', '\\"')
                                     + ("" if i == len(parts) - 1 else " "))
                     for i, p in enumerate(parts)).lstrip()


def render(x, lesson_id, source):
    subject = "None" if x["scope"] == "ALL" else _py(x["applies_to"])
    return (
        '\n    L("%s", "%s", %s,\n'
        '      %s,\n      %s,\n      %s,\n      "%s",\n      %s,\n      %s'
        '%s),\n'
        % (lesson_id, x["scope"], subject, _py(x["headline"]), _py(x["plain"]),
           _py(source), x["origin"], _py(x["evidence"]),
           _py(x["overturned_by"]),
           "" if x.get("status", "adopted") == "adopted"
           else ',\n      "%s"' % x["status"]))


def main(argv):
    if len(argv) < 2:
        print("usage: python3 engine/lessons_add.py <TICKER> [draft.json]")
        return 2
    ticker = argv[1].upper()
    draft_path = argv[2] if len(argv) > 2 else os.path.join(
        HERE, "%s_walkforward" % ticker.lower(), "lessons_draft.json")
    if not os.path.exists(draft_path):
        print("no draft file at %s — run lessons_harvest.py first" % draft_path)
        return 1

    doc = json.load(open(draft_path))
    drafts = doc["drafts"]
    source = doc.get("source") or "%s walk-forward, %s" % (
        ticker, doc.get("run_date", "date not recorded"))

    ready, problems, skipped = [], [], []
    existing_headlines = {x["headline"].lower() for x in LR.LESSONS}
    for x in drafts:
        if x.get("registered") or x.get("declined"):
            skipped.append(x["proposed_id"])
            continue
        if not x.get("confirmed"):
            problems.append("%s: not confirmed — decide its scope first, or "
                            "set declined:'<reason>'" % x["proposed_id"])
            continue
        if x["scope"] not in ("ALL", "CLASS", "STOCK"):
            problems.append("%s: scope is %r; it must be ALL, CLASS or STOCK"
                            % (x["proposed_id"], x["scope"]))
            continue
        if x["scope"] != "ALL" and not x.get("applies_to"):
            problems.append("%s: a %s lesson must name its subject"
                            % (x["proposed_id"], x["scope"]))
            continue
        if x["scope"] == "CLASS" and x.get("applies_to") not in LR.CLASSES:
            problems.append("%s: %r is not a registered class; add it to "
                            "CLASSES first" % (x["proposed_id"],
                                               x.get("applies_to")))
            continue
        if not x.get("overturned_by"):
            problems.append("%s: no falsifier — a lesson with nothing that "
                            "would overturn it is a habit" % x["proposed_id"])
            continue
        if x["headline"].lower() in existing_headlines:
            problems.append("%s: a lesson with this headline is already "
                            "registered" % x["proposed_id"])
            continue
        ready.append(x)

    if problems:
        print("REFUSED — %d draft(s) not ready:" % len(problems))
        for p in problems:
            print("  - %s" % p)
        return 1
    if not ready:
        print("nothing to add (%d already resolved)" % len(skipped))
        return 0

    src = open(SRC).read()
    anchor = "]\n\n\ndef assert_lessons_register"
    assert anchor in src, "cannot find the end of LESSONS in lessons_register.py"
    block = ""
    for x in ready:
        lid = _next_id(x["scope"])
        block += render(x, lid, source)
        x["registered"] = lid
        # keep _next_id honest across several appends in one run
        LR.LESSONS.append({"id": lid, "scope": x["scope"],
                           "applies_to": x.get("applies_to")})
    src = src.replace(anchor, block + anchor, 1)
    open(SRC, "w").write(src)

    # VERIFY BY IMPORT, NOT BY PARSE, before anything downstream trusts it
    import importlib
    importlib.reload(LR)
    LR.assert_lessons_register()
    importlib.reload(BUILD)
    open(os.path.join(HERE, "Lessons_Register.md"), "w").write(BUILD.build())

    json.dump(doc, open(draft_path, "w"), indent=1)
    c = LR.counts()
    print("added %d lesson(s): %s"
          % (len(ready), ", ".join(x["registered"] for x in ready)))
    print("register now holds %d — ALL %d · CLASS %d · STOCK %d"
          % (c["total"], c["ALL"], c["CLASS"], c["STOCK"]))
    print("Lessons_Register.md regenerated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
