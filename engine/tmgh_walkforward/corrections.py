"""TMGH walk-forward — corrections: estimated, tested, and mostly refused.

The rule was fixed in §8 of the pre-registration before any error was computed:
expanding window only, half strength by default, applied ONLY where the bias
holds its sign across eras, reset after a structural break, and — the clause
that does the real work — a correction enters the live drivers only if it ALSO
matches how that driver class is built across the market's book.

That second clause is not a formality. On PHDC it blocked a finance-cost
correction that had passed its own test convincingly, and the block is what
exposed the arithmetic error underneath [L-002], [L-003]. It bites here too,
for a different reason, and the reason is recorded rather than worked around.
"""
import json, math, os, statistics, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bottom_up as BU
import score as SC

HALF = 0.5
TWO_SIGMA = 2.0

# How the same driver is built across this repo's book. Filled from the studies
# themselves, not from memory — the second-clause test reads this.
CLASS_PRACTICE = {
    "finance_cost": {
        "how_the_book_builds_it": (
            "from NAMED facilities, each at its own disclosed rate, against the "
            "borrowings that actually bear interest (engine/phdc_study, "
            "engine/du_study, engine/arcc_study all do this)"),
        "how_this_run_builds_it": (
            "a single effective rate kd = finance cost / opening interest-bearing "
            "debt, with debt held flat"),
        "consistent": False,
        "why": (
            "TMG's reported finance cost is NOT interest on its borrowings alone. "
            "The FY2025 note splits it into finance expenses of EGP 3,820.4mn and "
            "bank charges of EGP 116.2mn, against opening interest-bearing debt of "
            "EGP 8,928mn - an implied 44%, against an Egyptian policy rate that "
            "peaked near 27.25%. The excess is the unwinding of the significant "
            "financing component the company recognises on customer contracts "
            "(FY2025 statements, note 2.3) plus factoring charges, neither of "
            "which arises on a loan. The ratio this run measures is therefore an "
            "effective charge per unit of BORROWING, not a borrowing rate, and the "
            "statements do not disclose the split. Correcting a driver whose "
            "denominator does not match its numerator would be a multiplier over "
            "a mis-specification - the same species as PHDC's blocked correction, "
            "arrived at from the opposite direction: there the denominator was too "
            "broad, here the numerator is."),
    },
    "da": {
        "how_the_book_builds_it": (
            "a depreciation rate on an opening PP&E balance that the model has "
            "also projected, from a disclosed capex programme where one exists"),
        "how_this_run_builds_it": "the same",
        "consistent": True,
        "why": "the construction matches the book; the correction is judged on its own test",
    },
    "development_properties": {
        "how_the_book_builds_it": (
            "a work-in-progress roll: opening balance plus build spend less cost "
            "recognised, both driven off the same contract book"),
        "how_this_run_builds_it": "the same",
        "consistent": True,
        "why": "the construction matches the book",
    },
    "new_sales": {
        "how_the_book_builds_it": (
            "an exogenous market anchor (population x penetration x share), which "
            "every study of this class uses and which [L-101] records as running "
            "low for developers because volume is set by the launch calendar"),
        "how_this_run_builds_it": "the same",
        "consistent": True,
        "why": ("the construction matches the book - but see the era test: this "
                "driver's miss is a launch calendar, not a calibration offset"),
    },
    "backlog": {
        "how_the_book_builds_it": "rolled from new sales less revenue recognised",
        "how_this_run_builds_it": "the same",
        "consistent": True,
        "why": "the construction matches the book",
    },
}


def by_driver(rows, setting="asknown"):
    d = defaultdict(list)
    for r in rows:
        if r["setting"] == setting and "log_error" in r:
            d[r["driver"]].append(r)
    return d


def expanding_estimates(rows):
    """The correction each origin WOULD have had, using only earlier outcomes."""
    out = {}
    # Every origin, INCLUDING the last one, which has no resolved cells of its
    # own and is exactly the origin the forward projection is struck from. A
    # first cut iterated over origins present in the error table and so had no
    # estimate for the only origin that needed one.
    seen_origins = {r["origin"] for r in rows}
    origins = sorted(seen_origins | {BU.LAST_ORIGIN})
    for o in origins:
        seen = [r["log_error"] for r in rows if r["year"] < o]
        if len(seen) < 4:
            continue
        mu = statistics.fmean(seen)
        sd = statistics.pstdev(seen) if len(seen) > 1 else 0.0
        # reset after a structural break: a driver error beyond its own two-sigma
        recent = [r["log_error"] for r in rows if r["year"] == o - 1]
        broke = bool(recent) and sd > 0 and any(abs(e - mu) > TWO_SIGMA * sd for e in recent)
        out[o] = {"n_resolved": len(seen), "bias": mu, "sd": sd,
                  "applied": 0.0 if broke else HALF * mu,
                  "reset_after_break": broke}
    return out


def test_correction(rows, est):
    """Adjusted versus raw, by origin, on the origins that HAD a correction."""
    per_origin, adj_all, raw_all = [], [], []
    for o, e in sorted(est.items()):
        sel = [r for r in rows if r["origin"] == o]
        if not sel or e["applied"] == 0.0:
            continue
        raw = [abs(r["log_error"]) for r in sel]
        adj = [abs(r["log_error"] - e["applied"]) for r in sel]
        per_origin.append({"origin": o, "n": len(sel), "applied": e["applied"],
                           "mae_raw": statistics.fmean(raw),
                           "mae_adjusted": statistics.fmean(adj),
                           "improved": statistics.fmean(adj) < statistics.fmean(raw)})
        raw_all += raw
        adj_all += adj
    if not raw_all:
        return None
    return {"by_origin": per_origin,
            "mae_raw": statistics.fmean(raw_all),
            "mae_adjusted": statistics.fmean(adj_all),
            "origins_improved": sum(1 for p in per_origin if p["improved"]),
            "origins_tested": len(per_origin),
            "passes_own_test": statistics.fmean(adj_all) < statistics.fmean(raw_all)}


def main():
    rows = json.load(open(os.path.join(HERE, "error_cells.json")))
    scores = json.load(open(os.path.join(HERE, "scores.json")))
    d = by_driver(rows)

    log, adopted, watch, refused = {}, [], [], []
    for drv, rs in sorted(d.items()):
        s = scores.get("asknown|%s|all" % drv)
        if not s:
            continue
        gate_robust = s["robust_sign"]
        gate_era = s["sign_holds_across_eras"]
        est = expanding_estimates(rs)
        test = test_correction(rs, est) if (gate_robust and gate_era) else None
        practice = CLASS_PRACTICE.get(drv)
        entry = {"driver": drv, "pooled_bias": s["bias"], "pooled_mae": s["mae"],
                 "n": s["n"], "by_era": s["by_era"],
                 "gate_robust_bootstrap": gate_robust,
                 "gate_sign_holds_across_eras": gate_era,
                 "expanding_estimates": est, "own_test": test,
                 "class_consistency": practice}
        if not gate_robust:
            entry["outcome"] = "no correction — the bias is not robust across bootstrap blocks"
            refused.append(entry)
        elif not gate_era:
            entry["outcome"] = ("no correction — the bias changes sign between eras. "
                                "That is instability, not a bias, and the average of "
                                "two opposite regimes was true in neither [L-029]")
            refused.append(entry)
        elif not test or not test["passes_own_test"]:
            entry["outcome"] = "no correction — it failed its own adjusted-versus-raw test"
            refused.append(entry)
        elif practice and not practice["consistent"]:
            entry["outcome"] = ("WATCH FLAG — it passed its own test and FAILED the "
                                "class-consistency clause. Recorded, graded live, "
                                "revisited at the next update, acted on by nobody")
            watch.append(entry)
        else:
            entry["outcome"] = "ADOPTED at half strength"
            adopted.append(entry)
        log[drv] = entry

    json.dump({"adopted": [e["driver"] for e in adopted],
               "watch_flags": [e["driver"] for e in watch],
               "refused": [e["driver"] for e in refused],
               "detail": log},
              open(os.path.join(HERE, "corrections_log.json"), "w"), indent=1)

    print("%-24s %8s %6s %6s %9s %9s  %s"
          % ("driver", "bias", "robust", "eras", "MAE raw", "MAE adj", "outcome"))
    for drv, e in sorted(log.items(), key=lambda kv: kv[1]["pooled_bias"]):
        t = e["own_test"]
        print("%-24s %+8.3f %6s %6s %9s %9s  %s"
              % (drv, e["pooled_bias"],
                 "YES" if e["gate_robust_bootstrap"] else "no",
                 {True: "same", False: "FLIP", None: "n/a"}[e["gate_sign_holds_across_eras"]],
                 "%.3f" % t["mae_raw"] if t else "-",
                 "%.3f" % t["mae_adjusted"] if t else "-",
                 e["outcome"][:74]))
    print("\nADOPTED: %s" % (", ".join(x["driver"] for x in adopted) or "none"))
    print("WATCH:   %s" % (", ".join(x["driver"] for x in watch) or "none"))


if __name__ == "__main__":
    main()
