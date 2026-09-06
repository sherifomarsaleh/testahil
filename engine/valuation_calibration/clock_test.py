"""Are a run's revenue and its costs escalating on the SAME clock?

[L-048], registered after AMOC and re-violated since, says a model that escalates
costs at domestic inflation while holding the currency or the price still counts
one event once and ignores it once, and then reports the manufactured margin
decline as a finding. [R-MACRO-01] made the macro PATH arithmetic; it did not
make the TRANSMISSION arithmetic, and the transmission is where the defect lives.
AMOC's was found by reading its module -- brent_ratio() returns exactly 1.0
outside foresight, so its dollar-linked revenue and 88% of its cost of sales are
frozen in pounds while the remaining domestic lines compound cpi_path().

READING EVERY MODULE IS NOT A CHECK, so this measures it instead.

THE FIRST DRAFT MEASURED THE WRONG THING AND ITS ANSWER WAS BACKWARDS. It bumped
the inflation path by a point and read the ELASTICITY of each side, which is a
LOCAL derivative: AMOC came out at 0.00 revenue against 0.12 cost, a gap of
0.12, and was reported as "one clock" -- when the truth is that BOTH sides are
frozen and the real defect is a frozen level rather than an unresponsive
derivative. A local slope cannot see a level held still. Re-pointed per
[R-COC-01] rather than widened: what is measured now is the ESCALATION each side
actually applies over the horizon, against the inflation the same model believes
in over the same horizon.

    escalation(side) = projected(side, o, h) / actual(side, o)
    clock(side)      = escalation(side) / the model's own cumulative inflation

A side at clock 1.0 escalates exactly at the model's own inflation. A side near
zero is FROZEN while the economy the model believes in inflates around it.

TWO CAVEATS, both real. Revenue is volume times price, so a run that also grows
or shrinks volume moves this ratio for a reason that is not escalation -- the
volume path is printed beside it. And a genuinely dollar-linked line SHOULD sit
below domestic inflation if the currency is expected to move by less; what is
never defensible is a line at zero. This flags modules to read; the reading
settles it.

Read live: python3 engine/valuation_calibration/clock_test.py
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.dirname(HERE)
H = 3

# (name, dir, revenue driver, cost driver, volume driver or None,
#  the module attribute holding the cumulative inflation path, adapter name)
#
# EVERY RUN IS LISTED, INCLUDING THE ONES THAT CANNOT BE MEASURED THIS WAY. A
# population that quietly omits the awkward names is the failure [R-ENF-04]
# describes: three of five reported clean would read as the book being clean.
# WHERE THE GAP IS READABLE AND WHERE IT IS NOT. The gap tests [L-048] only when
# both sides of the income statement scale on the SAME volume path, so that volume
# cancels. On a single-product operating company it does. On a DEVELOPER it does
# not: revenue is a percentage release of a backlog while cost follows deliveries,
# two different quantities, so a wide gap there is the recognition mechanism
# rather than an escalation asymmetry. This was learned by reading PHDC's
# projector after its gap came out four times the next widest -- the number was
# real and the reading of it was wrong.
SHARED_VOLUME = {"AMOC": True, "EGCH": True, "ARCC": True,
                 "TMGH": False, "PHDC": False}

RUNS = [
    ("AMOC", "amoc_walkforward", "net_sales", "cost_of_sales", "volume_t", "cpi_path", "plain"),
    ("EGCH", "egch_walkforward", "revenue", "cost_of_sales", "urea_t", "cpi_path", "plain"),
    ("ARCC", "arcc_walkforward", "revenue", "cogs", "vol_total", None, "plain"),
    # TMGH: the development leg, the only revenue and cost pair its projection
    # and its actuals BOTH carry. total_revenue is projected and never recorded
    # as an actual under that name, so pairing them would compare a sum against
    # a leg.
    ("TMGH", "tmgh_walkforward", "dev_revenue", "dev_cost", None, None, "tmgh"),
    # PHDC's two sides do NOT share a volume driver: revenue is a percentage
    # release of a backlog (delta x (backlog + new sales)) while cost is unit
    # cost x DELIVERIES. The gap is therefore not volume-free on this run and
    # cannot be read as an escalation asymmetry -- see SHARED_VOLUME below.
    ("PHDC", "phdc_walkforward", "is.revenue", "is.cogs", "units_delivered", None, "phdc"),
]


def _adapt_tmgh(rev, cost, vol):
    """TMGH's projector takes its panel and macro paths as arguments and returns
    every horizon at once, so there is no module-level cells()/actual() to drive
    the common path. Its committed bottom_up.json carries exactly the same three
    quantities -- the projection, the actuals and the inflation the origin
    believed in -- so it is read from there rather than the module being
    reshaped to suit a checker."""
    bj = json.load(open(os.path.join(ENG, "tmgh_walkforward", "bottom_up.json")))
    A = {int(k): v for k, v in bj["actuals"].items()}
    rows = []
    for key, run in bj["runs"].items():
        o, setting = key.split("|")
        if setting != "asknown":
            continue
        o = int(o)
        f = run["projection"].get(str(H)) or run["projection"].get(H)
        if not f or o not in A:
            continue
        pi = run["params"].get("cpi_known")
        if pi is None:
            continue
        rec = {"origin": o, "infl": (1.0 + pi) ** H}
        for lab, drv in (("rev", rev), ("cost", cost), ("vol", vol)):
            if not drv:
                continue
            pv, av = f.get(drv), A[o].get(drv)
            # A cost recorded as a negative is a sign convention, not a missing
            # value. The first draft filtered on av > 0 and dropped every cost
            # line TMGH commits, then reported the run untestable -- an absent
            # answer wearing the costume of a result [R-ENF-04].
            rec[lab] = (abs(pv) / abs(av)) if (pv and av) else None
        rows.append(rec)
    return rows


def _adapt_phdc(rev, cost, vol):
    """PHDC's projector is panel-driven and exposes no module-level cells(), so
    the common path cannot drive it. Its committed error_cells.json carries the
    projection and the actual for every (origin, horizon, field), and THE ACTUAL
    AT AN ORIGIN IS RECOVERABLE FROM THE CELL WHOSE TARGET *IS* THAT ORIGIN --
    a later origin's own base year is an earlier origin's forecast year. Nothing
    is estimated: every figure below is one this run already committed.

    The inflation the origin believed in is the same construction the module
    itself uses on the as-known path -- a trailing three-year mean of Egyptian
    CPI -- read from the run's own macro_eg.json rather than recomputed.
    """
    d = os.path.join(ENG, "phdc_walkforward")
    cells = json.load(open(os.path.join(d, "error_cells.json")))["as_known"]
    cpi = {int(k): v / 100.0 for k, v in
           json.load(open(os.path.join(d, "macro_eg.json")))["cpi_pct"].items()}

    actual_at = {}
    for c in cells:
        t, f, a = c.get("target"), c.get("field"), c.get("actual")
        if t is not None and f and a is not None:
            actual_at.setdefault(int(t), {})[f] = a

    def ttm3(o):
        vs = [cpi[y] for y in (o - 2, o - 1, o) if y in cpi]
        return (sum(vs) / len(vs)) if len(vs) == 3 else None

    rows = []
    for c in cells:
        if c.get("h") != H:
            continue
        o, f, pv = int(c["origin"]), c.get("field"), c.get("proj")
        if pv is None:
            continue
        pi = ttm3(o)
        if pi is None or o not in actual_at:
            continue
        rec = None
        for lab, drv in (("rev", rev), ("cost", cost), ("vol", vol)):
            if drv and f == drv:
                av = actual_at[o].get(drv)
                if av:
                    rec = (o, pi, lab, abs(pv) / abs(av))
        if rec:
            rows.append(rec)

    by_o = {}
    for o, pi, lab, v in rows:
        r = by_o.setdefault(o, {"origin": o, "infl": (1.0 + pi) ** H})
        r[lab] = v
    return list(by_o.values())


def measure(d, rev, cost, vol, attr, adapter="plain"):
    if adapter == "tmgh":
        return _adapt_tmgh(rev, cost, vol)
    if adapter == "phdc":
        return _adapt_phdc(rev, cost, vol)
    p = os.path.join(ENG, d)
    sys.path.insert(0, p)
    for m in ("bottom_up", "panel", "score", "macro"):
        sys.modules.pop(m, None)
    import bottom_up as B
    # Each run names its own actuals resolver: some expose actual() on the
    # projector module, others only on the panel. Both are tried and a run that
    # exposes neither is REPORTED untestable rather than skipped [R-ENF-04].
    act = getattr(B, "actual", None)
    if act is None:
        try:
            import panel as _P
            act = getattr(_P, "actual", None)
        except Exception:
            act = None
    if act is None:
        sys.path.remove(p)
        raise RuntimeError("no actual() on the projector module or its panel")
    try:
        rows = []
        for o, h, t in B.cells():
            if h != H:
                continue
            pr, a0 = B.project(o, h), act(o)
            pi = None
            if attr and hasattr(B, attr):
                pi = getattr(B, attr)(o, h)
            elif hasattr(B, "cpi"):
                pi = (1 + B.cpi(o)) ** h
            if not pi:
                continue
            rec = {"origin": o, "infl": pi}
            for lab, drv in (("rev", rev), ("cost", cost), ("vol", vol)):
                if not drv:
                    continue
                pv, av = pr.get(drv), a0.get(drv)
                rec[lab] = (abs(pv) / abs(av)) if (pv and av) else None
            rows.append(rec)
    finally:
        sys.path.remove(p)
    return rows


def main():
    print("Clock test -- what each side actually escalates by, against the model's own inflation")
    print("Horizon %d years. clock = escalation / the model's own cumulative inflation.\n" % H)
    print("%-6s %8s %8s %8s %8s %8s %8s %8s %9s %9s" %
          ("name", "infl", "rev x", "cost x", "vol x", "rev clk", "cost clk", "gap",
           "price clk", "unitcost"))
    tested = 0
    untestable = []
    for name, d, rev, cost, vol, attr, adapter in RUNS:
        if not os.path.isdir(os.path.join(ENG, d)):
            untestable.append((name, "no run directory on disk"))
            continue
        try:
            rows = measure(d, rev, cost, vol, attr, adapter)
        except Exception as e:
            untestable.append((name, str(e)[:90]))
            continue
        rows = [r for r in rows if r.get("rev") and r.get("cost")]
        if not rows:
            untestable.append((name, "no cell at horizon %d carries both sides" % H))
            continue
        tested += 1
        # A CLOCK IS AVERAGED, NEVER A RATIO OF AVERAGES. The first draft took
        # mean(rev)/mean(inflation), which is a ratio of two averages over origins
        # whose inflation differs by half again -- it weights the high-inflation
        # origins into the denominator and the high-growth ones into the
        # numerator, and on PHDC it reported a price clock of 1.02 where every
        # single origin sits between 1.05 and 1.13. Each origin's own clock is
        # formed first and the clocks are averaged.
        def per_origin(key):
            vs = [r[key] / r["infl"] for r in rows if r.get(key) is not None]
            return (sum(vs) / len(vs)) if vs else None

        def raw(key):
            vs = [r[key] for r in rows if r.get(key) is not None]
            return (sum(vs) / len(vs)) if vs else None

        infl, r_, c_ = raw("infl"), raw("rev"), raw("cost")
        v_ = raw("vol") if any(r.get("vol") for r in rows) else None
        rev_clk, cost_clk = per_origin("rev"), per_origin("cost")
        unit = [(r["rev"] / r["vol"] / r["infl"], r["cost"] / r["vol"] / r["infl"])
                for r in rows if r.get("vol") and r.get("rev") and r.get("cost")]
        pc = (sum(a for a, _ in unit) / len(unit)) if unit else None
        uc = (sum(b for _, b in unit) / len(unit)) if unit else None
        shared = SHARED_VOLUME.get(name)
        gap = "%+.2f" % (cost_clk - rev_clk) if shared else "n/a"
        print("%-6s %8.2f %8.2f %8.2f %8s %8.2f %8.2f %8s %9s %9s" %
              (name, infl, r_, c_, ("%.2f" % v_) if v_ else "-",
               rev_clk, cost_clk, gap,
               ("%.2f" % pc) if (pc and shared) else "-",
               ("%.2f" % uc) if (uc and shared) else "-"))
    for name, why in untestable:
        print("%-6s UNTESTABLE -- %s" % (name, why))
    if not tested:
        raise SystemExit("FAIL: no run was testable -- that is not a clean result")
    if tested < 3:
        raise SystemExit("FAIL: only %d of %d runs measured; too few to read"
                         % (tested, len(RUNS)))
    print("\nA side at clock 1.00 escalates exactly at the model's own inflation.")
    print("A side near zero is FROZEN while the economy the model believes in inflates.")
    print("\nGAP n/a MEANS THE TWO SIDES DO NOT SHARE A VOLUME PATH, so volume does not")
    print("cancel and the difference is a recognition mechanism rather than an escalation")
    print("asymmetry. PHDC releases revenue as a percentage of backlog while its cost")
    print("follows deliveries; its raw difference is the widest in the book and means")
    print("nothing about [L-048]. Reported as not applicable rather than as a finding.")
    print("\nTHE GAP IS THE ROBUST COLUMN AND THE LEVELS ARE NOT. Revenue is volume times")
    print("price, so a run projecting real growth or decline moves BOTH clocks together for")
    print("a reason that is not escalation -- TMGH sits near 1.9 on both because it forecasts")
    print("a growing book, which is a forecast rather than a defect. Volume cancels out of the")
    print("GAP, so the gap is what tests [L-048]: costs escalating while revenue sits still.")
    print("A level far BELOW 1.00 on BOTH sides is the other defect, and it is not [L-048]:")
    print("it is a whole model standing still in nominal terms inside an economy it says is")
    print("inflating, which is a real-terms decline nothing disclosed.")
    print("\nWhere a volume path is committed, PRICE CLK and UNITCOST divide it out. Those two")
    print("are what a margin forecast actually rests on, and a model escalating one faster")
    print("than the other has forecast a margin move that nothing in the filings sourced --")
    print("in EITHER direction. The book carries both signs, so a single correction would")
    print("make half of it worse [R-TERM-01 CLAUSE TWO].")


if __name__ == "__main__":
    main()
