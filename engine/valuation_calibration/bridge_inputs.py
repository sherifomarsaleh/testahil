"""What the walk-forwards actually commit toward a VALUE, item by item, origin by origin.

WHY THIS EXISTS. [R-VCAL-01]'s pre-registration commits series (a): a fair value
rebuilt at every origin from the drivers the statement walk-forwards produce, with
no judgement. Twice a construction has been declared for that series and twice the
binding question turned out to be the same one, asked too late: *is the input even
committed?* The first developer declaration capitalised earnings because a
cash-flow lens needs capital expenditure and working capital and neither was to
hand; the second fell back to the order book for the same reason. Arguing about
which lens to declare next is the wrong move. THE QUESTION IS A MEASUREMENT.

WHAT A VALUE NEEDS, AND WHY EACH ITEM IS HERE

  cash    the bridge's largest single swing on this book — AMOC is a net-cash
          company, so omitting cash there is not a rounding error, it is most of
          the answer. [R-BRIDGE-01] (iii).
  debt    the other side of the same bridge.
  capex   the reinvestment a flow lens must subtract.
  ppe     recorded because capex is DERIVABLE from it: capex = ΔPPE + D&A, an
          identity, not an assumption. A cell with PPE in two consecutive years
          and a depreciation charge can produce a capex figure honestly; a cell
          with neither cannot, and the difference is worth measuring.
  dep     recorded SEPARATELY from capex, because "capex = depreciation" is an
          assumption a reader must be able to see being made.
  wc      the working-capital movement.
  shares  the count that turns an equity value into a price — a FOOTED count
          read off that year's own filing, never today's count carried back.
  cap     the paid-in capital in currency, recorded SEPARATELY because it is not
          a share count: it becomes one only when divided by the par value, which
          is a figure from the same note and is not yet read. Crediting a cell
          with a share count it does not have is the fabrication this whole
          archive exists to refuse, so the two are different rows.

TWO SOURCES, AND THE SECOND ONE IS THE POINT OF THE FIRST. Since [R-FCAL-01
AMENDED] a run commits a VALUATION-INPUT BLOCK beside its driver panel —
`valuation_inputs.json`, named items, a value or an explicit missing-with-a-reason
for each — and that record is read first and needs no key map. What follows is for
the runs that predate the amendment, which committed whatever their own schema
happened to carry. An item recorded MISSING is not credited: recording it is what
makes the gap visible, and crediting it would undo that.

HOW IT MATCHES, AND WHY THE MAP IS EXPLICIT. The five runs share no schema and
several use abbreviations — TMGH writes `da` for depreciation and `nr_undelivered`
for notes receivable, PHDC writes `bs.ar` and `bs.np_short`. A regex broad enough
to catch `da` and `ar` would match a third of the keys in the repository; a regex
narrow enough to be safe reported TMGH as carrying no depreciation and PHDC as
carrying no working capital, which is how the first cut of this module UNDERSTATED
two of the five runs. So the map is NAMED PER RUN, the way export_panels.SOURCES
is, and the regex survives only as a GUARD: every key it matches that the map does
not claim is printed as unclaimed, so the next run's vocabulary cannot go missing
in silence. A named map that is wrong is visible; a regex that is silently narrow
is not [R-ENF-04].

WHY THE DIRECTION OF WHAT IS MISSING MATTERS MORE THAN THE COUNT. The whole
reassessment tests whether this house leans pessimistic. Each omission has a KNOWN
SIGN: no cash understates equity value, no capex overstates it, no working capital
does either depending on growth. An instrument assembled from whatever happens to
be present carries a bias whose direction is set by which items are missing — so
it varies from cell to cell, and a bias that varies in unknown direction is worse
than one that is merely large. That is why this module reports the missing items
and their signs rather than a completeness percentage.

IT VALUES NOTHING AND DECIDES NOTHING. It reports. The lens declaration that
follows is written against what this measures, in that order, and never the
reverse.
"""
from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, ENGINE)

import panel as P  # noqa: E402  (the calibration panel, not a run's own)

CANDIDATES = ("panel.json", "panel_annual.json", "panel_export.json",
              "panel_kpi_verified.json", "bottom_up.json", "fs_parsed.json",
              "legacy_parsed.json")

SIGN = {
    "cash": "understates equity value",
    "debt": "overstates equity value",
    "capex": "overstates equity value",
    "ppe": "no direct sign — it is what makes capex derivable",
    "dep": "no direct sign — it is what a declared capex substitution would use",
    "wc": "sign depends on growth",
    "shares": "no value can be compared with a price at all",
    "cap": "not a share count on its own — it needs the par value beside it",
}
ITEMS = ["cash", "debt", "capex", "ppe", "dep", "wc", "shares", "cap"]

# The record [R-FCAL-01 AMENDED] defines, which a run commits BESIDE its driver
# panel. It is read first and needs no key map: the amendment names the items, so
# a run that commits it has no private vocabulary for this module to have read
# wrongly. The named map below stays for the runs that predate the amendment —
# they committed whatever their own schema happened to carry, and only a named
# map can find it. A run appearing in both is not double-counted; the same item
# simply resolves through two files and both are reported.
STANDARD = "valuation_inputs.json"

# The leaf keys each run actually uses. Named, not guessed — see the header.
MAP = {
    "AMOC": {
        "dep": ["cost_stack.depreciation"],
    },
    "ARCC": {
        "debt": ["debt.total", "debt.noncurrent", "debt.current_portion",
                 "debt.credit_facilities"],
        "dep": ["cost.mfg_dep", "cost.amort"],
    },
    "EGCH": {
        "debt": ["borrowings.bank", "borrowings.holdco", "borrowings.current"],
    },
    "PHDC": {
        "cash": ["bs.cash"],
        "debt": ["bs.loans_current", "bs.loans_lt", "bs.banks_credit"],
        "ppe": ["bs.fixed_assets", "bs.investment_property",
                "bs.projects_under_constr"],
        "wc": ["bs.ar", "bs.nr_short", "bs.nr_long", "bs.np_short", "bs.np_long",
               "bs.wip", "bs.advances_customers", "bs.total_current_assets",
               "bs.total_current_liabs"],
    },
    "TMGH": {
        "cash": ["cash", "time_deposits_c", "time_deposits_nc"],
        "debt": ["current_loans", "lt_loans", "sukuk_current", "bank_facilities",
                 "lease_liab_c", "lease_liab_nc", "interest_bearing_debt"],
        "capex": ["capex"],
        "ppe": ["ppe", "development_properties", "investment_properties", "puc"],
        "dep": ["da"],
        "wc": ["inventories", "notes_receivable", "notes_payable", "creditors",
               "customer_advances", "other_current_assets", "total_ca", "total_cl"],
        "cap": ["paid_capital"],
    },
}

# The guard. Anything this matches that the map does not claim is REPORTED, so a
# run whose vocabulary nobody has read yet cannot be scored as empty.
GUARD = re.compile(
    r"cash|deposit|debt|borrow|loan|facilit|sukuk|lease_liab|capex|"
    r"capital[._]?expenditure|ppe|fixed[._]?asset|investment[._]?propert|"
    r"development[._]?propert|deprec|amort|receivab|payab|inventor|creditor|"
    r"advance|working[._]?capital|paid[._]?capital|share", re.I)


def _is_number(v):
    if isinstance(v, bool):
        return False
    if isinstance(v, (int, float)):
        return True
    if isinstance(v, list) and v and isinstance(v[0], (int, float)):
        return True                      # a [current, comparative] column pair
    if isinstance(v, dict):
        return _is_number(v.get("value"))
    return False


def _year_of(key):
    m = re.fullmatch(r"(?:FY)?((?:19|20)\d{2})", str(key))
    return int(m.group(1)) if m else None


def scan_file(path, claims):
    """({year: {item: [where]}}, {leaf: [where]}) — claimed, and guard-unclaimed."""
    try:
        doc = json.load(open(path, encoding="utf-8"))
    except Exception:
        return {}, {}
    want = {}
    for item, keys in claims.items():
        for k in keys:
            want[k.lower()] = item
    out, unclaimed = {}, {}

    def walk(node, year, trail):
        if isinstance(node, dict):
            for k, v in node.items():
                y = _year_of(k)
                walk(v, y if y else year, trail + "/" + str(k))
            return
        if isinstance(node, list) and node and isinstance(node[0], (dict, list)):
            for i, v in enumerate(node[:40]):
                walk(v, year, trail + "[%d]" % i)
            return
        if year is None or not _is_number(node):
            return
        leaf = trail.split("/")[-1].lower()
        item = want.get(leaf)
        if item:
            out.setdefault(year, {}).setdefault(item, []).append(trail)
        elif GUARD.search(leaf):
            unclaimed.setdefault(leaf, []).append(trail)

    walk(doc, None, "")
    return out, unclaimed


def scan_standard(path):
    """{year: {item: [where]}} from the record [R-FCAL-01 AMENDED] defines.

    An item marked MISSING is not present — that is the whole point of recording
    it as missing rather than omitting it, and crediting a cell for a recorded
    absence would turn the clause that makes gaps visible into one that hides
    them. `cap` is credited from the share record's own issued capital, which is
    where the amendment puts it: the count and the capital it was footed against
    live in one record rather than two rows.
    """
    try:
        doc = json.load(open(path, encoding="utf-8"))
    except Exception:
        return {}
    out = {}
    for key, block in (doc.get("origins") or {}).items():
        y = _year_of(key)
        if y is None or not isinstance(block, dict):
            continue
        for item, rec in block.items():
            if item not in ITEMS or not isinstance(rec, dict):
                continue
            if "missing" in rec or not _is_number(rec.get("value")):
                continue
            out.setdefault(y, {}).setdefault(item, []).append(
                "/origins/%s/%s" % (key, item))
            if item == "shares" and _is_number(rec.get("issued_capital")):
                out[y].setdefault("cap", []).append(
                    "/origins/%s/shares/issued_capital" % key)
    return out


def census():
    found, files, loose = {}, {}, {}
    for tk, rundir in P.runs().items():
        claims = MAP.get(tk, {})
        agg, seen, un = {}, [], {}
        p = os.path.join(rundir, STANDARD)
        if os.path.exists(p):
            got = scan_standard(p)
            if got:
                seen.append(STANDARD)
                for y, items in got.items():
                    for item, wheres in items.items():
                        agg.setdefault(y, {}).setdefault(item, [])
                        agg[y][item].extend("%s:%s" % (STANDARD, w) for w in wheres[:2])
        for fn in CANDIDATES:
            p = os.path.join(rundir, fn)
            if not os.path.exists(p):
                continue
            got, unc = scan_file(p, claims)
            if got:
                seen.append(fn)
                for y, items in got.items():
                    for item, wheres in items.items():
                        agg.setdefault(y, {}).setdefault(item, [])
                        agg[y][item].extend("%s:%s" % (fn, w) for w in wheres[:2])
            for leaf, wheres in unc.items():
                un.setdefault(leaf, set()).add(fn)
        found[tk] = agg
        files[tk] = seen
        loose[tk] = un
    return found, files, loose


def report(market="EG"):
    found, files, loose = census()
    if not found:
        raise SystemExit("REFUSED: no walk-forward run directories were examined. "
                         "An empty census is not a clean census [R-ENF-04].")
    declared = [int(o["year"]) for o in P.MH.load(market).get("origins", [])]
    names = sorted(found)
    key = {"cash": "c", "debt": "d", "capex": "x", "ppe": "f", "dep": "p",
           "wc": "w", "shares": "s", "cap": "k"}

    print("what the walk-forwards commit toward a VALUE — %s\n" % market)
    print("  key:  c cash   d debt   x capex   f fixed assets/PPE   "
          "p depreciation\n        w working capital   s footed share count   "
          "k paid-in capital (not a count)\n")
    head = "  %-8s " % "origin" + " ".join("%-10s" % n[:10] for n in names)
    print(head)
    print("  " + "-" * (len(head) - 2))

    tally = {i: 0 for i in ITEMS}
    per_cell, cells = {}, 0
    for y in declared:
        row = "  %-8d " % y
        for tk in names:
            have = set(found.get(tk, {}).get(y, {}))
            if P.SHARES.get(tk, {}).get(str(y)):
                have.add("shares")
            per_cell[(tk, y)] = have
            cells += 1
            for i in have:
                tally[i] += 1
            row += "%-10s " % ("".join(key[i] for i in ITEMS if i in have) or "·")
        print(row.rstrip())

    print("\n  present, out of %d name-origin cells:" % cells)
    for i in ITEMS:
        print("    %-7s %3d  (%3.0f%%)   absent → %s"
              % (i, tally[i], 100.0 * tally[i] / cells if cells else 0, SIGN[i]))

    # THE NUMBERS THE LENS QUESTION TURNS ON. Not the average completeness, but
    # how many cells carry enough to value WITHOUT assuming an item — a valuation
    # is built per origin, and an item present on another name in another year
    # does nothing for this cell.
    def has(c, *items):
        return all(i in per_cell[c] for i in items)

    full = [c for c in per_cell if has(c, "cash", "debt", "capex", "shares")]
    derivable = [c for c in per_cell
                 if has(c, "cash", "debt", "shares", "ppe", "dep")
                 and (c[0], c[1] - 1) in per_cell
                 and "ppe" in per_cell[(c[0], c[1] - 1)]]
    bridge = [c for c in per_cell if has(c, "cash", "debt", "shares")]
    print("\n  cells with a complete bridge AND a capex FIGURE"
          " (cash, debt, capex, shares): %d of %d" % (len(full), cells))
    print("  cells where capex is DERIVABLE by identity (ΔPPE + D&A) on top of a")
    print("  complete bridge: %d of %d%s"
          % (len(derivable), cells,
             ("  —  " + ", ".join("%s %d" % c for c in sorted(derivable)))
             if derivable else ""))
    print("  cells with the bridge but no route to capex — valuable only under a")
    print("  DECLARED substitution, which is an assumption and not a figure:"
          " %d of %d%s"
          % (len([c for c in bridge if c not in full and c not in derivable]), cells,
             ("  —  " + ", ".join("%s %d" % c for c in sorted(
                 c for c in bridge if c not in full and c not in derivable)))
             if bridge else ""))

    print("\n  artefacts that answered:")
    for tk in names:
        print("    %-6s %s" % (tk, ", ".join(files[tk]) or "none"))
    un = {tk: v for tk, v in loose.items() if v}
    print("\n  keys the guard matched that the map does not claim"
          " (a run's vocabulary nobody has read yet):")
    if not un:
        print("    none")
    for tk, v in sorted(un.items()):
        print("    %-6s %s" % (tk, ", ".join(sorted(v))[:150]))
    return found, files, loose


if __name__ == "__main__":
    report(*(sys.argv[1:] or []))
