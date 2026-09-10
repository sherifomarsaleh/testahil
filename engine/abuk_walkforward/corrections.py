"""ABUK fundamental walk-forward — corrections, under the two-clause test.

Expanding window only. Half strength by default. A correction is even PROPOSED
only where the driver's bias holds its sign across both eras; every driver whose
sign changes is reported as instability and is not corrected for.
"""
import json, math, os
import bottom_up as bu

HERE = os.path.dirname(os.path.abspath(__file__))
ORIGINS = bu.ORIGINS
STRENGTH = 0.5


def expanding_bias(panel, macro, o, driver):
    """Bias on that driver using ONLY origins resolved strictly before o."""
    es = []
    for prev in ORIGINS:
        if bu._y(prev) >= bu._y(o):
            continue
        proj = bu.project(panel, macro, prev)
        for t, row in proj.items():
            if bu._y(t) > bu._y(o):        # not resolved by the time o is set
                continue
            p, a = row.get(driver), panel["years"][t].get(driver)
            if p and a and p > 0 and a > 0:
                es.append(math.log(p / a))
    return (sum(es) / len(es), len(es)) if es else (None, 0)


def main():
    panel, macro = bu.load()
    scores = json.load(open(os.path.join(HERE, "scores.json")))
    diag = json.load(open(os.path.join(HERE, "diagnostics.json")))

    proposed, blocked = [], []
    for d in ("vol_proxy", "cogs", "sell", "admin", "nonop"):
        st = diag["era_stability"].get(d)
        s = scores["model"]["drivers"][d]
        if not st or not st["same_sign"]:
            blocked.append(dict(driver=d, reason="the bias changes sign between "
                                "eras — that is instability, not a bias, and it "
                                "is reported rather than corrected for",
                                pre=st["pre_bias"] if st else None,
                                post=st["post_bias"] if st else None))
            continue
        ci = s["ci90_bias"]
        if ci[0] * ci[1] <= 0:
            blocked.append(dict(driver=d, reason="the 90% block-bootstrap "
                                "interval on the bias straddles zero",
                                ci90=ci))
            continue
        proposed.append(dict(driver=d, bias=s["bias"], ci90=ci,
                             factor=math.exp(-STRENGTH * s["bias"])))

    results = []
    for pr in proposed:
        d = pr["driver"]
        key = {"vol_proxy": "vol"}.get(d, d)
        by_origin = []
        for o in ORIGINS:
            b, n = expanding_bias(panel, macro, o, d)
            if b is None:
                by_origin.append(dict(origin=o, note="no resolved history at this "
                                      "origin — the correction cannot be formed "
                                      "and the raw projection stands"))
                continue
            f = math.exp(-STRENGTH * b)
            raw = bu.project(panel, macro, o)
            adj = bu.project(panel, macro, o, corr={key: f})
            def m(p, dr):
                es = [abs(math.log(r[dr] / panel["years"][t][dr]))
                      for t, r in p.items()
                      if r.get(dr) and panel["years"][t].get(dr)
                      and r[dr] > 0 and panel["years"][t][dr] > 0]
                return sum(es) / len(es) if es else None
            by_origin.append(dict(origin=o, expanding_bias=b, n_resolved=n,
                                  factor=f,
                                  mae_raw_driver=m(raw, d), mae_adj_driver=m(adj, d),
                                  mae_raw_np=m(raw, "np"), mae_adj_np=m(adj, "np")))
        ok = [r for r in by_origin if "mae_raw_np" in r]
        improved = sum(1 for r in ok if r["mae_adj_np"] < r["mae_raw_np"])
        results.append(dict(driver=d, proposed=pr, by_origin=by_origin,
                            origins_tested=len(ok), origins_improved=improved))

    doc = dict(strength=STRENGTH, proposed=proposed, blocked=blocked,
               tests=results)
    json.dump(doc, open(os.path.join(HERE, "corrections_log.json"), "w"),
              indent=1, sort_keys=True, default=float)
    return doc


if __name__ == "__main__":
    d = main()
    print("BLOCKED before any test was run:")
    for b in d["blocked"]:
        print("  %-10s %s" % (b["driver"], b["reason"]))
    print("\nPROPOSED (bias holds its sign across eras and its interval excludes zero):")
    for p in d["proposed"]:
        print("  %-10s bias %+.3f  CI90 [%+.3f, %+.3f]  half-strength factor %.4f"
              % (p["driver"], p["bias"], p["ci90"][0], p["ci90"][1], p["factor"]))
    for t in d["tests"]:
        print("\nadjusted vs raw, by origin — driver %s" % t["driver"])
        for r in t["by_origin"]:
            if "note" in r:
                print("  %-8s %s" % (r["origin"], r["note"]))
            else:
                print("  %-8s expanding bias %+.3f (n=%d) factor %.4f | driver MAE "
                      "%.3f -> %.3f | net profit MAE %.3f -> %.3f  %s" % (
                          r["origin"], r["expanding_bias"], r["n_resolved"],
                          r["factor"], r["mae_raw_driver"], r["mae_adj_driver"],
                          r["mae_raw_np"], r["mae_adj_np"],
                          "better" if r["mae_adj_np"] < r["mae_raw_np"] else "WORSE"))
        print("  -> improved net profit at %d of %d origins tested"
              % (t["origins_improved"], t["origins_tested"]))
