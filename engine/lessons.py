"""Read the lessons register.  [R-LESSON-01]

  python3 engine/lessons.py                 everything that binds on every study
  python3 engine/lessons.py PHDC            every ALL lesson + PHDC's own
  python3 engine/lessons.py PHDC --class developer
  python3 engine/lessons.py --classes       what classes are registered
  python3 engine/lessons.py --scope CLASS   one scope only
  python3 engine/lessons.py --search cash   anything mentioning a word
  python3 engine/lessons.py --open          what is recorded and not yet acted on
  python3 engine/lessons.py --counts        the live counts, never from a document
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import lessons_register as LR

ORIGIN = {"walk_forward_fundamental": "fundamental walk-forward test",
          "walk_forward_price": "price-engine walk-forward test",
          "critique": "outside critique", "self_audit": "self-audit",
          "build": "found while building"}


def show(rows, header):
    print("\n%s — %d lesson%s\n" % (header, len(rows), "" if len(rows) == 1 else "s"))
    for x in rows:
        who = ("every study" if x["scope"] == "ALL"
               else "every %s" % x["applies_to"] if x["scope"] == "CLASS"
               else "%s only" % x["applies_to"])
        flag = "" if x["status"] == "adopted" else "  [%s]" % x["status"].upper()
        print("  %s  %s%s" % (x["id"], x["headline"], flag))
        print("      %s" % x["plain"])
        print("      applies to %s · learned from a %s · %s"
              % (who, ORIGIN[x["origin"]], x["source"]))
        print("      how we know: %s" % x["evidence"])
        print("      overturned by: %s\n" % x["overturned_by"])


def resolve_class(word):
    if not word:
        return None
    hits = [c for c in LR.CLASSES if word.lower() in c.lower()]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise SystemExit("no registered class matches %r. Registered: %s"
                         % (word, "; ".join(LR.CLASSES)))
    raise SystemExit("%r matches several classes: %s" % (word, "; ".join(hits)))


def main(argv):
    LR.assert_lessons_register()
    args = [a for a in argv[1:]]
    if "--classes" in args:
        print("\nregistered classes\n")
        for c in LR.CLASSES:
            n = sum(1 for x in LR.LESSONS
                    if x["scope"] == "CLASS" and x["applies_to"] == c)
            print("  %-52s %d lesson%s" % (c, n, "" if n == 1 else "s"))
        print()
        return 0
    c = LR.counts()
    if "--counts" in args:
        print("\n  total %d — ALL %d · CLASS %d · STOCK %d" %
              (c["total"], c["ALL"], c["CLASS"], c["STOCK"]))
        print("  by how it was learned: " + " · ".join(
            "%s %d" % (ORIGIN[k], v) for k, v in c["by_origin"].items()))
        print("  by status: " + " · ".join("%s %d" % (k, v)
                                           for k, v in c["by_status"].items()))
        print()
        return 0
    if "--open" in args:
        show([x for x in LR.LESSONS if x["status"] != "adopted"],
             "Recorded and not yet acted on")
        return 0
    if "--search" in args:
        w = args[args.index("--search") + 1].lower()
        hits = [x for x in LR.LESSONS
                if w in (x["headline"] + x["plain"] + x["evidence"]
                         + str(x["applies_to"])).lower()]
        show(hits, "Lessons mentioning %r" % w)
        return 0
    if "--scope" in args:
        s = args[args.index("--scope") + 1].upper()
        show([x for x in LR.LESSONS if x["scope"] == s],
             "Lessons scoped %s" % s)
        return 0

    klass = None
    if "--class" in args:
        klass = resolve_class(args[args.index("--class") + 1])
        args = [a for i, a in enumerate(args)
                if i not in (args.index("--class"), args.index("--class") + 1)]
    ticker = next((a for a in args if not a.startswith("-")), None)

    rows = LR.lessons_for(ticker, klass)
    who = "every study"
    if ticker and klass:
        who = "a %s update (%s)" % (ticker.upper(), klass)
    elif ticker:
        who = "a %s update" % ticker.upper()
    elif klass:
        who = "a new %s study" % klass
    show(rows, "What binds on %s" % who)

    # The widening path, printed under its own heading and never mixed into the
    # set above. These are other companies' single-company lessons: they do NOT
    # bind here, and the only legitimate use is to check whether the same thing
    # happens on this name too. If it does, that is the second observation the
    # scope rule waits for and the lesson is refiled at CLASS scope.
    if klass:
        watch = LR.watchlist(klass, ticker)
        if watch:
            print("\nDoes any of this repeat here? — %d single-company lesson%s "
                  "from other %s\n" % (len(watch), "" if len(watch) == 1 else "s",
                                       klass))
            print("  These do NOT bind on this name. Applying one as-is would be "
                  "superstition.\n  Check each against this company's own "
                  "numbers; where one repeats, that is the\n  second observation "
                  "and the lesson is refiled at class scope.\n")
            for x in watch:
                print("  %s  %s   [%s only]" % (x["id"], x["headline"],
                                                x["applies_to"]))
                print("      %s\n" % x["plain"])

    if not ticker and not klass:
        print("  (%d more bind on a class or a single name — "
              "add a ticker or --class to see them)\n"
              % (c["CLASS"] + c["STOCK"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
