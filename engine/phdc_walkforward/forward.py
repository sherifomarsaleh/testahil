"""The forward projection this training record hands to the update.

Years 3-5 are published as RANGES, not points, and the range is built from this
record's own driver-error distribution at that horizon — the empirical spread of
ln(projected/actual) over every resolved origin — rather than from a assumed
distribution. Years 1-2 carry the same treatment for consistency.

Nothing here is a valuation, a rating or a target. It is the fundamental lens's
own forward path with the uncertainty this exercise actually measured.
"""
import json, os, math
import bottom_up as B
import score as S

HERE = os.path.dirname(os.path.abspath(__file__))
ORIGIN = 2025


def latest(panel, field, upto):
    for y in range(upto, upto - 6, -1):
        v = panel.get(y, {}).get(field)
        if v is not None:
            return y, v
    return None, None


def error_quantiles(cells, field, h, qs=(0.10, 0.25, 0.50, 0.75, 0.90)):
    es = sorted(r["e"] for r in cells
                if r["field"] == field and r["h"] == h and "e" in r)
    if len(es) < 3:
        return None
    out = {}
    for q in qs:
        i = q * (len(es) - 1)
        lo, hi = int(math.floor(i)), int(math.ceil(i))
        out[q] = es[lo] + (es[hi] - es[lo]) * (i - lo)
    out["n"] = len(es)
    return out


def main():
    panel = B.load()
    cells = S.cells(panel, "bottom_up", "as_known")
    proj = B.project(panel, ORIGIN)
    anchors = {f: latest(panel, f, ORIGIN) for f in
               ("units_sold", "new_sales", "is.revenue", "is.npat_mi")}
    out = {"origin": ORIGIN, "anchors": {k: {"year": v[0], "value": v[1]}
                                         for k, v in anchors.items()},
           "note": "years 3-5 are ranges built from this record's own driver-error "
                   "distribution; a point would overstate what ten origins support",
           "years": {}}
    print("FORWARD PATH FROM ORIGIN FY%d — ranges from the measured error spread" % ORIGIN)
    print("(a range, never a point; no rating, target or recommendation)\n")
    print("%-16s %2s %12s   %-34s %s" %
          ("driver", "h", "central", "10th-90th of the record", "n"))
    for f in ("units_sold", "new_sales", "is.revenue", "is.gross_profit", "is.npat_mi"):
        for h in B.HORIZONS:
            p = proj[h].get(f)
            q = error_quantiles(cells, f, h)
            if p is None or q is None:
                continue
            lo = p / math.exp(q[0.90])
            hi = p / math.exp(q[0.10])
            mid = p / math.exp(q[0.50])
            print("%-16s %2d %12.0f   %10.0f  to %10.0f      %d" %
                  (f, h, mid, lo, hi, q["n"]))
            out["years"].setdefault(f, {})[h] = {
                "year": ORIGIN + h, "raw_projection": round(p, 1),
                "central_after_record_median": round(mid, 1),
                "p10": round(lo, 1), "p90": round(hi, 1),
                "n_resolved_errors": q["n"]}
    json.dump(out, open(os.path.join(HERE, "forward_ranges.json"), "w"), indent=1)
    print("\nanchors used (latest disclosed at or before the origin):")
    for k, (y, v) in anchors.items():
        print("   %-14s FY%s = %s" % (k, y, None if v is None else round(v, 1)))


if __name__ == "__main__":
    main()
