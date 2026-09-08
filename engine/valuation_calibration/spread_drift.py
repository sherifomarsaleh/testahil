"""Does the spread move with the price? Measured on each run's own filed record.

THE QUESTION THIS ANSWERS IS THE ONE THAT DECIDES WHERE EFFORT GOES. A forecast
of an operating company is two decisions: the RATE at which the whole income
statement escalates, and the SPREAD between its two sides. This house spends most
of its driver work on the second. Measured on the runs' own history, the first is
worth two orders of magnitude more -- AMOC's entire 0.52 log points of bias comes
from a model using 0% where 44.6% a year was needed, while its spread moved 0.97%
a year over the same window.

WHAT IS MEASURED: the realised escalation of revenue per unit against cost per
unit, from each run's own committed actuals, and the DRIFT between them. Every
figure is that company's filed record; nothing is projected and nothing is fitted.

WHY PER UNIT AND NOT IN TOTAL: volume cancels, so the drift is a statement about
price against cost rather than about how much the company grew. A run with no
committed volume series cannot answer it and is REPORTED as such rather than
omitted [R-ENF-04].

READ THE WINDOW LENGTHS, NOT ONLY THE DRIFTS. A two-year window measures a swing;
this book has one, and it is printed with its length beside it and counted
nowhere.

Read live: python3 engine/valuation_calibration/spread_drift.py
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.dirname(HERE)
MIN_YEARS = 4          # below this a window measures a swing, not a drift

# (name, class, adapter, revenue field, cost field, volume field)
RUNS = [
    ("AMOC", "refiner", "module", "net_sales", "cost_of_sales", "volume_t"),
    ("EGCH", "fertiliser", "module", "revenue", "cost_of_sales", "urea_t"),
    ("PHDC", "developer", "panel", "is.revenue", "is.cogs", "units_delivered"),
    ("TMGH", "developer", "bottom_up_json", "dev_revenue", "dev_cost", None),
    ("ARCC", "cement", "none", None, None, None),
]


def _series_module(d, rev, cost, vol):
    p = os.path.join(ENG, d)
    sys.path.insert(0, p)
    for m in ("bottom_up", "panel", "score", "macro"):
        sys.modules.pop(m, None)
    try:
        import bottom_up as B
        import panel as P
        act = getattr(B, "actual", None) or getattr(P, "actual")
        years = sorted(P.IS)
        out = []
        for fy in years:
            a = act(fy)
            r, c, v = a.get(rev), a.get(cost), a.get(vol)
            if r and c and v:
                out.append((int("".join(ch for ch in fy if ch.isdigit())[-4:]),
                            abs(r) / v, abs(c) / v))
        return out
    finally:
        sys.path.remove(p)


def _series_panel(d, rev, cost, vol):
    p = os.path.join(ENG, d)
    sys.path.insert(0, p)
    for m in ("bottom_up", "panel", "score"):
        sys.modules.pop(m, None)
    try:
        import bottom_up as B
        panel = B.load()
        out = []
        for y in sorted(panel):
            r, c, v = panel[y].get(rev), panel[y].get(cost), panel[y].get(vol)
            if r and c and v:
                out.append((y, abs(r) / v, abs(c) / v))
        return out
    finally:
        sys.path.remove(p)


def _series_bottom_up_json(d, rev, cost, vol):
    """No volume series is committed, so the two sides are taken in TOTAL and the
    drift is read as a MARGIN drift. That is a weaker statement -- a mix shift
    would show up in it -- and it is labelled rather than presented as the same
    measurement."""
    bj = json.load(open(os.path.join(ENG, d, "bottom_up.json")))
    A = {int(k): v for k, v in bj["actuals"].items()}
    out = []
    for y in sorted(A):
        r, c = A[y].get(rev), A[y].get(cost)
        if r and c:
            out.append((y, abs(r), abs(c)))
    return out


ADAPTERS = {"module": _series_module, "panel": _series_panel,
            "bottom_up_json": _series_bottom_up_json}


def drift(series):
    if len(series) < 2:
        return None
    (y0, r0, c0), (y1, r1, c1) = series[0], series[-1]
    n = y1 - y0
    if n <= 0:
        return None
    dp = (r1 / r0) ** (1.0 / n) - 1.0
    dc = (c1 / c0) ** (1.0 / n) - 1.0
    return {"from": y0, "to": y1, "years": n, "rev": dp, "cost": dc,
            "drift": (1 + dc) / (1 + dp) - 1.0,
            "margin_from": 1 - c0 / r0, "margin_to": 1 - c1 / r1}


def main():
    rows, skipped = [], []
    for name, klass, adapter, rev, cost, vol in RUNS:
        if adapter == "none":
            skipped.append((name, "no volume series committed by this run"))
            continue
        d = "%s_walkforward" % name.lower()
        if not os.path.isdir(os.path.join(ENG, d)):
            skipped.append((name, "no run directory on disk"))
            continue
        try:
            s = ADAPTERS[adapter](d, rev, cost, vol)
        except Exception as e:
            skipped.append((name, str(e)[:70]))
            continue
        r = drift(s)
        if r is None:
            skipped.append((name, "fewer than two usable years"))
            continue
        r.update(name=name, klass=klass, per_unit=(vol is not None))
        rows.append(r)

    if not rows:
        raise SystemExit("FAIL: no run measured -- that is not a clean result")

    print("Realised escalation of revenue against cost, from each run's own filed actuals\n")
    print("%-6s %-12s %-14s %5s %10s %10s %10s   %s" %
          ("name", "class", "window", "yrs", "revenue", "cost", "DRIFT", "margin"))
    for r in sorted(rows, key=lambda x: -x["years"]):
        mark = "" if r["per_unit"] else "  (totals, not per unit)"
        print("%-6s %-12s %-14s %5d %+9.1f%% %+9.1f%% %+9.2f%%   %.3f -> %.3f%s" %
              (r["name"], r["klass"], "%d-%d" % (r["from"], r["to"]), r["years"],
               100 * r["rev"], 100 * r["cost"], 100 * r["drift"],
               r["margin_from"], r["margin_to"], mark))
    for name, why in skipped:
        print("%-6s NOT MEASURED -- %s" % (name, why))

    long = [r for r in rows if r["years"] >= MIN_YEARS]
    print("\nWindows of at least %d years: %d, spanning %d name-years."
          % (MIN_YEARS, len(long), sum(r["years"] for r in long)))
    if long:
        ds = [r["drift"] for r in long]
        print("Drift range %+.2f%% to %+.2f%%; signs %s."
              % (100 * min(ds), 100 * max(ds),
                 "MIXED" if (min(ds) < 0 < max(ds)) else "ALL ONE WAY"))
        print("A drift bounded near zero with MIXED signs is a flat spread. A drift of the")
        print("same size all one way would be a slow trend, and would mean something else.")
    print("\nShorter windows are printed and NOT counted: a two-year window measures a swing.")
    json.dump({"rows": rows, "skipped": skipped, "min_years": MIN_YEARS},
              open(os.path.join(HERE, "spread_drift.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
