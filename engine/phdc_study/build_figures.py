"""Regenerate every delivered figure from study_numbers.json.

The figures used to have no committed caller at all: they were produced once by
hand and then only ever CHECKED — for transparency, for label collisions —
which meant a model change left them stale while the check went on reporting
them clean. An empty result is not a clean result. This script is the caller,
it is run by the gate before the check, and every number in every figure is
read from the numbers file rather than typed.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import figures as F

N = json.load(open(os.path.join(HERE, "study_numbers.json")))


def main():
    spot = N["price_map"]["spot"]
    S, D = N["sensitivity"], N["derived"]
    # Each bar is one observed conversion rate, spanning the discount rate from
    # four points below the rebuilt cost of capital to four points above, with
    # the tick at the rebuilt rate itself — read straight off the published
    # grid, so the figure and the sensitivity table cannot disagree.
    mid_i = len(S["waccs"]) // 2
    bars = []
    for gi, ci, tag in ((0, 1, "weakest of the three published years"),
                        (2, 0, "three-year mean"),
                        (4, 2, "strongest of the three published years")):
        rowv = S["grid"][gi]
        bars.append(("Cash conversion %.1f%%\n(%s)" % (100 * S["cfos"][gi], tag),
                     min(rowv), max(rowv), rowv[mid_i], ci))
    bars.append(("Book equity per share", D["book_equity_per_share"],
                 D["book_equity_per_share"], None, 3))

    out = [F.fig1_football(bars, spot, D["prior_edition_fair"]["base"]),
           F.fig2_sensitivity(S["waccs"], S["cfos"], S["grid"], spot),
           F.fig3_cone(N["price_map"]["dist"], spot, N["price_map"]["touch"]),
           F.fig4_peers([p for p in N["peers"] if "beta" in p])]
    F.assert_opaque(out)
    for p in out:
        print("  %-24s %7d bytes" % (os.path.basename(p), os.path.getsize(p)))
    print("%d figures rebuilt, all opaque" % len(out))
    return out


if __name__ == "__main__":
    main()
