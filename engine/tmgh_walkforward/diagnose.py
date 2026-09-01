"""TMGH walk-forward — diagnosis: what the errors are made of.

Three things §4 of the standing prompt asks for and this produces:
  * the projected-versus-actual income statement, side by side, for EVERY origin;
  * the revenue and net-profit errors decomposed into the drivers that made them;
  * every one-off in the history identified, and what the record looks like with
    it classified.
"""
import json, math, os, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bottom_up as BU
import score as SC

# One-offs the company itself attributed, with the document that says so.
ONE_OFFS = [
    {"year": 2023, "item": "non-core land transaction inside new sales",
     "size": "EGP 47.9bn of the EGP 142.8bn total (core EGP 94.9bn)",
     "source": "FY2023 earnings release", "affects": ["new_sales", "backlog"]},
    {"year": 2024, "item": "seven-hotel acquisition (39% with management rights)",
     "size": "hospitality revenue 3,540.9 -> 11,496.5 EGP mn",
     "source": "FY2024 consolidated financial statements, business combinations note",
     "affects": ["recurring_revenue", "recurring_cost", "ppe"]},
    {"year": 2024, "item": "investment-property revaluation surplus",
     "size": "EGP 4,924.1mn", "source": "FY2024 statements",
     "affects": ["net_profit"]},
    {"year": 2024, "item": "gain on the hotels acquisition",
     "size": "EGP 718.8mn", "source": "FY2024 statements", "affects": ["net_profit"]},
    {"year": 2024, "item": "SouthMed launch (July 2024)",
     "size": "contracted sales 142.8 -> 504.0 EGP bn",
     "source": "FY2024 earnings release", "affects": ["new_sales", "backlog"]},
    {"year": 2025, "item": "investment-property revaluation surplus",
     "size": "EGP 3,952.5mn", "source": "FY2025 statements", "affects": ["net_profit"]},
    {"year": 2025, "item": "first Saudi revenue (Banan) on percentage-of-completion",
     "size": "52.5% of real-estate segment revenue by 1H2026",
     "source": "FY2025 statements note 2.3; 1H2026 earnings release",
     "affects": ["dev_revenue"]},
]

IS_LINES = [("dev_revenue", "Development revenue"),
            ("recurring_revenue", "Recurring revenue (hospitality + other)"),
            ("total_revenue", "Total revenue"),
            ("dev_cost", "Development cost"),
            ("recurring_cost", "Recurring cost"),
            ("gross_profit", "Gross profit"),
            ("sga", "SG&A"),
            ("da", "Depreciation and amortisation"),
            ("finance_cost", "Finance cost"),
            ("net_profit", "Net profit")]


def side_by_side(bj, A, path):
    """The projected-versus-actual income statement, every origin, every horizon."""
    out = ["# TMGH walk-forward — projected versus actual, every origin",
           "",
           "Internal training record. EGP mn. `as-known` macro setting: the honest",
           "information set at each origin. A dash is a line the panel does not source",
           "for that year — left empty, never filled.", ""]
    for o in range(bj["first_origin"], bj["last_origin"] + 1):
        run = bj["runs"].get("%d|asknown" % o)
        if not run:
            continue
        yrs = [o + h for h in BU.HORIZONS if o + h <= bj["last_actual"]]
        if not yrs:
            out += ["## Origin FY%d — struck but unresolved (it produces the forward "
                    "projection and contributes no error)" % o, ""]
            continue
        out += ["## Origin FY%d" % o, "",
                "| line | " + " | ".join("FY%d P | FY%d A | err" % (y, y) for y in yrs) + " |",
                "|---|" + "---|" * (3 * len(yrs))]
        for f, label in IS_LINES:
            cells = []
            for y in yrs:
                p = run["projection"].get(str(y - o), {}).get(f)
                a = A.get(y, {}).get(f)
                if p is None or a is None:
                    cells += ["–", "–", "–"]
                    continue
                pp, aa = (abs(p), abs(a)) if f in SC.MAGNITUDE else (p, a)
                e = ("%+.2f" % math.log(pp / aa)) if pp > 0 and aa > 0 else "n/m"
                cells += ["%,.0f".replace(",", "") % p, "%.0f" % a, e]
            out.append("| %s | %s |" % (label, " | ".join(cells)))
        out.append("")
    open(path, "w").write("\n".join(out))
    return len(out)


def decompose(bj, A):
    """Which drivers made the revenue and net-profit errors.

    Each driver is set to its ACTUAL value one at a time, the aggregate rebuilt,
    and the reduction in the aggregate's log error attributed to that driver.
    The parts do not add exactly — the aggregate is a product of ratios, not a
    sum — and the residual is reported rather than spread across the drivers.
    """
    res = defaultdict(list)
    for o in range(bj["first_origin"], bj["last_origin"] + 1):
        run = bj["runs"].get("%d|asknown" % o)
        if not run:
            continue
        for h in BU.HORIZONS:
            y = o + h
            if y > bj["last_actual"]:
                continue
            f = run["projection"].get(str(h), {})
            a = A.get(y, {})
            for agg, parts in (("total_revenue", ["dev_revenue", "recurring_revenue"]),
                               ("gross_profit", ["dev_revenue", "dev_cost",
                                                 "recurring_revenue", "recurring_cost"]),
                               ("net_profit", ["gross_profit", "sga", "da", "finance_cost"])):
                if f.get(agg) is None or a.get(agg) in (None, 0):
                    continue
                if any(f.get(p) is None or a.get(p) is None for p in parts):
                    continue
                base = f[agg] - sum(f[p] for p in parts) if agg != "total_revenue" else 0.0
                full_err = abs(f[agg] - a[agg])
                for p in parts:
                    swapped = base + sum(a[q] if q == p else f[q] for q in parts)
                    res["%s|%s" % (agg, p)].append(
                        {"origin": o, "horizon": h,
                         "error_removed": full_err - abs(swapped - a[agg]),
                         "full_error": full_err})
    out = {}
    for k, rows in res.items():
        tot = sum(r["full_error"] for r in rows)
        out[k] = {"n": len(rows),
                  "share_of_absolute_error": (sum(r["error_removed"] for r in rows) / tot)
                  if tot else None}
    return out


def main():
    bj = json.load(open(os.path.join(HERE, "bottom_up.json")))
    A = {int(k): v for k, v in bj["actuals"].items()}
    n = side_by_side(bj, A, os.path.join(HERE, "tmgh_IS_projected_vs_actual_all_origins.md"))
    dec = decompose(bj, A)
    json.dump({"decomposition": dec, "one_offs": ONE_OFFS},
              open(os.path.join(HERE, "diagnostics.json"), "w"), indent=1)

    print("side-by-side income statements written (%d lines)\n" % n)
    print("=== error decomposition: share of the aggregate's absolute error each "
          "driver accounts for ===")
    for agg in ("total_revenue", "gross_profit", "net_profit"):
        rows = [(k.split("|")[1], v) for k, v in dec.items() if k.startswith(agg + "|")]
        if not rows:
            continue
        print("\n%s" % agg)
        for name, v in sorted(rows, key=lambda r: -(r[1]["share_of_absolute_error"] or 0)):
            print("   %-24s %6.1f%%  (n=%d)"
                  % (name, 100 * (v["share_of_absolute_error"] or 0), v["n"]))
    print("\n=== one-offs identified in the history ===")
    for x in ONE_OFFS:
        print("  FY%d  %-56s %s" % (x["year"], x["item"], x["size"]))


if __name__ == "__main__":
    main()
