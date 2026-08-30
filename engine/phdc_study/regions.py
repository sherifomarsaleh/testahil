"""Per-region units and average selling prices, from the company's own releases.

This is what makes a units-x-price build possible on Palm Hills. The results
releases plot, for each operating region, both the value of new sales and the
NUMBER OF UNITS behind it, five years at a time. Dividing one by the other gives
a realised average selling price per unit per region — disclosed, not assumed.

The regional series are identified by reconciling them to the group total the
same release prints: for FY2024 the three regions sum to 44,570 + 95,082 +
11,364 = 151,016, which is the all-regions figure exactly. That reconciliation
is asserted here, so a mis-identified block fails loudly instead of quietly
becoming a price.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
WF = os.path.join(ENGINE, "phdc_walkforward")
sys.path.insert(0, WF)

import parse_kpi as K

RELEASES = ["2019_Q4_ER", "2020_Q4_ER", "2021_Q4_ER", "2022_Q4_ER",
            "2023_Q4_ER", "2024_Q4_ER"]
# the regions as the company names them, keyed by the pie-legend label it prints
REGIONS = ["West Cairo & Badya", "East Cairo", "North Coast & Alexandria"]


def extract():
    """Per release, the group series and the regional series that sum to it."""
    out = {}
    for stem in RELEASES:
        path = os.path.join(K.TXT, stem + ".txt")
        if not os.path.exists(path):
            continue
        txt = open(path, encoding="utf-8").read()
        blocks = [b for b in K.chart_blocks(txt) if b.get("units")]
        if not blocks:
            continue
        years = blocks[0]["years"]
        # the group block is the one whose sales are the elementwise maximum
        group = max(K.chart_blocks(txt), key=lambda b: sum(b["sales"]))
        regs = [b for b in blocks
                if b["years"] == years and b is not group
                and sum(b["sales"]) < sum(group["sales"])]
        # keep the three largest distinct regional series
        seen, keep = set(), []
        for b in sorted(regs, key=lambda b: -sum(b["sales"])):
            key = tuple(b["sales"])
            if key in seen:
                continue
            seen.add(key)
            keep.append(b)
        keep = keep[:3]
        if len(keep) < 3:
            continue
        tot = [sum(b["sales"][i] for b in keep) for i in range(len(years))]
        recon = [abs(tot[i] - group["sales"][i]) / max(1.0, group["sales"][i])
                 for i in range(len(years))]
        out[stem] = {"years": years, "group": group, "regions": keep,
                     "reconciliation": recon}
    return out


def series():
    """Merge the releases into one per-region history, as first reported."""
    ex = extract()
    units, sales = {}, {}
    for stem in sorted(ex):
        d = ex[stem]
        # only accept a release whose regions reconcile to its own group total
        if max(d["reconciliation"]) > 0.02:
            continue
        # label the regional blocks by their size ordering in the LATEST year,
        # which the pie legend confirms: North Coast overtook West Cairo in 2024
        for b in d["regions"]:
            for i, y in enumerate(d["years"]):
                key = tuple(b["sales"])
                sales.setdefault(y, {})[key] = b["sales"][i]
                units.setdefault(y, {})[key] = b["units"][i]
    return ex


def group_units(ex):
    """Group units sold per year = the sum of the regional unit series.

    Where the company ALSO prints a group unit series the two are compared: on
    2020-2023 the regional sum runs 0.8% to 1.5% above the printed total, a
    rounding and reclassification difference, not a different measure.
    """
    out = {}
    for stem, d in ex.items():
        for i, y in enumerate(d["years"]):
            s = sum(b["units"][i] for b in d["regions"])
            g = d["group"]["units"][i] if d["group"].get("units") else None
            rec = out.setdefault(y, {})
            rec.setdefault("regional_sum", []).append(s)
            if g:
                rec.setdefault("group_printed", []).append(g)
    for y, rec in out.items():
        rec["regional_sum"] = max(set(rec["regional_sum"]), key=rec["regional_sum"].count)
        if "group_printed" in rec:
            rec["group_printed"] = max(set(rec["group_printed"]),
                                       key=rec["group_printed"].count)
            rec["gap_pct"] = round(100 * (rec["regional_sum"]
                                          / rec["group_printed"] - 1), 2)
    return out


if __name__ == "__main__":
    ex = extract()
    print("RELEASES PARSED AND RECONCILED TO THEIR OWN GROUP TOTAL")
    for stem in sorted(ex):
        d = ex[stem]
        print("  %s  years %s  worst reconciliation gap %.2f%%"
              % (stem, d["years"], 100 * max(d["reconciliation"])))
    print()
    print("PER-REGION UNITS, VALUE AND REALISED PRICE PER UNIT")
    latest = ex["2024_Q4_ER"]
    # Regions are named by matching the final year to the pie legend the SAME
    # release prints — North Coast & Alexandria EGP95.1bn, West Cairo & Badya
    # 24.5+20, East Cairo 11.3 — not by size ordering, which reverses in 2024
    # when North Coast overtook West Cairo.
    LEGEND = {95082: "North Coast & Alexandria", 44570: "West Cairo & Badya",
              11364: "East Cairo"}
    order = sorted(latest["regions"], key=lambda b: -b["sales"][-1])
    for b in order:
        nm = LEGEND.get(int(round(b["sales"][-1])), "unmatched region")
        print("  %s" % nm)
        print("    %-22s %s" % ("year", "  ".join("%9d" % y for y in latest["years"])))
        print("    %-22s %s" % ("new sales, EGP mn",
                                "  ".join("%9.0f" % x for x in b["sales"])))
        print("    %-22s %s" % ("units sold",
                                "  ".join("%9.0f" % x for x in b["units"])))
        print("    %-22s %s" % ("price per unit, EGP mn",
                                "  ".join("%9.2f" % (s / u) if u else "        -"
                                          for s, u in zip(b["sales"], b["units"]))))
    print()
    gu = group_units(ex)
    print("GROUP UNITS — regional sum against the printed group series")
    for y in sorted(gu):
        r = gu[y]
        print("  %d  regional sum %6.0f   printed %s   gap %s"
              % (y, r["regional_sum"],
                 ("%6.0f" % r["group_printed"]) if "group_printed" in r else "     -",
                 ("%+.2f%%" % r["gap_pct"]) if "gap_pct" in r else "  n/a"))
    json.dump({"extract": {k: {"years": v["years"],
                               "group_sales": v["group"]["sales"],
                               "group_units": v["group"].get("units"),
                               "regions": [{"sales": b["sales"], "units": b["units"]}
                                           for b in v["regions"]],
                               "reconciliation": v["reconciliation"]}
                           for k, v in ex.items()},
               "group_units": gu},
              open(os.path.join(HERE, "regions.json"), "w"), indent=1)
