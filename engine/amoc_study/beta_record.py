"""AMOC beta — the sanctioned route, replacing this study's composite regression.

WHAT THIS REPLACES AND WHY IT MATTERS. The previous edition regressed AMOC's weekly
returns against a 33-name EQUAL-WEIGHT COMPOSITE of the Egyptian names this engine
happens to cover, and recorded beta 0.9405 with `usable: true`. That is a hard SIGCM
clause-6 failure: a composite of covered names is a coverage artefact, not a market —
it changes whenever a stock is posted, and it shares constituents with the panel it
prices. The rule against it was already written down while every study in this
repository did it anyway, which is why the check now runs from outside the study.

Nothing here hand-rolls a regression. `beta_regression.own_stock_beta()` resolves the
regressor itself — the PUBLISHED index of the exchange the stock is listed on, read from
engine/raw_indices/ — runs Step 0.0 on both series, matches the weekly grid to the EGX's
real trading week, and returns provenance with the number.

THE SIZE OF THE CORRECTION IS WORTH RECORDING, because it is not what the precedent
suggests. On FERTIGLB the composite understated beta by about 40% and overstated fair
value by 21.6%. Here the composite gave 0.9405 against the published index's 0.9080 —
about 3.5% too high, and it moves fair value by well under a percent. The defect was
real and had to be fixed; its MAGNITUDE on this name is small, and saying so is more
useful than implying every composite beta was wrong by the same amount.
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import beta_regression
import research_protocol as rp

SUPERSEDED = {"beta": 0.9404669016938088, "r2": 0.31243483206998157, "n": 257,
              "se": 0.08736764640128777, "regressor": "33-name equal-weight EGX composite",
              "why_withdrawn": ("A constituent composite is a coverage artefact, not a market. "
                                "SIGCM clause 6 hard fail; never a fallback and never a tier.")}


def main():
    rec = beta_regression.own_stock_beta("AMOC", "EG", "EGX")
    rp.assert_beta_provenance(rec)              # raises unless the regressor is a published index
    rec["superseded_composite"] = SUPERSEDED
    rec["standard_version"] = rp.STANDARD_VERSION
    with open(os.path.join(HERE, "beta_result.json"), "w") as f:
        json.dump(rec, f, indent=1, default=str)
    print("AMOC beta %.4f vs %s (as of %s)" % (rec["beta"], rec["index_file"], rec["index_asof"]))
    print("  R2 %.4f  n=%d  SE %.4f  usable=%s  conforming=%s"
          % (rec["r2"], rec["n"], rec["se"], rec["usable"], rec["conforming"]))
    print("  superseded composite %.4f -> published index %.4f (%+.1f%%)"
          % (SUPERSEDED["beta"], rec["beta"], 100 * (rec["beta"] / SUPERSEDED["beta"] - 1)))
    return rec


if __name__ == "__main__":
    main()
