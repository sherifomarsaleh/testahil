"""Which KNOWABLE escalation rule gets closest? The measurement that decides
where a forecast's effort should go.

engine/valuation_calibration/spread_drift.py established that the spread between
revenue and cost per unit drifts by under one per cent a year across twenty-six
name-years, while the RATE at which both escalate runs anywhere from 16% to 46%
a year. So the rate is worth two orders of magnitude more than the spread, and
this house's driver work is mostly spent on the spread.

THE RATE IS THEREFORE THE THING TO GET RIGHT, AND NOBODY HAD ASKED WHICH RULE
GETS CLOSEST. Four candidates, all knowable at the origin with nothing fitted:

  freeze      no escalation at all -- what AMOC's model actually does
  cpi         the origin's last published consumer inflation, compounded
  ppp         relative purchasing-power parity on the CPI differential
  trail3      the company's OWN trailing three-year escalation of the line

None is a forecast of anything. Each is a rule a study could have followed at the
origin, scored against what the company then reported, on that company's own
committed actuals.

WHAT THIS IS NOT. It is not a search for the best rule to adopt: selecting a rule
because it scores best on this panel is the CRPS-selection mistake the promotion
rule forbids, and it is said here so that a later reader cannot mistake the table
for a recommendation. What a measurement like this can honestly do is rule rules
OUT -- a rule beaten by 'no change' on every name has not earned its place -- and
say how much of the error the rate accounts for.

Read live: python3 engine/valuation_calibration/escalation_rules.py
"""
import os, sys, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.dirname(HERE)
HORIZONS = (1, 2, 3)
TRAIL = 3

# (name, adapter, revenue field, volume field or None, cpi field)
RUNS = [
    ("PHDC", "panel", "is.revenue", "units_delivered", "macro.cpi_pct"),
    ("TMGH", "bottom_up_json", "dev_revenue", None, None),
    ("AMOC", "module", "net_sales", "volume_t", None),
    ("EGCH", "module", "revenue", "urea_t", None),
]
US_LONGRUN = 0.025   # long-run foreign inflation for the PPP leg, stated not fitted


def _load(name, adapter, rev, vol, cpif):
    """Returns {year: (unit_revenue, cpi_rate)}. A run with no volume series is
    read on TOTALS and labelled, never silently mixed with the per-unit ones."""
    d = "%s_walkforward" % name.lower()
    path = os.path.join(ENG, d)
    if adapter == "panel":
        sys.path.insert(0, path)
        for m in ("bottom_up", "panel", "score"):
            sys.modules.pop(m, None)
        try:
            import bottom_up as B
            p = B.load()
            return {y: (v[rev] / v[vol], (v.get(cpif) or 0) / 100.0)
                    for y, v in p.items()
                    if v.get(rev) and v.get(vol)}, bool(vol)
        finally:
            sys.path.remove(path)
    if adapter == "bottom_up_json":
        bj = json.load(open(os.path.join(path, "bottom_up.json")))
        A = {int(k): v for k, v in bj["actuals"].items()}
        return {y: (abs(v[rev]), None) for y, v in A.items() if v.get(rev)}, False
    sys.path.insert(0, path)
    for m in ("bottom_up", "panel", "score", "macro"):
        sys.modules.pop(m, None)
    try:
        import bottom_up as B
        import panel as P
        act = getattr(B, "actual", None) or getattr(P, "actual")
        out = {}
        for fy in sorted(P.IS):
            a = act(fy)
            r, v = a.get(rev), a.get(vol)
            if r and v:
                y = int("".join(c for c in fy if c.isdigit())[-4:])
                cpi = None
                try:
                    cpi = B.cpi_path(fy, 1) - 1
                except Exception:
                    pass
                out[y] = (abs(r) / v, cpi)
        return out, bool(vol)
    finally:
        sys.path.remove(path)


def score(series):
    """Log error of each rule at each (origin, horizon), on identical cells."""
    ys = sorted(series)
    cells = []
    for o in ys:
        if o - TRAIL not in series:
            continue
        base, cpi = series[o]
        prev = series[o - TRAIL][0]
        if prev <= 0:
            continue
        trail = (base / prev) ** (1.0 / TRAIL) - 1.0
        ppp = ((1 + cpi) / (1 + US_LONGRUN) - 1.0) if cpi is not None else None
        for h in HORIZONS:
            if o + h not in series:
                continue
            real = series[o + h][0] / base
            rules = {"freeze": 1.0, "trail3": (1 + trail) ** h}
            if cpi is not None:
                rules["cpi"] = (1 + cpi) ** h
                rules["ppp"] = (1 + ppp) ** h
            cells.append({"origin": o, "h": h, "realised": real, "rules": rules})
    return cells


def main():
    allcells, notes = [], []
    print("Which knowable escalation rule gets closest?")
    print("Log error of the projected escalation against the realised one.\n")
    for name, adapter, rev, vol, cpif in RUNS:
        try:
            series, per_unit = _load(name, adapter, rev, vol, cpif)
        except Exception as e:
            notes.append((name, str(e)[:70]))
            continue
        cells = score(series)
        if not cells:
            notes.append((name, "no cell with %d prior years and a later actual" % TRAIL))
            continue
        for c in cells:
            c["name"] = name
            c["per_unit"] = per_unit
        allcells.extend(cells)
        rules = sorted({r for c in cells for r in c["rules"]})
        print("%-6s %s  n=%d" % (name, "per unit" if per_unit else "TOTALS, not per unit",
                                 len(cells)))
        print("       %-8s %8s %8s" % ("rule", "bias", "mae"))
        for r in rules:
            v = [math.log(c["rules"][r] / c["realised"]) for c in cells
                 if r in c["rules"] and c["realised"] > 0]
            if v:
                print("       %-8s %+8.3f %8.3f"
                      % (r, sum(v) / len(v), sum(abs(x) for x in v) / len(v)))
        print()
    for name, why in notes:
        print("%-6s NOT MEASURED -- %s" % (name, why))
    if not allcells:
        raise SystemExit("FAIL: no cell measured -- that is not a clean result")

    print("POOLED across every name that could be measured")
    print("%-8s %5s %8s %8s   %s" % ("rule", "n", "bias", "mae", "beats freeze?"))
    fr = {(c["name"], c["origin"], c["h"]): math.log(1.0 / c["realised"])
          for c in allcells if c["realised"] > 0}
    for r in sorted({x for c in allcells for x in c["rules"]}):
        pairs = [(math.log(c["rules"][r] / c["realised"]),
                  fr[(c["name"], c["origin"], c["h"])])
                 for c in allcells if r in c["rules"] and c["realised"] > 0]
        if not pairs:
            continue
        m = sum(abs(a) for a, _ in pairs) / len(pairs)
        b = sum(abs(x) for _, x in pairs) / len(pairs)
        print("%-8s %5d %+8.3f %8.3f   %s"
              % (r, len(pairs), sum(a for a, _ in pairs) / len(pairs), m,
                 "yes, %.0f%% better" % (100 * (1 - m / b)) if m < b
                 else "NO, %.0f%% worse" % (100 * (m / b - 1))))
    print("\nREAD THE COMPOSITION BEFORE THE POOLED ROW. TMGH contributes 30 of the 43 cells")
    print("and is measured on TOTALS, so its 'escalation' carries real volume growth as well")
    print("as price -- which flatters a trailing rule, because a trailing rule extrapolates")
    print("growth and the others do not. The per-unit names are PHDC at 12 cells and AMOC at")
    print("1. The pooled trail3 figure is therefore not a like-for-like comparison and the")
    print("per-name blocks above are where the comparison is honest.")
    print("\nNOT A RECOMMENDATION. Selecting a rule because it scores best on this panel is")
    print("the CRPS-selection mistake the promotion rule forbids. What a table like this")
    print("can honestly do is rule a rule OUT and say how much of the error the RATE is.")
    json.dump({"cells": len(allcells)},
              open(os.path.join(HERE, "escalation_rules.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
