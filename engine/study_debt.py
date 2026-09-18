"""What the book owes, counted in one place, anchored on the ratchets themselves.

[R-ENF-02] is right that a ratchet is the way to carry a known debt: a check red from
the day it is written is one everybody learns to ignore. [R-REPAIR-01] is right that a
system which only detects accumulates debt at exactly the rate it detects, and that
every individual entry is legitimate, which is what makes the total invisible.

NOBODY HAD COUNTED THE TOTAL. [R-REPAIR-01] was adopted on "47 ratchet entries
accumulated on five studies", read off the lists somebody happened to open. Measured
18-09-2026 across every ratchet in engine/build_depth_audit/, the real figure is far
larger, and the gap between the two numbers is the whole argument for this module: a
debt nobody counts is a debt nobody pays down.

IT INVENTS NO REGISTER. A hand-curated list of what each study owes would rot exactly
as the stale-library list did, and for the same reason -- a ratchet moves when somebody
prunes it and a hand list moves when somebody remembers. So the population IS the
ratchets, read live, and this module only classifies and counts.

AN UNRECOGNISED KEY IS RED, NEVER SKIPPED. Sixty-seven files carry a dozen key shapes
and a reader that guesses silently finds nothing and reports that as a result -- the
failure this project has now caught five times in one week. Every key is classified by
a NAMED rule or the file is refused.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RATCHETS = os.path.join(HERE, "build_depth_audit")

# THE CLASSIFICATION IS BY NAME AND THE LIST IS CLOSED, for [R-COC-01 AMENDED]'s
# reason: an open list lets a ratchet opt out of being counted by inventing a key.
DEBT = ("outstanding", "breaching", "unreadable", "failing", "no_check", "red",
        "red_detail", "records", "skipped", "tree_dirty", "held_unregistered",
        # EACH OF THESE WAS CLASSIFIED BY LOOKING AT IT, not by a pattern. The reader
        # refused all eleven on its first run and every one needed a decision:
        "unrunnable",              # a figure script that cannot run -- red, never skipped
        "findings",                # table-footing findings, one per defect
        "breach_no_review",        # a gap past the trigger with no eight-heading review
        "review_central_unstated",  # a review that does not say what it audited
        "unscored",                # a terminal whose charge never resolved, so untested
        "runs")                    # walk-forward runs owing a valuation-input block
NOT_DEBT = ("pruned", "pruned_on", "conforming_at_adoption", "conforming", "added",
            "members", "peers", "subjects", "candidate_sets", "documents", "figures",
            "measurements", "reasons", "exempt", "resolved", "why_each", "entries",
            "adopted", "seeded", "note", "rule", "_",
            "closed",              # entries RESOLVED and kept as the record of why
            "aliases",             # a name mapping, not a debt
            "signature",           # [R-ENF-08] failure signatures beside their entries
            "scope_widened")       # a dated record that a gate's scope grew
PROSE = re.compile(r'^(_|note|rule|why|measurement|reason|seeded|adopted|generated|'
                   r'source|date|as_of|version)', re.I)

# A TICKER MAY START WITH A DIGIT AND ONE IN THIS BOOK DOES. The first draft required
# a leading letter and silently dropped 2POINTZERO -- the same name the standing rule
# already records as having been dropped from three separate tools by a regex matching
# unquoted object keys. COUNT AGAINST A KNOWN TOTAL: it was found because the reader
# refuses an unclassified key rather than skipping it, and this one arrived as a key it
# could not place.
TICKER = re.compile(r'^[A-Z0-9][A-Z0-9_]{1,13}$')


class UnknownShape(Exception):
    """A ratchet whose key this module cannot classify. RED, never skipped."""


def _tickers(v):
    """Every ticker-shaped name in a list or a dict's keys."""
    if isinstance(v, list):
        return [x for x in v if isinstance(x, str) and TICKER.match(x)]
    if isinstance(v, dict):
        return [k for k in v if TICKER.match(k)]
    return []


def read_one(path):
    """{ticker: [key, ...]} of DEBT entries in one ratchet, and its unclassified keys."""
    with open(path, encoding="utf-8") as fh:
        j = json.load(fh)
    debt, unknown = {}, []
    if isinstance(j, list):
        # a bare list IS the outstanding list -- one file in the book ships this way
        for tk in _tickers(j):
            debt.setdefault(tk, []).append("outstanding")
        return debt, unknown
    if not isinstance(j, dict):
        raise UnknownShape("%s: top level is %s" % (os.path.basename(path), type(j).__name__))
    for k, v in j.items():
        base = k.lower()
        if PROSE.match(base) or isinstance(v, (str, int, float, bool)) or v is None:
            continue
        if base in DEBT:
            for tk in _tickers(v):
                debt.setdefault(tk, []).append(k)
        elif base in NOT_DEBT:
            continue
        elif TICKER.match(k):
            # a ratchet keyed BY TICKER at the top level: the entry itself is the debt
            debt.setdefault(k, []).append("entry")
        else:
            unknown.append(k)
    return debt, unknown


def survey():
    """(per-ticker debt, files read, unclassified [(file, key), ...])."""
    by_tk, files, unknown = {}, 0, []
    for f in sorted(os.listdir(RATCHETS)):
        if not f.endswith(".json"):
            continue
        p = os.path.join(RATCHETS, f)
        name = f.replace("_outstanding.json", "").replace(".json", "")
        try:
            debt, unk = read_one(p)
        except (ValueError, OSError) as exc:
            raise UnknownShape("%s will not parse: %s" % (f, str(exc)[:60]))
        files += 1
        unknown += [(f, k) for k in unk]
        for tk, keys in debt.items():
            by_tk.setdefault(tk, set()).update("%s:%s" % (name, k) for k in keys)
    return {k: sorted(v) for k, v in by_tk.items()}, files, unknown


def report():
    by_tk, files, unknown = survey()
    total = sum(len(v) for v in by_tk.values())
    lines = ["%d ratchet file(s) read; %d stud%s carrying a recorded debt; %d entries "
             "in total" % (files, len(by_tk), 'y' if len(by_tk) == 1 else 'ies', total)]
    for tk, v in sorted(by_tk.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        lines.append("  %-13s %2d  %s" % (tk, len(v), ", ".join(x.split(":")[0]
                                                               for x in v)[:110]))
    return lines, by_tk, files, unknown


if __name__ == "__main__":
    for l in report()[0]:
        print(l)
