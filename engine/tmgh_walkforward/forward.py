"""TMGH walk-forward — the forward projection, and the ranges it earns.

Origin FY2025 is struck but unresolved: it contributes no error and produces the
projection the current update consumes. Years 3-5 are published as RANGES built
from this record's OWN driver-error distribution [L-011] — never as points.

The range is the empirical distribution of this method's log errors at that
horizon, applied to the central path. It is not a confidence interval in any
model sense; it is what the method has actually done, on this company, at that
distance, over ten origins whose cells are not independent.

The guidance ledger sits here too, and guidance is SCORED, never consumed
[L-012]: management's forward targets lean the same way an optimistic model
does, so a driver that takes guidance as an input inherits the lean.
"""
import json, math, os, statistics, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bottom_up as BU
import score as SC

CENTRAL = ["new_sales", "dev_revenue", "recurring_revenue", "total_revenue",
           "gross_profit", "net_profit"]

# Management's own forward targets, and what happened. Scored, never consumed.
GUIDANCE = [
    {"given_for": 2021, "target": "EGP 30bn new sales (raised mid-year from a lower number)",
     "target_mid": 30000.0, "outcome": 32400.0,
     "source": "FY2021 earnings release: 'largely exceeding the sales guidance of EGP30bn'"},
    {"given_for": 2022, "target": "EGP 24-26bn new sales", "target_mid": 25000.0,
     "outcome": 33200.0,
     "source": "9M2022 and FY2022 earnings releases: 'exceeding the upper limit of its "
               "annual sales guidance of EGP24-26bn'"},
    {"given_for": 2024, "target": "internal sales targets for the full year",
     "target_mid": None, "outcome": 504000.0,
     "source": "FY2024 earnings release: 'surpassing the company's internal sales "
               "targets for the entire year in just few [months]' — no figure published, "
               "so it cannot be graded"},
]


def error_quantiles(rows, driver, h, setting="asknown", applied=0.0):
    """The method's own error distribution at this horizon.

    Where a correction is applied to the central path, the SAME correction is
    applied to the errors the range is built from. Building the band from raw
    errors around a corrected centre put the FY2026 net-profit central value
    outside its own published range — the range and the number it surrounds
    have to describe the same method.
    """
    e = [r["log_error"] - applied for r in rows
         if r["setting"] == setting and r["driver"] == driver
         and r["horizon"] == h and "log_error" in r]
    if len(e) < 3:
        return None
    e.sort()
    def q(p):
        i = min(len(e) - 1, max(0, int(round(p * (len(e) - 1)))))
        return e[i]
    return {"n": len(e), "p10": q(0.10), "p50": q(0.50), "p90": q(0.90),
            "lo": e[0], "hi": e[-1]}


def main():
    bj = json.load(open(os.path.join(HERE, "bottom_up.json")))
    rows = json.load(open(os.path.join(HERE, "error_cells.json")))
    corr = json.load(open(os.path.join(HERE, "corrections_log.json")))
    adopted = set(corr["adopted"])

    o = bj["last_origin"]
    run = bj["runs"].get("%d|asknown" % o)
    if run is None:
        raise SystemExit("no unresolved origin to project from")

    out = {}
    for h in BU.HORIZONS:
        y = o + h
        f = run["projection"].get(str(h), {})
        row = {}
        for d in CENTRAL:
            p = f.get(d)
            if p is None:
                continue
            # the adopted correction, at half strength, as §8 fixed it
            # §8 is expanding-window ONLY: the correction carried forward is the
            # one the LAST origin would have had from outcomes resolved before
            # it, not the pooled bias over the whole record. Using the pooled
            # figure would let outcomes the origin could not have seen set its
            # own correction, and on the launch-era origins it double-counts the
            # boom it is trying to correct for.
            est = corr["detail"][d].get("expanding_estimates", {}) if d in corr["detail"] else {}
            applied = 0.0
            if d in adopted:
                last = max((int(k) for k in est), default=None)
                if last is not None:
                    applied = est[str(last)]["applied"] if str(last) in est else est[last]["applied"]
            adj = p * math.exp(-applied) if applied else None
            central = adj if adj is not None else p
            q = error_quantiles(rows, d, h, applied=applied)
            cell = {"raw": p, "corrected": adj, "central": central,
                    "correction_applied_log": applied,
                    "correction_basis": "expanding window at the last origin, half strength"}
            if q:
                # An error of +e means the method ran HIGH, so the outcome band
                # is the central path divided through the error distribution.
                # The band's OWN MEDIAN is reported as the published centre: the
                # mechanical path is the method's point estimate, and where the
                # method has a standing bias that point sits outside the band it
                # earns. On net profit it does — the method over-forecasts, so
                # the honest centre is below the model's own number, and saying
                # so is the whole purpose of measuring the bias.
                cell.update({
                    "n_observations": q["n"],
                    "median_of_band": central / math.exp(q["p50"]),
                    "low": central / math.exp(q["p90"]),
                    "high": central / math.exp(q["p10"]),
                    "widest_low": central / math.exp(q["hi"]),
                    "widest_high": central / math.exp(q["lo"])})
            row[d] = cell
        out[str(y)] = row

    # guidance ledger
    graded = [g for g in GUIDANCE if g["target_mid"]]
    led = []
    for g in graded:
        led.append(dict(g, log_error=math.log(g["target_mid"] / g["outcome"]),
                        direction="under-promised" if g["target_mid"] < g["outcome"]
                        else "over-promised"))
    bias = statistics.fmean(x["log_error"] for x in led) if led else None

    json.dump({"origin": o, "projection": out,
               "corrections_applied": sorted(adopted),
               "guidance_ledger": {"entries": led, "mean_log_error": bias,
                                   "n_gradeable": len(led),
                                   "n_published": len(GUIDANCE)}},
              open(os.path.join(HERE, "forward_ranges.json"), "w"), indent=1)

    print("Forward projection from origin FY%d — EGP mn, ranges from this "
          "record's own error distribution\n" % o)
    print("%-20s %5s %11s %11s %24s %4s"
          % ("driver", "year", "model path", "band median", "band (p10-p90)", "n"))
    for y in sorted(out, key=int):
        for d in CENTRAL:
            c = out[y].get(d)
            if not c:
                continue
            rng = ("%,.0f - %,.0f".replace(",", "") % (c["low"], c["high"])
                   if "low" in c else "-")
            print("%-20s %5s %11.0f %11s %24s %4s"
                  % (d, y, c["raw"],
                     "%.0f" % c["median_of_band"] if "median_of_band" in c else "-",
                     rng, c.get("n_observations", "-")))
        print()
    print("=== guidance ledger — scored, never consumed ===")
    for g in led:
        print("  FY%d target %s -> outcome %.0f : %s (log error %+0.3f)"
              % (g["given_for"], "%.0f" % g["target_mid"], g["outcome"],
                 g["direction"], g["log_error"]))
    ng = [g for g in GUIDANCE if not g["target_mid"]]
    for g in ng:
        print("  FY%d %s" % (g["given_for"], g["source"]))
    if bias is not None:
        print("  mean log error of published guidance: %+0.3f "
              "(negative = management guided BELOW the outcome)" % bias)


if __name__ == "__main__":
    main()
