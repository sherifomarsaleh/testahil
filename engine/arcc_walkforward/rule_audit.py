"""ARCC — every driver rule read against what the company reported, then fixed in a
pre-registered order with the net re-measured after each.

TWO HALVES, AND THE ORDER MATTERS. The first half MEASURES: what rate each line
actually ran at, what rule the model applies to it, and what that rule costs in
pounds of profit. The second half FIXES, one lever at a time, in an order fixed by
the first half's own numbers before any lever was written — largest measured cost
first. [R-VCAL-01]'s promotion guard, applied to driver rules rather than to
valuation levers, and for the reason it was written: several individually justified
corrections stack into an overshoot.

WHY BOTH HALVES ARE HERE. The audit found the errors run BOTH ways — EGP 77bn of
rules that under-forecast profit against EGP 54bn that over-forecast it, netting to
23bn. Fixing the single largest lever alone swings the net from -23bn to +7.9bn.
A fix list that is not measured cumulatively is a list of individually correct
changes that together make the model worse.

EVERY REPLACEMENT RULE IS KNOWABLE AT THE ORIGIN. No lever reads a figure published
after the origin it is applied at. Where a line's own history is too short or turns
non-positive, the lever DECLINES for that cell and the original rule stands, and the
count of declines is printed — a lever that quietly fell back would be scored as if
it had been applied.

NO CAP, NO WINDOW PARAMETER. Trailing growth is the geometric mean over EVERY prior
year the origin can see, not a 3-year window somebody chose, and it is not clipped.
Both would be free parameters the promotion rule forbids, and an uncapped rate that
explodes is a finding rather than something to hide.
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bottom_up as B  # noqa: E402

# The rule the model applies to each line, for the audit table.
RULE = {
    "vol_local": "x population growth", "vol_export": "FLAT",
    "price_local": "x CPI", "price_export": "x FX depreciation",
    "services": "x CPI", "raw_per_t": "x (w.coal + (1-w).CPI), coal FROZEN",
    "transport_per_t": "x CPI", "overhead_per_t": "x CPI", "ga": "x CPI",
    "mfg_dep": "FLAT", "amort": "FLAT", "provisions": "FLAT",
    "interest_income": "FLAT", "other_income": "FLAT", "finance_costs": "FLAT",
}


def actuals():
    out = {}
    for o in B.ORIGINS:
        try:
            out[o] = B.actual(o)
        except Exception:
            pass
    return out


def geo(series):
    """Geometric mean growth over every consecutive pair. None if not usable."""
    vals = [v for v in series if isinstance(v, (int, float)) and v > 0]
    if len(vals) < 3:
        return None
    return (vals[-1] / vals[0]) ** (1.0 / (len(vals) - 1)) - 1.0


def trailing(A, key, origin):
    """The line's own growth rate over everything the ORIGIN can see. Never later."""
    ys = [o for o in sorted(A) if B._y(o) <= B._y(origin)]
    return geo([A[o].get(key) for o in ys])


# --------------------------------------------------------------- the levers
def lever_price_local(A, o, h, p, ctx):
    """The company's own price premium over consumer inflation, from its own history.

    Cement is not the consumer basket. Escalating a works price at CPI asserts they
    move together; this company's own record says its price ran 6 points a year
    above it. The PREMIUM is what is carried forward, not the price growth itself,
    so the lever still rides the inflation path the origin knows."""
    g = trailing(A, "price_local", o)
    pi = B.cpi(o)
    if g is None or pi is None or (1 + pi) <= 0:
        return None
    prem = (1 + g) / (1 + pi)
    p["price_local"] = A[o]["price_local"] * ((1 + pi) * prem) ** h
    return "premium %+.1f%% a year over CPI" % (100 * (prem - 1))


def lever_volume_mix(A, o, h, p, ctx):
    """Each leg on its own drift instead of population growth and a freeze.

    Total volume looks right only because a local over-forecast and an export
    under-forecast cancel in tonnes. They do not cancel in pounds, because the two
    legs sell at different prices."""
    gl, ge = trailing(A, "vol_local", o), trailing(A, "vol_export", o)
    if gl is None or ge is None:
        return None
    p["vol_local"] = A[o]["vol_local"] * (1 + gl) ** h
    p["vol_export"] = A[o]["vol_export"] * (1 + ge) ** h
    return "local %+.1f%%, export %+.1f%% a year" % (100 * gl, 100 * ge)


def lever_coal_on_fx(A, o, h, p, ctx):
    """Imported coal is priced in dollars, so its EGP cost carries the currency.

    The model freezes the coal multiplier at 1.0 outside foresight, which asserts
    that an imported input costs the same in pounds after a devaluation."""
    fx = B.fx_dep(o)
    if fx is None:
        return None
    w = B.W_DEFAULT
    pi = B.cpi(o)
    p["raw_per_t"] = A[o]["raw_per_t"] * (w * (1 + fx) ** h + (1 - w) * (1 + pi) ** h)
    return "coal leg at FX, %+.1f%% a year" % (100 * fx)


def lever_price_export(A, o, h, p, ctx):
    """The export price's own premium over the currency, from its own history."""
    g = trailing(A, "price_export", o)
    fx = B.fx_dep(o)
    if g is None or fx is None or (1 + fx) <= 0:
        return None
    prem = (1 + g) / (1 + fx)
    p["price_export"] = A[o]["price_export"] * ((1 + fx) * prem) ** h
    return "premium %+.1f%% a year over FX" % (100 * (prem - 1))


def _own_rate(A, o, h, p, keys, label):
    used = []
    for k in keys:
        g = trailing(A, k, o)
        if g is None:
            continue
        p[k] = A[o][k] * (1 + g) ** h
        used.append("%s %+.1f%%" % (k, 100 * g))
    return (label + ": " + ", ".join(used)) if used else None


def lever_transport(A, o, h, p, ctx):
    """Road haulage follows diesel, which is administered and moves in steps of its
    own. No diesel series is held, so the company's own realised haulage cost is the
    closest knowable proxy — and it ran at more than twice CPI."""
    return _own_rate(A, o, h, p, ["transport_per_t"], "own rate")


def lever_opex(A, o, h, p, ctx):
    """Services, overheads and administration on their own rates rather than one
    shared consumer index."""
    return _own_rate(A, o, h, p, ["services", "overhead_per_t", "ga"], "own rates")


def lever_nonop(A, o, h, p, ctx):
    """The frozen non-operating lines. Interest income follows the policy rate,
    which trebled across this window while the model held the income still."""
    return _own_rate(A, o, h, p, ["interest_income", "other_income", "provisions"],
                     "own rates")


def lever_runoff(A, o, h, p, ctx):
    """The two lines that genuinely decline — amortisation as assets complete their
    life, finance costs as the book runs off. Freezing them OVER-forecasts."""
    return _own_rate(A, o, h, p, ["amort", "finance_costs"], "own rates")


# ORDER FIXED BY THE AUDIT'S OWN MEASURED COST, LARGEST FIRST, BEFORE ANY LEVER
# BELOW WAS WRITTEN. The volume legs are ONE lever because they are one decision.
LEVERS = [
    ("price, local", lever_price_local),
    ("the volume mix", lever_volume_mix),
    ("raw material — coal on the currency", lever_coal_on_fx),
    ("price, export", lever_price_export),
    ("transport per tonne", lever_transport),
    ("services, overhead, administration", lever_opex),
    ("the frozen non-operating lines", lever_nonop),
    ("amortisation and finance costs", lever_runoff),
]


def rebuild(p, A, o):
    """Re-foot the statement from whatever the levers changed. One definition of
    each aggregate, so a lever cannot move a driver and leave the total behind."""
    a = A[o]
    p["vol_total"] = p["vol_local"] + p["vol_export"]
    vt = p["vol_total"]
    p["revenue"] = (p["price_local"] * p["vol_local"] * 1000.0
                    + p["price_export"] * p["vol_export"] * 1000.0 + p["services"])
    p["raw"] = p["raw_per_t"] * vt * 1000.0
    p["transport"] = p["transport_per_t"] * vt * 1000.0
    p["overhead"] = p["overhead_per_t"] * vt * 1000.0
    p["cogs"] = (p["raw"] + p["transport"] + p["overhead"]
                 + p["mfg_dep"] + p["amort"] + a["rou"])
    p["gross_profit"] = p["revenue"] - p["cogs"]
    p["pbt"] = (p["gross_profit"] - p["ga"] - p["provisions"] + a["reversals"]
                - a["impairments"] + p["interest_income"] + p["other_income"]
                - p["finance_costs"] + a["disposals"] + a["jv"])
    p["tax"] = B.TAX_RATE * p["pbt"] if p["pbt"] > 0 else 0.0
    p["pat"] = p["pbt"] - p["tax"]
    return p


def net_miss(A, upto):
    """Profit before tax, projected minus actual, summed over every matured cell.

    PBT rather than a driver-by-driver attribution, because the whole point of
    measuring cumulatively is that the drivers interact: a lever that raises revenue
    and one that raises cost do not add."""
    tot = 0.0
    n = 0
    declined = 0
    notes = {}
    for o in B.ORIGINS:
        for h in B.HORIZONS:
            ty = "FY%d" % (B._y(o) + h)
            if ty not in A:
                continue
            try:
                p = dict(B.project(o, h))
            except Exception:
                continue
            for name, fn in LEVERS[:upto]:
                r = fn(A, o, h, p, None)
                if r is None:
                    declined += 1
                else:
                    notes.setdefault(name, r)
            if upto:
                p = rebuild(p, A, o)
            tot += p["pbt"] - A[ty]["pbt"]
            n += 1
    return tot, n, declined, notes


def report():
    A = actuals()
    ys = sorted(A)
    cpis = [B.cpi(o) for o in ys[1:] if B.cpi(o) is not None]
    m = 1.0
    for c in cpis:
        m *= (1 + c)
    CPI = m ** (1.0 / len(cpis)) - 1

    print("ARCC — WHAT EACH LINE DID, AND WHAT RULE THE MODEL APPLIES TO IT")
    print("  realised consumer inflation over the window: %+.1f%% a year\n" % (100 * CPI))
    print("  %-18s %10s   %s" % ("line", "realised", "rule in the model"))
    for k, rule in sorted(RULE.items(),
                          key=lambda kv: -(geo([A[o].get(kv[0]) for o in ys]) or -9)):
        g = geo([A[o].get(k) for o in ys])
        if g is None:
            continue
        print("  %-18s %+9.1f%%   %s" % (k, 100 * g, rule))

    print("\n\nFIXING THEM, IN THE ORDER THE AUDIT'S OWN NUMBERS FIXED BEFORE ANY")
    print("LEVER WAS WRITTEN — largest measured cost first, net re-measured after each\n")
    base, n, _d, _x = net_miss(A, 0)
    print("  %-38s %14s %12s" % ("after applying", "net PBT miss", "move"))
    print("  %-38s %14s %12s" % ("(nothing — the model as it stands)",
                                 "{:+,.0f}".format(base), ""))
    prev = base
    crossed = None
    for i, (name, _fn) in enumerate(LEVERS, start=1):
        cur, n2, dec, notes = net_miss(A, i)
        flag = ""
        if prev < 0 <= cur or prev > 0 >= cur:
            flag = "  <-- CROSSES ZERO"
            if crossed is None:
                crossed = i
        print("  %-38s %14s %12s%s"
              % ("+ " + name, "{:+,.0f}".format(cur), "{:+,.0f}".format(cur - prev), flag))
        if dec:
            print("  %-38s %s" % ("", "lever declined on %d cell(s) — original rule stood" % dec))
        prev = cur
    print("\n  %d matured cells. NET is projected minus actual profit before tax," % n)
    print("  summed. Negative means the model forecast LESS profit than the company")
    print("  earned.")
    if crossed:
        print("\n  THE SEQUENCE CROSSES ZERO AT LEVER %d. Under [R-VCAL-01]'s promotion" % crossed)
        print("  guard that is where it stops: past this point the corrections are")
        print("  no longer removing a lean, they are building the opposite one.")
    return base


if __name__ == "__main__":
    report()


# ---------------------------------------------------------------------------
# PART THREE — the drivers those lines actually have, rather than a statistical
# rule laid over them. Fix A failed because extrapolation cannot cross a regime
# break. These do not extrapolate the line; they name what moves it.
# ---------------------------------------------------------------------------

def real_volume_mix(A, o, h, p, ctx):
    """The kiln runs; local demand decides how much stays home; export takes the rest.

    That is the physical fact this plant operates under and it is what the run's own
    B-9 records: exports went from 1% of tonnes to 48% while local sales FELL. The
    model grows local at POPULATION GROWTH and freezes export, which asserts the
    opposite of both.

    Total volume is forecast on its own trailing rate — the one volume quantity the
    model already gets right, at a bias of -0.019 — and the EXPORT SHARE drifts at
    the rate it has been drifting, bounded to [0,1] because a share cannot leave it.
    Knowable at the origin: both series are the company's own disclosed tonnages."""
    ys = [x for x in sorted(A) if B._y(x) <= B._y(o)]
    if len(ys) < 3:
        return None
    tot = [A[x]["vol_local"] + A[x]["vol_export"] for x in ys]
    sh = [A[x]["vol_export"] / t if t else None for x, t in zip(ys, tot)]
    if any(t is None or t <= 0 for t in tot) or any(s is None for s in sh):
        return None
    g = (tot[-1] / tot[0]) ** (1.0 / (len(tot) - 1)) - 1.0
    d = (sh[-1] - sh[0]) / (len(sh) - 1)          # share drift, per year, LINEAR
    s_h = min(1.0, max(0.0, sh[-1] + d * h))
    v = tot[-1] * (1 + g) ** h
    p["vol_export"] = v * s_h
    p["vol_local"] = v * (1 - s_h)
    return "total %+.1f%% a year, export share %.0f%% drifting %+.1f pts a year" % (
        100 * g, 100 * sh[-1], 100 * d)


def real_nonop_scales(A, o, h, p, ctx):
    """A company twice the size in nominal pounds earns about twice the interest.

    Freezing a nominal non-operating line asserts the opposite — that it stays the
    same number of pounds while the business it sits inside trebles. This does not
    extrapolate those lines' own noisy histories (Fix A showed that fails); it ties
    them to the size of the business the model is already forecasting."""
    r0 = A[o].get("revenue")
    if not r0 or not p.get("revenue"):
        return None
    k = p["revenue"] / r0
    for f in ("interest_income", "other_income", "provisions"):
        if A[o].get(f) is not None:
            p[f] = A[o][f] * k
    return "scaled with revenue, x%.2f at this horizon" % k


def real_amortisation(A, o, h, p, ctx):
    """DECLINED, AND THE REASON IS THE FINDING.

    Amortisation is the one line here that is fully deterministic: the intangibles
    note gives cost and accumulated amortisation per asset, so the remaining life —
    and the exact year the charge steps down — is arithmetic. ARCC's FY2025 note
    shows the operating licence at cost 563,204,713 against accumulated 428,248,847
    and a charge of 28,156,249, and the electricity contract fully amortised. That
    is a schedule, not a forecast.

    THE RUN DOES NOT COMMIT IT. Its panel carries the amortisation CHARGE and not
    the schedule behind it, so the driver cannot be built from what this run holds —
    the same class of gap the valuation-input block was created to close, arriving
    on a different line. Recorded as declined with its reason rather than replaced
    by something that merely looks like a driver."""
    return None


REAL = [
    ("the volume mix, on the kiln's own physics", real_volume_mix),
    ("non-operating lines scaled to the business", real_nonop_scales),
    ("amortisation from the disclosed schedule", real_amortisation),
]


def net_real(A, upto):
    tot = 0.0
    n = 0
    dec = {}
    notes = {}
    for o in B.ORIGINS:
        for h in B.HORIZONS:
            ty = "FY%d" % (B._y(o) + h)
            if ty not in A:
                continue
            try:
                p = dict(B.project(o, h))
            except Exception:
                continue
            for name, fn in REAL[:upto]:
                r = fn(A, o, h, p, None)
                if r is None:
                    dec[name] = dec.get(name, 0) + 1
                else:
                    notes.setdefault(name, r)
            if upto:
                p = rebuild(p, A, o)
            tot += p["pbt"] - A[ty]["pbt"]
            n += 1
    return tot, n, dec, notes


def report_real():
    A = actuals()
    print("\n\nPART THREE — THE DRIVERS THOSE LINES ACTUALLY HAVE\n")
    base, n, _d, _x = net_real(A, 0)
    print("  %-46s %16s %14s" % ("after applying", "net PBT miss", "move"))
    print("  %-46s %16s" % ("(nothing — the model as it stands)",
                            "{:+,.0f}".format(base)))
    prev = base
    for i, (name, _fn) in enumerate(REAL, start=1):
        cur, n2, dec, notes = net_real(A, i)
        print("  %-46s %16s %14s"
              % ("+ " + name, "{:+,.0f}".format(cur), "{:+,.0f}".format(cur - prev)))
        if name in notes:
            print("  %-46s %s" % ("", notes[name]))
        if name in dec:
            print("  %-46s DECLINED on %d of %d cells" % ("", dec[name], n2))
        prev = cur
    print("\n  %d matured cells. Negative = the model forecast LESS profit than the"
          % n)
    print("  company earned. Compare with Fix A, which reached -37.0bn.")
