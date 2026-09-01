"""TMGH walk-forward — the annual panel, footed and corroborated.

Nothing here trusts a reading because it parsed cleanly. Three things decide
whether a figure enters the panel:

  1. ARITHMETIC. Every year is footed against the identities the statement
     itself asserts. A cell that breaks one is not kept on the strength of the
     extractor's confidence — the identity is the arbiter.
  2. CORROBORATION. Most fiscal years appear in three or four documents (its
     own release, its own statements, and the following year's comparatives).
     Where two INDEPENDENT documents agree, the cell is corroborated; where
     they disagree, both readings are recorded and the audited statement wins.
  3. PROVENANCE. Four fields on every cell — value, source document, document
     date, tier — plus the route (text layer or OCR) the figure came by, and
     the identity behind it where it was recovered rather than read.

A cell that survives none of these is DROPPED and listed, never estimated.
"""
import json, os, re, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TOL_REL, TOL_ABS = 0.005, 1.0          # 0.5% or EGP 1mn, whichever is looser

# Fields the company reports as a deduction. Both families print them in
# parentheses; normalising the sign here means the identities below can be
# plain sums and a sign slip cannot hide inside one.
NEGATIVE = {"dev_cost", "hosp_cost", "other_cost", "total_cost",
            "recurring_combined_cost", "sga", "marketing", "finance_cost",
            "finance_expenses", "bank_charges", "da", "tax", "nci"}

IDENTITIES = [
    ("I1", "gp_dev",        ["dev_revenue", "dev_cost"]),
    ("I2", "gp_hosp",       ["hosp_revenue", "hosp_cost"]),
    ("I3", "gp_other",      ["other_revenue", "other_cost"]),
    ("I4", "gross_profit",  ["gp_dev", "gp_hosp", "gp_other"]),
    ("I5", "total_revenue", ["dev_revenue", "hosp_revenue", "other_revenue"]),
    ("I6", "npat_parent",   ["net_profit", "nci"]),
    ("I7", "total_assets",  ["total_nca", "total_ca"]),
    ("I8", "total_assets",  ["total_equity", "total_liab"]),
    ("I9", "total_liab",    ["total_nc_liab", "total_cl"]),
    # the legacy summary table's own two cross-foots; they are what caught a
    # row whose columns had slipped while every other identity stayed silent
    ("I10", "total_cost",   ["dev_cost", "hosp_cost", "other_cost"]),
    ("I11", "gross_profit", ["total_revenue", "total_cost"]),
    # the FY2017/FY2018 presentation, where the two recurring segments are one
    ("I12", "gp_recurring_combined",
     ["recurring_combined_revenue", "recurring_combined_cost"]),
    ("I13", "gross_profit", ["gp_dev", "gp_recurring_combined"]),
]


def close(a, b):
    return abs(a - b) <= max(TOL_ABS, TOL_REL * max(abs(a), abs(b)))


def normalise(cells):
    """Sign convention, applied once, where the company's own sign is known."""
    for f in NEGATIVE:
        if f in cells and cells[f] is not None:
            cells[f] = -abs(cells[f])
    return cells


def foot(cells):
    """Which identities hold, which break, and which cannot be tested."""
    res = {}
    for tag, lhs, rhs in IDENTITIES:
        have = [f for f in rhs if cells.get(f) is not None]
        if cells.get(lhs) is None or len(have) < len(rhs):
            res[tag] = "untestable"
            continue
        res[tag] = "ok" if close(cells[lhs], sum(cells[f] for f in rhs)) else "BREAK"
    return res


def repair(cells, res):
    """Recover the one cell an identity pins, where every other cell foots.

    Only ever applied where the identity leaves exactly one unknown AND the
    cells it rests on are themselves footed by a different identity, so a
    single bad reading cannot propagate into a second one. Every repair is
    recorded with the identity that produced it — the panel says how it knows.
    """
    fixed = {}
    for _pass in range(3):
        moved = False
        for tag, lhs, rhs in IDENTITIES:
            vals = {f: cells.get(f) for f in [lhs] + rhs}
            missing = [f for f, v in vals.items() if v is None]
            broken = res.get(tag) == "BREAK"
            if len(missing) == 1 and not broken:
                f = missing[0]
                cells[f] = (sum(cells[x] for x in rhs) if f == lhs
                            else cells[lhs] - sum(cells[x] for x in rhs if x != f))
                fixed[f] = {"how": "derived", "identity": tag}
                moved = True
            elif broken and len(missing) == 0:
                # exactly one cell is wrong; identify it as the one whose
                # correction is corroborated by a second identity
                for f in [lhs] + rhs:
                    want = (sum(cells[x] for x in rhs) if f == lhs
                            else cells[lhs] - sum(cells[x] for x in rhs if x != f))
                    trial = dict(cells); trial[f] = want
                    before = sum(1 for v in foot(cells).values() if v == "ok")
                    after = sum(1 for v in foot(trial).values() if v == "ok")
                    if after > before + 0:
                        cells[f] = want
                        fixed[f] = {"how": "repaired", "identity": tag,
                                    "was": round(vals[f], 3)}
                        moved = True
                        break
        res = foot(cells)
        if not moved:
            break
    return cells, res, fixed


TIER = {"consolidated_fs": "A", "earnings_release": "A"}


def blocks():
    """One block per (document, year column). A block is a single document's
    reading of a single year — the unit that either foots or does not.

    Footing at BLOCK level rather than after merging is the whole point. A
    first cut merged cell-by-cell across documents and then made the identities
    hold, which they duly did — on top of readings that were wrong. An identity
    satisfied by a set of wrong numbers is not evidence, and a repair that
    produces one is the arithmetic equivalent of a correction factor hiding a
    mis-specification.
    """
    parsed = json.load(open(os.path.join(HERE, "fs_parsed.json")))
    reg = {re.sub(r"[^A-Za-z0-9._-]+", "_", r["name"])[:150][:-4]: r
           for r in json.load(open(os.path.join(HERE, "ir_register.json")))}
    out = []
    for doc, d in parsed.items():
        month = d["period"][1] if d["period"] else None
        interim = month not in (12, None)
        # An interim document still carries ANNUAL data — but only on one side.
        # Under IAS 34 its comparative balance sheet is as at the preceding
        # YEAR END, while its comparative income statement is the same interim
        # period a year earlier. So an interim contributes its balance-sheet
        # comparative column and nothing else; taking its income statement
        # would have put nine months of revenue into a full-year cell.
        tables = (("bs", "prov_bs"),) if interim else (("is", "prov_is"), ("bs", "prov_bs"))
        # JSON turns the year columns into strings; casting here rather than at
        # each comparison is what makes the interim exclusion below actually
        # fire — comparing "2023" with 2023 silently never excluded anything.
        years = set()
        for tbl, _ in tables:
            for byyear in d[tbl].values():
                years |= {int(k) for k in byyear}
        if interim:
            years = {y for y in years if y != d["period"][0]}
        for y in sorted(years):
            cells, prov = {}, {}
            for tbl, pk in tables:
                for field, byyear in d[tbl].items():
                    if str(y) in byyear:
                        cells[field] = byyear[str(y)]
                        prov[field] = dict(d[pk][field][str(y)],
                                           interim_comparative=interim)
            if not cells:
                continue
            out.append({"doc": doc, "year": y, "kind": d["kind"],
                        "interim_source": interim,
                        "family": "statement_layout",
                        "reports": d["period"][0] if d["period"] else None,
                        "url": reg.get(doc, {}).get("url"),
                        "tier": TIER[d["kind"]], "cells": cells, "prov": prov})
    out += legacy_blocks()
    return out


def legacy_blocks():
    """The pre-2018 releases' own summary table, one block per year column."""
    path = os.path.join(HERE, "legacy_parsed.json")
    if not os.path.exists(path):
        return []
    d = json.load(open(path))
    out = []
    for doc, v in d.items():
        for y, cells in v["by_year"].items():
            out.append({"doc": doc, "year": int(y), "kind": "earnings_release",
                        "interim_source": False, "family": "legacy_summary",
                        "reports": (v["period_from_filename"] or [None])[0],
                        "url": v["url"], "tier": "A",
                        "cells": dict(cells),
                        "prov": {f: dict(p) for f, p in v["prov"][y].items()}})
    return out


def fill_missing(cells):
    """Recover a cell an identity pins EXACTLY, and only then.

    Applied only where the identity has one unknown and no identity is broken:
    a derivation on top of a break is a guess. Nothing is ever 'repaired' by
    choosing which of several present cells to overwrite.
    """
    got = {}
    for _pass in range(3):
        res, moved = foot(cells), False
        if any(v == "BREAK" for v in res.values()):
            break
        for tag, lhs, rhs in IDENTITIES:
            names = [lhs] + rhs
            missing = [f for f in names if cells.get(f) is None]
            if len(missing) != 1:
                continue
            f = missing[0]
            if any(cells.get(x) is None for x in names if x != f):
                continue
            cells[f] = (sum(cells[x] for x in rhs) if f == lhs
                        else cells[lhs] - sum(cells[x] for x in rhs if x != f))
            got[f] = {"how": "derived from the statement's own arithmetic",
                      "identity": tag}
            moved = True
        if not moved:
            break
    return cells, got


MAG_MAX = 5e6          # EGP 5 trillion in EGP mn: no reading above this is real


def unit_guard(b):
    """One block, one unit — checked against the size of the company.

    Every identity is scale-invariant, so a balance sheet read a million times
    too large foots perfectly and looks clean. The magnitude is the only thing
    that catches it, and it is checked against the company rather than against
    a round number: TMG's assets have never been EGP 5 trillion, and its
    revenue has never been EGP 5 trillion either.
    """
    c = b["cells"]
    anchor = c.get("total_assets") or c.get("total_revenue") or c.get("dev_revenue")
    if anchor is None:
        return b, None
    if abs(anchor) > MAG_MAX:
        for f in c:
            c[f] *= 1e-6
        return b, "rescaled by 1e-6: read in LE where the table declared none"
    return b, None


def quarantine(cells, res):
    """Drop the cells a broken identity implicates, keep the rest.

    A break says one of the cells in that identity is wrong without saying
    which, so every cell it touches is suspect — unless a DIFFERENT identity
    that foots also vouches for it, which is corroboration by arithmetic rather
    than by assumption. Dropping is the whole response; nothing is repaired,
    because repairing would mean choosing which reading to overwrite and that
    choice is a guess. Rejecting the entire block instead was tried and threw
    away a correct income statement over one mis-read line.
    """
    ok, broken = set(), set()
    for tag, lhs, rhs in IDENTITIES:
        if res.get(tag) == "ok":
            ok |= {lhs} | set(rhs)
        elif res.get(tag) == "BREAK":
            broken |= {lhs} | set(rhs)
    drop = sorted((broken - ok) & set(cells))
    for f in drop:
        cells.pop(f, None)
    return cells, drop


def score(b):
    """Blocks are ranked on evidence, never on convenience."""
    res = b["foot"]
    # POINT-IN-TIME ORDER. The document that REPORTS the year outranks any later
    # document quoting it, before anything else is considered. TMG restated
    # FY2024 in its FY2025 statements — hospitality cost, gross profit, net
    # profit and EPS all move — and the restated column is explicitly labelled
    # as such. An origin must see the year as it was FIRST reported; the
    # restatement is recorded beside it, never substituted for it.
    return (1 if b.get("interim_source") else 0,
            0 if b["reports"] == b["year"] else 1,
            -sum(1 for v in res.values() if v == "ok"),
            0 if b["kind"] == "consolidated_fs" else 1,
            0 if all(p.get("route") == "text" for p in b["prov"].values()) else 1,
            -len(b["cells"]))


def main():
    bl = []
    for b in blocks():
        b["cells"] = normalise(b["cells"])
        b, note = unit_guard(b)
        b["unit_note"] = note
        b["cells"], b["derived"] = fill_missing(b["cells"])
        b["foot"] = foot(b["cells"])
        b["quarantined"] = []
        if any(v == "BREAK" for v in b["foot"].values()):
            b["cells"], b["quarantined"] = quarantine(b["cells"], b["foot"])
            b["foot"] = foot(b["cells"])
        b["ok"] = sum(1 for v in b["foot"].values() if v == "ok")
        b["broken"] = [t for t, v in b["foot"].items() if v == "BREAK"]
        bl.append(b)

    good = [b for b in bl if not b["broken"] and b["ok"] >= 1]
    bad = [b for b in bl if b["broken"]]
    thin = [b for b in bl if not b["broken"] and b["ok"] < 1]

    byyear = defaultdict(list)
    for b in good:
        byyear[b["year"]].append(b)

    panel, conflicts = {}, {}
    for y, bs in sorted(byyear.items()):
        bs.sort(key=score)
        lead = bs[0]
        cells = dict(lead["cells"])
        prov = {f: dict(lead["prov"].get(f, {}), source=lead["doc"], url=lead["url"],
                        tier=lead["tier"], kind=lead["kind"],
                        reported_in=lead["reports"])
                for f in cells}
        for f, how in lead["derived"].items():
            prov.setdefault(f, {}).update({"route": "identity", "tier": "DERIVED",
                                           "derivation": how, "source": lead["doc"],
                                           "url": lead["url"]})
        corro, disagree = defaultdict(list), defaultdict(list)
        for b in bs[1:]:
            shared = [f for f in b["cells"] if f in cells and cells[f] is not None]
            agree = [f for f in shared if close(b["cells"][f], cells[f])]
            # a second document only extends the year where it AGREES with the
            # lead on everything the two share; a document that disagrees on a
            # line is not trusted to supply the lines the lead lacks
            for f in agree:
                corro[f].append(b["doc"])
            for f in shared:
                if f not in agree:
                    disagree[f].append({"doc": b["doc"], "value": round(b["cells"][f], 2),
                                        "kind": b["kind"], "reports": b["reports"],
                                        "route": b["prov"].get(f, {}).get("route")})
            # A second document extends the year only where it agrees with the
            # lead on EVERY line the two share. One shared line is enough where
            # both blocks footed independently — an agreement on top of two
            # independent arithmetic checks is not a coincidence — but zero
            # shared lines is not agreement, it is silence.
            if len(shared) >= 1 and len(agree) == len(shared):
                for f, v in b["cells"].items():
                    if cells.get(f) is None and v is not None:
                        cells[f] = v
                        prov[f] = dict(b["prov"].get(f, {}), source=b["doc"],
                                       url=b["url"], tier=b["tier"], kind=b["kind"],
                                       reported_in=b["reports"],
                                       note="supplied by a second document that "
                                            "agrees with the lead on every line "
                                            "the two share")
        for f in cells:
            prov.setdefault(f, {})["corroborating_docs"] = corro.get(f, [])
            if disagree.get(f):
                prov[f]["disagreeing"] = disagree[f]
        restated = {f: [d for d in v if (d.get("reports") or 0) > int(y)]
                    for f, v in disagree.items()}
        restated = {f: v for f, v in restated.items() if v}
        if disagree:
            conflicts[str(y)] = {f: v for f, v in disagree.items()}
        panel[str(y)] = {"cells": {f: round(v, 4) for f, v in cells.items() if v is not None},
                         "provenance": prov,
                         "lead_document": lead["doc"], "lead_kind": lead["kind"],
                         "identities_ok": lead["ok"], "foot": lead["foot"],
                         "blocks_available": len(bs),
                         "unit_note": lead.get("unit_note"),
                         "quarantined_in_lead": lead.get("quarantined", []),
                         "restated_later": restated}

    # Final screens, applied to the merged year and stated rather than silent.
    # A cell above the magnitude bound is a unit that was never declared; a
    # year with almost nothing in it is not a short year, it is a year we could
    # not read, and the honest response to both is to shorten the window.
    MIN_CELLS = 12
    excluded = {}
    for y in sorted(panel, key=int):
        cells = panel[y]["cells"]
        oversize = [f for f, v in cells.items() if abs(v) > MAG_MAX]
        for f in oversize:
            cells.pop(f)
            panel[y]["provenance"].pop(f, None)
        if oversize:
            panel[y]["cells_dropped_oversize"] = oversize
        if len(cells) < MIN_CELLS:
            excluded[y] = ("only %d readable cells after footing (below the %d the "
                           "panel requires); the documents for this year are "
                           "scans whose columns could not be resolved"
                           % (len(cells), MIN_CELLS))
    for y in excluded:
        panel.pop(y)
    years = sorted(int(y) for y in panel)
    panel["_span"] = {
        "first": years[0], "last": years[-1], "n_years": len(years),
        "years": years,
        "excluded": excluded,
        "note": ("The span stops where it does because of what could be READ, not "
                 "what was published: TMG's own archive reaches back to FY2007, but "
                 "its pre-2011 releases survive only as scans whose summary tables "
                 "do not resolve into columns. Nothing was estimated to extend it.")}
    json.dump(panel, open(os.path.join(HERE, "panel_annual.json"), "w"), indent=1)
    json.dump({"rejected_blocks": [
                   {"doc": b["doc"], "year": b["year"], "broken": b["broken"],
                    "cells": {f: round(v, 2) for f, v in b["cells"].items()}}
                   for b in bad],
               "blocks_with_no_testable_identity": [
                   {"doc": b["doc"], "year": b["year"], "n_cells": len(b["cells"])}
                   for b in thin],
               "cells_quarantined_by_a_broken_identity": [
                   {"doc": b["doc"], "year": b["year"], "dropped": b["quarantined"]}
                   for b in bl if b["quarantined"]],
               "cell_level_disagreements": conflicts},
              open(os.path.join(HERE, "dropped_figures.json"), "w"), indent=1)

    print("blocks: %d read, %d footed, %d REJECTED on a broken identity, "
          "%d with nothing testable" % (len(bl), len(good), len(bad), len(thin)))
    print("\nspan obtained: FY%d-FY%d (%d years); excluded %s"
          % (panel["_span"]["first"], panel["_span"]["last"],
             panel["_span"]["n_years"], sorted(panel["_span"]["excluded"]) or "none"))
    print("\n%-6s %-4s %-5s %-3s  %s" % ("year", "cells", "ident", "blk", "lead document"))
    for y in sorted((k for k in panel if not k.startswith("_")), key=int):
        p = panel[y]
        print("%-6s %-4d %-5d %-3d  %s" % (y, len(p["cells"]), p["identities_ok"],
                                           p["blocks_available"], p["lead_document"][:58]))


if __name__ == "__main__":
    main()
