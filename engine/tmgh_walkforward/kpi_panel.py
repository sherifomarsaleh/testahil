"""Resolve the operating drivers into one panel, and show the working.

A headline figure is repeated several times inside its own release — in the
strap line, in the highlights box and in the segment discussion — while a
misreading is not. The resolution rule is therefore a mode vote across the
year's OWN full-year documents, with the sentence that produced the winning
value carried into the panel so the figure can be read against its context.

Where the vote is a tie or a single unrepeated mention, the cell is marked
`weak` and listed. Nothing is filled in from a neighbouring year.
"""
import json, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))

FULLYEAR = re.compile(r"full[_ ]?year|FY\d|financial[_ ]year|4Q|12M", re.I)
FIELDS = ["new_sales_value", "units_sold", "units_delivered", "backlog", "landbank_msqm"]


def year_of(r):
    p = r.get("period")
    if not p:
        return None
    if p[1] in (12, None) and FULLYEAR.search(r["doc"]):
        return p[0]
    return None


def main():
    rows = json.load(open(os.path.join(HERE, "kpi_candidates.json")))
    fy = [r for r in rows if year_of(r) is not None]
    for r in fy:
        r["year"] = year_of(r)
    panel, weak = {}, []
    for y in sorted({r["year"] for r in fy}):
        cell = {}
        for f in FIELDS:
            cands = [r for r in fy if r["year"] == y and r["field"] == f]
            if not cands:
                continue
            cnt = collections.Counter(r["value"] for r in cands)
            top = cnt.most_common()
            # a tie on count is broken by the EARLIEST page: a release states
            # its headline first and qualifies it later
            best = sorted([v for v, n in top if n == top[0][1]],
                          key=lambda v: min(c["page"] or 99 for c in cands
                                            if c["value"] == v))[0]
            ev = sorted([c for c in cands if c["value"] == best],
                        key=lambda c: c["page"] or 99)[0]
            cell[f] = {"value": best, "votes": cnt[best], "candidates": len(cands),
                       "doc": ev["doc"], "page": ev["page"], "route": ev["route"],
                       "sentence": ev["sentence"], "tier": "A",
                       "distinct_values": sorted(cnt)}
            if cnt[best] < 2:
                weak.append({"year": y, "field": f, "value": best,
                             "why": "single unrepeated mention",
                             "sentence": ev["sentence"]})
        if cell:
            panel[str(y)] = cell
    json.dump({"panel": panel, "weak_cells": weak},
              open(os.path.join(HERE, "panel_kpi.json"), "w"), indent=1)
    print("%-6s %14s %10s %10s %12s %8s" % ("year", "new sales", "units sold",
                                            "delivered", "backlog", "landbank"))
    for y in sorted(panel, key=int):
        c = panel[y]
        def g(f, fmt="%14.0f"):
            return (fmt % c[f]["value"]) if f in c else (fmt.replace("f", "s") % "-")
        print("%-6s %14s %10s %10s %12s %8s"
              % (y, g("new_sales_value", "%.0f"), g("units_sold", "%.0f"),
                 g("units_delivered", "%.0f"), g("backlog", "%.0f"),
                 g("landbank_msqm", "%.1f")))
    print("\n%d weak cells (single unrepeated mention)" % len(weak))


if __name__ == "__main__":
    main()
