"""AMOC walk-forward — what this record licenses the study to say about years 3-5.

[R-FCAL-01] requires the delivered study to publish years 3-5 as RANGES built
from this record's own driver-error distribution, never as points. This module
builds those ranges and, just as importantly, states what they are not.

WITH NINE CELLS THERE IS NO DISTRIBUTION TO TAKE PERCENTILES OF. Each horizon
holds 4, 3 and 2 observations. A p10/p90 computed on two numbers is a pair of
numbers wearing the costume of a distribution, so this module reports the SPAN
(min, max) and the bias-and-mean-absolute-error band, labels the count beside
every figure, and refuses to print a percentile it cannot support. A figure that
cannot separate an honest read from a broken one is not published at that scope.
"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import score as S
import bottom_up as B
import diagnose as D
import panel as P

KEYS = ["net_sales", "cost_of_sales", "gross_profit", "majority"]


def errors_by_h(basis):
    """log errors per horizon under a named basis."""
    out = {h: [] for h in B.HORIZONS}
    for o, h, t in B.cells():
        a = B.actual(t)
        if basis == "prereg":
            p = B.project(o, h)
        elif basis == "ppp":
            p = D.ppp_project(o, h)
        else:
            p = B.project(o, h, foresight=True)
        rec = {}
        for k in KEYS:
            rec[k] = S.logerr(p[k], a[k])
        out[h].append(rec)
    return out


def band(vals):
    v = [x for x in vals if x is not None]
    if not v:
        return None
    n = len(v)
    bias = sum(v) / n
    mae = sum(abs(x) for x in v) / n
    return {"n": n, "bias": bias, "mae": mae, "min": min(v), "max": max(v),
            "low_factor": math.exp(bias - mae), "high_factor": math.exp(bias + mae),
            "span_low_factor": math.exp(min(v)), "span_high_factor": math.exp(max(v))}


def main():
    res = {"note": ("Ranges are stated as MULTIPLIERS to apply to a point projection. A factor "
                    "below 1.0 means the record says the method came in BELOW the outturn and "
                    "the point should be read as a floor. Every figure carries its count."),
           "counts_warning": ("4, 3 and 2 observations at horizons 1, 2 and 3. No percentile is "
                              "computed on those counts; the span and the bias/MAE band are what "
                              "the record supports."),
           "bases": {}}
    for basis in ("prereg", "ppp", "foresight"):
        eb = errors_by_h(basis)
        res["bases"][basis] = {
            str(h): {k: band([r[k] for r in eb[h]]) for k in KEYS} for h in B.HORIZONS}

    # What the study should carry. The pre-registered record is the evidence of
    # record; the PPP run is a post-hoc diagnostic and cannot set a published
    # range on its own. Where they disagree the WIDER band is published, because
    # a range narrower than our demonstrated ignorance is a false precision.
    pub = {}
    for h in B.HORIZONS:
        pub[str(h)] = {}
        for k in KEYS:
            a = res["bases"]["prereg"][str(h)][k]
            b = res["bases"]["ppp"][str(h)][k]
            if not a or not b:
                continue
            lo = min(a["low_factor"], b["low_factor"])
            hi = max(a["high_factor"], b["high_factor"])
            pub[str(h)][k] = {"n": a["n"], "low_factor": lo, "high_factor": hi,
                              "width_x": hi / lo}
    res["published_band"] = pub
    res["published_band_rule"] = ("The wider of the pre-registered band and the PPP diagnostic "
                                  "band, per horizon per line. The pre-registered record is the "
                                  "evidence; the diagnostic cannot narrow a published range.")
    json.dump(res, open(os.path.join(HERE, "forward_ranges.json"), "w"), indent=1, default=str)
    return res


if __name__ == "__main__":
    r = main()
    print("FORWARD RANGES — multiplicative bands this record supports\n")
    print("%-14s %-3s %-28s %-28s" % ("line", "h", "pre-registered band", "PPP diagnostic band"))
    print("-" * 78)
    for k in KEYS:
        for h in ("1", "2", "3"):
            a = r["bases"]["prereg"][h][k]
            b = r["bases"]["ppp"][h][k]
            print("%-14s %-3s %-28s %-28s"
                  % (k if h == "1" else "", h,
                     "x%.2f - x%.2f  (n=%d)" % (a["low_factor"], a["high_factor"], a["n"]),
                     "x%.2f - x%.2f" % (b["low_factor"], b["high_factor"])))
    print("\nPUBLISHED BAND (the wider of the two, per horizon):")
    for h in ("1", "2", "3"):
        for k in KEYS:
            p = r["published_band"][h].get(k)
            if p:
                print("  h=%s %-14s x%.2f - x%.2f  (%.1fx wide, n=%d)"
                      % (h, k, p["low_factor"], p["high_factor"], p["width_x"], p["n"]))
